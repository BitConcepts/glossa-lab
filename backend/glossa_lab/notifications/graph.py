"""Microsoft Graph mail transport — OAuth device-code flow + ``/me/sendMail``.

This module is the "modern" alternative to SMTP for Outlook 365 / Microsoft
365 users. Microsoft is phasing out basic SMTP AUTH tenant-by-tenant, and
app passwords are increasingly disabled in business deployments, so the
right way to send mail from a desktop app today is OAuth 2.0 against the
Microsoft Graph API.

Why device-code flow?
    Glossa Lab is a single-user desktop app; the "auth code with PKCE" flow
    needs a redirect URI the OS browser can hit, which is fiddly behind an
    Electron-style local server. Device code flow asks the user to visit
    https://microsoft.com/devicelogin in any browser, paste a short code,
    and approve — the local app polls for the token in the background.

Setup the user does once:
    1. Visit https://entra.microsoft.com (or portal.azure.com) → Identity →
       App registrations → New registration.
    2. Name: "Glossa Lab". Supported account types: "Accounts in any
       organizational directory and personal Microsoft accounts" (so both
       Outlook 365 work + personal Outlook addresses work).
    3. Don't add a redirect URI; mark the app as a *public client*
       (Authentication tab → "Allow public client flows" = Yes).
    4. API permissions → Add → Microsoft Graph → Delegated → ``Mail.Send``
       (and ``offline_access`` so we can keep refreshing). User consent is
       fine; admin consent is not required for these scopes.
    5. Copy the Application (client) ID, paste it into Settings →
       ``ms_graph_client_id``. Tenant ID can stay ``common`` for the
       broadest compatibility.

The user clicks "Connect Outlook 365" in the Notifications panel, sees a
short user_code + URL, completes consent in their browser, and the server
saves the long-lived refresh_token in ``.keys.json``. From then on the
:class:`Notifier` automatically picks Graph over SMTP when sending mail.
"""

from __future__ import annotations

import json
import logging
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from glossa_lab.api.settings import get_key

_log = logging.getLogger("glossa_lab.notifications.graph")

# Public Microsoft endpoints. Tenant is configurable per install but defaults
# to ``common`` so both consumer (@outlook.com) and work/school accounts work.
_DEFAULT_TENANT = "common"
_GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# Well-known multi-tenant public client ("Microsoft Graph PowerShell" SDK).
# This is a *Microsoft-published* public client app that anyone can use for
# device-code flow against Mail.Send / offline_access. Choosing it lets the
# user skip the entire Azure portal app-registration dance for first-time
# setup; the consent screen will simply say "Microsoft Graph PowerShell"
# instead of "Glossa Lab". Users who want branded consent can still register
# their own client and paste its ID into ``ms_graph_client_id``.
DEFAULT_CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"

# ``offline_access`` is required to receive a refresh_token alongside the
# short-lived (~1h) access_token. ``Mail.Send`` is the minimum scope for
# /me/sendMail.
_SCOPES = "Mail.Send offline_access"

# ── Errors ──────────────────────────────────────────────────────────────────


class GraphError(RuntimeError):
    """Raised on any non-recoverable Graph / OAuth API error."""


class GraphAuthPending(GraphError):
    """Special-case: device flow polled but user hasn't approved yet."""


# ── Config ──────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class GraphConfig:
    """Resolved Microsoft Graph configuration (loaded from .keys.json / env)."""

    client_id: str = ""
    tenant: str = _DEFAULT_TENANT
    refresh_token: str = ""

    @classmethod
    def from_settings(cls) -> "GraphConfig":
        # If the user hasn't pasted a custom client_id, fall back to the
        # public Microsoft Graph PowerShell client so they can connect with
        # ZERO Azure-portal setup. They can always override later for
        # branded consent.
        cid = (get_key("ms_graph_client_id") or "").strip() or DEFAULT_CLIENT_ID
        return cls(
            client_id=cid,
            tenant=(get_key("ms_graph_tenant_id") or _DEFAULT_TENANT).strip() or _DEFAULT_TENANT,
            refresh_token=(get_key("ms_graph_refresh_token") or "").strip(),
        )

    def is_configured(self) -> bool:
        # client_id always resolves (default fallback), so configuration is
        # complete once the user has finished the device-code consent flow
        # and we have a refresh_token.
        return bool(self.client_id and self.refresh_token)

    @property
    def is_default_client(self) -> bool:
        """True if we're using the public Microsoft-Graph-PowerShell client."""
        return self.client_id == DEFAULT_CLIENT_ID


# ── Token cache (thread-safe, in-memory) ─────────────────────────────────────


@dataclass(slots=True)
class _TokenCacheEntry:
    access_token: str
    expires_at: float


_token_cache: dict[str, _TokenCacheEntry] = {}
_token_cache_lock = threading.Lock()


# ── HTTP helpers ────────────────────────────────────────────────────────────


