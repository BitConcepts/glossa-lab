"""Experiment graph node definitions for Phases 248–254.

Phase-248: Ceiling-breaker literature mine (identify actionable experiments)
Phase-249: Ceiling experiments design (allograph, semantic scope, commodity, LE vocab)
Phase-250/251: Full corpus allograph + commodity analysis
Phase-252: Allograph detection → 56 MEDIUM→HIGH upgrades (HIGH 105→125)
Phase-253: CISI allograph clustering (P-sign ↔ HIGH M-sign cross-corpus)
Phase-254: Seal-type semantic constraint analysis (motif-enriched MEDIUM→HIGH)
Phase-255: Trade commodity phoneme mapping (commodity PDr names → MEDIUM→HIGH)
Phase-256: Linear Elamite vocabulary extension (LE+DEDR triple corroboration)
"""
from __future__ import annotations

from glossa_lab.experiment_graph import AtomicNodeDef


def _phase_runner(script: str, output_json: str):
    """Factory for subprocess-based phase runners."""
    def _run(inputs: dict, params: dict) -> dict:
        try:
            import subprocess, sys  # noqa: PLC0415
            r = subprocess.run(
                [sys.executable, f"scripts/{script}"],
                capture_output=True, text=True, timeout=120,
                cwd=str(__import__("pathlib").Path(__file__).parents[2] / "backend"),
            )
            import json  # noqa: PLC0415
            from pathlib import Path  # noqa: PLC0415
            out = Path(__file__).parents[2] / "outputs" / output_json
            data = json.loads(out.read_text("utf-8")) if out.exists() else {}
            return {**{k: data.get(k) for k in list(data.keys())[:10]}, "stdout": r.stdout[-800:]}
        except Exception as exc:  # noqa: BLE001
            return {"error": str(exc)}
    return _run


def _phase248_254_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            "IndusPhase248CeilingMine",
            "Phase-248: Ceiling-Breaker Literature Mine",
            "Indus Decipherment",
            "Fetches ~2800 papers and identifies 5 actionable ceiling-cracking experiments: "
            "allograph detection (C1), semantic scope (C1), trade commodity phonology (C2), "
            "Linear Elamite vocabulary extension (C2), Munda substrate (C1).",
            inputs=[],
            outputs=[
                {"name": "ceiling_analysis", "type": "object"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase248_ceiling_breaker_mine.py", "phase248_ceiling_breaker_mine.json"),
        ),
        AtomicNodeDef(
            "IndusPhase249CeilingExperiments",
            "Phase-249: Ceiling Experiments Design",
            "Indus Decipherment",
            "Designs and evaluates 5 ceiling-cracking experiments from Phase-248 mine: "
            "Daggumati & Revesz allograph detection, semantic scope constraint SA, "
            "trade commodity phoneme mapping, Linear Elamite vocabulary extension, "
            "Munda phoneme constraint.",
            inputs=[],
            outputs=[
                {"name": "synthesis", "type": "object"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase249_ceiling_experiments.py", "phase249_ceiling_experiments.json"),
        ),
        AtomicNodeDef(
            "IndusPhase250AllographCommodity",
            "Phase-250/251: Allograph + Commodity Analysis",
            "Indus Decipherment",
            "Full corpus allograph detection via positional correlation matrix (390 signs). "
            "Identifies strong allograph pairs (r>=0.95) across Holdat corpus. "
            "Also maps commodity vocabulary to rare TERMINAL signs on trade seals.",
            inputs=[],
            outputs=[
                {"name": "phase_250_allograph", "type": "object"},
                {"name": "phase_251_commodity", "type": "object"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase250_251_allograph_commodity.py", "phase250_251_allograph_commodity.json"),
        ),
        AtomicNodeDef(
            "IndusPhase252AllographUpgrade",
            "Phase-252: Allograph Detection → HIGH Upgrades",
            "Indus Decipherment",
            "Applies allograph detection results to upgrade 56 MEDIUM→HIGH anchors. "
            "Signs sharing positional profiles (r>=0.90) with existing HIGH anchors "
            "inherit HIGH confidence. HIGH count: 105→125.",
            inputs=[],
            outputs=[
                {"name": "n_high_upgrades", "type": "number"},
                {"name": "upgrade_log", "type": "array"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase252_allograph_upgrade.py", "phase252_allograph_upgrade.json"),
        ),
        AtomicNodeDef(
            "IndusPhase253CISIAllograph",
            "Phase-253: CISI Allograph Clustering",
            "Indus Decipherment",
            "Cross-corpus allograph detection: correlates CISI P-sign positional profiles "
            "against HIGH Holdat M-sign profiles. CANDIDATE P-signs with r>=0.92 → MEDIUM; "
            "MEDIUM with r>=0.95 → HIGH. Extends allograph method to independent CISI corpus.",
            inputs=[],
            outputs=[
                {"name": "n_upgrades", "type": "number"},
                {"name": "upgrade_log", "type": "array"},
                {"name": "candidate_allographs", "type": "array"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase253_cisi_allograph.py", "phase253_cisi_allograph.json"),
        ),
        AtomicNodeDef(
            "IndusPhase254SemanticConstraint",
            "Phase-254: Seal-Type Semantic Constraint",
            "Indus Decipherment",
            "Motif-enrichment analysis: MEDIUM signs strongly associated with a seal motif "
            "(unicorn/zebu/elephant/rhino/tiger) have readings checked against the semantic "
            "domain of that motif. Domain-matched signs with chi2>6.64 and lift>2.0 → HIGH.",
            inputs=[],
            outputs=[
                {"name": "n_upgraded", "type": "number"},
                {"name": "upgrade_log", "type": "array"},
                {"name": "top_enrichments", "type": "array"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase254_semantic_constraint.py", "phase254_semantic_constraint.json"),
        ),
        AtomicNodeDef(
            "IndusPhase255CommodityPhonemes",
            "Phase-255: Trade Commodity Phoneme Mapping",
            "Indus Decipherment",
            "Maps 16 known Harappan trade commodities to Proto-Dravidian names, then "
            "cross-references MEDIUM signs on zebu/bull seals. Signs with commodity PDr "
            "reading match + trade-seal presence → MEDIUM→HIGH upgrade.",
            inputs=[],
            outputs=[
                {"name": "n_upgraded", "type": "number"},
                {"name": "upgrade_log", "type": "array"},
                {"name": "commodity_matches", "type": "array"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase255_commodity_phonemes.py", "phase255_commodity_phonemes.json"),
        ),
        AtomicNodeDef(
            "IndusPhase256LEExtension",
            "Phase-256: Linear Elamite Vocabulary Extension",
            "Indus Decipherment",
            "Extends Phase-235 Elamite bridge using Desset 2022 + 2025 LE data. "
            "MEDIUM signs with LE backing (E41) + DEDR + McAlpin triple corroboration "
            "→ MEDIUM→HIGH upgrade. Also maps extended LE phonemes against MEDIUM signs.",
            inputs=[],
            outputs=[
                {"name": "n_upgraded", "type": "number"},
                {"name": "upgrade_log", "type": "array"},
                {"name": "le_backed_medium", "type": "array"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase256_le_extension.py", "phase256_le_extension.json"),
        ),
    ]
