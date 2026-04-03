"""Ventris Grid Validation Experiment.

SCIENTIFIC CLAIM BEING VALIDATED:
  Our GPU-accelerated affinity analysis (vowel/consonant context similarity)
  can automatically reconstruct the Ventris grid for Linear B — without
  knowing the language — using only distributional statistics.

HISTORICAL CONTEXT:
  Michael Ventris (1952) deciphered Linear B by observing that:
    1. Some signs share a VOWEL: they appear in the same structural positions
       (same slot in inflectional paradigms), so their left-context distributions
       are similar. These signs form ROWS of a CV grid.
    2. Some signs share a CONSONANT: they appear before the same set of
       vowel-initial signs, so their right-context distributions are similar.
       These signs form COLUMNS of a CV grid.

  Ventris built his grid manually from thousands of tablets. We test whether
  our automatic method — GPU cosine similarity on context frequency vectors —
  recovers the same groupings.

GROUND TRUTH (Linear B known syllabary):
  Rows (same vowel -V):
    -a: a, da, ja, ka, ma, na, pa, ra, sa, ta, wa, za  (and qa, nwa, etc.)
    -e: e, de, ke, me, ne, pe, re, se, te, we, ze
    -i: i, di, ki, mi, ni, pi, ri, si, ti, wi
    -o: o, do, jo, ko, mo, no, po, ro, so, to, wo, zo
    -u: u, du, ku, mu, nu, pu, ru, su, tu
  Columns (same consonant C-):
    d-: da, de, di, do, du
    k-: ka, ke, ki, ko, ku
    m-: ma, me, mi, mo, mu
    n-: na, ne, ni, no, nu
    p-: pa, pe, pi, po, pu
    r-: ra, re, ri, ro, ru
    s-: sa, se, si, so, su
    t-: ta, te, ti, to, tu

METRICS:
  precision_row:     fraction of predicted vowel groups that are correct
  recall_row:        fraction of true vowel groups recovered
  f1_row:            harmonic mean
  precision_col:     fraction of predicted consonant groups that are correct
  recall_col:        fraction of true consonant groups recovered
  f1_col:            harmonic mean
  correct_pairs:     fraction of sign pairs correctly grouped (same row or col)

Usage:
    python -m glossa_lab.experiments.ventris_validation
"""

from __future__ import annotations

import os
import sys
from collections import Counter
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Ground truth Linear B grid ────────────────────────────────────────

# ROW = same vowel (same ending)
_TRUE_ROWS: list[list[str]] = [
    ["a",  "da", "ja",  "ka",  "ma",  "na",  "pa",  "ra",  "sa",  "ta",  "wa",  "za"],
    ["e",  "de",        "ke",  "me",  "ne",  "pe",  "re",  "se",  "te",  "we",  "ze"],
    ["i",  "di",        "ki",  "mi",  "ni",  "pi",  "ri",  "si",  "ti",  "wi"],
    ["o",  "do", "jo",  "ko",  "mo",  "no",  "po",  "ro",  "so",  "to",  "wo",  "zo"],
    ["u",  "du",        "ku",  "mu",  "nu",  "pu",  "ru",  "su",  "tu"],
]

# COLUMN = same consonant (same onset)
_TRUE_COLS: list[list[str]] = [
    ["da", "de", "di", "do", "du"],
    ["ja", "je", "jo"],
    ["ka", "ke", "ki", "ko", "ku"],
    ["ma", "me", "mi", "mo", "mu"],
    ["na", "ne", "ni", "no", "nu"],
    ["pa", "pe", "pi", "po", "pu"],
    ["ra", "re", "ri", "ro", "ru"],
    ["sa", "se", "si", "so", "su"],
    ["ta", "te", "ti", "to", "tu"],
    ["wa", "we", "wi", "wo"],
    ["za", "ze", "zo"],
]


def _sign_to_row() -> dict[str, int]:
    m = {}
    for row_idx, row in enumerate(_TRUE_ROWS):
        for s in row:
            m[s] = row_idx
    return m

