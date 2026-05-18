"""Phase-100: Full Corpus Translation.

Translates all 1,670 Holdat seals using the complete anchor set.
Produces the definitive Indus reference translation dataset.

Each seal entry contains:
- CISI ID, site, object type
- Sign sequence
- Transliteration (with [M###] for unknown signs)
- Coverage percentage
- Translation confidence (HIGH/MEDIUM/LOW)
- Formula type
- DEDR citations for decoded slots

This is the complete reference dataset for all further work.
CPU only. Output: reports/phase100_full_corpus.json
"""
from __future__ import annotations
import csv, json
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase100_full_corpus.json"

# Formula classification sign sets (updated with all current anchors)
TITLE_SIGNS   = {"M099","M073","M059","M107","M017","M030","M041","M063"}
SUFFIX_SIGNS  = {"M342","M176","M367","M391","M336","M089","M328","M162"}
ANIMAL_SIGNS  = {"M006","M016","M045","M062","M047","M039","M040","M001","M007"}
GENITIVE      = {"M267"}
PLACE_SIGNS   = {"M233","M162","M164","M163"}
NUMERAL_SIGNS = {"M079","M095","M096","M097","M098"}


def classify(signs: list) -> str:
    roles = set()
    for s in signs:
        if s in TITLE_SIGNS:   roles.add("T")
        if s in SUFFIX_SIGNS:  roles.add("S")
        if s in ANIMAL_SIGNS:  roles.add("A")
        if s in GENITIVE:      roles.add("G")
        if s in PLACE_SIGNS:   roles.add("P")
        if s in NUMERAL_SIGNS: roles.add("N")
    if "A" in roles and "T" in roles and "S" in roles: return "TITLE_FORMULA_ANIMAL"
    if "G" in roles: return "OWNERSHIP_FORMULA"
    if "T" in roles and "S" in roles: return "TITLE_FORMULA_SIMPLE"
    if "P" in roles: return "PLACE_FORMULA"
    if "N" in roles: return "NUMERAL_FORMULA"
    if "S" in roles: return "SUFFIX_ONLY"
    if "T" in roles: return "TITLE_ONLY"
    return "UNCERTAIN"


def translate(signs: list, anchors: dict, confirmed: set) -> dict:
    parts = []
    dedr_refs = []
    n_dec = 0
    for s in signs:
        info = anchors.get(s, {})
        conf = info.get("confidence","UNREAD")
        reading = info.get("reading","")
        if conf in ("HIGH","MEDIUM") and reading:
            n_dec += 1
            clean = reading.split("/")[0].split("(")[0].strip()
            parts.append(clean)
            dedr = info.get("dedr_id","")
            if dedr: dedr_refs.append(dedr)
        else:
            parts.append(f"[{s}]")
    cov = n_dec / len(signs) * 100 if signs else 0
    conf_label = "HIGH" if cov >= 90 else ("MEDIUM" if cov >= 70 else "LOW")
    return {
        "transliteration": " ".join(parts),
        "coverage_pct": round(cov, 1),
        "translation_confidence": conf_label,
        "n_decoded": n_dec,
        "dedr_refs": list(set(dedr_refs))[:6],
    }


