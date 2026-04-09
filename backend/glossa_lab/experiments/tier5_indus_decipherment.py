"""Tier 5 — Indus Script Beam Decipherment Hypothesis Test.

SCIENTIFIC CONTEXT (Dr. Fuls validation progression):
  After validating the beam decipherment framework on Ugaritic→Hebrew
  (Tier 1–4), we apply it to the Indus Script — the primary research target.

APPROACH:
  For each language-family hypothesis, we build a language model and run
  the beam decipherment on the top-N most-frequent Indus signs.  The beam
  finds the mapping from Indus sign IDs → hypothesis-language phonemes
  that maximises the bigram log-likelihood.

  We compare:
    (A) Best-mapping score       — the optimal fit achievable
    (B) Random baseline score    — mean of 50 random mappings
    (C) Z-score = (A − B) / σ   — how far above random is the best fit?
    (D) Kandles confidence       — phonetic fingerprint similarity

  The hypothesis with the highest Z-score has the STRONGEST bigram
  signal relative to a random baseline, suggesting the Indus phonotactics
  are most similar to that language family.

HYPOTHESES TESTED:
  1. Proto-Dravidian (Tamil/Kannada/Telugu ancestor) — Parpola hypothesis
  2. Indo-Aryan / Sanskrit (Vedic ancestor)          — Rao et al. hypothesis
  3. Sumerian (cuneiform, logo-syllabic)              — some early proposals
  4. Hebrew / NW Semitic (control — known decipherment)

LIMITATIONS:
  - We treat all Indus signs as phonograms; logograms are included,
    inflating sign count and reducing model quality.
  - Corpora are small (Dravidian ~1300, Sanskrit ~1000 tokens).
  - No phonological group constraints applied (unknown correspondences).
  - This is a HYPOTHESIS SCORING experiment, not a claimed decipherment.

Usage:
    python -m glossa_lab.experiments.tier5_indus_decipherment
"""
from __future__ import annotations

import math
import os
import random
import sys
from collections import Counter
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _BACKEND)


# ── Shared setup ────────────────────────────────────────────────────────

def _load():
    from glossa_lab.data.dravidian  import get_corpus_symbols as drav_sym
    from glossa_lab.data.sanskrit   import get_corpus_symbols as skt_sym
    from glossa_lab.data.sumerian_ur3 import (
        get_corpus_symbols as sum_sym,
        get_corpus_inscriptions as sum_ins,
    )
    from glossa_lab.data.old_hebrew  import (
        get_corpus_symbols as heb_sym,
        get_corpus_inscriptions as heb_ins,
    )
    from glossa_lab.data.indus_public_corpus import (
        get_corpus_symbols as ind_sym,
        get_corpus_inscriptions as ind_ins,
    )
    from glossa_lab.pipelines.decipher import LanguageModel, _score_mapping
    from glossa_lab.pipelines.beam_decipher import beam_decipher

    # Dravidian + Sanskrit: no inscription-level data, build flat LM only
    lm_drav = LanguageModel(drav_sym())
    lm_skt  = LanguageModel(skt_sym())
    lm_sum  = LanguageModel(sum_sym(), inscriptions=sum_ins())
    lm_heb  = LanguageModel(heb_sym(), inscriptions=heb_ins())

    indus_flat  = ind_sym()
    indus_inscr = ind_ins()
    indus_freq  = Counter(indus_flat)

    return {
        "lm_drav":     lm_drav,
        "lm_skt":      lm_skt,
        "lm_sum":      lm_sum,
        "lm_heb":      lm_heb,
        "indus_flat":  indus_flat,
        "indus_inscr": indus_inscr,
        "indus_freq":  indus_freq,
        "beam_decipher":   beam_decipher,
        "_score_mapping":  _score_mapping,
        "LanguageModel":   LanguageModel,
    }


# ── Beam + random-baseline scoring ──────────────────────────────────────

