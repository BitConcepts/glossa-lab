"""Studies CRUD API.

A Study is a named, user-editable visual workflow graph comprising
experiment and pipeline nodes connected by data-flow edges.

Endpoints:
  GET    /studies               -- list all studies
  GET    /studies/{id}          -- get a study
  POST   /studies               -- create a study
  PUT    /studies/{id}          -- update a study (name/description/graph)
  DELETE /studies/{id}          -- delete a study
  POST   /studies/{id}/run      -- execute all experiment nodes in topological order
  POST   /studies/{id}/summarize -- AI-generate a structured summary
  POST   /studies/generate      -- AI-design a study from a prompt
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


# ── AI features ──────────────────────────────────────────────────────


class GenerateStudyRequest(BaseModel):
    prompt: str
    name: str


@router.post("/studies/generate", status_code=201)
async def generate_study(body: GenerateStudyRequest) -> dict[str, Any]:
    """Use AI to design a study graph from a natural-language prompt.

    Lists available experiments, sends them to the LLM, and creates a study
    with the AI-designed node graph already populated.
    """
    import asyncio
    import json

    from glossa_lab.ai_utils import call_llm
    from glossa_lab.experiment_base import list_discovered_experiments

    exps = list_discovered_experiments()
    exp_list = "\n".join(
        f"  id={e['id']!r}, name={e['name']!r}, category={e['category']!r}, "
        f"desc={e['description'][:80]!r}"
        for e in exps[:30]
    )

    system = (
        "You are a research workflow designer for Glossa Lab — a computational linguistics lab "
        "studying the Indus Script. Given a research goal and available experiments, design a "
        "study graph. Return ONLY valid JSON:\n"
        '{"description": "brief research goal", '
        '"nodes": [{"id": "n1", "ref_id": "<experiment id>", '
        '"label": "<experiment name>", "type": "experiment", '
        '"position": {"x": 100, "y": 100}}], '
        '"edges": [{"id": "e1", "source": "n1", "target": "n2"}]}\n'
        "Rules: only use IDs from the provided list; space nodes 220px apart horizontally "
        "and 150px vertically; connect experiments that share data dependencies; "
        "include 2-6 nodes maximum."
    )
    user = (
        f"Available experiments:\n{exp_list}\n\n"
        f'Design a study called "{body.name}" that: {body.prompt}'
    )

    try:
        loop = asyncio.get_event_loop()
        raw = await loop.run_in_executor(
            None,
            lambda: call_llm(
                [{"role": "system", "content": system}, {"role": "user", "content": user}],
                json_mode=True,
            ),
        )
        graph_data: dict[str, Any] = json.loads(raw)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"LLM error: {exc}") from exc

    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.create_study(
        name=body.name,
        description=graph_data.get("description", ""),
        graph={"nodes": graph_data.get("nodes", []), "edges": graph_data.get("edges", [])},
        created_at=_now_iso(),
    )
    return _fmt(study)


@router.post("/studies/{study_id}/summarize")
async def summarize_study(study_id: str) -> dict[str, Any]:
    """Use AI to generate a structured summary of a study.

    Returns {abstract, hypothesis, highlights, insights, next_steps,
    suggested_actions, study_id, name, description, node_count}.
    """
    import asyncio
    import json

    from glossa_lab.ai_utils import call_llm
    from glossa_lab.experiment_base import get_experiment

    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    study = await db.get_study(study_id)
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study '{study_id}' not found")

    graph = study.get("graph") or {}
    nodes: list[dict[str, Any]] = graph.get("nodes", [])
    edges: list[dict[str, Any]] = graph.get("edges", [])

    exp_details = []
    for node in nodes:
        ref_id = node.get("ref_id", "")
        cls = get_experiment(ref_id)
        if cls:
            m = cls.to_dict()
            exp_details.append(f"- {m['name']} ({m['category']}): {m['description'][:100]}")
        else:
            exp_details.append(f"- {node.get('label', ref_id)} (ref: {ref_id})")

    system = (
        "You are a research assistant summarizing a multi-experiment scientific study on the "
        "Indus Script. Return ONLY valid JSON with these exact fields:\n"
        '{"abstract": "2-3 sentence study-level summary", '
        '"hypothesis": "overarching hypothesis or research question or null", '
        '"highlights": ["key cross-experiment finding 1", "key finding 2"], '
        '"insights": "what combined results tell us about the Indus Script", '
        '"next_steps": ["recommended research direction 1", "direction 2"], '
        '"suggested_actions": [{"label": "Create Follow-up Study", '
        '"action": "create_study", "hint": "brief description"}, '
        '{"label": "Generate Experiment", "action": "generate_experiment", '
        '"hint": "brief description"}]}'
    )
    user = (
        f"Study: {study['name']}\n"
        f"Description: {study.get('description', 'N/A')}\n"
        f"Experiments ({len(nodes)} nodes, {len(edges)} edges):\n"
        + ("\n".join(exp_details) if exp_details else "No experiments in graph")
        + "\n\nSummarize this study and its research implications."
    )

    try:
        loop = asyncio.get_event_loop()
        raw = await loop.run_in_executor(
            None,
            lambda: call_llm(
                [{"role": "system", "content": system}, {"role": "user", "content": user}],
                json_mode=True,
            ),
        )
        result: dict[str, Any] = json.loads(raw)
        result["study_id"] = study_id
        result["name"] = study["name"]
        result["description"] = study.get("description", "")
        result["node_count"] = len(nodes)
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


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
