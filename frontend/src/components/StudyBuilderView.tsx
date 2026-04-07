/**
 * Study Builder — visual workflow composer.
 *
 * Compose experiments and pipelines as graph nodes connected by
 * data-flow edges. Studies are persisted to the backend /studies API.
 *
 * Layout:
 *   Left   │ Palette (experiments + pipelines, draggable)
 *   Center │ React Flow canvas
 *   Right  │ Inspector (selected node params + metadata)
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  ReactFlow,
  addEdge,
  Background,
  BackgroundVariant,
  Controls,
  type Connection,
  type Edge,
  type Node,
  type NodeChange,
  type EdgeChange,
  applyNodeChanges,
  applyEdgeChanges,
  MiniMap,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import {
  createStudy,
  deleteStudy,
  generateStudy,
  listExperiments,
  listStudies,
  getPipelineCatalog,
  runStudy,
  summarizeStudy,
  updateStudy,
  type AISummaryResult,
  type ExperimentMeta,
  type CatalogPipeline,
  type StudyResponse,
  type StudyGraph,
  type StudyRunResult,
} from "../api";
import { useAIChat } from "../hooks/useAIChat";

// ── Param schema helpers ───────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function schemaFromPipelineDefaults(defaults: Record<string, any>): Record<string, any> {
  const props: Record<string, Record<string, unknown>> = {};
  for (const [key, val] of Object.entries(defaults)) {
    const title = key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
    if (typeof val === "boolean") props[key] = { type: "boolean", title, default: val };
    else if (typeof val === "number" && Number.isInteger(val)) props[key] = { type: "integer", title, default: val, minimum: 0 };
    else if (typeof val === "number") props[key] = { type: "number", title, default: val };
    else props[key] = { type: "string", title, default: val ?? "" };
  }
  return { type: "object", properties: props };
}

// ── Node data shape ────────────────────────────────────────────────────

interface NodeData extends Record<string, unknown> {
  label: string;
  nodeType: "experiment" | "pipeline";
  refId: string;
  description?: string;
  params?: Record<string, unknown>;
}

// ── Palette item ───────────────────────────────────────────────────────

function PaletteItem({
  label,
  kind,
  description,
  refId,
  onDragStart,
}: {
  label: string;
  kind: "experiment" | "pipeline";
  description: string;
  refId: string;
  onDragStart: (kind: "experiment" | "pipeline", refId: string, label: string) => void;
}) {
  const color = kind === "experiment" ? "#7c3aed" : "#2563eb";
  return (
    <div
      draggable
      onDragStart={() => onDragStart(kind, refId, label)}
      title={description}
      style={{
        padding: "7px 10px",
        border: `1px solid ${color}30`,
        borderRadius: 6,
        marginBottom: 5,
        cursor: "grab",
        background: color + "08",
        fontSize: 12,
      }}
    >
      <div style={{ fontWeight: 600, color, fontSize: 12 }}>{label}</div>
      <div style={{ fontSize: 10, color: "#9ca3af", lineHeight: 1.3, marginTop: 2 }}>
        {description.slice(0, 60)}{description.length > 60 ? "…" : ""}
      </div>
    </div>
  );
}

// ── Inspector panel ────────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function ParamField({ fieldKey, def, value, onChange }: {
  fieldKey: string;
  def: Record<string, any>;
  value: unknown;
  onChange: (v: unknown) => void;
}) {
  const label = (def.title as string) ?? fieldKey;
  const desc = def.description as string | undefined;
  const type = def.type as string;

  const inputStyle: React.CSSProperties = {
    width: "100%", boxSizing: "border-box",
    padding: "4px 7px", border: "1px solid #d1d5db",
    borderRadius: 4, fontSize: 11, outline: "none",
    background: "#fff",
  };

  let control: React.ReactNode;
  if (type === "boolean") {
    control = (
      <div style={{ display: "flex", alignItems: "center", gap: 5, marginTop: 3 }}>
        <input type="checkbox" checked={!!value}
          onChange={(e) => onChange(e.target.checked)}
          style={{ cursor: "pointer", width: 14, height: 14 }} />
        <span style={{ fontSize: 11, color: "#374151" }}>{value ? "Yes" : "No"}</span>
      </div>
    );
  } else if (type === "integer" || type === "number") {
    control = (
      <input type="number" value={(value as number) ?? (def.default as number) ?? ""}
        step={type === "integer" ? 1 : "any"}
        min={def.minimum as number | undefined}
        max={def.maximum as number | undefined}
        onChange={(e) => onChange(
          type === "integer" ? (parseInt(e.target.value, 10) || 0) : (parseFloat(e.target.value) || 0)
        )}
        style={inputStyle} />
    );
  } else {
    control = (
      <input type="text" value={(value as string) ?? (def.default as string) ?? ""}
        onChange={(e) => onChange(e.target.value)}
        placeholder={def.default as string ?? ""}
        style={inputStyle} />
    );
  }

  return (
    <div style={{ marginBottom: 9 }}>
      <div style={{ fontSize: 11, fontWeight: 600, color: "#374151", marginBottom: 2 }}>{label}</div>
      {desc && <div style={{ fontSize: 10, color: "#9ca3af", marginBottom: 3, lineHeight: 1.4 }}>{desc}</div>}
      {control}
    </div>
  );
}

function Inspector({
  node,
  experiments,
  pipelines,
  onClose,
  onParamChange,
}: {
  node: Node<NodeData> | null;
  experiments: ExperimentMeta[];
  pipelines: CatalogPipeline[];
  onClose: () => void;
  onParamChange: (nodeId: string, params: Record<string, unknown>) => void;
}) {
  if (!node) return null;
  const color = node.data.nodeType === "experiment" ? "#7c3aed" : "#2563eb";
  const params = (node.data.params ?? {}) as Record<string, unknown>;

  // Resolve the params schema: use experiment's params_schema or derive from pipeline defaults
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let schema: Record<string, Record<string, any>> = {};
  if (node.data.nodeType === "experiment") {
    const exp = experiments.find((e) => e.id === node.data.refId);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    schema = ((exp?.params_schema as Record<string, any> | null)?.properties as Record<string, Record<string, any>> | undefined) ?? {};
  } else {
    const pipe = pipelines.find((p) => p.id === node.data.refId);
    if (pipe?.default_params && Object.keys(pipe.default_params).length > 0) {
      schema = schemaFromPipelineDefaults(pipe.default_params).properties ?? {};
    }
  }

  const handleChange = (key: string, val: unknown) => {
    onParamChange(node.id, { ...params, [key]: val });
  };

  return (
    <div style={{
      width: 260, borderLeft: "1px solid #e5e7eb", padding: "14px 16px",
      background: "#fafafa", overflowY: "auto", flexShrink: 0,
    }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
        <span style={{ fontSize: 12, fontWeight: 700, color }}>
          {node.data.nodeType === "experiment" ? "🧪 Experiment" : "⚙️ Pipeline"}
        </span>
        <button onClick={onClose} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 14, color: "#9ca3af" }}>✕</button>
      </div>

      {/* Node label */}
      <div style={{ fontSize: 13, fontWeight: 600, color: "#111827", marginBottom: 4 }}>{node.data.label}</div>
      {node.data.description && (
        <p style={{ fontSize: 11, color: "#6b7280", lineHeight: 1.45, margin: "0 0 10px" }}>
          {(node.data.description as string).slice(0, 140)}{(node.data.description as string).length > 140 ? "…" : ""}
        </p>
      )}

      {/* Editable params */}
      {Object.keys(schema).length > 0 ? (
        <div>
          <div style={{ fontSize: 10, fontWeight: 700, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8, borderTop: "1px solid #e5e7eb", paddingTop: 8 }}>
            Parameters
          </div>
          {Object.entries(schema).map(([key, def]) => (
            <ParamField
              key={key}
              fieldKey={key}
              def={def}
              value={params[key] ?? def.default}
              onChange={(v) => handleChange(key, v)}
            />
          ))}
          <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 6 }}>
            Params are saved with the study graph.
          </div>
        </div>
      ) : (
        <div style={{ fontSize: 11, color: "#d1d5db", fontStyle: "italic", marginTop: 6 }}>
          No configurable parameters.
        </div>
      )}

      {/* Meta */}
      <div style={{ marginTop: 12, paddingTop: 8, borderTop: "1px solid #f3f4f6" }}>
        <div style={{ fontSize: 10, color: "#d1d5db" }}>Node: <code style={{ fontSize: 10 }}>{node.id.slice(0, 16)}…</code></div>
        <div style={{ fontSize: 10, color: "#d1d5db", marginTop: 2 }}>Ref: <code style={{ fontSize: 10 }}>{node.data.refId}</code></div>
      </div>
    </div>
  );
}

