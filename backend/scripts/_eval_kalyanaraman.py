"""Cross-check Kalyanaraman rebus readings against INDUS_FINAL_ANCHORS.

Extracts sign readings from the 52 imported papers and compares them
against the SA-derived anchor readings to find:
  - MATCH: reading appears in both systems (independent corroboration)
  - RELATED: reading root overlaps (partial agreement)
  - NEW: reading not in anchors (potential new candidate)
  - CONFLICT: same sign, different reading (needs investigation)
"""
import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB = REPO / "backend" / "data" / "glossa.db"
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"

# Load anchors
fa = json.loads(ANCHORS.read_text(encoding="utf-8"))
anchors = fa.get("anchors", {})

# Build reading → sign mapping
reading_to_sign: dict[str, list[str]] = defaultdict(list)
for sid, info in anchors.items():
    reading = info.get("reading", "")
    if reading:
        for variant in reading.split("/"):
            v = variant.strip().lower()
            if v:
                reading_to_sign[v].append(sid)

print(f"Anchors: {len(anchors)} signs, {len(reading_to_sign)} unique readings")
print()

# Load imported papers
conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row
rows = conn.execute(
    "SELECT id, title, raw_json FROM discovery_items WHERE source='local_pdf' ORDER BY title"
).fetchall()

# Extract readings from papers
# Kalyanaraman uses "X rebus Y" pattern extensively
kalyan_readings: dict[str, str] = {}
kalyan_terms: Counter = Counter()

for r in rows:
    raw = r["raw_json"]
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = {}
    text = raw.get("text_preview", "")
    title = r["title"] or ""
    full = title + " " + text[:2000]

    # Extract rebus patterns
    for m in re.finditer(
        r'([a-zA-Z\u0100-\u1EFF]{2,20})\s+rebus\s+([a-zA-Z\u0100-\u1EFF]{2,20})',
        full, re.IGNORECASE
    ):
        pic, meaning = m.group(1).lower(), m.group(2).lower()
        if len(pic) >= 2 and len(meaning) >= 2:
            kalyan_readings[pic] = meaning
            kalyan_terms[pic] += 1
            kalyan_terms[meaning] += 1

    # Also extract Dravidian terms (kol, min, etc.)
    for m in re.finditer(
        r"'([a-zA-Z\u0100-\u1EFF]{2,15})'",
        full
    ):
        term = m.group(1).lower()
        if len(term) >= 2:
            kalyan_terms[term] += 1

conn.close()

print(f"Papers analyzed: {len(rows)}")
print(f"Rebus readings extracted: {len(kalyan_readings)}")
print(f"Unique terms found: {len(kalyan_terms)}")
print()

# Cross-check
print("=== CROSS-CHECK: Kalyanaraman vs Glossa Lab Anchors ===\n")

matches = []
related = []
new_candidates = []

for k_pic, k_meaning in sorted(kalyan_readings.items()):
    # Check if the pictogram reading matches an anchor
    if k_pic in reading_to_sign:
        signs = reading_to_sign[k_pic]
        matches.append((k_pic, k_meaning, signs))
    elif k_meaning in reading_to_sign:
        signs = reading_to_sign[k_meaning]
        related.append((k_pic, k_meaning, signs))
    else:
        # Check partial matches (root overlap)
        root = k_pic[:3] if len(k_pic) >= 3 else k_pic
        partial = [r for r in reading_to_sign if r.startswith(root)]
        if partial:
            related.append((k_pic, k_meaning, [reading_to_sign[p][0] for p in partial[:2]]))
        else:
            new_candidates.append((k_pic, k_meaning))

print(f"MATCHES (reading in both systems): {len(matches)}")
for pic, meaning, signs in matches:
    print(f"  ✓ '{pic}' → '{meaning}' (anchor signs: {', '.join(signs[:3])})")

print(f"\nRELATED (partial overlap): {len(related)}")
for pic, meaning, signs in related[:15]:
    print(f"  ~ '{pic}' / '{meaning}' (near: {', '.join(signs[:2])})")

print(f"\nNEW CANDIDATES (not in anchors): {len(new_candidates)}")
for pic, meaning in new_candidates[:15]:
    print(f"  + '{pic}' → '{meaning}'")

# Most frequent Kalyanaraman terms that overlap with anchor readings
print("\n=== MOST RELEVANT TERMS (by frequency × anchor overlap) ===\n")
overlap_terms = []
for term, count in kalyan_terms.most_common(100):
    if term in reading_to_sign:
        signs = reading_to_sign[term]
        overlap_terms.append((term, count, signs))

for term, count, signs in overlap_terms[:20]:
    conf = anchors[signs[0]].get("confidence", "?")
    print(f"  '{term}' (×{count}) → {signs[0]} [{conf}]: {anchors[signs[0]].get('reading','')}")

print(f"\nTotal anchor-overlapping terms: {len(overlap_terms)}")
print(f"\nSummary: {len(matches)} direct matches, {len(related)} related, "
      f"{len(new_candidates)} new candidates from {len(rows)} papers")
