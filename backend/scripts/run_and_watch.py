"""run_and_watch.py — canonical experiment launcher (H17.6).

Spawns one or more experiments as DETACHED subprocesses, then polls
/api/v1/jobs from the foreground and prints a status line on every
state transition (pending → running → completed/failed/timed_out).

Why this exists:
  Running experiments in the foreground via `shell.cmd python ...`
  produces zero output for minutes at a time. The agent (or human)
  cannot tell whether the run is alive or hung. This script makes
  every experiment observable in real time.

Usage:
    shell.cmd python backend/scripts/run_and_watch.py \\
        fuls_writing_system_comparison \\
        fuls_nw_semitic_ngram \\
        --poll-interval 5 --max-wait 1800

Exit codes:
  0 — every tracked job reached `completed`
  1 — at least one job ended in `failed` / `timed_out` / `cancelled`
  2 — max-wait exceeded; some jobs still running (treated as suspect)
  3 — backend not reachable
  4 — invalid experiment id (no ExperimentBase subclass found)

Output format (one line per event):
    [HH:MM:SS] [exp_id]  pending  -> running       (job_id=...)
    [HH:MM:SS] [exp_id]  running  -> completed     (3.2s elapsed)
    [HH:MM:SS] [exp_id]  ...heartbeat  running     (12s in state)
"""

from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Force UTF-8 stdout
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(_HERE)
ROOT = Path(_BACKEND).parent

for _p in (_BACKEND, os.path.join(_BACKEND, "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

API = "http://127.0.0.1:8001/api/v1"
TERMINAL_STATES = {"completed", "failed", "timed_out", "cancelled"}


def ts() -> str:
    return datetime.now().strftime("%H:%M:%S")


def log(msg: str) -> None:
    print(f"[{ts()}] {msg}", flush=True)


def http_get(path: str) -> Any | None:
    try:
        with urllib.request.urlopen(f"{API}{path}", timeout=5) as r:
            return json.loads(r.read())
    except urllib.error.URLError:
        return None
    except Exception as e:  # noqa: BLE001
        log(f"WARN: GET {path} failed: {e}")
        return None


def list_jobs_since(after_iso: str) -> list[dict]:
    """Return all jobs created at or after `after_iso`."""
    data = http_get("/jobs")
    if data is None:
        return []
    jobs = data if isinstance(data, list) else data.get("jobs", [])
    return [j for j in jobs if j.get("created_at", "") >= after_iso]


def find_experiment_class(exp_id: str):
    """Walk the experiments package and return the ExperimentBase subclass with matching id."""
    from glossa_lab.experiment_base import ExperimentBase

    # Register saved graph experiments first so JSON-defined experiments are
    # discoverable by id alongside Python ExperimentBase subclasses.
    try:
        from glossa_lab.experiment_graph import (  # noqa: PLC0415
            auto_migrate_hardcoded_experiments,
            register_graph_experiments,
        )
        auto_migrate_hardcoded_experiments()
        register_graph_experiments()
    except Exception as exc:  # noqa: BLE001
        log(f"WARN: graph experiment registration failed: {exc}")

    # Search both the public experiments package and the _legacy subpackage
    candidates = [
        "glossa_lab.experiments._legacy",
        "glossa_lab.experiments",
    ]
    import importlib
    import pkgutil

    for pkg_name in candidates:
        try:
            pkg = importlib.import_module(pkg_name)
        except Exception:  # noqa: BLE001
            continue
        for mod_info in pkgutil.iter_modules(pkg.__path__):
            if mod_info.name.startswith("_"):
                continue
            try:
                mod = importlib.import_module(f"{pkg_name}.{mod_info.name}")
            except Exception as e:  # noqa: BLE001
                log(f"WARN: import {pkg_name}.{mod_info.name} failed: {e}")
                continue
            for attr in dir(mod):
                obj = getattr(mod, attr)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, ExperimentBase)
                    and obj is not ExperimentBase
                    and getattr(obj, "id", None) == exp_id
                ):
                    return obj

    # Last-resort: check the discover_experiments registry (graph experiments
    # register themselves directly into this registry without going through
    # the package walker).
    try:
        from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415
        registry = discover_experiments()
        cls = registry.get(exp_id)
        if cls is not None and issubclass(cls, ExperimentBase) and cls is not ExperimentBase:
            return cls
    except Exception as exc:  # noqa: BLE001
        log(f"WARN: discover_experiments lookup failed: {exc}")

    return None


