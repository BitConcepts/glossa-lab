"""Experiment Graph nodes for Phases 216-220 (H23 compliance)."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
from glossa_lab.experiment_graph import AtomicNodeDef

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend" / "scripts"
_OUTPUTS = _REPO / "outputs"
_S = [{"name": "json", "type": "json"}, {"name": "number", "type": "number"}, {"name": "text", "type": "text"}]


def _run(script, timeout=900):
    p = _SCRIPTS / script
    if not p.exists():
        return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True,
                           timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"Exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    return {"status": "ok"}


def _load(name):
    p = _OUTPUTS / name
    if not p.exists():
        return {"available": False}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"available": False}


def _p216(i, p):
    r = _load("phase216_sa_recal_410anchors.json")
    if r.get("available") is False:
        res = _run("phase216_sa_recal_410anchors.py", timeout=1800)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P216 error"}
        r = _load("phase216_sa_recal_410anchors.json")
    upg = r.get("n_upgraded_to_high", 0)
    cov = r.get("hm_token_coverage", 0.0)
    return {"json": r, "number": upg, "text": f"P216: +{upg} HIGH upgrades, coverage={cov:.1%}"}


def _p218(i, p):
    r = _load("phase218_site_semantic_updated.json")
    if r.get("available") is False:
        res = _run("phase218_site_semantic_updated.py", timeout=300)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P218 error"}
        r = _load("phase218_site_semantic_updated.json")
    nf = r.get("total_fully_decoded", 0)
    return {"json": r, "number": nf, "text": f"P218: {nf}/1670 seals fully decoded"}


def _p219(i, p):
    r = _load("phase219_arxiv_updated.json")
    if r.get("available") is False:
        res = _run("phase219_arxiv_updated.py", timeout=30)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P219 error"}
        r = _load("phase219_arxiv_updated.json")
    return {"json": r, "number": r.get("n_evidence_items", 0),
            "text": f"P219: arXiv draft. {r.get('n_evidence_items', 0)} evidence items."}


def _p220(i, p):
    r = _load("phase220_parpola_cisi_crossref.json")
    if r.get("available") is False:
        res = _run("phase220_parpola_cisi_crossref.py", timeout=120)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P220 error"}
        r = _load("phase220_parpola_cisi_crossref.json")
    n_new = r.get("new_candidates", {}).get("total", 0)
    return {"json": r, "number": n_new, "text": f"P220: {n_new} new candidates from CISI."}


def _phase216_220_node_defs():
    return [
        AtomicNodeDef("IndusPhase216SARecal", "SA Recalibration 410 Anchors (P216)",
                      "Indus Decipherment",
                      "Re-runs SA with all 410 anchors. +29 HIGH upgrades. H+M coverage 91.0%.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p216),
        AtomicNodeDef("IndusPhase218SiteSemantic", "Site-Stratified Semantic Analysis (P218)",
                      "Indus Decipherment",
                      "9 sites; 1,165/1,670 seals fully decoded with 164 H+M anchors.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p218),
        AtomicNodeDef("IndusPhase219ArxivDraft", "arXiv Preprint Draft E01-E37 (P219)",
                      "Indus Decipherment",
                      "37-evidence-item preprint draft. E28 falsified. E36=CISI. E37=Courtallam.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p219),
        AtomicNodeDef("IndusPhase220PapolaCISI", "Parpola/CISI Cross-Reference (P220)",
                      "Indus Decipherment",
                      "181 CISI P-signs; 97 outside M77. P324 freq=99 INITIAL. 23 new candidates.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p220),
    ]
