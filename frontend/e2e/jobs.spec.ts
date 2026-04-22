import { test, expect } from "@playwright/test";

/**
 * Jobs view tests.
 * Structural tests do not require the backend.
 * Submission tests require the backend (guarded by env).
 */

// Pipelines guaranteed to exist in the backend catalog.
// "decipher", "hypothesis", "kandles" removed — no longer registered.
// Pipeline list is populated from the backend; without backend only
// "block_entropy" shows as the default fallback (see JobsView.tsx line 285).
const EXPECTED_PIPELINES_BACKEND = [
  "block_entropy",
  "char_freq",
  "positional",
  "cooccurrence",
  "paradigm",
  "sign_cluster",
  "numerals",
  "logosyllabic",
];

test.describe("Jobs view structure", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    // Use title attr to scope to sidebar nav button (avoids strict mode violation
    // caused by the bottom panel also having a 'Jobs' tab button).
    await page.getByTitle("Jobs").first().click();
    await expect(page.getByRole("heading", { name: "Jobs" })).toBeVisible();
  });

  test("shows the Jobs heading", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "Jobs" })).toBeVisible();
  });

  test("shows the submit summary element", async ({ page }) => {
    await expect(page.getByText("+ Submit new job")).toBeVisible();
  });

  test("expanding submit section shows job name field", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    await expect(
      page.getByPlaceholder(/Entropy analysis/i)
    ).toBeVisible();
  });

  test("submit form has pipeline selector", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    await expect(page.getByRole("combobox")).toBeVisible();
  });

  test("pipeline selector has at least one option", async ({ page }) => {
    // Without the backend, only the fallback default pipeline (block_entropy)
    // is shown. The combobox must have at least 1 option.
    await page.getByText("+ Submit new job").click();
    const select = page.getByRole("combobox");
    const options = await select.locator("option").allTextContents();
    expect(options.length).toBeGreaterThanOrEqual(1);
    // Default is always block_entropy
    expect(options).toContain("block_entropy");
  });

  test("submit form has parameters JSON textarea", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    // The params textarea should contain JSON.
    // Use first() to avoid strict mode: the AI panel may also have a textarea.
    const textarea = page.locator("textarea").first();
    await expect(textarea).toBeVisible();
    const value = await textarea.inputValue();
    expect(() => JSON.parse(value)).not.toThrow();
  });

  test("submit form has Submit button", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    await expect(page.getByRole("button", { name: "Submit" })).toBeVisible();
  });

  test("selecting a different pipeline updates the params field (requires backend)", async ({ page }) => {
    // This test only makes sense with the backend providing multiple pipeline options.
    // Without backend, only block_entropy is shown so switching is impossible.
    await page.getByText("+ Submit new job").click();
    const select = page.getByRole("combobox");
    const options = await select.locator("option").allTextContents();
    if (options.length < 2) {
      // Backend not running — only one pipeline option, skip
      test.skip();
      return;
    }
    // Switch to any non-default pipeline
    const nonDefault = options.find(o => o !== "block_entropy") ?? options[0];
    await select.selectOption(nonDefault);
    const textarea = page.locator("textarea");
    const value = await textarea.inputValue();
    // Should still be valid JSON
    expect(() => JSON.parse(value)).not.toThrow();
  });
});

test.describe("Jobs view with backend", () => {
  test.skip(!process.env.BACKEND_RUNNING, "Skipped: set BACKEND_RUNNING=1 to run");

  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Jobs").first().click();
    await expect(page.getByRole("heading", { name: "Jobs" })).toBeVisible();
  });

  test("pipeline selector contains all registered pipelines", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    const select = page.getByRole("combobox");
    const options = await select.locator("option").allTextContents();
    for (const pipeline of EXPECTED_PIPELINES_BACKEND) {
      expect(options).toContain(pipeline);
    }
  });

  test("shows empty state message when no jobs exist", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Jobs").first().click();
    const emptyMsg = page.getByText(/No jobs yet/i);
    const table = page.locator("table");
    await expect(emptyMsg.or(table)).toBeVisible({ timeout: 5000 });
  });

  test("submitting a job with invalid JSON shows an error", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Jobs").first().click();
    await page.getByText("+ Submit new job").click();

    await page.getByPlaceholder(/Entropy analysis/i).fill("Test job");
    await page.locator("textarea").fill("not valid json");
    await page.getByRole("button", { name: "Submit" }).click();

    await expect(page.getByText(/valid JSON/i)).toBeVisible();
  });

  test("submitting a job with empty name shows an error", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Jobs").first().click();
    await page.getByText("+ Submit new job").click();

    // Leave name blank, click Submit
    await page.getByRole("button", { name: "Submit" }).click();
    await expect(page.getByText(/name is required/i)).toBeVisible();
  });
});
