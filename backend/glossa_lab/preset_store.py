"""Lightweight file-backed preset store for pipeline and experiment presets."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from glossa_lab.config import get_settings


def _store_path() -> Path:
    return Path(get_settings().data_dir) / "presets.json"


def _load() -> dict[str, list[dict[str, Any]]]:
    path = _store_path()
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"pipeline_presets": [], "experiment_presets": []}


def _save(data: dict[str, list[dict[str, Any]]]) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ── Pipeline presets ──────────────────────────────────────────────────


def list_pipeline_presets() -> list[dict[str, Any]]:
    return _load()["pipeline_presets"]


def add_pipeline_preset(preset: dict[str, Any]) -> dict[str, Any]:
    data = _load()
    entry = {**preset, "id": uuid.uuid4().hex[:12], "custom": True}
    data["pipeline_presets"].append(entry)
    _save(data)
    return entry


def duplicate_pipeline_preset(preset_id: str) -> dict[str, Any] | None:
    data = _load()
    src = next((p for p in data["pipeline_presets"] if p.get("id") == preset_id), None)
    if src is None:
        return None
    entry = {**src, "id": uuid.uuid4().hex[:12], "label": src.get("label", "") + " (copy)"}
    data["pipeline_presets"].append(entry)
    _save(data)
    return entry


def delete_pipeline_preset(preset_id: str) -> bool:
    data = _load()
    before = len(data["pipeline_presets"])
    data["pipeline_presets"] = [p for p in data["pipeline_presets"] if p.get("id") != preset_id]
    if len(data["pipeline_presets"]) == before:
        return False
    _save(data)
    return True


# ── Experiment presets ────────────────────────────────────────────────


def list_experiment_presets() -> list[dict[str, Any]]:
    return _load()["experiment_presets"]


def add_experiment_preset(preset: dict[str, Any]) -> dict[str, Any]:
    data = _load()
    entry = {**preset, "id": uuid.uuid4().hex[:12], "custom": True}
    data["experiment_presets"].append(entry)
    _save(data)
    return entry


def duplicate_experiment_preset(preset_id: str) -> dict[str, Any] | None:
    data = _load()
    src = next((p for p in data["experiment_presets"] if p.get("id") == preset_id), None)
    if src is None:
        return None
    entry = {**src, "id": uuid.uuid4().hex[:12], "name": src.get("name", "") + " (copy)"}
    data["experiment_presets"].append(entry)
    _save(data)
    return entry


def delete_experiment_preset(preset_id: str) -> bool:
    data = _load()
    before = len(data["experiment_presets"])
    data["experiment_presets"] = [p for p in data["experiment_presets"] if p.get("id") != preset_id]
    if len(data["experiment_presets"]) == before:
        return False
    _save(data)
    return True
