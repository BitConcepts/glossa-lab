"""Ugaritic proper benchmark: honest train/test separated decipherment.

Addresses the train/test circularity raised by Dr. Andreas Fuls.

CIRCULAR (what we originally did implicitly):
  - Language model: built from same 82-line Baal Cycle corpus
  - Cipher text: same 82-line corpus (encoded with opaque IDs)
  → The algorithm is effectively matching a text against itself.
    Any high accuracy here is an artefact of circularity.

PROPER (what this benchmark does):
  - Split: lines 0-60 → TRAIN (language model), lines 61-81 → TEST (cipher)
  - Language model: trained on decoded Baal Cycle lines 0-60 ONLY
  - Cipher: encoded Baal Cycle lines 61-81 with opaque IDs
  → The algorithm must generalise from training phonotactics to unseen text.

RESULTS format:
  - circular_accuracy:  accuracy when train==test (the problematic approach)
  - proper_accuracy:    accuracy with 75/25 train/test split
  - delta:              proper - circular (how much does circularity inflate results)

Usage:
    python -m glossa_lab.experiments.ugaritic_proper_benchmark
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


def run_ugaritic_benchmark(verbose: bool = True) -> dict[str, Any]:
    """Run both circular and proper (train/test separated) Ugaritic benchmarks.

    Returns:
        dict with circular_result, proper_result, corpus_stats, commentary.
    """
    from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy  # noqa: I001
    from corpora.ugaritic import (
        _BAAL_CYCLE_LINES,
        _SIGN_TO_ID,
        UGARITIC_SIGNS,
        get_answer_key,
    )

    def _print(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    # ── Parse lines into sign sequences ──────────────────────────────
    def _parse_line(line: str) -> list[str]:
        return [ch for ch in line.split() if ch != "."]

    decoded_lines = [_parse_line(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines = [
        [_SIGN_TO_ID.get(s, s) for s in line]
        for line in decoded_lines
    ]
    answer_key = get_answer_key()  # opaque_id → real_sign

    n_lines = len(decoded_lines)
    split_idx = int(n_lines * 0.75)  # 75% train, 25% test

    _print("\n" + "="*65)
    _print("  Ugaritic Benchmark: Circular vs Proper Train/Test Split")
    _print("="*65)
    _print(f"  Total lines:   {n_lines}")
    _print(f"  Train lines:   {split_idx}  (decoded — used for language model only)")
    _print(f"  Test  lines:   {n_lines - split_idx}  (encoded — presented as cipher)")
    _print()

    # ── Corpus statistics ─────────────────────────────────────────────
    flat_all = [s for line in decoded_lines for s in line]
    freq_all = Counter(flat_all)
    corpus_stats = {
        "total_lines": n_lines,
        "total_tokens": len(flat_all),
        "distinct_signs": len(freq_all),
        "theoretical_inventory": len(UGARITIC_SIGNS),
        "type_token_ratio": round(len(freq_all) / len(flat_all), 4),
        "hapax_count": sum(1 for v in freq_all.values() if v == 1),
        "avg_tokens_per_sign": round(len(flat_all) / len(freq_all), 1),
        "most_frequent": freq_all.most_common(5),
    }
    _print("  Corpus statistics:")
    _print(f"    N={corpus_stats['total_tokens']}  V={corpus_stats['distinct_signs']}  "
           f"V/N={corpus_stats['type_token_ratio']}  "
           f"hapax={corpus_stats['hapax_count']}")

    # ── EXPERIMENT A: Circular (train == test) ────────────────────────
    _print("\n  [A] CIRCULAR benchmark (train == test — the problematic approach):")
    circ_train_flat = flat_all
    circ_test_encoded = [s for line in encoded_lines for s in line]
    circ_test_inscr = encoded_lines

    model_circ = LanguageModel(circ_train_flat, inscriptions=decoded_lines)
    result_circ = decipher(
        circ_test_encoded, model_circ,
        seed=42, max_iterations=5000, restarts=3,
        cipher_inscriptions=circ_test_inscr,
    )
    acc_circ = score_accuracy(result_circ["proposed_mapping"], answer_key)
    _print(f"    Accuracy: {acc_circ['correct']}/{acc_circ['total']} = "
           f"{acc_circ['accuracy']*100:.1f}%")
    _print(f"    Kandles confidence: {result_circ['kandles_confidence']:.4f}")
    _print("    NOTE: This inflates accuracy — the LM and cipher use the same text.")

    # ── EXPERIMENT B: Proper train/test split ─────────────────────────
    _print("\n  [B] PROPER benchmark (75% train, 25% test — no data leakage):")
    train_decoded = [s for line in decoded_lines[:split_idx] for s in line]
    train_inscr   = decoded_lines[:split_idx]
    test_encoded  = [s for line in encoded_lines[split_idx:] for s in line]
    test_inscr    = encoded_lines[split_idx:]

    model_proper = LanguageModel(train_decoded, inscriptions=train_inscr)
    result_proper = decipher(
        test_encoded, model_proper,
        seed=42, max_iterations=5000, restarts=3,
        cipher_inscriptions=test_inscr,
    )
    acc_proper = score_accuracy(result_proper["proposed_mapping"], answer_key)
    _print(f"    Accuracy: {acc_proper['correct']}/{acc_proper['total']} = "
           f"{acc_proper['accuracy']*100:.1f}%")
    _print(f"    Kandles confidence: {result_proper['kandles_confidence']:.4f}")
    _print("    NOTE: This is the scientifically valid measurement.")

    # ── EXPERIMENT C: Cross-text (train on KTU 1.1-1.3, test on 1.4-1.6) ─
    # Approximate section split: first ~30 lines = KTU 1.1-1.2, next ~20 = 1.3-1.4
    ktu_split = 49  # approximate KTU 1.1-1.3 boundary
    _print("\n  [C] CROSS-SECTION benchmark (KTU 1.1\u20131.3 train, 1.4\u20131.6 test):")
    _print(f"    Train: lines 0-{ktu_split-1}  Test: lines {ktu_split}-{n_lines-1}")
    train_ktu_flat = [s for line in decoded_lines[:ktu_split] for s in line]
    train_ktu_inscr = decoded_lines[:ktu_split]
    test_ktu_encoded = [s for line in encoded_lines[ktu_split:] for s in line]
    test_ktu_inscr = encoded_lines[ktu_split:]

    model_ktu = LanguageModel(train_ktu_flat, inscriptions=train_ktu_inscr)
    result_ktu = decipher(
        test_ktu_encoded, model_ktu,
        seed=42, max_iterations=5000, restarts=3,
        cipher_inscriptions=test_ktu_inscr,
    )
    acc_ktu = score_accuracy(result_ktu["proposed_mapping"], answer_key)
    _print(f"    Accuracy: {acc_ktu['correct']}/{acc_ktu['total']} = "
           f"{acc_ktu['accuracy']*100:.1f}%")
    _print(f"    Kandles confidence: {result_ktu['kandles_confidence']:.4f}")

    # ── Summary ───────────────────────────────────────────────────────
    _print("\n  Summary:")
    _print(f"    Circular (train=test):      {acc_circ['accuracy']*100:.1f}%")
    _print(f"    Proper (75/25 split):       {acc_proper['accuracy']*100:.1f}%")
    _print(f"    Cross-section (KTU split):  {acc_ktu['accuracy']*100:.1f}%")
    delta = acc_circ['accuracy'] - acc_proper['accuracy']
    _print(f"    Circularity inflation:      +{delta*100:.1f} percentage points")
    _print()
    _print("  IMPORTANT: The 'proper' and 'cross-section' figures are the only")
    _print("  scientifically valid accuracy claims for submission to Dr. Fuls.")
    _print("  Future work: train on non-Baal Cycle Ugaritic texts (letters,")
    _print("  administrative documents) and test on literary texts.")

    return {
        "corpus_stats": corpus_stats,
        "circular_result": {
            "accuracy": acc_circ["accuracy"],
            "correct": acc_circ["correct"],
            "total": acc_circ["total"],
            "kandles": result_circ["kandles_confidence"],
            "note": "INVALID — train==test corpus",
        },
        "proper_result": {
            "accuracy": acc_proper["accuracy"],
            "correct": acc_proper["correct"],
            "total": acc_proper["total"],
            "kandles": result_proper["kandles_confidence"],
            "note": "VALID — 75/25 train/test split",
        },
        "cross_section_result": {
            "accuracy": acc_ktu["accuracy"],
            "correct": acc_ktu["correct"],
            "total": acc_ktu["total"],
            "kandles": result_ktu["kandles_confidence"],
            "note": "VALID — KTU 1.1-1.3 train, KTU 1.4-1.6 test",
        },
        "circularity_inflation_pp": round(delta * 100, 1),
    }


if __name__ == "__main__":
    result = run_ugaritic_benchmark(verbose=True)
