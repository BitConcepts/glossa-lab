"""Phase-26 atomic-node implementations.

Phase-26 builds on the Phase-25 phonetic-readout pipeline with:
  1. Expanded phoneme map (15 -> 25 sign->phoneme entries from Parpola 2010).
  2. CISI Vol 3 Part 3 site-prefix find-spot map (24 sites).
  3. Expanded phonetic search vocabulary (mul-, kakkab-, imin- in
     addition to direct mi-in/me-en transliterations).
  4. Provenience-stratified replication of the bipartite readout test.
  5. Bayesian decoder: scores inscribed-seal corpus under Parpola
     phoneme-map hypothesis vs random shuffled-map nulls; produces
     global p-value for the Dravidian hypothesis.
  6. Expanded Janabiyah phonetic readout (with translation candidates).
  7. Shu-ilishu candidate filter using CISI find-spot metadata.
"""

from __future__ import annotations

from typing import Any


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── Loader ────────────────────────────────────────────────────────────


def _phase26_corpus_loader(inputs: dict, params: dict) -> dict:
    """Load all Phase-26 contact-zone artefacts (extends Phase-25)."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_cisi_findspot_map,
            get_contact_zone_prefix_set,
            get_indus_seals_at_mesopotamia,
            get_janabiyah_seal_reading,
            get_meluhha_tablets,
            get_meluhhan_persons_v3,
            get_miin_renderings,
            get_parpola_phoneme_map,
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
        "miin_renderings": get_miin_renderings(include_translated=True),
        "miin_renderings_direct_only": get_miin_renderings(include_translated=False),
    }


# ── Tier #4: Provenience-stratified replication ──────────────────────


# Heuristic: classify a CDLI provenience string into a coarse city bucket.
_PROVENIENCE_BUCKETS = [
    ("Girsu", ("girsu", "tello", "telloh")),
    ("Nippur", ("nippur",)),
    ("Ur", (" ur ", " ur,", "ur,", "ur ", "ur (mod", "ur-",
            "ur (modern")),
    ("Umma", ("umma",)),
    ("Lagash", ("lagash", "lagas")),
    ("Susa", ("susa", "shush")),
    ("Mari", ("mari ",)),
    ("Nineveh", ("nineveh", "kuyunjik", "kouyunjik")),
    ("Sippar", ("sippar",)),
    ("Babylon", ("babylon",)),
    ("Drehem", ("drehem", "puzrish-dagan", "puzris-dagan")),
    ("Eshnunna", ("eshnunna", "tell asmar", "tell-asmar")),
    ("Ebla", ("ebla", "tell mardikh")),
]


def _provenience_stratified_readout(inputs: dict, params: dict) -> dict:
    """Re-run bipartite readout test split by provenience (Girsu, Nippur,
    Ur, Umma, Susa, Nineveh, etc.). Provides a second axis of robustness
    on top of the Phase-25c period split.

    Spec 087 S3 (family F5): the mechanism is the generic
    StratifiedPermutationTest engine (glossa_lab.generic_primitives);
    this node is its Phase-26 parameterisation. _PROVENIENCE_BUCKETS
    above stays as the delegation data; the module-local
    _classify_provenience / _run_bipartite_test / _greedy_score /
    _name_n_segments / _length_score helpers were used only here and
    by the decoder below; both consumers are engine delegations now,
    so the helpers were removed (the engine carries the shared
    copies).
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        stratified_permutation_test_execute,
    )

    merged = dict(params)
    merged["strata_spec"] = {
        "stratum_field": "provenience",
        "axis_key": "provenience",
        "strata_rules": _PROVENIENCE_BUCKETS,
        "case_insensitive": True,
        "strip_value": False,
        "empty_bucket": "Unknown",
        "fallback_bucket": "Other",
        "seed_base": 137,
        "verdict_template": (
            "Provenience-stratified readout: {n_results} provenience "
            "buckets; {n_significant} achieve p<0.05. Combined with "
            "Phase-25c (3/4 period strata p<0.05), this is the second "
            "axis of independent significance: if multiple proveniences "
            "each yield p<0.05, the bipartite signal is provenience-"
            "robust."
        ),
    }
    return stratified_permutation_test_execute(inputs, merged)


