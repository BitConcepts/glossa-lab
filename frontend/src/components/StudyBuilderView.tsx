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
  listExperiments,
  listStudies,
  getPipelineCatalog,
  runStudy,
  updateStudy,
  type ExperimentMeta,
  type CatalogPipeline,
  type StudyResponse,
  type StudyGraph,
  type StudyRunResult,
} from "../api";

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

function Inspector({
  node,
  onClose,
}: {
  node: Node<NodeData> | null;
  onClose: () => void;
}) {
  if (!node) return null;
  const color = node.data.nodeType === "experiment" ? "#7c3aed" : "#2563eb";
  return (
    <div style={{
      width: 240, borderLeft: "1px solid #e5e7eb", padding: "14px 16px",
      background: "#fafafa", overflowY: "auto", flexShrink: 0,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <span style={{ fontSize: 12, fontWeight: 700, color }}>
          {node.data.nodeType === "experiment" ? "Experiment" : "Pipeline"}
        </span>
        <button onClick={onClose} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 14, color: "#9ca3af" }}>✕</button>
      </div>
      <div style={{ fontSize: 13, fontWeight: 600, color: "#111827", marginBottom: 6 }}>{node.data.label}</div>
      {node.data.description && (
        <p style={{ fontSize: 12, color: "#6b7280", lineHeight: 1.5, margin: "0 0 10px" }}>
          {node.data.description}
        </p>
      )}
      <div style={{ fontSize: 11, color: "#9ca3af" }}>
        Node ID: <code style={{ fontSize: 11 }}>{node.id}</code>
      </div>
      <div style={{ fontSize: 11, color: "#9ca3af", marginTop: 4 }}>
        Ref: <code style={{ fontSize: 11 }}>{node.data.refId}</code>
      </div>
    </div>
  );
}

// ── Main StudyBuilderView ──────────────────────────────────────────────

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

  const handleDeleteStudy = async (id: string) => {
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
            onClick={() => void handleRun()}
            disabled={running || !activeStudy || !nodes.length}
            title="Run all experiment nodes in topological order"
            style={{
              ...btnPrimary,
              background: running ? "#7c3aed" : "#16a34a",
              marginRight: 4,
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
                  onClick={(e) => { e.stopPropagation(); void handleDeleteStudy(s.id); }}
                  style={{ border: "none", background: "none", cursor: "pointer", fontSize: 11, color: activeStudy?.id === s.id ? "#fff" : "#9ca3af", padding: "0 2px" }}
                  title="Delete study"
                >✕</button>
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
          onClose={() => setSelectedNode(null)}
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

      <p style={{ fontSize: 12, color: "#9ca3af", marginTop: 8, marginBottom: 0 }}>
        Drag items from the palette onto the canvas. Connect nodes by dragging between handles. Click a node to inspect it. Save stores the graph to the backend.
      </p>
    </div>
  );
}

// ── Shared styles ──────────────────────────────────────────────────────

const btnPrimary: React.CSSProperties = {
  padding: "6px 14px", border: "none", borderRadius: 6,
  cursor: "pointer", fontSize: 12, fontWeight: 600,
  background: "#1e3a5f", color: "#fff",
};
