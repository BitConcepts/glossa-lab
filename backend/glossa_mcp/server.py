"""Glossa Lab MCP server.

Exposes Glossa Lab backend operations as MCP tools so Warp's Oz agent can
query and control the server directly without manual API calls.

Configuration:
  GLOSSA_BASE_URL  — base URL of the running Glossa Lab backend
                     (default: http://127.0.0.1:8001)

Run:
  python backend/glossa_mcp/server.py
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# ── Config ───────────────────────────────────────────────────────────────────

BASE_URL = os.environ.get("GLOSSA_BASE_URL", "http://127.0.0.1:8001")
_REPO = Path(__file__).resolve().parent.parent.parent
_TIMEOUT = 30.0

mcp = FastMCP(
    "glossa-lab",
    instructions=(
        "Tools for controlling and querying the Glossa Lab research backend. "
        "The backend runs at " + BASE_URL + ". "
        "Use get_status to check server health before other calls. "
        "Use list_jobs / get_job to monitor pipeline execution. "
        "Use run_experiment to launch graph experiments as background jobs. "
        "Use start_research_loop to mine new insights (fires in background). "
        "Use run_foundation_check to validate research data integrity."
    ),
)


def _get() -> httpx.Client:
    """Return a short-lived sync httpx client."""
    return httpx.Client(base_url=BASE_URL, timeout=_TIMEOUT)


def _fmt(data: Any) -> str:
    """Return compact JSON string suitable for an MCP tool response."""
    return json.dumps(data, ensure_ascii=False, default=str)


def _err(exc: Exception) -> str:
    return json.dumps({"error": str(exc), "type": type(exc).__name__})


# ── 1. Status & health ───────────────────────────────────────────────────────

@mcp.tool()
def get_status() -> str:
    """Return Glossa Lab server health, version, uptime, job counts, and pipeline list.

    Use this as a first call to confirm the server is running.
    """
    try:
        with _get() as c:
            r = c.get("/api/v1/status")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_system_metrics() -> str:
    """Return live hardware metrics: CPU %, RAM GB, GPU VRAM usage, disk, network.

    Use this to check if there is enough VRAM/RAM before launching GPU experiments.
    """
    try:
        with _get() as c:
            r = c.get("/api/v1/system/metrics")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


# ── 2. Job management ────────────────────────────────────────────────────────

@mcp.tool()
def list_jobs(status: str = "") -> str:
    """List all pipeline jobs.

    Args:
        status: Optional filter — one of: pending, running, completed, failed, cancelled.
                Leave empty to return all jobs.
    """
    try:
        with _get() as c:
            r = c.get("/api/v1/jobs")
            r.raise_for_status()
            jobs = r.json()
            if status:
                jobs = [j for j in jobs if j.get("status") == status]
            return _fmt(jobs)
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_job(job_id: str) -> str:
    """Get full details of a single job by ID.

    Args:
        job_id: The job UUID (full or first 8+ characters).
    """
    try:
        with _get() as c:
            r = c.get(f"/api/v1/jobs/{job_id}")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_job_results(job_id: str) -> str:
    """Return the stored result data for a completed job.

    Args:
        job_id: The completed job UUID.
    """
    try:
        with _get() as c:
            r = c.get(f"/api/v1/jobs/{job_id}/results")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def create_job(name: str, pipeline: str, params_json: str = "{}") -> str:
    """Submit a new pipeline job.

    Args:
        name: Human-readable job name.
        pipeline: Pipeline identifier (e.g. block_entropy, decipher, hypothesis).
        params_json: JSON string of pipeline parameters (default: empty object).
    """
    try:
        params = json.loads(params_json) if params_json.strip() else {}
        with _get() as c:
            r = c.post(
                "/api/v1/jobs",
                json={"name": name, "pipeline": pipeline, "params": params},
            )
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def cancel_job(job_id: str) -> str:
    """Cancel or delete a job (pending or running).

    Args:
        job_id: The job UUID to cancel.
    """
    try:
        with _get() as c:
            r = c.delete(f"/api/v1/jobs/{job_id}")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


# ── 3. Experiments ───────────────────────────────────────────────────────────

@mcp.tool()
def list_experiments() -> str:
    """Return all graph experiment definitions (id, name, description, node/edge counts).

    These are the experiments visible in the Experiments tab of the Glossa Lab UI.
    """
    try:
        with _get() as c:
            r = c.get("/api/v1/experiment-graphs")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_experiment(experiment_id: str) -> str:
    """Return the full graph definition of an experiment (nodes, edges, params).

    Args:
        experiment_id: The experiment ID (e.g. phase_32_t4_sa_decipher).
    """
    try:
        with _get() as c:
            r = c.get(f"/api/v1/experiment-graphs/{experiment_id}")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def run_experiment(experiment_id: str, kwargs_json: str = "{}") -> str:
    """Launch a graph experiment via the SSE run endpoint and return the final result.

    The experiment executes synchronously (this call blocks until all nodes
    complete or an error occurs).  A Job record is created server-side and
    appears in the Jobs panel automatically.

    Args:
        experiment_id: The experiment ID to run.
        kwargs_json: Optional JSON string of override kwargs (default: empty object).
    """
    try:
        kwargs = json.loads(kwargs_json) if kwargs_json.strip() else {}
        # Use a long timeout — SA nodes can run for hours on large sign inventories.
        with httpx.Client(base_url=BASE_URL, timeout=7200.0) as c:
            with c.stream(
                "POST",
                f"/api/v1/experiment-graphs/{experiment_id}/run",
                json={"kwargs": kwargs},
            ) as resp:
                resp.raise_for_status()
                last_event: dict[str, Any] | None = None
                for line in resp.iter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = json.loads(line[6:])
                    evt = data.get("event", "")
                    if evt == "run_complete":
                        return _fmt(data)
                    if evt == "run_error":
                        return _fmt(data)
                    last_event = data
        return _fmt(last_event or {"error": "No SSE events received"})
    except Exception as e:
        return _err(e)


# ── 4. Foundation check ──────────────────────────────────────────────────────

@mcp.tool()
def run_foundation_check() -> str:
    """Run all foundation checks and return pass/fail/warn status per check.

    Checks: Holdat corpus integrity, INDUS_FINAL_ANCHORS, Parpola phonemes,
    iconographic anchors, CISI corpus, phase result files, crosswalk, citations.

    Returns verdict (PASS/FAIL/WARN) and per-check details.
    This operation reads files from disk — no network or GPU required.
    """
    try:
        with httpx.Client(base_url=BASE_URL, timeout=90.0) as c:
            r = c.get("/api/v1/research/foundation-check")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


# ── 5. Research loop ─────────────────────────────────────────────────────────

@mcp.tool()
def start_research_loop(max_cycles: int = 15) -> str:
    """Start the research loop in the background and return immediately.

    The loop mines the Holdat corpus for gaps, cross-references CrossRef,
    generates anchor candidates, and saves them to outputs/anchor_staging.json.

    A Job record is created in the database (pipeline=research_loop).
    Use get_research_loop_status or list_jobs(status='running') to monitor.

    Args:
        max_cycles: Maximum number of mining cycles to run (1–100, default 15).
    """
    def _fire():
        try:
            # The endpoint is SSE; open with no timeout and consume silently
            with httpx.Client(base_url=BASE_URL, timeout=None) as c:
                with c.stream(
                    "POST",
                    "/api/v1/research-loop/start",
                    params={"max_cycles": max_cycles},
                ) as resp:
                    for _ in resp.iter_lines():
                        pass  # consume SSE stream until server closes it
        except Exception:
            pass  # daemon thread — errors are non-fatal

    t = threading.Thread(target=_fire, daemon=True)
    t.start()
    return _fmt({
        "status": "started",
        "max_cycles": max_cycles,
        "message": (
            f"Research loop started in background ({max_cycles} cycles). "
            "A Job record will appear in list_jobs(). "
            "Use get_research_loop_status() to check progress."
        ),
    })


@mcp.tool()
def get_research_loop_status() -> str:
    """Return the current state of the research loop (running/idle, cycle count, etc.)."""
    try:
        with _get() as c:
            r = c.get("/api/v1/research-loop/status")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def stop_research_loop() -> str:
    """Request a graceful stop of the research loop at the end of the current cycle."""
    try:
        with _get() as c:
            r = c.post("/api/v1/research-loop/stop")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_research_loop_results() -> str:
    """Return the full results from the last completed research loop run."""
    try:
        with _get() as c:
            r = c.get("/api/v1/research-loop/results")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_anchor_staging(max_candidates: int = 50) -> str:
    """Read the anchor staging file written by the research loop.

    Returns up to max_candidates anchor candidates sorted by score.
    File location: outputs/anchor_staging.json

    Args:
        max_candidates: Maximum number of candidates to return (default 50).
    """
    try:
        staging = _REPO / "outputs" / "anchor_staging.json"
        if not staging.exists():
            return _fmt({"error": "anchor_staging.json not found — run start_research_loop first"})
        data = json.loads(staging.read_text(encoding="utf-8"))
        candidates = data.get("candidates", [])
        # Sort by score descending if available
        if candidates and isinstance(candidates[0], dict) and "score" in candidates[0]:
            candidates = sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)
        return _fmt({
            "source": str(staging),
            "run_id": data.get("run_id"),
            "generated_at": data.get("generated_at"),
            "gap_type": data.get("gap_type"),
            "total_candidates": len(candidates),
            "candidates": candidates[:max_candidates],
        })
    except Exception as e:
        return _err(e)


# ── 6. Discovery items ───────────────────────────────────────────────────────

@mcp.tool()
def list_discovery_items(
    topic: str = "",
    kind: str = "",
    status: str = "",
    limit: int = 30,
) -> str:
    """Return discovery items (papers, tools, preprints) from the research feed.

    Args:
        topic: Filter by topic (e.g. indus_script, dravidian, cryptography).
        kind:  Filter by kind (e.g. paper, tool, preprint).
        status: Filter by curation status (e.g. new, saved, reviewed, dismissed).
        limit: Maximum items to return (default 30).
    """
    try:
        params: dict[str, Any] = {"limit": limit, "offset": 0}
        if topic:
            params["topic"] = topic
        if kind:
            params["kind"] = kind
        if status:
            params["status"] = status
        with _get() as c:
            r = c.get("/api/v1/discovery/items", params=params)
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_discovery_stats(group: str = "status") -> str:
    """Return grouped counts of discovery items.

    Args:
        group: Group by field — one of: status, kind, topic, source (default: status).
    """
    try:
        with _get() as c:
            r = c.get("/api/v1/discovery/stats", params={"group": group})
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def trigger_discovery_fetch(topics: str = "", sources: str = "") -> str:
    """Trigger a discovery fetch job to pull new papers/tools from external sources.

    Returns a job acknowledgement. The fetch runs as a background job.

    Args:
        topics:  Comma-separated topic IDs to fetch (empty = all configured topics).
        sources: Comma-separated source IDs to query (empty = all configured sources).
    """
    try:
        payload: dict[str, Any] = {}
        if topics:
            payload["topics"] = [t.strip() for t in topics.split(",") if t.strip()]
        if sources:
            payload["sources"] = [s.strip() for s in sources.split(",") if s.strip()]
        with _get() as c:
            r = c.post("/api/v1/discovery/fetch", json=payload)
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def update_discovery_item_status(item_id: str, status: str, notes: str = "") -> str:
    """Mark a discovery item as reviewed, saved, or dismissed.

    Args:
        item_id: The item UUID.
        status:  New status — one of: new, saved, reviewed, dismissed.
        notes:   Optional curator notes.
    """
    try:
        payload: dict[str, Any] = {"status": status}
        if notes:
            payload["notes"] = notes
        with _get() as c:
            r = c.post(f"/api/v1/discovery/items/{item_id}/status", json=payload)
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


# ── 7. Dashboard / insights ──────────────────────────────────────────────────

@mcp.tool()
def get_latest_insight() -> str:
    """Return the most recent AI-generated research insight from the server cache.

    This is a fast read — it returns the cached insight without calling the LLM.
    Returns null if no insight has been generated yet in this session.
    """
    try:
        with _get() as c:
            r = c.get("/api/v1/dashboard/latest-insight")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_dashboard_highlights(include_ai: bool = False, days: int = 14) -> str:
    """Return dashboard highlights: recent discovery items, top kinds, impact suggestions.

    Args:
        include_ai: Set True to also generate a fresh AI insight (burns LLM tokens).
        days:       Look-back window in days (default 14).
    """
    try:
        params: dict[str, Any] = {"days": days}
        if include_ai:
            params["include_ai"] = "true"
        with httpx.Client(base_url=BASE_URL, timeout=120.0) as c:
            r = c.get("/api/v1/dashboard/highlights", params=params)
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


# ── 8. Anchor sets ───────────────────────────────────────────────────────────

@mcp.tool()
def list_anchor_sets(corpus_id: str = "") -> str:
    """List all saved anchor sets (verified sign → reading mappings).

    Args:
        corpus_id: Filter by corpus ID (empty = all anchor sets).
    """
    try:
        params: dict[str, Any] = {}
        if corpus_id:
            params["corpus_id"] = corpus_id
        with _get() as c:
            r = c.get("/api/v1/anchor-sets", params=params)
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_anchor_set(anchor_set_id: str) -> str:
    """Return full details of one anchor set including all cipher→reading pairs.

    Args:
        anchor_set_id: The anchor set UUID.
    """
    try:
        with _get() as c:
            r = c.get(f"/api/v1/anchor-sets/{anchor_set_id}")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def create_anchor_set(
    name: str,
    description: str = "",
    corpus_id: str = "",
    language: str = "",
    pairs_json: str = "[]",
) -> str:
    """Create a new anchor set with cipher→reading pairs.

    Args:
        name:        Human-readable name for the anchor set.
        description: Optional description.
        corpus_id:   Corpus this set applies to (optional).
        language:    Target language code (optional).
        pairs_json:  JSON array of {cipher, target, confidence, note} objects.
    """
    try:
        pairs = json.loads(pairs_json) if pairs_json.strip() else []
        payload: dict[str, Any] = {
            "name": name,
            "description": description,
            "language": language,
            "pairs": pairs,
        }
        if corpus_id:
            payload["corpus_id"] = corpus_id
        with _get() as c:
            r = c.post("/api/v1/anchor-sets", json=payload)
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


# ── 9. Reports & results ─────────────────────────────────────────────────────

@mcp.tool()
def list_reports() -> str:
    """List all available result files in the reports and outputs directories.

    Returns file names, sizes, and modification times.
    """
    try:
        with _get() as c:
            r = c.get("/api/v1/reports")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_report(report_name: str) -> str:
    """Return the JSON contents of a named report/result file.

    Args:
        report_name: File name (without path) as returned by list_reports,
                     e.g. 'phase_32_t4_result.json' or 'INDUS_FINAL_ANCHORS.json'.
    """
    try:
        with httpx.Client(base_url=BASE_URL, timeout=60.0) as c:
            r = c.get(f"/api/v1/reports/{report_name}")
            r.raise_for_status()
            return _fmt(r.json())
    except Exception as e:
        return _err(e)


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
