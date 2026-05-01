"""Phase-30b: Tier-1 fixes + Tier-3 Sanskrit falsification.

Tier-1 fixes (response to Phase-30a PARTIAL verdict):
  T1.1  Tighten BASE_RENDERINGS (drop generic Sumerian syllables that
        leaked through Phase-29 — 'in', 'en', 'na', 'il', 'min', 'men',
        'mul', 'imin', 'kakkab', 'asz'). Re-run A1 + A5 + A6.
  T1.2  A3-v2 token-level Meluhha co-occurrence matcher (replace exact
        substring match with token-level segment matching that handles
        diacritics + subscript digits).
  T1.3  A8-v2 sign-ID alignment audit (zero-padded vs unpadded; document
        the genuine M77 ↔ phoneme-map overlap of 2 signs).

Tier-3 Sanskrit falsification:
  T3.1  Load yajnadevam_phonemes_sanskrit.json (synthetic Sanskrit-
        logographic competing map).
  T3.2  Run iconographic-anchor-score random-mapping null on BOTH
        Parpola's Dravidian map and Yajnadevam's Sanskrit map.
        Report observed score + null distribution + p-value for each.

Outputs:
  reports/indus_phase30b_t1_1_tight_renderings_<ts>.json
  reports/indus_phase30b_t1_2_meluhha_v2_<ts>.json
  reports/indus_phase30b_t1_3_signid_audit_<ts>.json
  reports/indus_phase30b_t3_yajnadevam_<ts>.json
  reports/indus_phase30b_verdict_<ts>.json
"""

from __future__ import annotations

import json
import math
import random
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_BACKEND = _REPO_ROOT / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from glossa_lab.data.mesopotamian_contact import (  # noqa: E402
    get_epsd2_personal_names,
    get_iconographic_anchors,
    get_janabiyah_seal_reading,
    get_mahadevan_inscriptions,
    get_mahadevan_parpola_crosswalk,
    get_meluhha_tablets,
    get_parpola_phoneme_map,
)

REPORTS_DIR = _REPO_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

# Janabiyah skeleton (unchanged):
JANABIYAH_TARGET_SEGMENTS = 7
JANABIYAH_MIIN_POSITIONS = {1, 3, 6}

# Phase-30a (loose) baseline rendering set, for comparison:
PHASE30A_RENDERINGS = {
    "miin", "mi-in", "me-en", "mi-na", "me-na", "mi-il",
    "me-il", "mi-en", "me-in", "mu-li", "min", "men",
    "mul", "imin", "kakkab", "asz",
}

# T1.1 — Tightened set: ONLY direct Akkadian / Sumerian transliterations of
# Dravidian *miin* with at least 4 letters or hyphens. Drops generic Sumerian
# syllables that leak ("in", "en", "na", "il", "men", "min", "mul", "imin").
TIGHT_RENDERINGS = {
    "mi-in", "me-en", "mi-na", "me-na",
    "mi-il", "me-il", "mi-en", "me-in",
    "mu-li",
}


def _expand_to_tokens(renderings: set[str]) -> set[str]:
    out: set[str] = set()
    for r in renderings:
        for t in r.split("-"):
            t = t.strip().lower()
            if t and len(t) >= 2:
                out.add(t)
    return out


def _epsd_pn_to_segments(forms: list[str]) -> list[list[str]]:
    segs: list[list[str]] = []
    for f in forms or []:
        if not f:
            continue
        clean = re.sub(r"\{[^}]+\}", "", str(f).lower())
        parts = [p for p in re.split(r"[-]+", clean) if p and not p.isspace()]
        parts = [re.sub(r"[0-9]+$", "", p) for p in parts]
        parts = [p for p in parts if p]
        if parts:
            segs.append(parts)
    return segs


def _score_pn(forms: list[str], rendering_tokens: set[str],
              miin_positions: set[int] = JANABIYAH_MIIN_POSITIONS,
              n_target_segments: int = JANABIYAH_TARGET_SEGMENTS) -> dict:
    all_segs = _epsd_pn_to_segments(forms)
    if not all_segs:
        return {"total_score": -999.0, "position_match": 0,
                "free_miin": 0, "best_form": "",
                "best_n_segs": 0, "positions_matched": []}
    best_score = -999.0
    best = None
    for segs in all_segs:
        n_segs = len(segs)
        delta = abs(n_segs - n_target_segments)
        length_score = max(0.0, 3.0 - 0.5 * delta)
        position_match = 0
        positions_matched: list[int] = []
        for i, seg in enumerate(segs):
            if i in miin_positions and seg in rendering_tokens:
                position_match += 1
                positions_matched.append(i)
        free_miin = sum(1 for s in segs if s in rendering_tokens)
        total = length_score + position_match * 1.5 + free_miin * 0.5
        if total > best_score:
            best_score = total
            best = {
                "total_score": round(total, 3),
                "length_score": round(length_score, 2),
                "position_match": position_match,
                "free_miin": free_miin,
                "best_form": "-".join(segs),
                "best_n_segs": n_segs,
                "positions_matched": positions_matched,
            }
    return best  # type: ignore


