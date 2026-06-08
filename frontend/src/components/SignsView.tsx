/**
 * SignsView — browse all deciphered/undeciphered signs with confidence
 * filters, search, glyph placeholders, and full cross-references to
 * experiments, DEDR entries, and reports.
 */
import { useCallback, useEffect, useState } from "react";
import {
  getSignsSummary,
  listSigns,
  type SignEntry,
  type SignsSummary,
  getSignImagesStatus,
  triggerSignImageProcessing,
  processOneSignImage,
  type SignImagesStatus,
  getPagePreviews,
  type PagePreview,
  verifySignImages,
  type VerifyResult,
  rebuildSignManifest,
} from "../api";
import { CorpusAnalyticsPanel } from "./CorpusAnalyticsPanel";

// ── SignGlyph ────────────────────────────────────────────────────────────
function SignGlyph({ sign_id, imageUrl, size = 56 }: { sign_id: string; imageUrl?: string | null; size?: number }) {
  const [imgFailed, setImgFailed] = useState(false);
  if (imageUrl && !imgFailed) {
    return (
      <img
        src={imageUrl}
        alt={sign_id}
        width={size}
        height={size}
        onError={() => setImgFailed(true)}
        style={{ flexShrink: 0, borderRadius: 6, objectFit: 'contain',
                 background: '#fff', border: '1px solid #e5e7eb' }}
      />
    );
  }
  // SVG fallback — white background, black text
  return (
    <svg width={size} height={size} viewBox="0 0 56 56" style={{ flexShrink: 0 }}>
      <rect x="1" y="1" width="54" height="54" rx="6" fill="#ffffff" stroke="#d1d5db" strokeWidth="1" />
      <text
        x="28" y="33"
        textAnchor="middle"
        dominantBaseline="central"
        fontFamily="'Georgia', 'Times New Roman', serif"
        fontWeight="700"
        fontSize={sign_id.length > 4 ? "11" : "14"}
        fill="#111827"
        letterSpacing="0.5"
      >
        {sign_id}
      </text>
    </svg>
  );
}

// ── Confidence chip ─────────────────────────────────────────────────────
const CONF_COLORS: Record<string, { bg: string; fg: string; border: string }> = {
  HIGH:   { bg: "#052e16", fg: "#4ade80", border: "#16a34a" },
  MEDIUM: { bg: "#1c1917", fg: "#fbbf24", border: "#d97706" },
  LOW:    { bg: "#1c1917", fg: "#f87171", border: "#dc2626" },
  UNCERTAIN: { bg: "#1e293b", fg: "#94a3b8", border: "#475569" },
};

function ConfChip({ level }: { level: string }) {
  const c = CONF_COLORS[level] ?? CONF_COLORS.UNCERTAIN;
  return (
    <span style={{
      padding: "1px 7px", borderRadius: 10, fontSize: 10, fontWeight: 700,
      background: c.bg, color: c.fg, border: `1px solid ${c.border}`,
      letterSpacing: 0.3, lineHeight: "18px",
    }}>
      ●{level}
    </span>
  );
}

// ── Filter chips ────────────────────────────────────────────────────────
type ConfLevel = "HIGH" | "MEDIUM" | "LOW" | "Undeciphered";

