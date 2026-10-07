"""Phase-113 candidate feature extractor (design stage).

New candidate families B (longer-range sequential) and C
(cross-text) for the blind affiliation program, defined on top of
the Phase-112 estimators and conventions: plug-in entropy with
Miller-Madow correction in bits, ALPHA = 0.1 smoothing, and the
frozen internal seed streams (Markov split [20261014, draw],
masking [20261015, draw]). Admission of any of these candidates to
a frozen study vector requires passing the pre-registered
permutation-sensitivity and statistical-power audits in
backend/scripts/phase113_feature_audit.py on KNOWN corpora only.

Deterministic, numpy-only, no corpus knowledge: this module never
learns which corpus a draw came from.

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from glossa_lab.phase112_features import (
    ALPHA,
    FEATURE_NAMES,
    _block_entropy,
    _entropy_mm,
    extract_candidates,
)

# Family B: longer-range sequential candidates.
NEW_CANDIDATES_B: list[str] = [
    "blockH5",
    "blockH6",
    "ent_incr_54",
    "ent_incr_65",
    "pp_ratio_ord3",
    "mi_lag2",
    "mi_lag3",
    "rep_adj_4",
    "rep_adj_5",
    "rep_adj_6",
    "adj_clustering_lag2",
    "restore_acc_tri",
    "ctx_pos_gain",
    "bigram_type_ratio_lag2",
]

# Family C: cross-text candidates (draw-level).
NEW_CANDIDATES_C: list[str] = [
    "dup_text_frac",
    "dup_token_coverage",
    "shared_bigram_type_frac",
    "cross_bigram_texts_mean",
    "longest_cross_repeat",
    "pair_bigram_overlap",
]

NEW_CANDIDATES: list[str] = NEW_CANDIDATES_B + NEW_CANDIDATES_C

# Ladder A: the 16 admitted Phase-112 features.
LADDER_A: list[str] = list(FEATURE_NAMES)


def _entropy_of_counter(counter: Counter) -> float:
    if not counter:
        return 0.0
    cnts = np.array([counter[key] for key in sorted(counter)], dtype=np.float64)
    return _entropy_mm(cnts)


def _mi_lag(texts: list[list[int]], lag: int, h1: float) -> float:
    if h1 == 0:
        return 0.0
    px: Counter = Counter()
    py: Counter = Counter()
    pxy: Counter = Counter()
    for t in texts:
        for j in range(len(t) - lag):
            a, b = t[j], t[j + lag]
            px[a] += 1
            py[b] += 1
            pxy[(a, b)] += 1
    if not pxy:
        return 0.0
    mi = _entropy_of_counter(px) + _entropy_of_counter(py) - _entropy_of_counter(pxy)
    return float(mi / h1)


def extract_new_candidates(texts: list[list[int]], draw_index: int) -> dict[str, float]:
    """Compute the Phase-113 new candidates (families B and C)."""
    texts = [t for t in texts if len(t) > 0]
    if not texts:
        return {name: (1.0 if name == "pp_ratio_ord3" else 0.0) for name in NEW_CANDIDATES}
    n_texts = len(texts)
    lengths = np.array([len(t) for t in texts], dtype=np.float64)
    n_tokens = int(lengths.sum())
    mean_len = float(lengths.mean()) if n_texts else 0.0
    max_len = int(lengths.max()) if n_texts else 0

    flat_counts: Counter = Counter(tok for t in texts for tok in t)
    K = len(flat_counts)
    p = np.array([flat_counts[key] for key in sorted(flat_counts)], dtype=np.float64)
    p = p / n_tokens if n_tokens else p
    exp_match = float(np.sum(p**2)) if K else 0.0

    # ---- Block entropy curve (k = 1..6) ----
    block_h = [_block_entropy(texts, k) for k in (1, 2, 3, 4, 5, 6)]
    h1 = block_h[0]

    # ---- Local repetition at distances 4, 5, 6 (phase112 construction) ----
    rep_adj: dict[int, float] = {}
    for d in (4, 5, 6):
        same = 0
        tot = 0
        for t in texts:
            if len(t) > d:
                a = np.array(t[:-d])
                b = np.array(t[d:])
                same += int(np.sum(a == b))
                tot += len(a)
        obs = same / tot if tot else 0.0
        rep_adj[d] = (obs - exp_match) / (1.0 - exp_match) if exp_match < 1 else 0.0

    # ---- Lag mutual information + lag-2 bigram type ratio ----
    mi_lag2 = _mi_lag(texts, 2, h1)
    mi_lag3 = _mi_lag(texts, 3, h1)
    lag2_types: set[tuple[int, int]] = set()
    n_lag2_tokens = 0
    for t in texts:
        for j in range(len(t) - 2):
            lag2_types.add((t[j], t[j + 2]))
            n_lag2_tokens += 1
    bigram_type_ratio_lag2 = len(lag2_types) / n_lag2_tokens if n_lag2_tokens else 0.0

    # ---- Lag-2 adjacency clustering ----
    adjacency: dict[int, set[int]] = {}
    for t in texts:
        for j in range(len(t) - 2):
            a, c = t[j], t[j + 2]
            if a != c:
                adjacency.setdefault(a, set()).add(c)
                adjacency.setdefault(c, set()).add(a)
    clus_vals: list[float] = []
    for v, nbrs in adjacency.items():
        deg = len(nbrs)
        if deg < 2:
            continue
        links = 0
        for u in nbrs:
            links += len(adjacency.get(u, set()) & nbrs)
        links //= 2
        clus_vals.append(links / (deg * (deg - 1) / 2))
    adj_clustering_lag2 = float(np.mean(clus_vals)) if clus_vals else 0.0

    # ---- Context + position-bin conditional entropy gain ----
    prev_c: Counter = Counter()
    pair_c: Counter = Counter()
    prev_bin_c: Counter = Counter()
    triple_c: Counter = Counter()
    for t in texts:
        lt = len(t)
        for j in range(lt - 1):
            prev, nxt = t[j], t[j + 1]
            b = (5 * (j + 1)) // lt
            prev_c[prev] += 1
            pair_c[(prev, nxt)] += 1
            prev_bin_c[(prev, b)] += 1
            triple_c[(prev, b, nxt)] += 1
    if pair_c:
        h_next_given_prev = _entropy_of_counter(pair_c) - _entropy_of_counter(prev_c)
        h_next_given_prev_bin = _entropy_of_counter(triple_c) - _entropy_of_counter(prev_bin_c)
        ctx_pos_gain = (
            float((h_next_given_prev - h_next_given_prev_bin) / h_next_given_prev)
            if h_next_given_prev > 0
            else 0.0
        )
    else:
        ctx_pos_gain = 0.0

    # ---- Frozen 80/20 split + Markov models (ord2 and ord3) ----
    rng_split = np.random.default_rng(np.random.SeedSequence([20261014, draw_index]))
    idx = np.arange(n_texts)
    rng_split.shuffle(idx)
    n_train = int(round(0.8 * n_texts))
    train_texts = [texts[i] for i in idx[:n_train]]
    test_texts = [texts[i] for i in idx[n_train:]]

    train_count_map: dict[int, int] = {}
    for t in train_texts:
        for tok in t:
            train_count_map[tok] = train_count_map.get(tok, 0) + 1
    n_train_tokens = int(sum(train_count_map.values()))
    bigram: dict[tuple[int, int], int] = {}
    unigram_ctx: dict[int, int] = {}
    trigram: dict[tuple[int, int, int], int] = {}
    bigram_ctx: dict[tuple[int, int], int] = {}
    quadgram: dict[tuple[int, int, int, int], int] = {}
    trigram_ctx: dict[tuple[int, int, int], int] = {}
    for t in train_texts:
        for a, b in zip(t[:-1], t[1:]):
            bigram[(a, b)] = bigram.get((a, b), 0) + 1
            unigram_ctx[a] = unigram_ctx.get(a, 0) + 1
        for a, b, c in zip(t[:-2], t[1:-1], t[2:]):
            trigram[(a, b, c)] = trigram.get((a, b, c), 0) + 1
            bigram_ctx[(a, b)] = bigram_ctx.get((a, b), 0) + 1
        for a, b, c, w in zip(t[:-3], t[1:-2], t[2:-1], t[3:]):
            quadgram[(a, b, c, w)] = quadgram.get((a, b, c, w), 0) + 1
            trigram_ctx[(a, b, c)] = trigram_ctx.get((a, b, c), 0) + 1

    def _p_uni(w: int) -> float:
        return (train_count_map.get(w, 0) + ALPHA) / (n_train_tokens + ALPHA * K)

    def _p_bi(prev: int, w: int) -> float:
        return (bigram.get((prev, w), 0) + ALPHA) / (unigram_ctx.get(prev, 0) + ALPHA * K)

    def _p_tri(a: int, b: int, w: int) -> float:
        ctx = bigram_ctx.get((a, b), 0)
        return (trigram.get((a, b, w), 0) + ALPHA * _p_bi(b, w)) / (ctx + ALPHA)

    def _p_quad(a: int, b: int, c: int, w: int) -> float:
        ctx = trigram_ctx.get((a, b, c), 0)
        return (quadgram.get((a, b, c, w), 0) + ALPHA * _p_tri(b, c, w)) / (ctx + ALPHA)

    ll_ord2 = 0.0
    ll_ord3 = 0.0
    n_test_tokens = 0
    if n_train_tokens and K:
        for t in test_texts:
            for j, w in enumerate(t):
                if j == 0:
                    lp_uni = np.log(_p_uni(w))
                    ll_ord2 += lp_uni
                    ll_ord3 += lp_uni
                elif j == 1:
                    lp_bi = np.log(_p_bi(t[0], w))
                    ll_ord2 += lp_bi
                    ll_ord3 += lp_bi
                elif j == 2:
                    lp_tri = np.log(_p_tri(t[0], t[1], w))
                    ll_ord2 += lp_tri
                    ll_ord3 += lp_tri
                else:
                    ll_ord2 += np.log(_p_tri(t[j - 2], t[j - 1], w))
                    ll_ord3 += np.log(_p_quad(t[j - 3], t[j - 2], t[j - 1], w))
                n_test_tokens += 1
    if n_test_tokens:
        pp_ord2 = float(np.exp(-ll_ord2 / n_test_tokens))
        pp_ord3 = float(np.exp(-ll_ord3 / n_test_tokens))
        pp_ratio_ord3 = pp_ord3 / pp_ord2 if pp_ord2 > 0 else 1.0
    else:
        pp_ratio_ord3 = 1.0

    # ---- Masked restoration with trigram prediction ----
    rng_mask = np.random.default_rng(np.random.SeedSequence([20261015, draw_index]))
    best_by_prev: dict[int, int] = {}
    best_by_tri: dict[tuple[int, int], int] = {}

    def _best_successor(prev: int) -> int:
        if prev in best_by_prev:
            return best_by_prev[prev]
        succ_counts = [(w, c) for (a, w), c in bigram.items() if a == prev]
        if succ_counts:
            max_c = max(c for _, c in succ_counts)
            cands = [w for w, c in succ_counts if c == max_c]
            best = min(cands, key=lambda w: (-train_count_map.get(w, 0), w))
        elif train_count_map:
            best = min(train_count_map.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        else:
            best = -1
        best_by_prev[prev] = best
        return best

    def _best_tri_successor(a: int, b: int) -> int:
        key = (a, b)
        if key in best_by_tri:
            return best_by_tri[key]
        succ_counts = [(w, c) for (x, y, w), c in trigram.items() if x == a and y == b]
        if succ_counts:
            max_c = max(c for _, c in succ_counts)
            cands = [w for w, c in succ_counts if c == max_c]
            best = min(cands, key=lambda w: (-train_count_map.get(w, 0), w))
        else:
            best = _best_successor(b)
        best_by_tri[key] = best
        return best

    correct = 0
    masked = 0
    for t in test_texts:
        if len(t) < 2:
            continue
        mask = rng_mask.random(len(t)) < 0.1
        mask[0] = False
        for j in range(1, len(t)):
            if not mask[j]:
                continue
            masked += 1
            pred = _best_successor(t[0]) if j == 1 else _best_tri_successor(t[j - 2], t[j - 1])
            if pred == t[j]:
                correct += 1
    restore_acc_tri = correct / masked if masked else 0.0

    # ---- Family C: cross-text structure ----
    tuple_counts: Counter = Counter(tuple(t) for t in texts)
    dup_tuples = {tpl for tpl, c in tuple_counts.items() if c >= 2}
    dup_texts = [t for t in texts if tuple(t) in dup_tuples]
    dup_text_frac = len(dup_texts) / n_texts if n_texts else 0.0
    dup_token_coverage = (
        sum(len(t) for t in dup_texts) / n_tokens if n_tokens else 0.0
    )

    bigram_counts: Counter = Counter()
    bigram_text_sets: dict[tuple[int, int], set[int]] = {}
    per_text_bigrams: list[Counter] = []
    n_bigram_tokens = 0
    for ti, t in enumerate(texts):
        bc: Counter = Counter(zip(t[:-1], t[1:]))
        per_text_bigrams.append(bc)
        bigram_counts.update(bc)
        n_bigram_tokens += sum(bc.values())
        for bg in bc:
            bigram_text_sets.setdefault(bg, set()).add(ti)
    if bigram_counts:
        shared_tokens = sum(
            c for bg, c in bigram_counts.items() if len(bigram_text_sets[bg]) >= 2
        )
        shared_bigram_type_frac = shared_tokens / n_bigram_tokens if n_bigram_tokens else 0.0
        cross_bigram_texts_mean = float(
            np.mean([len(s) / n_texts for s in bigram_text_sets.values()])
        )
    else:
        shared_bigram_type_frac = 0.0
        cross_bigram_texts_mean = 0.0

    longest_cross_repeat = 0.0
    if mean_len > 0:
        for n in range(min(12, max_len), 2, -1):
            first_seen: dict[tuple[int, ...], int] = {}
            found = False
            for ti, t in enumerate(texts):
                if len(t) < n:
                    continue
                for j in range(len(t) - n + 1):
                    ng = tuple(t[j : j + n])
                    if ng in first_seen:
                        if first_seen[ng] != ti:
                            found = True
                            break
                    else:
                        first_seen[ng] = ti
                if found:
                    break
            if found:
                longest_cross_repeat = n / mean_len
                break

    pair_bigram_overlap = 0.0
    if n_texts >= 2:
        rng_pairs = np.random.default_rng(np.random.SeedSequence([20261025, draw_index]))
        pairs = rng_pairs.integers(0, n_texts, size=(2000, 2))
        vals: list[float] = []
        totals = [int(sum(bc.values())) for bc in per_text_bigrams]
        for i_raw, j_raw in pairs:
            i, j = int(i_raw), int(j_raw)
            if i == j or totals[i] == 0 or totals[j] == 0:
                continue
            ci, cj = per_text_bigrams[i], per_text_bigrams[j]
            inter = sum(min(c, cj[bg]) for bg, c in ci.items() if bg in cj)
            vals.append(inter / min(totals[i], totals[j]))
        pair_bigram_overlap = float(np.mean(vals)) if vals else 0.0

    values = {
        "blockH5": block_h[4],
        "blockH6": block_h[5],
        "ent_incr_54": block_h[4] - block_h[3],
        "ent_incr_65": block_h[5] - block_h[4],
        "pp_ratio_ord3": pp_ratio_ord3,
        "mi_lag2": mi_lag2,
        "mi_lag3": mi_lag3,
        "rep_adj_4": rep_adj[4],
        "rep_adj_5": rep_adj[5],
        "rep_adj_6": rep_adj[6],
        "adj_clustering_lag2": adj_clustering_lag2,
        "restore_acc_tri": restore_acc_tri,
        "ctx_pos_gain": ctx_pos_gain,
        "bigram_type_ratio_lag2": bigram_type_ratio_lag2,
        "dup_text_frac": dup_text_frac,
        "dup_token_coverage": dup_token_coverage,
        "shared_bigram_type_frac": shared_bigram_type_frac,
        "cross_bigram_texts_mean": cross_bigram_texts_mean,
        "longest_cross_repeat": longest_cross_repeat,
        "pair_bigram_overlap": pair_bigram_overlap,
    }
    return {name: float(values[name]) for name in NEW_CANDIDATES}


def extract_all113(texts: list[list[int]], draw_index: int) -> dict[str, float]:
    """Phase-112 candidates merged with the Phase-113 new candidates."""
    merged = extract_candidates(texts, draw_index=draw_index)
    merged.update(extract_new_candidates(texts, draw_index=draw_index))
    return merged
