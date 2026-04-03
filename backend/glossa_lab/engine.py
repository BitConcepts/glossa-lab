"""Pipeline execution engine.

Async background worker that polls for pending jobs, dispatches them
to the correct pipeline, and stores results.
"""

from __future__ import annotations

import asyncio
import logging
import traceback
from datetime import datetime, timezone
from typing import Any

from glossa_lab.database import get_db

logger = logging.getLogger(__name__)

# Pipeline registry — maps pipeline name to callable
_PIPELINES: dict[str, Any] = {}


def register_pipeline(name: str):
    """Decorator to register a pipeline function."""
    def decorator(fn):
        _PIPELINES[name] = fn
        return fn
    return decorator


def get_registered_pipelines() -> list[str]:
    return list(_PIPELINES.keys())


async def _run_job(job: dict[str, Any]) -> dict[str, Any]:
    """Execute a single job and return its result data."""
    pipeline_name = job["pipeline"]
    pipeline_fn = _PIPELINES.get(pipeline_name)
    if pipeline_fn is None:
        raise ValueError(f"Unknown pipeline: {pipeline_name}")

    params = job.get("params", {})
    return await pipeline_fn(params)


async def _process_one() -> bool:
    """Try to claim and process one pending job. Returns True if work was done."""
    db = get_db()
    if db is None:
        return False

    job = await db.claim_pending_job()
    if job is None:
        return False

    job_id = job["id"]
    logger.info("Running job %s (pipeline=%s)", job_id, job["pipeline"])

    try:
        result_data = await _run_job(job)
        now = datetime.now(timezone.utc).isoformat()
        await db.store_result(job_id=job_id, data=result_data, created_at=now)
        await db.update_job_status(job_id, "completed")
        logger.info("Job %s completed", job_id)
    except Exception as exc:
        logger.error("Job %s failed: %s", job_id, exc)
        await db.store_result(
            job_id=job_id,
            data={"error": str(exc), "traceback": traceback.format_exc()},
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        await db.update_job_status(job_id, "failed")

    return True


async def run_engine_loop(*, poll_interval: float = 2.0) -> None:
    """Main engine loop — runs until cancelled."""
    logger.info("Pipeline engine started (poll_interval=%.1fs)", poll_interval)
    # Import pipelines so they register themselves
    _ensure_pipelines_loaded()

    try:
        while True:
            did_work = await _process_one()
            if not did_work:
                await asyncio.sleep(poll_interval)
    except asyncio.CancelledError:
        logger.info("Pipeline engine stopped")


async def run_once() -> bool:
    """Process one job (for testing). Returns True if a job was processed."""
    _ensure_pipelines_loaded()
    return await _process_one()


def _ensure_pipelines_loaded() -> None:
    """Import pipeline modules to trigger registration."""
    if not _PIPELINES:
        import glossa_lab.pipelines.block_entropy  # noqa: F401,I001
        import glossa_lab.pipelines.char_freq  # noqa: F401
        import glossa_lab.pipelines.cooccurrence  # noqa: F401
        import glossa_lab.pipelines.decipher  # noqa: F401
        import glossa_lab.pipelines.distributional_decipherment  # noqa: F401
        import glossa_lab.pipelines.hypothesis  # noqa: F401
        import glossa_lab.pipelines.kandles  # noqa: F401
        import glossa_lab.pipelines.logosyllabic  # noqa: F401
        import glossa_lab.pipelines.numerals  # noqa: F401
        import glossa_lab.pipelines.paradigm  # noqa: F401
        import glossa_lab.pipelines.sign_cluster  # noqa: F401
        import glossa_lab.pipelines.word_structure_hypothesis  # noqa: F401
