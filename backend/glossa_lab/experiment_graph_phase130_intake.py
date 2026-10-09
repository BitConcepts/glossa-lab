"""Experiment Graph Nodes: Phase-130 (spec 021) — independent-data
intake pack.

Ledger-sequence Phase-130 (2026-10-08): schema + validator
(license gate) for incoming inscription datasets, the shared
spec 018 section 5 dedup module, evaluability-class
assignment, and the intake runbook whose final stage is the
Phase-119 harness DRY-RUN path only — intake output can
never reach a scorer. Distinct from the legacy Phase-130
decode-blocker node (IndusDecodeBlockerAudit).

  IndusPhase130IntakePack
      synthetic-fixture intake end-to-end + report
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _run(script: str, args: list[str], report: str, timeout: int = 7200):
    s = _SCRIPTS / script
    rp = _REPORTS / report
    if not s.exists():
        return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(s), *args], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    if rp.exists():
        try:
            return json.loads(rp.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase130_intake_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase130IntakePack",
         "Phase-130 Independent-Data Intake Pack (dry run only)",
         "phase130_intake_pack.py", [],
         "phase130_intake_pack_results.json",
         "Phase-130 (spec 021): intake pack for independent "
         "inscription datasets. Versioned intake schema v1, "
         "validator with a hard license gate, shared spec 018 "
         "section 5 dedup module, section 4 evaluability-class "
         "assignment, and a runbook ending at the Phase-119 "
         "harness labelled dry run. This node runs the "
         "synthetic fixture only — it ingests no real dataset "
         "and evaluates no prediction. CPU."),
    ]
    nodes = []
    for nid, name, script, args, report, desc in specs:
        def fn(i, p, s=script, a=args, r=report):
            return {**_run(s, a, r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}}, fn=fn))
    return nodes
