import { useEffect, useState } from "react";
import { getSettings, updateSettings, KeyStatus } from "../api";

const KEY_LABELS: Record<string, { label: string; hint: string }> = {
  mistral_api_key: {
    label: "Mistral API Key",
    hint: "Required for OCR of Mahadevan corpus (pixtral-12b). Get at console.mistral.ai",
  },
  openai_api_key: {
    label: "OpenAI API Key",
    hint: "Optional. For future GPT-4 vision tasks.",
  },
  anthropic_api_key: {
    label: "Anthropic API Key",
    hint: "Optional. For future Claude vision tasks.",
  },
};

export function SettingsView() {
  const [keys, setKeys] = useState<Record<string, KeyStatus>>({});
  const [dataDir, setDataDir] = useState("");
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [showKey, setShowKey] = useState<Record<string, boolean>>({});
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState("");
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const s = await getSettings();
      setKeys(s.keys);
      setDataDir(s.data_dir);
      setError("");
    } catch (e) {
      setError("Backend not reachable — start the backend service first.");
    }
  };

  useEffect(() => { load(); }, []);

  const handleSave = async () => {
    const payload: Record<string, string> = {};
    Object.entries(drafts).forEach(([k, v]) => {
      if (v !== undefined) payload[k] = v;
    });
    if (Object.keys(payload).length === 0) return;
    try {
      setSaving(true);
      await updateSettings(payload);
      setDrafts({});
      await load();
      setSavedMsg("Saved successfully");
      setTimeout(() => setSavedMsg(""), 3000);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleClear = async (key: string) => {
    if (!window.confirm(`Clear ${KEY_LABELS[key]?.label ?? key}?`)) return;
    try {
      await updateSettings({ [key]: "" });
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Clear failed");
    }
  };

  const hasDrafts = Object.values(drafts).some((v) => v !== undefined);

  return (
    <div style={{ maxWidth: 640 }}>
      <h2 style={{ marginTop: 0 }}>Settings</h2>

      {error && (
        <div style={{ ...alertStyle, background: "#fef2f2", borderColor: "#fca5a5", color: "#991b1b" }}>
          {error}
        </div>
      )}
      {savedMsg && (
        <div style={{ ...alertStyle, background: "#f0fdf4", borderColor: "#86efac", color: "#166534" }}>
          ✓ {savedMsg}
        </div>
      )}

      {/* AI API Keys */}
      <section style={sectionStyle}>
        <h3 style={sectionTitleStyle}>AI API Keys</h3>
        <p style={hintTextStyle}>
          Keys are stored securely in the backend data directory and never exposed
          in the UI. Environment variables take precedence over stored keys.
        </p>

        {Object.entries(KEY_LABELS).map(([key, { label, hint }]) => {
          const status = keys[key];
          const isSet = status?.set ?? false;
          const source = status?.source;
          const isDraft = drafts[key] !== undefined;
          const show = showKey[key] ?? false;

          return (
            <div key={key} style={fieldGroupStyle}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                <label style={labelStyle}>{label}</label>
                <span style={{
                  fontSize: 11,
                  padding: "1px 7px",
                  borderRadius: 10,
                  background: isSet ? "#dcfce7" : "#f3f4f6",
                  color: isSet ? "#166534" : "#6b7280",
                  fontWeight: 500,
                }}>
                  {isSet ? `Set (${source})` : "Not set"}
                </span>
              </div>
              <p style={{ ...hintTextStyle, marginTop: 2, marginBottom: 6 }}>{hint}</p>
              <div style={{ display: "flex", gap: 6 }}>
                <input
                  type={show ? "text" : "password"}
                  placeholder={isSet ? "••••••••  (enter new value to replace)" : "Paste API key here…"}
                  value={drafts[key] ?? ""}
                  onChange={(e) => setDrafts((d) => ({ ...d, [key]: e.target.value }))}
                  disabled={source === "env"}
                  style={{
                    ...inputStyle,
                    flex: 1,
                    fontFamily: "monospace",
                    opacity: source === "env" ? 0.6 : 1,
                  }}
                />
                <button
                  onClick={() => setShowKey((s) => ({ ...s, [key]: !s[key] }))}
                  style={iconBtnStyle}
                  title={show ? "Hide" : "Show"}
                >
                  {show ? "🙈" : "👁"}
                </button>
                {isSet && source !== "env" && (
                  <button onClick={() => handleClear(key)} style={{ ...iconBtnStyle, color: "#dc2626" }} title="Clear key">
                    ✕
                  </button>
                )}
              </div>
              {source === "env" && (
                <p style={{ ...hintTextStyle, color: "#d97706", marginTop: 4 }}>
                  Set via environment variable — cannot be overridden here.
                </p>
              )}
              {isDraft && (
                <p style={{ ...hintTextStyle, color: "#2563eb", marginTop: 4 }}>
                  Unsaved change — click Save below.
                </p>
              )}
            </div>
          );
        })}

        <button
          onClick={handleSave}
          disabled={saving || !hasDrafts}
          style={{
            ...btnStyle,
            marginTop: "0.75rem",
            opacity: hasDrafts ? 1 : 0.4,
          }}
        >
          {saving ? "Saving…" : "Save API Keys"}
        </button>
      </section>

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
