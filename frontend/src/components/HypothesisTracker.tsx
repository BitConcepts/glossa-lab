/**
 * HypothesisTracker — create, track, and manage research hypotheses.
 * Statuses: active → confirmed | refuted | paused.
 * Links hypotheses to experiments and studies.
 */
import { useEffect, useState } from "react";
import {
  aiGenerateHypotheses, aiExperimentChain,
  createHypothesis, deleteHypothesis, listHypotheses, listStudies, updateHypothesis,
  type Hypothesis,
} from "../api";
import { useToast } from "../hooks/useToast";

const STATUS_COLORS: Record<string, { bg: string; text: string }> = {
  active:    { bg: "#eff6ff", text: "#2563eb" },
  confirmed: { bg: "#f0fdf4", text: "#16a34a" },
  refuted:   { bg: "#fef2f2", text: "#dc2626" },
  paused:    { bg: "#fef3c7", text: "#d97706" },
};

function HypCard({ h, onUpdated, onDeleted }: {
  h: Hypothesis; onUpdated: (h: Hypothesis) => void; onDeleted: (id: string) => void;
}) {
  const { toast } = useToast();
  const [expanded, setExpanded] = useState(false);
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(h.title);
  const [statement, setStatement] = useState(h.statement);
  const [, ] = useState(h.status); // unused — status changed via changeStatus()
  const [newEvidence, setNewEvidence] = useState("");
  const [saving, setSaving] = useState(false);
  const [chainLoading, setChainLoading] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [chain, setChain] = useState<Record<string, any> | null>(null);

  const sc = STATUS_COLORS[h.status] ?? STATUS_COLORS.active;

  const save = async () => {
    setSaving(true);
    try {
      const updated = await updateHypothesis(h.id, { title, statement, status });
      onUpdated(updated); setEditing(false);
      toast("Hypothesis saved", "success");
    } catch (e) { toast(e instanceof Error ? e.message : "Save failed", "error"); }
    finally { setSaving(false); }
  };

  const addEvidence = async () => {
    if (!newEvidence.trim()) return;
    try {
      const updated = await updateHypothesis(h.id, { evidence: [...h.evidence, newEvidence.trim()] });
      onUpdated(updated); setNewEvidence("");
    } catch (e) { toast(e instanceof Error ? e.message : "Failed", "error"); }
  };

  const removeEvidence = async (i: number) => {
    try {
      const updated = await updateHypothesis(h.id, { evidence: h.evidence.filter((_, j) => j !== i) });
      onUpdated(updated);
    } catch (e) { toast(e instanceof Error ? e.message : "Failed", "error"); }
  };

  const planChain = async () => {
    setChainLoading(true); setChain(null);
    try { setChain(await aiExperimentChain({ hypothesis: h.statement || h.title })); }
    catch (e) { toast(e instanceof Error ? e.message : "AI error", "error"); }
    finally { setChainLoading(false); }
  };

  const changeStatus = async (s: string) => {
    try {
      const updated = await updateHypothesis(h.id, { status: s });
      onUpdated(updated); toast(`Status → ${s}`, "info");
    } catch { toast("Update failed", "error"); }
  };

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden", marginBottom: 8 }}>
      <div style={{ display: "flex", gap: 10, padding: "10px 14px", background: "#fafafa", cursor: "pointer", alignItems: "center" }}
        onClick={() => setExpanded(x => !x)}>
        <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 8, background: sc.bg, color: sc.text, fontWeight: 700, whiteSpace: "nowrap" }}>
          {h.status}
        </span>
        <span style={{ flex: 1, fontWeight: 600, fontSize: 13, color: "#111827" }}>{h.title}</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{h.evidence.length} evidence</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{h.updated_at.slice(0, 10)}</span>
        <button onClick={(e) => { e.stopPropagation(); if (!confirm("Delete?")) return; deleteHypothesis(h.id).then(() => onDeleted(h.id)).catch(() => toast("Delete failed", "error")); }}
          style={{ border: "1px solid #fca5a5", background: "none", color: "#dc2626", borderRadius: 4, fontSize: 10, padding: "1px 7px", cursor: "pointer" }}>🗑</button>
        <span style={{ fontSize: 14, color: "#9ca3af" }}>{expanded ? "▲" : "▼"}</span>
      </div>

      {expanded && (
        <div style={{ padding: "14px 16px" }} onClick={(e) => e.stopPropagation()}>
          {/* Status switcher */}
          <div style={{ display: "flex", gap: 6, marginBottom: 12 }}>
            {["active", "confirmed", "refuted", "paused"].map((s) => {
              const c = STATUS_COLORS[s];
              return (
                <button key={s} onClick={() => changeStatus(s)}
                  style={{ padding: "3px 10px", borderRadius: 6, border: `1px solid ${h.status === s ? c.text : "#d1d5db"}`, background: h.status === s ? c.bg : "#fff", color: h.status === s ? c.text : "#6b7280", cursor: "pointer", fontSize: 11, fontWeight: h.status === s ? 700 : 400 }}>
                  {s}
                </button>
              );
            })}
          </div>

          {editing ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 8, maxWidth: 560, marginBottom: 12 }}>
              <input value={title} onChange={(e) => setTitle(e.target.value)} style={inputStyle} placeholder="Title" />
              <textarea value={statement} onChange={(e) => setStatement(e.target.value)} rows={4}
                style={{ ...inputStyle, fontFamily: "inherit", resize: "vertical" }} placeholder="Full hypothesis statement…" />
              <div style={{ display: "flex", gap: 8 }}>
                <button onClick={save} disabled={saving} style={btnPrimary}>{saving ? "Saving…" : "Save"}</button>
                <button onClick={() => setEditing(false)} style={btnSecondary}>Cancel</button>
              </div>
            </div>
          ) : (
            <div style={{ marginBottom: 12 }}>
              {h.statement && <p style={{ margin: "0 0 8px", fontSize: 13, lineHeight: 1.6, color: "#374151" }}>{h.statement}</p>}
              <button onClick={() => setEditing(true)} style={{ ...btnSecondary, fontSize: 11, padding: "3px 10px" }}>✎ Edit</button>
            </div>
          )}

          {/* Evidence */}
          <div style={{ marginBottom: 12 }}>
            <div style={sLabel}>Evidence ({h.evidence.length})</div>
            {h.evidence.map((ev, i) => (
              <div key={i} style={{ display: "flex", gap: 6, alignItems: "flex-start", marginBottom: 4 }}>
                <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#2563eb", marginTop: 5, flexShrink: 0 }} />
                <span style={{ flex: 1, fontSize: 12, color: "#374151", lineHeight: 1.5 }}>{ev}</span>
                <button onClick={() => removeEvidence(i)} style={{ border: "none", background: "none", color: "#9ca3af", cursor: "pointer", fontSize: 12 }}>×</button>
              </div>
            ))}
            <div style={{ display: "flex", gap: 6, marginTop: 6 }}>
              <input value={newEvidence} onChange={(e) => setNewEvidence(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter") addEvidence(); }}
                placeholder="Add evidence note…" style={{ ...inputStyle, flex: 1, fontSize: 12 }} />
              <button onClick={addEvidence} style={btnPrimary}>+</button>
            </div>
          </div>

          {/* AI Experiment Chain */}
          <div>
            <button onClick={planChain} disabled={chainLoading} style={{ ...btnPrimary, background: "#7c3aed" }}>
              {chainLoading ? "✨ Planning…" : "✨ Plan Experiment Chain"}
            </button>
            {chain && (
              <div style={{ marginTop: 10, background: "#faf5ff", border: "1px solid #a78bfa", borderRadius: 8, padding: "12px 14px" }}>
                <div style={sLabel}>Experiment Chain</div>
                {(chain.chain ?? []).map((step: { step: number; experiment_name: string; purpose: string; expected_output: string }, i: number) => (
                  <div key={i} style={{ display: "flex", gap: 10, marginBottom: 8, padding: "8px 10px", background: "#fff", borderRadius: 6, border: "1px solid #e5e7eb" }}>
                    <span style={{ width: 22, height: 22, borderRadius: "50%", background: "#7c3aed", color: "#fff", fontSize: 11, fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{step.step}</span>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 600, fontSize: 12, color: "#374151" }}>{step.experiment_name}</div>
                      <div style={{ fontSize: 11, color: "#6b7280" }}>{step.purpose}</div>
                    </div>
                  </div>
                ))}
                {chain.success_criteria && <p style={{ margin: "8px 0 0", fontSize: 12, color: "#7c3aed", fontStyle: "italic" }}>Success: {chain.success_criteria}</p>}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export function HypothesisTracker() {
  const { toast } = useToast();
  const [hypotheses, setHypotheses] = useState<Hypothesis[]>([]);
  const [loading, setLoading] = useState(true);
  const [newTitle, setNewTitle] = useState("");
  const [aiContext, setAiContext] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [aiResult, setAiResult] = useState<Record<string, any> | null>(null);
  const [studies, setStudies] = useState<{ id: string; name: string }[]>([]);
  const [aiStudyId, setAiStudyId] = useState("");
  const [filter, setFilter] = useState<"all" | "active" | "confirmed" | "refuted" | "paused">("all");

  const load = async () => {
    setLoading(true);
    try { setHypotheses(await listHypotheses()); }
    catch { toast("Failed to load", "error"); }
    finally { setLoading(false); }
  };

  useEffect(() => {
    load();
    listStudies().then((s) => setStudies(s.map((x) => ({ id: x.id, name: x.name })))).catch(() => {});
  }, []);

  const addHyp = async () => {
    if (!newTitle.trim()) return;
    try {
      const h = await createHypothesis({ title: newTitle.trim() });
      setHypotheses((prev) => [h, ...prev]); setNewTitle("");
      toast("Hypothesis created", "success");
    } catch { toast("Failed", "error"); }
  };

  const handleAIGenerate = async () => {
    setAiLoading(true); setAiResult(null);
    try {
      const r = await aiGenerateHypotheses({ study_id: aiStudyId || undefined, context: aiContext });
      setAiResult(r);
    } catch (e) { toast(e instanceof Error ? e.message : "AI error", "error"); }
    finally { setAiLoading(false); }
  };

  const importHypothesis = async (h: { title: string; statement: string }) => {
    try {
      const created = await createHypothesis({ title: h.title, statement: h.statement });
      setHypotheses((prev) => [created, ...prev]); toast("Imported", "success");
    } catch { toast("Import failed", "error"); }
  };

  const visible = filter === "all" ? hypotheses : hypotheses.filter((h) => h.status === filter);

  const counts = hypotheses.reduce((acc, h) => ({ ...acc, [h.status]: (acc[h.status] ?? 0) + 1 }), {} as Record<string, number>);

  return (
    <div>
      <h2 style={{ margin: "0 0 0.75rem" }}>Hypothesis Tracker</h2>
      <p style={{ margin: "0 0 1.25rem", fontSize: 13, color: "#6b7280" }}>
        Track research hypotheses from active investigation through confirmation or refutation.
      </p>

      {/* Stats */}
      <div style={{ display: "flex", gap: 8, marginBottom: "1.25rem", flexWrap: "wrap" }}>
        {["active", "confirmed", "refuted", "paused"].map((s) => {
          const c = STATUS_COLORS[s];
          return (
            <div key={s} style={{ padding: "6px 14px", borderRadius: 8, background: c.bg, border: `1px solid ${c.text}40` }}>
              <span style={{ fontWeight: 700, color: c.text, fontSize: 18, fontFamily: "monospace" }}>{counts[s] ?? 0}</span>
              <span style={{ fontSize: 11, color: c.text, marginLeft: 5 }}>{s}</span>
            </div>
          );
        })}
      </div>

      {/* Quick add */}
      <div style={{ display: "flex", gap: 8, marginBottom: "1.25rem" }}>
        <input value={newTitle} onChange={(e) => setNewTitle(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") addHyp(); }}
          placeholder="New hypothesis title…" style={{ ...inputStyle, flex: 1 }} />
        <button onClick={addHyp} disabled={!newTitle.trim()} style={btnPrimary}>+ Add</button>
      </div>

      {/* AI generate */}
      <details style={{ marginBottom: "1.25rem" }}>
        <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13, color: "#7c3aed" }}>✨ AI Generate Hypotheses</summary>
        <div style={{ marginTop: 10, padding: "14px 16px", border: "1px solid #a78bfa", borderRadius: 8, background: "#faf5ff" }}>
          {studies.length > 0 && (
            <div style={{ marginBottom: 8 }}>
              <label style={sLabel}>Link to study (optional)</label>
              <select value={aiStudyId} onChange={(e) => setAiStudyId(e.target.value)} style={inputStyle}>
                <option value="">— none —</option>
                {studies.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
              </select>
            </div>
          )}
          <div style={{ marginBottom: 8 }}>
            <label style={sLabel}>Context (optional)</label>
            <textarea value={aiContext} onChange={(e) => setAiContext(e.target.value)} rows={3}
              style={{ ...inputStyle, fontFamily: "inherit", resize: "vertical" }} placeholder="Describe current research state or findings…" />
          </div>
          <button onClick={handleAIGenerate} disabled={aiLoading} style={{ ...btnPrimary, background: "#7c3aed" }}>
            {aiLoading ? "✨ Generating…" : "✨ Generate"}
          </button>
          {aiResult?.hypotheses && (
            <div style={{ marginTop: 12 }}>
              <div style={sLabel}>Suggested Hypotheses</div>
              {aiResult.hypotheses.map((h: { title: string; statement: string; priority: string }, i: number) => (
                <div key={i} style={{ padding: "10px 12px", border: "1px solid #e5e7eb", borderRadius: 6, marginBottom: 6, background: "#fff" }}>
                  <div style={{ fontWeight: 600, fontSize: 13, color: "#111827", marginBottom: 3 }}>{h.title}</div>
                  <p style={{ margin: "0 0 6px", fontSize: 12, color: "#374151" }}>{h.statement}</p>
                  <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                    <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 4, background: "#f3f4f6", color: "#6b7280" }}>{h.priority}</span>
                    <button onClick={() => importHypothesis(h)} style={{ ...btnPrimary, fontSize: 11, padding: "2px 8px" }}>Import</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </details>

      {/* Filter */}
      <div style={{ display: "flex", gap: 6, marginBottom: "1rem", flexWrap: "wrap" }}>
        {(["all", "active", "confirmed", "refuted", "paused"] as const).map((f) => (
          <button key={f} onClick={() => setFilter(f)}
            style={{ padding: "3px 12px", borderRadius: 6, border: "1px solid", cursor: "pointer", fontSize: 12,
              background: filter === f ? "#1e3a5f" : "#fff", borderColor: filter === f ? "#1e3a5f" : "#d1d5db",
              color: filter === f ? "#fff" : "#374151", fontWeight: filter === f ? 700 : 400 }}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
        <span style={{ fontSize: 12, color: "#9ca3af", marginLeft: "auto", alignSelf: "center" }}>{visible.length} hypothesis</span>
      </div>

      {loading && <p style={{ color: "#6b7280", fontSize: 13 }}>Loading…</p>}
      {!loading && visible.length === 0 && <p style={{ color: "#6b7280", fontSize: 13 }}>No hypotheses yet. Create one above.</p>}
      {visible.map((h) => (
        <HypCard key={h.id} h={h}
          onUpdated={(updated) => setHypotheses((prev) => prev.map((x) => x.id === updated.id ? updated : x))}
          onDeleted={(id) => setHypotheses((prev) => prev.filter((x) => x.id !== id))} />
      ))}
    </div>
  );
}

const sLabel: React.CSSProperties = { fontSize: 10, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 };
const inputStyle: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box", display: "block" };
const btnPrimary: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer", fontWeight: 600, whiteSpace: "nowrap" };
const btnSecondary: React.CSSProperties = { background: "#fff", color: "#374151", border: "1px solid #d1d5db", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer" };
