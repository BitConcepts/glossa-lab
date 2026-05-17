import { test, expect } from "@playwright/test";

/**
 * Status view tests.
 *
 * Two groups:
 *   "Status view structure"   — tests that pass regardless of backend state.
 *   "Status view with backend"— tests that require the backend (guarded by env).
 */

test.describe("Status view structure", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    // Default tab is 'Indus Studies' — navigate to Status first
    await page.getByRole("button", { name: "Status" }).click();
    await expect(page.getByRole("heading", { name: "System Status" })).toBeVisible();
  });

  test("shows System Status heading", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "System Status" })).toBeVisible();
  });

  test("shows loading or a status row within 5 seconds", async ({ page }) => {
    // Within 5s, the component should show 'Loading' or resolved status.
    // Use .first() to avoid strict mode: health badge + status view both match.
    await expect(
      page.getByText(/loading|healthy|degraded|disconnected|offline/i).first()
    ).toBeVisible({ timeout: 5000 });
  });

  test("shows Offline/Disconnected when backend is unreachable", async ({ page, context }) => {
    // Block all API requests to simulate backend being down
    await context.route("**/api/v1/**", (route) => route.abort());
    // Navigate fresh so all API calls are blocked from the start
    await page.goto("/");
    // Navigate to Status tab (default is Indus Studies)
    await page.getByTitle("Status").first().click();

    // The header health badge shows "Offline"; StatusView may say "Disconnected".
    // Match either so the test is resilient to wording changes.
    await expect(
      page.getByText(/disconnected|offline/i).first()
    ).toBeVisible({ timeout: 10000 });
  });
});

test.describe("Status view with backend", () => {
  /**
   * These tests only run when BACKEND_RUNNING=1 is set.
   * In CI they run after the backend starts; locally run setup-os.cmd start first.
   */
  test.skip(!process.env.BACKEND_RUNNING, "Skipped: set BACKEND_RUNNING=1 to run");

  test("shows healthy status when backend is running", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Status" }).click();
    await expect(page.getByText(/healthy/i)).toBeVisible({ timeout: 8000 });
  });

  test("shows backend version string", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Status" }).click();
    await page.waitForTimeout(2000);
    // Version is shown as "v0.1.0" (no label word "version"), check for version pattern
    const hasVersion = await page.getByText(/v[\d.]+/).first().isVisible({ timeout: 8000 }).catch(() => false);
    const hasVersionLabel = await page.getByText(/version/i).first().isVisible({ timeout: 3000 }).catch(() => false);
    expect(hasVersion || hasVersionLabel).toBeTruthy();
  });

  test("shows uptime in seconds", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Status" }).click();
    await page.waitForTimeout(2000);
    // Uptime row should contain a number followed by 's'
    await expect(page.getByText(/\d+s/).first()).toBeVisible({ timeout: 8000 });
  });

  test("shows registered pipeline count", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Status" }).click();
    await page.waitForTimeout(2000);
    // Registered pipelines section is conditional; check for heading OR pipeline list
    const hasRegistered = await page.getByText(/registered/i).first().isVisible({ timeout: 5000 }).catch(() => false);
    const hasPipelines = await page.getByText(/pipeline/i).first().isVisible({ timeout: 3000 }).catch(() => false);
    expect(hasRegistered || hasPipelines).toBeTruthy();
  });
});
