"""Research-oriented CRUD endpoints.

Endpoints:
  /hypotheses  -- track research hypotheses
  /notebooks   -- markdown scratchpads
  /citations   -- paper references / BibTeX records
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


# ── Models ─────────────────────────────────────────────────────────────────────


class HypothesisCreate(BaseModel):
    title: str
    statement: str = ""
    status: str = "active"


class HypothesisUpdate(BaseModel):
    title: str | None = None
    statement: str | None = None
    status: str | None = None
    evidence: list[str] | None = None
    study_ids: list[str] | None = None
    exp_ids: list[str] | None = None


class NotebookCreate(BaseModel):
    title: str
    content: str = ""
    study_id: str | None = None
    tags: list[str] = []


class NotebookUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    study_id: str | None = None
    tags: list[str] | None = None


class CitationCreate(BaseModel):
    key: str
    title: str = ""
    authors: str = ""
    year: str = ""
    venue: str = ""
    doi: str = ""
    url: str = ""
    bibtex: str = ""
    notes: str = ""


class CitationUpdate(BaseModel):
    title: str | None = None
    authors: str | None = None
    year: str | None = None
    venue: str | None = None
    doi: str | None = None
    url: str | None = None
    bibtex: str | None = None
    notes: str | None = None
    exp_ids: list[str] | None = None
    study_ids: list[str] | None = None


# ── Hypotheses ─────────────────────────────────────────────────────────────────


@router.get("/hypotheses")
async def list_hypotheses() -> list[dict[str, Any]]:
    """List all hypotheses."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.list_hypotheses()


@router.post("/hypotheses", status_code=201)
async def create_hypothesis(body: HypothesisCreate) -> dict[str, Any]:
    """Create a new hypothesis."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.create_hypothesis(
        title=body.title, statement=body.statement, status=body.status, created_at=_now_iso()
    )


@router.put("/hypotheses/{hypothesis_id}")
async def update_hypothesis(hypothesis_id: str, body: HypothesisUpdate) -> dict[str, Any]:
    """Update a hypothesis."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    hypothesis = await db.update_hypothesis(hypothesis_id, **body.model_dump(exclude_none=True))
    if hypothesis is None:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    return hypothesis


@router.delete("/hypotheses/{hypothesis_id}")
async def delete_hypothesis(hypothesis_id: str) -> dict[str, Any]:
    """Delete a hypothesis."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    hypothesis = await db.delete_hypothesis(hypothesis_id)
    if hypothesis is None:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    return hypothesis


# ── Notebooks ──────────────────────────────────────────────────────────────────


@router.get("/notebooks")
async def list_notebooks() -> list[dict[str, Any]]:
    """List all notebooks."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.list_notebooks()


@router.post("/notebooks", status_code=201)
async def create_notebook(body: NotebookCreate) -> dict[str, Any]:
    """Create a new notebook."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.create_notebook(
        title=body.title,
        content=body.content,
        study_id=body.study_id,
        tags=body.tags,
        created_at=_now_iso(),
    )


@router.put("/notebooks/{notebook_id}")
async def update_notebook(notebook_id: str, body: NotebookUpdate) -> dict[str, Any]:
    """Update a notebook."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    notebook = await db.update_notebook(notebook_id, **body.model_dump(exclude_none=True))
    if notebook is None:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return notebook


@router.delete("/notebooks/{notebook_id}")
async def delete_notebook(notebook_id: str) -> dict[str, Any]:
    """Delete a notebook."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    notebook = await db.delete_notebook(notebook_id)
    if notebook is None:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return notebook


# ── Citations ──────────────────────────────────────────────────────────────────


@router.get("/citations")
async def list_citations() -> list[dict[str, Any]]:
    """List all citations."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.list_citations()


@router.post("/citations", status_code=201)
async def create_citation(body: CitationCreate) -> dict[str, Any]:
    """Create a new citation."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    try:
        return await db.create_citation(created_at=_now_iso(), **body.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/citations/{citation_id}")
async def update_citation(citation_id: str, body: CitationUpdate) -> dict[str, Any]:
    """Update a citation."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    citation = await db.update_citation(citation_id, **body.model_dump(exclude_none=True))
    if citation is None:
        raise HTTPException(status_code=404, detail="Citation not found")
    return citation


@router.delete("/citations/{citation_id}")
async def delete_citation(citation_id: str) -> dict[str, Any]:
    """Delete a citation."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    citation = await db.delete_citation(citation_id)
    if citation is None:
        raise HTTPException(status_code=404, detail="Citation not found")
    return citation
