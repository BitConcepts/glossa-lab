"""Experiment Graph atomic nodes for Phases 171–178.

Network analysis batch — network centrality, betweenness stratification,
and deep-dive phases building toward the ICIT corpus access request.

Nodes:
  IndusNetworkCentrality171       — Phase-171 (Roif × Pierson bridge-node validation)
  IndusBetweennessStratification172_174 — Phases 172-174 (full BC, irresolvable check,
                                           Meluhhan name matching)
  IndusNetworkDeep175_178         — Phases 175-178 (site-stratified, M059, BC-to-slot,
                                     ICIT priority targeting)
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
_OUTPUTS = _REPO / "outputs"
_REPORTS = _REPO / "research" / "indus" / "phase_reports"


def _run_phase_script(script_name: str, timeout: int = 600) -> dict[str, Any]:
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
            return {"error": f"Script exited {result.returncode}",
                    "stderr": result.stderr[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Script timed out after {timeout}s"}
    except Exception as exc:
        return {"error": str(exc)}
    return {"status": "ok", "stdout_tail": result.stdout[-500:]}


def _load_output(json_name: str) -> dict[str, Any]:
    """Load from outputs/ directory (phases 171-178 write there)."""
    path = _OUTPUTS / json_name
    if not path.exists():
        return {"available": False, "error": f"Output not found: {json_name}"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _load_report(json_name: str) -> dict[str, Any]:
    """Load from research/indus/phase_reports/ (phase172 also writes there)."""
    path = _REPORTS / json_name
    if not path.exists():
        return {"available": False, "error": f"Report not found: {json_name}"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "error": str(exc)}


# ── Phase-171: Network Centrality Validation ─────────────────────────────────

def _network_centrality_171(inputs: dict, params: dict) -> dict[str, Any]:
    """Phase-171: independent validation of Roif's betweenness centrality claim."""
    report = _load_output("phase171_network_centrality_validation.json")
    if report.get("available") is False:
        run_result = _run_phase_script(
            "phase171_network_centrality_validation.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-171 error", "gpu_device": "cpu"}
        report = _load_output("phase171_network_centrality_validation.json")

    verdict  = report.get("verdict", {})
    claim    = verdict.get("bridge_node_claim", "UNKNOWN")
    m099_r   = report.get("B_our_graph", {}).get("M099_rank")
    m267_r   = report.get("B_our_graph", {}).get("M267_rank")
    return {
        "bridge_node_claim":      claim,
        "M099_rank_our_graph":    m099_r,
        "M267_rank_our_graph":    m267_r,
        "json":   {"claim": claim, "M099_rank": m099_r, "M267_rank": m267_r},
        "number": 1.0 if claim == "CONFIRMED" else 0.5 if claim == "PARTIAL" else 0.0,
        "text":   (f"Phase-171 network centrality: bridge-node claim {claim}. "
                   f"M099 rank {m099_r}, M267 rank {m267_r} in our independent graph."),
        "gpu_device": "cpu",
    }


# ── Phases 172-174: Betweenness Stratification ───────────────────────────────

