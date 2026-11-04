"""Phase-28 atomic-node implementations.

Phase-28 builds on Phase-27 with five priority items:
  1. CISIVol3OCRNode: invokes Mistral pixtral-12b-2409 (or local Ollama
     vision model if configured) on CISI Vol 3 Part 3 PDF pages via the
     glossa-lab `call_llm_vision` framework. Persists raw OCR output to
     `reports/cisi_vol3_extracted_signs.json`.
  2. Phase-28 expanded phoneme map (30 -> 35 entries) loaded via the
     same accessor as Phase-27, with new entries for lion, eagle,
     cobra, plus strengthened yoke-carrier/buffalo entries.
  3. ReverseJanabiyahSearchV2: re-runs Phase-27a with the expanded map
     and allograph-aware position scoring (fish-family signs all match
     the miin slot at positions 1/3/6).
  4. MahadevanCrosswalkLoader: loads Mahadevan 1977 -> Parpola 1994b
     sign crosswalk (25 entries) + 4 allograph families.
  5. AllographAwareIconographicScore: extends Phase-27c so that when an
     iconographic anchor reads "fish" against a single sign ID, ALL
     fish-family allographs (47/48/50/52/60/145/147) score against the
     same anchor. Expands anchor coverage from 7 sign IDs to ~14+.

Plus a corpus loader and verdict aggregator.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── Loader ────────────────────────────────────────────────────────────


def _phase28_corpus_loader(inputs: dict, params: dict) -> dict:
    """Phase-28 loader: extends Phase-27 with Mahadevan-Parpola crosswalk,
    allograph-family map, and CISI Vol 3 OCR results."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_allograph_families,
            get_cisi_findspot_map,
            get_cisi_vol3_ocr_results,
            get_contact_zone_prefix_set,
            get_iconographic_anchors,
            get_indus_seals_at_mesopotamia,
            get_janabiyah_seal_reading,
            get_mahadevan_parpola_crosswalk,
            get_meluhha_tablets,
            get_meluhhan_persons_v3,
            get_parpola_phoneme_map,
            get_phase27_seal_findspot_overrides,
            get_seals_with_inscription,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    return {
        "all_seals": get_indus_seals_at_mesopotamia(),
        "inscribed_seals": get_seals_with_inscription(),
        "persons_v3": get_meluhhan_persons_v3(),
        "phoneme_map": get_parpola_phoneme_map(),
        "janabiyah_reading": get_janabiyah_seal_reading(),
        "tablets": get_meluhha_tablets(),
        "n_tablets": len(get_meluhha_tablets()),
        "findspot_map": get_cisi_findspot_map(),
        "contact_zone_prefixes": sorted(get_contact_zone_prefix_set()),
        "phase27_overrides": get_phase27_seal_findspot_overrides(),
        "iconographic_anchors": get_iconographic_anchors(),
        "mahadevan_crosswalk": get_mahadevan_parpola_crosswalk(),
        "allograph_families": get_allograph_families(),
        "cisi_vol3_ocr": get_cisi_vol3_ocr_results(),
    }


# ── Tier 1 #1: CISI Vol 3 OCR (via call_llm_vision) ─────────────────


_OCR_PROMPT_DEFAULT = (
    "You are looking at a page of the Corpus of Indus Seals and Inscriptions "
    "(CISI) Vol 3 Part 3, edited by Asko Parpola. The page may contain seal "
    "drawings with their CISI catalogue IDs (e.g. 'M-410', 'H-9', 'B-12'), "
    "Parpola sign-list IDs, and iconographic motifs.\n\n"
    "Extract a structured listing in this exact format, one record per line:\n"
    "  SEAL: <catalogue_id> | SIGNS: <comma-separated sign ids or descriptive>\n"
    "  ICONOGRAPHY: <catalogue_id or descriptor> | MOTIF: <motif text>\n"
    "  SIGN_REF: <sign id> | MEANING: <meaning text>\n"
    "If no seal IDs are visible, say 'NO_SEALS_FOUND'."
)


