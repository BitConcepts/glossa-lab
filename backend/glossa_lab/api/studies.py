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
import json
import logging
from collections import deque
from collections.abc import AsyncGenerator
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from glossa_lab.database import get_db
from glossa_lab.experiment_base import get_experiment

logger = logging.getLogger(__name__)
router = APIRouter()

_SSE_HEADERS = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}


def _sse(data: dict[str, Any]) -> str:
    return f"data: {json.dumps(data)}\n\n"


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
    type: str = "experiment"   # experiment|pipeline|corpus|note|report|hypothesis|rag_query|ai_analysis
    ref_id: str = ""
    label: str = ""
    params: dict[str, Any] = {}
    note_text: str = ""        # text content for note nodes
    color: str = ""            # optional custom hex color override
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


# ── Node type helpers ────────────────────────────────────────────────────────

# Annotation-only node types: just pass through without execution
_ANNOTATION_TYPES = frozenset({"note", "hypothesis"})
# note: "report" is now executable (saves compiled upstream results to file)


def _run_experiment_node(
    node: dict[str, Any],
    upstream_results: dict[str, Any],
) -> dict[str, Any]:
    """Execute an experiment node synchronously (runs in a thread executor).

    corpus_id is resolved in priority order:
      1. Explicit param on the node (set in Inspector)
      2. corpus_id from an upstream 'corpus' type node result
      3. Blank — experiment falls back to its built-in default corpus

    All upstream results are also passed so experiments can use them.
    """
    ref_id = node.get("ref_id", "")
    node_params = node.get("params") or {}

    cls = get_experiment(ref_id)
    if cls is None:
        return {"status": "error", "reason": f"Experiment '{ref_id}' not found"}

    # Resolve corpus_id: node param wins; otherwise take from upstream corpus node.
    corpus_id: str | None = node_params.get("corpus_id") or None
    if not corpus_id:
        for r in upstream_results.values():
            if isinstance(r, dict) and r.get("corpus_id"):
                corpus_id = r["corpus_id"]
                break

    # Build run kwargs: merge node params, inject corpus_id, pass upstream results.
    run_kwargs: dict[str, Any] = {**node_params}
    if corpus_id:
        run_kwargs["corpus_id"] = corpus_id
    run_kwargs["upstream_results"] = upstream_results

    try:
        instance = cls()
        result = instance.run(**run_kwargs)
        return {"status": "complete", "result": result}
    except NotImplementedError:
        return {
            "status": "skipped",
            "reason": f"'{ref_id}' has no run() implementation; use the CLI command.",
        }
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "reason": str(exc)}


async def _run_pipeline_node(
    node: dict[str, Any],
    upstream_results: dict[str, Any],
    db: Any,
    timeout: float = 120.0,
) -> dict[str, Any]:
    """Submit a pipeline as a background Job and poll until complete.

    Returns the job result if it completes within ``timeout`` seconds,
    or a ``pending`` status dict if it times out.
    """
    import asyncio  # noqa: PLC0415

    ref_id = node.get("ref_id", "")
    node_params = node.get("params") or {}

    if not ref_id:
        return {"status": "skipped", "reason": "Pipeline node has no ref_id set"}

    # Merge upstream corpus_id into params when present
    corpus_id = node_params.get("corpus_id") or (
        next((r.get("corpus_id") for r in upstream_results.values()
              if isinstance(r, dict) and r.get("corpus_id")), None)
    )
    if corpus_id:
        node_params = {**node_params, "corpus_id": corpus_id}
        node_params.setdefault("text_id", corpus_id)  # some pipelines use text_id

    try:
        job = await db.create_job(
            name=f"Study: {node.get('label', ref_id)}",
            pipeline=ref_id,
            params=node_params,
            created_at=_now_iso(),
        )
        job_id = job["id"]
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "reason": f"Failed to submit pipeline job: {exc}"}

    # Poll for completion
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        await asyncio.sleep(1.5)
        try:
            job = await db.get_job(job_id)
            if job is None:
                return {"status": "error", "reason": f"Job {job_id} disappeared"}
            status = job["status"]
            if status == "completed":
                result_row = await db.get_result_for_job(job_id)
                result_data = result_row["data"] if result_row else {}
                return {"status": "complete", "result": result_data, "job_id": job_id}
            if status == "failed":
                result_row = await db.get_result_for_job(job_id)
                err = (result_row or {}).get("data", {}).get("error", "job failed")
                return {"status": "error", "reason": err, "job_id": job_id}
        except Exception:  # noqa: BLE001
            pass

    return {
        "status": "pending",
        "reason": f"Pipeline job {job_id} timed out after {timeout:.0f}s. Re-run study when complete.",
        "job_id": job_id,
    }


