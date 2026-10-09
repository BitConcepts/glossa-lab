"""Phase-131 (spec 022) — orchestration: load the frozen
inputs -> assert totals + anchors hash -> Arm A join
stages + content matcher -> Arm B direction -> Arm C
stratification + adjustment -> Arm D synthesis -> reports.

Executes the frozen protocol of
specs/022-phase131-attribution/spec.md. This phase is
attribution diagnostics ONLY: it does NOT re-score
Phase-125, issues no verdict, and changes no anchor,
PRED, or status. The Phase-125 verdict (FAIL —
DISAGREEMENT) is final and spec 020's NO stands
untouched. Object identity between Holdat and mayig is
established only by inscription content in the shared
M-sign space: Holdat's cisi_number is internal
sequential numbering, not a CISI object ID (spec 019
section 2.1), and no key join is performed anywhere in
this phase. Profiles are computed strictly within each
compilation; inscriptions are never pooled. Holdat data
is read from the gitignored downloads area and never
committed; only statistics, counts, and the spec 3.3
matched-example sequences are published. The anchors
file is never opened for writing; its sha256 is asserted
identical before and after.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_BACKEND = _REPO / "backend"
sys.path.insert(0, str(_BACKEND))

from glossa_lab.data import mayig_layer as ml  # noqa: E402
from glossa_lab.data import (  # noqa: E402
    parpola_mahadevan_crosswalk_v1 as xw,
)
from glossa_lab.phase113_battery import CorpusContext  # noqa: E402
from glossa_lab.phase113_run import _gpu_device  # noqa: E402
from glossa_lab.phase125_run import (  # noqa: E402
    ANCHORS_PATH, ANCHORS_SHA256, HOLDAT_EXPECTED, MAYIG_EXPECTED,
    _find_holdat_csv, _sha256, load_holdat_inscriptions,
)
from glossa_lab.phase131_attribution import (  # noqa: E402
    NOISE_BAND_HI, NOISE_BAND_LO, NOISE_BAND_MEDIAN,
    OBSERVED_MEDIAN_TV, adjusted_profiles, block_token_totals,
    direction_supports, length_bin, mapped_sequence, match_objects,
    matched_object_tv, matched_tv_gate, primary_map,
    reversed_median_tv, stratum_tv, synthesis,
)

RESULTS_PATH = _REPO / "reports" / "phase131_attribution_results.json"
REPORT_PATH = _REPO / "reports" / "phase131_attribution.md"
PHASE125_RESULTS = _REPO / "reports" / "phase125_cross_compilation_results.json"
PHASE127_RESULTS = _REPO / "reports" / "phase127_cross_compilation_diagnostic_results.json"
SPEC = "specs/022-phase131-attribution"
DATE = "2026-10-09"


def load_holdat_keyed(csv_path: Path) -> list[dict]:
    """Holdat inscriptions with their (internal) key and
    per-inscription stratum values, grouped exactly as
    the Phase-125 loader groups (cisi_number + position).
    Each record: {key, tokens, sites: set, iconographies: set}."""
    seals: dict[str, list] = {}
    strata: dict[str, dict[str, set]] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals:
                seals[c] = []
                strata[c] = {"site": set(), "iconography": set()}
            while len(seals[c]) <= p:
                seals[c].append("")
            seals[c][p] = s
            if (row.get("site") or "").strip():
                strata[c]["site"].add(row["site"].strip())
            if (row.get("iconography") or "").strip():
                strata[c]["iconography"].add(row["iconography"].strip())
    out = []
    for c, toks in seals.items():
        tokens = [t for t in toks if t]
        if tokens:
            out.append({"key": c, "tokens": tokens,
                        "sites": strata[c]["site"],
                        "iconographies": strata[c]["iconography"]})
    return out


def _fmt(x, nd=6):
    return "null" if x is None else f"{x:.{nd}f}"


def run_all(write: bool = True) -> dict:
    anchors_before = _sha256(ANCHORS_PATH)
    assert anchors_before == ANCHORS_SHA256, anchors_before

    # ── Frozen inputs (spec 022 section 2) ──
    mayig_records = ml.load_inscriptions()
    mayig_inscriptions = [list(r["tokens"]) for r in mayig_records]
    mayig_ctx = CorpusContext(mayig_inscriptions)
    assert len(mayig_inscriptions) == MAYIG_EXPECTED["inscriptions"]
    assert mayig_ctx.n_tokens == MAYIG_EXPECTED["tokens"]
    assert len(mayig_ctx.token_counts) == MAYIG_EXPECTED["signs"]

    holdat_csv = _find_holdat_csv()
    holdat_inscriptions = load_holdat_inscriptions(holdat_csv)
    holdat_ctx = CorpusContext(holdat_inscriptions)
    assert len(holdat_inscriptions) == HOLDAT_EXPECTED["inscriptions"]
    assert holdat_ctx.n_tokens == HOLDAT_EXPECTED["tokens"]
    assert len(holdat_ctx.token_counts) == HOLDAT_EXPECTED["signs"]

    keyed = load_holdat_keyed(holdat_csv)
    assert [r["tokens"] for r in keyed] == holdat_inscriptions
    n_site_inconsistent = sum(1 for r in keyed if len(r["sites"]) != 1)
    n_icon_inconsistent = sum(
        1 for r in keyed if len(r["iconographies"]) != 1)

    rows = xw.load_crosswalk()
    assert xw.crosswalk_stats()["n_pairs"] == 762
    pmap = primary_map(rows)
    assert len(pmap) == 286, len(pmap)

    # ── Fixed judgeable set + noise band (of record) ──
    p125 = json.loads(PHASE125_RESULTS.read_text(encoding="utf-8"))
    primary_records = p125["arms"]["primary"]["records"]
    judged = [r for r in primary_records if r["judgeable"]]
    assert len(judged) == 16, len(judged)
    assert p125["arms"]["primary"]["stats"]["median_tv"] == OBSERVED_MEDIAN_TV
    assert p125["verdict"]["verdict"] == "FAIL"
    pairs = [{"parpola_id": r["parpola_id"],
              "mahadevan_id": r["mahadevan_id"]} for r in judged]

    p127 = json.loads(PHASE127_RESULTS.read_text(encoding="utf-8"))
    band = p127["arms"]["b_matched_size"]["median_tv_distribution"]
    assert band["median"] == NOISE_BAND_MEDIAN, band
    assert band["ci95_lo"] == NOISE_BAND_LO, band
    assert band["ci95_hi"] == NOISE_BAND_HI, band

    # ── Arm A: join stages (spec 3.1) ──
    holdat_keys = [r["key"] for r in keyed]
    holdat_m_ints = {int(k.split("-", 1)[1]) for k in holdat_keys
                     if k.startswith("M-")}
    mayig_ids = [r["cisi_object_id"] for r in mayig_records]
    apparent = sum(1 for oid in mayig_ids
                   if int(oid.split("-", 1)[1]) in holdat_m_ints)
    join_stages = {
        "mayig_objects": len(mayig_ids),
        "holdat_inscriptions": len(holdat_inscriptions),
        "s1_cisi_id": {
            "apparent_zero_padded_namesakes": apparent,
            "validated_matches": 0,
            "note": "REJECTED as non-identity: Holdat cisi_number is "
                    "internal sequential numbering, not a CISI object "
                    "ID (spec 019 section 2.1; spec 015 section 1). "
                    "No S1 join is performed.",
        },
        "s2_catalogue_cross_reference": {
            "usable_cross_references_found": 0,
            "note": "Searched the committed crosswalk v1 rows (fields: "
                    "parpola_id / mahadevan_id / confidence / sources; "
                    "no Holdat key field exists) and the mayig layer "
                    "metadata: no table mapping Holdat keys (cisi_number "
                    "/ seal_id / form) to CISI object IDs exists in the "
                    "committed inputs.",
        },
        "s3_shared_artifact_keys": {
            "shared_keys_found": 0,
            "note": "mayig keys (cisi_object_id / side_id / source_file) "
                    "and Holdat keys (cisi_number / seal_id / form) "
                    "share no field with the same meaning on both "
                    "sides; each side's non-CISI keys are internal.",
        },
    }
    assert not any("holdat" in k.lower() or "seal_id" in k.lower()
                   or "cisi_number" in k.lower() for k in rows[0])

    # ── Arm A: content matcher (spec 3.2) ──
    eligible = []
    n_mapped_tokens = 0
    for r in mayig_records:
        seq = mapped_sequence(r["tokens"], pmap)
        n_mapped_tokens += sum(1 for t in r["tokens"] if t in pmap)
        if seq is not None:
            eligible.append({"id": r["cisi_object_id"], "mapped": seq,
                             "tokens": list(r["tokens"])})
    coverage = round(n_mapped_tokens / mayig_ctx.n_tokens, 6)
    holdat_seqs = [{"key": r["key"], "tokens": r["tokens"]} for r in keyed]
    arm_a_match = match_objects(eligible, holdat_seqs)
    arm_a_match["block_token_totals"] = block_token_totals(
        arm_a_match["pairs"])
    pair_class_counts = Counter(p["pair_class"] for p in arm_a_match["pairs"])
    block_class_counts = Counter()
    for p in arm_a_match["pairs"]:
        for blk in p["blocks"]:
            block_class_counts[blk["class"]] += 1
    examples: dict[str, list] = {}
    for p in arm_a_match["pairs"]:
        if p["pair_class"] in ("identical",):
            continue
        examples.setdefault(p["pair_class"], [])
        if len(examples[p["pair_class"]]) < 3:
            examples[p["pair_class"]].append({
                "mayig_object_id": p["mayig_object_id"],
                "holdat_key": p["holdat_key"],
                "tier": p["tier"],
                "mapped_mayig_sequence": p["mapped_mayig_sequence"],
                "holdat_sequence": p["holdat_sequence"],
                "aligned_holdat_sequence": p["aligned_holdat_sequence"],
                "blocks": p["blocks"],
            })
    matched_ids = {p["mayig_object_id"] for p in arm_a_match["pairs"]}
    matched_hkeys = {p["holdat_key"] for p in arm_a_match["pairs"]}
    by_obj = {r["cisi_object_id"]: list(r["tokens"]) for r in mayig_records}
    by_key = {r["key"]: r["tokens"] for r in keyed}
    mtv_raw = matched_object_tv(
        [by_obj[i] for i in by_obj if i in matched_ids],
        [by_key[k] for k in by_key if k in matched_hkeys], pairs)
    mtv_estimable = matched_tv_gate(arm_a_match["n_matched"],
                                    mtv_raw["n_defined"])
    matched_tv = {
        "records": mtv_raw["records"],
        "n_defined": mtv_raw["n_defined"],
        "median_tv": (mtv_raw["median_tv_defined"] if mtv_estimable
                      else None),
        "median_tv_unthresholded": mtv_raw["median_tv_defined"],
        "estimable": mtv_estimable,
        "status": "ESTIMABLE" if mtv_estimable else "NOT ESTIMABLE",
        "gate": "requires MATCHED >= 10 pairs AND >= 4 of the 16 "
                "judgeable pairs with defined matched TVs (spec 3.4)",
    }
    arm_a = {
        "join_stages": join_stages,
        "matcher": {
            "n_eligible": arm_a_match["n_eligible"],
            "eligible_mayig_object_ids": [e["id"] for e in eligible],
            "primary_map_pairs": len(pmap),
            "primary_map_token_coverage_all_mayig": coverage,
            "n_matched": arm_a_match["n_matched"],
            "tier_counts": arm_a_match["tier_counts"],
            "n_ambiguous_orientation":
                arm_a_match["n_ambiguous_orientation"],
            "ambiguous_orientation_eligible_ids":
                arm_a_match["ambiguous_orientation_eligible_ids"],
            "matched_mayig_coverage": round(
                arm_a_match["n_matched"] / len(mayig_ids), 6),
            "matched_holdat_coverage": round(
                arm_a_match["n_matched"] / len(holdat_inscriptions), 6),
            "pairs": arm_a_match["pairs"],
        },
        "pair_class_counts": dict(sorted(pair_class_counts.items())),
        "block_class_counts": dict(sorted(block_class_counts.items())),
        "block_token_totals": arm_a_match["block_token_totals"],
        "examples_by_pair_class": examples,
        "matched_object_tv": matched_tv,
    }

    # ── Arm B: reading direction (spec section 4) ──
    base_ev = reversed_median_tv(mayig_inscriptions, holdat_inscriptions,
                                 pairs, "none")
    assert base_ev["n_judgeable"] == 16
    assert base_ev["median_tv"] == OBSERVED_MEDIAN_TV, base_ev["median_tv"]
    b1 = reversed_median_tv(mayig_inscriptions, holdat_inscriptions,
                            pairs, "mayig")
    b2 = reversed_median_tv(mayig_inscriptions, holdat_inscriptions,
                            pairs, "holdat")
    assert b1["n_judgeable"] == 16 and b2["n_judgeable"] == 16
    arm_b = {
        "criterion": "an arm supports direction as a mechanism iff its "
                     "median TV <= 0.131316 (Phase-127 matched-size "
                     "noise band upper bound; band median 0.082613, "
                     "95% interval [0.046665, 0.131316])",
        "framing": "Attribution diagnostics ONLY — not a re-score of "
                   "Phase-125; no Phase-125 gate is applied to any "
                   "Arm B number and the Phase-125 FAIL verdict stands "
                   "untouched (spec 022 section 0).",
        "b1_mayig_reversed": {
            "median_tv": b1["median_tv"],
            "reduction_vs_observed": round(
                OBSERVED_MEDIAN_TV - b1["median_tv"], 6),
            "supports_direction": direction_supports(b1["median_tv"]),
            "records": b1["records"],
        },
        "b2_holdat_reversed": {
            "median_tv": b2["median_tv"],
            "reduction_vs_observed": round(
                OBSERVED_MEDIAN_TV - b2["median_tv"], 6),
            "supports_direction": direction_supports(b2["median_tv"]),
            "records": b2["records"],
        },
    }

    # ── Arm C: stratification (spec 5.1) ──
    def site_of_mayig(_r):
        return "Mohenjo-daro"

    def variant_of(r):
        # "unicorn I seal" -> "unicorn I"
        return r["description"].rsplit(" seal", 1)[0]

    strata: dict[str, dict] = {"site": {}, "object_type": {},
                               "text_length": {}}
    holdat_sites = sorted({next(iter(r["sites"])) for r in keyed
                           if len(r["sites"]) == 1})
    for site in ["Mohenjo-daro"] + [s for s in holdat_sites
                                    if s != "Mohenjo-daro"]:
        m_ins = [list(r["tokens"]) for r in mayig_records
                 if site_of_mayig(r) == site]
        h_ins = [r["tokens"] for r in keyed if r["sites"] == {site}]
        strata["site"][site] = stratum_tv(m_ins, h_ins, pairs)
    holdat_icons = sorted({next(iter(r["iconographies"])) for r in keyed
                           if len(r["iconographies"]) == 1})
    variants = sorted({variant_of(r) for r in mayig_records})
    for var in variants:
        m_ins = [list(r["tokens"]) for r in mayig_records
                 if variant_of(r) == var]
        h_ins = [r["tokens"] for r in keyed
                 if r["iconographies"] == {"unicorn"}]
        strata["object_type"][var] = stratum_tv(m_ins, h_ins, pairs)
    for icon in [i for i in holdat_icons if i != "unicorn"]:
        strata["object_type"][f"holdat_only:{icon}"] = stratum_tv(
            [], [r["tokens"] for r in keyed
                 if r["iconographies"] == {icon}], pairs)
    for bname in ("1", "2-3", "4-5", "6+"):
        m_ins = [x for x in mayig_inscriptions
                 if length_bin(len(x)) == bname]
        h_ins = [x for x in holdat_inscriptions
                 if length_bin(len(x)) == bname]
        strata["text_length"][bname] = stratum_tv(m_ins, h_ins, pairs)

    adjusted = adjusted_profiles(mayig_inscriptions, holdat_inscriptions,
                                 pairs)
    arm_c = {
        "strata": strata,
        "n_site_inconsistent_inscriptions": n_site_inconsistent,
        "n_iconography_inconsistent_inscriptions": n_icon_inconsistent,
        "period": {
            "status": "NOT ESTIMABLE",
            "note": "Neither the mayig layer metadata nor the Holdat "
                    "CSV carries a period / dating field; no period "
                    "stratum is estimable in any cell and none is "
                    "improvised from a proxy (spec 5.1).",
        },
        "composition_adjustment": {
            "method": "Holdat per-sign profiles reweighted to the "
                      "mayig text-length-bin composition (spec 5.2). "
                      "Site adjustment is the site stratum itself "
                      "(mayig is entirely Mohenjo-daro) and object-type "
                      "adjustment is the unicorn stratum; neither is "
                      "double-counted here.",
            **adjusted,
        },
    }

    # ── Arm D: synthesis (spec section 6) ──
    arm_d = synthesis(
        arm_a_match,
        {"b1_median_tv": b1["median_tv"], "b2_median_tv": b2["median_tv"]},
        adjusted,
        matched_tv={"median_tv": matched_tv["median_tv"],
                    "estimable": mtv_estimable})

    results = {
        "phase": 131,
        "spec": SPEC,
        "date": DATE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gpu_device": _gpu_device(),
        "framing": "ATTRIBUTION DIAGNOSTICS ONLY. This phase does not "
                   "re-score Phase-125 and issues no verdict. The "
                   "Phase-125 verdict FAIL — DISAGREEMENT is FINAL and "
                   "unchanged; spec 020's NO stands untouched. No "
                   "anchor, PRED verdict, or status was modified.",
        "phase125_verdict_of_record": {
            "verdict": "FAIL", "substate": "DISAGREEMENT",
            "median_tv": OBSERVED_MEDIAN_TV, "n_judgeable": 16,
            "n_primary_pairs": 286, "status": "FINAL — unchanged",
        },
        "noise_band_of_record": {
            "source": "Phase-127 arm (b) matched-size subsampling null",
            "median": NOISE_BAND_MEDIAN, "ci95_lo": NOISE_BAND_LO,
            "ci95_hi": NOISE_BAND_HI,
        },
        "inputs": {
            "mayig_layer": {"inscriptions": 179, "tokens": 1003,
                            "signs": 182},
            "holdat": {"inscriptions": 1670, "tokens": 7002,
                       "signs": 390},
            "crosswalk": {"n_pairs": 762, "primary_map_pairs": len(pmap)},
            "judgeable_set": "the 16 Phase-125 PRIMARY judgeable pairs, "
                             "read from reports/"
                             "phase125_cross_compilation_results.json",
        },
        "arms": {
            "a_matched_object_alignment": arm_a,
            "b_reading_direction": arm_b,
            "c_stratification": arm_c,
            "d_synthesis": arm_d,
        },
        "anchors_sha256_before": anchors_before,
    }
    anchors_after = _sha256(ANCHORS_PATH)
    assert anchors_after == anchors_before
    results["anchors_sha256_after"] = anchors_after
    results["anchors_unchanged"] = anchors_after == anchors_before

    if write:
        RESULTS_PATH.write_text(
            json.dumps(results, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8")
        REPORT_PATH.write_text(_report(results), encoding="utf-8")
    return results


def _stratum_rows(strata: dict) -> str:
    out = []
    for name, s in strata.items():
        out.append(
            f"| {name} | {s['n_mayig_inscriptions']} | "
            f"{s['n_holdat_inscriptions']} | {s['n_judgeable']} | "
            f"{_fmt(s['median_tv'])} | {s['status']} |")
    return "\n".join(out)


def _report(r: dict) -> str:
    a = r["arms"]["a_matched_object_alignment"]
    b = r["arms"]["b_reading_direction"]
    c = r["arms"]["c_stratification"]
    d = r["arms"]["d_synthesis"]
    m = a["matcher"]
    mtv = a["matched_object_tv"]
    js = a["join_stages"]
    syn_rows = "\n".join(
        f"| {name} | {_fmt(row['share'])} | {row['status']} | "
        f"{row['basis']} |"
        for name, row in d["rows"].items())
    ex_lines = []
    for cls, exs in a["examples_by_pair_class"].items():
        for ex in exs:
            ex_lines.append(
                f"- **{cls}** — mayig {ex['mayig_object_id']} vs Holdat "
                f"{ex['holdat_key']} (tier {ex['tier']}): mapped mayig "
                f"`{' '.join(ex['mapped_mayig_sequence'])}` vs Holdat "
                f"`{' '.join(ex['holdat_sequence'])}`"
                + (f" (aligned reversed: "
                   f"`{' '.join(ex['aligned_holdat_sequence'])}`)"
                   if ex["tier"].endswith("REV") else "")
                + "; blocks: "
                + "; ".join(
                    f"{blk['class']} (a: {' '.join(blk['a_tokens']) or '∅'}"
                    f" → b: {' '.join(blk['b_tokens']) or '∅'})"
                    for blk in ex["blocks"]))
    examples_block = "\n".join(ex_lines) if ex_lines else (
        "No non-identical matched pairs exist to exemplify (see the "
        "pair-class counts above).")
    return f"""# Phase-131 — Source-of-Disagreement Attribution (spec 022)

