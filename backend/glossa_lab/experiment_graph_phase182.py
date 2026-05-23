"""Experiment Graph atomic node for Phase 182.

IndusDeepEvidenceMine182 — deep evidence mine
  Shodhganga + forward citations + Zenodo/HAL + JSTOR OA + strong paper fulltext.
  Outputs new scorecard evidence items for the master synthesis.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from glossa_lab.experiment_graph import AtomicNodeDef

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend" / "scripts"
_OUTPUTS = _REPO / "outputs"


def _run(script: str, timeout: int = 900) -> dict[str, Any]:
    p = _SCRIPTS / script
    if not p.exists():
        return {"error": f"Script not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True,
                           timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"Exit {r.returncode}", "stderr": r.stderr[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout after {timeout}s"}
    except Exception as exc:
        return {"error": str(exc)}
    return {"status": "ok", "stdout_tail": r.stdout[-500:]}


def _load(json_name: str) -> dict[str, Any]:
    p = _OUTPUTS / json_name
    if not p.exists():
        return {"available": False, "error": f"Not found: {json_name}"}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _deep_evidence_mine_182(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load("phase182_deep_evidence_mine.json")
    if report.get("available") is False:
        run_result = _run("phase182_deep_evidence_mine.py", timeout=900)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-182 error", "gpu_device": "cpu"}
        report = _load("phase182_deep_evidence_mine.json")

    n_papers  = report.get("n_papers", 0)
    n_strong  = report.get("n_strong_evidence", 0)
    n_mod     = report.get("n_moderate_evidence", 0)
    n_new_ev  = len(report.get("new_scorecard_items", []))
    strong_ext = report.get("strong_paper_extraction", {})

    return {
        "n_papers":            n_papers,
        "n_strong_evidence":   n_strong,
        "n_moderate_evidence": n_mod,
        "n_new_scorecard_items": n_new_ev,
        "new_scorecard_items": report.get("new_scorecard_items", []),
        "strong_paper_found":  strong_ext.get("found", False),
        "strong_paper_proposals": len(strong_ext.get("sign_proposals", [])),
        "source_breakdown":    report.get("source_breakdown", {}),
        "json": {"n_papers": n_papers, "n_strong": n_strong, "n_new_ev": n_new_ev},
        "number": n_strong + n_mod,
        "text":   (f"Phase-182 deep mine: {n_papers} papers. "
                   f"{n_strong} STRONG, {n_mod} MODERATE. "
                   f"{n_new_ev} new scorecard items identified."),
        "gpu_device": "cpu",
    }


def _phase182_node_defs() -> list[AtomicNodeDef]:
    _STD = [
        {"name": "json",       "type": "json"},
        {"name": "number",     "type": "number"},
        {"name": "text",       "type": "text"},
        {"name": "gpu_device", "type": "text"},
    ]
    return [
        AtomicNodeDef(
            id="IndusDeepEvidenceMine182",
            name="Deep Evidence Mine (P182)",
            category="Indus Decipherment",
            description=(
                "Phase-182: deep evidence mine targeting sources not covered by "
                "Phases 88-181. Four tracks: Shodhganga Indian thesis database; "
                "forward citation chains of 2023 IVC-Dravidian paper + Rakhigarhi "
                "genome + Narasimhan 2019; Zenodo + HAL European open archives; "
                "JSTOR OA filtered. Plus full-text extraction of the 2023 STRONG "
                "paper for sign-level evidence. Outputs new_scorecard_items for "
                "addition to the Phase-169 master evidence synthesis."
            ),
            inputs=[],
            outputs=[
                {"name": "n_papers",               "type": "number"},
                {"name": "n_strong_evidence",       "type": "number"},
                {"name": "n_moderate_evidence",     "type": "number"},
                {"name": "n_new_scorecard_items",   "type": "number"},
                {"name": "new_scorecard_items",     "type": "json"},
                {"name": "strong_paper_found",      "type": "text"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_deep_evidence_mine_182,
        ),
    ]
