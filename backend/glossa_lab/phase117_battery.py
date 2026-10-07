"""Phase-117 (spec 016) — within-compilation validation battery:
pure machinery.

Ledger-sequence Phase-117 (2026-10-07). Implements the frozen
battery of specs/016-phase117-within-compilation-validation/
spec.md. Every instrument lives inside Holdat (Phase-116 R-NONE
forbids the cross-corpus gate on the Holdat/ICIT pair):

  W1 split-half positional cross-fit (spec-011 T2a thresholds
     carried over unretuned; derivation and scoring on disjoint
     halves of the frozen seed-117 partition),
  W2 iconographic co-occurrence — DROPPED as a decision-bearing
     instrument by spec section 4.2; its support/context counts
     and composed legality are recorded descriptively in the W3
     record and gate nothing,
  W3 distributional-neighborhood coherence (junction model over
     STRICT94 readings; absolute floor phi = 10th percentile of
     STRICT94 leave-one-out self-scores; seeded donor-permutation
     null, B = 999, frequency-band donors),
  W4 site-stratum stability with an attestation-asymmetric
     FAIL rule,

plus the section-8 decision rule. No instrument reads any SA
artifact, any anchor's basis text, any ICIT artifact, or any
prior phase's verdict (governance H26). Deterministic: counting,
one seeded partition shuffle, one seeded donor stream (both
seeded 117, spec section 3).

Corpus contexts are built from inscription lists supplied by
the caller (phase117_run), so this module is testable on toy
corpora.
"""
from __future__ import annotations

import math
import random
from collections import Counter, defaultdict

from glossa_lab.phase113_battery import (
    FAIL, INDETERMINATE, PASS, CorpusContext, _tokenize,
    canon_legal, modal_class, normalize_reading, tv_distance,
)

__all__ = [
    "FAIL", "INDETERMINATE", "PASS", "SEED",
    "build_partition", "decide", "evaluate_anchor",
    "half_centroids", "junction_model", "junction_observations",
    "percentile", "phonemes_of", "site_group", "test_w1",
    "test_w3", "test_w4", "w1_direction",
]

SEED = 117

# ── Frozen thresholds (spec 016 sections 3-5) ──────────────────
W1_MIN_HALF_TOKENS = 4
W1_TV_MAX = 0.35
W1_MODAL_SHARE_MIN = 0.45
W3_JUNCTION_FLOOR = 6
W3_DONOR_REPLICATES = 999
W3_P_PASS = 0.05
W3_P_FAIL = 0.50
W3_BAND_LO_DIV = 3          # donor band: ceil(n_H(s)/3) .. 3*n_H(s)
W4_MIN_STRATUM_TOKENS = 4
W4_FAIL_STRATUM_TOKENS = 8
W4_TV_MAX = 0.40

SITE_GROUPS = ("Mohenjo-daro", "Harappa")


# ── Phonemes (spec section 3 tokenizer) ────────────────────────

def phonemes_of(reading_norm: str):
    """(initial, final) phonemes of a normalized reading under
    the section-3 syllable-canon tokenizer; None when the
    reading does not tokenize."""
    toks = _tokenize(reading_norm)
    if not toks:
        return None
    return (toks[0][1], toks[-1][1])


# ── The frozen partition (spec section 3) ──────────────────────

def site_group(site: str) -> str:
    return site if site in SITE_GROUPS else "OTHER"


def _length_bin(n: int) -> int:
    return min(n, 6)        # bins {2, 3, 4, 5, 6+}


def build_partition(inscriptions_sites) -> list[str]:
    """Assign each inscription to half 'A' or 'B' by the frozen
    rule: strata are the 15 cells of (length bin x site group);
    within each stratum, inscriptions in loader order are
    shuffled with one random.Random(117) stream (strata in
    sorted (length bin, site group) key order) and dealt
    alternately A, B, A, B, ... beginning with A."""
    strata: dict[tuple[int, str], list[int]] = defaultdict(list)
    for idx, (toks, site) in enumerate(inscriptions_sites):
        strata[(_length_bin(len(toks)), site_group(site))].append(idx)
    rng = random.Random(SEED)
    half: list[str] = [""] * len(inscriptions_sites)
    for key in sorted(strata):
        members = list(strata[key])
        rng.shuffle(members)
        for j, idx in enumerate(members):
            half[idx] = "A" if j % 2 == 0 else "B"
    return half


