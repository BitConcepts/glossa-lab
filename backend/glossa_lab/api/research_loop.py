"""Research Loop API — start, status, stop endpoints.

POST /api/v1/research-loop/start   — start the loop (returns SSE stream)
GET  /api/v1/research-loop/status  — current loop state
POST /api/v1/research-loop/stop    — graceful stop at end of current cycle
GET  /api/v1/research-loop/results — full results from last run

Persistence and job tracking happen HERE in the async API layer, not
inside ResearchLoop.run() (which runs in a worker thread).
"""
from __future__ import annotations

import asyncio
import json
import logging
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

_REPO = Path(__file__).resolve().parents[3]

router = APIRouter(prefix="/api/v1/research-loop", tags=["research-loop"])
_log = logging.getLogger("glossa_lab.api.research_loop")

# Singleton loop instance
_loop_instance = None


def _get_loop():
    global _loop_instance
    if _loop_instance is None:
        from glossa_lab.database import get_db
        from glossa_lab.pipelines.research_loop import ResearchLoop
        _loop_instance = ResearchLoop(db=get_db())
    return _loop_instance


async def _persist(loop) -> None:
    """Save loop state to DB (called from async context — no thread issues).

    all_seen is intentionally NOT persisted (per-job only); only history
    is saved so experiment selection state survives across server restarts.
    """
    from glossa_lab.database import get_db
    db = get_db()
    if db is None:
        return
    try:
        await db.save_research_loop_state(
            all_seen=[],
            history=loop.history,
        )
    except Exception as exc:  # noqa: BLE001
        _log.warning("Failed to persist research loop state: %s", exc)


async def _run_foundation_check() -> dict[str, Any]:
    """Run foundation_check.py as a subprocess and return a compact summary.

    Runs in a thread executor so the async event loop is not blocked.
    Timeout: 90 s (covers CSV parsing + JSON reads across all checks).
    Returns a dict with n_ok/n_fail/n_warn/verdict and any failed check labels.
    """
    script = _REPO / "backend" / "scripts" / "foundation_check.py"
    report_path = _REPO / "reports" / "foundation_check_report.json"

    if not script.exists():
        _log.warning("Foundation check skipped — script not found: %s", script)
        return {"skipped": True, "reason": "foundation_check.py not found"}

    def _run() -> subprocess.CompletedProcess:  # type: ignore[type-arg]
        return subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=90,
            cwd=str(_REPO),
        )

    loop = asyncio.get_event_loop()
    try:
        proc = await loop.run_in_executor(None, _run)
        if report_path.exists():
            report = json.loads(report_path.read_text(encoding="utf-8"))
            n_fail = report.get("n_fail", 0)
            result = {
                "n_ok":    report.get("n_ok", 0),
                "n_fail":  n_fail,
                "n_warn":  report.get("n_warn", 0),
                "verdict": report.get("verdict", "UNKNOWN"),
                "failed":  report.get("failed", []),
            }
            _log.info(
                "Foundation check complete: %d ok, %d fail, %d warn",
                result["n_ok"], n_fail, result["n_warn"],
            )
            return result
        # Script ran but didn't write the report
        return {
            "skipped": False,
            "returncode": proc.returncode,
            "stderr": proc.stderr[:400] if proc.stderr else "",
        }
    except subprocess.TimeoutExpired:
        _log.warning("Foundation check timed out after 90 s")
        return {"skipped": True, "reason": "timeout after 90 s"}
    except Exception as exc:  # noqa: BLE001
        _log.warning("Foundation check failed: %s", exc)
        return {"skipped": True, "reason": str(exc)}


