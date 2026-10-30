import { expect, test } from "./fixtures";

/**
 * Navigation tests — Spec 081 shell.
 *
 * The shell is program-agnostic: brand "Glossa Lab / Epistemic
 * research workbench", a program switcher card, program-space nav in
 * loop order (Home, Claims, Digestion, Evidence & sources, Data,
 * Analysis, Experiments, Discovery, Research loop, Reports & ledger)
 * and a tool group (Jobs, Status, Settings, Help). The backend
 * seeds one active program ("Indus Script Decipherment") on a fresh
 * data dir, so program space is exercised here; the no-program
 * first run needs an empty backend and is verified separately.
 *
 * Sidebar nav buttons use title attr = clean label. Use getByTitle()
 * to avoid strict-mode collisions with other elements.
 */

test.describe("App shell", () => {
  test("loads and shows Glossa Lab title", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("Glossa Lab").first()).toBeVisible();
  });

  test("brand subtitle is the tool's, not a program's subject", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText(/Epistemic research workbench/i)).toBeVisible();
    // The old subject subtitle must be gone from the shell (C081-1).
    await expect(page.getByText(/Indus Script Analysis/i)).toHaveCount(0);
  });

  test("service chip names the service, host and check time", async ({ page }) => {
    await page.goto("/");
    // FR-007: identity + observation time, never a bare dot.
    await expect(page.getByText(/Glossa Lab v\d/).first()).toBeVisible();
    await expect(page.getByText(/checked \d{2}:\d{2}/).first()).toBeVisible();
  });

  test("program switcher card names the open program and its question", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("Indus Script Decipherment").first()).toBeVisible();
    // The seeded program has no question yet; the card falls back to
    // its description (a program's question shows here once set).
    await expect(page.getByText(/Decipher the Indus/i).first()).toBeVisible();
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

test.describe("Program-space navigation", () => {
  test("program nav items are visible in loop order groups", async ({ page }) => {
    await page.goto("/");
    for (const title of [
      "Home", "Claims", "Digestion", "Evidence & sources", "Data",
      "Analysis", "Experiments", "Discovery", "Research loop",
      "Reports & ledger",
    ]) {
      await expect(page.getByTitle(title).first()).toBeVisible();
    }
  });

  test("tool group items are visible", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTitle("Jobs").first()).toBeVisible();
    await expect(page.getByTitle("Status").first()).toBeVisible();
    await expect(page.getByTitle("Settings").first()).toBeVisible();
    await expect(page.getByTitle("Help").first()).toBeVisible();
  });

  test("retired subject nav labels are absent", async ({ page }) => {
    await page.goto("/");
    for (const title of [
      "Evidence Graph", "Corpora", "Hypotheses", "Notebooks",
      "Citations", "Pipelines", "Entropy", "Signs", "Timeline", "Dashboard",
    ]) {
      await expect(page.getByTitle(title)).toHaveCount(0);
    }
  });

  test("launch lands on the open program's home", async ({ page }) => {
    await page.goto("/");
    // Crumb trail ends at Home while a program is open.
    await expect(page.getByTitle("Home").first()).toBeVisible();
    await expect(page).toHaveURL(/#\/home/);
  });

  test("Programs lists the seeded program with its question", async ({ page }) => {
    await page.goto("/");
    // With a program open, Programs is reached from the switcher menu.
    await page.getByLabel("Switch program").click();
    await page.getByText(/All programs/).click();
    await expect(page.getByRole("heading", { name: "Programs" })).toBeVisible();
    await expect(page.getByText("Indus Script Decipherment").first()).toBeVisible();
  });

  test("clicking Claims renders the claims register", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Claims").first().click();
    // PR-5 (step 3) replaced the interim evidence-workspace claims
    // tab with the wireframe-03 register: the claims surface with
    // its PageHead and the separated verdict/digestion columns.
    await expect(page.getByTestId("claims-surface"))
      .toBeVisible({ timeout: 5000 });
    await expect(page.getByText("Verdict (machine checks)"))
      .toBeVisible({ timeout: 5000 });
    await expect(page.getByText("Digestion (human settlement)"))
      .toBeVisible({ timeout: 5000 });
  });

  test("clicking Evidence & sources renders the evidence workspace", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Evidence & sources").first().click();
    await expect(page.getByRole("heading", { name: "Evidence & sources" }))
      .toBeVisible({ timeout: 5000 });
    // Library tab is the workspace's landing lane.
    await expect(page.getByText(/Registered Papers/).first())
      .toBeVisible({ timeout: 5000 });
  });

  test("clicking Data shows the Corpora view", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Data").first().click();
    await expect(page.getByRole("heading", { name: "Corpora" })).toBeVisible();
  });

  test("clicking Status tab shows Status", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Status").first().click();
    await expect(page.getByRole("heading", { name: "Status" })).toBeVisible();
  });

  test("clicking Experiments renders the Experiment Builder canvas", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Experiments").first().click();
    await expect(page.getByText(/Experiment Builder/i).first()).toBeVisible();
  });

  test("clicking Jobs shows the jobs panel", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Jobs").first().click();
    await expect(page.getByRole("heading", { name: /Jobs/i })).toBeVisible();
  });
});

test.describe("Program management", () => {
  test("Manage programs shows the project manager with + New Project", async ({ page }) => {
    await page.goto("/#/builder");
    await expect(page.getByRole("button", { name: /New Project/i })).toBeVisible({ timeout: 5000 });
  });

  test("nav indicator starts clean (no stale unsaved-changes dot on load)", async ({ page }) => {
    await page.goto("/");
    const amber = await page.evaluate(() => {
      const el = document.querySelector('[title="Unsaved changes"]');
      return el ? el.getAttribute("title") : null;
    });
    expect(amber).toBeNull();
  });
});

test.describe("Experiments workspace features", () => {
  test("Run All button is visible in Experiments list header", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Experiments").first().click();
    await expect(
      page.getByTitle("Run all experiments (skips already-running ones)").first(),
    ).toBeVisible({ timeout: 5000 });
  });

  test("Stop All button not visible when nothing is running", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Experiments").first().click();
    const stopAllBtns = page.getByTitle("Stop all running experiments");
    expect(await stopAllBtns.count()).toBe(0);
  });

  test("floating Run button in canvas only appears when experiment is open", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Experiments").first().click();
    const floatingRun = page.getByTitle("Run experiment");
    const visibleBefore = await floatingRun.isVisible({ timeout: 1000 }).catch(() => false);
    expect(visibleBefore).toBe(false);
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
    await page.getByTitle(/Toggle dark mode/i).click();
    const stored2 = await page.evaluate(() => localStorage.getItem("glossa_dark"));
    expect(stored2).toBe("0");
  });
});
