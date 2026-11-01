// Step 2 identity tests (Spec 083): T014–T017, T020–T022 + the plan's
// Step 2 claim-test matrix for the edge half.
//
//   - C083-1: registration without a valid code creates no account
//     and no session (form posts, code-shaped guesses, stray routes).
//   - C083-2: invite redeemed twice / expired / revoked fails the
//     second use in every case; no plaintext code in D1 rows or logs.
//   - C083-3: /setup closed (404) once an admin exists; expired or
//     replayed setup codes create nothing; setup identity comes from
//     the seed record, never the request body.
//   - C083-4: forged/expired/revoked sessions authenticate nowhere;
//     a disabled user's next request is refused, session rows gone;
//     30-day sliding lifetime extends on activity.
//   - C083-5/16/19: member → admin surface is 403 + audit-logged;
//     the workspace-access matrix reads/writes as stored; a Guest
//     granted above Viewer is refused.
//   - C083-12: audit rows exist, with actor + timestamp, for every
//     FR-012 event the edge handles.

import { describe, expect, it, vi } from "vitest";
import {
  PASSWORDS,
  T0,
  makeHarness,
  seedUser,
  seedWorkspace,
  sessionTokenFromResponse,
  sha256Hex,
  type Harness,
} from "./harness";
import { Argon2idHasher, ARGON2_PARAMS } from "../src/password";
import { D1IdentityStore } from "../src/identity-store";
import { D1SessionStore } from "../src/session-store";

const DAY = 24 * 60 * 60 * 1000;
const SETUP_CODE = "setup-code-from-seed-step-0123456789";
const SEED_EMAIL = "tristen.pierson@gmail.com";

function post(path: string, body: unknown, cookie?: string) {
  return {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    ...(cookie ? { cookie } : {}),
  };
}

async function setupOwner(h: Harness): Promise<string> {
  await seedUser(h, "glassbreak", "owner");
  return h.cookieFor("glassbreak");
}

async function seedSetupState(h: Harness, overrides: Partial<{ expiresAt: string }> = {}) {
  h.store.setup = {
    setupCodeHash: await sha256Hex(SETUP_CODE),
    setupCodeExpiresAt:
      overrides.expiresAt ?? new Date(T0.getTime() + DAY).toISOString(),
    completedAt: null,
    username: "glassbreak",
    email: SEED_EMAIL,
  };
}

async function createInvite(
  h: Harness,
  adminCookie: string,
  body: Record<string, unknown> = {},
): Promise<{ res: Response; json: any }> {
  const res = await h.call("/api/admin/invites", post("/api/admin/invites", body, adminCookie));
  return { res, json: (await res.clone().json()) as any };
}

// ---------------------------------------------------------------------------

describe("T015 / C083-1 — registration exists only as invite redemption or setup", () => {
  it("stray registration routes create no account and no session", async () => {
    const h = makeHarness();
    for (const path of [
      "/register",
      "/signup",
      "/api/register",
      "/api/signup",
      "/api/auth/register",
      "/api/users",
    ]) {
      const res = await h.call(
        path,
        post(path, { username: "mallory", password: "mallory-pass-1" }),
      );
      expect(res.status, path).not.toBe(201);
      expect(res.status, path).toBe(404);
    }
    expect(h.store.users).toHaveLength(0);
    expect(h.store.sessions).toHaveLength(0);
  });

  it("code-shaped guesses at the redeem route create nothing", async () => {
    const h = makeHarness();
    for (const guess of [
      "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
      "guessed-code-0000000000000000000000",
      "x",
    ]) {
      const res = await h.call(
        `/invite/${guess}/redeem`,
        post("", { username: "mallory", password: "mallory-pass-1" }),
      );
      expect(res.status).toBe(400);
    }
    expect(h.store.users).toHaveLength(0);
    expect(h.store.sessions).toHaveLength(0);
  });

  it("form posts to public pages and login attempts create nothing", async () => {
    const h = makeHarness();
    const form = {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "username=mallory&password=mallory-pass-1",
    };
    await h.call("/invite/some-code", form); // page post, not the redeem API
    const login = await h.call("/login", post("/login", {
      username: "mallory",
      password: "mallory-pass-1",
    }));
    expect(login.status).toBe(401);
    expect(h.store.users).toHaveLength(0);
    expect(h.store.sessions).toHaveLength(0);
  });
});

// ---------------------------------------------------------------------------

