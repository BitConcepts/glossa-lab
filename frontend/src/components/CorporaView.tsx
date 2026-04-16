/**
 * CorporaView — full-featured corpus management.
 * Cards expand on click; each card shows: Browse, Edit, Stats, N-grams, Concordance, AI tabs.
 * Includes file import, export, copy, benchmark comparison.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  createText, deleteText, detectCorpusDirection, getText,
  getCorpusConcordance, getCorpusEntropy, getCorpusExportUrl, getCorpusNgrams,
  listTexts, updateText,
  listCorpusCatalogue, importCorpusCatalogueEntry,
  listAnchorSets, createAnchorSet, deleteAnchorSet,
  type ConcordanceResult, type EntropyResult, type NgramEntry, type TextResponse,
  type CorpusCatalogueEntry, type AnchorSet, type AnchorPair,
} from "../api";
import { ContextMenuOverlay, copyItems, useContextMenu } from "../hooks/useContextMenu";
import { useAIChat } from "../hooks/useAIChat";
import { useToast } from "../hooks/useToast";

const CORPUS_TYPES = ["linguistic", "ancient", "dna", "code", "random", "other"];

const DIR_OPTIONS = [
  { value: "unknown", label: "Unknown" },
  { value: "ltr",     label: "LTR — Left to Right" },
  { value: "rtl",     label: "RTL — Right to Left" },
] as const;

const DIR_META: Record<string, { label: string; color: string; bg: string }> = {
  ltr:     { label: "LTR", color: "#065f46", bg: "#d1fae5" },
  rtl:     { label: "RTL", color: "#7c2d12", bg: "#fee2e2" },
  unknown: { label: "?",   color: "#6b7280", bg: "#f3f4f6" },
};
const PAGE_SIZE = 200;

function BarChart({ data, xKey, yKey, color = "#2563eb", height = 100 }: {
  data: Record<string, unknown>[]; xKey: string; yKey: string; color?: string; height?: number;
}) {
  if (!data.length) return null;
  const vals = data.map((d) => Number(d[yKey]) || 0);
  const max = Math.max(...vals, 1);
  const w = Math.max(8, Math.floor(560 / data.length));
  return (
    <svg viewBox={`0 0 ${data.length * w} ${height}`} style={{ width: "100%", height, overflow: "visible" }}>
      {data.map((d, i) => {
        const v = Number(d[yKey]) || 0;
        const bh = Math.max(1, (v / max) * (height - 16));
        return (
          <g key={i}>
            <rect x={i * w + 1} y={height - bh - 12} width={Math.max(2, w - 2)} height={bh} fill={color} opacity={0.8} rx={1} />
            {data.length <= 20 && (
              <text x={i * w + w / 2} y={height - 2} textAnchor="middle" fontSize={Math.min(9, w - 1)} fill="#6b7280">
                {String(d[xKey]).slice(0, 4)}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}

function Sparkline({ values, color = "#2563eb" }: { values: number[]; color?: string }) {
  if (values.length < 2) return null;
  const h = 40; const w = 300;
  const max = Math.max(...values, 1); const min = Math.min(...values, 0);
  const range = max - min || 1;
  const step = w / (values.length - 1);
  const pts = values.map((v, i) => `${i * step},${h - ((v - min) / range) * h}`).join(" ");
  return (
    <svg viewBox={`0 0 ${w} ${h}`} style={{ width: "100%", height: h }}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth={1.5} />
    </svg>
  );
}

function StatBadge({ label, value, color = "#374151" }: { label: string; value: string | number; color?: string }) {
  return (
    <div style={{ padding: "6px 12px", borderRadius: 6, background: "#f9fafb", border: "1px solid #e5e7eb", textAlign: "center", minWidth: 90 }}>
      <div style={{ fontSize: 18, fontWeight: 700, color, fontFamily: "monospace" }}>{value}</div>
      <div style={{ fontSize: 10, color: "#6b7280", textTransform: "uppercase", letterSpacing: 0.5 }}>{label}</div>
    </div>
  );
}

/** Classify a single token string into a Unicode category bucket. */
function classifyToken(token: string): "numeric" | "latin" | "ancient" | "punctuation" | "mixed" {
  let hasNumeric = false;
  let hasLatin = false;
  let hasAncient = false;
  let hasPunct = false;
  for (const ch of token) {
    const cp = ch.codePointAt(0) ?? 0;
    if (cp >= 0x30 && cp <= 0x39) { hasNumeric = true; continue; } // 0-9
    if ((cp >= 0x41 && cp <= 0x5A) || (cp >= 0x61 && cp <= 0x7A)) { hasLatin = true; continue; } // A-Z a-z
    if (cp === 0x2D || cp === 0x5F || cp === 0x20) continue; // dash / underscore / space (connectors, not counted)
    if (cp < 0x0080) { hasPunct = true; continue; } // other ASCII
    // Non-ASCII: treated as ancient/script character
    hasAncient = true;
  }
  const categories = [hasNumeric, hasLatin, hasAncient, hasPunct].filter(Boolean).length;
  if (categories > 1) return "mixed";
  if (hasAncient) return "ancient";
  if (hasLatin) return "latin";
  if (hasPunct) return "punctuation";
  return "numeric";
}

const TOKEN_TYPE_META: Record<string, { label: string; color: string; bg: string; desc: string }> = {
  numeric:     { label: "Numeric codes",   color: "#2563eb", bg: "#dbeafe", desc: "Tokens like 066 or 066-069 (sign codes)" },
  latin:       { label: "Latin / ASCII",   color: "#16a34a", bg: "#dcfce7", desc: "Latin letter tokens" },
  ancient:     { label: "Non-Latin Unicode", color: "#7c3aed", bg: "#ede9fe", desc: "Ancient script glyphs (Geez, Hebrew, etc.)" },
  punctuation: { label: "Punctuation",     color: "#d97706", bg: "#fef3c7", desc: "Punctuation-only tokens" },
  mixed:       { label: "Mixed (⚠ noise)", color: "#dc2626", bg: "#fee2e2", desc: "Tokens mixing Latin + non-Latin + punctuation" },
};

