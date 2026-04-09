"""Tier 3 — Sumerian Logo-Syllabic Self-Decipherment Validation.

SCIENTIFIC CONTEXT (Dr. Fuls validation progression):
  Tier 3 tests whether our beam-search framework can recover sign values
  from a LOGO-SYLLABIC script — the same script type as the Indus Script.
  Sumerian (UR III period, ~2100-2000 BCE) is the ideal Tier 3 test case:
    - Well-documented logo-syllabic script (107 distinct signs)
    - Large public corpus (39,287 tokens, 5,000 inscriptions)
    - Ground truth known (every sign value established)
    - Script type matches Indus (mixed logograms + phonograms)

PROTOCOL (no circularity):
  Train:  first 75% of corpus (3,750 inscriptions, ~29,000 tokens) → LM
  Test:   last 25%  (1,250 inscriptions, ~10,000 tokens) → cipher with opaque IDs
  Score:  fraction of the 107 Sumerian signs correctly recovered

EXPECTATIONS:
  Sumerian has 107 signs vs Hebrew's 22. The search space is much larger.
  Without phonological group constraints (Sumerian→Sumerian correspondences
  are identical, so every sign should map to itself), the beam should achieve
  near-perfect accuracy — this validates that bigram statistics alone can
  recover logo-syllabic sign values within the SAME language.

  This validates the methodology before applying it to UNKNOWN scripts like
  the Indus, where the phonological correspondences are still hypothetical.

Usage:
    python -m glossa_lab.experiments.tier3_sumerian_validation
"""
from __future__ import annotations

import os
import sys
import time
from collections import Counter
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _BACKEND)


