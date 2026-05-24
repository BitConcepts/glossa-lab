"""Experiment Graph nodes for Phases 226-228 (H23 compliance)."""
from __future__ import annotations
import json, subprocess, sys
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


def _p226(i, p):
    r = _load("phase226_p122_phonetic.json")
    if r.get("available") is False:
        res = _run("phase226_p122_phonetic.py", timeout=60)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P226 error"}
        r = _load("phase226_p122_phonetic.json")
    top = r.get("top_candidate", {})
    return {"json": r, "number": top.get("score", 0),
            "text": f"P226: P122='{top.get('reading','')}' DEDR {top.get('dedr','')} score={top.get('score',0)}."}


def _p227(i, p):
    r = _load("phase227_p324_p332_formula.json")
    if r.get("available") is False:
        res = _run("phase227_p324_p332_formula.py", timeout=60)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P227 error"}
        r = _load("phase227_p324_p332_formula.json")
    n = r.get("formula_count", 0)
    return {"json": r, "number": n, "text": f"P227: [P324][P332] formula count={n}."}


def _p228(i, p):
    r = _load("phase228_cisi_tripartite.json")
    if r.get("available") is False:
        res = _run("phase228_cisi_tripartite.py", timeout=120)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P228 error"}
        r = _load("phase228_cisi_tripartite.json")
    rate = r.get("formula_rate", 0)
    lift = r.get("lift_vs_null", 0)
    return {"json": r, "number": rate,
            "text": f"P228: CISI tripartite rate={rate:.1%} ({lift:.0f}x null)."}


def _phase226_228_node_defs():
    return [
        AtomicNodeDef("IndusPhase226P122Phonetic", "P122 Phonetic Value Determination (P226)",
                      "Indus Decipherment",
                      "Determines phonetic value candidates for P122 (MEDIAL 100%, freq=76). "
                      "Top candidate: 'pa' (DEDR 4265). Formula [P364][P122][P385] analysed.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p226),
        AtomicNodeDef("IndusPhase227P324Formula", "[P324][P332] Title Formula Analysis (P227)",
                      "Indus Decipherment",
                      "Maps the [P324][P332] CISI title formula — equivalent of [M267][M099] in Holdat. "
                      "Full bigram frequency, dominance ratio, and grammar model.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p227),
        AtomicNodeDef("IndusPhase228CISITripartite", "CISI Tripartite Grammar Test (P228)",
                      "Indus Decipherment",
                      "Runs I→M→T tripartite grammar test on 178 CISI inscriptions. "
                      "Independent cross-corpus validation of Dravidian suffix model.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p228),
    ]
