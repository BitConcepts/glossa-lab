import { expect, test } from "@playwright/test";

/**
 * Program home + digestion board (Spec 081 steps 4–5, T016/T017;
 * wireframes 02 + 05).
 *
 * Home is the program's loop status, not a dashboard: verdict counts
 * from the claims register, the digestion queue with its doorway,
 * the /signs anchor totals (never the unexposed strict/pending
 * split), the canonical foundation status, and exactly one primary
 * action. The board's columns are acts owed; every card names its
 * missing act.
 */

test.describe("Program home (Spec 081)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("program-home")).toBeVisible({ timeout: 20_000 });
  });

  test("the four stat cards render from live endpoints", async ({ page }) => {
    await expect(page.getByText("claims in the register")).toBeVisible();
    await expect(page.getByText("claims waiting on a human")).toBeVisible();
    await expect(page.getByText("anchors recorded")).toBeVisible();
    await expect(page.getByText(/high-confidence/)).toBeVisible();
    await expect(
      page.getByText(/foundation check — the integrity gate/),
    ).toBeVisible();
  });

  test("no strict/pending anchor split is printed (D3)", async ({ page }) => {
    const home = page.getByTestId("program-home");
    await expect(home).not.toContainText("94 strict");
    await expect(home).not.toContainText("44 pending");
  });

  test("latest verdicts lead, with the what-this-does-not-show note", async ({
    page,
  }) => {
    await expect(page.getByText(/Latest verdicts/)).toBeVisible();
    await expect(
      page.getByText(/What this does not show: a verdict settles one claim/),
    ).toBeVisible();
  });

  test("the one primary action opens the claims surface", async ({ page }) => {
    await page.getByRole("button", { name: "+ Register a claim" }).click();
    await expect(page).toHaveURL(/#\/claims/);
  });

  test("the digestion doorway opens the board", async ({ page }) => {
    await page.getByRole("button", { name: "Open the digestion board →" }).click();
    await expect(page.getByTestId("digestion-board")).toBeVisible({
      timeout: 20_000,
    });
  });
});

test.describe("Digestion board (Spec 081)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/#/digestion");
    await expect(page.getByTestId("digestion-board")).toBeVisible({
      timeout: 20_000,
    });
  });

  test("columns are the acts owed", async ({ page }) => {
    await expect(page.getByText("Needs explanation")).toBeVisible();
    await expect(page.getByText("Needs acceptance")).toBeVisible();
    await expect(page.getByText("Ready to digest")).toBeVisible();
  });

  test("every waiting card names its missing act", async ({ page }) => {
    const board = page.getByTestId("digestion-board");
    await expect(board.getByText(/Missing:/).first()).toBeVisible({
      timeout: 20_000,
    });
    await expect(
      board.getByText(/an explanation record/).first(),
    ).toBeVisible();
  });

  test("the primary action is the longest-waiting claim", async ({ page }) => {
    const btn = page.getByRole("button", {
      name: "Start with the longest-waiting claim",
    });
    await expect(btn).toBeVisible();
    await expect(btn).toBeEnabled();
    await btn.click();
    await expect(page).toHaveURL(/#\/claims/);
  });

  test("the lede states the five stages and the named-act rule", async ({
    page,
  }) => {
    await expect(
      page.getByText(/only when a named person records the act/),
    ).toBeVisible();
  });
});
