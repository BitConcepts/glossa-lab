import { useEffect, useRef, useState } from "react";
import {
  deleteOllamaModel,
  getEnvPackages,
  getEnvStatus,
  getLocalCtxLength, setLocalCtxLength,
  getOllamaLibrary,
  getOllamaPullUrl,
  getOllamaRecommendation,
  getOllamaStatus,
  getProviderCatalog,
  getSettings,
  getStatus,
  isLocalKeySet, clearLocalKey, getLocalKeys, setLocalKey,
  listOllamaInstalled,
  runEnvRebuild, runEnvSetup, runEnvUpgrade,
  setOllamaContextLength,
  updateSettings,
  verifyKey,
  type CatalogProvider, type EnvPackage, type EnvStatus, type KeyStatus, type ModelDetail,
  type OllamaInstalledModel, type OllamaLibraryEntry, type OllamaRecommendation,
  type VerifyKeyResult,
} from "../api";
import { useToast } from "../hooks/useToast";

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

// ── Context Length Panel ───────────────────────────────────────────────────

function ContextLengthPanel({ recommendation }: { recommendation: OllamaRecommendation }) {
  const { toast } = useToast();
  const [ctx, setCtx] = useState(getLocalCtxLength);
  const [saving, setSaving] = useState(false);

  const recommended = recommendation.recommended_ctx_length;
  const options = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072];

  const apply = async (val: number) => {
    setCtx(val);
    setLocalCtxLength(val);
    setSaving(true);
    try {
      await setOllamaContextLength(val);
      toast(`Context length set to ${val.toLocaleString()} tokens`, "success");
    } catch { toast("Failed to update session context length", "error"); }
    finally { setSaving(false); }
  };

  return (
    <div style={{ borderTop: "1px solid #bae6fd", paddingTop: 10, marginTop: 2 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
        <div>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#0284c7", textTransform: "uppercase", letterSpacing: 0.5 }}>Context Length</div>
          <div style={{ fontSize: 11, color: "#6b7280" }}>{recommendation.ctx_tier_note}</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 18, fontWeight: 800, color: "#0284c7", fontFamily: "monospace", lineHeight: 1 }}>
            {ctx.toLocaleString()}
          </div>
          <div style={{ fontSize: 10, color: "#9ca3af" }}>tokens</div>
        </div>
      </div>

      {/* Slider */}
      <input
        type="range"
        min={0} max={options.length - 1} step={1}
        value={options.indexOf(ctx) === -1 ? 3 : options.indexOf(ctx)}
        onChange={(e) => apply(options[parseInt(e.target.value)])}
        style={{ width: "100%", accentColor: "#0284c7", marginBottom: 6 }}
      />

      {/* Quick presets */}
      <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
        {options.map((o) => (
          <button
            key={o}
            onClick={() => apply(o)}
            title={o === recommended ? "Auto-detected recommendation for your GPU" : ""}
            style={{
              padding: "2px 7px", borderRadius: 4, border: "1px solid",
              cursor: "pointer", fontSize: 10, fontFamily: "monospace",
              background: ctx === o ? "#0284c7" : o === recommended ? "#e0f2fe" : "#fff",
              borderColor: ctx === o ? "#0284c7" : o === recommended ? "#7dd3fc" : "#d1d5db",
              color: ctx === o ? "#fff" : o === recommended ? "#0369a1" : "#374151",
              fontWeight: (ctx === o || o === recommended) ? 700 : 400,
            }}
          >
            {o >= 1024 ? `${o / 1024}K` : o}
            {o === recommended && " ★"}
          </button>
        ))}
      </div>
      <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 6 }}>
        ★ = auto-detected for your {recommendation.ctx_tier_label}
        {saving && <span style={{ marginLeft: 8, color: "#0284c7" }}>Saving…</span>}
      </div>
    </div>
  );
}

// ── Python Environment Section ─────────────────────────────────────────────────────────

