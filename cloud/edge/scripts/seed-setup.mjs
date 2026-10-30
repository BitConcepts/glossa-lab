#!/usr/bin/env node
// Glassbreak setup seed step (Spec 083, T017 / FR-003, Amendment 3).
//
// Generates a one-time setup code (CSPRNG, 32 bytes), stores ONLY its
// SHA-256 hash + a 24-hour expiry in D1 `setup_state`, together with
// the seed record for the account /setup will create:
//
//     username  glassbreak
//     email     tristen.pierson@gmail.com
//
// It creates NO user. The plaintext code is printed to this terminal
// exactly once, with the production URL — never written to a file,
// git, email, or a log. The SQL it executes contains only the hash.
//
// Usage (from cloud/edge/):
//   node scripts/seed-setup.mjs              # local D1 (wrangler dev persistence)
//   node scripts/seed-setup.mjs --remote     # production D1
//   node scripts/seed-setup.mjs --dry-run --sql-out <path>
//                                            # write the SQL instead of
//                                            # executing it (tests/debug)
//
// Local execution goes through `wrangler d1 execute --local --file`,
// i.e. the same local D1 persistence `wrangler dev` uses, so the
// local production-shaped build sees the seeded state. Production is
// the same command with --remote against the deployed database.
//
// The UPDATE is guarded by `completed_at IS NULL`: once setup has
// completed, seeding again changes nothing (and this script then
// refuses to print a code, because none was stored).

import { createHash, randomBytes } from "node:crypto";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

export const SEED_USERNAME = "glassbreak";
export const SEED_EMAIL = "tristen.pierson@gmail.com";
export const PRODUCTION_URL = "https://glossa.bitconcepts.tech";
export const SETUP_TTL_MS = 24 * 60 * 60 * 1000;

export function sha256Hex(value) {
  return createHash("sha256").update(value, "utf8").digest("hex");
}

export function buildSeedSql(codeHash, expiresAtIso) {
  // All interpolated values are generated/constant and quote-safe
  // (hex hash, ISO timestamp, fixed seed record); escape anyway.
  const esc = (s) => String(s).replace(/'/g, "''");
  return [
    "UPDATE setup_state",
    `SET setup_code_hash = '${esc(codeHash)}',`,
    `    setup_code_expires_at = '${esc(expiresAtIso)}',`,
    `    username = '${esc(SEED_USERNAME)}',`,
    `    email = '${esc(SEED_EMAIL)}'`,
    "WHERE id = 'singleton' AND completed_at IS NULL;",
    "",
  ].join("\n");
}

function parseArgs(argv) {
  const args = { remote: false, dryRun: false, sqlOut: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--remote") args.remote = true;
    else if (argv[i] === "--local") args.remote = false;
    else if (argv[i] === "--dry-run") args.dryRun = true;
    else if (argv[i] === "--sql-out") args.sqlOut = argv[++i];
    else throw new Error(`unknown argument: ${argv[i]}`);
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const code = randomBytes(32).toString("base64url");
  const codeHash = sha256Hex(code);
  const expiresAt = new Date(Date.now() + SETUP_TTL_MS).toISOString();
  const sql = buildSeedSql(codeHash, expiresAt);

  if (args.dryRun) {
    if (!args.sqlOut) throw new Error("--dry-run requires --sql-out <path>");
    writeFileSync(args.sqlOut, sql, "utf8");
  } else {
    const dir = mkdtempSync(join(tmpdir(), "glossa-seed-"));
    const file = join(dir, "seed.sql");
    try {
      writeFileSync(file, sql, "utf8");
      const wranglerArgs = [
        "wrangler", "d1", "execute", "glossa-identity",
        args.remote ? "--remote" : "--local",
        "--file", file, "--json",
      ];
      const result = spawnSync("npx", wranglerArgs, {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "inherit"],
      });
      if (result.status !== 0) {
        throw new Error(`wrangler d1 execute failed (exit ${result.status})`);
      }
      // Refuse to print a code that was not stored: if setup already
      // completed, the guarded UPDATE changed zero rows.
      let changes = null;
      try {
        const parsed = JSON.parse(result.stdout);
        const first = Array.isArray(parsed) ? parsed[0] : parsed;
        changes = first?.meta?.changes ?? first?.results?.meta?.changes ?? null;
      } catch {
        changes = null;
      }
      if (changes === 0) {
        console.error(
          "seed-setup: setup is already completed — no code was stored and none is printed.",
        );
        process.exit(2);
      }
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  }

  // The one and only appearance of the plaintext code: this terminal.
  console.log(`Glassbreak setup code (single-use, expires ${expiresAt}):`);
  console.log(code);
  console.log(`Open: ${PRODUCTION_URL}/setup`);
}

const isMain = process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href;
if (isMain) main();
