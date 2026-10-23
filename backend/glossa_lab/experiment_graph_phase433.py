"""Experiment Graph Nodes: Phase 433 (Spec 070 —
the Hunt opening signs successor on the Shakti
corpus: are the opening-strong signs the animal
signs, in re-scoped form).

  IndusPhase433OpeningSigns   Phase-433: the
  step-0 gates in order (0.1 Asset A asserted
  against Spec 069's executed record; 0.2 the
  Shakti intake under P-F1 S1/S2; 0.3 input
  integrity; 0.4 the population enumerated and
  published in Wells space before any join, every
  sign keyed under the freeze-fixed route of
  DD-070-9, an unkeyable sign closing as
  POPULATION NOT KEYED under DD-070-11; 0.5 the
  comparison census and coverage; 0.6 the
  freeze-order proof), then the single counting
  run: the section 2 battery applied new, R1/R2
  with Fisher exact tests, the section 4.3
  precedence, and sensitivities S-A/S-B/S-C.

The node serves the phase's committed results JSON
(reports/phase433_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/070-hunt-opening-
signs-successor/freeze.md (digest 763108f8...); the
frozen spec's contract registration is OSF
https://osf.io/nghs5/.
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
    ("IndusPhase433OpeningSigns",
     "phase433_opening_signs.py",
     "phase433_results.json",
     "Phase-433 Opening Signs on Shakti (spec 070)",
     "Phase-433 (spec 070): execution of the frozen Spec "
     "070 contract - step-0 gates in order (0.1 Asset A "
     "frozen under Spec 069 and its digest recomputing "
     "to 95231935...; 0.2 the Shakti intake under P-F1 "
     "S1/S2 against the intake record; 0.3 input "
     "integrity; 0.4 the opening-strong set enumerated "
     "in full in Wells space and published before any "
     "join, keyed under DD-070-9, an unkeyable sign "
     "closing as POPULATION NOT KEYED under DD-070-11; "
     "0.5 the comparison census and coverage; 0.6 the "
     "freeze-order proof), then one counting run: the "
     "recovered Phase-43 battery applied new to the "
     "documented-lineage rows (threshold-only; no "
     "chance-baseline step, G5), R1/R2 with Fisher "
     "exact tests under the frozen section 4.3 "
     "precedence, sensitivities S-A (contested "
     "included), S-B (unicorn removed), S-C "
     "(documented + corroborated, classes re-derived). "
     "Outcome as recorded in "
     "reports/phase433_results.json. CPU."),
]


def _phase433_node_defs():
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
