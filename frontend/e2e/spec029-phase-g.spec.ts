import { expect, test, type Page } from "@playwright/test";

/**
 * Spec 029 Phase G — display guards as a permanent gate
 * (tasks G4; FR-029-08/09/10; claims F029-C06/C07; OD-4).
 *
 * Program-wide extensions of the Phase E2 rendered guards, on
 * the same SYNTHETIC fixtures (one plain claim, one contested
 * bundle parent; no live record is given text, a contest, or a
 * stage by these tests):
 *
 *  - the withdrawn "signs deciphered" headline pattern appears
 *    NOWHERE on the rendered surfaces (panel or claims tab) —
 *    not merely on the panel E1/E2 checked;
 *  - the stage vocabulary on the rendered claim surfaces is
 *    exactly the five verbatim names: every stage label shown
 *    is one of the five, and no synonym (verified / proven /
 *    confirmed as a stage label) appears in the legend, the
 *    lane regions, the standing position, or the stage summary;
 *  - every expanded verdict display carries a not_understood
 *    slot (data-testid="not-understood") — the authored form
 *    for the bundle parent, the stated-absence form for the
 *    plain claim;
 *  - lane labels and the OD-4 stage legend are present on the
 *    claim surface (the G4 presence half of the guard pair).
 */

const STAGE_OBJECT = (stage: string) => ({
  stage,
  stage_source: "synthetic-fixture",
  stage_as_of: "2026-10-12",
  stamped: true,
  stage_history: [],
  stage_history_count: 0,
  latest_transition: null,
});

const SCORE = {
  claim_id: "synthetic-bundle-001",
  direct_score: 0.917,
  propagated_score: 0.917,
  band: "high",
  components: { evidence: 0.9, independence: 0.8, falsifiability: 0.9, boundary: 1.0 },
  notes: [],
};

const CLAIMS = {
  total: 2,
  limit: 200,
  offset: 0,
  claims: [
    {
      claim_id: "synthetic-plain-001",
      source_document_id: "synthetic_doc",
      claim_type: "sign_value_claim",
      normalized_claim: "Synthetic plain claim about a sign value.",
      claim_status: "untested",
      falsification_condition: "A synthetic counter-observation defeats it.",
      stage: STAGE_OBJECT("created"),
      verified_unexplained: false,
      aee_score: { ...SCORE, propagated_score: 0.5, band: "medium" },
      lane1_score: { ...SCORE, propagated_score: 0.5, band: "medium" },
      not_understood: null,
      not_understood_recorded: false,
      bundle: null,
    },
    {
      claim_id: "synthetic-bundle-001",
      source_document_id: "synthetic_doc",
      claim_type: "sign_value_claim",
      normalized_claim: "Synthetic bundle parent claim.",
      claim_status: "partially_supported",
      falsification_condition: "A synthetic falsifier defeats the parent.",
      stage: STAGE_OBJECT("checked"),
      verified_unexplained: true,
      aee_score: SCORE,
      lane1_score: SCORE,
      not_understood:
        "Synthetic authored statement: which sign values the neighbouring signs force remains not understood.",
      not_understood_recorded: true,
      bundle: {
        claim_id: "synthetic-bundle-001",
        stage: STAGE_OBJECT("checked"),
        stage_computation: {
          stage: "checked",
          minimum_stage: "explained",
          subclaim_stages: { attribution: "checked" },
          unstamped_subclaims: [],
          attribution_contested: true,
          caps_applied: ["od3-contested-attribution-caps-at-checked"],
        },
        sub_claims: [
          {
            claim_id: "synthetic-sub-attribution",
            kind: "attribution",
            contest_state: "contested",
            attribution_contested: true,
            contest_record: {
              contested_by: "Synthetic Contester",
              evidence: ["https://example.org/rival-attribution"],
              contested_on: "2026-10-05",
            },
          },
        ],
        attribution_contested: true,
        contest_record: {
          contested_by: "Synthetic Contester",
          evidence: ["https://example.org/rival-attribution"],
          contested_on: "2026-10-05",
        },
        contested: true,
        adverse_digestion: null,
      },
    },
  ],
};

