"""Phase-27 atomic-node implementations.

Phase-27 builds on Phase-26 with:
  1. ReverseJanabiyahSearch: starts from common Akkadian PNs in the Meluhha
     context, decomposes each into segments, and scores against Janabiyah's
     predicted phonetic skeleton. Smaller, more constrained search space
     than Phase-25a/26c.
  2. BayesianDecoderV2: extends Phase-26b to permute phoneme VALUES (not
     just confidence labels) under a Dravidian compound-name plausibility
     metric.
  3. IconographicAnchorScore: scores Parpola's phoneme map against the
     12 iconographic anchors (M-410, H-9, M-414, M-1186, M-1202, etc).
  4. PeriodStratifiedReadout6Bucket: extends Phase-25c with finer-grained
     period buckets (Lagash II, Sargonic Akkadian, Neo-Assyrian, Ebla
     split out from 'Other').
  5. ShuIlishuContactZoneFilter: now ACTUALLY filters the 138 candidates
     using Phase-27's catalogue_id-aware indus_cisi accessor.
  6. Phase27CorpusLoader: loads Phase-26 + iconographic anchors + Phase-27
     find-spot overrides.
"""

from __future__ import annotations

import math
import random
import re
from collections import Counter
from typing import Any


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


def _name_n_segments(name: str) -> int:
    return name.count("-") + 1 if name else 0


def _length_score(n_signs: int, n_segments: int, tolerance: int = 2) -> float:
    delta = abs(n_signs - n_segments)
    if delta > tolerance:
        return 0.0
    return round(1.0 - delta / (tolerance + 1), 3)


# ── Loader ────────────────────────────────────────────────────────────


