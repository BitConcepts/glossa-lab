"""Experiment Graph Nodes: Phase 394 (Spec 030 — Q6
chronology-spine extension).

  IndusPhase394SpineExtension    Phase-394: spine extension
  build (routes R5 -> R1 -> R2 -> R4 -> R3) + Q6 re-test

The node serves the phase's committed results JSON
(reports/phase394_results.json), recomputing via the phase
script when that script's pinned inputs are present locally
(the route inputs live in the gitignored local store
corpora/downloads/spec030_phase394/ and never enter git).
Freeze: specs/030-q6-chronology-spine-extension/freeze.md;
registered before execution at OSF https://osf.io/bge3k/
(DOI 10.17605/OSF.IO/BGE3K).
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
    ("IndusPhase394SpineExtension", "phase394_spine_extension.py",
     "phase394_results.json",
     "Phase-394 Q6 Chronology-Spine Extension + Re-test (spec 030)",
     "Phase-394 (spec 030): audited extension of the Phase-391 "
     "chronology spine through the frozen routes R5 (XRONOS "
     "re-retrieval) -> R1 (origin-record tracing) -> R2 "
     "(c14bazAAR source-database audit) -> R4 (TwoRains "
     "supplement audit) -> R3 (targeted published-date "
     "extraction, internal-spine-only), short-lived-first "
     "tracing, lab-code dedupe, then the Q6 timing-support "
     "re-test: the stage0-freeze section 4 assessment verbatim "
     "on the extended spine, reported as frozen and excluding "
     "CONTESTED rows. Margins/metadata only; mints no timing "
     "verdict. CPU."),
]


def _phase394_node_defs():
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
