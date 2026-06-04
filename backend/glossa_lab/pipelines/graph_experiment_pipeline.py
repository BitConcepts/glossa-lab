"""Graph experiment pipeline — executes saved graph experiments as background jobs.

Registered as ``graph_experiment`` in the engine so that jobs created by
``queue_graph_experiment()`` (e.g. from the Phase Advancer) are picked up
and executed by the background job engine rather than silently failing.

Unlike the SSE-streamed ``/experiment-graphs/{id}/run`` endpoint which
streams node-by-node progress to a connected browser, this pipeline runs
the full graph synchronously in a worker thread and stores the result on
the job record — suitable for fire-and-forget queuing from the Phase Guide.
"""
from __future__ import annotations

import logging

from glossa_lab.engine import register_pipeline

_log = logging.getLogger("glossa_lab.pipelines.graph_experiment")


@register_pipeline("graph_experiment")
async def run_graph_experiment(params: dict) -> dict:
    """Execute a saved graph experiment and return its output dict.

    Expected params:
      experiment_id: str   — ID of the graph experiment to run
      **kwargs             — forwarded to execute_graph as kwargs overrides
    """
    import asyncio as _asyncio  # noqa: PLC0415
    from glossa_lab.experiment_graph import execute_graph, get_graph_experiment  # noqa: PLC0415

    exp_id = (params or {}).get("experiment_id", "")
    if not exp_id:
        return {"error": "No experiment_id in job params", "status": "failed"}

    graph_def = get_graph_experiment(exp_id)
    if graph_def is None:
        _log.error("Graph experiment '%s' not found in registry", exp_id)
        return {"error": f"Graph experiment '{exp_id}' not found", "status": "failed"}

    # Extra kwargs — everything except experiment_id
    kwargs = {k: v for k, v in params.items() if k != "experiment_id"}

    _log.info("graph_experiment pipeline: running '%s' (%d extra kwargs)",
              exp_id, len(kwargs))

    loop = _asyncio.get_event_loop()
    try:
        result: dict = await loop.run_in_executor(
            None, lambda: execute_graph(graph_def, kwargs=kwargs or None)
        )
    except Exception as exc:  # noqa: BLE001
        _log.error("graph_experiment '%s' raised: %s", exp_id, exc)
        return {"error": str(exc), "status": "failed", "exp_id": exp_id}

    had_errors = any("error" in v for v in result.values()
                     if isinstance(v, dict))
    _log.info("graph_experiment '%s' finished (had_errors=%s)", exp_id, had_errors)
    return {
        "status": "failed" if had_errors else "completed",
        "exp_id": exp_id,
        "exp_name": graph_def.get("name", exp_id),
        **result,
    }
