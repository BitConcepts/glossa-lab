"""Phase-127 (spec 021) — cross-compilation disagreement
diagnostic: pure machinery.

Ledger-sequence Phase-127 (2026-10-08). Implements the
frozen protocol of
specs/021-phase127-cross-compilation-diagnostic/spec.md:
a decomposition of Phase-125's observed disagreement
(median TV 0.636931 over the 16 PRIMARY judgeable pairs)
into sampling noise, crosswalk-ambiguity, and
composition components. This module NEVER re-scores
Phase-125 and issues no verdict: its outputs are null
distributions, intervals, and descriptive decompositions
only (spec 021 sections 0, 9).

Arms (spec sections 3-8):
  (a) Holdat split-half noise floor — per-sign token
      pools shuffled and halved; TV between halves;
      full-size estimate = split-half median / sqrt(2)
      (registered multinomial scaling approximation).
  (b) Matched-size subsampling — Holdat tokens subsampled
      without replacement to the mayig token count for
      the sign; primary statistic TV(subsample, disjoint
      remainder); secondary TV(subsample, full profile).
  (c) Inscription-level bootstrap — inscriptions of each
      compilation resampled with replacement
      independently; per-pair TV CIs and a CI for the
      median TV across the fixed judgeable set.
  (d) Crosswalk neighbourhood decomposition — for each
      judgeable primary pair, its all-pairs neighbourhood
      (rows sharing its P or its M), ambiguity share, and
      attributable TV = TV_primary - neighbourhood median
      TV (descriptive estimator, spec section 6).
  (e) Composition controls — profiles recomputed from
      stratum-restricted inscription lists; the caller
      supplies the restricted lists (metadata discipline
      lives in phase127_run).
  (f) Power grid — TV(subsample, remainder) noise at
      tokens-per-sign grid points, priced from arm (b)'s
      machinery.

Profiles / TV reuse phase113_battery and
phase125_cross_compilation conventions exactly. Token
pools here are positional-class label lists (0=INITIAL,
1=MEDIAL, 2=TERMINAL) built with the frozen convention.
No corpus data is hardcoded (H16): every input arrives
from the caller (phase127_run).
"""
from __future__ import annotations

import math
import random
from collections import Counter

from glossa_lab.phase113_battery import (
    positional_counts, profile_from_counts, tv_distance,
)
from glossa_lab.phase125_cross_compilation import median, percentile_type7

# ── Frozen constants (spec 021 sections 2-8) ──────────────
SEED_SPLIT_HALF = 127001        # arm (a) stream
SEED_MATCHED_SIZE = 127002      # arm (b) stream
SEED_BOOTSTRAP = 127003         # arm (c) stream
SEED_POWER = 127004             # arm (f) stream
B_MAIN = 999                    # replicates, arms (a)-(c)
B_POWER = 499                   # replicates per power grid point
POWER_GRID = (8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256)
PASS_TV_BOUND = 0.35            # frozen Phase-125 PASS bound (spec 019 6.2)
OBSERVED_MEDIAN_TV = 0.636931   # Phase-125 results of record

INITIAL, MEDIAL, TERMINAL = 0, 1, 2


def _round(x):
    return round(x, 6) if x is not None else None


def summary(values: list[float]) -> dict:
    """Median + type-7 95% percentile interval of a
    replicate distribution."""
    if not values:
        return {"median": None, "ci95_lo": None, "ci95_hi": None,
                "n_replicates": 0}
    return {
        "median": _round(median(values)),
        "ci95_lo": _round(percentile_type7(values, 2.5)),
        "ci95_hi": _round(percentile_type7(values, 97.5)),
        "n_replicates": len(values),
    }


# ── Token class-label pools (frozen convention) ───────────

def class_labels(inscriptions, sign: str) -> list[int]:
    """Positional-class labels of `sign`'s tokens, in
    inscription order: position 0 of a multi-sign
    inscription is INITIAL, the last is TERMINAL,
    everything else (including a sole token) is MEDIAL
    — the phase113_battery convention, per token."""
    labels: list[int] = []
    for ins in inscriptions:
        n = len(ins)
        for pos, tok in enumerate(ins):
            if tok != sign:
                continue
            if pos == 0 and n > 1:
                labels.append(INITIAL)
            elif pos == n - 1 and n > 1:
                labels.append(TERMINAL)
            else:
                labels.append(MEDIAL)
    return labels


