"""Sequence-Level Evaluation Benchmark.

Evaluates the decipherment engine at the INSCRIPTION LEVEL — not just
whether individual sign mappings are correct (sign-mapping accuracy) but
whether the decoded inscription sequences are linguistically coherent.

Two complementary measurements:

1. INSCRIPTION-LEVEL DECODING QUALITY
   Uses the known Ugaritic→Hebrew mapping (ground truth) to produce a
   "reference" decoded inscription.  Compares it to the engine's output
   using character n-gram recall (unigram to 3-gram) — a proxy for how
   much correct phoneme sequence is recovered regardless of alignment.

   This simulates the "inscription-level decoding" scenario: given a full
   inscription, how legible / structurally coherent is the decoded result?

2. NOISE ROBUSTNESS SWEEP
   Injects random sign substitution noise into the cipher at rates
   10% / 20% / 30% / 50%, then re-runs the beam decipherment and measures
   accuracy degradation.  This mimics real-world conditions:
     - Damaged inscriptions with missing or corrupted signs
     - OCR errors in digitised corpora
     - Sign variant confusion in early-stage decipherment

   The robustness curve (accuracy vs noise rate) shows at what corpus
   degradation level the engine still produces meaningful output.

Usage:
    python -m glossa_lab.experiments.sequence_eval_benchmark
"""
from __future__ import annotations

import os
import random
import sys
from collections import Counter
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ── N-gram utilities ──────────────────────────────────────────────────

def _ngrams(seq: list[str], n: int) -> Counter:
    return Counter(tuple(seq[i: i + n]) for i in range(len(seq) - n + 1))


def _ngram_recall(reference: list[str], hypothesis: list[str], n: int) -> float:
    """Fraction of reference n-grams that appear anywhere in the hypothesis."""
    ref_ng = _ngrams(reference, n)
    hyp_ng = _ngrams(hypothesis, n)
    total  = sum(ref_ng.values())
    if total == 0:
        return 0.0
    matched = sum(min(ref_ng[ng], hyp_ng.get(ng, 0)) for ng in ref_ng)
    return matched / total


def _word_boundary_coherence(
    decoded_words: list[list[str]],
    target_model: "LanguageModel",
) -> float:
    """Average log-likelihood of decoded word bigrams under target LM.

    A decoded inscription is 'coherent' if its within-word bigrams are
    plausible under the target language model.  Returns normalised score.
    """
    smoothing = 1e-8
    total_ll  = 0.0
    n_scored  = 0
    for word in decoded_words:
        for i in range(len(word) - 1):
            import math
            p = target_model.word_bigram_freq.get((word[i], word[i + 1]), smoothing)
            total_ll += math.log(p)
            n_scored += 1
    return round(total_ll / n_scored, 4) if n_scored > 0 else 0.0


# ── Data loading ──────────────────────────────────────────────────────

