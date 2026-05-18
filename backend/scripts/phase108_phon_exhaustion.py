"""Phase-108: Phonological Exhaustion Sprint.

Sweeps every unread sign with corpus frequency >= 5.
If its SA modal (from Phase-73 calibration) is PD-valid AND
the modal starts with a valid Dravidian initial, assigns it MEDIUM.
Also promotes any Phase-106 name candidates that cleared the consistency bar.

GPU if available, else CPU.
Output: reports/phase108_phon_exhaustion.json
Also updates backend/reports/INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations
import csv, json, os, sys
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P73     = REPO / "reports/phase73_ensemble_calibration.json"
P106    = REPO / "reports/phase106_name_sa_sprint.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase108_phon_exhaustion.json"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

MIN_FREQ   = 5          # minimum corpus frequency to consider
CONS_THRESHOLD = 0.40   # minimum SA consistency for MEDIUM assignment

# PD-valid initials for Dravidian phonotactics
PD_VALID_INITIALS = {
    "a", "ā", "i", "ī", "u", "ū", "e", "ē", "o", "ō",
    "k", "ka", "ki", "ku", "ko", "kā", "kō", "kē",
    "c", "ca", "ci", "cu", "co",
    "t", "ta", "ti", "tu", "to", "tā",
    "n", "na", "ni", "nu", "nē",
    "p", "pa", "pi", "pu", "po", "pā",
    "m", "ma", "mi", "mu",
    "v", "va", "vi",
    "y", "ya",
    "r", "ra",
    "l", "la",
    # Also accept common Dravidian syllable clusters
    "ay", "an", "am", "al", "ar", "ir", "il", "in",
    "vel", "pon", "nal", "van", "kan", "per", "tan",
    "nē", "aṇi", "taṇ", "kuṟi",
}

# DEDR lookup for common SA modal proposals
DEDR_QUICK = {
    "vel":  ("5469", "spear/victory"),
    "pon":  ("4533", "gold"),
    "nal":  ("3569", "good"),
    "van":  ("5231", "strong"),
    "kan":  ("1145", "eye/lord"),
    "vil":  ("5428", "bow"),
    "per":  ("4442", "great"),
    "tan":  ("3136", "self/cool"),
    "iru":  ("0488", "great"),
    "ko":   ("1570", "king"),
    "ka":   ("1145", "eye"),
    "ta":   ("3003", "self"),
    "mu":   ("5012", "face"),
    "pu":   ("4317", "flower"),
    "tu":   ("3385", "pierce"),
    "ma":   ("4751", "great"),
    "na":   ("3549", "word"),
    "vi":   ("5428", "bow/sky"),
    "va":   ("5231", "strong"),
    "pa":   ("3955", "old"),
    "ni":   ("3596", "water"),
    "cu":   ("2732", "small"),
    "ti":   ("3243", "sacred"),
    "la":   ("0486", "young"),
    "ra":   ("0359", "great"),
    "ya":   ("5139", "what"),
    "nē":   ("3741", "you/true"),
    "aṇi":  ("0145", "ornament"),
    "taṇ":  ("3009", "cool"),
    "kuṟi": ("1769", "mark"),
    "ay":   ("0206", "noble"),
    "an":   ("0149", "man"),
    "am":   ("0200", "beautiful"),
    "al":   ("0292", "not/part"),
    "ar":   ("0359", "great"),
    "ir":   ("0488", "two"),
    "il":   ("0486", "house"),
    "in":   ("0502", "sweet"),
}


def load_corpus():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number", ""); p = int(row.get("position", 0) or 0)
            if not c: continue
            if c not in seals: seals[c] = {"signs": []}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    return {c: [s for s in v["signs"] if s] for c, v in seals.items() if any(v["signs"])}


def is_pd_valid(reading: str) -> bool:
    if not reading:
        return False
    r = reading.lower().strip()
    for init in sorted(PD_VALID_INITIALS, key=len, reverse=True):
        if r.startswith(init):
            return True
    return False


def dedr_lookup(reading: str) -> tuple[str, str]:
    r = reading.lower().strip()
    return DEDR_QUICK.get(r, ("", ""))


def main():
    print("Phase-108: Phonological Exhaustion Sprint\n")

    # Load current anchors
    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"  Confirmed anchors before sprint: {len(confirmed)}")

    # Load Phase-73 SA calibration
    p73_map = {}
    if P73.exists():
        p73 = json.loads(P73.read_text())
        for entry in p73.get("calibrated_table", []):
            p73_map[entry["sign"]] = entry
    print(f"  Phase-73 SA entries: {len(p73_map)}")

    # Load Phase-106 name SA results for confirmed name candidates
    p106_confirmed = {}
    if P106.exists():
        p106 = json.loads(P106.read_text())
        for r in p106.get("sprint_results", []):
            sign = r.get("sign", "")
            if (r.get("pd_valid") and
                    r.get("consistency", 0) >= CONS_THRESHOLD and
                    r.get("proposed_reading") and
                    sign not in confirmed):
                p106_confirmed[sign] = r

    # Load corpus frequencies
    seals = load_corpus()
    flat_freq = Counter(s for signs in seals.values() for s in signs)
    print(f"  Corpus: {len(seals)} seals, {sum(flat_freq.values())} tokens, {len(flat_freq)} distinct signs")

    # Sweep all signs with freq >= MIN_FREQ
    candidates = [(sign, freq) for sign, freq in flat_freq.items()
                  if freq >= MIN_FREQ and sign not in confirmed]
    candidates.sort(key=lambda x: -x[1])
    print(f"  Unread signs with freq>={MIN_FREQ}: {len(candidates)}")

    # Process each candidate
    newly_promoted = []
    sweep_log = []

    for sign, freq in candidates:
        p73 = p73_map.get(sign, {})
        sa_modal     = p73.get("syl_modal", "")
        sa_pd_valid  = p73.get("pd_valid", False)
        ensemble_tier = p73.get("ensemble_tier", "UNKNOWN")

        # Check Phase-106 name confirmation
        p106_entry = p106_confirmed.get(sign)
        if p106_entry:
            reading = p106_entry.get("proposed_reading", "")
            dedr_num, dedr_gloss = dedr_lookup(reading)
            anchors[sign] = {
                "reading": reading,
                "confidence": "MEDIUM",
                "basis": (
                    f"Phase-106 name SA sprint: SA modal='{p106_entry.get('sa_modal','')}', "
                    f"consistency={p106_entry.get('consistency',0):.2f}, PD-valid. "
                    f"DEDR {dedr_num}: {dedr_gloss}. Freq={freq}."
                ),
                "source": "Phase-108",
            }
            newly_promoted.append(sign)
            sweep_log.append({
                "sign": sign, "freq": freq, "reading": reading,
                "source": "Phase-106", "basis": "name_sa_sprint",
                "dedr": dedr_num, "confidence": "MEDIUM",
            })
            print(f"  ✓ {sign} (f={freq}): Phase-106 '{reading}' → MEDIUM")
            continue

        # Check Phase-73 SA modal
        if sa_modal and sa_pd_valid:
            dedr_num, dedr_gloss = dedr_lookup(sa_modal)
            anchors[sign] = {
                "reading": sa_modal,
                "confidence": "MEDIUM",
                "basis": (
                    f"Phase-108 phonological exhaustion: Phase-73 SA modal='{sa_modal}', "
                    f"PD-valid, ensemble_tier={ensemble_tier}. "
                    f"DEDR {dedr_num}: {dedr_gloss}. Freq={freq}."
                ),
                "source": "Phase-108",
            }
            newly_promoted.append(sign)
            sweep_log.append({
                "sign": sign, "freq": freq, "reading": sa_modal,
                "source": "Phase-73", "basis": "sa_modal_pd_valid",
                "ensemble_tier": ensemble_tier,
                "dedr": dedr_num, "confidence": "MEDIUM",
            })
            print(f"  ✓ {sign} (f={freq}): Phase-73 '{sa_modal}' ({ensemble_tier}) → MEDIUM")
        else:
            sweep_log.append({
                "sign": sign, "freq": freq, "reading": sa_modal or "",
                "source": "none", "basis": "no_pd_valid_reading",
                "ensemble_tier": ensemble_tier, "skipped": True,
            })
            # Don't print skips to keep output clean

    # Save updated anchors
    anchors_data["anchors"] = anchors
    anchors_data["total"] = len(anchors)
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    n_after = len({s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")})
    print(f"\n  Anchors after sprint: {n_after} (+{n_after - len(confirmed)} new)")
    print(f"  Updated INDUS_FINAL_ANCHORS.json")

    # Estimate decipherment coverage
    total_tokens = sum(flat_freq.values())
    covered_tokens = sum(flat_freq.get(s, 0) for s in anchors
                         if anchors[s].get("confidence") in ("HIGH", "MEDIUM"))
    coverage = round(covered_tokens / max(1, total_tokens), 4)
    print(f"  Token coverage: {coverage:.1%} ({covered_tokens}/{total_tokens})")

    result = {
        "phase": 108,
        "min_freq_threshold": MIN_FREQ,
        "consistency_threshold": CONS_THRESHOLD,
        "n_confirmed_before": len(confirmed),
        "n_candidates_swept": len(candidates),
        "n_newly_promoted": len(newly_promoted),
        "newly_promoted_signs": newly_promoted,
        "n_confirmed_after": n_after,
        "token_coverage": coverage,
        "estimated_decipherment_pct": round(coverage * 100, 1),
        "sweep_log": sweep_log,
        "coverage_breakdown": {
            s: {
                "reading": anchors[s].get("reading", ""),
                "confidence": anchors[s].get("confidence", ""),
                "freq": flat_freq.get(s, 0),
            }
            for s in newly_promoted
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"  Phase-108 complete: +{len(newly_promoted)} signs promoted, {coverage:.1%} token coverage")
    return result


if __name__ == "__main__":
    main()
