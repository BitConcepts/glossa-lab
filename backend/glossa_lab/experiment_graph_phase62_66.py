"""Experiment Graph Nodes: Phase-62–66 Indus Script Decipherment Pipeline.

  IndusEnsembleFix        Phase-62a: Fix Phase-55 token-granularity mismatch
  IndusContactInvestigate Phase-60b: Contact zone deep re-investigation
  IndusFilteredSA         Phase-63:  Phonotactic-filtered SA re-run
  IndusMorphBoundary      Phase-64:  Morphological boundary + M267 resolution
  IndusCrosswalkTop100    Phase-65:  M-to-P crosswalk top-100 by frequency
  IndusSanskritSA         Phase-66:  Sanskrit SA falsification (competing hypothesis)

MANDATORY: Created per H23 before any Phase-62-66 script execution.
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


# ── Phase-62a: Ensemble Fix ──────────────────────────────────────────────────

def _ensemble_fix(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase62_ensemble_fix.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    n_high = result.get("n_ensemble_high", 0)
    n_med  = result.get("n_ensemble_medium", 0)
    return {
        "n_ensemble_high":   n_high,
        "n_ensemble_medium": n_med,
        "fixed_table":       result.get("fixed_table", []),
        "json":              result,
        "number":            float(n_high),
        "text": f"Phase-62a: Ensemble fixed. ENSEMBLE_HIGH={n_high}, MEDIUM={n_med}.",
        "gpu_device": device,
    }


# ── Phase-60b: Contact Zone Re-Investigation ─────────────────────────────────

def _contact_investigate(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase60b_contact_investigation.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    n_found = result.get("n_new_readings", 0)
    return {
        "n_new_readings":   n_found,
        "new_readings":     result.get("new_readings", []),
        "pub_quality":      result.get("pub_quality", {}),
        "recommendation":   result.get("recommendation", ""),
        "json":             result,
        "number":           float(n_found),
        "text": (f"Phase-60b: Contact investigation. "
                 f"{n_found} readings found. {result.get('recommendation','')}"),
        "gpu_device": device,
    }


# ── Phase-63: Phonotactic Filtered SA ────────────────────────────────────────

def _filtered_sa(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase63_filtered_sa.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    z63 = result.get("z_score", 0)
    return {
        "z_score":           z63,
        "n_pinned":          result.get("n_pinned", 0),
        "n_vocab_filtered":  result.get("n_vocab_filtered", 0),
        "sa_agreement_pct":  result.get("sa_agreement_pct", 0),
        "decipherment_table":result.get("decipherment_table", []),
        "json":              result,
        "number":            float(z63),
        "text": (f"Phase-63: Phonotactic-filtered SA. z={z63:.2f}, "
                 f"{result.get('n_vocab_filtered',0)} invalid initials removed."),
        "gpu_device": device,
    }


# ── Phase-64: Morphological Boundary + M267 ──────────────────────────────────

def _morph_boundary(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase64_morphological_boundary.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    m267_top = result.get("m267_top_candidate", "?")
    n_boundaries = result.get("n_boundaries_detected", 0)
    return {
        "m267_top_candidate":   m267_top,
        "m267_candidates":      result.get("m267_candidates", []),
        "n_boundaries_detected":n_boundaries,
        "boundary_map":         result.get("boundary_map", {}),
        "json":                 result,
        "number":               float(n_boundaries),
        "text": (f"Phase-64: Morphological boundary. M267 top candidate: {m267_top}. "
                 f"{n_boundaries} boundaries detected in top formulas."),
        "gpu_device": device,
    }


# ── Phase-65: M-to-P Crosswalk Top-100 ───────────────────────────────────────

def _crosswalk_top100(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase65_crosswalk_top100.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    n_mapped = result.get("n_newly_mapped", 0)
    total_mp = result.get("total_mp_mapped", 0)
    return {
        "n_newly_mapped":   n_mapped,
        "total_mp_mapped":  total_mp,
        "coverage_pct":     result.get("corpus_coverage_pct", 0),
        "crosswalk_table":  result.get("crosswalk_table", []),
        "json":             result,
        "number":           float(total_mp),
        "text": (f"Phase-65: M↔P crosswalk top-100. "
                 f"+{n_mapped} new mappings, {total_mp} total. "
                 f"Coverage: {result.get('corpus_coverage_pct',0):.1f}%."),
        "gpu_device": device,
    }


# ── Phase-66: Sanskrit SA Falsification ──────────────────────────────────────

def _sanskrit_sa(inputs: dict, params: dict) -> dict:
    device = _get_device()
    result = _run_phase_script("phase66_sanskrit_sa.py")
    if "error" in result:
        return {**result, "gpu_device": device}
    z_skt = result.get("z_score_sanskrit", 0)
    z_drav = result.get("z_score_dravidian_ref", 0)
    ratio = result.get("z_ratio_dravidian_vs_sanskrit", 0)
    return {
        "z_score_sanskrit":               z_skt,
        "z_score_dravidian_ref":          z_drav,
        "z_ratio_dravidian_vs_sanskrit":  ratio,
        "verdict":                        result.get("verdict", "?"),
        "json":                           result,
        "number":                         float(ratio),
        "text": (f"Phase-66: Sanskrit falsification. "
                 f"Dravidian z={z_drav:.2f} vs Sanskrit z={z_skt:.2f}. "
                 f"Ratio={ratio:.2f}×. Verdict: {result.get('verdict','?')}."),
        "gpu_device": device,
    }


# ── Node definitions ─────────────────────────────────────────────────────────

def _phase62_66_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415
    return [
        AtomicNodeDef(
            id="IndusEnsembleFix",
            name="Ensemble Fix (token normalisation)",
            category="Indus Decipherment",
            description=(
                "Phase-62a: Fix Phase-55 token-granularity mismatch. "
                "Tamil_char LM uses Unicode characters; syllabic LMs use romanized syllables — "
                "they could never agree. Fix: use only Tamil_syllabic + Proto_Dravidian + Sanskrit "
                "for consensus. ENSEMBLE_HIGH = syllabic agrees with ProtoD, Sanskrit differs. "
                "Upgrades from DO NOT CLAIM → VERIFIED."
            ),
            inputs=[],
            outputs=[
                {"name": "n_ensemble_high",   "type": "number"},
                {"name": "n_ensemble_medium", "type": "number"},
                {"name": "fixed_table",       "type": "json"},
                {"name": "gpu_device",        "type": "text"},
                {"name": "text",              "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_ensemble_fix,
        ),
        AtomicNodeDef(
            id="IndusContactInvestigate",
            name="Contact Zone Re-Investigation",
            category="Indus Decipherment",
            description=(
                "Phase-60b: Re-investigate the Phase-60 contact zone mining (0 hits). "
                "Check OCR quality of publications, try broader regex patterns without "
                "requiring quotation marks, scan for any Parpola P-number context."
            ),
            inputs=[],
            outputs=[
                {"name": "n_new_readings",  "type": "number"},
                {"name": "new_readings",    "type": "json"},
                {"name": "pub_quality",     "type": "json"},
                {"name": "recommendation",  "type": "text"},
                {"name": "gpu_device",      "type": "text"},
                {"name": "text",            "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_contact_investigate,
        ),
        AtomicNodeDef(
            id="IndusFilteredSA",
            name="Phonotactic Filtered SA",
            category="Indus Decipherment",
            description=(
                "Phase-63: Re-run Phase-57 constrained SA with a phonotactic filter. "
                "Filter removes Proto-Dravidian-invalid initials (voiced stops b/d/g/f/w/x/q) "
                "from the SA target vocabulary. Expected z > 19.07 and fewer invalid assignments. "
                "GPU: BigramScorer CUDA. ~5 min."
            ),
            inputs=[],
            outputs=[
                {"name": "z_score",           "type": "number"},
                {"name": "n_pinned",          "type": "number"},
                {"name": "n_vocab_filtered",  "type": "number"},
                {"name": "sa_agreement_pct",  "type": "number"},
                {"name": "decipherment_table","type": "json"},
                {"name": "gpu_device",        "type": "text"},
                {"name": "text",              "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_filtered_sa,
        ),
        AtomicNodeDef(
            id="IndusMorphBoundary",
            name="Morphological Boundary + M267 Resolution",
            category="Indus Decipherment",
            description=(
                "Phase-64: Use positional entropy to locate morpheme boundaries in multi-sign "
                "formulas. Separate case markers (M342=āy, M176=an, M367=am) from root syllables. "
                "Analyse M267 position distribution to narrow candidates from 4 (col/iṉ/um/ē) "
                "to 1-2 using grammar constraints."
            ),
            inputs=[],
            outputs=[
                {"name": "m267_top_candidate",    "type": "text"},
                {"name": "m267_candidates",       "type": "json"},
                {"name": "n_boundaries_detected", "type": "number"},
                {"name": "boundary_map",          "type": "json"},
                {"name": "gpu_device",            "type": "text"},
                {"name": "text",                  "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_morph_boundary,
        ),
        AtomicNodeDef(
            id="IndusCrosswalkTop100",
            name="M↔P Crosswalk Top-100",
            category="Indus Decipherment",
            description=(
                "Phase-65: Map the top-100 most frequent M-signs to Parpola P-numbers. "
                "Currently only 45/390 M-signs are mapped. Top-100 by corpus frequency "
                "covers ~85% of tokens. Uses Phase-56 master + Phase-51 + DEDR catalogue."
            ),
            inputs=[],
            outputs=[
                {"name": "n_newly_mapped",  "type": "number"},
                {"name": "total_mp_mapped", "type": "number"},
                {"name": "coverage_pct",    "type": "number"},
                {"name": "crosswalk_table", "type": "json"},
                {"name": "gpu_device",      "type": "text"},
                {"name": "text",            "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_crosswalk_top100,
        ),
        AtomicNodeDef(
            id="IndusSanskritSA",
            name="Sanskrit SA Falsification",
            category="Indus Decipherment",
            description=(
                "Phase-66: Run the same phonotactic-filtered constrained SA (Phase-63) "
                "but targeting the Sanskrit syllable LM instead of Dravidian. "
                "Computes Dravidian z / Sanskrit z ratio — the key quantitative falsification. "
                "If Dravidian z >> Sanskrit z, the Dravidian hypothesis is statistically preferred. "
                "GPU: BigramScorer CUDA. ~5 min."
            ),
            inputs=[],
            outputs=[
                {"name": "z_score_sanskrit",              "type": "number"},
                {"name": "z_score_dravidian_ref",         "type": "number"},
                {"name": "z_ratio_dravidian_vs_sanskrit", "type": "number"},
                {"name": "verdict",                       "type": "text"},
                {"name": "gpu_device",                    "type": "text"},
                {"name": "text",                          "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_sanskrit_sa,
        ),
    ]
