/**
 * AIChatWindow — floating, draggable AI chat popup.
 *
 * Features:
 *  - Markdown rendering (headers, bold, italic, code, lists, links)
 *  - Date/time on every message
 *  - Copy message / Copy all buttons
 *  - Context window indicator with token estimate + auto-compress at 90%
 *  - Context selector: study → experiment → report
 *  - File upload (reads text into message)
 *  - URL paste-and-fetch
 *  - Delete individual messages / clear all
 *  - Pre-filled context + prompt from openChat() calls
 *  - Boundary-clamped dragging
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  aiChat,
  getLocalCtxLength,
  getResearchContext,
  listExperiments,
  listStudies,
  listTexts,
  type ChatMessage,
  type ExperimentMeta,
  type StudyResponse,
  type TextResponse,
} from "../api";
import { useAIChat } from "../hooks/useAIChat";
import { useToast } from "../hooks/useToast";

// ── Markdown renderer ─────────────────────────────────────────────────────────

/** Render a single markdown table block to HTML. */
function renderTableBlock(block: string): string {
  // Each line should start with '|'
  const lines = block.split("\n").map(l => l.trim()).filter(l => l.startsWith("|"));
  if (lines.length < 3) return block;

  // Parse a row: split on | and drop first/last empty segments.
  // "| A | B | C |" → ["A", "B", "C"]
  const parseRow = (line: string): string[] =>
    line.split("|").slice(1, -1).map(c => c.trim());

  const headers = parseRow(lines[0]);
  // lines[1] is the separator row — skip it
  const rows = lines.slice(2).filter(l => l.trim()).map(parseRow);

  const thStyle = [
    "background:#1e3a5f",
    "color:#e2e8f0",
    "padding:5px 8px",
    "text-align:left",
    "font-size:11px",
    "font-weight:600",
    "white-space:nowrap",
    "border:1px solid #334155",
  ].join(";");

  const tdStyleBase = [
    "padding:4px 8px",
    "font-size:11px",
    "border:1px solid #e5e7eb",
    "vertical-align:top",
  ].join(";");

  const thead = `<thead><tr>${headers
    .map(h => `<th style='${thStyle}'>${h}</th>`)
    .join("")}</tr></thead>`;

  const tbody = `<tbody>${rows
    .map((cells, ri) => {
      const rowBg = ri % 2 === 0 ? "" : "background:#f8fafc;";
      const tds = headers.map((_, ci) => {
        const cell = cells[ci] ?? "";
        return `<td style='${tdStyleBase};${rowBg}'>${cell}</td>`;
      }).join("");
      return `<tr>${tds}</tr>`;
    })
    .join("")}</tbody>`;

  return [
    "<div style='overflow-x:auto;margin:8px 0;border-radius:5px;border:1px solid #e5e7eb'>",
    "<table style='border-collapse:collapse;width:100%;font-size:11px'>",
    thead,
    tbody,
    "</table></div>",
  ].join("");
}

/**
 * Render markdown to HTML.
 * Tables are extracted first (placeholder technique) so that the line-by-line
 * substitutions do not corrupt multi-line table blocks.
 */
