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

    HARD BLOCK: automatic email sends are disabled.
    Emails may ONLY be sent via an explicit manual action in the Settings UI
    (the 'Send test' button).  The scheduler calls this function but it will
    always no-op so it never fires emails without the user's direct intent.
    """
    # ── STRICT RULE: no automatic email sends ────────────────────────────────
    # This function is called automatically by the discovery scheduler on every
    # 24h tick.  Sending emails without the user explicitly clicking a button
    # is not allowed.  Any code path that reaches here automatically will
    # silently no-op.  To re-enable auto-digest in the future, remove this
    # early return AND add a user-facing opt-in toggle in the Notifications UI.
    _log.debug("send_pending_digest: auto-send is disabled; returning no-op")
    return _summary(reason="auto-send disabled — use Settings > Notifications > Send test")


def _summary(*, reason: str, item_count: int = 0) -> dict[str, Any]:
    return {
        "sent": 0, "skipped": 0, "failed": 0,
        "item_count": item_count,
        "subject": "",
        "reason": reason,
        "recipients": [],
    }


__all__ = ["send_pending_digest"]