**This study is attribution diagnostics ONLY. It does not
re-score Phase-125 and it issues no verdict.** **The Phase-125
verdict is FAIL — DISAGREEMENT, and it is FINAL** (spec 019,
PRIMARY arm: 16 judgeable pairs of 286; median TV 0.636931;
Spearman ρ initial −0.424758 / terminal 0.316034; shuffle null
p = 0.824). **Spec 020's adjudication outcome — NO — stands
untouched.** No finding below softens, qualifies, conditions,
or re-opens either outcome; no anchor, PRED verdict, or status
was changed by this phase. What follows attributes the
*observed disagreement* of that finished result to mechanisms —
segmentation, substitution, insertion/deletion, reading
direction, composition — under the estimators frozen in spec
022 before any Phase-131 statistic existed, and states the
residual unexplained share plainly. **Spec:** {SPEC} ·
**Date:** {DATE} · **GPU device:** {r['gpu_device']}

## Arm A — Matched-object alignment (spec §3)

### Join stages — all counted, as found

| Stage | Result |
|---|---|
| mayig objects / Holdat inscriptions | {js['mayig_objects']} / {js['holdat_inscriptions']} |
| S1 CISI-ID join: apparent zero-padded namesakes | {js['s1_cisi_id']['apparent_zero_padded_namesakes']} apparent / **0 validated** — REJECTED as non-identity: Holdat `cisi_number` is internal sequential numbering, not a CISI object ID (spec 019 §2.1). No S1 join was performed. |
| S2 catalogue cross-reference (Holdat key → CISI ID) | 0 usable cross-references found in the committed inputs |
| S3 shared artifact keys | 0 shared keys |
| S4 content matcher (§3.2): eligible mayig inscriptions | {m['n_eligible']} / 179 (every token mapped by the 286-pair primary crosswalk map; primary-map token coverage over all mayig tokens {_fmt(m['primary_map_token_coverage_all_mayig'])}) |
| S4 matched pairs | **{m['n_matched']}** (tiers: {m['tier_counts']}; ambiguous-orientation excluded: {m['n_ambiguous_orientation']}) |
| Matched coverage | mayig {_fmt(m['matched_mayig_coverage'])} · Holdat {_fmt(m['matched_holdat_coverage'])} |

