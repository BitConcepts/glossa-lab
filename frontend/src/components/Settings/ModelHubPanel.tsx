import { useEffect, useState } from "react";
import {
  getOllamaLibrary, getOllamaRecommendation, deleteOllamaModel,
  listModelScores, getSettings, updateSettings, syncModelIntelligence,
  type OllamaLibraryEntry, type OllamaRecommendation, type ModelScore,
} from "../../api";
import { useToast } from "../../hooks/useToast";

// Module-level pull tracking — survives component unmount/remount (page navigation).
const _activePulls: Map<string, { es: EventSource; pct: number; status: string }> = new Map();

/** VRAM filter tiers — matches common GPU sizes. "My GPU" is added dynamically. */
const VRAM_TIERS = [
  { label: "All", max: 999 },
  { label: "≤ 4 GB", max: 4 },
  { label: "≤ 8 GB", max: 8 },
  { label: "≤ 12 GB", max: 12 },
  { label: "≤ 16 GB", max: 16 },
  { label: "≤ 24 GB", max: 24 },
];

// Quality badge colours.
const Q_COLORS: Record<string, string> = {
  excellent: "#16a34a",
  great: "#2563eb",
  good: "#ca8a04",
};

export function ModelHubPanel() {
  const { toast } = useToast();
  const [library, setLibrary] = useState<(OllamaLibraryEntry & { installed: boolean })[]>([]);
  const [rec, setRec] = useState<OllamaRecommendation | null>(null);
  const [scores, setScores] = useState<ModelScore[]>([]);
  const [loading, setLoading] = useState(true);
  const [ollamaRunning, setOllamaRunning] = useState(false);
  const [filter, setFilter] = useState(-1);          // -1 = "My GPU" auto, 999 = all
  // Restore any in-progress pulls from the module-level map.
  const [pulling, setPulling] = useState<Record<string, { pct: number; status: string }>>(() => {
    const init: Record<string, { pct: number; status: string }> = {};
    for (const [k, v] of _activePulls) init[k] = { pct: v.pct, status: v.status };
    return init;
  });
  const [hfToken, setHfToken] = useState<{ set: boolean; editing: boolean; value: string }>({ set: false, editing: false, value: "" });

  const refresh = async () => {
    setLoading(true);
    try {
      const [lib, recData, sc] = await Promise.all([
        getOllamaLibrary(),
        getOllamaRecommendation().catch(() => null),
        listModelScores(),
      ]);
      setLibrary(lib.models as (OllamaLibraryEntry & { installed: boolean })[]);
      setOllamaRunning(lib.running);
      setRec(recData);
      setScores(sc.scores);
      // Check HF token status
      try {
        const s = await getSettings();
        setHfToken(h => ({ ...h, set: s.keys?.hf_api_token?.set ?? false }));
      } catch { /* */ }
      // Auto-select "My GPU" filter on first load if GPU detected
      if (recData && recData.vram_gb > 0 && filter === -1) {
        setFilter(-1); // keep as "My GPU"
      } else if (filter === -1) {
        setFilter(999); // no GPU → show all
      }
    } catch { /* */ }
    setLoading(false);
  };

  useEffect(() => { refresh(); }, []);

  // Find model intelligence score by name (fuzzy).
  const getScore = (name: string): ModelScore | undefined =>
    scores.find(s => s.model_name === name || name.includes(s.model_name) || s.model_name.includes(name));

  // ── Pull via SSE (persisted in module-level map) ────────────────
  const handlePull = (modelName: string) => {
    if (_activePulls.has(modelName)) return;
    const entry = { pct: 0, status: "connecting…" };
    const es = new EventSource(`/api/v1/ollama/pull/${encodeURIComponent(modelName)}`);
    _activePulls.set(modelName, { es, ...entry });
    setPulling(p => ({ ...p, [modelName]: entry }));
    es.onmessage = (ev) => {
      try {
        const d = JSON.parse(ev.data) as { status?: string; total?: number; completed?: number; error?: string };
        if (d.error) {
          toast(`Pull failed: ${d.error}`, "error");
          _activePulls.delete(modelName);
          setPulling(p => { const n = { ...p }; delete n[modelName]; return n; });
          es.close();
          return;
        }
        if (d.status === "success") {
          toast(`${modelName} downloaded`, "success");
          _activePulls.delete(modelName);
          setPulling(p => { const n = { ...p }; delete n[modelName]; return n; });
          es.close();
          refresh();
          return;
        }
        const pct = d.total && d.completed ? Math.round((d.completed / d.total) * 100) : 0;
        const st = d.status || "downloading…";
        const ap = _activePulls.get(modelName);
        if (ap) { ap.pct = pct; ap.status = st; }
        setPulling(p => ({ ...p, [modelName]: { pct, status: st } }));
      } catch { /* */ }
    };
    es.onerror = () => {
      _activePulls.delete(modelName);
      setPulling(p => { const n = { ...p }; delete n[modelName]; return n; });
      es.close();
    };
  };

  const handleSaveHfToken = async () => {
    try {
      await updateSettings({ hf_api_token: hfToken.value });
      setHfToken({ set: true, editing: false, value: "" });
      toast("HF token saved — click Sync Scores to fetch leaderboard data", "success");
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Save failed", "error");
    }
  };

  const handleSyncHf = async () => {
    try {
      const r = await syncModelIntelligence();
      toast(r.message, "success");
      refresh();
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Sync failed", "error");
    }
  };

  const handleDelete = async (name: string) => {
    if (!confirm(`Delete ${name}?`)) return;
    try {
      await deleteOllamaModel(name);
      toast(`${name} deleted`, "success");
      refresh();
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Delete failed", "error");
    }
  };

  // ── Filter + Sort ─────────────────────────────────────────────────
  // Always show ALL models. Supported ones sort first; unsupported are dimmed.
  const gpuVram = rec?.vram_gb ?? 0;
  const effectiveMax = filter === -1 ? gpuVram : filter;
  const isFiltering = filter !== 999 && !(filter === -1 && gpuVram === 0);

  const displayModels = library.slice().sort((a, b) => {
    if (isFiltering) {
      const aFits = a.min_vram_gb <= effectiveMax ? 0 : 1;
      const bFits = b.min_vram_gb <= effectiveMax ? 0 : 1;
      if (aFits !== bFits) return aFits - bFits;
    }
    return b.glossa_score - a.glossa_score || a.min_vram_gb - b.min_vram_gb;
  });

  const s = {
    section: { border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 16, background: "#fff" } as const,
  };

  return (
    <section style={s.section}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
        <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>🏪 Model Hub</h3>
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: ollamaRunning ? "#16a34a" : "#ef4444" }} />
          <span style={{ fontSize: 11, color: "#6b7280" }}>
            {ollamaRunning ? "Ollama running" : "Ollama offline"}
          </span>
        </div>
      </div>

      {/* HF token row */}
      <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 10, fontSize: 11 }}>
        <span style={{ color: "#6b7280" }}>HuggingFace token:</span>
        {hfToken.editing ? (
          <>
            <input value={hfToken.value} onChange={e => setHfToken(h => ({ ...h, value: e.target.value }))}
              placeholder="hf_..." type="password"
              style={{ flex: 1, maxWidth: 220, padding: "2px 6px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 11 }} />
            <button onClick={handleSaveHfToken} style={{ padding: "2px 8px", fontSize: 10, border: "none", borderRadius: 4, background: "#2563eb", color: "#fff", cursor: "pointer" }}>Save</button>
            <button onClick={() => setHfToken(h => ({ ...h, editing: false, value: "" }))} style={{ padding: "2px 8px", fontSize: 10, border: "1px solid #d1d5db", borderRadius: 4, background: "#fff", cursor: "pointer" }}>Cancel</button>
          </>
        ) : (
          <>
            <span style={{ color: hfToken.set ? "#16a34a" : "#9ca3af" }}>{hfToken.set ? "set ✓" : "not set"}</span>
            <button onClick={() => setHfToken(h => ({ ...h, editing: true }))} style={{ padding: "2px 8px", fontSize: 10, border: "1px solid #d1d5db", borderRadius: 4, background: "#fff", cursor: "pointer" }}>
              {hfToken.set ? "Change" : "Add"}
            </button>
            <button onClick={handleSyncHf} style={{ padding: "2px 8px", fontSize: 10, border: "1px solid #d1d5db", borderRadius: 4, background: "#fff", cursor: "pointer" }}>
              🔄 Sync from HF
            </button>
            {!hfToken.set && <span style={{ color: "#9ca3af", fontSize: 10 }}>Optional — free at huggingface.co/settings/tokens</span>}
          </>
        )}
      </div>

      {/* GPU tier bar */}
      {rec && rec.vram_gb > 0 && (
        <div style={{ background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 6, padding: "8px 12px", marginBottom: 10, fontSize: 11, color: "#166534" }}>
          🖥️ <strong>{rec.gpu_name}</strong> — {rec.vram_gb} GB VRAM · Recommended: <strong>{rec.recommended.display}</strong>
        </div>
      )}

      {/* VRAM filter tabs */}
      <div style={{ display: "flex", gap: 4, marginBottom: 12, flexWrap: "wrap" }}>
        {gpuVram > 0 && (
          <button onClick={() => setFilter(-1)}
            style={{
              padding: "3px 10px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer",
              background: filter === -1 ? "#16a34a" : "#fff", color: filter === -1 ? "#fff" : "#374151", fontWeight: filter === -1 ? 700 : 400,
            }}>
            🖥️ My GPU ({gpuVram} GB)
          </button>
        )}
        {VRAM_TIERS.map(t => (
          <button key={t.max} onClick={() => setFilter(t.max)}
            style={{
              padding: "3px 10px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer",
              background: filter === t.max ? "#2563eb" : "#fff", color: filter === t.max ? "#fff" : "#374151", fontWeight: filter === t.max ? 700 : 400,
            }}>
            {t.label}
          </button>
        ))}
        <span style={{ fontSize: 10, color: "#9ca3af", alignSelf: "center", marginLeft: 4 }}>
          {displayModels.length} model{displayModels.length !== 1 ? "s" : ""}
        </span>
      </div>

      {loading && <div style={{ color: "#9ca3af", fontSize: 12, padding: 16, textAlign: "center" }}>Loading…</div>}

      {!loading && !ollamaRunning && (
        <div style={{ textAlign: "center", padding: 20, color: "#9ca3af", fontSize: 12, background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 6 }}>
          Ollama is not running. Install from <a href="https://ollama.com" target="_blank" rel="noopener noreferrer">ollama.com</a> and start it to download models.
        </div>
      )}

      {/* Model list */}
      {!loading && displayModels.map(m => {
        const sc = getScore(m.name);
        const isPulling = pulling[m.name];
        const fitsFilter = !isFiltering || m.min_vram_gb <= effectiveMax;
        const dimmed = isFiltering && !fitsFilter;
        return (
          <div key={m.name} style={{
            display: "flex", gap: 10, alignItems: "flex-start", padding: "10px 0",
            borderBottom: "1px solid #f3f4f6",
            opacity: dimmed ? 0.45 : 1,
          }}>
            {/* Left: info */}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" }}>
                <span style={{ fontSize: 13, fontWeight: 700 }}>{m.display}</span>
                <span style={{ fontSize: 9, padding: "1px 5px", borderRadius: 8, background: Q_COLORS[m.quality] || "#6b7280", color: "#fff", fontWeight: 600 }}>
                  {m.quality}
                </span>
                {m.installed && (
                  <span style={{ fontSize: 9, padding: "1px 5px", borderRadius: 8, background: "#16a34a", color: "#fff", fontWeight: 600 }}>installed</span>
                )}
                {m.tags.includes("top-pick") && (
                  <span style={{ fontSize: 9, padding: "1px 5px", borderRadius: 8, background: "#f59e0b", color: "#78350f", fontWeight: 700 }}>⭐ TOP PICK</span>
                )}
                {m.tags.includes("moe") && (
                  <span style={{ fontSize: 9, padding: "1px 5px", borderRadius: 8, background: "#8b5cf6", color: "#fff", fontWeight: 600 }}>MoE</span>
                )}
                {dimmed && (
                  <span style={{ fontSize: 9, padding: "1px 5px", borderRadius: 8, background: "#ef4444", color: "#fff", fontWeight: 600 }}>needs ≥{m.min_vram_gb} GB</span>
                )}
              </div>
              <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>{m.desc}</div>
              <div style={{ display: "flex", gap: 10, marginTop: 3, fontSize: 10, color: "#9ca3af" }}>
                <span>{m.param_b}B params</span>
                <span>{m.size_gb} GB</span>
                <span>≥{m.min_vram_gb} GB VRAM</span>
                {sc && (
                  <>
                    <span title="Reasoning">🧠{sc.reasoning_score.toFixed(0)}</span>
                    <span title="Conversational">💬{sc.conversational_score.toFixed(0)}</span>
                    <span title="Long-form">📝{sc.longform_score.toFixed(0)}</span>
                  </>
                )}
              </div>
              {/* Pull progress bar */}
              {isPulling && (
                <div style={{ marginTop: 4 }}>
                  <div style={{ height: 4, background: "#e5e7eb", borderRadius: 2, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: `${isPulling.pct}%`, background: "#2563eb", transition: "width 0.3s" }} />
                  </div>
                  <div style={{ fontSize: 9, color: "#6b7280", marginTop: 1 }}>{isPulling.status} {isPulling.pct > 0 ? `${isPulling.pct}%` : ""}</div>
                </div>
              )}
            </div>
            {/* Right: actions */}
            <div style={{ display: "flex", gap: 4, flexShrink: 0, alignItems: "center" }}>
              {m.installed ? (
                <button onClick={() => handleDelete(m.name)}
                  style={{ padding: "3px 8px", fontSize: 10, border: "1px solid #fca5a5", borderRadius: 4, background: "#fff", color: "#dc2626", cursor: "pointer" }}>
                  🗑️ Delete
                </button>
              ) : (
                <button onClick={() => handlePull(m.name)} disabled={!ollamaRunning || !!isPulling}
                  style={{
                    padding: "3px 10px", fontSize: 10, border: "none", borderRadius: 4, cursor: ollamaRunning && !isPulling ? "pointer" : "not-allowed",
                    background: ollamaRunning && !isPulling ? "#2563eb" : "#e5e7eb", color: ollamaRunning && !isPulling ? "#fff" : "#9ca3af", fontWeight: 600,
                  }}>
                  {isPulling ? "Pulling…" : "⬇ Pull"}
                </button>
              )}
            </div>
          </div>
        );
      })}

      {/* Custom model pull */}
      {ollamaRunning && (
        <CustomPull onPull={handlePull} pulling={pulling} />
      )}
    </section>
  );
}

/** Small inline form to pull any model name not in the curated list. */
function CustomPull({ onPull, pulling }: { onPull: (n: string) => void; pulling: Record<string, unknown> }) {
  const [name, setName] = useState("");
  return (
    <div style={{ marginTop: 10, display: "flex", gap: 6, alignItems: "center" }}>
      <input value={name} onChange={e => setName(e.target.value)} placeholder="any-model:tag"
        style={{ flex: 1, fontSize: 11, padding: "4px 8px", border: "1px solid #d1d5db", borderRadius: 4 }}
        onKeyDown={e => { if (e.key === "Enter" && name.trim()) { onPull(name.trim()); setName(""); } }} />
      <button onClick={() => { if (name.trim()) { onPull(name.trim()); setName(""); } }}
        disabled={!name.trim() || !!pulling[name.trim()]}
        style={{ padding: "4px 10px", fontSize: 10, border: "none", borderRadius: 4, background: "#7c3aed", color: "#fff", cursor: "pointer", fontWeight: 600 }}>
        Pull custom
      </button>
    </div>
  );
}
