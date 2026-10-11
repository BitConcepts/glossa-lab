"""Experiment Graph Nodes: Phases 391-392 (Spec 027 — movement,
culture, and language in the greater Indus world).

  IndusPhase391Stage0Spine    Stage 0: gazetteer + chronology spine
  (IndusPhase392Q2Gate is added by the Stage 1 execution step,
  before that script runs — H23.)

(Numbering note: 391+ because the repository's registered phase
space ends at Phase-386 (Spec 026) and 387-390 are claimed by
the docstring of the legacy unregistered script
backend/scripts/phase382_390_actionable.py. Recorded in
specs/027-movement-culture-language/adjudication.md.)

Each node serves its phase's committed results JSON
(reports/phaseNNN_results.json), recomputing via the phase
script when that script's pinned inputs are present locally
(the Stage 0 inputs live in the gitignored local store
corpora/downloads/spec027_stage0/ and never enter git).
Freezes: specs/027-movement-culture-language/stage0-freeze.md,
stage1-freeze.md.
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
    ("IndusPhase391Stage0Spine", "phase391_stage0_spine.py",
     "phase391_results.json",
     "Phase-391 Stage-0 Gazetteer + Chronology Spine (spec 027)",
     "Phase-391 (spec 027, Stage 0): source-asserted settlement "
     "gazetteer (CISI Vols 1-2 catalogue layer + XRONOS) and "
     "traced chronology spine (XRONOS export + Mutin et al. "
     "2025 SI Table S2 as a CONTESTED scenario), built under "
     "stage0-freeze.md from pinned, hash-asserted inputs. "
     "Descriptive infrastructure only; mints no verdict. The "
     "Q6 timing-support assessment applies criteria frozen "
     "before the build. CPU."),
]


def _phase391_392_node_defs():
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
