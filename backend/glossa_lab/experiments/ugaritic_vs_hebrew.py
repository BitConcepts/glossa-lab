"""Ugaritic decipherment using Old Hebrew as language model.

Implements the standard benchmark protocol from:
  Snyder, Naseem & Barzilay (2010) "A Statistical Model for Lost Language
  Decipherment"  — 28/30 correct sign mappings (93.3%)
  Luo, Cao & Barzilay (2019) "Neural Decipherment via Minimum-Cost Flow"
  — 29/30 correct sign mappings (96.7%)

This is the scientifically valid setup because:
  - Language model: built from Old Hebrew consonant corpus (SEPARATE language)
  - Cipher text:    Ugaritic Baal Cycle (opaque sign IDs)
  - Both languages are Northwest Semitic with known phonological correspondences
  - No overlap between training data and test data

Our result with the same-corpus circular setup was coincidentally 29/30 as well,
but for invalid methodological reasons.  This benchmark provides the honest,
comparable result under the standard field protocol.

Expected result range based on literature:
  State-of-the-art (Luo 2019 neural):  29/30 = 96.7%
  Snyder 2010 Bayesian:                28/30 = 93.3%
  HMM baseline (Knight & Yamada 1999): 23/30 = 76.7%
  Our hill-climbing (this benchmark):  TBD — limited by:
    1. Corpus size (our Hebrew corpus is smaller than Snyder's)
    2. No cognate-level alignment (we match statistics, not words)
    3. No morphological constraints

Usage:
    python -m glossa_lab.experiments.ugaritic_vs_hebrew
"""

from __future__ import annotations

