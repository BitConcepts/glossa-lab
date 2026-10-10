#!/usr/bin/env python3
"""Phase-140 (spec 025, FROZEN 2026-10-10) — G1: the
Phase-137 F3 site-repertoire test re-run on the
ICIT-lineage layer (horus84) under confounder control.

Implements specs/025-stage2-controlled-followup/
phase140-freeze.md exactly, under the Phase-139 freeze
record (phase139-freeze.md, merged PR #130):

- Population: the Phase-137 F3 analysis population
  reproduced by rule (7 eligible sites; 5,410
  inscriptions with >= 1 parsed token).
- Statistic family: Phase-137 F3 exactly — site x sign
  profile table (columns = layer-wide count >= 10
  within the population, rarer signs pooled into
  OTHER; placeholders 000/999 excluded), Pearson
  chi-square as the divergence statistic, Cramer's V
  and per-site total-variation distances descriptive,
  inference ONLY by permutation. The Phase-137 pure
  helpers are imported and reused, not re-implemented.
- Primary test G1: permutation of site labels WITHIN
  composition (Phase-137 type class x length class) x
  preservation strata (complete / fragment / damaged;
  UNRECORDED retained as a stratum level). The
  primary-control set is exactly {preservation}.
  B = 9,999, seed 20261009, p = (1 + #{chi2_perm >=
  chi2_obs}) / (1 + B).
- Verdict (adjudication Q4(b)): Benjamini-Hochberg over
  G1 alone at q = 0.05 — with m = 1 this is exactly the
  raw permutation p against 0.05: SUPPORTED under
  control iff raw p <= 0.05, else NOT SUPPORTED under
  control. It is NOT a family correction across the
  LOSO members; that is stated wherever the verdict
  appears.
- Sensitivity panel (EXPLORATORY, pre-declared in the
  Phase-139 record): S-chron (composition x chron_band
  strata) and S-depth (composition x depth_band
  strata), same statistic / B / seed. Reported as
  bounds with their recorded coverage stated; never
  the controlled verdict; excluded from verdict words.
- Pre-run regression: the uncontrolled configuration
  (composition-only strata, the Phase-137 F3
  configuration) must reproduce the committed
  Phase-137 F3 result EXACTLY (observed chi-square,
  permutation count, median, p95, raw p) before the
  controlled configurations are accepted. A mismatch
  aborts the run (freeze section 5).
- Covariates come from the committed Phase-139
  harmonized dataset, joined on the layer's unique id
  column; the join and the composition-stratum
  agreement are asserted for all 5,410 rows.

Chronology is NOT controlled in the primary test:
period/phase (chronology) remain uncontrolled
confounders, and that rider travels with every G1
number this script emits.

Class I fields (horus84 class/sanskrit/translation/
notes) enter NOTHING. The layer input lives in the
local store (never committed); its path + sha256 are
recorded. Deterministic: the permutation stream is
fully seeded; no wall-clock values are written into
the results JSON (governance H9/H11).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

_SPEC137 = importlib.util.spec_from_file_location(
    "phase137_site_repertoire",
    REPO / "backend" / "scripts" / "phase137_site_repertoire.py")
p137 = importlib.util.module_from_spec(_SPEC137)
_SPEC137.loader.exec_module(p137)

HORUS84 = (Path.home() / "workspace" / "research_notes"
           / "indus-data-deep-sweep-20261008" / "downloads"
           / "horus84-computational-linguistics" / "data"
           / "inscriptions.csv")
LAYER_SHA256 = "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
COVARIATES = (REPO / "data" / "evidence_integration"
              / "phase139_harmonized_covariates.json")
PHASE137_RESULTS = REPO / "reports" / "phase137_results.json"
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
ANCHORS_SHA256 = ("eccea6d527c412c8e882f9a6a786b002aebaf8b"
                  "e1f282c86ebb1fa3b602cfaed")
DEFAULT_OUT = REPO / "reports" / "phase140_results.json"

B_PERM = p137.B_PERMUTATIONS    # 9,999 (frozen)
SEED = p137.SEED                # 20261009 (frozen)
MIN_SIGN_COUNT = p137.MIN_SIGN_COUNT
PLACEHOLDERS = p137.PLACEHOLDERS
DEADLINE_SECONDS = 3300

HEADLINE_LABEL = "ICIT-lineage layer (horus84)"
CHRONOLOGY_RIDER = (
    "Chronology is NOT controlled in the primary test: "
    "period/phase (chronology) remain uncontrolled "
    "confounders; the S-chron sensitivity bound is "
    "reported alongside, never as the controlled "
    "verdict.")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_horus_with_id(path: Path) -> list[dict]:
    """Phase-137 load_horus, verbatim, plus the layer's
    raw ``id`` value (unstripped) for the Phase-139
    covariate join. Every other field is computed
    exactly as Phase-137 computes it."""
    inscriptions = []
    with open(path, encoding="utf-8", newline="") as fh:
        for raw in csv.DictReader(fh):
            site = (raw["site"] or "").strip()
            type_value = (raw["type"] or "").strip()
            text = raw["text"] or ""
            parsed = re.findall(r"\d{3}", text)
            profile = [c for c in parsed
                       if c not in PLACEHOLDERS]
            inscriptions.append({
                "id": raw["id"],
                "site": site,
                "stratum": (
                    f"{p137.horus_type_class(type_value)}|"
                    f"{p137.horus_length_class(len(parsed))}"),
                "tokens": profile,
                "n_parsed_tokens": len(parsed),
            })
    return inscriptions


def permutable_inscriptions(analysis: list[dict],
                            key_of) -> tuple[int, list[dict]]:
    """Inscriptions in strata containing >= 2 distinct
    sites are permutable; rows in single-site strata are
    constant under permutation. Returns (permutable_n,
    per-stratum table)."""
    by_stratum: dict[str, dict] = {}
    for insc in analysis:
        key = key_of(insc)
        e = by_stratum.setdefault(
            key, {"stratum": key, "n_inscriptions": 0,
                  "sites": set()})
        e["n_inscriptions"] += 1
        e["sites"].add(insc["site"])
    table = []
    permutable = 0
    for key in sorted(by_stratum):
        e = by_stratum[key]
        n_sites = len(e["sites"])
        p = e["n_inscriptions"] if n_sites >= 2 else 0
        permutable += p
        table.append({"stratum": key,
                      "n_inscriptions": e["n_inscriptions"],
                      "n_sites": n_sites,
                      "sites": sorted(e["sites"]),
                      "permutable_inscriptions": p})
    return permutable, table


def run_configuration(analysis, sparse_base, table,
                      n_sites, n_cols, key_of,
                      label: str) -> dict:
    """One Phase-137-family configuration under the
    given stratum-key function. ``sparse_base`` entries
    are (site_idx, vec_tuple) in analysis order; the
    Phase-137 helpers are reused verbatim."""
    observed = p137.chi_square(table)
    permutable, strata_table = permutable_inscriptions(
        analysis, key_of)
    perm_input = [(site_idx, key_of(insc), vec)
                  for insc, (site_idx, vec)
                  in zip(analysis, sparse_base)]
    stats_sorted, count_ge = p137.run_permutation(
        perm_input, n_sites, n_cols, observed,
        B_PERM, SEED, DEADLINE_SECONDS, label)
    summary = p137.permutation_summary(stats_sorted, count_ge,
                                       B_PERM)
    return {
        "observed_chi_square": observed,
        "cramers_v_descriptive": p137.cramers_v(table, observed),
        "per_site_tv_distance_descriptive": None,  # filled by caller
        "sparsity_disclosure": p137.sparsity_disclosure(table),
        "strata": {"n_strata": len(strata_table),
                   "table": strata_table},
        "nominal_inscriptions": len(analysis),
        "permutable_inscriptions": permutable,
        "permutation": summary,
        "p_value_raw": summary["p_value_raw"],
        "_table": table,
    }


def build(out_path: Path) -> dict:
    assert sha256_of(ANCHORS) == ANCHORS_SHA256, "anchors drift (pre)"
    layer_sha = sha256_of(HORUS84)
    assert layer_sha == LAYER_SHA256, f"layer hash drift: {layer_sha}"

    # --- Phase-137 population, reproduced by rule ------
    inscriptions = load_horus_with_id(HORUS84)
    per_site_insc: Counter = Counter()
    per_site_parsed: Counter = Counter()
    for insc in inscriptions:
        per_site_insc[insc["site"]] += 1
        per_site_parsed[insc["site"]] += insc["n_parsed_tokens"]
    eligible = sorted(
        s for s in per_site_insc
        if p137.site_eligible(per_site_insc[s], per_site_parsed[s]))
    analysis = [i for i in inscriptions
                if i["site"] in set(eligible)
                and i["n_parsed_tokens"] >= 1]

    committed137 = json.loads(
        PHASE137_RESULTS.read_text("utf-8"))["layers"]["F3_icit_lineage"]
    assert eligible == committed137["eligible_sites"], eligible
    assert len(analysis) == committed137[
        "analysis_population"]["inscriptions"] == 5410

    # Frozen column set (Phase-137 analyse_layer, verbatim).
    sign_counts: Counter = Counter()
    for insc in analysis:
        sign_counts.update(insc["tokens"])
    kept_signs = sorted(s for s, c in sign_counts.items()
                        if c >= MIN_SIGN_COUNT)
    other_tokens = sum(c for s, c in sign_counts.items()
                       if c < MIN_SIGN_COUNT)
    columns = kept_signs + ([p137.OTHER] if other_tokens else [])
    col_index = {s: j for j, s in enumerate(kept_signs)}
    other_idx = len(kept_signs) if other_tokens else None
    assert [len(eligible), len(columns)] == \
        committed137["table_dimensions"], (len(eligible), len(columns))

    site_index = {s: j for j, s in enumerate(eligible)}
    table = [[0] * len(columns) for _ in eligible]
    sparse_base = []
    for insc in analysis:
        vec: Counter = Counter()
        for tok in insc["tokens"]:
            vec[col_index.get(tok, other_idx)] += 1
        for col_idx, count in vec.items():
            table[site_index[insc["site"]]][col_idx] += count
        sparse_base.append((site_index[insc["site"]],
                            tuple(sorted(vec.items()))))
    tv_by_site = {site: dist for site, dist
                  in zip(eligible, p137.tv_distances(table))}

    # --- Covariate join (asserted, all 5,410 rows) -----
    cov_rows = json.loads(COVARIATES.read_text("utf-8"))
    cov_by_id = {r["id"]: r for r in cov_rows}
    assert len(cov_by_id) == len(cov_rows) == 5410
    for insc in analysis:
        row = cov_by_id.get(insc["id"])
        assert row is not None, f"no covariate row for id {insc['id']!r}"
        assert row["site"] == insc["site"]
        assert row["composition_stratum"] == insc["stratum"], (
            insc["id"], row["composition_stratum"], insc["stratum"])
        insc["preservation_class"] = row["preservation_class"]
        insc["chron_band"] = row["chron_band"]
        insc["depth_band"] = row["depth_band"]

    def finish(cfg: dict) -> dict:
        cfg["per_site_tv_distance_descriptive"] = tv_by_site
        cfg.pop("_table")
        return cfg

    # --- Pre-run regression (freeze section 5) ---------
    reg = finish(run_configuration(
        analysis, sparse_base, table, len(eligible),
        len(columns), lambda i: i["stratum"],
        "phase140-regression"))
    f3 = committed137
    regression_ok = (
        reg["observed_chi_square"] == f3["observed_chi_square"]
        and reg["permutation"]["count_perm_ge_observed"]
        == f3["permutation"]["count_perm_ge_observed"]
        and reg["permutation"]["permutation_median"]
        == f3["permutation"]["permutation_median"]
        and reg["permutation"]["permutation_p95_nearest_rank"]
        == f3["permutation"]["permutation_p95_nearest_rank"]
        and reg["p_value_raw"] == f3["permutation"]["p_value_raw"])
    assert regression_ok, (
        "REGRESSION FAILURE: uncontrolled configuration does "
        "not reproduce Phase-137 F3 exactly; the controlled "
        "run must not proceed (phase140-freeze.md section 5).")
    print("[phase140] regression vs Phase-137 F3: EXACT MATCH",
          flush=True)

    # --- G1 primary: composition x preservation --------
    g1 = finish(run_configuration(
        analysis, sparse_base, table, len(eligible),
        len(columns),
        lambda i: f"{i['stratum']}|{i['preservation_class']}",
        "phase140-G1"))
    p_raw = g1["p_value_raw"]
    verdict = ("SUPPORTED under control" if p_raw <= 0.05
               else "NOT SUPPORTED under control")
    g1.update({
        "role": "PRIMARY — the controlled test (G1)",
        "strata_definition": (
            "composition (Phase-137 type class x length "
            "class) x preservation (complete / fragment / "
            "damaged / UNRECORDED as a level)"),
        "primary_control_set": ["preservation"],
        "benjamini_hochberg": {
            "family": "G1 alone (adjudication Q4(b))",
            "m": 1, "q": 0.05,
            "adjusted_value": p_raw,
            "statement": (
                "BH over G1 alone at q = 0.05; with m = 1 "
                "the adjusted value equals the raw "
                "permutation p. This is NOT a family "
                "correction across the LOSO members.")},
        "verdict": verdict,
        "verdict_statement": (
            f"G1 is {verdict}: site-repertoire association "
            f"in the ICIT-lineage layer (horus84) under "
            f"permutation within composition x "
            f"preservation strata (preservation recorded "
            f"coverage 99.9%). " + CHRONOLOGY_RIDER),
    })

    # --- Sensitivity panel (EXPLORATORY) ---------------
    s_chron = finish(run_configuration(
        analysis, sparse_base, table, len(eligible),
        len(columns),
        lambda i: f"{i['stratum']}|{i['chron_band']}",
        "phase140-S-chron"))
    s_chron.update({
        "role": ("EXPLORATORY sensitivity — a bound only, "
                 "never the controlled verdict"),
        "strata_definition": ("composition x chron_band "
                              "(UNRECORDED as a level)"),
        "recorded_coverage": 2267 / 5410,
        "coverage_statement": (
            "chron_band recorded for 2,267 of 5,410 "
            "inscriptions (41.9%); the remaining 3,143 sit "
            "in UNRECORDED strata."),
    })
    s_depth = finish(run_configuration(
        analysis, sparse_base, table, len(eligible),
        len(columns),
        lambda i: f"{i['stratum']}|{i['depth_band']}",
        "phase140-S-depth"))
    s_depth.update({
        "role": ("EXPLORATORY sensitivity — a bound only, "
                 "never the controlled verdict"),
        "strata_definition": (
            "composition x depth_band (within-site "
            "relative tertiles; UNRECORDED as a level)"),
        "recorded_coverage": 2765 / 5410,
        "coverage_statement": (
            "depth_band recorded for 2,765 of 5,410 "
            "inscriptions (51.1%); the remaining 2,645 sit "
            "in UNRECORDED strata."),
    })

    result = {
        "phase": "Phase-140",
        "spec": "025",
        "test": "G1",
        "title": ("G1 — site repertoire differentiation "
                  "under preservation control, ICIT-lineage "
                  "layer (horus84); chronology NOT "
                  "controlled in the primary test"),
        "lineage_label": HEADLINE_LABEL,
        "headline_rider": CHRONOLOGY_RIDER,
        "freeze": ("specs/025-stage2-controlled-followup/"
                   "phase140-freeze.md (under "
                   "phase139-freeze.md)"),
        "input": {"path": str(HORUS84), "sha256": layer_sha},
        "covariates_input": {
            "path": "data/evidence_integration/"
                    "phase139_harmonized_covariates.json",
            "sha256": sha256_of(COVARIATES),
            "rows": len(cov_rows),
            "join": ("layer id column (unique); asserted "
                     "complete over the 5,410-row "
                     "population; composition_stratum "
                     "agreement asserted per row")},
        "anchors_sha256": sha256_of(ANCHORS),
        "parameters": {
            "B": B_PERM, "seed": SEED,
            "p_formula": "(1 + #{chi2_perm >= chi2_obs}) / (1 + B)",
            "min_sign_count": MIN_SIGN_COUNT,
            "site_inclusion": (">=30 inscriptions AND >=100 "
                               "parsed tokens (Phase-137 rule)"),
            "placeholders_excluded_from_profiles":
                sorted(PLACEHOLDERS)},
        "population": {
            "eligible_sites": eligible,
            "inscriptions": len(analysis),
            "profile_tokens": sum(len(i["tokens"]) for i in analysis),
            "parsed_tokens": sum(i["n_parsed_tokens"] for i in analysis),
            "matches_committed_phase137_f3": True},
        "table_dimensions": [len(eligible), len(columns)],
        "regression_composition_only": {
            "configuration": ("strata = composition only "
                              "(the Phase-137 F3 "
                              "configuration)"),
            "observed_chi_square": reg["observed_chi_square"],
            "permutation": reg["permutation"],
            "permutable_inscriptions":
                reg["permutable_inscriptions"],
            "matches_committed_phase137_f3_exactly": True,
            "committed_phase137_f3": {
                "observed_chi_square": f3["observed_chi_square"],
                "permutation": f3["permutation"]}},
        "g1_primary": g1,
        "sensitivity_panel_exploratory": {
            "S_chron": s_chron, "S_depth": s_depth},
        "fields_used": {
            "layer": ["id (join key only)", "site", "type",
                      "text (sign substrate)"],
            "covariates": ["preservation_class (Class O, "
                           "collapsed per Phase-139)",
                           "chron_band (Class C, "
                           "constructed)",
                           "depth_band (Class C, "
                           "constructed)"]},
        "class_i_fields_entering_nothing": [
            "class", "sanskrit", "translation", "notes"],
        "section8_language": (
            "Associations describe co-occurrence in the "
            "recorded data of this labeled lineage layer "
            "only, not meaning. No result under this spec "
            "can mint, promote, demote, or validate any "
            "sign reading, change any anchor's status, or "
            "move PRED-2026 in either direction. "
            "Harmonized covariates are constructed context "
            "(Class C); their citations and coverage travel "
            "with every number computed from them."),
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
    g1 = result["g1_primary"]
    print(f"[phase140] wrote {args.out}")
    print(f"[phase140] G1 chi2={g1['observed_chi_square']:.4f} "
          f"count_ge={g1['permutation']['count_perm_ge_observed']} "
          f"p={g1['p_value_raw']} verdict={g1['verdict']}")
    for name in ("S_chron", "S_depth"):
        s = result["sensitivity_panel_exploratory"][name]
        print(f"[phase140] {name} (EXPLORATORY) "
              f"chi2={s['observed_chi_square']:.4f} "
              f"p={s['p_value_raw']} "
              f"permutable={s['permutable_inscriptions']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
