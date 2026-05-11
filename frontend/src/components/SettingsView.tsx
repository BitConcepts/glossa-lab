import { useEffect, useRef, useState } from "react";
import {
  getEnvPackages,
  getEnvStatus,
  getSettings,
  isLocalKeySet, clearLocalKey, getLocalKeys, setLocalKey,
  runEnvRebuild, runEnvSetup, runEnvUpgrade,
  updateSettings,
  verifyKey,
  type EnvPackage, type EnvStatus, type KeyStatus,
  type VerifyKeyResult,
} from "../api";
import { useToast } from "../hooks/useToast";
import { NotificationsPanel } from "./Notifications/NotificationsPanel";
import { AutoDiscoveryPanel } from "./Settings/AutoDiscoveryPanel";
import { ProvidersPanel } from "./Settings/ProvidersPanel";
import { ModelAssignmentsPanel } from "./Settings/ModelAssignmentsPanel";

type KeyMeta = { label: string; hint: string; priority?: boolean; verifiable?: boolean };

// Discovery source keys — shown on the "Discovery" tab.
const DISCOVERY_KEY_LABELS: Record<string, KeyMeta> = {
  serp_api_key: {
    label: "SerpAPI Key",
    hint: "Google News + Scholar via serpapi.com.",
    verifiable: true,
  },
  news_api_key: {
    label: "NewsAPI Key",
    hint: "Latest articles via newsapi.org.",
    verifiable: true,
  },
  brave_search_api_key: {
    label: "Brave Search Key",
    hint: "Web + news search via api.search.brave.com.",
    verifiable: true,
  },
  semantic_scholar_api_key: {
    label: "Semantic Scholar Key",
    hint: "Optional — removes 100 req/5min cap. Free at semanticscholar.org/product/api.",
    verifiable: true,
  },
  openalex_email: {
    label: "OpenAlex Email",
    hint: "Optional — email for polite-pool priority access.",
    verifiable: true,
  },
  uspto_api_key: {
    label: "USPTO (ODP) API Key",
    hint: "For patent data from api.uspto.gov.",
    verifiable: true,
  },
  academia_session_cookie: {
    label: "Academia.edu Session Cookie",
    hint: "Optional — paste from browser to enable authenticated PDF downloads.",
  },
};

// Combined for the key-input renderer.
const ALL_KEY_LABELS: Record<string, KeyMeta> = { ...DISCOVERY_KEY_LABELS };

// ── Python Environment Section ─────────────────────────────────────────────

