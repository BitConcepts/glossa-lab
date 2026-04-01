"""Job results endpoint."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from glossa_lab.database import get_db

router = APIRouter()


@router.get("/jobs/{job_id}/results")
async def get_job_results(job_id: str) -> dict[str, Any]:
    """Return results for a completed job."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    job = await db.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if job["status"] != "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Job status is '{job['status']}', not 'completed'",
        )

    result = await db.get_result_for_job(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="No results found")

    return result["data"]
