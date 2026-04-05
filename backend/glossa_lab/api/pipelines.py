"""Pipeline discovery and management API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.catalog import list_pipeline_catalog
from glossa_lab.pipeline_base import (
    delete_pipeline_file,
    duplicate_pipeline_file,
    import_pipeline_file,
)

router = APIRouter()


@router.get("/pipelines")
async def list_pipelines() -> list[dict[str, Any]]:
    """Return all registered pipelines with metadata."""
    return list_pipeline_catalog()


class ImportPipelineRequest(BaseModel):
    source_path: str


@router.post("/pipelines/import", status_code=201)
async def import_pipeline(body: ImportPipelineRequest) -> dict[str, Any]:
    try:
        return import_pipeline_file(body.source_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


class DupPipelineRequest(BaseModel):
    new_id: str | None = None


@router.post("/pipelines/{pipeline_id}/duplicate", status_code=201)
async def dup_pipeline(pipeline_id: str, body: DupPipelineRequest) -> dict[str, Any]:
    try:
        return duplicate_pipeline_file(pipeline_id, body.new_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/pipelines/{pipeline_id}")
async def del_pipeline(pipeline_id: str) -> dict[str, Any]:
    try:
        return delete_pipeline_file(pipeline_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