async def _run_rag_node(
    node: dict[str, Any],
    upstream_results: dict[str, Any],
) -> dict[str, Any]:
    """Query the RAG index using upstream context or a param override."""
    from glossa_lab.rag import build_index, index_size, query as rag_query  # noqa: PLC0415
    from glossa_lab.database import get_db  # noqa: PLC0415

    node_params = node.get("params") or {}
    query_override = str(node_params.get("query_override", "")).strip()
    top_k = int(node_params.get("top_k", 5))

    # Build query text from upstream results if no override given
    if not query_override:
        parts = []
        for r in upstream_results.values():
            if isinstance(r, dict):
                # Pull a compact text summary from upstream result
                for key in ("interpretation", "winner_kl", "summary", "title"):
                    if key in r:
                        parts.append(str(r[key])[:200])
                        break
        query_override = " ".join(parts) or node.get("label", "research context")

    # Auto-build index if needed
    if index_size() == 0:
        db = get_db()
        await build_index(db)

    chunks = rag_query(query_override, top_k=top_k)
    retrieved_text = "\n\n".join(
        f"[{c['source_type']}:{c['source']}]\n{c['text']}"
        for c in chunks
    )
    return {
        "status": "complete",
        "result": {
            "query": query_override,
            "chunks": chunks,
            "retrieved_text": retrieved_text,
        },
    }


def _run_report_node(
    node: dict[str, Any],
    upstream_results: dict[str, Any],
) -> dict[str, Any]:
    """Compile all upstream results and save to a named JSON file in reports/.

    The report_name param controls the filename (defaults to slugified label).
    Upstream results are stored under a 'results' key alongside metadata.
    """
    import json as _json  # noqa: PLC0415
    import re  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    node_params = node.get("params") or {}
    report_name = str(node_params.get("report_name", "")).strip()
    if not report_name:
        label = node.get("label", "study_report")
        report_name = re.sub(r"[^a-z0-9_]+", "_", label.lower()).strip("_") + ".json"
    if not report_name.endswith(".json"):
        report_name += ".json"

    rep_dir = Path(__file__).resolve().parent.parent.parent.parent / "reports"
    rep_dir.mkdir(exist_ok=True)
    out_path = rep_dir / report_name

    compiled = {
        "report": node.get("label", "Study Report"),
        "generated": _now_iso(),
        "results": {k: v.get("result") for k, v in upstream_results.items() if isinstance(v, dict)},
    }
    out_path.write_text(_json.dumps(compiled, indent=2, default=str), encoding="utf-8")
    return {
        "status": "complete",
        "result": {"saved": True, "path": str(out_path), "filename": report_name},
    }


