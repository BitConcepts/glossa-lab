"""Correspondence API — track researcher communications.

CRUD at ``/api/v1/correspondences`` with project_id scoping.
Parse endpoint for pasting raw email text or .eml content.

Endpoints:
  GET    /correspondences              — list (optional ?project_id=)
  POST   /correspondences              — create
  GET    /correspondences/{id}         — get one
  PUT    /correspondences/{id}         — update
  DELETE /correspondences/{id}         — delete
  POST   /correspondences/parse        — LLM-assisted email parsing
"""

from __future__ import annotations

import email as email_mod
import json
import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from glossa_lab.database import get_db

_log = logging.getLogger("glossa_lab.api.correspondences")

router = APIRouter(prefix="/api/v1/correspondences", tags=["correspondences"])


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Models ─────────────────────────────────────────────────────────────────────


class CorrespondenceCreate(BaseModel):
    project_id: str = ""
    direction: str = "outbound"
    channel: str = "email"
    from_addr: str = ""
    to_addr: str = ""
    cc_addr: str = ""
    subject: str = ""
    body: str = ""
    date: str = ""
    attachments: list[dict[str, Any]] = []
    claims_made: str = ""
    questions: str = ""
    reply_status: str = "pending"
    follow_up_date: str = ""
    tags: list[str] = []


class CorrespondenceUpdate(BaseModel):
    project_id: str | None = None
    direction: str | None = None
    channel: str | None = None
    from_addr: str | None = None
    to_addr: str | None = None
    cc_addr: str | None = None
    subject: str | None = None
    body: str | None = None
    date: str | None = None
    attachments: list[dict[str, Any]] | None = None
    claims_made: str | None = None
    questions: str | None = None
    reply_status: str | None = None
    follow_up_date: str | None = None
    tags: list[str] | None = None


class ParseRequest(BaseModel):
    raw_text: str
    is_eml: bool = False


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.get("")
async def list_correspondences(
    project_id: str | None = Query(None),
) -> list[dict[str, Any]]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    return await db.list_correspondences(project_id=project_id)


@router.post("", status_code=201)
async def create_correspondence(body: CorrespondenceCreate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    return await db.create_correspondence(
        project_id=body.project_id,
        direction=body.direction,
        channel=body.channel,
        from_addr=body.from_addr,
        to_addr=body.to_addr,
        cc_addr=body.cc_addr,
        subject=body.subject,
        body=body.body,
        date=body.date or _now_iso()[:10],
        attachments=body.attachments,
        claims_made=body.claims_made,
        questions=body.questions,
        reply_status=body.reply_status,
        follow_up_date=body.follow_up_date,
        tags=body.tags,
        created_at=_now_iso(),
    )


@router.get("/{corr_id}")
async def get_correspondence(corr_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    c = await db.get_correspondence(corr_id)
    if c is None:
        raise HTTPException(404, f"Correspondence {corr_id} not found")
    return c


@router.put("/{corr_id}")
async def update_correspondence(
    corr_id: str, body: CorrespondenceUpdate,
) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    updated = await db.update_correspondence(
        corr_id, **body.model_dump(exclude_none=True),
    )
    if updated is None:
        raise HTTPException(404, f"Correspondence {corr_id} not found")
    return updated


@router.delete("/{corr_id}")
async def delete_correspondence(corr_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    deleted = await db.delete_correspondence(corr_id)
    if deleted is None:
        raise HTTPException(404, f"Correspondence {corr_id} not found")
    return {"deleted": True, "correspondence": deleted}


# ── Parse endpoint (F2) ───────────────────────────────────────────────────────


def _parse_eml(raw: str) -> dict[str, Any]:
    """Parse a raw .eml string using Python's email stdlib module."""
    msg = email_mod.message_from_string(raw)
    body_parts: list[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body_parts.append(payload.decode("utf-8", errors="replace"))
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body_parts.append(payload.decode("utf-8", errors="replace"))

    attachments: list[dict[str, Any]] = []
    if msg.is_multipart():
        for part in msg.walk():
            fn = part.get_filename()
            if fn:
                attachments.append({
                    "name": fn,
                    "content_type": part.get_content_type(),
                })

    return {
        "from_addr": msg.get("From", ""),
        "to_addr": msg.get("To", ""),
        "cc_addr": msg.get("Cc", "") or "",
        "subject": msg.get("Subject", ""),
        "date": msg.get("Date", ""),
        "body": "\n".join(body_parts).strip(),
        "attachments": attachments,
        "direction": "inbound",
        "channel": "email",
        "claims_made": "",
        "questions": "",
    }


@router.post("/parse")
async def parse_email(body: ParseRequest) -> dict[str, Any]:
    """Parse raw email text into structured correspondence fields.

    If ``is_eml`` is True, uses Python's ``email`` module for deterministic
    header/body extraction. Otherwise falls back to LLM-assisted extraction.
    """
    if body.is_eml or body.raw_text.strip().startswith(("From:", "Received:", "MIME-Version:")):
        try:
            return _parse_eml(body.raw_text)
        except Exception as exc:
            _log.warning("EML parse failed, falling back to LLM: %s", exc)

    # LLM-assisted extraction for plain-text paste
    try:
        from glossa_lab.ai_utils import call_llm  # noqa: PLC0415

        raw = call_llm(
            [
                {"role": "system", "content": (
                    "You extract structured fields from pasted email text. "
                    "Return ONLY valid JSON with keys: from_addr, to_addr, cc_addr, "
                    "subject, date, body, attachments (array of {name}), direction "
                    "(inbound or outbound), claims_made, questions. "
                    "Infer direction from context. If unsure, default to inbound."
                )},
                {"role": "user", "content": body.raw_text[:4000]},
            ],
            json_mode=True,
            max_tokens=800,
            temperature=0.1,
        )
        parsed = json.loads(raw)
        # Ensure expected keys
        for k in ("from_addr", "to_addr", "cc_addr", "subject", "date", "body",
                   "attachments", "direction", "claims_made", "questions"):
            parsed.setdefault(k, "" if k != "attachments" else [])
        parsed.setdefault("channel", "email")
        return parsed
    except Exception as exc:
        _log.warning("LLM parse failed: %s", exc)
        # Return empty template so the user can fill it manually
        return {
            "from_addr": "", "to_addr": "", "cc_addr": "",
            "subject": "", "date": "", "body": body.raw_text[:2000],
            "attachments": [], "direction": "inbound", "channel": "email",
            "claims_made": "", "questions": "",
            "parse_error": str(exc),
        }
