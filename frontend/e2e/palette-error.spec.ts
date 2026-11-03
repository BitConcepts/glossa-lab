import { expect, test } from "./fixtures";

/**
 * Spec 087 S1 (T104, claim C087-3): a failed Experiment Builder catalog
 * load renders a named error state in the palette, with retry — never a
 * silently empty palette.
 *
 * The catalog endpoint is intercepted per-test, so these run regardless
 * of backend state:
 *   1. catalog 500s -> the palette error state is visible and names the
 *      failure; no node categories render.
 *   2. catalog 500s once, then succeeds -> clicking Retry loads the
 *      palette and the error state clears.
 */

const CATALOG_ROUTE = "**/api/v1/experiment-graphs/catalog";

const PROBE_NODE = {
  id: "RetryProbeNode",
  name: "Retry Probe Node",
  category: "Test Category",
  description: "Catalog probe node for the palette retry test.",
  inputs: [],
  outputs: [{ name: "report", type: "object" }],
  params_schema: { type: "object", properties: {} },
};

async function navigateToExpBuilder(page: import("@playwright/test").Page) {
  await page.goto("/");
  const btn = page.getByTitle("Experiments").first();
  await btn.waitFor({ state: "visible", timeout: 8000 });
  await btn.click();
  await expect(page.getByText(/Experiment Builder/i).first()).toBeVisible();
}

test.describe("Experiment Builder palette failure (Spec 087 S1)", () => {
  test("failed catalog load shows a named error state, not an empty palette", async ({ page }) => {
    await page.route(CATALOG_ROUTE, (route) =>
      route.fulfill({ status: 500, contentType: "text/plain", body: "seeded catalog failure" }),
    );
    await navigateToExpBuilder(page);
    const alert = page.getByTestId("palette-error");
    await expect(alert).toBeVisible();
    await expect(alert).toContainText("Node palette failed to load");
    // The palette must not present the failure as "no nodes exist":
    // no category listing renders behind the error.
    await expect(page.getByText("Indus Decipherment", { exact: true })).toHaveCount(0);
  });

  test("retry after a failed load populates the palette and clears the error", async ({ page }) => {
    let calls = 0;
    await page.route(CATALOG_ROUTE, (route) => {
      calls += 1;
      if (calls === 1) {
        return route.fulfill({ status: 500, contentType: "text/plain", body: "seeded catalog failure" });
      }
      return route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([PROBE_NODE]),
      });
    });
    await navigateToExpBuilder(page);
    const alert = page.getByTestId("palette-error");
    await expect(alert).toBeVisible();
    await alert.getByRole("button", { name: "Retry" }).click();
    await expect(page.getByText("Retry Probe Node")).toBeVisible();
    await expect(page.getByText("Test Category")).toBeVisible();
    await expect(alert).toHaveCount(0);
  });
});
