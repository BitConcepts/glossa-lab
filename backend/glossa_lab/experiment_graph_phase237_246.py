"""Experiment graph node definitions for Phases 237-246.

H23 compliance: retroactive registration of unregistered phase scripts.
"""
from __future__ import annotations
import subprocess, sys, json
from pathlib import Path
from glossa_lab.experiment_graph import AtomicNodeDef

_BACKEND = str(Path(__file__).parents[1])

def _run_script(script_name: str) -> dict:
    try:
        r = subprocess.run(
            [sys.executable, f"scripts/{script_name}"],
            capture_output=True, text=True, timeout=300, cwd=_BACKEND,
        )
        out_name = script_name.replace(".py", ".json")
        for d in [Path(__file__).parents[2] / "outputs", Path(__file__).parents[2] / "reports"]:
            p = d / out_name
            if p.exists():
                return json.loads(p.read_text("utf-8"))
        return {"stdout": r.stdout[-500:], "stderr": r.stderr[-300:], "rc": r.returncode}
    except Exception as exc:
        return {"error": str(exc)}

def _make_runner(script: str):
    def _runner(inputs: dict, params: dict) -> dict:
        return _run_script(script)
    return _runner

def _phase237_246_node_defs() -> list[AtomicNodeDef]:
    specs = [
        ("IndusPhase237BlockerMine", "Phase-237 Blocker Targeted Mine",
         "Targeted literature mining for blocker resolution.", "phase237_blocker_targeted_mine.py"),
        ("IndusPhase238BlockerFollowup", "Phase-238 Blocker Follow-up",
         "Follow-up experiments on blocker signs.", "phase238_blocker_followup.py"),
        ("IndusPhase239MediumBatchUpgrade", "Phase-239 Medium Batch Upgrade",
         "Batch upgrade of MEDIUM anchors with dual external corroboration.", "phase239_medium_batch_upgrade.py"),
        ("IndusPhase240UnlockMine", "Phase-240 Unlock Mine",
         "Mining for evidence to unlock MEDIUM to HIGH promotions.", "phase240_unlock_mine.py"),
        ("IndusPhase241_242Experiments", "Phase-241/242 Experiments",
         "Paired experiments for anchor validation and SA refinement.", "phase241_242_experiments.py"),
        ("IndusPhase243Synthesis", "Phase-243 Synthesis Report",
         "Master synthesis report across all evidence lines.", "phase243_synthesis_report.py"),
        ("IndusPhase244E41Dedr", "Phase-244 E41 DEDR Upgrade",
         "DEDR injection for Linear Elamite E41 corroborated anchors.", "phase244_e41_dedr_upgrade.py"),
        ("IndusPhase245_246SACrossing", "Phase-245/246 SA Crossing",
         "SA convergence crossing experiments for anchor stability.", "phase245_246_sa_crossing.py"),
    ]
    return [
        AtomicNodeDef(
            nid, label, "Indus Decipherment", desc,
            inputs=[], outputs=[{"name": "report", "type": "object"}],
            params_schema={"type": "object", "properties": {}},
            fn=_make_runner(script),
        )
        for nid, label, desc, script in specs
    ]