def profile_from_labels(labels) -> tuple | None:
    """(I, M, T) share triple of a label sequence, or
    None if empty."""
    if not labels:
        return None
    counts = [0, 0, 0]
    for lab in labels:
        counts[lab] += 1
    return profile_from_counts(tuple(counts))


def tv_from_labels(a, b):
    pa, pb = profile_from_labels(a), profile_from_labels(b)
    if pa is None or pb is None:
        return None
    return tv_distance(pa, pb)


# ── Arm (a): split-half (spec section 3) ──────────────────

def split_half_replicates(pool: list[int], rng: random.Random,
                          b: int = B_MAIN) -> list[float]:
    """TV(first half, remainder) over b shuffles of the
    token pool (halves of size floor(n/2) / ceil(n/2))."""
    n = len(pool)
    if n < 2:
        return []
    half = n // 2
    out = []
    for _ in range(b):
        shuffled = list(pool)
        rng.shuffle(shuffled)
        tv = tv_from_labels(shuffled[:half], shuffled[half:])
        if tv is not None:
            out.append(tv)
    return out


def split_half_arm(pools: dict[str, list[int]], seed: int = SEED_SPLIT_HALF,
                   b: int = B_MAIN) -> dict:
    """Per-sign split-half summaries + the noise floor
    (median of per-sign median TVs) and its registered
    full-size estimate (floor / sqrt(2)). Signs are
    consumed in sorted key order from one stream."""
    rng = random.Random(seed)
    per_sign = {}
    medians = []
    for sign in sorted(pools):
        reps = split_half_replicates(pools[sign], rng, b=b)
        s = summary(reps)
        s["n_tokens"] = len(pools[sign])
        s["fullsize_median_tv_est"] = (
            _round(s["median"] / math.sqrt(2)) if s["median"] is not None
            else None)
        per_sign[sign] = s
        if s["median"] is not None:
            medians.append(s["median"])
    floor = median(medians) if medians else None
    return {
        "per_sign": per_sign,
        "noise_floor_median_tv": _round(floor),
        "noise_floor_fullsize_est": (
            _round(floor / math.sqrt(2)) if floor is not None else None),
        "b": b, "seed": seed,
    }


# ── Arms (b) + (f): subsample-vs-remainder (spec 4, 8) ───

def subsample_remainder_tv(pool: list[int], m: int,
                           rng: random.Random):
    """One draw: shuffle the pool, take the first m labels
    as the subsample and the rest as the remainder.
    Returns (tv_vs_remainder, tv_vs_full) or (None, None)
    if m <= 0 or no remainder exists."""
    n = len(pool)
    if m <= 0 or m >= n:
        return None, None
    shuffled = list(pool)
    rng.shuffle(shuffled)
    sub, rem = shuffled[:m], shuffled[m:]
    tv_rem = tv_from_labels(sub, rem)
    tv_full = tv_from_labels(sub, pool)
    return tv_rem, tv_full


def matched_size_arm(pools: dict[str, list[int]],
                     sizes: dict[str, int],
                     seed: int = SEED_MATCHED_SIZE,
                     b: int = B_MAIN,
                     observed_median: float = OBSERVED_MEDIAN_TV) -> dict:
    """Replicate-major: each replicate draws every sign
    (sorted order) once and records the median primary
    TV across signs. Per-sign distributions are collected
    alongside. Signs with size >= pool size are skipped
    (counted)."""
    rng = random.Random(seed)
    signs = sorted(pools)
    per_sign_primary: dict[str, list[float]] = {s: [] for s in signs}
    per_sign_full: dict[str, list[float]] = {s: [] for s in signs}
    replicate_medians: list[float] = []
    skipped = {s: 0 for s in signs}
    for _ in range(b):
        tvs = []
        for s in signs:
            tv_rem, tv_full = subsample_remainder_tv(pools[s], sizes[s], rng)
            if tv_rem is None:
                skipped[s] += 1
                continue
            per_sign_primary[s].append(tv_rem)
            per_sign_full[s].append(tv_full)
            tvs.append(tv_rem)
        if tvs:
            replicate_medians.append(median(tvs))
    dist = summary(replicate_medians)
    n_ge = sum(1 for m in replicate_medians if m >= observed_median)
    return {
        "per_sign": {
            s: {"n_tokens": len(pools[s]), "target_size": sizes[s],
                "primary_tv_sub_vs_remainder": summary(per_sign_primary[s]),
                "secondary_tv_sub_vs_full": summary(per_sign_full[s]),
                "n_skipped_replicates": skipped[s]}
            for s in signs},
        "median_tv_distribution": {
            **dist,
            "share_replicates_ge_observed": (
                _round(n_ge / len(replicate_medians))
                if replicate_medians else None),
            "observed_median_tv": observed_median,
        },
        "b": b, "seed": seed,
    }


