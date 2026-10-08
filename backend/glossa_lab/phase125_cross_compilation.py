"""Phase-125 (spec 019) — cross-compilation positional
comparison: pure machinery.

Ledger-sequence Phase-125 (2026-10-08). Implements the
frozen protocol of
specs/019-phase125-cross-compilation-positional/spec.md:

  * Arms (spec section 3): PRIMARY = crosswalk pairs with
    confidence "high" that are unambiguous within the
    high-confidence pair set (each P and each M in exactly
    one high pair); SENSITIVITY A = confidence in
    {high, medium} with the same uniqueness rule
    (crosswalk v1 has zero medium pairs — arm A is run and
    reported, and its expected coincidence with PRIMARY
    is a registered design fact, not an independent
    check); SENSITIVITY B = every pair row, judged
    pair-by-pair (ambiguity included as separate pair
    comparisons). Arms are never pooled.
  * Profiles (spec section 4): computed strictly inside
    one compilation from that compilation's inscriptions
    alone, reusing phase113_battery's positional counts /
    profile / TV / modal-class conventions unchanged. No
    function in this module ever receives a merged
    cross-compilation token set.
  * Floor (spec section 4.2): a pair is judgeable iff
    the P sign has >= 8 mayig tokens AND the M sign has
    >= 8 Holdat tokens, each counted within its own
    compilation. Below-floor pairs are counted and
    excluded, never imputed, and are not scored.
  * Statistics (spec section 5): per-pair TV (gated
    statistic: median over judgeable pairs), per-pair
    ordinal W1 (recorded, not gated), Spearman rho on
    initial rates and on terminal rates (gated), modal
    agreement share (descriptive), and a pairing-shuffle
    permutation null (B = 999, seed 125125; gated) —
    agreement must beat wrong pairings of the same
    profiles.
  * Verdict (spec section 6, PRIMARY arm only, in
    order): NULL-STARVED if judgeable < 12; PASS iff
    median TV <= 0.35 and both gated rhos >= 0.50 and
    p_null <= 0.05; FAIL iff median TV >= 0.50 and
    p_null > 0.05 (the falsifier: far apart AND the
    pairing no better than shuffled); otherwise
    NULL-INCONCLUSIVE.

No SA artifact, no anchor data, and no object-level
join of any kind is an input to anything here (spec
sections 2.1, A3-A5). The corpora arrive as inscription
lists supplied by the caller (phase125_run), so this
module is testable on toy corpora.
"""
from __future__ import annotations

import random
from collections import Counter

from glossa_lab.phase113_battery import (
    CorpusContext, modal_class, positional_counts,
    profile_from_counts, tv_distance,
)

# ── Frozen constants (spec 019 sections 3-6) ──────────────
FLOOR = 8                 # tokens per sign per compilation (section 4.2)
STARVED_MIN = 12          # primary judgeable count bound (section 6.1)
TV_PASS_MAX = 0.35        # median TV for PASS (section 6.2)
TV_FAIL_MIN = 0.50        # median TV for FAIL (section 6.3)
RHO_MIN = 0.50            # Spearman rho for PASS (section 6.2)
P_NULL_MAX = 0.05         # shuffle-null p for PASS (section 6.2)
NULL_B = 999              # permutation replicates (section 5)
NULL_SEED = 125125        # permutation stream seed (section 5)

PASS = "PASS"
FAIL = "FAIL"
NULL = "NULL"
STARVED = "STARVED"
INCONCLUSIVE = "INCONCLUSIVE"

ARM_PRIMARY = "primary"
ARM_SENSITIVITY_A = "sensitivity_a_medium_included"
ARM_SENSITIVITY_B = "sensitivity_b_all_pairs"
ARM_ORDER = (ARM_PRIMARY, ARM_SENSITIVITY_A, ARM_SENSITIVITY_B)


# ── Arms (spec section 3) ─────────────────────────────────

def _unique_pairs(pairs: list[dict]) -> list[dict]:
    """Pairs whose P and M each appear exactly once in
    this pair set (the arm's unambiguity rule)."""
    p_counts = Counter(r["parpola_id"] for r in pairs)
    m_counts = Counter(r["mahadevan_id"] for r in pairs)
    return [r for r in pairs
            if p_counts[r["parpola_id"]] == 1
            and m_counts[r["mahadevan_id"]] == 1]


