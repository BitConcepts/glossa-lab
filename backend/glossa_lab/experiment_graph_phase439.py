"""Experiment Graph Nodes: Phase 439 (Spec 040 —
D-25: G1 with time held fixed, the
chronology-controlled rerun of the Spec 025 /
Phase-140 site-repertoire test).

  IndusPhase439G1ChronologyControlled
  Phase-439: execution of the frozen Spec 040
  contract in the spec section 13 order,
  fail-closed — step 0 (dependency
  re-verification: every freeze section 3 pin
  recomputes, including the accepted Spec 041
  artifact at 1e5b54c9... consumed by
  successor-artifact substitution, Spec 039's
  artifact at 64f288d3... named as not
  satisfying section 1, the Phase-139
  covariates at a0f0d05a..., the spine at
  9dc2fba5..., the anchors at df0cf620...; the
  freeze record replays; the ICIT-lineage layer
  (horus84 inscriptions.csv) asserted at its
  pin c368f290... before any use; then the
  section 4.1 join under derivation A1, which
  must reproduce the freeze section 3 counts
  exactly — 1,457 placed (EARLY 32, MATURE
  1,386, LATE 39), 3,953 unplaced — any failure
  INVALID), determinism (the step-0 + margins
  record computed twice, identical), then the
  section 5 margins gate with all three arms
  retained (DD-040-6): each coarse period
  retains assigned inscriptions from at least
  5 distinct sites; the unassigned share is at
  most 40%; permutable inscriptions under the
  primary strata number at least 1,000. Any
  arm failing closes the execution
  NOT-YET-TESTABLE (DD-040-5) before any
  outcome quantity exists; the section 7
  regression and the section 6 primary are
  reached only past a passing gate. No outcome
  moves any anchor or touches PRED-2026.

The node serves the phase's committed results
JSON (reports/phase439_results.json),
recomputing via the phase script when that
script's pinned inputs are present locally.
Freeze: specs/040-d25-g1-chronology-controlled/
freeze.md (digest 16aeeb70...); the frozen
spec's contract registration is OSF
https://osf.io/2rgtb/.
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
                [sys.executable, str(script), "run"],
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
    ("IndusPhase439G1ChronologyControlled",
     "phase439_g1_chronology_controlled.py",
     "phase439_results.json",
     "Phase-439 G1 chronology-controlled (spec 040)",
     "Phase-439 (spec 040): execution of the frozen "
     "Spec 040 contract — step 0 in order (pin "
     "verification: the freeze section 3 pins incl. "
     "the accepted Spec 041 artifact at 1e5b54c9... "
     "consumed by successor-artifact substitution, "
     "the Phase-139 covariates at a0f0d05a..., the "
     "spine at 9dc2fba5..., the anchors at "
     "df0cf620... — mismatch INVALID; the layer "
     "(horus84 inscriptions.csv) asserted at "
     "c368f290...; population reproduction and the "
     "section 4.1 join under derivation A1 "
     "reproducing the freeze counts exactly — "
     "1,457 placed (EARLY 32 / MATURE 1,386 / LATE "
     "39), 3,953 unplaced (2,294 no informative "
     "label; 1,658 all labels UNASSIGNED; 1 "
     "disagreement) — coverage failure INVALID; "
     "determinism: identical second computation), "
     "then the section 5 margins gate, all three "
     "arms retained per DD-040-6 (at least 5 "
     "distinct sites in each of EARLY, MATURE, "
     "LATE; unassigned share at most 40%; "
     "permutable inscriptions under the primary "
     "strata at least 1,000) — any arm failing "
     "closes NOT-YET-TESTABLE (DD-040-5) with no "
     "outcome quantity computed, and the section "
     "7 regression and section 6 primary not "
     "reached. G1 stands unchanged with its rider "
     "under this closure. Outcome as recorded in "
     "reports/phase439_results.json. CPU."),
]


def _phase439_node_defs():
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