@router.post("/start")
async def start_loop(
    max_cycles: int = Query(15, ge=1, le=100),
) -> StreamingResponse:
    """Start the research loop and stream cycle results as SSE events.

    Creates a Job record visible in the Jobs panel. Each cycle yields an
    SSE event and persists state to the DB from the async context.
    """
    from glossa_lab.database import get_db
    from glossa_lab.pipelines.research_loop import ResearchLoop

    global _loop_instance
    _loop_instance = ResearchLoop(max_cycles=max_cycles, db=get_db())
    loop = _loop_instance

    # ── Create a Job record so the run appears in the Jobs panel ────────
    db = get_db()
    job_id: str | None = None
    if db is not None:
        try:
            now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
            job = await db.create_job(
                name=f"Research Loop ({max_cycles} cycles)",
                pipeline="research_loop",
                params={"max_cycles": max_cycles},
                created_at=now,
                initial_status="running",  # skip 'pending' so engine never claims it
            )
            job_id = job["id"]
        except Exception as exc:  # noqa: BLE001
            _log.warning("Could not create job for research loop: %s", exc)

    # Trigger a discovery fetch before the loop if data is stale (> 6 h).
    # This ensures the dashboard feed has fresh items when insight regenerates.
    if db is not None:
        try:
            import time as _t  # noqa: PLC0415
            rows = await db.list_discovery_items(
                topic=None, kind=None, status=None, since=None, limit=1, offset=0)
            last_fetch = 0.0
            if rows:
                ts = rows[0].get("fetched_at", "")
                if ts:
                    from datetime import datetime as _dt, timezone as _tz  # noqa: PLC0415
                    try:
                        last_fetch = _dt.fromisoformat(
                            ts.replace("Z", "+00:00")
                        ).timestamp()
                    except Exception:  # noqa: BLE001
                        pass
            age_hours = (_t.time() - last_fetch) / 3600 if last_fetch else 999
            if age_hours >= 6:
                _log.info("Research loop: fetch is %.1f h stale — triggering discovery fetch",
                          age_hours)
                from glossa_lab.api.discovery import fetch_endpoint, FetchRequest  # noqa: PLC0415
                asyncio.create_task(fetch_endpoint(FetchRequest()))
        except Exception as _exc:  # noqa: BLE001
            _log.info("Research loop pre-fetch check failed (non-critical): %s", _exc)

    async def event_stream():
        """Run the loop in a thread via a queue, persist + stream per cycle."""
        queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()

        def _producer():
            """Runs in worker thread — puts entries on the queue."""
            try:
                for entry in loop.run():
                    queue.put_nowait(entry)
            finally:
                queue.put_nowait(None)  # sentinel

        # Start the producer in a background thread
        task = asyncio.get_event_loop().run_in_executor(None, _producer)

        cycles_done = 0
        while True:
            # Wait for next entry (with timeout so we don't hang forever)
            try:
                entry = await asyncio.wait_for(queue.get(), timeout=120)
            except asyncio.TimeoutError:
                break

            if entry is None:  # producer finished
                break

            cycles_done += 1
            yield f"data: {json.dumps(entry)}\n\n"

            # Persist state from async context (no thread issues)
            await _persist(loop)

            # Update job progress
            if job_id and db:
                try:
                    await db.update_job_status(job_id, "running")
                except Exception:  # noqa: BLE001
                    pass

        # Wait for producer thread to finish
        await task

        # Final persist (before foundation check so history is durable)
        await _persist(loop)

        # ── Foundation check (post-loop integrity gate, pre-synthesis) ──
        foundation_result = await _run_foundation_check()

        # ── Post-loop: synthesize results + propose next actions ────────
        synthesis = _build_synthesis(loop, foundation_result=foundation_result)

        # Mark job completed — synthesis included in stored result so it
        # can be retrieved later via GET /last-run.
        if job_id and db:
            try:
                results = {**loop.get_full_results(), "synthesis": synthesis}
                await db.store_result(
                    job_id=job_id,
                    data=results,
                    created_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
                )
                await db.update_job_status(job_id, "completed")
            except Exception as exc:  # noqa: BLE001
                _log.warning("Could not finalize job: %s", exc)

        # Trigger dashboard insight refresh (best-effort, non-blocking)
        try:
            from glossa_lab.api.dashboard import dashboard_insight  # noqa: PLC0415
            _log.info("Research loop complete — refreshing dashboard insights")
            asyncio.create_task(_refresh_insight_background())
        except Exception:  # noqa: BLE001
            pass

        yield f"data: {json.dumps({'type': 'complete', 'job_id': job_id, **loop.get_full_results(), 'synthesis': synthesis})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _build_synthesis(loop, foundation_result: dict[str, Any] | None = None) -> dict[str, Any]:
    """Generate a post-loop synthesis: what was found, what to do next."""
    from glossa_lab.pipelines.research_loop import INSIGHT_TO_EXPERIMENTS

    history = loop.history or []
    if not history:
        return {"summary": "No cycles completed.", "proposals": [],
                "needle_moved": False, "anchor_candidates": [],
                "candidate_counts": {"total": 0, "staged": 0, "blocked": 0}}

    # Aggregate insight types across all cycles
    all_types: dict[str, int] = {}
    for h in history:
        for t, c in (h.get("insight_types") or {}).items():
            all_types[t] = all_types.get(t, 0) + c

    # Identify experiments that produced new results vs. repeats
    new_verdicts = [h for h in history if h.get("is_new_info")]
    repeat_verdicts = [h for h in history if not h.get("is_new_info")]

    # Find which insight types haven't been explored yet
    explored_types = set(all_types.keys())
    unexplored_types = set(INSIGHT_TO_EXPERIMENTS.keys()) - explored_types

    # Build proposals for next actions
    proposals: list[dict[str, str]] = []

    # 1. Propose experiments for unexplored insight types
    for utype in sorted(unexplored_types):
        top_exp = INSIGHT_TO_EXPERIMENTS[utype][0]
        proposals.append({
            "action": "run_experiment",
            "experiment": top_exp,
            "rationale": f"No {utype} insights found — run {top_exp} to explore this gap.",
        })

    # 2. Propose deeper analysis for the most common insight type
    if all_types:
        top_type = max(all_types, key=all_types.get)  # type: ignore[arg-type]
        candidates = INSIGHT_TO_EXPERIMENTS.get(top_type, [])
        used_exps = {h["experiment"] for h in history}
        unused = [c for c in candidates if c not in used_exps]
        if unused:
            proposals.append({
                "action": "run_experiment",
                "experiment": unused[0],
                "rationale": f"{top_type} was the dominant insight ({all_types[top_type]} total) — run {unused[0]} for deeper analysis.",
            })

    # 3. Always propose a dashboard insight refresh
    proposals.append({
        "action": "refresh_insights",
        "experiment": "",
        "rationale": "Refresh dashboard AI insights to incorporate new mining results.",
    })

    # 4. Surface foundation check failures as top-priority proposals
    if foundation_result and foundation_result.get("n_fail", 0) > 0:
        failed_labels = ", ".join(
            f.split(":")[0].replace("[FAIL] ", "") for f in foundation_result["failed"][:3]
        )
        proposals.insert(0, {
            "action": "fix_foundation",
            "experiment": "",
            "rationale": (
                f"Foundation check: {foundation_result['n_fail']} failure(s) — "
                f"{failed_labels}. Resolve before next research loop run."
            ),
        })

    # Candidate summary from loop
    candidates = getattr(loop, "anchor_candidates", [])
    staged = [c for c in candidates if c.get("review_status") == "staged"]
    blocked = [c for c in candidates if c.get("review_status") == "blocked"]
    needle_moved = len(staged) > 0

    # Add candidate-based proposals
    if staged:
        proposals.insert(0, {
            "action": "review_candidates",
            "experiment": "",
            "rationale": (
                f"{len(staged)} staged anchor candidate(s) ready for review "
                f"in outputs/anchor_staging.json. "
                f"Top: {staged[0]['sign']}={staged[0]['proposed_reading']} "
                f"({staged[0]['evidence_type']})"
            ),
        })
    elif not needle_moved:
        proposals.append({
            "action": "expand_mining",
            "experiment": "",
            "rationale": (
                "No anchor candidates staged. Consider expanding gap queries "
                "or running blocker_sign_context to find staging opportunities."
            ),
        })

    path_signals = getattr(loop, "path_signals", {})

    return {
        "summary": (
            f"{len(history)} cycles completed. "
            f"{sum(h['n_papers'] for h in history)} papers mined, "
            f"{sum(h['n_insights'] for h in history)} insights extracted. "
            f"{len(staged)} candidates staged, {len(blocked)} blocked."
        ),
        "needle_moved": needle_moved,
        "insight_type_totals": all_types,
        "unexplored_types": sorted(unexplored_types),
        "path_signals": path_signals,
        "proposals": proposals,
        "anchor_candidates": candidates[:20],  # top 20 for SSE payload
        "candidate_counts": {
            "total": len(candidates),
            "staged": len(staged),
            "blocked": len(blocked),
        },
        "foundation_check": foundation_result or {"skipped": True, "reason": "not run"},
    }


