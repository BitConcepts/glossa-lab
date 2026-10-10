#!/usr/bin/env python3
"""Phase-141 (spec 025, FROZEN 2026-10-10) — F1
leave-one-site-out (LOSO) sensitivity.

Implements specs/025-stage2-controlled-followup/
phase141-freeze.md exactly, under Spec 025 sec.5 and
the Phase-139 freeze record sec.4:

- The Phase-136 test exactly as frozen (Phase-133
  exact-string join; Seals/Tablets restriction;
  TERMINAL14 outcome via the frozen mapping machinery
  only; site strata with the Phase-136 eligibility
  definition; CMH statistic; within-stratum
  permutation of object-type labels, B = 9,999, seed
  20261009; MH common OR with Robins-Breslow-Greenland
  95% CI), with ONE added parameter — a stratum-drop
  selector. The Phase-136 pure functions are imported
  and reused, not re-implemented.
- Pre-run reproduction: the no-drop configuration must
  reproduce the committed Phase-136 result EXACTLY
  (flow, strata, tables, CMH, MH OR + CI, permutation
  counts, raw p) before any subset is accepted. A
  mismatch aborts the run (freeze section 2).
- Subsets: L-MD (drop Mohenjo-daro), L-HA (drop
  Harappa), L-KA (drop Kalibangan). Remaining strata
  are not re-derived; their tables are asserted equal
  to the committed Phase-136 tables.
- Estimability per subset: the Phase-136 sec.5 rule
  mechanically (>= 2 eligible strata AND pooled
  expected counts >= 5 in >= 80% of cells). A failing
  subset is NOT ESTIMABLE as a sensitivity — a
  designed outcome; it mints no statistic.
- Robustness criterion (spec sec.5, verbatim): F1 is
  reported stable iff every estimable subset's MH
  common OR > 1 with its 95% CI excluding 1; otherwise
  the dropped site whose removal breaks the criterion
  is named LOAD-BEARING and the F1 summary language is
  downgraded accordingly. Raw permutation p-values are
  reported; NO q-values are computed for LOSO members
  (adjudication Q4(b)). LOSO mints no verdicts — its
  output is a robustness statement about F1 only.

Class I fields enter NOTHING (the Phase-136 fence is
inherited unchanged). This script imports ONLY the
mapping machinery from the PRED harness lineage
(SignMapper / build_sign_maps, via the Phase-136
module); it never imports or calls any PRED scoring,
and no output of this phase is an input to PRED.

Inputs live in the local store (never committed);
every input path + sha256 is recorded. Deterministic:
permutation streams are fully seeded; no wall-clock
values are written into the results JSON (H9/H11).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

_SPEC136 = importlib.util.spec_from_file_location(
    "phase136_terminal_type",
    REPO / "backend" / "scripts" / "phase136_terminal_type.py")
p136 = importlib.util.module_from_spec(_SPEC136)
_SPEC136.loader.exec_module(p136)

from glossa_lab.pred_harness import SignMapper, build_sign_maps  # noqa: E402

PHASE136_RESULTS = REPO / "reports" / "phase136_results.json"
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
ANCHORS_SHA256 = ("eccea6d527c412c8e882f9a6a786b002aebaf8b"
                  "e1f282c86ebb1fa3b602cfaed")
DEFAULT_OUT = REPO / "reports" / "phase141_results.json"

B_PERM = p136.B_PERM            # 9,999 (frozen)
SEED = p136.SEED                # 20261009 (frozen)
TERMINAL14 = p136.TERMINAL14
PLACEHOLDERS = p136.PLACEHOLDERS

DROP_LABELS = {"Mohenjo-daro": "L-MD", "Harappa": "L-HA",
               "Kalibangan": "L-KA"}


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact p for [[a, b], [c, d]] with
    fixed margins, by exact rational enumeration of all
    tables with the same margins (probability-ordering
    rule). Descriptive stratum detail only."""
    n = a + b + c + d
    row1, col1 = a + b, a + c
    lo = max(0, row1 + col1 - n)
    hi = min(row1, col1)
    denom = math.comb(n, col1)

    def prob(x: int) -> Fraction:
        return Fraction(math.comb(row1, x)
                        * math.comb(n - row1, col1 - x), denom)

    p_obs = prob(a)
    total = sum((prob(x) for x in range(lo, hi + 1)
                 if prob(x) <= p_obs), Fraction(0))
    return float(total)