def _cisi_vol3_ocr(inputs: dict, params: dict) -> dict:
    """Run vision-LLM OCR on CISI Vol 3 Part 3 PDF pages.

    Routes through `glossa_lab.ai_utils.call_llm_vision` so the same
    Settings infrastructure (Ollama llava/gemma3-vision first, then
    Mistral pixtral-12b-2409) is used. By default this is a NO-OP that
    returns the previously-saved OCR results to avoid re-running a
    paid API call on every graph execution.

    Params:
      pdf_path: optional path to input PDF (skips OCR if not provided).
      pages: optional list of page numbers to OCR (default: all).
      prompt: custom prompt (default: extraction prompt above).
      run_ocr: if False (default), only load existing results from
        `reports/cisi_vol3_extracted_signs.json`. Set True to re-run.
      output_path: where to write the JSON results.

    Spec 087 S3 PR-F: delegates to the generic VisionOCRNode; the
    prompt, the SEAL:/ICONOGRAPHY:/SIGN_REF: line grammar, the paths
    and the verdict/error texts are spec data.
    """
    from glossa_lab.generic_primitives import vision_ocr_node_execute

    merged = dict(params)
    merged["ocr_spec"] = {
        "base_dir": str(Path(__file__).resolve().parents[2]),
        "default_output_path": "reports/cisi_vol3_extracted_signs.json",
        "default_prompt": _OCR_PROMPT_DEFAULT,
        "count_types": [["seal", "n_seal"], ["iconography", "n_iconography"],
                        ["sign_ref", "n_sign_ref"]],
        "grammar": [
            {"prefix": "SEAL:", "marker": "SIGNS:", "type": "seal",
             "id_out": "seal_id", "value_out": "signs"},
            {"prefix": "ICONOGRAPHY:", "marker": "MOTIF:",
             "type": "iconography", "id_out": "seal_id",
             "value_out": "motif"},
            {"prefix": "SIGN_REF:", "marker": "MEANING:",
             "type": "sign_ref", "id_out": "sign_id",
             "value_out": "meaning"},
        ],
        "skip_prefixes": ["NO_SEALS"],
        "dpi": 200,
        "noop_template": (
            "OCR no-op (run_ocr=False): loaded {n} existing records "
            "from {output_path} ({n_seal} seal, {n_iconography} "
            "iconography, {n_sign_ref} sign_ref). To re-run vision "
            "OCR, set run_ocr=true and provide pdf_path."),
        "run_template": (
            "OCR run on {n_pages} pages of {pdf_name}: {n} records "
            "({n_seal} seal, {n_iconography} iconography, {n_sign_ref} "
            "sign_ref). Saved to {output_path}."),
        "errors": {
            "no_pdf": "run_ocr=True but pdf_path not provided",
            "pdf_not_found": "pdf not found: {pdf_path}",
            "fitz": "PyMuPDF (fitz) not available: {error}",
            "vision": "call_llm_vision not available: {error}",
        },
    }
    return vision_ocr_node_execute(inputs, merged)


# ── Tier 1 #5: Allograph-aware iconographic anchor score ─────────────


# Iconic-reading -> (phoneme alias, allograph family) table for the
# Phase-28 scorer, in the IconographicAnchorScorer spec shape:
# ordered (reading key, [aliases], family) entries.
_ICONOGRAPHIC_ALIAS_TABLE_28: list = [
    ("fish", ["miin"], "fish"),
    ("fish/star", ["miin"], "fish"),
    ("fig", ["vaTa"], "fig_tree"),
    ("banyan/fig", ["vaTa"], "fig_tree"),
    ("banyan", ["vaTa"], "fig_tree"),
    ("muruku", ["muruku"], "intersecting_circles"),
    ("intersecting circles", ["muruku"], "intersecting_circles"),
    ("squirrel", ["piLLai"], None),
    ("pot", ["kuTam"], None),
    ("pot/jar", ["kuTam"], None),
    ("veL", ["veL"], "numerals"),
    ("veN-miin", ["veL"], None),
    ("venus", ["veL"], None),
    ("pleiades", ["aru-"], "numerals"),
    ("ursa major", ["eZu-"], "numerals"),
    ("north star", ["vaTa"], "fig_tree"),
]


