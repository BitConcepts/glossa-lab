"""Experiment Graph atomic nodes for Phases 169–170.

Final two phases before the ICIT corpus frontier.

Nodes:
  IndusMasterSynthesis169  — Phase-169 (full evidence scorecard Phases 1-168)
  IndusGrammarVariance170  — Phase-170 (grammar explained variance at 161 H+M)
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
_REPORTS = _REPO / "backend" / "reports"


def _run_phase_script(script_name: str, timeout: int = 300) -> dict[str, Any]:
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
            return {"error": f"Script exited {result.returncode}", "stderr": result.stderr[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Script timed out after {timeout}s"}
    except Exception as exc:
        return {"error": str(exc)}
    return {"status": "ok", "stdout_tail": result.stdout[-500:]}


def _load_report(json_name: str) -> dict[str, Any]:
    path = _REPORTS / json_name
    if not path.exists():
        return {"available": False, "error": f"Report not found: {json_name}"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "error": str(exc)}


# ── Phase-169: Master Evidence Synthesis ─────────────────────────────────────

def _master_synthesis_169(inputs: dict, params: dict) -> dict[str, Any]:
    """Phase-169: updated master evidence scorecard covering Phases 1-168."""
    report = _load_report("phase169_master_synthesis.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase169_master_synthesis.py", timeout=120)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-169 error", "gpu_device": "cpu"}
        report = _load_report("phase169_master_synthesis.json")
    agg       = report.get("aggregate_confidence_pct", 0.0)
    n_items   = report.get("n_evidence_items", 0)
    n_strong  = report.get("n_strongly_confirmed", 0)
    scorecard = report.get("evidence_scorecard", [])
    return {
        "aggregate_confidence_pct":    agg,
        "n_evidence_items":            n_items,
        "n_strongly_confirmed":        n_strong,
        "evidence_scorecard":          scorecard,
        "json": {"agg": agg, "n_items": n_items, "n_strong": n_strong},
        "number": agg,
        "text":   (f"Phase-169 synthesis: {n_items} evidence items, "
                   f"{agg:.0f}% aggregate confidence, {n_strong} strongly confirmed."),
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Phase-170: Grammar Variance Retest ───────────────────────────────────────

def _grammar_variance_170(inputs: dict, params: dict) -> dict[str, Any]:
    """Phase-170: grammar explained variance retest with 161 H+M anchors."""
    report = _load_report("phase170_grammar_variance.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase170_grammar_variance.py", timeout=120)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-170 error", "gpu_device": "cpu"}
        report = _load_report("phase170_grammar_variance.json")
    var_pct    = report.get("explained_variance_pct", 0.0)
    hm_count   = report.get("hm_count", 0)
    delta      = report.get("delta_from_phase133", 0.0)
    verdict    = report.get("verdict", "UNKNOWN")
    return {
        "explained_variance_pct": var_pct,
        "hm_count":               hm_count,
        "delta_from_phase133":    delta,
        "verdict":                verdict,
        "json": {"var_pct": var_pct, "hm_count": hm_count, "delta": delta},
        "number": var_pct,
        "text":   (f"Phase-170 grammar variance: {var_pct:.1f}% explained "
                   f"(was 44.3% at 157 H+M, delta={delta:+.1f}pp at {hm_count} H+M). "
                   f"Verdict: {verdict}."),
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Node definitions ──────────────────────────────────────────────────────────

def _phase169_170_node_defs() -> list[AtomicNodeDef]:
    _STD = [
        {"name": "json",       "type": "json"},
        {"name": "number",     "type": "number"},
        {"name": "text",       "type": "text"},
        {"name": "gpu_device", "type": "text"},
    ]
    return [
        AtomicNodeDef(
            id="IndusMasterSynthesis169",
            name="Master Evidence Synthesis (P169)",
            category="Indus Decipherment",
            description=(
                "Phase-169: updated full evidence scorecard spanning Phases 1–168. "
                "Updates Phase-141 with new confirmations from Parpola 1994, Wells 2015, "
                "Mahadevan grammar, Phase-166 sibilant DEDR validation. "
                "Computes aggregate confidence percentage across all evidence categories."
            ),
            inputs=[],
            outputs=[
                {"name": "aggregate_confidence_pct", "type": "number"},
                {"name": "n_evidence_items",         "type": "number"},
                {"name": "n_strongly_confirmed",     "type": "number"},
                {"name": "evidence_scorecard",       "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_master_synthesis_169,
        ),
        AtomicNodeDef(
            id="IndusGrammarVariance170",
            name="Grammar Variance Retest (P170)",
            category="Indus Decipherment",
            description=(
                "Phase-170: retest grammar explained variance with 161 H+M anchors "
                "(was 44.3% at 157 H+M in Phase-133). Adds 4 sibilant signs. "
                "Reports positional variance explained by the 3-slot grammar model."
            ),
            inputs=[],
            outputs=[
                {"name": "explained_variance_pct", "type": "number"},
                {"name": "hm_count",               "type": "number"},
                {"name": "delta_from_phase133",    "type": "number"},
                {"name": "verdict",                "type": "text"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_grammar_variance_170,
        ),
    ]
