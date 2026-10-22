"""Experiment Graph Nodes: Phase 400 (Spec 036 —
PRED-2026-011: scoring the screened clean-withholding
successor, exactly as registered).

  IndusPhase400Pred011Scoring    Phase-400: step 0
  (registration re-verification, input integrity,
  training-pool + classification + screen
  reproduction, crosswalk coverage — fail-closed, in
  the frozen order), then — only behind a full step-0
  pass — the registered scoring

The node serves the phase's committed results JSON
(reports/phase400_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
036-pred-2026-011-scoring/freeze.md (digest
bbd5c4fd...); the prediction's preregistration is
OSF https://osf.io/t6whq/ (DOI 10.17605/OSF.IO/T6WHQ);
the frozen spec's own contract registration is OSF
https://osf.io/gjen4/.
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
    ("IndusPhase400Pred011Scoring",
     "phase400_pred011_scoring.py",
     "phase400_results.json",
     "Phase-400 PRED-2026-011 Scoring (spec 036)",
     "Phase-400 (spec 036): execution of the frozen Spec 036 "
     "contract — PRED-2026-011 scored exactly as registered "
     "(at least 70% of the trained INITIAL signs {P217, P324}, "
     "derived at registration from the CISI Mohenjo-daro-only "
     "pool under the disclosed mappability screen, at Harappa "
     "start rate at least 0.40 on the withheld Yajnadevam "
     "Harappa sequences; with 2 signs, only 2 of 2 passes). "
     "Step 0 ran first, fail-closed, in the frozen order: "
     "0.1 the prediction's OSF preregistration (t6whq) "
     "re-verified accepted and public; 0.2 the four "
     "registered input pins verified bytewise (the withheld "
     "file hashed only, never opened); 0.3 the training "
     "pool re-derived (179 CISI Mohenjo-daro inscriptions, "
     "manifest hash), the recorded classification "
     "reproduced exactly (28 classifiable signs; unscreened "
     "INITIAL set {P000, P217, P324}), and the registered "
     "screen re-applied, returning {P217, P324} with P000's "
     "exclusion reproduced as a screen outcome; 0.4 "
     "crosswalk coverage of the trained signs under the "
     "frozen best-match reading (P217 -> Y0520, confidence "
     "1.0, confirmed; P324 -> Y0740, confidence 0.9867, "
     "confirmed, conflict-flagged) — no unmappable trained "
     "sign. Step 0 passed in full, the withheld file was "
     "opened, and the registered computation ran: P217 — "
     "119 Harappa occurrences, 104 initial, start rate "
     "0.8739; P324 — 774 Harappa occurrences, 473 initial, "
     "start rate 0.6111. Both signs meet the bar: share 1.0, "
     "verdict CONFIRMED on the exact two-sign criterion. "
     "The verdict concerns only P217 and P324 in this pinned "
     "dataset; it does not validate the INITIAL class as a "
     "whole and says nothing about P000. CPU."),
]


def _phase400_node_defs():
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
