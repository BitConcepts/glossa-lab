"""Optional background scheduler for the discovery engine.

Runs ``fetch + mine + digest`` over every configured topic on a fixed cadence
(default 24 h). Two ways to enable it:

* Environment: ``GLOSSA_DISCOVERY_DAILY=1`` — picked up at lifespan startup.
* Persistent setting: ``discovery_daily=1`` in ``.keys.json`` — toggled from
  the Notifications panel UI; honoured at startup AND can be flipped at
  runtime via :func:`enable_at_runtime` / :func:`disable_at_runtime`.

The scheduler module exposes a single in-process task. ``start_scheduler``
is safe to call when one is already running (it returns the existing task).
"""

from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime, timezone

from glossa_lab.api.settings import _load_keys, _save_keys, get_key
from glossa_lab.discovery import mine_pending, store
from glossa_lab.discovery.fetchers import run_all
from glossa_lab.discovery.llm import LLMClient
from glossa_lab.discovery.notify import send_pending_digest

_log = logging.getLogger("glossa_lab.discovery.scheduler")

# Module-level reference to the running task so HTTP endpoints can stop /
# restart the scheduler without re-importing or re-instantiating.
_running_task: asyncio.Task | None = None
_running_lock = asyncio.Lock()


def _interval_seconds() -> float:
    """Read the scheduler interval (hours) from env or settings, with sane bounds."""
    # Settings store wins when present; env is the fallback for legacy installs.
    setting_val = (get_key("discovery_interval_hours") or "").strip()
    raw = setting_val or os.environ.get("GLOSSA_DISCOVERY_INTERVAL_HOURS", "24")
    try:
        hours = float(raw)
    except ValueError:
        hours = 24.0
    return max(1.0, hours) * 3600.0


def _enabled() -> bool:
    """True iff env *or* persistent setting opts the scheduler in."""
    if os.environ.get("GLOSSA_DISCOVERY_DAILY", "").lower() in ("1", "true", "yes"):
        return True
    val = (get_key("discovery_daily") or "").strip().lower()
    return val in ("1", "true", "yes", "on")


def is_running() -> bool:
    """True iff the in-process scheduler task is alive."""
    return _running_task is not None and not _running_task.done()


async def run_once() -> dict[str, object]:
    """Fetch every topic with every configured source, mine, then notify."""
    started = datetime.now(timezone.utc).isoformat()
    fetch_summary = await run_all()
    client = LLMClient()
    mine_summary: dict[str, object] = {}
    if client.configured_providers():
        mine_summary = await mine_pending(client=client, limit=50)
    else:
        mine_summary = {"skipped": "no LLM provider configured"}
    # Always attempt the digest; the notifier silently no-ops if SMTP is
    # unconfigured or the recipient list is empty, so this is safe to call
    # unconditionally on every tick.
    notify_summary = await send_pending_digest(min_confidence=0.5)
    finished = datetime.now(timezone.utc).isoformat()
    return {
        "started_at": started,
        "finished_at": finished,
        "fetch": fetch_summary,
        "mine": mine_summary,
        "notify": notify_summary,
    }


async def _scheduler_loop(interval: float) -> None:
    """Run :func:`run_once` every *interval* seconds until the task is cancelled."""
    _log.info("discovery scheduler started (interval=%.0fs)", interval)
    while True:
        try:
            summary = await run_once()
            _log.info(
                "discovery scheduler tick: fetched=%s new=%s classified=%s notified=%s",
                summary.get("fetch", {}).get("fetched"),
                summary.get("fetch", {}).get("new"),
                summary.get("mine", {}).get("classified"),
                summary.get("notify", {}).get("sent"),
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 — never let the loop die
            _log.warning("discovery scheduler tick failed: %s", exc)
        try:
            await asyncio.sleep(interval)
        except asyncio.CancelledError:
            raise


def start_scheduler() -> asyncio.Task | None:
    """Start the scheduler if enabled. Returns the task, or None if disabled.

    Safe to call multiple times — if a task is already running, the existing
    one is returned. This makes the lifespan + runtime-toggle paths converge.
    """
    global _running_task  # noqa: PLW0603
    if not _enabled():
        _log.info(
            "discovery scheduler not enabled (set GLOSSA_DISCOVERY_DAILY=1 "
            "or toggle 'Auto-start discovery' in Settings)"
        )
        return None
    if _running_task is not None and not _running_task.done():
        return _running_task
    interval = _interval_seconds()
    _running_task = asyncio.create_task(
        _scheduler_loop(interval), name="discovery_scheduler",
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
    _log.info("discovery scheduler stopped")
    return True


def set_persistent_enabled(enabled: bool) -> None:
    """Persist the auto-start preference to ``.keys.json``.

    Sibling :func:`start_scheduler` / :func:`stop_scheduler` actually start /
    stop the in-process task; this only updates the *next-startup* policy.
    """
    stored = _load_keys()
    if enabled:
        stored["discovery_daily"] = "1"
    else:
        stored.pop("discovery_daily", None)
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
    "run_once",
    "start_scheduler",
    "stop_scheduler",
    "is_running",
    "enable_at_runtime",
    "disable_at_runtime",
    "set_persistent_enabled",
]
