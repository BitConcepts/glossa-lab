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
  aiChat,
  type Project,
} from "../api";
import { useToast } from "../hooks/useToast";

/** Deep-link to a specific experiment in the builder. */
function openExpInBuilder(expId: string) {
  localStorage.setItem(
    "glossa_exp_builder_open",
    JSON.stringify({ action: "load", id: expId }),
  );
  window.dispatchEvent(
    new CustomEvent("glossa:navigate", { detail: { view: "exp-builder" } }),
  );
}

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
      window.dispatchEvent(new CustomEvent("glossa:project-changed"));
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
      window.dispatchEvent(new CustomEvent("glossa:project-changed"));
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
      window.dispatchEvent(new CustomEvent("glossa:project-changed"));
      void refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Create failed", "error");
    }
  };

  const [editingLabel, setEditingLabel] = useState(false);
  const [labelDraft, setLabelDraft] = useState("");

  const onRenameProject = async (id: string, newLabel: string) => {
    const proj = projects.find((p) => p.id === id);
    if (!proj || !newLabel.trim() || newLabel.trim() === proj.label) {
      setEditingLabel(false); return;
    }
    try {
      await upsertProject(id, { ...proj, label: newLabel.trim() });
      toast("Project renamed", "success");
      window.dispatchEvent(new CustomEvent("glossa:project-changed"));
      void refresh();
    } catch (e) {
      toast(e instanceof Error ? e.message : "Rename failed", "error");
    } finally { setEditingLabel(false); }
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
              {editingLabel ? (
                <div style={{ display: "flex", gap: 6, alignItems: "center", flex: 1 }}>
                  <input
                    value={labelDraft}
                    onChange={(e) => setLabelDraft(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") void onRenameProject(active.id, labelDraft);
                      if (e.key === "Escape") setEditingLabel(false);
                    }}
                    autoFocus
                    style={{ fontSize: 16, fontWeight: 700, padding: "4px 8px",
                      border: "1px solid #2563eb", borderRadius: 5, flex: 1 }}
                  />
                  <button onClick={() => void onRenameProject(active.id, labelDraft)}
                    style={{ padding: "4px 10px", background: "#2563eb", color: "#fff",
                      border: "none", borderRadius: 5, fontSize: 11, cursor: "pointer" }}>
                    Rename
                  </button>
                  <button onClick={() => setEditingLabel(false)}
                    style={{ padding: "4px 8px", border: "1px solid #d1d5db",
                      borderRadius: 5, fontSize: 11, cursor: "pointer" }}>
                    ✕
                  </button>
                </div>
              ) : (
                <h3
                  onClick={() => { setLabelDraft(active.label); setEditingLabel(true); }}
                  title="Click to rename"
                  style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "#111827",
                    flex: 1, cursor: "pointer", borderBottom: "1px dashed transparent",
                    transition: "border-color 0.15s" }}
                  onMouseEnter={(e) => (e.currentTarget.style.borderBottomColor = "#93c5fd")}
                  onMouseLeave={(e) => (e.currentTarget.style.borderBottomColor = "transparent")}
                >
                  {active.label} <span style={{ fontSize: 11, color: "#93c5fd", fontWeight: 400 }}>✎</span>
                </h3>
              )}
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

            {/* Description shown in header only if non-empty and not in edit section */}
            {active.description && (
              <p style={{ fontSize: 13, color: "#374151", lineHeight: 1.55, margin: "0 0 16px" }}>
                {active.description}
              </p>
            )}

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
                    onClick={() => openExpInBuilder(e)}
                    title={`Open ${e} in Experiment Builder`}>
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

            {/* Project Goals (editable prompt_context) */}
            <Section title="🎯 Project Goals" count={active.prompt_context ? 1 : 0}>
              <EditableTextArea
                value={active.prompt_context}
                placeholder="Describe the research goals for this project. This text is injected into every LLM call (discovery mining, dashboard insight, AI chat) to scope the AI to your research."
                onSave={async (val) => {
                  try {
                    await upsertProject(active.id, { ...active, prompt_context: val });
                    toast("Project goals saved", "success");
                    void refresh();
                  } catch (e) {
                    toast(e instanceof Error ? e.message : "Save failed", "error");
                  }
                }}
                onGenerate={async () => {
                  const desc = active.description || active.label;
                  const topics = (active.topic_ids || []).join(", ");
                  const nExp = active.experiment_ids?.length ?? 0;
                  const resp = await aiChat({
                    messages: [
                      { role: "system", content: "You are a research-project goal writer for Glossa Lab, a computational decipherment platform. Write clear, concise, actionable project goals. Output ONLY the goals text — no preamble, no markdown fences, no explanation. The goals should: (1) state the core research objective, (2) list 4–6 key research axes as bullet points using •, (3) specify methodological standards (falsifiability, benchmarks, transparency). Keep it under 250 words." },
                      { role: "user", content: `Generate project goals for:\nProject: ${active.label}\nDescription: ${desc}\nTopics: ${topics || "(none)"}\nLinked experiments: ${nExp}\nExisting goals: ${active.prompt_context || "(none yet)"}` },
                    ],
                  });
                  return resp.content;
                }}
              />
            </Section>

            {/* Description (editable) */}
            <Section title="📝 Description" count={active.description ? 1 : 0}>
              <EditableTextArea
                value={active.description}
                placeholder="Short description of this project."
                onSave={async (val) => {
                  try {
                    await upsertProject(active.id, { ...active, description: val });
                    toast("Description saved", "success");
                    void refresh();
                  } catch (e) {
                    toast(e instanceof Error ? e.message : "Save failed", "error");
                  }
                }}
                onGenerate={async () => {
                  const topics = (active.topic_ids || []).join(", ");
                  const nExp = active.experiment_ids?.length ?? 0;
                  const resp = await aiChat({
                    messages: [
                      { role: "system", content: "You are a research-project description writer for Glossa Lab, a computational decipherment and linguistic analysis platform. Write a concise, informative project description in 1-2 sentences. Output ONLY the description text — no preamble, no markdown, no explanation." },
                      { role: "user", content: `Generate a short project description for:\nProject: ${active.label}\nTopics: ${topics || "(none)"}\nLinked experiments: ${nExp}\nExisting goals: ${active.prompt_context || "(none)"}\nExisting description: ${active.description || "(none yet)"}` },
                    ],
                  });
                  return resp.content;
                }}
              />
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

