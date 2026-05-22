"""Tests for new generic atomic nodes in experiment_graph.py (TEST-AN-001..033).

Sources:
  TEST-AN-001  BuiltinCorpus loads 'indus' and returns sequences.
  TEST-AN-002  BuiltinCorpus unknown corpus name returns error.

Transforms:
  TEST-AN-003  CorpusSplitter returns correct train/test counts.
  TEST-AN-004  CorpusSplitter 75/25 split is contiguous.
  TEST-AN-005  CorpusSplitter with empty input returns error.
  TEST-AN-006  DirectionNormalizer ltr leaves sequences unchanged.
  TEST-AN-007  DirectionNormalizer rtl reverses each sequence.
  TEST-AN-008  DirectionNormalizer auto detects direction.

Analysis:
  TEST-AN-009  KLDivergence identical distributions gives KL=0.
  TEST-AN-010  KLDivergence returns kl_divergence and js_divergence keys.
  TEST-AN-011  KLDivergence missing input returns error.
  TEST-AN-012  NgramCounter n=2 counts bigrams.
  TEST-AN-013  NgramCounter n=3 counts trigrams.
  TEST-AN-014  NgramCounter returns freq_map with string keys.
  TEST-AN-015  AnchorGenerator returns top-k by frequency.
  TEST-AN-016  AnchorGenerator n_anchors=0 returns empty list.

Decipherment:
  TEST-AN-017  LMBuilder returns lm, n_signs, n_tokens, h1.
  TEST-AN-018  LMBuilder empty sequences returns error.
  TEST-AN-019  BuiltinLM hebrew loads without error.
  TEST-AN-020  BuiltinLM geez loads without error.
  TEST-AN-021  BuiltinLM unknown language returns error.
  TEST-AN-022  SADecipher missing lm returns error.
  TEST-AN-023  SADecipher missing sequences returns error.
  TEST-AN-024  SADecipher returns proposed_mapping, all_mappings, n_seeds.
  TEST-AN-025  SADecipher runs specified number of seeds.
  TEST-AN-026  ConsistencyScorer aggregates all_mappings correctly.
  TEST-AN-027  ConsistencyScorer with empty returns error.
  TEST-AN-028  ConsistencyScorer single mapping gives consistency=1.0.
  TEST-AN-029  BenchmarkScorer with no answer key returns accuracy=0.
  TEST-AN-030  BenchmarkScorer with correct key returns accuracy=1.0.
  TEST-AN-031  BenchmarkScorer missing mapping returns error.
"""
from __future__ import annotations

from glossa_lab.experiment_graph import ATOMIC_NODES


def _run(node_id: str, inputs: dict, params: dict) -> dict:
    """Helper: run an atomic node and return its result."""
    assert node_id in ATOMIC_NODES, f"Node '{node_id}' not in ATOMIC_NODES"
    return ATOMIC_NODES[node_id].fn(inputs, params)


# ── Sources ───────────────────────────────────────────────────────────────────

def test_builtin_corpus_indus():
    """TEST-AN-001: BuiltinCorpus loads 'indus'."""
    r = _run("BuiltinCorpus", {}, {"corpus": "indus"})
    assert "sequences" in r
    assert r["total_tokens"] > 0
    assert r["distinct_symbols"] > 0


def test_builtin_corpus_unknown():
    """TEST-AN-002: BuiltinCorpus unknown name returns error."""
    r = _run("BuiltinCorpus", {}, {"corpus": "nonexistent_xyz"})
    assert "error" in r


# ── CorpusSplitter ────────────────────────────────────────────────────────────

_SEQS = [["a", "b"], ["c", "d"], ["e", "f"], ["g", "h"], ["i", "j"],
         ["k", "l"], ["m", "n"], ["o", "p"]]


def test_corpus_splitter_counts():
    """TEST-AN-003: 75/25 split gives correct sequence counts."""
    r = _run("CorpusSplitter", {"sequences": _SEQS}, {"train_ratio": 0.75})
    assert r["train_n_sequences"] == 6
    assert r["test_n_sequences"] == 2
    assert r["train_n_sequences"] + r["test_n_sequences"] == len(_SEQS)


def test_corpus_splitter_contiguous():
    """TEST-AN-004: Split is contiguous — first 75% in train, rest in test."""
    r = _run("CorpusSplitter", {"sequences": _SEQS}, {"train_ratio": 0.75})
    assert r["train_sequences"] == _SEQS[:6]
    assert r["test_sequences"] == _SEQS[6:]


def test_corpus_splitter_empty():
    """TEST-AN-005: Empty input returns error."""
    r = _run("CorpusSplitter", {"sequences": []}, {})
    assert "error" in r


# ── DirectionNormalizer ───────────────────────────────────────────────────────

_WORDS = [["A", "B", "C"], ["D", "E"]]