def main():
    print("Phase-100: Full Corpus Translation\n")

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}
    print(f"  Anchors: {len(confirmed)} HIGH+MEDIUM")

    seals: dict = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number",""); p = int(row.get("position",0) or 0)
            if not c: continue
            if c not in seals:
                seals[c] = {"signs":[], "site": row.get("site","?"),
                            "object_type": row.get("object_type","?")}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    for v in seals.values():
        v["signs"] = [s for s in v["signs"] if s]
    seals = {c: v for c, v in seals.items() if v["signs"]}
    print(f"  Seals: {len(seals)}")

    translations = []
    dist: Counter = Counter()
    cov_dist: Counter = Counter()

    for cisi_id, seal in seals.items():
        signs = seal["signs"]
        t = translate(signs, anchors, confirmed)
        ft = classify(signs)
        dist[ft] += 1
        cov_bucket = int(t["coverage_pct"] // 10) * 10
        cov_dist[cov_bucket] += 1

        translations.append({
            "cisi_id": cisi_id,
            "site": seal.get("site","?"),
            "object_type": seal.get("object_type","?"),
            "signs": signs,
            "n_signs": len(signs),
            "transliteration": t["transliteration"],
            "coverage_pct": t["coverage_pct"],
            "translation_confidence": t["translation_confidence"],
            "n_decoded": t["n_decoded"],
            "formula_type": ft,
            "dedr_refs": t["dedr_refs"],
        })

    # Sort by coverage (best first)
    translations.sort(key=lambda x: -x["coverage_pct"])

    # Statistics
    n_high = sum(1 for t in translations if t["translation_confidence"] == "HIGH")
    n_med  = sum(1 for t in translations if t["translation_confidence"] == "MEDIUM")
    n_low  = sum(1 for t in translations if t["translation_confidence"] == "LOW")
    mean_cov = sum(t["coverage_pct"] for t in translations) / len(translations)
    n_100 = sum(1 for t in translations if t["coverage_pct"] == 100.0)

    print(f"\n  Formula distribution:")
    for ft, count in sorted(dist.items(), key=lambda x: -x[1]):
        print(f"    {ft:35s}: {count:4d} ({count/len(seals)*100:.1f}%)")

    print(f"\n  Coverage distribution:")
    for bucket in sorted(cov_dist.keys(), reverse=True):
        print(f"    {bucket:3d}-{bucket+9}%: {cov_dist[bucket]:4d} seals")

    print(f"\n=== Phase-100 Results ===")
    print(f"  Total seals translated: {len(translations)}")
    print(f"  100% coverage:          {n_100}")
    print(f"  HIGH confidence:        {n_high}")
    print(f"  MEDIUM confidence:      {n_med}")
    print(f"  LOW confidence:         {n_low}")
    print(f"  Mean coverage:          {mean_cov:.1f}%")
    print(f"  UNCERTAIN formula:      {dist.get('UNCERTAIN',0)}")

    # Estimate final decipherment percentage
    sign_pct = len(confirmed) / 390 * 100
    token_pct = mean_cov
    formula_pct = (len(seals) - dist.get("UNCERTAIN",0)) / len(seals) * 100
    decipherment_est = (sign_pct * 0.3 + token_pct * 0.4 + formula_pct * 0.3)
    print(f"\n  DECIPHERMENT ESTIMATE: {decipherment_est:.1f}%")
    print(f"    Sign inventory: {sign_pct:.1f}% ({len(confirmed)}/390)")
    print(f"    Token coverage: {token_pct:.1f}%")
    print(f"    Formula coverage: {formula_pct:.1f}%")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "n_anchors": len(confirmed),
        "n_seals_total": len(translations),
        "n_100pct_coverage": n_100,
        "n_high_confidence": n_high,
        "n_medium_confidence": n_med,
        "n_low_confidence": n_low,
        "mean_coverage_pct": round(mean_cov, 1),
        "formula_distribution": dict(dist),
        "coverage_distribution": {str(k): v for k, v in cov_dist.items()},
        "decipherment_estimate": {
            "sign_inventory_pct": round(sign_pct, 1),
            "token_coverage_pct": round(token_pct, 1),
            "formula_coverage_pct": round(formula_pct, 1),
            "overall_pct": round(decipherment_est, 1),
        },
        "translations": translations,  # ALL 1,670 seals
        "verdict": (
            f"Phase-100: Complete corpus translation. All {len(translations)} seals translated. "
            f"{n_100} at 100% coverage, {n_high} HIGH confidence. "
            f"Mean coverage: {mean_cov:.1f}%. UNCERTAIN: {dist.get('UNCERTAIN',0)}. "
            f"OVERALL DECIPHERMENT ESTIMATE: {decipherment_est:.1f}%."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
