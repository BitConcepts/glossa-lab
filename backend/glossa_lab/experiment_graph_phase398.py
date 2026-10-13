"""Experiment Graph Nodes: Phase 398 (Spec 034 —
Matched-Object Attribution of the settled Phase-125
cross-compilation disagreement).

  IndusPhase398MatchedObjectAttribution    Phase-398:
  step 0 bridge census + frozen gate; behind the gate,
  step 1 attribution under the frozen lines

The node serves the phase's committed results JSON
(reports/phase398_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
034-matched-object-attribution/freeze.md (digest
696fd185...); registered before execution at OSF
https://osf.io/zd7uq/ (DOI 10.17605/OSF.IO/ZD7UQ).
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
    ("IndusPhase398MatchedObjectAttribution",
     "phase398_matched_object_attribution.py",
     "phase398_results.json",
     "Phase-398 Matched-Object Attribution (spec 034)",
     "Phase-398 (spec 034): execution of the frozen Spec 034 "
     "contract — step 0 builds the object bridge through the "
     "three frozen routes (the CISI catalogue layer; the "
     "Mahadevan side's published object references admitted "
     "through the Phase-130 intake schema and joined on the "
     "published CISI object ID — Holdat cisi_number is never "
     "a join key; the 44 Phase-128 dossiers) and applies the "
     "frozen gate (>= 150 matched objects with texts of "
     "three or more signs in both compilations; below it, "
     "TOO THIN TO ATTRIBUTE with the census as the finding). "
     "Step 1, behind the gate only, measures Phase-125's own "
     "statistic (total variation, floor 8, PRIMARY arm) on "
     "the matched subset and decomposes the remainder in "
     "Phase-131's categories, under the frozen verdict lines "
     "(<= 0.20 composition; >= 0.32 transcription; between, "
     "a split attribution). The settled Phase-125 verdict "
     "is never re-judged. CPU."),
]


def _phase398_node_defs():
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