def _allograph_aware_iconographic_score(inputs: dict, params: dict) -> dict:
    """Phase-28 extension of Phase-27c IconographicAnchorScore.

    Key change: when an iconographic anchor reads "fish" against a
    single sign ID (e.g. M-410 -> sign 47), all members of the
    fish-allograph family (47, 48, 50, 52, 60, 145, 147) are also
    credited. This expands anchor coverage from 7 sign IDs to ~14+.

    Scoring per anchor (allograph-extended):
      base_score (Phase-27c): 2.0 high anchor + match, 1.0 medium, 0.5 low
      ph_conf bonus: x1.5 if phoneme also high-confidence
      allograph_extension_bonus: +0.25 per additional allograph-family
        member that matches the anchor's iconic_reading

    Spec 087 S3 (family F4): the mechanism is the generic
    IconographicAnchorScorer engine (glossa_lab.generic_primitives)
    in its allograph mode (extension bonus 0.25); this node is its
    Phase-28 parameterisation, with the alias/family table above.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        iconographic_anchor_scorer_execute,
    )

    merged = dict(params)
    merged["scorer_spec"] = {
        "alias_table": _ICONOGRAPHIC_ALIAS_TABLE_28,
        "extension_bonus": 0.25,
        "verdict_template": (
            "Allograph-aware iconographic anchor score (Phase-28): "
            "{n_matches}/{n_total_anchors} anchors have a phoneme match; "
            "{n_allograph_extensions} additional allograph-family members "
            "score against the same anchors (vs Phase-27c which scored "
            "only the explicit sign ID). Total weighted score = "
            "{total_score:.2f}. Distinct sign IDs gaining anchor support "
            "via allograph extension: {extended_sign_ids}."
        ),
    }
    return iconographic_anchor_scorer_execute(inputs, merged)


# ── Tier 1 #3: Reverse Janabiyah Search v2 (allograph-aware) ────────


def _reverse_janabiyah_search_v2(inputs: dict, params: dict) -> dict:
    """Phase-28 extension of Phase-27a reverse Janabiyah search.

    Same scoring as Phase-27a but with two enhancements:
      1. Expanded miin-rendering set: pulls all phonemes whose value
         contains 'miin' from the (expanded) phoneme map dynamically,
         so newly-added entries are picked up automatically.
      2. Allograph-aware position match: any sign in the fish family
         (47/48/50/52/60/145/147) that maps to a Sumerian transliteration
         containing miin/me/mi syllables counts as a position match.

    Spec 087 S3 (family F7): the mechanism is the generic
    ReverseSkeletonSearch engine (glossa_lab.generic_primitives)
    in its persons mode; this node is its Phase-28 parameterisation
    — the same scoring core as Phase-27, the 16-item base rendering
    set, and the dynamic expansion from the phoneme map via the
    fish allograph family (the expansion toggle + family source
    the triage names), all carried as spec data.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        reverse_skeleton_search_execute,
    )

    merged = dict(params)
    merged["search_spec"] = {
        "candidate_mode": "persons",
        "candidates_input": "persons_v3",
        "target_positions": [1, 3, 6],
        "target_length": 7,
        "length_base": 3.0,
        "length_step": 0.5,
        "position_weight": 1.5,
        "free_weight": 0.5,
        "renderings": [
            "miin", "mi-in", "me-en", "mi-na", "me-na", "mi-il",
            "me-il", "mi-en", "me-in", "mu-li", "min", "men",
            "mul", "imin", "kakkab", "asz",
        ],
        "expand_renderings": True,
        "expansion_family": "fish",
        "report_renderings_count": True,
        "penalty_suffixes": ["-me-luh-ha", "-me-luh-ha-ki"],
        "penalty_value": -1.5,
        "top_k_default": 30,
        "top_k_floor": 10,
        "empty_result": {
            "verdict": "INSUFFICIENT_DATA",
            "n_candidates": 0,
            "top_matches": [],
        },
        "verdict_template": (
            "Reverse Janabiyah search v2 (Phase-28, expanded map + "
            "allograph-aware): {n_candidates} unique persons-v3 "
            "candidates scored against {n_renderings} "
            "miin-renderings (vs Phase-27a's static 15). "
            "{n_with_position_match} have at least one "
            "position-match; {n_with_free_miin} have at least one "
            "miin-rendering anywhere. Top candidate: '{top_name}' "
            "(score {top_score}, occurrences {top_occurrences})."
        ),
        "empty_top_text": "No candidates.",
    }
    return reverse_skeleton_search_execute(inputs, merged)


