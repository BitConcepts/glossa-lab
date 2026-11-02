#!/usr/bin/env python3
"""Render the built System graph surface for the T504 comparison.

Usage:  <venv-python-with-playwright> render-shots.py
Env:    GLOSSA_BASE_URL (default http://127.0.0.1:8001),
        GLOSSA_API_TOKEN (the backend's API token).

Captures the five screens at desktop (1440x1000) and mobile
(390x844), full page, into ./shots next to this script. The
served-identity probe runs first: the surface must carry the
new build's map stamp (the published artifact's ledger hash)
before any shot is taken — a stale server fails the run.
"""
from __future__ import annotations

import glob
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
BASE = os.environ.get("GLOSSA_BASE_URL", "http://127.0.0.1:8001")
TOKEN = os.environ.get("GLOSSA_API_TOKEN", "")


def _launch(p):
    candidates = sorted(
        glob.glob(
            os.path.expanduser(
                "~/.cache/ms-playwright/chromium_headless_shell-*/"
                "chrome-linux/headless_shell"
            )
        )
        + glob.glob(
            os.path.expanduser(
                "~/.cache/ms-playwright/chromium-*/chrome-linux/chrome"
            )
        )
    )
    for exe in reversed(candidates):
        try:
            return p.chromium.launch(executable_path=exe)
        except Exception:
            continue
    return p.chromium.launch()


def _fit_height(page, width: int) -> None:
    """The app scrolls inside its shell, so a full-page shot is
    only as tall as the viewport. Grow the viewport to the
    scroll container's full height so the shot shows the whole
    screen."""
    height = page.evaluate(
        """() => {
          let m = 0;
          document.querySelectorAll('*').forEach((el) => {
            if (el.scrollHeight > el.clientHeight && el.clientHeight > 200) {
              m = Math.max(m, el.scrollHeight);
            }
          });
          return m;
        }"""
    )
    if height:
        page.set_viewport_size(
            {"width": width, "height": min(int(height) + 140, 6000)}
        )
        page.wait_for_timeout(350)


def capture(browser, width: int, height: int, tag: str) -> None:
    context = browser.new_context(viewport={"width": width, "height": height})
    if TOKEN:
        context.add_init_script(
            f"sessionStorage.setItem('glossa_api_token', '{TOKEN}');"
        )
    page = context.new_page()
    page.goto(f"{BASE}/#/system-graph")
    page.wait_for_selector("[data-testid='indus-map-header']", timeout=30000)
    page.wait_for_timeout(700)
    stamp = page.inner_text("[data-testid='indus-map-stamp']")
    print(f"[{tag}] served stamp: {stamp}")
    if "c4e2326e" not in stamp or "fresh" not in stamp:
        raise SystemExit(
            f"SERVED-IDENTITY FAILURE [{tag}]: the surface does not "
            f"carry the new build's map stamp: {stamp!r}"
        )
    _fit_height(page, width)
    page.screenshot(path=str(SHOTS / f"01-system-view-{tag}.png"))
    page.get_by_role("button", name="Open the claim view →").click()
    page.wait_for_selector("text=Displayed score", timeout=15000)
    page.wait_for_timeout(500)
    _fit_height(page, width)
    page.screenshot(path=str(SHOTS / f"02-claim-view-{tag}.png"))
    page.get_by_role("button", name="Evidence view →").click()
    page.wait_for_selector("text=What bears on this claim", timeout=15000)
    page.wait_for_timeout(500)
    _fit_height(page, width)
    page.screenshot(path=str(SHOTS / f"03-evidence-view-{tag}.png"))
    page.get_by_role("button", name="Open the matrix →").click()
    page.wait_for_selector(
        "text=Claims × evidence — the generated matrix", timeout=15000
    )
    page.wait_for_timeout(500)
    _fit_height(page, width)
    page.screenshot(path=str(SHOTS / f"04-matrix-view-{tag}.png"))
    page.get_by_role("button", name="Settling", exact=True).click()
    page.wait_for_selector("text=Stored runs of record (T405)", timeout=15000)
    page.wait_for_timeout(500)
    _fit_height(page, width)
    page.screenshot(path=str(SHOTS / f"05-settling-panel-{tag}.png"))
    context.close()


def main() -> int:
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = _launch(p)
        capture(browser, 1440, 1000, "desktop")
        capture(browser, 390, 844, "mobile")
        browser.close()
    print(f"shots written to {SHOTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
