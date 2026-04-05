"""Studies CRUD API.

A Study is a named, user-editable visual workflow graph comprising
experiment and pipeline nodes connected by data-flow edges.

Endpoints:
  GET    /studies            -- list all studies
  GET    /studies/{id}       -- get a study
  POST   /studies            -- create a study
  PUT    /studies/{id}       -- update a study (name/description/graph)
  DELETE /studies/{id}       -- delete a study
  POST   /studies/{id}/run   -- execute all experiment nodes in topological order
"""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db
from glossa_lab.experiment_base import get_experiment

router = APIRouter()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fmt(study: dict[str, Any]) -> dict[str, Any]:
    """Ensure graph is always a dict with nodes/edges lists."""
    g = study.get("graph") or {}
    if not isinstance(g, dict):
        g = {}
    study["graph"] = {
        "nodes": g.get("nodes", []),
        "edges": g.get("edges", []),
    }
    return study


# ── Models ─────────────────────────────────────────────────────────────


class NodePos(BaseModel):
    x: float = 0.0
    y: float = 0.0


class StudyNodeIn(BaseModel):
    id: str
    type: str = "experiment"
    ref_id: str = ""
    label: str = ""
    params: dict[str, Any] = {}
    position: NodePos = NodePos()


class StudyEdgeIn(BaseModel):
    id: str
    source: str
    target: str


class StudyGraphIn(BaseModel):
    nodes: list[StudyNodeIn] = []
    edges: list[StudyEdgeIn] = []


class StudyCreate(BaseModel):
    name: str
    description: str = ""
    graph: StudyGraphIn = StudyGraphIn()


class StudyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    graph: StudyGraphIn | None = None


# ── Endpoints ──────────────────────────────────────────────────────────


@router.get("/studies")
async def list_studies() -> list[dict[str, Any]]:
    db = get_db()
    if db is None:
        return []
    studies = await db.list_studies()
    return [_fmt(s) for s in studies]


@router.get("/studies/{study_id}")
async def get_study(study_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.get_study(study_id)
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")
    return _fmt(study)


@router.post("/studies", status_code=201)
async def create_study(body: StudyCreate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.create_study(
        name=body.name,
        description=body.description,
        graph=body.graph.model_dump(),
        created_at=_now_iso(),
    )
    return _fmt(study)


@router.put("/studies/{study_id}")
async def update_study(study_id: str, body: StudyUpdate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.update_study(
        study_id,
        name=body.name,
        description=body.description,
        graph=body.graph.model_dump() if body.graph is not None else None,
    )
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")
    return _fmt(study)


@router.delete("/studies/{study_id}")
async def delete_study(study_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    deleted = await db.delete_study(study_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")
    return {"deleted": True, "id": study_id}


# ── Study execution ──────────────────────────────────────────────────


def _topological_sort(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Kahn’s algorithm: return nodes in execution order (sources first).

    Nodes that are not reachable from any ordering are appended at the end.
    """
    id_to_node = {n["id"]: n for n in nodes}
    in_degree: dict[str, int] = {n["id"]: 0 for n in nodes}
    successors: dict[str, list[str]] = {n["id"]: [] for n in nodes}

    for edge in edges:
        src, tgt = edge.get("source", ""), edge.get("target", "")
        if src in in_degree and tgt in in_degree:
            in_degree[tgt] += 1
            successors[src].append(tgt)

    queue: deque[str] = deque(node_id for node_id, deg in in_degree.items() if deg == 0)
    order: list[dict[str, Any]] = []
    while queue:
        nid = queue.popleft()
        order.append(id_to_node[nid])
        for succ in successors[nid]:
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                queue.append(succ)

    # Append any remaining nodes (cycle members — degrade gracefully)
    visited_ids = {n["id"] for n in order}
    for n in nodes:
        if n["id"] not in visited_ids:
            order.append(n)

    return order


def _run_node(
    node: dict[str, Any],
    upstream_results: dict[str, Any],
) -> dict[str, Any]:
    """Execute a single node synchronously. Returns a result dict."""
    node_type = node.get("type", "")
    ref_id = node.get("ref_id", "")
    node_params = node.get("params") or {}

    if node_type != "experiment":
        return {"status": "skipped", "reason": "pipeline nodes require job submission"}

    cls = get_experiment(ref_id)
    if cls is None:
        return {"status": "error", "reason": f"Experiment '{ref_id}' not found"}

    try:
        instance = cls()
        kwargs = {**node_params, "upstream_results": upstream_results}
        result = instance.run(**kwargs)
        return {"status": "complete", "result": result}
    except NotImplementedError:
        return {
            "status": "skipped",
            "reason": f"'{ref_id}' has no run() implementation; use the CLI command.",
        }
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "reason": str(exc)}


@router.post("/studies/{study_id}/run")
async def run_study(study_id: str) -> dict[str, Any]:
    """Execute all experiment nodes in topological order.

    Passes each completed node’s result to its downstream nodes as
    ``upstream_results`` in the experiment kwargs.

    Pipeline nodes are skipped (they require a job with a corpus ID).
    """
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.get_study(study_id)
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")

    graph = study.get("graph") or {}
    nodes: list[dict[str, Any]] = graph.get("nodes", [])
    edges: list[dict[str, Any]] = graph.get("edges", [])

    if not nodes:
        return {"study_id": study_id, "node_count": 0, "results": {}}

    ordered = _topological_sort(nodes, edges)

    # Build successor map for result forwarding
    successors: dict[str, list[str]] = {n["id"]: [] for n in nodes}
    for edge in edges:
        src = edge.get("source", "")
        if src in successors:
            successors[src].append(edge.get("target", ""))

    node_results: dict[str, Any] = {}  # node_id → result dict
    loop = asyncio.get_event_loop()

    for node in ordered:
        nid = node["id"]
        # Collect results from all immediate predecessors
        predecessors = [e.get("source", "") for e in edges if e.get("target", "") == nid]
        upstream: dict[str, Any] = {
            pred: node_results[pred].get("result")
            for pred in predecessors
            if pred in node_results and node_results[pred].get("status") == "complete"
        }
        node_results[nid] = await loop.run_in_executor(None, _run_node, node, upstream)

    completed = sum(1 for r in node_results.values() if r["status"] == "complete")
    skipped = sum(1 for r in node_results.values() if r["status"] == "skipped")
    errors = sum(1 for r in node_results.values() if r["status"] == "error")

    return {
        "study_id": study_id,
        "node_count": len(nodes),
        "completed": completed,
        "skipped": skipped,
        "errors": errors,
        "results": node_results,
    }
