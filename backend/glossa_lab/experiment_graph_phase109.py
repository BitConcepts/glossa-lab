"""Experiment Graph Nodes: Phase-109 (spec 007) — Phase-108 follow-through.

Ledger-sequence Phase-109 (2026-10-06): executes the Phase-108
provenance audit's recommendations under pre-registered rules —
staging-cohort re-review, SA-lineage provenance flags, M293 /
M362 / M398 re-reviews, and the headline re-base recomputation.
Nodes run the phase scripts in `decide` mode (decision/dossier
artifacts only); application to the anchors file is a separate,
reviewed step in the package workflow.

  IndusPhase109StagingReview  Step 1: staging-cohort decisions
  IndusPhase109SaFlags        Step 2: SA-lineage flag set
  IndusPhase109Rereviews      Step 3: M293/M362/M398 dossiers
  IndusPhase109Rebase         Step 5: re-base recomputation
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _run(script: str, args: list[str], report: str, timeout: int = 1800):
    s = _SCRIPTS / script
    rp = _REPORTS / report
    if not s.exists():
        return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(s), *args], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    if rp.exists():
        try:
            return json.loads(rp.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase109_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase109StagingReview", "Phase-109 Staging-Cohort Re-Review",
         "phase109_step1_staging_review.py", [], "phase109_step1_decisions.json",
         "Phase-109 Step 1 (spec 007): per-anchor evidence assembly and "
         "(a) keep / (b) restore / (c) demote decisions for the 116 "
         "research-loop staging anchors. Decide mode — touches nothing. CPU."),
        ("IndusPhase109SaFlags", "Phase-109 SA-Lineage Provenance Flags",
         "phase109_step2_sa_flags.py", [], "phase109_step2_flags.json",
         "Phase-109 Step 2 (spec 007): the 44 SA_DERIVED + SA_CONFIRMED_ONLY "
         "HIGH anchors flagged pending_non_sa_validation (no value/tier "
         "change). Decide mode. CPU."),
        ("IndusPhase109Rereviews", "Phase-109 Individual Re-Reviews",
         "phase109_step3_rereviews.py", [], "phase109_dossier_M293.json",
         "Phase-109 Step 3 (spec 007): evidence dossiers for M293, M362, "
         "M398 and the pre-registered tier-cap determinations. Decide "
         "mode. CPU."),
        ("IndusPhase109Rebase", "Phase-109 Headline Re-Base Recomputation",
         "phase109_step5_rebase.py", [], "phase109_rebase.json",
         "Phase-109 Step 5 (spec 007): headline quantities recomputed "
         "fresh on the post-change anchor set (Phase-108 methods, strict "
         "SA-independent subset). Decide mode. CPU."),
    ]
    nodes = []
    for nid, name, script, args, report, desc in specs:
        def fn(i, p, s=script, a=args, r=report):
            return {**_run(s, a, r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}}, fn=fn))
    return nodes
