import { expect, test } from "@playwright/test";

/**
 * Backend integration tests — run against the live backend on port 8001.
 *
 * These tests require the backend to be running:
 *   shell.cmd run   (or pythonw -m uvicorn glossa_lab.main:app --port 8001)
 *
 * Tests cover: health, corpora, entropy, system metrics, hypotheses,
 *   notebooks, citations, command palette, AI Chat tab, AI Tools tab,
 *   Ollama settings, Sign Dictionary, Timeline.
 */

// All integration tests skip gracefully if backend is down
async function backendRunning(page: Parameters<typeof page.goto>[0] extends undefined ? never : import("@playwright/test").Page): Promise<boolean> {
  try {
    const resp = await (page as import("@playwright/test").Page).request.get("/api/v1/health");
    return resp.status() === 200;
  } catch {
    return false;
  }
}

// ── Backend health ────────────────────────────────────────────────────────────

test.describe("Backend health", () => {
  test("health endpoint returns healthy", async ({ request }) => {
    const resp = await request.get("/api/v1/health");
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.status).toMatch(/healthy|degraded/);
    expect(body.version).toBeTruthy();
  });

  test("studies endpoint returns array", async ({ request }) => {
    const resp = await request.get("/api/v1/studies");
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(Array.isArray(body)).toBeTruthy();
  });

  test("texts endpoint returns array", async ({ request }) => {
    const resp = await request.get("/api/v1/texts");
    expect(resp.status()).toBe(200);
    expect(Array.isArray(await resp.json())).toBeTruthy();
  });

  test("hypotheses endpoint works", async ({ request }) => {
    const resp = await request.get("/api/v1/hypotheses");
    expect(resp.status()).toBe(200);
    expect(Array.isArray(await resp.json())).toBeTruthy();
  });

  test("notebooks endpoint works", async ({ request }) => {
    const resp = await request.get("/api/v1/notebooks");
    expect(resp.status()).toBe(200);
    expect(Array.isArray(await resp.json())).toBeTruthy();
  });

  test("citations endpoint works", async ({ request }) => {
    const resp = await request.get("/api/v1/citations");
    expect(resp.status()).toBe(200);
    expect(Array.isArray(await resp.json())).toBeTruthy();
  });

  test("system metrics endpoint works", async ({ request }) => {
    const resp = await request.get("/api/v1/system/metrics");
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body).toHaveProperty("cpu");
    expect(body).toHaveProperty("ram");
    expect(body).toHaveProperty("disk");
    expect(body).toHaveProperty("network");
    expect(body.cpu).toHaveProperty("percent");
    expect(body.ram).toHaveProperty("total_gb");
  });

  test("system GPU endpoint works", async ({ request }) => {
    const resp = await request.get("/api/v1/system/gpu");
    expect(resp.status()).toBe(200);
    expect(Array.isArray(await resp.json())).toBeTruthy();
  });

  test("ollama status endpoint works", async ({ request }) => {
    const resp = await request.get("/api/v1/ollama/status");
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body).toHaveProperty("running");
    expect(body).toHaveProperty("message");
  });

  test("ollama library endpoint returns curated models", async ({ request }) => {
    const resp = await request.get("/api/v1/ollama/library");
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(Array.isArray(body.models)).toBeTruthy();
    expect(body.models.length).toBeGreaterThan(5);
    // Mistral should be in the library
    const hasMistral = body.models.some((m: { family: string }) => m.family === "mistral");
    expect(hasMistral).toBeTruthy();
  });

  test("ollama recommend endpoint returns recommendation", async ({ request }) => {
    const resp = await request.get("/api/v1/ollama/recommend");
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body).toHaveProperty("recommended");
    expect(body).toHaveProperty("glossa_note");
  });
});

// ── Corpus entropy routes ─────────────────────────────────────────────────────

