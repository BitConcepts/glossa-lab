"""Experiment Graph Nodes: Phase-48–55 Indus Script Decipherment Pipeline.

Registers 8 new Experiment Builder nodes covering the full decipherment
pipeline from MEDIUM anchor validation through multi-LM ensemble:

  IndusMediumValidator      Phase-48: Validate MEDIUM anchors → promote to HIGH
  IndusSyllabicLMBuilder    Phase-49: Build syllabic Tamil LM from TamilTB + DEDR
  IndusDEDRCatalogue        Phase-50: Map sign depictions → DEDR etymologies → rebus
  IndusParpola Importer     Phase-51: Import Parpola 1994 sign readings into anchors
  IndusConstrainedSA        Phase-52: Constrained SA with syllabic LM + all anchors
  IndusFormulaPilot         Phase-53: Decode top-50 inscription formulas
  IndusFalsificationBattery Phase-54: Falsify per-sign reading predictions
  IndusEnsembleDecipher     Phase-55: Multi-LM ensemble for confidence stratification

MANDATORY: All nodes use GPU (torch.cuda) when available.
           GPU device is reported in all outputs.

Port types used:
  decipherment_table  — list of {sign, reading, confidence} records
  anchor_set          — dict of anchor readings keyed by M-number
  syllabic_lm         — serialised syllabic bigram LM
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

# AtomicNodeDef imported lazily inside _phase48_55_node_defs() to avoid circular import

_REPO = Path(__file__).resolve().parent.parent.parent
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


# ── Phase-48: MEDIUM Anchor Validator ────────────────────────────────────────

def _medium_validator(inputs: dict, params: dict) -> dict:
    """Validate MEDIUM anchors against 3 tests; promote passing signs to HIGH.
    GPU: torch for bigram consistency matrix.
    """
    device = _get_device()
    result = _run_phase_script("phase48_medium_validation.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    promoted = result.get("promoted_signs", [])
    n = result.get("n_promoted", 0)
    cov = result.get("new_total_high_coverage_pct", 0)

    return {
        "promoted_signs": promoted,
        "n_promoted": n,
        "coverage_pct": cov,
        "results": result.get("results", []),
        "json": result,
        "number": float(n),
        "text": (
            f"Phase-48: Promoted {n} MEDIUM signs to HIGH. "
            f"Total HIGH coverage: {cov:.1f}%. Signs: {promoted[:5]}…"
        ),
        "gpu_device": device,
    }


# ── Phase-49: Syllabic LM Builder ────────────────────────────────────────────

def _syllabic_lm_builder(inputs: dict, params: dict) -> dict:
    """Build Tamil syllabic bigram LM from TamilTB + DEDR + anchor readings.
    GPU: torch for LM probability matrix.
    """
    device = _get_device()
    result = _run_phase_script("phase49_syllabic_lm.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    lm_path = _DATA / "dravidian_syllabic_lm.json"
    lm_exists = lm_path.exists()

    return {
        "n_syllables": result.get("n_syllables", 0),
        "n_bigrams": result.get("n_bigrams", 0),
        "top_syllables": result.get("top_syllables", []),
        "lm_path": str(lm_path) if lm_exists else "",
        "lm_built": lm_exists,
        "json": result,
        "number": float(result.get("n_bigrams", 0)),
        "text": (
            f"Phase-49: Syllabic LM built. "
            f"{result.get('n_syllables', 0)} syllable types, "
            f"{result.get('n_bigrams', 0)} bigrams. "
            f"Top syllables: {result.get('top_syllables', [])[:10]}"
        ),
        "gpu_device": device,
    }


# ── Phase-50: DEDR Sign Catalogue ────────────────────────────────────────────

def _dedr_catalogue(inputs: dict, params: dict) -> dict:
    """Map sign depictions → DEDR etymologies → rebus phoneme candidates.
    GPU: torch for cosine similarity matrix.
    """
    device = _get_device()
    result = _run_phase_script("phase50_dedr_sign_catalogue.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    candidates = result.get("new_rebus_candidates", [])
    return {
        "new_candidates": candidates,
        "n_new_candidates": len(candidates),
        "catalogue": result.get("catalogue", []),
        "similar_pairs": result.get("similar_sign_pairs", []),
        "json": result,
        "number": float(len(candidates)),
        "text": (
            f"Phase-50: DEDR catalogue built. "
            f"{result.get('n_signs_catalogued', 0)} signs catalogued, "
            f"{len(candidates)} new rebus candidates."
        ),
        "gpu_device": device,
    }


# ── Phase-51: Parpola Crosswalk Importer ─────────────────────────────────────

def _parpola_importer(inputs: dict, params: dict) -> dict:
    """Import Parpola 1994 sign readings into INDUS_FINAL_ANCHORS.json.
    Also mines Parpola/Levit texts for additional readings.
    """
    device = _get_device()
    result = _run_phase_script("phase51_parpola_crosswalk.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    # Re-read updated anchors
    anchors = {}
    if _ANCHORS.exists():
        try:
            anchors = json.loads(_ANCHORS.read_text("utf-8"))["anchors"]
        except Exception:  # noqa: BLE001
            pass

    n_added = result.get("n_added_to_anchors", 0)
    n_total = len(anchors)
    return {
        "n_added": n_added,
        "n_upgraded": result.get("n_upgraded_in_anchors", 0),
        "total_anchors": n_total,
        "merged_map": result.get("merged_phoneme_map", {}),
        "json": result,
        "number": float(n_added),
        "text": (
            f"Phase-51: Parpola import complete. "
            f"Added {n_added} new signs, {result.get('n_upgraded_in_anchors',0)} upgraded. "
            f"Total anchors: {n_total}."
        ),
        "gpu_device": device,
    }


# ── Phase-52: Constrained Syllabic SA ────────────────────────────────────────

def _constrained_sa(inputs: dict, params: dict) -> dict:
    """Run constrained SA with syllabic LM and all confirmed anchors.
    Produces full 390-sign candidate decipherment table.
    GPU: BigramScorer on CUDA. ~2.5 min on GPU.
    """
    device = _get_device()
    result = _run_phase_script("phase52_syllabic_sa.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    # Load the full decipherment table
    table = []
    table_path = _REPORTS / "phase52_full_decipherment_table.json"
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
        "n_high": cov.get("n_high", 0),
        "n_medium": cov.get("n_medium", 0),
        "n_sa_only": cov.get("n_sa_only", 0),
        "sa_agreement_pct": (
            cov.get("sa_agrees_confirmed", 0) / max(cov.get("n_high", 0) + cov.get("n_medium", 0), 1)
        ),
        "json": result,
        "number": float(sa_res.get("z_score", 0)),
        "text": (
            f"Phase-52: Constrained syllabic SA complete. "
            f"z={sa_res.get('z_score',0):.2f}, lift={sa_res.get('lift',0):.4f}. "
            f"SA agrees with confirmed: {cov.get('sa_agrees_confirmed',0)}/{cov.get('n_high',0)+cov.get('n_medium',0)}."
        ),
        "gpu_device": device,
    }


# ── Phase-53: Formula Pilot ───────────────────────────────────────────────────

def _formula_pilot(inputs: dict, params: dict) -> dict:
    """Decode top-50 inscription formulas using confirmed readings.
    GPU: torch for formula clustering.
    """
    device = _get_device()
    result = _run_phase_script("phase53_formula_pilot.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    fully = result.get("fully_decoded", [])
    return {
        "fully_decoded_formulas": fully,
        "n_fully_decoded": len(fully),
        "top_formulas": result.get("top_50_formulas", [])[:10],
        "n_unique_formulas": result.get("n_unique_formulas", 0),
        "json": result,
        "number": float(len(fully)),
        "text": (
            f"Phase-53: Formula pilot complete. "
            f"{len(fully)} formulas ≥80% decoded. "
            f"Sample: {fully[0]['morphological'] if fully else 'none'}"
        ),
        "gpu_device": device,
    }


# ── Phase-54: Falsification Battery ──────────────────────────────────────────

def _falsification_battery(inputs: dict, params: dict) -> dict:
    """Run distributional falsification tests for promoted sign readings.
    GPU: torch for co-occurrence matrix.
    """
    device = _get_device()
    result = _run_phase_script("phase54_falsification.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    n_pass = result.get("n_pass", 0)
    n_weak = result.get("n_weak", 0)
    n_fail = result.get("n_fail", 0)
    total  = n_pass + n_weak + n_fail
    support = result.get("support_rate", 0)
    return {
        "n_pass": n_pass,
        "n_weak": n_weak,
        "n_fail": n_fail,
        "support_rate": support,
        "test_results": result.get("test_results", []),
        "json": result,
        "number": float(support),
        "text": (
            f"Phase-54: Falsification battery: {n_pass} PASS, {n_weak} WEAK, {n_fail} FAIL. "
            f"Support rate: {support:.0%}."
        ),
        "gpu_device": device,
    }


# ── Phase-55: Multi-LM Ensemble ──────────────────────────────────────────────

def _ensemble_decipher(inputs: dict, params: dict) -> dict:
    """Run SA against 4 LMs (Tamil char/syllabic, Proto-Dravidian, Sanskrit).
    Signs where Dravidian LMs agree and Sanskrit differs = ENSEMBLE_HIGH.
    GPU: BigramScorer CUDA for all 4 runs. ~10 min.
    """
    device = _get_device()
    result = _run_phase_script("phase55_ensemble.py")
    if "error" in result:
        return {**result, "gpu_device": device}

    # Load final table
    final_table = []
    final_path = _REPORTS / "phase55_final_decipherment.json"
    if final_path.exists():
        try:
            final_table = json.loads(final_path.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass

    ens = result.get("ensemble_summary", {})
    n_high = ens.get("ENSEMBLE_HIGH", 0)
    n_med  = ens.get("ENSEMBLE_MEDIUM", 0)
    return {
        "final_decipherment": final_table,
        "n_ensemble_high": n_high,
        "n_ensemble_medium": n_med,
        "ensemble_summary": ens,
        "lm_configs_used": result.get("lm_configs", []),
        "json": result,
        "number": float(n_high),
        "text": (
            f"Phase-55: Ensemble complete. "
            f"ENSEMBLE_HIGH: {n_high} signs, ENSEMBLE_MEDIUM: {n_med} signs. "
            f"LMs used: {result.get('lm_configs', [])}."
        ),
        "gpu_device": device,
    }


# ── Node definitions ─────────────────────────────────────────────────────────

def _phase48_55_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415
    return [
        AtomicNodeDef(
            id="IndusMediumValidator",
            name="MEDIUM Anchor Validator",
            category="Indus Decipherment",
            description=(
                "Phase-48: Validate all MEDIUM-confidence Indus anchor readings against "
                "3 independent tests (positional, DEDR attestation, bigram consistency). "
                "Signs passing ≥2/3 are promoted to HIGH. GPU-accelerated. "
                "MANDATORY: Run after any anchor set update."
            ),
            inputs=[],
            outputs=[
                {"name": "promoted_signs",  "type": "json",   "description": "List of sign IDs promoted to HIGH"},
                {"name": "n_promoted",       "type": "number", "description": "Count of promoted signs"},
                {"name": "coverage_pct",     "type": "number", "description": "New total HIGH coverage %"},
                {"name": "results",          "type": "json",   "description": "Per-sign test results"},
                {"name": "gpu_device",       "type": "text"},
                {"name": "text",             "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_medium_validator,
        ),
        AtomicNodeDef(
            id="IndusSyllabicLMBuilder",
            name="Syllabic LM Builder",
            category="Indus Decipherment",
            description=(
                "Phase-49: Build a Tamil syllabic (CV/CVC) bigram language model "
                "from TamilTB corpus + DEDR etymologies + anchor readings. "
                "Saves to dravidian_syllabic_lm.json for use by IndusConstrainedSA. "
                "GPU: torch for probability matrix construction."
            ),
            inputs=[],
            outputs=[
                {"name": "n_syllables",   "type": "number"},
                {"name": "n_bigrams",     "type": "number"},
                {"name": "top_syllables", "type": "json"},
                {"name": "lm_built",      "type": "number", "description": "1 if LM file saved"},
                {"name": "gpu_device",    "type": "text"},
                {"name": "text",          "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_syllabic_lm_builder,
        ),
        AtomicNodeDef(
            id="IndusDEDRCatalogue",
            name="DEDR Sign Catalogue",
            category="Indus Decipherment",
            description=(
                "Phase-50: For each IVC sign with a known depiction (animal, tool, plant), "
                "scan the Dravidian Etymological Dictionary (DEDR) for the Proto-Dravidian "
                "word for that object and extract its initial syllable (rebus phoneme). "
                "GPU: cosine similarity matrix over phoneme vectors."
            ),
            inputs=[],
            outputs=[
                {"name": "new_candidates",    "type": "json",   "description": "New rebus candidates for unread signs"},
                {"name": "n_new_candidates",  "type": "number"},
                {"name": "catalogue",         "type": "json",   "description": "Full sign depiction catalogue"},
                {"name": "similar_pairs",     "type": "json",   "description": "Phonemically similar sign pairs"},
                {"name": "gpu_device",        "type": "text"},
                {"name": "text",              "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_dedr_catalogue,
        ),
        AtomicNodeDef(
            id="IndusParpolaImporter",
            name="Parpola 1994 Importer",
            category="Indus Decipherment",
            description=(
                "Phase-51: Import all Parpola 1994 sign readings via the "
                "Parpola-sign-number → M-number crosswalk. Mines Parpola 1994, "
                "Parpola 2010, and Levit 2010 texts. Merges new readings into "
                "INDUS_FINAL_ANCHORS.json non-destructively."
            ),
            inputs=[],
            outputs=[
                {"name": "n_added",        "type": "number", "description": "New signs added to ANCHORS"},
                {"name": "n_upgraded",     "type": "number"},
                {"name": "total_anchors",  "type": "number"},
                {"name": "merged_map",     "type": "json"},
                {"name": "gpu_device",     "type": "text"},
                {"name": "text",           "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_parpola_importer,
        ),
        AtomicNodeDef(
            id="IndusConstrainedSA",
            name="Constrained Syllabic SA",
            category="Indus Decipherment",
            description=(
                "Phase-52: Run Simulated Annealing on the Holdat corpus using the "
                "syllabic LM with all HIGH+MEDIUM anchors fixed as constraints. "
                "Produces full 390-sign candidate decipherment table. "
                "GPU: BigramScorer CUDA. ~2-5 min on GPU. "
                "REQUIRES: IndusSyllabicLMBuilder must run first."
            ),
            inputs=[],
            outputs=[
                {"name": "decipherment_table", "type": "json",   "description": "Full 390-sign decipherment table"},
                {"name": "n_signs",            "type": "number"},
                {"name": "z_score",            "type": "number"},
                {"name": "lift",               "type": "number"},
                {"name": "sa_agreement_pct",   "type": "number", "description": "SA vs confirmed agreement rate"},
                {"name": "gpu_device",         "type": "text"},
                {"name": "text",               "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_constrained_sa,
        ),
        AtomicNodeDef(
            id="IndusFormulaPilot",
            name="Formula Pilot Reader",
            category="Indus Decipherment",
            description=(
                "Phase-53: Extract the 50 most frequent inscription formula patterns "
                "and decode them using confirmed readings. Reports formulas ≥80% decoded "
                "with morphological annotation. "
                "GPU: torch for formula clustering."
            ),
            inputs=[],
            outputs=[
                {"name": "fully_decoded_formulas", "type": "json",   "description": "Formulas ≥80% decoded"},
                {"name": "n_fully_decoded",         "type": "number"},
                {"name": "top_formulas",            "type": "json"},
                {"name": "gpu_device",              "type": "text"},
                {"name": "text",                    "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_formula_pilot,
        ),
        AtomicNodeDef(
            id="IndusFalsificationBattery",
            name="Falsification Battery",
            category="Indus Decipherment",
            description=(
                "Phase-54: Run distributional falsification tests for promoted sign readings. "
                "Each test makes a specific prediction that would be violated if the reading "
                "is wrong (e.g. M059=person sign should precede title markers). "
                "GPU: torch for co-occurrence matrix."
            ),
            inputs=[],
            outputs=[
                {"name": "n_pass",         "type": "number"},
                {"name": "n_weak",         "type": "number"},
                {"name": "n_fail",         "type": "number"},
                {"name": "support_rate",   "type": "number"},
                {"name": "test_results",   "type": "json"},
                {"name": "gpu_device",     "type": "text"},
                {"name": "text",           "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_falsification_battery,
        ),
        AtomicNodeDef(
            id="IndusEnsembleDecipher",
            name="Multi-LM Ensemble Decipherment",
            category="Indus Decipherment",
            description=(
                "Phase-55: Run SA against 4 LMs: Tamil char, Tamil syllabic, "
                "Proto-Dravidian (DEDR), and Sanskrit (adversarial). "
                "Signs where Dravidian LMs agree and Sanskrit differs = ENSEMBLE_HIGH. "
                "This produces the final confidence-stratified decipherment table. "
                "GPU: CUDA BigramScorer for all 4 LMs. ~10 min total."
            ),
            inputs=[],
            outputs=[
                {"name": "final_decipherment",  "type": "json",   "description": "Full confidence-stratified decipherment"},
                {"name": "n_ensemble_high",      "type": "number", "description": "Signs with highest confidence"},
                {"name": "n_ensemble_medium",    "type": "number"},
                {"name": "ensemble_summary",     "type": "json"},
                {"name": "lm_configs_used",      "type": "json"},
                {"name": "gpu_device",           "type": "text"},
                {"name": "text",                 "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_ensemble_decipher,
        ),
    ]
