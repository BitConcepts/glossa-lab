"""Experiment Graph Nodes: Phase 430 (Spec 068 —
Yadav's Zipf fit re-measured on the Shakti
corpus: Spec 053's frozen control-systems
comparison executed as its successor under
Amendment S-053).

  IndusPhase430YadavZipfControls    Phase-430:
  step 0 (input integrity, estimator self-test,
  Shakti intake gates S1 and S2 with the
  successor's own restricted census, the limb-B
  population act, the control set entered whole
  as cited data, census floors) and, gates
  passed, every system fitted under Spec 053's
  one frozen estimator, the frozen comparison
  rule on the primary fit, and the section 6
  sensitivities in full.

The node serves the phase's committed results JSON
(reports/phase430_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
068-yadav-zipf-controls-successor/freeze.md
(digest ab890859...); the frozen spec's contract
registration is OSF https://osf.io/3pbwe/.
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
                capture_output=True, text=True, timeout=3600,
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
    ("IndusPhase430YadavZipfControls",
     "phase430_yadav_zipf_controls.py",
     "phase430_results.json",
     "Phase-430 Yadav Zipf Controls Successor (spec 068)",
     "Phase-430 (spec 068): execution of the frozen Spec "
     "068 contract — step 0 in order: gate 0.1 input "
     "integrity against the freeze pins (the claim file "
     "at its DD-068-8 re-pinned hash); gate 0.2 the "
     "estimator self-test by Phase-413's own functions; "
     "gates 0.3-0.4 the Shakti intake gates S1 and S2 "
     "asserted on the restricted-local files (both "
     "SHA-256 pins recompute; the audit census "
     "reproduces: 5,704 rows, 5,536 analyzable, grades "
     "3,212 / 2,087 / 405, 18,065 tokens, 713 signs, 77 "
     "sites) with this successor's own restricted "
     "census governing; gate 0.5 the population act "
     "under limb B (DD-068-7: the strict-sign-set "
     "restriction dropped openly; the full ICIT sign "
     "inventory of the restricted corpus); gate 0.6 "
     "the four named controls entered whole as cited "
     "data (Mesopotamian numerical signs; heraldic "
     "charges from the Dering Roll; the synthetic "
     "emblem inventory, Yule-Simon rho 0.10, seed "
     "20261021, 99 replicates; Linear B as the "
     "linguistic positive control); gate 0.7 the "
     "census floors. Every system is then fitted "
     "under Spec 053's one frozen estimator and the "
     "frozen comparison rule (epsilon = 0) assigns "
     "the headline on the primary fit alone; the "
     "grade sensitivity and subsampling tables are "
     "reported in full beside it. The result is a "
     "new baseline on the Shakti corpus and a "
     "strength label for the recorded fit; it "
     "neither confirms nor corrects any Phase-43 "
     "quantity. CPU."),
]


def _phase430_node_defs():
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
