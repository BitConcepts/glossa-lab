"""Phase-131 (spec 022) — source-of-disagreement
attribution: pure machinery.

Ledger-sequence Phase-131 (2026-10-09). Implements the
frozen protocol of specs/022-phase131-attribution/spec.md:
a mechanism attribution of Phase-125's observed
disagreement (median TV 0.636931 over the 16 PRIMARY
judgeable pairs). This module NEVER re-scores Phase-125
and issues no verdict: Phase-125's FAIL — DISAGREEMENT
is final and spec 020's NO stands untouched (spec 022
section 0). Its outputs are join counts, alignments,
stratified TVs, and descriptive attribution shares
only.

Arms (spec sections 3-6):
  (A) Matched-object alignment — object identity is
      established ONLY by inscription content in the
      shared M-sign space (the Phase-116 matcher route):
      Holdat's cisi_number is internal sequential
      numbering, not a CISI object ID (spec 019 section
      2.1), so no key join exists. Eligible mayig
      inscriptions (every token mapped by the Phase-125
      PRIMARY crosswalk map) are matched to Holdat
      inscriptions in tiers EXACT / EXACT-REV / NEAR
      (mutual best similarity >= 0.60), aligned by
      unit-cost Levenshtein (tie-break diagonal >
      deletion > insertion), and every difference block
      is classified substitution / segmentation split /
      segmentation merge / insertion-deletion.
  (B) Reading direction — the Phase-125 primary
      statistic recomputed with mayig (B1) or Holdat
      (B2) sequences reversed; an arm supports direction
      iff its median TV <= 0.131316 (the Phase-127
      matched-size noise band's upper bound).
      Attribution diagnostics only, never a re-score.
  (C) Stratification — TV within site / object-type /
      text-length strata (period NOT ESTIMABLE: no
      period metadata exists on either side) plus a
      length-composition adjustment reweighting Holdat
      profiles to the mayig length composition.
  (D) Synthesis — per-mechanism supported shares under
      the frozen estimators of spec section 6; rows
      whose inputs are not estimable are marked
      NOT ESTIMABLE; shares are never rescaled to sum
      to 100%.

Profiles / TV reuse phase113_battery and
phase125_cross_compilation conventions exactly, via
phase127_diagnostic.evaluate_pairs_on_contexts where
applicable. No corpus data is hardcoded (H16): every
input arrives from the caller (phase131_run). This
phase has no stochastic procedure (spec A5).
"""
from __future__ import annotations

from collections import Counter

from glossa_lab.phase113_battery import CorpusContext
from glossa_lab.phase125_cross_compilation import (
    FLOOR, median, profiles_from_context,
)
from glossa_lab.phase113_battery import tv_distance

# ── Frozen constants (spec 022 sections 2-6) ──────────────
OBSERVED_MEDIAN_TV = 0.636931   # Phase-125 results of record
NOISE_BAND_MEDIAN = 0.082613    # Phase-127 arm (b) of record
NOISE_BAND_LO = 0.046665        # Phase-127 noise band lower bound
NOISE_BAND_HI = 0.131316        # Phase-127 noise band upper bound
DIRECTION_SUPPORT_MAX = NOISE_BAND_HI  # spec section 4 criterion
NEAR_SIMILARITY_MIN = 0.60      # Tier NEAR threshold (spec 3.2)
MIN_MATCHED = 10                # Arm A estimability gate (spec 3.4)
MIN_STRATUM_PAIRS = 4           # Arm C estimability gate (spec 5)
MATCHED_TV_MIN_PAIRS = 4        # defined-TV pairs needed (spec 3.4)
LENGTH_BINS = ("1", "2-3", "4-5", "6+")

CLS_IDENTICAL = "identical"
CLS_ORDER_ONLY = "order-only"
CLS_SPLIT = "segmentation_split"
CLS_MERGE = "segmentation_merge"
CLS_SUBSTITUTION = "substitution"
CLS_INDEL = "insertion-deletion"


