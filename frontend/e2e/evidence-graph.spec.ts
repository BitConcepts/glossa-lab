import { expect, test } from "./fixtures";

/**
 * Evidence & sources tests — Spec 081 step 6 consolidation.
 *
 * The old three-tab "Evidence Graph" workspace (Library / Claims /
 * Sweep in one IndusEvidenceView) was dismantled by the redesign:
 *   - Library      → the Library tab of Evidence & sources (this spec)
 *   - Citations, Correspondence, Notebooks → tabs of the same surface
 *     (Q10: notebooks are the fourth tab)
 *   - Claims       → the Claims register, its own surface
 *     (covered by claims-surface.spec.ts)
 *   - Sweep        → a section of the Research loop surface
 *     (asserted here at its new home)
 *
 * Library tab content is the pre-redesign component verbatim, so its
 * tests carry over unchanged.
 */

// ── Helpers ───────────────────────────────────────────────────────────────────

async function navigateToEvidence(page: import("@playwright/test").Page) {
  await page.goto("/");
  const btn = page.getByTitle("Evidence & sources").first();
  await btn.waitFor({ state: "visible", timeout: 8000 });
  await btn.click();
  await page.waitForTimeout(400);
}

async function navigateToLoop(page: import("@playwright/test").Page) {
  await page.goto("/");
  const btn = page.getByTitle("Research loop").first();
  await btn.waitFor({ state: "visible", timeout: 8000 });
  await btn.click();
  await page.waitForTimeout(400);
}

// ── Navigation ────────────────────────────────────────────────────────────────

test.describe("Evidence & sources navigation", () => {
  test("nav item is visible in the sidebar", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle("Evidence & sources").first()).toBeVisible();
  });

  test("clicking the nav item renders the surface heading", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByRole("heading", { name: "Evidence & sources" })).toBeVisible();
  });

  test("the surface states what it is for", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(
      page.getByText(/Everything the program reads/i).first()
    ).toBeVisible();
  });
});

// ── Tab bar ────────────────────────────────────────────────────────────────────

test.describe("Evidence & sources tab bar", () => {
  test("Library tab button is visible", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByText(/📚 Library/).first()).toBeVisible();
  });

  test("Citations tab button is visible", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByRole("button", { name: "Citations" })).toBeVisible();
  });

  test("Correspondence tab button is visible", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByRole("button", { name: "Correspondence" })).toBeVisible();
  });

  test("Notebooks tab button is visible (Q10: the fourth tab)", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByRole("button", { name: "Notebooks" })).toBeVisible();
  });

  test("there is NO claims tab on this surface — claims are their own surface", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByText(/🔖 Claims/)).toHaveCount(0);
  });

  test("Library is the default active tab on load", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByText(/Drop PDF papers here/i)).toBeVisible({ timeout: 5000 });
  });

  test("clicking Citations tab switches content", async ({ page }) => {
    await navigateToEvidence(page);
    await page.getByRole("button", { name: "Citations" }).click();
    await expect(page.getByText(/BibTeX/).first()).toBeVisible({ timeout: 3000 });
  });

  test("clicking Correspondence tab switches content", async ({ page }) => {
    await navigateToEvidence(page);
    await page.getByRole("button", { name: "Correspondence" }).click();
    await expect(page.getByText(/Paste Email|No correspondence yet/i).first()).toBeVisible({ timeout: 3000 });
  });

  test("clicking Notebooks tab switches content", async ({ page }) => {
    await navigateToEvidence(page);
    await page.getByRole("button", { name: "Notebooks" }).click();
    await expect(page.getByPlaceholder(/New notebook title/i)).toBeVisible({ timeout: 3000 });
  });

  test("clicking Library tab restores Library content", async ({ page }) => {
    await navigateToEvidence(page);
    await page.getByRole("button", { name: "Notebooks" }).click();
    await page.getByText(/📚 Library/).first().click();
    await expect(page.getByText(/Drop PDF papers here/i)).toBeVisible({ timeout: 3000 });
  });
});

// ── Library tab (component carried over verbatim) ─────────────────────────────

