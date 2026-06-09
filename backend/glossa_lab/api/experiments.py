"""Experiments discovery and management API.

Endpoints:
  GET  /experiments              -- list all discovered experiments
  GET  /experiments/{id}         -- get experiment metadata
  POST /experiments/{id}/run     -- run synchronously, return JSON result
  GET  /experiments/{id}/stream  -- SSE: run with heartbeat + final result
  POST /experiments/import       -- import a .py file
  POST /experiments/{id}/duplicate -- duplicate an experiment
  DELETE /experiments/{id}       -- delete an experiment file
  POST /experiments/generate     -- AI-generate a new experiment
  POST /experiments/{id}/summarize -- AI-generate a structured summary
"""

from __future__ import annotations

import asyncio
import json
import threading
import time
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from glossa_lab.experiment_base import (
    create_experiment_from_prompt,
    delete_experiment_file,
    duplicate_experiment_file,
    get_experiment,
    import_experiment_file,
    invalidate_cache,
)
from glossa_lab.experiment_graph import (
    get_graph_experiment,
    list_graph_experiments,
    queue_graph_experiment,
)

router = APIRouter()


@router.get("/experiments/metadata")
async def get_experiments_metadata() -> list[dict[str, Any]]:
    """Return experiment ledger metadata for all registered nodes.

    Merges the static experiment_ledger.json with live ATOMIC_NODES
    registration data. Used by the frontend ExperimentRegistry component.
    """
    from glossa_lab.experiment_graph import get_experiment_metadata  # noqa: PLC0415
    return get_experiment_metadata()


@router.get("/experiments")
async def list_experiments() -> list[dict[str, Any]]:
    """Return graph experiments only (H16 compliance).

    Python ExperimentBase subclasses are no longer user-visible.
    All experiments are defined as graph specs in experiments/graphs/.
    """
    return [
        {
            "id":             spec["id"],
            "name":           spec["name"],
            "category":       "Graph Experiments",
            "description":    spec["description"],
            "estimated_time": "varies",
            "requires_key":   None,
            "command":        "",
            "results_file":   None,
            "report_schema":  None,
            "params_schema":  {"type": "object", "properties": {}},
            "source_file":    f"experiments/graphs/{spec['id']}.json",
            "custom":         False,
            "node_count":     spec.get("node_count", 0),
            "edge_count":     spec.get("edge_count", 0),
        }
        for spec in list_graph_experiments()
    ]


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
    """Execute an experiment and return the result.

    Tries graph experiments first (queue as a Job); falls back to legacy
    ExperimentBase subclasses for backwards compatibility.
    """
    # ── Graph experiment path (preferred) ─────────────────────────────────
    graph_spec = get_graph_experiment(experiment_id)
    if graph_spec is not None:
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        job = await queue_graph_experiment(
            experiment_id, db=db, params=body.kwargs,
        ) if db is not None else None
        if job is not None:
            return {
                "experiment_id": experiment_id,
                "job_id": job["id"],
                "status": "queued",
            }
        # db unavailable or queue failed — fall through to legacy path

    # ── Legacy ExperimentBase path ────────────────────────────────────────
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


@router.post("/experiments/{experiment_id}/queue", status_code=202)
async def queue_experiment(experiment_id: str, body: RunRequest) -> dict[str, Any]:
    """Queue a graph experiment as a background Job. Returns {job_id, experiment_id}.

    Non-blocking — the job engine picks it up asynchronously.
    """
    graph_spec = get_graph_experiment(experiment_id)
    if graph_spec is None:
        raise HTTPException(
            status_code=404,
            detail=f"Graph experiment '{experiment_id}' not found",
        )
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    job = await queue_graph_experiment(
        experiment_id, db=db, params=body.kwargs,
    )
    if job is None:
        raise HTTPException(status_code=503, detail="Failed to create job")
    return {
        "experiment_id": experiment_id,
        "job_id": job["id"],
        "queued": True,
    }


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