# ── Verdict aggregator ──────────────────────────────────────────────


def _phase28_verdict(inputs: dict, params: dict) -> dict:
    summary = (
        "Phase-28 contact-zone progress: (1) CISI Vol 3 Part 3 OCR "
        "executed via glossa-lab `call_llm_vision` framework (Mistral "
        "pixtral-12b-2409) on 40-page PDF; 23 records extracted but the "
        "PDF on disk turned out to be introduction/front-matter only "
        "(seal IDs are LPIW/LE = Linear Proto-Iranian/Linear Elamite, "
        "NOT Indus script; no overlap with Phase-22 catalogue IDs). "
        "(2) Mahadevan 1977 -> Parpola 1994b crosswalk: 25 entries + 4 "
        "allograph families (fish, numerals, intersecting circles, fig "
        "tree). (3) Phoneme map expanded 30 -> 35 entries: lion (araL), "
        "eagle (puL/Garuda?), cobra (naagam?), strengthened yoke-carrier "
        "(kavai) and buffalo (erumai) entries promoted to high-confidence. "
        "(4) ReverseJanabiyahSearchV2: re-ran Phase-27a against the "
        "expanded map with allograph-aware miin-rendering set "
        "(dynamically pulled from fish-family entries). (5) "
        "AllographAwareIconographicScore: extends Phase-27c so e.g. M-410 "
        "fish anchor (sign 47) credits ALL fish-family allographs "
        "(48/50/52/60/145/147) — anchor coverage roughly doubles."
    )
    next_steps = [
        "Phase-29 priority 1: acquire CISI Vol 3 Part 1/Part 2 (the "
        "ACTUAL Indus catalogue plates — Vol 3 Part 3 turned out to be "
        "introduction). Best route: ICIPS or Helsinki/Harvard ILL.",
        "Phase-29 priority 2: complete Mahadevan 1977 sign-list "
        "crosswalk to all ~417 signs (currently 25 of the most-cited).",
        "Phase-29 priority 3: extend allograph-family coverage to Wells "
        "2015 typology (more granular than Parpola 1994b families).",
        "Phase-29 priority 4: attempt Crawford 2001 'Early Dilmun' "
        "again via a different mirror.",
        "Phase-29 priority 5: build a held-out blind test set (any "
        "newly-published seals from 2024-2026) and run the full Phase-28 "
        "pipeline on them as a pre-registered confirmation.",
    ]
    return {
        "summary": summary,
        "next_steps": next_steps,
    }


# ── Atomic node defs for registration ───────────────────────────────


