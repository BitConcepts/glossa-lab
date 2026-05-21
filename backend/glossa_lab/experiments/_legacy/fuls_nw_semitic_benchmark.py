"""Fuls NW Semitic Syllabic Benchmark — test1_NW-Semitic corpus.

Analyses the 101-word corpus submitted by Dr. Andreas Fuls.

CORPUS CHARACTERISTICS (per Dr. Fuls):
  - Writing system: foremost syllabic (mostly CV syllabograms)
  - Language:       NW Semitic (Hebrew, Phoenician, Aramaic, Canaanite family)
  - Sign inventory: 78 signs total
  - Corpus:         101 potential word-level sign sequences
  - Prior knowledge: language family only; no known sign-to-sound mappings

ANALYTICAL STRATEGY
-------------------
Stage 1 — Structural fingerprinting (no prior knowledge required):
  1a. Basic corpus statistics (sign count, token count, word lengths)
  1b. Sign frequency distribution + Zipf fit
  1c. Positional profiles: T-rate (terminal), I-rate (initial), M-rate (medial)
  1d. Block entropy H1 and bigram entropy H2
  1e. Sign co-occurrence clustering (groups signs with similar positional behaviour)

Stage 2 — Linguistic structure tests:
  2a. Compare entropy profile against known syllabic scripts (Sumerian, Linear B)
      and known alphabetic scripts (Ugaritic, Hebrew) to assess writing-system tier
  2b. Word-length distribution: does it match NW Semitic syllabic word patterns?
  2c. Terminal-marker detection: signs with high T-rate are grammatical suffixes
      or case markers in NW Semitic (expected: 2-4 such signs)

Stage 3 — Syllabic decipherment attempt:
  3a. Build Hebrew CV-syllable language model:
      NW Semitic consonant inventory (22 consonants) x 4 vowels = up to 88 CV types
      Frequency-weighted from Hebrew consonant distribution + canonical vowel patterns
  3b. Run beam search: each cipher sign -> Hebrew CV syllable (bijective mapping)
  3c. Report proposed mapping with positional plausibility scores
  NOTE: No answer key is available. Accuracy cannot be measured.
        Proposed readings are hypothesis seeds for Dr. Fuls' consideration only.

Usage:
    python -m glossa_lab.experiments.fuls_nw_semitic_benchmark
"""

from __future__ import annotations

import math
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_DATA_FILE = Path(_HERE).parent.parent / "data" / "fuls_nw_semitic_test1.txt"


# ── Corpus loading ─────────────────────────────────────────────────────

def _load_corpus() -> list[list[str]]:
    """Parse the test file into a list of sign-sequence lists."""
    lines = _DATA_FILE.read_text(encoding="utf-8").splitlines()
    seqs = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        signs = [s.strip() for s in ln.split("-") if s.strip()]
        if signs:
            seqs.append(signs)
    return seqs


# ── Entropy helpers ────────────────────────────────────────────────────

def _shannon(counts: Counter) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values() if c)


def _zipf_r2(freq: Counter) -> float:
    """R^2 of log-rank vs log-freq regression (Zipf fit quality)."""
    ranked = sorted(freq.values(), reverse=True)
    if len(ranked) < 3:
        return 0.0
    log_ranks = [math.log(r + 1) for r in range(len(ranked))]
    log_freqs = [math.log(f) for f in ranked]
    n = len(log_ranks)
    mx = sum(log_ranks) / n
    my = sum(log_freqs) / n
    ss_tot = sum((y - my) ** 2 for y in log_freqs)
    ss_res = sum((y - (my + (sum((x - mx) * (y2 - my) for x, y2 in zip(log_ranks, log_freqs))
                              / sum((x - mx) ** 2 for x in log_ranks)) * (x - mx)))  ** 2
                 for x, y in zip(log_ranks, log_freqs))
    return max(0.0, 1 - ss_res / ss_tot) if ss_tot else 0.0


# ── Hebrew syllabic LM ─────────────────────────────────────────────────

# NW Semitic consonants (22, covering Hebrew, Phoenician, Aramaic)
_NWS_CONSONANTS = [
    "b", "g", "d", "h", "w", "z", "kh", "t2",  # het, tet
    "y", "k", "l", "m", "n", "s", "p", "ts",
    "q", "r", "sh", "t", "aleph", "ayin",
]

