"""Studies CRUD API.

A Study is a named, user-editable visual workflow graph comprising
experiment and pipeline nodes connected by data-flow edges.

Endpoints:
  GET    /studies            -- list all studies
  GET    /studies/{id}       -- get a study
  POST   /studies            -- create a study
  PUT    /studies/{id}       -- update a study (name/description/graph)
  DELETE /studies/{id}       -- delete a study
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db

router = APIRouter()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fmt(study: dict[str, Any]) -> dict[str, Any]:
    """Ensure graph is always a dict with nodes/edges lists."""
    g = study.get("graph") or {}
    if not isinstance(g, dict):
        g = {}
    study["graph"] = {
        "nodes": g.get("nodes", []),
        "edges": g.get("edges", []),
    }
    return study


# ── Models ─────────────────────────────────────────────────────────────


class NodePos(BaseModel):
    x: float = 0.0
    y: float = 0.0


class StudyNodeIn(BaseModel):
    id: str
    type: str = "experiment"
    ref_id: str = ""
    label: str = ""
    params: dict[str, Any] = {}
    position: NodePos = NodePos()


class StudyEdgeIn(BaseModel):
    id: str
    source: str
    target: str


class StudyGraphIn(BaseModel):
    nodes: list[StudyNodeIn] = []
    edges: list[StudyEdgeIn] = []


class StudyCreate(BaseModel):
    name: str
    description: str = ""
    graph: StudyGraphIn = StudyGraphIn()


class StudyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    graph: StudyGraphIn | None = None


# ── Endpoints ──────────────────────────────────────────────────────────


@router.get("/studies")
async def list_studies() -> list[dict[str, Any]]:
    db = get_db()
    if db is None:
        return []
    studies = await db.list_studies()
    return [_fmt(s) for s in studies]


@router.get("/studies/{study_id}")
async def get_study(study_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.get_study(study_id)
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")
    return _fmt(study)


@router.post("/studies", status_code=201)
async def create_study(body: StudyCreate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.create_study(
        name=body.name,
        description=body.description,
        graph=body.graph.model_dump(),
        created_at=_now_iso(),
    )
    return _fmt(study)


@router.put("/studies/{study_id}")
async def update_study(study_id: str, body: StudyUpdate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.update_study(
        study_id,
        name=body.name,
        description=body.description,
        graph=body.graph.model_dump() if body.graph is not None else None,
    )
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")
    return _fmt(study)


@router.delete("/studies/{study_id}")
async def delete_study(study_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    deleted = await db.delete_study(study_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")
    return {"deleted": True, "id": study_id}
