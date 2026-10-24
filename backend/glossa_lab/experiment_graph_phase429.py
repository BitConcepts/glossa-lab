"""Experiment Graph Nodes: Phase 429 (Spec 067 —
the seal/tablet difference on the enlarged join;
Spec 059's question re-run against the Spec 066
merged catalogue layer v2).

  IndusPhase429F1EnlargedJoin    Phase-429: step 0
  (input integrity with layer v2 asserted on the
  local file, original-join reproduction, object-ID
  join census against layer v2, the mandatory
  type-fill census, gate comparison) and,
  gate-passed only, the frozen Phase-136 test on
  the enlarged set.

The node serves the phase's committed results JSON
(reports/phase429_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
067-f1-enlarged-join/freeze.md (digest
73463ab9...); the frozen spec's contract registration
is OSF https://osf.io/qsthg/.
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
    ("IndusPhase429F1EnlargedJoin",
     "phase429_f1_enlarged_join.py",
     "phase429_results.json",
     "Phase-429 F1 Enlarged Join (spec 067)",
     "Phase-429 (spec 067): execution of the frozen Spec "
     "067 contract — step 0 in order: gate 0.1 input "
     "integrity against the freeze pins and the DD-067-9 "
     "sources, the merged catalogue layer v2 asserted on "
     "the local file first (9,741 rows, 5,529 distinct "
     "objects); gate 0.2 original concordance join "
     "reproduced exactly against the vols. 1-2 layer "
     "(5,679 / 2,895 / 2 / 2,782); gate 0.3 the "
     "object-identifier join census against layer v2 "
     "through the Phase-130 schema (provenance.object_id "
     "only; string identity never a key); gate 0.4 the "
     "mandatory type-fill census on the newly joined "
     "objects and the whole joined set, with the "
     "resulting eligible seal/tablet strata; gate 0.5 "
     "the gate comparison against the bar adopted at "
     "DD-067-7 (joined share at least 61.0%, at least "
     "3,465 of 5,679 rows, carried from Spec 059). "
     "Outcome (2026-10-22): gates 0.1-0.5 PASS — the "
     "join joined 4,676 of 5,679 rows (82.34%); the "
     "frozen Phase-136 flow on the enlarged set "
     "returned REPLICATED (MH odds ratio 2.452, 95% CI "
     "[1.965-3.058], family-adjusted q = 0.0001; LOSO: "
     "no site load-bearing). The per-row census "
     "against layer v2 stays restricted-local (spec "
     "section 7.3). CPU."),
]


def _phase429_node_defs():
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
