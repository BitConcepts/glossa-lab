"""Reports API backed by the repository reports directory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from glossa_lab.catalog import list_report_catalog

router = APIRouter()

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_REPORTS_DIR = _REPO_ROOT / "reports"
_ALIASES = {"indus": "real_indus_catalog_analysis.json"}


@router.get("/reports")
async def list_reports() -> list[dict[str, Any]]:
    return list_report_catalog()


@router.get("/reports/{report_name}")
async def get_report(report_name: str) -> dict[str, Any]:
    path = _resolve(report_name)
    if path is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "name": path.name,
        "relative_path": path.relative_to(_REPO_ROOT).as_posix(),
        "content": path.read_text(encoding="utf-8"),
    }


@router.delete("/reports/{report_name}")
async def delete_report(report_name: str) -> dict[str, Any]:
    path = _resolve(report_name)
    if path is None:
        raise HTTPException(status_code=404, detail="Report not found")
    relative_path = path.relative_to(_REPO_ROOT).as_posix()
    path.unlink()
    return {"deleted": True, "relative_path": relative_path}


def _resolve(report_name: str) -> Path | None:
    name = _ALIASES.get(report_name, report_name)
    for path in _REPORTS_DIR.rglob("*"):
        if path.is_file() and (path.name == name or path.stem == name):
            return path
    return None
