#!/usr/bin/env python3
"""Mass seal translator — apply 605-sign anchor table to all known inscriptions.

Reads:
  - Holdat/Mahadevan corpus (1,670 seals via indus_m77.py)
  - Yajnadevam corpus (5,679 inscriptions via yajnadevam_inscriptions.csv)
  - INDUS_FINAL_ANCHORS.json (605 sign readings)

Produces:
  - outputs/seal_translations.json (full translation corpus)
  - outputs/seal_translations.csv (flat CSV for spreadsheet use)
  - outputs/seal_translations_summary.json (cultural insights by site/domain)
  - outputs/pdr_vs_sanskrit.csv (side-by-side comparison)

Usage:
  python backend/scripts/translate_all_seals.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

ANCHORS_PATH = BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
YAJNADEVAM_PATH = BACKEND / "glossa_lab" / "data" / "yajnadevam_inscriptions.csv"
YAJ_CROSSWALK_PATH = ROOT / "data" / "crosswalks" / "yajnadevam_to_parpola_crosswalk.csv"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)


def load_anchors() -> dict[str, dict]:
    """Load the 605-sign anchor table."""
    data = json.loads(ANCHORS_PATH.read_text("utf-8"))
    return data["anchors"]


def load_holdat_inscriptions() -> list[dict]:
    """Load Holdat/Mahadevan corpus inscriptions."""
    try:
        from glossa_lab.data.indus_m77 import get_corpus_inscriptions
        inscriptions = get_corpus_inscriptions()
    except (ImportError, AttributeError):
        inscriptions = []

    results = []
    for i, seq in enumerate(inscriptions):
        entry = {
            "id": f"H-{i+1:04d}",
            "corpus": "holdat",
            "site": "",
            "signs": seq,
            "sign_count": len(seq),
        }
        results.append(entry)
    return results


def load_yajnadevam_crosswalk(anchors: dict) -> dict[str, str]:
    """Build Yajnadevam glyph ID -> Mahadevan M-number mapping.

    Two methods combined:
    1. Crosswalk: Yaj glyph -> Parpola P-number -> M-number (P=M for standard signs)
    2. Direct: Yaj glyph NNN -> M + NNN (works for ~500 signs where numbering matches)
    """
    import re as _re  # noqa: PLC0415
    yaj_to_m: dict[str, str] = {}

    # Method 1: via existing crosswalk CSV
    if YAJ_CROSSWALK_PATH.exists():
        with open(YAJ_CROSSWALK_PATH, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                gid = row.get("yajnadevam_glyph_id", "")
                p_id = row.get("best_parpola_match", "")
                if gid and p_id and p_id.startswith("P"):
                    m_key = "M" + p_id[1:]
                    if m_key in anchors:
                        yaj_to_m[gid] = m_key

    # Method 2: direct numeric match (Yaj NNN -> MNNN)
    # This works because Yajnadevam largely adopted Mahadevan numbering
    for g in range(1000):
        gid = f"{g:03d}"
        if gid not in yaj_to_m:
            m_key = f"M{gid}"
            if m_key in anchors:
                yaj_to_m[gid] = m_key
            # Also try without leading zeros: M12 vs M012
            m_key_short = f"M{g}"
            if m_key_short in anchors and gid not in yaj_to_m:
                yaj_to_m[gid] = m_key_short

    return yaj_to_m


def _parse_yaj_text(text: str) -> list[str]:
    """Parse Yajnadevam text format into individual 3-digit glyph IDs.

    Format: +NNN-NNN-NNN+ where each NNN is a glyph ID.
    [ = damaged/incomplete end, / = alternative reading.
    """
    import re as _re  # noqa: PLC0415
    cleaned = text.strip("+").strip("[")
    parts = _re.split(r"[-/]", cleaned)
    glyphs = []
    for p in parts:
        p = p.strip().strip("+").strip("[")
        if _re.match(r"^\d{3}$", p):
            glyphs.append(p)
    return glyphs


def load_yajnadevam_inscriptions(yaj_to_m: dict[str, str]) -> list[dict]:
    """Load Yajnadevam corpus inscriptions with metadata and M-number mapping."""
    results = []
    with open(YAJNADEVAM_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = (row.get("text") or "").strip()
            if not text:
                continue
            # Parse into 3-digit glyph IDs
            yaj_glyphs = _parse_yaj_text(text)
            if not yaj_glyphs:
                continue
            # Map to M-numbers where possible
            signs = [yaj_to_m.get(g, g) for g in yaj_glyphs]
            results.append({
                "id": row.get("id", ""),
                "cisi": row.get("cisi", ""),
                "corpus": "yajnadevam",
                "site": row.get("site", ""),
                "region": row.get("region", ""),
                "period": row.get("period", ""),
                "material": row.get("material", ""),
                "type": row.get("type", ""),
                "signs": signs,
                "sign_count": len(signs),
                "sanskrit": (row.get("sanskrit") or "").strip(),
                "translation_yaj": (row.get("translation") or "").strip(),
            })
    return results


def translate_inscription(signs: list[str], anchors: dict) -> dict:
    """Translate a single inscription using the anchor table."""
    readings = []
    unknown = []
    for sign in signs:
        # Try M-prefixed and bare forms
        anchor = anchors.get(sign) or anchors.get(f"M{sign}") or anchors.get(sign.lstrip("M"))
        if anchor and anchor.get("reading"):
            readings.append(anchor["reading"])
        else:
            readings.append(f"[{sign}]")
            unknown.append(sign)

    # Build a readable translation string
    pdr_reading = "-".join(readings)

    # Classify the grammar pattern
    pattern = classify_grammar(signs, anchors)

    return {
        "readings": readings,
        "pdr_reading": pdr_reading,
        "n_translated": len(signs) - len(unknown),
        "n_unknown": len(unknown),
        "coverage": round((len(signs) - len(unknown)) / max(1, len(signs)), 3),
        "grammar_pattern": pattern,
    }


def classify_grammar(signs: list[str], anchors: dict) -> str:
    """Classify the I-M-T grammar pattern of an inscription."""
    if len(signs) < 2:
        return "SOLO"

    positions = []
    for sign in signs:
        anchor = anchors.get(sign) or anchors.get(f"M{sign}") or anchors.get(sign.lstrip("M"))
        if not anchor:
            positions.append("?")
            continue
        basis = (anchor.get("basis", "") or "").lower()
        reading = anchor.get("reading", "")
        if any(kw in basis for kw in ["initial", "classifier", "exclusive to"]):
            positions.append("I")
        elif any(kw in basis for kw in ["terminal", "suffix", "case", "genitive", "locative", "comitative", "neuter"]):
            positions.append("T")
        elif "medial" in basis or "positional" in basis:
            positions.append("M")
        # Check by known terminal signs
        elif sign in ("M342", "342", "M176", "176", "M367", "367", "M336", "336", "M305", "305"):
            positions.append("T")
        elif sign in ("M267", "267"):
            positions.append("M")  # genitive particle is medial
        else:
            positions.append("M")

    pattern = "".join(positions)
    return pattern


def generate_cultural_summary(translations: list[dict]) -> dict:
    """Generate cultural insights from the translated corpus."""
    site_counts = Counter()
    site_readings = defaultdict(list)
    domain_counts = Counter()
    top_formulas = Counter()
    period_counts = Counter()
    material_counts = Counter()
    fully_translated = 0
    total = len(translations)

    for t in translations:
        site = t.get("site", "unknown") or "unknown"
        site_counts[site] += 1
        site_readings[site].append(t["pdr_reading"])

        if t["coverage"] == 1.0:
            fully_translated += 1

        top_formulas[t["pdr_reading"]] += 1

        period = t.get("period", "")
        if period:
            period_counts[period] += 1

        material = t.get("material", "")
        if material:
            material_counts[material] += 1

    # Top 50 most common formulas (actual seal readings)
    common_formulas = [
        {"reading": r, "count": c, "pct": round(c / total * 100, 1)}
        for r, c in top_formulas.most_common(50)
    ]

    # Sites ranked by inscription count
    sites_ranked = [
        {"site": s, "count": c, "pct": round(c / total * 100, 1)}
        for s, c in site_counts.most_common(30)
    ]

    return {
        "total_inscriptions": total,
        "fully_translated": fully_translated,
        "fully_translated_pct": round(fully_translated / max(1, total) * 100, 1),
        "unique_formulas": len(top_formulas),
        "top_50_formulas": common_formulas,
        "sites_ranked": sites_ranked,
        "n_sites": len(site_counts),
        "periods": dict(period_counts.most_common(20)),
        "materials": dict(material_counts.most_common(20)),
    }


def main():
    print("Loading 605-sign anchor table...")
    anchors = load_anchors()
    print(f"  {len(anchors)} signs loaded")

    print("Loading Holdat/Mahadevan corpus...")
    holdat = load_holdat_inscriptions()
    print(f"  {len(holdat)} inscriptions")

    print("Building Yajnadevam crosswalk...")
    yaj_to_m = load_yajnadevam_crosswalk(anchors)
    print(f"  {len(yaj_to_m)} glyph->M-number mappings")

    print("Loading Yajnadevam corpus...")
    yajnadevam = load_yajnadevam_inscriptions(yaj_to_m)
    print(f"  {len(yajnadevam)} inscriptions")

    all_inscriptions = holdat + yajnadevam
    print(f"\nTotal: {len(all_inscriptions)} inscriptions to translate")

    # Translate everything
    print("Translating...")
    translations = []
    pdr_vs_sanskrit = []

    for insc in all_inscriptions:
        result = translate_inscription(insc["signs"], anchors)
        entry = {**insc, **result}
        # Don't include raw sign list in JSON output (it's redundant with readings)
        entry["signs_str"] = " ".join(insc["signs"])
        translations.append(entry)

        # Side-by-side for Yajnadevam entries with Sanskrit
        if insc.get("sanskrit"):
            pdr_vs_sanskrit.append({
                "id": insc["id"],
                "site": insc.get("site", ""),
                "signs": entry["signs_str"],
                "pdr_reading": result["pdr_reading"],
                "sanskrit": insc["sanskrit"],
                "translation_yaj": insc.get("translation_yaj", ""),
                "coverage": result["coverage"],
            })

    # Stats
    total = len(translations)
    full_cov = sum(1 for t in translations if t["coverage"] == 1.0)
    mean_cov = sum(t["coverage"] for t in translations) / max(1, total)
    print(f"\nResults:")
    print(f"  Total translated: {total}")
    print(f"  Fully covered (100%): {full_cov} ({full_cov/total*100:.1f}%)")
    print(f"  Mean coverage: {mean_cov*100:.1f}%")
    print(f"  PDr vs Sanskrit comparisons: {len(pdr_vs_sanskrit)}")

    # Generate cultural summary
    print("\nGenerating cultural insights...")
    summary = generate_cultural_summary(translations)
    summary["mean_coverage_pct"] = round(mean_cov * 100, 1)

    # Sample translations
    print("\n--- Sample Translations ---")
    for t in translations[:10]:
        site = t.get("site", "?")
        print(f"  [{t['id']}] {site}: {t['signs_str']}")
        print(f"    → {t['pdr_reading']}")
        if t.get("sanskrit"):
            print(f"    Sanskrit: {t['sanskrit']}")
        print()

    # Top formulas
    print("--- Top 10 Most Common Seal Readings ---")
    for f in summary["top_50_formulas"][:10]:
        print(f"  {f['reading']}  ({f['count']} seals, {f['pct']}%)")

    # Save outputs
    print("\nSaving outputs...")

    # Full JSON
    out_json = OUTPUTS / "seal_translations.json"
    out_json.write_text(json.dumps({
        "total": total,
        "fully_covered": full_cov,
        "mean_coverage_pct": round(mean_cov * 100, 1),
        "translations": translations,
    }, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  {out_json} ({out_json.stat().st_size:,} bytes)")

    # CSV
    out_csv = OUTPUTS / "seal_translations.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "corpus", "site", "region", "period", "material", "type",
            "signs_str", "sign_count", "pdr_reading", "grammar_pattern",
            "n_translated", "n_unknown", "coverage",
            "sanskrit", "translation_yaj",
        ])
        writer.writeheader()
        for t in translations:
            writer.writerow({k: t.get(k, "") for k in writer.fieldnames})
    print(f"  {out_csv}")

    # Summary JSON
    out_summary = OUTPUTS / "seal_translations_summary.json"
    out_summary.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  {out_summary}")

    # PDr vs Sanskrit CSV
    if pdr_vs_sanskrit:
        out_compare = OUTPUTS / "pdr_vs_sanskrit.csv"
        with open(out_compare, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "id", "site", "signs", "pdr_reading", "sanskrit", "translation_yaj", "coverage",
            ])
            writer.writeheader()
            writer.writerows(pdr_vs_sanskrit)
        print(f"  {out_compare} ({len(pdr_vs_sanskrit)} comparisons)")

    print("\nDone.")


if __name__ == "__main__":
    main()
