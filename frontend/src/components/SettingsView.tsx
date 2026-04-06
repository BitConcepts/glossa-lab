import { useEffect, useState } from "react";
import {
  getSettings, updateSettings,
  getProviderCatalog,
  setLocalKey, clearLocalKey, isLocalKeySet, getLocalKeys,
  verifyKey,
  type KeyStatus, type CatalogProvider, type ModelDetail, type VerifyKeyResult,
} from "../api";

const KEY_LABELS: Record<string, { label: string; hint: string; priority?: boolean }> = {
  mistral_api_key: {
    label: "Mistral API Key",
    hint: "Required for OCR via pixtral-12b. Get yours at console.mistral.ai",
    priority: true,
  },
  openai_api_key: {
    label: "OpenAI API Key",
    hint: "For GPT-4 vision, embeddings, and agentic tasks.",
  },
  anthropic_api_key: {
    label: "Anthropic API Key",
    hint: "For Claude vision and reasoning tasks.",
  },
  google_api_key: {
    label: "Google API Key",
    hint: "For Gemini vision and multimodal tasks.",
  },
};

export function SettingsView() {
  const [backendKeys, setBackendKeys] = useState<Record<string, KeyStatus>>({});
  const [dataDir, setDataDir] = useState("");
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState<Record<string, string>>({});
  const [error, setError] = useState("");
  const [verifying, setVerifying] = useState<Record<string, boolean>>({});
  const [verifyResult, setVerifyResult] = useState<Record<string, VerifyKeyResult>>({});
  const [providers, setProviders] = useState<CatalogProvider[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [providerPrefs, setProviderPrefs] = useState<Record<string, any>>({});

  const load = async () => {
    try {
      const s = await getSettings();
      setBackendKeys(s.keys);
      setDataDir(s.data_dir);
      setProviderPrefs((s as unknown as Record<string, unknown>).providers as Record<string, unknown> ?? {});
      setError("");
    } catch {
      // Backend might not be available; localStorage still works
    }
    getProviderCatalog().then(setProviders).catch(() => {});
  };

  useEffect(() => { load(); }, []);

  const handleProviderToggle = async (pid: string, enabled: boolean) => {
    const updated = { ...providerPrefs, [pid]: { ...(providerPrefs[pid] ?? {}), enabled } };
    setProviderPrefs(updated);
    try { await updateSettings({ providers: { [pid]: { ...(providerPrefs[pid] ?? {}), enabled } } }); } catch { /* optional */ }
  };

  const handleModelSelect = async (pid: string, model: string) => {
    const updated = { ...providerPrefs, [pid]: { ...(providerPrefs[pid] ?? {}), selected_model: model } };
    setProviderPrefs(updated);
    try { await updateSettings({ providers: { [pid]: { ...(providerPrefs[pid] ?? {}), selected_model: model } } }); } catch { /* optional */ }
  };

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
    if (!window.confirm(`Clear ${KEY_LABELS[key]?.label ?? key}?`)) return;
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


  return (
    <div style={{ maxWidth: 640 }}>
      <h2 style={{ marginTop: 0 }}>Settings</h2>

      {error && (
        <div style={{ ...alertStyle, background: "#fef2f2", borderColor: "#fca5a5", color: "#991b1b" }}>
          {error}
        </div>
      )}

      {/* AI API Keys */}
      <section style={sectionStyle}>
        <h3 style={sectionTitleStyle}>AI API Keys</h3>
        <p style={hintTextStyle}>
          Paste a key and click Save. The key is hidden immediately and stored in your browser.
          It is also synced to the backend so terminal scripts (OCR, experiments) can use it.
        </p>

        {Object.entries(KEY_LABELS).map(([key, { label, hint, priority }]) => {
          const keyIsSet = isSet(key);
          const keySrc = source(key);
          const envOnly = keySrc === "env";
          const draft = drafts[key] ?? "";
          const msg = savedMsg[key];

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
                  <span><strong>{verifyResult[key].provider || KEY_LABELS[key]?.label}:</strong> {verifyResult[key].message}</span>
                </div>
              )}

              {msg && (
                <p style={{ ...hintTextStyle, color: "#16a34a", marginTop: 4, fontWeight: 600 }}>✓ {msg}</p>
              )}
            </div>
          );
        })}
      </section>

      {/* Provider toggles */}
      {providers.length > 0 && (
        <section style={sectionStyle}>
          <h3 style={sectionTitleStyle}>Provider Enable / Model Selection</h3>
          <p style={hintTextStyle}>Enable providers and select the model to use for each. OCR-capable providers are highlighted.</p>
          <div style={{ display: "grid", gap: "0.75rem", marginTop: "0.75rem" }}>
            {providers.map((p) => {
              const pref = providerPrefs[p.id] ?? {};
              const enabled = pref.enabled ?? false;
              const selectedModel = pref.selected_model ?? p.recommended_models[0] ?? "";
              const keySet = backendKeys[p.api_key_setting]?.set || isLocalKeySet(p.api_key_setting);
              const details: ModelDetail[] = p.model_details ?? [];
              const selectedDetail = details.find((d) => d.id === selectedModel);
              return (
                <div key={p.id} style={{ border: "1px solid #e5e7eb", borderRadius: 8,
                  background: enabled ? "#f0fdf4" : "#fafafa", overflow: "hidden" }}>
                  {/* Header row */}
                  <div style={{ display: "flex", alignItems: "center", gap: 10,
                    padding: "10px 12px" }}>
                    <input type="checkbox" checked={enabled}
                      onChange={(e) => handleProviderToggle(p.id, e.target.checked)}
                      style={{ width: 16, height: 16, cursor: "pointer" }} />
                    <span style={{ fontWeight: 600, fontSize: 13, minWidth: 80 }}>{p.label}</span>
                    {p.ocr_preferred_models.length > 0 && (
                      <span style={{ fontSize: 10, color: "#7c3aed", background: "#ede9fe",
                        padding: "1px 6px", borderRadius: 8, fontWeight: 600 }}>OCR</span>
                    )}
                    {!keySet && (
                      <span style={{ fontSize: 10, color: "#d97706", background: "#fef3c7",
                        padding: "1px 6px", borderRadius: 8 }}>No key</span>
                    )}
                    <select
                      value={selectedModel}
                      onChange={(e) => handleModelSelect(p.id, e.target.value)}
                      disabled={!enabled}
                      style={{ marginLeft: "auto", fontSize: 12, padding: "3px 6px",
                        borderRadius: 4, border: "1px solid #d1d5db",
                        background: enabled ? "#fff" : "#f9fafb",
                        cursor: enabled ? "pointer" : "default",
                        minWidth: 260, maxWidth: 480 }}
                    >
                      {details.length > 0
                        ? details.map((d) => (
                            <option key={d.id} value={d.id}>
                              {d.id}{d.use_for ? ` — ${d.use_for}` : ""}
                            </option>
                          ))
                        : p.recommended_models.map((m) => (
                            <option key={m} value={m}>{m}</option>
                          ))
                      }
                    </select>
                  </div>
                  {/* Model description */}
                  {enabled && selectedDetail && (
                    <div style={{ padding: "6px 12px 10px 38px",
                      borderTop: "1px solid #e5e7eb", background: "#f8fafc" }}>
                      <p style={{ margin: 0, fontSize: 11, color: "#374151",
                        lineHeight: 1.5 }}>{selectedDetail.description}</p>
                      {selectedDetail.use_for && (
                        <p style={{ margin: "4px 0 0", fontSize: 11, color: "#6b7280" }}>
                          <strong>Best for:</strong> {selectedDetail.use_for}
                        </p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* System info */}
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

      {/* OCR quick-start */}
      <section style={sectionStyle}>
        <h3 style={sectionTitleStyle}>OCR Quick Start</h3>
        <p style={hintTextStyle}>
          After setting your Mistral key, run OCR from the Experiments tab or directly from the terminal:
        </p>
        <pre style={codeStyle}>
{`# Bigram + frequency tables (29 pages, fastest)
python ocr_mahadevan.py --target tables

# All inscription sequences (124 pages)
python ocr_mahadevan.py --target texts`}
        </pre>
        <p style={{ ...hintTextStyle, marginTop: 6 }}>
          Results auto-convert from Mahadevan → Fuls sign numbering and save to <code>reports/</code>.
        </p>
      </section>

      {/* About */}
      <section style={sectionStyle}>
        <h3 style={sectionTitleStyle}>About Glossa Lab</h3>
        <p style={hintTextStyle}>
          17 analysis pipelines for ancient script analysis. Real Indus data extracted
          from Fuls (2023) <em>A Catalog of Indus Signs</em>: 713 signs, 17,990 token occurrences.
          Collaboration target: ICIT access from Dr. Andreas Fuls (TU Berlin).
        </p>
      </section>
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
