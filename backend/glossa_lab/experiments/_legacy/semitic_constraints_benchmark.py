"""Semitic structural constraints benchmark — Tier 1a cross-language.

Tests whether adding structural linguistic constraints improves the
score landscape and decipherment accuracy on the Ugaritic→Hebrew task.

Four constraint levels are compared:

  Level 0 — Baseline
    Flat bigrams across the full sign stream (current default).
    No word boundaries, no OCP, default positional weight.

  Level 1 — + OCP penalty
    Penalise mappings that produce repeated consecutive consonants
    within words (OCP: Obligatory Contour Principle, Semitic phonology).
    Uses actual Ugaritic word-level parsing (dot separators).
    ocp_weight=1.0

  Level 2 — + Word-boundary bigrams
    Score bigrams only within words, not across them.
    Uses: Ugaritic word-level cipher inscriptions + Hebrew word-level LM
    (approximated by splitting verses into 4-sign chunks).
    use_word_bigrams=True

  Level 3 — All constraints combined
    Word-boundary bigrams + OCP + strong positional weight.

For each level, the experiment also runs the ORACLE analysis (score of
correct mapping vs SA-found) to measure how much the landscape sharpens.

Usage:
    python -m glossa_lab.experiments.semitic_constraints_benchmark
"""
from __future__ import annotations

import os
import sys
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ── Data loading ──────────────────────────────────────────────────────

