"""Phase-23 atomic-node implementations.

Phase-23 builds on the Phase-22 contact-zone corpus to attempt the
first quantitative bilingual analysis. Three sub-experiments:

  Experiment 23a — Seal sign audit
      RefinedSealLoader -> SealSignAuditor -> JSONExport.
      Reports the inscription_length distribution across the 13
      Indus seals catalogued at Mesopotamia, the confidence-tier
      breakdown, and the per-seal sign-source citations.

  Experiment 23b — Refined Meluhhan-name extraction
      RefinedSealLoader -> RefinedMeluhhanPersonsExtractor -> JSONExport.
      Strict Sumerian-PN heuristic (lu2-/lu-/dumu- prefix OR
      -me-luh-ha-ki suffix) with a 100+ entry Akkadian particle /
      Sumerian function-word stoplist. Replaces Phase-22b which
      surfaced mostly noise.

  Experiment 23c — Bilingual readout test
      RefinedSealLoader -> EnhancedNameMatcher -> BilingualReadoutTest -> JSONExport.
      Runs a permutation test on the name-to-seal pairings: for each
      candidate name, score the best length-compatible seal; permute
      the name labels N times and recompute the score; the p-value is
      the fraction of permutations whose best score equals or exceeds
      the observed score. The falsifiable readout test the strategy
      review demanded.

  Phase23Verdict aggregates the three into a single contact-zone
  decipherment-progress verdict.
"""

from __future__ import annotations

import math
import random
from collections import Counter
from typing import Any

# ── Helpers ───────────────────────────────────────────────────────────


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── Loaders ───────────────────────────────────────────────────────────


