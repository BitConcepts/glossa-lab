// The identity-store seam (Spec 083, Step 2).
//
// Step 1 shipped SessionStore (src/session-store.ts) for the perimeter
// lookup. Step 2 builds the full identity logic — invites, users,
// sessions, workspaces, audit — behind this IdentityStore interface:
// the handlers in src/identity.ts depend only on the interface, the
// production implementation below runs against D1, and the vitest
// suite injects an in-memory implementation with the same semantics
// (the fake-D1 pattern of Step 1, one level up).
//
// Atomicity notes (T014/T017): the two check-and-consume gates are
// SINGLE conditional UPDATE statements —
//   consumeInvite:  UPDATE invites SET redeemed… WHERE code_hash = ?
//                   AND redeemed_at IS NULL AND revoked_at IS NULL
//                   AND expires_at > ?
//   completeSetup:  UPDATE setup_state SET completed_at = ? WHERE
//                   id = 'singleton' AND completed_at IS NULL
//                   AND setup_code_hash = ? AND setup_code_expires_at > ?
// A gate reports success only when exactly one row changed, so a
// second redemption / a replayed setup can never pass the gate, even
// under concurrent requests — D1 serializes the UPDATE itself.
//
// Audit (T022): audit_log is append-only. This interface exposes an
// append and a read for tests/admin display — no update, no delete.

import { D1SessionStore, type SessionStore } from "./session-store";
import type { SessionIdentity } from "./session-store";
import type { GlobalType, WorkspaceRole } from "./types";

export type UserStatus = "active" | "disabled";

export interface UserRow {
  id: string;
  username: string;
  email: string | null;
  passwordHash: string;
  globalType: GlobalType;
  status: UserStatus;
  createdAt: string;
  removedAt: string | null;
}

export interface InviteRow {
  id: string;
  codeHash: string;
  createdBy: string;
  email: string | null;
  /** JSON-shaped map: workspace id -> role granted on redemption. */
  workspaceGrants: Record<string, WorkspaceRole>;
  createdAt: string;
  expiresAt: string;
  revokedAt: string | null;
  redeemedBy: string | null;
  redeemedAt: string | null;
}

export interface SessionRow {
  id: string;
  tokenHash: string;
  userId: string;
  createdAt: string;
  lastSeenAt: string;
  expiresAt: string;
  revokedAt: string | null;
}

export interface WorkspaceRow {
  id: string;
  name: string;
  slug: string;
  /** The question/scope line shown on cards (Step 3, migration 0005). */
  description: string | null;
  archivedAt: string | null;
  createdBy: string;
  createdAt: string;
}

/** Filter for audit reads (Step 3): exact event and/or actor, paged. */
export interface AuditFilter {
  event?: string;
  actorId?: string;
  limit: number;
  offset: number;
}

/** One row of a workspace's member list (Step 3 admin reads). */
export interface WorkspaceMember {
  userId: string;
  username: string;
  role: WorkspaceRole;
}

export interface SetupStateRow {
  setupCodeHash: string | null;
  setupCodeExpiresAt: string | null;
  completedAt: string | null;
  /** Seed record (Amendment 3): the account setup will create. */
  username: string | null;
  email: string | null;
}

export interface AuditInput {
  actorId: string | null;
  actorLabel: string;
  event: string;
  target: string | null;
  detail: Record<string, unknown>;
  ts: string;
}

export interface AuditRow extends AuditInput {
  id: string;
}

/** Outcome of the conditional revoke gate. */
export type RevokeOutcome = "ok" | "not_found" | "redeemed" | "revoked";

export interface IdentityStore {
  // --- audit (append-only writes; reads added Step 3) ---
  appendAudit(row: AuditRow): Promise<void>;
  /** Newest-first audit reads for the admin surface + own-activity. */
  listAudit(filter: AuditFilter): Promise<AuditRow[]>;

  // --- setup ---
  getSetupState(): Promise<SetupStateRow | null>;
  /** True when any owner/admin account row exists (setup is closed). */
  hasAdminOrOwner(): Promise<boolean>;
  /** Single-statement check-and-consume gate for the setup code. */
  completeSetup(codeHash: string, nowIso: string): Promise<boolean>;

