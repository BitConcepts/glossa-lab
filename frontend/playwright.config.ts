import { defineConfig, devices } from "@playwright/test";

/**
 * Glossa Lab Playwright configuration.
 *
 * Tests run against the Vite dev server (started automatically).
 * The backend is expected to be running separately at localhost:8000.
 * Tests that require the backend are guarded by the BACKEND_URL env variable
 * or handle the disconnected state gracefully.
 *
 * Run all tests:
 *   npx playwright test          (from frontend/)
 *   shell.cmd e2e                (from repo root)
 *
 * Run with visible browser:
 *   npx playwright test --headed
 */

// When PLAYWRIGHT_USE_BACKEND=1, the Glossa Lab backend (port 8001) serves both
// the built frontend (via StaticFiles) and the API.  This is the correct mode for CI:
// no separate Vite preview server is needed, and API calls resolve on the same origin.
const USE_BACKEND = !!process.env.PLAYWRIGHT_USE_BACKEND;
const BACKEND_URL = process.env.PLAYWRIGHT_BACKEND_URL || "http://127.0.0.1:8001";
const PREVIEW_URL = "http://localhost:4173";
const BASE_URL = USE_BACKEND ? BACKEND_URL : PREVIEW_URL;

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: process.env.CI ? "github" : "list",

  use: {
    baseURL: BASE_URL,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],

  /**
   * Start a server before running tests.
   *
   * PLAYWRIGHT_USE_BACKEND=1 (CI): re-use the already-running Glossa backend
   *   which serves the built frontend from frontend/dist/ via StaticFiles mount.
   *   API calls resolve on the same origin so no proxy is needed.
   *
   * Local (default): uses `vite preview` at port 4173. Run `npm run build` first.
   *   Set PLAYWRIGHT_DEV=1 to use `npm run dev` instead.
   */
  webServer: USE_BACKEND
    ? {
        // Backend already started externally — just wait for it to be healthy.
        command: "echo \"Using backend as server\"",
        url: BACKEND_URL + "/api/v1/health",
        reuseExistingServer: true,
        timeout: 60_000,
        stdout: "ignore",
        stderr: "ignore",
      }
    : {
        command: process.env.PLAYWRIGHT_DEV ? "npm run dev" : "npm run preview",
        url: PREVIEW_URL,
        reuseExistingServer: !process.env.CI,
        timeout: 60_000,
        stdout: "ignore",
        stderr: "pipe",
      },
});
