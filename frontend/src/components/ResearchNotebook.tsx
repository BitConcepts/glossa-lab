/**
 * ResearchNotebook — markdown scratchpad with live preview.
 * Each notebook can be linked to a study and tagged.
 */
import { useEffect, useState } from "react";
import {
  createNotebook, deleteNotebook, listNotebooks, updateNotebook,
  type Notebook,
} from "../api";
import { useProject } from "../hooks/useProject";
import { useToast } from "../hooks/useToast";

/** Minimal markdown renderer (no external deps) */
function renderMarkdown(md: string): string {
  return md
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/^#{3} (.+)$/gm, "<h3 style='margin:10px 0 4px;font-size:14px'>$1</h3>")
    .replace(/^#{2} (.+)$/gm, "<h2 style='margin:12px 0 6px;font-size:16px'>$1</h2>")
    .replace(/^# (.+)$/gm, "<h1 style='margin:14px 0 8px;font-size:18px'>$1</h1>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/`(.+?)`/g, "<code style='background:#f3f4f6;padding:1px 4px;border-radius:3px;font-size:12px'>$1</code>")
    .replace(/^- (.+)$/gm, "<li style='margin:2px 0'>$1</li>")
    .replace(/(<li[^>]*>.*<\/li>)/s, "<ul style='margin:6px 0;padding-left:18px'>$1</ul>")
    .replace(/\n\n/g, "</p><p style='margin:6px 0'>")
    .replace(/^/, "<p style='margin:0'>").replace(/$/, "</p>");
}

function NoteCard({ note, onUpdated, onDeleted, studies }: {
  note: Notebook; onUpdated: (n: Notebook) => void; onDeleted: (id: string) => void;
  studies: { id: string; name: string }[];
}) {
  const { toast } = useToast();
  const [editing, setEditing] = useState(false);
  const [preview, setPreview] = useState(false);
  const [content, setContent] = useState(note.content);
  const [title, setTitle] = useState(note.title);
  const [studyId, setStudyId] = useState(note.study_id ?? "");
  const [saving, setSaving] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const study = studies.find((s) => s.id === note.study_id);

  const save = async () => {
    setSaving(true);
    try {
      const updated = await updateNotebook(note.id, { title, content, study_id: studyId || null });
      onUpdated(updated); setEditing(false); toast("Saved", "success");
    } catch { toast("Save failed", "error"); }
    finally { setSaving(false); }
  };

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden", marginBottom: 8 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 14px", background: "#fafafa", cursor: "pointer" }}
        onClick={() => setExpanded(x => !x)}>
        <span style={{ fontSize: 16 }}>📓</span>
        <span style={{ flex: 1, fontWeight: 600, fontSize: 13, color: "#111827" }}>{note.title}</span>
        {study && <span style={{ fontSize: 11, padding: "1px 7px", borderRadius: 8, background: "#eff6ff", color: "#2563eb", fontWeight: 600 }}>{study.name.slice(0, 20)}</span>}
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{note.updated_at.slice(0, 10)}</span>
        <button onClick={(e) => { e.stopPropagation(); if (!confirm("Delete?")) return; deleteNotebook(note.id).then(() => onDeleted(note.id)).catch(() => toast("Delete failed", "error")); }}
          style={{ border: "1px solid #fca5a5", background: "none", color: "#dc2626", borderRadius: 4, fontSize: 10, padding: "1px 7px", cursor: "pointer" }}>🗑</button>
        <span style={{ fontSize: 14, color: "#9ca3af" }}>{expanded ? "▲" : "▼"}</span>
      </div>

      {expanded && (
        <div style={{ padding: "14px 16px" }} onClick={(e) => e.stopPropagation()}>
          {editing ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              <div style={{ display: "flex", gap: 8 }}>
                <input value={title} onChange={(e) => setTitle(e.target.value)} style={{ ...inputStyle, flex: 1 }} placeholder="Title" />
                <select value={studyId} onChange={(e) => setStudyId(e.target.value)} style={{ ...inputStyle, width: 200 }}>
                  <option value="">— no study —</option>
                  {studies.map((s) => <option key={s.id} value={s.id}>{s.name.slice(0, 30)}</option>)}
                </select>
              </div>
              <div style={{ display: "flex", gap: 4, marginBottom: 4 }}>
                <button onClick={() => setPreview(false)} style={{ ...btnSmall, background: !preview ? "#1e3a5f" : "#f3f4f6", color: !preview ? "#fff" : "#374151" }}>Edit</button>
                <button onClick={() => setPreview(true)} style={{ ...btnSmall, background: preview ? "#1e3a5f" : "#f3f4f6", color: preview ? "#fff" : "#374151" }}>Preview</button>
              </div>
              {!preview ? (
                <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={12}
                  style={{ ...inputStyle, fontFamily: "monospace", resize: "vertical", fontSize: 12 }}
                  placeholder="Write in markdown…&#10;&#10;## Section&#10;**bold**, *italic*, `code`&#10;- list items" />
              ) : (
                <div style={{ minHeight: 200, padding: "12px 14px", border: "1px solid #e5e7eb", borderRadius: 6, fontSize: 13, lineHeight: 1.7, background: "#fff" }}
                  dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }} />
              )}
              <div style={{ display: "flex", gap: 8 }}>
                <button onClick={save} disabled={saving} style={btnPrimary}>{saving ? "Saving…" : "Save"}</button>
                <button onClick={() => setEditing(false)} style={btnSecondary}>Cancel</button>
              </div>
            </div>
          ) : (
            <div>
              {content ? (
                <div style={{ fontSize: 13, lineHeight: 1.7, color: "#374151", marginBottom: 10 }}
                  dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }} />
              ) : (
                <p style={{ color: "#9ca3af", fontSize: 13, fontStyle: "italic", marginBottom: 10 }}>Empty notebook. Click Edit to write.</p>
              )}
              <button onClick={() => { setEditing(true); setPreview(false); }} style={btnSecondary}>✎ Edit</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export function ResearchNotebook() {
  const { toast } = useToast();
  const { activeProject } = useProject();
  const projectId = activeProject?.id ?? null;
  const [notebooks, setNotebooks] = useState<Notebook[]>([]);
  const [loading, setLoading] = useState(true);
  const [newTitle, setNewTitle] = useState("");

  useEffect(() => {
    setLoading(true);
    listNotebooks(projectId)
      .then(setNotebooks)
      .catch(() => toast("Failed to load", "error"))
      .finally(() => setLoading(false));
  }, [projectId]);

  const addNote = async () => {
    if (!newTitle.trim()) return;
    try {
      const n = await createNotebook({ title: newTitle.trim(), project_id: projectId || undefined });
      setNotebooks((prev) => [n, ...prev]); setNewTitle(""); toast("Notebook created", "success");
    } catch { toast("Failed", "error"); }
  };

  return (
    <div>
      <h2 style={{ margin: "0 0 0.75rem" }}>Research Notebooks</h2>
      <p style={{ margin: "0 0 1.25rem", fontSize: 13, color: "#6b7280" }}>
        Freeform markdown notes.{activeProject ? ` Scoped to ${activeProject.label}.` : ""}
      </p>
      <div style={{ display: "flex", gap: 8, marginBottom: "1.25rem" }}>
        <input value={newTitle} onChange={(e) => setNewTitle(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") addNote(); }}
          placeholder="New notebook title…" style={{ ...inputStyle, flex: 1 }} />
        <button onClick={addNote} disabled={!newTitle.trim()} style={btnPrimary}>+ Create</button>
      </div>
      {loading && <p style={{ color: "#6b7280", fontSize: 13 }}>Loading…</p>}
      {!loading && notebooks.length === 0 && <p style={{ color: "#6b7280", fontSize: 13 }}>No notebooks yet. Create one above.</p>}
      {notebooks.map((n) => (
        <NoteCard key={n.id} note={n} studies={[]}
          onUpdated={(u) => setNotebooks((prev) => prev.map((x) => x.id === u.id ? u : x))}
          onDeleted={(id) => setNotebooks((prev) => prev.filter((x) => x.id !== id))} />
      ))}
    </div>
  );
}

const inputStyle: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box", display: "block" };
const btnPrimary: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer", fontWeight: 600, whiteSpace: "nowrap" };
const btnSecondary: React.CSSProperties = { background: "#fff", color: "#374151", border: "1px solid #d1d5db", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer" };
const btnSmall: React.CSSProperties = { padding: "3px 10px", border: "1px solid #e5e7eb", borderRadius: 4, cursor: "pointer", fontSize: 11, background: "#f9fafb", color: "#374151" };
