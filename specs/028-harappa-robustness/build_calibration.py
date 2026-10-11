"""Spec 028 — pre-freeze calibration (SYNTHETIC DATA ONLY).

Runs the frozen-design controls for Arm A and Arm B through
the exact pipeline (pipeline393.py) on synthetic populations
templated on the real populations' margins (cell sizes,
per-inscription legible lengths, pooled composition). No real
site-by-sign structure enters any quantity here: synthetic
inscriptions are drawn from pooled or deterministically
perturbed pooled distributions, exactly as the frozen
control definitions require. Control populations are
regenerated per draw (freeze Amendment 1b). This is the
Phase-392 Amendment 1 calibration pattern: machinery
evidence from synthetic data only, gathered BEFORE the
freeze, used to confirm the design can discriminate at the
declared margin on each arm's population shape.

Seed: the frozen Spec 028 seed 20261012 (fresh, pre-declared
in the freeze). One RNG per arm, controls run in the
execution order (negative, then positive).
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_margins_audit as audit_mod
import pipeline393 as P

SEED = 20261012


def count_vector(entry, col_index, n_cols):
    vec = np.zeros(n_cols, dtype=np.float64)
    for tok, kind in zip(entry["tokens"], entry["kinds"]):
        if kind in ("direct", "chain"):
            vec[col_index.get(tok, col_index["OTHER"])] += 1.0
        elif kind == "unmapped":
            vec[col_index["UNMAPPED"]] += 1.0
    return vec


def main() -> int:
    t0 = time.time()
    keyed = json.loads(
        (audit_mod.STORE / "icit_converted_v2_keyed.json")
        .read_text(encoding="utf-8"))
    import csv
    horus = {}
    with open(audit_mod.STORE / "horus_inscriptions.csv",
              newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            horus[row["id"]] = row
    eligible, flow = audit_mod.build_eligible(keyed["inscriptions"],
                                              horus)
    assert flow["eligible_primary"] == 3144
    columns, _ = audit_mod.composition_columns(eligible)
    col_index = {c: i for i, c in enumerate(columns)}
    n_cols = len(columns)
    site_counts = Counter(e["site"] for e in eligible)
    analysis = [e for e in eligible
                if site_counts[e["site"]] >= audit_mod.MIN_SITE]
    assert len(analysis) == 3030

    audit = json.loads((HERE / "margins-audit.json")
                       .read_text(encoding="utf-8"))

    def pooled_probs(subset):
        counts = np.zeros(n_cols)
        for e in subset:
            counts += count_vector(e, col_index, n_cols)
        return counts / counts.sum()

    def run_arm(name, template, eligible_subset, sites, sets,
                control_runner):
        rng = np.random.default_rng(SEED)
        pooled = pooled_probs(eligible_subset)
        neg = P.summarise(control_runner(
            template, {s: pooled for s in sites}, rng))
        pos_probs = {}
        for s in sites:
            p = pooled.copy()
            idx = [col_index[c] for c in sets[s]]
            p[idx] *= P.POSITIVE_BOOST
            pos_probs[s] = p / p.sum()
        pos = P.summarise(control_runner(template, pos_probs, rng))
        out = {
            "negative_control": dict(
                neg, **{"pass": P.negative_control_pass(neg)}),
            "positive_control": dict(
                pos, **{"pass": P.positive_control_pass(pos)}),
        }
        print(f"[{time.time()-t0:.0f}s] {name}: "
              f"neg median {neg['median_adj_r2']:.5f} "
              f"pass={out['negative_control']['pass']}; "
              f"pos median {pos['median_adj_r2']:.5f} "
              f"interval {pos['adj_r2_interval_95']} "
              f"pass={out['positive_control']['pass']}",
              flush=True)
        return out

    arm_a = [e for e in analysis if e["site"] != "Harappa"]
    arm_a_eligible = [e for e in eligible if e["site"] != "Harappa"]
    res_a = run_arm(
        "arm_a", arm_a, arm_a_eligible, audit_mod.ARM_A_SITES,
        audit["arm_a_harappa_excluded"]["positive_control_sign_sets"],
        lambda t, probs, r: P.run_control_cells(t, probs, r))
    res_b = run_arm(
        "arm_b", analysis, eligible, audit_mod.PHASE392_ANALYSIS_SITES,
        audit["arm_b_site_equal"]["positive_control_sign_sets"],
        lambda t, probs, r: P.run_control_quota(t, probs, r))

    out = {
        "calibration": "spec028-synthetic-only",
        "seed": SEED,
        "real_outcomes_computed": False,
        "arm_a": res_a,
        "arm_b": res_b,
        "elapsed_s": round(time.time() - t0, 1),
    }
    text = json.dumps(out, indent=1)
    print(text)
    out_path = os.environ.get("SPEC028_CALIB_OUT")
    if out_path:
        Path(out_path).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
