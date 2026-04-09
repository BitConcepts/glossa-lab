/**
 * Reports View — browse, sort, filter, and open report artifacts.
 * View opens in a new browser window. Sort by name/kind/size/updated.
 */

import { useEffect, useState } from "react";
import {
  listReports, deleteReport, getReportDownloadUrl, openReportFolder,
  listStudies,
  type CatalogReport, type StudyResponse,
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
  const [studyFilter, setStudyFilter] = useState<Set<string>>(new Set());
  const [sortKey, setSortKey] = useState<SortKey>("updated_at");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [groupByExp, setGroupByExp] = useState(true); // default on
  const [studies, setStudies] = useState<StudyResponse[]>([]);
  const [popupBlocked, setPopupBlocked] = useState<string | null>(null);
  // ── Compose mode ──────────────────────────────────────────────
  const [composeMode, setComposeMode] = useState(false);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const toggleSelected = (id: string) =>
    setSelected((prev) => { const s = new Set(prev); s.has(id) ? s.delete(id) : s.add(id); return s; });

  // ── Starred reports (persist to localStorage) ──────────────────
  const [starredReports, setStarredReports] = useState<Set<string>>(() => {
    try { return new Set(JSON.parse(localStorage.getItem("glossa_starred_reports") ?? "[]")); }
    catch { return new Set(); }
  });
  const toggleStarReport = (id: string) => {
    setStarredReports(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      localStorage.setItem("glossa_starred_reports", JSON.stringify([...next]));
      return next;
    });
  };

  const exportComposedPdf = async () => {
    const picked = reports.filter((r) => selected.has(r.id));
    if (!picked.length) return;

    // Fetch actual JSON content from each selected report
    const sectionsHtml = await Promise.all(picked.map(async (r) => {
      const url = getReportDownloadUrl(r.id);
      let contentHtml = `<a href="${url}" target="_blank" style="font-size:12px;color:#2563eb">Open source file →</a>`;
      try {
        const res = await fetch(url);
        if (res.ok && r.kind === "json_report") {
          const data = await res.json();
          // If it's a Glossa study report, render results section
          if (data.results && typeof data.results === "object") {
            const rows = Object.entries(data.results as Record<string, unknown>).map(([key, val]) => {
              const valStr = typeof val === "object" ? JSON.stringify(val, null, 2) : String(val);
              return (
                `<tr style="border-bottom:1px solid #f3f4f6">` +
                `<td style="padding:6px 12px 6px 0;font-size:12px;font-weight:600;color:#1e3a5f;white-space:nowrap;vertical-align:top;width:220px">${key.replace(/_/g, ' ')}</td>` +
                `<td style="padding:6px 0;font-size:11px;color:#374151"><pre style="margin:0;white-space:pre-wrap;font-family:monospace;font-size:10px;max-height:160px;overflow:hidden">${valStr.slice(0, 800)}${valStr.length > 800 ? '\u2026' : ''}</pre></td>` +
                `</tr>`
              );
            }).join('');
            const generated = typeof data.generated === "string" ? `<p style="font-size:10px;color:#9ca3af;margin:0 0 6px">${data.generated}</p>` : "";
            contentHtml = generated + (rows.length
              ? `<table style="border-collapse:collapse;width:100%">${rows}</table>`
              : `<pre style="font-size:10px;color:#6b7280">${JSON.stringify(data, null, 2).slice(0, 1200)}</pre>`);
          } else {
            contentHtml = `<pre style="font-size:10px;color:#374151;white-space:pre-wrap">${JSON.stringify(data, null, 2).slice(0, 2000)}</pre>`;
          }
        }
      } catch { /* leave fallback link */ }
      return (
        `<section style="margin-bottom:32px;page-break-inside:avoid">` +
        `<h2 style="font-size:14px;margin:0 0 3px;color:#1e3a5f">${r.name}</h2>` +
        `<p style="font-size:11px;color:#9ca3af;margin:0 0 8px">${r.kind.replace('_', ' ')} · ${r.relative_path}</p>` +
        contentHtml +
        `</section>`
      );
    }));

    const sections = sectionsHtml.join("<hr style='border:none;border-top:1px solid #e5e7eb;margin:20px 0'>\n");
    const win = window.open("", "_blank", "width=920,height=940");
    if (!win) { alert("Allow popups from localhost in your browser settings, then try again."); return; }
    win.document.write(
      `<!DOCTYPE html><html><head><title>Glossa Lab — Research Report</title>` +
      `<style>
        body{font-family:system-ui,sans-serif;max-width:780px;margin:40px auto;font-size:13px;line-height:1.65;color:#111}
        h1{font-size:20px;margin-bottom:4px}h2{font-size:15px;color:#1e3a5f}
        @media print{body{margin:10px 20px}section{page-break-inside:avoid}}
      </style></head><body>` +
      `<h1>Glossa Lab — Research Report</h1>` +
      `<p style="color:#9ca3af;font-size:11px;margin:0 0 16px">Generated ${new Date().toLocaleString()} · ${picked.length} report${picked.length !== 1 ? 's' : ''}</p>` +
      `<hr style="border:none;border-top:2px solid #e5e7eb;margin-bottom:24px">` +
      sections +
      `<script>setTimeout(()=>{window.print()},600)</script></body></html>`
    );
    win.document.close();
  };

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

  useEffect(() => {
    load();
    listStudies().then(setStudies).catch(() => {});
  }, []);

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
  const toggleStudy = (sid: string) => setStudyFilter((prev) => {
    const s = new Set(prev); s.has(sid) ? s.delete(sid) : s.add(sid); return s;
  });

  // Build study->experiments mapping from study graph nodes
  const studyExpMap: Record<string, Set<string>> = {};
  for (const st of studies) {
    const exps = new Set((st.graph?.nodes ?? []).map((n: {ref_id: string}) => n.ref_id).filter(Boolean));
    studyExpMap[st.id] = exps;
  }

  // Resolve which experiment IDs belong to the selected studies
  const studyExpIds = studyFilter.size === 0 ? null :
    new Set([...studyFilter].flatMap((sid) => [...(studyExpMap[sid] ?? new Set())]));

  const sorted = [...reports]
    .filter((r) => (!search || r.name.toLowerCase().includes(search.toLowerCase()))
                && (kindFilter.size === 0 || kindFilter.has(r.kind))
                && (expFilter.size === 0 || expFilter.has(r.experiment_id))
                && (studyExpIds === null || (r.experiment_id && studyExpIds.has(r.experiment_id))))
    .sort((a, b) => {
      // Starred always float to top
      const aS = starredReports.has(a.id), bS = starredReports.has(b.id);
      if (aS && !bS) return -1;
      if (!aS && bS) return 1;
      // Then by selected sort key
      const av = a[sortKey as keyof CatalogReport] as string | number;
      const bv = b[sortKey as keyof CatalogReport] as string | number;
      const cmp = av < bv ? -1 : av > bv ? 1 : 0;
      return sortDir === "asc" ? cmp : -cmp;
    });

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>Reports</h2>
        <div style={{ display: "flex", gap: 6 }}>
          <button
            onClick={() => { setComposeMode((m) => !m); setSelected(new Set()); }}
            style={{ ...btnStyle, padding: "4px 12px", fontSize: 12,
              background: composeMode ? "#7c3aed" : "#f3f4f6",
              color: composeMode ? "#fff" : "#374151",
              border: composeMode ? "none" : "1px solid #d1d5db" }}
          >
            {composeMode ? "✕ Cancel Compose" : "📊 Compose"}
          </button>
          <button onClick={load} style={{ ...btnStyle, padding: "4px 12px", fontSize: 12, background: "#6b7280" }}>
            ⟳ Refresh
          </button>
        </div>
      </div>

      {/* Compose toolbar */}
      {composeMode && (
        <div style={{
          display: "flex", alignItems: "center", gap: 10,
          padding: "10px 14px", background: "#f3e8ff",
          border: "1px solid #a78bfa", borderRadius: 8, marginBottom: "0.75rem",
        }}>
          <span style={{ fontSize: 12, color: "#7c3aed", fontWeight: 600 }}>
            📊 Compose mode &mdash; select reports to include
          </span>
          <span style={{ fontSize: 12, color: "#9ca3af" }}>
            {selected.size} selected
          </span>
          <button onClick={() => setSelected(new Set(sorted.map((r) => r.id)))}
            style={{ padding: "3px 10px", border: "1px solid #a78bfa", borderRadius: 4, background: "#fff", fontSize: 11, cursor: "pointer", color: "#7c3aed" }}>
            Select all
          </button>
          <button onClick={() => setSelected(new Set())}
            style={{ padding: "3px 10px", border: "1px solid #d1d5db", borderRadius: 4, background: "#fff", fontSize: 11, cursor: "pointer", color: "#6b7280" }}>
            Clear
          </button>
          <div style={{ flex: 1 }} />
          <button
            onClick={exportComposedPdf}
            disabled={selected.size === 0}
            style={{ ...btnStyle, padding: "5px 16px", fontSize: 12, background: selected.size > 0 ? "#7c3aed" : "#d1d5db", cursor: selected.size > 0 ? "pointer" : "not-allowed" }}>
            📄 Export PDF ({selected.size})
          </button>
        </div>
      )}

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

      {/* Kind filter */}
      {allKinds.length > 0 && (
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginBottom: "0.5rem", alignItems: "center" }}>
          <span style={{ fontSize: 11, color: "#9ca3af", marginRight: 2 }}>Type:</span>
          <button onClick={() => setKindFilter(new Set())} style={pillStyle(kindFilter.size === 0, "#1e3a5f")}>
            All
          </button>
          {allKinds.map((k) => (
            <button key={k} onClick={() => toggleKind(k)}
              style={pillStyle(kindFilter.has(k), kindColor[k] ?? "#1e3a5f")}>
              {k.replace("_", " ")}
            </button>
          ))}
        </div>
      )}

      {/* Experiment filter */}
      {allExps.length > 0 && (
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginBottom: "0.5rem", alignItems: "center" }}>
          <span style={{ fontSize: 11, color: "#9ca3af", marginRight: 2 }}>Experiment:</span>
          <button onClick={() => setExpFilter(new Set())} style={pillStyle(expFilter.size === 0, "#1e3a5f")}>
            All
          </button>
          {allExps.map((e) => (
            <button key={e} onClick={() => toggleExp(e)}
              style={pillStyle(expFilter.has(e), "#1e3a5f")}>
              {e.replace(/_/g, " ")}
            </button>
          ))}
        </div>
      )}

      {/* Study filter */}
      {studies.length > 0 && (
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginBottom: "1rem", alignItems: "center" }}>
          <span style={{ fontSize: 11, color: "#9ca3af", marginRight: 2 }}>Study:</span>
          <button onClick={() => setStudyFilter(new Set())} style={pillStyle(studyFilter.size === 0, "#7c3aed")}>
            All
          </button>
          {studies.map((st) => (
            <button key={st.id} onClick={() => toggleStudy(st.id)}
              style={pillStyle(studyFilter.has(st.id), "#7c3aed")}>
              {st.name}
            </button>
          ))}
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
              {/* Star column */}
              <th style={{ ...thStyle, width: 24, cursor: "default" }}>⭐</th>
              {composeMode && (
                <th style={{ ...thStyle, width: 32, cursor: "default" }}></th>
              )}
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
              const isSel = selected.has(r.id);
              const isStarred = starredReports.has(r.id);
              return (
                <tr
                  key={r.relative_path}
                  style={{ cursor: "pointer",
                    background: isSel ? "#f3e8ff" : isStarred ? "#fffbeb" : undefined }}
                  onClick={() => composeMode ? toggleSelected(r.id) : handleView(r)}
                >
                  {/* Star toggle — stopPropagation so row click doesn't also fire */}
                  <td style={{ ...tdStyle, width: 24 }} onClick={(e) => { e.stopPropagation(); toggleStarReport(r.id); }}>
                    <span style={{ cursor: "pointer", fontSize: 13, opacity: isStarred ? 1 : 0.25, lineHeight: 1 }}
                      title={isStarred ? "Unpin" : "Pin to top"}>
                      {isStarred ? "⭐" : "☆"}
                    </span>
                  </td>
                  {composeMode && (
                    // Bug fix: td onClick only stops propagation; onChange on input does the actual toggle.
                    // Previously both fired toggleSelected, causing a double-toggle (net = no change).
                    <td style={{ ...tdStyle, width: 32 }} onClick={(e) => e.stopPropagation()}>
                      <input type="checkbox" checked={isSel} onChange={() => toggleSelected(r.id)}
                        style={{ cursor: "pointer", width: 14, height: 14 }} />
                    </td>
                  )}
                  <td style={tdStyle}>
                    <span style={{ fontWeight: 500, color: isSel ? "#7c3aed" : "#1e3a5f" }}>{r.name}</span>
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

const pillStyle = (active: boolean, color: string): React.CSSProperties => ({
  padding: "2px 10px", border: `1px solid ${active ? color : "#d1d5db"}`,
  borderRadius: 10, cursor: "pointer", fontSize: 11,
  fontWeight: active ? 700 : 400,
  background: active ? color : "#fff",
  color: active ? "#fff" : "#374151",
});

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
