/**
 * Reports View — browse, view, and delete report artifacts from the backend.
 * Supports JSON inline view and PDF iframe embedding.
 */

import { useEffect, useState } from "react";
import {
  listReports, deleteReport, getReport, getReportDownloadUrl, CatalogReport
} from "../api";

type ViewMode = { kind: "json"; name: string; data: unknown } | { kind: "pdf"; name: string; url: string } | null;

export function ReportsView() {
  const [reports, setReports] = useState<CatalogReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewing, setViewing] = useState<ViewMode>(null);
  const [viewLoading, setViewLoading] = useState(false);
  const [search, setSearch] = useState("");

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

  const handleView = async (r: CatalogReport) => {
    if (r.kind === "pdf") {
      setViewing({ kind: "pdf", name: r.name, url: getReportDownloadUrl(r.id) });
      return;
    }
    setViewLoading(true);
    try {
      const data = await getReport(r.id);
      setViewing({ kind: "json", name: r.name, data });
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed to load report");
    } finally {
      setViewLoading(false);
    }
  };

  const handleDelete = async (r: CatalogReport) => {
    if (!confirm(`Delete "${r.name}"?`)) return;
    try { await deleteReport(r.id); await load(); }
    catch (e) { alert(e instanceof Error ? e.message : "Delete failed"); }
  };

  const fmtSize = (b: number) =>
    b > 1_000_000 ? `${(b / 1_000_000).toFixed(1)} MB`
    : b > 1_000 ? `${(b / 1_000).toFixed(0)} KB`
    : `${b} B`;

  const kindColor: Record<string, string> = {
    json_report: "#2563eb", document: "#7c3aed", table: "#16a34a", pdf: "#dc2626", artifact: "#6b7280",
  };

  const filtered = reports.filter(
    (r) => !search || r.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h2 style={{ margin: 0 }}>Reports</h2>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <input
            placeholder="Search reports..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ padding: "4px 10px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, width: 200 }}
          />
          <button onClick={load} style={{ ...btnStyle, padding: "4px 12px", fontSize: 12, background: "#6b7280" }}>
            Refresh
          </button>
        </div>
      </div>

      {loading && <p style={{ color: "#6b7280" }}>Loading reports...</p>}
      {error && (
        <div style={{ padding: "10px 14px", background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 6, color: "#991b1b", fontSize: 13, marginBottom: 12 }}>
          {error} — <button onClick={load} style={{ background: "none", border: "none", cursor: "pointer", color: "#2563eb", textDecoration: "underline" }}>Retry</button>
        </div>
      )}

      {!loading && !error && reports.length === 0 && (
        <p style={{ color: "#6b7280" }}>No reports yet. Run an experiment to generate one.</p>
      )}

      {filtered.length > 0 && (
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              {["Name", "Kind", "Size", "Updated", ""].map((h) => (
                <th key={h} style={thStyle}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((r) => {
              const color = kindColor[r.kind] ?? "#6b7280";
              const canView = r.kind === "json_report" || r.kind === "pdf" || r.kind === "document" || r.kind === "table";
              return (
                <tr key={r.relative_path} style={{ cursor: "pointer" }}
                  onClick={() => canView && handleView(r)}>
                  <td style={tdStyle}>
                    <span style={{ fontWeight: 500, color: canView ? "#1e3a5f" : undefined }}>{r.name}</span>
                    <br /><span style={{ fontSize: 11, color: "#9ca3af" }}>{r.relative_path}</span>
                  </td>
                  <td style={tdStyle}>
                    <span style={{ fontSize: 11, padding: "1px 6px", borderRadius: 8, background: color + "20", color, fontWeight: 600 }}>
                      {r.kind.replace("_", " ")}
                    </span>
                  </td>
                  <td style={tdStyle}>{fmtSize(r.size_bytes)}</td>
                  <td style={tdStyle}>{r.updated_at.slice(0, 16).replace("T", " ")}</td>
                  <td style={tdStyle} onClick={(e) => e.stopPropagation()}>
                    <span style={{ display: "flex", gap: 4 }}>
                      {canView && (
                        <button onClick={() => handleView(r)} disabled={viewLoading}
                          style={{ ...btnStyle, padding: "2px 10px", fontSize: 11 }}>View</button>
                      )}
                      <a href={getReportDownloadUrl(r.id)} target="_blank" rel="noopener noreferrer"
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 11, background: "#7c3aed", textDecoration: "none", display: "inline-block" }}>
                        Open
                      </a>
                      <button onClick={() => handleDelete(r)}
                        style={{ background: "none", border: "1px solid #fca5a5", borderRadius: 4, color: "#dc2626", fontSize: 11, padding: "2px 8px", cursor: "pointer" }}>
                        Delete
                      </button>
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

      {/* Viewer panel */}
      {viewing && (
        <div style={{ marginTop: "1.5rem", border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center",
            padding: "10px 14px", background: "#f9fafb", borderBottom: "1px solid #e5e7eb" }}>
            <strong style={{ fontSize: 13 }}>{viewing.name}</strong>
            <div style={{ display: "flex", gap: 8 }}>
              <a href={viewing.kind === "pdf" ? viewing.url : getReportDownloadUrl(viewing.name)}
                target="_blank" rel="noopener noreferrer"
                style={{ fontSize: 12, color: "#2563eb" }}>Open in tab</a>
              <button onClick={() => setViewing(null)}
                style={{ background: "none", border: "none", cursor: "pointer", fontSize: 18, color: "#6b7280" }}>
                ×
              </button>
            </div>
          </div>

          {viewing.kind === "pdf" && (
            <iframe
              src={viewing.url}
              style={{ width: "100%", height: 640, border: "none", display: "block" }}
              title={viewing.name}
            />
          )}

          {viewing.kind === "json" && (
            <pre style={{ margin: 0, padding: "14px", fontSize: 11, fontFamily: "monospace",
              background: "#1e293b", color: "#e2e8f0", overflowX: "auto", maxHeight: 540 }}>
              {JSON.stringify(viewing.data, null, 2).slice(0, 12000)}
              {JSON.stringify(viewing.data, null, 2).length > 12000 ? "\n\u2026(truncated)" : ""}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}

const thStyle: React.CSSProperties = {
  textAlign: "left", padding: "4px 12px 4px 0",
  borderBottom: "2px solid #e5e7eb", fontSize: 13, color: "#374151",
};

const tdStyle: React.CSSProperties = {
  padding: "6px 12px 6px 0", borderBottom: "1px solid #f3f4f6", fontSize: 13, verticalAlign: "top",
};

const btnStyle: React.CSSProperties = {
  background: "#2563eb", color: "#fff", border: "none", borderRadius: 4,
  padding: "6px 16px", fontSize: 13, cursor: "pointer",
};