test.describe("Corpus analysis routes", () => {
  let textId = "";

  test.beforeAll(async ({ request }) => {
    // Get a text ID to test with
    const resp = await request.get("/api/v1/texts");
    const texts = await resp.json();
    if (texts.length > 0) {
      textId = texts[0].id;
    }
  });

  test("entropy endpoint returns H1/H2 metrics", async ({ request }) => {
    test.skip(!textId, "No corpus available");
    const resp = await request.get(`/api/v1/texts/${textId}/entropy`);
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body).toHaveProperty("h1");
    expect(body).toHaveProperty("conditional_h");
    expect(body).toHaveProperty("type_token_ratio");
    expect(body).toHaveProperty("zipf_table");
    expect(typeof body.h1).toBe("number");
    expect(body.h1).toBeGreaterThan(0);
  });

  test("ngrams endpoint returns bigrams", async ({ request }) => {
    test.skip(!textId, "No corpus available");
    const resp = await request.get(`/api/v1/texts/${textId}/ngrams?n=2&limit=10`);
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(Array.isArray(body)).toBeTruthy();
    if (body.length > 0) {
      expect(body[0]).toHaveProperty("ngram");
      expect(body[0]).toHaveProperty("count");
    }
  });

  test("concordance endpoint returns KWIC hits", async ({ request }) => {
    test.skip(!textId, "No corpus available");
    // Get a real token first
    const eResp = await request.get(`/api/v1/texts/${textId}/entropy`);
    const metrics = await eResp.json();
    const topToken = metrics.zipf_table?.[0]?.token;
    test.skip(!topToken, "No tokens");

    const resp = await request.get(`/api/v1/texts/${textId}/concordance?q=${encodeURIComponent(topToken)}&w=3`);
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body).toHaveProperty("query");
    expect(body).toHaveProperty("total");
    expect(body).toHaveProperty("hits");
    expect(body.total).toBeGreaterThan(0);
  });

  test("export endpoint returns txt file", async ({ request }) => {
    test.skip(!textId, "No corpus available");
    const resp = await request.get(`/api/v1/texts/${textId}/export?fmt=txt`);
    expect(resp.status()).toBe(200);
    const ct = resp.headers()["content-type"];
    expect(ct).toContain("text/plain");
  });

  test("export endpoint returns csv file", async ({ request }) => {
    test.skip(!textId, "No corpus available");
    const resp = await request.get(`/api/v1/texts/${textId}/export?fmt=csv`);
    expect(resp.status()).toBe(200);
    expect(resp.headers()["content-type"]).toContain("text/csv");
  });

  test("export endpoint returns json file", async ({ request }) => {
    test.skip(!textId, "No corpus available");
    const resp = await request.get(`/api/v1/texts/${textId}/export?fmt=json`);
    expect(resp.status()).toBe(200);
    expect(resp.headers()["content-type"]).toContain("application/json");
    const body = await resp.json();
    expect(body).toHaveProperty("content");
  });
});

// ── Research CRUD ─────────────────────────────────────────────────────────────

test.describe("Hypothesis CRUD", () => {
  let hId = "";

  test("create hypothesis", async ({ request }) => {
    const resp = await request.post("/api/v1/hypotheses", {
      data: { title: "E2E Test Hypothesis", statement: "Created by Playwright", status: "active" },
    });
    expect(resp.status()).toBe(201);
    const body = await resp.json();
    expect(body.title).toBe("E2E Test Hypothesis");
    expect(body.status).toBe("active");
    hId = body.id;
  });

  test("update hypothesis status", async ({ request }) => {
    test.skip(!hId, "No hypothesis created");
    const resp = await request.put(`/api/v1/hypotheses/${hId}`, {
      data: { status: "confirmed" },
    });
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.status).toBe("confirmed");
  });

  test("add evidence to hypothesis", async ({ request }) => {
    test.skip(!hId, "No hypothesis created");
    const resp = await request.put(`/api/v1/hypotheses/${hId}`, {
      data: { evidence: ["H1=0.875 confirms natural language profile"] },
    });
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.evidence).toContain("H1=0.875 confirms natural language profile");
  });

  test("list hypotheses includes our test entry", async ({ request }) => {
    test.skip(!hId, "No hypothesis created");
    const resp = await request.get("/api/v1/hypotheses");
    const body = await resp.json();
    const found = body.find((h: { id: string }) => h.id === hId);
    expect(found).toBeTruthy();
  });

  test("delete hypothesis", async ({ request }) => {
    test.skip(!hId, "No hypothesis created");
    const resp = await request.delete(`/api/v1/hypotheses/${hId}`);
    expect(resp.status()).toBe(200);
    // Confirm gone
    const listResp = await request.get("/api/v1/hypotheses");
    const body = await listResp.json();
    expect(body.find((h: { id: string }) => h.id === hId)).toBeUndefined();
  });
});

