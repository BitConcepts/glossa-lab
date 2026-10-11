"""Spec 028 — margins-only corpus audit (freeze input).

Computes population flow, per-arm population margins, cell
support, quota feasibility, and control-construction margins
for the Spec 028 freeze (Phase-393, Harappa-robustness
follow-up to Spec 027 Stage 1 / Phase-392).

NO repertoire outcome is computed: no site-by-sign
association, no between-site divergence, no permutation
statistic, and no per-sign site share appears in the output.
Pooled (whole-population) sign-frequency rankings are
margins — the same class of quantity the Phase-392 freeze
used to construct its deterministic positive-control sign
sets — and are the only sign-level quantities recorded.
A test pins the absence of outcome fields (the Phase-139
no-peeking fence pattern, as in Spec 027).

Populations are built under the adjudicated Spec 027 Ask 3
corpus rules exactly as frozen in Spec 027's stage1-freeze.md
(the Phase-392 population); Arm A is that population minus
Harappa; Arm B is that population in full; Arm C margins
concern Harappa's own cell/token counts only.

Inputs (hashes asserted):
  icit_converted_v2_keyed.json  (M77-keyed layer, Phase-115/116
      build; sha256 bbfdbcd5... as frozen in Spec 027)
  horus_inscriptions.csv        (horus84 / ICIT-lineage layer,
      sha256 c368f290... as frozen in Spec 025 / Spec 027)

Store: corpora/downloads/spec028_harappa/ (gitignored), or
$SPEC028_STORE when set.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

if os.environ.get("SPEC028_STORE"):
    STORE = Path(os.environ["SPEC028_STORE"])
else:
    STORE = (Path(__file__).resolve().parents[2]
             / "corpora" / "downloads" / "spec028_harappa")

EXPECTED_SHA256 = {
    "icit_converted_v2_keyed.json":
        "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8",
    "horus_inscriptions.csv":
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
}

# Frozen in Spec 027 stage1-freeze.md section 3 (the audit
# must reproduce these counts; the Phase-393 run asserts them
# again before computing any outcome).
PHASE392_ANALYSIS_SITES = ["Harappa", "Mohenjo-daro", "Dholavira",
                           "Lothal", "Chanhu-daro", "Kalibangan"]
ARM_A_SITES = ["Mohenjo-daro", "Dholavira", "Lothal",
               "Chanhu-daro", "Kalibangan"]
N_CELL = 49          # Phase-392 Amendment 1 rarefaction cell
MIN_SITE = 20        # Phase-392 analysis-population threshold
ARM_B_QUOTA = 52     # smallest analysis-site total (margins)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def type_class(type_value: str) -> str:
    prefix = (type_value or "").split(":")[0]
    return prefix if prefix in ("SEAL", "TAB", "POT") else "OTHER"


def build_eligible(keyed_records, horus):
    """The Phase-392 eligible population (frozen Ask 3 rules)."""
    flow = Counter()
    eligible = []
    for rec in keyed_records:
        flow["layer_records"] += 1
        if rec["status"] != "kept":
            flow[f"excluded_status_{rec['status']}"] += 1
            continue
        flow["after_dedup_kept"] += 1
        site = (rec["site"] or "").strip()
        if not site:
            flow["excluded_no_site"] += 1
            continue
        if site == "Unknown":
            flow["excluded_site_unknown"] += 1
            continue
        flow["provenanced"] += 1
        h = horus.get(rec["id"]) or {}
        if not h:
            flow["unjoined_in_horus"] += 1
        tc = type_class(rec["type"])
        if rec["type"] == "POT:T:g":
            flow["excluded_graffiti_pottg"] += 1
        if tc not in ("SEAL", "TAB"):
            flow[f"excluded_type_{tc}"] += 1
            continue
        flow["seal_tab"] += 1
        kinds = rec["kinds"]
        n_legible = sum(1 for k in kinds
                        if k in ("direct", "chain", "unmapped"))
        if n_legible < 2:
            flow["excluded_legible_lt2"] += 1
            continue
        flow["eligible_primary"] += 1
        eligible.append({
            "id": rec["id"], "site": site, "type_class": tc,
            "tokens": rec["tokens"], "kinds": kinds,
            "n_legible": n_legible,
            "complete": (h.get("complete") or "").strip(),
        })
    return eligible, dict(flow)


def composition_columns(eligible):
    """Frozen columns (Phase-392 rule): signs with >= 10 mapped
    tokens in the eligible population + UNMAPPED + OTHER."""
    counts = Counter()
    for e in eligible:
        for tok, kind in zip(e["tokens"], e["kinds"]):
            if kind in ("direct", "chain"):
                counts[tok] += 1
    frequent = sorted(s for s, c in counts.items() if c >= 10)
    return frequent + ["UNMAPPED", "OTHER"], counts


def cell_table(entries):
    cells = Counter((e["site"], e["type_class"]) for e in entries)
    return {f"{s}|{t}": n for (s, t), n in sorted(cells.items())}


def arm_margins(entries, sites, columns):
    """Margins for one arm population: counts and cell support
    only. ``entries`` are the arm's analysis records."""
    cells = cell_table(entries)
    included = {k: v for k, v in cells.items() if v >= N_CELL}
    excluded = {k: v for k, v in cells.items() if v < N_CELL}
    site_totals = Counter(e["site"] for e in entries)
    # LOSO cell support: included-cell count after each drop.
    loso_cells = {}
    for dropped in sites:
        rest = [e for e in entries if e["site"] != dropped]
        rest_cells = cell_table(rest)
        loso_cells[dropped] = {
            "cells_ge_cell": sum(1 for v in rest_cells.values()
                                 if v >= N_CELL),
            "records": len(rest),
        }
    s_complete = [e for e in entries if e["complete"] != "N"]
    sc_cells = cell_table(s_complete)
    return {
        "sites": sites,
        "records": len(entries),
        "site_totals": {s: site_totals[s] for s in sites},
        "cells": cells,
        "cells_included_ge49": included,
        "cells_excluded_lt49": excluded,
        "n_cells_included": len(included),
        "inscriptions_per_draw": N_CELL * len(included),
        "loso_support": loso_cells,
        "s_complete_records": len(s_complete),
        "s_complete_cells_ge49": sum(
            1 for v in sc_cells.values() if v >= N_CELL),
    }


