"""
Phases 161 / 162 / 165  —  Literature Reading Extraction Battery

Systematically mines three reference sources for sign reading proposals,
then cross-checks against our LOW-confidence signs to identify upgrade candidates.

Sources:
  161 — Parpola 1994 (1.5 M chars of extracted text)
  162 — Mahadevan 1970-2018 (38 papers, ~1.2 M chars total)
  165 — Wells 2015 (264 K chars of extracted text)

For each LOW-confidence sign (240 total, 220 with placeholder "kur"):
  • Search for M-number pattern + Dravidian reading in each source
  • Score by number of sources that agree on a reading
  • Flag candidates for MEDIUM promotion if ≥ 2 sources agree
    or if 1 authoritative source gives a DEDR-referenced Dravidian reading

Output: backend/reports/phase161_162_165_reading_extraction.json
        backend/reports/phase161_162_165_upgrade_proposals.json
"""
import sys, json, re
from pathlib import Path
from collections import defaultdict, Counter

REPO      = Path(__file__).resolve().parents[2]
PDF_DIR   = REPO / "corpora/downloads/external_repos/acquired_pdfs"
MAHA_DIR  = REPO / "corpora/downloads/external_repos/mahadevan_papers"
ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
OUT_FULL  = REPO / "backend/reports/phase161_162_165_reading_extraction.json"
OUT_UPGRD = REPO / "backend/reports/phase161_162_165_upgrade_proposals.json"

print("="*70)
print("PHASES 161-162-165: LITERATURE READING EXTRACTION")
print("="*70)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors     = anchor_data["anchors"]
low_signs   = {k: v for k, v in anchors.items() if v.get("confidence") == "LOW"}
hm_signs    = {k for k, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}

print(f"\nLOW signs to upgrade: {len(low_signs)}")

def load(path): return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

# Load all sources
parpola_text = load(PDF_DIR / "parpola_1994_deciphering_extracted.txt")
wells_text   = load(PDF_DIR / "wells_2015_archaeology_epigraphy_extracted.txt")

maha_texts = {}
for f in sorted(MAHA_DIR.glob("*.txt")):
    maha_texts[f.stem] = load(f)
maha_all = "\n\n===PAPER===\n\n".join(maha_texts.values())

print(f"Parpola: {len(parpola_text):,} chars")
print(f"Mahadevan (38 papers): {len(maha_all):,} chars")
print(f"Wells: {len(wells_text):,} chars")

# ─── Dravidian phoneme set for validation ─────────────────────────────────
DRAVIDIAN_WORDS = set()
# Build from existing H+M readings as a "known good" set
for sign_id, data in anchors.items():
    if data.get("confidence") in ("HIGH","MEDIUM"):
        r = data.get("reading","").lower()
        for part in re.split(r'[/\s]+', r):
            part = part.strip()
            if len(part) >= 2:
                DRAVIDIAN_WORDS.add(part)

# Dravidian phonological patterns (readings that look Dravidian)
DRV_PATTERN = re.compile(
    r'\b([a-z\u0101\u012b\u016b\u0113\u014d\u1e37\u1e5f\u1e49\u1e3b\u1e47\u1e7f]{2,10})\b',
    re.UNICODE
)

def looks_dravidian(word: str) -> bool:
    """Check if a word looks like a Dravidian reading."""
    w = word.lower().strip()
    if len(w) < 2: return False
    # Already in our known set
    if w in DRAVIDIAN_WORDS: return True
    # Has Dravidian-exclusive characters
    drv_chars = "\u1e37\u1e5f\u1e49\u1e3b"
    if any(c in w for c in drv_chars): return True
    # Common Dravidian endings
    drv_endings = ("an","aṇ","al","āl","am","ai","il","iḷ","ar","um","oṭu","kku","ku")
    if any(w.endswith(e) for e in drv_endings): return True
    # Typical Dravidian syllable patterns (CV, CVC)
    if re.match(r'^[kmnptvcrsṭṇḷṟṉ][aāiīuūeē][lrntṭṇkmnp]?$', w): return True
    return False