def _load() -> dict[str, Any]:
    from corpora.ugaritic import (
        _BAAL_CYCLE_LINES,
        _SIGN_TO_ID,
        get_answer_key,
        get_word_level_inscriptions,
    )

    from glossa_lab.data.old_hebrew import (
        get_corpus_inscriptions as heb_line_inscr,
    )
    from glossa_lab.data.old_hebrew import (
        get_corpus_symbols as heb_syms,
    )
    from glossa_lab.data.old_hebrew import (
        get_ugaritic_to_hebrew_map,
    )
    from glossa_lab.data.old_hebrew import (
        get_word_inscriptions as heb_word_inscr,
    )
    from glossa_lab.pipelines.decipher import (
        LanguageModel,
        _score_mapping,
        decipher,
        score_accuracy,
    )

    # ── Ugaritic cipher (LINE-level) ──────────────────────────────
    def _parse_line(line: str) -> list[str]:
        return [ch for ch in line.split() if ch != "."]

    decoded_lines  = [_parse_line(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines  = [[_SIGN_TO_ID.get(s, s) for s in line] for line in decoded_lines]
    cipher_flat    = [s for line in encoded_lines for s in line]

    # ── Ugaritic cipher (WORD-level) ──────────────────────────────
    ug_words_decoded = get_word_level_inscriptions(encoded=False)
    ug_words_encoded = get_word_level_inscriptions(encoded=True)

    # ── Ground truth ──────────────────────────────────────────────
    ug_to_ug     = get_answer_key()
    ug_to_heb    = get_ugaritic_to_hebrew_map()
    ground_truth = {
        oid: ug_to_heb[us]
        for oid, us in ug_to_ug.items()
        if us in ug_to_heb
    }

    # ── Hebrew language models ────────────────────────────────────
    heb_flat = heb_syms()

    # Line-level LM (current default)
    lm_line = LanguageModel(heb_flat, inscriptions=heb_line_inscr())

    # Word-level LM (4-sign chunks approximating Hebrew word boundaries)
    lm_word = LanguageModel(heb_flat, inscriptions=heb_word_inscr())

    return {
        "cipher_flat":      cipher_flat,
        "cipher_line_inscr": encoded_lines,
        "cipher_word_inscr": ug_words_encoded,
        "ug_decoded_words":  ug_words_decoded,
        "ground_truth":      ground_truth,
        "ug_to_ug":          ug_to_ug,
        "lm_line":           lm_line,
        "lm_word":           lm_word,
        "decipher":          decipher,
        "score_accuracy":    score_accuracy,
        "_score_mapping":    _score_mapping,
    }


# ── Oracle: score correct mapping vs SA mapping ───────────────────────

def _oracle(d: dict, lm, cipher_inscr, use_word_bigrams: bool,
            ocp_weight: float, positional_weight: float) -> dict[str, Any]:
    """Run SA once + compare score of correct vs found mapping."""
    from collections import defaultdict

    _score_mapping = d["_score_mapping"]
    score_accuracy = d["score_accuracy"]
    cipher_flat    = d["cipher_flat"]
    ground_truth   = d["ground_truth"]

    # Build positional dict
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
        cipher_flat, ground_truth, lm, cipher_pos,
        use_word_bigrams=use_word_bigrams,
        cipher_inscriptions=cipher_inscr,
        ocp_weight=ocp_weight,
        positional_weight=positional_weight,
    )

    sa_result = d["decipher"](
        cipher_flat, lm,
        seed=42, max_iterations=15000, restarts=10,
        cipher_inscriptions=cipher_inscr,
        use_word_bigrams=use_word_bigrams,
        ocp_weight=ocp_weight,
        positional_weight=positional_weight,
    )
    sa_map = sa_result["proposed_mapping"]
    score_sa = _score_mapping(
        cipher_flat, sa_map, lm, cipher_pos,
        use_word_bigrams=use_word_bigrams,
        cipher_inscriptions=cipher_inscr,
        ocp_weight=ocp_weight,
        positional_weight=positional_weight,
    )
    acc_sa = score_accuracy(sa_map, ground_truth)

    delta = score_correct - score_sa
    return {
        "score_correct": round(score_correct, 1),
        "score_sa":      round(score_sa, 1),
        "delta":         round(delta, 1),
        "correct":       acc_sa["correct"],
    }


# ── Main benchmark ────────────────────────────────────────────────────

def run_semitic_constraints_benchmark(verbose: bool = True) -> dict[str, Any]:
    def _print(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _print("\n" + "=" * 70)
    _print("  Semitic Structural Constraints Benchmark (Tier 1a cross-language)")
    _print("=" * 70)

    d = _load()

    lm_line = d["lm_line"]
    lm_word = d["lm_word"]

    _print(f"\n  Hebrew LM (line-level): {len(lm_line.alphabet)} signs  "
           f"{len(lm_line.bigram_freq)} flat bigrams  "
           f"{len(lm_line.word_bigram_freq)} word-boundary bigrams (line-level proxy)")
    _print(f"  Hebrew LM (word-level): {len(lm_word.alphabet)} signs  "
           f"{len(lm_word.bigram_freq)} flat bigrams  "
           f"{len(lm_word.word_bigram_freq)} word-boundary bigrams  "
           f"OCP rate={lm_word.ocp_rate:.4f}")

    ug_word_count = len(d["cipher_word_inscr"])
    ug_avg_wlen = sum(len(w) for w in d["cipher_word_inscr"]) / ug_word_count
    _print(f"  Ugaritic words:          {ug_word_count} words  "
           f"avg length {ug_avg_wlen:.1f} signs/word")
    _print(f"  Ground truth: {len(d['ground_truth'])}/30 Ugaritic→Hebrew mappings")

    configs = [
        {
            "name":              "Level 0 — Baseline (flat bigrams)",
            "lm":                lm_line,
            "cipher_inscr":      d["cipher_line_inscr"],
            "use_word_bigrams":  False,
            "ocp_weight":        0.0,
            "positional_weight": 0.005,
        },
        {
            "name":              "Level 1 — + OCP penalty (word-level Ugaritic)",
            "lm":                lm_line,
            "cipher_inscr":      d["cipher_word_inscr"],
            "use_word_bigrams":  False,
            "ocp_weight":        1.0,
            "positional_weight": 0.005,
        },
        {
            "name":              "Level 2 — + Word-boundary bigrams",
            "lm":                lm_word,
            "cipher_inscr":      d["cipher_word_inscr"],
            "use_word_bigrams":  True,
            "ocp_weight":        0.0,
            "positional_weight": 0.005,
        },
        {
            "name":              "Level 3 — All constraints (word-bigrams + OCP + pos)",
            "lm":                lm_word,
            "cipher_inscr":      d["cipher_word_inscr"],
            "use_word_bigrams":  True,
            "ocp_weight":        1.0,
            "positional_weight": 0.02,
        },
    ]

    results = []
    for cfg in configs:
        _print(f"\n  {cfg['name']}")
        _print("  " + "-" * 60)
        r = _oracle(
            d,
            lm=cfg["lm"],
            cipher_inscr=cfg["cipher_inscr"],
            use_word_bigrams=cfg["use_word_bigrams"],
            ocp_weight=cfg["ocp_weight"],
            positional_weight=cfg["positional_weight"],
        )
        _print(f"    Accuracy (SA, seed=42):      {r['correct']:2d}/30 = {r['correct']/30*100:.1f}%")
        _print(f"    score(correct mapping):      {r['score_correct']:>10.1f}")
        _print(f"    score(SA-found mapping):     {r['score_sa']:>10.1f}")
        sign = "+" if r["delta"] >= 0 else ""
        pct  = r["delta"] / abs(r["score_sa"]) * 100 if r["score_sa"] else 0
        _print(f"    delta (correct - SA):        {sign}{r['delta']:.1f}  ({sign}{pct:.2f}%)")

        landscape_quality = "SHARP" if r["delta"] > abs(r["score_sa"]) * 0.02 else (
            "MODERATE" if r["delta"] > 0 else "FLAT/INVERTED"
        )
        _print(f"    Landscape:  {landscape_quality}")
        results.append({
            "level":             cfg["name"],
            "accuracy":          r["correct"],
            "score_correct":     r["score_correct"],
            "score_sa":          r["score_sa"],
            "delta":             r["delta"],
            "use_word_bigrams":  cfg["use_word_bigrams"],
            "ocp_weight":        cfg["ocp_weight"],
            "positional_weight": cfg["positional_weight"],
        })

    _print("\n" + "=" * 70)
    _print("  CONSTRAINT SUMMARY")
    _print("=" * 70)
    _print(f"\n  {'Level':<48} {'Accuracy':>8}  {'Delta score':>12}  Landscape")
    _print("  " + "-" * 68)
    for r in results:
        level_short = r["level"].split("—")[0].strip()
        ls = "SHARP" if r["delta"] > abs(r["score_sa"]) * 0.02 else (
             "MODERATE" if r["delta"] > 0 else "FLAT/INV")
        _print(f"  {level_short:<48} {r['accuracy']:2d}/30 = {r['accuracy']/30*100:4.1f}%  "
               f"  {r['delta']:>+8.0f}    {ls}")

    best = max(results, key=lambda x: x["accuracy"])
    sharpest = max(results, key=lambda x: x["delta"])
    _print(f"\n  Best accuracy:    {best['level'].split('—')[0].strip()}"
           f"  → {best['accuracy']}/30 = {best['accuracy']/30*100:.1f}%")
    _print(f"  Sharpest landscape: {sharpest['level'].split('—')[0].strip()}"
           f"  → delta = {sharpest['delta']:+.0f}")

    # How much does the best constraint level improve over baseline?
    baseline_correct = results[0]["accuracy"]
    best_correct     = best["accuracy"]
    improvement      = best_correct - baseline_correct

    _print(f"\n  Overall improvement over baseline: {improvement:+d} correct signs")

    if improvement >= 5:
        conclusion = (
            "SIGNIFICANT — Structural constraints improve Tier 1a accuracy noticeably. "
            "The constraints sharpen the score landscape enough for SA to find better solutions."
        )
    elif improvement >= 1:
        conclusion = (
            "MODEST — Constraints provide small accuracy improvements. "
            "The landscape is sharper but SA still struggles with cross-language transfer."
        )
    elif sharpest["delta"] > results[0]["delta"]:
        conclusion = (
            "LANDSCAPE IMPROVEMENT — Delta increased but accuracy didn't follow. "
            "The model has sharper signal; more restarts or better SA tuning might exploit it."
        )
    else:
        conclusion = (
            "MINIMAL — Structural constraints alone are insufficient for cross-language "
            "improvement at this corpus scale. Morphological alignment is still required."
        )

    _print(f"\n  CONCLUSION: {conclusion}")

    return {
        "results":       results,
        "best_level":    best["level"],
        "best_accuracy": best["accuracy"],
        "baseline_accuracy": baseline_correct,
        "improvement": improvement,
        "conclusion":  conclusion,
    }


if __name__ == "__main__":
    run_semitic_constraints_benchmark(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class SemiticConstraintsBenchmark(_EB):
    id = "semitic_constraints_benchmark"
    name = "Semitic Structural Constraints Benchmark"
    category = "Validation"
    description = (
        "Tests four constraint levels on Tier 1a cross-language decipherment: "
        "baseline flat bigrams, + OCP penalty (Obligatory Contour Principle), "
        "+ word-boundary bigrams, and all combined. "
        "Measures both accuracy and score landscape sharpening (oracle delta). "
        "Identifies whether structural constraints close the gap to Snyder (2010)."
    )
    estimated_time = "~5 min"
    command = "python -m glossa_lab.experiments.semitic_constraints_benchmark"
    params_schema = {
        "type": "object",
        "properties": {
            "ocp_weight": {
                "type": "number",
                "title": "OCP Weight",
                "default": 1.0,
                "minimum": 0.0,
                "description": (
                    "Penalty weight for OCP violations (repeated consonants within words). "
                    "0 = disabled. Typical range: 0.5–2.0."
                ),
            },
            "positional_weight": {
                "type": "number",
                "title": "Positional Weight",
                "default": 0.005,
                "minimum": 0.0,
                "description": (
                    "Weight for word-initial/final positional profile matching bonus. "
                    "Default 0.005. Higher values (0.02–0.1) strengthen the constraint."
                ),
            },
        },
    }

    def run(self, **kwargs) -> dict:
        return run_semitic_constraints_benchmark(verbose=False)
