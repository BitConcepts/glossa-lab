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


# ── Built-in schemas for non-experiment/pipeline node types ───────────────────────

_BUILTIN_SCHEMAS: dict[str, dict[str, Any]] = {
    "corpus": {
        "type": "object",
        "properties": {
            "corpus_id": {
                "type": "string",
                "title": "Corpus ID",
                "description": "UUID of the corpus in the Corpora tab. Downstream nodes receive this as corpus_id.",
            },
        },
    },
    "note": {
        "type": "object",
        "properties": {
            "note_text": {
                "type": "string",
                "title": "Note Text",
                "description": "Annotation text shown on the graph node.",
            },
        },
    },
    "report": {
        "type": "object",
        "properties": {
            "report_name": {
                "type": "string",
                "title": "Report File",
                "description": "Name of the report file in reports/ (e.g. positional_profile_analysis.json).",
            },
        },
    },
    "hypothesis": {
        "type": "object",
        "properties": {
            "hypothesis_id": {
                "type": "string",
                "title": "Hypothesis ID",
                "description": "Optional ID of an existing Hypothesis record to link to this node.",
            },
            "title": {
                "type": "string",
                "title": "Hypothesis Title",
                "description": "Short title if creating a new hypothesis.",
            },
        },
    },
    "rag_query": {
        "type": "object",
        "properties": {
            "query_override": {
                "type": "string",
                "title": "Query Override",
                "description": "Custom search query. Leave blank to auto-generate from upstream results.",
            },
            "top_k": {
                "type": "integer",
                "title": "Top K Results",
                "default": 5,
                "minimum": 1,
                "maximum": 20,
                "description": "Maximum number of retrieved chunks to pass downstream.",
            },
        },
    },
    "ai_analysis": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "title": "Prompt",
                "description": "Optional custom instruction to guide the AI analysis. Leave blank for default interpretation.",
            },
            "context_summary": {
                "type": "boolean",
                "title": "Include Context Summary",
                "default": True,
                "description": "Prepend a summary of all upstream results to the AI prompt.",
            },
        },
    },
}


def get_node_params_schema(node_type: str, ref_id: str) -> dict[str, Any] | None:
    """Return the JSON Schema describing a node's run() parameters.

    Returns ``None`` if the node type / ref_id is unknown.
    Returns an empty schema dict if the node is known but declares no params.
    """
    # Built-in node types with fixed schemas
    if node_type in _BUILTIN_SCHEMAS:
        return _BUILTIN_SCHEMAS[node_type]

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
