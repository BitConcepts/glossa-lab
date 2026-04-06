"""Linear A anti-circularity experiment suite.

Seven experiments designed to test whether the Greek-dominant result in the
real-corpus Linear A analysis is an artifact of using Linear B-derived phoneme
assignments, or reflects genuine structure in the corpus.

Scientific goal:
  Demonstrate that the Greek-adjacent signal survives:
  1. Raw tablet sequences (not Markov-generated)
  2. Reduced / ablated phoneme mappings
  3. Perturbed / noisy phoneme assignments
  4. Comparison against random / permuted mappings (null distribution)
  5. Lexical evidence removed (Kandles + bigram only)
  6. Equalized language model sizes
  7. Destroyed corpus structure (null corpus controls)

Usage:
    from glossa_lab.experiments.linear_a_circularity import run_all_experiments
    results = run_all_experiments(n_mc_trials=30, verbose=True)
"""

from __future__ import annotations

import os
import random
import sys
from collections import Counter
from typing import Any

# Path setup for running standalone — must precede glossa_lab imports.
_HERE = os.path.dirname(__file__)
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from glossa_lab.experiments.stats import bootstrap_ci, empirical_p_value, z_score  # noqa: E402
from glossa_lab.pipelines.decipher import LanguageModel  # noqa: E402
from glossa_lab.pipelines.hypothesis import Hypothesis, HypothesisEngine  # noqa: E402

# ── Lazy imports (avoid import-time costs) ────────────────────────────


def _get_lb_model():
    from glossa_lab.data.linear_b_language import get_corpus_symbols

    return LanguageModel(get_corpus_symbols())


def _get_gorila_map():
    from tests.corpora.linear_a_real_corpus import (  # noqa: I001
        _ALREADY_PHONETIC,
        GORILA_TO_PHONEME,
    )

    mapping = dict(GORILA_TO_PHONEME)
    for s in _ALREADY_PHONETIC:
        mapping[s] = s.lower()
    return mapping


def _load_raw_corpus():
    from tests.corpora.linear_a_real_corpus import load_raw_tablet_corpus

    flat, site_dict = load_raw_tablet_corpus()
    return flat, site_dict


def _load_markov_corpus(seed=42):
    from tests.corpora.linear_a_real_corpus import generate_real_linear_a_sequence

    return generate_real_linear_a_sequence(seed=seed)


def _translate(seq, mapping):
    result = []
    for s in seq:
        p = mapping.get(s, s)
        if not p.startswith("?"):
            result.append(p)
    return result


# ── Shared language models (built once per process) ───────────────────

_LANGUAGE_MODELS: dict[str, LanguageModel] | None = None


