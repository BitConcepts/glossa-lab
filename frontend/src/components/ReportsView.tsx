/**
 * Reports & ledger — Spec 081 (wireframe 12), replacing the old
 * file-browser ReportsView in place (route id "reports" unchanged).
 *
 * Reports are what the program said; the ledger is what it did. The
 * reports list is the instance's report catalog presented as
 * title / state / meta / Open; the study register (the program
 * record's own list, PR #443 endpoint) and the program-items list
 * ride below it. The Ledger tab states the ledger's terms and where
 * the record lives — this instance exposes no ledger endpoint, so no
 * entries are shown and none are invented (Leg B delta D1: explicit
 * instance states, never fake data).
 *
 * Retired with this surface (backend endpoints untouched): compose
 * mode, the AI report-synthesis UI, star pins, the user-template
 * editor UI, and the delete / open-folder buttons. The two report
 * template families (built-in /reports/templates and user
 * /report-templates) stay labelled as separate families in the
 * Generate dialog — never silently merged (Leg B delta D5).
 */

import { useEffect, useState } from "react";
import {
  listReports, getReportDownloadUrl,
  listReportTemplates, generateReport,
  listUserReportTemplates,
  type CatalogReport, type ReportTemplate, type UserReportTemplate,
} from "../api";
import { useProject } from "../hooks/useProject";
import { fmtDateTimeCompact } from "../dateFormat";
import {
  Card, CardTitle, Chip, PageHead, palette, PrimaryButton, QuietButton,
  RowItem, RowMeta, RowTitle, SmallButton, TabsRow, type Palette,
} from "./ui081";
import { StudyRegister } from "./StudyRegister";

const KIND_LABEL: Record<string, string> = {
  report: "PDF Report",
  data: "Data",
  document: "Document",
};

function fmtSize(b: number): string {
  return b > 1_000_000
    ? `${(b / 1_000_000).toFixed(1)} MB`
    : b > 1_000
      ? `${(b / 1_000).toFixed(0)} KB`
      : `${b} B`;
}

function ReportRow({ p, r, onOpen }: { p: Palette; r: CatalogReport; onOpen: (r: CatalogReport) => void }) {
  return (
    <RowItem p={p}>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
          <RowTitle p={p}><span style={{ overflowWrap: "anywhere" }}>{r.name}</span></RowTitle>
          <Chip tone="line">{KIND_LABEL[r.kind] ?? r.kind}</Chip>
          {r.experiment_id && <Chip tone="neutral">{r.experiment_id.replace(/_/g, " ")}</Chip>}
        </div>
        <RowMeta p={p} style={{ overflowWrap: "anywhere" }}>
          {r.relative_path} · {fmtSize(r.size_bytes)} · updated {fmtDateTimeCompact(r.updated_at)}
        </RowMeta>
      </div>
      <SmallButton onClick={() => onOpen(r)}>Open</SmallButton>
    </RowItem>
  );
}

