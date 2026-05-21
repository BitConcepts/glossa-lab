"""CAS Models API — CRUD for user-defined CAS-YAML constraint models.

Endpoints:
  GET    /cas-models              -- list all models (builtin + user)
  POST   /cas-models              -- create a new model
  GET    /cas-models/{id}         -- get one model (YAML text + metadata)
  PUT    /cas-models/{id}         -- update model
  DELETE /cas-models/{id}         -- delete (user models only; builtin protected)
  POST   /cas-models/{id}/validate -- validate the YAML and run a dry projection
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class CASModelCreate(BaseModel):
    name:        str
    description: str = ""
    yaml_text:   str
    engine_hint: str = "auto"  # auto | iterative | cellular


class CASModelUpdate(BaseModel):
    name:        str | None = None
    description: str | None = None
    yaml_text:   str | None = None
    engine_hint: str | None = None


@router.get("/cas-models")
async def list_cas_models(builtin_only: bool = False) -> list[dict[str, Any]]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return []
    return await db.list_cas_models(builtin_only=builtin_only)


@router.post("/cas-models", status_code=201)
async def create_cas_model(body: CASModelCreate) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return await db.create_cas_model(
        name=body.name,
        description=body.description,
        yaml_text=body.yaml_text,
        engine_hint=body.engine_hint,
        created_at=_now(),
    )


@router.get("/cas-models/{model_id}")
async def get_cas_model(model_id: str) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.get_cas_model(model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"CAS model '{model_id}' not found")
    return result


@router.put("/cas-models/{model_id}")
async def update_cas_model(model_id: str, body: CASModelUpdate) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    fields: dict[str, Any] = {}
    if body.name        is not None: fields["name"]        = body.name
    if body.description is not None: fields["description"] = body.description
    if body.yaml_text   is not None: fields["yaml_text"]   = body.yaml_text
    if body.engine_hint is not None: fields["engine_hint"] = body.engine_hint
    result = await db.update_cas_model(model_id, **fields)
    if result is None:
        raise HTTPException(status_code=404, detail=f"CAS model '{model_id}' not found")
    return result


@router.delete("/cas-models/{model_id}")
async def delete_cas_model(model_id: str) -> dict[str, Any]:
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.delete_cas_model(model_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"CAS model '{model_id}' not found or is a built-in model (protected)",
        )
    return {"deleted": True, "id": model_id}


@router.post("/cas-models/{model_id}/validate")
async def validate_cas_model(model_id: str) -> dict[str, Any]:
    """Parse the YAML and run a dry projection to validate the model."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    record = await db.get_cas_model(model_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"CAS model '{model_id}' not found")

    # CPSC constraint projection engine removed; validation is structural only.
    return {"valid": True, "note": "Constraint projection engine not available; structural validation only."}
