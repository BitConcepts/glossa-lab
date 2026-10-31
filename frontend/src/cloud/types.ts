/**
 * Spec 083 (Step 3) — types for the cloud edition's edge API.
 *
 * These mirror the edge Worker's JSON shapes (cloud/edge/src/
 * identity.ts): snake_case fields, exactly as served. The cloud
 * session is a cookie — no type here ever carries a credential.
 */

export type GlobalType = "owner" | "admin" | "member" | "guest";
export type WorkspaceRole = "owner" | "admin" | "member" | "viewer";

export interface CloudUser {
  id: string;
  username: string;
  email: string | null;
  global_type: GlobalType;
  status: "active" | "disabled";
  removed: boolean;
  created_at: string;
  removed_at: string | null;
  workspace_roles?: Record<string, WorkspaceRole>;
}

/** A workspace as the session read shapes it for one signed-in user. */
export interface SessionWorkspace {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  archived_at: string | null;
  created_by: string;
  created_at: string;
  /** The caller's effective role: stored grant or implicit admin. */
  role: WorkspaceRole;
  role_source: "stored" | "implicit";
}

export interface SessionResponse {
  user: CloudUser;
  implicit_workspace_admin: boolean;
  workspaces: SessionWorkspace[];
}

export type InviteState = "open" | "redeemed" | "revoked" | "expired" | "invalid";

export interface InvitePreview {
  state: InviteState;
  email?: string | null;
  expires_at?: string;
  created_by?: { username: string; global_type: GlobalType } | null;
  workspaces?: { id: string; name: string; role: WorkspaceRole }[];
}

export interface AdminUser extends CloudUser {
  workspace_roles: Record<string, WorkspaceRole>;
}

export interface AdminInvite {
  id: string;
  email: string | null;
  workspace_grants: Record<string, WorkspaceRole>;
  created_at: string;
  expires_at: string;
  revoked_at: string | null;
  redeemed_by: string | null;
  redeemed_at: string | null;
  status: "outstanding" | "redeemed" | "revoked" | "expired";
}

export interface AdminWorkspaceMember {
  user_id: string;
  username: string;
  role: WorkspaceRole;
}

export interface AdminWorkspace {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  archived_at: string | null;
  created_by: string;
  created_at: string;
  member_count: number;
  members: AdminWorkspaceMember[];
  your_role: WorkspaceRole | null;
  your_role_source: "stored" | "implicit" | null;
}

export interface AuditEntry {
  id: string;
  ts: string;
  actor_id: string | null;
  actor_label: string;
  event: string;
  target: string | null;
  detail: Record<string, unknown>;
}

export interface AccountSession {
  id: string;
  created_at: string;
  last_seen_at: string;
  expires_at: string;
  current: boolean;
}

export interface AccountView {
  user: CloudUser;
  sessions: AccountSession[];
  activity: AuditEntry[];
}

/** The per-user access matrix (wireframe 10). */
export interface AccessMatrix {
  user_id: string;
  global_type: GlobalType;
  implicit_workspace_admin: boolean;
  workspace_roles: Record<string, WorkspaceRole>;
  workspaces: {
    id: string;
    name: string;
    slug: string;
    description: string | null;
    archived_at: string | null;
    role: WorkspaceRole | null;
  }[];
}
