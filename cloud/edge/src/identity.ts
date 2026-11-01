// Identity handlers (Spec 083, Step 2: T014–T017, T020–T022).
//
// Everything here is edge-handled: these routes are answered by the
// Worker itself from D1 and are NEVER forwarded to the container.
// Account creation exists in exactly two places in this file —
// redeemInvite (T015) and setup (T017) — and nowhere else in the
// Worker (FR-001, C083-1).
//
// Audit (T022, FR-012): every handler appends its audit rows through
// the store's append-only audit path, with actor + timestamp.

import type {
  AuditRow,
  IdentityStore,
  UserRow,
  WorkspaceRow,
} from "./identity-store";
import type { SessionIdentity } from "./session-store";
import {
  DUMMY_PASSWORD_HASH,
  isAcceptablePassword,
  type PasswordHasher,
} from "./password";
import { newId, newInviteCode, newSessionToken } from "./random";
import {
  clearedSessionCookieHeader,
  sessionCookieHeader,
  sessionExpiryIso,
  sha256Hex,
} from "./session";
import type { GlobalType, WorkspaceRole } from "./types";

export interface IdentityDeps {
  store: IdentityStore;
  hasher: PasswordHasher;
  now: () => Date;
}

// --- shared helpers --------------------------------------------------------

export function json(status: number, body: unknown, headers: HeadersInit = {}): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...headers },
  });
}

export function jsonError(status: number, code: string, message: string): Response {
  return json(status, { error: { code, message } });
}

async function readJsonBody(request: Request): Promise<Record<string, unknown>> {
  try {
    const value = (await request.json()) as unknown;
    if (value && typeof value === "object" && !Array.isArray(value)) {
      return value as Record<string, unknown>;
    }
  } catch {
    /* fall through to empty */
  }
  return {};
}

async function audit(
  deps: IdentityDeps,
  actor: { id: string | null; label: string },
  event: string,
  target: string | null,
  detail: Record<string, unknown> = {},
): Promise<void> {
  await deps.store.appendAudit({
    id: newId("aud"),
    ts: deps.now().toISOString(),
    actorId: actor.id,
    actorLabel: actor.label,
    event,
    target,
    detail,
  });
}

/** Audit writes are evidence, but a failed append must not 500 a login. */
async function auditBestEffort(
  deps: IdentityDeps,
  actor: { id: string | null; label: string },
  event: string,
  target: string | null,
  detail: Record<string, unknown> = {},
): Promise<void> {
  try {
    await audit(deps, actor, event, target, detail);
  } catch {
    /* best effort */
  }
}

const USERNAME_RE = /^[a-z0-9_.-]{3,32}$/;

/** Normalize (trim + lowercase) then validate (T015). */
export function normalizeUsername(raw: unknown): string | null {
  if (typeof raw !== "string") return null;
  const username = raw.trim().toLowerCase();
  return USERNAME_RE.test(username) ? username : null;
}

function publicUser(user: UserRow) {
  return {
    id: user.id,
    username: user.username,
    email: user.email,
    global_type: user.globalType,
    status: user.status,
    removed: user.removedAt !== null,
    created_at: user.createdAt,
    removed_at: user.removedAt,
  };
}

/** Issue a session for a user: plaintext token out, hash at rest. */
async function issueSession(
  deps: IdentityDeps,
  user: UserRow,
): Promise<{ token: string; responseHeaders: HeadersInit }> {
  const token = newSessionToken();
  const now = deps.now();
  await deps.store.createSession({
    id: newId("ses"),
    tokenHash: await sha256Hex(token),
    userId: user.id,
    createdAt: now.toISOString(),
    lastSeenAt: now.toISOString(),
    expiresAt: sessionExpiryIso(now),
    revokedAt: null,
  });
  return { token, responseHeaders: { "Set-Cookie": sessionCookieHeader(token) } };
}

const GLOBAL_TYPES: GlobalType[] = ["owner", "admin", "member", "guest"];
const WORKSPACE_ROLES: WorkspaceRole[] = ["owner", "admin", "member", "viewer"];

function isGlobalType(v: unknown): v is GlobalType {
  return typeof v === "string" && (GLOBAL_TYPES as string[]).includes(v);
}
/** Global Owner/Admin — the two types holding implicit Workspace Admin. */
function isGlobalAdmin(t: GlobalType): boolean {
  return t === "admin" || t === "owner";
}
/** Public audit entry: every stored field is safe to show an admin. */
export function publicAudit(r: AuditRow) {
  return {
    id: r.id,
    ts: r.ts,
    actor_id: r.actorId,
    actor_label: r.actorLabel,
    event: r.event,
    target: r.target,
    detail: r.detail,
  };
}
function isWorkspaceRole(v: unknown): v is WorkspaceRole {
  return typeof v === "string" && (WORKSPACE_ROLES as string[]).includes(v);
}

