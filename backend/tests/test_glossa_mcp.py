"""Tests for the Glossa Lab MCP server (backend/glossa_mcp/server.py).

TEST-MCP-001  Every tool formats a happy-path response from the backend JSON.
TEST-MCP-002  Tools send the expected method/path/params/body (request formation).
TEST-MCP-003  Backend errors surface as clean JSON error objects (never raise).
TEST-MCP-004  _err helper formats exceptions as {error, type} JSON.
TEST-MCP-005  Drift guard: every /api/v1 route the MCP source calls exists
              in the live FastAPI route table (method + path shape).
TEST-MCP-006  Tool inventory: the Indus evidence + foundation-status tools
              are registered alongside the original tool set.

The HTTP layer is mocked with httpx.MockTransport — no live server needed.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import httpx
import pytest

from glossa_mcp import server

# ── Mock transport ───────────────────────────────────────────────────────────

CANNED: dict[tuple[str, str], object] = {
    ("GET", "/api/v1/status"): {"status": "ok", "version": "test"},
    ("GET", "/api/v1/system/metrics"): {"cpu_percent": 1.0},
    ("GET", "/api/v1/jobs"): [{"id": "j1", "status": "completed"},
                               {"id": "j2", "status": "running"}],
    ("GET", "/api/v1/jobs/j1"): {"id": "j1", "status": "completed"},
    ("GET", "/api/v1/jobs/j1/results"): {"rows": [1, 2]},
    ("POST", "/api/v1/jobs"): {"id": "j9", "status": "pending"},
    ("DELETE", "/api/v1/jobs/j1"): {"deleted": True},
    ("GET", "/api/v1/experiment-graphs"): [{"id": "exp1"}],
    ("GET", "/api/v1/experiment-graphs/exp1"): {"id": "exp1", "nodes": []},
    ("GET", "/api/v1/research/foundation-check"): {"verdict": "PASS", "n_fail": 0},
    ("GET", "/api/v1/foundation/status"): {"verdict": "PASS", "dirty": False},
    ("GET", "/api/v1/research-loop/status"): {"running": False},
    ("POST", "/api/v1/research-loop/stop"): {"stopped": True},
    ("GET", "/api/v1/research-loop/results"): {"cycles": 3},
    ("GET", "/api/v1/discovery/items"): {"items": [], "total": 0},
    ("GET", "/api/v1/discovery/stats"): {"new": 2},
    ("POST", "/api/v1/discovery/fetch"): {"job": "fetch1"},
    ("POST", "/api/v1/discovery/items/i1/status"): {"id": "i1", "status": "saved"},
    ("GET", "/api/v1/dashboard/latest-insight"): {"insight": "x"},
    ("GET", "/api/v1/dashboard/highlights"): {"items": []},
    ("GET", "/api/v1/anchor-sets"): [{"id": "a1"}],
    ("GET", "/api/v1/anchor-sets/a1"): {"id": "a1", "pairs": []},
    ("POST", "/api/v1/anchor-sets"): {"id": "a2"},
    ("GET", "/api/v1/reports"): [{"name": "r.json"}],
    ("GET", "/api/v1/reports/r.json"): {"ok": True},
    ("GET", "/api/v1/indus-evidence/claims"): {
        "claims": [{"claim_id": "c1", "claim_status": "untested"}],
        "total": 1, "limit": 200, "offset": 0,
    },
    ("GET", "/api/v1/indus-evidence/claims/aee-scores"): {
        "n_claims": 1, "mean_score": 0.5,
    },
    ("GET", "/api/v1/indus-evidence/library"): {"documents": [], "total": 0},
    ("GET", "/api/v1/indus-evidence/hypotheses"): {"models": []},
}

SSE_BODY = 'data: {"event": "run_complete", "result": {"ok": true}}\n\n'


class Recorder:
    """MockTransport handler: records requests, returns canned responses."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        key = (request.method, request.url.path)
        if key == ("POST", "/api/v1/experiment-graphs/exp1/run"):
            return httpx.Response(200, text=SSE_BODY,
                                  headers={"content-type": "text/event-stream"})
        if key == ("POST", "/api/v1/research-loop/start"):
            return httpx.Response(200, text="data: {\"event\": \"done\"}\n\n",
                                  headers={"content-type": "text/event-stream"})
        if key in CANNED:
            return httpx.Response(200, json=CANNED[key])
        return httpx.Response(404, json={"detail": "not found"})


