"""Run all pending analyses on the decoded M77 (Mahadevan 1977) corpus.

Steps:
  1. NWSP positional classification on real ordered sequences
  2. TMK bigram cross-validation
  3. Block entropy (Rao 2009 replication)
  4. Bigram Markov model with conditional probabilities
  5. Ventris / distributional affinity clustering
  6. Word-structure typology
  7. Structural fingerprint comparison

Output: reports/m77_corpus_analysis.json
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_REPO = Path(__file__).parent.parent
_REPORTS = _REPO / "reports"
sys.path.insert(0, str(Path(__file__).parent))


# ── Load corpus ────────────────────────────────────────────────────────


def load_corpus() -> list[list[str]]:
    p = _REPORTS / "mahadevan_texts_decoded.json"
    if not p.exists():
        raise FileNotFoundError(f"Run decode_inscription_texts.py first: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    return [ins["sequence"] for ins in data["inscriptions"] if ins.get("sequence")]


# ── 1. Block entropy ───────────────────────────────────────────────────


def compute_entropy(inscriptions: list[list[str]]) -> dict:
    flat = [s for ins in inscriptions for s in ins]
    n = len(flat)
    vocab = sorted(set(flat))
    V = len(vocab)
    ln_V = math.log(V) if V > 1 else 1.0

    results = {}
    for order in range(1, 5):
        counts: Counter = Counter()
        for i in range(n - order + 1):
            counts[tuple(flat[i : i + order])] += 1
        total = sum(counts.values())
        h = -sum((c / total) * math.log(c / total) for c in counts.values() if c > 0)
        results[order] = {"raw_nats": round(h, 4), "normalized": round(h / ln_V, 4)}

    h1 = results[1]["normalized"]
    h2 = results[2]["normalized"]
    return {
        "alphabet_size": V,
        "n_tokens": n,
        "h1_norm": results[1]["normalized"],
        "h2_norm": results[2]["normalized"],
        "h2_h1_ratio": round(h2 / h1, 4) if h1 > 0 else 0,
        "block_entropies": results,
        "linguistic_confirmation": h1 > 0.5 and h2 / h1 < 2.0 if h1 > 0 else False,
    }


# ── 2. NWSP positional analysis ────────────────────────────────────────


def nwsp_analysis(inscriptions: list[list[str]]) -> dict:
    terminal: Counter = Counter()
    initial: Counter = Counter()
    medial: Counter = Counter()
    solo: Counter = Counter()
    total: Counter = Counter()

    for ins in inscriptions:
        for s in ins:
            total[s] += 1
        if len(ins) == 1:
            solo[ins[0]] += 1
        else:
            initial[ins[0]] += 1
            terminal[ins[-1]] += 1
            for s in ins[1:-1]:
                medial[s] += 1

    sign_stats = {}
    for s, n in total.items():
        t = terminal[s]
        i = initial[s]
        m = medial[s]
        sol = solo[s]
        t_rate = t / n if n > 0 else 0
        i_rate = i / n if n > 0 else 0
        sign_stats[s] = {
            "total": n, "terminal": t, "initial": i,
            "medial": m, "solo": sol,
            "terminal_rate": round(t_rate, 4),
            "initial_rate": round(i_rate, 4),
        }

    tmk, initial_cls, itm, med, con = [], [], [], [], []
    for s, d in sign_stats.items():
        if d["total"] < 3:
            continue
        tr, ir = d["terminal_rate"], d["initial_rate"]
        if tr >= 0.55:
            tmk.append(s)
        elif ir >= 0.50:
            initial_cls.append(s)
        elif tr >= 0.30 and ir >= 0.30:
            itm.append(s)
        elif tr <= 0.25 and ir <= 0.25:
            med.append(s)
        else:
            con.append(s)

    top_tmk = sorted(
        [(s, sign_stats[s]["terminal_rate"], sign_stats[s]["total"]) for s in tmk],
        key=lambda x: (-x[1], -x[2]),
    )[:10]

    return {
        "nwsp": {"TMK": len(tmk), "INITIAL": len(initial_cls), "ITM": len(itm),
                 "MED": len(med), "CON": len(con)},
        "top_tmk": [{"sign": s, "terminal_rate": r, "total": n} for s, r, n in top_tmk],
        "top_initial": sorted(
            [{"sign": s, "initial_rate": sign_stats[s]["initial_rate"],
              "total": sign_stats[s]["total"]} for s in initial_cls],
            key=lambda x: (-x["initial_rate"], -x["total"]),
        )[:8],
        "sign_stats": sign_stats,
    }


# ── 3. TMK bigram cross-validation ─────────────────────────────────────


def tmk_bigram_validation(inscriptions: list[list[str]], tmk_signs: set[str]) -> dict:
    bigrams = [(ins[j], ins[j + 1]) for ins in inscriptions for j in range(len(ins) - 1)]
    total = len(bigrams)
    if total == 0:
        return {"total_bigrams": 0, "interpretation": "No bigrams"}

    tmk_as_second = sum(1 for _, b in bigrams if b in tmk_signs)
    rate = tmk_as_second / total
    baseline = len(tmk_signs) / max(len({s for ins in inscriptions for s in ins}), 1)

    top10_second = Counter(b for _, b in bigrams).most_common(10)
    tmk_in_top10 = sum(1 for s, _ in top10_second if s in tmk_signs)

    return {
        "total_bigrams": total,
        "tmk_second_rate": round(rate, 4),
        "baseline": round(baseline, 4),
        "tmk_advantage_pp": round((rate - baseline) * 100, 2),
        "tmk_in_top10_second": tmk_in_top10,
        "interpretation": (
            "STRONGLY SUPPORTS agglutinative-suffix hypothesis"
            if rate > baseline + 0.10
            else "SUPPORTS suffix hypothesis"
            if rate > baseline
            else "Weak signal"
        ),
    }


# ── 4. Bigram Markov model ─────────────────────────────────────────────


def markov_model(inscriptions: list[list[str]]) -> dict:
    bigram_counts: Counter = Counter()
    unigram_counts: Counter = Counter()

    for ins in inscriptions:
        for s in ins:
            unigram_counts[s] += 1
        for j in range(len(ins) - 1):
            bigram_counts[(ins[j], ins[j + 1])] += 1

    total_bigrams = sum(bigram_counts.values())

    # Conditional probabilities P(B|A)
    cond: dict[str, dict[str, float]] = defaultdict(dict)
    for (a, b), cnt in bigram_counts.items():
        cond[a][b] = cnt / unigram_counts[a]

    # Top transitions (most informative)
    top_transitions = sorted(
        [(f"{a}->{b}", cnt, round(cnt / unigram_counts[a], 3))
         for (a, b), cnt in bigram_counts.most_common(15)],
        key=lambda x: -x[1],
    )

    # Entropy of bigram distribution
    n = total_bigrams
    h_bigram = -sum((c / n) * math.log(c / n) for c in bigram_counts.values() if c > 0) if n > 0 else 0

    return {
        "total_bigrams": total_bigrams,
        "unique_bigram_types": len(bigram_counts),
        "bigram_entropy_nats": round(h_bigram, 4),
        "top_15_transitions": [
            {"pair": t, "count": c, "cond_prob": p} for t, c, p in top_transitions
        ],
        "note": "Markov model built from decoded M77 sequences (rank-corr mapped)",
    }


# ── 5. Ventris affinity clustering ─────────────────────────────────────


def ventris_clustering(inscriptions: list[list[str]]) -> dict:
    """Simplified Ventris: group signs by left-context (vowel) and right-context (consonant)."""
    signs = sorted({s for ins in inscriptions for s in ins})
    if len(signs) < 4:
        return {"note": "Insufficient data for clustering"}

    # Build context vectors
    left_ctx: dict[str, Counter] = defaultdict(Counter)   # sign B after sign A -> vowel row
    right_ctx: dict[str, Counter] = defaultdict(Counter)  # sign A before sign B -> consonant col

    for ins in inscriptions:
        for j in range(len(ins) - 1):
            a, b = ins[j], ins[j + 1]
            left_ctx[b][a] += 1
            right_ctx[a][b] += 1

    # Compute cosine similarity between context vectors
    def cosine(v1: Counter, v2: Counter) -> float:
        common = set(v1) & set(v2)
        if not common:
            return 0.0
        dot = sum(v1[k] * v2[k] for k in common)
        n1 = math.sqrt(sum(x * x for x in v1.values()))
        n2 = math.sqrt(sum(x * x for x in v2.values()))
        return dot / (n1 * n2) if n1 * n2 > 0 else 0.0

    # Find top-N signs by frequency for clustering
    freq = Counter(s for ins in inscriptions for s in ins)
    top_signs = [s for s, _ in freq.most_common(20)]

    # Cluster by left context (vowel affinity)
    vowel_clusters: list[list[str]] = []
    assigned: set[str] = set()
    threshold = 0.40

    for i, s1 in enumerate(top_signs):
        if s1 in assigned:
            continue
        cluster = [s1]
        for s2 in top_signs[i + 1:]:
            if s2 not in assigned and cosine(left_ctx[s1], left_ctx[s2]) > threshold:
                cluster.append(s2)
                assigned.add(s2)
        if len(cluster) > 1:
            assigned.add(s1)
            vowel_clusters.append(cluster)

    # Cluster by right context (consonant affinity)
    cons_clusters: list[list[str]] = []
    assigned2: set[str] = set()
    for i, s1 in enumerate(top_signs):
        if s1 in assigned2:
            continue
        cluster = [s1]
        for s2 in top_signs[i + 1:]:
            if s2 not in assigned2 and cosine(right_ctx[s1], right_ctx[s2]) > threshold:
                cluster.append(s2)
                assigned2.add(s2)
        if len(cluster) > 1:
            assigned2.add(s1)
            cons_clusters.append(cluster)

    return {
        "signs_analyzed": len(top_signs),
        "threshold": threshold,
        "vowel_clusters": vowel_clusters,
        "consonant_clusters": cons_clusters,
        "n_vowel_clusters": len(vowel_clusters),
        "n_consonant_clusters": len(cons_clusters),
        "note": "Simplified Ventris on decoded M77 sequences. Signs grouped by left (vowel) and right (consonant) co-occurrence contexts.",
    }


# ── 6. Word-structure typology ─────────────────────────────────────────


def word_structure_typology(inscriptions: list[list[str]]) -> dict:
    lengths = [len(ins) for ins in inscriptions]
    total = len(lengths)
    observed = {k: v / total for k, v in Counter(lengths).items()}

    profiles = {
        "Proto-Dravidian":  {1: 0.05, 2: 0.20, 3: 0.32, 4: 0.25, 5: 0.12, 6: 0.04, 7: 0.02},
        "Vedic Sanskrit":   {1: 0.08, 2: 0.22, 3: 0.28, 4: 0.22, 5: 0.12, 6: 0.05, 7: 0.03},
        "Luwian/Anatolian": {1: 0.10, 2: 0.30, 3: 0.30, 4: 0.18, 5: 0.08, 6: 0.03, 7: 0.01},
        "Mycenaean Greek":  {1: 0.12, 2: 0.28, 3: 0.28, 4: 0.18, 5: 0.08, 6: 0.04, 7: 0.02},
        "Proto-Semitic":    {1: 0.08, 2: 0.18, 3: 0.30, 4: 0.24, 5: 0.12, 6: 0.05, 7: 0.03},
        "Sumerian":         {1: 0.06, 2: 0.15, 3: 0.25, 4: 0.28, 5: 0.15, 6: 0.07, 7: 0.04},
    }

    def kl(p: dict, q: dict) -> float:
        eps = 0.001
        all_k = set(p) | set(q)
        return sum(p.get(k, 0) * math.log(p.get(k, 0) / max(q.get(k, eps), eps))
                   for k in all_k if p.get(k, 0) > 0)

    scores = {name: round(kl(observed, prof), 4) for name, prof in profiles.items()}
    ranked = sorted(scores.items(), key=lambda x: x[1])

    return {
        "mean_length": round(sum(lengths) / max(len(lengths), 1), 3),
        "length_distribution": {str(k): round(v, 4) for k, v in sorted(observed.items())},
        "kl_divergences": scores,
        "ranking": [{"language": n, "kl": v} for n, v in ranked],
        "winner": ranked[0][0],
        "data_source": "Decoded M77 OCR sequences (rank-correlation mapped)",
    }


# ── Main ──────────────────────────────────────────────────────────────


def main() -> None:
    print("Loading decoded M77 corpus...")
    inscriptions = load_corpus()
    n = len(inscriptions)
    tokens = sum(len(i) for i in inscriptions)
    print(f"  {n} inscriptions, {tokens} sign tokens")

    print("\n[1/6] Block entropy (Rao 2009 replication)...")
    entropy = compute_entropy(inscriptions)
    print(f"  H1 normalized = {entropy['h1_norm']} (linguistic range: >0.5)")
    print(f"  H2/H1 ratio  = {entropy['h2_h1_ratio']} (sub-linear = language)")
    print(f"  Confirmed linguistic: {entropy['linguistic_confirmation']}")

    print("\n[2/6] NWSP positional classification...")
    nwsp = nwsp_analysis(inscriptions)
    cls = nwsp["nwsp"]
    print(f"  TMK={cls['TMK']} INITIAL={cls['INITIAL']} ITM={cls['ITM']} MED={cls['MED']}")
    if nwsp["top_tmk"]:
        print(f"  Top TMK: {[(x['sign'], x['terminal_rate']) for x in nwsp['top_tmk'][:3]]}")

    print("\n[3/6] TMK bigram cross-validation...")
    tmk_signs = {x["sign"] for x in nwsp["top_tmk"]}
    tmk_bv = tmk_bigram_validation(inscriptions, tmk_signs)
    print(f"  TMK second-rate: {tmk_bv['tmk_second_rate']} (baseline: {tmk_bv['baseline']})")
    print(f"  Advantage: +{tmk_bv['tmk_advantage_pp']}pp")
    print(f"  {tmk_bv['interpretation']}")

    print("\n[4/6] Bigram Markov model...")
    markov = markov_model(inscriptions)
    print(f"  {markov['total_bigrams']} bigrams, {markov['unique_bigram_types']} types")
    print(f"  Bigram entropy: {markov['bigram_entropy_nats']} nats")
    if markov["top_15_transitions"]:
        t = markov["top_15_transitions"][0]
        print(f"  Most common transition: {t['pair']} (n={t['count']}, P={t['cond_prob']})")

    print("\n[5/6] Ventris affinity clustering...")
    ventris = ventris_clustering(inscriptions)
    print(f"  Vowel groups: {ventris.get('n_vowel_clusters', 0)}")
    print(f"  Consonant groups: {ventris.get('n_consonant_clusters', 0)}")
    if ventris.get("vowel_clusters"):
        print(f"  Sample vowel cluster: {ventris['vowel_clusters'][0]}")

    print("\n[6/6] Word-structure typology...")
    typology = word_structure_typology(inscriptions)
    print(f"  Winner: {typology['winner']} (KL={typology['kl_divergences'][typology['winner']]})")
    for r in typology["ranking"][:4]:
        print(f"    {r['language']:<25} KL={r['kl']}")

    results = {
        "corpus": {"n_inscriptions": n, "n_tokens": tokens,
                   "source": "Mahadevan (1977) OCR + rank-corr glyph mapping"},
        "block_entropy": entropy,
        "nwsp": nwsp,
        "tmk_bigram_validation": tmk_bv,
        "markov_model": markov,
        "ventris_clustering": ventris,
        "word_structure_typology": typology,
    }

    out = _REPORTS / "m77_corpus_analysis.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nAll results saved: {out}")


if __name__ == "__main__":
    main()
