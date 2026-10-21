"""Experiment Graph Nodes: Phase 403 (Spec 039 —
gazetteer period assignment: published determinations
only, exactly as frozen).

  IndusPhase403GazetteerAssignment    Phase-403: input
  integrity (fail-closed), the frozen mapping table
  applied to the assembled published determinations,
  Output A (the assigned gazetteer), and the margins
  verification step confined to the period-eligibility
  gate

The node serves the phase's committed results JSON
(reports/phase403_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
039-gazetteer-period-assignment/freeze.md (digest
ec53a841...); the frozen spec's own contract
registration is OSF https://osf.io/w38ha/ (filed
2026-10-20, pending the owner's approval click).
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
    ("IndusPhase403GazetteerAssignment",
     "phase403_gazetteer_assignment.py",
     "phase403_results.json",
     "Phase-403 Gazetteer Period Assignment (spec 039)",
     "Phase-403 (spec 039): execution of the frozen Spec 039 "
     "contract — the 30 gazetteer sites receive program "
     "period assignments from published determinations only "
     "(owner decision D2, Option 1; no program-derived "
     "assignments, no spine-date inference), mapped through "
     "the frozen mapping table (Early / Mature / Late "
     "Harappan labels), each assignment carrying its "
     "evidence (citation, locator, published value, period "
     "scheme) and contested flags where determinations "
     "disagree. Undetermined sites stay null with a "
     "recorded reason code. The verification step re-runs "
     "the Phase-395 period-eligibility gate (rule F031-C10) "
     "over the assigned gazetteer and records the "
     "link-mass floor closure. The labels are finding aids, "
     "not dating evidence; the act changes no study "
     "outcome; Q7 still fails its link-mass floors (link "
     "mass 2 sites / 1 pair against floors of 8 eligible "
     "sites / 10 linked pairs); Q6 remains "
     "NOT-YET-TESTABLE. Outcome (2026-10-20): 11 of 30 "
     "sites assigned, 1 contested (banawali), 19 blank "
     "(8 NO_PUBLISHED_DETERMINATION, 2 "
     "UNMAPPED_SCHEME_VALUE, 9 OUTSIDE_LABEL_SET); "
     "period-eligible sites 8 with contested counted, 7 "
     "with contested excluded; the step closes at the "
     "link-mass floor. CPU."),
]


def _phase403_node_defs():
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
