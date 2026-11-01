/**
 * Shared Playwright fixtures (Spec 082, T010).
 *
 * The CI backend now enforces API-token auth (the GLOSSA_API_AUTH=off
 * accommodation is removed), so the suite authenticates the way the
 * ui-contract sanctions for tests: the token — provided through the
 * GLOSSA_API_TOKEN env var, matching the throwaway backend's — is
 * seeded into sessionStorage before any app code runs, and the
 * `request` fixture sends it as a Bearer header on API calls.
 *
 * When GLOSSA_API_TOKEN is unset (a local run against an auth-off
 * backend), both overrides are inert and behavior is unchanged.
 * Tests of the token contract itself (auth-token.spec.ts) use raw
 * browser contexts and never rely on this seeding.
 */
import { test as base, expect } from "@playwright/test";

const TOKEN = process.env.GLOSSA_API_TOKEN ?? "";

export const test = base.extend({
  context: async ({ browser }, use) => {
    const ctx = await browser.newContext();
    if (TOKEN) {
      await ctx.addInitScript((token: string) => {
        try {
          sessionStorage.setItem("glossa_api_token", token);
        } catch {
          /* storage unavailable — the app will ask for the token */
        }
      }, TOKEN);
    }
    await use(ctx);
    await ctx.close();
  },
  request: async ({ playwright }, use) => {
    const ctx = await playwright.request.newContext(
      TOKEN
        ? { extraHTTPHeaders: { Authorization: `Bearer ${TOKEN}` } }
        : undefined,
    );
    await use(ctx);
    await ctx.dispose();
  },
});

export { expect };