@router.post("/experiments/{experiment_id}/summarize")
async def summarize_experiment(experiment_id: str) -> dict[str, Any]:
    """Use AI to generate a structured summary of an experiment.

    Returns {abstract, hypothesis, highlights, insights, next_steps, suggested_actions,
    experiment_id, name, category, description}.
    """
    import asyncio
    import json

    from glossa_lab.ai_utils import call_llm

    cls = get_experiment(experiment_id)
    if cls is None:
        raise HTTPException(status_code=404, detail=f"Experiment '{experiment_id}' not found")

    meta = cls.to_dict()

    try:
        from glossa_lab.config import get_project_config  # noqa: PLC0415
        _project_name = get_project_config().project_name
    except Exception:
        _project_name = "Indus Script"

    system = (
        f"You are a research assistant summarizing scientific experiments on the {_project_name} "
        "and ancient script analysis. Return ONLY valid JSON with these exact fields:\n"
        '{"abstract": "2-3 sentence summary", '
        '"hypothesis": "the hypothesis being tested or null", '
        '"highlights": ["key finding 1", "key finding 2"], '
        '"insights": "what results mean for Indus Script research", '
        '"next_steps": ["recommended follow-up 1", "recommended follow-up 2"], '
        '"suggested_actions": [{"label": "Create Follow-up Study", '
        '"action": "create_study", "hint": "brief description"}, '
        '{"label": "Generate Experiment", "action": "generate_experiment", '
        '"hint": "brief description"}]}'
    )
    user = (
        f"Experiment: {meta.get('name')}\n"
        f"Category: {meta.get('category')}\n"
        f"Description: {meta.get('description')}\n"
        f"Estimated time: {meta.get('estimated_time')}\n"
        f"Results file: {meta.get('results_file', 'N/A')}\n\n"
        "Summarize this experiment and suggest research next steps."
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
        result["experiment_id"] = experiment_id
        result["name"] = meta.get("name")
        result["category"] = meta.get("category")
        result["description"] = meta.get("description")
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/experiments/reload")
async def reload_experiments() -> dict[str, Any]:
    """Invalidate the discovery cache and re-scan."""
    invalidate_cache()
    experiments = list_graph_experiments()
    return {"reloaded": True, "count": len(experiments)}


# ── SSE streaming run ──────────────────────────────────────────────


def _sse(event: str, data: dict[str, Any]) -> str:
    """Format a Server-Sent Events message."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def _stream_experiment(
    experiment_id: str,
    kwargs: dict[str, Any],
) -> AsyncGenerator[str, None]:
    """Run an experiment in a thread and stream SSE events.

    Events:
      started   -- experiment is running
      heartbeat -- still running (every 3 s)
      complete  -- finished successfully; data includes result
      error     -- failed; data includes message
    """
    cls = get_experiment(experiment_id)
    if cls is None:
        yield _sse("error", {"message": f"Experiment '{experiment_id}' not found"})
        return

    result_holder: dict[str, Any] = {}
    error_holder: dict[str, str] = {}
    done_event = threading.Event()

    def _run() -> None:
        try:
            instance = cls()
            result_holder["result"] = instance.run(**kwargs)
        except NotImplementedError:
            error_holder["message"] = (
                f"Experiment '{experiment_id}' has no run() implementation. "
                "Use the CLI command instead."
            )
        except Exception as exc:  # noqa: BLE001
            error_holder["message"] = str(exc)
        finally:
            done_event.set()

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    yield _sse("started", {"experiment_id": experiment_id, "timestamp": time.time()})

    # Stream heartbeats until done
    loop = asyncio.get_event_loop()
    while not done_event.is_set():
        await loop.run_in_executor(None, done_event.wait, 3.0)
        if not done_event.is_set():
            yield _sse("heartbeat", {"elapsed_s": round(time.time(), 1)})

    thread.join(timeout=5)

    if error_holder:
        yield _sse("error", {"message": error_holder["message"]})
    else:
        yield _sse(
            "complete",
            {"experiment_id": experiment_id, "result": result_holder.get("result")},
        )


_VALID_BUILTIN_LANGUAGES = {
    "hebrew", "geez", "phoenician", "sumerian",
    "dravidian", "south_dravidian", "kannada", "telugu",
    "pali", "sanskrit", "coptic", "linear_b",
    "meroitic", "proto_sinaitic", "nw_semitic",
    "hieroglyphic_luwian",
}

_VALID_BUILTIN_CORPORA = {
    "indus", "indus_cisi", "indus_m77",
    "hebrew", "geez", "phoenician", "nw_semitic", "ugaritic",
    "meroitic", "proto_sinaitic", "linear_b", "sanskrit", "dravidian",
}


@router.post("/experiments/build-sa")
async def build_sa_experiment(body: dict[str, Any]) -> dict[str, Any]:
    """Build and register a new SA multi-language comparison graph experiment.

    Body: {corpus, languages, name?, n_seeds?, max_iterations?}
    - corpus: BuiltinCorpus name (e.g. 'indus_cisi')
    - languages: comma-separated language list (e.g. 'dravidian,sanskrit,hebrew')
    - name: optional human-readable name
    - n_seeds: seeds per language (default 3)
    - max_iterations: SA iterations (default 5000)

    Returns: {experiment_id, name, graph_file, ok}
    """
    import re as _re  # noqa: PLC0415
    import time as _t  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    corpus = str(body.get("corpus", "indus_cisi")).strip().lower()
    languages_raw = str(body.get("languages", "dravidian,sanskrit")).strip()
    name = str(body.get("name", "")).strip()
    n_seeds = max(1, int(body.get("n_seeds", 3)))
    max_iterations = max(100, int(body.get("max_iterations", 5000)))

    # Normalize common AI-generated corpus name variations
    _CORPUS_ALIASES: dict[str, str] = {
        # indus variants
        "indus script": "indus_cisi",
        "indus_script": "indus_cisi",
        "indus-script": "indus_cisi",
        "indus valley": "indus_cisi",
        "indus valley civilization": "indus_cisi",
        "indus valley civilisation": "indus_cisi",
        "the indus valley civilization": "indus_cisi",
        "ivc": "indus_cisi",
        "harappan": "indus_cisi",
        "harappa": "indus_cisi",
        "cisi": "indus_cisi",
        "indus parpola": "indus_cisi",
        "indus-cisi": "indus_cisi",
        "indus-script-cisi": "indus_cisi",
        # m77 variants
        "m77": "indus_m77",
        "mahadevan": "indus_m77",
        "mahadevan_1977": "indus_m77",
        "mahadevan 1977": "indus_m77",
        # nw_semitic / fuls variants
        "fuls": "nw_semitic",
        "fuls_nw_semitic": "nw_semitic",
        "northwest semitic": "nw_semitic",
        "north-west semitic": "nw_semitic",
    }
    corpus = _CORPUS_ALIASES.get(corpus, corpus)

    if corpus not in _VALID_BUILTIN_CORPORA:
        return {"ok": False, "error": f"Unknown corpus '{corpus}'. Valid: {', '.join(sorted(_VALID_BUILTIN_CORPORA))}"}

    # Normalize multi-word language names before splitting
    _LANG_NORMALIZATIONS = {
        "nw semitic": "nw_semitic", "proto sinaitic": "proto_sinaitic",
        "south dravidian": "south_dravidian", "old hebrew": "old_hebrew",
        "hieroglyphic luwian": "hieroglyphic_luwian", "linear b": "linear_b",
        "middle indo aryan": "pali",
    }
    _norm_raw = languages_raw.lower()
    for phrase, replacement in _LANG_NORMALIZATIONS.items():
        _norm_raw = _norm_raw.replace(phrase, replacement)
    lang_list = [l.strip() for l in _re.split(r"[,;\s]+", _norm_raw) if l.strip()]
    invalid = [l for l in lang_list if l not in _VALID_BUILTIN_LANGUAGES]
    if invalid:
        return {"ok": False, "error": f"Unknown language(s): {', '.join(invalid)}. Valid: {', '.join(sorted(_VALID_BUILTIN_LANGUAGES))}"}
    if not lang_list:
        return {"ok": False, "error": "No languages specified."}

    if not name:
        name = f"SA: {corpus} vs {' / '.join(lang_list)}"

    # ── Deduplication: return existing experiment if same name already exists ──
    graphs_dir_check = Path(__file__).resolve().parents[1] / "experiments" / "graphs"
    if graphs_dir_check.exists():
        for existing in graphs_dir_check.glob("*.json"):
            try:
                existing_data = __import__("json").loads(existing.read_text(encoding="utf-8"))
                if existing_data.get("name", "").strip().lower() == name.lower():
                    return {
                        "ok": True,
                        "experiment_id": existing_data["id"],
                        "name": existing_data["name"],
                        "graph_file": existing.name,
                        "n_languages": len(lang_list),
                        "languages": lang_list,
                        "corpus": corpus,
                        "existing": True,
                    }
            except Exception:  # noqa: BLE001
                pass

    # Generate unique experiment ID
    slug = _re.sub(r"[^a-z0-9]+", "_", f"{corpus}_sa_{'_vs_'.join(lang_list)}").strip("_")
    exp_id = slug  # stable ID — no timestamp suffix
    # If the slug-based ID file somehow exists (different name), add suffix
    graphs_dir_id_check = Path(__file__).resolve().parents[1] / "experiments" / "graphs" / f"{slug}.json"
    if graphs_dir_id_check.exists():
        exp_id = f"{slug}_{int(_t.time())}"


    graph = {
        "id": exp_id,
        "name": name,
        "description": f"Auto-generated SA multi-language comparison. Corpus: {corpus}. Languages: {', '.join(lang_list)}. Seeds: {n_seeds}. Max iterations: {max_iterations}.",
        "nodes": [
            {"id": "corpus", "type": "expNode",
             "position": {"x": 60, "y": 200},
             "data": {"atomicId": "BuiltinCorpus", "label": f"Corpus: {corpus}",
                      "params": {"corpus": corpus}}},
            {"id": "multi_sa", "type": "expNode",
             "position": {"x": 340, "y": 200},
             "data": {"atomicId": "SAMultiComparison",
                      "label": f"SA vs {' / '.join(lang_list)}",
                      "params": {"languages": ",".join(lang_list),
                                 "n_seeds": n_seeds,
                                 "max_iterations": max_iterations}}},
            {"id": "merge", "type": "expNode",
             "position": {"x": 660, "y": 200},
             "data": {"atomicId": "Merger", "label": "Collect results", "params": {}}},
            {"id": "out", "type": "expNode",
             "position": {"x": 920, "y": 200},
             "data": {"atomicId": "JSONExport",
                      "label": "Export results",
                      "params": {"filename": f"{exp_id}.json"}}},
        ],
        "edges": [
            {"id": "e1", "source": "corpus", "target": "multi_sa",
             "sourcePort": "sequences", "targetPort": "sequences"},
            {"id": "e2", "source": "multi_sa", "target": "merge",
             "sourcePort": "comparison_results", "targetPort": "a"},
            {"id": "e3", "source": "multi_sa", "target": "merge",
             "sourcePort": "best_language", "targetPort": "b"},
            {"id": "e4", "source": "multi_sa", "target": "merge",
             "sourcePort": "best_consistency", "targetPort": "c"},
            {"id": "e5", "source": "merge", "target": "out",
             "sourcePort": "json", "targetPort": "data"},
        ],
    }

    graphs_dir = Path(__file__).resolve().parents[1] / "experiments" / "graphs"
    graphs_dir.mkdir(parents=True, exist_ok=True)
    graph_file = graphs_dir / f"{exp_id}.json"
    graph_file.write_text(
        __import__("json").dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    # Invalidate graph experiment cache so the new experiment appears immediately
    try:
        from glossa_lab.experiment_graph import _invalidate  # noqa: PLC0415
        _invalidate()
    except Exception:  # noqa: BLE001
        pass

    return {
        "ok": True,
        "experiment_id": exp_id,
        "name": name,
        "graph_file": str(graph_file.name),
        "n_languages": len(lang_list),
        "languages": lang_list,
        "corpus": corpus,
    }


@router.get("/experiments/{experiment_id}/stream")
async def stream_experiment(experiment_id: str) -> StreamingResponse:
    """SSE endpoint: run experiment and stream progress events.

    Use with EventSource in the browser. Events: started, heartbeat, complete, error.
    """
    return StreamingResponse(
        _stream_experiment(experiment_id, {}),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
