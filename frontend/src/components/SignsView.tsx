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
      <div style={{ display: "flex", gap: 6, marginTop: 8, flexWrap: "wrap" }}>
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

// ── Detail panel ────────────────────────────────────────────────────────
function SignDetail({ sign, onClose }: { sign: SignEntry; onClose: () => void }) {
  return (
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

      <div style={{ display: "flex", gap: 16, marginBottom: 20 }}>
        <SignGlyph sign_id={sign.sign_id} imageUrl={sign.image_url} size={80} />
        <div>
          <ConfChip level={sign.confidence} />
          {sign.reading && <div style={{ fontSize: 18, fontWeight: 700, color: "#93c5fd", marginTop: 8 }}>{sign.reading}</div>}
          {sign.gloss && <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 4 }}>{sign.gloss}</div>}
        </div>
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
  const [activeTab, setActiveTab] = useState<"signs" | "corpus">("signs");

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
      <div style={{ display: "flex", gap: 4, marginBottom: 16 }}>
        {(["signs", "corpus"] as const).map(t => (
          <button key={t} onClick={() => setActiveTab(t)} style={{
            padding: "6px 16px", borderRadius: 6, fontSize: 12, fontWeight: activeTab === t ? 700 : 500,
            border: activeTab === t ? "1px solid #2563eb" : "1px solid #d1d5db",
            background: activeTab === t ? "#dbeafe" : "#f9fafb",
            color: activeTab === t ? "#1d4ed8" : "#374151",
            cursor: "pointer",
          }}>
            {t === "signs" ? "🔣 Signs Index" : "📊 Corpus Analytics"}
          </button>
        ))}
      </div>

      {activeTab === "corpus" ? (
        <CorpusAnalyticsPanel />
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
