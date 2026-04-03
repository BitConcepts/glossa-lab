"""Kandles biased experiment runner.

Runs the Linear A anti-circularity suite twice — once with the default
Greek/English Kandles phoneme→colour mapping, and once with each hypothesis
using its own language-specific Kandles profile.

Scientific rationale:
  The default Kandles system uses Greek phonological categories for ALL
  hypotheses. This systematically advantages Greek and disadvantages
  languages with different phonological structures (laryngeals in Luwian,
  pharyngeals in Semitic, retroflexes in Dravidian).  By comparing scores
  under biased and unbiased conditions we can measure the size of this
  artefact and test whether Luwian's Kandles advantage persists even when
  Greek is evaluated with Greek categories.

Acceleration:
  - Tier 1 (always): multi-process MC trials via ProcessPoolExecutor
  - Tier 2 (numpy):  vectorised bigram scoring, batch cosine similarity
  - Tier 3 (GPU):    CUDA-accelerated batch ops via torch or cupy

Usage:
    # From repo root:
    python -m glossa_lab.experiments.run_kandles_biased_experiments
    # or
    python backend/glossa_lab/experiments/run_kandles_biased_experiments.py

    # Quiet (no progress output):
    python -m glossa_lab.experiments.run_kandles_biased_experiments --quiet

    # More MC trials:
    python -m glossa_lab.experiments.run_kandles_biased_experiments --trials 100

Output:
    reports/kandles_biased_results.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any

# ── Path setup (allows running as script without `python -m`) ─────────
_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Top-level picklable trial functions (required for ProcessPoolExecutor) ──
# These must be defined at module level so pickle can serialise them.

def _ablation_trial(
    seed: int,
    corpus: list[str],
    base_mapping: dict[str, str],
    n_signs: int,
    models: dict,
    use_kandles_bias: bool,
) -> dict[str, float]:
    """Single MC trial for Exp2 (mapping ablation)."""
    from glossa_lab.experiments.linear_a_circularity import (
        make_ablated_mapping,
        run_one_trial,
    )
    m = make_ablated_mapping(base_mapping, corpus, n_signs, seed=seed)
    return run_one_trial(corpus, m, "no_vocab", models,
                         use_kandles_bias=use_kandles_bias)


def _perturbation_trial(
    seed: int,
    corpus: list[str],
    base_mapping: dict[str, str],
    noise: float,
    models: dict,
    use_kandles_bias: bool,
) -> dict[str, float]:
    """Single MC trial for Exp3 (mapping perturbation)."""
    from glossa_lab.experiments.linear_a_circularity import (
        make_perturbed_mapping,
        run_one_trial,
    )
    if noise == 0.0:
        return run_one_trial(corpus, base_mapping, "no_vocab", models,
                             use_kandles_bias=use_kandles_bias)
    m = make_perturbed_mapping(base_mapping, noise, seed=seed * 100)
    return run_one_trial(corpus, m, "no_vocab", models,
                         use_kandles_bias=use_kandles_bias)


def _null_mapping_trial(
    seed: int,
    corpus: list[str],
    base_mapping: dict[str, str],
    null_type: str,
    models: dict,
    use_kandles_bias: bool,
) -> dict[str, float]:
    """Single MC trial for Exp4 (null distribution)."""
    from glossa_lab.experiments.linear_a_circularity import (
        make_permuted_mapping,
        make_random_mapping,
        run_one_trial,
    )
    if null_type == "frequency_matched_random":
        m = make_random_mapping(base_mapping, corpus,
                                seed=seed * 7 + 13, preserve_cv_structure=False)
    elif null_type == "cv_structure_preserving":
        m = make_random_mapping(base_mapping, corpus,
                                seed=seed * 7 + 13, preserve_cv_structure=True)
    else:  # permuted_lb_correspondences
        m = make_permuted_mapping(base_mapping, seed=seed * 7 + 13)
    return run_one_trial(corpus, m, "no_vocab", models,
                         use_kandles_bias=use_kandles_bias)


def _null_corpus_trial(
    seed: int,
    corpus: list[str],
    base_mapping: dict[str, str],
    null_type: str,
    models: dict,
    use_kandles_bias: bool,
) -> dict[str, float]:
    """Single MC trial for Exp7 (null corpus controls)."""
    from glossa_lab.experiments.linear_a_circularity import (
        make_shuffled_corpus,
        make_unigram_corpus,
        run_one_trial,
    )
    if null_type == "real":
        c = corpus
    elif null_type == "shuffled":
        c = make_shuffled_corpus(corpus, seed)
    else:  # unigram_only
        c = make_unigram_corpus(corpus, seed)
    return run_one_trial(c, base_mapping, "no_vocab", models,
                         use_kandles_bias=use_kandles_bias)


# ── Parallel MC wrappers ───────────────────────────────────────────────

def _run_ablation_parallel(
    corpus: list[str],
    base_mapping: dict[str, str],
    n_signs: int,
    models: dict,
    n_trials: int,
    use_kandles_bias: bool,
    n_workers: int | None = None,
) -> list[dict[str, float]]:
    from glossa_lab.accelerate import parallel_mc_trials
    return parallel_mc_trials(
        _ablation_trial,
        list(range(n_trials)),
        corpus, base_mapping, n_signs, models, use_kandles_bias,
        n_workers=n_workers,
    )


def _run_perturbation_parallel(
    corpus: list[str],
    base_mapping: dict[str, str],
    noise: float,
    models: dict,
    n_trials: int,
    use_kandles_bias: bool,
    n_workers: int | None = None,
) -> list[dict[str, float]]:
    from glossa_lab.accelerate import parallel_mc_trials
    return parallel_mc_trials(
        _perturbation_trial,
        list(range(n_trials)),
        corpus, base_mapping, noise, models, use_kandles_bias,
        n_workers=n_workers,
    )


def _run_null_mapping_parallel(
    corpus: list[str],
    base_mapping: dict[str, str],
    null_type: str,
    models: dict,
    n_trials: int,
    use_kandles_bias: bool,
    n_workers: int | None = None,
) -> list[dict[str, float]]:
    from glossa_lab.accelerate import parallel_mc_trials
    return parallel_mc_trials(
        _null_mapping_trial,
        list(range(n_trials)),
        corpus, base_mapping, null_type, models, use_kandles_bias,
        n_workers=n_workers,
    )


def _run_null_corpus_parallel(
    corpus: list[str],
    base_mapping: dict[str, str],
    null_type: str,
    models: dict,
    n_trials: int,
    use_kandles_bias: bool,
    n_workers: int | None = None,
) -> list[dict[str, float]]:
    from glossa_lab.accelerate import parallel_mc_trials
    return parallel_mc_trials(
        _null_corpus_trial,
        list(range(n_trials)),
        corpus, base_mapping, null_type, models, use_kandles_bias,
        n_workers=n_workers,
    )


# ── Shared stat helpers ────────────────────────────────────────────────

def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0

def _ci(vals: list[float]) -> tuple[float, float, float]:
    """Bootstrap-style 95% CI (uses stats module if available)."""
    try:
        from glossa_lab.experiments.stats import bootstrap_ci
        return bootstrap_ci(vals)
    except Exception:
        m = _mean(vals)
        return m, m, m


def _summarise_scores(
    trial_results: list[dict[str, float] | None],
    hyp_id: str,
    n_trials: int,
) -> dict[str, Any]:
    """Extract per-hypothesis stats from a list of trial result dicts."""
    vals = [r[hyp_id] for r in trial_results if r is not None and hyp_id in r]
    if not vals:
        return {"mean": 0.0, "ci_lo": 0.0, "ci_hi": 0.0, "n": 0}
    m, lo, hi = _ci(vals)
    return {"mean": round(m, 3), "ci_lo": round(lo, 3),
            "ci_hi": round(hi, 3), "n": len(vals)}


# ── Full parallel experiment suite ────────────────────────────────────

def run_parallel_experiments(
    n_mc_trials: int = 30,
    use_kandles_bias: bool = False,
    n_workers: int | None = None,
    verbose: bool = True,
) -> dict[str, Any]:
    """Run all 7 experiments using parallel MC with accelerated scoring.

    Equivalent to linear_a_circularity.run_all_experiments() but:
      - MC loops run in parallel (ProcessPoolExecutor)
      - FastScorer (numpy bigram matrix) used where available
      - Kandles cosine similarity computed in batch

    Args:
        n_mc_trials:      MC trials per stochastic experiment.
        use_kandles_bias: Use language-specific Kandles profiles.
        n_workers:        Worker processes (default: cpu_count-1).
        verbose:          Print progress.
    """
    from glossa_lab.experiments.linear_a_circularity import (  # noqa: I001
        _get_gorila_map,
        _get_language_models,
        _known_vocab,
        _load_markov_corpus,
        _load_raw_corpus,
        run_one_trial,
        SCORING_MODES,
    )
    from glossa_lab.experiments.stats import bootstrap_ci, empirical_p_value, z_score

    bias_label = "BIASED" if use_kandles_bias else "UNBIASED"

    def _print(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _print(f"\n{'='*65}")
    _print(f"  Linear A Anti-Circularity Suite  [{bias_label}]")
    _print(f"  MC trials: {n_mc_trials}  |  Workers: {n_workers or 'auto'}")
    _print(f"{'='*65}\n")

    flat, site_dict = _load_raw_corpus()
    corpus = flat if len(flat) > 100 else _load_markov_corpus()
    base_mapping = _get_gorila_map()
    models = _get_language_models()
    _known_vocab()  # warm up cache

    results: dict[str, Any] = {"use_kandles_bias": use_kandles_bias}

    # ── Exp 1: Raw tablet replication ──────────────────────────────────
    _print("[Exp1] Raw tablet sequence replication...")
    r1: dict[str, Any] = {}
    splits = {"ALL": flat}
    splits.update(site_dict)
    for split_name, split_corpus in splits.items():
        if len(split_corpus) < 50:
            continue
        scores = run_one_trial(split_corpus, base_mapping, "full", models,
                               use_kandles_bias=use_kandles_bias)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_id, best_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else 0.0
        r1[split_name] = {
            "n_tokens": len(split_corpus),
            "scores": scores,
            "winner": best_id,
            "greek_score": scores.get("greek", 0.0),
            "greek_rank": next(i + 1 for i, (k, _) in enumerate(ranked) if k == "greek"),
            "margin_vs_second": round(best_score - second_score, 3),
        }
        _print(f"  {split_name:8} n={len(split_corpus):4}  "
               f"greek={scores.get('greek', 0):.2f}  "
               f"winner={best_id}  margin={best_score - second_score:.2f}")
    results["exp1_raw_tablet"] = r1

    # ── Exp 2: Mapping ablation (parallel) ─────────────────────────────
    _print("[Exp2] Mapping ablation (parallel)...")
    from collections import Counter as _Counter
    all_mapped = [s for s in base_mapping if s in _Counter(corpus)]
    total_mapped = len(all_mapped)
    ablation_levels = [n for n in [10, 20, 30, 40, total_mapped] if n <= total_mapped]
    r2: dict[str, Any] = {}
    for n_signs in ablation_levels:
        trials = _run_ablation_parallel(
            corpus, base_mapping, n_signs, models,
            n_mc_trials, use_kandles_bias, n_workers,
        )
        g_stats = _summarise_scores(trials, "greek", n_mc_trials)
        h_stats = _summarise_scores(trials, "hurrian", n_mc_trials)
        lw_stats = _summarise_scores(trials, "luwian", n_mc_trials)
        greek_wins = sum(
            1 for t in trials
            if t and t.get("greek", 0) >= max(
                t.get("hurrian", 0), t.get("luwian", 0), t.get("semitic", 0)
            )
        )
        r2[str(n_signs)] = {
            "n_signs": n_signs,
            "trials": n_mc_trials,
            "greek": g_stats,
            "hurrian": h_stats,
            "luwian": lw_stats,
            "greek_rank_1_fraction": round(greek_wins / n_mc_trials, 3),
        }
        _print(f"  n={n_signs:3}  greek={g_stats['mean']:.2f}  "
               f"luwian={lw_stats['mean']:.2f}  greek#1={greek_wins}/{n_mc_trials}")
    results["exp2_mapping_ablation"] = r2

    # ── Exp 3: Mapping perturbation (parallel) ─────────────────────────
    _print("[Exp3] Mapping perturbation (parallel)...")
    noise_levels = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]
    r3: dict[str, Any] = {}
    for noise in noise_levels:
        trials = _run_perturbation_parallel(
            corpus, base_mapping, noise, models,
            n_mc_trials, use_kandles_bias, n_workers,
        )
        g_stats = _summarise_scores(trials, "greek", n_mc_trials)
        r3[str(noise)] = {
            "noise_fraction": noise,
            "trials": n_mc_trials,
            "greek": g_stats,
        }
        _print(f"  noise={noise:.0%}  greek={g_stats['mean']:.2f} "
               f"[{g_stats['ci_lo']:.2f},{g_stats['ci_hi']:.2f}]")
    results["exp3_perturbation"] = r3

    # ── Exp 4: Null distribution (parallel) ────────────────────────────
    _print("[Exp4] Random mapping controls (parallel)...")
    real_scores = run_one_trial(corpus, base_mapping, "no_vocab", models,
                                use_kandles_bias=use_kandles_bias)
    real_greek = real_scores.get("greek", 0.0)
    _print(f"  Real mapping: greek={real_greek:.2f}")
    null_types = [
        "frequency_matched_random",
        "cv_structure_preserving",
        "permuted_lb_correspondences",
    ]
    r4: dict[str, Any] = {"real_greek": real_greek, "nulls": {}}
    for nt in null_types:
        trials = _run_null_mapping_parallel(
            corpus, base_mapping, nt, models,
            n_mc_trials, use_kandles_bias, n_workers,
        )
        null_vals = [t.get("greek", 0.0) for t in trials if t]
        p_val = empirical_p_value(real_greek, null_vals)
        z = z_score(real_greek, null_vals)
        m, lo, hi = bootstrap_ci(null_vals)
        r4["nulls"][nt] = {
            "trials": n_mc_trials,
            "null_mean": round(m, 3),
            "null_ci": [round(lo, 3), round(hi, 3)],
            "real_score": real_greek,
            "p_value": round(p_val, 4),
            "z_score": round(z, 3),
            "pct_exceeding_real": round(
                sum(v >= real_greek for v in null_vals) / n_mc_trials * 100, 1
            ),
        }
        _print(f"  {nt}: mean={m:.2f}  p={p_val:.4f}  z={z:.2f}")
    results["exp4_null_distribution"] = r4

    # ── Exp 5: Scoring mode comparison ─────────────────────────────────
    _print("[Exp5] Scoring mode comparison...")
    r5: dict[str, Any] = {}
    for mode in SCORING_MODES:
        scores = run_one_trial(corpus, base_mapping, mode, models,
                               use_kandles_bias=use_kandles_bias)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        winner = ranked[0][0]
        greek_rank = next(i + 1 for i, (k, _) in enumerate(ranked) if k == "greek")
        r5[mode] = {
            "scores": scores,
            "winner": winner,
            "greek_rank": greek_rank,
            "greek_score": scores.get("greek", 0.0),
            "luwian_score": scores.get("luwian", 0.0),
        }
        mode_labels = {
            "full": "Full (bigram+Kandles+vocab)",
            "no_vocab": "No vocab (bigram+Kandles)",
            "kandles_only": "Kandles only",
        }
        _print(f"  {mode_labels[mode]}: "
               f"greek={scores.get('greek', 0):.2f}  "
               f"luwian={scores.get('luwian', 0):.2f}  "
               f"rank=#{greek_rank}  winner={winner}")
    results["exp5_scoring_modes"] = r5

    # ── Exp 6: Language model fairness ─────────────────────────────────
    _print("[Exp6] Language model fairness (equalized corpus sizes)...")
    from glossa_lab.experiments.linear_a_circularity import _get_language_models
    eq_models = _get_language_models(size=2000)
    scores_base = run_one_trial(corpus, base_mapping, "no_vocab", models,
                                use_kandles_bias=use_kandles_bias)
    scores_eq = run_one_trial(corpus, base_mapping, "no_vocab", eq_models,
                              use_kandles_bias=use_kandles_bias)
    ranked_base = sorted(scores_base.items(), key=lambda x: x[1], reverse=True)
    ranked_eq = sorted(scores_eq.items(), key=lambda x: x[1], reverse=True)
    _print(f"  Baseline:  greek={scores_base.get('greek', 0):.2f}  winner={ranked_base[0][0]}")
    _print(f"  Equalized: greek={scores_eq.get('greek', 0):.2f}  winner={ranked_eq[0][0]}")
    results["exp6_fairness"] = {
        "equalized_size": 2000,
        "baseline": {
            "scores": scores_base, "winner": ranked_base[0][0],
            "greek_rank": next(i + 1 for i, (k, _) in enumerate(ranked_base) if k == "greek"),
        },
        "equalized": {
            "scores": scores_eq, "winner": ranked_eq[0][0],
            "greek_rank": next(i + 1 for i, (k, _) in enumerate(ranked_eq) if k == "greek"),
        },
    }

    # ── Exp 7: Null corpus controls (parallel) ─────────────────────────
    _print("[Exp7] Null corpus controls (parallel)...")
    null_corpus_types = ["real", "shuffled", "unigram_only"]
    r7: dict[str, Any] = {}
    for nct in null_corpus_types:
        trials = _run_null_corpus_parallel(
            corpus, base_mapping, nct, models,
            n_mc_trials, use_kandles_bias, n_workers,
        )
        g_stats = _summarise_scores(trials, "greek", n_mc_trials)
        lw_stats = _summarise_scores(trials, "luwian", n_mc_trials)
        r7[nct] = {
            "null_type": nct,
            "trials": n_mc_trials,
            "greek": g_stats,
            "luwian": lw_stats,
        }
        _print(f"  {nct:20}  greek={g_stats['mean']:.2f}  luwian={lw_stats['mean']:.2f}")
    results["exp7_null_corpus"] = r7

    results["n_mc_trials"] = n_mc_trials
    return results


# ── Bias comparison ────────────────────────────────────────────────────

def run_bias_comparison(
    n_mc_trials: int = 30,
    n_workers: int | None = None,
    verbose: bool = True,
) -> dict[str, Any]:
    """Run Exp1 and Exp5 with both UNBIASED and BIASED Kandles and compare.

    Returns a compact dict with side-by-side Kandles scores for each
    hypothesis under default vs language-specific profiles.
    """
    from glossa_lab.accelerate import gpu_info  # noqa: I001
    from glossa_lab.experiments.linear_a_circularity import (
        _get_gorila_map,
        _get_language_models,
        _load_markov_corpus,
        _load_raw_corpus,
        run_one_trial,
        SCORING_MODES,
    )

    def _print(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _print("\n" + "="*65)
    _print("  KANDLES BIAS COMPARISON")
    _print("="*65)

    accel = gpu_info()
    _print(f"  Acceleration: {accel['tier_name']}  "
           f"({accel['cpu_cores']} cores"
           + (f"  GPU: {accel.get('gpu_name', '')}" if accel["cuda"] else "")
           + ")")

    flat, _ = _load_raw_corpus()
    corpus = flat if len(flat) > 100 else _load_markov_corpus()
    base_mapping = _get_gorila_map()
    models = _get_language_models()

    comparison: dict[str, Any] = {
        "acceleration": accel,
        "corpus_size": len(corpus),
    }

    # Run Exp5 (scoring modes) unbiased vs biased
    for bias in (False, True):
        label = "biased" if bias else "unbiased"
        _print(f"\n  -- Exp5 [{label.upper()}] scoring mode comparison --")
        mode_results: dict[str, Any] = {}
        for mode in SCORING_MODES:
            scores = run_one_trial(corpus, base_mapping, mode, models,
                                   use_kandles_bias=bias)
            ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            winner = ranked[0][0]
            greek_rank = next(i + 1 for i, (k, _) in enumerate(ranked) if k == "greek")
            mode_results[mode] = {
                "scores": scores,
                "winner": winner,
                "greek_rank": greek_rank,
                "luwian_rank": next(
                    i + 1 for i, (k, _) in enumerate(ranked) if k == "luwian"
                ),
            }
            _print(f"    {mode:12}  greek={scores.get('greek', 0):.2f}  "
                   f"luwian={scores.get('luwian', 0):.2f}  "
                   f"hurrian={scores.get('hurrian', 0):.2f}  "
                   f"winner={winner}")
        comparison[f"exp5_{label}"] = mode_results

    # Delta analysis
    _print("\n  -- Kandles-only bias delta (biased - unbiased) --")
    deltas: dict[str, float] = {}
    for hyp_id in ("greek", "luwian", "hurrian", "semitic"):
        unb = comparison["exp5_unbiased"].get("kandles_only", {}).get(
            "scores", {}).get(hyp_id, 0.0)
        bi  = comparison["exp5_biased"].get("kandles_only", {}).get(
            "scores", {}).get(hyp_id, 0.0)
        delta = round(bi - unb, 4)
        deltas[hyp_id] = delta
        dir_label = "▲" if delta > 0 else ("▼" if delta < 0 else "=")
        _print(f"    {hyp_id:10}  {unb:.4f} → {bi:.4f}  Δ={delta:+.4f}  {dir_label}")

    comparison["kandles_only_deltas"] = deltas
    comparison["interpretation"] = _interpret_deltas(deltas)
    _print(f"\n  Interpretation: {comparison['interpretation']}")

    return comparison


def _interpret_deltas(deltas: dict[str, float]) -> str:
    """Generate a one-line scientific interpretation of the delta results."""
    luw_delta = deltas.get("luwian", 0)
    grk_delta = deltas.get("greek", 0)

    lines = []
    if luw_delta > 0:
        lines.append(f"Luwian gains +{luw_delta:.4f} with own-language profile")
    elif luw_delta < 0:
        lines.append(f"Luwian loses {luw_delta:.4f} with own-language profile")

    if grk_delta < 0:
        lines.append(f"Greek loses {grk_delta:.4f} under fair evaluation (bias corrected)")
    elif grk_delta > 0:
        lines.append(f"Greek gains {grk_delta:.4f} (Greek profile is already default)")

    if lines:
        return "; ".join(lines) + "."
    return "No significant delta observed."


# ── CLI entry point ────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Kandles bias comparison and full anti-circularity suite."
    )
    parser.add_argument(
        "--trials", type=int, default=30,
        help="MC trials per stochastic experiment (default: 30)",
    )
    parser.add_argument(
        "--workers", type=int, default=None,
        help="Parallel worker processes (default: cpu_count-1)",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress progress output",
    )
    parser.add_argument(
        "--bias-only", action="store_true",
        help="Only run the fast bias comparison (Exp1+Exp5), skip full suite",
    )
    parser.add_argument(
        "--output", type=str,
        default=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(_HERE))),
            "reports", "kandles_biased_results.json",
        ),
        help="Output JSON path (default: reports/kandles_biased_results.json)",
    )
    args = parser.parse_args()

    verbose = not args.quiet
    t_start = time.time()

    from glossa_lab.accelerate import gpu_info
    accel = gpu_info()
    if verbose:
        print("\nGlossa Lab — Kandles Bias Experiment Runner")
        print(f"Acceleration tier: {accel['tier']}  ({accel['tier_name']})")
        if accel.get("gpu_name"):
            print(f"GPU: {accel['gpu_name']}  ({accel.get('gpu_mem_gb', '?')} GB)")
        print(f"CPU cores: {accel['cpu_cores']}")
        print(f"MC trials: {args.trials}")
        print()

    all_results: dict[str, Any] = {
        "meta": {
            "trials": args.trials,
            "workers": args.workers,
            "acceleration": accel,
        },
    }

    # 1. Bias comparison (always run)
    all_results["bias_comparison"] = run_bias_comparison(
        n_mc_trials=args.trials,
        n_workers=args.workers,
        verbose=verbose,
    )

    if not args.bias_only:
        # 2. Full suite unbiased
        if verbose:
            print("\n" + "─"*65)
            print("Running FULL SUITE (unbiased) ...")
        all_results["suite_unbiased"] = run_parallel_experiments(
            n_mc_trials=args.trials,
            use_kandles_bias=False,
            n_workers=args.workers,
            verbose=verbose,
        )

        # 3. Full suite biased
        if verbose:
            print("\n" + "─"*65)
            print("Running FULL SUITE (biased) ...")
        all_results["suite_biased"] = run_parallel_experiments(
            n_mc_trials=args.trials,
            use_kandles_bias=True,
            n_workers=args.workers,
            verbose=verbose,
        )

        # 4. Summary table
        all_results["summary"] = _build_summary(
            all_results["suite_unbiased"],
            all_results["suite_biased"],
        )
        if verbose:
            _print_summary(all_results["summary"])

    elapsed = round(time.time() - t_start, 1)
    all_results["elapsed_seconds"] = elapsed

    # Save output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(all_results, fh, indent=2)

    if verbose:
        print(f"\nResults saved → {args.output}")
        print(f"Total time: {elapsed}s")


def _build_summary(
    unbiased: dict[str, Any],
    biased: dict[str, Any],
) -> dict[str, Any]:
    """Build a side-by-side comparison table from two full-suite results."""
    summary: dict[str, Any] = {}

    def _exp5_scores(suite: dict[str, Any], mode: str) -> dict[str, float]:
        return suite.get("exp5_scoring_modes", {}).get(mode, {}).get("scores", {})

    for mode in ("full", "no_vocab", "kandles_only"):
        unb = _exp5_scores(unbiased, mode)
        bi  = _exp5_scores(biased, mode)
        summary[f"exp5_{mode}"] = {
            hyp: {
                "unbiased": round(unb.get(hyp, 0), 4),
                "biased":   round(bi.get(hyp, 0), 4),
                "delta":    round(bi.get(hyp, 0) - unb.get(hyp, 0), 4),
            }
            for hyp in ("greek", "luwian", "hurrian", "semitic")
        }

    # Exp1 ALL split winner comparison
    unb_exp1 = unbiased.get("exp1_raw_tablet", {}).get("ALL", {})
    bi_exp1  = biased.get("exp1_raw_tablet", {}).get("ALL", {})
    summary["exp1_ALL"] = {
        "unbiased_winner": unb_exp1.get("winner"),
        "biased_winner":   bi_exp1.get("winner"),
        "unbiased_greek":  unb_exp1.get("greek_score"),
        "biased_greek":    bi_exp1.get("greek_score"),
        "unbiased_luwian": unb_exp1.get("scores", {}).get("luwian"),
        "biased_luwian":   bi_exp1.get("scores", {}).get("luwian"),
    }
    return summary


def _print_summary(summary: dict[str, Any]) -> None:
    print("\n" + "="*65)
    print("  SUMMARY: Unbiased vs Biased Kandles scores")
    print("="*65)
    print(f"  {'Hyp':10}  {'Unbiased':>10}  {'Biased':>10}  {'Delta':>8}")
    print("  " + "-"*50)

    for mode in ("full", "no_vocab", "kandles_only"):
        key = f"exp5_{mode}"
        if key not in summary:
            continue
        mode_label = {"full": "Full", "no_vocab": "No-vocab",
                      "kandles_only": "Kandles-only"}[mode]
        print(f"\n  [Exp5 — {mode_label}]")
        for hyp in ("greek", "luwian", "hurrian", "semitic"):
            d = summary[key].get(hyp, {})
            delta = d.get("delta", 0)
            arrow = "▲" if delta > 0.001 else ("▼" if delta < -0.001 else "=")
            print(f"  {hyp:10}  {d.get('unbiased', 0):>10.4f}  "
                  f"{d.get('biased', 0):>10.4f}  {delta:>+8.4f} {arrow}")

    print()
    exp1 = summary.get("exp1_ALL", {})
    if exp1:
        print(f"  [Exp1 ALL]  "
              f"Unbiased winner: {exp1.get('unbiased_winner')}  "
              f"Biased winner: {exp1.get('biased_winner')}")
        ug = exp1.get('unbiased_greek', 0) or 0
        bg = exp1.get('biased_greek', 0) or 0
        ul = exp1.get('unbiased_luwian', 0) or 0
        bl = exp1.get('biased_luwian', 0) or 0
        print(f"    Greek:  {ug:.2f} \u2192 {bg:.2f}")
        print(f"    Luwian: {ul:.2f} \u2192 {bl:.2f}")


if __name__ == "__main__":
    # Required guard for Windows multiprocessing
    import multiprocessing
    multiprocessing.freeze_support()
    main()
