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
    "mistral_api_key",
    "openai_api_key",
    "anthropic_api_key",
    "google_api_key",
]

KNOWN_PROVIDERS = ["openai", "anthropic", "google", "mistral"]
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


def get_key(key_name: str) -> str | None:
    """Return the plaintext value of a stored key (for internal use only)."""
    # Check environment variable first (overrides stored keys)
    env_val = os.environ.get(key_name.upper())
    if env_val:
        return env_val
    return _load_keys().get(key_name)


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
    if ep["auth_header"] is None:  # Google: key in query param
        url = f"{url}?key={key_val}"

    headers: dict[str, str] = {"Accept": "application/json"}
    if ep["auth_header"]:
        headers[ep["auth_header"]] = ep["auth_prefix"] + key_val
    headers.update(ep.get("extra_headers", {}))

    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
        if status == 200:
            return {
                "valid": True,
                "provider": ep["provider"],
                "message": f"{ep['provider']} key is valid.",
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
