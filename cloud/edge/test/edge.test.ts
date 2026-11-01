// Perimeter tests for the Glossa edge Worker (Spec 083, T009).
//
// Covers the Phase 1 claims the edge owns:
//   - C083-7: X-Robots-Tag: noindex, nofollow on EVERY response class
//     (200 pass-through, 401, 404, 500, redirect), robots.txt content.
//   - C083-4 / Amendment 2: the anonymous surface is exactly the public
//     routes; everything else 401s (API) or redirects to /login
//     (pages); forged/expired sessions are exactly anonymous.
//   - FR-011 / FR-008: identity headers are injected on authenticated
//     forwards, client-supplied X-Glossa-* headers never survive, and
//     the service credential rides container-bound requests only.

import { describe, expect, it, vi } from "vitest";
import { FRONT_INSTANCE_NAME, ROBOTS_TXT, handleRequest } from "../src/worker";
import { D1SessionStore, type SessionIdentity, type SessionStore } from "../src/session-store";
import { sha256Hex } from "../src/session";
import { classifyRoute } from "../src/routes";
import type { Env } from "../src/types";

const HOST = "https://glossa.bitconcepts.tech";
const SERVICE_CREDENTIAL = "test-only-service-credential";

const IDENTITY: SessionIdentity = {
  userId: "usr_0001",
  username: "glassbreak",
  globalType: "owner",
  workspaceRoles: { ws_indus: "owner", ws_other: "viewer" },
};

class FakeStore implements SessionStore {
  seenHashes: string[] = [];
  touchedHashes: string[] = [];
  constructor(private readonly identity: SessionIdentity | null) {}
  async findIdentityByTokenHash(tokenHash: string): Promise<SessionIdentity | null> {
    this.seenHashes.push(tokenHash);
    return this.identity;
  }
  async touchSession(tokenHash: string): Promise<void> {
    this.touchedHashes.push(tokenHash);
  }
}

function makeCtx() {
  const pending: Promise<unknown>[] = [];
  const ctx = {
    waitUntil: (p: Promise<unknown>) => pending.push(p),
    passThroughOnException: () => undefined,
  } as unknown as ExecutionContext;
  return { ctx, pending };
}

function makeEnv(frontFetch: (req: Request) => Promise<Response> | Response) {
  const names: string[] = [];
  const env = {
    DB: {} as D1Database,
    DATASETS: {} as R2Bucket,
    SERVICE_CREDENTIAL,
    GLOSSA_FRONT: {
      getByName: (name: string) => {
        names.push(name);
        return { fetch: frontFetch };
      },
    } as unknown as DurableObjectNamespace,
  } as Env;
  return { env, names };
}

function req(path: string, init: RequestInit = {}): Request {
  return new Request(`${HOST}${path}`, init);
}

function authedReq(path: string, init: RequestInit = {}): Request {
  const headers = new Headers(init.headers);
  headers.set("Cookie", "glossa_session=opaque-token-value");
  return req(path, { ...init, headers });
}

function expectNoindex(res: Response) {
  expect(res.headers.get("X-Robots-Tag")).toBe("noindex, nofollow");
}

describe("robots.txt (C083-7)", () => {
  it("serves a disallow-all robots.txt from the edge itself", async () => {
    const front = vi.fn(async () => new Response("must not be called"));
    const { env } = makeEnv(front);
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/robots.txt"), env, ctx, {
      store: new FakeStore(null),
    });
    expect(res.status).toBe(200);
    expect(await res.text()).toBe("User-agent: *\nDisallow: /\n");
    expect(ROBOTS_TXT).toContain("Disallow: /");
    expect(res.headers.get("Content-Type")).toContain("text/plain");
    expectNoindex(res);
    expect(front).not.toHaveBeenCalled();
  });
});

