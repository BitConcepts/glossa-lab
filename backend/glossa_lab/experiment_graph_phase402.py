"""Experiment Graph Nodes: Phase 402 (Spec 037 —
CISI 3.1 concordance spine: verifying the string
matches before anything is joined, exactly as
frozen).

  IndusPhase402Concordance    Phase-402: step 0
  (gate and integrity, fail-closed, in the frozen
  order), then — only behind a full step-0 pass —
  the pilot census under the fixed ladder, the
  halt rule, the spine build behind the halt rule,
  and the HARP provenance annex

The node serves the phase's committed results JSON
(reports/phase402_results.json), recomputing via
the phase script when that script's pinned inputs
are present locally. The script's row-level inputs
and products live only in the restricted local
store (the Phase-130 gate); the committed results
carry aggregate statistics only. Freeze: specs/
037-cisi31-concordance-spine/freeze.md (digest
122c2ea4...); the frozen spec's own contract
registration is OSF https://osf.io/j6t9k/.
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
    ("IndusPhase402Concordance",
     "phase402_concordance.py",
     "phase402_results.json",
     "Phase-402 CISI 3.1 Concordance Census (spec 037)",
     "Phase-402 (spec 037): execution of the frozen Spec 037 "
     "contract — the CISI 3.1 intake's 693 exact-string matches "
     "between the portion's catalogue numbers and corpus_master "
     "object ids graded as same-object joins under the fixed "
     "ladder (site mandatory; object type mandatory where "
     "graded, seal distinct from seal impression; corroborating "
     "keys graded only where both sides carry a value; "
     "number-level ambiguity barring VERIFIED), the halt rule "
     "(a CONFLICT share above 20 percent of all candidates "
     "halts the spine build), and the descriptive HARP "
     "provenance annex. Step 0 ran first, fail-closed, in the "
     "frozen order (gate record; portion PDF hash and local "
     "table parse and census; corpus_master pin; repo "
     "cleanliness). Row-level products live only in the "
     "restricted local store; this node serves the committed "
     "aggregate record. The concordance is a finding aid, not "
     "evidence about readings; no PRED-2026 entry is scored by "
     "this phase. Outcome (2026-10-20): step 0 passed in "
     "full; of 693 candidates, VERIFIED 269, CONFLICT 341, "
     "UNRESOLVED 83; the conflict share of 49.21 percent "
     "exceeded the frozen 20 percent cap, so no spine was "
     "written: PILOT COMPLETE - SPINE HALTED. CPU."),
]


def _phase402_node_defs():
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
