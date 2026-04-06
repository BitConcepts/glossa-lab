"""Ollama integration API.

Connects to a local Ollama instance at http://localhost:11434.

Endpoints:
  GET  /ollama/status           -- is Ollama running?
  GET  /ollama/installed         -- list installed models
  GET  /ollama/library           -- curated model catalog with GPU requirements
  GET  /ollama/recommend         -- GPU-aware model recommendation
  POST /ollama/pull/{model}      -- SSE stream: download model with progress
  DELETE /ollama/models/{model}  -- delete a model
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/ollama", tags=["ollama"])

OLLAMA_BASE = "http://localhost:11434"

# ── Context length recommendations by VRAM tier ────────────────────────────────

_CTX_TIERS: list[dict[str, Any]] = [
    {
        "min_vram_gb": 0,
        "max_vram_gb": 0,
        "label": "CPU-only",
        "ctx": 2048,
        "note": "Limited RAM; keep context small",
    },
    {
        "min_vram_gb": 0,
        "max_vram_gb": 4,
        "label": "2-4 GB VRAM",
        "ctx": 4096,
        "note": "Suitable for short conversations",
    },
    {
        "min_vram_gb": 4,
        "max_vram_gb": 8,
        "label": "4-8 GB VRAM",
        "ctx": 8192,
        "note": "Good balance of speed and context",
    },
    {
        "min_vram_gb": 8,
        "max_vram_gb": 16,
        "label": "8-16 GB VRAM",
        "ctx": 16384,
        "note": "Full document analysis possible",
    },
    {
        "min_vram_gb": 16,
        "max_vram_gb": 24,
        "label": "16-24 GB VRAM",
        "ctx": 32768,
        "note": "Large research documents",
    },
    {
        "min_vram_gb": 24,
        "max_vram_gb": 999,
        "label": "24+ GB VRAM",
        "ctx": 65536,
        "note": "Full corpus context possible",
    },
]

# Session context length — stored in memory, updated via API
_session_ctx_length: int = 4096


# ── Curated model library ─────────────────────────────────────────────────────

LIBRARY: list[dict[str, Any]] = [
    # Small (< 4 GB VRAM) — good for low-end GPUs or CPU-only
    {
        "name": "llama3.2:3b",
        "display": "Llama 3.2 3B",
        "family": "llama",
        "size_gb": 2.0,
        "min_vram_gb": 0,
        "param_b": 3,
        "desc": "Meta's latest small model. Fast, capable, runs on CPU.",
        "quality": "good",
        "glossa_score": 7,
        "tags": ["fast", "cpu-friendly"],
    },
    {
        "name": "mistral:7b-instruct-q4_0",
        "display": "Mistral 7B Instruct (Q4)",
        "family": "mistral",
        "size_gb": 4.1,
        "min_vram_gb": 4,
        "param_b": 7,
        "desc": "Excellent instruction-following. Best small model for structured JSON output.",
        "quality": "great",
        "glossa_score": 9,
        "tags": ["structured-output", "json", "recommended"],
    },
    {
        "name": "phi4:14b-q4_K_M",
        "display": "Phi-4 14B (Q4)",
        "family": "phi",
        "size_gb": 8.5,
        "min_vram_gb": 6,
        "param_b": 14,
        "desc": "Microsoft's Phi-4. Exceptional reasoning for its size.",
        "quality": "great",
        "glossa_score": 8,
        "tags": ["reasoning"],
    },
    {
        "name": "gemma3:9b",
        "display": "Gemma 3 9B",
        "family": "gemma",
        "size_gb": 5.4,
        "min_vram_gb": 6,
        "param_b": 9,
        "desc": "Google's Gemma 3. Good multimodal understanding.",
        "quality": "great",
        "glossa_score": 7,
        "tags": ["google"],
    },
    # Medium (8–16 GB VRAM)
    {
        "name": "llama3.1:8b",
        "display": "Llama 3.1 8B",
        "family": "llama",
        "size_gb": 4.7,
        "min_vram_gb": 5,
        "param_b": 8,
        "desc": "Meta's Llama 3.1. Strong general reasoning and instruction-following.",
        "quality": "great",
        "glossa_score": 8,
        "tags": ["general"],
    },
    {
        "name": "mistral-nemo:12b",
        "display": "Mistral NeMo 12B",
        "family": "mistral",
        "size_gb": 7.1,
        "min_vram_gb": 8,
        "param_b": 12,
        "desc": "Mistral + NVIDIA collaboration. Best structured output at 12B scale. Top pick for Glossa Lab.",
        "quality": "excellent",
        "glossa_score": 10,
        "tags": ["structured-output", "json", "top-pick", "recommended"],
    },
    {
        "name": "qwen2.5:14b",
        "display": "Qwen 2.5 14B",
        "family": "qwen",
        "size_gb": 8.9,
        "min_vram_gb": 10,
        "param_b": 14,
        "desc": "Alibaba's Qwen 2.5. Excellent at multilingual and linguistics tasks.",
        "quality": "excellent",
        "glossa_score": 9,
        "tags": ["multilingual", "linguistics"],
    },
    {
        "name": "deepseek-r1:14b",
        "display": "DeepSeek R1 14B",
        "family": "deepseek",
        "size_gb": 9.0,
        "min_vram_gb": 10,
        "param_b": 14,
        "desc": "DeepSeek's reasoning model. Very strong at analytical and research tasks.",
        "quality": "excellent",
        "glossa_score": 9,
        "tags": ["reasoning", "research"],
    },
    # Large (24+ GB VRAM)
    {
        "name": "llama3.1:70b-instruct-q4_K_M",
        "display": "Llama 3.1 70B (Q4)",
        "family": "llama",
        "size_gb": 40.0,
        "min_vram_gb": 24,
        "param_b": 70,
        "desc": "Full-scale Llama 3.1. Excellent for complex research and multi-step reasoning.",
        "quality": "excellent",
        "glossa_score": 9,
        "tags": ["large", "research"],
    },
    {
        "name": "mixtral:8x7b-instruct-q4_K_M",
        "display": "Mixtral 8x7B (Q4)",
        "family": "mistral",
        "size_gb": 26.4,
        "min_vram_gb": 24,
        "param_b": 47,
        "desc": "Mistral's MoE model. Excellent reasoning and structured output at large scale.",
        "quality": "excellent",
        "glossa_score": 9,
        "tags": ["moe", "reasoning"],
    },
    {
        "name": "deepseek-r1:70b",
        "display": "DeepSeek R1 70B",
        "family": "deepseek",
        "size_gb": 43.0,
        "min_vram_gb": 32,
        "param_b": 70,
        "desc": "DeepSeek's largest reasoning model. State-of-the-art for complex research.",
        "quality": "excellent",
        "glossa_score": 10,
        "tags": ["reasoning", "research", "top-pick"],
    },
]


def _ollama_get(path: str, timeout: int = 5) -> Any:
    """GET from Ollama API. Raises urllib.error.URLError if unavailable."""
    req = urllib.request.Request(f"{OLLAMA_BASE}{path}", method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _is_running() -> bool:
    try:
        _ollama_get("/api/tags", timeout=2)
        return True
    except Exception:  # noqa: BLE001
        return False


# ── Endpoints ──────────────────────────────────────────────────────────────────


def _recommended_ctx(vram_gb: float) -> dict[str, Any]:
    """Return context-length recommendation for the given VRAM amount."""
    for tier in reversed(_CTX_TIERS):
        if vram_gb >= tier["min_vram_gb"] or (
            vram_gb == 0 and tier["min_vram_gb"] == 0 and tier["max_vram_gb"] == 0
        ):
            return tier
    return _CTX_TIERS[0]  # fallback: CPU-only


class ContextConfigRequest(BaseModel):
    ctx_length: int


@router.get("/context-config")
async def get_context_config() -> dict[str, Any]:
    """Return current session context length and all available tiers."""
    return {
        "session_ctx_length": _session_ctx_length,
        "tiers": _CTX_TIERS,
        "all_options": [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072],
    }


@router.post("/context-config")
async def set_context_config(body: ContextConfigRequest) -> dict[str, Any]:
    """Set the session context length. Stored in memory until restart."""
    global _session_ctx_length  # noqa: PLW0603
    valid = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
    if body.ctx_length not in valid:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=f"ctx_length must be one of: {valid}")
    _session_ctx_length = body.ctx_length
    return {"session_ctx_length": _session_ctx_length, "updated": True}


@router.get("/status")
async def ollama_status() -> dict[str, Any]:
    """Check if Ollama is running locally."""
    running = _is_running()
    return {
        "running": running,
        "base_url": OLLAMA_BASE,
        "message": "Ollama is running"
        if running
        else "Ollama is not running. Install from https://ollama.com",
    }


@router.get("/installed")
async def list_installed() -> dict[str, Any]:
    """List all locally installed Ollama models with details."""
    if not _is_running():
        return {"running": False, "models": []}
    try:
        data = _ollama_get("/api/tags")
        models = data.get("models", [])
        # Enrich with library metadata
        enriched = []
        for m in models:
            lib_entry = next((e for e in LIBRARY if e["name"] == m["name"]), None)
            enriched.append(
                {
                    "name": m["name"],
                    "size_gb": round(m.get("size", 0) / 1_073_741_824, 2),
                    "modified_at": m.get("modified_at", ""),
                    "digest": m.get("digest", "")[:16],
                    "family": lib_entry["family"] if lib_entry else "unknown",
                    "display": lib_entry["display"] if lib_entry else m["name"],
                    "glossa_score": lib_entry["glossa_score"] if lib_entry else None,
                    "tags": lib_entry.get("tags", []) if lib_entry else [],
                }
            )
        return {"running": True, "models": enriched, "count": len(enriched)}
    except Exception as exc:  # noqa: BLE001
        return {"running": True, "models": [], "error": str(exc)}


@router.get("/library")
async def get_library() -> dict[str, Any]:
    """Return curated model library with GPU requirements and Glossa Lab scores."""
    # Mark which are installed
    installed: set[str] = set()
    if _is_running():
        try:
            data = _ollama_get("/api/tags")
            installed = {m["name"] for m in data.get("models", [])}
        except Exception:  # noqa: BLE001
            pass

    lib = [{**entry, "installed": entry["name"] in installed} for entry in LIBRARY]
    return {
        "running": _is_running(),
        "models": lib,
        "installed_names": list(installed),
    }


@router.get("/recommend")
async def recommend_model() -> dict[str, Any]:
    """Recommend the best Ollama model for Glossa Lab based on available GPU VRAM."""
    import platform
    import subprocess

    vram_gb = 0.0
    gpu_name = ""

    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL,
            timeout=3,
            creationflags=0x08000000 if platform.system() == "Windows" else 0,
        )
        parts = out.decode(errors="replace").strip().split(",")
        if len(parts) >= 2:
            gpu_name = parts[0].strip()
            vram_gb = float(parts[1].strip()) / 1024
    except Exception:  # noqa: BLE001
        pass

    # Find best fitting models
    fitting = sorted(
        [m for m in LIBRARY if m["min_vram_gb"] <= vram_gb + 2 or vram_gb == 0],
        key=lambda m: (-m["glossa_score"], -m["param_b"]),
    )
    top_pick = fitting[0] if fitting else LIBRARY[0]

    # Tier description
    if vram_gb == 0:
        tier = "cpu_only"
        tier_desc = "No GPU detected — CPU-only mode. Use small quantized models."
    elif vram_gb < 4:
        tier = "low_vram"
        tier_desc = f"{gpu_name} ({vram_gb:.1f} GB VRAM). Small quantized models recommended."
    elif vram_gb < 10:
        tier = "mid_vram"
        tier_desc = f"{gpu_name} ({vram_gb:.1f} GB VRAM). Mid-range models available."
    else:
        tier = "high_vram"
        tier_desc = f"{gpu_name} ({vram_gb:.1f} GB VRAM). Large models supported."

    ctx_rec = _recommended_ctx(vram_gb)
    return {
        "gpu_name": gpu_name or "Not detected",
        "vram_gb": round(vram_gb, 1),
        "tier": tier,
        "tier_description": tier_desc,
        "recommended": top_pick,
        "all_fitting": [m["name"] for m in fitting[:5]],
        "recommended_ctx_length": ctx_rec["ctx"],
        "ctx_tier_label": ctx_rec["label"],
        "ctx_tier_note": ctx_rec["note"],
        "ctx_tiers": _CTX_TIERS,
        "glossa_note": (
            "Mistral NeMo 12B or Mistral 7B are best for Glossa Lab — "
            "they produce clean structured JSON for AI summaries, hypothesis generation, "
            "and decipherment assistance."
        ),
    }


@router.delete("/models/{model_name:path}")
async def delete_model(model_name: str) -> dict[str, Any]:
    """Delete a locally installed Ollama model."""
    if not _is_running():
        raise HTTPException(status_code=503, detail="Ollama is not running")
    try:
        body = json.dumps({"name": model_name}).encode()
        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/delete",
            data=body,
            headers={"Content-Type": "application/json"},
            method="DELETE",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            _ = resp.read()
        return {"deleted": True, "model": model_name}
    except urllib.error.HTTPError as exc:
        raise HTTPException(
            status_code=exc.code, detail=f"Ollama error: {exc.read().decode()[:200]}"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def _pull_stream(model_name: str) -> AsyncGenerator[str, None]:
    """Stream Ollama pull progress as SSE frames."""
    import asyncio

    try:
        body = json.dumps({"name": model_name}).encode()

        def _blocking_pull() -> list[dict[str, Any]]:
            events: list[dict[str, Any]] = []
            try:
                req = urllib.request.Request(
                    f"{OLLAMA_BASE}/api/pull",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=3600) as resp:
                    while True:
                        line = resp.readline()
                        if not line:
                            break
                        try:
                            events.append(json.loads(line.decode()))
                        except Exception:  # noqa: BLE001
                            pass
            except Exception as exc:  # noqa: BLE001
                events.append({"status": "error", "error": str(exc)})
            return events

        # Run in thread and yield as we get events
        loop = asyncio.get_event_loop()

        # Use a queue-based approach for streaming from a thread
        import queue
        import threading

        q: queue.Queue[dict[str, Any] | None] = queue.Queue()

        def _stream_pull() -> None:
            try:
                req = urllib.request.Request(
                    f"{OLLAMA_BASE}/api/pull",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=3600) as resp:
                    while True:
                        line = resp.readline()
                        if not line:
                            break
                        try:
                            event = json.loads(line.decode())
                            q.put(event)
                        except Exception:  # noqa: BLE001
                            pass
            except Exception as exc:  # noqa: BLE001
                q.put({"status": "error", "error": str(exc)})
            finally:
                q.put(None)  # sentinel

        t = threading.Thread(target=_stream_pull, daemon=True)
        t.start()

        while True:
            try:
                event = await loop.run_in_executor(None, lambda: q.get(timeout=120))
            except Exception:  # noqa: BLE001
                break
            if event is None:
                break
            yield f"data: {json.dumps(event)}\n\n"
            if event.get("status") in ("success", "error"):
                break

    except Exception as exc:  # noqa: BLE001
        yield f"data: {json.dumps({'status': 'error', 'error': str(exc)})}\n\n"


@router.get("/pull/{model_name:path}")
async def pull_model(model_name: str) -> StreamingResponse:
    """Start downloading a model via SSE stream.

    Uses GET so browsers can use EventSource.
    Each event: {status, digest, total, completed} or {status: 'success'} at end.
    """
    if not _is_running():
        raise HTTPException(status_code=503, detail="Ollama is not running. Start Ollama first.")
    return StreamingResponse(
        _pull_stream(model_name),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
