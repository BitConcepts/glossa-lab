"""Collaboration messages API.

Per-study threaded messages for team collaboration.
Messages can be pinned to surface them to AI context.

  GET    /studies/{study_id}/messages          -- list messages for a study
  POST   /studies/{study_id}/messages          -- add a message
  PATCH  /studies/{study_id}/messages/{msg_id} -- update (pin/edit)
  DELETE /studies/{study_id}/messages/{msg_id} -- delete
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab import database as db_mod

router = APIRouter()


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _get_db():
    d = db_mod.get_db()
    if d is None:
        raise HTTPException(status_code=503, detail="Database not ready")
    return d


# ── Request/response models ───────────────────────────────────────────────────

class CollabMessageCreate(BaseModel):
    author: str = ""
    message: str


class CollabMessageUpdate(BaseModel):
    pinned: int | None = None
    message: str | None = None
    author: str | None = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/studies/{study_id}/messages")
async def list_messages(study_id: str) -> list[dict[str, Any]]:
    """Return all collaboration messages for a study, pinned first."""
    db = _get_db()
    # Verify study exists
    study = await db.get_study(study_id)
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")
    return await db.list_collab_messages(study_id)


@router.post("/studies/{study_id}/messages", status_code=201)
async def create_message(study_id: str, body: CollabMessageCreate) -> dict[str, Any]:
    """Add a collaboration message to a study."""
    db = _get_db()
    study = await db.get_study(study_id)
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")
    if not body.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")
    return await db.create_collab_message(
        study_id=study_id,
        author=body.author.strip(),
        message=body.message.strip(),
        created_at=_now(),
    )


@router.patch("/studies/{study_id}/messages/{msg_id}")
async def update_message(
    study_id: str, msg_id: str, body: CollabMessageUpdate
) -> dict[str, Any]:
    """Update a message (toggle pin, edit text)."""
    db = _get_db()
    msg = await db.get_collab_message(msg_id)
    if msg is None or msg["study_id"] != study_id:
        raise HTTPException(status_code=404, detail=f"Message '{msg_id}' not found")
    updated = await db.update_collab_message(
        msg_id,
        pinned=body.pinned,
        message=body.message,
        author=body.author,
    )
    return updated  # type: ignore[return-value]


@router.delete("/studies/{study_id}/messages/{msg_id}")
async def delete_message(study_id: str, msg_id: str) -> dict[str, Any]:
    """Delete a collaboration message."""
    db = _get_db()
    msg = await db.get_collab_message(msg_id)
    if msg is None or msg["study_id"] != study_id:
        raise HTTPException(status_code=404, detail=f"Message '{msg_id}' not found")
    deleted = await db.delete_collab_message(msg_id)
    return {"deleted": True, "id": msg_id, "message": deleted}
