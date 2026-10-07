"""Tests for Phase-111 (spec 009) blind language-affiliation pipeline.

Covers: feature extraction against hand-computed toy values, the
blinding invariant for analyst-facing artifacts, resampling
exactness, gate logic pass/fail branches, generator determinism,
and the frozen syllabifiers.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from glossa_lab import phase111_analyst as analyst
from glossa_lab import phase111_custodian as custodian
from glossa_lab.phase111_features import FEATURE_NAMES, extract_features

# ---------------------------------------------------------------------------
# Feature extraction on toy corpora (hand-computed expectations)
# ---------------------------------------------------------------------------

TOY_DRAW = [[0, 1, 0], [1, 0]]  # counts: 0->3, 1->2; N=5, K=2


def test_feature_names_frozen_count():
    assert len(FEATURE_NAMES) == 28


def test_toy_positional_and_length_features():
    f = extract_features(TOY_DRAW, draw_index=0)
    assert f["len_mean"] == pytest.approx(2.5)
    assert f["len_sd"] == pytest.approx(0.5)
    assert f["singleton_share"] == 0.0
    assert f["vocab_K"] == 2.0
    assert f["ttr"] == pytest.approx(2 / 5)
    assert f["top10_share"] == pytest.approx(1.0)
    # firsts {0:1, 1:1}: 80% of 2 texts = 1.6 -> both signs needed
    assert f["init80_frac"] == pytest.approx(1.0)
    # lasts {0:2}: one sign covers 80%
    assert f["term80_frac"] == pytest.approx(0.5)
    assert f["term_init_ratio"] == pytest.approx(0.5)
    assert f["cover80_frac"] == pytest.approx(1.0)
    assert f["hapax_prop"] == 0.0


def test_toy_repetition_feature():
    f = extract_features(TOY_DRAW, draw_index=0)
    # no adjacent equal pairs; exp = 0.6^2 + 0.4^2 = 0.52
    assert f["rep_adj_1"] == pytest.approx((0.0 - 0.52) / (1 - 0.52))


def test_toy_block_entropy_h1():
    f = extract_features(TOY_DRAW, draw_index=0)
    p = np.array([0.6, 0.4])
    h_plugin = -float(np.sum(p * np.log2(p)))
    mm = h_plugin + (2 - 1) / (2 * 5 * np.log(2))
    assert f["blockH1"] == pytest.approx(mm)


def test_feature_extraction_deterministic():
    draw = [[3, 1, 4, 1, 5], [9, 2, 6], [5, 3, 5]]
    a = extract_features(draw, draw_index=7)
    b = extract_features(draw, draw_index=7)
    assert a == b


def test_single_sign_corpus_guards():
    f = extract_features([[0, 0], [0]], draw_index=0)
    assert f["vocab_K"] == 1.0
    assert f["hend_first"] == 0.0
    assert np.isfinite(list(f.values())).all()


# ---------------------------------------------------------------------------
# Syllabifiers (spec section 3)
# ---------------------------------------------------------------------------


def test_syllabify_sanskrit():
    assert custodian.syllabify_sanskrit("agnim") == ["ag", "nim"]
    assert custodian.syllabify_sanskrit("īḍe") == ["ī", "ḍe"]
    # no vowel -> passthrough
    assert custodian.syllabify_sanskrit("kṣ") == ["kṣ"]


def test_syllabify_latin():
    vowels = set("aeıioöuü")
    assert custodian.syllabify_latin("kitap", vowels, set()) == ["ki", "tap"]
    assert custodian.syllabify_latin("sair", set("aeiou"), {"ai"}) == ["sair"]


# ---------------------------------------------------------------------------
# Resampling exactness (spec section 2)
# ---------------------------------------------------------------------------


def test_resample_draw_exact_token_count():
    texts = [[1, 2, 3], [4, 5], [6, 7, 8, 9], [10]]
    rng = np.random.default_rng(np.random.SeedSequence([20261006, 99, 0]))
    for n in (11_000, 5_000, 37):
        draw = custodian.resample_draw(texts, n, rng)
        assert sum(len(t) for t in draw) == n


def test_chunk_stream_lengths_and_conservation():
    tokens = [str(i % 50) for i in range(100_003)]
    chunks = custodian.chunk_stream(tokens, corpus_index=12345)
    allowed = set(custodian.TARGET_LEN_DIST.keys())
    assert all(len(c) in allowed for c in chunks)
    total = sum(len(c) for c in chunks)
    assert 100_003 - total < max(allowed)  # only the dropped tail is lost
    # empirical length distribution roughly matches the target
    from collections import Counter

    dist = Counter(len(c) for c in chunks)
    for length, count in custodian.TARGET_LEN_DIST.items():
        expected = count / sum(custodian.TARGET_LEN_DIST.values())
        observed = dist[length] / len(chunks)
        assert observed == pytest.approx(expected, abs=0.02)


def test_remap_is_permutation_of_ints():
    texts = [["b", "a", "b"], ["c", "a"]]
    out = custodian._remap(texts, corpus_index=5)
    flat = [t for s in out for t in s]
    assert all(isinstance(t, int) for t in flat)
    assert sorted(set(flat)) == [0, 1, 2]
    # same string -> same int
    assert out[0][0] == out[0][2]


# ---------------------------------------------------------------------------
# Generators (spec section 5)
# ---------------------------------------------------------------------------


def test_generators_deterministic_and_shaped():
    r1 = [[1, 2, 3, 2], [2, 1], [3, 3, 1, 2, 2], [1, 1, 2]]
    r1 = [[str(x) for x in t] for t in r1]
    g1 = custodian._generators(r1)
    g2 = custodian._generators(r1)
    assert g1 == g2
    # S1 is a within-text permutation of R1
    for orig, perm in zip(r1, g1["S1_permutation"]):
        assert sorted(orig) == sorted(perm)
    # S2/S3/S4 generate at least 5x N_PRIMARY tokens
    for code in ("S2_iid_zipf", "S3_heraldic_gen", "S4_admin_gen"):
        assert sum(len(t) for t in g1[code]) >= 5 * custodian.N_PRIMARY
    # S4 uses only the top-60 inventory (here: the full toy vocab)
    assert {t for s in g1["S4_admin_gen"] for t in s} <= {"1", "2", "3"}


# ---------------------------------------------------------------------------
# Gate logic branches (spec section 7)
# ---------------------------------------------------------------------------


def _fake_panel(separable: bool) -> dict:
    rng = np.random.default_rng(0)
    members = {}
    labels = analyst.FAMILIES + [analyst.NONLING]
    for i, label in enumerate(labels):
        cid = f"C{i + 1:02d}"
        centre = i * 10.0
        rows = []
        for _ in range(100):
            row = np.full(28, 0.5)
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
    X = rng.normal(size=(40, 28))
    y = np.array(["a"] * 20 + ["b"] * 20)
    model = analyst.LDA().fit(X, y, ["a", "b"])
    post = model.posterior(X)
    assert np.allclose(post.sum(axis=1), 1.0)


# ---------------------------------------------------------------------------
# Blinding invariant: analyst-facing artifacts carry no identities
# ---------------------------------------------------------------------------

_FORBIDDEN = ("holdat", "indus", "linear", "tamil", "sumerian", "geez",
              "turkish", "indonesian", "khipu", "damos", "icit", "wells",
              "mahadevan", "vedic", "sanskrit")


def test_panel_schema_blind_entries_have_no_identity():
    panel = _fake_panel(separable=True)
    panel["members"]["C99"] = {"label": None,
                               "features_primary": [[0.1] * 28 for _ in range(100)]}
    panel["blind_ids"] = ["C99"]
    blind_blob = json.dumps(panel["members"]["C99"]).lower()
    assert all(word not in blind_blob for word in _FORBIDDEN)
    assert panel["members"]["C99"]["label"] is None


def test_real_panel_blinding_invariant_if_built():
    panel_path = custodian.STATE_DIR / "panel.json"
    if not panel_path.exists():
        pytest.skip("panel not built in this environment")
    panel = json.loads(panel_path.read_text(encoding="utf-8"))
    for cid in panel["blind_ids"]:
        entry = panel["members"][cid]
        assert entry["label"] is None
        blob = json.dumps(entry).lower()
        assert all(word not in blob for word in _FORBIDDEN)
    # analyst module must not import the custodian
    src = Path(analyst.__file__).read_text(encoding="utf-8")
    assert "phase111_custodian" not in src
    assert "import custodian" not in src


def test_benjamini_hochberg_monotone():
    out = analyst.benjamini_hochberg({"a": 0.001, "b": 0.04, "c": 0.5}, q=0.05)
    assert out["a"]["bh_adjusted_p"] <= out["b"]["bh_adjusted_p"] <= out["c"]["bh_adjusted_p"]
    assert out["a"]["significant_at_q"] is True
    assert out["c"]["significant_at_q"] is False
