"""Experiment graph node definitions for Phases 298-308.

Phase-298: Deep Munda & archaeology literature mine
Phase-299: Proto-Munda bigram LM construction
Phase-300: Competing SA — Munda vs Dravidian vs Hebrew vs Uniform
Phase-301: Munda substrate cross-reference against 605 anchors
Phase-302: Archaeological context scoring (guild-identity model)
Phase-303: Anchored Munda SA (pin 605 Dravidian anchors, test Munda LM)
Phase-304: Allograph independent validation
Phase-305: Cross-researcher reading comparison
Phase-306: Seal translation semantic coherence test
Phase-307: DEDR coverage depth analysis
Phase-308: Elamite bigram LM baseline — 5-way competing anchored SA
"""
from __future__ import annotations
import subprocess
import sys
import json
from pathlib import Path
from glossa_lab.experiment_graph import AtomicNodeDef

_BACKEND = str(Path(__file__).parents[1])


def _make_runner(script: str, out_name: str | None = None):
    def _runner(inputs: dict, params: dict) -> dict:
        try:
            r = subprocess.run(
                [sys.executable, f"scripts/{script}"],
                capture_output=True, text=True, timeout=900, cwd=_BACKEND,
            )
            fname = out_name or script.replace(".py", ".json")
            for d in [Path(__file__).parents[2] / "outputs"]:
                p = d / fname
                if p.exists():
                    return json.loads(p.read_text("utf-8"))
            return {"stdout": r.stdout[-500:], "rc": r.returncode}
        except Exception as exc:
            return {"error": str(exc)}
    return _runner