// ── AI Design Study dialog ───────────────────────────────────────────────────

function DesignStudyDialog({
  onClose,
  onCreated,
}: {
  onClose: () => void;
  onCreated: (study: StudyResponse) => void;
}) {
  const [name, setName] = useState("");
  const [prompt, setPrompt] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const backdropRef = useRef<HTMLDivElement>(null);

  const handle = async () => {
    if (!name.trim() || !prompt.trim()) { setError("Name and description are required."); return; }
    setBusy(true); setError(null);
    try {
      const study = await generateStudy({ name: name.trim(), prompt: prompt.trim() });
      onCreated(study);
      onClose();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div
      ref={backdropRef}
      onClick={(ev) => { if (ev.target === backdropRef.current) onClose(); }}
      style={{
        position: "fixed", inset: 0, background: "rgba(0,0,0,0.45)",
        display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000,
      }}
    >
      <div style={{
        background: "#fff", borderRadius: 12, padding: "1.75rem 2rem",
        width: 520, maxWidth: "95vw", boxShadow: "0 20px 60px rgba(0,0,0,0.2)",
      }}>
        <h3 style={{ margin: "0 0 1.25rem", color: "#111827", fontSize: 16 }}>✨ AI Design Study</h3>
        <label style={dlgLabelStyle}>Study name</label>
        <input
          style={dlgInputStyle}
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g. Linguistic Entropy Deep-Dive"
          autoFocus
        />
        <label style={dlgLabelStyle}>Describe the research goal</label>
        <textarea
          style={{ ...dlgInputStyle, height: 90, resize: "vertical", fontFamily: "inherit" }}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Explore entropy metrics across different script corpora and compare with control languages…"
        />
        {error && (
          <div style={{ background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 6, padding: "8px 12px", marginBottom: 12, fontSize: 12, color: "#b91c1c" }}>
            {error}
          </div>
        )}
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 8 }}>
          <button onClick={onClose} style={dlgBtnSecondary} disabled={busy}>Cancel</button>
          <button onClick={() => void handle()} style={dlgBtnPrimary} disabled={busy}>
            {busy ? "Designing…" : "Design Study"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Study Summary panel ──────────────────────────────────────────────────

function StudySummaryPanel({ summary, onClose }: { summary: AISummaryResult; onClose: () => void }) {
  return (
    <div style={{ marginTop: 8, border: "1px solid #a78bfa", borderRadius: 8, overflow: "hidden", background: "#faf5ff" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#7c3aed", padding: "8px 14px" }}>
        <span style={{ color: "#fff", fontWeight: 700, fontSize: 13 }}>✨ AI Study Summary</span>
        <button onClick={onClose} style={{ border: "none", background: "none", color: "rgba(255,255,255,0.8)", cursor: "pointer", fontSize: 16, padding: 0 }}>✕</button>
      </div>
      <div style={{ padding: "14px 16px", display: "flex", flexDirection: "column", gap: 12 }}>
        <div>
          <div style={sectionLabel}>Abstract</div>
          <p style={{ margin: 0, fontSize: 13, lineHeight: 1.6, color: "#1f2937" }}>{summary.abstract}</p>
        </div>
        {summary.hypothesis && (
          <div>
            <div style={sectionLabel}>Hypothesis</div>
            <p style={{ margin: 0, fontSize: 13, lineHeight: 1.6, color: "#374151", fontStyle: "italic" }}>{summary.hypothesis}</p>
          </div>
        )}
        {(summary.highlights?.length ?? 0) > 0 && (
          <div>
            <div style={sectionLabel}>Key Highlights</div>
            <ul style={{ margin: 0, paddingLeft: 20, display: "flex", flexDirection: "column", gap: 3 }}>
              {summary.highlights.map((h, i) => <li key={i} style={{ fontSize: 13, lineHeight: 1.5, color: "#1f2937" }}>{h}</li>)}
            </ul>
          </div>
        )}
        {summary.insights && (
          <div>
            <div style={sectionLabel}>Insights</div>
            <p style={{ margin: 0, fontSize: 13, lineHeight: 1.6, color: "#374151" }}>{summary.insights}</p>
          </div>
        )}
        {(summary.next_steps?.length ?? 0) > 0 && (
          <div>
            <div style={sectionLabel}>Next Steps</div>
            <ul style={{ margin: 0, paddingLeft: 20, display: "flex", flexDirection: "column", gap: 3 }}>
              {summary.next_steps.map((s, i) => <li key={i} style={{ fontSize: 13, lineHeight: 1.5, color: "#374151" }}>{s}</li>)}
            </ul>
          </div>
        )}
        {(summary.suggested_actions?.length ?? 0) > 0 && (
          <div>
            <div style={sectionLabel}>Suggested Actions</div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              {summary.suggested_actions.map((a, i) => (
                <button key={i} title={a.hint} style={{ padding: "6px 14px", borderRadius: 6, border: "1px solid #7c3aed", background: "#7c3aed", color: "#fff", cursor: "pointer", fontSize: 12, fontWeight: 600 }}>
                  {a.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const sectionLabel: React.CSSProperties = {
  fontSize: 11, fontWeight: 700, color: "#7c3aed",
  textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4,
};

// ── Main StudyBuilderView ───────────────────────────────────────────────────────────

let _nodeIdCounter = 0;
function nextNodeId() { return `node_${Date.now()}_${_nodeIdCounter++}`; }

export function StudyBuilderView() {
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [pipelines, setPipelines] = useState<CatalogPipeline[]>([]);
  const [studies, setStudies] = useState<StudyResponse[]>([]);
  const [activeStudy, setActiveStudy] = useState<StudyResponse | null>(null);
  const [nodes, setNodes] = useState<Node<NodeData>[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedNode, setSelectedNode] = useState<Node<NodeData> | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [runResult, setRunResult] = useState<StudyRunResult | null>(null);
  const [runError, setRunError] = useState<string | null>(null);
  const [newStudyName, setNewStudyName] = useState("");
  const [palFilter, setPalFilter] = useState<"all" | "experiment" | "pipeline">("all");
  const [palSearch, setPalSearch] = useState("");
  const [showDesign, setShowDesign] = useState(false);
  const { openChat } = useAIChat();
  const [studySummarizing, setStudySummarizing] = useState(false);
  const [studySummary, setStudySummary] = useState<AISummaryResult | null>(null);
  const [studySummaryError, setStudySummaryError] = useState<string | null>(null);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);

  // dragged item ref (set in dragStart, read in drop)
  const draggedRef = useRef<{ kind: "experiment" | "pipeline"; refId: string; label: string } | null>(null);

  // Load palette + studies
  useEffect(() => {
    void listExperiments().then(setExperiments).catch(() => {});
    void getPipelineCatalog().then(setPipelines).catch(() => {});
    void listStudies().then(setStudies).catch(() => {});
  }, []);

  const loadStudy = (s: StudyResponse) => {
    setActiveStudy(s);
    setSelectedNode(null);
    const g = s.graph;
    setNodes(
      (g.nodes ?? []).map((n) => ({
        id: n.id,
        type: "default",
        position: n.position ?? { x: 100, y: 100 },
        data: {
          label: n.label,
          nodeType: n.type as "experiment" | "pipeline",
          refId: n.ref_id,
          params: n.params ?? {},
        } as NodeData,
      }))
    );
    setEdges(
      (g.edges ?? []).map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
      }))
    );
  };

  const handleNewStudy = async () => {
    if (!newStudyName.trim()) return;
    const s = await createStudy({ name: newStudyName.trim() });
    setStudies((prev) => [s, ...prev]);
    setNewStudyName("");
    loadStudy(s);
  };

  const handleSave = async () => {
    if (!activeStudy) return;
    setSaving(true);
    try {
      const graph: StudyGraph = {
        nodes: nodes.map((n) => ({
          id: n.id,
          type: n.data.nodeType,
          ref_id: n.data.refId,
          label: n.data.label,
          params: (n.data.params ?? {}) as Record<string, unknown>,
          position: n.position,
        })),
        edges: edges.map((e) => ({
          id: e.id,
          source: e.source,
          target: e.target,
        })),
      };
      const updated = await updateStudy(activeStudy.id, { graph });
      setActiveStudy(updated);
      setStudies((prev) => prev.map((s) => s.id === updated.id ? updated : s));
      setSaveMsg("Saved");
      setTimeout(() => setSaveMsg(null), 2000);
    } catch {
      setSaveMsg("Save failed");
    } finally {
      setSaving(false);
    }
  };

  const handleSummarizeStudy = async () => {
    if (!activeStudy) return;
    setStudySummarizing(true);
    setStudySummaryError(null);
    setStudySummary(null);
    try {
      const result = await summarizeStudy(activeStudy.id);
      setStudySummary(result);
    } catch (e: unknown) {
      setStudySummaryError(e instanceof Error ? e.message : String(e));
    } finally {
      setStudySummarizing(false);
    }
  };

  const handleRun = async () => {
    if (!activeStudy) return;
    setRunning(true);
    setRunResult(null);
    setRunError(null);
    try {
      const res = await runStudy(activeStudy.id);
      setRunResult(res);
    } catch (e: unknown) {
      setRunError(e instanceof Error ? e.message : String(e));
    } finally {
      setRunning(false);
    }
  };

  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  const handleDeleteStudy = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (deleteConfirm !== id) {
      setDeleteConfirm(id);
      setTimeout(() => setDeleteConfirm(null), 3000); // auto-cancel after 3s
      return;
    }
    setDeleteConfirm(null);
    await deleteStudy(id);
    setStudies((prev) => prev.filter((s) => s.id !== id));
    if (activeStudy?.id === id) {
      setActiveStudy(null);
      setNodes([]);
      setEdges([]);
      setSelectedNode(null);
    }
  };

  // React Flow handlers
  const onNodesChange = useCallback(
    (changes: NodeChange[]) => setNodes((n) => applyNodeChanges(changes, n) as Node<NodeData>[]),
    []
  );
  const onEdgesChange = useCallback(
    (changes: EdgeChange[]) => setEdges((e) => applyEdgeChanges(changes, e)),
    []
  );
  const onConnect = useCallback(
    (conn: Connection) => setEdges((e) => addEdge(conn, e)),
    []
  );
  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => setSelectedNode(node as Node<NodeData>),
    []
  );
  const onPaneClick = useCallback(() => setSelectedNode(null), []);

  // Drop from palette onto canvas
  const onDrop = useCallback(
    (ev: React.DragEvent<HTMLDivElement>) => {
      ev.preventDefault();
      if (!draggedRef.current || !reactFlowWrapper.current) return;
      const rect = reactFlowWrapper.current.getBoundingClientRect();
      const position = {
        x: ev.clientX - rect.left - 60,
        y: ev.clientY - rect.top - 20,
      };
      const { kind, refId, label } = draggedRef.current;
      const desc = kind === "experiment"
        ? (experiments.find((e) => e.id === refId)?.description ?? "")
        : (pipelines.find((p) => p.id === refId)?.description ?? "");
      const newNode: Node<NodeData> = {
        id: nextNodeId(),
        type: "default",
        position,
        data: { label, nodeType: kind, refId, description: desc, params: {} },
      };
      setNodes((n) => [...n, newNode]);
      draggedRef.current = null;
    },
    [experiments, pipelines]
  );
  const onDragOver = (ev: React.DragEvent<HTMLDivElement>) => {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
  };
  const handleDragStart = (
    kind: "experiment" | "pipeline",
    refId: string,
    label: string
  ) => {
    draggedRef.current = { kind, refId, label };
  };

  // ── Palette items ──────────────────────────────────────────────────
  const expItems = experiments.filter(
    (e) => palSearch === "" || e.name.toLowerCase().includes(palSearch.toLowerCase())
  );
  const pipItems = pipelines.filter(
    (p) => palSearch === "" || (p.label ?? p.id).toLowerCase().includes(palSearch.toLowerCase())
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", minHeight: 660 }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <h2 style={{ margin: 0 }}>Study Builder</h2>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          {activeStudy && (
            <span style={{ fontSize: 12, color: "#6b7280" }}>
              {activeStudy.name}
            </span>
          )}
          {saveMsg && (
            <span style={{ fontSize: 12, color: saveMsg === "Saved" ? "#16a34a" : "#b91c1c", fontWeight: 600 }}>
              {saveMsg}
            </span>
          )}
          <button
            onClick={() => void handleSummarizeStudy()}
            disabled={studySummarizing || !activeStudy}
            title="AI summary of this study"
            style={{
              ...btnPrimary,
              background: studySummarizing ? "#f3e8ff" : "#f3f4f6",
              color: studySummarizing ? "#7c3aed" : "#374151",
              marginRight: 0,
            }}
          >
            {studySummarizing ? "✨…" : "✨ AI"}
          </button>
          <button
            onClick={() => openChat({
              contextType: activeStudy ? "study" : "",
              contextId: activeStudy?.id ?? "",
              contextLabel: activeStudy?.name,
              initialPrompt: activeStudy
                ? `Please help me improve this study called "${activeStudy.name}". Suggest additional experiments, identify gaps, and describe what insights we could gain.`
                : "I want to design a new research study for Glossa Lab. Please help me choose a good name and a clear research goal, then I'll describe what I want to investigate.",
            })}
            title="AI Design Study — opens AI Chat with study context"
            style={{ ...btnPrimary, background: "#7c3aed" }}
          >
            ✨ Design
          </button>
          <button
            onClick={() => void handleRun()}
            disabled={running || !activeStudy || !nodes.length}
            title="Run all experiment nodes in topological order"
            style={{
              ...btnPrimary,
              background: running ? "#7c3aed" : "#16a34a",
            }}
          >
            {running ? "Running…" : "▶ Run Study"}
          </button>
          <button
            onClick={handleSave}
            disabled={saving || !activeStudy}
            style={btnPrimary}
          >
            {saving ? "Saving…" : "💾 Save"}
          </button>
        </div>
      </div>

      <div style={{ display: "flex", gap: 0, border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden", height: 560 }}>
        {/* ── Left: study list + palette ── */}
        <div style={{ width: 220, borderRight: "1px solid #e5e7eb", display: "flex", flexDirection: "column", background: "#fafafa" }}>
          {/* Studies list */}
          <div style={{ padding: "10px 10px 8px", borderBottom: "1px solid #e5e7eb" }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: "#6b7280", textTransform: "uppercase", marginBottom: 6 }}>Studies</div>
            {studies.map((s) => (
              <div
                key={s.id}
                style={{
                  display: "flex", justifyContent: "space-between", alignItems: "center",
                  padding: "5px 7px", borderRadius: 5, marginBottom: 2, cursor: "pointer",
                  background: activeStudy?.id === s.id ? "#1e3a5f" : "transparent",
                  color: activeStudy?.id === s.id ? "#fff" : "#374151",
                }}
                onClick={() => loadStudy(s)}
              >
                <span style={{ fontSize: 12, fontWeight: 500, flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{s.name}</span>
                <button
                  onClick={(e) => void handleDeleteStudy(s.id, e)}
                  style={{
                    border: deleteConfirm === s.id ? "1px solid #fca5a5" : "none",
                    background: deleteConfirm === s.id ? "#fef2f2" : "none",
                    color: deleteConfirm === s.id ? "#b91c1c" : (activeStudy?.id === s.id ? "#fff" : "#9ca3af"),
                    cursor: "pointer", fontSize: 11, borderRadius: 3, padding: "0 4px",
                  }}
                  title={deleteConfirm === s.id ? "Click again to confirm" : "Delete study"}
                >{deleteConfirm === s.id ? "Sure?" : "✕"}</button>
              </div>
            ))}
            <div style={{ display: "flex", gap: 5, marginTop: 6 }}>
              <input
                value={newStudyName}
                onChange={(e) => setNewStudyName(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter") void handleNewStudy(); }}
                placeholder="New study name"
                style={{ flex: 1, padding: "4px 6px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, outline: "none" }}
              />
              <button onClick={() => void handleNewStudy()} style={{ ...btnPrimary, padding: "4px 8px", fontSize: 11 }}>+</button>
            </div>
          </div>

          {/* Palette */}
          <div style={{ flex: 1, overflowY: "auto", padding: "8px 10px" }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: "#6b7280", textTransform: "uppercase", marginBottom: 6 }}>Palette</div>
            <input
              value={palSearch}
              onChange={(e) => setPalSearch(e.target.value)}
              placeholder="Search…"
              style={{ width: "100%", boxSizing: "border-box", padding: "4px 7px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, marginBottom: 6, outline: "none" }}
            />
            <div style={{ display: "flex", gap: 3, marginBottom: 8, flexWrap: "wrap" }}>
              {(["all", "experiment", "pipeline"] as const).map((f) => (
                <button
                  key={f}
                  onClick={() => setPalFilter(f)}
                  style={{
                    padding: "2px 8px", border: "1px solid", borderRadius: 10, cursor: "pointer",
                    fontSize: 10, fontWeight: palFilter === f ? 700 : 400,
                    background: palFilter === f ? "#1e3a5f" : "#fff",
                    borderColor: palFilter === f ? "#1e3a5f" : "#d1d5db",
                    color: palFilter === f ? "#fff" : "#374151",
                  }}
                >{f}</button>
              ))}
            </div>

            {(palFilter === "all" || palFilter === "experiment") && expItems.length > 0 && (
              <>
                <div style={{ fontSize: 10, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Experiments</div>
                {expItems.map((e) => (
                  <PaletteItem
                    key={e.id}
                    label={e.name}
                    kind="experiment"
                    description={e.description}
                    refId={e.id}
                    onDragStart={handleDragStart}
                  />
                ))}
              </>
            )}

            {(palFilter === "all" || palFilter === "pipeline") && pipItems.length > 0 && (
              <>
                <div style={{ fontSize: 10, fontWeight: 700, color: "#2563eb", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4, marginTop: 8 }}>Pipelines</div>
                {pipItems.map((p) => (
                  <PaletteItem
                    key={p.id}
                    label={p.label ?? p.id}
                    kind="pipeline"
                    description={p.description}
                    refId={p.id}
                    onDragStart={handleDragStart}
                  />
                ))}
              </>
            )}
          </div>
        </div>

        {/* ── Center: React Flow canvas ── */}
        <div
          ref={reactFlowWrapper}
          style={{ flex: 1, position: "relative" }}
          onDrop={onDrop}
          onDragOver={onDragOver}
        >
          {!activeStudy && (
            <div style={{
              position: "absolute", inset: 0, display: "flex", alignItems: "center",
              justifyContent: "center", flexDirection: "column", gap: 8,
              color: "#9ca3af", fontSize: 14, zIndex: 10, pointerEvents: "none",
            }}>
              <div style={{ fontSize: 32 }}>📐</div>
              <div>Create or select a study to start building</div>
              <div style={{ fontSize: 12 }}>Drag experiments and pipelines from the palette onto the canvas</div>
            </div>
          )}
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            onPaneClick={onPaneClick}
            fitView
            proOptions={{ hideAttribution: true }}
            style={{ background: "#f8fafc" }}
          >
            <Controls />
            <MiniMap
              style={{ background: "#f3f4f6" }}
              nodeColor={(n) => {
                const d = n.data as NodeData | undefined;
                return d?.nodeType === "experiment" ? "#7c3aed40" : "#2563eb40";
              }}
            />
            <Background variant={BackgroundVariant.Dots} gap={20} size={1} color="#d1d5db" />
          </ReactFlow>
        </div>

        {/* ── Right: Inspector ── */}
        <Inspector
          node={selectedNode}
          experiments={experiments}
          pipelines={pipelines}
          onClose={() => setSelectedNode(null)}
          onParamChange={(nodeId, newParams) => {
            setNodes((prev) =>
              prev.map((n) =>
                n.id === nodeId ? { ...n, data: { ...n.data, params: newParams } } : n
              )
            );
            // Keep selectedNode in sync so the form re-renders immediately
            setSelectedNode((prev) =>
              prev?.id === nodeId ? { ...prev, data: { ...prev.data, params: newParams } } : prev
            );
          }}
        />
      </div>

      {runError && (
        <div style={{
          marginTop: 8, padding: "10px 14px",
          background: "#fef2f2", border: "1px solid #fca5a5",
          borderRadius: 6, fontSize: 12, color: "#b91c1c",
        }}>
          Run failed: {runError}
        </div>
      )}

      {runResult && (
        <div style={{
          marginTop: 8, border: "1px solid #e5e7eb",
          borderRadius: 8, overflow: "hidden",
        }}>
          <div style={{
            background: "#f0fdf4", padding: "8px 14px",
            borderBottom: "1px solid #e5e7eb",
            display: "flex", gap: 16, alignItems: "center",
          }}>
            <span style={{ fontSize: 12, fontWeight: 700, color: "#15803d" }}>Study Run Results</span>
            <span style={{ fontSize: 11, color: "#6b7280" }}>
              {runResult.completed} completed · {runResult.skipped} skipped · {runResult.errors} errors
              {" "}· {runResult.node_count} total nodes
            </span>
            <button
              onClick={() => setRunResult(null)}
              style={{ marginLeft: "auto", border: "none", background: "none", cursor: "pointer", fontSize: 12, color: "#9ca3af" }}
            >× dismiss</button>
          </div>
          <div style={{ overflowX: "auto" }}>
            {Object.entries(runResult.results).map(([nodeId, res]) => {
              const statusColor = res.status === "complete" ? "#16a34a" : res.status === "error" ? "#b91c1c" : "#d97706";
              const statusBg = res.status === "complete" ? "#f0fdf4" : res.status === "error" ? "#fef2f2" : "#fef3c7";
              // Find the node label from the canvas
              const nodeLabel = nodes.find((n) => n.id === nodeId)?.data?.label as string | undefined;
              return (
                <div key={nodeId} style={{
                  display: "flex", alignItems: "flex-start", gap: 10,
                  padding: "8px 14px", borderBottom: "1px solid #f3f4f6",
                }}>
                  <span style={{
                    fontSize: 10, padding: "2px 7px", borderRadius: 8,
                    background: statusBg, color: statusColor, fontWeight: 700,
                    whiteSpace: "nowrap", marginTop: 1,
                  }}>
                    {res.status}
                  </span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 2 }}>
                      {nodeLabel ?? nodeId}
                    </div>
                    {res.reason && (
                      <div style={{ fontSize: 11, color: "#6b7280" }}>{res.reason}</div>
                    )}
                    {res.status === "complete" && res.result && (
                      <pre style={{
                        background: "#1e293b", color: "#e2e8f0",
                        margin: "4px 0 0", padding: "6px 10px",
                        fontSize: 10, fontFamily: "monospace",
                        borderRadius: 4, overflowX: "auto",
                        maxHeight: 120,
                      }}>
                        {JSON.stringify(res.result, null, 2)}
                      </pre>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {studySummaryError && (
        <div style={{ marginTop: 8, padding: "8px 12px", background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 6, fontSize: 12, color: "#b91c1c" }}>
          AI error: {studySummaryError}
        </div>
      )}

      {studySummary && (
        <StudySummaryPanel summary={studySummary} onClose={() => setStudySummary(null)} />
      )}

      <p style={{ fontSize: 12, color: "#9ca3af", marginTop: 8, marginBottom: 0 }}>
        Drag items from the palette onto the canvas. Connect nodes by dragging between handles. Click a node to inspect it. Save stores the graph to the backend.
      </p>

      {showDesign && (
        <DesignStudyDialog
          onClose={() => setShowDesign(false)}
          onCreated={(study) => {
            setStudies((prev) => [study, ...prev]);
            loadStudy(study);
          }}
        />
      )}
    </div>
  );
}

// ── Shared styles ──────────────────────────────────────────────────

const btnPrimary: React.CSSProperties = {
  padding: "6px 14px", border: "none", borderRadius: 6,
  cursor: "pointer", fontSize: 12, fontWeight: 600,
  background: "#1e3a5f", color: "#fff",
};

const dlgInputStyle: React.CSSProperties = {
  display: "block", width: "100%", boxSizing: "border-box",
  padding: "7px 10px", border: "1px solid #d1d5db", borderRadius: 6,
  fontSize: 13, marginBottom: 12, outline: "none",
};

const dlgLabelStyle: React.CSSProperties = {
  display: "block", fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 4,
};

const dlgBtnPrimary: React.CSSProperties = {
  padding: "7px 18px", border: "none", borderRadius: 6,
  cursor: "pointer", fontSize: 13, fontWeight: 600,
  background: "#7c3aed", color: "#fff",
};

const dlgBtnSecondary: React.CSSProperties = {
  padding: "7px 18px", border: "1px solid #d1d5db", borderRadius: 6,
  cursor: "pointer", fontSize: 13, fontWeight: 400,
  background: "#fff", color: "#374151",
};
