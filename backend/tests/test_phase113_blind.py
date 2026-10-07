"""Tests for Phase-113 (design stage) new candidate features.

Design-stage tests (pre-freeze): the mechanical permutation-
sensitivity verification — every new candidate must change
materially under within-text permutation on structured toy
corpora — plus hand-computed values, determinism, and
degenerate-input guards.

Note on toy choice: toy_a / toy_b are the Phase-112 toy
constructions, copied verbatim. On those two small-vocabulary
toys alone, shared_bigram_type_frac (token-weighted, per its
definition) cannot move by more than 0.0016 under any within-text
permutation (its original value is 1.0 and every permuted bigram
type still recurs across texts), so a third toy with a larger
vocabulary and cross-text bigram structure (toy_c) is included
for the cross-text family; every candidate must move on at least
one of the three toys.
"""
from __future__ import annotations

import numpy as np
import pytest

from glossa_lab.phase112_features import CANDIDATE_FEATURES as CANDIDATES112
from glossa_lab.phase112_features import FEATURE_NAMES as FEATURE_NAMES112
from glossa_lab.phase113_features import (
    LADDER_A,
    NEW_CANDIDATES,
    NEW_CANDIDATES_B,
    NEW_CANDIDATES_C,
    extract_all113,
    extract_new_candidates,
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


def toy_c() -> list[list[int]]:
    """Cross-text toy: overlapping windows over a 40-token cycle,
    so most bigram types are shared across many texts."""
    return [[(i + j) % 40 for j in range(6)] for i in range(80)]


def _permute(texts: list[list[int]], seed: int = 999) -> list[list[int]]:
    rng = np.random.default_rng(np.random.SeedSequence([seed]))
    out = []
    for t in texts:
        arr = list(t)
        rng.shuffle(arr)
        out.append(arr)
    return out


# ---------------------------------------------------------------------------
# Mechanical permutation-sensitivity
# ---------------------------------------------------------------------------


def test_all_new_candidates_permutation_sensitive_on_toys():
    """Each new candidate must move by > 0.002 under permutation
    on at least one structured toy."""
    toys = [toy_a(), toy_b(), toy_c()]
    originals = [extract_new_candidates(t, draw_index=0) for t in toys]
    permuted = [extract_new_candidates(_permute(t), draw_index=0) for t in toys]
    for name in NEW_CANDIDATES:
        delta = max(abs(o[name] - p[name]) for o, p in zip(originals, permuted))
        assert delta > 0.002, f"{name} is permutation-insensitive on toys (delta={delta})"


def test_candidate_lists_disjoint_and_complete():
    assert NEW_CANDIDATES == NEW_CANDIDATES_B + NEW_CANDIDATES_C
    assert len(NEW_CANDIDATES) == len(set(NEW_CANDIDATES))
    assert not set(NEW_CANDIDATES) & set(CANDIDATES112)


def test_ladder_a_is_phase112_feature_names():
    assert LADDER_A == FEATURE_NAMES112
    assert len(LADDER_A) == 16


# ---------------------------------------------------------------------------
# Hand-computed values
# ---------------------------------------------------------------------------


def test_dup_features_hand_values():
    f = extract_new_candidates([[0, 1, 2], [0, 1, 2], [3], [4, 5]], draw_index=0)
    # [0,1,2] occurs twice; the other two texts are unique.
    assert f["dup_text_frac"] == pytest.approx(2 / 4)
    # duplicated texts hold 6 of the 9 tokens
    assert f["dup_token_coverage"] == pytest.approx(6 / 9)


def test_dup_features_all_identical():
    f = extract_new_candidates([[1, 2], [1, 2], [1, 2]], draw_index=0)
    assert f["dup_text_frac"] == pytest.approx(1.0)
    assert f["dup_token_coverage"] == pytest.approx(1.0)


def test_mi_lag2_zero_when_lag2_token_constant():
    # Lag-2 pairs are (0, 5) and (1, 5): the lag-2 token is constant,
    # so H(py) = 0 and H(pxy) = H(px) exactly (same counts, same
    # Miller-Madow correction), giving MI = 0.
    draw = [[0, 9, 5], [1, 8, 5], [0, 7, 5], [1, 6, 5]] * 20
    f = extract_new_candidates(draw, draw_index=0)
    assert f["mi_lag2"] == pytest.approx(0.0, abs=1e-9)


def test_mi_lag2_near_zero_for_independent_lag2_pairs():
    # All four lag-2 combinations occur equally often, so the
    # plug-in MI is 0 up to the (small) Miller-Madow corrections.
    draw = [[0, 9, 0], [0, 9, 1], [1, 9, 0], [1, 9, 1]] * 50
    f = extract_new_candidates(draw, draw_index=0)
    assert abs(f["mi_lag2"]) < 0.01


def test_block_h5_constant_text_is_zero():
    # A constant text has exactly one 5-gram type, so the plug-in
    # entropy is 0 and the Miller-Madow term (m - 1) is also 0.
    f = extract_new_candidates([[7] * 10] * 5, draw_index=0)
    assert f["blockH5"] == pytest.approx(0.0)
    assert f["blockH6"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Determinism and degenerate inputs
# ---------------------------------------------------------------------------


def test_extraction_deterministic():
    draw = [[3, 1, 4, 1, 5], [9, 2, 6], [5, 3, 5]]
    assert extract_new_candidates(draw, draw_index=7) == extract_new_candidates(draw, draw_index=7)
    assert extract_all113(draw, draw_index=7) == extract_all113(draw, draw_index=7)


def test_extract_all113_merges_phase112_and_new():
    f = extract_all113([[0, 1, 0], [1, 0, 1], [0, 1, 0]], draw_index=0)
    assert set(f.keys()) == set(CANDIDATES112) | set(NEW_CANDIDATES)
    assert np.isfinite(list(f.values())).all()


def test_empty_draw_guards():
    f = extract_new_candidates([], draw_index=0)
    assert list(f.keys()) == NEW_CANDIDATES
    assert np.isfinite(list(f.values())).all()
    assert f["pp_ratio_ord3"] == pytest.approx(1.0)


def test_single_token_texts_guards():
    f = extract_new_candidates([[5], [5], [9]], draw_index=0)
    assert list(f.keys()) == NEW_CANDIDATES
    assert np.isfinite(list(f.values())).all()


def test_two_identical_texts_guards():
    f = extract_new_candidates([[0, 1], [0, 1]], draw_index=0)
    assert list(f.keys()) == NEW_CANDIDATES
    assert np.isfinite(list(f.values())).all()
    assert f["dup_text_frac"] == pytest.approx(1.0)
