"""Study Loop API — autonomous research loop orchestration.

POST /api/v1/study-loop/start           — SSE stream of a study loop run
GET  /api/v1/study-loop/status          — current run state
POST /api/v1/study-loop/stop            — graceful stop
GET  /api/v1/study-loop/history         — all persisted sessions
GET  /api/v1/study-loop/last-session    — most recent session
GET  /api/v1/study-loop/scheduler/status  — scheduler state
POST /api/v1/study-loop/scheduler/enable  — enable scheduler at runtime
POST /api/v1/study-loop/scheduler/disable — disable scheduler at runtime

H14 compliance: email is routed through the backend Notifier only.
H11 compliance: no unbounded loops — ResearchLoop has max_cycles cap.
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/v1/study-loop", tags=["study-loop"])
_log = logging.getLogger("glossa_lab.api.study_loop")

_REPO = Path(__file__).resolve().parents[3]
_SESSIONS_JSON = _REPO / "outputs" / "study_loop_sessions.json"

# Module-level run state
_running = False
_session_id: str | None = None
_iterations: int = 0
_trigger: str = "user"
_started_at: str | None = None
_cycles_completed: int = 0  # live counter incremented per node_complete event


def is_study_loop_running() -> bool:
    """Check if a study loop is currently running (used by scheduler)."""
    return _running


async def start_study_loop_session(
    iterations: int = 15,
    trigger: str = "user",
) -> None:
    """Start a study loop session without SSE streaming (for scheduler use).

    Consumes all events internally. Sends completion email if configured.
    """
    from glossa_lab.pipelines.study_loop import run_study_loop  # noqa: PLC0415

    global _running, _session_id, _iterations, _trigger, _started_at  # noqa: PLW0603
    if _running:
        _log.info("Study loop already running — skipping scheduler tick")
        return

    _running = True
    _iterations = iterations
    _trigger = trigger
    _started_at = datetime.now(UTC).isoformat()
    _session_id = None

    try:
        session: dict[str, Any] | None = None
        async for event in run_study_loop(iterations=iterations, trigger=trigger):
            if event.get("type") == "study_loop_complete":
                session = event.get("session")
                if session:
                    _session_id = session.get("session_id")
        if session:
            asyncio.create_task(_send_loop_email(session))
    except Exception as exc:  # noqa: BLE001
        _log.warning("Study loop session error: %s", exc)
    finally:
        _running = False


# ── Email helper (H14: routes through Notifier) ─────────────────────────────


async def _send_loop_email(session: dict[str, Any]) -> None:
    """Send a study-loop-complete email via the backend Notifier.

    Swallows all exceptions with a warning log so the caller is never
    interrupted by email failures.
    """
    try:
        from glossa_lab.notifications.smtp import get_notifier  # noqa: PLC0415
        from glossa_lab.notifications.templates import (  # noqa: PLC0415
            format_study_loop_complete,
        )

        notifier = get_notifier()
        if not notifier.is_configured():
            _log.info("Study loop email: notifier not configured — skipping")
            return

        recipients = await notifier.list_active_recipients()
        if not recipients:
            _log.info("Study loop email: no active recipients — skipping")
            return

        subject, body_text, body_html = format_study_loop_complete(session)
        await notifier.send(
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            kind="study_loop_complete",
            recipients=recipients,
        )
        _log.info("Study loop completion email sent to %d recipient(s)",
                   len(recipients))
    except Exception as exc:  # noqa: BLE001
        _log.warning("Study loop email failed (non-critical): %s", exc)


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.post("/start")
async def start_loop(
    iterations: int = Query(15, ge=1, le=100),
) -> StreamingResponse:
    """Start the study loop and stream events as SSE."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    from glossa_lab.pipelines.study_loop import run_study_loop  # noqa: PLC0415

    global _running, _session_id, _iterations, _trigger, _started_at  # noqa: PLW0603

    if _running:
        return StreamingResponse(
            iter([f"data: {json.dumps({'type': 'error', 'reason': 'study loop already running'})}\n\n"]),
            media_type="text/event-stream",
        )

    _running = True
    _iterations = iterations
    _trigger = "user"
    _started_at = datetime.now(UTC).isoformat()
    _session_id = None

    # Create a job record
    db = get_db()
    job_id: str | None = None
    if db is not None:
        try:
            now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
            job = await db.create_job(
                name=f"Study Loop ({iterations} cycles)",
                pipeline="study_loop",
                params={"iterations": iterations},
                created_at=now,
                initial_status="running",
            )
            job_id = job["id"]
        except Exception as exc:  # noqa: BLE001
            _log.warning("Could not create job for study loop: %s", exc)

    async def event_stream():
        global _running, _session_id, _cycles_completed  # noqa: PLW0603
        session: dict[str, Any] | None = None
        _cycles_completed = 0
        try:
            async for event in run_study_loop(iterations=iterations, trigger="user"):
                yield f"data: {json.dumps(event, default=str)}\n\n"
                etype = event.get("type")
                if etype == "node_complete":
                    _cycles_completed += 1
                elif etype == "study_loop_complete":
                    session = event.get("session")
                    if session:
                        _session_id = session.get("session_id")
        except Exception as exc:  # noqa: BLE001
            _log.error("Study loop stream error: %s", exc)
            yield f"data: {json.dumps({'type': 'error', 'reason': str(exc)})}\n\n"

        # Mark job completed/failed
        if job_id and db:
            try:
                status = "completed" if session else "failed"
                await db.update_job_status(job_id, status)
            except Exception:  # noqa: BLE001
                pass

        # Send email (non-blocking)
        if session:
            asyncio.create_task(_send_loop_email(session))

        _running = False

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/status")
async def loop_status() -> dict[str, Any]:
    """Return current study loop state."""
    return {
        "running": _running,
        "session_id": _session_id,
        "iterations": _iterations,
        "cycles_completed": _cycles_completed,
        "trigger": _trigger,
        "started_at": _started_at,
    }


