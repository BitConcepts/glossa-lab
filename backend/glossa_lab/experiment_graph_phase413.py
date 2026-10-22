"""Experiment Graph Nodes: Phase 413 (Spec 053 —
Yadav's Zipf fit: what is a curve fit worth?;
design D-07, arm A only).

  IndusPhase413YadavZipfControls    Phase-413:
  step 0 only (input integrity; estimator
  self-test; strict corpus identification —
  gates 0.4 and 0.5 not reached), closing as
  STRICT CORPUS NOT PINNABLE.

The node serves the phase's committed results JSON
(reports/phase413_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
053-yadav-zipf-controls/freeze.md (digest
fd2d5cb8...); the frozen spec's contract
registration is OSF https://osf.io/s9yfe/
(approved and public).
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
    ("IndusPhase413YadavZipfControls",
     "phase413_yadav_zipf_controls.py",
     "phase413_results.json",
     "Phase-413 Yadav Zipf Controls Step 0 (spec 053)",
     "Phase-413 (spec 053): execution of the frozen "
     "Spec 053 contract at step 0 — gate 0.1 input "
     "integrity against the freeze pins, gate 0.2 "
     "the estimator self-test for the Zipf-Mandelbrot "
     "estimator the freeze specified completely "
     "(DD-053-11; fitted alpha 1.256 and q 2.72 "
     "against the planted 1.20 / 2.0, within "
     "tolerance), then gate 0.3 strict corpus "
     "identification. Outcome (2026-10-21): gate "
     "0.1 PASS; gate 0.2 PASS; gate 0.3 FAIL — the "
     "V3 / Mahadevan-lineage layer's data file (the "
     "Firestore 'indusarrays' dump) is absent from "
     "the tree, the V3 loader loads zero sequences, "
     "and no other layer in the tree is the corpus "
     "the Phase-43 record names, so the execution "
     "closed STRICT CORPUS NOT PINNABLE in the "
     "frozen wording. Gates 0.4 and 0.5 were not "
     "reached, no control count was entered, and no "
     "system was fitted. The claim "
     "yadav_2009_arxiv_manual_001 stands exactly as "
     "recorded. CPU."),
]


def _phase413_node_defs():
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