# ─── Extraction functions ─────────────────────────────────────────────────
def extract_sign_readings(text: str, source_name: str) -> dict:
    """
    Extract (sign_id, reading) pairs from text.
    Looks for patterns like:
      "M342 = ay/ā"  "M 047 (fish)"  "sign M342 reads as"
      Also: Mnn followed within 50 chars by a Tamil word
    """
    proposals = defaultdict(list)

    # Pattern 1: M-number immediately followed by = or : or "reads"
    for m in re.finditer(
        r'\bM\s*(\d{3})\b.{0,60}?[=:]\s*([^\n,;\.]{2,25})',
        text, re.IGNORECASE
    ):
        sign_id = f"M{int(m.group(1)):03d}"
        reading = m.group(2).strip().split()[0] if m.group(2).strip() else ""
        if reading and looks_dravidian(reading):
            proposals[sign_id].append({
                "reading": reading, "source": source_name,
                "context": text[max(0,m.start()-30):m.end()+50].replace("\n"," ")
            })

    # Pattern 2: "sign NNN" near a Tamil reading
    for m in re.finditer(r'\bsign\s+(\d{3})\b(.{0,80})', text, re.IGNORECASE):
        sign_id = f"M{int(m.group(1)):03d}"
        nearby = m.group(2)
        words = DRV_PATTERN.findall(nearby.lower())
        for w in words:
            if looks_dravidian(w) and len(w) >= 2:
                proposals[sign_id].append({
                    "reading": w, "source": source_name,
                    "context": text[max(0,m.start()-20):m.end()].replace("\n"," ")[:150]
                })

    # Pattern 3: Explicit "M042 = mīn" style with Tamil characters
    for m in re.finditer(
        r'\bM\s*(\d{3})\b[^=]*?[=:]\s*([\u0100-\u024F\w]{2,20})',
        text, re.IGNORECASE
    ):
        sign_id = f"M{int(m.group(1)):03d}"
        reading = m.group(2).strip()
        if reading and len(reading) >= 2:
            proposals[sign_id].append({
                "reading": reading, "source": source_name,
                "context": text[max(0,m.start()-20):m.end()+30].replace("\n"," ")[:150]
            })

    return dict(proposals)

# ─── Phase 161: Parpola ─────────────────────────────────────────────────
print("\n" + "─"*70)
print("PHASE-161: PARPOLA 1994")
print("─"*70)

parpola_proposals = extract_sign_readings(parpola_text, "Parpola_1994")
print(f"  Signs with reading proposals: {len(parpola_proposals)}")
for sign_id, props in sorted(parpola_proposals.items())[:10]:
    conf = anchors.get(sign_id,{}).get("confidence","NONE")
    print(f"  {sign_id} ({conf}): {[p['reading'] for p in props[:3]]}")

# ─── Phase 162: Mahadevan ────────────────────────────────────────────────
print("\n" + "─"*70)
print("PHASE-162: MAHADEVAN (38 PAPERS)")
print("─"*70)

maha_proposals = extract_sign_readings(maha_all, "Mahadevan_1970-2018")
print(f"  Signs with reading proposals: {len(maha_proposals)}")
for sign_id, props in sorted(maha_proposals.items())[:10]:
    conf = anchors.get(sign_id,{}).get("confidence","NONE")
    print(f"  {sign_id} ({conf}): {[p['reading'] for p in props[:3]]}")

# ─── Phase 165: Wells 2015 ──────────────────────────────────────────────
print("\n" + "─"*70)
print("PHASE-165: WELLS 2015")
print("─"*70)

wells_proposals = extract_sign_readings(wells_text, "Wells_2015")
print(f"  Signs with reading proposals: {len(wells_proposals)}")
for sign_id, props in sorted(wells_proposals.items())[:10]:
    conf = anchors.get(sign_id,{}).get("confidence","NONE")
    print(f"  {sign_id} ({conf}): {[p['reading'] for p in props[:3]]}")

# ─── Multi-source consensus scoring ──────────────────────────────────────
print("\n" + "─"*70)
print("MULTI-SOURCE CONSENSUS SCORING")
print("─"*70)

# Merge all proposals
all_proposals = defaultdict(lambda: defaultdict(list))
for source, props in [("Parpola_1994", parpola_proposals),
                       ("Mahadevan", maha_proposals),
                       ("Wells_2015", wells_proposals)]:
    for sign_id, items in props.items():
        for item in items:
            reading = item["reading"].lower().strip()
            if len(reading) >= 2:
                all_proposals[sign_id][reading].append(item)

# Score: consensus = number of distinct sources proposing the same reading
upgrade_candidates = []
for sign_id, reading_groups in all_proposals.items():
    current_conf = anchors.get(sign_id, {}).get("confidence", "NONE")
    current_reading = anchors.get(sign_id, {}).get("reading", "")

    for reading, proposals in reading_groups.items():
        sources = list({p["source"] for p in proposals})
        n_sources = len(sources)

        # Skip if reading matches existing HIGH/MEDIUM (already captured)
        if current_conf in ("HIGH","MEDIUM") and reading == current_reading.lower():
            continue

        # Score promotability
        if current_conf == "LOW" or current_conf == "NONE":
            # More stringent: reading must be clearly Dravidian
            if looks_dravidian(reading):
                target_conf = "HIGH" if n_sources >= 3 else ("MEDIUM" if n_sources >= 2 else "LOW_CANDIDATE")
                if target_conf in ("HIGH","MEDIUM","LOW_CANDIDATE"):
                    upgrade_candidates.append({
                        "sign_id": sign_id,
                        "proposed_reading": reading,
                        "current_confidence": current_conf,
                        "current_reading": current_reading,
                        "target_confidence": target_conf,
                        "n_sources": n_sources,
                        "sources": sources,
                        "sample_context": proposals[0]["context"][:200] if proposals else "",
                        "promote": target_conf in ("HIGH","MEDIUM"),
                    })

