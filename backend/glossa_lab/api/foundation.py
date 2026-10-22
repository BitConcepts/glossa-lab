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

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/foundation", tags=["foundation"])
_log = logging.getLogger("glossa_lab.api.foundation")

_REPO = Path(__file__).resolve().parents[3]
_CONFIG_PATH = _REPO / "backend" / "outputs" / "foundation_config.json"

# Spec 029 Phase J (D-D): the status endpoint serves the on-disk
# foundation report or fails loudly — never the silent nulls the
# audit found beside a healthy report file (§5-P8 defect 3).
_REPORT_PATH = _REPO / "reports" / "foundation_check_report.json"
_ANCHORS_PATH = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"


def _load_disk_report() -> dict[str, Any]:
    """Read the on-disk foundation report; raise on any failure."""
    raw = _REPORT_PATH.read_text(encoding="utf-8")
    report = json.loads(raw)
    if not isinstance(report, dict):
        raise ValueError("foundation report is not a JSON object")
    return report


def _report_block(report: dict[str, Any]) -> dict[str, Any]:
    """The served form of the on-disk report, with staleness check.

    The block carries the report's figures, its as-of label, and
    its anchors-file hash stamp. If the stamped hash no longer
    matches the anchors file currently on disk, the report is
    served WITH an explicit staleness flag and warning (its
    figures describe its own stamped table, not the current one)
    — flagged, never silently current.
    """
    from glossa_lab.foundation_annotations import (  # noqa: PLC0415
        anchors_file_sha256,
    )

    block: dict[str, Any] = {
        "verdict": report.get("verdict"),
        "n_ok": report.get("n_ok"),
        "n_fail": report.get("n_fail"),
        "n_warn": report.get("n_warn"),
        "generated_at": report.get("generated_at"),
        "annotations_as_of": report.get("annotations_as_of"),
        "anchors_file": report.get("anchors_file"),
        "anchors_file_sha256": report.get("anchors_file_sha256"),
        "claims_store_sha256": report.get("claims_store_sha256"),
        "solid_claims": report.get("solid_claims", []),
        "caveated_claims": report.get("caveated_claims", []),
    }
    stamped = report.get("anchors_file_sha256")
    current: str | None = None
    if _ANCHORS_PATH.exists():
        current = anchors_file_sha256(_ANCHORS_PATH)
    block["anchors_file_sha256_current"] = current
    block["report_stale"] = bool(
        stamped and current and stamped != current
    )
    if block["report_stale"]:
        block["staleness_warning"] = (
            "This foundation report was computed against a different "
            f"anchors file (stamped SHA-256 {stamped}; current "
            f"{current}). Its figures carry its own as-of label and "
            "do not describe the current anchor table — re-run the "
            "foundation check to refresh the report."
        )
    return block

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
        result = {**result, "source": "foundation_api"}
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


# ── External result recording ────────────────────────────────────────────

async def record_result(result: dict[str, Any], *, source: str) -> None:
    """Record a foundation check run that happened outside _run_check().

    The research API (GET /api/v1/research/foundation-check — the path
    the MCP run_foundation_check tool uses) runs its own check set and
    previously recorded nothing, so /foundation/status stayed null even
    after a full check had just run. Any completed run, from any entry
    point, should be visible in the tracker.
    """
    global _last_result, _last_checked_at, _foundation_dirty  # noqa: PLW0603
    _last_result = {**result, "source": source}
    _last_checked_at = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    _foundation_dirty = False
    try:
        from glossa_lab.api.events import emit_event  # noqa: PLC0415
        await emit_event("foundation_complete", result=_last_result)
    except Exception:  # noqa: BLE001
        pass
    _log.info(
        "Foundation check recorded (source=%s): %d ok, %d fail, %d warn",
        source,
        result.get("n_ok", 0), result.get("n_fail", 0), result.get("n_warn", 0),
    )


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
    """Return last check result and auto-check state.

    Spec 029 Phase J (D-D): when no run has been recorded in this
    process, the on-disk foundation report is served instead of
    silent nulls. A missing or unreadable report (with no recorded
    run) is an explicit HTTP 503 error — loud, never a null
    payload. The on-disk report, when readable, is attached under
    ``report`` in both paths, hash-stamped and staleness-flagged;
    when a recorded run exists but the report cannot be read, the
    failure is stated in ``report_error`` rather than hidden.
    """
    cfg = _load_config()
    result: dict[str, Any] = {
        "last_checked_at": _last_checked_at,
        "auto_check_enabled": cfg.get("auto_check_enabled", True),
        "dirty": _foundation_dirty,
        "running": _check_running,
    }
    report: dict[str, Any] | None = None
    report_error: str | None = None
    try:
        report = _load_disk_report()
    except Exception as exc:  # noqa: BLE001
        report_error = f"{type(exc).__name__}: {exc}"

    if _last_result:
        result["verdict"] = _last_result.get("verdict", "UNKNOWN")
        result["n_ok"] = _last_result.get("n_ok", 0)
        result["n_fail"] = _last_result.get("n_fail", 0)
        result["n_warn"] = _last_result.get("n_warn", 0)
        result["source"] = _last_result.get("source", "foundation_api")
    elif report is not None:
        block = _report_block(report)
        result["verdict"] = block["verdict"]
        result["n_ok"] = block["n_ok"]
        result["n_fail"] = block["n_fail"]
        result["n_warn"] = block["n_warn"]
        result["source"] = "on_disk_report"
        result["last_checked_at"] = block["generated_at"]
    else:
        raise HTTPException(
            status_code=503,
            detail=(
                "foundation report unavailable: no foundation check "
                "has been recorded in this process and the on-disk "
                f"report at {_REPORT_PATH} could not be served "
                f"({report_error}). Run the foundation check to "
                "generate the report."
            ),
        )
    if report is not None:
        result["report"] = _report_block(report)
    else:
        result["report_error"] = (
            f"on-disk foundation report unreadable: {report_error}"
        )
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
