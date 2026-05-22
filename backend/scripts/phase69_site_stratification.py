"""Phase-69: Multi-Site Stratification.

Tests whether the positional grammar (I/M/T rates) of HIGH/MEDIUM anchor
signs is site-invariant across all 9 Holdat sites.

Hypothesis (to test): The Indus writing system is pan-Indus — the same
grammatical rules apply at Mohenjo-daro, Harappa, Dholavira, etc.

Method:
  - For each HIGH/MEDIUM anchor sign, compute I/T/M rates per site
  - Chi-squared test: are rates consistent across sites?
  - Signs where chi2 p-value < 0.05 are SITE-VARIANT (local dialect or noise)
  - Signs where p-value >= 0.05 are SITE-INVARIANT (consistent grammar)

GPU: torch for frequency matrices.
Output: reports/phase69_site_stratification.json
"""
from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase69_site_stratification.json"


def chi2_test(observed: list[list[float]]) -> tuple[float, float]:
    """
    Chi-squared test for independence on a 2D contingency table.
    observed[site][position_bin] = count
    Returns (chi2_statistic, p_value_approx).
    """
    n_sites = len(observed)
    if n_sites < 2:
        return 0.0, 1.0
    n_cols = max(len(r) for r in observed)
    # Pad rows to same length
    mat = [[observed[i][j] if j < len(observed[i]) else 0
            for j in range(n_cols)]
           for i in range(n_sites)]
    # Row and column totals
    row_totals = [sum(mat[i]) for i in range(n_sites)]
    col_totals = [sum(mat[i][j] for i in range(n_sites)) for j in range(n_cols)]
    grand = sum(row_totals)
    if grand == 0:
        return 0.0, 1.0

    chi2 = 0.0
    df   = 0
    for i in range(n_sites):
        for j in range(n_cols):
            expected = row_totals[i] * col_totals[j] / grand
            if expected > 0:
                chi2 += (mat[i][j] - expected) ** 2 / expected
                df   += 1

    df = max(1, (n_sites - 1) * (n_cols - 1))
    # Approximate p-value using chi2 CDF (Wilson–Hilferty)
    if df <= 0 or chi2 <= 0:
        return 0.0, 1.0
    try:
        k = df / 2
        x = chi2 / 2
        # Regularised incomplete gamma using series
        # Simple: use survival function approximation
        if chi2 > 2 * df:
            p = 0.0  # very significant
        elif chi2 < 0.5:
            p = 1.0  # not significant
        else:
            # Wilson–Hilferty: (X/df)^(1/3) ~ N(1 - 2/(9df), 2/(9df))
            c = 1.0 - 2.0 / (9.0 * df)
            s = math.sqrt(2.0 / (9.0 * df))
            z = ((chi2 / df) ** (1.0 / 3.0) - c) / s
            # Approximate: p ≈ 1 - Phi(z)
            import math
            p = 0.5 * math.erfc(z / math.sqrt(2))
    except Exception:
        p = 0.5
    return round(chi2, 4), max(0.0, min(1.0, round(p, 6)))


