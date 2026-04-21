"""Pipeline execution engine.

Async background worker that polls for pending jobs, dispatches them
to the correct pipeline, and stores results.
"""

from __future__ import annotations

import ast
import asyncio
import importlib
import logging
import pkgutil
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from glossa_lab.database import get_db

logger = logging.getLogger(__name__)

# Pipeline registry — maps pipeline name to callable
_PIPELINES: dict[str, Any] = {}
_PIPELINE_MODULES_LOADED = False


def register_pipeline(name: str):
    """Decorator to register a pipeline function."""

    def decorator(fn):
        _PIPELINES[name] = fn
        return fn

    return decorator


def get_registered_pipelines() -> list[str]:
    _ensure_pipelines_loaded()
    return sorted(_PIPELINES.keys())


def get_registered_pipeline_info() -> list[dict[str, str]]:
    """Return registered pipelines with module metadata."""
    _ensure_pipelines_loaded()
    return [
        {
            "name": name,
            "module": getattr(fn, "__module__", "unknown"),
        }
        for name, fn in sorted(_PIPELINES.items())
    ]


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


# How long a running job can go without a heartbeat (updated_at) before being
# marked as timed_out.  exp_run jobs update updated_at on every node completion.
_JOB_STALL_TIMEOUT_SECONDS = 600  # 10 minutes — generous for heavy SA runs


async def _stall_watchdog() -> None:
    """Background task: mark stalled running jobs as timed_out.

    A job is considered stalled if its status is 'running' and its updated_at
    has not changed in _JOB_STALL_TIMEOUT_SECONDS seconds.  For exp_run jobs
    the updated_at is touched on every node completion, so this catches
    genuinely frozen jobs (e.g. BeamDecipher on enormous sign inventory).
    """
    while True:
        await asyncio.sleep(60)  # check every minute
        db = get_db()
        if db is None or db._conn is None:  # noqa: SLF001
            continue
        try:
            cursor = await db._conn.execute(  # noqa: SLF001
                """SELECT id, name FROM jobs WHERE status = 'running'
                   AND (julianday('now') - julianday(updated_at)) * 86400 > ?""",
                (_JOB_STALL_TIMEOUT_SECONDS,),
            )
            stalled = await cursor.fetchall()
            for row in stalled:
                jid, jname = row["id"], row["name"]
                logger.warning(
                    "Job %s ('%s') has stalled (no heartbeat in %ds) — marking timed_out",
                    jid, jname, _JOB_STALL_TIMEOUT_SECONDS,
                )
                await db._conn.execute(  # noqa: SLF001
                    "UPDATE jobs SET status = 'failed', updated_at = datetime('now'), "
                    "params = json_set(params, '$.stall_reason', 'timeout') WHERE id = ?",
                    (jid,),
                )
            if stalled:
                await db._conn.commit()  # noqa: SLF001
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            logger.debug("Stall watchdog error: %s", exc)


async def run_engine_loop(*, poll_interval: float = 2.0) -> None:
    """Main engine loop — runs until cancelled."""
    logger.info("Pipeline engine started (poll_interval=%.1fs)", poll_interval)
    # Import pipelines so they register themselves
    _ensure_pipelines_loaded()

    # Start stall watchdog as a sibling task (cancelled when engine is cancelled)
    watchdog = asyncio.create_task(_stall_watchdog())

    try:
        while True:
            did_work = await _process_one()
            if not did_work:
                await asyncio.sleep(poll_interval)
    except asyncio.CancelledError:
        watchdog.cancel()
        logger.info("Pipeline engine stopped")


async def run_once() -> bool:
    """Process one job (for testing). Returns True if a job was processed."""
    _ensure_pipelines_loaded()
    return await _process_one()


def _ensure_pipelines_loaded() -> None:
    """Import pipeline modules to trigger registration."""
    global _PIPELINE_MODULES_LOADED  # noqa: PLW0603
    if _PIPELINE_MODULES_LOADED:
        return

    import glossa_lab.pipelines as pipeline_package

    for module_name in _discover_pipeline_modules(pipeline_package.__path__[0]):
        importlib.import_module(f"{pipeline_package.__name__}.{module_name}")

    _PIPELINE_MODULES_LOADED = True


def _discover_pipeline_modules(package_dir: str) -> list[str]:
    """Find pipeline modules by scanning for register_pipeline decorators."""
    discovered: list[str] = []
    package_path = Path(package_dir)
    for module_info in pkgutil.iter_modules([str(package_path)]):
        if module_info.name.startswith("_"):
            continue
        module_path = package_path / f"{module_info.name}.py"
        if module_path.exists() and _module_registers_pipeline(module_path):
            discovered.append(module_info.name)
    return sorted(discovered)


def _module_registers_pipeline(module_path: Path) -> bool:
    """Return True if the module contains a register_pipeline call."""
    try:
        module_ast = ast.parse(module_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return False

    for node in ast.walk(module_ast):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "register_pipeline":
            return True
        if isinstance(node.func, ast.Attribute) and node.func.attr == "register_pipeline":
            return True
    return False
