"""Experiment Graph Nodes: Phase-113 (spec 011) — non-SA validation battery.

Ledger-sequence Phase-113 (2026-10-07): the battery Phase-109
deferred for the 44 SA-lineage anchors it flagged
`pending_non_sa_validation` (H26: SA agreement is not evidence).
Three frozen non-SA tests (cross-corpus consistency,
positional-grammar fit, compositional co-occurrence), calibrated
on the strict SA-independent core (positive, leave-one-out) and
the Phase-110 premise-superseded `kur` cohort (negative) before
the 44 are run; a failed calibration gate rejects the battery
and leaves the anchors file untouched.

  IndusPhase113NonSaValidation  calibration + (gated) main run + reports
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


def _phase113_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase113NonSaValidation",
         "Phase-113 Non-SA Validation Battery (44 flagged anchors)",
         "phase113_nonsa_battery.py", [], "phase113_nonsa44_results.json",
         "Phase-113 (spec 011): frozen non-SA battery (T1 cross-corpus "
         "ICIT-vs-Holdat consistency, T2 positional-grammar fit vs the "
         "strict SA-independent core, T3 compositional co-occurrence) "
         "for the 44 anchors Phase-109 flagged pending_non_sa_validation. "
         "Calibration gates run first (strict-94 leave-one-out VALIDATED "
         ">= 57; kur-113 negative control VALIDATED <= 5); a rejected "
         "battery stops the phase with anchors untouched. Outcomes: "
         "VALIDATED_NON_SA / DEMOTE to CANDIDATE / UNRESOLVED. CPU."),
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
