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
    list_discovered_experiments,
)

router = APIRouter()


@router.get("/experiments")
async def list_experiments() -> list[dict[str, Any]]:
    """Return all discovered experiments with metadata."""
    return list_discovered_experiments()


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
    """Execute an experiment and return the result."""
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


@router.post("/experiments/reload")
async def reload_experiments() -> dict[str, Any]:
    """Invalidate the discovery cache and re-scan."""
    invalidate_cache()
    experiments = list_discovered_experiments()
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
