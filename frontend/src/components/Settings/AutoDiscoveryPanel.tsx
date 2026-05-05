/**
 * AutoDiscoveryPanel — single Settings tab for everything Discovery-related.
 *
 * Consolidates:
 *   • Source API keys (NewsAPI, SerpAPI, Brave Search) with inline verify
 *   • Manual fetch + mine triggers (mirrors the Discovery view but reachable
 *     from Settings without leaving the page)
 *   • Scheduler auto-start toggle + interval display
 *   • Notify-on-run preference + jump-to-recipients link
 *
 * The full recipient list / SMTP config still lives in the Email & Notifications
 * panel below; this panel intentionally only exposes the discovery-specific
 * controls so users have a single place to see "is the discovery loop running?"
 */

import { useCallback, useEffect, useState } from "react";
import {
  getDiscoverySchedulerStatus,
  getNotifierStatus,
  getSettings,
  listDiscoverySources,
  listDiscoveryTopics,
  startDiscoveryFetch,
  startDiscoveryMine,
  startDiscoveryScheduler,
  stopDiscoveryScheduler,
  updateSettings,
  verifyKey,
  type DiscoverySchedulerStatus,
  type DiscoverySource,
  type DiscoveryTopic,
  type NotifierStatus,
  type SettingsResponse,
  type VerifyKeyResult,
} from "../../api";
import { useToast } from "../../hooks/useToast";

const SOURCE_KEYS: { id: string; label: string; href: string }[] = [
  { id: "news_api_key",         label: "NewsAPI",       href: "https://newsapi.org/account" },
  { id: "serp_api_key",         label: "SerpAPI",       href: "https://serpapi.com/manage-api-key" },
  { id: "brave_search_api_key", label: "Brave Search",  href: "https://api-dashboard.search.brave.com/" },
];

