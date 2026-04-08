"""Experiment Graph API.

Endpoints:
  GET    /experiment-graphs/catalog        -- atomic node catalog (for Exp Builder palette)
  GET    /experiment-graphs/port-colors    -- port type → hex colour map
  GET    /experiment-graphs                -- list saved graph experiments
  GET    /experiment-graphs/{id}           -- get one graph experiment
  POST   /experiment-graphs               -- save / create a graph experiment
  PUT    /experiment-graphs/{id}           -- update a graph experiment
  DELETE /experiment-graphs/{id}           -- delete a graph experiment
  POST   /experiment-graphs/{id}/run       -- run a graph experiment (preview)
"""
from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from glossa_lab.experiment_graph import (
    ATOMIC_NODES,
    PORT_COLORS,
    _node_type_and_params,
    _topo_sort,
    delete_graph_experiment,
    get_graph_experiment,
    list_graph_experiments,
    save_graph_experiment,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/experiment-graphs", tags=["experiment-graphs"])

_SSE_HEADERS = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}


def _sse(data: dict[str, Any]) -> str:
    return f"data: {json.dumps(data)}\n\n"


class GraphExperimentBody(BaseModel):
    id: str | None = None
    name: str = "Untitled Experiment"
    description: str = ""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []


class RunGraphBody(BaseModel):
    kwargs: dict[str, Any] = {}


# ── Catalog ──────────────────────────────────────────────────────────────────

@router.get("/catalog")
async def get_atomic_catalog() -> list[dict[str, Any]]:
    """Return the full atomic node catalog for the Experiment Builder palette."""
    return [n.to_dict() for n in ATOMIC_NODES.values()]


@router.get("/port-colors")
async def get_port_colors() -> dict[str, str]:
    """Return the port type → hex colour map (shared with the frontend)."""
    return PORT_COLORS


# ── CRUD ─────────────────────────────────────────────────────────────────────

@router.get("")
async def list_experiments() -> list[dict[str, Any]]:
    return list_graph_experiments()


@router.get("/{exp_id}")
async def get_experiment(exp_id: str) -> dict[str, Any]:
    d = get_graph_experiment(exp_id)
    if d is None:
        raise HTTPException(status_code=404, detail=f"Graph experiment '{exp_id}' not found")
    return d


@router.post("", status_code=201)
async def create_experiment(body: GraphExperimentBody) -> dict[str, Any]:
    data = body.model_dump()
    return save_graph_experiment(data)


@router.put("/{exp_id}")
async def update_experiment(exp_id: str, body: GraphExperimentBody) -> dict[str, Any]:
    data = body.model_dump()
    data["id"] = exp_id
    return save_graph_experiment(data)


@router.delete("/{exp_id}")
async def delete_experiment(exp_id: str) -> dict[str, Any]:
    ok = delete_graph_experiment(exp_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Graph experiment '{exp_id}' not found")
    return {"deleted": True, "id": exp_id}


# ── Run / Preview (SSE streaming) ────────────────────────────────────────────

@router.post("/{exp_id}/run")
async def run_experiment(exp_id: str, body: RunGraphBody) -> StreamingResponse:
    """Stream graph experiment execution as SSE. One event per atomic node."""
    d = get_graph_experiment(exp_id)
    if d is None:
        raise HTTPException(status_code=404, detail=f"Graph experiment '{exp_id}' not found")

    nodes = d.get("nodes", [])
    edges = d.get("edges", [])
    kwargs = body.kwargs or {}

    async def _stream() -> AsyncGenerator[str, None]:
        if not nodes:
            yield _sse({"event": "run_complete", "exp_id": exp_id,
                        "node_count": 0, "status": "complete", "result": {}})
            return

        ordered = _topo_sort(nodes, edges)
        loop = asyncio.get_event_loop()
        res: dict[str, dict[str, Any]] = {}

        yield _sse({"event": "started", "exp_id": exp_id,
                    "exp_name": d.get("name", exp_id), "node_count": len(ordered)})
        logger.info("Experiment run '%s' starting (%d nodes)", d.get("name"), len(ordered))

        try:
            for node_idx, node in enumerate(ordered):
                nid = node["id"]
                ntype, node_params = _node_type_and_params(node)
                node_label = (node.get("data") or {}).get("label") or ntype

                yield _sse({"event": "node_start", "nid": nid, "label": node_label,
                            "type": ntype, "idx": node_idx, "total": len(ordered)})

                # Collect inputs from upstream nodes
                node_inputs: dict[str, Any] = {}
                for e in edges:
                    src, sp, tp = e.get("source", ""), e.get("sourcePort", ""), e.get("targetPort", "")
                    if e.get("target") != nid or src not in res:
                        continue
                    tp = tp or sp or "data"
                    if sp and sp in res[src]:
                        node_inputs[tp] = res[src][sp]
                    else:
                        node_inputs.update(res[src])

                params = {**node_params, **kwargs}
                atomic = ATOMIC_NODES.get(ntype)
                if not atomic:
                    node_result = {"error": f"Unknown node type: '{ntype}'"}
                else:
                    try:
                        node_result = await loop.run_in_executor(
                            None, atomic.fn, node_inputs, params
                        ) or {}
                    except Exception as exc:  # noqa: BLE001
                        node_result = {"error": str(exc)}

                res[nid] = node_result
                had_error = "error" in node_result
                yield _sse({"event": "node_end", "nid": nid,
                            "status": "error" if had_error else "complete",
                            "error": node_result.get("error", "")})

        except Exception as exc:  # noqa: BLE001
            logger.error("Experiment run '%s' crashed: %s", d.get("name"), exc)
            yield _sse({"event": "run_error", "message": str(exc)})
            return

        # Collect outputs (Output-category nodes)
        output_ids = [
            n["id"] for n in nodes
            if ATOMIC_NODES.get(_node_type_and_params(n)[0]) is not None
            and ATOMIC_NODES[_node_type_and_params(n)[0]].category == "Outputs"
        ]
        merged: dict[str, Any] = {}
        for oid in output_ids:
            if oid in res:
                merged.update(res[oid])
        if not merged and res:
            # If no Output nodes, return last node result
            merged = res[list(res.keys())[-1]]

        logger.info("Experiment run '%s' complete", d.get("name"))
        yield _sse({"event": "run_complete", "exp_id": exp_id,
                    "node_count": len(ordered), "status": "complete",
                    "result": merged, "node_results": res})

    return StreamingResponse(_stream(), media_type="text/event-stream", headers=_SSE_HEADERS)
