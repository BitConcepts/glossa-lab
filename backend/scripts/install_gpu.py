#!/usr/bin/env python3
"""Glossa Lab — Smart GPU Package Installer
============================================

Detects the GPU vendor and CUDA/ROCm version on this machine and installs
the correct accelerator package (CuPy for NVIDIA, instructions for AMD).

Run automatically by ``shell.cmd setup`` after base dependencies are installed.
Can also be run standalone:

    python backend/scripts/install_gpu.py
    python backend/scripts/install_gpu.py --quiet     # suppress progress
    python backend/scripts/install_gpu.py --check     # detect only, no install

GPU → package mapping
---------------------
NVIDIA + CUDA 11.x  →  cupy-cuda11x
NVIDIA + CUDA 12.x  →  cupy-cuda12x
NVIDIA + CUDA 13.x  →  cupy-cuda13x
NVIDIA + CUDA 14+   →  cupy-cuda13x  (try latest known; fall back to 12x)
AMD / ROCm          →  print instructions (ROCm CuPy is complex; see docs)
Intel Arc / Xe      →  print instructions
No GPU / CPU-only   →  skip (NumPy already installed by base deps)

After installation, the BigramScorer in ``glossa_lab.pipelines.decipher``
and all parallel seed runners in experiments automatically use the GPU
via CuPy without any code change.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

# ── Helpers ──────────────────────────────────────────────────────────────────

def _run(cmd: list[str], capture: bool = True) -> tuple[int, str]:
    """Run a command and return (returncode, stdout+stderr)."""
    try:
        r = subprocess.run(cmd, capture_output=capture, text=True, timeout=30)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return 1, ""


def _pip_install(pkg: str, quiet: bool = False) -> bool:
    """Install pkg via the current Python's pip. Returns True on success."""
    cmd = [sys.executable, "-m", "pip", "install", pkg]
    if quiet:
        cmd.append("--quiet")
    rc, out = _run(cmd, capture=False)
    return rc == 0


def _pip_installed(pkg_name: str) -> bool:
    """Return True if *pkg_name* (e.g. 'cupy-cuda13x') is already installed."""
    rc, out = _run([sys.executable, "-m", "pip", "show", pkg_name])
    return rc == 0 and "Name:" in out


def _cupy_works() -> bool:
    """Return True if CuPy is importable and CUDA is available."""
    rc, _ = _run([sys.executable, "-c",
                  "import cupy as cp; assert cp.cuda.is_available()"])
    return rc == 0


# ── GPU detection ─────────────────────────────────────────────────────────────

def detect_nvidia() -> dict | None:
    """Detect NVIDIA GPU via nvidia-smi and nvcc.

    Returns dict with keys: name, driver, cuda_major, cuda_minor, vram_mb
    or None if no NVIDIA GPU is found.
    """
    # Try nvidia-smi
    rc, out = _run(["nvidia-smi",
                     "--query-gpu=name,memory.total,driver_version",
                     "--format=csv,noheader,nounits"])
    if rc != 0 or not out.strip():
        return None

    parts = [p.strip() for p in out.strip().split(",")]
    name  = parts[0] if len(parts) > 0 else "NVIDIA GPU"
    vram  = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    drv   = parts[2] if len(parts) > 2 else "unknown"

    # Get CUDA Toolkit version from nvcc (more reliable than smi for toolkit)
    cuda_major, cuda_minor = 0, 0
    rc2, out2 = _run(["nvcc", "--version"])
    if rc2 == 0:
        for line in out2.splitlines():
            if "release" in line.lower():
                # e.g. "Cuda compilation tools, release 13.1, V13.1.115"
                for tok in line.split(","):
                    tok = tok.strip()
                    if tok.lower().startswith("release "):
                        ver = tok.split()[-1]
                        try:
                            major, minor = ver.split(".")
                            cuda_major, cuda_minor = int(major), int(minor)
                        except Exception:  # noqa: BLE001
                            pass

    # Fallback: parse CUDA version from nvidia-smi header
    if cuda_major == 0:
        rc3, out3 = _run(["nvidia-smi"])
        if rc3 == 0:
            for line in out3.splitlines():
                if "CUDA Version:" in line:
                    try:
                        ver = line.split("CUDA Version:")[-1].strip().split()[0]
                        major, minor = ver.split(".")
                        cuda_major, cuda_minor = int(major), int(minor)
                    except Exception:  # noqa: BLE001
                        pass

    return {"name": name, "driver": drv, "cuda_major": cuda_major,
            "cuda_minor": cuda_minor, "vram_mb": vram}


def detect_amd() -> dict | None:
    """Detect AMD GPU via rocm-smi or clinfo."""
    rc, out = _run(["rocm-smi", "--showproductname"])
    if rc == 0 and out.strip():
        return {"vendor": "AMD", "info": out.strip()[:200]}
    # Linux: check /dev/kfd (ROCm kernel fusion driver)
    if Path("/dev/kfd").exists():
        return {"vendor": "AMD", "info": "ROCm KFD found at /dev/kfd"}
    return None


def detect_intel() -> dict | None:
    """Detect Intel discrete GPU via oclinfo or igpu check."""
    rc, out = _run(["oclinfo"])
    if rc == 0 and "Intel" in out:
        return {"vendor": "Intel", "info": "Intel GPU via OpenCL"}
    return None


# ── CuPy package selection ────────────────────────────────────────────────────

