/**
 * AIChatView — conversational AI assistant (Glossa).
 * Optional context injection: corpus, experiment, or study.
 */
import { useEffect, useRef, useState } from "react";
import {
  aiChat, listExperiments, listStudies, listTexts,
  type ChatMessage, type ExperimentMeta, type StudyResponse, type TextResponse,
} from "../api";
import { useToast } from "../hooks/useToast";

interface MsgUI extends ChatMessage {
  id: number;
  loading?: boolean;
}

let _id = 0;

export function AIChatView() {
  const { toast } = useToast();
  const [messages, setMessages] = useState<MsgUI[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [contextType, setContextType] = useState<"" | "corpus" | "experiment" | "study">("");
  const [contextId, setContextId] = useState("");
  const [corpora, setCorpora] = useState<TextResponse[]>([]);
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [studies, setStudies] = useState<StudyResponse[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    listTexts().then(setCorpora).catch(() => {});
    listExperiments().then(setExperiments).catch(() => {});
    listStudies().then(setStudies).catch(() => {});
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    const text = input.trim();
    if (!text || busy) return;
    setInput("");

    const userMsg: MsgUI = { id: ++_id, role: "user", content: text };
    const loadingMsg: MsgUI = { id: ++_id, role: "assistant", content: "", loading: true };
    setMessages((prev) => [...prev, userMsg, loadingMsg]);
    setBusy(true);

    try {
      const history = [...messages, userMsg].map(({ role, content }) => ({ role, content }));
      const result = await aiChat({
        messages: history,
        context_type: contextType || null,
        context_id: contextId || null,
      });
      setMessages((prev) => prev.map((m) => m.id === loadingMsg.id ? { ...m, content: result.content as string, loading: false } : m));
    } catch (e) {
      const err = e instanceof Error ? e.message : "AI error";
      toast(err, "error");
      setMessages((prev) => prev.filter((m) => m.id !== loadingMsg.id));
    } finally {
      setBusy(false);
    }
  };

  const contextLabel = () => {
    if (!contextType || !contextId) return null;
    if (contextType === "corpus") return corpora.find(c => c.id === contextId)?.name;
    if (contextType === "experiment") return experiments.find(e => e.id === contextId)?.name;
    if (contextType === "study") return studies.find(s => s.id === contextId)?.name;
    return null;
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: 620 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>✨ Glossa AI Chat</h2>
        <button onClick={() => setMessages([])} style={{ padding: "4px 10px", background: "#f3f4f6", border: "1px solid #e5e7eb", borderRadius: 4, fontSize: 12, cursor: "pointer", color: "#6b7280" }}>
          Clear
        </button>
      </div>

      {/* Context selector */}
      <div style={{ display: "flex", gap: 8, marginBottom: "0.75rem", alignItems: "center", flexWrap: "wrap" }}>
        <span style={{ fontSize: 12, color: "#6b7280", whiteSpace: "nowrap" }}>Context:</span>
        {(["", "corpus", "experiment", "study"] as const).map((ct) => (
          <button key={ct || "none"} onClick={() => { setContextType(ct); setContextId(""); }}
            style={{ padding: "3px 10px", borderRadius: 6, border: "1px solid", cursor: "pointer", fontSize: 11,
              background: contextType === ct ? "#1e3a5f" : "#fff", borderColor: contextType === ct ? "#1e3a5f" : "#d1d5db",
              color: contextType === ct ? "#fff" : "#374151" }}>
            {ct || "None"}
          </button>
        ))}
        {contextType === "corpus" && (
          <select value={contextId} onChange={(e) => setContextId(e.target.value)} style={selectStyle}>
            <option value="">— select corpus —</option>
            {corpora.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        )}
        {contextType === "experiment" && (
          <select value={contextId} onChange={(e) => setContextId(e.target.value)} style={selectStyle}>
            <option value="">— select experiment —</option>
            {experiments.map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
          </select>
        )}
        {contextType === "study" && (
          <select value={contextId} onChange={(e) => setContextId(e.target.value)} style={selectStyle}>
            <option value="">— select study —</option>
            {studies.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        )}
        {contextLabel() && (
          <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 8, background: "#eff6ff", color: "#2563eb", fontWeight: 600 }}>
            📎 {contextLabel()}
          </span>
        )}
      </div>

      {/* Chat messages */}
      <div style={{ flex: 1, overflowY: "auto", border: "1px solid #e5e7eb", borderRadius: 8, padding: "14px 16px", background: "#fafafa", display: "flex", flexDirection: "column", gap: 12 }}>
        {messages.length === 0 && (
          <div style={{ textAlign: "center", padding: "2rem 1rem", color: "#9ca3af" }}>
            <div style={{ fontSize: 32, marginBottom: 10 }}>💬</div>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 6 }}>Glossa AI</div>
            <div style={{ fontSize: 13, lineHeight: 1.6, maxWidth: 400, margin: "0 auto" }}>
              Ask me anything about the Indus Script, entropy analysis, n-gram statistics,
              decipherment theories, or your specific research data.
            </div>
            <div style={{ marginTop: 16, display: "flex", gap: 6, justifyContent: "center", flexWrap: "wrap" }}>
              {[
                "What is the H2/H1 ratio for natural language?",
                "Explain the Zipf law in the context of the Indus Script",
                "Compare entropy of the Indus corpus with Sumerian",
                "What experiments should I run to test linguistic hypothesis?",
              ].map((s) => (
                <button key={s} onClick={() => setInput(s)}
                  style={{ padding: "4px 10px", border: "1px solid #e5e7eb", borderRadius: 6, background: "#fff", fontSize: 11, cursor: "pointer", color: "#374151" }}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} style={{ display: "flex", flexDirection: msg.role === "user" ? "row-reverse" : "row", gap: 10, alignItems: "flex-start" }}>
            <div style={{
              width: 28, height: 28, borderRadius: "50%", flexShrink: 0,
              background: msg.role === "user" ? "#1e3a5f" : "#7c3aed",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 12, color: "#fff", fontWeight: 700,
            }}>
              {msg.role === "user" ? "U" : "G"}
            </div>
            <div style={{
              maxWidth: "75%", padding: "10px 14px", borderRadius: 10,
              background: msg.role === "user" ? "#1e3a5f" : "#fff",
              color: msg.role === "user" ? "#fff" : "#111827",
              border: msg.role === "user" ? "none" : "1px solid #e5e7eb",
              fontSize: 13, lineHeight: 1.65,
              boxShadow: "0 1px 3px rgba(0,0,0,0.06)",
            }}>
              {msg.loading ? (
                <span style={{ color: "#9ca3af" }}>✨ Thinking…</span>
              ) : (
                <pre style={{ margin: 0, fontFamily: "inherit", whiteSpace: "pre-wrap", wordBreak: "break-word" }}>{msg.content}</pre>
              )}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
          placeholder="Ask Glossa anything… (Enter to send, Shift+Enter for newline)"
          rows={2}
          style={{ flex: 1, padding: "8px 12px", border: "1px solid #d1d5db", borderRadius: 6, fontSize: 13, resize: "none", fontFamily: "inherit" }}
          disabled={busy}
        />
        <button onClick={send} disabled={busy || !input.trim()} style={{
          padding: "0 20px", background: "#7c3aed", color: "#fff", border: "none", borderRadius: 6,
          fontSize: 13, fontWeight: 600, cursor: busy ? "not-allowed" : "pointer",
        }}>
          {busy ? "…" : "Send"}
        </button>
      </div>
    </div>
  );
}

const selectStyle: React.CSSProperties = { padding: "4px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 12, background: "#fff" };