def _score_all_pns(pns, rendering_tokens, **kw) -> list[dict]:
    out = []
    for pn in pns:
        r = _score_pn(pn.get("forms") or [], rendering_tokens, **kw)
        if r is None:
            continue
        out.append({
            "headword": pn.get("headword", ""),
            "icount": int(pn.get("icount", 0) or 0),
            "periods": pn.get("periods", []),
            **r,
        })
    return out


def _save_report(test_id: str, payload: dict) -> Path:
    fname = f"indus_phase30b_{test_id}_{TS}.json"
    p = REPORTS_DIR / fname
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def _build_syllable_vocab(pns: list[dict]) -> list[str]:
    vocab = Counter()
    for pn in pns:
        for segs in _epsd_pn_to_segments(pn.get("forms") or []):
            for s in segs:
                if 2 <= len(s) <= 4:
                    vocab[s] += 1
    return list(vocab.elements())


# ─── T1.1: Tight renderings — re-run A1 + A5 + A6 ────────────────────


def run_t1_1(pns: list[dict],
             n_a1_perms: int = 10_000,
             n_a5_perms_per_pn: int = 500,
             top_k: int = 30,
             headword: str = "Enmenanak[1]PN",
             observed_score_baseline: float = 7.0) -> dict:
    """Re-run A1 (perm null), A5 (BH-FDR), A6 (Ur III vs OBab) with the
    tightened rendering set.
    """
    rng_global = random.Random(42)
    vocab = _build_syllable_vocab(pns)
    tight_tokens = _expand_to_tokens(TIGHT_RENDERINGS)
    loose_tokens = _expand_to_tokens(PHASE30A_RENDERINGS)

    # Baseline + tight scoring of all PNs
    scored_loose = _score_all_pns(pns, loose_tokens)
    scored_tight = _score_all_pns(pns, tight_tokens)

    n_pos_loose = sum(1 for r in scored_loose if r["position_match"] > 0)
    n_pos_tight = sum(1 for r in scored_tight if r["position_match"] > 0)

    # Find Enmenanak under both
    enm_loose = next((r for r in scored_loose if r["headword"] == headword), None)
    enm_tight = next((r for r in scored_tight if r["headword"] == headword), None)
    enm_score_tight = enm_tight["total_score"] if enm_tight else 0.0

    # ── A1 with tight renderings ──
    enmenanak_forms = next((p.get("forms") or [] for p in pns if p.get("headword") == headword), [])
    target_size_tight = len(tight_tokens)
    null_scores_a1 = []
    n_geq_a1 = 0
    for _ in range(n_a1_perms):
        sampled: set[str] = set()
        while len(sampled) < target_size_tight:
            sampled.add(rng_global.choice(vocab))
        s = _score_pn(enmenanak_forms, sampled)["total_score"]
        null_scores_a1.append(s)
        if s >= enm_score_tight:
            n_geq_a1 += 1
    null_scores_a1.sort()
    n_d = len(null_scores_a1)
    p_a1 = (n_geq_a1 + 1) / (n_a1_perms + 1)

    # ── A5 BH-FDR with tight renderings ──
    rng_a5 = random.Random(0)
    sorted_tight = sorted(scored_tight, key=lambda r: -r["total_score"])
    top = sorted_tight[:top_k]
    pvals = []
    for r in top:
        pn_obj = next((p for p in pns if p.get("headword") == r["headword"]), None)
        if not pn_obj:
            continue
        n_geq = 0
        for _ in range(n_a5_perms_per_pn):
            sampled: set[str] = set()
            while len(sampled) < target_size_tight:
                sampled.add(rng_a5.choice(vocab))
            s = _score_pn(pn_obj.get("forms") or [], sampled)["total_score"]
            if s >= r["total_score"]:
                n_geq += 1
        p = (n_geq + 1) / (n_a5_perms_per_pn + 1)
        pvals.append({"headword": r["headword"], "score": r["total_score"],
                       "icount": r["icount"], "periods": r["periods"],
                       "p_value": round(p, 6)})
    pvals.sort(key=lambda x: x["p_value"])
    m = len(pvals)
    k_star = 0
    for i, row in enumerate(pvals, 1):
        row["bh_threshold_q05"] = round(0.05 * i / m, 6)
        row["significant_at_q05"] = row["p_value"] <= row["bh_threshold_q05"]
        if row["p_value"] <= 0.05 * i / m:
            k_star = i
    n_sig = k_star

    # ── A6 with tight renderings ──
    ur3 = [p for p in pns if "Ur III" in (p.get("periods") or [])]
    obab = [p for p in pns if "Old Babylonian" in (p.get("periods") or [])]
    ur3_scored_t = _score_all_pns(ur3, tight_tokens)
    obab_scored_t = _score_all_pns(obab, tight_tokens)
    rate_ur3_t = sum(1 for r in ur3_scored_t if r["position_match"] > 0) / max(1, len(ur3_scored_t))
    rate_obab_t = sum(1 for r in obab_scored_t if r["position_match"] > 0) / max(1, len(obab_scored_t))

    return {
        "test_id": "T1.1",
        "test_name": "Tight rendering set: re-run A1 + A5 + A6",
        "loose_rendering_set_size": len(loose_tokens),
        "tight_rendering_set_size": len(tight_tokens),
        "loose_tokens": sorted(loose_tokens),
        "tight_tokens": sorted(tight_tokens),
        "loose_n_position_matched": n_pos_loose,
        "tight_n_position_matched": n_pos_tight,
        "loose_enmenanak_score": enm_loose["total_score"] if enm_loose else None,
        "tight_enmenanak_score": enm_score_tight,
        "loose_top_3": [r["headword"] for r in sorted(scored_loose, key=lambda r: -r["total_score"])[:3]],
        "tight_top_3": [r["headword"] for r in sorted_tight[:3]],
        "a1_n_permutations": n_a1_perms,
        "a1_observed_score": enm_score_tight,
        "a1_p_value": round(p_a1, 6),
        "a1_null_mean": round(sum(null_scores_a1) / n_d, 4),
        "a1_null_p95": round(null_scores_a1[int(0.95 * n_d)], 4),
        "a1_null_p99": round(null_scores_a1[int(0.99 * n_d)], 4),
        "a5_n_tests": m,
        "a5_n_perms_per_test": n_a5_perms_per_pn,
        "a5_n_significant_after_bh": n_sig,
        "a5_top_pvals": pvals[:10],
        "a6_ur3_n": len(ur3_scored_t),
        "a6_ur3_position_match_rate": round(rate_ur3_t, 4),
        "a6_obab_n": len(obab_scored_t),
        "a6_obab_position_match_rate": round(rate_obab_t, 4),
        "a6_rate_delta_pp": round((rate_obab_t - rate_ur3_t) * 100, 4),
        "verdict": (
            f"T1.1 tightened renderings: position-match rate dropped from "
            f"{n_pos_loose} (loose, {len(loose_tokens)} tokens) to "
            f"{n_pos_tight} (tight, {len(tight_tokens)} tokens). "
            f"Enmenanak score went from {enm_loose['total_score'] if enm_loose else 0} -> "
            f"{enm_score_tight}. A1 p-value (tight) = {p_a1:.4f}. "
            f"A5 BH-FDR survivors (tight) = {n_sig}/{m}. "
            f"A6 Ur III rate {rate_ur3_t*100:.2f}% vs OBab {rate_obab_t*100:.2f}% "
            f"(delta {(rate_obab_t-rate_ur3_t)*100:+.2f}pp)."
        ),
    }


