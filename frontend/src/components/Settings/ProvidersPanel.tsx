import { useEffect, useState } from "react";
import {
  listProviders, createProvider, updateProvider, deleteProvider, testProvider,
  listCloudProviders, detectOllama,
  type ProviderEntry, type ProviderType, type CloudProviderInfo,
} from "../../api";
import { useToast } from "../../hooks/useToast";

const TYPE_ICONS: Record<string, string> = { cloud: "☁️", ollama: "🦙", byoe: "🔌", huggingface: "🤗" };
const STATUS_COLORS: Record<string, string> = { reachable: "#16a34a", unreachable: "#dc2626", untested: "#9ca3af" };

export function ProvidersPanel() {
  const { toast } = useToast();
  const [providers, setProviders] = useState<ProviderEntry[]>([]);
  const [cloudCatalog, setCloudCatalog] = useState<CloudProviderInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [testing, setTesting] = useState<Record<string, boolean>>({});
  const [showAdd, setShowAdd] = useState(false);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [editDraft, setEditDraft] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState<Record<string, boolean>>({});

  const [addType, setAddType] = useState<ProviderType>("cloud");
  const [addCloudId, setAddCloudId] = useState("");
  const [addName, setAddName] = useState("");
  const [addUrl, setAddUrl] = useState("");
  const [addKey, setAddKey] = useState("");
  const [addSaving, setAddSaving] = useState(false);

  const refresh = async () => {
    setLoading(true);
    try { const r = await listProviders(); setProviders(r.providers); } catch { /* */ }
    finally { setLoading(false); }
  };

  useEffect(() => {
    refresh();
    listCloudProviders().then(r => setCloudCatalog(r.providers)).catch(() => {});
  }, []);

  const handleTest = async (id: string) => {
    setTesting(t => ({ ...t, [id]: true }));
    try { const r = await testProvider(id); toast(r.message, r.valid ? "success" : "error"); await refresh(); }
    catch (e: unknown) { toast(e instanceof Error ? e.message : "Test failed", "error"); }
    setTesting(t => ({ ...t, [id]: false }));
  };

  const handleDelete = async (id: string, name: string) => {
    if (!window.confirm(`Delete provider "${name}"?`)) return;
    try { await deleteProvider(id); toast(`${name} deleted`, "success"); setExpanded(null); await refresh(); }
    catch (e: unknown) { toast(e instanceof Error ? e.message : "Delete failed", "error"); }
  };

  const handleToggle = async (id: string, enabled: boolean) => {
    try { await updateProvider(id, { enabled: enabled ? 1 : 0 } as never); await refresh(); } catch { /* */ }
  };

  const handleSaveField = async (id: string, field: string, value: string) => {
    setSaving(s => ({ ...s, [`${id}_${field}`]: true }));
    try {
      await updateProvider(id, { [field]: value } as never);
      toast(`${field} updated`, "success");
      setEditDraft(d => { const n = { ...d }; delete n[`${id}_${field}`]; return n; });
      await refresh();
    } catch (e: unknown) { toast(e instanceof Error ? e.message : "Save failed", "error"); }
    setSaving(s => ({ ...s, [`${id}_${field}`]: false }));
  };

  const handleAdd = async () => {
    if (!addName.trim()) { toast("Name is required", "error"); return; }
    setAddSaving(true);
    try {
      const cp = cloudCatalog.find(c => c.id === addCloudId);
      await createProvider({ name: addName, provider_type: addType, provider_id: addType === "cloud" ? addCloudId : addType, base_url: addUrl || (cp?.base_url ?? ""), api_key: addKey });
      toast(`${addName} added`, "success");
      setShowAdd(false); setAddName(""); setAddUrl(""); setAddKey(""); setAddCloudId("");
      await refresh();
    } catch (e: unknown) { toast(e instanceof Error ? e.message : "Add failed", "error"); }
    setAddSaving(false);
  };

  const handleDetectOllama = async () => {
    toast("Scanning for Ollama...", "info");
    try {
      const r = await detectOllama();
      if (r.detected.length === 0) { toast("No Ollama instances found", "error"); return; }
      const first = r.detected[0];
      setAddType("ollama"); setAddName("Ollama (local)"); setAddUrl(first.url); setShowAdd(true);
      toast(`Found Ollama at ${first.url} with ${first.models.length} model(s)`, "success");
    } catch { toast("Detection failed", "error"); }
  };

  const renderEditField = (p: ProviderEntry, field: string, label: string, type = "text", placeholder = "") => {
    const dk = `${p.id}_${field}`;
    const draft = editDraft[dk] ?? "";
    const isSaving = saving[dk];
    const cur = field === "api_key" ? "" : (p as unknown as Record<string, string>)[field] || "";
    return (
      <div style={{ marginBottom: 8 }}>
        <label style={{ fontSize: 10, fontWeight: 600, color: "#6b7280", display: "block", marginBottom: 2 }}>{label}</label>
        <div style={{ display: "flex", gap: 4 }}>
          <input type={type} value={draft || (field === "api_key" ? "" : cur)}
            onChange={e => setEditDraft(d => ({ ...d, [dk]: e.target.value }))}
            placeholder={field === "api_key" ? (p.api_key_set ? "••••••••  (paste new to replace)" : "Paste API key...") : placeholder || cur}
            style={{ flex: 1, padding: "4px 8px", fontSize: 12, borderRadius: 4, border: "1px solid #d1d5db", fontFamily: type === "password" ? "monospace" : undefined }} />
          {draft && (
            <button onClick={() => handleSaveField(p.id, field, draft)} disabled={isSaving}
              style={{ padding: "4px 10px", fontSize: 11, border: "none", borderRadius: 4, background: "#2563eb", color: "#fff", cursor: "pointer", fontWeight: 600 }}>
              {isSaving ? "..." : "Save"}
            </button>
          )}
        </div>
      </div>
    );
  };

  const sec: React.CSSProperties = { border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 16, background: "#fff" };

  return (
    <section style={sec}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>🔗 Provider Registry</h3>
        <div style={{ display: "flex", gap: 6 }}>
          <button onClick={handleDetectOllama} style={{ padding: "4px 10px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer", background: "#fff" }}>🦙 Detect Ollama</button>
          <button onClick={() => setShowAdd(true)} style={{ padding: "4px 10px", fontSize: 11, border: "none", borderRadius: 4, cursor: "pointer", background: "#2563eb", color: "#fff", fontWeight: 600 }}>+ Add Provider</button>
        </div>
      </div>

      {loading && <div style={{ color: "#9ca3af", fontSize: 12 }}>Loading...</div>}

      <div style={{ display: "grid", gap: 8 }}>
        {providers.map(p => {
          const isExp = expanded === p.id;
          return (
            <div key={p.id} style={{ border: "1px solid #e5e7eb", borderRadius: 6, overflow: "hidden", background: p.enabled ? "#f0fdf4" : "#fafafa" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 12px", cursor: "pointer" }}
                onClick={() => setExpanded(isExp ? null : p.id)}>
                <span style={{ fontSize: 16 }}>{TYPE_ICONS[p.provider_type] || "🔗"}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                    <span style={{ fontWeight: 600, fontSize: 13 }}>{p.name}</span>
                    <span style={{ fontSize: 10, padding: "1px 5px", borderRadius: 3, background: `${STATUS_COLORS[p.status] || "#9ca3af"}20`, color: STATUS_COLORS[p.status] || "#9ca3af", fontWeight: 700 }}>{p.status}</span>
                    {p.api_key_set && <span style={{ fontSize: 9, padding: "1px 4px", borderRadius: 3, background: "#dcfce7", color: "#166534" }}>key set</span>}
                    {p.available_models.length > 0 && <span style={{ fontSize: 10, color: "#6b7280" }}>{p.available_models.length} model(s)</span>}
                  </div>
                  <div style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}>
                    {p.provider_type}{p.provider_id !== p.provider_type ? ` · ${p.provider_id}` : ""}
                    {p.base_url && <span> · {p.base_url.replace(/https?:\/\//, "").slice(0, 40)}</span>}
                  </div>
                </div>
                <input type="checkbox" checked={!!p.enabled} onChange={e => { e.stopPropagation(); handleToggle(p.id, e.target.checked); }} style={{ width: 14, height: 14, cursor: "pointer" }} />
                <button onClick={e => { e.stopPropagation(); handleTest(p.id); }} disabled={testing[p.id]}
                  style={{ padding: "3px 8px", fontSize: 10, border: "1px solid #d1d5db", borderRadius: 3, cursor: "pointer", background: "#fff" }}>
                  {testing[p.id] ? "..." : "Test"}
                </button>
                <span style={{ fontSize: 10, color: "#9ca3af", transform: isExp ? "rotate(90deg)" : "rotate(0deg)", transition: "transform 0.15s" }}>▶</span>
              </div>

              {isExp && (
                <div style={{ padding: "8px 12px 12px", borderTop: "1px solid #e5e7eb", background: "#f8fafc" }}>
                  {renderEditField(p, "name", "Name", "text", "Provider name")}
                  {renderEditField(p, "base_url", "Base URL", "text", "https://api.openai.com/v1")}
                  {renderEditField(p, "api_key", "API Key", "password", "sk-...")}
                  {p.available_models.length > 0 && (
                    <div style={{ marginBottom: 8 }}>
                      <label style={{ fontSize: 10, fontWeight: 600, color: "#6b7280", display: "block", marginBottom: 4 }}>Available Models</label>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                        {p.available_models.slice(0, 20).map(m => (
                          <span key={m} style={{ fontSize: 10, padding: "2px 6px", background: "#e0f2fe", color: "#0369a1", borderRadius: 3, fontFamily: "monospace" }}>{m}</span>
                        ))}
                        {p.available_models.length > 20 && <span style={{ fontSize: 10, color: "#9ca3af" }}>+{p.available_models.length - 20} more</span>}
                      </div>
                    </div>
                  )}
                  <div style={{ display: "flex", gap: 6, marginTop: 8 }}>
                    <button onClick={() => handleTest(p.id)} disabled={testing[p.id]}
                      style={{ padding: "4px 12px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer", background: "#fff" }}>
                      {testing[p.id] ? "Testing..." : "↻ Refresh Models"}
                    </button>
                    <button onClick={() => handleDelete(p.id, p.name)}
                      style={{ padding: "4px 12px", fontSize: 11, border: "1px solid #fca5a5", borderRadius: 4, cursor: "pointer", background: "#fef2f2", color: "#dc2626", marginLeft: "auto" }}>
                      Delete Provider
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
        {!loading && providers.length === 0 && (
          <div style={{ textAlign: "center", padding: 20, color: "#9ca3af", fontSize: 12 }}>No providers configured. Click "Add Provider" to get started.</div>
        )}
      </div>

      {showAdd && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.3)", zIndex: 1000, display: "flex", alignItems: "center", justifyContent: "center" }} onClick={() => setShowAdd(false)}>
          <div style={{ background: "#fff", borderRadius: 10, padding: 24, width: 440, maxHeight: "80vh", overflow: "auto" }} onClick={e => e.stopPropagation()}>
            <h4 style={{ margin: "0 0 12px" }}>Add Provider</h4>
            <label style={{ fontSize: 11, fontWeight: 600, display: "block", marginBottom: 4 }}>Type</label>
            <select value={addType} onChange={e => { setAddType(e.target.value as ProviderType); setAddCloudId(""); setAddUrl(""); }}
              style={{ width: "100%", padding: "6px 8px", borderRadius: 4, border: "1px solid #d1d5db", marginBottom: 10, fontSize: 13 }}>
              <option value="cloud">☁️ Cloud (OpenAI, Anthropic, Mistral, ...)</option>
              <option value="ollama">🦙 Ollama (local)</option>
              <option value="byoe">🔌 BYOE (vLLM, LM Studio, custom endpoint)</option>
              <option value="huggingface">🤗 HuggingFace Inference</option>
            </select>
            {addType === "cloud" && (
              <>
                <label style={{ fontSize: 11, fontWeight: 600, display: "block", marginBottom: 4 }}>Provider</label>
                <select value={addCloudId} onChange={e => { const id = e.target.value; setAddCloudId(id); const cp = cloudCatalog.find(c => c.id === id); if (cp) { setAddName(cp.label); setAddUrl(cp.base_url); } }}
                  style={{ width: "100%", padding: "6px 8px", borderRadius: 4, border: "1px solid #d1d5db", marginBottom: 10, fontSize: 13 }}>
                  <option value="">Select...</option>
                  {cloudCatalog.map(c => <option key={c.id} value={c.id}>{c.label}</option>)}
                </select>
              </>
            )}
            <label style={{ fontSize: 11, fontWeight: 600, display: "block", marginBottom: 4 }}>Name</label>
            <input value={addName} onChange={e => setAddName(e.target.value)} placeholder="My vLLM server"
              style={{ width: "100%", padding: "6px 8px", borderRadius: 4, border: "1px solid #d1d5db", marginBottom: 10, fontSize: 13 }} />
            <label style={{ fontSize: 11, fontWeight: 600, display: "block", marginBottom: 4 }}>Base URL</label>
            <input value={addUrl} onChange={e => setAddUrl(e.target.value)} placeholder={addType === "ollama" ? "http://localhost:11434" : "http://layer1labs:8000/v1"}
              style={{ width: "100%", padding: "6px 8px", borderRadius: 4, border: "1px solid #d1d5db", marginBottom: 10, fontSize: 13 }} />
            <label style={{ fontSize: 11, fontWeight: 600, display: "block", marginBottom: 4 }}>API Key (optional)</label>
            <input value={addKey} onChange={e => setAddKey(e.target.value)} type="password" placeholder="sk-..."
              style={{ width: "100%", padding: "6px 8px", borderRadius: 4, border: "1px solid #d1d5db", marginBottom: 16, fontSize: 13 }} />
            <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
              <button onClick={() => setShowAdd(false)} style={{ padding: "6px 14px", borderRadius: 4, border: "1px solid #d1d5db", cursor: "pointer", background: "#fff", fontSize: 12 }}>Cancel</button>
              <button onClick={handleAdd} disabled={addSaving} style={{ padding: "6px 14px", borderRadius: 4, border: "none", cursor: "pointer", background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600 }}>
                {addSaving ? "Saving..." : "Add Provider"}
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
