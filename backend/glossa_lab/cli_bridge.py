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
import os as _os
import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_log = logging.getLogger("glossa_lab.cli")

# ── Configuration ─────────────────────────────────────────────────────────────────────────
# The API base URL.  Override with GLOSSA_PORT env var if needed.
_PORT = int(_os.environ.get("GLOSSA_PORT", "8001"))
_API_BASE = f"http://localhost:{_PORT}/api/v1"

# Reports directory relative to the repo root (same place the UI watches).
_REPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "reports"


# ── HTTP helpers (stdlib only, no extra deps) ─────────────────────────────────


def _http(method: str, path: str, body: dict | None = None) -> dict | None:
    """Make a JSON HTTP request to the local API.  Returns None on any error.

    Per H17: errors from the backend are LOGGED at WARNING so that silent
    job-status drift can be detected.  We still return None on failure so
    callers don't crash if the backend is offline, but we no longer pretend
    nothing went wrong.
    """
    url = f"{_API_BASE}{path}"
    # Use ensure_ascii=True (default) so non-Latin-1 characters are escaped.
    # Encode the bytes explicitly as UTF-8 (which JSON-escaped ASCII already is).
    data = json.dumps(body or {}).encode("utf-8") if body is not None else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        try:
            err_body = exc.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            err_body = ""
        _log.warning(
            "cli_bridge HTTP %s %s -> %s: %s",
            method,
            path,
            exc.code,
            err_body[:300],
        )
        return None
    except urllib.error.URLError as exc:
        # Backend not reachable — still log at DEBUG so we can confirm
        _log.debug("cli_bridge HTTP %s %s unreachable: %s", method, path, exc.reason)
        return None
    except Exception as exc:  # noqa: BLE001
        _log.warning("cli_bridge HTTP %s %s failed: %s", method, path, exc)
        return None


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
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
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

    def __init__(self, experiment_id: str, name: str, *, heartbeat_interval: float = 60.0) -> None:
        self.experiment_id = experiment_id
        self.name = name
        self.job_id: str | None = None
        self._t0: float = 0.0
        self._heartbeat_interval = heartbeat_interval
        self._heartbeat_stop = threading.Event()
        self._heartbeat_thread: threading.Thread | None = None

    def __enter__(self) -> "CliReporter":
        self._t0 = time.time()
        _log.info(
            "CLI experiment started",
            extra={"experiment": self.experiment_id, "exp_name": self.name},
        )
        # Create directly as 'running' so the pipeline engine never picks it up.
        # If created as 'pending' there is a race: the engine polls every 2s and
        # would claim the job before the subsequent PATCH could arrive.
        # Detect compute device for UI display
        _device = "unknown"
        _device_label = "unknown"
        try:
            from glossa_lab.experiments._parallel import compute_device, compute_device_label

            _device = compute_device()
            _device_label = compute_device_label()
        except Exception:
            pass

        job = _http(
            "POST",
            "/jobs",
            {
                "name": f"{self.name}  [CLI]",
                "pipeline": self.experiment_id,
                "initial_status": "running",
                "params": {
                    "source": "cli",
                    "started_at": datetime.now(timezone.utc).isoformat(),
                    "compute_device": _device,
                    "compute_device_label": _device_label,
                },
            },
        )
        if job:
            self.job_id = job.get("id")
            _log.info("Job registered with UI", extra={"job_id": self.job_id})
            # Start auto-heartbeat thread so the backend stall watchdog
            # does not kill genuinely-running silent experiments.
            self._start_heartbeat()
        return self

    def _start_heartbeat(self) -> None:
        """Spawn a daemon thread that PATCHes the job every heartbeat_interval
        seconds with status=running. Stops when __exit__ sets the event.
        Per H17.7: silent legacy experiments rely on this to avoid the
        backend watchdog (default 1800s).
        """
        if not self.job_id:
            return

        def _beat() -> None:
            n = 0
            while not self._heartbeat_stop.wait(self._heartbeat_interval):
                n += 1
                # PATCH with status=running just to bump updated_at.
                # The backend update_job_status touches updated_at as a side effect.
                _http("PATCH", f"/jobs/{self.job_id}", {"status": "running"})
                _log.debug("heartbeat #%d for job %s", n, self.job_id)

        self._heartbeat_thread = threading.Thread(
            target=_beat,
            name=f"cli-heartbeat-{self.job_id}",
            daemon=True,
        )
        self._heartbeat_thread.start()

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
        # Stop the heartbeat thread BEFORE the final PATCH so the two don't race.
        self._heartbeat_stop.set()
        if self._heartbeat_thread is not None:
            self._heartbeat_thread.join(timeout=2.0)
        elapsed = round(time.time() - self._t0, 1)
        status = "failed" if exc_type else "completed"
        if self.job_id:
            # PATCH to completed/failed so the job persists and is visible in the UI
            result_snapshot = getattr(self, "_last_result", {})
            summary: dict[str, Any] = {}
            if isinstance(result_snapshot, dict):
                # Keep payload small AND JSON-serialisable.  Drop any value that
                # cannot be JSON-encoded (e.g. LanguageModel, numpy arrays).
                for k in list(result_snapshot)[:10]:
                    v = result_snapshot[k]
                    try:
                        json.dumps(v, default=str)
                        summary[k] = v
                    except (TypeError, ValueError):
                        summary[k] = f"<unserialisable: {type(v).__name__}>"
            _http(
                "PATCH",
                f"/jobs/{self.job_id}",
                {
                    "status": status,
                    "result_data": {"elapsed_s": elapsed, **summary},
                },
            )
        _log.info(
            "CLI experiment %s",
            status,
            extra={
                "experiment": self.experiment_id,
                "elapsed_s": elapsed,
                "success": exc_type is None,
            },
        )
        return False  # never suppress exceptions


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