function TokenTypeInspector({ tokens }: { tokens: string[] }) {
  const counts: Record<string, number> = { numeric: 0, latin: 0, ancient: 0, punctuation: 0, mixed: 0 };
  for (const t of tokens) counts[classifyToken(t)]++;
  const total = tokens.length || 1;
  const mixedPct = (counts.mixed / total) * 100;
  const hasMixedWarning = mixedPct > 5;
  const entries = Object.entries(counts).filter(([, v]) => v > 0);

  return (
    <div style={{ marginTop: 16, padding: "10px 12px", border: "1px solid #e5e7eb", borderRadius: 6, background: "#f9fafb" }}>
      <div style={{ fontSize: 10, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8 }}>
        Token-Type Breakdown
      </div>
      {hasMixedWarning && (
        <div style={{ padding: "4px 8px", background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 4, fontSize: 11, color: "#991b1b", marginBottom: 8 }}>
          ⚠ {mixedPct.toFixed(1)}% mixed-category tokens detected. Consider using a <strong>TokenFilter</strong> node to sanitize this corpus before analysis.
        </div>
      )}
      <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
        {entries.map(([cat, count]) => {
          const meta = TOKEN_TYPE_META[cat];
          const pct = (count / total) * 100;
          return (
            <div key={cat} style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ width: 130, fontSize: 11, color: meta.color, fontWeight: 600, flexShrink: 0 }} title={meta.desc}>
                {meta.label}
              </div>
              <div style={{ flex: 1, background: "#e5e7eb", borderRadius: 3, height: 10, overflow: "hidden" }}>
                <div style={{ width: `${pct}%`, background: meta.color, height: "100%", borderRadius: 3, opacity: 0.85 }} />
              </div>
              <div style={{ width: 60, fontSize: 11, color: "#6b7280", textAlign: "right", flexShrink: 0 }}>
                {count.toLocaleString()} ({pct.toFixed(1)}%)
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function CorpusCard({ text, onUpdated, onDeleted, allTexts }: {
  text: TextResponse;
  onUpdated: (t: TextResponse) => void;
  onDeleted: (id: string) => void;
  allTexts: TextResponse[];
}) {
  const { toast } = useToast();
  const [expanded, setExpanded] = useState(false);
  const [activeTab, setActiveTab] = useState<"browse" | "edit" | "stats" | "ngrams" | "concordance" | "ai" | "compare">("browse");

  const [page, setPage] = useState(0);
  const [search, setSearch] = useState("");

  const [editName, setEditName] = useState(text.name);
  const [editType, setEditType] = useState(text.corpus_type);
  const [editContent, setEditContent] = useState(text.content.join(" "));
  const [editDelimiter, setEditDelimiter] = useState<"space" | "line" | "char">("space");
  const [editDirection, setEditDirection] = useState(text.reading_direction ?? "unknown");
  const [detectingDir, setDetectingDir] = useState(false);
  const [saving, setSaving] = useState(false);

  const [ngramN, setNgramN] = useState(2);
  const [ngrams, setNgrams] = useState<NgramEntry[] | null>(null);
  const [ngramLoading, setNgramLoading] = useState(false);

  const [concQuery, setConcQuery] = useState("");
  const [concResult, setConcResult] = useState<ConcordanceResult | null>(null);
  const [concLoading, setConcLoading] = useState(false);

  const [entropy, setEntropy] = useState<EntropyResult | null>(null);
  const [entropyLoading, setEntropyLoading] = useState(false);

  const [aiMode, setAiMode] = useState<"analyze" | "anomalies" | "critique">("analyze");

  const [compareId, setCompareId] = useState<string>("");
  const [compareEntropy, setCompareEntropy] = useState<EntropyResult | null>(null);
  const [myEntropy, setMyEntropy] = useState<EntropyResult | null>(null);
  const [compareLoading, setCompareLoading] = useState(false);

  const fileRef = useRef<HTMLInputElement>(null);

  const { menu: ctxMenu, show: showCtx, close: closeCtx } = useContextMenu();
  const { openChat } = useAIChat();

  const filtered = search ? text.content.filter((t) => t.toLowerCase().includes(search.toLowerCase())) : text.content;
  const totalPages = Math.ceil(filtered.length / PAGE_SIZE);
  const paginated = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  const handleSave = async () => {
    setSaving(true);
    try {
      let content: string[];
      if (editDelimiter === "line") content = editContent.split("\n").map(s => s.trim()).filter(Boolean);
      else if (editDelimiter === "char") content = editContent.replace(/\s/g, "").split("");
      else content = editContent.trim().split(/\s+/).filter(Boolean);
      const updated = await updateText(text.id, { name: editName.trim(), corpus_type: editType, content, reading_direction: editDirection });
      onUpdated(updated);
      toast("Corpus updated", "success");
    } catch (e) { toast(e instanceof Error ? e.message : "Save failed", "error"); }
    finally { setSaving(false); }
  };

  const handleDetectDirection = async () => {
    setDetectingDir(true);
    try {
      const result = await detectCorpusDirection(text.id);
      setEditDirection(result.inferred_direction);
      // Update the parent with the new reading_direction returned (if direction was updated in DB)
      const updated = await getText(text.id);
      onUpdated(updated);
      const conf = result.confidence === "high" ? "high confidence" : result.confidence === "medium" ? "medium confidence" : "low confidence";
      toast(`Detected: ${result.inferred_direction.toUpperCase()} (${conf}, ${result.n_words} words)`, "info");
    } catch (e) { toast(e instanceof Error ? e.message : "Detection failed", "error"); }
    finally { setDetectingDir(false); }
  };

  const [corpusCopied, setCorpusCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(text.content.join(" ")).then(() => {
      setCorpusCopied(true);
      setTimeout(() => setCorpusCopied(false), 1400);
    });
  };

  const handleFileImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const raw = ev.target?.result as string;
      if (file.name.endsWith(".json")) {
        try { const p = JSON.parse(raw); setEditContent(Array.isArray(p) ? p.join(" ") : (p.content ?? []).join(" ") || raw); }
        catch { setEditContent(raw); }
      } else { setEditContent(raw); }
      setActiveTab("edit");
    };
    reader.readAsText(file);
    e.target.value = "";
  };

  const loadNgrams = async () => {
    setNgramLoading(true);
    try { setNgrams(await getCorpusNgrams(text.id, ngramN)); }
    catch (e) { toast(e instanceof Error ? e.message : "Error", "error"); }
    finally { setNgramLoading(false); }
  };

  const loadConcordance = async () => {
    if (!concQuery.trim()) return;
    setConcLoading(true);
    try { setConcResult(await getCorpusConcordance(text.id, concQuery.trim())); }
    catch (e) { toast(e instanceof Error ? e.message : "Error", "error"); }
    finally { setConcLoading(false); }
  };

  const loadEntropy = useCallback(async () => {
    if (entropy) return;
    setEntropyLoading(true);
    try { setEntropy(await getCorpusEntropy(text.id)); }
    catch (e) { toast(e instanceof Error ? e.message : "Error", "error"); }
    finally { setEntropyLoading(false); }
  }, [entropy, text.id, toast]);

  const handleAI = () => {
    const prompts: Record<string, string> = {
      analyze: `Please analyze the corpus "${text.name}" (${text.corpus_type}, ${text.content.length.toLocaleString()} tokens, alphabet ${text.alphabet_size}). Provide: summary, linguistic characteristics, Indus Script relevance, key insights, and suggested experiments.`,
      anomalies: `Please detect anomalies in the corpus "${text.name}" (${text.corpus_type}, ${text.content.length.toLocaleString()} tokens). Look for statistical anomalies, unusual patterns, structural breaks, and data quality issues.`,
      critique: `Please critique the corpus "${text.name}" (${text.corpus_type}, ${text.content.length.toLocaleString()} tokens, alphabet ${text.alphabet_size}) for research use. Evaluate coverage, bias, completeness, and suitability for Indus Script entropy analysis.`,
    };
    openChat({
      contextType: "corpus",
      contextId: text.id,
      contextLabel: text.name,
      initialPrompt: prompts[aiMode],
    });
  };

  const handleCompare = async () => {
    if (!compareId) return;
    setCompareLoading(true);
    try {
      const [me, other] = await Promise.all([getCorpusEntropy(text.id), getCorpusEntropy(compareId)]);
      setMyEntropy(me); setCompareEntropy(other);
    } catch (e) { toast(e instanceof Error ? e.message : "Error", "error"); }
    finally { setCompareLoading(false); }
  };

  useEffect(() => { if (expanded && activeTab === "stats") loadEntropy(); }, [expanded, activeTab, loadEntropy]);

  const typeColor: Record<string, string> = {
    linguistic: "#2563eb", ancient: "#7c3aed", dna: "#16a34a", code: "#d97706", random: "#6b7280",
  };
  const tc = typeColor[text.corpus_type] ?? "#374151";

  const TABS: Array<{ id: typeof activeTab; label: string }> = [
    { id: "browse", label: "Browse" }, { id: "edit", label: "Edit" }, { id: "stats", label: "Stats" },
    { id: "ngrams", label: "N-grams" }, { id: "concordance", label: "Concordance" },
    { id: "ai", label: "✨ AI" }, { id: "compare", label: "Compare" },
  ];

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden", marginBottom: 8, boxShadow: "0 1px 3px rgba(0,0,0,0.04)" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 14px", background: "#fafafa", cursor: "pointer", borderBottom: expanded ? "1px solid #e5e7eb" : "none" }}
        onClick={() => setExpanded((x) => !x)}>
        <span style={{ fontSize: 11, padding: "1px 7px", borderRadius: 8, background: tc + "20", color: tc, fontWeight: 700, whiteSpace: "nowrap" }}>{text.corpus_type}</span>
        {(() => {
          const dir = text.reading_direction ?? "unknown";
          if (dir === "unknown") return null;  // don't show a "?" badge — direction is simply not set yet
          const dm = DIR_META[dir] ?? DIR_META.ltr;
          return (
            <span title={`Reading direction: ${dir.toUpperCase()}`}
              style={{ fontSize: 10, padding: "1px 6px", borderRadius: 8, background: dm.bg, color: dm.color, fontWeight: 700, whiteSpace: "nowrap", border: `1px solid ${dm.color}33` }}>
              {dm.label}
            </span>
          );
        })()}
        <span style={{ flex: 1, fontWeight: 600, fontSize: 13, color: "#111827" }}>{text.name}</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{text.content.length.toLocaleString()} tokens</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>Σ {text.alphabet_size}</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{text.created_at.slice(0, 10)}</span>
        <span onClick={(e) => e.stopPropagation()} style={{ display: "flex", gap: 4 }}>
          <button onClick={handleCopy} title="Copy" style={{ ...btnMini, background: corpusCopied ? "#dcfce7" : undefined, color: corpusCopied ? "#16a34a" : undefined, transition: "background 0.2s" }}>{corpusCopied ? "✓" : "⎘"}</button>
          <a href={getCorpusExportUrl(text.id, "txt")} download onClick={(e) => e.stopPropagation()} style={{ ...btnMini, textDecoration: "none" }}>↓txt</a>
          <a href={getCorpusExportUrl(text.id, "csv")} download onClick={(e) => e.stopPropagation()} style={{ ...btnMini, textDecoration: "none" }}>↓csv</a>
          <button onClick={() => fileRef.current?.click()} title="Import file" style={btnMini}>↑ file</button>
          <button onClick={async (e) => { e.stopPropagation(); if (!confirm(`Delete "${text.name}"?`)) return; try { await deleteText(text.id); onDeleted(text.id); toast("Deleted", "info"); } catch { toast("Delete failed", "error"); } }}
            style={{ ...btnMini, color: "#dc2626", borderColor: "#fca5a5" }}>🗑</button>
        </span>
        <input ref={fileRef} type="file" accept=".txt,.csv,.json" style={{ display: "none" }} onChange={handleFileImport} />
        <span style={{ fontSize: 14, color: "#9ca3af", marginLeft: 2 }}>{expanded ? "▲" : "▼"}</span>
      </div>

      {expanded && (
        <div>
          <div style={{ display: "flex", borderBottom: "1px solid #e5e7eb", background: "#f9fafb" }}>
            {TABS.map((tab) => (
              <button key={tab.id} onClick={(e) => { e.stopPropagation(); setActiveTab(tab.id); }}
                style={{ padding: "7px 14px", border: "none", borderBottom: activeTab === tab.id ? "2px solid #1e3a5f" : "2px solid transparent", background: "none", cursor: "pointer", fontSize: 12, fontWeight: activeTab === tab.id ? 700 : 400, color: activeTab === tab.id ? "#1e3a5f" : "#6b7280" }}>
                {tab.label}
              </button>
            ))}
          </div>

          <div style={{ padding: "14px 16px" }} onClick={(e) => e.stopPropagation()}>
            {activeTab === "browse" && (
              <div>
                <div style={{ display: "flex", gap: 8, marginBottom: 10, alignItems: "center" }}>
                  <input placeholder="Search tokens…" value={search} onChange={(e) => { setSearch(e.target.value); setPage(0); }} style={{ ...inputStyle, flex: 1 }} />
                  <span style={{ fontSize: 11, color: "#9ca3af", whiteSpace: "nowrap" }}>{filtered.length.toLocaleString()} / {text.content.length.toLocaleString()}</span>
                </div>
                <pre
                  style={{ background: "#1e293b", color: "#e2e8f0", borderRadius: 6, padding: "10px 14px", fontSize: 11, overflowX: "auto", maxHeight: 220, margin: 0, lineHeight: 1.8, cursor: "context-menu" }}
                  onContextMenu={(e) => showCtx(e, [
                    ...copyItems(paginated.join(" "), "Copy page"),
                    { label: "Copy all tokens", icon: "📄", action: () => navigator.clipboard.writeText(text.content.join(" ")).catch(() => {}) },
                  ])}
                >
                  {paginated.join("  ")}
                </pre>
                <ContextMenuOverlay menu={ctxMenu} onClose={closeCtx} />
                {totalPages > 1 && (
                  <div style={{ display: "flex", gap: 6, marginTop: 8, alignItems: "center" }}>
                    <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} style={btnSmall}>← Prev</button>
                    <span style={{ fontSize: 12, color: "#6b7280" }}>Page {page + 1} / {totalPages}</span>
                    <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page >= totalPages - 1} style={btnSmall}>Next →</button>
                  </div>
                )}
              </div>
            )}

            {activeTab === "edit" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 10, maxWidth: 560 }}>
                <div><label style={labelStyle}>Name</label><input value={editName} onChange={(e) => setEditName(e.target.value)} style={inputStyle} /></div>
                <div><label style={labelStyle}>Type</label>
                  <select value={editType} onChange={(e) => setEditType(e.target.value)} style={inputStyle}>
                    {CORPUS_TYPES.map((t) => <option key={t}>{t}</option>)}
                  </select>
                </div>
                <div>
                  <label style={labelStyle}>Reading Direction</label>
                  <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                    <select value={editDirection} onChange={(e) => setEditDirection(e.target.value)} style={{ ...inputStyle, flex: 1 }}>
                      {DIR_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
                    </select>
                    <button onClick={handleDetectDirection} disabled={detectingDir} style={{ ...btnSecondary, whiteSpace: "nowrap" }}
                      title="Auto-detect reading direction using Ashraf & Sinha (2018) positional entropy method">
                      {detectingDir ? "Detecting…" : "🔍 Auto-detect"}
                    </button>
                  </div>
                  <div style={{ fontSize: 10, color: "#6b7280", marginTop: 3 }}>
                    Auto-detect applies the Ashraf &amp; Sinha (2018) positional entropy method. Lower entropy at word-end indicates the reading direction.
                  </div>
                </div>
                <div><label style={labelStyle}>Tokenisation mode (for re-parsing)</label>
                  <select value={editDelimiter} onChange={(e) => setEditDelimiter(e.target.value as "space" | "line" | "char")} style={inputStyle}>
                    <option value="space">Space-separated</option><option value="line">Line-per-token</option><option value="char">Character-level</option>
                  </select>
                </div>
                <div><label style={labelStyle}>Content ({text.content.length.toLocaleString()} tokens)</label>
                  <textarea value={editContent} onChange={(e) => setEditContent(e.target.value)} rows={8}
                    style={{ ...inputStyle, fontFamily: "monospace", resize: "vertical", fontSize: 11 }} />
                </div>
                <div style={{ display: "flex", gap: 8 }}>
                  <button onClick={handleSave} disabled={saving} style={btnPrimary}>{saving ? "Saving…" : "Save"}</button>
                  <button onClick={handleCopy} style={btnSecondary}>Copy All</button>
                  <button onClick={() => fileRef.current?.click()} style={btnSecondary}>Import File</button>
                </div>
              </div>
            )}

            {activeTab === "stats" && (
              <div>
                {entropyLoading && <p style={{ color: "#6b7280", fontSize: 13 }}>Computing metrics…</p>}
                {entropy && (
                  <>
                    <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 14 }}>
                      <StatBadge label="H1 (bits)" value={entropy.h1} color="#2563eb" />
                      <StatBadge label="H2/H1" value={entropy.h2_h1_ratio ?? "—"} color="#7c3aed" />
                      <StatBadge label="Cond H" value={entropy.conditional_h} color="#d97706" />
                      <StatBadge label="TTR" value={entropy.type_token_ratio.toFixed(3)} color="#16a34a" />
                      <StatBadge label="Zipf ρ" value={entropy.zipf_correlation.toFixed(3)} color="#6b7280" />
                      <StatBadge label="Hapax" value={entropy.hapax_count.toLocaleString()} />
                    </div>
                    <div style={{ marginBottom: 10 }}>
                      <div style={sLabel}>Token frequency (top {Math.min(entropy.zipf_table.length, 30)})</div>
                      <BarChart data={entropy.zipf_table.slice(0, 30)} xKey="token" yKey="freq" height={90} />
                    </div>
                    <div><div style={sLabel}>Zipf log-rank vs log-freq</div><Sparkline values={entropy.zipf_table.map(d => d.log_freq)} color="#7c3aed" /></div>
                  </>
                )}
                <TokenTypeInspector tokens={text.content} />
              </div>
            )}

            {activeTab === "ngrams" && (
              <div>
                <div style={{ display: "flex", gap: 6, marginBottom: 10, alignItems: "center" }}>
                  <span style={{ fontSize: 12, color: "#374151" }}>n =</span>
                  {[1, 2, 3, 4].map((n) => (
                    <button key={n} onClick={() => setNgramN(n)} style={{ ...btnSmall, background: ngramN === n ? "#1e3a5f" : "#f3f4f6", color: ngramN === n ? "#fff" : "#374151" }}>{n}</button>
                  ))}
                  <button onClick={loadNgrams} disabled={ngramLoading} style={btnPrimary}>{ngramLoading ? "Loading…" : "Load"}</button>
                </div>
                {ngrams && (
                  <>
                    <BarChart data={ngrams.slice(0, 30).map(g => ({ k: g.ngram.slice(0, 6), count: g.count }))} xKey="k" yKey="count" height={90} color="#7c3aed" />
                    <table style={{ borderCollapse: "collapse", width: "100%", marginTop: 10, fontSize: 12 }}>
                      <thead><tr><th style={thStyle}>N-gram</th><th style={thStyle}>Count</th></tr></thead>
                      <tbody>{ngrams.slice(0, 50).map((g) => (
                        <tr key={g.ngram}><td style={tdStyle}><code>{g.ngram}</code></td><td style={tdStyle}>{g.count.toLocaleString()}</td></tr>
                      ))}</tbody>
                    </table>
                  </>
                )}
              </div>
            )}

            {activeTab === "concordance" && (
              <div>
                <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
                  <input placeholder="Token (exact match)…" value={concQuery} onChange={(e) => setConcQuery(e.target.value)}
                    onKeyDown={(e) => { if (e.key === "Enter") loadConcordance(); }} style={{ ...inputStyle, flex: 1 }} />
                  <button onClick={loadConcordance} disabled={concLoading} style={btnPrimary}>{concLoading ? "…" : "Search"}</button>
                </div>
                {concResult && (
                  <div>
                    <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 8 }}>
                      {concResult.total.toLocaleString()} occurrences of <code>"{concResult.query}"</code>
                    </div>
                    <div style={{ maxHeight: 300, overflowY: "auto" }}>
                      {concResult.hits.slice(0, 100).map((hit, i) => (
                        <div key={i} style={{ display: "flex", gap: 4, padding: "3px 0", borderBottom: "1px solid #f3f4f6", fontSize: 12, fontFamily: "monospace" }}>
                          <span style={{ color: "#9ca3af", width: 50, flexShrink: 0, textAlign: "right", fontSize: 10 }}>{hit.position}</span>
                          <span style={{ color: "#6b7280" }}>{hit.left.join(" ")}</span>
                          <span style={{ background: "#fef3c7", padding: "0 2px", borderRadius: 2, fontWeight: 700, color: "#92400e" }}>{hit.match}</span>
                          <span style={{ color: "#6b7280" }}>{hit.right.join(" ")}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === "ai" && (
              <div>
                <div style={{ display: "flex", gap: 6, marginBottom: 12, flexWrap: "wrap" }}>
                  {(["analyze", "anomalies", "critique"] as const).map((m) => (
                    <button key={m} onClick={() => setAiMode(m)}
                      style={{ ...btnSmall, background: aiMode === m ? "#7c3aed" : "#f3f4f6", color: aiMode === m ? "#fff" : "#374151" }}>
                      {m === "analyze" ? "Corpus Analysis" : m === "anomalies" ? "Anomaly Detection" : "Critique"}
                    </button>
                  ))}
                  <button onClick={handleAI} style={{ ...btnPrimary, background: "#7c3aed", marginLeft: "auto" }}>
                    ✨ Ask AI
                  </button>
                </div>
              </div>
            )}

            {activeTab === "compare" && (
              <div>
                <div style={{ display: "flex", gap: 8, marginBottom: 12, alignItems: "center" }}>
                  <label style={{ fontSize: 12, color: "#374151", whiteSpace: "nowrap" }}>Compare with:</label>
                  <select value={compareId} onChange={(e) => setCompareId(e.target.value)} style={{ ...inputStyle, flex: 1 }}>
                    <option value="">— select corpus —</option>
                    {allTexts.filter((t) => t.id !== text.id).map((t) => (
                      <option key={t.id} value={t.id}>{t.name} ({t.corpus_type})</option>
                    ))}
                  </select>
                  <button onClick={handleCompare} disabled={!compareId || compareLoading} style={btnPrimary}>
                    {compareLoading ? "Loading…" : "Compare"}
                  </button>
                </div>
                {myEntropy && compareEntropy && (() => {
                  const other = allTexts.find((t) => t.id === compareId);
                  const metrics: Array<[string, keyof EntropyResult]> = [
                    ["H1 (bits)", "h1"], ["H2/H1", "h2_h1_ratio"], ["Cond H", "conditional_h"],
                    ["TTR", "type_token_ratio"], ["Zipf ρ", "zipf_correlation"],
                    ["Tokens", "token_count"], ["Alphabet", "type_count"], ["Hapax", "hapax_count"],
                  ];
                  return (
                    <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 12 }}>
                      <thead>
                        <tr>
                          <th style={thStyle}>Metric</th>
                          <th style={thStyle}>{text.name.slice(0, 20)}</th>
                          <th style={thStyle}>{other?.name.slice(0, 20) ?? compareId}</th>
                          <th style={thStyle}>Δ</th>
                        </tr>
                      </thead>
                      <tbody>
                        {metrics.map(([label, key]) => {
                          const a = (myEntropy[key] as number | null) ?? 0;
                          const b = (compareEntropy[key] as number | null) ?? 0;
                          const delta = typeof a === "number" && typeof b === "number" ? (a - b) : null;
                          const highlight = delta !== null && Math.abs(delta) > 0.05 * Math.max(Math.abs(a as number), Math.abs(b as number), 0.001);
                          return (
                            <tr key={key}>
                              <td style={{ ...tdStyle, fontWeight: 600 }}>{label}</td>
                              <td style={tdStyle}>{typeof a === "number" ? (Number.isInteger(a) ? a.toLocaleString() : (a as number).toFixed(3)) : "—"}</td>
                              <td style={tdStyle}>{typeof b === "number" ? (Number.isInteger(b) ? b.toLocaleString() : (b as number).toFixed(3)) : "—"}</td>
                              <td style={{ ...tdStyle, color: !highlight ? "#9ca3af" : (delta! > 0 ? "#16a34a" : "#dc2626"), fontWeight: highlight ? 700 : 400 }}>
                                {delta !== null ? (delta > 0 ? "+" : "") + delta.toFixed(3) : "—"}
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  );
                })()}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function UploadPanel({ onCreated }: { onCreated: (t: TextResponse) => void }) {
  const { toast } = useToast();
  const [name, setName] = useState(""); const [type, setType] = useState("linguistic");
  const [delimiter, setDelimiter] = useState<"space" | "line" | "char">("space");
  const [direction, setDirection] = useState("unknown");
  const [rawContent, setRawContent] = useState(""); const [busy, setBusy] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const tokenise = (raw: string): string[] => {
    if (delimiter === "char") return raw.replace(/\s+/g, "").split("");
    if (delimiter === "line") return raw.split("\n").map(s => s.trim()).filter(Boolean);
    return raw.trim().split(/\s+/).filter(Boolean);
  };

  const handleUpload = async () => {
    if (!name.trim() || !rawContent.trim()) { toast("Name and content required", "warning"); return; }
    const content = tokenise(rawContent);
    if (!content.length) { toast("Content cannot be empty", "warning"); return; }
    setBusy(true);
    try { const t = await createText({ name: name.trim(), corpus_type: type, content, reading_direction: direction }); onCreated(t); setName(""); setRawContent(""); setDirection("unknown"); toast("Corpus created", "success"); }
    catch (e) { toast(e instanceof Error ? e.message : "Upload failed", "error"); }
    finally { setBusy(false); }
  };

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]; if (!file) return;
    if (!name) setName(file.name.replace(/\.[^.]+$/, ""));
    const reader = new FileReader();
    reader.onload = (ev) => {
      const raw = ev.target?.result as string;
      if (file.name.endsWith(".json")) {
        try { const p = JSON.parse(raw); setRawContent(Array.isArray(p) ? p.join(" ") : (p.content ?? []).join(" ") || raw); }
        catch { setRawContent(raw); }
      } else { setRawContent(raw); }
    };
    reader.readAsText(file); e.target.value = "";
  };

  return (
    <details style={{ marginBottom: "1.5rem" }}>
      <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13, padding: "8px 0" }}>+ Upload / import corpus</summary>
      <div style={{ marginTop: 10, padding: "1rem", border: "1px solid #e5e7eb", borderRadius: 8, maxWidth: 560 }}>
        <div style={{ marginBottom: 8 }}><label style={labelStyle}>Name</label><input value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Moby Dick" style={inputStyle} /></div>
        <div style={{ marginBottom: 8 }}>
          <label style={labelStyle}>Type</label>
          <select value={type} onChange={(e) => setType(e.target.value)} style={inputStyle}>{CORPUS_TYPES.map(t => <option key={t}>{t}</option>)}</select>
        </div>
        <div style={{ marginBottom: 8 }}>
          <label style={labelStyle}>Reading Direction</label>
          <select value={direction} onChange={(e) => setDirection(e.target.value)} style={inputStyle}>
            {DIR_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </div>
        <div style={{ marginBottom: 8 }}>
          <label style={labelStyle}>Tokenisation</label>
          <select value={delimiter} onChange={(e) => setDelimiter(e.target.value as "space" | "line" | "char")} style={inputStyle}>
            <option value="space">Space-separated</option><option value="line">Line-per-token</option><option value="char">Character-level</option>
          </select>
        </div>
        <div style={{ marginBottom: 10 }}>
          <label style={labelStyle}>Paste text content</label>
          <textarea value={rawContent} onChange={(e) => setRawContent(e.target.value)} rows={5} style={{ ...inputStyle, fontFamily: "monospace", resize: "vertical", fontSize: 11 }} placeholder="Paste text here…" />
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={handleUpload} disabled={busy} style={btnPrimary}>{busy ? "Uploading…" : "Upload"}</button>
          <button onClick={() => fileRef.current?.click()} style={btnSecondary}>↑ Import File (.txt/.csv/.json)</button>
          <input ref={fileRef} type="file" accept=".txt,.csv,.json" style={{ display: "none" }} onChange={handleFile} />
        </div>
      </div>
    </details>
  );
}

// ── World Language Corpus Catalogue Browser ─────────────────────────────────────────────

function CatalogueBrowser({ onImported }: { onImported: () => void }) {
  const { toast } = useToast();
  const [entries, setEntries] = useState<CorpusCatalogueEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [filterUD, setFilterUD] = useState<"all" | "undeciphered" | "deciphered">("all");

  const load = async () => {
    setLoading(true);
    try { setEntries(await listCorpusCatalogue()); }
    catch (e) { toast(e instanceof Error ? e.message : "Failed to load catalogue", "error"); }
    finally { setLoading(false); }
  };

  const handleImport = async (e: CorpusCatalogueEntry) => {
    if (!e.local_module) {
      toast(`No bundled module for '${e.name}'. Download from source URL and upload manually.`, "warning");
      return;
    }
    setImporting(e.id);
    try {
      const r = await importCorpusCatalogueEntry(e.id);
      if (r.imported) {
        setEntries(prev => prev.map(x => x.id === e.id ? { ...x, already_imported: true } : x));
        toast(`Imported '${r.name}' (${r.tokens?.toLocaleString()} tokens)`, "success");
        onImported();
      } else {
        toast(`'${r.name}' already in your corpora`, "info");
      }
    } catch (err) {
      toast(err instanceof Error ? err.message : "Import failed", "error");
    } finally { setImporting(null); }
  };

  const filtered = entries.filter(e => {
    const matchSearch = !search || e.name.toLowerCase().includes(search.toLowerCase()) || e.language.toLowerCase().includes(search.toLowerCase());
    const matchUD = filterUD === "all" || (filterUD === "undeciphered" ? e.is_undeciphered : !e.is_undeciphered);
    return matchSearch && matchUD;
  });

  // Group by language_family
  const groups: Record<string, CorpusCatalogueEntry[]> = {};
  for (const e of filtered) {
    const g = e.language_family || "Other";
    (groups[g] = groups[g] || []).push(e);
  }

  const scriptTypeColor: Record<string, string> = {
    abjad: "#7c3aed", syllabary: "#059669", logosyllabic: "#d97706",
    logographic: "#dc2626", alphabet: "#2563eb", unknown: "#6b7280",
  };

  return (
    <details style={{ marginBottom: "1.5rem" }}>
      <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13, padding: "8px 0",
        color: "#059669" }} onClick={() => entries.length === 0 && void load()}>
        🌍 Browse World Language Corpus Catalogue
      </summary>
      <div style={{ marginTop: 10, padding: "1rem", border: "1px solid #d1fae5", borderRadius: 8, background: "#f0fdf4" }}>
        <div style={{ display: "flex", gap: 8, marginBottom: 10, flexWrap: "wrap", alignItems: "center" }}>
          <input placeholder="Search language or name…" value={search} onChange={e => setSearch(e.target.value)}
            style={{ ...inputStyle, width: 220 }} />
          {(["all", "undeciphered", "deciphered"] as const).map(f => (
            <button key={f} onClick={() => setFilterUD(f)}
              style={{ ...btnSmall, background: filterUD === f ? "#059669" : undefined,
                color: filterUD === f ? "#fff" : undefined }}>
              {f === "all" ? "All" : f === "undeciphered" ? "🔓 Undeciphered" : "✔ Deciphered"}
            </button>
          ))}
          <button onClick={() => void load()} style={btnSmall}>⟳ Refresh</button>
          <span style={{ fontSize: 11, color: "#6b7280", marginLeft: "auto" }}>{filtered.length} entries</span>
        </div>
        {loading && <p style={{ color: "#6b7280", fontSize: 13 }}>Loading catalogue…</p>}
        {Object.entries(groups).sort(([a], [b]) => a.localeCompare(b)).map(([family, items]) => (
          <div key={family} style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: "#374151", textTransform: "uppercase",
              letterSpacing: 0.5, marginBottom: 4, paddingBottom: 2, borderBottom: "1px solid #d1fae5" }}>
              {family}
            </div>
            {items.map(e => {
              const sc = scriptTypeColor[e.script_type] ?? "#6b7280";
              const canImport = !!e.local_module;
              return (
                <div key={e.id} style={{ display: "flex", alignItems: "center", gap: 8, padding: "5px 0",
                  borderBottom: "1px solid #ecfdf5" }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" }}>
                      <span style={{ fontWeight: 600, fontSize: 12, color: e.is_undeciphered ? "#7c2d12" : "#1e3a5f" }}>
                        {e.name}
                      </span>
                      <span style={{ fontSize: 9, padding: "1px 5px", borderRadius: 8,
                        background: sc + "20", color: sc, fontWeight: 700 }}>{e.script_type}</span>
                      {e.is_undeciphered && <span style={{ fontSize: 9, color: "#dc2626", fontWeight: 700 }}>🔓</span>}
                    </div>
                    <div style={{ fontSize: 10, color: "#6b7280", marginTop: 1 }}>
                      {e.language} · {e.period} · ~{e.tokens_approx.toLocaleString()} tokens · {e.license}
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 4, flexShrink: 0 }}>
                    {e.already_imported
                      ? <span style={{ fontSize: 10, color: "#059669", fontWeight: 700 }}>✓ Imported</span>
                      : canImport
                      ? <button
                          onClick={() => void handleImport(e)}
                          disabled={importing === e.id}
                          style={{ ...btnSmall, background: importing === e.id ? "#d1d5db" : "#059669",
                            color: "#fff", border: "none", fontSize: 10 }}>
                          {importing === e.id ? "⏳" : "↓ Import"}
                        </button>
                      : <a href={e.source_url} target="_blank" rel="noopener noreferrer"
                          style={{ ...btnSmall, textDecoration: "none", fontSize: 10 }}>Source ↗</a>
                    }
                  </div>
                </div>
              );
            })}
          </div>
        ))}
        {!loading && filtered.length === 0 && entries.length > 0 && (
          <p style={{ color: "#6b7280", fontSize: 13 }}>No entries match your search.</p>
        )}
        {!loading && entries.length === 0 && (
          <p style={{ color: "#6b7280", fontSize: 13 }}>Click Refresh to load the catalogue.</p>
        )}
      </div>
    </details>
  );
}

