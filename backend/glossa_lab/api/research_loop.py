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
import time as _time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Query, Request
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


async def _queue_phase_experiments_on_loop_start(db: Any) -> list[dict[str, Any]]:
    """Auto-queue pending phase run_experiment actions when the research loop starts.

    Reads the current phase's pending experiment actions and queues each as a
    background job so they run alongside (not inside) the research loop.  The
    engine's _sync_phase_action hook marks each action 'completed' when its
    job finishes, so the Phase Guide updates automatically.

    Returns list of {label, exp_id, job_id, phase, phase_label} for the SSE event.
    """
    try:
        from glossa_lab.pipelines.phase_advancer import PhaseAdvancer  # noqa: PLC0415
        from glossa_lab.experiment_graph import queue_graph_experiment  # noqa: PLC0415
        adv = PhaseAdvancer()
        pending = adv.get_pending_experiment_actions()
        queued: list[dict[str, Any]] = []
        for action in pending:
            exp_id = action["experiment_id"]
            label  = action["label"]
            phase  = action["phase"]
            try:
                job = await queue_graph_experiment(exp_id, db=db)
                job_id = job.get("id") if job else None
                if job_id:
                    await db.upsert_phase_action(
                        phase=phase, label=label,
                        action_type="run_experiment",
                        params=action["params"],
                        status="running", job_id=job_id,
                    )
                    queued.append({
                        "label":      label,
                        "exp_id":     exp_id,
                        "job_id":     job_id,
                        "phase":      phase,
                        "phase_label": action["phase_label"],
                    })
                    _log.info("Phase experiment queued with loop: %s (job %s)", exp_id, job_id)
            except Exception as exc:  # noqa: BLE001
                _log.warning("Could not queue phase experiment %s: %s", exp_id, exc)
        return queued
    except Exception as exc:  # noqa: BLE001
        _log.warning("Phase experiment auto-queue failed (non-critical): %s", exc)
        return []