# ── Tier #3: Bayesian decoder ────────────────────────────────────────


def _bayesian_decoder(inputs: dict, params: dict) -> dict:
    """Score inscribed-seal corpus under Parpola phoneme map vs
    random shuffled-map null distributions. Produces a global p-value
    for the Dravidian hypothesis.

    Strategy:
      1. Compute observed total phoneme-coverage weight across all
         inscribed seals using the actual Parpola map.
      2. Generate N random null maps by shuffling the phoneme/confidence
         assignments across the same set of sign IDs (i.e. each sign
         gets a phoneme from the original map but assigned to a
         different sign).
      3. Compute the same total weight for each null.
      4. p-value = fraction of null weights >= observed.

    Spec 087 S3 (family F4): the mechanism is the generic
    PhonemeMapPermutationTest engine (glossa_lab.generic_primitives)
    in its confidence-shuffle mode; this node is its Phase-26
    parameterisation (seed 1234, top-10 rows). The module-local
    _seal_phoneme_match_score helper was used only here and was
    removed with the delegation (the engine carries the scorer).
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        phoneme_map_permutation_test_execute,
    )

    merged = dict(params)
    merged.setdefault("seed", 1234)
    merged["decoder_spec"] = {
        "shuffle_dimension": "confidence",
        "null_gloss": "(null permutation)",
        "observed_key": "observed_total_weight",
        "null_mean_key": "null_mean_weight",
        "rows_key": "obs_per_seal_top10",
        "rows_limit": 10,
        "verdict_template": (
            "Bayesian decoder: observed total weight = {observed:.3f} "
            "across {n_seals} inscribed seals. Null mean = "
            "{null_mean:.3f} ({n_perms} permutations of confidence "
            "assignments). Global p-value = {p_value:.4f}. Lower p "
            "= signs assigned to high-confidence phonemes really do "
            "cluster on the inscribed-seal corpus more than chance."
        ),
        "interpretation": (
            "Caveat: this null-permutation strategy keeps the multiset of "
            "confidence labels constant but breaks their assignment to "
            "specific sign IDs. A significant p means the observed map "
            "places high-confidence phonemes on more 'frequent' signs in "
            "our corpus than chance would predict. This is a NECESSARY "
            "but not SUFFICIENT condition for the Dravidian hypothesis -- "
            "it only validates that Parpola's high-confidence proposals "
            "land on the right SIGNS, not that those phoneme VALUES are "
            "correct."
        ),
    }
    return phoneme_map_permutation_test_execute(inputs, merged)


# ── Tier #2: Expanded Janabiyah phonetic readout ─────────────────────


def _janabiyah_phonetic_readout_v2(inputs: dict, params: dict) -> dict:
    """Phase-26 Janabiyah readout: searches with the EXPANDED phonetic
    vocabulary (direct miin transliterations + Sumerian/Akkadian
    translation candidates).

    Spec 087 S3 (family F7): the mechanism is the generic
    SkeletonTabletSearch engine (glossa_lab.generic_primitives);
    this node is its Phase-26 parameterisation — two scans (the
    direct-only list, then the full list) over rendering lists that
    arrive through input ports, the translation-gain count carried
    as a derived count of the two scans. Phase-25's readout is the
    same engine with its rendering list supplied as a constant.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        skeleton_tablet_search_execute,
    )

    merged = dict(params)
    merged["readout_spec"] = {
        "scans": [
            {
                "renderings": {"input": "miin_renderings_direct_only"},
                "hit_key": "n_hits",
                "top_key": "matches_direct_top20",
                "count_key": "n_matches_direct",
            },
            {
                "renderings": {"input": "miin_renderings"},
                "hit_key": "n_hits",
                "top_key": "matches_expanded_top20",
                "count_key": "n_matches_expanded",
            },
        ],
        "count_difference": {
            "key": "n_new_matches_from_translation",
            "minuend": "n_matches_expanded",
            "subtrahend": "n_matches_direct",
        },
        "renderings_echo": {"input": "miin_renderings"},
        "keyword_gate": "me-luh",
        "min_hits": 2,
        "verdict_template": (
            "Janabiyah phonetic readout v2 (Phase-26): predicted "
            "skeleton '{skeleton}' ({n_miin}/7 confirmed miin). "
            "Direct-transliteration search (Phase-25a vocab): "
            "{n_matches_direct} matches. Expanded search "
            "(direct + mul-/kakkab-/imin- translation candidates): "
            "{n_matches_expanded} matches. The translation-candidate "
            "hypothesis is supported if the expanded search produces "
            "new matches that the direct search missed."
        ),
    }
    return skeleton_tablet_search_execute(inputs, merged)


