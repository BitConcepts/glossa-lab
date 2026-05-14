"""Final supplemental acquisition for high-confidence Indus terms, then full merge."""
import json
import html as html_mod
import re
import urllib.request
import urllib.parse
import time
from pathlib import Path
from datetime import datetime

BASE = "https://museumsofindia.gov.in/repository/search/basic/fetch"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://museumsofindia.gov.in/repository/",
}

FINAL_TERMS = [
    "mother goddess",   # 82  — Indus terracotta figurines
    "cemetery h",       # 38  — Cemetery H = late Harappan
    "humped",           # 165 — humped bull, dominant Indus seal motif
    "pipal",            # 29  — pipal tree motif on seals
    "painted grey ware",# 11  — related Iron Age successor culture
    "figurine",         # 946 — broad but high Indus yield
]

PAGE_SIZE = 28
DELAY = 1.5
TODAY = datetime.utcnow().strftime("%Y-%m-%d")
BASE_PATH = Path("glossa-corpus/indus/sources/museums-of-india/raw")
DAY_DIR = BASE_PATH / TODAY
OUT_DIR = DAY_DIR / "api_scrape_final_supp"
OUT_DIR.mkdir(exist_ok=True)
PAGES_DIR = OUT_DIR / "pages"
PAGES_DIR.mkdir(exist_ok=True)
LOG_PATH = OUT_DIR / "acquisition.log"


def log(msg):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def strip_html(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html_mod.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def fix_cdn(url):
    return re.sub(r"http:///+", "http://", url or "")


def fetch_json(url, retries=3):
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            log(f"  HTTP {e.code} attempt {attempt}")
            if e.code in (403, 404):
                return None
            time.sleep(2 * attempt)
        except Exception as e:
            log(f"  Error attempt {attempt}: {e}")
            time.sleep(2 * attempt)
    return None


def normalize(raw, terms_hit):
    rid = raw.get("recordIdentifier", "")
    return {
        "_citation": {"primary_sources": ["I.7"]},
        "record_id": rid,
        "museum_prefix": rid.split("-")[0] if rid else "",
        "title": raw.get("title", "").strip(),
        "name_to_view": raw.get("nameToView", "").strip(),
        "museum_name": raw.get("museumName", "").strip(),
        "description_html": raw.get("description", ""),
        "description_text": strip_html(raw.get("description", "")),
        "thumbnail_url": fix_cdn(raw.get("path", "")),
        "display_image_url": fix_cdn(raw.get("displayImage", "")),
        "search_terms_hit": terms_hit,
        "source": "museums-of-india",
        "source_url": f"https://museumsofindia.gov.in/repository/search/basic?searchterm={terms_hit[0]}&museumId=all",
        "acquired_utc": datetime.utcnow().isoformat(),
    }


# ── Acquire ─────────────────────────────────────────────────────────────────
log("=== Final Supplemental Acquisition ===")
new_records: dict[str, dict] = {}
term_stats = []

for i, term in enumerate(FINAL_TERMS):
    log(f"\n--- '{term}' ---")
    term_records = []
    result_size = 0

    for page_no in range(1, 200):
        params = urllib.parse.urlencode({
            "searchterm": term, "museumId": "all",
            "pageNo": page_no, "facetFilters": "{}", "anaglyph": "",
        })
        data = fetch_json(f"{BASE}?{params}")
        if not data or not data.get("resultFound"):
            break
        page_recs = data.get("listOfResult", [])
        if not page_recs:
            break
        if page_no == 1:
            result_size = data.get("resultSize", 0)
            log(f"  Total: {result_size}")
        (PAGES_DIR / f"{term.replace(' ', '_')}_page_{page_no:03d}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        term_records.extend(page_recs)
        log(f"  Page {page_no}: +{len(page_recs)} (total {len(term_records)})")
        total_pages = (result_size + PAGE_SIZE - 1) // PAGE_SIZE
        if page_no >= total_pages:
            break
        time.sleep(DELAY)

    term_new = 0
    for raw in term_records:
        rid = raw.get("recordIdentifier", "")
        if not rid:
            continue
        if rid in new_records:
            new_records[rid]["search_terms_hit"].append(term)
        else:
            new_records[rid] = normalize(raw, [term])
            term_new += 1

    term_stats.append({"term": term, "api_size": result_size, "new_here": term_new})
    log(f"  New in this batch: {term_new}")

    if i < len(FINAL_TERMS) - 1:
        time.sleep(3)

log(f"\nFinal supplemental batch: {len(new_records)} unique records")

# ── Full merge ───────────────────────────────────────────────────────────────
log("\n=== Full merge into definitive corpus ===")

EXISTING_MERGED = DAY_DIR / "api_scrape_merged" / "records.ndjson"
FINAL_OUT_DIR = DAY_DIR / "api_scrape_final"
FINAL_OUT_DIR.mkdir(exist_ok=True)

all_records: dict[str, dict] = {}

# Load existing merged
n_existing = 0
with open(EXISTING_MERGED, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        rid = r.get("record_id", "")
        if rid:
            all_records[rid] = r
            n_existing += 1

log(f"Loaded {n_existing} records from existing merged → {len(all_records)} unique")

# Merge final supplemental
n_new = 0
n_dupe = 0
for rid, record in new_records.items():
    if rid in all_records:
        existing = set(all_records[rid].get("search_terms_hit", []))
        incoming = set(record.get("search_terms_hit", []))
        all_records[rid]["search_terms_hit"] = sorted(existing | incoming)
        n_dupe += 1
    else:
        all_records[rid] = record
        n_new += 1

log(f"Final supplemental: {n_new} new, {n_dupe} dupes → total {len(all_records)} unique")

# Write final
final_path = FINAL_OUT_DIR / "records.ndjson"
with open(final_path, "w", encoding="utf-8") as f:
    for record in all_records.values():
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

log(f"Wrote {len(all_records)} records → {final_path}")

# Manifest
manifest = {
    "_citation": {"primary_sources": ["I.7"]},
    "batch_id": f"{TODAY}-MUSEUMS-OF-INDIA-FINAL",
    "acquired_utc": datetime.utcnow().isoformat(),
    "total_unique_records": len(all_records),
    "records_path": str(final_path),
    "all_search_terms": [
        "harappan", "indus", "mohenjo", "dholavira", "harappa",
        "steatite", "kalibangan", "unicorn", "chalcolithic", "etched bead",
        "proto-historic", "weight", "amri", "copper tablet", "chanhu",
        "rangpur", "ivory rod",
        "mother goddess", "cemetery h", "humped", "pipal",
        "painted grey ware", "figurine",
    ],
    "final_supplemental_terms": [s["term"] for s in term_stats],
    "final_supplemental_stats": term_stats,
}
(FINAL_OUT_DIR / "manifest.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
)

log("\n=== DONE ===")
log(f"FINAL TOTAL: {len(all_records)} unique records")
log(f"Output: {final_path}")
for s in term_stats:
    log(f"  {s['term']:20s}: {s['api_size']:4d} reported, {s['new_here']:4d} new to corpus")
