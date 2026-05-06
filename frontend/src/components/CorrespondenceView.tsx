/**
 * CorrespondenceView — track researcher communications.
 * Card-based UI with paste-to-import and project scoping.
 */
import { useEffect, useState } from "react";
import {
  listCorrespondences, createCorrespondence, updateCorrespondence,
  deleteCorrespondence, parseEmailToCorrespondence,
  type Correspondence,
} from "../api";
import { useProject } from "../hooks/useProject";
import { useToast } from "../hooks/useToast";

const DIR_COLORS: Record<string, { bg: string; fg: string }> = {
  inbound:  { bg: "#dbeafe", fg: "#1d4ed8" },
  outbound: { bg: "#dcfce7", fg: "#15803d" },
  internal: { bg: "#fef3c7", fg: "#b45309" },
};
const STATUS_COLORS: Record<string, { bg: string; fg: string }> = {
  pending:  { bg: "#eff6ff", fg: "#2563eb" },
  replied:  { bg: "#f0fdf4", fg: "#16a34a" },
  no_reply: { bg: "#fef3c7", fg: "#d97706" },
  closed:   { bg: "#f3f4f6", fg: "#6b7280" },
};

function fmtDate(d: string): string {
  if (!d) return "";
  try { return new Date(d).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" }); }
  catch { return d.slice(0, 10); }
}

function CorrCard({ c, onUpdated, onDeleted }: {
  c: Correspondence; onUpdated: (c: Correspondence) => void; onDeleted: (id: string) => void;
}) {
  const { toast } = useToast();
  const [expanded, setExpanded] = useState(false);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ ...c });
  const [saving, setSaving] = useState(false);

  const dc = DIR_COLORS[c.direction] ?? DIR_COLORS.outbound;
  const sc = STATUS_COLORS[c.reply_status] ?? STATUS_COLORS.pending;

  const save = async () => {
    setSaving(true);
    try {
      const updated = await updateCorrespondence(c.id, {
        subject: form.subject, body: form.body, from_addr: form.from_addr,
        to_addr: form.to_addr, cc_addr: form.cc_addr, date: form.date,
        direction: form.direction, channel: form.channel,
        reply_status: form.reply_status, follow_up_date: form.follow_up_date,
        claims_made: form.claims_made, questions: form.questions,
      });
      onUpdated(updated); setEditing(false); toast("Saved", "success");
    } catch { toast("Save failed", "error"); }
    finally { setSaving(false); }
  };

  const changeStatus = async (s: string) => {
    try {
      const updated = await updateCorrespondence(c.id, { reply_status: s });
      onUpdated(updated);
    } catch { toast("Update failed", "error"); }
  };

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden", marginBottom: 8 }}>
      <div style={{ display: "flex", gap: 8, padding: "10px 14px", background: "#fafafa", cursor: "pointer", alignItems: "center" }}
        onClick={() => setExpanded(x => !x)}>
        <span style={{ fontSize: 14 }}>{c.direction === "inbound" ? "📥" : c.direction === "internal" ? "🔄" : "📤"}</span>
        <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 6, background: dc.bg, color: dc.fg, fontWeight: 700 }}>
          {c.direction}
        </span>
        <span style={{ flex: 1, fontWeight: 600, fontSize: 13, color: "#111827" }}>
          {c.subject || "(no subject)"}
        </span>
        <span style={{ fontSize: 11, color: "#6b7280" }}>{c.from_addr.split("<")[0].trim() || c.from_addr}</span>
        <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 6, background: sc.bg, color: sc.fg, fontWeight: 700 }}>
          {c.reply_status}
        </span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{fmtDate(c.date)}</span>
        <button onClick={(e) => { e.stopPropagation(); if (!confirm("Delete?")) return; deleteCorrespondence(c.id).then(() => onDeleted(c.id)).catch(() => toast("Delete failed", "error")); }}
          style={{ border: "1px solid #fca5a5", background: "none", color: "#dc2626", borderRadius: 4, fontSize: 10, padding: "1px 7px", cursor: "pointer" }}>🗑</button>
        <span style={{ fontSize: 14, color: "#9ca3af" }}>{expanded ? "▲" : "▼"}</span>
      </div>

      {expanded && (
        <div style={{ padding: "14px 16px" }} onClick={(e) => e.stopPropagation()}>
          {/* Status switcher */}
          <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
            {["pending", "replied", "no_reply", "closed"].map((s) => {
              const col = STATUS_COLORS[s];
              return (
                <button key={s} onClick={() => changeStatus(s)}
                  style={{ padding: "2px 10px", borderRadius: 5, border: `1px solid ${c.reply_status === s ? col.fg : "#d1d5db"}`, background: c.reply_status === s ? col.bg : "#fff", color: c.reply_status === s ? col.fg : "#6b7280", cursor: "pointer", fontSize: 10, fontWeight: c.reply_status === s ? 700 : 400 }}>
                  {s.replace("_", " ")}
                </button>
              );
            })}
          </div>

          {editing ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 6, maxWidth: 600, marginBottom: 10 }}>
              {(["subject", "from_addr", "to_addr", "cc_addr", "date", "follow_up_date"] as const).map((f) => (
                <div key={f}>
                  <label style={lbl}>{f.replace(/_/g, " ")}</label>
                  <input value={String((form as unknown as Record<string, unknown>)[f] ?? "")} onChange={(e) => setForm(prev => ({ ...prev, [f]: e.target.value }))} style={inp} />
                </div>
              ))}
              <div>
                <label style={lbl}>Body</label>
                <textarea value={form.body} onChange={(e) => setForm(prev => ({ ...prev, body: e.target.value }))} rows={6} style={{ ...inp, resize: "vertical", fontFamily: "inherit" }} />
              </div>
              <div>
                <label style={lbl}>Claims made</label>
                <textarea value={form.claims_made} onChange={(e) => setForm(prev => ({ ...prev, claims_made: e.target.value }))} rows={2} style={{ ...inp, resize: "vertical", fontFamily: "inherit" }} />
              </div>
              <div>
                <label style={lbl}>Questions asked</label>
                <textarea value={form.questions} onChange={(e) => setForm(prev => ({ ...prev, questions: e.target.value }))} rows={2} style={{ ...inp, resize: "vertical", fontFamily: "inherit" }} />
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                <button onClick={save} disabled={saving} style={btnP}>{saving ? "Saving…" : "Save"}</button>
                <button onClick={() => setEditing(false)} style={btnS}>Cancel</button>
              </div>
            </div>
          ) : (
            <div>
              <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 6 }}>
                <strong>From:</strong> {c.from_addr} · <strong>To:</strong> {c.to_addr}
                {c.cc_addr && <> · <strong>CC:</strong> {c.cc_addr}</>}
                {c.follow_up_date && <> · <strong>Follow-up:</strong> {fmtDate(c.follow_up_date)}</>}
              </div>
              {c.body && <pre style={{ margin: "0 0 8px", fontSize: 12, color: "#374151", lineHeight: 1.6, whiteSpace: "pre-wrap", fontFamily: "inherit" }}>{c.body.slice(0, 2000)}</pre>}
              {c.claims_made && <p style={{ margin: "4px 0", fontSize: 11, color: "#7c3aed" }}><strong>Claims:</strong> {c.claims_made}</p>}
              {c.questions && <p style={{ margin: "4px 0", fontSize: 11, color: "#2563eb" }}><strong>Questions:</strong> {c.questions}</p>}
              {c.attachments?.length > 0 && (
                <div style={{ fontSize: 11, color: "#6b7280", marginTop: 4 }}>
                  📎 {c.attachments.map((a: Record<string, string>) => a.name || "attachment").join(", ")}
                </div>
              )}
              <button onClick={() => { setForm({ ...c }); setEditing(true); }} style={{ ...btnS, marginTop: 8, fontSize: 11, padding: "3px 10px" }}>✎ Edit</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export function CorrespondenceView() {
  const { toast } = useToast();
  const { activeProject } = useProject();
  const projectId = activeProject?.id ?? null;
  const [items, setItems] = useState<Correspondence[]>([]);
  const [loading, setLoading] = useState(true);
  const [showPaste, setShowPaste] = useState(false);
  const [pasteText, setPasteText] = useState("");
  const [parsing, setParsing] = useState(false);
  const [showManual, setShowManual] = useState(false);
  const [manualForm, setManualForm] = useState({
    direction: "outbound", channel: "email", from_addr: "", to_addr: "",
    cc_addr: "", subject: "", body: "", date: "", claims_made: "", questions: "",
    follow_up_date: "",
  });

  useEffect(() => {
    setLoading(true);
    listCorrespondences(projectId).then(setItems).catch(() => toast("Failed to load", "error")).finally(() => setLoading(false));
  }, [projectId]);

  const handlePaste = async () => {
    if (!pasteText.trim()) return;
    setParsing(true);
    try {
      const parsed = await parseEmailToCorrespondence({ raw_text: pasteText });
      const created = await createCorrespondence({ ...parsed, project_id: projectId || "" });
      setItems(prev => [created, ...prev]);
      setPasteText(""); setShowPaste(false);
      toast("Correspondence imported", "success");
    } catch (e) { toast(e instanceof Error ? e.message : "Parse failed", "error"); }
    finally { setParsing(false); }
  };

  const handleManualCreate = async () => {
    try {
      const created = await createCorrespondence({ ...manualForm, project_id: projectId || "" });
      setItems(prev => [created, ...prev]);
      setShowManual(false);
      setManualForm({ direction: "outbound", channel: "email", from_addr: "", to_addr: "", cc_addr: "", subject: "", body: "", date: "", claims_made: "", questions: "", follow_up_date: "" });
      toast("Correspondence created", "success");
    } catch { toast("Create failed", "error"); }
  };

  return (
    <div>
      <div style={{ display: "flex", alignItems: "flex-end", gap: 12, marginBottom: 16 }}>
        <div style={{ flex: 1 }}>
          <h2 style={{ margin: 0, fontSize: 20, color: "#111827" }}>✉ Correspondence</h2>
          <p style={{ margin: "4px 0 0", fontSize: 13, color: "#6b7280" }}>
            Track emails, meetings, and letters with researchers.{activeProject ? ` Scoped to ${activeProject.label}.` : ""}
          </p>
        </div>
        <button onClick={() => setShowPaste(true)} style={{ ...btnP, background: "#7c3aed" }}>📋 Paste Email</button>
        <button onClick={() => setShowManual(true)} style={btnP}>+ New</button>
      </div>

      {/* Paste modal */}
      {showPaste && (
        <div style={{ marginBottom: 16, padding: "16px 20px", border: "1px solid #a78bfa", borderRadius: 8, background: "#faf5ff" }}>
          <div style={{ fontWeight: 700, fontSize: 13, color: "#7c3aed", marginBottom: 8 }}>📋 Paste Email Content</div>
          <p style={{ fontSize: 11, color: "#6b7280", margin: "0 0 8px" }}>
            Paste raw email text, headers+body, or .eml content. Glossa AI will extract structured fields for review.
          </p>
          <textarea value={pasteText} onChange={(e) => setPasteText(e.target.value)} rows={10}
            placeholder="Paste email content here…"
            style={{ width: "100%", padding: 8, border: "1px solid #c4b5fd", borderRadius: 6, fontSize: 12, fontFamily: "monospace", resize: "vertical", boxSizing: "border-box" }} />
          <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
            <button onClick={handlePaste} disabled={parsing || !pasteText.trim()} style={{ ...btnP, background: "#7c3aed" }}>
              {parsing ? "✨ Parsing…" : "✨ Import"}
            </button>
            <button onClick={() => { setShowPaste(false); setPasteText(""); }} style={btnS}>Cancel</button>
          </div>
        </div>
      )}

      {/* Manual create form */}
      {showManual && (
        <div style={{ marginBottom: 16, padding: "16px 20px", border: "1px solid #e5e7eb", borderRadius: 8, background: "#f9fafb", maxWidth: 600 }}>
          <div style={{ fontWeight: 700, fontSize: 13, color: "#111827", marginBottom: 10 }}>+ New Correspondence</div>
          <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
            <div>
              <label style={lbl}>Direction</label>
              <select value={manualForm.direction} onChange={(e) => setManualForm(f => ({ ...f, direction: e.target.value }))} style={inp}>
                <option value="outbound">Outbound</option>
                <option value="inbound">Inbound</option>
                <option value="internal">Internal</option>
              </select>
            </div>
            <div>
              <label style={lbl}>Channel</label>
              <select value={manualForm.channel} onChange={(e) => setManualForm(f => ({ ...f, channel: e.target.value }))} style={inp}>
                <option value="email">Email</option>
                <option value="meeting">Meeting</option>
                <option value="letter">Letter</option>
                <option value="phone">Phone</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div style={{ flex: 1 }}>
              <label style={lbl}>Date</label>
              <input type="date" value={manualForm.date} onChange={(e) => setManualForm(f => ({ ...f, date: e.target.value }))} style={inp} />
            </div>
          </div>
          {(["from_addr", "to_addr", "cc_addr", "subject"] as const).map((f) => (
            <div key={f} style={{ marginBottom: 6 }}>
              <label style={lbl}>{f.replace(/_/g, " ")}</label>
              <input value={manualForm[f]} onChange={(e) => setManualForm(prev => ({ ...prev, [f]: e.target.value }))} style={inp} />
            </div>
          ))}
          <div style={{ marginBottom: 6 }}>
            <label style={lbl}>Body</label>
            <textarea value={manualForm.body} onChange={(e) => setManualForm(f => ({ ...f, body: e.target.value }))} rows={4} style={{ ...inp, resize: "vertical", fontFamily: "inherit" }} />
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={handleManualCreate} style={btnP}>Create</button>
            <button onClick={() => setShowManual(false)} style={btnS}>Cancel</button>
          </div>
        </div>
      )}

      {loading && <p style={{ color: "#6b7280", fontSize: 13 }}>Loading…</p>}
      {!loading && items.length === 0 && (
        <div style={{ textAlign: "center", padding: "2rem", color: "#9ca3af", border: "1px dashed #cbd5e1", borderRadius: 10 }}>
          No correspondence yet. Use "Paste Email" to import or "+ New" to create manually.
        </div>
      )}
      {items.map((c) => (
        <CorrCard key={c.id} c={c}
          onUpdated={(u) => setItems(prev => prev.map(x => x.id === u.id ? u : x))}
          onDeleted={(id) => setItems(prev => prev.filter(x => x.id !== id))} />
      ))}
    </div>
  );
}

const lbl: React.CSSProperties = { fontSize: 10, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 3, display: "block" };
const inp: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box", display: "block" };
const btnP: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer", fontWeight: 600, whiteSpace: "nowrap" };
const btnS: React.CSSProperties = { background: "#fff", color: "#374151", border: "1px solid #d1d5db", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer" };
