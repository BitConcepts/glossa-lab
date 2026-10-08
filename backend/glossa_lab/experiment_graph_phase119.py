"""Experiment Graph Nodes: Phase-119 (spec 018) — PRED-2026
readiness harness.

Ledger-sequence Phase-119 (2026-10-07): the evaluation
harness for the pre-registered PRED-2026-001..003, built so
it fires the day a genuinely independent corpus lands.
Frozen evaluability matrix (ICIT lineage is
derivation-adjacent and never qualifies), frozen dedup
protocol (stages A/B/C), mechanical scoring of the
registered criteria, verdict lock, and the labelled dry-run
regime (dry run on the Phase-115 ICIT converted layer only;
no prediction is evaluated by this phase).

  IndusPhase119PredHarness
      fixture self-checks + dry run + reports
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


def _phase119_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase119PredHarness",
         "Phase-119 PRED-2026 Readiness Harness (dry run)",
         "phase119_pred_harness.py", [],
         "phase119_pred_harness_results.json",
         "Phase-119 (spec 018): evaluation harness for the "
         "pre-registered PRED-2026-001..003. Adapters for the "
         "three awaited independent source classes (RMRL "
         "concordance, image-derived transcriptions, future "
         "concordance) with provenance logging; frozen dedup "
         "(exact / sentinel-normalized / near-duplicate); "
         "mechanical scoring of the registered criteria under "
         "the section 4 evaluability gate and section 6.5 "
         "verdict lock. This node runs fixture self-checks and "
         "the labelled dry run on the non-independent Phase-115 "
         "ICIT layer only — it evaluates no prediction. CPU."),
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
