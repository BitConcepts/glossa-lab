"""Phase-131 (spec 022) — source-of-disagreement attribution tests.

Toy hand-computed controls for every arm (matcher tiers,
alignment classes, estimability gates, Arm B reversal,
Arm C strata + reweighting, Arm D synthesis rules),
determinism, and real-input pins (the Phase-125 judgeable
set is exactly its 16 PRIMARY pairs; observed median TV
0.636931; the Phase-127 noise band is [0.046665, 0.131316]).
This phase is attribution diagnostics ONLY: nothing here
re-scores Phase-125 or touches spec 020's NO.
"""
from __future__ import annotations

import json
from pathlib import Path

from glossa_lab.phase131_attribution import (
    CLS_INDEL, CLS_MERGE, CLS_ORDER_ONLY, CLS_SPLIT, CLS_SUBSTITUTION,
    NOISE_BAND_HI, NOISE_BAND_LO, NOISE_BAND_MEDIAN, OBSERVED_MEDIAN_TV,
    adjusted_profiles, align, block_token_totals, classify_pair,
    difference_blocks, direction_supports, length_bin, levenshtein,
    mapped_sequence, match_objects, matched_object_tv, matched_tv_gate,
    primary_map, reversed_median_tv, similarity, stratum_tv, synthesis,
)

_REPO = Path(__file__).resolve().parents[2]
_P125 = _REPO / "reports" / "phase125_cross_compilation_results.json"
_P127 = _REPO / "reports" / "phase127_cross_compilation_diagnostic_results.json"


def _pair(p, m):
    return {"parpola_id": p, "mahadevan_id": m}


PAIRS16_TOY = [_pair("P1", "M1"), _pair("P2", "M2")]


# ── Map + eligibility ─────────────────────────────────────

def test_mapped_sequence_all_or_nothing():
    pmap = {"P1": "M1", "P2": "M2"}
    assert mapped_sequence(["P1", "P2"], pmap) == ["M1", "M2"]
    assert mapped_sequence(["P1", "P9"], pmap) is None


def test_primary_map_real_crosswalk():
    from glossa_lab.data import parpola_mahadevan_crosswalk_v1 as xw
    pmap = primary_map(xw.load_crosswalk())
    assert len(pmap) == 286  # Phase-125 PRIMARY pairs of record


def test_mayig_eligibility_pin():
    from glossa_lab.data import mayig_layer as ml
    from glossa_lab.data import parpola_mahadevan_crosswalk_v1 as xw
    pmap = primary_map(xw.load_crosswalk())
    recs = ml.load_inscriptions()
    eligible = [r for r in recs
                if mapped_sequence(r["tokens"], pmap) is not None]
    assert len(recs) == 179
    assert len(eligible) == 32  # spec 022 Appendix A design count


# ── Alignment machinery ───────────────────────────────────

def test_levenshtein_and_similarity():
    assert levenshtein(["A", "B"], ["A", "B"]) == 0
    assert levenshtein(["A", "B"], ["A", "C"]) == 1
    assert levenshtein(["A"], ["A", "B"]) == 1
    assert levenshtein([], ["A"]) == 1
    assert similarity(["A", "B"], ["A", "B"]) == 1.0
    assert similarity(["A", "B"], ["C", "D"]) == 0.0


def _blocks(a, b):
    return difference_blocks(align(a, b))


def test_align_identical():
    cols = align(["A", "B"], ["A", "B"])
    assert all(c["op"] == "match" for c in cols)
    assert _blocks(["A", "B"], ["A", "B"]) == []
    assert classify_pair(["A", "B"], ["A", "B"], []) == "identical"


def test_align_substitution_block():
    blocks = _blocks(["A", "B", "C"], ["A", "X", "C"])
    assert len(blocks) == 1
    assert blocks[0]["class"] == CLS_SUBSTITUTION
    assert (blocks[0]["p"], blocks[0]["q"]) == (1, 1)


def test_align_split_block():
    # A vs A,B in place of one position: diagonal preference makes
    # the block (1 a-token, 2 b-tokens) -> segmentation split.
    blocks = _blocks(["A", "B", "C"], ["A", "B", "X", "C"])
    assert len(blocks) == 1
    assert blocks[0]["class"] in (CLS_SPLIT, CLS_INDEL)
    # explicit 1->2 substitution+insertion run with no matches inside
    blocks2 = _blocks(["A", "Z", "C"], ["A", "X", "Y", "C"])
    assert len(blocks2) == 1
    assert blocks2[0]["class"] == CLS_SPLIT
    assert (blocks2[0]["p"], blocks2[0]["q"]) == (1, 2)


def test_align_merge_block():
    blocks = _blocks(["A", "X", "Y", "C"], ["A", "Z", "C"])
    assert len(blocks) == 1
    assert blocks[0]["class"] == CLS_MERGE
    assert (blocks[0]["p"], blocks[0]["q"]) == (2, 1)


def test_align_indel_block():
    blocks = _blocks(["A", "B", "C"], ["A", "C"])
    assert len(blocks) == 1
    assert blocks[0]["class"] == CLS_INDEL
    assert (blocks[0]["p"], blocks[0]["q"]) == (1, 0)