upgrade_candidates.sort(key=lambda x: (-x["n_sources"], x["sign_id"]))

# Filter to genuine LOW signs
genuine_upgrades = [c for c in upgrade_candidates
                    if c["current_confidence"] == "LOW"
                    and c["promote"]]

print(f"\n  Total signs with literature proposals: {len(all_proposals)}")
print(f"  LOW signs with upgrade proposals: {len(genuine_upgrades)}")
print(f"\n  TOP UPGRADE CANDIDATES:")
print(f"  {'Sign':<8} {'Current':>8} {'Target':>8} {'N':>4} {'Reading':<15} {'Sources'}")
for c in genuine_upgrades[:20]:
    print(f"  {c['sign_id']:<8} {c['current_confidence']:>8} {c['target_confidence']:>8} "
          f"{c['n_sources']:>4} {c['proposed_reading']:<15} {c['sources']}")

# ─── Also: check NEW readings for LOW "kur" signs ────────────────────────
print(f"\n  Signs proposed for kur→specific upgrade:")
kur_upgrades = [c for c in upgrade_candidates
                if anchors.get(c["sign_id"],{}).get("reading","") == "kur"
                and c["promote"]]
print(f"  Count: {len(kur_upgrades)}")
for c in kur_upgrades[:10]:
    print(f"    {c['sign_id']}: kur → {c['proposed_reading']} ({c['n_sources']} sources: {c['sources']})")

# Summary
print(f"\n  SUMMARY:")
print(f"  Parpola proposals: {len(parpola_proposals)} signs")
print(f"  Mahadevan proposals: {len(maha_proposals)} signs")
print(f"  Wells proposals: {len(wells_proposals)} signs")
print(f"  LOW→MEDIUM upgrades identified: {len([c for c in genuine_upgrades if c['target_confidence']=='MEDIUM'])}")
print(f"  LOW→HIGH upgrades identified:   {len([c for c in genuine_upgrades if c['target_confidence']=='HIGH'])}")
print(f"  kur→specific upgrades:          {len(kur_upgrades)}")

# Save full extraction
output = {
    "phases": "161-162-165",
    "date": "2026-05-20",
    "parpola_proposals": {k: v[:5] for k,v in parpola_proposals.items()},
    "mahadevan_proposals": {k: v[:5] for k,v in maha_proposals.items()},
    "wells_proposals": {k: v[:5] for k,v in wells_proposals.items()},
    "n_parpola": len(parpola_proposals),
    "n_mahadevan": len(maha_proposals),
    "n_wells": len(wells_proposals),
    "n_genuine_upgrades": len(genuine_upgrades),
    "n_medium_upgrades": len([c for c in genuine_upgrades if c["target_confidence"]=="MEDIUM"]),
    "n_high_upgrades": len([c for c in genuine_upgrades if c["target_confidence"]=="HIGH"]),
    "n_kur_upgrades": len(kur_upgrades),
    "key_findings": [
        f"Parpola 1994 proposes readings for {len(parpola_proposals)} signs",
        f"Mahadevan papers propose readings for {len(maha_proposals)} signs",
        f"Wells 2015 proposes readings for {len(wells_proposals)} signs",
        f"LOW→MEDIUM upgrades: {len([c for c in genuine_upgrades if c['target_confidence']=='MEDIUM'])}",
        f"LOW→HIGH upgrades (3 sources): {len([c for c in genuine_upgrades if c['target_confidence']=='HIGH'])}",
        f"kur→specific upgrades: {len(kur_upgrades)}",
    ]
}
OUT_FULL.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

# Save upgrade proposals separately (for apply script)
upgrades_out = {
    "date": "2026-05-20",
    "source": "Phases 161-162-165 literature mining",
    "proposals": genuine_upgrades,
    "n_proposals": len(genuine_upgrades),
}
OUT_UPGRD.write_text(json.dumps(upgrades_out, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"\nReports saved:")
print(f"  {OUT_FULL}")
print(f"  {OUT_UPGRD}")
print("="*70)
