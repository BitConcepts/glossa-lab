/**
 * BottomPanel — VS Code-style IDE panel.
 * Tabs: Logs | Jobs | Terminal
 * - Drag-resizable from top edge
 * - Minimize collapses to tab bar only
 * - Maximize fills ~65% of viewport
 * - AI Chat tab appears when docked
 */
import { useCallback, useEffect, useRef, useState } from "react";
import { cancelJob, clearJobs, getLogStreamUrl, listJobs, runTerminalCommand, type JobResponse } from "../api";
import { ChatInline } from "./AIChatWindow";
import { useAIChat } from "../hooks/useAIChat";
import { useToast } from "../hooks/useToast";

type PanelTab = "logs" | "jobs" | "terminal" | "chat";

const MIN_HEIGHT = 100;
const MAX_HEIGHT_RATIO = 0.65;

// ── Markdown-like ANSI stripping for log lines ────────────────────────────────
function stripAnsi(s: string): string {
  // eslint-disable-next-line no-control-regex
  return s.replace(/\x1b\[[0-9;]*[mGKHF]/g, "");
}

function logLineColor(line: string): string {
  const l = line.toLowerCase();
  if (l.includes("error") || l.includes("exception") || l.includes("failed")) return "#f87171";
  if (l.includes("warn")) return "#fbbf24";
  if (l.includes("info") || l.includes("started") || l.includes("ready")) return "#86efac";
  if (l.includes("debug")) return "#94a3b8";
  return "#e2e8f0";
}

// ── Log Panel ─────────────────────────────────────────────────────────────────

function LogPanel() {
  const [lines, setLines] = useState<string[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [filter, setFilter] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const esRef = useRef<EventSource | null>(null);
  const autoScroll = useRef(true);

  useEffect(() => {
    const es = new EventSource(getLogStreamUrl());
    esRef.current = es;
    setStreaming(true);
    es.onmessage = (ev) => {
      try {
        const d = JSON.parse(ev.data) as { text: string };
        setLines((prev) => [...prev.slice(-499), stripAnsi(d.text)]);
      } catch { /* ignore */ }
    };
    es.onerror = () => { setStreaming(false); };
    return () => { es.close(); esRef.current = null; };
  }, []);

  useEffect(() => {
    if (autoScroll.current) bottomRef.current?.scrollIntoView({ behavior: "auto" });
  }, [lines]);

  const visible = filter ? lines.filter((l) => l.toLowerCase().includes(filter.toLowerCase())) : lines;

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ display: "flex", gap: 8, padding: "4px 8px", borderBottom: "1px solid #1e293b", alignItems: "center" }}>
        <input
          placeholder="Filter logs…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ flex: 1, padding: "2px 6px", background: "#1e293b", border: "1px solid #334155", borderRadius: 3, fontSize: 11, color: "#e2e8f0", outline: "none" }}
        />
        {streaming && <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#16a34a", animation: "pulse 1.5s infinite", flexShrink: 0 }} />}
        <button onClick={() => setLines([])} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#94a3b8", cursor: "pointer", fontSize: 10 }}>Clear</button>
      </div>
      <div
        style={{ flex: 1, overflowY: "auto", fontFamily: "monospace", fontSize: 11, padding: "4px 8px", lineHeight: 1.6 }}
        onScroll={(e) => {
          const el = e.currentTarget;
          autoScroll.current = el.scrollTop + el.clientHeight >= el.scrollHeight - 20;
        }}
      >
        {visible.length === 0 && <div style={{ color: "#64748b", fontStyle: "italic" }}>Waiting for log output…</div>}
        {visible.map((line, i) => (
          <div key={i} style={{ color: logLineColor(line), whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{line}</div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}

// ── Jobs Panel ────────────────────────────────────────────────────────────────

function JobsPanel() {
  const { toast } = useToast();
  const [jobs, setJobs] = useState<JobResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState<Set<string>>(new Set());

  const load = useCallback(async () => {
    try { setJobs(await listJobs()); setLoading(false); }
    catch { setLoading(false); }
  }, []);

  useEffect(() => {
    load();
    const t = setInterval(load, 3000);
    return () => clearInterval(t);
  }, [load]);

  const handleCancel = async (id: string) => {
    setCancelling((s) => new Set([...s, id]));
    try { await cancelJob(id); await load(); toast("Job aborted", "info"); }
    catch { toast("Cancel failed", "error"); }
    finally { setCancelling((s) => { const n = new Set(s); n.delete(id); return n; }); }
  };

  const handleClearAll = async () => {
    try { await clearJobs(); await load(); toast("Jobs cleared", "info"); }
    catch { toast("Clear failed", "error"); }
  };

  const statusColor: Record<string, string> = {
    pending: "#d97706", running: "#2563eb", completed: "#16a34a", failed: "#dc2626", cancelled: "#6b7280",
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", overflowY: "auto" }}>
      <div style={{ padding: "6px 10px", borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, color: "#94a3b8" }}>{jobs.length} jobs</span>
        <div style={{ display: "flex", gap: 4 }}>
          <button onClick={load} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#94a3b8", cursor: "pointer", fontSize: 10 }}>⟳</button>
          {jobs.length > 0 && (
            <button onClick={handleClearAll} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#ef4444", cursor: "pointer", fontSize: 10 }}>Delete All</button>
          )}
        </div>
      </div>
      {loading && <div style={{ padding: 10, color: "#64748b", fontSize: 12 }}>Loading…</div>}
      {!loading && jobs.length === 0 && (
        <div style={{ padding: "1rem", textAlign: "center", color: "#64748b", fontSize: 12 }}>
          <div style={{ fontSize: 22, marginBottom: 6 }}>📦</div>
          No jobs in queue. Submit a pipeline job to see it here.
        </div>
      )}
      {jobs.map((job) => {
        const isRunning = job.status === "running";
        const elapsed = isRunning ? Math.round((Date.now() - new Date(job.created_at).getTime()) / 1000) : null;
        return (
          <div key={job.id} style={{ padding: "8px 10px", borderBottom: "1px solid #1e293b" }}>
            <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 4 }}>
              <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 3, background: (statusColor[job.status] ?? "#6b7280") + "25", color: statusColor[job.status] ?? "#6b7280", fontWeight: 700 }}>
                {job.status}
              </span>
              <span style={{ flex: 1, fontWeight: 600, fontSize: 12, color: "#e2e8f0" }}>{job.name}</span>
              <span style={{ fontSize: 10, padding: "1px 5px", borderRadius: 3, background: "#1e293b", color: "#94a3b8" }}>CPU</span>
              {elapsed !== null && <span style={{ fontSize: 10, color: "#64748b" }}>{elapsed}s</span>}
              {(isRunning || job.status === "pending") && (
                <button
                  onClick={() => handleCancel(job.id)}
                  disabled={cancelling.has(job.id)}
                  style={{ padding: "2px 7px", border: "1px solid #ef4444", borderRadius: 3, background: "none", color: "#ef4444", cursor: "pointer", fontSize: 10 }}
                >
                  {cancelling.has(job.id) ? "…" : "Abort"}
                </button>
              )}
            </div>
            {isRunning && (
              <div style={{ height: 2, background: "#1e293b", borderRadius: 1, overflow: "hidden" }}>
                <div style={{ height: "100%", background: "#2563eb", borderRadius: 1, animation: "progress 1.5s linear infinite", width: "40%" }} />
              </div>
            )}
            <div style={{ fontSize: 10, color: "#64748b", marginTop: 2 }}>
              {job.pipeline} · {new Date(job.created_at).toLocaleTimeString()}
            </div>
          </div>
        );
      })}
      <style>{`@keyframes progress { 0%{transform:translateX(-100%)} 100%{transform:translateX(350%)} }`}</style>
    </div>
  );
}

// ── Terminal Panel ────────────────────────────────────────────────────────────

const BUILTINS = [
  "ls", "ll", "la", "dir", "cat", "type", "head", "tail",
  "pwd", "cd", "echo", "mkdir", "rm", "rmdir", "cp", "mv",
  "find", "grep", "wc", "env", "which", "clear", "help",
  "python", "python3",
];

function TerminalPanel() {
  const [history, setHistory] = useState<{ text: string; type: "input" | "output" | "error" | "info" }[]>([
    { text: "Glossa Lab Terminal — builtins: ls cat head tail grep find python… | Tab: autocomplete | help: list commands", type: "info" },
    { text: "─────────────────────────────────────────────────────────────────────────────", type: "info" },
  ]);
  const [input, setInput] = useState("");
  const [cmdHistory, setCmdHistory] = useState<string[]>([]);
  const [cmdIdx, setCmdIdx] = useState(-1);
  const [running, setRunning] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  // Track last command + output for Ask AI
  const [lastCmd, setLastCmd] = useState("");
  const lastOutputRef = useRef<string[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { openChat } = useAIChat();

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "auto" }); }, [history]);

  const run = useCallback(async () => {
    const cmd = input.trim();
    if (!cmd) return;
    setHistory((h) => [...h, { text: `$ ${cmd}`, type: "input" }]);
    setCmdHistory((h) => [cmd, ...h.slice(0, 49)]);
    setCmdIdx(-1);
    setInput("");
    setSuggestions([]);
    setLastCmd(cmd);
    lastOutputRef.current = [];
    setRunning(true);

    try {
      const resp = await runTerminalCommand(cmd);
      if (!resp.body) { setHistory((h) => [...h, { text: "No response body", type: "error" }]); setRunning(false); return; }
      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const parts = buf.split("\n\n");
        buf = parts.pop() ?? "";
        for (const part of parts) {
          for (const ln of part.split("\n")) {
            if (ln.startsWith("data: ")) {
              try {
                const d = JSON.parse(ln.slice(6)) as { text?: string; return_code?: number; message?: string };
                if (d.text !== undefined) {
                  const line = stripAnsi(d.text!);
                  setHistory((h) => [...h, { text: line, type: "output" }]);
                  lastOutputRef.current = [...lastOutputRef.current.slice(-29), line];
                }
                // Never show exit code — real terminals don't display them.
                // Only surface actual error messages from the shell.
                if (d.message)
                  setHistory((h) => [...h, { text: `Error: ${d.message}`, type: "error" }]);
              } catch { /* ignore */ }
            }
          }
        }
      }
    } catch (e) {
      setHistory((h) => [...h, { text: `Error: ${e instanceof Error ? e.message : String(e)}`, type: "error" }]);
    } finally {
      setRunning(false);
      inputRef.current?.focus();
    }
  }, [input]);

  const handleKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") { run(); return; }
    if (e.key === "Tab") {
      e.preventDefault();
      const prefix = input.trim();
      // Build unique candidate list: builtins + cmd history that start with prefix
      const all = [...BUILTINS, ...cmdHistory].filter(
        (c, i, arr) => c.startsWith(prefix) && arr.indexOf(c) === i
      );
      if (all.length === 0) return;
      if (all.length === 1) { setInput(all[0] + " "); setSuggestions([]); return; }
      setSuggestions(all);
      // Cycle: each Tab press advances through matches
      const cur = suggestions.indexOf(input);
      setInput(all[(cur + 1) % all.length]);
      return;
    }
    // Any other key clears suggestions
    if (e.key !== "ArrowUp" && e.key !== "ArrowDown") setSuggestions([]);
    if (e.key === "ArrowUp") {
      e.preventDefault();
      const idx = Math.min(cmdIdx + 1, cmdHistory.length - 1);
      setCmdIdx(idx);
      if (cmdHistory[idx]) setInput(cmdHistory[idx]);
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      const idx = Math.max(cmdIdx - 1, -1);
      setCmdIdx(idx);
      setInput(idx === -1 ? "" : (cmdHistory[idx] ?? ""));
    }
  };

  const lineColor: Record<string, string> = {
    input: "#86efac", output: "#e2e8f0", error: "#f87171", info: "#94a3b8",
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }} onClick={() => inputRef.current?.focus()}>
      {/* Toolbar */}
      <div style={{ display: "flex", gap: 4, padding: "2px 8px", borderBottom: "1px solid #0f172a", alignItems: "center", flexShrink: 0 }}>
        <button onClick={() => { setInput("help"); setTimeout(() => run(), 0); }}
          title="Show available commands"
          style={tBtn}>? help</button>
        <button onClick={() => { setHistory([]); setSuggestions([]); }}
          title="Clear terminal"
          style={tBtn}>✕ clear</button>
        {lastCmd && !running && (
          <button
            onClick={() => openChat({ initialPrompt: `I ran this terminal command:\n\`${lastCmd}\`\n\nOutput:\n\`\`\`\n${lastOutputRef.current.slice(0, 25).join("\n")}\n\`\`\`\n\nCan you help me understand or debug this?` })}
            title="Ask Glossa AI about this command and output"
            style={{ ...tBtn, color: "#c4b5fd" }}>✨ Ask AI</button>
        )}
      </div>

      {/* Output */}
      <div style={{ flex: 1, overflowY: "auto", fontFamily: "monospace", fontSize: 11, padding: "4px 8px", lineHeight: 1.6 }}>
        {history.map((item, i) => (
          <div key={i} style={{ color: lineColor[item.type], whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{item.text}</div>
        ))}
        {running && <div style={{ color: "#d97706" }}>▌ running…</div>}
        <div ref={bottomRef} />
      </div>

      {/* Suggestion bar */}
      {suggestions.length > 0 && (
        <div style={{ display: "flex", gap: 4, padding: "2px 8px", flexWrap: "wrap", borderTop: "1px solid #1e293b", background: "#0f172a" }}>
          {suggestions.map(s => (
            <button key={s} onClick={() => { setInput(s + " "); setSuggestions([]); inputRef.current?.focus(); }}
              style={{ padding: "0 5px", background: "#1e293b", border: "none", borderRadius: 3, color: s === input ? "#60a5fa" : "#94a3b8", cursor: "pointer", fontSize: 10, fontFamily: "monospace" }}>
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input row */}
      <div style={{ display: "flex", alignItems: "center", padding: "4px 8px", borderTop: "1px solid #1e293b", gap: 4 }}>
        <span style={{ color: "#86efac", fontSize: 11, fontFamily: "monospace" }}>$</span>
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => { setInput(e.target.value); if (suggestions.length) setSuggestions([]); }}
          onKeyDown={handleKey}
          disabled={running}
          placeholder="Enter command… (Tab: autocomplete)"
          style={{ flex: 1, background: "transparent", border: "none", outline: "none", color: "#e2e8f0", fontSize: 11, fontFamily: "monospace", caretColor: "#86efac" }}
          autoFocus
        />
        {running && <span style={{ color: "#d97706", fontSize: 10 }}>running…</span>}
      </div>
    </div>
  );
}

const tBtn: React.CSSProperties = { padding: "1px 6px", background: "none", border: "1px solid #1e293b", borderRadius: 3, color: "#64748b", cursor: "pointer", fontSize: 10, fontFamily: "monospace" };

// ── Main BottomPanel ──────────────────────────────────────────────────────────

interface BottomPanelProps {
  height: number;
  onHeightChange: (h: number) => void;
  minimized: boolean;
  onMinimizedChange: (v: boolean) => void;
  activeTab: PanelTab;
  onTabChange: (t: PanelTab) => void;
  leftOffset?: number;
}

export function BottomPanel({ height, onHeightChange, minimized, onMinimizedChange, activeTab, onTabChange, leftOffset = 0 }: BottomPanelProps) {
  const [maximized, setMaximized] = useState(false);
  const dragging = useRef(false);
  const dragStartY = useRef(0);
  const dragStartH = useRef(0);
  const { isOpen: chatOpen, isDocked } = useAIChat();

  const TABS: Array<{ id: PanelTab; label: string; icon: string }> = [
    { id: "logs", label: "Logs", icon: "📋" },
    { id: "jobs", label: "Jobs", icon: "📦" },
    { id: "terminal", label: "Terminal", icon: ">_" },
    ...(isDocked && chatOpen ? [{ id: "chat" as PanelTab, label: "AI Chat", icon: "✨" }] : []),
  ];

  // Drag-resize
  const onDragStart = useCallback((e: React.MouseEvent) => {
    dragging.current = true;
    dragStartY.current = e.clientY;
    dragStartH.current = height;
    e.preventDefault();
  }, [height]);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!dragging.current) return;
      const delta = dragStartY.current - e.clientY;
      const newH = Math.max(MIN_HEIGHT, Math.min(window.innerHeight * MAX_HEIGHT_RATIO, dragStartH.current + delta));
      onHeightChange(newH);
      if (minimized && delta > 20) onMinimizedChange(false);
    };
    const onUp = () => { dragging.current = false; };
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    return () => { window.removeEventListener("mousemove", onMove); window.removeEventListener("mouseup", onUp); };
  }, [height, minimized, onHeightChange, onMinimizedChange]);

  const panelH = maximized
    ? Math.floor(window.innerHeight * MAX_HEIGHT_RATIO)
    : minimized ? 30 : height;

  return (
    <div style={{
      position: "fixed", bottom: 0, left: leftOffset, right: 0,
      height: panelH, background: "#0f172a", borderTop: "1px solid #1e293b",
      display: "flex", flexDirection: "column", zIndex: 5000, userSelect: "none",
    }}>
      {/* Drag handle */}
      {!minimized && !maximized && (
        <div
          onMouseDown={onDragStart}
          style={{ height: 4, cursor: "ns-resize", background: "transparent", flexShrink: 0 }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.background = "#334155"; }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = "transparent"; }}
        />
      )}

      {/* Tab bar */}
      <div style={{ display: "flex", alignItems: "center", height: 26, flexShrink: 0, borderBottom: minimized ? "none" : "1px solid #1e293b", paddingLeft: 6 }}>
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => { onTabChange(tab.id); if (minimized) onMinimizedChange(false); }}
            style={{
              padding: "3px 10px", border: "none", borderBottom: activeTab === tab.id && !minimized ? "2px solid #3b82f6" : "2px solid transparent",
              background: "none", cursor: "pointer", fontSize: 11, fontWeight: activeTab === tab.id ? 600 : 400,
              color: activeTab === tab.id ? "#e2e8f0" : "#64748b",
              display: "flex", alignItems: "center", gap: 4,
            }}
          >
            <span style={{ fontSize: 10 }}>{tab.icon}</span>
            {tab.label}
          </button>
        ))}
        <div style={{ flex: 1 }} />
        {/* Panel controls */}
        <button onClick={() => { setMaximized(false); onMinimizedChange(!minimized); }}
          title={minimized ? "Restore" : "Minimize"}
          style={{ padding: "3px 8px", border: "none", background: "none", color: "#64748b", cursor: "pointer", fontSize: 13 }}>
          {minimized ? "▲" : "▼"}
        </button>
        <button onClick={() => { setMaximized(!maximized); if (minimized) onMinimizedChange(false); }}
          title={maximized ? "Restore" : "Maximize"}
          style={{ padding: "3px 8px", border: "none", background: "none", color: "#64748b", cursor: "pointer", fontSize: 11 }}>
          {maximized ? "⊟" : "⊞"}
        </button>
      </div>

      {/* Content */}
      {!minimized && (
        <div style={{ flex: 1, overflow: "hidden", userSelect: "text" }}>
          {activeTab === "logs" && <LogPanel />}
          {activeTab === "jobs" && <JobsPanel />}
          {activeTab === "terminal" && <TerminalPanel />}
          {activeTab === "chat" && <ChatInline />}
        </div>
      )}
      <style>{`@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }`}</style>
    </div>
  );
}
