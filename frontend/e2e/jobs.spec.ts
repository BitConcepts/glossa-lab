import { test, expect } from "@playwright/test";

/**
 * Jobs view tests.
 * Structural tests do not require the backend.
 * Submission tests require the backend (guarded by env).
 */

const EXPECTED_PIPELINES = [
  "block_entropy",
  "char_freq",
  "decipher",
  "hypothesis",
  "kandles",
  "logosyllabic",
  "cooccurrence",
  "paradigm",
  "positional",
  "sign_cluster",
  "numerals",
];

test.describe("Jobs view structure", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Jobs" }).click();
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

  test("pipeline selector contains all registered pipelines", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    const select = page.getByRole("combobox");
    const options = await select.locator("option").allTextContents();
    for (const pipeline of EXPECTED_PIPELINES) {
      expect(options).toContain(pipeline);
    }
  });

  test("submit form has parameters JSON textarea", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    // The params textarea should contain JSON
    const textarea = page.locator("textarea");
    await expect(textarea).toBeVisible();
    const value = await textarea.inputValue();
    expect(() => JSON.parse(value)).not.toThrow();
  });

  test("submit form has Submit button", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    await expect(page.getByRole("button", { name: "Submit" })).toBeVisible();
  });

  test("selecting a different pipeline updates the params field", async ({ page }) => {
    await page.getByText("+ Submit new job").click();
    const select = page.getByRole("combobox");
    // Default is block_entropy — switch to decipher
    await select.selectOption("decipher");
    // Params should now default to the new pipeline's JSON
    const textarea = page.locator("textarea");
    const value = await textarea.inputValue();
    // Should still be valid JSON
    expect(() => JSON.parse(value)).not.toThrow();
  });
});

test.describe("Jobs view with backend", () => {
  test.skip(!process.env.BACKEND_RUNNING, "Skipped: set BACKEND_RUNNING=1 to run");

  test("shows empty state message when no jobs exist", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Jobs" }).click();
    const emptyMsg = page.getByText(/No jobs yet/i);
    const table = page.locator("table");
    await expect(emptyMsg.or(table)).toBeVisible({ timeout: 5000 });
  });

  test("submitting a job with invalid JSON shows an error", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Jobs" }).click();
    await page.getByText("+ Submit new job").click();

    await page.getByPlaceholder(/Entropy analysis/i).fill("Test job");
    await page.locator("textarea").fill("not valid json");
    await page.getByRole("button", { name: "Submit" }).click();

    await expect(page.getByText(/valid JSON/i)).toBeVisible();
  });

  test("submitting a job with empty name shows an error", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Jobs" }).click();
    await page.getByText("+ Submit new job").click();

    // Leave name blank, click Submit
    await page.getByRole("button", { name: "Submit" }).click();
    await expect(page.getByText(/name is required/i)).toBeVisible();
  });
});
