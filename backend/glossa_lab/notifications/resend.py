"""Resend HTTPS API mail transport — zero-server, zero-mailbox sending.

Resend (https://resend.com) is an HTTP-only mail-sending service:
    * sign up with email + password,
    * generate an API key,
    * POST JSON to https://api.resend.com/emails.

No SMTP server. No mailbox. No domain. No DNS records. The user can also
send from the free shared sender ``onboarding@resend.dev`` (3 000 emails /
month, 100 / day, free) without verifying any domain — perfect for getting
notifications working in 30 seconds.

This is preferred over SMTP whenever ``resend_api_key`` is set, because:
    * no provider bans on residential ISPs / port 587,
    * no app-password dance,
    * no Azure / Microsoft 365 admin consent flow,
    * the same backend code path works for every user.

The :class:`Notifier` selects this transport when it sees ``resend_api_key``
configured (after Microsoft Graph but before SMTP, since Graph keeps a
specific Outlook-365 ergonomic and Resend is the universal fallback).
"""

from __future__ import annotations

import json
import logging
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from glossa_lab.api.settings import get_key

_log = logging.getLogger("glossa_lab.notifications.resend")

# Public Resend HTTPS endpoint.
_RESEND_URL = "https://api.resend.com/emails"

# Identifying user-agent for outbound HTTPS requests. Cloudflare's bot-block
# (error 1010) bans ``Python-urllib/*`` outright, so we MUST send a real UA
# or every send comes back as a Cloudflare 403 even though the API key, From,
# and recipient are all valid. The string mirrors the resend-python SDK so
# Cloudflare's allowlist treats us identically to the official client.
_USER_AGENT = "glossa-lab-notifier/1.0 (resend-python-compat)"

# Resend's free shared sender — works without verifying any domain. Anything
# beyond it (e.g. "Glossa Lab <noreply@yourdomain.com>") needs a domain
# verified in the Resend dashboard.
#
# IMPORTANT: when sending from this shared sender, Resend rejects the
# RFC 5322 "Display Name <email>" form and *also* only delivers to the
# email address the Resend account was registered with (the so-called
# "testing" mode). We therefore default to the bare email and let
# :func:`_normalise_sender` strip any display name the user may have
# pasted in the Settings UI when the underlying address is
# ``onboarding@resend.dev``.
DEFAULT_FROM = "onboarding@resend.dev"
SHARED_SENDER_EMAIL = "onboarding@resend.dev"


# ── Errors ──────────────────────────────────────────────────────────────────


class ResendError(RuntimeError):
    """Raised on any non-recoverable Resend API error."""


# ── Config ──────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class ResendConfig:
    api_key: str = ""
    sender: str = ""

    @classmethod
    def from_settings(cls) -> "ResendConfig":
        return cls(
            api_key=(get_key("resend_api_key") or "").strip(),
            sender=(get_key("resend_from") or "").strip() or DEFAULT_FROM,
        )

    def is_configured(self) -> bool:
        # Sender always falls back to onboarding@resend.dev, so a key is enough.
        return bool(self.api_key)


# ── Send ────────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class ResendSendResult:
    success: bool
    message_id: str = ""
    error: str = ""


# Match "Display Name <email@host>" → (display, email). Used to detect when
# the user pasted a friendly-name From while we still need the bare email
# (e.g. for the shared ``onboarding@resend.dev`` sender, which rejects
# display names).
_DISPLAY_NAME_RE = re.compile(r"^\s*(?P<name>.*?)\s*<\s*(?P<email>[^>]+?)\s*>\s*$")


def _split_sender(sender: str) -> tuple[str, str]:
    """Return ``(display_name, bare_email)`` for an RFC-5322-ish ``From``.

    Falls back to ``("", sender.strip())`` when no angle-bracket form is
    detected.
    """
    m = _DISPLAY_NAME_RE.match(sender or "")
    if m:
        return m.group("name"), m.group("email")
    return "", (sender or "").strip()


def _normalise_sender(sender: str) -> str:
    """Return a Resend-acceptable ``from`` value for ``sender``.

    Resend rejects ``Name <onboarding@resend.dev>`` outright — the shared
    sender must be sent as the bare email. For domain-verified senders the
    full display-name form is preserved.
    """
    name, email = _split_sender(sender or DEFAULT_FROM)
    if email.lower() == SHARED_SENDER_EMAIL:
        return SHARED_SENDER_EMAIL
    return f"{name} <{email}>" if name else email


