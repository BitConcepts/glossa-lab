import { expect, test } from "@playwright/test";

/**
 * Navigation tests — app shell, grouped tab bar, header features.
 * Runs against vite preview (port 4173) without requiring the backend.
 */

test.describe("App shell", () => {
  test("loads and shows Glossa Lab title", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("h1").filter({ hasText: "Glossa Lab" })).toBeVisible();
  });

  test("shows collaboration subtitle", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText(/Indus Script Analysis/i)).toBeVisible();
  });

  test("shows health badge in header", async ({ page }) => {
    await page.goto("/");
    // Health badge contains "Healthy", "Degraded", or "Offline"
    await expect(page.locator("div").filter({ hasText: /Healthy|Degraded|Offline/ }).first()).toBeVisible();
  });

  test("shows Cmd+K button in header", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle(/Command palette/i)).toBeVisible();
  });

  test("shows dark mode toggle in header", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle(/Toggle dark mode/i)).toBeVisible();
  });
});

test.describe("Grouped tab navigation", () => {
  test("Core group is visible and expanded by default", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("button", { name: /Status/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Studies/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Experiments/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Corpora/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Reports/i })).toBeVisible();
  });

  test("default tab renders Studies view", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: /Studies/ })).toBeVisible();
  });

  test("clicking Status tab shows System Status", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: /^Status$/ }).first().click();
    await expect(page.getByRole("heading", { name: "System Status" })).toBeVisible();
  });

  test("clicking Experiments tab shows Experiments view", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: /^Experiments$/ }).first().click();
    await expect(page.getByRole("heading", { name: "Experiments" })).toBeVisible();
  });

  test("clicking Corpora tab shows Corpora view", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: /^Corpora$/ }).first().click();
    await expect(page.getByRole("heading", { name: "Corpora" })).toBeVisible();
  });

  test("AI group tabs are visible", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("button", { name: /AI Chat/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /AI Tools/i })).toBeVisible();
  });

  test("Research group tabs are visible", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("button", { name: /Hypotheses/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Notebooks/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Citations/i })).toBeVisible();
  });

  test("Analysis group tabs are visible", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("button", { name: /Entropy/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Timeline/i })).toBeVisible();
  });
});

test.describe("Dark mode", () => {
  test("toggling dark mode changes body background", async ({ page }) => {
    await page.goto("/");
    const before = await page.evaluate(() => document.body.style.background);
    await page.getByTitle(/Toggle dark mode/i).click();
    const after = await page.evaluate(() => document.body.style.background);
    expect(before).not.toBe(after);
  });

  test("dark mode preference persists via localStorage", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle(/Toggle dark mode/i).click();
    const stored = await page.evaluate(() => localStorage.getItem("glossa_dark"));
    expect(stored).toBe("1");
    // Toggle back
    await page.getByTitle(/Toggle dark mode/i).click();
    const stored2 = await page.evaluate(() => localStorage.getItem("glossa_dark"));
    expect(stored2).toBe("0");
  });
});
