"""Experiment Graph Nodes: Phase 420 (Spec 058 —
what drove the Spec 023 transcription disagreement;
design D-21, arm A only).

  IndusPhase420TranscriptionDisagreement    Phase-420:
  step 0 (committed-record integrity; pilot-pass
  record production, inventory, and manifest; frame
  identity; exact reproduction of the committed
  Phase-132 metrics; adjudication-taxonomy
  cross-check; mismatched-population census), then
  the section 4 localisation tabulations (T1 by sign,
  T2 by recorded object type, T3 by divergence type;
  first divergence; the UNK-excluded descriptive
  secondary; the M-space sensitivity) and the
  section 5 headline, under the frozen Spec 058
  contract. Arm B is blocked and out of scope; no AI
  substitution for human coders is designed or run.

The node serves the phase's committed results JSON
(reports/phase420_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
058-transcription-disagreement-mechanism/freeze.md
(digest 8bdd4764...); the frozen spec's contract
registration is OSF https://osf.io/86dgh/.
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
    ("IndusPhase420TranscriptionDisagreement",
     "phase420_transcription_disagreement.py",
     "phase420_results.json",
     "Phase-420 Transcription Disagreement Mechanism (spec 058)",
     "Phase-420 (spec 058): execution of the frozen Spec "
     "058 contract (design D-21, arm A only) — step 0 "
     "gates in frozen order (0.1 committed-record "
     "integrity against the section 2.1 freeze pins; "
     "0.2 production, inventory, and per-file SHA-256 "
     "manifest of the Phase-132 pilot-pass record set; "
     "0.3 frame identity; 0.4 exact reproduction of the "
     "committed Phase-132 metrics by the pinned metrics "
     "module imported unchanged; 0.5 adjudication-"
     "taxonomy cross-check, 93/45/11/10/2/1 of 162; 0.6 "
     "the mismatched-population census), then the "
     "section 4 tabulations over the frozen alignment: "
     "mismatch events typed SUBSTITUTION / INDEL, T1 by "
     "sign (involvement; top-10 share over summed "
     "involvement; frequency shares over 381 tokens), "
     "T2 by recorded object type, T3 by divergence type "
     "(the INDEL share is the registered segmentation "
     "proxy), the first-divergence table, the "
     "UNK-excluded descriptive secondary, and the "
     "M-space sensitivity; the headline is the "
     "mechanical section 5.2 function of the loci that "
     "fire. Outcome (2026-10-21): all step-0 gates "
     "PASS (162-file manifest; metrics reproduced in "
     "full; taxonomy exact; census 40); LOCALISED TO "
     "SIGNS — E = 103 events, the 10 most-involved "
     "signs account for 54.5% of summed involvement, "
     "with UNK itself among them (27.7% of "
     "involvement: in part a localisation to "
     "illegibility); the object-type locus does not "
     "fire (Seals carry 77.7% of events but only a "
     "9.7-point enrichment over their 68.0% frame "
     "share, below the frozen 10-point margin) and "
     "the segmentation locus does not fire (INDEL "
     "share 14.6%). The Spec 023 pilot's CONTRADICTED "
     "verdict stands exactly as recorded. CPU."),
]


def _phase420_node_defs():
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