Identity here is **textual, not artifactual** (spec A3): a
matched pair shows the same sign text occurs in both
compilations under the primary crosswalk map, within the
frozen matcher tolerance. The small matched set is a finding,
reported as found (spec A6): under the only legitimate join,
the two compilations' texts essentially do not coincide —
consistent with, and sharper than, Phase-125's profile-level
disagreement, and not a defect to paper over by loosening the
matcher.

### Difference classification (§3.3)

Pair-class counts over the matched set: {a['pair_class_counts']}.
Difference-block counts by class: {a['block_class_counts']}.
Block token totals: {a['block_token_totals']}.

Concrete examples per non-identical pair class (all pairs of a
class if fewer than 3 exist):

{examples_block}

### Matched-object positional TV (§3.4)

Matched-object median TV: **{mtv['status']}**
(defined per-pair TVs: {mtv['n_defined']} of the 16 judgeable
pairs; unthresholded median over defined pairs:
{_fmt(mtv['median_tv_unthresholded'])}; gate: {mtv['gate']}).
Per-pair records are in the results JSON.

## Arm B — Reading direction (spec §4)

**Attribution diagnostics, not a re-score of Phase-125.** No
Phase-125 gate is applied to any number in this section; the
Phase-125 FAIL verdict stands untouched. Criterion (frozen):
an arm supports direction as a mechanism iff its median TV ≤
0.131316 — the upper bound of the Phase-127 matched-size noise
band (median 0.082613, 95% interval [0.046665, 0.131316]).

