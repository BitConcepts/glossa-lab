/**
 * Playwright backend integration config.
 * Runs tests directly against the backend on port 8001.
 *
 * Usage: npx playwright test --config=playwright.backend.config.ts
 *
 * Requires backend to be running:
 *   Use the tray "Restart Service" or: pythonw -m uvicorn glossa_lab.main:app --port 8001
 */
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  testMatch: ["**/backend-integration.spec.ts"],
  fullyParallel: false,
  retries: 1,
  workers: 1,
  reporter: "list",
  use: {
    baseURL: "http://localhost:8001",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    actionTimeout: 20_000,
    navigationTimeout: 30_000,
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],
  // No webServer — backend must already be running
});
