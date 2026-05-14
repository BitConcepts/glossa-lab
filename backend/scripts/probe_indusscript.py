"""indusscript.in Flutter/Firestore probe.

Downloads app bundle, service worker, asset manifests, and extracts
Firestore collection names and data paths from the compiled Dart bundle.

Phase A: Download static assets (no auth required)
Phase B: String extraction from main.dart.js
Phase C: Playwright-based network capture (requires user interaction)

Usage:
    shell.cmd python backend/scripts/probe_indusscript.py --phase A
    shell.cmd python backend/scripts/probe_indusscript.py --phase B
    shell.cmd python backend/scripts/probe_indusscript.py --phase C
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).parents[2]
OUT = REPO / "glossa-corpus" / "indus" / "sources" / "rmrl" / "raw" / "indusscript-probe"
OUT.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
BASE = "https://indusscript.in"


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def download(url: str, name: str, force: bool = False) -> Path:
    p = OUT / name
    if p.exists() and not force:
        print(f"  EXISTS: {name} ({p.stat().st_size:,} bytes)")
        return p
    try:
        data = fetch(url)
        p.write_bytes(data)
        print(f"  OK: {name} ({len(data):,} bytes)")
        return p
    except Exception as exc:
        print(f"  FAIL: {name} -> {exc}")
        return p


def phase_a_download():
    """Download all publicly accessible static assets."""
    print("=== Phase A: Download static assets ===")

    # Main page first
    idx_path = download(f"{BASE}/", "index.html")

    # Get service worker version from index.html
    if idx_path.exists():
        idx = idx_path.read_text(encoding="utf-8", errors="replace")
        sw_match = re.search(r'flutter_service_worker\.js\?v=(\d+)', idx)
        if sw_match:
            sw_url = f"{BASE}/flutter_service_worker.js?v={sw_match.group(1)}"
            download(sw_url, "flutter_service_worker.js")

        # Find main.dart.js (may have hash suffix)
        dart_match = re.search(r'src="(main\.dart[^"]*\.js)"', idx)
        if dart_match:
            dart_file = dart_match.group(1)
            dart_url = f"{BASE}/{dart_file}"
            print(f"  main.dart.js URL: {dart_url}")
            download(dart_url, "main.dart.js", force=False)
            # Check for source map
            map_url = dart_url + ".map"
            download(map_url, "main.dart.js.map")
        else:
            # Try standard name
            download(f"{BASE}/main.dart.js", "main.dart.js")
            download(f"{BASE}/main.dart.js.map", "main.dart.js.map")

    # Flutter asset manifests
    for name, path in [
        ("manifest.json", "/manifest.json"),
        ("AssetManifest.json", "/assets/AssetManifest.json"),
        ("FontManifest.json", "/assets/FontManifest.json"),
        ("NOTICES", "/assets/NOTICES"),
    ]:
        download(f"{BASE}{path}", name)

    print(f"\nAssets saved to: {OUT}")
    print("Files:")
    for f in sorted(OUT.iterdir()):
        print(f"  {f.name}: {f.stat().st_size:,} bytes")


def phase_b_extract():
    """Extract Firestore collection names and data paths from main.dart.js."""
    print("=== Phase B: Extract strings from Flutter bundle ===")

    dart_js = OUT / "main.dart.js"
    if not dart_js.exists():
        print("  ERROR: main.dart.js not found. Run --phase A first.")
        return

    print(f"  Reading {dart_js.name} ({dart_js.stat().st_size:,} bytes)...")
    text = dart_js.read_text(encoding="utf-8", errors="ignore")

    # Extract all string literals
    strings = set(re.findall(r'["\']([^"\']{3,200})["\']', text))
    print(f"  Total unique strings: {len(strings):,}")

    # Keywords to look for
    firestore_kws = [
        "firestore", "collection", "documents", "where", "orderBy",
        "snapshot", "getDocs", "getDoc", "query"
    ]
    indus_kws = [
        "inscription", "sign", "seal", "mahadevan", "im77", "concordance",
        "corpus", "harappa", "mohenjo", "indus", "script", "grapheme",
        "text_id", "textId", "sign_id", "signId", "site_id", "siteId",
        "reading", "phoneme", "transliteration"
    ]
    route_kws = [
        "search", "detail", "browse", "home", "about", "page", "route",
        "nav", "screen", "list", "view"
    ]
    storage_kws = [
        "storage", "pdf", ".pdf", "gs://", "blob", "download", "url", "asset"
    ]

    all_kws = firestore_kws + indus_kws + route_kws + storage_kws

    hits = []
    for s in sorted(strings):
        if any(kw in s.lower() for kw in all_kws):
            hits.append(s)

    # Save results
    results = {
        "total_strings": len(strings),
        "keyword_hits": len(hits),
        "firestore_related": [s for s in hits if any(kw in s.lower() for kw in firestore_kws)],
        "indus_related": [s for s in hits if any(kw in s.lower() for kw in indus_kws)],
        "route_related": [s for s in hits if any(kw in s.lower() for kw in route_kws)],
        "storage_related": [s for s in hits if any(kw in s.lower() for kw in storage_kws)],
        "all_hits": hits,
    }
    out_path = OUT / "bundle_strings_analysis.json"
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Analysis saved: {out_path}")

    print(f"\n=== KEY FINDINGS ===")
    print(f"Firestore-related strings ({len(results['firestore_related'])}):")
    for s in results['firestore_related'][:30]:
        print(f"  {s}")

    print(f"\nIndus-related strings ({len(results['indus_related'])}):")
    for s in results['indus_related'][:30]:
        print(f"  {s}")

    print(f"\nStorage/PDF strings ({len(results['storage_related'])}):")
    for s in results['storage_related'][:20]:
        print(f"  {s}")

    # Also check AssetManifest for bundled data files
    asset_manifest = OUT / "AssetManifest.json"
    if asset_manifest.exists():
        try:
            assets = json.loads(asset_manifest.read_text(encoding="utf-8"))
            print(f"\nBundled assets ({len(assets)} total):")
            for path in sorted(assets.keys()):
                if any(x in path.lower() for x in ["json", "pdf", "csv", "txt", "data"]):
                    print(f"  {path}")
        except Exception as exc:
            print(f"  AssetManifest parse error: {exc}")

    # Check service worker for cached URLs
    sw = OUT / "flutter_service_worker.js"
    if sw.exists():
        sw_text = sw.read_text(encoding="utf-8", errors="ignore")
        cached = re.findall(r'["\']([^"\']*\.(json|pdf|csv|js|dart))["\']', sw_text)
        print(f"\nService worker cached files ({len(cached)}):")
        for path, ext in sorted(set(cached))[:20]:
            print(f"  {path}")


def phase_c_playwright():
    """Playwright-based live network capture from the running app."""
    print("=== Phase C: Playwright Firestore network capture ===")
    print("This requires user interaction to log in and navigate the app.")
    print()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run: shell.cmd python -m pip install playwright")
        print("Then: shell.cmd python -m playwright install chromium")
        return

    har_path = OUT / "indusscript.har"
    network_log = OUT / "firestore_network.tsv"
    storage_path = OUT / "storage_state.json"

    with sync_playwright() as p:
        # Use real installed Chrome — Playwright's bundled Chromium is blocked by Google sign-in.
        # Falls back to bundled Chromium if real Chrome is not found.
        try:
            browser = p.chromium.launch(
                channel="chrome",  # use system Chrome, not Playwright's "Chrome for Testing"
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
            )
            print("  Using real Chrome installation")
        except Exception:
            browser = p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
            )
            print("  WARNING: Using Playwright Chromium — Google sign-in may be blocked")
            print("  If blocked: close the popup, and try navigating without login")

        context = browser.new_context(
            viewport={"width": 1440, "height": 1000},
            locale="en-IN",
            record_har_path=str(har_path),
            record_har_content="embed",
            no_viewport=False,
        )
        page = context.new_page()

        firestore_calls = []
        all_network = []

        def on_response(response):
            url = response.url
            ctype = response.headers.get("content-type", "")
            status = response.status
            all_network.append((status, ctype, url))

            if any(x in url.lower() for x in [
                "firestore.googleapis.com", "identitytoolkit", "securetoken",
                "firebaseio.com", "googleapis.com/v1/projects/theindusscript",
                "main.dart.js", ".map", "assetmanifest", "pdf", "json"
            ]):
                try:
                    body = response.text()
                except Exception:
                    body = ""
                firestore_calls.append({
                    "status": status,
                    "url": url,
                    "content_type": ctype,
                    "body_preview": body[:2000],
                })
                fname = re.sub(r'[^a-zA-Z0-9._-]', '_', url)[:120]
                (OUT / f"net_{status}_{fname}.txt").write_text(
                    f"URL: {url}\nSTATUS: {status}\nCONTENT-TYPE: {ctype}\n\n{body[:10000]}",
                    encoding="utf-8", errors="replace"
                )

        page.on("response", on_response)

        print("Opening indusscript.in in Chromium...")
        page.goto("https://indusscript.in", wait_until="networkidle", timeout=90000)
        (OUT / "rendered_home.html").write_text(page.content(), encoding="utf-8")
        print("Home page loaded. Saved: rendered_home.html")
        print()
        print(">>> INSTRUCTIONS:")
        print("1. Log in with Google if you have an account")
        print("2. Search for some inscriptions (e.g., 'M-1', 'fish sign', 'mohenjo')")
        print("3. Click on a few inscription records to load detail pages")
        print("4. Try to find a 'download' or 'export' option if visible")
        print("5. Press ENTER here when done to save all captured data")
        print()
        input("Press ENTER when done navigating...")

        (OUT / "rendered_after_navigation.html").write_text(page.content(), encoding="utf-8")
        context.storage_state(path=str(storage_path))

        with network_log.open("w", encoding="utf-8") as f:
            f.write("status\tcontent_type\turl\n")
            for status, ctype, url in all_network:
                f.write(f"{status}\t{ctype}\t{url}\n")

        fs_log = OUT / "firestore_calls.json"
        fs_log.write_text(json.dumps(firestore_calls, indent=2, ensure_ascii=False), encoding="utf-8")

        context.close()
        browser.close()

    print(f"\n=== Phase C complete ===")
    print(f"HAR: {har_path}")
    print(f"Firestore calls: {fs_log} ({len(firestore_calls)} entries)")
    print(f"Network log: {network_log}")
    print(f"Storage state: {storage_path}")
    print()
    print("Next: analyze firestore_calls.json for collection names and document paths")
    print("Look for URLs like: firestore.googleapis.com/v1/projects/theindusscript/databases/(default)/documents/COLLECTION_NAME")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["A", "B", "C", "all"], default="A")
    args = parser.parse_args()

    if args.phase in ("A", "all"):
        phase_a_download()
    if args.phase in ("B", "all"):
        phase_b_extract()
    if args.phase == "C":
        phase_c_playwright()
