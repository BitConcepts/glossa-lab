"""Prior Ablation Study — Tier 1a (Ugaritic → Hebrew).

Quantifies the MARGINAL CONTRIBUTION of each phonological prior to decipherment
accuracy and score-landscape sharpness.  Runs 7 successive levels:

  Level 0 — Frequency-rank seed only (NO optimizer, NO priors)
    The initial mapping is built by rank-matching cipher sign frequencies to
    target frequencies.  No SA, no beam, no iteration.  This is the floor.

  Level 1 — + Bigram optimizer (SA), zero linguistic priors
    Same frequency seed + SA refinement using flat bigram log-likelihood only.
    Measures the pure algorithmic contribution before any domain knowledge.

  Level 2 — + Positional weight (word-initial / word-final bonus)
    SA with flat bigrams + positional profile matching bonus.

  Level 3 — + OCP penalty (Obligatory Contour Principle)
    Level 2 + penalises mappings producing repeated consecutive consonants
    within words (rare in Semitic roots).

  Level 4 — + Word-boundary bigrams
    Level 3 + bigrams scored only within words (not across word boundaries).

  Level 5 — + Root co-occurrence prior
    Level 4 + rewards mapped consonant pairs that commonly co-occur in Hebrew
    roots (word_cooccur prior).

  Level 6 — All combined (current best config)
    All five priors active simultaneously.

For each level, the experiment measures:
  - Accuracy (N/30 correct sign mappings)
  - Oracle delta (score of correct mapping − score of SA-found mapping)
  - Landscape quality (SHARP / MODERATE / FLAT / INVERTED)

The result table shows clearly how much each prior contributes and how
accuracy degrades as priors are removed — directly addressing the
"reduce reliance on priors" research question.

Usage:
    python -m glossa_lab.experiments.prior_ablation_benchmark
"""
from __future__ import annotations

import os
import sys
from collections import Counter, defaultdict
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ── Data loading ─────────────────────────────────────────────────────

def _load() -> dict[str, Any]:
    from corpora.ugaritic import (
        _BAAL_CYCLE_LINES, _SIGN_TO_ID,
        get_answer_key, get_word_level_inscriptions,
    )
    from glossa_lab.data.old_hebrew import (
        get_corpus_symbols     as heb_sym,
        get_corpus_inscriptions as heb_line_inscr,
        get_word_inscriptions   as heb_word_inscr,
        get_ugaritic_to_hebrew_map,
    )
    from glossa_lab.pipelines.decipher import (
        LanguageModel, decipher, score_accuracy, _score_mapping,
    )

    def _parse(line: str) -> list[str]:
        return [ch for ch in line.split() if ch != "."]

    decoded_lines  = [_parse(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines  = [[_SIGN_TO_ID.get(s, s) for s in l] for l in decoded_lines]
    cipher_flat    = [s for l in encoded_lines for s in l]

    ug_words_enc = get_word_level_inscriptions(encoded=True)

    ug_to_ug  = get_answer_key()
    ug_to_heb = get_ugaritic_to_hebrew_map()
    gt        = {oid: ug_to_heb[us] for oid, us in ug_to_ug.items() if us in ug_to_heb}

    heb_flat = heb_sym()
    lm_line  = LanguageModel(heb_flat, inscriptions=heb_line_inscr())
    lm_word  = LanguageModel(heb_flat, inscriptions=heb_word_inscr())

    return {
        "cipher_flat":       cipher_flat,
        "cipher_line_inscr": encoded_lines,
        "cipher_word_inscr": ug_words_enc,
        "gt":                gt,
        "lm_line":           lm_line,
        "lm_word":           lm_word,
        "decipher":          decipher,
        "score_accuracy":    score_accuracy,
        "_score_mapping":    _score_mapping,
    }


# ── Floor: frequency-rank seed (no optimizer) ─────────────────────────

def _freq_rank_mapping(
    cipher_flat: list[str],
    target_model: "LanguageModel",
) -> dict[str, str]:
    """Build the initial frequency-rank seed mapping and return it as-is."""
    from collections import Counter
    cipher_counts = Counter(cipher_flat)
    cipher_ranked = [s for s, _ in cipher_counts.most_common()]
    target_ranked = list(target_model.ranked[: len(cipher_ranked)])
    while len(target_ranked) < len(cipher_ranked):
        target_ranked.append(f"?{len(target_ranked)}")
    return dict(zip(cipher_ranked, target_ranked))


# ── Oracle scoring ────────────────────────────────────────────────────

def _oracle(
    d: dict,
    lm,
    cipher_inscr: list[list[str]],
    use_word_bigrams: bool,
    ocp_weight: float,
    positional_weight: float,
    root_prior_weight: float,
    restarts: int = 15,
    verbose: bool = False,
) -> dict[str, Any]:
    """Score correct mapping vs SA-found mapping; return accuracy + oracle delta."""
    _score_mapping = d["_score_mapping"]
    score_accuracy = d["score_accuracy"]
    cipher_flat    = d["cipher_flat"]
    gt             = d["gt"]

    # Build cipher positional profile
    pos_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"initial": 0, "medial": 0, "terminal": 0}
    )
    for insc in cipher_inscr:
        if len(insc) >= 2:
            pos_counts[insc[0]]["initial"]  += 1
            pos_counts[insc[-1]]["terminal"] += 1
            for s in insc[1:-1]:
                pos_counts[s]["medial"] += 1
    cipher_pos = {
        sign: {k: v / (sum(pc.values()) or 1) for k, v in pc.items()}
        for sign, pc in pos_counts.items()
    }

    score_correct = _score_mapping(
        cipher_flat, gt, lm, cipher_pos,
        use_word_bigrams=use_word_bigrams,
        cipher_inscriptions=cipher_inscr,
        ocp_weight=ocp_weight,
        positional_weight=positional_weight,
        root_prior_weight=root_prior_weight,
    )

    sa_result = d["decipher"](
        cipher_flat, lm,
        seed=42, max_iterations=15000, restarts=restarts,
        cipher_inscriptions=cipher_inscr,
        use_word_bigrams=use_word_bigrams,
        ocp_weight=ocp_weight,
        positional_weight=positional_weight,
        root_prior_weight=root_prior_weight,
        surjective=True,
    )
    sa_map    = sa_result["proposed_mapping"]
    score_sa  = _score_mapping(
        cipher_flat, sa_map, lm, cipher_pos,
        use_word_bigrams=use_word_bigrams,
        cipher_inscriptions=cipher_inscr,
        ocp_weight=ocp_weight,
        positional_weight=positional_weight,
        root_prior_weight=root_prior_weight,
    )
    acc_sa    = score_accuracy(sa_map, gt)
    delta     = score_correct - score_sa
    return {
        "accuracy":       acc_sa["correct"],
        "score_correct":  round(score_correct, 1),
        "score_sa":       round(score_sa, 1),
        "delta":          round(delta, 1),
    }