def _sign_to_col() -> dict[str, int]:
    m = {}
    for col_idx, col in enumerate(_TRUE_COLS):
        for s in col:
            m[s] = col_idx
    return m


# ── Precision/recall scoring ──────────────────────────────────────────

def _score_clusters(
    predicted: list[list[str]],
    ground_truth_map: dict[str, int],
    label: str,
    verbose: bool = True,
) -> dict[str, Any]:
    """Score predicted clusters against ground truth.

    A predicted cluster is CORRECT if all its members share the same
    ground-truth group index (pure cluster).

    Returns precision, recall, F1, and details.
    """
    n_predicted_multi = 0

    # Build ground truth pairs
    gt_same: set[frozenset[str]] = set()
    for group in ground_truth_map.values() if False else []:
        pass
    # Group signs by their ground truth class
    from collections import defaultdict
    gt_groups: dict[int, set[str]] = defaultdict(set)
    for sign, gidx in ground_truth_map.items():
        gt_groups[gidx].add(sign)
    for g in gt_groups.values():
        signs = list(g)
        for i in range(len(signs)):
            for j in range(i + 1, len(signs)):
                gt_same.add(frozenset([signs[i], signs[j]]))

    pred_pairs: set[frozenset[str]] = set()
    for group in predicted:
        if len(group) >= 2:
            n_predicted_multi += 1
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    pred_pairs.add(frozenset([group[i], group[j]]))

    tp = len(pred_pairs & gt_same)
    fp = len(pred_pairs - gt_same)
    fn = len(gt_same - pred_pairs)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    if verbose:
        print(f"  [{label}] pairs TP={tp} FP={fp} FN={fn}  "
              f"P={precision:.3f} R={recall:.3f} F1={f1:.3f}")

        # Show best correct clusters
        print(f"  [{label}] predicted groups (multi-sign only):")
        for g in sorted(predicted, key=len, reverse=True)[:8]:
            if len(g) >= 2:
                # Check purity
                gt_ids = {ground_truth_map.get(s, -1) for s in g}
                pure = len(gt_ids) == 1 and -1 not in gt_ids
                tag = "✓" if pure else "✗"
                print(f"    {tag} {sorted(g)}")

    return {
        "precision":   round(precision, 4),
        "recall":      round(recall, 4),
        "f1":          round(f1, 4),
        "true_pairs":  len(gt_same),
        "pred_pairs":  len(pred_pairs),
        "true_positives": tp,
    }


# ── Main validation ───────────────────────────────────────────────────

