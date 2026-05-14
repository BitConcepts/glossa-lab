"""Museums of India Repository — Programmatic API acquisition.

Search API confirmed via Playwright discovery:
    /repository/search/basic/fetch
        ?searchterm=harappan
        &museumId=all
        &pageNo=1
        &facetFilters=%7B%7D
        &anaglyph=

Response structure per page:
    {
        "listOfResult": [ {recordIdentifier, title, description, path,
                           nameToView, museumName, displayImage}, ... ],
        "resultSize": 174,
        "resultFound": true,
        "facetMap": { "MuseumName": [...], "ObjectType": [...], ... }
    }

28 results per page. No auth required. No Playwright needed.

Usage:
    shell.cmd python backend/scripts/acquire_museums_of_india.py

Output:
    glossa-corpus/indus/sources/museums-of-india/raw/{date}/api_scrape/
    - pages/{term}_page_{n}.json   — raw API responses per page
    - records.ndjson               — all unique records, newline-delimited JSON
    - manifest.json                — run summary + facet data per term

Acquisition mode: api_direct
"""
from __future__ import annotations

import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO = Path(__file__).parents[2]
TODAY = datetime.utcnow().strftime("%Y-%m-%d")
OUT = (
    REPO
    / "glossa-corpus"
    / "indus"
    / "sources"
    / "museums-of-india"
    / "raw"
    / TODAY
    / "api_scrape"
)
OUT.mkdir(parents=True, exist_ok=True)

LOG = OUT / "acquisition.log"

BASE_URL = "https://museumsofindia.gov.in/repository/search/basic/fetch"

# Search terms targeting Indus Valley / Harappan material
SEARCH_TERMS = ["harappan", "indus", "mohenjo", "dholavira", "harappa"]

# Supplemental terms discovered via facet analysis and probe queries.
# Run separately: set SEARCH_TERMS = SUPPLEMENTAL_TERMS before running.
SUPPLEMENTAL_TERMS = [
    "steatite",       # material for Indus seals (284 results)
    "kalibangan",     # Indus site, Rajasthan (83)
    "unicorn",        # iconic Indus unicorn seal motif (79)
    "chalcolithic",   # period classification (68)
    "etched bead",    # characteristic Indus technique (59)
    "proto-historic", # period term (186)
    "weight",         # standardized cubical weights — IVC hallmark (405)
    "amri",           # Indus site, Sindh (31)
    "copper tablet",  # Indus inscribed copper tablets (29)
    "chanhu",         # Chanhu-daro site (20)
    "rangpur",        # Harappan site, Gujarat (17)
    "ivory rod",      # characteristic Indus artifact (11)
]

PAGE_SIZE = 28          # observed from API responses
DELAY_BETWEEN_PAGES = 1.5   # seconds — be polite to a government server
DELAY_BETWEEN_TERMS = 3.0
MAX_PAGES_PER_TERM = 200    # safety cap (~5,600 records)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://museumsofindia.gov.in/repository/",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def fix_cdn_url(url: str) -> str:
    """Fix the triple-slash bug in CDN URLs from the API.

    The API returns: http:///museumsofindia.gov.in:81/cdn/...
    Correct form:    http://museumsofindia.gov.in:81/cdn/...
    """
    return re.sub(r"http:///+", "http://", url or "")


def fetch_json(url: str, retries: int = 3) -> dict | None:
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8", errors="replace")
            return json.loads(body)
        except urllib.error.HTTPError as e:
            log(f"  HTTP {e.code} on attempt {attempt}: {url}")
            if e.code in (403, 404):
                return None
            time.sleep(2 * attempt)
        except Exception as e:
            log(f"  Error on attempt {attempt}: {e}")
            time.sleep(2 * attempt)
    return None


# ---------------------------------------------------------------------------
# Core acquisition
# ---------------------------------------------------------------------------

def fetch_all_pages(term: str, pages_dir: Path) -> list[dict]:
    """Fetch all pages for a single search term. Returns list of raw records."""
    log(f"\n--- Searching: '{term}' ---")
    records: list[dict] = []
    facets: dict = {}
    result_size: int = 0

    for page_no in range(1, MAX_PAGES_PER_TERM + 1):
        params = urllib.parse.urlencode({
            "searchterm": term,
            "museumId": "all",
            "pageNo": page_no,
            "facetFilters": "{}",
            "anaglyph": "",
        })
        url = f"{BASE_URL}?{params}"
        log(f"  Page {page_no}: {url}")

        data = fetch_json(url)
        if data is None:
            log(f"  Failed to fetch page {page_no} — stopping this term.")
            break

        if not data.get("resultFound"):
            log(f"  resultFound=false on page {page_no} — done.")
            break

        page_records = data.get("listOfResult", [])
        if not page_records:
            log(f"  Empty listOfResult on page {page_no} — done.")
            break

        # Capture metadata from first page
        if page_no == 1:
            result_size = data.get("resultSize", 0)
            facets = data.get("facetMap", {})
            log(f"  Total results reported: {result_size}")

        # Save raw page response
        page_path = pages_dir / f"{term}_page_{page_no:03d}.json"
        page_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        records.extend(page_records)
        log(f"  Collected {len(page_records)} records (running total: {len(records)})")

        # Check if we've retrieved all available results
        total_pages = (result_size + PAGE_SIZE - 1) // PAGE_SIZE
        if page_no >= total_pages:
            log(f"  Reached last page ({page_no}/{total_pages}).")
            break

        time.sleep(DELAY_BETWEEN_PAGES)

    log(f"  '{term}': {len(records)} records fetched (API reported {result_size})")
    return records, result_size, facets


