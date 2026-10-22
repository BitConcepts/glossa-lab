"""Experiment Graph Nodes: Phase 397 (Spec 033 —
SA-Free Language Comparison).

  IndusPhase397LanguageComparison    Phase-397: the frozen
  Spec 033 estimator run over the strict sign set — Dravidian vs
  Sanskrit vs Munda vs no-language baseline vs 999 random
  assignments, no semantic-anchoring machinery anywhere

The node serves the phase's committed results JSON
(reports/phase397_results.json), recomputing via the phase
script when that script's pinned inputs are present locally.
Freeze: specs/033-sa-free-language-comparison/freeze.md
(digest 412b4805...); registered before execution at OSF
https://osf.io/ephf7/ (DOI 10.17605/OSF.IO/EPHF7).
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
    ("IndusPhase397LanguageComparison",
     "phase397_sa_free_language_comparison.py",
     "phase397_results.json",
     "Phase-397 SA-Free Language Comparison (spec 033)",
     "Phase-397 (spec 033): execution of the frozen Spec 033 "
     "contract — the Dravidian-versus-rivals sign-sequence "
     "comparison rerun with no semantic-anchoring machinery "
     "(H26): the strict sign set (94 strict_sa_independent "
     "anchors), anchor values frozen as cited data before "
     "scoring (five published candidates per family; a second "
     "list per family as the robustness arm), the freeze-time "
     "estimator (counted conditional model, add-one smoothing, "
     "mean log probability per sign, identical for every family "
     "and control), 999 random-assignment controls, the "
     "Harappa-removed sensitivity, and the frozen verdict rules "
     "(margin 0.10 and the 99th-percentile condition both "
     "required for SUPPORTED). CPU."),
]


def _phase397_node_defs():
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