async def _run_compare_node(
    node: dict[str, Any],
    upstream_results: dict[str, Any],
) -> dict[str, Any]:
    """Compare two upstream results using Glossa AI with a structured template."""
    from glossa_lab.ai_utils import call_llm  # noqa: PLC0415

    node_params = node.get("params") or {}
    custom_prompt = str(node_params.get("comparison_prompt", "")).strip()
    aspects = str(node_params.get("comparison_aspects", "accuracy, patterns, key differences")).strip()

    keys = list(upstream_results.keys())
    a_key = keys[0] if keys else "A"
    b_key = keys[1] if len(keys) > 1 else "B"
    a_val = upstream_results.get(a_key, {})
    b_val = upstream_results.get(b_key, {})

    system = (
        "You are a scientific comparator. Analyse two research results and produce a structured comparison. "
        "Return ONLY valid JSON in this exact format: "
        '{"summary": "1-2 sentence overall comparison", '
        '"a_strengths": ["..."], "b_strengths": ["..."], '
        '"key_differences": ["..."], "recommendation": "which approach to prefer and why", '
        '"insights": "deeper analytical insight for the research question"}'
    )
    prompt = custom_prompt or f"Compare these two research results across: {aspects}"
    user = (
        f"{prompt}\n\n"
        f"Result A ({a_key}):\n{json.dumps(a_val)[:1200]}\n\n"
        f"Result B ({b_key}):\n{json.dumps(b_val)[:1200]}"
    )

    loop = asyncio.get_event_loop()
    try:
        raw = await loop.run_in_executor(
            None,
            lambda: call_llm(
                [{"role": "system", "content": system}, {"role": "user", "content": user}],
                json_mode=True, max_tokens=800, temperature=0.3,
            ),
        )
        comparison = json.loads(raw)
        return {
            "status": "complete",
            "result": {
                "comparison": comparison,
                "a_key": a_key, "b_key": b_key,
                "prompt_used": prompt,
            },
        }
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "reason": f"Compare failed: {exc}"}


async def _run_ai_analysis_node(
    node: dict[str, Any],
    upstream_results: dict[str, Any],
) -> dict[str, Any]:
    """Pass upstream results to Glossa AI for interpretation."""
    from glossa_lab.ai_utils import call_llm  # noqa: PLC0415

    node_params = node.get("params") or {}
    custom_prompt = str(node_params.get("prompt", "")).strip()
    include_summary = bool(node_params.get("context_summary", True))

    # Build context from upstream
    ctx_parts = []
    for nid, result in upstream_results.items():
        if isinstance(result, dict):
            ctx_parts.append(f"From {nid}: {json.dumps(result)[:600]}")

    context = "\n\n".join(ctx_parts) or "(no upstream results)"
    prompt_text = custom_prompt or "Interpret the following analysis results and provide key findings:"

    system = (
        "You are Glossa, a computational linguistics research assistant. "
        "Analyse the provided data and return concise, scientifically grounded findings."
    )
    user = f"{prompt_text}\n\n{context}"

    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: call_llm(
                [{"role": "system", "content": system}, {"role": "user", "content": user}],
                max_tokens=800,
                temperature=0.3,
            ),
        )
        return {"status": "complete", "result": {"analysis": response, "prompt": prompt_text}}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "reason": f"AI analysis failed: {exc}"}