async def _refresh_insight_background() -> None:
    """Refresh dashboard AI insight after loop completion (fire-and-forget)."""
    try:
        from glossa_lab.api.dashboard import (
            _generate_insight,
            _graph_experiment_ids,
            _recent_discovery,
        )
        from glossa_lab.database import get_db

        db = get_db()
        items = await _recent_discovery(limit=30, days=14)
        studies = []
        if db:
            try:
                studies = await db.list_studies()
            except Exception:  # noqa: BLE001
                pass
        exp_ids = _graph_experiment_ids()
        await _generate_insight(items, studies, exp_ids)
        _log.info("Post-loop dashboard insight refresh completed")
    except Exception as exc:  # noqa: BLE001
        _log.warning("Post-loop insight refresh failed: %s", exc)


@router.get("/status")
async def loop_status() -> dict[str, Any]:
    """Return current loop state."""
    loop = _get_loop()
    return loop.get_status()


@router.post("/stop")
async def stop_loop() -> dict[str, str]:
    """Gracefully stop the loop at end of current cycle."""
    loop = _get_loop()
    loop.stop()
    return {"status": "stopping", "message": "Loop will stop after current cycle completes."}


@router.get("/results")
async def loop_results() -> dict[str, Any]:
    """Return full results from the last run."""
    loop = _get_loop()
    return loop.get_full_results()


