"""Experiment Graph Nodes: Phase-116–121 (final push to 100%).

  IndusSARecal         Phase-116: SA re-calibration with 131 anchors → MEDIUM→HIGH upgrades
  IndusGrammarLow      Phase-117: Commit Phase-112 grammar inferences as LOW anchors
  IndusSiteSemantic    Phase-118: Site-stratified semantic field analysis
  IndusArxivDraft      Phase-119: arXiv preprint draft
  IndusLowToMedium     Phase-120: Final LOW→MEDIUM upgrade sprint
  IndusFullEmail       Phase-121: Comprehensive decipherment email
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _get_device():
    try:
        from glossa_lab.gpu_utils import detect_device  # noqa: PLC0415
        return detect_device()
    except Exception:  # noqa: BLE001
        return "cpu"


def _run(script: str, timeout: int = 3600) -> dict:
    s = _SCRIPTS / script
    rp = _REPORTS / script.replace(".py", ".json")
    if not s.exists():
        return {"error": f"Script not found: {script}"}
    try:
        r = subprocess.run(
            [sys.executable, str(s)],
            capture_output=True, text=True,
            timeout=timeout, cwd=str(_REPO),
        )
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-600:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timeout after {timeout}s"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}
    if rp.exists():
        try:
            return json.loads(rp.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase116_121_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    specs = [
        (
            "IndusSARecal",
            "SA Re-calibration (131 anchors)",
            "phase116_sa_recalibration.py",
            "Phase-116: Re-run ensemble SA calibration with 131 anchors pinned (vs Phase-73's ~40). "
            "Assigns ENSEMBLE_HIGH/MEDIUM tiers to all unread signs. Then re-applies Phase-113 "
            "upgrade criteria → promotes additional MEDIUM anchors to HIGH. GPU.",
        ),
        (
            "IndusGrammarLow",
            "Grammar Inferences → LOW Anchors",
            "phase117_grammar_low_anchors.py",
            "Phase-117: Commits Phase-112 grammar-slot inferences (≥2 contexts) as LOW confidence "
            "anchors in INDUS_FINAL_ANCHORS. Bridges the remaining 11.7% gap from the H+M coverage. CPU.",
        ),
        (
            "IndusSiteSemantic",
            "Site-Stratified Semantic Analysis",
            "phase118_site_semantic.py",
            "Phase-118: Loads Phase-114 translations grouped by site (Harappa, Mohenjo-daro, "
            "Dholavira, etc.). Computes semantic field profiles per site: animal clans, "
            "personal names, titles, place markers. Identifies site-specific patterns. CPU.",
        ),
        (
            "IndusArxivDraft",
            "arXiv Preprint Draft",
            "phase119_arxiv_draft.py",
            "Phase-119: Generates a structured academic preprint draft using all accumulated "
            "evidence: M293 proof, 131-anchor table, Phase-115 statistics, TB validation, "
            "1,048-seal translation corpus. Outputs LaTeX-ready abstract + sections. CPU.",
        ),
        (
            "IndusLowToMedium",
            "Final LOW→MEDIUM Upgrade",
            "phase120_low_to_medium.py",
            "Phase-120: Upgrades the strongest Phase-111 allographs and Phase-117 grammar "
            "anchors from LOW to MEDIUM using positional + frequency thresholds. "
            "Final anchor inventory consolidation. CPU.",
        ),
        (
            "IndusFullEmail",
            "Full Decipherment Assessment Email",
            "phase121_full_email.py",
            "Phase-121: Sends a comprehensive decipherment status email with full insights, "
            "statistics, anchor table, significance test results, and next-steps roadmap. CPU.",
        ),
    ]

    nodes = []
    for nid, name, script, desc in specs:
        def _make_fn(s=script):
            def fn(inputs: dict, params: dict) -> dict:
                return {**_run(s), "gpu_device": _get_device()}
            return fn

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[
                {"name": "result",     "type": "json"},
                {"name": "gpu_device", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_make_fn(),
        ))
    return nodes
