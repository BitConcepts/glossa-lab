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

  // Add form state
  const [addType, setAddType] = useState<ProviderType>("cloud");
  const [addCloudId, setAddCloudId] = useState("");
  const [addName, setAddName] = useState("");
  const [addUrl, setAddUrl] = useState("");
  const [addKey, setAddKey] = useState("");
  const [addSaving, setAddSaving] = useState(false);

  const refresh = async () => {
    setLoading(true);
    try {
      const r = await listProviders();
      setProviders(r.providers);
    } catch { /* */ }
    finally { setLoading(false); }
  };

  useEffect(() => {
    refresh();
    listCloudProviders().then(r => setCloudCatalog(r.providers)).catch(() => {});
  }, []);

  const handleTest = async (id: string) => {
    setTesting(t => ({ ...t, [id]: true }));
    try {
      const r = await testProvider(id);
      toast(r.message, r.valid ? "success" : "error");
      await refresh();
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Test failed", "error");
    }
    setTesting(t => ({ ...t, [id]: false }));
  };

  const handleDelete = async (id: string, name: string) => {
    if (!window.confirm(`Delete provider "${name}"?`)) return;
    try {
      await deleteProvider(id);
      toast(`${name} deleted`, "success");
      await refresh();
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Delete failed", "error");
    }
  };

  const handleToggle = async (id: string, enabled: boolean) => {
    try {
      await updateProvider(id, { enabled: enabled ? 1 : 0 } as never);
      await refresh();
    } catch { /* */ }
  };

  const handleAdd = async () => {
    if (!addName.trim()) { toast("Name is required", "error"); return; }
    setAddSaving(true);
    try {
      const cp = cloudCatalog.find(c => c.id === addCloudId);
      await createProvider({
        name: addName,
        provider_type: addType,
        provider_id: addType === "cloud" ? addCloudId : addType,
        base_url: addUrl || (cp?.base_url ?? ""),
        api_key: addKey,
      });
      toast(`${addName} added`, "success");
      setShowAdd(false);
      setAddName(""); setAddUrl(""); setAddKey(""); setAddCloudId("");
      await refresh();
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Add failed", "error");
    }
    setAddSaving(false);
  };

  const handleDetectOllama = async () => {
    toast("Scanning for Ollama...", "info");
    try {
      const r = await detectOllama();
      if (r.detected.length === 0) {
        toast("No Ollama instances found on LAN", "error");
        return;
      }
      const first = r.detected[0];
      setAddType("ollama");
      setAddName("Ollama (local)");
      setAddUrl(first.url);
      setShowAdd(true);
      toast(`Found Ollama at ${first.url} with ${first.models.length} model(s)`, "success");
    } catch { toast("Detection failed", "error"); }
  };

  const s = { section: { border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 16, background: "#fff" } as const };

  return (
    <section style={s.section}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>🔗 Provider Registry</h3>
        <div style={{ display: "flex", gap: 6 }}>
          <button onClick={handleDetectOllama} style={{ padding: "4px 10px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer", background: "#fff" }}>
            🦙 Detect Ollama
          </button>
          <button onClick={() => setShowAdd(true)} style={{ padding: "4px 10px", fontSize: 11, border: "none", borderRadius: 4, cursor: "pointer", background: "#2563eb", color: "#fff", fontWeight: 600 }}>
            + Add Provider
          </button>
        </div>
      </div>

      {loading && <div style={{ color: "#9ca3af", fontSize: 12 }}>Loading...</div>}

      {/* Provider list */}
      <div style={{ display: "grid", gap: 8 }}>
        {providers.map(p => (
          <div key={p.id} style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 12px", border: "1px solid #e5e7eb", borderRadius: 6, background: p.enabled ? "#f0fdf4" : "#fafafa" }}>
            <span style={{ fontSize: 16 }}>{TYPE_ICONS[p.provider_type] || "🔗"}</span>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                <span style={{ fontWeight: 600, fontSize: 13 }}>{p.name}</span>
                <span style={{ fontSize: 10, padding: "1px 5px", borderRadius: 3, background: `${STATUS_COLORS[p.status] || "#9ca3af"}20`, color: STATUS_COLORS[p.status] || "#9ca3af", fontWeight: 700 }}>
                  {p.status}
                </span>
                {p.available_models.length > 0 && (
                  <span style={{ fontSize: 10, color: "#6b7280" }}>{p.available_models.length} model(s)</span>
                )}
              </div>
              <div style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}>
                {p.provider_type}{p.provider_id && p.provider_id !== p.provider_type ? ` · ${p.provider_id}` : ""}
                {p.base_url && <span> · {p.base_url.replace(/https?:\/\//, "").slice(0, 40)}</span>}
              </div>
            </div>
            <input type="checkbox" checked={!!p.enabled} onChange={e => handleToggle(p.id, e.target.checked)} style={{ width: 14, height: 14, cursor: "pointer" }} />
            <button onClick={() => handleTest(p.id)} disabled={testing[p.id]} style={{ padding: "3px 8px", fontSize: 10, border: "1px solid #d1d5db", borderRadius: 3, cursor: "pointer", background: "#fff" }}>
              {testing[p.id] ? "..." : "Test"}
            </button>
            <button onClick={() => handleDelete(p.id, p.name)} style={{ padding: "3px 8px", fontSize: 10, border: "1px solid #fca5a5", borderRadius: 3, cursor: "pointer", background: "#fef2f2", color: "#dc2626" }}>
              ×
            </button>
          </div>
        ))}
        {!loading && providers.length === 0 && (
          <div style={{ textAlign: "center", padding: 20, color: "#9ca3af", fontSize: 12 }}>
            No providers configured. Click "Add Provider" to get started.
          </div>
        )}
      </div>

      {/* Add modal */}
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
                <select value={addCloudId} onChange={e => {
                  const id = e.target.value;
                  setAddCloudId(id);
                  const cp = cloudCatalog.find(c => c.id === id);
                  if (cp) { setAddName(cp.label); setAddUrl(cp.base_url); }
                }} style={{ width: "100%", padding: "6px 8px", borderRadius: 4, border: "1px solid #d1d5db", marginBottom: 10, fontSize: 13 }}>
                  <option value="">Select...</option>
                  {cloudCatalog.map(c => <option key={c.id} value={c.id}>{c.label}</option>)}
                </select>
              </>
            )}

            <label style={{ fontSize: 11, fontWeight: 600, display: "block", marginBottom: 4 }}>Name</label>
            <input value={addName} onChange={e => setAddName(e.target.value)} placeholder="My vLLM server"
              style={{ width: "100%", padding: "6px 8px", borderRadius: 4, border: "1px solid #d1d5db", marginBottom: 10, fontSize: 13 }} />

            <label style={{ fontSize: 11, fontWeight: 600, display: "block", marginBottom: 4 }}>Base URL</label>
            <input value={addUrl} onChange={e => setAddUrl(e.target.value)}
              placeholder={addType === "ollama" ? "http://localhost:11434" : "http://layer1labs:8000/v1"}
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
