"""Experiment Graph Nodes: Phase 409 (Spec 051 —
Roif: the arrow sign — border marker, or city sign?;
design D-10).

  IndusPhase409RoifArrowSign    Phase-409: the full
  execution of the frozen Spec 051 contract — step 0
  (input integrity; the Asset B digest assertion
  against Spec 047's step-1 outcome record, DD-051-14;
  Asset B form and the testable set; the counting
  layer identified, pinned, and its M391 census
  reproduced exactly; the join census; the
  test-population census and floors), closing at
  gate 0.6 as INCONCLUSIVE — the classification is
  the finding. No share was computed.

The node serves the phase's committed results JSON
(reports/phase409_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
051-roif-arrow-sign/freeze.md (digest 818cfa4e...);
the frozen spec's contract registration is OSF
https://osf.io/xnrph/. All products are held under
the Roif gate (spec section 9).
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
    ("IndusPhase409RoifArrowSign",
     "phase409_roif_arrow_sign.py",
     "phase409_results.json",
     "Phase-409 Roif Arrow Sign (spec 051)",
     "Phase-409 (spec 051): execution of the frozen Spec "
     "051 contract — step 0 gates in the frozen order "
     "(input integrity against the freeze pins; Asset B "
     "digest asserted against the digest recorded in "
     "Spec 047's step-1 outcome record, a1a9e484...; "
     "Asset B form, 30 rows, and the testable set "
     "derived by rule, 2 sites; the Holdat counting "
     "layer of record identified, exported in full and "
     "pinned at 62d14d2b..., its M391 census reproducing "
     "the section 1 census exactly, 193 occurrences "
     "over 9 sites; the join census accounting for "
     "every one of the 7,002 records exactly once; the "
     "test-population census and floors), closing at "
     "gate 0.6 as INCONCLUSIVE — the classification is "
     "the finding: 0 testable gateway/border sites "
     "carry M391 (floor 3) and the contrast side is "
     "empty in the test population. No share, ratio, "
     "permutation, or regression quantity was "
     "computed, and the primary test did not run. The "
     "claim stands UNTESTED. All products held under "
     "the Roif gate. CPU."),
]


def _phase409_node_defs():
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
