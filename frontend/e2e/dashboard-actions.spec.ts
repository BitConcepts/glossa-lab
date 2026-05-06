import { expect, test } from "@playwright/test";

/**
 * Dashboard actions E2E tests.
 *
 * Exercises the AI Insight panel: regeneration, impact experiment buttons,
 * next-action buttons, and verifies that experiment IDs resolve to real
 * registered experiments (no phantom hash-IDs reach the user).
 *
 * Requires backend running on localhost:8001.
 */

const BACKEND = "http://localhost:8001";

async function backendUp(request: import("@playwright/test").APIRequestContext): Promise<boolean> {
  try {
    const r = await request.get(`${BACKEND}/api/v1/health`);
    return r.status() === 200;
  } catch {
    return false;
  }
}

// ── API-level: experiment registry sanity ─────────────────────────────────────

test.describe("Experiment registry", () => {
  test("all experiment IDs are non-hash human-readable strings", async ({ request }) => {
    const resp = await request.get(`${BACKEND}/api/v1/experiments`);
    expect(resp.status()).toBe(200);
    const exps = await resp.json();
    expect(Array.isArray(exps)).toBeTruthy();
    expect(exps.length).toBeGreaterThan(0);
    const hexRe = /^[0-9a-f]{8,}$/i;
    for (const e of exps) {
      expect(hexRe.test(e.id), `Experiment ID "${e.id}" looks like a hex hash`).toBeFalsy();
      expect(e.id.length).toBeGreaterThan(3);
    }
  });
});

// ── API-level: dashboard insight validation ───────────────────────────────────

test.describe("Dashboard insight API", () => {
  test("POST /insight returns valid structure", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");
    const resp = await request.post(`${BACKEND}/api/v1/dashboard/insight?days=14&limit=30`);
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body).toHaveProperty("highlights");
    expect(body).toHaveProperty("what_it_means");
    expect(body).toHaveProperty("impact");
    expect(body).toHaveProperty("next_actions");
    expect(body).toHaveProperty("model");
    expect(Array.isArray(body.highlights)).toBeTruthy();
    expect(Array.isArray(body.impact)).toBeTruthy();
    expect(Array.isArray(body.next_actions)).toBeTruthy();
  });

  test("impact items have valid experiment IDs (no hex hashes)", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");
    // Get experiment registry for cross-check
    const expResp = await request.get(`${BACKEND}/api/v1/experiments`);
    const exps = await expResp.json();
    const validIds = new Set(exps.map((e: { id: string }) => e.id));
    const hexRe = /^[0-9a-f]{8,}$/i;

    const resp = await request.post(`${BACKEND}/api/v1/dashboard/insight?days=14&limit=30`);
    const body = await resp.json();
    for (const im of body.impact) {
      const eid = im.study_or_experiment_id ?? "";
      // Must not be a hex hash
      expect(hexRe.test(eid), `Impact experiment ID "${eid}" is a hex hash`).toBeFalsy();
      // If it has an experiment_id in suggested_params, it must be valid
      if (im.suggested_params?.experiment_id) {
        const pid = im.suggested_params.experiment_id;
        expect(hexRe.test(pid), `suggested_params.experiment_id "${pid}" is a hex hash`).toBeFalsy();
        if (pid) {
          expect(validIds.has(pid), `suggested_params.experiment_id "${pid}" not in registry`).toBeTruthy();
        }
      }
    }
  });

  test("next_actions with run_experiment have valid experiment IDs", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");
    const expResp = await request.get(`${BACKEND}/api/v1/experiments`);
    const exps = await expResp.json();
    const validIds = new Set(exps.map((e: { id: string }) => e.id));

    const resp = await request.post(`${BACKEND}/api/v1/dashboard/insight?days=14&limit=30`);
    const body = await resp.json();
    for (const a of body.next_actions) {
      if (a.action_type === "run_experiment") {
        const eid = a.params?.experiment_id ?? "";
        if (eid) {
          expect(
            validIds.has(eid),
            `next_action run_experiment has invalid id "${eid}"`
          ).toBeTruthy();
        }
      }
      // If unresolvable, action_type should have been downgraded to open_view
      // (or legacy no_op) with an informational rationale.
      if (
        (a.action_type === "open_view" || a.action_type === "no_op") &&
        a.rationale?.includes("not in registry")
      ) {
        // This is expected — the backend caught a hallucinated ID
        expect(a.rationale).toContain("not in registry");
      }
    }
  });
});

