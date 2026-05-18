"""Experiment Graph Nodes: Phase-88–90 Indus Decipherment Pipeline.

  IndusLiteratureMine      Phase-88: 500-item targeted literature mine + extraction
  IndusDedrExpansion120    Phase-89: Systematic DEDR expansion to 120 HIGH+MEDIUM
  IndusScholarlyTranslations Phase-90: Scholarly-grade seal translations

MANDATORY: Created per H23 before any Phase-88-90 script execution.
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


def _run_phase_script(script_name: str, timeout: int = 1800) -> dict[str, Any]:
    script = _SCRIPTS / script_name
    report_stem = script_name.replace(".py", "")
    report_path = _REPORTS / f"{report_stem}.json"
    if not script.exists():
        return {"error": f"Script not found: {script_name}"}
    try:
        r = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=timeout,
            cwd=str(_REPO),
        )
        if r.returncode != 0:
            return {"error": f"Script failed (exit {r.returncode})",
                    "stderr": r.stderr[-500:], "stdout": r.stdout[-500:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Timed out after {timeout}s: {script_name}"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}
    if report_path.exists():
        try:
            return json.loads(report_path.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True, "stdout": r.stdout[-200:]}


def _literature_mine(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase88_literature_mine.py", timeout=1200)
    if "error" in result: return {**result, "gpu_device": device}
    n = result.get("n_papers_fetched", 0)
    nf = result.get("n_actionable_findings", 0)
    return {"n_papers": n, "n_findings": nf,
            "findings": result.get("actionable_findings", []),
            "json": result, "number": float(nf),
            "text": f"Phase-88: {n} papers mined, {nf} actionable findings.",
            "gpu_device": device}

def _dedr_expansion_120(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase89_dedr_systematic.py", timeout=600)
    if "error" in result: return {**result, "gpu_device": device}
    n = result.get("n_new_medium_anchors", 0)
    total = result.get("total_high_medium", 0)
    return {"n_new_anchors": n, "total_high_medium": total,
            "new_anchors": result.get("new_anchors", []),
            "json": result, "number": float(total),
            "text": f"Phase-89: +{n} anchors. Total HIGH+MEDIUM={total}.",
            "gpu_device": device}

def _scholarly_translations(inputs, params):
    device = _get_device()
    result = _run_phase_script("phase90_scholarly_translations.py", timeout=300)
    if "error" in result: return {**result, "gpu_device": device}
    n = result.get("n_translations", 0)
    return {"n_translations": n,
            "translations": result.get("translations", []),
            "json": result, "number": float(n),
            "text": f"Phase-90: {n} scholarly seal translations produced.",
            "gpu_device": device}


def _phase88_90_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415
    return [
        AtomicNodeDef(id="IndusLiteratureMine", name="Literature Mine + Extraction",
            category="Indus Decipherment",
            description="Phase-88: 500-item targeted literature mine across SemanticScholar, OpenAlex, CrossRef, EuropePMC. Queries: Indus Dravidian, Parpola sign reading, DEDR rebus, Mahadevan. Extracts: sign proposals, crosswalk entries, M293 evidence. Produces ranked actionable findings. Takes 5-10 min.",
            inputs=[], outputs=[{"name":"n_papers","type":"number"},{"name":"n_findings","type":"number"},{"name":"findings","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_literature_mine),
        AtomicNodeDef(id="IndusDedrExpansion120", name="DEDR Systematic Expansion to 120",
            category="Indus Decipherment",
            description="Phase-89: Systematic pass over all 390 Holdat signs vs Parpola 1994 App.B + full DEDR. Integrates Phase-88 mine findings. Target: 15 new MEDIUM anchors to reach 120 total HIGH+MEDIUM.",
            inputs=[], outputs=[{"name":"n_new_anchors","type":"number"},{"name":"total_high_medium","type":"number"},{"name":"new_anchors","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_dedr_expansion_120),
        AtomicNodeDef(id="IndusScholarlyTranslations", name="Scholarly Seal Translations",
            category="Indus Decipherment",
            description="Phase-90: Produce 5-10 publication-ready Indus seal translations with full DEDR citations, morphological analysis, formula type labels, confidence breakdown. Scholarly format suitable for academic communication.",
            inputs=[], outputs=[{"name":"n_translations","type":"number"},{"name":"translations","type":"json"},{"name":"gpu_device","type":"text"},{"name":"text","type":"text"}],
            params_schema={"type":"object","properties":{}}, fn=_scholarly_translations),
    ]
