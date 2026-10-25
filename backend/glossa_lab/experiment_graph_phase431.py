"""Experiment Graph Nodes: Phase 431 (Spec 072 —
Parpola's fish-sign family, sign by sign, in ICIT
numbering on the Shakti corpus; the Spec 048
question, re-designed).

  IndusPhase431FishFamilyProfiles    Phase-431:
  step 0 (intake assertion S1/S2, Asset F digest
  assertion, the freeze-pinned concordance
  exhibited, classes and census, verdict-line
  assertion) and the primary + sensitivity runs
  under the frozen majority partition.

The node serves the phase's committed results JSON
(reports/phase431_results.json), recomputing via
the phase script when that script's pinned inputs
are present locally. Freeze: specs/
072-fish-family-profiles-redesign/freeze.md
(digest 3925f365...); the frozen spec's contract
registration is filed on OSF at the freeze
(osf-spec-registration.md in the spec directory).
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
    ("IndusPhase431FishFamilyProfiles",
     "phase431_fish_family_profiles.py",
     "phase431_results.json",
     "Phase-431 Fish-Family Profiles (spec 072)",
     "Phase-431 (spec 072): execution of the frozen Spec "
     "072 contract — step 0 in order: gate 0.1 the Shakti "
     "intake assertion (P-F1 S1/S2 against the merged "
     "intake record; corpus sha256 345241b1..., row-grades "
     "sha256 02394241..., census 5,704 / 5,536 / 3,212 / "
     "2,087 / 405 / 4,904); gate 0.2 the Asset F digest "
     "assertion (ca5fb1b5..., Spec 044 section 4.2 "
     "exclusion rule); gate 0.3 the freeze-pinned "
     "concordance exhibited (M048=243, M050=220, M060=235, "
     "M145=032, M147=033 identified; M047 and M052 "
     "UNIDENTIFIED IN ICIT under the confirmed DD-072-5 "
     "disposition); gate 0.4 classes and census under the "
     "carried cascade; gate 0.5 the freeze-fixed verdict "
     "line L = 0.765 (95th percentile, nearest-rank, of "
     "the 86-sign non-fish reference distribution) "
     # Correction (2026-10-25, programme red team, RT-17/E-9): L = 0.765 is the MAXIMUM of the
     # 86-sign non-fish reference distribution, not its 95th percentile; the description string
     # above is the frozen record's wording and stands as executed.
     "asserted. Primary run on documented-lineage rows "
     "and the mandatory documented + corroborated "
     "sensitivity against the same line; the family word "
     "under the frozen majority partition; grade-flips "
     "are findings. Records internal under the Roif "
     "gate. CPU. "
     "Outcome (2026-10-22): executed — held under "
     "the Roif gate (spec 072 outcome.md; result "
     "content redacted 2026-10-25 under the owner's "
     "realignment decision — see docs/decisions/"
     "2026-10-25-realignment-decision.md)."),
]


def _phase431_node_defs():
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
