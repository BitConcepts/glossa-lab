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

def capture_state() -> dict[str, Any]:
    """Snapshot current anchor coverage and staging state."""
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
    coverage = round(hm / max(total, 1), 4)

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
        "anchors_low": low,
        "staged_candidates": staged_candidates,
        "blocker_count": blocker_count,
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
    """Build a concise factual narrative from the before/after diff."""
    cov_before = before.get("coverage", 0)
    cov_after = after.get("coverage", 0)
    cov_delta = round(cov_after - cov_before, 4)

    hm_before = before.get("anchors_hm", 0)
    hm_after = after.get("anchors_hm", 0)
    hm_delta = hm_after - hm_before

    staged_before = before.get("staged_candidates", 0)
    staged_after = after.get("staged_candidates", 0)
    staged_delta = staged_after - staged_before

    cycles = loop_results.get("cycles_run", 0)
    papers = loop_results.get("total_papers_mined", 0)
    insights = loop_results.get("total_insights", 0)

    where_we_came_from = (
        f"Coverage was {cov_before:.1%} with {hm_before} HIGH+MEDIUM anchors "
        f"and {staged_before} staged candidates."
    )

    what_happened = (
        f"Ran {cycles} research cycle(s), mining {papers} paper(s) "
        f"and extracting {insights} insight(s)."
    )

    what_we_learned_parts: list[str] = []
    if cov_delta > 0:
        what_we_learned_parts.append(
            f"Coverage increased by {cov_delta:.2%} to {cov_after:.1%}.")
    elif cov_delta == 0:
        what_we_learned_parts.append(
            f"Coverage held steady at {cov_after:.1%}.")
    else:
        what_we_learned_parts.append(
            f"Coverage decreased by {abs(cov_delta):.2%} to {cov_after:.1%}.")
    if hm_delta > 0:
        what_we_learned_parts.append(
            f"{hm_delta} new HIGH+MEDIUM anchor(s) confirmed.")
    path_signals = loop_results.get("path_signals", {})
    if path_signals:
        top_signal = max(path_signals, key=path_signals.get)  # type: ignore[arg-type]
        what_we_learned_parts.append(
            f"Strongest research path: {top_signal} ({path_signals[top_signal]:.1%}).")
    what_we_learned = " ".join(what_we_learned_parts)

    actions: list[str] = []
    if staged_delta > 0:
        actions.append(f"Staged {staged_delta} new anchor candidate(s).")
    top_findings = loop_results.get("top_findings", [])
    for finding in top_findings[:3]:
        actions.append(
            f"{finding['experiment']}: {finding['metric']}="
            f"{finding['value']}"
        )
    proposed_next = loop_results.get("proposed_next", [])
    if not actions:
        actions.append("No new anchor candidates staged this run.")

    whats_next_parts: list[str] = []
    for p in proposed_next[:3]:
        whats_next_parts.append(
            f"{p.get('display_name', p.get('experiment_id', '?'))}: "
            f"{p.get('rationale', '')[:100]}")
    if not whats_next_parts:
        whats_next_parts.append(
            "Continue with the next scheduled study loop run.")
    whats_next = " | ".join(whats_next_parts)

    return {
        "where_we_came_from": where_we_came_from,
        "what_happened": what_happened,
        "what_we_learned": what_we_learned,
        "actions_taken": actions,
        "whats_next": whats_next,
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
