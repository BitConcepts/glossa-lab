/**
 * AIToolsView — specialized AI research tools.
 * Tools: Decipherment Assistant, Draft Paper Section, Sign Reading, Cross-Study Synthesis.
 */
import { useEffect, useState } from "react";
import {
  aiDecipher, aiDraftSection, aiSignReading, aiSynthesize,
  listExperiments, listStudies,
  type ExperimentMeta, type StudyResponse,
} from "../api";
import { useToast } from "../hooks/useToast";

type Tool = "decipher" | "draft" | "sign-reading" | "synthesis";

// ── Shared result panel ───────────────────────────────────────────────────────

function ResultPanel({ result, onClose }: { result: Record<string, unknown>; onClose: () => void }) {
  const skip = new Set(["sign_sequence", "sign_ids", "theory", "experiment_id", "study_ids"]);
  return (
    <div style={{ marginTop: 12, border: "1px solid #a78bfa", borderRadius: 8, overflow: "hidden" }}>
      <div style={{ display: "flex", justifyContent: "space-between", background: "#7c3aed", padding: "8px 14px" }}>
        <span style={{ color: "#fff", fontWeight: 700, fontSize: 13 }}>✨ AI Result</span>
        <button onClick={onClose} style={{ border: "none", background: "none", color: "#fff", cursor: "pointer", fontSize: 14 }}>×</button>
      </div>
      <div style={{ padding: "14px 16px", background: "#faf5ff", display: "flex", flexDirection: "column", gap: 10 }}>
        {Object.entries(result).filter(([k]) => !skip.has(k)).map(([k, v]) => {
          const label = k.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
          if (Array.isArray(v)) return (
            <div key={k}>
              <div style={sl}>{label}</div>
              <ul style={{ margin: 0, paddingLeft: 18 }}>
                {(v as unknown[]).map((x, i) => (
                  <li key={i} style={{ fontSize: 12, lineHeight: 1.5, color: "#374151" }}>
                    {typeof x === "object" ? JSON.stringify(x) : String(x)}
                  </li>
                ))}
              </ul>
            </div>
          );
          if (typeof v === "object" && v !== null) return (
            <div key={k}>
              <div style={sl}>{label}</div>
              <pre style={{ margin: 0, fontSize: 10, background: "#1e293b", color: "#e2e8f0", padding: "6px 10px", borderRadius: 4, overflowX: "auto" }}>
                {JSON.stringify(v, null, 2)}
              </pre>
            </div>
          );
          return (
            <div key={k}>
              <div style={sl}>{label}</div>
              <p style={{ margin: 0, fontSize: 13, color: "#374151", lineHeight: 1.6 }}>{String(v)}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Tools ─────────────────────────────────────────────────────────────────────

function DecipherTool() {
  const { toast } = useToast();
  const [signs, setSigns] = useState("740 400 700 520");
  const [theory, setTheory] = useState("dravidian");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const run = async () => {
    const seq = signs.trim().split(/\s+/).filter(Boolean);
    if (!seq.length) { toast("Enter sign IDs", "warning"); return; }
    setLoading(true); setResult(null);
    try { setResult(await aiDecipher({ sign_sequence: seq, theory }) as Record<string, unknown>); }
    catch (e) { toast(e instanceof Error ? e.message : "AI error", "error"); }
    finally { setLoading(false); }
  };

  return (
    <div>
      <h3 style={{ margin: "0 0 10px", fontSize: 14, color: "#374151" }}>🔤 Indus Decipherment Assistant</h3>
      <p style={{ margin: "0 0 12px", fontSize: 13, color: "#6b7280", lineHeight: 1.5 }}>
        Apply a decipherment theory to an Indus sign sequence. Enter Mahadevan sign IDs or symbolic labels.
      </p>
      <div style={{ display: "flex", gap: 8, marginBottom: 10, flexWrap: "wrap" }}>
        <input value={signs} onChange={(e) => setSigns(e.target.value)} placeholder="Sign IDs (space-separated, e.g. 740 400 700)"
          style={{ ...inputStyle, flex: 1 }} />
        <select value={theory} onChange={(e) => setTheory(e.target.value)} style={{ ...inputStyle, width: 160 }}>
          <option value="dravidian">Dravidian</option>
          <option value="linguistic">Linguistic</option>
          <option value="logo-syllabic">Logo-syllabic</option>
          <option value="acrophonic">Acrophonic</option>
        </select>
        <button onClick={run} disabled={loading} style={btnPurple}>{loading ? "✨ Deciphering…" : "✨ Decipher"}</button>
      </div>
      {result && <ResultPanel result={result} onClose={() => setResult(null)} />}
    </div>
  );
}

function DraftTool({ experiments }: { experiments: ExperimentMeta[] }) {
  const { toast } = useToast();
  const [expId, setExpId] = useState("");
  const [section, setSection] = useState("results");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const run = async () => {
    if (!expId) { toast("Select an experiment", "warning"); return; }
    setLoading(true); setResult(null);
    try { setResult(await aiDraftSection({ experiment_id: expId, section_type: section }) as Record<string, unknown>); }
    catch (e) { toast(e instanceof Error ? e.message : "AI error", "error"); }
    finally { setLoading(false); }
  };

  return (
    <div>
      <h3 style={{ margin: "0 0 10px", fontSize: 14, color: "#374151" }}>📝 Draft Paper Section</h3>
      <p style={{ margin: "0 0 12px", fontSize: 13, color: "#6b7280", lineHeight: 1.5 }}>
        Generate a journal-quality paper section from experiment results.
      </p>
      <div style={{ display: "flex", gap: 8, marginBottom: 10, flexWrap: "wrap" }}>
        <select value={expId} onChange={(e) => setExpId(e.target.value)} style={{ ...inputStyle, flex: 1 }}>
          <option value="">— select experiment —</option>
          {experiments.map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
        </select>
        <select value={section} onChange={(e) => setSection(e.target.value)} style={{ ...inputStyle, width: 140 }}>
          {["abstract", "introduction", "methods", "results", "discussion"].map((s) => (
            <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
          ))}
        </select>
        <button onClick={run} disabled={loading} style={btnPurple}>{loading ? "✨ Drafting…" : "✨ Draft"}</button>
      </div>
      {result && typeof result.text === "string" && (
        <div style={{ marginTop: 12, padding: "14px 16px", background: "#f8f9fa", border: "1px solid #e5e7eb", borderRadius: 8 }}>
          <div style={sl}>Draft {result.section_type as string} — {result.suggested_title as string}</div>
          <p style={{ margin: "8px 0 0", fontSize: 13, lineHeight: 1.8, color: "#111827", fontFamily: "Georgia, serif" }}>
            {result.text}
          </p>
          {Array.isArray(result.keywords) && (result.keywords as string[]).length > 0 && (
            <div style={{ marginTop: 10, fontSize: 11, color: "#6b7280" }}>
              Keywords: {(result.keywords as string[]).join(", ")}
            </div>
          )}
          <button onClick={() => { navigator.clipboard.writeText(result.text as string); toast("Copied", "success"); }}
            style={{ ...btnSecondary, marginTop: 10, fontSize: 11 }}>Copy Text</button>
        </div>
      )}
    </div>
  );
}

function SignReadingTool() {
  const { toast } = useToast();
  const [signIds, setSignIds] = useState("740 400 700");
  const [theory, setTheory] = useState("dravidian");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const run = async () => {
    const ids = signIds.trim().split(/\s+/).filter(Boolean);
    if (!ids.length) { toast("Enter sign IDs", "warning"); return; }
    setLoading(true); setResult(null);
    try { setResult(await aiSignReading({ sign_ids: ids, theory, context }) as Record<string, unknown>); }
    catch (e) { toast(e instanceof Error ? e.message : "AI error", "error"); }
    finally { setLoading(false); }
  };

  return (
    <div>
      <h3 style={{ margin: "0 0 10px", fontSize: 14, color: "#374151" }}>🔍 Sign Reading Suggestions</h3>
      <p style={{ margin: "0 0 12px", fontSize: 13, color: "#6b7280", lineHeight: 1.5 }}>
        Get probabilistic phonetic and semantic readings for Indus Script sign IDs using a selected theory.
      </p>
      <div style={{ display: "flex", gap: 8, marginBottom: 8, flexWrap: "wrap" }}>
        <input value={signIds} onChange={(e) => setSignIds(e.target.value)} placeholder="Sign IDs: 740 400 700"
          style={{ ...inputStyle, flex: 1 }} />
        <select value={theory} onChange={(e) => setTheory(e.target.value)} style={{ ...inputStyle, width: 140 }}>
          <option value="dravidian">Dravidian</option>
          <option value="linguistic">Linguistic</option>
          <option value="logo-syllabic">Logo-syllabic</option>
          <option value="acrophonic">Acrophonic</option>
        </select>
      </div>
      <input value={context} onChange={(e) => setContext(e.target.value)} placeholder="Context (optional: inscription type, find location…)"
        style={{ ...inputStyle, marginBottom: 10 }} />
      <button onClick={run} disabled={loading} style={btnPurple}>{loading ? "✨ Reading…" : "✨ Get Readings"}</button>
      {result && <ResultPanel result={result} onClose={() => setResult(null)} />}
    </div>
  );
}

function SynthesisTool({ studies }: { studies: StudyResponse[] }) {
  const { toast } = useToast();
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const toggle = (id: string) =>
    setSelectedIds((prev) => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);

  const run = async () => {
    if (selectedIds.length < 2) { toast("Select at least 2 studies", "warning"); return; }
    setLoading(true); setResult(null);
    try { setResult(await aiSynthesize({ study_ids: selectedIds, question }) as Record<string, unknown>); }
    catch (e) { toast(e instanceof Error ? e.message : "AI error", "error"); }
    finally { setLoading(false); }
  };

  return (
    <div>
      <h3 style={{ margin: "0 0 10px", fontSize: 14, color: "#374151" }}>🔬 Cross-Study Synthesis</h3>
      <p style={{ margin: "0 0 12px", fontSize: 13, color: "#6b7280", lineHeight: 1.5 }}>
        Find patterns, contradictions, and insights across multiple studies.
      </p>
      <div style={{ marginBottom: 10 }}>
        <div style={sl}>Select studies (2–6)</div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 8 }}>
          {studies.map((s) => (
            <button key={s.id} onClick={() => toggle(s.id)}
              style={{ padding: "3px 10px", borderRadius: 6, border: "1px solid", cursor: "pointer", fontSize: 11,
                background: selectedIds.includes(s.id) ? "#7c3aed" : "#fff",
                borderColor: selectedIds.includes(s.id) ? "#7c3aed" : "#d1d5db",
                color: selectedIds.includes(s.id) ? "#fff" : "#374151" }}>
              {s.name.slice(0, 25)}
            </button>
          ))}
        </div>
        <input value={question} onChange={(e) => setQuestion(e.target.value)}
          placeholder="Optional: specific research question to address…"
          style={{ ...inputStyle, marginBottom: 10 }} />
        <button onClick={run} disabled={loading || selectedIds.length < 2} style={btnPurple}>
          {loading ? "✨ Synthesising…" : "✨ Synthesise"}
        </button>
      </div>
      {result && <ResultPanel result={result} onClose={() => setResult(null)} />}
    </div>
  );
}

// ── Main view ─────────────────────────────────────────────────────────────────

export function AIToolsView() {
  const [activeTool, setActiveTool] = useState<Tool>("decipher");
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [studies, setStudies] = useState<StudyResponse[]>([]);

  useEffect(() => {
    listExperiments().then(setExperiments).catch(() => {});
    listStudies().then(setStudies).catch(() => {});
  }, []);

  const tools: Array<{ id: Tool; label: string; icon: string }> = [
    { id: "decipher", label: "Decipherment", icon: "🔤" },
    { id: "draft", label: "Draft Paper", icon: "📝" },
    { id: "sign-reading", label: "Sign Reading", icon: "🔍" },
    { id: "synthesis", label: "Cross-Study Synthesis", icon: "🔬" },
  ];

  return (
    <div>
      <h2 style={{ margin: "0 0 0.75rem" }}>✨ AI Research Tools</h2>
      <p style={{ margin: "0 0 1.25rem", fontSize: 13, color: "#6b7280" }}>
        Specialized AI tools for Indus Script research — decipherment, academic writing, and cross-study analysis.
      </p>

      <div style={{ display: "flex", gap: 0, borderBottom: "2px solid #e5e7eb", marginBottom: "1.5rem" }}>
        {tools.map((t) => (
          <button key={t.id} onClick={() => setActiveTool(t.id)}
            style={{ padding: "10px 18px", border: "none", borderBottom: activeTool === t.id ? "2px solid #7c3aed" : "2px solid transparent",
              marginBottom: -2, background: "none", cursor: "pointer", fontSize: 13,
              fontWeight: activeTool === t.id ? 700 : 400,
              color: activeTool === t.id ? "#7c3aed" : "#6b7280" }}>
            {t.icon} {t.label}
          </button>
        ))}
      </div>

      {activeTool === "decipher" && <DecipherTool />}
      {activeTool === "draft" && <DraftTool experiments={experiments} />}
      {activeTool === "sign-reading" && <SignReadingTool />}
      {activeTool === "synthesis" && <SynthesisTool studies={studies} />}
    </div>
  );
}

const sl: React.CSSProperties = { fontSize: 10, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 };
const inputStyle: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box", display: "block" };
const btnPurple: React.CSSProperties = { background: "#7c3aed", color: "#fff", border: "none", borderRadius: 4, padding: "7px 16px", fontSize: 12, cursor: "pointer", fontWeight: 600, whiteSpace: "nowrap" };
const btnSecondary: React.CSSProperties = { background: "#fff", color: "#374151", border: "1px solid #d1d5db", borderRadius: 4, padding: "5px 12px", fontSize: 12, cursor: "pointer" };
