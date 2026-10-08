"""Phase-118 (spec 017) — within-compilation validation
battery v2: pure machinery.

Ledger-sequence Phase-118 (2026-10-07). Implements the frozen
battery of specs/017-phase118-within-compilation-validation-
v2/spec.md — the W1-primary redesign of spec 016's battery,
which Phase-117's calibration rejected (STRICT94 LOO VALIDATED
2/94; W3 PASS 3/94; KUR113 gate passed vacuously). Every
instrument lives inside Holdat (Phase-116 R-NONE):

  W1 split-half positional cross-fit — PRIMARY; spec 016
     section 4.1 carried verbatim (frozen seed-117 partition,
     spec-011 T2a thresholds unretuned), imported unchanged
     from phase117_battery,
  W2 iconographic co-occurrence — remains DROPPED as a
     decision-bearing instrument (spec 016 section 4.2); its
     statistics are recorded descriptively in the W3 record,
  W3 distributional-neighborhood coherence REBUILT as
     cross-fit: junction model and phi derived on the
     opposite partition half from the observations scored
     (the spec-016 leave-one-out-minus-self reference is
     abolished); donor-permutation null (B = 999, frequency
     band) retained per direction as the discrimination leg;
     bands PASS_d: score_d >= phi_d and p_d <= 0.50, FAIL_d
     the exact mirror; per-direction junction floor 2,
  W4 site-stratum stability — spec 016 section 4.4 verbatim,
     narrowed to a FAIL-guard (its PASS has no positive
     effect in the section-8 rule),

plus the section-8 W1-primary decision rule. Judgeability is
a count property (spec section 2.1): J94 = STRICT94 signs
W1-scorable and W3-scorable (asserted 67); JKUR = KUR113
signs W3-scorable (asserted 29). No instrument reads any SA
artifact, any anchor's basis text, any ICIT artifact, or any
prior phase's verdict (governance H26). Deterministic:
counting, the frozen partition shuffle (seed 117, carried),
one seeded donor stream (seed 118, spec section 3).

Corpus contexts are built from inscription lists supplied by
the caller (phase118_run), so this module is testable on toy
corpora.
"""
from __future__ import annotations

import math
import random

from glossa_lab.phase113_battery import (
    FAIL, INDETERMINATE, PASS, CorpusContext, normalize_reading,
)
from glossa_lab.phase117_battery import (
    JunctionModel, _descriptives, _score, build_partition,
    junction_observations, percentile, phonemes_of, site_profiles,
    test_w1, test_w4,
)

__all__ = [
    "FAIL", "INDETERMINATE", "PASS", "DONOR_SEED",
    "W3X_JUNCTION_FLOOR", "build_partition", "decide",
    "donor_pool", "evaluate_anchor", "percentile", "phonemes_of",
    "site_profiles", "test_w1", "test_w3x", "test_w4",
    "w3x_scorable", "w3x_self_score",
]

DONOR_SEED = 118

# ── Frozen thresholds (spec 017 sections 4.3-5) ────────────────
W3X_JUNCTION_FLOOR = 2        # per direction, on the scoring half
W3X_DONOR_REPLICATES = 999
W3X_P_BAND = 0.50             # median-donor criterion, both legs
W3X_BAND_LO_DIV = 3           # donor band: ceil(n_H/3) .. 3*n_H


# ── W3 cross-fit (spec section 4.3) ───────────────────────────

def donor_pool(sign, holdat_counts, anchor_signs) -> list:
    """The frozen donor band for a sign: anchored signs t != s
    with n_H(t) in [ceil(n_H(s)/3), 3*n_H(s)] (total Holdat
    counts; spec section 4.3)."""
    n_h = holdat_counts.get(sign, 0)
    lo = math.ceil(n_h / W3X_BAND_LO_DIV)
    hi = W3X_BAND_LO_DIV * n_h
    return sorted(t for t in anchor_signs
                  if t != sign and lo <= holdat_counts.get(t, 0) <= hi)


def _junction_count(scoring_ins, sign, core_signs) -> int:
    obs = junction_observations(scoring_ins, sign, core_signs)
    return sum(obs[0].values()) + sum(obs[1].values())


def w3x_scorable(sign, ins_a, ins_b, core_signs, holdat_counts,
                 anchor_signs) -> bool:
    """Spec section 2.1: both directions at or above the
    per-direction junction floor, and a non-empty donor band.
    A count property — no score is computed."""
    if not donor_pool(sign, holdat_counts, anchor_signs):
        return False
    return (_junction_count(ins_a, sign, core_signs)
            >= W3X_JUNCTION_FLOOR
            and _junction_count(ins_b, sign, core_signs)
            >= W3X_JUNCTION_FLOOR)


def w3x_self_score(sign, model_ins, scoring_ins, core_signs,
                   phon: dict):
    """The sign's cross-fit junction score in one direction
    (model built on model_ins without the sign's pairs when
    the caller passes a leave-one-out core); None when below
    the per-direction junction floor. Used for phi (spec
    section 4.3)."""
    obs = junction_observations(scoring_ins, sign, core_signs)
    n_j = sum(obs[0].values()) + sum(obs[1].values())
    if n_j < W3X_JUNCTION_FLOOR:
        return None
    model = JunctionModel(model_ins, core_signs, phon)
    ini, fin = phon[sign]
    return _score(obs, phon, ini, fin, model)


