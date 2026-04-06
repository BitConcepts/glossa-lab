"""System metrics API — live hardware monitoring.

Endpoints:
  GET  /system/metrics         -- single snapshot (CPU, RAM, GPU, disk, network)
  GET  /system/metrics/stream  -- SSE stream at 1-second interval
  GET  /system/gpu             -- GPU info only (nvidia-smi)
  POST /system/peaks/clear     -- reset peak readings
"""

from __future__ import annotations

import asyncio
import json
import platform
import subprocess
import time
from collections.abc import AsyncGenerator
from typing import Any

import psutil
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/system", tags=["system"])

# Peak tracker (module-level, reset-able)
_peaks: dict[str, float] = {
    "cpu_pct": 0.0,
    "ram_pct": 0.0,
    "gpu_pct": 0.0,
    "gpu_mem_pct": 0.0,
    "net_send_mbps": 0.0,
    "net_recv_mbps": 0.0,
    "disk_read_mbps": 0.0,
    "disk_write_mbps": 0.0,
}

# Counters for delta calculations
_prev_net: psutil._common.snetio | None = None
_prev_disk: psutil._common.sdiskio | None = None
_prev_time: float = time.monotonic()


def _update_peaks(**vals: float) -> None:
    for k, v in vals.items():
        if k in _peaks and v > _peaks[k]:
            _peaks[k] = v


def _get_gpu_info() -> list[dict[str, Any]]:
    """Query NVIDIA GPU info via nvidia-smi. Returns [] if unavailable."""
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,utilization.memory,temperature.gpu",
                "--format=csv,noheader,nounits",
            ],
            stderr=subprocess.DEVNULL,
            timeout=3,
            creationflags=0x08000000 if platform.system() == "Windows" else 0,
        )
        gpus = []
        for line in out.decode(errors="replace").strip().splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 7:
                continue
            mem_total = float(parts[1]) if parts[1].replace(".", "").isdigit() else 0.0
            mem_used = float(parts[2]) if parts[2].replace(".", "").isdigit() else 0.0
            gpus.append(
                {
                    "name": parts[0],
                    "memory_total_mb": round(mem_total),
                    "memory_used_mb": round(mem_used),
                    "memory_free_mb": round(float(parts[3]))
                    if parts[3].replace(".", "").isdigit()
                    else 0,
                    "utilization_pct": float(parts[4])
                    if parts[4].replace(".", "").isdigit()
                    else 0.0,
                    "memory_utilization_pct": float(parts[5])
                    if parts[5].replace(".", "").isdigit()
                    else 0.0,
                    "temperature_c": float(parts[6])
                    if parts[6].replace(".", "").isdigit()
                    else None,
                }
            )
        return gpus
    except Exception:  # noqa: BLE001
        return []


