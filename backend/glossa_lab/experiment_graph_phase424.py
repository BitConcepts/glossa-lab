"""Experiment Graph Node: Phase 424 (Spec 062 —
Spec 028 Arm A: the precision computation,
calibration repair; design D-27, arm A1 only).

  IndusPhase424ArmAPrecisionRepair    Phase-424: the
  precision computation on Phase-393's recorded
  resampling distribution under the frozen Spec 062
  contract (freeze digest 1800de53...; OSF contract
  registration https://osf.io/4m27t/), the successor
  to Spec 061 (Phase-423, closed CANNOT BE RUN AS
  WRITTEN at its gate 0.5) carrying construction
  R-1's repaired calibration, verified at gate
  0.5-R.

The node serves the phase's committed results JSON
(reports/phase424_results.json) only. Unlike the
shorter phases, it does NOT recompute via the phase
script on a node call: the frozen computation is
9,950 trials of the frozen Phase-393 machinery (199
draws x 499 permutations each) on two seeded streams
— a multi-day, checkpointed run that resumes on its
exact Generator stream; a node call is not a place
to launch it. The script
(backend/scripts/phase424_arm_a_precision_calibration_repair.py)
is the executed machinery and its record is the
committed results JSON.
"""
from __future__ import annotations

import json
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _serve(results_name: str) -> dict:
    results = _REPO / "reports" / results_name
    if results.exists():
        return {"source": "committed_results",
                **json.loads(results.read_text("utf-8"))}
    return {"error": f"{results_name} not found"}


_NODE_SPECS = [
    ("IndusPhase424ArmAPrecisionRepair",
     "phase424_results.json",
     "Phase-424 Arm A Precision Computation, Calibration Repair (spec 062)",
     "Phase-424 (spec 062): the precision computation "
     "of design D-27 arm A1 on Phase-393's recorded "
     "resampling distribution for Spec 028's "
     "Harappa-excluded Arm A (INCONCLUSIVE: median "
     "adjusted R^2 0.00878393455594817, interval "
     "[0.004626892186724407, 0.01297407559730989] "
     "straddling the 0.01 margin). A simulation over "
     "recorded data: the recorded site samples are "
     "resampled with replacement at integer multiples "
     "m = 1..25 of their current sizes under the "
     "effect-imposition construction (candidate "
     "(b)'s imposed compositions with construction "
     "R-1's repaired calibration: per-inscription "
     "Dirichlet drawing around the imposed "
     "composition, kappa_i = n_legible(i) - 1, fixed "
     "uniforms from the dedicated calibration "
     "Generator seeded 20261021; boost calibrated "
     "per scenario on [1, 3] to tolerance 1e-6, "
     "verified at gate 0.5-R), 199 trials per grid "
     "point, 199 draws and 499 permutations per "
     "trial, seed 20261021; a trial resolves iff its "
     "interval excludes the 0.01 margin strictly in "
     "its scenario's direction (scenario 1: theta = "
     "the recorded point estimate, downward; "
     "scenario 2: theta = 0.015, upward); a grid "
     "point qualifies at >= 80% of trials resolving; "
     "the product is the smallest qualifying added-"
     "inscription total per scenario — an intake "
     "target. Step 0 gates 0.1-0.4 and 0.5-R run fail-closed "
     "before any trial, including gate 0.3's exact "
     "reproduction of the recorded Arm A summary "
     "from the composite pin. The computation "
     "measures the resolution of a recorded test; "
     "it establishes nothing about the ancient "
     "world, and Arm A2 (the contingent rerun) is "
     "not part of this execution (campaign E-3). "
     "CPU."),
]


def _phase424_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    nodes = []
    for nid, results_name, name, desc in _NODE_SPECS:
        def fn(i, p, _r=results_name):
            return {**_serve(_r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
