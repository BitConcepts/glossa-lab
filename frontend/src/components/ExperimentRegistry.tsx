import { useCallback, useEffect, useState } from "react";
import type { GraphExperimentMeta } from "../api";
import { listGraphExperiments } from "../api";

export default function ExperimentRegistry() {
  const [exps, setExps] = useState<GraphExperimentMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  const load = useCallback(async () => {
    try {
      const data = await listGraphExperiments();
      setExps(data);
    } catch { /* ignore */ }
    setLoading(false);
  }, []);

  useEffect(() => { void load(); }, [load]);

  const filtered = search.trim()
    ? exps.filter(e =>
        e.name.toLowerCase().includes(search.toLowerCase()) ||
        e.id.toLowerCase().includes(search.toLowerCase()) ||
        (e.description ?? "").toLowerCase().includes(search.toLowerCase())
      )
    : exps;

  return (
    <section style={{
      background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10,
      padding: "12px 16px", marginBottom: 14,
    }}>
      <div
        style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", userSelect: "none" }}
        onClick={() => setOpen(!open)}
      >
        <span style={{ fontSize: 16 }}>🧪</span>
        <strong style={{ fontSize: 14, color: "#111827" }}>
          Experiment Registry ({exps.length})
        </strong>
        <span style={{ fontSize: 11, color: "#6b7280" }}>{open ? "▾" : "▸"}</span>
      </div>

      {open && (
        <div style={{ marginTop: 10 }}>
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search experiments…"
            style={{
              width: "100%", boxSizing: "border-box", padding: "5px 9px",
              fontSize: 11, border: "1px solid #d1d5db", borderRadius: 5,
              marginBottom: 8, outline: "none",
            }}
          />
          {loading && <div style={{ fontSize: 12, color: "#6b7280" }}>Loading…</div>}
          {!loading && filtered.length === 0 && (
            <div style={{ fontSize: 12, color: "#9ca3af" }}>No experiments match.</div>
          )}
          <div style={{ display: "flex", flexDirection: "column", gap: 3, maxHeight: 320, overflowY: "auto" }}>
            {filtered.map(e => (
              <div key={e.id} title={e.description ?? ""}
                style={{
                  display: "flex", alignItems: "center", gap: 8,
                  padding: "4px 7px", borderRadius: 5, fontSize: 12,
                  border: "1px solid #f3f4f6", background: "#fafafa",
                }}>
                <span style={{ flex: 1, fontWeight: 500, color: "#374151",
                  overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {e.name}
                </span>
                <span style={{
                  fontSize: 10, color: "#9ca3af", flexShrink: 0,
                  overflow: "hidden", textOverflow: "ellipsis", maxWidth: 140,
                  whiteSpace: "nowrap",
                }}>
                  {e.id}
                </span>
                {e.node_count > 0 && (
                  <span style={{ fontSize: 9, color: "#9ca3af", flexShrink: 0 }}>
                    {e.node_count}n
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