def build_arms(rows: list[dict]) -> dict[str, list[dict]]:
    """Build the three frozen arms from crosswalk rows.

    `rows` are crosswalk v1 rows; rows with no
    mahadevan_id (the unmapped-P rows) belong to no arm.
    Returns {arm_name: sorted list of (parpola_id,
    mahadevan_id) pair dicts}.
    """
    pair_rows = [r for r in rows if r.get("mahadevan_id")]

    def as_pairs(sel: list[dict]) -> list[dict]:
        out = [{"parpola_id": r["parpola_id"],
                "mahadevan_id": r["mahadevan_id"],
                "confidence": r["confidence"]}
               for r in sel]
        return sorted(out, key=lambda d: (d["parpola_id"],
                                          d["mahadevan_id"]))

    high = [r for r in pair_rows if r["confidence"] == "high"]
    high_medium = [r for r in pair_rows
                   if r["confidence"] in ("high", "medium")]
    return {
        ARM_PRIMARY: as_pairs(_unique_pairs(high)),
        ARM_SENSITIVITY_A: as_pairs(_unique_pairs(high_medium)),
        ARM_SENSITIVITY_B: as_pairs(pair_rows),
    }


# ── Profiles (spec section 4; within-compilation only) ───

def sign_profile(inscriptions, sign: str):
    """(profile, n_tokens, counts) of one sign inside one
    compilation, or (None, 0, (0, 0, 0)) if unattested."""
    counts = positional_counts(inscriptions, sign)
    profile = profile_from_counts(counts)
    return profile, sum(counts), counts


def profiles_from_context(ctx: CorpusContext, sign: str):
    """Same as sign_profile, over a precomputed context."""
    profile = ctx.profile(sign)
    return profile, ctx.token_count(sign)


def w1_distance(p, q) -> float:
    """Ordinal 1-Wasserstein over INITIAL < MEDIAL <
    TERMINAL with unit bin spacing (cumulative form)."""
    return abs(p[0] - q[0]) + abs((p[0] + p[1]) - (q[0] + q[1]))


# ── Spearman (spec section 5) ─────────────────────────────

