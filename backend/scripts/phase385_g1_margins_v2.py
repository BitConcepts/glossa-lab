"""Phase-385 v2 (Spec 026) — C1 margin completion for Phase-140
(G1), corrected interval.

v1 (phase385_g1_margins.py, frozen digest 8af60b985d9994bc…)
resampled inscriptions within the frozen strata — the correct
sampling unit — but reported only the percentile interval of a
statistic (Cramer's V) whose plug-in bias grows under
resampling; the v1 percentile CI [0.2282, 0.2537] excluded the
point estimate 0.2190. v2 (own contract + freeze:
phase385-contract-v2.md / phase385-freeze-v2.json) keeps the
v1 design and adds the BASIC bootstrap interval
[2V - q97.5, 2V - q2.5] as the governing interval for the
margin adjudication, with B raised to 4,999 and seed 20261012.
The v1 execution is preserved in the Phase-385 report.

Rerun contract: specs/026-rcph-framework-transfer/reruns/
phase385-contract.md (frozen at the S3 merge; freeze record
phase385-freeze.json). G1's SUPPORTED-under-control verdict
rested on the controlled permutation p-value (0/9,999) with a
point Cramer's V of 0.2190 and no interval. This rerun:

1. Rebuilds the Phase-140 population with the Phase-140 module's
   own loaders and asserts the recorded quantities (5,410
   inscriptions, 7 sites, observed chi2 4966.362228365138).
2. Computes a stratified bootstrap 95% CI for Cramer's V:
   inscriptions resampled WITHIN the frozen G1 strata
   (composition x preservation, UNRECORDED retained as a level),
   B = 1,999, seed 20261011.
3. Adjudicates against the margin declared in the contract
   BEFORE this run: V = 0.10. Exploratory companions: the same
   bootstrap within composition x chron_band and composition x
   depth_band strata (Phase-140's sensitivity designs), CIs
   only, labeled EXPLORATORY.

The permutation result is NOT recomputed and NOT altered.
Chronology remains NOT controlled in the primary design; the
rider travels with every G1 statement this phase emits.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "backend" / "scripts"
DEFAULT_OUT = REPO_ROOT / "reports" / "phase385_results.json"

SEED = 20261012
B_BOOT = 4999
MARGIN_V = 0.10
EXPECTED_CHI2 = 4966.362228365138

CHRONOLOGY_RIDER = (
    "chronology is NOT controlled in the primary test — "
    "period/phase remain uncontrolled confounders"
)


def _load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _chi2_v(table: np.ndarray) -> float:
    t = table.astype(float)
    row = t.sum(axis=1, keepdims=True)
    col = t.sum(axis=0, keepdims=True)
    grand = t.sum()
    exp = row @ col / grand
    mask = exp > 0
    chi2 = float((((t - exp) ** 2) / np.where(mask, exp, 1.0))[mask].sum())
    return float(np.sqrt(chi2 / (grand * min(t.shape[0] - 1, t.shape[1] - 1))))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    p140 = _load_module("phase140_g1_controlled")
    p137 = p140._SPEC137_LOADER if hasattr(p140, "_SPEC137_LOADER") else None
    # phase140 loads the Phase-137 module at import time as `p137`.
    p137 = p140.__dict__.get("p137") or p137
    if p137 is None:
        raise SystemExit("phase140 module did not expose its p137 loader")

    assert p140.sha256_of(p140.HORUS84) == p140.LAYER_SHA256, "layer hash drift"
    inscriptions = p140.load_horus_with_id(p140.HORUS84)
    per_site_insc: Counter = Counter()
    per_site_parsed: Counter = Counter()
    for insc in inscriptions:
        per_site_insc[insc["site"]] += 1
        per_site_parsed[insc["site"]] += insc["n_parsed_tokens"]
    eligible = sorted(
        s for s in per_site_insc
        if p137.site_eligible(per_site_insc[s], per_site_parsed[s])
    )
    analysis = [
        i for i in inscriptions
        if i["site"] in set(eligible) and i["n_parsed_tokens"] >= 1
    ]
    assert len(analysis) == 5410, len(analysis)

    sign_counts: Counter = Counter()
    for insc in analysis:
        sign_counts.update(insc["tokens"])
    kept_signs = sorted(
        s for s, c in sign_counts.items() if c >= p140.MIN_SIGN_COUNT
    )
    other_tokens = sum(
        c for s, c in sign_counts.items() if c < p140.MIN_SIGN_COUNT
    )
    columns = kept_signs + ([p137.OTHER] if other_tokens else [])
    col_index = {s: j for j, s in enumerate(kept_signs)}
    other_idx = len(kept_signs) if other_tokens else None
    site_index = {s: j for j, s in enumerate(eligible)}

    cov_rows = json.loads(p140.COVARIATES.read_text("utf-8"))
    cov_by_id = {r["id"]: r for r in cov_rows}
    assert len(cov_by_id) == 5410

    # Per-inscription sparse token vectors + stratum keys.
    vecs: list[tuple[tuple[int, int], ...]] = []
    site_of: list[int] = []
    keys_primary: list[str] = []
    keys_chron: list[str] = []
    keys_depth: list[str] = []
    table = np.zeros((len(eligible), len(columns)), dtype=np.int64)
    for insc in analysis:
        row = cov_by_id[insc["id"]]
        assert row["site"] == insc["site"]
        assert row["composition_stratum"] == insc["stratum"]
        vec: Counter = Counter()
        for tok in insc["tokens"]:
            vec[col_index.get(tok, other_idx)] += 1
        items = tuple(sorted(vec.items()))
        vecs.append(items)
        si = site_index[insc["site"]]
        site_of.append(si)
        for col_idx, count in items:
            table[si, col_idx] += count
        keys_primary.append(f"{insc['stratum']}|{row['preservation_class']}")
        keys_chron.append(f"{insc['stratum']}|{row['chron_band']}")
        keys_depth.append(f"{insc['stratum']}|{row['depth_band']}")

    # Verification against the recorded marginal computation.
    t = table.astype(float)
    r = t.sum(axis=1, keepdims=True)
    c = t.sum(axis=0, keepdims=True)
    exp = r @ c / t.sum()
    mask = exp > 0
    chi2 = float((((t - exp) ** 2) / np.where(mask, exp, 1.0))[mask].sum())
    rel = abs(chi2 - EXPECTED_CHI2) / EXPECTED_CHI2
    if rel > 1e-6:
        raise SystemExit(f"observed chi2 mismatch: {chi2} vs {EXPECTED_CHI2}")
    v_point = _chi2_v(table)
    print(f"step 1 OK: population 5410 / {len(eligible)} sites; "
          f"chi2 {chi2:.6f}; V {v_point:.4f}")
    if args.verify_only:
        return 0

    site_arr = np.array(site_of)
    n_sites, n_cols = table.shape

    def stratified_bootstrap(strata_keys: list[str]) -> dict:
        # returns percentile + basic intervals for V
        groups: dict[str, list[int]] = {}
        for i, k in enumerate(strata_keys):
            groups.setdefault(k, []).append(i)
        group_idx = [np.array(v) for v in groups.values()]
        rng = np.random.default_rng(SEED)
        boots = np.empty(B_BOOT)
        for b in range(B_BOOT):
            bt = np.zeros((n_sites, n_cols), dtype=np.int64)
            for g in group_idx:
                sel = rng.choice(g, size=len(g), replace=True)
                for i in sel:
                    for col_idx, count in vecs[i]:
                        bt[site_arr[i], col_idx] += count
            boots[b] = _chi2_v(bt)
        lo, hi = np.percentile(boots, [2.5, 97.5])
        return {
            "percentile_ci95": [float(lo), float(hi)],
            "basic_ci95": [float(2 * v_point - hi), float(2 * v_point - lo)],
            "bootstrap_median": float(np.median(boots)),
        }

    ci_primary = stratified_bootstrap(keys_primary)
    ci_chron = stratified_bootstrap(keys_chron)
    ci_depth = stratified_bootstrap(keys_depth)

    adjudication = (
        "basic CI lower bound > 0.10: SUPPORTED under control "
        "stands at the declared margin"
        if ci_primary["basic_ci95"][0] > MARGIN_V else
        "basic CI crosses 0.10: INCONCLUSIVE at the declared margin"
    )
    results = {
        "phase": "Phase-385",
        "spec": "026",
        "reruns": "Phase-140 (G1) — C1 margin completion",
        "version": "v2 (governing interval: basic bootstrap; v1 percentile-only interval superseded — see report)",
        "contract": "specs/026-rcph-framework-transfer/reruns/phase385-contract-v2.md",
        "chronology_rider": CHRONOLOGY_RIDER,
        "parameters": {"B_bootstrap": B_BOOT, "seed": SEED, "margin_v": MARGIN_V, "governing_interval": "basic bootstrap"},
        "verification": {
            "population_inscriptions": len(analysis),
            "sites": len(eligible),
            "observed_chi2_recomputed": chi2,
            "observed_chi2_recorded": EXPECTED_CHI2,
            "cramers_v_point": v_point,
        },
        "g1_primary": {
            "strata": "composition x preservation (UNRECORDED retained as a level)",
            "bootstrap_v_intervals": ci_primary,
            "margin_adjudication": adjudication,
            "recorded_permutation": {
                "count_perm_ge_observed": 0, "B": 9999, "p_value_raw": 0.0001,
                "note": "Phase-140 recorded result, reported alongside; "
                        "not recomputed by this rerun.",
            },
        },
        "sensitivities_exploratory": {
            "S_chron_composition_x_chron_band": {"bootstrap_v_intervals": ci_chron},
            "S_depth_composition_x_depth_band": {"bootstrap_v_intervals": ci_depth},
        },
        "ai_disclosure": (
            "Executed by an AI agent (Muse Spark, via Muse) "
            "at the direction of Tristen Pierson, per constitution sec.VI."
        ),
    }
    args.out.write_text(json.dumps(results, indent=1), "utf-8")
    print("primary intervals:", ci_primary, "->", adjudication)
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
