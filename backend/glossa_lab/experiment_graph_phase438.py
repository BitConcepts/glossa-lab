"""Experiment Graph Nodes: Phase 438 (Spec 054 —
Yadav's opening/closing signs: given a falsifier,
then rerun; the amended falsifier act under
battery NB-1).

  IndusPhase438YadavOpeningClosing   Phase-438:
  the amended step-0 gates in order (pin checks
  against the freeze section 2 pins — mismatch
  INVALID; strict corpus identification and pin —
  the V3 / Mahadevan-lineage layer the Phase-43
  battery ran on, identified mechanically against
  the Phase-43 record's own census, failure
  STRICT CORPUS NOT PINNABLE; thinness — arm 1
  under 30 sequences of length >= 3 or under 10
  classifiable signs, TOO THIN; second arm
  runnability — the Holdat layer pinned, the
  crosswalk pins, arm 2 under 10 classifiable
  signs, SECOND ARM NOT RUNNABLE; determinism —
  the frozen implementation run twice with seed
  44054, identical outputs, failure INVALID),
  then battery NB-1 exactly as the frozen
  amendment specifies in both arms (position
  classes initial/terminal/medial over sequences
  of length >= 2, length-1 sequences counted
  separately; classifiable iff N >= 20; STRONG
  >= 2/3, MODERATE >= 1/2), per-class
  reappearance at >= 1/2 through crosswalk v1
  under DD-054-5's denominator discipline, the
  pooled overlap against the 999-shuffle
  label-permutation null (seed 44054,
  nearest-rank 95th percentile), DD-054-2's
  precedence in the amendment section 5.5 order,
  and the amended verdict wordings (SUPPORTED /
  NOT SUPPORTED / INCONCLUSIVE — no RE-EARNED
  wording anywhere). No verdict moves the parent
  claim's recorded status.

The node serves the phase's committed results
JSON (reports/phase438_results.json),
recomputing via the phase script when that
script's pinned inputs are present locally.
Freeze: specs/054-yadav-opening-closing/
freeze.md (digest d85f6ace...); the frozen
spec's contract registration is OSF
https://osf.io/8spvf/.
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
    ("IndusPhase438YadavOpeningClosing",
     "phase438_yadav_opening_closing.py",
     "phase438_results.json",
     "Phase-438 Yadav opening/closing NB-1 (spec 054)",
     "Phase-438 (spec 054): execution of the frozen "
     "amended Spec 054 contract — step-0 gates in "
     "the amendment section 6 order (pin checks: the "
     "freeze section 2 pins incl. the claim store "
     "after the falsifier append at 938174b0..., the "
     "crosswalk v1 files at 4e7559df.../3d0b9ef1..., "
     "the anchors at df0cf620... — mismatch INVALID; "
     "strict corpus identification: the V3 / "
     "Mahadevan-lineage Firestore 'indusarrays' "
     "layer the Phase-43 battery ran on, identified "
     "mechanically against the Phase-43 record's "
     "census (3,916 records / 2,665 dockeys / 3,137 "
     "sequences / 12,494 sign instances) — failure "
     "STRICT CORPUS NOT PINNABLE; thinness: arm 1 "
     "under 30 sequences of length >= 3 or under 10 "
     "classifiable signs — TOO THIN; second arm: "
     "the Holdat layer (indus_corpus 2.csv, "
     "gitignored downloads area) pinned, arm 2 "
     "under 10 classifiable signs — SECOND ARM NOT "
     "RUNNABLE; determinism: identical second run, "
     "seed 44054 — failure INVALID), then battery "
     "NB-1 as frozen in both arms (classes "
     "initial/terminal/medial over sequences of "
     "length >= 2, length-1 sequences counted "
     "separately; classifiable iff N >= 20; STRONG "
     "at rate >= 2/3, MODERATE at >= 1/2), per-class "
     "reappearance at >= 1/2 through crosswalk v1 "
     "with DD-054-5's denominator discipline "
     "(TOO THIN / UNMAPPED / CONFLICT named; the "
     "sensitivity beside the primary), the pooled "
     "overlap against the 999-shuffle "
     "label-permutation null (seed 44054, "
     "nearest-rank 95th percentile), precedence "
     "per DD-054-2 in the amendment section 5.5 "
     "order, verdicts in the amended wordings "
     "(SUPPORTED / NOT SUPPORTED / INCONCLUSIVE; "
     "no RE-EARNED). The parent claim stands "
     "strongly supported as recorded; no verdict "
     "moves it. Outcome as recorded in "
     "reports/phase438_results.json. CPU."),
]


def _phase438_node_defs():
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
