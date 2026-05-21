"""Phase-114: Full Seal Translation Corpus.

Applies confirmed readings to all 1,670 seals. Produces:
  - Sign sequence → phonetic reading → English gloss
  - Confidence score per seal (fraction of signs decoded)
  - Site-stratified translation table
  - Summary statistics

CPU only. Output: reports/phase114_full_seal_translations.json
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
OUT     = REPORTS / "phase114_full_seal_translations.json"

# English gloss for common readings
READING_GLOSS = {
    "ay/ā": "belonging/of", "an/aṇ": "(masculine man)", "am/neuter": "(neuter)",
    "iṉ/locative": "at/in", "ōṭu/comitative": "with/together",
    "kol/koḷ": "merchant/trader", "kōṉ": "king", "ūr": "town/settlement",
    "il/iḷ": "house/home", "ka/kaṇ": "eye/lord",
    "erutu": "bull/ox", "yānai": "elephant", "puli": "tiger",
    "kāṇṭāmirukam": "rhinoceros", "nakaram": "crocodile/gharial",
    "pū/puḷ": "flower/blossom", "mu/muṉ": "front/face",
    "tu/tū": "pure/noble", "nal": "good/excellent",
    "oṉṟu/1": "one", "ēḷ/eḷ": "seven",
    "ā/āl": "great/lord", "kai": "hand",
    "nēr": "straight/true", "kō": "king",
    "māṭu": "cattle", "āṉai": "elephant",
    "vēṅkai": "tiger (poetic)", "māṭu": "cattle",
    "nē": "you/true", "aṇi": "ornament",
    "taṇ": "cool", "kuṟi": "mark/sign",
    "mā": "great", "māṟ": "change/great",
    "tōḷ": "shoulder/arm", "kēḷ": "hear/noble",
    "pēr": "name/great", "tiru": "sacred",
    "mutalai": "crocodile", "kōṭṭāṉ": "horned one",
    "maṟi": "young animal",
}


def load_corpus_with_site():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number", "")
            p = int(row.get("position", 0) or 0)
            site = (row.get("site") or row.get("location") or "").strip()
            if not c: continue
            if c not in seals:
                seals[c] = {"signs": [], "site": site}
            while len(seals[c]["signs"]) <= p:
                seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    return {c: {"signs": [s for s in v["signs"] if s], "site": v["site"]}
            for c, v in seals.items() if any(v["signs"])}


def translate_seal(signs: list, anchors: dict) -> dict:
    """Translate a single seal inscription."""
    readings = []
    glosses  = []
    decoded  = 0

    for sign in signs:
        anchor = anchors.get(sign, {})
        reading = anchor.get("reading", "")
        conf    = anchor.get("confidence", "")

        if reading and conf in ("HIGH", "MEDIUM"):
            gloss = READING_GLOSS.get(reading, reading)
            readings.append(reading)
            glosses.append(gloss)
            decoded += 1
        elif reading and conf == "LOW":
            readings.append(f"[{reading}?]")
            glosses.append(f"[{READING_GLOSS.get(reading, reading)}?]")
            decoded += 0.5
        else:
            readings.append(f"({sign})")
            glosses.append("?")

    n = len(signs)
    confidence = round(decoded / max(1, n), 3)
    return {
        "signs": signs,
        "readings": readings,
        "translation": " ".join(glosses),
        "phonetic": " ".join(readings),
        "n_signs": n,
        "n_decoded": int(decoded),
        "confidence": confidence,
        "fully_decoded": confidence >= 0.99,
    }


def main():
    print("Phase-114: Full Seal Translation Corpus\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"  Confirmed anchors: {len(confirmed)}")

    seals = load_corpus_with_site()
    print(f"  Seals to translate: {len(seals)}")

    translations = {}
    site_stats: dict[str, dict] = defaultdict(lambda: {"total": 0, "fully": 0, "tokens": 0, "decoded_tokens": 0})
    confidence_dist = Counter()

    for cisi_id, seal_data in seals.items():
        signs = seal_data["signs"]
        site  = seal_data["site"] or "Unknown"
        tx = translate_seal(signs, anchors)
        translations[cisi_id] = {**tx, "site": site}
        # Stats
        conf_bucket = int(tx["confidence"] * 10) * 10  # 0, 10, 20, ..., 100
        confidence_dist[conf_bucket] += 1
        site_stats[site]["total"] += 1
        site_stats[site]["tokens"] += tx["n_signs"]
        site_stats[site]["decoded_tokens"] += tx["n_decoded"]
        if tx["fully_decoded"]:
            site_stats[site]["fully"] += 1

    # Summary stats
    n_fully   = sum(1 for t in translations.values() if t["fully_decoded"])
    n_partial = sum(1 for t in translations.values() if 0 < t["confidence"] < 1.0)
    n_zero    = sum(1 for t in translations.values() if t["confidence"] == 0)
    mean_conf = sum(t["confidence"] for t in translations.values()) / max(1, len(translations))

    print(f"\n  Translation summary ({len(seals)} seals):")
    print(f"    Fully decoded (100%): {n_fully}")
    print(f"    Partially decoded:    {n_partial}")
    print(f"    No decoding:          {n_zero}")
    print(f"    Mean seal confidence: {mean_conf:.1%}")

    # Top 20 fully decoded seals (sample)
    sample_full = [
        {"cisi_id": cid, **{k: v for k, v in t.items() if k != "signs"}}
        for cid, t in translations.items()
        if t["fully_decoded"]
    ][:20]

    # Site-level table
    site_table = [
        {
            "site": site,
            "total": stats["total"],
            "fully_decoded": stats["fully"],
            "pct_fully": round(stats["fully"] / max(1, stats["total"]), 3),
            "token_coverage": round(stats["decoded_tokens"] / max(1, stats["tokens"]), 3),
        }
        for site, stats in sorted(site_stats.items(), key=lambda x: -x[1]["total"])
    ]

    result = {
        "phase": 114,
        "n_seals": len(seals),
        "n_fully_decoded": n_fully,
        "n_partially_decoded": n_partial,
        "n_zero_decoded": n_zero,
        "mean_seal_confidence": round(mean_conf, 4),
        "confidence_distribution": {str(k): v for k, v in sorted(confidence_dist.items())},
        "site_table": site_table,
        "sample_full_translations": sample_full,
        "all_translations": translations,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"  Phase-114 complete: {n_fully} fully decoded, {mean_conf:.1%} mean seal confidence")
    return result


if __name__ == "__main__":
    main()
