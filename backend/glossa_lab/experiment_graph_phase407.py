"""Experiment Graph Nodes: Phase 407 (Spec 042 —
Arm B split by object type, a registered primary
variant of Spec 028 Arm B; design D-28).

  IndusPhase407ArmBObjectTypeSplit    Phase-407:
  step 0 (spec section 3 gates 0.1-0.5, in order,
  fail-closed), then the per-stratum primaries
  (spec section 4) if every gate passes.

The node serves the phase's committed results JSON
(reports/phase407_results.json), recomputing via
the phase script when that script's pinned inputs
are present locally. Freeze: specs/
042-arm-b-object-type-split/freeze.md (digest
6be2988d...); the frozen spec's own contract
registration is OSF https://osf.io/tmyzg/
(approved and public, 2026-10-21). Executed
2026-10-21: gates 0.1-0.3 passed; gate 0.4 fired
THIN (the tablet stratum carries at least 20
inscriptions at only 2 of the 6 sites), so the
execution closed with headline THIN, neither
stratum was computed, and gate 0.5 was not
reached. Spec 028 Arm B stands exactly as
recorded (INCONCLUSIVE).
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
    ("IndusPhase407ArmBObjectTypeSplit",
     "phase407_arm_b_object_type_split.py",
     "phase407_results.json",
     "Phase-407 Arm B Object-Type Split (spec 042)",
     "Phase-407 (spec 042): the object-type split of "
     "Spec 028's Arm B, executed 2026-10-21 under the "
     "runnable-experiments campaign (Wave 3). Step 0 "
     "ran in the frozen order: gate 0.1 input integrity "
     "PASS (every spec section 2 pin recomputes); gate "
     "0.2 population reproduction PASS (the frozen flow "
     "reproduces 5,679 / 4,531 / 4,505 / 3,605 / 3,144 / "
     "3,030 and the recorded Arm B analysis set, cell "
     "for cell against the Spec 028 margins audit); gate "
     "0.3 partition census PASS (SEAL 1,768 + TAB 1,262 "
     "= 3,030, no record of any other type). Gate 0.4 "
     "fired THIN: the seal stratum clears the floor at "
     "all 6 sites (minimum Kalibangan, 49), but the "
     "tablet stratum carries at least 20 inscriptions "
     "at only 2 of the 6 sites (Harappa 1,076; "
     "Mohenjo-daro 164; Dholavira 15; Lothal 2; "
     "Chanhu-daro 2; Kalibangan 3), so it is recorded "
     "TOO THIN and, under DD-042-2, the execution "
     "closed with headline THIN: neither stratum was "
     "computed, gate 0.5 was not reached, and no "
     "verdict is recorded. Spec 028's Arm B stands "
     "exactly as recorded (INCONCLUSIVE). This result "
     "is about repertoire association in recorded "
     "data; it is not evidence that any population "
     "moved. CPU."),
]


def _phase407_node_defs():
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
