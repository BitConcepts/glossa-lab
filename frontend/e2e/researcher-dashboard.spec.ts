import { expect, test } from "./fixtures";

/**
 * Researcher dashboard (Spec 095 T403, built to the approved
 * wireframes). The home states the gate-verified census of record
 * and what the program does not claim; each of the six features
 * reads the records themselves. These specs hold the surface's
 * refusals: the falsifier-less claims are findable as a class of
 * exactly the recorded size, the contribution form cannot submit
 * without a falsifier, an unavailable corpus serves nothing, and
 * no translation is presented anywhere.
 */

test.describe("Researcher dashboard (Spec 095 T403)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/#/researcher-dashboard");
    await expect(page.getByTestId("researcher-dashboard")).toBeVisible({
      timeout: 20_000,
    });
    await expect(page.getByTestId("dashboard-home")).toBeVisible({
      timeout: 20_000,
    });
  });

  test("home states the census of record and the does-not-claim panel", async ({
    page,
  }) => {
    await expect(page.getByTestId("census-claims")).toHaveText("1,009");
    await expect(page.getByText("claims in the ledger")).toBeVisible();
    await expect(page.getByText("recorded anchor signs")).toBeVisible();
    await expect(
      page.getByText("What this program does not claim"),
    ).toBeVisible();
    await expect(
      page.getByText(/The Indus script is not deciphered/),
    ).toBeVisible();
    // The six strongest readings are stated with their outcome.
    await expect(page.getByText("NOT IDENTIFIABLE").first()).toBeVisible();
    await expect(page.getByText(/M044/)).toBeVisible();
  });

  test("program status names blocked items and landing records", async ({
    page,
  }) => {
    await page.getByTestId("section-status").click();
    await expect(page.getByTestId("dashboard-status")).toBeVisible();
    await expect(
      page.getByText("Blocked items, with their blockers"),
    ).toBeVisible();
    await expect(page.getByText(/GR-088-01/)).toBeVisible();
  });

  test("inscription explorer lists the canonical corpus and layers a record", async ({
    page,
  }) => {
    await page.getByTestId("section-inscriptions").click();
    await expect(page.getByTestId("dashboard-inscriptions")).toBeVisible();
    await expect(page.getByText(/15,508 inscriptions/)).toBeVisible({
      timeout: 20_000,
    });
    // A failed-identity corpus is listed unavailable, never as data.
    await expect(page.getByText("unavailable").first()).toBeVisible();
    await page.getByText("GLI-IND-0000206").click();
    await expect(page.getByText("Observation", { exact: true })).toBeVisible();
    await expect(page.getByText("Transcription", { exact: true })).toBeVisible();
    await expect(page.getByText("Hypothesis", { exact: true })).toBeVisible();
    // Selecting a sign position shows only that sign's statements.
    await page.getByTestId("sign-pos-1").click();
    await expect(page.getByText(/Position 2: sign 145/)).toBeVisible();
  });

  test("hypothesis comparison presents no translation", async ({ page }) => {
    await page.getByTestId("section-hypotheses").click();
    await expect(page.getByTestId("dashboard-hypotheses")).toBeVisible();
    await expect(
      page.getByText(/The program holds no translation of any inscription/),
    ).toBeVisible();
    await expect(
      page.getByText("The nonlinguistic position"),
    ).toBeVisible();
    await expect(
      page.getByText("Rival readings, sign by sign"),
    ).toBeVisible();
  });

  test("the falsifier-less claims are findable as a class of nine", async ({
    page,
  }) => {
    await page.getByTestId("section-evidence").click();
    await expect(page.getByTestId("dashboard-evidence")).toBeVisible();
    await page.getByTestId("claim-falsifier").selectOption("absent");
    await expect(page.getByText("9 claims match")).toBeVisible({
      timeout: 20_000,
    });
    await expect(
      page.getByText("no falsifier — the gap").first(),
    ).toBeVisible();
    // Opening one of the nine shows its detail with the lineage
    // layer and the falsifier stated as absent, not worked around.
    await page
      .getByText("Sign value: 900 / number six")
      .first()
      .click();
    await expect(page.getByTestId("claim-detail")).toBeVisible({
      timeout: 20_000,
    });
    await expect(
      page.getByText(/Lineage — claim, evidence, derivation, source/),
    ).toBeVisible();
    await expect(
      page.getByText(/none recorded — this claim is in the falsifier-less class/),
    ).toBeVisible();
  });

  test("reproduction lists incomplete runs as not reproducible, missing pieces named", async ({
    page,
  }) => {
    await page.getByTestId("section-reproduction").click();
    await expect(page.getByTestId("dashboard-reproduction")).toBeVisible();
    await expect(
      page.getByText("not reproducible").first(),
    ).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText(/missing: command/).first()).toBeVisible();
  });

  test("the contribution form cannot submit without a falsifier", async ({
    page,
  }) => {
    await page.getByTestId("section-contribute").click();
    await expect(page.getByTestId("dashboard-contribute")).toBeVisible();
    await expect(
      page.getByText(/no automatic promotion anywhere in this system/),
    ).toBeVisible();
    await page.getByTestId("contrib-statement").fill("M044 carries the value ku.");
    await page.getByTestId("contrib-refs").fill("M044");
    await page.getByTestId("contrib-submitter").fill("E2E Researcher");
    await page.getByRole("button", { name: "Submit to the staging queue" }).click();
    await expect(page.getByTestId("contrib-error")).toContainText(
      "cannot submit without a falsifier",
    );
  });
});