test.describe("Notebook CRUD", () => {
  let nId = "";

  test("create notebook", async ({ request }) => {
    const resp = await request.post("/api/v1/notebooks", {
      data: { title: "E2E Test Notebook", content: "# Test\nPlaywright test." },
    });
    expect(resp.status()).toBe(201);
    const body = await resp.json();
    expect(body.title).toBe("E2E Test Notebook");
    nId = body.id;
  });

  test("update notebook content", async ({ request }) => {
    test.skip(!nId, "No notebook created");
    const resp = await request.put(`/api/v1/notebooks/${nId}`, {
      data: { content: "# Updated\nModified by test." },
    });
    expect(resp.status()).toBe(200);
    expect((await resp.json()).content).toContain("Updated");
  });

  test("delete notebook", async ({ request }) => {
    test.skip(!nId, "No notebook created");
    expect((await request.delete(`/api/v1/notebooks/${nId}`)).status()).toBe(200);
  });
});

test.describe("Citation CRUD", () => {
  let cId = "";

  test("create citation", async ({ request }) => {
    const resp = await request.post("/api/v1/citations", {
      data: { key: "e2e_test_2026", title: "E2E Test Paper", authors: "Playwright, Test", year: "2026", venue: "Test Conf", doi: "", url: "", bibtex: "", notes: "" },
    });
    expect(resp.status()).toBe(201);
    const body = await resp.json();
    expect(body.key).toBe("e2e_test_2026");
    cId = body.id;
  });

  test("update citation notes", async ({ request }) => {
    test.skip(!cId, "No citation created");
    const resp = await request.put(`/api/v1/citations/${cId}`, { data: { notes: "Test note" } });
    expect(resp.status()).toBe(200);
    expect((await resp.json()).notes).toBe("Test note");
  });

  test("delete citation", async ({ request }) => {
    test.skip(!cId, "No citation created");
    expect((await request.delete(`/api/v1/citations/${cId}`)).status()).toBe(200);
  });
});

// ── System metrics peaks ──────────────────────────────────────────────────────

test.describe("System metrics peaks", () => {
  test("clear peaks resets all peak values", async ({ request }) => {
    const resp = await request.post("/api/v1/system/peaks/clear");
    expect(resp.status()).toBe(200);
    const body = await resp.json();
    expect(body.cleared).toBe(true);
    expect(Object.values(body.peaks as Record<string, number>).every((v) => v === 0)).toBeTruthy();
  });

  test("metrics snapshot includes peaks object", async ({ request }) => {
    const resp = await request.get("/api/v1/system/metrics");
    const body = await resp.json();
    expect(body).toHaveProperty("peaks");
    expect(typeof body.peaks).toBe("object");
  });
});

// ── UI feature tests ──────────────────────────────────────────────────────────

test.describe("Corpora UI", () => {
  test("corpora page shows corpus cards", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Corpora").first().click();
    await page.waitForTimeout(1000);
    // Either shows corpora or "No corpora yet" message
    const hasCorpora = await page.locator("div").filter({ hasText: /corpus entries/i }).count() > 0;
    const hasEmpty = await page.getByText(/No corpora yet/i).count() > 0;
    expect(hasCorpora || hasEmpty).toBeTruthy();
  });

  test("corpus card expands on click", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Corpora").first().click();
    await page.waitForTimeout(1500);
    // If there are corpus cards, click the first one
    const cards = page.locator("[style*='border: 1px solid'][style*='border-radius: 8px']");
    const count = await cards.count();
    if (count > 0) {
      await cards.first().click();
      // Should show tab bar with Browse/Edit/Stats/etc.
      await expect(page.getByRole("button", { name: "Browse" })).toBeVisible({ timeout: 3000 });
    }
  });
});

