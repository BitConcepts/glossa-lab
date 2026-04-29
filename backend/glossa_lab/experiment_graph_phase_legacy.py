"""Legacy Phase-16/17/18/19 atomic-node migration shims.

WARP.md rule G1 requires every Phase-N research run to be expressed as
either a graph experiment or an `ExperimentBase` subclass. Phases 16-19
predate that rule and were authored as standalone scripts under
`scripts/phase{N}/`. This module wraps each analysis script's `main()`
as a single primitive atomic node (one well-defined operation: run a
named legacy phase script, return its produced JSON output path).

A thin per-script graph JSON in `experiments/graphs/` then makes each
legacy run discoverable in the UI Jobs panel and re-runnable through
the standard `shell.cmd python -m glossa_lab.experiments <id>`
executor.

This is *not* a refactor of the underlying analysis logic — it
preserves the exact behaviour of each pre-existing script while
restoring graph-executor compliance. Future Phase-N work should follow
the proper Phase-15 / Phase-20 / Phase-21 atomic-node decomposition
pattern instead.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def _resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _legacy_phase_script_runner(inputs: dict, params: dict) -> dict:
    """Run a Phase-16/17/18/19 analysis script and return its produced
    output path + a snippet of the parsed JSON output (if available).

    Params:
      script_path  -- repo-relative path of the Python script to run,
                       e.g. ``scripts/phase19/omnibus.py``.
      output_path  -- repo-relative path of the JSON file the script is
                       expected to write to ``reports/`` or anywhere
                       under the repo. If empty, no output is parsed.
      timeout_s    -- subprocess timeout in seconds (default 1200).
    """
    script_path = str(params.get("script_path") or "").strip()
    output_path = str(params.get("output_path") or "").strip()
    timeout_s = int(params.get("timeout_s", 1200))

    if not script_path:
        return {"error": "script_path is required"}

    root = _resolve_repo_root()
    script_abs = (root / script_path).resolve()
    if not script_abs.exists():
        return {"error": f"script not found: {script_abs}"}

    # Subprocess-run the script with the project's Python.
    # We rely on the running interpreter being the venv Python (the
    # graph executor is itself launched by shell.cmd which activates
    # the venv).
    try:
        proc = subprocess.run(
            [sys.executable, str(script_abs)],
            cwd=str(root), capture_output=True, text=True,
            timeout=timeout_s, check=False,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"subprocess error: {exc}"}

    output_data: Any = None
    output_size = 0
    output_present = False
    if output_path:
        out_abs = (root / output_path).resolve()
        if out_abs.exists():
            try:
                output_size = out_abs.stat().st_size
                with out_abs.open("r", encoding="utf-8") as fh:
                    output_data = json.load(fh)
                output_present = True
            except Exception as exc:  # noqa: BLE001
                output_data = {"error": f"failed to parse output JSON: {exc}"}

    # Trim large output snippets so the graph result stays small.
    if isinstance(output_data, dict):
        snippet_keys = list(output_data.keys())[:30]
        snippet = {k: output_data[k] for k in snippet_keys}
    elif isinstance(output_data, list):
        snippet = output_data[:5]
    else:
        snippet = output_data

    return {
        "script_path": str(script_abs),
        "output_path": str((root / output_path).resolve()) if output_path else "",
        "output_size_bytes": output_size,
        "output_present": output_present,
        "exit_code": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-2000:],
        "stderr_tail": (proc.stderr or "")[-2000:],
        "json_snippet": snippet,
        "verdict": (
            f"Legacy script ran with exit code {proc.returncode}. "
            f"Output {'present' if output_present else 'missing'} "
            f"({output_size} bytes)."
        ),
    }


def _phase_legacy_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "LegacyPhaseScriptRunner", "Legacy Phase Script Runner",
            "Phase-16-19 / Migration",
            "Subprocess-run a pre-WARP.md analysis script under "
            "`scripts/phase{N}/` and parse its produced JSON output. "
            "Used by retroactive Phase-16/17/18/19 graph migrations to "
            "make legacy analyses re-runnable + visible in the Jobs "
            "panel without rewriting their internals.",
            inputs=[],
            outputs=[
                {"name": "script_path", "type": "text"},
                {"name": "output_path", "type": "text"},
                {"name": "output_size_bytes", "type": "number"},
                {"name": "output_present", "type": "any"},
                {"name": "exit_code", "type": "number"},
                {"name": "stdout_tail", "type": "text"},
                {"name": "stderr_tail", "type": "text"},
                {"name": "json_snippet", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "script_path": {"type": "string", "default": "",
                                     "description": "Repo-relative path of the .py script (e.g. scripts/phase19/omnibus.py)."},
                    "output_path": {"type": "string", "default": "",
                                     "description": "Repo-relative path of the JSON file the script writes (e.g. reports/phase19_omnibus.json)."},
                    "timeout_s": {"type": "integer", "default": 1200, "minimum": 30,
                                   "description": "Subprocess timeout in seconds."},
                },
            },
            fn=_legacy_phase_script_runner,
        ),
    ]


__all__ = [
    "_legacy_phase_script_runner",
    "_phase_legacy_node_defs",
]