def power_grid(pools: dict[str, list[int]], seed: int = SEED_POWER,
               b: int = B_POWER, grid=POWER_GRID,
               pass_bound: float = PASS_TV_BOUND) -> dict:
    """Spec section 8: per grid point n, per-replicate
    median TV(subsample-to-n, remainder) across the signs
    that contribute at n (pool size > n), plus the pooled
    per-sign distribution. Returns the grid records and
    the registered tokens-per-sign figures."""
    rng = random.Random(seed)
    signs = sorted(pools)
    records = []
    for n in grid:
        contributing = [s for s in signs if len(pools[s]) > n]
        pooled: list[float] = []
        replicate_medians: list[float] = []
        for _ in range(b):
            tvs = []
            for s in contributing:
                tv_rem, _ = subsample_remainder_tv(pools[s], n, rng)
                if tv_rem is not None:
                    pooled.append(tv_rem)
                    tvs.append(tv_rem)
            if tvs:
                replicate_medians.append(median(tvs))
        records.append({
            "tokens_per_sign": n,
            "n_signs_contributing": len(contributing),
            "signs_excluded": [s for s in signs if s not in contributing],
            "pooled_per_sign_tv_p95": _round(
                percentile_type7(pooled, 95) if pooled else None),
            "pooled_per_sign_tv_median": _round(
                median(pooled) if pooled else None),
            "median_tv_p95": _round(
                percentile_type7(replicate_medians, 95)
                if replicate_medians else None),
            "median_tv_median": _round(
                median(replicate_medians) if replicate_medians else None),
        })
    req_median = next((r["tokens_per_sign"] for r in records
                       if r["median_tv_p95"] is not None
                       and r["median_tv_p95"] <= pass_bound), None)
    req_persign = next((r["tokens_per_sign"] for r in records
                        if r["pooled_per_sign_tv_p95"] is not None
                        and r["pooled_per_sign_tv_p95"] <= pass_bound), None)
    return {
        "grid": records,
        "pass_bound": pass_bound,
        "tokens_per_sign_required_median_gate": req_median,
        "tokens_per_sign_required_per_sign": req_persign,
        "b": b, "seed": seed,
    }


# ── Arm (c): inscription bootstrap (spec section 5) ───────

def inscription_count_vectors(inscriptions, signs) -> list[dict]:
    """Per inscription, {sign: (nI, nM, nT)} positional
    counts under the frozen convention (via
    phase113_battery.positional_counts on the single
    inscription). Only the requested signs are tracked."""
    wanted = set(signs)
    out = []
    for ins in inscriptions:
        vec = {}
        for sign in wanted.intersection(ins):
            vec[sign] = positional_counts([ins], sign)
        out.append(vec)
    return out


def _profile_from_summed(vectors, drawn, sign):
    tot = [0, 0, 0]
    for idx in drawn:
        c = vectors[idx].get(sign)
        if c is not None:
            tot[0] += c[0]
            tot[1] += c[1]
            tot[2] += c[2]
    if sum(tot) == 0:
        return None
    return profile_from_counts(tuple(tot))


def bootstrap_arm(mayig_vectors, holdat_vectors, pairs,
                  seed: int = SEED_BOOTSTRAP, b: int = B_MAIN) -> dict:
    """pairs: list of (p_sign, m_sign) in registered order.
    Each replicate draws len(vectors) inscription indices
    with replacement per compilation, independently, and
    recomputes every pair's TV. The judgeable set is
    fixed: a pair whose sign has 0 tokens in a replicate
    is excluded from that replicate's median and counted.
    """
    rng = random.Random(seed)
    n_may, n_hol = len(mayig_vectors), len(holdat_vectors)
    per_pair: dict[str, list[float]] = {}
    exclusions: Counter = Counter()
    replicate_medians: list[float] = []
    for _ in range(b):
        drawn_may = [rng.randrange(n_may) for _ in range(n_may)]
        drawn_hol = [rng.randrange(n_hol) for _ in range(n_hol)]
        tvs = []
        for p_sign, m_sign in pairs:
            key = f"{p_sign}-{m_sign}"
            pp = _profile_from_summed(mayig_vectors, drawn_may, p_sign)
            hp = _profile_from_summed(holdat_vectors, drawn_hol, m_sign)
            if pp is None or hp is None:
                exclusions[key] += 1
                continue
            tv = tv_distance(pp, hp)
            per_pair.setdefault(key, []).append(tv)
            tvs.append(tv)
        if tvs:
            replicate_medians.append(median(tvs))
    return {
        "per_pair": {
            f"{p}-{m}": {**summary(per_pair.get(f"{p}-{m}", [])),
                         "n_excluded_replicates": exclusions[f"{p}-{m}"]}
            for p, m in pairs},
        "median_tv": summary(replicate_medians),
        "b": b, "seed": seed,
    }