# ── W1 — split-half positional cross-fit (spec section 4.1) ────

def half_centroids(half_ctx: CorpusContext, core_signs) -> dict:
    """Per modal class k: the token-weighted mean positional
    profile, on this half, of core signs whose modal class on
    this half is k (core signs with >= 1 token on the half)."""
    by_class: dict[str, list] = defaultdict(list)
    for s in core_signs:
        prof = half_ctx.profile(s)
        if prof is None:
            continue
        by_class[modal_class(prof)].append(
            (prof, half_ctx.token_count(s)))
    out = {}
    for k, members in by_class.items():
        wsum = sum(w for _, w in members) or 1
        out[k] = tuple(
            sum(p[i] * w for p, w in members) / wsum for i in range(3))
    return out


def w1_direction(sign, scoring_ctx: CorpusContext, centroids: dict) -> dict:
    """One cross-fit direction: model centroids from the model
    half, the tested sign scored on the scoring half."""
    n = scoring_ctx.token_count(sign)
    out = {"n_scoring_half": n}
    if n < W1_MIN_HALF_TOKENS:
        out.update({"state": INDETERMINATE,
                    "reason": "half_count_below_floor"})
        return out
    prof = scoring_ctx.profile(sign)
    m = modal_class(prof)
    share = max(prof)
    out.update({"modal_class": m, "modal_share": round(share, 6),
                "profile": [round(x, 6) for x in prof]})
    cent = centroids.get(m)
    if cent is None:
        out.update({"state": INDETERMINATE,
                    "reason": "centroid_undefined"})
        return out
    tv = tv_distance(prof, cent)
    out["tv_to_centroid"] = round(tv, 6)
    out["state"] = (PASS if tv <= W1_TV_MAX
                    and share >= W1_MODAL_SHARE_MIN else FAIL)
    return out


def test_w1(sign, ctx_a: CorpusContext, ctx_b: CorpusContext,
            core_signs) -> dict:
    cent_a = half_centroids(ctx_a, core_signs)
    cent_b = half_centroids(ctx_b, core_signs)
    d_ab = w1_direction(sign, ctx_b, cent_a)   # model A -> score B
    d_ba = w1_direction(sign, ctx_a, cent_b)   # model B -> score A
    states = (d_ab["state"], d_ba["state"])
    if FAIL in states:
        state = FAIL
    elif states == (PASS, PASS):
        state = PASS
    else:
        state = INDETERMINATE
    return {"state": state,
            "directions": {"modelA_scoreB": d_ab, "modelB_scoreA": d_ba}}


# ── W3 — junction coherence (spec section 4.3) ─────────────────

def junction_observations(inscriptions, sign, core_signs):
    """Ordered adjacent pairs (x, sign) and (sign, y) with the
    other sign in the core. Returns (as_right, as_left): Counters
    keyed by the NEIGHBOR's relevant phoneme-slot filler sign —
    as_right counts left neighbors, as_left counts right
    neighbors. n_j = total count."""
    as_right: Counter = Counter()
    as_left: Counter = Counter()
    for toks in inscriptions:
        for i, t in enumerate(toks):
            if t != sign:
                continue
            if i > 0 and toks[i - 1] in core_signs:
                as_right[toks[i - 1]] += 1
            if i + 1 < len(toks) and toks[i + 1] in core_signs:
                as_left[toks[i + 1]] += 1
    return as_right, as_left


class JunctionModel:
    """P(final phoneme of u, initial phoneme of v) over all
    ordered adjacent core-core pairs, add-0.5 smoothed over the
    attested-phoneme grid (spec section 4.3)."""

    def __init__(self, inscriptions, core_signs, phon: dict):
        self.counts: Counter = Counter()
        n = 0
        for toks in inscriptions:
            for u, v in zip(toks, toks[1:]):
                if u in core_signs and v in core_signs:
                    self.counts[(phon[u][1], phon[v][0])] += 1
                    n += 1
        self.n = n
        finals = {phon[s][1] for s in core_signs}
        initials = {phon[s][0] for s in core_signs}
        self.grid_size = len(finals) * len(initials)
        self.denom = n + 0.5 * self.grid_size

    def logp(self, f: str, i: str) -> float:
        return math.log((self.counts.get((f, i), 0) + 0.5) / self.denom)


def junction_model(inscriptions, core_signs, phon: dict) -> JunctionModel:
    return JunctionModel(inscriptions, core_signs, phon)


