/**
 * Spec 083 (Step 3) — client for the edge Worker's identity API.
 *
 * Every call is same-origin with `credentials: "same-origin"`: the
 * edge session is an HttpOnly cookie the browser sends on its own.
 * This client NEVER sets an Authorization header — the Spec 082 API
 * token belongs to the desktop surface and is refused at the edge
 * (Amendment 5); attaching it here would be a credential-confusion
 * bug, not a convenience.
 */

import type {
  AccessMatrix,
  AccountView,
  AdminInvite,
  AdminUser,
  AdminWorkspace,
  AuditEntry,
  CloudUser,
  GlobalType,
  InvitePreview,
  SessionResponse,
  WorkspaceRole,
} from "./types";

export class CloudApiError extends Error {
  status: number;
  code: string;
  constructor(status: number, code: string, message: string) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

async function cloudFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    ...init,
    credentials: "same-origin",
    headers: {
      ...(init?.body ? { "Content-Type": "application/json" } : {}),
      ...(init?.headers ?? {}),
    },
  });
  const text = await res.text().catch(() => "");
  let data: unknown = null;
  if (text) {
    try { data = JSON.parse(text); } catch { data = null; }
  }
  if (!res.ok) {
    const err = (data as { error?: { code?: string; message?: string } } | null)?.error;
    throw new CloudApiError(
      res.status,
      err?.code ?? "request_failed",
      err?.message ?? `Request failed (${res.status}).`,
    );
  }
  return data as T;
}

const post = (body: unknown): RequestInit => ({
  method: "POST",
  body: JSON.stringify(body),
});

// ── Session / auth pages ────────────────────────────────────────────────────

export const getSession = (): Promise<SessionResponse> =>
  cloudFetch<SessionResponse>("/api/session");

export const login = (username: string, password: string): Promise<{ user: CloudUser }> =>
  cloudFetch("/login", post({ username, password }));

export const logout = (): Promise<{ ok: boolean }> =>
  cloudFetch("/logout", { method: "POST" });

export const getInvitePreview = (code: string): Promise<InvitePreview> =>
  cloudFetch<InvitePreview>(`/invite/${encodeURIComponent(code)}/preview`);

export const redeemInvite = (
  code: string,
  body: { username: string; email?: string; password: string },
): Promise<{ user: CloudUser }> =>
  cloudFetch(`/invite/${encodeURIComponent(code)}/redeem`, post(body));

export const completeSetup = (
  code: string,
  password: string,
): Promise<{ user: CloudUser }> =>
  cloudFetch("/setup", post({ code, password }));

/**
 * Whether the one-time glassbreak setup is still open. The edge
 * serves the SPA shell (200, HTML) while setup is open and a JSON
 * 404 once it has completed — the status alone is the signal.
 */
export async function probeSetupOpen(): Promise<boolean> {
  try {
    const res = await fetch("/setup", { credentials: "same-origin" });
    return res.status === 200;
  } catch {
    return false;
  }
}

// ── Account self-service (wireframe 08) ─────────────────────────────────────

export const getAccount = (): Promise<AccountView> =>
  cloudFetch<AccountView>("/api/account");

export const changeEmail = (email: string): Promise<{ user: CloudUser }> =>
  cloudFetch("/api/account/email", post({ email }));

export const changePassword = (
  currentPassword: string,
  newPassword: string,
): Promise<{ ok: boolean }> =>
  cloudFetch("/api/account/password", post({
    current_password: currentPassword,
    new_password: newPassword,
  }));

export const revokeSession = (sessionId: string): Promise<{ ok: boolean }> =>
  cloudFetch(`/api/account/sessions/${encodeURIComponent(sessionId)}/revoke`, {
    method: "POST",
  });

// ── Admin surface (wireframes 04–06, 09, 10) ────────────────────────────────

export const listAdminUsers = (): Promise<{ users: AdminUser[] }> =>
  cloudFetch("/api/admin/users");

export const setUserGlobalType = (
  userId: string,
  globalType: GlobalType,
): Promise<{ user: AdminUser }> =>
  cloudFetch(`/api/admin/users/${encodeURIComponent(userId)}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ global_type: globalType }),
  });

export const disableUser = (userId: string): Promise<{ user: AdminUser }> =>
  cloudFetch(`/api/admin/users/${encodeURIComponent(userId)}/disable`, { method: "POST" });

export const enableUser = (userId: string): Promise<{ user: AdminUser }> =>
  cloudFetch(`/api/admin/users/${encodeURIComponent(userId)}/enable`, { method: "POST" });

export const removeUser = (userId: string): Promise<{ user: AdminUser }> =>
  cloudFetch(`/api/admin/users/${encodeURIComponent(userId)}/remove`, { method: "POST" });

export const getAccessMatrix = (userId: string): Promise<AccessMatrix> =>
  cloudFetch(`/api/admin/users/${encodeURIComponent(userId)}/workspaces`);

export const putAccessMatrix = (
  userId: string,
  roles: Record<string, WorkspaceRole>,
): Promise<AccessMatrix> =>
  cloudFetch(`/api/admin/users/${encodeURIComponent(userId)}/workspaces`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ workspace_roles: roles }),
  });

export const listAdminInvites = (): Promise<{ invites: AdminInvite[] }> =>
  cloudFetch("/api/admin/invites");

export const createInvite = (body: {
  email?: string;
  workspace_grants: Record<string, WorkspaceRole>;
  expires_in_days?: number;
}): Promise<{ invite: AdminInvite; code: string; invite_url: string }> =>
  cloudFetch("/api/admin/invites", post(body));

export const revokeInvite = (inviteId: string): Promise<{ invite: AdminInvite }> =>
  cloudFetch(`/api/admin/invites/${encodeURIComponent(inviteId)}/revoke`, { method: "POST" });

export const listAdminWorkspaces = (): Promise<{ workspaces: AdminWorkspace[] }> =>
  cloudFetch("/api/admin/workspaces");

export const createWorkspace = (body: {
  name: string;
  description?: string;
}): Promise<{ workspace: AdminWorkspace }> =>
  cloudFetch("/api/admin/workspaces", post(body));

export const archiveWorkspace = (
  workspaceId: string,
): Promise<{ workspace: AdminWorkspace }> =>
  cloudFetch(`/api/admin/workspaces/${encodeURIComponent(workspaceId)}/archive`, {
    method: "POST",
  });

export const listAudit = (params: {
  event?: string;
  actorId?: string;
  limit?: number;
  offset?: number;
} = {}): Promise<{ entries: AuditEntry[]; limit: number; offset: number }> => {
  const q = new URLSearchParams();
  if (params.event) q.set("event", params.event);
  if (params.actorId) q.set("actor_id", params.actorId);
  if (params.limit) q.set("limit", String(params.limit));
  if (params.offset) q.set("offset", String(params.offset));
  const qs = q.toString();
  return cloudFetch(`/api/admin/audit${qs ? `?${qs}` : ""}`);
};
