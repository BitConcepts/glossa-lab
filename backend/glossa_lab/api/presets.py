"""Preset management endpoints for pipelines and experiments."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from glossa_lab.preset_store import (
    add_experiment_preset,
    add_pipeline_preset,
    delete_experiment_preset,
    delete_pipeline_preset,
    duplicate_experiment_preset,
    duplicate_pipeline_preset,
    list_experiment_presets,
    list_pipeline_presets,
)

router = APIRouter()


@router.get("/presets/pipelines")
async def get_pipeline_presets() -> list[dict[str, Any]]:
    return list_pipeline_presets()


@router.post("/presets/pipelines", status_code=201)
async def create_pipeline_preset(body: dict[str, Any]) -> dict[str, Any]:
    return add_pipeline_preset(body)


@router.post("/presets/pipelines/{preset_id}/duplicate", status_code=201)
async def dup_pipeline_preset(preset_id: str) -> dict[str, Any]:
    result = duplicate_pipeline_preset(preset_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Preset not found")
    return result


@router.delete("/presets/pipelines/{preset_id}")
async def del_pipeline_preset(preset_id: str) -> dict[str, Any]:
    if not delete_pipeline_preset(preset_id):
        raise HTTPException(status_code=404, detail="Preset not found")
    return {"deleted": True, "id": preset_id}


@router.get("/presets/experiments")
async def get_experiment_presets() -> list[dict[str, Any]]:
    return list_experiment_presets()


@router.post("/presets/experiments", status_code=201)
async def create_experiment_preset(body: dict[str, Any]) -> dict[str, Any]:
    return add_experiment_preset(body)


@router.post("/presets/experiments/{preset_id}/duplicate", status_code=201)
async def dup_experiment_preset(preset_id: str) -> dict[str, Any]:
    result = duplicate_experiment_preset(preset_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Preset not found")
    return result


@router.delete("/presets/experiments/{preset_id}")
async def del_experiment_preset(preset_id: str) -> dict[str, Any]:
    if not delete_experiment_preset(preset_id):
        raise HTTPException(status_code=404, detail="Preset not found")
    return {"deleted": True, "id": preset_id}
