// Step 3 read + self-service surfaces (Spec 083 T025/T026 seams):
// the routes the Phase 3 frontend needs beyond the Step 2 write APIs.
//
//   - GET /api/session: the shell bootstrap — user + the workspaces
//     THEY can enter (stored grant, else implicit admin for global
//     Owner/Admin; archived workspaces never listed).
//   - GET /invite/:code/preview: what the acceptance screen shows
//     before redeeming; reading never consumes; an unknown code
//     answers only {state:"invalid"} (no existence oracle).
//   - GET /api/admin/audit: the append-only log becomes readable —
//     admin-gated (member denial audited, as before), filters work.
//   - /api/account/*: self-service — email, password change (ends
//     other sessions, this one survives), session list/revoke.
//   - Workspace description (migration 0005) round-trips through
//     create + admin list, with member counts and the caller's
//     effective role.

import { describe, expect, it } from "vitest";
import {
  makeHarness,
  seedUser,
  seedWorkspace,
  type Harness,
} from "./harness";

function post(path: string, body: unknown, cookie?: string) {
  return {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    ...(cookie ? { cookie } : {}),
  };
}

async function ownerCookie(h: Harness): Promise<string> {
  await seedUser(h, "glassbreak", "owner");
  return h.cookieFor("glassbreak");
}

async function createInvite(
  h: Harness,
  adminCookie: string,
  body: Record<string, unknown> = {},
): Promise<{ code: string; json: any }> {
  const res = await h.call("/api/admin/invites", post("/api/admin/invites", body, adminCookie));
  const json = (await res.json()) as any;
  return { code: json.code as string, json };
}

describe("GET /api/session — shell bootstrap", () => {
  it("answers 401 to anonymous callers", async () => {
    const h = makeHarness();
    const res = await h.call("/api/session");
    expect(res.status).toBe(401);
    expect(((await res.json()) as any).error.code).toBe("authentication_required");
  });

  it("lists only the member's granted, non-archived workspaces", async () => {
    const h = makeHarness();
    const admin = await ownerCookie(h);
    await seedWorkspace(h, "ws_indus", "Indus Script");
    await seedWorkspace(h, "ws_other", "Other Corpus");
    await seedWorkspace(h, "ws_old", "Old Archive");
    await seedUser(h, "alice", "member");
    // Alice: member of indus, viewer of the soon-archived one, nothing else.
    const put = await h.call(
      "/api/admin/users/usr_alice/workspaces",
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ workspace_roles: { ws_indus: "member", ws_old: "viewer" } }),
        cookie: admin,
      },
    );
    expect(put.status).toBe(200);
    // Archiving afterwards must hide it from her session list too.
    await h.store.archiveWorkspace("ws_old", new Date().toISOString());

    const res = await h.call("/api/session", { cookie: await h.cookieFor("alice") });
    expect(res.status).toBe(200);
    const body = (await res.json()) as any;
    expect(body.user.username).toBe("alice");
    expect(body.implicit_workspace_admin).toBe(false);
    expect(body.workspaces.map((w: any) => w.id)).toEqual(["ws_indus"]);
    expect(body.workspaces[0].role).toBe("member");
    expect(body.workspaces[0].role_source).toBe("stored");
  });

  it("gives a global admin every open workspace with the implicit role", async () => {
    const h = makeHarness();
    const admin = await ownerCookie(h);
    await seedWorkspace(h, "ws_indus", "Indus Script");
    const res = await h.call("/api/session", { cookie: admin });
    const body = (await res.json()) as any;
    expect(body.implicit_workspace_admin).toBe(true);
    expect(body.workspaces).toHaveLength(1);
    expect(body.workspaces[0].role).toBe("admin");
    expect(body.workspaces[0].role_source).toBe("implicit");
  });
});

