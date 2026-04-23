/**
 * Experiment Builder — ComfyUI-like visual composer for custom experiments.
 *
 * Users wire typed atomic computation nodes (CorpusReader → FreqCounter →
 * PositionalProfiler → JSONExport …) with coloured typed ports.  The resulting
 * graph is saved as a GraphExperiment that appears in the Study Builder palette.
 *
 * Port type colours (matches backend PORT_COLORS):
 *   sequences  #059669   freq_map  #2563eb   profiles  #7c3aed
 *   clusters   #d97706   number    #dc2626   text      #0d9488
 *   json       #4f46e5   any       #64748b
 */

import React, {
  useCallback, useEffect, useMemo, useRef, useState,
} from "react";
import { autoArrange as autoArrangeNodes } from "../utils/autoArrange";
import { runGraphExperimentStream } from "../api";
import { CorpusSelector } from "./CorpusSelector";
import {
  ReactFlow,
  addEdge,
  Background, BackgroundVariant,
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

import {
  getAtomicNodeCatalog,
  listGraphExperiments,
  getGraphExperiment,
  createGraphExperiment,
  updateGraphExperiment,
  deleteGraphExperiment,
  PORT_COLORS,
  type AtomicNodeDef,
  type AtomicPort,
  type GraphExperiment,
  type GraphExperimentMeta,
} from "../api";

// ── Theme (same helper as StudyBuilderView) ─────────────────────────────────

function ebTheme(dark: boolean) {
  return {
    panelBg:   dark ? "#0f172a" : "#f8fafc",
    panelBg2:  dark ? "#1e293b" : "#ffffff",
    text:      dark ? "#e2e8f0" : "#1e293b",
    textMuted: dark ? "#94a3b8" : "#64748b",
    textFaint: dark ? "#64748b" : "#94a3b8",
    border:    dark ? "#1e293b" : "#e2e8f0",
    borderHov: dark ? "#334155" : "#cbd5e1",
    activeBg:  dark ? "#1e3a5f" : "#dbeafe",
    activeText:dark ? "#ffffff" : "#1e40af",
    inputBg:   dark ? "#0f172a" : "#ffffff",
    inputText: dark ? "#e2e8f0" : "#1e293b",
    inputBdr:  dark ? "#334155" : "#d1d5db",
    canvasBg:  dark ? "#080d18" : "#f1f5f9",
    canvasGrid:dark ? "#161e2e" : "#e2e8f0",
  };
}

const PORT_CLR = PORT_COLORS;

// ── Layout constants (shared by ExpNode and auto-arrange) ─────────────────────
const PORT_ROW_H = 22;  // px — height of each input/output port row
const HEADER_H   = 26;  // px — height of the title bar

// (autoArrange is imported from ../utils/autoArrange)

// ── ExpNode — ComfyUI-style node with per-row port handles ───────────────────

interface ExpNodeData extends Record<string, unknown> {
  atomicId: string;
  label: string;
  inputs:  AtomicPort[];
  outputs: AtomicPort[];
  params: Record<string, unknown>;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  params_schema: Record<string, any>;
  runStatus?: "idle" | "running" | "complete" | "error";
  runResult?: string;
}

const ExpNode = ({ data, id, selected }: NodeProps) => {
  const nd = data as ExpNodeData;
  const { setNodes, setEdges } = useReactFlow();

  const isDark     = (nd as Record<string, unknown>).darkMode !== false;
  const nodeBg     = isDark ? "#111827" : "#ffffff";
  const portBg     = isDark ? "#0d1424" : "#f8fafc";
  const portRowBdr = isDark ? "#1a2535" : "#e8edf2";
  const paramBg    = isDark ? "#0a1020" : "#f1f5f9";
  const paramLbl   = isDark ? "#475569" : "#9ca3af";
  const paramVal   = isDark ? "#94a3b8" : "#64748b";
  const runStatus  = nd.runStatus;
  const runClrMap: Record<string, string> = { complete: "#22c55e", error: "#ef4444", running: "#60a5fa" };
  const runClr     = runStatus ? (runClrMap[runStatus] ?? "") : "";
  const headerColor = (nd.outputs?.[0] ? PORT_CLR[nd.outputs[0].type] : null) ?? "#334155";
  const shadow = isDark
    ? (selected ? "0 0 0 2px #60a5fa40, 0 4px 20px rgba(0,0,0,0.6)" : "0 2px 14px rgba(0,0,0,0.5)")
    : (selected ? "0 0 0 2px #60a5fa60, 0 4px 12px rgba(0,0,0,0.15)" : "0 1px 6px rgba(0,0,0,0.12)");

  const maxRows  = Math.max(nd.inputs.length, nd.outputs.length);
  const paramEntries = Object.entries(nd.params_schema?.properties ?? {});

  const onDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    setNodes(n => n.filter(node => node.id !== id));
    setEdges(ed => ed.filter(edge => edge.source !== id && edge.target !== id));
  };

  return (
    <div
      data-testid="exp-node"
      style={{
        background: nodeBg,
        border: `2px solid ${selected ? "#60a5fa" : headerColor + "66"}`,
        borderRadius: 8,
        minWidth: 220, maxWidth: 280,
        boxShadow: shadow,
        fontFamily: "system-ui, sans-serif",
        overflow: "visible",
      }}
    >
      {/* ── Title bar ── */}
      <div
        data-testid="exp-node-header"
        style={{
          background: headerColor,
          borderRadius: "6px 6px 0 0",
          height: HEADER_H,
          padding: "0 8px",
          display: "flex", alignItems: "center", gap: 5,
        }}
      >
        <span style={{
          color: "#fff", fontSize: 11, fontWeight: 700, flex: 1,
          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
          textShadow: "0 1px 2px rgba(0,0,0,0.4)",
        }}>
          {nd.label}
        </span>
        {runStatus && runStatus !== "idle" && (
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: runClr, flexShrink: 0,
            display: "inline-block", boxShadow: `0 0 4px ${runClr}` }} />
        )}
        <button
          onMouseDown={onDelete}
          data-testid="exp-node-delete"
          style={{ border: "none", background: "rgba(0,0,0,0.3)", color: "#fff",
            cursor: "pointer", fontSize: 12, lineHeight: 1, borderRadius: 3, padding: "1px 4px", flexShrink: 0 }}
        >×</button>
      </div>

      {/* ── Port rows: inputs (left) + outputs (right), zipper pattern ── */}
      {maxRows > 0 && (
        <div
          data-testid="exp-node-ports"
          style={{ background: portBg, borderBottom: maxRows > 0 ? `1px solid ${portRowBdr}` : undefined }}
        >
          {Array.from({ length: maxRows }, (_, i) => {
            const inp = nd.inputs[i];
            const out = nd.outputs[i];
            return (
              <div
                key={i}
                style={{
                  display: "flex", alignItems: "center",
                  height: PORT_ROW_H,
                  borderBottom: i < maxRows - 1 ? `1px solid ${portRowBdr}` : undefined,
                }}
              >
                {/* Input port label + visual square */}
                <div style={{ flex: 1, display: "flex", alignItems: "center", gap: 4, paddingLeft: 10, minWidth: 0 }}>
                  {inp && (
                    <>
                      <span
                        data-testid="port-square-in"
                        style={{
                          width: 7, height: 7, borderRadius: 2, flexShrink: 0,
                          background: PORT_CLR[inp.type] ?? PORT_CLR.any,
                          border: "1.5px solid rgba(0,0,0,0.35)",
                        }}
                      />
                      <span style={{
                        fontSize: 9.5, color: PORT_CLR[inp.type] ?? PORT_CLR.any,
                        whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
                        fontWeight: 500,
                      }}>{inp.name}</span>
                    </>
                  )}
                </div>

                {/* Output port label + visual square */}
                <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "flex-end", gap: 4, paddingRight: 10, minWidth: 0 }}>
                  {out && (
                    <>
                      <span style={{
                        fontSize: 9.5, color: PORT_CLR[out.type] ?? PORT_CLR.any,
                        whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
                        fontWeight: 500, textAlign: "right",
                      }}>{out.name}</span>
                      <span
                        data-testid="port-square-out"
                        style={{
                          width: 7, height: 7, borderRadius: 2, flexShrink: 0,
                          background: PORT_CLR[out.type] ?? PORT_CLR.any,
                          border: "1.5px solid rgba(0,0,0,0.35)",
                        }}
                      />
                    </>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* ── Params section ── */}
      {paramEntries.length > 0 && (
        <div
          data-testid="exp-node-params"
          style={{ background: paramBg, borderRadius: "0 0 6px 6px", padding: "4px 8px" }}
        >
          {Object.entries(nd.params)
            .filter(([, v]) => v !== "" && v !== undefined)
            .map(([k, v]) => (
              <div key={k} style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 1 }}>
                <span style={{ fontSize: 9, color: paramLbl, flexShrink: 0, marginRight: 4 }}>{k}</span>
                <span style={{ fontSize: 9, color: paramVal, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 130 }}>
                  {String(v).slice(0, 28)}
                </span>
              </div>
            ))
          }
          {runStatus === "complete" && nd.runResult && (
            <div style={{ fontSize: 9, color: "#22c55e", marginTop: 2 }}>✓ {nd.runResult.slice(0, 40)}</div>
          )}
        </div>
      )}
      {paramEntries.length === 0 && runStatus === "complete" && nd.runResult && (
        <div style={{ padding: "2px 8px 4px", borderRadius: "0 0 6px 6px", fontSize: 9, color: "#22c55e" }}>
          ✓ {nd.runResult.slice(0, 40)}
        </div>
      )}

      {/* ── React Flow Handles — positioned at row centres ── */}
      {nd.inputs.map((p, i) => (
        <Handle
          key={`in_${p.name}`}
          type="target"
          position={Position.Left}
          id={`in__${p.name}`}
          style={{
            width: 10, height: 10,
            background: PORT_CLR[p.type] ?? PORT_CLR.any,
            border: "2px solid rgba(0,0,0,0.5)",
            borderRadius: 3,
            left: -6,
            top: HEADER_H + (i + 0.5) * PORT_ROW_H,
            transform: "translateY(-50%)",
            position: "absolute",
          }}
          title={`${p.name} : ${p.type}${p.required ? " (required)" : ""}`}
        />
      ))}
      {nd.outputs.map((p, i) => (
        <Handle
          key={`out_${p.name}`}
          type="source"
          position={Position.Right}
          id={`out__${p.name}`}
          style={{
            width: 10, height: 10,
            background: PORT_CLR[p.type] ?? PORT_CLR.any,
            border: "2px solid rgba(0,0,0,0.5)",
            borderRadius: 3,
            right: -6,
            top: HEADER_H + (i + 0.5) * PORT_ROW_H,
            transform: "translateY(-50%)",
            position: "absolute",
          }}
          title={`${p.name} : ${p.type}`}
        />
      ))}
    </div>
  );
};

const EXP_NODE_TYPES = { expNode: ExpNode };

// Helper rendered inside ReactFlow to call fitView programmatically
function AutoFitView({ trigger }: { trigger: number }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    if (trigger > 0) setTimeout(() => fitView({ padding: 0.2 }), 80);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [trigger]);
  return null;
}