  // --- invites ---
  createInvite(row: InviteRow): Promise<void>;
  listInvites(): Promise<InviteRow[]>;
  getInviteById(id: string): Promise<InviteRow | null>;
  peekInviteByHash(codeHash: string): Promise<InviteRow | null>;
  /** Single-statement atomic check-and-consume. */
  consumeInvite(codeHash: string, userId: string, nowIso: string): Promise<boolean>;
  revokeInvite(id: string, nowIso: string): Promise<RevokeOutcome>;

  // --- users ---
  createUser(row: UserRow): Promise<void>;
  /** Case-insensitive lookup: pass the already-lowercased username. */
  findUserByUsername(usernameLower: string): Promise<UserRow | null>;
  findUserById(id: string): Promise<UserRow | null>;
  listUsers(): Promise<UserRow[]>;
  updateUserGlobalType(id: string, globalType: GlobalType): Promise<void>;
  setUserStatus(id: string, status: UserStatus): Promise<void>;
  markUserRemoved(id: string, nowIso: string): Promise<void>;
  /** Account self-service (Step 3): the user's own contact email. */
  updateUserEmail(id: string, email: string | null): Promise<void>;
  /** Account self-service (Step 3): password change (hash only). */
  updateUserPasswordHash(id: string, passwordHash: string): Promise<void>;

  // --- sessions ---
  createSession(row: SessionRow): Promise<void>;
  /** Instant revocation cascade: the user's session rows are deleted. */
  deleteSessionsForUser(userId: string): Promise<void>;
  deleteSessionByTokenHash(tokenHash: string): Promise<void>;
  /** The user's live session rows (Step 3 account screen). */
  listSessionsForUser(userId: string): Promise<SessionRow[]>;
  /** Delete one session, only if it belongs to the user. */
  deleteSessionById(userId: string, sessionId: string): Promise<boolean>;

  // --- workspaces + roles ---
  createWorkspace(row: WorkspaceRow): Promise<void>;
  listWorkspaces(): Promise<WorkspaceRow[]>;
  getWorkspaceById(id: string): Promise<WorkspaceRow | null>;
  getWorkspaceBySlug(slug: string): Promise<WorkspaceRow | null>;
  archiveWorkspace(id: string, nowIso: string): Promise<boolean>;
  getWorkspaceRoles(userId: string): Promise<Record<string, WorkspaceRole>>;
  replaceWorkspaceRoles(
    userId: string,
    roles: Record<string, WorkspaceRole>,
    grantedBy: string,
    nowIso: string,
  ): Promise<void>;
  /** The user id holding the workspace's `owner` role, if any. */
  findWorkspaceOwner(workspaceId: string): Promise<string | null>;
  /** Stored members of one workspace (Step 3 admin reads). */
  listWorkspaceMembers(workspaceId: string): Promise<WorkspaceMember[]>;
  /** Rename / re-describe a workspace (Step 3, wireframe 09 Manage).
   *  The slug never changes: it is the workspace's identity. */
  updateWorkspace(
    id: string,
    fields: { name: string; description: string | null },
  ): Promise<void>;
  /** Reverse an archive (Step 3, wireframe 09 Manage). */
  unarchiveWorkspace(id: string): Promise<boolean>;
}

// ---------------------------------------------------------------------------
// D1 implementation
// ---------------------------------------------------------------------------

interface DbUserRow {
  id: string;
  username: string;
  email: string | null;
  password_hash: string;
  global_type: GlobalType;
  status: UserStatus;
  created_at: string;
  removed_at: string | null;
}
interface DbInviteRow {
  id: string;
  code_hash: string;
  created_by: string;
  email: string | null;
  workspace_grants: string;
  created_at: string;
  expires_at: string;
  revoked_at: string | null;
  redeemed_by: string | null;
  redeemed_at: string | null;
}
interface DbWorkspaceRow {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  archived_at: string | null;
  created_by: string;
  created_at: string;
}
interface DbAuditRow {
  id: string;
  ts: string;
  actor_id: string | null;
  actor_label: string;
  event: string;
  target: string | null;
  detail: string;
}
interface DbSetupRow {
  setup_code_hash: string | null;
  setup_code_expires_at: string | null;
  completed_at: string | null;
  username: string | null;
  email: string | null;
}

