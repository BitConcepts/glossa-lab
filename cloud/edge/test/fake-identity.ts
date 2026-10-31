// In-memory IdentityStore + SessionStore for Step 2 tests.
//
// Same semantics as D1IdentityStore, including the atomic gates:
// consumeInvite / completeSetup / revokeInvite do their
// check-and-mutate with no intervening await, which in JS is the
// in-memory equivalent of the single conditional UPDATE in D1.
// All rows are public so tests can assert hash-only storage directly.

import type {
  AuditRow,
  IdentityStore,
  InviteRow,
  SessionRow,
  SetupStateRow,
  UserRow,
  WorkspaceRow,
} from "../src/identity-store";
import type { SessionIdentity, SessionStore } from "../src/session-store";
import { sessionExpiryIso } from "../src/session";
import type { WorkspaceRole } from "../src/types";

export class InMemoryIdentityStore implements IdentityStore, SessionStore {
  users: UserRow[] = [];
  invites: InviteRow[] = [];
  sessions: SessionRow[] = [];
  workspaces: WorkspaceRow[] = [];
  roles = new Map<string, Record<string, WorkspaceRole>>(); // userId -> {wsId: role}
  audit: AuditRow[] = [];
  setup: SetupStateRow = {
    setupCodeHash: null,
    setupCodeExpiresAt: null,
    completedAt: null,
    username: null,
    email: null,
  };

  // --- SessionStore ---
  async findIdentityByTokenHash(
    tokenHash: string,
    now: Date,
  ): Promise<SessionIdentity | null> {
    const session = this.sessions.find(
      (s) =>
        s.tokenHash === tokenHash &&
        !s.revokedAt &&
        s.expiresAt > now.toISOString(),
    );
    if (!session) return null;
    const user = this.users.find((u) => u.id === session.userId);
    if (!user || user.status !== "active" || user.removedAt) return null;
    return {
      userId: user.id,
      username: user.username,
      globalType: user.globalType,
      workspaceRoles: { ...(this.roles.get(user.id) ?? {}) },
    };
  }

  async touchSession(tokenHash: string, now: Date): Promise<void> {
    const session = this.sessions.find(
      (s) => s.tokenHash === tokenHash && !s.revokedAt,
    );
    if (session) {
      session.lastSeenAt = now.toISOString();
      session.expiresAt = sessionExpiryIso(now);
    }
  }

  // --- audit ---
  async appendAudit(row: AuditRow): Promise<void> {
    this.audit.push({ ...row, detail: { ...row.detail } });
  }
  async listAudit(filter: {
    event?: string;
    actorId?: string;
    limit: number;
    offset: number;
  }): Promise<AuditRow[]> {
    const rows = this.audit.filter(
      (r) =>
        (!filter.event || r.event === filter.event) &&
        (!filter.actorId || r.actorId === filter.actorId),
    );
    // Newest first; id breaks ties the same way the D1 read does.
    const sorted = [...rows].sort((a, b) =>
      a.ts === b.ts ? (a.id < b.id ? 1 : -1) : a.ts < b.ts ? 1 : -1,
    );
    return sorted
      .slice(filter.offset, filter.offset + filter.limit)
      .map((r) => ({ ...r, detail: { ...r.detail } }));
  }

  // --- setup ---
  async getSetupState(): Promise<SetupStateRow | null> {
    return { ...this.setup };
  }
  async hasAdminOrOwner(): Promise<boolean> {
    return this.users.some(
      (u) => u.globalType === "owner" || u.globalType === "admin",
    );
  }
  async completeSetup(codeHash: string, nowIso: string): Promise<boolean> {
    if (
      this.setup.completedAt ||
      this.setup.setupCodeHash !== codeHash ||
      !this.setup.setupCodeExpiresAt ||
      this.setup.setupCodeExpiresAt <= nowIso
    ) {
      return false;
    }
    this.setup.completedAt = nowIso;
    return true;
  }

  // --- invites ---
  async createInvite(row: InviteRow): Promise<void> {
    this.invites.push({ ...row, workspaceGrants: { ...row.workspaceGrants } });
  }
  async listInvites(): Promise<InviteRow[]> {
    return [...this.invites].reverse();
  }
  async getInviteById(id: string): Promise<InviteRow | null> {
    const found = this.invites.find((i) => i.id === id);
    return found ? { ...found, workspaceGrants: { ...found.workspaceGrants } } : null;
  }
  async peekInviteByHash(codeHash: string): Promise<InviteRow | null> {
    const found = this.invites.find((i) => i.codeHash === codeHash);
    return found ? { ...found, workspaceGrants: { ...found.workspaceGrants } } : null;
  }
  async consumeInvite(
    codeHash: string,
    userId: string,
    nowIso: string,
  ): Promise<boolean> {
    const invite = this.invites.find((i) => i.codeHash === codeHash);
    if (
      !invite ||
      invite.redeemedAt ||
      invite.revokedAt ||
      invite.expiresAt <= nowIso
    ) {
      return false;
    }
    invite.redeemedBy = userId;
    invite.redeemedAt = nowIso;
    return true;
  }
  async revokeInvite(id: string, nowIso: string) {
    const invite = this.invites.find((i) => i.id === id);
    if (!invite) return "not_found" as const;
    if (invite.redeemedAt) return "redeemed" as const;
    if (invite.revokedAt) return "revoked" as const;
    invite.revokedAt = nowIso;
    return "ok" as const;
  }

