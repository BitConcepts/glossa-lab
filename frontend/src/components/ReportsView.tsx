/**
 * Reports View — browse, sort, filter, and open report artifacts.
 * View opens in a new browser window. Sort by name/kind/size/updated.
 */

import { useEffect, useState } from "react";
import {
  listReports, deleteReport, getReportDownloadUrl, openReportFolder, type CatalogReport,
} from "../api";

type SortKey = "name" | "kind" | "size_bytes" | "updated_at";
type SortDir = "asc" | "desc";

export function ReportsView() {
  const [reports, setReports] = useState<CatalogReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [kindFilter, setKindFilter] = useState("all");
  const [sortKey, setSortKey] = useState<SortKey>("updated_at");
  const [sortDir, setSortDir] = useState<SortDir>("desc");

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
    // Always open in a new window/tab — no inline panel
    window.open(getReportDownloadUrl(r.id), "_blank", "noopener,noreferrer");
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

  const kinds = ["all", ...Array.from(new Set(reports.map((r) => r.kind)))];

  const sorted = [...reports]
    .filter((r) => (!search || r.name.toLowerCase().includes(search.toLowerCase()))
                && (kindFilter === "all" || r.kind === kindFilter))
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

      {/* Filters */}
      <div style={{ display: "flex", gap: 8, marginBottom: "1rem", flexWrap: "wrap", alignItems: "center" }}>
        <input
          placeholder="Search by name…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ padding: "4px 10px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, width: 220 }}
        />
        <select
          value={kindFilter}
          onChange={(e) => setKindFilter(e.target.value)}
          style={{ padding: "4px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 12, cursor: "pointer" }}
        >
          {kinds.map((k) => (
            <option key={k} value={k}>
              {k === "all" ? "All types" : k.replace("_", " ")}
            </option>
          ))}
        </select>
        <span style={{ fontSize: 12, color: "#9ca3af", marginLeft: 4 }}>
          {sorted.length} / {reports.length} reports
        </span>
      </div>

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
                    <br /><span style={{ fontSize: 11, color: "#9ca3af" }}>{r.relative_path}</span>
                  </td>
                  <td style={tdStyle}>
                    <span style={{ fontSize: 11, padding: "1px 6px", borderRadius: 8, background: color + "20", color, fontWeight: 600 }}>
                      {r.kind.replace("_", " ")}
                    </span>
                  </td>
                  <td style={{ ...tdStyle, whiteSpace: "nowrap" }}>{fmtSize(r.size_bytes)}</td>
                  <td style={{ ...tdStyle, whiteSpace: "nowrap" }}>{r.updated_at.slice(0, 16).replace("T", " ")}</td>
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
