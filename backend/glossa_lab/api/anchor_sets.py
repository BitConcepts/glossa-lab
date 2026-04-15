"""User-definable Anchor Sets API.

Anchor sets store verified sign → reading mappings that users can
reuse across experiments without embedding them in Python files.

Endpoints:
  GET    /anchor-sets                    -- list all anchor sets
  POST   /anchor-sets                    -- create a new anchor set
  GET    /anchor-sets/{id}               -- get one anchor set
  PUT    /anchor-sets/{id}               -- update anchor set
  DELETE /anchor-sets/{id}               -- delete anchor set
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AnchorPair(BaseModel):
    """One verified cipher→target sign pair."""
    cipher:     str               # cipher sign (as it appears in the undeciphered corpus)
    target:     str               # target reading (e.g. phoneme, syllable value)
    confidence: str = "high"     # high | medium | low
    note:       str = ""


class AnchorSetCreate(BaseModel):
    name:        str
    description: str = ""
    corpus_id:   str | None = None
    language:    str = ""
    pairs:       list[AnchorPair] = []


class AnchorSetUpdate(BaseModel):
    name:        str | None = None
    description: str | None = None
    corpus_id:   str | None = None
    language:    str | None = None
    pairs:       list[AnchorPair] | None = None


@router.get("/anchor-sets")
async def list_anchor_sets(corpus_id: str | None = None) -> list[dict[str, Any]]:
    """List all anchor sets, optionally filtered by corpus_id."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return []
    return await db.list_anchor_sets(corpus_id=corpus_id)


@router.post("/anchor-sets", status_code=201)
async def create_anchor_set(body: AnchorSetCreate) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.create_anchor_set(
        name=body.name,
        description=body.description,
        corpus_id=body.corpus_id,
        language=body.language,
        pairs=[p.model_dump() for p in body.pairs],
        created_at=_now(),
    )


@router.get("/anchor-sets/{anchor_set_id}")
async def get_anchor_set(anchor_set_id: str) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.get_anchor_set(anchor_set_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Anchor set '{anchor_set_id}' not found")
    return result


@router.put("/anchor-sets/{anchor_set_id}")
async def update_anchor_set(anchor_set_id: str, body: AnchorSetUpdate) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    fields: dict[str, Any] = {}
    if body.name is not None:        fields["name"] = body.name
    if body.description is not None: fields["description"] = body.description
    if body.corpus_id is not None:   fields["corpus_id"] = body.corpus_id
    if body.language is not None:    fields["language"] = body.language
    if body.pairs is not None:       fields["pairs"] = [p.model_dump() for p in body.pairs]
    result = await db.update_anchor_set(anchor_set_id, **fields)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Anchor set '{anchor_set_id}' not found")
    return result


@router.delete("/anchor-sets/{anchor_set_id}")
async def delete_anchor_set(anchor_set_id: str) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.delete_anchor_set(anchor_set_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Anchor set '{anchor_set_id}' not found")
    return {"deleted": True, "id": anchor_set_id}
