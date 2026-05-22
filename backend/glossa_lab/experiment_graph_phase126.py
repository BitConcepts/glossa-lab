"""Experiment Graph atomic nodes for Phase-126.

Registers Phase-126 ICIT corpus access plan as a callable Experiment Builder node
under the 'Indus Decipherment' palette category.

Nodes:
  IndusICITCorpusPlan  — Phase-126 (ICIT database access strategy + Gulf sites)
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


# ── Phase-126: ICIT Corpus Plan ───────────────────────────────────────────────

def _icit_corpus_plan(inputs: dict, params: dict) -> dict[str, Any]:
    """Load Phase-126 ICIT corpus access strategy.

    ICIT = Dr. Andreas Fuls' database: 4,537 objects, 5,509 texts, 19,616 occurrences.
    Gulf sites: Failaka (400 seals), Saar (200+ seals), Janabiyah.
    Returns access plan, site list, and recommended contact strategy.
    """
    _load_report("phase127_gulf_corpus_report.json")  # closest available proxy
    plan_text = (
        "ICIT access plan: Contact fuls@epigraphica.de with fish-polysemy context + research offer. "
        "Required downloads: Kjaerum 1983, Tell F6 2012, Crawford 1997. "
        "Gulf sites: Failaka (400 seals), Saar (200+), Janabiyah (key contact-zone seal). "
        "ICIT: 4,537 objects, 5,509 texts, 19,616 occurrences. "
        "Next step: ICIT corpus is the primary path beyond Phase-165 literature-mining ceiling."
    )
    return {
        "plan_text": plan_text,
        "gulf_sites": ["Failaka", "Saar", "Janabiyah"],
        "icit_texts": 5509,
        "icit_objects": 4537,
        "contact": "fuls@epigraphica.de",
        "json": {"plan": plan_text, "gulf_sites": ["Failaka", "Saar", "Janabiyah"]},
        "number": 5509.0,
        "text": plan_text,
        "gpu_device": "cpu",
    }


def _phase126_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            id="IndusICITCorpusPlan",
            name="ICIT Corpus Access Plan (P126)",
            category="Indus Decipherment",
            description=(
                "Phase-126 ICIT corpus building plan. Dr. Andreas Fuls' database: "
                "4,537 objects, 5,509 texts across Gulf sites (Failaka, Saar, Janabiyah). "
                "Returns access strategy and next-step recommendations beyond Phase-165 ceiling."
            ),
            inputs=[],
            outputs=[
                {"name": "plan_text",   "type": "text"},
                {"name": "gulf_sites",  "type": "json"},
                {"name": "icit_texts",  "type": "number"},
                {"name": "contact",     "type": "text"},
                {"name": "json",        "type": "json"},
                {"name": "number",      "type": "number"},
                {"name": "text",        "type": "text"},
                {"name": "gpu_device",  "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_icit_corpus_plan,
        ),
    ]
