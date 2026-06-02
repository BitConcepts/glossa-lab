import { useCallback, useEffect, useState } from "react";
import type { ExperimentLedgerEntry } from "../api";
import { getExperimentMetadata } from "../api";

const CATEGORIES = [
  "structural_analysis", "lm_scoring", "sa_variant", "ctt",
  "contact_zone", "cross_language", "archaeological", "misc",
] as const;

const CATEGORY_LABELS: Record<string, string> = {
  structural_analysis: "Structural",
  lm_scoring: "LM Scoring",
  sa_variant: "SA Variant",
  ctt: "CTT",
  contact_zone: "Contact Zone",
  cross_language: "Cross-Language",
  archaeological: "Archaeological",
  misc: "Misc",
};

const STATUS_COLORS: Record<string, { bg: string; fg: string }> = {
  active:     { bg: "#dcfce7", fg: "#166534" },
  superseded: { bg: "#fef9c3", fg: "#854d0e" },
  legacy:     { bg: "#f3f4f6", fg: "#6b7280" },
  scaffold:   { bg: "#ede9fe", fg: "#6d28d9" },
};

export default function ExperimentRegistry() {
  const [entries, setEntries] = useState<ExperimentLedgerEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [activeFilter, setActiveFilter] = useState<string | null>(null);
  const [showAll, setShowAll] = useState(false);

  const load = useCallback(async () => {
    try {
      const data = await getExperimentMetadata();
      setEntries(data);
    } catch { /* ignore */ }
    setLoading(false);
  }, []);

  useEffect(() => { void load(); }, [load]);

  const filtered = entries.filter((e) => {
    if (activeFilter && e.category !== activeFilter) return false;
    if (!showAll && e.status !== "active") return false;
    return true;
  });

  const byCategory = new Map<string, ExperimentLedgerEntry[]>();
  for (const e of filtered) {
    const cat = e.category || "misc";
    if (!byCategory.has(cat)) byCategory.set(cat, []);
    byCategory.get(cat)!.push(e);
  }

  const totalActive = entries.filter((e) => e.status === "active").length;

  return (
    <section style={{
      background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10,
      padding: "12px 16px", marginBottom: 14,
    }}>
      <div
        style={{
          display: "flex", alignItems: "center", gap: 8, cursor: "pointer",
          userSelect: "none",
        }}
        onClick={() => setOpen(!open)}
      >
        <span style={{ fontSize: 16 }}>🧪</span>
        <strong style={{ fontSize: 14, color: "#111827" }}>
          Experiment Registry ({totalActive})
        </strong>
        <span style={{ fontSize: 11, color: "#6b7280" }}>
          {open ? "▾" : "▸"}
        </span>
      </div>

      {open && (
        <div style={{ marginTop: 10 }}>
          {/* Category filter chips */}
          <div style={{ display: "flex", gap: 4, flexWrap: "wrap", marginBottom: 8 }}>
            <button
              onClick={() => setActiveFilter(null)}
              style={{
                padding: "2px 8px", borderRadius: 10, border: "1px solid #d1d5db",
                fontSize: 11, cursor: "pointer",
                background: activeFilter === null ? "#2563eb" : "#fff",
                color: activeFilter === null ? "#fff" : "#374151",
              }}
            >
              All
            </button>
            {CATEGORIES.map((cat) => {
              const count = entries.filter(
                (e) => e.category === cat && (showAll || e.status === "active")
              ).length;
              if (count === 0) return null;
              return (
                <button
                  key={cat}
                  onClick={() => setActiveFilter(activeFilter === cat ? null : cat)}
                  style={{
                    padding: "2px 8px", borderRadius: 10, border: "1px solid #d1d5db",
                    fontSize: 11, cursor: "pointer",
                    background: activeFilter === cat ? "#2563eb" : "#fff",
                    color: activeFilter === cat ? "#fff" : "#374151",
                  }}
                >
                  {CATEGORY_LABELS[cat] || cat} ({count})
                </button>
              );
            })}
            <span style={{ flex: 1 }} />
            <label style={{ fontSize: 11, color: "#6b7280", display: "flex", alignItems: "center", gap: 4 }}>
              <input
                type="checkbox"
                checked={showAll}
                onChange={(e) => setShowAll(e.target.checked)}
              />
              Show legacy/superseded
            </label>
          </div>

          {loading && <div style={{ fontSize: 12, color: "#6b7280" }}>Loading…</div>}

          {!loading && filtered.length === 0 && (
            <div style={{ fontSize: 12, color: "#9ca3af" }}>No experiments match the filter.</div>
          )}

          {/* Experiments grouped by category */}
          {Array.from(byCategory.entries()).map(([cat, items]) => (
            <div key={cat} style={{ marginBottom: 10 }}>
              <div style={{
                fontSize: 11, fontWeight: 700, color: "#6b7280",
                textTransform: "uppercase", letterSpacing: "0.05em",
                marginBottom: 4, paddingBottom: 2, borderBottom: "1px solid #f3f4f6",
              }}>
                {CATEGORY_LABELS[cat] || cat} ({items.length})
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
                {items.slice(0, 20).map((e) => {
                  const sc = STATUS_COLORS[e.status] || STATUS_COLORS.active;
                  return (
                    <div
                      key={e.id}
                      title={e.description}
                      style={{
                        display: "flex", alignItems: "center", gap: 6,
                        padding: "3px 6px", borderRadius: 4,
                        fontSize: 12, color: "#374151",
                      }}
                    >
                      <span style={{
                        display: "inline-block", padding: "0 5px",
                        borderRadius: 6, fontSize: 10, fontWeight: 600,
                        background: sc.bg, color: sc.fg,
                        lineHeight: "16px", flexShrink: 0,
                      }}>
                        {e.status}
                      </span>
                      <span style={{ fontWeight: 500 }}>{e.display_name}</span>
                      {e.phase && (
                        <span style={{ fontSize: 10, color: "#9ca3af" }}>
                          ph {e.phase}
                        </span>
                      )}
                      {e.superseded_by && (
                        <span style={{ fontSize: 10, color: "#d97706" }}>
                          → {e.superseded_by}
                        </span>
                      )}
                    </div>
                  );
                })}
                {items.length > 20 && (
                  <div style={{ fontSize: 11, color: "#9ca3af", paddingLeft: 6 }}>
                    + {items.length - 20} more
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
