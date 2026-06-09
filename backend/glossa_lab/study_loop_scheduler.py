"""Optional background scheduler for the autonomous study loop.

Mirrors the pattern in ``glossa_lab.discovery.scheduler`` exactly.

Two ways to enable:

* Environment: ``GLOSSA_STUDY_LOOP_DAILY=1`` — picked up at lifespan startup.
* Persistent setting: ``study_loop_daily=1`` in ``.keys.json`` — toggled from
  the Study Loop panel UI; honoured at startup AND can be flipped at runtime
  via :func:`enable_at_runtime` / :func:`disable_at_runtime`.

H11 compliance: the scheduler loop uses ``asyncio.sleep(interval)`` which
terminates on cancel. No unbounded blocking waits.
H5 compliance: all scheduled behaviour is documented and opt-in (env var or
persistent setting must be explicitly enabled).
"""
from __future__ import annotations

import asyncio
import logging
import os

from glossa_lab.api.settings import _load_keys, _save_keys, get_key

_log = logging.getLogger("glossa_lab.study_loop_scheduler")

# Module-level reference to the running task so HTTP endpoints can stop /
# restart the scheduler without re-importing or re-instantiating.
_running_task: asyncio.Task | None = None
_running_lock = asyncio.Lock()


def _enabled() -> bool:
    """True iff env *or* persistent setting opts the scheduler in."""
    if os.environ.get("GLOSSA_STUDY_LOOP_DAILY", "").lower() in ("1", "true", "yes"):
        return True
    val = (get_key("study_loop_daily") or "").strip().lower()
    return val in ("1", "true", "yes", "on")


def _interval_seconds() -> float:
    """Read the scheduler interval (hours) from env or settings, with sane bounds."""
    setting_val = (get_key("study_loop_interval_hours") or "").strip()
    raw = setting_val or os.environ.get("GLOSSA_STUDY_LOOP_INTERVAL_HOURS", "24")
    try:
        hours = float(raw)
    except ValueError:
        hours = 24.0
    return max(1.0, hours) * 3600.0


def _default_iterations() -> int:
    """Read the default cycle count from env or settings."""
    setting_val = (get_key("study_loop_daily_iterations") or "").strip()
    raw = setting_val or os.environ.get("GLOSSA_STUDY_LOOP_DAILY_ITERATIONS", "15")
    try:
        iterations = int(raw)
    except ValueError:
        iterations = 15
    return max(1, min(100, iterations))


def is_running() -> bool:
    """True iff the in-process scheduler task is alive."""
    return _running_task is not None and not _running_task.done()


async def _scheduler_loop(interval: float) -> None:
    """Run a study loop session every *interval* seconds until cancelled."""
    _log.info("study loop scheduler started (interval=%.0fs)", interval)

    _INITIAL_DELAY = float(
        os.environ.get("GLOSSA_STUDY_LOOP_INITIAL_DELAY", "60")
    )
    if _INITIAL_DELAY > 0:
        _log.info(
            "study loop scheduler: waiting %.0fs before first tick",
            _INITIAL_DELAY,
        )
        await asyncio.sleep(_INITIAL_DELAY)

    while True:
        try:
            from glossa_lab.api.study_loop import (  # noqa: PLC0415
                is_study_loop_running,
                start_study_loop_session,
            )

            if is_study_loop_running():
                _log.info(
                    "study loop scheduler: loop already running — skipping tick"
                )
            else:
                iterations = _default_iterations()
                _log.info(
                    "study loop scheduler: starting session (%d iterations)",
                    iterations,
                )
                await start_study_loop_session(
                    iterations=iterations, trigger="scheduler"
                )
                _log.info("study loop scheduler: session complete")
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 — never let the loop die
            _log.warning("study loop scheduler tick failed: %s", exc)
        try:
            await asyncio.sleep(interval)
        except asyncio.CancelledError:
            raise


def start_scheduler() -> asyncio.Task | None:
    """Start the scheduler if enabled. Returns the task, or None if disabled.

    Safe to call multiple times — if a task is already running, the existing
    one is returned.
    """
    global _running_task  # noqa: PLW0603
    if not _enabled():
        _log.info(
            "study loop scheduler not enabled (set GLOSSA_STUDY_LOOP_DAILY=1 "
            "or toggle 'Auto-start study loop' in Settings)"
        )
        return None
    if _running_task is not None and not _running_task.done():
        return _running_task
    interval = _interval_seconds()
    _running_task = asyncio.create_task(
        _scheduler_loop(interval), name="study_loop_scheduler",
    )
    return _running_task


async def stop_scheduler() -> bool:
    """Cancel the running scheduler task. Returns True if a task was stopped."""
    global _running_task  # noqa: PLW0603
    task = _running_task
    if task is None or task.done():
        _running_task = None
        return False
    task.cancel()
    try:
        await task
    except (asyncio.CancelledError, Exception):  # noqa: BLE001
        pass
    _running_task = None
    _log.info("study loop scheduler stopped")
    return True


def set_persistent_enabled(enabled: bool) -> None:
    """Persist the auto-start preference to ``.keys.json``.

    Sibling :func:`start_scheduler` / :func:`stop_scheduler` actually start /
    stop the in-process task; this only updates the *next-startup* policy.
    """
    stored = _load_keys()
    if enabled:
        stored["study_loop_daily"] = "1"
    else:
        stored.pop("study_loop_daily", None)
    _save_keys(stored)


async def enable_at_runtime() -> bool:
    """Persist auto-start=on AND start the task immediately. True if newly started."""
    set_persistent_enabled(True)
    async with _running_lock:
        was_running = is_running()
        start_scheduler()
        return not was_running


async def disable_at_runtime() -> bool:
    """Persist auto-start=off AND cancel the running task. True if a task was stopped."""
    set_persistent_enabled(False)
    async with _running_lock:
        return await stop_scheduler()


__all__ = [
    "start_scheduler",
    "stop_scheduler",
    "is_running",
    "enable_at_runtime",
    "disable_at_runtime",
    "set_persistent_enabled",
]
