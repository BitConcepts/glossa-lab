"""Fuls Split Sensitivity Analysis — Ugaritic→Hebrew.

Addresses Dr. Fuls' question:
  "Does the accuracy change with different train/test split ratios,
   such as 50/50? Have you tried random selection for multiple tests?"

Observation to investigate: 66.7% accuracy for a ~2/3 training split.
If accuracy simply tracks the training fraction this would indicate the
model is learning nothing beyond the proportion of data it has seen —
a serious methodological concern.  This experiment tests that directly.

METHODOLOGY
-----------
For each split fraction f in [0.10, 0.25, 0.33, 0.50, 0.67, 0.75, 0.90]:
  A. Sequential split: first f×82 lines → LM,  remaining → cipher
  B. Random sampling (5 independent seeds): random f×82 lines → LM,
     remaining → cipher

We report:
  - Accuracy per split (sequential and random mean ± std)
  - Pearson correlation of accuracy vs. training fraction
  - Whether the 66.7% coincidence with 2/3 is structural or artefact

Usage:
    python -m glossa_lab.experiments.fuls_split_sensitivity
"""

from __future__ import annotations

import math
import os
import random
import sys
from typing import Any

from glossa_lab.experiments._parallel import run_seeds_parallel as _rsp_ss

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ── Helpers ────────────────────────────────────────────────────────────

def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = _mean(xs), _mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx  = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy  = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (dx * dy) if dx * dy else 0.0


# ── Core run ───────────────────────────────────────────────────────────

def _run_one(decoded_lines, encoded_lines, answer_key, train_indices):
    """Run SA decipherment with a given set of training line indices."""
    from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy  # noqa

    train_decoded = [decoded_lines[i] for i in train_indices]
    test_idx      = [i for i in range(len(decoded_lines)) if i not in set(train_indices)]
    test_encoded  = [encoded_lines[i] for i in test_idx]

    train_flat   = [s for line in train_decoded for s in line]
    test_flat    = [s for line in test_encoded  for s in line]
    test_inscr   = test_encoded

    if not train_flat or not test_flat:
        return None

    lm     = LanguageModel(train_flat, inscriptions=train_decoded)
    result = decipher(
        test_flat, lm,
        seed=42,
        max_iterations=10000,
        restarts=10,
        cipher_inscriptions=test_inscr,
        surjective=True,
    )
    acc = score_accuracy(result["proposed_mapping"], answer_key)
    return acc["correct"], acc["total"], acc["accuracy"]


# ── Main experiment ────────────────────────────────────────────────────

