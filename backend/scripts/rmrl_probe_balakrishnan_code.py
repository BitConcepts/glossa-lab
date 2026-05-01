"""Quick Playwright probe to determine the S3 author code for Balakrishnan +
also probe d8 notebook (which 403'd in scrape)."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


async def main():
    from playwright.async_api import async_playwright  # noqa: PLC0415
    PROBES = [
        ("balakrishnan_first_paper",
         "https://rmrl.in/en/dl/research-papers/balakrishnan/ebook?id=AFRICAN ROOTS OF THE DRAVIDIAN SPEAKING TRIBES"),
        ("notebook_d8",
         "https://rmrl.in/en/dl/personal-archives/mahadevan/notebook?id=d8"),
    ]
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Glossa-Lab Indus Decipherment Research Project; "
                "+https://github.com/layer1labs/glossa-lab; oz-agent@warp.dev)"
            )
        )
        out = {}
        for label, url in PROBES:
            print(f"\n=== {label}: {url}")
            page = await ctx.new_page()
            requests = []
            page.on("request", lambda req: requests.append({
                "url": req.url, "type": req.resource_type
            }) if any(k in req.url for k in (".pdf", "amazon", "s3",
                                                "rmrldl", "cloudfront")) else None)
            try:
                await page.goto(url, wait_until="networkidle", timeout=45000)
                await page.wait_for_timeout(3000)
            except Exception as exc:
                print(f"  GOTO ERROR: {exc}")
            print(f"  {len(requests)} relevant requests:")
            for r in requests[:15]:
                print(f"    [{r['type']}] {r['url'][:200]}")
            out[label] = requests
            await page.close()
            await asyncio.sleep(3)
        await browser.close()
        Path(REPO / "corpora" / "downloads" / "rmrl_recon" / "balakrishnan_d8_probe.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
