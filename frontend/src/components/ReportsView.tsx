/**
 * Reports View — browse, sort, filter, and open report artifacts.
 * View opens in a new browser window. Sort by name/kind/size/updated.
 */

import { useEffect, useState } from "react";
import {
  listReports, deleteReport, getReportDownloadUrl, openReportFolder, type CatalogReport,
} from "../api";
import { fmtDateTimeCompact } from "../dateFormat";

type SortKey = "name" | "kind" | "size_bytes" | "updated_at";
type SortDir = "asc" | "desc";

export function ReportsView() {
  const [reports, setReports] = useState<CatalogReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [kindFilter, setKindFilter] = useState<Set<string>>(new Set());
  const [expFilter, setExpFilter] = useState<Set<string>>(new Set());
  const [sortKey, setSortKey] = useState<SortKey>("updated_at");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [groupByExp, setGroupByExp] = useState(false);
  const [popupBlocked, setPopupBlocked] = useState<string | null>(null); // blocked URL

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      setReports(await listReports());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load reports");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleView = (r: CatalogReport) => {
    const url = getReportDownloadUrl(r.id);
    // Open as a popup so it stays near the app; detect if blocked
    const popup = window.open(
      url,
      `glossa_report_${r.id}`,
      "width=1100,height=800,menubar=no,toolbar=no,location=no,status=no,scrollbars=yes,resizable=yes"
    );
    if (!popup || popup.closed || typeof popup.closed === "undefined") {
      // Popup blocked — show inline fallback
      setPopupBlocked(url);
    } else {
      popup.focus();
      setPopupBlocked(null);
    }
  };

  const handleDelete = async (r: CatalogReport) => {
    if (!confirm(`Delete "${r.name}"?`)) return;
    try { await deleteReport(r.id); await load(); }
    catch (e) { alert(e instanceof Error ? e.message : "Delete failed"); }
  };

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) setSortDir((d) => d === "asc" ? "desc" : "asc");
    else { setSortKey(key); setSortDir("asc"); }
  };

  const sortIcon = (key: SortKey) =>
    sortKey !== key ? " ↕" : sortDir === "asc" ? " ↑" : " ↓";

  const fmtSize = (b: number) =>
    b > 1_000_000 ? `${(b / 1_000_000).toFixed(1)} MB`
    : b > 1_000 ? `${(b / 1_000).toFixed(0)} KB`
    : `${b} B`;

  const kindColor: Record<string, string> = {
    json_report: "#2563eb", document: "#7c3aed", table: "#16a34a", pdf: "#dc2626", artifact: "#6b7280",
  };

  const allKinds = Array.from(new Set(reports.map((r) => r.kind)));
  const allExps  = Array.from(new Set(reports.map((r) => r.experiment_id).filter(Boolean)));

  const toggleKind = (k: string) => setKindFilter((prev) => {
    const s = new Set(prev); s.has(k) ? s.delete(k) : s.add(k); return s;
  });
  const toggleExp = (e: string) => setExpFilter((prev) => {
    const s = new Set(prev); s.has(e) ? s.delete(e) : s.add(e); return s;
  });

  const sorted = [...reports]
    .filter((r) => (!search || r.name.toLowerCase().includes(search.toLowerCase()))
                && (kindFilter.size === 0 || kindFilter.has(r.kind))
                && (expFilter.size === 0 || expFilter.has(r.experiment_id)))
    .sort((a, b) => {
      const av = a[sortKey as keyof CatalogReport] as string | number;
      const bv = b[sortKey as keyof CatalogReport] as string | number;
      const cmp = av < bv ? -1 : av > bv ? 1 : 0;
      return sortDir === "asc" ? cmp : -cmp;
    });

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>Reports</h2>
        <button onClick={load} style={{ ...btnStyle, padding: "4px 12px", fontSize: 12, background: "#6b7280" }}>
          ⟳ Refresh
        </button>
      </div>

      {/* Search */}
      <div style={{ display: "flex", gap: 8, marginBottom: "0.75rem", alignItems: "center", flexWrap: "wrap" }}>
        <input
          placeholder="Search by name…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ padding: "4px 10px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, width: 240 }}
        />
        <label style={{ fontSize: 12, color: "#6b7280", display: "flex", alignItems: "center", gap: 5, cursor: "pointer" }}>
          <input type="checkbox" checked={groupByExp} onChange={(e) => setGroupByExp(e.target.checked)} />
          Group by experiment
        </label>
        <span style={{ fontSize: 12, color: "#9ca3af", marginLeft: "auto" }}>
          {sorted.length} / {reports.length} reports
        </span>
      </div>

      {/* Kind multi-select pills */}
      {allKinds.length > 0 && (
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginBottom: "0.5rem", alignItems: "center" }}>
          <span style={{ fontSize: 11, color: "#9ca3af", marginRight: 2 }}>Type:</span>
          {allKinds.map((k) => (
            <button
              key={k}
              onClick={() => toggleKind(k)}
              style={{
                padding: "2px 10px", border: "1px solid", borderRadius: 10, cursor: "pointer",
                fontSize: 11, fontWeight: kindFilter.has(k) ? 700 : 400,
                background: kindFilter.has(k) ? (kindColor[k] ?? "#1e3a5f") : "#fff",
                borderColor: kindFilter.has(k) ? (kindColor[k] ?? "#1e3a5f") : "#d1d5db",
                color: kindFilter.has(k) ? "#fff" : "#374151",
              }}
            >
              {k.replace("_", " ")}
            </button>
          ))}
          {kindFilter.size > 0 && (
            <button onClick={() => setKindFilter(new Set())} style={{ fontSize: 11, background: "none", border: "none", color: "#6b7280", cursor: "pointer" }}>clear</button>
          )}
        </div>
      )}

      {/* Experiment multi-select pills */}
      {allExps.length > 0 && (
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginBottom: "1rem", alignItems: "center" }}>
          <span style={{ fontSize: 11, color: "#9ca3af", marginRight: 2 }}>Experiment:</span>
          {allExps.map((e) => (
            <button
              key={e}
              onClick={() => toggleExp(e)}
              style={{
                padding: "2px 10px", border: "1px solid", borderRadius: 10, cursor: "pointer",
                fontSize: 11, fontWeight: expFilter.has(e) ? 700 : 400,
                background: expFilter.has(e) ? "#1e3a5f" : "#fff",
                borderColor: expFilter.has(e) ? "#1e3a5f" : "#d1d5db",
                color: expFilter.has(e) ? "#fff" : "#374151",
              }}
            >
              {e.replace(/_/g, " ")}
            </button>
          ))}
          {expFilter.size > 0 && (
            <button onClick={() => setExpFilter(new Set())} style={{ fontSize: 11, background: "none", border: "none", color: "#6b7280", cursor: "pointer" }}>clear</button>
          )}
        </div>
      )}

      {/* Popup-blocked warning */}
      {popupBlocked && (
        <div style={{
          display: "flex", alignItems: "flex-start", gap: 12,
          padding: "12px 16px", marginBottom: "1rem",
          background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 8,
        }}>
          <span style={{ fontSize: 20, lineHeight: 1, flexShrink: 0 }}>&#128683;</span>
          <div style={{ flex: 1 }}>
            <p style={{ margin: "0 0 6px", fontWeight: 700, color: "#b91c1c", fontSize: 13 }}>
              Popups are blocked by your browser.
            </p>
            <p style={{ margin: "0 0 8px", fontSize: 12, color: "#7f1d1d" }}>
              Allow popups for <strong>localhost:8001</strong> in your browser settings, then click View again.
              Or open the file directly:
            </p>
            <a
              href={popupBlocked}
              target="_blank"
              rel="noopener noreferrer"
              style={{ fontSize: 12, color: "#2563eb", fontWeight: 600 }}
            >
              Open in new tab instead →
            </a>
          </div>
          <button
            onClick={() => setPopupBlocked(null)}
            style={{ border: "none", background: "none", cursor: "pointer", fontSize: 18, color: "#9ca3af", padding: 0, flexShrink: 0 }}
          >×</button>
        </div>
      )}

      {loading && <p style={{ color: "#6b7280" }}>Loading reports…</p>}
      {error && (
        <div style={{ padding: "10px 14px", background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 6, color: "#991b1b", fontSize: 13, marginBottom: 12 }}>
          {error} — <button onClick={load} style={{ background: "none", border: "none", cursor: "pointer", color: "#2563eb", textDecoration: "underline" }}>Retry</button>
        </div>
      )}
      {!loading && !error && reports.length === 0 && (
        <p style={{ color: "#6b7280" }}>No reports yet. Run an experiment to generate one.</p>
      )}

      {sorted.length > 0 && (
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              {([
                ["name", "Name"],
                ["kind", "Kind"],
                ["size_bytes", "Size"],
                ["updated_at", "Updated"],
                ["", ""],
              ] as [string, string][]).map(([key, label]) => (
                <th
                  key={key || "actions"}
                  style={{ ...thStyle, cursor: key ? "pointer" : "default", userSelect: "none", whiteSpace: "nowrap" }}
                  onClick={() => key && toggleSort(key as SortKey)}
                >
                  {label}{key ? sortIcon(key as SortKey) : ""}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((r) => {
              const color = kindColor[r.kind] ?? "#6b7280";
              return (
                <tr
                  key={r.relative_path}
                  style={{ cursor: "pointer" }}
                  onClick={() => handleView(r)}
                >
                  <td style={tdStyle}>
                    <span style={{ fontWeight: 500, color: "#1e3a5f" }}>{r.name}</span>
                    {r.experiment_id && (
                      <span style={{ marginLeft: 6, fontSize: 10, padding: "1px 6px", borderRadius: 8, background: "#eff6ff", color: "#2563eb", fontWeight: 600 }}>
                        {r.experiment_id.replace(/_/g, " ")}
                      </span>
                    )}
                    <br /><span style={{ fontSize: 11, color: "#9ca3af" }}>{r.relative_path}</span>
                  </td>
                  <td style={tdStyle}>
                    <span style={{ fontSize: 11, padding: "1px 6px", borderRadius: 8, background: color + "20", color, fontWeight: 600 }}>
                      {r.kind.replace("_", " ")}
                    </span>
                  </td>
                  <td style={{ ...tdStyle, whiteSpace: "nowrap" }}>{fmtSize(r.size_bytes)}</td>
                  <td style={{ ...tdStyle, whiteSpace: "nowrap" }}>{fmtDateTimeCompact(r.updated_at)}</td>
                  <td style={tdStyle} onClick={(e) => e.stopPropagation()}>
                    <span style={{ display: "flex", gap: 4 }}>
                      <button
                        onClick={() => handleView(r)}
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 11, background: "#2563eb" }}
                        title="View in new window"
                      >View</button>
                      <button
                        onClick={() => openReportFolder(r.id).catch(() => {})}
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 11, background: "#6b7280" }}
                        title="Open containing folder in Explorer"
                      >Open Folder</button>
                      <button
                        onClick={() => handleDelete(r)}
                        style={{ background: "none", border: "1px solid #fca5a5", borderRadius: 4, color: "#dc2626", fontSize: 11, padding: "2px 8px", cursor: "pointer" }}
                      >Delete</button>
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}

const thStyle: React.CSSProperties = {
  textAlign: "left", padding: "6px 14px 6px 0",
  borderBottom: "2px solid #e5e7eb", fontSize: 13, color: "#374151",
};

const tdStyle: React.CSSProperties = {
  padding: "6px 12px 6px 0", borderBottom: "1px solid #f3f4f6", fontSize: 13, verticalAlign: "middle",
};

const btnStyle: React.CSSProperties = {
  background: "#2563eb", color: "#fff", border: "none", borderRadius: 4,
  padding: "6px 16px", fontSize: 13, cursor: "pointer",
};
