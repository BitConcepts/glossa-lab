/**
 * Spec 083 (Step 3, T026) — the admin surface: one screen, four
 * tabs (Users / Workspaces / Invites / Audit log), plus the
 * per-user workspace-access matrix as a drill-in (wireframes
 * 04–06, 09, 10). Every action here is written to the audit log by
 * the edge; the ledes say so where the actions happen.
 *
 * Named deviation (BUILD-RECORD): wireframe 04's Manage menu lists
 * "issue a password-reset link", but the Phase 2 identity API has
 * no reset-link flow — the shipped recovery path is disable +
 * re-invite, so the menu omits the item rather than faking it.
 */

import { Fragment, useCallback, useEffect, useMemo, useState } from "react";
import {
  archiveWorkspace,
  createInvite,
  createWorkspace,
  disableUser,
  enableUser,
  getAccessMatrix,
  listAdminInvites,
  listAdminUsers,
  listAdminWorkspaces,
  listAudit,
  putAccessMatrix,
  removeUser,
  restoreWorkspace,
  revokeInvite,
  setUserGlobalType,
  updateWorkspace,
} from "./api";
import {
  inviteState,
  type AccessMatrix,
  type AdminInvite,
  type AdminUser,
  type AdminWorkspace,
  type AuditEntry,
  type GlobalType,
  type WorkspaceRole,
} from "./types";
import { auditClassOf, auditLabel, describeAudit, type AuditClass, type AuditContext } from "./auditText";
import { fmtDay, fmtWhenShort } from "./fmt";
import { useCloudSession } from "./session";

const PRIMARY_SLUG = "indus-script";
const AUDIT_PAGE = 200;

type AdminTab = "users" | "workspaces" | "invites" | "audit";

const TYPE_CHIP: Record<GlobalType, string> = {
  owner: "",
  admin: "",
  member: "grey",
  guest: "amber",
};

function TypeChip({ type }: { type: GlobalType }) {
  return <span className={`cl-chip ${TYPE_CHIP[type]}`}>{type}</span>;
}

function StatusChip({ user }: { user: AdminUser }) {
  if (user.removed) return <span className="cl-chip red">removed</span>;
  if (user.status === "disabled") return <span className="cl-chip amber">disabled</span>;
  return <span className="cl-chip green">active</span>;
}

