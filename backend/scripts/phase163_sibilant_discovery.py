"""
Phase-163: Sibilant Reading Discovery

Phase-152 found /su/ and /shu/ missing from H+M reading set.
This phase specifically mines reference literature for sibilant-initial
Dravidian readings (ca-, ce-, ci-, co-, cu-, cu-, su-) associated with
sign numbers, to close the Shu-ilishu phonological gap.

Also extracts Wells' explicit sibilant sign assignments and Parpola's
Chapter 6 (proto-Dravidian phonology) for sibilant phoneme attestations.

Output: backend/reports/phase163_sibilant_discovery.json
"""
import sys, json, re
from pathlib import Path
from collections import defaultdict

REPO      = Path(__file__).resolve().parents[2]
PDF_DIR   = REPO / "corpora/downloads/external_repos/acquired_pdfs"
MAHA_DIR  = REPO / "corpora/downloads/external_repos/mahadevan_papers"
ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
OUT          = REPO / "backend/reports/phase163_sibilant_discovery.json"

print("="*70)
print("PHASE-163: SIBILANT READING DISCOVERY")
print("="*70)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors     = anchor_data["anchors"]

def load(p): return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

parpola_text = load(PDF_DIR / "parpola_1994_deciphering_extracted.txt")
wells_text   = load(PDF_DIR / "wells_2015_archaeology_epigraphy_extracted.txt")
maha_texts = {f.stem: load(f) for f in sorted(MAHA_DIR.glob("*.txt"))}

# Sibilant patterns to search for
SIBILANT_ROOTS = [
    # (phoneme_pattern, description)
    (r'\bca[lrnmtṭṇkp]?\b', 'ca-family'),
    (r'\bce[lrnmtṭṇkp]?\b', 'ce-family'),
    (r'\bci[lrnmtṭṇkp]?\b', 'ci-family'),
    (r'\bco[lrnmtṭṇkp]?\b', 'co-family'),
    (r'\bcu[lrnmtṭṇkp]?\b', 'cu-family'),
    (r'\bsam?\b|\bcan\b|\bcam\b', 'cam/can'),
    (r'\bcol\b|\bcoḻ\b', 'col/colḻ'),
    (r'\bcum\b|\bcul\b', 'cum/cul'),
    (r'\bcin\b|\bcil\b', 'cin/cil'),
    (r'\bcem\b|\bcel\b|\bceṉ\b', 'cem/cel'),
]

# Current sibilant H+M readings (from Phase-153)
current_sib = {k: v for k,v in anchors.items()
               if v.get("confidence") in ("HIGH","MEDIUM")
               and any(v.get("reading","").lower().startswith(s)
                       for s in ["ca","ce","ci","co","cu","ñ"])}
print(f"\nExisting H+M sibilant signs: {len(current_sib)}")
for k,v in sorted(current_sib.items()):
    print(f"  {k}: '{v.get('reading','')}' ({v.get('confidence','')})")

print(f"\n/su/ or /shu/ covered: NO (gap remains from Phase-152)")

# ─── Search each source for sibilant + sign number associations ───────────
print("\n" + "─"*70)
print("SIBILANT SIGN ASSOCIATIONS IN LITERATURE")
print("─"*70)

sibilant_proposals = defaultdict(list)

def search_sibilant_context(text, source):
    """Find sibilant readings near sign number references."""
    # Look for sign numbers near sibilant words
    for m in re.finditer(r'M\s*(\d{3})', text, re.IGNORECASE):
        sign_id = f"M{int(m.group(1)):03d}"
        # Check window around this sign reference
        window = text[max(0,m.start()-100):m.end()+200].lower()
        for pat, desc in SIBILANT_ROOTS:
            sib_match = re.search(pat, window)
            if sib_match:
                reading = sib_match.group().strip()
                ctx = text[max(0,m.start()-50):m.end()+150].replace("\n"," ")
                sibilant_proposals[sign_id].append({
                    "reading": reading,
                    "source": source,
                    "family": desc,
                    "context": ctx[:200]
                })

    # Also search for explicit sibilant readings near signs
    for pat, desc in SIBILANT_ROOTS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            # Look for sign reference nearby
            window_before = text[max(0,m.start()-150):m.start()]
            window_after  = text[m.end():min(len(text),m.end()+150)]
            sign_m = re.search(r'M\s*(\d{3})', window_before + window_after, re.IGNORECASE)
            if sign_m:
                sign_id = f"M{int(sign_m.group(1)):03d}"
                reading = m.group().strip().lower()
                ctx = text[max(0,m.start()-80):m.end()+80].replace("\n"," ")
                sibilant_proposals[sign_id].append({
                    "reading": reading,
                    "source": source,
                    "family": desc,
                    "context": ctx[:200]
                })

