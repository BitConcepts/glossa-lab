"""Experiment Graph Nodes: Phase 437 (Spec 052 —
Farmer, Sproat & Witzel's "not writing" thesis:
the amended D-01 arm A, battery NB-1 on the
Shakti corpus layer).

  IndusPhase437FarmerNB1   Phase-437: the amended
  step-0 gates in order (A the corpus pin —
  sanitized_corpus.json at 345241b1... and the
  row-grades file at 02394241..., restricted-local;
  B population reproduction — the primary set
  under Spec 068's step-0 limb at 3,045 rows /
  11,805 tokens / 557 signs; C determinism — the
  battery run twice under seed 43052, identical
  outputs; D thinness NB-1.9), then battery NB-1
  exactly as the frozen amendment specifies
  (position classes initial/terminal/medial;
  classifiable iff N >= 20; STRONG >= 2/3,
  MODERATE >= 1/2; opening-bigram dominance over
  B; the within-sequence permutation null, 999
  permutations, seed 43052, nearest-rank 95th
  percentile), conditions F and O, and the
  amended outcome words (CONSISTENT / INCONSISTENT
  / PARTIAL / TOO THIN) on the primary
  population, with the sensitivity population
  (5,131 rows) run and reported with the same
  prominence when the primary reaches an outcome
  word. No outcome moves the parent claim's
  recorded status.

The node serves the phase's committed results
JSON (reports/phase437_results.json),
recomputing via the phase script when that
script's pinned inputs are present locally.
Freeze: specs/052-farmer-not-writing-soviet/
freeze.md (digest 83658949...); the frozen
spec's contract registration is OSF
https://osf.io/7cu23/.
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
                [sys.executable, str(script), "run"],
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
    ("IndusPhase437FarmerNB1",
     "phase437_farmer_nb1_shakti.py",
     "phase437_results.json",
     "Phase-437 Farmer NB-1 on Shakti (spec 052)",
     "Phase-437 (spec 052): execution of the frozen "
     "amended Spec 052 contract — step-0 gates in "
     "order (A the corpus pin: the Shakti corpus "
     "layer at 345241b1... and its row-grades file "
     "at 02394241..., restricted-local, never in "
     "git; B population reproduction under Spec "
     "068's step-0 limb: primary 3,045 rows / "
     "11,805 tokens / 557 signs, sensitivity 5,131 "
     "rows; C determinism: battery run twice, seed "
     "43052, identical outputs; D thinness NB-1.9: "
     ">= 30 sequences of length >= 3 and >= 10 "
     "classifiable signs), then battery NB-1 as "
     "frozen (classes initial/terminal/medial over "
     "sequences of length >= 2, length-1 sequences "
     "counted separately; classifiable iff "
     "N >= 20; STRONG at rate >= 2/3, MODERATE at "
     ">= 1/2; opening-bigram dominance over B; "
     "permutation null 999 permutations, seed "
     "43052, nearest-rank 95th percentile), "
     "conditions F (dedicated final sets) and O "
     "(opening formula, count floor 10), outcome "
     "words CONSISTENT / INCONSISTENT / PARTIAL "
     "under the amendment's re-pointed semantics, "
     "sensitivity run with the same prominence. "
     "The parent claim stands contradicted as "
     "recorded; no outcome is a verdict on the "
     "thesis. Outcome as recorded in "
     "reports/phase437_results.json. CPU."),
]


def _phase437_node_defs():
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