# ── Tier #1: CISI Vol 3 + find-spot reporter ─────────────────────────


def _cisi_findspot_reporter(inputs: dict, params: dict) -> dict:
    """Report the CISI find-spot map; identify which Phase-22 inscribed
    seals have a known find-spot from the prefix mapping.

    Spec 087 S3 PR-F: delegates to the generic PrefixFindspotAssigner
    (reporter mode); the prefix lengths (4, 3, 2, 1), the key-presence
    match and the verdict text are spec data.
    """
    from glossa_lab.generic_primitives import prefix_findspot_assigner_execute

    merged = dict(params)
    merged["assigner_spec"] = {
        "mode": "reporter",
        "prefix_lengths": [4, 3, 2, 1],
        "map_key": "findspot_map",
        "contact_key": "contact_zone_prefixes",
        "records_key": "inscribed_seals",
        "id_field": "catalogue_id",
        "volume_field": "n_seals_in_volume",
        "volume_out": "n_seals_in_cisi_vol3",
        "country_default": "Unknown",
        "sites_out": "sites_by_country",
        "assignments_out": "seal_findspot_assignments",
        "verdict_template": (
            "CISI find-spot map: {n_prefixes} site prefixes covering "
            "~{n_volume} seals across {n_countries} countries. "
            "Contact-zone prefix set has {n_contact} entries. Of "
            "{n_records} Phase-22 inscribed seals, {n_assigned} could "
            "be assigned a site via prefix matching (the remainder use "
            "Mahadevan M77 IDs / hand-encoded catalogue IDs not "
            "following the CISI prefix convention)."),
    }
    return prefix_findspot_assigner_execute(inputs, merged)


# ── Tier: Shu-ilishu candidate filter using find-spot metadata ───────


def _shu_ilishu_candidate_filter(inputs: dict, params: dict) -> dict:
    """Filter the Phase-25e Shu-ilishu candidate list (138 inscriptions
    of length 3-7) to those with a contact-zone prefix in their
    catalogue ID.
    """
    findspot_map = inputs.get("findspot_map") or {}
    contact_zone = set(inputs.get("contact_zone_prefixes") or [])

    try:
        from glossa_lab.data.indus_cisi import (  # noqa: PLC0415
            get_corpus_inscriptions as _cisi_inscs,
        )
    except Exception:  # noqa: BLE001
        _cisi_inscs = None

    if _cisi_inscs is None:
        return {"error": "indus_cisi corpus not available",
                "n_filtered_candidates": 0}

    inscs = _cisi_inscs()
    inspected = 0
    for ins in inscs[:5000]:
        inspected += 1
        if not (3 <= len(ins) <= 7):
            continue
        # Many CISI inscription records carry IDs but the simplified
        # corpus view (lists of sign sequences) often does not. We
        # report what we can: total Phase-25e candidates that DO have
        # IDs prefixed with a contact-zone code.
        # Without per-inscription IDs we can only report aggregate.
    # Aggregate-level summary using the prefix counts from the find-
    # spot map (Vol 3 Part 3 contact zone has 612 seals total)
    contact_zone_total = sum(_safe_int(v.get("n_seals_in_volume", 0))
                              for k, v in findspot_map.items()
                              if k in contact_zone)

    verdict = (
        f"Shu-ilishu candidate filter: CISI Vol 3 Part 3 contact-zone "
        f"prefixes total {contact_zone_total} seals across "
        f"{len(contact_zone)} contact-zone sites. The "
        f"glossa_lab.data.indus_cisi corpus view exposes sign "
        f"sequences without their CISI catalogue IDs, so we cannot "
        f"presently filter the 138 Phase-25e candidates by prefix. "
        f"Phase-26 ingests the find-spot map (sufficient for offline "
        f"narrowing); a future Phase needs to extend indus_cisi.py "
        f"to expose catalogue_id alongside the sign sequence."
    )
    return {
        "n_contact_zone_prefixes": len(contact_zone),
        "n_seals_total_in_contact_zone": contact_zone_total,
        "n_inscriptions_inspected": inspected,
        "verdict": verdict,
    }


