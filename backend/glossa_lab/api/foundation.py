"""Foundation check automation API.

POST /api/v1/foundation/check   — run foundation check synchronously
GET  /api/v1/foundation/status  — last check result + auto-check state
PATCH /api/v1/foundation/config — enable/disable auto-checks

A background task runs every 15 minutes; if the `foundation_dirty` flag
is set (by anchor changes or SA experiments), it triggers a check
automatically and clears the flag.
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/foundation", tags=["foundation"])
_log = logging.getLogger("glossa_lab.api.foundation")

_REPO = Path(__file__).resolve().parents[3]
_CONFIG_PATH = _REPO / "backend" / "outputs" / "foundation_config.json"

# ── Mutable state ────────────────────────────────────────────────────────
_foundation_dirty: bool = False
_last_result: dict[str, Any] | None = None
_last_checked_at: str | None = None
_check_running: bool = False
_bg_task: asyncio.Task | None = None


# ── Config persistence ───────────────────────────────────────────────────

def _load_config() -> dict[str, Any]:
    try:
        if _CONFIG_PATH.exists():
            return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        pass
    return {"auto_check_enabled": True}


def _save_config(cfg: dict[str, Any]) -> None:
    try:
        _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        _log.warning("Could not save foundation config: %s", exc)


def mark_dirty() -> None:
    """Set the dirty flag — call when anchors change or SA experiments finish."""
    global _foundation_dirty  # noqa: PLW0603
    _foundation_dirty = True
    _log.debug("Foundation marked dirty")


# ── Core check runner ────────────────────────────────────────────────────

async def _run_check() -> dict[str, Any]:
    """Run foundation check synchronously (reuses existing _run_foundation_check)."""
    global _last_result, _last_checked_at, _check_running, _foundation_dirty  # noqa: PLW0603
    if _check_running:
        return _last_result or {"error": "check already in progress"}
    _check_running = True
    try:
        from glossa_lab.api.research_loop import _run_foundation_check  # noqa: PLC0415
        result = await _run_foundation_check()
        now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
        _last_result = result
        _last_checked_at = now
        _foundation_dirty = False

        # Emit event for frontend
        try:
            from glossa_lab.api.events import emit_event  # noqa: PLC0415
            await emit_event("foundation_complete", result=result)
        except Exception:  # noqa: BLE001
            pass

        _log.info(
            "Foundation check complete: %d ok, %d fail, %d warn",
            result.get("n_ok", 0), result.get("n_fail", 0), result.get("n_warn", 0),
        )
        return result
    except Exception as exc:  # noqa: BLE001
        _log.warning("Foundation check failed: %s", exc)
        return {"error": str(exc)}
    finally:
        _check_running = False


# ── Background auto-check task ───────────────────────────────────────────

async def _auto_check_loop() -> None:
    """Background task: checks every 15 minutes if dirty and enabled."""
    while True:
        await asyncio.sleep(15 * 60)  # 15 minutes
        try:
            cfg = _load_config()
            if not cfg.get("auto_check_enabled", True):
                continue
            if not _foundation_dirty:
                continue
            if _check_running:
                continue
            _log.info("Auto foundation check triggered (dirty flag set)")
            await _run_check()
        except Exception as exc:  # noqa: BLE001
            _log.warning("Auto foundation check error: %s", exc)


def start_auto_check() -> None:
    """Start the background auto-check task (call once at app startup)."""
    global _bg_task  # noqa: PLW0603
    if _bg_task is None or _bg_task.done():
        _bg_task = asyncio.create_task(_auto_check_loop())
        _log.info("Foundation auto-check background task started")


# ── API endpoints ────────────────────────────────────────────────────────

@router.post("/check")
async def check_foundation() -> dict[str, Any]:
    """Run foundation check synchronously and return results."""
    return await _run_check()


@router.get("/status")
async def foundation_status() -> dict[str, Any]:
    """Return last check result and auto-check state."""
    cfg = _load_config()
    result: dict[str, Any] = {
        "last_checked_at": _last_checked_at,
        "auto_check_enabled": cfg.get("auto_check_enabled", True),
        "dirty": _foundation_dirty,
        "running": _check_running,
    }
    if _last_result:
        result["verdict"] = _last_result.get("verdict", "UNKNOWN")
        result["n_ok"] = _last_result.get("n_ok", 0)
        result["n_fail"] = _last_result.get("n_fail", 0)
        result["n_warn"] = _last_result.get("n_warn", 0)
    else:
        result["verdict"] = None
        result["n_ok"] = 0
        result["n_fail"] = 0
        result["n_warn"] = 0
    return result


class FoundationConfigUpdate(BaseModel):
    auto_check_enabled: bool | None = None


@router.patch("/config")
async def update_foundation_config(body: FoundationConfigUpdate) -> dict[str, Any]:
    """Enable/disable auto-checks."""
    cfg = _load_config()
    if body.auto_check_enabled is not None:
        cfg["auto_check_enabled"] = body.auto_check_enabled
    _save_config(cfg)
    return {"ok": True, **cfg}