const toUser = (r: DbUserRow): UserRow => ({
  id: r.id,
  username: r.username,
  email: r.email,
  passwordHash: r.password_hash,
  globalType: r.global_type,
  status: r.status,
  createdAt: r.created_at,
  removedAt: r.removed_at,
});
const toInvite = (r: DbInviteRow): InviteRow => ({
  id: r.id,
  codeHash: r.code_hash,
  createdBy: r.created_by,
  email: r.email,
  workspaceGrants: JSON.parse(r.workspace_grants || "{}") as Record<
    string,
    WorkspaceRole
  >,
  createdAt: r.created_at,
  expiresAt: r.expires_at,
  revokedAt: r.revoked_at,
  redeemedBy: r.redeemed_by,
  redeemedAt: r.redeemed_at,
});
const toWorkspace = (r: DbWorkspaceRow): WorkspaceRow => ({
  id: r.id,
  name: r.name,
  slug: r.slug,
  description: r.description ?? null,
  archivedAt: r.archived_at,
  createdBy: r.created_by,
  createdAt: r.created_at,
});
const toAudit = (r: DbAuditRow): AuditRow => ({
  id: r.id,
  ts: r.ts,
  actorId: r.actor_id,
  actorLabel: r.actor_label,
  event: r.event,
  target: r.target,
  detail: (() => {
    try {
      const parsed = JSON.parse(r.detail || "{}") as unknown;
      return parsed && typeof parsed === "object" && !Array.isArray(parsed)
        ? (parsed as Record<string, unknown>)
        : {};
    } catch {
      return {};
    }
  })(),
});

function changes(res: D1Result): number {
  return (res.meta as { changes?: number } | undefined)?.changes ?? 0;
}

export class D1IdentityStore implements IdentityStore, SessionStore {
  private readonly sessions: D1SessionStore;
  constructor(private readonly db: D1Database) {
    this.sessions = new D1SessionStore(db);
  }

  // SessionStore seam (delegates to the Step 1 store).
  findIdentityByTokenHash(tokenHash: string, now: Date) {
    return this.sessions.findIdentityByTokenHash(tokenHash, now);
  }
  touchSession(tokenHash: string, now: Date) {
    return this.sessions.touchSession(tokenHash, now);
  }

