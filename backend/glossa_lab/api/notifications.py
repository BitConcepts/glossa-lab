"""Notifications API.

Endpoints (mounted at ``/api/v1/notifications``):

* ``GET    /recipients``           — list every recipient (active + inactive)
* ``POST   /recipients``           — add a recipient
* ``PATCH  /recipients/{id}``      — change email / label / active flag
* ``DELETE /recipients/{id}``      — remove a recipient
* ``GET    /log``                  — most recent send-log rows (paginated)
* ``POST   /test``                 — send a deliverability-test email to all active recipients
* ``GET    /status``               — Notifier configuration status (host configured? recipient count?)
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from glossa_lab.database import get_db
from glossa_lab.notifications import format_test, get_notifier
from glossa_lab.notifications.smtp import mask_email

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])

_log = logging.getLogger("glossa_lab.api.notifications")

_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_email(addr: str) -> str:
    addr = (addr or "").strip().lower()
    if not _EMAIL_RE.match(addr):
        raise HTTPException(status_code=400, detail=f"Invalid email address: {addr!r}")
    return addr


# ── Pydantic models ──────────────────────────────────────────────────────────


class RecipientCreate(BaseModel):
    email: str
    label: str = ""
    active: bool = True


class RecipientUpdate(BaseModel):
    email: str | None = None
    label: str | None = None
    active: bool | None = None


# ── Recipients CRUD ──────────────────────────────────────────────────────────


@router.get("/recipients")
async def list_recipients() -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    rows = await db.list_recipients()
    return {"recipients": rows, "count": len(rows)}


@router.post("/recipients", status_code=201)
async def create_recipient(body: RecipientCreate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    email = _validate_email(body.email)
    try:
        return await db.create_recipient(
            email=email, label=body.label.strip(),
            active=body.active, created_at=_now_iso(),
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "UNIQUE constraint" in msg:
            raise HTTPException(status_code=409, detail="Recipient already exists") from exc
        raise HTTPException(status_code=500, detail=f"Could not create recipient: {msg}") from exc


@router.patch("/recipients/{rid}")
async def update_recipient(rid: str, body: RecipientUpdate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    next_email = _validate_email(body.email) if body.email is not None else None
    row = await db.update_recipient(
        rid, email=next_email, label=body.label, active=body.active,
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return row


@router.delete("/recipients/{rid}")
async def delete_recipient(rid: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    row = await db.delete_recipient(rid)
    if row is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return {"deleted": True, "id": rid}


# ── Log ──────────────────────────────────────────────────────────────────────


@router.get("/log")
async def list_log(limit: int = 100) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    limit = max(1, min(int(limit), 500))
    rows = await db.list_notification_log(limit=limit)
    return {"entries": rows, "limit": limit}


# ── Status ───────────────────────────────────────────────────────────────────


@router.get("/status")
async def notifier_status() -> dict[str, Any]:
    """Lightweight health/config snapshot used by the Settings UI."""
    notifier = get_notifier()
    cfg = notifier.config
    db = get_db()
    n_active = 0
    n_total = 0
    if db is not None:
        rows = await db.list_recipients()
        n_total = len(rows)
        n_active = sum(1 for r in rows if r.get("active"))
    return {
        "configured": notifier.is_configured(),
        "host": cfg.host,
        "port": cfg.port,
        "from": cfg.sender,
        "use_tls": cfg.use_tls,
        "username_set": bool(cfg.username),
        "password_set": bool(cfg.password),
        "recipients_total": n_total,
        "recipients_active": n_active,
    }


# ── Test send ────────────────────────────────────────────────────────────────


@router.post("/test")
async def send_test_email() -> dict[str, Any]:
    """Send a deliverability test email to every active recipient.

    Returns a per-recipient result list (with masked addresses) so the UI
    can surface which addresses succeeded / failed without exposing the
    full address list to the client.
    """
    notifier = get_notifier()
    if not notifier.is_configured():
        raise HTTPException(
            status_code=400,
            detail="SMTP is not configured. Set smtp_host and smtp_from in Settings first.",
        )
    recipients = await notifier.list_active_recipients()
    if not recipients:
        raise HTTPException(
            status_code=400,
            detail="No active recipients. Add at least one in Settings → Notifications.",
        )

    subject, body_text, body_html = format_test()
    batch = await notifier.send(
        subject=subject, body_text=body_text, body_html=body_html,
        kind="test", item_count=0, recipients=recipients,
    )
    return {
        "subject": subject,
        "results": [
            {
                "recipient": mask_email(r.recipient),
                "status": r.status,
                "error": r.error,
            }
            for r in batch.results
        ],
        "sent": sum(1 for r in batch.results if r.status == "sent"),
        "failed": sum(1 for r in batch.results if r.status == "failed"),
    }


__all__ = ["router"]
