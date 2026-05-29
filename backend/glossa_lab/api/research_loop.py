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
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

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
    """Save loop state to DB (called from async context — no thread issues)."""
    from glossa_lab.database import get_db
    db = get_db()
    if db is None:
        return
    try:
        await db.save_research_loop_state(
            all_seen=list(loop.all_seen),
            history=loop.history,
        )
    except Exception as exc:  # noqa: BLE001
        _log.warning("Failed to persist research loop state: %s", exc)


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
            )
            job_id = job["id"]
            await db.update_job_status(job_id, "running")
        except Exception as exc:  # noqa: BLE001
            _log.warning("Could not create job for research loop: %s", exc)

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

        # Mark job completed
        if job_id and db:
            try:
                results = loop.get_full_results()
                await db.store_result(
                    job_id=job_id,
                    data=results,
                    created_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
                )
                await db.update_job_status(job_id, "completed")
            except Exception as exc:  # noqa: BLE001
                _log.warning("Could not finalize job: %s", exc)

        # Final persist + completion event
        await _persist(loop)
        yield f"data: {json.dumps({'type': 'complete', 'job_id': job_id, **loop.get_full_results()})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


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
