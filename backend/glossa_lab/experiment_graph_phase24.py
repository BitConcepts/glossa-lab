"""Phase-24 atomic-node implementations.

Phase-24 builds on Phase-23 with four upgrades that address the
methodological flaw surfaced by Phase-23c (the readout test was
permutation-invariant) and the three structural-noise findings of
Phase-23b:

  Experiment 24a — Laursen 2010 Table 1 audit
      LaursenTable1Loader -> LaursenTable1Auditor -> JSONExport.
      Reports the parsed structure of Laursen 2010's canonical 121-row
      Gulf-Type seal catalogue (parsed by
      scripts/phase24/ingest_laursen_table1.py).

  Experiment 24b — Seal sign-ID upgrade audit
      RefinedSealLoaderV2 -> SealSignUpgradeAuditor -> JSONExport.
      Reports the Phase-24 sign-ID upgrade: cross-references with
      Laursen Table 1 (4 seals upgraded) + the Janabiyah seal #10
      added with full Parpola-1994b sign sequence (signs_confidence
      = 'high').

  Experiment 24c — Persons-v2 (toponym-filtered, wider window)
      RefinedSealLoaderV2 -> RefinedMeluhhanPersonsExtractorV2 -> JSONExport.
      Reports the Phase-24 strict persons extractor with toponym
      filter (drops e2-/bad3-/iri-/kur- prefixes), extended Akkadian
      stoplist (lu-u, ka-bal, sze-ga, ...), and widened tablet-window
      that scans every line of any tablet whose matched_keywords
      include me-luh-ha.

  Experiment 24d — Bilingual readout test v2 (proper null)
      RefinedSealLoaderV2 -> RefinedMeluhhanPersonsExtractorV2 ->
      EnhancedNameMatcherV2 -> BilingualReadoutTestV2 -> JSONExport.
      Replaces the Phase-23c statistic (permutation-invariant) with a
      *bipartite-assignment* permutation test: each candidate name is
      paired to exactly one seal (greedy by length match), and we
      permute the assignment vector. The null genuinely varies, so
      the p-value is meaningful.

  Phase24Verdict aggregates the four into a single contact-zone
  decipherment-progress verdict.
"""

from __future__ import annotations

import math
import random
from collections import Counter
from typing import Any


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── Loaders ───────────────────────────────────────────────────────────


def _laursen_table1_loader(inputs: dict, params: dict) -> dict:
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_laursen_table1, get_laursen_parpola_readings,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}
    rows = get_laursen_table1()
    parpola = get_laursen_parpola_readings()
    return {
        "rows": rows,
        "n_rows": len(rows),
        "parpola_readings": parpola,
        "n_parpola_readings": len(parpola),
    }