test.describe("Entropy Dashboard UI", () => {
  test("entropy tab shows dashboard with corpus selector", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Entropy").first().click();
    await expect(page.getByRole("heading", { name: "Entropy Dashboard" })).toBeVisible();
    await expect(page.getByRole("button", { name: /Add Corpus/i })).toBeVisible();
  });

  test("entropy dashboard shows select corpus dropdown", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Entropy").first().click();
    await page.waitForTimeout(1000);
    await expect(page.locator("select").filter({ hasText: /select corpus/i })).toBeVisible();
  });
});

test.describe("Hypothesis Tracker UI", () => {
  test("hypotheses tab loads", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Hypotheses").first().click();
    await expect(page.getByRole("heading", { name: "Hypothesis Tracker" })).toBeVisible();
    await expect(page.getByPlaceholder(/New hypothesis title/i)).toBeVisible();
  });

  test("can type a hypothesis title", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Hypotheses").first().click();
    const input = page.getByPlaceholder(/New hypothesis title/i);
    await input.fill("Indus Script is linguistic");
    await expect(input).toHaveValue("Indus Script is linguistic");
    // Clear to not pollute DB
    await input.fill("");
  });
});

test.describe("Research Notebook UI", () => {
  test("notebooks tab loads", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Notebooks").first().click();
    await expect(page.getByRole("heading", { name: "Research Notebooks" })).toBeVisible();
    await expect(page.getByPlaceholder(/New notebook title/i)).toBeVisible();
  });
});

test.describe("Citation Manager UI", () => {
  test("citations tab loads with add form", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Citations").first().click();
    await expect(page.getByRole("heading", { name: "Citation Manager" })).toBeVisible();
  });
});

test.describe("AI Chat UI", () => {
  // The AI assistant is opened via the "✨ Glossa AI" sidebar button (not a tab).
  // The panel shows "Glossa AI" + "Research assistant" text — no role=heading.

  test("Glossa AI panel opens with chat textarea", async ({ page }) => {
    await page.goto("/");
    // Open via the sidebar button (title toggles between Open/Close)
    await page.getByTitle(/Open AI assistant/i).first().click();
    // Panel header shows "Glossa AI"
    await expect(page.getByText("Glossa AI").first()).toBeVisible();
    // Sub-header shows "Research assistant"
    await expect(page.getByText("Research assistant")).toBeVisible();
    // Chat input textarea is present
    await expect(page.locator("textarea").first()).toBeVisible();
  });

  test("Glossa AI panel shows starter prompt buttons", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle(/Open AI assistant/i).first().click();
    // Starter prompts: "What experiments should I run?", "Explain the Ventris method", etc.
    await expect(page.getByText(/Ventris/i)).toBeVisible({ timeout: 3000 });
  });

  test("Glossa AI panel has Research context button", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle(/Open AI assistant/i).first().click();
    // Context is auto-inferred from active view.
    // The only manual context override is the \"🔬 Research\" button.
    await expect(
      page.locator("button").filter({ hasText: /Research/ }).first()
    ).toBeVisible({ timeout: 3000 });
  });
});

test.describe("AI Tools UI", () => {
  test("AI Tools tab shows tool sections", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("AI Tools").first().click();
    await expect(page.getByRole("heading", { name: /AI Research Tools/i })).toBeVisible();
    await expect(page.getByText(/Decipherment/i)).toBeVisible();
    await expect(page.getByText(/Draft Paper/i)).toBeVisible();
  });
});

test.describe("Sign Dictionary UI", () => {
  test("signs tab shows dictionary grid", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Signs").first().click();
    await expect(page.getByRole("heading", { name: "Sign Dictionary" })).toBeVisible();
    // Should show sign IDs like 740
    await expect(page.getByText("740")).toBeVisible({ timeout: 3000 });
  });

  test("sign search filters results", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Signs").first().click();
    await page.getByPlaceholder(/Search sign ID/i).fill("fish");
    await expect(page.getByText(/fish/i).first()).toBeVisible({ timeout: 2000 });
  });
});

