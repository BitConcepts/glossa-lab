"""Phase-112 candidate feature extractor (spec 010, design stage).

ORDER-CARRYING features only. Phase-111 (spec 009) proved that a
28-feature vector dominated by unigram statistics classifies even
order-destroyed Indus nulls as linguistic; Phase-112 admits only
features whose distributions change materially under within-text
permutation. Every candidate here is therefore permutation-sensitive
by construction; admission to the frozen study vector additionally
requires passing the pre-registered permutation-sensitivity audit
(backend/scripts/phase112_feature_audit.py) on KNOWN corpora only.

Definitions of inherited candidates are byte-for-byte the spec 009
section 4 computations (same estimators, same seeds, same
constants); the permutation-invariant spec-009 features (blockH1 as
a standalone, hapax_prop, heaps_beta, ttr, zipf_slope, top10_share,
cover80_frac, vocab_K, len_mean, len_sd, singleton_share) are NOT
computed here. New candidates (cond_ent2, ent_incr_43, pp_ratio_tri,
bigram_type_ratio, adj_clustering, fl_mi) are defined in spec 010
section 4.

Deterministic, numpy-only, no corpus knowledge: this module never
learns which corpus a draw came from.

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

import numpy as np

# All permutation-sensitive candidates (design stage). Spec 010
# section 4 freezes the ADMITTED subset into FEATURE_NAMES after the
# audit; extract_features returns exactly FEATURE_NAMES.
CANDIDATE_FEATURES: list[str] = [
    "init80_frac",        # spec009 F01 (positional)
    "term80_frac",        # spec009 F02
    "term_init_ratio",    # spec009 F03
    "hend_first",         # spec009 F04
    "hend_last",          # spec009 F05
    "term_productivity",  # spec009 F06
    "init_productivity",  # spec009 F07
    "blockH2",            # spec009 F09 (entropy curve)
    "blockH3",            # spec009 F10
    "blockH4",            # spec009 F11
    "cond_ent",           # spec009 F12
    "cond_ent_gap",       # spec009 F13
    "cond_ent2",          # NEW: H3 - H2 (second-order conditional entropy)
    "ent_incr_43",        # NEW: H4 - H3 (entropy-curve increment)
    "rep_adj_1",          # spec009 F14 (local repetition)
    "rep_adj_2",          # spec009 F15
    "rep_adj_3",          # spec009 F16
    "pp_ratio",           # spec009 F20 (Markov predictability)
    "restore_acc",        # spec009 F21
    "pp_ratio_tri",       # NEW: trigram pp / bigram pp (order-2 vs order-1)
    "bigram_type_ratio",  # NEW: distinct bigrams / bigram tokens
    "adj_clustering",     # NEW: token-adjacency graph clustering
    "fl_mi",              # NEW: MI(first token; last token) / H1
]

FEATURE_NAMES: list[str] = list(CANDIDATE_FEATURES)

_LN2 = np.log(2.0)
ALPHA = 0.1  # add-alpha smoothing for Markov features (frozen, spec 009)


def _entropy_mm(counts: np.ndarray) -> float:
    """Plug-in entropy in bits with Miller-Madow correction."""
    counts = counts[counts > 0]
    n = counts.sum()
    if n == 0:
        return 0.0
    p = counts / n
    h = -float(np.sum(p * np.log2(p)))
    m = len(counts)
    return h + (m - 1) / (2.0 * n * _LN2)


def _block_entropy(texts: list[list[int]], k: int) -> float:
    windows: list[np.ndarray] = []
    for t in texts:
        if len(t) < k:
            continue
        arr = np.array(t, dtype=np.int64)
        win = np.lib.stride_tricks.sliding_window_view(arr, k)
        windows.append(win)
    if not windows:
        return 0.0
    all_win = np.concatenate(windows, axis=0)
    void_view = np.ascontiguousarray(all_win).view(
        np.dtype((np.void, all_win.dtype.itemsize * k))
    )
    _, cnts = np.unique(void_view, return_counts=True)
    return _entropy_mm(cnts.astype(np.float64))


def _cover_count(sorted_desc: np.ndarray, frac: float, total: float) -> int:
    if total <= 0:
        return 0
    csum = np.cumsum(sorted_desc)
    return int(np.searchsorted(csum, frac * total) + 1)


def extract_candidates(texts: list[list[int]], draw_index: int) -> dict[str, float]:
    """Compute ALL candidate features for one draw.

    draw_index seeds the internal stochastic sub-procedures with the
    spec 009 seed streams (permutation gap [20261012], Markov split
    [20261014], masking [20261015]).
    """
    texts = [t for t in texts if len(t) > 0]
    n_texts = len(texts)
    lengths = np.array([len(t) for t in texts], dtype=np.float64)
    n_tokens = int(lengths.sum())

    flat = np.array([tok for t in texts for tok in t], dtype=np.int64)
    _, counts = np.unique(flat, return_counts=True)
    K = len(counts)
    p = counts / n_tokens

    # ---- Positional (spec009 F01-F07 definitions) ----
    firsts = np.array([t[0] for t in texts], dtype=np.int64)
    lasts = np.array([t[-1] for t in texts], dtype=np.int64)
    _, first_counts = np.unique(firsts, return_counts=True)
    _, last_counts = np.unique(lasts, return_counts=True)
    init80_n = _cover_count(np.sort(first_counts)[::-1], 0.8, n_texts)
    term80_n = _cover_count(np.sort(last_counts)[::-1], 0.8, n_texts)

    block_h = [_block_entropy(texts, k) for k in (1, 2, 3, 4)]
    h1 = block_h[0]
    hend_first = _entropy_mm(first_counts.astype(np.float64)) / h1 if h1 > 0 else 0.0
    hend_last = _entropy_mm(last_counts.astype(np.float64)) / h1 if h1 > 0 else 0.0

    def _productivity(edge_tokens: np.ndarray, neighbour_offset: int) -> float:
        vals, cnts = np.unique(edge_tokens, return_counts=True)
        top = vals[np.argsort(cnts)[::-1][:10]]
        neigh: dict[int, set[int]] = {int(s): set() for s in top}
        for t in texts:
            if len(t) < 2:
                continue
            edge = t[-1] if neighbour_offset < 0 else t[0]
            if edge in neigh:
                nb = t[-2] if neighbour_offset < 0 else t[1]
                neigh[edge].add(nb)
        if not top.size:
            return 0.0
        return float(np.mean([len(s) for s in neigh.values()])) / K

    term_prod = _productivity(lasts, -1)
    init_prod = _productivity(firsts, +1)

    # ---- Entropy curve (spec009 F09-F13 + new increments) ----
    cond_ent = block_h[1] - block_h[0]
    cond_ent2 = block_h[2] - block_h[1]
    ent_incr_43 = block_h[3] - block_h[2]
    rng_perm = np.random.default_rng(np.random.SeedSequence([20261012, draw_index]))
    perm_conds = []
    for _ in range(20):
        perm_texts = []
        for t in texts:
            arr = np.array(t, dtype=np.int64)
            rng_perm.shuffle(arr)
            perm_texts.append(arr.tolist())
        perm_conds.append(_block_entropy(perm_texts, 2) - block_h[0])
    cond_ent_gap = cond_ent - float(np.mean(perm_conds))

    # ---- Local repetition (spec009 F14-F16 definitions) ----
    exp_match = float(np.sum(p**2))
    rep_adj = []
    for d in (1, 2, 3):
        same = 0
        tot = 0
        for t in texts:
            if len(t) > d:
                a = np.array(t[:-d])
                b = np.array(t[d:])
                same += int(np.sum(a == b))
                tot += len(a)
        obs = same / tot if tot else 0.0
        rep_adj.append((obs - exp_match) / (1.0 - exp_match) if exp_match < 1 else 0.0)

    # ---- Bigram inventory + adjacency topology (new) ----
    bigram_counts: dict[tuple[int, int], int] = {}
    adjacency: dict[int, set[int]] = {}
    n_bigram_tokens = 0
    for t in texts:
        for a, b in zip(t[:-1], t[1:]):
            bigram_counts[(a, b)] = bigram_counts.get((a, b), 0) + 1
            n_bigram_tokens += 1
            if a != b:
                adjacency.setdefault(a, set()).add(b)
                adjacency.setdefault(b, set()).add(a)
    bigram_type_ratio = (
        len(bigram_counts) / n_bigram_tokens if n_bigram_tokens else 0.0
    )
    clus_vals: list[float] = []
    for v, nbrs in adjacency.items():
        deg = len(nbrs)
        if deg < 2:
            continue
        links = 0
        for u in nbrs:
            links += len(adjacency.get(u, set()) & nbrs)
        links //= 2  # each neighbour-neighbour edge counted twice
        clus_vals.append(links / (deg * (deg - 1) / 2))
    adj_clustering = float(np.mean(clus_vals)) if clus_vals else 0.0

    # ---- First-last mutual information (new) ----
    if n_texts and h1 > 0:
        joint: dict[tuple[int, int], int] = {}
        for t in texts:
            key = (t[0], t[-1])
            joint[key] = joint.get(key, 0) + 1
        h_first = _entropy_mm(first_counts.astype(np.float64))
        h_last = _entropy_mm(last_counts.astype(np.float64))
        h_joint = _entropy_mm(np.array(list(joint.values()), dtype=np.float64))
        fl_mi = (h_first + h_last - h_joint) / h1
    else:
        fl_mi = 0.0

    # ---- Markov predictability (spec009 F20-F21 + trigram ratio) ----
    rng_split = np.random.default_rng(np.random.SeedSequence([20261014, draw_index]))
    idx = np.arange(n_texts)
    rng_split.shuffle(idx)
    n_train = int(round(0.8 * n_texts))
    train_texts = [texts[i] for i in idx[:n_train]]
    test_texts = [texts[i] for i in idx[n_train:]]

    train_flat = np.array([tok for t in train_texts for tok in t], dtype=np.int64)
    train_count_map: dict[int, int] = {}
    tv, tc = np.unique(train_flat, return_counts=True)
    for v, c in zip(tv.tolist(), tc.tolist()):
        train_count_map[int(v)] = int(c)
    bigram: dict[tuple[int, int], int] = {}
    unigram_ctx: dict[int, int] = {}
    trigram: dict[tuple[int, int, int], int] = {}
    bigram_ctx: dict[tuple[int, int], int] = {}
    for t in train_texts:
        for a, b in zip(t[:-1], t[1:]):
            bigram[(a, b)] = bigram.get((a, b), 0) + 1
            unigram_ctx[a] = unigram_ctx.get(a, 0) + 1
        for a, b, c in zip(t[:-2], t[1:-1], t[2:]):
            trigram[(a, b, c)] = trigram.get((a, b, c), 0) + 1
            bigram_ctx[(a, b)] = bigram_ctx.get((a, b), 0) + 1
    n_train_tokens = int(len(train_flat))

    def _logp_uni(w: int) -> float:
        return np.log((train_count_map.get(w, 0) + ALPHA) / (n_train_tokens + ALPHA * K))

    def _p_bi(prev: int, w: int) -> float:
        return (bigram.get((prev, w), 0) + ALPHA) / (unigram_ctx.get(prev, 0) + ALPHA * K)

    def _logp_bi(prev: int, w: int) -> float:
        return np.log(_p_bi(prev, w))

    def _logp_tri(a: int, b: int, w: int) -> float:
        ctx = bigram_ctx.get((a, b), 0)
        p_tri = (trigram.get((a, b, w), 0) + ALPHA * _p_bi(b, w)) / (ctx + ALPHA)
        return np.log(p_tri)

    ll_uni = 0.0
    ll_bi = 0.0
    ll_tri = 0.0
    n_test_tokens = 0
    for t in test_texts:
        for j, w in enumerate(t):
            ll_uni += _logp_uni(w)
            if j == 0:
                ll_bi += _logp_uni(w)
                ll_tri += _logp_uni(w)
            elif j == 1:
                ll_bi += _logp_bi(t[0], w)
                ll_tri += _logp_bi(t[0], w)
            else:
                ll_bi += _logp_bi(t[j - 1], w)
                ll_tri += _logp_tri(t[j - 2], t[j - 1], w)
            n_test_tokens += 1
    if n_test_tokens:
        pp_uni = float(np.exp(-ll_uni / n_test_tokens))
        pp_bi = float(np.exp(-ll_bi / n_test_tokens))
        pp_tri = float(np.exp(-ll_tri / n_test_tokens))
        pp_ratio = pp_bi / pp_uni if pp_uni > 0 else 1.0
        pp_ratio_tri = pp_tri / pp_bi if pp_bi > 0 else 1.0
    else:
        pp_ratio = 1.0
        pp_ratio_tri = 1.0

    rng_mask = np.random.default_rng(np.random.SeedSequence([20261015, draw_index]))
    best_by_prev: dict[int, int] = {}

    def _best_successor(prev: int) -> int:
        if prev in best_by_prev:
            return best_by_prev[prev]
        succ_counts = [(w, c) for (a, w), c in bigram.items() if a == prev]
        if succ_counts:
            max_c = max(c for _, c in succ_counts)
            cands = [w for w, c in succ_counts if c == max_c]
            best = min(cands, key=lambda w: (-train_count_map.get(w, 0), w))
        else:
            best = min(
                train_count_map.items(), key=lambda kv: (-kv[1], kv[0])
            )[0]
        best_by_prev[prev] = best
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
            if _best_successor(t[j - 1]) == t[j]:
                correct += 1
    restore_acc = correct / masked if masked else 0.0

    values = {
        "init80_frac": init80_n / K if K else 0.0,
        "term80_frac": term80_n / K if K else 0.0,
        "term_init_ratio": (term80_n / init80_n) if init80_n else 0.0,
        "hend_first": float(hend_first),
        "hend_last": float(hend_last),
        "term_productivity": term_prod,
        "init_productivity": init_prod,
        "blockH2": block_h[1],
        "blockH3": block_h[2],
        "blockH4": block_h[3],
        "cond_ent": cond_ent,
        "cond_ent_gap": cond_ent_gap,
        "cond_ent2": cond_ent2,
        "ent_incr_43": ent_incr_43,
        "rep_adj_1": rep_adj[0],
        "rep_adj_2": rep_adj[1],
        "rep_adj_3": rep_adj[2],
        "pp_ratio": pp_ratio,
        "restore_acc": restore_acc,
        "pp_ratio_tri": pp_ratio_tri,
        "bigram_type_ratio": bigram_type_ratio,
        "adj_clustering": adj_clustering,
        "fl_mi": fl_mi,
    }
    return {name: float(values[name]) for name in CANDIDATE_FEATURES}


def extract_features(texts: list[list[int]], draw_index: int) -> dict[str, float]:
    """The frozen study vector: FEATURE_NAMES subset of the candidates."""
    all_vals = extract_candidates(texts, draw_index)
    return {name: all_vals[name] for name in FEATURE_NAMES}


def feature_matrix(draws: list[list[list[int]]]) -> np.ndarray:
    rows = []
    for i, draw in enumerate(draws):
        feats = extract_features(draw, draw_index=i)
        rows.append([feats[name] for name in FEATURE_NAMES])
    return np.array(rows, dtype=np.float64)