export function AutoDiscoveryPanel() {
  const { toast } = useToast();
  const [settings, setSettings] = useState<SettingsResponse | null>(null);
  const [sources, setSources]   = useState<DiscoverySource[]>([]);
  const [topics,  setTopics]    = useState<DiscoveryTopic[]>([]);
  const [sched,   setSched]     = useState<DiscoverySchedulerStatus | null>(null);
  const [notif,   setNotif]     = useState<NotifierStatus | null>(null);

  const [pendingKeys, setPendingKeys] = useState<Record<string, string>>({});
  const [verify,      setVerify]      = useState<Record<string, VerifyKeyResult | "loading">>({});

  const [busy,    setBusy]    = useState(false);
  const [fetching, setFetching] = useState(false);
  const [mining,   setMining]   = useState(false);

  const refresh = useCallback(async () => {
    try {
      const [s, src, top, sc, n] = await Promise.all([
        getSettings(),
        listDiscoverySources(),
        listDiscoveryTopics(),
        getDiscoverySchedulerStatus().catch(() => null),
        getNotifierStatus().catch(() => null),
      ]);
      setSettings(s); setSources(src.sources); setTopics(top.topics);
      setSched(sc);   setNotif(n);
    } catch (e) {
      toast(e instanceof Error ? e.message : "Failed to load discovery state", "error");
    }
  }, [toast]);

  useEffect(() => { void refresh(); }, [refresh]);

  // ── Source-key save+verify ─────────────────────────────────────────────
  const onSaveKey = async (k: string) => {
    const v = (pendingKeys[k] ?? "").trim();
    if (!v) { toast("Paste a value first", "warning"); return; }
    setBusy(true);
    try {
      await updateSettings({ [k]: v });
      setPendingKeys((p) => ({ ...p, [k]: "" }));
      toast(`${k} saved`, "success");
      await refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Save failed", "error");
    } finally { setBusy(false); }
  };

  const onVerifyKey = async (k: string) => {
    setVerify((v) => ({ ...v, [k]: "loading" }));
    try {
      const r = await verifyKey(k);
      setVerify((v) => ({ ...v, [k]: r }));
    } catch (e) {
      setVerify((v) => ({
        ...v, [k]: { valid: false, provider: k,
          message: e instanceof Error ? e.message : "verify failed" },
      }));
    }
  };

  // ── Scheduler toggle ───────────────────────────────────────────────────
  const onToggleScheduler = async (enable: boolean) => {
    setBusy(true);
    try {
      const next = enable ? await startDiscoveryScheduler() : await stopDiscoveryScheduler();
      setSched(next);
      toast(enable
        ? `Auto-start ON · every ${Math.round(next.interval_seconds / 3600)}h`
        : "Auto-start OFF", "info");
    } catch (e) {
      toast(e instanceof Error ? e.message : "Toggle failed", "error");
    } finally { setBusy(false); }
  };

  // ── Manual fetch + mine ────────────────────────────────────────────────
  const onRunFetch = async () => {
    setFetching(true);
    try {
      const ack = await startDiscoveryFetch({});
      toast(`Fetch started · job ${ack.job_id.slice(0, 8)}`, "info");
    } catch (e) {
      toast(e instanceof Error ? e.message : "Fetch failed to start", "error");
    } finally { setFetching(false); }
  };
  const onRunMine = async () => {
    setMining(true);
    try {
      const ack = await startDiscoveryMine({ limit: 50 });
      toast(`Mine started · job ${ack.job_id.slice(0, 8)} · limit 50`, "info");
    } catch (e) {
      toast(e instanceof Error ? e.message : "Mine failed to start", "error");
    } finally { setMining(false); }
  };

  const configuredSources = sources.filter((s) => s.configured).length;
  const totalSources      = sources.length;

  return (
    <section style={section}>
      <h3 style={titleStyle}>🔭 Auto Discovery</h3>
      <p style={hint}>
        The continuous-discovery loop fetches new findings from external sources,
        classifies + de-duplicates them via your AI provider, and surfaces them in
        the Discovery view + Dashboard. Configure the sources, toggle the schedule,
        and trigger manual runs from this panel.
      </p>

      {/* Status strip */}
      <div style={{
        marginTop: 10, padding: "10px 14px", borderRadius: 7,
        border: `1px solid ${sched?.running ? "#86efac" : "#fcd34d"}`,
        background: sched?.running ? "#f0fdf4" : "#fffbeb",
        display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap",
      }}>
        <span style={{ fontSize: 16 }}>{sched?.running ? "⏱️" : "💤"}</span>
        <div style={{ flex: 1, minWidth: 220 }}>
          <div style={{ fontSize: 13, fontWeight: 600,
            color: sched?.running ? "#15803d" : "#92400e" }}>
            {sched?.running ? "Auto-discovery running" : "Auto-discovery off"}
          </div>
          <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>
            {configuredSources}/{totalSources} sources configured
            {sched ? ` · interval ${Math.round(sched.interval_seconds / 3600)}h` : ""}
            {sched?.enabled ? " · persisted" : sched ? " · not persisted" : ""}
            {topics.length > 0 ? ` · ${topics.length} topic(s)` : ""}
          </div>
        </div>
        <div onClick={() => !busy && void onToggleScheduler(!sched?.running)}
          title={sched?.running ? "Stop scheduler" : "Start scheduler + persist"}
          style={{ width: 44, height: 24, borderRadius: 12,
            cursor: busy ? "not-allowed" : "pointer", flexShrink: 0,
            position: "relative",
            background: sched?.running ? "#22c55e" : "#d1d5db",
            opacity: busy ? 0.5 : 1, transition: "background 0.2s" }}>
          <div style={{ position: "absolute", top: 3, left: sched?.running ? 23 : 3,
            width: 18, height: 18, borderRadius: "50%", background: "#fff",
            boxShadow: "0 1px 3px rgba(0,0,0,0.25)", transition: "left 0.2s" }} />
        </div>
      </div>

      {/* Manual run buttons */}
      <div style={{ marginTop: 14 }}>
        <div style={subhead}>1 · Manual run</div>
        <p style={{ ...hint, marginTop: 4 }}>
          Trigger a fetch (pulls new items from every configured source for every
          topic) and/or a mine (LLM-classifies un-mined items in the queue). Both
          run as background jobs you can watch in the Jobs panel.
        </p>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <button onClick={() => void onRunFetch()} disabled={fetching}
            style={{ ...btnPrimary,
              opacity: fetching ? 0.5 : 1,
              cursor:  fetching ? "not-allowed" : "pointer" }}>
            {fetching ? "⏳ Fetching…" : "▶ Fetch now"}
          </button>
          <button onClick={() => void onRunMine()} disabled={mining}
            style={{ ...btnAccent,
              opacity: mining ? 0.5 : 1,
              cursor:  mining ? "not-allowed" : "pointer" }}>
            {mining ? "⏳ Mining…" : "✨ Mine now (50)"}
          </button>
          <span style={{ flex: 1 }} />
          <a href="#" onClick={(e) => {
              e.preventDefault();
              window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "discovery" } }));
            }}
            style={{ alignSelf: "center", fontSize: 11, color: "#2563eb", textDecoration: "underline" }}>
            Open Discovery view →
          </a>
        </div>
        <p style={{ ...hint, marginTop: 8, fontSize: 11 }}>
          Or from a shell:&nbsp;
          <code>python -m glossa_lab.discovery fetch</code> / <code>mine --limit 50</code> / <code>daily --notify</code>
        </p>
      </div>

      {/* Source API keys */}
      <div style={{ marginTop: 14 }}>
        <div style={subhead}>2 · Source API keys</div>
        <p style={{ ...hint, marginTop: 4 }}>
          Each fetcher is enabled when its key is set. OpenAlex, arXiv, Crossref,
          Wikidata, and GitHub are key-less and always on.
        </p>
        <div style={{ display: "grid", gap: 8, marginTop: 8 }}>
          {SOURCE_KEYS.map((k) => {
            const isSet = settings?.keys[k.id]?.set ?? false;
            const src   = (settings?.keys[k.id]?.source ?? null) as "env" | "stored" | null;
            const v     = verify[k.id];
            return (
              <div key={k.id} style={{
                padding: 10, border: "1px solid #e5e7eb", borderRadius: 7, background: "#fff",
                display: "flex", flexDirection: "column", gap: 6,
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
                  <span style={{ fontSize: 13, fontWeight: 600, color: "#111827" }}>{k.label}</span>
                  {isSet ? (
                    <span style={{ fontSize: 10, padding: "1px 7px", borderRadius: 9,
                      background: "#dcfce7", color: "#15803d", fontWeight: 700 }}>
                      SET ({src})
                    </span>
                  ) : (
                    <span style={{ fontSize: 10, padding: "1px 7px", borderRadius: 9,
                      background: "#fee2e2", color: "#b91c1c", fontWeight: 700 }}>
                      MISSING
                    </span>
                  )}
                  <a href={k.href} target="_blank" rel="noopener noreferrer"
                    style={{ fontSize: 11, color: "#2563eb", marginLeft: "auto" }}>
                    Get a key →
                  </a>
                </div>
                <div style={{ display: "flex", gap: 6 }}>
                  <input value={pendingKeys[k.id] ?? ""}
                    onChange={(e) => setPendingKeys((p) => ({ ...p, [k.id]: e.target.value }))}
                    placeholder={isSet ? "●●●●●●●● (paste new value to replace)" : `Paste your ${k.label} API key`}
                    type="password" autoComplete="off" style={input} />
                  <button onClick={() => void onSaveKey(k.id)}
                    disabled={busy || !(pendingKeys[k.id]?.trim())}
                    style={{ ...btnGhostStrong,
                      opacity: (busy || !pendingKeys[k.id]?.trim()) ? 0.5 : 1,
                      cursor:  (busy || !pendingKeys[k.id]?.trim()) ? "not-allowed" : "pointer" }}>
                    Save
                  </button>
                  <button onClick={() => void onVerifyKey(k.id)}
                    disabled={!isSet || v === "loading"}
                    style={{ ...btnGhost,
                      opacity: (!isSet || v === "loading") ? 0.5 : 1,
                      cursor:  (!isSet || v === "loading") ? "not-allowed" : "pointer" }}>
                    {v === "loading" ? "…" : "Verify"}
                  </button>
                </div>
                {v && v !== "loading" && (
                  <div style={{ fontSize: 11,
                    color: v.valid ? "#15803d" : "#b91c1c" }}>
                    {v.valid ? "✓" : "✗"} {v.message}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Notify-on-run + recipient summary */}
      <div style={{ marginTop: 14 }}>
        <div style={subhead}>3 · Email digest on run</div>
        <p style={{ ...hint, marginTop: 4 }}>
          When notifications are configured (any active recipient + a working
          transport), every scheduled fetch+mine cycle sends a digest of new
          findings.
        </p>
        <div style={{
          padding: 10, borderRadius: 7,
          border: `1px solid ${notif?.configured ? "#86efac" : "#fcd34d"}`,
          background: notif?.configured ? "#f0fdf4" : "#fffbeb",
          display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap",
        }}>
          <span style={{ fontSize: 14 }}>{notif?.configured ? "✉" : "⚠"}</span>
          <div style={{ flex: 1, minWidth: 220 }}>
            <div style={{ fontSize: 12, fontWeight: 600,
              color: notif?.configured ? "#15803d" : "#92400e" }}>
              {notif?.configured
                ? `Transport: ${notif?.transport} · ${notif?.recipients_active}/${notif?.recipients_total} active recipient(s)`
                : "Email transport not configured"}
            </div>
            <div style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>
              {notif?.configured
                ? "Manage recipients + send a test in the Email & Notifications section below."
                : "Configure Resend, Outlook 365 OAuth, or SMTP in the Email & Notifications section below."}
            </div>
          </div>
        </div>
      </div>

      {/* Configured-source summary */}
      <div style={{ marginTop: 14 }}>
        <div style={subhead}>4 · Sources detected by the backend</div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 6 }}>
          {sources.map((s) => (
            <span key={s.source} title={s.disabled_reason || `${s.source} ready`}
              style={{
                padding: "3px 9px", borderRadius: 12, border: "1px solid",
                background: s.configured ? "#f0fdf4" : "#fafafa",
                borderColor: s.configured ? "#86efac" : "#e5e7eb",
                color: s.configured ? "#15803d" : "#9ca3af",
                fontSize: 11, fontWeight: 500,
              }}>
              {s.configured ? "✓ " : "✗ "}{s.source}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}

// ── Styles ─────────────────────────────────────────────────────────────
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
  flex: 1, padding: "6px 10px", border: "1px solid #d1d5db", borderRadius: 5,
  fontSize: 13, boxSizing: "border-box", outline: "none",
};
const btnPrimary: React.CSSProperties = {
  padding: "6px 14px", border: "1px solid #2563eb", borderRadius: 6,
  background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const btnAccent: React.CSSProperties = {
  padding: "6px 14px", border: "1px solid #7c3aed", borderRadius: 6,
  background: "#7c3aed", color: "#fff", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const btnGhost: React.CSSProperties = {
  padding: "5px 10px", border: "1px solid #d1d5db", borderRadius: 5,
  background: "#fff", cursor: "pointer", fontSize: 12,
};
const btnGhostStrong: React.CSSProperties = {
  padding: "5px 12px", border: "1px solid #c7d2fe", borderRadius: 6,
  background: "#fff", color: "#4338ca", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
