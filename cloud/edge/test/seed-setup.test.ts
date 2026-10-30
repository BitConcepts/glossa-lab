// T017 — the operator seed script (scripts/seed-setup.mjs).
//
// Runs the script in --dry-run mode (SQL written to a temp file
// instead of executed against D1) and asserts the guarantees:
//   - it creates NO user (the SQL contains no INSERT at all);
//   - the SQL stores ONLY the code's SHA-256 hash, never the code;
//   - the guarded UPDATE carries the glassbreak seed record and
//     refuses to reopen a completed setup (completed_at IS NULL);
//   - the plaintext code is printed exactly once, with the
//     production /setup URL.

import { describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const EDGE_DIR = join(dirname(fileURLToPath(import.meta.url)), "..");
const SCRIPT = join(EDGE_DIR, "scripts", "seed-setup.mjs");

describe("seed-setup.mjs (T017)", () => {
  it("seeds hash-only state + the glassbreak record, prints the code once with the production URL", () => {
    const dir = mkdtempSync(join(tmpdir(), "glossa-seed-test-"));
    const sqlPath = join(dir, "seed.sql");
    try {
      const stdout = execFileSync(
        "node",
        [SCRIPT, "--dry-run", "--sql-out", sqlPath],
        { encoding: "utf8" },
      );
      const lines = stdout.trim().split("\n");
      const code = lines[1];
      expect(code).toBeTruthy();
      expect(code.length).toBeGreaterThanOrEqual(22); // 32 bytes base64url
      // Printed exactly once, alongside the production setup URL.
      expect(stdout.split(code).length - 1).toBe(1);
      expect(stdout).toContain("https://glossa.bitconcepts.tech/setup");

      const sql = readFileSync(sqlPath, "utf8");
      const expectedHash = createHash("sha256").update(code, "utf8").digest("hex");
      expect(sql).toContain(expectedHash);
      expect(sql).not.toContain(code);
      expect(sql).toContain("UPDATE setup_state");
      expect(sql).not.toMatch(/INSERT/i);
      expect(sql).not.toMatch(/INTO users/i);
      expect(sql).toContain("glassbreak");
      expect(sql).toContain("tristen.pierson@gmail.com");
      expect(sql).toContain("completed_at IS NULL");
      // 24-hour expiry: the printed expiry is ~24h out.
      const expiryText = lines[0].match(/expires (.+)\)/)?.[1];
      expect(expiryText).toBeTruthy();
      const deltaMs = new Date(expiryText!).getTime() - Date.now();
      expect(deltaMs).toBeGreaterThan(23 * 60 * 60 * 1000);
      expect(deltaMs).toBeLessThan(25 * 60 * 60 * 1000);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("two runs generate different codes (CSPRNG)", () => {
    const dir = mkdtempSync(join(tmpdir(), "glossa-seed-test-"));
    try {
      const run = () =>
        execFileSync("node", [SCRIPT, "--dry-run", "--sql-out", join(dir, "s.sql")], {
          encoding: "utf8",
        }).trim().split("\n")[1];
      expect(run()).not.toBe(run());
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
