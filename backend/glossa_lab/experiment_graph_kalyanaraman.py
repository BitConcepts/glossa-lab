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
from collections import Counter
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DATA = Path(__file__).parent / "data"
_BKRPT = Path(__file__).parents[1] / "reports"

_LEXICON_PATH = _DATA / "kalyanaraman_rebus.json"
_ANCHORS_PATH = _BKRPT / "INDUS_FINAL_ANCHORS.json"


def _normalise(reading: str) -> set[str]:
    """Return a set of normalised root forms for fuzzy matching."""
    roots: set[str] = set()
    for variant in reading.split("/"):
        v = re.sub(r"[^a-z]", "", variant.strip().lower())
        if len(v) >= 2:
            roots.add(v)
            if len(v) >= 3:
                roots.add(v[:3])  # 3-char prefix for fuzzy
    return roots


def _kalyan_cross_validation(inputs: dict, params: dict) -> dict[str, Any]:
    """Cross-validate anchors against Kalyanaraman rebus lexicon."""

    # ── Load anchors ──────────────────────────────────────────────────────
    if not _ANCHORS_PATH.exists():
        return {"error": "INDUS_FINAL_ANCHORS.json not found"}
    fa = json.loads(_ANCHORS_PATH.read_text(encoding="utf-8"))
    anchors = fa.get("anchors", {})

    # ── Load Kalyanaraman lexicon ─────────────────────────────────────────
    if not _LEXICON_PATH.exists():
        return {"error": "kalyanaraman_rebus.json not found — run _build_kalyanaraman_lexicon.py first"}
    lexicon = json.loads(_LEXICON_PATH.read_text(encoding="utf-8"))

    k_sign_readings: dict[str, list[str]] = lexicon.get("sign_readings", {})
    k_rebus: list[dict] = lexicon.get("rebus_pairs", [])
    k_terms: list[dict] = lexicon.get("dravidian_terms", [])
    k_craft: list[dict] = lexicon.get("craft_vocabulary", [])

    # Build anchor reading → sign index
    anchor_roots: dict[str, list[str]] = {}  # normalised root → [sign_ids]
    for sid, info in anchors.items():
        reading = info.get("reading", "")
        for root in _normalise(reading):
            anchor_roots.setdefault(root, []).append(sid)

    # ── Cross-check sign readings ─────────────────────────────────────────
    corroborated: list[dict] = []
    conflicting: list[dict] = []
    new_candidates: list[dict] = []

    for sign_id, k_readings in k_sign_readings.items():
        anchor_info = anchors.get(sign_id)
        if not anchor_info:
            # Sign not in our anchors — potential new candidate
            for kr in k_readings[:3]:
                new_candidates.append({
                    "sign": sign_id,
                    "kalyanaraman_reading": kr,
                    "source": "sign_proximity",
                    "our_reading": None,
                    "status": "new_candidate",
                })
            continue

        our_reading = anchor_info.get("reading", "")
        our_roots = _normalise(our_reading)
        our_conf = anchor_info.get("confidence", "?")

        for kr in k_readings:
            kr_roots = _normalise(kr)
            overlap = our_roots & kr_roots
            if overlap:
                corroborated.append({
                    "sign": sign_id,
                    "our_reading": our_reading,
                    "our_confidence": our_conf,
                    "kalyanaraman_reading": kr,
                    "overlap_roots": sorted(overlap),
                    "status": "corroborated",
                })
            elif kr_roots and our_roots and not overlap:
                conflicting.append({
                    "sign": sign_id,
                    "our_reading": our_reading,
                    "our_confidence": our_conf,
                    "kalyanaraman_reading": kr,
                    "status": "divergent",
                })

    # ── Cross-check rebus pairs against anchor terms ──────────────────────
    rebus_matches: list[dict] = []
    rebus_new: list[dict] = []

    for rp in k_rebus:
        pic = rp.get("pictogram", "")
        meaning = rp.get("meaning", "")
        pic_roots = _normalise(pic)
        meaning_roots = _normalise(meaning)

        matched_signs = set()
        for root in pic_roots | meaning_roots:
            for sid in anchor_roots.get(root, []):
                matched_signs.add(sid)

        if matched_signs:
            rebus_matches.append({
                "pictogram": pic,
                "meaning": meaning,
                "count": rp.get("count", 0),
                "matched_signs": sorted(matched_signs)[:5],
                "sources": rp.get("sources", [])[:3],
            })
        else:
            rebus_new.append({
                "pictogram": pic,
                "meaning": meaning,
                "count": rp.get("count", 0),
                "sources": rp.get("sources", [])[:3],
            })

    # ── Domain vocabulary check ───────────────────────────────────────────
    # Are our anchor readings content-words or grammar-words?
    grammar_markers = {"ay", "an", "in", "kol", "min", "kal", "itu", "atu"}
    content_words = set()
    grammar_words = set()
    for sid, info in anchors.items():
        reading = info.get("reading", "").lower()
        roots = _normalise(reading)
        if roots & grammar_markers:
            grammar_words.add(sid)
        else:
            content_words.add(sid)

    # ── Build summary ─────────────────────────────────────────────────────
    n_total_anchors = len(anchors)
    n_kalyan_signs = len(k_sign_readings)
    n_overlap_signs = len(set(k_sign_readings.keys()) & set(anchors.keys()))

    complementarity_score = round(
        1.0 - (len(corroborated) / max(n_overlap_signs, 1)), 3
    ) if n_overlap_signs > 0 else 1.0

    summary = {
        "verdict": (
            "COMPLEMENTARY" if complementarity_score > 0.7
            else "PARTIAL_OVERLAP" if complementarity_score > 0.3
            else "HIGH_AGREEMENT"
        ),
        "interpretation": (
            f"Kalyanaraman's rebus system covers {n_kalyan_signs} signs "
            f"({n_overlap_signs} overlap with our {n_total_anchors} anchors). "
            f"{len(corroborated)} corroborated, "
            f"{len(conflicting)} divergent, "
            f"{len(new_candidates)} new candidates. "
            f"Complementarity={complementarity_score:.2f} "
            f"(his system focuses on content-words/trade vocabulary; "
            f"ours on grammatical markers)."
        ),
        "complementarity_score": complementarity_score,
        "system_comparison": {
            "kalyanaraman": {
                "system": "content_word_rebus",
                "domain": "metalwork/trade/craft",
                "focus": "nouns, trade goods, animal names",
            },
            "glossa_lab": {
                "system": "statistical_annealing",
                "domain": "grammatical_structure",
                "focus": "case suffixes, particles, verbal markers",
                "grammar_signs": len(grammar_words),
                "content_signs": len(content_words),
            },
        },
    }

    return {
        "summary": summary,
        "corroborated": corroborated,
        "conflicting": conflicting,
        "new_candidates": new_candidates[:50],  # cap for output size
        "rebus_matches": rebus_matches,
        "rebus_new": rebus_new[:20],
        "coverage": {
            "our_anchors": n_total_anchors,
            "kalyanaraman_signs": n_kalyan_signs,
            "overlap_signs": n_overlap_signs,
            "corroborated_count": len(corroborated),
            "conflicting_count": len(conflicting),
            "new_candidate_count": len(new_candidates),
            "rebus_matched": len(rebus_matches),
            "rebus_new": len(rebus_new),
        },
        "lexicon_stats": lexicon.get("_stats", {}),
    }


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