def _get_language_models(size: int | None = None) -> dict[str, LanguageModel]:
    """Build / cache language models. If size given, equalise corpus sizes."""
    global _LANGUAGE_MODELS  # noqa: PLW0603

    LUWIAN = list("atimimitatiwawatarruszidandaparananturapiariwalaasiisaparamanani" * 30)
    SEMITIC = list("abuummuahubanukalbu" * 30)
    HURRIAN = list("eniattianevretiurihifattimannikketmennakiagallammewuriurihewuri" * 30)

    lb_syms = _get_lb_model().symbols

    if size:
        # Equalise to `size` characters
        lb_syms = lb_syms[:size] if len(lb_syms) >= size else lb_syms * (size // len(lb_syms) + 1)
        lb_syms = lb_syms[:size]
        LUWIAN = (LUWIAN * (size // len(LUWIAN) + 1))[:size]
        SEMITIC = (SEMITIC * (size // len(SEMITIC) + 1))[:size]
        HURRIAN = (HURRIAN * (size // len(HURRIAN) + 1))[:size]

    return {
        "greek": LanguageModel(lb_syms),
        "hurrian": LanguageModel(HURRIAN),
        "luwian": LanguageModel(LUWIAN),
        "semitic": LanguageModel(SEMITIC),
    }


# ── Core scoring function ─────────────────────────────────────────────

SCORING_MODES = ("full", "no_vocab", "kandles_only")

_HYPOTHESES = [
    Hypothesis(id="greek", name="Mycenaean Greek", target_language="greek"),
    Hypothesis(id="hurrian", name="Hurrian", target_language="hurrian"),
    Hypothesis(id="luwian", name="Luwian/Anatolian", target_language="luwian"),
    Hypothesis(id="semitic", name="Proto-Semitic", target_language="semitic"),
]

# Hypotheses with language-appropriate Kandles bias profiles.
# Each hypothesis uses the phonological categories of its own language family
# when computing the Kandles color-fingerprint similarity score.
_HYPOTHESES_BIASED = [
    Hypothesis(
        id="greek", name="Mycenaean Greek", target_language="greek", kandles_profile="default"
    ),
    Hypothesis(id="hurrian", name="Hurrian", target_language="hurrian", kandles_profile="hurrian"),
    Hypothesis(
        id="luwian", name="Luwian/Anatolian", target_language="luwian", kandles_profile="luwian"
    ),
    Hypothesis(
        id="semitic", name="Proto-Semitic", target_language="semitic", kandles_profile="semitic"
    ),
]


def _known_vocab():
    from tests.corpora.linear_a_real_corpus import KNOWN_LINEAR_A_WORDS

    return KNOWN_LINEAR_A_WORDS


def run_one_trial(
    corpus: list[str],
    mapping: dict[str, str],
    scoring_mode: str = "full",
    models: dict[str, LanguageModel] | None = None,
    max_iter: int = 500,
    restarts: int = 2,
    use_kandles_bias: bool = False,
) -> dict[str, float]:
    """Score all four hypotheses on the given corpus+mapping.

    Args:
        corpus:            Raw sign sequence (GORILA codes or mixed).
        mapping:           Sign → phoneme assignment.
        scoring_mode:      'full', 'no_vocab', or 'kandles_only'.
        models:            Pre-built language models (built if None).
        max_iter:          Hill-climbing iterations per trial.
        restarts:          Number of random restarts.
        use_kandles_bias:  When True each hypothesis uses its own language’s
                           Kandles phonological profile (luwian→luwian profile,
                           semitic→semitic profile, etc.) instead of the default
                           Greek/English mapping for all.

    Returns:
        {hypothesis_id: total_score} for all four hypotheses.
    """
    if models is None:
        models = _get_language_models()

    # Apply mapping to get phoneme corpus
    phonemes = [mapping.get(s, s) for s in corpus]
    phonemes = [p for p in phonemes if not p.startswith("?")]

    hyps = _HYPOTHESES_BIASED if use_kandles_bias else _HYPOTHESES
    if len(phonemes) < 20:
        return {h.id: 0.0 for h in hyps}

    vocab = _known_vocab() if scoring_mode == "full" else {}

    engine = HypothesisEngine(cipher_signs=phonemes)
    results = engine.run_iteration(
        hyps,
        models,
        {"greek": vocab, "hurrian": {}, "luwian": {}, "semitic": {}},
        max_iterations=max_iter,
    )

    scores: dict[str, float] = {}
    for r in results:
        if scoring_mode == "kandles_only":
            scores[r.hypothesis_id] = r.scores.get("kandles", 0.0) * 10.0
        elif scoring_mode == "no_vocab":
            # Remove word_match contribution: total - word_matches * 10
            word_bonus = r.scores.get("word_matches", 0) * 10.0
            scores[r.hypothesis_id] = max(0.0, r.total_score - word_bonus)
        else:
            scores[r.hypothesis_id] = r.total_score

    return scores


# ── Mapping variant generators ────────────────────────────────────────


def make_ablated_mapping(
    base_mapping: dict[str, str],
    corpus: list[str],
    n_signs: int,
    seed: int = 42,
) -> dict[str, str]:
    """Return a mapping that only assigns values to the top-n most frequent signs.

    Signs outside the top-n are treated as unknown (kept as-is).
    If n_signs < total, a random subset of size n_signs is drawn.
    """
    rng = random.Random(seed)
    freq = Counter(s for s in corpus if s in base_mapping)
    # draw randomly from all mapped signs that appear in corpus
    all_mapped = [s for s in base_mapping if s in freq]
    if n_signs >= len(all_mapped):
        selected = set(all_mapped)
    else:
        selected = set(rng.sample(all_mapped, min(n_signs, len(all_mapped))))
    return {s: v for s, v in base_mapping.items() if s in selected}


def make_perturbed_mapping(
    base_mapping: dict[str, str],
    noise_fraction: float,
    seed: int = 42,
) -> dict[str, str]:
    """Return a mapping with noise_fraction of sign assignments randomly swapped.

    Swaps phoneme labels among the mapped signs without changing the inventory.
    """
    rng = random.Random(seed)
    result = dict(base_mapping)
    signs = list(result.keys())
    n_swap = max(1, int(len(signs) * noise_fraction))
    indices = rng.sample(range(len(signs)), min(n_swap, len(signs)))
    for i in range(0, len(indices) - 1, 2):
        a, b = signs[indices[i]], signs[indices[i + 1]]
        result[a], result[b] = result[b], result[a]
    return result


def make_random_mapping(
    base_mapping: dict[str, str],
    corpus: list[str],
    seed: int = 42,
    preserve_cv_structure: bool = False,
) -> dict[str, str]:
    """Return a frequency-matched random phoneme mapping.

    Args:
        preserve_cv_structure: If True, assign only CV syllables to signs that
                               had CV values, V-only to V-only, etc.
    """
    rng = random.Random(seed)
    phoneme_pool = list(base_mapping.values())
    signs = list(base_mapping.keys())

    if preserve_cv_structure:
        # Separate CV from pure-V values
        cv_values = [v for v in phoneme_pool if len(v) > 1 and not v.startswith("?")]
        v_values = [v for v in phoneme_pool if len(v) == 1 and v.isalpha()]
        cv_signs = [s for s in signs if len(base_mapping[s]) > 1]
        v_signs = [s for s in signs if len(base_mapping[s]) == 1]

        rng.shuffle(cv_values)
        rng.shuffle(v_values)

        result: dict[str, str] = {}
        for i, s in enumerate(cv_signs):
            result[s] = cv_values[i % len(cv_values)] if cv_values else base_mapping[s]
        for i, s in enumerate(v_signs):
            result[s] = v_values[i % len(v_values)] if v_values else base_mapping[s]
        return result

    rng.shuffle(phoneme_pool)
    return {s: phoneme_pool[i % len(phoneme_pool)] for i, s in enumerate(signs)}


def make_permuted_mapping(
    base_mapping: dict[str, str],
    seed: int = 42,
) -> dict[str, str]:
    """Permute the phoneme values across sign keys (same inventory, random assignment).

    This directly answers: does ANY Greek-derived phoneme set produce a Greek win,
    or only the actual correspondence mapping?
    """
    rng = random.Random(seed)
    signs = list(base_mapping.keys())
    values = list(base_mapping.values())
    rng.shuffle(values)
    return dict(zip(signs, values))


# ── Null corpus generators ────────────────────────────────────────────


def make_shuffled_corpus(corpus: list[str], seed: int = 42) -> list[str]:
    """Shuffle the sign sequence — destroys sequential structure."""
    rng = random.Random(seed)
    result = list(corpus)
    rng.shuffle(result)
    return result


def make_unigram_corpus(corpus: list[str], seed: int = 42) -> list[str]:
    """Generate corpus by sampling from unigram distribution — destroys bigrams."""
    rng = random.Random(seed)
    freq = Counter(corpus)
    total = len(corpus)
    signs = list(freq.keys())
    weights = [freq[s] / total for s in signs]
    # Cumulative weights
    cum = []
    running = 0.0
    for w in weights:
        running += w
        cum.append(running)

    result = []
    for _ in range(len(corpus)):
        r = rng.random()
        for i, c in enumerate(cum):
            if r <= c:
                result.append(signs[i])
                break
        else:
            result.append(signs[-1])
    return result


# ── Experiment 1: Raw tablet sequence replication ─────────────────────


def exp1_raw_tablet_replication(
    models: dict[str, LanguageModel] | None = None,
    use_kandles_bias: bool = False,
) -> dict[str, Any]:
    """Run hypothesis engine on actual tablet sequences partitioned by site."""
    tag = " [BIASED]" if use_kandles_bias else ""
    print(f"[Exp1] Raw tablet sequence replication{tag}...")
    flat, site_dict = _load_raw_corpus()
    mapping = _get_gorila_map()
    models = models or _get_language_models()

    results: dict[str, Any] = {}

    splits = {"ALL": flat}
    splits.update(site_dict)

    for split_name, corpus in splits.items():
        if len(corpus) < 50:
            continue
        scores = run_one_trial(corpus, mapping, "full", models, use_kandles_bias=use_kandles_bias)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_id, best_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else 0.0
        results[split_name] = {
            "n_tokens": len(corpus),
            "scores": scores,
            "winner": best_id,
            "greek_score": scores.get("greek", 0.0),
            "greek_rank": next(i + 1 for i, (k, _) in enumerate(ranked) if k == "greek"),
            "margin_vs_second": round(best_score - second_score, 3),
        }
        margin = best_score - second_score
        print(
            f"  {split_name:8} n={len(corpus):4} "
            f"greek={scores.get('greek', 0):.2f} winner={best_id} margin={margin:.2f}"
        )

    return results


# ── Experiment 2: Mapping ablation ────────────────────────────────────


def exp2_mapping_ablation(
    n_trials: int = 30,
    models: dict[str, LanguageModel] | None = None,
) -> dict[str, Any]:
    """Score under ablated mappings: top-10/20/30/40/all mapped signs."""
    print("[Exp2] Mapping ablation...")
    flat, _ = _load_raw_corpus()
    corpus = flat if len(flat) > 100 else _load_markov_corpus()
    base_mapping = _get_gorila_map()
    models = models or _get_language_models()

    all_mapped = [s for s in base_mapping if s in Counter(corpus)]
    total_mapped = len(all_mapped)
    levels = [n for n in [10, 20, 30, 40, total_mapped] if n <= total_mapped]

    results: dict[str, Any] = {}
    for n in levels:
        greek_scores, hurrian_scores = [], []
        for trial in range(n_trials):
            m = make_ablated_mapping(base_mapping, corpus, n, seed=trial)
            s = run_one_trial(corpus, m, "no_vocab", models)
            greek_scores.append(s.get("greek", 0.0))
            hurrian_scores.append(s.get("hurrian", 0.0))

        g_mean, g_lo, g_hi = bootstrap_ci(greek_scores)
        h_mean = sum(hurrian_scores) / len(hurrian_scores) if hurrian_scores else 0.0
        greek_wins = sum(1 for g, h in zip(greek_scores, hurrian_scores) if g >= h)
        results[n] = {
            "n_signs": n,
            "trials": n_trials,
            "greek_mean": round(g_mean, 3),
            "greek_ci_lo": round(g_lo, 3),
            "greek_ci_hi": round(g_hi, 3),
            "hurrian_mean": round(h_mean, 3),
            "greek_rank_1_fraction": round(greek_wins / n_trials, 3),
        }
        print(
            f"  n={n:3}  greek={g_mean:.2f} [{g_lo:.2f},{g_hi:.2f}]  "  # noqa: E501
            f"hurrian={h_mean:.2f}  greek#1={greek_wins}/{n_trials}"
        )

    return results


# ── Experiment 3: Mapping perturbation ───────────────────────────────


def exp3_mapping_perturbation(
    n_trials: int = 30,
    models: dict[str, LanguageModel] | None = None,
) -> dict[str, Any]:
    """Inject controlled noise into the mapping and measure Greek score decay."""
    print("[Exp3] Mapping perturbation...")
    flat, _ = _load_raw_corpus()
    corpus = flat if len(flat) > 100 else _load_markov_corpus()
    base_mapping = _get_gorila_map()
    models = models or _get_language_models()

    noise_levels = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]
    results: dict[str, Any] = {}

    for noise in noise_levels:
        greek_scores = []
        for trial in range(n_trials):
            if noise == 0.0:
                m = base_mapping
            else:
                m = make_perturbed_mapping(base_mapping, noise, seed=trial * 100)
            s = run_one_trial(corpus, m, "no_vocab", models)
            greek_scores.append(s.get("greek", 0.0))

        g_mean, g_lo, g_hi = bootstrap_ci(greek_scores)
        results[noise] = {
            "noise_fraction": noise,
            "trials": n_trials,
            "greek_mean": round(g_mean, 3),
            "greek_ci_lo": round(g_lo, 3),
            "greek_ci_hi": round(g_hi, 3),
        }
        print(f"  noise={noise:.0%}  greek={g_mean:.2f} [{g_lo:.2f},{g_hi:.2f}]")

    return results


# ── Experiment 4: Random mapping null distribution ────────────────────


def exp4_random_mapping_controls(
    n_trials: int = 100,
    models: dict[str, LanguageModel] | None = None,
) -> dict[str, Any]:
    """Build null distribution via random/permuted mappings."""
    print("[Exp4] Random mapping controls...")
    flat, _ = _load_raw_corpus()
    corpus = flat if len(flat) > 100 else _load_markov_corpus()
    base_mapping = _get_gorila_map()
    models = models or _get_language_models()

    # Real mapping score (single run as reference)
    real_scores = run_one_trial(corpus, base_mapping, "no_vocab", models)
    real_greek = real_scores.get("greek", 0.0)
    print(f"  Real mapping: greek={real_greek:.2f}")

    def _rand_map(seed: int) -> dict[str, str]:
        return make_random_mapping(base_mapping, corpus, seed=seed, preserve_cv_structure=False)

    def _cv_map(seed: int) -> dict[str, str]:
        return make_random_mapping(base_mapping, corpus, seed=seed, preserve_cv_structure=True)

    def _perm_map(seed: int) -> dict[str, str]:
        return make_permuted_mapping(base_mapping, seed=seed)

    null_types = {
        "frequency_matched_random": _rand_map,
        "cv_structure_preserving": _cv_map,
        "permuted_lb_correspondences": _perm_map,
    }

    results: dict[str, Any] = {"real_greek": real_greek, "nulls": {}}

    for null_name, null_fn in null_types.items():
        null_greek_scores = []
        for trial in range(n_trials):
            m = null_fn(seed=trial * 7 + 13)
            s = run_one_trial(corpus, m, "no_vocab", models)
            null_greek_scores.append(s.get("greek", 0.0))

        p_val = empirical_p_value(real_greek, null_greek_scores)
        z = z_score(real_greek, null_greek_scores)
        g_mean, g_lo, g_hi = bootstrap_ci(null_greek_scores)
        pct = sum(1 for s in null_greek_scores if s >= real_greek) / n_trials * 100

        results["nulls"][null_name] = {
            "trials": n_trials,
            "null_mean": round(g_mean, 3),
            "null_std": round(bootstrap_ci(null_greek_scores)[0], 3),
            "null_ci_lo": round(g_lo, 3),
            "null_ci_hi": round(g_hi, 3),
            "real_score": real_greek,
            "p_value": round(p_val, 4),
            "z_score": round(z, 3),
            "pct_exceeding_real": round(pct, 1),
        }
        print(f"  {null_name}: mean={g_mean:.2f}  p={p_val:.4f}  z={z:.2f}")

    return results


# ── Experiment 5: Scoring mode comparison ────────────────────────────


def exp5_scoring_mode_comparison(
    models: dict[str, LanguageModel] | None = None,
    use_kandles_bias: bool = False,
) -> dict[str, Any]:
    """Run all three scoring modes and compare rankings."""
    tag = " [BIASED]" if use_kandles_bias else ""
    print(f"[Exp5] Scoring mode comparison{tag}...")
    flat, _ = _load_raw_corpus()
    corpus = flat if len(flat) > 100 else _load_markov_corpus()
    mapping = _get_gorila_map()
    models = models or _get_language_models()

    results: dict[str, Any] = {}

    for mode in SCORING_MODES:
        scores = run_one_trial(corpus, mapping, mode, models, use_kandles_bias=use_kandles_bias)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        winner = ranked[0][0]
        greek_rank = next(i + 1 for i, (k, _) in enumerate(ranked) if k == "greek")
        results[mode] = {
            "scores": scores,
            "winner": winner,
            "greek_rank": greek_rank,
            "greek_score": scores.get("greek", 0.0),
        }
        labels = {
            "full": "Full (bigram+Kandles+vocab)",
            "no_vocab": "No vocab (bigram+Kandles)",
            "kandles_only": "Kandles only",
        }
        label = labels[mode]
        print(f"  {label}: greek={scores.get('greek', 0):.2f}  rank=#{greek_rank}  winner={winner}")

    return results


# ── Experiment 6: Language model fairness ────────────────────────────


def exp6_language_model_fairness(
    equalized_size: int = 2000,
    models: dict[str, LanguageModel] | None = None,
) -> dict[str, Any]:
    """Re-run with equalized corpus sizes for all language models."""
    print("[Exp6] Language model fairness (equalized corpus sizes)...")
    flat, _ = _load_raw_corpus()
    corpus = flat if len(flat) > 100 else _load_markov_corpus()
    mapping = _get_gorila_map()

    eq_models = _get_language_models(size=equalized_size)
    base_models = _get_language_models()

    scores_base = run_one_trial(corpus, mapping, "no_vocab", base_models)
    scores_eq = run_one_trial(corpus, mapping, "no_vocab", eq_models)

    ranked_base = sorted(scores_base.items(), key=lambda x: x[1], reverse=True)
    ranked_eq = sorted(scores_eq.items(), key=lambda x: x[1], reverse=True)

    print(f"  Baseline:  greek={scores_base.get('greek', 0):.2f}  winner={ranked_base[0][0]}")
    print(f"  Equalized: greek={scores_eq.get('greek', 0):.2f}  winner={ranked_eq[0][0]}")

    return {
        "equalized_size": equalized_size,
        "baseline": {
            "scores": scores_base,
            "winner": ranked_base[0][0],
            "greek_rank": next(i + 1 for i, (k, _) in enumerate(ranked_base) if k == "greek"),
        },
        "equalized": {
            "scores": scores_eq,
            "winner": ranked_eq[0][0],
            "greek_rank": next(i + 1 for i, (k, _) in enumerate(ranked_eq) if k == "greek"),
        },
    }


# ── Experiment 7: Null corpus controls ───────────────────────────────


def exp7_null_corpus_controls(
    n_trials: int = 30,
    models: dict[str, LanguageModel] | None = None,
) -> dict[str, Any]:
    """Test that the signal collapses when corpus structure is destroyed."""
    print("[Exp7] Null corpus controls...")
    flat, _ = _load_raw_corpus()
    corpus = flat if len(flat) > 100 else _load_markov_corpus()
    mapping = _get_gorila_map()
    models = models or _get_language_models()

    null_corpora = {
        "real": lambda seed: corpus,
        "shuffled": lambda seed: make_shuffled_corpus(corpus, seed),
        "unigram_only": lambda seed: make_unigram_corpus(corpus, seed),
    }

    results: dict[str, Any] = {}
    for null_name, corpus_fn in null_corpora.items():
        greek_scores = []
        for trial in range(n_trials):
            c = corpus_fn(seed=trial)
            s = run_one_trial(c, mapping, "no_vocab", models)
            greek_scores.append(s.get("greek", 0.0))

        g_mean, g_lo, g_hi = bootstrap_ci(greek_scores)
        results[null_name] = {
            "null_type": null_name,
            "trials": n_trials,
            "greek_mean": round(g_mean, 3),
            "greek_ci_lo": round(g_lo, 3),
            "greek_ci_hi": round(g_hi, 3),
        }
        print(f"  {null_name:20}  greek={g_mean:.2f} [{g_lo:.2f},{g_hi:.2f}]")

    return results


# ── Master runner ─────────────────────────────────────────────────────


def run_all_experiments(
    n_mc_trials: int = 30,
    verbose: bool = True,
    use_kandles_bias: bool = False,
) -> dict[str, Any]:
    """Run all 7 anti-circularity experiments and return combined results.

    Args:
        n_mc_trials:       Number of Monte Carlo trials for stochastic experiments.
        verbose:           Print progress.
        use_kandles_bias:  When True each hypothesis uses its own language’s
                           Kandles phonological profile.

    Returns:
        dict with keys exp1..exp7, each containing that experiment's results.
    """
    import contextlib
    import io

    if not verbose:
        _f = io.StringIO()
        ctx: Any = contextlib.redirect_stdout(_f)
    else:
        ctx = contextlib.nullcontext()

    # Build language models once and share
    models = _get_language_models()

    with ctx:
        print(f"\n{'=' * 60}")
        bias_label = (
            "BIASED (language-specific Kandles)"
            if use_kandles_bias
            else "UNBIASED (default Kandles)"
        )
        print(f"Linear A Anti-Circularity Experiment Suite  [{bias_label}]")
        print(f"MC trials per experiment: {n_mc_trials}")
        print(f"{'=' * 60}\n")

        r1 = exp1_raw_tablet_replication(models=models, use_kandles_bias=use_kandles_bias)
        r2 = exp2_mapping_ablation(n_trials=n_mc_trials, models=models)
        r3 = exp3_mapping_perturbation(n_trials=n_mc_trials, models=models)
        r4 = exp4_random_mapping_controls(n_trials=n_mc_trials, models=models)
        r5 = exp5_scoring_mode_comparison(models=models, use_kandles_bias=use_kandles_bias)
        r6 = exp6_language_model_fairness(models=models)
        r7 = exp7_null_corpus_controls(n_trials=n_mc_trials, models=models)

    return {
        "exp1_raw_tablet": r1,
        "exp2_mapping_ablation": r2,
        "exp3_perturbation": r3,
        "exp4_null_distribution": r4,
        "exp5_scoring_modes": r5,
        "exp6_fairness": r6,
        "exp7_null_corpus": r7,
        "n_mc_trials": n_mc_trials,
        "use_kandles_bias": use_kandles_bias,
    }


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class LinearACircularity(_EB):
    id = "linear_a_circularity"
    name = "Linear A Anti-Circularity Suite (7 experiments)"
    category = "Experiments"
    description = "7-experiment anti-circularity suite for Linear A phoneme hypothesis testing."
    estimated_time = "~10 min"
    command = "python backend/generate_report_linear_a_circularity.py"
    results_file = "reports/circularity_results.json"

    def run(self, **kwargs):
        raise NotImplementedError(
            "Linear A circularity suite requires ~10 min. Use the CLI command or Stream mode."
        )
