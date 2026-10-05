"""TEST-FSW: foundation status tracker records research-API check runs.

The MCP run_foundation_check tool calls GET /api/v1/research/foundation-check
(glossa_lab.api.foundation_check). That handler runs its own check set and
previously recorded nothing, so GET /api/v1/foundation/status stayed null
even immediately after a full check run. These tests pin the wiring: a
research-API run must be visible in the tracker (with source attribution),
mapped from the research summary shape (n_pass -> n_ok, overall_status ->
verdict).
"""
from __future__ import annotations

import glossa_lab.api.foundation_check as foundation_check_module


def _fake_checks() -> list[dict]:
    return [
        {"label": "fake pass 1", "status": "pass"},
        {"label": "fake pass 2", "status": "pass"},
        {"label": "fake warn", "status": "warn"},
    ]


def test_research_run_is_recorded_in_status_tracker(client, monkeypatch):
    monkeypatch.setattr(foundation_check_module, "_run_checks", _fake_checks)

    run = client.get("/api/v1/research/foundation-check")
    assert run.status_code == 200
    body = run.json()
    assert body["summary"]["n_pass"] == 2
    assert body["summary"]["n_warn"] == 1

    status = client.get("/api/v1/foundation/status")
    assert status.status_code == 200
    data = status.json()
    assert data["last_checked_at"] is not None
    assert data["verdict"] == "PASS"  # overall_status of the fake run
    assert data["n_ok"] == 2
    assert data["n_fail"] == 0
    assert data["n_warn"] == 1
    assert data["source"] == "research_api"
    assert data["dirty"] is False


def test_research_run_with_failure_records_fail_verdict(client, monkeypatch):
    def failing_checks() -> list[dict]:
        return [
            {"label": "fake pass", "status": "pass"},
            {"label": "fake fail", "status": "fail"},
        ]

    monkeypatch.setattr(foundation_check_module, "_run_checks", failing_checks)

    run = client.get("/api/v1/research/foundation-check")
    assert run.status_code == 200

    data = client.get("/api/v1/foundation/status").json()
    assert data["verdict"] == "FAIL"
    assert data["n_ok"] == 1
    assert data["n_fail"] == 1
    assert data["source"] == "research_api"
