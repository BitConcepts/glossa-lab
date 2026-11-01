"""Leg C hardening (C-15): delivery-integrity checker tests.

The three failure modes from 2026-10-29 — a nonexistent run id
reported complete, an inverted CI status, and a run id mismatched
against the primary record — must each come back UNRESOLVED.
"""
from __future__ import annotations

from glossa_lab.delivery_check import check_delivery

SHA = "abcdef1234567890abcdef1234567890abcdef12"


def _fetch_factory(run=None, jobs=None, run_status=200, jobs_status=200):
    def fetch(path):
        if path.endswith("/jobs"):
            return jobs_status, jobs
        return run_status, run
    return fetch


def _run(**over):
    run = {"head_sha": SHA, "status": "completed", "conclusion": "success"}
    run.update(over)
    return run


def _jobs(n=8, conclusions=None):
    conclusions = conclusions or ["success"] * n
    return {"jobs": [{"name": f"job-{i}", "conclusion": c}
                     for i, c in enumerate(conclusions)]}


def test_resolved_run_reports_counted_jobs():
    ok, verdict = check_delivery(
        123, SHA, fetch=_fetch_factory(run=_run(), jobs=_jobs()))
    assert ok
    assert verdict.startswith("RESOLVED run 123 sha abcdef123456 8/8 success @")


def test_nonexistent_run_is_unresolved():
    ok, verdict = check_delivery(
        999, SHA, fetch=_fetch_factory(run=None, run_status=404))
    assert not ok
    assert verdict.startswith("UNRESOLVED: run 999 not found")


def test_sha_mismatch_is_unresolved():
    ok, verdict = check_delivery(
        123, "0000000000000000000000000000000000000000",
        fetch=_fetch_factory(run=_run(), jobs=_jobs()))
    assert not ok
    assert "does not match" in verdict


def test_inverted_ci_status_is_unresolved():
    ok, verdict = check_delivery(
        123, SHA, fetch=_fetch_factory(
            run=_run(), jobs=_jobs(conclusions=["success"] * 7 + ["failure"])))
    assert not ok
    assert "7/8 success" in verdict and "failure" in verdict


def test_incomplete_run_is_unresolved():
    ok, verdict = check_delivery(
        123, SHA, fetch=_fetch_factory(
            run=_run(status="in_progress", conclusion=None), jobs=_jobs()))
    assert not ok
    assert "not completed" in verdict
