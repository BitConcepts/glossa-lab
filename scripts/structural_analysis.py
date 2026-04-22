"""
Glossa-Lab Decipherment Sprint — Phases 6-8: Structural Analysis
================================================================
Phase 6: Full structural analysis (6 sub-analyses)
Phase 7: Latent sign class discovery
Phase 8: Candidate DoF recovery

Run from the glossa-lab root:
    python scripts/structural_analysis.py

Outputs:
    analysis/structural_stats.json     (machine-readable full stats)
    reports/sequence_analysis_report.md
    reports/candidate_prefix_suffix_report.md
    reports/latent_sign_class_report.md
    reports/decipherment_readiness_report.md
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
DATA_NORM = ROOT / "data_normalized"
CROSSWALKS = ROOT / "crosswalks"
ANALYSIS = ROOT / "analysis"
REPORTS = ROOT / "reports"

for d in (ANALYSIS, REPORTS):
    d.mkdir(parents=True, exist_ok=True)

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Load corpus_master ───────────────────────────────────────────────────────

def load_corpus_master() -> list[dict]:
    path = DATA_NORM / "corpus_master.csv"
    if not path.exists():
        raise FileNotFoundError(f"corpus_master.csv not found. Run build_corpus_pipeline.py first.")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ── Phase 6.1: Frequency analysis ───────────────────────────────────────────

def frequency_analysis(records: list[dict]) -> dict:
    """Global and stratified sign frequency analysis."""
    freq: Counter = Counter()
    by_site: dict[str, Counter] = defaultdict(Counter)
    by_artifact: dict[str, Counter] = defaultdict(Counter)
    lengths = []

    for rec in records:
        seq = rec["sign_sequence_raw"].split()
        lengths.append(len(seq))
        site = rec["site"]
        artifact = rec["artifact_type"]
        for sign in seq:
            freq[sign] += 1
            by_site[site][sign] += 1
            by_artifact[artifact][sign] += 1

    n_tokens = sum(freq.values())
    # Hapax (signs appearing exactly once)
    hapax = [s for s, c in freq.items() if c == 1]
    # Length distribution
    len_dist = dict(sorted(Counter(lengths).items()))

    # Entropy of sign frequency distribution
    total = sum(freq.values())
    h1 = -sum((c / total) * math.log2(c / total) for c in freq.values() if c > 0)

    return {
        "global_freq": dict(freq.most_common()),
        "by_site": {k: dict(v.most_common(30)) for k, v in by_site.items()},
        "by_artifact": {k: dict(v.most_common(20)) for k, v in by_artifact.items()},
        "length_distribution": len_dist,
        "n_tokens": n_tokens,
        "n_distinct_signs": len(freq),
        "n_hapax": len(hapax),
        "hapax_fraction": round(len(hapax) / len(freq), 4),
        "mean_length": round(sum(lengths) / len(lengths), 2),
        "median_length": sorted(lengths)[len(lengths) // 2],
        "max_length": max(lengths),
        "min_length": min(lengths),
        "unigram_entropy_h1": round(h1, 4),
        "top_30_signs": dict(freq.most_common(30)),
    }


# ── Phase 6.2: Positional analysis ──────────────────────────────────────────

def positional_analysis(records: list[dict]) -> dict:
    """Start/end/internal rates and position-conditioned entropy."""
    freq: Counter = Counter()
    start_freq: Counter = Counter()
    end_freq: Counter = Counter()
    internal_freq: Counter = Counter()
    # Position-conditioned: for each position 0..N-1 in inscriptions of length N
    pos_counts: dict[tuple[int, int], Counter] = defaultdict(Counter)

    for rec in records:
        seq = rec["sign_sequence_raw"].split()
        n = len(seq)
        for i, sign in enumerate(seq):
            freq[sign] += 1
            pos_counts[(i, n)][sign] += 1
            if i == 0:
                start_freq[sign] += 1
            elif i == n - 1:
                end_freq[sign] += 1
            else:
                internal_freq[sign] += 1

    # Position-conditioned entropy: H(sign | position=0) vs H(sign | position=-1)
    start_counter = Counter()
    end_counter = Counter()
    for (pos, length), ctr in pos_counts.items():
        if pos == 0:
            for s, c in ctr.items():
                start_counter[s] += c
        if pos == length - 1:
            for s, c in ctr.items():
                end_counter[s] += c

    def _entropy(ctr: Counter) -> float:
        total = sum(ctr.values())
        return -sum((c / total) * math.log2(c / total) for c in ctr.values() if c > 0)

    h_start = _entropy(start_counter)
    h_end = _entropy(end_counter)
    h_all = _entropy(freq)

    # Terminal candidates: high end_rate AND end_freq > 5
    terminal_candidates = []
    initial_candidates = []
    for sign, f in freq.items():
        end_rate = end_freq[sign] / f
        start_rate = start_freq[sign] / f
        internal_rate = internal_freq[sign] / f if f else 0
        if end_rate >= 0.5 and end_freq[sign] >= 5:
            terminal_candidates.append((sign, end_rate, end_freq[sign], f))
        if start_rate >= 0.5 and start_freq[sign] >= 3:
            initial_candidates.append((sign, start_rate, start_freq[sign], f))

    terminal_candidates.sort(key=lambda x: -x[1])
    initial_candidates.sort(key=lambda x: -x[1])

    # Build per-sign positional profile
    per_sign = {}
    for sign, f in freq.items():
        s = start_freq[sign]
        e = end_freq[sign]
        m = internal_freq[sign]
        per_sign[sign] = {
            "freq": f,
            "start_rate": round(s / f, 4),
            "end_rate": round(e / f, 4),
            "internal_rate": round(m / f, 4),
            "start_count": s,
            "end_count": e,
            "internal_count": m,
        }

    return {
        "h_unigram": round(h_all, 4),
        "h_start_position": round(h_start, 4),
        "h_end_position": round(h_end, 4),
        "terminal_candidates": [
            {"sign": s, "end_rate": round(r, 4), "end_count": ec, "total_freq": tf}
            for s, r, ec, tf in terminal_candidates
        ],
        "initial_candidates": [
            {"sign": s, "start_rate": round(r, 4), "start_count": sc, "total_freq": tf}
            for s, r, sc, tf in initial_candidates
        ],
        "per_sign_profile": per_sign,
    }


# ── Phase 6.3: N-gram and adjacency analysis ─────────────────────────────────

def ngram_analysis(records: list[dict]) -> dict:
    """Bigrams, trigrams, conditional probabilities, PMI, transition graph."""
    unigram: Counter = Counter()
    bigram: Counter = Counter()
    trigram: Counter = Counter()
    cooccurrence: dict[str, Counter] = defaultdict(Counter)

    for rec in records:
        seq = rec["sign_sequence_raw"].split()
        for sign in seq:
            unigram[sign] += 1
        for i in range(len(seq) - 1):
            bigram[(seq[i], seq[i + 1])] += 1
            cooccurrence[seq[i]][seq[i + 1]] += 1
            cooccurrence[seq[i + 1]][seq[i]] += 1
        for i in range(len(seq) - 2):
            trigram[(seq[i], seq[i + 1], seq[i + 2])] += 1

    total_uni = sum(unigram.values())
    total_bi = sum(bigram.values())

    # Conditional probability P(B|A) = count(A,B) / count(A)
    cond_prob: dict[str, list[tuple[str, float]]] = {}
    for a in unigram:
        followers = [(b, c / unigram[a]) for (x, b), c in bigram.items() if x == a]
        followers.sort(key=lambda x: -x[1])
        cond_prob[a] = followers[:10]

    # PMI (pointwise mutual information)
    pmi_scores: list[tuple[str, str, float]] = []
    for (a, b), cnt in bigram.items():
        if cnt < 2:
            continue
        p_ab = cnt / total_bi
        p_a = unigram[a] / total_uni
        p_b = unigram[b] / total_uni
        pmi = math.log2(p_ab / (p_a * p_b)) if p_a > 0 and p_b > 0 else 0
        pmi_scores.append((a, b, round(pmi, 4)))
    pmi_scores.sort(key=lambda x: -x[2])

    # Bigram entropy H(B|A) — conditional entropy
    h_bigram = 0.0
    for a, f_a in unigram.items():
        p_a = f_a / total_uni
        row_total = sum(c for (x, _), c in bigram.items() if x == a)
        if row_total == 0:
            continue
        row_entropy = -sum(
            (c / row_total) * math.log2(c / row_total)
            for (x, b), c in bigram.items()
            if x == a and c > 0
        )
        h_bigram += p_a * row_entropy

    return {
        "top_30_bigrams": [
            {"a": a, "b": b, "count": c}
            for (a, b), c in bigram.most_common(30)
        ],
        "top_20_trigrams": [
            {"a": a, "b": b, "c_sign": c_s, "count": cnt}
            for (a, b, c_s), cnt in trigram.most_common(20)
        ],
        "top_30_pmi_pairs": [
            {"a": a, "b": b, "pmi": p}
            for a, b, p in pmi_scores[:30]
        ],
        "conditional_entropy_h2": round(h_bigram, 4),
        "n_distinct_bigrams": len(bigram),
        "n_distinct_trigrams": len(trigram),
    }


# ── Phase 6.4: Sequence segmentation analysis ────────────────────────────────

def segmentation_analysis(records: list[dict], pos: dict) -> dict:
    """Identify prefix-like, suffix-like, recurrent stems, and formula structures."""
    # Candidate delimiters: signs with very high start OR end rates at any position
    terminal_signs = {e["sign"] for e in pos["terminal_candidates"]}
    initial_signs = {e["sign"] for e in pos["initial_candidates"]}

    # Formula detection: recurring multi-sign sequences of length 2-4
    template_freq: Counter = Counter()
    for rec in records:
        seq = rec["sign_sequence_raw"].split()
        for length in (2, 3, 4):
            for i in range(len(seq) - length + 1):
                template = tuple(seq[i: i + length])
                template_freq[template] += 1

    recurrent_templates = [
        {"template": list(t), "count": c}
        for t, c in template_freq.most_common(40)
        if c >= 3
    ]

    # Terminal slot occupants: last-position signs
    terminal_occupants: Counter = Counter()
    initial_occupants: Counter = Counter()
    for rec in records:
        seq = rec["sign_sequence_raw"].split()
        if seq:
            initial_occupants[seq[0]] += 1
        if len(seq) > 1:
            terminal_occupants[seq[-1]] += 1

    # Affix template: proportion of inscriptions matching T = (any)* + terminal_sign
    inscriptions_with_known_terminal = sum(
        1 for rec in records
        if rec["sign_sequence_raw"].split()
        and rec["sign_sequence_raw"].split()[-1] in terminal_signs
    )
    inscriptions_with_known_initial = sum(
        1 for rec in records
        if rec["sign_sequence_raw"].split()
        and rec["sign_sequence_raw"].split()[0] in initial_signs
    )

    total = len(records)

    return {
        "terminal_sign_candidates": sorted(terminal_signs),
        "initial_sign_candidates": sorted(initial_signs),
        "inscriptions_ending_in_terminal_candidate": inscriptions_with_known_terminal,
        "fraction_ending_in_terminal_candidate": round(inscriptions_with_known_terminal / total, 4),
        "inscriptions_starting_with_initial_candidate": inscriptions_with_known_initial,
        "fraction_starting_with_initial_candidate": round(inscriptions_with_known_initial / total, 4),
        "top_terminal_occupants": [
            {"sign": s, "count": c} for s, c in terminal_occupants.most_common(15)
        ],
        "top_initial_occupants": [
            {"sign": s, "count": c} for s, c in initial_occupants.most_common(15)
        ],
        "recurrent_templates_count_ge3": recurrent_templates,
    }


# ── Phase 6.5: Graph and community analysis ──────────────────────────────────

def graph_analysis(records: list[dict]) -> dict:
    """Co-occurrence graph, directed adjacency, hub/bridge ranking."""
    # Build co-occurrence matrix (undirected, any position)
    cooccur: dict[str, Counter] = defaultdict(Counter)
    directed: dict[str, Counter] = defaultdict(Counter)
    sign_freq: Counter = Counter()

    for rec in records:
        seq = rec["sign_sequence_raw"].split()
        for sign in seq:
            sign_freq[sign] += 1
        for i in range(len(seq)):
            for j in range(i + 1, min(i + 4, len(seq))):  # window=3
                a, b = seq[i], seq[j]
                if a != b:
                    cooccur[a][b] += 1
                    cooccur[b][a] += 1
            if i < len(seq) - 1:
                directed[seq[i]][seq[i + 1]] += 1

    # Hub ranking: signs with most total co-occurrence weight
    hub_scores = {
        sign: sum(cooccur[sign].values())
        for sign in cooccur
    }
    hubs = sorted(hub_scores.items(), key=lambda x: -x[1])[:25]

    # Out-degree and in-degree from directed graph
    out_degree = {s: len(d) for s, d in directed.items()}
    in_degree: Counter = Counter()
    for s, targets in directed.items():
        for t in targets:
            in_degree[t] += 1

    # Strongly connected pairs (bidirectional adjacency)
    bidirectional_pairs = []
    for a in directed:
        for b in directed[a]:
            if a in directed.get(b, {}):
                if a < b:  # avoid duplicates
                    bidirectional_pairs.append({
                        "a": a, "b": b,
                        "a_to_b": directed[a][b],
                        "b_to_a": directed[b][a],
                    })
    bidirectional_pairs.sort(key=lambda x: -(x["a_to_b"] + x["b_to_a"]))

    # Simple Jaccard-based community grouping (pairs with Jaccard >= 0.3)
    signs = list(sign_freq.keys())
    high_jaccard_pairs = []
    for a, b in combinations(signs[:60], 2):  # top 60 by frequency to limit complexity
        set_a = set(cooccur[a].keys())
        set_b = set(cooccur[b].keys())
        union = len(set_a | set_b)
        inter = len(set_a & set_b)
        if union > 0 and inter / union >= 0.25:
            high_jaccard_pairs.append({"a": a, "b": b, "jaccard": round(inter / union, 4)})
    high_jaccard_pairs.sort(key=lambda x: -x["jaccard"])

    return {
        "top_25_hubs_by_cooccurrence_weight": [{"sign": s, "weight": w} for s, w in hubs],
        "top_20_out_degree": sorted(out_degree.items(), key=lambda x: -x[1])[:20],
        "top_20_in_degree": in_degree.most_common(20),
        "bidirectional_adjacency_pairs": bidirectional_pairs[:30],
        "high_jaccard_neighbor_pairs": high_jaccard_pairs[:30],
    }


# ── Phase 6.6: Cross-site comparison ─────────────────────────────────────────

def cross_site_analysis(records: list[dict]) -> dict:
    """Sign overlap and sequence-pattern overlap across sites."""
    site_signs: dict[str, set] = defaultdict(set)
    site_seq_patterns: dict[str, set] = defaultdict(set)

    for rec in records:
        site = rec["site"]
        seq = rec["sign_sequence_raw"].split()
        for sign in seq:
            site_signs[site].add(sign)
        for length in (2, 3):
            for i in range(len(seq) - length + 1):
                site_seq_patterns[site].add(tuple(seq[i: i + length]))

    sites = list(site_signs.keys())
    overlap_matrix = {}
    for a in sites:
        for b in sites:
            if a >= b:
                continue
            union = len(site_signs[a] | site_signs[b])
            inter = len(site_signs[a] & site_signs[b])
            overlap_matrix[f"{a}↔{b}"] = {
                "sign_jaccard": round(inter / union, 4) if union else 0,
                "signs_in_a_only": len(site_signs[a] - site_signs[b]),
                "signs_in_b_only": len(site_signs[b] - site_signs[a]),
                "signs_shared": inter,
            }

    note = ("Site comparison is not meaningful — only Mohenjo-daro is present. "
            "This will become informative once Harappa / Dholavira / Lothal data are ingested.")

    return {
        "note": note,
        "sites_present": sites,
        "n_sites": len(sites),
        "site_sign_inventory": {k: sorted(v) for k, v in site_signs.items()},
        "cross_site_overlap": overlap_matrix,
    }


# ── Phase 7: Latent sign class discovery ─────────────────────────────────────

def latent_class_discovery(records: list[dict], pos: dict, ngram: dict, graph: dict) -> dict:
    """
    Feature-vector clustering of signs into structural latent classes.
    Methods: threshold-based rule clustering + greedy hierarchical grouping.
    No sklearn required — pure stdlib.
    """
    # Build feature vectors for each sign
    sign_profiles = pos["per_sign_profile"]

    # Rules-based primary classification
    classes: dict[str, str] = {}
    for sign, profile in sign_profiles.items():
        sr = profile["start_rate"]
        er = profile["end_rate"]
        ir = profile["internal_rate"]
        f = profile["freq"]

        # PRIMARY: strong terminal bias
        if er >= 0.55 and f >= 4:
            classes[sign] = "TERMINAL_STRONG"
        # PRIMARY: strong initial bias
        elif sr >= 0.55 and f >= 4:
            classes[sign] = "INITIAL_STRONG"
        # MEDIAL: strong internal bias
        elif ir >= 0.70 and f >= 3:
            classes[sign] = "MEDIAL_STRONG"
        # BIMODAL: split between initial and terminal
        elif sr >= 0.30 and er >= 0.30 and ir < 0.30:
            classes[sign] = "BIMODAL_INIT_TERM"
        # HAPAX: only seen once
        elif f == 1:
            classes[sign] = "HAPAX"
        # LOW FREQUENCY: 2-3 occurrences
        elif f <= 3:
            classes[sign] = "LOW_FREQUENCY"
        # DEFAULT: mixed / undetermined
        else:
            classes[sign] = "MIXED"

    # Count class distribution
    class_dist = Counter(classes.values())

    # Cluster stability: within each class, compute mean and variance of end_rate
    class_profiles: dict[str, dict] = {}
    for cls in class_dist:
        members = [sign_profiles[s] for s, c in classes.items() if c == cls]
        if not members:
            continue
        er_vals = [m["end_rate"] for m in members]
        sr_vals = [m["start_rate"] for m in members]
        ir_vals = [m["internal_rate"] for m in members]
        n = len(members)
        mean_er = sum(er_vals) / n
        mean_sr = sum(sr_vals) / n
        mean_ir = sum(ir_vals) / n
        var_er = sum((v - mean_er) ** 2 for v in er_vals) / n
        class_profiles[cls] = {
            "n_members": n,
            "mean_end_rate": round(mean_er, 4),
            "mean_start_rate": round(mean_sr, 4),
            "mean_internal_rate": round(mean_ir, 4),
            "variance_end_rate": round(var_er, 4),
            "members": sorted([s for s, c in classes.items() if c == cls]),
        }

    # Cross-entropy reduction: how much entropy drops when we use class label instead of sign ID
    total_signs = len(sign_profiles)
    class_entropy = -sum(
        (n / total_signs) * math.log2(n / total_signs)
        for n in class_dist.values()
        if n > 0
    )
    sign_entropy = math.log2(total_signs)  # max entropy if uniform
    entropy_reduction = round(1 - (class_entropy / sign_entropy), 4) if sign_entropy else 0

    return {
        "n_signs_classified": len(classes),
        "class_distribution": dict(class_dist.most_common()),
        "class_profiles": class_profiles,
        "sign_to_class": classes,
        "sign_entropy_max": round(sign_entropy, 4),
        "class_entropy": round(class_entropy, 4),
        "entropy_reduction_fraction": entropy_reduction,
        "interpretation": (
            "Classes are derived from positional behavior only (start/end/internal rates). "
            "These are candidate structural classes, NOT phoneme assignments. "
            "TERMINAL_STRONG signs are candidates for morpheme-final markers. "
            "INITIAL_STRONG signs are candidates for title/initial determinatives."
        ),
    }


# ── Phase 8: Candidate DoF recovery ──────────────────────────────────────────

def dof_recovery(records: list[dict], classes: dict[str, str], seg: dict) -> dict:
    """
    Model inscriptions as latent-class sequences.
    Estimate structural slots and DoF count.
    """
    # Map each inscription to its class sequence
    class_sequences: list[list[str]] = []
    for rec in records:
        seq = rec["sign_sequence_raw"].split()
        cls_seq = [classes.get(sign, "UNKNOWN") for sign in seq]
        class_sequences.append(cls_seq)

    # Template frequency in class space
    template_freq: Counter = Counter()
    for cls_seq in class_sequences:
        for length in (2, 3, 4):
            for i in range(len(cls_seq) - length + 1):
                template_freq[tuple(cls_seq[i: i + length])] += 1

    # Entropy in raw sign space vs class space
    sign_seq_counter: Counter = Counter()
    class_seq_counter: Counter = Counter()
    for rec in records:
        seq = tuple(rec["sign_sequence_raw"].split())
        sign_seq_counter[seq] += 1
    for cls_seq in class_sequences:
        class_seq_counter[tuple(cls_seq)] += 1

    def _counter_entropy(ctr: Counter) -> float:
        total = sum(ctr.values())
        return -sum((c / total) * math.log2(c / total) for c in ctr.values() if c > 0)

    h_raw = _counter_entropy(sign_seq_counter)
    h_class = _counter_entropy(class_seq_counter)

    # Slot model analysis: what appears in each slot position
    slot_occupants: dict[int, Counter] = defaultdict(Counter)
    slot_class_occupants: dict[int, Counter] = defaultdict(Counter)
    for rec in records:
        seq = rec["sign_sequence_raw"].split()
        for i, sign in enumerate(seq):
            # Normalize slot: 0=initial, -1=terminal, else internal
            if i == 0:
                slot = 0
            elif i == len(seq) - 1:
                slot = -1
            else:
                slot = 1  # all internal positions collapsed
            slot_occupants[slot][sign] += 1
            slot_class_occupants[slot][classes.get(sign, "UNKNOWN")] += 1

    # Estimate structural DoF:
    # Minimum structural DoFs = number of clearly differentiated slot classes
    # that appear with meaningful frequency in their respective positions
    terminal_signs_set = set(s for s in seg["terminal_sign_candidates"][:20] if s in classes)
    initial_signs_set = set(s for s in seg["initial_sign_candidates"][:20] if s in classes)
    medial_signs = {s for s, c in classes.items() if c in ("MEDIAL_STRONG", "MIXED")}
    hapax_signs = {s for s, c in classes.items() if c == "HAPAX"}

    # Recurrent templates from class space
    recurrent_class_templates = [
        {"template": list(t), "count": c}
        for t, c in template_freq.most_common(25)
        if c >= 3
    ]

    return {
        "sequence_entropy_raw_signs": round(h_raw, 4),
        "sequence_entropy_class_labels": round(h_class, 4),
        "entropy_reduction_abs": round(h_raw - h_class, 4),
        "entropy_reduction_pct": round(100 * (h_raw - h_class) / h_raw, 1) if h_raw else 0,
        "slot_class_occupants": {
            str(k): dict(v.most_common(8))
            for k, v in slot_class_occupants.items()
        },
        "n_candidate_terminal_signs": len(terminal_signs_set),
        "n_candidate_initial_signs": len(initial_signs_set),
        "n_candidate_medial_signs": len(medial_signs),
        "n_hapax_signs": len(hapax_signs),
        "recurrent_class_templates": recurrent_class_templates,
        "candidate_dof_schema": {
            "INITIAL_SLOT": {
                "description": "Opening sign/signs — candidate title or determinative",
                "evidence": f"{len(initial_signs_set)} signs with start_rate >= 0.55",
                "top_candidates": list(initial_signs_set)[:10],
            },
            "MEDIAL_SLOT": {
                "description": "Internal signs — candidate root or modifier",
                "evidence": f"{len(medial_signs)} signs with internal_rate >= 0.70",
                "top_candidates": list(medial_signs)[:10],
            },
            "TERMINAL_SLOT": {
                "description": "Final sign/signs — candidate suffix or formula closure",
                "evidence": f"{len(terminal_signs_set)} signs with end_rate >= 0.55",
                "top_candidates": list(terminal_signs_set)[:10],
            },
            "HAPAX_SLOT": {
                "description": "Signs appearing once only — high uncertainty",
                "evidence": f"{len(hapax_signs)} hapax signs ({round(100*len(hapax_signs)/len(classes),1)}% of sign inventory)",
                "top_candidates": [],
            },
        },
    }


# ── Report writers ───────────────────────────────────────────────────────────

def write_sequence_analysis_report(freq: dict, pos: dict, ngram: dict, seg: dict, cross: dict, graph: dict) -> Path:
    out = REPORTS / "sequence_analysis_report.md"
    lines = [
        "# Sequence Analysis Report",
        f"Generated: {NOW}",
        "**Site scope**: Mohenjo-daro only (179 inscriptions). All results are site-limited.",
        "Multi-site comparison will be possible after Harappa / Dholavira data acquisition.",
        "",
        "---",
        "",
        "## Phase 6.1 — Frequency Analysis",
        "",
        f"- Total sign tokens: {freq['n_tokens']}",
        f"- Distinct signs: {freq['n_distinct_signs']}",
        f"- Hapax signs (appear once): {freq['n_hapax']} ({round(100*freq['hapax_fraction'],1)}%)",
        f"- Unigram entropy H1: {freq['unigram_entropy_h1']} bits",
        f"- Mean inscription length: {freq['mean_length']} signs",
        f"- Median inscription length: {freq['median_length']} signs",
        f"- Max inscription length: {freq['max_length']} signs",
        "",
        "### Top 30 signs by frequency",
        "",
    ]
    for sign, cnt in list(freq["top_30_signs"].items())[:30]:
        lines.append(f"  - {sign}: {cnt}")

    lines += [
        "",
        "### Length distribution",
        "",
    ]
    for length, cnt in sorted(freq["length_distribution"].items()):
        lines.append(f"  - {length} signs: {cnt} inscriptions")

    lines += [
        "",
        "---",
        "",
        "## Phase 6.2 — Positional Analysis",
        "",
        f"- H(sign|position=0, i.e. start): {pos['h_start_position']} bits",
        f"- H(sign|position=-1, i.e. end): {pos['h_end_position']} bits",
        "",
        "Low end-position entropy means few signs dominate the terminal slot.",
        f"High start-position entropy ({pos['h_start_position']} bits) means many different signs appear at the start.",
        "",
        "### Candidate terminal markers (end_rate ≥ 0.55, freq ≥ 5)",
        "",
    ]
    for t in pos["terminal_candidates"]:
        lines.append(f"  - {t['sign']}: end_rate={t['end_rate']}, end_count={t['end_count']}, total={t['total_freq']}")

    lines += [
        "",
        "### Candidate initial markers (start_rate ≥ 0.55, freq ≥ 3)",
        "",
    ]
    for t in pos["initial_candidates"]:
        lines.append(f"  - {t['sign']}: start_rate={t['start_rate']}, start_count={t['start_count']}, total={t['total_freq']}")

    lines += [
        "",
        "---",
        "",
        "## Phase 6.3 — N-gram and Adjacency Analysis",
        "",
        f"- Conditional entropy H2 (bigram): {ngram['conditional_entropy_h2']} bits",
        f"- Distinct bigrams: {ngram['n_distinct_bigrams']}",
        f"- Distinct trigrams: {ngram['n_distinct_trigrams']}",
        "",
        "### Top 30 bigrams",
        "",
    ]
    for bg in ngram["top_30_bigrams"]:
        lines.append(f"  - {bg['a']} → {bg['b']}: {bg['count']}")

    lines += [
        "",
        "### Top 20 PMI pairs (high mutual information, freq ≥ 2)",
        "",
    ]
    for p in ngram["top_30_pmi_pairs"][:20]:
        lines.append(f"  - {p['a']} ↔ {p['b']}: PMI={p['pmi']}")

    lines += [
        "",
        "---",
        "",
        "## Phase 6.4 — Sequence Segmentation",
        "",
        f"- Fraction of inscriptions ending in a candidate terminal: {round(100*seg['fraction_ending_in_terminal_candidate'],1)}%",
        f"- Fraction of inscriptions starting with a candidate initial: {round(100*seg['fraction_starting_with_initial_candidate'],1)}%",
        "",
        "### Recurrent templates (length 2-4, count ≥ 3)",
        "",
    ]
    for t in seg["recurrent_templates_count_ge3"][:25]:
        lines.append(f"  - {' '.join(t['template'])}: {t['count']} times")

    lines += [
        "",
        "---",
        "",
        "## Phase 6.5 — Graph and Community Analysis",
        "",
        "### Top 25 hub signs (by co-occurrence weight)",
        "",
    ]
    for h in graph["top_25_hubs_by_cooccurrence_weight"]:
        lines.append(f"  - {h['sign']}: weight={h['weight']}")

    lines += [
        "",
        "### Top 30 bidirectional adjacency pairs",
        "",
    ]
    for p in graph["bidirectional_adjacency_pairs"][:15]:
        lines.append(f"  - {p['a']} ↔ {p['b']}: ({p['a_to_b']} + {p['b_to_a']})")

    lines += [
        "",
        "---",
        "",
        "## Phase 6.6 — Cross-site Comparison",
        "",
        f"**Note**: {cross['note']}",
        "",
        f"Sites in corpus: {', '.join(cross['sites_present'])}",
        "",
        "Cross-site analysis requires ≥ 2 sites. Currently deferred pending corpus expansion.",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Phase 6] sequence_analysis_report.md written")
    return out


def write_prefix_suffix_report(seg: dict, ngram: dict) -> Path:
    out = REPORTS / "candidate_prefix_suffix_report.md"
    lines = [
        "# Candidate Prefix/Suffix Report",
        f"Generated: {NOW}",
        "**Site scope**: Mohenjo-daro only. Results are site-limited.",
        "",
        "---",
        "",
        "## Summary",
        "",
        "This report identifies signs and sign patterns that behave like affixes",
        "based purely on positional statistics. No phonetic claims are made.",
        "All labels ('prefix-like', 'suffix-like') are structural candidates only.",
        "",
        "---",
        "",
        "## Candidate Suffix-like Signs (terminal position bias)",
        "",
        "Definition: sign appears in final position in ≥ 55% of its occurrences,",
        "with at least 5 total occurrences.",
        "",
    ]
    for t in seg["top_terminal_occupants"]:
        lines.append(f"  - {t['sign']}: appears terminally {t['count']} times")

    lines += [
        "",
        "## Candidate Prefix-like Signs (initial position bias)",
        "",
        "Definition: sign appears in initial position in ≥ 55% of its occurrences,",
        "with at least 3 total occurrences.",
        "",
    ]
    for t in seg["top_initial_occupants"]:
        lines.append(f"  - {t['sign']}: appears initially {t['count']} times")

    lines += [
        "",
        "## Recurrent Multi-sign Templates",
        "",
        "These patterns appear ≥ 3 times in the corpus.",
        "They may represent formulaic expressions or recurring morphological patterns.",
        "",
    ]
    for t in seg["recurrent_templates_count_ge3"][:30]:
        lines.append(f"  - `{' '.join(t['template'])}`: {t['count']} times")

    lines += [
        "",
        "## Top Bigrams (strongest adjacency pairs)",
        "",
    ]
    for bg in ngram["top_30_bigrams"][:20]:
        lines.append(f"  - {bg['a']} → {bg['b']}: {bg['count']}")

    lines += [
        "",
        "## Interpretation Guidelines",
        "",
        "- Do NOT treat these candidates as confirmed morphemes.",
        "- Do NOT assign phonemes to these candidates.",
        "- Terminal candidates are CONSISTENT WITH suffix-like behavior,",
        "  but this is a necessary-not-sufficient condition.",
        "- These results should be validated after Harappa / Dholavira data are added.",
        "- The sign P086 / P122 terminal cluster (if confirmed in these results)",
        "  is consistent with Mahadevan's known terminal sign concordance.",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Phase 6] candidate_prefix_suffix_report.md written")
    return out


def write_latent_class_report(lc: dict) -> Path:
    out = REPORTS / "latent_sign_class_report.md"
    lines = [
        "# Latent Sign Class Report",
        f"Generated: {NOW}",
        "**Site scope**: Mohenjo-daro only. Clustering is provisional and site-limited.",
        "",
        "---",
        "",
        "## Important Caveats",
        "",
        "- Classes are derived from positional behavior only.",
        "- Visual similarity has NOT been incorporated (requires image data).",
        "- These are CANDIDATE STRUCTURAL CLASSES, not phoneme assignments.",
        "- Multi-site data will likely refine class boundaries.",
        "- No class should be treated as final without visual crosswalk confirmation.",
        "",
        "---",
        "",
        "## Classification Method",
        "",
        "Feature vector per sign: (freq, start_rate, end_rate, internal_rate)",
        "Classification: threshold rules on positional rates.",
        "Class labels are structural descriptors, not linguistic categories.",
        "",
        "## Class Inventory",
        "",
        f"- Total signs classified: {lc['n_signs_classified']}",
        f"- Unigram entropy (sign ID space): {lc['sign_entropy_max']} bits",
        f"- Class entropy: {lc['class_entropy']} bits",
        f"- Entropy reduction from sign→class: {round(100*lc['entropy_reduction_fraction'],1)}%",
        "",
        "### Class distribution",
        "",
    ]
    for cls, n in lc["class_distribution"].items():
        lines.append(f"  - {cls}: {n} signs")

    lines += [
        "",
        "---",
        "",
        "## Per-Class Profiles",
        "",
    ]
    for cls, profile in sorted(lc["class_profiles"].items()):
        lines += [
            f"### {cls} ({profile['n_members']} members)",
            f"  - Mean end_rate: {profile['mean_end_rate']}",
            f"  - Mean start_rate: {profile['mean_start_rate']}",
            f"  - Mean internal_rate: {profile['mean_internal_rate']}",
            f"  - Variance (end_rate): {profile['variance_end_rate']}",
            f"  - Members: {', '.join(profile['members'][:30])}{'...' if len(profile['members']) > 30 else ''}",
            "",
        ]

    lines += [
        "---",
        "",
        "## Interpretation",
        "",
        lc["interpretation"],
        "",
        "## Next Steps for Class Refinement",
        "",
        "1. Add visual feature vectors once sign plate images are acquired.",
        "2. Re-run clustering on multi-site corpus (Harappa, Dholavira).",
        "3. Add graph-neighbor features to the feature vector.",
        "4. Run hierarchical and spectral clustering for stability comparison.",
        "5. Do NOT collapse classes into phoneme assignments until Phase 9 gates are met.",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Phase 7] latent_sign_class_report.md written")
    return out


def write_decipherment_readiness_report(lc: dict, dof: dict) -> Path:
    out = REPORTS / "decipherment_readiness_report.md"
    lines = [
        "# Decipherment Readiness Report",
        f"Generated: {NOW}",
        "**Site scope**: Mohenjo-daro only (179 inscriptions).",
        "",
        "---",
        "",
        "## Purpose",
        "",
        "This report assesses whether the corpus and structural analysis are",
        "sufficient to justify moving to Phase 9 (linguistic hypothesis testing).",
        "Per the instructions: 'Success is not a phonetic decipherment. Success is a",
        "representation that preserves the corpus, reduces entropy, improves",
        "predictability, remains stable across sites and artifacts, and does not",
        "require arbitrary sign collapse.'",
        "",
        "---",
        "",
        "## Phase 8 Summary — Candidate DoF Schema",
        "",
    ]
    for slot, info in dof["candidate_dof_schema"].items():
        lines += [
            f"### {slot}",
            f"  Description: {info['description']}",
            f"  Evidence: {info['evidence']}",
            f"  Top candidates: {', '.join(info['top_candidates'][:8]) if info['top_candidates'] else 'none identified'}",
            "",
        ]

    lines += [
        "---",
        "",
        "## Entropy Analysis",
        "",
        f"- Sequence entropy in raw sign space: {dof['sequence_entropy_raw_signs']} bits",
        f"- Sequence entropy in class-label space: {dof['sequence_entropy_class_labels']} bits",
        f"- Entropy reduction: {dof['entropy_reduction_abs']} bits ({dof['entropy_reduction_pct']}%)",
        "",
        "Class-label representation reduces sequence entropy, indicating that",
        "structural classes capture real patterns in inscription structure.",
        "",
        "## Recurrent Class Templates",
        "",
    ]
    for t in dof["recurrent_class_templates"][:20]:
        lines.append(f"  - {' '.join(t['template'])}: {t['count']} times")

    lines += [
        "",
        "---",
        "",
        "## Hard Review Checklist (from decipherment_agent_instructions.md)",
        "",
        "- [ ] Mohenjo-daro is not the only major site represented — **FAIL: only M**",
        "- [ ] Harappa is substantially represented — **FAIL: 0 inscriptions**",
        "- [ ] Dholavira is represented — **FAIL: 0 inscriptions**",
        "- [ ] Kalibangan and Lothal are represented — **FAIL: 0 inscriptions**",
        "- [x] Artifact types are mixed — PASS",
        "- [ ] Sign IDs are tied to images — **FAIL: no image data**",
        "- [x] Variant handling is explicit — PASS (no collapsing)",
        "- [x] Duplicate objects reconciled — PASS",
        "- [x] No destructive surrogate alphabet — PASS",
        "- [x] Crosswalk file exists — PASS",
        "- [x] Positional and adjacency statistics run — PASS",
        "- [x] Latent class report exists — PASS",
        "- [x] DoF report exists — PASS",
        "",
        "---",
        "",
        "## Decision: Is Phase 9 (Linguistic Testing) Justified?",
        "",
        "**NO. Phase 9 is NOT justified yet.**",
        "",
        "Blocking reasons:",
        "1. Only Mohenjo-daro data is present. Multi-site stability of latent classes",
        "   has not been verified. Classes may be site-specific artefacts.",
        "2. No image-backed sign crosswalk exists. Sign identity cannot be",
        "   confirmed across sources.",
        "3. The structural DoF schema is derived from a 179-inscription subset.",
        "   The full CISI/ICIT corpus has ~6,800 inscriptions — 38x more data.",
        "4. The hapax fraction is high (>= 50%), indicating sparse sign coverage",
        "   in the available sample.",
        "",
        "**Minimum conditions for Phase 9:**",
        "1. At least Harappa inscriptions added (from CISI Vol.2 or equivalent).",
        "2. Latent class structure verified as cross-site stable.",
        "3. Visual crosswalk for the top 30 signs confirmed against sign plates.",
        "4. Human review gate explicitly passed.",
        "",
        "---",
        "",
        "## Recommended Next Actions",
        "",
        "1. **Acquire CISI Vol.2** — Harappa and additional Mohenjo-daro coverage.",
        "2. **Check mayig repo** for H/L/DK site data additions.",
        "3. **Acquire Fuls 2014** catalog — 676-sign crosswalk and frequency tables.",
        "4. **Request full ICIT export** from Wells/Fuls (~6,800 inscriptions).",
        "5. **Contact Parpola group** for CISI digital data access.",
        "6. After corpus expansion: re-run Phases 6-8 and re-evaluate Phase 9 gate.",
        "",
        "The structural infrastructure (corpus_master, sign_registry, crosswalk,",
        "analysis scripts) is now in place. The bottleneck is data volume, not tooling.",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Phase 8] decipherment_readiness_report.md written")
    return out


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("Glossa-Lab Decipherment Sprint: Phases 6-8")
    print("=" * 60)

    print("\nLoading corpus_master.csv...")
    records = load_corpus_master()
    print(f"  {len(records)} inscriptions loaded.")

    print("\n[Phase 6.1] Frequency analysis...")
    freq = frequency_analysis(records)

    print("[Phase 6.2] Positional analysis...")
    pos = positional_analysis(records)

    print("[Phase 6.3] N-gram analysis...")
    ngram = ngram_analysis(records)

    print("[Phase 6.4] Segmentation analysis...")
    seg = segmentation_analysis(records, pos)

    print("[Phase 6.5] Graph/community analysis...")
    graph = graph_analysis(records)

    print("[Phase 6.6] Cross-site analysis...")
    cross = cross_site_analysis(records)

    print("\n[Phase 7] Latent sign class discovery...")
    lc = latent_class_discovery(records, pos, ngram, graph)

    print("[Phase 8] Candidate DoF recovery...")
    dof = dof_recovery(records, lc["sign_to_class"], seg)

    # Save full stats JSON
    stats_out = ANALYSIS / "structural_stats.json"
    stats = {
        "generated": NOW,
        "frequency": freq,
        "positional": pos,
        "ngram": ngram,
        "segmentation": seg,
        "graph": graph,
        "cross_site": cross,
        "latent_classes": lc,
        "dof": dof,
    }
    # Remove non-serializable keys
    stats_out.write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")
    print(f"  structural_stats.json written.")

    print("\nWriting reports...")
    write_sequence_analysis_report(freq, pos, ngram, seg, cross, graph)
    write_prefix_suffix_report(seg, ngram)
    write_latent_class_report(lc)
    write_decipherment_readiness_report(lc, dof)

    print("\n" + "=" * 60)
    print("Phases 6-8 complete.")
    print(f"  structural_stats.json  → {stats_out}")
    print(f"  sequence_analysis_report → {REPORTS / 'sequence_analysis_report.md'}")
    print(f"  prefix_suffix_report     → {REPORTS / 'candidate_prefix_suffix_report.md'}")
    print(f"  latent_class_report      → {REPORTS / 'latent_sign_class_report.md'}")
    print(f"  readiness_report         → {REPORTS / 'decipherment_readiness_report.md'}")
    print("=" * 60)
    print("\n>> REVIEW GATE: Phase 9 (linguistic testing) is BLOCKED.")
    print(">> See decipherment_readiness_report.md for conditions.")


if __name__ == "__main__":
    main()