def _cupy_package_for_cuda(cuda_major: int) -> list[str]:
    """Return ordered list of CuPy packages to try, best-fit first."""
    if cuda_major <= 0:
        # Unknown CUDA version — try in descending order
        return ["cupy-cuda13x", "cupy-cuda12x", "cupy-cuda11x"]
    if cuda_major == 11:
        return ["cupy-cuda11x", "cupy-cuda12x"]
    if cuda_major == 12:
        return ["cupy-cuda12x", "cupy-cuda13x"]
    if cuda_major == 13:
        return ["cupy-cuda13x", "cupy-cuda12x"]
    if cuda_major >= 14:
        # Future-proof: try newest first
        return ["cupy-cuda13x", "cupy-cuda12x"]
    return ["cupy-cuda12x", "cupy-cuda13x", "cupy-cuda11x"]


# ── Main logic ────────────────────────────────────────────────────────────────

def main(quiet: bool = False, check_only: bool = False) -> int:
    """Main GPU detection and install routine. Returns exit code."""

    def pr(*args, **kw):
        if not quiet:
            print(*args, **kw)

    pr("\n[GPU] Detecting hardware…")

    # ── NVIDIA ──────────────────────────────────────────────────────────────
    nvidia = detect_nvidia()
    if nvidia:
        cuda_ver = f"{nvidia['cuda_major']}.{nvidia['cuda_minor']}"
        pr(f"[GPU] Found NVIDIA: {nvidia['name']} "
           f"({nvidia['vram_mb']} MiB VRAM, CUDA {cuda_ver}, "
           f"driver {nvidia['driver']})")

        if check_only:
            pr(f"[GPU] Would install: {_cupy_package_for_cuda(nvidia['cuda_major'])[0]}")
            return 0

        # Check if CuPy already works
        if _cupy_works():
            pr("[GPU] CuPy already installed and GPU accessible. ✓")
            return 0

        pkgs = _cupy_package_for_cuda(nvidia["cuda_major"])
        for pkg in pkgs:
            if _pip_installed(pkg):
                pr(f"[GPU] {pkg} already installed, verifying GPU access…")
                if _cupy_works():
                    pr("[GPU] GPU accessible. ✓")
                    return 0
                # Installed but broken — try next
                pr(f"[GPU] {pkg} installed but GPU not accessible. Trying next…")
                continue

            pr(f"[GPU] Installing {pkg}…")
            if _pip_install(pkg, quiet=quiet):
                if _cupy_works():
                    pr(f"[GPU] ✓ {pkg} installed — GPU (CUDA {cuda_ver}) is active.")
                    _write_gpu_info(nvidia, pkg)
                    return 0
                pr(f"[GPU] {pkg} installed but GPU not accessible. Trying fallback…")
            else:
                pr(f"[GPU] {pkg} install failed. Trying fallback…")

        pr("[GPU] WARNING: Could not install a working CuPy for this CUDA version.")
        pr(f"[GPU] See docs/GPU_SETUP.md for manual instructions.")
        pr(f"[GPU] GPU vendor: NVIDIA, CUDA: {cuda_ver}")
        pr(f"[GPU] Tried packages: {pkgs}")
        pr("[GPU] Falling back to NumPy (CPU-only). Experiments will still run.")
        return 0

    # ── AMD ─────────────────────────────────────────────────────────────────
    amd = detect_amd()
    if amd:
        pr(f"[GPU] Found AMD GPU: {amd['info']}")
        if not check_only:
            pr("[GPU] AMD ROCm CuPy requires manual setup. See docs/GPU_SETUP.md.")
            pr("[GPU] Quick start:")
            pr("  pip install cupy-rocm-5-0   # for ROCm 5.x")
            pr("  pip install cupy-rocm-6-0   # for ROCm 6.x")
            pr("[GPU] Falling back to NumPy (CPU-only) until ROCm CuPy is installed.")
        return 0

    # ── Intel ────────────────────────────────────────────────────────────────
    intel = detect_intel()
    if intel:
        pr(f"[GPU] Found Intel GPU: {intel['info']}")
        if not check_only:
            pr("[GPU] Intel GPU support requires Intel Extension for PyTorch.")
            pr("[GPU] See docs/GPU_SETUP.md for Intel setup instructions.")
            pr("[GPU] Falling back to NumPy (CPU-only).")
        return 0

    # ── No GPU ───────────────────────────────────────────────────────────────
    pr("[GPU] No GPU detected. NumPy CPU path will be used.")
    pr(f"[GPU] Using {_cpu_info()} for parallel computation.")
    return 0


def _cpu_info() -> str:
    try:
        import multiprocessing
        return f"CPU ({multiprocessing.cpu_count()} cores)"
    except Exception:  # noqa: BLE001
        return "CPU"


def _write_gpu_info(nvidia: dict, pkg: str) -> None:
    """Write GPU detection result to .gpu_info.json for the backend to read."""
    info = {
        "vendor": "nvidia",
        "name": nvidia["name"],
        "vram_mb": nvidia["vram_mb"],
        "driver": nvidia["driver"],
        "cuda_major": nvidia["cuda_major"],
        "cuda_minor": nvidia["cuda_minor"],
        "cupy_package": pkg,
    }
    out = Path(__file__).resolve().parent.parent / ".gpu_info.json"
    try:
        out.write_text(json.dumps(info, indent=2), encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Glossa Lab GPU installer")
    parser.add_argument("--quiet",  "-q", action="store_true", help="Suppress output")
    parser.add_argument("--check",  "-c", action="store_true", help="Detect only, no install")
    args = parser.parse_args()
    sys.exit(main(quiet=args.quiet, check_only=args.check))