def estimability(tables: list[dict]) -> dict:
    """Phase-136 sec.5 rule, verbatim: >= 2 eligible
    strata AND pooled expected counts >= 5 in >= 80% of
    the pooled 2x2's 4 cells."""
    pooled = {k: sum(t[k] for t in tables) for k in "abcd"}
    pooled_n = sum(pooled.values())
    row_totals = [pooled["a"] + pooled["b"],
                  pooled["c"] + pooled["d"]]
    col_totals = [pooled["a"] + pooled["c"],
                  pooled["b"] + pooled["d"]]
    expected = [row_totals[0] * col_totals[0] / pooled_n,
                row_totals[0] * col_totals[1] / pooled_n,
                row_totals[1] * col_totals[0] / pooled_n,
                row_totals[1] * col_totals[1] / pooled_n]
    frac = sum(1 for e in expected if e >= 5) / 4
    estimable = len(tables) >= 2 and frac >= 0.8
    return {"n_eligible_strata": len(tables),
            "pooled_table": pooled,
            "pooled_expected_counts": expected,
            "fraction_expected_ge_5": frac,
            "rule": ("Phase-136 sec.5: >=2 eligible strata "
                     "AND pooled expected counts >=5 in "
                     ">=80% of cells"),
            "estimable": estimable,
            "verdict": "ESTIMABLE" if estimable
                       else "NOT ESTIMABLE"}


def run_configuration(strata: list[dict], label: str) -> dict:
    """One Phase-136 configuration over the given
    eligible strata (machinery imported, unchanged)."""
    tables = [s["table"] for s in strata]
    est = estimability(tables)
    out: dict = {
        "strata_sites": [s["site"] for s in strata],
        "estimability": est,
        "per_stratum": [],
        "effect_sizes": None, "test": None}
    for s in strata:
        t = s["table"]
        or_value = p136.odds_ratio(t["a"], t["b"], t["c"], t["d"])
        out["per_stratum"].append({
            "site": s["site"], "table": t,
            "odds_ratio": (or_value if or_value is not None
                           and math.isfinite(or_value) else None),
            "fisher_exact_two_sided_p_descriptive":
                fisher_exact_two_sided(t["a"], t["b"],
                                       t["c"], t["d"]),
            "terminal14_share_seals": (
                t["a"] / (t["a"] + t["b"])
                if t["a"] + t["b"] else None),
            "terminal14_share_tablets": (
                t["c"] / (t["c"] + t["d"])
                if t["c"] + t["d"] else None)})
    if not tables:
        return out
    mh = p136.mh_odds_ratio(tables)
    pooled = est["pooled_table"]
    out["effect_sizes"] = {
        "mh_common_odds_ratio": mh["common_odds_ratio"],
        "mh_log_or": mh["log_or"],
        "mh_var_log_or_rbg": mh["var_log_or"],
        "mh_ci95": mh["ci95"],
        "crude_odds_ratio_uncontrolled":
            p136.crude_odds_ratio(tables),
        "pooled_terminal14_shares": {
            "seals": (pooled["a"] / (pooled["a"] + pooled["b"])
                      if pooled["a"] + pooled["b"] else None),
            "tablets": (pooled["c"] / (pooled["c"] + pooled["d"])
                        if pooled["c"] + pooled["d"] else None)}}
    if est["estimable"]:
        obs = p136.cmh_statistic(tables)
        perm = p136.permutation_test(strata)
        assert abs(perm["statistic_observed"] - obs) < 1e-9
        out["test"] = {
            "statistic_observed": obs, "B": perm["b"],
            "seed": perm["seed"],
            "n_perm_ge_observed": perm["n_perm_ge_observed"],
            "raw_p": perm["p_value"],
            "perm_stat_median": perm["perm_stat_median"],
            "perm_stat_p95": perm["perm_stat_p95"]}
    return out


