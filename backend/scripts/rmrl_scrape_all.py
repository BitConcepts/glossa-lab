"""Polite scraper for RMRL Mahadevan + Manivannan + Balakrishnan content.

Asset types and patterns discovered via Playwright probe:

  1. Research papers (PNG flipbook + full OCR text in book_config.js):
     - Listing: https://rmrl.in/en/dl/research-papers/{author}
     - Per-paper text: https://s3.us-east-1.amazonaws.com/rmrldl.in/RP/{author_code}/{title}/files/search/book_config.js
     - The textForPages array in book_config.js IS the OCR'd text per page.

  2. Manuscripts (Manivannan, direct PDFs):
     - https://d2pqb2rl3mcws3.cloudfront.net/mss/RMRL_NNNN.pdf for N=1..63

  3. Notebooks (Mahadevan, PNG flipbook with EMPTY textForPages):
     - https://d2pqb2rl3mcws3.cloudfront.net/IMNB/d{N}/files/page/{P}.png
     - book_config.js indicates page count via array length
     - We just record page-count metadata; image download deferred to a later
       OCR-aware phase.

Politeness:
  - User-Agent identifies our research project + contact email
  - Min 1.5 sec between requests, 3 sec between pages
  - Honors HTTP 429 / 503 with exponential backoff
  - Caches every response locally; never re-fetches a successful response
  - Limits concurrency to 1 (serial)

Outputs (everything under corpora/downloads/rmrl/):
  - manuscripts/RMRL_NNNN.pdf  — 63 PDFs
  - notebooks/d{N}/book_config.js + meta.json  — page-count metadata
  - research_papers/{author}/listing.json  — all paper IDs from listing page
  - research_papers/{author}/{title}/book_config.js + text.json  — per-paper full text
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import urllib.request
import urllib.error

REPO = Path(__file__).resolve().parents[2]
DOWNLOADS = REPO / "corpora" / "downloads" / "rmrl"
DOWNLOADS.mkdir(parents=True, exist_ok=True)

UA = (
    "Mozilla/5.0 (Glossa-Lab Indus Decipherment Research Project; "
    "+https://github.com/layer1labs/glossa-lab; oz-agent@warp.dev)"
)
MIN_DELAY_SEC = 1.5
INTER_PAGE_DELAY_SEC = 3.0
MAX_RETRIES = 3
BACKOFF_BASE_SEC = 5.0


def polite_get(url: str, dest: Optional[Path] = None,
                expect_text: bool = False, max_retries: int = MAX_RETRIES) -> Optional[bytes | str]:
    """Polite GET. Saves to dest (creating parents) if provided. Returns content
    on success, None on failure. Skips if dest already exists.
    """
    if dest and dest.exists() and dest.stat().st_size > 0:
        if expect_text:
            return dest.read_text(encoding="utf-8", errors="replace")
        return dest.read_bytes()
    for attempt in range(max_retries):
        time.sleep(MIN_DELAY_SEC)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                content = resp.read()
                if dest:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(content)
                if expect_text:
                    return content.decode("utf-8", errors="replace")
                return content
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 503):
                wait = BACKOFF_BASE_SEC * (2 ** attempt)
                print(f"    HTTP {exc.code}; backing off {wait}s", flush=True)
                time.sleep(wait)
                continue
            print(f"    HTTPError {exc.code} for {url}: {exc.reason}", flush=True)
            return None
        except Exception as exc:  # noqa: BLE001
            print(f"    Error attempt {attempt+1}: {exc}", flush=True)
            time.sleep(BACKOFF_BASE_SEC * (2 ** attempt))
    print(f"    Giving up on {url}", flush=True)
    return None


# ─── Manuscripts (direct PDFs) ───────────────────────────────────────


def scrape_manuscripts(start: int = 1, end: int = 63) -> dict:
    """Download RMRL_NNNN.pdf manuscripts."""
    out_dir = DOWNLOADS / "manuscripts"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {"n_attempted": 0, "n_succeeded": 0, "n_failed": 0,
                "n_skipped_existing": 0, "files": []}
    for n in range(start, end + 1):
        results["n_attempted"] += 1
        fname = f"RMRL_{n:04d}.pdf"
        url = f"https://d2pqb2rl3mcws3.cloudfront.net/mss/{fname}"
        dest = out_dir / fname
        if dest.exists() and dest.stat().st_size > 0:
            results["n_skipped_existing"] += 1
            results["files"].append({"id": fname, "size": dest.stat().st_size,
                                       "status": "cached"})
            continue
        print(f"  [{n}/{end}] {fname}...", end=" ", flush=True)
        content = polite_get(url, dest)
        if content:
            size = dest.stat().st_size
            print(f"OK ({size/1024:.1f} KB)")
            results["n_succeeded"] += 1
            results["files"].append({"id": fname, "size": size, "status": "ok"})
        else:
            print("FAILED")
            results["n_failed"] += 1
            results["files"].append({"id": fname, "status": "failed"})
        time.sleep(INTER_PAGE_DELAY_SEC)
    return results


# ─── Notebooks (PNG flipbook, image-only — defer OCR) ────────────────


def scrape_notebooks(start: int = 1, end: int = 10) -> dict:
    """Download notebook book_config.js + record page-count metadata.

    Image download (per-page PNGs) is deferred to a future OCR phase. For now
    we just record what's there and the listing.
    """
    out_dir = DOWNLOADS / "notebooks"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {"n_attempted": 0, "n_succeeded": 0, "n_failed": 0, "files": []}
    for n in range(start, end + 1):
        results["n_attempted"] += 1
        d_dir = out_dir / f"d{n}"
        d_dir.mkdir(parents=True, exist_ok=True)
        config_url = (f"https://d2pqb2rl3mcws3.cloudfront.net/IMNB/d{n}"
                       f"/files/search/book_config.js")
        config_path = d_dir / "book_config.js"
        print(f"  [{n}/{end}] d{n} book_config.js...", end=" ", flush=True)
        text = polite_get(config_url, config_path, expect_text=True)
        if text is None:
            print("FAILED")
            results["n_failed"] += 1
            results["files"].append({"id": f"d{n}", "status": "failed"})
            continue
        # Parse textForPages array length to get page count
        page_count = 0
        text_pages = []
        m = re.search(r"var\s+textForPages\s*=\s*(\[[^\]]*\])", text, re.S)
        if m:
            arr_str = m.group(1)
            try:
                # Strip JS literal: works for arrays of strings
                text_pages = json.loads(arr_str)
                page_count = len(text_pages)
            except Exception:  # noqa: BLE001
                # Count quote pairs as a fallback
                page_count = arr_str.count('","') + 1 if arr_str.strip() != "[]" else 0
        n_with_text = sum(1 for t in text_pages if t and str(t).strip())
        meta = {
            "id": f"d{n}",
            "config_url": config_url,
            "page_count": page_count,
            "n_pages_with_ocr_text": n_with_text,
            "fully_text_indexed": n_with_text == page_count and page_count > 0,
            "image_pattern": (
                f"https://d2pqb2rl3mcws3.cloudfront.net/IMNB/d{n}/files/page/{{p}}.png"
            ),
        }
        if n_with_text > 0 and text_pages:
            # Save the OCR text if any
            (d_dir / "text.json").write_text(
                json.dumps({"pages": text_pages}, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            meta["text_saved"] = True
        (d_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"OK ({page_count} pages, {n_with_text} with OCR text)")
        results["n_succeeded"] += 1
        results["files"].append(meta)
        time.sleep(INTER_PAGE_DELAY_SEC)
    return results


# ─── Research papers ─────────────────────────────────────────────────


# Each author has a listing page + an internal author code for the S3 path.
# The S3 path uses an abbreviation:
#   Mahadevan = "IM" (Iravatham Mahadevan)
#   Balakrishnan = "RB" (R. Balakrishnan; verify when probing)
RP_AUTHOR_CODE = {
    "mahadevan": "IM",
    "balakrishnan": "BK",  # confirmed via Playwright probe
}


def fetch_paper_listing(author: str) -> list[dict]:
    """Fetch listing page and extract paper IDs from hrefs."""
    listing_url = f"https://rmrl.in/en/dl/research-papers/{author}"
    print(f"  Listing: {listing_url}")
    html = polite_get(listing_url, expect_text=True)
    if not html:
        return []
    pattern = (
        r'href="(/en/dl/research-papers/' + re.escape(author)
        + r'/ebook\?id=([^"]+))"'
    )
    matches = re.findall(pattern, html)
    seen = set()
    papers = []
    for href, raw_id in matches:
        # raw_id may be URL-encoded, so decode for the human-readable id
        decoded = urllib.parse.unquote(raw_id)
        if decoded in seen:
            continue
        seen.add(decoded)
        papers.append({"id": decoded, "href": href})
    return papers


def scrape_research_papers(author: str, max_papers: Optional[int] = None) -> dict:
    """For each paper in the listing, fetch book_config.js and extract OCR text."""
    out_dir = DOWNLOADS / "research_papers" / author
    out_dir.mkdir(parents=True, exist_ok=True)
    code = RP_AUTHOR_CODE.get(author, author[:2].upper())

    papers = fetch_paper_listing(author)
    print(f"  Found {len(papers)} papers in listing for '{author}'")
    (out_dir / "listing.json").write_text(
        json.dumps(papers, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    results = {"author": author, "code": code,
                "n_papers_listed": len(papers),
                "n_succeeded": 0, "n_failed": 0,
                "n_with_ocr_text": 0, "papers": []}

    if max_papers:
        papers = papers[:max_papers]

    for i, paper in enumerate(papers, 1):
        title = paper["id"]
        # Sanitize title for local filesystem (Windows-safe)
        safe_title = re.sub(r'[<>:"/\\|?*]', "_", title)[:200]
        paper_dir = out_dir / safe_title
        paper_dir.mkdir(parents=True, exist_ok=True)

        # S3 path uses URL-encoded title (spaces as %20)
        encoded_title = urllib.parse.quote(title, safe="")
        config_url = (
            f"https://s3.us-east-1.amazonaws.com/rmrldl.in/RP/{code}/"
            f"{encoded_title}/files/search/book_config.js"
        )
        config_path = paper_dir / "book_config.js"
        print(f"  [{i}/{len(papers)}] {title[:80]}...", end=" ", flush=True)
        text = polite_get(config_url, config_path, expect_text=True)
        if text is None:
            print("FAILED")
            results["n_failed"] += 1
            results["papers"].append({"id": title, "status": "failed"})
            continue
        # Parse textForPages
        page_count = 0
        text_pages: list[str] = []
        m = re.search(r"var\s+textForPages\s*=\s*(\[.*?\])\s*;?\s*$", text, re.S)
        if not m:
            m = re.search(r"var\s+textForPages\s*=\s*(\[.*?\])\s*$", text, re.S)
        if m:
            arr_str = m.group(1)
            try:
                # Replace JS escapes for parsing as JSON
                arr_normalized = re.sub(r"\\u000d", "\\\\u000d", arr_str)
                arr_normalized = re.sub(r"\\u000a", "\\\\u000a", arr_normalized)
                # Just use the original — the format is JSON-compatible if escapes are JSON-style
                text_pages = json.loads(arr_str)
                page_count = len(text_pages)
            except Exception as exc:  # noqa: BLE001
                # Fallback: split on '","'
                cleaned = arr_str.strip("[]")
                if cleaned:
                    parts = cleaned.split('","')
                    text_pages = [p.strip('"') for p in parts]
                    page_count = len(text_pages)
                print(f"(parse err: {exc})", end=" ")

        n_with_text = sum(1 for t in text_pages if t and str(t).strip())
        meta = {
            "id": title,
            "config_url": config_url,
            "page_count": page_count,
            "n_pages_with_ocr_text": n_with_text,
            "fully_text_indexed": n_with_text == page_count and page_count > 0,
        }
        if n_with_text > 0 and text_pages:
            (paper_dir / "text.json").write_text(
                json.dumps({"id": title, "pages": text_pages}, indent=2,
                            ensure_ascii=False),
                encoding="utf-8",
            )
            meta["text_saved"] = True
            results["n_with_ocr_text"] += 1
        (paper_dir / "meta.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"OK ({page_count} pages, {n_with_text} OCR'd)")
        results["n_succeeded"] += 1
        results["papers"].append(meta)
        time.sleep(INTER_PAGE_DELAY_SEC)

    return results


# ─── Main ────────────────────────────────────────────────────────────


def main() -> int:
    print("=== RMRL Polite Scraper ===")
    print(f"Output dir: {DOWNLOADS}")
    print(f"Politeness: {MIN_DELAY_SEC}s minimum, {INTER_PAGE_DELAY_SEC}s between assets, "
          f"backoff on 429/503\n")

    summary: dict = {}

    print("\n--- (1) Manuscripts (Manivannan, RMRL_0001..0063) ---")
    summary["manuscripts"] = scrape_manuscripts(1, 63)
    print(f"\n  Total: {summary['manuscripts']['n_succeeded']} new + "
          f"{summary['manuscripts']['n_skipped_existing']} cached, "
          f"{summary['manuscripts']['n_failed']} failed")

    print("\n--- (2) Notebooks (Mahadevan, d1..d10) ---")
    summary["notebooks"] = scrape_notebooks(1, 10)
    print(f"\n  Total: {summary['notebooks']['n_succeeded']} OK, "
          f"{summary['notebooks']['n_failed']} failed")

    print("\n--- (3) Research papers — Mahadevan ---")
    summary["research_papers_mahadevan"] = scrape_research_papers("mahadevan")
    print(f"\n  Total: {summary['research_papers_mahadevan']['n_succeeded']} OK, "
          f"{summary['research_papers_mahadevan']['n_failed']} failed, "
          f"{summary['research_papers_mahadevan']['n_with_ocr_text']} with OCR text")

    print("\n--- (4) Research papers — Balakrishnan ---")
    summary["research_papers_balakrishnan"] = scrape_research_papers("balakrishnan")
    print(f"\n  Total: {summary['research_papers_balakrishnan']['n_succeeded']} OK, "
          f"{summary['research_papers_balakrishnan']['n_failed']} failed, "
          f"{summary['research_papers_balakrishnan']['n_with_ocr_text']} with OCR text")

    summary_path = DOWNLOADS / "scrape_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                              encoding="utf-8")
    print(f"\n=== Summary saved: {summary_path} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