  async appendAudit(row: AuditRow): Promise<void> {
    await this.db
      .prepare(
        `INSERT INTO audit_log (id, ts, actor_id, actor_label, event, target, detail)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
      )
      .bind(
        row.id,
        row.ts,
        row.actorId,
        row.actorLabel,
        row.event,
        row.target,
        JSON.stringify(row.detail),
      )
      .run();
  }

  async listAudit(filter: AuditFilter): Promise<AuditRow[]> {
    const clauses: string[] = [];
    const binds: unknown[] = [];
    if (filter.event) {
      clauses.push(`event = ?`);
      binds.push(filter.event);
    }
    if (filter.actorId) {
      clauses.push(`actor_id = ?`);
      binds.push(filter.actorId);
    }
    const where = clauses.length ? `WHERE ${clauses.join(" AND ")}` : "";
    const res = await this.db
      .prepare(
        `SELECT * FROM audit_log ${where} ORDER BY ts DESC, id DESC LIMIT ? OFFSET ?`,
      )
      .bind(...binds, filter.limit, filter.offset)
      .all<DbAuditRow>();
    return (res.results ?? []).map(toAudit);
  }

  async getSetupState(): Promise<SetupStateRow | null> {
    const r = await this.db
      .prepare(
        `SELECT setup_code_hash, setup_code_expires_at, completed_at, username, email
           FROM setup_state WHERE id = 'singleton'`,
      )
      .first<DbSetupRow>();
    if (!r) return null;
    return {
      setupCodeHash: r.setup_code_hash,
      setupCodeExpiresAt: r.setup_code_expires_at,
      completedAt: r.completed_at,
      username: r.username,
      email: r.email,
    };
  }

  async hasAdminOrOwner(): Promise<boolean> {
    const r = await this.db
      .prepare(
        `SELECT id FROM users WHERE global_type IN ('owner', 'admin') LIMIT 1`,
      )
      .first<{ id: string }>();
    return r !== null;
  }

  async completeSetup(codeHash: string, nowIso: string): Promise<boolean> {
    const res = await this.db
      .prepare(
        `UPDATE setup_state SET completed_at = ?
          WHERE id = 'singleton' AND completed_at IS NULL
            AND setup_code_hash = ? AND setup_code_expires_at > ?`,
      )
      .bind(nowIso, codeHash, nowIso)
      .run();
    return changes(res) === 1;
  }

  async createInvite(row: InviteRow): Promise<void> {
    await this.db
      .prepare(
        `INSERT INTO invites (id, code_hash, created_by, email, workspace_grants,
                               created_at, expires_at, revoked_at, redeemed_by, redeemed_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      )
      .bind(
        row.id,
        row.codeHash,
        row.createdBy,
        row.email,
        JSON.stringify(row.workspaceGrants),
        row.createdAt,
        row.expiresAt,
        row.revokedAt,
        row.redeemedBy,
        row.redeemedAt,
      )
      .run();
  }

  async listInvites(): Promise<InviteRow[]> {
    const res = await this.db
      .prepare(`SELECT * FROM invites ORDER BY created_at DESC`)
      .all<DbInviteRow>();
    return (res.results ?? []).map(toInvite);
  }

  async getInviteById(id: string): Promise<InviteRow | null> {
    const r = await this.db
      .prepare(`SELECT * FROM invites WHERE id = ?`)
      .bind(id)
      .first<DbInviteRow>();
    return r ? toInvite(r) : null;
  }

  async peekInviteByHash(codeHash: string): Promise<InviteRow | null> {
    const r = await this.db
      .prepare(`SELECT * FROM invites WHERE code_hash = ?`)
      .bind(codeHash)
      .first<DbInviteRow>();
    return r ? toInvite(r) : null;
  }

  async consumeInvite(
    codeHash: string,
    userId: string,
    nowIso: string,
  ): Promise<boolean> {
    const res = await this.db
      .prepare(
        `UPDATE invites SET redeemed_by = ?, redeemed_at = ?
          WHERE code_hash = ? AND redeemed_at IS NULL
            AND revoked_at IS NULL AND expires_at > ?`,
      )
      .bind(userId, nowIso, codeHash, nowIso)
      .run();
    return changes(res) === 1;
  }

  async revokeInvite(id: string, nowIso: string): Promise<RevokeOutcome> {
    const res = await this.db
      .prepare(
        `UPDATE invites SET revoked_at = ?
          WHERE id = ? AND revoked_at IS NULL AND redeemed_at IS NULL`,
      )
      .bind(nowIso, id)
      .run();
    if (changes(res) === 1) return "ok";
    const existing = await this.getInviteById(id);
    if (!existing) return "not_found";
    if (existing.redeemedAt) return "redeemed";
    return "revoked";
  }

  async createUser(row: UserRow): Promise<void> {
    await this.db
      .prepare(
        `INSERT INTO users (id, username, email, password_hash, global_type,
                            status, created_at, removed_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      )
      .bind(
        row.id,
        row.username,
        row.email,
        row.passwordHash,
        row.globalType,
        row.status,
        row.createdAt,
        row.removedAt,
      )
      .run();
  }

  async findUserByUsername(usernameLower: string): Promise<UserRow | null> {
    const r = await this.db
      .prepare(`SELECT * FROM users WHERE lower(username) = ?`)
      .bind(usernameLower)
      .first<DbUserRow>();
    return r ? toUser(r) : null;
  }

  async findUserById(id: string): Promise<UserRow | null> {
    const r = await this.db
      .prepare(`SELECT * FROM users WHERE id = ?`)
      .bind(id)
      .first<DbUserRow>();
    return r ? toUser(r) : null;
  }

  async listUsers(): Promise<UserRow[]> {
    const res = await this.db
      .prepare(`SELECT * FROM users ORDER BY created_at ASC`)
      .all<DbUserRow>();
    return (res.results ?? []).map(toUser);
  }

  async updateUserGlobalType(id: string, globalType: GlobalType): Promise<void> {
    await this.db
      .prepare(`UPDATE users SET global_type = ? WHERE id = ?`)
      .bind(globalType, id)
      .run();
  }

  async setUserStatus(id: string, status: UserStatus): Promise<void> {
    await this.db
      .prepare(`UPDATE users SET status = ? WHERE id = ?`)
      .bind(status, id)
      .run();
  }

  async markUserRemoved(id: string, nowIso: string): Promise<void> {
    await this.db
      .prepare(
        `UPDATE users SET removed_at = ?, status = 'disabled' WHERE id = ?`,
      )
      .bind(nowIso, id)
      .run();
  }

  async updateUserEmail(id: string, email: string | null): Promise<void> {
    await this.db
      .prepare(`UPDATE users SET email = ? WHERE id = ?`)
      .bind(email, id)
      .run();
  }

  async updateUserPasswordHash(id: string, passwordHash: string): Promise<void> {
    await this.db
      .prepare(`UPDATE users SET password_hash = ? WHERE id = ?`)
      .bind(passwordHash, id)
      .run();
  }

  async createSession(row: SessionRow): Promise<void> {
    await this.db
      .prepare(
        `INSERT INTO sessions (id, token_hash, user_id, created_at,
                               last_seen_at, expires_at, revoked_at)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
      )
      .bind(
        row.id,
        row.tokenHash,
        row.userId,
        row.createdAt,
        row.lastSeenAt,
        row.expiresAt,
        row.revokedAt,
      )
      .run();
  }

  async deleteSessionsForUser(userId: string): Promise<void> {
    await this.db
      .prepare(`DELETE FROM sessions WHERE user_id = ?`)
      .bind(userId)
      .run();
  }

  async deleteSessionByTokenHash(tokenHash: string): Promise<void> {
    await this.db
      .prepare(`DELETE FROM sessions WHERE token_hash = ?`)
      .bind(tokenHash)
      .run();
  }

  async listSessionsForUser(userId: string): Promise<SessionRow[]> {
    const res = await this.db
      .prepare(
        `SELECT * FROM sessions WHERE user_id = ? AND revoked_at IS NULL
          ORDER BY last_seen_at DESC`,
      )
      .bind(userId)
      .all<{
        id: string;
        token_hash: string;
        user_id: string;
        created_at: string;
        last_seen_at: string;
        expires_at: string;
        revoked_at: string | null;
      }>();
    return (res.results ?? []).map((r) => ({
      id: r.id,
      tokenHash: r.token_hash,
      userId: r.user_id,
      createdAt: r.created_at,
      lastSeenAt: r.last_seen_at,
      expiresAt: r.expires_at,
      revokedAt: r.revoked_at,
    }));
  }

  async deleteSessionById(userId: string, sessionId: string): Promise<boolean> {
    const res = await this.db
      .prepare(`DELETE FROM sessions WHERE id = ? AND user_id = ?`)
      .bind(sessionId, userId)
      .run();
    return changes(res) === 1;
  }

  async createWorkspace(row: WorkspaceRow): Promise<void> {
    await this.db
      .prepare(
        `INSERT INTO workspaces (id, name, slug, description, archived_at, created_by, created_at)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
      )
      .bind(row.id, row.name, row.slug, row.description, row.archivedAt, row.createdBy, row.createdAt)
      .run();
  }

  async listWorkspaces(): Promise<WorkspaceRow[]> {
    const res = await this.db
      .prepare(`SELECT * FROM workspaces ORDER BY created_at ASC`)
      .all<DbWorkspaceRow>();
    return (res.results ?? []).map(toWorkspace);
  }

  async getWorkspaceById(id: string): Promise<WorkspaceRow | null> {
    const r = await this.db
      .prepare(`SELECT * FROM workspaces WHERE id = ?`)
      .bind(id)
      .first<DbWorkspaceRow>();
    return r ? toWorkspace(r) : null;
  }

  async getWorkspaceBySlug(slug: string): Promise<WorkspaceRow | null> {
    const r = await this.db
      .prepare(`SELECT * FROM workspaces WHERE slug = ?`)
      .bind(slug)
      .first<DbWorkspaceRow>();
    return r ? toWorkspace(r) : null;
  }

  async archiveWorkspace(id: string, nowIso: string): Promise<boolean> {
    const res = await this.db
      .prepare(
        `UPDATE workspaces SET archived_at = ? WHERE id = ? AND archived_at IS NULL`,
      )
      .bind(nowIso, id)
      .run();
    return changes(res) === 1;
  }

  async getWorkspaceRoles(
    userId: string,
  ): Promise<Record<string, WorkspaceRole>> {
    const res = await this.db
      .prepare(
        `SELECT workspace_id, role FROM workspace_roles WHERE user_id = ?`,
      )
      .bind(userId)
      .all<{ workspace_id: string; role: WorkspaceRole }>();
    const out: Record<string, WorkspaceRole> = {};
    for (const r of res.results ?? []) out[r.workspace_id] = r.role;
    return out;
  }

  async replaceWorkspaceRoles(
    userId: string,
    roles: Record<string, WorkspaceRole>,
    grantedBy: string,
    nowIso: string,
  ): Promise<void> {
    const statements: D1PreparedStatement[] = [
      this.db
        .prepare(`DELETE FROM workspace_roles WHERE user_id = ?`)
        .bind(userId),
    ];
    for (const [workspaceId, role] of Object.entries(roles)) {
      statements.push(
        this.db
          .prepare(
            `INSERT INTO workspace_roles (user_id, workspace_id, role, granted_by, granted_at)
             VALUES (?, ?, ?, ?, ?)`,
          )
          .bind(userId, workspaceId, role, grantedBy, nowIso),
      );
    }
    // One batch = one transaction: the set is replaced whole or not at all.
    await this.db.batch(statements);
  }

  async findWorkspaceOwner(workspaceId: string): Promise<string | null> {
    const r = await this.db
      .prepare(
        `SELECT user_id FROM workspace_roles
          WHERE workspace_id = ? AND role = 'owner' LIMIT 1`,
      )
      .bind(workspaceId)
      .first<{ user_id: string }>();
    return r?.user_id ?? null;
  }

  async listWorkspaceMembers(workspaceId: string): Promise<WorkspaceMember[]> {
    const res = await this.db
      .prepare(
        `SELECT wr.user_id AS user_id, u.username AS username, wr.role AS role
           FROM workspace_roles AS wr
           JOIN users AS u ON u.id = wr.user_id
          WHERE wr.workspace_id = ?
          ORDER BY u.username ASC`,
      )
      .bind(workspaceId)
      .all<{ user_id: string; username: string; role: WorkspaceRole }>();
    return (res.results ?? []).map((r) => ({
      userId: r.user_id,
      username: r.username,
      role: r.role,
    }));
  }

  async updateWorkspace(
    id: string,
    fields: { name: string; description: string | null },
  ): Promise<void> {
    await this.db
      .prepare(`UPDATE workspaces SET name = ?, description = ? WHERE id = ?`)
      .bind(fields.name, fields.description, id)
      .run();
  }

  async unarchiveWorkspace(id: string): Promise<boolean> {
    const res = await this.db
      .prepare(
        `UPDATE workspaces SET archived_at = NULL WHERE id = ? AND archived_at IS NOT NULL`,
      )
      .bind(id)
      .run();
    return changes(res) === 1;
  }
}

export type { SessionIdentity };

/** The production store serves both seams (identity + session lookup). */
export type IdentitySessionStore = IdentityStore & SessionStore;
