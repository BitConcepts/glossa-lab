import { expect, test } from "@playwright/test";

/**
 * Backend insight/registry API tests (the file's original UI describes
 * exercised the Dashboard's AI Insight panel).
 *
 * Spec 081 step 5 (T017) retired the Dashboard as the home surface —
 * the AI narrative left the program home (D2.2) — so the Dashboard UI
 * describes were removed with the surface they tested. The API-level
 * describes below test backend endpoints that remain live and stay.
 * The new home surface is covered by e2e/program-home.spec.ts.
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
    test.setTimeout(90_000); // insight endpoint calls LLM — can take up to 60s
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");
    const resp = await request.post(`${BACKEND}/api/v1/dashboard/insight?days=14&limit=30`, { timeout: 75_000 });
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
    test.setTimeout(90_000);
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");
    // Get experiment registry for cross-check
    const expResp = await request.get(`${BACKEND}/api/v1/experiments`);
    const exps = await expResp.json();
    const validIds = new Set(exps.map((e: { id: string }) => e.id));
    const hexRe = /^[0-9a-f]{8,}$/i;

    const resp = await request.post(`${BACKEND}/api/v1/dashboard/insight?days=14&limit=30`, { timeout: 75_000 });
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
    test.setTimeout(90_000);
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");
    const expResp = await request.get(`${BACKEND}/api/v1/experiments`);
    const exps = await expResp.json();
    const validIds = new Set(exps.map((e: { id: string }) => e.id));

    const resp = await request.post(`${BACKEND}/api/v1/dashboard/insight?days=14&limit=30`, { timeout: 75_000 });
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

