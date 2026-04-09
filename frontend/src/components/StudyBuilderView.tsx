/**
 * Study Builder — World-class visual workflow editor.
 *
 * Node types: experiment, pipeline, corpus, rag_query, ai_analysis,
 *             note, report, hypothesis
 *
 * Features:
 *  - Full-screen canvas with snap-to-grid (15px) and animated edges
 *  - Custom GlossaNode with left-target + right-source handles, delete button, status
 *  - Right-click context menus: canvas (add node), node (dup/rename/delete), edge (delete/reverse)
 *  - Edge reconnection by dragging endpoints; edge deletion via right-click or Delete key
 *  - Resizable + collapsible + dock-switchable left panel (studies + palette)
 *  - Collapsible right Inspector with typed param forms from params_schema
 *  - Import study from .glossa-study.json / export current study
 *  - Duplicate study one-click; New Study dialog with name + description
 *  - Per-node run-status overlay (running / complete / error / etc.)
 *  - RAG index status + rebuild button in toolbar
 */

import React, {
  useCallback, useEffect, useMemo, useRef, useState,
} from "react";
import {
  ReactFlow,
  addEdge,
  reconnectEdge,
  Background,
  BackgroundVariant,
  Controls,
  Handle,
  MiniMap,
  Position,
  type Connection,
  type Edge,
  type Node,
  type NodeChange,
  type EdgeChange,
  type NodeProps,
  applyNodeChanges,
  applyEdgeChanges,
  useReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { autoArrange } from "../utils/autoArrange";

import {
  createStudy,
  deleteStudy,
  getRagStatus,
  rebuildRagIndex,
  listExperiments,
  listStudies,
  getPipelineCatalog,
  runStudyStream,
  summarizeStudy,
  updateStudy,
  type AISummaryResult,
  type ExperimentMeta,
  type CatalogPipeline,
  type StudyNodeType,
  type StudyResponse,
  type StudyGraph,
  type StudyRunResult,
  type NodeRunStatus,
} from "../api";
import { useAIChat } from "../hooks/useAIChat";
import { CorpusSelector } from "./CorpusSelector";

// ── Theme helpers ────────────────────────────────────────────────────────

function sbTheme(dark: boolean) {
  return {
    // Side panels + toolbar
    panelBg:    dark ? "#0f172a" : "#f8fafc",
    panelBg2:   dark ? "#1e293b" : "#ffffff",
    text:       dark ? "#e2e8f0" : "#1e293b",
    textMuted:  dark ? "#94a3b8" : "#64748b",
    textFaint:  dark ? "#64748b" : "#94a3b8",
    border:     dark ? "#1e293b" : "#e2e8f0",
    borderHov:  dark ? "#334155" : "#cbd5e1",
    activeBg:   dark ? "#1e3a5f" : "#dbeafe",
    activeText: dark ? "#ffffff" : "#1e40af",
    inputBg:    dark ? "#0f172a" : "#ffffff",
    inputText:  dark ? "#e2e8f0" : "#1e293b",
    inputBdr:   dark ? "#334155" : "#d1d5db",
    btnBg:      dark ? "#1e293b" : "#f3f4f6",
    btnText:    dark ? "#94a3b8" : "#374151",
    // Canvas — light mode uses a light slate; dark stays deep navy
    canvasBg:   dark ? "#0a0f1e" : "#f1f5f9",
    canvasGrid: dark ? "#1a2235" : "#e2e8f0",
    edgeDef:    dark ? "#334155" : "#94a3b8",
    edgeRun:    "#7c3aed",
    // Nodes adapt to theme
    nodeBg:     dark ? "#111827" : "#ffffff",
    nodeText:   dark ? "#cbd5e1" : "#1e293b",
    nodeRef:    dark ? "#94a3b8" : "#64748b",
    nodeDesc:   dark ? "#64748b" : "#94a3b8",
    nodeHndBrd: dark ? "#111827" : "#ffffff",
  };
}

// ── Node type configuration

interface NodeTypeCfg {
  color: string;
  icon: string;
  defaultLabel: string;
  executable: boolean;
  description: string;
}

const NODE_CFG: Record<StudyNodeType, NodeTypeCfg> = {
  experiment:  { color: "#7c3aed", icon: "🧪", defaultLabel: "Experiment",   executable: true,  description: "Runs in-process via ExperimentBase.run()" },
  pipeline:    { color: "#2563eb", icon: "⚙️", defaultLabel: "Pipeline",     executable: true,  description: "Submits a background Job + polls for result" },
  corpus:      { color: "#059669", icon: "📚", defaultLabel: "Corpus",        executable: false, description: "Data source — corpus_id forwarded to downstream" },
  rag_query:   { color: "#6d28d9", icon: "🔍", defaultLabel: "RAG Query",     executable: true,  description: "Retrieves chunks from the knowledge base" },
  ai_analysis: { color: "#4f46e5", icon: "✨", defaultLabel: "AI Analysis",   executable: true,  description: "Sends upstream context to Glossa AI" },
  compare:     { color: "#ea580c", icon: "↔️", defaultLabel: "Compare",       executable: true,  description: "AI-powered comparison of two upstream results with structured insights" },
  note:        { color: "#d97706", icon: "📝", defaultLabel: "Note",          executable: false, description: "Annotation — no execution" },
  report:      { color: "#0d9488", icon: "📄", defaultLabel: "Report",        executable: true,  description: "Compile upstream results and save to a report file" },
  hypothesis:  { color: "#e11d48", icon: "💡", defaultLabel: "Hypothesis",    executable: false, description: "Links to a Hypothesis record" },
};

// ── NodeData ────────────────────────────────────────────────────────────────

interface NodeData extends Record<string, unknown> {
  label: string;
  nodeType: StudyNodeType;
  refId: string;
  description?: string;
  params?: Record<string, unknown>;
  noteText?: string;
  color?: string;
  runStatus?: "idle" | "running" | "complete" | "error" | "skipped" | "annotation" | "corpus" | "pending";
}

// ── GlossaNode ──────────────────────────────────────────────────────────────

const RUN_CLR: Record<string, string> = {
  complete: "#22c55e", error: "#ef4444", skipped: "#f59e0b",
  pending: "#f59e0b", annotation: "#64748b", corpus: "#059669", running: "#60a5fa",
};

const GlossaNode = ({ data, id, selected }: NodeProps) => {
  const nd = data as NodeData;
  const { setNodes, setEdges } = useReactFlow();
  const cfg = NODE_CFG[nd.nodeType] ?? NODE_CFG.experiment;
  const hdr = nd.color ?? cfg.color;
  const runStatus = nd.runStatus;
  const filledParams = Object.entries(nd.params ?? {}).filter(([, v]) => v !== "" && v !== undefined).length;
  // Theme-aware node colors: passed via data.darkMode (set when loading/creating nodes)
  const isDark = (nd as Record<string, unknown>).darkMode !== false;
  const nodeBg    = isDark ? "#111827" : "#ffffff";
  const nodeText  = isDark ? "#cbd5e1" : "#1e293b";
  const nodeRef   = isDark ? "#94a3b8" : "#64748b";
  const nodeDesc  = isDark ? "#64748b" : "#94a3b8";
  const hndBrd    = isDark ? "#111827" : "#ffffff";
  const shadow    = isDark
    ? (selected ? `0 0 0 2px #60a5fa40, 0 4px 20px rgba(0,0,0,0.6)` : "0 2px 12px rgba(0,0,0,0.5)")
    : (selected ? `0 0 0 2px #60a5fa60, 0 4px 12px rgba(0,0,0,0.15)` : "0 1px 6px rgba(0,0,0,0.12)");
  const isRunningNode = runStatus === "running";
  const nodeBorderColor = isRunningNode ? "#60a5fa" : selected ? "#60a5fa" : hdr + "66";
  const nodeBorderWidth = isRunningNode ? 3 : 2;
  const nodeBoxShadow   = isRunningNode
    ? "0 0 0 3px rgba(96,165,250,0.35), 0 4px 24px rgba(96,165,250,0.3)"
    : shadow;

  const onDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    setNodes(n => n.filter(node => node.id !== id));
    setEdges(e => e.filter(edge => edge.source !== id && edge.target !== id));
  };

  return (
    <div
      className={isRunningNode ? "glossa-node-running" : undefined}
      style={{
        background: nodeBg,
        border: `${nodeBorderWidth}px solid ${nodeBorderColor}`,
        borderRadius: 8, minWidth: 155, maxWidth: 230,
        boxShadow: nodeBoxShadow,
        fontFamily: "system-ui, sans-serif",
      }}>
      <Handle type="target" position={Position.Left}
        style={{ width: 11, height: 11, background: hdr, border: `2px solid ${hndBrd}`, left: -6 }} />

      {/* Header */}
      <div style={{ background: hdr, borderRadius: "6px 6px 0 0", padding: "6px 8px", display: "flex", alignItems: "center", gap: 5 }}>
        <span style={{ fontSize: 13, lineHeight: 1, flexShrink: 0 }}>{cfg.icon}</span>
        <span style={{ color: "#fff", fontSize: 12, fontWeight: 700, flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", textShadow: "0 1px 2px rgba(0,0,0,0.3)" }}>
          {nd.label}
        </span>
        {runStatus && runStatus !== "idle" && (
          <span style={{ width: 7, height: 7, borderRadius: "50%", background: RUN_CLR[runStatus] ?? "#64748b", display: "inline-block", flexShrink: 0, boxShadow: `0 0 5px ${RUN_CLR[runStatus] ?? "#64748b"}` }} />
        )}
        <button onMouseDown={onDelete} title="Delete" style={{ border: "none", background: "rgba(0,0,0,0.3)", color: "#fff", cursor: "pointer", fontSize: 13, lineHeight: 1, borderRadius: 3, padding: "2px 5px", flexShrink: 0 }}>×</button>
      </div>

      {/* Body */}
      <div style={{ padding: "6px 9px 7px", fontSize: 11, color: nodeText, lineHeight: 1.45 }}>
        {nd.nodeType === "note" && nd.noteText
          ? <em style={{ color: "#d97706", fontSize: 10 }}>{String(nd.noteText).slice(0, 75)}</em>
          : nd.refId
            ? <span style={{ color: nodeRef, fontFamily: "monospace", fontSize: 10 }}>{nd.refId.slice(0, 24)}</span>
            : <span style={{ color: nodeDesc, fontSize: 10 }}>{cfg.description.slice(0, 55)}</span>
        }
        {(filledParams > 0 || (runStatus && runStatus !== "idle")) && (
          <div style={{ marginTop: 5, display: "flex", gap: 4, flexWrap: "wrap", alignItems: "center" }}>
            {filledParams > 0 && (
              <span style={{ background: hdr + "25", color: hdr, padding: "1px 6px", borderRadius: 3, fontSize: 9, fontWeight: 700 }}>
                {filledParams} param{filledParams > 1 ? "s" : ""}
              </span>
            )}
            {runStatus && runStatus !== "idle" && (
              <span style={{ fontSize: 9, color: RUN_CLR[runStatus] ?? "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5 }}>
                {runStatus}
              </span>
            )}
          </div>
        )}
      </div>

      <Handle type="source" position={Position.Right}
        style={{ width: 11, height: 11, background: hdr, border: `2px solid ${hndBrd}`, right: -6 }} />
    </div>
  );
};

const GLOSSA_NODE_TYPES = { glossaNode: GlossaNode };

// ── Context Menu ────────────────────────────────────────────────────────────

interface CtxItem { label?: string; icon?: string; danger?: boolean; divider?: boolean; action?: () => void; }

const ContextMenu = ({ x, y, items, onClose }: { x: number; y: number; items: CtxItem[]; onClose: () => void }) => {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const h = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as HTMLElement)) onClose(); };
    setTimeout(() => document.addEventListener("mousedown", h), 0);
    return () => document.removeEventListener("mousedown", h);
  }, [onClose]);
  const left = Math.min(x, window.innerWidth - 185);
  const top  = Math.min(y, window.innerHeight - items.length * 30 - 16);
  return (
    <div ref={ref} style={{ position: "fixed", left, top, background: "#1e293b", border: "1px solid #334155", borderRadius: 7, zIndex: 99999, minWidth: 172, padding: "3px 0", boxShadow: "0 8px 32px rgba(0,0,0,0.55)" }}>
      {items.map((it, i) =>
        it.divider ? <div key={i} style={{ height: 1, background: "#334155", margin: "3px 0" }} /> : (
          <button key={i} onClick={() => { it.action?.(); onClose(); }}
            style={{ display: "flex", alignItems: "center", gap: 7, width: "100%", padding: "6px 12px", border: "none", background: "none", color: it.danger ? "#f87171" : "#e2e8f0", cursor: "pointer", textAlign: "left", fontSize: 12, borderRadius: 4 }}
            onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = "#334155"; }}
            onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = "none"; }}>
            {it.icon && <span style={{ fontSize: 13, width: 16, textAlign: "center" }}>{it.icon}</span>}
            {it.label}
          </button>
        )
      )}
    </div>
  );
};

