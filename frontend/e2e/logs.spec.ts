import { expect, test } from "./fixtures";

/**
 * Spec 087 S5 (T502, claim C087-10): the restored Logs view.
 *
 * The terminal-log and record endpoints are intercepted per-test
 * (the palette-error.spec.ts pattern), so these run regardless of
 * backend state:
 *   1. the Tool home group carries a Logs entry between Jobs and
 *      Status (Q1), and clicking it opens the stream tab over the
 *      getLog first load;
 *   2. the level filter is client-side over the fetched lines;
 *   3. a failed first load renders the named error state with
 *      retry — never a silent empty surface (the S1/F5 lesson);
 *   4. purge is reachable only through its confirmation (Q2):
 *      opening the confirmation does not call the endpoint,
 *      Cancel does not call it, the confirm button does, exactly
 *      once;
 *   5. the records tab reads jobs, phase actions and the
 *      notification log as one read-only log: rows render, a job
 *      expands to its stored detail + result excerpt, a failed
 *      phase action shows its error_message verbatim, and a
 *      notification's recipient is shown masked.
 */

const LOG_ROUTE = "**/api/v1/terminal/log?lines=200";
const LOG_COUNT_ROUTE = "**/api/v1/terminal/log?lines=1";
const STREAM_ROUTE = "**/api/v1/terminal/log/stream";
const PURGE_ROUTE = "**/api/v1/terminal/log/purge";
const JOBS_ROUTE = "**/api/v1/jobs";
const RESULTS_ROUTE = "**/api/v1/jobs/*/results";
const PHASE_ACTIONS_ROUTE = "**/api/v1/phase/actions";
const NOTIF_LOG_ROUTE = "**/api/v1/notifications/log?limit=100";
const REPORTS_ROUTE = "**/api/v1/reports";

const LOG_LINES = [
  JSON.stringify({
    timestamp: "2026-11-02 14:52:03,118",
    level: "INFO",
    module: "glossa_lab.main",
    message: "Glossa Lab backend ready",
  }),
  JSON.stringify({
    timestamp: "2026-11-02 14:52:12,377",
    level: "WARNING",
    module: "glossa_lab.experiment_graph",
    message: "example warning line for the filter test",
  }),
  JSON.stringify({
    timestamp: "2026-11-02 14:53:01,220",
    level: "ERROR",
    module: "glossa_lab.api.terminal",
    message: "frontend error intake captured a render error",
  }),
];

const JOB = {
  id: "20261102T145211Z-graph-run",
  name: "Graph run — indus_sa_dravidian",
  pipeline: "exp_run",
  status: "completed",
  params: { experiment: "indus_sa_dravidian" },
  created_at: "2026-11-02T14:52:11Z",
  updated_at: "2026-11-02T14:52:14Z",
};

const PHASE_ACTION = {
  id: "pa-1",
  phase: 401,
  action_label: "execute stage",
  action_type: "stage",
  params_json: "{}",
  status: "failed",
  job_id: "20261102T143055Z-pipeline-run",
  error_message: "report file not found: reports/phase401_results.json",
  started_at: "2026-11-02T14:31:02Z",
  completed_at: "2026-11-02T14:31:43Z",
  created_at: "2026-11-02T14:31:02Z",
};

const NOTIFICATION = {
  id: "n-1",
  recipient: "operator@example.com",
  subject: "research-breakthrough alert",
  kind: "breakthrough",
  sent_at: "2026-11-02T13:12:19Z",
  item_count: 3,
  status: "sent",
  error: "",
};

async function stubStream(page: import("@playwright/test").Page) {
  // Faithful to the endpoint: the backfill is the file's tail (here
  // all 3 lines, flagged backfill), then live lines as written.
  const backfill = LOG_LINES.map(
    (text) => `data: ${JSON.stringify({ text, backfill: true })}\n\n`,
  ).join("");
  await page.route(STREAM_ROUTE, (route) =>
    route.fulfill({
      status: 200,
      contentType: "text/event-stream",
      body:
        backfill +
        `data: ${JSON.stringify({ text: JSON.stringify({
          timestamp: "2026-11-02 14:54:00,000",
          level: "INFO",
          module: "glossa_lab.api.jobs",
          message: "live line appended by the tail",
        }) })}\n\n`,
    }),
  );
}

async function stubLogOk(page: import("@playwright/test").Page) {
  await page.route(LOG_ROUTE, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        lines: LOG_LINES,
        total_lines: 3,
        exists: true,
        file: "glossa.log",
      }),
    }),
  );
  await page.route(LOG_COUNT_ROUTE, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        lines: [LOG_LINES[2]],
        total_lines: 3,
        exists: true,
        file: "glossa.log",
      }),
    }),
  );
}

async function openLogs(page: import("@playwright/test").Page) {
  await page.goto("/");
  const nav = page.getByTitle("Logs").first();
  await nav.waitFor({ state: "visible", timeout: 8000 });
  await nav.click();
  await expect(page.getByRole("heading", { name: "Logs" })).toBeVisible();
}