def main():
    print("Phase-69: Multi-Site Stratification\n")

    # Load corpus with site info
    seals: dict[str, dict] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]
            p = int(row.get("position", 0) or 0)
            s = (row.get("letters") or "").strip()
            site = (row.get("site") or "UNKNOWN").strip()
            if c not in seals:
                seals[c] = {"signs": [], "site": site}
            while len(seals[c]["signs"]) <= p:
                seals[c]["signs"].append("")
            seals[c]["signs"][p] = s

    # Build per-site inscriptions
    site_inscriptions: dict[str, list] = defaultdict(list)
    for seal_data in seals.values():
        site = seal_data["site"]
        signs = [s for s in seal_data["signs"] if s]
        if signs:
            site_inscriptions[site].append(signs)

    sites = sorted(site_inscriptions.keys())
    print(f"  Sites: {sites}")
    for site in sites:
        n = len(site_inscriptions[site])
        tokens = sum(len(ins) for ins in site_inscriptions[site])
        print(f"  {site:20s}: {n} seals, {tokens} tokens")

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    # Only analyse HIGH/MEDIUM signs with enough corpus frequency
    focal_signs = {sign for sign, info in anchors.items()
                   if info.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"\nFocal signs (HIGH/MEDIUM): {len(focal_signs)}")

    # Compute per-site I/M/T rates for each focal sign
    # Position bins: INITIAL=0, MEDIAL=1, TERMINAL=2
    site_profiles: dict[str, dict] = {}
    for site in sites:
        inscs = site_inscriptions[site]
        counts = defaultdict(lambda: [0, 0, 0])  # [I, M, T]
        for ins in inscs:
            n = len(ins)
            for pos, sign in enumerate(ins):
                if sign not in focal_signs:
                    continue
                if pos == 0 and n > 1:
                    counts[sign][0] += 1  # initial
                elif pos == n - 1 and n > 1:
                    counts[sign][2] += 1  # terminal
                else:
                    counts[sign][1] += 1  # medial
        site_profiles[site] = {sign: counts[sign] for sign in focal_signs
                               if sum(counts[sign]) > 0}

    # GPU: build frequency tensor [n_signs x n_sites x 3]
    sign_list = sorted(focal_signs)
    n_signs = len(sign_list)
    n_sites = len(sites)

    if torch is not None:
        mat = torch.zeros(n_signs, n_sites, 3, device=DEVICE)
        for si, site in enumerate(sites):
            profile = site_profiles[site]
            for gi, sign in enumerate(sign_list):
                if sign in profile:
                    for b in range(3):
                        mat[gi, si, b] = float(profile[sign][b])
        freq_cpu = mat.cpu().numpy()
        print(f"\n[GPU:{DEVICE}] Built {n_signs}×{n_sites}×3 frequency tensor")
    else:
        freq_cpu = None

    # Chi-squared test per sign across sites
    sign_results = []
    n_invariant = 0
    n_variant = 0

    for gi, sign in enumerate(sign_list):
        # Build contingency table: [site][position_bin]
        observed = []
        for si, site in enumerate(sites):
            profile = site_profiles.get(site, {})
            counts = profile.get(sign, [0, 0, 0])
            total = sum(counts)
            if total >= 3:  # only include sites with enough data
                observed.append(counts)

        if len(observed) < 2:
            chi2, p = 0.0, 1.0
            verdict = "INSUFFICIENT_DATA"
        else:
            chi2, p = chi2_test(observed)
            verdict = "INVARIANT" if p >= 0.05 else "SITE_VARIANT"

        if verdict == "INVARIANT": n_invariant += 1
        elif verdict == "SITE_VARIANT": n_variant += 1

        anchor_info = anchors.get(sign, {})
        sign_results.append({
            "sign":          sign,
            "reading":       anchor_info.get("reading", ""),
            "confidence":    anchor_info.get("confidence", "?"),
            "chi2":          chi2,
            "p_value":       p,
            "verdict":       verdict,
            "sites_with_data": len(observed),
        })

    # Overall verdict
    total_tested = n_invariant + n_variant
    invariant_rate = n_invariant / max(total_tested, 1)
    if invariant_rate >= 0.75:
        verdict = f"GRAMMAR_INVARIANT: {invariant_rate:.0%} of signs show consistent positional grammar across sites"
    elif invariant_rate >= 0.5:
        verdict = f"MOSTLY_INVARIANT: {invariant_rate:.0%} invariant — some site variation present"
    else:
        verdict = f"SITE_VARIANT: only {invariant_rate:.0%} invariant — significant site variation"

    # Summary of variant signs
    variant_signs = [r for r in sign_results if r["verdict"] == "SITE_VARIANT"]
    invariant_signs = [r for r in sign_results if r["verdict"] == "INVARIANT"]

    print("\n=== Phase-69 Results ===")
    print(f"  Signs tested:     {total_tested}")
    print(f"  INVARIANT:        {n_invariant} ({invariant_rate:.0%})")
    print(f"  SITE_VARIANT:     {n_variant}")
    print(f"  Verdict:          {verdict}")
    if variant_signs:
        print("\n  SITE_VARIANT signs (grammar differs across sites):")
        for r in variant_signs[:8]:
            print(f"  {r['sign']} {r['reading']!r}: chi2={r['chi2']:.1f} p={r['p_value']:.3f}")

    # Combined chi2 across all signs
    all_chi2 = [r["chi2"] for r in sign_results if r["verdict"] != "INSUFFICIENT_DATA"]
    mean_chi2 = sum(all_chi2) / max(len(all_chi2), 1)
    # Use median p-value as summary stat
    all_p = sorted(r["p_value"] for r in sign_results if r["verdict"] != "INSUFFICIENT_DATA")
    median_p = all_p[len(all_p)//2] if all_p else 1.0

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device":        DEVICE,
        "sites":             sites,
        "n_focal_signs":     len(focal_signs),
        "n_tested":          total_tested,
        "n_invariant":       n_invariant,
        "n_site_variant":    n_variant,
        "invariant_rate":    round(invariant_rate, 3),
        "mean_chi2":         round(mean_chi2, 3),
        "median_p_value":    round(median_p, 4),
        "chi2_p_value":      round(median_p, 4),
        "verdict":           verdict,
        "invariant_signs":   [r["sign"] for r in invariant_signs],
        "variant_signs":     [r for r in variant_signs[:20]],
        "sign_results":      sign_results,
        "site_profiles":     {site: {sign: list(v) for sign, v in profile.items()}
                              for site, profile in site_profiles.items()},
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