// ── Context menu ─────────────────────────────────────────────────────────────

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
    <div ref={ref} style={{ position: "fixed", left, top, background: "#1e293b", border: "1px solid #334155", borderRadius: 7, zIndex: 99999, minWidth: 172, padding: "3px 0", boxShadow: "0 8px 32px rgba(0,0,0,0.6)" }}>
      {items.map((it, i) =>
        it.divider ? <div key={i} style={{ height: 1, background: "#334155", margin: "3px 0" }} /> : (
          <button key={i} onClick={() => { it.action?.(); onClose(); }}
            style={{ display: "flex", alignItems: "center", gap: 7, width: "100%", padding: "6px 12px", border: "none", background: "none", color: it.danger ? "#f87171" : "#e2e8f0", cursor: "pointer", fontSize: 12 }}
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

// ── New Experiment Dialog ─────────────────────────────────────────────────────

function NewExpDialog({ onClose, onCreate }: { onClose: () => void; onCreate: (name: string, desc: string) => void }) {
  const [name, setName] = useState(""); const [desc, setDesc] = useState("");
  const bdRef = useRef<HTMLDivElement>(null);
  const inp: React.CSSProperties = { display: "block", width: "100%", boxSizing: "border-box", padding: "7px 10px", border: "1px solid #334155", borderRadius: 6, fontSize: 13, marginBottom: 10, outline: "none", background: "#0f172a", color: "#e2e8f0" };
  return (
    <div ref={bdRef} onClick={e => { if (e.target === bdRef.current) onClose(); }}
      style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.65)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 10000 }}>
      <div style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 10, padding: "1.5rem", width: 440, maxWidth: "95vw", boxShadow: "0 20px 60px rgba(0,0,0,0.6)" }}>
        <h3 style={{ margin: "0 0 1rem", color: "#e2e8f0", fontSize: 15 }}>New Graph Experiment</h3>
        <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: "#64748b", marginBottom: 4 }}>Name *</label>
        <input autoFocus value={name} onChange={e => setName(e.target.value)} onKeyDown={e => { if (e.key === "Enter" && name.trim()) { onCreate(name.trim(), desc.trim()); onClose(); }}} placeholder="e.g. Indus Symbol Analysis" style={inp} />
        <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: "#64748b", marginBottom: 4 }}>Description (optional)</label>
        <textarea value={desc} onChange={e => setDesc(e.target.value)} rows={2} placeholder="What does this experiment compute?" style={{ ...inp, resize: "vertical", fontFamily: "inherit" }} />
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <button onClick={onClose} style={{ padding: "7px 16px", border: "1px solid #334155", borderRadius: 6, cursor: "pointer", fontSize: 12, background: "none", color: "#64748b" }}>Cancel</button>
          <button onClick={() => { if (name.trim()) { onCreate(name.trim(), desc.trim()); onClose(); }}} disabled={!name.trim()}
            style={{ padding: "7px 18px", border: "none", borderRadius: 6, cursor: name.trim() ? "pointer" : "not-allowed", fontSize: 12, fontWeight: 600, background: "#7c3aed", color: "#fff", opacity: name.trim() ? 1 : 0.4 }}>
            Create
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Inspector ─────────────────────────────────────────────────────────────────

function Inspector({ node, onClose, onParamChange, darkMode = true }: {
  node: Node<ExpNodeData> | null;
  onClose: () => void;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onParamChange: (nodeId: string, params: Record<string, any>) => void;
  darkMode?: boolean;
}) {
  if (!node) return null;
  const nd = node.data;
  const headerColor = (nd.outputs?.[0] ? PORT_CLR[nd.outputs[0].type] : null) ?? "#334155";
  const schema = nd.params_schema?.properties ?? {};
  const params = nd.params ?? {};
  const iBg    = darkMode ? "#0f172a" : "#f8fafc";
  const iBdr   = darkMode ? "#1e293b" : "#e2e8f0";
  const iText  = darkMode ? "#e2e8f0" : "#1e293b";
  const iMuted = darkMode ? "#64748b" : "#9ca3af";
  const iInpBg = darkMode ? "#1e293b" : "#ffffff";
  const iInpClr= darkMode ? "#e2e8f0" : "#1e293b";
  const iInpBdr= darkMode ? "#334155" : "#d1d5db";

  return (
    <div style={{ width: 240, borderLeft: `1px solid ${iBdr}`, padding: "11px 12px", background: iBg, overflowY: "auto", flexShrink: 0 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
        <span style={{ fontSize: 12, fontWeight: 700, color: headerColor }}>{nd.label}</span>
        <button onClick={onClose} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 14, color: iMuted }}>✕</button>
      </div>

      {/* Port legend */}
      <div style={{ marginBottom: 10, display: "flex", gap: 8, flexWrap: "wrap" }}>
        {nd.inputs.map(p => (
          <span key={p.name} style={{ fontSize: 9, display: "flex", alignItems: "center", gap: 3, color: PORT_CLR[p.type] ?? PORT_CLR.any }}>
            <span style={{ width: 6, height: 6, borderRadius: "50%", background: PORT_CLR[p.type] ?? PORT_CLR.any, display: "inline-block" }} />
            IN:{p.name}
          </span>
        ))}
        {nd.outputs.map(p => (
          <span key={p.name} style={{ fontSize: 9, display: "flex", alignItems: "center", gap: 3, color: PORT_CLR[p.type] ?? PORT_CLR.any }}>
            OUT:{p.name}
            <span style={{ width: 6, height: 6, borderRadius: "50%", background: PORT_CLR[p.type] ?? PORT_CLR.any, display: "inline-block" }} />
          </span>
        ))}
      </div>

      {/* Params */}
      {Object.keys(schema).length > 0 ? (
        <div>
          <div style={{ fontSize: 9, fontWeight: 700, color: iMuted, textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8, borderTop: `1px solid ${iBdr}`, paddingTop: 8 }}>Parameters</div>
          {Object.entries(schema).map(([k, def]) => {
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            const d = def as Record<string, any>;
            const type = d.type as string;
            const label = (d.title as string) ?? k;
            const iStyle: React.CSSProperties = { width: "100%", boxSizing: "border-box", padding: "4px 7px",
              border: `1px solid ${iInpBdr}`, borderRadius: 4, fontSize: 11, outline: "none",
              background: iInpBg, color: iInpClr };
            return (
              <div key={k} style={{ marginBottom: 9 }}>
                <div style={{ fontSize: 11, fontWeight: 600, color: iText, marginBottom: 2 }}>{label}</div>
                {d.description && <div style={{ fontSize: 10, color: iMuted, marginBottom: 3 }}>{d.description as string}</div>}
                {k === "corpus_id"
                  ? <CorpusSelector value={(params[k] as string) ?? ""} onChange={v => onParamChange(node.id, { ...params, [k]: v })} darkMode={darkMode} />
                  : type === "boolean"
                    ? <input type="checkbox" checked={!!(params[k])} onChange={e => onParamChange(node.id, { ...params, [k]: e.target.checked })} />
                    : type === "integer" || type === "number"
                      ? <input type="number" value={(params[k] as number) ?? (d.default as number) ?? ""} step={type === "integer" ? 1 : "any"} min={d.minimum as number | undefined} onChange={e => onParamChange(node.id, { ...params, [k]: (type === "integer" ? parseInt(e.target.value, 10) : parseFloat(e.target.value)) || 0 })} style={iStyle} />
                      : <input type="text" value={(params[k] as string) ?? (d.default as string) ?? ""} onChange={e => onParamChange(node.id, { ...params, [k]: e.target.value })} placeholder={(d.default as string) ?? ""} style={iStyle} />
                }
              </div>
            );
          })}
          <div style={{ fontSize: 9, color: iMuted }}>Saved with experiment.</div>
        </div>
      ) : (
        <div style={{ fontSize: 10, color: iMuted, fontStyle: "italic", marginTop: 6 }}>No parameters for this node.</div>
      )}
    </div>
  );
}

