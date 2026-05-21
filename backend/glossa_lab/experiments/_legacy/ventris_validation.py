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

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Ground truth Linear B grid ────────────────────────────────────────

# ROW = same vowel (same ending)
_TRUE_ROWS: list[list[str]] = [
    ["a", "da", "ja", "ka", "ma", "na", "pa", "ra", "sa", "ta", "wa", "za"],
    ["e", "de", "ke", "me", "ne", "pe", "re", "se", "te", "we", "ze"],
    ["i", "di", "ki", "mi", "ni", "pi", "ri", "si", "ti", "wi"],
    ["o", "do", "jo", "ko", "mo", "no", "po", "ro", "so", "to", "wo", "zo"],
    ["u", "du", "ku", "mu", "nu", "pu", "ru", "su", "tu"],
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
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    if verbose:
        print(
            f"  [{label}] pairs TP={tp} FP={fp} FN={fn}  "
            f"P={precision:.3f} R={recall:.3f} F1={f1:.3f}"
        )

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
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "true_pairs": len(gt_same),
        "pred_pairs": len(pred_pairs),
        "true_positives": tp,
    }


# ── Main validation ───────────────────────────────────────────────────


def _run_affinity_at_fraction(
    inscriptions: list[list[str]],
    fraction: float,
    verbose: bool = True,
) -> dict[str, Any]:
    """Run affinity analysis on a fraction of the corpus and score against ground truth."""
    from collections import Counter

    from glossa_lab.pipelines.logosyllabic import classify_signs, compute_affinity

    n = max(10, int(len(inscriptions) * fraction))
    subset = inscriptions[:n]
    flat = [s for insc in subset for s in insc]
    freq = Counter(flat)

    sign_class = classify_signs(subset, flat)
    syllabograms = [s for s, info in sign_class.items() if info["type"] == "syllabogram"]
    if len(syllabograms) < 5:
        return {"n_inscriptions": n, "n_tokens": len(flat), "fraction": fraction,
                "error": "Too few syllabograms in subset", "f1_average": 0.0}

    affinity = compute_affinity(subset, syllabograms, top_n=40, window=2)
    vowel_groups = affinity.get("vowel_groups", [])
    consonant_groups = affinity.get("consonant_groups", [])

    row_score = _score_clusters(vowel_groups, _sign_to_row(), "row", verbose=False)
    col_score = _score_clusters(consonant_groups, _sign_to_col(), "col", verbose=False)
    f1_avg = (row_score["f1"] + col_score["f1"]) / 2

    return {
        "fraction": fraction,
        "n_inscriptions": n,
        "n_tokens": len(flat),
        "n_distinct_signs": len(freq),
        "n_syllabograms": len(syllabograms),
        "row_f1": round(row_score["f1"], 4),
        "col_f1": round(col_score["f1"], 4),
        "f1_average": round(f1_avg, 4),
        "row_precision": round(row_score["precision"], 4),
        "row_recall": round(row_score["recall"], 4),
        "col_precision": round(col_score["precision"], 4),
        "col_recall": round(col_score["recall"], 4),
    }