/** Validate a workspace-grants object; returns null when malformed. */
function parseGrants(raw: unknown): Record<string, WorkspaceRole> | null {
  if (raw === undefined || raw === null) return {};
  if (typeof raw !== "object" || Array.isArray(raw)) return null;
  const out: Record<string, WorkspaceRole> = {};
  for (const [k, v] of Object.entries(raw as Record<string, unknown>)) {
    if (!k || !isWorkspaceRole(v)) return null;
    out[k] = v;
  }
  return out;
}

// --- T016: login / logout --------------------------------------------------

export async function handleLogin(
  request: Request,
  deps: IdentityDeps,
): Promise<Response> {
  const body = await readJsonBody(request);
  const usernameRaw = typeof body.username === "string" ? body.username : "";
  const username = usernameRaw.trim().toLowerCase();
  const password = typeof body.password === "string" ? body.password : "";

  const user = username
    ? await deps.store.findUserByUsername(username)
    : null;
  const canSignIn =
    user !== null && user.status === "active" && user.removedAt === null;
  // Always run one Argon2id verification — against the real hash when
  // the account can sign in, the dummy hash otherwise — so unknown
  // user, wrong password, disabled, and removed are indistinguishable.
  const verified = await deps.hasher.verify(
    password,
    canSignIn ? user.passwordHash : DUMMY_PASSWORD_HASH,
  );

  if (!canSignIn || !verified) {
    await auditBestEffort(
      deps,
      { id: user?.id ?? null, label: username || "anonymous" },
      "login_failure",
      user?.id ?? null,
      { username },
    );
    return jsonError(401, "invalid_credentials", "Invalid username or password.");
  }

  const { responseHeaders } = await issueSession(deps, user);
  await auditBestEffort(
    deps,
    { id: user.id, label: user.username },
    "login_success",
    user.id,
  );
  return json(200, { user: publicUser(user) }, responseHeaders);
}

export async function handleLogout(
  deps: IdentityDeps,
  identity: SessionIdentity | null,
  tokenHash: string | null,
): Promise<Response> {
  if (!identity || !tokenHash) {
    return jsonError(401, "authentication_required", "Sign in is required for this route.");
  }
  // Instant revocation: the session row is deleted, not flagged.
  await deps.store.deleteSessionByTokenHash(tokenHash);
  await auditBestEffort(
    deps,
    { id: identity.userId, label: identity.username },
    "logout",
    identity.userId,
  );
  return json(
    200,
    { ok: true },
    { "Set-Cookie": clearedSessionCookieHeader() },
  );
}

// --- T014/T015: invite redemption (registration path 1 of 2) ---------------

export async function handleInviteRedeem(
  request: Request,
  deps: IdentityDeps,
  code: string,
): Promise<Response> {
  const body = await readJsonBody(request);
  const codeHash = await sha256Hex(code);
  const nowIso = deps.now().toISOString();
  const invite = await deps.store.peekInviteByHash(codeHash);

  const refuse = (status: number, errCode: string, message: string) =>
    jsonError(status, errCode, message);

  if (!invite) return refuse(400, "invite_not_found", "This invite link is not valid.");
  if (invite.revokedAt) return refuse(400, "invite_revoked", "This invite has been revoked by an admin.");
  if (invite.redeemedAt) return refuse(400, "invite_redeemed", "This invite has already been used.");
  if (invite.expiresAt <= nowIso) return refuse(400, "invite_expired", "This invite has expired.");

  // Optional email binding (FR-002 / D-2): a bound invite redeems only
  // for that email. The binding is checked BEFORE consumption, so a
  // mismatch never spends the invite.
  let email: string | null = invite.email;
  if (invite.email) {
    const presented = typeof body.email === "string" ? body.email.trim().toLowerCase() : "";
    if (presented !== invite.email.trim().toLowerCase()) {
      return refuse(400, "invite_email_mismatch", "This invite was issued for a different email address.");
    }
  } else if (typeof body.email === "string" && body.email.trim()) {
    email = body.email.trim();
  }

  const username = normalizeUsername(body.username);
  if (!username) {
    return refuse(400, "invalid_username", "Username must be 3–32 characters of a–z, 0–9, underscore, dot, or hyphen.");
  }
  if (!isAcceptablePassword(body.password)) {
    return refuse(400, "invalid_password", "Password must be at least 8 characters.");
  }
  if (await deps.store.findUserByUsername(username)) {
    return refuse(409, "username_taken", "That username is already taken.");
  }
  // Grants must point at live workspaces; a dangling grant refuses
  // before consumption rather than silently dropping access.
  for (const workspaceId of Object.keys(invite.workspaceGrants)) {
    const ws = await deps.store.getWorkspaceById(workspaceId);
    if (!ws || ws.archivedAt) {
      return refuse(400, "invite_grant_invalid", "This invite names a workspace that no longer exists.");
    }
  }

  const passwordHash = await deps.hasher.hash(body.password);
  const userId = newId("usr");

  // Atomic check-and-consume (single conditional UPDATE in D1). If
  // the gate fails, a concurrent redemption won — nothing is created.
  const consumed = await deps.store.consumeInvite(codeHash, userId, nowIso);
  if (!consumed) {
    return refuse(400, "invite_redeemed", "This invite has already been used.");
  }

  const user: UserRow = {
    id: userId,
    username,
    email,
    passwordHash,
    globalType: "member",
    status: "active",
    createdAt: nowIso,
    removedAt: null,
  };
  await deps.store.createUser(user);
  if (Object.keys(invite.workspaceGrants).length > 0) {
    await deps.store.replaceWorkspaceRoles(
      userId,
      invite.workspaceGrants,
      invite.createdBy,
      nowIso,
    );
  }
  const { responseHeaders } = await issueSession(deps, user);
  await auditBestEffort(
    deps,
    { id: user.id, label: user.username },
    "invite_redeemed",
    invite.id,
    { invite_id: invite.id, username },
  );
  return json(201, { user: publicUser(user) }, responseHeaders);
}