// ── PaletteItem ─────────────────────────────────────────────────────────────

const PaletteItem = ({ label, nodeType, description, refId, onDragStart }:
  { label: string; nodeType: StudyNodeType; description: string; refId: string;
    onDragStart: (nt: StudyNodeType, refId: string, label: string) => void }) => {
  const cfg = NODE_CFG[nodeType];
  return (
    <div draggable onDragStart={() => onDragStart(nodeType, refId, label)} title={description}
      style={{ padding: "5px 8px", marginBottom: 3, cursor: "grab", border: `1px solid ${cfg.color}30`, borderRadius: 5, background: cfg.color + "0d" }}>
      <div style={{ fontWeight: 600, color: cfg.color, fontSize: 11, display: "flex", alignItems: "center", gap: 4 }}>
        <span>{cfg.icon}</span>{label}
      </div>
      {description && <div style={{ fontSize: 9, color: "#475569", lineHeight: 1.3, marginTop: 1 }}>{description.slice(0, 52)}{description.length > 52 ? "…" : ""}</div>}
    </div>
  );
};

// ── ParamField ──────────────────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const ParamField = ({ fieldKey, def, value, onChange, darkMode = true }: { fieldKey: string; def: Record<string, any>; value: unknown; onChange: (v: unknown) => void; darkMode?: boolean }) => {
  const label = (def.title as string) ?? fieldKey;
  const desc  = def.description as string | undefined;
  const type  = def.type as string;
  const iStyle: React.CSSProperties = { width: "100%", boxSizing: "border-box", padding: "4px 7px",
    border: `1px solid ${darkMode ? "#334155" : "#d1d5db"}`, borderRadius: 4, fontSize: 11, outline: "none",
    background: darkMode ? "#1e293b" : "#ffffff", color: darkMode ? "#e2e8f0" : "#1e293b" };
  let ctrl: React.ReactNode;
  // corpus_id params always get a corpus dropdown (not a text input)
  if (type === "corpus_selector" || fieldKey === "corpus_id") {
    ctrl = <CorpusSelector value={(value as string) ?? ""} onChange={v => onChange(v)} darkMode={darkMode} />;
  } else if (type === "boolean") {
    ctrl = <div style={{ display: "flex", alignItems: "center", gap: 5, marginTop: 3 }}><input type="checkbox" checked={!!value} onChange={e => onChange(e.target.checked)} style={{ cursor: "pointer", width: 14, height: 14 }} /><span style={{ fontSize: 11, color: "#94a3b8" }}>{value ? "Yes" : "No"}</span></div>;
  } else if (type === "integer" || type === "number") {
    ctrl = <input type="number" value={(value as number) ?? (def.default as number) ?? ""} step={type === "integer" ? 1 : "any"} min={def.minimum as number | undefined} max={def.maximum as number | undefined} onChange={e => onChange(type === "integer" ? (parseInt(e.target.value, 10) || 0) : (parseFloat(e.target.value) || 0))} style={iStyle} />;
  } else {
    ctrl = <input type="text" value={(value as string) ?? (def.default as string) ?? ""} onChange={e => onChange(e.target.value)} placeholder={(def.default as string) ?? ""} style={iStyle} />;
  }
  return (
    <div style={{ marginBottom: 9 }}>
      <div style={{ fontSize: 11, fontWeight: 600, color: darkMode ? "#cbd5e1" : "#1e293b", marginBottom: 2 }}>{label}</div>
      {desc && <div style={{ fontSize: 10, color: darkMode ? "#64748b" : "#9ca3af", marginBottom: 3, lineHeight: 1.4 }}>{desc}</div>}
      {ctrl}
    </div>
  );
};

// ── Inspector

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function schemaFromDefaults(defaults: Record<string, any>): Record<string, any> {
  const props: Record<string, Record<string, unknown>> = {};
  for (const [k, v] of Object.entries(defaults)) {
    const title = k.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
    if (typeof v === "boolean") props[k] = { type: "boolean", title, default: v };
    else if (typeof v === "number" && Number.isInteger(v)) props[k] = { type: "integer", title, default: v, minimum: 0 };
    else if (typeof v === "number") props[k] = { type: "number", title, default: v };
    else props[k] = { type: "string", title, default: v ?? "" };
  }
  return { type: "object", properties: props };
}

const BUILTIN_SCHEMAS: Record<string, Record<string, Record<string, unknown>>> = {
  corpus:      { corpus_id:       { type: "corpus_selector", title: "Select Corpus",
                                    description: "Which corpus to load. Blank = default Indus (ICIT). Connected experiments will receive this corpus automatically." } },
  note:        { note_text:       { type: "string", title: "Note Text", description: "Annotation shown on the node." } },
  report:      { report_name:     { type: "string", title: "Report File", description: "Filename in reports/." } },
  hypothesis:  { title:           { type: "string", title: "Hypothesis Title" },
                 hypothesis_id:   { type: "string", title: "Hypothesis ID (existing)" } },
  rag_query:   { query_override:  { type: "string", title: "Query Override", description: "Leave blank to auto-generate from upstream." },
                 top_k:           { type: "integer", title: "Top K", default: 5, minimum: 1, maximum: 20, description: "Max retrieved chunks." } },
  ai_analysis: { prompt:          { type: "string", title: "Prompt", description: "Custom instruction. Leave blank for default." },
                 context_summary: { type: "boolean", title: "Include Context Summary", default: true } },
};

function Inspector({ node, experiments, pipelines, onClose, onParamChange, darkMode = true }:
  { node: Node<NodeData> | null; experiments: ExperimentMeta[]; pipelines: CatalogPipeline[];
    onClose: () => void; onParamChange: (nodeId: string, params: Record<string, unknown>) => void; darkMode?: boolean }) {
  if (!node) return null;
  const cfg = NODE_CFG[node.data.nodeType] ?? NODE_CFG.experiment;
  const params = (node.data.params ?? {}) as Record<string, unknown>;
  // Theme-aware inspector colors
  const iBg    = darkMode ? "#0f172a" : "#f8fafc";
  const iBdr   = darkMode ? "#1e293b" : "#e2e8f0";
  const iText  = darkMode ? "#e2e8f0" : "#1e293b";
  const iMuted = darkMode ? "#64748b" : "#9ca3af";

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let schema: Record<string, Record<string, any>> = {};
  if (node.data.nodeType === "experiment") {
    const exp = experiments.find(e => e.id === node.data.refId);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    schema = ((exp?.params_schema as Record<string, any> | null)?.properties as Record<string, Record<string, any>> | undefined) ?? {};
  } else if (node.data.nodeType === "pipeline") {
    const pipe = pipelines.find(p => p.id === node.data.refId);
    if (pipe?.default_params && Object.keys(pipe.default_params).length > 0)
      schema = schemaFromDefaults(pipe.default_params).properties ?? {};
  } else {
    schema = BUILTIN_SCHEMAS[node.data.nodeType] ?? {};
  }

  return (
    <div style={{ width: 252, borderLeft: `1px solid ${iBdr}`, padding: "11px 12px", background: iBg, overflowY: "auto", flexShrink: 0 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
        <span style={{ fontSize: 12, fontWeight: 700, color: cfg.color }}>{cfg.icon} {node.data.nodeType.replace(/_/g, " ")}</span>
        <button onClick={onClose} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 14, color: iMuted }}>✕</button>
      </div>
      <div style={{ fontSize: 12, fontWeight: 600, color: iText, marginBottom: 4 }}>{node.data.label}</div>
      {node.data.description && (
        <p style={{ fontSize: 10, color: iMuted, lineHeight: 1.45, margin: "0 0 10px" }}>
          {(node.data.description as string).slice(0, 110)}
        </p>
      )}
      {Object.keys(schema).length > 0 ? (
        <div>
          <div style={{ fontSize: 9, fontWeight: 700, color: iMuted, textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8, borderTop: `1px solid ${iBdr}`, paddingTop: 8 }}>Parameters</div>
          {Object.entries(schema).map(([k, def]) => (
            <ParamField key={k} fieldKey={k} def={def} value={params[k] ?? def.default} darkMode={darkMode}
              onChange={v => onParamChange(node.id, { ...params, [k]: v })} />
          ))}
          <div style={{ fontSize: 9, color: iMuted }}>Saved with study graph.</div>
        </div>
      ) : (
        <div style={{ fontSize: 10, color: iMuted, fontStyle: "italic", marginTop: 6 }}>No configurable parameters.</div>
      )}
      <div style={{ marginTop: 10, paddingTop: 8, borderTop: `1px solid ${iBdr}` }}>
        {node.data.refId && <div style={{ fontSize: 9, color: iMuted, fontFamily: "monospace" }}>ref: {node.data.refId}</div>}
        <div style={{ fontSize: 9, color: iMuted, marginTop: 1 }}>id: {node.id.slice(0, 18)}</div>
      </div>
    </div>
  );
}

