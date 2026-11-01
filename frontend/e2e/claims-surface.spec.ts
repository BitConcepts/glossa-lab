import { expect, test } from "./fixtures";

/**
 * Claims surface (Spec 081 step 3, T015; wireframes 03–04; FR-018).
 *
 * The register is program-scoped and keeps the two kinds of standing
 * in separate columns — the machine verdict (lane 1) and the human
 * settlement stage (lane 2). Hypotheses fold into the register as
 * early-state entries (Q7). The detail keeps the falsifier first and
 * the two lanes apart. Live-data style, like the program-home spec:
 * assertions are structural, not pinned to one claim's text.
 */

test.describe("Claims register (Spec 081 step 3)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/#/claims");
    await expect(page.getByTestId("claims-surface")).toBeVisible({
      timeout: 20_000,
    });
    await expect(page.getByTestId("claim-row").first()).toBeVisible({
      timeout: 20_000,
    });
  });

  test("the register separates verdict from digestion", async ({ page }) => {
    await expect(
      page.getByText("Falsifier — what would prove it wrong"),
    ).toBeVisible();
    await expect(page.getByText("Verdict (machine checks)")).toBeVisible();
    await expect(
      page.getByText("Digestion (human settlement)"),
    ).toBeVisible();
  });

  test("every row carries a verdict chip and a stage chip", async ({
    page,
  }) => {
    const row = page.getByTestId("claim-row").first();
    await expect(row).toContainText(/Supported|Not supported|Insufficient evidence|Inconclusive|Contradicted|Awaiting expert|Cannot be administered/);
    await expect(row).toContainText(/created|checked|explained|accepted|digested/i);
  });

  test("search narrows the register and states an empty match plainly", async ({
    page,
  }) => {
    const box = page.getByLabel("Search claims");
    await box.fill("zzz-no-such-claim-zzz");
    await expect(page.getByText("No claims match this filter.")).toBeVisible();
    await box.fill("");
    await expect(page.getByTestId("claim-row").first()).toBeVisible();
  });

  test("hypotheses fold in as early-state entries (Q7)", async ({ page }) => {
    const h = page.getByTestId("hypothesis-row").first();
    await expect(h).toBeVisible({ timeout: 20_000 });
    await expect(h).toContainText("No verdict yet");
    await expect(h).toContainText("Not yet sharp");
  });

  test("the register-a-claim doorway states how claims enter", async ({
    page,
  }) => {
    await page
      .getByRole("button", { name: "+ Register a claim" })
      .click();
    await expect(
      page.getByText("How a claim enters this register"),
    ).toBeVisible();
    await expect(
      page.getByText(/Claims are never typed in directly/),
    ).toBeVisible();
  });
});

test.describe("Claim detail (Spec 081 step 3)", () => {
  test("opens from a row with the falsifier first and the lanes apart", async ({
    page,
  }) => {
    await page.goto("/#/claims");
    await expect(page.getByTestId("claim-row").first()).toBeVisible({
      timeout: 20_000,
    });
    await page.getByTestId("claim-row").first().click();
    const detail = page.getByTestId("claim-detail");
    await expect(detail).toBeVisible({ timeout: 20_000 });
    await expect(detail.getByText("Falsifier", { exact: true })).toBeVisible();
    await expect(page.getByTestId("lane1-region")).toBeVisible();
    await expect(page.getByTestId("lane2-region")).toBeVisible();
    await expect(
      page.getByText(/Lane 1 — machine-speed verification/),
    ).toBeVisible();
    await expect(
      page.getByText(/Lane 2 — human-paced settlement/),
    ).toBeVisible();
    await page.getByRole("button", { name: "← All claims" }).click();
    await expect(page.getByTestId("claims-surface")).toBeVisible();
  });

  test("the digestion doorway deep link opens the claim (session key)", async ({
    page,
  }) => {
    await page.goto("/#/claims");
    const row = page.getByTestId("claim-row").first();
    await expect(row).toBeVisible({ timeout: 20_000 });
    const meta = await row.locator("div").nth(1).textContent();
    const claimId = (meta ?? "").split("·")[0]?.trim();
    expect(claimId).toBeTruthy();
    await page.evaluate(
      (id) => sessionStorage.setItem("glossa_open_claim", id),
      claimId,
    );
    await page.reload();
    await expect(page.getByTestId("claim-detail")).toBeVisible({
      timeout: 20_000,
    });
    await expect(page.getByTestId("claim-detail")).toContainText(claimId!);
  });
});
