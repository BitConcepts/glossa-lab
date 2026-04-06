/**
 * CorporaView — full-featured corpus management.
 * Cards expand on click; each card shows: Browse, Edit, Stats, N-grams, Concordance, AI tabs.
 * Includes file import, export, copy, benchmark comparison.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  analyzeCorpus, critiqueCorpus, createText, deleteText, detectCorpusAnomalies,
  getCorpusConcordance, getCorpusEntropy, getCorpusExportUrl, getCorpusNgrams,
  listTexts, updateText,
  type ConcordanceResult, type EntropyResult, type NgramEntry, type TextResponse,
} from "../api";
import { ContextMenuOverlay, copyItems, useContextMenu } from "../hooks/useContextMenu";
import { useToast } from "../hooks/useToast";

const CORPUS_TYPES = ["linguistic", "ancient", "dna", "code", "random", "other"];
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

function AIResultPanel({ result, onClose }: { result: Record<string, unknown>; onClose: () => void }) {
  const skip = new Set(["text_id", "name", "stats"]);
  return (
    <div style={{ marginTop: 10, border: "1px solid #a78bfa", borderRadius: 8, overflow: "hidden" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#7c3aed", padding: "7px 12px" }}>
        <span style={{ color: "#fff", fontWeight: 700, fontSize: 12 }}>✨ AI Result</span>
        <button onClick={onClose} style={{ border: "none", background: "none", color: "#fff", cursor: "pointer", fontSize: 14 }}>×</button>
      </div>
      <div style={{ padding: "12px 14px", background: "#faf5ff", display: "flex", flexDirection: "column", gap: 10 }}>
        {Object.entries(result).filter(([k]) => !skip.has(k)).map(([k, v]) => {
          const label = k.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
          if (Array.isArray(v)) return (
            <div key={k}>
              <div style={sLabel}>{label}</div>
              <ul style={{ margin: 0, paddingLeft: 18 }}>
                {(v as unknown[]).map((item, i) => (
                  <li key={i} style={{ fontSize: 12, lineHeight: 1.5, color: "#374151" }}>
                    {typeof item === "object" ? JSON.stringify(item) : String(item)}
                  </li>
                ))}
              </ul>
            </div>
          );
          if (typeof v === "object" && v !== null) return (
            <div key={k}>
              <div style={sLabel}>{label}</div>
              <pre style={{ margin: 0, fontSize: 10, background: "#1e293b", color: "#e2e8f0", padding: "6px 10px", borderRadius: 4, overflowX: "auto" }}>
                {JSON.stringify(v, null, 2)}
              </pre>
            </div>
          );
          return (
            <div key={k}>
              <div style={sLabel}>{label}</div>
              <p style={{ margin: 0, fontSize: 12, color: "#374151", lineHeight: 1.6 }}>{String(v)}</p>
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
  const [aiResult, setAiResult] = useState<Record<string, unknown> | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  const [compareId, setCompareId] = useState<string>("");
  const [compareEntropy, setCompareEntropy] = useState<EntropyResult | null>(null);
  const [myEntropy, setMyEntropy] = useState<EntropyResult | null>(null);
  const [compareLoading, setCompareLoading] = useState(false);

  const fileRef = useRef<HTMLInputElement>(null);

  const { menu: ctxMenu, show: showCtx, close: closeCtx } = useContextMenu();

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
      const updated = await updateText(text.id, { name: editName.trim(), corpus_type: editType, content });
      onUpdated(updated);
      toast("Corpus updated", "success");
    } catch (e) { toast(e instanceof Error ? e.message : "Save failed", "error"); }
    finally { setSaving(false); }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(text.content.join(" ")).then(() => toast("Copied to clipboard", "success"));
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

  const handleAI = async () => {
    setAiLoading(true); setAiResult(null);
    try {
      const fn = aiMode === "analyze" ? analyzeCorpus : aiMode === "anomalies" ? detectCorpusAnomalies : critiqueCorpus;
      setAiResult(await fn(text.id) as Record<string, unknown>);
    } catch (e) { toast(e instanceof Error ? e.message : "AI error", "error"); }
    finally { setAiLoading(false); }
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
        <span style={{ flex: 1, fontWeight: 600, fontSize: 13, color: "#111827" }}>{text.name}</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{text.content.length.toLocaleString()} tokens</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>Σ {text.alphabet_size}</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{text.created_at.slice(0, 10)}</span>
        <span onClick={(e) => e.stopPropagation()} style={{ display: "flex", gap: 4 }}>
          <button onClick={handleCopy} title="Copy" style={btnMini}>⎘</button>
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
                    <button key={m} onClick={() => { setAiMode(m); setAiResult(null); }}
                      style={{ ...btnSmall, background: aiMode === m ? "#7c3aed" : "#f3f4f6", color: aiMode === m ? "#fff" : "#374151" }}>
                      {m === "analyze" ? "Corpus Analysis" : m === "anomalies" ? "Anomaly Detection" : "Critique"}
                    </button>
                  ))}
                  <button onClick={handleAI} disabled={aiLoading} style={{ ...btnPrimary, background: "#7c3aed", marginLeft: "auto" }}>
                    {aiLoading ? "✨ Thinking…" : "✨ Run AI"}
                  </button>
                </div>
                {aiResult && <AIResultPanel result={aiResult} onClose={() => setAiResult(null)} />}
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
    try { const t = await createText({ name: name.trim(), corpus_type: type, content }); onCreated(t); setName(""); setRawContent(""); toast("Corpus created", "success"); }
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
