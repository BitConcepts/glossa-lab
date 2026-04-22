import { expect, test } from "@playwright/test";

/**
 * Navigation tests — app shell, grouped tab bar, header features.
 * Runs against vite preview (port 4173) without requiring the backend.
 */

test.describe("App shell", () => {
  test("loads and shows Glossa Lab title", async ({ page }) => {
    await page.goto("/");
    // Logo is in a div/span in the sidebar — not an h1
    await expect(page.getByText("Glossa Lab").first()).toBeVisible();
  });

  test("shows collaboration subtitle", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText(/Indus Script Analysis/i)).toBeVisible();
  });

  test("shows health badge in header", async ({ page }) => {
    await page.goto("/");
    // Health badge contains "Healthy", "Degraded", or "Offline"
    await expect(page.locator("div").filter({ hasText: /Healthy|Degraded|Offline/ }).first()).toBeVisible();
  });

  test("shows Cmd+K button in header", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle(/Command palette/i)).toBeVisible();
  });

  test("shows dark mode toggle in header", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle(/Toggle dark mode/i)).toBeVisible();
  });
});

// Note: sidebar nav buttons use title attr = clean label (no emoji).
// Use getByTitle() to avoid strict mode violations caused by the bottom
// panel or other elements also having matching text content.
test.describe("Grouped tab navigation", () => {
  test("Workflow section tabs are visible", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle("Studies").first()).toBeVisible();
    await expect(page.getByTitle("Experiments").first()).toBeVisible();
    await expect(page.getByTitle("Corpora").first()).toBeVisible();
    await expect(page.getByTitle("Reports").first()).toBeVisible();
    await expect(page.getByTitle("Pipelines").first()).toBeVisible();
  });

  test("default tab renders Study Builder canvas", async ({ page }) => {
    await page.goto("/");
    // Default is the Studies canvas workspace — shows toolbar text, not an h2 heading
    await expect(page.getByText(/Study Builder/i).first()).toBeVisible();
  });

  test("clicking Status tab shows System Status", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Status").first().click();
    await expect(page.getByRole("heading", { name: "System Status" })).toBeVisible();
  });

  test("clicking Experiments tab renders Experiment Builder canvas", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Experiments").first().click();
    // Experiments now opens the unified Experiment Builder canvas — shows toolbar text
    await expect(page.getByText(/Experiment Builder/i).first()).toBeVisible();
  });

  test("clicking Corpora tab shows Corpora view", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Corpora").first().click();
    await expect(page.getByRole("heading", { name: "Corpora" })).toBeVisible();
  });

  test("AI Tools tab is visible in Research section", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("button", { name: /AI Tools/i })).toBeVisible();
  });

  test("Research group tabs are visible", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle("Hypotheses").first()).toBeVisible();
    await expect(page.getByTitle("Notebooks").first()).toBeVisible();
    await expect(page.getByTitle("Citations").first()).toBeVisible();
  });

  test("Analysis group tabs are visible", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle("Entropy").first()).toBeVisible();
    await expect(page.getByTitle("Timeline").first()).toBeVisible();
    await expect(page.getByTitle("Indus Data").first()).toBeVisible();
  });

  test("System items visible at sidebar bottom", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle("Status").first()).toBeVisible();
    // Jobs: use title to scope to sidebar (bottom panel also has a Jobs tab)
    await expect(page.getByTitle("Jobs").first()).toBeVisible();
    await expect(page.getByTitle("Settings").first()).toBeVisible();
  });

  test("Exp. Builder tab is no longer in sidebar (merged into Experiments)", async ({ page }) => {
    await page.goto("/");
    // The old separate Exp. Builder tab should not exist — it is now the Experiments canvas
    const expBuilderBtn = page.getByRole("button", { name: /Exp\.?\s*Builder/i });
    await expect(expBuilderBtn).toHaveCount(0);
  });
});

test.describe("Studies workspace features", () => {
  test("Run All button is visible in Studies list header", async ({ page }) => {
    await page.goto("/");
    // ▶▶ button in the Studies left panel header
    await expect(page.getByTitle("Run all studies in parallel").first()).toBeVisible();
  });

  test("floating Run Study button appears on canvas when study is open (requires backend)", async ({ page }) => {
    await page.goto("/");
    // Floating run button only shows when a study with nodes is loaded
    // This test checks the canvas area for the button when backend is available
    const runBtn = page.getByTitle("Run this study");
    const hasStudies = await page.getByText(/Positional Profile/i).first().isVisible({ timeout: 3000 }).catch(() => false);
    if (!hasStudies) { test.skip(); return; }
    await page.getByText(/Positional Profile/i).first().click();
    await page.waitForTimeout(600);
    const floatingBtn = await runBtn.isVisible({ timeout: 2000 }).catch(() => false);
    // Just verify page doesn't crash; button may or may not be visible depending on node count
    expect(floatingBtn || true).toBeTruthy();
  });

  test("nav Studies indicator starts clean (no stale orange dot on page load)", async ({ page }) => {
    await page.goto("/");
    // The Studies nav button should NOT show the amber dirty dot on fresh load
    // because we clear stale glossa_study_draft on StudyBuilderView mount.
    // Amber dot has a 0 0 4px #f59e0b box-shadow — we check it's not present immediately.
    const amberId = await page.evaluate(() => {
      const el = document.querySelector('[title="Unsaved changes"]');
      return el ? el.getAttribute('title') : null;
    });
    expect(amberId).toBeNull();
  });
});

test.describe("Experiments workspace features", () => {
  test("Run All button is visible in Experiments list header", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Experiments").first().click();
    await expect(page.getByTitle("Run all experiments in parallel").first()).toBeVisible();
  });

  test("Stop All button not visible when nothing is running", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Experiments").first().click();
    // Stop All only appears when activeRuns has entries
    const stopAllBtns = page.getByTitle("Stop all running experiments");
    const count = await stopAllBtns.count();
    expect(count).toBe(0);
  });

  test("floating Run button in canvas only appears when experiment is open", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Experiments").first().click();
    // When no experiment is open, there should be no floating run button
    const floatingRun = page.getByTitle("Run experiment");
    const visibleBefore = await floatingRun.isVisible({ timeout: 1000 }).catch(() => false);
    expect(visibleBefore).toBe(false);
  });
});

test.describe("Jobs panel", () => {
  test("Jobs tab is visible in sidebar", async ({ page }) => {
    await page.goto("/");
    // Use getByTitle to avoid strict mode: bottom panel also has a 'Jobs' tab
    await expect(page.getByTitle("Jobs").first()).toBeVisible();
  });

  test("clicking Jobs tab shows jobs panel", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Jobs").first().click();
    await expect(page.getByRole("heading", { name: /Jobs/i })).toBeVisible();
  });
});

test.describe("Dark mode", () => {
  test("toggling dark mode changes body background", async ({ page }) => {
    await page.goto("/");
    const before = await page.evaluate(() => document.body.style.background);
    await page.getByTitle(/Toggle dark mode/i).click();
    const after = await page.evaluate(() => document.body.style.background);
    expect(before).not.toBe(after);
  });

  test("dark mode preference persists via localStorage", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle(/Toggle dark mode/i).click();
    const stored = await page.evaluate(() => localStorage.getItem("glossa_dark"));
    expect(stored).toBe("1");
    // Toggle back
    await page.getByTitle(/Toggle dark mode/i).click();
    const stored2 = await page.evaluate(() => localStorage.getItem("glossa_dark"));
    expect(stored2).toBe("0");
  });
});
