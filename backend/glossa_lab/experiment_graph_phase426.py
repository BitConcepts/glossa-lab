"""Experiment Graph Nodes: Phase 426 (Spec 064 —
identification concordance for the horned-tiger fragment,
successor to Spec 046: the preserved drawn-form reference
checked by step D, its mandatory step C discrimination
test, and the section 6 delivery on every terminal
outcome; the reference's continuity status is QUALIFIED).

  IndusPhase426Sign297ConcordanceSuccessor    Phase-426:
  step-0 gates (input pins including the preserved
  reference at its pinned digest, source producible,
  four lists accounted for, reference producible with
  the thesis digest asserted), step 1.1 (list named
  from the document), step D (descriptor derived twice
  and checked against the preserved record), step C
  (continuity / discrimination, mandatory)

The node serves the phase's committed results JSON
(reports/phase426_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally (the thesis gate needs the program's
local store; in an environment without it the script
aborts without writing and the committed record is
served). Freeze: specs/
064-sign297-concordance-successor/freeze.md (freeze
digest cfeb7baf... in freeze.json); the frozen spec's
own contract registration is OSF https://osf.io/s6hr9/
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
    ("IndusPhase426Sign297ConcordanceSuccessor",
     "phase426_concordance.py",
     "phase426_results.json",
     "Phase-426 Sign-297 Identification Concordance, Successor (spec 064)",
     "Phase-426 (spec 064): execution of the frozen Spec 064 "
     "contract, successor to Spec 046 / Phase-405 — the "
     "fragment 'Sign value: 297 / the horned tiger, or "
     "perhaps just tiger generically' (Wells 2015, printed "
     "p. 97) is carried through step 0 (input pins verified, "
     "including the preserved drawn-form reference at its "
     "pinned digest and Spec 046's closure delivery "
     "unedited; the source produced from the held copy with "
     "the passage located verbatim; the four lists of "
     "record — Wells as SOURCE, CISI, Parpola, and "
     "Mahadevan as INDEPENDENT — accounted for as held or "
     "citable; the thesis plate page produced from the "
     "local thesis file after its digest was asserted) "
     "and step 1 (the source's sign list named from the "
     "book's own apparatus as Wells's own list, Wells 2011, "
     "in Wells 2015 Chapter 2 / Figure 2.6; step D derived "
     "the drawn-form descriptor twice from the thesis "
     "plate and sustained the preserved reference; step C, "
     "mandatory in this successor, then tested whether the "
     "descriptor picks out plate 297 and no neighbour in "
     "the 289-308 run). Outcome (2026-10-22): "
     "IDENTIFICATION FAILED (continuity/discrimination not "
     "sustained) — neither independent derivation affirms "
     "the discrimination (signs 299, 302 and 303 satisfy "
     "every stated feature of the descriptor), so the run "
     "closed before step M and before any scoring, under "
     "the pre-registered closure. The preserved reference's "
     "continuity status is QUALIFIED — anchored at family "
     "level only — and is carried on every product of the "
     "run. No statement about the sign is made, and nothing "
     "is fed to Asset A: the delivery concordance-297.json "
     "in the Spec 064 directory carries an empty signs "
     "array and the closure block. This result settles what "
     "the published lists say the drawn sign depicts. It is "
     "not evidence of what the sign meant in use. CPU."),
]


def _phase426_node_defs():
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