def _load() -> dict[str, Any]:
    from corpora.ugaritic import (
        _BAAL_CYCLE_LINES,
        _SIGN_TO_ID,
        get_answer_key,
        get_word_level_inscriptions,
    )

    from glossa_lab.data.old_hebrew import (
        get_corpus_symbols as heb_sym,
    )
    from glossa_lab.data.old_hebrew import (
        get_ugaritic_to_hebrew_map,
    )
    from glossa_lab.data.old_hebrew import (
        get_word_inscriptions as heb_word_inscr,
    )
    from glossa_lab.pipelines.beam_decipher import UGARITIC_PHONO_GROUPS_TIGHT, beam_decipher
    from glossa_lab.pipelines.decipher import LanguageModel, score_accuracy

    def _parse(line: str) -> list[str]:
        return [ch for ch in line.split() if ch != "."]

    decoded_lines  = [_parse(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines  = [[_SIGN_TO_ID.get(s, s) for s in l] for l in decoded_lines]
    cipher_flat    = [s for l in encoded_lines for s in l]

    ug_words_enc   = get_word_level_inscriptions(encoded=True)

    ug_to_ug  = get_answer_key()
    ug_to_heb = get_ugaritic_to_hebrew_map()
    gt        = {oid: ug_to_heb[us] for oid, us in ug_to_ug.items() if us in ug_to_heb}

    heb_flat = heb_sym()
    lm       = LanguageModel(heb_flat, inscriptions=heb_word_inscr())

    # Anchors
    inv_ug = {v: k for k, v in ug_to_ug.items()}
    anchors_10 = {
        inv_ug["r"]: "r", inv_ug["m"]: "m", inv_ug["b"]: "b",
        inv_ug["l"]: "l", inv_ug["n"]: "n", inv_ug["y"]: "y",
        inv_ug["k"]: "k", inv_ug["t"]: "t", inv_ug["d"]: "d",
        inv_ug["h"]: "h",
    }

    return {
        "cipher_flat":       cipher_flat,
        "cipher_lines":      encoded_lines,
        "cipher_words":      ug_words_enc,
        "gt":                gt,
        "lm":                lm,
        "anchors_10":        anchors_10,
        "phono_tight":       UGARITIC_PHONO_GROUPS_TIGHT,
        "beam_decipher":     beam_decipher,
        "score_accuracy":    score_accuracy,
    }


# ── Noise injection ───────────────────────────────────────────────────

def _inject_noise(
    cipher_flat: list[str],
    noise_rate: float,
    rng: random.Random,
) -> list[str]:
    """Randomly substitute `noise_rate` fraction of tokens with other known signs."""
    vocab = list(set(cipher_flat))
    noisy = list(cipher_flat)
    for i in range(len(noisy)):
        if rng.random() < noise_rate:
            # Substitute with a random DIFFERENT sign
            alternatives = [v for v in vocab if v != noisy[i]]
            if alternatives:
                noisy[i] = rng.choice(alternatives)
    return noisy


def _inject_noise_words(
    cipher_words: list[list[str]],
    noise_rate: float,
    rng: random.Random,
) -> list[list[str]]:
    """Noise injection that preserves word-level structure."""
    vocab = list({s for w in cipher_words for s in w})
    result = []
    for word in cipher_words:
        nw = list(word)
        for i in range(len(nw)):
            if rng.random() < noise_rate:
                alts = [v for v in vocab if v != nw[i]]
                if alts:
                    nw[i] = rng.choice(alts)
        result.append(nw)
    return result


# ── Main benchmark ────────────────────────────────────────────────────

def run_sequence_eval_benchmark(verbose: bool = True) -> dict[str, Any]:
    def _pr(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _pr("\n" + "=" * 68)
    _pr("  Sequence-Level Evaluation Benchmark")
    _pr("  (Ugaritic → Hebrew, inscription-level scoring + noise robustness)")
    _pr("=" * 68)

    d   = _load()
    rng = random.Random(42)

    n_tokens = len(d["cipher_flat"])
    n_lines  = len(d["cipher_lines"])
    n_gt     = len(d["gt"])
    _pr(f"\n  Corpus: {n_tokens} tokens  {n_lines} inscription lines")
    _pr(f"  Ground truth: {n_gt} sign mappings")

    results: dict[str, Any] = {}

    # ── Part 1: Inscription-level decoding quality ────────────────────
    _pr("\n\n  ══ PART 1 — Inscription-Level Decoding Quality ══")
    _pr("  Using best beam config (tight phono groups + 10 anchors)")

    beam_result = d["beam_decipher"](
        d["cipher_flat"], d["lm"],
        beam_width=50,
        cipher_inscriptions=d["cipher_words"],
        anchors=d["anchors_10"],
        phono_groups=d["phono_tight"],
        surjective=True,
    )
    proposed_mapping = beam_result["proposed_mapping"]
    sign_acc = d["score_accuracy"](proposed_mapping, d["gt"])

    # Reference decoded text (ground truth mapping)
    ref_flat = [d["gt"].get(s, "?") for s in d["cipher_flat"]]
    ref_words = [[d["gt"].get(s, "?") for s in word] for word in d["cipher_words"]]

    # Engine decoded text
    hyp_flat = [proposed_mapping.get(s, "?") for s in d["cipher_flat"]]
    hyp_words = [[proposed_mapping.get(s, "?") for s in word] for word in d["cipher_words"]]

    # N-gram recall at 1, 2, 3
    r1 = _ngram_recall(ref_flat, hyp_flat, 1)
    r2 = _ngram_recall(ref_flat, hyp_flat, 2)
    r3 = _ngram_recall(ref_flat, hyp_flat, 3)
    wb_coh_ref = _word_boundary_coherence(ref_words, d["lm"])
    wb_coh_hyp = _word_boundary_coherence(hyp_words, d["lm"])

    _pr(f"\n  Sign-mapping accuracy: {sign_acc['correct']}/{n_gt} = "
        f"{sign_acc['correct']/n_gt*100:.1f}%")
    _pr(f"  Unigram recall (1-gram): {r1:.3f}")
    _pr(f"  Bigram  recall (2-gram): {r2:.3f}")
    _pr(f"  Trigram recall (3-gram): {r3:.3f}")
    _pr(f"  Word-boundary coherence (reference): {wb_coh_ref:.4f}")
    _pr(f"  Word-boundary coherence (hypothesis): {wb_coh_hyp:.4f}")
    _pr(f"  Coherence ratio: {wb_coh_hyp / wb_coh_ref:.3f}" if wb_coh_ref != 0 else "  Coherence ratio: N/A")

    results["inscription_level"] = {
        "sign_accuracy": sign_acc["correct"],
        "sign_total":    n_gt,
        "ngram_recall":  {"1gram": round(r1, 3), "2gram": round(r2, 3), "3gram": round(r3, 3)},
        "wb_coherence_ref": wb_coh_ref,
        "wb_coherence_hyp": wb_coh_hyp,
    }

    # ── Part 2: Noise robustness ──────────────────────────────────────
    _pr("\n\n  ══ PART 2 — Noise Robustness Sweep ══")
    _pr("  Injecting random sign substitution noise then re-deciphering")
    _pr(f"  {'Noise':>7}  {'Correct':>8}  {'Accuracy':>9}  {'1-gram rec':>12}  {'2-gram rec':>12}")
    _pr("  " + "-" * 56)

    noise_results = []

    # Clean baseline
    c_clean = sign_acc["correct"]
    r1_clean = r1
    r2_clean = r2
    _pr(f"  {'0% (clean)':>7}  {c_clean:>8}/{n_gt}  {c_clean/n_gt*100:>8.1f}%  "
        f"{r1_clean:>12.3f}  {r2_clean:>12.3f}")
    noise_results.append({
        "noise_rate": 0.0,
        "correct":    c_clean,
        "r1":         r1_clean,
        "r2":         r2_clean,
    })

    for noise_rate in (0.10, 0.20, 0.30, 0.50):
        noisy_flat  = _inject_noise(d["cipher_flat"], noise_rate, rng)
        noisy_words = _inject_noise_words(d["cipher_words"], noise_rate, rng)

        nr = d["beam_decipher"](
            noisy_flat, d["lm"],
            beam_width=50,
            cipher_inscriptions=noisy_words,
            anchors=d["anchors_10"],
            phono_groups=d["phono_tight"],
            surjective=True,
        )
        acc_n  = d["score_accuracy"](nr["proposed_mapping"], d["gt"])
        hyp_n  = [nr["proposed_mapping"].get(s, "?") for s in noisy_flat]
        r1_n   = _ngram_recall(ref_flat, hyp_n, 1)
        r2_n   = _ngram_recall(ref_flat, hyp_n, 2)
        pct_n  = acc_n["correct"] / n_gt * 100
        _pr(f"  {noise_rate*100:>6.0f}%  {acc_n['correct']:>8}/{n_gt}  {pct_n:>8.1f}%  "
            f"{r1_n:>12.3f}  {r2_n:>12.3f}")
        noise_results.append({
            "noise_rate": noise_rate,
            "correct":    acc_n["correct"],
            "r1":         round(r1_n, 3),
            "r2":         round(r2_n, 3),
        })

    results["noise_robustness"] = noise_results

    # ── Robustness summary ────────────────────────────────────────────
    half_acc = sign_acc["correct"] / 2
    breakpoint = next(
        (r["noise_rate"] for r in noise_results if r["correct"] <= half_acc),
        None,
    )
    bp_str = f"{breakpoint*100:.0f}%" if breakpoint is not None else ">50%"

    conclusion = (
        f"Sign-mapping accuracy at 0% noise: {c_clean}/{n_gt} = {c_clean/n_gt*100:.1f}%. "
        f"N-gram recall: 1-gram={r1:.3f}, 2-gram={r2:.3f}, 3-gram={r3:.3f}. "
        f"Accuracy halves at ~{bp_str} noise injection. "
        "This characterises the engine's robustness to damaged or noisy inscription data."
    )
    _pr(f"\n  CONCLUSION: {conclusion}")

    results["conclusion"] = conclusion
    return results


if __name__ == "__main__":
    run_sequence_eval_benchmark(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class SequenceEvalBenchmark(_EB):
    id = "sequence_eval_benchmark"
    name = "Sequence-Level Evaluation Benchmark"
    category = "Validation"
    description = (
        "Evaluates decipherment quality at the inscription level, not just "
        "sign-mapping accuracy. Measures character n-gram recall (1–3-gram) "
        "and word-boundary coherence of decoded inscriptions vs ground truth. "
        "Also sweeps noise injection at 10/20/30/50% to produce robustness "
        "degradation curves for damaged inscription scenarios."
    )
    estimated_time = "~2 min"
    command = "python -m glossa_lab.experiments.sequence_eval_benchmark"
    params_schema: dict = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return run_sequence_eval_benchmark(verbose=False)
