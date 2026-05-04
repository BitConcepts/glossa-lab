/**
 * NotificationsPanel — provider-aware email + recipients + send log.
 *
 * Top of panel is a single "Mail provider" selector. Choosing a preset
 * (Outlook 365 OAuth, Gmail SMTP, Yahoo SMTP, iCloud, Zoho, Infomaniak/
 * Swissmail, ProtonMail Bridge, SendGrid/Mailgun, university SMTP, custom)
 * either runs the device-code OAuth flow or unfolds a tailored SMTP form
 * pre-filled with the provider's defaults. SMTP credentials are stored via
 * the existing settings keys; users never have to memorise host/port/TLS.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  EMAIL_PROVIDER_PRESETS, createNotificationRecipient,
  deleteNotificationRecipient, disconnectGraph,
  getDiscoverySchedulerStatus, getNotifierStatus, getSettings,
  listNotificationLog, listNotificationRecipients, pollGraphDeviceFlow,
  sendTestNotification, startDiscoveryScheduler, startGraphDeviceFlow,
  stopDiscoveryScheduler, updateNotificationRecipient, updateSettings,
  type DiscoverySchedulerStatus,
  type GraphDeviceFlowStart, type NotificationLogEntry,
  type NotificationRecipient, type NotifierStatus,
} from "../../api";
import { useToast } from "../../hooks/useToast";

const PRESET_LS_KEY = "glossa_email_provider_preset";

// Resend's free shared sender — works without verifying any domain. Mirrors
// the backend default in glossa_lab/notifications/resend.py so the From
// field is visibly populated even before /notifications/status responds and
// even when the running backend is too old to return resend_from.
//
// Resend rejects the "Display Name <email>" form for the shared sender, so
// the default is the bare email; users with a verified domain can still
// type "Glossa Lab <noreply@yourdomain.com>" — the backend preserves the
// display name in that case.
const DEFAULT_RESEND_FROM = "onboarding@resend.dev";
const SHARED_SENDER_EMAIL = "onboarding@resend.dev";

export function NotificationsPanel() {
  const { toast } = useToast();
  const [status, setStatus] = useState<NotifierStatus | null>(null);
  const [rows, setRows] = useState<NotificationRecipient[]>([]);
  const [log, setLog] = useState<NotificationLogEntry[]>([]);
  const [sched, setSched] = useState<DiscoverySchedulerStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [newLabel, setNewLabel] = useState("");

  const [presetId, setPresetId] = useState<string>(() =>
    localStorage.getItem(PRESET_LS_KEY) ?? "outlook365_oauth");
  const preset = useMemo(
    () => EMAIL_PROVIDER_PRESETS.find((p) => p.id === presetId) ?? EMAIL_PROVIDER_PRESETS[0],
    [presetId],
  );

  const [smtpHost, setSmtpHost] = useState("");
  const [smtpPort, setSmtpPort] = useState<number>(587);
  const [smtpUser, setSmtpUser] = useState("");
  const [smtpPass, setSmtpPass] = useState("");
  const [smtpFrom, setSmtpFrom] = useState("");
  const [smtpUseTls, setSmtpUseTls] = useState(true);

  // Resend HTTPS API state — just a key + optional From: address.
  // Pre-fill From with Resend's free shared sender so the input is *visibly*
  // populated the moment the user picks the Resend preset, even before the
  // backend status round-trip completes.
  const [resendKey, setResendKey] = useState("");
  const [resendFrom, setResendFrom] = useState(DEFAULT_RESEND_FROM);

  // True when the running backend is too old to know about Resend (its
  // /notifications/status response omits the resend_* fields). We detect
  // this so the UI can warn the user that saving the API key is currently
  // a no-op until the backend is restarted.
  const [backendSupportsResend, setBackendSupportsResend] = useState(true);

  const [graphFlow, setGraphFlow] = useState<GraphDeviceFlowStart | null>(null);
  const [graphPolling, setGraphPolling] = useState(false);
  const [graphError, setGraphError] = useState<string>("");
  const [graphClientId, setGraphClientId] = useState("");
  const [graphTenant, setGraphTenant] = useState("common");
  const graphPollAbort = useRef(false);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const [s, r, l, sc, settings] = await Promise.all([
        getNotifierStatus(),
        listNotificationRecipients(),
        listNotificationLog(20),
        getDiscoverySchedulerStatus().catch(() => null),
        getSettings().catch(() => null),
      ]);
      setStatus(s);
      setRows(r.recipients);
      setLog(l.entries);
      setSched(sc);
      setSmtpHost(s.host || "");
      setSmtpPort(s.port || 587);
      setSmtpFrom(s.from || "");
      setSmtpUseTls(s.use_tls ?? true);
      setGraphTenant(s.graph_tenant || "common");
      if (settings && !s.graph_client_id_set) setGraphClientId("");
      // Pre-fill Resend From with the configured value, falling back to the
      // shared-sender default so the field is never visually empty.
      setResendFrom(s.resend_from || DEFAULT_RESEND_FROM);
      // The presence of resend_configured (even when false) signals the
      // backend has the Resend transport wired in. If it's missing entirely,
      // the running backend is stale and Resend saves will silently no-op.
      setBackendSupportsResend(s.resend_configured !== undefined);
    } catch (e) {
      toast(e instanceof Error ? e.message : "Failed to load notifications", "error");
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => { void refresh(); }, [refresh]);

  useEffect(() => {
    localStorage.setItem(PRESET_LS_KEY, preset.id);
    if (preset.category === "smtp") {
      if (preset.smtp_host !== undefined) setSmtpHost(preset.smtp_host);
      if (preset.smtp_port !== undefined) setSmtpPort(preset.smtp_port);
      if (preset.smtp_use_tls !== undefined) setSmtpUseTls(preset.smtp_use_tls);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [preset.id]);

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

  const onSaveResend = async () => {
    const newKey       = resendKey.trim();
    const newFrom      = resendFrom.trim();
    const currentFrom  = (status?.resend_from || "").trim();
    const fromChanged  = newFrom.length > 0 && newFrom !== currentFrom;
    const keyAlreadySet = !!status?.resend_configured;

    // Nothing to do? Bail with a friendly message rather than firing an
    // empty PUT that the backend would happily 200-OK with no effect.
    if (!newKey && !fromChanged) {
      if (!keyAlreadySet) {
        toast("Paste your Resend API key first", "warning");
      } else {
        toast("Nothing to save — edit the From address or paste a new key", "info");
      }
      return;
    }
    // First-time setup needs a key, full stop.
    if (!newKey && !keyAlreadySet) {
      toast("Paste your Resend API key first", "warning");
      return;
    }

    setBusy(true);
    try {
      const body: Record<string, string> = {};
      if (newKey)      body.resend_api_key = newKey;
      if (fromChanged) body.resend_from    = newFrom;

      const res = await updateSettings(body);
      // The backend silently ignores keys that aren't in KNOWN_KEYS. Detect
      // a stale-backend save no-op so the user gets a real error toast and
      // not a misleading success.
      const expected = Object.keys(body);
      const missing  = expected.filter((k) => !res.updated.includes(k));
      if (missing.length > 0) {
        toast(
          `Backend ignored ${missing.join(", ")} — it's likely running an older build. ` +
          "Restart the backend (setup-os.cmd restart) and try again.",
          "error",
        );
        return;
      }

      const parts: string[] = [];
      if (newKey)      parts.push("API key updated");
      if (fromChanged) parts.push(`From set to ${newFrom}`);
      toast(`Resend: ${parts.join(" · ")}`, "success");
      setResendKey("");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Save failed", "error");
    } finally { setBusy(false); }
  };

  const onClearResend = async () => {
    if (!window.confirm("Clear the Resend API key? Email will fall back to SMTP/Outlook if configured, otherwise no transport.")) return;
    setBusy(true);
    try {
      await updateSettings({ resend_api_key: "" });
      toast("Resend API key cleared", "info");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Clear failed", "error");
    } finally { setBusy(false); }
  };

  const onSaveSmtp = async () => {
    setBusy(true);
    try {
      const body: Record<string, string> = {
        smtp_host: smtpHost.trim(),
        smtp_port: String(smtpPort || 587),
        smtp_from: smtpFrom.trim(),
        smtp_use_tls: smtpUseTls ? "1" : "0",
      };
      if (smtpUser.trim()) body.smtp_username = smtpUser.trim();
      if (smtpPass) body.smtp_password = smtpPass;
      await updateSettings(body);
      toast("SMTP settings saved", "success");
      setSmtpPass("");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Save failed", "error");
    } finally { setBusy(false); }
  };

  const onSaveGraphConfig = async () => {
    setBusy(true);
    try {
      const body: Record<string, string> = { ms_graph_tenant_id: graphTenant.trim() || "common" };
      if (graphClientId.trim()) body.ms_graph_client_id = graphClientId.trim();
      await updateSettings(body);
      toast("Outlook 365 client config saved", "success");
      setGraphClientId("");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Save failed", "error");
    } finally { setBusy(false); }
  };

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
      toast("Outlook connect failed — check ms_graph_client_id", "error");
    } finally { setBusy(false); }
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
          setGraphFlow(null); setGraphPolling(false);
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
    graphPollAbort.current = true; setGraphFlow(null); setGraphPolling(false);
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
  const isOAuthPreset = preset.category === "oauth";
  const isApiPreset   = preset.category === "api";

  return (
    <section style={section}>
      <h3 style={titleStyle}>📬 Email & Notifications</h3>
      <p style={hint}>
        Pick a mail provider, fill in the credentials it needs, then add recipients.
        Outlook 365 uses Microsoft's modern OAuth (no app password) — recommended for
        anyone with a Microsoft 365 / school / work account.
      </p>

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
                  : status?.transport === "resend"
                    ? "Resend (HTTPS API) configured"
                    : "SMTP configured")
              : "Email not configured"}
          </div>
          <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>
            {!configured
              ? "Choose a provider below and complete its setup."
              : status?.transport === "graph"
                ? `Tenant ${status?.graph_tenant} · ${activeCount}/${totalCount} active recipients`
                : status?.transport === "resend"
                  ? `From ${status?.resend_from || "onboarding@resend.dev"} · ${activeCount}/${totalCount} active recipients`
                  : `Host ${status?.host}:${status?.port} · From ${status?.from || "(unset)"} · ${activeCount}/${totalCount} active`}
          </div>
        </div>
        <button onClick={() => void onTest()} disabled={busy || !configured || activeCount === 0}
          title={activeCount === 0 ? "Add an active recipient first" : "Send a deliverability test email"}
          style={{ ...btnPrimary,
            opacity: (busy || !configured || activeCount === 0) ? 0.5 : 1,
            cursor: (busy || !configured || activeCount === 0) ? "not-allowed" : "pointer" }}>
          {busy ? "Sending…" : "✉ Send Test"}
        </button>
        <button onClick={() => void refresh()} title="Reload" style={btnGhost}>⟳</button>
      </div>

      <div style={{ marginTop: 14 }}>
        <div style={subhead}>1 · Mail provider</div>
        <select
          value={presetId}
          onChange={(e) => setPresetId(e.target.value)}
          style={{ ...input, fontSize: 13 }}
        >
          {EMAIL_PROVIDER_PRESETS.map((p) => (
            <option key={p.id} value={p.id}>
              {p.label}{p.recommended ? "  ⭐" : ""}
            </option>
          ))}
        </select>
        <p style={{ ...hint, marginTop: 6 }}>{preset.notes}</p>
      </div>

      {isOAuthPreset && (
        <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 7,
          border: "1px solid #c7d2fe", background: "#eef2ff" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            <span style={{ fontSize: 16 }}>🪪</span>
            <div style={{ flex: 1, minWidth: 240 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#3730a3" }}>
                Outlook 365 (Microsoft Graph)
              </div>
              <div style={{ fontSize: 11, color: "#4338ca", marginTop: 2 }}>
                {status?.graph_configured
                  ? `Connected. Tenant: ${status?.graph_tenant}. Mail.Send delegated.`
                  : status?.graph_client_id_set
                    ? "Client ID set, but not yet authorised. Click Connect to start."
                    : "Set the Application (client) ID below, then click Connect."}
              </div>
            </div>
            {status?.graph_configured ? (
              <button onClick={() => void onDisconnectOutlook()} disabled={busy} style={btnGhostStrong}>
                Disconnect
              </button>
            ) : (
              <button onClick={() => void onConnectOutlook()}
                disabled={busy || !status?.graph_client_id_set || graphPolling}
                title={!status?.graph_client_id_set
                  ? "Set the Application (client) ID first"
                  : "Start the device-code OAuth flow"}
                style={{ ...btnPrimary,
                  background: "#4338ca",
                  cursor: busy || !status?.graph_client_id_set ? "not-allowed" : "pointer",
                  opacity: busy || !status?.graph_client_id_set ? 0.5 : 1 }}>
                🔗 Connect Outlook 365
              </button>
            )}
          </div>

          {!status?.graph_configured && (
            <div style={{ marginTop: 10, display: "grid", gap: 6 }}>
              <input
                value={graphClientId}
                placeholder={status?.graph_client_id_set
                  ? "●●●●●●●●  (paste new Application (client) ID to replace)"
                  : "Application (client) ID  (Azure AD app registration)"}
                onChange={(e) => setGraphClientId(e.target.value)}
                style={input}
              />
              <input
                value={graphTenant}
                placeholder='Tenant ID (default "common" works for both work and personal accounts)'
                onChange={(e) => setGraphTenant(e.target.value)}
                style={input}
              />
              <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                <button onClick={() => void onSaveGraphConfig()} disabled={busy}
                  style={btnGhostStrong}>Save client config</button>
                <span style={{ fontSize: 10, color: "#6b7280" }}>
                  Need help registering an app? entra.microsoft.com → App registrations → New
                  → public client → Mail.Send delegated permission.
                </span>
              </div>
            </div>
          )}

          {graphFlow && (
            <div style={{ marginTop: 10, padding: "10px 12px", borderRadius: 6,
              background: "#fff", border: "1px solid #c7d2fe" }}>
              <div style={{ fontSize: 12, color: "#374151" }}>
                1. Open <a href={graphFlow.verification_uri} target="_blank" rel="noopener noreferrer"
                  style={{ color: "#4338ca" }}>{graphFlow.verification_uri}</a>
              </div>
              <div style={{ fontSize: 12, color: "#374151", marginTop: 4 }}>2. Paste this code:</div>
              <div style={{ marginTop: 6, fontSize: 22, fontWeight: 800, fontFamily: "monospace",
                color: "#4338ca", letterSpacing: 2, padding: "6px 10px", border: "2px dashed #c7d2fe",
                borderRadius: 6, display: "inline-block" }}>
                {graphFlow.user_code}
              </div>
              <div style={{ fontSize: 11, color: "#6b7280", marginTop: 6 }}>
                {graphPolling ? "Waiting for approval…" : "Polling stopped"}
                {" "}· Code expires in {Math.round(graphFlow.expires_in / 60)} min.
                <button onClick={onCancelOutlookFlow} style={{ ...btnGhost, marginLeft: 8 }}>Cancel</button>
              </div>
            </div>
          )}
          {graphError && (
            <div style={{ marginTop: 8, fontSize: 11, color: "#b91c1c" }}>⚠ {graphError}</div>
          )}
        </div>
      )}

      {/* API path — currently only Resend, but the slot is generic. */}
      {isApiPreset && (
        <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 7,
          border: "1px solid #bbf7d0", background: "#f0fdf4" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            <span style={{ fontSize: 16 }}>⚡</span>
            <div style={{ flex: 1, minWidth: 240 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#15803d" }}>
                Resend (HTTPS API)
              </div>
              <div style={{ fontSize: 11, color: "#166534", marginTop: 2 }}>
                {status?.resend_configured
                  ? `Connected. Sends from ${status?.resend_from || DEFAULT_RESEND_FROM}.`
                  : "Paste your Resend API key (starts with re_). No SMTP, no mailbox, no domain needed."}
              </div>
            </div>
            {status?.resend_configured && (
              <button onClick={() => void onClearResend()} disabled={busy}
                style={{ ...btnGhostStrong, color: "#15803d", borderColor: "#bbf7d0" }}>
                Clear key
              </button>
            )}
          </div>
          {!backendSupportsResend && (
            <div style={{ marginTop: 10, padding: "8px 12px", borderRadius: 6,
              border: "1px solid #fcd34d", background: "#fffbeb",
              fontSize: 11, color: "#92400e" }}>
              ⚠ The running backend doesn&rsquo;t expose Resend yet — saving the
              key here will be silently ignored. Restart the backend
              (<code>setup-os.cmd restart</code>) so the new transport loads,
              then come back to this screen.
            </div>
          )}
          {backendSupportsResend && status?.resend_configured && status?.transport !== "resend" && (
            <div style={{ marginTop: 10, padding: "8px 12px", borderRadius: 6,
              border: "1px solid #fcd34d", background: "#fffbeb",
              fontSize: 11, color: "#92400e" }}>
              ⚠ Resend is configured but the active transport is
              <b> {status?.transport}</b>. Microsoft Graph (Outlook OAuth)
              outranks Resend; if you don&rsquo;t want that, click
              <b> Disconnect Outlook 365</b> above. Plain SMTP cannot outrank
              Resend, so if you see <i>smtp</i> here despite Resend being
              configured, the backend hasn&rsquo;t reloaded yet — restart it.
            </div>
          )}
          {(() => {
              const fromEmail = (resendFrom.match(/<([^>]+)>/)?.[1] ?? resendFrom).trim().toLowerCase();
              const isShared  = fromEmail === SHARED_SENDER_EMAIL;
              return isShared && (
                <div style={{ marginTop: 10, padding: "8px 12px", borderRadius: 6,
                  border: "1px solid #fde68a", background: "#fffbeb",
                  fontSize: 11, color: "#92400e" }}>
                  ℹ You&rsquo;re using Resend&rsquo;s free shared sender
                  (<code>onboarding@resend.dev</code>). Resend will only
                  deliver to the email you signed up to Resend with.
                  Recipients other than that one address get a 403.
                  Verify your own domain at
                  {" "}<a href="https://resend.com/domains" target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: "#92400e", textDecoration: "underline" }}>
                    resend.com/domains
                  </a>
                  {" "}and switch From to <code>noreply@&lt;your-domain&gt;</code>
                  to send to anyone.
                </div>
              );
            })()}
          <div style={{ display: "grid", gap: 8, marginTop: 10 }}>
            <label style={{ fontSize: 11, fontWeight: 600, color: "#166534",
              display: "flex", flexDirection: "column", gap: 4 }}>
              API key
              <input value={resendKey}
                onChange={(e) => setResendKey(e.target.value)}
                placeholder={status?.resend_configured
                  ? "●●●●●●●●  (leave blank to keep current key)"
                  : "Resend API key (re_xxx…)"}
                type="password" autoComplete="off" style={input} />
            </label>
            <label style={{ fontSize: 11, fontWeight: 600, color: "#166534",
              display: "flex", flexDirection: "column", gap: 4 }}>
              From address (always editable)
              <input value={resendFrom}
                onChange={(e) => setResendFrom(e.target.value)}
                placeholder='"noreply@yourdomain.com" or "Glossa Lab <noreply@yourdomain.com>" once a domain is verified at resend.com/domains.'
                style={input} />
              <span style={{ fontSize: 10, fontWeight: 400, color: "#6b7280" }}>
                Currently saved: <code>{status?.resend_from || "(unset)"}</code>
              </span>
            </label>
            {(() => {
              const newKey      = resendKey.trim();
              const newFrom     = resendFrom.trim();
              const currentFrom = (status?.resend_from || "").trim();
              const fromChanged = newFrom.length > 0 && newFrom !== currentFrom;
              const canSave     = !!newKey || (!!status?.resend_configured && fromChanged);
              const label = busy
                ? "Saving…"
                : !status?.resend_configured
                  ? "Save Resend key"
                  : newKey && fromChanged
                    ? "Save key + From"
                    : newKey
                      ? "Replace key"
                      : fromChanged
                        ? "Save From address"
                        : "Save Resend settings";
              return (
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  <button onClick={() => void onSaveResend()}
                    disabled={busy || !canSave} style={{ ...btnPrimary,
                      opacity: (busy || !canSave) ? 0.5 : 1,
                      cursor:  (busy || !canSave) ? "not-allowed" : "pointer" }}>
                    {label}
                  </button>
                  <button onClick={() => void onTest()}
                    disabled={busy || !configured || activeCount === 0}
                    style={{ ...btnGhostStrong,
                      cursor: (busy || !configured || activeCount === 0) ? "not-allowed" : "pointer",
                      opacity: (busy || !configured || activeCount === 0) ? 0.5 : 1 }}>
                    ✉ Send test
                  </button>
                  <a href="https://resend.com/api-keys" target="_blank" rel="noopener noreferrer"
                    style={{ marginLeft: "auto", fontSize: 11, color: "#15803d",
                      alignSelf: "center" }}>
                    Get an API key →
                  </a>
                </div>
              );
            })()}
          </div>
        </div>
      )}

      {!isOAuthPreset && !isApiPreset && (
        <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 7,
          border: "1px solid #e5e7eb", background: "#fafafa" }}>
          <div style={{ ...subhead, color: "#374151", margin: "0 0 8px" }}>
            2 · SMTP credentials
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 8 }}>
            <input value={smtpHost} placeholder="SMTP host (e.g. smtp.gmail.com)"
              onChange={(e) => setSmtpHost(e.target.value)} style={input} />
            <input value={smtpPort || ""} type="number"
              placeholder="Port (587)"
              onChange={(e) => setSmtpPort(parseInt(e.target.value || "0", 10) || 587)}
              style={input} />
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginTop: 8 }}>
            <input value={smtpUser} placeholder="Username (usually your full email address)"
              onChange={(e) => setSmtpUser(e.target.value)} style={input} autoComplete="off" />
            <input value={smtpPass} type="password"
              placeholder={status?.password_set ? "●●●●●●●●  (paste new app password)" : "App password / SMTP password"}
              onChange={(e) => setSmtpPass(e.target.value)} style={input} autoComplete="off" />
          </div>
          <input value={smtpFrom}
            placeholder='From address (e.g. "Glossa Lab <noreply@example.com>" or just an email)'
            onChange={(e) => setSmtpFrom(e.target.value)}
            style={{ ...input, marginTop: 8 }} />
          <label style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 8, fontSize: 12, color: "#374151" }}>
            <input type="checkbox" checked={smtpUseTls}
              onChange={(e) => setSmtpUseTls(e.target.checked)} />
            Use STARTTLS (recommended)
          </label>
          <div style={{ display: "flex", gap: 6, marginTop: 10, flexWrap: "wrap" }}>
            <button onClick={() => void onSaveSmtp()} disabled={busy} style={btnPrimary}>
              {busy ? "Saving…" : "Save SMTP settings"}
            </button>
            <button onClick={() => void onTest()}
              disabled={busy || !configured || activeCount === 0}
              style={{ ...btnGhostStrong,
                cursor: (busy || !configured || activeCount === 0) ? "not-allowed" : "pointer",
                opacity: (busy || !configured || activeCount === 0) ? 0.5 : 1 }}>
              ✉ Send test
            </button>
          </div>
        </div>
      )}

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
                  sched.enabled ? "Persisted; resumes on next backend boot." : "Not persisted."
                }`
              : "Loading scheduler status…"}
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

      <div style={{ marginTop: 14 }}>
        <div style={subhead}>3 · Recipients ({rows.length})</div>
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
                    <div style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}>{r.label}</div>
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

        <div style={{ display: "flex", gap: 6, marginTop: 8, flexWrap: "wrap" }}>
          <input value={newEmail}
            onChange={(e) => setNewEmail(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && newEmail.trim()) void onAdd(); }}
            placeholder="recipient@example.com"
            style={{ ...input, flex: 2, minWidth: 200 }} />
          <input value={newLabel}
            onChange={(e) => setNewLabel(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && newEmail.trim()) void onAdd(); }}
            placeholder="Label (optional, e.g. PI, lab)"
            style={{ ...input, flex: 1, minWidth: 140 }} />
          <button onClick={() => void onAdd()} disabled={busy || !newEmail.trim()}
            style={{ ...btnAccent,
              cursor: busy || !newEmail.trim() ? "not-allowed" : "pointer",
              opacity: busy || !newEmail.trim() ? 0.5 : 1 }}>
            + Add
          </button>
        </div>
      </div>

      <details style={{ marginTop: 16 }}>
        <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13, color: "#374151" }}>
          📜 Recent send log ({log.length})
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
                      <div style={{ fontSize: 10, color: "#dc2626", marginTop: 1 }}>{row.error}</div>
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

const section: React.CSSProperties = {
  marginBottom: "2rem", padding: "1.25rem",
  border: "1px solid #e5e7eb", borderRadius: 8,
};
const titleStyle: React.CSSProperties = {
  margin: "0 0 0.5rem 0", fontSize: 15, fontWeight: 600, color: "#111827",
};
const hint: React.CSSProperties = {
  margin: 0, fontSize: 12, color: "#6b7280", lineHeight: 1.5,
};
const subhead: React.CSSProperties = {
  fontSize: 11, fontWeight: 700, color: "#7c3aed",
  textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6,
};
const input: React.CSSProperties = {
  padding: "6px 10px", border: "1px solid #d1d5db", borderRadius: 5,
  fontSize: 13, width: "100%", boxSizing: "border-box", outline: "none",
};
const btnPrimary: React.CSSProperties = {
  padding: "5px 12px", border: "1px solid #2563eb", borderRadius: 6,
  background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const btnAccent: React.CSSProperties = {
  padding: "6px 16px", border: "none", borderRadius: 5,
  background: "#7c3aed", color: "#fff", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const btnGhost: React.CSSProperties = {
  padding: "5px 9px", border: "1px solid #d1d5db", borderRadius: 5,
  background: "#fff", cursor: "pointer", fontSize: 12,
};
const btnGhostStrong: React.CSSProperties = {
  padding: "5px 12px", border: "1px solid #c7d2fe", borderRadius: 6,
  background: "#fff", color: "#4338ca", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
