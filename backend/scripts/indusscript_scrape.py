"""Scrape indusscript.in (Indus Research Centre concordance) with Playwright
persistent context to inherit Google authentication.

USAGE
=====

Step 1 (FIRST RUN ONLY) — interactive Google login:

    python backend/scripts/indusscript_scrape.py --auth

This launches a visible Chromium window pointed at indusscript.in. Sign in
with your Google account interactively. The session cookies + tokens are
saved to a dedicated profile dir at:
    corpora/downloads/indusscript_playwright_profile/

After signing in, navigate to a few pages within the site so cookies are
populated, then close the window. Authentication is done.

Step 2 (RECON) — discover what API endpoints / data the site exposes:

    python backend/scripts/indusscript_scrape.py --recon

This launches Chromium HEADLESS with the saved profile, navigates to several
candidate pages, and captures every network request to find the data
endpoints (Firestore, Firebase Storage, REST, etc.). Outputs to
corpora/downloads/indusscript_recon/network_log.json.

Step 3 (SCRAPE) — once we know the endpoints, fetch the data:

    python backend/scripts/indusscript_scrape.py --scrape

Currently this is a placeholder; will be filled in once recon shows what
endpoints to hit.

PROFILE PATH
============

The Playwright user-data-dir is at:
    corpora/downloads/indusscript_playwright_profile/

It holds: Chrome cookies, localStorage, IndexedDB, Firebase auth tokens,
and any other site state. This dir is gitignored.

Do NOT delete this dir between runs — it would invalidate the auth.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROFILE_DIR = REPO / "corpora" / "downloads" / "indusscript_playwright_profile"
RECON_DIR = REPO / "corpora" / "downloads" / "indusscript_recon"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)
RECON_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = (
    "Mozilla/5.0 (Glossa-Lab Indus Decipherment Research Project; "
    "+https://github.com/layer1labs/glossa-lab; oz-agent@warp.dev)"
)

LANDING_URL = "https://indusscript.in/"


# ─── Mode 1: interactive auth ────────────────────────────────────────


async def auth_mode():
    from playwright.async_api import async_playwright  # noqa: PLC0415

    print("=== indusscript.in interactive Google authentication ===")
    print(f"Profile dir: {PROFILE_DIR}")
    print()
    print("A Chromium window will open. Please:")
    print("  1. Sign in to indusscript.in with your Google account")
    print("  2. Browse a few concordance pages so cookies populate")
    print("  3. Close the window when done")
    print()
    print("Launching browser in 3 seconds...")
    await asyncio.sleep(3)

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            user_agent=USER_AGENT,
            viewport={"width": 1280, "height": 900},
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        await page.goto(LANDING_URL)
        print("Browser launched. Sign in then close the window when done.")

        # Wait for the user to close the browser
        try:
            while True:
                await asyncio.sleep(2)
                if not ctx.pages or all(p.is_closed() for p in ctx.pages):
                    break
                # check if browser disconnected
        except Exception:
            pass

        try:
            await ctx.close()
        except Exception:
            pass
        print("\n=== Auth complete. Profile saved. ===")
        print(f"To verify, run: python backend/scripts/indusscript_scrape.py --recon")


# ─── Mode 2: headless recon ──────────────────────────────────────────


CANDIDATE_PAGES = [
    "https://indusscript.in/",
    "https://indusscript.in/concordance",
    "https://indusscript.in/sign-list",
    "https://indusscript.in/inscription",
    "https://indusscript.in/search",
    "https://indusscript.in/about",
    "https://indusscript.in/data",
    "https://indusscript.in/download",
    "https://indusscript.in/export",
]


async def recon_mode():
    from playwright.async_api import async_playwright  # noqa: PLC0415

    print("=== indusscript.in network recon (HEADLESS, with auth) ===")

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            user_agent=USER_AGENT,
        )
        all_requests: list[dict] = []
        all_responses: list[dict] = []

        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        page.on(
            "request",
            lambda r: all_requests.append({
                "url": r.url,
                "method": r.method,
                "type": r.resource_type,
                "from_page": page.url,
            }),
        )
        page.on(
            "response",
            lambda r: all_responses.append({
                "url": r.url,
                "status": r.status,
                "from_page": page.url,
            }),
        )

        for url in CANDIDATE_PAGES:
            print(f"  Navigating: {url}")
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(2000)
                title = await page.title()
                # Try to capture some on-page text
                body_snippet = await page.evaluate(
                    "() => document.body ? document.body.innerText.substring(0, 500) : ''"
                )
                print(f"    Title: {title}")
                print(f"    Body snippet: {body_snippet[:200].replace(chr(10), ' / ')}")
            except Exception as exc:
                print(f"    ERROR: {exc}")
            await asyncio.sleep(2)

        # Summarize captured network
        print(f"\n  Captured {len(all_requests)} requests, "
              f"{len(all_responses)} responses")

        # Filter for interesting endpoints
        interesting_keywords = (
            "firestore", "firebase", "googleapis", "storage",
            "indusscript.in/api", "rest", ".json", "concordance",
            "sign", "download", "export",
        )
        interesting = [
            r for r in all_requests
            if any(k in r["url"].lower() for k in interesting_keywords)
            and not any(skip in r["url"] for skip in ("gtag", "google-analytics",
                                                        "fonts.googleapis"))
        ]

        out = {
            "n_total_requests": len(all_requests),
            "n_total_responses": len(all_responses),
            "n_interesting": len(interesting),
            "interesting_requests": interesting,
            "all_response_statuses": [
                {"url": r["url"], "status": r["status"]}
                for r in all_responses
                if r["status"] >= 400 or any(k in r["url"].lower()
                                                for k in interesting_keywords)
            ],
        }
        log_path = RECON_DIR / "network_log.json"
        log_path.write_text(json.dumps(out, indent=2, ensure_ascii=False),
                              encoding="utf-8")
        print(f"\n  Wrote {log_path}")

        try:
            await ctx.close()
        except Exception:
            pass


# ─── CLI ─────────────────────────────────────────────────────────────


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", action="store_true",
                          help="Interactive auth: launch visible browser, you sign in")
    parser.add_argument("--recon", action="store_true",
                          help="Headless recon with saved auth, capture network traffic")
    parser.add_argument("--scrape", action="store_true",
                          help="Scrape known endpoints (placeholder, fill in after recon)")
    args = parser.parse_args()

    if args.auth:
        await auth_mode()
    elif args.recon:
        await recon_mode()
    elif args.scrape:
        print("Scrape mode is a placeholder. Run --recon first to discover endpoints.")
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
