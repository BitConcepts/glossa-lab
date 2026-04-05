"""Experiments discovery and management API.

Endpoints:
  GET  /experiments              -- list all discovered experiments
  GET  /experiments/{id}         -- get experiment metadata
  POST /experiments/{id}/run     -- run an experiment
  POST /experiments/import       -- import a .py file
  POST /experiments/{id}/duplicate -- duplicate an experiment
  DELETE /experiments/{id}       -- delete an experiment file
  POST /experiments/generate     -- AI-generate a new experiment
"""

from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.experiment_base import (
    create_experiment_from_prompt,
    delete_experiment_file,
    duplicate_experiment_file,
    get_experiment,
    import_experiment_file,
    invalidate_cache,
    list_discovered_experiments,
)

router = APIRouter()


@router.get("/experiments")
async def list_experiments() -> list[dict[str, Any]]:
    """Return all discovered experiments with metadata."""
    return list_discovered_experiments()


@router.get("/experiments/{experiment_id}")
async def get_experiment_meta(experiment_id: str) -> dict[str, Any]:
    cls = get_experiment(experiment_id)
    if cls is None:
        raise HTTPException(status_code=404, detail=f"Experiment '{experiment_id}' not found")
    return cls.to_dict()


class RunRequest(BaseModel):
    kwargs: dict[str, Any] = {}


@router.post("/experiments/{experiment_id}/run")
async def run_experiment(experiment_id: str, body: RunRequest) -> dict[str, Any]:
    """Execute an experiment and return the result."""
    cls = get_experiment(experiment_id)
    if cls is None:
        raise HTTPException(status_code=404, detail=f"Experiment '{experiment_id}' not found")
    try:
        instance = cls()
        if asyncio.iscoroutinefunction(instance.run):
            result = await instance.run(**body.kwargs)
        else:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: instance.run(**body.kwargs))
        return {"experiment_id": experiment_id, "result": result}
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail=f"Experiment '{experiment_id}' has no run() implementation. "
                   "Use the CLI command instead.",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


class ImportRequest(BaseModel):
    source_path: str


@router.post("/experiments/import", status_code=201)
async def import_experiment(body: ImportRequest) -> dict[str, Any]:
    try:
        return import_experiment_file(body.source_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


class DuplicateRequest(BaseModel):
    new_id: str | None = None
    new_name: str | None = None


@router.post("/experiments/{experiment_id}/duplicate", status_code=201)
async def dup_experiment(experiment_id: str, body: DuplicateRequest) -> dict[str, Any]:
    try:
        return duplicate_experiment_file(experiment_id, body.new_id, body.new_name)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/experiments/{experiment_id}")
async def del_experiment(experiment_id: str) -> dict[str, Any]:
    try:
        return delete_experiment_file(experiment_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


class GenerateRequest(BaseModel):
    prompt: str
    name: str
    category: str = "Analysis"


@router.post("/experiments/generate", status_code=201)
async def generate_experiment(body: GenerateRequest) -> dict[str, Any]:
    """Use AI to generate a new experiment from a natural language prompt."""
    import os
    api_key = os.environ.get("OPENAI_API_KEY")
    try:
        result = create_experiment_from_prompt(
            prompt=body.prompt,
            name=body.name,
            category=body.category,
            openai_api_key=api_key,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ImportError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/experiments/reload")
async def reload_experiments() -> dict[str, Any]:
    """Invalidate the discovery cache and re-scan."""
    invalidate_cache()
    experiments = list_discovered_experiments()
    return {"reloaded": True, "count": len(experiments)}
