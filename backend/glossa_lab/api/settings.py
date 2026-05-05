"""Settings API — secure storage of API keys and configuration.

Keys are stored in {data_dir}/.keys.json (not in the database).
Values are never returned in plaintext; only a masked status is returned.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from glossa_lab.config import get_settings

router = APIRouter(prefix="/api/v1/settings", tags=["settings"])

_MASK = "••••••••"

KNOWN_KEYS = [
    # LLM providers (verifiable via _VERIFY_ENDPOINTS)
    "mistral_api_key",
    "openai_api_key",
    "anthropic_api_key",
    "google_api_key",
    # Discovery / search providers — used by the continuous-discovery engine
    # (no verify endpoints yet; added in a follow-up phase if needed).
    "serp_api_key",
    "news_api_key",
    "brave_search_api_key",
    # Optional API keys for higher rate limits on keyless sources.
    # Semantic Scholar: free key removes the 100 req/5min cap.
    # OpenAlex: "polite pool" with an email gets priority access.
    "semantic_scholar_api_key",
    "openalex_email",
    # Patent data sources.
    # PatentsView (search.patentsview.org) — required for the patentsview fetcher.
    "patentsview_api_key",
    # USPTO Open Data Portal — optional upgrade key for the keyless PPUBS fetcher.
    "uspto_api_key",
    # Academia.edu — NOT an API key, but a *session cookie* harvested from a
    # logged-in browser. Optional. When present the academia.py fetcher
    # upgrades from public-search-only to authenticated mode and can stream
    # PDFs into the local data dir. Leave unset for keyless metadata-only
    # discovery, which works without any account.
    "academia_session_cookie",
    # SMTP — outbound email notifications (discovery digest + study/experiment
    # completion emails). All optional; if smtp_host or smtp_from is unset the
    # Notifier becomes a silent no-op so runs never fail because of missing creds.
    "smtp_host",
    "smtp_port",
    "smtp_username",
    "smtp_password",
    "smtp_from",
    "smtp_use_tls",
    # Microsoft Graph (Outlook 365 OAuth) — set via the Connect Outlook 365
    # button in the Notifications panel, which runs the device-code flow.
    # ``ms_graph_client_id`` is the Application (client) ID from the Azure
    # app registration; ``ms_graph_tenant_id`` defaults to ``common`` so
    # both consumer and work/school accounts work; ``ms_graph_refresh_token``
    # is written by the OAuth callback after the user approves consent.
    "ms_graph_client_id",
    "ms_graph_tenant_id",
    "ms_graph_refresh_token",
    # Resend HTTPS API — zero-server email transport. With just an API key,
    # users can email out from "onboarding@resend.dev" without any domain,
    # mailbox, or DNS setup. ``resend_from`` is optional; defaults to the
    # Resend shared sender.
    "resend_api_key",
    "resend_from",
    # Discovery scheduler auto-start. "1" = run fetch+mine+digest every 24h
    # automatically when the backend lifespan boots. Surfaced in the
    # Notifications panel as a toggle so the user doesn't need shell access.
    "discovery_daily",
]

KNOWN_PROVIDERS = ["openai", "anthropic", "google", "mistral", "ollama"]
_PROVIDERS_KEY = "_provider_prefs"


def _keys_file() -> Path:
    settings = get_settings()
    return Path(settings.data_dir) / ".keys.json"


def _load_keys() -> dict[str, str]:
    f = _keys_file()
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_keys(data: dict[str, str]) -> None:
    f = _keys_file()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, indent=2), encoding="utf-8")
    # Restrict permissions on Unix
    try:
        f.chmod(0o600)
    except Exception:
        pass


# Values that look like a real key but are actually placeholders. We treat
# them as "not configured" so a fetcher / verifier never POSTs them to a
# real provider (which would 401/422). Match by exact-equal OR by prefix
# so common forms like ``dummy-news``, ``dummy_serp``, ``placeholder-xxx``,
# ``your-api-key-here``, ``<insert key>`` are all caught.
_PLACEHOLDER_EQUAL = {
    "", "none", "null", "undefined", "<your-key>", "<your-api-key>",
    "your-api-key-here", "your_api_key_here", "replace-me", "replace_me",
    "changeme", "change-me", "todo", "tbd", "xxx", "xxxx", "xxxxxxxx",
}
_PLACEHOLDER_PREFIX = (
    "dummy", "placeholder", "<insert", "<your", "sk-xxx", "your-", "your_",
)
_log_warned: set[str] = set()


def _is_placeholder(value: str | None) -> bool:
    if not value:
        return True
    v = value.strip().lower()
    if not v or v in _PLACEHOLDER_EQUAL:
        return True
    return any(v.startswith(p) for p in _PLACEHOLDER_PREFIX)


def get_key(key_name: str) -> str | None:
    """Return the plaintext value of a stored key (for internal use only).

    Resolution order: process env (UPPERCASE name) -> stored ``.keys.json``.
    Placeholder values (``dummy-*``, ``your-api-key-here`` etc.) are
    treated as if no key were set so callers fall through to the next
    source or skip the request entirely.
    """
    import logging  # noqa: PLC0415

    env_name = key_name.upper()
    env_val = os.environ.get(env_name)
    if env_val and not _is_placeholder(env_val):
        return env_val
    if env_val and _is_placeholder(env_val) and env_name not in _log_warned:
        # Surface this once: a polluted env variable beats the stored value
        # and would otherwise cause silent provider 401s with no clue why.
        _log_warned.add(env_name)
        logging.getLogger("glossa_lab.api.settings").warning(
            "Ignoring placeholder env value for %s (%r); falling back to stored key. "
            "Run `Remove-Item Env:%s` in your shell or `setx %s \"\"` to clear it.",
            env_name, env_val, env_name, env_name,
        )
    stored = _load_keys().get(key_name)
    if stored and _is_placeholder(stored):
        return None
    return stored


# ── Verification ─────────────────────────────────────────────────────

_VERIFY_ENDPOINTS: dict[str, dict[str, Any]] = {
    "mistral_api_key": {
        "provider": "Mistral",
        "url": "https://api.mistral.ai/v1/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "extra_headers": {},
    },
    "openai_api_key": {
        "provider": "OpenAI",
        "url": "https://api.openai.com/v1/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "extra_headers": {},
    },
    "anthropic_api_key": {
        "provider": "Anthropic",
        "url": "https://api.anthropic.com/v1/models",
        "auth_header": "x-api-key",
        "auth_prefix": "",
        "extra_headers": {"anthropic-version": "2023-06-01"},
    },
    "google_api_key": {
        "provider": "Google",
        "url": "https://generativelanguage.googleapis.com/v1beta/models",
        "auth_header": None,  # key goes in query param
        "auth_prefix": "",
        "query_param": "key",
        "extra_headers": {},
    },
    # ── Discovery / search providers ─────────────────────────────────────
    "serp_api_key": {
        "provider": "SerpAPI",
        "url": "https://serpapi.com/account",
        "auth_header": None,
        "auth_prefix": "",
        "query_param": "api_key",
        "extra_headers": {},
    },
    "news_api_key": {
        "provider": "NewsAPI",
        # /v2/sources is the cheapest auth check; returns 200 + sources list
        "url": "https://newsapi.org/v2/sources",
        "auth_header": "X-Api-Key",
        "auth_prefix": "",
        "extra_headers": {},
    },
    "brave_search_api_key": {
        "provider": "Brave Search",
        "url": "https://api.search.brave.com/res/v1/web/search?q=test&count=1",
        "auth_header": "X-Subscription-Token",
        "auth_prefix": "",
        "extra_headers": {"Accept": "application/json"},
    },
    "semantic_scholar_api_key": {
        "provider": "Semantic Scholar",
        # Lightweight search with limit=1 — validates the key + returns rate headers.
        "url": "https://api.semanticscholar.org/graph/v1/paper/search?query=test&limit=1&fields=paperId",
        "auth_header": "x-api-key",
        "auth_prefix": "",
        "extra_headers": {},
    },
    "openalex_email": {
        "provider": "OpenAlex",
        # A minimal search with mailto= — 200 means the polite pool accepted us.
        "url": "https://api.openalex.org/works?search=test&per-page=1",
        "auth_header": None,
        "auth_prefix": "",
        "query_param": "mailto",
        "extra_headers": {},
    },
    # ── Patent data sources ──────────────────────────────────────────────
    "patentsview_api_key": {
        "provider": "PatentsView",
        # Lightweight search — validates the key + returns rate headers.
        "url": "https://search.patentsview.org/api/v1/patent/?q={%22patent_id%22:%2210000000%22}&f=[%22patent_id%22]&o={%22size%22:1}",
        "auth_header": "X-Api-Key",
        "auth_prefix": "",
        "extra_headers": {},
    },
}


class VerifyRequest(BaseModel):
    key_name: str
    key_value: str | None = None  # if provided, verifies this value instead of stored


@router.post("/verify-key")
async def verify_key(body: VerifyRequest) -> dict[str, Any]:
    """Test an API key against the provider's models endpoint.

    Uses the stored key unless key_value is supplied directly.
    Returns {valid, provider, message}.
    """
    key_name = body.key_name
    if key_name not in KNOWN_KEYS:
        return {"valid": False, "provider": "", "message": f"Unknown key: {key_name}"}

    ep = _VERIFY_ENDPOINTS.get(key_name)
    if not ep:
        return {"valid": False, "provider": "", "message": "No verification endpoint configured"}

    # Resolve the key value
    key_val = body.key_value or get_key(key_name)
    if not key_val:
        return {
            "valid": False,
            "provider": ep["provider"],
            "message": "Key is not set. Enter and save the key first.",
        }

    # Build the request
    url = ep["url"]
    if ep["auth_header"] is None:
        # Key goes in a query parameter (Google, SerpAPI, etc.)
        param = ep.get("query_param", "key")
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}{param}={key_val}"

    headers: dict[str, str] = {"Accept": "application/json"}
    if ep["auth_header"]:
        headers[ep["auth_header"]] = ep["auth_prefix"] + key_val
    headers.update(ep.get("extra_headers", {}))

    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            # Capture rate-limit headers from the verify response.
            rl_limit = (
                resp.headers.get("X-RateLimit-Limit")
                or resp.headers.get("RateLimit-Limit")
            )
            rl_remaining = (
                resp.headers.get("X-RateLimit-Remaining")
                or resp.headers.get("RateLimit-Remaining")
            )
        if status == 200:
            msg = f"{ep['provider']} key is valid."
            if rl_limit:
                msg += f" Rate limit: {rl_limit}/window"
                if rl_remaining:
                    msg += f", {rl_remaining} remaining"
                msg += "."
            # Record in the rate tracker so the /sources API shows the limit.
            try:
                from glossa_lab.discovery.fetchers.base import get_rate_tracker  # noqa: PLC0415
                tracker = get_rate_tracker()
                # Map key_name → source name for the tracker.
                src_map = {
                    "semantic_scholar_api_key": "semanticscholar",
                    "openalex_email": "openalex",
                    "brave_search_api_key": "brave",
                    "news_api_key": "newsapi",
                    "serp_api_key": "serpapi",
                    "patentsview_api_key": "patentsview",
                }
                src = src_map.get(key_name)
                if src:
                    info: dict[str, object] = {}
                    if rl_limit:
                        try: info["limit"] = int(rl_limit)
                        except ValueError: info["limit"] = rl_limit
                    if rl_remaining:
                        try: info["remaining"] = int(rl_remaining)
                        except ValueError: info["remaining"] = rl_remaining
                    if info:
                        tracker.record_request(src, ok=True, rate_limit_info=info)
            except Exception:  # noqa: BLE001
                pass
            return {
                "valid": True,
                "provider": ep["provider"],
                "message": msg,
            }
        return {
            "valid": False,
            "provider": ep["provider"],
            "message": f"Unexpected status {status}.",
        }
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return {
                "valid": False,
                "provider": ep["provider"],
                "message": f"Invalid key (HTTP {exc.code}: Unauthorized).",
            }
        return {
            "valid": False,
            "provider": ep["provider"],
            "message": f"HTTP error {exc.code}: {exc.reason}.",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "valid": False,
            "provider": ep["provider"],
            "message": f"Connection error: {exc}",
        }


@router.get("")
async def read_settings() -> dict[str, Any]:
    """Return settings with masked key values — never exposes plaintext."""
    stored = _load_keys()
    keys_status: dict[str, Any] = {}
    for k in KNOWN_KEYS:
        # Env var takes precedence
        env_val = os.environ.get(k.upper())
        if env_val:
            keys_status[k] = {"set": True, "source": "env", "masked": _MASK}
        elif k in stored and stored[k]:
            keys_status[k] = {"set": True, "source": "stored", "masked": _MASK}
        else:
            keys_status[k] = {"set": False, "source": None, "masked": ""}

    stored_providers = stored.get(_PROVIDERS_KEY, {})
    return {
        "keys": keys_status,
        "providers": stored_providers,
        "data_dir": str(get_settings().data_dir),
    }


@router.put("")
async def update_settings(body: dict[str, Any]) -> dict[str, Any]:
    """Update stored settings. Pass empty string to clear a key."""
    stored = _load_keys()
    updated: list[str] = []

    for k in KNOWN_KEYS:
        if k in body:
            val = body[k].strip()
            if val:
                stored[k] = val
                # Also set in current process environment so pipelines pick it up
                os.environ[k.upper()] = val
                updated.append(k)
            elif val == "" and k in stored:
                # Clear the key
                del stored[k]
                os.environ.pop(k.upper(), None)
                updated.append(k)

    # Provider preferences (enable/model-selection state)
    updated_providers: list[str] = []
    if "providers" in body and isinstance(body.get("providers"), dict):
        prefs = stored.get(_PROVIDERS_KEY, {})
        for pid, pdata in body["providers"].items():
            if pid in KNOWN_PROVIDERS and isinstance(pdata, dict):
                prefs[pid] = pdata
                updated_providers.append(pid)
        stored[_PROVIDERS_KEY] = prefs

    _save_keys(stored)

    return {
        "updated": updated,
        "updated_providers": updated_providers,
        "message": f"{len(updated)} key(s) and {len(updated_providers)} provider(s) updated",
    }
