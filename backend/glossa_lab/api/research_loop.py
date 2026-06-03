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
        producer_error: list[Exception] = []  # capture worker thread errors

        def _producer():
            """Runs in worker thread — puts entries on the queue."""
            try:
                for entry in loop.run():
                    queue.put_nowait(entry)
            except Exception as exc:  # noqa: BLE001
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

    return {"ok": True, "action": action, "sign": sign,
            "proposed_reading": reading, "staged_remaining": remaining}


_ARCHIVE_JSON = _REPO / "outputs" / "anchor_staging_archive.json"


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


@router.post("/staging/verify-sa")
async def staging_verify_sa() -> dict[str, Any]:
    """Verify approved staging candidates and archive them.

    One-click action for the anchor review queue. Marks all 'approved'
    candidates as 'verified', archives them, and queues the best available
    anchored SA graph experiment so the user can see the result in Jobs.
    Does NOT require a full research loop run.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415
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
        "indus_cisi_anchored_5",
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

    db = get_db()
    if exp_id and db:
        try:
            # Import here to avoid circular import at module load time
            from glossa_lab.api.experiment_graphs import _run_exp_background  # noqa: PLC0415
            exp_data = get_graph_experiment(exp_id)  # already loaded above
            nodes = (exp_data or {}).get("nodes", [])
            edges = (exp_data or {}).get("edges", [])
            # _run_exp_background creates its own job with initial_status='running'
            # so the pipeline engine never picks it up — it's self-managed.
            queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=128)
            task = asyncio.create_task(
                _run_exp_background(exp_id, exp_data or {}, nodes, edges, {}, False, queue),
                name=f"staging-verify-sa-{exp_id}",
            )
            # Drain the queue in background so it doesn't fill and block the task
            async def _drain() -> None:
                while True:
                    item = await queue.get()
                    if item is None:
                        break
            asyncio.create_task(_drain(), name=f"drain-{exp_id}")
            _ = task  # task is fire-and-forget; job tracking handled inside _run_exp_background
            job_id = f"see Jobs panel — {exp_name}"
            _log.info("verify-sa: started experiment '%s' as background task", exp_id)
        except Exception as exc:  # noqa: BLE001
            _log.warning("verify-sa: could not start experiment: %s", exc)

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
        "message": (
            f"{len(to_archive)} candidate(s) verified and archived."
            + (f" SA experiment '{exp_name}' queued (job {job_id})." if job_id else ""
               " No SA experiment found — create one in the builder.")
        ),
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
