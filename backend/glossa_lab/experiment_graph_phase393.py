"""Experiment Graph Node: Phase 393 (Spec 028 — Harappa
robustness of the M77 site effect).

  IndusPhase393HarappaRobustness  Phase-393: Spec 027
  Stage 1 follow-up under specs/028-harappa-robustness/
  freeze.md (including Amendment 1).

The node serves the phase's committed results JSON
(reports/phase393_results.json), recomputing via the phase
script when that script's pinned inputs are present locally
(the inputs live in the gitignored local store
corpora/downloads/spec028_harappa/ and never enter git).
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
                capture_output=True, text=True, timeout=3600,
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
    ("IndusPhase393HarappaRobustness",
     "phase393_harappa_robustness.py",
     "phase393_results.json",
     "Phase-393 Harappa Robustness (spec 028)",
     "Phase-393 (spec 028): Harappa-robustness follow-up to "
     "the Spec 027 Stage 1 Q2 gate under "
     "specs/028-harappa-robustness/freeze.md (Amendment 1 "
     "included) — Arm A (primary): the Phase-392 population "
     "minus Harappa through the identical machinery "
     "(adjusted PERMANOVA R^2 for site on M77 composition, "
     "cell rarefaction n=49, 199 draws, 499 permutations "
     "within type x legible-length strata, margin 0.01, "
     "LOSO over 5 sites, S-complete sensitivity); Arm B "
     "(secondary): site-equal-weight estimand, quota 52 per "
     "site per draw, LOSO over 6 sites; per-arm "
     "discriminating controls with per-draw regenerated "
     "synthetic populations (failure = that arm INVALID); "
     "Arm C exploratory Harappa decomposition (no verdict). "
     "Per-arm verdicts in the Spec 026 taxonomy; "
     "hierarchical reporting, no pooled headline. Seed "
     "20261012. No anchor or PRED contact; Phase-392's "
     "record is never modified. CPU."),
]


def _phase393_node_defs():
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
