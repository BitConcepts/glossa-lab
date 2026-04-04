"""System status endpoint (REQ-API-002)."""

import time

from fastapi import APIRouter

from glossa_lab import __version__
from glossa_lab.catalog import get_catalog_summary
from glossa_lab.database import get_db
from glossa_lab.engine import get_registered_pipelines

router = APIRouter()


@router.get("/status")
async def status():
    """Return detailed system status including job counts and pipeline states.

    Satisfies REQ-API-002.
    """
    from glossa_lab.main import get_start_time

    start = get_start_time()
    uptime = time.time() - start if start > 0 else 0.0

    db = get_db()
    job_counts = (
        await db.get_job_counts()
        if db
        else {
            "total": 0,
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0,
        }
    )
    pipelines = get_registered_pipelines()

    return {
        "status": "healthy",
        "version": __version__,
        "uptime_seconds": round(uptime, 1),
        "jobs": job_counts,
        "job_counts": job_counts,
        "pipelines": pipelines,
        "pipeline_count": len(pipelines),
        "catalog_counts": get_catalog_summary(),
    }