def run_tier3_sumerian(verbose: bool = True) -> dict[str, Any]:
    from glossa_lab.data.sumerian_ur3 import (
        get_corpus_symbols as sum_sym,
        get_corpus_inscriptions as sum_ins,
    )
    from glossa_lab.pipelines.decipher   import LanguageModel, decipher, score_accuracy
    from glossa_lab.pipelines.beam_decipher import beam_decipher

    def _pr(*a, **kw):
        if verbose: print(*a, **kw)

    _pr("\n" + "="*70)
    _pr("  Tier 3 — Sumerian UR III Logo-Syllabic Self-Decipherment")
    _pr("="*70)

    flat  = sum_sym()
    inscr = sum_ins()
    freq  = Counter(flat)

    n      = len(inscr)
    split  = int(n * 0.75)
    train_inscr = inscr[:split]
    test_inscr  = inscr[split:]
    train_flat  = [s for i in train_inscr for s in i]
    test_flat   = [s for i in test_inscr  for s in i]

    _pr(f"\n  Full corpus:  {len(flat)} tokens  V={len(freq)} signs  {n} inscriptions")
    _pr(f"  Train: {split} inscriptions  ({len(train_flat)} tokens)")
    _pr(f"  Test:  {n-split} inscriptions  ({len(test_flat)} tokens)")

    # Build LM from train
    lm = LanguageModel(train_flat, inscriptions=train_inscr)
    _pr(f"  LM: {len(lm.alphabet)} sign types  {len(lm.bigram_freq)} bigrams")

    # Encode test with opaque IDs
    test_signs = sorted(set(test_flat))
    sign_to_id = {s: f"S{i:03d}" for i, s in enumerate(test_signs)}
    id_to_sign = {v: k for k, v in sign_to_id.items()}

    encoded_test  = [sign_to_id.get(s, s) for s in test_flat]
    encoded_inscr = [[sign_to_id.get(s, s) for s in ins] for ins in test_inscr]

    # Ground truth: opaque_id → actual Sumerian sign value
    ground_truth = {sign_to_id[s]: s for s in test_signs if s in sign_to_id}
    _pr(f"\n  Test cipher: {len(test_signs)} distinct signs, {len(encoded_test)} tokens")
    _pr(f"  Ground truth mappings: {len(ground_truth)}")

    # ── SA baseline ────────────────────────────────────────────────────────
    _pr("\n  Running SA baseline (seed=42, 5 restarts, surjective=True)...")
    t0 = time.time()
    r_sa = decipher(
        encoded_test, lm, seed=42, max_iterations=10000, restarts=5,
        cipher_inscriptions=encoded_inscr, surjective=True,
    )
    acc_sa = score_accuracy(r_sa["proposed_mapping"], ground_truth)
    _pr(f"  SA surjective:  {acc_sa['correct']}/{acc_sa['total']} = "
        f"{acc_sa['accuracy']*100:.1f}%  [{time.time()-t0:.1f}s]")

    # ── Beam bijective (within-language, same sign inventory) ──────────────
    _pr("\n  Running beam bijective (w=200, within-language)...")
    t0 = time.time()
    r_b1 = beam_decipher(
        encoded_test, lm, beam_width=200,
        cipher_inscriptions=encoded_inscr, surjective=False,
    )
    acc_b1 = score_accuracy(r_b1["proposed_mapping"], ground_truth)
    _pr(f"  Beam bijective w=200:  {acc_b1['correct']}/{acc_b1['total']} = "
        f"{acc_b1['accuracy']*100:.1f}%  [{time.time()-t0:.1f}s]")

    # ── Beam bijective w=500 ──────────────────────────────────────────────
    _pr("\n  Running beam bijective (w=500)...")
    t0 = time.time()
    r_b2 = beam_decipher(
        encoded_test, lm, beam_width=500,
        cipher_inscriptions=encoded_inscr, surjective=False,
    )
    acc_b2 = score_accuracy(r_b2["proposed_mapping"], ground_truth)
    _pr(f"  Beam bijective w=500:  {acc_b2['correct']}/{acc_b2['total']} = "
        f"{acc_b2['accuracy']*100:.1f}%  [{time.time()-t0:.1f}s]")

    # ── Beam w=1000 ───────────────────────────────────────────────────────
    _pr("\n  Running beam bijective (w=1000)...")
    t0 = time.time()
    r_b3 = beam_decipher(
        encoded_test, lm, beam_width=1000,
        cipher_inscriptions=encoded_inscr, surjective=False,
    )
    acc_b3 = score_accuracy(r_b3["proposed_mapping"], ground_truth)
    _pr(f"  Beam bijective w=1000: {acc_b3['correct']}/{acc_b3['total']} = "
        f"{acc_b3['accuracy']*100:.1f}%  [{time.time()-t0:.1f}s]")

    best = max(acc_b1["correct"], acc_b2["correct"], acc_b3["correct"], acc_sa["correct"])
    best_pct = best / acc_b1["total"] * 100

    # Show first 15 correct and wrong
    correct_maps = [d for d in acc_b3["details"] if d["correct"]][:12]
    wrong_maps   = [d for d in acc_b3["details"] if not d["correct"]][:8]

    _pr("\n  Correct mappings (sample):")
    for d in correct_maps:
        _pr(f"    {d['sign']:8} -> {d['proposed']:12} correct={d['true']} OK")
    if wrong_maps:
        _pr("\n  Wrong mappings (sample):")
        for d in wrong_maps:
            _pr(f"    {d['sign']:8} -> {d['proposed']:12} expected {d['true']}")

    if best_pct >= 70:
        interp = (
            f"STRONG ({best}/{acc_b1['total']} = {best_pct:.1f}%) — "
            "Beam search recovers the majority of Sumerian signs from within-corpus "
            "bigram statistics alone. This validates the framework on a logo-syllabic "
            "script before application to the Indus corpus."
        )
    elif best_pct >= 40:
        interp = (
            f"MODERATE ({best}/{acc_b1['total']} = {best_pct:.1f}%) — "
            "Beam recovers a significant fraction of Sumerian signs. "
            "Sumerian has 107 signs (much larger alphabet than Ugaritic/Hebrew); "
            "the larger search space reduces accuracy compared to Tier 1a."
        )
    else:
        interp = (
            f"PARTIAL ({best}/{acc_b1['total']} = {best_pct:.1f}%) — "
            "The logo-syllabic nature of Sumerian (mixed logograms + syllabograms) "
            "makes self-decipherment harder than pure abjad/syllabary scripts. "
            "Sign classification (to separate logograms from phonograms) is needed "
            "before phonological group constraints can be applied."
        )

    _pr(f"\n  TIER 3 SUMMARY:")
    _pr(f"    SA surjective:          {acc_sa['correct']}/{acc_sa['total']} = {acc_sa['accuracy']*100:.1f}%")
    _pr(f"    Beam bijective w=200:   {acc_b1['correct']}/{acc_b1['total']} = {acc_b1['accuracy']*100:.1f}%")
    _pr(f"    Beam bijective w=500:   {acc_b2['correct']}/{acc_b2['total']} = {acc_b2['accuracy']*100:.1f}%")
    _pr(f"    Beam bijective w=1000:  {acc_b3['correct']}/{acc_b3['total']} = {acc_b3['accuracy']*100:.1f}%")
    _pr(f"\n  INTERPRETATION: {interp}")
    _pr("\n  Note: Sumerian (107 signs) has a much larger alphabet than Ugaritic (30).")
    _pr("  Without phonological group constraints, the beam must search 107!")
    _pr("  Adding sign-function classification (logogram vs phonogram) would")
    _pr("  reduce the effective search space and improve accuracy significantly.")

    return {
        "tier": "3",
        "system": "Sumerian UR III (logo-syllabic, 107 signs)",
        "train": {"inscriptions": split,   "tokens": len(train_flat)},
        "test":  {"inscriptions": n-split, "tokens": len(test_flat),
                  "signs": len(test_signs)},
        "results": {
            "sa_surjective":    {"correct": acc_sa["correct"],  "total": acc_sa["total"],  "accuracy": acc_sa["accuracy"]},
            "beam_bij_200":     {"correct": acc_b1["correct"],  "total": acc_b1["total"],  "accuracy": acc_b1["accuracy"]},
            "beam_bij_500":     {"correct": acc_b2["correct"],  "total": acc_b2["total"],  "accuracy": acc_b2["accuracy"]},
            "beam_bij_1000":    {"correct": acc_b3["correct"],  "total": acc_b3["total"],  "accuracy": acc_b3["accuracy"]},
        },
        "best_accuracy": round(best_pct / 100, 3),
        "interpretation": interp,
    }


if __name__ == "__main__":
    run_tier3_sumerian(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class Tier3SumerianValidation(_EB):
    id = "tier3_sumerian_validation"
    name = "Tier 3 — Sumerian Logo-Syllabic Self-Validation"
    category = "Validation"
    description = (
        "Tier 3 (Dr. Fuls progression): Sumerian UR III logo-syllabic script. "
        "75/25 train/test self-decipherment — validates beam framework on a "
        "mixed logogram+syllabogram script before Indus application. "
        "107 distinct signs, 39k tokens, 5k inscriptions."
    )
    estimated_time = "~3 min"
    command = "python -m glossa_lab.experiments.tier3_sumerian_validation"
    params_schema = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return run_tier3_sumerian(verbose=False)
