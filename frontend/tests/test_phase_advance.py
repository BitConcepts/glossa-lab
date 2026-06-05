"""Playwright E2E test: Phase 5 advancement completes fully.

Clicks the Advance button repeatedly until the phase shows 'complete'.
Verifies each click advances to the next action (no infinite loops).
"""
import sys
from playwright.sync_api import sync_playwright, expect

BASE_URL = "http://127.0.0.1:8001"
MAX_ADVANCES = 8  # safety: abort if more clicks than expected actions


def test_phase_advance_to_completion():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app — the PhaseAdvancerPanel is on the Dashboard
        page.goto(BASE_URL, wait_until="load", timeout=20000)
        page.wait_for_timeout(3000)  # let React render + API calls settle
        print("  Page loaded")

        # Wait for the phase panel to appear
        phase_header = page.locator("text=PHASE").first
        phase_header.wait_for(timeout=10000)
        print("  Phase panel found")

        # Check if already all_done from a previous run
        all_done = page.locator('[data-testid="phase-all-done"]')
        if all_done.count() > 0:
            print("  Phase already complete — PASS (from prior state)")
            browser.close()
            return

        # Find the advance button
        advance_btn = page.locator('[data-testid="advance-button"]')
        if advance_btn.count() == 0:
            print("  ERROR: No advance button found")
            browser.close()
            sys.exit(1)

        remaining_before = advance_btn.inner_text()
        print(f"  Initial button: {remaining_before}")

        # Click Advance repeatedly until all_done appears or we hit the limit
        for click_num in range(1, MAX_ADVANCES + 1):
            # Click advance
            advance_btn = page.locator('[data-testid="advance-button"]')
            if advance_btn.count() == 0:
                # Check if phase completed
                if page.locator('[data-testid="phase-all-done"]').count() > 0:
                    print(f"  ✅ Phase complete after {click_num - 1} advances!")
                    break
                print(f"  ERROR: No advance button and no all_done after {click_num - 1} clicks")
                browser.close()
                sys.exit(1)

            btn_text = advance_btn.inner_text()
            print(f"  Click {click_num}: {btn_text}")
            advance_btn.click()

            # Wait for the button to re-enable (advancing state clears)
            page.wait_for_timeout(2000)  # wait for advance + refresh

            # Check for message
            msg = page.locator('[data-testid="advance-message"]')
            if msg.count() > 0:
                print(f"    → {msg.inner_text()[:100]}")

            # Check if complete
            if page.locator('[data-testid="phase-all-done"]').count() > 0:
                print(f"  ✅ Phase complete after {click_num} advances!")
                break
        else:
            print(f"  FAIL: Hit MAX_ADVANCES ({MAX_ADVANCES}) without completing")
            browser.close()
            sys.exit(1)

        # Final verification
        complete_badge = page.locator('[data-testid="phase-all-done"]')
        expect(complete_badge).to_be_visible()
        complete_text = complete_badge.inner_text()
        print(f"  Final: {complete_text}")
        assert "complete" in complete_text.lower(), f"Expected 'complete' in badge, got: {complete_text}"

        print("\n  ✅ PASS — Phase advancement works end-to-end")
        browser.close()


if __name__ == "__main__":
    test_phase_advance_to_completion()