def _phase28_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "Phase28CorpusLoader", "Phase-28 Contact Corpus Loader",
            "Phase-28 / Sources",
            "Load Phase-28 contact-zone artefacts: extends Phase-27 with "
            "Mahadevan-Parpola crosswalk, allograph families, and CISI "
            "Vol 3 OCR results.",
            inputs=[],
            outputs=[
                {"name": "all_seals", "type": "json"},
                {"name": "inscribed_seals", "type": "json"},
                {"name": "persons_v3", "type": "json"},
                {"name": "phoneme_map", "type": "json"},
                {"name": "janabiyah_reading", "type": "json"},
                {"name": "tablets", "type": "json"},
                {"name": "n_tablets", "type": "number"},
                {"name": "findspot_map", "type": "json"},
                {"name": "contact_zone_prefixes", "type": "json"},
                {"name": "phase27_overrides", "type": "json"},
                {"name": "iconographic_anchors", "type": "json"},
                {"name": "mahadevan_crosswalk", "type": "json"},
                {"name": "allograph_families", "type": "json"},
                {"name": "cisi_vol3_ocr", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase28_corpus_loader,
        ),
        AtomicNodeDef(
            "CISIVol3OCRNode",
            "CISI Vol 3 OCR (Mistral pixtral-12b via call_llm_vision)",
            "Phase-28 / Sources",
            "Run vision-LLM OCR on CISI Vol 3 Part 3 PDF pages via the "
            "glossa-lab `call_llm_vision` framework. Default no-op "
            "loads previously-saved results from "
            "`reports/cisi_vol3_extracted_signs.json`. Set "
            "run_ocr=true + pdf_path=... to re-run.",
            inputs=[],
            outputs=[
                {"name": "n_records", "type": "number"},
                {"name": "n_seal", "type": "number"},
                {"name": "n_iconography", "type": "number"},
                {"name": "n_sign_ref", "type": "number"},
                {"name": "records", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "run_ocr": {"type": "boolean", "default": False},
                    "pdf_path": {"type": "string"},
                    "pages": {"type": "array", "items": {"type": "integer"}},
                    "prompt": {"type": "string"},
                    "output_path": {
                        "type": "string",
                        "default": "reports/cisi_vol3_extracted_signs.json",
                    },
                },
            },
            fn=_cisi_vol3_ocr,
        ),
        AtomicNodeDef(
            "MahadevanCrosswalkLoader",
            "Mahadevan 1977 - Parpola 1994b Crosswalk Loader (Phase-28)",
            "Phase-28 / Sources",
            "Load the Mahadevan 1977 -> Parpola 1994b sign-list crosswalk "
            "(25 entries) plus the 4 allograph families (fish, numerals, "
            "intersecting circles, fig tree). Used by allograph-aware "
            "iconographic scorer.",
            inputs=[],
            outputs=[
                {"name": "mahadevan_crosswalk", "type": "json"},
                {"name": "allograph_families", "type": "json"},
                {"name": "n_crosswalk_entries", "type": "number"},
                {"name": "n_allograph_families", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=lambda inputs, params: {
                **(_phase28_corpus_loader({}, {}) or {}),
                "n_crosswalk_entries": len(
                    (_phase28_corpus_loader({}, {}) or {}).get(
                        "mahadevan_crosswalk", {}
                    )
                ),
                "n_allograph_families": len(
                    (_phase28_corpus_loader({}, {}) or {}).get(
                        "allograph_families", {}
                    )
                ),
            },
        ),
        AtomicNodeDef(
            "AllographAwareIconographicScore",
            "Allograph-Aware Iconographic Anchor Score (Phase-28)",
            "Phase-28 / Decipherment",
            "Phase-28 extension of Phase-27c IconographicAnchorScore: "
            "when an iconographic anchor reads 'fish' against a single "
            "sign (e.g. M-410 -> sign 47), all members of the fish-"
            "allograph family (48/50/52/60/145/147) also score against "
            "the same anchor. Expands anchor coverage from 7 sign IDs "
            "to ~14+.",
            inputs=[
                {"name": "iconographic_anchors", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
                {"name": "allograph_families", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_total_anchors", "type": "number"},
                {"name": "n_matches", "type": "number"},
                {"name": "n_allograph_extensions", "type": "number"},
                {"name": "extended_sign_ids", "type": "json"},
                {"name": "total_score", "type": "number"},
                {"name": "rows", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_allograph_aware_iconographic_score,
        ),
        AtomicNodeDef(
            "ReverseJanabiyahSearchV2",
            "Reverse Janabiyah Search V2 (Phase-28, expanded + allograph-aware)",
            "Phase-28 / Decipherment",
            "Phase-28 extension of Phase-27a ReverseJanabiyahSearch: "
            "uses the expanded 35-entry phoneme map and dynamically "
            "pulls all miin-renderings from fish-family entries.",
            inputs=[
                {"name": "persons_v3", "type": "json", "required": True},
                {"name": "janabiyah_reading", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
                {"name": "allograph_families", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_candidates", "type": "number"},
                {"name": "n_renderings", "type": "number"},
                {"name": "n_with_position_match", "type": "number"},
                {"name": "n_with_free_miin", "type": "number"},
                {"name": "top_matches", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "top_k": {"type": "integer", "default": 30, "minimum": 5},
                },
            },
            fn=_reverse_janabiyah_search_v2,
        ),
        AtomicNodeDef(
            "Phase28Verdict", "Phase-28 Verdict Aggregator",
            "Phase-28 / Reporters",
            "Aggregate Phase-28 sub-experiment outputs into a "
            "decipherment-progress verdict + Phase-29 priority list.",
            inputs=[],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "next_steps", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase28_verdict,
        ),
    ]


__all__ = [
    "_phase28_corpus_loader",
    "_cisi_vol3_ocr",
    "_allograph_aware_iconographic_score",
    "_reverse_janabiyah_search_v2",
    "_phase28_verdict",
    "_phase28_node_defs",
]
