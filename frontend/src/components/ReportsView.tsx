/**
 * Reports View — browse, sort, filter, and open report artifacts.
 * View opens in a new browser window. Sort by name/kind/size/updated.
 */

import { useEffect, useState } from "react";
import {
  listReports, deleteReport, getReportDownloadUrl, openReportFolder,
  listStudies, aiReportSynthesis,
  listReportTemplates, generateReport,
  listUserReportTemplates, createUserReportTemplate,
  deleteUserReportTemplate,
  type CatalogReport, type StudyResponse, type ReportTemplate,
  type UserReportTemplate, type ReportTemplateSection,
} from "../api";
import { fmtDateTimeCompact } from "../dateFormat";

/** Simple markdown → HTML renderer for the AI report modal. */
function renderMarkdown(md: string): string {
  return md
    .replace(/^### (.+)$/gm, '<h3 style="font-size:14px;margin:16px 0 6px;color:#1e3a5f">$1</h3>')
    .replace(/^## (.+)$/gm, '<h2 style="font-size:16px;margin:20px 0 8px;color:#1e3a5f">$1</h2>')
    .replace(/^# (.+)$/gm, '<h1 style="font-size:18px;margin:24px 0 10px;color:#111">$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^\| (.+) \|$/gm, (row) => {
      const cells = row.split('|').filter(c => c.trim());
      return '<tr>' + cells.map(c => `<td style="padding:4px 10px;border:1px solid #e5e7eb">${c.trim()}</td>`).join('') + '</tr>';
    })
    .replace(/(<tr>.*?<\/tr>\n?)+/gs, (t) => `<table style="border-collapse:collapse;width:100%;margin:8px 0">${t}</table>`)
    .replace(/^- (.+)$/gm, '<li style="margin:2px 0">$1</li>')
    .replace(/(<li.*?<\/li>\n?)+/gs, '<ul style="margin:6px 0;padding-left:20px">$1</ul>')
    .replace(/^(?!<[a-z])(.+)$/gm, '<p style="margin:6px 0">$1</p>')
    .replace(/```[\s\S]*?```/g, (code) => `<pre style="background:#f8fafc;padding:8px;border-radius:4px;font-size:11px;overflow-x:auto">${code.replace(/```\w*/g, '').trim()}</pre>`);
}

type SortKey = "name" | "kind" | "size_bytes" | "updated_at";
type SortDir = "asc" | "desc";

/** Data files are raw outputs (JSON, CSV, artifact). Reports are formatted documents (PDF, Markdown). */
const DATA_KINDS  = new Set(["json_report", "table", "artifact"]);
const REPORT_KINDS = new Set(["pdf", "document"]);

export function ReportsView() {
  const [reports, setReports] = useState<CatalogReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [areaTab, setAreaTab] = useState<"data" | "reports" | "templates">("reports");
  const [search, setSearch] = useState("");
  const [kindFilter, setKindFilter] = useState<Set<string>>(new Set());
  const [expFilter, setExpFilter] = useState<Set<string>>(new Set());
  const [studyFilter, setStudyFilter] = useState<Set<string>>(new Set());
  const [sortKey, setSortKey] = useState<SortKey>("updated_at");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [groupByExp, setGroupByExp] = useState(true); // default on
  const [studies, setStudies] = useState<StudyResponse[]>([]);
  const [popupBlocked, setPopupBlocked] = useState<string | null>(null);
  // ── Generate PDF Report modal ─────────────────────────────────────────
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [templates, setTemplates] = useState<ReportTemplate[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");
  const [generating, setGenerating] = useState(false);
  const [generateMsg, setGenerateMsg] = useState<string | null>(null);

  const openGenerateModal = async () => {
    setGenerateMsg(null);
    setShowGenerateModal(true);
    try {
      const t = await listReportTemplates();
      setTemplates(t);
      if (t.length > 0) setSelectedTemplate(t[0].id);
    } catch { setTemplates([]); }
  };

  const handleGenerate = async () => {
    if (!selectedTemplate) return;
    setGenerating(true);
    setGenerateMsg(null);
    try {
      const r = await generateReport(selectedTemplate);
      setGenerateMsg(r.message);
      setTimeout(() => { setShowGenerateModal(false); setGenerateMsg(null); load(); }, 3000);
    } catch (e) {
      setGenerateMsg(e instanceof Error ? e.message : "Generation failed");
    } finally {
      setGenerating(false);
    }
  };

  // ── Compose mode ───────────────────────────────────────────────
  const [composeMode, setComposeMode] = useState(false);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  // AI Report generation
  const [aiReportLoading, setAiReportLoading] = useState(false);
  const [aiReportResult, setAiReportResult] = useState<{ title: string; markdown: string } | null>(null);

  const generateAiReport = async () => {
    const picked = reports.filter(r => selected.has(r.id));
    if (!picked.length) return;
    setAiReportLoading(true);
    try {
      // Fetch JSON content for each selected report
      const contents = await Promise.all(picked.map(async r => {
        const url = getReportDownloadUrl(r.id);
        try {
          const res = await fetch(url);
          if (res.ok) {
            const data = await res.json();
            return { name: r.name, filename: r.relative_path, data };
          }
        } catch { /* ignore */ }
        return { name: r.name, filename: r.relative_path, data: {} };
      }));
      const result = await aiReportSynthesis({
        report_contents: contents,
        title: picked.length === 1 ? `Analysis: ${picked[0].name}` : `Synthesis of ${picked.length} Reports`,
      });
      setAiReportResult(result);
    } catch (e) {
      alert(e instanceof Error ? e.message : "AI report generation failed. Check that a language model is configured in Settings.");
    } finally {
      setAiReportLoading(false);
    }
  };

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

  // Filter the catalog by the active area tab
  const areaFiltered = reports.filter(r =>
    areaTab === "data" ? DATA_KINDS.has(r.kind) : REPORT_KINDS.has(r.kind)
  );

  const dataCnt   = reports.filter(r => DATA_KINDS.has(r.kind)).length;
  const reportCnt = reports.filter(r => REPORT_KINDS.has(r.kind)).length;

  // ── Template editor state ───────────────────────────────────────────────
  const [userTemplates, setUserTemplates] = useState<UserReportTemplate[]>([]);
  const [tmplLoading, setTmplLoading] = useState(false);
  const [showNewTmpl, setShowNewTmpl] = useState(false);
  const [newTmplName, setNewTmplName] = useState("");
  const [newTmplCat, setNewTmplCat]   = useState("General");
  const [newTmplDesc, setNewTmplDesc] = useState("");
  const [newTmplSections, setNewTmplSections] = useState<ReportTemplateSection[]>([]);

  const loadUserTemplates = async () => {
    setTmplLoading(true);
    try { setUserTemplates(await listUserReportTemplates()); }
    catch { /* ignore */ }
    finally { setTmplLoading(false); }
  };

  const handleCreateTmpl = async () => {
    if (!newTmplName.trim()) return;
    try {
      const t = await createUserReportTemplate({
        name: newTmplName.trim(), description: newTmplDesc.trim(),
        category: newTmplCat, sections: newTmplSections,
      });
      setUserTemplates(prev => [t, ...prev]);
      setShowNewTmpl(false); setNewTmplName(""); setNewTmplDesc(""); setNewTmplSections([]);
    } catch { /* ignore */ }
  };

  const handleDeleteTmpl = async (id: string) => {
    if (!confirm("Delete this template?")) return;
    try { await deleteUserReportTemplate(id); setUserTemplates(prev => prev.filter(t => t.id !== id)); }
    catch { /* ignore */ }
  };

  const addSection = () => setNewTmplSections(prev => [
    ...prev,
    { title: "", data_source: "", data_key: "", chart_type: "table", include_table: true, description: "" },
  ]);

  const updateSection = (i: number, field: keyof ReportTemplateSection, val: unknown) =>
    setNewTmplSections(prev => prev.map((s, idx) => idx === i ? { ...s, [field]: val } : s));

  const sorted = [...areaFiltered]
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
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
        <h2 style={{ margin: 0 }}>Reports &amp; Data</h2>
        <div style={{ display: "flex", gap: 6 }}>
          <button
            onClick={() => void openGenerateModal()}
            style={{ ...btnStyle, padding: "4px 12px", fontSize: 12, background: "#16a34a" }}
            title="Generate a PDF report from experiment results"
          >
            📄 Generate Report
          </button>
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

      {/* Area tabs */}
      <div style={{ display: "flex", gap: 0, marginBottom: "0.75rem", borderBottom: "2px solid #e5e7eb" }}>
        {(["reports", "data", "templates"] as const).map(tab => (
          <button key={tab} onClick={() => { setAreaTab(tab); if (tab === "templates" && userTemplates.length === 0) void loadUserTemplates(); }}
            style={{ padding: "7px 18px", border: "none", background: "none", cursor: "pointer",
              fontSize: 13, fontWeight: areaTab === tab ? 700 : 400,
              color: areaTab === tab ? "#1e3a5f" : "#6b7280",
              borderBottom: areaTab === tab ? "2px solid #1e3a5f" : "2px solid transparent",
              marginBottom: "-2px", whiteSpace: "nowrap" }}>
            {tab === "reports"
              ? `📋 Reports ${reportCnt > 0 ? `(${reportCnt})` : ""}`
              : tab === "data"
              ? `📂 Data ${dataCnt > 0 ? `(${dataCnt})` : ""}`
              : `📝 Templates ${userTemplates.length > 0 ? `(${userTemplates.length})` : ""}`}
          </button>
        ))}
        <div style={{ flex: 1 }} />
        <span style={{ fontSize: 11, color: "#9ca3af", alignSelf: "center", paddingRight: 4 }}>
          {areaTab === "reports" ? "PDF & formatted documents"
            : areaTab === "data" ? "JSON results, CSV exports, raw artifacts"
            : "User-defined report templates (stored in database)"}
        </span>
      </div>

      {/* Templates editor panel */}
      {areaTab === "templates" && (
        <div style={{ padding: "0 0 24px" }}>
          <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
            <button onClick={() => { setShowNewTmpl(s => !s); setNewTmplSections([]); }}
              style={{ ...btnStyle, background: "#7c3aed", padding: "4px 14px", fontSize: 12 }}>
              + New Template
            </button>
            <button onClick={() => void loadUserTemplates()} style={{ ...btnStyle, background: "#6b7280", padding: "4px 12px", fontSize: 12 }}>⟳</button>
          </div>
          {showNewTmpl && (
            <div style={{ border: "1px solid #a78bfa", borderRadius: 8, padding: 16, marginBottom: 16, background: "#faf5ff" }}>
              <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 10, color: "#7c3aed" }}>📝 New Report Template</div>
              <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
                <div style={{ flex: 2 }}>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#374151", display: "block", marginBottom: 3 }}>Name</label>
                  <input value={newTmplName} onChange={e => setNewTmplName(e.target.value)}
                    placeholder="e.g. Fuls NW Semitic Report"
                    style={{ width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 12, boxSizing: "border-box" }} />
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#374151", display: "block", marginBottom: 3 }}>Category</label>
                  <input value={newTmplCat} onChange={e => setNewTmplCat(e.target.value)}
                    placeholder="General"
                    style={{ width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 12, boxSizing: "border-box" }} />
                </div>
              </div>
              <div style={{ marginBottom: 10 }}>
                <label style={{ fontSize: 11, fontWeight: 600, color: "#374151", display: "block", marginBottom: 3 }}>Description</label>
                <input value={newTmplDesc} onChange={e => setNewTmplDesc(e.target.value)}
                  placeholder="What this report covers…"
                  style={{ width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 12, boxSizing: "border-box" }} />
              </div>
              <div style={{ marginBottom: 10 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                  <label style={{ fontSize: 11, fontWeight: 600, color: "#374151" }}>Sections</label>
                  <button onClick={addSection} style={{ fontSize: 11, background: "#ede9fe", border: "none", borderRadius: 4, padding: "2px 8px", cursor: "pointer", color: "#7c3aed" }}>+ Add Section</button>
                </div>
                {newTmplSections.map((s, i) => (
                  <div key={i} style={{ display: "flex", gap: 6, marginBottom: 6, padding: "8px", background: "#fff", borderRadius: 4, border: "1px solid #e5e7eb" }}>
                    <input placeholder="Title" value={s.title} onChange={e => updateSection(i, "title", e.target.value)}
                      style={{ flex: 2, padding: "3px 6px", border: "1px solid #d1d5db", borderRadius: 3, fontSize: 11 }} />
                    <input placeholder="Data key" value={s.data_key} onChange={e => updateSection(i, "data_key", e.target.value)}
                      style={{ flex: 2, padding: "3px 6px", border: "1px solid #d1d5db", borderRadius: 3, fontSize: 11 }} />
                    <select value={s.chart_type} onChange={e => updateSection(i, "chart_type", e.target.value)}
                      style={{ padding: "3px 6px", border: "1px solid #d1d5db", borderRadius: 3, fontSize: 11 }}>
                      <option value="table">Table</option>
                      <option value="bar">Bar</option>
                      <option value="line">Line</option>
                      <option value="text">Text</option>
                    </select>
                    <button onClick={() => setNewTmplSections(prev => prev.filter((_, j) => j !== i))}
                      style={{ fontSize: 12, background: "none", border: "none", cursor: "pointer", color: "#dc2626" }}>×</button>
                  </div>
                ))}
                {newTmplSections.length === 0 && <p style={{ fontSize: 11, color: "#9ca3af" }}>No sections yet. Add one above.</p>}
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                <button onClick={() => void handleCreateTmpl()} disabled={!newTmplName.trim()}
                  style={{ ...btnStyle, background: "#7c3aed", padding: "5px 16px", fontSize: 12, opacity: newTmplName.trim() ? 1 : 0.4 }}>Create Template</button>
                <button onClick={() => setShowNewTmpl(false)}
                  style={{ ...btnStyle, background: "#6b7280", padding: "5px 14px", fontSize: 12 }}>Cancel</button>
              </div>
            </div>
          )}
          {tmplLoading && <p style={{ color: "#6b7280", fontSize: 13 }}>Loading…</p>}
          {!tmplLoading && userTemplates.length === 0 && (
            <div style={{ padding: "20px", border: "2px dashed #e5e7eb", borderRadius: 8, textAlign: "center", color: "#9ca3af" }}>
              <div style={{ fontSize: 32, marginBottom: 8 }}>📝</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>No report templates yet</div>
              <div style={{ fontSize: 12 }}>Create a template to define reusable report structures for your experiments.</div>
            </div>
          )}
          {userTemplates.map(t => (
            <div key={t.id} style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: "12px 16px", marginBottom: 8, background: "#fff" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 700, fontSize: 13 }}>{t.name}</div>
                  <div style={{ fontSize: 11, color: "#6b7280" }}>{t.category} · {t.sections.length} section{t.sections.length !== 1 ? "s" : ""} · {t.description}</div>
                </div>
                <button onClick={() => void handleDeleteTmpl(t.id)}
                  style={{ fontSize: 11, border: "1px solid #fca5a5", borderRadius: 4, padding: "2px 8px", background: "none", cursor: "pointer", color: "#dc2626" }}>
                  Delete
                </button>
              </div>
              {t.sections.length > 0 && (
                <div style={{ marginTop: 6, display: "flex", gap: 4, flexWrap: "wrap" }}>
                  {t.sections.map((s, i) => (
                    <span key={i} style={{ fontSize: 10, padding: "2px 8px", borderRadius: 10,
                      background: "#f3f4f6", color: "#374151" }}>{s.title || `Section ${i+1}`} ({s.chart_type})</span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Generate Report Modal */}
      {showGenerateModal && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.45)", zIndex: 9000,
                      display: "flex", alignItems: "center", justifyContent: "center" }}
             onClick={() => setShowGenerateModal(false)}>
          <div style={{ background: "#fff", borderRadius: 10, padding: 28, maxWidth: 560, width: "90%",
                        boxShadow: "0 20px 60px rgba(0,0,0,0.25)" }}
               onClick={(e) => e.stopPropagation()}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
              <h3 style={{ margin: 0, fontSize: 16, color: "#111827" }}>📄 Generate PDF Report</h3>
              <button onClick={() => setShowGenerateModal(false)}
                style={{ border: "none", background: "none", fontSize: 20, cursor: "pointer", color: "#9ca3af" }}>×</button>
            </div>
            <p style={{ fontSize: 12, color: "#6b7280", margin: "0 0 16px" }}>
              Select a template. The corresponding experiments must have been run first.
              The PDF will appear in the Reports list when complete, and the job will show in the Jobs panel.
            </p>
            {templates.length === 0
              ? <p style={{ color: "#9ca3af", fontSize: 13 }}>Loading templates…</p>
              : (
                <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 20 }}>
                  {templates.map((t) => (
                    <label key={t.id} style={{
                      display: "flex", alignItems: "flex-start", gap: 10, padding: "10px 14px",
                      border: `2px solid ${selectedTemplate === t.id ? "#16a34a" : "#e5e7eb"}`,
                      borderRadius: 8, cursor: "pointer",
                      background: selectedTemplate === t.id ? "#f0fdf4" : "#fafafa",
                    }}>
                      <input type="radio" name="template" value={t.id}
                        checked={selectedTemplate === t.id}
                        onChange={() => setSelectedTemplate(t.id)}
                        style={{ marginTop: 2 }} />
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 700, fontSize: 13, color: "#111827" }}>
                          {t.name}
                          {!t.ready && (
                            <span style={{ marginLeft: 8, fontSize: 10, color: "#d97706",
                                           background: "#fef3c7", padding: "1px 6px", borderRadius: 4 }}>
                              ⚠ run experiments first
                            </span>
                          )}
                        </div>
                        <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>{t.description}</div>
                        <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 2 }}>{t.category}</div>
                      </div>
                    </label>
                  ))}
                </div>
              )}
            {generateMsg && (
              <div style={{ padding: "8px 12px", borderRadius: 6, marginBottom: 12, fontSize: 12,
                             background: generateMsg.includes("fail") || generateMsg.includes("Cannot")
                               ? "#fef2f2" : "#f0fdf4",
                             color: generateMsg.includes("fail") || generateMsg.includes("Cannot")
                               ? "#dc2626" : "#16a34a" }}>
                {generateMsg}
              </div>
            )}
            <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
              <button onClick={() => setShowGenerateModal(false)}
                style={{ padding: "6px 16px", border: "1px solid #d1d5db", borderRadius: 4, background: "#fff",
                         fontSize: 13, cursor: "pointer", color: "#374151" }}>Cancel</button>
              <button
                onClick={() => void handleGenerate()}
                disabled={!selectedTemplate || generating}
                style={{ padding: "6px 20px", background: generating ? "#6b7280" : "#16a34a",
                         color: "#fff", border: "none", borderRadius: 4, fontSize: 13,
                         cursor: generating ? "not-allowed" : "pointer", fontWeight: 600 }}>
                {generating ? "⏳ Generating…" : "Generate PDF"}
              </button>
            </div>
          </div>
        </div>
      )}
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
            onClick={() => void generateAiReport()}
            disabled={selected.size === 0 || aiReportLoading}
            style={{ ...btnStyle, padding: "5px 14px", fontSize: 12,
              background: selected.size > 0 && !aiReportLoading ? "#2563eb" : "#d1d5db",
              cursor: selected.size > 0 && !aiReportLoading ? "pointer" : "not-allowed" }}>
            {aiReportLoading ? "⏳ Generating…" : "🤖 AI Report"}
          </button>
          <button
            onClick={() => void exportComposedPdf()}
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

      {/* AI Report Modal */}
      {aiReportResult && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.55)", zIndex: 10000, display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}
          onClick={() => setAiReportResult(null)}>
          <div style={{ background: "#fff", borderRadius: 10, maxWidth: 860, width: "100%", maxHeight: "85vh",
            display: "flex", flexDirection: "column", boxShadow: "0 20px 60px rgba(0,0,0,0.4)" }}
            onClick={e => e.stopPropagation()}>
            {/* Modal header */}
            <div style={{ padding: "14px 20px", borderBottom: "1px solid #e5e7eb", display: "flex", alignItems: "center", gap: 10, flexShrink: 0 }}>
              <span style={{ fontSize: 15, fontWeight: 700, color: "#1e3a5f", flex: 1 }}>🤖 {aiReportResult.title}</span>
              <button
                onClick={() => {
                  const html = renderMarkdown(aiReportResult.markdown);
                  const win = window.open("", "_blank", "width=860,height=900");
                  if (!win) { alert("Allow popups to export PDF"); return; }
                  win.document.write(
                    `<!DOCTYPE html><html><head><title>${aiReportResult.title}</title>` +
                    `<style>body{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;font-size:13px;line-height:1.7;color:#111}` +
                    `table{border-collapse:collapse;width:100%}td,th{border:1px solid #e5e7eb;padding:5px 10px}` +
                    `@media print{body{margin:10px 20px}}` +
                    `</style></head><body>` +
                    `<h1 style="font-size:20px;margin-bottom:4px">${aiReportResult.title}</h1>` +
                    `<p style="color:#9ca3af;font-size:11px">Generated by Glossa AI · ${new Date().toLocaleString()}</p>` +
                    `<hr style="border:none;border-top:2px solid #e5e7eb;margin:16px 0">` +
                    html +
                    `<script>setTimeout(()=>window.print(),600)</script></body></html>`
                  );
                  win.document.close();
                }}
                style={{ padding: "5px 14px", border: "none", borderRadius: 6, background: "#7c3aed", color: "#fff", cursor: "pointer", fontSize: 12, fontWeight: 600 }}>
                📄 Export PDF
              </button>
              <button onClick={() => setAiReportResult(null)}
                style={{ border: "none", background: "none", cursor: "pointer", fontSize: 18, color: "#9ca3af" }}>×</button>
            </div>
            {/* Modal body — rendered markdown */}
            <div style={{ padding: "16px 24px", overflowY: "auto", flex: 1 }}
              dangerouslySetInnerHTML={{ __html: renderMarkdown(aiReportResult.markdown) }} />
          </div>
        </div>
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
