"""Health and status endpoints."""

import time

from fastapi import APIRouter

from glossa_lab import __version__

router = APIRouter()


@router.get("/health")
async def health():
    """Return health status, version, and uptime.

    Satisfies REQ-API-001.
    """
    from glossa_lab.main import get_start_time

    start = get_start_time()
    uptime = time.time() - start if start > 0 else 0.0

    return {
        "status": "healthy",
        "version": __version__,
        "uptime_seconds": round(uptime, 1),
    }
