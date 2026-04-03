"""Settings API — secure storage of API keys and configuration.

Keys are stored in {data_dir}/.keys.json (not in the database).
Values are never returned in plaintext; only a masked status is returned.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter

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