def _score_hypothesis(
    d: dict,
    lm,
    label: str,
    top_n: int = 30,
    n_random: int = 50,
    verbose: bool = True,
) -> dict[str, Any]:
    """Run beam decipherment and score against random baseline."""
    indus_flat  = d["indus_flat"]
    indus_inscr = d["indus_inscr"]
    indus_freq  = d["indus_freq"]
    _score_mapping = d["_score_mapping"]

    # Restrict cipher to top-N signs (most frequent — fewest missing bigrams)
    top_signs = [s for s, _ in indus_freq.most_common(top_n)]
    top_sign_set = set(top_signs)

    # Filter inscriptions to only use top-N signs
    filtered_inscr = [
        [s for s in insc if s in top_sign_set]
        for insc in indus_inscr
    ]
    filtered_inscr = [i for i in filtered_inscr if len(i) >= 2]
    filtered_flat  = [s for i in filtered_inscr for s in i]

    # ── Beam: find best mapping ────────────────────────────────────────
    result = d["beam_decipher"](
        filtered_flat,
        lm,
        beam_width=200,
        cipher_inscriptions=filtered_inscr,
        surjective=True,
    )
    best_score = result["score"]
    best_map   = result["proposed_mapping"]
    kandles    = result["kandles_confidence"]

    # ── Random baseline: 50 random mappings ───────────────────────────
    cipher_ranked = [s for s, _ in Counter(filtered_flat).most_common()]
    target_alpha  = lm.ranked
    rng = random.Random(42)
    rand_scores = []
    for _ in range(n_random):
        shuffled = list(target_alpha)
        rng.shuffle(shuffled)
        # Build random mapping (surjective: cycle if cipher > target)
        from itertools import cycle
        m = dict(zip(cipher_ranked, cycle(shuffled)))
        rand_scores.append(_score_mapping(filtered_flat, m, lm, {}))

    mean_rand = sum(rand_scores) / len(rand_scores)
    std_rand  = math.sqrt(sum((x - mean_rand)**2 for x in rand_scores) / len(rand_scores))
    z_score   = (best_score - mean_rand) / std_rand if std_rand > 0 else 0.0

    # ── Top-sign proposed readings ─────────────────────────────────────
    top10_readings = [
        (sign, indus_freq[sign], best_map.get(sign, "?"))
        for sign in top_signs[:10]
    ]

    if verbose:
        print(f"\n  [{label}]  LM: {len(lm.alphabet)} signs, {len(lm.bigram_freq)} bigrams")
        print(f"    Best beam score:   {best_score:.1f}")
        print(f"    Random mean ± std: {mean_rand:.1f} ± {std_rand:.1f}")
        print(f"    Z-score:           {z_score:+.2f}")
        print(f"    Kandles:           {kandles:.4f}")
        print(f"    Top 10 proposed readings (sign → phoneme):")
        for s, cnt, ph in top10_readings:
            print(f"      {s:6} (n={cnt:4})  →  {ph}")

    return {
        "label":           label,
        "best_score":      round(best_score, 2),
        "mean_random":     round(mean_rand, 2),
        "std_random":      round(std_rand, 2),
        "z_score":         round(z_score, 3),
        "kandles":         round(kandles, 4),
        "top10_readings":  top10_readings,
        "lm_size":         len(lm.alphabet),
    }


# ── Main experiment ──────────────────────────────────────────────────────

