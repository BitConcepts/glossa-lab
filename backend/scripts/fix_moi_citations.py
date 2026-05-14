"""Fix _citation blocks in Museums of India records.ndjson to meet Citation Requirements Standard.

Per CITATIONS.md I.7 and the Citation Requirements Standard (v2, 2026-05-11),
every data file must include _citation with: primary_sources, derivation,
authors_credited, license, and rights notes.

Rights gate (CITATIONS.md I.7):
    india-museum-restricted — discovery and metadata reconciliation only.
    No ML training or redistribution without explicit per-record rights clearance.
"""
import json
from datetime import datetime
from pathlib import Path

BASE = Path("glossa-corpus/indus/sources/museums-of-india/raw")
TODAY = datetime.utcnow().strftime("%Y-%m-%d")
FINAL = BASE / TODAY / "api_scrape_final" / "records.ndjson"
OUT = BASE / TODAY / "api_scrape_final" / "records.ndjson"  # in-place

CITATION = {
    "primary_sources": ["I.7"],
    "derivation": (
        "Acquired programmatically from the Museums of India Repository search API "
        "(https://museumsofindia.gov.in/repository/search/basic/fetch) using 23 "
        "Indus Valley / Harappan keyword search terms. Records represent metadata "
        "only (title, description, museum name, object type, image URLs). "
        "Images are not downloaded (CDN inaccessible externally). "
        "Acquired 2026-05-14 via backend/scripts/acquire_museums_of_india.py."
    ),
    "authors_credited": [
        "Ministry of Culture, Government of India — Museums of India Repository",
        "C-DAC (Centre for Development of Advanced Computing) — portal operator",
    ],
    "year_data": "2026",
    "license": "india-museum-restricted — see CITATIONS.md I.7",
    "rights_gate": (
        "NO ML training or redistribution without explicit per-record rights clearance. "
        "Use for discovery and metadata reconciliation only. "
        "Source URL: https://museumsofindia.gov.in/repository/"
    ),
    "glossa_lab_version": "2026-05-14",
    "see_also": "CITATIONS.md section I.7",
}

records = []
with open(FINAL, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            r = json.loads(line)
            r["_citation"] = CITATION
            records.append(r)

with open(OUT, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"Updated {len(records)} records with full _citation block → {OUT}")
