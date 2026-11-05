#!/usr/bin/env python3
"""Write the repo-side citation record for one backend
job (Spec 089 Stage 4, T403; C089-8).

A backend job executes in the live backend under its own
execution-minted job id (uuid4 hex 12). Its results are
citable only under that job id, with the inputs the job
ran over recorded — and that binding is made here, at
citation time: this tool reads the job, its results, and
(where the job names a graph) the graph record through
the backend API, and writes the run record (run-defs v1
header; the experiment pins; the job_results payload
hash + the quotable summary) into the citing record's
store, whose run index gains the `entry` act.

A completed job with no stored results, and a failed or
cancelled job, yield an absence record — an execution
with no citable result is recorded as absent, never
silently skipped. A pending or running job refuses:
there is no outcome to cite yet. The tool is read-only
against the backend: it creates nothing and runs no
experiment.

Usage:

    python3 tools/runs/job_citation.py JOB_ID \
        --store specs/<spec>/records \
        [--base-url http://127.0.0.1:8001] \
        [--determinism-class named-nondeterministic] \
        [--environment-class desktop/windows] \
        [--summary-json summary.json]

The API token is resolved from $GLOSSA_API_TOKEN, else
the install's api_token file (~/.local/share/glossa-lab/
api_token) — the MCP server's resolution order. The
token value is never printed and never enters the
record. Exit code 0 on success, 1 on a named refusal.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab import run_records as rr

_TIMEOUT_SECONDS = 30


class _Refusal(Exception):
    """A named refusal: the citation cannot be made."""


def _resolve_token() -> Optional[str]:
    token = os.environ.get("GLOSSA_API_TOKEN")
    if token:
        return token.strip()
    token_file = Path.home() / ".local" / "share" / "glossa-lab" / "api_token"
    if token_file.is_file():
        return token_file.read_text(encoding="utf-8").strip()
    return None


def _get_json(
    base_url: str, path: str, token: Optional[str]
) -> tuple[int, Any]:
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}{path}",
        headers=(
            {"Authorization": f"Bearer {token}"} if token else {}
        ),
    )
    try:
        with urllib.request.urlopen(
            request, timeout=_TIMEOUT_SECONDS
        ) as response:
            return response.status, json.loads(
                response.read().decode("utf-8")
            )
    except urllib.error.HTTPError as exc:
        return exc.code, None
    except (urllib.error.URLError, OSError) as exc:
        raise _Refusal(
            f"backend unreachable at {base_url}: {exc}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise _Refusal(
            f"backend returned non-JSON for {path}: {exc}"
        ) from exc


def _backend_identity(base_url: str, token: Optional[str]) -> tuple[str, str]:
    """The deployed build identity (the experiment key's
    code_version) and the backend's version (the header's
    tool_version), from the health payload. Unreachable
    health is recorded as "unknown", never invented."""
    try:
        status, payload = _get_json(base_url, "/api/v1/health", token)
    except _Refusal:
        return "unknown", "unknown"
    if status != 200 or not isinstance(payload, dict):
        return "unknown", "unknown"
    version = payload.get("version") or "unknown"
    build = payload.get("build") or "unknown"
    return f"{version}+{build}", str(version)


def make_reader(base_url: str, token: Optional[str]):
    """The backend-API reader `cite_job` consumes:
    job_id → (job, results, graph). A completed job whose
    results read as 404 yields results=None (the absence
    case); transport and lookup failures refuse."""

    def read_job(job_id: str):
        status, job = _get_json(base_url, f"/api/v1/jobs/{job_id}", token)
        if status == 404:
            raise _Refusal(f"no such backend job: {job_id!r}")
        if status != 200 or not isinstance(job, dict):
            raise _Refusal(
                f"reading job {job_id!r} failed (HTTP {status})"
            )
        params = job.get("params") or {}
        graph = None
        graph_id = params.get("exp_id") or params.get("experiment_id")
        if graph_id:
            g_status, g_payload = _get_json(
                base_url, f"/api/v1/experiment-graphs/{graph_id}", token
            )
            if g_status == 200 and isinstance(g_payload, dict):
                graph = g_payload
        results = None
        if job.get("status") == "completed":
            r_status, payload = _get_json(
                base_url, f"/api/v1/jobs/{job_id}/results", token
            )
            if r_status == 200:
                results = payload
            elif r_status != 404:
                raise _Refusal(
                    f"reading results for job {job_id!r} failed "
                    f"(HTTP {r_status})"
                )
        return job, results, graph

    return read_job


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the citation record for one "
        "backend job (Spec 089, T403)."
    )
    parser.add_argument("job_id", help="the backend job id to cite")
    parser.add_argument(
        "--store",
        type=Path,
        required=True,
        help="the citing record's store directory",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("GLOSSA_BASE_URL", "http://127.0.0.1:8001"),
        help="the backend API base (default: $GLOSSA_BASE_URL "
        "or http://127.0.0.1:8001)",
    )
    parser.add_argument(
        "--determinism-class",
        default="named-nondeterministic",
        choices=list(rr.DETERMINISM_CLASSES),
        help="the graph's registered determinism class "
        "(run-defs v1 §5: the default is "
        "named-nondeterministic; deterministic only by a "
        "per-graph registration act)",
    )
    parser.add_argument(
        "--environment-class",
        default="desktop/windows",
        help="the backend's venue class (default: "
        "desktop/windows — the backend's host of record)",
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="a JSON object to record as the quotable "
        "summary instead of the mechanical one",
    )
    args = parser.parse_args(argv)

    token = _resolve_token()
    summary = None
    if args.summary_json is not None:
        try:
            summary = json.loads(
                args.summary_json.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            print(f"refused: cannot read summary: {exc}", file=sys.stderr)
            return 1
        if not isinstance(summary, dict):
            print(
                "refused: --summary-json must carry a JSON object",
                file=sys.stderr,
            )
            return 1
    code_version, tool_version = _backend_identity(args.base_url, token)
    try:
        path = rr.cite_job(
            make_reader(args.base_url, token),
            args.job_id,
            args.store,
            code_version=code_version,
            environment_class=args.environment_class,
            determinism_class=args.determinism_class,
            tool_version=tool_version,
            summary=summary,
        )
        record = json.loads(path.read_text(encoding="utf-8"))
    except (_Refusal, rr.RunRecordError) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    print(f"citation record: {path}")
    print(json.dumps(record, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