test.describe("Logs view (Spec 087 S5)", () => {
  test("nav carries Logs between Jobs and Status; stream tab renders the first load and the tail", async ({ page }) => {
    await stubLogOk(page);
    await stubStream(page);
    await page.goto("/");
    await page.getByTitle("Logs").first().waitFor({ state: "visible", timeout: 8000 });
    const titles = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll("button[title]"));
      return btns.map((b) => b.getAttribute("title"));
    });
    const jobsAt = titles.indexOf("Jobs");
    const logsAt = titles.indexOf("Logs");
    const statusAt = titles.indexOf("Status");
    expect(jobsAt).toBeGreaterThanOrEqual(0);
    expect(logsAt).toBeGreaterThan(jobsAt);
    expect(statusAt).toBeGreaterThan(logsAt);

    await openLogs(page);
    const stream = page.getByTestId("log-stream");
    await expect(stream).toContainText("Glossa Lab backend ready");
    await expect(stream).toContainText("example warning line for the filter test");
    // The stream's live (non-backfill) line is appended; its backfill
    // of the first line is merged, not doubled.
    await expect(stream).toContainText("live line appended by the tail");
    expect(await stream.getByText("Glossa Lab backend ready").count()).toBe(1);
    await expect(page.getByText(/exists · 3 lines/)).toBeVisible();
  });

  test("level filter hides other levels client-side", async ({ page }) => {
    await stubLogOk(page);
    await stubStream(page);
    await openLogs(page);
    const stream = page.getByTestId("log-stream");
    await expect(stream).toContainText("example warning line for the filter test");
    await page.getByRole("button", { name: "ERROR", exact: true }).click();
    await expect(stream).toContainText("frontend error intake captured a render error");
    await expect(stream).not.toContainText("example warning line for the filter test");
    await expect(stream).not.toContainText("Glossa Lab backend ready");
  });

  test("failed first load renders the named error state; retry recovers", async ({ page }) => {
    let calls = 0;
    await page.route(LOG_ROUTE, (route) => {
      calls += 1;
      if (calls === 1) {
        return route.fulfill({ status: 500, contentType: "text/plain", body: "seeded log failure" });
      }
      return route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ lines: LOG_LINES, total_lines: 3, exists: true, file: "glossa.log" }),
      });
    });
    await stubStream(page);
    await openLogs(page);
    const alert = page.getByTestId("logs-error");
    await expect(alert).toBeVisible();
    await expect(alert).toContainText("Log failed to load");
    await page.getByRole("button", { name: "Retry" }).click();
    await expect(page.getByTestId("log-stream")).toContainText("Glossa Lab backend ready");
  });

  test("purge fires only through its confirmation, exactly once", async ({ page }) => {
    await stubLogOk(page);
    await stubStream(page);
    let purgeCalls = 0;
    await page.route(PURGE_ROUTE, (route) => {
      purgeCalls += 1;
      return route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ cleared: 4096, file: "glossa.log", truncated: true, deleted_rotated: [] }),
      });
    });
    await openLogs(page);
    await expect(page.getByTestId("log-stream")).toContainText("Glossa Lab backend ready");

    await page.getByRole("button", { name: "Purge log…" }).click();
    const confirmBox = page.getByTestId("purge-confirm");
    await expect(confirmBox).toBeVisible();
    await expect(confirmBox).toContainText("cannot be undone");
    expect(purgeCalls).toBe(0);

    await confirmBox.getByRole("button", { name: "Cancel" }).click();
    await expect(confirmBox).toHaveCount(0);
    expect(purgeCalls).toBe(0);

    await page.getByRole("button", { name: "Purge log…" }).click();
    await page.getByTestId("purge-confirm").getByRole("button", { name: /Purge 3 lines/ }).click();
    await expect.poll(() => purgeCalls).toBe(1);
    await expect(page.getByText(/Log purged/)).toBeVisible();
  });

  test("records tab reads the three record tables as one read-only log", async ({ page }) => {
    await stubLogOk(page);
    await stubStream(page);
    await page.route(JOBS_ROUTE, (route) => {
      if (route.request().method() !== "GET") return route.fallback();
      return route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([JOB]),
      });
    });
    await page.route(RESULTS_ROUTE, (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ nodes_executed: 27, failed_nodes: 0 }),
      }),
    );
    await page.route(PHASE_ACTIONS_ROUTE, (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ actions: [PHASE_ACTION] }),
      }),
    );
    await page.route(NOTIF_LOG_ROUTE, (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ entries: [NOTIFICATION], limit: 100 }),
      }),
    );
    await page.route(REPORTS_ROUTE, (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: "[]" }),
    );

    await openLogs(page);
    await page.getByRole("button", { name: "Job & phase records" }).click();

    await expect(page.getByText("Graph run — indus_sa_dravidian")).toBeVisible();
    await expect(page.getByText("Phase action — execute stage")).toBeVisible();
    await expect(page.getByText(/report file not found: reports\/phase401_results\.json/)).toBeVisible();
    await expect(page.getByText("Notification — research-breakthrough alert")).toBeVisible();
    await expect(page.getByText(/Records are read-only here/)).toBeVisible();

    // Expand the job: stored detail + the job_results excerpt.
    const row = page.getByRole("row", { name: /Graph run/ });
    await row.getByRole("button", { name: /Detail/ }).click();
    await expect(page.getByText(/Detail — job record/)).toBeVisible();
    await expect(page.getByText(/nodes_executed/)).toBeVisible();

    // Expand the notification: the recipient is masked, never raw.
    const nrow = page.getByRole("row", { name: /Notification/ });
    await nrow.getByRole("button", { name: /Detail/ }).click();
    await expect(page.getByText(/o\*\*\*@example\.com/)).toBeVisible();
    await expect(page.getByText(/operator@example\.com/)).toHaveCount(0);

    // Read-only: the records surface carries no record-mutating control.
    await expect(page.getByRole("button", { name: /Cancel job|Delete|Pause job/i })).toHaveCount(0);
  });
});
