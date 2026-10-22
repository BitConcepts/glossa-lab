"""Experiment Graph Nodes: Phase 411 (Spec 045 —
Hunt's three parts: pattern, or meanings?; step 0).

  IndusPhase411HuntDepictedStep0    Phase-411: step 0
  only (input integrity; positional reproduction;
  population census and freeze-order proof not
  reached), under the campaign's Wave 3 execution
  order in which step 0 runs before the Asset A build.

The node serves the phase's committed results JSON
(reports/phase411_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
045-hunt-depicted-kinds/freeze.md (digest
5d8254dd...); the frozen spec's contract registration
is OSF https://osf.io/4mt9k/.
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
    ("IndusPhase411HuntDepictedStep0",
     "phase411_hunt_depicted_step0.py",
     "phase411_results.json",
     "Phase-411 Hunt Depicted Kinds Step 0 (spec 045)",
     "Phase-411 (spec 045): execution of the frozen Spec "
     "045 contract at step 0 only — gate 0.1 input "
     "integrity against the freeze pins, then gate 0.2 "
     "positional reproduction: the pinned positional "
     "record's quantities (805/2,267 formula count; "
     "40/61/20 strong-sign classes) reproduced from the "
     "pinned corpus under the recorded framework. "
     "Outcome (2026-10-21): gate 0.1 PASS; gate 0.2 "
     "FAIL — the pinned corpus carries 3,463 "
     "inscriptions of length >= 3 against the recorded "
     "2,267, the strong-sign classes are exhibited by "
     "no record of record, and the corpus the recorded "
     "quantities belong to (Firestore V3, 3,137 "
     "sequences) is absent from the tree. The execution "
     "closed INVALID in the frozen wording; gates 0.3 "
     "and 0.4 were not reached, Asset A was not built, "
     "and no model was fitted. The claim stands as "
     "recorded. CPU."),
]


def _phase411_node_defs():
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
