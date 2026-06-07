"""Phase Advancement API.

Endpoints (mounted at /api/v1/phase):
  GET  /status   — current phase, coverage, next milestone, top 5 actions
  GET  /plan     — full action plan for current phase
  POST /advance  — execute top recommended action (queues a job)
  POST /override — manually override current phase in outputs/phase_state.json
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/phase", tags=["phase"])
_log = logging.getLogger("glossa_lab.api.phase")
_REPO = Path(__file__).resolve().parents[3]
_PHASE_STATE_JSON = _REPO / "outputs" / "phase_state.json"


def _advancer():
    from glossa_lab.pipelines.phase_advancer import PhaseAdvancer  # noqa: PLC0415
    return PhaseAdvancer()


@router.get("/status")
async def phase_status() -> dict[str, Any]:
    """Return current phase status and top 5 recommended actions."""
    adv = _advancer()
    status = adv.assess()
    plan = adv.plan_next()[:10]  # show more actions including Complete Phase
    remaining = adv.plan_next(include_done=False)
    # Read override if present
    override_phase: int | None = None
    if _PHASE_STATE_JSON.exists():
        try:
            state = json.loads(_PHASE_STATE_JSON.read_text(encoding="utf-8"))
            override_phase = state.get("override_phase")
        except Exception:  # noqa: BLE001
            pass
    # Merge DB-persisted action status into the plan
    from glossa_lab.database import get_db as _gdb  # noqa: PLC0415
    _db = _gdb()
    db_actions: dict[str, dict] = {}
    if _db:
        try:
            import asyncio as _aio  # noqa: PLC0415
            rows = await _db.list_phase_actions(phase=status.current_phase)
            db_actions = {r["action_label"]: r for r in rows}
        except Exception:  # noqa: BLE001
            pass

    enriched_actions = []
    for a in plan:
        db_entry = db_actions.get(a.label, {})
        enriched_actions.append({
            "action_type": a.action_type,
            "label": a.label,
            "rationale": a.rationale,
            "params": a.params,
            "priority": a.priority,
            "db_status": db_entry.get("status", "pending"),
            "job_id": db_entry.get("job_id"),
            "error_message": db_entry.get("error_message", ""),
            "completed_at": db_entry.get("completed_at"),
        })

    return {
        **asdict(status),
        "override_phase": override_phase,
        "top_actions": enriched_actions,
        "remaining_actions": len(remaining),
        "all_done": len(remaining) == 0 and len(plan) > 0,
    }


@router.get("/plan")
async def phase_plan() -> dict[str, Any]:
    """Return full action plan for the current phase."""
    adv = _advancer()
    status = adv.assess()
    plan = adv.plan_next()
    return {
        "current_phase": status.current_phase,
        "phase_label": status.phase_label,
        "coverage": status.coverage,
        "next_milestone": status.next_milestone,
        "actions": [
            {
                "action_type": a.action_type,
                "label": a.label,
                "rationale": a.rationale,
                "params": a.params,
                "priority": a.priority,
            }
            for a in plan
        ],
    }


@router.post("/advance")
async def advance_phase() -> dict[str, Any]:
    """Execute the highest-priority READY action for the current phase.

    An action is 'ready' if all its dependencies (depends_on) are completed/skipped.
    Running actions are not re-queued. Failed actions stay on the list.
    Returns {ok, action_taken, job_id, message, current_phase, coverage}.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    adv = _advancer()
    result = await adv.advance(db=db)
    if result.ok:
        try:
            from glossa_lab.api.dashboard import mark_insights_stale  # noqa: PLC0415
            mark_insights_stale()
        except Exception:  # noqa: BLE001
            pass
    return {
        "ok": result.ok,
        "action_taken": result.action_taken,
        "action_type": result.action_type,
        "job_id": result.job_id,
        "experiment_id": result.experiment_id,
        "message": result.message,
        "current_phase": result.current_phase,
        "coverage": result.coverage,
    }