describe("noindex header on every response class (C083-7)", () => {
  it("200 pass-through (authenticated API request)", async () => {
    const { env } = makeEnv(async () => new Response("ok", { status: 200 }));
    const { ctx } = makeCtx();
    const res = await handleRequest(authedReq("/api/status"), env, ctx, {
      store: new FakeStore(IDENTITY),
    });
    expect(res.status).toBe(200);
    expectNoindex(res);
  });

  it("401 (anonymous API request)", async () => {
    const { env } = makeEnv(async () => new Response("unreachable"));
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/api/claims"), env, ctx, {
      store: new FakeStore(null),
    });
    expect(res.status).toBe(401);
    expectNoindex(res);
  });

  it("404 (container's own 404, authenticated)", async () => {
    const { env } = makeEnv(
      async () => new Response("nope", { status: 404 }),
    );
    const { ctx } = makeCtx();
    const res = await handleRequest(authedReq("/api/no-such-thing"), env, ctx, {
      store: new FakeStore(IDENTITY),
    });
    expect(res.status).toBe(404);
    expectNoindex(res);
  });

  it("500 (front stub throws)", async () => {
    const { env } = makeEnv(async () => {
      throw new Error("container unreachable");
    });
    const { ctx } = makeCtx();
    const res = await handleRequest(authedReq("/api/status"), env, ctx, {
      store: new FakeStore(IDENTITY),
    });
    expect(res.status).toBe(500);
    expectNoindex(res);
  });

  it("500 (session store throws)", async () => {
    const broken: SessionStore = {
      findIdentityByTokenHash: async () => {
        throw new Error("D1 unavailable");
      },
      touchSession: async () => undefined,
    };
    const { env } = makeEnv(async () => new Response("unreachable"));
    const { ctx } = makeCtx();
    const res = await handleRequest(authedReq("/api/status"), env, ctx, {
      store: broken,
    });
    expect(res.status).toBe(500);
    expectNoindex(res);
  });

  it("redirect (anonymous page request)", async () => {
    const { env } = makeEnv(async () => new Response("unreachable"));
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/claims"), env, ctx, {
      store: new FakeStore(null),
    });
    expect(res.status).toBe(302);
    expectNoindex(res);
  });

  it("overwrites a container-set X-Robots-Tag (perimeter cannot be weakened from inside)", async () => {
    const { env } = makeEnv(
      async () =>
        new Response("ok", {
          status: 200,
          headers: { "X-Robots-Tag": "index, follow" },
        }),
    );
    const { ctx } = makeCtx();
    const res = await handleRequest(authedReq("/api/status"), env, ctx, {
      store: new FakeStore(IDENTITY),
    });
    expect(res.headers.get("X-Robots-Tag")).toBe("noindex, nofollow");
  });
});

describe("anonymous gating (C083-4, Amendment 2)", () => {
  it("public pages are forwarded anonymously: /login, /setup, /invite/<code>", async () => {
    for (const path of ["/login", "/setup", "/invite/abc123", "/invite"]) {
      const seen: Request[] = [];
      const { env } = makeEnv(async (r) => {
        seen.push(r);
        return new Response("shell", { status: 200 });
      });
      const { ctx } = makeCtx();
      const res = await handleRequest(req(path), env, ctx, {
        store: new FakeStore(null),
      });
      expect(res.status).toBe(200);
      expect(seen).toHaveLength(1);
      // Anonymous forward: service credential present, identity absent.
      expect(seen[0].headers.get("X-Glossa-Service-Credential")).toBe(
        SERVICE_CREDENTIAL,
      );
      expect(seen[0].headers.get("X-Glossa-User-Id")).toBeNull();
    }
  });

  it("SPA shell assets are forwarded anonymously", async () => {
    for (const path of ["/assets/index-abc123.js", "/assets/app.css", "/favicon.ico"]) {
      const front = vi.fn(async () => new Response("asset", { status: 200 }));
      const { env } = makeEnv(front);
      const { ctx } = makeCtx();
      const res = await handleRequest(req(path), env, ctx, {
        store: new FakeStore(null),
      });
      expect(res.status).toBe(200);
      expect(front).toHaveBeenCalledTimes(1);
    }
  });

  it("anonymous API requests get 401 JSON and never reach the front", async () => {
    const front = vi.fn(async () => new Response("must not be called"));
    const { env } = makeEnv(front);
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/api/claims"), env, ctx, {
      store: new FakeStore(null),
    });
    expect(res.status).toBe(401);
    const body = (await res.json()) as { error: { code: string } };
    expect(body.error.code).toBe("authentication_required");
    expect(front).not.toHaveBeenCalled();
  });

  it("anonymous page requests redirect to /login with a next parameter", async () => {
    const front = vi.fn(async () => new Response("must not be called"));
    const { env } = makeEnv(front);
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/workspaces/indus/claims?x=1"), env, ctx, {
      store: new FakeStore(null),
    });
    expect(res.status).toBe(302);
    expect(res.headers.get("Location")).toBe(
      `/login?next=${encodeURIComponent("/workspaces/indus/claims?x=1")}`,
    );
    expect(front).not.toHaveBeenCalled();
  });

  it("anonymous non-GET page requests get 401, not a redirect", async () => {
    const { env } = makeEnv(async () => new Response("must not be called"));
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/claims", { method: "POST" }), env, ctx, {
      store: new FakeStore(null),
    });
    expect(res.status).toBe(401);
  });

  it("a forged session cookie is exactly anonymous", async () => {
    const front = vi.fn(async () => new Response("must not be called"));
    const { env } = makeEnv(front);
    const { ctx } = makeCtx();
    const store = new FakeStore(null); // D1 finds no such token hash
    const res = await handleRequest(
      req("/api/claims", { headers: { Cookie: "glossa_session=forged-value" } }),
      env,
      ctx,
      { store },
    );
    expect(res.status).toBe(401);
    expect(front).not.toHaveBeenCalled();
    // The lookup was by hash, never by the presented plaintext.
    expect(store.seenHashes).toEqual([await sha256Hex("forged-value")]);
  });

  it("the root path is a gated page for anonymous requests", async () => {
    const { env } = makeEnv(async () => new Response("must not be called"));
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/"), env, ctx, {
      store: new FakeStore(null),
    });
    expect(res.status).toBe(302);
    expect(res.headers.get("Location")).toContain("/login");
  });
});

