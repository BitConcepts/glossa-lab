"""Museums of India Repository — Playwright network capture.

The museums-of-india.gov.in search API returns non-JSON when called directly.
This script uses Playwright to:
1. Load the repository page as a real browser
2. Capture ALL network requests made during manual search navigation
3. Identify the real search API endpoint, payload format, and response structure
4. Save all JSON responses for later processing

Usage:
    shell.cmd python backend/scripts/acquire_museums_of_india_playwright.py

IMPORTANT: This script requires MANUAL INTERACTION.
When the browser opens, search for: harappan, indus, mohenjo, dholavira
Click on results and let pages fully load before pressing ENTER.

Output:
    glossa-corpus/indus/sources/museums-of-india/raw/{date}/playwright_capture/
    - rendered_*.html       — saved page states
    - network.tsv           — all network requests
    - api_responses/        — JSON responses from discovered endpoints
    - endpoint_discovery.json — summary of real API endpoints found

Acquisition mode: browser_network_capture
"""
from __future__ import annotations
import json
import re
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
TODAY = datetime.utcnow().strftime("%Y-%m-%d")
RUN_TS = datetime.utcnow().strftime("%H%M%S")
OUT = REPO / "glossa-corpus" / "indus" / "sources" / "museums-of-india" / "raw" / TODAY / f"playwright_capture_{RUN_TS}"
OUT.mkdir(parents=True, exist_ok=True)
HAR_PATH = OUT / "museums_of_india.har"

LOG = OUT / "capture.log"

SEARCH_TERMS = ["harappan", "indus", "mohenjo", "dholavira", "harappa"]
TARGET = "https://museumsofindia.gov.in/repository/"


