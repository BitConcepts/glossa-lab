"""Lightweight in-memory event bus + SSE endpoint.

Provides a simple pub/sub mechanism for broadcasting real-time events
to frontend subscribers via Server-Sent Events.

Usage (emitting events from other modules):
    from glossa_lab.api.events import emit_event
    await emit_event("insight_trigger", reason="loop_complete")

Usage (subscribing from frontend):
    const es = new EventSource("/api/v1/events/stream");
    es.onmessage = (e) => { const data = JSON.parse(e.data); ... };
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/v1/events", tags=["events"])
_log = logging.getLogger("glossa_lab.api.events")

# ── In-memory event bus ──────────────────────────────────────────────────
# Maps event_name → set of asyncio.Queue subscribers.
# Each subscriber gets its own queue; emit fans out to all of them.
_subscribers: dict[str, set[asyncio.Queue]] = {}
_ALL = "__all__"  # wildcard channel — receives every event


def _ensure_channel(channel: str) -> set[asyncio.Queue]:
    if channel not in _subscribers:
        _subscribers[channel] = set()
    return _subscribers[channel]


async def emit_event(event_type: str, **kwargs: Any) -> None:
    """Broadcast an event to all subscribers of *event_type* and the wildcard channel."""
    payload = {
        "type": event_type,
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        **kwargs,
    }
    _log.debug("Event emitted: %s", event_type)
    for channel in (event_type, _ALL):
        for q in list(_ensure_channel(channel)):
            try:
                q.put_nowait(payload)
            except asyncio.QueueFull:
                pass  # drop if subscriber is slow


def subscribe(channel: str = _ALL, maxsize: int = 64) -> asyncio.Queue:
    """Create a new subscription queue for the given channel."""
    q: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
    _ensure_channel(channel).add(q)
    return q


def unsubscribe(q: asyncio.Queue, channel: str = _ALL) -> None:
    """Remove a subscription queue."""
    subs = _subscribers.get(channel)
    if subs:
        subs.discard(q)


# ── SSE endpoint ─────────────────────────────────────────────────────────

@router.get("/stream")
async def event_stream() -> StreamingResponse:
    """SSE endpoint — streams all events to the client with 30 s keep-alive."""

    async def _generate():
        q = subscribe(_ALL)
        try:
            while True:
                try:
                    payload = await asyncio.wait_for(q.get(), timeout=30.0)
                    yield f"data: {json.dumps(payload)}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive comment so proxies don't close the connection
                    yield ": keep-alive\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            unsubscribe(q, _ALL)

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