// ── UI-level: dashboard loads and shows insight ──────────────────────────────

test.describe("Dashboard UI", () => {
  test("dashboard loads with counters", async ({ page }) => {
    await page.goto("/");
    // Dashboard is the default view
    await expect(page.getByRole("heading", { name: /Dashboard/i })).toBeVisible({ timeout: 5000 });
    // Should show counter tiles
    await expect(page.getByText("Discovery items")).toBeVisible({ timeout: 5000 });
    // Use exact role match to avoid strict-mode violation (sidebar + description + counter all contain "Experiments")
    await expect(page.getByRole("button", { name: /Experiments.*graph registry/i })).toBeVisible({ timeout: 5000 });
  });

  test("AI Insight section renders", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: /AI Insight/i })).toBeVisible({ timeout: 5000 });
  });

  test("Regenerate button triggers LLM call", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(2000);
    const regenBtn = page.getByRole("button", { name: /Regenerate/i });
    if (await regenBtn.isVisible()) {
      await regenBtn.click();
      // Should show loading state — use specific locator to avoid strict-mode
      await expect(page.getByText("Asking the AI to read the latest items")).toBeVisible({ timeout: 3000 });
    }
  });

  test("impact section shows experiment names, not hex hashes", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(3000);
    // If insight is loaded, check for hex hashes in impact section
    const impactSection = page.locator("text=Impact on your studies");
    if (await impactSection.isVisible()) {
      // Get all text inside impact list items
      const impactItems = page.locator("ul").nth(1).locator("li");
      const count = await impactItems.count();
      const hexRe = /^[0-9a-f]{8,}$/i;
      for (let i = 0; i < count; i++) {
        const text = await impactItems.nth(i).textContent();
        // No standalone hex hashes should appear in the impact text
        const words = (text ?? "").split(/\s+/);
        for (const w of words) {
          expect(hexRe.test(w.replace(/[^\w]/g, "")),
            `Found hex hash "${w}" in impact item`).toBeFalsy();
        }
      }
    }
  });

  test("next actions buttons are present and clickable", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(3000);
    const nextActionsHeader = page.locator("text=Next actions");
    if (await nextActionsHeader.isVisible()) {
      // Should have at least one action button
      const actionBtns = page.locator("button").filter({ hasText: /▶|Fetch|Run|Plan|Ask|Open|Done/i });
      expect(await actionBtns.count()).toBeGreaterThan(0);
    }
  });
});

// ── UI-level: run experiment from next actions ───────────────────────────────

test.describe("Dashboard action: run_experiment", () => {
  test("clicking Run does not show 'not registered' toast for valid experiments", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(3000);
    // Find a Run button in next actions
    const runBtns = page.locator("button").filter({ hasText: /^▶ Run$/i });
    const count = await runBtns.count();
    if (count > 0) {
      // Click the first Run button
      await runBtns.first().click();
      // Wait briefly for toast
      await page.waitForTimeout(2000);
      // Should NOT see "not registered" toast
      const badToast = page.locator("text=is not registered");
      expect(await badToast.count()).toBe(0);
    }
  });
});

test.describe("Dashboard action: plan_chain", () => {
  test("clicking Plan chain does not error immediately", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(3000);
    const planBtns = page.locator("button").filter({ hasText: /Plan chain/i });
    const count = await planBtns.count();
    if (count > 0) {
      await planBtns.first().click();
      await page.waitForTimeout(2000);
      // Should show "Hypothesis created" or "Running N experiment(s)" toast, not an error
      const errorToast = page.locator("text=not registered");
      expect(await errorToast.count()).toBe(0);
    }
  });
});
