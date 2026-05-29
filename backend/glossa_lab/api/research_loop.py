"""Research Loop API — start, status, stop endpoints.

POST /api/v1/research-loop/start   — start the loop (returns SSE stream)
GET  /api/v1/research-loop/status  — current loop state
POST /api/v1/research-loop/stop    — graceful stop at end of current cycle
GET  /api/v1/research-loop/results — full results from last run
"""
from __future__ import annotations

import asyncio
import json
import logging
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
        from glossa_lab.pipelines.research_loop import ResearchLoop
        _loop_instance = ResearchLoop()
    return _loop_instance


@router.post("/start")
async def start_loop(
    max_cycles: int = Query(15, ge=1, le=100),
) -> StreamingResponse:
    """Start the research loop and stream cycle results as SSE events."""
    from glossa_lab.pipelines.research_loop import ResearchLoop

    global _loop_instance
    _loop_instance = ResearchLoop(max_cycles=max_cycles)
    loop = _loop_instance

    async def event_stream():
        """Run the loop in a thread and yield SSE events."""
        for entry in await asyncio.to_thread(_run_loop_sync, loop):
            yield f"data: {json.dumps(entry)}\n\n"
        # Final event
        yield f"data: {json.dumps({'type': 'complete', **loop.get_full_results()})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def _run_loop_sync(loop) -> list[dict[str, Any]]:
    """Run the loop synchronously (called from asyncio.to_thread)."""
    results = []
    for entry in loop.run():
        results.append(entry)
    return results


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
