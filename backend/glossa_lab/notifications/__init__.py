"""Email notification subsystem.

Three trigger surfaces feed into a single :class:`Notifier`:

* **Discovery digest** — :mod:`glossa_lab.discovery.notify` gathers items where
  ``notified_at IS NULL`` and confidence >= ``min_confidence``, calls the
  notifier, and stamps ``notified_at`` so each item is emailed at most once.
* **Study completion** — :func:`notify_study_complete` is invoked by the
  studies SSE runner when ``notify=True`` was passed to ``POST /studies/{id}/run``.
* **Experiment-graph completion** — :func:`notify_experiment_complete` is the
  matching hook on the experiment-graph runner.

The notifier is **silent-by-default** — if SMTP host or from address are
unset (or the SQLite recipient table is empty), the calls become a no-op
that logs a warning. This keeps any feature that opts into notifications
from breaking when the SMTP creds aren't yet configured.

SMTP credentials live in the same ``.keys.json`` settings store as every
other API key (see :mod:`glossa_lab.api.settings`). The keys are:

* ``smtp_host``      — required
* ``smtp_port``      — defaults to ``587``
* ``smtp_username``  — optional
* ``smtp_password``  — optional
* ``smtp_from``      — required (RFC 5321 ``MAIL FROM``)
* ``smtp_use_tls``   — ``"1"``/``"true"`` enables STARTTLS (default ``True``)
"""

from __future__ import annotations

from glossa_lab.notifications.smtp import (
    Notifier,
    NotifierConfig,
    SendResult,
    get_notifier,
)
from glossa_lab.notifications.templates import (
    format_discovery_digest,
    format_experiment_complete,
    format_study_complete,
    format_test,
)

__all__ = [
    "Notifier",
    "NotifierConfig",
    "SendResult",
    "get_notifier",
    "format_discovery_digest",
    "format_experiment_complete",
    "format_study_complete",
    "format_test",
]