function PythonEnvSection() {
  const { toast } = useToast();
  const [status, setStatus] = useState<EnvStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [output, setOutput] = useState<{ text: string; type: string }[]>([]);
  const [packages, setPackages] = useState<EnvPackage[] | null>(null);
  const [outputOpen, setOutputOpen] = useState(true);
  const [packagesOpen, setPackagesOpen] = useState(true);
  // ref points to the scrollable output container, NOT a sentinel inside it
  const outputContainerRef = useRef<HTMLDivElement>(null);

  const refresh = async () => {
    setLoading(true);
    try { setStatus(await getEnvStatus()); } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  useEffect(() => { refresh(); }, []);
  // Scroll the output container itself — never scroll the page
  useEffect(() => {
    const el = outputContainerRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [output]);

  const runStream = async (fetcher: () => Promise<Response>, label: string) => {
    setRunning(true);
    setOutput([{ text: `Running: ${label}…`, type: "info" }]);
    try {
      const resp = await fetcher();
      if (!resp.body) { setOutput(o => [...o, { text: "No response body", type: "error" }]); return; }
      const reader = resp.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const parts = buf.split("\n\n"); buf = parts.pop() ?? "";
        for (const part of parts) {
          for (const ln of part.split("\n")) {
            if (ln.startsWith("data: ")) {
              try {
                const d = JSON.parse(ln.slice(6)) as { text?: string };
                if (d.text) {
                  const isErr = d.text.toLowerCase().includes("error") || d.text.startsWith("⚠");
                  const isDone = d.text.startsWith("✓");
                  setOutput(o => [...o, { text: d.text!, type: isErr ? "error" : isDone ? "success" : "output" }]);
                }
              } catch { /* ignore */ }
            } else if (ln.startsWith("event: done") || ln.startsWith("event: error")) {
              // handled via data
            }
          }
        }
      }
      await refresh();
      toast(`${label} complete`, "success");
    } catch (e) {
      setOutput(o => [...o, { text: `Failed: ${e instanceof Error ? e.message : String(e)}`, type: "error" }]);
      toast(`${label} failed`, "error");
    } finally {
      setRunning(false);
    }
  };

  // Show-packages is a *toggle*: first click fetches + shows; second click
  // hides the list without re-fetching; a third click re-shows the cached
  // list immediately, with the latest counts updated only on the first click
  // of each session.
  const togglePackages = async () => {
    if (packages !== null) {
      // Already loaded — toggle visibility without re-fetching.
      setPackages(null);
      return;
    }
    const r = await getEnvPackages();
    setPackages(r.packages);
    // Default the inner accordion to "open" when first revealed so the user
    // sees the list immediately rather than just a header.
    setPackagesOpen(true);
  };

  const active = status?.venv_exists;
  const dotColor = loading ? "#9ca3af" : active ? "#16a34a" : "#ef4444";
  const dotLabel = loading ? "checking…" : active ? `Active \u00b7 Python ${status?.python_version ?? "?"}` : "Not found";

  const btnSt = (color: string, disabled: boolean): React.CSSProperties => ({
    padding: "5px 12px", border: "none", borderRadius: 5,
    background: disabled ? "#e5e7eb" : color, color: disabled ? "#9ca3af" : "#fff",
    cursor: disabled ? "not-allowed" : "pointer", fontSize: 12, fontWeight: 600,
  });

  return (
    <section style={ollamaSection}>
      <h3 style={{ margin: "0 0 10px", fontSize: 15, fontWeight: 600, color: "#111827" }}>🐍 Python Environment</h3>

      {/* Status row */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12, padding: "10px 14px",
        background: active ? "#f0fdf4" : "#fef2f2",
        border: `1px solid ${active ? "#86efac" : "#fca5a5"}`, borderRadius: 7 }}>
        <span style={{ width: 9, height: 9, borderRadius: "50%", background: dotColor, flexShrink: 0 }} />
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#111827" }}>{dotLabel}</div>
          {status?.venv_path && <div style={{ fontSize: 10, color: "#6b7280", fontFamily: "monospace", marginTop: 1 }}>{status.venv_path}</div>}
          {active && <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>{status?.pkg_count ?? 0} packages installed</div>}
        </div>
        <button onClick={refresh} style={{ padding: "3px 8px", border: "1px solid #d1d5db", borderRadius: 4, background: "#fff", cursor: "pointer", fontSize: 11, color: "#6b7280" }}>⟳</button>
      </div>

      {/* Warning if no venv */}
      {!active && !loading && (
        <div style={{ padding: "12px 14px", background: "#fef3c7", border: "1px solid #fcd34d", borderRadius: 6, marginBottom: 12, fontSize: 12, color: "#92400e" }}>
          No virtual environment found. Click <strong>Setup venv</strong> to create one and install all dependencies.
        </div>
      )}

      {/* Action buttons */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
        <button onClick={() => runStream(runEnvSetup, "Setup venv")} disabled={running}
          style={btnSt("#16a34a", running)}>
          ⬇ Setup venv
        </button>
        <button onClick={() => runStream(runEnvRebuild, "Rebuild venv")} disabled={running}
          style={btnSt("#ea580c", running)}>
          ↺ Rebuild venv
        </button>
        <button onClick={() => runStream(runEnvUpgrade, "Upgrade deps")} disabled={running || !active}
          style={btnSt("#2563eb", running || !active)}>
          ↑ Upgrade deps
        </button>
        <button onClick={togglePackages} disabled={!active}
          style={btnSt("#7c3aed", !active)}
          title={packages !== null
            ? "Hide the package list (does not uninstall anything)"
            : "Fetch and show installed packages"}>
          {packages !== null ? "📦 Hide packages" : "📦 Show packages"}
        </button>
      </div>

      {/* Output stream — collapsible */}
      {output.length > 0 && (
        <div style={{ marginBottom: 10 }}>
          <button
            onClick={() => setOutputOpen(o => !o)}
            style={{ display: "flex", alignItems: "center", gap: 5, background: "none",
              border: "none", cursor: "pointer", padding: "2px 0", marginBottom: 4,
              fontSize: 11, fontWeight: 700, color: "#374151", textTransform: "uppercase", letterSpacing: 0.5 }}
          >
            <span style={{ fontSize: 9, transition: "transform .15s", transform: outputOpen ? "rotate(90deg)" : "rotate(0deg)" }}>▶</span>
            Install output
          </button>
          {outputOpen && (
            /* ref is on THIS div so scrollTop affects only this container */
            <div ref={outputContainerRef}
              style={{ background: "#0f172a", borderRadius: 5, padding: "8px 10px",
                maxHeight: 200, overflowY: "auto", fontFamily: "monospace", fontSize: 11 }}>
              {output.map((l, i) => (
                <div key={i} style={{ color: l.type === "error" ? "#f87171" : l.type === "success" ? "#86efac" : "#e2e8f0", lineHeight: 1.6 }}>{l.text}</div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Package list — collapsible */}
      {packages && (
        <div>
          <button
            onClick={() => setPackagesOpen(o => !o)}
            style={{ display: "flex", alignItems: "center", gap: 5, background: "none",
              border: "none", cursor: "pointer", padding: "2px 0", marginBottom: 4,
              fontSize: 11, fontWeight: 700, color: "#374151", textTransform: "uppercase", letterSpacing: 0.5 }}
          >
            <span style={{ fontSize: 9, transition: "transform .15s", transform: packagesOpen ? "rotate(90deg)" : "rotate(0deg)" }}>▶</span>
            Installed packages ({packages.length})
          </button>
          {packagesOpen && (
            <div style={{ display: "flex", flexWrap: "wrap", gap: "2px 8px", maxHeight: 140, overflowY: "auto" }}>
              {packages.map(p => (
                <span key={p.name} style={{ fontSize: 10, fontFamily: "monospace", color: "#374151" }}>
                  {p.name} <span style={{ color: "#9ca3af" }}>{p.version}</span>
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
}

const SETTINGS_TAB_KEY = "glossa_settings_tab";
type SettingsTab = "ai" | "discovery" | "notifications" | "system";
const TABS: { id: SettingsTab; label: string; icon: string }[] = [
  { id: "ai",            label: "AI",            icon: "🤖" },
  { id: "discovery",     label: "Discovery",     icon: "🔭" },
  { id: "notifications", label: "Notifications", icon: "✉️" },
  { id: "system",        label: "System",        icon: "⚙️" },
];

// ── Main SettingsView ─────────────────────────────────────────────────────

export function SettingsView() {
  const [tab, setTabState] = useState<SettingsTab>(() => {
    const saved = localStorage.getItem(SETTINGS_TAB_KEY);
    return (saved && TABS.some(t => t.id === saved) ? saved : "ai") as SettingsTab;
  });
  const setTab = (t: SettingsTab) => { setTabState(t); localStorage.setItem(SETTINGS_TAB_KEY, t); };

  const [backendKeys, setBackendKeys] = useState<Record<string, KeyStatus>>({});
  const [dataDir, setDataDir] = useState("");
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState<Record<string, string>>({});
  const [error, setError] = useState("");
  const [verifying, setVerifying] = useState<Record<string, boolean>>({});
  const [verifyResult, setVerifyResult] = useState<Record<string, VerifyKeyResult>>({});

  const load = async () => {
    try {
      const s = await getSettings();
      setBackendKeys(s.keys);
      setDataDir(s.data_dir);
      setError("");
    } catch {
      // Backend might not be available; localStorage still works
    }
  };

  useEffect(() => { load(); }, []);

  // A key is "set" if it's in localStorage OR in backend env/storage
  const isSet = (key: string) => isLocalKeySet(key) || (backendKeys[key]?.set ?? false);
  const source = (key: string): string => {
    if (isLocalKeySet(key)) return "browser";
    if (backendKeys[key]?.source === "env") return "env";
    if (backendKeys[key]?.set) return "backend";
    return "";
  };

  const handleSave = async (key: string) => {
    const val = drafts[key]?.trim() ?? "";
    if (!val) return;
    // 1. Store in localStorage immediately (masked after save)
    setLocalKey(key, val);
    // 2. Also sync to backend so terminal scripts can use it
    try {
      setSaving(true);
      await updateSettings({ [key]: val });
    } catch { /* backend optional */ }
    finally { setSaving(false); }
    setDrafts((d) => { const n = { ...d }; delete n[key]; return n; });
    setSavedMsg((m) => ({ ...m, [key]: "Saved" }));
    setTimeout(() => setSavedMsg((m) => { const n = { ...m }; delete n[key]; return n; }), 2500);
    await load();
  };

  const handleClear = async (key: string) => {
    if (!window.confirm(`Clear ${ALL_KEY_LABELS[key]?.label ?? key}?`)) return;
    clearLocalKey(key);
    try { await updateSettings({ [key]: "" }); } catch { /* optional */ }
    setDrafts((d) => { const n = { ...d }; delete n[key]; return n; });
    setVerifyResult((r) => { const n = { ...r }; delete n[key]; return n; });
    await load();
  };

  const handleVerify = async (key: string) => {
    setVerifying((v) => ({ ...v, [key]: true }));
    setVerifyResult((r) => { const n = { ...r }; delete n[key]; return n; });
    // If there's an unsaved draft, verify that value directly so user gets
    // instant feedback before committing. Otherwise use the stored backend key.
    const draft = drafts[key]?.trim();
    // Also check localStorage in case it was saved client-side only
    const localVal = getLocalKeys()[key];
    try {
      const result = await verifyKey(key, draft || localVal || undefined);
      setVerifyResult((r) => ({ ...r, [key]: result }));
    } catch (e: unknown) {
      setVerifyResult((r) => ({
        ...r,
        [key]: { valid: false, provider: "", message: e instanceof Error ? e.message : "Request failed" },
      }));
    } finally {
      setVerifying((v) => ({ ...v, [key]: false }));
    }
  };


  // Render a key-input group (reused for AI and Discovery tabs)
  const renderKeyGroup = (keyLabels: Record<string, KeyMeta>) =>
    Object.entries(keyLabels).map(([key, { label, hint, priority, verifiable }]) => {
          const keyIsSet = isSet(key);
          const keySrc = source(key);
          const envOnly = keySrc === "env";
          const draft = drafts[key] ?? "";
          const msg = savedMsg[key];
          const canVerify = verifiable ?? false;

          return (
            <div key={key} style={{
              ...fieldGroupStyle,
              borderLeft: priority ? "3px solid #2563eb" : undefined,
              paddingLeft: priority ? 12 : undefined,
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 4 }}>
                <label style={labelStyle}>
                  {label}
                  {priority && <span style={{ fontSize: 10, color: "#2563eb", marginLeft: 6, fontWeight: 700 }}>REQUIRED</span>}
                </label>
                <span style={{
                  fontSize: 11, padding: "1px 8px", borderRadius: 10, fontWeight: 600,
                  background: keyIsSet ? "#dcfce7" : "#f3f4f6",
                  color: keyIsSet ? "#166534" : "#6b7280",
                }}>
                  {keyIsSet ? `Set (${keySrc})` : "Not set"}
                </span>
              </div>
              <p style={{ ...hintTextStyle, marginBottom: 8 }}>{hint}</p>

              {envOnly && (
                <p style={{ ...hintTextStyle, color: "#d97706", marginBottom: 6 }}>Currently set via environment variable. Paste a new key below to override it.</p>
              )}
              <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                <input
                  type="password"
                  placeholder={keyIsSet ? "●●●●●●●●  (paste new key to replace)" : "Paste API key here…"}
                  value={draft}
                  onChange={(e) => setDrafts((d) => ({ ...d, [key]: e.target.value }))}
                  onKeyDown={(e) => { if (e.key === "Enter" && draft) handleSave(key); }}
                  style={{ ...inputStyle, flex: 1, fontFamily: "monospace" }}
                  autoComplete="off"
                  spellCheck={false}
                />
                <button
                  onClick={() => handleSave(key)}
                  disabled={saving || !draft}
                  style={{ ...btnStyle, padding: "6px 14px", opacity: draft ? 1 : 0.4 }}
                >
                  {saving ? "…" : "Save"}
                </button>
                {canVerify && (
                  <button
                    onClick={() => handleVerify(key)}
                    disabled={verifying[key] || (!keyIsSet && !draft)}
                    title={(keyIsSet || draft) ? "Test this key against the provider API" : "Save a key first"}
                    style={{
                      ...btnStyle,
                      padding: "6px 14px",
                      background: "#6b7280",
                      opacity: (keyIsSet || draft) ? 1 : 0.4,
                    }}
                  >
                    {verifying[key] ? "Testing…" : "Verify"}
                  </button>
                )}
                {keyIsSet && (
                  <button onClick={() => handleClear(key)} style={{ ...iconBtnStyle, color: "#dc2626" }} title="Clear">
                    ✕
                  </button>
                )}
              </div>

              {/* Verification result */}
              {verifyResult[key] && (
                <div style={{
                  display: "flex", alignItems: "center", gap: 6, marginTop: 6,
                  padding: "7px 12px", borderRadius: 6, fontSize: 12,
                  background: verifyResult[key].valid ? "#f0fdf4" : "#fef2f2",
                  border: `1px solid ${verifyResult[key].valid ? "#86efac" : "#fca5a5"}`,
                  color: verifyResult[key].valid ? "#15803d" : "#b91c1c",
                }}>
                  <span style={{ fontSize: 14 }}>{verifyResult[key].valid ? "✓" : "✗"}</span>
                  <span><strong>{verifyResult[key].provider || ALL_KEY_LABELS[key]?.label}:</strong> {verifyResult[key].message}</span>
                </div>
              )}

              {msg && (
                <p style={{ ...hintTextStyle, color: "#16a34a", marginTop: 4, fontWeight: 600 }}>✓ {msg}</p>
              )}
            </div>
          );
    });

  return (
    <div style={{ maxWidth: 760 }}>
      <h2 style={{ marginTop: 0, marginBottom: 12 }}>Settings</h2>

      {/* ── Tab bar ───────────────────────────────────────────────────── */}
      <div style={{ display: "flex", gap: 2, borderBottom: "2px solid #e5e7eb", marginBottom: 20 }}>
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            style={{
              padding: "8px 16px", border: "none", cursor: "pointer",
              fontSize: 13, fontWeight: tab === t.id ? 700 : 500,
              color: tab === t.id ? "#2563eb" : "#6b7280",
              background: tab === t.id ? "#eff6ff" : "transparent",
              borderBottom: tab === t.id ? "2px solid #2563eb" : "2px solid transparent",
              borderRadius: "6px 6px 0 0",
              marginBottom: -2,  // overlap the container border
            }}>
            {t.icon} {t.label}
          </button>
        ))}
      </div>

      {error && (
        <div style={{ ...alertStyle, background: "#fef2f2", borderColor: "#fca5a5", color: "#991b1b" }}>
          {error}
        </div>
      )}

      {/* ═════ TAB: AI ═════ */}
      {tab === "ai" && (
        <>
          <ProvidersPanel />
          <ModelAssignmentsPanel />

          <section style={sectionStyle}>
            <h3 style={sectionTitleStyle}>AI Behavior</h3>
            <p style={hintTextStyle}>
              Control how Glossa AI handles action proposals during chat.
            </p>
            <AutoApproveSetting />
          </section>
        </>
      )}

      {/* ═════ TAB: Discovery ═════ */}
      {tab === "discovery" && (
        <AutoDiscoveryPanel />
      )}

      {/* ═════ TAB: Notifications ═════ */}
      {tab === "notifications" && <NotificationsPanel />}

      {/* ═════ TAB: System ═════ */}
      {tab === "system" && (
        <>
          <PythonEnvSection />

          <section style={sectionStyle}>
            <h3 style={sectionTitleStyle}>System</h3>
            <table style={{ borderCollapse: "collapse" }}>
              <tbody>
                <InfoRow label="Data directory" value={dataDir || "—"} mono />
                <InfoRow label="OCR pipeline" value="ocr_mahadevan.py (pixtral-12b)" />
                <InfoRow label="Corpus" value="Mahadevan (1977) — Internet Archive" />
                <InfoRow label="Sign mapping" value="Fuls (2023) Chapter 2.4 — 386 entries" />
              </tbody>
            </table>
          </section>

          <section style={sectionStyle}>
            <h3 style={sectionTitleStyle}>OCR Quick Start</h3>
            <p style={hintTextStyle}>
              After setting your Mistral key, run OCR from the Experiments tab or from the terminal:
            </p>
            <pre style={codeStyle}>
{`# Bigram + frequency tables (29 pages, fastest)
python ocr_mahadevan.py --target tables

# All inscription sequences (124 pages)
python ocr_mahadevan.py --target texts`}
            </pre>
          </section>

          <section style={sectionStyle}>
            <h3 style={sectionTitleStyle}>About Glossa Lab</h3>
            <p style={hintTextStyle}>
              17 analysis pipelines for ancient script analysis. Real Indus data extracted
              from Fuls (2023) <em>A Catalog of Indus Signs</em>: 713 signs, 17,990 token occurrences.
            </p>
          </section>
        </>
      )}
    </div>
  );
}

// ── Auto-approve setting ─────────────────────────────────────────────────────────

const AUTO_APPROVE_KEY = "glossa_auto_approve";

function AutoApproveSetting() {
  const { toast } = useToast();
  const [enabled, setEnabled] = useState(() => localStorage.getItem(AUTO_APPROVE_KEY) === "true");

  const toggle = (v: boolean) => {
    setEnabled(v);
    localStorage.setItem(AUTO_APPROVE_KEY, v ? "true" : "false");
    // Notify any open AIChatWindow instances
    window.dispatchEvent(new CustomEvent("glossa:auto_approve_changed"));
    toast(v ? "Auto-approve enabled — Glossa AI will run all actions automatically" : "Auto-approve disabled", v ? "success" : "info");
  };

  return (
    <div style={{ marginTop: 12 }}>
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "12px 14px", borderRadius: 7,
        border: `1px solid ${enabled ? "#fbbf24" : "#e5e7eb"}`,
        background: enabled ? "#fffbeb" : "#fafafa",
      }}>
        <div>
          <div style={{ fontSize: 13, fontWeight: 600, color: enabled ? "#92400e" : "#374151", display: "flex", alignItems: "center", gap: 6 }}>
            <span style={{ fontSize: 15 }}>{enabled ? "⚡" : "✋"}</span>
            Auto Approve All AI Actions
            {enabled && (
              <span style={{ fontSize: 9, padding: "1px 6px", borderRadius: 8, background: "#f59e0b", color: "#78350f", fontWeight: 700 }}>ACTIVE</span>
            )}
          </div>
          <p style={{ ...hintTextStyle, marginTop: 3 }}>
            {enabled
              ? "Glossa AI will execute all proposed actions automatically without asking for approval. Click to disable."
              : "Glossa AI will ask for approval before executing actions. Toggle on to run all actions automatically."}
          </p>
        </div>
        {/* Toggle switch */}
        <div
          onClick={() => toggle(!enabled)}
          title={enabled ? "Click to disable auto-approve" : "Click to enable auto-approve"}
          style={{
            width: 44, height: 24, borderRadius: 12, cursor: "pointer", flexShrink: 0,
            background: enabled ? "#f59e0b" : "#d1d5db",
            position: "relative", transition: "background 0.2s",
          }}
        >
          <div style={{
            position: "absolute", top: 3, left: enabled ? 23 : 3,
            width: 18, height: 18, borderRadius: "50%",
            background: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.25)",
            transition: "left 0.2s",
          }} />
        </div>
      </div>
      <p style={{ ...hintTextStyle, marginTop: 6, color: "#9ca3af" }}>
        You can also toggle auto-approve per-session from the <strong>⚡ AUTO</strong> badge
        in the Glossa AI chat header, or via the <strong>▾</strong> dropdown on any Approve button.
      </p>
    </div>
  );
}

function InfoRow({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <tr>
      <td style={{ padding: "3px 16px 3px 0", fontSize: 13, color: "#6b7280", whiteSpace: "nowrap" }}>{label}</td>
      <td style={{ padding: "3px 0", fontSize: 13, fontFamily: mono ? "monospace" : undefined }}>{value}</td>
    </tr>
  );
}

const sectionStyle: React.CSSProperties = {
  marginBottom: "2rem",
  padding: "1.25rem",
  border: "1px solid #e5e7eb",
  borderRadius: 8,
};

const sectionTitleStyle: React.CSSProperties = {
  margin: "0 0 0.75rem 0",
  fontSize: 15,
  fontWeight: 600,
  color: "#111827",
};

const fieldGroupStyle: React.CSSProperties = {
  marginBottom: "1.25rem",
  paddingBottom: "1.25rem",
  borderBottom: "1px solid #f3f4f6",
};

const labelStyle: React.CSSProperties = {
  fontSize: 13,
  fontWeight: 600,
  color: "#374151",
};

const hintTextStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 12,
  color: "#6b7280",
  lineHeight: 1.5,
};

const inputStyle: React.CSSProperties = {
  padding: "6px 10px",
  border: "1px solid #d1d5db",
  borderRadius: 5,
  fontSize: 13,
  width: "100%",
  boxSizing: "border-box",
};

const iconBtnStyle: React.CSSProperties = {
  padding: "6px 10px",
  border: "1px solid #d1d5db",
  borderRadius: 5,
  background: "#fff",
  cursor: "pointer",
  fontSize: 14,
  flexShrink: 0,
};

const btnStyle: React.CSSProperties = {
  background: "#2563eb",
  color: "#fff",
  border: "none",
  borderRadius: 5,
  padding: "8px 20px",
  fontSize: 13,
  fontWeight: 600,
  cursor: "pointer",
};

const alertStyle: React.CSSProperties = {
  padding: "10px 14px",
  borderRadius: 6,
  border: "1px solid",
  marginBottom: "1rem",
  fontSize: 13,
};


const ollamaSection: React.CSSProperties = {
  marginBottom: "2rem",
  padding: "1.25rem",
  border: "1px solid #d1fae5",
  borderRadius: 8,
  background: "#fafffe",
};

const codeStyle: React.CSSProperties = {
  background: "#1e293b",
  color: "#e2e8f0",
  padding: "12px 14px",
  borderRadius: 6,
  fontSize: 12,
  fontFamily: "monospace",
  margin: "8px 0 0",
  overflowX: "auto",
  lineHeight: 1.7,
};