// ── New Study Dialog ────────────────────────────────────────────────────────

function NewStudyDialog({ onClose, onCreated }: { onClose: () => void; onCreated: (s: StudyResponse) => void }) {
  const [name, setName] = useState(""); const [desc, setDesc] = useState("");
  const [busy, setBusy] = useState(false); const [err, setErr] = useState<string | null>(null);
  const bdRef = useRef<HTMLDivElement>(null);
  const go = async () => {
    if (!name.trim()) { setErr("Name is required."); return; }
    setBusy(true); setErr(null);
    try { const s = await createStudy({ name: name.trim(), description: desc.trim() }); onCreated(s); onClose(); }
    catch (e) { setErr(e instanceof Error ? e.message : String(e)); }
    finally { setBusy(false); }
  };
  const inp: React.CSSProperties = { display: "block", width: "100%", boxSizing: "border-box", padding: "7px 10px", border: "1px solid #334155", borderRadius: 6, fontSize: 13, marginBottom: 10, outline: "none", background: "#0f172a", color: "#e2e8f0" };
  return (
    <div ref={bdRef} onClick={e => { if (e.target === bdRef.current) onClose(); }}
      style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.65)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 10000 }}>
      <div style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 10, padding: "1.5rem", width: 450, maxWidth: "95vw", boxShadow: "0 20px 60px rgba(0,0,0,0.6)" }}>
        <h3 style={{ margin: "0 0 1rem", color: "#e2e8f0", fontSize: 15 }}>Create New Study</h3>
        <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: "#64748b", marginBottom: 4 }}>Study name *</label>
        <input autoFocus value={name} onChange={e => setName(e.target.value)} onKeyDown={e => { if (e.key === "Enter") void go(); }} placeholder="e.g. Indus Sign Formula Analysis" style={inp} />
        <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: "#64748b", marginBottom: 4 }}>Description (optional)</label>
        <textarea value={desc} onChange={e => setDesc(e.target.value)} rows={3} placeholder="Research goal…" style={{ ...inp, resize: "vertical", fontFamily: "inherit" }} />
        {err && <div style={{ padding: "6px 10px", background: "#450a0a", border: "1px solid #7f1d1d", borderRadius: 5, fontSize: 12, color: "#fca5a5", marginBottom: 10 }}>{err}</div>}
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <button onClick={onClose} disabled={busy} style={{ padding: "7px 16px", border: "1px solid #334155", borderRadius: 6, cursor: "pointer", fontSize: 12, background: "none", color: "#64748b" }}>Cancel</button>
          <button onClick={() => void go()} disabled={busy} style={{ padding: "7px 18px", border: "none", borderRadius: 6, cursor: busy ? "not-allowed" : "pointer", fontSize: 12, fontWeight: 600, background: "#7c3aed", color: "#fff" }}>
            {busy ? "Creating…" : "Create Study"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── StudySummaryPanel ───────────────────────────────────────────────────────

function StudySummaryPanel({ summary, onClose }: { summary: AISummaryResult; onClose: () => void }) {
  return (
    <div style={{ border: "1px solid #7c3aed40", borderRadius: 8, overflow: "hidden", background: "#0f0a1e", marginTop: 6 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#7c3aed", padding: "7px 12px" }}>
        <span style={{ color: "#fff", fontWeight: 700, fontSize: 12 }}>✨ AI Study Summary</span>
        <button onClick={onClose} style={{ border: "none", background: "none", color: "rgba(255,255,255,0.8)", cursor: "pointer", fontSize: 16 }}>✕</button>
      </div>
      <div style={{ padding: "12px 14px", display: "flex", flexDirection: "column", gap: 8, color: "#e2e8f0" }}>
        {summary.abstract && <p style={{ margin: 0, fontSize: 12, lineHeight: 1.6 }}>{summary.abstract}</p>}
        {(summary.highlights?.length ?? 0) > 0 && <ul style={{ margin: 0, paddingLeft: 18 }}>{summary.highlights.map((h, i) => <li key={i} style={{ fontSize: 11 }}>{h}</li>)}</ul>}
        {(summary.next_steps?.length ?? 0) > 0 && <div>
          <div style={{ fontSize: 9, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", marginBottom: 3 }}>Next Steps</div>
          <ul style={{ margin: 0, paddingLeft: 18 }}>{summary.next_steps.map((s, i) => <li key={i} style={{ fontSize: 11, color: "#94a3b8" }}>{s}</li>)}</ul>
        </div>}
      </div>
    </div>
  );
}

// ── AutoFitView — must live inside ReactFlow provider ───────────────────────

function AutoFitView({ trigger }: { trigger: number }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    if (trigger > 0) setTimeout(() => fitView({ padding: 0.2 }), 80);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [trigger]);
  return null;
}

// ── Main: StudyBuilderView ──────────────────────────────────────────────────

let _nid = 0;
function nextNodeId() { return `n_${Date.now()}_${_nid++}`; }

const SPECIAL_TYPES: StudyNodeType[] = ["corpus", "rag_query", "ai_analysis", "compare", "note", "report", "hypothesis"];

// Snap a coordinate to the 15px grid
const snap15 = (n: number) => Math.round(n / 15) * 15;

export function StudyBuilderView({ darkMode = true }: { darkMode?: boolean }) {
  const th = sbTheme(darkMode);
  // Shared helper to create node data with darkMode baked in
  const mkNodeData = useCallback((base: NodeData): NodeData => ({ ...base, darkMode } as NodeData & { darkMode: boolean }), [darkMode]);
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [pipelines, setPipelines]     = useState<CatalogPipeline[]>([]);
  const [studies, setStudies]         = useState<StudyResponse[]>([]);
  const [activeStudy, setActiveStudy] = useState<StudyResponse | null>(null);

  const [nodes, setNodes] = useState<Node<NodeData>[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedNode, setSelectedNode] = useState<Node<NodeData> | null>(null);

  // ── Multi-run state (one entry per running study) ─────────────────────
  type ActiveRun = {
    controller: AbortController;
    startTime: number;
    nodeStatuses: Record<string, string>;  // nodeId → status
    currentNodeLabel: string;
    currentNodeIdx: number;
    totalNodes: number;
  };
  const [activeRuns, setActiveRuns] = useState<Record<string, ActiveRun>>({});
  const activeRunsRef = useRef<Record<string, ActiveRun>>({});
  useEffect(() => { activeRunsRef.current = activeRuns; }, [activeRuns]);
  const [, setTick] = useState(0);  // force re-render for elapsed display
  const hasActiveRuns = Object.keys(activeRuns).length > 0;
  useEffect(() => {
    if (!hasActiveRuns) return;
    const t = setInterval(() => setTick(n => n + 1), 1000);
    return () => clearInterval(t);
  }, [hasActiveRuns]);
  const getElapsed = (studyId: string) => {
    const r = activeRuns[studyId]; if (!r) return 0;
    return Math.floor((Date.now() - r.startTime) / 1000);
  };

  // Per-study run result cache — persisted across navigation
  type RunCacheEntry = { completed: number; errors: number; ts: number; nodeCount: number };
  const [runCache, setRunCache] = useState<Record<string, RunCacheEntry>>(() => {
    try { return JSON.parse(localStorage.getItem("gsb_run_cache") ?? "{}") as Record<string, RunCacheEntry>; }
    catch { return {}; }
  });
  const saveToRunCache = useCallback((studyId: string, entry: RunCacheEntry) => {
    setRunCache(prev => {
      const next = { ...prev, [studyId]: entry };
      localStorage.setItem("gsb_run_cache", JSON.stringify(next));
      return next;
    });
  }, []);

  const [runResult, setRunResult] = useState<StudyRunResult | null>(null);
  const [runError, setRunError]   = useState<string | null>(null);
  const [saving, setSaving]       = useState(false);
  const [saveMsg, setSaveMsg]     = useState<string | null>(null);

  const [summarizing, setSummarizing] = useState(false);
  const [summary, setSummary]         = useState<AISummaryResult | null>(null);

  // Dirty tracking — compare canonical save form to last-saved reference
  const [isDirty, setIsDirty]       = useState(false);
  const savedGraphJson = useRef<string>("");  // canonical JSON of last-saved state
  const justLoaded     = useRef(false);       // suppress dirty on initial load

  const [palSearch, setPalSearch] = useState("");
  const [palFilter, setPalFilter] = useState<"all" | "experiment" | "pipeline" | "special">("all");
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [showNewStudy, setShowNewStudy]   = useState(false);
  const [inspectorOff, setInspectorOff]  = useState(false);
  const [ctxMenu, setCtxMenu] = useState<{ x: number; y: number; type: "pane" | "node" | "edge"; nodeId?: string; edgeId?: string } | null>(null);

  // Panel layout — outer left-panel width + inner studies/palette split
  const [leftW, setLeftW] = useState<number>(() => parseInt(localStorage.getItem("gsb_lw")  ?? "238", 10));
  const [studiesH, setStudiesH] = useState<number>(() => parseInt(localStorage.getItem("gsb_sh") ?? "180", 10));
  const [leftOff, setLeftOff] = useState(false);
  const [dockL, setDockL]    = useState<boolean>(() => localStorage.getItem("gsb_dock") !== "right");
  const isDragging     = useRef(false);
  const dragStart      = useRef(0);
  const dragW0         = useRef(leftW);
  const innerDivStart  = useRef(0);
  const innerDivH0     = useRef(studiesH);

  // RAG
  const [ragReady, setRagReady]     = useState(false);
  const [ragBuilding, setRagBuilding] = useState(false);

  // AI menu dropdown
  const [aiMenuOpen, setAiMenuOpen] = useState(false);

  // Auto-arrange fit trigger
  const [fitTrigger, setFitTrigger] = useState(0);

  // Starred / pinned studies — floated to top, persisted across sessions
  const [starredStudies, setStarredStudies] = useState<Set<string>>(() => {
    try { return new Set(JSON.parse(localStorage.getItem("glossa_starred_studies") ?? "[]")); }
    catch { return new Set(); }
  });
  const toggleStarStudy = (id: string) => {
    setStarredStudies(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      localStorage.setItem("glossa_starred_studies", JSON.stringify([...next]));
      return next;
    });
  };

  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const draggedRef = useRef<{ nodeType: StudyNodeType; refId: string; label: string } | null>(null);
  const reconnectOk = useRef(false);
  const { openChat } = useAIChat();

  // On mount: clear any stale draft left from a previous session so the
  // nav sidebar never shows an incorrect orange dot on startup.
  useEffect(() => {
    localStorage.removeItem("glossa_study_draft");
    window.dispatchEvent(new CustomEvent("glossa:dirty", { detail: { builder: "study", dirty: false } }));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load
  useEffect(() => {
    void listExperiments().then(setExperiments).catch(() => {});
    void getPipelineCatalog().then(setPipelines).catch(() => {});
    void listStudies().then(setStudies).catch(() => {});
    void getRagStatus().then(s => setRagReady(s.ready)).catch(() => {});
  }, []);
  useEffect(() => { localStorage.setItem("gsb_lw", String(leftW)); }, [leftW]);
  useEffect(() => { localStorage.setItem("gsb_sh", String(studiesH)); }, [studiesH]);
  useEffect(() => { localStorage.setItem("gsb_dock", dockL ? "left" : "right"); }, [dockL]);

  // ── Dirty tracking ──────────────────────────────────────────────────────────
  // Canonical helper — same field set as doSave so comparisons are valid
  // (position is included so moving nodes also triggers the dirty flag).
  const canonNodes = useCallback(() =>
    nodes.map(n => ({
      id: n.id, type: n.data.nodeType, ref_id: n.data.refId ?? "",
      label: n.data.label ?? "", params: n.data.params ?? {},
      note_text: n.data.noteText ?? "", color: n.data.color ?? "",
      position: n.position,
    })), [nodes]);
  const canonEdges = useCallback(() =>
    edges.map(e => ({ id: e.id, source: e.source, target: e.target })), [edges]);

  useEffect(() => {
    // Skip the very first render after loadStudy — the initial node/edge state
    // reflects the saved graph, not a user change.
    if (justLoaded.current) { justLoaded.current = false; return; }
    if (!activeStudy) return;
    const currentJson = JSON.stringify({ nodes: canonNodes(), edges: canonEdges() });
    const dirty = currentJson !== savedGraphJson.current;
    setIsDirty(dirty);
    if (dirty) {
      localStorage.setItem("glossa_study_draft", currentJson);
      window.dispatchEvent(new CustomEvent("glossa:dirty", { detail: { builder: "study", dirty: true } }));
    } else {
      localStorage.removeItem("glossa_study_draft");
      window.dispatchEvent(new CustomEvent("glossa:dirty", { detail: { builder: "study", dirty: false } }));
    }
  }, [nodes, edges, activeStudy]); // eslint-disable-line react-hooks/exhaustive-deps

  // Load study into graph — snap positions to 15px grid and reset dirty state
  const loadStudy = useCallback((s: StudyResponse) => {
    justLoaded.current = true;   // next effect run is the initial load — don't mark dirty
    const snNodes = (s.graph.nodes ?? []).map(n => ({
      id: n.id, type: n.type, ref_id: n.ref_id ?? "",
      label: n.label ?? "", params: n.params ?? {},
      note_text: n.note_text ?? "", color: n.color ?? "",
      position: { x: snap15((n.position?.x ?? 80)), y: snap15((n.position?.y ?? 80)) },
    }));
    const snEdges = (s.graph.edges ?? []).map(e => ({ id: e.id, source: e.source, target: e.target }));
    savedGraphJson.current = JSON.stringify({ nodes: snNodes, edges: snEdges });
    setIsDirty(false);
    localStorage.removeItem("glossa_study_draft");
    window.dispatchEvent(new CustomEvent("glossa:dirty", { detail: { builder: "study", dirty: false } }));
    setActiveStudy(s); setSelectedNode(null); setSummary(null);
    // Build nodes — if a run is currently active for this study, restore its node statuses
    const currentRun = activeRunsRef.current[s.id];
    setNodes((s.graph.nodes ?? []).map(n => ({
      id: n.id, type: "glossaNode",
      position: { x: snap15((n.position?.x ?? 80)), y: snap15((n.position?.y ?? 80)) },
      data: { label: n.label, nodeType: n.type as StudyNodeType, refId: n.ref_id, params: n.params ?? {}, noteText: n.note_text, color: n.color,
              runStatus: (currentRun ? (currentRun.nodeStatuses[n.id] ?? "idle") : "idle") as NodeData["runStatus"],
              darkMode } as NodeData,
    })));
    setEdges((s.graph.edges ?? []).map(e => ({ id: e.id, source: e.source, target: e.target, reconnectable: true, style: { stroke: th.edgeDef, strokeWidth: 2 } })));
  }, [darkMode, th.edgeDef]);

  // Save
  const doSave = useCallback(async () => {
    if (!activeStudy) return;
    setSaving(true);
    try {
      const graph: StudyGraph = {
        nodes: nodes.map(n => ({ id: n.id, type: n.data.nodeType as StudyNodeType, ref_id: n.data.refId, label: n.data.label, params: (n.data.params ?? {}) as Record<string, unknown>, note_text: n.data.noteText ?? "", color: n.data.color ?? "", position: n.position })),
        edges: edges.map(e => ({ id: e.id, source: e.source, target: e.target })),
      };
      const updated = await updateStudy(activeStudy.id, { graph });
      // Update the saved-state reference so dirty clears immediately
      savedGraphJson.current = JSON.stringify({ nodes: canonNodes(), edges: canonEdges() });
      setIsDirty(false);
      localStorage.removeItem("glossa_study_draft");
      window.dispatchEvent(new CustomEvent("glossa:dirty", { detail: { builder: "study", dirty: false } }));
      setActiveStudy(updated);
      setStudies(prev => prev.map(s => s.id === updated.id ? updated : s));
      setSaveMsg("Saved"); setTimeout(() => setSaveMsg(null), 2000);
    } catch { setSaveMsg("Failed"); }
    finally { setSaving(false); }
  }, [activeStudy, nodes, edges, canonNodes, canonEdges]);

  // Revert — discard all unsaved changes and reload last-saved state
  const doRevert = useCallback(() => {
    if (!activeStudy) return;
    loadStudy(activeStudy);  // activeStudy always holds the last-saved graph
  }, [activeStudy, loadStudy]);

  // ── Run (streaming, supports multiple concurrent) ──────────────────────
  const doRun = useCallback(async (target: StudyResponse) => {
    if (activeRunsRef.current[target.id]) return;  // already running
    setRunError(null);
    if (target.id === activeStudy?.id) {
      await doSave();
    }
    const controller = new AbortController();
    const startTime = Date.now();
    const initRun: ActiveRun = { controller, startTime, nodeStatuses: {}, currentNodeLabel: "", currentNodeIdx: 0, totalNodes: 0 };
    setActiveRuns(prev => ({ ...prev, [target.id]: initRun }));
    window.dispatchEvent(new CustomEvent("glossa:running", { detail: { builder: "study", running: true, id: target.id, name: target.name } }));

    try {
      for await (const ev of runStudyStream(target.id, controller.signal)) {
        if (ev.event === "started") {
          setActiveRuns(prev => ({ ...prev, [target.id]: { ...prev[target.id], totalNodes: ev.node_count ?? 0 } }));
        } else if (ev.event === "node_start" && ev.nid) {
          const nid = ev.nid;
          setActiveRuns(prev => ({
            ...prev, [target.id]: { ...prev[target.id],
              currentNodeLabel: ev.label ?? "", currentNodeIdx: ev.idx ?? 0,
              totalNodes: ev.total ?? prev[target.id]?.totalNodes ?? 0,
              nodeStatuses: { ...prev[target.id]?.nodeStatuses, [nid]: "running" },
            }
          }));
          // Update canvas if this is the active study
          if (activeStudy?.id === target.id || !activeStudy) {
            setNodes(prev => prev.map(n => ({
              ...n, data: { ...n.data,
                runStatus: n.id === nid ? "running" : (n.data.runStatus === "running" ? "idle" : n.data.runStatus) }
            })));
          }
        } else if (ev.event === "node_end" && ev.nid) {
          const nid = ev.nid; const st = (ev.status ?? "idle") as NodeRunStatus;
          setActiveRuns(prev => ({
            ...prev, [target.id]: { ...prev[target.id],
              nodeStatuses: { ...prev[target.id]?.nodeStatuses, [nid]: st } }
          }));
          if (activeStudy?.id === target.id || !activeStudy) {
            setNodes(prev => prev.map(n => n.id === nid ? { ...n, data: { ...n.data, runStatus: st } } : n));
          }
        } else if (ev.event === "run_complete") {
          saveToRunCache(target.id, { completed: ev.completed ?? 0, errors: ev.errors ?? 0, nodeCount: ev.node_count ?? 0, ts: Date.now() });
          if (activeStudy?.id === target.id || !activeStudy) {
            setRunResult(ev as unknown as StudyRunResult);
          }
        } else if (ev.event === "run_error") {
          setRunError(ev.message ?? "Run failed");
          saveToRunCache(target.id, { completed: 0, errors: 1, nodeCount: 0, ts: Date.now() });
        }
      }
    } catch (e) {
      if (!(e instanceof DOMException && e.name === "AbortError")) {
        setRunError(e instanceof Error ? e.message : "Run failed");
        saveToRunCache(target.id, { completed: 0, errors: 1, nodeCount: 0, ts: Date.now() });
        window.dispatchEvent(new CustomEvent("glossa:running", { detail: { builder: "study", running: false, id: target.id, status: "fail" } }));
      } else {
        // Aborted by user — treat as failure so indicator shows red
        window.dispatchEvent(new CustomEvent("glossa:running", { detail: { builder: "study", running: false, id: target.id, status: "fail" } }));
      }
      return;
    } finally {
      setActiveRuns(prev => { const n = { ...prev }; delete n[target.id]; return n; });
    }
    // Normal completion (no exception): status comes from run_complete event errors field
    const cached = runCache[target.id];
    const wasSuccess = !cached || cached.errors === 0;
    window.dispatchEvent(new CustomEvent("glossa:running", { detail: { builder: "study", running: false, id: target.id, status: wasSuccess ? "success" : "fail" } }));
  }, [activeStudy, doSave, saveToRunCache, runCache]);

  const stopAll = useCallback(() => {
    Object.values(activeRunsRef.current).forEach(r => r.controller.abort());
  }, []);

  // Delete / duplicate / export / import study
  const delStudy = useCallback(async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (deleteConfirm !== id) { setDeleteConfirm(id); setTimeout(() => setDeleteConfirm(null), 3000); return; }
    setDeleteConfirm(null);
    await deleteStudy(id);
    setStudies(prev => prev.filter(s => s.id !== id));
    if (activeStudy?.id === id) { setActiveStudy(null); setNodes([]); setEdges([]); setSelectedNode(null); }
  }, [deleteConfirm, activeStudy]);

  const dupStudy = useCallback(async (s: StudyResponse) => {
    // Snap positions when duplicating too
    const snappedGraph = {
      ...s.graph,
      nodes: (s.graph.nodes ?? []).map(n => ({ ...n, position: { x: snap15(n.position.x), y: snap15(n.position.y) } })),
    };
    const c = await createStudy({ name: `${s.name} (copy)`, description: s.description, graph: snappedGraph });
    setStudies(prev => [c, ...prev]); loadStudy(c);
  }, [loadStudy]);

  const exportStudy = useCallback(() => {
    if (!activeStudy) return;
    const blob = new Blob([JSON.stringify({ name: activeStudy.name, description: activeStudy.description, graph: activeStudy.graph }, null, 2)], { type: "application/json" });
    const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: `${activeStudy.name.replace(/\s+/g, "_")}.glossa-study.json` });
    a.click(); URL.revokeObjectURL(a.href);
  }, [activeStudy]);

  const importRef = useRef<HTMLInputElement>(null);
  const onImport = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    try { const d = JSON.parse(await f.text()); const s = await createStudy({ name: d.name || f.name, description: d.description || "", graph: d.graph }); setStudies(prev => [s, ...prev]); loadStudy(s); }
    catch { alert("Invalid study file."); }
    e.target.value = "";
  }, [loadStudy]);

  // React Flow callbacks
  const onNodesChange = useCallback((ch: NodeChange[]) => setNodes(n => applyNodeChanges(ch, n) as Node<NodeData>[]), []);
  const onEdgesChange = useCallback((ch: EdgeChange[]) => setEdges(e => applyEdgeChanges(ch, e)), []);
  const onConnect = useCallback((c: Connection) => setEdges(e => addEdge({ ...c, reconnectable: true, style: { stroke: "#334155", strokeWidth: 2 } }, e)), []);
  const onNodeClick = useCallback((_: React.MouseEvent, n: Node) => { setSelectedNode(n as Node<NodeData>); setCtxMenu(null); setInspectorOff(false); }, []);
  const onPaneClick = useCallback(() => { setSelectedNode(null); setCtxMenu(null); }, []);
  const onReconnectStart = useCallback(() => { reconnectOk.current = false; }, []);
  const onReconnect = useCallback((old: Edge, conn: Connection) => { reconnectOk.current = true; setEdges(es => reconnectEdge(old, conn, es)); }, []);
  const onReconnectEnd = useCallback((_: unknown, edge: Edge) => { if (!reconnectOk.current) setEdges(es => es.filter(e => e.id !== edge.id)); reconnectOk.current = false; }, []);

  // Drop — position at cursor (no arbitrary offset)
  const onDrop = useCallback((ev: React.DragEvent<HTMLDivElement>) => {
    ev.preventDefault();
    if (!activeStudy) return;  // guard: no project open, ignore drop
    if (!draggedRef.current || !reactFlowWrapper.current) return;
    const rect = reactFlowWrapper.current.getBoundingClientRect();
    const pos = { x: snap15(ev.clientX - rect.left - 8), y: snap15(ev.clientY - rect.top - 8) };
    const { nodeType, refId, label } = draggedRef.current;
    const desc = nodeType === "experiment" ? (experiments.find(e => e.id === refId)?.description ?? "")
               : nodeType === "pipeline"   ? (pipelines.find(p => p.id === refId)?.description ?? "")
               : NODE_CFG[nodeType]?.description ?? "";
    setNodes(n => [...n, { id: nextNodeId(), type: "glossaNode", position: pos, data: mkNodeData({ label, nodeType, refId, description: desc, params: {}, runStatus: "idle" }) }]);
    draggedRef.current = null;
  }, [experiments, pipelines, mkNodeData]);

  const onDragOver = (ev: React.DragEvent) => {
    if (!activeStudy) return;  // no drop target when no project
    ev.preventDefault(); ev.dataTransfer.dropEffect = "move";
  };
  const onDragStart = useCallback((nt: StudyNodeType, refId: string, label: string) => { draggedRef.current = { nodeType: nt, refId, label }; }, []);

  // Auto-arrange
  const doArrange = useCallback(() => {
    setNodes(prev => autoArrange(prev, edges) as Node<NodeData>[]);
    setFitTrigger(t => t + 1);
  }, [edges]);

  // Param change
  const onParamChange = useCallback((nodeId: string, p: Record<string, unknown>) => {
    setNodes(prev => prev.map(n => n.id === nodeId ? { ...n, data: { ...n.data, params: p } } : n));
    setSelectedNode(prev => prev?.id === nodeId ? { ...prev, data: { ...prev.data, params: p } } : prev);
  }, []);

  // Context menus — properly typed handlers
  const onNodeCtx = useCallback((ev: React.MouseEvent, n: Node) => {
    ev.preventDefault(); ev.stopPropagation();
    setCtxMenu({ x: ev.clientX, y: ev.clientY, type: "node", nodeId: n.id });
    setSelectedNode(n as Node<NodeData>);
  }, []);
  const onEdgeCtx = useCallback((ev: React.MouseEvent, edge: Edge) => {
    ev.preventDefault(); ev.stopPropagation();
    setCtxMenu({ x: ev.clientX, y: ev.clientY, type: "edge", edgeId: edge.id });
  }, []);
  // Pane right-click is handled via direct onContextMenu on the wrapper div (more reliable)
  const onPaneCtxMenu = useCallback((ev: React.MouseEvent<HTMLDivElement>) => {
    ev.preventDefault();
    setCtxMenu({ x: ev.clientX, y: ev.clientY, type: "pane" });
  }, []);

  const addNodeAt = useCallback((nt: StudyNodeType, x: number, y: number) => {
    if (!reactFlowWrapper.current) return;
    const rect = reactFlowWrapper.current.getBoundingClientRect();
    const pos = { x: snap15(x - rect.left - 8), y: snap15(y - rect.top - 8) };
    setNodes(n => [...n, { id: nextNodeId(), type: "glossaNode", position: pos, data: mkNodeData({ label: NODE_CFG[nt].defaultLabel, nodeType: nt, refId: "", params: {}, runStatus: "idle" }) }]);
  }, [mkNodeData]);

  const nodeCtxItems = useCallback((nodeId: string): CtxItem[] => {
    const nd = nodes.find(n => n.id === nodeId);
    return [
      { icon: "⎘", label: "Duplicate", action: () => { if (!nd) return; setNodes(n => [...n, { id: nextNodeId(), type: "glossaNode", position: { x: nd.position.x + 20, y: nd.position.y + 20 }, data: { ...nd.data, runStatus: "idle" } as NodeData }]); } },
      { icon: "✏", label: "Rename", action: () => { const lbl = prompt("Label:", nd?.data.label as string || ""); if (lbl !== null) setNodes(n => n.map(node => node.id === nodeId ? { ...node, data: { ...node.data, label: lbl } } : node)); } },
      { divider: true },
      { icon: "🔗", label: "Disconnect all edges", action: () => setEdges(e => e.filter(ed => ed.source !== nodeId && ed.target !== nodeId)) },
      { divider: true },
      { icon: "🗑", label: "Delete node", danger: true, action: () => { setNodes(n => n.filter(node => node.id !== nodeId)); setEdges(e => e.filter(ed => ed.source !== nodeId && ed.target !== nodeId)); if (selectedNode?.id === nodeId) setSelectedNode(null); } },
    ];
  }, [nodes, selectedNode]);

  const edgeCtxItems = useCallback((edgeId: string): CtxItem[] => [
    { icon: "🗑", label: "Delete connection", danger: true, action: () => setEdges(e => e.filter(ed => ed.id !== edgeId)) },
    { icon: "↔", label: "Reverse direction", action: () => setEdges(e => e.map(ed => ed.id === edgeId ? { ...ed, source: ed.target, target: ed.source } : ed)) },
  ], []);

  const paneCtxItems = useCallback((x: number, y: number): CtxItem[] => {
    if (!activeStudy) return [];  // no add-node menu when no project is open
    return [
    { icon: "🧪", label: "Add Experiment", action: () => addNodeAt("experiment", x, y) },
    { icon: "⚙️", label: "Add Pipeline", action: () => addNodeAt("pipeline", x, y) },
    { icon: "📚", label: "Add Corpus", action: () => addNodeAt("corpus", x, y) },
    { divider: true },
    { icon: "🔍", label: "Add RAG Query", action: () => addNodeAt("rag_query", x, y) },
    { icon: "✨", label: "Add AI Analysis", action: () => addNodeAt("ai_analysis", x, y) },
    { divider: true },
    { icon: "📝", label: "Add Note", action: () => addNodeAt("note", x, y) },
    { icon: "📄", label: "Add Report Link", action: () => addNodeAt("report", x, y) },
    { icon: "💡", label: "Add Hypothesis", action: () => addNodeAt("hypothesis", x, y) },
    { icon: "↔️", label: "Add Compare", action: () => addNodeAt("compare", x, y) },
    { divider: true },
    { icon: "⊞", label: "Select all", action: () => setNodes(n => n.map(node => ({ ...node, selected: true }))) },
    { icon: "✖", label: "Clear canvas", danger: true, action: () => { setNodes([]); setEdges([]); setSelectedNode(null); } },
    ];
  }, [activeStudy, addNodeAt]);

  // Outer panel divider drag (width)
  const onDividerDown = useCallback((e: React.MouseEvent) => {
    isDragging.current = true; dragStart.current = e.clientX; dragW0.current = leftW;
    const onMove = (me: MouseEvent) => { if (!isDragging.current) return; const dx = dockL ? me.clientX - dragStart.current : dragStart.current - me.clientX; setLeftW(Math.max(160, Math.min(420, dragW0.current + dx))); };
    const onUp   = () => { isDragging.current = false; document.removeEventListener("mousemove", onMove); document.removeEventListener("mouseup", onUp); };
    document.addEventListener("mousemove", onMove); document.addEventListener("mouseup", onUp);
  }, [leftW, dockL]);

  // Inner panel divider drag (studies-list height vs palette)
  const onInnerDivDown = useCallback((e: React.MouseEvent) => {
    innerDivStart.current = e.clientY; innerDivH0.current = studiesH;
    e.preventDefault(); e.stopPropagation();
    const onMove = (me: MouseEvent) => { setStudiesH(Math.max(60, Math.min(400, innerDivH0.current + me.clientY - innerDivStart.current))); };
    const onUp   = () => { document.removeEventListener("mousemove", onMove); document.removeEventListener("mouseup", onUp); };
    document.addEventListener("mousemove", onMove); document.addEventListener("mouseup", onUp);
  }, [studiesH]);

  // Filtered palette
  const fExps  = experiments.filter(e => (palFilter === "all" || palFilter === "experiment") && (!palSearch || e.name.toLowerCase().includes(palSearch.toLowerCase())));
  const fPipes = pipelines.filter(p => (palFilter === "all" || palFilter === "pipeline") && (!palSearch || (p.label ?? p.id).toLowerCase().includes(palSearch.toLowerCase())));

  // Animated edges — animate when the active study is running
  const activeStudyRunning = activeStudy ? !!activeRuns[activeStudy.id] : false;
  const animEdges = useMemo(() => edges.map(e => ({ ...e, animated: activeStudyRunning, style: { stroke: activeStudyRunning ? "#7c3aed" : th.edgeDef, strokeWidth: 2 } })), [edges, activeStudyRunning, th.edgeDef]);

  // ── Left panel — theme-aware ──
  const LeftPanel = (
    <div style={{ width: leftOff ? 32 : leftW, background: th.panelBg, [dockL ? "borderRight" : "borderLeft"]: `1px solid ${th.border}`, display: "flex", flexDirection: "column", flexShrink: 0, overflow: "hidden", transition: "width 0.12s" }}>
      <div style={{ padding: "6px 5px", borderBottom: `1px solid ${th.border}`, display: "flex", alignItems: "center", gap: 3, flexShrink: 0 }}>
        <button onClick={() => setLeftOff(c => !c)} title={leftOff ? "Expand" : "Collapse"} style={{ border: "none", background: "none", color: th.textMuted, cursor: "pointer", fontSize: 13, padding: "2px 4px", borderRadius: 3 }}>{leftOff ? "▶" : "◀"}</button>
        {!leftOff && <><span style={{ fontSize: 10, fontWeight: 700, color: th.textFaint, flex: 1, textTransform: "uppercase", letterSpacing: 0.5 }}>Workspace</span><button onClick={() => setDockL(d => !d)} title="Switch dock side" style={{ border: "none", background: "none", color: th.textFaint, cursor: "pointer", fontSize: 12 }}>⇄</button></>}
      </div>

      {!leftOff && (
        <>
      {/* Studies list — height controlled by inner resize divider */}
          <div style={{ padding: "7px 7px 4px", borderBottom: `1px solid ${th.border}`, flexShrink: 0, height: studiesH, overflowY: "auto", boxSizing: "border-box" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 3, marginBottom: 5 }}>
              <span style={{ fontSize: 9, fontWeight: 700, color: th.textMuted, textTransform: "uppercase", letterSpacing: 0.5, flex: 1 }}>Studies</span>
              <button onClick={() => studies.filter(s => !activeRuns[s.id]).forEach(s => void doRun(s))}
                title="Run all studies in parallel" disabled={studies.length === 0 || hasActiveRuns}
                style={{ ...bm, color: "#22c55e", borderColor: "#15803d40", padding: "0 4px", opacity: studies.length === 0 || hasActiveRuns ? 0.4 : 1 }}>▶▶</button>
              <button onClick={() => setShowNewStudy(true)} title="New study" style={{ ...bm, color: th.textMuted, borderColor: th.border }}>+</button>
              <button onClick={() => importRef.current?.click()} title="Import" style={{ ...bm, color: th.textMuted, borderColor: th.border }}>↑</button>
              <input ref={importRef} type="file" accept=".json" style={{ display: "none" }} onChange={onImport} />
            </div>
            {studies.length === 0 && <div style={{ fontSize: 10, color: th.textFaint, fontStyle: "italic", padding: "4px 2px" }}>No studies yet. Click + to create one.</div>}
            {[...studies].sort((a, b) => {
              const aS = starredStudies.has(a.id), bS = starredStudies.has(b.id);
              return aS === bS ? 0 : aS ? -1 : 1;
            }).map(s => {
              const active    = activeStudy?.id === s.id;
              const modified  = active && isDirty;
              const isRunning = !!activeRuns[s.id];
              const isStarred = starredStudies.has(s.id);
              const run = activeRuns[s.id];
              const cached = runCache[s.id];
              const runBadge = isRunning && run
                ? { label: `⏳ ${getElapsed(s.id)}s · ${run.currentNodeLabel.slice(0,16) || `${run.currentNodeIdx + 1}/${run.totalNodes}`}`, color: "#60a5fa" }
                : cached
                  ? cached.errors > 0
                    ? { label: `✗ ${cached.completed}/${cached.nodeCount}`, color: "#ef4444" }
                    : { label: `✓ ${cached.completed}/${cached.nodeCount}`, color: "#22c55e" }
                  : null;
              return (
                <div key={s.id} onClick={() => loadStudy(s)}
                  style={{ display: "flex", alignItems: "center", gap: 3, padding: "5px 6px", borderRadius: 5, marginBottom: 2, cursor: "pointer",
                    background: active ? th.activeBg : isStarred ? (darkMode ? "#1c1806" : "#fffbeb") : "transparent",
                    border: `1px solid ${isRunning ? "#60a5fa40" : active ? "#2563eb40" : isStarred ? "#f59e0b30" : "transparent"}` }}>
                  {/* Pin/star button */}
                  <button onClick={e => { e.stopPropagation(); toggleStarStudy(s.id); }}
                    title={isStarred ? "Unpin" : "Pin to top"}
                    style={{ border: "none", background: "none", cursor: "pointer", fontSize: 10, padding: 0, lineHeight: 1, flexShrink: 0,
                      color: isStarred ? "#f59e0b" : th.textFaint, opacity: isStarred ? 1 : 0.35 }}>
                    {isStarred ? "⭐" : "☆"}
                  </button>
                  <span style={{ flex: 1, fontSize: 11, fontWeight: active ? 600 : 400, color: active ? th.activeText : th.text, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{s.name}</span>
                  {modified && !isRunning && (
                    <span title="Unsaved changes" style={{ width: 6, height: 6, borderRadius: "50%", background: "#f59e0b", flexShrink: 0, display: "inline-block", boxShadow: "0 0 4px #f59e0b" }} />
                  )}
                  {runBadge && (
                    <span style={{ fontSize: 8, color: runBadge.color, fontWeight: 700, flexShrink: 0, whiteSpace: "nowrap" }}>{runBadge.label}</span>
                  )}
                  {!isRunning && (
                    <button onClick={e => { e.stopPropagation(); void doRun(s); }} title="Run study" style={{ ...bm, color: "#22c55e", borderColor: "#15803d40", background: "none", padding: "0 3px" }}>▶</button>
                  )}
                  <button onClick={e => { e.stopPropagation(); void dupStudy(s); }} title="Dup" style={{ ...bm, color: th.textMuted, borderColor: th.border }}>⥘</button>
                  <button onClick={e => void delStudy(s.id, e)} title={deleteConfirm === s.id ? "Confirm?" : "Delete"}
                    style={{ ...bm, color: deleteConfirm === s.id ? "#f87171" : th.textMuted, background: deleteConfirm === s.id ? "#450a0a" : "none", borderColor: th.border }}>
                    {deleteConfirm === s.id ? "!" : "×"}
                  </button>
                </div>
              );
            })}
          </div>

          {/* Inner drag divider — resize studies list vs palette */}
          <div
            onMouseDown={onInnerDivDown}
            title="Drag to resize"
            style={{ height: 5, cursor: "row-resize", flexShrink: 0, background: th.border,
              borderTop: `1px solid ${th.borderHov}`, transition: "background 0.1s" }}
            onMouseEnter={e => (e.currentTarget.style.background = th.borderHov)}
            onMouseLeave={e => (e.currentTarget.style.background = th.border)}
          />

          <div style={{ flex: 1, overflowY: "auto", minHeight: 0, padding: "7px 7px" }}>
            <div style={{ fontSize: 9, fontWeight: 700, color: th.textMuted, textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 5 }}>Palette</div>
            <input value={palSearch} onChange={e => setPalSearch(e.target.value)} placeholder="Search…"
              style={{ width: "100%", boxSizing: "border-box", padding: "5px 8px", fontSize: 11, border: `1px solid ${th.inputBdr}`, borderRadius: 5, marginBottom: 5, outline: "none", background: th.inputBg, color: th.inputText }} />
            <div style={{ display: "flex", gap: 2, marginBottom: 7, flexWrap: "wrap" }}>
              {(["all", "experiment", "pipeline", "special"] as const).map(f => (
                <button key={f} onClick={() => setPalFilter(f)} style={{ padding: "2px 7px", border: `1px solid ${palFilter === f ? "#475569" : th.border}`, borderRadius: 8, cursor: "pointer", fontSize: 9, background: palFilter === f ? (darkMode ? "#334155" : "#1e293b") : "transparent", color: palFilter === f ? "#e2e8f0" : th.textMuted }}>{f}</button>
              ))}
            </div>
            {(palFilter === "all" || palFilter === "special") && (
              <div style={{ marginBottom: 8 }}>
                <div style={{ fontSize: 9, fontWeight: 700, color: th.textMuted, textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 }}>Data &amp; Analysis</div>
                {SPECIAL_TYPES.map(nt => <PaletteItem key={nt} label={NODE_CFG[nt].defaultLabel} nodeType={nt} description={NODE_CFG[nt].description} refId="" onDragStart={onDragStart} />)}
              </div>
            )}
            {/* User graph experiments first (promoted to top) */}
            {fExps.filter(e => e.category === "Graph Experiments").length > 0 && (
              <div style={{ marginBottom: 8 }}>
                <div style={{ fontSize: 9, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 3 }}>User Experiments</div>
                <div style={{ fontSize: 8, color: th.textFaint, marginBottom: 4 }}>← created in Exp. Builder</div>
                {fExps.filter(e => e.category === "Graph Experiments").map(e => <PaletteItem key={e.id} label={e.name.replace(/^\ud83d\udd00 /, "")} nodeType="experiment" description={e.description} refId={e.id} onDragStart={onDragStart} />)}
              </div>
            )}
            {fExps.filter(e => e.category !== "Graph Experiments").length > 0 && (
              <div style={{ marginBottom: 8 }}>
                <div style={{ fontSize: 9, fontWeight: 700, color: "#6b7280", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 3 }}>Primitive Experiments</div>
                <div style={{ fontSize: 8, color: th.textFaint, marginBottom: 4 }}>Tip: wrap in Exp. Builder → promotes to User Experiment</div>
                {fExps.filter(e => e.category !== "Graph Experiments").map(e => <PaletteItem key={e.id} label={e.name} nodeType="experiment" description={e.description} refId={e.id} onDragStart={onDragStart} />)}
              </div>
            )}
            {fPipes.length > 0 && (
              <div style={{ marginTop: 4 }}>
                <div style={{ fontSize: 9, fontWeight: 700, color: "#2563eb", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 }}>Pipelines</div>
                {fPipes.map(p => <PaletteItem key={p.id} label={p.label ?? p.id} nodeType="pipeline" description={p.description ?? ""} refId={p.id} onDragStart={onDragStart} />)}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );

  const Divider = (
    <div onMouseDown={onDividerDown}
      style={{ width: 4, cursor: "col-resize", background: th.panelBg, flexShrink: 0, borderLeft: `1px solid ${th.border}`, transition: "border-color 0.1s" }}
      onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderLeftColor = th.borderHov; }}
      onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderLeftColor = th.border; }}
    />);

  const Right = !inspectorOff && selectedNode ? (
    <Inspector node={selectedNode} experiments={experiments} pipelines={pipelines} darkMode={darkMode}
      onClose={() => setInspectorOff(true)} onParamChange={onParamChange} />
  ) : null;

  const importStudyRef = useRef<HTMLInputElement>(null);
  const onImportStudy = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    try { const d = JSON.parse(await f.text()); const s = await createStudy({ name: d.name || f.name, description: d.description || "", graph: d.graph }); setStudies(prev => [s, ...prev]); loadStudy(s); }
    catch { alert("Invalid study file."); }
    e.target.value = "";
  }, [loadStudy]);

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0, overflow: "hidden" }}>
      {/* Toolbar — condensed, single row */}
      <div style={{ display: "flex", alignItems: "center", gap: 4, padding: "3px 8px", background: th.panelBg2, borderBottom: `1px solid ${th.border}`, flexShrink: 0 }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: th.text, marginRight: 2, flexShrink: 0 }}>Study Builder</span>
        {activeStudy && <span style={{ fontSize: 10, color: th.textMuted, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 180 }}>{activeStudy.name}</span>}
        {saveMsg && <span style={{ fontSize: 10, color: saveMsg === "Saved" ? "#22c55e" : "#ef4444", fontWeight: 600, flexShrink: 0 }}>{saveMsg}</span>}
        <div style={{ flex: 1 }} />
        <button onClick={async () => { if (!ragReady) { setRagBuilding(true); try { const r = await rebuildRagIndex(); setRagReady(r.ready); } finally { setRagBuilding(false); } } }}
          title={ragReady ? "RAG ready — click to rebuild" : "Build RAG index"}
          style={{ border: "1px solid", borderRadius: 4, padding: "2px 6px", cursor: "pointer", fontSize: 9, fontWeight: 600, background: "none",
            color: ragBuilding ? "#f59e0b" : ragReady ? "#22c55e" : th.textFaint, borderColor: ragBuilding ? "#f59e0b40" : ragReady ? "#22c55e30" : th.border }}>
          {ragBuilding ? "⏳" : ragReady ? "🔍✓" : "🔍"}
        </button>

        {/* AI dropdown */}
        <div style={{ position: "relative" }}>
          <button onClick={() => setAiMenuOpen(v => !v)} disabled={summarizing}
            title="AI tools" style={{ ...tBtn, padding: "3px 8px", fontSize: 10, cursor: summarizing ? "not-allowed" : "pointer", opacity: summarizing ? 0.5 : 1, color: th.textMuted, border: `1px solid ${th.border}` }}>
            {summarizing ? "⏳" : "✨ AI"} ▾
          </button>
          {aiMenuOpen && (
            <div style={{ position: "absolute", top: "100%", left: 0, zIndex: 9000, background: "#1e293b", border: "1px solid #334155", borderRadius: 7, minWidth: 150, padding: "3px 0", boxShadow: "0 8px 32px rgba(0,0,0,0.6)", marginTop: 2 }}
              onMouseLeave={() => setAiMenuOpen(false)}>
              {[
                { label: "✨ Summary", action: () => { setAiMenuOpen(false); void (async () => { setSummarizing(true); setSummary(null); try { setSummary(await summarizeStudy(activeStudy!.id)); } finally { setSummarizing(false); } })(); }, disabled: !activeStudy },
                { label: "✨ Design", action: () => { setAiMenuOpen(false); openChat({ contextType: activeStudy ? "study" : "", contextId: activeStudy?.id ?? "", initialPrompt: activeStudy ? `Help me improve "${activeStudy.name}".` : undefined }); }, disabled: false },
              ].map(({ label, action, disabled }) => (
                <button key={label} onClick={action} disabled={disabled}
                  style={{ display: "flex", alignItems: "center", gap: 7, width: "100%", padding: "6px 12px", border: "none", background: "none", color: disabled ? "#64748b" : "#e2e8f0", cursor: disabled ? "not-allowed" : "pointer", fontSize: 12 }}
                  onMouseEnter={e => { if (!disabled) (e.currentTarget as HTMLElement).style.background = "#334155"; }}
                  onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = "none"; }}>
                  {label}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Running status badge for active study */}
        {activeStudyRunning && activeStudy && (() => {
          const run = activeRuns[activeStudy.id];
          return (
            <span style={{ fontSize: 10, color: "#60a5fa", fontWeight: 600, flexShrink: 0, whiteSpace: "nowrap" }}>
              ⏳ {getElapsed(activeStudy.id)}s · {run?.currentNodeLabel.slice(0, 20) || "running…"} ({(run?.currentNodeIdx ?? 0) + 1}/{run?.totalNodes ?? "?"})
            </span>
          );
        })()}
        {hasActiveRuns && (
          <button onClick={stopAll} title="Stop all running studies"
            style={{ ...tBtn, padding: "3px 8px", fontSize: 10, color: "#ef4444", border: "1px solid #ef444430", cursor: "pointer" }}>
            ⏹ Stop All
          </button>
        )}
        {[
          { label: "↑ Import", title: "Import study from JSON", disabled: false, action: () => importStudyRef.current?.click() },
          { label: "↓ Export", title: "Export study as JSON", disabled: !activeStudy, action: exportStudy },
          { label: saving ? "…" : "💾 Save", title: "Save", disabled: saving || !activeStudy, action: () => void doSave() },
          { label: "⬦ Arrange", title: "Auto-arrange nodes", disabled: !activeStudy || nodes.length === 0, action: doArrange },
          { label: "↩ Revert", title: isDirty ? "Discard changes and revert to last saved" : "No unsaved changes", disabled: !isDirty || !activeStudy, action: doRevert, warn: true },
        ].map(({ label, title, disabled, action, warn }) => (
          <button key={label} onClick={action} disabled={disabled} title={title}
            style={{ ...tBtn, padding: "3px 8px", fontSize: 10, opacity: disabled ? 0.4 : 1, cursor: disabled ? "not-allowed" : "pointer", color: (warn as boolean | undefined) ? "#f59e0b" : th.textMuted, border: `1px solid ${(warn as boolean | undefined) ? "#f59e0b40" : th.border}` }}>
            {label}
          </button>
        ))}
        <input ref={importStudyRef} type="file" accept=".json" style={{ display: "none" }} onChange={onImportStudy} />
      </div>

      {/* Main canvas area */}
      <div style={{ flex: 1, display: "flex", minHeight: 0, flexDirection: dockL ? "row" : "row-reverse", position: "relative" }}>
        {LeftPanel}
        {!leftOff && Divider}

        <div ref={reactFlowWrapper} style={{ flex: 1, minWidth: 0, background: th.canvasBg }}
          onDrop={onDrop} onDragOver={onDragOver}
          onContextMenu={onPaneCtxMenu}>
          {/* No-study overlay */}
          {!activeStudy && (
            <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", gap: 10, zIndex: 5, pointerEvents: "none" }}>
              <div style={{ fontSize: 40 }}>📐</div>
              <div style={{ fontSize: 14, color: th.textMuted, fontWeight: 600 }}>Select or create a study to start</div>
              <div style={{ fontSize: 11, color: th.textFaint }}>Use the panel on the left</div>
            </div>
          )}
          {/* Empty canvas hint */}
          {activeStudy && nodes.length === 0 && (
            <div style={{ position: "absolute", bottom: 24, left: "50%", transform: "translateX(-50%)", zIndex: 5, pointerEvents: "none",
              background: th.panelBg2, border: `1px solid ${th.border}`, borderRadius: 8, padding: "8px 16px",
              fontSize: 12, color: th.textMuted, textAlign: "center", whiteSpace: "nowrap",
              boxShadow: "0 2px 12px rgba(0,0,0,0.15)" }}>
              Drag from palette · Right-click canvas to add nodes
            </div>
          )}

          {/* Floating run/stop button — top-center of canvas */}
          {activeStudy && nodes.length > 0 && (
            <div style={{ position: "absolute", top: 12, left: "50%", transform: "translateX(-50%)", zIndex: 20 }}>
              {activeStudyRunning ? (
                <button onClick={() => activeRuns[activeStudy.id]?.controller.abort()}
                  title="Stop this study run"
                  style={{ padding: "6px 16px", border: "2px solid #ef4444", borderRadius: 20, background: "rgba(69,10,10,0.9)", color: "#f87171", cursor: "pointer", fontSize: 12, fontWeight: 700, boxShadow: "0 2px 12px rgba(0,0,0,0.5)", whiteSpace: "nowrap", backdropFilter: "blur(4px)" }}>
                  ⏹ Stop
                </button>
              ) : (
                <button onClick={() => void doRun(activeStudy)}
                  title="Run this study"
                  style={{ padding: "6px 18px", border: "none", borderRadius: 20, background: "linear-gradient(135deg,#16a34a,#22c55e)", color: "#fff", cursor: "pointer", fontSize: 12, fontWeight: 700, boxShadow: "0 2px 12px rgba(0,0,0,0.4)", whiteSpace: "nowrap" }}>
                  ▶ Run Study
                </button>
              )}
            </div>
          )}
          <ReactFlow
            nodes={nodes} edges={animEdges}
            nodeTypes={GLOSSA_NODE_TYPES}
            onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick} onPaneClick={onPaneClick}
            onNodeContextMenu={onNodeCtx}
            onEdgeContextMenu={onEdgeCtx}
            onReconnectStart={onReconnectStart}
            onReconnect={onReconnect}
            onReconnectEnd={onReconnectEnd}
            snapToGrid snapGrid={[15, 15]}
            deleteKeyCode={["Backspace", "Delete"]}
            fitView fitViewOptions={{ padding: 0.2 }}
            minZoom={0.15} maxZoom={2.5}
            proOptions={{ hideAttribution: true }}
            style={{ background: th.canvasBg }}
            defaultEdgeOptions={{ reconnectable: true, style: { stroke: th.edgeDef, strokeWidth: 2 } }}
          >
            <Controls style={{ background: darkMode ? "#1e293b" : "#ffffff", border: `1px solid ${th.border}` }} />
            <MiniMap style={{ background: th.canvasBg }} nodeColor={n => NODE_CFG[(n.data as NodeData)?.nodeType]?.color ?? "#334155"} />
            <Background variant={BackgroundVariant.Dots} gap={15} size={1} color={th.canvasGrid} />
            <AutoFitView trigger={fitTrigger} />
          </ReactFlow>
        </div>

        {Right}
        {selectedNode && inspectorOff && (
          <button onClick={() => setInspectorOff(false)}
            style={{ position: "absolute", right: 6, top: "50%", transform: "translateY(-50%)", border: "1px solid #334155", background: "#1e293b", color: "#64748b", cursor: "pointer", borderRadius: 4, padding: "6px 4px", fontSize: 12, zIndex: 100 }}>◀</button>
        )}
      </div>

      {/* Below-canvas panels — theme-aware, capped height to avoid pushing canvas */}
      <div style={{ flexShrink: 0, maxHeight: 220, overflow: "auto", background: th.panelBg }}>
        {runError && <div style={{ margin: "5px 0", padding: "7px 12px", background: "#450a0a", border: "1px solid #7f1d1d", borderRadius: 5, fontSize: 12, color: "#fca5a5" }}>{runError}</div>}

        {runResult && (
          <div style={{ background: th.panelBg, border: `1px solid ${th.border}`, borderRadius: 6, overflow: "hidden", marginTop: 4 }}>
            <div style={{ background: th.panelBg2, padding: "6px 12px", display: "flex", gap: 8, alignItems: "center", borderBottom: `1px solid ${th.border}` }}>
              <span style={{ fontSize: 11, fontWeight: 700, color: "#22c55e" }}>Run Results</span>
              <span style={{ fontSize: 10, color: th.textMuted }}>{runResult.completed} complete · {runResult.skipped} skipped · {runResult.annotations ?? 0} annotations · {runResult.errors} errors</span>
              <div style={{ flex: 1 }} />
              {/* Quick navigation to Reports tab */}
              <button
                onClick={() => window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "reports" } }))}
                title="Open Reports tab to view, compose and export PDF"
                style={{ padding: "2px 8px", border: `1px solid ${th.border}`, borderRadius: 4, background: "none", cursor: "pointer", fontSize: 10, color: th.textMuted, whiteSpace: "nowrap" }}>
                📄 View Reports
              </button>
              <button onClick={() => setRunResult(null)} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 11, color: th.textFaint }}>× dismiss</button>
            </div>
            <div style={{ overflowX: "auto", maxHeight: 160, overflowY: "auto" }}>
              {Object.entries(runResult.results).map(([nid, res]) => {
                const sc = ({ complete: "#22c55e", error: "#ef4444", skipped: "#f59e0b", annotation: "#64748b", corpus: "#059669", pending: "#f59e0b" } as Record<string, string>)[res.status] ?? "#64748b";
                const lbl = nodes.find(n => n.id === nid)?.data?.label as string | undefined;
                return (
                  <div key={nid} style={{ display: "flex", gap: 8, padding: "6px 12px", borderBottom: `1px solid ${th.border}`, alignItems: "flex-start" }}>
                    <span style={{ fontSize: 9, padding: "1px 6px", borderRadius: 6, background: sc + "20", color: sc, fontWeight: 700, whiteSpace: "nowrap", marginTop: 1 }}>{res.status}</span>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: 11, fontWeight: 500, color: th.text }}>{lbl ?? nid}</div>
                      {res.reason && <div style={{ fontSize: 10, color: th.textMuted }}>{res.reason}</div>}
                      {res.status === "complete" && res.result && (
                        <pre style={{ background: darkMode ? "#1e293b" : "#f1f5f9", color: th.textMuted, margin: "3px 0 0", padding: "4px 8px", fontSize: 9, borderRadius: 3, maxHeight: 70, overflowY: "auto" }}>
                          {JSON.stringify(res.result, null, 2).slice(0, 400)}
                        </pre>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {summary && <StudySummaryPanel summary={summary} onClose={() => setSummary(null)} />}
      </div>

      {/* Context menu */}
      {ctxMenu && (
        <ContextMenu x={ctxMenu.x} y={ctxMenu.y} onClose={() => setCtxMenu(null)}
          items={ctxMenu.type === "node" && ctxMenu.nodeId ? nodeCtxItems(ctxMenu.nodeId) : ctxMenu.type === "edge" && ctxMenu.edgeId ? edgeCtxItems(ctxMenu.edgeId) : paneCtxItems(ctxMenu.x, ctxMenu.y)} />
      )}

      {showNewStudy && (
        <NewStudyDialog onClose={() => setShowNewStudy(false)} onCreated={s => { setStudies(prev => [s, ...prev]); loadStudy(s); }} />
      )}

      {/* CSS animations for running nodes */}
      <style>{`
        @keyframes glossaNodePulse {
          0%, 100% { box-shadow: 0 0 0 3px rgba(96,165,250,0.35), 0 4px 24px rgba(96,165,250,0.3); }
          50%       { box-shadow: 0 0 0 5px rgba(96,165,250,0.6),  0 4px 32px rgba(96,165,250,0.55); }
        }
        .glossa-node-running { animation: glossaNodePulse 1s ease-in-out infinite; }
      `}</style>
    </div>
  );
}

// ── Shared styles ─────────────────────────────────────────────────────

// These are module-level fallbacks — actual values are derived from th in the component
const tBtn: React.CSSProperties = { padding: "4px 10px", border: "1px solid #334155", borderRadius: 5, cursor: "pointer", fontSize: 11, fontWeight: 600, background: "transparent", color: "#94a3b8" };
const bm:   React.CSSProperties = { border: "1px solid #334155", borderRadius: 3, background: "none", color: "#94a3b8", cursor: "pointer", fontSize: 10, padding: "0 4px", lineHeight: "18px" };