describe("T014 / C083-2 — invite lifecycle", () => {
  it("create returns the plaintext code exactly once; D1 stores only its hash", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    const logs = vi.spyOn(console, "log").mockImplementation(() => undefined);
    const { res, json } = await createInvite(h, admin);
    expect(res.status).toBe(201);
    const code = (json as { code: string }).code;
    expect(typeof code).toBe("string");
    // 24 random bytes base64url = 32 chars (>= 128-bit floor).
    expect(code.length).toBeGreaterThanOrEqual(22);
    expect((json as { invite_url: string }).invite_url).toBe(`/invite/${code}`);
    // Default expiry is 7 days.
    const invite = (json as { invite: { expires_at: string } }).invite;
    expect(invite.expires_at).toBe(new Date(T0.getTime() + 7 * DAY).toISOString());
    // Stored row: hash only.
    expect(h.store.invites).toHaveLength(1);
    expect(h.store.invites[0].codeHash).toBe(await sha256Hex(code));
    expect(JSON.stringify(h.store.invites)).not.toContain(code);
    // List view exposes neither code nor hash.
    const list = await h.call("/api/admin/invites", { cookie: admin });
    const listText = await list.text();
    expect(listText).not.toContain(code);
    expect(listText).not.toContain(h.store.invites[0].codeHash);
    // Nothing logged the code.
    const logged = logs.mock.calls.flat().join(" ");
    expect(logged).not.toContain(code);
    logs.mockRestore();
    // Audit row for the creation.
    expect(h.store.audit.some((a) => a.event === "invite_created")).toBe(true);
  });

  it("redemption creates a member, applies workspace grants, issues a session", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedWorkspace(h);
    const { json } = await createInvite(h, admin, {
      workspace_grants: { ws_indus: "member" },
    });
    const code = (json as { code: string }).code;
    const res = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "Alice", password: PASSWORDS.alice }),
    );
    expect(res.status).toBe(201);
    const body = (await res.json()) as { user: { username: string; global_type: string } };
    expect(body.user.username).toBe("alice"); // normalized lowercase
    expect(body.user.global_type).toBe("member");
    const stored = h.store.users.find((u) => u.username === "alice")!;
    expect(await h.store.getWorkspaceRoles(stored.id)).toEqual({
      ws_indus: "member",
    });
    expect(stored.passwordHash).not.toContain(PASSWORDS.alice);
    expect(h.store.invites[0].redeemedBy).toBe(stored.id);
    expect(h.store.invites[0].redeemedAt).toBe(T0.toISOString());
    // The issued session authenticates, with identity headers injected.
    const token = sessionTokenFromResponse(res);
    const api = await h.call("/api/claims", { cookie: token });
    expect(api.status).toBe(200);
    const fwd = h.frontRequests.at(-1)!;
    expect(fwd.headers.get("X-Glossa-User-Name")).toBe("alice");
    expect(fwd.headers.get("X-Glossa-Global-Type")).toBe("member");
    expect(
      h.store.audit.some(
        (a) => a.event === "invite_redeemed" && a.actorLabel === "alice" && a.ts === T0.toISOString(),
      ),
    ).toBe(true);
  });

  it("a second redemption of the same code always fails and creates nothing", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    const { json } = await createInvite(h, admin);
    const code = (json as { code: string }).code;
    const first = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "alice", password: PASSWORDS.alice }),
    );
    expect(first.status).toBe(201);
    const usersBefore = h.store.users.length;
    const sessionsBefore = h.store.sessions.length;
    const second = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "bob", password: PASSWORDS.bob }),
    );
    expect(second.status).toBe(400);
    expect(((await second.json()) as { error: { code: string } }).error.code).toBe("invite_redeemed");
    expect(h.store.users).toHaveLength(usersBefore);
    expect(h.store.sessions).toHaveLength(sessionsBefore);
  });

  it("an expired invite fails redemption and creates nothing", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    const { json } = await createInvite(h, admin, { expires_in_days: 1 });
    const code = (json as { code: string }).code;
    h.setNow(new Date(T0.getTime() + 2 * DAY));
    const res = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "alice", password: PASSWORDS.alice }),
    );
    expect(res.status).toBe(400);
    expect(((await res.json()) as { error: { code: string } }).error.code).toBe("invite_expired");
    expect(h.store.users.map((u) => u.username)).toEqual(["glassbreak"]);
    expect(h.store.sessions.filter((s) => s.userId !== "usr_glassbreak")).toHaveLength(0);
  });

  it("a revoked invite fails redemption; revocation is audited; double-revoke is refused", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    const { json } = await createInvite(h, admin);
    const inviteId = (json as { invite: { id: string } }).invite.id;
    const code = (json as { code: string }).code;
    const revoke = await h.call(
      `/api/admin/invites/${inviteId}/revoke`,
      post("", {}, admin),
    );
    expect(revoke.status).toBe(200);
    expect(h.store.audit.some((a) => a.event === "invite_revoked" && a.target === inviteId)).toBe(true);
    const res = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "alice", password: PASSWORDS.alice }),
    );
    expect(res.status).toBe(400);
    expect(((await res.json()) as { error: { code: string } }).error.code).toBe("invite_revoked");
    expect(h.store.users.map((u) => u.username)).toEqual(["glassbreak"]);
    const again = await h.call(
      `/api/admin/invites/${inviteId}/revoke`,
      post("", {}, admin),
    );
    expect(again.status).toBe(409);
  });

  it("email binding: mismatch or missing email does not spend the invite; the bound email redeems", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    const { json } = await createInvite(h, admin, { email: "invitee@example.org" });
    const code = (json as { code: string }).code;
    const wrong = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "alice", password: PASSWORDS.alice, email: "other@example.org" }),
    );
    expect(wrong.status).toBe(400);
    const missing = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "alice", password: PASSWORDS.alice }),
    );
    expect(missing.status).toBe(400);
    expect(h.store.invites[0].redeemedAt).toBeNull();
    const ok = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "alice", password: PASSWORDS.alice, email: "Invitee@Example.ORG" }),
    );
    expect(ok.status).toBe(201);
    expect(h.store.users.find((u) => u.username === "alice")?.email).toBe("invitee@example.org");
  });

  it("username rules: invalid shapes refused, case-insensitive duplicates refused, invite unspent", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    const { json } = await createInvite(h, admin);
    const code = (json as { code: string }).code;
    for (const bad of ["ab", "a".repeat(33), "white space", "bang!name", ""]) {
      const res = await h.call(
        `/invite/${code}/redeem`,
        post("", { username: bad, password: PASSWORDS.alice }),
      );
      expect(res.status, bad).toBe(400);
    }
    const taken = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "GLASSBREAK", password: PASSWORDS.alice }),
    );
    expect(taken.status).toBe(409);
    expect(h.store.invites[0].redeemedAt).toBeNull();
    expect(h.store.users).toHaveLength(1);
  });
});