def run_ventris_validation(verbose: bool = True) -> dict[str, Any]:
    """Load Linear B corpus, run affinity analysis, score against ground truth.

    Runs at three data fractions (100%, 75%, 50%) to show how F1 scales
    with corpus size — directly answers Dr. Fuls' question about data requirements.
    """
    from glossa_lab.accelerate import gpu_info  # noqa: I001
    from glossa_lab.pipelines.logosyllabic import classify_signs, compute_affinity
    from pathlib import Path

    def _print(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _print("\n" + "=" * 70)
    _print("  Ventris Grid Validation — Linear B")
    _print("=" * 70)

    accel = gpu_info()
    _print(
        f"  Acceleration: {accel['tier_name']}  ({accel['cpu_cores']} cores"
        + (f"  GPU: {accel.get('gpu_name', '')}" if accel["cuda"] else "")
        + ")"
    )

    # Load Linear B word-level corpus
    fixture = Path(_BACKEND) / "tests" / "corpora" / "fixtures" / "linear_b.txt"
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

    _print(f"\n  Corpus: {len(inscriptions)} words  {len(flat)} tokens  {len(freq)} distinct signs")
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
    syllabograms = [s for s, info in sign_class.items() if info["type"] == "syllabogram"]
    _print(
        f"\n  Sign classification: {len(syllabograms)} syllabograms  "
        f"{sum(1 for i in sign_class.values() if i['type'] == 'logogram')} logograms"
    )

    # Run affinity analysis (GPU-backed)
    _print("\n  Running GPU-backed Ventris affinity analysis...")
    affinity = compute_affinity(
        inscriptions,
        syllabograms,
        top_n=40,
        window=2,
    )

    vowel_groups = affinity.get("vowel_groups", [])
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
        vowel_groups,
        sign_to_row,
        "row",
        verbose=verbose,
    )

    _print("\n  Scoring consonant (column) groups...")
    col_score = _score_clusters(
        consonant_groups,
        sign_to_col,
        "col",
        verbose=verbose,
    )

    # ── Corpus-size scaling (Tier 4 addition for Dr. Fuls) ───────────
    _print("\n  Corpus-size scaling analysis:")
    _print("  (How well does the Ventris grid recover with limited data?)")
    scaling_results: list[dict] = []
    for frac in (1.0, 0.75, 0.5):
        sr = _run_affinity_at_fraction(inscriptions, frac, verbose=False)
        scaling_results.append(sr)
        if "error" not in sr:
            _print(
                f"    {int(frac * 100):3}% ({sr['n_inscriptions']:4} words, {sr['n_tokens']:5} tokens): "
                f"F1={sr['f1_average']:.3f}  "
                f"row={sr['row_f1']:.3f}  col={sr['col_f1']:.3f}"
            )
        else:
            _print(f"    {int(frac * 100):3}%: {sr['error']}")

    # Overall summary
    f1_avg = (row_score["f1"] + col_score["f1"]) / 2
    _print(f"\n  OVERALL F1 (row+col avg): {f1_avg:.3f}")
    _print(
        f"  Vowel row  F1: {row_score['f1']:.3f}  "
        f"({row_score['true_positives']}/{row_score['true_pairs']} pairs)"
    )
    _print(
        f"  Consonant  F1: {col_score['f1']:.3f}  "
        f"({col_score['true_positives']}/{col_score['true_pairs']} pairs)"
    )
    _print()
    _print("  TIER 4 (Linear B / Ventris) summary for Dr. Fuls:")
    _print(f"    Full corpus → F1={f1_avg:.3f}")
    for sr in scaling_results[1:]:
        if "error" not in sr:
            _print(f"    {int(sr['fraction'] * 100)}% corpus → F1={sr['f1_average']:.3f}")
    _print("  This demonstrates the data requirements before applying to Indus.")

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
        "tier": "4",
        "system": "Mycenaean Linear B (syllabary, 87 signs)",
        "protocol": "Unsupervised affinity clustering vs known Ventris CV grid",
        "corpus_stats": {
            "n_words": len(inscriptions),
            "n_tokens": len(flat),
            "n_distinct_signs": len(freq),
            "gt_signs_in_corpus": len(known_in_corpus),
        },
        "affinity": {
            "n_vowel_groups": len(vowel_groups),
            "n_consonant_groups": len(consonant_groups),
            "threshold": affinity.get("threshold_used"),
            "acceleration": affinity.get("acceleration"),
        },
        "row_score": row_score,
        "col_score": col_score,
        "f1_average": round(f1_avg, 4),
        "corpus_scaling": scaling_results,
        "interpretation": interp,
        "fuls_notes": (
            "Tier 4 validation: affinity analysis on syllabary. "
            "F1 measures fraction of Ventris vowel/consonant pairs recovered. "
            "Corpus-size scaling shows data requirements before Indus application."
        ),
    }


if __name__ == "__main__":
    result = run_ventris_validation(verbose=True)

try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class VentrisValidation(_EB):
    id = "ventris_validation"
    name = "Ventris Grid Validation (Linear B, Tier 4)"
    category = "Validation"
    description = (
        "Tier 4 (Dr. Fuls progression): Linear B syllabary (87 signs) — "
        "automatic recovery of Ventris vowel/consonant grid via affinity clustering. "
        "F1 scored against the known ground-truth grid. "
        "Also shows how F1 scales at 100%/75%/50% corpus to answer: "
        "how much data is needed before applying to Indus?"
    )
    estimated_time = "~15 sec"
    command = "python -m glossa_lab.experiments.ventris_validation"
    results_file = "reports/ventris_validation.json"
    params_schema = {
        "type": "object",
        "properties": {},
        "$comment": "Uses the built-in Linear B corpus. Fully automated validation against known Ventris CV grid.",
    }

    def run(self, **kwargs):
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415
        result = run_ventris_validation(verbose=False)
        out = (
            Path(__file__).resolve().parent.parent.parent.parent
            / "reports" / "ventris_validation.json"
        )
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result