test.describe("Timeline UI", () => {
  test("timeline tab loads", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Timeline").first().click();
    await expect(page.getByRole("heading", { name: "Timeline" })).toBeVisible();
  });
});

test.describe("Command Palette", () => {
  test("opens on Ctrl+K", async ({ page }) => {
    await page.goto("/");
    await page.keyboard.press("Control+k");
    await expect(page.getByPlaceholder(/Search commands/i)).toBeVisible({ timeout: 2000 });
  });

  test("closes on Escape", async ({ page }) => {
    await page.goto("/");
    await page.keyboard.press("Control+k");
    await page.getByPlaceholder(/Search commands/i).waitFor();
    await page.keyboard.press("Escape");
    await expect(page.getByPlaceholder(/Search commands/i)).not.toBeVisible({ timeout: 2000 });
  });

  test("filtering by query shows relevant commands", async ({ page }) => {
    await page.goto("/");
    await page.keyboard.press("Control+k");
    await page.getByPlaceholder(/Search commands/i).fill("Entropy");
    await expect(page.getByText(/Go to Entropy/i)).toBeVisible({ timeout: 2000 });
  });

  test("clicking ⌘K button opens palette", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle(/Command palette/i).click();
    await expect(page.getByPlaceholder(/Search commands/i)).toBeVisible({ timeout: 2000 });
  });

  test("palette header can be dragged without going off-screen", async ({ page }) => {
    await page.goto("/");
    await page.keyboard.press("Control+k");
    const header = page.locator("div[style*='cursor: grab']").first();
    await header.waitFor();
    const headerBox = await header.boundingBox();
    if (!headerBox) return;
    // Drag slightly right
    await page.mouse.move(headerBox.x + 10, headerBox.y + 10);
    await page.mouse.down();
    await page.mouse.move(headerBox.x + 50, headerBox.y + 30);
    await page.mouse.up();
    // Palette should still be visible
    await expect(page.getByPlaceholder(/Search commands/i)).toBeVisible();
  });
});

test.describe("Settings - Ollama", () => {
  test("settings tab shows Ollama section", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Settings").first().click();
    await page.waitForTimeout(500);
    await expect(page.getByText(/Ollama/i).first()).toBeVisible();
    await expect(page.getByText(/Local AI Models/i)).toBeVisible();
  });

  test("Ollama section shows model library", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Settings").first().click();
    await page.waitForTimeout(1500);
    await expect(page.getByText(/Model Library/i)).toBeVisible({ timeout: 5000 });
  });

  test("Ollama section shows GPU recommendation", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Settings").first().click();
    await page.waitForTimeout(2000);
    // Either shows recommendation or "not running" message
    const hasRec = await page.getByText(/GPU.*Recommendation/i).count() > 0;
    const hasNotRunning = await page.getByText(/not running/i).count() > 0;
    expect(hasRec || hasNotRunning).toBeTruthy();
  });
});

test.describe("Status view - system metrics", () => {
  test("status page shows system metrics sections", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Status").first().click();
    await page.waitForTimeout(2000);
    // Should show CPU, Memory, Disk, Network sections
    await expect(page.getByText(/CPU/i).first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/Memory/i).first()).toBeVisible({ timeout: 5000 });
  });

  test("status page shows Clear Peaks button", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Status").first().click();
    await expect(page.getByRole("button", { name: /Clear Peaks/i })).toBeVisible({ timeout: 3000 });
  });

  test("Clear Peaks button is clickable", async ({ page }) => {
    await page.goto("/");
    await page.getByTitle("Status").first().click();
    await page.waitForTimeout(500);
    const btn = page.getByRole("button", { name: /Clear Peaks/i });
    await btn.waitFor({ timeout: 5000 });
    await btn.click();
    // Should not throw; backend will respond
    await page.waitForTimeout(500);
  });
});