describe("GET /invite/:code/preview — acceptance screen read", () => {
  it("shows inviter, workspaces and expiry for an open invite, without consuming it", async () => {
    const h = makeHarness();
    const admin = await ownerCookie(h);
    await seedWorkspace(h);
    const { code } = await createInvite(h, admin, {
      email: "new.person@example.org",
      workspace_grants: { ws_indus: "member" },
    });
    const res = await h.call(`/invite/${code}/preview`);
    expect(res.status).toBe(200);
    const body = (await res.json()) as any;
    expect(body.state).toBe("open");
    expect(body.email).toBe("new.person@example.org");
    expect(body.created_by.username).toBe("glassbreak");
    expect(body.workspaces).toEqual([{ id: "ws_indus", name: "Indus Script", role: "member" }]);
    // Reading did not consume: redemption still succeeds afterwards.
    const redeem = await h.call(
      `/invite/${code}/redeem`,
      post(`/invite/${code}/redeem`, {
        username: "newperson",
        email: "new.person@example.org",
        password: "newperson-pass-1",
      }),
    );
    expect(redeem.status).toBe(201);
    const spent = (await (await h.call(`/invite/${code}/preview`)).json()) as any;
    expect(spent.state).toBe("redeemed");
  });

  it("reports revoked and expired states in plain terms", async () => {
    const h = makeHarness();
    const admin = await ownerCookie(h);
    const a = await createInvite(h, admin, {});
    await h.call(`/api/admin/invites/${a.json.invite.id}/revoke`, post("", {}, admin));
    expect(((await (await h.call(`/invite/${a.code}/preview`)).json()) as any).state).toBe("revoked");

    const b = await createInvite(h, admin, { expires_in_days: 1 });
    h.setNow(new Date(Date.now() + 3 * 24 * 60 * 60 * 1000));
    expect(((await (await h.call(`/invite/${b.code}/preview`)).json()) as any).state).toBe("expired");
  });

  it("answers only {state:'invalid'} for an unknown code — no oracle fields", async () => {
    const h = makeHarness();
    await ownerCookie(h);
    const res = await h.call("/invite/definitely-not-a-real-code/preview");
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ state: "invalid" });
  });
});

describe("GET /api/admin/audit — the log is readable by admins only", () => {
  it("returns entries newest-first and honors event + actor filters", async () => {
    const h = makeHarness();
    const admin = await ownerCookie(h);
    await seedUser(h, "alice", "member");
    await h.cookieFor("alice"); // a login_success row for alice
    const all = (await (await h.call("/api/admin/audit", { cookie: admin })).json()) as any;
    expect(all.entries.length).toBeGreaterThanOrEqual(2);
    expect(all.entries[0].ts >= all.entries[all.entries.length - 1].ts).toBe(true);
    const logins = (await (await h.call("/api/admin/audit?event=login_success", { cookie: admin })).json()) as any;
    expect(logins.entries.every((e: any) => e.event === "login_success")).toBe(true);
    expect(logins.entries.some((e: any) => e.actor_label === "alice")).toBe(true);
    const aliceOnly = (await (await h.call("/api/admin/audit?actor_id=usr_alice", { cookie: admin })).json()) as any;
    expect(aliceOnly.entries.length).toBeGreaterThan(0);
    expect(aliceOnly.entries.every((e: any) => e.actor_id === "usr_alice")).toBe(true);
  });

  it("refuses members (403, denial audited) and anonymous callers (401)", async () => {
    const h = makeHarness();
    await ownerCookie(h);
    await seedUser(h, "alice", "member");
    const alice = await h.cookieFor("alice");
    expect((await h.call("/api/admin/audit", { cookie: alice })).status).toBe(403);
    expect((await h.call("/api/admin/audit")).status).toBe(401);
    expect(h.store.audit.some((a) => a.event === "admin_api_denial")).toBe(true);
  });
});

