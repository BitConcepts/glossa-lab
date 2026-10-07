"""Phase-116 (spec 015) unit tests: matcher tiers, profile
conventions, W1/Spearman helpers, verdict-rule boundaries, and
the H23 graph-registration assertion."""
from __future__ import annotations

from glossa_lab.phase116_harmonization import (
    _compatible, assemble_recommendation, bh_qvalues, modal_bin,
    run_matcher, spearman, verdict_composition, verdict_d1,
    verdict_definition, verdict_mapping, verdict_s1, wasserstein1,
)


def _rec(tokens, row=0):
    return {"tokens": tokens, "row": row, "cisi": "X-1",
            "status": "kept"}


def test_compatible_wildcard_and_mapped_floor():
    assert _compatible(["M1", "M2", "M3"], ["M1", "UNK", "M3"])
    assert not _compatible(["M1", "M2", "M3"], ["M1", "UNK", "UNK"])
    assert not _compatible(["M1", "M2"], ["M1", "UNK", "M3"])
    assert not _compatible(["M1", "M2", "M3"], ["M1", "M9", "M3"])


def test_matcher_direct_unique():
    holdat = [("h1", ["M1", "M2", "M3"])]
    icit = [_rec(["M1", "UNK", "M3"])]
    m = run_matcher(holdat, icit)
    assert m["tier_a"] == [(0, 0)]
    assert m["tier_b"] == [] and m["tier_c"] == []


def test_matcher_reversed_tier_b():
    holdat = [("h1", ["M1", "M2", "M3"])]
    icit = [_rec(["M3", "M2", "M1"])]
    m = run_matcher(holdat, icit)
    assert m["tier_a"] == [] and m["tier_b"] == [(0, 0)]


def test_matcher_ambiguous_orientation_excluded():
    # Palindromic-compatible: matches in both orientations.
    holdat = [("h1", ["M1", "M2", "M1"])]
    icit = [_rec(["M1", "M2", "M1"])]
    m = run_matcher(holdat, icit)
    assert m["tier_a"] == [] and m["tier_b"] == []
    assert m["ambiguous_pairs"] == 1


def test_matcher_nonunique_excluded():
    holdat = [("h1", ["M1", "M2", "M3"]), ("h2", ["M1", "M2", "M3"])]
    icit = [_rec(["M1", "M2", "M3"])]
    m = run_matcher(holdat, icit)
    assert m["tier_a"] == []


def test_matcher_containment_tier_c():
    holdat = [("h1", ["M9", "M1", "M2", "M3", "M8"])]
    icit = [_rec(["M1", "M2", "M3"])]
    m = run_matcher(holdat, icit)
    assert m["tier_c"] == [(0, 0)]


def test_wasserstein1_known_values():
    assert wasserstein1([0.0], [1.0]) == 1.0
    assert wasserstein1([0.0, 1.0], [0.0, 1.0]) == 0.0
    assert abs(wasserstein1([0.0, 0.0], [1.0, 1.0]) - 1.0) < 1e-12
    assert abs(wasserstein1([0.5], [0.25]) - 0.25) < 1e-12


def test_bh_qvalues_monotone():
    q = bh_qvalues([0.001, 0.5, 0.04])
    assert q[0] <= q[2] <= q[1]
    assert abs(q[0] - 0.003) < 1e-9


def test_spearman_perfect_and_inverse():
    assert spearman([1, 2, 3], [10, 20, 30]) == 1.0
    assert spearman([1, 2, 3], [30, 20, 10]) == -1.0


def test_modal_bin_tie_lowest():
    assert modal_bin((0.2, 0.2, 0.2, 0.2, 0.2)) == 0
    assert modal_bin((0.1, 0.4, 0.4, 0.05, 0.05)) == 1


def test_verdict_boundaries():
    # Composition: supported / refuted / unresolved edges.
    assert verdict_composition(True, 0.75, 0.20, 0.20, 0.40) == "SUPPORTED"
    assert verdict_composition(True, 0.25, 0.38, 0.20, 0.40) == "REFUTED"
    assert verdict_composition(True, 0.50, 0.30, 0.20, 0.40) == "UNRESOLVED"
    assert verdict_composition(False, 1.0, 0.0, 0.0, 0.4) == "UNRESOLVED"
    # S1 edges.
    assert verdict_s1(21) == "SUPPORTED"
    assert verdict_s1(39) == "REFUTED"
    assert verdict_s1(30) == "UNRESOLVED"
    # Mapping edges incl. void-group rule.
    assert verdict_mapping(0.60, 0.20, True) == "SUPPORTED"
    assert verdict_mapping(0.40, 0.05, True) == "REFUTED"
    assert verdict_mapping(0.90, None, False) == "UNRESOLVED"
    assert verdict_mapping(0.30, None, False) == "REFUTED"
    # D1 edges.
    assert verdict_d1(True, 0.60) == "SUPPORTED"
    assert verdict_d1(True, 0.10) == "REFUTED"
    assert verdict_d1(False, 0.90) == "UNRESOLVED"
    # Definition edges.
    assert verdict_definition(0.12, 0.25, 0.70) == "SUPPORTED"
    assert verdict_definition(0.20, 0.10, 0.90) == "REFUTED"
    assert verdict_definition(0.10, 0.50, 0.90) == "REFUTED"
    assert verdict_definition(0.15, 0.30, 0.80) == "UNRESOLVED"


def test_recommendation_none_when_nothing_supported():
    rec = assemble_recommendation(
        {"composition": "REFUTED", "segmentation": "REFUTED",
         "mapping": "UNRESOLVED", "direction": "REFUTED",
         "definition": "UNRESOLVED"},
        {"s1": "REFUTED", "s2": "REFUTED"})
    assert rec["lines"] and rec["lines"][0].startswith("R-NONE")
    assert rec["may_not_assume"] and rec["unresolved"] == [
        "mapping", "definition"]


def test_recommendation_supported_lines():
    rec = assemble_recommendation(
        {"composition": "SUPPORTED", "segmentation": "SUPPORTED",
         "mapping": "REFUTED", "direction": "REFUTED",
         "definition": "REFUTED"},
        {"s1": "SUPPORTED", "s2": "UNRESOLVED"})
    joined = " ".join(rec["lines"])
    assert "R-SEG1" in joined and "R-COMP" in joined
    assert "R-NONE" not in joined


def test_h23_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase116Harmonization" in ATOMIC_NODES
