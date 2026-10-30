// Static guards over the Step 1 artifacts (Spec 083, T010 / T012):
//   - the D1 migrations keep secrets hash-only and the audit log
//     structurally append-only;
//   - the deployment configuration is production-only (Amendment 2):
//     exactly one hostname, one container instance, and no second
//     standing environment anywhere in the shipped config files.
//     (The banned word is assembled at runtime so this guard file does
//     not itself trip the rule it enforces.)

import { describe, expect, it } from "vitest";
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const EDGE_DIR = join(dirname(fileURLToPath(import.meta.url)), "..");
const REPO_ROOT = join(EDGE_DIR, "..", "..");

function read(path: string): string {
  return readFileSync(path, "utf8");
}

const migrationFiles = readdirSync(join(EDGE_DIR, "migrations"))
  .filter((f) => f.endsWith(".sql"))
  .sort();
const allSql = migrationFiles.map((f) => read(join(EDGE_DIR, "migrations", f))).join("\n");

describe("D1 migrations (T010)", () => {
  it("are numbered and cover every required table", () => {
    expect(migrationFiles).toEqual([
      "0001_identity_core.sql",
      "0002_invites_sessions.sql",
      "0003_workspaces_audit.sql",
    ]);
    for (const table of [
      "users",
      "invites",
      "sessions",
      "workspaces",
      "workspace_roles",
      "audit_log",
      "setup_state",
    ]) {
      expect(allSql).toContain(`CREATE TABLE ${table}`);
    }
  });

  it("keep secrets hash-only: no plaintext code/token/password columns", () => {
    expect(allSql).toContain("code_hash");
    expect(allSql).toContain("token_hash");
    expect(allSql).toContain("password_hash");
    expect(allSql).toContain("setup_code_hash");
    // A bare `code TEXT` / `token TEXT` column would be plaintext storage.
    expect(allSql).not.toMatch(/^\s*code\s+TEXT/im);
    expect(allSql).not.toMatch(/^\s*token\s+TEXT/im);
  });

  it("encode the Amendment 1 enums", () => {
    expect(allSql).toContain("('owner', 'admin', 'member', 'guest')");
    expect(allSql).toContain("('owner', 'admin', 'member', 'viewer')");
    expect(allSql).toContain("UNIQUE"); // username + slug + hashes
    expect(allSql).toContain("PRIMARY KEY (user_id, workspace_id)");
  });

  it("make audit_log structurally append-only", () => {
    expect(allSql).toContain("BEFORE UPDATE ON audit_log");
    expect(allSql).toContain("BEFORE DELETE ON audit_log");
    expect(allSql).toContain("RAISE(ABORT");
  });
});

describe("production-only configuration (T012, Amendment 2)", () => {
  const banned = ["stag", "ing"].join("");

  function expectNoBannedWord(path: string) {
    expect(read(path).toLowerCase()).not.toContain(banned);
  }

  it("no banned environment word in any shipped config or source file", () => {
    expectNoBannedWord(join(EDGE_DIR, "wrangler.toml"));
    expectNoBannedWord(join(EDGE_DIR, "README.md"));
    expectNoBannedWord(join(REPO_ROOT, "cloud", "docker-compose.yml"));
    expectNoBannedWord(join(REPO_ROOT, "cloud", "README.md"));
    expectNoBannedWord(
      join(REPO_ROOT, ".github", "workflows", "deploy-cloud.yml"),
    );
    for (const f of readdirSync(join(EDGE_DIR, "src"))) {
      expectNoBannedWord(join(EDGE_DIR, "src", f));
    }
    for (const f of migrationFiles) {
      expectNoBannedWord(join(EDGE_DIR, "migrations", f));
    }
  });

  it("wrangler.toml carries the production shape", () => {
    const toml = read(join(EDGE_DIR, "wrangler.toml"));
    expect(toml).toContain('name = "glossa-edge"');
    expect(toml).toContain('pattern = "glossa.bitconcepts.tech"');
    expect(toml).toContain("custom_domain = true");
    expect(toml).toContain('database_name = "glossa-identity"');
    expect(toml).toContain('bucket_name = "glossa-datasets"');
    expect(toml).toContain('class_name = "GlossaFront"');
    expect(toml).toContain('image = "../../Dockerfile"');
    expect(toml).toContain("max_instances = 1");
    // No environment sections: one deployment only.
    expect(toml).not.toMatch(/\[env\./);
  });
});