| Arm | Median TV | Reduction vs 0.636931 | Supports direction? |
|---|---|---|---|
| B1 mayig reversed | {_fmt(b['b1_mayig_reversed']['median_tv'])} | {_fmt(b['b1_mayig_reversed']['reduction_vs_observed'])} | {b['b1_mayig_reversed']['supports_direction']} |
| B2 Holdat reversed | {_fmt(b['b2_holdat_reversed']['median_tv'])} | {_fmt(b['b2_holdat_reversed']['reduction_vs_observed'])} | {b['b2_holdat_reversed']['supports_direction']} |

Note, as found and as the algebra requires: B1 and B2 coincide
exactly, per pair and therefore in the median. Reversal swaps
the INITIAL and TERMINAL shares of one side's profiles, and TV
is symmetric in that swap — TV(p with I/T swapped, q) equals
TV(p, q with I/T swapped) — so the two arms cannot differ under
the Phase-125 statistic. Either way the answer is the same:
reversing one compilation's orientation reduces the median TV
only slightly, from 0.636931 to the value above, nowhere near
the noise band. Reading direction is **not** a supported
mechanism for the observed disagreement under the frozen
criterion.

## Arm C — Stratification + composition adjustment (spec §5)

A stratum's median TV is estimable iff ≥ 4 pairs are judgeable
within the stratum under floor 8 re-applied on both sides;
otherwise the row is marked NOT ESTIMABLE with its counts.
Stratum-inconsistent Holdat inscriptions (counted, excluded
from the affected stratum): site
{c['n_site_inconsistent_inscriptions']}, iconography
{c['n_iconography_inconsistent_inscriptions']}.