def _phase298_308_node_defs() -> list[AtomicNodeDef]:
    _out = [{"name": "report", "type": "object"}]
    _empty_params = {"type": "object", "properties": {}}

    return [
        # ── Phase 298: Deep Munda & Archaeology mine ──
        AtomicNodeDef(
            "IndusPhase298DeepMundaArchMine",
            "Phase-298 Deep Munda & Archaeology Mine",
            "Indus Decipherment",
            "Exhaustive multi-API literature mine targeting Proto-Munda "
            "SA comparisons and archaeological bilingual inscription "
            "discoveries. 7,984 papers mined; 208 Munda-relevant, "
            "62 archaeology-relevant. No new bilingual found.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase298_deep_munda_archaeology_mine.py",
                "phase298_deep_munda_archaeology_mine.json",
            ),
        ),
        # ── Phase 299: Proto-Munda bigram LM ──
        AtomicNodeDef(
            "IndusPhase299MundaLM",
            "Phase-299 Proto-Munda Bigram LM",
            "Indus Decipherment",
            "Build Proto-Munda bigram language model from Pinnow 1959, "
            "Anderson 2008, Witzel 1999, Fuller 2006, and DEDR Munda "
            "cognate entries. ~170 vocab items, character bigram scoring.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase299_302_munda_sa_substrate_archaeology.py",
                "phase299_302_munda_sa_substrate_archaeology.json",
            ),
        ),
        # ── Phase 300: Competing SA — Munda vs Dravidian ──
        AtomicNodeDef(
            "IndusPhase300CompetingSA",
            "Phase-300 Competing SA (Munda vs Dravidian)",
            "Indus Decipherment",
            "Unconstrained SA decipherment on IVS corpus with 4 competing "
            "LMs: Dravidian (TamilTB), Proto-Munda, Hebrew (OT), Uniform. "
            "Tests whether raw bigram scoring discriminates language family.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase299_302_munda_sa_substrate_archaeology.py",
                "phase299_302_munda_sa_substrate_archaeology.json",
            ),
        ),
        # ── Phase 301: Munda substrate cross-reference ──
        AtomicNodeDef(
            "IndusPhase301MundaSubstrate",
            "Phase-301 Munda Substrate Cross-Reference",
            "Indus Decipherment",
            "Cross-reference known Munda substrate words (Witzel 1999, "
            "Southworth 2005) against 605 anchor readings. 2 confirmed "
            "matches (M374=kul, M351=vī), 71 potential partial matches.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase299_302_munda_sa_substrate_archaeology.py",
                "phase299_302_munda_sa_substrate_archaeology.json",
            ),
        ),
        # ── Phase 302: Archaeological context scoring ──
        AtomicNodeDef(
            "IndusPhase302ArchaeologyScoring",
            "Phase-302 Archaeological Context Scoring",
            "Indus Decipherment",
            "Score guild-identity model against 9 major IVC sites using "
            "seal density, trade goods, and site specialization data from "
            "Kenoyer 2008, Possehl 2002, Wright 2010.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase299_302_munda_sa_substrate_archaeology.py",
                "phase299_302_munda_sa_substrate_archaeology.json",
            ),
        ),
        # ── Phase 303: Anchored Munda SA ──
        AtomicNodeDef(
            "IndusPhase303AnchoredMundaSA",
            "Phase-303 Anchored Munda SA",
            "Indus Decipherment",
            "Pin 605 Dravidian anchors and test if Munda LM degrades "
            "consistency. Compares Dravidian vs Munda bigram hit rates "
            "on anchor-constrained corpus bigrams.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase303_307_advanced_experiments.py",
                "phase303_307_advanced_experiments.json",
            ),
        ),
        # ── Phase 304: Allograph independent validation ──
        AtomicNodeDef(
            "IndusPhase304AllographValidation",
            "Phase-304 Allograph Independent Validation",
            "Indus Decipherment",
            "Test whether allograph-inferred signs have independent "
            "supporting evidence (DEDR entries, SA convergence, Elamite "
            "corroboration) beyond profile similarity alone.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase303_307_advanced_experiments.py",
                "phase303_307_advanced_experiments.json",
            ),
        ),
        # ── Phase 305: Cross-researcher comparison ──
        AtomicNodeDef(
            "IndusPhase305CrossResearcher",
            "Phase-305 Cross-Researcher Comparison",
            "Indus Decipherment",
            "Compare our model against competing proposals: Mukhopadhyay "
            "(semasiographic), Shaw 2026 (LISSE), Singh 2026 (structural-"
            "semiotic), Yajnadevam 2024 (Sanskrit). Tally agreements and "
            "contradictions.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase303_307_advanced_experiments.py",
                "phase303_307_advanced_experiments.json",
            ),
        ),
        # ── Phase 306: Semantic coherence ──
        AtomicNodeDef(
            "IndusPhase306SemanticCoherence",
            "Phase-306 Seal Translation Semantic Coherence",
            "Indus Decipherment",
            "Test whether decoded seal translations are semantically "
            "coherent. Classify inscriptions by semantic type (animal/"
            "guild, title/formula, suffix-only) and assess guild-identity "
            "model support.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase303_307_advanced_experiments.py",
                "phase303_307_advanced_experiments.json",
            ),
        ),
        # ── Phase 307: DEDR coverage depth ──
        AtomicNodeDef(
            "IndusPhase307DEDRCoverage",
            "Phase-307 DEDR Coverage Depth",
            "Indus Decipherment",
            "Analyze DEDR citation depth across 605 anchors: how many "
            "have explicit DEDR entries, what sources are cited, and "
            "which DEDR roots are shared by multiple signs.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase303_307_advanced_experiments.py",
                "phase303_307_advanced_experiments.json",
            ),
        ),
        # ── Phase 308: Elamite baseline ──
        AtomicNodeDef(
            "IndusPhase308ElamiteBaseline",
            "Phase-308 Elamite Bigram LM Baseline",
            "Indus Decipherment",
            "Build Elamite bigram LM (Hinz & Koch 1987, Stolper 1984, "
            "Grillot-Susini 1987, Tavernier 2007). Run 5-way competing "
            "anchored SA: Elamite vs Dravidian vs Munda vs Hebrew vs "
            "Uniform. Tests McAlpin's Elamo-Dravidian hypothesis.",
            inputs=[], outputs=_out,
            params_schema=_empty_params,
            fn=_make_runner(
                "phase308_elamite_baseline.py",
                "phase308_elamite_baseline.json",
            ),
        ),
    ]