# ── Arm (d): neighbourhood decomposition (spec section 6) ─

def neighbourhood_decomposition(all_pairs, primary_pair, tv_lookup) -> dict:
    """all_pairs: crosswalk pair dicts with parpola_id /
    mahadevan_id. tv_lookup(p, m) -> TV float or None
    (None = not judgeable at the frozen floor). The
    estimator is spec section 6's, verbatim."""
    p0, m0 = primary_pair["parpola_id"], primary_pair["mahadevan_id"]
    rows = {(r["parpola_id"], r["mahadevan_id"]) for r in all_pairs}
    neighbourhood = {(p, m) for (p, m) in rows if p == p0 or m == m0}
    others = sorted(neighbourhood - {(p0, m0)})
    alt_tvs = []
    alt_records = []
    for p, m in others:
        tv = tv_lookup(p, m)
        alt_records.append({"parpola_id": p, "mahadevan_id": m,
                            "tv": _round(tv), "judgeable": tv is not None})
        if tv is not None:
            alt_tvs.append(tv)
    tv_primary = tv_lookup(p0, m0)
    neigh_med = median(alt_tvs) if alt_tvs else None
    attributable = (tv_primary - neigh_med
                    if tv_primary is not None and neigh_med is not None
                    else None)
    return {
        "parpola_id": p0,
        "mahadevan_id": m0,
        "k_p_rows": sum(1 for (p, _m) in rows if p == p0),
        "k_m_rows": sum(1 for (_p, m) in rows if m == m0),
        "neighbourhood_size": len(neighbourhood),
        "ambiguity_share": (
            _round((len(neighbourhood) - 1) / len(neighbourhood))
            if neighbourhood else None),
        "tv_primary": _round(tv_primary),
        "n_neighbourhood_judgeable": len(alt_tvs),
        "neighbourhood_comparisons": alt_records,
        "neighbourhood_median_tv": _round(neigh_med),
        "attributable_tv": _round(attributable),
        "attributable_share": (
            _round(attributable / tv_primary)
            if attributable is not None and tv_primary else None),
    }


# ── Arm (e): composition-control evaluation (spec 7) ──────

def evaluate_pairs_on_contexts(pairs, mayig_ctx, holdat_ctx, floor: int = 8):
    """TV per pair under caller-supplied contexts (e.g. a
    stratum-restricted Holdat context), with the frozen
    floor re-applied to both sides' counts in those
    contexts. Returns per-pair records + the median TV
    over the judgeable subset."""
    from glossa_lab.phase125_cross_compilation import (
        profiles_from_context, w1_distance,
    )
    records = []
    tvs = []
    for pair in pairs:
        p_prof, p_n = profiles_from_context(mayig_ctx, pair["parpola_id"])
        m_prof, m_n = profiles_from_context(holdat_ctx, pair["mahadevan_id"])
        judgeable = (p_prof is not None and m_prof is not None
                     and p_n >= floor and m_n >= floor)
        tv = (round(tv_distance(p_prof, m_prof), 6) if judgeable else None)
        records.append({
            "parpola_id": pair["parpola_id"],
            "mahadevan_id": pair["mahadevan_id"],
            "mayig_n": p_n, "holdat_n_restricted": m_n,
            "judgeable_under_control": judgeable,
            "tv": tv,
            "w1": (round(w1_distance(p_prof, m_prof), 6)
                   if judgeable else None),
        })
        if judgeable:
            tvs.append(tv)
    return {
        "records": records,
        "n_judgeable": len(tvs),
        "median_tv": _round(median(tvs)) if tvs else None,
    }
