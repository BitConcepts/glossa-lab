/**
 * Spec 083 (Step 3, T026/T027) — the cloud pieces of the app shell:
 * the workspace switcher card (wireframe 11), the signed-in user
 * chip (wireframe 07), and the dataset identity chip (wireframe 07
 * program header). All three render ONLY from the edge session +
 * the container's own status read — a workspace the user is not in
 * appears nowhere, including here.
 */

import { useEffect, useRef, useState } from "react";
import { getStatus, type Project, type StatusResponse } from "../api";
import { listAdminInvites } from "./api";
import { fmtWhenShort } from "./fmt";
import { useCloudSession } from "./session";

export const PRIMARY_WORKSPACE_SLUG = "indus-script";

/** The dataset identity from /status (bundle · source · hydrated). */
export function useDatasetIdentity(): StatusResponse["dataset"] {
  const [dataset, setDataset] = useState<StatusResponse["dataset"]>(undefined);
  useEffect(() => {
    let live = true;
    const load = () => {
      getStatus()
        .then((s) => { if (live) setDataset(s.dataset ?? null); })
        .catch(() => { if (live) setDataset(null); });
    };
    load();
    const t = window.setInterval(load, 60_000);
    return () => { live = false; window.clearInterval(t); };
  }, []);
  return dataset;
}

export function datasetText(dataset: NonNullable<StatusResponse["dataset"]>): string {
  const commit = dataset.source_commit ? dataset.source_commit.slice(0, 8) : "";
  const when = dataset.hydrated_at || dataset.built_at;
  return `Dataset ${dataset.bundle_id}${commit ? ` · source ${commit}` : ""}${when ? ` · hydrated ${fmtWhenShort(when)}` : ""}`;
}

/** The dataset chip for program-surface headers (wireframe 07). */
export function DatasetChip() {
  const dataset = useDatasetIdentity();
  if (!dataset) return null;
  return (
    <span
      title="The dataset bundle this surface is reading"
      style={{
        display: "inline-flex", alignItems: "center", gap: 5,
        fontSize: 11, fontWeight: 600, color: "#1d4ed8",
        background: "#eff6ff", border: "1px solid #bfdbfe",
        padding: "3px 9px", borderRadius: 999, whiteSpace: "nowrap",
      }}
    >
      ▦ {datasetText(dataset)}
    </span>
  );
}

/** A right-aligned header row carrying the chip — renders nothing
 *  at all (no layout cost) when no bundle identity exists. */
export function DatasetChipRow() {
  const dataset = useDatasetIdentity();
  if (!dataset) return null;
  return (
    <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: 10 }}>
      <span
        title="The dataset bundle this surface is reading"
        style={{
          display: "inline-flex", alignItems: "center", gap: 5,
          fontSize: 11, fontWeight: 600, color: "#1d4ed8",
          background: "#eff6ff", border: "1px solid #bfdbfe",
          padding: "3px 9px", borderRadius: 999, whiteSpace: "nowrap",
        }}
      >
        ▦ {datasetText(dataset)}
      </span>
    </div>
  );
}

/** Outstanding-invite count for the Admin nav badge (admins only). */
export function useAdminInviteCount(enabled: boolean): number {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!enabled) return;
    let live = true;
    const load = () => {
      listAdminInvites()
        .then(({ invites }) => {
          if (!live) return;
          setCount(invites.filter((i) => !i.revoked_at && !i.redeemed_at && i.expires_at > new Date().toISOString()).length);
        })
        .catch(() => { /* the badge is advisory; the tab itself reports errors */ });
    };
    load();
    const t = window.setInterval(load, 60_000);
    return () => { live = false; window.clearInterval(t); };
  }, [enabled]);
  return count;
}

// ── Workspace switcher (wireframe 11) ───────────────────────────────────────