function FilterChip({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return (
    <button onClick={onClick} style={{
      padding: "4px 12px", borderRadius: 14, fontSize: 11, fontWeight: active ? 700 : 500,
      border: active ? "1px solid #2563eb" : "1px solid #d1d5db",
      background: active ? "#dbeafe" : "#f9fafb",
      color: active ? "#1d4ed8" : "#6b7280",
      cursor: "pointer", transition: "all 0.12s",
    }}>
      {label}
    </button>
  );
}

// ── Sign Card ───────────────────────────────────────────────────────────
function SignCard({ sign, onClick }: { sign: SignEntry; onClick?: () => void }) {
  const phase = sign.source?.phase;
  const dedr = sign.source?.dedr_ref;
  const expName = sign.source?.experiment || "";
  // Truncate long experiment names
  const shortExp = expName.length > 30 ? expName.slice(0, 30) + "…" : expName;

  return (
    <div
      onClick={onClick}
      style={{
        padding: "14px 16px", borderRadius: 10, cursor: "pointer",
        background: "#1e293b", border: "1px solid rgba(255,255,255,0.08)",
        transition: "border-color 0.12s, box-shadow 0.12s",
      }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = "#3b82f6"; e.currentTarget.style.boxShadow = "0 0 0 1px #3b82f680"; }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = "rgba(255,255,255,0.08)"; e.currentTarget.style.boxShadow = "none"; }}
    >
      {/* Top row: glyph + id + reading + confidence */}
      <div style={{ display: "flex", gap: 12, alignItems: "flex-start", marginBottom: 10 }}>
        <SignGlyph sign_id={sign.sign_id} imageUrl={sign.image_url} />
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
            <span style={{ fontSize: 16, fontWeight: 700, color: "#e2e8f0", fontFamily: "monospace" }}>
              {sign.sign_id}
            </span>
            <ConfChip level={sign.confidence} />
          </div>
          {sign.reading && (
            <div style={{ fontSize: 14, color: "#93c5fd", fontWeight: 600, marginTop: 3 }}>
              Reading: <em>{sign.reading}</em>
            </div>
          )}
          {sign.corpus_freq > 0 && (
            <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 2 }}>
              Corpus freq: {sign.corpus_freq.toLocaleString()}
            </div>
          )}
        </div>
      </div>

      {/* Divider */}
      <div style={{ borderTop: "1px solid rgba(255,255,255,0.06)", margin: "0 -2px 8px" }} />

      {/* Cross-reference section */}
      <div style={{ fontSize: 11, color: "#94a3b8", lineHeight: 1.6 }}>
        {phase != null && phase > 0 && (
          <div>Source: <span style={{ color: "#cbd5e1" }}>Phase {phase} Anchored SA</span></div>
        )}
        {dedr && (
          <div>Evidence: <span style={{ color: "#fbbf24" }}>{dedr}</span>{sign.gloss ? ` (${sign.gloss})` : ""}</div>
        )}
        {shortExp && (
          <div>Experiment: <span style={{ color: "#a78bfa" }}>{shortExp}</span></div>
        )}
        {sign.basis && !dedr && (
          <div style={{ color: "#6b7280", fontSize: 10, marginTop: 2 }}>
            {sign.basis.length > 80 ? sign.basis.slice(0, 80) + "…" : sign.basis}
          </div>
        )}
      </div>

      {/* Action buttons */}
      <div style={{ display: "flex", gap: 6, marginTop: 8, flexWrap: "wrap", alignItems: "center" }}>
        {/* Triple-check badge */}
        <span title={sign.image_url ? "Image present" : "Missing image"}
          style={{ fontSize: 10, fontWeight: 700, letterSpacing: 1,
                   color: sign.image_url ? "#4ade80" : "#f87171" }}>
          {sign.image_url ? "✓✓✓" : "✗"}
        </span>
        {/* Reprocess button */}
        <button
          onClick={async (e) => {
            e.stopPropagation();
            try {
              await processOneSignImage(sign.sign_id, true);
              window.dispatchEvent(new CustomEvent("glossa:sign-reprocessed", { detail: { sign_id: sign.sign_id } }));
            } catch { /* best effort */ }
          }}
          style={{
            padding: "2px 8px", fontSize: 10, borderRadius: 4,
            border: "1px solid rgba(255,255,255,0.1)", background: "rgba(255,255,255,0.04)",
            color: "#fbbf24", cursor: "pointer",
          }}
          title="Reprocess this sign image"
        >
          🔄 Reprocess
        </button>
        {sign.source?.report_ref && (
          <button
            onClick={e => { e.stopPropagation(); window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "reports" } })); }}
            style={{
              padding: "2px 8px", fontSize: 10, borderRadius: 4,
              border: "1px solid rgba(255,255,255,0.1)", background: "rgba(255,255,255,0.04)",
              color: "#93c5fd", cursor: "pointer",
            }}
          >
            📄 Report
          </button>
        )}
        {expName && (
          <button
            onClick={e => { e.stopPropagation(); window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "experiments" } })); }}
            style={{
              padding: "2px 8px", fontSize: 10, borderRadius: 4,
              border: "1px solid rgba(255,255,255,0.1)", background: "rgba(255,255,255,0.04)",
              color: "#a78bfa", cursor: "pointer",
            }}
          >
            🔬 Experiment
          </button>
        )}
      </div>
    </div>
  );
}