describe("authenticated forwarding + header contract (FR-011, FR-008)", () => {
  it("injects the identity headers and routes via the single named instance", async () => {
    const seen: Request[] = [];
    const { env, names } = makeEnv(async (r) => {
      seen.push(r);
      return new Response("ok");
    });
    const { ctx, pending } = makeCtx();
    const store = new FakeStore(IDENTITY);
    const res = await handleRequest(authedReq("/api/claims"), env, ctx, { store });
    expect(res.status).toBe(200);
    expect(names).toEqual([FRONT_INSTANCE_NAME]);
    const fwd = seen[0];
    expect(fwd.headers.get("X-Glossa-User-Id")).toBe("usr_0001");
    expect(fwd.headers.get("X-Glossa-User-Name")).toBe("glassbreak");
    expect(fwd.headers.get("X-Glossa-Global-Type")).toBe("owner");
    expect(JSON.parse(fwd.headers.get("X-Glossa-Workspace-Roles")!)).toEqual({
      ws_indus: "owner",
      ws_other: "viewer",
    });
    expect(fwd.headers.get("X-Glossa-Service-Credential")).toBe(SERVICE_CREDENTIAL);
    // Activity stamp was scheduled with the token hash.
    await Promise.all(pending);
    expect(store.touchedHashes).toEqual([await sha256Hex("opaque-token-value")]);
  });

  it("client-supplied X-Glossa-* headers never survive forwarding", async () => {
    const seen: Request[] = [];
    const { env } = makeEnv(async (r) => {
      seen.push(r);
      return new Response("shell");
    });
    const { ctx } = makeCtx();
    const spoof = req("/login", {
      headers: {
        "X-Glossa-User-Id": "usr_attacker",
        "X-Glossa-Global-Type": "owner",
        "X-Glossa-Service-Credential": "guessed",
      },
    });
    await handleRequest(spoof, env, ctx, { store: new FakeStore(null) });
    const fwd = seen[0];
    expect(fwd.headers.get("X-Glossa-User-Id")).toBeNull();
    expect(fwd.headers.get("X-Glossa-Global-Type")).toBeNull();
    expect(fwd.headers.get("X-Glossa-Service-Credential")).toBe(SERVICE_CREDENTIAL);
  });

  it("the service credential never appears on edge-generated responses", async () => {
    const { env } = makeEnv(async () => new Response("unreachable"));
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/api/claims"), env, ctx, {
      store: new FakeStore(null),
    });
    expect(res.headers.get("X-Glossa-Service-Credential")).toBeNull();
    expect(await res.text()).not.toContain(SERVICE_CREDENTIAL);
  });

  it("authenticated page requests are forwarded, not redirected", async () => {
    const front = vi.fn(async () => new Response("app", { status: 200 }));
    const { env } = makeEnv(front);
    const { ctx } = makeCtx();
    const res = await handleRequest(authedReq("/claims"), env, ctx, {
      store: new FakeStore(IDENTITY),
    });
    expect(res.status).toBe(200);
    expect(front).toHaveBeenCalledTimes(1);
  });

  it("no session cookie at all: the store is never consulted", async () => {
    const store = new FakeStore(IDENTITY);
    const { env } = makeEnv(async () => new Response("unreachable"));
    const { ctx } = makeCtx();
    const res = await handleRequest(req("/api/claims"), env, ctx, { store });
    expect(res.status).toBe(401);
    expect(store.seenHashes).toEqual([]);
  });
});

