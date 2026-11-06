#!/usr/bin/env python3
"""Phase-424 — Spec 062: Spec 028 Arm A, the precision
computation, calibration repair (successor to Spec 061;
design D-27, arm A1 only).

Executes the FROZEN Spec 062 contract
(specs/062-arm-a-precision-calibration-repair/freeze.md;
freeze digest
1800de5337503d7c596642ae48d1dc2465809c653901fa6efe1ade781957f488;
OSF contract registration 4m27t, approved + public,
DOI 10.17605/OSF.IO/4M27T, before this run). Spec 061
(Phase-423) closed CANNOT BE RUN AS WRITTEN at its
gate 0.5: its frozen calibration applied the estimator
to the constructed population in expectation, so the
calibration function was a step function (A(1) =
-0.0025188916876574316, A(b) = 1.0 at every b > 1) and
no boost in [1, 3] could impose either scenario's
theta. This successor carries Spec 061's precision
question, scenarios, search frame, gates 0.1-0.4,
trial construction, resolution and target rules
verbatim in substance, and replaces ONLY the
calibration definition (spec section 4.7-R,
construction R-1, DD-062-9) and its gate (gate
0.5-R). Arm A2 — the decisive rerun of Arm A — is
NOT part of this execution (campaign decision E-3);
nothing here runs, arms, or designs it, and Spec
061's operative target T* stays undefined on Spec
061's record.

The computation is a SIMULATION OVER RECORDED DATA:
it measures, from Phase-393's recorded resampling
distribution, how much added non-Harappa material Arm A
would need for its adjusted-R^2 interval to resolve at
the family's 0.01 margin, under two stated scenarios
(theta_1 = 0.00878393455594817, the recorded point
estimate, resolving downward; theta_2 = 0.015, resolving
upward). Its product is an intake target. It establishes
nothing about the ancient world, and it does not change
Arm A's INCONCLUSIVE verdict.

Step 0 gates, in the frozen order (spec section 3),
fail-closed — a failure stops the run in its named
class before any trial, and nothing is repaired at
run time:

  0.1 Composite pin integrity — every spec section 2
      input hashes to its freeze-record value.
      Mismatch closes INVALID.
  0.2 Population reproduction — the frozen population
      flow, re-run on the pinned inputs, reproduces
      the recorded Arm A population exactly: 1,593
      records at the 5 named sites with the recorded
      site totals and cell counts, 6 included cells,
      294 inscriptions per draw. Mismatch closes
      INVALID.
  0.3 Recorded-distribution reproduction — the frozen
      Arm A primary, re-run under the recorded
      machinery and seed (20261012; R = 199; B = 499),
      reproduces the recorded summary EXACTLY: median
      adjusted R^2 0.00878393455594817, interval
      [0.004626892186724407, 0.01297407559730989],
      rejection share 0.6231155778894473. Mismatch
      closes INVALID. The repaired calibration is
      downstream of this gate, consumes none of its
      inputs, and shares no RNG stream with it.
  0.4 Search frame present — the freeze record states
      the full frame of spec section 4.7 (integer
      grid m = 1..25, ceiling m = 25, 199 trials per
      point, 199 draws and 499 permutations per
      trial, simulation seed 20261021, construction
      R-1 effect imposition). Any element absent
      closes CANNOT BE RUN AS WRITTEN.
  0.5-R Construction calibration (repaired; spec
      section 4.7-R) — per scenario: (i) the bracket
      recomputes, A_R(1) < theta < A_R(3), where A_R
      is the drawn-population median of section
      4.7-R step 3; (ii) A_R is strictly increasing
      on the recorded scan grid b = 1, 1.25, ..., 3;
      (iii) bisection on [1, 3] achieves
      |A_R(b) - theta| <= 1e-6 within 100 iterations;
      the achieved b and A_R(b) are recorded. Any
      failure closes CANNOT BE RUN AS WRITTEN.

Construction R-1 (DD-062-9): per draw and
inscription i at site s, the proportion row is a
Dirichlet draw centred exactly on the site's imposed
composition p_s(b) — q_i(b) = G_i / sum_k G_ik with
G_ik = GammaQuantile(U[d, i, k]; kappa_i * p_s,k(b))
and kappa_i = n_legible(i) - 1 — coupled across b by
fixed uniforms U and fixed rarefaction selections,
both drawn once, before any b is evaluated, from a
dedicated calibration Generator seeded 20261021
(DD-062-7), a separate Generator object from both
per-scenario trial Generators, created before them
and used for nothing else. A_R(b) is the median of
the 199 draw statistics (the frozen pipeline393
estimator, permutations off, on each draw's fixed
rarefaction selection of 294 inscriptions). The
gamma quantile is evaluated with
scipy.special.gammaincinv (the inverse regularised
lower incomplete gamma function, i.e. the
Gamma(shape, scale 1) quantile function).

Computation (spec section 4), only after all gates
pass. Per scenario, ONE NumPy Generator seeded
20261021, consumed in ascending grid order; within a
grid point, trials 1..199 in order; within a trial,
first the template slot resampling (sites in
alphabetical order), then the frozen world generation
(the pinned pipeline393.synthetic_entries under the
imposed per-site compositions at the calibrated
boost b*), then the frozen pipeline run (the pinned
pipeline393.run_pipeline_cells, summarised by the
pinned pipeline393.summarise). The trial's interval
is its adj_r2_interval_95; a trial resolves iff the
interval excludes the 0.01 margin strictly in its
scenario's direction (DD-061-2 carried). A grid
point qualifies iff at least 80% of its trials
resolve. The scenario's target is the smallest total
added-inscription count at a qualifying grid point
(added total at m is (m - 1) x 1,593; per-site added
counts exactly (m - 1) x the recorded site totals,
DD-061-3 carried).

The machinery executed is the pinned module itself
(specs/028-harappa-robustness/pipeline393.py,
SHA-256 6c2ff91c...), imported, never copied or
modified; the population flow and the pooled
composition are Spec 028's frozen
build_margins_audit / build_calibration computations
on the pinned store inputs (hashes asserted by that
machinery and re-asserted here under gate 0.1's
composite pin).

Modes:
  --step0-only        run gates 0.1-0.5-R, write the
                      step-0 record, stop.
  --scenario {1,2}    gates, then that scenario's
                      grid, checkpointing after every
                      grid point (trial intervals +
                      Generator state) under the work
                      directory so an interrupted run
                      resumes on the exact stream.
  --assemble          when both scenarios are
                      complete, assemble
                      reports/phase424_results.json
                      and reports/phase424_report.md.

Integrity: the anchors file is asserted byte-identical
before and after. No anchor, PRED, or Arm A2 contact.
Outputs: reports/phase424_results.json,
reports/phase424_report.md (on --assemble; gate
closures write their terminal record directly).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pickle
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.special import gammaincinv  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SPEC028_DIR = ROOT / "specs" / "028-harappa-robustness"
SPEC062_DIR = ROOT / "specs" / "062-arm-a-precision-calibration-repair"
STORE = Path(os.environ.get(
    "SPEC028_STORE",
    str(ROOT / "corpora" / "downloads" / "spec028_harappa")))
RESULTS_PATH = ROOT / "reports" / "phase424_results.json"
REPORT_PATH = ROOT / "reports" / "phase424_report.md"
WORK = Path(os.environ.get(
    "PHASE424_WORK", str(ROOT / ".glossa-state" / "phase424")))

sys.path.insert(0, str(SPEC028_DIR))
import build_margins_audit as audit_mod  # noqa: E402
import pipeline393 as P  # noqa: E402

FREEZE_DIGEST = ("1800de5337503d7c596642ae48d1dc2465809c653901f"
                 "a6efe1ade781957f488")
PINS = {
    "reports/phase393_results.json":
        "0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607",
    "backend/glossa_lab/data/yajnadevam_inscriptions.csv":
        "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98",
    "specs/028-harappa-robustness/pipeline393.py":
        "6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e",
    "specs/028-harappa-robustness/margins-audit.json":
        "15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d",
    "specs/028-harappa-robustness/freeze.json":
        "376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc",
    "backend/reports/INDUS_FINAL_ANCHORS.json":
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
}
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"

RECORDED_PRIMARY = {
    "median_adj_r2": 0.00878393455594817,
    "adj_r2_interval_95": [0.004626892186724407,
                           0.01297407559730989],
    "share_draws_rejecting": 0.6231155778894473,
}
SITE_TOTALS = {"Mohenjo-daro": 1302, "Dholavira": 111,
               "Lothal": 74, "Chanhu-daro": 54,
               "Kalibangan": 52}
ARM_A_SITES = audit_mod.ARM_A_SITES  # alphabetical order
MARGIN = 0.01
GRID = list(range(1, 26))
CEILING = 25
TRIALS = 199
SIM_SEED = 20261021
RECORDED_SEED = 20261012
THETAS = {1: 0.00878393455594817, 2: 0.015}
QUALIFY_SHARE = 0.80
CAL_TOL = 1e-6
CAL_SEED = 20261021
SCAN_GRID = [1.0 + 0.25 * i for i in range(9)]
CAL_MAX_ITER = 100
BRACKET = (1.0, 3.0)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def count_vector(entry, col_index, n_cols):
    """Verbatim from Spec 028's build_calibration.py /
    phase393 execution script (the frozen vectoriser)."""
    vec = np.zeros(n_cols, dtype=np.float64)
    for tok, kind in zip(entry["tokens"], entry["kinds"]):
        if kind in ("direct", "chain"):
            vec[col_index.get(tok, col_index["OTHER"])] += 1.0
        elif kind == "unmapped":
            vec[col_index["UNMAPPED"]] += 1.0
    return vec


class Closure(Exception):
    """A step-0 gate failure in its frozen class."""

    def __init__(self, outcome: str, gate: str, detail: str):
        super().__init__(detail)
        self.outcome = outcome
        self.gate = gate
        self.detail = detail


def build_population():
    """The frozen population flow, exactly as the
    Phase-393 execution ran it."""
    import csv
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
    a_ix = [analysis_ix[i] for i, e in enumerate(analysis)
            if e["site"] != "Harappa"]
    a_entries = [eligible[i] for i in a_ix]
    a_vectors = vectors[a_ix]
    a_eligible = [e for e in eligible if e["site"] != "Harappa"]
    audit = json.loads((SPEC028_DIR / "margins-audit.json")
                       .read_text(encoding="utf-8"))
    return {
        "eligible": eligible, "flow": flow, "columns": columns,
        "col_index": col_index, "n_cols": n_cols,
        "analysis": analysis, "a_entries": a_entries,
        "a_vectors": a_vectors, "a_eligible": a_eligible,
        "audit": audit,
    }


def gate_01():
    got = {}
    for rel, want in PINS.items():
        h = sha256_file(ROOT / rel)
        got[rel] = h
        if h != want:
            raise Closure(
                "INVALID", "0.1",
                f"composite pin mismatch for {rel}: "
                f"recomputed {h}, freeze pin {want}")
    return {"gate": "0.1", "verdict": "PASS", "pins": got}


def gate_02(pop):
    a_entries = pop["a_entries"]
    audit = pop["audit"]
    bad = []
    if pop["flow"] != audit["population_flow"]:
        bad.append("population flow != frozen margins audit")
    if len(a_entries) != 1593:
        bad.append(f"Arm A records {len(a_entries)} != 1593")
    totals = dict(Counter(e["site"] for e in a_entries))
    if totals != SITE_TOTALS:
        bad.append(f"Arm A site totals {totals} != recorded")
    cells = dict(Counter(f"{e['site']}|{e['type_class']}"
                         for e in a_entries))
    if cells != audit["arm_a_harappa_excluded"]["cells"]:
        bad.append("Arm A cell table != margins audit")
    plan_cells, _excl = P._cells_plan(a_entries, P.N_CELL)
    if len(plan_cells) != 6:
        bad.append(f"included cells {len(plan_cells)} != 6")
    if len(plan_cells) * P.N_CELL != 294:
        bad.append("inscriptions per draw != 294")
    if bad:
        raise Closure("INVALID", "0.2",
                      "population reproduction failed: "
                      + "; ".join(bad))
    return {"gate": "0.2", "verdict": "PASS",
            "records": len(a_entries), "site_totals": totals,
            "cells": cells, "cells_included": len(plan_cells),
            "inscriptions_per_draw": len(plan_cells) * P.N_CELL}


def gate_03(pop):
    rng = np.random.default_rng(RECORDED_SEED)
    run = P.run_pipeline_cells(pop["a_entries"],
                               pop["a_vectors"], rng)
    s = P.summarise(run)
    got = {"median_adj_r2": s["median_adj_r2"],
           "adj_r2_interval_95": s["adj_r2_interval_95"],
           "share_draws_rejecting": s["share_draws_rejecting"]}
    if got != RECORDED_PRIMARY:
        raise Closure(
            "INVALID", "0.3",
            "recorded-distribution reproduction failed: "
            f"recomputed {got}, recorded {RECORDED_PRIMARY}")
    return {"gate": "0.3", "verdict": "PASS",
            "reproduced": got,
            "median_raw_r2": s["median_raw_r2"],
            "median_p": s["median_p"]}


def gate_04():
    freeze = json.loads((SPEC062_DIR / "freeze.json")
                        .read_text(encoding="utf-8"))
    if freeze.get("digest") != FREEZE_DIGEST:
        raise Closure(
            "CANNOT BE RUN AS WRITTEN", "0.4",
            "Spec 062 freeze digest mismatch: "
            f"{freeze.get('digest')} != {FREEZE_DIGEST}")
    frame = freeze["definition"]["design"]["search_frame"]
    checks = {
        "grid": frame.get("grid"),
        "ceiling_multiple": frame.get("ceiling_multiple"),
        "trials_per_grid_point":
            frame.get("trials_per_grid_point"),
        "draws_per_trial": frame.get("draws_per_trial"),
        "permutations_per_draw":
            frame.get("permutations_per_draw"),
        "simulation_seed": frame.get("simulation_seed"),
        "effect_imposition_ruling":
            frame.get("effect_imposition", {}).get("ruling"),
        "calibration_seed": CAL_SEED,
    }
    ok = (checks["grid"] == "integer multiples m = 1, 2, ..., 25 (step 1)"
          and checks["ceiling_multiple"] == CEILING
          and checks["trials_per_grid_point"] == TRIALS
          and checks["draws_per_trial"] == P.DRAWS == 199
          and checks["permutations_per_draw"] == P.PERMS == 499
          and checks["simulation_seed"] == SIM_SEED
          and bool(checks["effect_imposition_ruling"])
          and "R-1" in checks["effect_imposition_ruling"])
    if not ok:
        raise Closure(
            "CANNOT BE RUN AS WRITTEN", "0.4",
            f"search frame incomplete or altered: {checks}")
    return {"gate": "0.4", "verdict": "PASS", "frame": checks}


def pooled_probs(pop):
    """Spec 028 build_calibration.py's pooled composition
    over the Arm A eligible population, verbatim."""
    counts = np.zeros(pop["n_cols"])
    for e in pop["a_eligible"]:
        counts += count_vector(e, pop["col_index"],
                               pop["n_cols"])
    return counts / counts.sum()


def imposed_probs(pop, pooled, b):
    """Candidate (b): per site, the pooled composition
    with the site's positive-control sign-set columns
    multiplied by b and renormalised — verbatim the
    frozen positive-control construction with b as the
    calibration variable."""
    sets = pop["audit"]["arm_a_harappa_excluded"][
        "positive_control_sign_sets"]
    out = {}
    for s in ARM_A_SITES:
        p = pooled.copy()
        idx = [pop["col_index"][c] for c in sets[s]]
        p[idx] *= b
        out[s] = p / p.sum()
    return out


class CalibrationContext:
    """The fixed randomness of spec section 4.7-R
    step 3-R.1: drawn once, before any b is
    evaluated, from the dedicated calibration
    Generator (seed 20261021, DD-062-7), in the
    frozen order — (i) the uniform array
    U[d, i, k] (draws, template order, composition
    columns order), clipped to [1e-12, 1 - 1e-12];
    (ii) per draw, the rarefaction selections,
    for each included cell in the order the frozen
    _draw_cells performs it (sorted cell order),
    rng.choice(cell size, 49, replace=False). The
    uniforms and selections are then fixed for
    both scenarios and every b."""

    def __init__(self, pop):
        rng = np.random.default_rng(CAL_SEED)
        entries = pop["a_entries"]
        self.n_draws = P.DRAWS
        self.uniforms = np.clip(
            rng.random((self.n_draws, len(entries),
                        pop["n_cols"])),
            1e-12, 1.0 - 1e-12)
        cells, _excl = P._cells_plan(entries, P.N_CELL)
        self.selections = []
        for _d in range(self.n_draws):
            chosen = []
            for cell, idxs in sorted(cells.items()):
                pick = rng.choice(len(idxs), size=P.N_CELL,
                                  replace=False)
                chosen.extend(idxs[j] for j in pick)
            self.selections.append(
                np.array(sorted(chosen)))
        self.kappa = np.array(
            [e["n_legible"] - 1 for e in entries],
            dtype=np.float64)
        self.n_legible = np.array(
            [e["n_legible"] for e in entries],
            dtype=np.float64)
        self.site_of = [e["site"] for e in entries]
        self.cache_path = WORK / "calibration_cache.json"
        self.cache = {}
        if self.cache_path.exists():
            self.cache = json.loads(
                self.cache_path.read_text(encoding="utf-8"))

    def save_cache(self):
        WORK.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(self.cache, indent=1) + "\n",
            encoding="utf-8")


def drawn_median(pop, ctx: CalibrationContext, probs):
    """A_R(b) for the imposed compositions probs:
    the median of the 199 draw statistics of spec
    section 4.7-R step 3-R.3 — per draw, the frozen
    estimator (pipeline393 proportion
    normalisation, Bray-Curtis, PERMANOVA,
    adjusted_r2; permutations off) on the draw's
    fixed rarefaction selection applied to the
    drawn population whose inscription rows are
    Dirichlet draws centred on their site's
    imposed composition (step 3-R.2: vec_i =
    q_i * n_legible(i) with q_i the normalised
    gamma-quantile row at the fixed uniforms)."""
    entries = pop["a_entries"]
    dummy = np.random.default_rng(0)
    adj_draws = []
    for d in range(ctx.n_draws):
        sel = ctx.selections[d]
        shapes = ctx.kappa[sel][:, None] * np.array(
            [probs[ctx.site_of[i]] for i in sel])
        g = gammaincinv(shapes, ctx.uniforms[d][sel])
        q = g / g.sum(axis=1, keepdims=True)
        vectors = np.zeros((len(entries), pop["n_cols"]))
        vectors[sel] = q * ctx.n_legible[sel][:, None]
        _r2, adj, _p = P._finish_draw(
            sel.copy(), entries, vectors, dummy, False)
        adj_draws.append(adj)
    return float(np.median(np.array(adj_draws)))


def a_r(pop, ctx: CalibrationContext, pooled, b: float):
    key = f"{b:.17g}"
    if key in ctx.cache:
        return ctx.cache[key]
    value = drawn_median(pop, ctx,
                         imposed_probs(pop, pooled, b))
    ctx.cache[key] = value
    ctx.save_cache()
    return value


def gate_05r(pop, pooled):
    ctx = CalibrationContext(pop)
    scan = {f"{b:.17g}": a_r(pop, ctx, pooled, b)
            for b in SCAN_GRID}
    scan_values = [scan[f"{b:.17g}"] for b in SCAN_GRID]
    strictly_increasing = all(
        x < y for x, y in zip(scan_values, scan_values[1:]))
    records = {}
    for scen in (1, 2):
        theta = THETAS[scen]
        a1 = scan[f"{1.0:.17g}"]
        a3 = scan[f"{3.0:.17g}"]
        rec = {"theta": theta, "A_R_at_1": a1,
               "A_R_at_3": a3, "scan_grid_b": SCAN_GRID,
               "scan_grid_A_R": scan_values,
               "scan_strictly_increasing":
                   strictly_increasing}
        if not (a1 < theta < a3):
            raise Closure(
                "CANNOT BE RUN AS WRITTEN", "0.5-R",
                f"scenario {scen}: calibration bracket "
                f"does not close: A_R(1)={a1}, "
                f"theta={theta}, A_R(3)={a3}; scan "
                f"A_R={scan_values}")
        if not strictly_increasing:
            raise Closure(
                "CANNOT BE RUN AS WRITTEN", "0.5-R",
                f"scenario {scen}: A_R is not strictly "
                f"increasing on the scan grid: "
                f"b={SCAN_GRID}, A_R={scan_values}")
        lo_b, hi_b = BRACKET
        achieved = None
        iters = 0
        for iters in range(1, CAL_MAX_ITER + 1):
            mid = 0.5 * (lo_b + hi_b)
            a_mid = a_r(pop, ctx, pooled, mid)
            if abs(a_mid - theta) <= CAL_TOL:
                achieved = (mid, a_mid, iters)
                break
            if a_mid < theta:
                lo_b = mid
            else:
                hi_b = mid
        if achieved is None:
            raise Closure(
                "CANNOT BE RUN AS WRITTEN", "0.5-R",
                f"scenario {scen}: bisection did not "
                f"reach |A_R(b) - theta| <= {CAL_TOL} "
                f"within {CAL_MAX_ITER} iterations; "
                f"scan A_R={scan_values}")
        b, a_b, iters = achieved
        rec.update({
            "boost_b": b, "A_at_b": a_b,
            "abs_error": abs(a_b - theta),
            "bisection_iterations": iters,
            "bracket": list(BRACKET), "tolerance": CAL_TOL})
        records[scen] = rec
    return {"gate": "0.5-R", "verdict": "PASS",
            "calibration": {str(k): v
                            for k, v in records.items()}}, records


def run_step0():
    gates = []
    gates.append(gate_01())
    pop = build_population()
    gates.append(gate_02(pop))
    gates.append(gate_03(pop))
    gates.append(gate_04())
    pooled = pooled_probs(pop)
    g5, calibration = gate_05r(pop, pooled)
    gates.append(g5)
    return pop, pooled, calibration, gates


# ---------------------------------------------------------------------------
# The precision computation (spec section 4)
# ---------------------------------------------------------------------------

def resolves(scen: int, interval) -> bool:
    lo, hi = interval
    if scen == 1:
        return bool(hi < MARGIN)
    return bool(lo > MARGIN)


def scenario_dir(scen: int) -> Path:
    d = WORK / f"scenario{scen}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_scenario(scen: int, pop, pooled, calibration):
    """One scenario's grid, on its own Generator stream
    (seed 20261021), checkpointed after every grid
    point. Resuming restores the Generator state saved
    at the last completed point, so the stream the
    frozen discipline defines is the stream executed,
    however many launches the computation takes."""
    d = scenario_dir(scen)
    probs = imposed_probs(pop, pooled,
                          calibration[scen]["boost_b"])
    by_site = {s: [e for e in pop["a_entries"]
                   if e["site"] == s] for s in ARM_A_SITES}
    rng = np.random.default_rng(SIM_SEED)
    done = []
    prefix = 0
    for m in GRID:
        if (d / f"m{m:02d}.json").exists() and \
                (d / f"m{m:02d}.state.pkl").exists():
            prefix = m
        else:
            break
    if prefix:
        with open(d / f"m{prefix:02d}.state.pkl", "rb") as f:
            rng.bit_generator.state = pickle.load(f)
    for m in GRID:
        point_path = d / f"m{m:02d}.json"
        state_path = d / f"m{m:02d}.state.pkl"
        if m <= prefix:
            done.append(json.loads(point_path.read_text(
                encoding="utf-8")))
            continue
        t0 = time.time()
        trials = []
        n_res = 0
        for _t in range(TRIALS):
            template = []
            for s in sorted(ARM_A_SITES):
                entries_s = by_site[s]
                pick = rng.choice(len(entries_s),
                                  size=m * len(entries_s),
                                  replace=True)
                template.extend(entries_s[j] for j in pick)
            w_entries, w_vectors = P.synthetic_entries(
                template, probs, rng)
            run = P.run_pipeline_cells(w_entries, w_vectors,
                                       rng)
            summ = P.summarise(run)
            interval = summ["adj_r2_interval_95"]
            r = resolves(scen, interval)
            n_res += int(r)
            trials.append({
                "interval": interval, "resolves": r,
                "cells_included": summ["cells_included"]})
        share = n_res / TRIALS
        point = {
            "scenario": scen, "m": m,
            "added_total": (m - 1) * 1593,
            "world_total": m * 1593,
            "per_site_added": {
                s: (m - 1) * SITE_TOTALS[s]
                for s in ARM_A_SITES},
            "trials": trials, "n_resolving": n_res,
            "share_resolving": share,
            "binomial_sd": float(np.sqrt(
                share * (1.0 - share) / TRIALS)),
            "qualifies": bool(share >= QUALIFY_SHARE),
            "elapsed_s": round(time.time() - t0, 1),
        }
        point_path.write_text(json.dumps(point) + "\n",
                              encoding="utf-8")
        with open(state_path, "wb") as f:
            pickle.dump(rng.bit_generator.state, f)
        done.append(point)
        print(f"[scenario {scen}] m={m} share={share:.4f} "
              f"qualifies={point['qualifies']} "
              f"({point['elapsed_s']}s)", flush=True)
    return done


def scenario_target(points):
    for point in points:  # ascending m = ascending added total
        if point["qualifies"]:
            return {
                "m": point["m"],
                "added_total": point["added_total"],
                "per_site_added": point["per_site_added"],
                "share_resolving": point["share_resolving"],
                "binomial_sd": point["binomial_sd"]}
    return None


def grid_table(points):
    return [{
        "m": p["m"], "added_total": p["added_total"],
        "share_resolving": p["share_resolving"],
        "binomial_sd": p["binomial_sd"],
        "n_resolving": p["n_resolving"],
        "qualifies": p["qualifies"],
        "cells_included_by_trial":
            sorted({t["cells_included"] for t in p["trials"]}),
    } for p in points]


def headline_for(t1, t2):
    if t1 and t2:
        return "TARGET UNDER BOTH SCENARIOS"
    if t1:
        return "TARGET UNDER SCENARIO 1 ONLY"
    if t2:
        return "TARGET UNDER SCENARIO 2 ONLY"
    return "NO TARGET UNDER EITHER SCENARIO"


def _per_site_str(dist):
    return "; ".join(f"{s} {dist[s]}" for s in
                     ["Mohenjo-daro", "Dholavira", "Lothal",
                      "Chanhu-daro", "Kalibangan"])


def outcome_paragraph(headline, t1, t2):
    fence = ("This is a measurement of the test's "
             "resolution on recorded data. It is not "
             "evidence about the ancient world, and it "
             "does not change Arm A's INCONCLUSIVE "
             "verdict.")
    if headline == "TARGET UNDER BOTH SCENARIOS":
        big = max(t1["added_total"], t2["added_total"])
        return (
            "From Phase-393's recorded resampling "
            "distribution, the precision computation "
            "returns an intake target for Spec 028 Arm A "
            "under both stated scenarios. If the true "
            "effect is at the current point estimate "
            "(0.00878, below the margin), "
            f"{t1['added_total']} added non-Harappa "
            f"inscriptions (multiple {t1['m']}; per-site "
            f"{_per_site_str(t1['per_site_added'])}) make "
            "the interval resolve downward at the 0.01 "
            "margin in at least 80% of trials. If the "
            "true effect is 0.015, "
            f"{t2['added_total']} added inscriptions "
            f"(multiple {t2['m']}; per-site "
            f"{_per_site_str(t2['per_site_added'])}) make "
            "it resolve upward. The intake target that "
            "resolves Arm A under either scenario is "
            f"the larger, {big} (DD-061-5). " + fence)
    if headline == "TARGET UNDER SCENARIO 1 ONLY":
        return (
            "From Phase-393's recorded resampling "
            "distribution, the precision computation "
            "returns an intake target under Scenario 1 "
            f"only: {t1['added_total']} added non-Harappa "
            f"inscriptions (multiple {t1['m']}; per-site "
            f"{_per_site_str(t1['per_site_added'])}) "
            "resolve Arm A downward at the 0.01 margin "
            "if the true effect is at the current point "
            "estimate (0.00878). Under Scenario 2 (true "
            "effect 0.015), no grid point inside the "
            "frozen search frame (integer multiples "
            "m = 1..25; ceiling m = 25) qualified, so "
            "no upward target is returned. " + fence)
    if headline == "TARGET UNDER SCENARIO 2 ONLY":
        return (
            "From Phase-393's recorded resampling "
            "distribution, the precision computation "
            "returns an intake target under Scenario 2 "
            f"only: {t2['added_total']} added non-Harappa "
            f"inscriptions (multiple {t2['m']}; per-site "
            f"{_per_site_str(t2['per_site_added'])}) "
            "resolve Arm A upward at the 0.01 margin if "
            "the true effect is 0.015. Under Scenario 1 "
            "(true effect at the current point estimate, "
            "0.00878), no grid point inside the frozen "
            "search frame (integer multiples m = 1..25; "
            "ceiling m = 25) qualified, so no downward "
            "target is returned. " + fence)
    return (
        "From Phase-393's recorded resampling "
        "distribution, the precision computation "
        "returns **no intake target that resolves Arm "
        "A at the 0.01 margin under either stated "
        "scenario**, within the frozen search frame "
        "(grid integer multiples m = 1..25; ceiling "
        "m = 25; 199 trials per point). The grid "
        "table is published with this record so the "
        "near misses are visible. Spec 028 Arm A "
        "stands INCONCLUSIVE with no computed intake "
        "target; the contingent rerun (Arm A2) has no "
        "target to arm on, and its trigger (section 6 "
        "of the adjudication) does not fire on this "
        "record.")


def closure_paragraph(closure: Closure):
    if closure.outcome == "INVALID":
        return (f"The precision computation did not run: "
                f"gate {closure.gate} failed "
                f"({closure.detail}). No target quantity "
                f"was computed. Spec 028 Arm A stands "
                f"exactly as recorded.")
    if closure.gate == "0.5-R":
        return (f"The precision computation did not "
                f"run: gate 0.5-R (construction "
                f"calibration) failed ({closure.detail}). "
                f"The repaired construction cannot "
                f"impose the scenario's theta on the "
                f"drawn-population calibration, and no "
                f"other construction may be supplied at "
                f"run time. No target quantity was "
                f"computed. Spec 028 Arm A stands "
                f"exactly as recorded.")
    return (f"The precision computation did not run: "
            f"gate {closure.gate} failed "
            f"({closure.detail}), and those values may "
            f"not be supplied at run time. No target "
            f"quantity was computed.")


def base_record():
    return {
        "experiment": "spec062-phase424-arm-a-precision-calibration-repair",
        "phase": 424,
        "spec": "specs/062-arm-a-precision-calibration-repair/spec.md",
        "freeze_digest": FREEZE_DIGEST,
        "osf_registration": "https://osf.io/4m27t/",
        "simulation_label": (
            "SIMULATION OVER RECORDED DATA: this "
            "computation resamples Phase-393's recorded "
            "site samples; its added inscriptions are "
            "resamples of recorded inscriptions, not "
            "new data and not data the program holds."),
        "claim_under_test": "STUDY-SPEC-028/ARM-A",
        "margin": MARGIN,
        "scenarios": {"scenario_1": {"theta": THETAS[1],
                                     "direction": "downward"},
                      "scenario_2": {"theta": THETAS[2],
                                     "direction": "upward"}},
        "search_frame": {
            "grid": "integer multiples m = 1..25, step 1",
            "ceiling_m": CEILING,
            "trials_per_grid_point": TRIALS,
            "draws_per_trial": P.DRAWS,
            "permutations_per_draw": P.PERMS,
            "simulation_seed": SIM_SEED,
            "effect_imposition": (
                "candidate (b) imposed compositions "
                "(DD-061-13 steps 1-2, carried) with the "
                "calibration of step 3 replaced by "
                "construction R-1 (spec section 4.7-R; "
                "DD-062-9): per-inscription Dirichlet "
                "drawing around the imposed composition, "
                "kappa_i = n_legible(i) - 1, fixed "
                "uniforms and rarefaction selections "
                "from the dedicated calibration "
                "Generator seeded 20261021 (DD-062-7); "
                "A_R the median of 199 draw statistics; "
                "bisection on [1, 3] to 1e-6, verified "
                "at gate 0.5-R"),
            "qualification": "share resolving >= 0.80",
            "resolution": "strict exclusion of the 0.01 "
                          "margin in the scenario's "
                          "direction (DD-061-2)"},
        "outcome": None,
        "headline_paragraph": None,
        "fence_sentence": (
            "This computation measures the resolution "
            "of a recorded test. It establishes nothing "
            "about the ancient world."),
    }


def write_outputs(res: dict):
    RESULTS_PATH.write_text(json.dumps(res, indent=1) + "\n",
                            encoding="utf-8")
    REPORT_PATH.write_text(write_report(res),
                           encoding="utf-8")


def write_report(res: dict) -> str:
    L = []
    L.append("# Phase-424 — Spec 062: Spec 028 Arm A, "
             "the Precision Computation, Calibration "
             "Repair (D-27, arm A1)")
    L.append("")
    L.append("**SIMULATION OVER RECORDED DATA.** This "
             "computation is a simulation over recorded "
             "data — Phase-393's recorded resampling "
             "distribution and the recorded site samples. "
             "Its added inscriptions are resamples of "
             "recorded inscriptions; they are not new "
             "data, and no part of this record describes "
             "them as data the program holds.")
    L.append("")
    L.append(f"**Outcome: {res['outcome']}**")
    L.append("")
    L.append(res["headline_paragraph"])
    L.append("")
    L.append("Both scenario values: theta_1 = "
             "0.00878393455594817 (the recorded point "
             "estimate, stated as 0.00878 in the design; "
             "resolves downward) and theta_2 = 0.015 "
             "(resolves upward); the margin is adjusted "
             "R^2 0.01.")
    L.append("")
    if res.get("gates"):
        L.append("## Step 0 gates")
        L.append("")
        for g in res["gates"]:
            L.append(f"- Gate {g['gate']}: {g['verdict']}")
        L.append("")
    if res.get("grid"):
        for scen in ("scenario_1", "scenario_2"):
            g = res["grid"][scen]
            cal = res["calibration"][scen]
            L.append(f"## Grid — {scen} "
                     f"(theta = {g['theta']}; boost "
                     f"b = {cal['boost_b']}, "
                     f"A_R(b) = {cal['A_at_b']})")
            L.append("")
            L.append("| m | Added total | Share resolving "
                     "| Binomial SD | Qualifies |")
            L.append("|---|---|---|---|---|")
            for row in g["table"]:
                L.append(f"| {row['m']} | "
                         f"{row['added_total']} | "
                         f"{row['share_resolving']:.4f} | "
                         f"{row['binomial_sd']:.4f} | "
                         f"{'yes' if row['qualifies'] else 'no'} |")
            L.append("")
            t = g["target"]
            if t:
                L.append(f"Target: {t['added_total']} added "
                         f"inscriptions at multiple "
                         f"{t['m']}; per-site added: "
                         f"{_per_site_str(t['per_site_added'])}; "
                         f"qualifying share "
                         f"{t['share_resolving']:.4f}.")
            else:
                L.append("Target: NO TARGET (within the "
                         "frozen search frame).")
            L.append("")
    if res.get("operative_target") is not None:
        L.append(f"Operative target T* (the DD-061-5 rule "
                 f"carried as this spec's own): "
                 f"{res['operative_target']} added "
                 "inscriptions"
                 + (f" ({res['operative_target_condition']})"
                    if res.get("operative_target_condition")
                    else "")
                 + ". Recording it arms nothing by itself: "
                 "Arm A2 is not part of this pass (E-3); "
                 "a fired trigger queues a mini planning "
                 "gate.")
        L.append("")
    L.append("Frozen search frame in full: integer grid "
             "m = 1..25 (step 1); ceiling m = 25 (added "
             "total 38,232; world total 39,825); 199 "
             "trials per grid point; 199 draws and 499 "
             "trial, seed 20261021; effect imposition by candidate "
             "(b)'s imposed compositions with the "
             "boost calibrated per scenario under "
             "construction R-1 (per-inscription "
             "Dirichlet drawing, fixed uniforms, "
             "calibration seed 20261021) on [1, 3] to "
             "tolerance 1e-6 (gate 0.5-R).")
    L.append("")
    L.append("This computation measures the resolution "
             "of a recorded test. It establishes nothing "
             "about the ancient world.")
    L.append("")
    return "\n".join(L)


def assemble(step0_record):
    points = {}
    for scen in (1, 2):
        d = scenario_dir(scen)
        pts = []
        for m in GRID:
            p = d / f"m{m:02d}.json"
            if not p.exists():
                raise SystemExit(
                    f"scenario {scen} incomplete: m={m} "
                    "missing")
            pts.append(json.loads(p.read_text(
                encoding="utf-8")))
        points[scen] = pts
    t1 = scenario_target(points[1])
    t2 = scenario_target(points[2])
    headline = headline_for(t1, t2)
    res = base_record()
    res["gates"] = step0_record["gates"]
    res["calibration"] = {
        f"scenario_{s}": step0_record["calibration"][str(s)]
        for s in (1, 2)}
    res["grid"] = {
        f"scenario_{s}": {
            "theta": THETAS[s],
            "table": grid_table(points[s]),
            "trial_intervals": [
                {"m": p["m"],
                 "intervals": [t["interval"]
                               for t in p["trials"]]}
                for p in points[s]],
            "target": ({"scenario": s, **t}
                       if (t := (t1 if s == 1 else t2))
                       else None),
        } for s in (1, 2)}
    res["targets"] = {"scenario_1": t1, "scenario_2": t2}
    if t1 and t2:
        big = max(t1, t2, key=lambda t: t["added_total"])
        res["operative_target"] = big["added_total"]
        res["operative_target_condition"] = None
    elif t1 or t2:
        only = t1 or t2
        res["operative_target"] = only["added_total"]
        res["operative_target_condition"] = (
            "scenario 1 only" if t1 else "scenario 2 only")
    else:
        res["operative_target"] = None
        res["operative_target_condition"] = None
    res["outcome"] = headline
    res["headline_paragraph"] = outcome_paragraph(
        headline, t1, t2)
    res["anchors_sha256_after"] = sha256_file(
        ROOT / ANCHORS_REL)
    write_outputs(res)
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step0-only", action="store_true")
    ap.add_argument("--scenario", type=int, choices=(1, 2))
    ap.add_argument("--assemble", action="store_true")
    args = ap.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    step0_path = WORK / "step0.json"
    anchors_before = sha256_file(ROOT / ANCHORS_REL)
    try:
        pop, pooled, calibration, gates = run_step0()
    except Closure as c:
        res = base_record()
        res["outcome"] = c.outcome
        res["closure"] = {"gate": c.gate, "detail": c.detail}
        res["headline_paragraph"] = closure_paragraph(c)
        res["anchors_sha256_after"] = sha256_file(
            ROOT / ANCHORS_REL)
        write_outputs(res)
        print(json.dumps({"outcome": c.outcome,
                          "gate": c.gate,
                          "detail": c.detail}, indent=1))
        return 0
    step0_record = {
        "gates": gates,
        "calibration": {str(k): v
                        for k, v in calibration.items()},
        "anchors_sha256_before": anchors_before}
    step0_path.write_text(json.dumps(step0_record, indent=1)
                          + "\n", encoding="utf-8")
    print(json.dumps({"step0": "PASS",
                      "calibration": step0_record[
                          "calibration"]}, indent=1),
          flush=True)
    if args.step0_only:
        return 0
    if args.scenario:
        run_scenario(args.scenario, pop, pooled,
                     calibration)
        return 0
    if args.assemble:
        res = assemble(step0_record)
        print(json.dumps({"outcome": res["outcome"],
                          "targets": res["targets"],
                          "operative_target":
                              res["operative_target"]},
                         indent=1))
        return 0
    # Default: both scenarios in sequence, then assemble.
    run_scenario(1, pop, pooled, calibration)
    run_scenario(2, pop, pooled, calibration)
    res = assemble(step0_record)
    print(json.dumps({"outcome": res["outcome"],
                      "targets": res["targets"],
                      "operative_target":
                          res["operative_target"]},
                     indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