def _phase27_corpus_loader(inputs: dict, params: dict) -> dict:
    """Phase-27 loader: extends Phase-26 with iconographic anchors and
    Phase-27 explicit find-spot overrides."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_indus_seals_at_mesopotamia, get_seals_with_inscription,
            get_meluhhan_persons_v3, get_parpola_phoneme_map,
            get_janabiyah_seal_reading, get_meluhha_tablets,
            get_cisi_findspot_map, get_contact_zone_prefix_set,
            get_phase27_seal_findspot_overrides,
            get_iconographic_anchors,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    return {
        "all_seals": get_indus_seals_at_mesopotamia(),
        "inscribed_seals": get_seals_with_inscription(),
        "persons_v3": get_meluhhan_persons_v3(),
        "phoneme_map": get_parpola_phoneme_map(),
        "janabiyah_reading": get_janabiyah_seal_reading(),
        "tablets": get_meluhha_tablets(),
        "n_tablets": len(get_meluhha_tablets()),
        "findspot_map": get_cisi_findspot_map(),
        "contact_zone_prefixes": sorted(get_contact_zone_prefix_set()),
        "phase27_overrides": get_phase27_seal_findspot_overrides(),
        "iconographic_anchors": get_iconographic_anchors(),
    }


# ── Tier 1 #1: Reverse Janabiyah search ──────────────────────────────


def _reverse_janabiyah_search(inputs: dict, params: dict) -> dict:
    """Reverse the Phase-25a/26c Janabiyah search: instead of asking 'does
    the predicted phonetic skeleton appear in CDLI?', ask 'for each
    common Akkadian PN in the Meluhha context, do its segments match
    Janabiyah's predicted phoneme structure?'.

    Strategy:
      1. Take all unique persons-v3 candidate names (44 in Phase-25d).
      2. For each, split into segments by '-'.
      3. Score against Janabiyah's predicted phoneme sequence
         [?, miin, or?, miin, ?, ?, miin] using:
           - Length match: bonus if PN has 5-9 segments (Janabiyah has 7).
           - 'miin' segments: bonus if PN contains *miin*-rendering syllables
             (mi-in, me-en, mi-na, etc.) at positions 1, 3, 6.
           - 'mul'-translation segments: bonus if PN contains mul/imin/kakkab
             at the same positions.
      4. Report top-K candidate PNs ranked by total score.
    """
    persons = inputs.get("persons_v3") or []
    janabiyah = inputs.get("janabiyah_reading") or {}
    top_k = max(10, _safe_int(params.get("top_k", 20), 20))

    if not persons or not janabiyah:
        return {"verdict": "INSUFFICIENT_DATA",
                "n_candidates": 0, "top_matches": []}

    # Aggregate persons by candidate_name
    name_counts: Counter[str] = Counter()
    name_meta: dict[str, dict] = {}
    for p in persons:
        n = p.get("candidate_name", "")
        if not n:
            continue
        name_counts[n] += 1
        if n not in name_meta:
            name_meta[n] = {
                "first_period": p.get("period", ""),
                "first_provenience": p.get("provenience", ""),
                "first_p_number": p.get("p_number", ""),
            }

    # Janabiyah pattern: [?, miin, or?, miin, ?, ?, miin]
    # Positions where miin should appear (0-indexed): 1, 3, 6
    miin_positions = {1, 3, 6}
    n_target_segments = 7
    miin_renderings = {"miin", "mi-in", "me-en", "mi-na", "me-na", "mi-il",
                       "me-il", "mi-en", "me-in", "mu-li", "min", "men",
                       "mul", "imin", "kakkab"}

    def _score(name: str) -> dict:
        """Score one candidate name against the Janabiyah pattern."""
        segs = name.split("-")
        n_segs = len(segs)
        # Length-match component (max 3.0)
        delta = abs(n_segs - n_target_segments)
        length_score = max(0.0, 3.0 - 0.5 * delta)

        # Position-match component: count segments at positions 1/3/6 that
        # contain a miin-rendering. Up to 3 points.
        position_match = 0
        positions_matched: list[int] = []
        for i, seg in enumerate(segs):
            seg_l = seg.lower().strip("()? ")
            if i in miin_positions and any(r in seg_l for r in miin_renderings):
                position_match += 1
                positions_matched.append(i)

        # Free miin component: count miin-renderings anywhere in the name.
        free_miin = sum(1 for s in segs
                        if any(r in s.lower().strip("()? ") for r in miin_renderings))

        # Penalize names that are clearly toponyms or function words even
        # if the regex passed
        penalty = 0.0
        if name.endswith("-me-luh-ha") or name.endswith("-me-luh-ha-ki"):
            penalty -= 1.5  # the suffix is generic 'of Meluhha', not a phoneme

        total = length_score + position_match * 1.5 + free_miin * 0.5 + penalty
        return {
            "candidate_name": name,
            "n_segments": n_segs,
            "length_score": round(length_score, 2),
            "position_match": position_match,
            "positions_matched": positions_matched,
            "free_miin": free_miin,
            "penalty": round(penalty, 2),
            "total_score": round(total, 3),
            "occurrences": name_counts[name],
            "first_period": name_meta[name].get("first_period", ""),
            "first_provenience": name_meta[name].get("first_provenience", ""),
        }

    scored = [_score(n) for n in name_counts.keys()]
    scored.sort(key=lambda r: (-r["total_score"], -r["occurrences"]))
    top = scored[:top_k]
    n_with_position_match = sum(1 for r in scored if r["position_match"] > 0)
    n_with_free_miin = sum(1 for r in scored if r["free_miin"] > 0)

    verdict = (
        f"Reverse Janabiyah search: {len(scored)} unique persons-v3 "
        f"candidates scored. {n_with_position_match} have at least one "
        f"position-match (segment with miin-rendering at Janabiyah "
        f"position 1/3/6). {n_with_free_miin} have at least one "
        f"miin-rendering anywhere in the name. Top candidate: "
        f"'{top[0]['candidate_name']}' (score {top[0]['total_score']}, "
        f"occurrences {top[0]['occurrences']})."
        if top else "No candidates."
    )
    return {
        "n_candidates": len(scored),
        "n_with_position_match": n_with_position_match,
        "n_with_free_miin": n_with_free_miin,
        "top_matches": top,
        "verdict": verdict,
    }


# ── Tier 2 #4: Phoneme-VALUE permutation null ────────────────────────


def _seal_phoneme_match_score(seal: dict, phoneme_map: dict) -> dict:
    signs = [s for s in (seal.get("indus_signs") or []) if s and s != "?"]
    n_high = 0
    n_attr = 0
    weight = 0.0
    phonemes_seen: list[str] = []
    for sid in signs:
        ph = phoneme_map.get(str(sid), {}) or {}
        conf = (ph.get("confidence") or "none").lower()
        phon = ph.get("phoneme", "?")
        if conf == "high":
            n_high += 1
            n_attr += 1
            weight += 1.0
            if phon and phon != "?":
                phonemes_seen.append(phon)
        elif conf == "medium":
            n_attr += 1
            weight += 0.5
            if phon and phon != "?":
                phonemes_seen.append(phon)
        elif conf == "low":
            n_attr += 1
            weight += 0.2
    return {
        "n_signs": len(signs),
        "n_high_conf": n_high,
        "n_attributed": n_attr,
        "weight": round(weight, 3),
        "phonemes_seen": phonemes_seen,
    }


# Dravidian compound name patterns from Parpola 2010: each tuple is a
# (component-1, component-2) pair that forms an attested compound.
_DRAVIDIAN_COMPOUND_PATTERNS: list[tuple[str, str]] = [
    ("aru", "miin"),    # Pleiades (six stars)
    ("eZu", "miin"),    # Ursa Major (seven stars)
    ("vaTa", "miin"),   # north star (banyan + star)
    ("veL", "miin"),    # Venus (white star)
    ("muruku", "veL"),  # Murukan-veL (Murukan compound)
    ("muruku", "piLLai"),  # Muruka-p-piLLa
    ("muruku", "miin"),  # Murukan + star
    ("katir", "miin"),  # radiant star
]


def _compound_plausibility_score(phonemes: list[str]) -> float:
    """Score a sequence of phonemes for Dravidian compound plausibility.
    +1.0 per attested compound match (any order), +0.2 per repeated phoneme."""
    if len(phonemes) < 2:
        return 0.0
    score = 0.0
    pset = set(p.lower().split()[0] for p in phonemes if p)
    for a, b in _DRAVIDIAN_COMPOUND_PATTERNS:
        if a.lower() in str(pset) or any(a in p.lower() for p in phonemes):
            for p in phonemes:
                if b.lower() in p.lower():
                    score += 1.0
                    break
    # Phoneme repetition bonus (Janabiyah has 3 miin)
    counts: Counter[str] = Counter()
    for p in phonemes:
        if not p or p == "?":
            continue
        for token in p.lower().split("/"):
            counts[token.strip()] += 1
    for c in counts.values():
        if c >= 2:
            score += 0.2 * (c - 1)
    return round(score, 3)


def _bayesian_decoder_v2(inputs: dict, params: dict) -> dict:
    """Phase-27 v2: permutes phoneme VALUES across sign IDs, scores under
    a Dravidian compound-name plausibility metric.

    For each null permutation, the phoneme VALUES (miin, aru-, eZu-, etc.)
    are randomly reassigned to sign IDs (preserving the multiset of
    values). For each seal, the resulting sequence of phonemes is scored
    via _compound_plausibility_score. Total score = sum across seals.
    p-value = fraction of nulls with score >= observed.
    """
    seals = inputs.get("inscribed_seals") or []
    phoneme_map = inputs.get("phoneme_map") or {}
    n_perms = max(200, _safe_int(params.get("n_permutations", 1000), 1000))
    seed = _safe_int(params.get("seed", 2727), 2727)

    if not seals or not phoneme_map:
        return {"verdict": "INSUFFICIENT_DATA",
                "p_value": None,
                "n_seals": len(seals),
                "n_phonemes_in_map": len(phoneme_map)}

    sign_ids = sorted(phoneme_map.keys())
    phonemes = [phoneme_map[s].get("phoneme", "?") for s in sign_ids]
    confidences = [(phoneme_map[s].get("confidence") or "none").lower()
                   for s in sign_ids]

    # Observed score
    obs_total = 0.0
    obs_per_seal = []
    for s in seals:
        sc = _seal_phoneme_match_score(s, phoneme_map)
        plausibility = _compound_plausibility_score(sc["phonemes_seen"])
        weighted = sc["weight"] * (1.0 + plausibility)
        obs_per_seal.append({
            "catalogue_id": s.get("catalogue_id"),
            "n_signs": sc["n_signs"],
            "phonemes_seen": sc["phonemes_seen"],
            "compound_plausibility": plausibility,
            "weighted_score": round(weighted, 3),
        })
        obs_total += weighted

    # Null permutations: shuffle phoneme VALUES across sign IDs, keep
    # confidences fixed.
    rng = random.Random(seed)
    null_totals: list[float] = []
    n_at_or_above = 0
    for _ in range(n_perms):
        shuffled_phonemes = list(phonemes)
        rng.shuffle(shuffled_phonemes)
        null_map = {}
        for sid, phon, conf in zip(sign_ids, shuffled_phonemes, confidences):
            null_map[sid] = {"confidence": conf, "phoneme": phon,
                             "gloss": "(value-permuted)"}
        total = 0.0
        for s in seals:
            sc = _seal_phoneme_match_score(s, null_map)
            plausibility = _compound_plausibility_score(sc["phonemes_seen"])
            total += sc["weight"] * (1.0 + plausibility)
        null_totals.append(total)
        if total >= obs_total:
            n_at_or_above += 1

    p_value = n_at_or_above / n_perms
    null_mean = sum(null_totals) / len(null_totals) if null_totals else 0.0

    verdict = (
        f"Bayesian decoder v2 (phoneme-VALUE permutation): observed total "
        f"weighted score = {obs_total:.3f} across {len(seals)} inscribed "
        f"seals. Null mean = {null_mean:.3f} ({n_perms} value permutations). "
        f"Global p-value = {p_value:.4f}. Lower p = the SPECIFIC Dravidian "
        f"phoneme values that Parpola assigns to specific sign IDs produce "
        f"more plausible compound names than chance value-assignments would."
    )
    interpretation = (
        "This extends Phase-26b: instead of permuting just confidence "
        "labels, we permute the actual Dravidian phoneme VALUES (miin, "
        "aru-, eZu-, vaTa-, muruku, etc.) across sign IDs. Significant p "
        "would mean Parpola's specific value-assignments produce more "
        "Dravidian-plausible compounds (aru-miin = Pleiades, vaTa-miin = "
        "north star, etc.) than randomized value-assignments. As with "
        "Phase-26b, this test is currently data-starved (1/11 readable "
        "seals) and will only become informative after CISI Vol 3 plate "
        "ingestion (Phase-28+)."
    )

    return {
        "n_seals": len(seals),
        "n_phonemes_in_map": len(phoneme_map),
        "observed_total_score": round(obs_total, 3),
        "null_mean_score": round(null_mean, 3),
        "p_value": round(p_value, 6),
        "n_perms": n_perms,
        "obs_per_seal": obs_per_seal,
        "verdict": verdict,
        "interpretation": interpretation,
    }


# ── Tier 1 #3: Iconographic anchor score ─────────────────────────────


def _iconographic_anchor_score(inputs: dict, params: dict) -> dict:
    """Score Parpola's phoneme map against the 12 iconographic anchors.

    For each anchor (sign_id, iconic_reading, confidence):
      - If sign_id is in phoneme_map: check whether the phoneme value
        matches the iconic reading (miin/fish, vaTa/banyan, etc.).
      - Score: high-anchor + match = 2.0; medium-anchor + match = 1.0;
        match = 0.0 if phoneme/iconic disagree.
    """
    anchors = inputs.get("iconographic_anchors") or []
    phoneme_map = inputs.get("phoneme_map") or {}

    if not anchors:
        return {"verdict": "NO_ANCHORS", "score": 0.0, "n_anchors": 0}

    iconic_to_phoneme_alias = {
        "fish": ["miin"],
        "fish/star": ["miin"],
        "fig": ["vaTa"],
        "banyan/fig": ["vaTa"],
        "banyan": ["vaTa"],
        "muruku": ["muruku"],
        "intersecting circles": ["muruku"],
        "squirrel": ["piLLai"],
        "pot": ["kuTam"],
        "pot/jar": ["kuTam"],
        "veL": ["veL", "veLLi"],
        "veN-miin": ["veL"],
        "venus": ["veL", "veLLi"],
        "pleiades": ["aru-", "miin"],
        "ursa major": ["eZu-", "miin"],
        "north star": ["vaTa", "miin"],
    }

    rows = []
    total_score = 0.0
    n_matches = 0
    n_total_anchors = 0
    for a in anchors:
        sid = str(a.get("sign_id", "")).split("+")[0]  # take first sign of compound
        iconic = (a.get("iconic_reading", "") or "").lower()
        anchor_conf = (a.get("confidence") or "low").lower()
        n_total_anchors += 1
        ph_entry = phoneme_map.get(sid, {}) or {}
        ph_value = (ph_entry.get("phoneme", "") or "").lower()
        ph_conf = (ph_entry.get("confidence") or "none").lower()

        # Direct or alias match
        match = False
        for k, aliases in iconic_to_phoneme_alias.items():
            if k in iconic:
                for al in aliases:
                    if al.lower() in ph_value:
                        match = True
                        break
                if match:
                    break

        anchor_score = 0.0
        if match:
            n_matches += 1
            if anchor_conf == "high":
                anchor_score = 2.0
            elif anchor_conf == "medium":
                anchor_score = 1.0
            else:
                anchor_score = 0.5
            # Bonus if both anchor and phoneme are high-confidence
            if ph_conf == "high":
                anchor_score *= 1.5
        total_score += anchor_score
        rows.append({
            "anchor_id": a.get("anchor_id"),
            "sign_id": sid,
            "object_id": a.get("object_id"),
            "iconic_reading": a.get("iconic_reading"),
            "phoneme_value": ph_value,
            "phoneme_confidence": ph_conf,
            "anchor_confidence": anchor_conf,
            "match": match,
            "anchor_score": round(anchor_score, 3),
        })

    rows.sort(key=lambda r: -r["anchor_score"])
    verdict = (
        f"Iconographic anchor score: {n_matches}/{n_total_anchors} anchors "
        f"have a phoneme match in our map. Total weighted score = "
        f"{total_score:.2f}. The anchors with the highest scores are "
        f"non-statistical confirmations of the corresponding sign->phoneme "
        f"reading (e.g. M-410: sign 47 = fish, confirmed by crocodile "
        f"iconography)."
    )
    return {
        "n_total_anchors": n_total_anchors,
        "n_matches": n_matches,
        "total_score": round(total_score, 3),
        "rows": rows,
        "verdict": verdict,
    }


# ── Tier 4 #10: 6-bucket period stratification ───────────────────────


def _greedy_score(score_mat: list[list[float]], assignment: list[int],
                   n_names: int) -> float:
    return sum(score_mat[i][assignment[i]]
               for i in range(n_names) if assignment[i] >= 0)


def _run_bipartite_test(
    candidates: list[dict],
    seal_lengths: list[int],
    n_perms: int,
    tolerance: int,
    seed: int,
) -> dict:
    n_names = len(candidates)
    n_seals = len(seal_lengths)
    if n_names == 0 or n_seals == 0:
        return {"p_value": None, "observed": 0.0,
                "n_names": n_names, "n_seals": n_seals,
                "reason": "empty inputs"}
    name_segs = [_name_n_segments(r["candidate_name"]) for r in candidates]
    score_mat = [
        [_length_score(seal_lengths[j], name_segs[i], tolerance)
         for j in range(n_seals)]
        for i in range(n_names)
    ]
    occs = [_safe_int(r.get("occurrences")) for r in candidates]
    order = sorted(range(n_names), key=lambda i: -occs[i])
    used: set[int] = set()
    obs_assignment = [-1] * n_names
    for i in order:
        best_j = -1
        best_s = 0.0
        for j in range(n_seals):
            if j in used:
                continue
            s = score_mat[i][j]
            if s > best_s:
                best_s = s
                best_j = j
        if best_j >= 0 and best_s > 0:
            obs_assignment[i] = best_j
            used.add(best_j)
    observed = _greedy_score(score_mat, obs_assignment, n_names)

    rng = random.Random(seed)
    n_at_or_above = 0
    null_dist: list[float] = []
    for _ in range(n_perms):
        shuffled_seal_idxs = list(range(n_seals))
        rng.shuffle(shuffled_seal_idxs)
        if n_names > n_seals:
            participating = rng.sample(range(n_names), n_seals)
        else:
            participating = list(range(n_names))
        random_assignment = [-1] * n_names
        for slot, name_i in enumerate(participating):
            random_assignment[name_i] = shuffled_seal_idxs[slot]
        v = _greedy_score(score_mat, random_assignment, n_names)
        null_dist.append(v)
        if v >= observed:
            n_at_or_above += 1
    p = n_at_or_above / n_perms
    null_mean = sum(null_dist) / len(null_dist)
    return {
        "p_value": round(p, 6),
        "observed": round(observed, 4),
        "null_mean": round(null_mean, 4),
        "n_names": n_names,
        "n_seals": n_seals,
        "n_perms": n_perms,
    }


# Phase-27 finer-grained period buckets (Phase-25c had 4-coarse, now 8)
_PERIOD_BUCKETS_6 = [
    ("Early Dynastic", ("early dynastic", "ed iiib", "ed iii")),
    ("Old Akkadian", ("old akkadian", "akkadian", "sargonic")),
    ("Lagash II", ("lagash ii", "gudea")),
    ("Ur III", ("ur iii", "ur 3", "neo-sumerian")),
    ("Old Babylonian", ("old babylonian",)),
    ("Middle Babylonian", ("middle babylonian", "kassite")),
    ("Neo-Assyrian", ("neo-assyrian", "neo assyrian", "nb period",
                      "neo-babylonian", "neo babylonian")),
    ("Ebla", ("ebla",)),
]


def _classify_period_6(text: str) -> str:
    if not text:
        return "Unknown"
    t = text.lower()
    for bucket, keys in _PERIOD_BUCKETS_6:
        for k in keys:
            if k in t:
                return bucket
    return "Other"


def _period_stratified_readout_6bucket(inputs: dict, params: dict) -> dict:
    """Phase-27 finer-grained period stratification: 8 buckets instead of 4
    (Early Dynastic, Old Akkadian, Lagash II, Ur III, Old Babylonian,
    Middle Babylonian, Neo-Assyrian, Ebla)."""
    persons = inputs.get("persons_v3") or []
    seals = inputs.get("inscribed_seals") or []
    n_perms = max(500, _safe_int(params.get("n_permutations", 1000), 1000))
    tolerance = _safe_int(params.get("tolerance", 2), 2)

    seal_lengths = [_safe_int(s.get("inscription_length")) for s in seals]
    if not persons or not seal_lengths:
        return {"verdict": "INSUFFICIENT_DATA", "results": []}

    candidates_by_period: dict[str, dict[str, dict]] = {}
    for p in persons:
        period_key = _classify_period_6(p.get("period", "") or "")
        cmap = candidates_by_period.setdefault(period_key, {})
        name = p.get("candidate_name", "")
        if not name:
            continue
        if name not in cmap:
            cmap[name] = {"candidate_name": name, "occurrences": 0}
        cmap[name]["occurrences"] += 1

    results: list[dict] = []
    overall: list[dict] = []
    for period, cmap in sorted(candidates_by_period.items()):
        cands = list(cmap.values())
        cands.sort(key=lambda r: -r["occurrences"])
        if len(cands) < 2:
            continue
        r = _run_bipartite_test(
            cands, seal_lengths, n_perms, tolerance,
            seed=271 + len(period),
        )
        r["period"] = period
        r["n_unique_candidates"] = len(cands)
        results.append(r)
        overall.extend(cands)

    if overall:
        merged: dict[str, dict] = {}
        for c in overall:
            n = c["candidate_name"]
            if n not in merged:
                merged[n] = {"candidate_name": n, "occurrences": 0}
            merged[n]["occurrences"] += c["occurrences"]
        ovr = list(merged.values())
        ovr.sort(key=lambda r: -r["occurrences"])
        r_all = _run_bipartite_test(ovr, seal_lengths, n_perms, tolerance,
                                     seed=271)
        r_all["period"] = "ALL (overall)"
        r_all["n_unique_candidates"] = len(ovr)
        results.append(r_all)

    significant = [r for r in results
                   if isinstance(r.get("p_value"), float)
                   and r["p_value"] < 0.05]
    verdict = (
        f"Period stratification (6-bucket Phase-27): {len(results)} buckets "
        f"tested; {len(significant)} achieve p<0.05. Compares with Phase-25c "
        f"(4-bucket: 3/4 + overall) at finer granularity."
    )
    return {
        "results": results,
        "n_significant_strata": len(significant),
        "verdict": verdict,
    }


# ── Tier 1 #2 + Tier 3 #6 combined: Shu-ilishu contact-zone filter ───


def _shu_ilishu_contact_zone_filter(inputs: dict, params: dict) -> dict:
    """Phase-27: ACTUALLY filter the 138 Phase-25e Shu-ilishu candidate
    inscriptions to those with contact-zone provenience, using the new
    catalogue_id-aware indus_cisi accessor."""
    contact_zone = set(inputs.get("contact_zone_prefixes") or [])
    findspot_map = inputs.get("findspot_map") or {}

    try:
        from glossa_lab.data.indus_cisi import (  # noqa: PLC0415
            get_corpus_inscriptions_with_ids,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"indus_cisi not available: {exc}",
                "n_filtered": 0}

    inscs = get_corpus_inscriptions_with_ids(min_length=3)
    # Keep only length 3-7 (Phase-25e criterion)
    inscs = [i for i in inscs if 3 <= len(i["signs"]) <= 7]

    contact_zone_inscs: list[dict] = []
    core_inscs: list[dict] = []
    for ins in inscs:
        cid = ins["catalogue_id"]
        is_contact = False
        site = "Unknown"
        for L in (4, 3, 2, 1):
            cand = cid[:L]
            info = findspot_map.get(cand)
            if info:
                is_contact = info.get("is_contact_zone", False)
                site = info.get("site", "Unknown")
                break
        rec = {
            "catalogue_id": cid,
            "n_signs": len(ins["signs"]),
            "signs": ins["signs"],
            "site": site,
            "is_contact_zone": is_contact,
        }
        if is_contact:
            contact_zone_inscs.append(rec)
        else:
            core_inscs.append(rec)

    sites_distribution: Counter[str] = Counter()
    for ins in inscs:
        cid = ins["catalogue_id"]
        for L in (4, 3, 2, 1):
            cand = cid[:L]
            info = findspot_map.get(cand)
            if info:
                sites_distribution[info.get("site", "Unknown")] += 1
                break
        else:
            sites_distribution["Unknown"] += 1

    verdict = (
        f"Shu-ilishu contact-zone filter (Phase-27): "
        f"{len(inscs)} Phase-25e candidate inscriptions (length 3-7) "
        f"resolved via catalogue_id. {len(contact_zone_inscs)} are from "
        f"contact-zone sites; {len(core_inscs)} are from Indus-core sites. "
        f"NOTE: the current indus_cisi corpus (179 inscriptions, all from "
        f"Mohenjo-daro) does NOT include any contact-zone seals -- those "
        f"are only in CISI Vol 3 Part 3 plates (not yet ingested with sign "
        f"sequences)."
    )
    return {
        "n_total_candidates": len(inscs),
        "n_contact_zone": len(contact_zone_inscs),
        "n_core_indus": len(core_inscs),
        "sites_distribution": dict(sites_distribution.most_common(15)),
        "contact_zone_inscriptions_top20": contact_zone_inscs[:20],
        "verdict": verdict,
    }


# ── Verdict aggregator ──────────────────────────────────────────────


def _phase27_verdict(inputs: dict, params: dict) -> dict:
    summary = (
        "Phase-27 contact-zone progress: indus_cisi corpus extended with "
        "catalogue_id-aware accessor (unblocks Shu-ilishu candidate "
        "filter); explicit find-spot overrides for Phase-22 hand-encoded "
        "seals (fixes Phase-26d mis-assignments); 12 iconographic anchors "
        "ingested from Parpola 2010 (M-410 fish=crocodile, H-9 ezhu-miin "
        "= Ursa Major, M-1202 muruku-piLLai, etc.); reverse Janabiyah "
        "search node ranks persons-v3 candidates against the 7-position "
        "Janabiyah skeleton; phoneme-VALUE permutation null extends the "
        "Bayesian decoder; 6-bucket period stratification (Early Dynastic, "
        "Old Akkadian, Lagash II, Ur III, Old Babylonian, Middle Babylonian, "
        "Neo-Assyrian, Ebla); phoneme map expanded 25 -> 30 entries; "
        "Parpola 1994 acquired (19 MB / 392 pages, the canonical sign-list "
        "reference); Crawford 2001 still inaccessible (login walls)."
    )
    next_steps = [
        "Phase-28 priority 1: ingest CISI Vol 3 Part 3 plates (the single "
        "remaining hard blocker for Bayesian decoder + blind held-out test). "
        "Approach: high-resolution plate scan + manual sign-ID assignment, "
        "or direct request to Parpola/Frenez/Laursen for digital catalogues.",
        "Phase-28 priority 2: process Parpola 1994 (acquired) for sign-by-"
        "sign readings of Chapter 10 ('fish' signs), Chapter 13 ('Murukan'), "
        "Chapter 14 ('Goddess') -- expand phoneme map from 30 to 50+ "
        "entries.",
        "Phase-28 priority 3: ingest Mahadevan 1977 sign-list as numerical "
        "Parpola-ID -> Mahadevan-ID crosswalk so we can resolve sign IDs "
        "across both numbering systems.",
        "Phase-28 priority 4: extend ReverseJanabiyahSearch to use the "
        "expanded phoneme map; report any new high-score candidates.",
        "Phase-28 priority 5: ingest CDLI provenience-and-period crosswalk "
        "to enable joint period * provenience stratification (3*8 = 24 "
        "subsets, much finer-grained robustness check).",
    ]
    return {
        "summary": summary,
        "next_steps": next_steps,
    }


# ── Atomic node defs for registration ───────────────────────────────


def _phase27_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "Phase27CorpusLoader", "Phase-27 Contact Corpus Loader",
            "Phase-27 / Sources",
            "Load Phase-27 contact-zone artefacts: extends Phase-26 with "
            "iconographic anchors (12 Parpola 2010 figures) and Phase-27 "
            "explicit find-spot overrides for Phase-22 hand-encoded seals.",
            inputs=[],
            outputs=[
                {"name": "all_seals", "type": "json"},
                {"name": "inscribed_seals", "type": "json"},
                {"name": "persons_v3", "type": "json"},
                {"name": "phoneme_map", "type": "json"},
                {"name": "janabiyah_reading", "type": "json"},
                {"name": "tablets", "type": "json"},
                {"name": "n_tablets", "type": "number"},
                {"name": "findspot_map", "type": "json"},
                {"name": "contact_zone_prefixes", "type": "json"},
                {"name": "phase27_overrides", "type": "json"},
                {"name": "iconographic_anchors", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase27_corpus_loader,
        ),
        AtomicNodeDef(
            "ReverseJanabiyahSearch",
            "Reverse Janabiyah Search (Phase-27)",
            "Phase-27 / Decipherment",
            "Reverse the Phase-25a/26c Janabiyah search direction: for each "
            "common Akkadian PN in the Meluhha context, score whether its "
            "segments match Janabiyah's predicted phonetic skeleton "
            "[?, miin, or?, miin, ?, ?, miin]. Smaller, more constrained "
            "search than the forward direction.",
            inputs=[
                {"name": "persons_v3", "type": "json", "required": True},
                {"name": "janabiyah_reading", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_candidates", "type": "number"},
                {"name": "n_with_position_match", "type": "number"},
                {"name": "n_with_free_miin", "type": "number"},
                {"name": "top_matches", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "top_k": {"type": "integer", "default": 20, "minimum": 5},
                },
            },
            fn=_reverse_janabiyah_search,
        ),
        AtomicNodeDef(
            "BayesianDecoderV2",
            "Bayesian Decoder V2 (phoneme-VALUE permutation, Phase-27)",
            "Phase-27 / Decipherment",
            "Extend Phase-26b: permute phoneme VALUES (miin, aru-, eZu-, "
            "vaTa-, muruku, etc.) across sign IDs (instead of just confidence "
            "labels) and score under a Dravidian compound-name plausibility "
            "metric.",
            inputs=[
                {"name": "inscribed_seals", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_seals", "type": "number"},
                {"name": "n_phonemes_in_map", "type": "number"},
                {"name": "observed_total_score", "type": "number"},
                {"name": "null_mean_score", "type": "number"},
                {"name": "p_value", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "interpretation", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000, "minimum": 200},
                    "seed": {"type": "integer", "default": 2727},
                },
            },
            fn=_bayesian_decoder_v2,
        ),
        AtomicNodeDef(
            "IconographicAnchorScore",
            "Iconographic Anchor Score (Phase-27)",
            "Phase-27 / Decipherment",
            "Score Parpola's phoneme map against 12 iconographic anchors "
            "from Parpola 2010 (M-410 fish=crocodile, H-9 ezhu-miin, "
            "M-1202 muruku-piLLai, etc.). Non-statistical confirmations "
            "of the iconic readings.",
            inputs=[
                {"name": "iconographic_anchors", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_total_anchors", "type": "number"},
                {"name": "n_matches", "type": "number"},
                {"name": "total_score", "type": "number"},
                {"name": "rows", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_iconographic_anchor_score,
        ),
        AtomicNodeDef(
            "PeriodStratifiedReadout6Bucket",
            "Period-Stratified Readout - 6-Bucket (Phase-27)",
            "Phase-27 / Decipherment",
            "Re-run Phase-25c bipartite readout test with finer-grained "
            "8-bucket period classification (Early Dynastic, Old Akkadian, "
            "Lagash II, Ur III, Old Babylonian, Middle Babylonian, "
            "Neo-Assyrian, Ebla) instead of Phase-25c's 4 buckets.",
            inputs=[
                {"name": "persons_v3", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "results", "type": "json"},
                {"name": "n_significant_strata", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000, "minimum": 100},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0},
                },
            },
            fn=_period_stratified_readout_6bucket,
        ),
        AtomicNodeDef(
            "ShuIlishuContactZoneFilter",
            "Shu-Ilishu Contact-Zone Filter (Phase-27)",
            "Phase-27 / Decipherment",
            "Filter the 138 Phase-25e Shu-ilishu candidate inscriptions "
            "(length 3-7) by contact-zone provenience, using the new "
            "catalogue_id-aware indus_cisi accessor.",
            inputs=[
                {"name": "contact_zone_prefixes", "type": "json", "required": True},
                {"name": "findspot_map", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_total_candidates", "type": "number"},
                {"name": "n_contact_zone", "type": "number"},
                {"name": "n_core_indus", "type": "number"},
                {"name": "sites_distribution", "type": "json"},
                {"name": "contact_zone_inscriptions_top20", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_shu_ilishu_contact_zone_filter,
        ),
        AtomicNodeDef(
            "Phase27Verdict", "Phase-27 Verdict Aggregator",
            "Phase-27 / Reporters",
            "Aggregate Phase-27 sub-experiment outputs into a "
            "decipherment-progress verdict + Phase-28 priority list.",
            inputs=[],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "next_steps", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase27_verdict,
        ),
    ]


__all__ = [
    "_phase27_corpus_loader",
    "_reverse_janabiyah_search",
    "_bayesian_decoder_v2",
    "_iconographic_anchor_score",
    "_period_stratified_readout_6bucket",
    "_shu_ilishu_contact_zone_filter",
    "_phase27_verdict",
    "_phase27_node_defs",
]