def spawn_experiment(exp_id: str) -> subprocess.Popen | None:
    """Launch a single experiment as a detached subprocess.

    Returns the Popen object so we can read its stdout/stderr if it dies
    BEFORE registering a job (caught error during import).
    """
    runner = ROOT / "backend" / "scripts" / f"_run_{exp_id}.py"
    runner.parent.mkdir(parents=True, exist_ok=True)
    # Self-contained runner: walks the experiments package itself, no
    # cross-import from run_and_watch (which is not on PYTHONPATH inside
    # the detached subprocess).
    body = (
        f'"""Auto-generated runner for {exp_id}."""\n'
        "import os, sys, io, importlib, pkgutil\n"
        'if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":\n'
        '    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")\n'
        f'sys.path.insert(0, r"{_BACKEND}")\n'
        f'sys.path.insert(0, r"{os.path.join(_BACKEND, "tests")}")\n'
        "from glossa_lab.experiment_base import ExperimentBase, discover_experiments\n"
        "# Register graph experiments (JSON-defined) into the discovery registry.\n"
        "try:\n"
        "    from glossa_lab.experiment_graph import (\n"
        "        auto_migrate_hardcoded_experiments,\n"
        "        register_graph_experiments,\n"
        "    )\n"
        "    auto_migrate_hardcoded_experiments()\n"
        "    register_graph_experiments()\n"
        "except Exception as e:\n"
        "    print(f'GRAPH-REG-FAIL: {e}', flush=True)\n"
        f'TARGET = "{exp_id}"\n'
        "def _find():\n"
        "    for pkg_name in ('glossa_lab.experiments._legacy', 'glossa_lab.experiments'):\n"
        "        try:\n"
        "            pkg = importlib.import_module(pkg_name)\n"
        "        except Exception:\n"
        "            continue\n"
        "        for mi in pkgutil.iter_modules(pkg.__path__):\n"
        "            if mi.name.startswith('_'):\n"
        "                continue\n"
        "            try:\n"
        "                mod = importlib.import_module(f'{pkg_name}.{mi.name}')\n"
        "            except Exception as e:\n"
        "                print(f'IMPORT-FAIL {pkg_name}.{mi.name}: {e}', flush=True)\n"
        "                continue\n"
        "            for attr in dir(mod):\n"
        "                obj = getattr(mod, attr)\n"
        "                if (isinstance(obj, type) and issubclass(obj, ExperimentBase)\n"
        "                        and obj is not ExperimentBase\n"
        "                        and getattr(obj, 'id', None) == TARGET):\n"
        "                    return obj\n"
        "    # Fall back to graph-experiment registry\n"
        "    try:\n"
        "        reg = discover_experiments()\n"
        "        cls = reg.get(TARGET)\n"
        "        if cls is not None and issubclass(cls, ExperimentBase) and cls is not ExperimentBase:\n"
        "            return cls\n"
        "    except Exception as e:\n"
        "        print(f'DISCOVER-FAIL: {e}', flush=True)\n"
        "    return None\n"
        "cls = _find()\n"
        "if cls is None:\n"
        "    print(f'NO SUCH EXPERIMENT: {TARGET}', flush=True); sys.exit(4)\n"
        "print(f'STARTING {cls.__module__}.{cls.__name__}', flush=True)\n"
        "cls().run_cli()\n"
    )
    runner.write_text(body, encoding="utf-8")

    venv_py = ROOT / "backend" / "venv" / "Scripts" / "python.exe"
    log_file = ROOT / "logs" / f"runner_{exp_id}.log"
    log_file.parent.mkdir(exist_ok=True)
    fout = log_file.open("w", encoding="utf-8")

    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS  # type: ignore[attr-defined]

    proc = subprocess.Popen(  # noqa: S603
        [str(venv_py), str(runner)],
        stdout=fout,
        stderr=subprocess.STDOUT,
        cwd=str(ROOT),
        creationflags=creationflags,
        close_fds=True,
    )
    log(f"SPAWN {exp_id}  pid={proc.pid}  log={log_file.relative_to(ROOT)}")
    return proc


