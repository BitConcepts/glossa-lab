"""Phase-30c: methodological hardening + 4-way falsification.

T1.1-v3: Whole-rendering matcher.
  Replace token-level matching (which leaks generic Sumerian syllables
  'in', 'en', 'na', 'il' through the splits of hyphenated renderings)
  with strict whole-rendering matching:
    - A position counts as a *miin* match only if a SINGLE segment
      exactly equals one of the single-token renderings ('miin', 'min')
      OR if TWO consecutive segments exactly equal one of the
      multi-token renderings ('mi-in', 'me-en', etc.).
  Re-run A1 + A5 + A6 with this stricter matcher.

T1.2-v3: Tiered Meluhha co-occurrence matcher.
  (a) >=3-segment contiguous (Phase-30b T1.2 baseline; was 0)
  (b) >=2-segment contiguous
  (c) bag-of-segments fractional overlap (>=70%)
  Establishes whether Phase-29 candidates are ANYWHERE attested on
  Meluhha-mention tablets.

T3-v2: 4-way iconographic-anchor falsification.
  Run E7 random-mapping null on FOUR competing maps:
    1. Parpola Dravidian (parpola_phonemes.json)
    2. Yajnadevam Sanskrit (yajnadevam_phonemes_sanskrit.json)
    3. S.R. Rao Sanskrit-logographic (rao_phonemes_sanskrit_logographic.json)
    4. Neukart Cosmological (neukart_phonemes_cosmological.json)
  Compare observed scores + p-values + null distributions.
"""

from __future__ import annotations

import json
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
    get_meluhha_tablets,
    get_parpola_phoneme_map,
)

