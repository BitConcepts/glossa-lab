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


# ---------------------------------------------------------------------------
# Pipeline: gate branches, blinding, S5 generator (spec 010 sections 5-8)
# ---------------------------------------------------------------------------

import json  # noqa: E402
from pathlib import Path  # noqa: E402

from glossa_lab import phase112_analyst as analyst  # noqa: E402
from glossa_lab import phase112_custodian as custodian  # noqa: E402


def _fake_panel(separable: bool) -> dict:
    rng = np.random.default_rng(0)
    n_feat = len(FEATURE_NAMES)
    members = {}
    labels = analyst.FAMILIES + [analyst.NONLING]
    for i, label in enumerate(labels):
        cid = f"C{i + 1:02d}"
        centre = i * 10.0
        rows = []
        for _ in range(100):
            row = np.full(n_feat, 0.5)
            row[0] = (centre + rng.normal(0, 0.01)) if separable else 35.0
            rows.append(row.tolist())
        members[cid] = {"label": label, "features_primary": rows}
    return {"members": members,
            "known_ids": [f"C{i + 1:02d}" for i in range(len(labels))],
            "blind_ids": [], "generator_train": {},
            "feature_names": FEATURE_NAMES}


def test_gate_passes_on_separable_panel():
    gate = analyst.evaluate_gate(_fake_panel(separable=True))
    assert gate["g1_binary_balanced_accuracy"] == pytest.approx(1.0)
    assert gate["gate_passed"] is True


def test_gate_fails_on_inseparable_panel():
    gate = analyst.evaluate_gate(_fake_panel(separable=False))
    assert gate["gate_passed"] is False


def test_lda_posterior_rows_sum_to_one():
    rng = np.random.default_rng(1)
    n_feat = len(FEATURE_NAMES)
    X = rng.normal(size=(40, n_feat))
    y = np.array(["a"] * 20 + ["b"] * 20)
    model = analyst.LDA().fit(X, y, ["a", "b"])
    post = model.posterior(X)
    assert np.allclose(post.sum(axis=1), 1.0)


_FORBIDDEN = ("holdat", "indus", "linear", "tamil", "sumerian", "geez",
              "turkish", "indonesian", "khipu", "damos", "icit", "wells",
              "mahadevan", "vedic", "sanskrit")


def test_analyst_imports_no_custodian():
    src = Path(analyst.__file__).read_text(encoding="utf-8")
    assert "phase112_custodian" not in src
    assert "phase111_custodian" not in src
    assert "import custodian" not in src


def test_real_panel_blinding_invariant_if_built():
    panel_path = custodian.STATE_DIR / "panel.json"
    if not panel_path.exists():
        pytest.skip("panel not built in this environment")
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    assert panel["feature_names"] == FEATURE_NAMES
    for cid in panel["blind_ids"]:
        entry = panel["members"][cid]
        assert entry["label"] is None
        blob = json.dumps(entry).lower()
        assert all(word not in blob for word in _FORBIDDEN)


def test_feature_names_match_committed_audit():
    audit_path = Path(__file__).resolve().parents[2] / "reports" / "phase112_feature_audit.json"
    if not audit_path.exists():
        pytest.skip("audit not committed in this environment")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    assert FEATURE_NAMES == audit["admitted_features"]


def test_reuse_wiring_points_at_phase111_loaders():
    # Spec 010 inherits spec 009's frozen loaders/chunking/resampling
    # by import; guard the wiring so a silent fork cannot creep in.
    from glossa_lab import phase111_custodian as c111

    assert custodian.LOADERS is c111.LOADERS
    texts = [[1, 2, 3], [4, 5], [6, 7, 8, 9], [10]]
    rng = np.random.default_rng(np.random.SeedSequence([20261006, 99, 0]))
    draw = c111.resample_draw(texts, 11_000, rng)
    assert sum(len(t) for t in draw) == 11_000


def _toy_r1() -> list[list[str]]:
    texts = []
    for i in range(200):
        length = 3 + (i % 5)
        start = f"S{i % 3}"
        body = [f"B{(i + j) % 6}" for j in range(length - 2)]
        texts.append([start] + body + ["E"])
    return texts


def test_s5_deterministic_shaped_and_positional():
    r1 = _toy_r1()
    texts1, stats1 = custodian.s5_generator(r1)
    texts2, stats2 = custodian.s5_generator(r1)
    assert texts1 == texts2
    assert stats1 == stats2
    # generates at least 5 x N_PRIMARY tokens, lengths from the
    # frozen target distribution, vocabulary from R1 only
    assert stats1["tokens"] >= 5 * custodian.N_PRIMARY
    assert {len(t) for t in texts1} <= set(custodian.c111.TARGET_LEN_DIST.keys())
    r1_vocab = {tok for t in r1 for tok in t}
    assert {tok for t in texts1 for tok in t} <= r1_vocab
    # positional fidelity: in R1 every text ends with "E", and the
    # positional-bigram model must place "E" finally far above its
    # own unigram rate (relative-position bins smear finality across
    # lengths by design, so the share is high but not ~1)
    final_e = np.mean([t[-1] == "E" for t in texts1])
    e_rate = np.mean([tok == "E" for t in texts1 for tok in t])
    assert final_e > 0.5 and final_e > 2 * e_rate
    # unigram fidelity recorded and small on this toy
    assert stats1["unigram_tv_distance_to_R1"] < 0.25


def test_benjamini_hochberg_monotone():
    out = analyst.benjamini_hochberg({"a": 0.001, "b": 0.04, "c": 0.5}, q=0.05)
    assert out["a"]["bh_adjusted_p"] <= out["b"]["bh_adjusted_p"] <= out["c"]["bh_adjusted_p"]
    assert out["a"]["significant_at_q"] is True
    assert out["c"]["significant_at_q"] is False
