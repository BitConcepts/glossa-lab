"""Experiment Graph node for Phase 183: bulk mine 5000."""
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

def _run(script: str, timeout: int = 1800) -> dict[str, Any]:
    p = _SCRIPTS / script
    if not p.exists(): return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0: return {"error": f"Exit {r.returncode}", "stderr": r.stderr[-500:]}
    except subprocess.TimeoutExpired: return {"error": f"Timeout after {timeout}s"}
    except Exception as exc: return {"error": str(exc)}
    return {"status": "ok"}

def _load(json_name: str) -> dict[str, Any]:
    p = _OUTPUTS / json_name
    if not p.exists(): return {"available": False}
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {"available": False}

def _bulk_mine_183(inputs: dict, params: dict) -> dict[str, Any]:
    report = _load("phase183_bulk_mine_5000.json")
    if report.get("available") is False:
        res = _run("phase183_bulk_mine_5000.py", timeout=1800)
        if "error" in res:
            return {**res, "json": {}, "number": 0.0, "text": "Phase-183 error", "gpu_device": "cpu"}
        report = _load("phase183_bulk_mine_5000.json")
    n = report.get("n_papers", 0)
    ns = report.get("n_strong_evidence", 0)
    nm = report.get("n_moderate_evidence", 0)
    total = report.get("total_papers_mined_all_phases", 0)
    return {
        "n_papers": n, "n_strong": ns, "n_moderate": nm,
        "total_all_phases": total,
        "strong_evidence": report.get("evidence", {}).get("strong", [])[:10],
        "sign_proposals":  report.get("evidence", {}).get("sign_proposals", []),
        "json": {"n": n, "ns": ns, "nm": nm},
        "number": ns + nm,
        "text": f"Phase-183 bulk mine: {n} papers. {ns} STRONG, {nm} MODERATE. Total across all mines: {total}.",
        "gpu_device": "cpu",
    }

def _phase183_node_defs() -> list[AtomicNodeDef]:
    _STD = [{"name": "json","type":"json"},{"name":"number","type":"number"},{"name":"text","type":"text"},{"name":"gpu_device","type":"text"}]
    return [AtomicNodeDef(
        id="IndusBulkMine183",
        name="Bulk Mine 5000 (P183)",
        category="Indus Decipherment",
        description=(
            "Phase-183: bulk mine 5000 papers via 5 high-volume tracks: "
            "OpenAlex paginated bulk (200/page × 8 pages × 21 queries), "
            "CrossRef (100/query × 15 queries), S2 deep pagination (50/page × 5 × 12), "
            "arXiv expanded (30 queries × 50), Wikipedia citation extraction (13 articles). "
            "Evidence classification: STRONG/MODERATE/WEAK + sign proposal extraction."
        ),
        inputs=[],
        outputs=[
            {"name":"n_papers","type":"number"},
            {"name":"n_strong","type":"number"},
            {"name":"n_moderate","type":"number"},
            {"name":"total_all_phases","type":"number"},
            {"name":"strong_evidence","type":"json"},
            {"name":"sign_proposals","type":"json"},
            *_STD,
        ],
        params_schema={"type":"object","properties":{}},
        fn=_bulk_mine_183,
    )]
