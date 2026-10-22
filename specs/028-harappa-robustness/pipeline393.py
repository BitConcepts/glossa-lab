"""Spec 028 (Phase-393) — shared analysis pipeline.

The exact machinery calibrated before the Spec 028 freeze
(build_calibration.py imports this module) and copied
verbatim into the execution script
backend/scripts/phase393_harappa_robustness.py at the
execution step; a test in the execution PR asserts the
pipeline section's textual identity between the two files,
so the frozen machinery is the executed machinery.

Machinery provenance: Phase-392 (Spec 027 Stage 1), whose
frozen pipeline this module generalises in exactly two ways:

1. Arm A runs the Phase-392 cell-rarefaction pipeline on a
   restricted entry set (the Phase-392 analysis population
   minus Harappa). No draw code path changes.
2. Arm B replaces per-cell rarefaction with a per-site equal
   quota: every site contributes exactly ``quota``
   inscriptions per draw, sampled within the site stratified
   by type class in proportion to the site's own type-class
   counts (deterministic allocation rule below). Everything
   downstream of the draw (proportions, Bray-Curtis,
   PERMANOVA, adjusted R^2) is identical.

Two further changes apply to BOTH arms and are forced by
pre-freeze calibration evidence (recorded in freeze.md as
Amendment 1):

(a) Permutation strata are type class x legible-length
    value, not type class alone, so labels are exchangeable
    within strata under the null (support, from margins:
    98.0% of Arm A and 99.6% of Arm B inscriptions sit in
    multi-site strata). Legible length is site-correlated
    within type class (margins: mean legible length
    3.88-4.96 across the included cells) and sampling
    dispersion follows length; the exact-length stratum
    removes that channel by construction.
(b) Control populations are REGENERATED PER DRAW. In the
    Phase-392 construction (one synthetic population,
    rarefied 199 times), the negative control's rejection
    share proved to be a lottery over the generation seed:
    0.171 and 0.156 in the Spec 028 calibration attempts
    (seed 20261012; type-only and exact-length strata) and
    0.015 / 0.000 under a second generation seed — the
    share is a property of the single generated population
    (its small cells' generation noise recurs in every
    draw), not of the instrument. With per-draw
    regeneration each draw is an independent null (or
    planted) world and the shares returned to nominal:
    0.050 / 0.035 / 0.070 across the diagnostic's strata
    and seed variants at alpha 0.05. The primary arms are
    untouched by (b): their population is the real corpus
    and rarefaction is the frozen resampling. The
    effect-size machinery (proportions, Bray-Curtis,
    PERMANOVA R^2, adjusted R^2, rarefaction, quota) is
    untouched by either change.

No function in this module reads the corpus; callers supply
entries (site, type_class, n_legible) and count vectors.
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np

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