_STAGING_JSON = _REPO / "outputs" / "anchor_staging.json"


@router.get("/staging")
async def get_staging() -> dict[str, Any]:
    """Return all anchor candidates from the staging file."""
    if not _STAGING_JSON.exists():
        return {"candidates": [], "counts": {"total": 0, "staged": 0,
                                              "approved": 0, "rejected": 0}}
    try:
        candidates: list[dict] = json.loads(
            _STAGING_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"error": str(exc), "candidates": []}
    counts = {
        "total":    len(candidates),
        "staged":   sum(1 for c in candidates if c.get("review_status") == "staged"),
        "approved": sum(1 for c in candidates if c.get("review_status") == "approved"),
        "rejected": sum(1 for c in candidates if c.get("review_status") == "rejected"),
    }
    return {"candidates": candidates, "counts": counts}


@router.post("/staging/action")
async def staging_action(body: dict[str, Any]) -> dict[str, Any]:
    """Approve, reject, or delete a staged anchor candidate.

    Body: {sign, proposed_reading, action: 'approve'|'reject'|'delete', reason?}

    - approve  → review_status='approved', approved_at timestamp
    - reject   → review_status='rejected', rejected_reason kept for audit
    - delete   → removes entry from file entirely
    """
    sign     = body.get("sign", "")
    reading  = body.get("proposed_reading", "")
    action   = body.get("action", "")
    reason   = body.get("reason", "")

    if not sign or not reading or action not in ("approve", "reject", "delete"):
        return {"ok": False, "error": "sign, proposed_reading, and action are required; "
                                       "action must be approve|reject|delete"}

    if not _STAGING_JSON.exists():
        return {"ok": False, "error": "staging file not found"}

    try:
        candidates: list[dict] = json.loads(
            _STAGING_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"ok": False, "error": f"could not read staging file: {exc}"}

    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    matched = False
    updated: list[dict] = []

    for c in candidates:
        if c.get("sign") == sign and c.get("proposed_reading") == reading:
            matched = True
            if action == "delete":
                continue  # drop from list
            elif action == "approve":
                c["review_status"] = "approved"
                c["approved_at"] = now
            elif action == "reject":
                c["review_status"] = "rejected"
                c["rejected_at"] = now
                c["rejected_reason"] = reason or "user rejected"
        updated.append(c)

    if not matched:
        return {"ok": False, "error": f"candidate {sign}={reading} not found"}

    _STAGING_JSON.write_text(json.dumps(updated, indent=2, ensure_ascii=False),
                             encoding="utf-8")
    remaining = sum(1 for c in updated if c.get("review_status") == "staged")
    _log.info("Staging action %s on %s=%s; %d staged remaining",
              action, sign, reading, remaining)
    return {"ok": True, "action": action, "sign": sign,
            "proposed_reading": reading, "staged_remaining": remaining}


@router.get("/last-run")
async def last_run() -> dict[str, Any]:
    """Return the synthesis + full results from the most recently completed loop job.

    Used by the frontend to display the run-summary dashboard on load,
    even between sessions. Returns {no_runs: true} if no completed job exists.
    """
    from glossa_lab.database import get_db
    db = get_db()
    if db is None:
        return {"error": "database not available"}
    jobs = await db.list_jobs()
    loop_jobs = [
        j for j in jobs
        if j.get("pipeline") == "research_loop" and j.get("status") == "completed"
    ]
    if not loop_jobs:
        return {"no_runs": True}
    latest = loop_jobs[0]  # list_jobs returns DESC by created_at
    result = await db.get_result_for_job(latest["id"])
    if not result:
        return {"job_id": latest["id"], "no_result": True}
    data = result.get("data") or {}
    return {
        "job_id": latest["id"],
        "completed_at": latest.get("updated_at"),
        **data,
    }