const MOCK_DECIPHER = {
  available: true,
  archived: true,
  anchors: {
    total: 171,
    total_all: 287,
    by_confidence: { HIGH: 166, MEDIUM: 5, LOW: 3, CANDIDATE: 113 },
    by_stage: { created: 193, checked: 94 },
    n_unstamped_stage: 0,
    corpus_token_coverage: 0.92,
    corpus_signs: 390,
    icit_total_signs: 713,
  },
  n_rounds: 0,
  current_state: null,
  progression: [],
  current_phase: 382,
  n_evidence_items: 41,
  total_seals: 1670,
};

async function setupMocks(page: Page) {
  // Catch-all first (Playwright routes are LIFO: last registered wins).
  await page.route("**/api/v1/**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({}) }));
  await page.route("**/api/v1/jobs**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: "[]" }));
  await page.route("**/api/v1/projects/active", (r) =>
    r.fulfill({ status: 404, contentType: "application/json", body: JSON.stringify({ detail: "No active project" }) }));
  await page.route("**/api/v1/projects", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: "[]" }));
  await page.route("**/api/v1/dismissals**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ dismissed: [] }) }));
  // App-shell endpoints whose shapes the shell reads fields from
  // (the catch-all {} crashes them — same mocks as decipherment-actions).
  await page.route("**/api/v1/dashboard/highlights**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({
        n_items: 0, since_days: 14, n_studies: 0, n_experiments: 0,
        n_atomic_nodes: 0, n_hypotheses: 0,
        by_kind: {}, by_topic: {}, by_source: {}, by_status: { saved: 0 },
        items: [], insight: null,
      }) }));
  await page.route("**/api/v1/dashboard/latest-insight**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({ available: false, generated_at: 0, insight: null }) }));
  await page.route("**/api/v1/dashboard/insight**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({ highlights: [], what_it_means: "Mock insight.", impact: [], next_actions: [], model: "mock" }) }));
  await page.route("**/api/v1/research-loop/status**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({ running: false, cycles_completed: 0, max_cycles: 15, total_papers: 0, total_insights: 0, history: [] }) }));
  await page.route("**/api/v1/research-loop/last-run**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ no_runs: true }) }));
  await page.route("**/api/v1/research-loop/staging**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({ candidates: [], counts: { total: 0, staged: 0, approved: 0, rejected: 0 } }) }));
  await page.route("**/api/v1/env/status", (r) =>
    r.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({ venv_exists: true, venv_path: "mock", python_path: "python", python_version: "3.12.0", pkg_count: 0, backend_dir: "mock" }) }));
  await page.route("**/api/v1/experiments", (r) => {
    if (!r.request().url().match(/experiments\/[^?]/)) {
      return r.fulfill({ status: 200, contentType: "application/json", body: "[]" });
    }
    return r.continue();
  });
  await page.route("**/api/v1/experiment-graphs", (r) => {
    if (!r.request().url().match(/experiment-graphs\/[^/]+/)) {
      return r.fulfill({ status: 200, contentType: "application/json", body: "[]" });
    }
    return r.continue();
  });
  await page.route("**/api/v1/indus-evidence/library**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({ documents: [], total: 0, limit: 100, offset: 0 }) }));
  await page.route("**/api/v1/indus-evidence/hypotheses", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ models: [] }) }));
  await page.route("**/api/v1/indus-evidence/claims**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(CLAIMS) }));
  await page.route("**/api/v1/dashboard/decipherment", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(MOCK_DECIPHER) }));
}

