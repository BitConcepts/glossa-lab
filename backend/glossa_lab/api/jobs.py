"""Jobs CRUD endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db

router = APIRouter()


class JobCreate(BaseModel):
    """Request body for creating a job."""

    name: str
    pipeline: str = "default"
    params: dict[str, Any] = {}
    initial_status: str = "pending"  # allow CLI to create jobs already in 'running' state


class JobResponse(BaseModel):
    """Serialised job returned by the API."""

    id: str
    name: str
    pipeline: str
    status: str
    params: dict[str, Any]
    created_at: str
    updated_at: str


class JobUpdate(BaseModel):
    """Request body for updating a job's status."""

    status: str  # running | completed | failed | cancelled
    result_data: dict[str, Any] = {}


class ClearJobsResponse(BaseModel):
    """Response body for bulk clearing jobs."""

    cleared: int


@router.post("/jobs", status_code=201)
async def create_job(body: JobCreate) -> JobResponse:
    """Submit a new job."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    now = datetime.now(timezone.utc).isoformat()
    job = await db.create_job(
        name=body.name,
        pipeline=body.pipeline,
        params=body.params,
        created_at=now,
        initial_status=body.initial_status,
    )
    return JobResponse(**job)


@router.get("/jobs")
async def list_jobs() -> list[JobResponse]:
    """List all jobs."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    rows = await db.list_jobs()
    return [JobResponse(**r) for r in rows]


@router.get("/jobs/{job_id}")
async def get_job(job_id: str) -> JobResponse:
    """Get a single job by ID."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    job = await db.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(**job)


@router.patch("/jobs/{job_id}")
async def update_job(job_id: str, body: JobUpdate) -> JobResponse:
    """Update a job's status (running / completed / failed / cancelled).

    Optionally store result_data in job_results so the UI can display
    experiment output alongside the job entry.
    """
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    job = await db.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    await db.update_job_status(job_id, body.status)
    if body.result_data:
        now = datetime.now(timezone.utc).isoformat()
        await db.store_result(job_id=job_id, data=body.result_data, created_at=now)
    return JobResponse(**(await db.get_job(job_id)))  # type: ignore[arg-type]


@router.delete("/jobs", status_code=200)
async def clear_jobs(finished_only: bool = False) -> ClearJobsResponse:
    """Delete jobs.  Pass ?finished_only=true to keep running/pending jobs."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    if finished_only:
        return ClearJobsResponse(cleared=await db.clear_finished_jobs())
    return ClearJobsResponse(cleared=await db.clear_jobs())


@router.delete("/jobs/{job_id}", status_code=200)
async def cancel_job(job_id: str) -> JobResponse:
    """Cancel (delete) a job."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    job = await db.cancel_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(**job)
