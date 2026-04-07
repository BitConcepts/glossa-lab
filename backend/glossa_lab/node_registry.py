"""Node Registry — unified param schema lookup for Study Builder nodes.

Provides a JSON-Schema-compatible dict for any experiment or pipeline node,
enabling the Study Builder inspector to render typed parameter forms.

Endpoints
---------
GET /node-registry/{node_type}/{ref_id}
    Returns the JSON Schema for the node's run/execute parameters.
    node_type: "experiment" | "pipeline"
    ref_id:    experiment id or pipeline id
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter()


# ── Schema helpers ─────────────────────────────────────────────────────


def _schema_from_defaults(defaults: dict[str, Any]) -> dict[str, Any]:
    """Infer a minimal JSON Schema from a dict of default param values."""
    props: dict[str, Any] = {}
    for key, val in defaults.items():
        title = key.replace("_", " ").title()
        if isinstance(val, bool):
            props[key] = {"type": "boolean", "title": title, "default": val}
        elif isinstance(val, int):
            props[key] = {"type": "integer", "title": title, "default": val, "minimum": 0}
        elif isinstance(val, float):
            props[key] = {"type": "number", "title": title, "default": val}
        elif val is None:
            props[key] = {"type": "string", "title": title, "default": ""}
        else:
            props[key] = {"type": "string", "title": title, "default": str(val) if val else ""}
    return {"type": "object", "properties": props}


def get_node_params_schema(node_type: str, ref_id: str) -> dict[str, Any] | None:
    """Return the JSON Schema describing a node's run() parameters.

    Returns ``None`` if the node type / ref_id is unknown.
    Returns an empty schema dict if the node is known but declares no params.
    """
    if node_type == "experiment":
        from glossa_lab.experiment_base import get_experiment  # noqa: PLC0415

        cls = get_experiment(ref_id)
        if cls is None:
            return None
        return cls.params_schema or {}

    if node_type == "pipeline":
        from glossa_lab.catalog import list_pipeline_catalog  # noqa: PLC0415

        catalog = list_pipeline_catalog()
        entry = next((p for p in catalog if p["id"] == ref_id), None)
        if entry is None:
            return None
        defaults: dict[str, Any] = entry.get("default_params") or {}
        return _schema_from_defaults(defaults) if defaults else {}

    return None


# ── API endpoint ────────────────────────────────────────────────────────


@router.get("/node-registry/{node_type}/{ref_id}")
async def get_node_schema(node_type: str, ref_id: str) -> dict[str, Any]:
    """Return the JSON Schema for a Study Builder node's parameters.

    - ``node_type`` must be ``experiment`` or ``pipeline``.
    - ``ref_id`` is the experiment/pipeline identifier.
    """
    schema = get_node_params_schema(node_type, ref_id)
    if schema is None:
        raise HTTPException(
            status_code=404,
            detail=f"Node '{node_type}/{ref_id}' not found in registry",
        )
    return schema
