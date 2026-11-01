#!/usr/bin/env python3
"""Render every Spec 081 wireframe to PNG screenshots (desktop 1440 + mobile 390).

Usage:  <venv-python-with-playwright> render-shots.py
Output: shots/<screen>-desktop1440.png and shots/<screen>-mobile390.png
        next to the wireframe HTML files.

Tries, in order: Playwright's bundled Chromium, any cached Chromium headless
shell under ~/.cache/ms-playwright, then Playwright's Firefox. Full-page
captures, so each screenshot is the whole screen the owner is approving.
"""
import glob
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)

SCREENS = sorted(
    os.path.basename(p)
    for p in glob.glob(os.path.join(HERE, "[0-9][0-9]-*.html"))
)


def launch(p):
    """Return a browser, trying each available engine in turn."""
    try:
        return p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    except Exception as e:  # noqa: BLE001 - fall through to the next engine
        print(f"chromium default failed: {e.__class__.__name__}")
    for exe in sorted(
        glob.glob(
            os.path.expanduser(
                "~/.cache/ms-playwright/chromium_headless_shell-*/"
                "chrome-headless-shell-linux64/chrome-headless-shell"
            )
        )
        + glob.glob(
            os.path.expanduser(
                "~/.cache/ms-playwright/chromium-*/chrome-linux/chrome"
            )
        )
    ):
        try:
            return p.chromium.launch(
                executable_path=exe,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
        except Exception as e:  # noqa: BLE001
            print(f"chromium {exe} failed: {e.__class__.__name__}")
    return p.firefox.launch()


def main() -> int:
    if not SCREENS:
        print("no wireframe HTML files found", file=sys.stderr)
        return 1
    done = 0
    with sync_playwright() as p:
        browser = launch(p)
        for name in SCREENS:
            stem = name[:-5]  # strip .html
            uri = "file://" + os.path.join(HERE, name)
            for label, w, h in (("desktop1440", 1440, 1000), ("mobile390", 390, 844)):
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto(uri)
                page.wait_for_timeout(350)
                out = os.path.join(SHOTS, f"{stem}-{label}.png")
                page.screenshot(path=out, full_page=True)
                page.close()
                done += 1
                print(f"{out} {os.path.getsize(out)} bytes")
        browser.close()
    print(f"RENDERED {done} screenshots for {len(SCREENS)} screens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
