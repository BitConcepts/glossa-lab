"""Experiment Graph Nodes: Phase-134 (spec 024, Stage 1) —
motif-coding pilot.

Ledger-sequence Phase-134 (2026-10-09): the Stage 1 pilot under
frozen spec 024 §4 and the stage freeze record
(specs/024-evidence-integration/stage1-freeze.md). A stratified
frame of 100 catalogue objects (site-group x object type,
sha256-seeded selection) was coded for primary motif by two
independent blinded passes plus a gold third coding of a 20-object
subset, with adjudication of all disagreements. All coding roles
were executed by AI agents in blinded role-isolated instances
(constitution section VI; spec 024 section 4.4). Headline result:
exact agreement 0.84, Cohen's kappa 0.7885 — the frozen section 4.5
gates resolve to the MIDDLE BAND (proceed gate not met, stop rule
not fired). No association statistic was computed. This node
exposes the pilot metrics summary only; the full dataset is the
committed data/evidence_integration/phase134_pilot_dataset.json
and the report is reports/phase134_pilot_report.md.

  IndusPhase134MotifPilot
      Stage 1 motif-coding pilot metrics summary
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_METRICS = _REPO / "reports" / "phase134_pilot_metrics.json"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _summary(metrics: dict, source: str) -> dict:
    return {
        "source": source,
        "phase": metrics["phase"],
        "n_sample": metrics["n_sample"],
        "exact_agreement": metrics["exact_agreement"],
        "cohens_kappa": metrics["cohens_kappa"],
        "gates": metrics["gates"],
        "per_category": metrics["per_category"],
        "confusion_pairs": metrics["confusion_pairs"],
        "gold_drift": metrics["gold_drift"],
        "adjudication_rate": metrics["adjudication_rate"],
        "ai_disclosure": metrics["ai_disclosure"],
    }


def _run_metrics():
    """Recompute via the metrics script when the local record store
    is present; otherwise serve the committed metrics (the script's
    inputs are local-store records that never enter git)."""
    script = _SCRIPTS / "phase134_metrics.py"
    if script.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)], capture_output=True,
                text=True, timeout=600, cwd=str(_REPO))
            if r.returncode == 0 and _METRICS.exists():
                return _summary(
                    json.loads(_METRICS.read_text("utf-8")),
                    "metrics_recomputed")
        except Exception:  # noqa: BLE001
            pass
    if _METRICS.exists():
        return _summary(json.loads(_METRICS.read_text("utf-8")),
                        "committed_metrics")
    return {"error": "phase134 metrics not found"}


def _phase134_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase134MotifPilot",
         "Phase-134 Motif-Coding Pilot (spec 024 Stage 1)",
         "Phase-134 (spec 024, FROZEN Stage 1): motif-coding "
         "reliability pilot — 100-object stratified frame coded by "
         "two independent blinded passes plus a gold third coding, "
         "adjudication of all disagreements, exact agreement and "
         "Cohen's kappa measured from the on-disk records, frozen "
         "section 4.5 gates applied (verdict: MIDDLE BAND). Coding "
         "roles executed by AI agents in blinded role-isolated "
         "instances (constitution section VI). Reliability only: "
         "no association statistics, no anchor or PRED changes. "
         "Recomputes from the local store when present and "
         "otherwise serves the committed metrics JSON. CPU."),
    ]
    nodes = []
    for nid, name, desc in specs:
        def fn(i, p):
            return {**_run_metrics(), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
