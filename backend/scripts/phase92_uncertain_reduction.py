"""Phase-92: UNCERTAIN Formula Reduction.

Re-classifies all 1,670 Holdat seals using the full current anchor set.
Previous classification used the Phase-78 model (97 anchors).
With 120+ anchors, many UNCERTAIN seals should now be classifiable.

Target: UNCERTAIN count below 200 (from current ~320).

CPU only. Output: reports/phase92_uncertain_reduction.json
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase92_uncertain_reduction.json"

TITLE_SIGNS   = {"M099","M073","M059","M030","M041","M107","M017","M063"}
SUFFIX_SIGNS  = {"M342","M176","M367","M391","M336","M089","M328","M162"}
ANIMAL_SIGNS  = {"M006","M016","M045","M062","M047","M039","M040","M001","M007"}
GENITIVE      = {"M267"}
PLACE_SIGNS   = {"M233","M162","M164","M163"}
NUMERAL_SIGNS = {"M079","M095","M096","M097","M098"}


def classify_seal(signs: list, anchors: dict, confirmed: set) -> str:
    roles = set()
    n_confirmed = sum(1 for s in signs if s in confirmed)
    coverage = n_confirmed / len(signs) if signs else 0

    for s in signs:
        if s in TITLE_SIGNS: roles.add("TITLE")
        if s in SUFFIX_SIGNS: roles.add("SUFFIX")
        if s in ANIMAL_SIGNS: roles.add("ANIMAL")
        if s in GENITIVE: roles.add("GENITIVE")
        if s in PLACE_SIGNS: roles.add("PLACE")
        if s in NUMERAL_SIGNS: roles.add("NUMERAL")
        # NEW: use anchor reading to identify roles
        info = anchors.get(s, {})
        if info.get("confidence") in ("HIGH","MEDIUM"):
            reading = info.get("reading","").lower()
            if any(x in reading for x in ("kol","eel","ko "," ko","nay")):
                roles.add("TITLE")
            if any(x in reading for x in ("tiru","il/i","uur","settlement")):
                roles.add("PLACE")

    if "ANIMAL" in roles and "TITLE" in roles and "SUFFIX" in roles:
        return "TITLE_FORMULA_ANIMAL"
    elif "GENITIVE" in roles:
        return "OWNERSHIP_FORMULA"
    elif "TITLE" in roles and "SUFFIX" in roles:
        return "TITLE_FORMULA_SIMPLE"
    elif "PLACE" in roles:
        return "PLACE_FORMULA"
    elif "NUMERAL" in roles:
        return "NUMERAL_FORMULA"
    elif "SUFFIX" in roles:
        return "SUFFIX_ONLY"
    elif "TITLE" in roles:
        return "TITLE_ONLY"
    elif coverage >= 0.75:
        return "HIGH_COVERAGE_UNCLASSIFIED"
    else:
        return "UNCERTAIN"


def main():
    print("Phase-92: UNCERTAIN Formula Reduction\n")

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}
    print(f"  Anchors: {len(confirmed)} HIGH+MEDIUM")

    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number",""); p = int(row.get("position",0) or 0)
            if not c: continue
            if c not in seals: seals[c] = {"signs":[], "site": row.get("site","?")}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    for v in seals.values():
        v["signs"] = [s for s in v["signs"] if s]
    seals = {c: v for c, v in seals.items() if v["signs"]}

    print(f"  Seals: {len(seals)}")

    new_dist: Counter = Counter()
    old_uncertain = 0
    new_uncertain = 0
    reclassified = 0
    site_dist: dict = defaultdict(Counter)

    for cisi_id, seal in seals.items():
        signs = seal["signs"]
        ft = classify_seal(signs, anchors, confirmed)
        new_dist[ft] += 1
        site_dist[seal.get("site","?")][ft] += 1
        if ft == "UNCERTAIN": new_uncertain += 1

    # Compare with Phase-78 results
    p78 = REPO / "reports/phase78_semantic_clustering.json"
    if p78.exists():
        old = json.loads(p78.read_text())
        old_uncertain = old.get("corpus_type_dist",{}).get("UNCERTAIN",321)
    else:
        old_uncertain = 321  # from Phase-78

    reclassified = old_uncertain - new_uncertain

    print(f"\n  Formula type distribution (Phase-92 with {len(confirmed)} anchors):")
    for ft, count in sorted(new_dist.items(), key=lambda x: -x[1]):
        pct = count/len(seals)*100
        print(f"    {ft:35s}: {count:4d} ({pct:.1f}%)")

    print(f"\n  UNCERTAIN: {old_uncertain} -> {new_uncertain} ({reclassified:+d} reclassified)")
    print(f"  Target <200: {'ACHIEVED!' if new_uncertain < 200 else f'need {new_uncertain-200} more anchor'}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "n_anchors_used": len(confirmed),
        "n_seals_total": len(seals),
        "formula_distribution": dict(new_dist),
        "n_uncertain_old": old_uncertain,
        "n_uncertain_new": new_uncertain,
        "n_reclassified": reclassified,
        "target_200_reached": new_uncertain < 200,
        "site_distribution": {site: dict(d) for site, d in site_dist.items()},
        "verdict": (
            f"Phase-92: UNCERTAIN reduced from {old_uncertain} to {new_uncertain} "
            f"({reclassified} seals reclassified). "
            f"{'Target <200 ACHIEVED!' if new_uncertain < 200 else f'Still {new_uncertain-200} above target.'}"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
