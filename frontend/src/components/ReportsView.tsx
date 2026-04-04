/**
 * Reports View — browse, view, and delete report artifacts from the backend.
 */

import { useEffect, useState } from "react";
import { listReports, deleteReport, getReport, CatalogReport } from "../api";

export function ReportsView() {
  const [reports, setReports] = useState<CatalogReport[]>([]);
  const [loading, setLoading] = useState(true);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [viewing, setViewing] = useState<{ name: string; data: any } | null>(null);
  const [viewLoading, setViewLoading] = useState(false);

  const load = async () => {
    try {
      setLoading(true);
      setReports(await listReports());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleView = async (name: string) => {
    setViewLoading(true);
    try {
      const data = await getReport(name);
      setViewing({ name, data });
    } catch { alert("Failed to load report"); }
    finally { setViewLoading(false); }
  };

  const handleDelete = async (name: string) => {
    if (!confirm(`Delete report "${name}"?`)) return;
    try { await deleteReport(name); await load(); }
    catch { alert("Delete failed"); }
  };

  const fmtSize = (bytes: number) =>
    bytes > 1_000_000 ? `${(bytes / 1_000_000).toFixed(1)} MB`
    : bytes > 1_000 ? `${(bytes / 1_000).toFixed(0)} KB`
    : `${bytes} B`;

  const kindBadge = (kind: string) => {
    const colors: Record<string, string> = {
      json_report: "#2563eb", document: "#7c3aed", table: "#16a34a", pdf: "#dc2626",
    };
    return colors[kind] ?? "#6b7280";
  };

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Reports</h2>

      {loading && <p>Loading…</p>}

      {!loading && reports.length === 0 && (
        <p style={{ color: "#6b7280" }}>No reports yet. Run an experiment to generate one.</p>
      )}

      {reports.length > 0 && (
        <table style={{ borderCollapse: "collapse", width: "100%", maxWidth: 900 }}>
          <thead>
            <tr>
              {["Name", "Kind", "Size", "Updated", ""].map((h) => (
                <th key={h} style={{ textAlign: "left", padding: "4px 12px 4px 0", borderBottom: "2px solid #e5e7eb", fontSize: 13, color: "#374151" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {reports.map((r) => (
              <tr key={r.relative_path}>
                <td style={tdStyle}>
                  <span style={{ fontWeight: 500 }}>{r.name}</span><br />
                  <span style={{ fontSize: 11, color: "#9ca3af" }}>{r.relative_path}</span>
                </td>
                <td style={tdStyle}>
                  <span style={{ fontSize: 11, padding: "1px 6px", borderRadius: 8, background: kindBadge(r.kind) + "20", color: kindBadge(r.kind), fontWeight: 600 }}>
                    {r.kind.replace("_", " ")}
                  </span>
                </td>
                <td style={tdStyle}>{fmtSize(r.size_bytes)}</td>
                <td style={tdStyle}>{r.updated_at.slice(0, 16).replace("T", " ")}</td>
                <td style={tdStyle}>
                  <span style={{ display: "flex", gap: 6 }}>
                    {r.kind === "json_report" && (
                      <button
                        onClick={() => handleView(r.id)}
                        disabled={viewLoading}
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 12 }}
                      >View</button>
                    )}
                    <button
                      onClick={() => handleDelete(r.id)}
                      style={{ background: "none", border: "1px solid #fca5a5", borderRadius: 4, color: "#dc2626", fontSize: 11, padding: "2px 8px", cursor: "pointer" }}
                    >Delete</button>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {viewing && (
        <div style={{ marginTop: "2rem", border: "1px solid #e5e7eb", borderRadius: 6, overflow: "hidden" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 14px", background: "#f9fafb", borderBottom: "1px solid #e5e7eb" }}>
            <strong style={{ fontSize: 13 }}>{viewing.name}</strong>
            <button onClick={() => setViewing(null)} style={{ background: "none", border: "none", cursor: "pointer", fontSize: 18, color: "#6b7280" }}>×</button>
          </div>
          <pre style={{ margin: 0, padding: "14px", fontSize: 11, fontFamily: "monospace", background: "#1e293b", color: "#e2e8f0", overflowX: "auto", maxHeight: 480 }}>
            {JSON.stringify(viewing.data, null, 2).slice(0, 8000)}
            {JSON.stringify(viewing.data, null, 2).length > 8000 ? "\n…(truncated)" : ""}
          </pre>
        </div>
      )}
    </div>
  );
}

const tdStyle: React.CSSProperties = {
  padding: "6px 12px 6px 0", borderBottom: "1px solid #f3f4f6", fontSize: 13, verticalAlign: "top",
};

const btnStyle: React.CSSProperties = {
  background: "#2563eb", color: "#fff", border: "none", borderRadius: 4,
  padding: "6px 16px", fontSize: 13, cursor: "pointer",
};