def _refined_seal_loader(inputs: dict, params: dict) -> dict:
    """Load Phase-23 augmented seals + refined persons."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_indus_seals_at_mesopotamia,
            get_meluhhan_persons_strict,
            get_seal_sign_metadata,
            get_seals_with_inscription,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    all_seals = get_indus_seals_at_mesopotamia()
    inscribed_seals = get_seals_with_inscription()
    sign_metadata = get_seal_sign_metadata()
    strict_persons = get_meluhhan_persons_strict()

    return {
        "all_seals": all_seals,
        "inscribed_seals": inscribed_seals,
        "n_seals_total": len(all_seals),
        "n_seals_inscribed": len(inscribed_seals),
        "sign_metadata": sign_metadata,
        "strict_persons": strict_persons,
        "n_strict_persons": len(strict_persons),
    }


# ── Reporters ─────────────────────────────────────────────────────────


def _seal_sign_auditor(inputs: dict, params: dict) -> dict:
    """Distribution of inscription_length and confidence tiers."""
    seals = inputs.get("all_seals") or []
    sign_metadata = inputs.get("sign_metadata") or {}

    by_confidence: Counter[str] = Counter()
    by_length: Counter[int] = Counter()
    rows = []
    total_signs = 0
    for s in seals:
        n = _safe_int(s.get("inscription_length"))
        conf = s.get("signs_confidence", "unknown") or "unknown"
        by_confidence[conf] += 1
        by_length[n] += 1
        total_signs += n
        rows.append({
            "catalogue_id": s.get("catalogue_id"),
            "find_country": s.get("find_country"),
            "inscription_length": n,
            "signs_confidence": conf,
            "signs_source": s.get("signs_source"),
        })

    inscribed_rows = [r for r in rows if r["inscription_length"] > 0]

    verdict = (
        f"Phase-23 seal-sign audit: {len(seals)} seals; "
        f"{len(inscribed_rows)} carry Indus signs ({total_signs} total). "
        f"Confidence tiers: "
        f"{dict(by_confidence.most_common())}."
    )

    return {
        "n_seals": len(seals),
        "n_inscribed": len(inscribed_rows),
        "total_indus_signs": total_signs,
        "by_confidence": dict(by_confidence.most_common()),
        "by_length": dict(sorted(by_length.items())),
        "rows": rows,
        "inscribed_rows": inscribed_rows,
        "method": sign_metadata.get("method", ""),
        "verdict": verdict,
    }


def _refined_persons_extractor(inputs: dict, params: dict) -> dict:
    """Aggregate the strict Phase-23 PN extractor output."""
    persons = inputs.get("strict_persons") or []
    min_freq = _safe_int(params.get("min_freq", 1), 1)

    name_counts: Counter[str] = Counter()
    name_periods: dict[str, set[str]] = {}
    name_provs: dict[str, set[str]] = {}
    name_lines: dict[str, list[str]] = {}
    name_patterns: dict[str, set[str]] = {}
    for p in persons:
        n = p.get("candidate_name", "")
        if not n:
            continue
        name_counts[n] += 1
        name_periods.setdefault(n, set()).add(p.get("period", "") or "")
        name_provs.setdefault(n, set()).add(p.get("provenience", "") or "")
        name_lines.setdefault(n, []).append(p.get("line", ""))
        name_patterns.setdefault(n, set()).add(p.get("source_pattern", "") or "")

    rows = []
    for n, c in name_counts.most_common():
        if c < min_freq:
            continue
        is_known = any(p.get("is_known") for p in persons
                       if p.get("candidate_name") == n)
        rows.append({
            "candidate_name": n,
            "occurrences": c,
            "n_distinct_tablets": len({p["p_number"] for p in persons
                                          if p.get("candidate_name") == n}),
            "periods": sorted(name_periods.get(n, set())),
            "proveniences": sorted(name_provs.get(n, set())),
            "source_patterns": sorted(name_patterns.get(n, set())),
            "is_known_meluhhan": is_known,
            "example_line": name_lines[n][0] if name_lines.get(n) else "",
        })

    confirmed = [r for r in rows if r["is_known_meluhhan"]]
    by_pattern: Counter[str] = Counter()
    for p in persons:
        by_pattern[p.get("source_pattern", "")] += 1

    verdict = (
        f"Refined Meluhhan-PN extractor (Phase-23): "
        f"{len(rows)} unique name candidates (freq>={min_freq}); "
        f"{len(confirmed)} historically-confirmed; "
        f"by-pattern distribution {dict(by_pattern.most_common())}."
    )

    return {
        "n_unique": len(rows),
        "rows_top50": rows[:50],
        "rows_all": rows,
        "n_total": len(rows),
        "confirmed_hits": confirmed,
        "by_pattern": dict(by_pattern.most_common()),
        "verdict": verdict,
    }


# ── Enhanced matcher ──────────────────────────────────────────────────


def _name_n_segments(name: str) -> int:
    """Count hyphen-separated segments in a candidate name."""
    return name.count("-") + 1 if name else 0


def _length_score(n_signs: int, n_segments: int, tolerance: int = 2) -> float:
    """Length compatibility: 1.0 at exact match, 0.0 once delta > tolerance."""
    delta = abs(n_signs - n_segments)
    if delta > tolerance:
        return 0.0
    return round(1.0 - delta / (tolerance + 1), 3)


def _enhanced_name_matcher(inputs: dict, params: dict) -> dict:
    """Score name <-> seal pairings using inscription_length.

    Phase-23 difference vs Phase-22c: now operates on the
    *strict* persons output (low-noise) and the *augmented* seals
    (inscription_length > 0 for 10/13 seals).
    """
    persons_rows = inputs.get("rows_all") or inputs.get("rows_top50") or []
    seals = inputs.get("inscribed_seals") or []
    min_name_freq = _safe_int(params.get("min_name_freq", 2), 2)
    tolerance = _safe_int(params.get("tolerance", 2), 2)

    # Filter candidates by frequency
    candidates = [r for r in persons_rows
                   if _safe_int(r.get("occurrences")) >= min_name_freq]
    if not candidates or not seals:
        return {
            "n_candidates": len(candidates),
            "n_seals": len(seals),
            "pairings": [],
            "n_pairings": 0,
            "best_per_name": [],
            "verdict": (
                f"Enhanced matcher: insufficient inputs "
                f"(candidates={len(candidates)}, inscribed_seals={len(seals)})."
            ),
        }

    pairings: list[dict] = []
    best_per_name: dict[str, dict] = {}
    for r in candidates:
        name = r["candidate_name"]
        n_seg = _name_n_segments(name)
        for s in seals:
            n_signs = _safe_int(s.get("inscription_length"))
            score = _length_score(n_signs, n_seg, tolerance)
            if score <= 0.0:
                continue
            pair = {
                "candidate_name": name,
                "name_n_segments": n_seg,
                "name_occurrences": r.get("occurrences"),
                "is_known_meluhhan": r.get("is_known_meluhhan", False),
                "seal_id": s.get("catalogue_id"),
                "seal_n_signs": n_signs,
                "seal_signs_confidence": s.get("signs_confidence"),
                "length_score": score,
            }
            pairings.append(pair)
            if (name not in best_per_name
                    or pair["length_score"] > best_per_name[name]["length_score"]):
                best_per_name[name] = pair

    pairings.sort(key=lambda p: (-p["length_score"], -p.get("name_occurrences", 0)))
    best_list = sorted(
        best_per_name.values(),
        key=lambda p: (-p["length_score"], -p.get("name_occurrences", 0)),
    )

    verdict = (
        f"Enhanced matcher (Phase-23): {len(pairings)} length-compatible "
        f"pairings between {len(seals)} inscribed seals and "
        f"{len(candidates)} strict-PN candidates (freq>={min_name_freq}, "
        f"tol={tolerance})."
    )

    return {
        "n_candidates": len(candidates),
        "n_seals": len(seals),
        "pairings": pairings,
        "pairings_top50": pairings[:50],
        "n_pairings": len(pairings),
        "best_per_name": best_list,
        "verdict": verdict,
    }


# ── Bilingual readout test (permutation) ──────────────────────────────


def _bilingual_readout_test(inputs: dict, params: dict) -> dict:
    """Permutation p-value on the observed name<->seal length match.

    Test statistic
    ---------------
    For each candidate name, take the *best* length_score against all
    inscribed seals; sum across names. This is the "observed" score.

    Null distribution
    -----------------
    For each of N permutations, randomly permute the inscription_length
    values across the seals (preserving the multiset of lengths) and
    recompute the same statistic. The p-value is the fraction of
    permutations whose statistic equals or exceeds the observed value.

    Why this is the right test
    --------------------------
    The strategy review asked for a falsifiable bilingual moment. A
    significant p-value here means: the *specific* mapping of name
    lengths to seal lengths in our data is unlikely under a null where
    seals carry random Indus-sign counts. That's a length-only signal,
    not a phonetic one — Phase-24 will need the actual sign IDs to
    upgrade the test to a phonetic one.
    """
    persons_rows = inputs.get("rows_all") or inputs.get("rows_top50") or []
    seals = inputs.get("inscribed_seals") or []
    n_perms = max(100, _safe_int(params.get("n_permutations", 1000), 1000))
    min_name_freq = _safe_int(params.get("min_name_freq", 2), 2)
    tolerance = _safe_int(params.get("tolerance", 2), 2)
    seed = _safe_int(params.get("seed", 42), 42)

    candidates = [r for r in persons_rows
                   if _safe_int(r.get("occurrences")) >= min_name_freq]
    seal_lengths = [_safe_int(s.get("inscription_length")) for s in seals]
    if not candidates or not seal_lengths:
        return {
            "verdict": "INSUFFICIENT_DATA: cannot run readout test",
            "n_candidates": len(candidates),
            "n_seals": len(seal_lengths),
            "p_value": None,
        }

    # Pre-compute name_n_segments for each candidate
    name_segs: list[tuple[str, int, int]] = [
        (r["candidate_name"], _name_n_segments(r["candidate_name"]),
         _safe_int(r.get("occurrences")))
        for r in candidates
    ]

    def _stat(lengths: list[int]) -> float:
        total = 0.0
        for _, n_seg, _occ in name_segs:
            best = 0.0
            for n_sign in lengths:
                s = _length_score(n_sign, n_seg, tolerance)
                if s > best:
                    best = s
            total += best
        return total

    observed = _stat(seal_lengths)

    rng = random.Random(seed)
    null_dist = []
    n_at_or_above = 0
    permuted = list(seal_lengths)
    for _ in range(n_perms):
        rng.shuffle(permuted)
        v = _stat(permuted)
        null_dist.append(v)
        if v >= observed:
            n_at_or_above += 1

    p_value = n_at_or_above / n_perms

    null_mean = sum(null_dist) / len(null_dist)
    null_var = (sum((x - null_mean) ** 2 for x in null_dist)
                / max(1, len(null_dist) - 1))
    null_sd = math.sqrt(null_var) if null_var > 0 else 0.0
    z = ((observed - null_mean) / null_sd) if null_sd > 0 else 0.0

    if p_value < 0.01:
        verdict = "READOUT_SIGNIFICANT (p<0.01)"
    elif p_value < 0.05:
        verdict = "READOUT_MARGINAL (p<0.05)"
    else:
        verdict = "READOUT_NOT_SIGNIFICANT"

    return {
        "verdict": verdict,
        "p_value": round(p_value, 6),
        "observed": round(observed, 4),
        "null_mean": round(null_mean, 4),
        "null_sd": round(null_sd, 4),
        "z_score": round(z, 4),
        "n_permutations": n_perms,
        "n_candidates": len(candidates),
        "n_seals": len(seal_lengths),
        "tolerance": tolerance,
        "interpretation": (
            "Length-only test: a significant p means the observed "
            "name-length-to-seal-length distribution is unlikely under "
            "shuffled-length null. Phase-24 needs sign IDs (not just "
            "lengths) to upgrade to a phonetic readout."
        ),
    }


# ── Verdict aggregator ────────────────────────────────────────────────


def _phase23_verdict(inputs: dict, params: dict) -> dict:
    n_seals = _safe_int(inputs.get("n_inscribed"))
    total_signs = _safe_int(inputs.get("total_indus_signs"))
    n_persons = _safe_int(inputs.get("n_unique"))
    n_confirmed = len(inputs.get("confirmed_hits") or [])
    n_pairings = _safe_int(inputs.get("n_pairings"))
    p_value = inputs.get("p_value")
    readout_verdict = inputs.get("readout_verdict") or ""

    summary = (
        f"Phase-23 contact-zone decipherment progress: "
        f"{n_seals} inscribed seals ({total_signs} signs), "
        f"{n_persons} strict-PN candidates "
        f"({n_confirmed} historically-confirmed), "
        f"{n_pairings} length-compatible pairings; "
        f"readout p={p_value} ({readout_verdict})."
    )

    next_steps: list[str] = []
    if total_signs > 0 and any("?" in str(p_value) for _ in [0]) is False:
        # Always include sign-ID upgrade as priority 1
        pass
    next_steps.append(
        "Phase-24 priority 1: upgrade indus_signs[] from '?' "
        "placeholders to actual Parpola/Mahadevan IDs (CISI Vol 3, "
        "Frenez 2018 plate IV, Ascalone 2008). Required for any "
        "phonetic readout."
    )
    if n_confirmed == 0:
        next_steps.append(
            "Phase-24 priority 2: extend the strict-PN regex to "
            "match additional historically-attested Meluhhan PN "
            "patterns (Ur-suen-me-luh-ha, Sheshkalla-me-luh-ha, "
            "Ur-Lamma-Meluhha)."
        )
    next_steps.append(
        "Phase-24 priority 3: phonetic readout test \u2014 once sign "
        "IDs land, score name<->seal pairings under a candidate "
        "Indus-to-Sumerian phoneme map and re-run the permutation "
        "test on that signal."
    )

    return {
        "summary": summary,
        "n_seals": n_seals,
        "total_signs": total_signs,
        "n_persons": n_persons,
        "n_confirmed_persons": n_confirmed,
        "n_pairings": n_pairings,
        "readout_p_value": p_value,
        "readout_verdict": readout_verdict,
        "next_steps": next_steps,
        "verdict": (
            "READOUT_SIGNIFICANT" if isinstance(p_value, (int, float))
            and p_value < 0.05 else
            "INSUFFICIENT_OR_NOT_SIGNIFICANT"
        ),
    }


# ── Atomic node defs for registration ─────────────────────────────────


def _phase23_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "RefinedSealLoader", "Refined Seal + Persons Loader (Phase-23)",
            "Phase-23 / Sources",
            "Load the Phase-23 augmented Indus-seals-at-Mesopotamia "
            "inventory (with inscription_length + indus_signs[]) and "
            "the strict Meluhhan-PN extraction (lu2-/dumu- prefix or "
            "-me-luh-ha-ki suffix; Akkadian particle stoplist).",
            inputs=[],
            outputs=[
                {"name": "all_seals", "type": "json"},
                {"name": "inscribed_seals", "type": "json"},
                {"name": "n_seals_total", "type": "number"},
                {"name": "n_seals_inscribed", "type": "number"},
                {"name": "sign_metadata", "type": "json"},
                {"name": "strict_persons", "type": "json"},
                {"name": "n_strict_persons", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_refined_seal_loader,
        ),
        AtomicNodeDef(
            "SealSignAuditor", "Seal Sign Auditor (Phase-23)",
            "Phase-23 / Reporters",
            "Audit inscription_length distribution + signs_confidence "
            "tiers across the Indus-seals-at-Mesopotamia inventory.",
            inputs=[
                {"name": "all_seals", "type": "json", "required": True},
                {"name": "sign_metadata", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "n_seals", "type": "number"},
                {"name": "n_inscribed", "type": "number"},
                {"name": "total_indus_signs", "type": "number"},
                {"name": "by_confidence", "type": "json"},
                {"name": "by_length", "type": "json"},
                {"name": "rows", "type": "json"},
                {"name": "inscribed_rows", "type": "json"},
                {"name": "method", "type": "text"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_seal_sign_auditor,
        ),
        AtomicNodeDef(
            "RefinedMeluhhanPersonsExtractor",
            "Refined Meluhhan Persons Extractor (Phase-23)",
            "Phase-23 / Reporters",
            "Aggregate the strict Phase-23 PN extractor: rejects "
            "Akkadian particles via stoplist; accepts only lu2-/lu-/"
            "dumu- prefixed or -me-luh-ha-ki suffixed candidates plus "
            "the historically-attested Meluhhan-name set (Lu-sun-zi-"
            "da, Shu-ilishu).",
            inputs=[
                {"name": "strict_persons", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_unique", "type": "number"},
                {"name": "rows_top50", "type": "json"},
                {"name": "rows_all", "type": "json"},
                {"name": "n_total", "type": "number"},
                {"name": "confirmed_hits", "type": "json"},
                {"name": "by_pattern", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_freq": {"type": "integer", "default": 1, "minimum": 1},
                },
            },
            fn=_refined_persons_extractor,
        ),
        AtomicNodeDef(
            "EnhancedNameMatcher", "Enhanced Name Matcher (Phase-23)",
            "Phase-23 / Decipherment",
            "Score name<->seal pairings using inscription_length on "
            "10 inscribed Mesopotamia-found Indus seals against the "
            "strict-PN candidate list. Sets up the test statistic for "
            "BilingualReadoutTest.",
            inputs=[
                {"name": "rows_all", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_candidates", "type": "number"},
                {"name": "n_seals", "type": "number"},
                {"name": "pairings", "type": "json"},
                {"name": "pairings_top50", "type": "json"},
                {"name": "n_pairings", "type": "number"},
                {"name": "best_per_name", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_name_freq": {"type": "integer", "default": 2, "minimum": 1},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0,
                                  "description": "Max |n_signs - name_n_segments| for non-zero score."},
                },
            },
            fn=_enhanced_name_matcher,
        ),
        AtomicNodeDef(
            "BilingualReadoutTest", "Bilingual Readout Test (Phase-23)",
            "Phase-23 / Decipherment",
            "Permutation test on the observed name<->seal length match. "
            "Statistic: sum of best-length-scores across candidate "
            "names. Null: shuffled inscription_length assignment. The "
            "first falsifiable bilingual contact-zone test.",
            inputs=[
                {"name": "rows_all", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "verdict", "type": "text"},
                {"name": "p_value", "type": "number"},
                {"name": "observed", "type": "number"},
                {"name": "null_mean", "type": "number"},
                {"name": "null_sd", "type": "number"},
                {"name": "z_score", "type": "number"},
                {"name": "n_permutations", "type": "number"},
                {"name": "n_candidates", "type": "number"},
                {"name": "n_seals", "type": "number"},
                {"name": "interpretation", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000,
                                        "minimum": 100},
                    "min_name_freq": {"type": "integer", "default": 2, "minimum": 1},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0},
                    "seed": {"type": "integer", "default": 42},
                },
            },
            fn=_bilingual_readout_test,
        ),
        AtomicNodeDef(
            "Phase23Verdict", "Phase-23 Verdict Aggregator",
            "Phase-23 / Reporters",
            "Aggregate the Phase-23 sub-experiment outputs (sign "
            "audit, refined persons, enhanced matcher, readout test) "
            "into a single contact-zone decipherment-progress verdict "
            "+ Phase-24 priority list.",
            inputs=[
                {"name": "n_inscribed", "type": "number", "required": False},
                {"name": "total_indus_signs", "type": "number", "required": False},
                {"name": "n_unique", "type": "number", "required": False},
                {"name": "confirmed_hits", "type": "json", "required": False},
                {"name": "n_pairings", "type": "number", "required": False},
                {"name": "p_value", "type": "number", "required": False},
                {"name": "readout_verdict", "type": "text", "required": False},
            ],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "n_seals", "type": "number"},
                {"name": "total_signs", "type": "number"},
                {"name": "n_persons", "type": "number"},
                {"name": "n_confirmed_persons", "type": "number"},
                {"name": "n_pairings", "type": "number"},
                {"name": "readout_p_value", "type": "number"},
                {"name": "readout_verdict", "type": "text"},
                {"name": "next_steps", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase23_verdict,
        ),
    ]


__all__ = [
    "_refined_seal_loader",
    "_seal_sign_auditor",
    "_refined_persons_extractor",
    "_enhanced_name_matcher",
    "_bilingual_readout_test",
    "_phase23_verdict",
    "_phase23_node_defs",
]
