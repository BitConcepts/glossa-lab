"""Experiment graph node definitions for Phases 295-297.

Phase-295: Bulk mine 5000 (May 2026 focus)
Phase-296: Mine cross-reference against anchor model
Phase-297: Full decipherment gap analysis
"""
from __future__ import annotations
import subprocess, sys, json
from pathlib import Path
from glossa_lab.experiment_graph import AtomicNodeDef

_BACKEND = str(Path(__file__).parents[1])

def _make_runner(script: str):
    def _runner(inputs: dict, params: dict) -> dict:
        try:
            r = subprocess.run(
                [sys.executable, f"scripts/{script}"],
                capture_output=True, text=True, timeout=600, cwd=_BACKEND,
            )
            out_name = script.replace(".py", ".json")
            for d in [Path(__file__).parents[2] / "outputs"]:
                p = d / out_name
                if p.exists():
                    return json.loads(p.read_text("utf-8"))
            return {"stdout": r.stdout[-500:], "rc": r.returncode}
        except Exception as exc:
            return {"error": str(exc)}
    return _runner

def _phase295_297_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            "IndusPhase295BulkMine", "Phase-295 Bulk Mine 5000",
            "Indus Decipherment",
            "May 2026 bulk mine: 3,359 papers from 5 APIs. "
            "92 STRONG, 85 MODERATE, 1,130 recent (2024+). "
            "Targets emailed researchers (Rao, Fuls, Nair, Sproat, Parpola, "
            "Renganathan, Murugaiyan, Kobayashi, Kolichala).",
            inputs=[], outputs=[{"name": "report", "type": "object"}],
            params_schema={"type": "object", "properties": {}},
            fn=_make_runner("phase295_bulk_mine_5000.py"),
        ),
        AtomicNodeDef(
            "IndusPhase296MineCrossref", "Phase-296 Mine Cross-Reference",
            "Indus Decipherment",
            "Cross-references STRONG papers from Phase 295 mine against "
            "our 605-sign anchor model. Categorizes as confirmations, "
            "contradictions, methodological, novel evidence, or false positives.",
            inputs=[], outputs=[{"name": "report", "type": "object"}],
            params_schema={"type": "object", "properties": {}},
            fn=_make_runner("phase296_297_mine_crossref_gap.py"),
        ),
        AtomicNodeDef(
            "IndusPhase297GapAnalysis", "Phase-297 Full Gap Analysis",
            "Indus Decipherment",
            "Comprehensive decipherment gap analysis: confidence distribution, "
            "allograph ratio, phonological inventory, blockers to 100% verified "
            "decipherment, and roadmap to peer-reviewed publication.",
            inputs=[], outputs=[{"name": "report", "type": "object"}],
            params_schema={"type": "object", "properties": {}},
            fn=_make_runner("phase296_297_mine_crossref_gap.py"),
        ),
    ]