def log(msg: str) -> None:
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.")
        return

    log("=== Museums of India — Playwright Network Capture ===")
    log(f"Output: {OUT}")

    all_network: list[tuple] = []
    visited_urls: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="en-IN",
            record_har_path=str(HAR_PATH),
            record_har_content="embed",
        )
        page = context.new_page()

        def on_response(response):
            # Only record metadata — never call response.text() here.
            # Doing so inside a sync event handler causes greenlet deadlocks.
            # Full bodies are captured by the HAR recorder instead.
            try:
                url = response.url
                ctype = response.headers.get("content-type", "")
                status = response.status
                all_network.append((status, ctype, url))
            except Exception:
                pass

        def on_load(page_obj):
            try:
                url = page_obj.url
            except Exception:
                return
            visited_urls.append({"url": url, "ts": datetime.utcnow().isoformat()})
            log(f"PAGE NAVIGATED: {url}")

        page.on("response", on_response)
        page.on("load", lambda: on_load(page))

        log(f"Opening: {TARGET}")
        page.goto(TARGET, wait_until="networkidle", timeout=60000)
        (OUT / "rendered_home.html").write_text(page.content(), encoding="utf-8")
        log("Home page loaded. Saved: rendered_home.html")

        print()
        print("=" * 60)
        print("MANUAL INTERACTION REQUIRED")
        print("=" * 60)
        print()
        print("THIS SESSION — go through ALL of the following:")
        print()
        print("STEP 1 — Searches (do ALL 5):")
        for i, term in enumerate(SEARCH_TERMS, 1):
            print(f"  {i}. Search for: '{term}'")
        print("       For EACH: wait for results, scroll to see thumbnails")
        print()
        print("STEP 2 — Detail pages (CRITICAL — do this for each search):")
        print("    - Click a result card")
        print("    - LOOK at the browser address bar — note the full URL")
        print("    - Wait for the page to finish loading (even if broken)")
        print("    - Press F5 if it shows a blank/error — note if it loads on reload")
        print("    - Click BACK, try another result")
        print()
        print("STEP 3 — Pagination:")
        print("    - On any search with results, click 'Next page' or page 2")
        print("    - Let it load fully")
        print()
        print("STEP 4 — Browse by category (top nav):")
        print("    - Click any nav item: Object Type, Museum, Artist, etc.")
        print("    - Note what loads")
        print()
        print("  >> Watch the terminal — it will log every page navigation <<")
        print()
        print("  When done, come back here and press ENTER")
        print("=" * 60)
        input("\nPress ENTER when done navigating...")

        try:
            (OUT / "rendered_after_nav.html").write_text(page.content(), encoding="utf-8")
            log(f"Final page URL: {page.url}")
        except Exception as e:
            log(f"Could not save final page HTML: {e}")
        try:
            context.storage_state(path=str(OUT / "storage_state.json"))
        except Exception:
            pass
        context.close()
        browser.close()

    # Write visited URL log
    visited_path = OUT / "visited_urls.json"
    visited_path.write_text(json.dumps(visited_urls, indent=2), encoding="utf-8")
    log(f"Visited URLs saved: {visited_path} ({len(visited_urls)} navigations)")

    # Write network log
    net_path = OUT / "network.tsv"
    with net_path.open("w", encoding="utf-8") as f:
        f.write("status\tcontent_type\turl\n")
        for status, ctype, url in all_network:
            f.write(f"{status}\t{ctype}\t{url}\n")

    # Parse HAR file to extract JSON/API response bodies
    api_responses = []
    log("Parsing HAR file for response bodies...")
    try:
        har_data = json.loads(HAR_PATH.read_text(encoding="utf-8", errors="replace"))
        entries = har_data.get("log", {}).get("entries", [])
        interesting_kws = [
            "search", "api", "repository", "fetch", "record", "detail",
            "harappan", "indus", "mohenjo", "dholavira", "harappa",
            "query", "object", "nat_del", "collection",
        ]
        api_dir = OUT / "api_responses"
        api_dir.mkdir(exist_ok=True)
        for entry in entries:
            try:
                req = entry.get("request", {})
                resp = entry.get("response", {})
                url = req.get("url", "")
                status = resp.get("status", 0)
                ctype = resp.get("content", {}).get("mimeType", "")
                body_text = resp.get("content", {}).get("text", "")
                if not body_text or len(body_text) < 10:
                    continue
                is_json = "json" in ctype.lower()
                is_interesting = any(kw in url.lower() for kw in interesting_kws)
                if is_json or is_interesting:
                    resp_rec = {
                        "status": status,
                        "url": url,
                        "content_type": ctype,
                        "body_length": len(body_text),
                        "body_preview": body_text[:5000],
                    }
                    api_responses.append(resp_rec)
                    fname = re.sub(r'[^a-zA-Z0-9._-]', '_', url)[:100]
                    (api_dir / f"{status}_{fname}.txt").write_text(
                        f"URL: {url}\nSTATUS: {status}\nCONTENT-TYPE: {ctype}\n\n{body_text[:20000]}",
                        encoding="utf-8", errors="replace"
                    )
            except Exception:
                continue
        log(f"HAR parsed: {len(api_responses)} interesting responses extracted")
    except Exception as e:
        log(f"HAR parse failed: {e}")

    # Analyze what we found
    json_responses = [r for r in api_responses if "json" in r.get("content_type", "").lower()]
    potential_apis = [r for r in api_responses if any(kw in r["url"].lower() for kw in ["api", "search", "query", "fetch", "record", "detail"])]

    endpoint_discovery = {
        "_citation": {"primary_sources": ["I.7"]},
        "batch_id": f"{TODAY}-MUSEUMS-OF-INDIA-PLAYWRIGHT",
        "timestamp": datetime.utcnow().isoformat(),
        "total_network_requests": len(all_network),
        "interesting_responses": len(api_responses),
        "json_responses": len(json_responses),
        "potential_api_endpoints": len(potential_apis),
        "json_endpoint_urls": sorted(set(r["url"] for r in json_responses))[:50],
        "api_endpoint_urls": sorted(set(r["url"] for r in potential_apis))[:50],
        "visited_page_urls": [v["url"] for v in visited_urls],
        "har_path": str(HAR_PATH),
        "network_log": str(net_path),
        "instructions": {
            "next_step": "Analyze json_endpoint_urls and api_endpoint_urls to find stable search API",
            "look_for": [
                "URL pattern like /api/v1/search?q=harappan",
                "POST endpoints that accept search queries",
                "Pagination parameters",
                "Object detail endpoint pattern",
                "Image serving endpoint",
            ],
            "test_with": "curl -H 'Accept: application/json' '<discovered_url>'",
        },
    }
    disc_path = OUT / "endpoint_discovery.json"
    disc_path.write_text(json.dumps(endpoint_discovery, indent=2), encoding="utf-8")

    log(f"\n=== Capture Complete ===")
    log(f"Total requests: {len(all_network)}")
    log(f"Interesting responses: {len(api_responses)}")
    log(f"JSON endpoints found: {len(json_responses)}")
    log(f"HAR: {HAR_PATH}")
    log(f"Discovery report: {disc_path}")

    print("\n=== JSON API endpoints found ===")
    for url in endpoint_discovery["json_endpoint_urls"][:20]:
        print(f"  {url}")


if __name__ == "__main__":
    main()
