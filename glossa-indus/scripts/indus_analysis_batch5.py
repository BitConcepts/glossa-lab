"""Batch 5: Formal analysis tests.

Runs:
  1. Null model tests (random shuffle, frequency-preserved shuffle, site-preserved shuffle)
  2. Contact zone analysis (Harappa vs Mohenjo-daro sign inventory)
  3. Hunt tripartite grammar test (faunal=initial, celestial=terminal, prefix-medial-suffix)
  4. Summary report

All results saved to glossa-indus/analysis/

Uses the Firestore corpus (supplementary, 3137 sequences) for the formal runs.
The primary V1 corpus (indus_research.jsonl) is used for cross-checks.

Per instruction plan section 14 — all analysis outputs are machine-readable JSON.
"""
from __future__ import annotations
import json, random, sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import numpy as np

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE = Path(__file__).parents[1]
GLOSSA_LAB = BASE.parent
sys.path.insert(0, str(GLOSSA_LAB / "backend"))

ANALYSIS_DIR = BASE / "analysis"
NULL_DIR = ANALYSIS_DIR / "null_models"
CONTACT_DIR = ANALYSIS_DIR / "artifact_context"  # reusing for contact zone
POSITIONAL_DIR = ANALYSIS_DIR / "positional"
REPORTS_DIR = BASE / "reports" / "model_reports"

