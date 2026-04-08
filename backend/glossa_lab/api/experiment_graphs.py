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

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.experiment_graph import (
    ATOMIC_NODES,
    PORT_COLORS,
    delete_graph_experiment,
    execute_graph,
    get_graph_experiment,
    list_graph_experiments,
    save_graph_experiment,
)

router = APIRouter(prefix="/experiment-graphs", tags=["experiment-graphs"])


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


# ── Run / Preview ─────────────────────────────────────────────────────────────

@router.post("/{exp_id}/run")
async def run_experiment(exp_id: str, body: RunGraphBody) -> dict[str, Any]:
    """Execute a graph experiment and return the result (preview mode)."""
    import asyncio  # noqa: PLC0415
    d = get_graph_experiment(exp_id)
    if d is None:
        raise HTTPException(status_code=404, detail=f"Graph experiment '{exp_id}' not found")
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, execute_graph, d, body.kwargs)
        return {"status": "complete", "result": result}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
