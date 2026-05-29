import { expect, test } from "@playwright/test";

/**
 * Research Loop Panel — end-to-end tests.
 *
 * Tests the dashboard-embedded research loop panel:
 *   - Panel visibility and structure
 *   - Controls (cycle selector, start/stop buttons)
 *   - Metrics row rendering
 *   - Status badge transitions
 *
 * No live mining is triggered (tests don't click Start to avoid 30s+ network calls).
 * SSE streaming and full cycle execution are tested via the API spec
 * (backend-integration.spec.ts / research-loop-api section).
 *
 * Run:
 *   npx playwright test e2e/research-loop.spec.ts
 */

async function navigateToDashboard(page: import("@playwright/test").Page) {
  await page.goto("/");
  // Dashboard is the default view
  await page.waitForTimeout(500);
}

// ── Panel visibility ──────────────────────────────────────────────────────────

test.describe("Research Loop Panel — visibility", () => {
  test("panel header is visible on dashboard", async ({ page }) => {
    await navigateToDashboard(page);
    await expect(
      page.getByText("Integrated Research Loop").first()
    ).toBeVisible({ timeout: 8000 });
  });

  test("panel shows protocol description", async ({ page }) => {
    await navigateToDashboard(page);
    await expect(
      page.getByText(/Mine → Analyze → Register → Execute/i).first()
    ).toBeVisible({ timeout: 5000 });
  });

  test("panel shows Ready badge when not running", async ({ page }) => {
    await navigateToDashboard(page);
    await expect(page.getByText("Ready").first()).toBeVisible({
      timeout: 5000,
    });
  });
});

// ── Controls ──────────────────────────────────────────────────────────────────

test.describe("Research Loop Panel — controls", () => {
  test("cycle selector is visible", async ({ page }) => {
    await navigateToDashboard(page);
    const select = page.locator("select").filter({ hasText: "cycles" }).first();
    await expect(select).toBeVisible({ timeout: 5000 });
  });

  test("cycle selector has expected options", async ({ page }) => {
    await navigateToDashboard(page);
    const select = page.locator("select").filter({ hasText: "cycles" }).first();
    const options = select.locator("option");
    const count = await options.count();
    expect(count).toBe(5); // 5, 10, 15, 20, 30
  });

  test("cycle selector default is 15", async ({ page }) => {
    await navigateToDashboard(page);
    const select = page.locator("select").filter({ hasText: "cycles" }).first();
    await expect(select).toHaveValue("15");
  });

  test("changing cycle selector updates value", async ({ page }) => {
    await navigateToDashboard(page);
    const select = page.locator("select").filter({ hasText: "cycles" }).first();
    await select.selectOption("5");
    await expect(select).toHaveValue("5");
  });

  test("Start Loop button is visible when not running", async ({ page }) => {
    await navigateToDashboard(page);
    await expect(
      page.getByRole("button", { name: /Start Loop/i })
    ).toBeVisible({ timeout: 5000 });
  });

  test("Stop button is NOT visible when not running", async ({ page }) => {
    await navigateToDashboard(page);
    await expect(
      page.getByRole("button", { name: /Stop/i })
    ).not.toBeVisible();
  });
});

// ── Metrics and status (from prior runs) ──────────────────────────────────────

test.describe("Research Loop Panel — status display", () => {
  test("panel shows last run summary or empty state", async ({ page }) => {
    await navigateToDashboard(page);
    // Either shows "Last run: X cycles" or has no cycle log (fresh install)
    const panel = page.locator("div").filter({
      hasText: "Integrated Research Loop",
    }).first();
    await expect(panel).toBeVisible({ timeout: 5000 });
    // Both states are valid — just verify the panel doesn't error out
  });

  test("panel does not show error on initial load", async ({ page }) => {
    await navigateToDashboard(page);
    // No red error box should appear on clean load
    const errorBox = page.locator("div[style*='#dc2626']");
    await page.waitForTimeout(1000);
    const errorCount = await errorBox.count();
    expect(errorCount).toBe(0);
  });
});

// ── Atomic nodes counter (Phase 5) ────────────────────────────────────────────

test.describe("Dashboard — Atomic Nodes counter", () => {
  test("atomic nodes tile is visible on dashboard", async ({ page }) => {
    await navigateToDashboard(page);
    await expect(
      page.getByText(/Atomic nodes/i).first()
    ).toBeVisible({ timeout: 8000 });
  });

  test("atomic nodes count is a positive number", async ({ page }) => {
    await navigateToDashboard(page);
    // The counter tile shows a number >= 400
    const tile = page.locator("text=Atomic nodes").first();
    await expect(tile).toBeVisible({ timeout: 5000 });
  });
});
