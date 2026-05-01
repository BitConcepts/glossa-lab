"""Notifier — SMTP send + audit log.

Each call to :meth:`Notifier.send` enumerates active recipients, hands the
message to ``smtplib.SMTP`` (with STARTTLS when configured), and writes one
row per recipient to ``notification_log`` so the UI can surface delivery
status without resorting to the SMTP server's logs.

The class is intentionally tiny — no Jinja, no async SMTP, no reactor — so
the whole subsystem stays understandable. ``smtplib`` is blocking; we run
it in a worker thread via :func:`asyncio.to_thread` so the discovery
scheduler / SSE runners don't stall on the network round-trip.
"""

from __future__ import annotations

import asyncio
import logging
import smtplib
import ssl
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import make_msgid
from typing import Any

from glossa_lab.api.settings import get_key
from glossa_lab.database import get_db
from glossa_lab.notifications.graph import GraphConfig, send_mail as graph_send_mail

_log = logging.getLogger("glossa_lab.notifications")


# ── Config ──────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class NotifierConfig:
    """Resolved SMTP configuration loaded from the settings store / env."""

    host: str = ""
    port: int = 587
    username: str = ""
    password: str = ""
    sender: str = ""
    use_tls: bool = True

    @classmethod
    def from_settings(cls) -> "NotifierConfig":
        host    = (get_key("smtp_host") or "").strip()
        port_s  = (get_key("smtp_port") or "587").strip()
        user    = (get_key("smtp_username") or "").strip()
        pwd     = (get_key("smtp_password") or "")
        sender  = (get_key("smtp_from") or "").strip()
        tls_raw = (get_key("smtp_use_tls") or "1").strip().lower()
        try:
            port = int(port_s) if port_s else 587
        except ValueError:
            port = 587
        return cls(
            host=host,
            port=port,
            username=user,
            password=pwd,
            sender=sender,
            use_tls=tls_raw not in ("0", "false", "no", "off"),
        )

    def is_configured(self) -> bool:
        """Return True once host AND from address are set."""
        return bool(self.host and self.sender)


# ── Result types ────────────────────────────────────────────────────────────


@dataclass(slots=True)
class SendResult:
    recipient: str
    status: str            # "sent" | "failed" | "skipped"
    error: str = ""

    def ok(self) -> bool:
        return self.status == "sent"


@dataclass(slots=True)
class _SendBatch:
    subject: str
    kind: str
    item_count: int
    results: list[SendResult] = field(default_factory=list)


# ── Notifier ────────────────────────────────────────────────────────────────


