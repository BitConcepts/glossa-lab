"""Experiment Graph nodes for Phases 196-201."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from typing import Any
from glossa_lab.experiment_graph import AtomicNodeDef

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend" / "scripts"
_OUTPUTS = _REPO / "outputs"


def _run(script, timeout=900):
    p = _SCRIPTS / script
    if not p.exists(): return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0: return {"error": f"Exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired: return {"error": f"Timeout {timeout}s"}
    except Exception as e: return {"error": str(e)}
    return {"status": "ok"}


def _load(name):
    p = _OUTPUTS / name
    if not p.exists(): return {"available": False}
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {"available": False}


def _mine196(i, p):
    r = _load("phase196_bulk_mine_5000.json")
    if r.get("available") is False:
        res = _run("phase196_bulk_mine_5000.py", timeout=1800)
        if "error" in res: return {**res, "number": 0.0, "text": "P196 error"}
        r = _load("phase196_bulk_mine_5000.json")
    ns, nm = r.get("n_strong_evidence",0), r.get("n_moderate_evidence",0)
    return {"n_strong": ns, "n_moderate": nm, "total": r.get("total_papers_mined_all_phases",0),
            "json": {"ns": ns, "nm": nm}, "number": ns, "text": f"P196: {ns} STRONG + {nm} MODERATE. Total: {r.get('total_papers_mined_all_phases',0)}"}


def _top8(i, p):
    r = _load("phase197_top8_unanchored_analysis.json")
    if r.get("available") is False:
        res = _run("phase197_top8_unanchored_analysis.py", timeout=600)
        if "error" in res: return {**res, "number": 0.0, "text": "P197 error"}
        r = _load("phase197_top8_unanchored_analysis.json")
    na = len(r.get("absent_candidates", []))
    nu = len(r.get("upgrade_candidates", []))
    return {"absent_candidates": r.get("absent_candidates",[]), "upgrade_candidates": r.get("upgrade_candidates",[]),
            "top8_analysis": r.get("top8_analysis",[]),
            "json": {"absent": na, "upgrades": nu}, "number": na, "text": f"P197: {na} absent hits, {nu} upgrade candidates. {r.get('verdict','')}"}


def _dedr198(i, p):
    r = _load("phase198_dedr_absent_lookup.json")
    if r.get("available") is False:
        res = _run("phase198_dedr_absent_lookup.py", timeout=60)
        if "error" in res: return {**res, "number": 0.0, "text": "P198 error"}
        r = _load("phase198_dedr_absent_lookup.json")
    nr = len(r.get("priority_ranking", []))
    return {"priority_ranking": r.get("priority_ranking",[]), "absent_analysis": r.get("absent_phoneme_analysis",[]),
            "json": {"n_ranked": nr}, "number": nr, "text": f"P198 DEDR: {nr} absent phonemes ranked. {r.get('verdict','')}"}


def _triple199(i, p):
    r = _load("phase199_triple_lm_convergence.json")
    if r.get("available") is False:
        res = _run("phase199_triple_lm_convergence.py", timeout=600)
        if "error" in res: return {**res, "number": 0.0, "text": "P199 error"}
        r = _load("phase199_triple_lm_convergence.json")
    nc = r.get("n_convergent", 0)
    na = r.get("n_absent_convergent", 0)
    return {"convergent_signs": r.get("convergent_signs",[]), "absent_convergent": r.get("absent_convergent",[]),
            "lm_results": r.get("lm_results",[]),
            "json": {"convergent": nc, "absent": na}, "number": nc, "text": f"P199 Triple-LM: {nc} convergent, {na} absent. {r.get('verdict','')}"}


def _allograph200(i, p):
    r = _load("phase200_allograph_direction.json")
    if r.get("available") is False:
        res = _run("phase200_allograph_direction.py", timeout=300)
        if "error" in res: return {**res, "number": 0.0, "text": "P200 error"}
        r = _load("phase200_allograph_direction.json")
    na = r.get("n_allograph_candidates", 0)
    alph = r.get("alphabet_test", {})
    return {"allograph_candidates": r.get("allograph_candidates",[]), "alphabet_test": alph,
            "direction_test": r.get("direction_test",{}),
            "json": {"allographs": na}, "number": na, "text": f"P200: {na} allograph candidates. {r.get('verdict','')}"}


def _inscriptions201(i, p):
    r = _load("phase201_inscription_reading_test.json")
    if r.get("available") is False:
        res = _run("phase201_inscription_reading_test.py", timeout=120)
        if "error" in res: return {**res, "number": 0.0, "text": "P201 error"}
        r = _load("phase201_inscription_reading_test.json")
    cov = r.get("mean_coverage", 0)
    return {"mean_coverage": cov, "pattern_distribution": r.get("pattern_distribution",{}),
            "sample_transcriptions": r.get("sample_transcriptions",[])[:10],
            "fully_readable_all": r.get("fully_readable_all",0),
            "json": {"coverage": cov}, "number": cov, "text": f"P201: mean coverage={cov*100:.1f}%. {r.get('verdict','')}"}


def _phase196_201_node_defs():
    S = [{"name":"json","type":"json"},{"name":"number","type":"number"},{"name":"text","type":"text"}]
    return [
        AtomicNodeDef("IndusMine196","Mine 5000 P196 (McAlpin/Brahui/aDNA)","Indus Decipherment",
            "Phase-196: Third bulk mine targeting McAlpin follow-up, Brahui contact, aDNA 2024-2026, Zvelebil/Krishnamurti, Dravidian substrate, script direction. 186 STRONG papers.",
            [],outputs=[{"name":"n_strong","type":"number"},{"name":"n_moderate","type":"number"},*S],
            params_schema={"type":"object","properties":{}},fn=_mine196),
        AtomicNodeDef("IndusTop8Analysis197","Top-8 Unanchored Sign Analysis (P197)","Indus Decipherment",
            "Phase-197: Deep SA analysis of the 8 highest-frequency unanchored M77 signs (700,520,481,692,861,820,817,858). 10-seed SA, DEDR cross-reference, absent phoneme check.",
            [],outputs=[{"name":"absent_candidates","type":"json"},{"name":"upgrade_candidates","type":"json"},{"name":"top8_analysis","type":"json"},*S],
            params_schema={"type":"object","properties":{}},fn=_top8),
        AtomicNodeDef("IndusDEDRLookup198","DEDR Absent Phoneme Lookup (P198)","Indus Decipherment",
            "Phase-198: Systematic DEDR lookup for 9 blocked absent phonemes. Finds top Tamil/PDr roots, computes sign candidates, scores by Elamite tier + SA stability.",
            [],outputs=[{"name":"priority_ranking","type":"json"},{"name":"absent_analysis","type":"json"},*S],
            params_schema={"type":"object","properties":{}},fn=_dedr198),
        AtomicNodeDef("IndusTripleLM199","Triple-LM Convergence (P199)","Indus Decipherment",
            "Phase-199: Runs SA with Tamil, North Dravidian, and Proto-Dravidian LMs. Signs where all 3 converge = strongest anchor candidates.",
            [],outputs=[{"name":"convergent_signs","type":"json"},{"name":"absent_convergent","type":"json"},{"name":"lm_results","type":"json"},*S],
            params_schema={"type":"object","properties":{}},fn=_triple199),
        AtomicNodeDef("IndusAllograph200","Allograph Detection + Direction (P200)","Indus Decipherment",
            "Phase-200: Detects allograph pairs (different sign forms, same phoneme) using Correa 2021 method. Falsifies 'Alphabet' hypothesis. Tests script direction.",
            [],outputs=[{"name":"allograph_candidates","type":"json"},{"name":"alphabet_test","type":"json"},{"name":"direction_test","type":"json"},*S],
            params_schema={"type":"object","properties":{}},fn=_allograph200),
        AtomicNodeDef("IndusInscriptionReading201","Inscription Reading Test (P201)","Indus Decipherment",
            "Phase-201: Tests complete inscription transcription using 100% title formula. Finds inscriptions with /en/ (M427), measures reading coverage, identifies Dravidian title patterns.",
            [],outputs=[{"name":"mean_coverage","type":"number"},{"name":"pattern_distribution","type":"json"},{"name":"sample_transcriptions","type":"json"},*S],
            params_schema={"type":"object","properties":{}},fn=_inscriptions201),
    ]