// --- T017: glassbreak setup (registration path 2 of 2) ---------------------

/** Setup is open only while no admin/owner exists and it never completed. */
export async function isSetupOpen(deps: IdentityDeps): Promise<boolean> {
  const state = await deps.store.getSetupState();
  if (!state || state.completedAt) return false;
  return !(await deps.store.hasAdminOrOwner());
}

export async function handleSetup(
  request: Request,
  deps: IdentityDeps,
): Promise<Response> {
  if (!(await isSetupOpen(deps))) {
    return jsonError(404, "not_found", "Not found.");
  }
  const state = await deps.store.getSetupState();
  const body = await readJsonBody(request);
  const code = typeof body.code === "string" ? body.code : "";
  const nowIso = deps.now().toISOString();

  if (
    !state?.setupCodeHash ||
    !state.setupCodeExpiresAt ||
    state.setupCodeExpiresAt <= nowIso
  ) {
    return jsonError(400, "setup_expired", "The setup code has expired. Re-run the operator seed step.");
  }
  if ((await sha256Hex(code)) !== state.setupCodeHash) {
    return jsonError(400, "setup_code_invalid", "The setup code is not valid.");
  }
  if (!isAcceptablePassword(body.password)) {
    return jsonError(400, "invalid_password", "Password must be at least 8 characters.");
  }
  if (!state.username || !state.email) {
    return jsonError(500, "setup_seed_missing", "The setup seed record is incomplete.");
  }

  const passwordHash = await deps.hasher.hash(body.password);
  // Single-statement gate: marks setup completed exactly once; a
  // replay (or a race) fails here and creates nothing.
  const claimed = await deps.store.completeSetup(state.setupCodeHash, nowIso);
  if (!claimed) {
    return jsonError(404, "not_found", "Not found.");
  }

  // Username and email come from the seed record — never from the
  // request body (Amendment 3).
  const user: UserRow = {
    id: newId("usr"),
    username: state.username.trim().toLowerCase(),
    email: state.email,
    passwordHash,
    globalType: "owner",
    status: "active",
    createdAt: nowIso,
    removedAt: null,
  };
  await deps.store.createUser(user);
  const { responseHeaders } = await issueSession(deps, user);
  await auditBestEffort(
    deps,
    { id: user.id, label: user.username },
    "setup_completed",
    user.id,
    { username: user.username },
  );
  return json(201, { user: publicUser(user) }, responseHeaders);
}

// --- T020/T021: admin API ----------------------------------------------------

export type AdminGate =
  | { ok: true; identity: SessionIdentity }
  | { ok: false; response: Response };

/**
 * Global Admin/Owner gate for /api/admin/*. Anonymous → 401;
 * member/guest → 403, and the denial is audit-logged (T022).
 */
export async function requireAdmin(
  deps: IdentityDeps,
  identity: SessionIdentity | null,
  routeLabel: string,
): Promise<AdminGate> {
  if (!identity) {
    await auditBestEffort(
      deps,
      { id: null, label: "anonymous" },
      "admin_api_denial",
      routeLabel,
      { route: routeLabel, reason: "anonymous" },
    );
    return {
      ok: false,
      response: jsonError(401, "authentication_required", "Sign in is required for this route."),
    };
  }
  if (identity.globalType !== "admin" && identity.globalType !== "owner") {
    await auditBestEffort(
      deps,
      { id: identity.userId, label: identity.username },
      "admin_api_denial",
      routeLabel,
      { route: routeLabel, global_type: identity.globalType },
    );
    return {
      ok: false,
      response: jsonError(403, "admin_required", "Admin access is required for this route."),
    };
  }
  return { ok: true, identity };
}