def pooled_ranking(eligible_subset, columns):
    """Pooled sign-frequency ranking over a population subset
    (a margin). Returns the deterministic positive-control
    sign sets: disjoint blocks of 10 from the 60 most
    frequent mapped sign columns."""
    counts = Counter()
    for e in eligible_subset:
        for tok, kind in zip(e["tokens"], e["kinds"]):
            if kind in ("direct", "chain"):
                counts[tok] += 1
    mapped_cols = [c for c in columns
                   if c not in ("UNMAPPED", "OTHER")]
    by_freq = sorted(mapped_cols, key=lambda c: -counts[c])[:60]
    return by_freq, counts


def main() -> int:
    keyed_path = STORE / "icit_converted_v2_keyed.json"
    horus_path = STORE / "horus_inscriptions.csv"
    hashes = {p.name: sha256_file(p) for p in (keyed_path, horus_path)}
    for name, expected in EXPECTED_SHA256.items():
        assert hashes[name] == expected, (name, hashes[name])

    keyed = json.loads(keyed_path.read_text(encoding="utf-8"))
    records = keyed["inscriptions"]
    horus = {}
    with open(horus_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            horus[row["id"]] = row

    eligible, flow = build_eligible(records, horus)
    columns, _sign_counts = composition_columns(eligible)
    site_counts = Counter(e["site"] for e in eligible)
    analysis = [e for e in eligible
                if site_counts[e["site"]] >= MIN_SITE]
    assert sorted({e["site"] for e in analysis}) == sorted(
        PHASE392_ANALYSIS_SITES)
    assert len(analysis) == 3030  # Phase-392 frozen margin

    arm_a = [e for e in analysis if e["site"] != "Harappa"]
    arm_a_eligible = [e for e in eligible if e["site"] != "Harappa"]
    harappa = [e for e in analysis if e["site"] == "Harappa"]

    # Arm A margins + its own pooled ranking (control sets).
    margins_a = arm_margins(arm_a, ARM_A_SITES, columns)
    top60_a, _ = pooled_ranking(arm_a_eligible, columns)
    control_sets_a = {
        site: sorted(top60_a[10 * k:10 * k + 10])
        for k, site in enumerate(ARM_A_SITES)}

    # Arm B margins: full population, equal quota feasibility.
    site_totals_b = {s: site_counts[s] for s in PHASE392_ANALYSIS_SITES
                     if site_counts[s] >= MIN_SITE}
    # (analysis site totals, not eligible: quota draws from the
    # analysis population)
    site_totals_b = {s: sum(1 for e in analysis if e["site"] == s)
                     for s in PHASE392_ANALYSIS_SITES}
    top60_b, _ = pooled_ranking(eligible, columns)
    control_sets_b = {
        site: sorted(top60_b[10 * k:10 * k + 10])
        for k, site in enumerate(PHASE392_ANALYSIS_SITES)}
    loso_quota_ok = {}
    for dropped in PHASE392_ANALYSIS_SITES:
        rest = [v for s, v in site_totals_b.items() if s != dropped]
        loso_quota_ok[dropped] = bool(rest and min(rest) >= ARM_B_QUOTA)

    # Arm C margins: Harappa counts only (no composition).
    harappa_tokens = Counter()
    for e in harappa:
        harappa_tokens[e["type_class"]] += e["n_legible"]

    out = {
        "audit": "spec028-margins-only",
        "outcome_fields_present": False,
        "input_hashes": hashes,
        "population_flow": flow,
        "eligible_records": len(eligible),
        "sign_columns": len(columns),
        "signs_ge10_tokens": len(columns) - 2,
        "analysis_population": {
            "records": len(analysis),
            "sites": PHASE392_ANALYSIS_SITES,
            "cells": cell_table(analysis),
        },
        "arm_a_harappa_excluded": dict(
            margins_a,
            positive_control_sign_sets=control_sets_a,
            pooled_top60_source=(
                "pooled mapped-token frequency over the Arm A "
                "eligible population (eligible records at the "
                "five non-Harappa analysis sites)")),
        "arm_b_site_equal": {
            "sites": PHASE392_ANALYSIS_SITES,
            "records": len(analysis),
            "site_totals": site_totals_b,
            "quota_per_site": ARM_B_QUOTA,
            "quota_is_min_site_total": (
                ARM_B_QUOTA == min(site_totals_b.values())),
            "inscriptions_per_draw": ARM_B_QUOTA * 6,
            "loso_quota_feasible": loso_quota_ok,
            "positive_control_sign_sets": control_sets_b,
            "pooled_top60_source": (
                "pooled mapped-token frequency over the full "
                "eligible population (the Phase-392 ranking)"),
        },
        "arm_c_harappa_counts": {
            "records": len(harappa),
            "cells": cell_table(harappa),
            "legible_tokens_by_type": dict(harappa_tokens),
            "share_of_analysis_records": round(
                len(harappa) / len(analysis), 4),
        },
    }
    text = json.dumps(out, indent=1)
    print(text)
    out_path = os.environ.get("SPEC028_AUDIT_OUT")
    if out_path:
        Path(out_path).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
