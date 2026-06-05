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
    plan = adv.plan_next()[:5]
    remaining = adv.plan_next(include_done=False)
    # Read override if present
    override_phase: int | None = None
    if _PHASE_STATE_JSON.exists():
        try:
            state = json.loads(_PHASE_STATE_JSON.read_text(encoding="utf-8"))
            override_phase = state.get("override_phase")
        except Exception:  # noqa: BLE001
            pass
    return {
        **asdict(status),
        "override_phase": override_phase,
        "top_actions": [
            {
                "action_type": a.action_type,
                "label": a.label,
                "rationale": a.rationale,
                "params": a.params,
                "priority": a.priority,
            }
            for a in plan
        ],
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
    """Execute the highest-priority action for the current phase.

    Queues a job for run_experiment / run_research_loop actions.
    Returns {ok, action_taken, job_id, message, current_phase, coverage}.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    adv = _advancer()
    result = await adv.advance(db=db)
    # Mark insights stale — the research plan has changed, insights should refresh
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