def _score(obs, phon, own_initial: str, own_final: str,
           model: JunctionModel) -> float:
    """Mean log P over the junction observations with the given
    (initial, final) phonemes in the tested sign's slots."""
    as_right, as_left = obs
    total = sum(as_right.values()) + sum(as_left.values())
    acc = 0.0
    for nb, c in as_right.items():       # pair (nb, s)
        acc += c * model.logp(phon[nb][1], own_initial)
    for nb, c in as_left.items():        # pair (s, nb)
        acc += c * model.logp(own_final, phon[nb][0])
    return acc / total


def percentile(values, q: float) -> float:
    """Linear-interpolation percentile (numpy 'linear' / type-7
    convention)."""
    xs = sorted(values)
    if not xs:
        raise ValueError("percentile of empty sequence")
    if len(xs) == 1:
        return xs[0]
    rank = (q / 100.0) * (len(xs) - 1)
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return xs[int(rank)]
    return xs[lo] + (xs[hi] - xs[lo]) * (rank - lo)


def w3_self_score(sign, inscriptions, core_signs, phon: dict):
    """The sign's junction score against the given core (the
    leave-one-out self-score when core excludes the sign);
    None when below the junction floor."""
    obs = junction_observations(inscriptions, sign, core_signs)
    n_j = sum(obs[0].values()) + sum(obs[1].values())
    if n_j < W3_JUNCTION_FLOOR:
        return None
    model = JunctionModel(inscriptions, core_signs, phon)
    ini, fin = phon[sign]
    return _score(obs, phon, ini, fin, model)


def _descriptives(sign, own_reading_norm, core_signs, readings_norm,
                  ctx: CorpusContext) -> dict:
    """W2's statistics, recorded descriptively (never gated):
    STRICT94-partner support and all-core context counts (spec
    011 T3 definitions) and the composed-legality fraction over
    those contexts under the anchor readings."""
    partners = {p for p, c in ctx.adjacency.get(sign, {}).items()
                if c >= 2 and p in core_signs}
    contexts = [ins for ins in ctx.inscriptions
                if len(ins) >= 2 and sign in ins
                and all(t == sign or t in core_signs for t in ins)]
    legal = 0
    for ins in contexts:
        composed = "".join(
            own_reading_norm if t == sign else readings_norm.get(t, "")
            for t in ins)
        if composed and canon_legal(composed):
            legal += 1
    return {"support": len(partners), "n_contexts": len(contexts),
            "legal_contexts": legal,
            "legal_fraction": (round(legal / len(contexts), 6)
                               if contexts else None)}


def test_w3(sign, reading_norm, inscriptions, core_signs, phon: dict,
            readings_norm, ctx: CorpusContext, holdat_counts,
            anchor_signs, phi: float, rng: random.Random) -> dict:
    n_h = holdat_counts.get(sign, 0)
    out = {"n_holdat_tokens": n_h,
           "descriptive": _descriptives(sign, reading_norm, core_signs,
                                        readings_norm, ctx)}
    obs = junction_observations(inscriptions, sign, core_signs)
    n_j = sum(obs[0].values()) + sum(obs[1].values())
    out["n_junctions"] = n_j
    if n_j < W3_JUNCTION_FLOOR:
        out.update({"state": INDETERMINATE, "reason": "junction_floor"})
        return out
    model = JunctionModel(inscriptions, core_signs, phon)
    ini, fin = phon[sign]
    score = _score(obs, phon, ini, fin, model)
    out["score"] = round(score, 6)
    out["phi"] = round(phi, 6)
    lo = math.ceil(n_h / W3_BAND_LO_DIV)
    hi = W3_BAND_LO_DIV * n_h
    pool = sorted(t for t in anchor_signs
                  if t != sign and lo <= holdat_counts.get(t, 0) <= hi)
    out["donor_pool_size"] = len(pool)
    out["donor_band"] = [lo, hi]
    if not pool:
        out.update({"state": INDETERMINATE,
                    "reason": "donor_band_empty"})
        return out
    ge = 0
    for _ in range(W3_DONOR_REPLICATES):
        d = pool[rng.randrange(len(pool))]
        d_ini, d_fin = phon[d]
        if _score(obs, phon, d_ini, d_fin, model) >= score:
            ge += 1
    p = (1 + ge) / (1 + W3_DONOR_REPLICATES)
    out["p_value"] = round(p, 6)
    out["donor_ge"] = ge
    if p <= W3_P_PASS and score >= phi:
        out["state"] = PASS
    elif p >= W3_P_FAIL and score < phi:
        out["state"] = FAIL
    else:
        out["state"] = INDETERMINATE
    return out


