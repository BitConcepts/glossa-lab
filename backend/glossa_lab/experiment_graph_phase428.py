"""Experiment Graph Nodes: Phase 428 (Spec 066 —
Phase-130 catalogue extension; CISI Vol. 3.1
portion objects into the pinned catalogue layer).

  IndusPhase428CatalogueExtension    Phase-428:
  step 0 (gate, pins, candidate-set re-derivation,
  repo cleanliness), the frozen ladder grading of
  all 2,101 candidates, the seeded hand-check
  stratum, the halt rule, and - on pass only - the
  locally built merged catalogue layer v2, the
  Phase-130 validator run, and the pinned
  section 4 products.

The node serves the phase's committed results JSON
(reports/phase428_results.json), recomputing via
the phase script when that script's pinned local
inputs are present. Freeze:
specs/066-phase130-catalogue-extension/freeze.md
(digest 0b81d842...). No OSF registration attaches
to this intake act (DD-066-8).
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
    ("IndusPhase428CatalogueExtension",
     "phase428_catalogue_extension.py",
     "phase428_results.json",
     "Phase-428 Catalogue Extension (spec 066)",
     "Phase-428 (spec 066): execution of the frozen Spec "
     "066 contract - step 0 in order: the Phase-130 gate "
     "re-verified on the record (PROVENANCE entry 22) and "
     "quoted; every pin recomputed (portion PDF, extraction "
     "table, vols. 1-2 catalogue layer, horus84 layer, "
     "Phase-421 census and results, intake schema and "
     "validator); the candidate sets re-derived (2,101 "
     "well-formed numbers: 1,341 referenced = 1,293 "
     "zero-resolution + 48 already-joined, 760 "
     "unreferenced); repo cleanliness. Then the frozen "
     "ladder of spec section 5.3 grades the full census "
     "(site, confidence gate, ambiguity bar, type "
     "carriage, corroboration) into VERIFIED / CONFLICT / "
     "UNRESOLVED; the seeded stratum (60, seed 20261021) "
     "attributes sampled conflicts by cause; the halt rule "
     "(conflict share above 20 percent of all graded "
     "candidates, or any sampled true non-identity) "
     "withholds the index and the pin on halt. On pass the "
     "merged catalogue layer v2 is built locally "
     "(restricted store, hash-pinned only), the pinned "
     "Phase-130 validator runs over the extension dataset "
     "form under the quoted entry-22 license basis, and "
     "the extension index (number + site section + type "
     "class + grade class) is committed. No join is run "
     "and no F1 quantity is computed; a VERIFIED "
     "catalogue object is not a verified join. CPU."),
]


def _phase428_node_defs():
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
