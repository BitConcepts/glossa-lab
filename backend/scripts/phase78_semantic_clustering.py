"""Phase-78: Semantic Corpus Clustering by Formula Type.

Using the Phase-68 morphological role database, classifies all 1,670 Holdat
seals by formula type (TITLE_FORMULA, PLACE_FORMULA, UNCERTAIN) and tests
whether formula type distribution varies by site.

If sites show different distributions -> possible semantic specialisation
  (e.g. Dholavira seals are more administrative/place-marker)
If sites are uniform -> single writing system, single function corpus

GPU: torch for formula classification matrix and site comparison.
Output: reports/phase78_semantic_clustering.json
"""
from __future__ import annotations
import csv, json, math, sys
from collections import Counter, defaultdict
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
P68     = REPO / "reports/phase68_formula_translation.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase78_semantic_clustering.json"

# Morphological roles from Phase-68 database (abbreviated)
SUFFIX_ROLES  = {"SUFFIX", "CASE"}
INITIAL_ROLES = {"CLASSIFIER", "INITIAL"}
TITLE_ROLES   = {"TITLE", "ROOT"}
PARTICLE_ROLES= {"PARTICLE", "GENITIVE"}

# Signs by role (from Phase-68 MORPH_ROLES)
SUFFIX_SIGNS  = {"M342", "M176", "M367", "M391", "M336", "M089", "M328", "M162"}
TITLE_SIGNS   = {"M099", "M211", "M073", "M030", "M041", "M059"}
CLASSIFIER_SIGNS = {"M006", "M016", "M045", "M062", "M047", "M039"}
PLACE_SIGNS   = {"M233", "M013", "M162", "M336"}  # uur, nakaram, il, in


def classify_inscription(signs: list) -> str:
    """Classify an inscription by its sign composition."""
    sign_set = set(signs)
    has_classifier = bool(sign_set & CLASSIFIER_SIGNS)
    has_title      = bool(sign_set & TITLE_SIGNS)
    has_suffix     = bool(sign_set & SUFFIX_SIGNS)
    has_place      = bool(sign_set & PLACE_SIGNS)

    if has_classifier and (has_title or has_suffix):
        return "TITLE_FORMULA"
    if has_place and has_suffix:
        return "PLACE_FORMULA"
    if has_title and has_suffix and not has_classifier:
        return "TITLE_FORMULA"
    if has_suffix and not has_title and not has_classifier:
        return "SUFFIX_ONLY"
    return "UNCERTAIN"


def chi2_site_test(site_dist: dict) -> tuple[float, float]:
    """Chi-squared test: are formula type distributions site-invariant?"""
    sites   = [s for s in site_dist if sum(site_dist[s].values()) >= 10]
    types   = sorted(set(t for site in sites for t in site_dist[site]))
    if len(sites) < 2 or len(types) < 2:
        return 0.0, 1.0

    mat = [[site_dist[s].get(t, 0) for t in types] for s in sites]
    row_totals = [sum(r) for r in mat]
    col_totals = [sum(mat[i][j] for i in range(len(sites))) for j in range(len(types))]
    grand = sum(row_totals)

    chi2 = 0.0
    for i in range(len(sites)):
        for j in range(len(types)):
            expected = row_totals[i] * col_totals[j] / grand
            if expected > 0:
                chi2 += (mat[i][j] - expected) ** 2 / expected

    df = (len(sites) - 1) * (len(types) - 1)
    if df <= 0: return chi2, 1.0
    # Wilson-Hilferty approximation
    c = 1.0 - 2.0 / (9.0 * df)
    s = math.sqrt(2.0 / (9.0 * df))
    z = ((chi2 / df) ** (1.0 / 3.0) - c) / s if df > 0 else 0
    p = max(0, min(1, 0.5 * math.erfc(z / math.sqrt(2))))
    return round(chi2, 4), round(p, 6)


