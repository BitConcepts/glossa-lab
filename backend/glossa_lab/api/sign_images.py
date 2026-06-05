"""Sign Images API — management endpoints for the sign image acquisition pipeline.

Endpoints (mounted at /api/v1/signs/images):
  GET  /status              — overall coverage stats + per-sign manifest
  GET  /status/{sign_id}    — single-sign image status
  POST /process             — trigger batch image processing (background task)
  POST /process/{sign_id}   — trigger processing for one sign
  POST /upload/{sign_id}    — manually upload a source image for a sign
  GET  /manifest            — full raw manifest JSON
"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/signs/images", tags=["sign-images"])
_log = logging.getLogger("glossa_lab.api.sign_images")

_STATIC_SIGNS = Path(__file__).resolve().parent.parent.parent / "static" / "signs"

# ── Background task state ─────────────────────────────────────────────────
_processing_lock = asyncio.Lock()
_last_run_stats: dict[str, Any] | None = None
_processing_running = False


# ── Request / response models ─────────────────────────────────────────────

class ProcessRequest(BaseModel):
    force: bool = False
    skip_wikimedia: bool = False
    sign_ids: list[str] | None = None  # None = all signs


# ── Helpers ───────────────────────────────────────────────────────────────

def _get_processor():
    from glossa_lab.tools.sign_image_processor import (  # noqa: PLC0415
        get_status, load_manifest, run_batch, process_single, _load_sign_catalog,
    )
    return get_status, load_manifest, run_batch, process_single, _load_sign_catalog


# ── Endpoints ─────────────────────────────────────────────────────────────

@router.get("/status")
async def images_status() -> dict[str, Any]:
    """Overall image coverage statistics."""
    try:
        get_status, _, _, _, _ = _get_processor()
        status = get_status()
        status["processing_running"] = _processing_running
        status["last_run_stats"] = _last_run_stats
        return status
    except Exception as exc:
        _log.warning("Failed to get sign image status: %s", exc)
        return {"error": str(exc), "processing_running": _processing_running}


@router.get("/manifest")
async def get_manifest() -> dict[str, Any]:
    """Return the full sign image manifest."""
    try:
        _, load_manifest, _, _, _ = _get_processor()
        return load_manifest()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/status/{sign_id}")
async def sign_image_status(sign_id: str) -> dict[str, Any]:
    """Return image status for a single sign."""
    try:
        _, load_manifest, _, _, _ = _get_processor()
        manifest = load_manifest()
        entry = manifest.get(sign_id)
        if entry is None:
            return {
                "sign_id": sign_id,
                "status": "missing",
                "image_url": None,
            }
        img_path = _STATIC_SIGNS / f"{sign_id}.png"
        return {
            "sign_id": sign_id,
            **entry,
            "image_url": f"/static/signs/{sign_id}.png" if img_path.exists() else None,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/process")
async def trigger_batch_process(
    req: ProcessRequest,
    background_tasks: BackgroundTasks,
) -> dict[str, Any]:
    """Trigger batch image acquisition (runs in background).

    Returns immediately; poll /status for progress.
    """
    global _processing_running  # noqa: PLW0603
    if _processing_running:
        return {"queued": False, "reason": "Processing already running"}

    async def _run() -> None:
        global _processing_running, _last_run_stats  # noqa: PLW0603
        async with _processing_lock:
            _processing_running = True
            try:
                _, _, run_batch, _, _ = _get_processor()
                # Run in executor to avoid blocking the event loop
                loop = asyncio.get_event_loop()
                stats = await loop.run_in_executor(
                    None,
                    lambda: run_batch(
                        sign_ids=req.sign_ids,
                        force=req.force,
                        skip_wikimedia=req.skip_wikimedia,
                    ),
                )
                _last_run_stats = stats
                _log.info("Sign image batch complete: %s", stats)
            except Exception as exc:
                _log.error("Sign image batch failed: %s", exc, exc_info=True)
                _last_run_stats = {"error": str(exc)}
            finally:
                _processing_running = False

    background_tasks.add_task(_run)
    return {"queued": True, "message": "Processing started in background — poll /status for progress"}


@router.post("/process/{sign_id}")
async def process_one_sign(
    sign_id: str,
    force: bool = False,
    skip_wikimedia: bool = False,
) -> dict[str, Any]:
    """Process a single sign synchronously."""
    try:
        _, _, _, process_single, _load_sign_catalog = _get_processor()
        catalog = _load_sign_catalog()
        iconic = catalog.get(sign_id, "")
        source = process_single(sign_id, iconic, force=force, skip_wikimedia=skip_wikimedia)
        img_path = _STATIC_SIGNS / f"{sign_id}.png"
        return {
            "sign_id": sign_id,
            "source": source,
            "image_url": f"/static/signs/{sign_id}.png" if img_path.exists() else None,
        }
    except Exception as exc:
        _log.error("Failed to process sign %s: %s", sign_id, exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/upload/{sign_id}")
async def upload_sign_image(sign_id: str, file: UploadFile = File(...)) -> dict[str, Any]:
    """Manually upload a source image for a sign.

    The uploaded image will be normalized (threshold → clean → 128×128)
    and stored as both original and processed versions.
    """
    import io  # noqa: PLC0415

    import cv2  # noqa: PLC0415
    import numpy as np  # noqa: PLC0415
    from PIL import Image  # noqa: PLC0415
    from glossa_lab.tools.sign_image_processor import (  # noqa: PLC0415
        normalize_sign_image, _save_sign, load_manifest, save_manifest,
    )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        content = await file.read()
        pil_img = Image.open(io.BytesIO(content)).convert("RGB")
        orig_arr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        processed = normalize_sign_image(orig_arr)

        manifest = load_manifest()
        _save_sign(sign_id, processed, orig_arr, "manual_upload", manifest)
        save_manifest(manifest)

        img_path = _STATIC_SIGNS / f"{sign_id}.png"
        return {
            "sign_id": sign_id,
            "source": "manual_upload",
            "image_url": f"/static/signs/{sign_id}.png" if img_path.exists() else None,
        }
    except HTTPException:
        raise
    except Exception as exc:
        _log.error("Upload failed for %s: %s", sign_id, exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
