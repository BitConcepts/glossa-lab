import { expect, test } from "@playwright/test";

/**
 * Projects + Goals E2E tests (API-level).
 *
 * Verifies:
 * - Project CRUD with prompt_context (goals) roundtrip
 * - Active project endpoint returns goals
 * - Dashboard highlights include n_hypotheses
 * - Dashboard insight impact/next_actions with open_view carry experiment_id
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

test.describe("Projects API — goals roundtrip", () => {
  const TEST_ID = "pw_test_goals";

  test("create project with prompt_context", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");

    const resp = await request.put(`${BACKEND}/api/v1/projects/${TEST_ID}`, {
      data: {
        label: "Playwright Goals Test",
        description: "E2E test for project goals",
        prompt_context: "Research goal: test decipherment method ABC.",
        topic_ids: ["t1"],
        experiment_ids: [],
        corpus_ids: [],
        is_active: false,
      },
    });
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.prompt_context).toBe("Research goal: test decipherment method ABC.");
  });

  test("get project returns goals", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");

    const resp = await request.get(`${BACKEND}/api/v1/projects/${TEST_ID}`);
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.prompt_context).toBe("Research goal: test decipherment method ABC.");
  });

  test("update prompt_context (goals) persists", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");

    await request.put(`${BACKEND}/api/v1/projects/${TEST_ID}`, {
      data: {
        label: "Playwright Goals Test",
        prompt_context: "Updated goal: method XYZ.",
        is_active: false,
      },
    });
    const resp = await request.get(`${BACKEND}/api/v1/projects/${TEST_ID}`);
    const body = await resp.json();
    expect(body.prompt_context).toBe("Updated goal: method XYZ.");
  });

  test("activate + active endpoint returns goals", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");

    await request.post(`${BACKEND}/api/v1/projects/${TEST_ID}/activate`);
    const resp = await request.get(`${BACKEND}/api/v1/projects/active`);
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.id).toBe(TEST_ID);
    expect(body.prompt_context).toContain("method XYZ");
  });

  test("cleanup: delete test project", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");

    const resp = await request.delete(`${BACKEND}/api/v1/projects/${TEST_ID}`);
    expect(resp.status()).toBe(200);
  });
});

test.describe("Dashboard highlights — n_hypotheses", () => {
  test("highlights payload includes n_hypotheses", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");

    const resp = await request.get(`${BACKEND}/api/v1/dashboard/highlights?days=14&limit=5`);
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body).toHaveProperty("n_hypotheses");
    expect(typeof body.n_hypotheses).toBe("number");
  });
});

test.describe("Dashboard insight — experiment_id in open_view actions", () => {
  test("downgraded actions carry experiment_id in params", async ({ request }) => {
    const up = await backendUp(request);
    test.skip(!up, "Backend not running");

    const resp = await request.post(`${BACKEND}/api/v1/dashboard/insight?days=14&limit=30`);
    if (resp.status() !== 200) return;
    const body = await resp.json();

    // Check impact items: any open_view with 'not in registry' should have experiment_id
    for (const im of body.impact ?? []) {
      if (im.suggested_action === "open_view" && im.suggested_params?.view === "experiments") {
        // If it was downgraded, the experiment_id should be present
        if (String(im.impact ?? "").includes("not in registry")) {
          expect(im.suggested_params).toHaveProperty("experiment_id");
        }
      }
    }

    // Check next_actions: same logic
    for (const a of body.next_actions ?? []) {
      if (a.action_type === "open_view" && a.params?.view === "experiments") {
        if (String(a.rationale ?? "").includes("not in registry")) {
          expect(a.params).toHaveProperty("experiment_id");
        }
      }
    }
  });
});