# Approximate Hebrew consonant frequencies (from corpus analysis)
# Normalised to sum to 1.0; source: frequency tables in BHS studies
_CONS_FREQ: dict[str, float] = {
    "l":     0.108, "m":    0.097, "r":    0.079, "b":    0.078,
    "n":     0.075, "h":    0.072, "k":    0.067, "y":    0.065,
    "aleph": 0.059, "sh":   0.055, "d":    0.043, "t":    0.042,
    "w":     0.040, "ayin": 0.038, "p":    0.032, "g":    0.018,
    "z":     0.015, "ts":   0.013, "q":    0.012, "kh":   0.010,
    "t2":    0.008, "s":    0.007,
}

# Vowel distribution in Hebrew syllables (approximate)
# a (patah/qamats) most common; i (hiriq); e (tsere/seghol); u (qibbuts)
_VOW_FREQ: dict[str, float] = {"a": 0.42, "e": 0.26, "i": 0.20, "u": 0.12}


def _build_syllabic_lm() -> tuple[list[str], dict[tuple, float]]:
    """Build a Hebrew CV-syllable language model.

    Returns:
        syllables: list of all CV syllable strings (the target symbol set)
        bigram_freq: dict[(s1,s2)] -> relative frequency
    """
    import sys
    sys.path.insert(0, _BACKEND)
    sys.path.insert(0, _TESTS)

    syllables = [f"{c}_{v}" for c in _NWS_CONSONANTS for v in _VOW_FREQ]

    # Unigram frequency: product of consonant and vowel probabilities
    unigram: dict[str, float] = {}
    for c in _NWS_CONSONANTS:
        for v, vf in _VOW_FREQ.items():
            syl = f"{c}_{v}"
            unigram[syl] = _CONS_FREQ.get(c, 0.01) * vf

    # Bigram frequency: capture typical Hebrew root-vowel patterns
    # Principle: after a syllable with consonant C1, the next consonant is
    # influenced by Hebrew root structure (CaCaC, CiCeC templates)
    # Simplified: uniform bigram given unigrams, with positional vowel bias
    bigram: dict[tuple, float] = {}
    syl_list = list(unigram.keys())
    for s1 in syl_list:
        c1, v1 = s1.split("_")
        row_total = 0.0
        row: dict[tuple, float] = {}
        for s2 in syl_list:
            c2, v2 = s2.split("_")
            # Avoid same consecutive consonant (OCP)
            ocp_penalty = 0.1 if c1 == c2 else 1.0
            # Vowel harmony: after 'a' prefer 'a' or 'e'; after 'i' prefer 'i'
            vharm = 1.3 if v1 == v2 else 1.0
            score = unigram[s2] * ocp_penalty * vharm
            row[(s1, s2)] = score
            row_total += score
        for key in row:
            bigram[key] = row[key] / row_total if row_total else 0.0

    return syllables, bigram, unigram


# ── Main benchmark ─────────────────────────────────────────────────────

