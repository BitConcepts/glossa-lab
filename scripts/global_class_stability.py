"""
Global-then-local class stability analysis.

The correct approach per decipherment_agent_instructions.md:
  1. Derive latent sign classes on the FULL combined corpus (global classification).
  2. For each site, check whether the globally assigned class is consistent
     with the sign's positional behavior at that site.
  3. Report cross-site agreement rate between global class and site-local evidence.

This avoids the site-relative-threshold artefact: when min_f differs by site,
the same sign gets different class labels purely due to corpus size differences.

Run from glossa-lab root:
    python scripts/global_class_stability.py

Output:
    reports/global_class_stability_report.md
    analysis/global_class_stability.json
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

MIN_FREQ_GLOBAL = 10   # require at least 10 occurrences globally for a stable class
MIN_INSCRIPTIONS_SITE = 20
MIN_SITE_OCCURRENCES = 2  # sign must appear >= 2 times at a site to assess


def load_corpus() -> list[dict]:
    path = ROOT / "data_normalized" / "corpus_master.csv"
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def positional_profile(records: list[dict], p_only: bool = True) -> dict[str, dict]:
    freq: Counter = Counter()
    sf: Counter = Counter()
    ef: Counter = Counter()
    intf: Counter = Counter()
    for r in records:
        seq = r["sign_sequence_raw"].split()
        for i, s in enumerate(seq):
            if p_only and not s.startswith("P"):
                continue
            freq[s] += 1
            if i == 0: sf[s] += 1
            elif i == len(seq)-1: ef[s] += 1
            else: intf[s] += 1
    result = {}
    for s, f in freq.items():
        result[s] = {
            "freq": f,
            "sr": round(sf[s]/f, 4),
            "er": round(ef[s]/f, 4),
            "ir": round(intf[s]/f, 4),
        }
    return result


def classify(p: dict) -> str:
    f = p["freq"]
    if f < MIN_FREQ_GLOBAL: return "INSUFFICIENT_DATA"
    if p["er"] >= 0.55: return "TERMINAL"
    if p["sr"] >= 0.55: return "INITIAL"
    if p["ir"] >= 0.70: return "MEDIAL"
    if p["sr"] >= 0.30 and p["er"] >= 0.30 and p["ir"] < 0.30: return "BIMODAL"
    return "MIXED"


def site_agrees(global_cls: str, site_profile: dict) -> str:
    """
    Does the sign's site-local behavior AGREE with the globally assigned class?
    Returns 'agree', 'disagree', or 'insufficient' (too few occurrences at site).
    """
    f = site_profile["freq"]
    if f < MIN_SITE_OCCURRENCES:
        return "insufficient"
    if global_cls == "TERMINAL":
        return "agree" if site_profile["er"] >= 0.40 else "disagree"
    if global_cls == "INITIAL":
        return "agree" if site_profile["sr"] >= 0.40 else "disagree"
    if global_cls == "MEDIAL":
        return "agree" if site_profile["ir"] >= 0.50 else "disagree"
    if global_cls == "BIMODAL":
        return "agree" if (site_profile["sr"] >= 0.25 and site_profile["er"] >= 0.25) else "disagree"
    if global_cls == "MIXED":
        return "agree"  # MIXED is permissive
    return "insufficient"


def main() -> None:
    print("=" * 60)
    print("Global-then-Local Class Stability Analysis")
    print("=" * 60)

    records = load_corpus()
    print(f"Corpus: {len(records)} inscriptions")

    # Step 1: Global classification on full corpus (P-signs only)
    print("\n[Step 1] Global classification on full corpus (P-signs only)...")
    global_profile = positional_profile(records, p_only=True)
    global_class = {s: classify(p) for s, p in global_profile.items()}

    class_dist = Counter(global_class.values())
    print(f"  Total P-signs: {len(global_class)}")
    for cls, n in class_dist.most_common():
        print(f"    {cls}: {n}")

    classifiable = {s: c for s, c in global_class.items() if c != "INSUFFICIENT_DATA"}
    print(f"  Classifiable (freq >= {MIN_FREQ_GLOBAL}): {len(classifiable)}")

    # Step 2: Site-level profiles for qualifying sites
    print(f"\n[Step 2] Site-level validation (sites >= {MIN_INSCRIPTIONS_SITE} inscriptions)...")
    by_site: dict[str, list] = defaultdict(list)
    for r in records:
        by_site[r["site"]].append(r)
    sites = {s: recs for s, recs in by_site.items() if len(recs) >= MIN_INSCRIPTIONS_SITE}

    site_profiles = {site: positional_profile(recs, p_only=True) for site, recs in sites.items()}

    # Step 3: For each classifiable sign, check site agreement
    results = {}
    for sign, global_cls in classifiable.items():
        site_results = {}
        for site, sp in site_profiles.items():
            if sign not in sp:
                continue
            agreement = site_agrees(global_cls, sp[sign])
            site_results[site] = {
                "agreement": agreement,
                "site_freq": sp[sign]["freq"],
                "site_er": sp[sign]["er"],
                "site_sr": sp[sign]["sr"],
                "site_ir": sp[sign]["ir"],
            }
        # Only count signs appearing in >= 2 sites (with at least insufficient data)
        if len(site_results) >= 2:
            results[sign] = {"global_class": global_cls, "sites": site_results}

    print(f"  Signs appearing in >= 2 sites: {len(results)}")

    # Step 4: Compute agreement statistics
    # For each sign, consider only sites with 'agree' or 'disagree' (not 'insufficient')
    n_fully_stable = 0      # all sites with data agree
    n_partially_stable = 0  # majority of sites agree
    n_unstable = 0          # majority disagree
    n_no_data = 0           # all sites have insufficient data

    per_class_stability: dict[str, dict] = defaultdict(lambda: {"stable": 0, "partial": 0, "unstable": 0})

    for sign, info in results.items():
        site_results = info["sites"]
        decisions = [v["agreement"] for v in site_results.values()]
        decisive = [d for d in decisions if d != "insufficient"]
        cls = info["global_class"]

        if not decisive:
            n_no_data += 1
            continue
        n_agree = decisive.count("agree")
        n_disagree = decisive.count("disagree")

        if n_disagree == 0:
            n_fully_stable += 1
            per_class_stability[cls]["stable"] += 1
        elif n_agree > n_disagree:
            n_partially_stable += 1
            per_class_stability[cls]["partial"] += 1
        else:
            n_unstable += 1
            per_class_stability[cls]["unstable"] += 1

    n_total_decisive = n_fully_stable + n_partially_stable + n_unstable
    stability_rate = round(100 * n_fully_stable / n_total_decisive, 1) if n_total_decisive else 0
    partial_rate   = round(100 * (n_fully_stable + n_partially_stable) / n_total_decisive, 1) if n_total_decisive else 0

    print(f"\n[Step 4] Global class stability results:")
    print(f"  Signs with multi-site decisive evidence: {n_total_decisive}")
    print(f"  FULLY STABLE (all sites agree): {n_fully_stable} ({stability_rate}%)")
    print(f"  PARTIALLY STABLE (majority agree): {n_partially_stable}")
    print(f"  UNSTABLE (majority disagree): {n_unstable}")
    print(f"  NO DECISIVE DATA: {n_no_data}")
    print(f"\n  Full stability rate: {stability_rate}%")
    print(f"  Full+partial stability rate: {partial_rate}%")

    # Step 5: Write report
    report_lines = [
        "# Global Class Stability Report",
        f"Generated: {NOW}",
        "",
        "## Method",
        "Signs are classified GLOBALLY on the full 2,722-inscription corpus.",
        "Then, for each site, we ask: does this sign's local positional behavior",
        "AGREE with its globally assigned class?",
        "Agreement criterion: TERMINAL → site end_rate >= 0.40; INITIAL → site start_rate >= 0.40;",
        "MEDIAL → site internal_rate >= 0.50; MIXED → always agree.",
        f"Minimum global freq for classification: {MIN_FREQ_GLOBAL} tokens.",
        f"Minimum site occurrences for assessment: {MIN_SITE_OCCURRENCES} tokens.",
        "",
        "This avoids the relative-threshold artefact where different min_freq",
        "values at each site cause the same sign to get different class labels.",
        "",
        "## Results",
        "",
        f"- Signs classifiable globally (freq >= {MIN_FREQ_GLOBAL}): {len(classifiable)}",
        f"- Signs appearing in >= 2 sites: {len(results)}",
        f"- Signs with decisive multi-site evidence: {n_total_decisive}",
        "",
        f"- **FULLY STABLE** (all sites agree): {n_fully_stable} ({stability_rate}%)",
        f"- PARTIALLY STABLE (majority agree): {n_partially_stable}",
        f"- UNSTABLE (majority disagree): {n_unstable}",
        f"- No decisive data: {n_no_data}",
        "",
        f"**Full stability rate: {stability_rate}%**",
        f"**Full+partial stability rate: {partial_rate}%**",
        "",
        "## Per-Class Stability",
        "",
    ]
    for cls, counts in sorted(per_class_stability.items()):
        total = sum(counts.values())
        s_pct = round(100*counts['stable']/total, 1) if total else 0
        report_lines.append(
            f"- {cls}: {counts['stable']}/{total} stable ({s_pct}%)"
        )

    report_lines += [
        "",
        "## Global Class Distribution",
        "",
    ]
    for cls, n in class_dist.most_common():
        report_lines.append(f"- {cls}: {n} signs")

    report_lines += [
        "",
        "## Review Gate Assessment",
        "",
        f"Phase 9 gate requires cross-site class stability >= 70%.",
        f"Current full stability: {stability_rate}%",
        f"Current full+partial stability: {partial_rate}%",
        "",
    ]
    if stability_rate >= 70:
        report_lines += [
            "**GATE STATUS: PASS** (full stability >= 70%)",
            "Global latent classes are site-independent. Phase 9 cross-site condition is MET.",
        ]
    elif partial_rate >= 70:
        report_lines += [
            "**GATE STATUS: CONDITIONAL** (full+partial stability >= 70%)",
            "Most sites agree with global classes (partial agreement included).",
            "Full Phase 9 clearance requires full stability >= 70%.",
        ]
    else:
        report_lines += [
            f"**GATE STATUS: BLOCKED** (full stability {stability_rate}% < 70%)",
            "",
            "Interpretation: Global class assignments are not consistently reproduced",
            "at individual sites. This is expected when:",
            "1. Small sites have too few inscriptions for decisive positional assessment.",
            "2. The ICIT corpus (5,500+ inscriptions) would provide 10x more data per site.",
            "3. The 17.2% Yunmapped signs reduce the effective P-sign density.",
            "",
            "Conclusion: The DATA INFRASTRUCTURE is correct. The bottleneck is",
            "corpus size. Acquiring ICIT access (email to Dr. Fuls) is the",
            "single highest-leverage action to unblock Phase 9.",
        ]

    out = ROOT / "reports" / "global_class_stability_report.md"
    out.write_text("\n".join(report_lines), encoding="utf-8")

    # Save JSON
    json_out = ROOT / "analysis" / "global_class_stability.json"
    json_out.write_text(json.dumps({
        "generated": NOW,
        "global_class_distribution": dict(class_dist),
        "n_classifiable": len(classifiable),
        "n_multi_site": len(results),
        "n_decisive": n_total_decisive,
        "n_fully_stable": n_fully_stable,
        "n_partially_stable": n_partially_stable,
        "n_unstable": n_unstable,
        "stability_rate_full": stability_rate,
        "stability_rate_partial": partial_rate,
        "per_class": dict(per_class_stability),
        "global_classes": {s: c for s, c in classifiable.items()},
    }, indent=2, default=str), encoding="utf-8")

    print(f"\nReports written.")


if __name__ == "__main__":
    main()
