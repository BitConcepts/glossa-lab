"""Experiment Graph Nodes: Phase 434 (Spec 071 —
the Hunt sky signs successor on the Shakti
corpus: do the sky signs gather at the ends of
texts, in re-scoped form).

  IndusPhase434SkySigns   Phase-434: the step-0
  gates in order (0.1 Asset A asserted against
  the pin source the freeze fixed - Spec 069's
  asset-a-freeze.json in its merged executed
  record; 0.2 the Shakti intake under P-F1 S1/S2;
  0.3 input integrity and coverage - every sign
  occurring in the primary population carrying
  exactly one Asset A row; 0.4 the
  terminal-strong frame enumerated and published
  in Wells space before any test, the celestial
  and comparison censuses, the TOO THIN floor;
  0.5 the freeze-order proof), then the single
  counting run under Spec 050's criteria carried
  unchanged.

The node serves the phase's committed results JSON
(reports/phase434_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/071-hunt-sky-
signs-successor/freeze.md (digest c06a7a86...); the
frozen spec's contract registration is OSF
https://osf.io/b62p4/.
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
    ("IndusPhase434SkySigns",
     "phase434_sky_signs.py",
     "phase434_results.json",
     "Phase-434 Sky Signs on Shakti (spec 071)",
     "Phase-434 (spec 071): execution of the frozen Spec "
     "071 contract - step-0 gates in order (0.1 Asset A "
     "frozen under Spec 069, pin source Spec 069's "
     "asset-a-freeze.json, digest recomputing to "
     "95231935...; 0.2 the Shakti intake under P-F1 "
     "S1/S2; 0.3 input integrity and coverage - every "
     "sign occurring in the primary population carrying "
     "exactly one Asset A row, an absent row never "
     "treated as non-celestial by default; 0.4 the "
     "terminal-strong frame enumerated in Wells space "
     "and published before any test, the celestial and "
     "comparison censuses, the TOO THIN floor at 30 "
     "total occurrences; 0.5 the freeze-order proof "
     "including this freeze following Spec 070's), then "
     "one counting run under Spec 050's criteria "
     "carried unchanged (ratio >= 1.5, two-sided Fisher "
     "exact at 5 percent, the half-of-occurrences "
     "condition), sensitivities S1/S2/S3. Outcome as "
     "recorded in reports/phase434_results.json. CPU."),
]


def _phase434_node_defs():
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
