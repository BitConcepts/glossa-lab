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

import uuid
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


# ── Export / Import ────────────────────────────────────────────────────────


@router.get("/{project_id}/export")
async def export_project(project_id: str) -> dict[str, Any]:
    """Export a project and all its linked entities as a JSON bundle."""
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    project = await db.get_project(project_id)
    if project is None:
        raise HTTPException(404, f"Project {project_id} not found")

    hypotheses = await db.list_hypotheses(project_id=project_id)
    notebooks = await db.list_notebooks(project_id=project_id)
    correspondences = await db.list_correspondences(project_id=project_id)
    # Citations don't have project_id filter yet — export all
    citations = await db.list_citations()

    return {
        "version": 1,
        "project": project,
        "hypotheses": hypotheses,
        "notebooks": notebooks,
        "citations": citations,
        "correspondences": correspondences,
    }


@router.post("/import")
async def import_project(bundle: dict[str, Any]) -> dict[str, Any]:
    """Import a project bundle. Creates new project + all linked entities with fresh IDs."""
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")

    proj = bundle.get("project")
    if not proj or not proj.get("label"):
        raise HTTPException(422, "Bundle must contain a project with a label")

    now = datetime.now(timezone.utc).isoformat()
    new_id = proj.get("label", "imported").lower().replace(" ", "_")[:30] + "_" + uuid.uuid4().hex[:6]

    created = await db.upsert_project(
        project_id=new_id,
        label=proj["label"],
        description=proj.get("description", ""),
        prompt_context=proj.get("prompt_context", ""),
        topic_ids=proj.get("topic_ids", []),
        experiment_ids=proj.get("experiment_ids", []),
        corpus_ids=proj.get("corpus_ids", []),
        is_active=False,
        created_at=now,
    )

    counts = {"hypotheses": 0, "notebooks": 0, "citations": 0, "correspondences": 0}

    for h in bundle.get("hypotheses", []):
        await db.create_hypothesis(
            title=h.get("title", ""), statement=h.get("statement", ""),
            status=h.get("status", "active"), project_id=new_id, created_at=now,
        )
        counts["hypotheses"] += 1

    for n in bundle.get("notebooks", []):
        await db.create_notebook(
            title=n.get("title", ""), content=n.get("content", ""),
            tags=n.get("tags", []), project_id=new_id, created_at=now,
        )
        counts["notebooks"] += 1

    for c in bundle.get("correspondences", []):
        await db.create_correspondence(
            project_id=new_id, direction=c.get("direction", "inbound"),
            channel=c.get("channel", "email"), from_addr=c.get("from_addr", ""),
            to_addr=c.get("to_addr", ""), cc_addr=c.get("cc_addr", ""),
            subject=c.get("subject", ""), body=c.get("body", ""),
            date=c.get("date", ""), attachments=c.get("attachments", []),
            claims_made=c.get("claims_made", ""), questions=c.get("questions", ""),
            reply_status=c.get("reply_status", "pending"),
            follow_up_date=c.get("follow_up_date", ""),
            tags=c.get("tags", []), created_at=now,
        )
        counts["correspondences"] += 1

    return {"project": created, "imported": counts}