@router.post("/advance-all")
async def advance_all_ready() -> dict[str, Any]:
    """Queue ALL ready (non-blocked, non-running) actions at once.

    Dependency-aware: only queues actions whose depends_on are all completed/skipped.
    Returns list of results for each action attempted.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    adv = _advancer()
    results: list[dict] = []
    for _ in range(20):  # safety cap
        result = await adv.advance(db=db)
        if not result.ok:
            break
        results.append({
            "action": result.action_taken,
            "type": result.action_type,
            "job_id": result.job_id,
            "message": result.message,
        })
        # Stop if we hit complete_phase
        if result.action_type == "complete_phase":
            break
    if results:
        try:
            from glossa_lab.api.dashboard import mark_insights_stale  # noqa: PLC0415
            mark_insights_stale()
        except Exception:  # noqa: BLE001
            pass
    status = adv.assess()
    return {
        "ok": len(results) > 0,
        "queued": len(results),
        "results": results,
        "current_phase": status.current_phase,
        "phase_label": status.phase_label,
        "coverage": status.coverage,
    }


@router.get("/actions")
async def list_phase_actions(phase: int | None = None) -> dict[str, Any]:
    """Return all tracked phase actions with DB-persisted status."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return {"actions": [], "error": "database not available"}
    actions = await db.list_phase_actions(phase=phase)
    return {"actions": actions}


@router.post("/actions/{label}/skip")
async def skip_phase_action(label: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    """Skip a phase action (mark as skipped)."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return {"ok": False, "error": "database not available"}
    phase = (body or {}).get("phase")
    if phase is None:
        adv = _advancer()
        phase = adv.assess().current_phase
    result = await db.upsert_phase_action(
        phase=phase, label=label, status="skipped")
    return {"ok": True, "action": result}


@router.post("/actions/{label}/redo")
async def redo_phase_action(label: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    """Reset a completed/failed/skipped action back to pending."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return {"ok": False, "error": "database not available"}
    phase = (body or {}).get("phase")
    if phase is None:
        adv = _advancer()
        phase = adv.assess().current_phase
    result = await db.reset_phase_action(phase, label)
    return {"ok": True, "action": result}


@router.get("/goals")
async def get_phase_goals() -> dict[str, Any]:
    """Return current phase goals (dynamic or default)."""
    from glossa_lab.pipelines.phase_generator import load_phase_goals  # noqa: PLC0415
    from glossa_lab.config import _DEFAULT_PHASE_GOALS, PhaseGoal  # noqa: PLC0415
    saved = load_phase_goals()
    if saved:
        return {"goals": saved, "source": "dynamic", "editable": True}
    # Convert defaults to dicts
    from dataclasses import asdict as _asdict  # noqa: PLC0415
    defaults = [_asdict(g) for g in _DEFAULT_PHASE_GOALS]
    return {"goals": defaults, "source": "default", "editable": True}


@router.post("/goals")
async def save_phase_goals_endpoint(body: dict[str, Any]) -> dict[str, Any]:
    """Save edited phase goals.

    Body: {goals: [...]}  — list of phase goal dicts.
    """
    from glossa_lab.pipelines.phase_generator import save_phase_goals  # noqa: PLC0415
    from glossa_lab.config import reload_project_config  # noqa: PLC0415
    goals = body.get("goals", [])
    if not goals:
        return {"ok": False, "error": "No goals provided"}
    path = save_phase_goals(goals)
    reload_project_config()  # pick up the new goals
    return {"ok": True, "saved": len(goals), "path": str(path.name)}


@router.post("/generate")
async def generate_phase_goals_endpoint() -> dict[str, Any]:
    """Auto-generate phase goals from current project state and save them."""
    from glossa_lab.pipelines.phase_generator import (  # noqa: PLC0415
        generate_phase_goals,
        save_phase_goals,
    )
    from glossa_lab.config import reload_project_config  # noqa: PLC0415
    goals = generate_phase_goals()
    path = save_phase_goals(goals)
    reload_project_config()
    return {"ok": True, "generated": len(goals), "goals": goals, "path": str(path.name)}


@router.post("/override")
async def override_phase(body: dict[str, Any]) -> dict[str, Any]:
    """Manually set a phase override stored in outputs/phase_state.json.

    Body: {phase: int} or {phase: null} to clear override.
    """
    phase = body.get("phase")
    if phase is not None and not isinstance(phase, int):
        return {"ok": False, "error": "phase must be an integer or null"}
    _PHASE_STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    state: dict = {}
    if _PHASE_STATE_JSON.exists():
        try:
            state = json.loads(_PHASE_STATE_JSON.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            state = {}
    if phase is None:
        state.pop("override_phase", None)
    else:
        state["override_phase"] = phase
    _PHASE_STATE_JSON.write_text(
        json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"ok": True, "override_phase": phase}
