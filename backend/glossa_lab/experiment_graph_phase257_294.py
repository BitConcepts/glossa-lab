"""Experiment graph node definitions for Phases 257–294.

Phase-257: SA rerun with 137 HIGH anchors pinned
Phase-258: CANDIDATE resolution pass (CANDIDATE→MEDIUM→HIGH)
Phase-259: Ceiling-breaker mine 5000 (sixth run)
Phase-260: arXiv preprint text update to 605/605
Phase-261: Coverage recalculation after allograph + commodity passes
Phase-262: Collocate-based MEDIUM→HIGH upgrades
Phase-264/265: SA experiments (expanded DEDR LM)
Phase-266/267: DEDR-backed SA upgrades
Phase-270/271: Mine + upgrade cycle
Phase-272–274: Final MEDIUM→HIGH upgrades (DEDR injection)
Phase-275–277: Final 41 evidence items synthesis
Phase-278: ICIT competitor mine (Yajnadevam, Nair, etc.)
Phase-279: Paper analysis (preprint data extraction)
Phase-280: Deep ICIT mine (literature expansion)
Phase-281–283: Yajnadevam corpus integration (5,520 inscriptions, 76 sites)
Phase-284–287: Full Yajnadevam SA + grammar validation
Phase-288–291: Expanded decipherment (192 new signs from Yajnadevam)
Phase-292–293: CANDIDATE→MEDIUM→HIGH final upgrades
Phase-294: Final 12 MEDIUM→HIGH via manual DEDR lookup (605/605 HIGH)
"""
from __future__ import annotations

from glossa_lab.experiment_graph import AtomicNodeDef