### Site

| Stratum | mayig inscr. | Holdat inscr. | Judgeable | Median TV | Status |
|---|---|---|---|---|---|
{_stratum_rows(c['strata']['site'])}

### Object type (mayig unicorn variants vs Holdat unicorn; other Holdat iconographies are mayig-empty)

| Stratum | mayig inscr. | Holdat inscr. | Judgeable | Median TV | Status |
|---|---|---|---|---|---|
{_stratum_rows(c['strata']['object_type'])}

### Text length

| Bin | mayig inscr. | Holdat inscr. | Judgeable | Median TV | Status |
|---|---|---|---|---|---|
{_stratum_rows(c['strata']['text_length'])}

### Period

**NOT ESTIMABLE in every cell.** Neither the mayig layer
metadata nor the Holdat CSV carries a period / dating field;
no period stratum is improvised from a proxy.

### Composition adjustment (§5.2)

Holdat per-sign profiles reweighted to the mayig text-length
composition (mayig bin weights:
{c['composition_adjustment']['weights_mayig_length_bins']}).
Adjusted median TV: **{_fmt(c['composition_adjustment']['median_tv'])}**
({c['composition_adjustment']['status']}; pairs included:
{c['composition_adjustment']['n_included']} of 16), vs the
unadjusted Phase-125 median of record 0.636931. Site adjustment
is the Mohenjo-daro stratum itself (mayig is entirely
Mohenjo-daro) and is not double-counted here.

