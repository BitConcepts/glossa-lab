"""Meroitic → Coptic benchmark — Tier 1f (graceful degradation test).

Tests the decipherment engine on a WRONG language hypothesis:
  Cipher:  Meroitic sign sequences (opaque ME01–ME19 IDs)
  Target:  Coptic language model (Egyptian-family, Afro-Asiatic)
  Relationship: None established; Meroitic is likely Nilo-Saharan

SCIENTIFIC PURPOSE:
  This benchmark answers the question: "what does the engine do when the
  target language is wrong?"  The Meroitic → Coptic direction is NOT a valid
  linguistic hypothesis — there is no established relationship between
  Meroitic and Coptic/Egyptian.  We expect:

  1. LOW accuracy with Coptic target (~15–25% — near frequency-rank chance)
  2. SMALL or NEGATIVE oracle delta (Coptic statistics provide no useful signal)
  3. LOW kandles confidence

  Contrast with a SELF-REFERENTIAL MODEL (Meroitic phonemes used as their
  own target statistics) which should show near-perfect accuracy and a large
  positive oracle delta.

  The degradation ratio (self-accuracy / Coptic-accuracy) quantifies the
  engine's ability to discriminate correct from incorrect language hypotheses.

ANSWER KEY:
  The Meroitic sign → phoneme mapping is based on Griffith (1911), which is
  accepted as PHONETICALLY CORRECT even though the language semantics remain
  unknown.  We use this as the ground truth for sign-mapping accuracy.

Usage:
    python -m glossa_lab.experiments.meroitic_benchmark
"""
from __future__ import annotations

import os
import sys
import time
from collections import defaultdict
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load() -> dict[str, Any]:
    from glossa_lab.data.meroitic import (
        get_corpus_symbols, get_corpus_inscriptions, get_line_inscriptions,
        get_full_answer_key,
        get_coptic_symbols, get_coptic_inscriptions,
    )
    from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy, _score_mapping
    from glossa_lab.pipelines.beam_decipher import beam_decipher

    cipher_flat  = get_corpus_symbols(encoded=True)
    cipher_words = get_corpus_inscriptions(encoded=True)

    # Self-referential: build LM from the KNOWN Meroitic phoneme sequences
    mero_phonemes = get_corpus_symbols(encoded=False)
    mero_words    = get_corpus_inscriptions(encoded=False)
    lm_self = LanguageModel(mero_phonemes, inscriptions=mero_words)

    # Wrong hypothesis: Coptic language model
    coptic_syms   = get_coptic_symbols()
    coptic_words  = get_coptic_inscriptions()
    lm_coptic = LanguageModel(coptic_syms, inscriptions=coptic_words)

    gt = get_full_answer_key()

    return {
        "cipher_flat":    cipher_flat,
        "cipher_words":   cipher_words,
        "gt":             gt,
        "lm_self":        lm_self,
        "lm_coptic":      lm_coptic,
        "decipher":       decipher,
        "beam_decipher":  beam_decipher,
        "score_accuracy": score_accuracy,
        "_score_mapping": _score_mapping,
    }


def _run_beam(d, lm, beam_width, anchors=None):
    t0 = time.time()
    r = d["beam_decipher"](
        d["cipher_flat"], lm,
        beam_width=beam_width,
        cipher_inscriptions=d["cipher_words"],
        surjective=True,
        anchors=anchors,
    )
    acc = d["score_accuracy"](r["proposed_mapping"], d["gt"])
    return acc["correct"], round(time.time() - t0, 2)


def _run_sa(d, lm, restarts=15, seed=42):
    t0 = time.time()
    r = d["decipher"](
        d["cipher_flat"], lm,
        seed=seed, max_iterations=10000, restarts=restarts,
        cipher_inscriptions=d["cipher_words"],
        surjective=True,
    )
    acc = d["score_accuracy"](r["proposed_mapping"], d["gt"])
    return acc["correct"], round(time.time() - t0, 2)


def _oracle_delta(d, lm, cipher_inscr) -> dict[str, Any]:
    """Score the correct Meroitic mapping against SA mapping under given LM."""
    _score_mapping = d["_score_mapping"]
    score_accuracy = d["score_accuracy"]
    cipher_flat    = d["cipher_flat"]
    gt             = d["gt"]

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

    score_correct = _score_mapping(cipher_flat, gt, lm, cipher_pos,
                                   cipher_inscriptions=cipher_inscr)
    sa_result = d["decipher"](
        cipher_flat, lm,
        seed=42, max_iterations=10000, restarts=15,
        cipher_inscriptions=cipher_inscr,
        surjective=True,
    )
    sa_map   = sa_result["proposed_mapping"]
    score_sa = _score_mapping(cipher_flat, sa_map, lm, cipher_pos,
                               cipher_inscriptions=cipher_inscr)
    acc_sa   = score_accuracy(sa_map, gt)
    delta    = score_correct - score_sa

    return {
        "accuracy":      acc_sa["correct"],
        "score_correct": round(score_correct, 1),
        "score_sa":      round(score_sa, 1),
        "delta":         round(delta, 1),
    }