def build_population() -> tuple[list[dict], dict, dict]:
    """The Phase-136 population construction, replicated
    call-for-call (join, restriction, terminal mapping,
    eligibility) using the Phase-136 module's constants
    and paths. Returns (eligible strata, flow, inputs).
    Exactness is enforced by the no-drop reproduction
    assertion in build()."""
    cat_dir = p136.catalogue_dir()
    inputs: dict[str, dict] = {}

    def register(key: str, path: Path) -> Path:
        inputs[key] = {"path": str(path), "exists": path.exists(),
                       "sha256": sha256_of(path) if path.exists()
                                 else None,
                       "bytes": path.stat().st_size
                                 if path.exists() else None}
        return path

    vol_paths = {vol: register(f"cisi_vol{vol}_catalogue",
                               cat_dir / f"cisi_vol{vol}_catalogue.csv")
                 for vol in (1, 2)}
    horus_path = register("horus84_inscriptions", p136.HORUS84)
    registry_path = register("canonical_sign_registry",
                             p136.REGISTRY)

    vol_ids: dict[int, set] = {}
    obj_view: dict[tuple[int, str], dict] = {}
    for vol in (1, 2):
        with vol_paths[vol].open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        vol_ids[vol] = {r["cisi_id"] for r in rows}
        for r in rows:
            d = obj_view.setdefault((vol, r["cisi_id"]),
                                    {"site": "", "object_type": ""})
            for f in d:
                if not d[f] and r[f].strip():
                    d[f] = r[f]

    with horus_path.open(newline="", encoding="utf-8") as fh:
        horus_rows = list(csv.DictReader(fh))

    matched = ambiguous = unmatched = 0
    typed: Counter = Counter()
    untyped = 0
    joined: list[tuple[dict, dict]] = []
    for r in horus_rows:
        value = r["cisi"]
        in1, in2 = value in vol_ids[1], value in vol_ids[2]
        if in1 and in2:
            ambiguous += 1
            continue
        if not (in1 or in2):
            unmatched += 1
            continue
        matched += 1
        obj = obj_view[(1 if in1 else 2, value)]
        joined.append((r, obj))
        if obj["object_type"]:
            typed[obj["object_type"]] += 1
        else:
            untyped += 1

    restricted = [(r, o) for r, o in joined
                  if o["object_type"] in ("Seals", "Tablets")]

    mapper = SignMapper(build_sign_maps(registry_path))
    mapped = unk_terminal = no_codes = 0
    terminal14_margin = 0
    analysis: list[tuple[str, str, bool]] = []
    for r, o in restricted:
        codes = re.findall(r"\d{3}", r["text"] or "")
        if not codes:
            no_codes += 1
            continue
        terminal_code = codes[-1]
        if terminal_code in PLACEHOLDERS:
            p_sign = "UNK"
        else:
            p_sign = mapper.map_w(terminal_code, Counter())
        if p_sign == "UNK":
            unk_terminal += 1
            continue
        mapped += 1
        is_terminal = p_sign in TERMINAL14
        terminal14_margin += int(is_terminal)
        analysis.append((r["site"], o["object_type"], is_terminal))

    by_site: dict[str, list] = defaultdict(list)
    for site, otype, is_term in analysis:
        by_site[site].append((otype, is_term))
    eligible: list[dict] = []
    for site in sorted(by_site, key=lambda s: (-len(by_site[s]), s)):
        rows = by_site[site]
        n_seals = sum(1 for t, _ in rows if t == "Seals")
        n_tablets = len(rows) - n_seals
        if not (len(rows) >= 20 and n_seals >= 5 and n_tablets >= 5):
            continue
        a = sum(1 for t, out in rows if t == "Seals" and out)
        c = sum(1 for t, out in rows if t == "Tablets" and out)
        table = p136.table_from_counts(n_seals, n_tablets, a, c)
        outcomes = ([out for t, out in rows if t == "Seals"]
                    + [out for t, out in rows if t == "Tablets"])
        eligible.append({"site": site, "n_seals": n_seals,
                         "outcomes": outcomes, "table": table})

    flow = {
        "layer_rows": len(horus_rows),
        "matched_single_volume": matched,
        "ambiguous": ambiguous,
        "unmatched": unmatched,
        "restricted_seals_tablets": len(restricted),
        "terminal_mapped": mapped,
        "terminal_unk": unk_terminal,
        "terminal_no_codes": no_codes,
        "terminal14_margin_among_mapped": terminal14_margin,
        "analysis_population_eligible_strata":
            sum(sum(e["table"].values()) for e in eligible),
    }
    return eligible, flow, inputs


