"""Experiment Graph atomic nodes for Phases 166–168.

This is the final computationally-achievable phase group before ICIT corpus
access is required. After Phase 168, the decipherment frontier cannot advance
further with available data.

Nodes:
  IndusSibilantDedrValidation  — Phase-166 (DEDR cross-validation of 4 sibilant
                                  MEDIUM upgrades: M330=can, M165=cul,
                                  M202=can, M198=co)
  IndusMeluhhanNamesExpanded   — Phase-167 (expand from 6 to ~25 Ur III
                                  Meluhhan personal names, match against seals)
  IndusBlockerTargetedSA       — Phase-168 (GPU SA with 161 pinned anchors,
                                  targeted at top decode-blocking LOW signs)
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


# ── Phase-166: Sibilant DEDR Cross-Validation ────────────────────────────────

def _sibilant_dedr_validation(inputs: dict, params: dict) -> dict[str, Any]:
    """Run or load Phase-166: DEDR cross-validation of Phase-163 sibilant upgrades.

    Tests M330=can, M165=cul, M202=can, M198=co against:
      - DEDR entries for proposed sibilant readings
      - Positional profile consistency (sibilant-initial syllables)
      - Phonotactic gap analysis
      - Cross-corpus frequency under proposed readings
    Verdict per sign: CONFIRMED / PROVISIONAL / REJECTED
    """
    report = _load_report("phase166_sibilant_dedr_validation.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase166_sibilant_dedr_validation.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-166 error", "gpu_device": "cpu"}
        report = _load_report("phase166_sibilant_dedr_validation.json")

    verdicts      = report.get("verdicts", {})
    n_confirmed   = sum(1 for v in verdicts.values() if v == "CONFIRMED")
    n_provisional = sum(1 for v in verdicts.values() if v == "PROVISIONAL")
    n_rejected    = sum(1 for v in verdicts.values() if v == "REJECTED")
    overall       = report.get("overall_verdict", "UNKNOWN")
    dedr_hits     = report.get("dedr_hit_count", 0)

    return {
        "verdicts":         verdicts,
        "n_confirmed":      n_confirmed,
        "n_provisional":    n_provisional,
        "n_rejected":       n_rejected,
        "overall_verdict":  overall,
        "dedr_hit_count":   dedr_hits,
        "json": {"verdicts": verdicts, "overall": overall},
        "number":  float(n_confirmed),
        "text": (f"Phase-166 sibilant DEDR validation: {n_confirmed} CONFIRMED, "
                 f"{n_provisional} PROVISIONAL, {n_rejected} REJECTED. "
                 f"Overall: {overall}. DEDR hits: {dedr_hits}."),
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Phase-167: Meluhhan Names Expanded ───────────────────────────────────────

def _meluhhan_names_expanded(inputs: dict, params: dict) -> dict[str, Any]:
    """Run or load Phase-167: expanded Meluhhan personal name matching.

    Extends Phase-164 from 6 to ~25 attested Ur III Meluhhan personal names
    (Parpola 1975, Steinkeller 1982, Potts 1994, Reade 2001).
    Matches phonological sequences against 1,670 Holdat seals using the
    161-anchor reading set. Reports all matches with ≥2/N slot coverage.
    """
    report = _load_report("phase167_meluhhan_names_expanded.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase167_meluhhan_names_expanded.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-167 error", "gpu_device": "cpu"}
        report = _load_report("phase167_meluhhan_names_expanded.json")

    n_names       = report.get("n_names_tested", 0)
    n_strong      = report.get("n_strong_matches", 0)
    n_partial     = report.get("n_partial_matches", 0)
    top_matches   = report.get("top_matches", [])
    verdict       = report.get("verdict", "NO_STRONG_MATCH")

    return {
        "n_names_tested":   n_names,
        "n_strong_matches": n_strong,
        "n_partial_matches": n_partial,
        "top_matches":      top_matches,
        "verdict":          verdict,
        "json": {"n_names": n_names, "verdict": verdict, "top": top_matches[:5]},
        "number": float(n_strong),
        "text": (f"Phase-167 Meluhhan names ({n_names} tested): "
                 f"{n_strong} strong (≥3/N slots), {n_partial} partial. "
                 f"Verdict: {verdict}."),
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Phase-168: Decode-Blocker Targeted SA ────────────────────────────────────

def _blocker_targeted_sa(inputs: dict, params: dict) -> dict[str, Any]:
    """Run or load Phase-168: GPU SA targeted at top decode-blocking LOW signs.

    Pins all 161 H+M anchors, runs BigramScorer SA (GPU) with focus on the
    top 20 decode-blocking LOW signs from Phase-130. For each blocker sign,
    records whether SA converges to the existing LOW reading or proposes a
    different one. Computes new coverage estimate if converged readings hold.
    This is the final computationally-achievable experiment before ICIT.
    """
    report = _load_report("phase168_blocker_sa.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase168_blocker_sa.py", timeout=900)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-168 error", "gpu_device": "cpu"}
        report = _load_report("phase168_blocker_sa.json")

    n_converged      = report.get("n_converged_to_low", 0)
    n_diverged       = report.get("n_diverged", 0)
    n_tested         = report.get("n_blockers_tested", 0)
    z_score          = report.get("z_score", 0.0)
    new_coverage_est = report.get("new_coverage_estimate", 0.0)
    verdict          = report.get("verdict", "UNKNOWN")
    blocker_results  = report.get("blocker_results", [])

    return {
        "n_blockers_tested":   n_tested,
        "n_converged_to_low":  n_converged,
        "n_diverged":          n_diverged,
        "z_score":             z_score,
        "new_coverage_estimate": new_coverage_est,
        "verdict":             verdict,
        "blocker_results":     blocker_results,
        "json": {"n_tested": n_tested, "n_converged": n_converged,
                 "z_score": z_score, "verdict": verdict},
        "number": z_score,
        "text": (f"Phase-168 blocker SA: {n_tested} blockers tested, "
                 f"{n_converged} converged to LOW reading, {n_diverged} diverged. "
                 f"z={z_score:.2f}. Coverage estimate: {new_coverage_est:.2%}. "
                 f"Verdict: {verdict}. "
                 f"[FINAL PHASE — ICIT corpus required to proceed further.]"),
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Node definitions ──────────────────────────────────────────────────────────

def _phase166_168_node_defs() -> list[AtomicNodeDef]:
    _STD = [
        {"name": "json",       "type": "json"},
        {"name": "number",     "type": "number"},
        {"name": "text",       "type": "text"},
        {"name": "gpu_device", "type": "text"},
    ]
    return [
        AtomicNodeDef(
            id="IndusSibilantDedrValidation",
            name="Sibilant DEDR Validation (P166)",
            category="Indus Decipherment",
            description=(
                "Phase-166: DEDR cross-validation of the 4 Phase-163 sibilant MEDIUM upgrades "
                "(M330=can, M165=cul, M202=can, M198=co). Tests each against DEDR entries, "
                "positional profiles, and phonotactics. Verdict: CONFIRMED / PROVISIONAL / REJECTED."
            ),
            inputs=[],
            outputs=[
                {"name": "verdicts",        "type": "json"},
                {"name": "n_confirmed",     "type": "number"},
                {"name": "n_provisional",   "type": "number"},
                {"name": "n_rejected",      "type": "number"},
                {"name": "overall_verdict", "type": "text"},
                {"name": "dedr_hit_count",  "type": "number"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_sibilant_dedr_validation,
        ),
        AtomicNodeDef(
            id="IndusMeluhhanNamesExpanded",
            name="Meluhhan Names Expanded (P167)",
            category="Indus Decipherment",
            description=(
                "Phase-167: expanded Meluhhan personal name matching using ~25 attested "
                "Ur III names (Parpola 1975, Steinkeller 1982, Potts 1994). "
                "Matches phonological sequences against 1,670 Holdat seals with 161-anchor set. "
                "Phase-164 used 6 names (no strong hits). This is the final name-matching experiment "
                "achievable without ICIT corpus."
            ),
            inputs=[],
            outputs=[
                {"name": "n_names_tested",    "type": "number"},
                {"name": "n_strong_matches",  "type": "number"},
                {"name": "n_partial_matches", "type": "number"},
                {"name": "top_matches",       "type": "json"},
                {"name": "verdict",           "type": "text"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_meluhhan_names_expanded,
        ),
        AtomicNodeDef(
            id="IndusBlockerTargetedSA",
            name="Decode-Blocker Targeted SA (P168)",
            category="Indus Decipherment",
            description=(
                "Phase-168: GPU BigramScorer SA with all 161 H+M anchors pinned, targeted at "
                "the top 20 decode-blocking LOW signs from Phase-130. Tests whether SA converges "
                "to existing LOW readings or proposes alternatives. Computes updated coverage "
                "estimate. FINAL computationally-achievable experiment — ICIT corpus required "
                "to proceed further."
            ),
            inputs=[],
            outputs=[
                {"name": "n_blockers_tested",    "type": "number"},
                {"name": "n_converged_to_low",   "type": "number"},
                {"name": "n_diverged",           "type": "number"},
                {"name": "z_score",              "type": "number"},
                {"name": "new_coverage_estimate","type": "number"},
                {"name": "verdict",              "type": "text"},
                {"name": "blocker_results",      "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_blocker_targeted_sa,
        ),
    ]
