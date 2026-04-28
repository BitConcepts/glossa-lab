"""Fuls NW Semitic Test1 -- RTL Correction and Verified Anchor Experiment.

Dr. Fuls has informed us that the test1 word list is read RIGHT-TO-LEFT.
This means every word sequence as parsed (left-to-right in the file) must
be REVERSED to obtain the phonetically correct order:

  File:  066-069-090-112   (parsed left-to-right)
  RTL:   112-090-069-066   (phonetic order: 112 is word-INITIAL, 066 is word-FINAL)

Previously, sign 066 was labelled I=0.967 (word-initial); corrected, it is
word-FINAL (T-position).  Sign 112 was labelled T=0.952; corrected, it is
word-INITIAL (I-position).

This module:

1. ASHRAF DIRECTIONAL ANALYSIS
   Ashraf & Sinha (2018 PLoS ONE) showed that the WORD-END is universally
   MORE CONSTRAINED (lower entropy / higher Gini) than the word-beginning.
   We apply this to confirm RTL from the data itself:
   - Compute H (entropy) of sign occurrence at position 0 (leftmost in our
     parse) and position -1 (rightmost).
   - If H(position 0) < H(position -1): leftmost is more constrained =
     leftmost is word-END = reading is RIGHT-TO-LEFT (confirms Dr. Fuls).

2. CORRECTED POSITIONAL PROFILES
   Re-compute T/I/M positional profiles on reversed sequences.

3. CONDITION A -- No anchors (RTL-corrected sequences)
   20 independent SA seeds. Mapping inference with reversed corpus.

4. CONDITION B -- Dr. Fuls' verified anchors (RTL-corrected sequences)
   Anchors provided by Dr. Fuls:
     004 = T (tet)
     066 = M (mem)
     208 = N (nun)
     133 = ' (ayin)
     128 = L (lamed)
     080 = W (waw, also written U for the vowel)
   20 seeds.

NOTE ON VOWELS:
   Hebrew is a consonant-only (abjad) writing system. The test1 corpus uses
   a CV syllabic system where each sign encodes a consonant+vowel pair.
   The surjective (many-to-one) mapping in our SA correctly handles this:
   multiple signs representing the same consonant with different vowels
   (e.g., ma/mi/mu) all map to the same target consonant (/m/).
   However, the Hebrew LM does not capture vowel harmony or vowel sequence
   patterns. This is acknowledged as a limitation; the consonantal skeleton
   model provides the primary phonotactic signal.

Usage:
    python -m glossa_lab.experiments.fuls_rtl_corrected

Output:
    reports/fuls_rtl_corrected_<timestamp>.json
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from glossa_lab.experiments._parallel import run_seeds_parallel

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
ROOT     = Path(_BACKEND).parent
REPORTS  = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

for _p in (_BACKEND, os.path.join(_BACKEND, "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Dr. Fuls' verified anchor assignments (Condition B)
FULS_ANCHORS = {
    "004": "T",    # tet
    "066": "m",    # mem  (note: was labelled word-initial before; corrected = word-final)
    "208": "n",    # nun
    "133": "E",    # ayin  (using 'E' as ayin transliteration, matching Hebrew corpus)
    "128": "l",    # lamed
    "080": "w",    # waw (also = U vowel in syllabic context)
}

N_SEEDS = 20


# ── Helpers ───────────────────────────────────────────────────────────────────

def _entropy(counts: dict) -> float:
    total = sum(counts.values()) or 1
    return -sum((c / total) * math.log2(c / total) for c in counts.values() if c > 0)

def _gini(counts: dict) -> float:
    """Gini coefficient of inequality for sign occurrence counts."""
    vals = sorted(counts.values())
    n = len(vals)
    if n == 0: return 0.0
    total = sum(vals)
    if total == 0: return 0.0
    cumsum = 0.0
    g = 0.0
    for i, v in enumerate(vals, 1):
        cumsum += v
        g += (2 * i - n - 1) * v
    return g / (n * total)

def _mean(xs): return sum(xs) / len(xs) if xs else float("nan")
def _std(xs):
    if len(xs) < 2: return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _load_test1():
    f = Path(_BACKEND) / "glossa_lab" / "data" / "fuls_nw_semitic_test1.txt"
    words = []
    with open(f, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line: continue
            parts = [s.strip() for s in line.split("-") if s.strip()]
            if parts: words.append(parts)
    return words


def _build_lm():
    from glossa_lab.data.old_hebrew import _HEBREW_LINES
    from glossa_lab.pipelines.decipher import LanguageModel
    hw = []
    for line in _HEBREW_LINES:
        for w in line.split("."):
            w = w.strip()
            if w: hw.append(w.split())
    return LanguageModel([s for w in hw for s in w], inscriptions=hw)


def _run_mapping(cipher_words, lm, seed, anchors=None):
    from glossa_lab.pipelines.decipher import decipher
    flat = [s for w in cipher_words for s in w]
    if not flat: return {}
    r = decipher(flat, lm, seed=seed, max_iterations=12000, restarts=10,
                 cipher_inscriptions=cipher_words, surjective=True, use_sa=True,
                 sa_temp_start=1.2, sa_cooling=0.9990,
                 positional_weight=0.01, ocp_weight=1.0,
                 anchors=anchors)
    return r.get("proposed_mapping", {})


def _bigram_plaus(mapping, cipher_words, lm):
    smoothing = 1e-8
    ll, n = 0.0, 0
    for word in cipher_words:
        dec = [mapping.get(s) for s in word if mapping.get(s)]
        for i in range(len(dec) - 1):
            ll += math.log(lm.bigram_freq.get((dec[i], dec[i+1]), smoothing))
            n += 1
    return ll / n if n > 0 else float("nan")


def _positional_profiles(words, all_signs):
    """Compute T/I/M positional profiles for a word list."""
    pos_counts = {s: {"initial": 0, "medial": 0, "terminal": 0} for s in all_signs}
    for word in words:
        if not word: continue
        pos_counts[word[0]]["initial"] += 1
        pos_counts[word[-1]]["terminal"] += 1
        for s in word[1:-1]:
            pos_counts[s]["medial"] += 1
    profiles = {}
    for s in all_signs:
        total = sum(pos_counts[s].values())
        if total == 0:
            profiles[s] = {"T": 0.0, "I": 0.0, "M": 0.0, "n": 0}
        else:
            profiles[s] = {
                "T": round(pos_counts[s]["terminal"] / total, 3),
                "I": round(pos_counts[s]["initial"]  / total, 3),
                "M": round(pos_counts[s]["medial"]   / total, 3),
                "n": total,
            }
    return profiles


def _consistency(all_mappings, all_signs):
    result = {}
    for sign in all_signs:
        proposals = [m.get(sign) for m in all_mappings if sign in m]
        if not proposals:
            result[sign] = {"modal": None, "consistency": 0.0, "n_runs": 0}
            continue
        counts = Counter(proposals)
        modal, mc = counts.most_common(1)[0]
        result[sign] = {"modal": modal, "consistency": round(mc / len(proposals), 3),
                        "n_runs": len(proposals), "top3": [k for k, _ in counts.most_common(3)]}
    return result


# ── Main experiment ───────────────────────────────────────────────────────────

def run_rtl_corrected(verbose: bool = True) -> dict[str, Any]:
    def _pr(*a, **kw):
        if verbose: print(*a, **kw)

    _pr("\n" + "=" * 76)
    _pr("  Fuls NW Semitic Test1 -- RTL Correction and Verified Anchor Experiment")
    _pr("=" * 76)

    # Load corpus (as originally parsed: left-to-right in file)
    words_ltr = _load_test1()
    all_signs  = sorted(set(s for w in words_ltr for s in w))
    sign_freqs = Counter(s for w in words_ltr for s in w)

    # RTL-corrected corpus: reverse each word
    words_rtl = [list(reversed(w)) for w in words_ltr]

    _pr(f"\n  Corpus: {len(words_ltr)} words, {sum(sign_freqs.values())} tokens, {len(all_signs)} signs")

    lm = _build_lm()

    # ── 1. ASHRAF DIRECTIONAL ANALYSIS ──────────────────────────────────────
    _pr("\n  1. Ashraf (2018) Directional Analysis...")

    # Count sign occurrences at position 0 (leftmost in file) and position -1 (rightmost)
    pos0_counts  = Counter(w[0]  for w in words_ltr if w)
    posN1_counts = Counter(w[-1] for w in words_ltr if w)

    H_pos0  = _entropy(dict(pos0_counts))
    H_posN1 = _entropy(dict(posN1_counts))
    G_pos0  = _gini(dict(pos0_counts))
    G_posN1 = _gini(dict(posN1_counts))

    # Lower entropy = more constrained = true word-END
    # If H(pos0) < H(posN1): pos0 = word-END => reading is RTL (reading ends at left)
    if H_pos0 < H_posN1:
        inferred_direction = "RIGHT-TO-LEFT"
        confirmed = True
    else:
        inferred_direction = "LEFT-TO-RIGHT"
        confirmed = False

    _pr(f"  Position 0 (leftmost in file):   H={H_pos0:.4f} bits  Gini={G_pos0:.4f}")
    _pr(f"  Position -1 (rightmost in file): H={H_posN1:.4f} bits  Gini={G_posN1:.4f}")
    _pr(f"  Ashraf method infers reading direction: {inferred_direction}")
    _pr(f"  Consistent with Dr. Fuls' statement (RTL): {confirmed}")

    ashraf_result = {
        "entropy_position_0_leftmost":  round(H_pos0, 4),
        "entropy_position_N1_rightmost": round(H_posN1, 4),
        "gini_position_0":  round(G_pos0, 4),
        "gini_position_N1": round(G_posN1, 4),
        "inferred_direction": inferred_direction,
        "confirms_rtl": confirmed,
        "interpretation": (
            f"Position 0 (leftmost in file) has {'lower' if H_pos0 < H_posN1 else 'higher'} "
            f"entropy ({H_pos0:.4f}) than position -1 ({H_posN1:.4f}). "
            f"Per Ashraf & Sinha (2018), the more constrained end is the word-END. "
            f"This {'confirms' if confirmed else 'contradicts'} right-to-left reading."
        ),
    }

    # ── 2. CORRECTED POSITIONAL PROFILES ─────────────────────────────────────
    _pr("\n  2. Positional Profiles -- LTR (original, incorrect) vs RTL (corrected)...")

    prof_ltr = _positional_profiles(words_ltr, all_signs)
    prof_rtl = _positional_profiles(words_rtl, all_signs)

    # Highlight the most affected signs
    _pr("  Top signs showing largest I/T flip:")
    flip_delta = {}
    for s in all_signs:
        ltr = prof_ltr[s]
        rtl = prof_rtl[s]
        delta_T = abs(rtl["T"] - ltr["T"])
        delta_I = abs(rtl["I"] - ltr["I"])
        flip_delta[s] = max(delta_T, delta_I)

    top_flips = sorted(flip_delta, key=lambda s: -flip_delta[s])[:10]
    for s in top_flips:
        ltr = prof_ltr[s]
        rtl = prof_rtl[s]
        _pr(f"    Sign {s:>5} (n={sign_freqs.get(s,0):3d}): "
            f"LTR T={ltr['T']:.2f}/I={ltr['I']:.2f} -> "
            f"RTL T={rtl['T']:.2f}/I={rtl['I']:.2f}")

    # ── 3. CONDITION A: No anchors (RTL sequences) ────────────────────────────
    _pr(f"\n  3. Condition A -- No anchors, RTL-corrected sequences ({N_SEEDS} seeds)...")

    rng_a = random.Random(5500)
    _seeds_a = [rng_a.randint(0, 999999) for _ in range(N_SEEDS)]
    _words_rtl_a, _lm_a = words_rtl, lm  # capture for lambda
    maps_a = run_seeds_parallel(
        lambda s, _w=_words_rtl_a, _m=_lm_a: _run_mapping(_w, _m, s), _seeds_a
    )
    _pr(f"    {len(maps_a)}/{N_SEEDS} done (parallel)")

    cons_a = _consistency(maps_a, all_signs)
    mc_a   = _mean([v["consistency"] for v in cons_a.values()])
    hci_a  = sum(1 for v in cons_a.values() if v["consistency"] >= 0.75)
    plaus_a = _mean([_bigram_plaus(m, words_rtl, lm) for m in maps_a])
    modal_a = {s: cons_a[s]["modal"] for s in all_signs if cons_a[s]["modal"]}

    _pr(f"  Condition A: mean consistency={mc_a:.1%}  HCI={hci_a}/78  "
        f"bigram_plaus={plaus_a:.3f}")

    # ── 4. CONDITION B: Dr. Fuls' verified anchors (RTL sequences) ───────────
    _pr(f"\n  4. Condition B -- Fuls' verified anchors, RTL sequences ({N_SEEDS} seeds)...")
    _pr(f"     Anchors: {FULS_ANCHORS}")

    rng_b = random.Random(6600)
    _seeds_b = [rng_b.randint(0, 999999) for _ in range(N_SEEDS)]
    _words_rtl_b, _lm_b, _anch = words_rtl, lm, FULS_ANCHORS  # capture for lambda
    maps_b = run_seeds_parallel(
        lambda s, _w=_words_rtl_b, _m=_lm_b, _a=_anch: _run_mapping(_w, _m, s, anchors=_a),
        _seeds_b
    )
    _pr(f"    {len(maps_b)}/{N_SEEDS} done (parallel)")

    cons_b = _consistency(maps_b, all_signs)
    mc_b   = _mean([v["consistency"] for v in cons_b.values()])
    hci_b  = sum(1 for v in cons_b.values() if v["consistency"] >= 0.75)
    plaus_b = _mean([_bigram_plaus(m, words_rtl, lm) for m in maps_b])
    modal_b = {s: cons_b[s]["modal"] for s in all_signs if cons_b[s]["modal"]}

    _pr(f"  Condition B: mean consistency={mc_b:.1%}  HCI={hci_b}/78  "
        f"bigram_plaus={plaus_b:.3f}")

    # Highlight the anchor signs specifically
    _pr("\n  Anchor sign results in Condition B:")
    for sign, anchor_val in FULS_ANCHORS.items():
        cb = cons_b.get(sign, {})
        _pr(f"    Sign {sign}: anchored to {anchor_val!r}  "
            f"(consistency={cb.get('consistency',0):.0%}, top3={cb.get('top3',[])})")

    # Top-20 by consistency in Condition B
    _pr("\n  Top-20 signs by consistency (Condition B):")
    _pr(f"  {'Sign':>5}  {'RTL-I':>5}  {'RTL-T':>5}  {'Proposed':>9}  "
        f"{'Cons':>5}  {'Freq':>4}  {'Anchored'}")
    _pr("  " + "-" * 65)
    sorted_by_cons_b = sorted(all_signs,
                               key=lambda s: (-cons_b[s]["consistency"],
                                              -sign_freqs.get(s, 0)))
    for s in sorted_by_cons_b[:20]:
        cb = cons_b[s]
        pr = prof_rtl[s]
        anch = FULS_ANCHORS.get(s, "")
        _pr(f"  {s:>5}  {pr['I']:>5.3f}  {pr['T']:>5.3f}  "
            f"{cb.get('modal','?'):>9}  {cb.get('consistency',0)*100:>4.0f}%  "
            f"{sign_freqs.get(s,0):>4}  {'<-- ' + anch if anch else ''}")

    # ── 5. Comparison with original LTR ──────────────────────────────────────
    _pr("\n  5. Comparison: original LTR (incorrect) vs RTL corrected...")
    _pr(f"  Original LTR, no anchors:  mc=59.9%  (from fuls_nw_semitic_decipher_run)")
    _pr(f"  RTL corrected, no anchors: mc={mc_a:.1%}  HCI={hci_a}")
    _pr(f"  RTL corrected + anchors:   mc={mc_b:.1%}  HCI={hci_b}")

    ts  = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out = REPORTS / f"fuls_rtl_corrected_{ts}.json"

    result = {
        "reading_direction_correction": {
            "original_analysis_assumption": "LEFT-TO-RIGHT",
            "correct_reading_direction":    "RIGHT-TO-LEFT (confirmed by Dr. Fuls)",
            "correction_applied":           "All word sequences reversed before analysis",
        },
        "ashraf_directional_analysis": ashraf_result,
        "fuls_verified_anchors": FULS_ANCHORS,
        "positional_profile_comparison": {
            "n_signs_with_significant_flip": len(top_flips),
            "most_affected": [
                {
                    "sign": s,
                    "freq": sign_freqs.get(s, 0),
                    "ltr_I": prof_ltr[s]["I"],
                    "ltr_T": prof_ltr[s]["T"],
                    "rtl_I": prof_rtl[s]["I"],
                    "rtl_T": prof_rtl[s]["T"],
                    "flip_delta": round(flip_delta[s], 3),
                }
                for s in top_flips
            ],
            "profiles_rtl": {s: prof_rtl[s] for s in all_signs},
        },
        "condition_a_no_anchors_rtl": {
            "n_seeds": N_SEEDS,
            "mean_consistency": round(mc_a, 4),
            "hci_count": hci_a,
            "bigram_plausibility": round(plaus_a, 4),
            "modal_mapping": modal_a,
            "consistency_per_sign": {s: cons_a[s] for s in all_signs},
        },
        "condition_b_fuls_anchors_rtl": {
            "n_seeds": N_SEEDS,
            "anchors_used": FULS_ANCHORS,
            "mean_consistency": round(mc_b, 4),
            "hci_count": hci_b,
            "bigram_plausibility": round(plaus_b, 4),
            "modal_mapping": modal_b,
            "consistency_per_sign": {s: cons_b[s] for s in all_signs},
        },
        "comparison": {
            "original_ltr_no_anchors_mc": 0.599,
            "rtl_corrected_no_anchors_mc": round(mc_a, 4),
            "rtl_corrected_with_anchors_mc": round(mc_b, 4),
            "improvement_from_rtl_correction_pp": round((mc_a - 0.599) * 100, 2),
            "improvement_from_anchors_pp": round((mc_b - mc_a) * 100, 2),
        },
        "vowel_model_note": (
            "Hebrew is a consonant-only (abjad) writing system. The test1 corpus is "
            "syllabic (CV pairs). The surjective (many-to-one) SA mapping correctly "
            "handles this: multiple signs with the same consonant but different vowels "
            "(e.g., MA, MI, MU) all map to the same target consonant (/m/). "
            "However, the Hebrew LM cannot model vowel harmony or vowel sequence "
            "patterns. A vocalized Hebrew or another syllabic reference language "
            "would improve accuracy. The consonantal skeleton model remains the "
            "primary signal for NW Semitic morphological constraints."
        ),
    }

    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    _pr(f"\n  Saved -> {out}")
    return result


if __name__ == "__main__":
    from glossa_lab.cli_bridge import run_with_reporting
    run_with_reporting(
        "fuls_rtl_corrected",
        "Fuls NW Semitic -- RTL Correction and Verified Anchor Experiment",
        run_rtl_corrected, verbose=True,
    )


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class FulsRTLCorrected(_EB):
    id             = "fuls_rtl_corrected"
    name           = "Fuls NW Semitic -- RTL Correction and Verified Anchor Experiment"
    category       = "Validation"
    description    = (
        "Corrects the reading direction error: reverses all word sequences (RTL), "
        "confirms RTL using Ashraf (2018) handedness entropy method, "
        "recomputes positional profiles, and runs mapping inference under "
        "(A) no anchors and (B) Dr. Fuls' verified anchors: "
        "004=T, 066=M, 208=N, 133=ayin, 128=L, 080=W."
    )
    estimated_time = "~10-15 min"
    command        = "python -m glossa_lab.experiments.fuls_rtl_corrected"

    def run(self, **kwargs) -> dict:
        return run_rtl_corrected(verbose=False)
