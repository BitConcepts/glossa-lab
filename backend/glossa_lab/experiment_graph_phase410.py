"""Experiment Graph Nodes: Phase 410 (Spec 043 —
PRED-2026-012 at full population, corrected registry
frame; step 0).

  IndusPhase410Pred012Step0    Phase-410: step 0 only
  (sources and pins; enumeration with re-derivation
  and census reconciliation; the provenance gate,
  check 0.3; recorded-output verification not
  reached), under the campaign's Wave 3 execution
  order, in which the step-0 provenance adjudication
  runs first and no Phase 5 assignment is looked up
  before the gate has passed.

The node serves the phase's committed results JSON
(reports/phase410_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
043-pred-2026-007-registry-frame/freeze.md (digest
8a8a334f...); the frozen spec's contract registration
is OSF https://osf.io/vmcra/.
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
    ("IndusPhase410Pred012Step0",
     "phase410_pred012_step0.py",
     "phase410_results.json",
     "Phase-410 PRED-2026-012 Step 0 (spec 043)",
     "Phase-410 (spec 043): execution of the frozen Spec "
     "043 contract at step 0 — check 0.1 sources and pins "
     "against the freeze record, check 0.2 enumeration of "
     "the ITM population from the canonical sign registry "
     "with full re-derivation from the pinned builder rule "
     "and census reconciliation, then check 0.3, the "
     "documentary provenance gate on the ITM codes "
     "(evidence set D1-D4, three limbs, the DD-043-10 "
     "standard). Outcome (2026-10-21): checks 0.1 and 0.2 "
     "PASS (803 rows; ITM = P056, P324, P378, P385; "
     "re-derivation exact); check 0.3 FAIL on all three "
     "limbs — the produced documents (Fuls 2013; Wells "
     "2015) define the ICTM class by cluster-final "
     "behaviour from positional distribution, state only "
     "positional bases for the signs (and no basis for "
     "W231), and assign different functions than the "
     "builder table (the published ICTM class is signs "
     "060, 001, 002). The execution closed PROVENANCE - "
     "CANNOT BE RUN AS WRITTEN, unscored; check 0.4 was "
     "not reached and no Phase 5 assignment was looked "
     "up. PRED-2026-012 stands PENDING. CPU."),
]


def _phase410_node_defs():
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
