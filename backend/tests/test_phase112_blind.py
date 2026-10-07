"""Tests for Phase-112 (spec 010) order-carrying feature pipeline.

Design-stage tests (pre-freeze): the mechanical permutation-
sensitivity verification of spec 010 section 4 — every candidate
feature must change materially under within-text permutation on
structured toy corpora — plus hand-computed values for the new
features, determinism, and degenerate-input guards. Panel, gate,
and generator tests for the frozen admitted set live here too
(added with the pipeline commit).
"""
from __future__ import annotations

import numpy as np
import pytest

from glossa_lab.phase112_features import (
    CANDIDATE_FEATURES,
    FEATURE_NAMES,
    extract_candidates,
    extract_features,
)

# ---------------------------------------------------------------------------
# Structured toy corpora (deterministic; no RNG in construction)
# ---------------------------------------------------------------------------


def toy_a() -> list[list[int]]:
    """Positional + Markov toy: fixed start tokens, a period-4 body
    cycle with an adjacent-double motif, one fixed end token."""
    texts = []
    for i in range(120):
        length = 5 + (i % 4)
        start = 90 + (i % 2)
        body_len = length - 2
        s = i % 4
        seq = [(s + j) % 4 for j in range(body_len)]
        if body_len >= 2:
            seq[1] = seq[0]
        texts.append([start] + seq + [80])
    return texts


def toy_b() -> list[list[int]]:
    """Period-3 repetition toy: distance-3 pairs are always equal."""
    return [[(j + i) % 3 for j in range(6 + (i % 3))] for i in range(90)]


def _permute(texts: list[list[int]], seed: int = 999) -> list[list[int]]:
    rng = np.random.default_rng(np.random.SeedSequence([seed]))
    out = []
    for t in texts:
        arr = list(t)
        rng.shuffle(arr)
        out.append(arr)
    return out


# ---------------------------------------------------------------------------
# Mechanical permutation-sensitivity (spec 010 section 4)
# ---------------------------------------------------------------------------


def test_all_candidates_permutation_sensitive_on_toys():
    """Each candidate must move by > 0.002 under permutation on at
    least one structured toy. A candidate failing here is dropped
    before the spec freeze and the drop recorded in spec 010."""
    toys = [toy_a(), toy_b()]
    originals = [extract_candidates(t, draw_index=0) for t in toys]
    permuted = [extract_candidates(_permute(t), draw_index=0) for t in toys]
    for name in CANDIDATE_FEATURES:
        delta = max(abs(o[name] - p[name]) for o, p in zip(originals, permuted))
        assert delta > 0.002, f"{name} is permutation-insensitive on toys (delta={delta})"


def test_feature_names_are_candidates():
    assert FEATURE_NAMES, "admitted feature set must be non-empty"
    assert set(FEATURE_NAMES) <= set(CANDIDATE_FEATURES)
    assert len(FEATURE_NAMES) == len(set(FEATURE_NAMES))
    assert len(CANDIDATE_FEATURES) == len(set(CANDIDATE_FEATURES))


# ---------------------------------------------------------------------------
# Hand-computed values for the new features
# ---------------------------------------------------------------------------


def test_bigram_type_ratio_hand_value():
    f = extract_candidates([[0, 1, 0], [1, 0]], draw_index=0)
    # bigrams: (0,1), (1,0), (1,0) -> 2 distinct / 3 tokens
    assert f["bigram_type_ratio"] == pytest.approx(2 / 3)


def test_adj_clustering_triangle():
    f = extract_candidates([[0, 1, 2, 0]] * 40, draw_index=0)
    # adjacency graph is the triangle {0,1,2}: clustering 1.0
    assert f["adj_clustering"] == pytest.approx(1.0)


def test_fl_mi_zero_when_last_constant_and_positive_when_determined():
    const_last = extract_candidates([[5, 1, 9], [6, 2, 9], [5, 3, 9], [6, 4, 9]] * 20,
                                     draw_index=0)
    assert const_last["fl_mi"] == pytest.approx(0.0)
    determined = extract_candidates(
        [[5, 1, 6], [5, 1, 6], [7, 2, 8], [7, 2, 8]] * 20, draw_index=0)
    assert determined["fl_mi"] > 0.3


def test_cond_ent2_is_block_entropy_increment():
    draw = [[0, 1, 2, 0, 1], [2, 0, 1, 2], [1, 2, 0, 1, 2, 0]]
    f = extract_candidates(draw, draw_index=3)
    assert f["cond_ent2"] == pytest.approx(f["blockH3"] - f["blockH2"])
    assert f["ent_incr_43"] == pytest.approx(f["blockH4"] - f["blockH3"])
    assert f["cond_ent"] == pytest.approx(f["blockH2"] - (f["blockH2"] - f["cond_ent"]))


# ---------------------------------------------------------------------------
# Determinism and degenerate inputs
# ---------------------------------------------------------------------------


def test_extraction_deterministic():
    draw = [[3, 1, 4, 1, 5], [9, 2, 6], [5, 3, 5]]
    assert extract_candidates(draw, draw_index=7) == extract_candidates(draw, draw_index=7)
    assert extract_features(draw, draw_index=7) == extract_features(draw, draw_index=7)


def test_single_sign_corpus_guards():
    f = extract_candidates([[0, 0], [0]], draw_index=0)
    assert np.isfinite(list(f.values())).all()
    assert f["hend_first"] == 0.0
    assert f["fl_mi"] == 0.0


def test_extract_features_returns_exactly_feature_names():
    f = extract_features([[0, 1, 0], [1, 0, 1]], draw_index=0)
    assert list(f.keys()) == FEATURE_NAMES
