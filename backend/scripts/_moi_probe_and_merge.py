"""Probe additional search terms and merge both record sets."""
import json
import urllib.request
import urllib.parse
import time
from pathlib import Path
from datetime import datetime

BASE = "https://museumsofindia.gov.in/repository/search/basic/fetch"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://museumsofindia.gov.in/repository/",
}

CANDIDATES = [
    "seal", "bead", "figurine", "inscribed", "bull",
    "mother goddess", "cemetery h", "painted grey ware",
    "carnelian", "tablet", "cord impression",
    "pipal", "humped", "zebu",
]

# ── Probe ──────────────────────────────────────────────────────────────────
print(f"Probing {len(CANDIDATES)} more candidate terms...\n")
for term in CANDIDATES:
    params = urllib.parse.urlencode({
        "searchterm": term, "museumId": "all",
        "pageNo": 1, "facetFilters": "{}", "anaglyph": "",
    })
    url = f"{BASE}?{params}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        size = data.get("resultSize", 0)
        found = data.get("resultFound", False)
        museums = data.get("facetMap", {}).get("MuseumName", [])
        mnames = ", ".join(
            f"{v['name'].split(',')[0]}({v['count']})" for v in museums[:3]
        )
        if found and size > 0:
            print(f"  {size:5d}  {term:25s}  [{mnames}]")
        else:
            print(f"      0  {term}")
    except Exception as e:
        print(f"  ERROR  {term}: {e}")
    time.sleep(0.8)

# ── Merge ──────────────────────────────────────────────────────────────────
print("\n\n=== MERGING RECORDS ===\n")

base_path = Path("glossa-corpus/indus/sources/museums-of-india/raw")
today = datetime.utcnow().strftime("%Y-%m-%d")
day_dir = base_path / today

src_a = day_dir / "api_scrape" / "records.ndjson"
src_b = day_dir / "api_scrape_supplemental" / "records.ndjson"
out_dir = day_dir / "api_scrape_merged"
out_dir.mkdir(exist_ok=True)

merged: dict[str, dict] = {}

def load_ndjson(path):
    count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                rid = r.get("record_id", "")
                if not rid:
                    continue
                if rid in merged:
                    # Merge search_terms_hit
                    existing_terms = set(merged[rid].get("search_terms_hit", []))
                    new_terms = set(r.get("search_terms_hit", []))
                    merged[rid]["search_terms_hit"] = sorted(existing_terms | new_terms)
                else:
                    merged[rid] = r
                count += 1
    return count

n_a = load_ndjson(src_a)
print(f"Loaded {n_a} records from primary scrape → {len(merged)} unique so far")

n_b = load_ndjson(src_b)
print(f"Loaded {n_b} records from supplemental scrape → {len(merged)} unique total")

# Write merged
out_path = out_dir / "records.ndjson"
with open(out_path, "w", encoding="utf-8") as f:
    for record in merged.values():
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"\nWrote {len(merged)} unique records → {out_path}")

# Manifest
manifest = {
    "_citation": {"primary_sources": ["I.7"]},
    "batch_id": f"{today}-MUSEUMS-OF-INDIA-MERGED",
    "acquired_utc": datetime.utcnow().isoformat(),
    "sources": [str(src_a), str(src_b)],
    "total_unique_records": len(merged),
    "records_path": str(out_path),
    "search_terms_primary": ["harappan", "indus", "mohenjo", "dholavira", "harappa"],
    "search_terms_supplemental": [
        "steatite", "kalibangan", "unicorn", "chalcolithic", "etched bead",
        "proto-historic", "weight", "amri", "copper tablet", "chanhu",
        "rangpur", "ivory rod",
    ],
}
(out_dir / "manifest.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(f"Manifest → {out_dir / 'manifest.json'}")
