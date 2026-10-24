"""Experiment Graph Nodes: Phase 405 (Spec 046 —
identification concordance for the horned-tiger fragment:
identification before scoring, exactly as frozen).

  IndusPhase405HornedTigerConcordance    Phase-405: step-0
  gates (input pins, source producible, four lists
  accounted for), step-1 identification (list named from
  the document; drawn sign matched by form only), and the
  section 6 delivery on every terminal outcome

The node serves the phase's committed results JSON
(reports/phase405_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
046-horned-tiger-concordance/freeze.md (freeze-act
digest 80c3be31...; successor digest e0d7add8... in
freeze.json as merged); the frozen spec's own contract
registration is OSF https://osf.io/dnts8/ (approved and
public before the run).
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
    ("IndusPhase405HornedTigerConcordance",
     "phase405_concordance.py",
     "phase405_results.json",
     "Phase-405 Horned-Tiger Identification Concordance (spec 046)",
     "Phase-405 (spec 046): execution of the frozen Spec 046 "
     "contract — the fragment 'Sign value: 297 / the horned "
     "tiger, or perhaps just tiger generically' (Wells 2015, "
     "printed p. 97; stopped at Phase-104 under RULE-NUM) is "
     "carried through step 0 (input pins verified; source "
     "produced from the held copy with the passage located "
     "verbatim; the four lists of record — Wells as SOURCE, "
     "CISI, Parpola, and Mahadevan as INDEPENDENT — accounted "
     "for as held or citable) and step 1 (the source's sign "
     "list named from the book's own apparatus as Wells's own "
     "list, Wells 2011, in Wells 2015 Chapter 2 / Figure 2.6; "
     "the drawn sign then matched by drawn form only, numbers "
     "never used as identities). Outcome (2026-10-21): "
     "IDENTIFICATION FAILED (sign unmatched) — the pinned "
     "crosswalk registry carries no entry for the drawn sign "
     "(its only W297 value sits inside the multi-value cell on "
     "the P205 'Prismed light rays' row, a trap the frozen "
     "spec names in advance), the Phase-123 Wells witness "
     "carries no Wells grapheme 297, and the drawn forms of "
     "Wells's Figure 2.6 did not survive the held copy's text "
     "extraction, so no inspectable drawn-sign reference "
     "exists in the held record. No list was scored, no "
     "statement about the sign is made, and nothing is fed "
     "to Asset A: the delivery concordance-297.json carries "
     "an empty signs array and the closure block. This "
     "result settles what the published lists say the drawn "
     "sign depicts. It is not evidence of what the sign meant "
     "in use. CPU."),
]


def _phase405_node_defs():
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