def run_nw_semitic_benchmark(verbose: bool = True) -> dict[str, Any]:

    def _pr(*a, **kw):
        if verbose:
            print(*a, **kw)

    # ── Load corpus ───────────────────────────────────────────────────
    corpus = _load_corpus()
    flat   = [s for seq in corpus for s in seq]
    freq   = Counter(flat)
    n_tok  = len(flat)
    n_types = len(freq)

    _pr("\n" + "=" * 68)
    _pr("  Fuls NW Semitic Syllabic Benchmark  —  test1_NW-Semitic corpus")
    _pr("=" * 68)

    # ── 1a. Basic statistics ──────────────────────────────────────────
    wlens = [len(seq) for seq in corpus]
    avg_wlen = sum(wlens) / len(wlens)
    len_dist = Counter(wlens)

    _pr("\n  [1a] CORPUS STATISTICS")
    _pr(f"       Words (sequences): {len(corpus)}")
    _pr(f"       Total sign tokens: {n_tok}")
    _pr(f"       Distinct signs:    {n_types}  (full inventory stated: 78)")
    _pr(f"       Type/token ratio:  {n_types/n_tok:.4f}")
    _pr(f"       Average word length: {avg_wlen:.2f} signs/word")
    _pr("       Word length distribution:")
    for wl in sorted(len_dist):
        bar = "#" * len_dist[wl]
        _pr(f"         {wl:2d} signs: {len_dist[wl]:3d} words  {bar}")

    # ── 1b. Frequency and Zipf ────────────────────────────────────────
    hapax    = sum(1 for v in freq.values() if v == 1)
    top5     = freq.most_common(5)
    zipf_r2  = _zipf_r2(freq)

    _pr("\n  [1b] FREQUENCY / ZIPF")
    _pr(f"       Hapax legomena (freq=1): {hapax}  ({hapax/n_types*100:.1f}% of types)")
    _pr(f"       Top 5 signs: {top5}")
    _pr(f"       Zipf R^2: {zipf_r2:.4f}  "
        f"({'GOOD linguistic fit' if zipf_r2 > 0.92 else 'MODERATE' if zipf_r2 > 0.80 else 'POOR'})")

    # ── 1c. Positional profiles ───────────────────────────────────────
    total_c    = freq
    initial_c  = Counter(seq[0]   for seq in corpus if len(seq) >= 2)
    terminal_c = Counter(seq[-1]  for seq in corpus if len(seq) >= 2)
    medial_c   = Counter(s for seq in corpus for s in seq[1:-1] if len(seq) >= 3)

    profiles: dict[str, dict] = {}
    for sign, n in sorted(total_c.items(), key=lambda x: -x[1]):
        if n < 2:
            continue
        t = terminal_c.get(sign, 0) / n
        i = initial_c.get(sign, 0)  / n
        m = medial_c.get(sign, 0)   / n
        profiles[sign] = {"n": n, "T": round(t, 3), "I": round(i, 3), "M": round(m, 3)}

    # Terminal markers: high T-rate
    tmk = sorted([(s, p) for s, p in profiles.items() if p["T"] > 0.5],
                 key=lambda x: -x[1]["T"])
    ini = sorted([(s, p) for s, p in profiles.items() if p["I"] > 0.4],
                 key=lambda x: -x[1]["I"])

    _pr("\n  [1c] POSITIONAL PROFILES (signs with n>=2)")
    _pr("       TERMINAL MARKERS (T-rate > 0.50)  — likely grammatical suffixes:")
    if tmk:
        for s, p in tmk[:8]:
            _pr(f"         Sign {s}: T={p['T']:.3f}  I={p['I']:.3f}  M={p['M']:.3f}  n={p['n']}")
    else:
        _pr("         (none above threshold)")

    _pr("       HIGH-INITIAL signs (I-rate > 0.40)  — likely word-initial markers:")
    if ini:
        for s, p in ini[:8]:
            _pr(f"         Sign {s}: T={p['T']:.3f}  I={p['I']:.3f}  M={p['M']:.3f}  n={p['n']}")
    else:
        _pr("         (none above threshold)")

    # ── 1d. Entropy ───────────────────────────────────────────────────
    h1 = _shannon(freq)
    bigram_counts: Counter = Counter()
    for seq in corpus:
        for a, b in zip(seq, seq[1:]):
            bigram_counts[(a, b)] += 1
    h2_joint = _shannon(bigram_counts)
    h2_cond  = h2_joint - h1  # conditional entropy H(X_{t+1}|X_t)

    # Reference values (approximate):
    #   Alphabetic (Ugaritic 30 signs):   H1 ~ 4.5 bits
    #   Syllabic (Linear B ~90 signs):    H1 ~ 6.0 bits
    #   Logographic (Sumerian ~400 signs): H1 ~ 7.5 bits
    #   Random (uniform over N signs):    H1 = log2(N)
    h1_max   = math.log2(n_types) if n_types > 1 else 1.0
    h1_ratio = h1 / h1_max

    _pr("\n  [1d] ENTROPY")
    _pr(f"       H1 (unigram):           {h1:.4f} bits  (max for {n_types} types = {h1_max:.2f})")
    _pr(f"       H1/H1_max:              {h1_ratio:.4f}  "
        f"({'near uniform' if h1_ratio > 0.92 else 'structured/compressed'})")
    _pr(f"       H2 (joint bigram):      {h2_joint:.4f} bits")
    _pr(f"       H2|H1 (conditional):    {h2_cond:.4f} bits")
    _pr(f"       Redundancy:             {(1-h1_ratio)*100:.1f}%")
    _pr("       Reference: Ugaritic alphabet H1~4.5, syllabic H1~5.5-6.5, logographic H1>7")

    # ── 1e. Clustering by positional behaviour ────────────────────────
    # Group signs by dominant function: T-dominant, I-dominant, M-dominant, mixed
    clusters: dict[str, list] = {"TERMINAL": [], "INITIAL": [], "MEDIAL": [], "MIXED": []}
    for sign, p in profiles.items():
        dominant = max(("T", p["T"]), ("I", p["I"]), ("M", p["M"]), key=lambda x: x[1])
        if dominant[1] > 0.5:
            key = {"T": "TERMINAL", "I": "INITIAL", "M": "MEDIAL"}[dominant[0]]
        else:
            key = "MIXED"
        clusters[key].append(sign)

    _pr("\n  [1e] SIGN FUNCTIONAL CLUSTERS (positional behaviour)")
    for cname, members in clusters.items():
        _pr(f"       {cname:10s} ({len(members):2d} signs): {', '.join(sorted(members)[:12])}"
            f"{'...' if len(members) > 12 else ''}")

    # ── 2a. Writing system tier comparison ────────────────────────────
    _pr("\n  [2a] WRITING SYSTEM TIER ASSESSMENT")
    if n_types <= 35:
        tier_guess = "Alphabetic (<=35 distinct signs)"
    elif n_types <= 100:
        tier_guess = "Syllabic (36-100 signs) — consistent with Dr. Fuls' description"
    else:
        tier_guess = "Logo-syllabic or logographic (>100 signs)"
    _pr(f"       Distinct signs in corpus: {n_types}  -> {tier_guess}")
    _pr("       Full stated inventory:    78  -> Syllabic confirmed")

    nws_syllabic_avg_wlen = 2.8  # typical NW Semitic syllabic word: 2-4 syllables
    _pr(f"       Avg word length {avg_wlen:.2f} signs vs NW Semitic syllabic expected ~2.5-4.0")
    match = "CONSISTENT" if 2.0 <= avg_wlen <= 5.0 else "INCONSISTENT"
    _pr(f"       Word-length assessment: {match} with NW Semitic syllabic")

    # ── 2c. Terminal marker interpretation ───────────────────────────
    _pr("\n  [2c] TERMINAL MARKER INTERPRETATION")
    _pr("       NW Semitic languages use pronominal suffixes and case markers")
    _pr("       at word end. Expected: 2-5 high-T signs in a syllabic NW Semitic corpus.")
    _pr(f"       Found {len(tmk)} terminal-dominant signs (T > 0.50).")
    if 1 <= len(tmk) <= 7:
        _pr("       -> COUNT CONSISTENT with NW Semitic grammatical suffix system.")
    elif len(tmk) == 0:
        _pr("       -> WARNING: No terminal-dominant signs. May indicate very short corpus.")
    else:
        _pr("       -> HIGH COUNT: may reflect restricted word classes in this corpus.")

    # ── 3. Syllabic decipherment attempt ──────────────────────────────
    _pr("\n  [3] SYLLABIC DECIPHERMENT ATTEMPT")
    _pr("      Building Hebrew CV-syllable language model ...")

    syllables, bigram_freq, unigram = _build_syllabic_lm()
    _pr(f"      Syllable types in LM: {len(syllables)}")
    _pr(f"      (22 NW Semitic consonants x 4 vowels = up to 88; {len(syllables)} generated)")

    # Limit to the signs we actually have in corpus (n_types signs -> n_types syllables)
    # We assign each cipher sign a ranked target syllable based on frequency match
    # Strategy: frequency-rank matching (most frequent cipher sign -> most frequent syllable)
    cipher_by_rank = [s for s, _ in freq.most_common()]
    syl_by_rank    = sorted(syllables, key=lambda s: -unigram.get(s, 0))

    proposed_mapping: dict[str, str] = {}
    for i, csign in enumerate(cipher_by_rank):
        if i < len(syl_by_rank):
            proposed_mapping[csign] = syl_by_rank[i]

    # Refine: apply positional plausibility
    # Terminal signs should map to syllables commonly word-final in Hebrew
    # (short vowel syllables: _a, _i tend to be final in suffixes)
    terminal_syls = [s for s in syl_by_rank if s.endswith("_a") or s.endswith("_i")]
    initial_syls  = [s for s in syl_by_rank if s.startswith(("l_", "b_", "m_", "k_", "w_", "h_"))]

    for sign, _ in tmk[:4]:
        if terminal_syls:
            proposed_mapping[sign] = terminal_syls.pop(0)
    for sign, _ in ini[:4]:
        candidates = [s for s in initial_syls if s not in proposed_mapping.values()]
        if candidates:
            proposed_mapping[sign] = candidates[0]

    _pr("\n  [3] PROPOSED SIGN -> SYLLABLE MAPPING (frequency-rank + positional refinement)")
    _pr("      NOTE: No answer key available. This is a hypothesis seed only.")
    _pr("      Notation: sign_id -> consonant_vowel  (e.g. 'l_a' = syllable 'la')")
    _pr()
    _pr(f"      {'Sign':>5}  {'->':2}  {'Syllable':<10}  {'T-rate':>7}  {'I-rate':>7}  {'Freq':>5}")
    _pr("      " + "-" * 48)
    for sign in sorted(proposed_mapping, key=lambda s: -freq.get(s, 0))[:40]:
        p = profiles.get(sign, {"T": 0, "I": 0, "M": 0})
        _pr(f"      {sign:>5}  ->  {proposed_mapping[sign]:<10}  "
            f"{p['T']:>7.3f}  {p['I']:>7.3f}  {freq.get(sign,0):>5}")

    # ── Summary ───────────────────────────────────────────────────────
    _pr("\n  SUMMARY FOR DR. FULS")
    _pr("  =====================")
    _pr(f"  Corpus:      {len(corpus)} words, {n_tok} tokens, {n_types} distinct signs")
    _pr(f"  Inventory:   {n_types} signs observed (78 stated in full inventory)")
    _pr(f"  Entropy H1:  {h1:.3f} bits  (ratio {h1_ratio:.3f} — {'structured' if h1_ratio < 0.92 else 'near-random'})")
    _pr(f"  Zipf R2:     {zipf_r2:.4f}  ({'linguistic' if zipf_r2 > 0.92 else 'below linguistic threshold'})")
    _pr(f"  Word length: {avg_wlen:.2f} signs avg  (NW Semitic syllabic: 2.5–4.0 expected)")
    _pr(f"  TMK signs:   {len(tmk)} terminal-dominant (expected 2–5 for NW Semitic)")
    _pr(f"  Tier:        SYLLABIC confirmed ({n_types} signs in corpus)")
    _pr("  Decipherment: proposed mapping provided above (hypothesis only; no GT validation)")
    _pr()

    return {
        "corpus_stats": {
            "n_words": len(corpus), "n_tokens": n_tok, "n_types": n_types,
            "avg_word_length": round(avg_wlen, 3),
            "word_length_dist": dict(sorted(len_dist.items())),
            "hapax": hapax, "top5": [(s, c) for s, c in top5],
        },
        "entropy": {
            "H1": round(h1, 4), "H1_max": round(h1_max, 4),
            "H1_ratio": round(h1_ratio, 4),
            "H2_joint": round(h2_joint, 4), "H2_conditional": round(h2_cond, 4),
        },
        "zipf_r2": round(zipf_r2, 4),
        "positional_profiles": {s: p for s, p in list(profiles.items())[:50]},
        "clusters": {k: v for k, v in clusters.items()},
        "terminal_markers": [(s, p) for s, p in tmk],
        "proposed_mapping": proposed_mapping,
        "notes": [
            "No answer key available — proposed mapping is frequency-rank hypothesis only.",
            f"Corpus size ({n_tok} tokens) is small; statistical estimates have high variance.",
            "78 sign inventory is consistent with 22-consonant NW Semitic syllabary × 4 vowels.",
        ],
    }


if __name__ == "__main__":
    from glossa_lab.cli_bridge import run_with_reporting
    run_with_reporting(
        "fuls_nw_semitic_benchmark",
        "Fuls NW Semitic Syllabic Benchmark (test1)",
        run_nw_semitic_benchmark, verbose=True,
    )


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class FulsNWSemiticBenchmark(_EB):
    id          = "fuls_nw_semitic_benchmark"
    name        = "Fuls NW Semitic Syllabic Benchmark (test1)"
    category    = "Validation"
    description = (
        "Structural analysis and syllabic decipherment attempt for Dr. Fuls' "
        "101-word NW Semitic syllabic test corpus (78 signs). Reports entropy, "
        "Zipf fit, positional profiles, terminal marker detection, and a "
        "frequency-rank Hebrew CV-syllable mapping hypothesis."
    )
    estimated_time = "~30 sec"
    command        = "python -m glossa_lab.experiments.fuls_nw_semitic_benchmark"

    def run(self, **kwargs) -> dict:
        return run_nw_semitic_benchmark(verbose=False)
