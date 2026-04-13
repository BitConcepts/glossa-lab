"""Fuls NW Semitic N-gram & Pattern Analysis — test1_NW-Semitic corpus.

Complements fuls_nw_semitic_benchmark.py with deeper sign-level analysis:

  1. Repeated word forms  — exact sign sequences that occur more than once.
     These are the HIGHEST PRIORITY for decipherment: a sequence that appears
     5 times in 101 words is likely a common NW Semitic word (verb, noun, preposition).

  2. Sign bigram network  — which sign pairs appear most often adjacently.
     Frequent bigrams = likely syllable pairs within morphemes.
     Anti-correlations (pairs that never co-occur) = OCP evidence.

  3. Sign co-occurrence graph — which signs appear WITHIN the same word.
     Signs that always share words may belong to the same morphological unit.

  4. Morpheme-family clustering — group signs by their positional profile
     L1 distance, revealing likely same-consonant different-vowel families
     (e.g., signs ba/be/bi/bu would cluster together).

  5. Sign sequence templates — categorise each word by its T/I/M pattern
     (e.g., I-M-T = initial + medial + terminal) and count template types.
     NW Semitic CVC nouns -> I-T, CVCVC verbs -> I-M-T, etc.

Usage:
    python -m glossa_lab.experiments fuls_nw_semitic_ngram
    python -m glossa_lab.experiments.fuls_nw_semitic_ngram
"""
from __future__ import annotations

import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_DATA_FILE = Path(_HERE).parent / "data" / "fuls_nw_semitic_test1.txt"


def _load_corpus() -> list[list[str]]:
    lines = _DATA_FILE.read_text(encoding="utf-8").splitlines()
    return [
        [s.strip() for s in ln.split("-") if s.strip()]
        for ln in lines if ln.strip()
    ]


