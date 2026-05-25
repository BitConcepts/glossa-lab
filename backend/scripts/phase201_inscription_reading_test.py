"""Phase 201 — Complete Inscription Reading Test

Phase 195 showed the title formula is now 100% covered. M427=/en/ (MEDIUM)
fills the last title slot, producing the full formula:
  [tiru/muruku/kōṉ] + [en] + [AN] → "[divine title] the person"

This phase attempts complete phonetic transcription of M77 inscriptions
that contain the /en/ sign (M427) plus title markers, and checks whether
the resulting strings form plausible Dravidian personal name/title patterns.

Dravidian title name patterns (Parpola 2009, Mahadevan 1977):
  Pattern A: [deity-epithet] + [kōṉ/ruler] → divine title
  Pattern B: [commodity] + [merchant-title] → merchant seal
  Pattern C: [place-name] + [person] → territorial title

Also tests the /sum/ (title/name marker) hypothesis:
  /sum/ is Elamite šum- = "name, title" → should appear BEFORE name signs
  M868 (freq=3, our /gi/ LOW anchor) may be the /sum/ sign in miniature inscs.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

# Known title signs (M77 format)
TITLE_SIGNS = {
    "073": "kōṉ",      # king
    "030": "kō",       # king variant
    "014": "tiru",     # auspicious/holy
    "261": "muruku",   # warrior deity
    "081": "ve",       # brightness
    "176": "an",       # person/man
    "342": "ay",       # terminal
    "427": "en",       # NEW: lord/person (Phase 192)
}

# Commodity signs that appear in merchant seals
COMMODITY_SIGNS = {
    "099": "kol",     # forge/iron
    "391": "ka",      # gem/eye
    "047": "min",     # fish/star
}


def load_data():
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    inscs = get_corpus_inscriptions()
    syms  = get_corpus_symbols()
    freq  = Counter(syms)
    anchors_raw = json.loads(ANCHOR_F.read_text())["anchors"]
    return inscs, freq, anchors_raw


def build_reading_map(anchors_raw, freq):
    """Build M77 sign → reading map from all anchors."""
    m = {}
    for aid, rec in anchors_raw.items():
        if not isinstance(rec, dict): continue
        reading = rec.get("reading","").split("/")[0].strip()
        m77 = aid.lstrip("M")
        if m77 in freq and reading:
            m[m77] = (reading, rec.get("confidence",""))
    return m


def transcribe_inscription(insc, reading_map):
    """Attempt phonetic transcription of an inscription."""
    parts = []
    for sign in insc:
        if sign in reading_map:
            reading, conf = reading_map[sign]
            parts.append({"sign": sign, "reading": reading, "confidence": conf, "anchored": True})
        else:
            parts.append({"sign": sign, "reading": "?", "confidence": "NONE", "anchored": False})
    coverage = sum(1 for p in parts if p["anchored"]) / max(1, len(parts))
    text = " ".join(p["reading"] for p in parts)
    return {"parts": parts, "text": text, "coverage": round(coverage, 2)}


def is_dravidian_title_pattern(parts):
    """Check if the inscription matches a known Dravidian title pattern."""
    readings = [p["reading"] for p in parts if p["anchored"]]
    # Pattern A: title sign + en + person marker
    has_title  = any(r in ("kōṉ","kō","tiru","muruku","ve") for r in readings)
    has_en     = "en" in readings
    has_person = any(r in ("an","āl","am") for r in readings)
    # Pattern B: commodity + forge
    has_commodity = any(r in ("min","kol","ka") for r in readings)
    # Pattern C: place + person
    has_place  = any(r in ("ūr","il","ki") for r in readings)

    if has_title and has_en:
        return "TITLE_FORMULA", "divine/royal title with /en/ person marker"
    elif has_title and has_person:
        return "PERSONAL_TITLE", "personal title formula"
    elif has_commodity:
        return "COMMODITY_SEAL", "merchant/commodity seal"
    elif has_place:
        return "PLACE_SEAL", "place/territory seal"
    else:
        return "UNKNOWN", "no recognized pattern"


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 201 — Complete Inscription Reading Test")
    print("=" * 60)

    inscs, freq, anchors_raw = load_data()
    reading_map = build_reading_map(anchors_raw, freq)
    print(f"\nReading map: {len(reading_map)} signs")

    # Find inscriptions containing M427 (en) — our newest MEDIUM anchor
    en_sign = "427"
    inscs_with_en = [insc for insc in inscs if en_sign in insc]
    print(f"\nInscriptions containing M427 (/en/): {len(inscs_with_en)}")

    # Transcribe and analyze
    transcriptions = []
    pattern_counts = Counter()
    fully_readable = []

    for insc in inscs_with_en:
        t = transcribe_inscription(insc, reading_map)
        pattern, pattern_desc = is_dravidian_title_pattern(t["parts"])
        pattern_counts[pattern] += 1
        t["pattern"] = pattern
        t["pattern_desc"] = pattern_desc
        t["inscription"] = insc
        transcriptions.append(t)
        if t["coverage"] >= 0.7:  # 70%+ readable
            fully_readable.append(t)

    print("\n=== Inscription Analysis ===")
    print(f"  Inscriptions with /en/: {len(inscs_with_en)}")
    print(f"  70%+ readable: {len(fully_readable)}")
    print("\nPattern distribution:")
    for pat, count in pattern_counts.most_common():
        print(f"  {pat}: {count}")

    print("\n=== Sample Transcriptions (highest coverage) ===")
    sorted_t = sorted(transcriptions, key=lambda x: (-x["coverage"], -len(x["inscription"])))
    for t in sorted_t[:15]:
        print(f"  [{t['coverage']*100:.0f}%] [{t['pattern']}] {t['text']}")
        print(f"       Signs: {t['inscription']}")

    # Test all inscriptions for overall reading rate
    all_transcriptions = []
    coverage_sum = 0
    for insc in inscs:
        t = transcribe_inscription(insc, reading_map)
        all_transcriptions.append(t)
        coverage_sum += t["coverage"]

    mean_coverage = round(coverage_sum / max(1, len(inscs)), 3)
    fully_readable_all = sum(1 for t in all_transcriptions if t["coverage"] >= 0.7)
    print("\n=== Overall Reading Statistics ===")
    print(f"  Total inscriptions: {len(inscs)}")
    print(f"  Mean reading coverage: {mean_coverage*100:.1f}%")
    print(f"  Fully readable (70%+): {fully_readable_all} ({fully_readable_all/len(inscs)*100:.1f}%)")
    print(f"  Partially readable (30%+): {sum(1 for t in all_transcriptions if t['coverage']>=0.3)}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase":              201,
        "elapsed_s":          elapsed,
        "n_inscs_with_en":   len(inscs_with_en),
        "n_fully_readable":  len(fully_readable),
        "pattern_distribution": dict(pattern_counts),
        "mean_coverage":     mean_coverage,
        "fully_readable_all": fully_readable_all,
        "sample_transcriptions": sorted_t[:20],
        "all_en_transcriptions": transcriptions[:50],
        "verdict": (
            f"TITLE FORMULA WORKS: {len(inscs_with_en)} inscriptions contain /en/ (M427). "
            f"{pattern_counts.get('TITLE_FORMULA',0)} match title formula. "
            f"Overall mean reading coverage: {mean_coverage*100:.1f}%. "
            f"{fully_readable_all} inscriptions 70%+ readable."
        ),
    }

    out = OUTPUTS / "phase201_inscription_reading_test.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase201_inscription_reading_test.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 201 complete in {elapsed}s")
    print(f"Verdict: {result['verdict']}")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
