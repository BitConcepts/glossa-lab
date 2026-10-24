"""Experiment Graph Nodes: Phase 408 (Spec 048 —
Parpola's fish-sign family, sign by sign; design
D-04; consumes Asset F).

  IndusPhase408FishFamilyStep0    Phase-408:
  step 0 only (Asset F digest assertion;
  membership join and cross-check; strict corpus
  identification), closing as STRICT CORPUS
  NOT PINNABLE at gate 0.3.

The node serves the phase's committed results JSON
(reports/phase408_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
048-parpola-fish-family-profiles/freeze.md (digest
56beec70...); the frozen spec's contract
registration is OSF https://osf.io/eqpab/
(approved and public). This spec is under the
campaign's Roif gate: its records are internal and
its results are not published or surfaced under
the campaign.
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
    ("IndusPhase408FishFamilyStep0",
     "phase408_fish_family_step0.py",
     "phase408_results.json",
     "Phase-408 Parpola Fish-Family Profiles Step 0 (spec 048)",
     "Phase-408 (spec 048): execution of the frozen "
     "Spec 048 contract at step 0 — gate 0.1 the "
     "Asset F digest assertion against Spec 044's "
     "step-0 outcome record (the pin source fixed "
     "at the freeze, DD-048-9; digest recomputed "
     "under Spec 044 section 4.2's exclusion rule "
     "and matching), gate 0.2 the membership join "
     "via each member's mahadevan_number locator "
     "through the pinned Mahadevan-Parpola "
     "crosswalk (all 7 members MAPPED, none "
     "UNMAPPED; the cross-check against the claim "
     "record's trio (72, 64, 70) and the Phase-43 "
     "six (267, 72, 65, 59, 60, 70) reported with "
     "every divergence named), then gate 0.3 "
     "strict corpus identification. Outcome "
     "(2026-10-21): gate 0.1 PASS; gate 0.2 PASS; "
     "gate 0.3 FAIL — the V3 / Mahadevan-lineage "
     "layer's data file (the Firestore "
     "'indusarrays' dump the V3 loader reads) is "
     "absent from the tree, the loader loads zero "
     "sequences, no database copy exists in the "
     "execution tree, and no other layer in the "
     "tree is the corpus the Phase-43 record "
     "names, so the execution closed STRICT "
     "CORPUS NOT PINNABLE in the frozen wording. "
     "Gates 0.4-0.6 were not reached, no "
     "ending-follower rate was computed for any "
     "sign, and no census or control figure "
     "exists. The claim "
     "parpola_2010_dravidian_solution_manual_002 "
     "stands exactly as recorded. Internal record "
     "under the campaign's Roif gate (R-7); not a "
     "publication. CPU."),
]


def _phase408_node_defs():
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
