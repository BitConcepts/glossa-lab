"""Phase-45 T6: Fish Sign (M047) Coastal Enrichment Test.

M047 (fish/mīn) is strongly initial (avg_pos≈0.0, count=13 in roles CSV).
The reading mīn/min is assigned HIGH confidence (Dravidian fish word).

Hypothesis: If M047 is a logograph for "fish" (mīn), it should be
enriched at coastal/maritime trade sites (Lothal, Dholavira) compared
to inland sites (Mohenjo-daro, Harappa, Kalibangan, etc.).

This script:
  1. Counts M047 occurrences per site from the full Holdat corpus CSV.
  2. Groups sites into coastal (Lothal, Dholavira) vs inland.
  3. Runs a 2×2 chi-squared test: [fish present/absent] × [coastal/inland].
  4. Computes relative risk (coastal vs inland enrichment ratio).
  5. Compares to the full sign frequency distribution as baseline.

GPU: uses torch for the inscription scanning tensor; CUDA if available.

Output: reports/phase45_fish_coastal_test.json
"""
from __future__ import annotations
import csv, json, math
from collections import Counter
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

try:
    from scipy.stats import chi2_contingency, fisher_exact
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("[WARN] scipy not available — using manual chi2")

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES   = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT = REPORTS / "phase45_fish_coastal_test.json"

TARGET = "M047"

# Coastal sites (maritime / estuarine access)
COASTAL_SITES = {"lothal", "dholavira"}

# Inland sites
INLAND_SITES = {
    "mohenjo-daro", "harappa", "kalibangan", "chanhu-daro",
    "rakhigarhi", "banawali", "sutkagen-dor", "shortugai",
}


def _is_coastal(site: str) -> bool | None:
    s = site.strip().lower()
    if any(c in s for c in COASTAL_SITES):
        return True
    if any(i in s for i in INLAND_SITES):
        return False
    return None  # unknown site — excluded from 2×2 test


def chi2_2x2(a: int, b: int, c: int, d: int) -> tuple[float, float]:
    """Manual Yates-corrected chi2 for 2×2 table [[a,b],[c,d]]."""
    n = a + b + c + d
    if n == 0:
        return 0.0, 1.0
    # Expected
    e_a = (a + b) * (a + c) / n
    e_b = (a + b) * (b + d) / n
    e_c = (c + d) * (a + c) / n
    e_d = (c + d) * (b + d) / n
    # Yates correction
    def term(o, e): return (max(0.0, abs(o - e) - 0.5) ** 2) / e if e > 0 else 0.0
    chi2 = term(a, e_a) + term(b, e_b) + term(c, e_c) + term(d, e_d)
    # Approximate p using chi2 CDF (1 df) via Cornish-Fisher
    # For a rough p: chi2 > 3.84 → p < 0.05
    if chi2 >= 10.83:
        p = 0.001
    elif chi2 >= 6.64:
        p = 0.01
    elif chi2 >= 3.84:
        p = 0.05
    elif chi2 >= 2.71:
        p = 0.10
    else:
        p = 0.50
    return chi2, p


