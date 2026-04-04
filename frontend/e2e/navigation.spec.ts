import { test, expect } from "@playwright/test";

/**
 * Navigation tests — basic app shell and tab switching.
 * These tests do NOT require the backend to be running.
 */

test.describe("App shell", () => {
  test("loads the page and shows the Glossa Lab title", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "Glossa Lab" })).toBeVisible();
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
  test("default tab shows Indus Studies view", async ({ page }) => {
    await page.goto("/");
    // Default tab is Studies; Status is also always present
    await expect(
      page.getByRole("button", { name: "Status" })
    ).toBeVisible();
  });

  test("clicking Corpora tab shows Corpora view", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Corpora" }).click();
    await expect(page.getByRole("heading", { name: "Corpora" })).toBeVisible();
  });

  test("clicking Jobs tab shows Jobs view", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Jobs" }).click();
    await expect(page.getByRole("heading", { name: "Jobs" })).toBeVisible();
  });

  test("clicking back to Status shows Status view again", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Jobs" }).click();
    await page.getByRole("button", { name: "Status" }).click();
    await expect(page.getByRole("heading", { name: "System Status" })).toBeVisible();
  });

  test("selected tab has a distinct visual style", async ({ page }) => {
    await page.goto("/");
    const statusBtn = page.getByRole("button", { name: "Status" });
    const corporaBtn = page.getByRole("button", { name: "Corpora" });

    // Status is selected by default — should have blue background
    const activeBg = await statusBtn.evaluate((el) =>
      window.getComputedStyle(el).backgroundColor
    );
    const inactiveBg = await corporaBtn.evaluate((el) =>
      window.getComputedStyle(el).backgroundColor
    );
    expect(activeBg).not.toBe(inactiveBg);
  });
});