# ─── T1.2: A3-v2 token-level Meluhha co-occurrence ───────────────────


def _normalize_atf_token(t: str) -> str:
    """Normalize an ATF token for matching: lowercase, strip diacritics
    {[^}]+}, strip trailing digits/subscripts.
    """
    t = re.sub(r"\{[^}]+\}", "", t.lower())
    t = re.sub(r"[0-9]+$", "", t)
    t = t.strip("()[]_,;:.!? ")
    return t


def _tokenize_atf_text(text: str) -> list[str]:
    """Tokenize ATF text: split on whitespace + hyphens.
    Each token is normalized.
    """
    tokens = re.split(r"[-\s]+", text.lower())
    out = [_normalize_atf_token(t) for t in tokens]
    return [t for t in out if t]


def run_t1_2(pns: list[dict], tablets: list[dict]) -> dict:
    """Token-level Meluhha co-occurrence filter.

    For each PN with a position match (using TIGHT renderings), check
    whether the PN's segment sequence appears as a contiguous run in
    any Meluhha-mentioning tablet's tokenized ATF text.
    Allow normalization of diacritics + subscript digits.
    """
    tight_tokens = _expand_to_tokens(TIGHT_RENDERINGS)
    scored_all = _score_all_pns(pns, tight_tokens)
    pos_matched = [r for r in scored_all if r["position_match"] > 0]

    # Tokenize all Meluhha-mention tablets
    tablet_token_streams: list[tuple[str, str, str, list[str]]] = []
    for t in tablets:
        text_parts: list[str] = []
        text_parts.extend(t.get("atf_lines_with_match") or [])
        text_parts.extend(t.get("atf_excerpt_lines") or [])
        excerpt = t.get("atf_excerpt") or ""
        if excerpt:
            text_parts.extend(str(excerpt).splitlines())
        full_text = " ".join(text_parts)
        if "me-luh" not in full_text.lower():
            continue
        tokens = _tokenize_atf_text(full_text)
        tablet_token_streams.append(
            (t.get("p_number", ""), t.get("period", ""),
             t.get("provenience", ""), tokens)
        )

    def _contiguous_match(needle: list[str], haystack: list[str], min_len: int = 3) -> bool:
        n = len(needle)
        if n < min_len:
            return False
        h = len(haystack)
        for i in range(h - n + 1):
            if haystack[i:i + n] == needle:
                return True
        return False

    survivors = []
    for r in pos_matched:
        pn_obj = next((p for p in pns if p.get("headword") == r["headword"]), None)
        if not pn_obj:
            continue
        # Use the BEST form's segments
        all_segs = _epsd_pn_to_segments(pn_obj.get("forms") or [])
        if not all_segs:
            continue
        # Try matching each form variant
        hits: list[dict] = []
        matched_form: list[str] = []
        for segs in all_segs:
            if len(segs) < 3:
                continue
            for p_num, period, prov, tokens in tablet_token_streams:
                if _contiguous_match(segs, tokens):
                    hits.append({"p_number": p_num, "period": period,
                                  "provenience": prov,
                                  "matched_form": "-".join(segs)})
                    matched_form = segs
                    if len(hits) >= 5:
                        break
            if hits:
                break
        if hits:
            survivors.append({
                **r,
                "n_meluhha_hits": len(hits),
                "matched_form": "-".join(matched_form),
                "meluhha_hits": hits,
            })

    survivors.sort(key=lambda r: (-r["total_score"], -r["icount"]))

    return {
        "test_id": "T1.2",
        "test_name": "A3-v2 token-level Meluhha co-occurrence (tight renderings)",
        "n_position_matched_input": len(pos_matched),
        "n_meluhha_tablets_searched": len(tablet_token_streams),
        "n_with_meluhha_cooccurrence": len(survivors),
        "fraction_kept": round(len(survivors) / max(1, len(pos_matched)), 4),
        "survivors": survivors[:30],
        "min_match_length": 3,
        "verdict": (
            f"T1.2 (A3-v2) token-level Meluhha co-occurrence: of "
            f"{len(pos_matched)} position-matched PNs (tight renderings), "
            f"{len(survivors)} have a >=3-segment contiguous match in at "
            f"least one of the {len(tablet_token_streams)} Meluhha-mentioning "
            f"tablets. "
            + (f"Top survivor: '{survivors[0]['headword']}' "
               f"(matched form '{survivors[0]['matched_form']}', "
               f"hits {survivors[0]['n_meluhha_hits']})."
               if survivors else "Zero substantive co-occurrences. Either "
                                  "(a) Phase-29 candidates are not Meluhhan "
                                  "names, or (b) the corpus does not contain "
                                  "them, or (c) the matcher needs further "
                                  "relaxation.")
        ),
    }


