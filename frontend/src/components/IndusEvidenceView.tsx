/**
 * IndusEvidenceView — three-tab workspace for the Glossa-Lab Indus Evidence Graph.
 *
 *  Library   — registered papers, PDF upload, URL import
 *  Claims    — extracted claims with filters
 *  Sweep     — sweep config editor, run sweep, import candidates
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  getIndusSweepCandidates,
  getIndusSweepConfig,
  intakeSweepCandidate,
  importIndusUrl,
  listIndusClaims,
  listIndusHypotheses,
  listIndusLibrary,
  runIndusIntake,
  runIndusSweep,
  saveIndusSweepConfig,
  uploadIndusPaper,
  type IndusClaim,
  type IndusDoc,
  type IndusHypothesisModel,
  type SweepCandidate,
  type SweepConfig,
} from "../api";
import { useToast } from "../hooks/useToast";

// ── Helpers ────────────────────────────────────────────────────────────────

function fmtBytes(b: number): string {
  if (!b) return "–";
  if (b < 1024) return `${b} B`;
  if (b < 1024 * 1024) return `${Math.round(b / 1024)} KB`;
  return `${(b / 1024 / 1024).toFixed(1)} MB`;
}

function fmtDate(s: string): string {
  if (!s) return "–";
  return s.slice(0, 10);
}

const STATUS_COLORS: Record<string, string> = {
  strongly_supported:  "#16a34a",
  partially_supported: "#4ade80",
  partially_falsified: "#f97316",
  contradicted:        "#dc2626",
  untested:            "#64748b",
  unregistered:        "#64748b",
};

// ── Main component ────────────────────────────────────────────────────────

type EvidenceTab = "library" | "claims" | "sweep";

export function IndusEvidenceView({ darkMode = true }: { darkMode?: boolean }) {
  const [activeTab, setActiveTab] = useState<EvidenceTab>("library");
  const { toast } = useToast();

  const bg     = darkMode ? "#0f172a" : "#f8fafc";
  const cardBg = darkMode ? "#1e293b" : "#ffffff";
  const border = darkMode ? "#334155" : "#e5e7eb";
  const fg     = darkMode ? "#e2e8f0" : "#111827";
  const muted  = darkMode ? "#94a3b8" : "#6b7280";
  const inputBg = darkMode ? "#0f172a" : "#ffffff";
  const inputBdr = darkMode ? "#334155" : "#d1d5db";

  const tabStyle = (t: EvidenceTab): React.CSSProperties => ({
    padding: "7px 18px",
    border: "none",
    borderBottom: `2px solid ${activeTab === t ? "#7c3aed" : "transparent"}`,
    background: "none",
    cursor: "pointer",
    fontSize: 13,
    fontWeight: activeTab === t ? 700 : 400,
    color: activeTab === t ? "#7c3aed" : muted,
    transition: "all 0.12s",
  });

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", background: bg, color: fg }}>
      {/* Header */}
      <div style={{ padding: "16px 24px 0", borderBottom: `1px solid ${border}`, flexShrink: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
          <span style={{ fontSize: 20 }}>🗂️</span>
          <div>
            <div style={{ fontSize: 16, fontWeight: 700, color: fg }}>Evidence Graph</div>
            <div style={{ fontSize: 11, color: muted }}>Indus Script Literature — Claims — Sweep</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 4 }}>
          {(["library", "claims", "sweep"] as EvidenceTab[]).map(t => (
            <button key={t} style={tabStyle(t)} onClick={() => setActiveTab(t)}>
              {t === "library" ? "📚 Library" : t === "claims" ? "🔖 Claims" : "🔭 Sweep"}
            </button>
          ))}
        </div>
      </div>

      {/* Tab content */}
      <div style={{ flex: 1, minHeight: 0, overflowY: "auto", padding: "20px 24px" }}>
        {activeTab === "library" && (
          <LibraryTab darkMode={darkMode} cardBg={cardBg} border={border} fg={fg} muted={muted}
            inputBg={inputBg} inputBdr={inputBdr} toast={toast} />
        )}
        {activeTab === "claims" && (
          <ClaimsTab darkMode={darkMode} cardBg={cardBg} border={border} fg={fg} muted={muted}
            inputBg={inputBg} inputBdr={inputBdr} />
        )}
        {activeTab === "sweep" && (
          <SweepTab darkMode={darkMode} cardBg={cardBg} border={border} fg={fg} muted={muted}
            inputBg={inputBg} inputBdr={inputBdr} toast={toast} />
        )}
      </div>
    </div>
  );
}