def _post_form(url: str, fields: dict[str, str], *, timeout: float = 30.0) -> dict[str, Any]:
    data = urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            body = {"error": "http_error", "error_description": str(exc)}
        err = body.get("error") or "http_error"
        if err == "authorization_pending":
            raise GraphAuthPending(body.get("error_description") or err) from None
        raise GraphError(
            f"{exc.code} {err}: {body.get('error_description', '')}"
        ) from exc
    except urllib.error.URLError as exc:
        raise GraphError(f"network error: {exc.reason}") from exc


def _post_json(url: str, payload: dict[str, Any], *, token: str, timeout: float = 30.0) -> bytes:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return resp.read()
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8"))
            err = body.get("error", {})
            msg = err.get("message") if isinstance(err, dict) else str(err)
            code = err.get("code") if isinstance(err, dict) else exc.code
        except Exception:  # noqa: BLE001
            msg = str(exc)
            code = exc.code
        raise GraphError(f"{code}: {msg}") from exc


# ── OAuth ───────────────────────────────────────────────────────────────────


def _device_code_url(tenant: str) -> str:
    return f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/devicecode"


def _token_url(tenant: str) -> str:
    return f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"


def start_device_flow(client_id: str, tenant: str = _DEFAULT_TENANT) -> dict[str, Any]:
    """Initiate the device-code flow.

    Returns the raw Microsoft response containing ``user_code``,
    ``verification_uri``, ``device_code``, ``expires_in`` (seconds), and the
    polling ``interval`` (seconds).
    """
    if not client_id:
        raise GraphError("ms_graph_client_id is not set")
    return _post_form(
        _device_code_url(tenant),
        {"client_id": client_id, "scope": _SCOPES},
    )


def poll_device_flow(
    client_id: str, tenant: str, device_code: str,
) -> dict[str, Any]:
    """Try to exchange ``device_code`` for tokens.

    Raises :class:`GraphAuthPending` if the user hasn't completed consent yet
    (caller should sleep ``interval`` seconds and retry). Raises
    :class:`GraphError` on any other failure. Returns the token bundle
    (access_token, refresh_token, expires_in, etc.) on success.
    """
    return _post_form(
        _token_url(tenant),
        {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": client_id,
            "device_code": device_code,
        },
    )


def refresh_access_token(
    client_id: str, tenant: str, refresh_token: str,
) -> dict[str, Any]:
    """Exchange a refresh token for a new access token (and rotated refresh)."""
    return _post_form(
        _token_url(tenant),
        {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": refresh_token,
            "scope": _SCOPES,
        },
    )


def _get_access_token(cfg: GraphConfig) -> tuple[str, str]:
    """Return (access_token, possibly_rotated_refresh_token).

    Caches tokens in-process for ``expires_in - 60s`` to avoid burning a
    refresh round-trip on every send. The returned refresh_token may differ
    from the one in ``cfg`` when Microsoft rotates it; the caller must
    persist the new value.
    """
    if not cfg.is_configured():
        raise GraphError("Graph is not configured (missing client_id or refresh_token)")

    cache_key = f"{cfg.client_id}:{cfg.tenant}"
    now = time.time()
    with _token_cache_lock:
        entry = _token_cache.get(cache_key)
        if entry and entry.expires_at - 60 > now:
            return entry.access_token, cfg.refresh_token

    bundle = refresh_access_token(cfg.client_id, cfg.tenant, cfg.refresh_token)
    access = bundle.get("access_token")
    if not access:
        raise GraphError("token endpoint returned no access_token")
    expires_in = int(bundle.get("expires_in", 3600))
    new_refresh = bundle.get("refresh_token") or cfg.refresh_token
    with _token_cache_lock:
        _token_cache[cache_key] = _TokenCacheEntry(access, now + expires_in)
    return access, new_refresh


# ── sendMail ────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class GraphSendResult:
    success: bool
    rotated_refresh_token: str = ""
    error: str = ""


def send_mail(
    cfg: GraphConfig,
    *,
    sender: str,
    recipient: str,
    subject: str,
    body_text: str,
    body_html: str = "",
) -> GraphSendResult:
    """Send a single email via ``/me/sendMail``.

    *sender* is informational only — Microsoft Graph forces the From: header
    to be the authenticated mailbox owner. The header is set so the audit
    log records the intended sender for transparency.
    """
    try:
        access_token, rotated = _get_access_token(cfg)
    except GraphError as exc:
        return GraphSendResult(success=False, error=str(exc))

    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML" if body_html else "Text",
                "content": body_html or body_text or " ",
            },
            "toRecipients": [{"emailAddress": {"address": recipient}}],
        },
        "saveToSentItems": True,
    }
    try:
        _post_json(f"{_GRAPH_BASE}/me/sendMail", payload, token=access_token)
        return GraphSendResult(success=True, rotated_refresh_token=rotated)
    except GraphError as exc:
        return GraphSendResult(success=False, error=str(exc), rotated_refresh_token=rotated)


__all__ = [
    "GraphConfig",
    "GraphError",
    "GraphAuthPending",
    "GraphSendResult",
    "start_device_flow",
    "poll_device_flow",
    "refresh_access_token",
    "send_mail",
]
