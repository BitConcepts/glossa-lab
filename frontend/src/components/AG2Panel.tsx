/**
 * AG2ResearchPanel — Multi-agent research conversation UI.
 *
 * Uses AG2 (AutoGen 2) with Ollama as backend LLM.
 * Shows: agent thinking steps, tool calls, tool results, and final messages.
 * Falls back gracefully if Ollama is offline (tool-only mode).
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  getAG2Status,
  streamAG2Chat,
  type AG2Status,
} from "../api";

interface Message {
  id: number;
  role: "user" | "assistant" | "tool_call" | "tool_result" | "system";
  content: string;
  agent?: string;
}

let _id = 0;
const nextId = () => ++_id;

const TYPE_STYLE: Record<string, React.CSSProperties> = {
  agent_start: { background: "#f0fdf4", border: "1px solid #86efac", color: "#15803d" },
  tool_call:   { background: "#eff6ff", border: "1px solid #93c5fd", color: "#1e40af", fontFamily: "monospace", fontSize: 11 },
  tool_result: { background: "#fafafa", border: "1px solid #e5e7eb", color: "#374151", fontFamily: "monospace", fontSize: 11 },
  message:     { background: "#fff",    border: "1px solid #e5e7eb", color: "#111827" },
  error:       { background: "#fef2f2", border: "1px solid #fca5a5", color: "#dc2626" },
  user:        { background: "#eff6ff", border: "1px solid #bfdbfe", color: "#1e40af" },
};

const TYPE_ICON: Record<string, string> = {
  agent_start: "🤖",
  tool_call:   "🔧",
  tool_result: "📋",
  message:     "💬",
  error:       "⚠️",
  user:        "👤",
};

export function AG2Panel({ contextType = "", contextId = "" }: {
  contextType?: string;
  contextId?: string;
}) {
  const [status, setStatus]   = useState<AG2Status | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput]     = useState("");
  const [busy, setBusy]       = useState(false);
  const [collapsed, setCollapsed] = useState<Set<number>>(new Set());
  const abortRef = useRef<AbortController | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Fetch status on mount
  useEffect(() => {
    getAG2Status().then(setStatus).catch(() =>
      setStatus({ available: false, model: null, mode: "tool_only", tools: [], error: "Backend unreachable" })
    );
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addMsg = useCallback((msg: Omit<Message, "id">) => {
    setMessages(prev => [...prev, { ...msg, id: nextId() }]);
  }, []);

  const send = useCallback(async () => {
    const text = input.trim();
    if (!text || busy) return;
    setInput("");
    setBusy(true);

    addMsg({ role: "user", content: text, agent: "You" });

    const ctrl = new AbortController();
    abortRef.current = ctrl;

    try {
      const history = messages.filter(m => m.role === "user" || m.role === "assistant")
        .map(m => ({ role: m.role as "user" | "assistant", content: m.content }));

      for await (const event of streamAG2Chat(text, history, contextType, contextId, ctrl.signal)) {
        if (event.type === "done") break;
        if (event.type === "error" && !event.content) continue;

        addMsg({
          role: event.type === "message" ? "assistant"
              : event.type === "tool_call" ? "tool_call"
              : event.type === "tool_result" ? "tool_result"
              : "system",
          content: event.content,
          agent: event.agent,
        });
      }
    } catch (e) {
      if (!(e instanceof Error && e.name === "AbortError")) {
        addMsg({ role: "system", content: `Error: ${e instanceof Error ? e.message : String(e)}`, agent: "system" });
      }
    } finally {
      setBusy(false);
      abortRef.current = null;
    }
  }, [input, busy, messages, contextType, contextId, addMsg]);

  const stop = () => { abortRef.current?.abort(); setBusy(false); };

  const toggleCollapse = (id: number) =>
    setCollapsed(prev => { const s = new Set(prev); s.has(id) ? s.delete(id) : s.add(id); return s; });

  const border = "#e5e7eb";
  const muted  = "#6b7280";

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", background: "#f8fafc" }}>

      {/* Header */}
      <div style={{ padding: "10px 16px", borderBottom: `1px solid ${border}`,
                    background: "#0f172a", display: "flex", alignItems: "center", gap: 10, flexShrink: 0 }}>
        <span style={{ fontSize: 18 }}>🤖</span>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 700, fontSize: 13, color: "#e2e8f0" }}>AG2 Research Agent</div>
          {status && (
            <div style={{ fontSize: 10, color: "#64748b" }}>
              {status.available
                ? (status.model ? `✓ ${status.model}` : "⚠ tool-only mode (Ollama offline)")
                : `✗ unavailable${status.error ? `: ${status.error}` : ""}`}
            </div>
          )}
        </div>
        {messages.length > 0 && (
          <button onClick={() => setMessages([])}
            style={{ border: "none", background: "rgba(255,255,255,0.1)", color: "#94a3b8",
                     cursor: "pointer", borderRadius: 4, padding: "2px 8px", fontSize: 11 }}>
            Clear
          </button>
        )}
      </div>

      {/* Status info if no messages */}
      {messages.length === 0 && status && (
        <div style={{ padding: 20, color: muted, fontSize: 12, lineHeight: 1.8 }}>
          <div style={{ fontWeight: 700, color: "#374151", marginBottom: 8 }}>AG2 Research Tools:</div>
          <ul style={{ margin: 0, paddingLeft: 20 }}>
            <li><code>list_experiments</code> — list all runnable graph experiments</li>
            <li><code>run_experiment</code> — execute any experiment and return results</li>
            <li><code>read_result</code> — read reports/ result files</li>
            <li><code>query_corpus</code> — get corpus stats (H1, tokens, signs)</li>
            <li><code>read_ledger</code> — read current LEDGER research state</li>
          </ul>
          <div style={{ marginTop: 12, padding: "8px 12px", background: "#f1f5f9", borderRadius: 6, fontSize: 11 }}>
            💡 Example prompts:<br/>
            "What experiments have we run on the CISI corpus?"<br/>
            "Run indus_cisi_dravidian_vs_sanskrit and interpret the results"<br/>
            "Summarise the current Indus decipherment status from the LEDGER"
          </div>
        </div>
      )}

      {/* Message list */}
      <div style={{ flex: 1, overflowY: "auto", padding: "10px 14px", display: "flex", flexDirection: "column", gap: 6 }}>
        {messages.map(msg => {
          const style = TYPE_STYLE[msg.role] ?? TYPE_STYLE.message;
          const icon  = TYPE_ICON[msg.role] ?? "•";
          const isCollapsible = msg.role === "tool_result" && msg.content.length > 200;
          const isCollapsed = collapsed.has(msg.id);

          return (
            <div key={msg.id} style={{ borderRadius: 6, padding: "7px 10px", ...style, position: "relative" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 5, marginBottom: 3 }}>
                <span style={{ fontSize: 12 }}>{icon}</span>
                <span style={{ fontSize: 10, fontWeight: 700, opacity: 0.7, textTransform: "uppercase", letterSpacing: 0.4 }}>
                  {msg.agent || msg.role}
                </span>
                {isCollapsible && (
                  <button onClick={() => toggleCollapse(msg.id)}
                    style={{ marginLeft: "auto", border: "none", background: "none", cursor: "pointer",
                             fontSize: 10, color: muted, padding: "0 2px" }}>
                    {isCollapsed ? "▶ expand" : "▼ collapse"}
                  </button>
                )}
              </div>
              <div style={{
                whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: 12, lineHeight: 1.6,
                maxHeight: isCollapsed ? "3em" : "none", overflow: isCollapsed ? "hidden" : "visible",
              }}>
                {msg.content.replace(/TERMINATE\s*$/, "").trim()}
              </div>
            </div>
          );
        })}
        {busy && (
          <div style={{ ...TYPE_STYLE.agent_start, borderRadius: 6, padding: "7px 10px", fontSize: 11 }}>
            🤖 GlossaResearch is thinking…
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{ padding: "10px 14px", borderTop: `1px solid ${border}`,
                    background: "#fff", display: "flex", gap: 8, flexShrink: 0 }}>
        <textarea
          ref={textareaRef}
          value={input}
          onChange={e => {
            setInput(e.target.value);
            e.target.style.height = "auto";
            e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
          }}
          onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
          placeholder="Ask the AG2 research agent… (Enter to send, Shift+Enter for newline)"
          rows={2}
          disabled={busy}
          style={{
            flex: 1, resize: "none", border: `1px solid ${border}`, borderRadius: 6,
            padding: "7px 10px", fontSize: 12, fontFamily: "inherit", lineHeight: 1.5,
            outline: "none", minHeight: 40, maxHeight: 120, overflowY: "hidden",
          }}
        />
        {busy ? (
          <button onClick={stop} style={{ padding: "0 14px", background: "#dc2626", color: "#fff",
                                          border: "none", borderRadius: 6, cursor: "pointer", fontSize: 12, flexShrink: 0 }}>
            Stop
          </button>
        ) : (
          <button onClick={send} disabled={!input.trim()}
            style={{ padding: "0 14px", background: input.trim() ? "#0f172a" : "#e5e7eb",
                     color: input.trim() ? "#fff" : "#9ca3af", border: "none",
                     borderRadius: 6, cursor: input.trim() ? "pointer" : "not-allowed",
                     fontSize: 12, flexShrink: 0, fontWeight: 600 }}>
            Send
          </button>
        )}
      </div>
    </div>
  );
}