@pytest.fixture()
def rec(monkeypatch):
    recorder = Recorder()
    real_client = httpx.Client

    def fake_client(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(recorder)
        return real_client(*args, **kwargs)

    monkeypatch.setattr(server.httpx, "Client", fake_client)
    return recorder


def _last(rec: Recorder) -> httpx.Request:
    return rec.requests[-1]


# ── TEST-MCP-001/002: happy paths + request formation ───────────────────────

def test_get_status(rec):
    out = json.loads(server.get_status())
    assert out["status"] == "ok"
    r = _last(rec)
    assert r.method == "GET" and r.url.path == "/api/v1/status"


def test_list_jobs_filter(rec):
    out = json.loads(server.list_jobs(status="running"))
    assert [j["id"] for j in out] == ["j2"]
    assert _last(rec).url.path == "/api/v1/jobs"


def test_create_job_body(rec):
    out = json.loads(server.create_job("n", "decipher", '{"k": 1}'))
    assert out["id"] == "j9"
    body = json.loads(_last(rec).content)
    assert body == {"name": "n", "pipeline": "decipher", "params": {"k": 1}}


def test_cancel_job(rec):
    out = json.loads(server.cancel_job("j1"))
    assert out["deleted"] is True
    r = _last(rec)
    assert r.method == "DELETE" and r.url.path == "/api/v1/jobs/j1"


def test_run_experiment_sse(rec):
    out = json.loads(server.run_experiment("exp1", "{}"))
    assert out["event"] == "run_complete"
    r = _last(rec)
    assert r.method == "POST" and r.url.path == "/api/v1/experiment-graphs/exp1/run"


def test_run_foundation_check(rec):
    out = json.loads(server.run_foundation_check())
    assert out["verdict"] == "PASS"


def test_get_foundation_status(rec):
    out = json.loads(server.get_foundation_status())
    assert out["dirty"] is False
    assert _last(rec).url.path == "/api/v1/foundation/status"


def test_trigger_discovery_fetch_body(rec):
    out = json.loads(server.trigger_discovery_fetch("indus_script", "gdelt_ngrams"))
    assert out["job"] == "fetch1"
    body = json.loads(_last(rec).content)
    assert body == {"topics": ["indus_script"], "sources": ["gdelt_ngrams"]}


def test_update_discovery_item_status(rec):
    out = json.loads(server.update_discovery_item_status("i1", "saved", "note"))
    assert out["status"] == "saved"
    body = json.loads(_last(rec).content)
    assert body == {"status": "saved", "notes": "note"}


def test_list_indus_claims_params(rec):
    out = json.loads(server.list_indus_claims(claim_status="untested", sign="M293", aee=True))
    assert out["total"] == 1
    r = _last(rec)
    assert r.url.path == "/api/v1/indus-evidence/claims"
    assert r.url.params["claim_status"] == "untested"
    assert r.url.params["sign"] == "M293"
    assert r.url.params["aee"] == "true"


def test_get_indus_claim_found(rec):
    out = json.loads(server.get_indus_claim("c1"))
    assert out["claim_id"] == "c1"


def test_get_indus_claim_missing(rec):
    out = json.loads(server.get_indus_claim("nope"))
    assert "error" in out and "nope" in out["error"]


def test_get_indus_claim_aee_scores(rec):
    out = json.loads(server.get_indus_claim_aee_scores())
    assert out["n_claims"] == 1
    assert _last(rec).url.path == "/api/v1/indus-evidence/claims/aee-scores"


def test_list_indus_library_and_hypotheses(rec):
    assert json.loads(server.list_indus_library(q="x"))["total"] == 0
    assert json.loads(server.list_indus_hypotheses()) == {"models": []}


def test_start_research_loop(rec):
    out = json.loads(server.start_research_loop(max_cycles=2))
    assert out["status"] == "started"
    assert out["max_cycles"] == 2


def test_get_anchor_staging_missing_file(rec, tmp_path, monkeypatch):
    monkeypatch.setattr(server, "_REPO", tmp_path)
    out = json.loads(server.get_anchor_staging())
    assert "error" in out


# ── TEST-MCP-003/004: error paths ────────────────────────────────────────────

def test_backend_404_becomes_error_object(rec):
    out = json.loads(server.get_job("missing"))
    assert "error" in out and out["type"] == "HTTPStatusError"


def test_unreachable_backend_becomes_error_object(monkeypatch):
    def boom(*args, **kwargs):
        raise httpx.ConnectError("refused", request=httpx.Request("GET", "http://x"))

    monkeypatch.setattr(server.httpx, "Client", boom)
    out = json.loads(server.get_status())
    assert "error" in out and out["type"] == "ConnectError"


def test_err_helper_shape():
    out = json.loads(server._err(ValueError("bad")))
    assert out == {"error": "bad", "type": "ValueError"}


def test_create_job_invalid_params_json(rec):
    out = json.loads(server.create_job("n", "p", "{not json"))
    assert "error" in out


# ── TEST-MCP-006: inventory ──────────────────────────────────────────────────

EXPECTED_TOOLS = {
    "get_status", "get_system_metrics",
    "list_jobs", "get_job", "create_job", "cancel_job", "get_job_results",
    "list_experiments", "get_experiment", "run_experiment",
    "run_foundation_check", "get_foundation_status",
    "start_research_loop", "get_research_loop_status", "stop_research_loop",
    "get_research_loop_results", "get_anchor_staging",
    "list_discovery_items", "get_discovery_stats", "trigger_discovery_fetch",
    "update_discovery_item_status",
    "get_latest_insight", "get_dashboard_highlights",
    "list_anchor_sets", "get_anchor_set", "create_anchor_set",
    "list_reports", "get_report",
    "list_indus_claims", "get_indus_claim", "get_indus_claim_aee_scores",
    "list_indus_library", "list_indus_hypotheses",
}


def test_tool_inventory():
    import asyncio

    names = {t.name for t in asyncio.run(server.mcp.list_tools())}
    assert names == EXPECTED_TOOLS
    assert len(names) == 33


# ── TEST-MCP-005: drift guard ────────────────────────────────────────────────

def _mcp_called_routes() -> set[tuple[str, tuple[str, ...]]]:
    """Extract (method, path-shape) pairs for every HTTP call in server.py.

    Path shape = tuple of segments with any ``{...}`` segment normalised to
    ``{}`` so server-side parameter names (e.g. ``{exp_id}``) don't matter —
    only the URL structure the MCP actually calls.
    """
    src = Path(server.__file__).read_text(encoding="utf-8")
    calls: set[tuple[str, tuple[str, ...]]] = set()
    pattern = re.compile(
        r"""\.(get|post|delete|put|patch)\(\s*f?"([^"]+)\""""
        r"""|\.stream\(\s*"(GET|POST|PUT|DELETE|PATCH)"\s*,\s*f?"([^"]+)\""""
    )
    for m in pattern.finditer(src):
        method = (m.group(1) or m.group(3)).upper()
        raw = m.group(2) or m.group(4)
        if not raw.startswith("/api/v1"):
            continue
        shape = tuple("{}" if seg.startswith("{") else seg
                      for seg in raw.split("/") if seg)
        calls.add((method, shape))
    return calls


def _shape(path: str) -> tuple[str, ...]:
    return tuple("{}" if seg.startswith("{") else seg
                 for seg in path.split("/") if seg)


def test_no_route_drift(client):
    """Every route the MCP calls must exist in the live FastAPI route table."""
    spec = client.get("/openapi.json").json()
    live = {
        (method.upper(), _shape(path))
        for path, ops in spec["paths"].items()
        for method in ops
    }
    called = _mcp_called_routes()
    assert called, "extractor found no MCP routes — guard is broken"
    missing = sorted(called - live)
    assert not missing, f"MCP calls routes that do not exist: {missing}"


def test_mcp_route_extractor_covers_indus_evidence():
    called = _mcp_called_routes()
    shapes = {shape for _, shape in called}
    assert ("api", "v1", "indus-evidence", "claims") in shapes
    assert ("api", "v1", "indus-evidence", "claims", "aee-scores") in shapes
    assert ("api", "v1", "foundation", "status") in shapes


def test_server_source_parses():
    ast.parse(Path(server.__file__).read_text(encoding="utf-8"))