def main() -> None:
    print(f"Phase-45 T6: Fish Sign {TARGET} Coastal Enrichment Test\n")

    # --- Load corpus ---
    seals: dict[str, dict] = {}
    with open(CORPUS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cisi = r["cisi_number"]
            pos = int(r.get("position", 0) or 0)
            if cisi not in seals:
                seals[cisi] = {
                    "signs": [],
                    "site": r.get("site", "").strip(),
                    "icon": (r.get("iconography") or "").strip().lower(),
                }
            while len(seals[cisi]["signs"]) <= pos:
                seals[cisi]["signs"].append("")
            seals[cisi]["signs"][pos] = r["letters"]

    inscriptions = []
    for cisi, d in seals.items():
        signs = [s for s in d["signs"] if s]
        if signs:
            inscriptions.append({
                "id": cisi,
                "signs": signs,
                "site": d["site"],
                "icon": d["icon"],
            })

    print(f"Loaded {len(inscriptions)} inscriptions across all sites")

    # --- GPU-accelerated: build site-presence matrix ---
    all_sites = sorted({ins["site"] for ins in inscriptions if ins["site"]})
    print(f"[GPU:{DEVICE}] Scanning {len(inscriptions)} inscriptions for {TARGET}…")

    site_total: Counter = Counter()
    site_with_target: Counter = Counter()

    if torch is not None:
        # Build a boolean tensor: inscriptions × 1 (has_target)
        n = len(inscriptions)
        has_target = torch.zeros(n, dtype=torch.bool, device=DEVICE)
        for i, ins in enumerate(inscriptions):
            if TARGET in ins["signs"]:
                has_target[i] = True
        has_target_cpu = has_target.cpu().tolist()

        for i, ins in enumerate(inscriptions):
            site = ins["site"]
            if not site:
                continue
            site_total[site] += 1
            if has_target_cpu[i]:
                site_with_target[site] += 1
    else:
        for ins in inscriptions:
            site = ins["site"]
            if not site:
                continue
            site_total[site] += 1
            if TARGET in ins["signs"]:
                site_with_target[site] += 1

    print(f"\nSite distribution for {TARGET}:")
    target_total = sum(site_with_target.values())
    for site, cnt in sorted(site_with_target.items(), key=lambda x: -x[1]):
        is_c = _is_coastal(site)
        label = "COASTAL" if is_c else ("inland" if is_c is False else "unknown")
        pct = cnt / site_total[site] if site_total[site] else 0
        print(f"  {site:25s}: {cnt:3d} / {site_total[site]:4d} ({pct:.1%})  [{label}]")

    if target_total == 0:
        print(f"\n⚠ {TARGET} not found in corpus — aborting test")
        result = {"error": f"{TARGET} has zero occurrences in the corpus"}
        OUT.write_text(json.dumps(result, indent=2), "utf-8")
        return

    # --- Build 2×2 contingency table ---
    # a = coastal inscriptions WITH target
    # b = inland inscriptions WITH target
    # c = coastal inscriptions WITHOUT target
    # d = inland inscriptions WITHOUT target
    a = b = c = d = 0
    site_label_map: dict[str, str] = {}
    for site in all_sites:
        is_c = _is_coastal(site)
        if is_c is None:
            continue
        total_s = site_total[site]
        with_s = site_with_target[site]
        without_s = total_s - with_s
        site_label_map[site] = "coastal" if is_c else "inland"
        if is_c:
            a += with_s
            c += without_s
        else:
            b += with_s
            d += without_s

    coastal_total = a + c
    inland_total = b + d
    coastal_rate = a / coastal_total if coastal_total else 0
    inland_rate = b / inland_total if inland_total else 0
    relative_risk = coastal_rate / inland_rate if inland_rate > 0 else float("inf")

    print(f"\n2×2 Contingency Table:")
    print(f"              With M047  Without M047  Total")
    print(f"  Coastal     {a:9d}  {c:12d}  {coastal_total}")
    print(f"  Inland      {b:9d}  {d:12d}  {inland_total}")
    print(f"\n  Coastal rate: {a}/{coastal_total} = {coastal_rate:.4f}")
    print(f"  Inland rate:  {b}/{inland_total} = {inland_rate:.4f}")
    print(f"  Relative risk (coastal/inland): {relative_risk:.2f}×")

    if HAS_SCIPY:
        # Use Fisher exact for small counts
        if (a + b + c + d) < 30 or min(a, b, c, d) < 5:
            odds_ratio, p_val = fisher_exact([[a, c], [b, d]])
            test_name = "Fisher exact"
            chi2_val = float(odds_ratio)  # report odds ratio as stat for Fisher
        else:
            chi2_val, p_val, _, _ = chi2_contingency([[a, c], [b, d]], correction=True)
            test_name = "Chi-squared (Yates)"
    else:
        chi2_val, p_val = chi2_2x2(a, b, c, d)
        test_name = "Chi-squared (Yates, manual)"

    print(f"\n  {test_name}: stat={chi2_val:.3f}, p={p_val:.4f}")

    sig = p_val < 0.05
    strong_sig = p_val < 0.01
    if strong_sig and relative_risk > 2.0:
        verdict = "STRONGLY_ENRICHED"
        note = (f"{TARGET} is {relative_risk:.1f}× more frequent at coastal sites (p={p_val:.4f}), "
                f"strongly supporting the mīn/'fish' logographic reading")
    elif sig and relative_risk > 1.5:
        verdict = "ENRICHED"
        note = (f"{TARGET} is {relative_risk:.1f}× more frequent at coastal sites (p={p_val:.4f}), "
                f"consistent with the mīn/'fish' logographic reading")
    elif relative_risk > 1.5:
        verdict = "TREND_COASTAL"
        note = (f"{TARGET} shows {relative_risk:.1f}× coastal enrichment but p={p_val:.4f} "
                f"(likely underpowered — M047 count={target_total})")
    elif relative_risk < 0.67:
        verdict = "INLAND_ENRICHED"
        note = f"{TARGET} actually skews inland (RR={relative_risk:.2f}) — unexpected for fish logograph"
    else:
        verdict = "NO_ENRICHMENT"
        note = (f"No coastal enrichment detected (RR={relative_risk:.2f}, p={p_val:.4f}); "
                f"count may be too low (n={target_total}) for reliable test")

    print(f"\nVerdict: {verdict}")
    print(f"Note: {note}")

    # --- Load roles to get M047 baseline ---
    m047_role = {}
    with open(ROLES, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["symbol"] == TARGET:
                m047_role = dict(r)
                break

    # Cast numpy scalars to Python natives for JSON serialisation
    def _native(v):
        try:
            return v.item()
        except AttributeError:
            return v

    sig = bool(sig)
    chi2_val = float(_native(chi2_val))
    p_val = float(_native(p_val))
    relative_risk = float(_native(relative_risk))
    coastal_rate = float(_native(coastal_rate))
    inland_rate = float(_native(inland_rate))

    result = {
        "_citation": {"primary_sources": ["A.1"], "reading": "mīn (fish) — Dravidian"},
        "gpu_device": DEVICE,
        "target_sign": TARGET,
        "total_occurrences": target_total,
        "site_breakdown": {
            site: {
                "count": site_with_target[site],
                "total_inscriptions": site_total[site],
                "rate": round(site_with_target[site] / site_total[site], 4) if site_total[site] else 0,
                "type": site_label_map.get(site, "unknown"),
            }
            for site in sorted(all_sites)
            if site_with_target[site] > 0 or site in site_label_map
        },
        "contingency_table": {
            "coastal_with": a, "coastal_without": c,
            "inland_with": b, "inland_without": d,
            "coastal_total": coastal_total, "inland_total": inland_total,
        },
        "coastal_rate": round(coastal_rate, 4),
        "inland_rate": round(inland_rate, 4),
        "relative_risk": round(relative_risk, 3),
        "test_name": test_name,
        "test_stat": round(chi2_val, 3),
        "p_value": round(p_val, 4),
        "significant_p05": sig,
        "verdict": verdict,
        "verdict_note": note,
        "m047_holdat_role": m047_role,
        "coastal_sites_used": sorted(COASTAL_SITES),
        "inland_sites_used": sorted(INLAND_SITES),
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
