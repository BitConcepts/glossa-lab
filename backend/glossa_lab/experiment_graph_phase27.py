"""Phase-27 atomic-node implementations.

Phase-27 builds on Phase-26 with:
  1. ReverseJanabiyahSearch: starts from common Akkadian PNs in the Meluhha
     context, decomposes each into segments, and scores against Janabiyah's
     predicted phonetic skeleton. Smaller, more constrained search space
     than Phase-25a/26c.
  2. BayesianDecoderV2: extends Phase-26b to permute phoneme VALUES (not
     just confidence labels) under a Dravidian compound-name plausibility
     metric.
  3. IconographicAnchorScore: scores Parpola's phoneme map against the
     12 iconographic anchors (M-410, H-9, M-414, M-1186, M-1202, etc).
  4. PeriodStratifiedReadout6Bucket: extends Phase-25c with finer-grained
     period buckets (Lagash II, Sargonic Akkadian, Neo-Assyrian, Ebla
     split out from 'Other').
  5. ShuIlishuContactZoneFilter: now ACTUALLY filters the 138 candidates
     using Phase-27's catalogue_id-aware indus_cisi accessor.
  6. Phase27CorpusLoader: loads Phase-26 + iconographic anchors + Phase-27
     find-spot overrides.
"""

from __future__ import annotations

from collections import Counter
from typing import Any


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── Loader ────────────────────────────────────────────────────────────


def _phase27_corpus_loader(inputs: dict, params: dict) -> dict:
    """Phase-27 loader: extends Phase-26 with iconographic anchors and
    Phase-27 explicit find-spot overrides."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_cisi_findspot_map,
            get_contact_zone_prefix_set,
            get_iconographic_anchors,
            get_indus_seals_at_mesopotamia,
            get_janabiyah_seal_reading,
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
    }


# ── Tier 1 #1: Reverse Janabiyah search ──────────────────────────────


def _reverse_janabiyah_search(inputs: dict, params: dict) -> dict:
    """Reverse the Phase-25a/26c Janabiyah search: instead of asking 'does
    the predicted phonetic skeleton appear in CDLI?', ask 'for each
    common Akkadian PN in the Meluhha context, do its segments match
    Janabiyah's predicted phoneme structure?'.

    Strategy:
      1. Take all unique persons-v3 candidate names (44 in Phase-25d).
      2. For each, split into segments by '-'.
      3. Score against Janabiyah's predicted phoneme sequence
         [?, miin, or?, miin, ?, ?, miin] using:
           - Length match: bonus if PN has 5-9 segments (Janabiyah has 7).
           - 'miin' segments: bonus if PN contains *miin*-rendering syllables
             (mi-in, me-en, mi-na, etc.) at positions 1, 3, 6.
           - 'mul'-translation segments: bonus if PN contains mul/imin/kakkab
             at the same positions.
      4. Report top-K candidate PNs ranked by total score.

    Spec 087 S3 (family F7): the mechanism is the generic
    ReverseSkeletonSearch engine (glossa_lab.generic_primitives)
    in its persons mode; this node is its Phase-27 parameterisation
    — the family's shared scoring core (target positions {1, 3, 6},
    target length 7, the 3.0/1.5/0.5 weights), the static 15-item
    rendering set, and the -me-luh-ha / -me-luh-ha-ki suffix
    penalty (the suffix is generic 'of Meluhha', not a phoneme),
    all carried as spec data.
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
            "mul", "imin", "kakkab",
        ],
        "penalty_suffixes": ["-me-luh-ha", "-me-luh-ha-ki"],
        "penalty_value": -1.5,
        "top_k_default": 20,
        "top_k_floor": 10,
        "empty_result": {
            "verdict": "INSUFFICIENT_DATA",
            "n_candidates": 0,
            "top_matches": [],
        },
        "verdict_template": (
            "Reverse Janabiyah search: {n_candidates} unique "
            "persons-v3 candidates scored. {n_with_position_match} "
            "have at least one position-match (segment with "
            "miin-rendering at Janabiyah position 1/3/6). "
            "{n_with_free_miin} have at least one miin-rendering "
            "anywhere in the name. Top candidate: '{top_name}' "
            "(score {top_score}, occurrences {top_occurrences})."
        ),
        "empty_top_text": "No candidates.",
    }
    return reverse_skeleton_search_execute(inputs, merged)


