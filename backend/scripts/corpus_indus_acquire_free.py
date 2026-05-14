"""Indus Corpus — Free Source Acquisition (All Tiers).

Acquires from all free sources in priority order:

TIER 1 — Structured data, zero friction
  1. mayig/indus-valley-script-corpus (GitHub, MIT) — JSON inscriptions
  2. The Met Open Access API (CC0) — object metadata + public-domain images
  3. Cleveland Museum of Art Open Access API (CC0) — object metadata + images
  4. Penn Museum Collections CSV (CC BY 4.0) — object metadata

TIER 2 — India-side official portals (HTML/PDF, high provenance)
  5. Indian Culture portal — PDFs of excavation reports and rare books
  6. RMRL / Indus Research Centre — bulletins + indusscript.in portal
  7. Museums of India Repository — metadata discovery endpoint

TIER 3 — Internet Archive IIIF (derivative fallback, OCR only)
  8. Internet Archive IIIF — Mahadevan 1977 + corpus-vol-2 page images

Usage (via shell wrapper — NEVER call directly):
    shell.cmd python backend/scripts/corpus_indus_acquire_free.py [--tier 1|2|3|all]

Each source:
  - Downloads into glossa-corpus/indus/sources/{source}/raw/{date}/
  - Creates SHA-256 checksums
  - Writes/updates provenance.yaml (download_date, checksum, paths)
  - Writes structured acquisition log
  - Returns exit code 0 on success, 1 on any hard failure

_citation:
  primary_sources: ["I.1", "I.2", "I.3", "I.4", "I.5", "I.6", "I.7", "I.8"]
  derivation: "Acquisition script for ICIT-scale Indus corpus reconstruction.
               Source endpoints per deep-research-report.md (2026-05-14)."
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO = Path(__file__).parents[2]
CORPUS = REPO / "glossa-corpus" / "indus"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")
LOG_PATH = CORPUS / "sources" / f"acquisition_{TODAY}.log"

# ── Constants ─────────────────────────────────────────────────────────────────
UA = "GlossaCorpus/1.0 (indus-reconstruction; glossa-lab research)"
DEFAULT_TIMEOUT = 30
MET_SEARCH_URL = (
    "https://collectionapi.metmuseum.org/public/collection/v1/search"
    "?hasImages=true&q=Indus+Valley"
)
MET_OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{}"
CLEVELAND_SEARCH_URL = (
    "https://openaccess-api.clevelandart.org/api/artworks/"
    "?q=indus&limit=100&skip=0"
)
CLEVELAND_SEARCH_URL2 = (
    "https://openaccess-api.clevelandart.org/api/artworks/"
    "?q=harappan&limit=100&skip=0"
)
CLEVELAND_SEARCH_URL3 = (
    "https://openaccess-api.clevelandart.org/api/artworks/"
    "?q=mohenjo&limit=100&skip=0"
)
CLEVELAND_SEARCH_URL4 = (
    "https://openaccess-api.clevelandart.org/api/artworks/"
    "?q=pakistan+seal+steatite&limit=100&skip=0"
)
# Penn Museum bulk download options (try in order)
# The direct asset URL was found from the data.php page source (requires browser UA).
# File size: ~138MB, last updated 2026-05-14, CC BY 4.0
PENN_CSV_URLS = [
    "https://www.penn.museum/collections/assets/data/Penn_Museum_Collections_Data.csv",  # direct asset (confirmed working)
    "https://www.penn.museum/collections/objects/data.php",  # fallback page (need browser UA)
]
MAYIG_REPO = "https://github.com/mayig/indus-valley-script-corpus"
MUSEUMS_OF_INDIA_LIST = "https://museumsofindia.gov.in/repository/collection/musuemList"
# RMRL Bulletins: Only #1 and #6 are confirmed hosted on rmrl.in.
# Bulletins 2-5 return 404 — never uploaded online. Investigation confirms no
# alternative URL pattern works. Contact RMRL directly for offline copies.
# Firebase Realtime DB (theindusscript.firebaseio.com) requires auth beyond anonymous.
RMRL_BULLETINS = [
    ("bulletin-1",  "https://rmrl.in/bulletin/bulletin-No-1-Sept-2009.pdf"),
    # bulletin-2 through bulletin-5: Not available online (confirmed 404 on all URL variants)
    ("bulletin-6",  "https://rmrl.in/bulletin/bulletin-No-6-June-2025.pdf"),
]
# Met Museum GitHub bulk CSV (CC0) — more reliable than API (no rate limits/403 errors)
# Full dataset: 474,000+ objects, ~250MB CSV, CC0 license
MET_BULK_CSV_URL = "https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv"
INDIAN_CULTURE_PAGES = [
    ("mohenjo-daro-civ", "https://indianculture.gov.in/mohenjo-daro-and-indus-civilization"),
    ("mohenjo-daro-rare", "https://indianculture.gov.in/rarebooks/mohenjo-daro-and-indus-civilization"),
    ("harappa-excavations", "https://indianculture.gov.in/ebooks/excavations-harappa"),
    ("dholavira-antiquities", "https://indianculture.gov.in/antiquities-dholavira-excavations-10"),
]
INTERNET_ARCHIVE_ITEMS = [
    ("mahadevan1977",
     "https://iiif.archive.org/iiif/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/manifest.json"),
    ("corpus-vol-2",
     "https://iiif.archive.org/iiif/corpus-vol-2/manifest.json"),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def ts() -> str:
    return datetime.utcnow().isoformat()

def log(msg: str) -> None:
    line = f"[{ts()}] {msg}"
    print(line)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

def http_get(url: str, timeout: int = DEFAULT_TIMEOUT, browser_ua: bool = False) -> Optional[bytes]:
    """Fetch URL, return bytes or None on failure."""
    try:
        ua = BROWSER_UA if browser_ua else UA
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception as exc:
        log(f"  FAIL {url}: {exc}")
        return None

def http_get_json(url: str, timeout: int = DEFAULT_TIMEOUT, browser_ua: bool = False) -> Optional[dict]:
    data = http_get(url, timeout, browser_ua=browser_ua)
    if data is None:
        return None
    try:
        return json.loads(data)
    except Exception as exc:
        log(f"  JSON parse FAIL {url}: {exc}")
        return None

def save_file(dest: Path, data: bytes) -> str:
    """Save bytes to dest, return SHA-256."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return sha256_bytes(data)

