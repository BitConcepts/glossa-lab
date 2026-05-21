"""Experiment Graph Nodes: Phase-104–109 (path to 100% decipherment).

  IndusOCR            Phase-104: Mistral pixtral OCR of im77intro.pdf
  IndusNameSigns      Phase-105: Decode top 4 personal name signs
  IndusNameSASprint   Phase-106: Personal name SA sprint (all 45 candidates)
  IndusTBNameCheck    Phase-107: Tamil-Brahmi comparative name check
  IndusPhonExhaust    Phase-108: Phonological exhaustion sprint
  IndusAcadSubmit     Phase-109: Academic submission prep for Dr. Fuls
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"

def _get_device():
    from glossa_lab.gpu_utils import detect_device; return detect_device()

def _run(script, timeout=3600):
    s = _SCRIPTS / script; rp = _REPORTS / script.replace(".py",".json")
    if not s.exists(): return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(s)], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired: return {"error": f"timeout {timeout}s"}
    except Exception as e: return {"error": str(e)}
    if rp.exists():
        try: return json.loads(rp.read_text("utf-8"))
        except Exception: pass
    return {"ok": True}

def _phase104_109_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef
    specs = [
        ("IndusOCR", "Mahadevan PDF OCR (Mistral pixtral)", "phase104_ocr_mahadevan.py",
         "Phase-104: OCR im77intro.pdf using Mistral pixtral-12b vision API. Extracts sign descriptions and reading proposals. CPU+API."),
        ("IndusNameSigns", "Top Personal Name Signs Decoded", "phase105_name_signs.py",
         "Phase-105: Decode M024=ne and top-3 personal name signs (M362, M398, M375) using name-slot evidence + SA. CPU."),
        ("IndusNameSASprint", "Personal Name SA Sprint", "phase106_name_sa_sprint.py",
         "Phase-106: SA with 125 pinned anchors targets all 45 name candidates. Assigns SA modal readings. GPU."),
        ("IndusTBNameCheck", "Tamil-Brahmi Name Comparison", "phase107_tb_name_check.py",
         "Phase-107: Cross-reference name candidate readings against Tamil-Brahmi personal names in Sangam corpus. CPU."),
        ("IndusPhonExhaust", "Phonological Exhaustion Sprint", "phase108_phon_exhaustion.py",
         "Phase-108: Assign SA modal reading (PD-valid, threshold 1.0) to every unread sign with freq>=5. Sweeps remaining inventory. GPU."),
        ("IndusAcadSubmit", "Academic Submission Package (Dr. Fuls)", "phase109_academic_submit.py",
         "Phase-109: Format M293 proof letter, 50 translations, stats summary into Dr. Fuls outreach package. CPU."),
    ]
    nodes = []
    for nid, name, script, desc in specs:
        def fn(i, p, s=script): return {**_run(s), "gpu_device": _get_device()}
        nodes.append(AtomicNodeDef(id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name":"result","type":"json"},{"name":"gpu_device","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=fn))
    return nodes