@router.post("/studies/{study_id}/run")
async def run_study(study_id: str) -> StreamingResponse:  # noqa: PLR0912
    """Stream study execution as Server-Sent Events.

    Events: started | node_start | node_end | run_complete | run_error
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

    async def _stream() -> AsyncGenerator[str, None]:  # noqa: PLR0912
        # ── Create job record ─────────────────────────────────────────────────
        job_id: str | None = None
        if not nodes:
            yield _sse({"event": "run_complete", "study_id": study_id,
                        "node_count": 0, "completed": 0, "errors": 0,
                        "skipped": 0, "annotations": 0, "results": {}, "job_id": None})
            return

        try:
            job = await db.create_job(
                name=f"Study run: {study['name']}",
                pipeline="study_run",
                params={"study_id": study_id, "node_count": len(nodes)},
                created_at=_now_iso(),
            )
            job_id = job["id"]
            await db.update_job_status(job_id, "running")
        except Exception as je:  # noqa: BLE001
            logger.warning("Could not create job record: %s", je)

        ordered = _topological_sort(nodes, edges)
        loop = asyncio.get_event_loop()
        node_results: dict[str, Any] = {}

        yield _sse({"event": "started", "study_id": study_id,
                    "study_name": study["name"],
                    "node_count": len(ordered), "job_id": job_id})
        logger.info("Starting study run '%s' (%d nodes) — job %s",
                    study["name"], len(ordered), job_id)

        try:
            for node_idx, node in enumerate(ordered):
                nid = node["id"]
                node_label = node.get("label") or nid
                node_type  = node.get("type", "experiment")

                yield _sse({"event": "node_start", "nid": nid, "label": node_label,
                            "type": node_type, "idx": node_idx, "total": len(ordered)})
                logger.info("[%s] Node %d/%d — %s (%s)",
                            study["name"], node_idx + 1, len(ordered), node_label, node_type)

                # Collect upstream results
                predecessors = [e.get("source", "") for e in edges if e.get("target", "") == nid]
                upstream: dict[str, Any] = {
                    pred: node_results[pred].get("result")
                    for pred in predecessors
                    if pred in node_results and node_results[pred].get("status") in ("complete", "corpus")
                }

                # Execute node
                if node_type in _ANNOTATION_TYPES:
                    result: dict[str, Any] = {"status": "annotation", "reason": f"{node_type} node"}
                elif node_type == "corpus":
                    corpus_id = (node.get("params") or {}).get("corpus_id", "")
                    result = {"status": "corpus", "result": {"corpus_id": corpus_id}, "reason": "Corpus source"}
                elif node_type == "pipeline":
                    result = await _run_pipeline_node(node, upstream, db)
                elif node_type == "rag_query":
                    result = await _run_rag_node(node, upstream)
                elif node_type == "compare":
                    result = await _run_compare_node(node, upstream)
                elif node_type == "ai_analysis":
                    result = await _run_ai_analysis_node(node, upstream)
                elif node_type == "report":
                    result = await loop.run_in_executor(None, _run_report_node, node, upstream)
                else:
                    result = await loop.run_in_executor(None, _run_experiment_node, node, upstream)

                node_results[nid] = result
                yield _sse({"event": "node_end", "nid": nid,
                            "status": result["status"],
                            "reason": result.get("reason", "")})

        except Exception as exc:  # noqa: BLE001
            logger.error("Study run '%s' crashed: %s", study["name"], exc)
            yield _sse({"event": "run_error", "message": str(exc)})
            if job_id:
                try:
                    await db.update_job_status(job_id, "failed")
                except Exception:  # noqa: BLE001
                    pass
            return

        # ── Summary ───────────────────────────────────────────────────────
        completed   = sum(1 for r in node_results.values() if r["status"] == "complete")
        skipped     = sum(1 for r in node_results.values() if r["status"] in ("skipped", "pending"))
        annotations = sum(1 for r in node_results.values() if r["status"] in ("annotation", "corpus"))
        errors      = sum(1 for r in node_results.values() if r["status"] == "error")
        final_status = "failed" if errors else "completed"

        logger.info("Study run '%s' done — %d complete, %d errors",
                    study["name"], completed, errors)

        if job_id:
            try:
                await db.update_job_status(job_id, final_status)
                await db._conn.execute(  # noqa: SLF001
                    "UPDATE jobs SET params = ? WHERE id = ?",
                    (json.dumps({"study_id": study_id, "node_count": len(ordered),
                                 "completed": completed, "errors": errors}), job_id),
                )
                await db._conn.commit()  # noqa: SLF001
            except Exception as je:  # noqa: BLE001
                logger.warning("Could not update job record: %s", je)

        yield _sse({"event": "run_complete", "study_id": study_id, "job_id": job_id,
                    "node_count": len(ordered), "completed": completed,
                    "skipped": skipped, "annotations": annotations, "errors": errors,
                    "results": node_results})

    return StreamingResponse(_stream(), media_type="text/event-stream", headers=_SSE_HEADERS)
