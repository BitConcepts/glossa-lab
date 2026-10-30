import { createHash } from "node:crypto";
import { expect, test } from "@playwright/test";

/**
 * Spec 082 — the API-token contract, end to end (ui-contract.md).
 *
 * This spec deliberately imports the RAW Playwright test object, not
 * ./fixtures: the fixtures seed the token for the rest of the suite,
 * and these tests exist to prove what happens without that seeding.
 * Every test drives its own raw browser context.
 *
 * Requires: a backend with token auth ENFORCING and GLOSSA_API_TOKEN
 * set to its token (the CI frontend-tests job provides both). The
 * whole describe skips when the env var is absent.
 */

const TOKEN = process.env.GLOSSA_API_TOKEN ?? "";

test.describe("Spec 082 token contract", () => {
  test.skip(!TOKEN, "Skipped: GLOSSA_API_TOKEN not set — no enforcing backend under test");

  test("no token anywhere → the named 'API token needed' state", async ({ browser }) => {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto("/");
    await expect(page.getByText("API token needed")).toBeVisible({ timeout: 10000 });
    await ctx.close();
  });

  test("fragment intake: token read once, stored, fragment stripped", async ({ browser }) => {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto(`/#token=${TOKEN}`);
    // The app loads (no gate) once the token is in.
    await expect(page.getByText("API token needed")).toHaveCount(0, { timeout: 10000 });
    const stored = await page.evaluate(() => sessionStorage.getItem("glossa_api_token"));
    expect(stored).toBe(TOKEN);
    const hash = await page.evaluate(() => window.location.hash);
    expect(hash).not.toContain(TOKEN);
    expect(hash).not.toContain("token=");
    await ctx.close();
  });

  test("query-string tokens are refused by design", async ({ browser }) => {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto(`/?token=${TOKEN}#/status`);
    // The app never reads the query string for a token, so the
    // backend's 401s raise the named gate.
    await expect(page.getByText("API token needed")).toBeVisible({ timeout: 10000 });
    const stored = await page.evaluate(() => sessionStorage.getItem("glossa_api_token"));
    expect(stored).toBeNull();
    await ctx.close();
  });

  test("a wrong stored token is cleared on 401 and the gate returns", async ({ browser }) => {
    const ctx = await browser.newContext();
    await ctx.addInitScript(() => {
      try {
        sessionStorage.setItem("glossa_api_token", "wrong-token-value");
      } catch { /* */ }
    });
    const page = await ctx.newPage();
    await page.goto("/");
    await expect(page.getByText("API token needed")).toBeVisible({ timeout: 10000 });
    const stored = await page.evaluate(() => sessionStorage.getItem("glossa_api_token"));
    expect(stored).toBeNull();
    await ctx.close();
  });

  test("pasting the token into the gate field lets the app in", async ({ browser }) => {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto("/");
    await expect(page.getByText("API token needed")).toBeVisible({ timeout: 10000 });
    await page.getByLabel("API token").fill(TOKEN);
    await page.getByRole("button", { name: "Save token" }).click();
    await expect(page.getByText("API token needed")).toHaveCount(0, { timeout: 10000 });
    await ctx.close();
  });

  test("Settings shows present + SHA-256 fingerprint, never the value", async ({ browser }) => {
    const ctx = await browser.newContext();
    await ctx.addInitScript((token: string) => {
      try {
        sessionStorage.setItem("glossa_api_token", token);
      } catch { /* */ }
    }, TOKEN);
    const page = await ctx.newPage();
    await page.goto("/");
    await page.getByRole("button", { name: "Settings" }).click();
    // The API token row is the first service row; open its Manage area.
    await page.getByRole("button", { name: "Manage", exact: true }).first().click();
    const fingerprint = createHash("sha256").update(TOKEN).digest("hex").slice(0, 8);
    await expect(page.getByText(/Token present — fingerprint/)).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(fingerprint, { exact: false })).toBeVisible();
    const html = await page.content();
    expect(html).not.toContain(TOKEN);
    await ctx.close();
  });
test("routed fragment: #/status#token= lands on Status, token stored, route kept", async ({ browser }) => {
    // The tray's "View status & session log" door (Spec 081 step 8;
    // ui-contract step-8 addendum).
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto(`/#/status#token=${TOKEN}`);
    await expect(page.getByRole("heading", { name: "Status" })).toBeVisible({ timeout: 10000 });
    await expect(page.getByText("API token needed")).toHaveCount(0);
    expect(await page.evaluate(() => sessionStorage.getItem("glossa_api_token"))).toBe(TOKEN);
    const hash = await page.evaluate(() => window.location.hash);
    expect(hash).toBe("#/status");
    expect(hash).not.toContain(TOKEN);
    await ctx.close();
  });
});