def test_direction_normalizer_ltr():
    """TEST-AN-006: LTR leaves sequences unchanged."""
    r = _run("DirectionNormalizer", {"sequences": _WORDS}, {"direction": "ltr"})
    assert r["sequences"] == _WORDS
    assert r["applied_direction"] == "ltr"


def test_direction_normalizer_rtl():
    """TEST-AN-007: RTL reverses each sequence."""
    r = _run("DirectionNormalizer", {"sequences": _WORDS}, {"direction": "rtl"})
    assert r["sequences"][0] == ["C", "B", "A"]
    assert r["sequences"][1] == ["E", "D"]
    assert r["applied_direction"] == "rtl"


def test_direction_normalizer_auto():
    """TEST-AN-008: Auto-detect runs without error and returns a direction."""
    r = _run("DirectionNormalizer", {"sequences": _WORDS}, {"direction": "auto"})
    assert r["applied_direction"] in ("ltr", "rtl", "unknown")
    assert "sequences" in r


# ── KLDivergence ─────────────────────────────────────────────────────────────

def test_kl_divergence_identical():
    """TEST-AN-009: KL divergence of identical distributions is 0."""
    fm = {"a": 10, "b": 5, "c": 3}
    r = _run("KLDivergence", {"freq_map": fm, "q": fm}, {})
    assert abs(r["kl_divergence"]) < 1e-9
    assert abs(r["js_divergence"]) < 1e-9


def test_kl_divergence_keys():
    """TEST-AN-010: Returns kl_divergence, js_divergence, n_symbols."""
    r = _run("KLDivergence", {"freq_map": {"a": 5, "b": 3}, "q": {"a": 4, "b": 4}}, {})
    assert "kl_divergence" in r
    assert "js_divergence" in r
    assert "n_symbols" in r


def test_kl_divergence_missing_inputs():
    """TEST-AN-011: Missing one input returns error."""
    r = _run("KLDivergence", {"freq_map": {"a": 5}}, {})
    assert "error" in r


# ── NgramCounter ─────────────────────────────────────────────────────────────

_SEQS_NGRAM = [["a", "b", "c", "a"], ["b", "c", "b"]]


def test_ngram_counter_bigrams():
    """TEST-AN-012: Bigram (n=2) counting works."""
    r = _run("NgramCounter", {"sequences": _SEQS_NGRAM}, {"n": 2})
    assert r["n"] == 2
    assert r["n_ngrams"] > 0
    assert isinstance(r["freq_map"], dict)


def test_ngram_counter_trigrams():
    """TEST-AN-013: Trigram (n=3) counting works."""
    r = _run("NgramCounter", {"sequences": _SEQS_NGRAM}, {"n": 3})
    assert r["n"] == 3
    assert r["n_ngrams"] > 0


def test_ngram_counter_string_keys():
    """TEST-AN-014: freq_map keys are space-joined strings."""
    r = _run("NgramCounter", {"sequences": _SEQS_NGRAM}, {"n": 2})
    for key in r["freq_map"]:
        assert isinstance(key, str)
        assert " " in key  # space-joined


# ── AnchorGenerator ──────────────────────────────────────────────────────────

def test_anchor_generator_top_k():
    """TEST-AN-015: Returns top-k most frequent signs."""
    fm = {"a": 100, "b": 50, "c": 10, "d": 5}
    r = _run("AnchorGenerator", {"freq_map": fm}, {"n_anchors": 2})
    assert r["n_anchors"] == 2
    assert r["anchor_signs"] == ["a", "b"]


def test_anchor_generator_zero():
    """TEST-AN-016: n_anchors=0 returns empty list."""
    r = _run("AnchorGenerator", {"freq_map": {"a": 5}}, {"n_anchors": 0})
    assert r["anchor_signs"] == []
    assert r["n_anchors"] == 0


# ── LMBuilder ─────────────────────────────────────────────────────────────────

_CIPHER_SEQS = [["s1", "s2", "s3"], ["s2", "s3"], ["s1", "s3", "s2"]]


def test_lm_builder_basic():
    """TEST-AN-017: LMBuilder returns lm object and stats."""
    r = _run("LMBuilder", {"sequences": _CIPHER_SEQS}, {})
    assert "lm" in r
    assert r["n_signs"] == 3     # s1, s2, s3
    assert r["n_tokens"] == 8    # total tokens
    assert r["h1"] > 0           # non-zero entropy


def test_lm_builder_empty():
    """TEST-AN-018: LMBuilder with empty sequences returns error."""
    r = _run("LMBuilder", {"sequences": []}, {})
    assert "error" in r


# ── BuiltinLM ─────────────────────────────────────────────────────────────────

def test_builtin_lm_hebrew():
    """TEST-AN-019: BuiltinLM 'hebrew' loads without error."""
    r = _run("BuiltinLM", {}, {"language": "hebrew"})
    assert "lm" in r
    assert r["n_signs"] >= 22   # at least 22 Hebrew consonants
    assert r["n_tokens"] > 1000


