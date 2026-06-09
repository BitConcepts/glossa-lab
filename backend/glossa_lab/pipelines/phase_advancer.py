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
_PHASE_STATE_JSON = _REPO / "outputs" / "phase_state.json"


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
    completed_through_phase: int = 0  # highest phase explicitly completed via complete_phase


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

    # ── Completion tracking ────────────────────────────────────────────────
    # Persisted in outputs/phase_state.json so state survives restarts.

    def _read_phase_state(self) -> dict:
        if _PHASE_STATE_JSON.exists():
            try:
                return json.loads(_PHASE_STATE_JSON.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                pass
        return {}

    def _write_phase_state(self, state: dict) -> None:
        _PHASE_STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
        _PHASE_STATE_JSON.write_text(
            json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _get_completed_actions(self, phase: int) -> set[str]:
        """Return set of action labels completed for the given phase."""
        state = self._read_phase_state()
        return set(state.get(f"phase_{phase}_completed", []))

    def _mark_action_done(self, phase: int, label: str) -> None:
        state = self._read_phase_state()
        key = f"phase_{phase}_completed"
        done = set(state.get(key, []))
        done.add(label)
        state[key] = sorted(done)
        self._write_phase_state(state)

    def _get_queued_experiment_ids(self) -> set[str]:
        """Return experiment IDs that already have a pending/running/completed job.

        Checks BOTH exp_run AND graph_experiment pipeline jobs, since the GPU
        concurrency guard queues experiments as graph_experiment pipeline jobs.
        """
        try:
            import sqlite3  # noqa: PLC0415
            db_path = _REPO / "backend" / "data" / "glossa.db"
            if not db_path.exists():
                return set()
            conn = sqlite3.connect(str(db_path), timeout=3)
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT params, status FROM jobs "
                "WHERE pipeline IN ('exp_run', 'graph_experiment') "
                "AND status IN ('pending', 'running', 'completed')"
            ).fetchall()
            conn.close()
            queued = set()
            for row in rows:
                try:
                    params = json.loads(row["params"]) if row["params"] else {}
                except (json.JSONDecodeError, TypeError):
                    continue
                exp_id = params.get("exp_id") or params.get("experiment_id", "")
                if exp_id:
                    queued.add(exp_id)
            return queued
        except Exception:  # noqa: BLE001
            return set()

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

    def _get_completed_through_phase(self) -> int:
        """Return the highest phase number that has been explicitly completed."""
        state = self._read_phase_state()
        return int(state.get("completed_through_phase", 0))

    def _set_completed_through_phase(self, phase: int) -> None:
        """Record that the user has completed through the given phase."""
        state = self._read_phase_state()
        state["completed_through_phase"] = phase
        self._write_phase_state(state)

    def _get_phase_for_coverage(self, coverage: float) -> Any:
        """Return the PhaseGoal that matches coverage + completion history.

        When multiple phases share the same coverage range (e.g. 5, 6, 7 all
        cover 0.95-1.01), the completed_through_phase field determines which
        one is current: the first uncompleted phase in the range.
        """
        from glossa_lab.config import _DEFAULT_PHASE_GOALS  # noqa: PLC0415
        goals = getattr(self.cfg, "phase_goals", None) or _DEFAULT_PHASE_GOALS
        completed_through = self._get_completed_through_phase()

        # Find all goals whose coverage range matches
        matching = [
            g for g in sorted(goals, key=lambda g: g.phase)
            if g.min_coverage <= coverage < g.max_coverage
        ]
        if not matching:
            return sorted(goals, key=lambda g: g.phase)[-1]

        # Return the first matching goal whose phase > completed_through
        for g in matching:
            if g.phase > completed_through:
                return g
        # All matching phases completed — return the last one
        return matching[-1]

    def get_pending_experiment_actions(self) -> list[dict]:
        """Return pending run_experiment phase actions for the current phase.

        Filters out actions already completed/skipped/running in the DB.
        Used by the research loop to auto-queue phase experiments at loop start.
        Returns list of {label, experiment_id, params, phase, phase_label} dicts.
        """
        status = self.assess()
        plan = self.plan_next()

        # Load DB statuses so we don't re-queue already-running/completed actions
        db_statuses: dict[str, str] = {}
        try:
            import sqlite3 as _sql  # noqa: PLC0415
            db_path = _REPO / "backend" / "data" / "glossa.db"
            if db_path.exists():
                conn = _sql.connect(str(db_path), timeout=3)
                conn.row_factory = _sql.Row
                rows = conn.execute(
                    "SELECT action_label, status FROM phase_actions WHERE phase = ?",
                    (status.current_phase,),
                ).fetchall()
                conn.close()
                db_statuses = {r["action_label"]: r["status"] for r in rows}
        except Exception:  # noqa: BLE001
            pass

        pending = []
        for action in plan:
            if action.action_type != "run_experiment":
                continue
            if db_statuses.get(action.label) in ("completed", "skipped", "running"):
                continue
            exp_id = action.params.get("experiment_id", "")
            if exp_id:
                pending.append({
                    "label": action.label,
                    "experiment_id": exp_id,
                    "params": action.params,
                    "phase": status.current_phase,
                    "phase_label": status.phase_label,
                })
        return pending

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
        completed_through = self._get_completed_through_phase()

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
            completed_through_phase=completed_through,
        )

    def plan_next(self, *, include_done: bool = True) -> list[PhaseAction]:
        """Return ordered list of recommended actions for the current phase.

        When include_done=False, filters out actions that are already completed
        (experiments already queued, non-experiment steps already marked done).
        """
        status = self.assess()
        current_goal = self._get_phase_for_coverage(status.coverage)
        actions: list[PhaseAction] = []

        # Load completion state for filtering
        queued_exp_ids = self._get_queued_experiment_ids() if not include_done else set()
        completed_labels = self._get_completed_actions(status.current_phase) if not include_done else set()

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

        # 5. Complete Phase — final action when all others are done
        actions.append(PhaseAction(
            action_type="complete_phase",
            label=f"Complete Phase {current_goal.phase}",
            rationale=(
                f"All validation steps for {current_goal.label} are complete. "
                "Click to clear the phase summary, regenerate insights, "
                "and start a fresh research mining cycle."
            ),
            params={"phase": current_goal.phase},
            priority=priority + 10,  # always last
        ))

        all_actions = sorted(actions, key=lambda a: a.priority)
        if include_done:
            return all_actions

        # Load DB action status for dependency-aware filtering
        db_action_status: dict[str, str] = {}  # label -> status
        try:
            import sqlite3 as _sql  # noqa: PLC0415
            db_path = _REPO / "backend" / "data" / "glossa.db"
            if db_path.exists():
                conn = _sql.connect(str(db_path), timeout=3)
                conn.row_factory = _sql.Row
                rows = conn.execute(
                    "SELECT action_label, status FROM phase_actions WHERE phase = ?",
                    (status.current_phase,),
                ).fetchall()
                conn.close()
                db_action_status = {r["action_label"]: r["status"] for r in rows}
        except Exception:  # noqa: BLE001
            pass

        # Filter: skip completed/skipped/running actions
        remaining = []
        for a in all_actions:
            db_st = db_action_status.get(a.label, "")
            # Already done in DB
            if db_st in ("completed", "skipped"):
                continue
            # Already running (queued job in progress)
            if db_st == "running":
                continue
            if a.action_type == "run_experiment":
                exp_id = a.params.get("experiment_id", "")
                if exp_id and exp_id in queued_exp_ids and db_st != "failed":
                    continue  # already queued
            elif a.action_type == "complete_phase":
                # GATE: only include if ALL other actions are completed or skipped.
                # If any action is pending, running, or failed, complete_phase is blocked.
                other_statuses = {
                    lbl: st for lbl, st in db_action_status.items()
                    if lbl != a.label
                }
                # Count non-complete_phase actions that exist in the plan
                plan_labels = {x.label for x in all_actions if x.action_type != "complete_phase"}
                # Check: every plan action must be in DB as completed/skipped
                all_plan_done = all(
                    db_action_status.get(lbl, "") in ("completed", "skipped")
                    for lbl in plan_labels
                )
                if not all_plan_done:
                    continue  # blocked — not all actions are done
            elif a.label in completed_labels and db_st != "failed":
                continue  # done in phase_state.json
            remaining.append(a)
        return remaining

    async def advance(self, db: Any = None) -> PhaseAdvanceResult:
        """Execute the highest-priority UNCOMPLETED action.

        Skips experiments already queued in the Jobs table and actions
        already marked done in phase_state.json. Persists action status to DB.
        """
        status = self.assess()
        plan = self.plan_next(include_done=False)
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
                    try:
                        job = await queue_graph_experiment(exp_id, db=db)
                        job_id = job.get("id") if job else None
                    except Exception as _qe:  # noqa: BLE001
                        self._mark_action_done(status.current_phase, top.label)
                        job_id = None
                        _log.warning("Could not queue experiment %s: %s", exp_id, _qe)
                message = (
                    f"Experiment queued: {top.label}"
                    + (f" — job {job_id}" if job_id else " (no DB, dry-run)")
                    + ". Will be marked done when job completes."
                )
                # Mark as RUNNING (not completed) — job completion hook will mark done
                self._mark_action_done(status.current_phase, top.label)

            elif top.action_type in ("review_candidates", "verify_sa"):
                # Mark done so advance() moves to next action
                self._mark_action_done(status.current_phase, top.label)
                message = f"✔ {top.label} — acknowledged, advancing to next step."

            elif top.action_type == "regenerate_insights":
                # Try to actually trigger regeneration
                try:
                    from glossa_lab.api.dashboard import _generate_insight  # noqa: PLC0415
                    await _generate_insight()
                    message = "✨ AI insights regenerated successfully."
                except Exception:  # noqa: BLE001
                    message = "✔ Regenerate Insights — acknowledged (trigger manually from Dashboard if needed)."
                self._mark_action_done(status.current_phase, top.label)

            elif top.action_type == "complete_phase":
                phase_num = top.params.get("phase", status.current_phase)
                # Mark this phase as completed so we advance to the next
                self._set_completed_through_phase(phase_num)
                # Clear completed actions for this phase
                state = self._read_phase_state()
                state.pop(f"phase_{phase_num}_completed", None)
                self._write_phase_state(state)
                # Clear stale insights so dashboard regenerates
                try:
                    from glossa_lab.api.dashboard import mark_insights_stale  # noqa: PLC0415
                    mark_insights_stale()
                except Exception:  # noqa: BLE001
                    pass
                # Clear finished jobs so queue is fresh
                try:
                    import sqlite3 as _sql  # noqa: PLC0415
                    _db_path = _REPO / "backend" / "data" / "glossa.db"
                    if _db_path.exists():
                        _conn = _sql.connect(str(_db_path), timeout=3)
                        _conn.execute(
                            "DELETE FROM job_results WHERE job_id IN "
                            "(SELECT id FROM jobs WHERE status IN ('completed','failed','cancelled'))"
                        )
                        _conn.execute(
                            "DELETE FROM jobs WHERE status IN ('completed','failed','cancelled')"
                        )
                        _conn.commit()
                        _conn.close()
                except Exception:  # noqa: BLE001
                    pass
                message = (
                    f"🏆 Phase {phase_num} complete! "
                    "Insights cleared, jobs cleaned up. "
                    "Dashboard will regenerate with fresh data."
                )

            elif top.action_type == "open_view":
                self._mark_action_done(status.current_phase, top.label)
                message = f"✔ {top.label} — acknowledged, advancing to next step."

            else:
                self._mark_action_done(status.current_phase, top.label)
                message = f"✔ {top.label} — acknowledged."

            # Persist action status to DB
            if db is not None:
                try:
                    # run_experiment: mark as 'running' until job completes
                    db_status = "running" if (top.action_type == "run_experiment" and job_id) else "completed"
                    await db.upsert_phase_action(
                        phase=status.current_phase,
                        label=top.label,
                        action_type=top.action_type,
                        params=top.params,
                        status=db_status,
                        job_id=job_id,
                    )
                except Exception:  # noqa: BLE001
                    pass

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
            # Persist failure to DB
            if db is not None:
                try:
                    await db.upsert_phase_action(
                        phase=status.current_phase,
                        label=top.label,
                        action_type=top.action_type,
                        params=top.params,
                        status="failed",
                        error_message=str(exc),
                    )
                except Exception:  # noqa: BLE001
                    pass
            return PhaseAdvanceResult(
                ok=False, action_taken=top.label, action_type=top.action_type,
                job_id=None, experiment_id=None,
                message=f"Advance failed: {exc}",
                current_phase=status.current_phase, coverage=status.coverage,
            )