// ---------------------------------------------------------------------------

describe("T016 / C083-4 — login, logout, sliding sessions, revocation", () => {
  it("login failures are indistinguishable (unknown user vs wrong password) and both are audited", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const unknown = await h.call("/login", post("/login", { username: "nosuch", password: "whatever-123" }));
    const wrong = await h.call("/login", post("/login", { username: "alice", password: "not-the-password" }));
    expect(unknown.status).toBe(401);
    expect(wrong.status).toBe(401);
    const unknownBody = await unknown.text();
    const wrongBody = await wrong.text();
    expect(unknownBody).toBe(wrongBody);
    expect(unknown.headers.get("Set-Cookie")).toBeNull();
    const failures = h.store.audit.filter((a) => a.event === "login_failure");
    expect(failures).toHaveLength(2);
    expect(failures.every((a) => a.ts === T0.toISOString() && a.actorLabel.length > 0)).toBe(true);
  });

  it("login success: opaque token hashed at rest, Phase 1 cookie shape, 30-day expiry, audited", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const res = await h.call("/login", post("/login", { username: "alice", password: PASSWORDS.alice }));
    expect(res.status).toBe(200);
    const cookie = res.headers.get("Set-Cookie")!;
    expect(cookie).toContain("HttpOnly");
    expect(cookie).toContain("Secure");
    expect(cookie).toContain("SameSite=Lax");
    expect(cookie).toContain("Max-Age=2592000");
    const token = sessionTokenFromResponse(res);
    expect(token.length).toBeGreaterThanOrEqual(43); // 32 bytes base64url
    expect(h.store.sessions).toHaveLength(1);
    const row = h.store.sessions[0];
    expect(row.tokenHash).toBe(await sha256Hex(token));
    expect(row.tokenHash).not.toBe(token);
    expect(JSON.stringify(h.store.sessions)).not.toContain(token);
    expect(row.expiresAt).toBe(new Date(T0.getTime() + 30 * DAY).toISOString());
    expect((await res.text()).length).toBeGreaterThan(0);
    expect(h.store.audit.some((a) => a.event === "login_success" && a.actorLabel === "alice")).toBe(true);
  });

  it("logout deletes the session row instantly; the token then authenticates nowhere", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const token = await h.cookieFor("alice");
    const out = await h.call("/logout", post("/logout", {}, token));
    expect(out.status).toBe(200);
    expect(out.headers.get("Set-Cookie")).toContain("Max-Age=0");
    expect(h.store.sessions).toHaveLength(0);
    expect(h.store.audit.some((a) => a.event === "logout" && a.actorLabel === "alice")).toBe(true);
    const after = await h.call("/api/claims", { cookie: token });
    expect(after.status).toBe(401);
  });

  it("sliding lifetime: activity extends expiry 30 days from last activity", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const token = await h.cookieFor("alice");
    h.setNow(new Date(T0.getTime() + 10 * DAY));
    const res = await h.call("/api/status", { cookie: token });
    expect(res.status).toBe(200);
    await h.flush();
    const row = h.store.sessions[0];
    expect(row.lastSeenAt).toBe(new Date(T0.getTime() + 10 * DAY).toISOString());
    expect(row.expiresAt).toBe(new Date(T0.getTime() + 40 * DAY).toISOString());
    // And past the extended expiry the session is dead.
    h.setNow(new Date(T0.getTime() + 41 * DAY));
    const dead = await h.call("/api/status", { cookie: token });
    expect(dead.status).toBe(401);
  });

  it("forged and expired session values authenticate nowhere", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const forged = await h.call("/api/claims", { cookie: "forged-token-value-0123456789abcdef" });
    expect(forged.status).toBe(401);
    expect(h.front).not.toHaveBeenCalled();
    const page = await h.call("/claims", { cookie: "forged-token-value-0123456789abcdef" });
    expect(page.status).toBe(302);
  });

  it("disabled user's next request is refused and their session rows are gone", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedUser(h, "alice", "member");
    const aliceToken = await h.cookieFor("alice");
    expect(h.store.sessions.some((s) => s.userId === "usr_alice")).toBe(true);
    const disable = await h.call(
      "/api/admin/users/usr_alice/disable",
      post("", {}, admin),
    );
    expect(disable.status).toBe(200);
    expect(h.store.sessions.filter((s) => s.userId === "usr_alice")).toHaveLength(0);
    expect(h.store.audit.some((a) => a.event === "user_disabled" && a.target === "usr_alice")).toBe(true);
    const next = await h.call("/api/claims", { cookie: aliceToken });
    expect(next.status).toBe(401);
    const login = await h.call("/login", post("/login", { username: "alice", password: PASSWORDS.alice }));
    expect(login.status).toBe(401);
  });

  it("removed user: row retained for attribution, sessions gone, login refused", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedUser(h, "alice", "member");
    const aliceToken = await h.cookieFor("alice");
    const remove = await h.call(
      "/api/admin/users/usr_alice/remove",
      post("", {}, admin),
    );
    expect(remove.status).toBe(200);
    const row = h.store.users.find((u) => u.username === "alice");
    expect(row).toBeDefined();
    expect(row!.removedAt).toBe(T0.toISOString());
    expect(h.store.sessions.filter((s) => s.userId === "usr_alice")).toHaveLength(0);
    expect(h.store.audit.some((a) => a.event === "user_removed")).toBe(true);
    expect((await h.call("/api/claims", { cookie: aliceToken })).status).toBe(401);
    expect(
      (await h.call("/login", post("/login", { username: "alice", password: PASSWORDS.alice }))).status,
    ).toBe(401);
  });

  it("global-type change kills the target's sessions in the same operation", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedUser(h, "alice", "member");
    const aliceToken = await h.cookieFor("alice");
    const res = await h.call("/api/admin/users/usr_alice/type", {
      ...post("", { global_type: "guest" }, admin),
    });
    expect(res.status).toBe(200);
    expect(h.store.users.find((u) => u.username === "alice")!.globalType).toBe("guest");
    expect(h.store.sessions.filter((s) => s.userId === "usr_alice")).toHaveLength(0);
    expect((await h.call("/api/claims", { cookie: aliceToken })).status).toBe(401);
    expect(
      h.store.audit.some(
        (a) => a.event === "user_type_changed" && a.detail.from === "member" && a.detail.to === "guest",
      ),
    ).toBe(true);
  });
});