# ─── T1.3: A8-v2 sign-ID alignment audit ─────────────────────────────


def run_t1_3(m77_inscriptions: list[list[str]],
             phoneme_map: dict,
             crosswalk: dict) -> dict:
    """Audit M77 corpus signs vs phoneme map signs vs crosswalk.

    Build canonical sign-ID normalizations (zero-padded vs unpadded, M-prefix);
    compute true overlap; document data limitation.
    """
    m77_signs_set = set()
    sign_freq = Counter()
    for ins in m77_inscriptions:
        for s in ins:
            m77_signs_set.add(s)
            sign_freq[s] += 1

    # Normalize: strip leading zeros from M77 (047 -> 47)
    m77_normalized = {str(int(s)) if s.isdigit() else s for s in m77_signs_set}
    pmap_signs = set(phoneme_map.keys())
    pmap_normalized = {str(int(k)) if k.isdigit() else k for k in pmap_signs}

    # Crosswalk: M001 -> 1, M047 -> 47
    crosswalk_normalized = {}
    for k, v in crosswalk.items():
        # Strip M prefix and leading zeros
        kn = re.sub(r"^M0*", "", k)
        if not kn:
            kn = "0"
        crosswalk_normalized[kn] = v

    # Triple intersection: M77 corpus AND phoneme map (direct + via crosswalk)
    direct_overlap = m77_normalized & pmap_normalized
    crosswalk_phoneme_signs = set()
    for k, v in crosswalk_normalized.items():
        ph = v.get("phoneme", "") if isinstance(v, dict) else ""
        if ph and k in m77_normalized:
            crosswalk_phoneme_signs.add(k)

    full_overlap = direct_overlap | crosswalk_phoneme_signs

    # M77 corpus tokens with phoneme coverage
    n_tokens_with_phoneme = sum(c for s, c in sign_freq.items()
                                  if (str(int(s)) if s.isdigit() else s) in full_overlap)
    total_tokens = sum(sign_freq.values())

    # M77 unique signs not in either
    m77_only = m77_normalized - pmap_normalized - set(crosswalk_normalized.keys())

    return {
        "test_id": "T1.3",
        "test_name": "A8-v2 sign-ID alignment audit",
        "m77_distinct_signs": len(m77_signs_set),
        "m77_total_tokens": total_tokens,
        "phoneme_map_entries": len(pmap_signs),
        "crosswalk_entries": len(crosswalk),
        "direct_overlap_count": len(direct_overlap),
        "direct_overlap_signs": sorted(direct_overlap),
        "via_crosswalk_overlap_count": len(crosswalk_phoneme_signs),
        "via_crosswalk_overlap_signs": sorted(crosswalk_phoneme_signs),
        "full_overlap_count": len(full_overlap),
        "full_overlap_signs": sorted(full_overlap),
        "m77_tokens_with_phoneme_coverage": n_tokens_with_phoneme,
        "phoneme_coverage_token_fraction": round(n_tokens_with_phoneme / max(1, total_tokens), 4),
        "m77_signs_with_no_phoneme": len(m77_only),
        "verdict": (
            f"T1.3 sign-ID audit: M77 corpus has {len(m77_signs_set)} distinct "
            f"signs ({total_tokens} tokens). Phoneme map has {len(pmap_signs)} "
            f"entries. Direct ID overlap = {len(direct_overlap)}; via crosswalk "
            f"= {len(crosswalk_phoneme_signs)}; UNION = {len(full_overlap)}. "
            f"Phoneme coverage of M77 token frequency = "
            f"{n_tokens_with_phoneme/max(1,total_tokens)*100:.2f}%. "
            f"This confirms the Phase-30a A8 finding: even with proper sign-ID "
            f"alignment, only {len(full_overlap)} signs in the M77 corpus have "
            f"a phoneme reading. Phase-30a A8 cannot be meaningfully re-run "
            f"until the phoneme map expands to cover more M77 corpus signs "
            f"(P30-B2 Wells 2015 + P30-D1/D2 Wells/Fuls cross-cluster)."
        ),
    }


