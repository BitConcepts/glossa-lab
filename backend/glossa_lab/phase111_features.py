"""Phase-111 frozen feature extractor (spec 009 section 4).

Computes the 28-feature vector (F01..F28) for one resampled draw.
A draw is a list of texts; each text is a list of integer token IDs
(the custodian remaps all tokens to ints before extraction).

Deterministic, numpy-only, no corpus knowledge: this module must
never learn which corpus a draw came from. All estimators and
constants are frozen by spec 009; changing any of them after the
spec freeze is a spec deviation (spec section 11).

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

import numpy as np

FEATURE_NAMES: list[str] = [
    "init80_frac",        # F01
    "term80_frac",        # F02
    "term_init_ratio",    # F03
    "hend_first",         # F04
    "hend_last",          # F05
    "term_productivity",  # F06
    "init_productivity",  # F07
    "blockH1",            # F08
    "blockH2",            # F09
    "blockH3",            # F10
    "blockH4",            # F11
    "cond_ent",           # F12
    "cond_ent_gap",       # F13
    "rep_adj_1",          # F14
    "rep_adj_2",          # F15
    "rep_adj_3",          # F16
    "hapax_prop",         # F17
    "heaps_beta",         # F18
    "ttr",                # F19
    "pp_ratio",           # F20
    "restore_acc",        # F21
    "zipf_slope",         # F22
    "top10_share",        # F23
    "cover80_frac",       # F24
    "vocab_K",            # F25
    "len_mean",           # F26
    "len_sd",             # F27
    "singleton_share",    # F28
]

_LN2 = np.log(2.0)
ALPHA = 0.1  # add-alpha smoothing for Markov features (frozen, spec section 4)


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


def _ngram_counts(texts: list[list[int]], k: int) -> dict[tuple[int, ...], int]:
    counts: dict[tuple[int, ...], int] = {}
    for t in texts:
        if len(t) < k:
            continue
        for i in range(len(t) - k + 1):
            key = tuple(t[i : i + k])
            counts[key] = counts.get(key, 0) + 1
    return counts


def _block_entropy(texts: list[list[int]], k: int) -> float:
    # Exact n-gram counting via a void-view of the sliding-window matrix
    # (works for any vocabulary size; deterministic).
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
    """Smallest number of top items whose mass reaches frac * total."""
    if total <= 0:
        return 0
    csum = np.cumsum(sorted_desc)
    return int(np.searchsorted(csum, frac * total) + 1)


def extract_features(texts: list[list[int]], draw_index: int) -> dict[str, float]:
    """Compute the frozen 28-feature vector for one draw.

    draw_index seeds the internal stochastic sub-procedures exactly as
    frozen in spec 009 section 4 (permutation gap, rarefaction,
    Markov split/masking).
    """
    texts = [t for t in texts if len(t) > 0]
    n_texts = len(texts)
    lengths = np.array([len(t) for t in texts], dtype=np.float64)
    n_tokens = int(lengths.sum())

    flat = np.array([tok for t in texts for tok in t], dtype=np.int64)
    vocab, counts = np.unique(flat, return_counts=True)
    K = len(vocab)
    counts_desc = np.sort(counts)[::-1]
    p = counts / n_tokens

    # ---- Positional (F01-F07) ----
    firsts = np.array([t[0] for t in texts], dtype=np.int64)
    lasts = np.array([t[-1] for t in texts], dtype=np.int64)
    _, first_counts = np.unique(firsts, return_counts=True)
    _, last_counts = np.unique(lasts, return_counts=True)
    init80_n = _cover_count(np.sort(first_counts)[::-1], 0.8, n_texts)
    term80_n = _cover_count(np.sort(last_counts)[::-1], 0.8, n_texts)

    h1 = _block_entropy(texts, 1)
    hend_first = _entropy_mm(first_counts.astype(np.float64)) / h1 if h1 > 0 else 0.0
    hend_last = _entropy_mm(last_counts.astype(np.float64)) / h1 if h1 > 0 else 0.0

    def _productivity(edge_tokens: np.ndarray, neighbour_offset: int) -> float:
        # top-10 edge signs by frequency; mean # distinct neighbours / K
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

    # ---- Entropy curve (F08-F13) ----
    block_h = [_block_entropy(texts, k) for k in (1, 2, 3, 4)]
    cond_ent = block_h[1] - block_h[0]
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

    # ---- Local repetition (F14-F16) ----
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

    # ---- Vocabulary growth (F17-F19) ----
    hapax_prop = float(np.sum(counts == 1)) / K if K else 0.0
    rng_rar = np.random.default_rng(np.random.SeedSequence([20261013, draw_index]))
    fracs = [0.125, 0.25, 0.5, 0.75, 1.0]
    rar_points: list[tuple[float, float]] = []
    order_base = np.arange(n_texts)
    for frac in fracs:
        target = frac * n_tokens
        type_means = []
        for _rep in range(5):
            order = order_base.copy()
            rng_rar.shuffle(order)
            acc_tokens = 0
            seen: set[int] = set()
            for idx in order:
                seen.update(texts[idx])
                acc_tokens += len(texts[idx])
                if acc_tokens >= target:
                    break
            type_means.append(len(seen))
        rar_points.append((target, float(np.mean(type_means))))
    xs = np.log(np.array([pt[0] for pt in rar_points]))
    ys = np.log(np.array([pt[1] for pt in rar_points]))
    if np.all(ys > 0) and len(set(xs.tolist())) >= 2:
        heaps_beta = float(np.polyfit(xs, ys, 1)[0])
    else:
        heaps_beta = 0.0

    # ---- Markov predictability (F20-F21) ----
    rng_split = np.random.default_rng(np.random.SeedSequence([20261014, draw_index]))
    idx = np.arange(n_texts)
    rng_split.shuffle(idx)
    n_train = int(round(0.8 * n_texts))
    train_texts = [texts[i] for i in idx[:n_train]]
    test_texts = [texts[i] for i in idx[n_train:]]

    train_flat = np.array([tok for t in train_texts for tok in t], dtype=np.int64)
    _, train_counts_all = np.unique(train_flat, return_counts=True)
    # map: token -> train count (tokens unseen in train get count 0)
    train_count_map: dict[int, int] = {}
    tv, tc = np.unique(train_flat, return_counts=True)
    for v, c in zip(tv.tolist(), tc.tolist()):
        train_count_map[int(v)] = int(c)
    bigram: dict[tuple[int, int], int] = {}
    unigram_ctx: dict[int, int] = {}
    for t in train_texts:
        for a, b in zip(t[:-1], t[1:]):
            bigram[(a, b)] = bigram.get((a, b), 0) + 1
            unigram_ctx[a] = unigram_ctx.get(a, 0) + 1
    n_train_tokens = int(len(train_flat))

    def _logp_uni(w: int) -> float:
        return np.log((train_count_map.get(w, 0) + ALPHA) / (n_train_tokens + ALPHA * K))

    def _logp_bi(prev: int, w: int) -> float:
        return np.log(
            (bigram.get((prev, w), 0) + ALPHA) / (unigram_ctx.get(prev, 0) + ALPHA * K)
        )

    ll_uni = 0.0
    ll_bi = 0.0
    n_test_tokens = 0
    for t in test_texts:
        for j, w in enumerate(t):
            ll_uni += _logp_uni(w)
            ll_bi += _logp_uni(w) if j == 0 else _logp_bi(t[j - 1], w)
            n_test_tokens += 1
    if n_test_tokens:
        pp_uni = float(np.exp(-ll_uni / n_test_tokens))
        pp_bi = float(np.exp(-ll_bi / n_test_tokens))
        pp_ratio = pp_bi / pp_uni if pp_uni > 0 else 1.0
    else:
        pp_ratio = 1.0

    rng_mask = np.random.default_rng(np.random.SeedSequence([20261015, draw_index]))
    # Group masked positions by left neighbour: the bigram argmax depends
    # only on the neighbour. Among max-count successors, ties break by
    # highest train unigram count, then lowest token ID (deterministic).
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
            # unseen context: every successor scores alpha/(alpha*K);
            # deterministic tiebreak = most frequent train token.
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
        mask[0] = False  # frozen: only positions >= 1 are restored by bigram
        for j in range(1, len(t)):
            if not mask[j]:
                continue
            masked += 1
            if _best_successor(t[j - 1]) == t[j]:
                correct += 1
    restore_acc = correct / masked if masked else 0.0

    # ---- Zipf / inventory (F22-F25) ----
    ranks = np.arange(1, K + 1, dtype=np.float64)
    if K >= 2:
        zipf_slope = float(np.polyfit(np.log(ranks), np.log(counts_desc.astype(np.float64)), 1)[0])
    else:
        zipf_slope = 0.0
    top10_share = float(np.sum(counts_desc[:10])) / n_tokens
    cover80 = _cover_count(counts_desc, 0.8, n_tokens)
    cover80_frac = cover80 / K if K else 0.0

    # ---- Length (F26-F28) ----
    len_mean = float(np.mean(lengths)) if n_texts else 0.0
    len_sd = float(np.std(lengths)) if n_texts else 0.0
    singleton_share = float(np.sum(lengths == 1)) / n_texts if n_texts else 0.0

    values = {
        "init80_frac": init80_n / K if K else 0.0,
        "term80_frac": term80_n / K if K else 0.0,
        "term_init_ratio": (term80_n / init80_n) if init80_n else 0.0,
        "hend_first": float(hend_first),
        "hend_last": float(hend_last),
        "term_productivity": term_prod,
        "init_productivity": init_prod,
        "blockH1": block_h[0],
        "blockH2": block_h[1],
        "blockH3": block_h[2],
        "blockH4": block_h[3],
        "cond_ent": cond_ent,
        "cond_ent_gap": cond_ent_gap,
        "rep_adj_1": rep_adj[0],
        "rep_adj_2": rep_adj[1],
        "rep_adj_3": rep_adj[2],
        "hapax_prop": hapax_prop,
        "heaps_beta": heaps_beta,
        "ttr": K / n_tokens if n_tokens else 0.0,
        "pp_ratio": pp_ratio,
        "restore_acc": restore_acc,
        "zipf_slope": zipf_slope,
        "top10_share": top10_share,
        "cover80_frac": cover80_frac,
        "vocab_K": float(K),
        "len_mean": len_mean,
        "len_sd": len_sd,
        "singleton_share": singleton_share,
    }
    return {name: float(values[name]) for name in FEATURE_NAMES}


def feature_matrix(draws: list[list[list[int]]]) -> np.ndarray:
    """Rows = draws, columns = FEATURE_NAMES order."""
    rows = []
    for i, draw in enumerate(draws):
        feats = extract_features(draw, draw_index=i)
        rows.append([feats[name] for name in FEATURE_NAMES])
    return np.array(rows, dtype=np.float64)