def run_nw_semitic_ngram(verbose: bool = True) -> dict[str, Any]:

    def _pr(*a, **kw):
        if verbose:
            print(*a, **kw)

    corpus = _load_corpus()
    flat   = [s for seq in corpus for s in seq]
    freq   = Counter(flat)

    # Positional profiles (needed for clustering)
    initial_c  = Counter(seq[0]  for seq in corpus if len(seq) >= 2)
    terminal_c = Counter(seq[-1] for seq in corpus if len(seq) >= 2)
    medial_c   = Counter(s for seq in corpus for s in seq[1:-1] if len(seq) >= 3)

    def _profile(sign):
        n = freq[sign]
        if n == 0:
            return (0.0, 0.0, 0.0)
        return (terminal_c[sign]/n, initial_c[sign]/n, medial_c[sign]/n)

    _pr("\n" + "=" * 68)
    _pr("  Fuls NW Semitic N-gram & Pattern Analysis — test1_NW-Semitic")
    _pr("=" * 68)

    # ── 1. Repeated word forms ────────────────────────────────────────
    word_counter: Counter = Counter(tuple(seq) for seq in corpus)
    repeated = [(list(seq), cnt) for seq, cnt in word_counter.most_common()
                if cnt >= 2]

    _pr(f"\n  [1] REPEATED WORD FORMS (sequences occurring >= 2 times)")
    _pr(f"      Total distinct word forms:   {len(word_counter)}")
    _pr(f"      Repeated forms (n>=2):        {len(repeated)}")
    _pr(f"      Singleton forms (n=1):        {sum(1 for _,c in word_counter.items() if c==1)}")
    _pr()
    _pr(f"      {'Count':>5}  Sequence")
    _pr("      " + "-" * 40)
    for seq, cnt in sorted(repeated, key=lambda x: -x[1])[:20]:
        _pr(f"      {cnt:>5}x  {'-'.join(seq)}")
    if len(repeated) > 20:
        _pr(f"      ... and {len(repeated)-20} more")

    # ── 2. Sign bigram network ────────────────────────────────────────
    bigrams: Counter = Counter()
    never_adjacent: set = set()
    all_signs = sorted(freq.keys())

    for seq in corpus:
        for a, b in zip(seq, seq[1:]):
            bigrams[(a, b)] += 1

    top_bigrams = bigrams.most_common(20)

    # Anti-correlations: pairs that NEVER appear adjacent despite both being frequent
    frequent_signs = {s for s, n in freq.items() if n >= 4}
    never_adj = []
    for s1 in frequent_signs:
        for s2 in frequent_signs:
            if s1 != s2 and bigrams[(s1, s2)] == 0 and bigrams[(s2, s1)] == 0:
                pair = tuple(sorted([s1, s2]))
                never_adj.append(pair)
    never_adj = list(set(never_adj))

    _pr(f"\n  [2] SIGN BIGRAM NETWORK")
    _pr(f"      Total bigram types: {len(bigrams)}")
    _pr(f"      Top 20 adjacent pairs:")
    _pr(f"      {'Count':>5}  Pair")
    _pr("      " + "-" * 30)
    for (a, b), cnt in top_bigrams:
        _pr(f"      {cnt:>5}x  {a}-{b}")

    _pr(f"\n      OCP ANTI-CORRELATIONS (frequent signs never adjacent, n>={4}):")
    _pr(f"      {len(never_adj)} pairs never appear adjacent.")
    _pr(f"      (These constrain possible consonant assignments: two signs that")
    _pr(f"       never co-occur cannot share a consonant family if OCP applies.)")
    for pair in sorted(never_adj)[:12]:
        _pr(f"        {pair[0]} <-> {pair[1]}")

    # ── 3. Sign co-occurrence within words ────────────────────────────
    cooccur: Counter = Counter()
    for seq in corpus:
        signs_in_word = set(seq)
        for s1 in signs_in_word:
            for s2 in signs_in_word:
                if s1 < s2:
                    cooccur[(s1, s2)] += 1

    top_cooccur = cooccur.most_common(15)
    _pr(f"\n  [3] SIGN CO-OCCURRENCE WITHIN WORDS (top 15 pairs)")
    _pr(f"      {'Count':>5}  Pair  (appear in same word)")
    _pr("      " + "-" * 35)
    for (a, b), cnt in top_cooccur:
        _pr(f"      {cnt:>5}x  {a} + {b}")

    # ── 4. Positional clustering (morpheme families) ──────────────────
    # L1 distance between positional profiles — signs that cluster together
    # likely share consonant family (same C, different V) in a syllabary
    profiles = {s: _profile(s) for s in freq if freq[s] >= 2}

    def _l1(p1, p2):
        return sum(abs(a - b) for a, b in zip(p1, p2))

    # Greedy clustering: assign each sign to nearest existing cluster centre
    # or start a new cluster if distance > threshold
    THRESHOLD = 0.25
    clusters: list[list[str]] = []
    centres:  list[tuple]     = []

    for sign in sorted(profiles, key=lambda s: -freq[s]):
        prof = profiles[sign]
        best_idx, best_dist = -1, float("inf")
        for i, c in enumerate(centres):
            d = _l1(prof, c)
            if d < best_dist:
                best_dist, best_idx = d, i
        if best_dist <= THRESHOLD:
            clusters[best_idx].append(sign)
            # Update centre to mean
            n = len(clusters[best_idx])
            old = centres[best_idx]
            centres[best_idx] = tuple((old[k]*(n-1) + prof[k]) / n for k in range(3))
        else:
            clusters.append([sign])
            centres.append(prof)

    # Sort clusters by size
    clusters_sorted = sorted(
        [(c, ctr) for c, ctr in zip(clusters, centres) if len(c) >= 2],
        key=lambda x: -len(x[0])
    )

    _pr(f"\n  [4] MORPHEME FAMILY CLUSTERS (signs with similar T/I/M profiles)")
    _pr(f"      Signs within a cluster likely share a consonant (differ by vowel only).")
    _pr(f"      Threshold: L1 distance <= {THRESHOLD}")
    _pr(f"      Clusters with >= 2 members: {len(clusters_sorted)}")
    _pr()
    for i, (members, ctr) in enumerate(clusters_sorted[:12]):
        t, iv, m = ctr
        dom = "TERM" if t > 0.5 else "INIT" if iv > 0.5 else "MED" if m > 0.5 else "MIX"
        mstr = ", ".join(f"{s}(n={freq[s]})" for s in members)
        _pr(f"      Cluster {i+1:2d} [{dom}] T={t:.2f} I={iv:.2f} M={m:.2f}: {mstr}")

    # ── 5. Word sequence templates ────────────────────────────────────
    def _template(seq):
        parts = []
        for j, s in enumerate(seq):
            t, iv, m = _profile(s)
            if j == 0 and j == len(seq)-1:
                parts.append("S")   # single-sign word
            elif j == 0:
                dom = "I" if iv >= t and iv >= m else ("T" if t >= m else "M")
                parts.append(dom)
            elif j == len(seq)-1:
                dom = "T" if t >= iv and t >= m else ("I" if iv >= m else "M")
                parts.append(dom)
            else:
                dom = "M" if m >= t and m >= iv else ("I" if iv >= t else "T")
                parts.append(dom)
        return "-".join(parts)

    templates = Counter(_template(seq) for seq in corpus)

    _pr(f"\n  [5] WORD SEQUENCE TEMPLATES (I=initial, M=medial, T=terminal)")
    _pr(f"      Expected NW Semitic patterns: I-T (biconsonantal), I-M-T (triconsonantal),")
    _pr(f"      I-M-M-T (4-consonant or CVVC), etc.")
    _pr()
    _pr(f"      {'Count':>5}  Template")
    _pr("      " + "-" * 28)
    for tmpl, cnt in templates.most_common(15):
        _pr(f"      {cnt:>5}x  {tmpl}")

    # ── Summary ───────────────────────────────────────────────────────
    most_repeated = repeated[0] if repeated else ([], 0)
    _pr(f"\n  SUMMARY FOR DR. FULS")
    _pr(f"  ====================")
    _pr(f"  Most frequent word form: {'-'.join(most_repeated[0])} (x{most_repeated[1]})")
    _pr(f"  Repeated forms:         {len(repeated)} of {len(word_counter)} distinct words")
    _pr(f"  Top bigram:             {'-'.join(top_bigrams[0][0])} (x{top_bigrams[0][1]})")
    _pr(f"  Morpheme clusters:      {len(clusters_sorted)} families of >= 2 signs")
    _pr(f"  Most common template:   {templates.most_common(1)[0]}")
    _pr(f"\n  RECOMMENDED PRIORITY TARGETS FOR ANCHOR ASSIGNMENT:")
    _pr(f"  The following repeated sequences should be matched first to known NW Semitic words:")
    for seq, cnt in sorted(repeated, key=lambda x: -x[1])[:5]:
        _pr(f"    {'-'.join(seq)} (x{cnt}) — {len(seq)}-sign word, "
            f"template={_template(seq)}")

    return {
        "repeated_word_forms": [
            {"sequence": seq, "count": cnt} for seq, cnt in repeated
        ],
        "top_bigrams": [
            {"pair": list(pair), "count": cnt} for pair, cnt in top_bigrams
        ],
        "ocp_anti_correlations": [list(p) for p in sorted(never_adj)[:30]],
        "top_cooccurrences": [
            {"pair": list(pair), "count": cnt} for pair, cnt in top_cooccur
        ],
        "morpheme_clusters": [
            {
                "members": members,
                "centre_T": round(ctr[0], 3),
                "centre_I": round(ctr[1], 3),
                "centre_M": round(ctr[2], 3),
            }
            for members, ctr in clusters_sorted
        ],
        "word_templates": dict(templates.most_common()),
        "corpus_size": len(corpus),
    }


if __name__ == "__main__":
    from glossa_lab.cli_bridge import run_with_reporting
    run_with_reporting(
        "fuls_nw_semitic_ngram",
        "Fuls NW Semitic N-gram & Pattern Analysis",
        run_nw_semitic_ngram, verbose=True,
    )


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class FulsNWSemiticNgram(_EB):
    id          = "fuls_nw_semitic_ngram"
    name        = "Fuls NW Semitic N-gram & Pattern Analysis"
    category    = "Validation"
    description = (
        "Deep sign-level analysis of Dr. Fuls' NW Semitic syllabic test corpus: "
        "repeated word forms (priority decipherment targets), sign bigram network, "
        "OCP anti-correlations, co-occurrence clustering, morpheme family groups, "
        "and word template classification (I-M-T patterns)."
    )
    estimated_time = "~5 sec"
    command        = "python -m glossa_lab.experiments fuls_nw_semitic_ngram"

    def run(self, **kwargs) -> dict:
        return run_nw_semitic_ngram(verbose=False)