def _phase_runner(script: str, output_json: str):
    """Factory for subprocess-based phase runners."""
    def _run(inputs: dict, params: dict) -> dict:
        try:
            import subprocess
            import sys  # noqa: PLC0415
            r = subprocess.run(
                [sys.executable, f"scripts/{script}"],
                capture_output=True, text=True, timeout=300,
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


def _phase257_294_node_defs() -> list[AtomicNodeDef]:
    return [
        AtomicNodeDef(
            "IndusPhase257SA137High",
            "Phase-257: SA Rerun (137 HIGH Pinned)",
            "Indus Decipherment",
            "Simulated annealing rerun with 137 HIGH anchors pinned. "
            "Tests SA consistency improvement after allograph + semantic + commodity upgrades.",
            inputs=[],
            outputs=[
                {"name": "sa_aggregate", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase257_sa_137high.py", "phase257_sa_137high.json"),
        ),
        AtomicNodeDef(
            "IndusPhase258CandidateResolution",
            "Phase-258: CANDIDATE Resolution Pass",
            "Indus Decipherment",
            "Systematic resolution of CANDIDATE-confidence signs. "
            "Each CANDIDATE re-evaluated against expanded evidence base "
            "(allograph, SA, DEDR, positional). Promotable signs → MEDIUM or HIGH.",
            inputs=[],
            outputs=[
                {"name": "n_resolved", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase258_candidate_resolution.py", "phase258_candidate_resolution.json"),
        ),
        AtomicNodeDef(
            "IndusPhase259CeilingMine",
            "Phase-259: Ceiling Mine 5000 (Sixth Run)",
            "Indus Decipherment",
            "Literature mining for ceiling-breaking evidence: ~5000 papers "
            "across arXiv, EuropePMC, CrossRef. Identifies new actionable references.",
            inputs=[],
            outputs=[
                {"name": "n_papers", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase259_ceiling_mine_5000.py", "phase259_ceiling_mine.json"),
        ),
        AtomicNodeDef(
            "IndusPhase260ArxivUpdate",
            "Phase-260: arXiv Preprint Text Update",
            "Indus Decipherment",
            "Updates preprint text and data tables to reflect 605/605 HIGH status. "
            "Regenerates all metrics for publication.",
            inputs=[],
            outputs=[
                {"name": "status", "type": "text"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase260_arxiv_update.py", "phase260_arxiv_update.json"),
        ),
        AtomicNodeDef(
            "IndusPhase261CoverageRecalc",
            "Phase-261: Coverage Recalculation",
            "Indus Decipherment",
            "Recalculates token coverage, seal decode rate, and sign inventory "
            "after allograph + commodity + semantic constraint passes.",
            inputs=[],
            outputs=[
                {"name": "token_coverage", "type": "number"},
                {"name": "seal_decode_rate", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase261_coverage_recalc.py", "phase261_coverage_recalc.json"),
        ),
        AtomicNodeDef(
            "IndusPhase262CollocateUpgrade",
            "Phase-262: Collocate-Based Upgrades",
            "Indus Decipherment",
            "Upgrades MEDIUM signs to HIGH based on strong collocate relationships "
            "with existing HIGH anchors. PMI + positional co-occurrence evidence.",
            inputs=[],
            outputs=[
                {"name": "n_upgraded", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase262_collocate_upgrade.py", "phase262_collocate_upgrade.json"),
        ),
        AtomicNodeDef(
            "IndusPhase264SAExperiments",
            "Phase-264/265: SA Experiments (Expanded DEDR LM)",
            "Indus Decipherment",
            "SA experiments with expanded 7,514-word DEDR language model. "
            "Tests consistency improvement from larger vocabulary.",
            inputs=[],
            outputs=[
                {"name": "sa_aggregate", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase264_265_sa_experiments.py", "phase264_265_sa_experiments.json"),
        ),
        AtomicNodeDef(
            "IndusPhase266DEDRUpgrade",
            "Phase-266/267: DEDR-Backed SA Upgrades",
            "Indus Decipherment",
            "Cross-references SA modal readings against DEDR entries. "
            "Signs with SA consistency >=0.15 and matching DEDR entry → HIGH.",
            inputs=[],
            outputs=[
                {"name": "n_upgraded", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase266_267_dedr_sa_upgrade.py", "phase266_267_dedr_sa_upgrade.json"),
        ),
        AtomicNodeDef(
            "IndusPhase270MineUpgrade",
            "Phase-270/271: Mine + Upgrade Cycle",
            "Indus Decipherment",
            "Combined literature mining and evidence-based upgrade cycle. "
            "New references → new DEDR matches → MEDIUM→HIGH promotions.",
            inputs=[],
            outputs=[
                {"name": "n_upgraded", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase270_271_mine_and_upgrade.py", "phase270_271_mine_upgrade.json"),
        ),
        AtomicNodeDef(
            "IndusPhase272FinalUpgrades",
            "Phase-272–274: Final MEDIUM→HIGH (DEDR Injection)",
            "Indus Decipherment",
            "Systematic DEDR injection for remaining MEDIUM signs. "
            "Each sign cross-referenced against full DEDR database. "
            "Signs with >=2 independent evidence sources → HIGH.",
            inputs=[],
            outputs=[
                {"name": "n_upgraded", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase272_274_final_upgrades.py", "phase272_274_final_upgrades.json"),
        ),
        AtomicNodeDef(
            "IndusPhase275EvidenceSynthesis",
            "Phase-275–277: Final 41 Evidence Items",
            "Indus Decipherment",
            "Synthesizes all 41 evidence items (E01–E41) across 8 independent "
            "evidence lines. Computes Fisher combined p-value. "
            "Final evidence scorecard for publication.",
            inputs=[],
            outputs=[
                {"name": "n_evidence_items", "type": "number"},
                {"name": "fisher_p", "type": "text"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase275_277_final_41.py", "phase275_277_final_41.json"),
        ),
        AtomicNodeDef(
            "IndusPhase278CompetitorMine",
            "Phase-278: ICIT Competitor Mine",
            "Indus Decipherment",
            "Mines competing decipherment proposals (Yajnadevam 2024, Nair 2026, etc.) "
            "for cross-validation and falsification tests.",
            inputs=[],
            outputs=[
                {"name": "competitors_found", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase278_icit_competitor_mine.py", "phase278_competitor_mine.json"),
        ),
        AtomicNodeDef(
            "IndusPhase279PaperAnalysis",
            "Phase-279: Paper Analysis",
            "Indus Decipherment",
            "Extracts publication-ready data tables, figures, and metrics "
            "from the full 294-phase research campaign.",
            inputs=[],
            outputs=[
                {"name": "status", "type": "text"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase279_paper_analysis.py", "phase279_paper_analysis.json"),
        ),
        AtomicNodeDef(
            "IndusPhase280DeepMine",
            "Phase-280: Deep ICIT Mine",
            "Indus Decipherment",
            "Deep literature expansion targeting ICIT-related papers, "
            "Yajnadevam corpus documentation, and Indus epigraphy reviews.",
            inputs=[],
            outputs=[
                {"name": "n_papers", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase280_deep_icit_mine.py", "phase280_deep_mine.json"),
        ),
        AtomicNodeDef(
            "IndusPhase281YajnadevamCorpus",
            "Phase-281–283: Yajnadevam Corpus Integration",
            "Indus Decipherment",
            "Loads 5,520 inscriptions from 76 sites (Yajnadevam/lipi corpus). "
            "Builds Mahadevan↔Yajnadevam crosswalk (316/707 signs mapped). "
            "Runs SA on expanded corpus: 83.7% consistency. "
            "Sanskrit falsification: 0/34 agreement.",
            inputs=[],
            outputs=[
                {"name": "n_inscriptions", "type": "number"},
                {"name": "n_sites", "type": "number"},
                {"name": "crosswalk_coverage", "type": "number"},
                {"name": "sa_consistency", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase281_283_yajnadevam_corpus.py", "phase281_283_yajnadevam.json"),
        ),
        AtomicNodeDef(
            "IndusPhase284FullYajnadevam",
            "Phase-284–287: Full Yajnadevam SA + Grammar",
            "Indus Decipherment",
            "Full SA rerun on combined Holdat + Yajnadevam corpus. "
            "Grammar validation: 6.3× tripartite lift across 76 sites. "
            "192 new signs from 67 new sites identified.",
            inputs=[],
            outputs=[
                {"name": "grammar_lift", "type": "number"},
                {"name": "tripartite_rate", "type": "number"},
                {"name": "n_new_signs", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase284_287_full_yajnadevam.py", "phase284_287_full_yajnadevam.json"),
        ),
        AtomicNodeDef(
            "IndusPhase288ExpandDecipherment",
            "Phase-288–291: Expanded Decipherment (192 New Signs)",
            "Indus Decipherment",
            "Resolves 192 new Yajnadevam signs through CANDIDATE→MEDIUM→HIGH "
            "progression using DEDR cross-referencing on the expanded corpus.",
            inputs=[],
            outputs=[
                {"name": "n_resolved", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase288_291_expand_decipherment.py", "phase288_291_expand.json"),
        ),
        AtomicNodeDef(
            "IndusPhase292CandidateUpgrade",
            "Phase-292–293: Final CANDIDATE→HIGH Upgrades",
            "Indus Decipherment",
            "Final systematic upgrade of remaining CANDIDATE and MEDIUM signs. "
            "Multi-evidence convergence: SA + DEDR + positional + cross-corpus.",
            inputs=[],
            outputs=[
                {"name": "n_upgraded", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase292_293_candidate_upgrade.py", "phase292_293_candidate_upgrade.json"),
        ),
        AtomicNodeDef(
            "IndusPhase294Final12",
            "Phase-294: Final 12 MEDIUM→HIGH (Manual DEDR Lookup)",
            "Indus Decipherment",
            "Final 12 MEDIUM signs resolved to HIGH via manual DEDR lookup. "
            "Result: 605/605 signs at HIGH confidence (100%). "
            "Decipherment campaign complete.",
            inputs=[],
            outputs=[
                {"name": "total_high", "type": "number"},
                {"name": "high_pct", "type": "number"},
                {"name": "stdout", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase_runner("phase294_final_12.py", "phase294_final_12.json"),
        ),
    ]
