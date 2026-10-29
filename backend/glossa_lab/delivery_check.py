"""Delivery-integrity checker (Leg C finding C-15).

Rule: **"No resolution, no report."** A run id or CI status may be
stated as fact only if, in the same reporting step, it was resolved
against the primary record (the GitHub API for CI runs; the
gatekeeper record for desktop jobs) and the resolution is quoted.

This module implements the mechanical half for GitHub Actions runs:

- the run must exist (HTTP 200 from ``actions/runs/<id>``);
- its ``head_sha`` must match the expected SHA (prefix match allowed
  for short SHAs);
- CI status is counted from per-job ``conclusion`` fields of that
  run (``actions/runs/<id>/jobs``), never from a summary string.

``check_delivery`` takes an injectable ``fetch(path) -> (status,
payload)`` callable so the logic is unit-testable without network or
``gh``; ``gh_fetch`` is the production fetcher (shells out to the
``gh`` CLI, the fleet's standard GitHub route). The CLI wrapper is
``tools/delivery-check/check_delivery.py``; it prints exactly one
citable verdict line and exits non-zero on any mismatch:

    RESOLVED run <id> sha <short> 8/8 success @ <timestamp>
    UNRESOLVED: <reason>
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from typing import Any, Callable

REPO = "BitConcepts/glossa-lab"

Fetch = Callable[[str], "tuple[int, dict[str, Any] | None]"]


def gh_fetch(path: str) -> tuple[int, dict[str, Any] | None]:
    """Fetch a GitHub API path via the ``gh`` CLI (JSON response)."""
    proc = subprocess.run(
        ["gh", "api", path],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        # gh exits non-zero on 404 etc.; surface the HTTP status when
        # it can be parsed from stderr, else a generic failure status.
        return 404 if "404" in proc.stderr else 502, None
    try:
        return 200, json.loads(proc.stdout)
    except json.JSONDecodeError:
        return 502, None


def check_delivery(
    run_id: str | int,
    expected_sha: str,
    fetch: Fetch = gh_fetch,
    repo: str = REPO,
) -> tuple[bool, str]:
    """Resolve *run_id* against the GitHub API. Returns (ok, verdict_line)."""
    status, run = fetch(f"repos/{repo}/actions/runs/{run_id}")
    if status == 404 or run is None:
        return False, f"UNRESOLVED: run {run_id} not found (HTTP {status})"
    if status != 200:
        return False, f"UNRESOLVED: run {run_id} lookup failed (HTTP {status})"

    head_sha = str(run.get("head_sha") or "")
    if not head_sha or not (
        head_sha.startswith(expected_sha) or expected_sha.startswith(head_sha)
    ):
        return False, (
            f"UNRESOLVED: run {run_id} head_sha {head_sha[:12]} "
            f"does not match expected {expected_sha[:12]}"
        )
    if run.get("status") != "completed":
        return False, (
            f"UNRESOLVED: run {run_id} is {run.get('status')}, not completed"
        )

    jstatus, jobs_payload = fetch(f"repos/{repo}/actions/runs/{run_id}/jobs")
    if jstatus != 200 or not jobs_payload:
        return False, f"UNRESOLVED: jobs for run {run_id} unreadable (HTTP {jstatus})"
    jobs = jobs_payload.get("jobs") or []
    if not jobs:
        return False, f"UNRESOLVED: run {run_id} reports no jobs"
    ok_jobs = sum(1 for j in jobs if j.get("conclusion") == "success")
    if ok_jobs != len(jobs):
        bad = [f"{j.get('name')}={j.get('conclusion')}" for j in jobs
               if j.get("conclusion") != "success"]
        return False, (
            f"UNRESOLVED: run {run_id} jobs {ok_jobs}/{len(jobs)} success "
            f"({'; '.join(bad)})"
        )
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return True, (
        f"RESOLVED run {run_id} sha {head_sha[:12]} "
        f"{ok_jobs}/{len(jobs)} success @ {ts}"
    )
