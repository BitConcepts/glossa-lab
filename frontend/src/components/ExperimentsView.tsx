/**
 * Experiments View — gallery of graph experiments.
 *
 * Every experiment is a composable graph built in the Experiment Builder.
 * Actions here (Open, Duplicate, Delete, New) all navigate to the
 * Experiment Builder so users work visually, not via code.
 *
 * To generate experiment structure using AI:
 *   → Open an experiment in the Builder → use AI Chat ✨ to add/suggest nodes.
 */

import { useEffect, useState, useCallback } from "react";
import {
  createGraphExperiment,
  deleteGraphExperiment,
  getGraphExperiment,
  listGraphExperiments,
  listJobs,
  runGraphExperiment,
  type GraphExperimentMeta,
} from "../api";
import { useAIChat } from "../hooks/useAIChat";
import { fmtDateTimeCompact } from "../dateFormat";

// ── Helpers ─────────────────────────────────────────────────────────────────

/** Navigate to Experiment Builder and set a pending action via localStorage. */
function openInBuilder(action: "load" | "new" | "dup", id?: string) {
  localStorage.setItem(
    "glossa_exp_builder_open",
    JSON.stringify({ action, id: id ?? null })
  );
  window.dispatchEvent(
    new CustomEvent("glossa:navigate", { detail: { view: "exp-builder" } })
  );
}

// ── Experiment card ──────────────────────────────────────────────────────────

interface CardProps {
  exp: GraphExperimentMeta;
  onDeleted: (id: string) => void;
  onRefresh: () => void;
  lastRun?: string;
}

