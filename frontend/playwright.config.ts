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
    baseURL: "http://localhost:5173",
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
   * Start the Vite dev server before running tests.
   * The backend must be started separately (shell.cmd run or setup-os.cmd start).
   * Tests tolerate the backend being down; they check both connected and
   * disconnected states.
   */
  webServer: {
    command: "npm run dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
    timeout: 20_000,
    stdout: "ignore",
    stderr: "pipe",
  },
});
