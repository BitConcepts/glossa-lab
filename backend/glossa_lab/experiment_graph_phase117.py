"""Experiment Graph Nodes: Phase-117 (spec 016) — within-
compilation validation battery.

Ledger-sequence Phase-117 (2026-10-07): the battery Phase-116's
R-NONE licensed — validation within a single compilation.
Holdat-internal instruments only: W1 split-half positional
cross-fit (frozen seed-117 partition, halves asserted at
3,531 / 3,471 tokens), W3 junction coherence vs a seeded
donor-permutation null (phi = 10th percentile of STRICT94
leave-one-out self-scores), W4 site-stratum stability; W2
dropped as decision-bearing at design. Calibration gates
(STRICT94 LOO VALIDATED >= 47/94; KUR113 <= 5/113) precede any
run of the 44 flagged anchors. A pass earns
`validated_within_compilation` (spec section 9: internal
coherence within Holdat, explicitly not independent
validation); the phase validates or demotes, never promotes.

  IndusPhase117WithinCompilationValidation
      partition + phi + calibration + main run + reports
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _run(script: str, args: list[str], report: str, timeout: int = 7200):
    s = _SCRIPTS / script
    rp = _REPORTS / report
    if not s.exists():
        return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(s), *args], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    if rp.exists():
        try:
            return json.loads(rp.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase117_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase117WithinCompilationValidation",
         "Phase-117 Within-Compilation Validation Battery (44 flagged anchors)",
         "phase117_within_battery.py", [],
         "phase117_within_battery_results.json",
         "Phase-117 (spec 016): within-compilation validation of "
         "the 44 Phase-109 SA-lineage flagged anchors. Frozen "
         "seed-117 split-half partition (asserted 3,531 / 3,471 "
         "tokens); W1 positional cross-fit, W3 junction coherence "
         "with donor-permutation null and phi floor, W4 "
         "site-stratum stability. Calibration gates STRICT94 "
         "LOO >= 47/94 and KUR113 <= 5/113 precede the main run; "
         "a failed gate rejects the battery and the 44 are never "
         "run. Pass = validated_within_compilation (internal "
         "coherence within Holdat only, spec section 9). CPU."),
    ]
    nodes = []
    for nid, name, script, args, report, desc in specs:
        def fn(i, p, s=script, a=args, r=report):
            return {**_run(s, a, r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}}, fn=fn))
    return nodes
