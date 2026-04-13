"""CLI-to-UI bridge for Glossa Lab experiments.

When experiments are run from the command line (outside the FastAPI server),
this module ensures the Glossa Lab UI still sees them:

  1. JOBS      — registers a job via POST /api/v1/jobs so it appears in the
                  Jobs panel (auto-cancels on error, auto-deletes on success).
  2. REPORTS   — saves the result dict as a timestamped JSON file in reports/
                  so it appears in the Reports catalog.
  3. LOGS      — emits structured JSON log entries that the backend's logging
                  infrastructure picks up (visible in the Logs / Terminal panel).

Usage (automatic via ExperimentBase.run_cli()):
    from glossa_lab.experiment_base import get_experiment
    cls = get_experiment("beam_decipher_benchmark")
    result = cls().run_cli()

Usage (direct):
    with CliReporter("beam_decipher_benchmark", "Beam Decipherment") as rep:
        result = run_my_experiment()
        rep.save_result(result)
"""
from __future__ import annotations

import json
import logging
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_log = logging.getLogger("glossa_lab.cli")

# ── Configuration ─────────────────────────────────────────────────────────────
# The API base URL.  Override with GLOSSA_PORT env var if needed.
import os as _os
_PORT     = int(_os.environ.get("GLOSSA_PORT", "8001"))
_API_BASE = f"http://localhost:{_PORT}/api/v1"

# Reports directory relative to the repo root (same place the UI watches).
_REPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "reports"


# ── HTTP helpers (stdlib only, no extra deps) ─────────────────────────────────

def _http(method: str, path: str, body: dict | None = None) -> dict | None:
    """Make a JSON HTTP request to the local API.  Returns None on any error."""
    url = f"{_API_BASE}{path}"
    data = json.dumps(body or {}).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=2) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, Exception):
        return None   # API not running — silently skip


def _api_running() -> bool:
    """Return True if the Glossa Lab backend is reachable."""
    return _http("GET", "/health") is not None


# ── Report saving ─────────────────────────────────────────────────────────────

def save_report(experiment_id: str, result: dict[str, Any]) -> Path | None:
    """Save a result dict to reports/{experiment_id}_{timestamp}.json.

    Returns the path written, or None on error.
    The UI's /api/v1/catalog/reports endpoint auto-discovers files here.
    """
    try:
        _REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        ts   = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        name = f"{experiment_id}_{ts}.json"
        path = _REPORTS_DIR / name
        path.write_text(
            json.dumps(result, indent=2, default=str),
            encoding="utf-8",
        )
        _log.info("CLI report saved", extra={"file": name, "experiment": experiment_id})
        return path
    except Exception as exc:
        _log.warning("Could not save CLI report: %s", exc)
        return None


# ── CliReporter context manager ───────────────────────────────────────────────

class CliReporter:
    """Context manager that hooks a CLI experiment into the Glossa Lab UI.

    Inside the ``with`` block:
      - A job is created in the backend (visible in the Jobs panel).
      - _log.info messages appear in the structured log / Terminal panel.
      - call ``save_result(result)`` to write a timestamped JSON report.

    On exit:
      - The job is removed (it completed / was cancelled).
      - Elapsed time is logged.

    If the backend is not running, all UI operations are silently skipped.
    The experiment still runs and outputs normally to stdout.
    """

    def __init__(self, experiment_id: str, name: str) -> None:
        self.experiment_id = experiment_id
        self.name          = name
        self.job_id: str | None = None
        self._t0: float = 0.0

    def __enter__(self) -> "CliReporter":
        self._t0 = time.time()
        _log.info(
            "CLI experiment started",
            extra={"experiment": self.experiment_id, "exp_name": self.name},
        )
        job = _http("POST", "/jobs", {
            "name":     f"{self.name}  [CLI]",
            "pipeline": self.experiment_id,
            "params":   {"source": "cli", "started_at": datetime.now(timezone.utc).isoformat()},
        })
        if job:
            self.job_id = job.get("id")
            # Immediately mark as running so the UI shows a spinner
            _http("PATCH", f"/jobs/{self.job_id}", {"status": "running"})
            _log.info("Job registered with UI", extra={"job_id": self.job_id})
        return self

    def save_result(self, result: dict[str, Any]) -> Path | None:
        """Persist result to reports/ so it appears in the Reports catalog."""
        self._last_result = result
        return save_report(self.experiment_id, result)

    def progress(self, message: str, **extra: Any) -> None:
        """Emit a structured log line (shows in backend log / Terminal panel)."""
        _log.info(message, extra={"experiment": self.experiment_id, **extra})

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> bool:
        elapsed = round(time.time() - self._t0, 1)
        status  = "failed" if exc_type else "completed"
        if self.job_id:
            # PATCH to completed/failed so the job persists and is visible in the UI
            result_snapshot = getattr(self, "_last_result", {})
            summary = {
                k: result_snapshot[k]
                for k in list(result_snapshot)[:10]  # keep payload small
            } if isinstance(result_snapshot, dict) else {}
            _http("PATCH", f"/jobs/{self.job_id}", {
                "status": status,
                "result_data": {"elapsed_s": elapsed, **summary},
            })
        _log.info(
            "CLI experiment %s",
            status,
            extra={
                "experiment": self.experiment_id,
                "elapsed_s":  elapsed,
                "success":    exc_type is None,
            },
        )
        return False   # never suppress exceptions


# ── Convenience wrapper ───────────────────────────────────────────────────────

@contextmanager
def report_context(experiment_id: str, name: str):
    """Shorthand context manager that also yields a save helper.

    Example::

        with report_context("my_exp", "My Experiment") as rep:
            result = run_my_experiment()
            rep.save_result(result)
    """
    with CliReporter(experiment_id, name) as rep:
        yield rep


def run_with_reporting(
    experiment_id: str,
    name: str,
    fn,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Run *fn(*args, **kwargs)* wrapped in a CliReporter.

    Saves the return value (if it is a dict) as a report and returns it.
    """
    with CliReporter(experiment_id, name) as rep:
        result = fn(*args, **kwargs)
        if isinstance(result, dict):
            rep.save_result(result)
        return result
