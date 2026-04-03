"""Text corpus management endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db

router = APIRouter()


class TextCreate(BaseModel):
    """Request body for uploading a text corpus."""

    name: str
    corpus_type: str = "linguistic"
    content: list[str]
    metadata: dict[str, Any] = {}


class TextResponse(BaseModel):
    """Serialised text returned by the API."""

    id: str
    name: str
    corpus_type: str
    content: list[str]
    alphabet_size: int
    symbol_set: list[str]
    metadata: dict[str, Any]
    created_at: str


class TextUpdate(BaseModel):
    """Request body for updating corpus metadata/content."""

    name: str | None = None
    corpus_type: str | None = None
    content: list[str] | None = None
    metadata: dict[str, Any] | None = None


@router.post("/texts", status_code=201)
async def create_text(body: TextCreate) -> TextResponse:
    """Upload a new text corpus."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    now = datetime.now(timezone.utc).isoformat()
    text = await db.create_text(
        name=body.name,
        corpus_type=body.corpus_type,
        content=body.content,
        metadata=body.metadata,
        created_at=now,
    )
    return TextResponse(**text)


@router.get("/texts")
async def list_texts() -> list[TextResponse]:
    """List all text corpora."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    rows = await db.list_texts()
    return [TextResponse(**r) for r in rows]


@router.get("/texts/{text_id}")
async def get_text(text_id: str) -> TextResponse:
    """Get a single text corpus by ID."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return TextResponse(**text)


@router.put("/texts/{text_id}")
async def update_text(text_id: str, body: TextUpdate) -> TextResponse:
    """Update a text corpus."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    text = await db.update_text(
        text_id,
        name=body.name,
        corpus_type=body.corpus_type,
        content=body.content,
        metadata=body.metadata,
    )
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return TextResponse(**text)


@router.delete("/texts/{text_id}")
async def delete_text(text_id: str) -> TextResponse:
    """Delete a text corpus."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    text = await db.delete_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return TextResponse(**text)