// ── Library Tab ────────────────────────────────────────────────────────────

function LibraryTab({ darkMode, cardBg, border, fg, muted, inputBg, inputBdr, toast }: {
  darkMode: boolean; cardBg: string; border: string; fg: string; muted: string;
  inputBg: string; inputBdr: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toast: (msg: string, kind?: any) => void;
}) {
  const [docs, setDocs] = useState<IndusDoc[]>([]);
  const [hypos, setHypos] = useState<IndusHypothesisModel[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState("");
  const [urlInput, setUrlInput] = useState("");
  const [urlBusy, setUrlBusy] = useState(false);
  const [intakeBusy, setIntakeBusy] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const reload = useCallback(async () => {
    setLoading(true);
    try {
      const [lib, hyp] = await Promise.all([
        listIndusLibrary({ q: q || undefined, limit: 100 }),
        listIndusHypotheses(),
      ]);
      setDocs(lib.documents);
      setTotal(lib.total);
      setHypos(hyp.models);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  }, [q]);

  useEffect(() => { void reload(); }, [reload]);

  const handleFiles = async (files: FileList) => {
    for (const file of Array.from(files)) {
      if (!file.name.toLowerCase().endsWith(".pdf")) {
        toast(`${file.name}: only PDFs supported`, "error"); continue;
      }
      try {
        const res = await uploadIndusPaper(file);
        if (res.ok) {
          toast(`Uploaded ${file.name} — intake queued`, "success");
          setTimeout(() => void reload(), 2000);
        } else {
          const j = await res.json().catch(() => ({}));
          toast(`Upload failed: ${(j as { detail?: string }).detail ?? res.statusText}`, "error");
        }
      } catch (e) { toast(String(e), "error"); }
    }
  };

  const handleImportUrl = async () => {
    if (!urlInput.trim()) return;
    setUrlBusy(true);
    try {
      const r = await importIndusUrl({ url: urlInput.trim() });
      toast(r.message, "success");
      setUrlInput("");
      setTimeout(() => void reload(), 2000);
    } catch (e) { toast(String(e), "error"); }
    finally { setUrlBusy(false); }
  };

  const handleRunIntake = async () => {
    setIntakeBusy(true);
    try {
      const r = await runIndusIntake();
      toast(r.message, "info");
      setTimeout(() => void reload(), 3000);
    } catch (e) { toast(String(e), "error"); }
    finally { setIntakeBusy(false); }
  };

  const inpStyle: React.CSSProperties = {
    padding: "7px 10px", border: `1px solid ${inputBdr}`, borderRadius: 6,
    fontSize: 12, background: inputBg, color: fg, outline: "none", width: "100%", boxSizing: "border-box",
  };

  return (
    <div>
      {/* Stats row */}
      <div style={{ display: "flex", gap: 16, marginBottom: 20, flexWrap: "wrap" }}>
        {[
          { label: "Registered Papers", value: total },
          { label: "Hypothesis Models", value: hypos.length },
          { label: "Encoded Models", value: hypos.filter(h => h.status !== "stub").length },
        ].map(s => (
          <div key={s.label} style={{ background: cardBg, border: `1px solid ${border}`, borderRadius: 9, padding: "12px 18px", minWidth: 140 }}>
            <div style={{ fontSize: 22, fontWeight: 700, color: "#7c3aed" }}>{s.value}</div>
            <div style={{ fontSize: 11, color: muted, marginTop: 2 }}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Upload dropzone */}
      <div
        onDragOver={e => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={e => { e.preventDefault(); setDragOver(false); if (e.dataTransfer.files.length) void handleFiles(e.dataTransfer.files); }}
        onClick={() => fileRef.current?.click()}
        style={{
          border: `2px dashed ${dragOver ? "#7c3aed" : border}`,
          borderRadius: 10, padding: "20px 16px",
          textAlign: "center", cursor: "pointer",
          background: dragOver ? (darkMode ? "#1e1040" : "#f5f3ff") : cardBg,
          marginBottom: 16, transition: "all 0.12s",
        }}
      >
        <div style={{ fontSize: 28, marginBottom: 6 }}>📄</div>
        <div style={{ fontSize: 13, fontWeight: 600, color: fg }}>Drop PDF papers here</div>
        <div style={{ fontSize: 11, color: muted, marginTop: 3 }}>or click to browse · PDF files only</div>
        <input ref={fileRef} type="file" accept=".pdf" multiple style={{ display: "none" }}
          onChange={e => { if (e.target.files?.length) { void handleFiles(e.target.files); e.target.value = ""; }}} />
      </div>

      {/* URL import */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input value={urlInput} onChange={e => setUrlInput(e.target.value)}
          onKeyDown={e => { if (e.key === "Enter") void handleImportUrl(); }}
          placeholder="Import from URL (direct PDF link)…"
          style={{ ...inpStyle, flex: 1 }} />
        <button onClick={() => void handleImportUrl()} disabled={urlBusy || !urlInput.trim()}
          style={{ padding: "7px 14px", border: "none", borderRadius: 6, background: "#7c3aed", color: "#fff",
            cursor: "pointer", fontSize: 12, fontWeight: 600, opacity: (urlBusy || !urlInput.trim()) ? 0.5 : 1 }}>
          {urlBusy ? "…" : "Import"}
        </button>
        <button onClick={() => void handleRunIntake()} disabled={intakeBusy}
          title="Re-run intake + claims extraction on all registered docs"
          style={{ padding: "7px 14px", border: `1px solid ${border}`, borderRadius: 6, background: "none",
            color: muted, cursor: "pointer", fontSize: 12, opacity: intakeBusy ? 0.5 : 1 }}>
          {intakeBusy ? "⏳" : "⟳ Re-run intake"}
        </button>
      </div>

      {/* Search */}
      <div style={{ marginBottom: 16 }}>
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search papers…" style={inpStyle} />
      </div>

      {/* Paper list */}
      {loading && <div style={{ color: muted, fontSize: 12 }}>Loading…</div>}
      {!loading && docs.length === 0 && (
        <div style={{ color: muted, fontSize: 12, fontStyle: "italic" }}>
          No papers registered yet. Upload PDFs or run the intake pipeline.
        </div>
      )}
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {docs.map(doc => (
          <div key={doc.document_id} style={{ background: cardBg, border: `1px solid ${border}`, borderRadius: 9, padding: "12px 16px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: fg, marginBottom: 2 }}>
                  {doc.title || doc.document_id}
                </div>
                {doc.authors.length > 0 && (
                  <div style={{ fontSize: 11, color: muted }}>
                    {doc.authors.join(", ")} {doc.year ? `(${doc.year})` : ""}
                    {doc.doi ? ` · DOI: ${doc.doi}` : ""}
                  </div>
                )}
              </div>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 4, flexShrink: 0 }}>
                <span style={{ fontSize: 9, padding: "2px 7px", borderRadius: 8,
                  background: doc.claim_count > 0 ? "#7c3aed22" : "#f1f5f9",
                  color: doc.claim_count > 0 ? "#7c3aed" : muted, fontWeight: 700 }}>
                  {doc.claim_count} claims
                </span>
                <span style={{ fontSize: 9, color: muted }}>{fmtBytes(doc.file_size_bytes)} · {fmtDate(doc.intake_date)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Hypothesis models */}
      {hypos.length > 0 && (
        <div style={{ marginTop: 28 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: fg, marginBottom: 12 }}>Hypothesis Models</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {hypos.map(h => (
              <div key={h.file} style={{ background: cardBg, border: `1px solid ${border}`, borderRadius: 8,
                padding: "10px 14px", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: fg }}>{h.model_name || h.model_id}</div>
                  <div style={{ fontSize: 10, color: muted }}>{h.model_type} · {h.n_claims} claims · {h.n_tests} tests planned</div>
                </div>
                <span style={{ fontSize: 9, padding: "2px 8px", borderRadius: 8,
                  background: h.status === "stub" ? "#f1f5f9" : "#d1fae522",
                  color: h.status === "stub" ? muted : "#16a34a", fontWeight: 700 }}>
                  {h.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Claims Tab ─────────────────────────────────────────────────────────────

function ClaimsTab({ cardBg, border, fg, muted, inputBg, inputBdr }: {
  darkMode: boolean; cardBg: string; border: string; fg: string; muted: string;
  inputBg: string; inputBdr: string;
}) {
  const [claims, setClaims] = useState<IndusClaim[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [signFilter, setSignFilter] = useState("");
  const [expanded, setExpanded] = useState<Set<string>>(new Set());

  const reload = useCallback(async () => {
    setLoading(true);
    try {
      const r = await listIndusClaims({
        q: q || undefined,
        claim_type: typeFilter || undefined,
        claim_status: statusFilter || undefined,
        sign: signFilter || undefined,
        limit: 200,
      });
      setClaims(r.claims);
      setTotal(r.total);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  }, [q, typeFilter, statusFilter, signFilter]);

  useEffect(() => { void reload(); }, [reload]);

  const inpStyle: React.CSSProperties = {
    padding: "6px 9px", border: `1px solid ${inputBdr}`, borderRadius: 5,
    fontSize: 11, background: inputBg, color: fg, outline: "none",
  };

  const toggleExpand = (id: string) => {
    setExpanded(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  // Collect unique claim types and statuses for filter dropdowns
  const claimTypes = [...new Set(claims.map(c => c.claim_type))].sort();
  const claimStatuses = [...new Set(claims.map(c => c.claim_status))].sort();

  return (
    <div>
      {/* Stats */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16, alignItems: "center", flexWrap: "wrap" }}>
        <span style={{ fontSize: 12, color: muted }}>
          {loading ? "Loading…" : `${total} total claims`}
        </span>
        <div style={{ flex: 1 }} />
        <input value={q} onChange={e => setQ(e.target.value)}
          placeholder="Search claim text…" style={{ ...inpStyle, width: 200 }} />
        <select value={typeFilter} onChange={e => setTypeFilter(e.target.value)} style={{ ...inpStyle }}>
          <option value="">All types</option>
          {claimTypes.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)} style={{ ...inpStyle }}>
          <option value="">All statuses</option>
          {claimStatuses.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <input value={signFilter} onChange={e => setSignFilter(e.target.value)}
          placeholder="Filter by sign…" style={{ ...inpStyle, width: 120 }} />
      </div>

      {claims.length === 0 && !loading && (
        <div style={{ color: muted, fontSize: 12, fontStyle: "italic" }}>
          No claims match the current filters.
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {claims.map(c => {
          const isExp = expanded.has(c.claim_id);
          const statusColor = STATUS_COLORS[c.claim_status] ?? "#64748b";
          return (
            <div key={c.claim_id} style={{ background: cardBg, border: `1px solid ${border}`,
              borderRadius: 8, overflow: "hidden" }}>
              <div style={{ padding: "10px 14px", cursor: "pointer", display: "flex", gap: 10, alignItems: "flex-start" }}
                onClick={() => toggleExpand(c.claim_id)}>
                {/* Status bar */}
                <div style={{ width: 3, alignSelf: "stretch", borderRadius: 2, background: statusColor, flexShrink: 0 }} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 12, color: fg, lineHeight: 1.4 }}>{c.normalized_claim}</div>
                  <div style={{ display: "flex", gap: 6, marginTop: 4, flexWrap: "wrap" }}>
                    <span style={{ fontSize: 9, padding: "1px 6px", borderRadius: 6,
                      background: "#7c3aed18", color: "#7c3aed", fontWeight: 600 }}>{c.claim_type}</span>
                    <span style={{ fontSize: 9, padding: "1px 6px", borderRadius: 6,
                      background: statusColor + "22", color: statusColor, fontWeight: 600 }}>{c.claim_status}</span>
                    {c.signs_involved && c.signs_involved.length > 0 && c.signs_involved.map(s => (
                      <span key={s} style={{ fontSize: 9, padding: "1px 6px", borderRadius: 6,
                        background: "#b4530922", color: "#b45309", fontWeight: 600 }}>{s}</span>
                    ))}
                  </div>
                </div>
                <span style={{ fontSize: 9, color: muted, flexShrink: 0, marginTop: 2 }}>{isExp ? "▲" : "▼"}</span>
              </div>
              {isExp && (
                <div style={{ padding: "8px 14px 12px 27px", borderTop: `1px solid ${border}` }}>
                  {c.source_document_id && (
                    <div style={{ fontSize: 10, color: muted, marginBottom: 4 }}>
                      Source: <span style={{ color: fg }}>{c.source_document_id}</span>
                    </div>
                  )}
                  {c.falsification_condition && (
                    <div style={{ fontSize: 10, marginBottom: 4 }}>
                      <span style={{ color: muted }}>Falsification: </span>
                      <span style={{ color: fg }}>{c.falsification_condition}</span>
                    </div>
                  )}
                  {c.glossa_lab_evidence && (
                    <div style={{ fontSize: 10, marginBottom: 4 }}>
                      <span style={{ color: muted }}>Glossa-Lab: </span>
                      <span style={{ color: "#22c55e" }}>{c.glossa_lab_evidence}</span>
                    </div>
                  )}
                  {c.proposed_value && (
                    <div style={{ fontSize: 10 }}>
                      <span style={{ color: muted }}>Proposed value: </span>
                      <span style={{ color: fg }}>{c.proposed_value}</span>
                    </div>
                  )}
                  {c.confidence_in_source !== undefined && (
                    <div style={{ fontSize: 10, color: muted, marginTop: 2 }}>
                      Source confidence: {Math.round(c.confidence_in_source * 100)}%
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Sweep Tab ──────────────────────────────────────────────────────────────

function SweepTab({ cardBg, border, fg, muted, inputBg, inputBdr, toast }: {
  darkMode?: boolean; cardBg: string; border: string; fg: string; muted: string;
  inputBg: string; inputBdr: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toast: (msg: string, kind?: any) => void;
}) {
  const [config, setConfig] = useState<SweepConfig | null>(null);
  const [configLoading, setConfigLoading] = useState(true);
  const [configSaving, setConfigSaving] = useState(false);
  const [sweepRunning, setSweepRunning] = useState(false);
  const [candidates, setCandidates] = useState<SweepCandidate[]>([]);
  const [candLoading, setCandLoading] = useState(false);
  const [sweepDate, setSweepDate] = useState<string | null>(null);
  const [totalNew, setTotalNew] = useState(0);
  const [intakingIds, setIntakingIds] = useState<Set<string>>(new Set());

  // Editable keyword strings (for inline editing)
  const [primaryKw, setPrimaryKw]     = useState("");
  const [secondaryKw, setSecondaryKw] = useState("");
  const [exclusions, setExclusions]   = useState("");
  const [sweepName, setSweepName]     = useState("");

  useEffect(() => {
    setConfigLoading(true);
    getIndusSweepConfig()
      .then(cfg => {
        setConfig(cfg);
        setSweepName(cfg.sweep.name || "");
        setPrimaryKw((cfg.sweep.keywords.primary || []).join(", "));
        setSecondaryKw((cfg.sweep.keywords.secondary || []).join(", "));
        setExclusions((cfg.sweep.exclusions || []).join(", "));
      })
      .catch(() => {})
      .finally(() => setConfigLoading(false));

    loadCandidates();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadCandidates = async () => {
    setCandLoading(true);
    try {
      const r = await getIndusSweepCandidates();
      setCandidates(r.candidates || []);
      setSweepDate(r.sweep_date || null);
      setTotalNew(r.total_new || 0);
    } catch { /* no candidates yet */ }
    finally { setCandLoading(false); }
  };

  const handleSaveConfig = async () => {
    if (!config) return;
    setConfigSaving(true);
    try {
      const updated: SweepConfig = {
        ...config,
        sweep: {
          ...config.sweep,
          name: sweepName,
          keywords: {
            ...config.sweep.keywords,
            primary:   primaryKw.split(",").map(s => s.trim()).filter(Boolean),
            secondary: secondaryKw.split(",").map(s => s.trim()).filter(Boolean),
          },
          exclusions: exclusions.split(",").map(s => s.trim()).filter(Boolean),
        },
      };
      await saveIndusSweepConfig(updated);
      setConfig(updated);
      toast("Sweep config saved", "success");
    } catch (e) { toast(String(e), "error"); }
    finally { setConfigSaving(false); }
  };

  const handleRunSweep = async () => {
    setSweepRunning(true);
    try {
      const r = await runIndusSweep();
      toast(r.message, "info");
      // Poll for candidates after a delay
      setTimeout(() => void loadCandidates(), 8000);
      setTimeout(() => void loadCandidates(), 20000);
    } catch (e) { toast(String(e), "error"); }
    finally { setSweepRunning(false); }
  };

  const handleIntake = async (cand: SweepCandidate) => {
    const key = cand.url || cand.title;
    setIntakingIds(prev => new Set(prev).add(key));
    try {
      const r = await intakeSweepCandidate({
        url: cand.url,
        pdf_url: cand.pdf_url || undefined,
        title: cand.title,
        doi: cand.doi || undefined,
        authors: cand.authors,
        source: cand.source,
      });
      toast(r.message, "success");
    } catch (e) { toast(String(e), "error"); }
    finally { setIntakingIds(prev => { const n = new Set(prev); n.delete(key); return n; }); }
  };

  const inpStyle: React.CSSProperties = {
    padding: "7px 10px", border: `1px solid ${inputBdr}`, borderRadius: 6,
    fontSize: 12, background: inputBg, color: fg, outline: "none",
    width: "100%", boxSizing: "border-box",
  };
  const textareaStyle: React.CSSProperties = {
    ...inpStyle, resize: "vertical" as const, fontFamily: "inherit",
    minHeight: 60, lineHeight: 1.5,
  };

  if (configLoading) return <div style={{ color: muted, fontSize: 12 }}>Loading sweep config…</div>;

  // Source toggles from config
  const sources = config?.sweep.sources ?? {};
  const enabledSources = Object.entries(sources).filter(([, v]) => v?.enabled).map(([k]) => k);
  const disabledSources = Object.entries(sources).filter(([, v]) => !v?.enabled).map(([k]) => k);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      {/* Config editor */}
      <div style={{ background: cardBg, border: `1px solid ${border}`, borderRadius: 10, padding: "16px 20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: fg }}>⚙️ Sweep Configuration</div>
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => void handleSaveConfig()} disabled={configSaving}
              style={{ padding: "6px 14px", border: "none", borderRadius: 6, background: "#7c3aed",
                color: "#fff", cursor: "pointer", fontSize: 12, fontWeight: 600,
                opacity: configSaving ? 0.5 : 1 }}>
              {configSaving ? "Saving…" : "💾 Save Config"}
            </button>
            <button onClick={() => void handleRunSweep()} disabled={sweepRunning}
              style={{ padding: "6px 14px", border: "none", borderRadius: 6, background: "#059669",
                color: "#fff", cursor: "pointer", fontSize: 12, fontWeight: 600,
                opacity: sweepRunning ? 0.5 : 1 }}>
              {sweepRunning ? "⏳ Running…" : "▶ Run Sweep"}
            </button>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          <div>
            <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
              Sweep Name
            </label>
            <input value={sweepName} onChange={e => setSweepName(e.target.value)} style={inpStyle} />
          </div>
          <div>
            <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
              Enabled Sources
            </label>
            <div style={{ fontSize: 11, color: fg, padding: "7px 10px", border: `1px solid ${inputBdr}`,
              borderRadius: 6, background: inputBg, lineHeight: 1.6 }}>
              {enabledSources.join(", ") || "none"}
            </div>
          </div>
        </div>

        <div style={{ marginTop: 14 }}>
          <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
            Primary Keywords <span style={{ fontWeight: 400 }}>(comma-separated)</span>
          </label>
          <textarea value={primaryKw} onChange={e => setPrimaryKw(e.target.value)} style={textareaStyle} />
        </div>

        <div style={{ marginTop: 14 }}>
          <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
            Secondary Keywords <span style={{ fontWeight: 400 }}>(comma-separated)</span>
          </label>
          <textarea value={secondaryKw} onChange={e => setSecondaryKw(e.target.value)} style={textareaStyle} />
        </div>

        <div style={{ marginTop: 14 }}>
          <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
            Exclusions <span style={{ fontWeight: 400 }}>(comma-separated, exact phrase match)</span>
          </label>
          <input value={exclusions} onChange={e => setExclusions(e.target.value)} style={inpStyle} />
        </div>

        {disabledSources.length > 0 && (
          <div style={{ marginTop: 12, fontSize: 10, color: muted }}>
            Disabled sources (edit sweep.yaml to enable): {disabledSources.join(", ")}
          </div>
        )}
      </div>

      {/* Candidates */}
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: fg }}>
            🔍 Sweep Candidates
            {sweepDate && <span style={{ fontSize: 10, color: muted, marginLeft: 8 }}>Last sweep: {fmtDate(sweepDate)}</span>}
          </div>
          {totalNew > 0 && (
            <span style={{ fontSize: 11, padding: "3px 10px", borderRadius: 8,
              background: "#7c3aed18", color: "#7c3aed", fontWeight: 700 }}>
              {totalNew} new candidates
            </span>
          )}
          <button onClick={() => void loadCandidates()} disabled={candLoading}
            style={{ padding: "5px 12px", border: `1px solid ${border}`, borderRadius: 6,
              background: "none", color: muted, cursor: "pointer", fontSize: 11 }}>
            {candLoading ? "…" : "↻ Refresh"}
          </button>
        </div>

        {candidates.length === 0 && !candLoading && (
          <div style={{ color: muted, fontSize: 12, fontStyle: "italic" }}>
            No candidates yet. Click "Run Sweep" to search for new papers.
          </div>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {candidates.map((cand, i) => {
            const key = cand.url || cand.title || String(i);
            const busy = intakingIds.has(key);
            return (
              <div key={i} style={{ background: cardBg, border: `1px solid ${border}`,
                borderRadius: 8, padding: "10px 14px", display: "flex", gap: 12, alignItems: "flex-start" }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <a href={cand.url} target="_blank" rel="noopener noreferrer"
                    style={{ fontSize: 12, fontWeight: 600, color: "#7c3aed", textDecoration: "none",
                      display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                    {cand.title || "(untitled)"}
                  </a>
                  <div style={{ fontSize: 10, color: muted, marginTop: 3, display: "flex", gap: 8, flexWrap: "wrap" }}>
                    <span>{cand.source}</span>
                    {cand.authors.length > 0 && <span>{cand.authors.slice(0, 2).join(", ")}</span>}
                    {cand.published_at && <span>{cand.published_at.slice(0, 7)}</span>}
                    {cand.open_access && <span style={{ color: "#16a34a" }}>OA PDF</span>}
                  </div>
                  {cand.summary && (
                    <div style={{ fontSize: 10, color: muted, marginTop: 3, lineHeight: 1.4,
                      display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                      {cand.summary}
                    </div>
                  )}
                </div>
                <button onClick={() => void handleIntake(cand)} disabled={busy}
                  title="Import this paper to the evidence library"
                  style={{ padding: "5px 12px", border: "none", borderRadius: 6, background: "#7c3aed",
                    color: "#fff", cursor: "pointer", fontSize: 11, fontWeight: 600,
                    opacity: busy ? 0.5 : 1, flexShrink: 0, whiteSpace: "nowrap" as const }}>
                  {busy ? "…" : "→ Import"}
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
