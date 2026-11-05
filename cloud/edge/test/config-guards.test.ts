// Static guards over the Step 1 artifacts (Spec 083, T010 / T012):
//   - the D1 migrations keep secrets hash-only and the audit log
//     structurally append-only;
//   - the deployment configuration is production-only (Amendment 2):
//     exactly one hostname, one origin, and no second standing
//     environment anywhere in the shipped config files.
//     (The banned word is assembled at runtime so this guard file does
//     not itself trip the rule it enforces.)
//   - Amendment 5 (T055 / T058): the production origin is the desktop
//     reached through the GLOSSA_ORIGIN Workers VPC binding; the
//     container, Durable Object front, and R2 bundle store have no
//     production role and must not reappear in the shipped config.

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
      "0004_setup_seed_and_username_case.sql",
      "0005_workspace_description.sql",
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
    // No environment sections: one deployment only.
    expect(toml).not.toMatch(/\[env\./);
  });

  it("wrangler.toml's origin is the VPC binding, never a tunnel hostname (T055)", () => {
    const toml = read(join(EDGE_DIR, "wrangler.toml"));
    expect(toml).toContain("[[vpc_services]]");
    expect(toml).toContain('binding = "GLOSSA_ORIGIN"');
    // The tunnel publishes no route: its hostname pattern must never
    // appear as an origin or DNS target in the shipped config.
    expect(toml).not.toContain("cfargotunnel.com");
  });
});

describe("bundle production path retired (T058, Amendment 5)", () => {
  it("no bundle store, container, or front in the production wrangler config", () => {
    const toml = read(join(EDGE_DIR, "wrangler.toml"));
    expect(toml).not.toContain("[[r2_buckets]]");
    expect(toml).not.toContain("[[containers]]");
    expect(toml).not.toContain("durable_objects");
    expect(toml).not.toContain("GlossaFront");
    expect(toml).not.toContain("glossa-datasets");
  });

  it("the edge source carries no retired binding", () => {
    for (const f of readdirSync(join(EDGE_DIR, "src"))) {
      const src = read(join(EDGE_DIR, "src", f));
      expect(src).not.toContain("DATASETS");
      expect(src).not.toContain("GLOSSA_FRONT");
      expect(src).not.toContain("@cloudflare/containers");
    }
  });

  it("the deploy workflow has no bundle publish or container leg", () => {
    const wf = read(
      join(REPO_ROOT, ".github", "workflows", "deploy-cloud.yml"),
    );
    expect(wf).not.toContain("wrangler r2");
    expect(wf).not.toMatch(/publish.*bundle/i);
    expect(wf).not.toMatch(/docker build/i);
  });
});
