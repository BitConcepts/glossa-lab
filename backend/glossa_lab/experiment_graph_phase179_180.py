"""Experiment Graph atomic nodes for Phases 179–180.

Mining batch — recent literature (2021-2026) and Mesopotamian contact evidence.

Nodes:
  IndusRecentLitMine179   — Phase-179 (arXiv + S2 + CORE + author-targeted, 2021+)
  IndusMesopotamianMine180 — Phase-180 (CDLI + Meluhhan names + phonological gap update)
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
_REPORTS = _REPO / "research" / "indus" / "phase_reports"


def _run_phase_script(script_name: str, timeout: int = 600) -> dict[str, Any]:
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


# ── Phase-179 ────────────────────────────────────────────────────────────────

def _recent_lit_mine_179(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load_output("phase179_recent_lit_mine.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase179_recent_lit_mine.py", timeout=600)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-179 error", "gpu_device": "cpu"}
        report = _load_output("phase179_recent_lit_mine.json")

    n_papers = report.get("n_papers", 0)
    n_sign   = report.get("n_sign_proposals", 0)
    n_adna   = report.get("n_adna_evidence", 0)
    n_new    = report.get("n_new_data", 0)
    n_icit   = report.get("n_icit_mentions", 0)
    return {
        "n_papers":          n_papers,
        "n_sign_proposals":  n_sign,
        "n_adna_evidence":   n_adna,
        "n_new_data":        n_new,
        "n_icit_mentions":   n_icit,
        "year_distribution": report.get("year_distribution", {}),
        "adna_evidence":     report.get("adna_evidence", []),
        "sign_proposals":    report.get("sign_proposals", []),
        "json":   {"n_papers": n_papers, "n_sign": n_sign, "n_adna": n_adna},
        "number": n_papers,
        "text":   (f"Phase-179: {n_papers} papers (2021-2026). "
                   f"{n_sign} sign proposals, {n_adna} aDNA items, "
                   f"{n_new} new-data signals, {n_icit} ICIT mentions."),
        "gpu_device": "cpu",
    }


# ── Phase-180 ────────────────────────────────────────────────────────────────

def _mesopotamian_mine_180(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load_output("phase180_mesopotamian_mine.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase180_mesopotamian_mine.py", timeout=600)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-180 error", "gpu_device": "cpu"}
        report = _load_output("phase180_mesopotamian_mine.json")

    gap  = report.get("gap_analysis", {})
    n_new_ev  = gap.get("n_new_evidence", 0)
    n_low     = gap.get("n_low_candidates", 0)
    n_true_g  = gap.get("n_true_gaps", 14)
    n_new_names = report.get("n_new_names", 0)
    cdli_refs   = report.get("cdli_results", {}).get("n_meluhha_refs", 0)
    return {
        "cdli_meluhha_refs":  cdli_refs,
        "n_new_meluhhan_names": n_new_names,
        "phoneme_new_evidence": n_new_ev,
        "phoneme_low_candidates": n_low,
        "phoneme_true_gaps":  n_true_g,
        "phoneme_coverage":   gap.get("phoneme_coverage", []),
        "json": {
            "cdli_refs": cdli_refs, "n_new_names": n_new_names,
            "n_new_ev": n_new_ev, "n_true_gaps": n_true_g,
        },
        "number": n_new_ev + n_low,
        "text":   (f"Phase-180: {cdli_refs} CDLI Meluhha refs, {n_new_names} new names. "
                   f"Phoneme gaps: {n_new_ev} new evidence, {n_low} LOW candidates, "
                   f"{n_true_g} true gaps remain."),
        "gpu_device": "cpu",
    }


# ── Node definitions ──────────────────────────────────────────────────────────

def _phase179_180_node_defs() -> list[AtomicNodeDef]:
    _STD = [
        {"name": "json",       "type": "json"},
        {"name": "number",     "type": "number"},
        {"name": "text",       "type": "text"},
        {"name": "gpu_device", "type": "text"},
    ]
    return [
        AtomicNodeDef(
            id="IndusRecentLitMine179",
            name="Recent Literature Mine (P179)",
            category="Indus Decipherment",
            description=(
                "Phase-179: recent literature mine 2021-2026 across four tracks: "
                "arXiv cs.CL/cs.AI, Semantic Scholar year-filtered, CORE open-access "
                "fulltext, and author-targeted search (Parpola, Rao, Vahia, Mahadevan). "
                "Improved table-aware sign extraction + aDNA/archaeogenetics evidence + "
                "new-data signals (Rakhigarhi, Dholavira) + ICIT mentions."
            ),
            inputs=[],
            outputs=[
                {"name": "n_papers",         "type": "number"},
                {"name": "n_sign_proposals", "type": "number"},
                {"name": "n_adna_evidence",  "type": "number"},
                {"name": "n_icit_mentions",  "type": "number"},
                {"name": "adna_evidence",    "type": "json"},
                {"name": "sign_proposals",   "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_recent_lit_mine_179,
        ),
        AtomicNodeDef(
            id="IndusMesopotamianMine180",
            name="Mesopotamian Contact Mine (P180)",
            category="Indus Decipherment",
            description=(
                "Phase-180: Mesopotamian contact evidence mine. Track A: CDLI texts "
                "mentioning Meluhha/Melukhha (Ur III administrative corpus). Track B: "
                "Semantic Scholar Mesopotamian contact phonology. Track C: OpenAlex "
                "Bronze Age contact zone. Track D: phonological gap re-analysis — "
                "cross-references Phase-178 absent phonemes against new Meluhhan names "
                "and LOW-confidence sign candidates. Produces ICIT-targeted phoneme list."
            ),
            inputs=[],
            outputs=[
                {"name": "cdli_meluhha_refs",       "type": "number"},
                {"name": "n_new_meluhhan_names",    "type": "number"},
                {"name": "phoneme_new_evidence",    "type": "number"},
                {"name": "phoneme_low_candidates",  "type": "number"},
                {"name": "phoneme_true_gaps",       "type": "number"},
                {"name": "phoneme_coverage",        "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_mesopotamian_mine_180,
        ),
    ]