def test_builtin_lm_geez():
    """TEST-AN-020: BuiltinLM 'geez' loads without error."""
    r = _run("BuiltinLM", {}, {"language": "geez"})
    assert "lm" in r
    assert r["n_signs"] >= 100  # Geez has 200+ syllabic signs
    assert r["n_tokens"] > 10000


def test_builtin_lm_unknown():
    """TEST-AN-021: Unknown language returns error."""
    r = _run("BuiltinLM", {}, {"language": "klingon"})
    assert "error" in r


# ── SADecipher ────────────────────────────────────────────────────────────────

def _make_small_lm():
    """Build a tiny Hebrew-like LM for fast tests."""
    from glossa_lab.pipelines.decipher import LanguageModel
    syms  = list("abcdeabcdeabcde" * 20)
    inscs = [list(w) for w in ["abc", "bcd", "cde", "dea", "eab"] * 10]
    return LanguageModel(syms, inscriptions=inscs)


def test_sa_decipher_missing_lm():
    """TEST-AN-022: SADecipher without lm returns error."""
    r = _run("SADecipher",
             {"sequences": _CIPHER_SEQS, "lm": None},
             {"n_seeds": 1, "max_iterations": 100, "restarts": 1})
    assert "error" in r


def test_sa_decipher_missing_sequences():
    """TEST-AN-023: SADecipher without sequences returns error."""
    lm = _make_small_lm()
    r = _run("SADecipher", {"lm": lm}, {"n_seeds": 1, "max_iterations": 100})
    assert "error" in r


def test_sa_decipher_returns_mapping():
    """TEST-AN-024: SADecipher returns proposed_mapping with correct keys."""
    lm = _make_small_lm()
    r = _run("SADecipher",
             {"sequences": _CIPHER_SEQS, "lm": lm},
             {"n_seeds": 2, "max_iterations": 300, "restarts": 2,
              "surjective": True, "ocp_weight": 0.0})
    assert "proposed_mapping" in r
    assert isinstance(r["proposed_mapping"], dict)
    assert "all_mappings" in r
    assert r["n_signs"] > 0


def test_sa_decipher_seed_count():
    """TEST-AN-025: SADecipher runs the specified number of seeds."""
    lm = _make_small_lm()
    r = _run("SADecipher",
             {"sequences": _CIPHER_SEQS, "lm": lm},
             {"n_seeds": 3, "max_iterations": 200, "restarts": 1,
              "ocp_weight": 0.0})
    assert r["n_seeds"] == 3
    assert len(r["all_mappings"]) == 3


# ── ConsistencyScorer ────────────────────────────────────────────────────────

def test_consistency_scorer_aggregates():
    """TEST-AN-026: ConsistencyScorer correctly aggregates multiple mappings."""
    maps = [{"s1": "a", "s2": "b"}, {"s1": "a", "s2": "c"}, {"s1": "a", "s2": "b"}]
    r = _run("ConsistencyScorer", {"all_mappings": maps}, {})
    assert r["n_signs"] == 2
    assert r["consistency_per_sign"]["s1"]["consistency"] == 1.0   # all agree
    assert r["consistency_per_sign"]["s2"]["consistency"] < 1.0    # split vote


def test_consistency_scorer_empty():
    """TEST-AN-027: ConsistencyScorer with no input returns error."""
    r = _run("ConsistencyScorer", {}, {})
    assert "error" in r


def test_consistency_scorer_single_mapping():
    """TEST-AN-028: Single mapping gives consistency=1.0 for all signs."""
    r = _run("ConsistencyScorer", {"proposed_mapping": {"s1": "a"}}, {})
    assert r["mean_consistency"] == 1.0


# ── BenchmarkScorer ───────────────────────────────────────────────────────────

def test_benchmark_scorer_no_key():
    """TEST-AN-029: BenchmarkScorer with no answer key reports accuracy=0."""
    r = _run("BenchmarkScorer", {"proposed_mapping": {"s1": "a"}}, {})
    assert r["accuracy"] == 0.0


def test_benchmark_scorer_perfect():
    """TEST-AN-030: BenchmarkScorer with matching key returns accuracy=1.0."""
    mapping    = {"s1": "a", "s2": "b"}
    answer_key = {"s1": "a", "s2": "b"}
    r = _run("BenchmarkScorer",
             {"proposed_mapping": mapping, "answer_key": answer_key}, {})
    assert r["accuracy"] == 1.0
    assert r["correct"] == 2


def test_benchmark_scorer_missing_mapping():
    """TEST-AN-031: BenchmarkScorer with no mapping returns error."""
    r = _run("BenchmarkScorer", {}, {})
    assert "error" in r