import os
import sys
from typing import Any

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def run_ugaritic_vs_hebrew_benchmark(
    verbose: bool = True,
    max_iterations: int = 15000,
    restarts: int = 10,
    seed: int = 42,
) -> dict[str, Any]:
    """Run the standard cross-language Ugaritic/Hebrew decipherment benchmark.

    Returns dict with accuracy, mapping, comparison to state-of-the-art.
    """
    from corpora.ugaritic import (
        _BAAL_CYCLE_LINES,
        _SIGN_TO_ID,
        get_answer_key,
    )

    from glossa_lab.data.old_hebrew import (
        corpus_statistics as heb_stats,
    )
    from glossa_lab.data.old_hebrew import (
        get_corpus_inscriptions as heb_inscriptions,
    )
    from glossa_lab.data.old_hebrew import (
        get_corpus_symbols as heb_symbols,
    )
    from glossa_lab.data.old_hebrew import (
        get_ugaritic_to_hebrew_map,
    )
    from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy

    def _print(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _print("\n" + "=" * 65)
    _print("  Ugaritic vs Hebrew Benchmark (Snyder 2010 / Luo 2019 protocol)")
    _print("=" * 65)

    # ── Hebrew language model (training data) ────────────────────────
    heb_flat = heb_symbols()
    heb_inscr = heb_inscriptions()
    heb_stat = heb_stats()

    _print(
        f"\n  Hebrew LM corpus:  {heb_stat['total_tokens']} tokens  "
        f"V={heb_stat['distinct_signs']}  "
        f"V/N={heb_stat['type_token_ratio']}"
    )
    _print(
        f"  Hebrew inscriptions: {heb_stat['n_inscriptions']}  "
        f"avg length: {heb_stat['avg_inscription_length']}"
    )

    # ── Ugaritic cipher text (test data) ────────────────────────────
    def _parse_line(line: str) -> list[str]:
        return [ch for ch in line.split() if ch != "."]

    decoded_lines = [_parse_line(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines = [[_SIGN_TO_ID.get(s, s) for s in line] for line in decoded_lines]
    cipher_flat = [s for line in encoded_lines for s in line]
    cipher_inscr = encoded_lines

    _print(
        f"\n  Ugaritic cipher:   {len(cipher_flat)} tokens  "
        f"V={len(set(cipher_flat))}  "
        f"({len(_BAAL_CYCLE_LINES)} lines)"
    )

    # The answer key maps opaque IDs → Ugaritic signs
    # We need to ALSO translate Ugaritic signs → Hebrew signs using known
    # phonological correspondences (this is the 'ground truth')
    ug_to_ug_answer = get_answer_key()  # opaque_id → ugaritic_sign
    ug_to_heb_map = get_ugaritic_to_hebrew_map()  # ugaritic_sign → hebrew_sign

    # Combined ground truth: opaque_id → hebrew_sign
    ground_truth: dict[str, str] = {}
    for opaque_id, ug_sign in ug_to_ug_answer.items():
        heb_sign = ug_to_heb_map.get(ug_sign)
        if heb_sign:
            ground_truth[opaque_id] = heb_sign

    _print(
        f"\n  Ground truth mappings: {len(ground_truth)}/{len(ug_to_ug_answer)} "
        f"Ugaritic signs have Hebrew equivalents"
    )

    # ── Build language model from HEBREW corpus ──────────────────────
    model = LanguageModel(heb_flat, inscriptions=heb_inscr)
    _print(
        f"\n  Language model: {len(model.alphabet)} Hebrew consonant types, "
        f"{len(model.bigram_freq)} bigrams"
    )

    # ── Run decipherment: Ugaritic cipher → Hebrew mapping ───────────
    _print(f"\n  Running decipherment (max_iter={max_iterations}, restarts={restarts})...")
    result = decipher(
        cipher_flat,
        model,
        seed=seed,
        max_iterations=max_iterations,
        restarts=restarts,
        cipher_inscriptions=cipher_inscr,
    )

    # ── Score against Ugaritic→Hebrew ground truth ───────────────────
    acc = score_accuracy(result["proposed_mapping"], ground_truth)

    _print("\n  Results:")
    _print(
        f"    Sign mapping accuracy:  {acc['correct']}/{acc['total']} = "
        f"{acc['accuracy'] * 100:.1f}%"
    )
    _print(f"    Kandles confidence:     {result['kandles_confidence']:.4f}")

    # Compare to literature baselines
    _print("\n  Comparison to published results:")
    _print("    HMM baseline (Knight & Yamada 1999):   23/30 = 76.7%")
    _print("    Snyder et al. 2010 (Bayesian):         28/30 = 93.3%")
    _print("    Luo et al. 2019 (neural MCF):          29/30 = 96.7%")
    _print(
        f"    Our system (hill-climbing bigram):     "
        f"{acc['correct']}/{acc['total']} = {acc['accuracy'] * 100:.1f}%"
    )

    # Report correct and incorrect mappings
    correct_signs = [d for d in acc["details"] if d["correct"]]
    wrong_signs = [d for d in acc["details"] if not d["correct"]]

    _print(f"\n  Correctly mapped ({len(correct_signs)}):")
    for d in correct_signs[:10]:
        ug_sign = ug_to_ug_answer.get(d["sign"], d["sign"])
        _print(f"    {d['sign']} (Ug:{ug_sign:3}) → {d['proposed']:3} ✓")

    if wrong_signs:
        _print(f"\n  Incorrectly mapped ({len(wrong_signs)}):")
        for d in wrong_signs[:10]:
            ug_sign = ug_to_ug_answer.get(d["sign"], d["sign"])
            _print(f"    {d['sign']} (Ug:{ug_sign:3}) → {d['proposed']:3} (expected {d['true']})")

    _print("\n  Limitations of our approach vs Snyder/Luo:")
    _print("    1. Hebrew corpus is much smaller (~700 tokens vs ~20k in Snyder)")
    _print("    2. No cognate alignment — we match phonotactics, not word pairs")
    _print("    3. No morphological constraints (verb/noun structure not modelled)")
    _print("    4. Hill-climbing hill (local optima) vs Bayesian/neural global search")
    _print("    5. No IPA phonological geometry (Luo 2021 improvement)")
    _print("\n  These are precisely the improvements Dr. Fuls' progression will drive.")

    return {
        "protocol": "standard_cross_language (Snyder 2010 / Luo 2019)",
        "cipher_corpus": "Ugaritic Baal Cycle 82 lines / 945 tokens",
        "language_model": f"Old Hebrew consonant corpus {heb_stat['total_tokens']} tokens",
        "accuracy": acc["accuracy"],
        "correct": acc["correct"],
        "total": acc["total"],
        "kandles": result["kandles_confidence"],
        "literature_comparison": {
            "heuristic_hm_1999": {"correct": 23, "total": 30, "accuracy": 0.767},
            "snyder_bayesian_2010": {"correct": 28, "total": 30, "accuracy": 0.933},
            "luo_neural_2019": {"correct": 29, "total": 30, "accuracy": 0.967},
            "our_hillclimb": {
                "correct": acc["correct"],
                "total": acc["total"],
                "accuracy": acc["accuracy"],
            },
        },
        "wrong_mappings": [
            {
                "opaque": d["sign"],
                "ugaritic": ug_to_ug_answer.get(d["sign"], "?"),
                "proposed": d["proposed"],
                "expected": d["true"],
            }
            for d in wrong_signs
        ],
    }


if __name__ == "__main__":
    result = run_ugaritic_vs_hebrew_benchmark(verbose=True)

try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class UgariticVsHebrew(_EB):
    id = "ugaritic_vs_hebrew"
    name = "Ugaritic vs Hebrew (Bigram Hill-Climbing)"
    category = "Validation"
    description = "Hill-climbing bigram baseline: 6.7% vs HMM (77%) and neural (97%)."
    estimated_time = "~30 sec"
    command = "python -m glossa_lab.experiments.ugaritic_vs_hebrew"
    params_schema = {
        "type": "object",
        "properties": {},
        "$comment": "Uses built-in Ugaritic Baal Cycle and Old Hebrew corpus. No user params required.",
    }

    def run(self, **kwargs):
        return run_ugaritic_vs_hebrew_benchmark(verbose=False)