def normalize_record(raw: dict, search_terms_hit: list[str]) -> dict:
    """Normalize a raw API record into a clean corpus record."""
    description_html = raw.get("description", "")
    record_id = raw.get("recordIdentifier", "")

    # Determine museum prefix (nat_del, ind_mus_kol, etc.) from record ID
    museum_prefix = record_id.split("-")[0] if record_id else ""

    thumbnail_url = fix_cdn_url(raw.get("path", ""))
    display_image_url = fix_cdn_url(raw.get("displayImage", ""))

    return {
        "_citation": {"primary_sources": ["I.7"]},
        "record_id": record_id,
        "museum_prefix": museum_prefix,
        "title": raw.get("title", "").strip(),
        "name_to_view": raw.get("nameToView", "").strip(),
        "museum_name": raw.get("museumName", "").strip(),
        "description_html": description_html,
        "description_text": strip_html(description_html),
        "thumbnail_url": thumbnail_url,
        "display_image_url": display_image_url,
        "search_terms_hit": search_terms_hit,
        "source": "museums-of-india",
        "source_url": f"https://museumsofindia.gov.in/repository/search/basic?searchterm={search_terms_hit[0]}&museumId=all",
        "acquired_utc": datetime.utcnow().isoformat(),
    }


def main() -> None:
    log("=== Museums of India — Programmatic API Acquisition ===")
    log(f"Output: {OUT}")
    log(f"Search terms: {SEARCH_TERMS}")

    pages_dir = OUT / "pages"
    pages_dir.mkdir(exist_ok=True)

    # Collect all records, deduplicating by recordIdentifier
    all_records: dict[str, dict] = {}   # record_id → normalized record
    manifest_terms: list[dict] = []

    for i, term in enumerate(SEARCH_TERMS):
        raw_records, result_size, facets = fetch_all_pages(term, pages_dir)

        term_new = 0
        term_dupe = 0
        for raw in raw_records:
            rid = raw.get("recordIdentifier", "")
            if not rid:
                continue
            if rid in all_records:
                # Already seen — append this term to search_terms_hit
                all_records[rid]["search_terms_hit"].append(term)
                term_dupe += 1
            else:
                all_records[rid] = normalize_record(raw, [term])
                term_new += 1

        manifest_terms.append({
            "term": term,
            "api_result_size": result_size,
            "pages_fetched": len(list(pages_dir.glob(f"{term}_page_*.json"))),
            "new_records": term_new,
            "duplicate_records": term_dupe,
            "facets": facets,
        })

        log(f"  New: {term_new} | Dupes: {term_dupe}")

        if i < len(SEARCH_TERMS) - 1:
            time.sleep(DELAY_BETWEEN_TERMS)

    # Write records.ndjson
    records_path = OUT / "records.ndjson"
    with records_path.open("w", encoding="utf-8") as f:
        for record in all_records.values():
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    log(f"\nWrote {len(all_records)} unique records → {records_path}")

    # Write manifest
    manifest = {
        "_citation": {"primary_sources": ["I.7"]},
        "batch_id": f"{TODAY}-MUSEUMS-OF-INDIA-API",
        "acquired_utc": datetime.utcnow().isoformat(),
        "search_terms": SEARCH_TERMS,
        "total_unique_records": len(all_records),
        "records_path": str(records_path),
        "terms": manifest_terms,
        "notes": [
            "Images served from port-81 CDN (http://museumsofindia.gov.in:81/cdn/...) — may be inaccessible from outside India",
            "detail page URLs not captured — site appears to render detail inline or detail pages are broken",
            "description field contains HTML — strip_html() applied for description_text",
        ],
    }
    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    log(f"Manifest written → {manifest_path}")
    log("\n=== Acquisition Complete ===")
    log(f"Total unique records: {len(all_records)}")
    for t in manifest_terms:
        log(f"  {t['term']:12s}: {t['api_result_size']:4d} reported, {t['new_records']:4d} new, {t['duplicate_records']:3d} dupes")


if __name__ == "__main__":
    main()
