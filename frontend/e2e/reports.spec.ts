import { test, expect } from "./fixtures";

/**
 * Reports & ledger — Spec 081 wireframe 12 (PR-R).
 *
 * The surface is the program's outputs plus its record: a reports
 * list (title / state / meta / Open), the spec-study register with
 * verbatim outcome headlines, the program-items list (records that
 * are not spec directories), and a Ledger tab that states the
 * ledger's append-only terms. The retired file-browser UI (compose
 * mode, AI synthesis, star pins, template editor, area tabs) must
 * not reappear.
 */

async function navigateToReports(page: import("@playwright/test").Page) {
  await page.goto("/");
  const nav = page.getByTitle("Reports & ledger").first();
  await nav.waitFor({ state: "visible", timeout: 8000 });
  await nav.click();
  await expect(
    page.getByRole("heading", { name: "Reports & ledger" }),
  ).toBeVisible();
}

test.describe("Reports & ledger surface", () => {
  test("heading and lede carry the append-only terms", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByText(/append-only/)).toBeVisible();
    await expect(page.getByText(/No ledger entry, no claim/)).toBeVisible();
  });

  test("Generate report is the primary action and opens the dialog", async ({ page }) => {
    await navigateToReports(page);
    await page.getByRole("button", { name: /\+ Generate report/ }).click();
    await expect(page.getByText("Built-in templates", { exact: true })).toBeVisible();
  });

  test("Reports and Ledger tabs are present; Ledger states where the record lives", async ({ page }) => {
    await navigateToReports(page);
    await page.getByRole("button", { name: "Ledger", exact: true }).click();
    await expect(page.getByText(/LEDGER\.md/)).toBeVisible();
    await expect(page.getByText(/no ledger endpoint/)).toBeVisible();
  });

  test("retired file-browser UI is absent", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByRole("button", { name: /Compose/i })).toHaveCount(0);
    await expect(page.getByRole("button", { name: /AI Report/i })).toHaveCount(0);
    await expect(page.getByText(/Data & Docs/)).toHaveCount(0);
  });

  test("reports list shows its empty state or rows", async ({ page }) => {
    await navigateToReports(page);
    const empty = page.getByTestId("reports-empty-state");
    const open = page.getByRole("button", { name: "Open", exact: true }).first();
    await expect(empty.or(open)).toBeVisible({ timeout: 8000 });
  });
});

test.describe("Study register (build-tree backend)", () => {
  test("register renders entries with outcome headlines", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByText("Study register")).toBeVisible();
    await expect(page.getByText(/\d+ register entries/).first()).toBeVisible({ timeout: 10000 });
    // A study with no outcome record is labelled as such, never as executed.
    await expect(page.getByText(/No outcome recorded/).first()).toBeVisible();
  });

  test("restricted entry renders name-only", async ({ page }) => {
    await navigateToReports(page);
    await expect(page.getByText(/Name-only record/)).toBeVisible({ timeout: 10000 });
  });

  test("program items carry their records' verdicts at full prominence", async ({ page }) => {
    await navigateToReports(page);
    await expect(
      page.getByText("Program items — records outside the spec register"),
    ).toBeVisible();
    await expect(page.getByText(/FAILED — KI-2 TRIGGERED/)).toBeVisible();
    await expect(page.getByText(/0 of 184/)).toBeVisible();
  });
});
