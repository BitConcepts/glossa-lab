"""Phase-384 v2 (Spec 026) — C1 margin completion for Phase-137
F2/F3, CORRECTED procedure.

Why v2 exists: the v1 frozen procedure (parametric bootstrap
over table CELLS, treating profile tokens as independent
draws) was shown NON-DISCRIMINATING by its own independence
control: applied to an independence table with F2's margins it
returned a 95% CI of [0.1115, 0.1242] for a true V of 0 (F3
shape: [0.0984, 0.1095]). Under the framework's
discriminating-control rule the v1 interval adjudication is
INVALID. The v1 execution and the control are preserved in the
Phase-384 report; this v2 runs under its own contract + freeze
(phase384-contract-v2.md / phase384-freeze-v2.json), frozen
before execution.

v2 procedure (the correction): the sampling unit is the
INSCRIPTION. Populations are rebuilt with the Phase-137
module's own loaders and population rule; the rebuilt profile
tables are asserted EQUAL to the tables recorded in
reports/phase137_results.json. Inscriptions are resampled
with replacement WITHIN each site (site sizes fixed); the
profile table and Cramer's V are recomputed per replicate
(B = 9,999, seed 20261012). Intervals: percentile (reported)
and BASIC bootstrap interval [2V - q97.5, 2V - q2.5]
(governing for the margin adjudication — the basic interval
corrects the plug-in bias of V under resampling).

Margin + verdict rules: unchanged from v1 (margin V = 0.10,
declared in the v1 contract before any run).
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
RESULTS_137 = REPO_ROOT / "reports" / "phase137_results.json"
DEFAULT_OUT = REPO_ROOT / "reports" / "phase384_results.json"

SEED = 20261012
B_BOOT = 9999
MARGIN_V = 0.10


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _chi2_v(table: np.ndarray) -> tuple[float, float]:
    t = table.astype(float)
    row = t.sum(axis=1, keepdims=True)
    col = t.sum(axis=0, keepdims=True)
    grand = t.sum()
    exp = row @ col / grand
    mask = exp > 0
    chi2 = float((((t - exp) ** 2) / np.where(mask, exp, 1.0))[mask].sum())
    v = float(np.sqrt(chi2 / (grand * min(t.shape[0] - 1, t.shape[1] - 1))))
    return chi2, v


def build_population(p137, inscriptions):
    """Mirror analyse_layer's frozen population rule with the
    module's own pieces; return (table, per-site sparse vecs)."""
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
    sign_counts: Counter = Counter()
    for insc in analysis:
        sign_counts.update(insc["tokens"])
    kept = sorted(s for s, c in sign_counts.items() if c >= p137.MIN_SIGN_COUNT)
    other_tokens = sum(c for s, c in sign_counts.items() if c < p137.MIN_SIGN_COUNT)
    columns = kept + ([p137.OTHER] if other_tokens else [])
    col_index = {s: j for j, s in enumerate(kept)}
    other_idx = len(kept) if other_tokens else None
    site_index = {s: j for j, s in enumerate(eligible)}
    table = np.zeros((len(eligible), len(columns)), dtype=np.int64)
    by_site: dict[int, list[tuple[tuple[int, int], ...]]] = {}
    for insc in analysis:
        vec: Counter = Counter()
        for tok in insc["tokens"]:
            vec[col_index.get(tok, other_idx)] += 1
        items = tuple(sorted(vec.items()))
        si = site_index[insc["site"]]
        by_site.setdefault(si, []).append(items)
        for col_idx, count in items:
            table[si, col_idx] += count
    return table, by_site, len(analysis)


def bootstrap_within_site(table, by_site, rng):
    n_sites, n_cols = table.shape
    groups = [by_site[i] for i in range(n_sites)]
    boots = np.empty(B_BOOT)
    for b in range(B_BOOT):
        bt = np.zeros((n_sites, n_cols), dtype=np.int64)
        for si, vecs in enumerate(groups):
            sel = rng.integers(0, len(vecs), size=len(vecs))
            for j in sel:
                for col_idx, count in vecs[j]:
                    bt[si, col_idx] += count
        boots[b] = _chi2_v(bt)[1]
    return boots


def intervals(boots: np.ndarray, point: float) -> dict:
    q_lo, q_hi = np.percentile(boots, [2.5, 97.5])
    return {
        "bootstrap_median": float(np.median(boots)),
        "percentile_ci95": [float(q_lo), float(q_hi)],
        "basic_ci95": [float(2 * point - q_hi), float(2 * point - q_lo)],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    p137 = _load_module("phase137_site_repertoire",
                        SCRIPTS / "phase137_site_repertoire.py")
    committed = json.loads(RESULTS_137.read_text("utf-8"))["layers"]

    holdat_insc, _ = p137.load_holdat(p137.DEFAULT_HOLDAT)
    horus_insc, _ = p137.load_horus(p137.DEFAULT_HORUS)
    layer_inputs = {
        "F2_holdat": holdat_insc,
        "F3_icit_lineage": horus_insc,
    }

    rng = np.random.default_rng(SEED)
    members = {}
    for key, inscriptions in layer_inputs.items():
        table, by_site, n_analysis = build_population(p137, inscriptions)
        recorded = np.array(committed[key]["profile_table"]["counts"])
        if table.shape != recorded.shape or not (table == recorded).all():
            raise SystemExit(f"{key}: rebuilt table != recorded profile table")
        chi2, v = _chi2_v(table)
        rec_chi2 = committed[key]["observed_chi_square"]
        rec_v = committed[key]["cramers_v_descriptive"]
        if abs(chi2 - rec_chi2) / rec_chi2 > 1e-9 or abs(v - rec_v) > 1e-9:
            raise SystemExit(f"{key}: chi2/V mismatch vs record")
        boots = bootstrap_within_site(table, by_site, rng)
        iv = intervals(boots, v)
        basic_lo, basic_hi = iv["basic_ci95"]
        if key.startswith("F3"):
            adjudication = (
                "basic CI lower bound > 0.10: SUPPORTED stands at the declared margin"
                if basic_lo > MARGIN_V else
                "basic CI crosses 0.10: INCONCLUSIVE at the declared margin"
            )
        else:
            adjudication = (
                "basic CI upper bound < 0.10: bounded claim CONTRADICTED at the declared margin"
                if basic_hi < MARGIN_V else
                "basic CI crosses 0.10: INCONCLUSIVE at the declared margin"
            )
        members[key] = {
            "n_analysis_inscriptions": n_analysis,
            "recorded_chi2": rec_chi2, "recomputed_chi2": chi2,
            "recorded_v": rec_v, "recomputed_v": v,
            **iv,
            "margin_adjudication_basic_ci": adjudication,
        }
        print(key, "V", round(v, 4), "basic CI", iv["basic_ci95"],
              "->", adjudication)

    results = {
        "phase": "Phase-384",
        "spec": "026",
        "version": "v2 (corrected procedure; v1 interval adjudication INVALID — see report)",
        "reruns": "Phase-137 (F2/F3) — C1 margin completion",
        "contract": "specs/026-rcph-framework-transfer/reruns/phase384-contract-v2.md",
        "parameters": {"B_bootstrap": B_BOOT, "seed": SEED,
                       "margin_v": MARGIN_V,
                       "resampling": "inscriptions within site, site sizes fixed",
                       "governing_interval": "basic bootstrap"},
        "members": members,
        "ai_disclosure": (
            "Executed by an AI agent (Muse Spark, via Muse) "
            "at the direction of Tristen Pierson, per constitution sec.VI."
        ),
    }
    args.out.write_text(json.dumps(results, indent=1), "utf-8")
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