@router.post("/stop")
async def stop_loop() -> dict[str, str]:
    """Signal the running ResearchLoop to stop after the current cycle."""
    if not _running:
        return {"status": "idle", "message": "No study loop is running."}
    from glossa_lab.pipelines.study_loop import stop_active_loop  # noqa: PLC0415
    stopped = stop_active_loop()
    return {
        "status": "stop_requested",
        "message": "Loop will stop after the current cycle completes." if stopped
                   else "Stop signal sent (loop may have just finished).",
    }


@router.get("/history")
async def loop_history() -> dict[str, Any]:
    """Return all persisted study loop sessions (reverse chronological)."""
    sessions: list[dict[str, Any]] = []
    if _SESSIONS_JSON.exists():
        try:
            data = json.loads(_SESSIONS_JSON.read_text(encoding="utf-8"))
            if isinstance(data, list):
                sessions = data
        except Exception as exc:  # noqa: BLE001
            _log.warning("Could not read session history: %s", exc)
    # Return reverse chronological
    sessions.reverse()
    return {"sessions": sessions}


@router.get("/last-session")
async def last_session() -> dict[str, Any]:
    """Return the most recent session or indicate none exist."""
    if _SESSIONS_JSON.exists():
        try:
            data = json.loads(_SESSIONS_JSON.read_text(encoding="utf-8"))
            if isinstance(data, list) and data:
                return data[-1]
        except Exception as exc:  # noqa: BLE001
            _log.warning("Could not read session history: %s", exc)
    return {"no_sessions": True}


# ── Scheduler endpoints ─────────────────────────────────────────────────────


@router.get("/scheduler/status")
async def scheduler_status() -> dict[str, Any]:
    """Return scheduler state."""
    from glossa_lab import study_loop_scheduler  # noqa: PLC0415

    return {
        "enabled": study_loop_scheduler._enabled(),
        "running": study_loop_scheduler.is_running(),
        "interval_hours": study_loop_scheduler._interval_seconds() / 3600,
        "iterations": study_loop_scheduler._default_iterations(),
    }


@router.post("/scheduler/enable")
async def scheduler_enable() -> dict[str, Any]:
    """Enable the study loop scheduler at runtime."""
    from glossa_lab import study_loop_scheduler  # noqa: PLC0415

    newly_started = await study_loop_scheduler.enable_at_runtime()
    return {
        "enabled": True,
        "newly_started": newly_started,
        "message": "Study loop scheduler enabled.",
    }


@router.post("/scheduler/disable")
async def scheduler_disable() -> dict[str, Any]:
    """Disable the study loop scheduler at runtime."""
    from glossa_lab import study_loop_scheduler  # noqa: PLC0415

    was_stopped = await study_loop_scheduler.disable_at_runtime()
    return {
        "enabled": False,
        "was_stopped": was_stopped,
        "message": "Study loop scheduler disabled.",
    }
