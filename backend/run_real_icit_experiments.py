"""Run the full experiment suite on the real reconstructed ICIT corpus.

Reads the extracted corpus from reports/icit_extracted_corpus.json,
then runs:
  1. Corpus statistics (tokens, types, entropy, Zipf)
  2. NWSP positional classification  
  3. Structural fingerprint comparison
  4. TMK bigram cross-validation (on real inscriptions)
  5. Word-structure typology
  6. Site-level breakdown

All results saved to reports/icit_real_experiment_results.json
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).parent.parent
_REPORTS = _REPO / "reports"
sys.path.insert(0, str(Path(__file__).parent))


def load_corpus() -> tuple[list[list[str]], dict]:
    """Load reconstructed ICIT corpus."""
    data = json.loads((_REPORTS / "icit_extracted_corpus.json").read_text(encoding="utf-8"))
    inscriptions = [[s for s in ins["sequence"]] for ins in data["inscriptions"] if ins["sequence"]]
    meta = {ins["icit_id"]: ins for ins in data["inscriptions"]}
    return inscriptions, meta


# ── 1. Corpus statistics ───────────────────────────────────────────────


def corpus_stats(inscriptions: list[list[str]]) -> dict:
    flat = [s for ins in inscriptions for s in ins]
    freq = Counter(flat)
    n_tokens = len(flat)
    n_types = len(freq)

    # Block entropy H1 (MLE)
    h1 = -sum((c / n_tokens) * math.log(c / n_tokens) for c in freq.values() if c > 0)
    ln_V = math.log(n_types) if n_types > 1 else 1.0
    h1_norm = h1 / ln_V

    # Zipf exponent (log-log rank regression)
    ranked = sorted(freq.values(), reverse=True)
    try:
        import numpy as np
        log_rank = np.log(range(1, len(ranked) + 1))
        log_freq = np.log(ranked)
        zipf_exp = -np.polyfit(log_rank, log_freq, 1)[0]
    except ImportError:
        zipf_exp = None

    hapax = sum(1 for c in freq.values() if c == 1)
    lengths = [len(ins) for ins in inscriptions]

    return {
        "n_inscriptions": len(inscriptions),
        "n_tokens": n_tokens,
        "n_types": n_types,
        "type_token_ratio": round(n_types / max(n_tokens, 1), 4),
        "hapax_count": hapax,
        "hapax_fraction": round(hapax / n_types, 4),
        "h1_nats": round(h1, 4),
        "h1_normalized": round(h1_norm, 4),
        "zipf_exponent": round(zipf_exp, 4) if zipf_exp else None,
        "mean_inscription_length": round(sum(lengths) / max(len(lengths), 1), 3),
        "max_inscription_length": max(lengths),
        "top_10_signs": [(s, c) for s, c in freq.most_common(10)],
    }


# ── 2. Positional analysis / NWSP ─────────────────────────────────────


def positional_analysis(inscriptions: list[list[str]]) -> dict:
    """Compute per-sign T/M/I/Solo rates from real inscriptions."""
    terminal: Counter = Counter()
    initial: Counter = Counter()
    medial: Counter = Counter()
    solo: Counter = Counter()
    total: Counter = Counter()

    for ins in inscriptions:
        if not ins:
            continue
        for s in ins:
            total[s] += 1
        if len(ins) == 1:
            solo[ins[0]] += 1
        else:
            initial[ins[0]] += 1
            terminal[ins[-1]] += 1
            for s in ins[1:-1]:
                medial[s] += 1

    signs = {}
    for s, n in total.items():
        t = terminal[s]
        i = initial[s]
        m = medial[s]
        sol = solo[s]
        signs[s] = {
            "sign": s,
            "total": n,
            "terminal": t,
            "medial": m,
            "initial": i,
            "solo": sol,
            "terminal_rate": round(t / n, 4) if n > 0 else 0,
            "initial_rate": round(i / n, 4) if n > 0 else 0,
        }

    # NWSP classification
    tmk, initial_cls, itm, med, con = [], [], [], [], []
    for s, d in signs.items():
        n = d["total"]
        if n < 4:
            continue
        t_rate = d["terminal_rate"]
        i_rate = d["initial_rate"]
        if t_rate >= 0.60:
            tmk.append(s)
        elif i_rate >= 0.55:
            initial_cls.append(s)
        elif t_rate >= 0.35 and i_rate >= 0.35:
            itm.append(s)
        elif t_rate <= 0.25 and i_rate <= 0.25:
            med.append(s)
        else:
            con.append(s)

    # Top TMK by terminal rate
    top_tmk = sorted(
        [(s, signs[s]["terminal_rate"], signs[s]["total"]) for s in tmk],
        key=lambda x: (-x[1], -x[2]),
    )[:10]

    return {
        "nwsp_classification": {
            "TMK": len(tmk),
            "INITIAL": len(initial_cls),
            "ITM": len(itm),
            "MED": len(med),
            "CON": len(con),
        },
        "top_tmk_signs": [
            {"sign": s, "terminal_rate": r, "total": n} for s, r, n in top_tmk
        ],
        "top_initial_signs": sorted(
            [{"sign": s, "initial_rate": signs[s]["initial_rate"], "total": signs[s]["total"]}
             for s in initial_cls],
            key=lambda x: (-x["initial_rate"], -x["total"]),
        )[:8],
    }


# ── 3. TMK bigram cross-validation ────────────────────────────────────


def tmk_bigram_validation(inscriptions: list[list[str]], tmk_signs: set[str]) -> dict:
    """Check whether TMK signs appear predominantly in second position of bigrams."""
    bigrams: list[tuple[str, str]] = []
    for ins in inscriptions:
        for j in range(len(ins) - 1):
            bigrams.append((ins[j], ins[j + 1]))

    tmk_as_second = sum(1 for a, b in bigrams if b in tmk_signs)
    total_bigrams = len(bigrams)
    total_second = total_bigrams
    non_tmk_as_second = total_bigrams - tmk_as_second

    unique_second_pos = Counter(b for _, b in bigrams)
    top10 = unique_second_pos.most_common(10)
    tmk_in_top10 = sum(1 for s, _ in top10 if s in tmk_signs)

    tmk_second_rate = tmk_as_second / max(total_bigrams, 1)
    baseline = len(tmk_signs) / 713  # expected rate by chance

    return {
        "total_bigrams": total_bigrams,
        "tmk_in_second_position": tmk_as_second,
        "tmk_second_rate": round(tmk_second_rate, 4),
        "expected_by_chance": round(baseline, 4),
        "tmk_advantage": round(tmk_second_rate - baseline, 4),
        "top10_second_signs_are_tmk": tmk_in_top10,
        "interpretation": (
            "STRONGLY SUPPORTS agglutinative-suffix hypothesis"
            if tmk_second_rate > baseline + 0.10
            else "WEAK SUPPORT for suffix hypothesis"
            if tmk_second_rate > baseline
            else "DOES NOT SUPPORT suffix hypothesis"
        ),
    }


# ── 4. Word-structure typology ─────────────────────────────────────────


def word_structure_typology(inscriptions: list[list[str]]) -> dict:
    """Rank language families by inscription length KL-divergence."""
    lengths = [len(ins) for ins in inscriptions]
    length_dist = Counter(lengths)
    total = sum(length_dist.values())
    observed = {k: v / total for k, v in length_dist.items()}

    profiles = {
        "Proto-Dravidian":    {1: 0.05, 2: 0.20, 3: 0.32, 4: 0.25, 5: 0.12, 6: 0.04, 7: 0.02},
        "Vedic Sanskrit":     {1: 0.08, 2: 0.22, 3: 0.28, 4: 0.22, 5: 0.12, 6: 0.05, 7: 0.03},
        "Luwian/Anatolian":   {1: 0.10, 2: 0.30, 3: 0.30, 4: 0.18, 5: 0.08, 6: 0.03, 7: 0.01},
        "Mycenaean Greek":    {1: 0.12, 2: 0.28, 3: 0.28, 4: 0.18, 5: 0.08, 6: 0.04, 7: 0.02},
        "Proto-Semitic":      {1: 0.08, 2: 0.18, 3: 0.30, 4: 0.24, 5: 0.12, 6: 0.05, 7: 0.03},
        "Sumerian":           {1: 0.06, 2: 0.15, 3: 0.25, 4: 0.28, 5: 0.15, 6: 0.07, 7: 0.04},
    }

    def kl(p, q):
        eps = 0.001
        all_k = set(p) | set(q)
        return sum(
            p.get(k, 0) * math.log(p.get(k, 0) / max(q.get(k, eps), eps))
            for k in all_k if p.get(k, 0) > 0
        )

    scores = {}
    for name, profile in profiles.items():
        scores[name] = round(kl(observed, profile), 4)

    ranked = sorted(scores.items(), key=lambda x: x[1])

    return {
        "observed_length_distribution": {str(k): v for k, v in sorted(observed.items())},
        "mean_length": round(sum(lengths) / max(len(lengths), 1), 3),
        "kl_divergences": scores,
        "ranking": [{"language": n, "kl_divergence": v} for n, v in ranked],
        "winner": ranked[0][0],
        "winner_kl": ranked[0][1],
        "method": "KL-divergence of inscription-length distribution vs language profiles",
    }


# ── 5. Site breakdown ─────────────────────────────────────────────────


def site_breakdown(inscriptions: list[list[str]], meta: dict) -> dict:
    icit_ids = list(meta.keys())
    sites: dict[str, list[list[str]]] = {}
    for icit_id, ins_meta in meta.items():
        site = ins_meta.get("site", "Unknown")
        insc = ins_meta.get("sequence", [])
        if insc:
            sites.setdefault(site, []).append(insc)

    result = {}
    for site, site_ins in sorted(sites.items(), key=lambda x: -len(x[1])):
        if len(site_ins) < 10:
            continue
        flat = [s for ins in site_ins for s in ins]
        freq = Counter(flat)
        n = len(flat)
        h1 = -sum((c / n) * math.log(c / n) for c in freq.values() if c > 0)
        ln_v = math.log(len(freq)) if len(freq) > 1 else 1.0
        result[site] = {
            "n_inscriptions": len(site_ins),
            "n_tokens": n,
            "n_sign_types": len(freq),
            "mean_length": round(n / max(len(site_ins), 1), 2),
            "h1_normalized": round(h1 / ln_v, 4),
        }

    return result


# ── Main ──────────────────────────────────────────────────────────────


def main() -> None:
    print("Loading reconstructed ICIT corpus...")
    inscriptions, meta = load_corpus()
    print(f"  {len(inscriptions)} inscriptions, {sum(len(i) for i in inscriptions)} tokens")

    print("\n[1/5] Corpus statistics...")
    stats = corpus_stats(inscriptions)
    print(f"  H1 normalized = {stats['h1_normalized']}")
    print(f"  Zipf exponent = {stats['zipf_exponent']}")
    print(f"  Mean length   = {stats['mean_inscription_length']}")

    print("\n[2/5] Positional analysis (NWSP)...")
    pos = positional_analysis(inscriptions)
    cls = pos["nwsp_classification"]
    print(f"  TMK={cls['TMK']}  INITIAL={cls['INITIAL']}  ITM={cls['ITM']}  MED={cls['MED']}")
    print(f"  Top TMK signs: {[(x['sign'], x['terminal_rate']) for x in pos['top_tmk_signs'][:3]]}")

    print("\n[3/5] TMK bigram cross-validation...")
    tmk_signs = {x["sign"] for x in pos["top_tmk_signs"]}
    # Add all TMK-classified signs
    flat = [s for ins in inscriptions for s in ins]
    freq = Counter(flat)
    from collections import Counter as C
    tmk_all: set[str] = set()
    for ins in inscriptions:
        for j, s in enumerate(ins):
            n = freq[s]
            if n < 4:
                continue
            t_rate = sum(1 for i2 in inscriptions if i2 and i2[-1] == s) / n
            if t_rate >= 0.60:
                tmk_all.add(s)
    bigram = tmk_bigram_validation(inscriptions, tmk_all)
    print(f"  TMK second-position rate: {bigram['tmk_second_rate']:.4f} (baseline: {bigram['expected_by_chance']:.4f})")
    print(f"  Advantage: +{bigram['tmk_advantage']:.4f}")
    print(f"  Interpretation: {bigram['interpretation']}")

    print("\n[4/5] Word-structure typology...")
    wst = word_structure_typology(inscriptions)
    print(f"  Winner: {wst['winner']} (KL={wst['winner_kl']})")
    for r in wst["ranking"][:4]:
        print(f"    {r['language']:<25} KL={r['kl_divergence']}")

    print("\n[5/5] Site breakdown...")
    sites = site_breakdown(inscriptions, meta)
    for site, s in sorted(sites.items(), key=lambda x: -x[1]["n_inscriptions"])[:5]:
        print(f"  {site:<30} N={s['n_inscriptions']}  H1={s['h1_normalized']}  len={s['mean_length']}")

    results = {
        "corpus_stats": stats,
        "positional_analysis": pos,
        "tmk_bigram_validation": bigram,
        "word_structure_typology": wst,
        "site_breakdown": sites,
        "notes": {
            "data_source": "Reconstructed from Fuls (2023) Kindle TXT exports",
            "sign_ordering": "Probabilistic (initial_rate->first, terminal_rate->last)",
            "n_inscriptions": len(inscriptions),
            "n_tokens": sum(len(i) for i in inscriptions),
            "caveat": "True ordering requires PDF version or direct ICIT database access",
        },
    }

    out = _REPORTS / "icit_real_experiment_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults saved to {out}")


if __name__ == "__main__":
    main()
