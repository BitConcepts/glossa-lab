"""Experiment Graph Nodes: Phase 432 (Spec 069 —
the Asset A build: the depicted-kind classification
under Spec 045's frozen sections 2-3 contract).

  IndusPhase432AssetABuild    Phase-432: gates
  A1-A6 in order (source availability, the D-18
  input state, blind double entry with
  reconciliation, coverage, citation
  completeness, the blind-entry attestation, the
  asset freeze record) — the build itself, whose
  product is Asset A and its SHA-256 digest.

The node serves the phase's committed results JSON
(reports/phase432_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/069-hunt-asset-a/
freeze.md (digest 657b930c...); the frozen spec's
contract registration is OSF https://osf.io/r3xqb/.
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
    ("IndusPhase432AssetABuild",
     "phase432_asset_a_build.py",
     "phase432_results.json",
     "Phase-432 Asset A Build (spec 069)",
     "Phase-432 (spec 069): execution of the frozen Spec "
     "069 contract — the Asset A build under Spec 045's "
     "frozen sections 2-3. Gates in order: A1 source "
     "availability (the CISI volumes and Parpola's "
     "published identifications in hand, named by edition "
     "in the build record); A2 the D-18 input resolved "
     "(Spec 046's terminal empty feed, SHA-256 772db4df..., "
     "re-asserted); blind entry from the held published "
     "sources only, in two independent passes reconciled "
     "sign by sign, disputes coded by the quoted rule; A3 "
     "coverage over the full pinned-crosswalk universe "
     "(187 distinct sign keys); A4 citation completeness; "
     "A5 the blind-entry and order attestation; A6 the "
     "asset freeze record, its digest recomputed from the "
     "canonical CSV — all before any join (this spec "
     "performs no join and computes no corpus quantity). "
     "Outcome (2026-10-22): ASSET BUILT AND FROZEN — 187 "
     "rows (animal 20, sky_cycle 0, object_goods 14, "
     "human 25, other 127, contested 0, unidentified 1); "
     "the digest is recorded in specs/069-hunt-asset-a/"
     "asset-a/asset-a-freeze.json and is the asserted "
     "step-0 input of Specs 070 and 071. CPU."),
]


def _phase432_node_defs():
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