export function CloudWorkspaceCard({
  projects,
  activeProject,
  onSelectProject,
  onOpenPrograms,
  onOpenAdminWorkspaces,
}: {
  projects: Project[];
  activeProject: Project | null;
  onSelectProject: (id: string) => void;
  onOpenPrograms: () => void;
  onOpenAdminWorkspaces: () => void;
}) {
  const cloud = useCloudSession();
  const dataset = useDatasetIdentity();
  const [open, setOpen] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const h = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, [open ]);

  const projectFor = (slug: string): Project | undefined =>
    projects.find((p) => p.slug === slug);
  const activeWs = cloud.workspaces.find((w) => w.slug === activeProject?.slug);
  const heading = activeWs?.name ?? activeProject?.label ?? "None open";
  const sub = activeWs?.description
    ?? (activeProject?.question ?? "").trim()
    ?? activeProject?.description
    ?? "";

  return (
    <div ref={ref} style={{ position: "relative", padding: "0 12px", flexShrink: 0 }}>
      <button
        onClick={() => setOpen((v) => !v)}
        aria-label="Switch workspace"
        style={{
          margin: "12px 0 4px", padding: "9px 11px", borderRadius: 8, width: "100%",
          border: activeWs || activeProject ? "1px solid rgba(96,165,250,.45)" : "1px dashed rgba(255,255,255,.25)",
          background: activeWs || activeProject ? "rgba(37,99,235,.14)" : "rgba(255,255,255,.04)",
          color: "#dbeafe", display: "block", textAlign: "left", cursor: "pointer",
        }}
      >
        <div style={{ fontSize: 9, letterSpacing: 1, textTransform: "uppercase", color: "#93c5fd", fontWeight: 700 }}>
          Workspace
        </div>
        <div style={{ fontSize: 13, fontWeight: 700, color: activeWs || activeProject ? "#fff" : "#a8c2e2", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 6 }}>
          <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{heading}</span>
          <span>▾</span>
        </div>
        {sub && (
          <div style={{ fontSize: 11, color: "#a8c2e2", marginTop: 2, lineHeight: 1.35 }}>{sub}</div>
        )}
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginTop: 6 }}>
          {activeWs && (
            <span className="cl-chip on-dark">{activeWs.role}{activeWs.role_source === "implicit" ? " · implicit" : ""}</span>
          )}
          {dataset && (
            <span className="cl-chip on-dark" title={datasetText(dataset)}>
              Dataset {dataset.bundle_id}
            </span>
          )}
        </div>
      </button>

      {open && (
        <div style={{
          position: "absolute", top: "100%", left: 12, right: 12, zIndex: 300,
          background: "#1e293b", border: "1px solid rgba(255,255,255,0.12)",
          borderRadius: 8, boxShadow: "0 8px 24px rgba(0,0,0,0.4)",
          maxHeight: 340, overflowY: "auto", marginTop: 2, padding: "6px 0",
        }}>
          <div style={{ padding: "6px 12px 8px", fontSize: 10.5, color: "#93c5fd", lineHeight: 1.45 }}>
            Workspaces — you see only the ones you belong to.
          </div>
          {cloud.workspaces.map((w) => {
            const proj = projectFor(w.slug);
            const isCurrent = !!activeProject && proj?.id === activeProject.id;
            return (
              <button
                key={w.id}
                onClick={() => {
                  if (proj) {
                    onSelectProject(proj.id);
                    setOpen(false);
                    setNotice(null);
                  } else {
                    setNotice(`“${w.name}” has no program attached yet — an admin sets that up on the desktop side.`);
                  }
                }}
                style={{
                  width: "100%", padding: "8px 12px", border: "none",
                  background: isCurrent ? "rgba(37,99,235,0.15)" : "none",
                  color: "#e2e8f0", cursor: "pointer", textAlign: "left",
                  borderBottom: "1px solid rgba(255,255,255,0.04)", display: "block",
                }}
              >
                <span style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 6 }}>
                  <span style={{ fontSize: 12, fontWeight: isCurrent ? 700 : 600 }}>
                    {w.name}
                    {w.slug === PRIMARY_WORKSPACE_SLUG && (
                      <span className="cl-chip on-dark" style={{ marginLeft: 6 }}>Primary</span>
                    )}
                  </span>
                  {isCurrent
                    ? <><span className="cl-chip on-dark">{w.role}</span> <span className="cl-chip on-dark">current</span></>
                    : <span className="cl-chip on-dark">{w.role}</span>}
                </span>
                {w.description && (
                  <span style={{ display: "block", fontSize: 11, color: "#a8c2e2", marginTop: 2, lineHeight: 1.4 }}>
                    {w.description}
                  </span>
                )}
              </button>
            );
          })}
          {cloud.workspaces.length === 0 && (
            <div style={{ padding: "8px 12px", fontSize: 11.5, color: "#a8c2e2", lineHeight: 1.5 }}>
              You are not a member of any workspace yet. An admin grants workspace access —
              until then there is nothing for this account to open.
            </div>
          )}
          {notice && (
            <div style={{ padding: "8px 12px", fontSize: 11, color: "#fbbf24", lineHeight: 1.45 }}>{notice}</div>
          )}
          <button
            onClick={() => { onOpenPrograms(); setOpen(false); }}
            style={{
              width: "100%", padding: "8px 12px", border: "none", background: "none",
              color: "rgba(255,255,255,0.75)", cursor: "pointer", textAlign: "left", fontSize: 11,
              borderTop: "1px solid rgba(255,255,255,0.08)",
            }}
          >
            ▦ All programs (tool home)
          </button>
          {cloud.isAdmin && (
            <button
              onClick={() => { onOpenAdminWorkspaces(); setOpen(false); }}
              style={{
                width: "100%", padding: "8px 12px", border: "none", background: "none",
                color: "rgba(255,255,255,0.75)", cursor: "pointer", textAlign: "left", fontSize: 11,
              }}
            >
              All workspaces → manage in Admin · Workspaces
            </button>
          )}
          <div style={{ padding: "8px 12px 4px", fontSize: 10.5, color: "rgba(255,255,255,0.45)", lineHeight: 1.5 }}>
            A workspace you are not in does not appear here, in lists, or in search results —
            as if it did not exist. That is deliberate, and it is what the access check enforces
            on every request.
          </div>
        </div>
      )}
    </div>
  );
}