export function ReportsView({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const { activeProject } = useProject();
  const projectId = activeProject?.id ?? null;

  const [tab, setTab] = useState<"reports" | "ledger">("reports");
  const [reports, setReports] = useState<CatalogReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [popupBlocked, setPopupBlocked] = useState<string | null>(null);

  // ── Generate report dialog (the wireframe's primary action) ──────
  const [showGenerate, setShowGenerate] = useState(false);
  const [templates, setTemplates] = useState<ReportTemplate[]>([]);
  const [userTemplates, setUserTemplates] = useState<UserReportTemplate[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState("");
  const [generating, setGenerating] = useState(false);
  const [generateMsg, setGenerateMsg] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      setReports(await listReports(projectId));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load reports");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void load(); }, [projectId]); // eslint-disable-line react-hooks/exhaustive-deps

  // Jobs 'Results' navigation lands here with a filename to surface.
  useEffect(() => {
    const handler = (e: Event) => {
      const d = (e as CustomEvent<{ search?: string }>).detail;
      if (d?.search) {
        setTab("reports");
        setSearch(d.search);
      }
      window.scrollTo({ top: 0, behavior: "smooth" });
    };
    window.addEventListener("glossa:reports_highlight", handler);
    return () => window.removeEventListener("glossa:reports_highlight", handler);
  }, []);

  const handleOpen = (r: CatalogReport) => {
    const url = getReportDownloadUrl(r.id);
    const popup = window.open(
      url,
      `glossa_report_${r.id}`,
      "width=1100,height=800,menubar=no,toolbar=no,location=no,status=no,scrollbars=yes,resizable=yes",
    );
    if (!popup || popup.closed || typeof popup.closed === "undefined") {
      setPopupBlocked(url);
    } else {
      popup.focus();
      setPopupBlocked(null);
    }
  };

  const openGenerate = async () => {
    setGenerateMsg(null);
    setShowGenerate(true);
    try {
      const t = await listReportTemplates();
      setTemplates(t);
      if (t.length > 0) setSelectedTemplate(t[0].id);
    } catch { setTemplates([]); }
    try {
      setUserTemplates(await listUserReportTemplates());
    } catch { setUserTemplates([]); }
  };

  const handleGenerate = async () => {
    if (!selectedTemplate) return;
    setGenerating(true);
    setGenerateMsg(null);
    try {
      const r = await generateReport(selectedTemplate);
      setGenerateMsg(r.message);
      setTimeout(() => { setShowGenerate(false); setGenerateMsg(null); void load(); }, 3000);
    } catch (e) {
      setGenerateMsg(e instanceof Error ? e.message : "Generation failed");
    } finally {
      setGenerating(false);
    }
  };

  const visible = reports.filter(
    (r) => !search || r.name.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div>
      <PageHead
        p={p}
        title="Reports & ledger"
        lede={
          <>
            What the program has produced, and the record of how it got there. The{" "}
            <b>ledger</b> is append-only: an entry is never edited or deleted — a
            correction is a new entry that names the old one. No ledger entry, no
            claim that the work happened.
          </>
        }
        primary={<PrimaryButton onClick={() => void openGenerate()}>+ Generate report</PrimaryButton>}
      />

      <TabsRow
        p={p}
        tabs={[
          { id: "reports" as const, label: "Reports" },
          { id: "ledger" as const, label: "Ledger" },
        ]}
        active={tab}
        onSelect={setTab}
      />

      {tab === "reports" && (
        <div style={{ display: "grid", gap: 16, minWidth: 0 }}>
          <Card p={p} style={{ minWidth: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap", marginBottom: 4 }}>
              <div style={{ flex: "1 1 140px", minWidth: 0 }}>
                <CardTitle p={p} sub="This instance's report catalog — what the program has produced, newest state first.">
                  Reports
                </CardTitle>
              </div>
              <input
                aria-label="Search reports"
                placeholder="Search reports…"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{
                  padding: "6px 10px", border: `1px solid ${p.border}`, borderRadius: 6,
                  fontSize: 12, width: 200, flex: "0 1 200px", minWidth: 120,
                  background: p.inputBg, color: p.fg,
                }}
              />
              <SmallButton onClick={() => void load()}>⟳ Refresh</SmallButton>
            </div>

            {popupBlocked && (
              <div style={{
                padding: "10px 14px", margin: "8px 0", borderRadius: 8,
                background: darkMode ? "#3f1d1d" : "#fef2f2",
                border: `1px solid ${p.bad}`, color: p.fg, fontSize: 12.5,
              }}>
                Popups are blocked by your browser, so the report could not open in
                a new window.{" "}
                <a href={popupBlocked} target="_blank" rel="noopener noreferrer" style={{ color: p.accent, fontWeight: 600 }}>
                  Open it in a new tab instead →
                </a>{" "}
                <button onClick={() => setPopupBlocked(null)} style={{ border: "none", background: "none", cursor: "pointer", color: p.muted, fontSize: 14 }}>×</button>
              </div>
            )}

            {loading && <RowMeta p={p}>Loading reports…</RowMeta>}
            {error && (
              <RowMeta p={p} style={{ color: p.bad }}>
                The report catalog could not be loaded from this instance ({error}).{" "}
                <button onClick={() => void load()} style={{ background: "none", border: "none", cursor: "pointer", color: p.accent, textDecoration: "underline", fontSize: 12 }}>
                  Retry
                </button>
              </RowMeta>
            )}
            {!loading && !error && reports.length === 0 && (
              <p data-testid="reports-empty-state" style={{ color: p.muted, fontSize: 13, margin: "8px 0" }}>
                No reports yet. Run an experiment to generate one, or use Generate
                report to build one from a template.
              </p>
            )}
            {!loading && !error && reports.length > 0 && visible.length === 0 && (
              <p data-testid="reports-empty-state" style={{ color: p.muted, fontSize: 13, margin: "8px 0" }}>
                No reports match “{search}”. Clear the search to see all {reports.length}.
              </p>
            )}
            {!loading && !error && visible.length > 0 && (
              <div>
                {visible.map((r) => (
                  <ReportRow key={r.relative_path} p={p} r={r} onOpen={handleOpen} />
                ))}
              </div>
            )}
          </Card>

          <StudyRegister darkMode={darkMode} />
        </div>
      )}

      {tab === "ledger" && (
        <Card p={p}>
          <CardTitle p={p} sub="append-only; a correction is a new entry that names the old one">
            Ledger — latest entries
          </CardTitle>
          <RowMeta p={p} style={{ maxWidth: "72ch" }}>
            The ledger is the program's continuity record: every landed change
            appends an entry to <b>LEDGER.md</b> at the repo root, and no entry is
            ever edited or deleted. This instance exposes no ledger endpoint, so
            entries are not listed here yet — the record itself is complete and
            current in LEDGER.md; this surface will read it when an endpoint
            serves it. Nothing is shown rather than anything invented.
          </RowMeta>
        </Card>
      )}

      {/* Generate report dialog */}
      {showGenerate && (
        <div
          style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.45)", zIndex: 9000, display: "flex", alignItems: "center", justifyContent: "center" }}
          onClick={() => setShowGenerate(false)}
        >
          <div
            style={{ background: p.card, borderRadius: 10, padding: 28, maxWidth: 560, width: "90%", boxShadow: "0 20px 60px rgba(0,0,0,0.25)", maxHeight: "85vh", overflowY: "auto" }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
              <h3 style={{ margin: 0, fontSize: 16, color: p.fg }}>Generate report</h3>
              <button onClick={() => setShowGenerate(false)} style={{ border: "none", background: "none", fontSize: 20, cursor: "pointer", color: p.muted }}>×</button>
            </div>
            <p style={{ fontSize: 12, color: p.muted, margin: "0 0 16px" }}>
              Select a built-in template. The corresponding experiments must have
              been run first. The report appears in the Reports list when complete,
              and the job shows in the Jobs panel.
            </p>

            <div style={{ fontSize: 11, fontWeight: 700, color: p.muted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>
              Built-in templates
            </div>
            {templates.length === 0
              ? <p style={{ color: p.muted, fontSize: 13 }}>Loading templates…</p>
              : (
                <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 20 }}>
                  {templates.map((t) => (
                    <label key={t.id} style={{
                      display: "flex", alignItems: "flex-start", gap: 10, padding: "10px 14px",
                      border: `2px solid ${selectedTemplate === t.id ? "#16a34a" : p.border}`,
                      borderRadius: 8, cursor: "pointer",
                      background: selectedTemplate === t.id ? (darkMode ? "#14532d33" : "#f0fdf4") : "transparent",
                    }}>
                      <input type="radio" name="template" value={t.id}
                        checked={selectedTemplate === t.id}
                        onChange={() => setSelectedTemplate(t.id)}
                        style={{ marginTop: 2 }} />
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 700, fontSize: 13, color: p.fg }}>
                          {t.name}
                          {!t.ready && (
                            <span style={{ marginLeft: 8, fontSize: 10, color: "#b45309", background: "#fef3c7", padding: "1px 6px", borderRadius: 4 }}>
                              ⚠ run experiments first
                            </span>
                          )}
                        </div>
                        <div style={{ fontSize: 11, color: p.muted, marginTop: 2 }}>{t.description}</div>
                        <div style={{ fontSize: 10, color: p.faint, marginTop: 2 }}>{t.category}</div>
                      </div>
                    </label>
                  ))}
                </div>
              )}

            {userTemplates.length > 0 && (
              <>
                <div style={{ fontSize: 11, fontWeight: 700, color: p.muted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>
                  Your templates
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 6, marginBottom: 20 }}>
                  {userTemplates.map((t) => (
                    <div key={t.id} style={{ padding: "8px 14px", border: `1px solid ${p.border}`, borderRadius: 8 }}>
                      <div style={{ fontWeight: 600, fontSize: 13, color: p.fg }}>{t.name}</div>
                      <div style={{ fontSize: 11, color: p.muted, marginTop: 2 }}>
                        {t.category} · {t.sections.length} section{t.sections.length !== 1 ? "s" : ""} · {t.description}
                      </div>
                    </div>
                  ))}
                  <p style={{ fontSize: 11, color: p.faint, margin: "2px 0 0" }}>
                    Your templates are a separate family from the built-in set and
                    are never merged into it. Generation runs from built-in
                    templates; the in-app template editor was retired with this
                    redesign — your templates remain stored and available via the API.
                  </p>
                </div>
              </>
            )}

            {generateMsg && (
              <div style={{
                padding: "8px 12px", borderRadius: 6, marginBottom: 12, fontSize: 12,
                background: generateMsg.includes("fail") || generateMsg.includes("Cannot") ? "#fef2f2" : "#f0fdf4",
                color: generateMsg.includes("fail") || generateMsg.includes("Cannot") ? "#b91c1c" : "#15803d",
              }}>
                {generateMsg}
              </div>
            )}
            <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
              <QuietButton onClick={() => setShowGenerate(false)}>Cancel</QuietButton>
              <PrimaryButton onClick={() => void handleGenerate()} disabled={!selectedTemplate || generating}>
                {generating ? "⏳ Generating…" : "Generate PDF"}
              </PrimaryButton>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
