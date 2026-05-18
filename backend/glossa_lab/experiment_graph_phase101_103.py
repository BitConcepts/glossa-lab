"""Experiment Graph Nodes: Phase-101–103.

  IndusM293Iconic     Phase-101: M293 definitive iconographic analysis
  IndusParpolaPDF     Phase-102: pdfplumber Parpola/Mahadevan PDF extraction
  IndusNameLexicon    Phase-103: Personal name lexicon from positional patterns
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"

def _get_device():
    from glossa_lab.gpu_utils import detect_device; return detect_device()

def _run(script, timeout=1800):
    s = _SCRIPTS / script; rp = _REPORTS / script.replace(".py",".json")
    if not s.exists(): return {"error": f"Script not found: {script}"}
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

def _phase101_103_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef
    specs = [
        ("IndusM293Iconic", "M293 Definitive Iconographic Analysis", "phase101_m293_iconographic.py",
         "Phase-101: Combines positional evidence, PDF extraction, and SemanticScholar search to give a defensible final verdict on M293=ta vs vil. CPU."),
        ("IndusParpolaPDF", "Parpola/Mahadevan PDF Table Extraction", "phase102_pdf_extraction.py",
         "Phase-102: Uses pdfplumber to extract sign tables from im77intro.pdf and other available PDFs. Maps sign numbers to readings. CPU."),
        ("IndusNameLexicon", "Personal Name Lexicon", "phase103_name_lexicon.py",
         "Phase-103: Identifies personal name slots ([M267]-[X]-[SUFFIX], [ANIMAL]-[X]-[TITLE]-[SUFFIX]). Builds frequency table of name candidates. CPU."),
    ]
    nodes = []
    for nid, name, script, desc in specs:
        def fn(i, p, s=script): return {**_run(s), "gpu_device": _get_device()}
        nodes.append(AtomicNodeDef(id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name":"result","type":"json"},{"name":"gpu_device","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=fn))
    return nodes