// ---------------------------------------------------------------------------

describe("T017 / C083-3 — glassbreak setup", () => {
  it("setup creates the owner from the SEED record (not request input), issues a session, audits", async () => {
    const h = makeHarness();
    await seedSetupState(h);
    const res = await h.call(
      "/setup",
      post("/setup", {
        code: SETUP_CODE,
        username: "attacker-chosen-name",
        email: "attacker@example.org",
        password: "owner-chosen-pass-1",
      }),
    );
    expect(res.status).toBe(201);
    const body = (await res.json()) as { user: { username: string; email: string; global_type: string } };
    expect(body.user.username).toBe("glassbreak");
    expect(body.user.email).toBe(SEED_EMAIL);
    expect(body.user.global_type).toBe("owner");
    const stored = h.store.users[0];
    expect(stored.passwordHash).not.toContain("owner-chosen-pass-1");
    expect(h.store.setup.completedAt).toBe(T0.toISOString());
    expect(h.store.audit.some((a) => a.event === "setup_completed" && a.actorLabel === "glassbreak")).toBe(true);
    // Session works.
    const token = sessionTokenFromResponse(res);
    expect((await h.call("/api/status", { cookie: token })).status).toBe(200);
  });

  it("after setup, /setup answers 404 forever (page and API) and a replayed code creates nothing", async () => {
    const h = makeHarness();
    await seedSetupState(h);
    const first = await h.call(
      "/setup",
      post("/setup", { code: SETUP_CODE, password: "owner-chosen-pass-1" }),
    );
    expect(first.status).toBe(201);
    expect((await h.call("/setup")).status).toBe(404);
    const replay = await h.call(
      "/setup",
      post("/setup", { code: SETUP_CODE, password: "another-pass-12345" }),
    );
    expect(replay.status).toBe(404);
    expect(h.store.users).toHaveLength(1);
  });

  it("/setup is closed as soon as ANY admin exists, even if setup never completed", async () => {
    const h = makeHarness();
    await seedSetupState(h);
    await seedUser(h, "admin2", "admin");
    expect((await h.call("/setup")).status).toBe(404);
    const res = await h.call(
      "/setup",
      post("/setup", { code: SETUP_CODE, password: "owner-chosen-pass-1" }),
    );
    expect(res.status).toBe(404);
    expect(h.store.users.map((u) => u.username)).toEqual(["admin2"]);
  });

  it("an expired setup code creates nothing; a wrong code creates nothing", async () => {
    const h = makeHarness();
    await seedSetupState(h, { expiresAt: new Date(T0.getTime() - 1000).toISOString() });
    const expired = await h.call(
      "/setup",
      post("/setup", { code: SETUP_CODE, password: "owner-chosen-pass-1" }),
    );
    expect(expired.status).toBe(400);
    expect(h.store.users).toHaveLength(0);

    const h2 = makeHarness();
    await seedSetupState(h2);
    const wrong = await h2.call(
      "/setup",
      post("/setup", { code: "wrong-code-wrong-code-wrong-code", password: "owner-chosen-pass-1" }),
    );
    expect(wrong.status).toBe(400);
    expect(h2.store.users).toHaveLength(0);
    expect(h2.store.setup.completedAt).toBeNull();
  });

  it("an open /setup page is still the public page (forwarded, no data)", async () => {
    const h = makeHarness();
    await seedSetupState(h);
    const res = await h.call("/setup");
    expect(res.status).toBe(200);
    expect(h.front).toHaveBeenCalledTimes(1);
  });
});

