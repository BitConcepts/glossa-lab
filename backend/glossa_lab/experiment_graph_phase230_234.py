"""Experiment graph node definitions for Phases 230–234.

Phase-230: Full all-data cross-reference matrix (indirect bilingual candidates)
Phase-231: Mine 5000 #6 — indirect bilingual / contact evidence focus
Phase-232: Indirect bilingual scoring + statistical substantiation (Fisher p-value)
Phase-233: Cultural & demographic movement analysis (aDNA, BRW, corridors)
Phase-234: P324 CISI deep-dive + LOW→MEDIUM upgrade attempt
"""
from __future__ import annotations

from glossa_lab.experiment_graph import AtomicNodeDef


def _phase230_runner(inputs: dict, params: dict) -> dict:
    try:
        import subprocess
        import sys  # noqa: PLC0415
        r = subprocess.run(
            [sys.executable, "scripts/phase230_cross_reference_matrix.py"],
            capture_output=True, text=True, timeout=120,
            cwd=str(__import__("pathlib").Path(__file__).parents[2] / "backend"),
        )
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415
        out = Path(__file__).parents[2] / "outputs" / "phase230_cross_reference_matrix.json"
        data = json.loads(out.read_text("utf-8")) if out.exists() else {}
        return {"verdict": data.get("verdict", ""), "n_candidates": data.get("n_indirect_bilingual_candidates", 0),
                "fisher_p": data.get("fisher_combined_p", None), "stdout": r.stdout[-800:]}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def _phase231_runner(inputs: dict, params: dict) -> dict:
    try:
        import subprocess
        import sys  # noqa: PLC0415
        r = subprocess.run(
            [sys.executable, "scripts/phase231_indirect_bilingual_mine.py"],
            capture_output=True, text=True, timeout=900,
            cwd=str(__import__("pathlib").Path(__file__).parents[2] / "backend"),
        )
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415
        out = Path(__file__).parents[2] / "outputs" / "phase231_indirect_bilingual_mine.json"
        data = json.loads(out.read_text("utf-8")) if out.exists() else {}
        return {"verdict": data.get("verdict", ""), "n_papers": data.get("total_papers_fetched", 0),
                "n_strong": data.get("n_strong_evidence", 0), "stdout": r.stdout[-800:]}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def _phase232_runner(inputs: dict, params: dict) -> dict:
    try:
        import subprocess
        import sys  # noqa: PLC0415
        r = subprocess.run(
            [sys.executable, "scripts/phase232_indirect_bilingual_scoring.py"],
            capture_output=True, text=True, timeout=120,
            cwd=str(__import__("pathlib").Path(__file__).parents[2] / "backend"),
        )
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415
        out = Path(__file__).parents[2] / "outputs" / "phase232_indirect_bilingual_scoring.json"
        data = json.loads(out.read_text("utf-8")) if out.exists() else {}
        return {"verdict": data.get("verdict", ""), "fisher_p": data.get("fisher_combined_p", None),
                "n_phonemes_addressed": data.get("n_absent_phonemes_addressed", 0),
                "chain_quality": data.get("evidence_chain", {}).get("chain_quality", ""),
                "stdout": r.stdout[-800:]}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def _phase233_runner(inputs: dict, params: dict) -> dict:
    try:
        import subprocess
        import sys  # noqa: PLC0415
        r = subprocess.run(
            [sys.executable, "scripts/phase233_cultural_demographic_analysis.py"],
            capture_output=True, text=True, timeout=120,
            cwd=str(__import__("pathlib").Path(__file__).parents[2] / "backend"),
        )
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415
        out = Path(__file__).parents[2] / "outputs" / "phase233_cultural_demographic_analysis.json"
        data = json.loads(out.read_text("utf-8")) if out.exists() else {}
        lsp = data.get("language_survival_probability", {})
        return {"verdict": data.get("verdict", ""),
                "language_survival_probability": lsp.get("posterior_estimate", 0),
                "confidence": lsp.get("confidence", ""),
                "combined_pdr_to_tamil": data.get("combined_probability_pdr_to_tamil", 0),
                "stdout": r.stdout[-800:]}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def _phase234_runner(inputs: dict, params: dict) -> dict:
    try:
        import subprocess
        import sys  # noqa: PLC0415
        r = subprocess.run(
            [sys.executable, "scripts/phase234_p324_cisi_expansion.py"],
            capture_output=True, text=True, timeout=120,
            cwd=str(__import__("pathlib").Path(__file__).parents[2] / "backend"),
        )
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415
        out = Path(__file__).parents[2] / "outputs" / "phase234_p324_cisi_expansion.json"
        data = json.loads(out.read_text("utf-8")) if out.exists() else {}
        return {"verdict": data.get("verdict", ""),
                "p324_best_reading": data.get("cisi_p324_summary", {}).get("best_reading_proposal", ""),
                "n_medium_proposals": data.get("n_proposed_medium", 0),
                "n_low_strong_proposals": data.get("n_proposed_low_strong", 0),
                "stdout": r.stdout[-800:]}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def _phase230_234_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            "IndusPhase230CrossRefMatrix",
            "Phase-230: Full Cross-Reference Matrix",
            "Indus Decipherment",
            "Synthesise all Phase 1–229 outputs into a unified evidence matrix. "
            "Identify and rank all indirect bilingual candidates (A–H categories). "
            "Cross-reference anchors × sites × DNA × Mesopotamian contact × CISI grammar.",
            inputs=[],
            outputs=[
                {"name": "verdict", "type": "text"},
                {"name": "n_candidates", "type": "number"},
                {"name": "fisher_p", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase230_runner,
        ),
        AtomicNodeDef(
            "IndusPhase231IndirectBilingualMine",
            "Phase-231: Indirect Bilingual Mine 5000 (#6)",
            "Indus Decipherment",
            "Bulk mine 5000 papers targeting indirect bilingual / contact evidence: "
            "Shu-ilishu seal, Gulf seals, Sanskrit substrate loanwords, Elamo-Dravidian, "
            "Vedic river-name substrates, Harappan weight system, BRW continuity, "
            "aDNA AASI corridors, Keezhadi 2024/2025, Tamil-Brahmi onomastics.",
            inputs=[],
            outputs=[
                {"name": "verdict", "type": "text"},
                {"name": "n_papers", "type": "number"},
                {"name": "n_strong", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase231_runner,
        ),
        AtomicNodeDef(
            "IndusPhase232IndirectBilingualScoring",
            "Phase-232: Indirect Bilingual Scoring",
            "Indus Decipherment",
            "Multi-vector scoring of all indirect bilingual candidates. "
            "Fisher combined p-value, evidence chain quality, phoneme coverage, "
            "anchor corroboration count. Generates paper Section 4.5 text.",
            inputs=[],
            outputs=[
                {"name": "verdict", "type": "text"},
                {"name": "fisher_p", "type": "number"},
                {"name": "n_phonemes_addressed", "type": "number"},
                {"name": "chain_quality", "type": "text"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase232_runner,
        ),
        AtomicNodeDef(
            "IndusPhase233CulturalDemographic",
            "Phase-233: Cultural & Demographic Analysis",
            "Indus Decipherment",
            "Statistical model of Harappan population movement: aDNA corridors, "
            "BRW cultural chain, Keezhadi literacy timeline, collapse dispersal model, "
            "Bayesian language survival probability. 4 migration corridors (C1–C4).",
            inputs=[],
            outputs=[
                {"name": "verdict", "type": "text"},
                {"name": "language_survival_probability", "type": "number"},
                {"name": "confidence", "type": "text"},
                {"name": "combined_pdr_to_tamil", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase233_runner,
        ),
        AtomicNodeDef(
            "IndusPhase234P324CISIExpansion",
            "Phase-234: P324 Deep-Dive + CISI Upgrades",
            "Indus Decipherment",
            "Full context analysis of P324 (freq=99, INITIAL 78%) — the most frequent "
            "undeciphered CISI-exclusive sign. Reading proposals (kuṭi/koṟ/eṉ/taṉ). "
            "LOW→MEDIUM upgrade attempt for all 243 LOW anchors using CISI cross-corpus.",
            inputs=[],
            outputs=[
                {"name": "verdict", "type": "text"},
                {"name": "p324_best_reading", "type": "text"},
                {"name": "n_medium_proposals", "type": "number"},
                {"name": "n_low_strong_proposals", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase234_runner,
        ),
    ]