// ── Lightbox ────────────────────────────────────────────────────────────
function SignLightbox({ sign, onClose }: { sign: SignEntry; onClose: () => void }) {
  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed", inset: 0, background: "rgba(0,0,0,0.85)",
        zIndex: 600, display: "flex", alignItems: "center", justifyContent: "center",
        cursor: "zoom-out",
      }}
    >
      <div onClick={e => e.stopPropagation()} style={{ textAlign: "center" }}>
        {sign.image_url ? (
          <img
            src={sign.image_url}
            alt={sign.sign_id}
            style={{
              width: 400, height: 400, objectFit: "contain",
              background: "#fff", borderRadius: 12, padding: 24,
              imageRendering: "pixelated",
            }}
          />
        ) : (
          <SignGlyph sign_id={sign.sign_id} size={400} />
        )}
        <div style={{ color: "#e2e8f0", fontSize: 18, fontWeight: 700, marginTop: 16 }}>
          {sign.sign_id}{sign.reading ? ` — ${sign.reading}` : ""}
        </div>
        <div style={{ color: "#64748b", fontSize: 12, marginTop: 4 }}>Click anywhere to close</div>
      </div>
    </div>
  );
}

// ── Detail panel ────────────────────────────────────────────────────────
function SignDetail({ sign, onClose }: { sign: SignEntry; onClose: () => void }) {
  const [showLightbox, setShowLightbox] = useState(false);
  return (
    <>
    {showLightbox && <SignLightbox sign={sign} onClose={() => setShowLightbox(false)} />}
    <div style={{
      position: "fixed", top: 0, right: 0, bottom: 0, width: 420,
      background: "#0f172a", borderLeft: "1px solid rgba(255,255,255,0.1)",
      boxShadow: "-4px 0 24px rgba(0,0,0,0.4)", zIndex: 500,
      overflowY: "auto", padding: 24,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <h3 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "#e2e8f0" }}>Sign {sign.sign_id}</h3>
        <button onClick={onClose} style={{ border: "none", background: "none", color: "#94a3b8", fontSize: 20, cursor: "pointer" }}>×</button>
      </div>

      {/* Large sign image — click to open lightbox */}
      <div
        onClick={() => setShowLightbox(true)}
        style={{
          display: "flex", justifyContent: "center", marginBottom: 20,
          cursor: "zoom-in", padding: 16, background: "#fff", borderRadius: 10,
          border: "1px solid rgba(255,255,255,0.1)",
        }}
        title="Click to enlarge"
      >
        {sign.image_url ? (
          <img
            src={sign.image_url}
            alt={sign.sign_id}
            style={{
              width: 200, height: 200, objectFit: "contain",
              imageRendering: "pixelated",
            }}
          />
        ) : (
          <SignGlyph sign_id={sign.sign_id} size={200} />
        )}
      </div>

      <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 16, flexWrap: "wrap" }}>
        <ConfChip level={sign.confidence} />
        {sign.reading && <span style={{ fontSize: 20, fontWeight: 700, color: "#93c5fd" }}>{sign.reading}</span>}
        {sign.gloss && <span style={{ fontSize: 13, color: "#94a3b8" }}>({sign.gloss})</span>}
      </div>

      {/* Fields */}
      {[
        ["Corpus Frequency", sign.corpus_freq > 0 ? sign.corpus_freq.toLocaleString() : "—"],
        ["In Corpus", sign.in_corpus ? "Yes" : "No"],
        ["Evidence Type", sign.evidence_type || "—"],
        ["Evidence Score", sign.evidence_score > 0 ? sign.evidence_score.toFixed(3) : "—"],
        ["Numbering System", sign.numbering_system || "—"],
        ["Phase", sign.source?.phase?.toString() || "—"],
        ["Source Experiment", sign.source?.experiment || "—"],
        ["DEDR Reference", sign.source?.dedr_ref || "—"],
        ["Report", sign.source?.report_ref || "—"],
      ].map(([k, v]) => (
        <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
          <span style={{ fontSize: 11, color: "#94a3b8" }}>{k}</span>
          <span style={{ fontSize: 12, color: "#cbd5e1", fontWeight: 500, maxWidth: "60%", textAlign: "right", wordBreak: "break-all" }}>{v}</span>
        </div>
      ))}

      {sign.basis && (
        <div style={{ marginTop: 16 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 }}>Basis</div>
          <p style={{ margin: 0, fontSize: 12, lineHeight: 1.6, color: "#cbd5e1" }}>{sign.basis}</p>
        </div>
      )}
    </div>
    </>
  );
}