# ── Tier 2 #4: Phoneme-VALUE permutation null ────────────────────────


# Dravidian compound name patterns from Parpola 2010: each tuple is a
# (component-1, component-2) pair that forms an attested compound.
_DRAVIDIAN_COMPOUND_PATTERNS: list[tuple[str, str]] = [
    ("aru", "miin"),    # Pleiades (six stars)
    ("eZu", "miin"),    # Ursa Major (seven stars)
    ("vaTa", "miin"),   # north star (banyan + star)
    ("veL", "miin"),    # Venus (white star)
    ("muruku", "veL"),  # Murukan-veL (Murukan compound)
    ("muruku", "piLLai"),  # Muruka-p-piLLa
    ("muruku", "miin"),  # Murukan + star
    ("katir", "miin"),  # radiant star
]


def _bayesian_decoder_v2(inputs: dict, params: dict) -> dict:
    """Phase-27 v2: permutes phoneme VALUES across sign IDs, scores under
    a Dravidian compound-name plausibility metric.

    For each null permutation, the phoneme VALUES (miin, aru-, eZu-, etc.)
    are randomly reassigned to sign IDs (preserving the multiset of
    values). For each seal, the resulting sequence of phonemes is scored
    via the compound-plausibility metric. Total score = sum across seals.
    p-value = fraction of nulls with score >= observed.

    Spec 087 S3 (family F4): the mechanism is the generic
    PhonemeMapPermutationTest engine (glossa_lab.generic_primitives)
    in its value-shuffle + plausibility mode; this node is its
    Phase-27 parameterisation (seed 2727, all rows). The pattern
    table above stays as the delegation data (+1.0 per attested
    compound match, +0.2 per repeated phoneme, as engine defaults).
    The module-local _seal_phoneme_match_score /
    _compound_plausibility_score helpers were used only here and
    were removed with the delegation.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        phoneme_map_permutation_test_execute,
    )

    merged = dict(params)
    merged.setdefault("seed", 2727)
    merged["decoder_spec"] = {
        "shuffle_dimension": "value",
        "null_gloss": "(value-permuted)",
        "observed_key": "observed_total_score",
        "null_mean_key": "null_mean_score",
        "rows_key": "obs_per_seal",
        "rows_limit": None,
        "plausibility_patterns": _DRAVIDIAN_COMPOUND_PATTERNS,
        "verdict_template": (
            "Bayesian decoder v2 (phoneme-VALUE permutation): observed total "
            "weighted score = {observed:.3f} across {n_seals} inscribed "
            "seals. Null mean = {null_mean:.3f} ({n_perms} value permutations). "
            "Global p-value = {p_value:.4f}. Lower p = the SPECIFIC Dravidian "
            "phoneme values that Parpola assigns to specific sign IDs produce "
            "more plausible compound names than chance value-assignments would."
        ),
        "interpretation": (
            "This extends Phase-26b: instead of permuting just confidence "
            "labels, we permute the actual Dravidian phoneme VALUES (miin, "
            "aru-, eZu-, vaTa-, muruku, etc.) across sign IDs. Significant p "
            "would mean Parpola's specific value-assignments produce more "
            "Dravidian-plausible compounds (aru-miin = Pleiades, vaTa-miin = "
            "north star, etc.) than randomized value-assignments. As with "
            "Phase-26b, this test is currently data-starved (1/11 readable "
            "seals) and will only become informative after CISI Vol 3 plate "
            "ingestion (Phase-28+)."
        ),
    }
    return phoneme_map_permutation_test_execute(inputs, merged)


# ── Tier 1 #3: Iconographic anchor score ─────────────────────────────


# Iconic-reading -> phoneme-alias table for the Phase-27 anchor
# scorer, in the IconographicAnchorScorer spec shape: ordered
# (reading key, [aliases], allograph family) entries; the family is
# unused by this node (Phase-28's table names families).
_ICONOGRAPHIC_ALIAS_TABLE: list = [
    ("fish", ["miin"], None),
    ("fish/star", ["miin"], None),
    ("fig", ["vaTa"], None),
    ("banyan/fig", ["vaTa"], None),
    ("banyan", ["vaTa"], None),
    ("muruku", ["muruku"], None),
    ("intersecting circles", ["muruku"], None),
    ("squirrel", ["piLLai"], None),
    ("pot", ["kuTam"], None),
    ("pot/jar", ["kuTam"], None),
    ("veL", ["veL", "veLLi"], None),
    ("veN-miin", ["veL"], None),
    ("venus", ["veL", "veLLi"], None),
    ("pleiades", ["aru-", "miin"], None),
    ("ursa major", ["eZu-", "miin"], None),
    ("north star", ["vaTa", "miin"], None),
]


def _iconographic_anchor_score(inputs: dict, params: dict) -> dict:
    """Score Parpola's phoneme map against the 12 iconographic anchors.

    For each anchor (sign_id, iconic_reading, confidence):
      - If sign_id is in phoneme_map: check whether the phoneme value
        matches the iconic reading (miin/fish, vaTa/banyan, etc.).
      - Score: high-anchor + match = 2.0; medium-anchor + match = 1.0;
        match = 0.0 if phoneme/iconic disagree.

    Spec 087 S3 (family F4): the mechanism is the generic
    IconographicAnchorScorer engine (glossa_lab.generic_primitives);
    this node is its Phase-27 parameterisation (alias table above,
    weights 2.0/1.0/0.5 and the x1.5 high-confidence bonus as engine
    defaults, no allograph extension).
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        iconographic_anchor_scorer_execute,
    )

    merged = dict(params)
    merged["scorer_spec"] = {
        "alias_table": _ICONOGRAPHIC_ALIAS_TABLE,
        "verdict_template": (
            "Iconographic anchor score: {n_matches}/{n_total_anchors} anchors "
            "have a phoneme match in our map. Total weighted score = "
            "{total_score:.2f}. The anchors with the highest scores are "
            "non-statistical confirmations of the corresponding sign->phoneme "
            "reading (e.g. M-410: sign 47 = fish, confirmed by crocodile "
            "iconography)."
        ),
    }
    return iconographic_anchor_scorer_execute(inputs, merged)


