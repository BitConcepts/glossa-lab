"""Experiment Graph Nodes: Phase-135 (spec 024, Stage 1) —
motif-coding re-pilot under the clarified codebook.

Ledger-sequence Phase-135 (2026-10-09): the Stage 1 re-pilot
under the owner's combined-path approval and the clarification
freeze record (specs/024-evidence-integration/
stage1-freeze-2.md). A fresh stratified frame of 100 catalogue
objects (the frozen section 4.2 population minus the 100
Phase-134 frame objects; zero overlap, verified) was coded for
primary motif by two independent blinded passes plus a gold
third coding of a 20-object subset, with adjudication of all
disagreements, under the clarified codebook (freeze-2 section 2:
the ILLEGIBLE / SCRIPT_ONLY / GEOMETRIC legibility boundary,
distilled from Phase-134's adjudicated disagreements). All
coding roles were executed by AI agents in blinded
role-isolated instances (constitution section VI; spec 024
section 4.4). Headline result: exact agreement 0.78, Cohen's
kappa 0.7129 — the frozen section 4.5 gates (unchanged by any
amount) resolve to the MIDDLE BAND for the second time
(proceed gate not met, stop rule not fired); no Stage 2(b)
design follows on this outcome. No association statistic was
computed. This node exposes the re-pilot metrics summary only;
the full dataset is the committed
data/evidence_integration/phase135_pilot_dataset.json and the
report is reports/phase135_pilot_report.md.

  IndusPhase135MotifRepilot
      Stage 1 motif-coding re-pilot metrics summary
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_METRICS = _REPO / "reports" / "phase135_pilot_metrics.json"


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
    script = _SCRIPTS / "phase135_metrics.py"
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
    return {"error": "phase135 metrics not found"}


def _phase135_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase135MotifRepilot",
         "Phase-135 Motif-Coding Re-Pilot (spec 024 Stage 1)",
         "Phase-135 (spec 024, Stage 1 continuation under "
         "stage1-freeze-2): motif-coding reliability re-pilot — "
         "fresh 100-object stratified frame (zero overlap with "
         "Phase-134) coded by two independent blinded passes plus "
         "a gold third coding under the clarified legibility-"
         "boundary codebook, adjudication of all disagreements, "
         "exact agreement and Cohen's kappa measured from the "
         "on-disk records, frozen section 4.5 gates applied "
         "unchanged (verdict: MIDDLE BAND, second time). Coding "
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