// ---------------------------------------------------------------------------

describe("T020/T021 / C083-5,16,19 — admin API", () => {
  it("member and guest get 403 on the admin surface, audited; anonymous gets 401, audited", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    await seedUser(h, "gwen", "guest");
    const alice = await h.cookieFor("alice");
    const gwen = await h.cookieFor("gwen");
    for (const cookie of [alice, gwen]) {
      const res = await h.call("/api/admin/users", { cookie });
      expect(res.status).toBe(403);
    }
    const anon = await h.call("/api/admin/users");
    expect(anon.status).toBe(401);
    const denials = h.store.audit.filter((a) => a.event === "admin_api_denial");
    expect(denials.length).toBeGreaterThanOrEqual(3);
    expect(denials.some((a) => a.actorLabel === "alice")).toBe(true);
    expect(denials.some((a) => a.actorLabel === "gwen")).toBe(true);
  });

  it("users list/get are sanitized: no password hash anywhere", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedUser(h, "alice", "member");
    const list = await h.call("/api/admin/users", { cookie: admin });
    expect(list.status).toBe(200);
    const text = await list.text();
    expect(text).not.toContain("password_hash");
    expect(text).not.toContain("fake$");
    const get = await h.call("/api/admin/users/usr_alice", { cookie: admin });
    expect(get.status).toBe(200);
    expect(((await get.json()) as { user: { username: string } }).user.username).toBe("alice");
    expect((await h.call("/api/admin/users/usr_nope", { cookie: admin })).status).toBe(404);
  });

  it("owner type is singular: granting it is refused + recorded; removing glassbreak's is refused + recorded", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedUser(h, "alice", "member");
    const grant = await h.call(
      "/api/admin/users/usr_alice/type",
      post("", { global_type: "owner" }, admin),
    );
    expect(grant.status).toBe(409);
    expect(h.store.users.find((u) => u.username === "alice")!.globalType).toBe("member");
    const strip = await h.call(
      "/api/admin/users/usr_glassbreak/type",
      post("", { global_type: "member" }, admin),
    );
    expect(strip.status).toBe(409);
    expect(h.store.users.find((u) => u.username === "glassbreak")!.globalType).toBe("owner");
    const refused = h.store.audit.filter((a) => a.event === "user_type_change_refused");
    expect(refused).toHaveLength(2);
  });

  it("workspaces: admin creates (name → slug) and archives; member cannot", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedUser(h, "alice", "member");
    const alice = await h.cookieFor("alice");
    const denied = await h.call(
      "/api/admin/workspaces",
      post("", { name: "Nope Lab" }, alice),
    );
    expect(denied.status).toBe(403);
    const created = await h.call(
      "/api/admin/workspaces",
      post("", { name: "New Lab!" }, admin),
    );
    expect(created.status).toBe(201);
    const ws = ((await created.json()) as { workspace: { id: string; slug: string } }).workspace;
    expect(ws.slug).toBe("new-lab");
    expect(h.store.audit.some((a) => a.event === "workspace_created" && a.target === ws.id)).toBe(true);
    const dupe = await h.call(
      "/api/admin/workspaces",
      post("", { name: "New Lab!" }, admin),
    );
    expect(((await dupe.json()) as { workspace: { slug: string } }).workspace.slug).toBe("new-lab-2");
    const archived = await h.call(
      `/api/admin/workspaces/${ws.id}/archive`,
      post("", {}, admin),
    );
    expect(archived.status).toBe(200);
    expect(h.store.workspaces.find((w) => w.id === ws.id)!.archivedAt).toBe(T0.toISOString());
    expect(h.store.audit.some((a) => a.event === "workspace_archived" && a.target === ws.id)).toBe(true);
  });

  it("access matrix: GET reads as stored, PUT replaces the full set, role change kills sessions, audited", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedWorkspace(h);
    await seedWorkspace(h, "ws_other", "Other Study");
    await seedUser(h, "alice", "member");
    const aliceToken = await h.cookieFor("alice");
    const get1 = await h.call("/api/admin/users/usr_alice/workspaces", { cookie: admin });
    const matrix = (await get1.json()) as {
      workspace_roles: Record<string, string>;
      implicit_workspace_admin: boolean;
      workspaces: { id: string; role: string | null }[];
    };
    expect(matrix.workspace_roles).toEqual({});
    expect(matrix.implicit_workspace_admin).toBe(false);
    expect(matrix.workspaces.map((w) => w.role)).toEqual([null, null]);

    const put = await h.call("/api/admin/users/usr_alice/workspaces", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ workspace_roles: { ws_indus: "member", ws_other: "viewer" } }),
      cookie: admin,
    });
    expect(put.status).toBe(200);
    expect(await h.store.getWorkspaceRoles("usr_alice")).toEqual({
      ws_indus: "member",
      ws_other: "viewer",
    });
    // Role change revoked alice's sessions.
    expect(h.store.sessions.filter((s) => s.userId === "usr_alice")).toHaveLength(0);
    expect((await h.call("/api/claims", { cookie: aliceToken })).status).toBe(401);
    expect(h.store.audit.some((a) => a.event === "workspace_matrix_changed" && a.target === "usr_alice")).toBe(true);

    // PUT with an unknown workspace refuses and changes nothing.
    const bad = await h.call("/api/admin/users/usr_alice/workspaces", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ workspace_roles: { ws_ghost: "member" } }),
      cookie: admin,
    });
    expect(bad.status).toBe(400);
    expect(await h.store.getWorkspaceRoles("usr_alice")).toEqual({
      ws_indus: "member",
      ws_other: "viewer",
    });
  });

  it("Guest granted a Member workspace role is refused (Viewer cap); Viewer itself is allowed", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedWorkspace(h);
    await seedUser(h, "gwen", "guest");
    const put = (roles: Record<string, string>) =>
      h.call("/api/admin/users/usr_gwen/workspaces", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ workspace_roles: roles }),
        cookie: admin,
      });
    const refused = await put({ ws_indus: "member" });
    expect(refused.status).toBe(403);
    expect(((await refused.json()) as { error: { code: string } }).error.code).toBe("guest_viewer_cap");
    expect(await h.store.getWorkspaceRoles("usr_gwen")).toEqual({});
    const allowed = await put({ ws_indus: "viewer" });
    expect(allowed.status).toBe(200);
    expect(await h.store.getWorkspaceRoles("usr_gwen")).toEqual({ ws_indus: "viewer" });
  });

  it("global Admin/Owner implicit Workspace Admin is not stored as rows", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await seedWorkspace(h);
    const get = await h.call("/api/admin/users/usr_glassbreak/workspaces", { cookie: admin });
    const matrix = (await get.json()) as {
      workspace_roles: Record<string, string>;
      implicit_workspace_admin: boolean;
    };
    expect(matrix.implicit_workspace_admin).toBe(true);
    expect(matrix.workspace_roles).toEqual({});
    expect(await h.store.getWorkspaceRoles("usr_glassbreak")).toEqual({});
  });
});