/** Format seconds as M:SS or H:MM:SS */
function fmtHMS(s: number): string {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = Math.floor(s % 60);
  if (h > 0) return `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
  return `${m}:${String(sec).padStart(2, "0")}`;
}

// ── Module-level exp-run store — survives component remounts / navigation ──────────
// Kept outside the component so state is never lost when the user navigates away.
type _ER = { controller: AbortController; startTime: number; currentLabel: string; idx: number; total: number; expId: string };
type _ERM = Record<string, _ER>;
const _erStore = { runs: {} as _ERM, cbs: new Set<(r: _ERM) => void>() };
function _erSet(fn: (prev: _ERM) => _ERM) { _erStore.runs = fn(_erStore.runs); _erStore.cbs.forEach(c => c(_erStore.runs)); }
function _erSub(cb: (r: _ERM) => void): () => void { _erStore.cbs.add(cb); return () => _erStore.cbs.delete(cb); }

// ── Main ExperimentBuilderView ─────────────────────────────────────────────

let _eid = 0;
function nextId() { return `en_${Date.now()}_${_eid++}`; }

export function ExperimentBuilderView({ darkMode = true }: { darkMode?: boolean }) {
  const th = ebTheme(darkMode);

  // Data
  const [catalog, setCatalog]     = useState<AtomicNodeDef[]>([]);
  const [savedExps, setSavedExps] = useState<GraphExperimentMeta[]>([]);
  const [activeExp, setActiveExp] = useState<GraphExperiment | null>(null);

  // Graph
  const [nodes, setNodes] = useState<Node<ExpNodeData>[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedNode, setSelectedNode] = useState<Node<ExpNodeData> | null>(null);
  const [inspectorOff, setInspectorOff] = useState(false);

  // UI
  const [saving, setSaving]     = useState(false);
  const [saveMsg, setSaveMsg]   = useState<string | null>(null);
  const [runResult, setRunResult] = useState<string | null>(null);

  // Per-experiment run result cache — persisted across navigation (mirrors StudyBuilderView)
  type ExpRunCacheEntry = { status: "success" | "fail"; ts: number };
  const [expRunCache, setExpRunCache] = useState<Record<string, ExpRunCacheEntry>>(() => {
    try { return JSON.parse(localStorage.getItem("geb_run_cache") ?? "{}") as Record<string, ExpRunCacheEntry>; }
    catch { return {}; }
  });
  const saveToExpRunCache = useCallback((expId: string, status: "success" | "fail") => {
    setExpRunCache(prev => {
      const next = { ...prev, [expId]: { status, ts: Date.now() } };
      localStorage.setItem("geb_run_cache", JSON.stringify(next));
      return next;
    });
  }, []);
  const [showNew, setShowNew]   = useState(false);
  const [palSearch, setPalSearch] = useState("");
  const [ctxMenu, setCtxMenu]   = useState<{ x: number; y: number; type: "pane" | "node"; nodeId?: string } | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [fitTrigger, setFitTrigger] = useState(0);

  // ── Active runs — backed by the module-level store (survives navigation) ──────────
  type ExpRun = _ER;
  const [activeRuns, setActiveRunsLocal] = useState<_ERM>(() => _erStore.runs);
  // Subscribe to store updates so any run started before/after navigation is reflected
  useEffect(() => _erSub(r => setActiveRunsLocal(r)), []);
  const [, setTick] = useState(0);
  const hasActiveRuns = Object.keys(activeRuns).length > 0;
  useEffect(() => {
    if (!hasActiveRuns) return;
    const t = setInterval(() => setTick(n => n + 1), 1000);
    return () => clearInterval(t);
  }, [hasActiveRuns]);

  // Helpers: check / iterate runs per experiment
  const getExpRuns   = useCallback((expId: string) => Object.values(activeRuns).filter(r => r.expId === expId), [activeRuns]);
  const isExpRunning = useCallback((expId: string) => Object.values(activeRuns).some(r => r.expId === expId), [activeRuns]);
  const getElapsed   = (run: ExpRun | undefined) => {
    if (!run) return 0;
    return Math.floor((Date.now() - run.startTime) / 1000);
  };

  // ── Undo / Redo history ────────────────────────────────────────────────────
  type HistorySnap = { nodes: Node<ExpNodeData>[]; edges: Edge[] };
  const historyRef       = useRef<HistorySnap[]>([]);
  const historyIdxRef    = useRef(-1);
  const isRestoringRef   = useRef(false);
  const isDraggingNodeRef = useRef(false);
  const historyTimerRef  = useRef<ReturnType<typeof setTimeout> | null>(null);

  const pushHistory = useCallback((ns: Node<ExpNodeData>[], es: Edge[]) => {
    if (isRestoringRef.current) return;
    const snap: HistorySnap = { nodes: ns.map(n => ({ ...n })), edges: es.map(e => ({ ...e })) };
    const trimmed = historyRef.current.slice(0, historyIdxRef.current + 1);
    trimmed.push(snap);
    if (trimmed.length > 150) trimmed.shift();
    historyRef.current = trimmed;
    historyIdxRef.current = trimmed.length - 1;
  }, []);

  const undo = useCallback(() => {
    if (historyIdxRef.current <= 0) return;
    isRestoringRef.current = true;
    historyIdxRef.current -= 1;
    const snap = historyRef.current[historyIdxRef.current];
    if (snap) { setNodes(snap.nodes); setEdges(snap.edges); }
    requestAnimationFrame(() => { isRestoringRef.current = false; });
  }, []);

  const redo = useCallback(() => {
    if (historyIdxRef.current >= historyRef.current.length - 1) return;
    isRestoringRef.current = true;
    historyIdxRef.current += 1;
    const snap = historyRef.current[historyIdxRef.current];
    if (snap) { setNodes(snap.nodes); setEdges(snap.edges); }
    requestAnimationFrame(() => { isRestoringRef.current = false; });
  }, []);

  const canUndo = historyIdxRef.current > 0;
  const canRedo = historyIdxRef.current < historyRef.current.length - 1;

  // Panel layout — outer left-panel width + inner experiments/palette split
  const [leftW,   setLeftW]   = useState<number>(() => parseInt(localStorage.getItem("geb_lw")  ?? "250", 10));
  const [expsH,   setExpsH]   = useState<number>(() => parseInt(localStorage.getItem("geb_exh") ?? "180", 10));
  const [leftOff, setLeftOff] = useState(false);
  const [dockL,   setDockL]   = useState<boolean>(() => localStorage.getItem("geb_dock") !== "right");
  const isDragging    = useRef(false);
  const dragStart     = useRef(0);
  const dragW0        = useRef(leftW);
  const innerDivStart = useRef(0);
  const innerDivH0    = useRef(expsH);

  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const draggedNodeType  = useRef<string | null>(null);

  // pendingAction: parsed from localStorage on mount.
  // Execution is deferred until AFTER loadExp is defined and catalog is populated.
  const [pendingAction, setPendingAction] = useState<{ action: string; id?: string } | null>(null);

  useEffect(() => {
    void getAtomicNodeCatalog().then(setCatalog).catch(() => {});
    void listGraphExperiments().then(setSavedExps).catch(() => {});
  }, []);
  useEffect(() => { localStorage.setItem("geb_lw",   String(leftW)); }, [leftW]);
  useEffect(() => { localStorage.setItem("geb_exh",  String(expsH)); }, [expsH]);
  useEffect(() => { localStorage.setItem("geb_dock", dockL ? "left" : "right"); }, [dockL]);

  // Debounced history push — fires after any nodes/edges change that isn't drag-in-progress or a restore
  useEffect(() => {
    if (isRestoringRef.current || isDraggingNodeRef.current) return;
    if (historyTimerRef.current) clearTimeout(historyTimerRef.current);
    historyTimerRef.current = setTimeout(() => pushHistory(nodes, edges), 120);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [nodes, edges]);

  // Keyboard Ctrl+Z / Ctrl+Y / Ctrl+Shift+Z for undo/redo
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName?.toLowerCase();
      if (tag === "input" || tag === "textarea") return;
      if (e.ctrlKey || e.metaKey) {
        if (e.key === "z" && !e.shiftKey) { e.preventDefault(); undo(); }
        if (e.key === "y" || (e.key === "z" && e.shiftKey)) { e.preventDefault(); redo(); }
      }
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [undo, redo]);

  // Parse pending action from localStorage ONCE on mount.
  // "new" is immediate; "load"/"dup" wait for catalog (handled after loadExp below).
  useEffect(() => {
    const pending = localStorage.getItem("glossa_exp_builder_open");
    if (!pending) return;
    localStorage.removeItem("glossa_exp_builder_open");
    try {
      const parsed = JSON.parse(pending) as { action: string; id?: string };
      if (parsed.action === "new") {
        setTimeout(() => setShowNew(true), 50);
      } else {
        setPendingAction(parsed);
      }
    } catch { /* ignore */ }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  // NOTE: the execution effect for pendingAction is placed AFTER loadExp
  // so that loadExp can be directly included in its deps (no forward-reference).

  // Load saved experiment — snap positions, restore handles, then auto-arrange.
  const loadExp = useCallback(async (id: string) => {
    try {
      const d = await getGraphExperiment(id);
      setActiveExp(d);
      setSelectedNode(null);
      // Dispatch context for Glossa AI auto-inference
      window.dispatchEvent(new CustomEvent("glossa:context", { detail: { type: "experiment", id, name: d.name } }));

      const snap15e = (n: number) => Math.round(n / 15) * 15;

      const mappedNodes = (d.nodes as Node<ExpNodeData>[]).map(n => {
        const atomicId = (n.data as ExpNodeData).atomicId;
        // Find the atomic node definition; fall back to a minimal ExperimentWrapper def
        let def = catalog.find(c => c.id === atomicId);
        if (!def && atomicId === "ExperimentWrapper") {
          def = {
            id: "ExperimentWrapper", name: (n.data as ExpNodeData).label, category: "Experiments",
            description: "",
            inputs:  [{ name: "upstream", type: "any",  required: false }],
            outputs: [{ name: "result",   type: "json" }],
            params_schema: { type: "object", properties: {
              experiment_id: { type: "string", title: "Experiment ID" },
              corpus_id:     { type: "string", title: "Corpus ID" },
            }},
          };
        }
        const rawPos = (n.position as { x?: number; y?: number } | undefined) ?? { x: 80, y: 80 };
        return {
          ...n, type: "expNode",
          position: { x: snap15e(rawPos.x ?? 80), y: snap15e(rawPos.y ?? 80) },
          data: { ...n.data as ExpNodeData, darkMode,
            inputs:       def?.inputs       ?? [],
            outputs:      def?.outputs      ?? [],
            params_schema:def?.params_schema ?? {} },
        };
      });

      // Restore React Flow sourceHandle / targetHandle from stored sourcePort / targetPort.
      // Edge colour is derived from the source port type.
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const mappedEdges = (d.edges as any[]).map(e => {
        const sp = (e as Record<string, string>).sourcePort;
        const tp = (e as Record<string, string>).targetPort;
        // Look up colour via the source node's output port type
        const srcNode = mappedNodes.find(n => n.id === e.source);
        const srcPortType = (srcNode?.data as ExpNodeData)?.outputs?.find(p => p.name === sp)?.type;
        const color = srcPortType ? (PORT_CLR[srcPortType] ?? PORT_CLR.any) : PORT_CLR.any;
        return {
          ...e,
          sourceHandle: sp ? `out__${sp}` : undefined,
          targetHandle: tp ? `in__${tp}`  : undefined,
          style: { stroke: color, strokeWidth: 2 },
        };
      });

      // Auto-arrange on load so the graph is always presented in a clean layout
      setNodes(autoArrangeNodes(mappedNodes as Node[], mappedEdges) as Node<ExpNodeData>[]);
      setEdges(mappedEdges);
      setFitTrigger(t => t + 1);
    } catch { /* ignore */ }
  }, [catalog, darkMode]);

  // Execute pending "load" / "dup" action AFTER catalog is populated.
  // loadExp is directly in deps here (no forward-reference because we are AFTER its definition).
  // This guarantees loadExp closes over the freshly-populated catalog.
  useEffect(() => {
    if (!pendingAction || catalog.length === 0) return;
    const { action, id } = pendingAction;
    setPendingAction(null);

    if (action === "load" && id) {
      void loadExp(id);
    } else if (action === "dup" && id) {
      const dup = async () => {
        try {
          const d = await getGraphExperiment(id);
          const copy = await createGraphExperiment({
            ...d, id: undefined as unknown as string, name: `${d.name} (copy)`,
          });
          setSavedExps(prev => [
            { id: copy.id!, name: copy.name, description: copy.description,
              node_count: copy.nodes.length, edge_count: copy.edges.length },
            ...prev,
          ]);
          void loadExp(copy.id!);
        } catch { /* ignore */ }
      };
      void dup();
    }
  }, [pendingAction, catalog, loadExp]);  // loadExp is defined above — no forward-reference

  // Save
  const doSave = useCallback(async () => {
    if (!activeExp) return;
    setSaving(true);
    try {
      const graph: GraphExperiment = {
        ...activeExp,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        nodes: nodes.map(n => ({ id: n.id, type: "expNode", position: n.position, data: { atomicId: (n.data as ExpNodeData).atomicId, label: n.data.label, params: n.data.params } })) as any,
        edges: edges.map(e => ({ id: e.id, source: e.source, target: e.target, sourcePort: e.sourceHandle?.replace("out__",""), targetPort: e.targetHandle?.replace("in__","") })) as any,
      };
      const saved = activeExp.id
        ? await updateGraphExperiment(activeExp.id, graph)
        : await createGraphExperiment(graph);
      setActiveExp(saved);
      setSavedExps(prev => {
        const idx = prev.findIndex(e => e.id === saved.id);
        const meta = { id: saved.id!, name: saved.name, description: saved.description, node_count: nodes.length, edge_count: edges.length };
        return idx >= 0 ? prev.map((e, i) => i === idx ? meta : e) : [meta, ...prev];
      });
      setSaveMsg("Saved"); setTimeout(() => setSaveMsg(null), 2000);
    } catch { setSaveMsg("Failed"); }
    finally { setSaving(false); }
  }, [activeExp, nodes, edges]);

  // Run (streaming) — only one run per experiment allowed; state persists across navigation.
  const doRun = useCallback(async (targetExp?: typeof activeExp) => {
    const exp = targetExp ?? activeExp;
    if (!exp?.id) return;
    // Single-run guard: don’t start if this experiment is already running
    if (Object.values(_erStore.runs).some(r => r.expId === exp.id)) return;
    await doSave();
    const runKey = `${exp.id}:${Date.now().toString(36)}`;
    const controller = new AbortController();
    _erSet(prev => ({ ...prev, [runKey]: { controller, startTime: Date.now(), currentLabel: "", idx: 0, total: 0, expId: exp.id! } }));
    setRunResult(null);
    window.dispatchEvent(new CustomEvent("glossa:running", { detail: { builder: "exp", running: true, id: exp.id, name: exp.name } }));
    // Use a local flag — DON’T rely on runResult state (it’s stale in this closure)
    let runSucceeded = false;
    let hadError = false;
    try {
      for await (const ev of runGraphExperimentStream(exp.id!, {}, controller.signal)) {
        if (ev.event === "started") {
          _erSet(prev => prev[runKey] ? { ...prev, [runKey]: { ...prev[runKey], total: ev.node_count ?? 0 } } : prev);
        } else if (ev.event === "node_start" && ev.nid) {
          _erSet(prev => prev[runKey] ? { ...prev, [runKey]: { ...prev[runKey], currentLabel: ev.label ?? "", idx: ev.idx ?? 0, total: ev.total ?? 0 } } : prev);
          if (activeExp?.id === exp.id) {
            setNodes(prev => prev.map(n => ({ ...n, data: { ...n.data, runStatus: n.id === ev.nid ? "running" : (n.data.runStatus === "running" ? "idle" : n.data.runStatus) } as ExpNodeData })));
          }
        } else if (ev.event === "node_end" && ev.nid) {
          const st = ev.status === "error" ? "error" : "complete";
          if (st === "error") hadError = true;
          if (activeExp?.id === exp.id) {
            setNodes(prev => prev.map(n => n.id === ev.nid ? { ...n, data: { ...n.data, runStatus: st } as ExpNodeData } : n));
          }
        } else if (ev.event === "run_complete") {
          runSucceeded = true;
          const keys = Object.keys(ev.result || {}).slice(0, 4).join(", ");
          setRunResult(`complete: ${keys || "done"}`);
        } else if (ev.event === "run_error") {
          hadError = true;
          setRunResult(`Error: ${ev.message ?? "run failed"}`);
          if (activeExp?.id === exp.id) {
            setNodes(prev => prev.map(n => ({ ...n, data: { ...n.data, runStatus: "error" } as ExpNodeData })));
          }
        }
      }
    } catch (e) {
      if (!(e instanceof DOMException && e.name === "AbortError")) {
        hadError = true;
        setRunResult(`Error: ${e instanceof Error ? e.message : "run failed"}`);
      }
      _erSet(prev => { const n = { ...prev }; delete n[runKey]; return n; });
      saveToExpRunCache(exp.id!, "fail");
      window.dispatchEvent(new CustomEvent("glossa:running", { detail: { builder: "exp", running: false, id: exp.id, status: "fail" } }));
      return;
    }
    _erSet(prev => { const n = { ...prev }; delete n[runKey]; return n; });
    const finalStatus: "success" | "fail" = (runSucceeded && !hadError) ? "success" : "fail";
    saveToExpRunCache(exp.id!, finalStatus);
    window.dispatchEvent(new CustomEvent("glossa:running", { detail: { builder: "exp", running: false, id: exp.id, status: finalStatus } }));
  }, [activeExp, doSave, saveToExpRunCache]);

  const stopAll = useCallback(() => {
    Object.values(_erStore.runs).forEach(r => r.controller.abort());
  }, []);

  const stopExp = useCallback((expId: string) => {
    Object.values(_erStore.runs).filter(r => r.expId === expId).forEach(r => r.controller.abort());
  }, []);


  // Delete saved experiment
  const doDeleteExp = useCallback(async (id: string) => {
    if (deleteConfirm !== id) { setDeleteConfirm(id); setTimeout(() => setDeleteConfirm(null), 3000); return; }
    setDeleteConfirm(null);
    await deleteGraphExperiment(id);
    setSavedExps(prev => prev.filter(e => e.id !== id));
    if (activeExp?.id === id) { setActiveExp(null); setNodes([]); setEdges([]); }
  }, [deleteConfirm, activeExp]);

  // Variable-input node helpers (Merger auto-grows when last input is wired)
  const VARIABLE_INPUT_NODES = new Set(["Merger", "ResultMerger"]);
  const nextInputName = (inputs: { name: string }[]) => {
    const used = new Set(inputs.map(i => i.name));
    const alpha = "abcdefghijklmnopqrstuvwxyz";
    for (const c of alpha) if (!used.has(c)) return c;
    for (let n = 2; n < 100; n++) for (const c of alpha) { const k = c + n; if (!used.has(k)) return k; }
    return `in${inputs.length}`;
  };

  // React Flow handlers
  const onNodesChange = useCallback((ch: NodeChange[]) => {
    // Track drag state so history doesn't push mid-drag
    const hasDragStart = ch.some(c => c.type === "position" && (c as { dragging?: boolean }).dragging);
    const hasDragStop  = ch.some(c => c.type === "position" && !(c as { dragging?: boolean }).dragging);
    if (hasDragStart) isDraggingNodeRef.current = true;
    if (hasDragStop)  isDraggingNodeRef.current = false;
    setNodes(n => applyNodeChanges(ch, n) as Node<ExpNodeData>[]);
  }, []);
  const onEdgesChange = useCallback((ch: EdgeChange[]) => setEdges(e => applyEdgeChanges(ch, e)), []);
  const onConnect = useCallback((c: Connection) => {
    const srcPort = c.sourceHandle?.replace("out__","") ?? "";
    const tgtPort = c.targetHandle?.replace("in__","") ?? "";
    const srcNode = nodes.find(n => n.id === c.source);
    const tgtNode = nodes.find(n => n.id === c.target);
    const srcType = (srcNode?.data as ExpNodeData)?.outputs?.find(p => p.name === srcPort)?.type ?? "any";
    const tgtType = (tgtNode?.data as ExpNodeData)?.inputs?.find(p => p.name === tgtPort)?.type ?? "any";
    const compatible = srcType === tgtType || srcType === "any" || tgtType === "any";
    const edgeColor = compatible ? (PORT_CLR[srcType] ?? PORT_CLR.any) : "#f59e0b";
    setEdges(e => addEdge({ ...c, id: `e_${Date.now().toString(36)}`, style: { stroke: edgeColor, strokeWidth: 2.5 }, label: compatible ? undefined : "⚠ type mismatch" }, e));
    // Auto-grow variable-input nodes: when the last input slot is wired, add a new empty slot
    if (tgtNode && VARIABLE_INPUT_NODES.has((tgtNode.data as ExpNodeData).atomicId)) {
      const tnd = tgtNode.data as ExpNodeData;
      if (tnd.inputs.length > 0 && tnd.inputs[tnd.inputs.length - 1].name === tgtPort) {
        const newName = nextInputName(tnd.inputs);
        setNodes(prev => prev.map(n =>
          n.id === c.target
            ? { ...n, data: { ...n.data, inputs: [...tnd.inputs, { name: newName, type: "any", required: false }] } as ExpNodeData }
            : n
        ));
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [nodes]);

  const onNodeClick = useCallback((_: React.MouseEvent, n: Node) => { setSelectedNode(n as Node<ExpNodeData>); setInspectorOff(false); setCtxMenu(null); }, []);
  const onPaneClick = useCallback(() => { setSelectedNode(null); setCtxMenu(null); }, []);

  // Context menus — properly typed so preventDefault works reliably
  const onNodeCtx = useCallback((ev: React.MouseEvent, n: Node) => {
    ev.preventDefault(); ev.stopPropagation();
    setCtxMenu({ x: ev.clientX, y: ev.clientY, type: "node", nodeId: n.id });
    setSelectedNode(n as Node<ExpNodeData>);
  }, []);
  const onPaneCtxMenu = useCallback((ev: React.MouseEvent<HTMLDivElement>) => {
    ev.preventDefault();
    setCtxMenu({ x: ev.clientX, y: ev.clientY, type: "pane" });
  }, []);

  // Param change
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const onParamChange = useCallback((nodeId: string, params: Record<string, any>) => {
    setNodes(prev => prev.map(n => n.id === nodeId ? { ...n, data: { ...n.data, params } as ExpNodeData } : n));
    setSelectedNode(prev => prev?.id === nodeId ? { ...prev, data: { ...prev.data, params } as ExpNodeData } : prev);
  }, []);

  // Drop from palette — supports both atomic nodes and experiment wrappers
  const draggedExpId = useRef<string | null>(null);
  const onDrop = useCallback((ev: React.DragEvent<HTMLDivElement>) => {
    ev.preventDefault();
    if (!activeExp) return;  // guard: no experiment open, ignore drop
    if (!reactFlowWrapper.current) return;
    const rect = reactFlowWrapper.current.getBoundingClientRect();
    const pos = { x: Math.round((ev.clientX - rect.left - 80) / 15) * 15, y: Math.round((ev.clientY - rect.top - 30) / 15) * 15 };
    if (draggedExpId.current) {
      // Create a SubExperiment node pointing to the dragged graph experiment (H16)
      const exp = savedExps.find(e => e.id === draggedExpId.current);
      if (exp) {
        const subDef = catalog.find(d => d.id === "SubExperiment");
        const subInputs  = subDef?.inputs  ?? [{ name: "a", type: "any", required: false }];
        const subOutputs = subDef?.outputs ?? [{ name: "result", type: "json" }, { name: "conclusions", type: "json" }];
        const subSchema  = subDef?.params_schema ?? { type: "object", properties: { experiment_id: { type: "string", title: "Experiment ID" } } };
        setNodes(n => [...n, { id: nextId(), type: "expNode", position: pos,
          data: { atomicId: "SubExperiment", label: exp.name, inputs: subInputs, outputs: subOutputs,
            params: { experiment_id: exp.id }, params_schema: subSchema, runStatus: "idle", darkMode } as ExpNodeData }]);
      }
      draggedExpId.current = null; draggedNodeType.current = null; return;
    }
    if (!draggedNodeType.current) return;
    const def = catalog.find(d => d.id === draggedNodeType.current);
    if (!def) return;
    const defaultParams = Object.fromEntries(Object.entries(def.params_schema.properties ?? {}).map(([k, v]) => [k, (v as Record<string, unknown>).default ?? ""]));
    setNodes(n => [...n, { id: nextId(), type: "expNode", position: pos,
      data: { atomicId: def.id, label: def.name, inputs: def.inputs, outputs: def.outputs, params: defaultParams, params_schema: def.params_schema, runStatus: "idle", darkMode } as ExpNodeData }]);
    draggedNodeType.current = null;
  }, [catalog, savedExps, darkMode]);
  const onDragOver = (ev: React.DragEvent) => {
    if (!activeExp) return;  // no drop target when no experiment open
    ev.preventDefault(); ev.dataTransfer.dropEffect = "move";
  };

  const nodeCtxItems = useCallback((nodeId: string): CtxItem[] => {
    const nd = nodes.find(n => n.id === nodeId);
    return [
      { icon: "⍘", label: "Duplicate", action: () => { if (!nd) return; setNodes(n => [...n, { id: nextId(), type: "expNode", position: { x: nd.position.x + 20, y: nd.position.y + 20 }, data: { ...nd.data, runStatus: "idle" } as ExpNodeData }]); }},
      { divider: true },
      { icon: "🔗", label: "Disconnect all", action: () => setEdges(e => e.filter(ed => ed.source !== nodeId && ed.target !== nodeId)) },
      { divider: true },
      { icon: "🗑", label: "Delete node", danger: true, action: () => { setNodes(n => n.filter(x => x.id !== nodeId)); setEdges(e => e.filter(ed => ed.source !== nodeId && ed.target !== nodeId)); if (selectedNode?.id === nodeId) setSelectedNode(null); }},
      { divider: true },
      { icon: "↩", label: "Undo", action: undo },
      { icon: "↪", label: "Redo", action: redo },
    ];
  }, [nodes, selectedNode, undo, redo]);

  const paneCtxItems = useCallback((x: number, y: number): CtxItem[] => {
    if (!activeExp) return [   // No experiment open — offer workspace-level actions
      { icon: "＋", label: "New Experiment",    action: () => setShowNew(true) },
      { icon: "↑",  label: "Import from JSON",  action: () => importRef.current?.click() },
      { divider: true },
      { icon: "↩",  label: "Undo", action: undo },
      { icon: "↪",  label: "Redo", action: redo },
    ];
    if (!reactFlowWrapper.current) return [];
    const rect = reactFlowWrapper.current.getBoundingClientRect();
    const pos = { x: Math.round((x - rect.left - 80) / 15) * 15, y: Math.round((y - rect.top - 30) / 15) * 15 };
    const addNode = (d: AtomicNodeDef) => {
      const dp = Object.fromEntries(Object.entries(d.params_schema.properties ?? {}).map(([k, v]) => [k, (v as Record<string, unknown>).default ?? ""]));
      setNodes(n => [...n, { id: nextId(), type: "expNode", position: pos, data: { atomicId: d.id, label: d.name, inputs: d.inputs, outputs: d.outputs, params: dp, params_schema: d.params_schema, runStatus: "idle", darkMode } as ExpNodeData }]);
    };
    const cats = [...new Set(catalog.filter(d => d.id !== "ExperimentWrapper").map(d => d.category))];
    return cats.flatMap((cat, ci) => [
      ...(ci > 0 ? [{ divider: true }] : []),
      ...catalog.filter(d => d.category === cat && d.id !== "ExperimentWrapper").map(d => ({ icon: "◆", label: `${cat}: ${d.name}`, action: () => addNode(d) })),
    ]);
  }, [catalog, darkMode]);

  // Outer panel divider (width)
  const onDividerDown = useCallback((e: React.MouseEvent) => {
    isDragging.current = true; dragStart.current = e.clientX; dragW0.current = leftW;
    const onMove = (me: MouseEvent) => {
      if (!isDragging.current) return;
      const dx = dockL ? me.clientX - dragStart.current : dragStart.current - me.clientX;
      setLeftW(Math.max(160, Math.min(480, dragW0.current + dx)));
    };
    const onUp = () => { isDragging.current = false; document.removeEventListener("mousemove", onMove); document.removeEventListener("mouseup", onUp); };
    document.addEventListener("mousemove", onMove); document.addEventListener("mouseup", onUp);
  }, [leftW, dockL]);

  // Inner panel divider (experiments list height vs palette)
  const onInnerDivDown = useCallback((e: React.MouseEvent) => {
    innerDivStart.current = e.clientY; innerDivH0.current = expsH;
    e.preventDefault(); e.stopPropagation();
    const onMove = (me: MouseEvent) => { setExpsH(Math.max(60, Math.min(400, innerDivH0.current + me.clientY - innerDivStart.current))); };
    const onUp   = () => { document.removeEventListener("mousemove", onMove); document.removeEventListener("mouseup", onUp); };
    document.addEventListener("mousemove", onMove); document.addEventListener("mouseup", onUp);
  }, [expsH]);

  // Auto-arrange
  const doArrange = useCallback(() => {
    setNodes(prev => autoArrangeNodes(prev, edges) as Node<ExpNodeData>[]);
    setFitTrigger(t => t + 1);
  }, [edges]);

  // Import/export helpers
  const importRef = useRef<HTMLInputElement>(null);
  const onImportExp = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]; if (!f) return;
    try {
      const d = JSON.parse(await f.text());
      const saved = await createGraphExperiment(d);
      setActiveExp(saved);
      setSavedExps(prev => [{ id: saved.id!, name: saved.name, description: saved.description, node_count: saved.nodes.length, edge_count: saved.edges.length }, ...prev]);
    } catch { alert("Invalid experiment file."); }
    e.target.value = "";
  }, []);
  const exportExp = useCallback(() => {
    if (!activeExp) return;
    const blob = new Blob([JSON.stringify(activeExp, null, 2)], { type: "application/json" });
    const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: `${(activeExp.name || "exp").replace(/\s+/g, "_")}.glossa-exp.json` });
    a.click(); URL.revokeObjectURL(a.href);
  }, [activeExp]);

  // Grouped atomic palette (ExperimentWrapper shown separately)
  const categories = useMemo(() => {
    const cats: Record<string, AtomicNodeDef[]> = {};
    for (const d of catalog) {
      if (d.id === "ExperimentWrapper") continue;
      if (palSearch && !d.name.toLowerCase().includes(palSearch.toLowerCase())) continue;
      (cats[d.category] = cats[d.category] || []).push(d);
    }
    return cats;
  }, [catalog, palSearch]);
  const [expSort, setExpSort] = useState<"name" | "nodes" | "id">("name");
  const [expSortAsc, setExpSortAsc] = useState(true);

  // Starred / pinned experiments — floated to top of name sort, persisted
  const [starredExps, setStarredExps] = useState<Set<string>>(() => {
    try { return new Set(JSON.parse(localStorage.getItem("glossa_starred_exps") ?? "[]")); }
    catch { return new Set(); }
  });
  const toggleStarExp = useCallback((id: string) => {
    setStarredExps(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      localStorage.setItem("glossa_starred_exps", JSON.stringify([...next]));
      return next;
    });
  }, []);

  const sortedFilteredExps = useMemo(() => {
    const arr = savedExps.filter(e => !palSearch || e.name.toLowerCase().includes(palSearch.toLowerCase()));
    return arr.slice().sort((a, b) => {
      if (expSort === "name") {
        // Starred group first (sorted by name), then unstarred group (sorted by name)
        const aS = starredExps.has(a.id ?? ""), bS = starredExps.has(b.id ?? "");
        if (aS !== bS) return aS ? -1 : 1;
        const c = a.name.localeCompare(b.name);
        return expSortAsc ? c : -c;
      }
      let cmp = 0;
      if (expSort === "nodes") cmp = (a.node_count ?? 0) - (b.node_count ?? 0);
      if (expSort === "id")    cmp = a.id!.localeCompare(b.id ?? "");
      return expSortAsc ? cmp : -cmp;
    });
  }, [savedExps, palSearch, expSort, expSortAsc, starredExps]);

  const filteredSavedExps = sortedFilteredExps;
  const catColors: Record<string, string> = { Sources: "#059669", Transforms: "#2563eb", Analysis: "#7c3aed", Outputs: "#0d9488" };
  const ebm: React.CSSProperties = { border: `1px solid ${th.border}`, borderRadius: 3, background: "none", color: th.textMuted, cursor: "pointer", fontSize: 10, padding: "0 4px", lineHeight: "18px" };

  // ── Left panel (resizable + collapsible + dockable) ────────────────────
  const LeftPanel = (
    <div style={{ width: leftOff ? 32 : leftW, background: th.panelBg, [dockL ? "borderRight" : "borderLeft"]: `1px solid ${th.border}`, display: "flex", flexDirection: "column", flexShrink: 0, overflow: "hidden", transition: "width 0.12s" }}>
      {/* Header row */}
      <div style={{ padding: "6px 5px", borderBottom: `1px solid ${th.border}`, display: "flex", alignItems: "center", gap: 3, flexShrink: 0 }}>
        <button onClick={() => setLeftOff(c => !c)} title={leftOff ? "Expand" : "Collapse"} style={{ border: "none", background: "none", color: th.textMuted, cursor: "pointer", fontSize: 13, padding: "2px 4px", borderRadius: 3 }}>{leftOff ? "▶" : "◀"}</button>
        {!leftOff && (
          <>
            <span style={{ fontSize: 10, fontWeight: 700, color: th.textFaint, flex: 1, textTransform: "uppercase", letterSpacing: 0.5 }}>Workspace</span>
            <button onClick={() => setDockL(d => !d)} title="Switch dock side" style={{ border: "none", background: "none", color: th.textFaint, cursor: "pointer", fontSize: 12 }}>⇄</button>
          </>
        )}
      </div>

      {!leftOff && (
        <>
          {/* Graph Experiments list */}
          <div style={{ padding: "7px 7px 4px", borderBottom: `1px solid ${th.border}`, flexShrink: 0, height: expsH, overflowY: "auto", boxSizing: "border-box" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 3, marginBottom: 4 }}>
              <span style={{ fontSize: 9, fontWeight: 700, color: th.textMuted, textTransform: "uppercase", letterSpacing: 0.5, flex: 1 }}>Graph Experiments</span>
              <button onClick={() => savedExps.filter(e => e.id && !isExpRunning(e.id)).forEach(e => void doRun({ id: e.id!, name: e.name, description: e.description ?? "", nodes: [], edges: [] }))}
                title="Run all experiments (skips already-running ones)" disabled={savedExps.length === 0}
                style={{ ...ebm, color: "#22c55e", borderColor: "#15803d40", opacity: savedExps.length === 0 || hasActiveRuns ? 0.4 : 1 }}>▶▶</button>
              <button onClick={() => setShowNew(true)} title="New graph experiment" style={{ ...ebm }}>+</button>
              <button onClick={() => importRef.current?.click()} title="Import" style={{ ...ebm }}>↑</button>
            </div>
            {/* Search + sort row */}
            <div style={{ display: "flex", gap: 3, marginBottom: 4, alignItems: "center" }}>
              <input value={palSearch} onChange={e => setPalSearch(e.target.value)}
                placeholder="Search…" style={{ flex: 1, padding: "2px 5px", fontSize: 9, borderRadius: 3,
                  border: `1px solid ${th.inputBdr}`, background: th.inputBg, color: th.inputText, outline: "none" }} />
              {(["name", "nodes"] as const).map(s => (
                <button key={s} onClick={() => { if (expSort === s) setExpSortAsc(a => !a); else { setExpSort(s); setExpSortAsc(true); } }}
                  title={`Sort by ${s}`}
                  style={{ ...ebm, fontWeight: expSort === s ? 700 : 400, color: expSort === s ? th.activeText : th.textMuted,
                    background: expSort === s ? th.activeBg : "none", padding: "0 4px" }}>
                  {s === "name" ? "A↓" : "#↓"}{expSort === s ? (expSortAsc ? "▲" : "▼") : ""}
                </button>
              ))}
            </div>
            {sortedFilteredExps.length === 0 && <div style={{ fontSize: 10, color: th.textFaint, fontStyle: "italic", padding: "4px 2px" }}>{palSearch ? "No matches." : "No graph experiments yet."}</div>}
            {sortedFilteredExps.map(e => {
              const active = activeExp?.id === e.id;
              const expRuns = getExpRuns(e.id);
              const isRunning = expRuns.length > 0;
              const latestRun = expRuns.sort((a, b) => b.startTime - a.startTime)[0];
              const isStarred = starredExps.has(e.id ?? "");
              return (
                <div key={e.id}
                  draggable
                  onDragStart={() => { draggedExpId.current = e.id; draggedNodeType.current = null; }}
                  onClick={() => void loadExp(e.id)}
                  title="Click to open · Drag to canvas to add as SubExperiment node"
                  style={{ display: "flex", alignItems: "center", gap: 3, padding: "5px 6px", borderRadius: 5, marginBottom: 2, cursor: "pointer",
                    background: active ? th.activeBg : isStarred ? (darkMode ? "#1a110a" : "#fffbeb") : "transparent",
                    border: `1px solid ${isRunning ? "#60a5fa60" : active ? "#7c3aed40" : isStarred ? "#f59e0b30" : "transparent"}` }}>
                  {/* Star / pin button */}
                  <button onClick={ev => { ev.stopPropagation(); toggleStarExp(e.id ?? ""); }}
                    title={isStarred ? "Unpin" : "Pin to top"}
                    style={{ border: "none", background: "none", cursor: "pointer", fontSize: 9, padding: 0, lineHeight: 1, flexShrink: 0,
                      color: isStarred ? "#f59e0b" : th.textFaint, opacity: isStarred ? 1 : 0.35 }}>
                    {isStarred ? "⭐" : "☆"}
                  </button>
                  {/* Pulsing ring indicator when running */}
                  {isRunning && (
                    <span style={{ position: "relative", display: "inline-flex", width: 8, height: 8, flexShrink: 0 }}>
                      <span style={{ position: "absolute", inset: 0, borderRadius: "50%", background: "#60a5fa",
                        animation: "glossa-pulse-ring 1.2s ease-out infinite" }} />
                      <span style={{ position: "relative", display: "inline-block", width: 8, height: 8, borderRadius: "50%", background: "#60a5fa" }} />
                    </span>
                  )}
                  <span style={{ flex: 1, fontSize: 11, fontWeight: active ? 600 : 400, color: active ? th.activeText : th.text, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>🔀 {e.name}</span>
                  {isRunning && latestRun && (() => {
                    const elSec = getElapsed(latestRun);
                    const pct = latestRun.total > 0 ? Math.round((latestRun.idx / latestRun.total) * 100) : null;
                    const eta = (pct !== null && pct > 5) ? Math.round((elSec / pct) * (100 - pct)) : null;
                    return (
                      <span style={{ fontSize: 8, color: "#60a5fa", fontWeight: 700, flexShrink: 0, whiteSpace: "nowrap" }}>
                        {pct !== null ? `${pct}%` : fmtHMS(elSec)}
                        {eta !== null && ` ≈${fmtHMS(eta)}`}
                      </span>
                    );
                  })()}
                  {/* Last-run status badge (only when not currently running) */}
                  {!isRunning && expRunCache[e.id ?? ""] && (
                    <span style={{
                      fontSize: 8, fontWeight: 700, flexShrink: 0,
                      color: expRunCache[e.id ?? ""].status === "success" ? "#22c55e" : "#ef4444",
                    }} title={expRunCache[e.id ?? ""].status === "success" ? "Last run succeeded" : "Last run failed"}>
                      {expRunCache[e.id ?? ""].status === "success" ? "✓" : "✗"}
                    </span>
                  )}
                  <span style={{ fontSize: 9, color: th.textFaint, flexShrink: 0 }}>{e.node_count}n</span>
                  {/* Run / running indicator button */}
                  {e.id && (
                    <button
                      onClick={ev => { ev.stopPropagation(); if (!isRunning) void doRun({ id: e.id, name: e.name, description: e.description ?? "", nodes: [], edges: [] }); }}
                      title={isRunning ? "Running…" : "Run"}
                      disabled={isRunning}
                      style={{ border: "none", background: "none", color: isRunning ? "#60a5fa" : "#22c55e",
                        cursor: isRunning ? "default" : "pointer", fontSize: 10, padding: "0 2px",
                        lineHeight: "18px", borderRadius: 3, flexShrink: 0, opacity: isRunning ? 0.6 : 1 }}>
                      {isRunning ? "⏳" : "▶"}
                    </button>
                  )}
                  <button onClick={ev => { ev.stopPropagation(); void doDeleteExp(e.id); }} title={deleteConfirm === e.id ? "Confirm?" : "Delete"}
                    style={{ border: "none", background: "none", color: deleteConfirm === e.id ? "#f87171" : th.textMuted, cursor: "pointer", fontSize: 10, padding: "0 3px", lineHeight: "18px", borderRadius: 3, flexShrink: 0 }}>
                    {deleteConfirm === e.id ? "!" : "×"}
                  </button>
                </div>
              );
            })}
          </div>

          {/* Inner resize divider — drag to adjust experiments list vs palette height */}
          <div onMouseDown={onInnerDivDown}
            style={{ height: 4, cursor: "row-resize", background: th.panelBg, flexShrink: 0, borderTop: `1px solid ${th.border}`, transition: "border-color 0.1s" }}
            onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderTopColor = th.borderHov; }}
            onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderTopColor = th.border; }}
          />

          {/* Atomic + Experiment palette */}
          <div style={{ flex: 1, overflowY: "auto", minHeight: 0, padding: "7px 8px" }}>
            <div style={{ fontSize: 9, fontWeight: 700, color: th.textMuted, textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 5 }}>Node Palette</div>
            <input value={palSearch} onChange={e => setPalSearch(e.target.value)} placeholder="Search nodes…"
              style={{ width: "100%", boxSizing: "border-box", padding: "4px 7px", fontSize: 10, border: `1px solid ${th.inputBdr}`, borderRadius: 5, marginBottom: 6, outline: "none", background: th.inputBg, color: th.inputText }} />
            {Object.entries(categories).map(([cat, defs]) => (
              <div key={cat} style={{ marginBottom: 8 }}>
                <div style={{ fontSize: 9, fontWeight: 700, color: catColors[cat] ?? "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 3 }}>{cat}</div>
                {defs.map(def => {
                  const hdrClr = def.outputs[0] ? PORT_CLR[def.outputs[0].type] : "#334155";
                  return (
                    <div key={def.id} draggable onDragStart={() => { draggedNodeType.current = def.id; draggedExpId.current = null; }}
                      title={def.description}
                      style={{ padding: "4px 7px", marginBottom: 3, cursor: "grab", border: `1px solid ${hdrClr}40`, borderRadius: 5, background: hdrClr + "0d" }}>
                      <div style={{ fontSize: 10, fontWeight: 600, color: hdrClr }}>{def.name}</div>
                      <div style={{ display: "flex", gap: 3, marginTop: 2, flexWrap: "wrap" }}>
                        {def.inputs.map(p  => <span key={p.name} style={{ fontSize: 8, padding: "0 3px", borderRadius: 2, background: PORT_CLR[p.type] + "25", color: PORT_CLR[p.type] ?? PORT_CLR.any }}>↓{p.name}</span>)}
                        {def.outputs.map(p => <span key={p.name} style={{ fontSize: 8, padding: "0 3px", borderRadius: 2, background: PORT_CLR[p.type] + "25", color: PORT_CLR[p.type] ?? PORT_CLR.any }}>↑{p.name}</span>)}
                      </div>
                    </div>
                  );
                })}
              </div>
            ))}
            {filteredSavedExps.length > 0 && (
              <div style={{ marginBottom: 8 }}>
                <div style={{ fontSize: 9, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 3 }}>Sub-Experiments</div>
                <div style={{ fontSize: 8, color: th.textFaint, marginBottom: 4, fontStyle: "italic" }}>Drag to canvas → SubExperiment node</div>
                {filteredSavedExps.map(exp => (
                  <div key={exp.id} draggable onDragStart={() => { draggedExpId.current = exp.id; draggedNodeType.current = null; }}
                    title={`Drag to add as SubExperiment: ${exp.description}`}
                    style={{ padding: "4px 7px", marginBottom: 3, cursor: "grab", border: "1px solid #7c3aed40", borderRadius: 5, background: "#7c3aed0d" }}>
                    <div style={{ fontSize: 10, fontWeight: 600, color: "#7c3aed" }}>🔀 {exp.name}</div>
                    <div style={{ fontSize: 8, color: th.textFaint, marginTop: 1 }}>{exp.node_count}n · SubExperiment</div>
                  </div>
                ))}
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

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0, overflow: "hidden" }}>
      {/* Toolbar — condensed single row */}
      <div style={{ display: "flex", alignItems: "center", gap: 4, padding: "3px 8px", background: th.panelBg2, borderBottom: `1px solid ${th.border}`, flexShrink: 0 }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: th.text, flexShrink: 0 }}>🔀 Experiment Builder</span>
        {activeExp && <span style={{ fontSize: 10, color: th.textMuted, maxWidth: 180, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{activeExp.name}</span>}
        {saveMsg && <span style={{ fontSize: 10, color: saveMsg === "Saved" ? "#22c55e" : "#ef4444", fontWeight: 600, flexShrink: 0 }}>{saveMsg}</span>}
        <div style={{ flex: 1 }} />
        {/* Active run progress for the current experiment */}
        {activeExp?.id && isExpRunning(activeExp.id) && (() => {
          const runs = getExpRuns(activeExp.id);
          const r = runs.sort((a, b) => b.startTime - a.startTime)[0];
          const elSec = getElapsed(r);
          const pct  = r.total > 0 ? Math.round((r.idx / r.total) * 100) : null;
          const eta  = (pct !== null && pct > 5) ? Math.round((elSec / pct) * (100 - pct)) : null;
          return (
            <span style={{ fontSize: 10, color: "#60a5fa", fontWeight: 600, flexShrink: 0, whiteSpace: "nowrap" }}>
              ⏳
              {pct !== null ? ` ${pct}%` : ""}
              {` ${fmtHMS(elSec)}`}
              {eta !== null ? ` ≈${fmtHMS(eta)} left` : ""}
              {r.currentLabel ? ` · ${r.currentLabel.slice(0, 14)}` : ""}
            </span>
          );
        })()}
        {hasActiveRuns && (
          <button onClick={stopAll} title="Stop all running experiments"
            style={{ padding: "3px 8px", border: "1px solid #ef444430", borderRadius: 5, cursor: "pointer", fontSize: 10, fontWeight: 600, background: "transparent", color: "#ef4444" }}>
            ⏹ Stop All
          </button>
        )}
        {[
          { label: "↩ Undo",   title: "Undo (Ctrl+Z)",       disabled: !canUndo,                   action: undo },
          { label: "↪ Redo",   title: "Redo (Ctrl+Y)",       disabled: !canRedo,                   action: redo },
          { label: "＋ New",    title: "New experiment",      action: () => setShowNew(true) },
          { label: "↑ Import",  title: "Import from JSON",    action: () => importRef.current?.click() },
          { label: "↓ Export",  title: "Export to JSON",      disabled: !activeExp,                 action: exportExp },
          { label: saving ? "…" : "💾 Save", title: "Save",   disabled: saving || !activeExp,       action: () => void doSave() },
          { label: "⬦ Arrange", title: "Auto-arrange nodes",  disabled: !activeExp || nodes.length === 0, action: doArrange },
        ].map(({ label, title, action, disabled }) => (
          <button key={label} onClick={action} disabled={disabled} title={title}
            style={{ padding: "3px 8px", border: `1px solid ${th.border}`, borderRadius: 5, cursor: disabled ? "not-allowed" : "pointer", fontSize: 10, fontWeight: 600, background: "transparent", color: th.textMuted, opacity: disabled ? 0.4 : 1 }}>
            {label}
          </button>
        ))}
        <input ref={importRef} type="file" accept=".json" style={{ display: "none" }} onChange={onImportExp} />
      </div>

      {/* Main area — flexDirection respects dock side */}
      <div style={{ flex: 1, display: "flex", minHeight: 0, flexDirection: dockL ? "row" : "row-reverse", position: "relative" }}>
        {LeftPanel}
        {!leftOff && Divider}

        {/* Canvas — onContextMenu on wrapper handles pane right-click reliably */}
        <div ref={reactFlowWrapper} style={{ flex: 1, minWidth: 0, background: th.canvasBg }}
          onDrop={onDrop} onDragOver={onDragOver} onContextMenu={onPaneCtxMenu}>
          {!activeExp && (
            <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", gap: 10, zIndex: 5, pointerEvents: "none" }}>
              <div style={{ fontSize: 40 }}>🔀</div>
              <div style={{ fontSize: 14, color: th.textMuted, fontWeight: 600 }}>Create or select a graph experiment</div>
              <div style={{ fontSize: 11, color: th.textFaint }}>Use the panel on the left</div>
            </div>
          )}
          {activeExp && nodes.length === 0 && (
            <div style={{ position: "absolute", bottom: 24, left: "50%", transform: "translateX(-50%)", zIndex: 5, pointerEvents: "none",
              background: th.panelBg2, border: `1px solid ${th.border}`, borderRadius: 8, padding: "8px 16px",
              fontSize: 12, color: th.textMuted, textAlign: "center", whiteSpace: "nowrap", boxShadow: "0 2px 12px rgba(0,0,0,0.15)" }}>
              Drag atomic nodes or experiments · Right-click to add
            </div>
          )}
          {/* Floating run/stop button — top-center of canvas */}
          {activeExp?.id && nodes.length > 0 && (
            <div style={{ position: "absolute", top: 12, left: "50%", transform: "translateX(-50%)", zIndex: 20, display: "flex", gap: 6 }}>
              {isExpRunning(activeExp.id) && (
                <button onClick={() => stopExp(activeExp.id!)} title="Stop all runs of this experiment"
                  style={{ padding: "6px 14px", border: "2px solid #ef4444", borderRadius: 20, background: "rgba(69,10,10,0.9)", color: "#f87171", cursor: "pointer", fontSize: 12, fontWeight: 700, boxShadow: "0 2px 12px rgba(0,0,0,0.5)", whiteSpace: "nowrap", backdropFilter: "blur(4px)" }}>
                  ⏹ Stop
                </button>
              )}
              {/* Run button — disabled while experiment is running (single-run enforced) */}
              {!isExpRunning(activeExp.id) && (
                <button onClick={() => void doRun()} title="Run experiment"
                  style={{ border: "none", background: "none", padding: 0, cursor: "pointer" }}>
                  <style>{`@keyframes glossa-pulse-ring{0%{transform:scale(1);opacity:.7}100%{transform:scale(2);opacity:0}}`}</style>
                  <span style={{ padding: "6px 18px", display: "inline-block", borderRadius: 20,
                    background: "linear-gradient(135deg,#7c3aed,#4f46e5)",
                    color: "#fff", fontSize: 12, fontWeight: 700,
                    boxShadow: "0 2px 12px rgba(0,0,0,0.4)", whiteSpace: "nowrap" }}>
                    ▶ Run
                  </span>
                </button>
              )}
            </div>
          )}
          <ReactFlow
            nodes={nodes} edges={edges}
            nodeTypes={EXP_NODE_TYPES}
            onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick} onPaneClick={onPaneClick}
            onNodeContextMenu={onNodeCtx}
            snapToGrid snapGrid={[15, 15]}
            deleteKeyCode={["Backspace", "Delete"]}
            fitView fitViewOptions={{ padding: 0.2 }}
            minZoom={0.15} maxZoom={2.5}
            proOptions={{ hideAttribution: true }}
            style={{ background: th.canvasBg }}
            defaultEdgeOptions={{ style: { stroke: PORT_CLR.any, strokeWidth: 2.5 } }}
          >
            <Controls style={{ background: darkMode ? "#1e293b" : "#fff", border: `1px solid ${th.border}` }} />
            <MiniMap style={{ background: th.canvasBg }} nodeColor={n => (n.data as ExpNodeData)?.outputs?.[0] ? PORT_CLR[(n.data as ExpNodeData).outputs[0].type] : "#334155"} />
            <Background variant={BackgroundVariant.Dots} gap={15} size={1} color={th.canvasGrid} />
            <AutoFitView trigger={fitTrigger} />
          </ReactFlow>
        </div>

        {/* Right Inspector */}
        {!inspectorOff && selectedNode && (
          <Inspector node={selectedNode} onClose={() => setInspectorOff(true)} onParamChange={onParamChange} darkMode={darkMode} />
        )}
        {selectedNode && inspectorOff && (
          <button onClick={() => setInspectorOff(false)}
            style={{ position: "absolute", right: 6, top: "50%", transform: "translateY(-50%)", border: `1px solid ${th.border}`, background: th.panelBg2, color: th.textMuted, cursor: "pointer", borderRadius: 4, padding: "6px 4px", fontSize: 12, zIndex: 100 }}>◀</button>
        )}
      </div>

      {/* Right-click context menu */}
      {ctxMenu && (
        <ContextMenu x={ctxMenu.x} y={ctxMenu.y} onClose={() => setCtxMenu(null)}
          items={ctxMenu.type === "node" && ctxMenu.nodeId ? nodeCtxItems(ctxMenu.nodeId) : paneCtxItems(ctxMenu.x, ctxMenu.y)} />
      )}

      {/* Run result banner */}
      {runResult && (
        <div style={{ flexShrink: 0, padding: "5px 12px", background: runResult.startsWith("Error") ? "#450a0a" : "#052e16", borderTop: `1px solid ${th.border}`, fontSize: 11, color: runResult.startsWith("Error") ? "#fca5a5" : "#86efac", display: "flex", justifyContent: "space-between" }}>
          <span>{runResult}</span>
          <button onClick={() => setRunResult(null)} style={{ border: "none", background: "none", cursor: "pointer", color: "inherit", fontSize: 11 }}>× dismiss</button>
        </div>
      )}

      {/* New experiment dialog */}
      {showNew && (
        <NewExpDialog onClose={() => setShowNew(false)} onCreate={(name, desc) => {
          const empty: GraphExperiment = { name, description: desc, nodes: [], edges: [] };
          setActiveExp(empty);
          setNodes([]); setEdges([]);
        }} />
      )}
    </div>
  );
}