def _round(x):
    return round(x, 6) if x is not None else None


def primary_map(rows) -> dict[str, str]:
    """The Phase-125 PRIMARY arm pair set as a function
    P -> M (286 unambiguous high-confidence pairs),
    built by the Phase-125 machinery itself."""
    from glossa_lab.phase125_cross_compilation import build_arms
    arms = build_arms(rows)
    return {r["parpola_id"]: r["mahadevan_id"] for r in arms["primary"]}


def mapped_sequence(tokens, pmap: dict[str, str]):
    """Token-wise image of a mayig sequence under the
    primary map, or None if any token is unmapped
    (spec 3.2 eligibility: all-or-nothing)."""
    out = []
    for t in tokens:
        m = pmap.get(t)
        if m is None:
            return None
        out.append(m)
    return out


# ── Levenshtein alignment (spec section 3.3) ──────────────

def levenshtein(a, b) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1,
                         prev[j - 1] + (0 if ca == cb else 1))
        prev = cur
    return prev[len(b)]


def similarity(a, b) -> float:
    if not a and not b:
        return 1.0
    return 1.0 - levenshtein(a, b) / max(len(a), len(b))


def align(a, b) -> list[dict]:
    """Optimal unit-cost alignment as columns
    {op, a, b} with op in match/sub/del/ins. Frozen
    tie-break at each backtrace step: diagonal over
    deletion (a-token unaligned) over insertion."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1,
                           dp[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1]
                                               else 1))
    cols = []
    i, j = n, m
    while i > 0 or j > 0:
        if (i > 0 and j > 0
                and dp[i][j] == dp[i - 1][j - 1]
                + (0 if a[i - 1] == b[j - 1] else 1)):
            cols.append({"op": "match" if a[i - 1] == b[j - 1] else "sub",
                         "a": a[i - 1], "b": b[j - 1]})
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            cols.append({"op": "del", "a": a[i - 1], "b": None})
            i -= 1
        else:
            cols.append({"op": "ins", "a": None, "b": b[j - 1]})
            j -= 1
    cols.reverse()
    return cols


def difference_blocks(cols) -> list[dict]:
    """Maximal runs of non-match columns, classified per
    spec 3.3 by their (p, q) shape."""
    blocks = []
    cur = []

    def flush():
        if not cur:
            return
        p = sum(1 for c in cur if c["a"] is not None)
        q = sum(1 for c in cur if c["b"] is not None)
        if p == q and p >= 1:
            cls = CLS_SUBSTITUTION
        elif p == 1 and q == 2:
            cls = CLS_SPLIT
        elif p == 2 and q == 1:
            cls = CLS_MERGE
        else:
            cls = CLS_INDEL
        blocks.append({
            "class": cls, "p": p, "q": q, "n_tokens": p + q,
            "a_tokens": [c["a"] for c in cur if c["a"] is not None],
            "b_tokens": [c["b"] for c in cur if c["b"] is not None],
        })
        cur.clear()

    for c in cols:
        if c["op"] == "match":
            flush()
        else:
            cur.append(c)
    flush()
    return blocks


def classify_pair(a, b, blocks) -> str:
    """Exactly one pair class, by the frozen priority:
    identical > order-only > first difference block."""
    if list(a) == list(b):
        return CLS_IDENTICAL
    if Counter(a) == Counter(b):
        return CLS_ORDER_ONLY
    return blocks[0]["class"] if blocks else CLS_IDENTICAL


# ── Arm A matcher (spec section 3.2) ──────────────────────

def match_objects(eligible, holdat_seqs) -> dict:
    """eligible: list of {id, mapped} (mapped M-space
    sequences). holdat_seqs: list of {key, tokens}.
    Returns tier assignments + counts. Identity is
    textual, not artifactual (spec A3)."""
    n_h = len(holdat_seqs)
    # similarity matrices, forward and reversed
    sims_f = [[similarity(e["mapped"], h["tokens"]) for h in holdat_seqs]
              for e in eligible]
    sims_r = [[similarity(e["mapped"], h["tokens"][::-1])
               for h in holdat_seqs] for e in eligible]

    def exact_pairs(sims):
        out = {}
        for i, row in enumerate(sims):
            for j in range(n_h):
                if row[j] == 1.0:
                    out.setdefault(i, []).append(j)
        return out

    fwd_exact = exact_pairs(sims_f)
    rev_exact = exact_pairs(sims_r)

    def mutual_unique(pairs_by_i):
        rev_count = Counter(j for js in pairs_by_i.values() for j in js)
        return {i: js[0] for i, js in pairs_by_i.items()
                if len(js) == 1 and rev_count[js[0]] == 1}

    fwd_uq = mutual_unique(fwd_exact)
    rev_uq = mutual_unique(rev_exact)

    matched = {}   # eligible idx -> (holdat idx, tier)
    ambiguous_orientation = []
    for i in range(len(eligible)):
        f = fwd_uq.get(i)
        r = rev_uq.get(i)
        if f is not None and r is not None and f == r:
            ambiguous_orientation.append(i)
        elif f is not None:
            matched[i] = (f, "EXACT")
        elif r is not None:
            matched[i] = (r, "EXACT-REV")

    # NEAR: unique mutual best at >= threshold, excluding
    # matched. A tie for best on either side disqualifies
    # the pairing (no arbitrary first-pick).
    def unique_best_j(row, banned):
        best, bestv, tie = None, -1.0, False
        for j, v in enumerate(row):
            if j in banned:
                continue
            if v > bestv:
                best, bestv, tie = j, v, False
            elif v == bestv:
                tie = True
        return (None, bestv) if tie else (best, bestv)

    used_h = {j for j, _t in matched.values()}
    for i in range(len(eligible)):
        if i in matched:
            continue
        jf, vf = unique_best_j(sims_f[i], used_h)
        jr, vr = unique_best_j(sims_r[i], used_h)
        fwd_ok = jf is not None and vf >= NEAR_SIMILARITY_MIN
        rev_ok = jr is not None and vr >= NEAR_SIMILARITY_MIN
        unmatched = [k for k in range(len(eligible)) if k not in matched]
        if fwd_ok:
            col = [sims_f[k][jf] for k in unmatched]
            top = max(col)
            if col.count(top) != 1 or unmatched[col.index(top)] != i:
                fwd_ok = False
        if rev_ok:
            col = [sims_r[k][jr] for k in unmatched]
            top = max(col)
            if col.count(top) != 1 or unmatched[col.index(top)] != i:
                rev_ok = False
        if fwd_ok and rev_ok and jf == jr:
            ambiguous_orientation.append(i)
        elif fwd_ok:
            matched[i] = (jf, "NEAR")
            used_h.add(jf)
        elif rev_ok:
            matched[i] = (jr, "NEAR-REV")
            used_h.add(jr)

    pairs = []
    for i, (j, tier) in sorted(matched.items()):
        a = list(eligible[i]["mapped"])
        b_raw = list(holdat_seqs[j]["tokens"])
        b = b_raw[::-1] if tier.endswith("REV") else b_raw
        cols = align(a, b)
        blocks = difference_blocks(cols)
        pairs.append({
            "mayig_object_id": eligible[i]["id"],
            "holdat_key": holdat_seqs[j]["key"],
            "tier": tier,
            "similarity": _round(similarity(a, b)),
            "mapped_mayig_sequence": a,
            "holdat_sequence": b_raw,
            "aligned_holdat_sequence": b,
            "alignment": cols,
            "blocks": blocks,
            "pair_class": classify_pair(a, b, blocks),
        })
    tier_counts = Counter(p["tier"] for p in pairs)
    return {
        "pairs": pairs,
        "n_eligible": len(eligible),
        "n_matched": len(pairs),
        "tier_counts": dict(sorted(tier_counts.items())),
        "n_ambiguous_orientation": len(ambiguous_orientation),
        "ambiguous_orientation_eligible_ids":
            [eligible[i]["id"] for i in ambiguous_orientation],
    }


def matched_object_tv(mayig_ins, holdat_ins, pairs16) -> dict:
    """Spec 3.4: profiles of the fixed 16 pairs on the
    matched inscriptions only; estimability gates."""
    from glossa_lab.phase127_diagnostic import evaluate_pairs_on_contexts
    ev = evaluate_pairs_on_contexts(pairs16, CorpusContext(mayig_ins),
                                    CorpusContext(holdat_ins), floor=1)
    defined = [r for r in ev["records"] if r["tv"] is not None]
    return {"records": ev["records"], "n_defined": len(defined),
            "median_tv_defined": ev["median_tv"]}


def matched_tv_gate(n_matched: int, n_defined: int) -> bool:
    return n_matched >= MIN_MATCHED and n_defined >= MATCHED_TV_MIN_PAIRS


# ── Arm B: reversed-context TV (spec section 4) ───────────

def reversed_median_tv(mayig_ins, holdat_ins, pairs16, reverse_side: str):
    """Median TV over the fixed 16 pairs with one side's
    inscriptions reversed. Counts are reversal-invariant,
    so the judgeable set is the Phase-125 set (asserted
    by the caller against the unreversed evaluation)."""
    from glossa_lab.phase127_diagnostic import evaluate_pairs_on_contexts
    may = [list(reversed(x)) for x in mayig_ins] \
        if reverse_side == "mayig" else mayig_ins
    hol = [list(reversed(x)) for x in holdat_ins] \
        if reverse_side == "holdat" else holdat_ins
    ev = evaluate_pairs_on_contexts(pairs16, CorpusContext(may),
                                    CorpusContext(hol), floor=FLOOR)
    return ev


def direction_supports(median_tv) -> bool:
    return median_tv is not None and median_tv <= DIRECTION_SUPPORT_MAX


# ── Arm C: stratification + adjustment (spec section 5) ──

def length_bin(n: int) -> str:
    if n <= 1:
        return "1"
    if n <= 3:
        return "2-3"
    if n <= 5:
        return "4-5"
    return "6+"


def stratum_tv(mayig_ins, holdat_ins, pairs16) -> dict:
    """Median TV within one stratum, floor 8 re-applied
    on both sides inside the stratum; estimability per
    spec 5.1 (MIN_STRATUM_PAIRS judgeable)."""
    from glossa_lab.phase127_diagnostic import evaluate_pairs_on_contexts
    ev = evaluate_pairs_on_contexts(pairs16, CorpusContext(mayig_ins),
                                    CorpusContext(holdat_ins), floor=FLOOR)
    estimable = ev["n_judgeable"] >= MIN_STRATUM_PAIRS
    return {
        "n_mayig_inscriptions": len(mayig_ins),
        "n_holdat_inscriptions": len(holdat_ins),
        "n_mayig_tokens": sum(len(x) for x in mayig_ins),
        "n_holdat_tokens": sum(len(x) for x in holdat_ins),
        "n_judgeable": ev["n_judgeable"],
        "median_tv": ev["median_tv"] if estimable else None,
        "median_tv_unthresholded": ev["median_tv"],
        "estimable": estimable,
        "status": "ESTIMABLE" if estimable else "NOT ESTIMABLE",
        "records": ev["records"],
    }


def adjusted_profiles(mayig_ins, holdat_ins, pairs16) -> dict:
    """Spec 5.2: per-sign Holdat profile reweighted to
    the mayig length-bin composition, with per-pair
    coverage; adjusted median TV over the fixed pairs."""
    may_bins = Counter(length_bin(len(x)) for x in mayig_ins)
    n_may = len(mayig_ins)
    weights = {b: may_bins.get(b, 0) / n_may for b in LENGTH_BINS}
    bin_ctx = {}
    for b in LENGTH_BINS:
        sel = [x for x in holdat_ins if length_bin(len(x)) == b]
        bin_ctx[b] = CorpusContext(sel)
    may_ctx = CorpusContext(mayig_ins)
    records = []
    tvs = []
    for pair in pairs16:
        p_prof, p_n = profiles_from_context(may_ctx, pair["parpola_id"])
        used = []
        acc = [0.0, 0.0, 0.0]
        wsum = 0.0
        for b in LENGTH_BINS:
            if weights[b] == 0:
                continue
            prof_b, n_b = profiles_from_context(bin_ctx[b],
                                                pair["mahadevan_id"])
            if prof_b is None or n_b == 0:
                continue
            used.append(b)
            wsum += weights[b]
            for k in range(3):
                acc[k] += weights[b] * prof_b[k]
        adj = None
        if wsum > 0:
            adj = tuple(v / wsum for v in acc)
        included = (p_prof is not None and p_n >= FLOOR and adj is not None)
        tv = (round(tv_distance(p_prof, adj), 6) if included else None)
        if included:
            tvs.append(tv)
        records.append({
            "parpola_id": pair["parpola_id"],
            "mahadevan_id": pair["mahadevan_id"],
            "mayig_n": p_n,
            "mayig_profile": ([round(x, 6) for x in p_prof]
                              if p_prof else None),
            "adjusted_holdat_profile": ([round(x, 6) for x in adj]
                                        if adj else None),
            "coverage": _round(wsum),
            "bins_used": used,
            "included": included,
            "tv": tv,
        })
    estimable = len(tvs) >= MIN_STRATUM_PAIRS
    return {
        "weights_mayig_length_bins": {b: _round(weights[b])
                                      for b in LENGTH_BINS},
        "records": records,
        "n_included": len(tvs),
        "median_tv": _round(median(tvs)) if (tvs and estimable) else None,
        "median_tv_unthresholded": _round(median(tvs)) if tvs else None,
        "estimable": estimable,
        "status": "ESTIMABLE" if estimable else "NOT ESTIMABLE",
    }


# ── Arm D: synthesis (spec section 6) ─────────────────────

def _share(num, den):
    if den is None or den == 0:
        return None
    return round(min(1.0, max(0.0, num / den)), 6)


def synthesis(matched, arm_b, arm_c_adjusted, matched_tv=None) -> dict:
    """matched: match_objects() output (+ computed block
    tallies attached by caller under 'block_token_totals').
    arm_b: {'b1_median_tv':…, 'b2_median_tv':…}.
    arm_c_adjusted: adjusted_profiles() output."""
    rows = {}
    totals = matched.get("block_token_totals") or {}
    total_diff_tokens = totals.get("all_difference_blocks", 0)
    a_estimable = (matched["n_matched"] >= MIN_MATCHED
                   and total_diff_tokens > 0)

    def a_share(key):
        if not a_estimable:
            return None
        return _share(totals.get(key, 0), total_diff_tokens)

    seg_tokens = totals.get(CLS_SPLIT, 0) + totals.get(CLS_MERGE, 0)
    rows["segmentation"] = {
        "share": (_share(seg_tokens, total_diff_tokens)
                  if a_estimable else None),
        "status": "ESTIMABLE" if a_estimable else "NOT ESTIMABLE",
        "basis": "Arm A difference-block tokens over the MATCHED set",
        "estimator": "(split + merge block tokens) / all difference-"
                     "block tokens",
    }
    rows["substitution"] = {
        "share": a_share(CLS_SUBSTITUTION),
        "status": "ESTIMABLE" if a_estimable else "NOT ESTIMABLE",
        "basis": "Arm A difference-block tokens over the MATCHED set",
        "estimator": "substitution block tokens / all difference-"
                     "block tokens",
    }
    rows["insertion_deletion"] = {
        "share": a_share(CLS_INDEL),
        "status": "ESTIMABLE" if a_estimable else "NOT ESTIMABLE",
        "basis": "Arm A difference-block tokens over the MATCHED set",
        "estimator": "indel block tokens / all difference-block tokens",
    }
    b1, b2 = arm_b.get("b1_median_tv"), arm_b.get("b2_median_tv")
    best = None
    best_arm = None
    for name, v in (("B1_mayig_reversed", b1), ("B2_holdat_reversed", b2)):
        if direction_supports(v) and (best is None or v < best):
            best, best_arm = v, name
    if best is not None:
        d_share = _share(OBSERVED_MEDIAN_TV - best, OBSERVED_MEDIAN_TV)
    else:
        d_share = 0.0
    rows["order_direction"] = {
        "share": d_share,
        "status": "ESTIMABLE",
        "basis": "Arm B median-TV scale vs Phase-125 observed median TV",
        "estimator": "(0.636931 - min supporting reversed median TV) / "
                     "0.636931, clipped [0,1]; 0.000 credited if neither "
                     "arm meets the section-4 support criterion",
        "supporting_arm": best_arm,
        "b1_median_tv": b1, "b2_median_tv": b2,
        "b1_reduction": (_round(OBSERVED_MEDIAN_TV - b1)
                         if b1 is not None else None),
        "b2_reduction": (_round(OBSERVED_MEDIAN_TV - b2)
                         if b2 is not None else None),
    }
    adj = arm_c_adjusted.get("median_tv")
    if arm_c_adjusted.get("estimable") and adj is not None:
        c_share = _share(OBSERVED_MEDIAN_TV - adj, OBSERVED_MEDIAN_TV)
        c_status = "ESTIMABLE"
    else:
        c_share, c_status = None, "NOT ESTIMABLE"
    rows["composition"] = {
        "share": c_share,
        "status": c_status,
        "basis": "Arm C length-composition-adjusted median TV",
        "estimator": "(0.636931 - adjusted median TV) / 0.636931, "
                     "clipped [0,1]",
        "adjusted_median_tv": adj,
    }
    mtv = (matched_tv or {}).get("median_tv")
    mtv_estimable = bool((matched_tv or {}).get("estimable"))
    rows["matched_object_residual"] = {
        "share": (_share(mtv, OBSERVED_MEDIAN_TV)
                  if (mtv_estimable and mtv is not None) else None),
        "status": "ESTIMABLE" if (mtv_estimable and mtv is not None)
                  else "NOT ESTIMABLE",
        "basis": "Arm A matched-object median TV (persistence measure, "
                 "not an explained share)",
        "estimator": "matched-object median TV / 0.636931",
        "matched_object_median_tv": mtv if mtv_estimable else None,
    }
    explained = sum(r["share"] for r in rows.values()
                    if r["share"] is not None
                    and r is not rows["matched_object_residual"])
    residual = round(max(0.0, 1.0 - explained), 6)
    return {
        "rows": rows,
        "sum_credited_shares": round(explained, 6),
        "residual_unexplained_share": residual,
        "overlap_note": "Order/direction and composition shares both "
                        "act on the median-TV scale and may overlap; "
                        "Arm A shares act on matched-pair token "
                        "differences, a different denominator. Shares "
                        "are not forced to sum to 100%; if credited "
                        "shares exceed 1 the residual is 0 and the "
                        "overlap is stated, never rescaled away.",
    }


def block_token_totals(pairs) -> dict:
    """Token tallies by block class across matched pairs."""
    totals = Counter()
    for p in pairs:
        for blk in p["blocks"]:
            totals[blk["class"]] += blk["n_tokens"]
            totals["all_difference_blocks"] += blk["n_tokens"]
    return dict(totals)