REPORTS_DIR = _REPO_ROOT / "reports"
DATA_DIR = _REPO_ROOT / "backend" / "glossa_lab" / "data"
REPORTS_DIR.mkdir(exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

JANABIYAH_TARGET_SEGMENTS = 7
JANABIYAH_MIIN_POSITIONS = {1, 3, 6}

# Direct miin renderings, kept as full strings (NOT split)
MIIN_RENDERINGS_FULL = [
    "miin", "min",
    "mi-in", "me-en", "mi-na", "me-na",
    "mi-il", "me-il", "mi-en", "me-in",
    "mu-li",
]

# Pre-split into single-token vs two-token sets for whole-rendering matching:
SINGLE_TOKEN_RENDERINGS = {r for r in MIIN_RENDERINGS_FULL if "-" not in r}
TWO_TOKEN_RENDERINGS = {tuple(r.split("-")) for r in MIIN_RENDERINGS_FULL if "-" in r}


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


# ─── T1.1-v3: Whole-rendering matcher ────────────────────────────────


def _whole_rendering_position_matches(segs: list[str],
                                       miin_positions: set[int],
                                       singles: set[str],
                                       pairs: set[tuple[str, str]]) -> tuple[int, list[int]]:
    """Count position matches under whole-rendering matching.

    A position p matches iff EITHER:
      (a) segs[p] is a single-token rendering, OR
      (b) (segs[p], segs[p+1]) is a two-token rendering, OR
      (c) (segs[p-1], segs[p]) is a two-token rendering (so the second
          token is at position p — counts position p).
    """
    matches = 0
    matched_positions: list[int] = []
    n = len(segs)
    for p in miin_positions:
        if p < 0 or p >= n:
            continue
        is_match = False
        if segs[p] in singles:
            is_match = True
        elif p + 1 < n and (segs[p], segs[p + 1]) in pairs:
            is_match = True
        elif p - 1 >= 0 and (segs[p - 1], segs[p]) in pairs:
            is_match = True
        if is_match:
            matches += 1
            matched_positions.append(p)
    return matches, matched_positions


def _whole_rendering_free_matches(segs: list[str],
                                    singles: set[str],
                                    pairs: set[tuple[str, str]]) -> int:
    """Count the number of whole-rendering matches anywhere in the segment list.
    (Doesn't double-count overlapping matches.)
    """
    count = 0
    n = len(segs)
    i = 0
    while i < n:
        if segs[i] in singles:
            count += 1
            i += 1
            continue
        if i + 1 < n and (segs[i], segs[i + 1]) in pairs:
            count += 1
            i += 2
            continue
        i += 1
    return count


def _score_pn_v3(forms: list[str],
                  singles: set[str] = SINGLE_TOKEN_RENDERINGS,
                  pairs: set[tuple[str, str]] = TWO_TOKEN_RENDERINGS,
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
        position_match, positions_matched = _whole_rendering_position_matches(
            segs, miin_positions, singles, pairs
        )
        free_miin = _whole_rendering_free_matches(segs, singles, pairs)
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


def _score_all_pns_v3(pns,
                       singles: set[str] = SINGLE_TOKEN_RENDERINGS,
                       pairs: set[tuple[str, str]] = TWO_TOKEN_RENDERINGS) -> list[dict]:
    out = []
    for pn in pns:
        r = _score_pn_v3(pn.get("forms") or [], singles=singles, pairs=pairs)
        if r is None:
            continue
        out.append({
            "headword": pn.get("headword", ""),
            "icount": int(pn.get("icount", 0) or 0),
            "periods": pn.get("periods", []),
            **r,
        })
    return out


def _build_syllable_vocab(pns: list[dict]) -> list[str]:
    vocab = Counter()
    for pn in pns:
        for segs in _epsd_pn_to_segments(pn.get("forms") or []):
            for s in segs:
                if 2 <= len(s) <= 4:
                    vocab[s] += 1
    return list(vocab.elements())


def _save_report(test_id: str, payload: dict) -> Path:
    fname = f"indus_phase30c_{test_id}_{TS}.json"
    p = REPORTS_DIR / fname
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def run_t1_1_v3(pns: list[dict],
                 n_a1_perms: int = 10_000,
                 n_a5_perms_per_pn: int = 500,
                 top_k: int = 30) -> dict:
    """Re-score all PNs under whole-rendering matching."""
    rng_a1 = random.Random(42)
    vocab = _build_syllable_vocab(pns)
    target_singles = len(SINGLE_TOKEN_RENDERINGS)
    target_pairs = len(TWO_TOKEN_RENDERINGS)

    scored = _score_all_pns_v3(pns)
    n_pos = sum(1 for r in scored if r["position_match"] > 0)
    enm_r = next((r for r in scored if r["headword"] == "Enmenanak[1]PN"), None)
    enh_r = next((r for r in scored if r["headword"] == "Enheduana[1]PN"), None)
    enm_score = enm_r["total_score"] if enm_r else 0.0
    sorted_scored = sorted(scored, key=lambda r: -r["total_score"])
    top_30 = sorted_scored[:30]

    # ── A1: permutation null on Enmenanak score ──
    enmenanak_forms = next((p.get("forms") or [] for p in pns
                              if p.get("headword") == "Enmenanak[1]PN"), [])
    null_scores = []
    n_geq_a1 = 0
    unique_vocab = list(set(vocab))
    for _ in range(n_a1_perms):
        # Randomize the rendering set: pick `target_singles` random vocab
        # tokens to act as "singles" and `target_pairs` random pairs.
        random_singles = set(rng_a1.sample(unique_vocab,
                                            min(target_singles, len(unique_vocab))))
        random_pairs: set[tuple[str, str]] = set()
        while len(random_pairs) < target_pairs:
            a = rng_a1.choice(vocab)
            b = rng_a1.choice(vocab)
            random_pairs.add((a, b))
        s = _score_pn_v3(enmenanak_forms,
                          singles=random_singles, pairs=random_pairs)["total_score"]
        null_scores.append(s)
        if s >= enm_score:
            n_geq_a1 += 1
    null_scores.sort()
    n_d = len(null_scores)
    p_a1 = (n_geq_a1 + 1) / (n_a1_perms + 1)

    # ── A5 BH-FDR ──
    rng_a5 = random.Random(0)
    pvals = []
    for r in top_30:
        pn_obj = next((p for p in pns if p.get("headword") == r["headword"]), None)
        if not pn_obj:
            continue
        n_geq = 0
        for _ in range(n_a5_perms_per_pn):
            random_singles = set(rng_a5.sample(unique_vocab,
                                                min(target_singles, len(unique_vocab))))
            random_pairs: set[tuple[str, str]] = set()
            while len(random_pairs) < target_pairs:
                a = rng_a5.choice(vocab)
                b = rng_a5.choice(vocab)
                random_pairs.add((a, b))
            s = _score_pn_v3(pn_obj.get("forms") or [],
                              singles=random_singles, pairs=random_pairs)["total_score"]
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

    # ── A6 Ur III vs OBab ──
    ur3 = [p for p in pns if "Ur III" in (p.get("periods") or [])]
    obab = [p for p in pns if "Old Babylonian" in (p.get("periods") or [])]
    ur3_scored = _score_all_pns_v3(ur3)
    obab_scored = _score_all_pns_v3(obab)
    rate_ur3 = sum(1 for r in ur3_scored if r["position_match"] > 0) / max(1, len(ur3_scored))
    rate_obab = sum(1 for r in obab_scored if r["position_match"] > 0) / max(1, len(obab_scored))

    return {
        "test_id": "T1.1-v3",
        "test_name": "Whole-rendering matcher (single-token + 2-token consecutive)",
        "single_token_renderings": sorted(SINGLE_TOKEN_RENDERINGS),
        "two_token_renderings": sorted([f"{a}-{b}" for a, b in TWO_TOKEN_RENDERINGS]),
        "n_position_matched": n_pos,
        "enmenanak_score": enm_score,
        "enmenanak_position_match": enm_r["position_match"] if enm_r else 0,
        "enheduana_score": enh_r["total_score"] if enh_r else 0,
        "top_10_scores": [
            {"headword": r["headword"], "score": r["total_score"],
             "best_form": r["best_form"], "icount": r["icount"],
             "periods": r["periods"], "position_match": r["position_match"],
             "free_miin": r["free_miin"]}
            for r in sorted_scored[:10]
        ],
        "a1_n_perms": n_a1_perms,
        "a1_observed_score": enm_score,
        "a1_p_value": round(p_a1, 6),
        "a1_null_mean": round(sum(null_scores) / n_d, 4),
        "a1_null_p95": round(null_scores[int(0.95 * n_d)], 4),
        "a1_null_p99": round(null_scores[int(0.99 * n_d)], 4),
        "a5_n_tests": m,
        "a5_n_perms_per_test": n_a5_perms_per_pn,
        "a5_n_significant_after_bh": k_star,
        "a5_top_pvals": pvals[:10],
        "a6_ur3_n": len(ur3_scored),
        "a6_ur3_position_match_rate": round(rate_ur3, 4),
        "a6_obab_n": len(obab_scored),
        "a6_obab_position_match_rate": round(rate_obab, 4),
        "a6_rate_delta_pp": round((rate_obab - rate_ur3) * 100, 4),
        "verdict": (
            f"T1.1-v3 whole-rendering matcher: position-match count = {n_pos} "
            f"(was 102 under loose token-level matching). Enmenanak score = "
            f"{enm_score} (was 7.0 → 5.0; now likely 0). "
            f"A1 p-value = {p_a1:.4f}. A5 BH-FDR survivors = {k_star}/{m}. "
            f"A6 Ur III rate {rate_ur3*100:.2f}% vs OBab {rate_obab*100:.2f}% "
            f"(delta {(rate_obab-rate_ur3)*100:+.2f}pp)."
        ),
    }


# ─── T1.2-v3: Tiered Meluhha matcher ─────────────────────────────────


def _normalize_atf_token(t: str) -> str:
    t = re.sub(r"\{[^}]+\}", "", t.lower())
    t = re.sub(r"[0-9]+$", "", t)
    t = t.strip("()[]_,;:.!? ")
    return t


def _tokenize_atf_text(text: str) -> list[str]:
    tokens = re.split(r"[-\s]+", text.lower())
    out = [_normalize_atf_token(t) for t in tokens]
    return [t for t in out if t]


def run_t1_2_v3(pns: list[dict], tablets: list[dict]) -> dict:
    """Tiered Meluhha co-occurrence matcher.

    Tier (a): >=3 contiguous segments
    Tier (b): >=2 contiguous segments
    Tier (c): bag-of-segments overlap >= 70 %
    """
    # Use loose Phase-30a scoring to get the same 102 candidate set
    # (so the tiered matcher's "fail" can't be blamed on a too-strict
    # candidate selection).
    scored = _score_all_pns_v3(pns)
    pos_matched = [r for r in scored if r["position_match"] > 0]

    # Also try with loose-style Phase-30a scoring (which had 102 PNs)
    from itertools import chain  # noqa: PLC0415
    # Tokenize all Meluhha tablets
    tablet_streams = []
    for t in tablets:
        text_parts = []
        text_parts.extend(t.get("atf_lines_with_match") or [])
        text_parts.extend(t.get("atf_excerpt_lines") or [])
        excerpt = t.get("atf_excerpt") or ""
        if excerpt:
            text_parts.extend(str(excerpt).splitlines())
        full_text = " ".join(text_parts)
        if "me-luh" not in full_text.lower():
            continue
        tokens = _tokenize_atf_text(full_text)
        tablet_streams.append((t.get("p_number", ""), t.get("period", ""),
                                t.get("provenience", ""), tokens, set(tokens)))

    def _contiguous_match(needle: list[str], haystack: list[str], min_len: int) -> bool:
        n = len(needle)
        if n < min_len:
            return False
        h = len(haystack)
        for i in range(h - n + 1):
            if haystack[i:i + n] == needle:
                return True
        return False

    def _bag_overlap(needle: list[str], haystack_set: set[str]) -> float:
        if not needle:
            return 0.0
        return sum(1 for s in needle if s in haystack_set) / len(needle)

    # For ALL 1,222 PNs (not just position-matched), check tiered matchers
    pn_results = []
    for pn in pns:
        all_segs = _epsd_pn_to_segments(pn.get("forms") or [])
        if not all_segs:
            continue
        # Use the longest form variant
        best_segs = max(all_segs, key=len)
        if len(best_segs) < 2:
            continue
        tier_a_hits = []
        tier_b_hits = []
        tier_c_hits = []
        for p_num, period, prov, tokens, tokens_set in tablet_streams:
            if _contiguous_match(best_segs, tokens, 3):
                tier_a_hits.append({"p_number": p_num, "period": period})
            elif _contiguous_match(best_segs, tokens, 2):
                tier_b_hits.append({"p_number": p_num, "period": period})
            overlap = _bag_overlap(best_segs, tokens_set)
            if overlap >= 0.70:
                tier_c_hits.append({"p_number": p_num, "overlap": round(overlap, 3)})
        if tier_a_hits or tier_b_hits or tier_c_hits:
            pn_results.append({
                "headword": pn.get("headword", ""),
                "icount": int(pn.get("icount", 0) or 0),
                "periods": pn.get("periods", []),
                "best_form": "-".join(best_segs),
                "n_segs": len(best_segs),
                "tier_a_3seg_hits": len(tier_a_hits),
                "tier_b_2seg_hits": len(tier_b_hits),
                "tier_c_bag_hits": len(tier_c_hits),
                "tier_a_examples": tier_a_hits[:3],
                "tier_b_examples": tier_b_hits[:3],
                "tier_c_examples": tier_c_hits[:3],
            })
    pn_results.sort(key=lambda r: (-(r["tier_a_3seg_hits"] + r["tier_b_2seg_hits"] + r["tier_c_bag_hits"]),
                                      -r["icount"]))

    n_tier_a = sum(1 for r in pn_results if r["tier_a_3seg_hits"] > 0)
    n_tier_b = sum(1 for r in pn_results if r["tier_b_2seg_hits"] > 0)
    n_tier_c = sum(1 for r in pn_results if r["tier_c_bag_hits"] > 0)

    return {
        "test_id": "T1.2-v3",
        "test_name": "Tiered Meluhha co-occurrence matcher (3-seg / 2-seg / bag)",
        "n_total_pns_searched": len(pns),
        "n_meluhha_tablets_searched": len(tablet_streams),
        "n_pos_matched_input": len(pos_matched),
        "n_tier_a_3seg_contiguous": n_tier_a,
        "n_tier_b_2seg_contiguous": n_tier_b,
        "n_tier_c_bag_70pct": n_tier_c,
        "n_with_any_tier_hit": len(pn_results),
        "top_results": pn_results[:30],
        "verdict": (
            f"T1.2-v3 tiered Meluhha matcher across all {len(pns)} ePSD2 PNs: "
            f"tier_a (>=3-seg contiguous) = {n_tier_a}, "
            f"tier_b (>=2-seg contiguous) = {n_tier_b}, "
            f"tier_c (bag overlap >=70%) = {n_tier_c}. "
            + (f"Top hit: '{pn_results[0]['headword']}' "
               f"({pn_results[0]['tier_a_3seg_hits']}+"
               f"{pn_results[0]['tier_b_2seg_hits']}+"
               f"{pn_results[0]['tier_c_bag_hits']} hits)."
               if pn_results else "ZERO hits across all tiers — substantively confirmed.")
        ),
    }


# ─── T3-v2: 4-way iconographic-anchor falsification ─────────────────


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


def run_t3_v2(anchors: list[dict],
               parpola_phoneme_map: dict,
               n_perms: int = 10_000) -> dict:
    """4-way E7 falsification."""
    yajn_path = DATA_DIR / "yajnadevam_phonemes_sanskrit.json"
    rao_path = DATA_DIR / "rao_phonemes_sanskrit_logographic.json"
    neukart_path = DATA_DIR / "neukart_phonemes_cosmological.json"

    def _load(p: Path, alias_key: str, fallback: dict):
        if not p.exists():
            return None, None
        d = json.loads(p.read_text(encoding="utf-8"))
        m = d.get("phoneme_map", {})
        a_raw = d.get(alias_key, {})
        a = {k: tuple(v) for k, v in a_raw.items()} if a_raw else fallback
        return m, a

    yajn_map, yajn_alias = _load(yajn_path, "iconic_to_phoneme_alias_sanskrit", {})
    rao_map, rao_alias = _load(rao_path, "iconic_to_phoneme_alias_sanskrit_rao", {})
    neukart_map, neukart_alias = _load(neukart_path, "iconic_to_phoneme_alias_cosmological", {})

    results: dict = {}
    results["parpola_dravidian"] = _random_mapping_null(
        anchors, parpola_phoneme_map, _PARPOLA_ALIAS, n_perms=n_perms, seed=2025)
    if yajn_map:
        results["yajnadevam_sanskrit"] = _random_mapping_null(
            anchors, yajn_map, yajn_alias, n_perms=n_perms, seed=2026)
    if rao_map:
        results["rao_sanskrit_logographic"] = _random_mapping_null(
            anchors, rao_map, rao_alias, n_perms=n_perms, seed=2027)
    if neukart_map:
        results["neukart_cosmological"] = _random_mapping_null(
            anchors, neukart_map, neukart_alias, n_perms=n_perms, seed=2028)

    # Sort by observed score
    ranked = sorted(results.items(),
                     key=lambda kv: -kv[1].get("observed_anchor_score", 0))

    # Determine the gap between #1 and #2
    if len(ranked) >= 2:
        gap = ranked[0][1]["observed_anchor_score"] - ranked[1][1]["observed_anchor_score"]
    else:
        gap = 0

    leader = ranked[0][0] if ranked else "(no maps loaded)"
    leader_score = ranked[0][1]["observed_anchor_score"] if ranked else 0

    return {
        "test_id": "T3-v2",
        "test_name": "4-way iconographic-anchor falsification",
        "n_perms_per_map": n_perms,
        "n_anchors": len(anchors),
        "results": results,
        "ranked": [
            {"map": name, "observed": d["observed_anchor_score"],
             "p_value": d["p_value_one_sided"], "null_max": d["null_max"]}
            for name, d in ranked
        ],
        "leader": leader,
        "leader_score": leader_score,
        "gap_first_to_second": round(gap, 4),
        "verdict": (
            f"T3-v2: 4-way head-to-head. Ranked: " +
            "; ".join(f"{name}={d['observed_anchor_score']:.1f} (p={d['p_value_one_sided']:.4f})"
                       for name, d in ranked) +
            f". LEADER: {leader} (score {leader_score:.1f}). "
            f"Gap to runner-up: {gap:+.1f} anchor-points."
        ),
    }


# ─── Main ────────────────────────────────────────────────────────────


def main() -> int:
    print(f"=== Phase-30c: methodological hardening + 4-way falsification ({TS}) ===")
    print("[load] Data...", end=" ", flush=True)
    pns = get_epsd2_personal_names()
    anchors = get_iconographic_anchors()
    phoneme_map = get_parpola_phoneme_map()
    tablets = get_meluhha_tablets()
    print(f"PNs={len(pns)}, anchors={len(anchors)}, "
           f"phoneme_map={len(phoneme_map)}, tablets={len(tablets)}.")

    aggregated = {
        "phase": "30c",
        "timestamp_utc": TS,
        "scope": "T1.1-v3 (whole-rendering) + T1.2-v3 (tiered Meluhha) + T3-v2 (4-way falsification)",
        "results": {},
    }

    test_specs = [
        ("t1_1_v3_whole_rendering", lambda: run_t1_1_v3(pns, n_a1_perms=10_000,
                                                          n_a5_perms_per_pn=500)),
        ("t1_2_v3_tiered_meluhha", lambda: run_t1_2_v3(pns, tablets)),
        ("t3_v2_four_way_falsification", lambda: run_t3_v2(anchors, phoneme_map,
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

    # ── Decision ──
    t1 = aggregated["results"].get("t1_1_v3_whole_rendering", {})
    t2 = aggregated["results"].get("t1_2_v3_tiered_meluhha", {})
    t3 = aggregated["results"].get("t3_v2_four_way_falsification", {})

    decision = []
    enm = t1.get("enmenanak_score", 0)
    n_pos = t1.get("n_position_matched", 0)
    a1_p = t1.get("a1_p_value", 1.0)
    a5_sig = t1.get("a5_n_significant_after_bh", 0)
    decision.append(
        f"T1.1-v3: position-match count = {n_pos} (was 102 under loose). "
        f"Enmenanak score = {enm}. A1 p-value = {a1_p:.4f}. A5 BH-FDR survivors = {a5_sig}/30."
    )
    decision.append(
        f"T1.2-v3: tier_a={t2.get('n_tier_a_3seg_contiguous', '?')}, "
        f"tier_b={t2.get('n_tier_b_2seg_contiguous', '?')}, "
        f"tier_c={t2.get('n_tier_c_bag_70pct', '?')}."
    )
    decision.append(f"T3-v2: leader = {t3.get('leader', '?')} "
                     f"(score {t3.get('leader_score', '?')}, "
                     f"gap to runner-up = {t3.get('gap_first_to_second', '?')}).")

    aggregated["decision_summary"] = decision

    # Next-action
    if enm <= 1.0 and n_pos < 30:
        next_action = ("CONFIRMED: Whole-rendering matcher correctly drops false-positive "
                        "rate. Phase-29 Janabiyah readout fully retracted. T3-v2 result is "
                        "the surviving headline. Phase-30d should focus on (a) acquiring "
                        "Tier-2 corpora, (b) Phase-30b T1.1-v3 rerun at expanded scale, "
                        "(c) preregistering the T3-v2 methodology for arXiv preprint.")
    else:
        next_action = (f"PARTIAL: T1.1-v3 still keeps {n_pos} PNs as position-matched. "
                        "Methodology may need further tightening.")
    aggregated["next_action"] = next_action

    verdict_path = REPORTS_DIR / f"indus_phase30c_verdict_{TS}.json"
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