def _w3x_direction(sign, model_ins, scoring_ins, core_signs,
                   phon: dict, pool: list, phi_d: float,
                   rng: random.Random) -> dict:
    """One cross-fit direction: model on model_ins, the tested
    sign's junction observations on scoring_ins. Guards
    consume no donor draws (spec section 3 stream order)."""
    obs = junction_observations(scoring_ins, sign, core_signs)
    n_j = sum(obs[0].values()) + sum(obs[1].values())
    out = {"n_junctions": n_j}
    if n_j < W3X_JUNCTION_FLOOR:
        out.update({"state": INDETERMINATE,
                    "reason": "junction_floor_half"})
        return out
    if not pool:
        out.update({"state": INDETERMINATE,
                    "reason": "donor_band_empty"})
        return out
    model = JunctionModel(model_ins, core_signs, phon)
    ini, fin = phon[sign]
    score = _score(obs, phon, ini, fin, model)
    out["score"] = round(score, 6)
    out["phi"] = round(phi_d, 6)
    out["donor_pool_size"] = len(pool)
    ge = 0
    for _ in range(W3X_DONOR_REPLICATES):
        d = pool[rng.randrange(len(pool))]
        d_ini, d_fin = phon[d]
        if _score(obs, phon, d_ini, d_fin, model) >= score:
            ge += 1
    p = (1 + ge) / (1 + W3X_DONOR_REPLICATES)
    out["p_value"] = round(p, 6)
    out["donor_ge"] = ge
    if score >= phi_d and p <= W3X_P_BAND:
        out["state"] = PASS
    elif score < phi_d and p >= W3X_P_BAND:
        out["state"] = FAIL
    else:
        out["state"] = INDETERMINATE
        out["reason"] = "legs_disagree"
    return out


def test_w3x(sign, reading_norm, ins_a, ins_b, core_signs,
             phon: dict, readings_norm, ctx_full: CorpusContext,
             holdat_counts, anchor_signs, phi: dict,
             rng: random.Random) -> dict:
    """The rebuilt W3 (spec section 4.3): two cross-fit
    directions combined by W1's rule — FAIL iff either
    direction FAILs, PASS iff both PASS, else INDETERMINATE.
    phi maps direction name -> phi_d. The W2 descriptives are
    recorded against the evaluation core (never gated)."""
    n_h = holdat_counts.get(sign, 0)
    out = {"n_holdat_tokens": n_h,
           "descriptive": _descriptives(sign, reading_norm,
                                        core_signs, readings_norm,
                                        ctx_full)}
    pool = donor_pool(sign, holdat_counts, anchor_signs)
    lo = math.ceil(n_h / W3X_BAND_LO_DIV)
    out["donor_band"] = [lo, W3X_BAND_LO_DIV * n_h]
    out["donor_pool_size"] = len(pool)
    d_ab = _w3x_direction(sign, ins_a, ins_b, core_signs, phon,
                          pool, phi["modelA_scoreB"], rng)
    d_ba = _w3x_direction(sign, ins_b, ins_a, core_signs, phon,
                          pool, phi["modelB_scoreA"], rng)
    states = (d_ab["state"], d_ba["state"])
    if FAIL in states:
        state = FAIL
    elif states == (PASS, PASS):
        state = PASS
    else:
        state = INDETERMINATE
    out["directions"] = {"modelA_scoreB": d_ab, "modelB_scoreA": d_ba}
    out["n_junctions"] = (d_ab["n_junctions"] + d_ba["n_junctions"])
    out["state"] = state
    return out


# ── Decision rule (spec section 8) ─────────────────────────────

def decide(w1: str, w3: str, w4: str) -> str:
    """VALIDATED iff W1 PASS and W3 PASS and no instrument
    FAILs (W4 is a FAIL-guard: its PASS has no positive
    effect); DEMOTE iff any instrument FAILs; else
    UNRESOLVED."""
    if FAIL in (w1, w3, w4):
        return "DEMOTE"
    if w1 == PASS and w3 == PASS:
        return "VALIDATED"
    return "UNRESOLVED"


def evaluate_anchor(sign, reading_raw, core_signs, phon: dict,
                    readings_norm, ins_a, ins_b,
                    inscriptions_sites, ctx_full: CorpusContext,
                    ctx_a: CorpusContext, ctx_b: CorpusContext,
                    profiles_by_site: dict, holdat_counts,
                    anchor_signs, phi: dict,
                    rng: random.Random) -> dict:
    """The full battery for one anchor against a fixed core
    (leave-one-out cores are the caller's responsibility)."""
    reading_norm = normalize_reading(reading_raw)
    w1 = test_w1(sign, ctx_a, ctx_b, core_signs)
    w3 = test_w3x(sign, reading_norm, ins_a, ins_b, core_signs,
                  phon, readings_norm, ctx_full, holdat_counts,
                  anchor_signs, phi, rng)
    w4 = test_w4(sign, profiles_by_site)
    return {"sign": sign, "reading": reading_raw,
            "reading_normalized": reading_norm,
            "w1": w1, "w3": w3, "w4": w4,
            "outcome": decide(w1["state"], w3["state"], w4["state"])}