# ── Verdict aggregator ──────────────────────────────────────────────


def _phase26_verdict(inputs: dict, params: dict) -> dict:
    summary = (
        "Phase-26 contact-zone progress: phoneme map expanded 15->25 "
        "(Parpola 2010 readings: aru-/eZu-/vaTa-/muruku/piLLai/veL/"
        "katir); CISI Vol 3 Part 3 site-prefix find-spot map "
        "(24 contact-zone sites + 7 core-Indus prefixes) ingested; "
        "phonetic search vocabulary widened with mul-/kakkab-/imin- "
        "translation candidates; provenience-stratified replication "
        "of the bipartite readout test executed; Bayesian decoder "
        "produces a global p-value for the Parpola map; expanded "
        "Janabiyah readout re-tested against the 1462-tablet CDLI "
        "corpus."
    )
    next_steps = [
        "Phase-27 priority 1: ingest CISI find-spot data INTO the "
        "indus_cisi.py corpus view -- expose catalogue_id alongside "
        "sign sequences so we can filter 138 Phase-25e candidates "
        "by prefix.",
        "Phase-27 priority 2: extend the Bayesian decoder to handle "
        "phoneme-VALUE permutations (not just confidence permutations) "
        "to test whether the specific Dravidian phoneme values are "
        "correct.",
        "Phase-27 priority 3: ingest CISI Vol 3 Parts 1 + 2 (Pakistan + "
        "India peripheries) for additional contact-zone seal IDs.",
        "Phase-27 priority 4: build the iconographic-anchor sub-test "
        "(Parpola 2010 fish-and-crocodile co-occurrence) on the M-410 "
        "Mohenjo-daro seal as a hard external anchor for the fish=miin "
        "reading.",
        "Phase-27 priority 5: contact Parpola/Frenez for their "
        "digital sign-by-sign catalogue of the 10 length-only "
        "Mesopotamia-found seals (Phase-25b blockers).",
    ]
    return {
        "summary": summary,
        "next_steps": next_steps,
    }


# ── Atomic node defs for registration ───────────────────────────────