# ── Tier 4 #10: 6-bucket period stratification ───────────────────────


# Phase-27 finer-grained period buckets (Phase-25c had 4-coarse, now 8)
_PERIOD_BUCKETS_6 = [
    ("Early Dynastic", ("early dynastic", "ed iiib", "ed iii")),
    ("Old Akkadian", ("old akkadian", "akkadian", "sargonic")),
    ("Lagash II", ("lagash ii", "gudea")),
    ("Ur III", ("ur iii", "ur 3", "neo-sumerian")),
    ("Old Babylonian", ("old babylonian",)),
    ("Middle Babylonian", ("middle babylonian", "kassite")),
    ("Neo-Assyrian", ("neo-assyrian", "neo assyrian", "nb period",
                      "neo-babylonian", "neo babylonian")),
    ("Ebla", ("ebla",)),
]


def _period_stratified_readout_6bucket(inputs: dict, params: dict) -> dict:
    """Phase-27 finer-grained period stratification: 8 buckets instead of 4
    (Early Dynastic, Old Akkadian, Lagash II, Ur III, Old Babylonian,
    Middle Babylonian, Neo-Assyrian, Ebla).

    Spec 087 S3 (family F5): the mechanism is the generic
    StratifiedPermutationTest engine (glossa_lab.generic_primitives);
    this node is its Phase-27 parameterisation. _PERIOD_BUCKETS_6
    above stays as the delegation data (seed base 271). The
    module-local _classify_period_6 / _run_bipartite_test /
    _greedy_score / _name_n_segments / _length_score helpers were
    used only here and by the decoder above; both consumers are
    engine delegations now, so the helpers were removed.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        stratified_permutation_test_execute,
    )

    merged = dict(params)
    merged["strata_spec"] = {
        "stratum_field": "period",
        "axis_key": "period",
        "strata_rules": _PERIOD_BUCKETS_6,
        "case_insensitive": True,
        "strip_value": False,
        "empty_bucket": "Unknown",
        "fallback_bucket": "Other",
        "seed_base": 271,
        "verdict_template": (
            "Period stratification (6-bucket Phase-27): {n_results} buckets "
            "tested; {n_significant} achieve p<0.05. Compares with Phase-25c "
            "(4-bucket: 3/4 + overall) at finer granularity."
        ),
    }
    return stratified_permutation_test_execute(inputs, merged)


# ── Tier 1 #2 + Tier 3 #6 combined: Shu-ilishu contact-zone filter ───


def _shu_ilishu_contact_zone_filter(inputs: dict, params: dict) -> dict:
    """Phase-27: ACTUALLY filter the 138 Phase-25e Shu-ilishu candidate
    inscriptions to those with contact-zone provenience, using the new
    catalogue_id-aware indus_cisi accessor."""
    set(inputs.get("contact_zone_prefixes") or [])
    findspot_map = inputs.get("findspot_map") or {}

    try:
        from glossa_lab.data.indus_cisi import (  # noqa: PLC0415
            get_corpus_inscriptions_with_ids,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"indus_cisi not available: {exc}",
                "n_filtered": 0}

    inscs = get_corpus_inscriptions_with_ids(min_length=3)
    # Keep only length 3-7 (Phase-25e criterion)
    inscs = [i for i in inscs if 3 <= len(i["signs"]) <= 7]

    contact_zone_inscs: list[dict] = []
    core_inscs: list[dict] = []
    for ins in inscs:
        cid = ins["catalogue_id"]
        is_contact = False
        site = "Unknown"
        for L in (4, 3, 2, 1):
            cand = cid[:L]
            info = findspot_map.get(cand)
            if info:
                is_contact = info.get("is_contact_zone", False)
                site = info.get("site", "Unknown")
                break
        rec = {
            "catalogue_id": cid,
            "n_signs": len(ins["signs"]),
            "signs": ins["signs"],
            "site": site,
            "is_contact_zone": is_contact,
        }
        if is_contact:
            contact_zone_inscs.append(rec)
        else:
            core_inscs.append(rec)

    sites_distribution: Counter[str] = Counter()
    for ins in inscs:
        cid = ins["catalogue_id"]
        for L in (4, 3, 2, 1):
            cand = cid[:L]
            info = findspot_map.get(cand)
            if info:
                sites_distribution[info.get("site", "Unknown")] += 1
                break
        else:
            sites_distribution["Unknown"] += 1

    verdict = (
        f"Shu-ilishu contact-zone filter (Phase-27): "
        f"{len(inscs)} Phase-25e candidate inscriptions (length 3-7) "
        f"resolved via catalogue_id. {len(contact_zone_inscs)} are from "
        f"contact-zone sites; {len(core_inscs)} are from Indus-core sites. "
        f"NOTE: the current indus_cisi corpus (179 inscriptions, all from "
        f"Mohenjo-daro) does NOT include any contact-zone seals -- those "
        f"are only in CISI Vol 3 Part 3 plates (not yet ingested with sign "
        f"sequences)."
    )
    return {
        "n_total_candidates": len(inscs),
        "n_contact_zone": len(contact_zone_inscs),
        "n_core_indus": len(core_inscs),
        "sites_distribution": dict(sites_distribution.most_common(15)),
        "contact_zone_inscriptions_top20": contact_zone_inscs[:20],
        "verdict": verdict,
    }


# ── Verdict aggregator ──────────────────────────────────────────────


def _phase27_verdict(inputs: dict, params: dict) -> dict:
    summary = (
        "Phase-27 contact-zone progress: indus_cisi corpus extended with "
        "catalogue_id-aware accessor (unblocks Shu-ilishu candidate "
        "filter); explicit find-spot overrides for Phase-22 hand-encoded "
        "seals (fixes Phase-26d mis-assignments); 12 iconographic anchors "
        "ingested from Parpola 2010 (M-410 fish=crocodile, H-9 ezhu-miin "
        "= Ursa Major, M-1202 muruku-piLLai, etc.); reverse Janabiyah "
        "search node ranks persons-v3 candidates against the 7-position "
        "Janabiyah skeleton; phoneme-VALUE permutation null extends the "
        "Bayesian decoder; 6-bucket period stratification (Early Dynastic, "
        "Old Akkadian, Lagash II, Ur III, Old Babylonian, Middle Babylonian, "
        "Neo-Assyrian, Ebla); phoneme map expanded 25 -> 30 entries; "
        "Parpola 1994 acquired (19 MB / 392 pages, the canonical sign-list "
        "reference); Crawford 2001 still inaccessible (login walls)."
    )
    next_steps = [
        "Phase-28 priority 1: ingest CISI Vol 3 Part 3 plates (the single "
        "remaining hard blocker for Bayesian decoder + blind held-out test). "
        "Approach: high-resolution plate scan + manual sign-ID assignment, "
        "or direct request to Parpola/Frenez/Laursen for digital catalogues.",
        "Phase-28 priority 2: process Parpola 1994 (acquired) for sign-by-"
        "sign readings of Chapter 10 ('fish' signs), Chapter 13 ('Murukan'), "
        "Chapter 14 ('Goddess') -- expand phoneme map from 30 to 50+ "
        "entries.",
        "Phase-28 priority 3: ingest Mahadevan 1977 sign-list as numerical "
        "Parpola-ID -> Mahadevan-ID crosswalk so we can resolve sign IDs "
        "across both numbering systems.",
        "Phase-28 priority 4: extend ReverseJanabiyahSearch to use the "
        "expanded phoneme map; report any new high-score candidates.",
        "Phase-28 priority 5: ingest CDLI provenience-and-period crosswalk "
        "to enable joint period * provenience stratification (3*8 = 24 "
        "subsets, much finer-grained robustness check).",
    ]
    return {
        "summary": summary,
        "next_steps": next_steps,
    }


# ── Atomic node defs for registration ───────────────────────────────


def _phase27_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "Phase27CorpusLoader", "Phase-27 Contact Corpus Loader",
            "Phase-27 / Sources",
            "Load Phase-27 contact-zone artefacts: extends Phase-26 with "
            "iconographic anchors (12 Parpola 2010 figures) and Phase-27 "
            "explicit find-spot overrides for Phase-22 hand-encoded seals.",
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
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase27_corpus_loader,
        ),
        AtomicNodeDef(
            "ReverseJanabiyahSearch",
            "Reverse Janabiyah Search (Phase-27)",
            "Phase-27 / Decipherment",
            "Reverse the Phase-25a/26c Janabiyah search direction: for each "
            "common Akkadian PN in the Meluhha context, score whether its "
            "segments match Janabiyah's predicted phonetic skeleton "
            "[?, miin, or?, miin, ?, ?, miin]. Smaller, more constrained "
            "search than the forward direction.",
            inputs=[
                {"name": "persons_v3", "type": "json", "required": True},
                {"name": "janabiyah_reading", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_candidates", "type": "number"},
                {"name": "n_with_position_match", "type": "number"},
                {"name": "n_with_free_miin", "type": "number"},
                {"name": "top_matches", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "top_k": {"type": "integer", "default": 20, "minimum": 5},
                },
            },
            fn=_reverse_janabiyah_search,
        ),
        AtomicNodeDef(
            "BayesianDecoderV2",
            "Bayesian Decoder V2 (phoneme-VALUE permutation, Phase-27)",
            "Phase-27 / Decipherment",
            "Extend Phase-26b: permute phoneme VALUES (miin, aru-, eZu-, "
            "vaTa-, muruku, etc.) across sign IDs (instead of just confidence "
            "labels) and score under a Dravidian compound-name plausibility "
            "metric.",
            inputs=[
                {"name": "inscribed_seals", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_seals", "type": "number"},
                {"name": "n_phonemes_in_map", "type": "number"},
                {"name": "observed_total_score", "type": "number"},
                {"name": "null_mean_score", "type": "number"},
                {"name": "p_value", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "interpretation", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000, "minimum": 200},
                    "seed": {"type": "integer", "default": 2727},
                },
            },
            fn=_bayesian_decoder_v2,
        ),
        AtomicNodeDef(
            "IconographicAnchorScore",
            "Iconographic Anchor Score (Phase-27)",
            "Phase-27 / Decipherment",
            "Score Parpola's phoneme map against 12 iconographic anchors "
            "from Parpola 2010 (M-410 fish=crocodile, H-9 ezhu-miin, "
            "M-1202 muruku-piLLai, etc.). Non-statistical confirmations "
            "of the iconic readings.",
            inputs=[
                {"name": "iconographic_anchors", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_total_anchors", "type": "number"},
                {"name": "n_matches", "type": "number"},
                {"name": "total_score", "type": "number"},
                {"name": "rows", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_iconographic_anchor_score,
        ),
        AtomicNodeDef(
            "PeriodStratifiedReadout6Bucket",
            "Period-Stratified Readout - 6-Bucket (Phase-27)",
            "Phase-27 / Decipherment",
            "Re-run Phase-25c bipartite readout test with finer-grained "
            "8-bucket period classification (Early Dynastic, Old Akkadian, "
            "Lagash II, Ur III, Old Babylonian, Middle Babylonian, "
            "Neo-Assyrian, Ebla) instead of Phase-25c's 4 buckets.",
            inputs=[
                {"name": "persons_v3", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "results", "type": "json"},
                {"name": "n_significant_strata", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000, "minimum": 100},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0},
                },
            },
            fn=_period_stratified_readout_6bucket,
        ),
        AtomicNodeDef(
            "ShuIlishuContactZoneFilter",
            "Shu-Ilishu Contact-Zone Filter (Phase-27)",
            "Phase-27 / Decipherment",
            "Filter the 138 Phase-25e Shu-ilishu candidate inscriptions "
            "(length 3-7) by contact-zone provenience, using the new "
            "catalogue_id-aware indus_cisi accessor.",
            inputs=[
                {"name": "contact_zone_prefixes", "type": "json", "required": True},
                {"name": "findspot_map", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_total_candidates", "type": "number"},
                {"name": "n_contact_zone", "type": "number"},
                {"name": "n_core_indus", "type": "number"},
                {"name": "sites_distribution", "type": "json"},
                {"name": "contact_zone_inscriptions_top20", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_shu_ilishu_contact_zone_filter,
        ),
        AtomicNodeDef(
            "Phase27Verdict", "Phase-27 Verdict Aggregator",
            "Phase-27 / Reporters",
            "Aggregate Phase-27 sub-experiment outputs into a "
            "decipherment-progress verdict + Phase-28 priority list.",
            inputs=[],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "next_steps", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase27_verdict,
        ),
    ]


__all__ = [
    "_phase27_corpus_loader",
    "_reverse_janabiyah_search",
    "_bayesian_decoder_v2",
    "_iconographic_anchor_score",
    "_period_stratified_readout_6bucket",
    "_shu_ilishu_contact_zone_filter",
    "_phase27_verdict",
    "_phase27_node_defs",
]