## Arm D — Synthesis: the attribution table (spec §6)

| Mechanism | Supported share | Status | Basis |
|---|---|---|---|
{syn_rows}

Sum of credited explained shares: {_fmt(d['sum_credited_shares'])}.
**Residual unexplained share: {_fmt(d['residual_unexplained_share'])}** —
stated plainly: this is the share of the observed disagreement
that no arm's registered estimator accounts for.

Overlap caveat (binding): {d['overlap_note']}

The matched-object residual row is a *persistence* measure
(how much disagreement survives on matched objects), not an
explained share, and is excluded from the explained sum.

## Claim scope (spec §7)

Every figure above is a statement about the frozen inputs, the
16 judgeable primary pairs, and the Arm A matched set as
found — never about the script as a whole, any individual
pair's crosswalk correctness, or Holdat vs the ICIT lineage
(Phase-116 R-NONE stands untouched). The matcher-eligible
subset ({m['n_eligible']} of 179) is biased toward
inscriptions built from well-attested, unambiguously mapped
signs; Arm A findings describe that subset. **The Phase-125
verdict — FAIL — DISAGREEMENT — and spec 020's NO are
unchanged by anything in this report.**

## Inputs and guards

- mayig layer: 179 inscriptions / 1,003 tokens / 182 P signs;
  Holdat: 1,670 inscriptions / 7,002 tokens / 390 M signs;
  crosswalk v1: 762 pairs, primary map 286 pairs — all asserted
  in code against the frozen totals; the Phase-125 judgeable
  set and observed median TV (0.636931) and the Phase-127
  noise band ([0.046665, 0.131316]) were read from the results
  of record and asserted.
