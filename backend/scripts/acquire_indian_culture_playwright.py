"""Indian Culture Portal — Playwright browser-rendered acquisition.

The portal blocks Python urllib (503) but serves correctly to real browsers.
This script uses Playwright Chromium to:
1. Load each target page as a real browser
2. Save rendered HTML
3. Extract all links (including PDF/ebook/download links)
4. Log all network responses (to find direct asset URLs)
5. Download any PDF or ebook files found

Target pages:
  - Mohenjo-daro and Indus Civilization
  - Harappa Excavations
  - Dholavira Antiquities

Usage:
    shell.cmd python backend/scripts/acquire_indian_culture_playwright.py

Output:
    glossa-corpus/indus/sources/indian-culture/raw/{date}/

Acquisition mode: browser_rendered (see AGENTS.md / acquisition_modes.yaml)
"""
from __future__ import annotations
import hashlib
import re
import time
import urllib.request
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
TODAY = datetime.utcnow().strftime("%Y-%m-%d")
OUT = REPO / "glossa-corpus" / "indus" / "sources" / "indian-culture" / "raw" / TODAY
OUT.mkdir(parents=True, exist_ok=True)

LOG = OUT / "playwright_acquisition.log"

TARGETS = [
    ("mohenjo-daro-civ",    "https://indianculture.gov.in/mohenjo-daro-and-indus-civilization"),
    ("mohenjo-daro-rare",   "https://indianculture.gov.in/rarebooks/mohenjo-daro-and-indus-civilization"),
    ("harappa-excavations", "https://indianculture.gov.in/ebooks/excavations-harappa"),
    ("dholavira",           "https://indianculture.gov.in/antiquities-dholavira-excavations-10"),
    ("indus-sites",         "https://indianculture.gov.in/indus-civilization"),
    ("mohenjo-museum",      "https://indianculture.gov.in/museums/mohenjo-daro"),
]

DOWNLOAD_KEYWORDS = [
    ".pdf", ".epub", ".djvu", "download", "ebook", "flipbook",
    "archive", "mohenjo", "harappa", "dholavira", "indus"
]


def log(msg: str) -> None:
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def safe_name(url: str) -> str:
    h = hashlib.sha256(url.encode()).hexdigest()[:12]
    base = url.split("/")[-1].split("?")[0]
    if not base or len(base) < 3:
        base = "asset"
    base = re.sub(r'[^a-zA-Z0-9._-]', '_', base)[:80]
    return f"{h}_{base}"


def download_file(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://indianculture.gov.in/"
        })
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        dest.write_bytes(data)
        log(f"    DOWNLOADED: {dest.name} ({len(data):,} bytes)")
        return True
    except Exception as exc:
        log(f"    FAIL DOWNLOAD: {url} -> {exc}")
        return False


def main() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.")
        print("Run: shell.cmd python -m pip install playwright")
        print("     shell.cmd python -m playwright install chromium")
        return

    log("=== Indian Culture Portal — Playwright Acquisition ===")
    log(f"Output: {OUT}")

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # headless=True first; set False if blocked
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="en-IN",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            extra_http_headers={
                "Accept-Language": "en-IN,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
            }
        )

        for slug, url in TARGETS:
            log(f"\n--- {slug}: {url} ---")
            page = context.new_page()

            network_responses = []
            page.on("response", lambda r: network_responses.append({
                "status": r.status,
                "url": r.url,
                "type": r.headers.get("content-type", ""),
            }))

            try:
                response = page.goto(url, wait_until="networkidle", timeout=45000)
                status = response.status if response else 0
                log(f"  Page status: {status}")

                if status == 503:
                    log(f"  BLOCKED (503): trying with headless=False not possible in this run")
                    log(f"  → Manual fallback: open {url} in Chrome, Save Page As, and put in {OUT}")
                    results[slug] = {"status": "blocked_503", "url": url}
                    page.close()
                    continue

                # Save rendered HTML
                html = page.content()
                html_path = OUT / f"{slug}.html"
                html_path.write_text(html, encoding="utf-8")
                log(f"  Saved HTML: {html_path.name} ({len(html):,} bytes)")

                # Extract all links
                links = page.eval_on_selector_all(
                    "a",
                    "els => els.map(a => ({text: a.innerText.trim(), href: a.href}))"
                )
                links_path = OUT / f"{slug}.links.tsv"
                with links_path.open("w", encoding="utf-8") as f:
                    f.write("text\thref\n")
                    for lnk in links:
                        href = lnk.get("href", "")
                        text = lnk.get("text", "").replace("\n", " ").strip()
                        if href:
                            f.write(f"{text}\t{href}\n")
                log(f"  Saved {len(links)} links to {links_path.name}")

                # Save network log
                net_path = OUT / f"{slug}.network.tsv"
                with net_path.open("w", encoding="utf-8") as f:
                    f.write("status\ttype\turl\n")
                    for r in network_responses:
                        f.write(f"{r['status']}\t{r['type']}\t{r['url']}\n")

                # Find downloadable assets
                download_links = [
                    lnk["href"] for lnk in links
                    if any(kw in lnk.get("href", "").lower() for kw in DOWNLOAD_KEYWORDS)
                ]
                # Also check network responses for direct PDF/ebook URLs
                for nr in network_responses:
                    if any(kw in nr["url"].lower() for kw in [".pdf", ".epub"]):
                        download_links.append(nr["url"])

                download_links = list(set(download_links))
                log(f"  Found {len(download_links)} download candidates")

                downloaded = 0
                for dl_url in download_links[:15]:  # cap at 15 per page
                    if not dl_url.startswith("http"):
                        continue
                    fname = safe_name(dl_url)
                    ext = dl_url.split(".")[-1].split("?")[0].lower()
                    if ext not in ("pdf", "epub", "djvu", "zip"):
                        ext = "pdf"
                    dest = OUT / f"{slug}_{fname}.{ext}"
                    if dest.exists():
                        log(f"    EXISTS: {fname}")
                        downloaded += 1
                        continue
                    time.sleep(1)
                    if download_file(dl_url, dest):
                        downloaded += 1

                results[slug] = {
                    "status": "ok",
                    "http_status": status,
                    "links": len(links),
                    "download_candidates": len(download_links),
                    "downloaded": downloaded,
                }

            except Exception as exc:
                log(f"  ERROR: {exc}")
                results[slug] = {"status": "error", "error": str(exc)}
            finally:
                page.close()
                network_responses.clear()

        browser.close()

    # Write summary
    import json
    report = {
        "_citation": {"primary_sources": ["I.5"]},
        "batch_id": f"{TODAY}-INDIAN-CULTURE-PLAYWRIGHT",
        "timestamp": datetime.utcnow().isoformat(),
        "output": str(OUT),
        "results": results,
    }
    rpt = OUT / "acquisition_report.json"
    rpt.write_text(json.dumps(report, indent=2), encoding="utf-8")
    log(f"\n=== DONE === Report: {rpt}")

    print("\nFallback instructions for any 503 results:")
    print("1. Open the URL manually in Chrome")
    print("2. Save Page As → Complete HTML")
    print("3. Export Network → HAR file")
    print(f"4. Put both in: {OUT}")
    print("5. Agent can extract PDF links from saved HTML")


if __name__ == "__main__":
    main()