function PythonEnvSection() {
  const { toast } = useToast();
  const [status, setStatus] = useState<EnvStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [output, setOutput] = useState<{ text: string; type: string }[]>([]);
  const [packages, setPackages] = useState<EnvPackage[] | null>(null);
  const outputRef = useRef<HTMLDivElement>(null);

  const refresh = async () => {
    setLoading(true);
    try { setStatus(await getEnvStatus()); } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  useEffect(() => { refresh(); }, []);
  useEffect(() => { outputRef.current?.scrollIntoView({ behavior: "auto" }); }, [output]);

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

  const loadPackages = async () => {
    const r = await getEnvPackages();
    setPackages(r.packages);
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
        <button onClick={loadPackages} disabled={!active}
          style={btnSt("#7c3aed", !active)}>
          📦 Show packages
        </button>
      </div>

      {/* Output stream */}
      {output.length > 0 && (
        <div style={{ background: "#0f172a", borderRadius: 5, padding: "8px 10px",
          maxHeight: 200, overflowY: "auto", fontFamily: "monospace", fontSize: 11, marginBottom: 10 }}>
          {output.map((l, i) => (
            <div key={i} style={{ color: l.type === "error" ? "#f87171" : l.type === "success" ? "#86efac" : "#e2e8f0", lineHeight: 1.6 }}>{l.text}</div>
          ))}
          <div ref={outputRef} />
        </div>
      )}

      {/* Package list */}
      {packages && (
        <div>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#374151", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>
            Installed packages ({packages.length})
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "2px 8px", maxHeight: 140, overflowY: "auto" }}>
            {packages.map(p => (
              <span key={p.name} style={{ fontSize: 10, fontFamily: "monospace", color: "#374151" }}>
                {p.name} <span style={{ color: "#9ca3af" }}>{p.version}</span>
              </span>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}

// ── Ollama Section ──────────────────────────────────────────────────────────────

function OllamaSection() {
  const { toast } = useToast();
  const [status, setStatus] = useState<{ running: boolean; message: string } | null>(null);
  const [ollamaInstalled, setOllamaInstalled] = useState<boolean | null>(null);
  const [installed, setInstalled] = useState<OllamaInstalledModel[]>([]);
  const [library, setLibrary] = useState<OllamaLibraryEntry[]>([]);
  const [recommendation, setRecommendation] = useState<OllamaRecommendation | null>(null);
  const [, setLoading] = useState(true);
  const [pulling, setPulling] = useState<Record<string, { progress: number; status: string; total: number; completed: number }>>({});
  const [pullCancelled, setPullCancelled] = useState<Set<string>>(new Set());
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [libFilter, setLibFilter] = useState<"all" | "compatible">("compatible");
  const [defaultModel, setDefaultModel] = useState<string | null>(null);
  const esRefs = useRef<Record<string, EventSource>>({})

  const refresh = async () => {
    setLoading(true);
    try {
      const [st, inst, lib, rec, settings, sysStatus] = await Promise.all([
        getOllamaStatus(), listOllamaInstalled(), getOllamaLibrary(),
        getOllamaRecommendation(), getSettings(), getStatus(),
      ]);
      setStatus(st);
      setOllamaInstalled(sysStatus.ollama_installed ?? null);
      setInstalled(inst.models ?? []);
      setLibrary(lib.models ?? []);
      setRecommendation(rec);
      // Load saved default model from provider prefs
      const prefs = (settings as unknown as Record<string, unknown>).providers as Record<string, unknown> ?? {};
      const ollamaPref = prefs.ollama as Record<string, unknown> | undefined;
      if (ollamaPref?.enabled && ollamaPref?.selected_model) {
        setDefaultModel(ollamaPref.selected_model as string);
      } else {
        setDefaultModel(null);
      }
    } catch { setStatus({ running: false, message: "Could not connect to backend" }); }
    finally { setLoading(false); }
  };

  const setAsDefault = async (modelName: string) => {
    try {
      await updateSettings({ providers: { ollama: { enabled: true, selected_model: modelName } } });
      setDefaultModel(modelName);
      toast(`${modelName} set as default AI model`, "success");
    } catch { toast("Failed to set default model", "error"); }
  };

  useEffect(() => { refresh(); return () => { Object.values(esRefs.current).forEach(es => es.close()); }; }, []);

  const startPull = (modelName: string) => {
    if (pulling[modelName]) return;
    const es = new EventSource(getOllamaPullUrl(modelName));
    esRefs.current[modelName] = es;
    setPulling(p => ({ ...p, [modelName]: { progress: 0, status: "Starting…", total: 0, completed: 0 } }));
    setPullCancelled(c => { const n = new Set(c); n.delete(modelName); return n; });

    es.onmessage = (ev) => {
      try {
        const d = JSON.parse(ev.data);
        const total = d.total ?? 0;
        const completed = d.completed ?? 0;
        const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
        setPulling(p => ({ ...p, [modelName]: { progress: pct, status: d.status ?? "Downloading…", total, completed } }));
        if (d.status === "success") {
          es.close(); delete esRefs.current[modelName];
          setPulling(p => { const n = { ...p }; delete n[modelName]; return n; });
          toast(`${modelName} downloaded`, "success");
          refresh();
        } else if (d.status === "error") {
          es.close(); delete esRefs.current[modelName];
          setPulling(p => { const n = { ...p }; delete n[modelName]; return n; });
          toast(`Download failed: ${d.error ?? "unknown error"}`, "error");
        }
      } catch { /* ignore */ }
    };
    es.onerror = () => {
      es.close(); delete esRefs.current[modelName];
      if (!pullCancelled.has(modelName)) {
        setPulling(p => { const n = { ...p }; delete n[modelName]; return n; });
        toast(`Connection lost during download of ${modelName}`, "error");
      }
    };
  };

  const cancelPull = (modelName: string) => {
    const es = esRefs.current[modelName];
    if (es) { es.close(); delete esRefs.current[modelName]; }
    setPullCancelled(c => new Set([...c, modelName]));
    setPulling(p => { const n = { ...p }; delete n[modelName]; return n; });
    toast(`Download cancelled`, "info");
  };

  const handleDelete = async (modelName: string) => {
    if (deleteConfirm !== modelName) { setDeleteConfirm(modelName); return; }
    setDeleteConfirm(null);
    try {
      await deleteOllamaModel(modelName);
      setInstalled(prev => prev.filter(m => m.name !== modelName));
      setLibrary(prev => prev.map(m => m.name === modelName ? { ...m, installed: false } : m));
      toast(`${modelName} deleted`, "info");
    } catch (e) { toast(e instanceof Error ? e.message : "Delete failed", "error"); }
  };

  const qualityColors: Record<string, string> = { good: "#6b7280", great: "#2563eb", excellent: "#7c3aed" };
  const familyColors: Record<string, string> = { mistral: "#f59e0b", llama: "#3b82f6", gemma: "#10b981", qwen: "#8b5cf6", deepseek: "#06b6d4", phi: "#ec4899" };

  const visibleLib = library.filter(m => {
    if (libFilter === "compatible") return recommendation && m.min_vram_gb <= (recommendation.vram_gb + 2);
    return true;
  });

  return (
    <section style={ollamaSection}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
        <div>
          <h3 style={{ margin: "0 0 2px", fontSize: 15, fontWeight: 600, color: "#111827" }}>🦙 Ollama — Local AI Models</h3>
          {status && (
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span style={{ width: 7, height: 7, borderRadius: "50%", background: status.running ? "#16a34a" : "#9ca3af", display: "inline-block" }} />
              <span style={{ fontSize: 12, color: status.running ? "#16a34a" : "#6b7280" }}>{status.message}</span>
            </div>
          )}
        </div>
        <button onClick={refresh} style={{ padding: "4px 10px", border: "1px solid #e5e7eb", borderRadius: 4, background: "#f9fafb", cursor: "pointer", fontSize: 12, color: "#6b7280" }}>⟳ Refresh</button>
      </div>

      {ollamaInstalled === false && (
        <div style={{ padding: "14px 16px", background: "#fff7ed", border: "1px solid #fed7aa", borderRadius: 8, marginBottom: 14 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
            <span style={{ fontSize: 20 }}>📦</span>
            <div>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#92400e" }}>Ollama not installed</div>
              <div style={{ fontSize: 11, color: "#b45309" }}>Install Ollama to run AI models locally, for free, with full privacy.</div>
            </div>
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <a href="https://ollama.com/download" target="_blank" rel="noopener noreferrer"
              style={{ display: "inline-block", padding: "6px 16px", background: "#ea580c", color: "#fff", borderRadius: 5, fontSize: 12, fontWeight: 700, textDecoration: "none" }}>
              ↓ Download Ollama
            </a>
            <button onClick={refresh}
              style={{ padding: "6px 14px", border: "1px solid #fed7aa", borderRadius: 5, background: "#fff", cursor: "pointer", fontSize: 12, color: "#92400e" }}>
              ⟳ I installed it — check again
            </button>
          </div>
          <div style={{ marginTop: 8, fontSize: 11, color: "#b45309" }}>
            After installing: Glossa Lab will start Ollama automatically on next launch.
            Currently on Windows? Run the Ollama installer, then click "check again" above.
          </div>
        </div>
      )}
      {ollamaInstalled === true && !status?.running && (
        <div style={{ padding: "10px 14px", background: "#fef3c7", border: "1px solid #fcd34d", borderRadius: 6, marginBottom: 12, fontSize: 12 }}>
          Ollama is installed but not responding at localhost:11434.
          <button onClick={refresh} style={{ marginLeft: 10, padding: "2px 10px", border: "1px solid #fcd34d", borderRadius: 4, background: "none", cursor: "pointer", fontSize: 11, color: "#92400e" }}>⟳ Retry</button>
        </div>
      )}

      <div style={{ padding: "8px 12px", background: "#fefce8", border: "1px solid #fde68a", borderRadius: 6, marginBottom: 14, fontSize: 11, display: "flex", gap: 8, alignItems: "flex-start" }}>
        <span style={{ flexShrink: 0, fontSize: 14 }}>⚠️</span>
        <span style={{ color: "#78350f", lineHeight: 1.5 }}>
          <strong>Shared model store:</strong> Ollama stores all models in a single system-wide location
          (<code>~/.ollama/models</code>). Models shown here are shared across all applications on this machine.
          Deleting a model removes it for all apps — not just Glossa Lab. Be careful before deleting.
        </span>
      </div>

      {/* GPU + Recommendation */}
      {recommendation && (
        <div style={{ padding: "12px 14px", background: "#f0f9ff", border: "1px solid #bae6fd", borderRadius: 8, marginBottom: 14 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#0284c7", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>GPU / Hardware</div>
          <p style={{ margin: "0 0 6px", fontSize: 13, color: "#374151" }}>{recommendation.tier_description}</p>
          <p style={{ margin: "0 0 8px", fontSize: 12, color: "#6b7280" }}>{recommendation.glossa_note}</p>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 10 }}>
            <span style={{ fontSize: 11, fontWeight: 700, color: "#0284c7" }}>Top pick:</span>
            <span style={{ fontSize: 11, padding: "2px 8px", background: "#7c3aed", color: "#fff", borderRadius: 4, fontWeight: 600 }}>{recommendation.recommended.display}</span>
            <span style={{ fontSize: 11, color: "#6b7280" }}>{recommendation.recommended.size_gb} GB · score {recommendation.recommended.glossa_score}/10</span>
          </div>
          {/* Context length config */}
          <ContextLengthPanel recommendation={recommendation} />
        </div>
      )}

      {/* Default model indicator */}
      {defaultModel && (
        <div style={{ padding: "8px 12px", background: "#f0fdf4", border: "1px solid #86efac",
          borderRadius: 6, marginBottom: 10, display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 12 }}>🤖</span>
          <span style={{ fontSize: 12, color: "#15803d" }}>
            <strong>Default AI:</strong> {defaultModel}
          </span>
          <button
            onClick={async () => {
              await updateSettings({ providers: { ollama: { enabled: false, selected_model: defaultModel } } });
              setDefaultModel(null);
              toast("Ollama disabled as default AI", "info");
            }}
            style={{ marginLeft: "auto", padding: "2px 8px", border: "1px solid #86efac",
              borderRadius: 4, background: "none", cursor: "pointer", fontSize: 10,
              color: "#15803d" }}
          >
            Clear default
          </button>
        </div>
      )}

      {/* Installed models — 2-row card matching library layout */}
      {installed.length > 0 && (
        <div style={{ marginBottom: 14 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#374151", textTransform: "uppercase",
            letterSpacing: 0.5, marginBottom: 6 }}>Installed ({installed.length})</div>
          {installed.map((m) => {
            const isDefault = m.name === defaultModel;
            const famColor = familyColors[m.family] ?? "#6b7280";
            // Try to find library entry for description
            const libEntry = library.find(l => l.name === m.name);
            return (
              <div key={m.name} style={{ border: `1px solid ${isDefault ? "#86efac" : "#e5e7eb"}`,
                borderRadius: 6, overflow: "hidden", marginBottom: 6,
                background: isDefault ? "#f0fdf4" : "#fafafa" }}>
                {/* Row 1: name + actions */}
                <div style={{ display: "flex", gap: 8, padding: "8px 12px", alignItems: "center" }}>
                  <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 4,
                    background: famColor + "20", color: famColor, fontWeight: 700,
                    flexShrink: 0 }}>{m.family}</span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: 600, fontSize: 13, lineHeight: 1.3 }}>{m.display || m.name}</div>
                    {libEntry?.desc && <div style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}>{libEntry.desc}</div>}
                    {!libEntry?.desc && <div style={{ fontSize: 11, color: "#9ca3af" }}>{m.name}</div>}
                  </div>
                  {/* Aligned metadata column */}
                  <div style={{ display: "flex", gap: 6, alignItems: "center", flexShrink: 0 }}>
                    <span style={{ fontSize: 11, color: "#6b7280", minWidth: 50, textAlign: "right" }}>{m.size_gb} GB</span>
                    {m.glossa_score != null && (
                      <span style={{ fontSize: 10, padding: "1px 5px", background: "#7c3aed20",
                        color: "#7c3aed", borderRadius: 4, minWidth: 42, textAlign: "center" }}>⭐ {m.glossa_score}/10</span>
                    )}
                    {isDefault
                      ? <span style={{ fontSize: 10, padding: "2px 7px", background: "#15803d",
                          color: "#fff", borderRadius: 4, fontWeight: 700, whiteSpace: "nowrap" }}>🤖 Default AI</span>
                      : <button onClick={() => setAsDefault(m.name)}
                          style={{ padding: "2px 8px", border: "1px solid #86efac", borderRadius: 4,
                            cursor: "pointer", fontSize: 10, fontWeight: 600,
                            background: "#f0fdf4", color: "#15803d", whiteSpace: "nowrap" }}>Set default</button>
                    }
                    <button onClick={() => handleDelete(m.name)}
                      style={{ padding: "2px 8px", border: "1px solid",
                        borderRadius: 4, cursor: "pointer", fontSize: 10, fontWeight: 600,
                        borderColor: deleteConfirm === m.name ? "#dc2626" : "#fca5a5",
                        background: deleteConfirm === m.name ? "#fef2f2" : "none",
                        color: "#dc2626", whiteSpace: "nowrap" }}>
                      {deleteConfirm === m.name ? "Confirm?" : "Delete"}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Library browser */}
      <div>
        <div style={{ display: "flex", gap: 6, marginBottom: 10, alignItems: "center" }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#374151", textTransform: "uppercase", letterSpacing: 0.5 }}>Model Library</div>
          {(["all", "compatible"] as const).map((f) => (
            <button key={f} onClick={() => setLibFilter(f)}
              style={{ padding: "2px 8px", borderRadius: 4, border: "1px solid", cursor: "pointer", fontSize: 11,
                background: libFilter === f ? "#1e3a5f" : "#fff",
                borderColor: libFilter === f ? "#1e3a5f" : "#d1d5db",
                color: libFilter === f ? "#fff" : "#374151" }}>
              {f === "compatible" ? "Compatible with my GPU" : "All models"}
            </button>
          ))}
          {recommendation && libFilter === "compatible" && (
            <span style={{ fontSize: 10, color: "#9ca3af", marginLeft: 2 }}>
              ({visibleLib.length} of {library.length} models)
            </span>
          )}
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {visibleLib.map((m) => {
            const isPulling = !!pulling[m.name];
            const pullState = pulling[m.name];
            const qualColor = qualityColors[m.quality] ?? "#6b7280";
            const famColor = familyColors[m.family] ?? "#6b7280";
            return (
              <div key={m.name} style={{ border: `1px solid ${m.installed ? "#bbf7d0" : "#e5e7eb"}`, borderRadius: 6, overflow: "hidden", background: m.installed ? "#f0fdf4" : "#fafafa" }}>
                <div style={{ display: "flex", gap: 8, padding: "8px 12px", alignItems: "center" }}>
                  <span style={{ fontSize: 10, padding: "1px 5px", borderRadius: 3, background: famColor + "20", color: famColor, fontWeight: 700, flexShrink: 0 }}>{m.family}</span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                      <span style={{ fontWeight: 600, fontSize: 13 }}>{m.display}</span>
                      {m.tags.includes("top-pick") && <span style={{ fontSize: 9, padding: "1px 5px", background: "#7c3aed", color: "#fff", borderRadius: 3, fontWeight: 700 }}>TOP PICK</span>}
                      {m.tags.includes("recommended") && <span style={{ fontSize: 9, padding: "1px 5px", background: "#2563eb", color: "#fff", borderRadius: 3, fontWeight: 700 }}>FOR GLOSSA</span>}
                    </div>
                    <div style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}>{m.desc}</div>
                  </div>
                  <div style={{ display: "flex", gap: 4, flexShrink: 0, alignItems: "center" }}>
                    <span style={{ fontSize: 10, color: "#9ca3af" }}>{m.size_gb} GB</span>
                    {m.min_vram_gb > 0 && <span style={{ fontSize: 10, color: "#9ca3af" }}>·</span>}
                    {m.min_vram_gb > 0 && <span style={{ fontSize: 10, color: "#9ca3af" }}>{m.min_vram_gb}+ GB VRAM</span>}
                    <span style={{ fontSize: 10, padding: "1px 5px", borderRadius: 3, background: qualColor + "20", color: qualColor, fontWeight: 700 }}>{m.quality}</span>
                    <span style={{ fontSize: 10, padding: "1px 5px", background: "#7c3aed10", color: "#7c3aed", borderRadius: 3 }}>⭐{m.glossa_score}</span>
                  </div>
                  {m.installed ? (
                    <span style={{ fontSize: 11, color: "#16a34a", fontWeight: 700, flexShrink: 0 }}>✓ Installed</span>
                  ) : isPulling ? (
                    <button onClick={() => cancelPull(m.name)}
                      style={{ padding: "3px 10px", border: "1px solid #fca5a5", borderRadius: 4, background: "#fef2f2", cursor: "pointer", fontSize: 11, color: "#dc2626", flexShrink: 0 }}>
                      Cancel
                    </button>
                  ) : (
                    <button onClick={() => startPull(m.name)} disabled={!status?.running}
                      style={{ padding: "3px 10px", border: "none", borderRadius: 4, background: status?.running ? "#2563eb" : "#e5e7eb", cursor: status?.running ? "pointer" : "not-allowed", fontSize: 11, color: status?.running ? "#fff" : "#9ca3af", flexShrink: 0, fontWeight: 600 }}>
                      ↓ Download
                    </button>
                  )}
                </div>
                {isPulling && (
                  <div style={{ padding: "6px 12px 10px", borderTop: "1px solid #e5e7eb", background: "#fff" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#6b7280", marginBottom: 4 }}>
                      <span>{pullState.status}</span>
                      <span>{pullState.progress}% · {(pullState.completed / 1_000_000).toFixed(0)} / {(pullState.total / 1_000_000).toFixed(0)} MB</span>
                    </div>
                    <div style={{ height: 4, background: "#f3f4f6", borderRadius: 2 }}>
                      <div style={{ height: "100%", width: `${pullState.progress}%`, background: "#2563eb", borderRadius: 2, transition: "width 0.3s" }} />
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

// ── Main SettingsView ─────────────────────────────────────────────────────────

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

      <PythonEnvSection />

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

      {/* Ollama */}
      <OllamaSection />

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

      {/* AI Behavior */}
      <section style={sectionStyle}>
        <h3 style={sectionTitleStyle}>AI Behavior</h3>
        <p style={hintTextStyle}>
          Control how Glossa AI handles action proposals during chat. These preferences
          persist across sessions.
        </p>

        {/* Auto-approve toggle */}
        <AutoApproveSetting />
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
