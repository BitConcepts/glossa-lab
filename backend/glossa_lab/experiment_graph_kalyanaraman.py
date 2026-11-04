"""Kalyanaraman Rebus Cross-Validation atomic node.

Provides a `KalyanCrossValidation` node that cross-checks
INDUS_FINAL_ANCHORS against the Kalyanaraman rebus lexicon
(extracted from 52 papers on metalwork/trade rebus readings).

Outputs:
  - corroborated: signs where both systems agree (independent evidence)
  - conflicting:  signs where readings diverge (needs investigation)
  - new_candidates: Kalyanaraman readings for signs we haven't decoded
  - coverage_stats: overlap metrics
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DATA = Path(__file__).parent / "data"
_BKRPT = Path(__file__).parents[1] / "reports"

_LEXICON_PATH = _DATA / "kalyanaraman_rebus.json"
_ANCHORS_PATH = _BKRPT / "INDUS_FINAL_ANCHORS.json"


def _kalyan_cross_validation(inputs: dict, params: dict) -> dict[str, Any]:
    """Cross-validate anchors against Kalyanaraman rebus lexicon.

    Spec 087 S3 PR-F: delegates to the generic LexiconCrossValidator;
    the file paths (resolved from this module's constants at call
    time), the error texts, the grammar-marker set, the caps, the
    complementarity bands and the comparison frames are spec data.
    """
    from glossa_lab.generic_primitives import (
        lexicon_cross_validator_execute,
    )

    merged = dict(params)
    merged["validator_spec"] = {
        "base_dir": str(Path(__file__).resolve().parent.parent.parent),
        "anchors_path": str(_ANCHORS_PATH),
        "lexicon_path": str(_LEXICON_PATH),
        "anchors_error": "INDUS_FINAL_ANCHORS.json not found",
        "lexicon_error": (
            "kalyanaraman_rebus.json not found — run "
            "_build_kalyanaraman_lexicon.py first"),
        "normalise": {"min_root_len": 2, "prefix_len": 3},
        "grammar_markers": ["ay", "an", "in", "kol", "min", "kal",
                            "itu", "atu"],
        "caps": {"new_per_sign": 3, "new_out": 50, "rebus_new_out": 20,
                 "matched_signs": 5, "sources": 3},
        "bands": [[0.7, "COMPLEMENTARY"], [0.3, "PARTIAL_OVERLAP"]],
        "bands_fallback": "HIGH_AGREEMENT",
        "interpretation_template": (
            "Kalyanaraman's rebus system covers {n_kalyan} signs "
            "({n_overlap} overlap with our {n_anchors} anchors). "
            "{n_corr} corroborated, {n_conf} divergent, {n_new} new "
            "candidates. Complementarity={score:.2f} (his system "
            "focuses on content-words/trade vocabulary; ours on "
            "grammatical markers)."),
        "systems": {
            "external": {
                "system": "content_word_rebus",
                "domain": "metalwork/trade/craft",
                "focus": "nouns, trade goods, animal names",
            },
            "own": {
                "system": "statistical_annealing",
                "domain": "grammatical_structure",
                "focus": "case suffixes, particles, verbal markers",
            },
        },
    }
    return lexicon_cross_validator_execute(inputs, merged)


def _kalyanaraman_node_defs() -> list:
    """Return atomic node definitions for Kalyanaraman cross-validation."""
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "KalyanCrossValidation",
            "Kalyanaraman Rebus Cross-Validation",
            "Validation",
            "Cross-validates INDUS_FINAL_ANCHORS against Kalyanaraman's rebus "
            "lexicon (52 papers, metalwork/trade content-word readings). "
            "Reports corroborated signs, divergent readings, and new anchor "
            "candidates not in our system. Measures complementarity between "
            "the two independent decipherment approaches.",
            inputs=[],
            outputs=[
                {"name": "summary", "type": "json"},
                {"name": "corroborated", "type": "json"},
                {"name": "conflicting", "type": "json"},
                {"name": "new_candidates", "type": "json"},
                {"name": "coverage", "type": "json"},
                {"name": "data", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {},
            },
            fn=_kalyan_cross_validation,
        ),
    ]
