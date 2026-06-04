"""Phase Advancement — automated research phase planning and execution.

The PhaseAdvancer reads current project state (anchor coverage, staging,
foundation check) and determines which research phase the project is in,
what actions are recommended for the next phase, and can execute the top
action by queuing a job.

API usage:
    advancer = PhaseAdvancer()
    status = advancer.assess()
    plan = advancer.plan_next()
    result = await advancer.advance(db)
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_log = logging.getLogger("glossa_lab.phase_advancer")
_REPO = Path(__file__).resolve().parents[3]  # repo root


@dataclass
class PhaseStatus:
    """Current phase assessment."""
    current_phase: int
    phase_label: str
    phase_description: str
    coverage: float           # corpus_token_coverage (0–1)
    next_milestone: float     # coverage threshold for next phase
    gap_to_next: float        # next_milestone - coverage
    n_staged: int
    n_rejected: int
    n_approved: int
    foundation_ok: bool
    anchors_total: int
    anchors_hm: int           # HIGH + MEDIUM confidence anchors


@dataclass
class PhaseAction:
    """A recommended action for phase advancement.

    action_type values:
      run_experiment    — queue a graph experiment as a background job
      review_candidates — informational: staged candidates need review (no job queued)
      verify_sa         — informational: approved candidates ready to archive (no job queued)
      open_view         — informational: navigate to a specific view (no job queued)

    Note: 'run_research_loop' is intentionally NOT supported here. The Research Loop
    is a paper-mining SSE stream that must be started manually from the loop panel.
    It operates independently of the phase advancement system.
    """
    action_type: str
    label: str
    rationale: str
    params: dict
    priority: int       # lower = higher priority


@dataclass
class PhaseAdvanceResult:
    """Result of executing a phase advance action."""
    ok: bool
    action_taken: str
    action_type: str
    job_id: str | None
    experiment_id: str | None
    message: str
    current_phase: int
    coverage: float


class PhaseAdvancer:
    """Assess project phase and advance to next milestone."""

    def __init__(self) -> None:
        from glossa_lab.config import get_project_config  # noqa: PLC0415
        self.cfg = get_project_config()

    def _read_anchors(self) -> dict[str, Any]:
        """Read INDUS_FINAL_ANCHORS.json for coverage metrics."""
        anchors_path = self.cfg.anchors_json_path()
        if not anchors_path.exists():
            return {}
        try:
            return json.loads(anchors_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            _log.warning("Could not read anchors: %s", exc)
            return {}

    def _read_staging_counts(self) -> dict[str, int]:
        """Read staging counts from anchor_staging.json."""
        staging_path = _REPO / "outputs" / "anchor_staging.json"
        if not staging_path.exists():
            return {"staged": 0, "approved": 0, "rejected": 0}
        try:
            candidates: list[dict] = json.loads(
                staging_path.read_text(encoding="utf-8"))
            return {
                "staged":   sum(1 for c in candidates if c.get("review_status") == "staged"),
                "approved": sum(1 for c in candidates if c.get("review_status") == "approved"),
                "rejected": sum(1 for c in candidates if c.get("review_status") == "rejected"),
            }
        except Exception:  # noqa: BLE001
            return {"staged": 0, "approved": 0, "rejected": 0}

    def _read_foundation_ok(self) -> bool:
        """Return True if foundation check has no failures."""
        fc_path = _REPO / "reports" / "foundation_check_report.json"
        if not fc_path.exists():
            return True  # optimistic default
        try:
            fc = json.loads(fc_path.read_text(encoding="utf-8"))
            return int(fc.get("n_fail", 0)) == 0
        except Exception:  # noqa: BLE001
            return True

    def _get_phase_for_coverage(self, coverage: float) -> Any:
        """Return the PhaseGoal that matches the given coverage."""
        from glossa_lab.config import _DEFAULT_PHASE_GOALS  # noqa: PLC0415
        goals = getattr(self.cfg, "phase_goals", None) or _DEFAULT_PHASE_GOALS
        for goal in sorted(goals, key=lambda g: g.phase):
            if goal.min_coverage <= coverage < goal.max_coverage:
                return goal
        # Fallback: last goal
        return sorted(goals, key=lambda g: g.phase)[-1]

    def assess(self) -> PhaseStatus:
        """Read current project state and return phase status."""
        anchors_data = self._read_anchors()
        coverage = float(anchors_data.get("corpus_token_coverage", 0.0) or 0.0)

        by_conf: dict[str, int] = {}
        for _, info in (anchors_data.get("anchors") or {}).items():
            c = (info.get("confidence") or "LOW").upper()
            by_conf[c] = by_conf.get(c, 0) + 1
        anchors_hm = by_conf.get("HIGH", 0) + by_conf.get("MEDIUM", 0)
        anchors_total = sum(by_conf.values())

        staging = self._read_staging_counts()
        foundation_ok = self._read_foundation_ok()

        current_goal = self._get_phase_for_coverage(coverage)
        from glossa_lab.config import _DEFAULT_PHASE_GOALS  # noqa: PLC0415
        goals = getattr(self.cfg, "phase_goals", None) or _DEFAULT_PHASE_GOALS
        sorted_goals = sorted(goals, key=lambda g: g.phase)
        next_goal = next(
            (g for g in sorted_goals if g.phase > current_goal.phase),
            current_goal,
        )
        next_milestone = next_goal.min_coverage if next_goal.phase > current_goal.phase else 1.0

        return PhaseStatus(
            current_phase=current_goal.phase,
            phase_label=current_goal.label,
            phase_description=current_goal.description,
            coverage=round(coverage, 4),
            next_milestone=round(next_milestone, 4),
            gap_to_next=round(max(0.0, next_milestone - coverage), 4),
            n_staged=staging["staged"],
            n_rejected=staging["rejected"],
            n_approved=staging["approved"],
            foundation_ok=foundation_ok,
            anchors_total=anchors_total,
            anchors_hm=anchors_hm,
        )

    def plan_next(self) -> list[PhaseAction]:
        """Return ordered list of recommended actions for the current phase."""
        status = self.assess()
        current_goal = self._get_phase_for_coverage(status.coverage)
        actions: list[PhaseAction] = []

        priority = 0

        # 0. Foundation failures take top priority
        if not status.foundation_ok:
            actions.append(PhaseAction(
                action_type="open_view",
                label="Fix Foundation Check failures",
                rationale=(
                    "Foundation check has failures — go to Foundation Check view. "
                    "Auto-fixes are available for most issues (blue ⚡ buttons). "
                    "Note: fixing foundation check does NOT block phase advancement — "
                    "it is a data integrity audit, not a gate."
                ),
                params={"view": "foundation"},
                priority=priority,
            ))
            priority += 1

        # 1. Staged candidates should be reviewed before running more experiments
        if status.n_staged > 0:
            actions.append(PhaseAction(
                action_type="review_candidates",
                label=f"Review {status.n_staged} staged candidate(s)",
                rationale="Staged candidates are waiting for approval/rejection.",
                params={"view": "research_loop", "tab": "staging"},
                priority=priority,
            ))
            priority += 1

        # 2. Approved candidates should be verified
        if status.n_approved > 0:
            actions.append(PhaseAction(
                action_type="verify_sa",
                label=f"Verify {status.n_approved} approved candidate(s)",
                rationale="Approved candidates are ready to be verified and archived.",
                params={},
                priority=priority,
            ))
            priority += 1

        # 3. Phase-specific recommended actions (from config)
        # These may include run_experiment entries from recommended_experiments + recommended_actions.
        # run_research_loop is intentionally excluded — it can't be queued as a background job.
        seen_exp_ids: set[str] = set()
        for exp_id in current_goal.recommended_experiments:
            if exp_id in seen_exp_ids:
                continue
            seen_exp_ids.add(exp_id)
            actions.append(PhaseAction(
                action_type="run_experiment",
                label=f"Queue: {exp_id.replace('_', ' ').title()}",
                rationale=(
                    f"Recommended SA/validation experiment for {current_goal.label} phase "
                    f"(coverage {status.coverage:.1%} → target {status.next_milestone:.1%})"
                ),
                params={"experiment_id": exp_id},
                priority=priority,
            ))
            priority += 1

        for act in current_goal.recommended_actions:
            atype = act.get("action_type", "no_op")
            # Skip run_research_loop — the Research Loop is a separate manual tool
            # and cannot be queued as a background job from the Phase Advancer.
            if atype == "run_research_loop":
                continue
            exp_id_act = act.get("params", {}).get("experiment_id", "")
            if exp_id_act and exp_id_act in seen_exp_ids:
                continue  # already added via recommended_experiments
            if exp_id_act:
                seen_exp_ids.add(exp_id_act)
            actions.append(PhaseAction(
                action_type=atype,
                label=act.get("label", ""),
                rationale=act.get("rationale", ""),
                params=act.get("params", {}),
                priority=priority,
            ))
            priority += 1

        # 4. If no experiment actions available, suggest using the Research Loop
        has_experiment_actions = any(a.action_type == "run_experiment" for a in actions)
        if not has_experiment_actions and current_goal.phase < 5:
            actions.append(PhaseAction(
                action_type="open_view",
                label="No experiments queued — use Manual Loop for paper mining",
                rationale=(
                    "No SA experiments are configured for this phase. "
                    "Use the Research Loop below to mine literature for anchor candidates."
                ),
                params={"view": "research_loop"},
                priority=priority,
            ))

        return sorted(actions, key=lambda a: a.priority)

    async def advance(self, db: Any = None) -> PhaseAdvanceResult:
        """Execute the highest-priority recommended action.

        Queues a job for experiment or research loop actions.
        Returns a PhaseAdvanceResult with job_id if applicable.
        """
        status = self.assess()
        plan = self.plan_next()
        if not plan:
            return PhaseAdvanceResult(
                ok=False, action_taken="none", action_type="no_op",
                job_id=None, experiment_id=None,
                message="No actions planned for current phase.",
                current_phase=status.current_phase, coverage=status.coverage,
            )

        top = plan[0]
        job_id: str | None = None
        exp_id: str | None = None

        try:
            if top.action_type == "run_experiment":
                exp_id = top.params.get("experiment_id", "")
                if exp_id and db:
                    from glossa_lab.experiment_graph import queue_graph_experiment  # noqa: PLC0415
                    job = await queue_graph_experiment(exp_id, db=db)
                    job_id = job.get("id") if job else None
                message = (
                    f"Experiment queued: {top.label}"
                    + (f" — job {job_id}" if job_id else " (no DB, dry-run)")
                    + ". Monitor progress in the Jobs panel."
                )

            elif top.action_type in ("review_candidates", "verify_sa"):
                # Informational actions — no job queued; user action required in UI
                message = (
                    f"{top.label} — no job needed. "
                    "Go to the Staging Review queue below to take action."
                )

            elif top.action_type == "regenerate_insights":
                message = f"{top.label} — navigate to Dashboard to regenerate"

            elif top.action_type == "open_view":
                message = f"{top.label}"

            else:
                message = f"Action acknowledged: {top.label}"

            return PhaseAdvanceResult(
                ok=True,
                action_taken=top.label,
                action_type=top.action_type,
                job_id=job_id,
                experiment_id=exp_id,
                message=message,
                current_phase=status.current_phase,
                coverage=status.coverage,
            )
        except Exception as exc:  # noqa: BLE001
            _log.error("Phase advance failed: %s", exc)
            return PhaseAdvanceResult(
                ok=False, action_taken=top.label, action_type=top.action_type,
                job_id=None, experiment_id=None,
                message=f"Advance failed: {exc}",
                current_phase=status.current_phase, coverage=status.coverage,
            )
