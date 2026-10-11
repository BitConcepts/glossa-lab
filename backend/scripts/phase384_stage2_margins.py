"""Phase-384 (Spec 026) — C1 margin completion for Phase-137 F2/F3.

Rerun contract: specs/026-rcph-framework-transfer/reruns/
phase384-contract.md (frozen at the S3 merge; freeze record
phase384-freeze.json). The F2/F3 verdicts of Phase-137 rested on
permutation p-values with point Cramer's V only. This rerun:

1. Recomputes chi-square and Cramer's V from the profile tables
   recorded in reports/phase137_results.json and asserts they
   match the recorded values (the tables are the recorded
   computation's sufficient statistics — no layer rebuild).
2. Computes a parametric bootstrap 95% CI for V per family
   member (per site row: multinomial resample of the row total
   over the row's recorded column proportions; B = 9,999;
   seed 20261011).
3. Adjudicates against the practical margin declared in the
   contract BEFORE this run: V = 0.10.

Reads only registered files (H16). Deterministic given the seed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_137 = REPO_ROOT / "reports" / "phase137_results.json"
DEFAULT_OUT = REPO_ROOT / "reports" / "phase384_results.json"

SEED = 20261011
B_BOOT = 9999
MARGIN_V = 0.10

EXPECTED = {
    "F2_holdat": {"chi2": 745.9530278664314, "v": 0.11539837515155221},
    "F3_icitin": None,  # resolved from the results file keys at runtime
}


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chi2_and_v(table: np.ndarray) -> tuple[float, float]:
    table = table.astype(float)
    row_tot = table.sum(axis=1, keepdims=True)
    col_tot = table.sum(axis=0, keepdims=True)
    grand = table.sum()
    expected = row_tot @ col_tot / grand
    mask = expected > 0
    chi2 = float((((table - expected) ** 2) / np.where(mask, expected, 1.0))[mask].sum())
    n_rows, n_cols = table.shape
    v = math.sqrt(chi2 / (grand * min(n_rows - 1, n_cols - 1)))
    return chi2, v


def bootstrap_v(table: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    table = table.astype(float)
    row_tot = table.sum(axis=1).astype(int)
    probs = table / np.where(row_tot[:, None] > 0, row_tot[:, None], 1)
    out = np.empty(B_BOOT)
    for b in range(B_BOOT):
        resampled = np.array(
            [
                rng.multinomial(int(row_tot[i]), probs[i])
                for i in range(table.shape[0])
            ]
        )
        _, out[b] = chi2_and_v(resampled)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--verify-only", action="store_true",
                    help="run only step 1 (table verification)")
    args = ap.parse_args()

    doc = json.loads(RESULTS_137.read_text("utf-8"))
    layers = doc["layers"]
    members = {}
    for key, layer in layers.items():
        table = np.array(layer["profile_table"]["counts"], dtype=float)
        chi2, v = chi2_and_v(table)
        members[key] = {
            "table": table,
            "recorded_chi2": layer["observed_chi_square"],
            "recorded_v": layer["cramers_v_descriptive"],
            "recomputed_chi2": chi2,
            "recomputed_v": v,
        }
        for name, rec, got in (
            ("chi2", layer["observed_chi_square"], chi2),
            ("v", layer["cramers_v_descriptive"], v),
        ):
            rel = abs(rec - got) / max(abs(rec), 1e-12)
            if rel > 1e-6:
                raise SystemExit(
                    f"{key}: recorded {name}={rec} != recomputed {got} (rel {rel})"
                )
    print("step 1 OK: recorded tables reproduce recorded chi2/V for",
          ", ".join(members))
    if args.verify_only:
        return 0

    rng = np.random.default_rng(SEED)
    results: dict = {
        "phase": "Phase-384",
        "spec": "026",
        "reruns": "Phase-137 (F2/F3) — C1 margin completion",
        "contract": "specs/026-rcph-framework-transfer/reruns/phase384-contract.md",
        "parameters": {"B_bootstrap": B_BOOT, "seed": SEED, "margin_v": MARGIN_V},
        "inputs": {"phase137_results_sha256": sha256_of(RESULTS_137)},
        "members": {},
        "ai_disclosure": (
            "Executed by an AI agent (Muse Spark, via Muse) "
            "at the direction of Tristen Pierson, per constitution sec.VI."
        ),
    }
    for key, m in members.items():
        boot = bootstrap_v(m["table"], rng)
        lo, hi = np.percentile(boot, [2.5, 97.5])
        entry = {
            "recorded_chi2": m["recorded_chi2"],
            "recorded_v": m["recorded_v"],
            "recomputed_chi2": m["recomputed_chi2"],
            "recomputed_v": m["recomputed_v"],
            "bootstrap_v_median": float(np.median(boot)),
            "bootstrap_v_ci95": [float(lo), float(hi)],
        }
        if key.startswith("F3"):
            entry["margin_adjudication"] = (
                "CI lower bound > 0.10: SUPPORTED stands at the declared margin"
                if lo > MARGIN_V else
                "CI crosses 0.10: INCONCLUSIVE at the declared margin"
            )
        elif key.startswith("F2"):
            entry["margin_adjudication"] = (
                "CI upper bound < 0.10: bounded claim CONTRADICTED at the declared margin"
                if hi < MARGIN_V else
                "CI crosses 0.10: INCONCLUSIVE at the declared margin"
            )
        results["members"][key] = entry
        print(key, entry["bootstrap_v_ci95"], "->", entry["margin_adjudication"])

    args.out.write_text(json.dumps(results, indent=1), "utf-8")
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