describe("classifyRoute", () => {
  it("classifies the surface exactly", () => {
    expect(classifyRoute("/robots.txt")).toBe("robots");
    expect(classifyRoute("/login")).toBe("public-page");
    expect(classifyRoute("/setup")).toBe("public-page");
    expect(classifyRoute("/invite/xyz")).toBe("public-page");
    expect(classifyRoute("/assets/a.js")).toBe("public-asset");
    expect(classifyRoute("/styles.css")).toBe("public-asset");
    expect(classifyRoute("/api")).toBe("api");
    expect(classifyRoute("/api/claims")).toBe("api");
    expect(classifyRoute("/")).toBe("page");
    expect(classifyRoute("/claims")).toBe("page");
    // Data formats are not public assets.
    expect(classifyRoute("/export.json")).toBe("page");
    expect(classifyRoute("/apiary")).toBe("page");
  });
});

describe("D1SessionStore (against a fake D1)", () => {
  class FakeStatement {
    args: unknown[] = [];
    constructor(
      private readonly db: FakeD1,
      readonly sql: string,
    ) {}
    bind(...args: unknown[]) {
      this.args = args;
      return this;
    }
    async first<T>() {
      return this.db.firstResult as T;
    }
    async all<T>() {
      return { results: this.db.allResults as T[] };
    }
    async run() {
      this.db.runs.push({ sql: this.sql, args: this.args });
      return { success: true, meta: {} };
    }
  }
  class FakeD1 {
    firstResult: unknown = null;
    allResults: unknown[] = [];
    statements: FakeStatement[] = [];
    runs: { sql: string; args: unknown[] }[] = [];
    prepare(sql: string) {
      const stmt = new FakeStatement(this, sql);
      this.statements.push(stmt);
      return stmt;
    }
  }

  it("resolves identity + workspace roles from the token hash", async () => {
    const db = new FakeD1();
    db.firstResult = {
      user_id: "usr_0001",
      username: "glassbreak",
      global_type: "owner",
    };
    db.allResults = [
      { workspace_id: "ws_indus", role: "owner" },
      { workspace_id: "ws_other", role: "viewer" },
    ];
    const store = new D1SessionStore(db as unknown as D1Database);
    const now = new Date("2026-10-30T12:00:00.000Z");
    const identity = await store.findIdentityByTokenHash("deadbeef", now);
    expect(identity).toEqual({
      userId: "usr_0001",
      username: "glassbreak",
      globalType: "owner",
      workspaceRoles: { ws_indus: "owner", ws_other: "viewer" },
    });
    const lookup = db.statements[0];
    expect(lookup.sql).toContain("s.token_hash = ?");
    expect(lookup.sql).toContain("s.revoked_at IS NULL");
    expect(lookup.sql).toContain("s.expires_at > ?");
    expect(lookup.sql).toContain("u.status = 'active'");
    expect(lookup.sql).toContain("u.removed_at IS NULL");
    expect(lookup.args).toEqual(["deadbeef", "2026-10-30T12:00:00.000Z"]);
  });

  it("returns null when no live session matches", async () => {
    const db = new FakeD1();
    db.firstResult = null;
    const store = new D1SessionStore(db as unknown as D1Database);
    await expect(
      store.findIdentityByTokenHash("nope", new Date()),
    ).resolves.toBeNull();
  });

  it("touchSession stamps last_seen_at and never touches the audit log", async () => {
    const db = new FakeD1();
    const store = new D1SessionStore(db as unknown as D1Database);
    await store.touchSession("deadbeef", new Date("2026-10-30T12:00:00.000Z"));
    expect(db.runs).toHaveLength(1);
    expect(db.runs[0].sql).toContain("UPDATE sessions SET last_seen_at");
    expect(db.runs[0].sql).not.toContain("audit_log");
  });
});
