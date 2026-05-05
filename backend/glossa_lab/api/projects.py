"""Projects API — CRUD for top-level research projects.

A project is the highest-level container in Glossa Lab. It scopes:
  - discovery topics (which feeds to watch)
  - experiments (which graph experiments belong to this project)
  - corpora (soft-linked; corpora are global but a project tracks which ones it uses)
  - prompt_context (injected into LLM system prompts for mine + dashboard insight)

Endpoints (mounted at ``/api/v1/projects``):
* ``GET /``             — list all projects
* ``GET /active``       — get the active project
* ``GET /{id}``         — get one
* ``PUT /{id}``         — create or update
* ``POST /{id}/activate`` — set as active project
* ``DELETE /{id}``      — delete
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


class ProjectBody(BaseModel):
    label: str
    description: str = ""
    prompt_context: str = ""
    topic_ids: list[str] = []
    experiment_ids: list[str] = []
    corpus_ids: list[str] = []
    is_active: bool = False


@router.get("")
async def list_projects() -> list[dict[str, Any]]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    return await db.list_projects()


@router.get("/active")
async def get_active_project() -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    project = await db.get_active_project()
    if project is None:
        raise HTTPException(404, "No projects configured")
    return project


@router.get("/{project_id}")
async def get_project(project_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    project = await db.get_project(project_id)
    if project is None:
        raise HTTPException(404, f"Project {project_id} not found")
    return project


@router.put("/{project_id}")
async def upsert_project(project_id: str, body: ProjectBody) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    now = datetime.now(timezone.utc).isoformat()
    return await db.upsert_project(
        project_id=project_id,
        label=body.label,
        description=body.description,
        prompt_context=body.prompt_context,
        topic_ids=body.topic_ids,
        experiment_ids=body.experiment_ids,
        corpus_ids=body.corpus_ids,
        is_active=body.is_active,
        created_at=now,
    )


@router.post("/{project_id}/activate")
async def activate_project(project_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    existing = await db.get_project(project_id)
    if existing is None:
        raise HTTPException(404, f"Project {project_id} not found")
    now = datetime.now(timezone.utc).isoformat()
    return await db.upsert_project(
        project_id=project_id,
        label=existing["label"],
        description=existing.get("description", ""),
        prompt_context=existing.get("prompt_context", ""),
        topic_ids=existing.get("topic_ids", []),
        experiment_ids=existing.get("experiment_ids", []),
        corpus_ids=existing.get("corpus_ids", []),
        is_active=True,
        created_at=existing.get("created_at", now),
    )


@router.delete("/{project_id}")
async def delete_project(project_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    deleted = await db.delete_project(project_id)
    if deleted is None:
        raise HTTPException(404, f"Project {project_id} not found")
    return {"deleted": True, "project": deleted}
