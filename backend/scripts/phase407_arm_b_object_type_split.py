"""Phase-407 — Spec 042: Arm B split by object type.

Executes specs/042-arm-b-object-type-split/freeze.md
(freeze digest 6be2988d...; OSF contract registration
https://osf.io/tmyzg/, approved and public before this
run): Spec 028's Arm B machinery (Phase-393, pinned
pipeline393.py) unchanged, run separately on the
seal-only and tablet-only sets of the Phase-393 analysis
population (3,030 records, 6 sites), each stratum under
the frozen family verdict rules of spec section 4.1, the
headline pre-registered as one pattern (SPLIT /
UNIFORM-PASS / UNIFORM-FAIL / THIN).

Step 0 (spec section 3) runs first, in the frozen
order, fail-closed, before any stratum quantity:

  0.1 input integrity — every section 2 input hashes
      to its freeze-record value (mismatch: INVALID);
  0.2 population reproduction — the frozen population
      flow, re-run on the pinned layer's machinery
      inputs, reproduces the recorded flow counts
      (5,679 / 4,531 / 4,505 / 3,605 / 3,144 / 3,030),
      the recorded flow dict, the recorded Arm B
      analysis set and its site x type cell table
      (mismatch: INVALID);
  0.3 partition census — the analysis population
      partitioned by recorded object type, per stratum
      and per site, the two strata summing to 3,030;
      a record typed neither SEAL nor TAB stops the
      run (INVALID);
  0.4 stratum floors — a stratum enters the test only
      if at least 6 sites each carry at least 20
      inscriptions of its type; a stratum below the
      floor is TOO THIN and, under DD-042-2, the
      execution closes at this gate with headline
      THIN and neither stratum is computed;
  0.5 pooled regression — the un-split Arm B
      machinery, run on the full analysis population
      under the recorded design and seed (20261012),
      reproduces the recorded primary quantities
      exactly (mismatch: INVALID). The recorded
      quantities were produced by the Phase-393
      execution's single RNG stream, in which the
      Arm A sequence consumed the stream before
      Arm B; this gate replicates that stream order
      exactly, using the Phase-393 execution script's
      own run order.

Primaries (spec section 4), reached only if every
gate passes: for each stratum, pipeline393's
run_pipeline_quota under the recorded quota scheme
(the per-site quota is the smallest analysis-site
total of the population under test — 52 in the pooled
Arm B run of record — held fixed across that
stratum's leave-one-site-out cells), the same
negative and positive controls (run_control_quota,
control sign sets and pooled-probability construction
as recorded for Arm B in the Spec 028 margins audit,
the pooled composition taken over the stratum's
eligible records), and the spec section 4.1 verdict
rules applied verbatim. A stratum whose controls
fail is NOT ADJUDICATED (DD-042-3).

Outputs:
  reports/phase407_results.json
  reports/phase407_report.md

The written records carry no timestamps or elapsed
times, so a re-run reproduces them byte-identically.
No anchor is moved; the anchors file is asserted
byte-identical before and after.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "specs" / "042-arm-b-object-type-split"
SPEC028_DIR = ROOT / "specs" / "028-harappa-robustness"
STORE = ROOT / "corpora" / "downloads" / "spec028_harappa"
RESULTS_PATH = ROOT / "reports" / "phase407_results.json"
REPORT_PATH = ROOT / "reports" / "phase407_report.md"
LAYER_PATH = ROOT / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
ANCHORS_PATH = ROOT / "backend/reports/INDUS_FINAL_ANCHORS.json"

SEED = 20261012
MARGIN_R2 = 0.01
FREEZE_DIGEST = ("6be2988d7f4c290591d36f391ac84a772f18a"
                 "9121e35ddd0e251956b5260f753")

# Spec section 2 pins (freeze record values; re-asserted
# in the foreground at execution by two routes).
SECTION2_PINS = {
    "backend/glossa_lab/data/yajnadevam_inscriptions.csv":
        "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98",
    "reports/phase393_results.json":
        "0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607",
    "specs/028-harappa-robustness/pipeline393.py":
        "6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e",
    "specs/028-harappa-robustness/margins-audit.json":
        "15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d",
    "specs/028-harappa-robustness/freeze.json":
        "376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc",
    "backend/reports/INDUS_FINAL_ANCHORS.json":
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
}

RECORDED_FLOW_COUNTS = [5679, 4531, 4505, 3605, 3144, 3030]
RECORDED_ARMB = {
    "median_adj_r2": 0.0223721,
    "adj_r2_interval_95": [0.0122174, 0.0333271],
    "share_draws_rejecting": 0.9548,
    "loso_median_adj_r2": {
        "Harappa": 0.0066068, "Mohenjo-daro": 0.0237627,
        "Dholavira": 0.0243568, "Lothal": 0.0247476,
        "Chanhu-daro": 0.0225587, "Kalibangan": 0.0245373,
    },
}
FLOOR_MIN_SITES = 6
FLOOR_MIN_PER_SITE = 20
FENCE = ("This result is about repertoire association in "
         "recorded data. It is not evidence that any "
         "population moved.")
CORPUS_LABEL = ("the Phase-393 layer (the "
                "Yajnadevam-compiled inscription file as "
                "held by the program), with its lineage "
                "posture as recorded in Specs 027/028")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def count_vector(entry, col_index, n_cols):
    """Verbatim from the Phase-393 execution script
    (backend/scripts/phase393_harappa_robustness.py,
    itself verbatim from Spec 028's build_calibration.py):
    mapped tokens to their M77 column (OTHER if outside
    the frozen set), unmapped to UNMAPPED."""
    vec = np.zeros(n_cols, dtype=np.float64)
    for tok, kind in zip(entry["tokens"], entry["kinds"]):
        if kind in ("direct", "chain"):
            vec[col_index.get(tok, col_index["OTHER"])] += 1.0
        elif kind == "unmapped":
            vec[col_index["UNMAPPED"]] += 1.0
    return vec


def stratum_verdict(controls_ok, primary, loso):
    """Spec 042 section 4.1, verbatim: within a stratum
    whose controls pass, SUPPORTED iff the primary
    median adjusted R^2 is > 0.01 and every
    leave-one-site-out median adjusted R^2 is > 0.01;
    CONTRADICTED iff >= 95% of the primary draws fail
    to reject or the adjusted R^2 percentile interval
    lies entirely at or below 0.01; INCONCLUSIVE iff
    neither fires. A stratum whose controls fail is
    NOT ADJUDICATED (DD-042-3)."""
    if not controls_ok:
        return "NOT ADJUDICATED"
    if (primary["median_adj_r2"] > MARGIN_R2
            and all(s["median_adj_r2"] > MARGIN_R2
                    for s in loso.values())):
        return "SUPPORTED"
    share_fail = 1.0 - primary["share_draws_rejecting"]
    if share_fail >= 0.95 or primary["adj_r2_interval_95"][1] <= MARGIN_R2:
        return "CONTRADICTED"
    return "INCONCLUSIVE"


def headline_for(verdicts):
    """Spec 042 section 4.2: exactly one headline
    pattern from the two per-stratum verdicts."""
    if any(v == "NOT ADJUDICATED" for v in verdicts.values()):
        return "NOT ADJUDICATED"
    seal_ok = verdicts["SEAL"] == "SUPPORTED"
    tab_ok = verdicts["TAB"] == "SUPPORTED"
    if seal_ok and tab_ok:
        return "UNIFORM-PASS"
    if seal_ok:
        return "SPLIT AS PREDICTED"
    if tab_ok:
        return "SPLIT REVERSED"
    return "UNIFORM-FAIL"


def _fmt(x, nd=7):
    return f"{x:.{nd}f}"


def census_table_lines(census):
    sites = census["sites"]
    lines = ["| Site | SEAL | TAB | Total |",
             "|---|---|---|---|"]
    for s in sites:
        lines.append(f"| {s} | {census['SEAL'][s]} | "
                     f"{census['TAB'][s]} | "
                     f"{census['SEAL'][s] + census['TAB'][s]} |")
    lines.append(f"| **Total** | **{census['totals']['SEAL']}** "
                 f"| **{census['totals']['TAB']}** | "
                 f"**{census['totals']['all']}** |")
    return lines


def write_report(res: dict) -> str:
    L = []
    L.append("# Phase-407 — Spec 042: Arm B Split by Object Type")
    L.append("")
    outcome = res["outcome"]
    g = res["step0"]
    census = g.get("gate_0_3", {}).get("census")
    if outcome == "THIN":
        thin = [t for t, f in g["gate_0_4"]["floors"].items()
                if not f["pass"]]
        name = {"SEAL": "seal", "TAB": "tablet"}[thin[0]]
        counts = "; ".join(
            f"{s} {census[thin[0]][s]}"
            for s in census["sites"])
        L.append(f"The object-type split cannot be run as "
                 f"designed: the {name} stratum carries fewer "
                 f"than six sites with at least twenty "
                 f"inscriptions of its type ({counts}). No "
                 f"stratum quantity was computed. Spec 028 "
                 f"Arm B stands exactly as recorded.")
        L.append("")
    elif outcome == "INVALID":
        L.append(f"**STOPPED — INVALID at gate "
                 f"{res['stop_gate']}: {res['stop_reason']}**")
        L.append("")
    L.append(f"Corpus: {CORPUS_LABEL}. Headline outcome: "
             f"**{outcome}**. {FENCE}")
    L.append("")
    L.append("## Step 0 (spec section 3, in order)")
    L.append("")
    L.append(f"- **0.1 Input integrity — "
             f"{'PASS' if g['gate_0_1']['pass'] else 'FAIL'}.** "
             f"Every section 2 input hashes to its "
             f"freeze-record value.")
    if "gate_0_2" in g:
        flow = g["gate_0_2"]
        L.append(f"- **0.2 Population reproduction — "
                 f"{'PASS' if flow['pass'] else 'FAIL'}.** The "
                 f"frozen flow re-run reproduces the recorded "
                 f"counts ({' / '.join(str(n) for n in RECORDED_FLOW_COUNTS)}) "
                 f"and the recorded Arm B analysis set "
                 f"({flow['analysis_records']} records, "
                 f"{flow['sign_columns']} sign columns, cell "
                 f"table identical to the Spec 028 margins "
                 f"audit).")
    if census is not None:
        L.append(f"- **0.3 Partition census — "
                 f"{'PASS' if g['gate_0_3']['pass'] else 'FAIL'}.** "
                 f"The analysis population partitions by "
                 f"recorded object type with no record of any "
                 f"other type; the strata sum to "
                 f"{census['totals']['all']}.")
        L.append("")
        L.extend(census_table_lines(census))
        L.append("")
    if "gate_0_4" in g:
        fl = g["gate_0_4"]["floors"]
        for tc in ("SEAL", "TAB"):
            f = fl[tc]
            L.append(f"- **0.4 Stratum floor ({tc}) — "
                     f"{'PASS' if f['pass'] else 'TOO THIN'}.** "
                     f"{f['sites_at_or_above_floor']} of "
                     f"{len(census['sites'])} sites carry at "
                     f"least {FLOOR_MIN_PER_SITE} inscriptions "
                     f"of the type (minimum site count "
                     f"{f['min_site_count']}).")
        L.append("")
    if outcome == "THIN":
        L.append("Gate 0.5 (pooled regression) was **not "
                 "reached**: the execution closed at gate "
                 "0.4 under DD-042-2, and neither stratum "
                 "was computed.")
        L.append("")
    elif "gate_0_5" in g:
        r = g["gate_0_5"]["reproduced"]
        L.append(f"- **0.5 Pooled regression — "
                 f"{'PASS' if g['gate_0_5']['pass'] else 'FAIL'}.** "
                 f"The un-split Arm B machinery reproduces "
                 f"the recorded primary: median adjusted "
                 f"R^2 {_fmt(r['median_adj_r2'])}, interval "
                 f"[{_fmt(r['adj_r2_interval_95'][0])}, "
                 f"{_fmt(r['adj_r2_interval_95'][1])}], "
                 f"rejection share "
                 f"{r['share_draws_rejecting']:.4f}, and "
                 f"every recorded leave-one-site-out median, "
                 f"including drop-Harappa "
                 f"{_fmt(r['loso_median_adj_r2']['Harappa'])}.")
        L.append("")
    if res.get("strata"):
        L.append("## Primaries (spec section 4)")
        L.append("")
        for tc in ("SEAL", "TAB"):
            s = res["strata"][tc]
            p = s["primary"]
            worst = min(s["loso"].items(),
                        key=lambda kv: kv[1]["median_adj_r2"])
            L.append(f"### {tc} stratum — verdict: "
                     f"**{s['verdict']}**")
            L.append("")
            L.append(f"- Records: {s['records']}; quota per "
                     f"site per draw: {s['quota']}; "
                     f"inscriptions per draw: "
                     f"{s['inscriptions_per_draw']}")
            L.append(f"- Median adjusted R^2: "
                     f"**{_fmt(p['median_adj_r2'])}**; interval "
                     f"[{_fmt(p['adj_r2_interval_95'][0])}, "
                     f"{_fmt(p['adj_r2_interval_95'][1])}] vs "
                     f"margin 0.01; rejection share "
                     f"{p['share_draws_rejecting']:.4f}; median "
                     f"raw R^2 {_fmt(p['median_raw_r2'])}")
            L.append(f"- Minimum leave-one-site-out median: "
                     f"{_fmt(worst[1]['median_adj_r2'])} "
                     f"(dropping {worst[0]})")
            L.append(f"- Controls: negative "
                     f"{'PASS' if s['negative_control']['pass'] else 'FAIL'}, "
                     f"positive "
                     f"{'PASS' if s['positive_control']['pass'] else 'FAIL'}")
            L.append("")
            L.append("| Dropped site | Median adj R^2 | "
                     "Interval | Share rejecting |")
            L.append("|---|---|---|---|")
            for site, cell in s["loso"].items():
                L.append(f"| {site} | "
                         f"{_fmt(cell['median_adj_r2'])} | "
                         f"[{_fmt(cell['adj_r2_interval_95'][0])}, "
                         f"{_fmt(cell['adj_r2_interval_95'][1])}] | "
                         f"{cell['share_draws_rejecting']:.4f} |")
            L.append("")
    if res.get("descriptions"):
        L.append("## Stratum descriptions (spec section 5; "
                 "described, not controlled)")
        L.append("")
    for tc in ("SEAL", "TAB"):
        if not res.get("descriptions"):
            break
        d = res["descriptions"][tc]
        per = ", ".join(f"{k}: {v}" for k, v in
                        d["period"].items())
        pres = ", ".join(f"{k}: {v}" for k, v in
                         d["preservation"].items())
        L.append(f"- **{tc}** (period mix, as recorded in "
                 f"the pinned layer): {per}.")
        L.append(f"- **{tc}** (preservation, as recorded "
                 f"in the pinned layer): {pres}.")
    L.append("")
    L.append("Object type is one compilation's recording: "
             "Spec 037's census found the CISI volumes and "
             "the program's corpus classify matched objects' "
             "types differently in 49% of cases. This test "
             "uses type only as recorded within the "
             "Phase-393 layer, consistently for both strata.")
    L.append("")
    L.append("## Provenance")
    L.append("")
    L.append(f"- Freeze: specs/042-arm-b-object-type-split/"
             f"freeze.md; digest {FREEZE_DIGEST}")
    L.append("- OSF registration of the frozen contract: "
             "https://osf.io/tmyzg/ (approved and public "
             "before execution)")
    L.append(f"- Seed {SEED}; margin adjusted R^2 0.01; "
             f"anchors asserted byte-identical before and "
             f"after ({res['anchors']['before'][:12]}...).")
    L.append("")
    return "\n".join(L)


def main() -> int:
    res: dict = {
        "experiment": "spec042-phase407-arm-b-object-type-split",
        "phase": 407,
        "spec": "042-arm-b-object-type-split",
        "freeze_digest": FREEZE_DIGEST,
        "claim_under_test": "STUDY-SPEC-028/ARM-B",
        "outcome": None,
        "stop_gate": None,
        "stop_reason": None,
        "step0": {},
        "strata": None,
        "headline": None,
    }
    anchors_before = sha256_file(ANCHORS_PATH)
    res["anchors"] = {"before": anchors_before}

    def finish():
        res["anchors"]["after"] = sha256_file(ANCHORS_PATH)
        res["anchors"]["byte_identical"] = bool(
            res["anchors"]["before"] == res["anchors"]["after"])
        RESULTS_PATH.write_text(
            json.dumps(res, indent=1) + "\n", encoding="utf-8")
        REPORT_PATH.write_text(write_report(res),
                               encoding="utf-8")
        print(json.dumps({"outcome": res["outcome"],
                          "stop_gate": res["stop_gate"],
                          "stop_reason": res["stop_reason"]},
                         indent=1))
        return 0

    def invalid(gate, reason):
        res["outcome"] = "INVALID"
        res["stop_gate"] = gate
        res["stop_reason"] = reason
        return finish()

    # ---- Gate 0.1: input integrity ----
    pins = {}
    for rel, want in SECTION2_PINS.items():
        got = sha256_file(ROOT / rel)
        pins[rel] = {"expected_sha256": want,
                     "observed_sha256": got,
                     "match": got == want}
    res["step0"]["gate_0_1"] = {
        "check": "every spec section 2 input hashes to its "
                 "freeze-record value",
        "pins": pins,
        "pass": all(p["match"] for p in pins.values()),
    }
    if not res["step0"]["gate_0_1"]["pass"]:
        bad = [r for r, p in pins.items() if not p["match"]]
        return invalid("0.1", "input hash mismatch: "
                       + ", ".join(bad))

    # Machinery inputs of the frozen flow (hash-asserted
    # in Spec 028's build_margins_audit.py, the frozen
    # values of Specs 025/027/028).
    sys.path.insert(0, str(SPEC028_DIR))
    import build_margins_audit as audit_mod
    import pipeline393 as pipe

    store_hashes = {}
    for name, want in audit_mod.EXPECTED_SHA256.items():
        got = sha256_file(STORE / name)
        store_hashes[name] = {"expected_sha256": want,
                              "observed_sha256": got,
                              "match": got == want}
    res["step0"]["gate_0_2_store_inputs"] = store_hashes
    if not all(h["match"] for h in store_hashes.values()):
        return invalid("0.2", "Phase-393 store input hash "
                       "mismatch")

    keyed = json.loads(
        (STORE / "icit_converted_v2_keyed.json").read_text(
            encoding="utf-8"))
    horus = {}
    with open(STORE / "horus_inscriptions.csv", newline="",
              encoding="utf-8") as f:
        for row in csv.DictReader(f):
            horus[row["id"]] = row
    eligible, flow = audit_mod.build_eligible(
        keyed["inscriptions"], horus)
    columns, _sc = audit_mod.composition_columns(eligible)
    col_index = {c: i for i, c in enumerate(columns)}
    n_cols = len(columns)
    vectors = np.array([count_vector(e, col_index, n_cols)
                        for e in eligible])
    site_counts = Counter(e["site"] for e in eligible)
    analysis_ix = [i for i, e in enumerate(eligible)
                   if site_counts[e["site"]] >= audit_mod.MIN_SITE]
    analysis = [eligible[i] for i in analysis_ix]
    a_vectors_all = vectors[analysis_ix]

    recorded = json.loads(
        (ROOT / "reports/phase393_results.json").read_text(
            encoding="utf-8"))
    audit = json.loads(
        (SPEC028_DIR / "margins-audit.json").read_text(
            encoding="utf-8"))

    # ---- Gate 0.2: population reproduction ----
    flow_counts = [flow["layer_records"],
                   flow["after_dedup_kept"],
                   flow["provenanced"], flow["seal_tab"],
                   flow["eligible_primary"], len(analysis)]
    cells = {f"{s}|{t}": n for (s, t), n in sorted(
        Counter((e["site"], e["type_class"])
                for e in analysis).items())}
    gate02 = {
        "check": "the frozen population flow re-run "
                 "reproduces the recorded counts, flow, and "
                 "Arm B analysis set exactly",
        "flow_counts_observed": flow_counts,
        "flow_counts_recorded": RECORDED_FLOW_COUNTS,
        "flow_matches_recorded_results":
            flow == recorded["population"]["flow"],
        "flow_matches_margins_audit":
            flow == audit["population_flow"],
        "analysis_records": len(analysis),
        "analysis_sites": sorted({e["site"] for e in analysis}),
        "cells_match_margins_audit":
            cells == audit["analysis_population"]["cells"],
        "sign_columns": n_cols,
        "sign_columns_recorded": audit["sign_columns"],
    }
    gate02["pass"] = bool(
        flow_counts == RECORDED_FLOW_COUNTS
        and gate02["flow_matches_recorded_results"]
        and gate02["flow_matches_margins_audit"]
        and gate02["cells_match_margins_audit"]
        and n_cols == audit["sign_columns"]
        and len(analysis) == recorded["arm_b"]["records"])
    res["step0"]["gate_0_2"] = gate02
    if not gate02["pass"]:
        return invalid("0.2", "population flow or analysis "
                       "set not reproduced")

    # ---- Gate 0.3: partition census ----
    sites_sorted = sorted({e["site"] for e in analysis})
    census = {"sites": sites_sorted}
    other_types = sorted({e["type_class"] for e in analysis}
                         - {"SEAL", "TAB"})
    for tc in ("SEAL", "TAB"):
        census[tc] = {s: sum(1 for e in analysis
                             if e["site"] == s
                             and e["type_class"] == tc)
                      for s in sites_sorted}
    census["totals"] = {
        "SEAL": sum(census["SEAL"].values()),
        "TAB": sum(census["TAB"].values()),
        "all": len(analysis),
    }
    gate03 = {
        "check": "partition census by recorded object "
                 "type; the two strata sum to 3,030; a "
                 "record typed neither SEAL nor TAB stops "
                 "the run",
        "census": census,
        "other_types_present": other_types,
        "strata_sum": (census["totals"]["SEAL"]
                       + census["totals"]["TAB"]),
    }
    gate03["pass"] = bool(gate03["strata_sum"] == 3030
                          and not other_types)
    res["step0"]["gate_0_3"] = gate03
    if not gate03["pass"]:
        return invalid("0.3", "partition census failed: "
                       f"strata sum {gate03['strata_sum']}, "
                       f"other types {other_types}")

    # Per-stratum descriptions (spec section 5): period
    # and preservation mixes as recorded in the pinned
    # layer, joined by inscription id. Descriptions are
    # recorded-field distributions over the census
    # population, not repertoire quantities.
    layer_by_id = {}
    with open(LAYER_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            layer_by_id[row["id"]] = row
    descriptions = {}
    for tc in ("SEAL", "TAB"):
        sub = [e for e in analysis if e["type_class"] == tc]
        joined = [layer_by_id[e["id"]] for e in sub
                  if e["id"] in layer_by_id]
        descriptions[tc] = {
            "records": len(sub),
            "description_join_coverage": len(joined),
            "period": dict(sorted(Counter(
                r["period"] for r in joined).items())),
            "preservation": dict(sorted(Counter(
                r["preservation"] for r in joined).items())),
        }
    res["descriptions"] = descriptions

    # ---- Gate 0.4: stratum floors ----
    floors = {}
    for tc in ("SEAL", "TAB"):
        counts = census[tc]
        floors[tc] = {
            "sites_at_or_above_floor": sum(
                1 for v in counts.values()
                if v >= FLOOR_MIN_PER_SITE),
            "sites_required": FLOOR_MIN_SITES,
            "min_per_site": FLOOR_MIN_PER_SITE,
            "min_site_count": min(counts.values()),
            "per_site_counts": counts,
        }
        floors[tc]["pass"] = bool(
            floors[tc]["sites_at_or_above_floor"]
            >= FLOOR_MIN_SITES)
        floors[tc]["too_thin"] = not floors[tc]["pass"]
    res["step0"]["gate_0_4"] = {
        "check": "at least 6 sites each carrying at "
                 "least 20 inscriptions of the type, per "
                 "stratum; either stratum below its floor "
                 "closes the execution THIN (DD-042-2)",
        "floors": floors,
        "pass": all(f["pass"] for f in floors.values()),
    }
    if not res["step0"]["gate_0_4"]["pass"]:
        res["outcome"] = "THIN"
        res["headline"] = "THIN"
        res["stop_gate"] = "0.4"
        thin = [t for t, f in floors.items() if not f["pass"]]
        res["stop_reason"] = (
            "stratum TOO THIN: " + ", ".join(thin)
            + " (execution closes at gate 0.4; neither "
              "stratum computed; gate 0.5 not reached)")
        res["step0"]["gate_0_5"] = {"reached": False}
        return finish()

    # ---- Gate 0.5: pooled regression ----
    # Replicates the Phase-393 execution's RNG stream
    # order exactly (Arm A sequence first, then Arm B),
    # so the recorded Arm B stream position is the one
    # the recorded quantities were produced at.
    def subset(entries_src, vec_src, keep):
        ix = [i for i, e in enumerate(entries_src)
              if e["site"] in keep]
        return [entries_src[i] for i in ix], vec_src[ix]

    all_sites = audit_mod.PHASE392_ANALYSIS_SITES
    arm_a_sites = audit_mod.ARM_A_SITES
    rng = np.random.default_rng(SEED)
    a_entries, a_vectors = subset(analysis, a_vectors_all,
                                  set(arm_a_sites))
    pipe.run_pipeline_cells(a_entries, a_vectors, rng)
    for site in arm_a_sites:
        sub_e, sub_v = subset(a_entries, a_vectors,
                              set(arm_a_sites) - {site})
        pipe.run_pipeline_cells(sub_e, sub_v, rng)
    s_ix = [i for i, e in enumerate(a_entries)
            if e["complete"] != "N"]
    pipe.run_pipeline_cells([a_entries[i] for i in s_ix],
                            a_vectors[s_ix], rng)
    b_primary = pipe.summarise(pipe.run_pipeline_quota(
        analysis, a_vectors_all, rng))
    b_loso = {}
    for site in all_sites:
        sub_e, sub_v = subset(analysis, a_vectors_all,
                              set(all_sites) - {site})
        b_loso[site] = pipe.summarise(pipe.run_pipeline_quota(
            sub_e, sub_v, rng))
    reproduced = {
        "median_adj_r2": b_primary["median_adj_r2"],
        "adj_r2_interval_95": b_primary["adj_r2_interval_95"],
        "share_draws_rejecting":
            b_primary["share_draws_rejecting"],
        "loso_median_adj_r2": {
            s: b_loso[s]["median_adj_r2"] for s in all_sites},
    }
    gate05_pass = bool(
        round(reproduced["median_adj_r2"], 7)
        == RECORDED_ARMB["median_adj_r2"]
        and [round(v, 7) for v in
             reproduced["adj_r2_interval_95"]]
        == RECORDED_ARMB["adj_r2_interval_95"]
        and round(reproduced["share_draws_rejecting"], 4)
        == RECORDED_ARMB["share_draws_rejecting"]
        and all(round(reproduced["loso_median_adj_r2"][s], 7)
                == RECORDED_ARMB["loso_median_adj_r2"][s]
                for s in all_sites))
    res["step0"]["gate_0_5"] = {
        "check": "the un-split Arm B machinery reproduces "
                 "the recorded primary quantities exactly "
                 "at the recorded precision",
        "reached": True,
        "reproduced": reproduced,
        "recorded": RECORDED_ARMB,
        "pass": gate05_pass,
    }
    if not gate05_pass:
        return invalid("0.5", "pooled Arm B regression does "
                       "not reproduce the recorded quantities")

    # ---- Primaries (spec section 4) ----
    sign_sets = audit["arm_b_site_equal"][
        "positive_control_sign_sets"]
    strata = {}
    verdicts = {}
    for tc in ("SEAL", "TAB"):
        sub_ix = [i for i, e in enumerate(analysis)
                  if e["type_class"] == tc]
        sub_entries = [analysis[i] for i in sub_ix]
        sub_vectors = a_vectors_all[sub_ix]
        site_totals = Counter(e["site"] for e in sub_entries)
        quota = min(site_totals[s] for s in all_sites)
        run = pipe.run_pipeline_quota(sub_entries, sub_vectors,
                                      rng, quota=quota)
        primary = pipe.summarise(run)
        loso = {}
        for site in all_sites:
            le, lv = subset(sub_entries, sub_vectors,
                            set(all_sites) - {site})
            loso[site] = pipe.summarise(pipe.run_pipeline_quota(
                le, lv, rng, quota=quota))
        elig_sub = [e for e in eligible
                    if e["type_class"] == tc]
        crng = np.random.default_rng(SEED)
        pooled_counts = np.zeros(n_cols)
        for e in elig_sub:
            pooled_counts += count_vector(e, col_index, n_cols)
        pooled = pooled_counts / pooled_counts.sum()
        neg = pipe.summarise(pipe.run_control_quota(
            sub_entries, {s: pooled for s in all_sites},
            crng, quota=quota))
        pos_probs = {}
        for s in all_sites:
            p = pooled.copy()
            idx = [col_index[c] for c in sign_sets[s]]
            p[idx] *= pipe.POSITIVE_BOOST
            pos_probs[s] = p / p.sum()
        pos = pipe.summarise(pipe.run_control_quota(
            sub_entries, pos_probs, crng, quota=quota))
        neg = dict(neg, **{"pass": pipe.negative_control_pass(neg)})
        pos = dict(pos, **{"pass": pipe.positive_control_pass(pos)})
        controls_ok = bool(neg["pass"] and pos["pass"])
        verdicts[tc] = stratum_verdict(controls_ok, primary, loso)
        strata[tc] = {
            "records": len(sub_entries),
            "quota": quota,
            "inscriptions_per_draw":
                int(sum(sum(a.values()) for a in
                        primary["quota_allocations"].values())),
            "primary": primary, "loso": loso,
            "negative_control": neg, "positive_control": pos,
            "controls_pass": controls_ok,
            "verdict": verdicts[tc],
            "failing_controls": [
                name for name, c in (("negative", neg),
                                     ("positive", pos))
                if not c["pass"]],
        }
    res["strata"] = strata
    res["headline"] = headline_for(verdicts)
    res["outcome"] = res["headline"]
    return finish()


if __name__ == "__main__":
    raise SystemExit(main())