// ── Sample grid for Image Analyzer tab ─────────────────────────────────
function SignSampleGrid() {
  const [signs, setSigns] = useState<SignEntry[]>([]);
  useEffect(() => {
    listSigns({ limit: 60, offset: 0 }).then(r => setSigns(r.items)).catch(() => {});
  }, []);
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(64px, 1fr))",
      gap: 6,
    }}>
      {signs.map(s => (
        <div key={s.sign_id} title={`${s.sign_id}${s.reading ? ` · ${s.reading}` : ""}`}
          style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 2 }}>
          <SignGlyph sign_id={s.sign_id} imageUrl={s.image_url} size={56} />
          <span style={{ fontSize: 8, color: "#6b7280", textAlign: "center", lineHeight: 1.2 }}>
            {s.sign_id}
          </span>
        </div>
      ))}
    </div>
  );
}

// ── Main component ──────────────────────────────────────────────────────
export function SignsView() {
  const [summary, setSummary] = useState<SignsSummary | null>(null);
  const [signs, setSigns] = useState<SignEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [confFilters, setConfFilters] = useState<Set<ConfLevel>>(new Set());
  const [search, setSearch] = useState("");
  const [inCorpusOnly, setInCorpusOnly] = useState(false);
  const [offset, setOffset] = useState(0);
  const [selected, setSelected] = useState<SignEntry | null>(null);
  const [activeTab, setActiveTab] = useState<"signs" | "corpus" | "analyzer">("signs");
  const [imgStatus, setImgStatus] = useState<SignImagesStatus | null>(null);
  const [imgStatusLoading, setImgStatusLoading] = useState(false);
  const [imgMsg, setImgMsg] = useState<string | null>(null);
  const [pagePreviews, setPagePreviews] = useState<PagePreview[]>([]);
  const [selectedPreview, setSelectedPreview] = useState<PagePreview | null>(null);
  const [verifyResult, setVerifyResult] = useState<VerifyResult | null>(null);
  const [verifying, setVerifying] = useState(false);
  const [rebuildMsg, setRebuildMsg] = useState<string | null>(null);

  const loadImgStatus = useCallback(async () => {
    setImgStatusLoading(true);
    try { setImgStatus(await getSignImagesStatus()); }
    catch { /* backend may be offline */ }
    finally { setImgStatusLoading(false); }
  }, []);

  useEffect(() => {
    if (activeTab === "analyzer") {
      void loadImgStatus();
      getPagePreviews().then(r => setPagePreviews(r.pages)).catch(() => {});
    }
  }, [activeTab, loadImgStatus]);

  const handleRegenLocal = async () => {
    setImgMsg("Regenerating sign images from local sources (no external downloads)…");
    try {
      const res = await triggerSignImageProcessing({ force: true, skip_wikimedia: true });
      setImgMsg(res.queued ? "✔ Running in background — refresh status in a moment." : (res.reason ?? "Already running."));
    } catch (e) {
      setImgMsg(`Error: ${e instanceof Error ? e.message : String(e)}`);
    }
  };

  const limit = 100;

  // Load summary on mount
  useEffect(() => {
    getSignsSummary().then(setSummary).catch(() => {});
  }, []);

  // Load signs with filters
  const loadSigns = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const confParam = confFilters.size > 0
        ? Array.from(confFilters).filter(c => c !== "Undeciphered").join(",")
        : undefined;
      const deciphered = confFilters.has("Undeciphered") && confFilters.size === 1 ? false : undefined;

      const resp = await listSigns({
        confidence: confParam || undefined,
        search: search || undefined,
        in_corpus: inCorpusOnly ? true : undefined,
        deciphered,
        limit,
        offset,
      });
      setSigns(resp.items);
      setTotal(resp.total);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load signs");
    } finally {
      setLoading(false);
    }
  }, [confFilters, search, inCorpusOnly, offset]);

  useEffect(() => { void loadSigns(); }, [loadSigns]);

  const toggleConf = (level: ConfLevel) => {
    setConfFilters(prev => {
      const next = new Set(prev);
      if (next.has(level)) next.delete(level); else next.add(level);
      return next;
    });
    setOffset(0);
  };

  const totalPages = Math.ceil(total / limit);
  const currentPage = Math.floor(offset / limit) + 1;

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ margin: "0 0 8px", fontSize: 22, fontWeight: 700 }}>
          🔣 Signs
        </h2>
        {summary && (
          <div style={{ display: "flex", gap: 16, flexWrap: "wrap", fontSize: 13, color: "#94a3b8" }}>
            <span><strong style={{ color: "#4ade80" }}>{summary.deciphered}</strong> deciphered</span>
            <span>·</span>
            <span><strong style={{ color: "#f87171" }}>{summary.undeciphered}</strong> undeciphered</span>
            <span>·</span>
            <span><strong style={{ color: "#e2e8f0" }}>{summary.icit_total}</strong> known</span>
            <span>·</span>
            <span><strong style={{ color: "#60a5fa" }}>{summary.in_corpus}</strong> in corpus</span>
          </div>
        )}
      </div>

      {/* Tab bar */}
      <div style={{ display: "flex", gap: 4, marginBottom: 16, flexWrap: "wrap" }}>
        {(["signs", "corpus", "analyzer"] as const).map(t => (
          <button key={t} onClick={() => setActiveTab(t)} style={{
            padding: "6px 16px", borderRadius: 6, fontSize: 12, fontWeight: activeTab === t ? 700 : 500,
            border: activeTab === t ? "1px solid #2563eb" : "1px solid #d1d5db",
            background: activeTab === t ? "#dbeafe" : "#f9fafb",
            color: activeTab === t ? "#1d4ed8" : "#374151",
            cursor: "pointer",
          }}>
            {t === "signs" ? "🔣 Signs Index" : t === "corpus" ? "📊 Corpus Analytics" : "🖼 Image Analyzer"}
          </button>
        ))}
      </div>

      {activeTab === "corpus" ? (
        <CorpusAnalyticsPanel />
      ) : activeTab === "analyzer" ? (
        <div>
          {/* Header */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
            <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>Sign Image Analyzer</h3>
            <button onClick={() => void loadImgStatus()} disabled={imgStatusLoading}
              style={{ padding: "4px 12px", fontSize: 11, borderRadius: 5, border: "1px solid #d1d5db",
                       background: "#f9fafb", cursor: "pointer", color: "#374151" }}>
              {imgStatusLoading ? "…" : "↻ Refresh"}
            </button>
          </div>

          {imgStatus && (
            <>
              {/* Coverage bar */}
              <div style={{ marginBottom: 16, padding: "12px 16px", background: "#f0fdf4",
                             border: "1px solid #86efac", borderRadius: 8 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 6 }}>
                  <span style={{ fontWeight: 700, color: "#15803d" }}>Image Coverage</span>
                  <span style={{ fontWeight: 700, color: "#15803d" }}>{imgStatus.coverage_pct}%</span>
                </div>
                <div style={{ height: 8, background: "#dcfce7", borderRadius: 4, overflow: "hidden" }}>
                  <div style={{ height: "100%", width: `${imgStatus.coverage_pct}%`,
                                 background: "#16a34a", borderRadius: 4, transition: "width 0.4s" }} />
                </div>
                <div style={{ display: "flex", gap: 16, marginTop: 8, fontSize: 12, color: "#374151" }}>
                  <span>✅ {imgStatus.with_image} with image</span>
                  <span>⬜ {imgStatus.without_image} without</span>
                  <span>Total: {imgStatus.total_signs}</span>
                </div>
              </div>

              {/* Source breakdown */}
              <div style={{ marginBottom: 16 }}>
                <div style={{ fontSize: 11, fontWeight: 700, color: "#6b7280",
                               textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8 }}>By Source</div>
                <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                  {Object.entries(imgStatus.by_source).map(([src, count]) => (
                    <div key={src} style={{ padding: "6px 12px", borderRadius: 6, fontSize: 12, fontWeight: 600,
                                            background: src === "wikimedia" ? "#dbeafe" :
                                                        src === "fallback_icon" ? "#fef3c7" :
                                                        src === "manual_upload" ? "#ede9fe" : "#f3f4f6",
                                            color: src === "wikimedia" ? "#1e40af" :
                                                   src === "fallback_icon" ? "#92400e" :
                                                   src === "manual_upload" ? "#5b21b6" : "#374151",
                                            border: "1px solid rgba(0,0,0,0.08)" }}>
                      {src === "wikimedia" ? "🌐" : src === "fallback_icon" ? "✏️" :
                       src === "manual_upload" ? "📤" : src === "none" ? "⬜" : "📄"}
                      {" "}{src}: {count}
                    </div>
                  ))}
                </div>
              </div>

              {/* Explanation */}
              <div style={{ marginBottom: 16, padding: "10px 14px", background: "#f0f9ff",
                             border: "1px solid #bae6fd", borderRadius: 6, fontSize: 11,
                             color: "#0369a1", lineHeight: 1.6 }}>
                <strong>✏️ Fallback icons</strong> are geometric reconstructions drawn from iconic descriptions
                (fish, bull, elephant, strokes, etc.). They are accurate identifiers but not archaeological facsimiles.
                <br />
                <strong>🌐 WikiMedia</strong> images are downloaded real sign renderings where they exist on Commons.
                <br />
                <strong>📤 Manual upload</strong>: drop a sign scan via the API{" "}
                <code style={{ background: "#e0f2fe", padding: "1px 4px", borderRadius: 3 }}>POST /api/v1/signs/images/upload/{"<sign_id>"}</code>
                <br />
                <strong>📄 Grid extraction</strong>: place a Mahadevan sign-table PNG + spec JSON in{" "}
                <code style={{ background: "#e0f2fe", padding: "1px 4px", borderRadius: 3 }}>backend/static/signs/source_pages/</code>
                and re-run the analyzer.
              </div>

              {/* Actions */}
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
                <button onClick={() => void handleRegenLocal()}
                  disabled={imgStatus.processing_running}
                  style={{
                    padding: "7px 16px", fontSize: 12, fontWeight: 700, borderRadius: 6,
                    background: imgStatus.processing_running ? "#e5e7eb" : "#1d4ed8",
                    color: imgStatus.processing_running ? "#9ca3af" : "#fff",
                    border: "none", cursor: imgStatus.processing_running ? "default" : "pointer",
                  }}>
                  {imgStatus.processing_running ? "⏳ Processing…" : "✨ Regenerate Local Images"}
                </button>
                <button onClick={async () => {
                  setRebuildMsg("Rebuilding manifest…");
                  try {
                    const r = await rebuildSignManifest();
                    setRebuildMsg(`✔ Rebuilt: ${r.reconciled} reconciled, ${r.already_ok} already ok, ${r.invalid} invalid`);
                    void loadImgStatus();
                  } catch (e) { setRebuildMsg(`Error: ${e instanceof Error ? e.message : String(e)}`); }
                }}
                  style={{
                    padding: "7px 16px", fontSize: 12, fontWeight: 700, borderRadius: 6,
                    background: "#059669", color: "#fff", border: "none", cursor: "pointer",
                  }}>
                  🔧 Rebuild Manifest
                </button>
                <button onClick={async () => {
                  setVerifying(true);
                  try { setVerifyResult(await verifySignImages({ force: false })); }
                  catch { /* backend offline */ }
                  finally { setVerifying(false); }
                }}
                  disabled={verifying}
                  style={{
                    padding: "7px 16px", fontSize: 12, fontWeight: 700, borderRadius: 6,
                    background: "#7c3aed", color: "#fff", border: "none", cursor: "pointer",
                  }}>
                  {verifying ? "⏳ Verifying…" : "✓✓✓ Triple Check"}
                </button>
              </div>

              {rebuildMsg && (
                <div style={{ padding: "8px 12px", borderRadius: 5, fontSize: 11,
                               background: "#f0fdf4", border: "1px solid #86efac", color: "#15803d",
                               marginBottom: 12 }}>
                  {rebuildMsg}
                </div>
              )}

              {verifyResult && (
                <div style={{ padding: "10px 14px", borderRadius: 6, fontSize: 12,
                               background: verifyResult.failed > 0 ? "#fef2f2" : "#f0fdf4",
                               border: `1px solid ${verifyResult.failed > 0 ? "#fca5a5" : "#86efac"}`,
                               color: verifyResult.failed > 0 ? "#991b1b" : "#15803d",
                               marginBottom: 12, lineHeight: 1.6 }}>
                  <strong>Triple-Check Results:</strong><br />
                  ✅ Passed: {verifyResult.passed} &nbsp;
                  ❌ Failed: {verifyResult.failed} &nbsp;
                  🔄 Requeued: {verifyResult.requeued}
                  {verifyResult.failures.length > 0 && (
                    <div style={{ marginTop: 6, fontSize: 11 }}>
                      <strong>Sample failures:</strong>
                      {verifyResult.failures.slice(0, 10).map(f => (
                        <div key={f.sign_id}>
                          {f.sign_id}: {f.issues.join(", ")}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {imgMsg && (
                <div style={{ padding: "8px 12px", borderRadius: 5, fontSize: 11,
                               background: "#f0fdf4", border: "1px solid #86efac", color: "#15803d",
                               marginBottom: 12 }}>
                  {imgMsg}
                </div>
              )}

              {/* Sample grid */}
              {imgStatus.with_image > 0 && (
                <div>
                  <div style={{ fontSize: 11, fontWeight: 700, color: "#6b7280",
                                 textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8 }}>
                    Sample — first 60 signs
                  </div>
                  <SignSampleGrid />
                </div>
              )}
            </>
          )}

          {!imgStatus && !imgStatusLoading && (
            <div style={{ color: "#9ca3af", fontSize: 12 }}>Backend offline — cannot load image status.</div>
          )}

          {/* Local Page Previews — reference images from Mahadevan, Fuls etc. */}
          {pagePreviews.length > 0 && (
            <div style={{ marginTop: 20 }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: "#6b7280",
                             textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8 }}>
                📖 Local Source Pages ({pagePreviews.length} available)
              </div>
              <div style={{ padding: "10px 14px", background: "#f0f9ff",
                             border: "1px solid #bae6fd", borderRadius: 6, fontSize: 11,
                             color: "#0369a1", lineHeight: 1.6, marginBottom: 12 }}>
                These are locally stored page scans from published sign catalogs (Mahadevan 1977, Fuls 2023).
                They serve as reference material for sign identification and can be used for manual grid extraction.
              </div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                {pagePreviews.map(p => (
                  <button
                    key={p.filename}
                    onClick={() => setSelectedPreview(p)}
                    style={{
                      padding: "6px 12px", borderRadius: 6, fontSize: 11, fontWeight: 600,
                      background: p.source === "mahadevan" ? "#fef3c7" : "#dbeafe",
                      color: p.source === "mahadevan" ? "#92400e" : "#1e40af",
                      border: "1px solid rgba(0,0,0,0.08)", cursor: "pointer",
                      transition: "all 0.12s",
                    }}
                    onMouseEnter={e => { e.currentTarget.style.opacity = "0.85"; }}
                    onMouseLeave={e => { e.currentTarget.style.opacity = "1"; }}
                  >
                    {p.source === "mahadevan" ? "📜" : "📘"} {p.filename.replace(".png", "")}
                    <span style={{ fontSize: 9, opacity: 0.7, marginLeft: 4 }}>
                      ({(p.size_bytes / 1024).toFixed(0)}KB)
                    </span>
                  </button>
                ))}
              </div>

              {/* Selected preview viewer */}
              {selectedPreview && (
                <div style={{ marginTop: 12, padding: 12, background: "#fff",
                               border: "1px solid #e5e7eb", borderRadius: 8 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                    <span style={{ fontSize: 13, fontWeight: 700, color: "#111827" }}>
                      {selectedPreview.filename}
                    </span>
                    <button onClick={() => setSelectedPreview(null)} style={{
                      border: "none", background: "none", fontSize: 16, cursor: "pointer", color: "#6b7280",
                    }}>×</button>
                  </div>
                  <img
                    src={selectedPreview.url}
                    alt={selectedPreview.filename}
                    style={{
                      maxWidth: "100%", maxHeight: 600, borderRadius: 4,
                      border: "1px solid #e5e7eb", objectFit: "contain",
                    }}
                  />
                </div>
              )}
            </div>
          )}
        </div>
      ) : (
        <>
          {/* Filter bar */}
          <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap", alignItems: "center" }}>
            {(["HIGH", "MEDIUM", "LOW", "Undeciphered"] as ConfLevel[]).map(level => (
              <FilterChip key={level} label={level} active={confFilters.has(level)} onClick={() => toggleConf(level)} />
            ))}
            <input
              placeholder="Search sign ID or reading…"
              value={search}
              onChange={e => { setSearch(e.target.value); setOffset(0); }}
              style={{
                padding: "5px 12px", borderRadius: 6, fontSize: 12, width: 220,
                border: "1px solid #d1d5db", background: "#fff",
                color: "#111827", outline: "none",
              }}
            />
            <label style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 11, color: "#6b7280", cursor: "pointer" }}>
              <input type="checkbox" checked={inCorpusOnly} onChange={e => { setInCorpusOnly(e.target.checked); setOffset(0); }} />
              In corpus only
            </label>
            <span style={{ fontSize: 11, color: "#64748b", marginLeft: "auto" }}>{total} signs</span>
          </div>

          {/* Error / loading */}
          {error && <div style={{ padding: 12, background: "#451a1a", borderRadius: 6, color: "#fca5a5", fontSize: 13, marginBottom: 12 }}>{error}</div>}

          {/* Sign grid */}
          {loading && signs.length === 0 ? (
            <div style={{ textAlign: "center", padding: 40, color: "#64748b" }}>Loading signs…</div>
          ) : (
            <div style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
              gap: 12,
            }}>
              {signs.map(s => (
                <SignCard key={s.sign_id} sign={s} onClick={() => setSelected(s)} />
              ))}
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div style={{ display: "flex", gap: 8, alignItems: "center", justifyContent: "center", marginTop: 20 }}>
              <button
                disabled={offset === 0}
                onClick={() => setOffset(Math.max(0, offset - limit))}
                style={{ padding: "4px 12px", borderRadius: 4, border: "1px solid rgba(255,255,255,0.1)", background: "rgba(255,255,255,0.04)", color: "#94a3b8", cursor: offset === 0 ? "default" : "pointer", opacity: offset === 0 ? 0.4 : 1 }}
              >
                ← Prev
              </button>
              <span style={{ fontSize: 12, color: "#94a3b8" }}>Page {currentPage} of {totalPages}</span>
              <button
                disabled={offset + limit >= total}
                onClick={() => setOffset(offset + limit)}
                style={{ padding: "4px 12px", borderRadius: 4, border: "1px solid rgba(255,255,255,0.1)", background: "rgba(255,255,255,0.04)", color: "#94a3b8", cursor: offset + limit >= total ? "default" : "pointer", opacity: offset + limit >= total ? 0.4 : 1 }}
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}

      {/* Detail slide-over */}
      {selected && <SignDetail sign={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