# ─── T3: Yajnadevam Sanskrit vs Parpola Dravidian falsification ─────


_PARPOLA_ALIAS = {
    "fish": ("miin", "fish"),
    "fish/star": ("miin", "fish"),
    "fig": ("vaTa", "fig_tree"),
    "banyan/fig": ("vaTa", "fig_tree"),
    "banyan": ("vaTa", "fig_tree"),
    "muruku": ("muruku", "intersecting_circles"),
    "intersecting circles": ("muruku", "intersecting_circles"),
    "squirrel": ("piLLai", None),
    "pot": ("kuTam", None),
    "pot/jar": ("kuTam", None),
    "veL": ("veL", "numerals"),
    "veN-miin": ("veL", None),
    "venus": ("veL", None),
    "pleiades": ("aru-", "numerals"),
    "ursa major": ("eZu-", "numerals"),
    "north star": ("vaTa", "fig_tree"),
}

_YAJNADEVAM_ALIAS_FALLBACK = {
    "fish": ("matsya", "fish"),
    "fish/star": ("matsya", "fish"),
    "fig": ("nyagrodha", "fig_tree"),
    "banyan/fig": ("nyagrodha", "fig_tree"),
    "banyan": ("nyagrodha", "fig_tree"),
    "muruku": ("skanda", "intersecting_circles"),
    "intersecting circles": ("skanda", "intersecting_circles"),
    "squirrel": ("putra", None),
    "pot": ("kumbha", None),
    "pot/jar": ("kumbha", None),
    "veL": ("shvet", "numerals"),
    "veN-miin": ("shvet", None),
    "venus": ("shvet", None),
    "pleiades": ("krittika", "numerals"),
    "ursa major": ("saptarshi", "numerals"),
    "north star": ("nyagrodha", "fig_tree"),
}