// ---------------------------------------------------------------------------

describe("T022 / C083-12 — audit completeness at the edge", () => {
  it("container-scope denials on proxied responses are audit-logged with actor + route", async () => {
    const h = makeHarness({ frontStatus: 404 });
    await seedUser(h, "alice", "member");
    const alice = await h.cookieFor("alice");
    const res = await h.call("/api/workspaces/ws_indus/claims", { cookie: alice });
    expect(res.status).toBe(404);
    await h.flush();
    const denial = h.store.audit.find((a) => a.event === "container_scope_denial");
    expect(denial).toBeDefined();
    expect(denial!.actorLabel).toBe("alice");
    expect(denial!.actorId).toBe("usr_alice");
    expect(denial!.target).toBe("/api/workspaces/ws_indus/claims");
    expect(denial!.detail.status).toBe(404);
    expect(denial!.ts).toBe(T0.toISOString());
  });

  it("every audit row carries actor + timestamp; the store exposes no audit update/delete", async () => {
    const h = makeHarness();
    const admin = await setupOwner(h);
    await createInvite(h, admin);
    expect(h.store.audit.length).toBeGreaterThan(0);
    for (const row of h.store.audit) {
      expect(row.actorLabel.length).toBeGreaterThan(0);
      expect(row.ts).toBe(T0.toISOString());
      expect(row.id.startsWith("aud_")).toBe(true);
    }
    const store = h.store as unknown as Record<string, unknown>;
    expect(store.updateAudit).toBeUndefined();
    expect(store.deleteAudit).toBeUndefined();
  });
});

