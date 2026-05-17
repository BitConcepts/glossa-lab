"""Experiment Graph Nodes: Phase-56–61 Indus Script Decipherment Pipeline.

Registers 6 new Experiment Builder nodes covering the extended decipherment
pipeline from expanded Parpola crosswalk through phonotactic falsification:

  IndusParpola56Expansion   Phase-56: Full Parpola sign list → anchor expansion
  IndusExpandedSA           Phase-57: Constrained SA with 70+ pinned anchors
  IndusPhonologicalGap      Phase-58: Dravidian phonotactic gap analysis
  IndusFormulaPilot59       Phase-59: Full pilot readings for 50 inscriptions
  IndusContactDeep          Phase-60: Contact zone P-number deep mining
  IndusPhonotactic          Phase-61: Phonotactic falsification battery

MANDATORY: All nodes use GPU (torch.cuda) when available.
           GPU device is reported in all outputs.
           Created per H23 (5-step gate) BEFORE any Phase-56-61 script execution.

Port types used:
  decipherment_table  — list of {sign, reading, confidence} records
  anchor_set          — dict of anchor readings keyed by M-number
  phoneme_table       — Dravidian phonotactic analysis results
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

# AtomicNodeDef imported lazily inside _phase56_61_node_defs() to avoid circular import

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"
_DATA    = _REPO / "backend/glossa_lab/data"
_ANCHORS = _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"


def _get_device() -> str:
    """Return best available compute device; see glossa_lab.gpu_utils for behaviour."""
    from glossa_lab.gpu_utils import detect_device  # noqa: PLC0415
    return detect_device()


def _run_phase_script(script_name: str) -> dict[str, Any]:
    """Run a phase script and return its JSON report."""
    script = _SCRIPTS / script_name
    report_stem = script_name.replace(".py", "")
    report_path = _REPORTS / f"{report_stem}.json"

    if not script.exists():
        return {"error": f"Script not found: {script_name}"}

    try:
        r = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=900,
            cwd=str(_REPO),
        )
        if r.returncode != 0:
            return {
                "error": f"Script failed (exit {r.returncode})",
                "stderr": r.stderr[-500:],
                "stdout": r.stdout[-500:],
            }
    except subprocess.TimeoutExpired:
        return {"error": f"Script timed out after 900s: {script_name}"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}

    if report_path.exists():
        try:
            return json.loads(report_path.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True, "stdout": r.stdout[-200:]}


# ── Phase-56: Parpola Sign List Expansion ─────────────────────────────────────

def _parpola56_expansion(inputs: dict, params: dict) -> dict:
    """Expand ANCHORS from full Parpola sign list (EXTENDED_PARPOLA_MAP).
    Targets 40-60 new MEDIUM anchors via P→M→reading master crosswalk.
    GPU: torch for bigram consistency scoring of new candidates.
    """
    device = _get_device()
    result = _run_phase_script("phase56_parpola_expansion.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    n_new = result.get("n_new_anchors", 0)
    n_total = result.get("total_anchors", 0)
    return {
        "n_new_anchors": n_new,
        "total_anchors": n_total,
        "new_signs": result.get("new_signs", []),
        "expanded_map": result.get("expanded_map", {}),
        "json": result,
        "number": float(n_new),
        "text": (
            f"Phase-56: Parpola expansion complete. "
            f"{n_new} new anchors added. Total: {n_total}."
        ),
        "gpu_device": device,
    }


# ── Phase-57: Expanded Constrained SA ─────────────────────────────────────────

def _expanded_sa(inputs: dict, params: dict) -> dict:
    """Re-run constrained SA with 70+ pinned syllabic anchors.
    Expected z>20 and SA agreement >70% with expanded anchor set.
    GPU: BigramScorer CUDA. ~5 min on GPU.
    """
    device = _get_device()
    result = _run_phase_script("phase57_expanded_sa.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    # Load the full decipherment table produced by Phase-57
    table = []
    table_path = _REPORTS / "phase57_decipherment_table.json"
    if table_path.exists():
        try:
            table = json.loads(table_path.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass

    sa_res = result.get("results", {})
    cov = result.get("coverage", {})
    return {
        "decipherment_table": table,
        "n_signs": len(table),
        "z_score": sa_res.get("z_score", 0),
        "lift": sa_res.get("lift", 0),
        "n_pinned": result.get("n_pinned_anchors", 0),
        "sa_agreement_pct": (
            cov.get("sa_agrees_confirmed", 0) /
            max(cov.get("n_high", 0) + cov.get("n_medium", 0), 1)
        ),
        "json": result,
        "number": float(sa_res.get("z_score", 0)),
        "text": (
            f"Phase-57: Expanded SA complete. "
            f"z={sa_res.get('z_score', 0):.2f}, "
            f"{result.get('n_pinned_anchors', 0)} pinned anchors."
        ),
        "gpu_device": device,
    }


# ── Phase-58: Phonological Gap Analysis ────────────────────────────────────────

def _phonological_gap(inputs: dict, params: dict) -> dict:
    """Validate SA assignments against Dravidian phonotactic rules.
    Detects impossible consonant clusters, vowel harmony violations, gaps.
    GPU: torch for phoneme distribution matrix.
    """
    device = _get_device()
    result = _run_phase_script("phase58_phonological_gap.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    n_valid = result.get("n_valid", 0)
    n_invalid = result.get("n_invalid", 0)
    n_gap = result.get("n_gap", 0)
    total = n_valid + n_invalid + n_gap
    return {
        "n_valid": n_valid,
        "n_invalid": n_invalid,
        "n_gap": n_gap,
        "validity_rate": n_valid / max(total, 1),
        "impossible_assignments": result.get("impossible_assignments", []),
        "phoneme_gaps": result.get("phoneme_gaps", []),
        "json": result,
        "number": float(n_valid / max(total, 1)),
        "text": (
            f"Phase-58: Phonological gap analysis. "
            f"{n_valid} valid, {n_invalid} invalid, {n_gap} gaps. "
            f"Validity: {n_valid / max(total, 1):.1%}."
        ),
        "gpu_device": device,
    }


# ── Phase-59: Full Inscription Pilot Readings ──────────────────────────────────

def _formula_pilot59(inputs: dict, params: dict) -> dict:
    """Generate complete human-readable pilot translations for top-50 formulas.
    Uses Phase-57 decipherment table as source. Includes morphological parse
    and per-slot confidence.
    GPU: torch for formula clustering.
    """
    device = _get_device()
    result = _run_phase_script("phase59_pilot_readings.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    fully = result.get("fully_decoded", [])
    top = result.get("top_readings", [])
    return {
        "fully_decoded_formulas": fully,
        "n_fully_decoded": len(fully),
        "top_readings": top[:10],
        "n_top_readings": len(top),
        "n_unique_formulas": result.get("n_unique_formulas", 0),
        "json": result,
        "number": float(len(fully)),
        "text": (
            f"Phase-59: Pilot readings complete. "
            f"{len(fully)} formulas ≥80% decoded from {len(top)} top formulas. "
            f"Sample: {fully[0].get('morphological', 'none') if fully else 'none'}"
        ),
        "gpu_device": device,
    }


# ── Phase-60: Contact Zone Deep Mining ─────────────────────────────────────────

def _contact_deep(inputs: dict, params: dict) -> dict:
    """Deep mine publications using Parpola sign NUMBER patterns (not M-numbers).
    Targets 10-20 additional readings from Parpola 1994/2010 analyses.
    GPU: torch for pattern scoring.
    """
    device = _get_device()
    result = _run_phase_script("phase60_contact_deep.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    n_found = result.get("n_new_readings", 0)
    return {
        "n_new_readings": n_found,
        "new_readings": result.get("new_readings", []),
        "pattern_matches": result.get("pattern_matches", []),
        "sources_mined": result.get("sources_mined", []),
        "json": result,
        "number": float(n_found),
        "text": (
            f"Phase-60: Contact zone deep mining complete. "
            f"{n_found} new readings found. "
            f"Sources: {result.get('sources_mined', [])}."
        ),
        "gpu_device": device,
    }


# ── Phase-61: Phonotactic Falsification Battery ────────────────────────────────

def _phonotactic_falsification(inputs: dict, params: dict) -> dict:
    """Test all assigned phoneme values against Dravidian phonotactic constraints.
    Chi-squared on phoneme distribution, gap analysis, impossible sequence detection.
    Vowel harmony validity check.
    GPU: torch for co-occurrence matrix and chi-squared computation.
    """
    device = _get_device()
    result = _run_phase_script("phase61_phonotactic.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    n_pass = result.get("n_pass", 0)
    n_fail = result.get("n_fail", 0)
    n_warn = result.get("n_warn", 0)
    total  = n_pass + n_fail + n_warn
    chi2_p = result.get("chi2_p_value", 1.0)
    return {
        "n_pass": n_pass,
        "n_fail": n_fail,
        "n_warn": n_warn,
        "pass_rate": n_pass / max(total, 1),
        "chi2_p_value": chi2_p,
        "impossible_sequences": result.get("impossible_sequences", []),
        "vowel_harmony_valid": result.get("vowel_harmony_valid", False),
        "phoneme_distribution": result.get("phoneme_distribution", {}),
        "json": result,
        "number": float(n_pass / max(total, 1)),
        "text": (
            f"Phase-61: Phonotactic falsification. "
            f"{n_pass} PASS, {n_fail} FAIL, {n_warn} WARN. "
            f"chi2 p={chi2_p:.4f}. Vowel harmony: {result.get('vowel_harmony_valid', False)}."
        ),
        "gpu_device": device,
    }


# ── Node definitions ─────────────────────────────────────────────────────────

def _phase56_61_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415
    return [
        AtomicNodeDef(
            id="IndusParpola56Expansion",
            name="Parpola Sign List Expansion",
            category="Indus Decipherment",
            description=(
                "Phase-56: Expand INDUS_FINAL_ANCHORS using the full Parpola sign list "
                "via an EXTENDED_PARPOLA_MAP (P→M→reading master crosswalk). "
                "Targets 40-60 new MEDIUM-confidence anchors covering numerical signs, "
                "animal classifiers, tools, and abstract signs. "
                "GPU: torch for bigram consistency scoring."
            ),
            inputs=[],
            outputs=[
                {"name": "n_new_anchors",  "type": "number", "description": "New anchors added"},
                {"name": "total_anchors",  "type": "number"},
                {"name": "new_signs",      "type": "json",   "description": "List of newly anchored sign IDs"},
                {"name": "expanded_map",   "type": "json",   "description": "Full P→M→reading crosswalk"},
                {"name": "gpu_device",     "type": "text"},
                {"name": "text",           "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_parpola56_expansion,
        ),
        AtomicNodeDef(
            id="IndusExpandedSA",
            name="Expanded Constrained SA (70+ anchors)",
            category="Indus Decipherment",
            description=(
                "Phase-57: Re-run constrained Simulated Annealing with all 70+ "
                "Phase-56-expanded anchors pinned as hard constraints. "
                "Expected z>20 and SA agreement >70%. Produces phase57_decipherment_table.json "
                "used by Phase-59 and Phase-61. "
                "GPU: BigramScorer CUDA. ~5 min. "
                "REQUIRES: IndusParpola56Expansion must run first."
            ),
            inputs=[],
            outputs=[
                {"name": "decipherment_table", "type": "json",   "description": "Full decipherment table (390+ signs)"},
                {"name": "n_signs",            "type": "number"},
                {"name": "z_score",            "type": "number"},
                {"name": "lift",               "type": "number"},
                {"name": "n_pinned",           "type": "number", "description": "Number of pinned anchors"},
                {"name": "sa_agreement_pct",   "type": "number"},
                {"name": "gpu_device",         "type": "text"},
                {"name": "text",               "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_expanded_sa,
        ),
        AtomicNodeDef(
            id="IndusPhonologicalGap",
            name="Phonological Gap Analyser",
            category="Indus Decipherment",
            description=(
                "Phase-58: Validate all SA assignments against Dravidian phonotactic rules. "
                "Detects impossible consonant clusters, vowel harmony violations, "
                "and gaps in the syllabic inventory. "
                "GPU: torch for phoneme distribution matrix. "
                "REQUIRES: IndusExpandedSA must run first."
            ),
            inputs=[],
            outputs=[
                {"name": "n_valid",                "type": "number"},
                {"name": "n_invalid",              "type": "number"},
                {"name": "n_gap",                  "type": "number"},
                {"name": "validity_rate",          "type": "number"},
                {"name": "impossible_assignments", "type": "json"},
                {"name": "phoneme_gaps",           "type": "json"},
                {"name": "gpu_device",             "type": "text"},
                {"name": "text",                   "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phonological_gap,
        ),
        AtomicNodeDef(
            id="IndusFormulaPilot59",
            name="Full Inscription Pilot Reader",
            category="Indus Decipherment",
            description=(
                "Phase-59: Generate complete human-readable candidate translations for "
                "the top-50 most frequent inscription formulas. Uses Phase-57 decipherment "
                "table. Includes per-slot confidence and morphological parse. "
                "GPU: torch for formula clustering. "
                "REQUIRES: IndusExpandedSA must run first (uses phase57_decipherment_table.json)."
            ),
            inputs=[],
            outputs=[
                {"name": "fully_decoded_formulas", "type": "json",   "description": "Formulas ≥80% decoded"},
                {"name": "n_fully_decoded",         "type": "number"},
                {"name": "top_readings",            "type": "json"},
                {"name": "n_top_readings",          "type": "number"},
                {"name": "gpu_device",              "type": "text"},
                {"name": "text",                    "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_formula_pilot59,
        ),
        AtomicNodeDef(
            id="IndusContactDeep",
            name="Contact Zone Deep Miner",
            category="Indus Decipherment",
            description=(
                "Phase-60: Deep-mine Parpola and contact-zone publications using "
                "Parpola sign NUMBER patterns (P-number regex) rather than M-numbers. "
                "Expected to yield 10-20 additional readings from Parpola 1994/2010. "
                "GPU: torch for pattern scoring. "
                "Runs independently of Phase-57/58/59."
            ),
            inputs=[],
            outputs=[
                {"name": "n_new_readings",  "type": "number"},
                {"name": "new_readings",    "type": "json"},
                {"name": "pattern_matches", "type": "json"},
                {"name": "sources_mined",   "type": "json"},
                {"name": "gpu_device",      "type": "text"},
                {"name": "text",            "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_contact_deep,
        ),
        AtomicNodeDef(
            id="IndusPhonotactic",
            name="Phonotactic Falsification Battery",
            category="Indus Decipherment",
            description=(
                "Phase-61: Test all assigned phoneme values against the full set of "
                "Dravidian phonotactic constraints. Runs chi-squared test on phoneme "
                "distribution, gap analysis, impossible sequence detection, and vowel "
                "harmony validity check. "
                "GPU: torch for co-occurrence matrix and chi-squared. "
                "REQUIRES: IndusExpandedSA must run first."
            ),
            inputs=[],
            outputs=[
                {"name": "n_pass",                "type": "number"},
                {"name": "n_fail",                "type": "number"},
                {"name": "n_warn",                "type": "number"},
                {"name": "pass_rate",             "type": "number"},
                {"name": "chi2_p_value",          "type": "number"},
                {"name": "impossible_sequences",  "type": "json"},
                {"name": "vowel_harmony_valid",   "type": "number", "description": "1 if valid"},
                {"name": "phoneme_distribution",  "type": "json"},
                {"name": "gpu_device",            "type": "text"},
                {"name": "text",                  "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phonotactic_falsification,
        ),
    ]
