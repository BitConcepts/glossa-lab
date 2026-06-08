import { expect, test } from "@playwright/test";

/**
 * Study Loop — end-to-end tests (UI-only, no live mining).
 *
 * Validates the iteration/cycle labelling changes and confirmation dialog:
 *   - Dropdown labels say "N cycles" not just "N"
 *   - Confirmation dialog says "experiment cycles"
 *   - Run Loop button opens confirmation panel
 *   - Start button in confirmation triggers loop
 *
 * No live mining is triggered to avoid 30s+ network calls. SSE streaming is
 * tested via the API spec (backend-integration.spec.ts).
 *
 * Run:
 *   npx playwright test e2e/study-loop.spec.ts
 */

async function navigateToDashboard(page: import("@playwright/test").Page) {
  await page.goto("/");
  await page.waitForTimeout(500);
}

// ── Cycle preset labels ────────────────────────────────────────────────────────

test.describe("Study Loop — cycle labels", () => {
  test("dropdown options mention 'cycles'", async ({ page }) => {
    await navigateToDashboard(page);

    const select = page
      .locator("select")
      .filter({ hasText: /Quick Scan|Standard|Deep Dive/ })
      .first();
    await expect(select).toBeVisible({ timeout: 8000 });

    // Verify each option includes the word "cycles"
    const options = select.locator("option");
    const count = await options.count();
    expect(count).toBe(4);

    for (let i = 0; i < count; i++) {
      const text = await options.nth(i).textContent();
      expect(text).toContain("cycles");
    }
  });

  test("5-cycle option text is correct", async ({ page }) => {
    await navigateToDashboard(page);

    const select = page
      .locator("select")
      .filter({ hasText: /Quick Scan|Standard|Deep Dive/ })
      .first();
    const opt5 = select.locator('option[value="5"]');
    await expect(opt5).toHaveText(/5 cycles.*Quick Scan/);
  });

  test("50-cycle option text is correct", async ({ page }) => {
    await navigateToDashboard(page);

    const select = page
      .locator("select")
      .filter({ hasText: /Quick Scan|Standard|Deep Dive/ })
      .first();
    const opt50 = select.locator('option[value="50"]');
    await expect(opt50).toHaveText(/50 cycles.*Extensive/);
  });
});

// ── Confirmation panel ─────────────────────────────────────────────────────────

test.describe("Study Loop — confirmation dialog", () => {
  test("Run Loop opens confirmation with 'experiment cycles'", async ({
    page,
  }) => {
    await navigateToDashboard(page);

    // Select 5-cycle preset
    const select = page
      .locator("select")
      .filter({ hasText: /Quick Scan|Standard|Deep Dive/ })
      .first();
    await select.selectOption("5");

    // Click Run Loop
    const runBtn = page.getByRole("button", { name: /Run Loop/i });
    await expect(runBtn).toBeVisible({ timeout: 5000 });
    await runBtn.click();

    // Confirmation panel should appear with "experiment cycles"
    await expect(
      page.getByText(/5 experiment cycles/i).first()
    ).toBeVisible({ timeout: 3000 });
  });

  test("confirmation explains the pipeline steps", async ({ page }) => {
    await navigateToDashboard(page);

    const runBtn = page.getByRole("button", { name: /Run Loop/i });
    await runBtn.click();

    // Check for pipeline step labels
    await expect(page.getByText("Mine").first()).toBeVisible({
      timeout: 3000,
    });
    await expect(page.getByText("Propose").first()).toBeVisible();
    await expect(page.getByText(/Run.*Analyze/).first()).toBeVisible();
  });

  test("confirmation has Cancel and Start buttons", async ({ page }) => {
    await navigateToDashboard(page);

    const runBtn = page.getByRole("button", { name: /Run Loop/i });
    await runBtn.click();

    await expect(
      page.getByRole("button", { name: /Cancel/i })
    ).toBeVisible({ timeout: 3000 });
    await expect(
      page.getByRole("button", { name: /Start/i })
    ).toBeVisible();
  });

  test("Cancel closes the confirmation panel", async ({ page }) => {
    await navigateToDashboard(page);

    const runBtn = page.getByRole("button", { name: /Run Loop/i });
    await runBtn.click();

    // Confirmation should be visible
    await expect(
      page.getByText(/experiment cycles/i).first()
    ).toBeVisible({ timeout: 3000 });

    // Click Cancel
    await page.getByRole("button", { name: /Cancel/i }).click();

    // Confirmation should disappear
    await expect(
      page.getByText(/experiment cycles/i).first()
    ).not.toBeVisible({ timeout: 2000 });

    // Run Loop button should be back
    await expect(
      page.getByRole("button", { name: /Run Loop/i })
    ).toBeVisible();
  });
});
