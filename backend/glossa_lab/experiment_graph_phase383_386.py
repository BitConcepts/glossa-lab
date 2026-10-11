"""Experiment Graph Nodes: Phases 383-386 (Spec 026 — RCPH
framework transfer reruns).

  IndusPhase383PilotRescoring   C4 rescoring of Phases 132/134/135
  IndusPhase384Stage2Margins    C1 margin completion for Phase-137
  IndusPhase385G1Margins        C1 margin completion for Phase-140
  IndusPhase386ReplayAudit      replay audit of Phases 116/125/127/131

(Numbering note: 383+ because the repository's global phase
space already runs to 382 in backend/reports/; the Spec 024/025
sub-series in reports/ ends at 141.)

Each node serves its phase's committed results JSON
(reports/phaseNNN_results.json), recomputing via the phase
script when that script's inputs are present locally (the
Spec 026 rerun scripts read registered files / local research
stores that never enter git). Contracts:
specs/026-rcph-framework-transfer/reruns/.
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
    ("IndusPhase383PilotRescoring", "phase383_pilot_rescoring.py",
     "phase383_results.json",
     "Phase-383 Pilot Rescoring (spec 026)",
     "Phase-383 (spec 026): C4 rescoring of the coding pilots "
     "132/134/135 from their on-disk records — headline "
     "statistics recomputed with the original metrics modules, "
     "bootstrap 95% CIs over objects added, coder origin-group "
     "audit (one origin group: a single model family), verdicts "
     "under the Spec 026 taxonomy. Rescoring only; no re-coding. "
     "CPU."),
    ("IndusPhase384Stage2Margins", "phase384_stage2_margins.py",
     "phase384_results.json",
     "Phase-384 Stage-2 Margin Completion (spec 026)",
     "Phase-384 (spec 026): C1 margin completion for Phase-137 "
     "F2/F3 — chi-square and Cramer's V verified from the "
     "recorded profile tables, parametric bootstrap 95% CI for "
     "V, adjudication against the pre-declared margin V = 0.10. "
     "CPU."),
    ("IndusPhase385G1Margins", "phase385_g1_margins.py",
     "phase385_results.json",
     "Phase-385 G1 Margin Completion (spec 026)",
     "Phase-385 (spec 026): C1 margin completion for Phase-140 "
     "G1 — population and observed chi-square verified, "
     "stratified bootstrap 95% CI for Cramer's V within the "
     "frozen composition x preservation strata, margin "
     "adjudication at V = 0.10; sensitivity CIs exploratory. "
     "Chronology NOT controlled (rider). CPU."),
    ("IndusPhase386ReplayAudit", "phase386_replay_audit.py",
     "phase386_results.json",
     "Phase-386 Replay Audit (spec 026)",
     "Phase-386 (spec 026): deterministic replay audit of "
     "Phases 116/125/127/131 — original scripts re-executed in "
     "a disposable worktree; headline quantities compared by "
     "the comparator (which requires a --replayed-root "
     "argument when recomputing; the node serves the committed "
     "comparison). CPU."),
]


def _phase383_386_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    nodes = []
    for nid, script_name, results_name, name, desc in _NODE_SPECS:
        def fn(i, p, _s=script_name, _r=results_name):
            if _s == "phase386_replay_audit.py":
                results = _REPO / "reports" / _r
                if results.exists():
                    return {"source": "committed_results",
                            **json.loads(results.read_text("utf-8")),
                            "gpu_device": _get_device()}
                return {"error": f"{_r} not found",
                        "gpu_device": _get_device()}
            return {**_serve(_s, _r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