def _explain_403(body: dict, raw: str, sender_email: str) -> str:
    """Build a human-friendly hint for a 403 from Resend.

    Resend returns 403 in two main cases:
      * the API key isn't valid / is for a different account,
      * the account is in *testing mode* (free tier with the shared sender)
        and the recipient isn't the address that was used to sign up.

    We surface Resend's own message when present and add an actionable hint
    when we recognise the testing-mode situation.
    """
    msg = (body.get("message") or body.get("error") or raw or "").strip()
    hint = ""
    if sender_email.lower() == SHARED_SENDER_EMAIL:
        hint = (
            " — Resend's free shared sender (onboarding@resend.dev) only "
            "delivers to the email you registered your Resend account with. "
            "Either send a test to that address, or verify your own domain "
            "in resend.com/domains and set From to noreply@<your-domain>."
        )
    return msg + hint if msg else (f"Forbidden{hint}" if hint else "Forbidden")


def send_mail(
    cfg: ResendConfig,
    *,
    recipient: str,
    subject: str,
    body_text: str,
    body_html: str = "",
) -> ResendSendResult:
    """POST a single email to the Resend API.

    The recipient is one address (the :class:`Notifier` calls us in a loop
    so audit logging stays one-row-per-recipient). At least one of
    ``body_text`` / ``body_html`` must be set; Resend will 422 a payload
    with neither.

    The shape mirrors the official Resend SDK example:

    .. code-block:: python

        resend.Emails.send({
            "from":    "onboarding@resend.dev",
            "to":      "user@example.com",
            "subject": "Hello World",
            "html":    "<p>...</p>",
        })
    """
    if not cfg.api_key:
        return ResendSendResult(success=False, error="resend_api_key not set")

    sender_value = _normalise_sender(cfg.sender or DEFAULT_FROM)
    _, sender_email = _split_sender(sender_value)

    payload: dict = {
        "from": sender_value,
        # Resend accepts either a string or a list of strings; the SDK
        # example uses a string for single-recipient sends, so we match it.
        "to": recipient,
        "subject": subject,
    }
    # Resend rejects payloads that have neither html nor text. Prefer html
    # when supplied (matches the SDK example) and always include the text
    # fallback so non-HTML clients still render something.
    if body_html:
        payload["html"] = body_html
    if body_text:
        payload["text"] = body_text
    if "html" not in payload and "text" not in payload:
        payload["text"] = " "

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        _RESEND_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {cfg.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Cloudflare (which fronts api.resend.com) bans the default
            # ``Python-urllib/3.x`` user-agent under error 1010 — every send
            # then comes back as a 403 with a Cloudflare access-denied JSON
            # payload that looks like a Resend rejection but isn't.
            # Setting a sane identifying UA dodges that ban entirely.
            "User-Agent": _USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            return ResendSendResult(success=True, message_id="")
        return ResendSendResult(
            success=True,
            message_id=str(body.get("id") or ""),
        )
    except urllib.error.HTTPError as exc:
        # Always read the body once and reuse it — calling exc.read() twice
        # returns b"" on the second call and that's exactly the bug that
        # produced the cryptic "HTTP 403: HTTP Error 403: Forbidden".
        try:
            raw = exc.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            raw = ""
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            body = {}
        if exc.code == 403:
            err_msg = _explain_403(body, raw, sender_email)
        else:
            err_msg = (
                body.get("message")
                or body.get("error")
                or (raw.strip() if raw else str(exc))
            )
        _log.warning("resend: HTTP %s sending to %s: %s", exc.code, recipient, err_msg)
        return ResendSendResult(success=False, error=f"HTTP {exc.code}: {err_msg}")
    except urllib.error.URLError as exc:
        return ResendSendResult(success=False, error=f"network error: {exc.reason}")
    except Exception as exc:  # noqa: BLE001
        return ResendSendResult(success=False, error=f"{type(exc).__name__}: {exc}")


__all__ = [
    "DEFAULT_FROM",
    "ResendConfig",
    "ResendError",
    "ResendSendResult",
    "send_mail",
]
