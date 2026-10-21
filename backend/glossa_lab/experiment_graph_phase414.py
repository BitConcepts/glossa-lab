"""Experiment Graph Nodes: Phase 414 (Spec 055 —
"sign 900 means six": identify the sign, then test it
as a numeral).

  IndusPhase414Sign900Numeral    Phase-414: step-0
  gates (input pins, source producible, recovery
  before verdict), step-1 identification (list named
  from the document; drawn sign matched by form only)
  with the preserved recovery record, gate 0.4 (strict
  corpus exported and pinned; occurrence floor 5), and
  step 2 (the three frozen measures and the section
  5.3 mapping), with the dry-run of DD-055-16 in the
  pre-counting record.

The node serves the phase's committed results JSON
(reports/phase414_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
055-sign900-numeral/freeze.md (digest 42ef8282...);
the frozen spec's own contract registration is OSF
https://osf.io/tbyqg/ (approved and public before the
run).
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
    ("IndusPhase414Sign900Numeral",
     "phase414_sign900_numeral.py",
     "phase414_results.json",
     "Phase-414 Sign 900 Numeral Test (spec 055)",
     "Phase-414 (spec 055): execution of the frozen Spec "
     "055 contract — the fragment 'Sign value: 900 / "
     "number six' (Fuls, Ancient Writing and Modern "
     "Technologies; stopped at Phase-104 under RULE-NUM) "
     "is carried through step 0 (input pins verified; "
     "source produced from the held copy with the "
     "sign-900 material located verbatim; recovery "
     "before verdict), step 1 (the source's sign list "
     "named from the document's own text as the extended "
     "Wells (2011, 2015) list of 702 distinct signs; the "
     "drawn sign matched BY DRAWN FORM ONLY — the named "
     "list's sign 900 is the single-arc grapheme per the "
     "verified Phase-123 Wells witness, and exactly one "
     "registry row is a plain right parenthesis with no "
     "added element: P154, Mahadevan 287; the registry's "
     "W900 cell on that row is the frozen trap, recorded "
     "and not used as the identification), gate 0.4 (the "
     "strict corpus — the Mahadevan-lineage layer as "
     "held, per the Spec 033 precedent — exported in "
     "full and pinned by SHA-256; the identified sign's "
     "census taken against the frozen floor of 5), and "
     "step 2 (both reference sets fixed in a "
     "pre-counting record — the known-numeral set from "
     "the source's own stroke-sign identification, the "
     "target excluded, hedged members excluded and "
     "listed separately; the control set by the frozen "
     "nearest-10 rule; a dry-run on a non-target sign "
     "first — then the three frozen measures and the "
     "section 5.3 mapping). The terminal outcome is "
     "recorded in reports/phase414_results.json and in "
     "the spec's outcome record. No outcome of this "
     "spec establishes the value six. Design D-16 does "
     "not join this campaign even though this recovery "
     "is the act that would unblock it (campaign "
     "decision E-7). CPU."),
]


def _phase414_node_defs():
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