describe("/api/account — self-service", () => {
  it("shows the user, their sessions (current flagged), and their activity", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const cookie = await h.cookieFor("alice");
    const res = await h.call("/api/account", { cookie });
    expect(res.status).toBe(200);
    const body = (await res.json()) as any;
    expect(body.user.username).toBe("alice");
    expect(body.sessions).toHaveLength(1);
    expect(body.sessions[0].current).toBe(true);
    expect(body.sessions[0]).not.toHaveProperty("token_hash");
    expect(body.activity.some((e: any) => e.event === "login_success")).toBe(true);
    expect((await h.call("/api/account")).status).toBe(401);
  });

  it("changes the email (audited) and refuses a malformed one", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const cookie = await h.cookieFor("alice");
    const bad = await h.call("/api/account/email", post("/api/account/email", { email: "not-an-email" }, cookie));
    expect(bad.status).toBe(400);
    const ok = await h.call("/api/account/email", post("/api/account/email", { email: "alice@example.org" }, cookie));
    expect(ok.status).toBe(200);
    expect(((await ok.json()) as any).user.email).toBe("alice@example.org");
    const row = h.store.audit.find((a) => a.event === "account_email_changed");
    expect(row?.detail).toMatchObject({ to: "alice@example.org" });
  });

  it("password change: wrong current refused; success ends other sessions only", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const first = await h.cookieFor("alice");
    const second = await h.cookieFor("alice"); // a second live session
    const wrong = await h.call(
      "/api/account/password",
      post("/api/account/password", { current_password: "nope-nope-nope", new_password: "alice-new-pass-1" }, first),
    );
    expect(wrong.status).toBe(400);
    expect(((await wrong.json()) as any).error.code).toBe("current_password_invalid");

    const ok = await h.call(
      "/api/account/password",
      post("/api/account/password", { current_password: "alice-pass-1234", new_password: "alice-new-pass-1" }, first),
    );
    expect(ok.status).toBe(200);
    // The other session is dead; the changing session still works.
    expect((await h.call("/api/account", { cookie: second })).status).toBe(401);
    expect((await h.call("/api/account", { cookie: first })).status).toBe(200);
    expect(h.store.audit.some((a) => a.event === "password_changed")).toBe(true);
    // The new password logs in; the old one does not.
    await expect(h.cookieFor("alice")).rejects.toThrow();
    const relogin = await h.call("/login", post("/login", { username: "alice", password: "alice-new-pass-1" }));
    expect(relogin.status).toBe(200);
  });

  it("revokes another session, refuses to revoke the current one, 404s strangers", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const first = await h.cookieFor("alice");
    const second = await h.cookieFor("alice");
    const view = (await (await h.call("/api/account", { cookie: first })).json()) as any;
    const other = view.sessions.find((s: any) => !s.current);
    const mine = view.sessions.find((s: any) => s.current);
    expect(other).toBeTruthy();
    const refused = await h.call(`/api/account/sessions/${mine.id}/revoke`, post("", {}, first));
    expect(refused.status).toBe(400);
    expect(((await refused.json()) as any).error.code).toBe("current_session");
    const ok = await h.call(`/api/account/sessions/${other.id}/revoke`, post("", {}, first));
    expect(ok.status).toBe(200);
    expect((await h.call("/api/account", { cookie: second })).status).toBe(401);
    const missing = await h.call("/api/account/sessions/sess_nope/revoke", post("", {}, first));
    expect(missing.status).toBe(404);
    expect(h.store.audit.some((a) => a.event === "session_revoked")).toBe(true);
  });
});

describe("workspace update + restore (wireframe 09 Manage)", () => {
  it("renames and re-describes without touching the slug, and restores an archive", async () => {
    const h = makeHarness();
    const admin = await ownerCookie(h);
    const created = await h.call(
      "/api/admin/workspaces",
      post("/api/admin/workspaces", { name: "Comparative Scripts" }, admin),
    );
    const ws = ((await created.json()) as any).workspace;
    const patched = await h.call(`/api/admin/workspaces/${ws.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: "Comparative Scripts II", description: "Cross-script comparisons." }),
      cookie: admin,
    });
    expect(patched.status).toBe(200);
    const after = ((await patched.json()) as any).workspace;
    expect(after.name).toBe("Comparative Scripts II");
    expect(after.description).toBe("Cross-script comparisons.");
    expect(after.slug).toBe(ws.slug);
    expect(h.store.audit.some((a) => a.event === "workspace_updated")).toBe(true);

    await h.call(`/api/admin/workspaces/${ws.id}/archive`, post("", {}, admin));
    const restored = await h.call(`/api/admin/workspaces/${ws.id}/restore`, post("", {}, admin));
    expect(restored.status).toBe(200);
    expect(((await restored.json()) as any).workspace.archived_at).toBeNull();
    expect(h.store.audit.some((a) => a.event === "workspace_restored")).toBe(true);
  });
});

describe("workspace description + admin list enrichment (migration 0005)", () => {
  it("round-trips the description and reports members + the caller's role", async () => {
    const h = makeHarness();
    const admin = await ownerCookie(h);
    await seedUser(h, "alice", "member");
    const created = await h.call(
      "/api/admin/workspaces",
      post("/api/admin/workspaces", { name: "Indus Script", description: "Decipherment of the Indus script." }, admin),
    );
    expect(created.status).toBe(201);
    const ws = ((await created.json()) as any).workspace;
    expect(ws.description).toBe("Decipherment of the Indus script.");
    // Give alice a stored member grant so member_count is real.
    await h.call(`/api/admin/users/usr_alice/workspaces`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ workspace_roles: { [ws.id]: "member" } }),
      cookie: admin,
    });
    const list = (await (await h.call("/api/admin/workspaces", { cookie: admin })).json()) as any;
    const row = list.workspaces.find((w: any) => w.id === ws.id);
    expect(row.description).toBe("Decipherment of the Indus script.");
    expect(row.member_count).toBe(1);
    expect(row.members).toEqual([{ user_id: "usr_alice", username: "alice", role: "member" }]);
    // glassbreak holds no stored grant here: implicit admin via global type.
    expect(row.your_role).toBe("admin");
    expect(row.your_role_source).toBe("implicit");
  });
});