def test_align_determinism_tiebreak():
    a, b = ["A", "B", "A"], ["B", "A", "B"]
    assert align(a, b) == align(a, b)


def test_classify_order_only_priority():
    a, b = ["A", "B", "C"], ["C", "B", "A"]
    blocks = _blocks(a, b)
    assert classify_pair(a, b, blocks) == CLS_ORDER_ONLY


# ── Matcher tiers ─────────────────────────────────────────

def _elig(i, seq):
    return {"id": f"M-{i}", "mapped": seq}


def _hol(j, seq):
    return {"key": f"K-{j}", "tokens": seq}


def test_matcher_exact_tier():
    out = match_objects([_elig(1, ["A", "B"])],
                        [_hol(1, ["A", "B"]), _hol(2, ["C"])])
    assert out["n_matched"] == 1
    assert out["pairs"][0]["tier"] == "EXACT"
    assert out["pairs"][0]["pair_class"] == "identical"


def test_matcher_exact_rev_tier():
    out = match_objects([_elig(1, ["A", "B"])],
                        [_hol(1, ["B", "A"])])
    assert out["n_matched"] == 1
    assert out["pairs"][0]["tier"] == "EXACT-REV"
    assert out["pairs"][0]["pair_class"] == "identical"


def test_matcher_no_match_below_threshold():
    out = match_objects([_elig(1, ["A", "B", "C", "D", "E"])],
                        [_hol(1, ["V", "W", "X", "Y", "Z"])])
    assert out["n_matched"] == 0


def test_matcher_near_tier_mutual_best():
    # 4/5 tokens agree -> similarity 0.8, mutual best
    out = match_objects([_elig(1, ["A", "B", "C", "D", "E"])],
                        [_hol(1, ["A", "B", "C", "D", "Z"]),
                         _hol(2, ["V", "W", "X", "Y", "Q"])])
    assert out["n_matched"] == 1
    assert out["pairs"][0]["tier"] == "NEAR"
    assert out["pairs"][0]["pair_class"] == CLS_SUBSTITUTION


def test_matcher_nonunique_exact_excluded():
    # eligible seq equals two identical Holdat inscriptions:
    # not mutually unique -> no EXACT match.
    out = match_objects([_elig(1, ["A", "B"])],
                        [_hol(1, ["A", "B"]), _hol(2, ["A", "B"])])
    assert out["tier_counts"].get("EXACT", 0) == 0


# ── Matched-object TV gates ───────────────────────────────

def test_matched_tv_gate():
    assert matched_tv_gate(10, 4) is True
    assert matched_tv_gate(9, 16) is False
    assert matched_tv_gate(10, 3) is False
    assert matched_tv_gate(0, 0) is False


def test_matched_object_tv_defined_pairs():
    may = [["P1", "P2", "P1"]]
    hol = [["M1", "M2", "M1"]]
    out = matched_object_tv(may, hol, PAIRS16_TOY)
    assert out["n_defined"] == 2
    assert out["median_tv_defined"] == 0.0


# ── Arm B ─────────────────────────────────────────────────

def test_direction_support_criterion():
    assert direction_supports(0.131316) is True
    assert direction_supports(0.131317) is False
    assert direction_supports(None) is False
    assert NOISE_BAND_HI == 0.131316


def test_arm_b_reversal_collapses_direction_only_toy():
    # mayig and Holdat agree except orientation: profiles swap
    # INITIAL/TERMINAL under reversal, so reversed TV collapses.
    may = [["P1", "P2", "P3"]] * 8 + [["P1", "P2"]] * 8
    hol = [["M3", "M2", "M1"]] * 8 + [["M2", "M1"]] * 8
    pairs = [_pair("P1", "M1"), _pair("P2", "M2"), _pair("P3", "M3")]
    base = reversed_median_tv(may, hol, pairs, "none")
    b2 = reversed_median_tv(may, hol, pairs, "holdat")
    # P3/M3 counts are 8 (<-> floor met on the 3-token rows only)
    assert b2["median_tv"] == 0.0
    assert base["median_tv"] > b2["median_tv"]


def test_arm_b_counts_invariant_under_reversal():
    may = [["P1", "P2"]] * 8
    hol = [["M1", "M2"]] * 8
    pairs = [_pair("P1", "M1"), _pair("P2", "M2")]
    for side in ("none", "mayig", "holdat"):
        ev = reversed_median_tv(may, hol, pairs, side)
        assert ev["n_judgeable"] == 2


# ── Arm C ─────────────────────────────────────────────────

def test_length_bins():
    assert length_bin(1) == "1"
    assert length_bin(2) == "2-3"
    assert length_bin(3) == "2-3"
    assert length_bin(5) == "4-5"
    assert length_bin(6) == "6+"


def test_stratum_tv_not_estimable_when_sparse():
    may = [["P1", "P2"]]
    hol = [["M1", "M2"]]
    out = stratum_tv(may, hol, PAIRS16_TOY)
    assert out["estimable"] is False
    assert out["status"] == "NOT ESTIMABLE"
    assert out["median_tv"] is None
    assert out["n_judgeable"] == 0  # below floor 8 in-stratum