def monitor(exp_ids: list[str], poll_interval: float, max_wait: float) -> int:
    # Sanity: backend must be up
    if http_get("/health") is None:
        log("ERROR: backend not reachable at http://127.0.0.1:8001")
        return 3

    # Validate every experiment id BEFORE spawning anything
    for exp_id in exp_ids:
        cls = find_experiment_class(exp_id)
        if cls is None:
            log(f"ERROR: no ExperimentBase subclass with id={exp_id!r}")
            return 4
        log(f"VALID  {exp_id} -> {cls.__module__}.{cls.__name__}")

    # Snapshot the time so we only track jobs created from now on. We use a
    # timezone-aware UTC datetime (datetime.utcnow is deprecated in 3.12+) but
    # then drop the tzinfo before isoformat() so the resulting string remains
    # in the same naive form ("YYYY-MM-DDTHH:MM:SS.ffffff") that the backend
    # `created_at` field is stored in. Keeping the format identical preserves
    # the lexicographic >= comparison used by list_jobs_since().
    started_iso = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    log(f"Tracking jobs created at or after: {started_iso}")

    procs: dict[str, subprocess.Popen] = {}
    for exp_id in exp_ids:
        p = spawn_experiment(exp_id)
        if p:
            procs[exp_id] = p

    # Poll loop
    last_state: dict[str, str] = {}  # job_id -> last seen status
    state_since: dict[str, float] = {}  # job_id -> wallclock when status entered
    seen_for_pipeline: dict[str, str] = {}  # exp_id -> job_id once first matched

    t_start = time.time()
    fail_summary: list[dict] = []

    while True:
        elapsed = time.time() - t_start
        if elapsed > max_wait:
            log(f"MAX-WAIT REACHED ({max_wait}s); some jobs still running")
            return 2

        # Check if any of our subprocesses exited before the job was registered
        for exp_id, p in list(procs.items()):
            rc = p.poll()
            if rc is not None and exp_id not in seen_for_pipeline:
                # The runner died and never created a job
                log(f"PROC-DEAD {exp_id}  exit={rc}  (no job ever registered)")
                tail = (ROOT / "logs" / f"runner_{exp_id}.log").read_text(
                    encoding="utf-8", errors="replace"
                )
                log(f"  last 30 lines of runner log:\n{chr(10).join(tail.splitlines()[-30:])}")
                fail_summary.append(
                    {
                        "exp_id": exp_id,
                        "reason": "runner_exited_before_job_register",
                        "exit_code": rc,
                    }
                )
                del procs[exp_id]

        # Pull fresh job list
        jobs = list_jobs_since(started_iso)

        # Match jobs to our experiments by pipeline id
        for j in jobs:
            pipeline = j.get("pipeline", "")
            jid = j.get("id", "")
            if pipeline in exp_ids:
                # Bind the FIRST matching job to that exp_id
                if pipeline not in seen_for_pipeline and jid not in last_state:
                    seen_for_pipeline[pipeline] = jid

            if jid not in last_state:
                continue
            new_status = j.get("status", "?")
            if last_state[jid] != new_status:
                prev = last_state[jid]
                last_state[jid] = new_status
                state_since[jid] = time.time()
                log(f"TRANS  {pipeline:<35} {prev:<10} -> {new_status:<10}  job={jid}")
                if new_status in TERMINAL_STATES and new_status != "completed":
                    params_str = json.dumps(j.get("params", {}))
                    log(
                        f"FAIL   {pipeline}  status={new_status}  params={params_str}"
                    )
                    fail_summary.append(
                        {
                            "exp_id": pipeline,
                            "job_id": jid,
                            "status": new_status,
                            "params": j.get("params", {}),
                        }
                    )

        # Detect newly-bound jobs
        for pipeline, jid in seen_for_pipeline.items():
            if jid not in last_state:
                # This is a fresh binding; find the job in the latest snapshot
                match = next((j for j in jobs if j.get("id") == jid), None)
                if match:
                    s = match.get("status", "?")
                    last_state[jid] = s
                    state_since[jid] = time.time()
                    log(f"BOUND  {pipeline:<35} initial-status={s:<10}  job={jid}")

        # Heartbeat for still-running jobs
        for jid, s in last_state.items():
            if s in TERMINAL_STATES:
                continue
            in_state = time.time() - state_since.get(jid, t_start)
            pipeline = next((p for p, x in seen_for_pipeline.items() if x == jid), "?")
            log(f"HBEAT  {pipeline:<35} {s:<10}  in-state={in_state:.0f}s  total={elapsed:.0f}s")

        # Done?
        if seen_for_pipeline and all(
            last_state.get(jid, "?") in TERMINAL_STATES for jid in seen_for_pipeline.values()
        ):
            break

        # Early exit: all subprocesses are dead AND no job ever registered
        # (avoids waiting the full max_wait for clearly-broken runs)
        if not procs and not seen_for_pipeline:
            log("ALL RUNNERS DIED before registering jobs — aborting early")
            break

        time.sleep(poll_interval)

    # ── Final summary ────────────────────────────────────────────────────
    log("=" * 78)
    log(f"BATCH COMPLETE in {time.time() - t_start:.1f}s")
    n_ok = 0
    for pipeline in exp_ids:
        jid = seen_for_pipeline.get(pipeline)
        if jid is None:
            log(f"  ?? {pipeline:<35}  no job ever registered")
            continue
        s = last_state.get(jid, "?")
        marker = "OK  " if s == "completed" else "FAIL"
        log(f"  {marker} {pipeline:<35}  status={s}  job={jid}")
        if s == "completed":
            n_ok += 1
    log(f"  Submitted: {len(exp_ids)}   Completed: {n_ok}   Failed: {len(exp_ids) - n_ok}")
    if fail_summary:
        log("FAILURE DETAILS:")
        for f in fail_summary:
            log("  " + json.dumps(f, default=str))
    return 0 if n_ok == len(exp_ids) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="H17.6 experiment runner with live job polling.")
    parser.add_argument(
        "experiment_ids", nargs="+", help="One or more experiment ids (e.g. fuls_rtl_corrected)"
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=5.0,
        help="Seconds between job-status polls (default 5)",
    )
    parser.add_argument(
        "--max-wait",
        type=float,
        default=1800.0,
        help="Total max wall-time before giving up (default 1800s = 30min)",
    )
    args = parser.parse_args()
    return monitor(args.experiment_ids, args.poll_interval, args.max_wait)


if __name__ == "__main__":
    sys.exit(main())
