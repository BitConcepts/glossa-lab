import { test, expect } from "./fixtures";

// Spec 086 Stage 5 (T503/T504): the System graph surface renders
// the published, gate-verified map artifact — the header contract
// (Q3), the standing position, and the five screens' drill-downs.
test.describe("System graph — the layered map (Spec 086)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/#/system-graph");
    await expect(page.getByTestId("indus-map-header")).toBeVisible();
  });

  test("system view renders the gated header, stamp and standing position", async ({ page }) => {
    await expect(page.getByText("950 claims in the ledger")).toBeVisible();
    await expect(page.getByText("32.8% of anchor signs validated (strict)")).toBeVisible();
    await expect(page.getByTestId("indus-map-stamp")).toContainText("fresh");
    await expect(page.getByTestId("indus-map-standing-position")).toContainText(
      "the Indus script is not deciphered",
    );
    await expect(page.getByRole("heading", { name: "Sign inventory & validation" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Matrix coverage" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Unresolved sign mentions" })).toBeVisible();
  });

  test("claim and evidence drill-downs render the specimen claim", async ({ page }) => {
    await page.getByRole("button", { name: "Open the claim view →" }).click();
    await expect(
      page.getByText(
        "The fish sign (meen in Dravidian) is the primary rebus sign in the Indus script.",
      ),
    ).toBeVisible();
    await expect(page.getByText("Displayed score")).toBeVisible();
    await expect(page.getByText("No AEE state is recorded on this claim")).toBeVisible();
    await page.getByRole("button", { name: "Evidence view →" }).click();
    await expect(page.getByText("What bears on this claim")).toBeVisible();
    await expect(
      page.getByText("Two layers name the same signs differently"),
    ).toBeVisible();
  });

  test("matrix and settling tabs render the computed layers", async ({ page }) => {
    await page.getByRole("button", { name: "Matrix", exact: true }).click();
    await expect(
      page.getByText("Claims × evidence — the generated matrix"),
    ).toBeVisible();
    await page.getByRole("button", { name: "Settling", exact: true }).click();
    await expect(
      page.getByText("Settling — what the recorded assignments imply"),
    ).toBeVisible();
    await expect(page.getByText("UNMEASURED")).toBeVisible();
    await expect(page.getByText("Stored runs of record (T405)")).toBeVisible();
  });
});