def _average_ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(xs: list[float], ys: list[float]):
    """Spearman rho (average ranks; Pearson on ranks).

    Returns None if either vector is constant (rho is
    undefined there — spec section 5: a constant rate
    vector is not agreement evidence) or n < 3.
    """
    if len(xs) != len(ys) or len(xs) < 3:
        return None
    if len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    rx = _average_ranks(xs)
    ry = _average_ranks(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    if vx == 0 or vy == 0:
        return None
    return cov / (vx * vy) ** 0.5


def median(values: list[float]):
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0


def percentile_type7(values: list[float], pct: float):
    """Linear-interpolation (type-7) percentile."""
    if not values:
        return None
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    rank = (pct / 100.0) * (len(s) - 1)
    lo = int(rank)
    hi = min(lo + 1, len(s) - 1)
    frac = rank - lo
    return s[lo] * (1 - frac) + s[hi] * frac


# ── Pairing-shuffle null (spec section 5) ─────────────────

def pairing_shuffle_null(mayig_profiles: list, holdat_profiles: list,
                         observed_median_tv: float,
                         seed: int = NULL_SEED, b: int = NULL_B) -> dict:
    """Permute the Holdat-side profiles among the pairs;
    replicate statistic = median TV of the permuted
    pairing. p_null = (1 + #{median_b <= observed}) / (1 + B).
    """
    rng = random.Random(seed)
    null_medians: list[float] = []
    for _ in range(b):
        perm = list(holdat_profiles)
        rng.shuffle(perm)
        tvs = [tv_distance(p, q) for p, q in zip(mayig_profiles, perm)]
        null_medians.append(median(tvs))
    n_le = sum(1 for m in null_medians if m <= observed_median_tv)
    return {
        "b": b,
        "seed": seed,
        "p_null": (1 + n_le) / (1 + b),
        "n_null_median_le_observed": n_le,
        "null_median_of_medians": median(null_medians),
        "null_p05_of_medians": percentile_type7(null_medians, 5),
    }


# ── Arm evaluation (spec sections 4-5) ────────────────────

def evaluate_arm(pairs: list[dict], mayig_ctx: CorpusContext,
                 holdat_ctx: CorpusContext,
                 seed: int = NULL_SEED, b: int = NULL_B) -> dict:
    """Score one arm. Profiles come from the two contexts
    separately (mayig_ctx holds mayig inscriptions only;
    holdat_ctx holds Holdat inscriptions only)."""
    records = []
    for pair in pairs:
        p_prof, p_n = profiles_from_context(mayig_ctx, pair["parpola_id"])
        m_prof, m_n = profiles_from_context(holdat_ctx, pair["mahadevan_id"])
        judgeable = (p_prof is not None and m_prof is not None
                     and p_n >= FLOOR and m_n >= FLOOR)
        rec = {
            "parpola_id": pair["parpola_id"],
            "mahadevan_id": pair["mahadevan_id"],
            "confidence": pair["confidence"],
            "mayig_n": p_n,
            "holdat_n": m_n,
            "mayig_profile": ([round(x, 6) for x in p_prof]
                              if p_prof is not None else None),
            "holdat_profile": ([round(x, 6) for x in m_prof]
                               if m_prof is not None else None),
            "judgeable": judgeable,
            "tv": None,
            "w1": None,
        }
        if judgeable:
            rec["tv"] = round(tv_distance(p_prof, m_prof), 6)
            rec["w1"] = round(w1_distance(p_prof, m_prof), 6)
        records.append(rec)

    judged = [r for r in records if r["judgeable"]]
    stats: dict = {
        "n_pairs": len(records),
        "n_judgeable": len(judged),
        "n_below_floor": len(records) - len(judged),
        "median_tv": None,
        "median_w1": None,
        "spearman_initial": None,
        "spearman_medial": None,
        "spearman_terminal": None,
        "modal_agreement_share": None,
        "null": None,
    }
    if judged:
        stats["median_tv"] = round(median([r["tv"] for r in judged]), 6)
        stats["median_w1"] = round(median([r["w1"] for r in judged]), 6)
        stats["spearman_initial"] = _round_or_none(spearman(
            [r["mayig_profile"][0] for r in judged],
            [r["holdat_profile"][0] for r in judged]))
        stats["spearman_medial"] = _round_or_none(spearman(
            [r["mayig_profile"][1] for r in judged],
            [r["holdat_profile"][1] for r in judged]))
        stats["spearman_terminal"] = _round_or_none(spearman(
            [r["mayig_profile"][2] for r in judged],
            [r["holdat_profile"][2] for r in judged]))
        agree = sum(
            1 for r in judged
            if modal_class(tuple(r["mayig_profile"]))
            == modal_class(tuple(r["holdat_profile"])))
        stats["modal_agreement_share"] = round(agree / len(judged), 6)
        stats["null"] = pairing_shuffle_null(
            [tuple(r["mayig_profile"]) for r in judged],
            [tuple(r["holdat_profile"]) for r in judged],
            stats["median_tv"], seed=seed, b=b)
        # rounded copies of the null summary floats
        for k in ("p_null", "null_median_of_medians",
                  "null_p05_of_medians"):
            if stats["null"][k] is not None:
                stats["null"][k] = round(stats["null"][k], 6)
    return {"records": records, "stats": stats}


def _round_or_none(x):
    return round(x, 6) if x is not None else None


# ── Verdict rule (spec section 6) ─────────────────────────

def classify(stats: dict) -> dict:
    """The frozen section-6 rule, applied in order, over
    one arm's statistics. Returns the pattern for that
    arm; the phase verdict is the PRIMARY arm's pattern.
    """
    n = stats["n_judgeable"]
    if n < STARVED_MIN:
        return {"verdict": NULL, "substate": STARVED,
                "reason": f"judgeable {n} < {STARVED_MIN}"}
    med = stats["median_tv"]
    rho_i = stats["spearman_initial"]
    rho_t = stats["spearman_terminal"]
    p_null = (stats["null"] or {}).get("p_null")
    if (med is not None and med <= TV_PASS_MAX
            and rho_i is not None and rho_i >= RHO_MIN
            and rho_t is not None and rho_t >= RHO_MIN
            and p_null is not None and p_null <= P_NULL_MAX):
        return {"verdict": PASS, "substate": "AGREEMENT",
                "reason": "all section-6.2 legs met"}
    if (med is not None and med >= TV_FAIL_MIN
            and p_null is not None and p_null > P_NULL_MAX):
        return {"verdict": FAIL, "substate": "DISAGREEMENT",
                "reason": "section-6.3 falsifier pattern met"}
    return {"verdict": NULL, "substate": INCONCLUSIVE,
            "reason": "neither the PASS nor the FAIL pattern met"}