def update_provenance(source_dir: Path, updates: dict) -> None:
    """Merge update dict into existing provenance.yaml."""
    prov_path = source_dir / "provenance.yaml"
    if not prov_path.exists():
        return
    # Simple key=value update — use lambda replacement to avoid backslash
    # escape issues with Windows paths in the replacement string.
    content = prov_path.read_text(encoding="utf-8")
    for key, value in updates.items():
        pattern = rf'^({re.escape(key)}:\s*).*$'
        # Normalize path separators to forward slashes to be safe in YAML
        safe_value = str(value).replace("\\", "/")
        content = re.sub(
            pattern,
            lambda m, v=safe_value: m.group(1) + f'"{v}"',
            content,
            flags=re.MULTILINE,
        )
    prov_path.write_text(content, encoding="utf-8")

def git_clone_shallow(repo_url: str, dest: Path) -> bool:
    if dest.exists() and any(dest.iterdir()):
        log(f"  EXISTS (pull update): {dest}")
        result = subprocess.run(
            ["git", "-C", str(dest), "pull", "--ff-only"],
            capture_output=True, text=True, timeout=120,
        )
        return result.returncode == 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "clone", "--depth=1", "--filter=blob:none", repo_url, str(dest)],
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode == 0:
        log(f"  Cloned {repo_url}")
        return True
    log(f"  Clone FAIL {repo_url}: {result.stderr[:300]}")
    return False