function renderMd(raw: string): string {
  // 1. HTML-escape user content.
  let html = raw
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // 2. Extract table blocks before any other substitution.
  //    A table = header row | separator row (|---|) | 1+ data rows.
  //    All lines start with '|'.
  const tables: string[] = [];
  html = html.replace(
    /(\|[^\n]+\n\|[ \t|:^-]+\n(?:\|[^\n]+\n?)+)/g,
    (match) => {
      tables.push(renderTableBlock(match));
      return `%%TBL${tables.length - 1}%%`;
    }
  );

  // 3. Apply all other markdown transformations.
  html = html
    // Code blocks
    .replace(
      /```[\w]*\n?([\s\S]*?)```/g,
      "<pre style='background:#1e293b;color:#e2e8f0;padding:8px 12px;" +
      "border-radius:5px;font-size:11px;overflow-x:auto;margin:6px 0'>$1</pre>"
    )
    // Inline code
    .replace(
      /`([^`]+)`/g,
      "<code style='background:#f1f5f9;padding:1px 4px;border-radius:3px;" +
      "font-size:12px;font-family:monospace'>$1</code>"
    )
    // Headers
    .replace(/^### (.+)$/gm, "<div style='font-size:13px;font-weight:700;margin:10px 0 4px'>$1</div>")
    .replace(/^## (.+)$/gm,  "<div style='font-size:14px;font-weight:700;margin:12px 0 5px'>$1</div>")
    .replace(/^# (.+)$/gm,   "<div style='font-size:15px;font-weight:800;margin:14px 0 6px'>$1</div>")
    // Bold / italic
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g,     "<em>$1</em>")
    // Links
    .replace(
      /\[([^\]]+)\]\(([^)]+)\)/g,
      "<a href='$2' target='_blank' rel='noopener noreferrer' style='color:#2563eb'>$1</a>"
    )
    // Unordered list items
    .replace(/^[-*] (.+)$/gm, "<li style='margin:2px 0;margin-left:16px'>$1</li>")
    // Numbered list items
    .replace(/^\d+\. (.+)$/gm, "<li style='margin:2px 0;margin-left:16px;list-style-type:decimal'>$1</li>")
    // Horizontal rule
    .replace(/^---$/gm, "<hr style='border:none;border-top:1px solid #e5e7eb;margin:10px 0'>")
    // Paragraph breaks / line breaks
    .replace(/\n\n/g, "</p><p style='margin:5px 0'>")
    .replace(/\n/g, "<br>")
    .replace(/^/, "<p style='margin:0'>").replace(/$/, "</p>");

  // 4. Restore extracted tables (they survive the substitutions as %%TBLn%%).
  tables.forEach((t, i) => {
    html = html.replace(`%%TBL${i}%%`, t);
  });

  return html;
}

function fmtTime(ts: number): string {
  return new Date(ts).toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

// Rough token estimate: 4 chars ≈ 1 token
function estimateTokens(messages: MsgUI[]): number {
  return Math.ceil(messages.reduce((acc, m) => acc + m.content.length, 0) / 4);
}

// ── Types ─────────────────────────────────────────────────────────────────────

interface MsgUI extends ChatMessage {
  id: number;
  timestamp: number;
  loading?: boolean;
  error?: boolean;
}

let _msgId = 0;

// ── Main component ────────────────────────────────────────────────────────────

export function AIChatWindow({ panelHeight = 0 }: { panelHeight?: number }) {
  const { isOpen, request, closeChat, setDocked, isDocked } = useAIChat();
  const { toast } = useToast();

  const [messages, setMessages] = useState<MsgUI[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [compressing, setCompressing] = useState(false);

  // Context
  const [contextType, setContextType] = useState<"" | "corpus" | "experiment" | "study" | "research">("");
  const [contextId, setContextId] = useState("");
  const [corpora, setCorpora] = useState<TextResponse[]>([]);
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [studies, setStudies] = useState<StudyResponse[]>([]);
  const [researchSummary, setResearchSummary] = useState<{
    n_assigned_signs: number; token_coverage_pct: number; next_steps: string[];
  } | null>(null);

  // Window position (drag)
  const [pos, setPos] = useState<{ x: number; y: number } | null>(null);
  const size = { w: 440, h: 580 };
  const dragging = useRef(false);
  const dragOffset = useRef({ x: 0, y: 0 });
  const winRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  /** Clamp a proposed {x,y} so the window stays fully inside the viewport. */
  const clamp = useCallback((x: number, y: number) => ({
    x: Math.max(0, Math.min(window.innerWidth  - size.w, x)),
    y: Math.max(0, Math.min(window.innerHeight - size.h, y)),
  }), [size.w, size.h]);

  // Reset position to default (bottom-right near bubble) when chat is closed
  useEffect(() => {
    if (!isOpen) setPos(null);
  }, [isOpen]);

  // Reclamp on viewport resize so window can never drift off-screen
  useEffect(() => {
    const onResize = () => {
      setPos((prev) => {
        if (!prev) return null;
        return clamp(prev.x, prev.y);
      });
    };
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [clamp]);

  // Token tracking
  const maxCtx = getLocalCtxLength();
  const usedTokens = estimateTokens(messages);
  const ctxPct = Math.min(100, Math.round((usedTokens / maxCtx) * 100));
  const ctxWarning = ctxPct >= 75;
  const ctxCritical = ctxPct >= 90;

  // Load resource lists once
  useEffect(() => {
    listTexts().then(setCorpora).catch(() => {});
    listExperiments().then(setExperiments).catch(() => {});
    listStudies().then(setStudies).catch(() => {});
  }, []);

  // Apply incoming chat request (context + initial prompt)
  useEffect(() => {
    if (!request) return;
    if (request.contextType !== undefined) setContextType(request.contextType ?? "");
    if (request.contextId) setContextId(request.contextId);
    if (request.initialPrompt) setInput(request.initialPrompt);
    setTimeout(() => textareaRef.current?.focus(), 100);
  }, [request]);

  // Scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Drag handlers
  const onDragStart = useCallback((e: React.MouseEvent) => {
    if (!winRef.current) return;
    dragging.current = true;
    const rect = winRef.current.getBoundingClientRect();
    dragOffset.current = { x: e.clientX - rect.left, y: e.clientY - rect.top };
    e.preventDefault();
  }, []);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!dragging.current) return;
      setPos(clamp(
        e.clientX - dragOffset.current.x,
        e.clientY - dragOffset.current.y,
      ));
    };
    const onUp = () => { dragging.current = false; };
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    return () => { window.removeEventListener("mousemove", onMove); window.removeEventListener("mouseup", onUp); };
  }, [clamp]);

  // ── Auto-compress ─────────────────────────────────────────────────────────

  const compress = useCallback(async () => {
    if (messages.length < 4) return;
    setCompressing(true);
    try {
      const summary = await aiChat({
        messages: [
          { role: "system", content: "Summarise the following conversation in 3-5 bullet points. Be concise. Return plain text only." },
          ...messages.filter(m => !m.loading).map(({ role, content }) => ({ role, content })),
        ],
      });
      const summaryText = `[Auto-compressed ${messages.length} messages]\n${summary.content as string}`;
      setMessages([{
        id: ++_msgId,
        role: "assistant",
        content: summaryText,
        timestamp: Date.now(),
      }]);
      toast("Chat context compressed", "info");
    } catch { toast("Compression failed", "error"); }
    finally { setCompressing(false); }
  }, [messages, toast]);

  // Auto-compress when ctx hits 90%
  useEffect(() => {
    if (ctxPct >= 90 && !compressing && !busy && messages.length > 4) compress();
  }, [ctxPct, compressing, busy, messages.length, compress]);

  // ── Send message ──────────────────────────────────────────────────────────

  const send = useCallback(async (overrideText?: string) => {
    const text = (overrideText ?? input).trim();
    if (!text || busy) return;
    setInput("");

    const userMsg: MsgUI = { id: ++_msgId, role: "user", content: text, timestamp: Date.now() };
    const loadingMsg: MsgUI = { id: ++_msgId, role: "assistant", content: "", timestamp: Date.now(), loading: true };
    setMessages(prev => [...prev, userMsg, loadingMsg]);
    setBusy(true);

    try {
      const history = [...messages, userMsg].filter(m => !m.loading).map(({ role, content }) => ({ role, content }));
      const result = await aiChat({
        messages: history,
        context_type: contextType || null,
        context_id: contextId || null,
      });
      setMessages(prev => prev.map(m =>
        m.id === loadingMsg.id
          ? { ...m, content: result.content as string, loading: false, timestamp: Date.now() }
          : m
      ));
    } catch (e) {
      const errMsg = e instanceof Error ? e.message : "AI error";
      setMessages(prev => prev.map(m =>
        m.id === loadingMsg.id
          ? { ...m, content: `Error: ${errMsg}`, loading: false, error: true, timestamp: Date.now() }
          : m
      ));
    } finally {
      setBusy(false);
    }
  }, [input, busy, messages, contextType, contextId]);

  // ── File upload ───────────────────────────────────────────────────────────

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const content = ev.target?.result as string;
      const preview = content.slice(0, 2000);
      setInput(prev => `${prev}\n\n[File: ${file.name}]\n\`\`\`\n${preview}${content.length > 2000 ? "\n… (truncated)" : ""}\n\`\`\``);
    };
    reader.readAsText(file);
    e.target.value = "";
  };

  const handleUrlPaste = useCallback(async () => {
    const url = prompt("Enter a URL to fetch and include as context:");
    if (!url?.startsWith("http")) return;
    try {
      toast("Fetching URL…", "info");
      const resp = await fetch(url);
      const text = await resp.text();
      const stripped = text.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").slice(0, 3000);
      setInput(prev => `${prev}\n\n[URL: ${url}]\n${stripped}…`);
    } catch { toast("Could not fetch URL", "error"); }
  }, [toast]);

  const contextLabel = () => {
    if (contextType === "research") return "Research";
    if (!contextType || !contextId) return null;
    const map: Record<string, string | undefined> = {
      corpus: corpora.find(c => c.id === contextId)?.name,
      experiment: experiments.find(e => e.id === contextId)?.name,
      study: studies.find(s => s.id === contextId)?.name,
    };
    return map[contextType];
  };

  const loadResearchContext = useCallback(async () => {
    setContextType("research");
    setContextId("");
    setResearchSummary(null);
    try {
      const data = await getResearchContext();
      setResearchSummary(data.summary);
      toast("Research context loaded", "info");
    } catch { toast("Could not load research context", "error"); }
  }, [toast]);

  // When docked, render via BottomPanel instead
  if (!isOpen || isDocked) return null;

  // Default position: bottom-right, above the panel + bubble
  // Clamped so it can never overflow the viewport even at first render.
  const defaultRight = 84;                                   // leave room for bubble (width 48 + margin)
  const defaultBottom = panelHeight + 82;                    // above panel + bubble (height 48 + gap)
  const defaultLeft = Math.max(0, window.innerWidth  - size.w - defaultRight);
  const defaultTop  = Math.max(0, window.innerHeight - size.h - defaultBottom);

  const winStyle: React.CSSProperties = pos
    ? { position: "fixed", left: pos.x, top: pos.y, width: size.w, height: size.h, zIndex: 8500 }
    : { position: "fixed", left: defaultLeft, top: defaultTop, width: size.w, height: size.h, zIndex: 8500 };

  return (
    <div ref={winRef} style={{
      ...winStyle,
      background: "#fff",
      borderRadius: 10,
      boxShadow: "0 20px 60px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.08)",
      display: "flex", flexDirection: "column",
      overflow: "hidden",
    }}>
      {/* Header — drag handle */}
      <div
        onMouseDown={onDragStart}
        style={{ background: "#1e3a5f", padding: "9px 12px", cursor: "grab", display: "flex", alignItems: "center", gap: 8, userSelect: "none", flexShrink: 0 }}
      >
        <span style={{ fontSize: 14 }}>✨</span>
        <span style={{ flex: 1, fontWeight: 700, fontSize: 13, color: "#fff" }}>Glossa AI</span>

        {/* Context window indicator */}
        <div style={{ display: "flex", alignItems: "center", gap: 5 }} title={`~${usedTokens.toLocaleString()} / ${maxCtx.toLocaleString()} tokens`}>
          <div style={{ width: 60, height: 4, background: "rgba(255,255,255,0.2)", borderRadius: 2, overflow: "hidden" }}>
            <div style={{
              height: "100%",
              width: `${ctxPct}%`,
              background: ctxCritical ? "#ef4444" : ctxWarning ? "#f59e0b" : "#34d399",
              borderRadius: 2,
              transition: "width 0.3s",
            }} />
          </div>
          <span style={{ fontSize: 9, color: "rgba(255,255,255,0.7)" }}>{ctxPct}%</span>
        </div>

        {compressing && <span style={{ fontSize: 10, color: "#fcd34d" }}>compressing…</span>}

        <button onClick={() => setDocked(true)} title="Dock to bottom panel"
          style={{ border: "none", background: "none", color: "rgba(255,255,255,0.6)", cursor: "pointer", fontSize: 13, padding: "0 4px" }}>⊟</button>
        <button onClick={() => { setMessages([]); }} title="Clear chat"
          style={{ border: "none", background: "none", color: "rgba(255,255,255,0.6)", cursor: "pointer", fontSize: 12, padding: "0 4px" }}>🗑</button>
        <button onClick={closeChat}
          style={{ border: "none", background: "none", color: "rgba(255,255,255,0.8)", cursor: "pointer", fontSize: 16, padding: "0 2px" }}>×</button>
      </div>

      {/* Context selector */}
      <div style={{ padding: "6px 10px", borderBottom: "1px solid #f3f4f6", background: "#fafafa", display: "flex", gap: 4, flexWrap: "wrap", alignItems: "center", flexShrink: 0 }}>
        <span style={{ fontSize: 10, color: "#9ca3af", flexShrink: 0 }}>Context:</span>
        {(["", "corpus", "experiment", "study"] as const).map((ct) => (
          <button key={ct || "none"} onClick={() => { setContextType(ct); setContextId(""); setResearchSummary(null); }}
            style={{ padding: "2px 7px", borderRadius: 4, border: "1px solid", cursor: "pointer", fontSize: 10,
              background: contextType === ct ? "#1e3a5f" : "#fff",
              borderColor: contextType === ct ? "#1e3a5f" : "#e5e7eb",
              color: contextType === ct ? "#fff" : "#6b7280" }}>
            {ct || "Global"}
          </button>
        ))}
        {/* Research context button */}
        <button
          onClick={loadResearchContext}
          title="Load current decipherment state (sign assignments, LEDGER, reports)"
          style={{ padding: "2px 7px", borderRadius: 4, border: "1px solid", cursor: "pointer", fontSize: 10,
            background: contextType === "research" ? "#7c3aed" : "#fff",
            borderColor: contextType === "research" ? "#7c3aed" : "#e5e7eb",
            color: contextType === "research" ? "#fff" : "#6b7280" }}>
          🔬 Research
        </button>
        {contextType === "corpus" && (
          <select value={contextId} onChange={e => setContextId(e.target.value)} style={selectSt}>
            <option value="">— corpus —</option>
            {corpora.map(c => <option key={c.id} value={c.id}>{c.name.slice(0, 25)}</option>)}
          </select>
        )}
        {contextType === "experiment" && (
          <select value={contextId} onChange={e => setContextId(e.target.value)} style={selectSt}>
            <option value="">— experiment —</option>
            {experiments.map(e => <option key={e.id} value={e.id}>{e.name.slice(0, 25)}</option>)}
          </select>
        )}
        {contextType === "study" && (
          <select value={contextId} onChange={e => setContextId(e.target.value)} style={selectSt}>
            <option value="">— study —</option>
            {studies.map(s => <option key={s.id} value={s.id}>{s.name.slice(0, 25)}</option>)}
          </select>
        )}
        {contextLabel() && contextType !== "research" && (
          <span style={{ fontSize: 10, padding: "1px 6px", background: "#eff6ff", color: "#2563eb", borderRadius: 4, fontWeight: 600 }}>
            📎 {contextLabel()?.slice(0, 20)}
          </span>
        )}
        {contextType === "research" && researchSummary && (
          <span style={{ fontSize: 9, padding: "2px 7px", background: "#f3e8ff", color: "#7c3aed",
            borderRadius: 4, fontWeight: 600, display: "flex", alignItems: "center", gap: 4 }}
            title={researchSummary.next_steps[0] ?? ""}
          >
            🔬 {researchSummary.n_assigned_signs} signs · {researchSummary.token_coverage_pct}% coverage
          </span>
        )}
        {contextType === "research" && !researchSummary && (
          <span style={{ fontSize: 9, color: "#9ca3af" }}>loading…</span>
        )}
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: "10px 12px", display: "flex", flexDirection: "column", gap: 8 }}>
        {messages.length === 0 && (
          <div style={{ textAlign: "center", padding: "2rem 1rem", color: "#9ca3af" }}>
            <div style={{ fontSize: 28, marginBottom: 8 }}>{contextType === "research" ? "🔬" : "✨"}</div>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 6, color: "#374151" }}>
              {contextType === "research" ? "Research Mode" : "Glossa AI"}
            </div>
            {contextType === "research" && researchSummary ? (
              <div style={{ fontSize: 11, lineHeight: 1.7, maxWidth: 360, margin: "0 auto", color: "#374151", textAlign: "left" }}>
                <div>📊 <strong>{researchSummary.n_assigned_signs} signs assigned</strong> · {researchSummary.token_coverage_pct}% token coverage</div>
                {researchSummary.next_steps[0] && (
                  <div style={{ marginTop: 6, padding: "6px 8px", background: "#f3e8ff", borderRadius: 5, fontSize: 10 }}>
                    Next: {researchSummary.next_steps[0].slice(0, 120)}
                  </div>
                )}
              </div>
            ) : (
              <div style={{ fontSize: 12, lineHeight: 1.6, maxWidth: 300, margin: "0 auto" }}>
                Ask about Indus Script, entropy analysis, experiment design, or anything research-related.
              </div>
            )}
            <div style={{ display: "flex", gap: 4, justifyContent: "center", flexWrap: "wrap", marginTop: 12 }}>
              {(contextType === "research" ? [
                "What should we work on next?",
                "Assign values to the unknown TMK signs",
                "Analyse the genitive pattern [615][503][752]",
              ] : [
                "What is H2/H1 for natural language?",
                "Suggest experiments for entropy analysis",
                "Explain the Ventris method",
              ]).map(s => (
                <button key={s} onClick={() => send(s)} style={{ padding: "4px 8px", border: "1px solid #e5e7eb", borderRadius: 5, background: "#fff", fontSize: 10, cursor: "pointer", color: "#374151" }}>{s}</button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={msg.id} style={{ display: "flex", flexDirection: msg.role === "user" ? "row-reverse" : "row", gap: 6, alignItems: "flex-start" }}>
            <div style={{ width: 24, height: 24, borderRadius: "50%", background: msg.role === "user" ? "#1e3a5f" : msg.error ? "#dc2626" : "#7c3aed", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, color: "#fff", fontWeight: 700, flexShrink: 0 }}>
              {msg.role === "user" ? "U" : "G"}
            </div>
            <div style={{ maxWidth: "80%", display: "flex", flexDirection: "column", gap: 2 }}>
              <div style={{
                padding: "8px 11px", borderRadius: 8, fontSize: 12, lineHeight: 1.65,
                background: msg.role === "user" ? "#1e3a5f" : msg.error ? "#fef2f2" : "#f8f9fa",
                color: msg.role === "user" ? "#fff" : msg.error ? "#dc2626" : "#111827",
                border: msg.role === "user" ? "none" : `1px solid ${msg.error ? "#fca5a5" : "#e5e7eb"}`,
              }}>
                {msg.loading
                  ? <span style={{ color: "#9ca3af" }}>✨ Thinking…</span>
                  : msg.role === "user"
                    ? <span style={{ whiteSpace: "pre-wrap" }}>{msg.content}</span>
                    : <div dangerouslySetInnerHTML={{ __html: renderMd(msg.content) }} />
                }
              </div>
              {/* Timestamp + actions */}
              <div style={{ display: "flex", gap: 6, alignItems: "center", paddingLeft: msg.role === "user" ? 0 : 4, justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
                <span style={{ fontSize: 9, color: "#9ca3af" }}>{fmtTime(msg.timestamp)}</span>
                {!msg.loading && (
                  <>
                    <button onClick={() => navigator.clipboard.writeText(msg.content).then(() => toast("Copied", "success"))}
                      title="Copy message"
                      style={{ border: "none", background: "none", cursor: "pointer", fontSize: 9, color: "#9ca3af", padding: 0 }}>⎘</button>
                    <button onClick={() => setMessages(prev => prev.filter((_, i) => i !== idx))}
                      title="Delete message"
                      style={{ border: "none", background: "none", cursor: "pointer", fontSize: 9, color: "#9ca3af", padding: 0 }}>×</button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Copy all */}
        {messages.length > 0 && (
          <div style={{ display: "flex", justifyContent: "center", marginTop: 4 }}>
            <button onClick={() => {
              const txt = messages.filter(m => !m.loading).map(m => `[${m.role.toUpperCase()} ${fmtTime(m.timestamp)}]\n${m.content}`).join("\n\n");
              navigator.clipboard.writeText(txt).then(() => toast("Chat copied", "success"));
            }} style={{ fontSize: 10, color: "#9ca3af", background: "none", border: "none", cursor: "pointer" }}>
              ⎘ Copy entire chat
            </button>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Context window warning */}
      {ctxWarning && (
        <div style={{ padding: "4px 10px", background: ctxCritical ? "#fef2f2" : "#fef3c7", borderTop: "1px solid " + (ctxCritical ? "#fca5a5" : "#fcd34d"), display: "flex", justifyContent: "space-between", alignItems: "center", flexShrink: 0 }}>
          <span style={{ fontSize: 10, color: ctxCritical ? "#dc2626" : "#d97706" }}>
            {ctxCritical ? "⚠ Context almost full" : "ℹ Context filling up"} — {ctxPct}% of {maxCtx.toLocaleString()} tokens
          </span>
          <button onClick={compress} disabled={compressing}
            style={{ padding: "2px 8px", border: "none", borderRadius: 3, background: ctxCritical ? "#dc2626" : "#d97706", color: "#fff", cursor: "pointer", fontSize: 10 }}>
            {compressing ? "…" : "Compress"}
          </button>
        </div>
      )}

      {/* Input area */}
      <div style={{ padding: "8px 10px", borderTop: "1px solid #e5e7eb", flexShrink: 0, display: "flex", flexDirection: "column", gap: 6 }}>
        {/* Attachment buttons */}
        <div style={{ display: "flex", gap: 4 }}>
          <button onClick={() => fileInputRef.current?.click()} title="Attach file" style={attachBtn}>📎 File</button>
          <button onClick={handleUrlPaste} title="Paste URL" style={attachBtn}>🔗 URL</button>
          {messages.length > 0 && (
            <button onClick={() => setMessages([])} title="Clear chat" style={{ ...attachBtn, marginLeft: "auto", color: "#dc2626" }}>🗑 Clear</button>
          )}
        </div>
        <input ref={fileInputRef} type="file" accept=".txt,.md,.csv,.json,.py" style={{ display: "none" }} onChange={handleFile} />

        <div style={{ display: "flex", gap: 6 }}>
          <textarea
            ref={textareaRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            placeholder="Ask anything… (Enter to send, Shift+Enter for newline)"
            rows={2}
            style={{ flex: 1, padding: "6px 9px", border: "1px solid #d1d5db", borderRadius: 6, fontSize: 12, resize: "none", fontFamily: "inherit", outline: "none" }}
            disabled={busy || compressing}
          />
          <button onClick={() => send()} disabled={busy || compressing || !input.trim()}
            style={{ padding: "0 14px", background: "#7c3aed", color: "#fff", border: "none", borderRadius: 6, cursor: busy ? "not-allowed" : "pointer", fontSize: 12, fontWeight: 600, opacity: input.trim() ? 1 : 0.5 }}>
            {busy ? "…" : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Inline docked chat (for BottomPanel) ─────────────────────────────────────────────

/**
 * ChatInline renders the AI chat inside the bottom panel (when docked).
 * Same logic as AIChatWindow but without the floating window chrome.
 */
export function ChatInline() {
  const { setDocked } = useAIChat();
  useToast(); // keep provider subscription for future

  const [messages, setMessages] = useState<MsgUI[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [contextType, setContextType] = useState<"" | "corpus" | "experiment" | "study">("");
  const [contextId, setContextId] = useState("");
  const [corpora, setCorpora] = useState<TextResponse[]>([]);
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [studies, setStudies] = useState<StudyResponse[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const maxCtx = getLocalCtxLength();
  const usedTokens = estimateTokens(messages);
  const ctxPct = Math.min(100, Math.round((usedTokens / maxCtx) * 100));

  useEffect(() => {
    listTexts().then(setCorpora).catch(() => {});
    listExperiments().then(setExperiments).catch(() => {});
    listStudies().then(setStudies).catch(() => {});
  }, []);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const send = useCallback(async (overrideText?: string) => {
    const text = (overrideText ?? input).trim();
    if (!text || busy) return;
    setInput("");
    const userMsg: MsgUI = { id: ++_msgId, role: "user", content: text, timestamp: Date.now() };
    const loadingMsg: MsgUI = { id: ++_msgId, role: "assistant", content: "", timestamp: Date.now(), loading: true };
    setMessages(prev => [...prev, userMsg, loadingMsg]);
    setBusy(true);
    try {
      const history = [...messages, userMsg].filter(m => !m.loading).map(({ role, content }) => ({ role, content }));
      const result = await aiChat({ messages: history, context_type: contextType || null, context_id: contextId || null });
      setMessages(prev => prev.map(m => m.id === loadingMsg.id ? { ...m, content: result.content as string, loading: false, timestamp: Date.now() } : m));
    } catch (e) {
      setMessages(prev => prev.map(m => m.id === loadingMsg.id ? { ...m, content: `Error: ${e instanceof Error ? e.message : "AI error"}`, loading: false, error: true, timestamp: Date.now() } : m));
    } finally { setBusy(false); }
  }, [input, busy, messages, contextType, contextId]);

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const content = ev.target?.result as string;
      setInput(prev => `${prev}\n\n[File: ${file.name}]\n\`\`\`\n${content.slice(0, 2000)}\n\`\`\``);
    };
    reader.readAsText(file); e.target.value = "";
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", background: "#0f172a" }}>
      {/* Mini header */}
      <div style={{ display: "flex", gap: 6, padding: "3px 8px", borderBottom: "1px solid #1e293b", alignItems: "center", flexShrink: 0 }}>
        <span style={{ color: "#94a3b8", fontSize: 10 }}>Context:</span>
        {(["", "corpus", "experiment", "study"] as const).map((ct) => (
          <button key={ct || "g"} onClick={() => { setContextType(ct); setContextId(""); }}
            style={{ padding: "1px 5px", border: "none", borderRadius: 3, cursor: "pointer", fontSize: 9, background: contextType === ct ? "#2563eb" : "#1e293b", color: contextType === ct ? "#fff" : "#64748b" }}>
            {ct || "Global"}
          </button>
        ))}
        {contextType === "corpus" && <select value={contextId} onChange={e => setContextId(e.target.value)} style={{ fontSize: 9, background: "#1e293b", color: "#e2e8f0", border: "none", borderRadius: 3 }}><option value="">corpus…</option>{corpora.map(c => <option key={c.id} value={c.id}>{c.name.slice(0, 18)}</option>)}</select>}
        {contextType === "experiment" && <select value={contextId} onChange={e => setContextId(e.target.value)} style={{ fontSize: 9, background: "#1e293b", color: "#e2e8f0", border: "none", borderRadius: 3 }}><option value="">exp…</option>{experiments.map(ex => <option key={ex.id} value={ex.id}>{ex.name.slice(0, 18)}</option>)}</select>}
        {contextType === "study" && <select value={contextId} onChange={e => setContextId(e.target.value)} style={{ fontSize: 9, background: "#1e293b", color: "#e2e8f0", border: "none", borderRadius: 3 }}><option value="">study…</option>{studies.map(s => <option key={s.id} value={s.id}>{s.name.slice(0, 18)}</option>)}</select>}
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 4 }}>
          <div style={{ width: 40, height: 3, background: "#1e293b", borderRadius: 2 }}>
            <div style={{ height: "100%", width: `${ctxPct}%`, background: ctxPct > 90 ? "#ef4444" : ctxPct > 75 ? "#f59e0b" : "#34d399", borderRadius: 2 }} />
          </div>
          <button onClick={() => setMessages([])} style={{ border: "none", background: "none", color: "#64748b", cursor: "pointer", fontSize: 10 }}>🗑</button>
          <button onClick={() => setDocked(false)} title="Undock" style={{ border: "none", background: "none", color: "#64748b", cursor: "pointer", fontSize: 10 }}>⊞</button>
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: "4px 8px", display: "flex", flexDirection: "column", gap: 5 }}>
        {messages.length === 0 && <div style={{ color: "#475569", fontSize: 10, fontStyle: "italic", padding: "8px 0" }}>Ask Glossa AI anything…</div>}
        {messages.map((msg) => (
          <div key={msg.id} style={{ display: "flex", gap: 4, alignItems: "flex-start", flexDirection: msg.role === "user" ? "row-reverse" : "row" }}>
            <div style={{ padding: "4px 8px", borderRadius: 5, fontSize: 11, lineHeight: 1.5, maxWidth: "82%",
              background: msg.role === "user" ? "#1e3a5f" : msg.error ? "#450a0a" : "#1e293b",
              color: msg.role === "user" ? "#e2e8f0" : msg.error ? "#fca5a5" : "#cbd5e1" }}>
              {msg.loading ? <span style={{ color: "#475569" }}>✨…</span>
                : msg.role === "user" ? <span style={{ whiteSpace: "pre-wrap" }}>{msg.content}</span>
                : <div dangerouslySetInnerHTML={{ __html: renderMd(msg.content) }} />}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{ display: "flex", gap: 4, padding: "4px 8px", borderTop: "1px solid #1e293b", flexShrink: 0 }}>
        <button onClick={() => fileInputRef.current?.click()} style={{ background: "#1e293b", border: "none", color: "#64748b", cursor: "pointer", fontSize: 11, padding: "0 4px", borderRadius: 3 }}>📎</button>
        <input ref={fileInputRef} type="file" accept=".txt,.md,.csv,.json,.py" style={{ display: "none" }} onChange={handleFile} />
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
          placeholder="Ask anything… (Enter)"
          style={{ flex: 1, background: "#1e293b", border: "none", color: "#e2e8f0", fontSize: 11, padding: "3px 6px", borderRadius: 3, outline: "none" }}
          disabled={busy}
        />
        <button onClick={() => send()} disabled={busy || !input.trim()}
          style={{ padding: "2px 8px", background: "#7c3aed", border: "none", borderRadius: 3, color: "#fff", cursor: "pointer", fontSize: 10 }}>
          {busy ? "…" : "Send"}
        </button>
      </div>
    </div>
  );
}

// ── Floating bubble ───────────────────────────────────────────────────────────

/**
 * AIChatBubble — fixed bottom-right, always above the bottom panel.
 *
 * No dragging — its position is determined entirely by panelHeight so it
 * stays anchored above the logs/jobs/terminal panel at all times.
 */
export function AIChatBubble({ panelHeight = 0 }: { panelHeight?: number }) {
  const { toggleChat, isOpen } = useAIChat();
  const SIZE = 48;

  return (
    <button
      onClick={toggleChat}
      title={isOpen ? "Close AI Chat" : "Open AI Chat ✨"}
      style={{
        position: "fixed",
        right: 24,
        bottom: panelHeight + 16,   // always above the bottom panel
        width: SIZE, height: SIZE,
        borderRadius: "50%",
        background: isOpen ? "#1e3a5f" : "linear-gradient(135deg,#7c3aed,#1e3a5f)",
        border: "2px solid rgba(255,255,255,0.15)",
        cursor: "pointer",
        boxShadow: "0 4px 20px rgba(124,58,237,0.45), 0 2px 8px rgba(0,0,0,0.2)",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 20,
        zIndex: 8400,
        transition: "bottom 0.2s",   // smooth slide when panel resizes
      }}
    >
      {isOpen ? "\u2715" : "\u2728"}
    </button>
  );
}

const selectSt: React.CSSProperties = { padding: "2px 5px", border: "1px solid #e5e7eb", borderRadius: 4, fontSize: 10, background: "#fff", maxWidth: 140 };
const attachBtn: React.CSSProperties = { padding: "2px 8px", border: "1px solid #e5e7eb", borderRadius: 4, background: "#f9fafb", cursor: "pointer", fontSize: 10, color: "#6b7280" };