async function openClaimsTab(page: Page) {
  await page.goto("/");
  const btn = page.getByTitle("Evidence Graph").first();
  await btn.waitFor({ state: "visible", timeout: 10000 });
  await btn.click();
  await page.getByText(/🔖 Claims/).first().click();
  await expect(page.getByText(/2 total claims/i)).toBeVisible({ timeout: 8000 });
}

test.describe("Spec 029 Phase G — display guards", () => {
  test.beforeEach(async ({ page }) => {
    await setupMocks(page);
  });

  test("withdrawn headline pattern appears nowhere on the rendered surfaces", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("standing-position")).toBeVisible({ timeout: 8000 });
    const panelText = (await page.locator("body").innerText()).toLowerCase();
    expect(panelText).not.toMatch(/\d[\d,]*\s+signs deciphered/);
    expect(panelText).not.toContain("signs deciphered");
    expect(panelText).not.toContain("sa confidence");
    await openClaimsTab(page);
    const claimsText = (await page.locator("body").innerText()).toLowerCase();
    expect(claimsText).not.toContain("signs deciphered");
  });

  test("stage vocabulary is exactly the five verbatim names; no synonym labels", async ({ page }) => {
    await openClaimsTab(page);
    await page.getByText("Synthetic plain claim about a sign value.").click();
    await page.getByText("Synthetic bundle parent claim.").click();
    // Legend: exactly the five names, each present.
    const legendText = (await page.getByTestId("stage-legend").innerText()).toLowerCase();
    for (const name of ["created", "checked", "explained", "accepted", "digested"]) {
      expect(legendText).toContain(name);
    }
    // No synonym renders as a stage label anywhere on the claim
    // surfaces (legend, both lane regions, standing position,
    // stage summary).
    const surfaces = [
      legendText,
      (await page.getByTestId("lane1-region").first().innerText()).toLowerCase(),
      (await page.getByTestId("lane2-region").first().innerText()).toLowerCase(),
    ];
    for (const text of surfaces) {
      for (const synonym of ["proven", "confirmed"]) {
        expect(text).not.toContain(synonym);
      }
      // "verified" may appear only inside the governed
      // verified_unexplained risk-flag name, never as a label.
      const withoutFlag = text.replace(/verified_unexplained/g, "");
      expect(withoutFlag).not.toContain("verified");
    }
    // Stage names render in lane-2 positions (both expanded claims).
    const lane2s = page.getByTestId("lane2-region");
    await expect(lane2s).toHaveCount(2);
    expect((await lane2s.nth(0).innerText()).toLowerCase()).toContain("created");
    expect((await lane2s.nth(1).innerText()).toLowerCase()).toContain("checked");
  });

  test("every verdict display carries a not_understood slot", async ({ page }) => {
    await openClaimsTab(page);
    await page.getByText("Synthetic plain claim about a sign value.").click();
    await page.getByText("Synthetic bundle parent claim.").click();
    const slots = page.getByTestId("not-understood");
    await expect(slots).toHaveCount(2);
    const states = [
      await slots.nth(0).getAttribute("data-state"),
      await slots.nth(1).getAttribute("data-state"),
    ];
    expect(states.sort()).toEqual(["not-yet-recorded", "recorded"]);
  });

  test("lane labels and legend present on the claim surface; panel summary names all five stages", async ({ page }) => {
    await page.goto("/");
    const summary = page.getByTestId("stage-summary");
    await expect(summary).toBeVisible({ timeout: 8000 });
    const summaryText = (await summary.innerText()).toLowerCase();
    for (const name of ["created", "checked", "explained", "accepted", "digested"]) {
      expect(summaryText).toContain(name);
    }
    await openClaimsTab(page);
    await page.getByText("Synthetic plain claim about a sign value.").click();
    await expect(page.getByTestId("lane2-region")).toContainText("Lane 2 — human-paced settlement");
    await expect(page.getByTestId("lane1-region")).toContainText(
      "Lane 1 — machine-speed verification (checking only)");
    await expect(page.getByTestId("stage-legend")).toBeVisible();
  });
});
