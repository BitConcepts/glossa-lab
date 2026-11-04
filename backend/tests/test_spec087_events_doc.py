"""Spec 087 Stage S5 — events-bus disposition pin (T503).

Claim covered:
  C087-11  The events bus's persistence semantics are stated
           once, and the code matches the statement: exactly one
           documented statement (module docstring, user manual,
           and HelpView, in agreement) declares the bus
           documented-ephemeral under decision D2, and the emit
           path's behaviour matches it.

The statement's core phrases are pinned on all three surfaces so
the fact cannot silently un-document itself, and the behaviour
legs pin the semantics the statement claims: an event emitted
with no live subscriber is not replayed to a later subscriber
(no persistence), and a slow subscriber's full queue drops
events (no delivery guarantee).
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from glossa_lab.api import events

_REPO = Path(__file__).resolve().parents[2]

# The statement's load-bearing phrases. All three surfaces must
# carry them (agreement), in the docstring's own words.
_PHRASES = ("documented-ephemeral", "no delivery guarantee")


def test_docstring_carries_the_d2_statement() -> None:
    doc = events.__doc__ or ""
    for phrase in _PHRASES:
        assert phrase in doc, f"events docstring lost the D2 phrase: {phrase!r}"
    assert "lost" in doc  # an event with no subscriber is lost


def test_manual_carries_the_d2_statement() -> None:
    manual = (_REPO / "docs" / "user-manual.md").read_text(encoding="utf-8")
    for phrase in _PHRASES:
        assert phrase in manual, f"user manual lost the D2 phrase: {phrase!r}"


def test_helpview_carries_the_d2_statement() -> None:
    helpview = (
        _REPO / "frontend" / "src" / "components" / "HelpView.tsx"
    ).read_text(encoding="utf-8")
    for phrase in _PHRASES:
        assert phrase in helpview, f"HelpView lost the D2 phrase: {phrase!r}"


def test_event_emitted_with_no_subscriber_is_not_replayed() -> None:
    async def run() -> None:
        await events.emit_event("spec087_pin_probe", marker="before-subscribe")
        queue = events.subscribe()
        try:
            assert queue.empty(), (
                "an event emitted with no live subscriber was replayed "
                "to a later subscriber — the bus is not ephemeral"
            )
        finally:
            events.unsubscribe(queue)

    asyncio.run(run())


def test_slow_subscriber_drops_events_when_queue_full() -> None:
    async def run() -> None:
        queue = events.subscribe(maxsize=1)
        try:
            for i in range(3):
                await events.emit_event("spec087_pin_probe", marker=i)
            assert queue.qsize() == 1, (
                "a full subscriber queue held more than its bound — "
                "the drop-on-full behaviour the statement claims is gone"
            )
        finally:
            events.unsubscribe(queue)

    asyncio.run(run())
