"""Experiment Graph Nodes: Phase-81–87 Indus Decipherment Pipeline.

  IndusMSign293         Phase-81: M293 targeted sign deep-dive
  IndusSealTranslation  Phase-82: Complete seal translation pilot
  IndusGapSprint        Phase-83: Top gap signs sprint (M220/M079/M022/M019)
  IndusFormulaLexicon   Phase-84: Extended formula lexicon
  IndusCisiCrossval     Phase-85: CISI corpus cross-validation
  IndusPhonologyRecon   Phase-86: Phonological reconstruction
  IndusAnchorSprint120  Phase-87: Anchor sprint to 120 HIGH+MEDIUM

MANDATORY: Created per H23 before any Phase-81-87 script execution.
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
            capture_output=True, text=True, timeout=1800,
            cwd=str(_REPO),
        )
        if r.returncode != 0:
            return {"error": f"Script failed (exit {r.returncode})",
                    "stderr": r.stderr[-500:], "stdout": r.stdout[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Timed out after 1800s: {script_name}"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}
    if report_path.exists():
        try:
            return json.loads(report_path.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True, "stdout": r.stdout[-200:]}


# ── node functions ────────────────────────────────────────────────────────────

def _m293_deep_dive(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase81_m293_sign_deep_dive.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"proposed_reading": result.get("proposed_reading", ""),
            "confidence": result.get("proposed_confidence", ""),
            "positional_class": result.get("positional_class", ""),
            "json": result, "number": float(result.get("evidence_score", 0)),
            "text": f"Phase-81: M293={result.get('proposed_reading','?')} "
                    f"conf={result.get('proposed_confidence','?')} "
                    f"pos={result.get('positional_class','?')}",
            "gpu_device": device}

def _seal_translation(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase82_seal_translation_pilot.py")
    if "error" in result: return {**result, "gpu_device": device}
    n = result.get("n_translated", 0)
    return {"n_translated": n, "translations": result.get("translations", []),
            "mean_coverage": result.get("mean_coverage_pct", 0),
            "json": result, "number": float(n),
            "text": f"Phase-82: {n} seals translated. "
                    f"Mean coverage={result.get('mean_coverage_pct',0):.1f}%.",
            "gpu_device": device}

def _gap_sprint(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase83_gap_signs_sprint.py")
    if "error" in result: return {**result, "gpu_device": device}
    n = result.get("n_new_proposals", 0)
    return {"n_new_proposals": n, "proposals": result.get("proposals", []),
            "promoted": result.get("promoted_to_medium", []),
            "json": result, "number": float(n),
            "text": f"Phase-83: {n} gap sign proposals. "
                    f"{len(result.get('promoted_to_medium',[]))} promoted to MEDIUM.",
            "gpu_device": device}

def _formula_lexicon(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase84_formula_lexicon.py")
    if "error" in result: return {**result, "gpu_device": device}
    n = result.get("n_formulas_decoded", 0)
    return {"n_formulas_decoded": n, "lexicon": result.get("formula_lexicon", []),
            "json": result, "number": float(n),
            "text": f"Phase-84: {n} formulas with full natural-language readings.",
            "gpu_device": device}

def _cisi_crossval(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase85_cisi_crossval.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"agreement_pct": result.get("agreement_pct", 0),
            "n_tested": result.get("n_anchors_tested", 0),
            "json": result, "number": float(result.get("agreement_pct", 0)),
            "text": f"Phase-85: CISI cross-val. Agreement={result.get('agreement_pct',0):.1f}% "
                    f"on {result.get('n_anchors_tested',0)} anchors.",
            "gpu_device": device}

def _phonology_recon(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase86_phonology_recon.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"n_consonants": result.get("n_consonants", 0),
            "n_vowels": result.get("n_vowels", 0),
            "coverage_pct": result.get("pd_coverage_pct", 0),
            "json": result, "number": float(result.get("pd_coverage_pct", 0)),
            "text": f"Phase-86: {result.get('n_consonants',0)}C "
                    f"{result.get('n_vowels',0)}V attested. "
                    f"PD coverage={result.get('pd_coverage_pct',0):.1f}%.",
            "gpu_device": device}

def _anchor_sprint_120(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase87_anchor_sprint_120.py")
    if "error" in result: return {**result, "gpu_device": device}
    n = result.get("n_new_medium_anchors", 0)
    total = result.get("total_high_medium", 0)
    return {"n_new_anchors": n, "total_high_medium": total,
            "new_anchors": result.get("new_medium_anchors", []),
            "json": result, "number": float(total),
            "text": f"Phase-87: +{n} MEDIUM anchors. "
                    f"Total HIGH+MEDIUM={total}.",
            "gpu_device": device}


# ── node definitions ─────────────────────────────────────────────────────────

def _phase81_87_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415
    return [
        AtomicNodeDef(id="IndusMSign293", name="M293 Sign Deep-Dive",
            category="Indus Decipherment",
            description="Phase-81: Targeted multi-method analysis of M293 — the highest-frequency unread sign (freq=232). Combines positional profiling, N-gram context, DEDR rebus, Parpola crosswalk, and Phase-73 SA consensus to propose a MEDIUM-confidence reading. CPU.",
            inputs=[], outputs=[{"name":"proposed_reading","type":"text"},{"name":"confidence","type":"text"},{"name":"positional_class","type":"text"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_m293_deep_dive),
        AtomicNodeDef(id="IndusSealTranslation", name="Complete Seal Translation Pilot",
            category="Indus Decipherment",
            description="Phase-82: Translate 10+ highest-coverage Holdat seals using all 97 HIGH+MEDIUM anchors. Score by coverage %. Produces the first human-readable Indus seal readings with confidence breakdown. CPU.",
            inputs=[], outputs=[{"name":"n_translated","type":"number"},{"name":"translations","type":"json"},{"name":"mean_coverage","type":"number"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_seal_translation),
        AtomicNodeDef(id="IndusGapSprint", name="Top Gap Signs Sprint",
            category="Indus Decipherment",
            description="Phase-83: Apply M293 deep-dive methodology to M220, M079, M022, M019, M044 (next highest-priority gaps after Phase-81). DEDR rebus + grammar position + SA consensus. Target 3-5 new MEDIUM anchors. CPU.",
            inputs=[], outputs=[{"name":"n_new_proposals","type":"number"},{"name":"proposals","type":"json"},{"name":"promoted","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_gap_sprint),
        AtomicNodeDef(id="IndusFormulaLexicon", name="Extended Formula Lexicon",
            category="Indus Decipherment",
            description="Phase-84: Full natural-language readings for all decoded formula patterns using all 97 HIGH+MEDIUM anchors. Extends Phase-68 translations. Produces complete formula-translation lexicon. CPU.",
            inputs=[], outputs=[{"name":"n_formulas_decoded","type":"number"},{"name":"lexicon","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_formula_lexicon),
        AtomicNodeDef(id="IndusCisiCrossval", name="CISI Corpus Cross-Validation",
            category="Indus Decipherment",
            description="Phase-85: Validate all 97 HIGH+MEDIUM anchor readings against the separate CISI corpus (179 inscriptions). Measure positional agreement, find CISI-unique patterns, check anchor sign frequency in CISI. CPU.",
            inputs=[], outputs=[{"name":"agreement_pct","type":"number"},{"name":"n_tested","type":"number"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_cisi_crossval),
        AtomicNodeDef(id="IndusPhonologyRecon", name="Phonological Reconstruction",
            category="Indus Decipherment",
            description="Phase-86: Reconstruct Proto-Dravidian phonological inventory from 97 confirmed anchor readings. Consonants, vowels, syllable structures. Compare to Zvelebil 1970 and Krishnamurti 2003 PD reconstruction. Identify gaps. CPU.",
            inputs=[], outputs=[{"name":"n_consonants","type":"number"},{"name":"n_vowels","type":"number"},{"name":"coverage_pct","type":"number"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_phonology_recon),
        AtomicNodeDef(id="IndusAnchorSprint120", name="Anchor Sprint to 120",
            category="Indus Decipherment",
            description="Phase-87: Systematic sprint from 97 to 120 HIGH+MEDIUM anchors. Combines: Phase-73 SA consensus (ENSEMBLE_HIGH/MED signs), DEDR extended rebus, grammar position analysis, and phonological plausibility filter. GPU: BigramScorer + torch.",
            inputs=[], outputs=[{"name":"n_new_anchors","type":"number"},{"name":"total_high_medium","type":"number"},{"name":"new_anchors","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_anchor_sprint_120),
    ]