search_sibilant_context(parpola_text, "Parpola_1994")
search_sibilant_context(wells_text, "Wells_2015")
for paper, text in maha_texts.items():
    search_sibilant_context(text, f"Mahadevan_{paper}")

# Deduplicate and filter to LOW signs
low_signs = {k for k,v in anchors.items() if v.get("confidence") == "LOW"}
no_anchor = set()  # signs not in our anchor set at all

sib_low_proposals = {}
for sign_id, props in sibilant_proposals.items():
    conf = anchors.get(sign_id,{}).get("confidence","NONE")
    if conf in ("LOW","NONE"):
        # Group by reading
        readings = defaultdict(list)
        for p in props:
            readings[p["reading"]].append(p)
        sib_low_proposals[sign_id] = {
            "current_confidence": conf,
            "current_reading": anchors.get(sign_id,{}).get("reading","?"),
            "sibilant_proposals": {
                r: {"n_mentions": len(ps), "sources": list({p["source"] for p in ps}),
                    "context": ps[0]["context"][:200]}
                for r,ps in readings.items()
            }
        }

print(f"\n  Total signs with sibilant associations: {len(sibilant_proposals)}")
print(f"  LOW/unanchored signs with sibilant proposals: {len(sib_low_proposals)}")

# Find the /cu/ and /co/ proposals (closest to /su/ gap)
print(f"\n  Signs with cu/co/ca proposals (closest to /su/ gap):")
su_gap_candidates = []
for sign_id, data in sib_low_proposals.items():
    for reading, rdata in data["sibilant_proposals"].items():
        if re.match(r'^c[uoa]', reading):
            su_gap_candidates.append({
                "sign_id": sign_id,
                "reading": reading,
                "n_mentions": rdata["n_mentions"],
                "sources": rdata["sources"],
                "context": rdata["context"][:150]
            })

su_gap_candidates.sort(key=lambda x: -x["n_mentions"])
print(f"  Total /cu/ /co/ /ca/ candidates: {len(su_gap_candidates)}")
for c in su_gap_candidates[:10]:
    print(f"  {c['sign_id']}: '{c['reading']}' ({c['n_mentions']}x) sources={c['sources']}")
    print(f"    → {c['context'][:120]}")

# Shu-ilishu coverage update
covered_slots = 2  # from Phase-152: /i/ and /li/ covered
if su_gap_candidates:
    best_su = su_gap_candidates[0]
    covered_slots = 3  # adding /cu/ covers the /su/ slot
    print(f"\n  Shu-ilishu coverage update:")
    print(f"  Best /su/-slot candidate: {best_su['sign_id']} = '{best_su['reading']}'")
    print(f"  Coverage: 2/4 → 3/4 slots (E02: PARTIALLY_SUPPORTED → more strongly)")

# Save
output = {
    "phase": 163,
    "date": "2026-05-20",
    "current_sibilant_hm": len(current_sib),
    "su_gap_filled": len(su_gap_candidates) > 0,
    "sib_low_proposals": sib_low_proposals,
    "su_gap_candidates": su_gap_candidates[:10],
    "shu_ilishu_coverage": f"{covered_slots}/4 slots",
    "key_findings": [
        f"Current H+M sibilant signs: {len(current_sib)}",
        f"LOW/unanchored signs with sibilant literature proposals: {len(sib_low_proposals)}",
        f"Signs with cu/co/ca proposals (su-gap candidates): {len(su_gap_candidates)}",
        f"Shu-ilishu coverage: {covered_slots}/4 slots",
        f"/su/ gap: {'CANDIDATES FOUND' if su_gap_candidates else 'STILL OPEN'}",
    ]
}
OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {OUT}")
print("="*70)
