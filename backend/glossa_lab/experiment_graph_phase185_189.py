"""Experiment Graph nodes for Phases 185-189: decipherment experiments."""
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


def _run(script: str, timeout: int = 900) -> dict[str, Any]:
    p = _SCRIPTS / script
    if not p.exists():
        return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"Exit {r.returncode}", "stderr": r.stderr[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout after {timeout}s"}
    except Exception as exc:
        return {"error": str(exc)}
    return {"status": "ok"}


def _load(json_name: str) -> dict[str, Any]:
    p = _OUTPUTS / json_name
    if not p.exists():
        return {"available": False}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"available": False}


# ── Phase 185: Fish-Sign Anchor Battery ──────────────────────────────────────

def _fish_sign_battery(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load("phase185_fish_sign_battery.json")
    if report.get("available") is False:
        res = _run("phase185_fish_sign_battery.py", timeout=900)
        if "error" in res:
            return {**res, "number": 0.0, "text": "Phase-185 error"}
        report = _load("phase185_fish_sign_battery.json")
    delta = report.get("consistency_delta", 0.0)
    verdict = report.get("verdict", "")
    return {
        "consistency_delta": delta,
        "verdict": verdict,
        "fish_sign_proposals": report.get("fish_sign_proposals", []),
        "bigram_analysis": report.get("bigram_analysis", {}),
        "candidate_new_anchors": report.get("candidate_new_anchors", []),
        "json": {"delta": delta},
        "number": delta,
        "text": f"Phase-185 fish-sign battery: delta={delta:+.4f}. {verdict}",
    }


# ── Phase 186: Elamo-Dravidian Gap Coverage ───────────────────────────────────

def _elamo_dravidian_gap(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load("phase186_elamo_dravidian_gap.json")
    if report.get("available") is False:
        res = _run("phase186_elamo_dravidian_gap.py", timeout=120)
        if "error" in res:
            return {**res, "number": 0.0, "text": "Phase-186 error"}
        report = _load("phase186_elamo_dravidian_gap.json")
    covered = report.get("absent_phonemes_covered_by_elamite", 0)
    total   = report.get("absent_phonemes_total", 14)
    pct     = report.get("coverage_pct", 0.0)
    return {
        "covered_count": covered,
        "total_absent": total,
        "coverage_pct": pct,
        "covered_phonemes": report.get("covered", []),
        "still_uncovered": report.get("still_uncovered", []),
        "priority_proposals": report.get("priority_proposals", []),
        "json": {"covered": covered, "pct": pct},
        "number": covered,
        "text": (f"Phase-186 Elamo-Dravidian: {covered}/{total} absent phonemes "
                 f"covered ({pct:.1f}%). {report.get('verdict', '')}"),
    }


# ── Phase 187: 2025-2026 Sign Hypothesis Battery ──────────────────────────────

def _sign_hypothesis_battery(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load("phase187_sign_hypothesis_battery.json")
    if report.get("available") is False:
        res = _run("phase187_sign_hypothesis_battery.py", timeout=180)
        if "error" in res:
            return {**res, "number": 0.0, "text": "Phase-187 error"}
        report = _load("phase187_sign_hypothesis_battery.json")
    agr = report.get("agreement_summary", {})
    return {
        "agreement_rate": agr.get("agreement_rate", 0.0),
        "full_agreement": agr.get("full_agreement", 0),
        "pleonastic_patterns": report.get("pleonastic_patterns", []),
        "mathematical_claims": report.get("mathematical_claims", []),
        "papers_found": report.get("papers_found", []),
        "json": agr,
        "number": agr.get("agreement_rate", 0.0),
        "text": f"Phase-187: {agr.get('full_agreement',0)} pleonastic compounds confirmed. {report.get('verdict','')}",
    }


# ── Phase 188: Commodity Semantic Layer ──────────────────────────────────────

def _commodity_semantic(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load("phase188_commodity_semantic.json")
    if report.get("available") is False:
        res = _run("phase188_commodity_semantic.py", timeout=180)
        if "error" in res:
            return {**res, "number": 0.0, "text": "Phase-188 error"}
        report = _load("phase188_commodity_semantic.json")
    strong = report.get("strong_matches", 0)
    mod    = report.get("moderate_matches", 0)
    return {
        "strong_commodity_matches": strong,
        "moderate_commodity_matches": mod,
        "strong_detail": report.get("strong_detail", []),
        "moderate_detail": report.get("moderate_detail", []),
        "commodity_results": report.get("commodity_results", []),
        "json": {"strong": strong, "moderate": mod},
        "number": strong + mod,
        "text": (f"Phase-188 commodity: {strong} STRONG + {mod} MODERATE matches. "
                 f"{report.get('verdict', '')}"),
    }


# ── Phase 189: Northern Dravidian LM Comparison ───────────────────────────────

def _northern_dravidian_lm(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load("phase189_northern_dravidian_lm.json")
    if report.get("available") is False:
        res = _run("phase189_northern_dravidian_lm.py", timeout=900)
        if "error" in res:
            return {**res, "number": 0.0, "text": "Phase-189 error"}
        report = _load("phase189_northern_dravidian_lm.json")
    delta   = report.get("consistency_delta", 0.0)
    novel   = len(report.get("novel_north_proposals", []))
    best_br = report.get("best_north_coverage_branch", "brahui")
    return {
        "consistency_delta": delta,
        "novel_absent_proposals": novel,
        "best_branch": best_br,
        "north_dr_coverage": report.get("north_dr_coverage", {}),
        "novel_north_proposals": report.get("novel_north_proposals", []),
        "absent_phoneme_comparisons": report.get("absent_phoneme_comparisons", []),
        "json": {"delta": delta, "novel": novel},
        "number": novel,
        "text": (f"Phase-189 North Dravidian: delta={delta:+.4f}, "
                 f"{novel} novel absent-phoneme proposals. {report.get('verdict', '')}"),
    }


# ── Node definitions ──────────────────────────────────────────────────────────

def _phase185_189_node_defs() -> list[AtomicNodeDef]:
    _STD = [
        {"name": "json",   "type": "json"},
        {"name": "number", "type": "number"},
        {"name": "text",   "type": "text"},
    ]
    return [
        AtomicNodeDef(
            id="IndusFishSignBattery185",
            name="Fish-Sign Anchor Battery (P185)",
            category="Indus Decipherment",
            description=(
                "Phase-185: Fish-sign phoneme battery. Fetches DOIs for E13/E17 papers "
                "via Unpaywall, extracts sign-phoneme proposals, runs SA convergence test "
                "with fish-sign anchors vs baseline, reports consistency delta. "
                "Targets M047 (min/mīn MEDIUM) and adjacent fish-sign variants."
            ),
            inputs=[],
            outputs=[
                {"name": "consistency_delta",    "type": "number"},
                {"name": "fish_sign_proposals",  "type": "json"},
                {"name": "candidate_new_anchors","type": "json"},
                {"name": "bigram_analysis",      "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_fish_sign_battery,
        ),
        AtomicNodeDef(
            id="IndusElamoDravidianGap186",
            name="Elamo-Dravidian Gap Coverage (P186)",
            category="Indus Decipherment",
            description=(
                "Phase-186: McAlpin (1974) Elamo-Dravidian gap coverage. "
                "Cross-references 57 Elamite/Dravidian cognate pairs against the 14 absent phonemes. "
                "Reports how many absent phonemes are independently supported by Elamite evidence, "
                "proposes sign candidates for each covered gap. Pure analysis, no SA."
            ),
            inputs=[],
            outputs=[
                {"name": "covered_count",      "type": "number"},
                {"name": "coverage_pct",       "type": "number"},
                {"name": "covered_phonemes",   "type": "json"},
                {"name": "still_uncovered",    "type": "json"},
                {"name": "priority_proposals", "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_elamo_dravidian_gap,
        ),
        AtomicNodeDef(
            id="IndusSignHypothesisBattery187",
            name="2025-2026 Sign Hypothesis Battery (P187)",
            category="Indus Decipherment",
            description=(
                "Phase-187: Tests pleonastic compounding proposals from E18 (2025/2026) "
                "and mathematical decipherment claims from E15 (2026). "
                "Checks bigram lift for predicted compound pairs in M77 corpus; "
                "verifies Indus entropy matches Tamil syllabic target; "
                "computes agreement rate with INDUS_FINAL_ANCHORS."
            ),
            inputs=[],
            outputs=[
                {"name": "agreement_rate",      "type": "number"},
                {"name": "pleonastic_patterns", "type": "json"},
                {"name": "mathematical_claims", "type": "json"},
                {"name": "papers_found",        "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_sign_hypothesis_battery,
        ),
        AtomicNodeDef(
            id="IndusCommoditySemantic188",
            name="Commodity Semantic Layer (P188)",
            category="Indus Decipherment",
            description=(
                "Phase-188: Tamil DEDR commodity vocabulary → corpus sequence mapping. "
                "Tests 25 commodity words (metals, gems, crops, livestock, crafts, titles) "
                "as rebus sequences in the M77 corpus. Reports lift (observed/expected) "
                "for each commodity sequence. Semantic complement to statistical anchors."
            ),
            inputs=[],
            outputs=[
                {"name": "strong_commodity_matches",   "type": "number"},
                {"name": "moderate_commodity_matches", "type": "number"},
                {"name": "strong_detail",              "type": "json"},
                {"name": "commodity_results",          "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_commodity_semantic,
        ),
        AtomicNodeDef(
            id="IndusNorthDravidianLM189",
            name="Northern Dravidian LM Comparison (P189)",
            category="Indus Decipherment",
            description=(
                "Phase-189: Builds a Brahui/Kurukh/Gondi-informed North Dravidian LM "
                "and compares SA results against Tamil LM baseline. "
                "Reports which of the 14 absent phonemes have North Dravidian coverage, "
                "novel sign-phoneme proposals from the northern LM, "
                "and consistency delta between North and South Dravidian runs."
            ),
            inputs=[],
            outputs=[
                {"name": "consistency_delta",        "type": "number"},
                {"name": "novel_absent_proposals",   "type": "number"},
                {"name": "north_dr_coverage",        "type": "json"},
                {"name": "novel_north_proposals",    "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_northern_dravidian_lm,
        ),
    ]