class Notifier:
    """Wraps mail send + recipient lookup + audit logging.

    The notifier prefers Microsoft Graph (modern OAuth, works with Outlook 365)
    when ``ms_graph_client_id`` AND ``ms_graph_refresh_token`` are configured.
    Otherwise it falls back to plain SMTP via stdlib ``smtplib`` so users on
    Gmail / SendGrid / Mailgun / etc. still work.

    Both transports go through :meth:`_send_one` so audit logging,
    error handling, and recipient enumeration are identical.
    """

    def __init__(self, config: NotifierConfig | None = None) -> None:
        self.config = config or NotifierConfig.from_settings()
        self.graph = GraphConfig.from_settings()

    def is_configured(self) -> bool:
        return self.graph.is_configured() or self.config.is_configured()

    @property
    def transport(self) -> str:
        """Human-readable name of the transport that would be used right now."""
        if self.graph.is_configured():
            return "graph"
        if self.config.is_configured():
            return "smtp"
        return "none"

    async def list_active_recipients(self) -> list[str]:
        """Return active recipient email addresses, deduped."""
        db = get_db()
        if db is None:
            return []
        rows = await db.list_recipients(active_only=True)
        seen: set[str] = set()
        out: list[str] = []
        for r in rows:
            email = (r.get("email") or "").strip().lower()
            if email and email not in seen:
                seen.add(email)
                out.append(email)
        return out

    async def send(
        self,
        *,
        subject: str,
        body_text: str,
        body_html: str = "",
        kind: str = "general",
        item_count: int = 0,
        recipients: list[str] | None = None,
    ) -> _SendBatch:
        """Send one email to every active recipient (or the explicit list).

        Returns a :class:`_SendBatch` summary; per-recipient errors are
        captured in :attr:`SendResult.error` so callers can surface them.
        """
        batch = _SendBatch(subject=subject, kind=kind, item_count=item_count)
        cfg = self.config

        # Resolve recipients
        if recipients is None:
            recipients = await self.list_active_recipients()
        if not recipients:
            _log.info("notifier: no active recipients; skipping send (kind=%s)", kind)
            return batch

        if self.transport == "none":
            _log.warning(
                "notifier: no transport configured (set ms_graph_* for Graph or "
                "smtp_host/smtp_from for SMTP); skipping send for %d recipient(s) (kind=%s)",
                len(recipients), kind,
            )
            for r in recipients:
                batch.results.append(SendResult(recipient=r, status="skipped",
                                                error="no transport configured"))
                await self._log_send(r, batch, status="skipped",
                                      error="no transport configured")
            return batch

        for recipient in recipients:
            try:
                if self.transport == "graph":
                    await self._send_via_graph(
                        recipient=recipient, subject=subject,
                        body_text=body_text, body_html=body_html,
                    )
                else:
                    await asyncio.to_thread(
                        self._smtp_send_one,
                        recipient, subject, body_text, body_html,
                    )
                batch.results.append(SendResult(recipient=recipient, status="sent"))
                await self._log_send(recipient, batch, status="sent")
            except Exception as exc:  # noqa: BLE001 — log every failure; never raise
                err = f"{type(exc).__name__}: {exc}"
                _log.warning("notifier: send to %s failed: %s", recipient, err)
                batch.results.append(SendResult(recipient=recipient, status="failed", error=err))
                await self._log_send(recipient, batch, status="failed", error=err)
        return batch

    # ── Internals ───────────────────────────────────────────────

    async def _send_via_graph(
        self, *, recipient: str, subject: str, body_text: str, body_html: str,
    ) -> None:
        """Hand off to Microsoft Graph; raise on failure.

        The Graph send is synchronous + I/O-bound, so we offload it to a
        worker thread the same way SMTP does. If Microsoft rotated the
        refresh token, we persist the new value via :func:`_save_keys`.
        """
        from glossa_lab.api.settings import _load_keys, _save_keys  # noqa: PLC0415

        sender = self.config.sender or ""
        result = await asyncio.to_thread(
            graph_send_mail, self.graph,
            sender=sender, recipient=recipient,
            subject=subject, body_text=body_text, body_html=body_html,
        )
        # Persist a rotated refresh token so the next send still works.
        if (
            result.rotated_refresh_token
            and result.rotated_refresh_token != self.graph.refresh_token
        ):
            try:
                stored = _load_keys()
                stored["ms_graph_refresh_token"] = result.rotated_refresh_token
                _save_keys(stored)
                self.graph.refresh_token = result.rotated_refresh_token
            except Exception as exc:  # noqa: BLE001
                _log.warning("notifier: failed to persist rotated refresh_token: %s", exc)
        if not result.success:
            raise RuntimeError(result.error or "Graph sendMail failed")

    def _smtp_send_one(
        self, recipient: str, subject: str, body_text: str, body_html: str,
    ) -> None:
        """Build + send one EmailMessage via SMTP."""
        cfg = self.config
        msg = EmailMessage()
        msg["From"] = cfg.sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg["Message-ID"] = make_msgid(domain=(cfg.sender.split("@", 1)[-1] or "glossa-lab"))
        msg.set_content(body_text or " ")
        if body_html:
            msg.add_alternative(body_html, subtype="html")
        ctx = ssl.create_default_context()
        with smtplib.SMTP(cfg.host, cfg.port, timeout=30) as s:
            s.ehlo()
            if cfg.use_tls:
                s.starttls(context=ctx)
                s.ehlo()
            if cfg.username and cfg.password:
                s.login(cfg.username, cfg.password)
            s.send_message(msg, from_addr=cfg.sender, to_addrs=[recipient])

    async def _log_send(
        self, recipient: str, batch: _SendBatch, *, status: str, error: str = "",
    ) -> None:
        db = get_db()
        if db is None:
            return
        try:
            await db.append_notification_log(
                recipient=recipient,
                subject=batch.subject,
                kind=batch.kind,
                sent_at=datetime.now(timezone.utc).isoformat(),
                item_count=batch.item_count,
                status=status,
                error=error,
            )
        except Exception as exc:  # noqa: BLE001
            _log.warning("notifier: failed to write audit row: %s", exc)


# ── Module-level helpers ────────────────────────────────────────────────────


def get_notifier() -> Notifier:
    """Return a fresh :class:`Notifier` (config is reread every call)."""
    return Notifier()


def mask_email(addr: str) -> str:
    """Redacted form for response payloads ('a***@example.com')."""
    if not addr or "@" not in addr:
        return addr
    local, domain = addr.split("@", 1)
    if not local:
        return addr
    return local[0] + "***@" + domain


__all__ = [
    "Notifier",
    "NotifierConfig",
    "SendResult",
    "get_notifier",
    "mask_email",
]
