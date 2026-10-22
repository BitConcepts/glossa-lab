"""Experiment Graph Nodes: Phase 421 (Spec 059 —
the seal/tablet difference on a better join; F1
rebuilt through object identifiers).

  IndusPhase421F1ObjectJoin    Phase-421: step 0
  (input integrity, original-join reproduction,
  object-ID join census, gate comparison) and,
  gate-passed only, the frozen Phase-136 test on
  the enlarged set.

The node serves the phase's committed results JSON
(reports/phase421_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
059-f1-object-join/freeze.md (digest
bba1caca...); the frozen spec's contract registration
is OSF https://osf.io/yfw7h/.
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
    ("IndusPhase421F1ObjectJoin",
     "phase421_f1_object_join.py",
     "phase421_results.json",
     "Phase-421 F1 Object-ID Join (spec 059)",
     "Phase-421 (spec 059): execution of the frozen Spec "
     "059 contract — step 0 in order: gate 0.1 input "
     "integrity against the freeze pins and the DD-059-9 "
     "object-identifier sources; gate 0.2 original "
     "concordance join reproduced exactly (5,679 / 2,895 "
     "/ 2 / 2,782); gate 0.3 the object-identifier join "
     "census through the Phase-130 schema (provenance."
     "object_id only; string identity never a key), "
     "validated pass (5,018 records); gate 0.4 the gate "
     "comparison against the bar adopted at DD-059-7 "
     "(joined share at least 61.0%, at least 3,465 of "
     "5,679 rows). Outcome (2026-10-21): gates 0.1-0.3 "
     "PASS; gate 0.4 FAIL — the object-ID join joined "
     "2,899 of 5,679 rows (51.05%), so the execution "
     "closed CLOSED AT STEP 0 — JOIN GATE NOT MET in "
     "the frozen wording, with the census published as "
     "the finding. No F1 quantity was computed; "
     "STUDY-SPEC-024/F1 stands exactly as recorded. CPU."),
]


def _phase421_node_defs():
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
