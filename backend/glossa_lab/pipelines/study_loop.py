"""Autonomous Study Loop — thin wrapper around ResearchLoop.

Adds state capture (before/after), narrative generation, and session
persistence so the UI can display a human-readable summary of each
autonomous run.

H11 compliance: ResearchLoop already caps iterations via ``max_cycles``.
No new unbounded loops are introduced.
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, AsyncGenerator

_log = logging.getLogger("glossa_lab.pipelines.study_loop")

_REPO = Path(__file__).resolve().parents[3]
_ANCHORS_JSON = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_STAGING_JSON = _REPO / "outputs" / "anchor_staging.json"
_SESSIONS_JSON = _REPO / "outputs" / "study_loop_sessions.json"

_MAX_SESSIONS = 30


# ---------------------------------------------------------------------------
# State capture
# ---------------------------------------------------------------------------

def _epistemic_entropy(anchors: dict[str, Any]) -> float:
    """Shannon entropy H over confidence distribution (0-1 normalised).

    H = -sum(p * log2(p))  where p is proportion of anchors at each
    confidence tier (HIGH, MEDIUM, LOW, CANDIDATE, unknown).
    Normalised by log2(5) (five tiers) to give a 0-1 value where:
      0 = all anchors at identical confidence (perfectly certain)
      1 = maximally spread across all tiers (maximally uncertain)
    """
    import math  # noqa: PLC0415
    if not anchors:
        return 1.0
    counts: dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "CANDIDATE": 0, "UNKNOWN": 0}
    for v in anchors.values():
        c = (v.get("confidence") or "UNKNOWN").upper()
        counts[c if c in counts else "UNKNOWN"] += 1
    total = len(anchors)
    H = 0.0
    for cnt in counts.values():
        if cnt > 0:
            p = cnt / total
            H -= p * math.log2(p)
    # Normalise: max entropy = log2(5) ≈ 2.322
    return round(min(H / math.log2(5), 1.0), 4)


def capture_state() -> dict[str, Any]:
    """Snapshot current anchor coverage, staging state, and epistemic entropy.

    Epistemic entropy (0-1) measures how uncertain we are across the sign set:
      0 = all signs at the same confidence tier (highly consistent)
      1 = signs spread maximally across all tiers (maximally uncertain)
    High entropy → more aggressive uncertainty-reduction experiments should
    be selected in the next loop iteration.
    """
    anchors: dict[str, Any] = {}
    if _ANCHORS_JSON.exists():
        try:
            data = json.loads(_ANCHORS_JSON.read_text(encoding="utf-8"))
            anchors = data.get("anchors", {})
        except Exception as exc:  # noqa: BLE001
            _log.warning("capture_state: could not read anchors: %s", exc)

    total = len(anchors)
    hm = sum(1 for v in anchors.values()
             if v.get("confidence") in ("HIGH", "MEDIUM"))
    low = sum(1 for v in anchors.values()
              if v.get("confidence") in ("LOW", "CANDIDATE"))
    high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    coverage = round(hm / max(total, 1), 4)
    entropy = _epistemic_entropy(anchors)

    # High-uncertainty signs: LOW confidence with no existing readings
    high_uncertainty = sum(
        1 for v in anchors.values()
        if v.get("confidence") in ("LOW", "CANDIDATE")
        and not (v.get("reading") or v.get("basis"))
    )

    staged_candidates = 0
    blocker_count = 0
    if _STAGING_JSON.exists():
        try:
            staging = json.loads(_STAGING_JSON.read_text(encoding="utf-8"))
            if isinstance(staging, list):
                staged_candidates = len(staging)
                blocker_count = sum(
                    1 for c in staging
                    if c.get("review_status") == "blocked"
                )
        except Exception as exc:  # noqa: BLE001
            _log.warning("capture_state: could not read staging: %s", exc)

    return {
        "coverage": coverage,
        "anchors_total": total,
        "anchors_hm": hm,
        "anchors_high": high,
        "anchors_low": low,
        "staged_candidates": staged_candidates,
        "blocker_count": blocker_count,
        "epistemic_entropy": entropy,
        "high_uncertainty_signs": high_uncertainty,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Narrative generation (no LLM — computed strings only)
# ---------------------------------------------------------------------------

def generate_narrative(
    before: dict[str, Any],
    after: dict[str, Any],
    loop_results: dict[str, Any],
) -> dict[str, Any]:
    """Build an epistemically-framed narrative from the before/after diff.

    All observations are grounded in measurable quantities (coverage, anchor
    counts, entropy, evidence chains) rather than subjective assessments.
    Epistemic entropy is the primary guide: high entropy → uncertainty-
    reduction experiments; low entropy → consolidation and validation.
    """
    cov_before = before.get("coverage", 0)
    cov_after = after.get("coverage", 0)
    cov_delta = round(cov_after - cov_before, 4)

    hm_before = before.get("anchors_hm", 0)
    hm_after = after.get("anchors_hm", 0)
    hm_delta = hm_after - hm_before

    entropy_before = before.get("epistemic_entropy", 0.5)
    entropy_after  = after.get("epistemic_entropy", 0.5)
    entropy_delta  = round(entropy_after - entropy_before, 4)

    unc_before = before.get("high_uncertainty_signs", 0)
    unc_after  = after.get("high_uncertainty_signs", 0)

    staged_before = before.get("staged_candidates", 0)
    staged_after  = after.get("staged_candidates", 0)
    staged_delta  = staged_after - staged_before

    cycles  = loop_results.get("cycles_run", 0)
    papers  = loop_results.get("total_papers_mined", 0)
    insights = loop_results.get("total_insights", 0)

    # ── Where we came from (epistemic baseline) ───────────────────────
    entropy_label = (
        "low (well-constrained)" if entropy_before < 0.35 else
        "moderate" if entropy_before < 0.60 else
        "high (many unknowns)"
    )
    where_we_came_from = (
        f"Coverage: {cov_before:.1%} \u00b7 {hm_before} HIGH+MEDIUM anchors \u00b7 "
        f"{staged_before} staged candidates. "
        f"Epistemic entropy: {entropy_before:.0%} ({entropy_label}), "
        f"{unc_before} signs with no evidence chain."
    )

    what_happened = (
        f"Ran {cycles} research iteration(s), mining {papers} paper(s) "
        f"and extracting {insights} insight(s)."
    )

    # ── What we learned (epistemic deltas) ───────────────────────────
    learned_parts: list[str] = []
    if cov_delta > 0:
        learned_parts.append(f"Coverage ↑ {cov_delta:+.2%} → {cov_after:.1%}.")
    elif cov_delta == 0:
        learned_parts.append(f"Coverage stable at {cov_after:.1%}.")
    else:
        learned_parts.append(f"Coverage ↓ {cov_delta:.2%} → {cov_after:.1%}.")
    if hm_delta > 0:
        learned_parts.append(f"{hm_delta} new HIGH+MEDIUM anchor(s) confirmed.")
    if entropy_delta < -0.02:
        learned_parts.append(
            f"Epistemic entropy reduced by {abs(entropy_delta):.0%} — "
            f"uncertainty decreased."
        )
    elif entropy_delta > 0.02:
        learned_parts.append(
            f"Entropy increased by {entropy_delta:.0%} — "
            f"new unknowns surfaced (expected when staging new candidates)."
        )
    if unc_after < unc_before:
        learned_parts.append(
            f"{unc_before - unc_after} previously-uncharted sign(s) "
            f"now have evidence."
        )
    path_signals = loop_results.get("path_signals", {})
    if path_signals:
        top_signal = max(path_signals, key=path_signals.get)  # type: ignore[arg-type]
        learned_parts.append(
            f"Dominant evidence path: {top_signal} "
            f"({path_signals[top_signal]:.0%} of insights)."
        )
    what_we_learned = " ".join(learned_parts) if learned_parts else "No measurable change this iteration."

    # ── Actions taken ──────────────────────────────────────────────
    actions: list[str] = []
    if staged_delta > 0:
        actions.append(f"Staged {staged_delta} new anchor candidate(s).")
    top_findings = loop_results.get("top_findings", [])
    for finding in top_findings[:3]:
        actions.append(
            f"{finding['experiment']}: {finding['metric']}={finding['value']}"
        )
    if not actions:
        actions.append("No new anchor candidates staged this run.")

    # ── What’s next (epistemic decision) ───────────────────────────
    proposed_next = loop_results.get("proposed_next", [])
    whats_next_parts: list[str] = []
    # Lead with epistemic directive based on current entropy
    if entropy_after >= 0.60:
        whats_next_parts.append(
            f"High uncertainty ({entropy_after:.0%} entropy): "
            "next loop should prioritise blocker-sign and rare-sign "
            "experiments to reduce evidence gaps."
        )
    elif entropy_after < 0.35:
        whats_next_parts.append(
            f"Low uncertainty ({entropy_after:.0%} entropy): "
            "system is well-constrained; focus on validation "
            "and falsification experiments."
        )
    for p in proposed_next[:2]:
        whats_next_parts.append(
            f"{p.get('display_name', p.get('experiment_id', '?'))}: "
            f"{p.get('rationale', '')[:100]}"
        )
    if not whats_next_parts:
        whats_next_parts.append("Continue scheduled study loop.")
    whats_next = " | ".join(whats_next_parts)

    return {
        "where_we_came_from": where_we_came_from,
        "what_happened": what_happened,
        "what_we_learned": what_we_learned,
        "actions_taken": actions,
        "whats_next": whats_next,
        # Pass entropy forward so the UI / email can display it
        "epistemic_entropy_before": entropy_before,
        "epistemic_entropy_after": entropy_after,
    }


# ---------------------------------------------------------------------------
# Session persistence
# ---------------------------------------------------------------------------

def _load_sessions() -> list[dict[str, Any]]:
    if _SESSIONS_JSON.exists():
        try:
            data = json.loads(_SESSIONS_JSON.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except Exception as exc:  # noqa: BLE001
            _log.warning("Could not read session history: %s", exc)
    return []


def _save_sessions(sessions: list[dict[str, Any]]) -> None:
    _SESSIONS_JSON.parent.mkdir(parents=True, exist_ok=True)
    # Cap at _MAX_SESSIONS (keep most recent)
    trimmed = sessions[-_MAX_SESSIONS:]
    _SESSIONS_JSON.write_text(
        json.dumps(trimmed, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main async generator
# ---------------------------------------------------------------------------

async def run_study_loop(
    iterations: int = 15,
    trigger: str = "user",
) -> AsyncGenerator[dict[str, Any], None]:
    """Run a full study loop session, yielding SSE-compatible dicts.

    1. Capture ``before`` state.
    2. Create and iterate a ``ResearchLoop(max_cycles=iterations)``.
    3. Capture ``after`` state, generate narrative, persist session.
    4. Yield final ``study_loop_complete`` event.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415
    from glossa_lab.pipelines.research_loop import ResearchLoop  # noqa: PLC0415

    session_id = uuid.uuid4().hex[:12]
    started_at = datetime.now(timezone.utc).isoformat()

    before = capture_state()
    yield {"type": "study_loop_state", "phase": "before", "state": before}

    loop = ResearchLoop(max_cycles=iterations, db=get_db())

    # Run the synchronous generator in a thread via a queue
    queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()

    def _producer() -> None:
        try:
            for entry in loop.run():
                queue.put_nowait(entry)
        except Exception as exc:  # noqa: BLE001
            _log.error("Study loop producer error: %s", exc)
            queue.put_nowait({"type": "error", "reason": str(exc)})
        finally:
            queue.put_nowait(None)  # sentinel

    task = asyncio.get_event_loop().run_in_executor(None, _producer)

    while True:
        try:
            entry = await asyncio.wait_for(queue.get(), timeout=420)
        except asyncio.TimeoutError:
            _log.warning("Study loop: queue read timed out after 420s")
            yield {"type": "error", "reason": "cycle timeout (420s)"}
            break
        if entry is None:
            break
        yield entry

    await task

    # Post-loop
    completed_at = datetime.now(timezone.utc).isoformat()
    full_results = loop.get_full_results()
    after = capture_state()

    narrative = generate_narrative(before, after, full_results)

    session: dict[str, Any] = {
        "session_id": session_id,
        "started_at": started_at,
        "completed_at": completed_at,
        "iterations": iterations,
        "trigger": trigger,
        "before": before,
        "after": after,
        "narrative": narrative,
        "cycles_run": full_results.get("cycles_run", 0),
        "total_papers": full_results.get("total_papers_mined", 0),
        "total_insights": full_results.get("total_insights", 0),
        "path_signals": full_results.get("path_signals", {}),
    }

    # Persist
    sessions = _load_sessions()
    sessions.append(session)
    _save_sessions(sessions)
    _log.info("Study loop session %s persisted (%d total sessions)",
              session_id, len(sessions))

    yield {"type": "study_loop_complete", "session": session}
