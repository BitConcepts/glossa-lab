/**
 * ProjectsView — top-level project management.
 *
 * Shows the list of projects (active project first) with detail view
 * showing linked topics, experiments, hypotheses, and corpora.
 */

import { useCallback, useEffect, useState } from "react";
import {
  listProjects,
  activateProject,
  upsertProject,
  deleteProject,
  type Project,
} from "../api";
import { useToast } from "../hooks/useToast";

export function ProjectsView() {
  const { toast } = useToast();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const ps = await listProjects();
      setProjects(ps);
      if (!selected && ps.length > 0) {
        setSelected(ps[0].id);
      }
    } catch (e) {
      toast(e instanceof Error ? e.message : "Failed to load projects", "error");
    } finally {
      setLoading(false);
    }
  }, [toast, selected]);

  useEffect(() => { void refresh(); }, [refresh]);

  const onActivate = async (id: string) => {
    try {
      await activateProject(id);
      toast("Project activated", "success");
      void refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Activate failed", "error");
    }
  };

  const onDelete = async (id: string) => {
    if (!confirm("Delete this project? This cannot be undone.")) return;
    try {
      await deleteProject(id);
      toast("Project deleted", "info");
      setSelected(null);
      void refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Delete failed", "error");
    }
  };

  const onCreateNew = async () => {
    const label = prompt("New project name:");
    if (!label?.trim()) return;
    const id = label.trim().toLowerCase().replace(/[^a-z0-9]+/g, "_").slice(0, 40);
    try {
      await upsertProject(id, {
        label: label.trim(),
        description: "",
        prompt_context: "",
        topic_ids: [],
        experiment_ids: [],
        corpus_ids: [],
        is_active: 0,
      });
      toast("Project created", "success");
      setSelected(id);
      void refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Create failed", "error");
    }
  };

  const active = projects.find((p) => p.id === selected);

  const navigate = (view: string) =>
    window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view } }));

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto" }}>
      <div style={{ display: "flex", alignItems: "flex-end", gap: 12, marginBottom: 16 }}>
        <div style={{ flex: 1 }}>
          <h2 style={{ margin: 0, fontSize: 22, color: "#111827" }}>📁 Projects</h2>
          <p style={{ margin: "4px 0 0", fontSize: 13, color: "#6b7280" }}>
            Each project scopes your research — topics, experiments, corpora, and AI context.
            The active project controls what the discovery engine fetches and how insights are generated.
          </p>
        </div>
        <button onClick={() => void onCreateNew()} style={{
          padding: "8px 16px", border: "1px solid #2563eb", borderRadius: 6,
          background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600,
          cursor: "pointer",
        }}>
          + New Project
        </button>
      </div>

      {loading && <div style={{ color: "#6b7280", fontSize: 13 }}>Loading projects…</div>}

      {!loading && projects.length === 0 && (
        <div style={{ textAlign: "center", padding: "2rem", color: "#9ca3af",
          border: "1px dashed #cbd5e1", borderRadius: 10 }}>
          No projects configured. The backend seeds a default project on first boot.
        </div>
      )}

      {/* Project list */}
      <div style={{ display: "grid", gap: 10, gridTemplateColumns: "280px 1fr" }}>
        {/* Left: project cards */}
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {projects.map((p) => (
            <button key={p.id} onClick={() => setSelected(p.id)} style={{
              padding: "12px 14px", border: "1px solid",
              borderColor: selected === p.id ? "#2563eb" : "#e5e7eb",
              borderRadius: 8, background: selected === p.id ? "#eff6ff" : "#fff",
              cursor: "pointer", textAlign: "left",
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 14, fontWeight: 700, color: "#111827", flex: 1 }}>
                  {p.label}
                </span>
                {p.is_active ? (
                  <span style={{ fontSize: 9, padding: "2px 7px", borderRadius: 9,
                    background: "#dcfce7", color: "#15803d", fontWeight: 700 }}>
                    ACTIVE
                  </span>
                ) : null}
              </div>
              <div style={{ fontSize: 11, color: "#6b7280", marginTop: 4, lineHeight: 1.4 }}>
                {p.description.slice(0, 100)}{p.description.length > 100 ? "…" : ""}
              </div>
              <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 4 }}>
                {p.topic_ids?.length ?? 0} topics · {p.experiment_ids?.length ?? 0} experiments
              </div>
            </button>
          ))}
        </div>

        {/* Right: detail panel */}
        {active && (
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 10, background: "#fff",
            padding: "20px 24px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
              <h3 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "#111827", flex: 1 }}>
                {active.label}
              </h3>
              {!active.is_active && (
                <button onClick={() => void onActivate(active.id)} style={{
                  padding: "5px 14px", border: "1px solid #2563eb", borderRadius: 6,
                  background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600,
                  cursor: "pointer",
                }}>
                  Set as Active
                </button>
              )}
              {active.is_active ? (
                <span style={{ fontSize: 11, padding: "3px 10px", borderRadius: 9,
                  background: "#dcfce7", color: "#15803d", fontWeight: 700 }}>
                  ✓ Active Project
                </span>
              ) : null}
              <button onClick={() => void onDelete(active.id)} style={{
                padding: "5px 10px", border: "1px solid #fca5a5", borderRadius: 6,
                background: "#fff", color: "#b91c1c", fontSize: 11, cursor: "pointer",
              }}>
                Delete
              </button>
            </div>

            <p style={{ fontSize: 13, color: "#374151", lineHeight: 1.55, margin: "0 0 16px" }}>
              {active.description}
            </p>

            {/* Topics */}
            <Section title="🔭 Discovery Topics" count={active.topic_ids?.length ?? 0}>
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                {(active.topic_ids || []).map((t) => (
                  <span key={t} style={chip}>{t}</span>
                ))}
                {(!active.topic_ids || active.topic_ids.length === 0) && (
                  <span style={{ fontSize: 11, color: "#9ca3af" }}>No topics linked</span>
                )}
              </div>
            </Section>

            {/* Experiments */}
            <Section title="🔀 Experiments" count={active.experiment_ids?.length ?? 0}>
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap", maxHeight: 200,
                overflowY: "auto" }}>
                {(active.experiment_ids || []).slice(0, 50).map((e) => (
                  <span key={e} style={{ ...chip, cursor: "pointer" }}
                    onClick={() => navigate("experiments")}
                    title={`Open experiment: ${e}`}>
                    {e}
                  </span>
                ))}
                {(active.experiment_ids?.length ?? 0) > 50 && (
                  <span style={{ fontSize: 10, color: "#6b7280" }}>
                    +{(active.experiment_ids?.length ?? 0) - 50} more
                  </span>
                )}
                {(!active.experiment_ids || active.experiment_ids.length === 0) && (
                  <span style={{ fontSize: 11, color: "#9ca3af" }}>No experiments linked</span>
                )}
              </div>
            </Section>

            {/* Corpora */}
            <Section title="📚 Corpora" count={active.corpus_ids?.length ?? 0}>
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                {(active.corpus_ids || []).map((c) => (
                  <span key={c} style={chip}>{c}</span>
                ))}
                {(!active.corpus_ids || active.corpus_ids.length === 0) && (
                  <span style={{ fontSize: 11, color: "#9ca3af" }}>
                    No corpora linked yet — corpora are global and can be linked here.
                  </span>
                )}
              </div>
            </Section>

            {/* AI Context */}
            <Section title="🤖 AI Prompt Context" count={active.prompt_context ? 1 : 0}>
              {active.prompt_context ? (
                <div style={{ fontSize: 12, color: "#374151", lineHeight: 1.5,
                  background: "#f8fafc", padding: 10, borderRadius: 6,
                  border: "1px solid #e5e7eb", maxHeight: 120, overflowY: "auto" }}>
                  {active.prompt_context}
                </div>
              ) : (
                <span style={{ fontSize: 11, color: "#9ca3af" }}>No prompt context set</span>
              )}
            </Section>

            {/* Quick links */}
            <div style={{ marginTop: 16, display: "flex", gap: 8, flexWrap: "wrap" }}>
              <button onClick={() => navigate("discovery")} style={linkBtn}>🔭 Discovery</button>
              <button onClick={() => navigate("experiments")} style={linkBtn}>🔀 Experiments</button>
              <button onClick={() => navigate("hypotheses")} style={linkBtn}>💡 Hypotheses</button>
              <button onClick={() => navigate("corpora")} style={linkBtn}>📚 Corpora</button>
              <button onClick={() => navigate("reports")} style={linkBtn}>📄 Reports</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function Section({ title, count, children }: {
  title: string; count: number; children: React.ReactNode;
}) {
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ fontSize: 11, fontWeight: 700, color: "#7c3aed",
        textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>
        {title} <span style={{ color: "#9ca3af", fontWeight: 500 }}>({count})</span>
      </div>
      {children}
    </div>
  );
}

const chip: React.CSSProperties = {
  fontSize: 10, padding: "3px 9px", borderRadius: 12,
  background: "#f1f5f9", color: "#475569", border: "1px solid #cbd5e1",
};

const linkBtn: React.CSSProperties = {
  padding: "6px 12px", border: "1px solid #e5e7eb", borderRadius: 6,
  background: "#f9fafb", cursor: "pointer", fontSize: 12, color: "#374151",
};