def build(out_path: Path) -> dict:
    assert sha256_of(ANCHORS) == ANCHORS_SHA256, "anchors drift (pre)"
    committed136 = json.loads(
        PHASE136_RESULTS.read_text("utf-8"))
    eligible, flow, inputs = build_population()

    # --- Pre-run reproduction (freeze section 2) -------
    nodrop = run_configuration(eligible, "phase141-nodrop")
    c136_test = committed136["test"]
    c136_fx = committed136["effect_sizes"]
    reproduction_ok = (
        flow["layer_rows"] == committed136["flow"]["layer_rows"]
        and flow["matched_single_volume"] == committed136[
            "flow"]["matched_single_volume"]
        and flow["ambiguous"] == committed136["flow"]["ambiguous"]
        and flow["unmatched"] == committed136["flow"]["unmatched"]
        and flow["restricted_seals_tablets"] == committed136[
            "flow"]["restricted_seals_tablets"]
        and flow["terminal_mapped"] == committed136[
            "flow"]["terminal_mapped"]
        and flow["analysis_population_eligible_strata"]
        == committed136["flow"][
            "analysis_population_eligible_strata"]
        and [s["site"] for s in eligible]
        == committed136["eligible_strata"]
        and all(s["table"] == next(
            r["table"] for r in committed136["strata"]
            if r["site"] == s["site"]) for s in eligible)
        and nodrop["test"]["statistic_observed"]
        == c136_test["statistic_observed"]
        and nodrop["test"]["n_perm_ge_observed"]
        == c136_test["n_perm_ge_observed"]
        and nodrop["test"]["raw_p"] == c136_test["raw_p"]
        and nodrop["test"]["perm_stat_median"]
        == c136_test["perm_stat_median"]
        and nodrop["effect_sizes"]["mh_common_odds_ratio"]
        == c136_fx["mh_common_odds_ratio"]
        and nodrop["effect_sizes"]["mh_ci95"] == c136_fx["mh_ci95"])
    assert reproduction_ok, (
        "REPRODUCTION FAILURE: no-drop configuration does not "
        "reproduce Phase-136 exactly; subsets must not proceed "
        "(phase141-freeze.md section 2).")
    print("[phase141] no-drop reproduction vs Phase-136: "
          "EXACT MATCH", flush=True)

    # --- LOSO subsets ----------------------------------
    subsets: dict[str, dict] = {}
    load_bearing: list[str] = []
    not_estimable: list[str] = []
    all_estimable_pass = True
    for drop_site, label in DROP_LABELS.items():
        remaining = [s for s in eligible if s["site"] != drop_site]
        cfg = run_configuration(remaining, f"phase141-{label}")
        cfg["label"] = label
        cfg["dropped_site"] = drop_site
        if not cfg["estimability"]["estimable"]:
            cfg["robustness_reading"] = (
                "NOT ESTIMABLE as a sensitivity (designed "
                "outcome, spec sec.5); mints no test statistic "
                "or p-value and neither confirms nor breaks "
                "stability.")
            not_estimable.append(label)
        else:
            or_value = cfg["effect_sizes"]["mh_common_odds_ratio"]
            ci = cfg["effect_sizes"]["mh_ci95"]
            passes = (or_value is not None and or_value > 1
                      and ci is not None and ci[0] > 1)
            cfg["criterion_reading"] = {
                "mh_or_gt_1": bool(or_value and or_value > 1),
                "ci95_excludes_1": bool(ci and ci[0] > 1),
                "passes": bool(passes)}
            if passes:
                cfg["robustness_reading"] = (
                    f"{label} (drop {drop_site}): MH common OR "
                    f"{or_value:.3f} with 95% CI excluding 1 — "
                    f"criterion holds for this subset.")
            else:
                all_estimable_pass = False
                load_bearing.append(drop_site)
                cfg["robustness_reading"] = (
                    f"{label} (drop {drop_site}): criterion "
                    f"BREAKS — MH common OR {or_value} with 95% "
                    f"CI {ci}; {drop_site} is LOAD-BEARING "
                    f"for F1.")
        subsets[label] = cfg

    if load_bearing:
        named = " and ".join(load_bearing)
        robustness_statement = (
            f"F1 is NOT stable under leave-one-site-out: "
            f"removing {named} breaks the sec.5 criterion, so "
            f"{named} is LOAD-BEARING and the F1 summary "
            f"language is downgraded to 'supported, "
            f"concentrated in {named}' (the strata that "
            f"remain when it is removed do not carry the "
            f"association at the frozen criterion).")
    elif not_estimable and len(not_estimable) == len(subsets):
        robustness_statement = (
            "No LOSO subset is estimable; the robustness of "
            "F1 is UNASSESSED by this panel (a designed "
            "outcome under the sec.5 rule), and no "
            "robustness claim is made.")
        all_estimable_pass = False
    else:
        robustness_statement = (
            "F1 is STABLE under leave-one-site-out: every "
            "estimable subset's Mantel-Haenszel common OR "
            "remains > 1 with its 95% CI excluding 1, so no "
            "single site is load-bearing for the F1 result.")
        if not_estimable:
            robustness_statement += (
                f" Scope: subsets {', '.join(not_estimable)} "
                f"were NOT ESTIMABLE under the sec.5 rule and "
                f"neither confirm nor break stability; the "
                f"statement covers the estimable subsets "
                f"only.")

    result = {
        "phase": "Phase-141",
        "spec": "025",
        "test": "LOSO sensitivity for F1 (Spec 024)",
        "title": ("Leave-one-site-out sensitivity of F1 "
                  "(terminal-class x object type) — "
                  "ICIT-lineage layer (horus84) joined subset"),
        "lineage_label": "ICIT-lineage layer (horus84)",
        "freeze": ("specs/025-stage2-controlled-followup/"
                   "phase141-freeze.md (under spec sec.5 and "
                   "phase139-freeze.md sec.4)"),
        "inputs": inputs,
        "anchors_sha256": sha256_of(ANCHORS),
        "parameters": {"B": B_PERM, "seed": SEED,
                       "p_formula": "(1 + #{perm >= obs}) / (1 + B)",
                       "statistic": ("Cochran-Mantel-Haenszel "
                                     "chi-square, no continuity "
                                     "correction (Phase-136)"),
                       "q_values": ("NONE — no q-values are "
                                    "computed for LOSO members "
                                    "(adjudication Q4(b))")},
        "flow": flow,
        "reproduction_no_drop": {
            "configuration": "Phase-136 exactly (no drop)",
            "matches_committed_phase136_exactly": True,
            "test": nodrop["test"],
            "effect_sizes": nodrop["effect_sizes"],
            "per_stratum": nodrop["per_stratum"],
            "committed_phase136": {
                "cmh_statistic": c136_test["statistic_observed"],
                "raw_p": c136_test["raw_p"],
                "mh_common_odds_ratio":
                    c136_fx["mh_common_odds_ratio"],
                "mh_ci95": c136_fx["mh_ci95"],
                "verdict_spec024": "SUPPORTED"}},
        "subsets": subsets,
        "robustness_criterion": (
            "Spec sec.5, verbatim: F1 is reported stable iff "
            "every estimable subset's Mantel-Haenszel common "
            "OR remains > 1 with its 95% CI excluding 1; if "
            "any estimable subset's CI includes 1 or its OR "
            "<= 1, the dropped site is named LOAD-BEARING "
            "and the F1 summary language is downgraded "
            "('supported, concentrated in ...')."),
        "robustness_outcome": {
            "stable": bool(all_estimable_pass
                           and not load_bearing),
            "load_bearing_sites": load_bearing,
            "not_estimable_subsets": not_estimable,
            "statement": robustness_statement},
        "fence": (
            "LOSO mints no verdicts: this is a robustness "
            "statement about the already-decided F1 result "
            "only. It cannot upgrade, downgrade, or replace "
            "the Spec 024 F1 verdict (SUPPORTED, family BH "
            "q = 0.00015); it qualifies F1's summary "
            "language only, as spec sec.5 pre-specifies."),
        "section8_language": (
            "Associations describe co-occurrence in the "
            "recorded data of this labeled lineage layer's "
            "joined subset only, not meaning. No result "
            "under this spec can mint, promote, demote, or "
            "validate any sign reading, change any anchor's "
            "status, or move PRED-2026 in either direction."),
        "ai_disclosure": (
            "Produced by an AI agent (Muse Spark, via "
            "Muse) at the direction of Tristen "
            "Pierson, per constitution section VI."),
    }
    assert sha256_of(ANCHORS) == ANCHORS_SHA256, "anchors drift (post)"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n",
                        encoding="utf-8")
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args(argv)
    result = build(args.out)
    print(f"[phase141] wrote {args.out}")
    for label, cfg in result["subsets"].items():
        fx = cfg["effect_sizes"] or {}
        test = cfg["test"] or {}
        print(f"[phase141] {label} (drop "
              f"{cfg['dropped_site']}): estimable="
              f"{cfg['estimability']['estimable']} "
              f"MH OR={fx.get('mh_common_odds_ratio')} "
              f"CI={fx.get('mh_ci95')} "
              f"raw_p={test.get('raw_p')}")
    print(f"[phase141] robustness: "
          f"{result['robustness_outcome']['statement']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