def _refined_seal_loader_v2(inputs: dict, params: dict) -> dict:
    """Phase-24 augmented seals + persons-v2 + Laursen Table 1."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_indus_seals_at_mesopotamia, get_seals_with_inscription,
            get_seal_sign_metadata, get_seal_sign_upgrade_metadata,
            get_meluhhan_persons_v2, get_laursen_table1,
            get_laursen_parpola_readings,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    all_seals = get_indus_seals_at_mesopotamia()
    inscribed_seals = get_seals_with_inscription()
    sign_metadata = get_seal_sign_metadata()
    upgrade_metadata = get_seal_sign_upgrade_metadata()
    persons_v2 = get_meluhhan_persons_v2()
    laursen_rows = get_laursen_table1()
    parpola = get_laursen_parpola_readings()

    return {
        "all_seals": all_seals,
        "inscribed_seals": inscribed_seals,
        "n_seals_total": len(all_seals),
        "n_seals_inscribed": len(inscribed_seals),
        "sign_metadata": sign_metadata,
        "upgrade_metadata": upgrade_metadata,
        "persons_v2": persons_v2,
        "n_persons_v2": len(persons_v2),
        "laursen_rows": laursen_rows,
        "n_laursen_rows": len(laursen_rows),
        "parpola_readings": parpola,
    }


# ── Auditors ──────────────────────────────────────────────────────────


def _laursen_table1_auditor(inputs: dict, params: dict) -> dict:
    rows = inputs.get("rows") or []
    parpola = inputs.get("parpola_readings") or {}
    by_type: Counter[str] = Counter()
    by_site: Counter[str] = Counter()
    n_inscribed = 0
    for r in rows:
        by_type[r.get("gulf_type", "(unknown)") or "(unknown)"] += 1
        by_site[r.get("site", "(unmatched)") or "(unmatched)"] += 1
        if "INDUS" in (r.get("gulf_type", "") or "").upper():
            n_inscribed += 1

    sample = []
    for r in rows[:8]:
        sample.append({
            "seal_no": r.get("seal_no"),
            "reference": (r.get("reference", "") or "")[:80],
            "gulf_type": r.get("gulf_type"),
            "site": r.get("site"),
        })

    verdict = (
        f"Laursen 2010 Table 1 audit: {len(rows)}/121 rows parsed; "
        f"{n_inscribed} inscribed Gulf-INDUS; {len(parpola)} seal(s) "
        f"with full Parpola sign-by-sign reading."
    )
    return {
        "n_rows": len(rows),
        "n_inscribed": n_inscribed,
        "n_parpola_readings": len(parpola),
        "by_gulf_type": dict(by_type.most_common()),
        "by_site_top10": dict(by_site.most_common(10)),
        "sample_rows": sample,
        "verdict": verdict,
    }


def _seal_sign_upgrade_auditor(inputs: dict, params: dict) -> dict:
    seals = inputs.get("all_seals") or []
    upgrade_md = inputs.get("upgrade_metadata") or {}

    by_confidence: Counter[str] = Counter()
    n_with_laursen_xref = 0
    upgrade_rows: list[dict] = []
    for s in seals:
        conf = s.get("signs_confidence", "unknown") or "unknown"
        by_confidence[conf] += 1
        if s.get("laursen_2010_seal_no") is not None:
            n_with_laursen_xref += 1
            upgrade_rows.append({
                "catalogue_id": s.get("catalogue_id"),
                "laursen_seal_no": s.get("laursen_2010_seal_no"),
                "inscription_length": s.get("inscription_length"),
                "signs_confidence": conf,
                "indus_signs": s.get("indus_signs"),
                "rationale": (
                    s.get("phase24_crossref_rationale", "") or ""
                )[:120],
            })

    n_high_conf = by_confidence.get("high", 0)
    total_signs = sum(_safe_int(s.get("inscription_length")) for s in seals)

    verdict = (
        f"Phase-24 sign-upgrade audit: {len(seals)} seals; "
        f"{n_with_laursen_xref} cross-referenced with Laursen Table 1; "
        f"{n_high_conf} with high-confidence Parpola IDs; "
        f"{total_signs} total Indus signs."
    )
    return {
        "n_seals": len(seals),
        "n_with_laursen_xref": n_with_laursen_xref,
        "n_high_conf": n_high_conf,
        "total_signs": total_signs,
        "by_confidence": dict(by_confidence.most_common()),
        "upgrade_rows": upgrade_rows,
        "metadata_summary": {
            "n_crossreferenced_with_laursen":
                upgrade_md.get("n_crossreferenced_with_laursen"),
            "n_seals_added": upgrade_md.get("n_seals_added"),
            "method": upgrade_md.get("method"),
        },
        "verdict": verdict,
    }


def _refined_persons_extractor_v2(inputs: dict, params: dict) -> dict:
    persons = inputs.get("persons_v2") or []
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

    rows: list[dict] = []
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
            "example_line": (name_lines[n][0] if name_lines.get(n) else "")[:120],
        })

    confirmed = [r for r in rows if r["is_known_meluhhan"]]
    by_pattern: Counter[str] = Counter()
    for p in persons:
        by_pattern[p.get("source_pattern", "")] += 1

    verdict = (
        f"Refined Meluhhan-PN extractor v2 (Phase-24): "
        f"{len(rows)} unique candidates (freq>={min_freq}); "
        f"{len(confirmed)} historically-confirmed; "
        f"by-pattern {dict(by_pattern.most_common())}."
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


# ── Bipartite-assignment matcher ──────────────────────────────────────


def _name_n_segments(name: str) -> int:
    return name.count("-") + 1 if name else 0


def _length_score(n_signs: int, n_segments: int, tolerance: int = 2) -> float:
    delta = abs(n_signs - n_segments)
    if delta > tolerance:
        return 0.0
    return round(1.0 - delta / (tolerance + 1), 3)


def _greedy_bipartite_assignment(
    name_segs: list[tuple[str, int, int]],
    seal_lengths: list[int],
    tolerance: int,
) -> dict[str, tuple[int, float]]:
    """Greedy bipartite: walk names from highest-occurrence to lowest;
    each takes the highest-scoring still-unused seal index. Returns
    {name -> (seal_idx, length_score)}.
    """
    assigned: dict[str, tuple[int, float]] = {}
    used: set[int] = set()
    # Sort names by occurrence desc so the most attested name picks first
    names_sorted = sorted(name_segs, key=lambda t: -t[2])
    for name, n_seg, _occ in names_sorted:
        best_idx = -1
        best_score = 0.0
        for idx, n_signs in enumerate(seal_lengths):
            if idx in used:
                continue
            sc = _length_score(n_signs, n_seg, tolerance)
            if sc > best_score:
                best_score = sc
                best_idx = idx
        if best_idx >= 0 and best_score > 0:
            assigned[name] = (best_idx, best_score)
            used.add(best_idx)
        else:
            assigned[name] = (-1, 0.0)
    return assigned


def _enhanced_name_matcher_v2(inputs: dict, params: dict) -> dict:
    """Phase-24 matcher: produces a bipartite assignment + scores.

    Differences vs Phase-23c matcher:
      - One seal per name (no double-use). Removes the multiset-
        invariance flaw that made the readout test return p=1.0.
      - Period-bucket awareness: emits a parallel period-overlap
        score per pairing.
    """
    persons_rows = inputs.get("rows_all") or inputs.get("rows_top50") or []
    seals = inputs.get("inscribed_seals") or []
    min_name_freq = _safe_int(params.get("min_name_freq", 1), 1)
    tolerance = _safe_int(params.get("tolerance", 2), 2)

    candidates = [r for r in persons_rows
                   if _safe_int(r.get("occurrences")) >= min_name_freq]
    if not candidates or not seals:
        return {
            "n_candidates": len(candidates),
            "n_seals": len(seals),
            "pairings": [],
            "n_pairings": 0,
            "verdict": (
                f"Matcher v2: insufficient inputs "
                f"(candidates={len(candidates)}, seals={len(seals)})."
            ),
        }

    name_segs = [
        (r["candidate_name"], _name_n_segments(r["candidate_name"]),
         _safe_int(r.get("occurrences")))
        for r in candidates
    ]
    seal_lengths = [_safe_int(s.get("inscription_length")) for s in seals]
    assignment = _greedy_bipartite_assignment(
        name_segs, seal_lengths, tolerance,
    )

    pairings: list[dict] = []
    name_to_row = {r["candidate_name"]: r for r in candidates}
    for name, (seal_idx, score) in assignment.items():
        if seal_idx < 0:
            continue
        seal = seals[seal_idx]
        row = name_to_row.get(name) or {}
        pairings.append({
            "candidate_name": name,
            "name_n_segments": _name_n_segments(name),
            "name_occurrences": row.get("occurrences"),
            "is_known_meluhhan": row.get("is_known_meluhhan", False),
            "seal_idx": seal_idx,
            "seal_id": seal.get("catalogue_id"),
            "seal_n_signs": _safe_int(seal.get("inscription_length")),
            "seal_signs_confidence": seal.get("signs_confidence"),
            "length_score": score,
        })
    pairings.sort(key=lambda p: (-p["length_score"],
                                  -(p.get("name_occurrences") or 0)))

    total_score = sum(p["length_score"] for p in pairings)
    n_assigned = len(pairings)

    return {
        "n_candidates": len(candidates),
        "n_seals": len(seals),
        "n_assigned": n_assigned,
        "n_unassigned": len(candidates) - n_assigned,
        "pairings": pairings,
        "n_pairings": n_assigned,
        "total_length_score": round(total_score, 4),
        "verdict": (
            f"Matcher v2: bipartite assignment of "
            f"{n_assigned}/{len(candidates)} candidates onto "
            f"{len(seals)} inscribed seals; total length-score = "
            f"{round(total_score, 4)}."
        ),
    }


# ── Bilingual readout test v2 (proper bipartite-assignment null) ─────


def _bilingual_readout_test_v2(inputs: dict, params: dict) -> dict:
    """Bipartite-assignment permutation test.

    Statistic
    ---------
    Compute a greedy bipartite assignment of names -> seals (each seal
    used at most once). Test statistic = sum of assigned length-scores.

    Null
    ----
    Permute the *seal index* assigned to each name, holding the
    multiset of name->seal pairings to {0,1,...,M-1} permutations. We
    pre-compute the score matrix S[name_i, seal_j], then sample N
    random one-to-one assignments (uniform over the symmetric group)
    and compute the assignment sum under each. The p-value is the
    fraction of samples whose assignment-sum >= observed.

    Why this null actually varies
    -----------------------------
    Unlike Phase-23c (which took max over the multiset and was
    permutation-invariant), the bipartite constraint forces each
    name to commit to a *specific* seal. Different permutations
    pair different names with the high-score seals, so the
    statistic genuinely changes.
    """
    persons_rows = inputs.get("rows_all") or inputs.get("rows_top50") or []
    seals = inputs.get("inscribed_seals") or []
    n_perms = max(100, _safe_int(params.get("n_permutations", 2000), 2000))
    min_name_freq = _safe_int(params.get("min_name_freq", 1), 1)
    tolerance = _safe_int(params.get("tolerance", 2), 2)
    seed = _safe_int(params.get("seed", 42), 42)

    candidates = [r for r in persons_rows
                   if _safe_int(r.get("occurrences")) >= min_name_freq]
    seal_lengths = [_safe_int(s.get("inscription_length")) for s in seals]
    if not candidates or not seal_lengths:
        return {
            "verdict": "INSUFFICIENT_DATA",
            "p_value": None,
            "n_candidates": len(candidates),
            "n_seals": len(seal_lengths),
        }

    n_names = len(candidates)
    n_seals = len(seal_lengths)

    # Pre-compute score matrix S[i, j]
    name_segs = [_name_n_segments(r["candidate_name"]) for r in candidates]
    score_mat = [
        [_length_score(seal_lengths[j], name_segs[i], tolerance)
         for j in range(n_seals)]
        for i in range(n_names)
    ]

    def _greedy_score(assignment: list[int]) -> float:
        """Score under the assignment[i] = seal_idx for name i.
        Negative seal_idx means unassigned."""
        return sum(score_mat[i][assignment[i]]
                   for i in range(n_names) if assignment[i] >= 0)

    # Observed: greedy bipartite assignment by occurrence
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

    observed = _greedy_score(obs_assignment)

    # Null: random one-to-one assignments. If n_names > n_seals, only
    # the first n_seals names get a seal in each shuffle (chosen
    # randomly to avoid ordering bias).
    rng = random.Random(seed)
    n_at_or_above = 0
    null_dist: list[float] = []
    for _ in range(n_perms):
        # Pick which names get assigned (random subset of size
        # min(n_names, n_seals))
        k = min(n_names, n_seals)
        shuffled_seal_idxs = list(range(n_seals))
        rng.shuffle(shuffled_seal_idxs)
        # Randomly select which k names participate
        if n_names > n_seals:
            participating = rng.sample(range(n_names), n_seals)
        else:
            participating = list(range(n_names))
        random_assignment = [-1] * n_names
        for slot, name_i in enumerate(participating):
            random_assignment[name_i] = shuffled_seal_idxs[slot]
        v = _greedy_score(random_assignment)
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

    obs_pairings = []
    for i, j in enumerate(obs_assignment):
        if j < 0:
            continue
        obs_pairings.append({
            "candidate_name": candidates[i]["candidate_name"],
            "name_n_segments": name_segs[i],
            "seal_idx": j,
            "seal_id": seals[j].get("catalogue_id"),
            "seal_n_signs": seal_lengths[j],
            "length_score": score_mat[i][j],
        })

    return {
        "verdict": verdict,
        "p_value": round(p_value, 6),
        "observed": round(observed, 4),
        "null_mean": round(null_mean, 4),
        "null_sd": round(null_sd, 4),
        "z_score": round(z, 4),
        "n_permutations": n_perms,
        "n_candidates": n_names,
        "n_seals": n_seals,
        "tolerance": tolerance,
        "observed_assignment": obs_pairings,
        "interpretation": (
            "Bipartite-assignment readout test: each candidate name "
            "committed to a unique seal. Null: random one-to-one "
            "name-to-seal pairings. A significant p-value would "
            "indicate the observed length-matching is unlikely under "
            "uniform random pairings."
        ),
    }


# ── Verdict aggregator ────────────────────────────────────────────────


def _phase24_verdict(inputs: dict, params: dict) -> dict:
    n_laursen = _safe_int(inputs.get("n_rows"))
    n_inscribed = _safe_int(inputs.get("n_inscribed"))
    n_xref = _safe_int(inputs.get("n_with_laursen_xref"))
    n_high_conf = _safe_int(inputs.get("n_high_conf"))
    n_persons = _safe_int(inputs.get("n_unique"))
    n_confirmed = len(inputs.get("confirmed_hits") or [])
    p_value = inputs.get("p_value")
    readout_verdict = inputs.get("readout_verdict") or ""

    summary = (
        f"Phase-24 progress: Laursen Table 1 = {n_laursen} rows "
        f"({n_inscribed} inscribed Gulf-INDUS); seals cross-referenced "
        f"with Laursen = {n_xref}; high-confidence Parpola-read seals "
        f"= {n_high_conf}; persons-v2 candidates = {n_persons} "
        f"({n_confirmed} historically-confirmed); readout-v2 p={p_value} "
        f"({readout_verdict})."
    )

    next_steps = [
        "Phase-25 priority 1: parse the remaining 19 Laursen Table 1 "
        "rows missed by the heuristic parser (likely 76-94, the "
        "newer Bahrain/Saar finds) by adding their site vocabulary.",
        "Phase-25 priority 2: cross-reference our 9 unmatched seals "
        "(Asmar, Lothal, Failaka KM 1113, Berlin VA 243, Konar Sandal, "
        "Jalalabad, Al-Maqsha, Shu-ilishu, Kish) with the broader "
        "non-Gulf-Type Indus seal corpus (Frenez 2018 Table II).",
        "Phase-25 priority 3: ingest CISI Vol 3 plates to lift "
        "remaining length_only confidence to high for all 11 inscribed "
        "seals.",
        "Phase-25 priority 4: phonetic readout test - score Janabiyah "
        "seal #10's 7-sign Parpola-read sequence against Sumerian/"
        "Akkadian PN candidates using the CISI Vol 1 phonetic-value "
        "proposals. First true bilingual decipherment attempt.",
    ]

    return {
        "summary": summary,
        "n_laursen_rows": n_laursen,
        "n_inscribed_gulf_indus": n_inscribed,
        "n_seals_xref": n_xref,
        "n_high_conf": n_high_conf,
        "n_persons": n_persons,
        "n_confirmed_persons": n_confirmed,
        "readout_p_value": p_value,
        "readout_verdict": readout_verdict,
        "next_steps": next_steps,
        "verdict": (
            "READOUT_SIGNIFICANT" if isinstance(p_value, (int, float))
            and p_value < 0.05 else
            "READOUT_NOT_SIGNIFICANT"
            if p_value is not None else
            "INSUFFICIENT_DATA"
        ),
    }


# ── Atomic node defs for registration ─────────────────────────────────


def _phase24_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "LaursenTable1Loader", "Laursen 2010 Table 1 Loader (Phase-24)",
            "Phase-24 / Sources",
            "Load the parsed Laursen 2010 Table 1 (canonical 121-row "
            "Gulf-Type seal catalogue) plus the Parpola-1994b sign-by-"
            "sign readings from Laursen footnote 2 (currently only "
            "seal #10 = Janabiyah Cemetery).",
            inputs=[],
            outputs=[
                {"name": "rows", "type": "json"},
                {"name": "n_rows", "type": "number"},
                {"name": "parpola_readings", "type": "json"},
                {"name": "n_parpola_readings", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_laursen_table1_loader,
        ),
        AtomicNodeDef(
            "RefinedSealLoaderV2",
            "Refined Seal + Persons Loader v2 (Phase-24)",
            "Phase-24 / Sources",
            "Load the Phase-24 augmented seal inventory (with Laursen "
            "cross-references + Janabiyah seal #10) + persons-v2 "
            "(toponym-filtered, extended stoplist, wider window) + "
            "Laursen Table 1 + Parpola readings.",
            inputs=[],
            outputs=[
                {"name": "all_seals", "type": "json"},
                {"name": "inscribed_seals", "type": "json"},
                {"name": "n_seals_total", "type": "number"},
                {"name": "n_seals_inscribed", "type": "number"},
                {"name": "sign_metadata", "type": "json"},
                {"name": "upgrade_metadata", "type": "json"},
                {"name": "persons_v2", "type": "json"},
                {"name": "n_persons_v2", "type": "number"},
                {"name": "laursen_rows", "type": "json"},
                {"name": "n_laursen_rows", "type": "number"},
                {"name": "parpola_readings", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_refined_seal_loader_v2,
        ),
        AtomicNodeDef(
            "LaursenTable1Auditor", "Laursen Table 1 Auditor (Phase-24)",
            "Phase-24 / Reporters",
            "Audit the parsed Laursen Table 1: count inscribed vs "
            "non-inscribed Gulf-Type seals, distribution by site and "
            "type, and the count of seals with full Parpola readings.",
            inputs=[
                {"name": "rows", "type": "json", "required": True},
                {"name": "parpola_readings", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "n_rows", "type": "number"},
                {"name": "n_inscribed", "type": "number"},
                {"name": "n_parpola_readings", "type": "number"},
                {"name": "by_gulf_type", "type": "json"},
                {"name": "by_site_top10", "type": "json"},
                {"name": "sample_rows", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_laursen_table1_auditor,
        ),
        AtomicNodeDef(
            "SealSignUpgradeAuditor",
            "Seal Sign Upgrade Auditor (Phase-24)",
            "Phase-24 / Reporters",
            "Audit the Phase-24 sign-ID upgrade: which seals were "
            "cross-referenced with Laursen Table 1, the Janabiyah "
            "addition, and the confidence-tier distribution.",
            inputs=[
                {"name": "all_seals", "type": "json", "required": True},
                {"name": "upgrade_metadata", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "n_seals", "type": "number"},
                {"name": "n_with_laursen_xref", "type": "number"},
                {"name": "n_high_conf", "type": "number"},
                {"name": "total_signs", "type": "number"},
                {"name": "by_confidence", "type": "json"},
                {"name": "upgrade_rows", "type": "json"},
                {"name": "metadata_summary", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_seal_sign_upgrade_auditor,
        ),
        AtomicNodeDef(
            "RefinedMeluhhanPersonsExtractorV2",
            "Refined Meluhhan Persons Extractor v2 (Phase-24)",
            "Phase-24 / Reporters",
            "Aggregate the Phase-24 persons-v2 output: strict Sumerian-"
            "PN regex + toponym filter (e2-/bad3-/iri-/kur- prefixes) "
            "+ extended Akkadian-modal stoplist + widened tablet "
            "extraction window.",
            inputs=[
                {"name": "persons_v2", "type": "json", "required": True},
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
            fn=_refined_persons_extractor_v2,
        ),
        AtomicNodeDef(
            "EnhancedNameMatcherV2",
            "Enhanced Name Matcher v2 (Phase-24, bipartite)",
            "Phase-24 / Decipherment",
            "Bipartite-assignment matcher: each candidate name commits "
            "to exactly one seal (greedy by length match). Resolves "
            "the multiset-invariance flaw of the Phase-23c matcher.",
            inputs=[
                {"name": "rows_all", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_candidates", "type": "number"},
                {"name": "n_seals", "type": "number"},
                {"name": "n_assigned", "type": "number"},
                {"name": "n_unassigned", "type": "number"},
                {"name": "pairings", "type": "json"},
                {"name": "n_pairings", "type": "number"},
                {"name": "total_length_score", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_name_freq": {"type": "integer", "default": 1, "minimum": 1},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0},
                },
            },
            fn=_enhanced_name_matcher_v2,
        ),
        AtomicNodeDef(
            "BilingualReadoutTestV2",
            "Bilingual Readout Test v2 (Phase-24, bipartite)",
            "Phase-24 / Decipherment",
            "Permutation test on the bipartite-assignment statistic. "
            "Null: random one-to-one name<->seal assignments. Unlike "
            "Phase-23c, this null genuinely varies because each seal "
            "is used at most once.",
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
                {"name": "observed_assignment", "type": "json"},
                {"name": "interpretation", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 2000,
                                        "minimum": 100},
                    "min_name_freq": {"type": "integer", "default": 1, "minimum": 1},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0},
                    "seed": {"type": "integer", "default": 42},
                },
            },
            fn=_bilingual_readout_test_v2,
        ),
        AtomicNodeDef(
            "Phase24Verdict", "Phase-24 Verdict Aggregator",
            "Phase-24 / Reporters",
            "Aggregate the Phase-24 sub-experiment outputs into a "
            "contact-zone decipherment-progress verdict + Phase-25 "
            "priority list.",
            inputs=[
                {"name": "n_rows", "type": "number", "required": False},
                {"name": "n_inscribed", "type": "number", "required": False},
                {"name": "n_with_laursen_xref", "type": "number", "required": False},
                {"name": "n_high_conf", "type": "number", "required": False},
                {"name": "n_unique", "type": "number", "required": False},
                {"name": "confirmed_hits", "type": "json", "required": False},
                {"name": "p_value", "type": "number", "required": False},
                {"name": "readout_verdict", "type": "text", "required": False},
            ],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "n_laursen_rows", "type": "number"},
                {"name": "n_inscribed_gulf_indus", "type": "number"},
                {"name": "n_seals_xref", "type": "number"},
                {"name": "n_high_conf", "type": "number"},
                {"name": "n_persons", "type": "number"},
                {"name": "n_confirmed_persons", "type": "number"},
                {"name": "readout_p_value", "type": "number"},
                {"name": "readout_verdict", "type": "text"},
                {"name": "next_steps", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase24_verdict,
        ),
    ]


__all__ = [
    "_laursen_table1_loader",
    "_refined_seal_loader_v2",
    "_laursen_table1_auditor",
    "_seal_sign_upgrade_auditor",
    "_refined_persons_extractor_v2",
    "_enhanced_name_matcher_v2",
    "_bilingual_readout_test_v2",
    "_phase24_verdict",
    "_phase24_node_defs",
]
