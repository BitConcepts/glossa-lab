"""Phase-21 atomic node implementations.

Three Phase-21 candidate experiments derived from the Phase-20 synthesis
(`reports/phase20_synthesis.md`). All implemented as graph atomic nodes
per WARP.md rule G1.

  Experiment 1 — Repetition-aware corpus segmentation (Phase-21a)
      RepetitionCollapser collapses runs of the same sign into a single
      occurrence (e.g. ``A B B B C`` → ``A B C``), producing a
      "de-numerified" corpus. Output stratifications ``{"original":
      sequences, "collapsed": collapsed_sequences}`` reuse the
      BinSpectralFingerprint input format so the existing Phase-20
      spectral node can re-measure the gap on both. Tests Phase-20
      finding 4 + Phase-19 finding 1 (the corpus's anomalous spectral
      gap is dominated by repetition-block tokens; collapsing them
      should recover a more language-like regime).

  Experiment 2 — Site-stratified hypothesis projection (Phase-21b)
      SiteStratifier groups M77 inscriptions by Mahadevan site_code
      prefix (first two digits → site group: 100000 = Mohenjo-daro,
      200000 = Harappa, 310000 = Lothal, 510000 = Banawali/Rakhigarhi,
      etc.). Output stratifications use the same shape as
      LengthStratifier so BinSpectralFingerprint and other downstream
      stratification consumers can be re-used. Tests Phase-20 finding 2
      (the 16-sign cluster's per-site enrichment) at the level of full
      structural fingerprints.

  Experiment 3 — Numerical-weight regression (Phase-21d)
      NumericalWeightAnalyzer identifies signs flagged NUMERICAL by
      Phase-20d's Fuls classifier and computes per-sign repetition-
      block-length statistics conditioned on archaeological covariates
      (site group, inscription length bin). For each numerical sign,
      reports mean / std / counts of repetition-block lengths and a
      simple Poisson-style coefficient of variation (CV) check for
      whether the block-length distribution is consistent with a
      counting/quantity-marking system (CV ~ 1) vs. a syntactic role
      (CV << 1).

  Phase21Verdict aggregates the three sub-experiment outputs into a
  single yes/no/maybe verdict per Phase-20 follow-up question.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any

# ── Helpers ────────────────────────────────────────────────────────────


def _flatten(seqs: list[list[str]]) -> list[str]:
    return [s for seq in seqs for s in seq]


def _site_prefix2(site_code: str) -> str:
    """Mahadevan site-code grouping: keep the first 2 digits, pad the
    rest with zeros (matches Phase-20's ClusterArchaeology helper).
    """
    sc = str(site_code or "")
    return (sc[:2] + "0000") if len(sc) >= 2 else sc


# ── Experiment 1: Repetition collapser ─────────────────────────────────


def _repetition_collapser(inputs: dict, params: dict) -> dict:
    """Collapse runs of identical consecutive signs.

    A "run" is two or more occurrences of the same sign back-to-back.
    Collapsing replaces ``A B B B C D D`` with ``A B C D`` (keep one
    representative of each run). For each input inscription we also
    record the sequence of repetition-block lengths
    (``[1, 3, 1, 2]`` for the example) so downstream nodes can analyse
    the discarded "count" information.

    Output ``stratifications`` is a dict matching the BinSpectralFingerprint
    input shape:

        {
          "original":  [list of original sequences],
          "collapsed": [list of collapsed sequences],
        }

    Output also includes ``collapsed_inscriptions`` (per-inscription
    metadata + collapsed sequence + block lengths) and corpus-level
    ``collapse_stats``.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    inscriptions: list[dict] = inputs.get("inscriptions") or []
    min_run = max(2, int(params.get("min_run", 2)))

    collapsed_sequences: list[list[str]] = []
    collapsed_inscriptions: list[dict] = []
    n_runs_collapsed = 0
    n_tokens_dropped = 0
    n_tokens_in = 0

    # If we don't have inscription metadata, build a simple stub.
    if not inscriptions:
        inscriptions = [
            {"id": None, "site_code": "", "length": len(s), "sequence": s}
            for s in sequences
        ]
    elif not sequences:
        sequences = [list(ins.get("sequence") or []) for ins in inscriptions]

    for ins, seq in zip(inscriptions, sequences):
        n_tokens_in += len(seq)
        if not seq:
            collapsed_sequences.append([])
            collapsed_inscriptions.append({**ins, "collapsed_sequence": [],
                                            "repetition_blocks": []})
            continue
        # Run-length encode
        rle: list[tuple[str, int]] = []
        cur = seq[0]
        cur_n = 1
        for s in seq[1:]:
            if s == cur:
                cur_n += 1
            else:
                rle.append((cur, cur_n))
                cur = s
                cur_n = 1
        rle.append((cur, cur_n))

        # Count collapses
        for _, ln in rle:
            if ln >= min_run:
                n_runs_collapsed += 1
                n_tokens_dropped += (ln - 1)

        collapsed = [tok for tok, _ in rle]
        block_lengths = [ln for _, ln in rle]
        collapsed_sequences.append(collapsed)
        collapsed_inscriptions.append({
            **{k: ins.get(k) for k in ("id", "site_code", "length")},
            "sequence": list(seq),
            "collapsed_sequence": collapsed,
            "repetition_blocks": block_lengths,
        })

    flat_orig = _flatten(sequences)
    flat_coll = _flatten(collapsed_sequences)

    stratifications = {
        "original": list(sequences),
        "collapsed": collapsed_sequences,
    }

    # Stats
    share_kept = (len(flat_coll) / max(1, len(flat_orig))) if flat_orig else 0.0
    collapse_stats = {
        "min_run": min_run,
        "n_inscriptions": len(sequences),
        "n_tokens_in": len(flat_orig),
        "n_tokens_out": len(flat_coll),
        "n_tokens_dropped": n_tokens_dropped,
        "n_runs_collapsed": n_runs_collapsed,
        "share_kept": round(share_kept, 4),
        "n_distinct_signs_in": len(set(flat_orig)),
        "n_distinct_signs_out": len(set(flat_coll)),
        "verdict": (
            f"Collapsed {n_runs_collapsed} runs of >= {min_run} same-sign "
            f"repetitions, dropping {n_tokens_dropped} of {len(flat_orig)} "
            f"tokens ({(1 - share_kept) * 100:.1f}% reduction). "
            f"Distinct signs unchanged ({len(set(flat_orig))} → "
            f"{len(set(flat_coll))})."
        ),
    }

    return {
        "stratifications": stratifications,
        "collapsed_sequences": collapsed_sequences,
        "collapsed_inscriptions": collapsed_inscriptions,
        "n_runs_collapsed": n_runs_collapsed,
        "n_tokens_dropped": n_tokens_dropped,
        "share_kept": collapse_stats["share_kept"],
        "collapse_stats": collapse_stats,
    }


# ── Experiment 2: Site stratifier ──────────────────────────────────────


def _site_stratifier(inputs: dict, params: dict) -> dict:
    """Group inscriptions by Mahadevan site_code prefix.

    Each inscription gets a ``site_label`` from its first 2 site_code
    digits (e.g. site_code="105432" → "100000"). Optional ``min_inscriptions``
    filters out site groups smaller than the cutoff (those are merged into
    a residual ``"other"`` bucket).

    Output ``stratifications`` matches the LengthStratifier shape so
    downstream nodes (BinSpectralFingerprint, AllographDetector,
    FulsPositionalClassifier) can re-use it.
    """
    inscriptions: list[dict] = inputs.get("inscriptions") or []
    min_inscriptions = max(1, int(params.get("min_inscriptions", 30)))
    top_n = int(params.get("top_n", 0))  # 0 = no limit
    custom_labels: dict[str, str] = params.get("site_labels") or {
        "100000": "Mohenjo-daro",
        "200000": "Harappa",
        "210000": "Chanhu-daro/Other",
        "310000": "Lothal",
        "400000": "Kalibangan",
        "510000": "Banawali/Rakhigarhi",
    }

    by_prefix: dict[str, list[dict]] = defaultdict(list)
    for ins in inscriptions:
        sc = str(ins.get("site_code") or "")
        prefix = _site_prefix2(sc)
        by_prefix[prefix].append(ins)

    counts = [(p, len(g)) for p, g in by_prefix.items()]
    counts.sort(key=lambda kv: -kv[1])
    if top_n > 0:
        keep_set = {p for p, _ in counts[:top_n]}
    else:
        keep_set = {p for p, c in counts if c >= min_inscriptions}

    stratifications: dict[str, list[list[str]]] = {}
    inscription_strata: dict[str, list[dict]] = {}
    summary: list[dict] = []
    other_seqs: list[list[str]] = []
    other_ins: list[dict] = []

    for prefix, group in by_prefix.items():
        seqs = [list(g.get("sequence") or []) for g in group]
        if prefix not in keep_set:
            other_seqs.extend(seqs)
            other_ins.extend(group)
            continue
        label = custom_labels.get(prefix, prefix)
        stratifications[label] = seqs
        inscription_strata[label] = list(group)
        flat = _flatten(seqs)
        summary.append({
            "site_label": label,
            "site_prefix": prefix,
            "n_inscriptions": len(seqs),
            "n_tokens": len(flat),
            "n_distinct_signs": len(set(flat)),
            "mean_length": round(sum(len(s) for s in seqs) / max(1, len(seqs)), 2),
        })

    if other_seqs:
        stratifications["Other"] = other_seqs
        inscription_strata["Other"] = other_ins
        flat = _flatten(other_seqs)
        summary.append({
            "site_label": "Other",
            "site_prefix": "other",
            "n_inscriptions": len(other_seqs),
            "n_tokens": len(flat),
            "n_distinct_signs": len(set(flat)),
            "mean_length": round(sum(len(s) for s in other_seqs) / max(1, len(other_seqs)), 2),
        })

    summary.sort(key=lambda r: -r["n_inscriptions"])
    return {
        "stratifications": stratifications,
        "inscription_strata": inscription_strata,
        "summary": summary,
        "n_groups": len(stratifications),
        "min_inscriptions": min_inscriptions,
        "total_sequences": sum(len(v) for v in stratifications.values()),
    }


# ── Experiment 2: Per-stratum verdict (compact view of stratified spectrum) ─


def _per_stratum_summary(inputs: dict, params: dict) -> dict:
    """Compactly summarise a per-bin spectral fingerprint output.

    Useful as a Phase-21 reporter on top of BinSpectralFingerprint when
    the upstream stratifier was SiteStratifier rather than LengthStratifier
    (so the verdict text mentions sites, not lengths).
    """
    per_bin = inputs.get("per_bin") or {}
    if not isinstance(per_bin, dict) or not per_bin:
        return {"verdict": "no per-bin data", "rows": []}

    rows: list[dict] = []
    for label, d in per_bin.items():
        rows.append({
            "stratum": label,
            "n_seqs": d.get("n_seqs"),
            "n_tokens": d.get("n_tokens"),
            "spectral_gap": d.get("spectral_gap"),
            "verdict": d.get("verdict"),
        })
    rows.sort(key=lambda r: -(r.get("n_tokens") or 0))

    nontrivial = [(r["stratum"], r["spectral_gap"]) for r in rows
                  if isinstance(r.get("spectral_gap"), (int, float))]
    if nontrivial:
        max_s, max_gap = max(nontrivial, key=lambda kv: kv[1])
        min_s, min_gap = min(nontrivial, key=lambda kv: kv[1])
        spread = max_gap - min_gap
        differs = spread >= 0.10
        verdict = (
            f"Spectral gap range across strata: "
            f"{min_gap:.4f} ({min_s}) → {max_gap:.4f} ({max_s}), "
            f"spread = {spread:.4f}. "
            f"{'Strata DIFFER materially.' if differs else 'Strata behave similarly.'}"
        )
    else:
        verdict = "no spectral data"

    return {
        "rows": rows,
        "verdict": verdict,
        "n_strata": len(rows),
    }


# ── Experiment 3: Numerical-weight analyzer ────────────────────────────


def _numerical_weight_analyzer(inputs: dict, params: dict) -> dict:
    """Repetition-block-length analysis for high-repetition signs.

    Inputs:
      inscriptions  -- M77InscriptionLoader output (must include
                        site_code + sequence per inscription).
      table         -- optional FulsPositionalClassifier per-sign table
                        (used to filter to NUMERICAL signs).

    Params:
      rep_rate_min     -- minimum repetition rate to consider (default 0.40)
      min_block_count  -- minimum number of repetition blocks per sign
                          to compute statistics (default 5)
      length_bins      -- inscription-length bins for cross-tabulation;
                          default [[1,4],[5,8],[9,9999]]

    For each qualifying sign, we collect every repetition-block length
    (i.e. consecutive run length) observed across the corpus, then
    cross-tabulate by site group and inscription-length bin. We report
    mean, std, max block lengths plus a coefficient of variation (CV)
    to characterise the block-length distribution. CV ~ 1 is the
    Poisson regime (consistent with a counting / quantity system);
    CV << 0.5 is more like a stylistic / syntactic doubling.
    """
    inscriptions: list[dict] = inputs.get("inscriptions") or []
    fuls_table: list[dict] = inputs.get("table") or []
    rep_rate_min = float(params.get("rep_rate_min", 0.40))
    min_block_count = int(params.get("min_block_count", 5))
    length_bins = params.get("length_bins") or [[1, 4], [5, 8], [9, 9999]]

    # Determine candidate signs
    candidate_signs: set[str] = set()
    if isinstance(fuls_table, list) and fuls_table:
        for row in fuls_table:
            if not isinstance(row, dict):
                continue
            cls = row.get("class")
            rr = float(row.get("repetition_rate") or 0.0)
            if cls == "NUMERICAL" and rr >= rep_rate_min:
                candidate_signs.add(str(row.get("sign")))
    if not candidate_signs:
        # Fall back: count repetition rates from inscriptions directly
        rep_counts: Counter[str] = Counter()
        rep_total: Counter[str] = Counter()
        for ins in inscriptions:
            seq = ins.get("sequence") or []
            for i in range(len(seq) - 1):
                rep_total[seq[i]] += 1
                if seq[i + 1] == seq[i]:
                    rep_counts[seq[i]] += 1
        for s, tot in rep_total.items():
            if tot > 0 and (rep_counts[s] / tot) >= rep_rate_min:
                candidate_signs.add(s)

    # Collect block lengths per sign with covariates
    block_lengths_by_sign: dict[str, list[int]] = defaultdict(list)
    block_lengths_by_sign_site: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(list)
    )
    block_lengths_by_sign_lenbin: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(list)
    )

    def _len_bin(L: int) -> str:
        for pair in length_bins:
            try:
                lo, hi = int(pair[0]), int(pair[1])
            except Exception:  # noqa: BLE001
                continue
            if lo <= L <= hi:
                return f"L{lo}-{hi}" if hi < 1000 else f"L{lo}+"
        return "Lother"

    for ins in inscriptions:
        seq = ins.get("sequence") or []
        if not seq:
            continue
        L = int(ins.get("length") or len(seq))
        lbin = _len_bin(L)
        site = _site_prefix2(str(ins.get("site_code") or ""))
        # RLE
        cur = seq[0]
        cur_n = 1
        for s in seq[1:]:
            if s == cur:
                cur_n += 1
            else:
                if cur in candidate_signs and cur_n >= 2:
                    block_lengths_by_sign[cur].append(cur_n)
                    block_lengths_by_sign_site[cur][site].append(cur_n)
                    block_lengths_by_sign_lenbin[cur][lbin].append(cur_n)
                cur = s
                cur_n = 1
        if cur in candidate_signs and cur_n >= 2:
            block_lengths_by_sign[cur].append(cur_n)
            block_lengths_by_sign_site[cur][site].append(cur_n)
            block_lengths_by_sign_lenbin[cur][lbin].append(cur_n)

    rows: list[dict] = []
    for sign, lengths in block_lengths_by_sign.items():
        n = len(lengths)
        if n < min_block_count:
            continue
        m = sum(lengths) / n
        var = sum((l - m) ** 2 for l in lengths) / n
        sd = math.sqrt(var)
        cv = sd / m if m > 0 else 0.0
        site_breakdown = {
            site: {
                "n": len(ls),
                "mean": round(sum(ls) / max(1, len(ls)), 3),
                "max": max(ls) if ls else 0,
            }
            for site, ls in block_lengths_by_sign_site[sign].items()
        }
        lenbin_breakdown = {
            lb: {
                "n": len(ls),
                "mean": round(sum(ls) / max(1, len(ls)), 3),
                "max": max(ls) if ls else 0,
            }
            for lb, ls in block_lengths_by_sign_lenbin[sign].items()
        }
        regime = (
            "poisson_count" if 0.5 <= cv <= 1.5
            else "low_variance_doubling" if cv < 0.5
            else "high_variance_count"
        )
        rows.append({
            "sign": sign,
            "n_blocks": n,
            "mean_block_length": round(m, 3),
            "std_block_length": round(sd, 3),
            "max_block_length": max(lengths),
            "coefficient_of_variation": round(cv, 3),
            "regime": regime,
            "by_site": site_breakdown,
            "by_length_bin": lenbin_breakdown,
        })

    rows.sort(key=lambda r: -r["n_blocks"])
    n_poisson = sum(1 for r in rows if r["regime"] == "poisson_count")
    n_low_var = sum(1 for r in rows if r["regime"] == "low_variance_doubling")
    n_high_var = sum(1 for r in rows if r["regime"] == "high_variance_count")

    if not rows:
        verdict = (
            "PREDICTION 4 (numerical-weight regression) UNABLE TO RUN: "
            "no NUMERICAL candidate signs with >= "
            f"{min_block_count} repetition blocks."
        )
    else:
        dom = max(("poisson_count", n_poisson),
                  ("low_variance_doubling", n_low_var),
                  ("high_variance_count", n_high_var),
                  key=lambda kv: kv[1])
        verdict = (
            f"Analysed {len(rows)} numerical signs (rep_rate >= "
            f"{rep_rate_min}). "
            f"Block-length CV regime distribution: poisson_count={n_poisson}, "
            f"low_variance_doubling={n_low_var}, "
            f"high_variance_count={n_high_var}. "
            f"Dominant regime: {dom[0]} ({dom[1]} signs). "
            + (
                "CONFIRMED: most numerical signs behave as Poisson-style "
                "counts → quantity-marking is the most likely function."
                if dom[0] == "poisson_count" and dom[1] >= max(1, len(rows) // 2)
                else
                "PARTIAL: numerical regime mix is not Poisson-dominant; "
                "stylistic / mantric repetition cannot be ruled out."
            )
        )

    return {
        "n_signs_analysed": len(rows),
        "n_poisson_regime": n_poisson,
        "n_low_variance_doubling": n_low_var,
        "n_high_variance_count": n_high_var,
        "rows": rows,
        "params": {
            "rep_rate_min": rep_rate_min,
            "min_block_count": min_block_count,
            "length_bins": length_bins,
        },
        "verdict": verdict,
    }


# ── Phase-21 verdict aggregator ────────────────────────────────────────


def _phase21_verdict(inputs: dict, params: dict) -> dict:
    """Aggregate Phase-21 sub-experiment verdicts.

    Inputs (all optional — missing → UNKNOWN):
      repetition_spectral   -- BinSpectralFingerprint output for
                                {"original","collapsed"} stratification.
      site_spectral         -- BinSpectralFingerprint output for
                                site stratification.
      site_summary          -- _per_stratum_summary output for the site
                                spectral run (used for richer text).
      numerical_weights     -- _numerical_weight_analyzer output.
    """

    def _extract_per_bin(v: Any) -> dict[str, dict]:
        """Accept either a full BinSpectralFingerprint output ({per_bin: {...}})
        or a bare per-bin dict (when wired directly via sourcePort='per_bin')."""
        if not isinstance(v, dict) or not v:
            return {}
        if "per_bin" in v and isinstance(v["per_bin"], dict):
            return v["per_bin"]
        # Bare per-bin dict: each value is a dict with spectral_gap / verdict.
        sample_vals = [val for val in v.values() if isinstance(val, dict)]
        if sample_vals and any("spectral_gap" in val for val in sample_vals):
            return v
        return {}

    rep_pb = _extract_per_bin(inputs.get("repetition_spectral"))
    site_pb = _extract_per_bin(inputs.get("site_spectral"))
    # site_summary may be the full _per_stratum_summary dict or just the verdict text.
    raw_site_sum = inputs.get("site_summary")
    if isinstance(raw_site_sum, dict):
        site_sum = raw_site_sum
    elif isinstance(raw_site_sum, str):
        site_sum = {"verdict": raw_site_sum}
    else:
        site_sum = {}
    # numerical_weights: prefer full dict, but synthesise from scalar fields if needed.
    raw_nw = inputs.get("numerical_weights")
    if isinstance(raw_nw, dict):
        nw = raw_nw
    else:
        nw_rows = inputs.get("nw_rows")
        rows_list = nw_rows if isinstance(nw_rows, list) else []
        n_poisson_v = inputs.get("nw_n_poisson")
        if rows_list:
            nw = {"rows": rows_list,
                  "n_poisson_regime": int(n_poisson_v or 0)}
        else:
            nw = {}

    # P21-1: did the spectral gap rise after repetition collapse?
    orig_gap = rep_pb.get("original", {}).get("spectral_gap")
    coll_gap = rep_pb.get("collapsed", {}).get("spectral_gap")
    if isinstance(orig_gap, (int, float)) and isinstance(coll_gap, (int, float)):
        if coll_gap >= max(0.10, 5 * max(orig_gap, 1e-6)):
            p1 = "CONFIRMED"
            p1_detail = (
                f"spectral gap rose from {orig_gap:.4f} (original) to "
                f"{coll_gap:.4f} (collapsed). De-numerification recovers "
                "natural-language structure."
            )
        elif coll_gap > orig_gap + 1e-3:
            p1 = "PARTIALLY CONFIRMED"
            p1_detail = (
                f"spectral gap rose from {orig_gap:.4f} → {coll_gap:.4f} "
                "but did not reach a natural-language regime (>= 0.40)."
            )
        else:
            p1 = "NOT CONFIRMED"
            p1_detail = (
                f"spectral gap unchanged at {orig_gap:.4f} → {coll_gap:.4f}; "
                "repetition is not the dominant source of the anomaly."
            )
    else:
        p1 = "UNKNOWN"
        p1_detail = "missing repetition-spectral data."

    # P21-2: do site groups differ structurally?
    if site_pb:
        gaps = [d.get("spectral_gap") for d in site_pb.values()
                if isinstance(d.get("spectral_gap"), (int, float))]
        if gaps:
            spread = max(gaps) - min(gaps)
            if spread >= 0.10:
                p2 = "CONFIRMED"
            elif spread >= 0.02:
                p2 = "PARTIALLY CONFIRMED"
            else:
                p2 = "NOT CONFIRMED"
            p2_detail = (
                f"spectral gap spread across {len(gaps)} site groups = "
                f"{spread:.4f}; "
                f"text from site_summary: "
                f"{site_sum.get('verdict', '')}"
            )
        else:
            p2 = "UNKNOWN"
            p2_detail = "no spectral data per site stratum."
    else:
        p2 = "UNKNOWN"
        p2_detail = "missing site-spectral data."

    # P21-4: numerical weight regime
    if nw and "rows" in nw:
        rows = nw.get("rows") or []
        n_poisson = nw.get("n_poisson_regime", 0)
        n_total = len(rows)
        if n_total == 0:
            p4 = "UNKNOWN"
            p4_detail = "no numerical signs analysed."
        elif n_poisson >= max(1, n_total // 2):
            p4 = "CONFIRMED"
            p4_detail = (
                f"{n_poisson}/{n_total} numerical signs in poisson_count "
                "regime — quantity-marking is the most likely function."
            )
        else:
            p4 = "PARTIALLY CONFIRMED"
            p4_detail = (
                f"only {n_poisson}/{n_total} signs in poisson_count "
                "regime; mixed numerical / stylistic behaviour."
            )
    else:
        p4 = "UNKNOWN"
        p4_detail = "missing numerical-weight regression."

    summary = (
        f"Phase-21: P21a={p1} | P21b={p2} | P21d={p4}"
    )

    return {
        "summary": summary,
        "predictions": {
            "p21a_repetition_recovers_naturallanguage": {
                "verdict": p1, "detail": p1_detail,
                "original_gap": orig_gap, "collapsed_gap": coll_gap,
            },
            "p21b_site_strata_differ": {
                "verdict": p2, "detail": p2_detail,
            },
            "p21d_numerical_weights_poisson": {
                "verdict": p4, "detail": p4_detail,
            },
        },
    }


# ── Atomic node defs for registration ──────────────────────────────────


def _phase21_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "RepetitionCollapser", "Repetition Collapser (Phase-21)",
            "Phase-21 / Transforms",
            "Collapse runs of identical consecutive signs into a single "
            "occurrence (e.g. 'A B B B C' → 'A B C'). Outputs both the "
            "original and collapsed corpus as a stratifications dict that "
            "BinSpectralFingerprint can consume directly. Tests Phase-20 "
            "finding 4 (de-numerify the corpus and recheck spectral gap).",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": False},
                {"name": "inscriptions", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "stratifications", "type": "json"},
                {"name": "collapsed_sequences", "type": "sequences"},
                {"name": "collapsed_inscriptions", "type": "json"},
                {"name": "n_runs_collapsed", "type": "number"},
                {"name": "n_tokens_dropped", "type": "number"},
                {"name": "share_kept", "type": "number"},
                {"name": "collapse_stats", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_run": {"type": "integer", "default": 2, "minimum": 2,
                                 "description": "Minimum consecutive same-sign run to collapse."},
                },
            },
            fn=_repetition_collapser,
        ),
        AtomicNodeDef(
            "SiteStratifier", "Site Stratifier (Phase-21)",
            "Phase-21 / Transforms",
            "Group inscriptions by Mahadevan site_code prefix (first two "
            "digits, e.g. 100000 = Mohenjo-daro, 200000 = Harappa, "
            "510000 = Banawali/Rakhigarhi). Output stratifications match "
            "the LengthStratifier shape so BinSpectralFingerprint and "
            "AllographDetector can be composed against site groups.",
            inputs=[
                {"name": "inscriptions", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "stratifications", "type": "json"},
                {"name": "inscription_strata", "type": "json"},
                {"name": "summary", "type": "json"},
                {"name": "n_groups", "type": "number"},
                {"name": "total_sequences", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_inscriptions": {"type": "integer", "default": 30, "minimum": 1,
                                          "description": "Site groups smaller than this go into the 'Other' bucket."},
                    "top_n": {"type": "integer", "default": 0,
                              "description": "0 = no limit; if > 0, keep only the N largest site groups."},
                    "site_labels": {"type": "object", "default": {},
                                     "description": "Optional prefix→human-label map."},
                },
            },
            fn=_site_stratifier,
        ),
        AtomicNodeDef(
            "PerStratumSummary", "Per-Stratum Summary (Phase-21)",
            "Phase-21 / Reporters",
            "Compactly summarise a BinSpectralFingerprint output as a list "
            "of {stratum, n_seqs, n_tokens, spectral_gap, verdict} rows "
            "with a corpus-level verdict on whether strata differ.",
            inputs=[
                {"name": "per_bin", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "rows", "type": "json"},
                {"name": "verdict", "type": "text"},
                {"name": "n_strata", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_per_stratum_summary,
        ),
        AtomicNodeDef(
            "NumericalWeightAnalyzer", "Numerical Weight Analyzer (Phase-21)",
            "Phase-21 / Numerical",
            "For NUMERICAL-classed M77 signs, collect repetition-block "
            "lengths conditioned on site group and inscription-length bin. "
            "Reports mean / std / CV per sign and classifies each sign's "
            "block-length distribution as poisson_count, "
            "low_variance_doubling, or high_variance_count.",
            inputs=[
                {"name": "inscriptions", "type": "json", "required": True},
                {"name": "table", "type": "json", "required": False,
                 "description": "FulsPositionalClassifier per-sign table."},
            ],
            outputs=[
                {"name": "n_signs_analysed", "type": "number"},
                {"name": "n_poisson_regime", "type": "number"},
                {"name": "n_low_variance_doubling", "type": "number"},
                {"name": "n_high_variance_count", "type": "number"},
                {"name": "rows", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "rep_rate_min": {"type": "number", "default": 0.40,
                                       "description": "Minimum repetition rate for sign inclusion."},
                    "min_block_count": {"type": "integer", "default": 5, "minimum": 1},
                    "length_bins": {"type": "array", "default": [[1, 4], [5, 8], [9, 9999]]},
                },
            },
            fn=_numerical_weight_analyzer,
        ),
        AtomicNodeDef(
            "Phase21Verdict", "Phase-21 Verdict Aggregator",
            "Phase-21 / Reporters",
            "Aggregate Phase-21 sub-experiment outputs (repetition spectral, "
            "site spectral + summary, numerical-weight regression) into a "
            "single yes / partially / no / unknown verdict per Phase-21 "
            "prediction (P21a, P21b, P21d).",
            inputs=[
                {"name": "repetition_spectral", "type": "json", "required": False},
                {"name": "site_spectral", "type": "json", "required": False},
                {"name": "site_summary", "type": "json", "required": False},
                {"name": "numerical_weights", "type": "json", "required": False},
                {"name": "nw_rows", "type": "json", "required": False,
                 "description": "NumericalWeightAnalyzer rows (alternative to numerical_weights)."},
                {"name": "nw_n_poisson", "type": "number", "required": False,
                 "description": "NumericalWeightAnalyzer n_poisson_regime count."},
            ],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "predictions", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase21_verdict,
        ),
    ]


__all__ = [
    "_repetition_collapser",
    "_site_stratifier",
    "_per_stratum_summary",
    "_numerical_weight_analyzer",
    "_phase21_verdict",
    "_phase21_node_defs",
]