  // --- users ---
  async createUser(row: UserRow): Promise<void> {
    this.users.push({ ...row });
  }
  // Reads return copies, like D1 rows — a caller holding a row must
  // not see later mutations through the reference.
  async findUserByUsername(usernameLower: string): Promise<UserRow | null> {
    const found = this.users.find(
      (u) => u.username.toLowerCase() === usernameLower,
    );
    return found ? { ...found } : null;
  }
  async findUserById(id: string): Promise<UserRow | null> {
    const found = this.users.find((u) => u.id === id);
    return found ? { ...found } : null;
  }
  async listUsers(): Promise<UserRow[]> {
    return this.users.map((u) => ({ ...u }));
  }
  async updateUserGlobalType(
    id: string,
    globalType: UserRow["globalType"],
  ): Promise<void> {
    const u = this.users.find((x) => x.id === id);
    if (u) u.globalType = globalType;
  }
  async setUserStatus(id: string, status: UserRow["status"]): Promise<void> {
    const u = this.users.find((x) => x.id === id);
    if (u) u.status = status;
  }
  async markUserRemoved(id: string, nowIso: string): Promise<void> {
    const u = this.users.find((x) => x.id === id);
    if (u) {
      u.removedAt = nowIso;
      u.status = "disabled";
    }
  }
  async updateUserEmail(id: string, email: string | null): Promise<void> {
    const u = this.users.find((x) => x.id === id);
    if (u) u.email = email;
  }
  async updateUserPasswordHash(id: string, passwordHash: string): Promise<void> {
    const u = this.users.find((x) => x.id === id);
    if (u) u.passwordHash = passwordHash;
  }

  // --- sessions ---
  async createSession(row: SessionRow): Promise<void> {
    this.sessions.push({ ...row });
  }
  async deleteSessionsForUser(userId: string): Promise<void> {
    this.sessions = this.sessions.filter((s) => s.userId !== userId);
  }
  async deleteSessionByTokenHash(tokenHash: string): Promise<void> {
    this.sessions = this.sessions.filter((s) => s.tokenHash !== tokenHash);
  }
  async listSessionsForUser(userId: string): Promise<SessionRow[]> {
    return this.sessions
      .filter((s) => s.userId === userId && !s.revokedAt)
      .map((s) => ({ ...s }))
      .sort((a, b) => (a.lastSeenAt < b.lastSeenAt ? 1 : -1));
  }
  async deleteSessionById(userId: string, sessionId: string): Promise<boolean> {
    const before = this.sessions.length;
    this.sessions = this.sessions.filter(
      (s) => !(s.id === sessionId && s.userId === userId),
    );
    return this.sessions.length !== before;
  }

  // --- workspaces + roles ---
  async createWorkspace(row: WorkspaceRow): Promise<void> {
    this.workspaces.push({ ...row });
  }
  async listWorkspaces(): Promise<WorkspaceRow[]> {
    return this.workspaces.map((w) => ({ ...w }));
  }
  async getWorkspaceById(id: string): Promise<WorkspaceRow | null> {
    const found = this.workspaces.find((w) => w.id === id);
    return found ? { ...found } : null;
  }
  async getWorkspaceBySlug(slug: string): Promise<WorkspaceRow | null> {
    const found = this.workspaces.find((w) => w.slug === slug);
    return found ? { ...found } : null;
  }
  async archiveWorkspace(id: string, nowIso: string): Promise<boolean> {
    const ws = this.workspaces.find((w) => w.id === id);
    if (!ws || ws.archivedAt) return false;
    ws.archivedAt = nowIso;
    return true;
  }
  async getWorkspaceRoles(
    userId: string,
  ): Promise<Record<string, WorkspaceRole>> {
    return { ...(this.roles.get(userId) ?? {}) };
  }
  async replaceWorkspaceRoles(
    userId: string,
    roles: Record<string, WorkspaceRole>,
  ): Promise<void> {
    this.roles.set(userId, { ...roles });
  }
  async findWorkspaceOwner(workspaceId: string): Promise<string | null> {
    for (const [userId, roles] of this.roles) {
      if (roles[workspaceId] === "owner") return userId;
    }
    return null;
  }
  async listWorkspaceMembers(workspaceId: string) {
    const out: { userId: string; username: string; role: WorkspaceRole }[] = [];
    for (const [userId, roles] of this.roles) {
      const role = roles[workspaceId];
      if (!role) continue;
      const user = this.users.find((u) => u.id === userId);
      out.push({ userId, username: user?.username ?? userId, role });
    }
    return out.sort((a, b) => (a.username < b.username ? -1 : 1));
  }
}

/** Fast deterministic hasher for API-flow tests (real Argon2id is
 *  exercised separately in password.test-scale tests). NOT for prod. */
export class FakeHasher {
  async hash(password: string): Promise<string> {
    const digest = await sha256HexForTest(`fake-salt:${password}`);
    return `fake$${digest}`;
  }
  async verify(password: string, encodedHash: string): Promise<boolean> {
    if (encodedHash.startsWith("$argon2id$")) return false;
    return (await this.hash(password)) === encodedHash;
  }
}

import { sha256Hex } from "../src/session";
async function sha256HexForTest(value: string): Promise<string> {
  return sha256Hex(value);
}
