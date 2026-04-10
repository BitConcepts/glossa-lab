/**
 * AIChatWindow — floating, draggable AI chat popup.
 *
 * Features:
 *  - Model picker (Ollama installed bold, uninstalled grayed, cloud providers grayed if no key)
 *  - Markdown rendering (headers, bold, italic, code, tables, lists, links)
 *  - Action cards: AI proposes actions → user approves / cancels
 *  - Compress/summarise: button in header + /compress slash command; warn at 75%
 *  - Export: /export md  or /export pdf (print window)
 *  - Slash commands: /compress  /clear  /help  /export md|pdf
 *  - Copy button per message (visible) + copy-all + export row
 *  - Context selector: global / corpus / experiment / study / research
 *  - File upload + URL fetch
 *  - Boundary-clamped dragging; resets to bottom-right on close
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  type AIAction,
  type AIChatResponse,
  type CatalogProvider,
  type OllamaInstalledModel,
  aiChat,
  executeAiAction,
  getLocalCtxLength,
  getProviderCatalog,
  getResearchContext,
  isLocalKeySet,
  listExperiments,
  listOllamaInstalled,
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

function renderTableBlock(block: string): string {
  const lines = block.split("\n").map(l => l.trim()).filter(l => l.startsWith("|"));
  if (lines.length < 3) return block;
  const parseRow = (line: string): string[] =>
    line.split("|").slice(1, -1).map(c => c.trim());
  const headers = parseRow(lines[0]);
  const rows = lines.slice(2).filter(l => l.trim()).map(parseRow);
  const thSt = "background:#1e3a5f;color:#e2e8f0;padding:5px 8px;text-align:left;font-size:11px;font-weight:600;white-space:nowrap;border:1px solid #334155";
  const tdSt = "padding:4px 8px;font-size:11px;border:1px solid #e5e7eb;vertical-align:top";
  const thead = `<thead><tr>${headers.map(h => `<th style='${thSt}'>${h}</th>`).join("")}</tr></thead>`;
  const tbody = `<tbody>${rows.map((cells, ri) => {
    const bg = ri % 2 === 0 ? "" : "background:#f8fafc;";
    return `<tr>${headers.map((_, ci) => `<td style='${tdSt};${bg}'>${cells[ci] ?? ""}</td>`).join("")}</tr>`;
  }).join("")}</tbody>`;
  return `<div style='overflow-x:auto;margin:8px 0;border-radius:5px;border:1px solid #e5e7eb'><table style='border-collapse:collapse;width:100%;font-size:11px'>${thead}${tbody}</table></div>`;
}

function renderMd(raw: string): string {
  let html = raw.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const tables: string[] = [];
  html = html.replace(/(\|[^\n]+\n\|[ \t|:^-]+\n(?:\|[^\n]+\n?)+)/g, match => {
    tables.push(renderTableBlock(match));
    return `%%TBL${tables.length - 1}%%`;
  });
  html = html
    .replace(/```[\w]*\n?([\s\S]*?)```/g, "<pre style='background:#1e293b;color:#e2e8f0;padding:8px 12px;border-radius:5px;font-size:11px;overflow-x:auto;margin:6px 0'>$1</pre>")
    .replace(/`([^`]+)`/g, "<code style='background:#f1f5f9;padding:1px 4px;border-radius:3px;font-size:12px;font-family:monospace'>$1</code>")
    .replace(/^### (.+)$/gm, "<div style='font-size:13px;font-weight:700;margin:10px 0 4px'>$1</div>")
    .replace(/^## (.+)$/gm,  "<div style='font-size:14px;font-weight:700;margin:12px 0 5px'>$1</div>")
    .replace(/^# (.+)$/gm,   "<div style='font-size:15px;font-weight:800;margin:14px 0 6px'>$1</div>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g,     "<em>$1</em>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "<a href='$2' target='_blank' rel='noopener noreferrer' style='color:#2563eb'>$1</a>")
    .replace(/^[-*] (.+)$/gm, "<li style='margin:2px 0;margin-left:16px'>$1</li>")
    .replace(/^\d+\. (.+)$/gm, "<li style='margin:2px 0;margin-left:16px;list-style-type:decimal'>$1</li>")
    .replace(/^---$/gm, "<hr style='border:none;border-top:1px solid #e5e7eb;margin:10px 0'>")
    .replace(/\n\n/g, "</p><p style='margin:5px 0'>")
    .replace(/\n/g, "<br>")
    .replace(/^/, "<p style='margin:0'>").replace(/$/, "</p>");
  tables.forEach((t, i) => { html = html.replace(`%%TBL${i}%%`, t); });
  return html;
}

// ── Silent copy button with brief checkmark feedback (no toast notification) ──
function CopyButton({ text, label = "Copy", style: extraStyle }: { text: string; label?: string; style?: React.CSSProperties }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1400);
    });
  };
  return (
    <button
      onClick={copy}
      title="Copy to clipboard"
      style={{
        border: "1px solid #e5e7eb", borderRadius: 3, cursor: "pointer",
        fontSize: 10, padding: "1px 6px",
        background: copied ? "#dcfce7" : "#f9fafb",
        color: copied ? "#16a34a" : "#6b7280",
        transition: "background 0.2s, color 0.2s",
        ...extraStyle,
      }}
    >
      {copied ? "✓" : label}
    </button>
  );
}

function fmtTime(ts: number): string {
  return new Date(ts).toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}
function estimateTokens(msgs: MsgUI[]): number {
  return Math.ceil(msgs.reduce((acc, m) => acc + m.content.length, 0) / 4);
}

// ── Types ─────────────────────────────────────────────────────────────────────

interface MsgUI extends ChatMessage {
  id: number;
  timestamp: number;
  loading?: boolean;
  error?: boolean;
  actions?: AIAction[];
  actionStates?: string[];  // "pending"|"executing"|"done"|"cancelled"|"failed"
}

interface ModelPref { provider: string; model: string; }
const MODEL_PREF_KEY = "glossa_model_pref";

// Action types that execute immediately without an approval card
const AUTO_EXEC = new Set(["open_view", "create_hypothesis", "create_notebook"]);

// LocalStorage key for persisted auto-approve preference
const AUTO_APPROVE_KEY = "glossa_auto_approve";

// Helper: resolve action label consistently (mirrors ActionCard fallback)
function resolveLabel(action: AIAction): string {
  return (
    action.label
    || (action.params as Record<string, string>)?.title
    || action.type.replace(/_/g, " ")
  );
}

let _msgId = 0;

// ── Model picker dropdown ─────────────────────────────────────────────────────

function ModelPickerDropdown({ installed, providers, current, onSelect, onReset, onClose }: {
  installed: OllamaInstalledModel[];
  providers: CatalogProvider[];
  current: ModelPref | null;
  onSelect: (p: ModelPref) => void;
  onReset: () => void;
  onClose: () => void;
}) {
  const isSel = (prov: string, mdl: string) =>
    current?.provider === prov && current?.model === mdl;

  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const h = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) onClose(); };
    setTimeout(() => document.addEventListener("mousedown", h), 0);
    return () => document.removeEventListener("mousedown", h);
  }, [onClose]);

  const row = (active: boolean, disabled = false): React.CSSProperties => ({
    display: "flex", alignItems: "center", width: "100%", padding: "5px 10px",
    border: "none", background: active ? "rgba(96,165,250,0.18)" : "none",
    color: disabled ? "#475569" : "#e2e8f0", cursor: disabled ? "not-allowed" : "pointer",
    fontSize: 11, textAlign: "left", gap: 6, opacity: disabled ? 0.55 : 1,
  });

  return (
    <div ref={ref} style={{
      position: "absolute", top: "calc(100% + 4px)", right: 0,
      background: "#1e293b", border: "1px solid #334155", borderRadius: 6,
      boxShadow: "0 8px 24px rgba(0,0,0,0.5)", zIndex: 9999,
      minWidth: 230, maxHeight: 310, overflowY: "auto",
    }}>
      <button onClick={() => { onReset(); onClose(); }} style={{ ...row(!current), borderBottom: "1px solid #2d3f55" }}>
        <span style={{ fontSize: 9, color: !current ? "#60a5fa" : "#475569" }}>◆</span>
        <span style={{ flex: 1 }}>Auto (Settings default)</span>
        {!current && <span style={{ color: "#60a5fa", fontSize: 9 }}>✓</span>}
      </button>

      <div style={{ padding: "5px 10px 2px", fontSize: 9, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.7 }}>
        Ollama · Local
      </div>
      {installed.length === 0
        ? <div style={{ padding: "3px 10px 8px", fontSize: 10, color: "#334155", fontStyle: "italic" }}>None installed</div>
        : installed.map(m => (
          <button key={m.name} onClick={() => onSelect({ provider: "ollama", model: m.name })} style={row(isSel("ollama", m.name))}>
            <span style={{ color: "#34d399", fontSize: 8 }}>●</span>
            <span style={{ flex: 1 }}>{m.name}</span>
            {isSel("ollama", m.name) && <span style={{ color: "#60a5fa", fontSize: 9 }}>✓</span>}
            <span style={{ color: "#64748b", fontSize: 9 }}>{m.size_gb.toFixed(1)} GB</span>
          </button>
        ))
      }

      {providers.filter(p => p.id !== "ollama").length > 0 && (
        <div style={{ padding: "7px 10px 2px", fontSize: 9, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.7, borderTop: "1px solid #2d3f55", marginTop: 4 }}>
          Cloud Providers
        </div>
      )}
      {providers.filter(p => p.id !== "ollama").map(p => {
        const ok = isLocalKeySet(p.api_key_setting);
        return p.recommended_models.slice(0, 3).map(m => (
          <button key={`${p.id}:${m}`} onClick={() => ok ? onSelect({ provider: p.id, model: m }) : undefined}
            style={row(isSel(p.id, m), !ok)} title={ok ? "" : `Set ${p.api_key_setting} in Settings`}>
            <span style={{ color: ok ? "#60a5fa" : "#2d3f55", fontSize: 8 }}>⚡</span>
            <span style={{ flex: 1 }}>{m}</span>
            {!ok && <span style={{ color: "#ef4444", fontSize: 9 }}>no key</span>}
            {isSel(p.id, m) && ok && <span style={{ color: "#60a5fa", fontSize: 9 }}>✓</span>}
          </button>
        ));
      })}
    </div>
  );
}

// ── Action approval card ──────────────────────────────────────────────────────

const ACTION_ICONS: Record<string, string> = {
  run_experiment:    "🧪",
  run_pipeline:      "⚙️",
  change_setting:    "⚙️",
  generate_report:   "📄",
  create_hypothesis: "💡",
  create_notebook:   "📓",
  open_view:         "→",
  clear_jobs:        "🗑️",
  execute_script:    "🔧",
  query_corpus:      "🔍",
  compare_results:   "📊",
  summarize_session: "💾",
  acquire_corpus:    "📥",
};

function ActionCard({ action, status, onApprove, onCancel, onAutoApproveAll }: {
  action: AIAction; status: string;
  onApprove: () => void;
  onCancel: () => void;
  onAutoApproveAll: () => void;
}) {
  const [ddOpen, setDdOpen] = useState(false);
  const ddRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ddOpen) return;
    const h = (e: MouseEvent) => {
      if (ddRef.current && !ddRef.current.contains(e.target as Node)) setDdOpen(false);
    };
    setTimeout(() => document.addEventListener("mousedown", h), 0);
    return () => document.removeEventListener("mousedown", h);
  }, [ddOpen]);

  // Guard: if action has no type, don't render anything (prevents 'undefined' errors)
  if (!action?.type) return null;
  const label = resolveLabel(action);
  const base: React.CSSProperties = { borderRadius: 6, padding: "8px 10px", margin: "5px 0", fontSize: 11, border: "1px solid" };
  if (status === "cancelled") return <div style={{ ...base, borderColor: "#374151", background: "#1a2332", color: "#6b7280" }}>✗ {label} — cancelled</div>;
  if (status === "done")      return <div style={{ ...base, borderColor: "#14532d", background: "#052e16", color: "#86efac" }}>✓ {label} — done</div>;
  if (status === "failed")    return <div style={{ ...base, borderColor: "#7f1d1d", background: "#1a0505", color: "#f87171" }}>⚠ {label} — failed</div>;
  return (
    <div style={{ ...base, borderColor: "#1d4ed8", background: "#eff6ff" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 5, marginBottom: 4 }}>
        <span>{ACTION_ICONS[action.type] || "⚡"}</span>
        <strong style={{ color: "#1e40af" }}>{label}</strong>
      </div>
      <div style={{ color: "#374151", marginBottom: 8, lineHeight: 1.5 }}>{action.description}</div>
      {status === "executing"
        ? <span style={{ color: "#6b7280", fontSize: 10 }}>⏳ Executing…</span>
        : <div style={{ display: "flex", gap: 0, alignItems: "center" }}>
            {/* Split Approve button */}
            <button
              onClick={onApprove}
              style={{ padding: "3px 11px", background: "#1d4ed8", color: "#fff", border: "none",
                borderRadius: "4px 0 0 4px", cursor: "pointer", fontSize: 11, fontWeight: 600 }}
            >✓ Approve</button>
            {/* Dropdown arrow */}
            <div style={{ position: "relative" }} ref={ddRef}>
              <button
                onClick={() => setDdOpen(o => !o)}
                title="More options"
                style={{ padding: "3px 6px", background: "#1a45c8", color: "#fff", border: "none",
                  borderLeft: "1px solid rgba(255,255,255,0.25)", borderRadius: "0 4px 4px 0",
                  cursor: "pointer", fontSize: 10, fontWeight: 700, lineHeight: 1.5 }}
              >▾</button>
              {ddOpen && (
                <div style={{ position: "absolute", top: "calc(100% + 2px)", left: 0,
                  background: "#fff", border: "1px solid #d1d5db", borderRadius: 5,
                  boxShadow: "0 4px 12px rgba(0,0,0,0.15)", zIndex: 9999, minWidth: 190 }}>
                  <button
                    onClick={() => { setDdOpen(false); onAutoApproveAll(); }}
                    style={{ display: "flex", alignItems: "center", gap: 7, width: "100%",
                      padding: "7px 12px", border: "none", background: "none",
                      cursor: "pointer", fontSize: 11, color: "#1d4ed8", textAlign: "left",
                      fontWeight: 600 }}
                  >
                    <span>⚡</span>
                    <div>
                      <div>Auto Approve All</div>
                      <div style={{ fontSize: 9, color: "#6b7280", fontWeight: 400 }}>Approve every action automatically this session</div>
                    </div>
                  </button>
                </div>
              )}
            </div>
            <button onClick={onCancel}
              style={{ marginLeft: 6, padding: "3px 10px", background: "none", color: "#6b7280",
                border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer", fontSize: 11 }}>✗ Cancel</button>
          </div>
      }
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export function AIChatWindow() {
  const { isOpen, request, closeChat, setDocked, isDocked } = useAIChat();
  const { toast } = useToast();

  const [messages, setMessages] = useState<MsgUI[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [compressing, setCompressing] = useState(false);
  const abortCtrl = useRef<AbortController | null>(null);

  // Auto-approve: persisted to localStorage so it survives page reload
  const [autoApprove, setAutoApproveState] = useState<boolean>(
    () => localStorage.getItem(AUTO_APPROVE_KEY) === "true"
  );
  const setAutoApprove = (v: boolean) => {
    setAutoApproveState(v);
    localStorage.setItem(AUTO_APPROVE_KEY, v ? "true" : "false");
  };

  // Listen for external changes to the auto-approve setting (e.g. from SettingsView)
  useEffect(() => {
    const handler = () => setAutoApproveState(localStorage.getItem(AUTO_APPROVE_KEY) === "true");
    window.addEventListener("glossa:auto_approve_changed", handler);
    return () => window.removeEventListener("glossa:auto_approve_changed", handler);
  }, []);

  // Model picker
  const [modelPref, setModelPref] = useState<ModelPref | null>(() => {
    try { return JSON.parse(localStorage.getItem(MODEL_PREF_KEY) ?? "null") as ModelPref | null; }
    catch { return null; }
  });
  const [modelPickerOpen, setModelPickerOpen] = useState(false);
  const [installedModels, setInstalledModels] = useState<OllamaInstalledModel[]>([]);
  const [providerCatalog, setProviderCatalog] = useState<CatalogProvider[]>([]);

  // Context
  const [contextType, setContextType] = useState<"" | "corpus" | "experiment" | "study" | "research">("");
  const [contextId, setContextId] = useState("");
  const [corpora, setCorpora] = useState<TextResponse[]>([]);
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [studies, setStudies] = useState<StudyResponse[]>([]);
  const [researchSummary, setResearchSummary] = useState<{ n_assigned_signs: number; token_coverage_pct: number; next_steps: string[] } | null>(null);

  // Window is fixed — no drag
  const size = { w: 460, h: 600 };
  const winRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // No clamp/drag needed — window is always fixed bottom-right

  const maxCtx = getLocalCtxLength();
  const usedTokens = estimateTokens(messages);
  const ctxPct = Math.min(100, Math.round((usedTokens / maxCtx) * 100));
  const ctxWarning = ctxPct >= 75;
  const ctxCritical = ctxPct >= 90;

  useEffect(() => {
    listTexts().then(setCorpora).catch(() => {});
    listExperiments().then(setExperiments).catch(() => {});
    listStudies().then(setStudies).catch(() => {});
    listOllamaInstalled().then(r => setInstalledModels(r.models)).catch(() => {});
    getProviderCatalog().then(setProviderCatalog).catch(() => {});
  }, []);

  useEffect(() => {
    if (!request) return;
    if (request.contextType !== undefined) setContextType(request.contextType ?? "");
    if (request.contextId) setContextId(request.contextId);
    if (request.initialPrompt) setInput(request.initialPrompt);
    setTimeout(() => textareaRef.current?.focus(), 100);
  }, [request]);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  // Drag removed — window is fixed at bottom-right above panel

  // Model pref helpers
  const saveModelPref = useCallback((p: ModelPref) => { setModelPref(p); localStorage.setItem(MODEL_PREF_KEY, JSON.stringify(p)); setModelPickerOpen(false); }, []);
  const resetModelPref = useCallback(() => { setModelPref(null); localStorage.removeItem(MODEL_PREF_KEY); }, []);
  const modelLabel = modelPref ? (modelPref.model.length > 18 ? modelPref.model.slice(0, 15) + "…" : modelPref.model) : "auto";

  // Compress
  const compress = useCallback(async () => {
    if (messages.length < 4) { toast("Not enough messages to compress", "info"); return; }
    setCompressing(true);
    try {
      const r = await aiChat({
        messages: [
          { role: "system", content: "Summarise the conversation below in 5–8 bullet points. Return plain text." },
          ...messages.filter(m => !m.loading).map(({ role, content }) => ({ role, content })),
        ],
        provider: modelPref?.provider ?? null, model: modelPref?.model ?? null,
      });
      setMessages([{ id: ++_msgId, role: "assistant", content: `[Compressed ${messages.length} messages]\n${r.content}`, timestamp: Date.now() }]);
      toast("Chat context compressed", "info");
    } catch { toast("Compression failed", "error"); }
    finally { setCompressing(false); }
  }, [messages, toast, modelPref]);

  useEffect(() => { if (ctxPct >= 90 && !compressing && !busy && messages.length > 4) compress(); }, [ctxPct, compressing, busy, messages.length, compress]);

  // Export
  const exportMd = useCallback(() => {
    const md = ["# Glossa AI Chat\n", `Exported: ${new Date().toLocaleString()}\n`,
      ...messages.filter(m => !m.loading).map(m =>
        `### ${m.role === "user" ? "You" : "Glossa AI"}  ·  ${fmtTime(m.timestamp)}\n\n${m.content}`)
    ].join("\n\n---\n\n");
    const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(new Blob([md], { type: "text/markdown" })), download: `glossa-chat-${Date.now()}.md` });
    a.click(); URL.revokeObjectURL(a.href);
    toast("Exported as Markdown", "success");
  }, [messages, toast]);

  const exportPdf = useCallback(() => {
    const body = messages.filter(m => !m.loading).map(m => {
      const who = m.role === "user" ? "You" : "Glossa AI";
      const c = m.role === "user" ? `<p>${m.content.replace(/\n/g, "<br>")}</p>` : renderMd(m.content);
      return `<div style="margin-bottom:14px"><strong>${who}</strong>&ensp;<span style="color:#9ca3af;font-size:11px">${fmtTime(m.timestamp)}</span>${c}</div>`;
    }).join("<hr style='border:none;border-top:1px solid #e5e7eb;margin:10px 0'>");
    const win = window.open("", "_blank", "width=860,height=940");
    if (!win) { toast("Allow popups to export PDF", "error"); return; }
    win.document.write(`<!DOCTYPE html><html><head><title>Glossa AI Chat</title><style>body{font-family:system-ui,sans-serif;max-width:720px;margin:40px auto;font-size:13px;line-height:1.65;color:#111}pre{background:#1e293b;color:#e2e8f0;padding:8px 12px;border-radius:5px;font-size:11px}code{background:#f1f5f9;padding:1px 4px;border-radius:3px;font-family:monospace}@media print{body{margin:0}}</style></head><body><h1 style="font-size:18px;margin-bottom:4px">Glossa AI Chat</h1><p style="color:#9ca3af;font-size:11px;margin-top:0">Exported ${new Date().toLocaleString()}</p><hr style="border:none;border-top:2px solid #e5e7eb;margin-bottom:20px">${body}<script>setTimeout(()=>window.print(),400)</script></body></html>`);
    win.document.close();
  }, [messages, toast]);

  // Action execution
  const updateActionState = useCallback((msgId: number, idx: number, state: string) => {
    setMessages(prev => prev.map(m => {
      if (m.id !== msgId) return m;
      const s = [...(m.actionStates ?? (m.actions ?? []).map(() => "pending"))];
      s[idx] = state;
      return { ...m, actionStates: s };
    }));
  }, []);

  const handleAction = useCallback(async (msg: MsgUI, idx: number, action: AIAction, approve: boolean) => {
    if (!approve) { updateActionState(msg.id, idx, "cancelled"); return; }
    updateActionState(msg.id, idx, "executing");
    const label = resolveLabel(action);
    try {
      // Ensure params is always an object, never undefined/null
      const params = action.params && typeof action.params === "object" ? action.params : {};
      const result = await executeAiAction({ type: action.type, params });
      updateActionState(msg.id, idx, "done");
      if (action.type === "open_view" && result.navigate)
        window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: result.navigate } }));
      setMessages(prev => [...prev, { id: ++_msgId, role: "assistant", content: `✓ **${label}** — ${result.summary ?? "done"}`, timestamp: Date.now() }]);
    } catch (e) {
      updateActionState(msg.id, idx, "failed");
      setMessages(prev => [...prev, { id: ++_msgId, role: "assistant", content: `✗ **${label}** failed: ${e instanceof Error ? e.message : String(e)}`, timestamp: Date.now(), error: true }]);
    }
  }, [updateActionState]);

  // Auto-execute: either the lite AUTO_EXEC set or (if autoApprove) all actions
  const autoExec = useCallback((msg: MsgUI, forceAll = false) => {
    (msg.actions ?? []).forEach((a, i) => {
      const shouldRun = forceAll || (AUTO_EXEC.has(a.type) && !a.requires_approval);
      if (shouldRun) handleAction(msg, i, a, true);
    });
  }, [handleAction]);

  // Send
  const send = useCallback(async (overrideText?: string) => {
    const text = (overrideText ?? input).trim();
    if (!text || busy) return;
    setInput("");
    // Collapse textarea back to 1 line
    if (textareaRef.current) textareaRef.current.style.height = "auto";

    // Slash commands
    if (text.startsWith("/")) {
      const parts = text.toLowerCase().split(/\s+/);
      if (parts[0] === "/compress" || parts[0] === "/summarize" || parts[0] === "/summarise") { await compress(); return; }
      if (parts[0] === "/clear") { setMessages([]); toast("Chat cleared", "info"); return; }
      if (parts[0] === "/export") { parts[1] === "pdf" ? exportPdf() : exportMd(); return; }
      if (parts[0] === "/help") {
        setMessages(p => [...p, { id: ++_msgId, role: "assistant", timestamp: Date.now(), content: "**Slash commands**\n- `/compress` — summarise & compress context\n- `/clear` — clear all messages\n- `/export md` — download as Markdown\n- `/export pdf` — open print/PDF dialog\n- `/help` — this message" }]);
        return;
      }
    }

    const userMsg: MsgUI = { id: ++_msgId, role: "user", content: text, timestamp: Date.now() };
    const loadingMsg: MsgUI = { id: ++_msgId, role: "assistant", content: "", timestamp: Date.now(), loading: true };
    setMessages(prev => [...prev, userMsg, loadingMsg]);
    setBusy(true);

    // Create a fresh AbortController for this request
    const ctrl = new AbortController();
    abortCtrl.current = ctrl;

    try {
      const history = [...messages, userMsg].filter(m => !m.loading).map(({ role, content }) => ({ role, content }));
      const result: AIChatResponse = await aiChat({
        messages: history,
        context_type: contextType || null,
        context_id: contextId || null,
        provider: modelPref?.provider ?? null,
        model: modelPref?.model ?? null,
      }, ctrl.signal);
      const shouldAutoAll = autoApprove || localStorage.getItem(AUTO_APPROVE_KEY) === "true";
      const newMsg: MsgUI = {
        id: loadingMsg.id, role: "assistant", content: result.content,
        actions: result.actions ?? [],
        actionStates: (result.actions ?? []).map(a =>
          (shouldAutoAll || (AUTO_EXEC.has(a.type) && !a.requires_approval)) ? "executing" : "pending"
        ),
        timestamp: Date.now(), loading: false,
      };
      setMessages(prev => prev.map(m => m.id === loadingMsg.id ? newMsg : m));
      if ((result.actions ?? []).length > 0)
        setTimeout(() => autoExec(newMsg, shouldAutoAll), 50);
    } catch (e) {
      const aborted = e instanceof Error && e.name === "AbortError";
      setMessages(prev => prev.map(m => m.id === loadingMsg.id
        ? { ...m,
            content: aborted ? "[Request stopped]" : `Error: ${e instanceof Error ? e.message : "AI error"}`,
            loading: false,
            error: !aborted,
            timestamp: Date.now() }
        : m));
    } finally { setBusy(false); abortCtrl.current = null; }
  }, [input, busy, messages, contextType, contextId, modelPref, compress, exportMd, exportPdf, autoExec, toast]);

  // File upload
  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      const c = ev.target?.result as string;
      setInput(p => `${p}\n\n[File: ${file.name}]\n\`\`\`\n${c.slice(0, 2000)}${c.length > 2000 ? "\n…(truncated)" : ""}\n\`\`\``);
    };
    reader.readAsText(file); e.target.value = "";
  };

  const handleUrlPaste = useCallback(async () => {
    const url = prompt("Enter a URL to fetch:");
    if (!url?.startsWith("http")) return;
    try {
      toast("Fetching URL…", "info");
      const t = await fetch(url).then(r => r.text());
      setInput(p => `${p}\n\n[URL: ${url}]\n${t.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").slice(0, 3000)}…`);
    } catch { toast("Could not fetch URL", "error"); }
  }, [toast]);

  const loadResearch = useCallback(async () => {
    setContextType("research"); setContextId(""); setResearchSummary(null);
    try { const d = await getResearchContext(); setResearchSummary(d.summary); toast("Research context loaded", "info"); }
    catch { toast("Could not load research context", "error"); }
  }, [toast]);

  if (!isOpen || isDocked) return null;

  // Fixed position — bottom-right corner, overlaps panel
  // maxHeight ensures window never goes off the top of the screen
  const winStyle: React.CSSProperties = {
    position: "fixed",
    right: 84,
    bottom: 82,
    width: size.w,
    maxHeight: "calc(100vh - 100px)",
    height: size.h,
    zIndex: 8500,
  };

  const ctxLabel = () => {
    if (contextType === "research") return "Research";
    if (!contextType || !contextId) return null;
    return { corpus: corpora.find(c => c.id === contextId)?.name, experiment: experiments.find(e => e.id === contextId)?.name, study: studies.find(s => s.id === contextId)?.name }[contextType];
  };

  return (
    <div ref={winRef} style={{ ...winStyle, background: "#fff", borderRadius: 10, boxShadow: "0 20px 60px rgba(0,0,0,0.22),0 0 0 1px rgba(0,0,0,0.08)", display: "flex", flexDirection: "column", overflow: "hidden" }}>

      {/* Header — no drag handle */}
      <div style={{ background: "#1e3a5f", padding: "8px 10px", display: "flex", alignItems: "center", gap: 6, userSelect: "none", flexShrink: 0 }}>
        <span style={{ fontSize: 14 }}>✨</span>
        <span style={{ fontWeight: 700, fontSize: 13, color: "#fff", flex: 1 }}>Glossa AI</span>
        {autoApprove && (
          <span
            title="Auto-approve is ON — all actions are executed automatically. Click to disable."
            onClick={() => { setAutoApprove(false); toast("Auto-approve disabled", "info"); }}
            style={{ fontSize: 9, padding: "1px 6px", borderRadius: 8, background: "#f59e0b",
              color: "#78350f", fontWeight: 700, cursor: "pointer", letterSpacing: 0.3 }}>⚡ AUTO</span>
        )}

        {/* Context bar + compress button */}
        <div style={{ display: "flex", alignItems: "center", gap: 3 }} title={`~${usedTokens.toLocaleString()} / ${maxCtx.toLocaleString()} tokens`}>
          <div style={{ width: 52, height: 4, background: "rgba(255,255,255,0.18)", borderRadius: 2, overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${ctxPct}%`, background: ctxCritical ? "#ef4444" : ctxWarning ? "#f59e0b" : "#34d399", borderRadius: 2, transition: "width 0.3s" }} />
          </div>
          <span style={{ fontSize: 9, color: "rgba(255,255,255,0.6)" }}>{ctxPct}%</span>
          <button onClick={compress} disabled={compressing} title="Compress context"
            style={{ border: "none", background: "none", color: ctxWarning ? "#fbbf24" : "rgba(255,255,255,0.4)", cursor: "pointer", fontSize: 11, padding: "0 1px", lineHeight: 1 }}>⊟</button>
        </div>
        {compressing && <span style={{ fontSize: 9, color: "#fcd34d" }}>compressing…</span>}

        {/* Model picker */}
        <div style={{ position: "relative" }}>
          <button onClick={() => setModelPickerOpen(o => !o)} title="Select model"
            style={{ border: "1px solid rgba(255,255,255,0.22)", borderRadius: 4, background: "rgba(255,255,255,0.1)", color: "#e2e8f0", fontSize: 10, padding: "2px 7px", cursor: "pointer", display: "flex", alignItems: "center", gap: 3 }}>
            {modelLabel}<span style={{ fontSize: 7, opacity: 0.7 }}>▾</span>
          </button>
          {modelPickerOpen && (
            <ModelPickerDropdown installed={installedModels} providers={providerCatalog} current={modelPref}
              onSelect={saveModelPref} onReset={resetModelPref} onClose={() => setModelPickerOpen(false)} />
          )}
        </div>

        <button onClick={() => setDocked(true)} title="Dock to panel" style={hdrBtn}>⊟</button>
        <button onClick={() => setMessages([])} title="Clear chat" style={hdrBtn}>🗑</button>
        <button onClick={closeChat} style={{ ...hdrBtn, fontSize: 16 }}>×</button>
      </div>

      {/* Context selector */}
      <div style={{ padding: "5px 10px", borderBottom: "1px solid #f3f4f6", background: "#fafafa", display: "flex", gap: 4, flexWrap: "wrap", alignItems: "center", flexShrink: 0 }}>
        <span style={{ fontSize: 10, color: "#9ca3af", flexShrink: 0 }}>Context:</span>
        {(["", "corpus", "experiment", "study"] as const).map(ct => (
          <button key={ct || "none"} onClick={() => { setContextType(ct); setContextId(""); setResearchSummary(null); }}
            style={{ padding: "2px 7px", borderRadius: 4, border: "1px solid", cursor: "pointer", fontSize: 10, background: contextType === ct ? "#1e3a5f" : "#fff", borderColor: contextType === ct ? "#1e3a5f" : "#e5e7eb", color: contextType === ct ? "#fff" : "#6b7280" }}>
            {ct || "Global"}
          </button>
        ))}
        <button onClick={loadResearch}
          style={{ padding: "2px 7px", borderRadius: 4, border: "1px solid", cursor: "pointer", fontSize: 10, background: contextType === "research" ? "#7c3aed" : "#fff", borderColor: contextType === "research" ? "#7c3aed" : "#e5e7eb", color: contextType === "research" ? "#fff" : "#6b7280" }}>
          🔬 Research
        </button>
        {contextType === "corpus"     && <select value={contextId} onChange={e => setContextId(e.target.value)} style={selSt}><option value="">— corpus —</option>{corpora.map(c => <option key={c.id} value={c.id}>{c.name.slice(0, 24)}</option>)}</select>}
        {contextType === "experiment" && <select value={contextId} onChange={e => setContextId(e.target.value)} style={selSt}><option value="">— experiment —</option>{experiments.map(e => <option key={e.id} value={e.id}>{e.name.slice(0, 24)}</option>)}</select>}
        {contextType === "study"      && <select value={contextId} onChange={e => setContextId(e.target.value)} style={selSt}><option value="">— study —</option>{studies.map(s => <option key={s.id} value={s.id}>{s.name.slice(0, 24)}</option>)}</select>}
        {ctxLabel() && contextType !== "research" && <span style={{ fontSize: 10, padding: "1px 6px", background: "#eff6ff", color: "#2563eb", borderRadius: 4, fontWeight: 600 }}>📎 {ctxLabel()?.slice(0, 20)}</span>}
        {contextType === "research" && researchSummary && (
          <span style={{ fontSize: 9, padding: "2px 6px", background: "#f3e8ff", color: "#7c3aed", borderRadius: 4, fontWeight: 600 }} title={researchSummary.next_steps[0] ?? ""}>
            🔬 {researchSummary.n_assigned_signs} signs · {researchSummary.token_coverage_pct}% coverage
          </span>
        )}
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: "10px 12px", display: "flex", flexDirection: "column", gap: 8 }}>
        {messages.length === 0 && (
          <div style={{ textAlign: "center", padding: "2rem 1rem", color: "#9ca3af" }}>
            <div style={{ fontSize: 28, marginBottom: 8 }}>{contextType === "research" ? "🔬" : "✨"}</div>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 6, color: "#374151" }}>{contextType === "research" ? "Research Mode" : "Glossa AI"}</div>
            {contextType === "research" && researchSummary
              ? <div style={{ fontSize: 11, lineHeight: 1.7, maxWidth: 370, margin: "0 auto", color: "#374151", textAlign: "left" }}>
                  <div>📊 <strong>{researchSummary.n_assigned_signs} signs assigned</strong> · {researchSummary.token_coverage_pct}% coverage</div>
                  {researchSummary.next_steps[0] && <div style={{ marginTop: 6, padding: "6px 8px", background: "#f3e8ff", borderRadius: 5, fontSize: 10 }}>Next: {researchSummary.next_steps[0].slice(0, 130)}</div>}
                </div>
              : <div style={{ fontSize: 12, lineHeight: 1.6, maxWidth: 310, margin: "0 auto" }}>
                  Ask about Indus Script, settings, experiments, or anything research-related.<br />
                  <span style={{ fontSize: 10, color: "#9ca3af" }}>Type <code style={{ background: "#f3f4f6", padding: "1px 3px", borderRadius: 3 }}>/help</code> for commands.</span>
                </div>
            }
            <div style={{ display: "flex", gap: 4, justifyContent: "center", flexWrap: "wrap", marginTop: 12 }}>
              {(contextType === "research" ? ["What should we work on next?", "Run the contact zone analysis", "Show current settings"] : ["What experiments should I run?", "Show me current settings", "Explain the Ventris method"]).map(s => (
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
            <div style={{ maxWidth: "80%", display: "flex", flexDirection: "column", gap: 2, minWidth: 0 }}>
              <div style={{ padding: "8px 11px", borderRadius: 8, fontSize: 12, lineHeight: 1.65, background: msg.role === "user" ? "#1e3a5f" : msg.error ? "#fef2f2" : "#f8f9fa", color: msg.role === "user" ? "#fff" : msg.error ? "#dc2626" : "#111827", border: msg.role === "user" ? "none" : `1px solid ${msg.error ? "#fca5a5" : "#e5e7eb"}` }}>
                {msg.loading
                  ? <span style={{ color: "#9ca3af" }}>✨ Thinking…</span>
                  : msg.role === "user"
                    ? <span style={{ whiteSpace: "pre-wrap" }}>{msg.content}</span>
                    : <div dangerouslySetInnerHTML={{ __html: renderMd(msg.content) }} />
                }
              </div>

              {/* Action cards */}
              {!msg.loading && (msg.actions ?? []).map((action, ai) => (
                <ActionCard key={ai} action={action}
                  status={(msg.actionStates ?? [])[ai] ?? "pending"}
                  onApprove={() => handleAction(msg, ai, action, true)}
                  onCancel={() => handleAction(msg, ai, action, false)}
                  onAutoApproveAll={() => {
                    setAutoApprove(true);
                    toast("Auto-approve ON — all future actions will run automatically", "success");
                    // Approve all currently-pending actions in this message too
                    (msg.actions ?? []).forEach((a, i) => {
                      if (((msg.actionStates ?? [])[i] ?? "pending") === "pending")
                        handleAction(msg, i, a, true);
                    });
                  }}
                />
              ))}

              {/* Per-message actions row */}
              <div style={{ display: "flex", gap: 5, alignItems: "center", paddingLeft: msg.role === "user" ? 0 : 4, justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
                <span style={{ fontSize: 9, color: "#9ca3af" }}>{fmtTime(msg.timestamp)}</span>
                {!msg.loading && (
                  <>
                    <CopyButton text={msg.content} />
                    <button onClick={() => setMessages(prev => prev.filter((_, i) => i !== idx))} title="Delete"
                      style={{ border: "none", background: "none", cursor: "pointer", fontSize: 10, color: "#d1d5db", padding: 0 }}>×</button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Bottom toolbar */}
        {messages.length > 0 && !busy && (
          <div style={{ display: "flex", gap: 5, justifyContent: "center", marginTop: 4, flexWrap: "wrap" }}>
            <button onClick={() => { const t = messages.filter(m => !m.loading).map(m => `[${m.role.toUpperCase()} ${fmtTime(m.timestamp)}]\n${m.content}`).join("\n\n"); navigator.clipboard.writeText(t); }} style={botBtn}>⏘ Copy all</button>
            <button onClick={exportMd}  style={botBtn}>📥 Export MD</button>
            <button onClick={exportPdf} style={botBtn}>📥 Export PDF</button>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Context warning */}
      {ctxWarning && (
        <div style={{ padding: "4px 10px", background: ctxCritical ? "#fef2f2" : "#fef3c7", borderTop: `1px solid ${ctxCritical ? "#fca5a5" : "#fcd34d"}`, display: "flex", justifyContent: "space-between", alignItems: "center", flexShrink: 0 }}>
          <span style={{ fontSize: 10, color: ctxCritical ? "#dc2626" : "#d97706" }}>
            {ctxCritical ? "⚠ Context almost full" : "ℹ Context filling up"} — {ctxPct}% of {maxCtx.toLocaleString()} tokens
          </span>
          <button onClick={compress} disabled={compressing} style={{ padding: "2px 8px", border: "none", borderRadius: 3, background: ctxCritical ? "#dc2626" : "#d97706", color: "#fff", cursor: "pointer", fontSize: 10 }}>
            {compressing ? "…" : "Compress"}
          </button>
        </div>
      )}

      {/* Input area */}
      <div style={{ padding: "7px 10px", borderTop: "1px solid #e5e7eb", flexShrink: 0, display: "flex", flexDirection: "column", gap: 5 }}>
        <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
          <button onClick={() => fileInputRef.current?.click()} style={attBtn}>📎 File</button>
          <button onClick={handleUrlPaste} style={attBtn}>🔗 URL</button>
          <span style={{ fontSize: 9, color: "#d1d5db", marginLeft: 2 }}>/help</span>
          {messages.length > 0 && <button onClick={() => setMessages([])} style={{ ...attBtn, marginLeft: "auto", color: "#dc2626" }}>🗑 Clear</button>}
        </div>
        <input ref={fileInputRef} type="file" accept=".txt,.md,.csv,.json,.py" style={{ display: "none" }} onChange={handleFile} />
        {/* Auto-grow textarea with embedded send/stop button */}
        <div style={{ position: "relative" }}>
          <textarea
            ref={textareaRef}
            value={input}
            onKeyDown={e => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            onChange={e => {
              setInput(e.target.value);
              // Auto-grow; show scrollbar when at max height
              const el = e.target;
              el.style.height = "auto";
              const newH = Math.min(el.scrollHeight, 180);
              el.style.height = newH + "px";
              el.style.overflowY = el.scrollHeight >= 180 ? "auto" : "hidden";
            }}
            placeholder="Message Glossa AI…"
            autoFocus
            style={{
              width: "100%", boxSizing: "border-box",
              minHeight: "38px", maxHeight: "180px", height: "38px",
              padding: "8px 44px 8px 10px",
              border: "1px solid #e5e7eb", borderRadius: 8,
              fontSize: 13, resize: "none", fontFamily: "inherit",
              outline: "none", lineHeight: 1.5, overflowY: "hidden",
              background: "#fafafa",
            }}
            disabled={busy || compressing}
            onFocus={e => { e.target.style.borderColor = "#a78bfa"; e.target.style.background = "#fff"; e.target.style.boxShadow = "0 0 0 2px rgba(124,58,237,0.08)"; }}
            onBlur={e => { e.target.style.borderColor = "#e5e7eb"; e.target.style.background = "#fafafa"; e.target.style.boxShadow = "none"; }}
          />
          {/* Embedded send / stop button */}
          {busy
            ? <button onClick={() => abortCtrl.current?.abort()}
                title="Stop generation (Escape)"
                style={{ position: "absolute", right: 6, bottom: 6,
                  padding: "3px 8px", background: "#dc2626", color: "#fff",
                  border: "none", borderRadius: 5, cursor: "pointer",
                  fontSize: 11, fontWeight: 700, lineHeight: 1.4 }}>
                ■ Stop
              </button>
            : <button onClick={() => send()} disabled={compressing || !input.trim()}
                title="Send (Enter)"
                style={{ position: "absolute", right: 6, bottom: 6,
                  padding: "3px 10px", background: input.trim() ? "#7c3aed" : "#e5e7eb",
                  color: input.trim() ? "#fff" : "#9ca3af",
                  border: "none", borderRadius: 5, cursor: input.trim() ? "pointer" : "not-allowed",
                  fontSize: 11, fontWeight: 600, lineHeight: 1.4 }}>
                Send
              </button>
          }
        </div>
      </div>
    </div>
  );
}

// ── ChatInline (docked in BottomPanel) ────────────────────────────────────────

export function ChatInline() {
  const { setDocked } = useAIChat();
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
  const ctxPct = Math.min(100, Math.round((estimateTokens(messages) / maxCtx) * 100));

  useEffect(() => {
    listTexts().then(setCorpora).catch(() => {});
    listExperiments().then(setExperiments).catch(() => {});
    listStudies().then(setStudies).catch(() => {});
  }, []);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const handleInlineAction = useCallback(async (msg: MsgUI, idx: number, action: AIAction, approve: boolean) => {
    const upd = (state: string) => setMessages(prev => prev.map(m => { if (m.id !== msg.id) return m; const s = [...(m.actionStates ?? [])]; s[idx] = state; return { ...m, actionStates: s }; }));
    if (!approve) { upd("cancelled"); return; }
    upd("executing");
    const label = resolveLabel(action);
    try {
      const r = await executeAiAction({ type: action.type, params: action.params });
      upd("done");
      if (action.type === "open_view" && r.navigate) window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: r.navigate } }));
      setMessages(p => [...p, { id: ++_msgId, role: "assistant", content: `✓ ${label} — ${r.summary ?? "done"}`, timestamp: Date.now() }]);
    } catch (e) {
      upd("failed");
      setMessages(p => [...p, { id: ++_msgId, role: "assistant", content: `✗ ${label} failed: ${e instanceof Error ? e.message : String(e)}`, timestamp: Date.now(), error: true }]);
    }
  }, []);

  const send = useCallback(async (text?: string) => {
    const t = (text ?? input).trim(); if (!t || busy) return;
    setInput("");
    const um: MsgUI = { id: ++_msgId, role: "user", content: t, timestamp: Date.now() };
    const lm: MsgUI = { id: ++_msgId, role: "assistant", content: "", timestamp: Date.now(), loading: true };
    setMessages(p => [...p, um, lm]); setBusy(true);
    try {
      const h = [...messages, um].filter(m => !m.loading).map(({ role, content }) => ({ role, content }));
      const r = await aiChat({ messages: h, context_type: contextType || null, context_id: contextId || null });
      const nm: MsgUI = { id: lm.id, role: "assistant", content: r.content, actions: r.actions ?? [], actionStates: (r.actions ?? []).map(() => "pending"), timestamp: Date.now(), loading: false };
      setMessages(p => p.map(m => m.id === lm.id ? nm : m));
    } catch (e) {
      setMessages(p => p.map(m => m.id === lm.id ? { ...m, content: `Error: ${e instanceof Error ? e.message : "AI error"}`, loading: false, error: true, timestamp: Date.now() } : m));
    } finally { setBusy(false); }
  }, [input, busy, messages, contextType, contextId]);

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    const r = new FileReader();
    r.onload = ev => setInput(p => `${p}\n\n[File: ${f.name}]\n\`\`\`\n${(ev.target?.result as string).slice(0, 2000)}\n\`\`\``);
    r.readAsText(f); e.target.value = "";
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", background: "#0f172a" }}>
      <div style={{ display: "flex", gap: 5, padding: "3px 8px", borderBottom: "1px solid #1e293b", alignItems: "center", flexShrink: 0 }}>
        <span style={{ color: "#94a3b8", fontSize: 10 }}>Context:</span>
        {(["", "corpus", "experiment", "study"] as const).map(ct => (
          <button key={ct || "g"} onClick={() => { setContextType(ct); setContextId(""); }}
            style={{ padding: "1px 5px", border: "none", borderRadius: 3, cursor: "pointer", fontSize: 9, background: contextType === ct ? "#2563eb" : "#1e293b", color: contextType === ct ? "#fff" : "#64748b" }}>
            {ct || "Global"}
          </button>
        ))}
        {contextType === "corpus"     && <select value={contextId} onChange={e => setContextId(e.target.value)} style={inSel}><option value="">corpus…</option>{corpora.map(c => <option key={c.id} value={c.id}>{c.name.slice(0,18)}</option>)}</select>}
        {contextType === "experiment" && <select value={contextId} onChange={e => setContextId(e.target.value)} style={inSel}><option value="">exp…</option>{experiments.map(x => <option key={x.id} value={x.id}>{x.name.slice(0,18)}</option>)}</select>}
        {contextType === "study"      && <select value={contextId} onChange={e => setContextId(e.target.value)} style={inSel}><option value="">study…</option>{studies.map(s => <option key={s.id} value={s.id}>{s.name.slice(0,18)}</option>)}</select>}
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 4 }}>
          <div style={{ width: 40, height: 3, background: "#1e293b", borderRadius: 2 }}>
            <div style={{ height: "100%", width: `${ctxPct}%`, background: ctxPct > 90 ? "#ef4444" : ctxPct > 75 ? "#f59e0b" : "#34d399", borderRadius: 2 }} />
          </div>
          <button onClick={() => setMessages([])} style={{ border: "none", background: "none", color: "#64748b", cursor: "pointer", fontSize: 10 }}>🗑</button>
          <button onClick={() => setDocked(false)} title="Undock" style={{ border: "none", background: "none", color: "#64748b", cursor: "pointer", fontSize: 10 }}>⊞</button>
        </div>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "4px 8px", display: "flex", flexDirection: "column", gap: 5 }}>
        {messages.length === 0 && <div style={{ color: "#475569", fontSize: 10, fontStyle: "italic", padding: "8px 0" }}>Ask Glossa AI anything…</div>}
        {messages.map((msg) => (
          <div key={msg.id}>
            <div style={{ display: "flex", gap: 4, alignItems: "flex-start", flexDirection: msg.role === "user" ? "row-reverse" : "row" }}>
              <div style={{ padding: "4px 8px", borderRadius: 5, fontSize: 11, lineHeight: 1.5, maxWidth: "85%", background: msg.role === "user" ? "#1e3a5f" : msg.error ? "#450a0a" : "#1e293b", color: msg.role === "user" ? "#e2e8f0" : msg.error ? "#fca5a5" : "#cbd5e1" }}>
                {msg.loading ? <span style={{ color: "#475569" }}>✨…</span>
                  : msg.role === "user" ? <span style={{ whiteSpace: "pre-wrap" }}>{msg.content}</span>
                  : <div dangerouslySetInnerHTML={{ __html: renderMd(msg.content) }} />}
              </div>
            </div>
            {!msg.loading && (msg.actions ?? []).map((action, ai) => (
              <ActionCard key={ai} action={action}
                status={(msg.actionStates ?? [])[ai] ?? "pending"}
                onApprove={() => handleInlineAction(msg, ai, action, true)}
                onCancel={() => handleInlineAction(msg, ai, action, false)}
                onAutoApproveAll={() => {
                  localStorage.setItem(AUTO_APPROVE_KEY, "true");
                  window.dispatchEvent(new CustomEvent("glossa:auto_approve_changed"));
                  (msg.actions ?? []).forEach((a, i) => {
                    if (((msg.actionStates ?? [])[i] ?? "pending") === "pending")
                      handleInlineAction(msg, i, a, true);
                  });
                }}
              />
            ))}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div style={{ display: "flex", gap: 4, padding: "4px 8px", borderTop: "1px solid #1e293b", flexShrink: 0 }}>
        <button onClick={() => fileInputRef.current?.click()} style={{ background: "#1e293b", border: "none", color: "#64748b", cursor: "pointer", fontSize: 11, padding: "0 4px", borderRadius: 3 }}>📎</button>
        <input ref={fileInputRef} type="file" accept=".txt,.md,.csv,.json,.py" style={{ display: "none" }} onChange={handleFile} />
        <input value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
          placeholder="Ask anything… (Enter)"
          style={{ flex: 1, background: "#1e293b", border: "none", color: "#e2e8f0", fontSize: 11, padding: "3px 6px", borderRadius: 3, outline: "none" }}
          disabled={busy} />
        <button onClick={() => send()} disabled={busy || !input.trim()}
          style={{ padding: "2px 8px", background: "#7c3aed", border: "none", borderRadius: 3, color: "#fff", cursor: "pointer", fontSize: 10 }}>
          {busy ? "…" : "Send"}
        </button>
      </div>
    </div>
  );
}

// ── Floating bubble ───────────────────────────────────────────────────────────

export function AIChatBubble() {
  const { toggleChat, isOpen } = useAIChat();
  return (
    <button onClick={toggleChat} title={isOpen ? "Close AI Chat" : "Open AI Chat"}
      style={{
        position: "fixed", right: 16, bottom: 16,
        width: 48, height: 48, borderRadius: "50%",
        background: isOpen
          ? "#dc2626"   // bright red when open — clearly a close button
          : "linear-gradient(135deg,#7c3aed,#1e3a5f)",
        border: isOpen ? "2px solid #fca5a5" : "2px solid rgba(255,255,255,0.15)",
        cursor: "pointer",
        boxShadow: isOpen
          ? "0 4px 16px rgba(220,38,38,0.4)"
          : "0 4px 20px rgba(124,58,237,0.45),0 2px 8px rgba(0,0,0,0.2)",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: isOpen ? 22 : 20, fontWeight: 700,
        color: "#fff", zIndex: 8400, transition: "bottom 0.2s, background 0.15s",
      }}>
      {isOpen ? "×" : "✨"}
    </button>
  );
}

// ── Style constants ───────────────────────────────────────────────────────────

const selSt:  React.CSSProperties = { padding: "2px 5px", border: "1px solid #e5e7eb", borderRadius: 4, fontSize: 10, background: "#fff", maxWidth: 140 };
const inSel:  React.CSSProperties = { fontSize: 9, background: "#1e293b", color: "#e2e8f0", border: "none", borderRadius: 3 };
const attBtn: React.CSSProperties = { padding: "2px 8px", border: "1px solid #e5e7eb", borderRadius: 4, background: "#f9fafb", cursor: "pointer", fontSize: 10, color: "#6b7280" };
const botBtn: React.CSSProperties = { fontSize: 10, color: "#9ca3af", background: "none", border: "1px solid #e5e7eb", borderRadius: 4, cursor: "pointer", padding: "2px 8px" };
const hdrBtn: React.CSSProperties = { border: "none", background: "none", color: "rgba(255,255,255,0.65)", cursor: "pointer", fontSize: 13, padding: "0 3px" };