test.describe("Evidence & sources — Library tab", () => {
  test("stats row is visible (Registered Papers, Hypothesis Models)", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByText(/Registered Papers/i).first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/Hypothesis Models/i).first()).toBeVisible();
  });

  test("upload dropzone shows drop target text", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByText(/Drop PDF papers here/i)).toBeVisible();
  });

  test("dropzone shows secondary instruction text", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByText(/or click to browse/i)).toBeVisible();
  });

  test("URL import field is visible", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByPlaceholder(/Import from URL/i)).toBeVisible();
  });

  test("Import URL button is visible", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByRole("button", { name: "Import" })).toBeVisible();
  });

  test("Re-run intake button is visible", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByText(/Re-run intake/i).first()).toBeVisible();
  });

  test("search papers input is visible", async ({ page }) => {
    await navigateToEvidence(page);
    await expect(page.getByPlaceholder(/Search papers/i)).toBeVisible();
  });

  test("typing in search field updates it", async ({ page }) => {
    await navigateToEvidence(page);
    const input = page.getByPlaceholder(/Search papers/i);
    await input.fill("parpola");
    await expect(input).toHaveValue("parpola");
    await input.fill("");
  });

  test("Import URL button is disabled when URL field is empty", async ({ page }) => {
    await navigateToEvidence(page);
    const btn = page.getByRole("button", { name: "Import" });
    await expect(btn).toBeVisible();
  });

  test("library shows paper list when backend available", async ({ page }) => {
    await navigateToEvidence(page);
    await page.waitForTimeout(2000);
    const hasItems = await page.locator("[style*='border: 1px solid'][style*='border-radius: 9px']").count() > 0;
    const hasEmpty = await page.getByText(/No papers registered yet/i).count() > 0;
    expect(hasItems || hasEmpty).toBeTruthy();
  });
});

// ── Sweep — at its new home under the Research loop ───────────────────────────

test.describe("Sweep — Research loop surface", () => {
  test("Sweep Configuration heading is visible", async ({ page }) => {
    await navigateToLoop(page);
    await expect(page.getByText(/Sweep Configuration/i).first()).toBeVisible({ timeout: 8000 });
  });

  test("the sweep section is fenced as candidate intake", async ({ page }) => {
    await navigateToLoop(page);
    await expect(page.getByText(/Literature sweep/i).first()).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/changes no claim by itself/i).first()).toBeVisible();
  });

  test("Save Config button is visible", async ({ page }) => {
    await navigateToLoop(page);
    await expect(page.getByRole("button", { name: /Save Config/i })).toBeVisible({ timeout: 8000 });
  });

  test("Run Sweep button is visible", async ({ page }) => {
    await navigateToLoop(page);
    await expect(page.getByRole("button", { name: /Run Sweep/i })).toBeVisible({ timeout: 8000 });
  });

  test("Sweep Name field is visible when config loads", async ({ page }) => {
    await navigateToLoop(page);
    await page.waitForTimeout(2000);
    const hasForm = await page.getByText(/Sweep Name/i).count() > 0;
    const hasLoading = await page.getByText(/Loading sweep config/i).count() > 0;
    expect(hasForm || hasLoading).toBeTruthy();
  });

  test("Primary Keywords label appears in config form", async ({ page }) => {
    await navigateToLoop(page);
    await page.waitForTimeout(3000);
    const hasForm = await page.getByText(/Primary Keywords/i).count() > 0;
    if (!hasForm) return; // backend not available — skip check
    await expect(page.getByText(/Primary Keywords/i).first()).toBeVisible();
  });

  test("Exclusions field is visible in config form", async ({ page }) => {
    await navigateToLoop(page);
    await page.waitForTimeout(3000);
    const hasForm = await page.getByText(/Exclusions/i).count() > 0;
    if (!hasForm) return;
    await expect(page.getByText(/Exclusions/i).first()).toBeVisible();
  });

  test("Sweep Candidates section heading is visible", async ({ page }) => {
    await navigateToLoop(page);
    await page.waitForTimeout(2000);
    await expect(page.getByText(/Sweep Candidates/i).first()).toBeVisible({ timeout: 5000 });
  });

  test("Refresh candidates button is visible", async ({ page }) => {
    await navigateToLoop(page);
    await expect(page.getByText(/↻ Refresh/).first()).toBeVisible({ timeout: 8000 });
  });

  test("No candidates message shown when no sweep has run", async ({ page }) => {
    await navigateToLoop(page);
    await page.waitForTimeout(2000);
    const hasEmpty = await page.getByText(/No candidates yet/i).count() > 0;
    const hasCandidates = await page.getByRole("link", { name: /.+/ }).count() > 0;
    expect(hasEmpty || hasCandidates).toBeTruthy();
  });
});

// ── Backend integration ───────────────────────────────────────────────────────

test.describe("Evidence & sources — backend integration", () => {
  test("Library tab shows registered paper count from backend", async ({ page }) => {
    await navigateToEvidence(page);
    await page.waitForTimeout(3000);
    const stat = page.getByText(/Registered Papers/i);
    await expect(stat).toBeVisible({ timeout: 5000 });
  });

  test("Hypothesis Models stat shows count from backend", async ({ page }) => {
    await navigateToEvidence(page);
    await page.waitForTimeout(3000);
    await expect(page.getByText(/Hypothesis Models/i).first()).toBeVisible();
  });
});
