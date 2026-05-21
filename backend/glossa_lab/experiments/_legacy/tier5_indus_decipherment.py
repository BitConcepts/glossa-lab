"""Tier 5 — Indus Script Beam Decipherment Hypothesis Test (Clean Protocol).

SCIENTIFIC CONTEXT (Dr. Fuls validation progression):
  After validating the beam decipherment on Ugaritic→Hebrew (Tier 1–4), we
  apply it to the Indus Script.  The first attempt revealed a methodological
  problem: the top-30 Indus signs are dominated by TERMINAL signs (logograms
  or determinatives) that appear at the end of nearly every inscription.
  Mapping all of them to the most-frequent vowel produces a trivially high
  score for any vowel-heavy language (Dravidian, Sanskrit).

  This version implements the Fuls-style anti-circularity fix:

  SIGN CLASSIFICATION PROTOCOL
  ──────────────────────────
  For each Indus sign compute:
    - terminal_bias = n_terminal / n_total_occurrences
    - initial_bias  = n_initial  / n_total_occurrences
    - positional_entropy = H(initial, medial, terminal)

  Classification:
    TERMINAL SIGN   terminal_bias >= 0.50  → likely logogram / determinative
    INITIAL  SIGN   initial_bias  >= 0.60  → likely prefix / conjunction marker
    PHONOGRAM CAND  otherwise, freq >= MIN_FREQ, entropy >= MIN_ENTROPY

  The beam runs ONLY on PHONOGRAM CANDIDATES.  This removes the terminal-sign
  artifact and tests genuine phonotactic compatibility.

HYPOTHESES TESTED:
  1. Proto-Dravidian (Tamil/Kannada/Telugu ancestor)  — Parpola hypothesis
  2. Indo-Aryan / Sanskrit (Vedic ancestor)           — Rao et al. hypothesis
  3. Sumerian (logo-syllabic control)                 — some early proposals
  4. Hebrew / NW Semitic (known-decipherment control)

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


# ── Sign classification ─────────────────────────────────────

# Thresholds
_TERMINAL_BIAS_LOGOGRAM = 0.50   # terminal% ≥ this → terminal logogram
_INITIAL_BIAS_PREFIX    = 0.60   # initial%  ≥ this → initial prefix/marker
_MIN_ENTROPY            = 0.50   # H(pos) ≥ this → balanced enough for phonogram
_MIN_FREQ               = 8      # minimum occurrences to include


def classify_indus_signs(
    inscriptions: list[list[str]],
) -> dict[str, dict]:
    """Classify each Indus sign as LOGOGRAM, INITIAL, or PHONOGRAM.

    Returns a dict {sign: {type, freq, terminal_bias, initial_bias, entropy}}.
    """
    from collections import defaultdict
    pos: dict[str, dict[str, int]] = defaultdict(
        lambda: {"initial": 0, "medial": 0, "terminal": 0}
    )
    freq: Counter = Counter()

    for insc in inscriptions:
        if len(insc) < 2:
            continue
        for s in insc:
            freq[s] += 1
        pos[insc[0]]["initial"]  += 1
        pos[insc[-1]]["terminal"] += 1
        for s in insc[1:-1]:
            pos[s]["medial"] += 1

    result = {}
    for sign, cnt in freq.items():
        if cnt < _MIN_FREQ:
            result[sign] = {"type": "RARE", "freq": cnt}
            continue
        p = pos[sign]
        total = p["initial"] + p["medial"] + p["terminal"]
        tb = p["terminal"] / total if total else 0.0
        ib = p["initial"]  / total if total else 0.0
        probs = [p["initial"] / total, p["medial"] / total, p["terminal"] / total]
        h = -sum(q * math.log(q + 1e-12) for q in probs)

        if tb >= _TERMINAL_BIAS_LOGOGRAM:
            stype = "LOGOGRAM"
        elif ib >= _INITIAL_BIAS_PREFIX:
            stype = "INITIAL"
        elif h >= _MIN_ENTROPY:
            stype = "PHONOGRAM"
        else:
            stype = "MEDIAL"   # appears mostly in medial position; ambiguous

        result[sign] = {
            "type":          stype,
            "freq":          cnt,
            "terminal_bias": round(tb, 3),
            "initial_bias":  round(ib, 3),
            "entropy":       round(h, 4),
        }
    return result


# ── Shared setup ─────────────────────────────────────

def _load():
    from glossa_lab.data.dravidian import get_corpus_symbols as drav_sym
    from glossa_lab.data.indus_public_corpus import (
        get_corpus_inscriptions as ind_ins,
    )
    from glossa_lab.data.indus_public_corpus import (
        get_corpus_symbols as ind_sym,
    )
    from glossa_lab.data.old_hebrew import (
        get_corpus_inscriptions as heb_ins,
    )
    from glossa_lab.data.old_hebrew import (
        get_corpus_symbols as heb_sym,
    )
    from glossa_lab.data.sanskrit import get_corpus_symbols as skt_sym
    from glossa_lab.data.sumerian_ur3 import (
        get_corpus_inscriptions as sum_ins,
    )
    from glossa_lab.data.sumerian_ur3 import (
        get_corpus_symbols as sum_sym,
    )
    from glossa_lab.pipelines.beam_decipher import beam_decipher
    from glossa_lab.pipelines.decipher import LanguageModel, _score_mapping

    lm_drav = LanguageModel(drav_sym())
    lm_skt  = LanguageModel(skt_sym())
    lm_sum  = LanguageModel(sum_sym(), inscriptions=sum_ins())
    lm_heb  = LanguageModel(heb_sym(), inscriptions=heb_ins())

    indus_flat  = ind_sym()
    indus_inscr = ind_ins()
    indus_freq  = Counter(indus_flat)

    # Classify all Indus signs
    sign_classes = classify_indus_signs(indus_inscr)

    return {
        "lm_drav":      lm_drav,
        "lm_skt":       lm_skt,
        "lm_sum":       lm_sum,
        "lm_heb":       lm_heb,
        "indus_flat":   indus_flat,
        "indus_inscr":  indus_inscr,
        "indus_freq":   indus_freq,
        "sign_classes": sign_classes,
        "beam_decipher":   beam_decipher,
        "_score_mapping":  _score_mapping,
        "LanguageModel":   LanguageModel,
    }


# ── Beam + random-baseline scoring ──────────────────────────────────────

def _score_hypothesis(
    d: dict,
    lm,
    label: str,
    allowed_sign_types: tuple = ("PHONOGRAM", "MEDIAL"),
    n_random: int = 50,
    verbose: bool = True,
    use_max_k: bool = True,
) -> dict[str, Any]:
    """Run beam decipherment and score against random baseline.

    allowed_sign_types: which sign classes to include in the cipher.
    use_max_k: if True, enforce max_target_reuse = ceil(n_cipher/n_target)
      to prevent degenerate all-to-one mappings.
    """
    indus_inscr   = d["indus_inscr"]
    indus_freq    = d["indus_freq"]
    sign_classes  = d["sign_classes"]
    _score_mapping = d["_score_mapping"]

    # Build the phonogram sign set
    allowed = {s for s, info in sign_classes.items()
               if info["type"] in allowed_sign_types}

    # Filter inscriptions to only use allowed signs
    filtered_inscr = [
        [s for s in insc if s in allowed]
        for insc in indus_inscr
    ]
    filtered_inscr = [i for i in filtered_inscr if len(i) >= 2]
    filtered_flat  = [s for i in filtered_inscr for s in i]

    # ── Beam: find best mapping ────────────────────────────────────
    # max-K diversity: each language phoneme used at most ceil(n_cipher/n_target) times
    # Prevents degenerate all-to-'a' solution that dominates without this constraint
    n_cipher_signs = len(Counter(filtered_flat))
    n_target_signs = len(lm.alphabet)
    max_k = math.ceil(n_cipher_signs / n_target_signs) if use_max_k and n_target_signs > 0 else 0

    result = d["beam_decipher"](
        filtered_flat,
        lm,
        beam_width=200,
        cipher_inscriptions=filtered_inscr,
        surjective=True,
        max_target_reuse=max_k,
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

    # ── Top-sign proposed readings ────────────────────────────────────
    # Top signs by frequency within the allowed subset
    top_signs_in_subset = [
        s for s, _ in Counter(filtered_flat).most_common()
    ]
    top10_readings = [
        (sign, indus_freq[sign], best_map.get(sign, "?"))
        for sign in top_signs_in_subset[:10]
    ]

    n_signs_used = len(Counter(filtered_flat))
    n_inscr_used = len(filtered_inscr)

    if verbose:
        print(f"\n  [{label}]  LM: {len(lm.alphabet)} signs, {len(lm.bigram_freq)} bigrams  max_k={max_k}")
        print(f"    Cipher signs used: {n_signs_used}  inscriptions: {n_inscr_used}")
        print(f"    Best beam score:   {best_score:.1f}")
        print(f"    Random mean ± std: {mean_rand:.1f} ± {std_rand:.1f}")
        print(f"    Z-score:           {z_score:+.2f}")
        print(f"    Kandles:           {kandles:.4f}")
        print("    Top 10 proposed readings (sign \u2192 phoneme):")
        for s, cnt, ph in top10_readings:
            cls = sign_classes.get(s, {}).get('type', '?')
            print(f"      {s:6} ({cls:10}) n={cnt:4}  \u2192  {ph}")

    return {
        "label":           label,
        "best_score":      round(best_score, 2),
        "mean_random":     round(mean_rand, 2),
        "std_random":      round(std_rand, 2),
        "z_score":         round(z_score, 3),
        "kandles":         round(kandles, 4),
        "top10_readings":  top10_readings,
        "lm_size":         len(lm.alphabet),
        "n_signs_used":    n_signs_used,
        "n_inscr_used":    n_inscr_used,
    }


# ── Main experiment ──────────────────────────────────────────────────────

def run_tier5_indus(verbose: bool = True, top_n: int = 30) -> dict[str, Any]:
    def _pr(*a, **kw):
        if verbose: print(*a, **kw)

    _pr("\n" + "=" * 70)
    _pr("  Tier 5 — Indus Script Beam Hypothesis Test (Clean Protocol)")
    _pr("=" * 70)

    d = _load()
    sign_classes = d["sign_classes"]

    # ── Sign classification summary ─────────────────────────────────
    by_type: dict[str, list] = {}
    for s, info in sign_classes.items():
        by_type.setdefault(info["type"], []).append((s, info["freq"]))

    _pr(f"\n  Indus corpus: {len(d['indus_flat'])} tokens  "
        f"V={len(d['indus_freq'])} signs  "
        f"{len(d['indus_inscr'])} inscriptions")
    _pr("\n  Sign classification (terminal≥50%→LOGOGRAM, initial≥60%→INITIAL, "
        "entropy≥0.50→PHONOGRAM, else MEDIAL):")
    for t in ("LOGOGRAM", "INITIAL", "PHONOGRAM", "MEDIAL", "RARE"):
        signs = by_type.get(t, [])
        top5 = sorted(signs, key=lambda x: -x[1])[:5]
        _pr(f"    {t:12}: {len(signs):3} signs  "
            f"(top 5: {', '.join(s for s,_ in top5)})")

    phonogram_signs = {s for s, info in sign_classes.items()
                       if info["type"] in ("PHONOGRAM", "MEDIAL")}
    _pr(f"\n  PHONOGRAM + MEDIAL subset: {len(phonogram_signs)} signs  "
        f"(excluding LOGOGRAM terminal signs and INITIAL prefix markers)")

    hypotheses = [
        ("Proto-Dravidian",   d["lm_drav"]),
        ("Indo-Aryan/Sanskrit", d["lm_skt"]),
        ("Sumerian",          d["lm_sum"]),
        ("Hebrew (control)",  d["lm_heb"]),
    ]

    _pr("\n" + "=" * 70)
    _pr("  PASS A — Phonogram + Medial signs only (clean, no logograms)")
    _pr("=" * 70)

    results = []
    for label, lm in hypotheses:
        r = _score_hypothesis(
            d, lm, label,
            allowed_sign_types=("PHONOGRAM", "MEDIAL"),
            verbose=verbose,
        )
        results.append(r)

    # ── Summary table ─────────────────────────────────────────────
    _pr("\n\n" + "=" * 70)
    _pr("  SUMMARY — Ranked by Z-score (phonogram+medial subset, no logograms)")
    _pr("=" * 70)
    ranked = sorted(results, key=lambda x: -x["z_score"])
    _pr(f"\n  {'Hypothesis':<24} {'Signs':>6}  {'Best':>10}  {'Random':>10}  "
        f"{'Z-score':>8}  {'Kandles':>8}")
    _pr("  " + "-" * 72)
    for r in ranked:
        _pr(f"  {r['label']:<24} {r['n_signs_used']:>6}  "
            f"{r['best_score']:>10.1f}  {r['mean_random']:>10.1f}  "
            f"{r['z_score']:>8.2f}  {r['kandles']:>8.4f}")

    winner  = ranked[0]
    runner  = ranked[1] if len(ranked) > 1 else winner
    margin  = winner["z_score"] - runner["z_score"]

    if winner["z_score"] > 3.0 and margin > 0.5:
        interp = (
            f"CLEAR SIGNAL — {winner['label']} leads (Z={winner['z_score']:.2f}, "
            f"+{margin:.2f} over {runner['label']}). "
            f"Phonogram-subset Indus phonotactics best fit this language family."
        )
    elif winner["z_score"] > 3.0:
        interp = (
            f"TIED SIGNAL — {winner['label']} and {runner['label']} score similarly "
            f"(Z={winner['z_score']:.2f} vs {runner['z_score']:.2f}, margin {margin:.2f}). "
            f"Both hypotheses are compatible with the phonogram-subset distributions."
        )
    elif winner["z_score"] > 1.5:
        interp = (
            f"WEAK SIGNAL — {winner['label']} marginally above random (Z={winner['z_score']:.2f}). "
            f"The phonogram subset may need more data or refined sign classification."
        )
    else:
        interp = (
            "INCONCLUSIVE — No hypothesis scores significantly above random on the "
            "phonogram subset. Further sign classification or larger language LMs needed."
        )

    _pr(f"\n  INTERPRETATION: {interp}")
    _pr("\n  METHODOLOGY NOTE: Terminal signs (logograms/determinatives) are excluded.")
    _pr("  Z-scores measure phonotactic compatibility of CANDIDATE PHONOGRAMS only.")
    _pr("  Hebrew control validates the method: low Z expected (Semitic unlike Indus).")
    _pr("  Leading hypothesis provides the prior for the next stage:")
    _pr("  constructing phonological group constraints — as done for Ugaritic→Hebrew.")

    return {
        "results":          results,
        "ranked":           ranked,
        "winner":           winner["label"],
        "winner_z":         round(winner["z_score"], 3),
        "margin":           round(margin, 3),
        "interpretation":   interp,
        "sign_class_counts": {t: len(by_type.get(t, []))
                              for t in ("LOGOGRAM","INITIAL","PHONOGRAM","MEDIAL","RARE")},
        "n_phonogram_signs": len(phonogram_signs),
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
