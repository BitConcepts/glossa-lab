/**
 * EvidenceLibrary — the Library tab of Evidence & sources (Spec 081
 * step 6): registered papers, PDF upload, URL import, hypothesis
 * models. Extracted verbatim from the retired IndusEvidenceView
 * three-tab workspace; the claims tab moved to the Claims surface
 * (step 3) and the sweep tab to the research loop (SweepPanel).
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  importIndusUrl,
  listIndusHypotheses,
  listIndusLibrary,
  runIndusIntake,
  uploadIndusPaper,
  type IndusDoc,
  type IndusHypothesisModel,
} from "../api";
import { useToast } from "../hooks/useToast";

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

export function EvidenceLibrary({ darkMode = true }: { darkMode?: boolean }) {
  const { toast } = useToast();
  const cardBg = darkMode ? "#1e293b" : "#ffffff";
  const border = darkMode ? "#334155" : "#e5e7eb";
  const fg = darkMode ? "#e2e8f0" : "#111827";
  const muted = darkMode ? "#94a3b8" : "#6b7280";
  const inputBg = darkMode ? "#0f172a" : "#ffffff";
  const inputBdr = darkMode ? "#334155" : "#d1d5db";
  return (
    <LibraryTab darkMode={darkMode} cardBg={cardBg} border={border} fg={fg} muted={muted}
      inputBg={inputBg} inputBdr={inputBdr} toast={toast} />
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
