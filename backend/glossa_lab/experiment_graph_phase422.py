"""Experiment Graph Nodes: Phase 422 (Spec 060 —
the Holdat site effect: margin curve and shared
population; design D-23).

  IndusPhase422F2MarginCurve    Phase-422: step 0
  (gates 0.1-0.4), arm 1 (the F2 margin curve, a
  sensitivity display) and arm 2 (per-layer site-effect
  intervals on the shared SEAL population), under the
  frozen Spec 060 contract.

The node serves the phase's committed results JSON
(reports/phase422_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
060-f2-margin-curve/freeze.md (digest
8c04b1a8...); the frozen spec's contract registration
is OSF https://osf.io/8ywxc/.
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
    ("IndusPhase422F2MarginCurve",
     "phase422_f2_margin_curve.py",
     "phase422_results.json",
     "Phase-422 F2 Margin Curve + Shared Population (spec 060)",
     "Phase-422 (spec 060): execution of the frozen Spec "
     "060 contract (design D-23) — step 0 gates 0.1-0.3 "
     "(input integrity against the section 3 pins, both "
     "layers' population reproduction, estimator "
     "regression against both recorded governing "
     "intervals), gate 0.4 shared-population census, "
     "arm 1 (the F2 verdict as a function of the margin "
     "on the fixed grid 0.05/0.075/0.10/0.125/0.15, "
     "labelled sensitivity), and arm 2 (per-layer "
     "governing intervals on the shared population — "
     "six shared sites, type SEAL — compared for "
     "overlap). Outcome (2026-10-21): all gates pass; "
     "the margin curve (sensitivity) reads SUPPORTED "
     "AT 0.05, STRADDLES 0.075, CONTRADICTED AT 0.10 / "
     "0.125 / 0.15 on the governing interval "
     "[0.0589, 0.0778]; on the shared population "
     "(1,516 Holdat / 2,139 ICIT SEAL inscriptions) "
     "the intervals [0.0553, 0.0761] and [0.0837, "
     "0.1084] still exclude each other — COMPOSITION "
     "DOES NOT, stated alongside Spec 034's finished "
     "attribution. No verdict moves: F2 stands "
     "CONTRADICTED at 0.10 and F3 stands SUPPORTED at "
     "0.10, exactly as recorded. CPU."),
]


def _phase422_node_defs():
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