def write_batch_report(source: str, results: dict) -> None:
    rpt = {
        "batch_id": f"{TODAY}-INDUS-{source.upper()}",
        "source": source,
        "timestamp": ts(),
        "results": results,
    }
    rpt_path = CORPUS / "sources" / f"batch_{source}_{TODAY}.json"
    rpt_path.write_text(json.dumps(rpt, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"  Report: {rpt_path}")


# ── TIER 1: Structured data ───────────────────────────────────────────────────

def acquire_mayig() -> dict:
    """Clone/pull mayig/indus-valley-script-corpus (MIT)."""
    log("=== TIER 1: mayig/indus-valley-script-corpus ===")
    dest = CORPUS / "sources" / "mayig-cisi" / "raw" / TODAY
    ok = git_clone_shallow(MAYIG_REPO, dest)
    results = {"success": ok, "local_path": str(dest)}

    if ok:
        # Count inscription JSON files
        json_files = list(dest.rglob("*.json"))
        results["json_files_found"] = len(json_files)
        log(f"  JSON files: {len(json_files)}")
        # Sample: try to find inscription-like files
        inscription_files = [f for f in json_files if "inscription" in f.name.lower()
                             or "corpus" in f.name.lower() or "seal" in f.name.lower()]
        results["inscription_candidates"] = len(inscription_files)
        log(f"  Inscription candidates: {len(inscription_files)}")
        update_provenance(CORPUS / "sources" / "mayig-cisi", {
            "download_date": TODAY,
            "local_path": str(dest.relative_to(REPO)),
        })

    write_batch_report("mayig", results)
    return results


def acquire_met() -> dict:
    """Fetch Met Open Access data — bulk GitHub CSV (primary) + API search (supplement).

    GitHub CSV (CC0, ~250MB) contains all 474k+ Met objects with Indus filtering.
    API search used as supplement for objects that may have been added post-CSV.
    GitHub CSV avoids the 403 rate-limiting on the per-object API endpoints.
    Met GitHub CSV: https://github.com/metmuseum/openaccess (CC0)
    """
    log("=== TIER 1: Met Open Access (GitHub CSV + API supplement) ===")
    raw_dir = CORPUS / "sources" / "met-open-access" / "raw" / TODAY
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Strategy 1: Download GitHub bulk CSV and filter for Indus-related objects
    csv_path = raw_dir / "MetObjects_full.csv"
    filtered_path = raw_dir / "met_indus_filtered.csv"
    bulk_ok = False

    if not csv_path.exists():
        log(f"  Downloading Met bulk CSV (~250MB)...")
        data = http_get(MET_BULK_CSV_URL, timeout=600)  # large file
        if data and len(data) > 1_000_000:
            csv_path.write_bytes(data)
            log(f"  Saved bulk CSV: {len(data)//1024//1024}MB")
            bulk_ok = True
        else:
            log(f"  Bulk CSV download failed or too small, falling back to API")
    else:
        log(f"  Bulk CSV EXISTS: {csv_path} ({csv_path.stat().st_size//1024//1024}MB)")
        bulk_ok = True

    # Filter CSV for Indus-related rows
    indus_rows = []
    keywords = ["indus", "harappan", "mohenjo", "chanhu", "dholavira",
                "harappa", "pakistan", "seal", "steatite", "impression"]
    if bulk_ok and csv_path.exists():
        try:
            import csv as _csv, io as _io
            content = csv_path.read_text(encoding="utf-8", errors="replace")
            reader = _csv.DictReader(_io.StringIO(content))
            for row in reader:
                combined = " ".join(str(v) for v in row.values()).lower()
                if any(kw in combined for kw in keywords):
                    indus_rows.append(row)
            log(f"  Filtered to {len(indus_rows)} Indus-related objects from bulk CSV")
            # Save filtered CSV
            if indus_rows:
                with open(filtered_path, "w", encoding="utf-8", newline="") as f:
                    writer = _csv.DictWriter(f, fieldnames=list(indus_rows[0].keys()))
                    writer.writeheader()
                    writer.writerows(indus_rows)
        except Exception as exc:
            log(f"  CSV filter WARN: {exc}")

    # Strategy 2: API search for supplemental coverage (may have 403s, that's OK)
    search_terms = ["Indus+Valley", "Harappan", "Indus+script", "Mohenjo-daro"]
    all_object_ids: set = set()
    for term in search_terms:
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q={term}"
        data_json = http_get_json(url)
        if data_json and "objectIDs" in data_json:
            ids = data_json["objectIDs"] or []
            all_object_ids.update(ids)
            log(f"  API search '{term}': {len(ids)} objects")

    # Fetch API object records (only those not already in CSV, to avoid redundancy)
    existing_ids = {str(r.get("Object ID", "")) for r in indus_rows}
    api_objects = []
    failed = 0
    for obj_id in sorted(all_object_ids):
        if str(obj_id) in existing_ids:
            continue
        obj_data = http_get_json(MET_OBJECT_URL.format(obj_id), timeout=15)
        if obj_data:
            api_objects.append(obj_data)
        else:
            failed += 1
        time.sleep(0.15)

    # Save API supplement objects
    api_path = raw_dir / "met_indus_api_supplement.json"
    api_path.write_text(json.dumps(api_objects, indent=2, ensure_ascii=False), encoding="utf-8")
    chk = sha256_file(api_path)
    total = len(indus_rows) + len(api_objects)
    log(f"  Total: {len(indus_rows)} CSV + {len(api_objects)} API = {total} Indus objects")

    update_provenance(CORPUS / "sources" / "met-open-access", {
        "download_date": TODAY,
        "checksum_sha256": chk,
        "local_path": str(raw_dir.relative_to(REPO)),
    })

    results = {
        "csv_indus_rows": len(indus_rows),
        "api_supplement": len(api_objects),
        "api_failed": failed,
        "total_objects": total,
        "local_path": str(filtered_path),
        "checksum_sha256": chk,
    }
    write_batch_report("met", results)
    return results


def acquire_cleveland() -> dict:
    """Fetch Cleveland Museum of Art Open Access API — Indus-related objects (CC0)."""
    log("=== TIER 1: Cleveland Museum of Art Open Access API ===")
    raw_dir = CORPUS / "sources" / "cleveland-art" / "raw" / TODAY
    raw_dir.mkdir(parents=True, exist_ok=True)

    all_objects = []
    for url in [CLEVELAND_SEARCH_URL, CLEVELAND_SEARCH_URL2, CLEVELAND_SEARCH_URL3, CLEVELAND_SEARCH_URL4]:
        # Paginate: Cleveland API returns up to 100 per page
        skip = 0
        while True:
            paged_url = f"{url}&skip={skip}" if "skip=0" in url else f"{url}&skip={skip}"
            data = http_get_json(paged_url.replace("skip=0", f"skip={skip}"))
            if not data or not data.get("data"):
                break
            batch = data["data"]
            all_objects.extend(batch)
            log(f"  Fetched {len(batch)} objects (total so far: {len(all_objects)})")
            if len(batch) < 100:
                break
            skip += 100
            time.sleep(0.2)

    # Deduplicate by id
    seen: set = set()
    unique = []
    for obj in all_objects:
        oid = obj.get("id") or obj.get("accession_number", "")
        if oid not in seen:
            seen.add(oid)
            unique.append(obj)

    out_path = raw_dir / "cleveland_indus_objects.json"
    out_path.write_text(json.dumps(unique, indent=2, ensure_ascii=False), encoding="utf-8")
    chk = sha256_file(out_path)
    log(f"  Saved {len(unique)} unique objects -> {out_path.name} ({chk[:12]}...)")

    update_provenance(CORPUS / "sources" / "cleveland-art", {
        "download_date": TODAY,
        "checksum_sha256": chk,
        "local_path": str(raw_dir.relative_to(REPO)),
    })

    results = {"objects_fetched": len(unique), "local_path": str(out_path), "checksum_sha256": chk}
    write_batch_report("cleveland", results)
    return results


def acquire_penn() -> dict:
    """Download Penn Museum Collections CSV (CC BY 4.0)."""
    log("=== TIER 1: Penn Museum Collections CSV ===")
    raw_dir = CORPUS / "sources" / "penn-museum" / "raw" / TODAY
    raw_dir.mkdir(parents=True, exist_ok=True)

    data = None
    used_url = ""
    for penn_url in PENN_CSV_URLS:
        log(f"  Trying: {penn_url}")
        # Penn Museum requires browser UA for the data.php page;
        # the direct asset URL works with any UA but we use browser UA for consistency
        data = http_get(penn_url, timeout=300, browser_ua=True)
        if data and len(data) > 50_000:  # real CSV should be >50KB
            used_url = penn_url
            log(f"  Got {len(data)//1024}KB ({len(data)//1024//1024}MB) — looks like real CSV")
            break
        elif data:
            log(f"  WARN: Only {len(data)} bytes from {penn_url} — skipping (likely HTML)")
            data = None
    if data is None:
        log("  FAIL: No Penn Museum CSV endpoint returned usable data")
        return {"success": False, "note": "All Penn CSV URLs returned HTML or failed"}

    out_path = raw_dir / "penn_collections.csv"
    chk = save_file(out_path, data)
    size_kb = len(data) // 1024
    log(f"  Saved Penn CSV: {size_kb}KB -> {out_path.name} ({chk[:12]}...)")

    # Quick filter: find rows with Indus-related keywords
    try:
        content = data.decode("utf-8", errors="replace")
        lines = content.split("\n")
        header = lines[0] if lines else ""
        keywords = ["indus", "harappan", "mohenjo", "chanhu", "dholavira",
                    "harappa", "seal", "steatite", "pakistan", "india"]
        matching = [l for l in lines[1:] if any(kw in l.lower() for kw in keywords)]
        filtered_path = raw_dir / "penn_indus_filtered.csv"
        filtered_path.write_text(header + "\n" + "\n".join(matching), encoding="utf-8")
        log(f"  Filtered to {len(matching)} Indus-relevant rows")
    except Exception as exc:
        log(f"  Filter WARN: {exc}")
        matching = []

    update_provenance(CORPUS / "sources" / "penn-museum", {
        "download_date": TODAY,
        "checksum_sha256": chk,
        "local_path": str(raw_dir.relative_to(REPO)),
    })

    results = {
        "total_rows": len(lines) - 1 if 'lines' in dir() else 0,
        "indus_rows": len(matching),
        "local_path": str(out_path),
        "checksum_sha256": chk,
    }
    write_batch_report("penn", results)
    return results


# ── TIER 2: India-side official portals ───────────────────────────────────────

def acquire_indian_culture() -> dict:
    """Scrape Indian Culture portal pages and download linked PDFs/scans."""
    log("=== TIER 2: Indian Culture Portal ===")
    raw_dir = CORPUS / "sources" / "indian-culture" / "raw" / TODAY
    raw_dir.mkdir(parents=True, exist_ok=True)

    results: dict = {"pages": {}, "pdfs_downloaded": 0, "pdfs_failed": 0}

    for name, url in INDIAN_CULTURE_PAGES:
        log(f"  Fetching page: {name}")
        # Indian Culture Portal blocks Python urllib UA — requires browser UA
        data = http_get(url, timeout=30, browser_ua=True)
        if data is None:
            results["pages"][name] = "FAIL"
            continue
        html_path = raw_dir / f"{name}.html"
        save_file(html_path, data)
        results["pages"][name] = "OK"
        # Extract PDF/scan links
        html = data.decode("utf-8", errors="replace")
        pdf_links = re.findall(r'href=["\']([^"\']*\.pdf[^"\']*)["\']', html, re.IGNORECASE)
        epub_links = re.findall(r'href=["\']([^"\']*\.epub[^"\']*)["\']', html, re.IGNORECASE)
        all_links = pdf_links + epub_links
        log(f"    Found {len(all_links)} download links")
        for link in all_links[:10]:  # cap at 10 per page to avoid abuse
            if not link.startswith("http"):
                link = "https://indianculture.gov.in" + link
            fname = re.sub(r'[^a-zA-Z0-9._-]', '_', link.split("/")[-1].split("?")[0])
            dest = raw_dir / f"{name}_{fname}"
            if dest.exists():
                log(f"    EXISTS: {fname}")
                continue
            pdf_data = http_get(link, timeout=60, browser_ua=True)
            if pdf_data:
                save_file(dest, pdf_data)
                results["pdfs_downloaded"] += 1
                log(f"    OK: {fname} ({len(pdf_data)//1024}KB)")
            else:
                results["pdfs_failed"] += 1
            time.sleep(1)

    update_provenance(CORPUS / "sources" / "indian-culture", {
        "download_date": TODAY,
        "local_path": str(raw_dir.relative_to(REPO)),
    })
    write_batch_report("indian-culture", results)
    return results


def acquire_rmrl() -> dict:
    """Download RMRL bulletins and crawl indusscript.in."""
    log("=== TIER 2: RMRL / Indus Research Centre ===")
    raw_dir = CORPUS / "sources" / "rmrl" / "raw" / TODAY
    raw_dir.mkdir(parents=True, exist_ok=True)

    results: dict = {"bulletins": {}, "portal_pages": {}}

    # Download bulletins
    for name, url in RMRL_BULLETINS:
        dest = raw_dir / f"{name}.pdf"
        if dest.exists():
            log(f"  EXISTS: {name}")
            results["bulletins"][name] = "EXISTS"
            continue
        data = http_get(url, timeout=30)
        if data:
            chk = save_file(dest, data)
            results["bulletins"][name] = {"status": "OK", "size_kb": len(data) // 1024, "sha256": chk[:16]}
            log(f"  OK: {name} ({len(data)//1024}KB)")
        else:
            results["bulletins"][name] = "FAIL"
        time.sleep(1)

    # Crawl IRC portal page
    for name, url in [
        ("irc-portal", "https://rmrl.in/en/irc"),
        ("indusscript-home", "https://indusscript.in"),
        ("indusscript-about", "https://indusscript.in/about"),
    ]:
        data = http_get(url, timeout=20)
        if data:
            html_path = raw_dir / f"{name}.html"
            save_file(html_path, data)
            results["portal_pages"][name] = "OK"
            log(f"  Saved portal page: {name}")
        else:
            results["portal_pages"][name] = "FAIL"
        time.sleep(0.5)

    update_provenance(CORPUS / "sources" / "rmrl", {
        "download_date": TODAY,
        "local_path": str(raw_dir.relative_to(REPO)),
    })
    write_batch_report("rmrl", results)
    return results


def acquire_museums_of_india() -> dict:
    """Fetch Museums of India repository discovery metadata."""
    log("=== TIER 2: Museums of India Repository ===")
    raw_dir = CORPUS / "sources" / "museums-of-india" / "raw" / TODAY
    raw_dir.mkdir(parents=True, exist_ok=True)

    results: dict = {}

    # Museum list endpoint
    data = http_get_json(MUSEUMS_OF_INDIA_LIST, timeout=20)
    if data:
        out_path = raw_dir / "museum_list.json"
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        results["museum_list"] = {"status": "OK", "count": len(data) if isinstance(data, list) else 1}
        log(f"  Museum list: {out_path.name}")
    else:
        results["museum_list"] = "FAIL"

    # Search for Harappan/Indus objects
    for term in ["harappan", "indus", "mohenjo-daro", "seal"]:
        search_url = f"https://museumsofindia.gov.in/repository/search-api?query={term}&limit=50"
        sdata = http_get_json(search_url, timeout=20)
        if sdata:
            out_path = raw_dir / f"search_{term}.json"
            out_path.write_text(json.dumps(sdata, indent=2, ensure_ascii=False), encoding="utf-8")
            count = len(sdata) if isinstance(sdata, list) else sdata.get("total", "?")
            results[f"search_{term}"] = {"status": "OK", "count": count}
            log(f"  Search '{term}': {count} results")
        else:
            results[f"search_{term}"] = "FAIL"
        time.sleep(1)

    update_provenance(CORPUS / "sources" / "museums-of-india", {
        "download_date": TODAY,
        "local_path": str(raw_dir.relative_to(REPO)),
    })
    write_batch_report("museums-of-india", results)
    return results


# ── TIER 3: Internet Archive IIIF ─────────────────────────────────────────────

def acquire_internet_archive() -> dict:
    """Download IIIF manifests from Internet Archive (derivative fallback)."""
    log("=== TIER 3: Internet Archive IIIF (derivative fallback) ===")
    log("  NOTE: These are for OCR seeding only. Do not canonicalize without official reconciliation.")
    raw_dir = CORPUS / "sources" / "internet-archive" / "raw" / TODAY
    raw_dir.mkdir(parents=True, exist_ok=True)

    results: dict = {"manifests": {}, "page_images_fetched": 0}

    for name, manifest_url in INTERNET_ARCHIVE_ITEMS:
        log(f"  Fetching manifest: {name}")
        manifest = http_get_json(manifest_url, timeout=30)
        if manifest is None:
            results["manifests"][name] = "FAIL"
            continue
        m_path = raw_dir / f"{name}_manifest.json"
        m_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        chk = sha256_file(m_path)
        results["manifests"][name] = {"status": "OK", "sha256": chk[:16]}
        log(f"  Manifest saved: {name} ({chk[:12]}...)")

        # Extract a small sample of page image URLs (first 5 pages only)
        # Full image download should be done in a separate batch operation
        # Extract canvases — handle BOTH IIIF v2 and v3 formats:
        #   v2: manifest.sequences[].canvases[]
        #   v3: manifest.items[] (each item is a Canvas)
        canvases = []
        try:
            # IIIF v3: items[] at top level
            if manifest.get("items"):
                canvases = manifest["items"]
                log(f"  {name}: IIIF v3 format — {len(canvases)} canvases")
            # IIIF v2: sequences[].canvases[]
            elif manifest.get("sequences"):
                for seq in manifest["sequences"]:
                    canvases.extend(seq.get("canvases", []))
                log(f"  {name}: IIIF v2 format — {len(canvases)} canvases")
        except Exception:
            pass

        def _extract_image_url_v3(canvas: dict) -> Optional[str]:
            """Extract image URL from IIIF v3 canvas annotation structure."""
            try:
                for ap in canvas.get("items", []):  # AnnotationPages
                    for ann in ap.get("items", []):  # Annotations
                        body = ann.get("body", {})
                        if isinstance(body, dict):
                            u = body.get("id") or body.get("@id", "")
                            if u:
                                return u
                        elif isinstance(body, list):
                            for b in body:
                                u = b.get("id") or b.get("@id", "")
                                if u:
                                    return u
            except Exception:
                pass
            return None

        def _extract_image_url_v2(canvas: dict) -> Optional[str]:
            """Extract image URL from IIIF v2 canvas image structure."""
            try:
                for img in canvas.get("images", []):
                    resource = img.get("resource", {})
                    u = resource.get("@id") or resource.get("service", {}).get("@id", "")
                    if u:
                        return u
            except Exception:
                pass
            return None

        is_v3 = bool(manifest.get("items"))
        extractor = _extract_image_url_v3 if is_v3 else _extract_image_url_v2

        # Save page image URL list (download separately)
        urls_path = raw_dir / f"{name}_page_image_urls.json"
        all_canvas_urls = []
        for canvas in canvases:
            u = extractor(canvas)
            if u:
                all_canvas_urls.append(u)
        urls_path.write_text(json.dumps(all_canvas_urls, indent=2), encoding="utf-8")
        results["manifests"][name]["total_pages"] = len(canvases)
        results["manifests"][name]["iiif_version"] = "v3" if is_v3 else "v2"
        results["manifests"][name]["image_url_list"] = str(urls_path.relative_to(REPO))
        log(f"  {name}: {len(canvases)} pages, {len(all_canvas_urls)} image URLs saved")
        time.sleep(1)

    update_provenance(CORPUS / "sources" / "internet-archive", {
        "download_date": TODAY,
        "local_path": str(raw_dir.relative_to(REPO)),
    })
    write_batch_report("internet-archive", results)
    return results


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire free Indus corpus sources")
    parser.add_argument(
        "--tier", choices=["1", "2", "3", "all"], default="all",
        help="Which tier(s) to acquire (default: all)"
    )
    parser.add_argument(
        "--sources", nargs="*",
        choices=["mayig", "met", "cleveland", "penn", "indian-culture",
                 "rmrl", "museums-of-india", "internet-archive"],
        help="Specific sources to acquire (overrides --tier)"
    )
    args = parser.parse_args()

    log(f"=== Indus Free Source Acquisition — {TODAY} ===")
    log(f"  Tier: {args.tier}  Sources override: {args.sources}")
    log(f"  Output root: {CORPUS}")

    all_results: dict = {}
    errors = 0

    tier1 = [
        ("mayig", acquire_mayig),
        ("met", acquire_met),
        ("cleveland", acquire_cleveland),
        ("penn", acquire_penn),
    ]
    tier2 = [
        ("indian-culture", acquire_indian_culture),
        ("rmrl", acquire_rmrl),
        ("museums-of-india", acquire_museums_of_india),
    ]
    tier3 = [
        ("internet-archive", acquire_internet_archive),
    ]

    if args.sources:
        target_names = set(args.sources)
        all_sources = tier1 + tier2 + tier3
        to_run = [(n, fn) for n, fn in all_sources if n in target_names]
    elif args.tier == "1":
        to_run = tier1
    elif args.tier == "2":
        to_run = tier2
    elif args.tier == "3":
        to_run = tier3
    else:
        to_run = tier1 + tier2 + tier3

    for name, fn in to_run:
        log(f"\n{'='*60}")
        try:
            result = fn()
            all_results[name] = result
            if not result.get("success", True):
                errors += 1
        except Exception as exc:
            log(f"  ERROR in {name}: {exc}")
            all_results[name] = {"error": str(exc)}
            errors += 1

    # Write master acquisition report
    report = {
        "_citation": {
            "primary_sources": ["I.1", "I.2", "I.3", "I.4", "I.5", "I.6", "I.7", "I.8"],
            "derivation": "Acquisition run for ICIT-scale Indus corpus reconstruction.",
        },
        "batch_id": f"{TODAY}-INDUS-FREE-ALL",
        "timestamp": ts(),
        "tier": args.tier,
        "sources_run": [n for n, _ in to_run],
        "errors": errors,
        "results": all_results,
    }
    rpt_path = CORPUS / "sources" / f"master_acquisition_{TODAY}.json"
    rpt_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"\n=== DONE — {len(to_run)} sources, {errors} errors ===")
    log(f"Master report: {rpt_path}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