function ExpCard({ exp, onDeleted, onRefresh, lastRun }: CardProps) {
  const [running, setRunning] = useState(false);
  const [runResult, setRunResult] = useState<string | null>(null);
  const [runError, setRunError] = useState<string | null>(null);
  const [confirmDel, setConfirmDel] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [duping, setDuping] = useState(false);
  const { openChat } = useAIChat();

  const handleOpen = () => openInBuilder("load", exp.id);

  const handleRun = async () => {
    setRunning(true); setRunResult(null); setRunError(null);
    try {
      const r = await runGraphExperiment(exp.id);
      const keys = Object.keys(r.result ?? {}).slice(0, 4).join(", ");
      setRunResult(r.status === "complete" ? `✓ ${keys || "done"}` : r.status);
    } catch (e) { setRunError(e instanceof Error ? e.message : "run failed"); }
    finally { setRunning(false); }
  };

  const handleDup = async () => {
    setDuping(true);
    try {
      const d = await getGraphExperiment(exp.id);
      // Create copy then open in builder
      const copy = await createGraphExperiment({
        ...d, id: undefined, name: `${d.name} (copy)`,
      } as Parameters<typeof createGraphExperiment>[0]);
      onRefresh();
      openInBuilder("load", copy.id);
    } catch { /* ignore */ }
    finally { setDuping(false); }
  };

  const handleDelete = async () => {
    if (!confirmDel) { setConfirmDel(true); setTimeout(() => setConfirmDel(false), 3000); return; }
    setDeleting(true);
    try { await deleteGraphExperiment(exp.id); onDeleted(exp.id); }
    catch { setDeleting(false); setConfirmDel(false); }
  };

  return (
    <div style={{
      border: "1px solid #e5e7eb", borderRadius: 10, overflow: "hidden",
      boxShadow: "0 1px 4px rgba(0,0,0,0.04)", background: "#fff",
      transition: "box-shadow 0.15s",
    }}
      onMouseEnter={e => { (e.currentTarget as HTMLElement).style.boxShadow = "0 4px 16px rgba(0,0,0,0.1)"; }}
      onMouseLeave={e => { (e.currentTarget as HTMLElement).style.boxShadow = "0 1px 4px rgba(0,0,0,0.04)"; }}
    >
      {/* Left accent bar */}
      <div style={{ height: 4, background: "linear-gradient(90deg, #7c3aed, #4f46e5)" }} />

      <div style={{ padding: "12px 14px" }}>
        {/* Name + meta */}
        <div style={{ display: "flex", alignItems: "flex-start", gap: 10, marginBottom: 6 }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#111827", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {exp.name}
            </div>
            {exp.description && (
              <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2, lineHeight: 1.4,
                overflow: "hidden", textOverflow: "ellipsis",
                display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" }}>
                {exp.description}
              </div>
            )}
          </div>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 3, flexShrink: 0 }}>
            <span style={{ fontSize: 10, padding: "2px 6px", borderRadius: 8, background: "#7c3aed20", color: "#7c3aed", fontWeight: 600, whiteSpace: "nowrap" }}>
              {exp.node_count}n · {exp.edge_count}e
            </span>
            {lastRun && (
              <span style={{ fontSize: 10, color: "#9ca3af", whiteSpace: "nowrap" }} title={lastRun}>
                🕐 {fmtDateTimeCompact(lastRun)}
              </span>
            )}
          </div>
        </div>

        {/* Run result */}
        {(runResult || runError) && (
          <div style={{ fontSize: 11, padding: "4px 8px", borderRadius: 5, marginBottom: 8,
            background: runError ? "#fef2f2" : "#f0fdf4",
            color: runError ? "#b91c1c" : "#15803d",
            border: `1px solid ${runError ? "#fca5a5" : "#86efac"}` }}>
            {runError ?? runResult}
          </div>
        )}

        {/* Actions */}
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginTop: 4 }}>
          <button onClick={handleOpen} style={btnPrimary}>
            🔀 Open in Builder
          </button>
          <button onClick={() => void handleRun()} disabled={running}
            style={{ ...btnSecondary, opacity: running ? 0.5 : 1, cursor: running ? "not-allowed" : "pointer" }}>
            {running ? "⏳" : "▶ Run"}
          </button>
          <button onClick={() => openChat({ contextType: "", contextId: "", initialPrompt: `Help me improve the experiment "${exp.name}": ${exp.description ?? ""}` })}
            style={btnSecondary} title="Open AI Chat for this experiment">
            ✨ AI
          </button>
          <button onClick={() => void handleDup()} disabled={duping} style={btnSecondary} title="Duplicate">
            {duping ? "…" : "⎘ Dup"}
          </button>
          <button onClick={() => void handleDelete()} disabled={deleting}
            style={{ ...btnSecondary, background: confirmDel ? "#fef2f2" : undefined, color: confirmDel ? "#b91c1c" : undefined, borderColor: confirmDel ? "#fca5a5" : undefined }}
            title={confirmDel ? "Click again to confirm" : "Delete"}>
            {deleting ? "…" : confirmDel ? "Sure?" : "🗑"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Main view ────────────────────────────────────────────────────────────────

type SortMode = "name_asc" | "name_desc" | "nodes" | "last_run";

export function ExperimentsView() {
  const [exps, setExps] = useState<GraphExperimentMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<SortMode>("last_run");
  // map exp_id → ISO timestamp of most recent completed job
  const [lastRunMap, setLastRunMap] = useState<Record<string, string>>({});

  const load = useCallback(async () => {
    setError(null); setLoading(true);
    try {
      const [expList, jobs] = await Promise.all([listGraphExperiments(), listJobs()]);
      setExps(expList);
      // build last-run map from jobs
      const m: Record<string, string> = {};
      for (const j of jobs) {
        const eid = (j.params as Record<string, unknown>)?.exp_id as string | undefined;
        if (eid && j.status === "completed" && j.created_at) {
          if (!m[eid] || j.created_at > m[eid]) m[eid] = j.created_at;
        }
      }
      setLastRunMap(m);
    }
    catch (e) { setError(e instanceof Error ? e.message : "Failed to load experiments"); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { void load(); }, [load]);

  const filtered = exps
    .filter(e =>
      !search || e.name.toLowerCase().includes(search.toLowerCase()) ||
                 e.description.toLowerCase().includes(search.toLowerCase())
    )
    .sort((a, b) => {
      if (sort === "name_asc")  return a.name.localeCompare(b.name);
      if (sort === "name_desc") return b.name.localeCompare(a.name);
      if (sort === "nodes")     return (b.node_count ?? 0) - (a.node_count ?? 0);
      // last_run: experiments with a run come first (newest first), then alphabetically
      const ra = lastRunMap[a.id] ?? "";
      const rb = lastRunMap[b.id] ?? "";
      if (ra && rb) return rb.localeCompare(ra);
      if (ra) return -1;
      if (rb) return 1;
      return a.name.localeCompare(b.name);
    });

  const handleDeleted = useCallback((id: string) => setExps(prev => prev.filter(e => e.id !== id)), []);

  return (
    <div>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
        <h2 style={{ margin: 0, fontSize: 20, color: "#111827" }}>Experiments</h2>
        <div style={{ display: "flex", gap: 6 }}>
          <button onClick={load} style={{ ...btnSecondary, fontSize: 12 }} title="Reload from server">
            ⟳ Reload
          </button>
          <button
            onClick={() => openInBuilder("new")}
            style={{ padding: "6px 14px", border: "none", borderRadius: 6, cursor: "pointer", fontSize: 12, fontWeight: 700, background: "linear-gradient(135deg, #7c3aed, #4f46e5)", color: "#fff" }}
          >
            + New Experiment
          </button>
        </div>
      </div>

      {/* Description + sort controls */}
      <div style={{ display: "flex", alignItems: "flex-start", gap: 10, marginBottom: 14, flexWrap: "wrap" }}>
        <div style={{ flex: 1, fontSize: 13, color: "#6b7280", lineHeight: 1.6, background: "#f8fafc", border: "1px solid #e5e7eb", borderRadius: 8, padding: "10px 14px", minWidth: 200 }}>
          <strong style={{ color: "#374151" }}>Every experiment is a composable graph</strong> built in the{" "}
          <button onClick={() => openInBuilder("new")} style={{ background: "none", border: "none", color: "#7c3aed", cursor: "pointer", fontWeight: 600, padding: 0, fontSize: 13 }}>
            🔀 Experiment Builder
          </button>
          {" "}— drag nodes, wire ports, let <strong>AI Chat ✨</strong> suggest improvements.
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 6, flexShrink: 0 }}>
          <span style={{ fontSize: 11, color: "#9ca3af", whiteSpace: "nowrap" }}>Sort by</span>
          {(["last_run", "name_asc", "name_desc", "nodes"] as SortMode[]).map(s => (
            <button key={s} onClick={() => setSort(s)}
              style={{ padding: "4px 9px", border: `1px solid ${sort === s ? "#7c3aed" : "#e5e7eb"}`,
                borderRadius: 5, cursor: "pointer", fontSize: 11, fontWeight: sort === s ? 700 : 400,
                background: sort === s ? "#ede9fe" : "#f9fafb",
                color: sort === s ? "#6d28d9" : "#374151" }}>
              {s === "last_run" ? "🕐 Last run" : s === "name_asc" ? "A→Z" : s === "name_desc" ? "Z→A" : "Nodes"}
            </button>
          ))}
        </div>
      </div>

      {/* Search */}
      <input
        value={search}
        onChange={e => setSearch(e.target.value)}
        placeholder={`Search ${exps.length} experiment${exps.length !== 1 ? "s" : ""}…`}
        style={{ width: "100%", boxSizing: "border-box", padding: "8px 12px", border: "1px solid #d1d5db", borderRadius: 7, fontSize: 13, marginBottom: 14, outline: "none" }}
      />

      {loading && <div style={{ color: "#6b7280", fontSize: 13 }}>Loading experiments…</div>}
      {error && (
        <div style={{ background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 7, padding: "10px 14px", fontSize: 13, color: "#b91c1c", marginBottom: 12 }}>
          {error}
        </div>
      )}

      {!loading && !error && filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: "2rem", color: "#9ca3af" }}>
          <div style={{ fontSize: 32, marginBottom: 8 }}>🔀</div>
          <div style={{ fontSize: 14, fontWeight: 600, color: "#374151", marginBottom: 6 }}>
            {search ? "No experiments match your search" : "No experiments yet"}
          </div>
          <div style={{ fontSize: 12, marginBottom: 16 }}>
            {search ? "Try a different search term" : "Create your first experiment in the Experiment Builder"}
          </div>
          {!search && (
            <button onClick={() => openInBuilder("new")}
              style={{ padding: "8px 20px", border: "none", borderRadius: 7, cursor: "pointer", fontSize: 13, fontWeight: 700, background: "#7c3aed", color: "#fff" }}>
              + New Experiment
            </button>
          )}
        </div>
      )}

      {/* Card grid */}
      <div style={{ display: "grid", gap: "0.75rem", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))" }}>
        {filtered.map(exp => (
          <ExpCard key={exp.id} exp={exp} onDeleted={handleDeleted} onRefresh={load}
            lastRun={lastRunMap[exp.id]} />
        ))}
      </div>
    </div>
  );
}

// ── Shared styles ────────────────────────────────────────────────────────────

const btnPrimary: React.CSSProperties = {
  padding: "5px 12px", border: "none", borderRadius: 5,
  cursor: "pointer", fontSize: 12, fontWeight: 700,
  background: "#1e3a5f", color: "#fff",
};

const btnSecondary: React.CSSProperties = {
  padding: "5px 10px", border: "1px solid #e5e7eb", borderRadius: 5,
  cursor: "pointer", fontSize: 12, fontWeight: 500,
  background: "#f9fafb", color: "#374151",
};