for d in [NULL_DIR, CONTACT_DIR, POSITIONAL_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── Load corpus ───────────────────────────────────────────────────────────────

def load_firestore_corpus():
    try:
        from glossa_lab.data.indus_corpus_firestore import (
            load_corpus,
            load_corpus_by_dockey,
        )
        seqs = load_corpus(min_length=2)
        by_dk = load_corpus_by_dockey(min_length=2)
        return seqs, by_dk
    except ImportError:
        print("  WARNING: indus_corpus_firestore.py not found, using v3 fallback")
        try:
            from glossa_lab.data.indus_corpus_v3 import (
                load_corpus,
                load_corpus_by_dockey,
            )
            return load_corpus(min_length=2), load_corpus_by_dockey(min_length=2)
        except ImportError:
            return [], {}

# ── Analysis utilities ────────────────────────────────────────────────────────

def sign_pos_profiles(seqs: list) -> dict:
    """Compute I/M/T rates for every sign."""
    counts = defaultdict(lambda: {"I": 0, "M": 0, "T": 0, "total": 0})
    for seq in seqs:
        if len(seq) < 2:
            continue
        for i, s in enumerate(seq):
            counts[s]["total"] += 1
            if i == 0:
                counts[s]["I"] += 1
            elif i == len(seq) - 1:
                counts[s]["T"] += 1
            else:
                counts[s]["M"] += 1
    profiles = {}
    for s, c in counts.items():
        tot = c["total"]
        if tot < 5:
            continue
        t, ii, m = c["T"]/tot, c["I"]/tot, c["M"]/tot
        role = (
            "TERMINAL_STRONG" if t >= 0.60 else
            "INITIAL_STRONG" if ii >= 0.55 else
            "MEDIAL_STRONG" if m >= 0.65 else
            "TERMINAL_MODERATE" if t >= 0.40 else
            "INITIAL_MODERATE" if ii >= 0.40 else "MIXED"
        )
        profiles[s] = {"t": round(t,3), "i": round(ii,3), "m": round(m,3),
                       "n": tot, "role": role}
    return profiles

def positional_entropy(seqs: list, profiles: dict) -> float:
    """H(position | sign) — lower = more constrained."""
    total_entropy = 0.0
    total_tokens = 0
    for s, p in profiles.items():
        n = p["n"]
        total_tokens += n
        t, ii, m = p["t"], p["i"], p["m"]
        h = 0.0
        for prob in [t, ii, m]:
            if prob > 0:
                h -= prob * np.log2(prob)
        total_entropy += n * h
    return total_entropy / max(total_tokens, 1)

# ── NULL MODEL 1: Random shuffle ──────────────────────────────────────────────

def null_random_shuffle(seqs: list, n_samples: int = 100) -> dict:
    """Randomly shuffle all tokens. Test: does real corpus have more structure?"""
    print("  Running null_random_shuffle...")
    # Collect all tokens
    all_tokens = [s for seq in seqs for s in seq]
    lengths = [len(seq) for seq in seqs]
    real_profiles = sign_pos_profiles(seqs)
    real_pos_entropy = positional_entropy(seqs, real_profiles)

    # Shuffle null models
    null_entropies = []
    for _ in range(n_samples):
        shuffled_tokens = all_tokens.copy()
        random.shuffle(shuffled_tokens)
        # Reconstruct sequences with same lengths
        null_seqs = []
        idx = 0
        for L in lengths:
            null_seqs.append(shuffled_tokens[idx:idx+L])
            idx += L
        null_prof = sign_pos_profiles(null_seqs)
        null_entropies.append(positional_entropy(null_seqs, null_prof))

    mean_null = float(np.mean(null_entropies))
    std_null = float(np.std(null_entropies))
    effect_size = (mean_null - real_pos_entropy) / max(std_null, 1e-10)

    return {
        "test": "null_random_shuffle",
        "real_positional_entropy": round(real_pos_entropy, 4),
        "null_mean_positional_entropy": round(mean_null, 4),
        "null_std": round(std_null, 4),
        "effect_size_d": round(effect_size, 3),
        "n_samples": n_samples,
        "interpretation": (
            f"Real corpus positional entropy ({real_pos_entropy:.4f}) is "
            f"{effect_size:.2f}σ below random shuffle null ({mean_null:.4f}). "
            f"{'SIGNIFICANT structure above random baseline.' if effect_size > 2.0 else 'WEAK evidence above random baseline.'}"
        ),
    }

# ── NULL MODEL 2: Frequency-preserved shuffle ─────────────────────────────────

def null_frequency_preserved(seqs: list, n_samples: int = 100) -> dict:
    """Shuffle preserving per-sign frequency. Tests for bigram structure above freq baseline."""
    print("  Running null_frequency_preserved...")
    all_tokens = [s for seq in seqs for s in seq]
    lengths = [len(seq) for seq in seqs]
    real_bigrams = Counter(
        (seq[i], seq[i+1]) for seq in seqs for i in range(len(seq)-1)
    )
    total_bigrams = sum(real_bigrams.values())
    top_real_bigrams = {bg: cnt/total_bigrams for bg, cnt in real_bigrams.most_common(20)}

    # Shuffle null
    null_top_bigrams_counts = []
    for _ in range(n_samples):
        shuffled = all_tokens.copy()
        random.shuffle(shuffled)
        null_seqs = []
        idx = 0
        for L in lengths:
            null_seqs.append(shuffled[idx:idx+L])
            idx += L
        null_bigrams = Counter(
            (null_seqs[j][i], null_seqs[j][i+1])
            for j in range(len(null_seqs))
            for i in range(len(null_seqs[j])-1)
        )
        # Count how many of the top-20 real bigrams appear in null at >50% rate
        match_count = sum(
            1 for bg, real_freq in top_real_bigrams.items()
            if null_bigrams.get(bg, 0) / max(total_bigrams, 1) > real_freq * 0.5
        )
        null_top_bigrams_counts.append(match_count)

    mean_null_matches = float(np.mean(null_top_bigrams_counts))

    return {
        "test": "null_frequency_preserved",
        "top_20_real_bigrams_preserved": {str(bg): round(freq,4)
                                          for bg, freq in list(top_real_bigrams.items())[:10]},
        "null_mean_top20_matches": round(mean_null_matches, 2),
        "n_samples": n_samples,
        "interpretation": (
            f"On average {mean_null_matches:.1f}/20 top bigrams appear at >50% rate in shuffled null. "
            f"{'HIGH bigram structure above frequency baseline.' if mean_null_matches < 5 else 'MODERATE structure above frequency baseline.'}"
        ),
    }

# ── NULL MODEL 3: Site-preserved shuffle ─────────────────────────────────────

def null_site_preserved(by_dockey: dict, n_samples: int = 50) -> dict:
    """Shuffle within-site, test for cross-site recurrence above chance."""
    print("  Running null_site_preserved...")
    site_seqs = {
        "mohenjo_daro": [seq for dk in range(1001,2000) for seq in by_dockey.get(dk,[])],
        "harappa": [seq for dk in range(2001,3000) for seq in by_dockey.get(dk,[])],
        "chanhu_daro": [seq for dk in range(3001,4000) for seq in by_dockey.get(dk,[])],
    }

    # Real cross-site bigrams
    all_bigrams_by_site = {}
    for site, seqs in site_seqs.items():
        bgs = Counter((s[i], s[i+1]) for s in seqs for i in range(len(s)-1))
        all_bigrams_by_site[site] = bgs

    # Real cross-site overlap
    sites = [s for s, seqs in site_seqs.items() if seqs]
    if len(sites) < 2:
        return {"test": "null_site_preserved", "status": "insufficient_sites"}

    real_shared = len(set(all_bigrams_by_site.get(sites[0],{}).keys()) &
                      set(all_bigrams_by_site.get(sites[1],{}).keys())) if len(sites) >= 2 else 0

    # Null: shuffle within each site
    null_shared_counts = []
    for _ in range(n_samples):
        null_site_bg = {}
        for site, seqs in site_seqs.items():
            if not seqs:
                continue
            tokens = [s for seq in seqs for s in seq]
            lengths = [len(seq) for seq in seqs]
            random.shuffle(tokens)
            null_seqs = []
            idx = 0
            for L in lengths:
                null_seqs.append(tokens[idx:idx+L])
                idx += L
            null_site_bg[site] = Counter(
                (s[i], s[i+1]) for s in null_seqs for i in range(len(s)-1)
            )
        if len(sites) >= 2:
            shared = len(set(null_site_bg.get(sites[0],{}).keys()) &
                         set(null_site_bg.get(sites[1],{}).keys()))
            null_shared_counts.append(shared)

    mean_null_shared = float(np.mean(null_shared_counts)) if null_shared_counts else 0
    effect_size = (real_shared - mean_null_shared) / max(float(np.std(null_shared_counts)) if null_shared_counts else 1, 1e-10)

    return {
        "test": "null_site_preserved",
        "sites_analysed": sites,
        "real_cross_site_shared_bigrams": real_shared,
        "null_mean_cross_site_shared": round(mean_null_shared, 1),
        "effect_size_d": round(effect_size, 3),
        "n_samples": n_samples,
        "interpretation": (
            f"Real {real_shared} shared bigrams between {sites[0]} and {sites[1]}. "
            f"Null: {mean_null_shared:.1f} (effect_size={effect_size:.2f}σ). "
            f"{'SIGNIFICANT cross-site bigram recurrence.' if effect_size > 2.0 else 'WEAK cross-site recurrence above null.'}"
        ),
    }

# ── CONTACT ZONE ANALYSIS ─────────────────────────────────────────────────────

def contact_zone_analysis(by_dockey: dict, profiles: dict) -> dict:
    """Formal Harappa vs Mohenjo-daro contact zone analysis."""
    print("  Running contact zone analysis...")
    m_seqs = [seq for dk in range(1001,2000) for seq in by_dockey.get(dk,[])]
    h_seqs = [seq for dk in range(2001,3000) for seq in by_dockey.get(dk,[])]

    m_signs = Counter(s for seq in m_seqs for s in seq)
    h_signs = Counter(s for seq in h_seqs for s in seq)

    m_set, h_set = set(m_signs), set(h_signs)
    shared = m_set & h_set
    m_only = m_set - h_set
    h_only = h_set - m_set
    jaccard = len(shared) / max(len(m_set | h_set), 1)

    h_exclusive_sorted = sorted(h_only, key=lambda s: -h_signs[s])[:15]
    m_exclusive_sorted = sorted(m_only, key=lambda s: -m_signs[s])[:15]

    # Classify Harappa-exclusive signs by role
    h_excl_with_roles = [
        {"sign": s, "harappa_freq": h_signs[s],
         "role": profiles.get(s, {}).get("role", "unknown"),
         "hypothesis": "trade/administrative logogram" if profiles.get(s,{}).get("role") in ("INITIAL_STRONG","TERMINAL_STRONG") else "unclear"}
        for s in h_exclusive_sorted[:10]
    ]

    return {
        "test": "contact_zone_mohenjo_harappa",
        "mohenjo_dockeys": len([dk for dk in range(1001,2000) if dk in by_dockey]),
        "harappa_dockeys": len([dk for dk in range(2001,3000) if dk in by_dockey]),
        "mohenjo_sign_types": len(m_set),
        "harappa_sign_types": len(h_set),
        "shared_signs": len(shared),
        "mohenjo_only": len(m_only),
        "harappa_only": len(h_only),
        "jaccard_similarity": round(jaccard, 3),
        "harappa_exclusive_signs": h_excl_with_roles,
        "mohenjo_exclusive_top10": [{"sign": s, "freq": m_signs[s],
                                      "role": profiles.get(s,{}).get("role","?")}
                                     for s in m_exclusive_sorted[:10]],
        "interpretation": (
            f"M↔H Jaccard={jaccard:.3f}. {len(h_only)} Harappa-exclusive signs "
            f"(contact zone candidates). {len(shared)} shared signs confirm "
            f"same civilization script inventory."
        ),
    }

# ── HUNT TRIPARTITE GRAMMAR TEST ─────────────────────────────────────────────

def hunt_tripartite_test(seqs: list, profiles: dict) -> dict:
    """Test Hunt model: faunal signs = initial, celestial = terminal."""
    print("  Running Hunt tripartite grammar test...")

    # We can't identify faunal/celestial signs without visual catalog
    # Instead we test the structural prediction: are INITIAL_STRONG signs
    # concentrated at prefix position AND TERMINAL_STRONG at suffix position?
    # This is what both Hunt and Dravidian-suffix models predict.

    initial_strong = [(s, p) for s, p in profiles.items() if p["role"] == "INITIAL_STRONG"]
    terminal_strong = [(s, p) for s, p in profiles.items() if p["role"] == "TERMINAL_STRONG"]
    medial_strong = [(s, p) for s, p in profiles.items() if p["role"] == "MEDIAL_STRONG"]

    # Test 1: Are prefixes (I-strong) actually at position 0 more than expected?
    # Expected by chance for sign s: i_rate = 1/mean_length
    mean_len = sum(len(s) for s in seqs) / max(len(seqs), 1)
    expected_i_by_chance = 1.0 / mean_len

    observed_mean_i = np.mean([p["i"] for _, p in initial_strong]) if initial_strong else 0
    observed_mean_t = np.mean([p["t"] for _, p in terminal_strong]) if terminal_strong else 0

    # Test 2: Prefix-medial-suffix structure: do inscriptions follow I→M→T order?
    formula_inscriptions = 0
    for seq in seqs:
        if len(seq) >= 3:
            # Check: first sign is INITIAL, last is TERMINAL, middle has MEDIAL
            first_role = profiles.get(seq[0], {}).get("role", "")
            last_role = profiles.get(seq[-1], {}).get("role", "")
            has_medial = any(profiles.get(s, {}).get("role","") in
                           ("MEDIAL_STRONG", "MIXED") for s in seq[1:-1])
            if "INITIAL" in first_role and "TERMINAL" in last_role and has_medial:
                formula_inscriptions += 1

    formula_rate = formula_inscriptions / max(len([s for s in seqs if len(s) >= 3]), 1)

    # Null expectation for formula rate (random assignment of roles)
    null_formula_rate = (
        len(initial_strong) / max(len(profiles), 1) *
        len(terminal_strong) / max(len(profiles), 1) *
        (len(medial_strong) / max(len(profiles), 1))
    )

    return {
        "test": "hunt_tripartite_grammar",
        "hunt_prediction": "Prefix(faunal/initial) + Medial(action/domain) + Suffix(celestial/terminal)",
        "glossa_lab_note": "Cannot directly classify faunal/celestial without visual catalog crosswalk",
        "structural_test": {
            "initial_strong_signs": len(initial_strong),
            "terminal_strong_signs": len(terminal_strong),
            "medial_strong_signs": len(medial_strong),
            "mean_i_rate_of_initial_signs": round(observed_mean_i, 3),
            "mean_t_rate_of_terminal_signs": round(observed_mean_t, 3),
            "expected_i_by_chance": round(expected_i_by_chance, 3),
            "lift_above_chance": round(observed_mean_i / max(expected_i_by_chance, 1e-10), 2),
        },
        "formula_test": {
            "inscriptions_with_imit_structure": formula_inscriptions,
            "total_inscriptions_len3plus": len([s for s in seqs if len(s) >= 3]),
            "formula_rate": round(formula_rate, 3),
            "null_expected_rate": round(null_formula_rate, 3),
            "lift_above_null": round(formula_rate / max(null_formula_rate, 1e-10), 2),
        },
        "verdict": (
            "STRUCTURAL PREFIX-MEDIAL-SUFFIX PATTERN EXISTS (lift > 2x null). "
            "Consistent with BOTH Hunt model and Dravidian suffix model. "
            "Cannot distinguish between them without visual sign classification."
            if formula_rate > null_formula_rate * 2 else
            "WEAK tripartite structure — may require visual catalog to classify sign types properly."
        ),
    }

# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    print(f"\n{'='*60}")
    print("Batch 5: Formal Analysis Tests")
    print(f"{'='*60}\n")

    print("Loading Firestore corpus...")
    seqs, by_dockey = load_firestore_corpus()
    if not seqs:
        print("ERROR: No corpus loaded. Check indus_corpus_firestore.py")
        return 1
    print(f"  Loaded {len(seqs)} sequences, {len(by_dockey)} dockeys")

    print("\nComputing sign positional profiles...")
    profiles = sign_pos_profiles(seqs)
    print(f"  {len(profiles)} signs profiled (min_count=5)")

    print(f"\nRunning {3} null models...")
    results = {}

    # Null model 1: Random shuffle
    r1 = null_random_shuffle(seqs, n_samples=100)
    results["null_random_shuffle"] = r1
    (NULL_DIR / "null_random_shuffle.json").write_text(json.dumps(r1, indent=2), "utf-8")
    print(f"    → effect_size={r1.get('effect_size_d','?')}σ  {r1['interpretation'][:60]}...")

    # Null model 2: Frequency-preserved
    r2 = null_frequency_preserved(seqs, n_samples=100)
    results["null_frequency_preserved"] = r2
    (NULL_DIR / "null_frequency_preserved.json").write_text(json.dumps(r2, indent=2), "utf-8")
    print(f"    → null_top20_matches={r2.get('null_mean_top20_matches','?')}")

    # Null model 3: Site-preserved
    r3 = null_site_preserved(by_dockey, n_samples=50)
    results["null_site_preserved"] = r3
    (NULL_DIR / "null_site_preserved.json").write_text(json.dumps(r3, indent=2), "utf-8")
    print(f"    → cross-site effect={r3.get('effect_size_d','?')}σ")

    # Contact zone analysis
    print("\nRunning contact zone analysis...")
    r4 = contact_zone_analysis(by_dockey, profiles)
    results["contact_zone"] = r4
    (CONTACT_DIR / "contact_zone_mohenjo_harappa.json").write_text(json.dumps(r4, indent=2), "utf-8")
    print(f"    → Jaccard={r4['jaccard_similarity']:.3f}, Harappa-exclusive={r4['harappa_only']}")

    # Hunt tripartite grammar test
    print("\nRunning Hunt tripartite grammar test...")
    r5 = hunt_tripartite_test(seqs, profiles)
    results["hunt_tripartite"] = r5
    (POSITIONAL_DIR / "hunt_tripartite_test.json").write_text(json.dumps(r5, indent=2), "utf-8")
    print(f"    → formula_rate={r5['formula_test']['formula_rate']:.3f} vs null={r5['formula_test']['null_expected_rate']:.3f}")
    print(f"    → {r5['verdict'][:80]}...")

    # Full synthesis report
    rpt = {
        "batch": "BATCH5-ANALYSIS",
        "timestamp": datetime.utcnow().isoformat(),
        "corpus": "Firestore supplementary (2026-05-14)",
        "n_sequences": len(seqs),
        "n_dockeys": len(by_dockey),
        "n_signs_profiled": len(profiles),
        "results": results,
        "_citation": {
            "primary_sources": ["I.6"],
            "note": "Formal null model analysis; contact zone; Hunt model test",
        },
    }
    rpt_path = REPORTS_DIR / "batch5_analysis_report.json"
    rpt_path.write_text(json.dumps(rpt, indent=2, default=str), "utf-8")

    print(f"\n{'='*60}")
    print(f"Batch 5 complete. Reports saved to:")
    print(f"  {NULL_DIR.relative_to(BASE)}/")
    print(f"  {CONTACT_DIR.relative_to(BASE)}/")
    print(f"  {POSITIONAL_DIR.relative_to(BASE)}/")
    print(f"  {rpt_path.relative_to(BASE)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