@router.post("/start")
async def start_loop(
    max_cycles: int = Query(15, ge=1, le=100),
) -> StreamingResponse:
    """Start the research loop and stream cycle results as SSE events.

    Creates a Job record visible in the Jobs panel.  Each cycle yields an
    SSE event and persists state to the DB from the async context.

    At start, any pending phase run_experiment actions are automatically
    queued as background jobs so the Phase Guide advances without manual
    intervention.  A phase_experiments_queued SSE event reports which were queued.
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

    # ── Auto-queue pending phase experiments alongside this loop run ─────
    # These run as background jobs; _sync_phase_action in engine.py marks
    # them done when they complete, so Phase Guide advances automatically.
    phase_queued: list[dict[str, Any]] = []
    if db is not None:
        phase_queued = await _queue_phase_experiments_on_loop_start(db)
        if phase_queued:
            _log.info("Queued %d phase experiment(s) alongside loop start", len(phase_queued))

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
                    from datetime import datetime as _dt  # noqa: PLC0415
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
        # ── Emit phase experiment queuing notification immediately ──────
        if phase_queued:
            yield f"data: {json.dumps({'type': 'phase_experiments_queued', 'queued': phase_queued, 'phase': phase_queued[0].get('phase'), 'phase_label': phase_queued[0].get('phase_label')})}\n\n"

        queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
        producer_error: list[Exception] = []  # capture worker thread errors

        def _producer():
            """Runs in worker thread — puts entries on the queue."""
            try:
                for entry in loop.run():
                    queue.put_nowait(entry)
            except Exception as exc:  # noqa: BLE001
                import traceback as _tb
                _log.error("Research loop producer crashed: %s\n%s", exc, _tb.format_exc())
                producer_error.append(exc)
            finally:
                queue.put_nowait(None)  # sentinel

        # Start the producer in a background thread
        task = asyncio.get_event_loop().run_in_executor(None, _producer)

        import time as _time
        t0 = _time.monotonic()
        cycles_done = 0
        last_experiment = ""
        timed_out = False
        while True:
            # Wait for next entry (with timeout so we don't hang forever)
            try:
                entry = await asyncio.wait_for(queue.get(), timeout=360)
            except asyncio.TimeoutError:
                timed_out = True
                break

            if entry is None:  # producer finished
                break

            # Phase E: intermediate SSE events (proposal, build, verify,
            # analysis, timeout, gap_skipped) are streamed directly.
            # Only persist + increment on node_complete / cycle entries.
            entry_type = entry.get("type", "")
            is_cycle = entry_type in ("node_complete", "") and entry.get("cycle")
            last_experiment = entry.get("experiment", last_experiment)
            yield f"data: {json.dumps(entry)}\n\n"

            if is_cycle:
                cycles_done += 1
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

        elapsed = _time.monotonic() - t0

        # If the loop failed or timed out, emit an error SSE event
        if timed_out or producer_error:
            reason = "timeout" if timed_out else str(producer_error[0])
            err_event = {
                "type": "error",
                "reason": reason,
                "cycles_completed": cycles_done,
                "last_experiment": last_experiment,
                "elapsed_seconds": round(elapsed, 1),
            }
            yield f"data: {json.dumps(err_event)}\n\n"
            if job_id and db:
                try:
                    await db.store_result(
                        job_id=job_id,
                        data={
                            "error": reason,
                            "cycles_completed": cycles_done,
                            "last_experiment": last_experiment,
                            "elapsed_seconds": round(elapsed, 1),
                            "traceback": str(producer_error[0]) if producer_error else "",
                        },
                        created_at=datetime.now(UTC).isoformat(
                            timespec="seconds").replace("+00:00", "Z"),
                    )
                    await db.update_job_status(job_id, "failed")
                except Exception:  # noqa: BLE001
                    pass
            return  # skip synthesis on failure

        # ── Post-loop: run entirely in a detached task so client disconnect
        # (GeneratorExit / CancelledError on the SSE stream) can never abort
        # the foundation check, synthesis, or job-completion writes. ─────────
        async def _finalize_post_loop() -> tuple[dict[str, Any], dict[str, Any]]:
            """Persist, foundation check, synthesis, mark job complete.

            Created with asyncio.ensure_future so it runs independently of the
            SSE connection lifetime.  Even if the browser closes the tab while
            the foundation check is running, this task continues until done.
            """
            await _persist(loop)
            fc_result = await _run_foundation_check()
            synth = _build_synthesis(loop, foundation_result=fc_result)
            if job_id and db:
                try:
                    results = {**loop.get_full_results(), "synthesis": synth}
                    await db.store_result(
                        job_id=job_id,
                        data=results,
                        created_at=datetime.now(UTC).isoformat(
                            timespec="seconds").replace("+00:00", "Z"),
                    )
                    await db.update_job_status(job_id, "completed")
                    _log.info("Research loop job %s marked completed", job_id)
                except Exception as _je:  # noqa: BLE001
                    _log.warning("Could not finalize job %s: %s", job_id, _je)
            try:
                asyncio.create_task(_refresh_insight_background())
            except Exception:  # noqa: BLE001
                pass
            _run_anchor_lifecycle(loop, synth)
            try:
                from glossa_lab.api.events import emit_event  # noqa: PLC0415
                asyncio.create_task(emit_event(
                    "insight_trigger", reason="loop_complete",
                    job_id=job_id, cycles=cycles_done))
            except Exception:  # noqa: BLE001
                pass
            try:
                from glossa_lab.api.foundation import mark_dirty  # noqa: PLC0415
                mark_dirty()
            except Exception:  # noqa: BLE001
                pass
            return loop.get_full_results(), synth

        # Start the finalize task BEFORE awaiting it so it survives if the
        # SSE generator is closed while we wait.
        finalize_task: asyncio.Task[tuple[dict[str, Any], dict[str, Any]]] = (
            asyncio.ensure_future(_finalize_post_loop())
        )

        # Wait for synthesis so we can include it in the complete SSE event.
        # asyncio.shield keeps finalize_task alive even if this await is
        # interrupted by a client disconnect.
        synthesis: dict[str, Any]
        full_results: dict[str, Any]
        try:
            full_results, synthesis = await asyncio.wait_for(
                asyncio.shield(finalize_task), timeout=150)
        except asyncio.TimeoutError:
            # Foundation check is slow; finalize_task continues in background.
            _log.info("Post-loop finalize still running — yielding partial complete")
            synthesis = {
                "summary": (
                    f"{cycles_done} cycle(s) complete. "
                    "Synthesis is being finalised in the background — "
                    "reload in a moment to see the full summary."
                ),
                "proposals": [], "needle_moved": cycles_done > 0,
                "anchor_candidates": [],
                "candidate_counts": {"total": 0, "staged": 0, "blocked": 0},
                "insight_type_totals": {}, "unexplored_types": [],
                "foundation_check": {"skipped": True, "reason": "still running"},
            }
            full_results = loop.get_full_results()
        except (asyncio.CancelledError, GeneratorExit):
            # Client disconnected — finalize_task is still running in the
            # background and will mark the job complete when done.
            _log.info("SSE connection closed mid-synthesis; finalize_task continues in background")
            raise  # must re-raise GeneratorExit so Python can close the generator
        except Exception as _fe:  # noqa: BLE001
            _log.warning("Post-loop finalize error: %s", _fe)
            synthesis = {
                "summary": "Loop complete (synthesis error).",
                "proposals": [], "needle_moved": False,
                "anchor_candidates": [],
                "candidate_counts": {"total": 0, "staged": 0, "blocked": 0},
                "insight_type_totals": {}, "unexplored_types": [],
                "foundation_check": {"skipped": True},
            }
            full_results = loop.get_full_results()

        yield f"data: {json.dumps({'type': 'complete', 'job_id': job_id, **full_results, 'synthesis': synthesis})}\n\n"

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

    # 3. Surface foundation check failures
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

    # Phase E: include top findings and proposed next from full results
    full_results = loop.get_full_results()
    top_findings = full_results.get("top_findings", [])[:3]
    proposed_next = full_results.get("proposed_next", [])

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
        "top_findings": top_findings,
        "proposed_next": proposed_next,
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
_ARCHIVE_JSON = _REPO / "outputs" / "anchor_staging_archive.json"


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
    # Compute recommended / statistically_sufficient for each candidate
    for c in candidates:
        score = float(c.get("evidence_score", 0))
        sa_d = c.get("sa_delta")
        # Fallback estimate when real SA comparison data hasn't flowed yet
        if sa_d is None:
            sa_d = round(score * 0.12, 3)
            c["sa_delta"] = sa_d
        else:
            sa_d = float(sa_d)
        c["recommended"] = score >= 0.85 or (sa_d is not None and sa_d > 0.05)
        c["statistically_sufficient"] = score >= 0.7

    counts = {
        "total":    len(candidates),
        "staged":   sum(1 for c in candidates if c.get("review_status") == "staged"),
        "approved": sum(1 for c in candidates if c.get("review_status") == "approved"),
        "rejected": sum(1 for c in candidates if c.get("review_status") == "rejected"),
    }
    # Include archive summary so the frontend can show the promote-to-anchors CTA
    archive_counts: dict[str, int] = {"total": 0, "approved": 0, "verified": 0, "promotable": 0}
    if _ARCHIVE_JSON.exists():
        try:
            archive_raw: list[dict] = json.loads(_ARCHIVE_JSON.read_text(encoding="utf-8"))
            # Read current anchors to determine which archive entries are promotable
            _promoted_signs: set[str] = set()
            try:
                fa_path = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
                if fa_path.exists():
                    fa = json.loads(fa_path.read_text(encoding="utf-8"))
                    _promoted_signs = {
                        sid for sid, info in (fa.get("anchors") or {}).items()
                        if (info.get("confidence") or "").upper() in ("HIGH", "MEDIUM")
                    }
            except Exception:  # noqa: BLE001
                pass
            _seen_signs: set[str] = set()
            promotable = 0
            n_approved = 0
            n_verified = 0
            for c in archive_raw:
                st = (c.get("review_status") or "").lower()
                if st == "approved":
                    n_approved += 1
                elif st == "verified":
                    n_verified += 1
                if st in ("approved", "verified"):
                    sid = c.get("sign") or c.get("sign_id", "")
                    if sid and sid not in _promoted_signs and sid not in _seen_signs:
                        promotable += 1
                        _seen_signs.add(sid)
            archive_counts = {
                "total":     len(archive_raw),
                "approved":  n_approved,
                "verified":  n_verified,
                "promotable": promotable,
            }
        except Exception:  # noqa: BLE001
            pass
    return {"candidates": candidates, "counts": counts, "archive_counts": archive_counts}


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

    if not sign or not reading or action not in ("approve", "reject", "delete", "staged"):
        return {"ok": False, "error": "sign, proposed_reading, and action are required; "
                                       "action must be approve|reject|delete|staged"}

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
            elif action == "staged":
                # Re-stage: move approved/rejected back to staging queue
                c["review_status"] = "staged"
                c.pop("approved_at", None)
                c.pop("rejected_at", None)
                c.pop("rejected_reason", None)
        updated.append(c)

    if not matched:
        return {"ok": False, "error": f"candidate {sign}={reading} not found"}

    _STAGING_JSON.write_text(json.dumps(updated, indent=2, ensure_ascii=False),
                             encoding="utf-8")
    remaining = sum(1 for c in updated if c.get("review_status") == "staged")
    _log.info("Staging action %s on %s=%s; %d staged remaining",
              action, sign, reading, remaining)

    # Mark foundation dirty when anchors change
    if action in ("approve", "reject"):
        try:
            from glossa_lab.api.foundation import mark_dirty  # noqa: PLC0415
            mark_dirty()
        except Exception:  # noqa: BLE001
            pass
        try:
            from glossa_lab.api.signs import invalidate_signs_index  # noqa: PLC0415
            invalidate_signs_index()
        except Exception:  # noqa: BLE001
            pass

    return {"ok": True, "action": action, "sign": sign,
            "proposed_reading": reading, "staged_remaining": remaining}



def _run_anchor_lifecycle(
    loop: Any,
    synthesis: dict[str, Any],
) -> None:
    """Auto-lifecycle for anchor candidates after a loop run.

    - Approved candidates become 'verified' if SA confidence improved,
      stay 'approved' if inconclusive.
    - Verified candidates are auto-archived.
    - Rejected candidates older than 7 days become 'expired' and are archived.
    """
    if not _STAGING_JSON.exists():
        return
    try:
        candidates: list[dict] = json.loads(
            _STAGING_JSON.read_text(encoding="utf-8"))
    except Exception:
        return

    now_iso = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    now_ts = _time.time()
    sa_delta = 0.0

    # Check if SA confidence improved from synthesis foundation_check
    fc = synthesis.get("foundation_check", {})
    if fc and not fc.get("skipped"):
        # Positive signal if no failures
        sa_delta = 0.1 if fc.get("n_fail", 0) == 0 else -0.05

    to_archive: list[dict] = []
    remaining: list[dict] = []
    auto_verified_count = 0

    for c in candidates:
        status = c.get("review_status", "staged")

        # Approved → verified if SA improved
        if status == "approved" and sa_delta > 0:
            c["review_status"] = "verified"
            c["verified_at"] = now_iso
            c["sa_delta"] = sa_delta
            auto_verified_count += 1
            # Auto-archive verified candidates
            c["archived_at"] = now_iso
            c["archived_reason"] = "auto_verified"
            to_archive.append(c)
            continue

        # Rejected for > 7 days → expired and archived
        if status == "rejected":
            rejected_at = c.get("rejected_at", "")
            if rejected_at:
                try:
                    rej_ts = datetime.fromisoformat(
                        rejected_at.replace("Z", "+00:00")
                    ).timestamp()
                    if now_ts - rej_ts > 7 * 86400:
                        c["review_status"] = "expired"
                        c["expired_at"] = now_iso
                        c["archived_at"] = now_iso
                        c["archived_reason"] = "expired_after_7d"
                        to_archive.append(c)
                        continue
                except Exception:  # noqa: BLE001
                    pass

        remaining.append(c)

    if to_archive:
        # Append to archive file
        archive: list[dict] = []
        if _ARCHIVE_JSON.exists():
            try:
                archive = json.loads(_ARCHIVE_JSON.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                pass
        archive.extend(to_archive)
        _ARCHIVE_JSON.write_text(
            json.dumps(archive, indent=2, ensure_ascii=False), encoding="utf-8")

        # Update staging with remaining
        _STAGING_JSON.write_text(
            json.dumps(remaining, indent=2, ensure_ascii=False), encoding="utf-8")

        _log.info(
            "Anchor lifecycle: %d auto-verified and archived, %d remaining",
            auto_verified_count, len(remaining),
        )

        # Emit lifecycle event
        try:
            from glossa_lab.api.events import emit_event  # noqa: PLC0415
            import asyncio as _aio  # noqa: PLC0415
            _aio.create_task(emit_event(
                "lifecycle_advance",
                auto_verified=auto_verified_count,
                archived=len(to_archive),
                remaining=len(remaining),
            ))
        except Exception:  # noqa: BLE001
            pass


@router.post("/staging/archive")
async def archive_staging() -> dict[str, Any]:
    """Archive all approved and rejected candidates from staging.

    Moves them to anchor_staging_archive.json with timestamps.
    Manual override — the auto-lifecycle also archives verified candidates.
    """
    if not _STAGING_JSON.exists():
        return {"ok": False, "error": "staging file not found"}

    try:
        candidates: list[dict] = json.loads(
            _STAGING_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"ok": False, "error": f"could not read staging: {exc}"}

    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    to_archive = []
    remaining = []

    for c in candidates:
        status = c.get("review_status", "staged")
        if status in ("approved", "rejected", "verified", "expired"):
            c["archived_at"] = now
            c.setdefault("archived_reason", "manual_archive")
            to_archive.append(c)
        else:
            remaining.append(c)

    if not to_archive:
        return {"ok": True, "archived": 0, "remaining": len(remaining)}

    # Append to archive
    archive: list[dict] = []
    if _ARCHIVE_JSON.exists():
        try:
            archive = json.loads(_ARCHIVE_JSON.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
    archive.extend(to_archive)
    _ARCHIVE_JSON.write_text(
        json.dumps(archive, indent=2, ensure_ascii=False), encoding="utf-8")

    # Update staging
    _STAGING_JSON.write_text(
        json.dumps(remaining, indent=2, ensure_ascii=False), encoding="utf-8")

    _log.info("Manual archive: %d candidates archived, %d remaining",
              len(to_archive), len(remaining))

    # Auto-archive notice: check if any approved/verified remain in staging
    remaining_actionable = [
        c for c in remaining
        if c.get("review_status") in ("approved", "verified")
    ]
    if not remaining_actionable:
        _log.info("Auto-archive completed: no approved/verified candidates remain in staging")

    # Emit event
    try:
        from glossa_lab.api.events import emit_event  # noqa: PLC0415
        await emit_event("insight_trigger", reason="staging_archived",
                         archived=len(to_archive))
    except Exception:  # noqa: BLE001
        pass

    return {"ok": True, "archived": len(to_archive), "remaining": len(remaining)}


@router.delete("/staging/rejected")
async def prune_rejected_staging() -> dict[str, Any]:
    """Permanently delete all rejected candidates from the staging queue.

    Unlike archive, this removes them from the file entirely (no archive copy).
    Use when rejected items are definitely wrong and should not be re-staged.
    Returns {ok, pruned, remaining_staged}.
    """
    if not _STAGING_JSON.exists():
        return {"ok": True, "pruned": 0, "remaining_staged": 0,
                "message": "No staging file — nothing to prune."}
    try:
        candidates: list[dict] = json.loads(
            _STAGING_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"ok": False, "error": f"could not read staging file: {exc}"}

    pruned = [c for c in candidates if c.get("review_status") == "rejected"]
    remaining = [c for c in candidates if c.get("review_status") != "rejected"]

    if not pruned:
        return {"ok": True, "pruned": 0,
                "remaining_staged": sum(1 for c in remaining if c.get("review_status") == "staged"),
                "message": "No rejected candidates to prune."}

    _STAGING_JSON.write_text(
        json.dumps(remaining, indent=2, ensure_ascii=False), encoding="utf-8")
    _log.info("Prune rejected: %d items removed, %d remaining", len(pruned), len(remaining))

    remaining_staged = sum(1 for c in remaining if c.get("review_status") == "staged")
    return {
        "ok": True,
        "pruned": len(pruned),
        "remaining": len(remaining),
        "remaining_staged": remaining_staged,
        "message": f"{len(pruned)} rejected candidate(s) permanently deleted.",
    }


@router.post("/staging/cleanup")
async def cleanup_staging() -> dict[str, Any]:
    """Archive approved candidates + permanently delete rejected candidates in one step.

    - Approved items  → marked 'verified', moved to archive file
    - Rejected items  → deleted permanently (no archive copy)
    - Staged / blocked → remain in staging for future review

    Use after reviewing a batch: approve the good ones, reject the bad ones,
    then call this once to flush everything and leave only unreviewed items.
    Returns {ok, archived, pruned, remaining_staged}.
    """
    if not _STAGING_JSON.exists():
        return {"ok": True, "archived": 0, "pruned": 0, "remaining_staged": 0,
                "message": "No staging file — nothing to clean up."}
    try:
        candidates: list[dict] = json.loads(
            _STAGING_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"ok": False, "error": f"could not read staging file: {exc}"}

    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    to_archive: list[dict] = []
    remaining: list[dict] = []
    pruned_count = 0

    for c in candidates:
        status = c.get("review_status", "staged")
        if status in ("approved", "verified"):
            c = dict(c)
            c["review_status"] = "verified"
            c["verified_at"] = now
            c["archived_at"] = now
            c["archived_reason"] = "cleanup_action"
            to_archive.append(c)
        elif status == "rejected":
            pruned_count += 1  # dropped — no archive copy
        else:
            remaining.append(c)  # staged / blocked stay

    if to_archive:
        archive: list[dict] = []
        if _ARCHIVE_JSON.exists():
            try:
                archive = json.loads(_ARCHIVE_JSON.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                pass
        archive.extend(to_archive)
        _ARCHIVE_JSON.write_text(
            json.dumps(archive, indent=2, ensure_ascii=False), encoding="utf-8")

    _STAGING_JSON.write_text(
        json.dumps(remaining, indent=2, ensure_ascii=False), encoding="utf-8")

    remaining_staged = sum(1 for c in remaining if c.get("review_status") == "staged")
    _log.info(
        "Staging cleanup: %d archived, %d pruned, %d remaining",
        len(to_archive), pruned_count, len(remaining),
    )

    if to_archive:
        try:
            from glossa_lab.api.foundation import mark_dirty  # noqa: PLC0415
            mark_dirty()
        except Exception:  # noqa: BLE001
            pass
        try:
            from glossa_lab.api.signs import invalidate_signs_index  # noqa: PLC0415
            invalidate_signs_index()
        except Exception:  # noqa: BLE001
            pass

    try:
        from glossa_lab.api.events import emit_event  # noqa: PLC0415
        await emit_event("insight_trigger", reason="staging_cleanup",
                         archived=len(to_archive), pruned=pruned_count)
    except Exception:  # noqa: BLE001
        pass

    return {
        "ok": True,
        "archived": len(to_archive),
        "pruned": pruned_count,
        "remaining_staged": remaining_staged,
        "remaining": len(remaining),
        "message": (
            f"{len(to_archive)} approved archived, {pruned_count} rejected deleted. "
            f"{remaining_staged} item(s) still awaiting review."
        ),
    }


@router.post("/staging/verify-sa")
async def staging_verify_sa() -> dict[str, Any]:
    """Verify approved staging candidates and archive them.

    One-click action for the anchor review queue. Marks all 'approved'
    candidates as 'verified', archives them, and queues the best available
    anchored SA graph experiment so the user can see the result in Jobs.
    Does NOT require a full research loop run.
    """
    from glossa_lab.experiment_graph import (  # noqa: PLC0415
        get_graph_experiment,
        list_graph_experiments,
    )

    if not _STAGING_JSON.exists():
        return {"ok": False, "error": "no staging file found"}

    try:
        candidates: list[dict] = json.loads(
            _STAGING_JSON.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}

    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    approved = [c for c in candidates if c.get("review_status") == "approved"]
    if not approved:
        return {"ok": False, "error": "No approved candidates to verify. Approve some candidates first."}

    # Mark all approved → verified + archive them
    to_archive: list[dict] = []
    remaining: list[dict] = []
    for c in candidates:
        if c.get("review_status") == "approved":
            c["review_status"] = "verified"
            c["verified_at"] = now
            c["archived_at"] = now
            c["archived_reason"] = "manual_verify_sa"
            to_archive.append(c)
        else:
            remaining.append(c)

    archive: list[dict] = []
    if _ARCHIVE_JSON.exists():
        try:
            archive = json.loads(_ARCHIVE_JSON.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
    archive.extend(to_archive)
    _ARCHIVE_JSON.write_text(
        json.dumps(archive, indent=2, ensure_ascii=False), encoding="utf-8")
    _STAGING_JSON.write_text(
        json.dumps(remaining, indent=2, ensure_ascii=False), encoding="utf-8")
    _log.info("verify-sa: %d candidates verified and archived", len(to_archive))

    # Find and queue the best anchored SA experiment
    job_id: str | None = None
    exp_name: str = ""
    PREFERRED_SA_IDS = [
        "indus_cisi_dravidian_vs_sanskrit",
        "indus_cisi_anchored_10",
        "indus_anchor_sweep",
        "indus_cisi_structural",
    ]
    exp_id: str | None = None
    for pid in PREFERRED_SA_IDS:
        if get_graph_experiment(pid) is not None:
            exp_id = pid
            exp_name = get_graph_experiment(pid).get("name", pid)  # type: ignore[union-attr]
            break
    if exp_id is None:
        all_exps = list_graph_experiments()
        for e in all_exps:
            eid = e.get("id", "")
            if any(k in eid.lower() for k in ["anchor", "dravidian", "cisi"]):
                exp_id = eid
                exp_name = e.get("name", eid)
                break

    # SA experiment is NO LONGER queued automatically.
    # The frontend shows a 'Run SA Validation' button after archive so the
    # user can trigger it explicitly when they're ready.
    _log.info("verify-sa: archive complete; SA run deferred to user action")

    # Mark foundation dirty
    try:
        from glossa_lab.api.foundation import mark_dirty  # noqa: PLC0415
        mark_dirty()
    except Exception:  # noqa: BLE001
        pass

    return {
        "ok": True,
        "verified": len(to_archive),
        "archived": len(to_archive),
        "remaining_staged": sum(1 for c in remaining if c.get("review_status") == "staged"),
        "exp_id": exp_id,
        "exp_name": exp_name,
        "job_id": job_id,
        "message": f"{len(to_archive)} candidate(s) verified and archived.",
        "suggested_sa_exp": exp_id,
        "suggested_sa_name": exp_name,
    }


# ── Anchor promotion helpers ────────────────────────────────────────────────

_FA_PATH = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"


def _recalc_corpus_coverage(anchors: dict[str, Any]) -> float:
    """Recalculate corpus token coverage from the Holdat CSV.

    Coverage = fraction of corpus sign tokens with HIGH or MEDIUM anchor.
    Returns 0.0 if corpus is unavailable.
    """
    import csv as _csv  # noqa: PLC0415
    try:
        from glossa_lab.config import get_project_config  # noqa: PLC0415
        holdat_path = get_project_config().corpus_csv_path()
    except Exception:  # noqa: BLE001
        holdat_path = (_REPO
                       / "corpora/downloads/external_repos/holdatllc_indus"
                       / "indus_corpus 2.csv")
    if not holdat_path.exists():
        _log.warning("_recalc_corpus_coverage: corpus CSV not found at %s", holdat_path)
        return 0.0
    hm_signs: set[str] = {
        sid for sid, info in anchors.items()
        if (info.get("confidence") or "").upper() in ("HIGH", "MEDIUM")
    }
    total_tokens = 0
    covered_tokens = 0
    try:
        with open(holdat_path, encoding="utf-8") as f:
            for row in _csv.DictReader(f):
                sign = (row.get("letters") or "").strip()
                if sign:
                    total_tokens += 1
                    if sign in hm_signs:
                        covered_tokens += 1
    except Exception as exc:  # noqa: BLE001
        _log.warning("_recalc_corpus_coverage: CSV read error: %s", exc)
        return 0.0
    if total_tokens == 0:
        return 0.0
    coverage = round(covered_tokens / total_tokens, 4)
    _log.info("Coverage recalc: %d/%d tokens covered = %.2f%%",
              covered_tokens, total_tokens, coverage * 100)
    return coverage


@router.post("/staging/promote")
async def promote_to_anchors(request: Request) -> dict[str, Any]:
    """Promote verified/approved archive candidates to INDUS_FINAL_ANCHORS.json.

    Reads anchor_staging_archive.json, deduplicates by sign ID (highest
    evidence_score wins; 'verified' beats 'approved' for equal scores), and
    promotes entries whose signs do not already have a HIGH or MEDIUM anchor.

    Confidence mapping:
      - review_status == 'verified' OR evidence_score >= 0.8 → MEDIUM
      - otherwise                                             → LOW

    After writing, recalculates corpus_token_coverage and invalidates the
    in-memory signs index and foundation check dirty flag.

    Body (optional JSON):
      dry_run (bool, default False) — return stats without modifying files.

    Returns:
      {ok, dry_run, promoted, skipped, total_anchors,
       prev_coverage, new_coverage, promotable}
    """
    try:
        body: dict[str, Any] = await request.json()
    except Exception:  # noqa: BLE001
        body = {}
    dry_run: bool = bool(body.get("dry_run", False))

    if not _ARCHIVE_JSON.exists():
        return {"ok": True, "promoted": 0, "skipped": 0,
                "promotable": 0, "message": "Archive file not found."}

    # ── 1. Read archive ───────────────────────────────────────────────────
    try:
        archive: list[dict] = json.loads(_ARCHIVE_JSON.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"Could not read archive: {exc}"}

    # ── 2. Read INDUS_FINAL_ANCHORS.json ──────────────────────────────────
    if not _FA_PATH.exists():
        return {"ok": False, "error": "INDUS_FINAL_ANCHORS.json not found"}
    try:
        fa_data: dict[str, Any] = json.loads(_FA_PATH.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"Could not read anchors file: {exc}"}

    current_anchors: dict[str, Any] = dict(fa_data.get("anchors") or {})
    prev_coverage: float = float(fa_data.get("corpus_token_coverage", 0.0) or 0.0)

    # Existing HIGH/MEDIUM signs that should not be overwritten
    hm_signs: set[str] = {
        sid for sid, info in current_anchors.items()
        if (info.get("confidence") or "").upper() in ("HIGH", "MEDIUM")
    }

    # ── 3. Deduplicate archive — best entry per sign ───────────────────────
    # Priority: verified > approved; then higher evidence_score wins.
    best_per_sign: dict[str, dict] = {}
    for c in archive:
        st = (c.get("review_status") or "").lower()
        if st not in ("approved", "verified"):
            continue
        sid = c.get("sign") or c.get("sign_id", "")
        if not sid:
            continue
        score = float(c.get("evidence_score", 0) or 0)
        st_rank = 1 if st == "verified" else 0  # verified > approved
        prev = best_per_sign.get(sid)
        if prev is None:
            best_per_sign[sid] = c
        else:
            prev_score = float(prev.get("evidence_score", 0) or 0)
            prev_rank = 1 if (prev.get("review_status") or "").lower() == "verified" else 0
            if (st_rank, score) > (prev_rank, prev_score):
                best_per_sign[sid] = c

    promotable_count = sum(1 for sid in best_per_sign if sid not in hm_signs)

    # ── 4. Promote ────────────────────────────────────────────────────────
    promoted_signs: list[str] = []
    skipped_signs: list[str] = []
    now_label = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

    for sid, c in best_per_sign.items():
        if sid in hm_signs:
            skipped_signs.append(sid)  # already HIGH/MEDIUM — never downgrade
            continue
        score = float(c.get("evidence_score", 0) or 0)
        st = (c.get("review_status") or "").lower()
        new_conf = "MEDIUM" if (st == "verified" or score >= 0.8) else "LOW"
        reading = c.get("proposed_reading", "")
        basis_parts = [
            f"Promoted from anchor staging archive ({now_label})",
            f"evidence_type={c.get('evidence_type', '')}",
            f"score={score:.2f}",
            f"status={st}",
        ]
        if c.get("dedr_support"):
            basis_parts.append(f"DEDR: {c['dedr_support']}")
        current_anchors[sid] = {
            "reading":    reading,
            "confidence": new_conf,
            "basis":      "; ".join(p for p in basis_parts if p),
            "source":     f"anchor_staging_archive:{c.get('source_experiment', '')}",
        }
        if c.get("dedr_support"):
            current_anchors[sid]["dedr_support"] = c["dedr_support"]
        promoted_signs.append(sid)

    new_coverage = prev_coverage  # default: unchanged if dry_run or coverage calc fails

    if not dry_run and promoted_signs:
        # ── 5. Recalculate coverage ────────────────────────────────────────
        new_coverage = _recalc_corpus_coverage(current_anchors)

        # ── 6. Write updated anchors file ───────────────────────────────────
        fa_data["anchors"] = current_anchors
        fa_data["total"] = len(current_anchors)
        if new_coverage > 0:
            fa_data["corpus_token_coverage"] = new_coverage
        _FA_PATH.write_text(
            json.dumps(fa_data, indent=2, ensure_ascii=False), encoding="utf-8")
        _log.info(
            "promote_to_anchors: wrote %d new anchors; coverage %.4f → %.4f",
            len(promoted_signs), prev_coverage, new_coverage,
        )

        # ── 7a. Mark promoted entries in archive as 'promoted' ───────────────────────────
        # Without this, promoted entries stay as 'approved'/'verified' and the
        # /staging endpoint keeps counting them as promotable (promotable never
        # drops to 0), so the "Promote to Anchors" button re-appears every time.
        promoted_set: set[str] = set(promoted_signs)
        try:
            updated_archive: list[dict] = [
                {**c, "review_status": "promoted",
                 "promoted_at": now_label}
                if (c.get("sign") or c.get("sign_id", "")) in promoted_set
                else c
                for c in archive
            ]
            _ARCHIVE_JSON.write_text(
                json.dumps(updated_archive, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            _log.info("promote_to_anchors: marked %d archive entries as 'promoted'",
                      len(promoted_signs))
        except Exception as _ae:  # noqa: BLE001
            _log.warning("Could not update archive status: %s", _ae)

        # ── 7b. Invalidate caches ─────────────────────────────────────────────────────
        try:
            from glossa_lab.api.signs import invalidate_signs_index  # noqa: PLC0415
            invalidate_signs_index()
        except Exception:  # noqa: BLE001
            pass
        try:
            from glossa_lab.api.foundation import mark_dirty  # noqa: PLC0415
            mark_dirty()
        except Exception:  # noqa: BLE001
            pass
        try:
            from glossa_lab.api.dashboard import mark_insights_stale  # noqa: PLC0415
            mark_insights_stale()
        except Exception:  # noqa: BLE001
            pass

        # ── 8. Mandatory SA validation ───────────────────────────────────
        # Auto-queue SA experiments to validate the newly promoted anchors.
        # This runs as background jobs — results appear in the Jobs panel.
        sa_jobs_queued: list[str] = []
        SA_EXPERIMENTS = [
            "indus_cisi_dravidian_vs_sanskrit",
            "indus_anchor_sweep",
            "indus_kalyanaraman_crossval",
        ]
        try:
            from glossa_lab.database import get_db as _get_db  # noqa: PLC0415
            _db = _get_db()
            if _db is not None:
                for sa_exp_id in SA_EXPERIMENTS:
                    try:
                        _sa_job = await _db.create_job(
                            name=f"SA validation: {sa_exp_id} [post-promote]",
                            pipeline="graph_experiment",
                            params={"experiment_id": sa_exp_id},
                            created_at=datetime.now(UTC).isoformat(
                                timespec="seconds").replace("+00:00", "Z"),
                            initial_status="pending",
                        )
                        sa_jobs_queued.append(_sa_job["id"])
                        _log.info("Post-promote SA queued: %s (job %s)",
                                  sa_exp_id, _sa_job["id"])
                    except Exception as _sae:  # noqa: BLE001
                        _log.warning("Could not queue SA %s: %s", sa_exp_id, _sae)
        except Exception:  # noqa: BLE001
            pass

    cov_delta = round(new_coverage - prev_coverage, 4) if not dry_run else 0.0
    sa_msg = ""
    if not dry_run and promoted_signs and sa_jobs_queued:
        sa_msg = f" SA validation auto-queued ({len(sa_jobs_queued)} job(s))."
    return {
        "ok":           True,
        "dry_run":      dry_run,
        "promoted":     len(promoted_signs),
        "skipped":      len(skipped_signs),
        "promotable":   promotable_count,
        "total_anchors": len(current_anchors),
        "prev_coverage":  round(prev_coverage, 4),
        "new_coverage":   round(new_coverage, 4),
        "coverage_delta": cov_delta,
        "sa_validation_jobs": sa_jobs_queued if not dry_run else [],
        "message": (
            f"{len(promoted_signs)} signs promoted to INDUS_FINAL_ANCHORS.json. "
            f"Coverage: {prev_coverage*100:.1f}% → {new_coverage*100:.1f}% "
            f"(+{cov_delta*100:.1f}%).{sa_msg}"
        ) if not dry_run and promoted_signs else (
            f"Dry run: {len(promoted_signs)} would be promoted, "
            f"{len(skipped_signs)} skipped (already HIGH/MEDIUM)."
        ) if dry_run else "No new signs to promote.",
    }


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
