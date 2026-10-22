"""Experiment Graph Nodes: Phase 404 (Spec 044 —
fish-sign coastal residue, sign by sign; step 0:
the step-0 gates and the one-time build of Asset F,
the frozen fish-family list).

  IndusPhase404FishCoastalStep0    Phase-404: gate
  0.1 layer pin and population reproduction, gate
  0.2 Asset F build and freeze, gate 0.3 coastal
  list freeze, gate 0.4 census (margins only), and
  the execution's closure at gate 0.4

The node serves the phase's committed results JSON
(reports/phase404_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
044-fish-sign-coastal-residue/freeze.md (digest
6851f943...); the frozen spec's own contract
registration is OSF https://osf.io/6p9et/ (approved
and public, 2026-10-21). This spec is under the
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
    ("IndusPhase404FishCoastalStep0",
     "phase404_fish_coastal_step0.py",
     "phase404_results.json",
     "Phase-404 Fish-Sign Coastal Residue — Step 0 "
     "(spec 044)",
     "Phase-404 (spec 044): step 0 of the frozen "
     "Spec 044 contract, executed 2026-10-21 under "
     "the runnable-experiments campaign (Wave 3, "
     "Group 1; step 0 only). Gate 0.1 re-asserted "
     "the CISI-based layer of record (the Holdat "
     "corpus file, SHA-256 62d14d2b...) and "
     "reproduced the original family-level test's "
     "population exactly (7,002 tokens; 1,670 "
     "inscriptions over 9 sites; M047 at 13 tokens "
     "in 13 inscriptions; Phase-45 T6 table "
     "2 / 10 / 228 / 1,369, Fisher two-sided "
     "p = 0.685). Gate 0.2 built and froze Asset F, "
     "the fish-family list, solely from Parpola's "
     "published list as held in the programme's "
     "pinned Mahadevan–Parpola crosswalk: 7 members "
     "(M047, M048, M050, M052, M060, M145, M147), "
     "canonical file specs/044-fish-sign-coastal-"
     "residue/asset-f-fish-family.json, digest "
     "recorded in the step-0 record. Gate 0.3 froze "
     "the coastal list under the design's rule "
     "(coastal/maritime: Lothal, Dholavira, both "
     "members by name; Surkotada classed inland "
     "and listed as contested). Gate 0.4's census "
     "(margins only) found one member clearing the "
     "30-occurrence floor (M048, 157) and six TOO "
     "THIN (M047 13, M050 17, M052 22, M060 20, "
     "M145 3, M147 2), so the execution closed as "
     "TOO THIN at gate 0.4 with the census as its "
     "finding: no per-sign coastal test was "
     "computed, gate 0.5 was not reached, and the "
     "family-level verdict (partially falsified) "
     "stands exactly as recorded. Internal record "
     "under the campaign's Roif gate (R-7); not a "
     "publication. CPU."),
]


def _phase404_node_defs():
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