// ── Anchor Set Editor ───────────────────────────────────────────────────────────────

function AnchorSetEditor() {
  const { toast } = useToast();
  const [sets, setSets] = useState<AnchorSet[]>([]);
  const [loading, setLoading] = useState(false);
  const [showNew, setShowNew] = useState(false);
  const [newName, setNewName] = useState("");
  const [newLang, setNewLang] = useState("");
  const [pairInput, setPairInput] = useState(""); // cipher<TAB>target per line

  const load = async () => {
    setLoading(true);
    try { setSets(await listAnchorSets()); }
    catch (e) { toast(e instanceof Error ? e.message : "Failed to load", "error"); }
    finally { setLoading(false); }
  };

  const parsePairs = (raw: string): AnchorPair[] =>
    raw.split("\n").map(l => l.trim()).filter(Boolean).map(l => {
      const [cipher, target, confidence, ...noteParts] = l.split(/\s+|\t/);
      return { cipher: cipher ?? "", target: target ?? "",
        confidence: (confidence ?? "high") as "high" | "medium" | "low",
        note: noteParts.join(" ") };
    }).filter(p => p.cipher && p.target);

  const handleCreate = async () => {
    if (!newName.trim()) { toast("Name required", "warning"); return; }
    try {
      const s = await createAnchorSet({ name: newName.trim(), language: newLang.trim(),
        pairs: parsePairs(pairInput) });
      setSets(prev => [s, ...prev]);
      setShowNew(false); setNewName(""); setNewLang(""); setPairInput("");
      toast("Anchor set created", "success");
    } catch (e) { toast(e instanceof Error ? e.message : "Create failed", "error"); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this anchor set?")) return;
    try { await deleteAnchorSet(id); setSets(prev => prev.filter(s => s.id !== id)); }
    catch (e) { toast(e instanceof Error ? e.message : "Delete failed", "error"); }
  };

  useEffect(() => { void load(); }, []);

  return (
    <details style={{ marginBottom: "1.5rem" }}>
      <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13, padding: "8px 0",
        color: "#7c3aed" }}>
        ⚓ Anchor Sets ({sets.length})
      </summary>
      <div style={{ marginTop: 10, padding: "1rem", border: "1px solid #ede9fe", borderRadius: 8, background: "#faf5ff" }}>
        <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
          <button onClick={() => setShowNew(s => !s)} style={{ ...btnSmall, background: "#7c3aed", color: "#fff", border: "none" }}>+ New Set</button>
          <button onClick={() => void load()} style={btnSmall}>⟳ Refresh</button>
        </div>
        {showNew && (
          <div style={{ padding: 12, border: "1px solid #a78bfa", borderRadius: 6, marginBottom: 12, background: "#fff" }}>
            <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
              <div style={{ flex: 2 }}>
                <label style={labelStyle}>Set Name</label>
                <input value={newName} onChange={e => setNewName(e.target.value)}
                  placeholder="e.g. Fuls Ugaritic Anchors" style={inputStyle} />
              </div>
              <div style={{ flex: 1 }}>
                <label style={labelStyle}>Language (optional)</label>
                <input value={newLang} onChange={e => setNewLang(e.target.value)}
                  placeholder="e.g. Ugaritic" style={inputStyle} />
              </div>
            </div>
            <div style={{ marginBottom: 8 }}>
              <label style={labelStyle}>Anchor Pairs (one per line: cipher target confidence note)</label>
              <textarea value={pairInput} onChange={e => setPairInput(e.target.value)}
                rows={5} style={{ ...inputStyle, fontFamily: "monospace", fontSize: 11, resize: "vertical" }}
                placeholder={"004 T high Fuls verified\n066 m high Fuls verified\n208 n high Fuls verified"} />
              <div style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>Format: cipher_sign target confidence(high/medium/low) note</div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={() => void handleCreate()} style={{ ...btnSmall, background: "#7c3aed", color: "#fff", border: "none" }}>Create</button>
              <button onClick={() => setShowNew(false)} style={btnSmall}>Cancel</button>
            </div>
          </div>
        )}
        {loading && <p style={{ fontSize: 13, color: "#6b7280" }}>Loading…</p>}
        {sets.length === 0 && !loading && <p style={{ fontSize: 13, color: "#6b7280" }}>No anchor sets yet. Create one above.</p>}
        {sets.map(s => (
          <div key={s.id} style={{ border: "1px solid #ede9fe", borderRadius: 6, padding: "8px 12px",
            marginBottom: 6, background: "#fff" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ flex: 1 }}>
                <span style={{ fontWeight: 600, fontSize: 12 }}>{s.name}</span>
                {s.language && <span style={{ fontSize: 11, color: "#7c3aed", marginLeft: 6 }}>{s.language}</span>}
                <span style={{ fontSize: 11, color: "#9ca3af", marginLeft: 6 }}>{s.pairs.length} pairs</span>
              </div>
              <button onClick={() => handleDelete(s.id)}
                style={{ ...btnMini, color: "#dc2626", borderColor: "#fca5a5" }}>Delete</button>
            </div>
            {s.pairs.length > 0 && (
              <div style={{ marginTop: 4, display: "flex", gap: 4, flexWrap: "wrap" }}>
                {s.pairs.slice(0, 8).map((p, i) => (
                  <span key={i} style={{ fontSize: 10, padding: "1px 5px", borderRadius: 4,
                    background: p.confidence === "high" ? "#d1fae5" : p.confidence === "medium" ? "#fef3c7" : "#fee2e2",
                    color: "#374151" }}>
                    {p.cipher}→{p.target}
                  </span>
                ))}
                {s.pairs.length > 8 && <span style={{ fontSize: 10, color: "#9ca3af" }}>+{s.pairs.length - 8} more</span>}
              </div>
            )}
          </div>
        ))}
      </div>
    </details>
  );
}

