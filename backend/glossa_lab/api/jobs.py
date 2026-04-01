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


class JobResponse(BaseModel):
    """Serialised job returned by the API."""

    id: str
    name: str
    pipeline: str
    status: str
    params: dict[str, Any]
    created_at: str
    updated_at: str


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
