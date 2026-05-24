"""Phase-218: Site-Stratified Semantic Field Analysis (updated, 164 H+M anchors).

Re-runs the site semantic analysis with the current anchor set after Phase-216
upgraded 29 additional MEDIUM→HIGH anchors (total H+M now 164).

Output: outputs/phase218_site_semantic_updated.json
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
OUT     = REPO / "outputs/phase218_site_semantic_updated.json"
OUT.parent.mkdir(exist_ok=True)

SEMANTIC_FIELDS = {
    "ANIMAL_CLAN": {
        "erutu", "yānai", "puli", "kāṇṭāmirukam", "nakaram",
        "māṭu", "āṉai", "vēṅkai", "mutalai", "kōṭṭāṉ",
        "maṟi", "kaḷiṟu", "erumai",
    },
    "TITLE": {
        "kol/koḷ", "kōṉ", "kō", "nal", "nēr", "kai", "pēr",
        "ā/āl", "tiru", "kēḷ", "māṟ", "kol", "nall",
    },
    "CASE_SUFFIX": {
        "ay/ā", "an/aṇ", "am/neuter", "iṉ/locative",
        "ōṭu/comitative", "ka/kaṇ", "il/iḷ", "tu/tū",
        "iN/in (genitive of)",
    },
    "PLACE": {"ūr"},
    "NUMERAL": {"oṉṟu/1", "ēḷ/eḷ"},
    "PERSONAL_NAME": {
        "nē", "aṇi", "taṇ", "kuṟi", "mu/muṉ", "pū/puḷ",
        "mā", "tōḷ", "inci", "nal/nall",
    },
    "PHONETIC_SYLLABLE": {
        "ka", "ma", "na", "pa", "ta", "va", "mi", "mu",
        "kol", "ve", "vi", "ya", "ra", "la",
        "ni", "miN3", "miN4", "miṭ", "cul", "vī", "kul",
        "pul", "taṇ", "nē",
    },
}


def load_corpus_with_site():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row.get("cisi_number", "")
            p = int(row.get("position", 0) or 0)
            s = (row.get("letters") or "").strip()
            site = (row.get("site") or row.get("location") or "").strip()
            if not c: continue
            if c not in seals: seals[c] = {"signs": [], "site": site}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    return {c: {"signs": [s for s in v["signs"] if s], "site": v["site"]}
            for c, v in seals.items() if any(v["signs"])}


def classify_reading(reading: str) -> str:
    r = reading.strip()
    for field, readings in SEMANTIC_FIELDS.items():
        if r in readings:
            return field
    return "OTHER"


def main():
    print("Phase-218: Site-Stratified Semantic Field Analysis (164 H+M anchors)\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s: v["reading"] for s, v in anchors.items()
                 if v.get("confidence") in ("HIGH", "MEDIUM") and v.get("reading")}
    print(f"  Confirmed H+M anchors: {len(confirmed)}")

    seals_raw = load_corpus_with_site()
    print(f"  Holdat seals: {len(seals_raw)}")

    site_stats: dict = defaultdict(lambda: {
        "n_seals": 0, "field_counts": Counter(), "top_readings": Counter(),
        "fully_decoded": 0, "partially_decoded": 0,
    })

    for cisi_id, data in seals_raw.items():
        signs = data["signs"]
        site = data["site"] or "Unknown"
        n = len(signs)
        decoded = sum(1 for s in signs if s in confirmed)
        fully = decoded == n
        partial = 0 < decoded < n

        site_stats[site]["n_seals"] += 1
        if fully: site_stats[site]["fully_decoded"] += 1
        if partial: site_stats[site]["partially_decoded"] += 1

        for sign in signs:
            if sign in confirmed:
                reading = confirmed[sign]
                field = classify_reading(reading)
                site_stats[site]["field_counts"][field] += 1
                site_stats[site]["top_readings"][reading] += 1

    # Build site profiles
    site_profiles = []
    for site, stats in sorted(site_stats.items(), key=lambda x: -x[1]["n_seals"]):
        n = stats["n_seals"]
        fc = stats["field_counts"]
        total_tokens = sum(fc.values())
        profile = {
            "site": site,
            "n_seals": n,
            "n_fully_decoded": stats["fully_decoded"],
            "n_partially_decoded": stats["partially_decoded"],
            "pct_fully": round(stats["fully_decoded"] / max(1, n), 3),
            "pct_partially": round(stats["partially_decoded"] / max(1, n), 3),
            "total_decoded_tokens": total_tokens,
            "field_profile": {
                f: round(fc[f] / max(1, total_tokens), 4) for f in SEMANTIC_FIELDS
            },
            "top_10_readings": [
                {"reading": r, "count": c}
                for r, c in stats["top_readings"].most_common(10)
            ],
        }
        site_profiles.append(profile)
        print(f"\n  {site} ({n} seals, {stats['fully_decoded']} fully / "
              f"{stats['partially_decoded']} partial decoded):")
        for field, frac in profile["field_profile"].items():
            if frac > 0.01:
                print(f"    {field:22s}: {frac:.1%}")

    # Harappa vs Mohenjo-daro comparison
    h = next((p for p in site_profiles if "arappa" in p["site"]), None)
    m = next((p for p in site_profiles if "ohenjo" in p["site"]), None)
    comparison = {}
    if h and m:
        print("\n  Harappa vs Mohenjo-daro field comparison:")
        for field in SEMANTIC_FIELDS:
            h_rate = h["field_profile"].get(field, 0)
            m_rate = m["field_profile"].get(field, 0)
            comparison[field] = {
                "harappa": h_rate, "mohenjo_daro": m_rate,
                "diff": round(h_rate - m_rate, 4),
                "dominant": "Harappa" if h_rate > m_rate else "Mohenjo-daro",
            }
            if abs(h_rate - m_rate) > 0.005:
                print(f"    {field}: H={h_rate:.1%} M={m_rate:.1%}"
                      f" → {'Harappa' if h_rate > m_rate else 'Mohenjo-daro'}")

    # Overall decode stats
    total_seals = sum(p["n_seals"] for p in site_profiles)
    total_fully = sum(p["n_fully_decoded"] for p in site_profiles)
    print(f"\n  Overall: {total_fully}/{total_seals} seals fully decoded"
          f" ({total_fully/total_seals:.1%})")

    result = {
        "phase": 218,
        "n_hm_anchors": len(confirmed),
        "n_sites": len(site_profiles),
        "total_seals": total_seals,
        "total_fully_decoded": total_fully,
        "pct_fully_decoded_overall": round(total_fully / max(1, total_seals), 4),
        "site_profiles": site_profiles,
        "harappa_vs_mohenjo_comparison": comparison,
        "semantic_field_definitions": {k: list(v) for k, v in SEMANTIC_FIELDS.items()},
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
