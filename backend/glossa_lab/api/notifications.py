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

import asyncio
import logging
import re
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.api.settings import _load_keys, _save_keys, get_key
from glossa_lab.database import get_db
from glossa_lab.notifications import format_test, get_notifier
from glossa_lab.notifications.graph import (
    GraphAuthPending,
    GraphError,
    poll_device_flow,
    start_device_flow,
)
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
    graph = notifier.graph
    resend = notifier.resend
    db = get_db()
    n_active = 0
    n_total = 0
    if db is not None:
        rows = await db.list_recipients()
        n_total = len(rows)
        n_active = sum(1 for r in rows if r.get("active"))
    return {
        "configured": notifier.is_configured(),
        "transport": notifier.transport,  # "graph" | "resend" | "smtp" | "none"
        "host": cfg.host,
        "port": cfg.port,
        "from": cfg.sender,
        "use_tls": cfg.use_tls,
        "username_set": bool(cfg.username),
        "password_set": bool(cfg.password),
        "graph_configured": graph.is_configured(),
        "graph_client_id_set": bool(graph.client_id),
        # graph_client_id always resolves now (default fallback). Tell the
        # frontend whether we're using the public default so it can offer a
        # one-click connect without any Azure setup.
        "graph_default_client": graph.is_default_client,
        "graph_tenant": graph.tenant,
        "resend_configured": resend.is_configured(),
        "resend_from": resend.sender,
        "recipients_total": n_total,
        "recipients_active": n_active,
    }


# ── Microsoft Graph device-flow endpoints ───────────────────────────
# In-memory store of pending device flows. Keyed by an opaque session id
# the frontend gets back from POST /graph/start. Entries auto-expire when
# the underlying device_code does (~15 min).

_pending_graph_flows: dict[str, dict[str, Any]] = {}
_pending_graph_lock = asyncio.Lock()


async def _purge_expired_graph_sessions() -> None:
    now = time.time()
    async with _pending_graph_lock:
        for sid in list(_pending_graph_flows):
            if _pending_graph_flows[sid].get("expires_at", 0) < now:
                _pending_graph_flows.pop(sid, None)


@router.post("/graph/start")
async def graph_start() -> dict[str, Any]:
    """Begin Microsoft Graph device-code flow.

    The user pastes the returned ``user_code`` at ``verification_uri`` in
    any browser, signs in to their Outlook 365 account, and approves the
    Mail.Send + offline_access scopes. The frontend polls /graph/poll with
    the returned ``session_id`` until ``status == "success"``.
    """
    client_id = (get_key("ms_graph_client_id") or "").strip()
    tenant = (get_key("ms_graph_tenant_id") or "common").strip() or "common"
    if not client_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "ms_graph_client_id is not set. Register a public-client app "
                "in entra.microsoft.com (Delegated Mail.Send + offline_access) "
                "and paste the Application (client) ID into Settings."
            ),
        )
    try:
        flow = await asyncio.to_thread(start_device_flow, client_id, tenant)
    except GraphError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    sid = uuid.uuid4().hex
    await _purge_expired_graph_sessions()
    async with _pending_graph_lock:
        _pending_graph_flows[sid] = {
            "client_id": client_id,
            "tenant": tenant,
            "device_code": flow["device_code"],
            "expires_at": time.time() + int(flow.get("expires_in", 900)),
            "interval": int(flow.get("interval", 5)),
            "status": "pending",
            "error": "",
        }

    return {
        "session_id": sid,
        "user_code": flow["user_code"],
        "verification_uri": flow["verification_uri"],
        "expires_in": int(flow.get("expires_in", 900)),
        "interval": int(flow.get("interval", 5)),
        "message": flow.get("message", ""),
    }


@router.post("/graph/poll")
async def graph_poll(body: dict[str, Any]) -> dict[str, Any]:
    """Poll a pending device-code flow.

    Returns ``{status: "pending"|"success"|"failed"|"expired"}``. On
    success, the refresh_token is persisted and the session is deleted.
    """
    sid = (body or {}).get("session_id") or ""
    async with _pending_graph_lock:
        state = _pending_graph_flows.get(sid)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    if state["status"] in ("success", "failed", "expired"):
        return {"status": state["status"], "error": state.get("error", "")}

    if time.time() > state["expires_at"]:
        async with _pending_graph_lock:
            state["status"] = "expired"
        return {"status": "expired", "error": "User did not approve in time"}

    try:
        bundle = await asyncio.to_thread(
            poll_device_flow,
            state["client_id"], state["tenant"], state["device_code"],
        )
    except GraphAuthPending:
        return {"status": "pending"}
    except GraphError as exc:
        async with _pending_graph_lock:
            state["status"] = "failed"
            state["error"] = str(exc)
        return {"status": "failed", "error": str(exc)}

    refresh_token = bundle.get("refresh_token")
    if not refresh_token:
        return {"status": "failed", "error": "no refresh_token returned"}
    # Persist via the shared keys file so the Notifier picks it up next call.
    stored = _load_keys()
    stored["ms_graph_refresh_token"] = refresh_token
    _save_keys(stored)
    async with _pending_graph_lock:
        state["status"] = "success"
        # Drop the session immediately — we're done.
        _pending_graph_flows.pop(sid, None)
    return {"status": "success"}


@router.post("/graph/disconnect")
async def graph_disconnect() -> dict[str, Any]:
    """Clear the stored refresh_token so Graph stops being used."""
    stored = _load_keys()
    had = bool(stored.pop("ms_graph_refresh_token", ""))
    _save_keys(stored)
    return {"disconnected": had}


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