// ── User chip (wireframe 07, sidebar bottom) ────────────────────────────────

export function UserChip({
  onOpenAccount,
  onOpenAdmin,
}: {
  onOpenAccount: () => void;
  onOpenAdmin: () => void;
}) {
  const cloud = useCloudSession();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const h = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, [open ]);

  if (!cloud.user) return null;
  const user = cloud.user;

  return (
    <div ref={ref} style={{ position: "relative", padding: "10px 12px", borderTop: "1px solid rgba(255,255,255,0.08)", flexShrink: 0 }}>
      <button
        onClick={() => setOpen((v) => !v)}
        aria-label="Your account"
        style={{
          width: "100%", display: "flex", alignItems: "center", gap: 9,
          background: "none", border: "none", cursor: "pointer", textAlign: "left", padding: 0,
        }}
      >
        <span style={{
          width: 28, height: 28, borderRadius: "50%", flexShrink: 0,
          background: "linear-gradient(135deg,#2563eb,#60a5fa)", color: "#fff",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 12, fontWeight: 800,
        }}>
          {user.username.slice(0, 1).toUpperCase()}
        </span>
        <span style={{ flex: 1, minWidth: 0 }}>
          <span style={{ display: "block", fontSize: 12.5, fontWeight: 700, color: "#fff", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {user.username}
          </span>
          <span style={{ display: "block", fontSize: 10.5, color: "#7a9bbf" }}>
            · {user.global_type}
          </span>
        </span>
        <span style={{ color: "#7a9bbf", fontSize: 11 }}>▾</span>
      </button>

      {open && (
        <div style={{
          position: "absolute", bottom: "100%", left: 12, right: 12, zIndex: 300,
          background: "#1e293b", border: "1px solid rgba(255,255,255,0.12)",
          borderRadius: 8, boxShadow: "0 8px 24px rgba(0,0,0,0.4)",
          marginBottom: 4, padding: "4px 0",
        }}>
          {[
            { label: "Account & security", action: () => { onOpenAccount(); setOpen(false); } },
            ...(cloud.isAdmin
              ? [{ label: "Admin", action: () => { onOpenAdmin(); setOpen(false); } }]
              : []),
            { label: "Sign out", action: () => { void cloud.signOut(); } },
          ].map((item) => (
            <button
              key={item.label}
              onClick={item.action}
              style={{
                width: "100%", padding: "8px 12px", border: "none", background: "none",
                color: "#e2e8f0", cursor: "pointer", textAlign: "left", fontSize: 12,
                display: "block",
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
