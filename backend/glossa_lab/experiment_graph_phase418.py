"""Experiment Graph Nodes: Phase 418 (Spec 056 —
sign-821 recovery: re-extract the pinned passage, or
retire the fragment).

  IndusPhase418Sign821Recovery    Phase-418: step-0
  gates (input pins, passage producible, passage
  pinnable), the DD-056-16 dry-run, two independent
  extraction passes with reconciliation by
  quotation, and the conjunctive R-1..R-5 recovery
  test of spec section 5

The node serves the phase's committed results JSON
(reports/phase418_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
056-sign821-recovery/freeze.md (freeze digest
64c28ce1... in freeze.json as merged); the frozen
spec's own contract registration is OSF
https://osf.io/3eygs/ (approved and public before
the run, DOI 10.17605/OSF.IO/3EYGS).
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
    ("IndusPhase418Sign821Recovery",
     "phase418_sign821_recovery.py",
     "phase418_results.json",
     "Phase-418 Sign-821 Recovery (spec 056)",
     "Phase-418 (spec 056): execution of the frozen Spec 056 "
     "contract — the fragment 'Sign value: 821 / it is used in a "
     "variety of contexts (Figure 6' "
     "(the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001, "
     "stopped at Phase-104 under RULE-NUM) is carried through "
     "step 0 (input pins verified in the freeze's Spec 038 form; "
     "the passage of record — Wells 2015, 'The Dholavira "
     "signboard, revisited', held cleaned-text lines 2783-2871, "
     "5,354 bytes, digest 51d6fb3a... — produced from the held "
     "copy and recomputed to its freeze-pinned digest), a "
     "dry-run of the sheet and checklist machinery on a "
     "non-record passage (DD-056-16), and two independent "
     "extraction passes over the pinned passage only, reconciled "
     "by quotation with unsettled disagreement resolving "
     "against recovery (DD-056-14). The reconciled candidate — "
     "sign 821, in the Dholavira signboard contexts, has a "
     "meaning of 'city', either as a determinative or as a word "
     "(printed p. 92) — passes the argument conditions R-1, "
     "R-2, R-4 and R-5, and the sign list is named from the "
     "document itself (Wells's own list, Wells 2011, in Wells "
     "2015 Chapter 2 / Figure 2.6); but the drawn sign cannot "
     "be identified by either route R-3 allows: the pinned "
     "crosswalk registry carries no W821 value in any row (its "
     "Yunmapped_0821 row is a Yajnadevam glyph identifier, the "
     "frozen number-collision trap, and was not used), the "
     "Phase-123 Wells witness carries no grapheme 821, and the "
     "source list's own entry stands in Figure 2.6, whose drawn "
     "forms did not survive the held copy's text extraction "
     "(captions only). Outcome (2026-10-21): IDENTIFICATION "
     "FAILED — the fragment is neither recovered nor retired; "
     "it stays a stated gap, and this act establishes, at "
     "most, what the source passage argues — never whether "
     "the argument is right, and nothing about sign 821 "
     "itself. CPU."),
]


def _phase418_node_defs():
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
