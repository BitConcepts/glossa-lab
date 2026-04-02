import { test, expect } from "@playwright/test";

/**
 * Corpora view tests.
 * Structural tests do not require the backend.
 * Upload interaction tests require the backend (guarded by env).
 */

test.describe("Corpora view structure", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Corpora" }).click();
    await expect(page.getByRole("heading", { name: "Corpora" })).toBeVisible();
  });

  test("shows the Corpora heading", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "Corpora" })).toBeVisible();
  });

  test("shows the upload summary element", async ({ page }) => {
    await expect(page.getByText("+ Upload new corpus")).toBeVisible();
  });

  test("expanding upload section reveals name field", async ({ page }) => {
    await page.getByText("+ Upload new corpus").click();
    await expect(page.getByPlaceholder(/Moby Dick/i)).toBeVisible();
  });

  test("upload form has corpus type selector", async ({ page }) => {
    await page.getByText("+ Upload new corpus").click();
    await expect(page.getByRole("combobox").first()).toBeVisible();
  });

  test("upload form has tokenisation selector", async ({ page }) => {
    await page.getByText("+ Upload new corpus").click();
    const selects = page.getByRole("combobox");
    // At least 2 selects: corpus type and tokenisation
    await expect(selects).toHaveCount(2);
  });

  test("upload form has content textarea", async ({ page }) => {
    await page.getByText("+ Upload new corpus").click();
    await expect(page.getByPlaceholder(/Paste text here/i)).toBeVisible();
  });

  test("upload form has Upload button", async ({ page }) => {
    await page.getByText("+ Upload new corpus").click();
    await expect(page.getByRole("button", { name: "Upload" })).toBeVisible();
  });

  test("tokenisation options include Character-level, Word/token-level, Line-level", async ({
    page,
  }) => {
    await page.getByText("+ Upload new corpus").click();
    const selects = page.getByRole("combobox");
    // Second select is tokenisation
    const tokenSelect = selects.nth(1);
    const options = await tokenSelect.locator("option").allTextContents();
    expect(options).toContain("Character-level");
    expect(options).toContain("Word/token-level");
    expect(options).toContain("Line-level");
  });

  test("corpus type options include linguistic, dna, ancient, code", async ({
    page,
  }) => {
    await page.getByText("+ Upload new corpus").click();
    const typeSelect = page.getByRole("combobox").first();
    const options = await typeSelect.locator("option").allTextContents();
    expect(options).toContain("linguistic");
    expect(options).toContain("dna");
    expect(options).toContain("ancient");
    expect(options).toContain("code");
  });
});

test.describe("Corpora view with backend", () => {
  test.skip(!process.env.BACKEND_RUNNING, "Skipped: set BACKEND_RUNNING=1 to run");

  test("shows empty state message when no corpora exist", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Corpora" }).click();
    // Either a table or the empty state message
    const emptyMsg = page.getByText(/No corpora yet/i);
    const table = page.locator("table");
    await expect(emptyMsg.or(table)).toBeVisible({ timeout: 5000 });
  });
});