export function CorporaView({ onSelect }: { onSelect?: (id: string, name: string) => void }) {
  const [texts, setTexts] = useState<TextResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try { setTexts(await listTexts()); setError(null); }
    catch (e) { setError(e instanceof Error ? e.message : "Failed to load"); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>Corpora</h2>
        <button onClick={load} style={{ ...btnPrimary, background: "#6b7280", padding: "4px 12px", fontSize: 12 }}>⟳ Refresh</button>
      </div>
      <UploadPanel onCreated={(t) => setTexts((prev) => [t, ...prev])} />
      <CatalogueBrowser onImported={() => void load()} />
      <AnchorSetEditor />
      {loading && <p style={{ color: "#6b7280", fontSize: 13 }}>Loading…</p>}
      {error && <p style={{ color: "#dc2626", fontSize: 13 }}>{error}</p>}
      {!loading && !error && texts.length === 0 && <p style={{ color: "#6b7280", fontSize: 13 }}>No corpora yet. Upload or import one above.</p>}
      {!loading && texts.length > 0 && (
        <div>
          <div style={{ fontSize: 12, color: "#9ca3af", marginBottom: 8 }}>{texts.length} corpus entries — click any row to expand</div>
          {texts.map((t) => (
            <CorpusCard key={t.id} text={t} allTexts={texts}
              onUpdated={(u) => setTexts((prev) => prev.map((x) => x.id === u.id ? u : x))}
              onDeleted={(id) => setTexts((prev) => prev.filter((x) => x.id !== id))} />
          ))}
        </div>
      )}
      {onSelect && texts.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 6 }}>Quick-select:</div>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
            {texts.map((t) => <button key={t.id} onClick={() => onSelect(t.id, t.name)} style={btnSmall}>{t.name}</button>)}
          </div>
        </div>
      )}
    </div>
  );
}

const sLabel: React.CSSProperties = { fontSize: 10, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 };
const inputStyle: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box", display: "block" };
const labelStyle: React.CSSProperties = { display: "block", fontWeight: 600, fontSize: 12, color: "#374151", marginBottom: 3 };
const btnPrimary: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer", fontWeight: 600, whiteSpace: "nowrap" };
const btnSecondary: React.CSSProperties = { background: "#fff", color: "#374151", border: "1px solid #d1d5db", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer", whiteSpace: "nowrap" };
const btnSmall: React.CSSProperties = { padding: "3px 10px", border: "1px solid #e5e7eb", borderRadius: 4, cursor: "pointer", fontSize: 11, background: "#f9fafb", color: "#374151" };
const btnMini: React.CSSProperties = { padding: "2px 7px", border: "1px solid #e5e7eb", borderRadius: 4, cursor: "pointer", fontSize: 10, background: "#f9fafb", color: "#374151" };
const thStyle: React.CSSProperties = { textAlign: "left", padding: "4px 10px 4px 0", borderBottom: "2px solid #e5e7eb", color: "#374151" };
const tdStyle: React.CSSProperties = { padding: "3px 10px 3px 0", borderBottom: "1px solid #f3f4f6", verticalAlign: "top" };
