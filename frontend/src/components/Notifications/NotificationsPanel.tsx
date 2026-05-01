/**
 * NotificationsPanel — embedded in SettingsView.
 *
 * Shows the SMTP configuration status, lets the user manage the recipient
 * list (add/remove/toggle-active/edit-label), fires a deliverability test,
 * and surfaces the most recent send log entries with success / fail badges.
 *
 * SMTP credentials live in the same `.keys.json` store as every other API
 * key (smtp_host / smtp_port / smtp_username / smtp_password / smtp_from /
 * smtp_use_tls). They're rendered by the existing keys block in SettingsView,
 * so this panel intentionally does NOT duplicate the credential editor —
 * it just shows whether the notifier is currently configured.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  createNotificationRecipient,
  deleteNotificationRecipient,
  disconnectGraph,
  getDiscoverySchedulerStatus,
  getNotifierStatus,
  listNotificationLog,
  listNotificationRecipients,
  pollGraphDeviceFlow,
  sendTestNotification,
  startDiscoveryScheduler,
  startGraphDeviceFlow,
  stopDiscoveryScheduler,
  updateNotificationRecipient,
  type DiscoverySchedulerStatus,
  type GraphDeviceFlowStart,
  type NotificationLogEntry,
  type NotificationRecipient,
  type NotifierStatus,
} from "../../api";
import { useToast } from "../../hooks/useToast";

export function NotificationsPanel() {
  const { toast } = useToast();
  const [status, setStatus]   = useState<NotifierStatus | null>(null);
  const [rows, setRows]       = useState<NotificationRecipient[]>([]);
  const [log, setLog]         = useState<NotificationLogEntry[]>([]);
  const [sched, setSched]     = useState<DiscoverySchedulerStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy]       = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [newLabel, setNewLabel] = useState("");

  // Outlook 365 device-code flow state
  const [graphFlow, setGraphFlow] = useState<GraphDeviceFlowStart | null>(null);
  const [graphPolling, setGraphPolling] = useState(false);
  const [graphError, setGraphError] = useState<string>("");
  const graphPollAbort = useRef(false);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const [s, r, l, sc] = await Promise.all([
        getNotifierStatus(),
        listNotificationRecipients(),
        listNotificationLog(20),
        getDiscoverySchedulerStatus().catch(() => null),
      ]);
      setStatus(s);
      setRows(r.recipients);
      setLog(l.entries);
      setSched(sc);
    } catch (e) {
      toast(e instanceof Error ? e.message : "Failed to load notifications", "error");
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => { void refresh(); }, [refresh]);

  const onAdd = async () => {
    const email = newEmail.trim();
    if (!email) return;
    setBusy(true);
    try {
      await createNotificationRecipient({ email, label: newLabel.trim(), active: true });
      setNewEmail(""); setNewLabel("");
      toast("Recipient added", "success");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Could not add recipient", "error");
    } finally { setBusy(false); }
  };

  const onToggle = async (r: NotificationRecipient) => {
    try {
      await updateNotificationRecipient(r.id, { active: !r.active });
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Update failed", "error");
    }
  };

  const onRename = async (r: NotificationRecipient) => {
    const next = window.prompt("Label:", r.label);
    if (next === null) return;
    try {
      await updateNotificationRecipient(r.id, { label: next });
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Update failed", "error");
    }
  };

  const onDelete = async (r: NotificationRecipient) => {
    if (!window.confirm(`Remove ${r.email} from notifications?`)) return;
    try {
      await deleteNotificationRecipient(r.id);
      toast("Recipient removed", "info");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Delete failed", "error");
    }
  };

  const onTest = async () => {
    setBusy(true);
    try {
      const r = await sendTestNotification();
      toast(`Test sent: ${r.sent} ok / ${r.failed} failed`, r.failed ? "warning" : "success");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Test failed", "error");
    } finally { setBusy(false); }
  };

  // ── Microsoft Graph: device-code flow ────────────────────────────────

  const onConnectOutlook = async () => {
    setGraphError("");
    setBusy(true);
    try {
      const flow = await startGraphDeviceFlow();
      setGraphFlow(flow);
      graphPollAbort.current = false;
      void pollGraphLoop(flow);
    } catch (e) {
      setGraphError(e instanceof Error ? e.message : "Could not start device flow");
      toast("Outlook connect failed \u2014 check ms_graph_client_id", "error");
    } finally {
      setBusy(false);
    }
  };

  const pollGraphLoop = async (flow: GraphDeviceFlowStart) => {
    setGraphPolling(true);
    const intervalMs = Math.max(2000, flow.interval * 1000);
    while (!graphPollAbort.current) {
      await new Promise((r) => setTimeout(r, intervalMs));
      if (graphPollAbort.current) break;
      try {
        const res = await pollGraphDeviceFlow(flow.session_id);
        if (res.status === "success") {
          toast("Outlook 365 connected", "success");
          setGraphFlow(null);
          setGraphPolling(false);
          await refresh();
          return;
        }
        if (res.status === "failed" || res.status === "expired") {
          setGraphError(res.error || res.status);
          setGraphPolling(false);
          return;
        }
      } catch (e) {
        setGraphError(e instanceof Error ? e.message : "poll failed");
        setGraphPolling(false);
        return;
      }
    }
    setGraphPolling(false);
  };

  const onCancelOutlookFlow = () => {
    graphPollAbort.current = true;
    setGraphFlow(null);
    setGraphPolling(false);
  };

  const onDisconnectOutlook = async () => {
    if (!window.confirm("Disconnect Outlook 365? You can reconnect anytime.")) return;
    setBusy(true);
    try {
      await disconnectGraph();
      toast("Outlook 365 disconnected", "info");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Disconnect failed", "error");
    } finally { setBusy(false); }
  };

  // ── Discovery scheduler auto-start ─────────────────────────────────────

  const onToggleAutoStart = async (enable: boolean) => {
    setBusy(true);
    try {
      const next = enable
        ? await startDiscoveryScheduler()
        : await stopDiscoveryScheduler();
      setSched(next);
      toast(
        enable
          ? `Auto-start ON — fetch + mine + digest will run every ${Math.round(next.interval_seconds / 3600)}h`
          : "Auto-start OFF",
        "info",
      );
    } catch (e) {
      toast(e instanceof Error ? e.message : "Toggle failed", "error");
    } finally { setBusy(false); }
  };

  const configured = status?.configured ?? false;
  const activeCount = status?.recipients_active ?? 0;
  const totalCount  = status?.recipients_total ?? 0;

  return (
    <section style={sectionStyle}>
      <h3 style={sectionTitleStyle}>📬 Email Notifications</h3>
      <p style={hintTextStyle}>
        Manage who receives the discovery digest and study/experiment completion emails.
        Configure SMTP credentials in the API Keys section above
        (<code>smtp_host</code>, <code>smtp_from</code>, optional <code>smtp_username</code>/
        <code>smtp_password</code>, <code>smtp_port</code>=587, <code>smtp_use_tls</code>=1).
      </p>

      {/* Status banner */}
      <div style={{
        marginTop: 10, padding: "10px 14px", borderRadius: 7,
        border: `1px solid ${configured ? "#86efac" : "#fcd34d"}`,
        background: configured ? "#f0fdf4" : "#fffbeb",
        display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap",
      }}>
        <span style={{ fontSize: 16 }}>{configured ? "✅" : "⚠️"}</span>
        <div style={{ flex: 1, minWidth: 220 }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: configured ? "#15803d" : "#92400e" }}>
            {configured
              ? (status?.transport === "graph"
                  ? "Outlook 365 (Microsoft Graph) configured"
                  : "SMTP configured")
              : "Email not configured"}
          </div>
          <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>
            {!configured
              ? "Connect Outlook 365 below \u2014 or set smtp_host + smtp_from in API Keys."
              : status?.transport === "graph"
                ? `Tenant ${status?.graph_tenant} · ${activeCount}/${totalCount} active recipients`
                : `Host ${status?.host}:${status?.port} · From ${status?.from || "(unset)"} · ${activeCount}/${totalCount} active`}
          </div>
        </div>
        <button onClick={() => void onTest()} disabled={busy || !configured || activeCount === 0}
          title={activeCount === 0 ? "Add an active recipient first" : "Send a deliverability test email"}
          style={{
            padding: "5px 12px", border: "1px solid #2563eb", borderRadius: 6,
            background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600,
            cursor: (busy || !configured || activeCount === 0) ? "not-allowed" : "pointer",
            opacity: (busy || !configured || activeCount === 0) ? 0.5 : 1,
          }}>
          {busy ? "Sending…" : "✉ Send Test"}
        </button>
        <button onClick={() => void refresh()} title="Reload"
          style={{ padding: "5px 9px", border: "1px solid #d1d5db", borderRadius: 5,
            background: "#fff", cursor: "pointer", fontSize: 12 }}>
          ⟳
        </button>
      </div>

      {/* Outlook 365 connect block */}
      <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 7,
        border: "1px solid #c7d2fe", background: "#eef2ff" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
          <span style={{ fontSize: 16 }}>📧</span>
          <div style={{ flex: 1, minWidth: 240 }}>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#3730a3" }}>
              Outlook 365 (Microsoft Graph)
            </div>
            <div style={{ fontSize: 11, color: "#4338ca", marginTop: 2 }}>
              {status?.graph_configured
                ? `Connected. Tenant: ${status?.graph_tenant}. Mail.Send delegated.`
                : status?.graph_client_id_set
                  ? "Client ID set, but not yet authorised. Click Connect to start."
                  : "Set ms_graph_client_id in API Keys (after registering a public-client app at entra.microsoft.com), then click Connect."}
            </div>
          </div>
          {status?.graph_configured ? (
            <button onClick={() => void onDisconnectOutlook()} disabled={busy}
              style={{ padding: "5px 12px", border: "1px solid #c7d2fe",
                borderRadius: 6, background: "#fff", color: "#4338ca",
                fontSize: 12, fontWeight: 600, cursor: busy ? "not-allowed" : "pointer" }}>
              Disconnect
            </button>
          ) : (
            <button onClick={() => void onConnectOutlook()}
              disabled={busy || !status?.graph_client_id_set || graphPolling}
              title={!status?.graph_client_id_set
                ? "Set ms_graph_client_id in API Keys first"
                : "Start the device-code OAuth flow"}
              style={{ padding: "5px 14px", border: "none", borderRadius: 6,
                background: "#4338ca", color: "#fff", fontSize: 12, fontWeight: 700,
                cursor: busy || !status?.graph_client_id_set ? "not-allowed" : "pointer",
                opacity: busy || !status?.graph_client_id_set ? 0.5 : 1 }}>
              🔗 Connect Outlook 365
            </button>
          )}
        </div>
        {graphFlow && (
          <div style={{ marginTop: 10, padding: "10px 12px", borderRadius: 6,
            background: "#fff", border: "1px solid #c7d2fe" }}>
            <div style={{ fontSize: 12, color: "#374151" }}>
              1. Open <a href={graphFlow.verification_uri} target="_blank"
                rel="noopener noreferrer" style={{ color: "#4338ca" }}>
                {graphFlow.verification_uri}
              </a>
            </div>
            <div style={{ fontSize: 12, color: "#374151", marginTop: 4 }}>
              2. Paste this code:
            </div>
            <div style={{ marginTop: 6, fontSize: 22, fontWeight: 800,
              fontFamily: "monospace", color: "#4338ca", letterSpacing: 2,
              padding: "6px 10px", border: "2px dashed #c7d2fe",
              borderRadius: 6, display: "inline-block" }}>
              {graphFlow.user_code}
            </div>
            <div style={{ fontSize: 11, color: "#6b7280", marginTop: 6 }}>
              {graphPolling ? "Waiting for approval\u2026 (polls automatically)" : "Polling stopped"}
              {" "}· Code expires in {Math.round(graphFlow.expires_in / 60)} min.
              <button onClick={onCancelOutlookFlow}
                style={{ marginLeft: 8, padding: "2px 8px", border: "1px solid #d1d5db",
                  borderRadius: 4, background: "#fff", cursor: "pointer", fontSize: 11,
                  color: "#6b7280" }}>
                Cancel
              </button>
            </div>
          </div>
        )}
        {graphError && (
          <div style={{ marginTop: 8, fontSize: 11, color: "#b91c1c" }}>
            ⚠ {graphError}
          </div>
        )}
      </div>

      {/* Auto-start discovery scheduler toggle */}
      <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 7,
        border: `1px solid ${sched?.running ? "#86efac" : "#e5e7eb"}`,
        background: sched?.running ? "#f0fdf4" : "#fafafa",
        display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
        <span style={{ fontSize: 16 }}>{sched?.running ? "⏱️" : "💤"}</span>
        <div style={{ flex: 1, minWidth: 240 }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: sched?.running ? "#15803d" : "#374151" }}>
            Auto-start discovery {sched?.running ? "— RUNNING" : "— OFF"}
          </div>
          <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>
            {sched
              ? `Fetch + mine + digest every ${Math.round(sched.interval_seconds / 3600)}h. ${
                  sched.enabled ? "Persisted; will resume on next backend boot." : "Not persisted."
                }`
              : "Loading scheduler status\u2026"}
          </div>
        </div>
        <div onClick={() => !busy && void onToggleAutoStart(!sched?.running)}
          title={sched?.running ? "Stop scheduler + persist OFF" : "Start scheduler + persist ON"}
          style={{ width: 44, height: 24, borderRadius: 12, cursor: busy ? "not-allowed" : "pointer",
            flexShrink: 0, position: "relative",
            background: sched?.running ? "#22c55e" : "#d1d5db",
            opacity: busy ? 0.5 : 1, transition: "background 0.2s" }}>
          <div style={{ position: "absolute", top: 3, left: sched?.running ? 23 : 3,
            width: 18, height: 18, borderRadius: "50%", background: "#fff",
            boxShadow: "0 1px 3px rgba(0,0,0,0.25)", transition: "left 0.2s" }} />
        </div>
      </div>

      {/* Recipients */}
      <div style={{ marginTop: 14 }}>
        <div style={{ fontSize: 11, fontWeight: 700, color: "#7c3aed",
          textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>
          Recipients ({rows.length})
        </div>
        {loading ? (
          <div style={{ fontSize: 12, color: "#6b7280" }}>Loading…</div>
        ) : rows.length === 0 ? (
          <div style={{ fontSize: 12, color: "#9ca3af", fontStyle: "italic" }}>
            No recipients yet. Add at least one address below to start receiving emails.
          </div>
        ) : (
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 6, overflow: "hidden" }}>
            {rows.map((r) => (
              <div key={r.id} style={{
                display: "flex", alignItems: "center", gap: 8,
                padding: "7px 12px", borderBottom: "1px solid #f1f5f9",
                background: r.active ? "#fff" : "#fafafa",
              }}>
                <span title={r.active ? "Active" : "Paused"} style={{
                  width: 8, height: 8, borderRadius: "50%",
                  background: r.active ? "#22c55e" : "#cbd5e1", flexShrink: 0,
                }} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 13, fontWeight: 500, color: "#111827",
                    overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {r.email}
                  </div>
                  {r.label && (
                    <div style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}>
                      {r.label}
                    </div>
                  )}
                </div>
                <button onClick={() => void onToggle(r)}
                  title={r.active ? "Pause notifications" : "Resume notifications"}
                  style={miniBtn(r.active ? "#f59e0b" : "#22c55e")}>
                  {r.active ? "⏸" : "▶"}
                </button>
                <button onClick={() => void onRename(r)} title="Edit label" style={miniBtn("#6b7280")}>✎</button>
                <button onClick={() => void onDelete(r)} title="Remove" style={miniBtn("#dc2626")}>🗑</button>
              </div>
            ))}
          </div>
        )}

        {/* Add recipient row */}
        <div style={{ display: "flex", gap: 6, marginTop: 8, flexWrap: "wrap" }}>
          <input value={newEmail}
            onChange={(e) => setNewEmail(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && newEmail.trim()) void onAdd(); }}
            placeholder="recipient@example.com"
            style={{ flex: 2, minWidth: 200, padding: "6px 10px",
              border: "1px solid #d1d5db", borderRadius: 5, fontSize: 13, outline: "none" }} />
          <input value={newLabel}
            onChange={(e) => setNewLabel(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && newEmail.trim()) void onAdd(); }}
            placeholder="Label (optional, e.g. PI, lab)"
            style={{ flex: 1, minWidth: 140, padding: "6px 10px",
              border: "1px solid #d1d5db", borderRadius: 5, fontSize: 13, outline: "none" }} />
          <button onClick={() => void onAdd()} disabled={busy || !newEmail.trim()}
            style={{
              padding: "6px 16px", border: "none", borderRadius: 5,
              background: "#7c3aed", color: "#fff", fontSize: 12, fontWeight: 600,
              cursor: busy || !newEmail.trim() ? "not-allowed" : "pointer",
              opacity: busy || !newEmail.trim() ? 0.5 : 1,
            }}>
            + Add
          </button>
        </div>
      </div>

      {/* Recent log */}
      <details style={{ marginTop: 16 }}>
        <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13, color: "#374151" }}>
          📜 Recent Send Log ({log.length})
        </summary>
        <div style={{ marginTop: 8, maxHeight: 220, overflowY: "auto",
          border: "1px solid #e5e7eb", borderRadius: 6 }}>
          {log.length === 0 ? (
            <div style={{ fontSize: 12, color: "#9ca3af", padding: "10px 14px",
              fontStyle: "italic" }}>No emails sent yet.</div>
          ) : (
            log.map((row) => {
              const sc = row.status === "sent" ? "#22c55e"
                       : row.status === "failed" ? "#dc2626"
                       : "#9ca3af";
              return (
                <div key={row.id} style={{
                  display: "flex", gap: 8, padding: "6px 12px",
                  borderBottom: "1px solid #f1f5f9", alignItems: "center",
                }}>
                  <span style={{ fontSize: 9, fontWeight: 700, color: sc,
                    background: sc + "20", padding: "1px 6px", borderRadius: 4,
                    textTransform: "uppercase", flexShrink: 0 }}>
                    {row.status}
                  </span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 12, color: "#111827", overflow: "hidden",
                      textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {row.subject}
                    </div>
                    <div style={{ fontSize: 10, color: "#6b7280", marginTop: 1 }}>
                      to {row.recipient} · {row.kind} · {fmtTime(row.sent_at)}
                      {row.item_count > 0 && ` · ${row.item_count} items`}
                    </div>
                    {row.error && (
                      <div style={{ fontSize: 10, color: "#dc2626", marginTop: 1 }}>
                        {row.error}
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </details>
    </section>
  );
}

// ── Helpers ────────────────────────────────────────────────────────────────

function miniBtn(color: string): React.CSSProperties {
  return {
    border: "1px solid " + color + "40", borderRadius: 4, background: "none",
    color, cursor: "pointer", fontSize: 11, padding: "2px 7px",
  };
}

function fmtTime(iso: string): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString();
}

const sectionStyle: React.CSSProperties = {
  marginBottom: "2rem", padding: "1.25rem",
  border: "1px solid #e5e7eb", borderRadius: 8,
};
const sectionTitleStyle: React.CSSProperties = {
  margin: "0 0 0.75rem 0", fontSize: 15, fontWeight: 600, color: "#111827",
};
const hintTextStyle: React.CSSProperties = {
  margin: 0, fontSize: 12, color: "#6b7280", lineHeight: 1.5,
};
