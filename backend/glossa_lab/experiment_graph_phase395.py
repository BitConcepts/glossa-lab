"""Experiment Graph Nodes: Phase 395 (Spec 031 — Spec 027
Stage 2 / Q7 provenanced-material networks).

  IndusPhase395Q7Execution    Phase-395: digitisation design
  step, margins step (population record hashed before any
  response), outcome step for any viable arm

The node serves the phase's committed results JSON
(reports/phase395_results.json), recomputing via the phase
script when that script's pinned inputs are present locally
(the digitisation inputs live in the gitignored local store
corpora/downloads/spec031_phase395/ and never enter git).
Freeze: specs/031-stage2-q7-provenance-networks/freeze.md
(digest f63167fc...); registered before execution at OSF
https://osf.io/jtwvc/ (DOI 10.17605/OSF.IO/JTWVC).
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
    ("IndusPhase395Q7Execution", "phase395_q7_execution.py",
     "phase395_results.json",
     "Phase-395 Q7 Provenanced-Material Networks (spec 031)",
     "Phase-395 (spec 031): execution of the frozen Q7 design "
     "— digitisation design step (Law 2011 method split "
     "under the D8 audit's named instrumental methods; "
     "ceramic posture audit; bead/craft source record), "
     "margins step (Stage 0 gazetteer coordinate and period "
     "screens, primary-tier link construction, per-arm "
     "eligibility and viability, population record hashed "
     "before any response), and the section 5 outcome step "
     "for any arm that passes margins. Both arms closed at "
     "margins in this execution (bead/craft "
     "NOT-YET-TESTABLE; ceramic NOT ESTIMABLE under DD-7); "
     "no response was computed. CPU."),
]


def _phase395_node_defs():
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