- Arm B's unreversed control evaluation reproduced the
  Phase-125 median TV of record exactly (0.636931) through
  this phase's own code path — a machinery check, not a
  re-score.
- No key join between Holdat and mayig was performed;
  inscriptions were never pooled across compilations;
  Phase-125/127 artifacts were read, never modified.
- Anchors file unchanged: sha256 {r['anchors_sha256_after']}
  before and after (asserted in code).

## Deviations

One implementation clarification, recorded per spec §9 (no
frozen quantity changes): spec §3.2's NEAR tier says "mutual
best"; the implementation reads a tie for best similarity on
either side as disqualifying the pairing (a tied best is not
*the* best), rather than picking the first tied candidate.
Threshold (0.60), tiers, eligibility, and gates are exactly as
frozen. One presentational note: spec Appendix A's design-stage
coverage figure (0.717) is the mean of per-inscription mapped
fractions; the run reports the token-weighted coverage
(0.725823) — same eligibility set (32/179), two averagings.
(Verification counts — suite and foundation — are recorded in
the ledger entries for this phase.)

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
section VI.
"""


if __name__ == "__main__":
    out = run_all()
    a = out["arms"]["a_matched_object_alignment"]
    b = out["arms"]["b_reading_direction"]
    print(json.dumps({
        "matched": a["matcher"]["n_matched"],
        "pair_class_counts": a["pair_class_counts"],
        "b1": b["b1_mayig_reversed"]["median_tv"],
        "b2": b["b2_holdat_reversed"]["median_tv"],
        "anchors_unchanged": out["anchors_unchanged"],
    }, indent=1))