def test_stratum_tv_empty_mayig_side():
    out = stratum_tv([], [["M1", "M2"]] * 20, PAIRS16_TOY)
    assert out["n_mayig_inscriptions"] == 0
    assert out["estimable"] is False
    assert out["status"] == "NOT ESTIMABLE"


def test_adjusted_profiles_toy():
    # Holdat length composition differs; mayig all length 2.
    may = [["P1", "P2"]] * 10
    hol = ([["M1", "M2"]] * 10            # bin 2-3, M1 initial
           + [["M9", "M9", "M9", "M9", "M1", "M9"]] * 10)  # bin 6+
    pairs = [_pair("P1", "M1"), _pair("P2", "M2")]
    out = adjusted_profiles(may, hol, pairs)
    assert out["weights_mayig_length_bins"]["2-3"] == 1.0
    rec = {r["parpola_id"]: r for r in out["records"]}
    # adjusted M1 profile uses only the 2-3 bin: M1 initial there
    assert rec["P1"]["adjusted_holdat_profile"] == [1.0, 0.0, 0.0]
    assert rec["P1"]["coverage"] == 1.0
    assert rec["P1"]["bins_used"] == ["2-3"]


# ── Arm D synthesis ───────────────────────────────────────

def _synth_input(matched_pairs, totals, b1, b2, adj_estimable=True,
                 adj_tv=0.4, mtv=None):
    matched = {"n_matched": matched_pairs, "block_token_totals": totals,
               "pairs": []}
    return synthesis(matched, {"b1_median_tv": b1, "b2_median_tv": b2},
                     {"estimable": adj_estimable, "median_tv": adj_tv},
                     matched_tv=mtv)


def test_synthesis_arm_a_not_estimable_below_min_matched():
    out = _synth_input(2, {"all_difference_blocks": 10,
                           CLS_SUBSTITUTION: 10}, 0.6, 0.6)
    for row in ("segmentation", "substitution", "insertion_deletion"):
        assert out["rows"][row]["status"] == "NOT ESTIMABLE"
        assert out["rows"][row]["share"] is None
    # direction: neither arm <= band -> credited 0.000, still estimable row
    assert out["rows"]["order_direction"]["share"] == 0.0
    assert out["rows"]["order_direction"]["supporting_arm"] is None


def test_synthesis_shares_and_residual():
    totals = {"all_difference_blocks": 100, CLS_SPLIT: 10,
              CLS_MERGE: 10, CLS_SUBSTITUTION: 50, CLS_INDEL: 30}
    mtv = {"median_tv": 0.318466, "estimable": True}
    out = _synth_input(20, totals, 0.1, 0.5, adj_tv=0.636931, mtv=mtv)
    assert out["rows"]["segmentation"]["share"] == 0.2
    assert out["rows"]["substitution"]["share"] == 0.5
    assert out["rows"]["insertion_deletion"]["share"] == 0.3
    assert out["rows"]["order_direction"]["share"] == round(
        (OBSERVED_MEDIAN_TV - 0.1) / OBSERVED_MEDIAN_TV, 6)
    assert out["rows"]["composition"]["share"] == 0.0
    assert out["rows"]["matched_object_residual"]["share"] == round(
        0.318466 / OBSERVED_MEDIAN_TV, 6)
    # residual floored at 0, never negative, shares never rescaled
    assert out["residual_unexplained_share"] == 0.0


def test_synthesis_composition_not_estimable():
    out = _synth_input(0, {}, None, None, adj_estimable=False, adj_tv=None)
    assert out["rows"]["composition"]["status"] == "NOT ESTIMABLE"
    assert out["rows"]["matched_object_residual"]["status"] == \
        "NOT ESTIMABLE"


def test_block_token_totals():
    pairs = [{"blocks": [{"class": CLS_SPLIT, "n_tokens": 3},
                         {"class": CLS_INDEL, "n_tokens": 1}]}]
    totals = block_token_totals(pairs)
    assert totals[CLS_SPLIT] == 3
    assert totals["all_difference_blocks"] == 4


# ── Real-input pins + H23 registration ────────────────────

def test_phase125_record_pins():
    p125 = json.loads(_P125.read_text(encoding="utf-8"))
    assert p125["verdict"]["verdict"] == "FAIL"
    stats = p125["arms"]["primary"]["stats"]
    assert stats["n_judgeable"] == 16
    assert stats["median_tv"] == OBSERVED_MEDIAN_TV == 0.636931


def test_phase127_noise_band_pins():
    p127 = json.loads(_P127.read_text(encoding="utf-8"))
    band = p127["arms"]["b_matched_size"]["median_tv_distribution"]
    assert band["median"] == NOISE_BAND_MEDIAN == 0.082613
    assert band["ci95_lo"] == NOISE_BAND_LO == 0.046665
    assert band["ci95_hi"] == NOISE_BAND_HI == 0.131316


def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase131Attribution" in ATOMIC_NODES
