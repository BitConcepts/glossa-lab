"""Experiment Graph Nodes: Phase 396 (Spec 032 —
PRED-2026-006: the Harappa breakdown, computed exactly as
registered).

  IndusPhase396Pred006Scoring    Phase-396: step 0
  (provenance checks, fail-closed), then — only behind a
  full step-0 pass — the registered scoring

The node serves the phase's committed results JSON
(reports/phase396_results.json), recomputing via the phase
script when that script's pinned inputs are present locally.
Freeze: specs/032-pred-2026-006-harappa-breakdown/freeze.md
(digest 34cd6230...); registered before execution at OSF
https://osf.io/3htn8/ (DOI 10.17605/OSF.IO/3HTN8).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _serve(script_name: str, results_name: str) -> dict:
    script = _SCRIPTS / script_name
    results = _REPO / "reports" / results_name
    if script.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=1200,
                cwd=str(_REPO))
            if r.returncode == 0 and results.exists():
                return {"source": "script_recomputed",
                        **json.loads(results.read_text("utf-8"))}
        except Exception:  # noqa: BLE001
            pass
    if results.exists():
        return {"source": "committed_results",
                **json.loads(results.read_text("utf-8"))}
    return {"error": f"{results_name} not found"}


_NODE_SPECS = [
    ("IndusPhase396Pred006Scoring", "phase396_pred006_step0.py",
     "phase396_results.json",
     "Phase-396 PRED-2026-006 Harappa Breakdown (spec 032)",
     "Phase-396 (spec 032): execution of the frozen Spec 032 "
     "contract — step 0 provenance checks in the frozen order "
     "(3.1 trained INITIAL set reconstructed from the recorded "
     "global_class_stability lineage and frozen; 3.2 the "
     "withholding verified against the recorded training "
     "corpus; 3.3 sign identity fixed through the existing "
     "crosswalks), the step-0 record written and hashed "
     "before any counting, and — only behind a full step-0 "
     "pass — the registered scoring of PRED-2026-006 "
     "(share of trained INITIAL signs with Harappa start "
     "rate >= 0.40; CONFIRMED at >= 70%). In this execution "
     "step 0 closed the study at check 3.2: CANNOT BE RUN "
     "AS WRITTEN — the recorded classification trained on "
     "the combined corpus, in which Yajnadevam Harappa "
     "inscriptions sat; no scoring ran. CPU."),
]


def _phase396_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    nodes = []
    for nid, script_name, results_name, name, desc in _NODE_SPECS:
        def fn(i, p, _s=script_name, _r=results_name):
            return {**_serve(_s, _r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