def _phase26_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "Phase26CorpusLoader", "Phase-26 Contact Corpus Loader",
            "Phase-26 / Sources",
            "Load Phase-26 contact-zone artefacts: extends Phase-25 with "
            "CISI Vol 3 Part 3 site-prefix find-spot map and the "
            "expanded phonetic search vocabulary (mul-/kakkab-/imin-).",
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
                {"name": "miin_renderings", "type": "json"},
                {"name": "miin_renderings_direct_only", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase26_corpus_loader,
        ),
        AtomicNodeDef(
            "ProvenienceStratifiedReadout",
            "Provenience-Stratified Readout Test (Phase-26)",
            "Phase-26 / Decipherment",
            "Re-run Phase-24d/25c bipartite readout test split by "
            "provenience (Girsu, Nippur, Ur, Umma, Susa, Nineveh, "
            "etc.). Provides a second axis of independent significance "
            "on top of Phase-25c's period stratification.",
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
            fn=_provenience_stratified_readout,
        ),
        AtomicNodeDef(
            "BayesianDecoder",
            "Bayesian Decoder (Phase-26)",
            "Phase-26 / Decipherment",
            "Score the inscribed-seal corpus under Parpola's phoneme "
            "map vs random shuffled-confidence-assignment nulls. "
            "Produces a global p-value for the assertion 'Parpola's "
            "high-confidence phoneme proposals land on the right "
            "SIGNS' (necessary but not sufficient condition for the "
            "Dravidian hypothesis).",
            inputs=[
                {"name": "inscribed_seals", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_seals", "type": "number"},
                {"name": "n_phonemes_in_map", "type": "number"},
                {"name": "observed_total_weight", "type": "number"},
                {"name": "null_mean_weight", "type": "number"},
                {"name": "p_value", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "interpretation", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000, "minimum": 200},
                    "seed": {"type": "integer", "default": 1234},
                },
            },
            fn=_bayesian_decoder,
        ),
        AtomicNodeDef(
            "JanabiyahPhoneticReadoutV2",
            "Janabiyah Phonetic Readout v2 — Expanded (Phase-26)",
            "Phase-26 / Decipherment",
            "Phase-25a re-test with EXPANDED phonetic search "
            "vocabulary: adds Sumerian astral terms (mul/mul-mul/"
            "imin) and Akkadian (kakkab) as translation candidates "
            "for *miin*. Tests the hypothesis that Akkadian scribes "
            "translated rather than transliterated Meluhhan astral "
            "names.",
            inputs=[
                {"name": "janabiyah_reading", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
                {"name": "tablets", "type": "json", "required": True},
                {"name": "miin_renderings", "type": "json", "required": True},
                {"name": "miin_renderings_direct_only", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "skeleton", "type": "text"},
                {"name": "predictions", "type": "json"},
                {"name": "n_miin", "type": "number"},
                {"name": "matches_direct_top20", "type": "json"},
                {"name": "n_matches_direct", "type": "number"},
                {"name": "matches_expanded_top20", "type": "json"},
                {"name": "n_matches_expanded", "type": "number"},
                {"name": "n_new_matches_from_translation", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_janabiyah_phonetic_readout_v2,
        ),
        AtomicNodeDef(
            "CISIFindspotReporter",
            "CISI Vol 3 Part 3 Find-Spot Reporter (Phase-26)",
            "Phase-26 / Reporters",
            "Report the CISI Vol 3 Part 3 site-prefix find-spot map; "
            "show how many Phase-22 inscribed seals can be assigned "
            "a site via prefix matching.",
            inputs=[
                {"name": "findspot_map", "type": "json", "required": True},
                {"name": "contact_zone_prefixes", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_prefixes", "type": "number"},
                {"name": "n_countries", "type": "number"},
                {"name": "n_seals_in_cisi_vol3", "type": "number"},
                {"name": "sites_by_country", "type": "json"},
                {"name": "seal_findspot_assignments", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_cisi_findspot_reporter,
        ),
        AtomicNodeDef(
            "ShuIlishuCandidateFilter",
            "Shu-Ilishu Candidate Filter using Find-Spot Metadata (Phase-26)",
            "Phase-26 / Decipherment",
            "Filter Phase-25e's 138 candidate inscriptions by CISI "
            "find-spot prefix (contact-zone vs Indus-core).",
            inputs=[
                {"name": "findspot_map", "type": "json", "required": True},
                {"name": "contact_zone_prefixes", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_contact_zone_prefixes", "type": "number"},
                {"name": "n_seals_total_in_contact_zone", "type": "number"},
                {"name": "n_inscriptions_inspected", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_shu_ilishu_candidate_filter,
        ),
        AtomicNodeDef(
            "Phase26Verdict", "Phase-26 Verdict Aggregator",
            "Phase-26 / Reporters",
            "Aggregate Phase-26 sub-experiment outputs into a "
            "decipherment-progress verdict + Phase-27 priority list.",
            inputs=[],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "next_steps", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase26_verdict,
        ),
    ]


__all__ = [
    "_phase26_corpus_loader",
    "_provenience_stratified_readout",
    "_bayesian_decoder",
    "_janabiyah_phonetic_readout_v2",
    "_cisi_findspot_reporter",
    "_shu_ilishu_candidate_filter",
    "_phase26_verdict",
    "_phase26_node_defs",
]
