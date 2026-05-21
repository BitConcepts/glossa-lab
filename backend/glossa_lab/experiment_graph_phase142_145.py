"""Experiment Graph atomic nodes for Phases 142–145.

Nodes:
  IndusCollocateNetwork   — Phase-142 (collocate network, INITIAL vocabulary)
  IndusIconographicFormula — Phase-143 (iconographic formula, blocking signs, CISI comparison)
  IndusDeepDive144        — Phase-144/145 (semantic deep dive, cluster analysis)
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


# ── Phase-142: Collocate Network ──────────────────────────────────────────────

def _collocate_network(inputs: dict, params: dict) -> dict[str, Any]:
    """Load Phase-142 collocate network + INITIAL sign vocabulary analysis."""
    report = _load_report("phase142_collocate_network.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase142_collocate_network.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0, "text": "Error", "gpu_device": "cpu"}
        report = _load_report("phase142_collocate_network.json")
    n_edges       = report.get("n_collocate_edges", 0)
    initial_vocab = report.get("initial_vocabulary", [])
    top_pairs     = report.get("top_collocate_pairs", [])
    return {
        "n_collocate_edges": n_edges,
        "initial_vocabulary": initial_vocab,
        "top_collocate_pairs": top_pairs,
        "json": {"edges": n_edges, "initial_vocab": initial_vocab},
        "number": float(n_edges),
        "text": (f"Phase-142: {n_edges} collocate edges; "
                 f"{len(initial_vocab)} INITIAL vocabulary signs."),
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Phase-143: Iconographic Formula Analysis ──────────────────────────────────

def _iconographic_formula(inputs: dict, params: dict) -> dict[str, Any]:
    """Load Phase-143 iconographic formula analysis + blocking sign identification."""
    report = _load_report("phase143_iconographic_formula.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase143_iconographic_formula.py", timeout=300)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0, "text": "Error", "gpu_device": "cpu"}
        report = _load_report("phase143_iconographic_formula.json")
    formulas  = report.get("formula_types", [])
    blockers  = report.get("blocking_signs", [])
    cisi_hits = report.get("cisi_comparison_hits", 0)
    return {
        "formula_types":         formulas,
        "blocking_signs":        blockers,
        "cisi_comparison_hits":  cisi_hits,
        "json": {"formulas": formulas, "blockers": blockers, "cisi_hits": cisi_hits},
        "number": float(len(formulas)),
        "text": (f"Phase-143: {len(formulas)} formula types; "
                 f"{len(blockers)} blocking signs; {cisi_hits} CISI comparison hits."),
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Phase-144/145: Deep Dive ──────────────────────────────────────────────────

def _deep_dive_144(inputs: dict, params: dict) -> dict[str, Any]:
    """Load Phase-144/145 semantic deep dive and cluster analysis."""
    report = _load_report("phase144_145_deep_dive.json")
    if report.get("available") is False:
        run_result = _run_phase_script("phase144_145_deep_dive.py", timeout=600)
        if "error" in run_result:
            return {**run_result, "json": {}, "number": 0.0, "text": "Error", "gpu_device": "cpu"}
        report = _load_report("phase144_145_deep_dive.json")
    findings = report.get("key_findings", [])
    clusters = report.get("semantic_clusters", [])
    verdict  = report.get("verdict", "UNKNOWN")
    return {
        "key_findings":     findings,
        "semantic_clusters": clusters,
        "verdict":          verdict,
        "json": {"findings": findings, "clusters": clusters, "verdict": verdict},
        "number": float(len(findings)),
        "text": (f"Phase-144/145: {len(findings)} key findings, "
                 f"{len(clusters)} semantic clusters, verdict={verdict}."),
        "gpu_device": report.get("gpu_device", "cpu"),
    }


# ── Node definitions ──────────────────────────────────────────────────────────

def _phase142_145_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            id="IndusCollocateNetwork",
            name="Collocate Network (P142)",
            category="Indus Decipherment",
            description=(
                "Phase-142: sign collocate network analysis + INITIAL vocabulary identification. "
                "Returns collocate edge count, top pairs, and INITIAL-class vocabulary."
            ),
            inputs=[],
            outputs=[
                {"name": "n_collocate_edges",  "type": "number"},
                {"name": "initial_vocabulary", "type": "json"},
                {"name": "top_collocate_pairs","type": "json"},
                {"name": "json",               "type": "json"},
                {"name": "number",             "type": "number"},
                {"name": "text",               "type": "text"},
                {"name": "gpu_device",         "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_collocate_network,
        ),
        AtomicNodeDef(
            id="IndusIconographicFormula",
            name="Iconographic Formula Analysis (P143)",
            category="Indus Decipherment",
            description=(
                "Phase-143: iconographic formula classification + blocking sign identification "
                "across CISI corpus comparison. Returns formula types, blocker list, cross-corpus hits."
            ),
            inputs=[],
            outputs=[
                {"name": "formula_types",        "type": "json"},
                {"name": "blocking_signs",       "type": "json"},
                {"name": "cisi_comparison_hits", "type": "number"},
                {"name": "json",                 "type": "json"},
                {"name": "number",               "type": "number"},
                {"name": "text",                 "type": "text"},
                {"name": "gpu_device",           "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_iconographic_formula,
        ),
        AtomicNodeDef(
            id="IndusDeepDive144",
            name="Semantic Deep Dive (P144-145)",
            category="Indus Decipherment",
            description=(
                "Phase-144/145: semantic cluster deep dive and cross-source analysis. "
                "Returns key findings, semantic cluster groupings, and overall verdict."
            ),
            inputs=[],
            outputs=[
                {"name": "key_findings",      "type": "json"},
                {"name": "semantic_clusters", "type": "json"},
                {"name": "verdict",           "type": "text"},
                {"name": "json",              "type": "json"},
                {"name": "number",            "type": "number"},
                {"name": "text",              "type": "text"},
                {"name": "gpu_device",        "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_deep_dive_144,
        ),
    ]