def run_meroitic_benchmark(verbose: bool = True) -> dict[str, Any]:
    def _pr(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _pr("\n" + "=" * 68)
    _pr("  Meroitic → Coptic Benchmark — Tier 1f (graceful degradation)")
    _pr("=" * 68)

    d = _load()
    n_tokens = len(d["cipher_flat"])
    n_signs  = len(set(d["cipher_flat"]))
    n_gt     = len(d["gt"])
    _pr(f"\n  Meroitic corpus: {n_tokens} tokens  {n_signs} distinct signs")
    _pr(f"  Answer key: {n_gt} Griffith phoneme assignments (Griffith 1911)")
    _pr(f"\n  Two targets:")
    _pr(f"    Self-model:   Meroitic phoneme statistics (correct LM)")
    _pr(f"    Coptic model: {len(d['lm_coptic'].bigram_freq)} bigrams (wrong hypothesis)")

    results: dict[str, Any] = {}

    # ── Self-referential test (ceiling) ──────────────────────────────
    _pr("\n\n  ══ SELF-REFERENTIAL (ceiling — correct Meroitic phoneme model) ══")
    self0, st0 = _run_sa(d, d["lm_self"])
    self_b, stb = _run_beam(d, d["lm_self"], beam_width=100)
    _pr(f"  SA (15 restarts):   {self0}/{n_gt} = {self0/n_gt*100:.1f}%  [{st0}s]")
    _pr(f"  Beam (w=100):       {self_b}/{n_gt} = {self_b/n_gt*100:.1f}%  [{stb}s]")

    self_oracle = _oracle_delta(d, d["lm_self"], d["cipher_words"])
    sign = "+" if self_oracle["delta"] >= 0 else ""
    denom_self = abs(self_oracle["score_sa"]) or 1
    _pr(f"  Oracle delta (self): {sign}{self_oracle['delta']:.1f}  "
        f"({sign}{self_oracle['delta']/denom_self*100:.2f}%)")
    results["self"] = {"sa": self0, "beam": self_b, "oracle_delta": self_oracle["delta"], "total": n_gt}

    # ── Coptic target test (wrong hypothesis) ────────────────────────
    _pr("\n\n  ══ COPTIC TARGET (wrong hypothesis) ══")
    cop0, ct0 = _run_sa(d, d["lm_coptic"])
    cop_b, ctb = _run_beam(d, d["lm_coptic"], beam_width=100)
    _pr(f"  SA (15 restarts):   {cop0}/{n_gt} = {cop0/n_gt*100:.1f}%  [{ct0}s]")
    _pr(f"  Beam (w=100):       {cop_b}/{n_gt} = {cop_b/n_gt*100:.1f}%  [{ctb}s]")

    cop_oracle = _oracle_delta(d, d["lm_coptic"], d["cipher_words"])
    sign2 = "+" if cop_oracle["delta"] >= 0 else ""
    denom_cop = abs(cop_oracle["score_sa"]) or 1
    _pr(f"  Oracle delta (Coptic): {sign2}{cop_oracle['delta']:.1f}  "
        f"({sign2}{cop_oracle['delta']/denom_cop*100:.2f}%)")
    results["coptic"] = {"sa": cop0, "beam": cop_b, "oracle_delta": cop_oracle["delta"], "total": n_gt}

    # ── Degradation analysis ──────────────────────────────────────────
    best_self  = max(self0, self_b)
    best_coptic = max(cop0, cop_b)
    ratio = best_coptic / best_self if best_self > 0 else 0.0

    _pr("\n\n  ══ DEGRADATION ANALYSIS ══")
    _pr(f"  Best accuracy (self-model):   {best_self}/{n_gt} = {best_self/n_gt*100:.1f}%")
    _pr(f"  Best accuracy (Coptic model): {best_coptic}/{n_gt} = {best_coptic/n_gt*100:.1f}%")
    _pr(f"  Degradation ratio:            {ratio:.2f}  "
        f"(1.0 = no degradation; < 0.5 = model detects wrong language)")
    _pr(f"\n  Oracle delta self:   {self_oracle['delta']:+.1f}")
    _pr(f"  Oracle delta Coptic: {cop_oracle['delta']:+.1f}")

    if cop_oracle["delta"] <= 0:
        signal_quality = "NEGATIVE — Coptic statistics actively mislead the optimizer. " \
                          "The engine correctly rejects the wrong hypothesis."
    elif cop_oracle["delta"] < abs(self_oracle["delta"]) * 0.3:
        signal_quality = "WEAK — Coptic provides little useful signal. " \
                          "The engine finds only chance-level alignment."
    else:
        signal_quality = "MODERATE — Some phonotactic overlap between Meroitic and Coptic " \
                          "accidentally provides partial signal. Not a validated relationship."

    conclusion = (
        f"Meroitic→Coptic accuracy: {best_coptic}/{n_gt} = {best_coptic/n_gt*100:.1f}% "
        f"(self-model: {best_self}/{n_gt} = {best_self/n_gt*100:.1f}%). "
        f"Oracle signal: {signal_quality}"
    )
    _pr(f"\n  CONCLUSION: {conclusion}")

    results["degradation_ratio"] = round(ratio, 3)
    results["oracle_signal_quality"] = signal_quality
    results["conclusion"] = conclusion
    return results


if __name__ == "__main__":
    run_meroitic_benchmark(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class MeroiticBenchmark(_EB):
    id = "meroitic_benchmark"
    name = "Meroitic → Coptic Benchmark (Tier 1f)"
    category = "Validation"
    description = (
        "Graceful degradation test: applies the decipherment engine to Meroitic "
        "(phonetically deciphered, language unknown) targeting Coptic "
        "(Egyptian/Afro-Asiatic — linguistically unrelated hypothesis). "
        "Contrasts self-model ceiling vs Coptic degradation to quantify the "
        "engine's ability to detect a wrong language hypothesis. "
        "Expected: low accuracy (~15–25%) and small/negative oracle delta with Coptic."
    )
    estimated_time = "~2 min"
    command = "python -m glossa_lab.experiments.meroitic_benchmark"
    params_schema: dict = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return run_meroitic_benchmark(verbose=False)
