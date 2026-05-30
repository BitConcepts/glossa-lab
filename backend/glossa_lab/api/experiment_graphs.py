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
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from glossa_lab import database as _db_mod
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
    notify: bool = False  # send a completion email when finished


async def _maybe_notify_experiment(
    *, exp_id: str, exp_name: str, status: str,
    summary: dict[str, Any], duration_s: float | None,
) -> None:
    """Fire an experiment_complete email to registered recipients only.

    STRICT RULE: emails are ONLY sent to addresses explicitly registered in
    Settings > Notifications > Recipients.  No external address can ever
    receive email — list_active_recipients() is the sole gate.
    """
    try:
        from glossa_lab.notifications import (  # noqa: PLC0415
            format_experiment_complete,
            get_notifier,
        )
        notifier = get_notifier()
        if not notifier.is_configured():
            return
        # STRICT RULE: only registered recipients.
        recipients = await notifier.list_active_recipients()
        if not recipients:
            return
        subject, body_text, body_html = format_experiment_complete(
            name=exp_name, exp_id=exp_id, status=status,
            summary=summary, duration_s=duration_s,
        )
        await notifier.send(
            subject=subject, body_text=body_text, body_html=body_html,
            kind="experiment_complete", item_count=0,
            recipients=recipients,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("experiment notify failed: %s", exc)


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
#
# Architecture: the experiment runs as an asyncio background Task, completely
# decoupled from the HTTP/SSE connection.  If the browser closes the connection
# (sleep, navigation, mobile backgrounding) the Task continues unaffected.
# The SA computation always runs to completion; the job is always marked
# completed or failed.  The SSE generator merely forwards events from a queue.

async def _run_exp_background(
    exp_id: str,
    d: dict[str, Any],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    kwargs: dict[str, Any],
    notify_on_done: bool,
    queue: "asyncio.Queue[str | None]",
) -> None:
    """Execute the experiment graph and put SSE event strings in *queue*.

    None in the queue signals end-of-stream to _stream().

    Key property: runs as asyncio.create_task() so it is NOT cancelled when the
    HTTP client disconnects.  The stall watchdog heartbeat (DB updated_at bump)
    fires inside this task every 30 s, not inside the SSE generator, so the
    watchdog can never kill a job just because the browser went to sleep.
    """

    def _q(data: dict[str, Any]) -> None:
        """Enqueue one SSE event string.  Drop silently if client has disconnected."""
        try:
            queue.put_nowait(_sse(data))
        except asyncio.QueueFull:
            pass

    _t0 = datetime.now(UTC)
    db = _db_mod.get_db()

    try:
        # ── Detect compute device ─────────────────────────────────────────────
        try:
            from glossa_lab.accelerate import gpu_info as _gpu_info  # noqa: PLC0415
            _ginfo = _gpu_info()
            _compute_device = "gpu" if _ginfo.get("cuda") else "cpu"
            _compute_label  = _ginfo.get("tier_name", "CPU")
        except Exception:  # noqa: BLE001
            _compute_device = "cpu"; _compute_label = "CPU"

        # ── VRAM pre-check ────────────────────────────────────────────────────
        _has_sa_node = any(
            (n.get("data") or {}).get("atomicId") in (
                "SADecipher", "IndusConstrainedSA", "IndusSyllabicSA", "BeamDecipher"
            )
            for n in nodes
        )
        if _has_sa_node or _compute_device == "gpu":
            try:
                import torch as _torch  # noqa: PLC0415
                _vram_min = float(
                    __import__("os").environ.get("GLOSSA_VRAM_MIN_FREE_GB", "2.5")
                )
                if _torch.cuda.is_available():
                    _props    = _torch.cuda.get_device_properties(0)
                    _reserved = _torch.cuda.memory_reserved(0)
                    _vram_free = (_props.total_memory - _reserved) / 1024 ** 3
                    if _vram_free < _vram_min:
                        logger.warning(
                            "exp_run '%s' rejected: VRAM %.1f GB free < %.1f GB threshold",
                            exp_id, _vram_free, _vram_min,
                        )
                        _q({
                            "event": "run_error",
                            "message": (
                                f"Insufficient VRAM: {_vram_free:.1f} GB free, "
                                f"need {_vram_min:.1f} GB. "
                                "Another GPU job may still be running. "
                                "Check the Jobs panel and retry when VRAM is available."
                            ),
                            "resource_blocked": True,
                            "vram_free_gb": round(_vram_free, 2),
                            "vram_required_gb": _vram_min,
                        })
                        return
                else:
                    logger.warning(
                        "exp_run '%s': SA node detected but CUDA unavailable — will run on CPU",
                        exp_id,
                    )
            except Exception as _re:  # noqa: BLE001
                logger.debug("VRAM pre-check skipped: %s", _re)

        # ── GPU concurrency guard ─────────────────────────────────────────────
        if db is not None and (_has_sa_node or _compute_device == "gpu"):
            try:
                _max_gpu = int(__import__("os").environ.get("GLOSSA_MAX_CONCURRENT_GPU_JOBS", "1"))
                _gpu_cursor = await db._conn.execute(  # noqa: SLF001
                    "SELECT id, json_extract(params, '$.exp_id') as exp_id FROM jobs "
                    "WHERE pipeline = 'exp_run' AND status = 'running' "
                    "AND json_extract(params, '$.compute_device') = 'gpu'",
                )
                _gpu_running = await _gpu_cursor.fetchall()
                if len(_gpu_running) >= _max_gpu:
                    _blocking_id  = _gpu_running[0]["id"]
                    _blocking_exp = _gpu_running[0]["exp_id"] or _blocking_id
                    logger.warning(
                        "GPU concurrency guard: '%s' rejected (%d/%d GPU slots occupied by %s)",
                        exp_id, len(_gpu_running), _max_gpu, _blocking_exp,
                    )
                    _q({
                        "event": "run_error",
                        "message": (
                            f"{len(_gpu_running)}/{_max_gpu} GPU slot(s) occupied "
                            f"({_blocking_exp} is running). "
                            "Wait for it to finish, abort it, or use the sequential queue. "
                            f"Override limit: set GLOSSA_MAX_CONCURRENT_GPU_JOBS > {_max_gpu}."
                        ),
                        "gpu_blocked": True,
                        "gpu_running": len(_gpu_running),
                        "gpu_limit": _max_gpu,
                        "blocking_job_id": _blocking_id,
                        "blocking_exp_id": _blocking_exp,
                    })
                    return
            except Exception as _ge:  # noqa: BLE001
                logger.warning("GPU concurrency check failed (non-critical): %s", _ge)

        # ── Duplicate-run guard ───────────────────────────────────────────────
        if db is not None:
            try:
                _cursor = await db._conn.execute(  # noqa: SLF001
                    "SELECT id FROM jobs "
                    "WHERE pipeline = 'exp_run' "
                    "AND status = 'running' "
                    "AND json_extract(params, '$.exp_id') = ?",
                    (exp_id,),
                )
                _existing = await _cursor.fetchone()
                if _existing:
                    existing_job_id = _existing[0]
                    logger.warning(
                        "Duplicate exp_run rejected: '%s' already running as job %s",
                        exp_id, existing_job_id,
                    )
                    _q({
                        "event": "run_error",
                        "message": (
                            f"Experiment '{exp_id}' is already running "
                            f"(job {existing_job_id}). "
                            "Wait for it to complete or cancel it before starting again."
                        ),
                        "duplicate": True,
                        "existing_job_id": existing_job_id,
                    })
                    return
            except Exception as _de:  # noqa: BLE001
                logger.warning("Duplicate-run check failed (non-critical): %s", _de)

        # ── Create job record ─────────────────────────────────────────────────
        job_id: str | None = None
        if db is not None:
            try:
                job = await db.create_job(
                    name=f"Exp run: {d.get('name', exp_id)}",
                    pipeline="exp_run",
                    params={
                        "exp_id": exp_id,
                        "node_count": len(nodes),
                        "nodes_done": 0,
                        "compute_device": _compute_device,
                        "compute_device_label": _compute_label,
                    },
                    created_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
                    initial_status="running",  # skip pending — engine must not claim exp_run jobs
                )
                job_id = job["id"]
            except Exception as _je:  # noqa: BLE001
                logger.warning("Could not create job record for exp run: %s", _je)

        if not nodes:
            if job_id and db:
                try: await db.update_job_status(job_id, "completed")
                except Exception: pass  # noqa: BLE001
            if notify_on_done:
                await _maybe_notify_experiment(
                    exp_id=exp_id, exp_name=d.get("name", exp_id),
                    status="completed",
                    summary={"node_count": 0, "job_id": job_id or ""},
                    duration_s=(datetime.now(UTC) - _t0).total_seconds(),
                )
            _q({"event": "run_complete", "exp_id": exp_id,
                "node_count": 0, "status": "complete", "result": {}, "job_id": job_id})
            return

        ordered = _topo_sort(nodes, edges)
        loop = asyncio.get_event_loop()
        res: dict[str, dict[str, Any]] = {}

        _q({"event": "started", "exp_id": exp_id, "job_id": job_id,
            "exp_name": d.get("name", exp_id), "node_count": len(ordered)})
        logger.info(
            "Experiment run '%s' starting (%d nodes) — job %s",
            d.get("name"), len(ordered), job_id,
        )

        try:
            for node_idx, node in enumerate(ordered):
                nid = node["id"]
                ntype, node_params = _node_type_and_params(node)
                node_label = (node.get("data") or {}).get("label") or ntype

                _q({"event": "node_start", "nid": nid, "label": node_label,
                    "type": ntype, "idx": node_idx, "total": len(ordered)})

                # Collect inputs from upstream nodes
                node_inputs: dict[str, Any] = {}
                for e in edges:
                    src = e.get("source", "")
                    sp  = e.get("sourcePort", "")
                    tp  = e.get("targetPort", "")
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
                    node_result: dict[str, Any] = {"error": f"Unknown node type: '{ntype}'"}
                else:
                    try:
                        # Run node in thread-pool; poll every 30 s for pause/cancel.
                        # asyncio.shield keeps the thread alive if this coroutine is
                        # ever cancelled (it won't be, but belt-and-suspenders).
                        future = loop.run_in_executor(
                            None, atomic.fn, node_inputs, params
                        )
                        while True:
                            try:
                                node_result = await asyncio.wait_for(
                                    asyncio.shield(future), timeout=30.0,
                                ) or {}
                                break
                            except asyncio.TimeoutError:
                                # ── Pause / cancel / delete check ─────────
                                if job_id and db:
                                    try:
                                        _sc = await db._conn.execute(  # noqa: SLF001
                                            "SELECT status FROM jobs WHERE id = ?",
                                            (job_id,),
                                        )
                                        _row = await _sc.fetchone()
                                        _stop_status = (
                                            None if _row is None else _row[0]
                                        )
                                        if _stop_status is None or _stop_status in (
                                            "paused", "cancelled", "failed"
                                        ):
                                            _label = _stop_status or "deleted"
                                            logger.info(
                                                "exp_run '%s' job %s %s — stopping",
                                                exp_id, job_id, _label,
                                            )
                                            _q({
                                                "event": "run_error",
                                                "message": f"Job {_label} by user.",
                                                "paused": _stop_status == "paused",
                                                "cancelled": _stop_status in ("cancelled", None),
                                            })
                                            return
                                    except Exception:  # noqa: BLE001
                                        pass

                                # ── Heartbeat + DB touch ──────────────────
                                # This runs inside the background task so it fires
                                # even when the SSE client is disconnected.  The stall
                                # watchdog sees a fresh updated_at and never kills the
                                # job regardless of client state.
                                _q({"event": "heartbeat", "nid": nid,
                                    "idx": node_idx, "total": len(ordered)})
                                if job_id and db:
                                    try:
                                        await db._conn.execute(  # noqa: SLF001
                                            "UPDATE jobs SET updated_at = datetime('now') "
                                            "WHERE id = ?",
                                            (job_id,),
                                        )
                                        await db._conn.commit()  # noqa: SLF001
                                    except Exception:  # noqa: BLE001
                                        pass
                    except Exception as exc:  # noqa: BLE001
                        node_result = {"error": str(exc)}

                res[nid] = node_result
                had_error = "error" in node_result
                _q({"event": "node_end", "nid": nid,
                    "status": "error" if had_error else "complete",
                    "error": node_result.get("error", "")})

                # Advance nodes_done counter + fresh updated_at
                if job_id and db:
                    try:
                        await db._conn.execute(  # noqa: SLF001
                            "UPDATE jobs SET params = json_set(params, '$.nodes_done', ?), "
                            "updated_at = datetime('now') WHERE id = ?",
                            (node_idx + 1, job_id),
                        )
                        await db._conn.commit()  # noqa: SLF001
                    except Exception:  # noqa: BLE001
                        pass

        except Exception as exc:  # noqa: BLE001
            logger.error("Experiment run '%s' crashed: %s", d.get("name"), exc)
            _q({"event": "run_error", "message": str(exc)})
            if job_id and db:
                try: await db.update_job_status(job_id, "failed")
                except Exception: pass  # noqa: BLE001
            if notify_on_done:
                await _maybe_notify_experiment(
                    exp_id=exp_id, exp_name=d.get("name", exp_id),
                    status="failed",
                    summary={"error": str(exc), "job_id": job_id or ""},
                    duration_s=(datetime.now(UTC) - _t0).total_seconds(),
                )
            return

        # ── Collect outputs and finalise ──────────────────────────────────────
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
            merged = res[list(res.keys())[-1]]

        had_errors = any("error" in v for v in res.values())
        final_status = "failed" if had_errors else "completed"
        logger.info("Experiment run '%s' complete (%s)", d.get("name"), final_status)

        if job_id and db:
            try:
                await db.update_job_status(job_id, final_status)
                await db._conn.execute(  # noqa: SLF001
                    "UPDATE jobs SET params = ? WHERE id = ?",
                    (json.dumps({
                        "exp_id": exp_id,
                        "node_count": len(ordered),
                        "nodes_done": len(ordered),
                        "errors": int(had_errors),
                        "compute_device": _compute_device,
                        "compute_device_label": _compute_label,
                    }), job_id),
                )
                await db._conn.commit()  # noqa: SLF001
                result_summary = {
                    k: v for k, v in merged.items()
                    if not isinstance(v, type(None))
                    and not hasattr(v, "unigram_freq")  # skip LM objects
                    and (not isinstance(v, dict) or len(json.dumps(v, default=str)) < 8192)
                }
                await db.store_result(
                    job_id=job_id,
                    data={
                        "exp_id": exp_id,
                        "exp_name": d.get("name", exp_id),
                        "status": final_status,
                        "node_count": len(ordered),
                        "had_errors": had_errors,
                        "result": result_summary,
                    },
                    created_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
                )
            except Exception as _je:  # noqa: BLE001
                logger.warning("Could not update job record: %s", _je)

        if notify_on_done:
            await _maybe_notify_experiment(
                exp_id=exp_id, exp_name=d.get("name", exp_id),
                status=final_status,
                summary={
                    "node_count": len(ordered),
                    "errors": int(had_errors),
                    "job_id": job_id or "",
                    "compute_device": _compute_device,
                },
                duration_s=(datetime.now(UTC) - _t0).total_seconds(),
            )

        _q({"event": "run_complete", "exp_id": exp_id, "job_id": job_id,
            "node_count": len(ordered), "status": "complete",
            "result": merged, "node_results": res})

    finally:
        # Always signal stream end — success, error, or unexpected cancellation.
        try:
            queue.put_nowait(None)
        except asyncio.QueueFull:
            pass


@router.post("/{exp_id}/run")
async def run_experiment(exp_id: str, body: RunGraphBody) -> StreamingResponse:
    """Stream graph experiment execution as SSE.

    The experiment runs as a background asyncio.Task completely decoupled from
    the HTTP connection.  Browser disconnect / sleep / navigation never stops
    the computation.  The SA node always runs to completion.
    """
    d = get_graph_experiment(exp_id)
    if d is None:
        raise HTTPException(status_code=404, detail=f"Graph experiment '{exp_id}' not found")

    nodes = d.get("nodes", [])
    edges = d.get("edges", [])
    kwargs = body.kwargs or {}
    notify_on_done = bool(body.notify)

    # Bounded queue: events are forwarded to the SSE client when connected.
    # If the client disconnects, _run_exp_background() silently drops events
    # once the queue fills — but the computation keeps running.
    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=512)

    asyncio.create_task(
        _run_exp_background(exp_id, d, nodes, edges, kwargs, notify_on_done, queue),
        name=f"exp-run-{exp_id}",
    )

    async def _stream() -> AsyncGenerator[str, None]:
        """Forward queue events to the SSE client until None (end sentinel)."""
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item

    return StreamingResponse(_stream(), media_type="text/event-stream", headers=_SSE_HEADERS)
