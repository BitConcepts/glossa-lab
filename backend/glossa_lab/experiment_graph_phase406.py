"""Experiment Graph Nodes: Phase 406 (Spec 047 —
Roif's ledger thesis, distribution test: step 0 gates
and the step-1 Asset B build and freeze; step 2, the
distribution test).

  IndusPhase406RoifLedgerStep1    Phase-406: step 0
  (input integrity, spine reproduction, join census),
  the Asset B site-function classification built and
  frozen at step 1 under the two-source agreement rule,
  and the ledger-sign list frozen in the same act.
  Step 2 (the distribution test) is not run by this
  phase's step-1 act.

  IndusPhase406RoifLedgerStep2    Phase-406 step 2:
  step 0 re-run, Asset B pin re-assertion against the
  step-1 outcome record, and the section 6.3
  classification gate (E5), with the section 6.2
  primaries and section 6.4 sensitivities (E6) behind
  the gate in the step-2 script.

The nodes serve the phase's committed results JSONs
(reports/phase406_results.json;
reports/phase406_step2_results.json), recomputing via
the phase scripts when those scripts' pinned inputs
are present locally. Freeze: specs/
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
    ("IndusPhase406RoifLedgerStep2",
     "phase406_roif_ledger_step2.py",
     "phase406_step2_results.json",
     "Phase-406 Roif Ledger Step 2 (spec 047)",
     "Phase-406 step 2 (spec 047): the distribution "
     "test act — step 0 re-run in the frozen order "
     "(input integrity against the freeze pins; spine "
     "reproduction; the join census), Asset B pin "
     "re-assertion against the step-1 outcome record "
     "(digest a1a9e484...; the ledger-sign list digest "
     "dfa48f50...), then the section 6.3 classification "
     "gate (E5): fewer than 12 testable sites, or an "
     "empty pooled/contrast side in the test "
     "population, ends the execution as INCONCLUSIVE "
     "with the classification as the finding and no "
     "distribution quantity computed; the section 6.2 "
     "primaries and section 6.4 sensitivities (E6) run "
     "only behind the gate. Outcome (2026-10-21): "
     "step 0 PASS; Asset B pin MATCH (30 rows, "
     "testable 2 — harappa administrative, lothal "
     "port/trade, both pooled; contrast side empty); "
     "the gate fired on both clauses — INCONCLUSIVE "
     "(classification); the claim stands UNTESTED for "
     "its distribution component. All products held "
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