def run_tier5_indus(verbose: bool = True, top_n: int = 30) -> dict[str, Any]:
    def _pr(*a, **kw):
        if verbose: print(*a, **kw)

    _pr("\n" + "=" * 70)
    _pr("  Tier 5 — Indus Script Beam Hypothesis Test")
    _pr("=" * 70)

    d = _load()

    _pr(f"\n  Indus corpus: {len(d['indus_flat'])} tokens  "
        f"V={len(d['indus_freq'])} distinct signs  "
        f"{len(d['indus_inscr'])} inscriptions")
    _pr(f"  Testing top {top_n} most-frequent signs against 4 hypotheses")
    _pr(f"  Scoring: beam (width=200) vs 50 random baselines → Z-score")

    hypotheses = [
        ("Proto-Dravidian",   d["lm_drav"]),
        ("Indo-Aryan/Sanskrit", d["lm_skt"]),
        ("Sumerian",          d["lm_sum"]),
        ("Hebrew (control)",  d["lm_heb"]),
    ]

    results = []
    for label, lm in hypotheses:
        r = _score_hypothesis(d, lm, label, top_n=top_n, verbose=verbose)
        results.append(r)

    # ── Summary table ───────────────────────────────────────────────────
    _pr("\n\n" + "=" * 70)
    _pr("  SUMMARY — Ranked by Z-score (higher = better fit above random)")
    _pr("=" * 70)
    ranked = sorted(results, key=lambda x: -x["z_score"])
    _pr(f"\n  {'Hypothesis':<24} {'Best score':>12}  {'Random mean':>12}  {'Z-score':>8}  {'Kandles':>8}")
    _pr("  " + "-" * 68)
    for r in ranked:
        _pr(f"  {r['label']:<24} {r['best_score']:>12.1f}  "
            f"{r['mean_random']:>12.1f}  {r['z_score']:>8.2f}  {r['kandles']:>8.4f}")

    winner = ranked[0]

    if winner["z_score"] > 3.0:
        interp = (
            f"STRONG SIGNAL — {winner['label']} fits significantly above random (Z={winner['z_score']:.2f}). "
            f"The Indus phonotactics are most consistent with this language family's bigram structure."
        )
    elif winner["z_score"] > 1.5:
        interp = (
            f"MODERATE SIGNAL — {winner['label']} marginally outperforms random (Z={winner['z_score']:.2f}). "
            f"Consistent with the hypothesis but not conclusive without more data."
        )
    else:
        interp = (
            f"WEAK / INCONCLUSIVE — No hypothesis produces a strong Z-score. "
            f"The Indus corpus may be too small, or the script may be logo-syllabic "
            f"(many signs are determinatives/logograms, not phonograms)."
        )

    _pr(f"\n  INTERPRETATION: {interp}")

    _pr("\n  NOTE ON METHODOLOGY:")
    _pr("  Z-scores measure bigram phonotactic similarity, not phonetic identity.")
    _pr("  A high Z-score means Indus sign sequences RESEMBLE the hypothesis")
    _pr("  language's consonant cluster patterns — not that the signs ARE those")
    _pr("  phonemes. This is a distributional compatibility test, not a reading.")
    _pr("  The Hebrew control should score near 0 (Semitic phonotactics are")
    _pr("  unlike Indus). A high-Z hypothesis provides the strongest prior for")
    _pr("  the next stage: phonological group hypothesis construction.")

    return {
        "results":          results,
        "ranked":           ranked,
        "winner":           winner["label"],
        "winner_z":         winner["z_score"],
        "interpretation":   interp,
        "top_n":            top_n,
        "indus_tokens":     len(d["indus_flat"]),
        "indus_vocabulary": len(d["indus_freq"]),
    }


if __name__ == "__main__":
    run_tier5_indus(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class Tier5IndusBenchmark(_EB):
    id = "tier5_indus_decipherment"
    name = "Tier 5 — Indus Beam Hypothesis Test"
    category = "Validation"
    description = (
        "Applies the validated beam decipherment framework to the Indus Script. "
        "Tests four language-family hypotheses (Proto-Dravidian, Sanskrit, Sumerian, "
        "Hebrew) by scoring the maximum-achievable bigram log-likelihood under each LM. "
        "Reports Z-scores relative to a 50-sample random baseline. "
        "Higher Z-score = Indus phonotactics more similar to that language family. "
        "This is a hypothesis SCORING experiment, not a claimed decipherment."
    )
    estimated_time = "~3 min"
    command = "python -m glossa_lab.experiments.tier5_indus_decipherment"
    params_schema = {
        "type": "object",
        "properties": {
            "top_n": {
                "type": "integer",
                "title": "Top N Signs",
                "default": 30,
                "minimum": 10,
                "maximum": 100,
                "description": "Number of most-frequent Indus signs to include.",
            },
        },
    }

    def run(self, **kwargs) -> dict:
        top_n = int(kwargs.get("top_n") or 30)
        return run_tier5_indus(verbose=False, top_n=top_n)