# ── W4 — stratum stability (spec section 4.4) ──────────────────

def site_profiles(inscriptions_sites) -> dict:
    """sign -> site -> positional profile, counts accumulated
    under the Phase-69 positional convention."""
    raw: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(lambda: [0, 0, 0]))
    for toks, site in inscriptions_sites:
        n = len(toks)
        for pos, tok in enumerate(toks):
            if pos == 0 and n > 1:
                raw[tok][site][0] += 1
            elif pos == n - 1 and n > 1:
                raw[tok][site][2] += 1
            else:
                raw[tok][site][1] += 1
    out = {}
    for sign, by_site in raw.items():
        out[sign] = {}
        for site, counts in by_site.items():
            total = sum(counts)
            out[sign][site] = {
                "n": total,
                "profile": tuple(c / total for c in counts)}
    return out


def test_w4(sign, profiles_by_site: dict) -> dict:
    by_site = profiles_by_site.get(sign, {})
    qualifying = {s: v for s, v in by_site.items()
                  if v["n"] >= W4_MIN_STRATUM_TOKENS}
    out = {"strata": {
        s: {"n": v["n"], "modal_class": modal_class(v["profile"]),
            "profile": [round(x, 6) for x in v["profile"]]}
        for s, v in sorted(qualifying.items())}}
    if len(qualifying) < 2:
        out.update({"state": INDETERMINATE,
                    "reason": "strata_below_two"})
        return out
    modals = {s: modal_class(v["profile"])
              for s, v in qualifying.items()}
    big = [s for s, v in qualifying.items()
           if v["n"] >= W4_FAIL_STRATUM_TOKENS]
    fail_pair = any(modals[a] != modals[b]
                    for i, a in enumerate(big) for b in big[i + 1:])
    if fail_pair:
        out["state"] = FAIL
        out["reason"] = "modal_disagreement_at_fail_attestation"
        return out
    sites = sorted(qualifying)
    tvs = [tv_distance(qualifying[a]["profile"],
                       qualifying[b]["profile"])
           for i, a in enumerate(sites) for b in sites[i + 1:]]
    out["max_pairwise_tv"] = round(max(tvs), 6) if tvs else 0.0
    if len(set(modals.values())) == 1 and all(
            t <= W4_TV_MAX for t in tvs):
        out["state"] = PASS
    else:
        out["state"] = INDETERMINATE
        out["reason"] = ("modal_disagreement_below_fail_bar"
                         if len(set(modals.values())) > 1
                         else "pairwise_tv_above_max")
    return out


# ── Decision rule (spec section 8) ─────────────────────────────

def decide(w1: str, w3: str, w4: str) -> str:
    """VALIDATED iff W3 PASS and (W1 or W4) PASS and no FAIL;
    DEMOTE iff any instrument FAILs; else UNRESOLVED."""
    if FAIL in (w1, w3, w4):
        return "DEMOTE"
    if w3 == PASS and (w1 == PASS or w4 == PASS):
        return "VALIDATED"
    return "UNRESOLVED"


def evaluate_anchor(sign, reading_raw, core_signs, phon: dict,
                    readings_norm, inscriptions, inscriptions_sites,
                    ctx_full: CorpusContext, ctx_a: CorpusContext,
                    ctx_b: CorpusContext, profiles_by_site: dict,
                    holdat_counts, anchor_signs, phi: float,
                    rng: random.Random) -> dict:
    """The full within-compilation battery for one anchor
    against a fixed core (leave-one-out cores are the caller's
    responsibility)."""
    reading_norm = normalize_reading(reading_raw)
    w1 = test_w1(sign, ctx_a, ctx_b, core_signs)
    w3 = test_w3(sign, reading_norm, inscriptions, core_signs, phon,
                 readings_norm, ctx_full, holdat_counts, anchor_signs,
                 phi, rng)
    w4 = test_w4(sign, profiles_by_site)
    return {"sign": sign, "reading": reading_raw,
            "reading_normalized": reading_norm,
            "w1": w1, "w3": w3, "w4": w4,
            "outcome": decide(w1["state"], w3["state"], w4["state"])}
