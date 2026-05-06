"""Discovery digest notifier — gather unnotified items, send, stamp.

This module is the glue between the discovery store and the
:class:`glossa_lab.notifications.Notifier`. It is intentionally small:

* :func:`send_pending_digest` reads the unnotified, undismissed items above
  a confidence floor, builds the digest body via
  :func:`format_discovery_digest`, sends to the active recipient list, and
  stamps ``notified_at`` on every successfully-emailed item id (so each
  finding is delivered at most once across recipients).
* If the notifier is not configured *or* there are no recipients *or* there
  are no items above the threshold, the function exits cleanly with a
  summary describing why nothing went out — keeping callers (CLI / scheduler
  / API) free to call it unconditionally.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from glossa_lab.database import get_db
from glossa_lab.notifications import format_discovery_digest, get_notifier

_log = logging.getLogger("glossa_lab.discovery.notify")


async def send_pending_digest(
    *,
    min_confidence: float = 0.5,
    topic: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Send a digest of unnotified discovery items.

    Returns a structured summary suitable for embedding in a Job result or a
    CLI report::

        {
            "sent": int,
            "skipped": int,
            "failed": int,
            "item_count": int,
            "subject": str,
            "reason": str | None,    # set when nothing was sent
        }
    """
    db = get_db()
    if db is None:
        return _summary(reason="database unavailable")

    items = await db.list_unnotified_discovery_items(
        min_confidence=min_confidence, topic=topic, limit=limit,
    )
    if not items:
        return _summary(reason="no unnotified items above min_confidence")

    notifier = get_notifier()
    if not notifier.is_configured():
        # Items remain unnotified so a future configured run can pick them up.
        return _summary(reason="smtp not configured", item_count=len(items))

    recipients = await notifier.list_active_recipients()
    if not recipients:
        return _summary(reason="no active recipients", item_count=len(items))

    subject, body_text, body_html = format_discovery_digest(items)
    batch = await notifier.send(
        subject=subject, body_text=body_text, body_html=body_html,
        kind="discovery_digest", item_count=len(items),
        recipients=recipients,
    )

    # Stamp items as notified only if at least one recipient got the digest.
    any_sent = any(r.ok() for r in batch.results)
    if any_sent:
        notified_at = datetime.now(timezone.utc).isoformat()
        await db.mark_discovery_notified(
            [it["id"] for it in items], notified_at=notified_at,
        )

        # F3: Auto-disclosure — log every successful send as an outbound correspondence.
        for r in batch.results:
            if r.ok():
                try:
                    await db.create_correspondence(
                        direction="outbound",
                        channel="email",
                        to_addr=r.recipient,
                        subject=subject,
                        body=f"Discovery digest with {len(items)} item(s).",
                        date=notified_at[:10],
                        claims_made="Automated discovery digest — no specific claims.",
                        reply_status="closed",
                        created_at=notified_at,
                    )
                except Exception:  # noqa: BLE001
                    _log.debug("Failed to log correspondence for %s", r.recipient)

    sent_n = sum(1 for r in batch.results if r.status == "sent")
    skip_n = sum(1 for r in batch.results if r.status == "skipped")
    fail_n = sum(1 for r in batch.results if r.status == "failed")
    return {
        "sent": sent_n,
        "skipped": skip_n,
        "failed": fail_n,
        "item_count": len(items),
        "subject": subject,
        "reason": None if any_sent else "all recipient sends failed",
        "recipients": [r.recipient for r in batch.results],
    }


def _summary(*, reason: str, item_count: int = 0) -> dict[str, Any]:
    return {
        "sent": 0, "skipped": 0, "failed": 0,
        "item_count": item_count,
        "subject": "",
        "reason": reason,
        "recipients": [],
    }


__all__ = ["send_pending_digest"]
