import { expect, test, type Page } from "./fixtures";

/**
 * Spec 029 Phase E2 — lane-separated rendering (FR-029-09/10,
 * FR-029-05 display rule; OD-4).
 *
 * All backend responses are mocked with SYNTHETIC fixtures: one
 * plain extracted claim (stage created, no authored not_understood,
 * not a bundle) and one synthetic bundle parent whose attribution
 * is contested (stage capped at checked) carrying an authored
 * not_understood statement. No live record is given text or a
 * contest by these tests — the live rendering of the absence
 * states is verified separately against the real backend.
 *
 * Guards asserted on the RENDERED surfaces:
 *  - the OD-4 legend shows the five stage names verbatim;
 *  - lane-1 and lane-2 regions are separate, labelled regions;
 *  - the lane-1 score value never appears inside the lane-2 region,
 *    and the lane-2 contest content never appears inside lane 1;
 *  - no stage name renders inside a lane-1 region;
 *  - an unauthored not_understood renders as a stated gap
 *    ("not yet recorded"), never as substitute prose presented as
 *    the record's own statement.
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
  // Spec 081: the shell is program-centric — with zero programs it
  // stays on the tool home and no program surface (dashboard, claims)
  // renders. One fixture program auto-activates (single-project rule),
  // which is the mocked equivalent of the old shell's global mode.
  await page.route("**/api/v1/projects", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify([{
        id: "indus_decipherment", label: "Indus Script Decipherment",
        description: "Mock program (shell bootstrap).", prompt_context: "", question: "",
        // Spec 081 Amendment 2: the standing position is program data,
        // carried on the program's record; the guards below assert it
        // on the program home, where the record renders it.
        standing_position:
          "The Indus script is not deciphered. The readings this program records are " +
          "candidate readings, each one a claim standing at a stage of the claim " +
          "lifecycle. A reading is not settled by being recorded and checked, and " +
          "no count in this program is a measure of decipherment.",
        topic_ids: [], experiment_ids: [], corpus_ids: [], is_active: 1,
        created_at: "2026-01-01T00:00:00Z", updated_at: "2026-01-01T00:00:00Z",
      }]) }));
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
  // Spec 081 step 6: the claims register reads the program-scoped
  // family now (the /indus-evidence/* routes above remain as the
  // backend's one-release shim). Same synthetic payloads.
  await page.route("**/api/v1/programs/*/claims**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(CLAIMS) }));
  await page.route("**/api/v1/programs/*/hypotheses", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ models: [] }) }));
  await page.route("**/api/v1/programs/*/library**", (r) =>
    r.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({ documents: [], total: 0, limit: 100, offset: 0 }) }));
  await page.route("**/api/v1/programs/**/trail", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({}) }));
  await page.route("**/api/v1/dashboard/decipherment", (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(MOCK_DECIPHER) }));
}

async function openClaimsTab(page: Page) {
  // Spec 081 step 6: claims are their own program surface now (the
  // Evidence & sources claims tab retired with IndusEvidenceView).
  await page.goto("/");
  const btn = page.getByTitle("Claims").first();
  await btn.waitFor({ state: "visible", timeout: 10000 });
  await btn.click();
  await expect(page.getByText("Synthetic plain claim about a sign value.")).toBeVisible({ timeout: 8000 });
}

