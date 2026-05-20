"""Experiment Graph atomic nodes for Phases 146–155.

Nodes:
  IndusF3Redesign146        — Phase-146 (F3 redesign, phonological exclusivity)
  IndusRoifValidation       — Phase-147 (Roif validation STRONGLY_SUPPORTED)
  IndusFormulaSemantics     — Phase-148 (formula semantics, morpheme roles)
  IndusAdversarialBattery   — Phase-149 (10/10 adversarial challenge battery)
  IndusPolysemyPermutation  — Phase-150 (fish-sign polysemy permutation test)
  IndusSiteKLBootstrap      — Phase-151 (site-stratified KL bootstrap)
  IndusShuIlishu152         — Phase-152 (Shu-ilishu seal cross-validation)
  IndusSibilantAnchors      — Phase-153 (sibilant sign anchor candidates)
  IndusVowelHarmonyDx       — Phase-154 (vowel harmony diagnostic)
  IndusPhonotacticSibilant  — Phase-155 (phonotactic sibilant gap analysis)
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


def _simple_load_fn(report_name: str, script_name: str, timeout: int,
                    label: str) -> dict[str, Any]:
    """Generic load-or-run helper returning standard output dict."""
    report = _load_report(report_name)
    if report.get("available") is False:
        run_result = _run_phase_script(script_name, timeout=timeout)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0, "text": f"{label}: Error",
                    "gpu_device": "cpu"}
        report = _load_report(report_name)
    verdict = report.get("verdict", report.get("overall_verdict", "UNKNOWN"))
    summary = report.get("summary", report.get("findings", {}))
    return {
        "verdict":    verdict,
        "summary":    summary,
        "json":       {"verdict": verdict, "summary": summary},
        "number":     float(report.get("score", report.get("n_confirmed", 0))),
        "text":       f"{label}: verdict={verdict}. {report.get('headline', '')}",
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Individual phase functions ────────────────────────────────────────────────

def _f3_redesign(i, p):
    return _simple_load_fn("phase146_f3_redesign.json", "phase146_f3_redesign.py", 300,
                            "Phase-146 F3 redesign")

def _roif_validation(i, p):
    r = _load_report("phase147_roif_validation.json")
    if r.get("available") is False:
        run_result = _run_phase_script("phase147_roif_validation.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0, "text": "Error", "gpu_device": "cpu"}
        r = _load_report("phase147_roif_validation.json")
    verdict      = r.get("verdict", "UNKNOWN")
    support_pct  = r.get("support_percentage", 0.0)
    n_tests      = r.get("n_tests", 0)
    return {
        "verdict":        verdict,
        "support_pct":    support_pct,
        "n_tests":        n_tests,
        "json": {"verdict": verdict, "support_pct": support_pct},
        "number": support_pct,
        "text": f"Phase-147 Roif validation: {verdict} ({support_pct:.0f}% support, {n_tests} tests).",
        "gpu_device": r.get("gpu_device", "cpu"),
    }

def _formula_semantics(i, p):
    return _simple_load_fn("phase148_formula_semantics.json", "phase148_formula_semantics.py",
                            300, "Phase-148 formula semantics")

def _adversarial_battery(i, p):
    r = _load_report("phase149_adversarial_challenge.json")
    if r.get("available") is False:
        run_result = _run_phase_script("phase149_adversarial_challenge.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0, "text": "Error", "gpu_device": "cpu"}
        r = _load_report("phase149_adversarial_challenge.json")
    n_survive = r.get("n_survive", r.get("claims_survive", 0))
    n_total   = r.get("n_total", r.get("n_claims", 0))
    n_fail    = r.get("n_fail", 0)
    return {
        "n_survive": n_survive, "n_total": n_total, "n_fail": n_fail,
        "json": {"n_survive": n_survive, "n_total": n_total},
        "number": float(n_survive),
        "text": f"Phase-149 adversarial battery: {n_survive}/{n_total} survive, {n_fail} FAIL.",
        "gpu_device": r.get("gpu_device", "cpu"),
    }

def _polysemy_permutation(i, p):
    return _simple_load_fn("phase150_polysemy_permutation.json", "phase150_polysemy_permutation.py",
                            300, "Phase-150 polysemy permutation")

def _site_kl_bootstrap(i, p):
    r = _load_report("phase151_site_kl_bootstrap.json")
    if r.get("available") is False:
        run_result = _run_phase_script("phase151_site_kl_bootstrap.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0, "text": "Error", "gpu_device": "cpu"}
        r = _load_report("phase151_site_kl_bootstrap.json")
    mean_kl  = r.get("mean_kl_divergence", 0.0)
    verdict  = r.get("verdict", "UNKNOWN")
    return {
        "mean_kl_divergence": mean_kl, "verdict": verdict,
        "json": {"mean_kl": mean_kl, "verdict": verdict},
        "number": mean_kl,
        "text": f"Phase-151 site KL bootstrap: mean_KL={mean_kl:.4f}, verdict={verdict}.",
        "gpu_device": r.get("gpu_device", "cpu"),
    }

def _shu_ilishu(i, p):
    return _simple_load_fn("phase152_shu_ilishu.json", "phase152_shu_ilishu.py", 300,
                            "Phase-152 Shu-ilishu")

def _sibilant_anchors(i, p):
    r = _load_report("phase153_sibilant_anchors.json")
    if r.get("available") is False:
        run_result = _run_phase_script("phase153_sibilant_anchors.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0, "text": "Error", "gpu_device": "cpu"}
        r = _load_report("phase153_sibilant_anchors.json")
    candidates = r.get("sibilant_candidates", [])
    n_proposed = r.get("n_proposed", len(candidates))
    return {
        "sibilant_candidates": candidates, "n_proposed": n_proposed,
        "json": {"candidates": candidates},
        "number": float(n_proposed),
        "text": f"Phase-153 sibilant anchors: {n_proposed} candidates proposed.",
        "gpu_device": r.get("gpu_device", "cpu"),
    }

def _vowel_harmony_dx(i, p):
    return _simple_load_fn("phase154_vowel_harmony_diagnostic.json",
                            "phase154_vowel_harmony_diagnostic.py", 300,
                            "Phase-154 vowel harmony diagnostic")

def _phonotactic_sibilant(i, p):
    return _simple_load_fn("phase155_phonotactic_sibilant.json",
                            "phase155_phonotactic_sibilant.py", 300,
                            "Phase-155 phonotactic sibilant")


# ── Standard output port set ─────────────────────────────────────────────────

_STD_OUTPUTS = [
    {"name": "verdict",     "type": "text"},
    {"name": "summary",     "type": "json"},
    {"name": "json",        "type": "json"},
    {"name": "number",      "type": "number"},
    {"name": "text",        "type": "text"},
    {"name": "gpu_device",  "type": "text"},
]


# ── Node definitions ──────────────────────────────────────────────────────────

def _phase146_155_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            id="IndusF3Redesign146",
            name="F3 Redesign (P146)",
            category="Indus Decipherment",
            description=(
                "Phase-146: redesigned F3 phonological exclusivity test. "
                "CV-skeleton anchors compared against Dravidian vs Sanskrit phoneme inventories."
            ),
            inputs=[], outputs=[
                {"name": "verdict", "type": "text"},
                {"name": "exclusivity_ratio", "type": "number"},
                *_STD_OUTPUTS[2:],
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_f3_redesign,
        ),
        AtomicNodeDef(
            id="IndusRoifValidation",
            name="Roif Hypothesis Validation (P147)",
            category="Indus Decipherment",
            description=(
                "Phase-147: formal test of Roif's phonetic-mnemonic Akkadian shorthand hypothesis. "
                "Result: STRONGLY_SUPPORTED — fish compound structure consistent with min/mīn."
            ),
            inputs=[], outputs=[
                {"name": "verdict",      "type": "text"},
                {"name": "support_pct",  "type": "number"},
                {"name": "n_tests",      "type": "number"},
                *_STD_OUTPUTS[2:],
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_roif_validation,
        ),
        AtomicNodeDef(
            id="IndusFormulaSemantics",
            name="Formula Semantics (P148)",
            category="Indus Decipherment",
            description=(
                "Phase-148: morpheme role database expansion + formula semantic classification. "
                "Assigns PLACE_FORMULA / TITLE_FORMULA / UNCERTAIN to decoded seals."
            ),
            inputs=[], outputs=_STD_OUTPUTS,
            params_schema={"type": "object", "properties": {}},
            fn=_formula_semantics,
        ),
        AtomicNodeDef(
            id="IndusAdversarialBattery",
            name="Adversarial Challenge Battery (P149)",
            category="Indus Decipherment",
            description=(
                "Phase-149: 10-claim adversarial challenge battery. "
                "Result: 10/10 claims survive (4 clean, 6 with caveat), 0 FAIL."
            ),
            inputs=[], outputs=[
                {"name": "n_survive", "type": "number"},
                {"name": "n_total",   "type": "number"},
                {"name": "n_fail",    "type": "number"},
                *_STD_OUTPUTS[2:],
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_adversarial_battery,
        ),
        AtomicNodeDef(
            id="IndusPolysemyPermutation",
            name="Polysemy Permutation Test (P150)",
            category="Indus Decipherment",
            description=(
                "Phase-150: permutation null model for fish-sign polysemy hypothesis. "
                "Tests whether M047 isolation rate differs from compound-only expectation."
            ),
            inputs=[], outputs=_STD_OUTPUTS,
            params_schema={"type": "object", "properties": {}},
            fn=_polysemy_permutation,
        ),
        AtomicNodeDef(
            id="IndusSiteKLBootstrap",
            name="Site KL Bootstrap (P151)",
            category="Indus Decipherment",
            description=(
                "Phase-151: site-stratified KL-divergence bootstrap test for sign-frequency "
                "homogeneity across 9 Holdat sites."
            ),
            inputs=[], outputs=[
                {"name": "mean_kl_divergence", "type": "number"},
                {"name": "verdict",            "type": "text"},
                *_STD_OUTPUTS[2:],
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_site_kl_bootstrap,
        ),
        AtomicNodeDef(
            id="IndusShuIlishu152",
            name="Shu-ilishu Cross-Validation (P152)",
            category="Indus Decipherment",
            description=(
                "Phase-152: cross-validation of anchor set against the Shu-ilishu "
                "Meluhhan interpreter inscription (Ur III period)."
            ),
            inputs=[], outputs=_STD_OUTPUTS,
            params_schema={"type": "object", "properties": {}},
            fn=_shu_ilishu,
        ),
        AtomicNodeDef(
            id="IndusSibilantAnchors",
            name="Sibilant Anchor Candidates (P153)",
            category="Indus Decipherment",
            description=(
                "Phase-153: distributional proximity analysis for sibilant sign candidates. "
                "Precursor to Phase-163 sibilant discovery."
            ),
            inputs=[], outputs=[
                {"name": "sibilant_candidates", "type": "json"},
                {"name": "n_proposed",          "type": "number"},
                *_STD_OUTPUTS[2:],
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_sibilant_anchors,
        ),
        AtomicNodeDef(
            id="IndusVowelHarmonyDx",
            name="Vowel Harmony Diagnostic (P154)",
            category="Indus Decipherment",
            description=(
                "Phase-154: diagnostic for Dravidian vowel harmony constraint across "
                "HIGH/MEDIUM anchor readings. Checks front/back vowel consistency."
            ),
            inputs=[], outputs=_STD_OUTPUTS,
            params_schema={"type": "object", "properties": {}},
            fn=_vowel_harmony_dx,
        ),
        AtomicNodeDef(
            id="IndusPhonotacticSibilant",
            name="Phonotactic Sibilant Analysis (P155)",
            category="Indus Decipherment",
            description=(
                "Phase-155: phonotactic gap analysis specifically for sibilant consonants. "
                "Identifies positions where sibilants are underrepresented in the anchor set."
            ),
            inputs=[], outputs=_STD_OUTPUTS,
            params_schema={"type": "object", "properties": {}},
            fn=_phonotactic_sibilant,
        ),
    ]
