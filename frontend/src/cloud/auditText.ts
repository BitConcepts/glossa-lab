/**
 * Spec 083 (Step 3) — plain-language rendering of audit entries
 * (wireframes 06 + 08). The edge stores events + small detail
 * objects; this module turns them into the wireframe's sentences.
 * It renders ONLY what the record carries — a failed sign-in, for
 * example, deliberately does not record which part was wrong, so
 * the sentence does not guess.
 */

import type { AuditEntry } from "./types";
import { fmtDay } from "./fmt";

export interface AuditContext {
  /** user id -> username */
  usernames: ReadonlyMap<string, string>;
  /** workspace id -> name */
  workspaceNames: ReadonlyMap<string, string>;
}

export type AuditClass = "logins" | "invites" | "user-changes" | "publishes" | "other";

const CLASS_BY_EVENT: Record<string, AuditClass> = {
  login_success: "logins",
  login_failure: "logins",
  logout: "logins",
  invite_created: "invites",
  invite_redeemed: "invites",
  invite_revoked: "invites",
  setup_completed: "user-changes",
  user_type_changed: "user-changes",
  user_type_change_refused: "user-changes",
  user_disabled: "user-changes",
  user_enabled: "user-changes",
  user_removed: "user-changes",
  workspace_matrix_changed: "user-changes",
  workspace_created: "user-changes",
  workspace_archived: "user-changes",
  workspace_restored: "user-changes",
  workspace_updated: "user-changes",
  account_email_changed: "user-changes",
  password_changed: "user-changes",
  session_revoked: "user-changes",
  admin_api_denial: "user-changes",
  container_scope_denial: "user-changes",
  dataset_published: "publishes",
  dataset_publish_failed: "publishes",
};

export function auditClassOf(event: string): AuditClass {
  return CLASS_BY_EVENT[event] ?? "other";
}

const LABEL: Record<string, string> = {
  login_success: "login",
  login_failure: "login failed",
  logout: "logout",
  invite_created: "invite created",
  invite_redeemed: "invite redeemed",
  invite_revoked: "invite revoked",
  setup_completed: "setup completed",
  user_type_changed: "user type changed",
  user_type_change_refused: "user type change refused",
  user_disabled: "user disabled",
  user_enabled: "user enabled",
  user_removed: "user removed",
  workspace_matrix_changed: "workspace access changed",
  workspace_created: "workspace created",
  workspace_archived: "workspace archived",
  workspace_restored: "workspace restored",
  workspace_updated: "workspace updated",
  account_email_changed: "email changed",
  password_changed: "password changed",
  session_revoked: "session revoked",
  admin_api_denial: "admin access refused",
  container_scope_denial: "container scope refusal",
  dataset_published: "dataset published",
  dataset_publish_failed: "dataset publish failed",
};

export function auditLabel(event: string): string {
  return LABEL[event] ?? event.replace(/_/g, " ");
}

/** Short titles for the account screen's own-activity list. */
const ACTIVITY_TITLE: Record<string, string> = {
  login_success: "Signed in",
  login_failure: "Failed sign-in attempt",
  logout: "Signed out",
  invite_created: "Created an invite",
  invite_redeemed: "Account created (invite redeemed)",
  setup_completed: "Account created (first-run setup)",
  password_changed: "Changed password",
  account_email_changed: "Changed email",
  session_revoked: "Revoked a session",
  workspace_created: "Created a workspace",
  workspace_matrix_changed: "Changed workspace access",
  user_type_changed: "Changed a user's type",
  user_disabled: "Disabled a user",
  user_enabled: "Re-enabled a user",
  user_removed: "Removed a user",
  invite_revoked: "Revoked an invite",
};

export function activityTitle(event: string): string {
  return ACTIVITY_TITLE[event] ?? auditLabel(event);
}