export function AdminView() {
  const cloud = useCloudSession();
  // The workspace switcher's "manage in Admin · Workspaces" entry
  // stashes the intended tab (the shell's evidence-tab pattern).
  const [tab, setTab] = useState<AdminTab>(() => {
    try {
      const hint = sessionStorage.getItem("glossa_admin_tab");
      if (hint === "workspaces" || hint === "invites" || hint === "audit") {
        sessionStorage.removeItem("glossa_admin_tab");
        return hint;
      }
    } catch { /* */ }
    return "users";
  });
  const [users, setUsers] = useState<AdminUser[] | null>(null);
  const [invites, setInvites] = useState<AdminInvite[] | null>(null);
  const [workspaces, setWorkspaces] = useState<AdminWorkspace[] | null>(null);
  const [audit, setAudit] = useState<AuditEntry[]>([]);
  const [auditHasMore, setAuditHasMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [matrixUserId, setMatrixUserId] = useState<string | null>(null);
  const [inviteSeed, setInviteSeed] = useState(0); // bump to open the invite form

  const reloadUsers = useCallback(async () => {
    setUsers((await listAdminUsers()).users);
  }, []);
  const reloadInvites = useCallback(async () => {
    setInvites((await listAdminInvites()).invites);
  }, []);
  const reloadWorkspaces = useCallback(async () => {
    setWorkspaces((await listAdminWorkspaces()).workspaces);
  }, []);
  const reloadAudit = useCallback(async () => {
    const page = await listAudit({ limit: AUDIT_PAGE, offset: 0 });
    setAudit(page.entries);
    setAuditHasMore(page.entries.length === AUDIT_PAGE);
  }, []);
  const loadMoreAudit = useCallback(async () => {
    const page = await listAudit({ limit: AUDIT_PAGE, offset: audit.length });
    setAudit((prev) => [...prev, ...page.entries]);
    setAuditHasMore(page.entries.length === AUDIT_PAGE);
  }, [audit.length]);

  useEffect(() => {
    let live = true;
    (async () => {
      try {
        await Promise.all([reloadUsers(), reloadInvites(), reloadWorkspaces(), reloadAudit()]);
      } catch (e) {
        if (live) setError(e instanceof Error ? e.message : "The admin data could not be loaded.");
      }
    })();
    return () => { live = false; };
  }, [reloadUsers, reloadInvites, reloadWorkspaces, reloadAudit]);

  const ctx: AuditContext = useMemo(() => ({
    usernames: new Map((users ?? []).map((u) => [u.id, u.username])),
    workspaceNames: new Map((workspaces ?? []).map((w) => [w.id, w.name])),
  }), [users, workspaces]);

  const lastActive = useMemo(() => {
    const out = new Map<string, string>();
    for (const e of audit) {
      if (e.event === "login_success" && e.actor_id && !out.has(e.actor_id)) {
        out.set(e.actor_id, e.ts);
      }
    }
    return out;
  }, [audit]);

  const outstanding = (invites ?? []).filter((i) => inviteState(i) === "outstanding").length;

  const act = async (fn: () => Promise<unknown>, after?: () => Promise<void>) => {
    setError(null);
    try {
      await fn();
      await after?.();
      await reloadAudit();
    } catch (e) {
      setError(e instanceof Error ? e.message : "That action failed.");
    }
  };

  const matrixUser = matrixUserId ? (users ?? []).find((u) => u.id === matrixUserId) ?? null : null;

  return (
    <div className="cl-root">
      <div className="cl-screen">
        <h1>Admin</h1>
        <p className="cl-sub">
          {tab === "users" && "Who can use this Glossa Lab, what they can reach, and what they have done. Every action on these tabs is written to the audit log."}
          {tab === "workspaces" && "Workspaces are the tenancy unit of this edition: claims, evidence, jobs and membership all live inside one workspace, and no workspace sees another's data. Every action on this screen is written to the audit log."}
          {tab === "invites" && "An invite is a single-use link that creates one account with access to the workspaces you choose. You send the link yourself — by email, message, however you reach the person."}
          {tab === "audit" && "The append-only record of security-relevant events: who signed in, who was invited, what changed. Entries cannot be edited or deleted from any screen — including this one."}
        </p>
        {error && <div className="cl-form-error">{error}</div>}
        <div className="cl-tabs">
          <button className={tab === "users" ? "active" : ""} onClick={() => { setTab("users"); setMatrixUserId(null); }}>
            Users {users && <span className="cl-count">{users.filter((u) => !u.removed).length}</span>}
          </button>
          <button className={tab === "workspaces" ? "active" : ""} onClick={() => { setTab("workspaces"); setMatrixUserId(null); }}>
            Workspaces {workspaces && <span className="cl-count">{workspaces.length}</span>}
          </button>
          <button className={tab === "invites" ? "active" : ""} onClick={() => { setTab("invites"); setMatrixUserId(null); }}>
            Invites {invites && <span className="cl-count">{outstanding} outstanding</span>}
          </button>
          <button className={tab === "audit" ? "active" : ""} onClick={() => { setTab("audit"); setMatrixUserId(null); }}>
            Audit log
          </button>
        </div>

        {tab === "users" && (
          matrixUser ? (
            <AccessMatrixScreen
              user={matrixUser}
              selfId={cloud.user?.id ?? ""}
              lastActive={lastActive.get(matrixUser.id)}
              onBack={() => setMatrixUserId(null)}
              act={act}
              reloadUsers={reloadUsers}
            />
          ) : (
            <UsersTab
              users={users}
              workspaces={workspaces ?? []}
              selfId={cloud.user?.id ?? ""}
              lastActive={lastActive}
              onManage={(id) => setMatrixUserId(id)}
              onInvite={() => { setTab("invites"); setInviteSeed((n) => n + 1); }}
            />
          )
        )}
        {tab === "workspaces" && (
          <WorkspacesTab
            workspaces={workspaces}
            users={users ?? []}
            selfId={cloud.user?.id ?? ""}
            act={act}
            reloadWorkspaces={reloadWorkspaces}
            reloadUsers={reloadUsers}
          />
        )}
        {tab === "invites" && (
          <InvitesTab
            invites={invites}
            workspaces={workspaces ?? []}
            users={users ?? []}
            formSeed={inviteSeed}
            act={act}
            reloadInvites={reloadInvites}
          />
        )}
        {tab === "audit" && (
          <AuditTab
            entries={audit}
            users={users ?? []}
            ctx={ctx}
            hasMore={auditHasMore}
            onLoadMore={() => void loadMoreAudit()}
          />
        )}
      </div>
    </div>
  );
}

// ── Users (wireframe 04) ────────────────────────────────────────────────────

function UsersTab({
  users, workspaces, selfId, lastActive, onManage, onInvite,
}: {
  users: AdminUser[] | null;
  workspaces: AdminWorkspace[];
  selfId: string;
  lastActive: Map<string, string>;
  onManage: (id: string) => void;
  onInvite: () => void;
}) {
  if (!users) return <div className="cl-loading">Loading users…</div>;
  const wsName = (id: string) => workspaces.find((w) => w.id === id)?.name ?? id;
  return (
    <>
      <div className="cl-toolbar">
        <span className="cl-spacer" />
        <button className="cl-btn primary" style={{ width: "auto" }} onClick={onInvite}>+ Invite user</button>
      </div>
      <div className="cl-card" style={{ padding: "6px 8px" }}>
        <div className="cl-table-wrap">
          <table className="cl-table">
            <thead>
              <tr><th>User</th><th>Role</th><th>Status</th><th>Workspaces</th><th>Last active</th><th /></tr>
            </thead>
            <tbody>
              {users.map((u) => {
                const implicit = u.global_type === "admin" || u.global_type === "owner";
                const granted = Object.keys(u.workspace_roles ?? {});
                return (
                  <tr key={u.id}>
                    <td>
                      <strong>{u.username}</strong>
                      {u.id === selfId && <> <span className="cl-chip">you</span></>}
                      <div className="cl-muted cl-small">
                        {u.global_type === "owner"
                          ? `Admin account · created at first-run setup, ${fmtDay(u.created_at)}`
                          : u.removed
                            ? `Removed ${fmtDay(u.removed_at)} · work stays attributed to this name`
                            : `Joined ${fmtDay(u.created_at)}${u.email ? ` · ${u.email}` : ""}`}
                      </div>
                    </td>
                    <td><TypeChip type={u.global_type} /></td>
                    <td><StatusChip user={u} /></td>
                    <td className="cl-small">
                      {implicit ? "All workspaces" : granted.length ? granted.map(wsName).join(", ") : "—"}
                    </td>
                    <td className="cl-small">{u.id === selfId ? "now" : fmtWhenShort(lastActive.get(u.id))}</td>
                    <td>
                      <button className="cl-btn ghost small" onClick={() => onManage(u.id)}>Manage</button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
      <p className="cl-small cl-muted" style={{ lineHeight: 1.55 }}>
        Manage opens: workspace memberships (grant / remove per workspace) · make admin / make
        member · disable or re-enable · remove account. Removal keeps the person's past work
        attributed to their name, marked <em>removed</em> — history is not rewritten. Disabling
        ends their sessions immediately. Your own row offers no disable or remove: the edition
        cannot lock out its only admin.
      </p>
    </>
  );
}

// ── Access matrix (wireframe 10) ────────────────────────────────────────────

const ROLE_OPTIONS: (WorkspaceRole | "none")[] = ["owner", "admin", "member", "viewer", "none"];
const ROLE_LABEL: Record<WorkspaceRole | "none", string> = {
  owner: "Owner", admin: "Admin", member: "Member", viewer: "Viewer", none: "No access",
};

function effectiveResult(role: WorkspaceRole | "none", username: string): string {
  switch (role) {
    case "owner": return "Owns this workspace: full control, and the workspace's accountable owner.";
    case "admin": return "Full control inside this workspace, including managing its members.";
    case "member": return "Can read and work on claims and evidence in this workspace.";
    case "viewer": return "Read-only: can open and read, cannot change anything.";
    case "none": return `This workspace does not appear for ${username} — not in lists, search, or the switcher.`;
  }
}

function AccessMatrixScreen({
  user, selfId, lastActive, onBack, act, reloadUsers,
}: {
  user: AdminUser;
  selfId: string;
  lastActive?: string;
  onBack: () => void;
  act: (fn: () => Promise<unknown>, after?: () => Promise<void>) => Promise<void>;
  reloadUsers: () => Promise<void>;
}) {
  const [matrix, setMatrix] = useState<AccessMatrix | null>(null);
  const [draft, setDraft] = useState<Record<string, WorkspaceRole>>({});
  const [loadError, setLoadError] = useState<string | null>(null);
  const [typeDraft, setTypeDraft] = useState<GlobalType>(user.global_type);
  const [confirmRemove, setConfirmRemove] = useState(false);
  const isSelf = user.id === selfId;
  const isOwnerAccount = user.global_type === "owner";
  const isGuest = (matrix?.global_type ?? user.global_type) === "guest";

  useEffect(() => {
    let live = true;
    getAccessMatrix(user.id)
      .then((m) => {
        if (!live) return;
        setMatrix(m);
        setDraft({ ...m.workspace_roles });
      })
      .catch((e) => { if (live) setLoadError(e instanceof Error ? e.message : "Could not load access."); });
    return () => { live = false; };
  }, [user.id]);

  const dirty = useMemo(() => {
    if (!matrix) return false;
    const orig = matrix.workspace_roles;
    const keys = new Set([...Object.keys(orig), ...Object.keys(draft)]);
    for (const k of keys) if ((orig[k] ?? null) !== (draft[k] ?? null)) return true;
    return false;
  }, [matrix, draft]);

  const save = () =>
    act(async () => {
      const updated = await putAccessMatrix(user.id, draft);
      setMatrix(updated);
      setDraft({ ...updated.workspace_roles });
    });

  return (
    <>
      <button className="cl-btn ghost small" onClick={onBack}>← All users</button>
      <div style={{ margin: "14px 0 4px", display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
        <h2 style={{ fontSize: 17, margin: 0 }}>{user.username}</h2>
        {isSelf && <span className="cl-chip">you</span>}
        <TypeChip type={user.global_type} />
        <StatusChip user={user} />
      </div>
      <p className="cl-small cl-muted" style={{ marginTop: 0 }}>
        {user.global_type === "owner"
          ? `Admin account · created at first-run setup, ${fmtDay(user.created_at)}`
          : `Joined ${fmtDay(user.created_at)}${user.email ? ` · ${user.email}` : ""}`} · last active {isSelf ? "now" : fmtWhenShort(lastActive)}
      </p>
      <p className="cl-sub" style={{ marginBottom: 14 }}>
        One user, every workspace, the exact grant stored for each. A change here takes effect
        on that user's next request — there is no cached copy of access anywhere else to
        disagree with this grid.
      </p>

      {loadError && <div className="cl-form-error">{loadError}</div>}
      {isGuest && (
        <div className="cl-callout warn">
          <strong>Guests can hold Viewer only.</strong> A Guest account can be granted Viewer in
          a workspace, or No access — the Member, Admin and Owner options are disabled below and
          cannot be saved for this user. To give this person more, first change their global
          type below.
        </div>
      )}
      {matrix?.implicit_workspace_admin && (
        <div className="cl-callout info">
          This account's global type also carries <strong>implicit Workspace Admin</strong> in
          every workspace — that part is not a stored grant and does not appear in the grid;
          the grid shows stored grants only.
        </div>
      )}

      {!matrix ? (
        <div className="cl-loading">Loading workspace access…</div>
      ) : (
        <div className="cl-card" style={{ padding: "6px 8px" }}>
          <div className="cl-table-wrap">
            <table className="cl-table">
              <thead>
                <tr><th>Workspace</th><th>Role</th><th>Effective result</th></tr>
              </thead>
              <tbody>
                {matrix.workspaces.map((w) => {
                  const current = draft[w.id] ?? "none";
                  return (
                    <tr key={w.id}>
                      <td>
                        <strong>{w.name}</strong>
                        {w.slug === PRIMARY_SLUG && <> <span className="cl-chip">Primary</span></>}
                        <div className="cl-muted cl-small">
                          {w.archived_at
                            ? "Archived workspace — grants are kept, but the workspace itself is read-only in the record"
                            : "Active workspace"}
                        </div>
                      </td>
                      <td>
                        <div className="cl-radio-row" role="radiogroup" aria-label={`Role in ${w.name}`}>
                          {ROLE_OPTIONS.map((r) => {
                            const capped = isGuest && r !== "viewer" && r !== "none";
                            return (
                              <button
                                key={r}
                                className={`cl-rolepick${current === r ? " sel" : ""}`}
                                disabled={capped}
                                title={capped ? `${ROLE_LABEL[r]} — unavailable for Guests` : ROLE_LABEL[r]}
                                onClick={() => {
                                  setDraft((prev) => {
                                    const next = { ...prev };
                                    if (r === "none") delete next[w.id];
                                    else next[w.id] = r;
                                    return next;
                                  });
                                }}
                              >
                                {ROLE_LABEL[r]}{capped ? " — unavailable for Guests" : ""}
                              </button>
                            );
                          })}
                        </div>
                      </td>
                      <td className="cl-small" style={{ minWidth: 200 }}>{effectiveResult(current, user.username)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="cl-toolbar">
        <button className="cl-btn primary" style={{ width: "auto" }} disabled={!dirty} onClick={() => void save()}>
          Save changes
        </button>
        <span className="cl-small cl-muted">
          Every role change is written to the audit log with the old and new role. Lowering a
          role to No access ends that workspace for the user on their next request; work they
          already did there stays attributed to them.
        </span>
      </div>

      <div className="cl-card">
        <h2>Account actions</h2>
        <p className="cl-card-sub">Global type, availability, and removal for this account.</p>
        <div className="cl-toolbar" style={{ marginBottom: 8 }}>
          <label className="cl-small" htmlFor="cl-type-select"><strong>Global type</strong></label>
          <select
            id="cl-type-select"
            value={typeDraft}
            onChange={(e) => setTypeDraft(e.target.value as GlobalType)}
          >
            <option value="owner">owner</option>
            <option value="admin">admin</option>
            <option value="member">member</option>
            <option value="guest">guest</option>
          </select>
          <button
            className="cl-btn ghost small"
            disabled={typeDraft === user.global_type}
            onClick={() => void act(() => setUserGlobalType(user.id, typeDraft), reloadUsers)}
          >
            Change type
          </button>
        </div>
        <div className="cl-actions">
          {user.status === "disabled" && !user.removed ? (
            <button className="cl-btn ghost small" onClick={() => void act(() => enableUser(user.id), reloadUsers)}>
              Re-enable account
            </button>
          ) : (
            !isSelf && !isOwnerAccount && !user.removed && (
              <button className="cl-btn ghost small" onClick={() => void act(() => disableUser(user.id), reloadUsers)}>
                Disable account
              </button>
            )
          )}
          {!isSelf && !isOwnerAccount && !user.removed && (
            <button className="cl-btn danger small" onClick={() => setConfirmRemove(true)}>
              Remove account…
            </button>
          )}
          {(isSelf || isOwnerAccount) && (
            <span className="cl-small cl-muted">
              Disable and remove are not offered for {isSelf ? "your own account" : "the owner account"}:
              the edition cannot lock out its only admin path.
            </span>
          )}
        </div>
      </div>

      {confirmRemove && (
        <div className="cl-modal-veil" role="dialog" aria-modal="true">
          <div className="cl-modal">
            <h2>Remove {user.username}?</h2>
            <p className="cl-lede">
              The account is removed and its sessions end immediately. Work the person already
              did stays in the record, attributed to their name and marked <em>removed</em> —
              history is not rewritten. This cannot be undone from any screen.
            </p>
            <div className="cl-modal-actions">
              <button className="cl-btn ghost" onClick={() => setConfirmRemove(false)}>Cancel</button>
              <button
                className="cl-btn primary"
                style={{ background: "#b91c1c" }}
                onClick={() => {
                  setConfirmRemove(false);
                  void act(() => removeUser(user.id), async () => { await reloadUsers(); onBack(); });
                }}
              >
                Remove account
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// ── Workspaces (wireframe 09) ───────────────────────────────────────────────

function WorkspacesTab({
  workspaces, users, selfId, act, reloadWorkspaces, reloadUsers,
}: {
  workspaces: AdminWorkspace[] | null;
  users: AdminUser[];
  selfId: string;
  act: (fn: () => Promise<unknown>, after?: () => Promise<void>) => Promise<void>;
  reloadWorkspaces: () => Promise<void>;
  reloadUsers: () => Promise<void>;
}) {
  const [formOpen, setFormOpen] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [initial, setInitial] = useState<Record<string, WorkspaceRole | "">>({});
  const [banner, setBanner] = useState<string | null>(null);
  const [manageId, setManageId] = useState<string | null>(null);
  const [editName, setEditName] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [archiveTarget, setArchiveTarget] = useState<AdminWorkspace | null>(null);

  if (!workspaces) return <div className="cl-loading">Loading workspaces…</div>;

  const create = async () => {
    await act(async () => {
      const { workspace } = await createWorkspace({
        name: name.trim(),
        ...(description.trim() ? { description: description.trim() } : {}),
      });
      // Initial members (and the creator's Owner grant) are stored
      // grants like any other: merge each pick into that user's
      // existing matrix and PUT the full set.
      const grants: Record<string, WorkspaceRole> = {};
      for (const [userId, role] of Object.entries(initial)) {
        if (role) grants[userId] = role;
      }
      if (selfId) grants[selfId] = "owner";
      for (const [userId, role] of Object.entries(grants)) {
        if (!role) continue;
        const current = await getAccessMatrix(userId);
        await putAccessMatrix(userId, { ...current.workspace_roles, [workspace.id]: role });
      }
      setBanner(`Workspace “${workspace.name}” created.`);
      setFormOpen(false);
      setName("");
      setDescription("");
      setInitial({});
    }, async () => { await reloadWorkspaces(); await reloadUsers(); });
  };

  const openManage = (w: AdminWorkspace) => {
    setManageId(manageId === w.id ? null : w.id);
    setEditName(w.name);
    setEditDescription(w.description ?? "");
  };

  return (
    <>
      <div className="cl-toolbar">
        <span className="cl-spacer" />
        <button className="cl-btn primary" style={{ width: "auto" }} onClick={() => setFormOpen((v) => !v)}>
          + Create workspace
        </button>
      </div>
      {banner && <div className="cl-banner-ok">{banner}</div>}

      {formOpen && (
        <div className="cl-card">
          <h2>Create workspace</h2>
          <p className="cl-card-sub">An admin act; there is no member-facing create path.</p>
          <div className="cl-field">
            <label htmlFor="cl-ws-name">Name</label>
            <input id="cl-ws-name" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Comparative Scripts" />
          </div>
          <div className="cl-field">
            <label htmlFor="cl-ws-desc">Description</label>
            <input id="cl-ws-desc" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="The question or scope this workspace holds" />
            <div className="cl-hint">Shown on the workspace's card in the switcher.</div>
          </div>
          <div className="cl-field">
            <label>Initial members</label>
            <div className="cl-hint" style={{ marginBottom: 6 }}>
              Pick from existing users; new people enter the edition by invite first.
            </div>
            {users.filter((u) => !u.removed).map((u) => (
              <div className="cl-checkline" key={u.id} style={{ justifyContent: "space-between" }}>
                <span>
                  {u.username}
                  {u.id === selfId && <> <span className="cl-chip">you</span></>}
                </span>
                {u.id === selfId ? (
                  <span className="cl-small cl-muted">Added as Owner of the new workspace</span>
                ) : (
                  <select
                    value={initial[u.id] ?? ""}
                    onChange={(e) => setInitial((prev) => ({ ...prev, [u.id]: e.target.value as WorkspaceRole | "" }))}
                    aria-label={`Initial role for ${u.username}`}
                  >
                    <option value="">Not added — can be granted later from Admin · Users</option>
                    <option value="viewer">Added as Viewer</option>
                    <option value="member">Added as Member</option>
                    <option value="admin">Added as Admin</option>
                    <option value="owner">Added as Owner</option>
                  </select>
                )}
              </div>
            ))}
          </div>
          <button className="cl-btn primary" style={{ width: "auto" }} disabled={!name.trim()} onClick={() => void create()}>
            Create workspace
          </button>
          <p className="cl-small cl-muted" style={{ marginBottom: 0 }}>
            Creation, its initial members and their roles are written to the audit log.
          </p>
        </div>
      )}

      <div className="cl-card" style={{ padding: "6px 8px" }}>
        <div className="cl-table-wrap">
          <table className="cl-table">
            <thead>
              <tr><th>Workspace</th><th>Members</th><th>Your role</th><th>Status</th><th>Created</th><th /></tr>
            </thead>
            <tbody>
              {workspaces.map((w) => (
                <Fragment key={w.id}>
                  <tr>
                    <td>
                      <strong>{w.name}</strong>
                      {w.slug === PRIMARY_SLUG && <> <span className="cl-chip">Primary</span></>}
                      <div className="cl-muted cl-small">
                        {w.slug === PRIMARY_SLUG ? "Seeded at first-run setup · " : ""}{w.description ?? ""}
                      </div>
                    </td>
                    <td>{w.member_count}</td>
                    <td>
                      {w.your_role
                        ? <><span className="cl-chip">{w.your_role}</span>{w.your_role_source === "implicit" && <span className="cl-small cl-muted"> implicit</span>}</>
                        : <span className="cl-muted">—</span>}
                    </td>
                    <td>{w.archived_at ? <span className="cl-chip amber">archived</span> : <span className="cl-chip green">active</span>}</td>
                    <td className="cl-small">{fmtDay(w.created_at)}</td>
                    <td>
                      <button className="cl-btn ghost small" onClick={() => openManage(w)}>
                        {manageId === w.id ? "Close" : "Manage"}
                      </button>
                    </td>
                  </tr>
                  {manageId === w.id && (
                    <tr>
                      <td colSpan={6} style={{ background: "#f9fafb" }}>
                        <div className="cl-field">
                          <label htmlFor={`cl-ws-edit-name-${w.id}`}>Name</label>
                          <input id={`cl-ws-edit-name-${w.id}`} value={editName} onChange={(e) => setEditName(e.target.value)} />
                        </div>
                        <div className="cl-field">
                          <label htmlFor={`cl-ws-edit-desc-${w.id}`}>Description</label>
                          <input id={`cl-ws-edit-desc-${w.id}`} value={editDescription} onChange={(e) => setEditDescription(e.target.value)} />
                        </div>
                        <div className="cl-actions" style={{ marginBottom: 10 }}>
                          <button
                            className="cl-btn ghost small"
                            disabled={!editName.trim() || (editName === w.name && editDescription === (w.description ?? ""))}
                            onClick={() => void act(() => updateWorkspace(w.id, { name: editName.trim(), description: editDescription.trim() || null }), reloadWorkspaces)}
                          >
                            Save name & description
                          </button>
                          {w.archived_at ? (
                            <button className="cl-btn ghost small" onClick={() => void act(() => restoreWorkspace(w.id), reloadWorkspaces)}>
                              Restore workspace
                            </button>
                          ) : (
                            w.slug !== PRIMARY_SLUG && (
                              <button className="cl-btn danger small" onClick={() => setArchiveTarget(w)}>
                                Archive workspace…
                              </button>
                            )
                          )}
                        </div>
                        <div className="cl-small">
                          <strong>Members</strong>
                          {w.members.length === 0 && <span className="cl-muted"> — no stored members yet.</span>}
                          {w.members.map((m) => (
                            <div key={m.user_id} style={{ padding: "3px 0" }}>
                              {m.username} <span className="cl-chip grey">{m.role}</span>
                            </div>
                          ))}
                          <div className="cl-muted" style={{ marginTop: 4 }}>
                            Change a member's role from Admin · Users · Manage — one grid shows
                            that person's role in every workspace.
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <p className="cl-small cl-muted" style={{ lineHeight: 1.55 }}>
        <em>Your role</em> is your own role in each workspace — an admin of the edition is not
        automatically an admin of every workspace. Where it reads <em>implicit</em>, the role
        comes from your global type rather than a stored grant; both are what the workspace
        enforces. The Primary workspace cannot be archived while it is the edition's primary
        workspace — its Archive action is absent, not merely disabled.
      </p>

      {archiveTarget && (
        <div className="cl-modal-veil" role="dialog" aria-modal="true">
          <div className="cl-modal">
            <h2>Archive “{archiveTarget.name}”?</h2>
            <p className="cl-lede">
              Its {archiveTarget.member_count} member{archiveTarget.member_count === 1 ? "" : "s"} lose
              access at their next request and it leaves their workspace switchers. Its claims,
              evidence and audit history are <strong>kept, read-only in the record</strong> —
              archiving is not deletion. An admin can restore it from this screen.
            </p>
            <div className="cl-modal-actions">
              <button className="cl-btn ghost" onClick={() => setArchiveTarget(null)}>Cancel</button>
              <button
                className="cl-btn primary"
                onClick={() => {
                  const target = archiveTarget;
                  setArchiveTarget(null);
                  void act(() => archiveWorkspace(target.id), reloadWorkspaces);
                }}
              >
                Archive workspace
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// ── Invites (wireframe 05) ──────────────────────────────────────────────────

function InvitesTab({
  invites, workspaces, users, formSeed, act, reloadInvites,
}: {
  invites: AdminInvite[] | null;
  workspaces: AdminWorkspace[];
  users: AdminUser[];
  formSeed: number;
  act: (fn: () => Promise<unknown>, after?: () => Promise<void>) => Promise<void>;
  reloadInvites: () => Promise<void>;
}) {
  const [formOpen, setFormOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [days, setDays] = useState(7);
  const [grants, setGrants] = useState<Record<string, WorkspaceRole>>({});
  const [created, setCreated] = useState<{ url: string } | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => { if (formSeed > 0) setFormOpen(true); }, [formSeed]);
  useEffect(() => {
    // Default grant: Member of the primary workspace, as the wireframe shows.
    const primary = workspaces.find((w) => w.slug === PRIMARY_SLUG && !w.archived_at)
      ?? workspaces.find((w) => !w.archived_at);
    if (primary) setGrants((prev) => (Object.keys(prev).length ? prev : { [primary.id]: "member" }));
  }, [workspaces]);

  if (!invites) return <div className="cl-loading">Loading invites…</div>;

  const usernameOf = (id: string | null) => (id ? users.find((u) => u.id === id)?.username ?? id : "—");
  const wsName = (id: string) => workspaces.find((w) => w.id === id)?.name ?? id;

  const create = async () => {
    await act(async () => {
      const res = await createInvite({
        ...(email.trim() ? { email: email.trim() } : {}),
        workspace_grants: grants,
        expires_in_days: days,
      });
      setCreated({ url: `${window.location.origin}${res.invite_url}` });
      setCopied(false);
      setEmail("");
    }, reloadInvites);
  };

  const stateChip = (i: AdminInvite) => {
    switch (inviteState(i)) {
      case "outstanding": return <span className="cl-chip">outstanding</span>;
      case "redeemed": return <span className="cl-chip green">used by {usernameOf(i.redeemed_by)}</span>;
      case "revoked": return <span className="cl-chip grey">revoked</span>;
      case "expired": return <span className="cl-chip amber">expired</span>;
    }
  };

  return (
    <>
      <div className="cl-toolbar">
        <span className="cl-spacer" />
        <button className="cl-btn primary" style={{ width: "auto" }} onClick={() => setFormOpen((v) => !v)}>
          + New invite
        </button>
      </div>

      {created && (
        <div className="cl-card" style={{ borderColor: "#bbf7d0", background: "#f0fdf4" }}>
          <h2>Invite created — copy it now</h2>
          <p className="cl-card-sub" style={{ marginBottom: 0 }}>
            This panel is the only place the full link ever appears.
          </p>
          <div className="cl-codebox">
            <code>{created.url}</code>
            <button
              onClick={() => {
                void navigator.clipboard?.writeText(created.url).then(() => setCopied(true)).catch(() => setCopied(false));
              }}
            >
              {copied ? "Copied" : "Copy link"}
            </button>
          </div>
          <p className="cl-small" style={{ marginBottom: 0, lineHeight: 1.55 }}>
            The code is stored only as a hash, so this link cannot be shown again — if it is
            lost, revoke the invite below and issue a new one. That is deliberate: a list of
            live, reusable entry links sitting in a database would be a standing way in.
          </p>
        </div>
      )}

      {formOpen && (
        <div className="cl-card">
          <h2>New invite</h2>
          <div className="cl-field">
            <label htmlFor="cl-inv-email">Email</label>
            <input id="cl-inv-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Optional" />
            <div className="cl-hint">Optional; when given, the acceptance screen requires it — the link is what counts.</div>
          </div>
          <div className="cl-field">
            <label>Expires</label>
            <div className="cl-radio-row">
              {[2, 7, 30].map((d) => (
                <button key={d} className={`cl-rolepick${days === d ? " sel" : ""}`} onClick={() => setDays(d)}>
                  {d} days{d === 7 ? " (default)" : ""}
                </button>
              ))}
            </div>
          </div>
          <div className="cl-field">
            <label>Joins these workspaces</label>
            {workspaces.filter((w) => !w.archived_at).map((w) => (
              <div className="cl-checkline" key={w.id} style={{ justifyContent: "space-between" }}>
                <span>{w.name}{w.slug === PRIMARY_SLUG && <> <span className="cl-chip">Primary</span></>}</span>
                <select
                  value={grants[w.id] ?? ""}
                  aria-label={`Invite role for ${w.name}`}
                  onChange={(e) => setGrants((prev) => {
                    const next = { ...prev };
                    if (!e.target.value) delete next[w.id];
                    else next[w.id] = e.target.value as WorkspaceRole;
                    return next;
                  })}
                >
                  <option value="">Not joined</option>
                  <option value="viewer">as Viewer</option>
                  <option value="member">as Member</option>
                  <option value="admin">as Admin</option>
                  <option value="owner">as Owner</option>
                </select>
              </div>
            ))}
          </div>
          <button className="cl-btn primary" style={{ width: "auto" }} onClick={() => void create()}>
            Create invite link
          </button>
          <p className="cl-small cl-muted" style={{ marginBottom: 0 }}>
            Creating shows the full link once, in the panel above, with a copy button.
          </p>
        </div>
      )}

      <div className="cl-card" style={{ padding: "6px 8px" }}>
        <div className="cl-table-wrap">
          <table className="cl-table">
            <thead>
              <tr><th>Invite</th><th>For</th><th>Workspaces</th><th>State</th><th>Expires</th><th /></tr>
            </thead>
            <tbody>
              {invites.map((i) => (
                <tr key={i.id}>
                  <td className="cl-small">Created by {usernameOf(i.created_by)} · {fmtDay(i.created_at)}</td>
                  <td className="cl-small">{i.email ?? "—"}</td>
                  <td className="cl-small">
                    {Object.entries(i.workspace_grants).map(([id, role]) => (
                      <span key={id} style={{ marginRight: 6 }}>{wsName(id)} <span className="cl-chip grey">{role}</span></span>
                    ))}
                    {Object.keys(i.workspace_grants).length === 0 && "—"}
                  </td>
                  <td>{stateChip(i)}</td>
                  <td className="cl-small">{inviteState(i) === "outstanding" ? fmtDay(i.expires_at) : "—"}</td>
                  <td>
                    {inviteState(i) === "outstanding" && (
                      <button className="cl-btn ghost small" onClick={() => void act(() => revokeInvite(i.id), reloadInvites)}>
                        Revoke
                      </button>
                    )}
                  </td>
                </tr>
              ))}
              {invites.length === 0 && (
                <tr><td colSpan={6} className="cl-empty">No invites yet — create the first one above.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
      <p className="cl-small cl-muted" style={{ lineHeight: 1.55 }}>
        Used, expired, and revoked invites stay on this list — the record of who was invited,
        and what became of it, is part of the project's history and lands in the audit log.
      </p>
    </>
  );
}

// ── Audit log (wireframe 06) ────────────────────────────────────────────────

const CLASS_OPTIONS: { id: AuditClass | "all"; label: string }[] = [
  { id: "all", label: "All events" },
  { id: "logins", label: "Logins" },
  { id: "invites", label: "Invites" },
  { id: "user-changes", label: "User changes" },
  { id: "publishes", label: "Publishes" },
];

function AuditTab({
  entries, users, ctx, hasMore, onLoadMore,
}: {
  entries: AuditEntry[];
  users: AdminUser[];
  ctx: AuditContext;
  hasMore: boolean;
  onLoadMore: () => void;
}) {
  const [cls, setCls] = useState<AuditClass | "all">("all");
  const [actor, setActor] = useState<string>("all");
  const visible = entries.filter(
    (e) => (cls === "all" || auditClassOf(e.event) === cls) && (actor === "all" || e.actor_id === actor || e.actor_label === actor),
  );
  const rangeLabel = (() => {
    if (!entries.length) return "No entries yet";
    const first = new Date(entries[0].ts);
    const last = new Date(entries[entries.length - 1].ts);
    const sameDay = first.toDateString() === last.toDateString();
    return sameDay ? `Showing ${fmtDay(entries[0].ts)}` : `Showing ${fmtDay(entries[entries.length - 1].ts)} – ${fmtDay(entries[0].ts)}`;
  })();
  return (
    <>
      <div className="cl-toolbar">
        <label className="cl-small" htmlFor="cl-audit-class"><strong>Event</strong></label>
        <select id="cl-audit-class" value={cls} onChange={(e) => setCls(e.target.value as AuditClass | "all")}>
          {CLASS_OPTIONS.map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}
        </select>
        <label className="cl-small" htmlFor="cl-audit-actor"><strong>Actor</strong></label>
        <select id="cl-audit-actor" value={actor} onChange={(e) => setActor(e.target.value)}>
          <option value="all">Everyone</option>
          {users.map((u) => <option key={u.id} value={u.id}>{u.username}</option>)}
          <option value="system">system</option>
        </select>
        <span className="cl-spacer" />
        <span className="cl-small cl-muted">{rangeLabel} · newest first · times in your zone</span>
      </div>
      <div className="cl-card" style={{ padding: "6px 8px" }}>
        <div className="cl-table-wrap">
          <table className="cl-table">
            <thead>
              <tr><th>Time</th><th>Actor</th><th>Event</th><th>Detail</th></tr>
            </thead>
            <tbody>
              {visible.map((e) => (
                <tr key={e.id}>
                  <td className="cl-small" style={{ whiteSpace: "nowrap" }}>{fmtWhenShort(e.ts)}</td>
                  <td className="cl-small">{e.actor_label || "—"}</td>
                  <td className="cl-small"><strong>{auditLabel(e.event)}</strong></td>
                  <td className="cl-small">{describeAudit(e, ctx)}</td>
                </tr>
              ))}
              {visible.length === 0 && (
                <tr><td colSpan={4} className="cl-empty">No entries match these filters.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
      {hasMore && (
        <button className="cl-btn ghost" onClick={onLoadMore}>Load older entries</button>
      )}
      <p className="cl-small cl-muted" style={{ lineHeight: 1.55 }}>
        A failed dataset publish (marker scan) is also an entry here — with the scan's findings
        named — so a blocked publish is a recorded event, not a silent one.
      </p>
    </>
  );
}