test.describe("Spec 029 Phase E2 — lane-separated rendering", () => {
  test.beforeEach(async ({ page }) => {
    await setupMocks(page);
  });

  test("legend shows the five stage names verbatim with the never-settles line", async ({ page }) => {
    await openClaimsTab(page);
    const legend = page.getByTestId("stage-legend");
    await expect(legend).toBeVisible();
    const text = (await legend.innerText()).toLowerCase();
    for (const name of ["created", "checked", "explained", "accepted", "digested"]) {
      expect(text).toContain(name);
    }
    expect(text).toContain("never settle a claim");
  });

  test("plain claim: two labelled lane regions; not_understood renders as a stated gap", async ({ page }) => {
    await openClaimsTab(page);
    await page.getByText("Synthetic plain claim about a sign value.").click();
    const lane2 = page.getByTestId("lane2-region");
    const lane1 = page.getByTestId("lane1-region");
    await expect(lane2).toBeVisible();
    await expect(lane1).toBeVisible();
    await expect(lane2).toContainText("Lane 2 — human-paced settlement");
    await expect(lane2).toContainText("created");
    await expect(lane1).toContainText("Lane 1 — machine-speed verification (checking only)");
    await expect(lane1).toContainText("untested");
    await expect(lane1).toContainText("AEE score");
    await expect(lane1).toContainText("band: medium");
    const nu = lane1.getByTestId("not-understood");
    await expect(nu).toHaveAttribute("data-state", "not-yet-recorded");
    await expect(nu).toContainText("not yet recorded");
    await expect(nu).toContainText("no machine-generated text is substituted");
    // No live-style contest is invented for a non-bundle claim.
    await expect(lane2.getByTestId("contest-display")).toHaveAttribute("data-state", "no-bundle");
  });

  test("contested bundle parent: contest + cap on the parent; authored not_understood; lanes do not mix", async ({ page }) => {
    await openClaimsTab(page);
    await page.getByText("Synthetic bundle parent claim.").click();
    const lane2 = page.getByTestId("lane2-region");
    const lane1 = page.getByTestId("lane1-region");
    const contest = lane2.getByTestId("contest-display");
    await expect(contest).toHaveAttribute("data-state", "contested");
    await expect(contest).toContainText("Attribution contested");
    await expect(contest).toContainText("capped at checked");
    await expect(contest).toContainText("Synthetic Contester");
    const nu = lane1.getByTestId("not-understood");
    await expect(nu).toHaveAttribute("data-state", "recorded");
    await expect(nu).toContainText("which sign values the neighbouring signs force");
    // Lane separation on the rendered DOM: the lane-1 score value
    // never appears in the lane-2 region; lane-2 contest content
    // never appears in the lane-1 region.
    await expect(lane1).toContainText("0.917");
    expect(await lane2.innerText()).not.toContain("0.917");
    expect(await lane1.innerText()).not.toContain("Synthetic Contester");
  });

  test("verbatim-name guard: no stage name renders inside a lane-1 region", async ({ page }) => {
    await openClaimsTab(page);
    // Spec 081: the register opens one claim's detail at a time (the
    // old surface expanded rows in place). The guard is unchanged —
    // it now visits each claim's detail in turn and checks its
    // lane-1 region.
    for (const claimText of [
      "Synthetic plain claim about a sign value.",
      "Synthetic bundle parent claim.",
    ]) {
      await page.getByText(claimText).click();
      const lane1 = page.getByTestId("lane1-region");
      await expect(lane1).toBeVisible();
      const text = (await lane1.innerText()).toLowerCase();
      for (const name of ["created", "explained", "accepted", "digested"]) {
        expect(text).not.toMatch(new RegExp(`\\b${name}\\b`));
      }
      // Synonyms used as stage labels are equally forbidden here.
      for (const synonym of ["proven", "confirmed"]) {
        expect(text).not.toContain(synonym);
      }
      await page.getByRole("button", { name: "← All claims" }).click();
      await expect(page.getByText("Synthetic plain claim about a sign value.")).toBeVisible();
    }
  });

  test("panel leads with the standing position and the lane-2 stage summary", async ({ page }) => {
    await page.goto("/");
    const standing = page.getByTestId("standing-position");
    await expect(standing).toBeVisible({ timeout: 8000 });
    await expect(standing).toContainText("The Indus script is not deciphered");
    const summary = page.getByTestId("stage-summary");
    await expect(summary).toContainText("created");
    await expect(summary).toContainText("193");
    await expect(summary).toContainText("checked");
    await expect(summary).toContainText("94");
    await expect(summary).toContainText("digested");
    await expect(page.getByTestId("stage-legend")).toBeVisible();
    // E1's withdrawn headline stays withdrawn on the rendered panel.
    expect((await page.locator("body").innerText()).toLowerCase()).not.toContain("signs deciphered");
  });
});
