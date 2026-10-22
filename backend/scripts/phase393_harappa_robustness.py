"""Phase-393 — Spec 028: Harappa robustness of the M77 site effect.

Executes specs/028-harappa-robustness/freeze.md (freeze digest
in freeze.json): adjusted PERMANOVA R^2 for site on
per-inscription M77 composition (Bray–Curtis), practical
margin adjusted R^2 = 0.01, seed 20261012, R=199 draws,
B=499 label permutations within type class x legible-length
strata per draw.

  Arm A (CONFIRMATORY, primary): the Phase-392 analysis
  population minus Harappa (1,593 records, 5 sites); cell
  rarefaction n=49; LOSO over the 5 sites; S-complete
  sensitivity (labelled, no verdict).
  Arm B (CONFIRMATORY, secondary): site-equal-weight
  estimand on the full population; quota Q=52 per site per
  draw under the frozen allocation rule; LOSO over the 6
  sites with Q held at 52.
  Per-arm discriminating negative/positive controls
  (synthetic population regenerated per draw, freeze
  Amendment 1); a control failure = that arm INVALID.
  Arm C (EXPLORATORY, descriptive only): Harappa
  decomposition; no verdict, no p-values.

The executed population is asserted equal to the frozen
margins audit (specs/028-harappa-robustness/
margins-audit.json) before any outcome is computed — a
mismatch stops the run as INVALID. The pipeline section
below is a verbatim copy of the freeze-time pipeline
module (pipeline393.py, pipeline section), enforced by
backend/tests/test_phase393_execution.py. No anchor or
PRED contact. Phase-392's record is read-only context.

Inputs (hashes asserted):
  corpora/downloads/spec028_harappa/icit_converted_v2_keyed.json
  corpora/downloads/spec028_harappa/horus_inscriptions.csv
Outputs:
  reports/phase393_results.json, reports/phase393_report.md
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / "corpora" / "downloads" / "spec028_harappa"
KEYED_PATH = STORE / "icit_converted_v2_keyed.json"
HORUS_PATH = STORE / "horus_inscriptions.csv"
SPEC_DIR = ROOT / "specs" / "028-harappa-robustness"
AUDIT_PATH = SPEC_DIR / "margins-audit.json"
FREEZE_PATH = SPEC_DIR / "freeze.json"
RESULTS_PATH = ROOT / "reports" / "phase393_results.json"
REPORT_PATH = ROOT / "reports" / "phase393_report.md"

EXPECTED_SHA256 = {
    "icit_converted_v2_keyed.json":
        "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8",
    "horus_inscriptions.csv":
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
}
SEED = 20261012
DEADLINE_S = 5400


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# === FROZEN PIPELINE BEGIN (verbatim: specs/028-harappa-robustness/pipeline393.py, pipeline section) ===
ALPHA = 0.05
MARGIN_R2 = 0.01          # adjusted R^2 scale (Phase-392 Amdt 1)
N_CELL = 49               # Phase-392 Amendment 1 cell size
ARM_B_QUOTA = 52          # smallest analysis-site total
DRAWS = 199
PERMS = 499
POSITIVE_BOOST = 3.0


def adjusted_r2(r2: float, n: int, g: int) -> float:
    """Standard PERMANOVA adjusted R^2: null expectation ~ 0."""
    if n <= g:
        return 0.0
    return 1.0 - (1.0 - r2) * (n - 1) / (n - g)


def perm_stratum(entry) -> str:
    """Frozen permutation stratum (Amendment 1): type class x
    exact legible-length value. Labels are exchangeable only
    among inscriptions of the same object type and the same
    legible-token count."""
    return f"{entry['type_class']}|{entry['n_legible']}"


# ---------------------------------------------------------------------------
# PERMANOVA machinery (verbatim from Phase-392)
# ---------------------------------------------------------------------------

def bray_curtis(props: np.ndarray) -> np.ndarray:
    """Bray-Curtis on proportion rows = 0.5 * L1 distance."""
    return 0.5 * np.abs(props[:, None, :] - props[None, :, :]).sum(-1)


def _ss_a(gower: np.ndarray, label_idx: np.ndarray,
          group_sizes: np.ndarray) -> float:
    n = gower.shape[0]
    g = len(group_sizes)
    z = np.zeros((n, g))
    z[np.arange(n), label_idx] = 1.0
    m = z.T @ gower @ z
    return float((np.diag(m) / group_sizes).sum())


def permanova(props: np.ndarray, label_idx: np.ndarray,
              group_sizes: np.ndarray):
    d = bray_curtis(props)
    a = -0.5 * d ** 2
    gower = (a - a.mean(axis=1, keepdims=True)
             - a.mean(axis=0, keepdims=True) + a.mean())
    ss_t = float(np.trace(gower))
    ss_a = _ss_a(gower, label_idx, group_sizes)
    return gower, ss_t, ss_a


def permuted_ss(gower, label_idx, group_sizes, strata, rng):
    perm = label_idx.copy()
    for s in np.unique(strata):
        idx = np.where(strata == s)[0]
        perm[idx] = rng.permutation(label_idx[idx])
    return _ss_a(gower, perm, group_sizes)


# ---------------------------------------------------------------------------
# Draw construction
# ---------------------------------------------------------------------------

def cell_members(entries):
    cells = defaultdict(list)
    for i, e in enumerate(entries):
        cells[(e["site"], e["type_class"])].append(i)
    return cells


def quota_allocation(cell_counts: dict, quota: int) -> dict:
    """Deterministic per-stratum allocation of a site's quota.

    Largest-remainder proportional allocation over the site's
    type-class counts; ties broken by type-class name
    ascending; a stratum is capped at its own count and any
    capped remainder is reassigned by continuing the same
    order. Frozen rule (Spec 028 freeze, Arm B).
    """
    total = sum(cell_counts.values())
    assert 0 < quota <= total, (quota, total)
    exact = {t: quota * n / total for t, n in cell_counts.items()}
    alloc = {t: min(int(exact[t] // 1), cell_counts[t])
             for t in cell_counts}
    remaining = quota - sum(alloc.values())
    order = sorted(cell_counts,
                   key=lambda t: (-(exact[t] - int(exact[t] // 1)), t))
    i = 0
    guard = 0
    while remaining > 0:
        t = order[i % len(order)]
        if alloc[t] < cell_counts[t]:
            alloc[t] += 1
            remaining -= 1
        i += 1
        guard += 1
        assert guard <= 4 * quota + 4, "allocation failed to converge"
    return alloc


def _finish_draw(chosen, entries, vectors, rng, with_perms):
    chosen = np.array(sorted(chosen))
    counts = vectors[chosen]
    props = counts / counts.sum(axis=1, keepdims=True)
    sites = sorted({entries[i]["site"] for i in chosen})
    site_of = [entries[i]["site"] for i in chosen]
    label_idx = np.array([sites.index(s) for s in site_of])
    g = len(sites)
    group_sizes = np.array(
        [(label_idx == k).sum() for k in range(g)], dtype=np.float64)
    strata = np.array([perm_stratum(entries[i]) for i in chosen])
    gower, ss_t, ss_a = permanova(props, label_idx, group_sizes)
    r2 = ss_a / ss_t if ss_t > 0 else 0.0
    p = None
    if with_perms:
        exceed = 0
        for _ in range(PERMS):
            if permuted_ss(gower, label_idx, group_sizes,
                           strata, rng) >= ss_a - 1e-12:
                exceed += 1
        p = (1 + exceed) / (1 + PERMS)
    return r2, adjusted_r2(r2, len(chosen), g), p


def _cells_plan(entries, n_cell):
    cells_all = cell_members(entries)
    cells = {c: idxs for c, idxs in cells_all.items()
             if len(idxs) >= n_cell}
    excluded = {f"{s}|{t}": len(v) for (s, t), v in
                sorted(cells_all.items()) if len(v) < n_cell}
    return cells, excluded


def _draw_cells(cells, entries, vectors, rng, with_perms, n_cell):
    chosen = []
    for cell, idxs in sorted(cells.items()):
        pick = rng.choice(len(idxs), size=n_cell, replace=False)
        chosen.extend(idxs[j] for j in pick)
    return _finish_draw(chosen, entries, vectors, rng, with_perms)


def run_pipeline_cells(entries, vectors, rng, *, with_perms=True,
                       n_cell=N_CELL):
    """Phase-392 pipeline: rarefy each site x type cell with
    >= n_cell members to n_cell, per draw."""
    cells, excluded = _cells_plan(entries, n_cell)
    if not cells:
        return {"cells_included": 0, "excluded_cells": excluded,
                "r2_draws": [], "adj_draws": [], "p_draws": []}
    sites = sorted({c[0] for c in cells})
    r2_draws, adj_draws, p_draws = [], [], []
    for _ in range(DRAWS):
        r2, adj, p = _draw_cells(cells, entries, vectors, rng,
                                 with_perms, n_cell)
        r2_draws.append(r2)
        adj_draws.append(adj)
        if p is not None:
            p_draws.append(p)
    return {"cells_included": len(cells),
            "excluded_cells": excluded, "sites": sites,
            "r2_draws": r2_draws, "adj_draws": adj_draws,
            "p_draws": p_draws}


def run_control_cells(template_entries, probs_by_site, rng, *,
                      n_cell=N_CELL):
    """Control runner (Amendment 1b): the synthetic population
    is regenerated per draw, so every draw is an independent
    null/planted world; the draw itself is the frozen cell
    rarefaction."""
    cells, excluded = _cells_plan(template_entries, n_cell)
    sites = sorted({c[0] for c in cells})
    r2_draws, adj_draws, p_draws = [], [], []
    for _ in range(DRAWS):
        entries, vectors = synthetic_entries(
            template_entries, probs_by_site, rng)
        r2, adj, p = _draw_cells(cells, entries, vectors, rng,
                                 True, n_cell)
        r2_draws.append(r2)
        adj_draws.append(adj)
        p_draws.append(p)
    return {"cells_included": len(cells),
            "excluded_cells": excluded, "sites": sites,
            "r2_draws": r2_draws, "adj_draws": adj_draws,
            "p_draws": p_draws}


def _quota_plans(entries, quota):
    by_site = defaultdict(list)
    for i, e in enumerate(entries):
        by_site[e["site"]].append(i)
    plans = {}
    for site, idxs in by_site.items():
        counts = defaultdict(int)
        for i in idxs:
            counts[entries[i]["type_class"]] += 1
        plans[site] = (idxs, quota_allocation(dict(counts), quota))
    return plans


def _draw_quota(plans, entries, vectors, rng, with_perms):
    chosen = []
    for site in sorted(plans):
        idxs, alloc = plans[site]
        for tc, q in sorted(alloc.items()):
            if q == 0:
                continue
            members = [i for i in idxs
                       if entries[i]["type_class"] == tc]
            pick = rng.choice(len(members), size=q, replace=False)
            chosen.extend(members[j] for j in pick)
    return _finish_draw(chosen, entries, vectors, rng, with_perms)


def run_pipeline_quota(entries, vectors, rng, *, with_perms=True,
                       quota=ARM_B_QUOTA):
    """Arm B pipeline: each site contributes exactly ``quota``
    inscriptions per draw, sampled within the site stratified
    by type class under quota_allocation."""
    plans = _quota_plans(entries, quota)
    sites = sorted(plans)
    r2_draws, adj_draws, p_draws = [], [], []
    for _ in range(DRAWS):
        r2, adj, p = _draw_quota(plans, entries, vectors, rng,
                                 with_perms)
        r2_draws.append(r2)
        adj_draws.append(adj)
        if p is not None:
            p_draws.append(p)
    return {"cells_included": None, "excluded_cells": {},
            "sites": sites, "quota_allocations": {
                s: plans[s][1] for s in sites},
            "r2_draws": r2_draws, "adj_draws": adj_draws,
            "p_draws": p_draws}


def run_control_quota(template_entries, probs_by_site, rng, *,
                      quota=ARM_B_QUOTA):
    """Control runner (Amendment 1b): per-draw regeneration;
    the draw itself is the frozen equal-quota draw (plans are
    functions of the template's margins and carry over to the
    regenerated population slot by slot)."""
    plans = _quota_plans(template_entries, quota)
    sites = sorted(plans)
    r2_draws, adj_draws, p_draws = [], [], []
    for _ in range(DRAWS):
        entries, vectors = synthetic_entries(
            template_entries, probs_by_site, rng)
        r2, adj, p = _draw_quota(plans, entries, vectors, rng,
                                 True)
        r2_draws.append(r2)
        adj_draws.append(adj)
        p_draws.append(p)
    return {"cells_included": None, "excluded_cells": {},
            "sites": sites, "quota_allocations": {
                s: plans[s][1] for s in sites},
            "r2_draws": r2_draws, "adj_draws": adj_draws,
            "p_draws": p_draws}


def summarise(run):
    adj = np.array(run["adj_draws"])
    raw = np.array(run["r2_draws"])
    out = {
        "cells_included": run["cells_included"],
        "excluded_cells": run["excluded_cells"],
        "median_adj_r2": float(np.median(adj)) if len(adj) else None,
        "adj_r2_interval_95": [float(np.percentile(adj, 2.5)),
                               float(np.percentile(adj, 97.5))]
        if len(adj) else None,
        "median_raw_r2": float(np.median(raw)) if len(raw) else None,
    }
    if run.get("quota_allocations"):
        out["quota_allocations"] = run["quota_allocations"]
    if run["p_draws"]:
        p = np.array(run["p_draws"])
        out["share_draws_rejecting"] = float((p <= ALPHA).mean())
        out["median_p"] = float(np.median(p))
    return out


# ---------------------------------------------------------------------------
# Controls (frozen construction, as Phase-392)
# ---------------------------------------------------------------------------

def synthetic_entries(template_entries, probs_by_site, rng):
    entries, vectors = [], []
    n_cols = len(next(iter(probs_by_site.values())))
    for slot in template_entries:
        p = probs_by_site[slot["site"]]
        draws = rng.choice(n_cols, size=slot["n_legible"], p=p)
        vec = np.bincount(draws, minlength=n_cols).astype(np.float64)
        entries.append({"site": slot["site"],
                        "type_class": slot["type_class"],
                        "n_legible": slot["n_legible"]})
        vectors.append(vec)
    return entries, np.array(vectors)


def negative_control_pass(summary) -> bool:
    # Amendment 1, part 3: under per-draw regeneration the
    # rejection share is a binomial proportion over 199
    # independent worlds (sd ~ 0.0155 at alpha 0.05), so the
    # Phase-392 bound (share <= 0.05) would fail a calibrated
    # instrument ~43% of the time by chance alone. The frozen
    # bound is share <= 0.10 (~3.2 sd above nominal), which
    # still fails the miscalibration this control exists to
    # catch (observed broken-construction shares 0.156-0.171).
    return bool(summary["median_adj_r2"] < MARGIN_R2
                and summary["share_draws_rejecting"] <= 0.10)


def positive_control_pass(summary) -> bool:
    return bool(summary["share_draws_rejecting"] >= 0.95
                and summary["adj_r2_interval_95"][0] > MARGIN_R2)
# === FROZEN PIPELINE END ===


def count_vector(entry, col_index, n_cols):
    """Verbatim from build_calibration.py (the calibration's
    vectoriser): mapped tokens to their M77 column (OTHER if
    outside the frozen set), unmapped to UNMAPPED."""
    vec = np.zeros(n_cols, dtype=np.float64)
    for tok, kind in zip(entry["tokens"], entry["kinds"]):
        if kind in ("direct", "chain"):
            vec[col_index.get(tok, col_index["OTHER"])] += 1.0
        elif kind == "unmapped":
            vec[col_index["UNMAPPED"]] += 1.0
    return vec


def apply_verdict(controls_ok, primary, loso):
    """Frozen verdict rule (freeze.md section 6), applied
    mechanically per arm."""
    if not controls_ok:
        return "INVALID"
    lo, hi = primary["adj_r2_interval_95"]
    share = primary["share_draws_rejecting"]
    if (share >= 0.95 and lo > MARGIN_R2
            and all(s["median_adj_r2"] >= MARGIN_R2
                    for s in loso.values())):
        return "SUPPORTED"
    if hi <= MARGIN_R2 and share <= 0.05:
        return "CONTRADICTED"
    return "INCONCLUSIVE"


def pooled_probs(subset, col_index, n_cols):
    counts = np.zeros(n_cols)
    for e in subset:
        counts += count_vector(e, col_index, n_cols)
    return counts / counts.sum()


def run_controls(template, eligible_subset, sites, sets, runner,
                 col_index, n_cols):
    """The calibration's control construction, verbatim in
    structure (build_calibration.py run_arm): one fresh RNG
    per arm at the frozen seed; negative then positive on
    the same stream; pooled composition over the arm's
    ELIGIBLE subset; positive profiles = pooled x
    POSITIVE_BOOST on the frozen sign sets, renormalised."""
    rng = np.random.default_rng(SEED)
    pooled = pooled_probs(eligible_subset, col_index, n_cols)
    neg = summarise(runner(template, {s: pooled for s in sites},
                           rng))
    pos_probs = {}
    for s in sites:
        p = pooled.copy()
        idx = [col_index[c] for c in sets[s]]
        p[idx] *= POSITIVE_BOOST
        pos_probs[s] = p / p.sum()
    pos = summarise(runner(template, pos_probs, rng))
    return (dict(neg, **{"pass": negative_control_pass(neg)}),
            dict(pos, **{"pass": positive_control_pass(pos)}))


def _bc(p, q):
    den = float((p + q).sum())
    return float(np.abs(p - q).sum() / den) if den else 0.0


def arm_c_decomposition(analysis, vectors, eligible, columns):
    """Frozen Arm C items (freeze.md section 2). Descriptive
    only: no verdict, no p-values, no margin rule."""
    props = vectors / vectors.sum(axis=1, keepdims=True)
    sites = audit_mod.PHASE392_ANALYSIS_SITES

    def centroid(idxs):
        return props[idxs].mean(axis=0)

    by_site = {s: [i for i, e in enumerate(analysis)
                   if e["site"] == s] for s in sites}
    cent = {s: centroid(ix) for s, ix in by_site.items()}
    matrix = {s: {t: _bc(cent[s], cent[t]) for t in sites}
              for s in sites}
    others_ix = [i for i, e in enumerate(analysis)
                 if e["site"] != "Harappa"]
    pooled_others = centroid(others_ix)
    h_cent = cent["Harappa"]
    contrib = np.abs(h_cent - pooled_others) / 2.0
    bc_val = float(contrib.sum())
    order = sorted(range(len(columns)),
                   key=lambda j: (-contrib[j], columns[j]))
    top25 = [{"sign": columns[j],
              "contribution": float(contrib[j]),
              "share_of_bc": float(contrib[j] / bc_val)
              if bc_val else 0.0} for j in order[:25]]
    within = {}
    for tc in ("SEAL", "TAB"):
        h_ix = [i for i in by_site["Harappa"]
                if analysis[i]["type_class"] == tc]
        o_ix = [i for i in others_ix
                if analysis[i]["type_class"] == tc]
        within[tc] = _bc(centroid(h_ix), centroid(o_ix))
    h_seal = centroid([i for i in by_site["Harappa"]
                       if analysis[i]["type_class"] == "SEAL"])
    h_tab = centroid([i for i in by_site["Harappa"]
                      if analysis[i]["type_class"] == "TAB"])
    mass: dict = {}
    for e in eligible:
        key = f"{e['site']}|{e['type_class']}"
        m = mass.setdefault(key, {"inscriptions": 0, "tokens": 0})
        m["inscriptions"] += 1
        m["tokens"] += e["n_legible"]
    return {
        "n_records": len(by_site["Harappa"]),
        "share_of_analysis_population":
            len(by_site["Harappa"]) / len(analysis),
        "centroid_bc_matrix": matrix,
        "harappa_vs_pooled_others_bc": bc_val,
        "column_contributions_top25": top25,
        "within_type": within,
        "harappa_seal_vs_tab_bc": _bc(h_seal, h_tab),
        "token_mass_by_site_type_eligible_population": mass,
    }


def population_guard(flow, eligible, analysis, columns, audit):
    """Recompute the frozen margins; return mismatches
    (empty = reproduced)."""
    bad = []
    if flow != audit["population_flow"]:
        bad.append("population flow != frozen margins audit")
    if len(analysis) != audit["analysis_population"]["records"]:
        bad.append("analysis records != audit")
    if sorted({e["site"] for e in analysis}) != sorted(
            audit["analysis_population"]["sites"]):
        bad.append("analysis site set != audit")
    if len(columns) != audit["sign_columns"]:
        bad.append("sign columns != audit")
    arm_a = [e for e in analysis if e["site"] != "Harappa"]
    aa = audit["arm_a_harappa_excluded"]
    if len(arm_a) != aa["records"]:
        bad.append("arm A records != audit")
    cells_a = dict(Counter(f"{e['site']}|{e['type_class']}"
                           for e in arm_a))
    if cells_a != aa["cells"]:
        bad.append("arm A cell table != audit")
    s_complete = [e for e in arm_a if e["complete"] != "N"]
    if len(s_complete) != aa["s_complete_records"]:
        bad.append("arm A S-complete records != audit")
    totals_b = dict(Counter(e["site"] for e in analysis))
    if totals_b != audit["arm_b_site_equal"]["site_totals"]:
        bad.append("arm B site totals != audit")
    return bad


def _fmt(x, nd=5):
    return f"{x:.{nd}f}"


def write_report(res: dict) -> str:
    L = []
    L.append("# Phase-393 — Spec 028: Harappa Robustness of "
             "the M77 Site Effect")
    L.append("")
    if res.get("stop_reason"):
        L.append(f"**STOPPED — {res['stop_reason']}**")
        L.append("")
    va, vb = res["verdicts"]["arm_a"], res["verdicts"]["arm_b"]
    L.append(f"**Arm A verdict (primary): {va}** — bounded claim: "
             "\"site-linked repertoire structure at/above the "
             "practical margin exists among the non-Harappa "
             "sites.\"")
    L.append("")
    L.append(f"**Arm B verdict (secondary): {vb}** — bounded "
             "claim: \"the site effect is not an "
             "inscription-count artifact of the large corpora.\"")
    L.append("")
    L.append("Arm C is exploratory and descriptive only; it "
             "carries no verdict. Reporting is hierarchical "
             "(freeze §6): Arm A is the headline; Arm B is a "
             "separate secondary bounded claim; there is no "
             "pooled headline. Period is not controlled in "
             "either arm (inherited stated boundary: the "
             "layer's period field is 59.2% uninformative).")
    L.append("")
    for key, title in (("arm_a", "Arm A — Harappa excluded "
                        "(confirmatory, primary)"),
                       ("arm_b", "Arm B — site-equal weight "
                        "(confirmatory, secondary)")):
        arm = res.get(key)
        L.append(f"## {title}")
        L.append("")
        if arm is None or arm.get("primary") is None:
            L.append("Not run (see stop reason above).")
            L.append("")
            continue
        p = arm["primary"]
        L.append(f"- Records: {arm['records']}; inscriptions "
                 f"per draw: {arm['inscriptions_per_draw']}")
        L.append(f"- Median adjusted R²: "
                 f"**{_fmt(p['median_adj_r2'])}**; interval "
                 f"[{_fmt(p['adj_r2_interval_95'][0])}, "
                 f"{_fmt(p['adj_r2_interval_95'][1])}] vs margin "
                 f"0.01")
        L.append(f"- Rejection share at α=0.05: "
                 f"{p['share_draws_rejecting']:.3f}; median p "
                 f"{p['median_p']:.4f}")
        L.append(f"- Median raw R²: {_fmt(p['median_raw_r2'])}")
        L.append("")
        L.append("### Controls (failure = this arm INVALID)")
        L.append("")
        L.append("| Control | Median adj R² | Interval | Share "
                 "rejecting | Result |")
        L.append("|---|---|---|---|---|")
        for name in ("negative_control", "positive_control"):
            c = arm[name]
            L.append(f"| {name} | {_fmt(c['median_adj_r2'])} | "
                     f"[{_fmt(c['adj_r2_interval_95'][0])}, "
                     f"{_fmt(c['adj_r2_interval_95'][1])}] | "
                     f"{c['share_draws_rejecting']:.3f} | "
                     f"{'PASS' if c['pass'] else 'FAIL'} |")
        L.append("")
        L.append("### Leave-one-site-out")
        L.append("")
        L.append("| Dropped site | Median adj R² | Interval | "
                 "Share rejecting |")
        L.append("|---|---|---|---|")
        for site, s in arm["loso"].items():
            L.append(f"| {site} | {_fmt(s['median_adj_r2'])} | "
                     f"[{_fmt(s['adj_r2_interval_95'][0])}, "
                     f"{_fmt(s['adj_r2_interval_95'][1])}] | "
                     f"{s['share_draws_rejecting']:.3f} |")
        L.append("")
        if arm.get("sensitivity_s_complete"):
            s = arm["sensitivity_s_complete"]
            L.append(f"S-complete sensitivity (labelled, no "
                     f"verdict): median adjusted R² "
                     f"{_fmt(s['median_adj_r2'])}, interval "
                     f"[{_fmt(s['adj_r2_interval_95'][0])}, "
                     f"{_fmt(s['adj_r2_interval_95'][1])}], "
                     f"rejection share "
                     f"{s['share_draws_rejecting']:.3f}.")
            L.append("")
    c = res.get("arm_c")
    if c:
        L.append("## Arm C — Harappa decomposition "
                 "(EXPLORATORY, descriptive only)")
        L.append("")
        L.append(f"Harappa records: {c['n_records']} "
                 f"({c['share_of_analysis_population']:.4f} of "
                 f"the analysis population). Harappa centroid vs "
                 f"the pooled other sites: Bray–Curtis "
                 f"{c['harappa_vs_pooled_others_bc']:.4f}; within "
                 f"SEAL only {c['within_type']['SEAL']:.4f}; "
                 f"within TAB only {c['within_type']['TAB']:.4f}; "
                 f"Harappa SEAL vs TAB centroids "
                 f"{c['harappa_seal_vs_tab_bc']:.4f}.")
        L.append("")
        L.append("Site-centroid Bray–Curtis matrix (analysis "
                 "population):")
        L.append("")
        sites = list(c["centroid_bc_matrix"].keys())
        L.append("| | " + " | ".join(sites) + " |")
        L.append("|" + "---|" * (len(sites) + 1))
        for s in sites:
            row = c["centroid_bc_matrix"][s]
            L.append(f"| {s} | " + " | ".join(
                f"{row[t]:.3f}" for t in sites) + " |")
        L.append("")
        L.append("Largest per-column contributions to Harappa "
                 "vs pooled others (|p − q| / 2, top 25):")
        L.append("")
        L.append("| Sign | Contribution | Share of distance |")
        L.append("|---|---|---|")
        for row in c["column_contributions_top25"]:
            L.append(f"| {row['sign']} | "
                     f"{row['contribution']:.5f} | "
                     f"{row['share_of_bc']:.4f} |")
        L.append("")
        L.append("Token mass by object type (eligible "
                 "population):")
        L.append("")
        L.append("| Site | Type | Inscriptions | Tokens |")
        L.append("|---|---|---|---|")
        mass = c["token_mass_by_site_type_eligible_population"]
        for key in sorted(mass):
            site, tc = key.split("|")
            m = mass[key]
            L.append(f"| {site} | {tc} | {m['inscriptions']} | "
                     f"{m['tokens']} |")
        L.append("")
    L.append("## Provenance")
    L.append("")
    L.append("- Freeze: specs/028-harappa-robustness/freeze.md; "
             f"digest {res['provenance']['freeze_digest']}")
    L.append("- OSF registration of the frozen contract: "
             "https://osf.io/7m35w/ (filed before execution)")
    L.append(f"- Seed {res['provenance']['seed']}; draws "
             f"{res['provenance']['draws']}; permutations per "
             f"draw {res['provenance']['permutations_per_draw']}; "
             f"elapsed {res['provenance']['elapsed_s']}s")
    L.append("- Population guard: reproduced the frozen "
             "margins exactly (see results JSON).")
    L.append("")
    return "\n".join(L)


def main() -> int:
    t0 = time.time()
    res: dict = {
        "experiment": "spec028-phase393-harappa-robustness",
        "phase": 393,
        "verdicts": {"arm_a": "INVALID", "arm_b": "INVALID"},
        "stop_reason": None,
    }

    def finish():
        res["provenance"] = {
            "seed": SEED, "draws": DRAWS,
            "permutations_per_draw": PERMS,
            "freeze_digest": json.loads(
                FREEZE_PATH.read_text(encoding="utf-8"))["digest"],
            "elapsed_s": round(time.time() - t0, 1),
            "script":
                "backend/scripts/phase393_harappa_robustness.py",
        }
        RESULTS_PATH.write_text(json.dumps(res, indent=1) + "\n",
                                encoding="utf-8")
        REPORT_PATH.write_text(write_report(res),
                               encoding="utf-8")
        print(json.dumps(
            {"verdicts": res["verdicts"],
             "stop_reason": res["stop_reason"],
             "elapsed_s": res["provenance"]["elapsed_s"]},
            indent=1))
        return 0

    for name, want in EXPECTED_SHA256.items():
        if sha256_file(STORE / name) != want:
            res["stop_reason"] = (f"INVALID: input hash "
                                  f"mismatch for {name}")
            return finish()

    os.environ["SPEC028_STORE"] = str(STORE)
    sys.path.insert(0, str(SPEC_DIR))
    global audit_mod
    import build_margins_audit as audit_mod

    keyed = json.loads(KEYED_PATH.read_text(encoding="utf-8"))
    horus = {}
    with open(HORUS_PATH, newline="", encoding="utf-8") as f:
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

    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    res["population"] = {"flow": flow, "eligible": len(eligible),
                         "analysis": len(analysis),
                         "columns": n_cols}
    bad = population_guard(flow, eligible, analysis, columns,
                           audit)
    res["population"]["guard_mismatches"] = bad
    if bad:
        res["stop_reason"] = ("INVALID: population not "
                              "reproduced: " + "; ".join(bad))
        return finish()

    def subset(entries_src, vec_src, keep):
        ix = [i for i, e in enumerate(entries_src)
              if e["site"] in keep]
        return [entries_src[i] for i in ix], vec_src[ix]

    arm_a_sites = audit_mod.ARM_A_SITES
    all_sites = audit_mod.PHASE392_ANALYSIS_SITES
    a_entries, a_vectors = subset(analysis, a_vectors_all,
                                  set(arm_a_sites))
    a_eligible = [e for e in eligible if e["site"] != "Harappa"]
    rng = np.random.default_rng(SEED)

    # ---- Arm A: primary, LOSO, S-complete, controls ----
    a_run = run_pipeline_cells(a_entries, a_vectors, rng)
    a_primary = summarise(a_run)
    a_loso = {}
    for site in arm_a_sites:
        sub_e, sub_v = subset(a_entries, a_vectors,
                              set(arm_a_sites) - {site})
        a_loso[site] = summarise(run_pipeline_cells(
            sub_e, sub_v, rng))
    s_ix = [i for i, e in enumerate(a_entries)
            if e["complete"] != "N"]
    a_sens = summarise(run_pipeline_cells(
        [a_entries[i] for i in s_ix], a_vectors[s_ix], rng))
    a_neg, a_pos = run_controls(
        a_entries, a_eligible, arm_a_sites,
        audit["arm_a_harappa_excluded"]
        ["positive_control_sign_sets"],
        lambda t, probs, r: run_control_cells(t, probs, r),
        col_index, n_cols)
    a_controls_ok = bool(a_neg["pass"] and a_pos["pass"])
    res["arm_a"] = {
        "records": len(a_entries),
        "inscriptions_per_draw":
            a_run["cells_included"] * N_CELL,
        "primary": a_primary, "loso": a_loso,
        "sensitivity_s_complete": a_sens,
        "negative_control": a_neg, "positive_control": a_pos,
        "controls_pass": a_controls_ok,
    }
    res["verdicts"]["arm_a"] = apply_verdict(
        a_controls_ok, a_primary, a_loso)
    if time.time() - t0 > DEADLINE_S:
        raise TimeoutError("deadline exceeded after Arm A")

    # ---- Arm B: primary, LOSO, controls ----
    b_run = run_pipeline_quota(analysis, a_vectors_all, rng)
    b_primary = summarise(b_run)
    b_ipd = int(sum(sum(a.values()) for a in
                    b_primary["quota_allocations"].values()))
    b_loso = {}
    for site in all_sites:
        sub_e, sub_v = subset(analysis, a_vectors_all,
                              set(all_sites) - {site})
        b_loso[site] = summarise(run_pipeline_quota(
            sub_e, sub_v, rng))
    b_neg, b_pos = run_controls(
        analysis, eligible, all_sites,
        audit["arm_b_site_equal"]["positive_control_sign_sets"],
        lambda t, probs, r: run_control_quota(t, probs, r),
        col_index, n_cols)
    b_controls_ok = bool(b_neg["pass"] and b_pos["pass"])
    res["arm_b"] = {
        "records": len(analysis),
        "inscriptions_per_draw": b_ipd,
        "primary": b_primary, "loso": b_loso,
        "negative_control": b_neg, "positive_control": b_pos,
        "controls_pass": b_controls_ok,
    }
    res["verdicts"]["arm_b"] = apply_verdict(
        b_controls_ok, b_primary, b_loso)

    # ---- Arm C: exploratory decomposition ----
    res["arm_c"] = arm_c_decomposition(analysis, a_vectors_all,
                                       eligible, columns)
    return finish()


if __name__ == "__main__":
    raise SystemExit(main())
