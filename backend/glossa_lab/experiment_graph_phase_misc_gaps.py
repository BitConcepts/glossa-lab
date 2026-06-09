"""Experiment graph node definitions for miscellaneous unregistered phases.

Covers phases that had scripts but no graph registration:
  Phase 44-47: Pre-pipeline infrastructure, Dravidian LM rebuild, fish tests
  Phase 202:   Bulk mine 5000 (second run)
  Phase 209:   Anchor injection M712/M817
  Phase 210:   Brahui genomics mine
  Phase 211:   Computational survey
  Phase 212:   Scale-free network analysis
  Phase 213:   SA rerun 408 anchors
  Phase 214:   Final injection blocked signs
  Phase 215:   PDF report generation
  Phase 254:   Semantic constraint experiment
  Phase 255:   Commodity phoneme mapping
  Phase 256:   LE extension experiment
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
            for d in [Path(__file__).parents[2] / "outputs",
                       Path(__file__).parents[2] / "backend" / "reports"]:
                p = d / fname
                if p.exists():
                    return json.loads(p.read_text("utf-8"))
            return {"stdout": r.stdout[-500:], "rc": r.returncode}
        except Exception as exc:
            return {"error": str(exc)}
    return _runner


def _misc_gaps_node_defs() -> list[AtomicNodeDef]:
    _out = [{"name": "report", "type": "object"}]
    _ep = {"type": "object", "properties": {}}

    return [
        # ── Phase 44: Infrastructure + Dravidian LM rebuild ──
        AtomicNodeDef(
            "IndusPhase44Infrastructure", "Phase-44 Infrastructure & Dravidian LM",
            "Indus Decipherment",
            "Phase-44 infrastructure rebuild: Dravidian Tamil LM construction, "
            "M342 bigram analysis, M99 DEDR test, V3 SA 300k-iteration run.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase44_infrastructure.py"),
        ),
        # ── Phase 45: Fish coastal test + Fuls crosscheck ──
        AtomicNodeDef(
            "IndusPhase45FishCoastal", "Phase-45 Fish Coastal & Fuls Crosscheck",
            "Indus Decipherment",
            "Phase-45: Fish-sign coastal distribution test, Fuls method crosscheck, "
            "M267 analysis, hunt tripartite test.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase45_fish_coastal_test.py"),
        ),
        # ── Phase 46: Contact zone + SA with 944-LM ──
        AtomicNodeDef(
            "IndusPhase46ContactZone", "Phase-46 Contact Zone & 944-LM SA",
            "Indus Decipherment",
            "Phase-46: Contact zone analysis, SA decipherment with 944-sign LM, "
            "M267 reading, fish expansion, SA parameter sweep.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase46_t1_contact_zone.py"),
        ),
        # ── Phase 47: Phoneme assignment + publication mining ──
        AtomicNodeDef(
            "IndusPhase47PhonemeAssign", "Phase-47 Phoneme Assignment & Pub Mining",
            "Indus Decipherment",
            "Phase-47: Systematic phoneme assignment, publication mining for "
            "validation targets, M267 constraint analysis.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase47_t1_phoneme_assignment.py"),
        ),
        # ── Phase 202: Bulk mine 5000 (second run) ──
        AtomicNodeDef(
            "IndusPhase202BulkMine2", "Phase-202 Bulk Mine 5000 (Run 2)",
            "Indus Decipherment",
            "Phase-202: Second iteration of the 5000-paper bulk literature mine.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase202_bulk_mine_5000.py"),
        ),
        # ── Phase 209: Anchor injection M712/M817 ──
        AtomicNodeDef(
            "IndusPhase209AnchorM712M817", "Phase-209 Anchor Injection M712/M817",
            "Indus Decipherment",
            "Phase-209: Inject anchors for M712 and M817 signs based on "
            "distributional evidence and DEDR cognates.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase209_anchor_injection_m712_m817.py"),
        ),
        # ── Phase 210: Brahui genomics mine ──
        AtomicNodeDef(
            "IndusPhase210BrahuiGenomics", "Phase-210 Brahui Genomics Mine",
            "Indus Decipherment",
            "Phase-210: Literature mine for Brahui population genetics and "
            "aDNA evidence connecting Dravidian speakers to IVC regions.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase210_brahui_genomics.py"),
        ),
        # ── Phase 211: Computational survey ──
        AtomicNodeDef(
            "IndusPhase211ComputationalSurvey", "Phase-211 Computational Survey",
            "Indus Decipherment",
            "Phase-211: Survey of computational approaches to Indus script "
            "decipherment — Rao, Wells, Fuls, Sproat methodologies compared.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase211_computational_survey.py"),
        ),
        # ── Phase 212: Scale-free network ──
        AtomicNodeDef(
            "IndusPhase212ScaleFreeNetwork", "Phase-212 Scale-Free Network",
            "Indus Decipherment",
            "Phase-212: Scale-free network analysis of sign co-occurrence graph. "
            "Tests if the Indus sign network exhibits power-law degree distribution.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase212_scale_free_network.py"),
        ),
        # ── Phase 213: SA rerun 408 anchors ──
        AtomicNodeDef(
            "IndusPhase213SARerun408", "Phase-213 SA Rerun 408 Anchors",
            "Indus Decipherment",
            "Phase-213: Full SA decipherment rerun with 408 pinned anchors "
            "to validate convergence improvement from anchor amplification.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase213_sa_rerun_408anchors.py"),
        ),
        # ── Phase 214: Final injection blocked ──
        AtomicNodeDef(
            "IndusPhase214FinalInjection", "Phase-214 Final Injection Blocked Signs",
            "Indus Decipherment",
            "Phase-214: Attempt to inject readings for remaining blocked signs "
            "using distributional profile matching and DEDR evidence.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase214_final_injection_blocked.py"),
        ),
        # ── Phase 215: PDF report ──
        AtomicNodeDef(
            "IndusPhase215PDFReport", "Phase-215 PDF Report Generation",
            "Indus Decipherment",
            "Phase-215: Generate comprehensive PDF report of decipherment results.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase215_pdf_report.py"),
        ),
        # ── Phase 254: Semantic constraint ──
        AtomicNodeDef(
            "IndusPhase254SemanticConstraint", "Phase-254 Semantic Constraint",
            "Indus Decipherment",
            "Phase-254: Semantic constraint experiment testing whether decoded "
            "readings form semantically coherent fields within inscription slots.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase254_semantic_constraint.py"),
        ),
        # ── Phase 255: Commodity phonemes ──
        AtomicNodeDef(
            "IndusPhase255CommodityPhonemes", "Phase-255 Commodity Phoneme Mapping",
            "Indus Decipherment",
            "Phase-255: Map Dravidian commodity terms to phonemic patterns and "
            "test against anchor readings for trade-vocabulary coverage.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase255_commodity_phonemes.py"),
        ),
        # ── Phase 256: LE extension ──
        AtomicNodeDef(
            "IndusPhase256LEExtension", "Phase-256 LE Extension",
            "Indus Decipherment",
            "Phase-256: Linguistic evidence extension experiment — broadening "
            "the phonological evidence base for low-confidence anchor signs.",
            inputs=[], outputs=_out, params_schema=_ep,
            fn=_make_runner("phase256_le_extension.py"),
        ),
    ]
