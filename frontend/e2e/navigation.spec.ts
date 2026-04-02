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
    await expect(page.getByText("Ancient & modern language analysis")).toBeVisible();
  });

  test("renders all three navigation tabs", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("button", { name: "Status" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Corpora" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Jobs" })).toBeVisible();
  });
});

test.describe("Tab switching", () => {
  test("Status tab is active by default", async ({ page }) => {
    await page.goto("/");
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
