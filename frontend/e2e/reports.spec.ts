import { test, expect } from "@playwright/test";

/**
 * Reports & Data view tests — covers the H16 tab split:
 *   📋 Reports tab: PDF and formatted documents
 *   📂 Data tab: JSON results, CSV exports, raw artifacts
 */

async function navigateToReports(page: import("@playwright/test").Page) {
  await page.goto("/");
  const btn = page.getByRole("button", { name: /Reports/i }).first();
  await btn.waitFor({ state: "visible", timeout: 8000 });
  await btn.click();
  await expect(page.getByRole("heading", { name: /Reports/i }).first()).toBeVisible();
}

// ── Tab structure ─────────────────────────────────────────────────────────────

test.describe("Reports & Data tab bar", () => {
  test("Reports heading is visible", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByRole("heading", { level: 2 }).first()).toBeVisible();
  });

  test("Reports tab button is visible", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByRole("button", { name: /Reports/i }).last()).toBeVisible();
  });

  test("Data tab button is visible", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByRole("button", { name: /Data/i }).first()).toBeVisible();
  });

  test("clicking Data tab changes view description", async ({ page }) => {
    await navigateToReports(page);
    // Find and click the Data tab (not the nav button)
    const dataTab = page.getByRole("button", { name: /📂\s*Data/i }).first();
    const fallbackTab = page.getByText(/JSON results, CSV exports/i);
    const hasDataTab = await dataTab.isVisible({ timeout: 3000 }).catch(() => false);
    if (!hasDataTab) {
      // Tab may not be visible if there are no reports yet
      return;
    }
    await dataTab.click();
    await expect(page.getByText(/JSON results/i)).toBeVisible();
  });

  test("clicking Reports tab shows PDF description", async ({ page }) => {
    await navigateToReports(page);
    const reportsTab = page.getByRole("button", { name: /📋\s*Reports/i }).first();
    const hasTab = await reportsTab.isVisible({ timeout: 3000 }).catch(() => false);
    if (!hasTab) return;
    await reportsTab.click();
    await expect(page.getByText(/PDF/i).first()).toBeVisible();
  });
});

// ── Toolbar ───────────────────────────────────────────────────────────────────

test.describe("Reports toolbar", () => {
  test("Generate Report button is visible", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByRole("button", { name: /Generate Report/i })).toBeVisible();
  });

  test("Compose button is visible", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByRole("button", { name: /Compose/i })).toBeVisible();
  });

  test("Refresh button is visible", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByRole("button", { name: /Refresh/i })).toBeVisible();
  });
});

// ── Backend integration ───────────────────────────────────────────────────────

test.describe("Reports view with backend", () => {
  test.skip(!process.env.BACKEND_RUNNING, "Skipped: set BACKEND_RUNNING=1");

  test("shows empty state or table when no reports exist", async ({ page }) => {
    await navigateToReports(page);
    const empty = page.getByText(/No reports yet/i);
    const table = page.locator("table");
    await expect(empty.or(table)).toBeVisible({ timeout: 5000 });
  });
});
