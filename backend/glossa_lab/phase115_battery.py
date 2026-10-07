"""Phase-115 (spec 014) — non-SA validation battery v2: T1 rebuilt.

Successor to the Phase-113 battery (spec 011), which calibration
rejected because T1 starved on the sparse Phase-107 ICIT layer.
Battery v2 changes exactly two things, both frozen in spec 014:

  1. T1 runs on the expanded v2 converted layer (spec 014
     section 2: key-normalized conversion, sentinel positions
     for placeholders/unmapped codes, partial inscriptions
     retained) — positional profiles are computed over the
     emitted sequences including sentinel positions.
  2. T1's attestation floor is scaled to each sign's measured
     opportunity-to-attest (spec 014 section 4): a sign is
     judged on the attestation it had a fair chance to produce,
     and never FAILs on fewer than 3 tokens.

T2, T3, the syllable canon, the profile conventions, and the
decision rule are spec 011 verbatim, reused from
phase113_battery (not reimplemented, so they cannot drift).
No SA artifact of any kind is read (governance H26).
"""
from __future__ import annotations

from glossa_lab.phase113_battery import (
    FAIL, NOT_ATTESTED, PASS, T1_TV_MAX, CoreGrammar, CorpusContext,
    decide, modal_class, normalize_reading, test_t2, test_t3,
    tv_distance,
)

__all__ = [
    "attestation_floor", "opportunity", "test_t1_v2",
    "evaluate_anchor_v2",
]

# ── Frozen constants (spec 014 section 4) ──────────────────────
OPPORTUNITY_BAND_LOW = 3.0    # O < 3        -> floor 1
OPPORTUNITY_BAND_HIGH = 9.0   # 3 <= O < 9   -> floor 2; O >= 9 -> floor 3
STABILITY_MIN_TOKENS = 3      # a T1 FAIL requires >= 3 ICIT tokens


def opportunity(n_holdat: int, ratio: float) -> float:
    """O(s) = r * n_H(s): the ICIT token count sign s would carry
    if the v2 layer sampled inscriptions in proportion to its
    Holdat presence. r = mapped v2-layer tokens / Holdat tokens."""
    return ratio * n_holdat


def attestation_floor(opp: float) -> int:
    """Frozen bands (spec 014 section 4): the floor never exceeds
    the Phase-113 absolute floor of 3 and never exceeds roughly a
    third of the sign's expected attestation."""
    if opp < OPPORTUNITY_BAND_LOW:
        return 1
    if opp < OPPORTUNITY_BAND_HIGH:
        return 2
    return 3


def test_t1_v2(sign, holdat: CorpusContext, icit: CorpusContext,
               ratio: float) -> dict:
    """T1 v2 — cross-corpus consistency with the opportunity-
    scaled attestation floor and the stability guard."""
    n_h = holdat.token_count(sign)
    n_i = icit.token_count(sign)
    opp = opportunity(n_h, ratio)
    floor = attestation_floor(opp)
    out = {"n_icit_tokens": n_i, "n_holdat_tokens": n_h,
           "opportunity": round(opp, 6), "floor": floor}
    prof_h = holdat.profile(sign)
    if prof_h is None:
        out.update({"state": NOT_ATTESTED,
                    "reason": "sign_absent_holdat"})
        return out
    if n_i < floor:
        out.update({"state": NOT_ATTESTED,
                    "reason": "below_opportunity_floor"})
        return out
    prof_i = icit.profile(sign)
    out["modal_holdat"] = modal_class(prof_h)
    out["modal_icit"] = modal_class(prof_i)
    out["tv"] = round(tv_distance(prof_h, prof_i), 6)
    agree = (out["modal_icit"] == out["modal_holdat"]
             and out["tv"] <= T1_TV_MAX)
    if agree:
        out["state"] = PASS
    elif n_i >= STABILITY_MIN_TOKENS:
        out["state"] = FAIL
    else:
        # Judged inconsistent on 1-2 tokens: below the stability
        # minimum, this is no verdict at all (spec 014 section 4).
        out.update({"state": NOT_ATTESTED,
                    "reason": "below_stability_floor"})
    return out


def evaluate_anchor_v2(sign, reading_raw, core: CoreGrammar,
                       readings_norm, holdat: CorpusContext,
                       icit: CorpusContext, is_valid_initial,
                       ratio: float) -> dict:
    """Full battery v2 for one anchor against a fixed core
    grammar: T1 v2 + spec-011 T2/T3 + the spec-011 section-5
    decision rule."""
    reading_norm = normalize_reading(reading_raw)
    t1 = test_t1_v2(sign, holdat, icit, ratio)
    t2 = test_t2(sign, reading_norm, core, holdat, is_valid_initial)
    t3 = test_t3(sign, reading_norm, core.core, readings_norm, holdat)
    states = {"t1": t1["state"], "t2": t2["state"], "t3": t3["state"]}
    return {"sign": sign, "reading": reading_raw,
            "reading_normalized": reading_norm,
            "t1": t1, "t2": t2, "t3": t3,
            "outcome": decide(states)}
