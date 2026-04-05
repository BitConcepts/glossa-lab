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

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: process.env.CI ? "github" : "list",

  use: {
    baseURL: "http://localhost:4173",
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
   * Locally: uses `vite preview` (serves the production build from dist/).
   *   Run `npm run build` first if dist/ is stale.
   *   Set PLAYWRIGHT_DEV=1 to use `npm run dev` instead.
   *
   * CI: controlled by the `playwright` job in ci.yml which starts the backend
   *   and sets CI=true, so reuseExistingServer=false and a fresh server starts.
   *
   * Tests tolerate the backend being down; they check both connected and
   * disconnected states.
   */
  webServer: {
    command: process.env.PLAYWRIGHT_DEV ? "npm run dev" : "npm run preview",
    url: "http://localhost:4173",
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
    stdout: "ignore",
    stderr: "pipe",
  },
});
