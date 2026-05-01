"""Optional background scheduler for the discovery engine.

Runs ``fetch + mine`` over every configured topic on a fixed cadence (default
24 h). Activated by setting ``GLOSSA_DISCOVERY_DAILY=1`` in the environment;
otherwise the scheduler is a no-op.
"""

from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime, timezone

from glossa_lab.discovery import mine_pending, store
from glossa_lab.discovery.fetchers import run_all
from glossa_lab.discovery.llm import LLMClient
from glossa_lab.discovery.notify import send_pending_digest

_log = logging.getLogger("glossa_lab.discovery.scheduler")


def _interval_seconds() -> float:
    """Read the scheduler interval (hours) from the env, with sane bounds."""
    raw = os.environ.get("GLOSSA_DISCOVERY_INTERVAL_HOURS", "24")
    try:
        hours = float(raw)
    except ValueError:
        hours = 24.0
    return max(1.0, hours) * 3600.0


def _enabled() -> bool:
    return os.environ.get("GLOSSA_DISCOVERY_DAILY", "").lower() in ("1", "true", "yes")


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
    """Start the scheduler if enabled. Returns the task, or None if disabled."""
    if not _enabled():
        _log.info(
            "discovery scheduler not enabled (set GLOSSA_DISCOVERY_DAILY=1 to enable)"
        )
        return None
    interval = _interval_seconds()
    return asyncio.create_task(_scheduler_loop(interval), name="discovery_scheduler")


__all__ = ["run_once", "start_scheduler"]
