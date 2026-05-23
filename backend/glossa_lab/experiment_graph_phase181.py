"""Experiment Graph atomic node for Phase 181.

IndusADNAArchaeogeneticsMine181 — aDNA/archaeogenetics mine
  PubMed + bioRxiv + OpenAlex citation network + specialized journals.
  Evidence classification: STRONG / MODERATE / WEAK for Dravidian hypothesis.
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


def _run_phase_script(script_name: str, timeout: int = 900) -> dict[str, Any]:
    script = _SCRIPTS / script_name
    if not script.exists():
        return {"error": f"Script not found: {script_name}"}
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=timeout,
            cwd=str(_REPO),
        )
        if result.returncode != 0:
            return {"error": f"Script exited {result.returncode}",
                    "stderr": result.stderr[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Script timed out after {timeout}s"}
    except Exception as exc:
        return {"error": str(exc)}
    return {"status": "ok", "stdout_tail": result.stdout[-500:]}


def _load_output(json_name: str) -> dict[str, Any]:
    path = _OUTPUTS / json_name
    if not path.exists():
        return {"available": False, "error": f"Output not found: {json_name}"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _adna_mine_181(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load_output("phase181_adna_archaeogenetics_mine.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase181_adna_archaeogenetics_mine.py", timeout=900)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-181 error", "gpu_device": "cpu"}
        report = _load_output("phase181_adna_archaeogenetics_mine.json")

    n_papers   = report.get("n_papers", 0)
    n_strong   = report.get("n_strong_evidence", 0)
    n_moderate = report.get("n_moderate_evidence", 0)
    n_weak     = report.get("n_weak_evidence", 0)
    strong     = report.get("evidence", {}).get("strong", [])

    return {
        "n_papers":            n_papers,
        "n_strong_evidence":   n_strong,
        "n_moderate_evidence": n_moderate,
        "n_weak_evidence":     n_weak,
        "strong_evidence":     strong[:10],
        "source_breakdown":    report.get("source_breakdown", {}),
        "json": {"n_papers": n_papers, "n_strong": n_strong, "n_moderate": n_moderate},
        "number": n_strong + n_moderate,
        "text":   (f"Phase-181 aDNA mine: {n_papers} papers. "
                   f"{n_strong} STRONG (Dravidian ancestry confirmed), "
                   f"{n_moderate} MODERATE (IVC genetics compatible), "
                   f"{n_weak} weak."),
        "gpu_device": "cpu",
    }


def _phase181_node_defs() -> list[AtomicNodeDef]:
    _STD = [
        {"name": "json",       "type": "json"},
        {"name": "number",     "type": "number"},
        {"name": "text",       "type": "text"},
        {"name": "gpu_device", "type": "text"},
    ]
    return [
        AtomicNodeDef(
            id="IndusADNAArchaeogeneticsMine181",
            name="aDNA Archaeogenetics Mine (P181)",
            category="Indus Decipherment",
            description=(
                "Phase-181: aDNA and archaeogenetics literature mine targeting sources "
                "NOT covered by Phases 88/94/179/180. Four tracks: PubMed/NCBI "
                "E-utilities (Harappan ancient DNA, AASI ancestry), bioRxiv/medRxiv "
                "preprints, OpenAlex citation network (papers citing Parpola/Mahadevan/"
                "Narasimhan 2019), and specialized journals (JRAS, BSOAS, Indo-Iranian). "
                "Classifies each paper as STRONG/MODERATE/WEAK evidence for Dravidian "
                "ancestry of IVC population."
            ),
            inputs=[],
            outputs=[
                {"name": "n_papers",            "type": "number"},
                {"name": "n_strong_evidence",   "type": "number"},
                {"name": "n_moderate_evidence", "type": "number"},
                {"name": "n_weak_evidence",     "type": "number"},
                {"name": "strong_evidence",     "type": "json"},
                {"name": "source_breakdown",    "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_adna_mine_181,
        ),
    ]