// ---------------------------------------------------------------------------

describe("Argon2id hasher (T015) — real implementation, OWASP-floor params", () => {
  it("hashes in encoded Argon2id form and verifies", async () => {
    const hasher = new Argon2idHasher();
    expect(ARGON2_PARAMS.memorySizeKiB).toBe(19456);
    expect(ARGON2_PARAMS.iterations).toBe(2);
    expect(ARGON2_PARAMS.parallelism).toBe(1);
    const encoded = await hasher.hash("a-real-password-123");
    expect(encoded.startsWith("$argon2id$v=19$m=19456,t=2,p=1$")).toBe(true);
    expect(encoded).not.toContain("a-real-password-123");
    await expect(hasher.verify("a-real-password-123", encoded)).resolves.toBe(true);
    await expect(hasher.verify("wrong-password-123", encoded)).resolves.toBe(false);
    await expect(hasher.verify("x", "not-a-hash")).resolves.toBe(false);
  });

  it("full flow with the real hasher: setup-free owner → invite → redeem → login", async () => {
    const hasher = new Argon2idHasher();
    const h = makeHarness({ hasher });
    await seedUser(h, "glassbreak", "owner", PASSWORDS.glassbreak, hasher);
    const admin = await h.cookieFor("glassbreak");
    const { json } = await createInvite(h, admin);
    const code = (json as { code: string }).code;
    const redeem = await h.call(
      `/invite/${code}/redeem`,
      post("", { username: "alice", password: PASSWORDS.alice }),
    );
    expect(redeem.status).toBe(201);
    const stored = h.store.users.find((u) => u.username === "alice")!;
    expect(stored.passwordHash.startsWith("$argon2id$")).toBe(true);
    const bad = await h.call("/login", post("/login", { username: "alice", password: "wrong-password-9" }));
    expect(bad.status).toBe(401);
    const good = await h.call("/login", post("/login", { username: "alice", password: PASSWORDS.alice }));
    expect(good.status).toBe(200);
  });
});