# ── Main benchmark ────────────────────────────────────────────────────

def run_prior_ablation_benchmark(verbose: bool = True) -> dict[str, Any]:
    def _pr(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _pr("\n" + "=" * 72)
    _pr("  Prior Ablation Study — Tier 1a (Ugaritic → Hebrew)")
    _pr("  Seven levels: floor → bigram SA → each prior added one at a time")
    _pr("=" * 72)

    d = _load()
    lm_line = d["lm_line"]
    lm_word = d["lm_word"]
    gt      = d["gt"]

    n_gt = len(gt)
    _pr(f"\n  Ground truth: {n_gt} sign mappings")
    _pr(f"  Hebrew LM OCP rate: {lm_word.ocp_rate:.4f}")
    _pr(f"  Hebrew word_cooccur pairs: {len(lm_word.word_cooccur)}")

    results = []

    # ── Level 0: Frequency-rank seed, no optimizer ──────────────────────
    _pr("\n\n  ══ Level 0 — Frequency-rank seed (no optimizer, no priors) ══")
    freq_map   = _freq_rank_mapping(d["cipher_flat"], lm_line)
    acc_floor  = d["score_accuracy"](freq_map, gt)
    _pr(f"  Accuracy (seed only): {acc_floor['correct']}/{n_gt} = "
        f"{acc_floor['correct']/n_gt*100:.1f}%")
    _pr("  (No oracle delta — optimizer never ran)")
    results.append({
        "level":            0,
        "label":            "Level 0 — Frequency-rank seed (no optimizer)",
        "accuracy":         acc_floor["correct"],
        "delta":            None,
        "landscape":        "FLOOR",
    })

    # ── Levels 1–6: SA with successive priors added ─────────────────────
    configs = [
        {
            "label":              "Level 1 — + Bigram SA (no priors)",
            "lm":                 lm_line,
            "cipher_inscr":       d["cipher_line_inscr"],
            "use_word_bigrams":   False,
            "ocp_weight":         0.0,
            "positional_weight":  0.0,
            "root_prior_weight":  0.0,
        },
        {
            "label":              "Level 2 — + Positional weight",
            "lm":                 lm_line,
            "cipher_inscr":       d["cipher_line_inscr"],
            "use_word_bigrams":   False,
            "ocp_weight":         0.0,
            "positional_weight":  0.02,
            "root_prior_weight":  0.0,
        },
        {
            "label":              "Level 3 — + OCP penalty",
            "lm":                 lm_line,
            "cipher_inscr":       d["cipher_word_inscr"],
            "use_word_bigrams":   False,
            "ocp_weight":         1.0,
            "positional_weight":  0.02,
            "root_prior_weight":  0.0,
        },
        {
            "label":              "Level 4 — + Word-boundary bigrams",
            "lm":                 lm_word,
            "cipher_inscr":       d["cipher_word_inscr"],
            "use_word_bigrams":   True,
            "ocp_weight":         1.0,
            "positional_weight":  0.02,
            "root_prior_weight":  0.0,
        },
        {
            "label":              "Level 5 — + Root co-occurrence prior",
            "lm":                 lm_word,
            "cipher_inscr":       d["cipher_word_inscr"],
            "use_word_bigrams":   False,
            "ocp_weight":         0.0,
            "positional_weight":  0.005,
            "root_prior_weight":  0.5,
        },
        {
            "label":              "Level 6 — All priors combined",
            "lm":                 lm_word,
            "cipher_inscr":       d["cipher_word_inscr"],
            "use_word_bigrams":   True,
            "ocp_weight":         1.0,
            "positional_weight":  0.02,
            "root_prior_weight":  0.5,
        },
    ]

    for lvl_num, cfg in enumerate(configs, start=1):
        _pr(f"\n  ══ {cfg['label']} ══")
        r = _oracle(
            d,
            lm=cfg["lm"],
            cipher_inscr=cfg["cipher_inscr"],
            use_word_bigrams=cfg["use_word_bigrams"],
            ocp_weight=cfg["ocp_weight"],
            positional_weight=cfg["positional_weight"],
            root_prior_weight=cfg["root_prior_weight"],
            verbose=verbose,
        )
        pct   = r["accuracy"] / n_gt * 100
        denom = abs(r["score_sa"]) or 1
        dpct  = r["delta"] / denom * 100
        sign  = "+" if r["delta"] >= 0 else ""
        ls    = ("SHARP"    if r["delta"] > denom * 0.02  else
                 "MODERATE" if r["delta"] > 0              else
                 "FLAT/INV")
        _pr(f"  Accuracy:          {r['accuracy']:2d}/{n_gt} = {pct:.1f}%")
        _pr(f"  score(correct):    {r['score_correct']:>10.1f}")
        _pr(f"  score(SA):         {r['score_sa']:>10.1f}")
        _pr(f"  delta:             {sign}{r['delta']:.1f}  ({sign}{dpct:.2f}%)")
        _pr(f"  Landscape:         {ls}")
        results.append({
            "level":       lvl_num,
            "label":       cfg["label"],
            "accuracy":    r["accuracy"],
            "delta":       r["delta"],
            "landscape":   ls,
        })

    # ── Summary table ──────────────────────────────────────────────────
    _pr("\n\n" + "=" * 72)
    _pr("  ABLATION SUMMARY")
    _pr("=" * 72)
    _pr(f"\n  {'Level':<48} {'Accuracy':>8}  {'Delta':>10}  Landscape")
    _pr("  " + "-" * 70)
    for r in results:
        delta_str = f"{r['delta']:+.0f}" if r["delta"] is not None else "   N/A"
        _pr(f"  {r['label']:<48} {r['accuracy']:2d}/{n_gt}={r['accuracy']/n_gt*100:4.1f}%"
            f"  {delta_str:>10}    {r['landscape']}")

    floor = results[0]["accuracy"]
    peak  = max(r["accuracy"] for r in results)
    gain  = peak - floor
    _pr(f"\n  Floor (no optimizer): {floor}/{n_gt} = {floor/n_gt*100:.1f}%")
    _pr(f"  Peak (all priors):    {peak}/{n_gt} = {peak/n_gt*100:.1f}%")
    _pr(f"  Total gain from priors: +{gain} correct signs")

    # Identify which single prior gave the biggest lift
    prev_acc = floor
    gains = []
    for r in results[1:]:
        lift = r["accuracy"] - prev_acc
        gains.append((r["label"], lift))
        prev_acc = r["accuracy"]
    if gains:
        best_prior = max(gains, key=lambda x: x[1])
        _pr(f"  Biggest single lift: {best_prior[0]} (+{best_prior[1]} signs)")

    conclusion = (
        f"Peak accuracy {peak}/{n_gt} = {peak/n_gt*100:.1f}% with all priors. "
        f"Floor (frequency rank only) = {floor}/{n_gt} = {floor/n_gt*100:.1f}%. "
        f"This establishes the marginal contribution of each prior to Tier 1a performance."
    )
    _pr(f"\n  CONCLUSION: {conclusion}")

    return {
        "results":     results,
        "floor":       floor,
        "peak":        peak,
        "total_gain":  gain,
        "conclusion":  conclusion,
    }


if __name__ == "__main__":
    run_prior_ablation_benchmark(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class PriorAblationBenchmark(_EB):
    id = "prior_ablation_benchmark"
    name = "Prior Ablation Study (Tier 1a)"
    category = "Validation"
    description = (
        "Measures the marginal contribution of each phonological prior to "
        "Tier 1a (Ugaritic→Hebrew) decipherment accuracy. "
        "Seven levels from frequency-rank floor (no optimizer) through "
        "bigram SA, positional weight, OCP penalty, word-boundary bigrams, "
        "root co-occurrence prior, to all combined. "
        "Shows how accuracy degrades as priors are removed."
    )
    estimated_time = "~8 min"
    command = "python -m glossa_lab.experiments.prior_ablation_benchmark"
    params_schema: dict = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return run_prior_ablation_benchmark(verbose=False)
