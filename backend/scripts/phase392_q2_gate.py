"""Phase-392 — Spec 027 Stage 1: Q2 repertoire gate.

Executes stage1-freeze.md AS AMENDED (Amendment 1; freeze
digest in stage1-freeze.json): adjusted PERMANOVA R^2 for site
on per-inscription M77 composition (Bray-Curtis), rarefaction
to cell n=49 within site x type-class, R=199 draws, B=499
permutations within type strata per draw, seed 20261011,
practical margin adjusted R^2 = 0.01, discriminating
negative/positive controls (failure = INVALID), LOSO over the
6 analysis sites, and the labelled S-complete sensitivity
(no verdict).

Population rules are the adjudicated Ask 3 rules as frozen;
the executed population is asserted equal to the margins
audit's frozen counts (stage1/margins-audit.json) before any
outcome is computed — a mismatch stops the run as INVALID
(population not reproduced). No anchor or PRED contact.

Inputs (hashes asserted):
  corpora/downloads/spec027_stage1/icit_converted_v2_keyed.json
  corpora/downloads/spec027_stage1/horus_inscriptions.csv
Outputs:
  reports/phase392_results.json, reports/phase392_report.md
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / "corpora" / "downloads" / "spec027_stage1"
KEYED_PATH = STORE / "icit_converted_v2_keyed.json"
HORUS_PATH = STORE / "horus_inscriptions.csv"
AUDIT_PATH = (ROOT / "specs" / "027-movement-culture-language"
              / "stage1" / "margins-audit.json")
RESULTS_PATH = ROOT / "reports" / "phase392_results.json"
REPORT_PATH = ROOT / "reports" / "phase392_report.md"

EXPECTED_SHA256 = {
    "icit_converted_v2_keyed.json":
        "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8",
    "horus_inscriptions.csv":
        "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
}
SEED = 20261011
ALPHA = 0.05
MARGIN_R2 = 0.01          # on the ADJUSTED R^2 scale (Amendment 1)
N_CELL = 49               # Amendment 1 (was 15 at first drafting)
DRAWS = 199
PERMS = 499
MIN_SITE = 20
POSITIVE_BOOST = 3.0
DEADLINE_S = 5400

ANALYSIS_SITES = ["Harappa", "Mohenjo-daro", "Dholavira",
                  "Lothal", "Chanhu-daro", "Kalibangan"]
EXPECTED_CELLS = {
    ("Harappa", "SEAL"): 361, ("Harappa", "TAB"): 1076,
    ("Mohenjo-daro", "SEAL"): 1138, ("Mohenjo-daro", "TAB"): 164,
    ("Dholavira", "SEAL"): 96, ("Dholavira", "TAB"): 15,
    ("Lothal", "SEAL"): 72, ("Lothal", "TAB"): 2,
    ("Chanhu-daro", "SEAL"): 52, ("Chanhu-daro", "TAB"): 2,
    ("Kalibangan", "SEAL"): 49, ("Kalibangan", "TAB"): 3,
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def type_class(type_value: str) -> str:
    prefix = (type_value or "").split(":")[0]
    return prefix if prefix in ("SEAL", "TAB", "POT") else "OTHER"


def adjusted_r2(r2: float, n: int, g: int) -> float:
    """Standard PERMANOVA adjusted R^2: null expectation ~ 0."""
    if n <= g:
        return 0.0
    return 1.0 - (1.0 - r2) * (n - 1) / (n - g)


# ---------------------------------------------------------------------------
# Population (frozen Ask 3 rules; identical to the margins audit)
# ---------------------------------------------------------------------------

def build_population():
    keyed = json.loads(KEYED_PATH.read_text(encoding="utf-8"))
    records = keyed["inscriptions"]
    horus = {}
    with open(HORUS_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            horus[row["id"]] = row
    flow = Counter()
    eligible = []
    for rec in records:
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
            "n_placeholder": sum(1 for k in kinds
                                 if k == "placeholder"),
            "complete": (h.get("complete") or "").strip(),
        })
    return eligible, dict(flow)


def composition_columns(eligible):
    """Frozen columns: signs with >= 10 mapped tokens in the
    eligible population + UNMAPPED + OTHER (order fixed)."""
    counts = Counter()
    for e in eligible:
        for tok, kind in zip(e["tokens"], e["kinds"]):
            if kind in ("direct", "chain"):
                counts[tok] += 1
    frequent = sorted(s for s, c in counts.items() if c >= 10)
    columns = frequent + ["UNMAPPED", "OTHER"]
    return columns, counts


def count_vector(entry, col_index):
    vec = np.zeros(len(col_index), dtype=np.float64)
    for tok, kind in zip(entry["tokens"], entry["kinds"]):
        if kind in ("direct", "chain"):
            vec[col_index.get(tok, col_index["OTHER"])] += 1.0
        elif kind == "unmapped":
            vec[col_index["UNMAPPED"]] += 1.0
    return vec


# ---------------------------------------------------------------------------
# PERMANOVA machinery
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
# The frozen pipeline (used identically for primary + controls)
# ---------------------------------------------------------------------------

def cell_members(entries):
    cells = defaultdict(list)
    for i, e in enumerate(entries):
        cells[(e["site"], e["type_class"])].append(i)
    return cells


def run_pipeline(entries, vectors, rng, *, with_perms=True):
    cells_all = cell_members(entries)
    cells = {c: idxs for c, idxs in cells_all.items()
             if len(idxs) >= N_CELL}
    excluded = {f"{s}|{t}": len(v) for (s, t), v in
                sorted(cells_all.items()) if len(v) < N_CELL}
    if not cells:
        return {"cells_included": 0, "excluded_cells": excluded,
                "r2_draws": [], "adj_draws": [], "p_draws": []}
    sites = sorted({c[0] for c in cells})
    n_draw = N_CELL * len(cells)
    g = len(sites)
    r2_draws, adj_draws, p_draws = [], [], []
    for _ in range(DRAWS):
        chosen = []
        for cell, idxs in sorted(cells.items()):
            pick = rng.choice(len(idxs), size=N_CELL, replace=False)
            chosen.extend(idxs[j] for j in pick)
        chosen = np.array(sorted(chosen))
        counts = vectors[chosen]
        props = counts / counts.sum(axis=1, keepdims=True)
        site_of = [entries[i]["site"] for i in chosen]
        label_idx = np.array([sites.index(s) for s in site_of])
        group_sizes = np.array(
            [(label_idx == k).sum() for k in range(g)],
            dtype=np.float64)
        strata = np.array([entries[i]["type_class"] for i in chosen])
        gower, ss_t, ss_a = permanova(props, label_idx, group_sizes)
        r2 = ss_a / ss_t if ss_t > 0 else 0.0
        r2_draws.append(r2)
        adj_draws.append(adjusted_r2(r2, n_draw, g))
        if with_perms:
            exceed = 0
            for _ in range(PERMS):
                if permuted_ss(gower, label_idx, group_sizes,
                               strata, rng) >= ss_a - 1e-12:
                    exceed += 1
            p_draws.append((1 + exceed) / (1 + PERMS))
    return {"cells_included": len(cells),
            "excluded_cells": excluded, "sites": sites,
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
    if run["p_draws"]:
        p = np.array(run["p_draws"])
        out["share_draws_rejecting"] = float((p <= ALPHA).mean())
        out["median_p"] = float(np.median(p))
    return out


# ---------------------------------------------------------------------------
# Controls (frozen construction)
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


def main() -> int:
    t0 = time.time()
    for path in (KEYED_PATH, HORUS_PATH):
        digest = sha256_file(path)
        if digest != EXPECTED_SHA256[path.name]:
            print(f"FATAL: {path.name} sha256 {digest} != frozen "
                  f"{EXPECTED_SHA256[path.name]}", file=sys.stderr)
            return 2

    eligible, flow = build_population()
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    flow_match = all(flow.get(k, 0) == v
                     for k, v in audit["population_flow"].items())
    columns, _ = composition_columns(eligible)
    col_index = {c: i for i, c in enumerate(columns)}
    site_counts = Counter(e["site"] for e in eligible)
    analysis = [e for e in eligible
                if site_counts[e["site"]] >= MIN_SITE]
    cells = cell_members(analysis)
    cell_counts = {f"{s}|{t}": len(v) for (s, t), v in
                   sorted(cells.items())}
    expected_cell_counts = {f"{s}|{t}": n for (s, t), n in
                            EXPECTED_CELLS.items()}
    population_ok = (
        flow_match
        and flow.get("eligible_primary") == 3144
        and len(analysis) == 3030
        and sorted({e["site"] for e in analysis}) == ANALYSIS_SITES
        and cell_counts == expected_cell_counts
        and len(columns) == 125)

    base = {
        "phase": 392,
        "spec": "027-movement-culture-language",
        "stage": "stage1-q2-gate",
        "seed": SEED, "margin_adj_r2": MARGIN_R2,
        "n_cell": N_CELL, "draws": DRAWS, "perms": PERMS,
        "population_flow": flow,
        "population_reproduced": bool(population_ok),
        "analysis_records": len(analysis),
        "sign_columns": len(columns),
        "deadline_s": DEADLINE_S,
    }
    if not population_ok:
        base["verdict"] = "INVALID"
        base["verdict_reason"] = (
            "population not reproduced against the frozen "
            "margins (stage1-freeze.md section 6 precondition)")
        RESULTS_PATH.write_text(json.dumps(base, indent=1) + "\n",
                                encoding="utf-8")
        REPORT_PATH.write_text(
            "# Phase-392 — INVALID (population not reproduced)\n\n"
            "The executed population differs from the frozen "
            "margins in stage1-freeze.md section 3/6. No outcome "
            "was computed. See reports/phase392_results.json.\n",
            encoding="utf-8")
        print(json.dumps(base, indent=1))
        return 0

    vectors = np.array([count_vector(e, col_index)
                        for e in analysis])
    rng = np.random.default_rng(SEED)

    primary = summarise(run_pipeline(analysis, vectors, rng))
    print(f"[{time.time()-t0:.0f}s] primary done", flush=True)

    loso = {}
    for dropped in ANALYSIS_SITES:
        sub_entries = [e for e in analysis if e["site"] != dropped]
        sub_idx = [i for i, e in enumerate(analysis)
                   if e["site"] != dropped]
        run = run_pipeline(sub_entries, vectors[sub_idx], rng,
                           with_perms=False)
        loso[dropped] = summarise(run)["median_adj_r2"]
    print(f"[{time.time()-t0:.0f}s] loso done", flush=True)

    sc_entries = [e for e in analysis if e["complete"] != "N"]
    sc_idx = [i for i, e in enumerate(analysis)
              if e["complete"] != "N"]
    sens = summarise(run_pipeline(sc_entries, vectors[sc_idx], rng))
    sens["records"] = len(sc_entries)
    print(f"[{time.time()-t0:.0f}s] sensitivity done", flush=True)

    pooled_counts = np.zeros(len(columns))
    for e in eligible:
        pooled_counts += count_vector(e, col_index)
    pooled_probs = pooled_counts / pooled_counts.sum()

    neg_entries, neg_vectors = synthetic_entries(
        analysis, {s: pooled_probs for s in ANALYSIS_SITES}, rng)
    neg = summarise(run_pipeline(neg_entries, neg_vectors, rng))
    neg_pass = bool(neg["median_adj_r2"] < MARGIN_R2
                    and (1.0 - neg["share_draws_rejecting"]) >= 0.95)
    print(f"[{time.time()-t0:.0f}s] negative control done",
          flush=True)

    # Positive control sign sets: DETERMINISTIC disjoint
    # blocks of 10 from the 60 most frequent sign columns
    # (pooled-frequency ranking — margins only), assigned in
    # the frozen site order. Amendment 1: rng-drawn sets made
    # the planted effect size luck-dependent in pre-freeze
    # simulation (adjusted R^2 0.012-0.027 at the same boost).
    sign_cols = [i for i, c in enumerate(columns)
                 if c not in ("UNMAPPED", "OTHER")]
    by_freq = sorted(sign_cols,
                     key=lambda i: -pooled_counts[i])[:60]
    pos_probs, planted = {}, {}
    for k, s in enumerate(ANALYSIS_SITES):
        p = pooled_probs.copy()
        boosted = sorted(by_freq[10 * k:10 * k + 10])
        p[boosted] *= POSITIVE_BOOST
        pos_probs[s] = p / p.sum()
        planted[s] = [columns[i] for i in boosted]
    pos_entries, pos_vectors = synthetic_entries(
        analysis, pos_probs, rng)
    pos = summarise(run_pipeline(pos_entries, pos_vectors, rng))
    pos_pass = bool(pos["share_draws_rejecting"] >= 0.95
                    and pos["adj_r2_interval_95"][0] > MARGIN_R2)
    print(f"[{time.time()-t0:.0f}s] positive control done",
          flush=True)

    share_rej = primary["share_draws_rejecting"]
    lo, hi = primary["adj_r2_interval_95"]
    loso_vals = [v for v in loso.values() if v is not None]
    if not (neg_pass and pos_pass):
        verdict = "INVALID"
        reason = ("a discriminating control failed "
                  f"(negative pass={neg_pass}, positive "
                  f"pass={pos_pass}); no primary verdict issued")
    elif (share_rej >= 0.95 and lo > MARGIN_R2
          and all(v > MARGIN_R2 for v in loso_vals)):
        verdict = "SUPPORTED"
        reason = ("controls pass; >=95% of draws reject; "
                  "adjusted R^2 interval entirely above the 0.01 "
                  "margin; every LOSO median adjusted R^2 above "
                  "the margin")
    elif (1.0 - share_rej) >= 0.95 or hi <= MARGIN_R2:
        verdict = "CONTRADICTED"
        reason = ("controls pass; the frozen contradiction "
                  "rule fires (>=95% of draws fail to reject, "
                  "or the adjusted R^2 interval lies entirely "
                  "at/below the 0.01 margin). Negative closure "
                  "per spec section 7.2 applies")
    else:
        verdict = "INCONCLUSIVE"
        reason = ("controls pass; neither the SUPPORTED nor "
                  "the CONTRADICTED rule fires (or the LOSO "
                  "range crosses the margin)")

    results = dict(base)
    results.update({
        "primary": primary,
        "loso_median_adj_r2": loso,
        "sensitivity_s_complete": sens,
        "negative_control": dict(neg, **{"pass": neg_pass}),
        "positive_control": dict(pos, **{"pass": pos_pass}),
        "positive_control_planted_signs": planted,
        "verdict": verdict,
        "verdict_reason": reason,
        "elapsed_s": round(time.time() - t0, 1),
    })
    RESULTS_PATH.write_text(json.dumps(results, indent=1) + "\n",
                            encoding="utf-8")

    lines = [
        "# Phase-392 — Spec 027 Stage 1 (Q2 repertoire gate)",
        "",
        f"**Verdict: {verdict}** — {reason}.",
        "",
        "Bounded claim (stage1-freeze.md section 1, as amended): "
        "in the named corpus, under M77, after rarefaction to a "
        "common cell size and stratification by object type, "
        "site explains more recorded sign-repertoire variation "
        "than expected under permuted site labels, at the "
        "declared practical margin (adjusted R^2 = 0.01). The "
        "claim concerns recorded repertoires in this corpus "
        "only; no outcome identifies a dialect or a language.",
        "",
        "## Primary",
        "",
        f"- Population reproduced: {population_ok} (eligible "
        f"{flow.get('eligible_primary')}; analysis "
        f"{len(analysis)} at 6 sites; cells included "
        f"{primary['cells_included']}; excluded cells "
        f"{primary['excluded_cells']}).",
        f"- Median adjusted PERMANOVA R^2 over {DRAWS} "
        f"rarefaction draws: {primary['median_adj_r2']:.4f}; "
        f"95% percentile interval [{lo:.4f}, {hi:.4f}]; median "
        f"raw R^2 {primary['median_raw_r2']:.4f} (reported for "
        f"transparency; all rules use the adjusted scale); "
        f"share of draws rejecting at alpha 0.05: "
        f"{share_rej:.3f}.",
        "",
        "## Jackknife (leave-one-site-out, median adjusted R^2)",
        "",
    ]
    for s in ANALYSIS_SITES:
        v = loso[s]
        lines.append(f"- Drop {s}: {v:.4f}" if v is not None
                     else f"- Drop {s}: not estimable")
    lines += [
        "",
        "## Controls (failure = INVALID)",
        "",
        f"- Negative (pooled composition, no site structure): "
        f"median adjusted R^2 {neg['median_adj_r2']:.4f}, "
        f"share rejecting {neg['share_draws_rejecting']:.3f} — "
        f"{'PASS' if neg_pass else 'FAIL'}.",
        f"- Positive (planted site effect, 10 signs x"
        f"{POSITIVE_BOOST:g} per site): median adjusted R^2 "
        f"{pos['median_adj_r2']:.4f}, interval "
        f"[{pos['adj_r2_interval_95'][0]:.4f}, "
        f"{pos['adj_r2_interval_95'][1]:.4f}], share rejecting "
        f"{pos['share_draws_rejecting']:.3f} — "
        f"{'PASS' if pos_pass else 'FAIL'}.",
        "",
        "## Labelled sensitivity (no verdict)",
        "",
        f"- S-complete (complete='N' excluded; "
        f"{sens['records']} records): median adjusted R^2 "
        f"{sens['median_adj_r2']:.4f}, share rejecting "
        f"{sens.get('share_draws_rejecting')}.",
        "",
        "## Boundaries",
        "",
        "- Period is not controlled (layer period field 59.2% "
        "uninformative; Phase-139 finding, frozen as a stated "
        "limitation).",
        "- Multi-line status is not recorded in this layer; "
        "eligibility ran on the frozen legible-token rule.",
        "- The Parpola/CISI sensitivity is NOT ESTIMABLE at "
        "the frozen crosswalk rule (freeze-time margins "
        "determination) and was not run.",
        "- Anchors and PRED untouched by this phase.",
    ]
    if verdict == "CONTRADICTED":
        lines += [
            "",
            "## Negative closure (spec section 7.2)",
            "",
            "The bounded claim is defeated and all downstream "
            "repertoire-geography work under Spec 027 STOPS. "
            "Stage 2's Q7 (material networks) is a different "
            "evidence type and is unaffected in principle, but "
            "it is not executed in this program and its own "
            "freeze remains a separate owner-gated step; Q6 "
            "was assessed NOT-YET-TESTABLE at Stage 0.",
        ]
    REPORT_PATH.write_text("\n".join(lines) + "\n",
                           encoding="utf-8")
    print(json.dumps({"verdict": verdict,
                      "median_adj_r2": primary["median_adj_r2"],
                      "interval": primary["adj_r2_interval_95"],
                      "share_rejecting": share_rej,
                      "neg_pass": neg_pass, "pos_pass": pos_pass,
                      "elapsed_s": results["elapsed_s"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
