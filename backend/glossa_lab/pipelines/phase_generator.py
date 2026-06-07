"""Dynamic Phase Generator — auto-generates research phase goals from project state.

Examines available experiments, current coverage, anchor quality, and project
type to produce a PhaseGoal list. Results are persisted to outputs/phase_goals.json
so the user can review and edit them.

Usage:
    goals = generate_phase_goals()           # auto-generate from current state
    save_phase_goals(goals)                  # persist to JSON
    goals = load_phase_goals()               # load persisted (or fall back to defaults)
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

_log = logging.getLogger("glossa_lab.phase_generator")
_REPO = Path(__file__).resolve().parents[3]
_GOALS_JSON = _REPO / "outputs" / "phase_goals.json"


def _available_experiment_ids() -> set[str]:
    """Return IDs of all registered graph experiments."""
    try:
        from glossa_lab.experiment_graph import list_graph_experiments  # noqa: PLC0415
        return {e["id"] for e in list_graph_experiments()}
    except Exception:  # noqa: BLE001
        return set()


def _categorise_experiments(available: set[str]) -> dict[str, list[str]]:
    """Categorise available experiments by purpose."""
    cats: dict[str, list[str]] = {
        "bootstrap_sa": [],
        "growth_sa": [],
        "validation": [],
        "structural": [],
        "falsification": [],
        "cross_validation": [],
        "benchmark": [],
    }
    for eid in sorted(available):
        el = eid.lower()
        if "neg_control" in el or "falsif" in el:
            cats["falsification"].append(eid)
        elif "kalyanaraman" in el or "crossval" in el:
            cats["cross_validation"].append(eid)
        elif "validation" in el or "holdout" in el:
            cats["validation"].append(eid)
        elif "structural" in el or "cgsa" in el or "atlas" in el or "entropy" in el:
            cats["structural"].append(eid)
        elif "benchmark" in el or "ventris" in el or "ugaritic" in el:
            cats["benchmark"].append(eid)
        elif "anchor_sweep" in el or "syllable" in el or "multi_comparison" in el:
            cats["bootstrap_sa"].append(eid)
        elif "dravidian" in el or "sanskrit" in el or "cisi" in el:
            cats["growth_sa"].append(eid)
    return cats


def generate_phase_goals() -> list[dict[str, Any]]:
    """Auto-generate phase goals from available experiments and project state.

    Returns a list of phase goal dicts (JSON-serialisable).
    """
    available = _available_experiment_ids()
    cats = _categorise_experiments(available)

    # Read current project state for context
    try:
        from glossa_lab.config import get_project_config  # noqa: PLC0415
        cfg = get_project_config()
        anchors_path = cfg.anchors_json_path()
        if anchors_path.exists():
            fa = json.loads(anchors_path.read_text(encoding="utf-8"))
            coverage = float(fa.get("corpus_token_coverage", 0) or 0)
        else:
            coverage = 0.0
    except Exception:  # noqa: BLE001
        coverage = 0.0

    goals: list[dict[str, Any]] = []

    # Phase 1: Bootstrap (0–30%)
    goals.append({
        "phase": 1,
        "label": "Bootstrap",
        "description": (
            "Run initial SA experiments to find anchor candidates. "
            "Mine literature for corroborating evidence."
        ),
        "min_coverage": 0.0,
        "max_coverage": 0.30,
        "recommended_experiments": cats["bootstrap_sa"][:3],
        "recommended_actions": [
            {"action_type": "run_experiment", "label": f"Queue: {eid.replace('_', ' ').title()}",
             "rationale": "Initial SA exploration", "params": {"experiment_id": eid}}
            for eid in cats["bootstrap_sa"][:2]
        ],
    })

    # Phase 2: Growth (30–60%)
    goals.append({
        "phase": 2,
        "label": "Growth",
        "description": "Expand anchor coverage with broader SA experiments.",
        "min_coverage": 0.30,
        "max_coverage": 0.60,
        "recommended_experiments": cats["growth_sa"][:3],
        "recommended_actions": [
            {"action_type": "run_experiment", "label": f"Queue: {eid.replace('_', ' ').title()}",
             "rationale": "Widen coverage with full-corpus SA", "params": {"experiment_id": eid}}
            for eid in cats["growth_sa"][:2]
        ],
    })

    # Phase 3: Validation (60–85%)
    goals.append({
        "phase": 3,
        "label": "Validation",
        "description": "Validate assignments with held-out data and negative controls.",
        "min_coverage": 0.60,
        "max_coverage": 0.85,
        "recommended_experiments": cats["validation"][:3],
        "recommended_actions": [
            {"action_type": "run_experiment", "label": f"Queue: {eid.replace('_', ' ').title()}",
             "rationale": "Cross-validate anchor assignments", "params": {"experiment_id": eid}}
            for eid in cats["validation"][:2]
        ],
    })

    # Phase 4: Completion (85–95%)
    goals.append({
        "phase": 4,
        "label": "Completion",
        "description": "Fill remaining gaps to reach 95%+ coverage.",
        "min_coverage": 0.85,
        "max_coverage": 0.95,
        "recommended_experiments": cats["structural"][:3],
        "recommended_actions": [
            {"action_type": "run_experiment", "label": f"Queue: {eid.replace('_', ' ').title()}",
             "rationale": "Map unanchored signs by structure", "params": {"experiment_id": eid}}
            for eid in cats["structural"][:2]
        ],
    })

    # Phase 5: Done (95%+)
    done_exps = cats["growth_sa"][:2]
    goals.append({
        "phase": 5,
        "label": "Done",
        "description": (
            "Target reached: ≥95% coverage. Run final SA validation and regenerate insights."
        ),
        "min_coverage": 0.95,
        "max_coverage": 1.01,
        "recommended_experiments": done_exps,
        "recommended_actions": [
            {"action_type": "regenerate_insights", "label": "Regenerate AI Insights",
             "rationale": "Refresh insights to reflect validated anchor set.", "params": {}},
            {"action_type": "open_view", "label": "Review Promoted Signs",
             "rationale": "Spot-check readings in the Signs index.", "params": {"view": "signs"}},
        ],
    })

    # Phase 6: Peer Review (95%+, after Phase 5 completed)
    peer_exps = cats["cross_validation"] + cats["falsification"]
    goals.append({
        "phase": 6,
        "label": "Peer Review",
        "description": (
            "Prepare for external review: independent cross-validation, "
            "falsification suite, foundation report."
        ),
        "min_coverage": 0.95,
        "max_coverage": 1.01,
        "recommended_experiments": peer_exps[:3],
        "recommended_actions": [
            {"action_type": "run_experiment", "label": f"Queue: {eid.replace('_', ' ').title()}",
             "rationale": "Independent validation for peer review", "params": {"experiment_id": eid}}
            for eid in peer_exps[:2]
        ] + [
            {"action_type": "open_view", "label": "Generate Foundation Report",
             "rationale": "Create PDF summary for external review.", "params": {"view": "foundation"}},
        ],
    })

    # Phase 7: Publication (95%+, after Phase 6 completed)
    goals.append({
        "phase": 7,
        "label": "Publication",
        "description": "All validations passed. Ready for academic publication.",
        "min_coverage": 0.95,
        "max_coverage": 1.01,
        "recommended_experiments": [],
        "recommended_actions": [
            {"action_type": "open_view", "label": "Review Final Report",
             "rationale": "Review complete evidence chain.", "params": {"view": "foundation"}},
        ],
    })

    return goals


def save_phase_goals(goals: list[dict[str, Any]]) -> Path:
    """Persist phase goals to outputs/phase_goals.json."""
    _GOALS_JSON.parent.mkdir(parents=True, exist_ok=True)
    _GOALS_JSON.write_text(
        json.dumps({"goals": goals, "_auto_generated": True}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    _log.info("Saved %d phase goals to %s", len(goals), _GOALS_JSON)
    return _GOALS_JSON


def load_phase_goals() -> list[dict[str, Any]] | None:
    """Load phase goals from outputs/phase_goals.json. Returns None if not found."""
    if not _GOALS_JSON.exists():
        return None
    try:
        data = json.loads(_GOALS_JSON.read_text(encoding="utf-8"))
        return data.get("goals", [])
    except Exception as exc:  # noqa: BLE001
        _log.warning("Could not load phase_goals.json: %s", exc)
        return None


def goals_to_phase_goals(goal_dicts: list[dict[str, Any]]) -> list:
    """Convert JSON goal dicts to PhaseGoal dataclass instances."""
    from glossa_lab.config import PhaseGoal  # noqa: PLC0415
    result = []
    for g in goal_dicts:
        result.append(PhaseGoal(
            phase=g["phase"],
            label=g["label"],
            description=g.get("description", ""),
            min_coverage=g.get("min_coverage", 0.0),
            max_coverage=g.get("max_coverage", 1.01),
            recommended_experiments=g.get("recommended_experiments", []),
            recommended_actions=g.get("recommended_actions", []),
        ))
    return result