function publicInvite(invite: import("./identity-store").InviteRow) {
  // Sanitized: neither the plaintext code (never stored) nor its hash
  // ever leaves the edge on a list/read path.
  return {
    id: invite.id,
    created_by: invite.createdBy,
    email: invite.email,
    workspace_grants: invite.workspaceGrants,
    created_at: invite.createdAt,
    expires_at: invite.expiresAt,
    revoked_at: invite.revokedAt,
    redeemed_by: invite.redeemedBy,
    redeemed_at: invite.redeemedAt,
  };
}

export function publicWorkspace(w: WorkspaceRow) {
  return {
    id: w.id,
    name: w.name,
    slug: w.slug,
    description: w.description,
    archived_at: w.archivedAt,
    created_by: w.createdBy,
    created_at: w.createdAt,
  };
}

export function slugify(name: string): string {
  return name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/**
 * The admin router. `path` is the normalized pathname starting with
 * /api/admin. Returns null when no admin route matches (caller 404s).
 */
export async function handleAdminApi(
  request: Request,
  deps: IdentityDeps,
  identity: SessionIdentity,
  path: string,
): Promise<Response | null> {
  const method = request.method;
  const nowIso = deps.now().toISOString();
  const actor = { id: identity.userId, label: identity.username };
  const seg = path.split("/").filter(Boolean); // ["api","admin",...]

  // ---- users ----
  if (seg.length === 3 && seg[2] === "users" && method === "GET") {
    const users = await deps.store.listUsers();
    const out = [];
    for (const u of users) {
      out.push({
        ...publicUser(u),
        workspace_roles: await deps.store.getWorkspaceRoles(u.id),
      });
    }
    return json(200, { users: out });
  }

  const userMatch = seg.length === 4 && seg[2] === "users" ? seg[3] : null;
  const userSub =
    seg.length === 5 && seg[2] === "users" ? { id: seg[3], sub: seg[4] } : null;

  if (userMatch && method === "GET") {
    const user = await deps.store.findUserById(userMatch);
    if (!user) return jsonError(404, "user_not_found", "No such user.");
    return json(200, {
      user: {
        ...publicUser(user),
        workspace_roles: await deps.store.getWorkspaceRoles(user.id),
      },
    });
  }

  // Change global type: PATCH /users/:id, or POST /users/:id/type.
  if (
    (userMatch && method === "PATCH") ||
    (userSub?.sub === "type" && method === "POST")
  ) {
    const targetId = userMatch ?? userSub!.id;
    const target = await deps.store.findUserById(targetId);
    if (!target) return jsonError(404, "user_not_found", "No such user.");
    const body = await readJsonBody(request);
    const newType = body.global_type ?? body.globalType ?? body.type;
    if (!isGlobalType(newType)) {
      return jsonError(400, "invalid_global_type", "global_type must be owner, admin, member, or guest.");
    }
    // Owner singularity (Amendment 1): no API grants a second owner,
    // and the owner's type cannot be removed by anyone. Both refusals
    // are recorded — as audit rows, per the task's "recorded as refused".
    if (newType === "owner" && target.globalType !== "owner") {
      await auditBestEffort(deps, actor, "user_type_change_refused", target.id, {
        from: target.globalType, to: newType, reason: "owner_is_singular",
      });
      return jsonError(409, "owner_is_singular", "There is exactly one owner account; its type cannot be granted to another account.");
    }
    if (target.globalType === "owner" && newType !== "owner") {
      await auditBestEffort(deps, actor, "user_type_change_refused", target.id, {
        from: target.globalType, to: newType, reason: "owner_type_cannot_be_removed",
      });
      return jsonError(409, "owner_type_cannot_be_removed", "The owner account's type cannot be removed.");
    }
    if (newType !== target.globalType) {
      await deps.store.updateUserGlobalType(target.id, newType);
      // Type change revokes sessions instantly (T016), same operation.
      await deps.store.deleteSessionsForUser(target.id);
      await auditBestEffort(deps, actor, "user_type_changed", target.id, {
        from: target.globalType, to: newType,
      });
    }
    const updated = await deps.store.findUserById(target.id);
    return json(200, { user: publicUser(updated ?? target) });
  }

  if (userSub?.sub === "disable" && method === "POST") {
    const target = await deps.store.findUserById(userSub.id);
    if (!target) return jsonError(404, "user_not_found", "No such user.");
    await deps.store.setUserStatus(target.id, "disabled");
    await deps.store.deleteSessionsForUser(target.id);
    await auditBestEffort(deps, actor, "user_disabled", target.id, {});
    const updated = await deps.store.findUserById(target.id);
    return json(200, { user: publicUser(updated ?? target) });
  }

  if (userSub?.sub === "enable" && method === "POST") {
    const target = await deps.store.findUserById(userSub.id);
    if (!target) return jsonError(404, "user_not_found", "No such user.");
    if (target.removedAt) return jsonError(409, "user_removed", "A removed account cannot be re-enabled.");
    await deps.store.setUserStatus(target.id, "active");
    await auditBestEffort(deps, actor, "user_enabled", target.id, {});
    const updated = await deps.store.findUserById(target.id);
    return json(200, { user: publicUser(updated ?? target) });
  }

  if (
    (userSub?.sub === "remove" && method === "POST") ||
    (userMatch && method === "DELETE")
  ) {
    const targetId = userSub ? userSub.id : userMatch!;
    const target = await deps.store.findUserById(targetId);
    if (!target) return jsonError(404, "user_not_found", "No such user.");
    // Removal retains the row (attribution survives); sessions die now.
    await deps.store.markUserRemoved(target.id, nowIso);
    await deps.store.deleteSessionsForUser(target.id);
    await auditBestEffort(deps, actor, "user_removed", target.id, {});
    const updated = await deps.store.findUserById(target.id);
    return json(200, { user: publicUser(updated ?? target) });
  }

  // Per-user workspace-access matrix (T021).
  if (userSub?.sub === "workspaces" && (method === "GET" || method === "PUT")) {
    const target = await deps.store.findUserById(userSub.id);
    if (!target) return jsonError(404, "user_not_found", "No such user.");
    const workspaces = await deps.store.listWorkspaces();
    if (method === "GET") {
      const roles = await deps.store.getWorkspaceRoles(target.id);
      return json(200, {
        user_id: target.id,
        global_type: target.globalType,
        // Global Admin/Owner implicit Workspace Admin is NOT stored.
        implicit_workspace_admin:
          target.globalType === "admin" || target.globalType === "owner",
        workspace_roles: roles,
        workspaces: workspaces.map((w) => ({
          id: w.id,
          name: w.name,
          slug: w.slug,
          description: w.description,
          archived_at: w.archivedAt,
          role: roles[w.id] ?? null,
        })),
      });
    }
    // PUT: replace the full stored set.
    const body = await readJsonBody(request);
    const grants = parseGrants(body.workspace_roles ?? body.workspaceRoles ?? body.roles ?? body.grants);
    if (!grants) {
      return jsonError(400, "invalid_workspace_roles", "workspace_roles must map workspace id to owner, admin, member, or viewer.");
    }
    for (const [workspaceId, role] of Object.entries(grants)) {
      const ws = await deps.store.getWorkspaceById(workspaceId);
      if (!ws) return jsonError(400, "workspace_not_found", `No such workspace: ${workspaceId}`);
      if (ws.archivedAt) return jsonError(400, "workspace_archived", "An archived workspace takes no grants.");
      // Guest cap (Amendment 1): a Guest holds Viewer only — refused.
      if (target.globalType === "guest" && role !== "viewer") {
        await auditBestEffort(deps, actor, "admin_api_denial", target.id, {
          route: path, reason: "guest_viewer_cap", workspace_id: workspaceId, role,
        });
        return jsonError(403, "guest_viewer_cap", "Guest accounts may hold Viewer workspace roles only.");
      }
      // Exactly one workspace owner per workspace.
      if (role === "owner") {
        const currentOwner = await deps.store.findWorkspaceOwner(workspaceId);
        if (currentOwner && currentOwner !== target.id) {
          return jsonError(409, "workspace_owner_exists", "That workspace already has an owner.");
        }
      }
    }
    const before = await deps.store.getWorkspaceRoles(target.id);
    await deps.store.replaceWorkspaceRoles(target.id, grants, identity.userId, nowIso);
    if (JSON.stringify(before) !== JSON.stringify(grants)) {
      // Role change revokes the target's sessions instantly (T016).
      await deps.store.deleteSessionsForUser(target.id);
    }
    await auditBestEffort(deps, actor, "workspace_matrix_changed", target.id, {
      from: before, to: grants,
    });
    return json(200, {
      user_id: target.id,
      global_type: target.globalType,
      workspace_roles: grants,
    });
  }

  // ---- invites ----
  if (seg.length === 3 && seg[2] === "invites" && method === "GET") {
    const invites = await deps.store.listInvites();
    return json(200, { invites: invites.map(publicInvite) });
  }

  if (seg.length === 3 && seg[2] === "invites" && method === "POST") {
    const body = await readJsonBody(request);
    const grants = parseGrants(body.workspace_grants ?? body.workspaceGrants);
    if (!grants) {
      return jsonError(400, "invalid_workspace_grants", "workspace_grants must map workspace id to owner, admin, member, or viewer.");
    }
    for (const workspaceId of Object.keys(grants)) {
      const ws = await deps.store.getWorkspaceById(workspaceId);
      if (!ws || ws.archivedAt) {
        return jsonError(400, "workspace_not_found", `No such live workspace: ${workspaceId}`);
      }
    }
    let expiresAt: string;
    if (typeof body.expires_at === "string" && !Number.isNaN(Date.parse(body.expires_at))) {
      expiresAt = new Date(body.expires_at).toISOString();
    } else {
      const daysRaw = body.expires_in_days ?? body.expiry_days ?? body.days;
      const days = typeof daysRaw === "number" && daysRaw > 0 ? daysRaw : 7;
      expiresAt = new Date(deps.now().getTime() + days * 24 * 60 * 60 * 1000).toISOString();
    }
    if (expiresAt <= nowIso) {
      return jsonError(400, "invalid_expiry", "Invite expiry must be in the future.");
    }
    const code = newInviteCode();
    const invite = {
      id: newId("inv"),
      codeHash: await sha256Hex(code),
      createdBy: identity.userId,
      email: typeof body.email === "string" && body.email.trim() ? body.email.trim() : null,
      workspaceGrants: grants,
      createdAt: nowIso,
      expiresAt,
      revokedAt: null,
      redeemedBy: null,
      redeemedAt: null,
    };
    await deps.store.createInvite(invite);
    await auditBestEffort(deps, actor, "invite_created", invite.id, {
      email: invite.email, workspace_grants: grants, expires_at: expiresAt,
    });
    // The plaintext code is returned exactly once — here, in the
    // creation response (for the shareable link). Never stored,
    // never logged, never returned again.
    return json(201, {
      invite: publicInvite(invite),
      code,
      invite_url: `/invite/${code}`,
    });
  }

  const inviteSub =
    seg.length === 5 && seg[2] === "invites" ? { id: seg[3], sub: seg[4] } : null;
  if (
    (inviteSub?.sub === "revoke" && method === "POST") ||
    (seg.length === 4 && seg[2] === "invites" && method === "DELETE")
  ) {
    const inviteId = inviteSub ? inviteSub.id : seg[3];
    const outcome = await deps.store.revokeInvite(inviteId, nowIso);
    if (outcome === "not_found") return jsonError(404, "invite_not_found", "No such invite.");
    if (outcome === "redeemed") return jsonError(409, "invite_already_redeemed", "A redeemed invite cannot be revoked.");
    if (outcome === "revoked") return jsonError(409, "invite_already_revoked", "This invite is already revoked.");
    await auditBestEffort(deps, actor, "invite_revoked", inviteId, {});
    const updated = await deps.store.getInviteById(inviteId);
    return json(200, { invite: updated ? publicInvite(updated) : null });
  }

  // ---- audit (Step 3 read surface: wireframes 06 + 08) ----
  if (seg.length === 3 && seg[2] === "audit" && method === "GET") {
    const params = new URL(request.url).searchParams;
    const limitRaw = Number(params.get("limit") ?? "100");
    const offsetRaw = Number(params.get("offset") ?? "0");
    const limit = Number.isFinite(limitRaw)
      ? Math.min(500, Math.max(1, Math.floor(limitRaw)))
      : 100;
    const offset = Number.isFinite(offsetRaw)
      ? Math.max(0, Math.floor(offsetRaw))
      : 0;
    const rows = await deps.store.listAudit({
      event: params.get("event") ?? undefined,
      actorId: params.get("actor_id") ?? undefined,
      limit,
      offset,
    });
    return json(200, {
      entries: rows.map(publicAudit),
      limit,
      offset,
    });
  }

  // ---- workspaces ----
  if (seg.length === 3 && seg[2] === "workspaces" && method === "GET") {
    // Step 3 (wireframe 09): each row carries its member list, its
    // member count, and the CALLER's effective role in it (stored
    // grant, else the implicit Workspace Admin of a global
    // Owner/Admin — T018), so one read drives the whole screen.
    const workspaces = await deps.store.listWorkspaces();
    const actorRoles = await deps.store.getWorkspaceRoles(identity.userId);
    const views = [];
    for (const w of workspaces) {
      const members = await deps.store.listWorkspaceMembers(w.id);
      const stored = actorRoles[w.id];
      views.push({
        ...publicWorkspace(w),
        member_count: members.length,
        members: members.map((m) => ({
          user_id: m.userId,
          username: m.username,
          role: m.role,
        })),
        your_role: stored ?? (isGlobalAdmin(identity.globalType) ? "admin" : null),
        your_role_source: stored
          ? "stored"
          : isGlobalAdmin(identity.globalType)
            ? "implicit"
            : null,
      });
    }
    return json(200, { workspaces: views });
  }

  if (seg.length === 3 && seg[2] === "workspaces" && method === "POST") {
    const body = await readJsonBody(request);
    const name = typeof body.name === "string" ? body.name.trim() : "";
    if (!name) return jsonError(400, "invalid_name", "A workspace name is required.");
    const description =
      typeof body.description === "string" && body.description.trim()
        ? body.description.trim().slice(0, 500)
        : null;
    const baseSlug = slugify(name);
    if (!baseSlug) return jsonError(400, "invalid_name", "The workspace name yields no usable slug.");
    let slug = baseSlug;
    for (let n = 2; await deps.store.getWorkspaceBySlug(slug); n++) {
      slug = `${baseSlug}-${n}`;
    }
    const workspace: WorkspaceRow = {
      id: newId("ws"),
      name,
      slug,
      description,
      archivedAt: null,
      createdBy: identity.userId,
      createdAt: nowIso,
    };
    await deps.store.createWorkspace(workspace);
    await auditBestEffort(deps, actor, "workspace_created", workspace.id, {
      name, slug,
    });
    return json(201, { workspace: publicWorkspace(workspace) });
  }

  const wsSub =
    seg.length === 5 && seg[2] === "workspaces" ? { id: seg[3], sub: seg[4] } : null;
  if (wsSub?.sub === "archive" && method === "POST") {
    const ws = await deps.store.getWorkspaceById(wsSub.id);
    if (!ws) return jsonError(404, "workspace_not_found", "No such workspace.");
    const archived = await deps.store.archiveWorkspace(ws.id, nowIso);
    if (archived) {
      await auditBestEffort(deps, actor, "workspace_archived", ws.id, {});
    }
    const updated = await deps.store.getWorkspaceById(ws.id);
    return json(200, {
      workspace: updated
        ? { id: updated.id, name: updated.name, slug: updated.slug, archived_at: updated.archivedAt }
        : null,
    });
  }

  // Step 3 (wireframe 09 Manage): restore an archived workspace.
  if (wsSub?.sub === "restore" && method === "POST") {
    const ws = await deps.store.getWorkspaceById(wsSub.id);
    if (!ws) return jsonError(404, "workspace_not_found", "No such workspace.");
    const restored = await deps.store.unarchiveWorkspace(ws.id);
    if (restored) {
      await auditBestEffort(deps, actor, "workspace_restored", ws.id, {});
    }
    const updated = await deps.store.getWorkspaceById(ws.id);
    return json(200, { workspace: updated ? publicWorkspace(updated) : null });
  }

  // Step 3 (wireframe 09 Manage): rename / re-describe. The slug is
  // the workspace's identity and never changes here.
  if (seg.length === 4 && seg[2] === "workspaces" && method === "PATCH") {
    const ws = await deps.store.getWorkspaceById(seg[3]);
    if (!ws) return jsonError(404, "workspace_not_found", "No such workspace.");
    const body = await readJsonBody(request);
    const name =
      typeof body.name === "string" && body.name.trim() ? body.name.trim() : ws.name;
    const description =
      body.description === null
        ? null
        : typeof body.description === "string"
          ? body.description.trim().slice(0, 500) || null
          : ws.description;
    await deps.store.updateWorkspace(ws.id, { name, description });
    await auditBestEffort(deps, actor, "workspace_updated", ws.id, {
      from: { name: ws.name, description: ws.description },
      to: { name, description },
    });
    const updated = await deps.store.getWorkspaceById(ws.id);
    return json(200, { workspace: updated ? publicWorkspace(updated) : null });
  }

  return null;
}

// --- Step 3 (T025/T026) read + self-service surfaces ----------------------

/**
 * GET /api/session — the shell bootstrap (wireframes 07/11). Returns
 * the signed-in user and the workspaces THEY can enter: non-archived,
 * with the effective role (stored grant, else the implicit Workspace
 * Admin of a global Owner/Admin). A member sees only granted
 * workspaces; the container re-checks every request regardless —
 * this list shapes navigation, it is not the enforcement.
 */
export async function handleSessionIdentity(
  deps: IdentityDeps,
  identity: SessionIdentity,
): Promise<Response> {
  const user = await deps.store.findUserById(identity.userId);
  if (!user) {
    return jsonError(401, "authentication_required", "Sign in is required for this route.");
  }
  const roles = identity.workspaceRoles;
  const all = await deps.store.listWorkspaces();
  const workspaces = [];
  for (const w of all) {
    if (w.archivedAt) continue;
    const stored = roles[w.id];
    if (stored) {
      workspaces.push({ ...publicWorkspace(w), role: stored, role_source: "stored" });
    } else if (isGlobalAdmin(user.globalType)) {
      workspaces.push({ ...publicWorkspace(w), role: "admin", role_source: "implicit" });
    }
  }
  return json(200, {
    user: { ...publicUser(user), workspace_roles: roles },
    implicit_workspace_admin: isGlobalAdmin(user.globalType),
    workspaces,
  });
}

/**
 * GET /invite/:code/preview — what the acceptance screen shows BEFORE
 * redemption (wireframe 02): inviter, workspaces, expiry. Reading
 * never consumes. An unknown code returns only {state:"invalid"} —
 * no field distinguishes "never existed" from anything else, so the
 * preview is no existence oracle beyond what redeem already answers.
 */
export async function handleInvitePreview(
  deps: IdentityDeps,
  code: string,
): Promise<Response> {
  const invite = await deps.store.peekInviteByHash(await sha256Hex(code));
  if (!invite) return json(200, { state: "invalid" });
  const nowIso = deps.now().toISOString();
  const state = invite.revokedAt
    ? "revoked"
    : invite.redeemedAt
      ? "redeemed"
      : invite.expiresAt <= nowIso
        ? "expired"
        : "open";
  const creator = await deps.store.findUserById(invite.createdBy);
  const workspaces = [];
  for (const [workspaceId, role] of Object.entries(invite.workspaceGrants)) {
    const ws = await deps.store.getWorkspaceById(workspaceId);
    if (ws) workspaces.push({ id: ws.id, name: ws.name, role });
  }
  return json(200, {
    state,
    email: invite.email,
    expires_at: invite.expiresAt,
    created_by: creator
      ? { username: creator.username, global_type: creator.globalType }
      : null,
    workspaces,
  });
}

const EMAIL_SHAPE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/**
 * /api/account* — self-service for any signed-in user (wireframe 08).
 * Everything is scoped to the caller's own rows; session summaries
 * never carry token hashes (the current session is matched by hash
 * server-side and reported as a boolean).
 */
export async function handleAccountApi(
  request: Request,
  deps: IdentityDeps,
  identity: SessionIdentity,
  tokenHash: string,
  path: string,
): Promise<Response | null> {
  const method = request.method;
  const actor = { id: identity.userId, label: identity.username };
  const user = await deps.store.findUserById(identity.userId);
  if (!user) {
    return jsonError(401, "authentication_required", "Sign in is required for this route.");
  }

  if (path === "/api/account" && method === "GET") {
    const sessions = await deps.store.listSessionsForUser(user.id);
    const activity = await deps.store.listAudit({
      actorId: user.id,
      limit: 20,
      offset: 0,
    });
    return json(200, {
      user: {
        ...publicUser(user),
        workspace_roles: await deps.store.getWorkspaceRoles(user.id),
      },
      sessions: sessions.map((s) => ({
        id: s.id,
        created_at: s.createdAt,
        last_seen_at: s.lastSeenAt,
        expires_at: s.expiresAt,
        current: s.tokenHash === tokenHash,
      })),
      activity: activity.map(publicAudit),
    });
  }

  if (path === "/api/account/email" && method === "POST") {
    const body = await readJsonBody(request);
    const raw = typeof body.email === "string" ? body.email.trim() : "";
    const email = raw ? raw : null;
    if (email && (email.length > 254 || !EMAIL_SHAPE.test(email))) {
      return jsonError(400, "invalid_email", "That does not look like an email address.");
    }
    await deps.store.updateUserEmail(user.id, email);
    await auditBestEffort(deps, actor, "account_email_changed", user.id, {
      from: user.email,
      to: email,
    });
    const updated = await deps.store.findUserById(user.id);
    return json(200, { user: publicUser(updated ?? user) });
  }

  if (path === "/api/account/password" && method === "POST") {
    const body = await readJsonBody(request);
    const current = typeof body.current_password === "string" ? body.current_password : "";
    const next = typeof body.new_password === "string" ? body.new_password : "";
    const verified = await deps.hasher.verify(current, user.passwordHash);
    if (!verified) {
      return jsonError(400, "current_password_invalid", "The current password did not match.");
    }
    if (!isAcceptablePassword(next)) {
      return jsonError(400, "invalid_password", "Choose a password of at least 8 characters.");
    }
    await deps.store.updateUserPasswordHash(user.id, await deps.hasher.hash(next));
    // A password change ends every OTHER session; this one survives.
    const sessions = await deps.store.listSessionsForUser(user.id);
    for (const s of sessions) {
      if (s.tokenHash !== tokenHash) {
        await deps.store.deleteSessionById(user.id, s.id);
      }
    }
    await auditBestEffort(deps, actor, "password_changed", user.id, {});
    return json(200, { ok: true });
  }

  const revokeMatch = path.match(/^\/api\/account\/sessions\/([^/]+)\/revoke$/);
  if (revokeMatch && method === "POST") {
    const sessionId = revokeMatch[1];
    const sessions = await deps.store.listSessionsForUser(user.id);
    const target = sessions.find((s) => s.id === sessionId);
    if (!target) return jsonError(404, "session_not_found", "No such session.");
    if (target.tokenHash === tokenHash) {
      return jsonError(400, "current_session", "This is your current session — sign out to end it.");
    }
    await deps.store.deleteSessionById(user.id, sessionId);
    await auditBestEffort(deps, actor, "session_revoked", user.id, {
      session_id: sessionId,
    });
    return json(200, { ok: true });
  }

  return null;
}

/** T022: a container-scope denial observed by the edge on a proxied response. */
export async function auditContainerDenial(
  deps: IdentityDeps,
  identity: SessionIdentity,
  method: string,
  path: string,
  status: number,
): Promise<void> {
  await auditBestEffort(
    deps,
    { id: identity.userId, label: identity.username },
    "container_scope_denial",
    path,
    { method, path, status },
  );
}
