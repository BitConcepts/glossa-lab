import { test, expect } from "@playwright/test";

/**
 * Navigation tests — basic app shell and tab switching.
 * These tests do NOT require the backend to be running.
 */

test.describe("App shell", () => {
  test("loads the page and shows the Glossa Lab title", async ({ page }) => {
    await page.goto("/");
    // Title is in the header as h1
    await expect(page.locator("h1").filter({ hasText: "Glossa Lab" })).toBeVisible();
  });

  test("shows the subtitle text", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText(/Indus Script Analysis/i)).toBeVisible();
  });

  test("renders core navigation tabs", async ({ page }) => {
    await page.goto("/");
    for (const label of ["Status", "Corpora", "Jobs", "Reports", "Presets", "Settings"]) {
      await expect(page.getByRole("button", { name: label })).toBeVisible();
    }
  });
});

test.describe("Tab switching", () => {
  test("default tab shows Indus Studies heading", async ({ page }) => {
    await page.goto("/");
    // Default tab is 'studies'
    await expect(page.getByRole("heading", { name: "Indus Studies" })).toBeVisible();
  });

  test("clicking Status tab shows System Status view", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Status" }).click();
    await expect(page.getByRole("heading", { name: "System Status" })).toBeVisible();
  });

  test("clicking Corpora tab shows Corpora view", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Corpora" }).click();
    await expect(page.getByRole("heading", { name: "Corpora" })).toBeVisible();
  });

  test("clicking Jobs tab shows Jobs view", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Jobs" }).click();
    await expect(page.locator("h2").filter({ hasText: "Jobs" })).toBeVisible();
  });

  test("selected tab has a distinct visual style", async ({ page }) => {
    await page.goto("/");
    // "Indus Studies" is selected by default
    const studiesBtn = page.getByRole("button", { name: "Indus Studies" });
    const statusBtn = page.getByRole("button", { name: "Status" });
    const activeBg = await studiesBtn.evaluate((el) =>
      window.getComputedStyle(el).backgroundColor
    );
    const inactiveBg = await statusBtn.evaluate((el) =>
      window.getComputedStyle(el).backgroundColor
    );
    expect(activeBg).not.toBe(inactiveBg);
  });
});
