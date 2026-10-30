// The session-store seam (Spec 083, Step 1 / T009).
//
// Phase 1 ships the interface and the D1-backed implementation of the
// lookup the perimeter needs: given a session token hash, resolve the
// authenticated identity (user + global type + per-workspace roles).
// Phase 2 (Step 2, T016/T018) builds the full identity logic — login,
// logout, issuance, revocation cascades — on top of this same store.
//
// A session authenticates only when ALL of these hold:
//   - a sessions row matches the token hash,
//   - the session is not revoked and not expired,
//   - the user is active and not removed (disable/removal kills every
//     session on the very next request, FR-004).

import type { GlobalType, WorkspaceRole } from "./types";

export interface SessionIdentity {
  userId: string;
  username: string;
  globalType: GlobalType;
  /** Map of workspace id -> the user's role in that workspace. */
  workspaceRoles: Record<string, WorkspaceRole>;
}

export interface SessionStore {
  findIdentityByTokenHash(
    tokenHash: string,
    now: Date,
  ): Promise<SessionIdentity | null>;
  /** Best-effort sliding-activity stamp (last_seen_at). */
  touchSession(tokenHash: string, now: Date): Promise<void>;
}

interface SessionUserRow {
  user_id: string;
  username: string;
  global_type: GlobalType;
}

interface WorkspaceRoleRow {
  workspace_id: string;
  role: WorkspaceRole;
}

export class D1SessionStore implements SessionStore {
  constructor(private readonly db: D1Database) {}

  async findIdentityByTokenHash(
    tokenHash: string,
    now: Date,
  ): Promise<SessionIdentity | null> {
    const row = await this.db
      .prepare(
        `SELECT u.id AS user_id, u.username AS username, u.global_type AS global_type
           FROM sessions AS s
           JOIN users AS u ON u.id = s.user_id
          WHERE s.token_hash = ?
            AND s.revoked_at IS NULL
            AND s.expires_at > ?
            AND u.status = 'active'
            AND u.removed_at IS NULL`,
      )
      .bind(tokenHash, now.toISOString())
      .first<SessionUserRow>();
    if (!row) return null;

    const roles = await this.db
      .prepare(
        `SELECT workspace_id, role FROM workspace_roles WHERE user_id = ?`,
      )
      .bind(row.user_id)
      .all<WorkspaceRoleRow>();

    const workspaceRoles: Record<string, WorkspaceRole> = {};
    for (const r of roles.results ?? []) {
      workspaceRoles[r.workspace_id] = r.role;
    }
    return {
      userId: row.user_id,
      username: row.username,
      globalType: row.global_type,
      workspaceRoles,
    };
  }

  async touchSession(tokenHash: string, now: Date): Promise<void> {
    await this.db
      .prepare(
        `UPDATE sessions SET last_seen_at = ?
          WHERE token_hash = ? AND revoked_at IS NULL`,
      )
      .bind(now.toISOString(), tokenHash)
      .run();
  }
}