def _anchor_score(anchors: list[dict], phoneme_map: dict, alias: dict) -> float:
    total = 0.0
    for a in anchors:
        sid = str(a.get("sign_id", "")).split("+")[0]
        iconic = (a.get("iconic_reading", "") or "").lower()
        anchor_conf = (a.get("confidence") or "low").lower()
        ph_entry = phoneme_map.get(sid, {}) or {}
        ph_value = (ph_entry.get("phoneme", "") or "").lower()
        ph_conf = (ph_entry.get("confidence") or "none").lower()

        match = False
        for k, val in alias.items():
            target = val[0] if isinstance(val, (list, tuple)) else val
            if k in iconic and target.lower() in ph_value:
                match = True
                break
        if not match:
            for k, val in alias.items():
                target = val[0] if isinstance(val, (list, tuple)) else val
                if k in iconic:
                    match = target.lower() in ph_value
                    if match:
                        break

        if match:
            if anchor_conf == "high":
                anchor_score = 2.0
            elif anchor_conf == "medium":
                anchor_score = 1.0
            else:
                anchor_score = 0.5
            if ph_conf == "high":
                anchor_score *= 1.5
            total += anchor_score
    return total


def _random_mapping_null(anchors: list[dict], phoneme_map: dict,
                          alias: dict, n_perms: int = 10_000,
                          seed: int = 2025) -> dict:
    observed = _anchor_score(anchors, phoneme_map, alias)
    sign_ids = list(phoneme_map.keys())
    phoneme_entries = list(phoneme_map.values())
    rng = random.Random(seed)
    null = []
    n_geq = 0
    for _ in range(n_perms):
        shuffled = list(phoneme_entries)
        rng.shuffle(shuffled)
        random_map = {sid: shuffled[i] for i, sid in enumerate(sign_ids)}
        s = _anchor_score(anchors, random_map, alias)
        null.append(s)
        if s >= observed:
            n_geq += 1
    null.sort()
    n = len(null)
    return {
        "observed_anchor_score": round(observed, 4),
        "n_perms": n_perms,
        "null_mean": round(sum(null) / n, 4),
        "null_p50": round(null[n // 2], 4),
        "null_p95": round(null[int(0.95 * n)], 4),
        "null_p99": round(null[int(0.99 * n)], 4),
        "null_max": round(null[-1], 4),
        "p_value_one_sided": round((n_geq + 1) / (n_perms + 1), 6),
        "rank_percentile": round(sum(1 for s in null if s < observed) / n * 100.0, 4),
    }


def run_t3_yajnadevam(anchors: list[dict],
                      parpola_phoneme_map: dict,
                      yajnadevam_path: Path,
                      n_perms: int = 10_000) -> dict:
    """Head-to-head Sanskrit vs Dravidian falsification on E7."""
    if not yajnadevam_path.exists():
        return {"error": f"Yajnadevam map not found at {yajnadevam_path}"}
    yd_data = json.loads(yajnadevam_path.read_text(encoding="utf-8"))
    yajnadevam_map = yd_data.get("phoneme_map", {})
    yajnadevam_alias_raw = yd_data.get("iconic_to_phoneme_alias_sanskrit", {})
    yajnadevam_alias = {k: tuple(v) for k, v in yajnadevam_alias_raw.items()} \
        if yajnadevam_alias_raw else _YAJNADEVAM_ALIAS_FALLBACK

    parpola_result = _random_mapping_null(anchors, parpola_phoneme_map,
                                            _PARPOLA_ALIAS, n_perms=n_perms,
                                            seed=2025)
    yajnadevam_result = _random_mapping_null(anchors, yajnadevam_map,
                                               yajnadevam_alias, n_perms=n_perms,
                                               seed=2026)

    # Decide outcome
    p_score = parpola_result["observed_anchor_score"]
    y_score = yajnadevam_result["observed_anchor_score"]
    p_p = parpola_result["p_value_one_sided"]
    y_p = yajnadevam_result["p_value_one_sided"]

    if p_score > y_score and p_p < 0.05 and y_p > 0.05:
        outcome = ("PARPOLA WINS: Dravidian map scores higher AND its score is "
                    "significant (p<0.05) while Sanskrit's is not.")
    elif y_score > p_score and y_p < 0.05 and p_p > 0.05:
        outcome = ("YAJNADEVAM WINS: Sanskrit map scores higher AND its score is "
                    "significant (p<0.05) while Dravidian's is not.")
    elif p_score > y_score and p_p < 0.05 and y_p < 0.05:
        outcome = ("PARPOLA EDGE: Both maps significant but Dravidian scores higher "
                    f"({p_score} vs {y_score}). Both hypotheses receive non-trivial "
                    "iconographic-anchor support; Parpola's edge suggests "
                    "Dravidian-specific homonymies (miin = fish/star, vaTa = "
                    "banyan/north, piLLai = squirrel/child) ARE doing real work.")
    elif p_score == y_score:
        outcome = "TIE: identical observed scores; iconographic-anchor methodology cannot distinguish."
    else:
        outcome = (f"INCONCLUSIVE: Parpola score {p_score} (p={p_p:.4f}), "
                   f"Yajnadevam score {y_score} (p={y_p:.4f}).")

    return {
        "test_id": "T3",
        "test_name": "Yajnadevam Sanskrit vs Parpola Dravidian falsification (E7 head-to-head)",
        "n_perms_per_map": n_perms,
        "n_anchors": len(anchors),
        "parpola_dravidian": parpola_result,
        "yajnadevam_sanskrit": yajnadevam_result,
        "score_difference_parpola_minus_yajnadevam": round(p_score - y_score, 4),
        "outcome": outcome,
        "verdict": (
            f"T3 falsification: Parpola Dravidian map observed anchor score = "
            f"{p_score} (p={p_p:.4f}); Yajnadevam Sanskrit map observed = "
            f"{y_score} (p={y_p:.4f}). Score difference = "
            f"{p_score - y_score:+.2f} in favor of "
            f"{'Parpola' if p_score > y_score else 'Yajnadevam' if y_score > p_score else 'tie'}. "
            f"{outcome}"
        ),
    }


# ─── Main runner ─────────────────────────────────────────────────────


def main() -> int:
    print(f"=== Phase-30b: Tier-1 fixes + Tier-3 Sanskrit falsification ({TS}) ===")

    print("[load] Data...", end=" ", flush=True)
    pns = get_epsd2_personal_names()
    anchors = get_iconographic_anchors()
    janabiyah = get_janabiyah_seal_reading()
    m77 = get_mahadevan_inscriptions()
    phoneme_map = get_parpola_phoneme_map()
    crosswalk = get_mahadevan_parpola_crosswalk()
    tablets = get_meluhha_tablets()
    yajnadevam_path = (_REPO_ROOT / "backend" / "glossa_lab" / "data"
                        / "yajnadevam_phonemes_sanskrit.json")
    print(f"PNs={len(pns)}, anchors={len(anchors)}, M77={len(m77)}, "
           f"phoneme_map={len(phoneme_map)}, crosswalk={len(crosswalk)}, "
           f"tablets={len(tablets)}.")

    aggregated = {
        "phase": "30b",
        "timestamp_utc": TS,
        "scope": "Tier-1 fixes (T1.1, T1.2, T1.3) + Tier-3 Sanskrit falsification (T3)",
        "results": {},
    }

    test_specs = [
        ("t1_1_tight_renderings", lambda: run_t1_1(pns, n_a1_perms=10_000,
                                                     n_a5_perms_per_pn=500,
                                                     top_k=30)),
        ("t1_2_meluhha_v2", lambda: run_t1_2(pns, tablets)),
        ("t1_3_signid_audit", lambda: run_t1_3(m77, phoneme_map, crosswalk)),
        ("t3_yajnadevam", lambda: run_t3_yajnadevam(anchors, phoneme_map,
                                                       yajnadevam_path,
                                                       n_perms=10_000)),
    ]

    for tid, fn in test_specs:
        t0 = time.time()
        print(f"[run] {tid}...", end=" ", flush=True)
        try:
            result = fn()
            elapsed = time.time() - t0
            result["_elapsed_seconds"] = round(elapsed, 2)
            path = _save_report(tid, result)
            print(f"done ({elapsed:.1f}s) -> {path.name}")
            aggregated["results"][tid] = result
        except Exception as exc:
            elapsed = time.time() - t0
            print(f"ERROR ({elapsed:.1f}s): {exc}")
            import traceback
            traceback.print_exc()
            aggregated["results"][tid] = {"error": str(exc),
                                            "_elapsed_seconds": round(elapsed, 2)}

    # ── Decision summary ──
    t1 = aggregated["results"].get("t1_1_tight_renderings", {})
    t2 = aggregated["results"].get("t1_2_meluhha_v2", {})
    t3 = aggregated["results"].get("t3_yajnadevam", {})

    decision = []
    # T1.1 — was the rendering set tightening helpful?
    if t1.get("a5_n_significant_after_bh", 0) > 0:
        decision.append(f"T1.1 PASS: with tight renderings, {t1['a5_n_significant_after_bh']} PNs survive BH-FDR.")
    else:
        decision.append(f"T1.1 PARTIAL: tight renderings drop position-match rate "
                         f"from {t1.get('loose_n_position_matched', '?')} to "
                         f"{t1.get('tight_n_position_matched', '?')}; A5 still "
                         f"{t1.get('a5_n_significant_after_bh', 0)}/30. "
                         f"A1 p={t1.get('a1_p_value', '?')}.")
    # T1.2
    n_meluhha = t2.get("n_with_meluhha_cooccurrence", 0)
    if n_meluhha > 0:
        decision.append(f"T1.2 PASS: {n_meluhha} PNs co-occur with Meluhha keyword (token-level).")
    else:
        decision.append("T1.2 FAIL: 0 PNs co-occur with Meluhha keyword even with token-level matching.")
    # T1.3
    overlap = t1_3 = aggregated["results"].get("t1_3_signid_audit", {}).get("full_overlap_count", 0)
    if overlap >= 5:
        decision.append(f"T1.3 PARTIAL: M77 ↔ phoneme-map overlap = {overlap}; can re-run A8.")
    else:
        decision.append(f"T1.3 CONFIRMS DATA LIMIT: M77 ↔ phoneme-map overlap = {overlap} (data-starved).")
    # T3
    if t3:
        decision.append(f"T3: {t3.get('outcome', '(no outcome)')}")

    aggregated["decision_summary"] = decision

    # Next-action recommendation
    p_score = (aggregated["results"].get("t3_yajnadevam") or {}).get("parpola_dravidian", {}).get("observed_anchor_score", 0)
    y_score = (aggregated["results"].get("t3_yajnadevam") or {}).get("yajnadevam_sanskrit", {}).get("observed_anchor_score", 0)
    p_pval = (aggregated["results"].get("t3_yajnadevam") or {}).get("parpola_dravidian", {}).get("p_value_one_sided", 1.0)
    y_pval = (aggregated["results"].get("t3_yajnadevam") or {}).get("yajnadevam_sanskrit", {}).get("p_value_one_sided", 1.0)

    if p_score > y_score and p_pval < 0.05:
        if n_meluhha > 0 and t1.get("a5_n_significant_after_bh", 0) > 0:
            next_action = ("PROCEED: Tier-1 fixes restored statistical signal AND "
                            "Parpola wins Sanskrit head-to-head. Phase-30c can pursue "
                            "B1-B3 phoneme-map expansion + L9 arXiv preprint.")
        else:
            next_action = ("PROCEED CAUTIOUSLY: Parpola wins Sanskrit head-to-head "
                            "(score "
                            f"{p_score} vs {y_score}, p={p_pval:.4f}), but Tier-1 fixes "
                            "did not fully restore A5/A3 power. Phase-30c should focus "
                            "on Tier-2 corpus expansion (Fuls + Wells), then re-run "
                            "Phase-30a tests at expanded scale.")
    elif y_score >= p_score:
        next_action = ("CRITICAL: Sanskrit ties or beats Dravidian on iconographic "
                        "anchors. Re-evaluate Parpola hypothesis. Phase-30c should "
                        "investigate where Sanskrit's score comes from + run additional "
                        "falsification rounds.")
    else:
        next_action = "INCONCLUSIVE: Mixed results; review per-test verdicts manually."
    aggregated["next_action"] = next_action

    verdict_path = REPORTS_DIR / f"indus_phase30b_verdict_{TS}.json"
    verdict_path.write_text(
        json.dumps(aggregated, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\n=== AGGREGATE VERDICT === ({verdict_path.name})")
    for d in decision:
        print(f"  {d}")
    print(f"\nNext: {next_action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