def run_ventris_validation(verbose: bool = True) -> dict[str, Any]:
    """Load Linear B corpus, run affinity analysis, score against ground truth."""
    from glossa_lab.accelerate import gpu_info  # noqa: I001
    from glossa_lab.pipelines.logosyllabic import classify_signs, compute_affinity
    from pathlib import Path

    def _print(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _print("\n" + "="*70)
    _print("  Ventris Grid Validation — Linear B")
    _print("="*70)

    accel = gpu_info()
    _print(f"  Acceleration: {accel['tier_name']}  ({accel['cpu_cores']} cores"
           + (f"  GPU: {accel.get('gpu_name', '')}" if accel["cuda"] else "") + ")")

    # Load Linear B word-level corpus
    fixture = (
        Path(_BACKEND) / "tests" / "corpora" / "fixtures" / "linear_b.txt"
    )
    text = fixture.read_text(encoding="utf-8")
    inscriptions: list[list[str]] = []
    for line in text.splitlines():
        for word in line.strip().split():
            parts = word.replace("3", "").split("-")
            signs = [
                p.strip().lower()
                for p in parts
                if p.strip() and p.strip().replace("*", "").replace("2", "").isalpha()
            ]
            if len(signs) >= 2:
                inscriptions.append(signs)

    flat = [s for insc in inscriptions for s in insc]
    freq = Counter(flat)

    _print(f"\n  Corpus: {len(inscriptions)} words  {len(flat)} tokens  "
           f"{len(freq)} distinct signs")
    _print(f"  Top 15 signs: {[s for s, _ in freq.most_common(15)]}")

    # All signs that appear in the ground truth
    all_gt_signs = set()
    for row in _TRUE_ROWS:
        all_gt_signs.update(row)
    for col in _TRUE_COLS:
        all_gt_signs.update(col)
    known_in_corpus = all_gt_signs & set(freq.keys())
    _print(f"  GT signs in corpus: {len(known_in_corpus)}/{len(all_gt_signs)}")

    # Classify signs
    sign_class = classify_signs(inscriptions, flat)
    syllabograms = [
        s for s, info in sign_class.items()
        if info["type"] == "syllabogram"
    ]
    _print(f"\n  Sign classification: {len(syllabograms)} syllabograms  "
           f"{sum(1 for i in sign_class.values() if i['type']=='logogram')} logograms")

    # Run affinity analysis (GPU-backed)
    _print("\n  Running GPU-backed Ventris affinity analysis...")
    affinity = compute_affinity(
        inscriptions, syllabograms,
        top_n=40, window=2,
    )

    vowel_groups    = affinity.get("vowel_groups", [])
    consonant_groups = affinity.get("consonant_groups", [])
    _print(f"  Threshold used: {affinity.get('threshold_used', '?')}")
    _print(f"  Acceleration:   {affinity.get('acceleration', '?')}")
    _print(f"  Vowel groups:      {len(vowel_groups)}")
    _print(f"  Consonant groups:  {len(consonant_groups)}")

    # Score against ground truth
    sign_to_row = _sign_to_row()
    sign_to_col = _sign_to_col()

    _print("\n  Scoring vowel (row) groups...")
    row_score = _score_clusters(
        vowel_groups, sign_to_row, "row", verbose=verbose,
    )

    _print("\n  Scoring consonant (column) groups...")
    col_score = _score_clusters(
        consonant_groups, sign_to_col, "col", verbose=verbose,
    )

    # Overall summary
    f1_avg = (row_score["f1"] + col_score["f1"]) / 2
    _print(f"\n  OVERALL F1 (row+col avg): {f1_avg:.3f}")
    _print(f"  Vowel row  F1: {row_score['f1']:.3f}  "
           f"({row_score['true_positives']}/{row_score['true_pairs']} pairs)")
    _print(f"  Consonant  F1: {col_score['f1']:.3f}  "
           f"({col_score['true_positives']}/{col_score['true_pairs']} pairs)")

    # Interpretation
    if f1_avg > 0.5:
        interp = (
            "STRONG: Our method recovers most Ventris grid relationships "
            "from raw distributional statistics alone."
        )
    elif f1_avg > 0.3:
        interp = (
            "MODERATE: Our method recovers a significant fraction of grid "
            "relationships. Results would be useful as a starting grid for "
            "manual refinement by a domain expert."
        )
    elif f1_avg > 0.1:
        interp = (
            "PARTIAL: Our method recovers some correct relationships. "
            "Useful as a filtering tool to reduce the search space."
        )
    else:
        interp = (
            "WEAK: Corpus too small or signs too sparse for reliable affinity "
            "analysis. A larger or more uniform corpus would improve results."
        )
    _print(f"\n  INTERPRETATION: {interp}")

    return {
        "corpus_stats": {
            "n_words": len(inscriptions),
            "n_tokens": len(flat),
            "n_distinct_signs": len(freq),
            "gt_signs_in_corpus": len(known_in_corpus),
        },
        "affinity": {
            "n_vowel_groups":    len(vowel_groups),
            "n_consonant_groups": len(consonant_groups),
            "threshold":         affinity.get("threshold_used"),
            "acceleration":      affinity.get("acceleration"),
        },
        "row_score":    row_score,
        "col_score":    col_score,
        "f1_average":   round(f1_avg, 4),
        "interpretation": interp,
    }


if __name__ == "__main__":
    result = run_ventris_validation(verbose=True)