/** Inline editable textarea with Save/Cancel and optional AI generation. */
function EditableTextArea({ value, placeholder, onSave, onGenerate }: {
  value: string; placeholder: string; onSave: (v: string) => Promise<void>;
  onGenerate?: () => Promise<string>;
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);
  const [saving, setSaving] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => { setDraft(value); }, [value]);

  const handleGenerate = async () => {
    if (!onGenerate) return;
    setGenerating(true);
    setEditing(true);
    try {
      const result = await onGenerate();
      setDraft(result);
    } catch {
      /* leave draft unchanged on error */
    } finally {
      setGenerating(false);
    }
  };

  if (!editing) {
    return (
      <div style={{ position: "relative" }}>
        <div
          onClick={() => setEditing(true)}
          style={{ fontSize: 12, color: value ? "#374151" : "#9ca3af", lineHeight: 1.5,
            background: "#f8fafc", padding: 10, borderRadius: 6,
            border: "1px solid #e5e7eb", cursor: "pointer",
            minHeight: 40, whiteSpace: "pre-wrap",
            paddingRight: onGenerate ? 90 : 10 }}
          title="Click to edit">
          {value || placeholder}
        </div>
        {onGenerate && (
          <button
            onClick={(e) => { e.stopPropagation(); void handleGenerate(); }}
            disabled={generating}
            style={{ position: "absolute", top: 6, right: 6,
              padding: "4px 10px", border: "1px solid #7c3aed", borderRadius: 5,
              background: "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)",
              color: "#fff", fontSize: 10, fontWeight: 600,
              cursor: generating ? "wait" : "pointer", opacity: generating ? 0.7 : 1 }}>
            {generating ? "Generating…" : "✨ Glossa AI"}
          </button>
        )}
      </div>
    );
  }

  return (
    <div>
      {generating && (
        <div style={{ fontSize: 11, color: "#7c3aed", marginBottom: 4 }}>
          ✨ Generating with Glossa AI…
        </div>
      )}
      <textarea
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        placeholder={placeholder}
        rows={6}
        style={{ width: "100%", fontSize: 12, padding: 8, borderRadius: 6,
          border: "1px solid #7c3aed", lineHeight: 1.5, resize: "vertical",
          fontFamily: "inherit" }}
        autoFocus
      />
      <div style={{ display: "flex", gap: 6, marginTop: 6 }}>
        <button
          disabled={saving || generating}
          onClick={async () => {
            setSaving(true);
            await onSave(draft);
            setSaving(false);
            setEditing(false);
          }}
          style={{ padding: "4px 12px", border: "1px solid #2563eb", borderRadius: 5,
            background: "#2563eb", color: "#fff", fontSize: 11, fontWeight: 600,
            cursor: "pointer" }}>
          {saving ? "Saving…" : "Save"}
        </button>
        {onGenerate && (
          <button
            onClick={() => void handleGenerate()}
            disabled={generating}
            style={{ padding: "4px 12px", border: "1px solid #7c3aed", borderRadius: 5,
              background: "#f5f3ff", color: "#7c3aed", fontSize: 11, fontWeight: 600,
              cursor: generating ? "wait" : "pointer" }}>
            {generating ? "Generating…" : "✨ Regenerate"}
          </button>
        )}
        <button
          onClick={() => { setDraft(value); setEditing(false); }}
          style={{ padding: "4px 12px", border: "1px solid #d1d5db", borderRadius: 5,
            background: "#fff", color: "#374151", fontSize: 11, cursor: "pointer" }}>
          Cancel
        </button>
      </div>
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
