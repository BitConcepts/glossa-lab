"""Experiment Graph Nodes: Phase-74–80 Indus Decipherment Pipeline.

  IndusM267Grammar     Phase-74: M267 formal grammar constraint test
  IndusLevitReadings   Phase-75: Levit 2010 Meluhha etymology validation
  IndusPlaceFormula    Phase-76: Place formula decipherment via DEDR geography
  IndusSAgreement      Phase-77: SA agreement rate analysis
  IndusSemanticCluster Phase-78: Semantic corpus clustering by formula type
  IndusAnchorGap       Phase-79: Anchor gap priority analysis
  IndusDedrRebus       Phase-80: DEDR rebus expansion with full crosswalk

MANDATORY: Created per H23 before any Phase-74-80 script execution.
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


# ── node functions ────────────────────────────────────────────────────────────

def _m267_grammar(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase74_m267_grammar_test.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"verdict": result.get("verdict","?"), "p_value": result.get("p_value",1.0),
            "promoted": result.get("m267_promoted",False), "json": result,
            "number": float(result.get("p_value",1.0)),
            "text": f"Phase-74: M267 grammar test. verdict={result.get('verdict','?')} p={result.get('p_value',1.0):.4f}.",
            "gpu_device": device}

def _levit_readings(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase75_levit_readings.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"n_validated": result.get("n_validated",0), "n_added": result.get("n_added_to_anchors",0),
            "validated": result.get("validated_readings",[]), "json": result,
            "number": float(result.get("n_validated",0)),
            "text": f"Phase-75: Levit validation. {result.get('n_validated',0)} confirmed, {result.get('n_added_to_anchors',0)} added.",
            "gpu_device": device}

def _place_formula(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase76_place_formula.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"n_matched": result.get("n_matched",0), "matches": result.get("matches",[]),
            "json": result, "number": float(result.get("n_matched",0)),
            "text": f"Phase-76: Place formulas. {result.get('n_matched',0)} matched to Dravidian geography.",
            "gpu_device": device}

def _sa_agreement(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase77_sa_agreement_analysis.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"agree_rate": result.get("overall_agreement_pct",0),
            "high_trust_proposals": result.get("high_trust_proposals",[]),
            "json": result, "number": float(result.get("overall_agreement_pct",0)),
            "text": f"Phase-77: SA agreement {result.get('overall_agreement_pct',0):.1f}%. {len(result.get('high_trust_proposals',[]))} high-trust proposals.",
            "gpu_device": device}

def _semantic_cluster(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase78_semantic_clustering.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"n_classified": result.get("n_classified",0), "type_dist": result.get("corpus_type_dist",{}),
            "site_variation": result.get("site_variation_found",False), "json": result,
            "number": float(result.get("n_classified",0)),
            "text": f"Phase-78: Classified {result.get('n_classified',0)} seals. Site variation={result.get('site_variation_found',False)}.",
            "gpu_device": device}

def _anchor_gap(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase79_anchor_gap_analysis.py")
    if "error" in result: return {**result, "gpu_device": device}
    return {"n_unread": result.get("n_unread_signs",0), "priority_list": result.get("priority_top20",[]),
            "json": result, "number": float(result.get("n_unread_signs",0)),
            "text": f"Phase-79: {result.get('n_unread_signs',0)} unread signs. Top priorities identified.",
            "gpu_device": device}

def _dedr_rebus(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase80_dedr_rebus_expansion.py")
    if "error" in result: return {**result, "gpu_device": device}
    n = result.get("n_new_anchors",0)
    return {"n_new_anchors": n, "new_anchors": result.get("new_anchors",[]),
            "json": result, "number": float(n),
            "text": f"Phase-80: DEDR rebus expansion. {n} new MEDIUM anchors added.",
            "gpu_device": device}


# ── node definitions ─────────────────────────────────────────────────────────

def _phase74_80_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415
    return [
        AtomicNodeDef(id="IndusM267Grammar", name="M267 Grammar Constraint Test",
            category="Indus Decipherment",
            description="Phase-74: Formal grammar test for M267=iN. Tests whether M267 appears between agent markers and titles at significantly higher-than-chance rates. CPU only.",
            inputs=[], outputs=[{"name":"verdict","type":"text"},{"name":"p_value","type":"number"},{"name":"promoted","type":"number"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_m267_grammar),
        AtomicNodeDef(id="IndusLevitReadings", name="Levit 2010 Readings Validation",
            category="Indus Decipherment",
            description="Phase-75: Validate 6 Dravidian readings from Levit 2010 Meluhha etymology study against DEDR and P56 crosswalk. Add confirmed ones as new anchors.",
            inputs=[], outputs=[{"name":"n_validated","type":"number"},{"name":"n_added","type":"number"},{"name":"validated","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_levit_readings),
        AtomicNodeDef(id="IndusPlaceFormula", name="Place Formula Decipherment",
            category="Indus Decipherment",
            description="Phase-76: Match 9 PLACE_FORMULA inscriptions to attested Dravidian geographic terms. Cross-reference with Tamil-Brahmi place names and DEDR.",
            inputs=[], outputs=[{"name":"n_matched","type":"number"},{"name":"matches","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_place_formula),
        AtomicNodeDef(id="IndusSAgreement", name="SA Agreement Rate Analysis",
            category="Indus Decipherment",
            description="Phase-77: Analyse which signs SA consistently agrees/disagrees with confirmed anchors. Identify high-trust SA proposals for unanchored signs. GPU: BigramScorer.",
            inputs=[], outputs=[{"name":"agree_rate","type":"number"},{"name":"high_trust_proposals","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_sa_agreement),
        AtomicNodeDef(id="IndusSemanticCluster", name="Semantic Corpus Clustering",
            category="Indus Decipherment",
            description="Phase-78: Classify all 1,670 Holdat seals by formula type using Phase-68 morphological role database. Test site-stratified formula distributions. GPU: torch.",
            inputs=[], outputs=[{"name":"n_classified","type":"number"},{"name":"type_dist","type":"json"},{"name":"site_variation","type":"number"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_semantic_cluster),
        AtomicNodeDef(id="IndusAnchorGap", name="Anchor Gap Priority Analysis",
            category="Indus Decipherment",
            description="Phase-79: Rank 227 unread signs by frequency x appears-in-decoded-formulas. Produces priority list for next anchor expansion sprint.",
            inputs=[], outputs=[{"name":"n_unread","type":"number"},{"name":"priority_list","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_anchor_gap),
        AtomicNodeDef(id="IndusDedrRebus", name="DEDR Rebus Expansion",
            category="Indus Decipherment",
            description="Phase-80: Apply rebus principle to signs with known iconography using 115 M<->P mappings. Target 10-15 new MEDIUM anchors from DEDR iconographic matches. GPU: torch.",
            inputs=[], outputs=[{"name":"n_new_anchors","type":"number"},{"name":"new_anchors","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_dedr_rebus),
    ]
