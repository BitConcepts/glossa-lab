"""Persistent dismissal store – keeps track of dismissed action keys.

Storage: ``outputs/dismissed_actions.json`` (a JSON array of string keys).
All file I/O is wrapped in try/except so the server never crashes on a
missing or corrupt file.  A module-level ``threading.Lock`` serialises
concurrent writes.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/dismissals", tags=["dismissals"])

_DISMISSED_JSON = Path(__file__).resolve().parents[3] / "outputs" / "dismissed_actions.json"
_lock = threading.Lock()


# ── helpers ──────────────────────────────────────────────────────────

def _load() -> List[str]:
    """Return the current list of dismissed keys (empty list on any error)."""
    try:
        if _DISMISSED_JSON.exists():
            data = json.loads(_DISMISSED_JSON.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return [str(k) for k in data]
    except Exception:  # noqa: BLE001
        pass
    return []


def _save(keys: List[str]) -> None:
    """Persist *keys* to the JSON file, creating parent dirs if needed."""
    try:
        _DISMISSED_JSON.parent.mkdir(parents=True, exist_ok=True)
        _DISMISSED_JSON.write_text(
            json.dumps(keys, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:  # noqa: BLE001
        pass


# ── request models ───────────────────────────────────────────────────

class _DismissBody(BaseModel):
    key: str


# ── endpoints ────────────────────────────────────────────────────────

@router.get("")
async def list_dismissed():
    """Return all dismissed keys."""
    with _lock:
        return {"dismissed": _load()}


@router.post("")
async def add_dismissed(body: _DismissBody):
    """Add a key to the dismissed list (idempotent)."""
    with _lock:
        keys = _load()
        if body.key not in keys:
            keys.append(body.key)
            _save(keys)
        return {"ok": True, "key": body.key}


@router.delete("/{key}")
async def remove_dismissed(key: str):
    """Remove a single key from the dismissed list."""
    with _lock:
        keys = _load()
        if key in keys:
            keys.remove(key)
            _save(keys)
            return {"ok": True}
        return {"ok": False}


@router.delete("")
async def clear_dismissed():
    """Clear all dismissed keys."""
    with _lock:
        keys = _load()
        n = len(keys)
        _save([])
        return {"cleared": n}
