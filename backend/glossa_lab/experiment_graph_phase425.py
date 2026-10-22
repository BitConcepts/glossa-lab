"""Experiment Graph Nodes: Phase 425 (Spec 063 —
sign-821 identification successor: identify the drawn
sign on the preserved reference, or close again on
the new record).

  IndusPhase425Sign821Identification    Phase-425:
  step-0 gates (input pins; the thesis file asserted
  on the local file before any plate is read; the
  reference producible with the plate page produced
  from the pinned file), step D (two independent
  descriptor derivations, reconciliation, comparison
  with the preserved descriptor), step C (continuity
  on the anchors' agreement), and step M (the match
  by exactly one frozen route, traps asserted)

The node serves the phase's committed results JSON
(reports/phase425_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally (the thesis file is held outside
the repository; where it cannot be located the
script exits non-zero without writing, and the
committed results are served). Freeze: specs/
063-sign821-identification-successor/freeze.md
(freeze digest dc24a10e... in freeze.json as
merged); the frozen spec's own contract
registration is OSF https://osf.io/kfet5/
(approved and public before the run).
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
    ("IndusPhase425Sign821Identification",
     "phase425_sign821_identification.py",
     "phase425_results.json",
     "Phase-425 Sign-821 Identification (spec 063)",
     "Phase-425 (spec 063): execution of the frozen Spec 063 "
     "contract — the identification successor to Spec 056 "
     "(Phase-418, IDENTIFICATION FAILED at R-3). Step 0 "
     "passed in full: every spec section 2 pin recomputed "
     "(held text 62acf855..., registry 8a0b2a82..., witness "
     "ecbc37a4..., Spec 056's freeze / outcome / extraction "
     "records, Phase-104 evaluation, lane-2 drafts, anchors "
     "df0cf620...), the claim record asserted in the Spec 038 "
     "form (constant bd0f7abd... plus the fragment's facts on "
     "the live file, its spec056_closure append present), "
     "the local Wells 2006 thesis PDF asserted to its frozen "
     "digest (4b39330c..., 19,313,853 bytes) BEFORE any plate "
     "was read, and the preserved reference "
     "(drawn-form-reference-821.json, SHA-256 695dd35d...) "
     "produced at its pinned digest with the plate page "
     "(thesis p. 92 / PDF p. 104, Figure 3.2) produced from "
     "the pinned file. Step D: two independent derivations "
     "from the plate agree feature by feature — two "
     "identical vertical ovals side by side, touching at the "
     "midline, each divided by three diameters (one "
     "vertical, two diagonal) into six sectors — and the "
     "reconciled descriptor agrees with the preserved "
     "record's descriptor, which is thereby sustained, not "
     "inherited. Step C: continuity passes on the anchors' "
     "agreement (the Appendix II formation passage: sign "
     "820 doubles to form sign 821; the P378 registry "
     "anchor, W820, 'Wheel with 6 spokes with even "
     "angles'; the plate agreement at 820/821). Step M: "
     "route 1 (registry, by drawn form) fails — no registry "
     "row carries the doubled form, and there is no "
     "fallback to P378, the base sign; route 2 (the list's "
     "own entry, through the preserved reference) "
     "satisfies the match; route 3 was not used. The traps "
     "are asserted: Yunmapped_0821 (a Yajnadevam glyph "
     "identifier, not Wells's 821), sign 861, P378 as the "
     "target, and number-only matching. Outcome "
     "(2026-10-22): RECOVERED — candidate K-1 (sign 821, "
     "in the Dholavira signboard contexts, has a meaning "
     "of 'city', either as a determinative or as a word; "
     "Wells 2015, printed p. 92) passes R-1 through R-5, "
     "the argument conditions standing as adjudicated in "
     "Spec 056's executed record, and enters the lifecycle "
     "at the created stage, untested, as an appended "
     "restatement on the fragment's own record, with a "
     "test design recorded and no test run. This act "
     "establishes, at most, whether the drawn sign K-1 "
     "names is identified in the program's claim form — "
     "never whether K-1's suggested meaning is right, and "
     "nothing about sign 821 itself beyond the "
     "identification. CPU."),
]


def _phase425_node_defs():
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