def run_split_sensitivity(verbose: bool = True) -> dict[str, Any]:
    from corpora.ugaritic import (
        _BAAL_CYCLE_LINES, _SIGN_TO_ID, get_answer_key,
    )
    from glossa_lab.data.old_hebrew import get_ugaritic_to_hebrew_map

    def _pr(*a, **kw):
        if verbose:
            print(*a, **kw)

    def _parse(line: str) -> list[str]:
        return [c for c in line.split() if c != "."]

    decoded_lines = [_parse(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines = [[_SIGN_TO_ID.get(s, s) for s in line] for line in decoded_lines]
    ug_to_ug   = get_answer_key()
    ug_to_heb  = get_ugaritic_to_hebrew_map()
    answer_key = {oid: ug_to_heb[us] for oid, us in ug_to_ug.items() if us in ug_to_heb}

    n = len(decoded_lines)
    fractions = [0.10, 0.25, 0.33, 0.50, 0.67, 0.75, 0.90]
    n_random_seeds = 5
    results = []

    _pr("\n" + "=" * 72)
    _pr("  Fuls Split Sensitivity — Ugaritic → Hebrew (Baal Cycle, 82 lines)")
    _pr("=" * 72)
    _pr(f"  Total lines: {n}   Distinct cipher signs: {len(set(s for l in encoded_lines for s in l))}")
    _pr(f"  Answer key:  {len(answer_key)}/30 Ugaritic→Hebrew mappings")
    _pr()
    _pr(f"  {'Fraction':>8}  {'N_train':>7}  {'Seq Acc':>9}  {'Rand Mean':>10}  {'Rand Std':>9}  {'Note'}")
    _pr("  " + "-" * 62)

    all_fracs, all_seq_accs, all_rand_accs = [], [], []

    for frac in fractions:
        n_train = max(1, int(round(n * frac)))
        n_test  = n - n_train
        if n_test < 1:
            continue

        # A. Sequential split
        seq_indices = list(range(n_train))
        seq_res = _run_one(decoded_lines, encoded_lines, answer_key, seq_indices)
        seq_acc = seq_res[2] if seq_res else 0.0
        seq_str = f"{seq_res[0]}/{seq_res[1]}={seq_acc*100:.1f}%" if seq_res else "N/A"

        # B. Random sampling with multiple seeds — parallel execution
        def _rand_seed(seed, _n=n, _n_train=n_train,
                       _dl=decoded_lines, _el=encoded_lines, _ak=answer_key):
            rng = random.Random(seed * 1000 + 7)
            rand_idx = sorted(rng.sample(range(_n), _n_train))
            r = _run_one(_dl, _el, _ak, rand_idx)
            return r[2] if r else None
        _raw = _rsp_ss(_rand_seed, list(range(n_random_seeds)))
        rand_accs = [r for r in _raw if r is not None]

        rand_mean = _mean(rand_accs)
        rand_std  = _std(rand_accs)

        note = ""
        if abs(frac - 0.67) < 0.02:
            note = "← 2/3 split (Fuls reference)"
        if abs(frac - 0.75) < 0.02:
            note = "← existing proper benchmark"

        _pr(
            f"  {frac:8.0%}  {n_train:7d}  {seq_str:>9}  "
            f"{rand_mean*100:9.1f}%  {rand_std*100:8.1f}%  {note}"
        )

        all_fracs.append(frac)
        all_seq_accs.append(seq_acc)
        all_rand_accs.append(rand_mean)
        results.append({
            "fraction": frac,
            "n_train":  n_train,
            "n_test":   n_test,
            "sequential": {
                "correct": seq_res[0] if seq_res else None,
                "total":   seq_res[1] if seq_res else None,
                "accuracy": seq_acc,
            },
            "random": {
                "mean":    rand_mean,
                "std":     rand_std,
                "n_seeds": len(rand_accs),
                "individual": rand_accs,
            },
        })

    # Correlation analysis
    r_seq  = _pearson(all_fracs, all_seq_accs)
    r_rand = _pearson(all_fracs, all_rand_accs)

    _pr()
    _pr("  CORRELATION ANALYSIS:")
    _pr(f"  Pearson r (fraction vs sequential accuracy): {r_seq:+.3f}")
    _pr(f"  Pearson r (fraction vs random-mean accuracy): {r_rand:+.3f}")
    _pr()

    if abs(r_seq) > 0.85:
        correlation_verdict = (
            "STRONG — accuracy tracks training fraction linearly. "
            "The 66.7% result is NOT coincidental; the model's performance "
            "scales with the amount of training data in a near-linear way, "
            "which indicates the statistical signal is weak and the model is "
            "relying heavily on the proportion of the vocabulary it has seen."
        )
    elif abs(r_seq) > 0.5:
        correlation_verdict = (
            "MODERATE — some positive correlation between fraction and accuracy, "
            "but the relationship is not linear. The 66.7% coincidence with the "
            "2/3 split may be partly structural and partly noise."
        )
    else:
        correlation_verdict = (
            "WEAK — accuracy does NOT track the training fraction. "
            "The 66.7% result coincides with the 2/3 split by chance. "
            "Performance is driven by factors other than sheer data volume."
        )

    _pr(f"  Verdict: {correlation_verdict}")
    _pr()
    _pr("  INTERPRETATION FOR DR. FULS:")
    _pr("  The critical question is whether the algorithm is genuinely learning")
    _pr("  phonotactic structure from the Hebrew LM, or simply benefiting from")
    _pr("  seeing more of the same corpus.  If r > 0.85, this is evidence that")
    _pr("  the result is largely driven by corpus overlap (circularity), not")
    _pr("  genuine phonotactic generalisation.  Random-split std tells us how")
    _pr("  stable the result is across different partitions of the same data.")

    return {
        "split_results": results,
        "correlation_sequential": round(r_seq, 4),
        "correlation_random_mean": round(r_rand, 4),
        "correlation_verdict": correlation_verdict,
        "corpus": {"total_lines": n, "answer_key_size": len(answer_key)},
    }


if __name__ == "__main__":
    from glossa_lab.cli_bridge import run_with_reporting
    run_with_reporting(
        "fuls_split_sensitivity",
        "Fuls Split Sensitivity Analysis",
        run_split_sensitivity, verbose=True,
    )

try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class FulsSplitSensitivity(_EB):
    id             = "fuls_split_sensitivity"
    name           = "Fuls Split Sensitivity Analysis"
    category       = "Validation"
    description    = (
        "Tests whether decipherment accuracy tracks the training/test split ratio "
        "(Dr. Fuls question). Sweeps 10–90% splits with both sequential and random "
        "sampling across 5 seeds. Reports Pearson correlation of accuracy vs. fraction."
    )
    estimated_time = "~3–5 min"
    command        = "python -m glossa_lab.experiments.fuls_split_sensitivity"

    def run(self, **kwargs) -> dict:
        return run_split_sensitivity(verbose=False)
