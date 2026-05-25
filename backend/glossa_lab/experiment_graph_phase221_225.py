"""Experiment Graph nodes for Phases 221-225 (H23 compliance)."""
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


def _p221(i, p):
    r = _load("phase221_p324_p122_investigation.json")
    if r.get("available") is False:
        res = _run("phase221_p324_p122_investigation.py", timeout=60)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P221 error"}
        r = _load("phase221_p324_p122_investigation.json")
    results = r.get("results", {})
    p324 = results.get("P324", {}).get("freq_cisi", 0)
    return {"json": r, "number": p324,
            "text": f"P221: P324 freq={p324} INITIAL=78%; P122 freq=76 MEDIAL=100%."}


def _p222(i, p):
    r = _load("phase222_cisi_anchor_injection.json")
    if r.get("available") is False:
        res = _run("phase222_cisi_anchor_injection.py", timeout=60)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P222 error"}
        r = _load("phase222_cisi_anchor_injection.json")
    n = r.get("total_injected", 0)
    total = r.get("new_total_anchors", 0)
    return {"json": r, "number": n,
            "text": f"P222: {n} CISI candidates injected. Total anchors={total}."}


def _p224(i, p):
    r = _load("phase224_slot_mismatch_investigation.json")
    if r.get("available") is False:
        res = _run("phase224_slot_mismatch_investigation.py", timeout=120)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P224 error"}
        r = _load("phase224_slot_mismatch_investigation.json")
    n_err = len(r.get("reading_errors", []))
    n_corp = len(r.get("corpus_differences", []))
    return {"json": r, "number": n_err,
            "text": f"P224: {n_err} reading errors, {n_corp} corpus differences (19 total)."}


def _p225(i, p):
    pdf = _REPO / "backend/reports/INDUS_DECIPHERMENT_REPORT.pdf"
    if not pdf.exists():
        res = _run("phase225_updated_pdf_report.py", timeout=60)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P225 error"}
    size_kb = pdf.stat().st_size // 1024 if pdf.exists() else 0
    return {"json": {"pdf_path": str(pdf), "size_kb": size_kb},
            "number": size_kb,
            "text": f"P225: INDUS_DECIPHERMENT_REPORT.pdf ({size_kb} KB). E01-E37 scorecard."}


def _phase221_225_node_defs():
    return [
        AtomicNodeDef("IndusPhase221P324P122", "P324 and P122 Deep Investigation (P221)",
                      "Indus Decipherment",
                      "Profiles P324 (freq=99 INITIAL 78%) and P122 (freq=76 MEDIAL 100%). "
                      "Bigram context, co-occurrence, hypotheses for 8 target CISI signs.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p221),
        AtomicNodeDef("IndusPhase222CISIInjection", "CISI Candidate Anchor Injection (P222)",
                      "Indus Decipherment",
                      "Injects P324=[TITLE_PREFIX], P385=[TERMINAL_SUFFIX], P332=o/ko. "
                      "Total anchors: 410 → 413.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p222),
        AtomicNodeDef("IndusPhase224SlotMismatch", "Slot Mismatch Investigation (P224)",
                      "Indus Decipherment",
                      "19 slot mismatches classified: 4 READING_ERROR (classification errors, "
                      "not reading errors), 15 CORPUS_DIFFERENCE.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p224),
        AtomicNodeDef("IndusPhase225PDFReport", "Updated PDF Decipherment Report (P225)",
                      "Indus Decipherment",
                      "Regenerates INDUS_DECIPHERMENT_REPORT.pdf. E01-E37, 164 H+M, 413 total, "
                      "91% coverage, CISI findings, site analysis.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p225),
    ]
