#!/usr/bin/env python3
"""Phase-136 (spec 024, FROZEN Stage 2(a); family member F1) —
terminal-class x object type, within-site stratified permutation
test on the ICIT-lineage (horus84) joined subset.

Implements specs/024-evidence-integration/stage2a-freeze.md exactly:

- Join: Phase-133 exact-string rule — a horus84 row joins iff its
  ``cisi`` value is a printed catalogue ID in exactly one CISI
  volume (printed-ID sets derived from the catalogue ``cisi_id``
  column of each volume). Ambiguous and unmatched rows are
  excluded and counted.
- The joined object's catalogue ``object_type`` (Class O) is the
  filled value on its catalogue rows (per-object view, first
  non-empty wins — the Phase-133 pattern; the freeze audit found
  no joined object with conflicting filled types).
- Population restricted to object types {Seals, Tablets}.
- Sequence parse (Phase-115 convention for this lineage):
  ``re.findall(r"\\d{3}", text)`` in recorded order; terminal =
  last code. Placeholder codes ``000``/``999`` -> UNK.
- Terminal mapping by the frozen machinery ONLY:
  ``glossa_lab.pred_harness.build_sign_maps`` +
  ``SignMapper.map_w`` over
  ``data/crosswalks/canonical_sign_registry.csv``. This script
  imports ONLY that mapping machinery — it never imports/calls
  ``evaluate``, ``dry_run``, or any PRED scoring; no output of
  this phase is an input to the PRED harness (freeze section 2).
- Outcome: terminal mapped P sign in TERMINAL14 (spec 018
  section 3 list, freeze section 4) vs not.
- Strata: horus84 ``site`` (Class O). Eligible iff analysis-
  population N >= 20 and >= 5 Seals and >= 5 Tablets.
- Estimability (freeze section 5): >= 2 eligible strata AND the
  pooled 2x2 expected counts >= 5 in at least 80% of its 4 cells.
- Statistic: Cochran-Mantel-Haenszel chi-square (no continuity
  correction). Null distribution: within-stratum permutation of
  object-type labels, B = 9,999, seed 20261009, Python stdlib
  ``random.Random(20261009)`` (Fisher-Yates via ``shuffle``),
  p = (1 + #{perm >= obs}) / (1 + B).
- Effect sizes (freeze section 6): Mantel-Haenszel common odds
  ratio with Robins-Breslow-Greenland 95% CI; crude
  (unstratified) odds ratio, labeled uncontrolled; per-stratum
  odds ratios; TERMINAL14 shares by type per stratum and pooled.

Class I fields (horus84 ``class``/``sanskrit``/``translation``/
``notes``) enter NOTHING (freeze section 0). The horus84 ``text``
field is used only as the text substrate (the inscriptions
themselves, as transcribed by their compilers), never as context
evidence.

Inputs live in the local store (never committed); every input
path + sha256 is recorded in the results JSON. Deterministic:
the permutation stream is fully seeded; no wall-clock values are
written into the results JSON (progress/deadline prints go to
stdout only, governance H9/H11).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

# Frozen machinery ONLY (mapping). Never evaluate / dry_run / PRED.
from glossa_lab.pred_harness import SignMapper, build_sign_maps  # noqa: E402

MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"
HORUS84 = (Path.home() / "workspace" / "research_notes"
           / "indus-data-deep-sweep-20261008" / "downloads"
           / "horus84-computational-linguistics" / "data"
           / "inscriptions.csv")
REGISTRY = REPO / "data" / "crosswalks" / "canonical_sign_registry.csv"
DEFAULT_OUT = REPO / "reports" / "phase136_results.json"

TERMINAL14 = frozenset({
    "P020", "P076", "P095", "P099", "P108", "P125", "P210",
    "P226", "P256", "P346", "P359", "P378", "P384", "P385",
})
PLACEHOLDERS = {"000", "999"}
B_PERM = 9_999
SEED = 20261009
DEADLINE_SECONDS = 1800


def catalogue_dir() -> Path:
    """Worktree catalogue if populated, else the main checkout's
    (Phase-115 downloads-resolution pattern)."""
    for cand in (REPO / "corpora" / "downloads" / "cisi_image_layer"
                 / "catalogue",
                 MAIN_CHECKOUT / "corpora" / "downloads"
                 / "cisi_image_layer" / "catalogue"):
        if (cand / "cisi_vol1_catalogue.csv").exists():
            return cand
    raise FileNotFoundError(
        "cisi catalogue not found in worktree or main checkout")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Statistics (pure functions; unit-tested on hand-checkable tables)
# Table convention per stratum: a = Seals & TERMINAL14,
# b = Seals & not, c = Tablets & TERMINAL14, d = Tablets & not.
# ---------------------------------------------------------------------------

def cmh_statistic(tables: list[dict]) -> float:
    """Cochran-Mantel-Haenszel chi-square, no continuity
    correction."""
    num = 0.0
    den = 0.0
    for t in tables:
        a, b, c, d = t["a"], t["b"], t["c"], t["d"]
        n = a + b + c + d
        if n <= 1:
            continue
        n1, n2 = a + b, c + d
        m1, m2 = a + c, b + d
        expected = n1 * m1 / n
        var = n1 * n2 * m1 * m2 / (n * n * (n - 1))
        num += a - expected
        den += var
    if den == 0.0:
        return 0.0
    return num * num / den


def mh_odds_ratio(tables: list[dict]) -> dict:
    """Mantel-Haenszel common OR with Robins-Breslow-Greenland
    variance on the log scale and a 95% CI."""
    sum_r = sum(t["a"] * t["d"] / (t["a"] + t["b"] + t["c"] + t["d"])
                for t in tables)
    sum_s = sum(t["b"] * t["c"] / (t["a"] + t["b"] + t["c"] + t["d"])
                for t in tables)
    if sum_r == 0.0 or sum_s == 0.0:
        return {"common_odds_ratio": None, "log_or": None,
                "var_log_or": None, "ci95": None}
    or_mh = sum_r / sum_s
    term1 = term2 = term3 = 0.0
    for t in tables:
        a, b, c, d = t["a"], t["b"], t["c"], t["d"]
        n = a + b + c + d
        p_k = (a + d) / n
        q_k = (b + c) / n
        r_k = a * d / n
        s_k = b * c / n
        term1 += p_k * r_k
        term2 += p_k * s_k + q_k * r_k
        term3 += q_k * s_k
    var = (term1 / (2 * sum_r ** 2)
           + term2 / (2 * sum_r * sum_s)
           + term3 / (2 * sum_s ** 2))
    log_or = math.log(or_mh)
    half = 1.96 * math.sqrt(var)
    return {"common_odds_ratio": or_mh, "log_or": log_or,
            "var_log_or": var,
            "ci95": [math.exp(log_or - half), math.exp(log_or + half)]}


def odds_ratio(a: int, b: int, c: int, d: int) -> float | None:
    """Plain 2x2 odds ratio (a*d)/(b*c); None when undefined
    (a zero denominator cell), +inf when only the numerator
    cross-product is nonzero."""
    if b * c == 0:
        return None if a * d == 0 else float("inf")
    return (a * d) / (b * c)


def crude_odds_ratio(tables: list[dict]) -> dict:
    """Pooled (unstratified) OR with a Wald log-scale 95% CI.
    Labeled uncontrolled wherever reported."""
    a = sum(t["a"] for t in tables)
    b = sum(t["b"] for t in tables)
    c = sum(t["c"] for t in tables)
    d = sum(t["d"] for t in tables)
    or_crude = odds_ratio(a, b, c, d)
    ci = None
    if or_crude and math.isfinite(or_crude) and min(a, b, c, d) > 0:
        se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
        log_or = math.log(or_crude)
        ci = [math.exp(log_or - 1.96 * se), math.exp(log_or + 1.96 * se)]
    return {"odds_ratio": or_crude, "ci95_wald": ci,
            "label": "uncontrolled (unstratified)"}


def table_from_counts(n_seals: int, n_tablets: int,
                      seals_terminal: int,
                      tablets_terminal: int) -> dict:
    return {"a": seals_terminal, "b": n_seals - seals_terminal,
            "c": tablets_terminal, "d": n_tablets - tablets_terminal}


def permutation_test(strata: list[dict], b_perm: int = B_PERM,
                     seed: int = SEED,
                     deadline_seconds: int = DEADLINE_SECONDS) -> dict:
    """Within-stratum permutation of object-type labels.

    ``strata``: [{site, outcomes: [bool,...] (TERMINAL14 membership,
    fixed), n_seals: int}] — the type-label multiset per stratum is
    fixed by n_seals / (N - n_seals); labels are shuffled with
    ``random.Random(seed)`` (Fisher-Yates via ``shuffle``).
    Progress prints every 1,000 permutations; a deadline aborts
    loudly rather than silently truncating (H9/H11).
    """
    import random

    def tables_for(labelings):
        tables = []
        for stratum, labels in zip(strata, labelings):
            outcomes = stratum["outcomes"]
            a = sum(1 for lab, out in zip(labels, outcomes)
                    if lab == "Seals" and out)
            c = sum(1 for lab, out in zip(labels, outcomes)
                    if lab == "Tablets" and out)
            tables.append(table_from_counts(
                stratum["n_seals"],
                len(outcomes) - stratum["n_seals"], a, c))
        return tables

    observed_tables = tables_for(
        [[("Seals" if i < s["n_seals"] else "Tablets")
          for i in range(len(s["outcomes"]))] for s in strata])
    # NOTE: the observed labeling above is a canonical arrangement;
    # the observed statistic is computed from the strata's own
    # terminal counts, which the caller guarantees match it.
    obs = cmh_statistic(observed_tables)
    rng = random.Random(seed)
    perm_stats: list[float] = []
    ge = 0
    start = time.monotonic()
    for i in range(1, b_perm + 1):
        labelings = []
        for s in strata:
            labels = (["Seals"] * s["n_seals"]
                      + ["Tablets"] * (len(s["outcomes"]) - s["n_seals"]))
            rng.shuffle(labels)
            labelings.append(labels)
        stat = cmh_statistic(tables_for(labelings))
        perm_stats.append(stat)
        if stat >= obs:
            ge += 1
        if i % 1000 == 0:
            elapsed = time.monotonic() - start
            print(f"[phase136] permutations {i}/{b_perm} "
                  f"elapsed {elapsed:.1f}s ge={ge}", flush=True)
            if elapsed > deadline_seconds:
                raise TimeoutError(
                    f"permutation deadline {deadline_seconds}s "
                    f"exceeded at permutation {i}")
    perm_sorted = sorted(perm_stats)
    median = perm_sorted[len(perm_sorted) // 2]
    p95 = perm_sorted[int(0.95 * (len(perm_sorted) - 1))]
    return {"statistic_observed": obs, "b": b_perm, "seed": seed,
            "n_perm_ge_observed": ge,
            "p_value": (1 + ge) / (1 + b_perm),
            "perm_stat_median": median, "perm_stat_p95": p95}


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build(out_path: Path) -> dict:
    cat_dir = catalogue_dir()
    inputs: dict[str, dict] = {}

    def register(key: str, path: Path) -> Path:
        inputs[key] = {"path": str(path), "exists": path.exists(),
                       "sha256": sha256_of(path) if path.exists() else None,
                       "bytes": path.stat().st_size if path.exists() else None}
        return path

    vol_paths = {vol: register(f"cisi_vol{vol}_catalogue",
                               cat_dir / f"cisi_vol{vol}_catalogue.csv")
                 for vol in (1, 2)}
    horus_path = register("horus84_inscriptions", HORUS84)
    registry_path = register("canonical_sign_registry", REGISTRY)

    # Catalogue printed-ID sets per volume + per-object view.
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

    # Join (Phase-133 exact-string rule).
    matched = ambiguous = unmatched = 0
    typed: Counter = Counter()
    untyped = 0
    joined: list[tuple[dict, dict]] = []
    concordant = discordant = 0
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
        if obj["site"] == r["site"]:
            concordant += 1
        else:
            discordant += 1
        if obj["object_type"]:
            typed[obj["object_type"]] += 1
        else:
            untyped += 1

    restricted = [(r, o) for r, o in joined
                  if o["object_type"] in ("Seals", "Tablets")]

    # Terminal mapping (frozen machinery only).
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

    # Strata + eligibility (freeze section 3 step 7).
    by_site: dict[str, list] = defaultdict(list)
    for site, otype, is_term in analysis:
        by_site[site].append((otype, is_term))
    strata_rows = []
    eligible: list[dict] = []
    for site in sorted(by_site, key=lambda s: (-len(by_site[s]), s)):
        rows = by_site[site]
        n_seals = sum(1 for t, _ in rows if t == "Seals")
        n_tablets = len(rows) - n_seals
        is_eligible = len(rows) >= 20 and n_seals >= 5 and n_tablets >= 5
        a = sum(1 for t, out in rows if t == "Seals" and out)
        c = sum(1 for t, out in rows if t == "Tablets" and out)
        table = table_from_counts(n_seals, n_tablets, a, c)
        _or = odds_ratio(table["a"], table["b"],
                         table["c"], table["d"])
        row = {"site": site, "n": len(rows), "n_seals": n_seals,
               "n_tablets": n_tablets, "eligible": is_eligible,
               "table": table,
               "odds_ratio": (_or if _or is not None
                              and math.isfinite(_or) else None),
               "odds_ratio_note": (
                   None if _or is not None and math.isfinite(_or)
                   else "undefined: zero cell in the stratum 2x2 "
                        "table (descriptive stratum only)"),
               "terminal14_share_seals": (a / n_seals if n_seals else None),
               "terminal14_share_tablets": (c / n_tablets if n_tablets else None),
               "terminal14_share": ((a + c) / len(rows) if rows else None)}
        strata_rows.append(row)
        if is_eligible:
            # Outcomes in file order; seals-first canonical labeling
            # reproduces the observed table because outcomes are
            # regrouped: seals' outcomes first, then tablets'.
            outcomes = ([out for t, out in rows if t == "Seals"]
                        + [out for t, out in rows if t == "Tablets"])
            eligible.append({"site": site, "n_seals": n_seals,
                             "outcomes": outcomes, "table": table})

    eligible_tables = [e["table"] for e in eligible]
    pooled = {k: sum(t[k] for t in eligible_tables) for k in "abcd"}
    pooled_n = sum(pooled.values())
    row_totals = [pooled["a"] + pooled["b"], pooled["c"] + pooled["d"]]
    col_totals = [pooled["a"] + pooled["c"], pooled["b"] + pooled["d"]]
    expected = [row_totals[0] * col_totals[0] / pooled_n,
                row_totals[0] * col_totals[1] / pooled_n,
                row_totals[1] * col_totals[0] / pooled_n,
                row_totals[1] * col_totals[1] / pooled_n]
    frac_ge5 = sum(1 for e in expected if e >= 5) / 4
    estimable = len(eligible) >= 2 and frac_ge5 >= 0.8

    result: dict = {
        "phase": "Phase-136",
        "spec": "024",
        "stage": "Stage 2(a)",
        "family_member": "F1",
        "title": ("Terminal-class x object type, within-site "
                  "stratified permutation test — ICIT-lineage "
                  "(horus84) joined subset"),
        "lineage_label": "ICIT-lineage (horus84)",
        "lineage_sentence": ("results describe this lineage layer's "
                             "joined subset, not the Indus corpus "
                             "in general."),
        "freeze": "specs/024-evidence-integration/stage2a-freeze.md",
        "inputs": inputs,
        "parameters": {"B": B_PERM, "seed": SEED,
                       "p_formula": "(1 + #{perm >= obs}) / (1 + B)",
                       "statistic": ("Cochran-Mantel-Haenszel "
                                     "chi-square, no continuity "
                                     "correction"),
                       "terminal14": sorted(TERMINAL14)},
        "flow": {
            "layer_rows": len(horus_rows),
            "matched_single_volume": matched,
            "ambiguous": ambiguous,
            "unmatched": unmatched,
            "unjoinable_or_ambiguous": ambiguous + unmatched,
            "unjoinable_or_ambiguous_share":
                (ambiguous + unmatched) / len(horus_rows),
            "typed_filled": sum(typed.values()),
            "typed_by_type": dict(sorted(typed.items())),
            "untyped": untyped,
            "restricted_seals_tablets": len(restricted),
            "excluded_graffiti": typed.get("Graffiti", 0),
            "excluded_objects": typed.get("Objects", 0),
            "terminal_mapped": mapped,
            "terminal_unk": unk_terminal,
            "terminal_no_codes": no_codes,
            "terminal14_margin_among_mapped": terminal14_margin,
            "analysis_population_all_strata": len(analysis),
            "analysis_population_eligible_strata":
                sum(e["table"]["a"] + e["table"]["b"] + e["table"]["c"]
                    + e["table"]["d"] for e in eligible),
        },
        "catalogue_site_concordance_joined": {
            "concordant": concordant, "discordant": discordant,
            "note": ("Descriptive only (freeze section 4); horus84 "
                     "site vs the joined catalogue object's site. "
                     "Not a variable.")},
        "strata": strata_rows,
        "eligible_strata": [e["site"] for e in eligible],
        "pooled_table_eligible": pooled,
        "pooled_expected_counts": expected,
        "estimability": {
            "n_eligible_strata": len(eligible),
            "fraction_expected_ge_5": frac_ge5,
            "rule": ("freeze section 5: >=2 eligible strata AND "
                     "pooled expected counts >=5 in >=80% of cells"),
            "estimable": estimable,
            "verdict": "ESTIMABLE" if estimable else "NOT ESTIMABLE"},
        "effect_sizes": {},
        "test": None,
        "section8_language": (
            "Associations describe use, not meaning. No result "
            "under this spec can mint, promote, demote, or validate "
            "any sign reading, change any anchor's status, or move "
            "PRED-2026 in either direction."),
        "ai_disclosure": ("Produced by an AI agent (Muse Spark, "
                          "via Muse) at the direction of Tristen "
                          "Pierson, per constitution section VI."),
    }

    if eligible_tables:
        mh = mh_odds_ratio(eligible_tables)
        result["effect_sizes"] = {
            "mh_common_odds_ratio": mh["common_odds_ratio"],
            "mh_log_or": mh["log_or"],
            "mh_var_log_or_rbg": mh["var_log_or"],
            "mh_ci95": mh["ci95"],
            "crude_odds_ratio_uncontrolled": crude_odds_ratio(
                eligible_tables),
            "per_stratum_odds_ratios": {
                e["site"]: (
                    lambda v: v if v is not None and math.isfinite(v)
                    else None)(
                    odds_ratio(e["table"]["a"], e["table"]["b"],
                               e["table"]["c"], e["table"]["d"]))
                for e in eligible},
            "pooled_terminal14_shares": {
                "seals": (pooled["a"] / (pooled["a"] + pooled["b"])
                          if pooled["a"] + pooled["b"] else None),
                "tablets": (pooled["c"] / (pooled["c"] + pooled["d"])
                            if pooled["c"] + pooled["d"] else None)},
        }

    if estimable:
        # Observed statistic from the eligible tables directly.
        obs = cmh_statistic(eligible_tables)
        perm = permutation_test(eligible)
        assert abs(perm["statistic_observed"] - obs) < 1e-9, (
            perm["statistic_observed"], obs)
        result["test"] = {
            "statistic_observed": obs, "B": perm["b"],
            "seed": perm["seed"],
            "n_perm_ge_observed": perm["n_perm_ge_observed"],
            "raw_p": perm["p_value"],
            "perm_stat_median": perm["perm_stat_median"],
            "perm_stat_p95": perm["perm_stat_p95"],
            "verdict_word": ("DEFERRED — assigned only after the "
                             "family Benjamini-Hochberg correction "
                             "(q = 0.05) in the combined Stage 2 "
                             "report (freeze sections 1-2)."),
        }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=False)
                        + "\n", encoding="utf-8")
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args(argv)
    result = build(args.out)
    print(f"[phase136] wrote {args.out}")
    print(f"[phase136] flow: {json.dumps(result['flow'])}")
    print(f"[phase136] estimability: {result['estimability']}")
    if result["test"]:
        print(f"[phase136] CMH={result['test']['statistic_observed']:.6f} "
              f"raw p={result['test']['raw_p']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
