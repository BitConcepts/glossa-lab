"""Probe RMRL viewer pages with Playwright to discover the PDF URL pattern.

Loads ONE viewer page from each of:
  - personal-archives/mahadevan/notebook?id=d1
  - personal-archives/manivannan/manuscript?id=RMRL_0001.pdf
  - research-papers/mahadevan/ebook?id=Murukan in the Indus script_1999

Captures every network request and prints any URL containing 's3', 'amazon',
'.pdf', '/api/', or 'rmrldl'. The goal is to identify the URL pattern used
to fetch PDFs so we can build a polite scraper without re-rendering each page.
"""
from __future__ import annotations
import asyncio
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROBES = [
    ("notebook_d1",
     "https://rmrl.in/en/dl/personal-archives/mahadevan/notebook?id=d1"),
    ("manuscript_RMRL_0001",
     "https://rmrl.in/en/dl/personal-archives/manivannan/manuscript?id=RMRL_0001.pdf"),
    ("ebook_murukan_1999",
     "https://rmrl.in/en/dl/research-papers/mahadevan/ebook?id=Murukan in the Indus script_1999"),
]


async def main() -> int:
    from playwright.async_api import async_playwright  # noqa: PLC0415

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Glossa-Lab Indus Decipherment Research Project; "
                "+https://github.com/layer1labs/glossa-lab; oz-agent@warp.dev)"
            )
        )
        results = {}
        for label, url in PROBES:
            print(f"\n=== Probing {label}: {url}")
            page = await ctx.new_page()
            requests: list[dict] = []

            def on_request(req):
                u = req.url
                if any(k in u for k in (".pdf", "amazon", "s3", "/api/",
                                          "rmrldl", "storage", "blob")):
                    requests.append({
                        "url": u,
                        "method": req.method,
                        "resource_type": req.resource_type,
                    })

            page.on("request", on_request)
            try:
                await page.goto(url, wait_until="networkidle", timeout=45000)
                await page.wait_for_timeout(3000)
            except Exception as exc:
                print(f"  GOTO ERROR: {exc}")
            print(f"  Captured {len(requests)} relevant requests:")
            for r in requests[:30]:
                print(f"    [{r['resource_type']}] {r['method']} {r['url'][:200]}")
            results[label] = {"page_url": url, "requests": requests}
            await page.close()
            await asyncio.sleep(3)  # polite delay

        await browser.close()
        out = REPO / "corpora" / "downloads" / "rmrl_recon" / "playwright_probe.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nSaved probe results to: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
