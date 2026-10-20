"""Experiment Graph Nodes: Phase 401 (Spec 038 —
PRED-2026-007: full-population ITM census and
scoring, exactly as frozen).

  IndusPhase401Pred007Census    Phase-401: step 0
  (registration record and sources verified;
  enumeration and held-record verification —
  fail-closed, in the frozen order), then — only
  behind a full step-0 pass — the registered
  scoring

The node serves the phase's committed results JSON
(reports/phase401_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
038-pred-2026-007-full-population/freeze.md (digest
b54571d8...); the prediction's registration is the
PRED register entry itself (PRED-2026-007,
registered 2026-04-22; no OSF preregistration of its
own); the frozen spec's own contract registration
is OSF https://osf.io/bkqeh/.
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
    ("IndusPhase401Pred007Census",
     "phase401_pred007_step0.py",
     "phase401_results.json",
     "Phase-401 PRED-2026-007 Full-Population Census (spec 038)",
     "Phase-401 (spec 038): execution of the frozen Spec 038 "
     "contract — PRED-2026-007 (at least 70% of ITM-coded signs "
     "TERMINAL or in TERMINAL clusters) taken to its "
     "full-population census exactly as frozen. Step 0 ran "
     "first, fail-closed, in the frozen order: 0.1 the "
     "registration record and every source verified against "
     "the freeze record (the PRED-2026-007 entry standing as "
     "registered; all four cited hashes matched; the "
     "coding-source readings in the cited form) — PASS; 0.2 "
     "the enumeration read all 611 records of the primary "
     "(reports/indus_cgsa_cluster_analysis.json, "
     "data.a[].icit_function) mechanically and returned zero "
     "ITM-coded signs, and the held-record verification "
     "failed at the same pass: P385's record carries an empty "
     "icit_function value, and P378 has no record in the "
     "primary at all. In this file the field is not a coded "
     "field: 579 of its 611 values are empty and 32 are "
     "free-text decipherment glosses; no record carries ITM "
     "or LOG. The frozen rule therefore closed the study at "
     "step 0.2 as CANNOT BE RUN AS WRITTEN, unscored; check "
     "0.3 never ran and the Phase 5 output was never read for "
     "assignments. PRED-2026-007's PARTIALLY CONFIRMED "
     "wording stands as the pre-execution record; the "
     "prediction is neither confirmed nor refuted by this "
     "closure. CPU."),
]


def _phase401_node_defs():
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