def main():
    print("Phase-78: Semantic Corpus Clustering by Formula Type\n")

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]

    # Load corpus with site info
    seals: dict[str, dict] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]; p = int(row.get("position", 0) or 0)
            s = (row.get("letters") or "").strip()
            site = (row.get("site") or "UNKNOWN").strip()
            if c not in seals: seals[c] = {"signs": [], "site": site}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = s

    print(f"  Corpus: {len(seals)} seals")

    # Classify all seals
    corpus_type_dist: Counter = Counter()
    site_dist: dict[str, Counter] = defaultdict(Counter)
    classified_seals = []
    n_classified = 0

    for seal_id, seal_data in seals.items():
        signs = [s for s in seal_data["signs"] if s]
        if not signs: continue
        formula_type = classify_inscription(signs)
        corpus_type_dist[formula_type] += 1
        site_dist[seal_data["site"]][formula_type] += 1
        if formula_type != "UNCERTAIN": n_classified += 1
        classified_seals.append({
            "seal_id":      seal_id,
            "site":         seal_data["site"],
            "n_signs":      len(signs),
            "formula_type": formula_type,
        })

    print(f"\n  Classification results:")
    for ftype, count in corpus_type_dist.most_common():
        pct = count / len(seals) * 100
        print(f"    {ftype:20s}: {count:4d} ({pct:.1f}%)")

    # Site distribution
    print(f"\n  Site x Formula-type breakdown:")
    sites = sorted(site_dist.keys())
    types = ["TITLE_FORMULA", "PLACE_FORMULA", "SUFFIX_ONLY", "UNCERTAIN"]
    for site in sites:
        dist = site_dist[site]
        total = sum(dist.values())
        row = [f"{dist.get(t,0):3d}" for t in types]
        print(f"    {site:20s}: {' / '.join(row)} (total={total})")

    # GPU: build site x type matrix for chi-squared
    if torch is not None and DEVICE == "cuda":
        site_list = [s for s in sites if sum(site_dist[s].values()) >= 10]
        n_sites = len(site_list); n_types = len(types)
        mat = torch.zeros(n_sites, n_types, device=DEVICE)
        for si, site in enumerate(site_list):
            for ti, ftype in enumerate(types):
                mat[si, ti] = float(site_dist[site].get(ftype, 0))
        row_sums = mat.sum(dim=1, keepdim=True).clamp(min=1)
        normed   = mat / row_sums
        # Variance across sites per type
        var_per_type = normed.var(dim=0).cpu().tolist()
        print(f"\n[GPU:{DEVICE}] Variance per formula type across sites:")
        for ftype, var in zip(types, var_per_type):
            print(f"  {ftype:20s}: var={var:.4f}")
        site_variation_found = max(var_per_type) > 0.01
    else:
        var_per_type = [0.0] * len(types)
        site_variation_found = False

    # Chi-squared test
    chi2, p_value = chi2_site_test(dict(site_dist))
    print(f"\n  Chi-squared test: chi2={chi2:.2f}, p={p_value:.4f}")

    if p_value >= 0.05:
        verdict = f"FORMULA_DISTRIBUTION_INVARIANT: No significant site variation (p={p_value:.4f}). Consistent with unified writing system."
        site_variation_found = False
    else:
        verdict = f"FORMULA_DISTRIBUTION_VARIES: Significant site variation (p={p_value:.4f}). Possible semantic specialisation."
        site_variation_found = True

    print(f"  Verdict: {verdict}")

    # Headline numbers
    total = sum(corpus_type_dist.values())
    title_pct = corpus_type_dist.get("TITLE_FORMULA", 0) / total * 100
    place_pct = corpus_type_dist.get("PLACE_FORMULA", 0) / total * 100
    uncertain_pct = corpus_type_dist.get("UNCERTAIN", 0) / total * 100

    print(f"\n=== Phase-78 Results ===")
    print(f"  Seals classified:   {n_classified}/{total} ({n_classified/total:.0%})")
    print(f"  TITLE_FORMULA:      {title_pct:.1f}%")
    print(f"  PLACE_FORMULA:      {place_pct:.1f}%")
    print(f"  UNCERTAIN:          {uncertain_pct:.1f}%")
    print(f"  Site variation:     {site_variation_found}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "n_seals_total":       total,
        "n_classified":        n_classified,
        "corpus_type_dist":    dict(corpus_type_dist),
        "site_type_dist":      {site: dict(dist) for site, dist in site_dist.items()},
        "chi2_p_value":        p_value,
        "site_variation_found":site_variation_found,
        "verdict":             verdict,
        "title_formula_pct":   round(title_pct, 1),
        "place_formula_pct":   round(place_pct, 1),
        "uncertain_pct":       round(uncertain_pct, 1),
        "sample_seals":        classified_seals[:30],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
