"""Experiment Graph Nodes: Phase-118 (spec 017) — within-
compilation validation battery v2 (W1-primary, cross-fit W3).

Ledger-sequence Phase-118 (2026-10-07): the redesign of spec
016's battery, rejected at Phase-117 calibration (STRICT94
LOO VALIDATED 2/94; W3 PASS 3/94 under its LOO-minus-self
reference and p <= 0.05 donor leg; KUR113 gate passed
vacuously on universal indeterminacy). Holdat-internal
instruments only: W1 split-half positional cross-fit as the
PRIMARY instrument (carried verbatim; frozen seed-117
partition asserted at 3,531 / 3,471 tokens), W3 junction
coherence rebuilt cross-fit (junction model and phi from the
opposite partition half; donor-permutation null retained per
direction with median-donor bands; per-direction junction
floor 2), W4 site-stratum stability as a FAIL-guard. Gates
with teeth precede any run of the 44: positive — VALIDATED
share over the judgeable core J94 (asserted 67) >= 0.50;
negative — over JKUR (asserted 29), VALIDATED = 0 and DEMOTE
share >= 0.25, so universal indeterminacy fails the gate.
A pass earns `validated_within_compilation` (spec 017
section 9: internal coherence within Holdat, explicitly not
independent validation); the phase validates or demotes,
never promotes.

  IndusPhase118WithinCompilationValidation
      partition + judgeability + phi + calibration + main run + reports
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


def _phase118_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase118WithinCompilationValidation",
         "Phase-118 Within-Compilation Validation Battery v2 (44 flagged anchors)",
         "phase118_within_battery.py", [],
         "phase118_within_battery_results.json",
         "Phase-118 (spec 017): within-compilation validation "
         "v2 of the 44 Phase-109 SA-lineage flagged anchors — "
         "the W1-primary redesign of spec 016. Frozen seed-117 "
         "split-half partition (asserted 3,531 / 3,471 tokens); "
         "W1 positional cross-fit primary, W3 junction "
         "coherence rebuilt cross-fit with per-direction phi "
         "and donor-permutation null, W4 stratum stability as "
         "FAIL-guard. Judgeability asserted (J94 = 67, "
         "JKUR = 29); calibration gates (positive share over "
         "J94 >= 0.50; negative VALIDATED = 0 and DEMOTE share "
         "over JKUR >= 0.25) precede the main run; a failed "
         "gate rejects the battery and the 44 are never run. "
         "Pass = validated_within_compilation (internal "
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
