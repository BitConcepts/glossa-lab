"""Experiment Graph atomic nodes for Phases 134–141.

Registers Phase-134→141 research scripts as callable Experiment Builder nodes
under the 'Indus Falsification' palette category.

Nodes:
  IndusFalsificationSuite   — Phase-134 (F1, F3, F7, F9, F10, F12)
  IndusAdvancementAnalysis  — Phase-135 (site semantics, Meluhhan, stability, ceiling)
  IndusExtendedBattery      — Phase-136–140 (CV-skeleton, Zipf control, n-gram, TTR)
  IndusMasterScorecard      — Phase-141 (full evidence synthesis)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from glossa_lab.experiment_graph import AtomicNodeDef

_REPO      = Path(__file__).resolve().parent.parent.parent
_SCRIPTS   = _REPO / "backend" / "scripts"
_REPORTS   = _REPO / "backend" / "reports"
_ANCHORS   = _REPORTS / "INDUS_FINAL_ANCHORS.json"


def _run_phase_script(script_name: str, timeout: int = 900) -> dict[str, Any]:
    """Run a phase script and return the saved JSON report."""
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
    """Load a report JSON from backend/reports/."""
    path = _REPORTS / json_name
    if not path.exists():
        return {"available": False, "error": f"Report not found: {json_name}"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "error": str(exc)}


# ── F134: Falsification Suite ────────────────────────────────────────────────

def _falsification_suite(inputs: dict, params: dict) -> dict:
    """Run Phase-134 comprehensive falsification battery (F1, F3, F7, F9, F10, F12).

    Connects to BuiltinCorpus(indus_holdat).sequences for the corpus and
    reads INDUS_FINAL_ANCHORS.json automatically.
    Returns test verdicts and overall assessment.
    """
    # Try to load pre-computed results first
    report = _load_report("phase134_falsification_suite.json")
    if report.get("available") is False:
        # Run the script
        run_result = _run_phase_script("phase134_falsification_suite.py", timeout=900)
        if "error" in run_result:
            return {**run_result, "verdicts": {}, "overall": "ERROR"}
        report = _load_report("phase134_falsification_suite.json")

    verdicts = report.get("summary", {}).get("verdicts", {})
    overall  = report.get("summary", {}).get("overall_verdict", "UNKNOWN")
    f1       = report.get("test_results", {}).get("F1_permutation_null", {})
    f7       = report.get("test_results", {}).get("F7_blind_held_out", {})
    f12      = report.get("test_results", {}).get("F12_sanskrit_ab", {})

    return {
        "verdicts": verdicts,
        "overall_verdict": overall,
        "n_confirmed": report.get("summary", {}).get("n_confirmed", 0),
        "n_failed":    report.get("summary", {}).get("n_failed", 0),
        "f1_permutation_r2":  f1.get("observed_r2", 0),
        "f1_z_score":         f1.get("z_score", 0),
        "f1_p_value":         f1.get("p_value", 1.0),
        "f7_accuracy":        f7.get("class_prediction_accuracy", 0),
        "f7_pearson_r":       f7.get("mean_positional_correlation", 0),
        "f12_dravidian_pct":  f12.get("dravidian_favored_pct", 0),
        "f12_lm_advantage":   f12.get("lm_advantage_drv_minus_skt", 0),
        "json": {"verdicts": verdicts, "overall": overall},
        "number": f1.get("z_score", 0),
        "text": (
            f"Falsification overall: {overall}. "
            f"F1 z={f1.get('z_score',0):.1f} p={f1.get('p_value',1):.3f}; "
            f"F7 acc={f7.get('class_prediction_accuracy',0):.0%}; "
            f"F12 {f12.get('dravidian_favored_pct',0):.0f}% Dravidian."
        ),
    }


# ── F135: Advancement Analysis ────────────────────────────────────────────────

def _advancement_analysis(inputs: dict, params: dict) -> dict:
    """Run Phase-135 advancement analysis (site semantics, Meluhhan names,
    grammar stability, coverage ceiling)."""
    report = _load_report("phase135_advancement.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase135_advancement.py", timeout=300)
        if "error" in run_result:
            return {**run_result}
        report = _load_report("phase135_advancement.json")

    a = report.get("results", {}).get("A_site_semantic_clustering", {})
    b = report.get("results", {}).get("B_meluhhan_name_alignment", {})
    c = report.get("results", {}).get("C_grammar_slot_stability", {})
    d = report.get("results", {}).get("D_coverage_ceiling", {})
    findings = report.get("key_findings", [])

    return {
        "site_profiles": a.get("site_profiles", {}),
        "n_sites_profiled": len(a.get("site_profiles", {})),
        "kl_divergences": a.get("kl_divergences", {}),
        "meluhhan_plausible": b.get("n_plausible", 0),
        "meluhhan_total": b.get("n_names_tested", 0),
        "grammar_stability_mean": c.get("mean_stability", 0),
        "grammar_stable_pct": 100 * c.get("n_stable", 0) / max(c.get("n_signs_analyzed", 1), 1),
        "current_coverage": d.get("current_hm_token_coverage", 0),
        "promotion_scenarios": d.get("promotion_scenarios", []),
        "key_findings": findings,
        "json": {"site_profiles": a.get("site_profiles", {}), "meluhhan": b, "stability": c},
        "number": c.get("mean_stability", 0),
        "text": (
            f"Phase-135: {len(a.get('site_profiles',{}))} sites; "
            f"Meluhhan {b.get('n_plausible',0)}/{b.get('n_names_tested',0)} plausible; "
            f"Grammar {100*c.get('n_stable',0)/max(c.get('n_signs_analyzed',1),1):.0f}% stable."
        ),
    }


# ── F136-140: Extended Battery ────────────────────────────────────────────────

def _extended_battery(inputs: dict, params: dict) -> dict:
    """Run Phase-136→140 extended falsification + structural tests.

    F136 CV-skeleton phonological exclusivity; F137 Zipf control corpora;
    F138 CISI single-sign seal census; F139 Shu-ilishu; F140 n-gram/TTR.
    """
    report = _load_report("phase136_140_battery.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase136_140_battery.py", timeout=120)
        if "error" in run_result:
            return {**run_result}
        report = _load_report("phase136_140_battery.json")

    verdicts  = report.get("summary", {}).get("verdicts", {})
    n_pos     = report.get("summary", {}).get("n_positive", 0)
    results   = report.get("test_results", {})
    p136 = results.get("P136_F3_fix", {})
    p137 = results.get("P137_F10_fix", {})
    p140 = results.get("P140_structural", {})

    return {
        "verdicts": verdicts,
        "n_positive": n_pos,
        "f3_exclusivity_ratio": p136.get("exclusivity_ratio_drv_over_skt", 0),
        "f10_zipf_verdict": p137.get("verdict", "UNKNOWN"),
        "f10_indus_alpha": p137.get("indus_zipf_alpha", 0),
        "bigram_cond_entropy_ratio": p140.get("cond_entropy_ratio", 0),
        "ttr": p140.get("ttr", 0),
        "freq_pos_spearman_r": p140.get("freq_pos_spearman_r", 0),
        "json": {"verdicts": verdicts, "structural": p140},
        "number": float(n_pos),
        "text": (
            f"Extended battery: {n_pos}/{len(verdicts)} positive. "
            f"F3 Drv/Skt ratio={p136.get('exclusivity_ratio_drv_over_skt',0):.1f}x; "
            f"Bigram H(X2|X1)/H(X1)={p140.get('cond_entropy_ratio',0):.3f}; "
            f"TTR={p140.get('ttr',0):.4f}."
        ),
    }


# ── F141: Master Scorecard Synthesis ─────────────────────────────────────────

def _master_scorecard(inputs: dict, params: dict) -> dict:
    """Run Phase-141 master evidence synthesis across all phases.

    Produces a 4-category scorecard (STRUCTURAL, LINGUISTIC, EXTERNAL,
    DECIPHERMENT) with aggregate confidence score and open items.
    """
    report = _load_report("phase141_synthesis.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase141_synthesis.py", timeout=60)
        if "error" in run_result:
            return {**run_result}
        report = _load_report("phase141_synthesis.json")

    scorecard   = report.get("evidence_scorecard", [])
    agg_conf    = report.get("aggregate_confidence_pct", 0)
    ind_strong  = report.get("independent_strong_confirmations", 0)
    open_items  = report.get("open_items", [])
    headline    = report.get("headline_metrics", {})
    by_cat      = report.get("by_category_count", {})

    return {
        "aggregate_confidence_pct": agg_conf,
        "independent_strong_confirmations": ind_strong,
        "n_evidence_items": len(scorecard),
        "by_category": by_cat,
        "headline_metrics": headline,
        "open_items": open_items,
        "evidence_scorecard": scorecard,
        "json": {"scorecard": scorecard, "headline": headline, "open_items": open_items},
        "number": agg_conf,
        "text": (
            f"Phase-141 synthesis: {len(scorecard)} evidence items, "
            f"{agg_conf:.0f}% aggregate confidence, "
            f"{ind_strong} strongly-confirmed independent tests. "
            f"Open: {len(open_items)} items."
        ),
    }


# ── Node definitions ──────────────────────────────────────────────────────────

def _phase134_141_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            id="IndusFalsificationSuite",
            name="Falsification Suite (P134)",
            category="Indus Falsification",
            description=(
                "Run or load Phase-134 comprehensive falsification: F1 permutation null, "
                "F3 anchor exclusivity, F7 blind held-out, F9 single-sign census, "
                "F10 Zipf gap, F12 Sanskrit A/B."
            ),
            inputs=[],
            outputs=[
                {"name": "verdicts",          "type": "json"},
                {"name": "overall_verdict",   "type": "text"},
                {"name": "n_confirmed",        "type": "number"},
                {"name": "f1_z_score",         "type": "number"},
                {"name": "f7_accuracy",        "type": "number"},
                {"name": "f12_dravidian_pct",  "type": "number"},
                {"name": "json",               "type": "json"},
                {"name": "number",             "type": "number"},
                {"name": "text",               "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_falsification_suite,
        ),
        AtomicNodeDef(
            id="IndusAdvancementAnalysis",
            name="Advancement Analysis (P135)",
            category="Indus Falsification",
            description=(
                "Run or load Phase-135: site-stratified semantic clustering, "
                "Meluhhan name phonological alignment, grammar slot cross-site stability, "
                "coverage ceiling scenarios."
            ),
            inputs=[],
            outputs=[
                {"name": "n_sites_profiled",      "type": "number"},
                {"name": "meluhhan_plausible",     "type": "number"},
                {"name": "grammar_stability_mean", "type": "number"},
                {"name": "current_coverage",       "type": "number"},
                {"name": "key_findings",           "type": "json"},
                {"name": "site_profiles",          "type": "json"},
                {"name": "json",                   "type": "json"},
                {"name": "number",                 "type": "number"},
                {"name": "text",                   "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_advancement_analysis,
        ),
        AtomicNodeDef(
            id="IndusExtendedBattery",
            name="Extended Battery (P136-140)",
            category="Indus Falsification",
            description=(
                "Run or load Phase-136→140: F3 CV-skeleton phonological exclusivity, "
                "F10 Zipf control corpora, F9 CISI single-sign census, "
                "Shu-ilishu seal alignment, bigram conditional entropy + TTR."
            ),
            inputs=[],
            outputs=[
                {"name": "n_positive",                 "type": "number"},
                {"name": "f3_exclusivity_ratio",       "type": "number"},
                {"name": "bigram_cond_entropy_ratio",  "type": "number"},
                {"name": "ttr",                        "type": "number"},
                {"name": "freq_pos_spearman_r",        "type": "number"},
                {"name": "verdicts",                   "type": "json"},
                {"name": "json",                       "type": "json"},
                {"name": "number",                     "type": "number"},
                {"name": "text",                       "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_extended_battery,
        ),
        AtomicNodeDef(
            id="IndusMasterScorecard",
            name="Master Evidence Scorecard (P141)",
            category="Indus Falsification",
            description=(
                "Run or load Phase-141 full synthesis across Phases 1–140. "
                "Produces 23-item evidence scorecard in 4 categories "
                "(STRUCTURAL, LINGUISTIC, EXTERNAL, DECIPHERMENT), "
                "aggregate confidence %, and open items list."
            ),
            inputs=[],
            outputs=[
                {"name": "aggregate_confidence_pct",        "type": "number"},
                {"name": "independent_strong_confirmations", "type": "number"},
                {"name": "n_evidence_items",                "type": "number"},
                {"name": "headline_metrics",                "type": "json"},
                {"name": "evidence_scorecard",              "type": "json"},
                {"name": "open_items",                      "type": "json"},
                {"name": "json",                            "type": "json"},
                {"name": "number",                          "type": "number"},
                {"name": "text",                            "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_master_scorecard,
        ),
    ]