// ---------------------------------------------------------------------------

describe("D1IdentityStore — SQL-level gates (fake D1, Step 1 pattern)", () => {
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
      return { success: true, meta: { changes: this.db.changes } };
    }
  }
  class FakeD1 {
    firstResult: unknown = null;
    allResults: unknown[] = [];
    changes = 1;
    runs: { sql: string; args: unknown[] }[] = [];
    batches: unknown[][] = [];
    prepare(sql: string) {
      return new FakeStatement(this, sql);
    }
    async batch(stmts: unknown[]) {
      this.batches.push(stmts);
      return [];
    }
  }

  it("consumeInvite is a single conditional UPDATE (atomic check-and-consume)", async () => {
    const db = new FakeD1();
    const store = new D1IdentityStore(db as unknown as D1Database);
    await expect(store.consumeInvite("hash", "usr_x", T0.toISOString())).resolves.toBe(true);
    expect(db.runs).toHaveLength(1);
    const sql = db.runs[0].sql;
    expect(sql).toContain("UPDATE invites SET redeemed_by");
    expect(sql).toContain("redeemed_at IS NULL");
    expect(sql).toContain("revoked_at IS NULL");
    expect(sql).toContain("expires_at > ?");
    db.changes = 0;
    await expect(store.consumeInvite("hash", "usr_x", T0.toISOString())).resolves.toBe(false);
  });

  it("completeSetup is a single conditional UPDATE gated on hash + expiry + not-completed", async () => {
    const db = new FakeD1();
    const store = new D1IdentityStore(db as unknown as D1Database);
    await expect(store.completeSetup("hash", T0.toISOString())).resolves.toBe(true);
    const sql = db.runs[0].sql;
    expect(sql).toContain("UPDATE setup_state SET completed_at");
    expect(sql).toContain("completed_at IS NULL");
    expect(sql).toContain("setup_code_hash = ?");
    expect(sql).toContain("setup_code_expires_at > ?");
    db.changes = 0;
    await expect(store.completeSetup("hash", T0.toISOString())).resolves.toBe(false);
  });

  it("revocation cascades delete session rows; audit writes are INSERT-only", async () => {
    const db = new FakeD1();
    const store = new D1IdentityStore(db as unknown as D1Database);
    await store.deleteSessionsForUser("usr_x");
    expect(db.runs[0].sql).toContain("DELETE FROM sessions WHERE user_id = ?");
    await store.appendAudit({
      id: "aud_1",
      ts: T0.toISOString(),
      actorId: "usr_x",
      actorLabel: "alice",
      event: "login_success",
      target: "usr_x",
      detail: {},
    });
    const auditSql = db.runs[1].sql;
    expect(auditSql).toContain("INSERT INTO audit_log");
    expect(auditSql).not.toMatch(/UPDATE|DELETE/);
  });

  it("D1SessionStore.touchSession slides expiry to now + 30 days", async () => {
    const db = new FakeD1();
    const store = new D1SessionStore(db as unknown as D1Database);
    await store.touchSession("deadbeef", T0);
    expect(db.runs[0].sql).toContain("UPDATE sessions SET last_seen_at = ?, expires_at = ?");
    expect(db.runs[0].args).toEqual([
      T0.toISOString(),
      new Date(T0.getTime() + 30 * DAY).toISOString(),
      "deadbeef",
    ]);
  });
});
