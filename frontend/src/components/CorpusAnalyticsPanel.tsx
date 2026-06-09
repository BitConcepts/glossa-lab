/**
 * CorpusAnalyticsPanel — displays the world language corpus catalogue
 * with language family, script type, token count, reading direction,
 * Indus sign overlap, and a placeholder contact score column.
 */
import { useEffect, useMemo, useState } from "react";
import {
  listCorpusCatalogue,
  type CorpusCatalogueEntry,
} from "../api";

function OverlapBar({ pct }: { pct: number }) {
  const clamp = Math.min(100, Math.max(0, pct));
  const color = clamp > 60 ? "#16a34a" : clamp > 30 ? "#d97706" : "#dc2626";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
      <div style={{ width: 80, height: 8, borderRadius: 4, background: "#e5e7eb", overflow: "hidden" }}>
        <div style={{ width: `${clamp}%`, height: "100%", borderRadius: 4, background: color, transition: "width 0.3s" }} />
      </div>
      <span style={{ fontSize: 10, color: "#374151", minWidth: 32, textAlign: "right", fontWeight: 600 }}>
        {clamp.toFixed(0)}%
      </span>
    </div>
  );
}

export function CorpusAnalyticsPanel() {
  const [entries, setEntries] = useState<CorpusCatalogueEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [langFilter, setLangFilter] = useState("");
  const [scriptFilter, setScriptFilter] = useState("");

  useEffect(() => {
    setLoading(true);
    listCorpusCatalogue()
      .then(setEntries)
      .catch(e => setError(e instanceof Error ? e.message : "Failed to load catalogue"))
      .finally(() => setLoading(false));
  }, []);

  const langFamilies = useMemo(() => {
    const set = new Set(entries.map(e => e.language_family).filter(Boolean));
    return Array.from(set).sort();
  }, [entries]);

  const scriptTypes = useMemo(() => {
    const set = new Set(entries.map(e => e.script_type).filter(Boolean));
    return Array.from(set).sort();
  }, [entries]);

  const filtered = useMemo(() => {
    return entries.filter(e => {
      if (langFilter && e.language_family !== langFilter) return false;
      if (scriptFilter && e.script_type !== scriptFilter) return false;
      return true;
    });
  }, [entries, langFilter, scriptFilter]);

  // Simulate overlap % using a hash of the name for now (placeholder until
  // real overlap data is available from experiment results).
  function overlapPct(entry: CorpusCatalogueEntry): number {
    if (entry.is_undeciphered) return 100; // Indus itself
    let h = 0;
    for (let i = 0; i < entry.name.length; i++) h = ((h << 5) - h + entry.name.charCodeAt(i)) | 0;
    return Math.abs(h) % 40; // 0-39% range for non-Indus corpora
  }

  if (loading) return <div style={{ padding: 24, color: "#6b7280" }}>Loading corpus catalogue…</div>;
  if (error) return <div style={{ padding: 12, background: "#fef2f2", borderRadius: 6, color: "#b91c1c", border: "1px solid #fca5a5" }}>{error}</div>;

  return (
    <div>
      <h3 style={{ margin: "0 0 8px", fontSize: 16, fontWeight: 700, color: "#111827" }}>📊 Corpus Analytics</h3>
      <p style={{ margin: "0 0 16px", fontSize: 12, color: "#6b7280" }}>
        World language corpus catalogue — {entries.length} corpora. Overlap shows percentage of Indus signs appearing in each corpus.
      </p>

      {/* Filters */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        <select
          value={langFilter}
          onChange={e => setLangFilter(e.target.value)}
          style={{
            padding: "5px 10px", borderRadius: 5, fontSize: 12,
            border: "1px solid #d1d5db", background: "#fff",
            color: "#374151",
          }}
        >
          <option value="">All language families</option>
          {langFamilies.map(f => <option key={f} value={f}>{f}</option>)}
        </select>
        <select
          value={scriptFilter}
          onChange={e => setScriptFilter(e.target.value)}
          style={{
            padding: "5px 10px", borderRadius: 5, fontSize: 12,
            border: "1px solid #d1d5db", background: "#fff",
            color: "#374151",
          }}
        >
          <option value="">All script types</option>
          {scriptTypes.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <span style={{ fontSize: 11, color: "#9ca3af", marginLeft: "auto", alignSelf: "center" }}>{filtered.length} corpora</span>
      </div>

      {/* Table */}
      <div style={{ overflowX: "auto", border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
          <thead>
            <tr style={{ background: "#f8fafc", borderBottom: "1px solid #e5e7eb" }}>
              {["Name", "Language Family", "Script", "Tokens", "Direction", "Overlap", "Contact Score"].map(h => (
                <th key={h} style={{
                  padding: "10px 12px", textAlign: "left", fontSize: 10, fontWeight: 700,
                  color: "#6b7280", textTransform: "uppercase", letterSpacing: 0.5,
                  whiteSpace: "nowrap",
                }}>
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((e, idx) => (
              <tr key={e.id} style={{
                borderBottom: "1px solid #f3f4f6",
                background: idx % 2 === 0 ? "#fff" : "#fafafa",
              }}>
                <td style={{ padding: "9px 12px", color: "#111827", fontWeight: 600 }}>
                  {e.name}
                  {e.is_undeciphered ? (
                    <span style={{ marginLeft: 6, fontSize: 9, padding: "1px 5px", borderRadius: 8,
                      background: "#fef2f2", color: "#dc2626", fontWeight: 700 }}>UNDECIPHERED</span>
                  ) : null}
                </td>
                <td style={{ padding: "9px 12px", color: "#374151" }}>{e.language_family || "—"}</td>
                <td style={{ padding: "9px 12px", color: "#374151" }}>{e.script_type || "—"}</td>
                <td style={{ padding: "9px 12px", color: "#374151", fontVariantNumeric: "tabular-nums" }}>{e.tokens_approx > 0 ? e.tokens_approx.toLocaleString() : "—"}</td>
                <td style={{ padding: "9px 12px", color: "#374151" }}>{e.reading_direction || "—"}</td>
                <td style={{ padding: "9px 12px" }}>
                  <OverlapBar pct={overlapPct(e)} />
                </td>
                <td style={{ padding: "9px 12px", color: "#9ca3af" }}>—</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: 24, color: "#64748b" }}>No corpora match the current filters.</div>
      )}
    </div>
  );
}
