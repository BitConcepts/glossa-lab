"""Experiment Graph Nodes: Phase 406 (Spec 047 —
Roif's ledger thesis, distribution test: step 0 gates
and the step-1 Asset B build and freeze).

  IndusPhase406RoifLedgerStep1    Phase-406: step 0
  (input integrity, spine reproduction, join census),
  the Asset B site-function classification built and
  frozen at step 1 under the two-source agreement rule,
  and the ledger-sign list frozen in the same act.
  Step 2 (the distribution test) is not run by this
  phase's step-1 act.

The node serves the phase's committed results JSON
(reports/phase406_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
047-roif-ledger-distribution/freeze.md (digest
8501feab...); the frozen spec's contract registration
is OSF https://osf.io/b2a8w/. All products are held
under the Roif gate (spec section 10).
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
    ("IndusPhase406RoifLedgerStep1",
     "phase406_roif_ledger_step1.py",
     "phase406_results.json",
     "Phase-406 Roif Ledger Step 1 (spec 047)",
     "Phase-406 (spec 047): execution of the frozen Spec "
     "047 contract through step 1 — step 0 gates (input "
     "integrity against the freeze pins; spine "
     "reproduction, 36 rows / 30 clusters; the corpus "
     "join census accounting for every primary-layer "
     "record exactly once), then Asset B: the "
     "site-function classification of the 30 gazetteer "
     "clusters from excavation literature only, under "
     "the two-source agreement rule with its recorded "
     "dispute statuses, frozen by SHA-256 digest; and "
     "the ledger-sign list extracted from Roif's two "
     "Academia.edu postings of record, frozen in the "
     "same act under its own digest. Step 2 (the "
     "distribution test) is not run here. Outcome "
     "(2026-10-21): step 0 gates PASS; Asset B frozen "
     "with 3 AGREED rows (2 testable), 1 DISAGREED, 10 "
     "SINGLE-SOURCE, 16 NO-SOURCE; ledger list 8 "
     "entries, 3 mapped, 5 UNMAPPED. All products held "
     "under the Roif gate. CPU."),
]


def _phase406_node_defs():
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
