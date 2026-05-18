"""Experiment Graph Nodes: Phase-67–73 Indus Decipherment Pipeline.

  IndusM267Validation       Phase-70: M267=in vs col SA validation
  IndusFormulaTranslation   Phase-68: Full formula translation with linguistic annotation
  IndusSanskritNorm         Phase-67: Sanskrit LM normalisation (proper z-comparison)
  IndusEnsembleCalibration  Phase-73: Ensemble calibration (10 seeds, 2-char agreement)
  IndusSiteStratification   Phase-69: Multi-site positional grammar stratification
  IndusCrosswalkComplete    Phase-71: M<->P crosswalk top-47 completion
  IndusParpolarParser       Phase-72: Parpola notation-specific publication parser

MANDATORY: Created per H23 (5-step gate) BEFORE any Phase-67-73 script execution.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"
_ANCHORS = _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"


def _get_device() -> str:
    from glossa_lab.gpu_utils import detect_device  # noqa: PLC0415
    return detect_device()


def _run_phase_script(script_name: str) -> dict[str, Any]:
    script = _SCRIPTS / script_name
    report_stem = script_name.replace(".py", "")
    report_path = _REPORTS / f"{report_stem}.json"
    if not script.exists():
        return {"error": f"Script not found: {script_name}"}
    try:
        r = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=1200,
            cwd=str(_REPO),
        )
        if r.returncode != 0:
            return {"error": f"Script failed (exit {r.returncode})",
                    "stderr": r.stderr[-500:], "stdout": r.stdout[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Timed out after 1200s: {script_name}"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}
    if report_path.exists():
        try:
            return json.loads(report_path.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True, "stdout": r.stdout[-200:]}


# ── Phase-70: M267 Validation ────────────────────────────────────────────────

def _m267_validation(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase70_m267_validation.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    winner = result.get("winner", "?")
    z_in   = result.get("z_in", 0)
    z_col  = result.get("z_col", 0)
    z_base = result.get("z_baseline", 0)
    return {
        "winner":      winner,
        "z_in":        z_in,
        "z_col":       z_col,
        "z_baseline":  z_base,
        "promoted":    result.get("m267_promoted", False),
        "json":        result,
        "number":      float(z_in),
        "text":  f"Phase-70: M267 winner={winner}. z_in={z_in:.2f} z_col={z_col:.2f} baseline={z_base:.2f}.",
        "gpu_device": device,
    }


# ── Phase-68: Formula Translation ────────────────────────────────────────────

def _formula_translation(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase68_formula_translation.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    n_glossed = result.get("n_glossed", 0)
    return {
        "n_glossed":       n_glossed,
        "translations":    result.get("translations", []),
        "formula_types":   result.get("formula_types", {}),
        "json":            result,
        "number":          float(n_glossed),
        "text":  f"Phase-68: {n_glossed} formulas fully glossed with DEDR citations.",
        "gpu_device": device,
    }


# ── Phase-67: Sanskrit LM Normalisation ──────────────────────────────────────

def _sanskrit_norm(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase67_sanskrit_norm.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    lift_d = result.get("dravidian_lift_pct", 0)
    lift_s = result.get("sanskrit_lift_pct", 0)
    ratio  = result.get("lift_ratio", 0)
    verdict = result.get("verdict", "?")
    return {
        "dravidian_lift_pct": lift_d,
        "sanskrit_lift_pct":  lift_s,
        "lift_ratio":         ratio,
        "verdict":            verdict,
        "json":               result,
        "number":             float(ratio),
        "text":  f"Phase-67: Dravidian {lift_d:.1f}% vs Sanskrit {lift_s:.1f}% lift. Ratio={ratio:.2f}x. {verdict}.",
        "gpu_device": device,
    }


# ── Phase-73: Ensemble Calibration ───────────────────────────────────────────

def _ensemble_calibration(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase73_ensemble_calibration.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    n_high = result.get("n_ensemble_high", 0)
    n_med  = result.get("n_ensemble_medium", 0)
    return {
        "n_ensemble_high":   n_high,
        "n_ensemble_medium": n_med,
        "calibrated_table":  result.get("calibrated_table", []),
        "json":              result,
        "number":            float(n_high),
        "text":  f"Phase-73: Calibrated ensemble. ENSEMBLE_HIGH={n_high}, MEDIUM={n_med}.",
        "gpu_device": device,
    }


# ── Phase-69: Site Stratification ────────────────────────────────────────────

def _site_stratification(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase69_site_stratification.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    verdict = result.get("verdict", "?")
    chi2_p  = result.get("chi2_p_value", 1.0)
    return {
        "verdict":       verdict,
        "chi2_p_value":  chi2_p,
        "site_profiles": result.get("site_profiles", {}),
        "invariant_signs": result.get("invariant_signs", []),
        "json":          result,
        "number":        float(chi2_p),
        "text":  f"Phase-69: Site stratification verdict={verdict}. chi2 p={chi2_p:.4f}.",
        "gpu_device": device,
    }


# ── Phase-71: Crosswalk Completion ───────────────────────────────────────────

def _crosswalk_complete(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase71_crosswalk_complete.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    n_new  = result.get("n_newly_mapped", 0)
    total  = result.get("total_mp_mapped", 0)
    cov    = result.get("corpus_coverage_pct", 0)
    return {
        "n_newly_mapped":   n_new,
        "total_mp_mapped":  total,
        "corpus_coverage_pct": cov,
        "new_mappings":     result.get("new_mappings", []),
        "json":             result,
        "number":           float(total),
        "text":  f"Phase-71: +{n_new} new M<->P mappings. Total={total}/390, coverage={cov:.1f}%.",
        "gpu_device": device,
    }


# ── Phase-72: Parpola Parser ──────────────────────────────────────────────────

def _parpola_parser(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase72_parpola_parser.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    n_found = result.get("n_new_readings", 0)
    return {
        "n_new_readings":  n_found,
        "new_readings":    result.get("new_readings", []),
        "parser_quality":  result.get("parser_quality", {}),
        "json":            result,
        "number":          float(n_found),
        "text":  f"Phase-72: Parpola parser found {n_found} new readings from publications.",
        "gpu_device": device,
    }


# ── Node definitions ─────────────────────────────────────────────────────────

def _phase67_73_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415
    return [
        AtomicNodeDef(
            id="IndusM267Validation",
            name="M267 Genitive Validation",
            category="Indus Decipherment",
            description=(
                "Phase-70: Test the Phase-64 conclusion that M267=in (genitive 'of'). "
                "Pins M267 to 'in' and re-runs Phase-63 phonotactic-filtered SA. "
                "Also tests M267='col' as alternative. If z improves with 'in' -> "
                "promotes M267 to HIGH confidence anchor. GPU: BigramScorer ~5 min."
            ),
            inputs=[],
            outputs=[
                {"name": "winner",      "type": "text",   "description": "in or col or baseline"},
                {"name": "z_in",        "type": "number"},
                {"name": "z_col",       "type": "number"},
                {"name": "z_baseline",  "type": "number"},
                {"name": "promoted",    "type": "number", "description": "1 if M267 promoted to HIGH"},
                {"name": "gpu_device",  "type": "text"},
                {"name": "text",        "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_m267_validation,
        ),
        AtomicNodeDef(
            id="IndusFormulaTranslation",
            name="Full Formula Translation Pilot",
            category="Indus Decipherment",
            description=(
                "Phase-68: Produce complete Dravidian linguistic annotations for the "
                "22 formulas decoded at >=80% in Phase-59. "
                "For each slot: morphological role (ROOT/SUFFIX/CLASSIFIER/GENITIVE), "
                "DEDR citation, and semantic interpretation (title/ownership/trade formula). "
                "No GPU required — pure linguistic analysis."
            ),
            inputs=[],
            outputs=[
                {"name": "n_glossed",     "type": "number"},
                {"name": "translations",  "type": "json"},
                {"name": "formula_types", "type": "json"},
                {"name": "gpu_device",    "type": "text"},
                {"name": "text",          "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_formula_translation,
        ),
        AtomicNodeDef(
            id="IndusSanskritNorm",
            name="Sanskrit LM Normalisation",
            category="Indus Decipherment",
            description=(
                "Phase-67: Fix Phase-66 methodological flaw. Build a Sanskrit LM "
                "at the same ~15k bigram density as the Dravidian syllabic LM, "
                "then run SA under both against the SAME null distribution. "
                "Produces a valid lift-ratio comparison (the definitive falsification). "
                "GPU: BigramScorer ~10 min."
            ),
            inputs=[],
            outputs=[
                {"name": "dravidian_lift_pct", "type": "number"},
                {"name": "sanskrit_lift_pct",  "type": "number"},
                {"name": "lift_ratio",         "type": "number"},
                {"name": "verdict",            "type": "text"},
                {"name": "gpu_device",         "type": "text"},
                {"name": "text",               "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_sanskrit_norm,
        ),
        AtomicNodeDef(
            id="IndusEnsembleCalibration",
            name="Ensemble Calibration",
            category="Indus Decipherment",
            description=(
                "Phase-73: Fix Phase-62a ENSEMBLE_HIGH=2 by calibrating the consensus method. "
                "Runs 10 seeds per LM (vs 3), uses first-2-char agreement (vs exact match), "
                "and weights by corpus frequency. Expected ENSEMBLE_HIGH ~15-25. "
                "GPU: BigramScorer CUDA ~15 min."
            ),
            inputs=[],
            outputs=[
                {"name": "n_ensemble_high",   "type": "number"},
                {"name": "n_ensemble_medium", "type": "number"},
                {"name": "calibrated_table",  "type": "json"},
                {"name": "gpu_device",        "type": "text"},
                {"name": "text",              "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_ensemble_calibration,
        ),
        AtomicNodeDef(
            id="IndusSiteStratification",
            name="Multi-Site Stratification",
            category="Indus Decipherment",
            description=(
                "Phase-69: Test whether the positional grammar (I/M/T rates) of anchor "
                "signs is site-invariant across all 9 Holdat sites. "
                "Chi-squared test per sign across sites. If grammar is invariant -> "
                "strong evidence for pan-Indus writing system (not local scripts). "
                "GPU: torch for frequency matrices."
            ),
            inputs=[],
            outputs=[
                {"name": "verdict",          "type": "text"},
                {"name": "chi2_p_value",     "type": "number"},
                {"name": "site_profiles",    "type": "json"},
                {"name": "invariant_signs",  "type": "json"},
                {"name": "gpu_device",       "type": "text"},
                {"name": "text",             "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_site_stratification,
        ),
        AtomicNodeDef(
            id="IndusCrosswalkComplete",
            name="M<->P Crosswalk Completion",
            category="Indus Decipherment",
            description=(
                "Phase-71: Map the 47 remaining top-100 M-signs to Parpola P-numbers "
                "using Wells 2015 ICIT sign list, Mahadevan 1977 concordance index, "
                "and Parpola 1994 Appendix B. "
                "Target: 90%+ corpus token coverage (currently 76.4%)."
            ),
            inputs=[],
            outputs=[
                {"name": "n_newly_mapped",      "type": "number"},
                {"name": "total_mp_mapped",     "type": "number"},
                {"name": "corpus_coverage_pct", "type": "number"},
                {"name": "new_mappings",        "type": "json"},
                {"name": "gpu_device",          "type": "text"},
                {"name": "text",                "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_crosswalk_complete,
        ),
        AtomicNodeDef(
            id="IndusParpolarParser",
            name="Parpola Notation Parser",
            category="Indus Decipherment",
            description=(
                "Phase-72: Build a sign-list-aware extractor for Parpola 1994/2010 "
                "publication notation. Handles: '(47)', 'Sign 47', '*miin', "
                "footnote references, and Parpola's apparatus style — "
                "all forms that Phase-60/60b regex could not match. "
                "Tests on parpola_2010_dravidian_solution.txt (472 parpola-keyword hits)."
            ),
            inputs=[],
            outputs=[
                {"name": "n_new_readings",  "type": "number"},
                {"name": "new_readings",    "type": "json"},
                {"name": "parser_quality",  "type": "json"},
                {"name": "gpu_device",      "type": "text"},
                {"name": "text",            "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_parpola_parser,
        ),
    ]