function wsNames(
  grants: Record<string, unknown> | undefined,
  ctx: AuditContext,
): string {
  if (!grants) return "no workspace";
  const names = Object.keys(grants).map((id) => ctx.workspaceNames.get(id) ?? id);
  return names.length ? names.join(", ") : "no workspace";
}

function str(v: unknown): string {
  return typeof v === "string" ? v : "";
}

export function describeAudit(e: AuditEntry, ctx: AuditContext): string {
  const d = e.detail ?? {};
  switch (e.event) {
    case "login_success":
      return "Signed in (success).";
    case "login_failure":
      // The record carries the presented username and nothing about
      // which part failed — deliberately (no oracle). Say exactly that.
      return `Sign-in failed${str(d.username) ? ` for ${str(d.username)}` : ""}. The record does not say which part was wrong.`;
    case "logout":
      return "Signed out.";
    case "invite_created":
      return `Invite for ${wsNames(d.workspace_grants as Record<string, unknown>, ctx)}${d.expires_at ? `, expires ${fmtDay(str(d.expires_at))}` : ""}${str(d.email) ? `; email noted (${str(d.email)})` : ""}.`;
    case "invite_redeemed":
      return `Account created for ${str(d.username) || e.actor_label}.`;
    case "invite_revoked":
      return "Outstanding invite withdrawn before use.";
    case "setup_completed":
      return "First-run setup created the owner account.";
    case "user_type_changed":
      return `Global type changed from ${str(d.from) || "?"} to ${str(d.to) || "?"}.`;
    case "user_type_change_refused":
      return `Global type change refused${str(d.reason) ? ` (${str(d.reason).replace(/_/g, " ")})` : ""}.`;
    case "user_disabled":
      return "Account disabled; its sessions ended immediately.";
    case "user_enabled":
      return "Account re-enabled.";
    case "user_removed":
      return "Account removed; past work stays attributed to the name.";
    case "workspace_matrix_changed": {
      const from = (d.from ?? {}) as Record<string, unknown>;
      const to = (d.to ?? {}) as Record<string, unknown>;
      const ids = [...new Set([...Object.keys(from), ...Object.keys(to)])];
      if (!ids.length) return "Workspace access changed.";
      const parts = ids.map(
        (id) =>
          `${ctx.workspaceNames.get(id) ?? id}: ${str(from[id]) || "no access"} → ${str(to[id]) || "no access"}`,
      );
      return `Workspace access changed — ${parts.join("; ")}.`;
    }
    case "workspace_created":
      return `Workspace created: ${str(d.name) || e.target || ""}.`;
    case "workspace_archived":
      return "Workspace archived; members lose access at their next request, the record is kept.";
    case "workspace_restored":
      return "Workspace restored from archive.";
    case "workspace_updated":
      return "Workspace name or description changed.";
    case "account_email_changed":
      return `Email changed${str(d.to) ? ` to ${str(d.to)}` : " (cleared)"}.`;
    case "password_changed":
      return "Password changed; every other session was signed out.";
    case "session_revoked":
      return "A session was revoked.";
    case "admin_api_denial":
      return `Admin surface refused${str(d.route) ? ` (${str(d.route)})` : ""} — the actor is not an admin.`;
    case "container_scope_denial":
      return `The workspace boundary refused a request (${str(d.method)} ${str(d.path)} → ${String(d.status ?? "")}).`;
    case "dataset_published":
      return `Dataset bundle ${str(d.bundle_id) || ""} published${str(d.source_commit) ? ` · source commit ${str(d.source_commit).slice(0, 8)}` : ""}.`;
    case "dataset_publish_failed":
      return `Dataset publish BLOCKED by the marker scan${str(d.bundle_id) ? ` (bundle ${str(d.bundle_id)})` : ""}. A blocked publish is a recorded event, not a silent one.`;
    default: {
      const keys = Object.keys(d);
      if (!keys.length) return "—";
      return keys.map((k) => `${k}: ${String(d[k])}`).join(" · ");
    }
  }
}