def _snapshot() -> dict[str, Any]:
    """Collect all metrics in one shot."""
    global _prev_net, _prev_disk, _prev_time  # noqa: PLW0603

    now = time.monotonic()
    elapsed = max(now - _prev_time, 0.001)
    _prev_time = now

    # CPU
    cpu_pct = psutil.cpu_percent(interval=None)
    cpu_count_logical = psutil.cpu_count(logical=True)
    cpu_count_physical = psutil.cpu_count(logical=False) or cpu_count_logical
    cpu_freq = psutil.cpu_freq()
    per_cpu = psutil.cpu_percent(interval=None, percpu=True)

    # RAM
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # Disk I/O delta
    disk_io = psutil.disk_io_counters()
    disk_read_mbps = 0.0
    disk_write_mbps = 0.0
    if _prev_disk and disk_io:
        read_bytes = disk_io.read_bytes - _prev_disk.read_bytes
        write_bytes = disk_io.write_bytes - _prev_disk.write_bytes
        disk_read_mbps = max(0.0, read_bytes / elapsed / 1_000_000)
        disk_write_mbps = max(0.0, write_bytes / elapsed / 1_000_000)
    _prev_disk = disk_io

    # Disk usage (root / C:\)
    root_path = "C:\\" if platform.system() == "Windows" else "/"
    try:
        disk_usage = psutil.disk_usage(root_path)
        disk_total_gb = disk_usage.total / 1_073_741_824
        disk_used_gb = disk_usage.used / 1_073_741_824
        disk_free_gb = disk_usage.free / 1_073_741_824
        disk_pct = disk_usage.percent
    except Exception:  # noqa: BLE001
        disk_total_gb = disk_used_gb = disk_free_gb = disk_pct = 0.0

    # Network I/O delta
    net_io = psutil.net_io_counters()
    net_send_mbps = 0.0
    net_recv_mbps = 0.0
    if _prev_net and net_io:
        sent = net_io.bytes_sent - _prev_net.bytes_sent
        recv = net_io.bytes_recv - _prev_net.bytes_recv
        net_send_mbps = max(0.0, sent / elapsed / 1_000_000)
        net_recv_mbps = max(0.0, recv / elapsed / 1_000_000)
    _prev_net = net_io

    # GPU
    gpus = _get_gpu_info()
    gpu_pct = gpus[0]["utilization_pct"] if gpus else 0.0
    gpu_mem_pct = gpus[0]["memory_utilization_pct"] if gpus else 0.0

    # Update peaks
    _update_peaks(
        cpu_pct=cpu_pct,
        ram_pct=vm.percent,
        gpu_pct=gpu_pct,
        gpu_mem_pct=gpu_mem_pct,
        net_send_mbps=net_send_mbps,
        net_recv_mbps=net_recv_mbps,
        disk_read_mbps=disk_read_mbps,
        disk_write_mbps=disk_write_mbps,
    )

    return {
        "timestamp": time.time(),
        "cpu": {
            "percent": round(cpu_pct, 1),
            "count_logical": cpu_count_logical,
            "count_physical": cpu_count_physical,
            "freq_mhz": round(cpu_freq.current) if cpu_freq else None,
            "freq_max_mhz": round(cpu_freq.max) if cpu_freq else None,
            "per_core_pct": [round(p, 1) for p in per_cpu],
            "peak_pct": _peaks["cpu_pct"],
        },
        "ram": {
            "total_gb": round(vm.total / 1_073_741_824, 1),
            "used_gb": round(vm.used / 1_073_741_824, 1),
            "available_gb": round(vm.available / 1_073_741_824, 1),
            "percent": round(vm.percent, 1),
            "peak_pct": _peaks["ram_pct"],
            "swap_total_gb": round(swap.total / 1_073_741_824, 1),
            "swap_used_gb": round(swap.used / 1_073_741_824, 1),
        },
        "gpu": gpus,
        "gpu_peaks": {
            "utilization_pct": _peaks["gpu_pct"],
            "memory_utilization_pct": _peaks["gpu_mem_pct"],
        },
        "disk": {
            "total_gb": round(disk_total_gb, 1),
            "used_gb": round(disk_used_gb, 1),
            "free_gb": round(disk_free_gb, 1),
            "percent": round(disk_pct, 1),
            "read_mbps": round(disk_read_mbps, 2),
            "write_mbps": round(disk_write_mbps, 2),
            "peak_read_mbps": _peaks["disk_read_mbps"],
            "peak_write_mbps": _peaks["disk_write_mbps"],
        },
        "network": {
            "send_mbps": round(net_send_mbps, 3),
            "recv_mbps": round(net_recv_mbps, 3),
            "peak_send_mbps": _peaks["net_send_mbps"],
            "peak_recv_mbps": _peaks["net_recv_mbps"],
            "total_sent_gb": round(net_io.bytes_sent / 1_073_741_824, 3) if net_io else 0,
            "total_recv_gb": round(net_io.bytes_recv / 1_073_741_824, 3) if net_io else 0,
        },
        "peaks": dict(_peaks),
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.get("/metrics")
async def get_metrics() -> dict[str, Any]:
    """Return a single system metrics snapshot."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _snapshot)


@router.get("/gpu")
async def get_gpu() -> list[dict[str, Any]]:
    """Return GPU information from nvidia-smi."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _get_gpu_info)


@router.post("/peaks/clear")
async def clear_peaks() -> dict[str, Any]:
    """Reset all peak readings to zero."""
    for k in _peaks:
        _peaks[k] = 0.0
    return {"cleared": True, "peaks": dict(_peaks)}


def _sse(data: dict[str, Any]) -> str:
    return f"data: {json.dumps(data)}\n\n"


async def _stream_metrics() -> AsyncGenerator[str, None]:
    """Yield SSE frames of system metrics at ~1-second intervals."""
    # prime the counters
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _snapshot)
    try:
        while True:
            await asyncio.sleep(1.0)
            snap = await loop.run_in_executor(None, _snapshot)
            yield _sse(snap)
    except asyncio.CancelledError:
        return


@router.get("/metrics/stream")
async def stream_metrics() -> StreamingResponse:
    """SSE endpoint streaming system metrics at 1-second intervals."""
    return StreamingResponse(
        _stream_metrics(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