def _betweenness_stratification_172_174(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 172-174: full BC, irresolvable MEDIAL check, Meluhhan name matching."""
    p172 = _load_report("phase172_betweenness_full.json")
    if p172.get("available") is False:
        run_result = _run_phase_script(
            "phase172_174_betweenness_stratification.py", timeout=600)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-172-174 error", "gpu_device": "cpu"}
        p172 = _load_report("phase172_betweenness_full.json")

    p173 = _load_output("phase173_irresolvable_check.json")
    p174 = _load_output("phase174_filtered_name_matching.json")

    n_grammar   = len(p172.get("grammar_candidates", []))
    n_namesyl   = len(p172.get("name_syllable_candidates", []))
    p173_verdict = p173.get("verdict", "UNKNOWN") if p173.get("available") is not False else "PENDING"
    p174_top     = p174.get("top_names_covered", []) if p174.get("available") is not False else []
    p174_gaps    = p174.get("absent_phonemes", []) if p174.get("available") is not False else []

    return {
        "n_grammar_candidates":      n_grammar,
        "n_name_syllable_candidates": n_namesyl,
        "phase173_verdict":          p173_verdict,
        "top_meluhhan_coverage":     p174_top[:5] if p174_top else [],
        "absent_phonemes":           p174_gaps,
        "json": {
            "n_grammar": n_grammar, "n_namesyl": n_namesyl,
            "p173_verdict": p173_verdict,
        },
        "number": n_grammar,
        "text":   (f"Phase-172: {n_grammar} grammar candidates (BC>0), "
                   f"{n_namesyl} name-syllable candidates (BC=0). "
                   f"Phase-173 irresolvable check: {p173_verdict}. "
                   f"Phase-174 absent phonemes: {len(p174_gaps)}."),
        "gpu_device": "cpu",
    }


# ── Phases 175-178: Network Deep Dive ────────────────────────────────────────

def _network_deep_175_178(inputs: dict, params: dict) -> dict[str, Any]:
    """Phases 175-178: site-stratified, M059 bridge, BC-to-slot, ICIT priority."""
    p175 = _load_output("phase175_site_stratified.json")
    if p175.get("available") is False:
        # Requires phase172 report to exist first
        p172_check = _load_report("phase172_betweenness_full.json")
        if p172_check.get("available") is False:
            return {"error": "Phase-175-178 requires Phase-172 output. Run Phase-172-174 first.",
                    "json": {}, "number": 0.0,
                    "text": "Phase-175-178 blocked: Phase-172 not yet run.", "gpu_device": "cpu"}
        run_result = _run_phase_script(
            "phase175_178_network_deep.py", timeout=600)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0,
                    "text": "Phase-175-178 error", "gpu_device": "cpu"}
        p175 = _load_output("phase175_site_stratified.json")

    p176 = _load_output("phase176_m059_bridge.json")
    p177 = _load_output("phase177_bc_slot_mapping.json")
    p178 = _load_output("phase178_icit_priority.json")

    p175_verdict  = p175.get("verdict", "UNKNOWN") if p175.get("available") is not False else "PENDING"
    p175_r        = p175.get("pearson_r_kl_vs_grammar", None) if p175.get("available") is not False else None
    m059_class    = p176.get("classification", "UNKNOWN") if p176.get("available") is not False else "PENDING"
    icit_priority = p178.get("icit_priority_list", []) if p178.get("available") is not False else []

    return {
        "phase175_grammar_kl_verdict": p175_verdict,
        "phase175_pearson_r":          p175_r,
        "phase176_m059_classification": m059_class,
        "icit_priority_phonemes":       icit_priority[:10] if icit_priority else [],
        "json": {
            "p175_verdict": p175_verdict, "p175_r": p175_r,
            "m059": m059_class,
            "icit_n_targets": len(icit_priority),
        },
        "number": len(icit_priority),
        "text":   (f"Phase-175 grammar/KL correlation: {p175_verdict} (r={p175_r}). "
                   f"Phase-176 M059: {m059_class}. "
                   f"Phase-178 ICIT priority targets: {len(icit_priority)}."),
        "gpu_device": "cpu",
    }


# ── Node definitions ──────────────────────────────────────────────────────────

def _phase171_178_node_defs() -> list[AtomicNodeDef]:
    _STD = [
        {"name": "json",       "type": "json"},
        {"name": "number",     "type": "number"},
        {"name": "text",       "type": "text"},
        {"name": "gpu_device", "type": "text"},
    ]
    return [
        AtomicNodeDef(
            id="IndusNetworkCentrality171",
            name="Network Centrality Validation (P171)",
            category="Indus Decipherment",
            description=(
                "Phase-171: independent validation of Roif's betweenness centrality claim "
                "that MEDIAL signs M099 and M267 are structural bridge nodes in the IVS "
                "co-occurrence network. Three-way analysis: Roif graph, our independent "
                "phase-142 bigram graph, and edge cross-validation. "
                "Outputs bridge_node_claim: CONFIRMED / PARTIAL / NOT_CONFIRMED."
            ),
            inputs=[],
            outputs=[
                {"name": "bridge_node_claim",   "type": "text"},
                {"name": "M099_rank_our_graph", "type": "number"},
                {"name": "M267_rank_our_graph", "type": "number"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_network_centrality_171,
        ),
        AtomicNodeDef(
            id="IndusBetweennessStratification172_174",
            name="Betweenness Stratification (P172-174)",
            category="Indus Decipherment",
            description=(
                "Phases 172-174: full H+M×H+M betweenness centrality on all 161 H+M signs "
                "(Phase-172); betweenness check on the 18 irresolvable MEDIAL signs from "
                "Phase-168, testing whether BC=0 predicts name-syllable status (Phase-173); "
                "betweenness-filtered Meluhhan name phonological coverage with absent-phoneme "
                "gap analysis for ICIT targeting (Phase-174)."
            ),
            inputs=[],
            outputs=[
                {"name": "n_grammar_candidates",       "type": "number"},
                {"name": "n_name_syllable_candidates", "type": "number"},
                {"name": "phase173_verdict",           "type": "text"},
                {"name": "top_meluhhan_coverage",      "type": "json"},
                {"name": "absent_phonemes",            "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_betweenness_stratification_172_174,
        ),
        AtomicNodeDef(
            id="IndusNetworkDeep175_178",
            name="Network Deep Dive (P175-178)",
            category="Indus Decipherment",
            description=(
                "Phases 175-178: site-stratified grammar/name proportion proxy testing "
                "Roif's peripheral-sites prediction (Phase-175); M059 bridge-role analysis "
                "— INITIAL hub vs MEDIAL bridge (Phase-176); full BC-to-slot mapping for "
                "all 161 H+M signs (Phase-177); ICIT-priority phoneme targeting — maps "
                "absent phonemes to LOW-confidence sign candidates (Phase-178). "
                "Requires Phase-172 output."
            ),
            inputs=[],
            outputs=[
                {"name": "phase175_grammar_kl_verdict",  "type": "text"},
                {"name": "phase175_pearson_r",           "type": "number"},
                {"name": "phase176_m059_classification", "type": "text"},
                {"name": "icit_priority_phonemes",       "type": "json"},
                *_STD,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_network_deep_175_178,
        ),
    ]
