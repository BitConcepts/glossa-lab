/**
 * AIToolsView — the central AI hub.
 *
 * Surfaces every backend AI capability:
 *   /ai/chat                — freeform conversational helper (handled by Glossa AI side panel)
 *   /ai/decipher            — sequence decipherment
 *   /ai/sign-reading        — probabilistic sign readings
 *   /ai/hypotheses/generate — hypothesis brainstorming
 *   /ai/experiment-chain    — plan a sequence of experiments
 *   /ai/draft-section       — paper paragraph from an experiment
 *   /ai/synthesize          — cross-study synthesis
 *   /ai/report-synthesis    — multi-report synthesis
 *   /ai/research-context    — read live research context
 *   /ai/execute-action      — run AI-proposed actions (used internally)
 *
 * Grouped into capability categories with one-click cards.
 */
import { useEffect, useState } from "react";
import {
  aiDecipher, aiDraftSection, aiExperimentChain, aiGenerateHypotheses,
  aiReportSynthesis, aiSignReading, aiSynthesize,
  getResearchContext, listExperiments, listStudies,
  type ExperimentMeta, type ResearchContextResponse, type StudyResponse,
} from "../api";
import { useToast } from "../hooks/useToast";

type Tool =
  | "decipher" | "sign-reading"
  | "hypotheses" | "chain"
  | "draft" | "synthesis" | "report-synth"
  | "context";

interface ToolMeta {
  id: Tool;
  label: string;
  icon: string;
  group: string;
  blurb: string;
}

const TOOLS: ToolMeta[] = [
  { id: "decipher",     label: "Decipherment",        icon: "🔤", group: "Decipherment",        blurb: "Apply a theory to a sign sequence" },
  { id: "sign-reading", label: "Sign Reading",         icon: "🔍", group: "Decipherment",        blurb: "Probabilistic phonetic + semantic readings" },
  { id: "hypotheses",   label: "Hypothesis Generator", icon: "💡", group: "Hypothesis Engine",  blurb: "Generate testable hypotheses from a study" },
  { id: "chain",        label: "Experiment Chain",     icon: "🔗", group: "Hypothesis Engine",  blurb: "Plan a sequence of experiments" },
  { id: "draft",        label: "Draft Paper Section",  icon: "📝", group: "Writing & Synthesis", blurb: "Journal-quality paragraph from an experiment" },
  { id: "synthesis",    label: "Cross-Study Synthesis",icon: "🔬", group: "Writing & Synthesis", blurb: "Patterns + contradictions across studies" },
  { id: "report-synth", label: "Multi-Report Synthesis",icon: "📚", group: "Writing & Synthesis", blurb: "Combine multiple report JSONs into one narrative" },
  { id: "context",      label: "Research Context",     icon: "🧠", group: "Agent Console",      blurb: "Inspect what the AI sees on every call" },
];
const GROUPS = Array.from(new Set(TOOLS.map((t) => t.group)));

// Silent copy button with brief ✓ visual feedback
function CopyTextButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={() => navigator.clipboard.writeText(text).then(() => { setCopied(true); setTimeout(() => setCopied(false), 1400); })}
      style={{ ...btnSecondary, marginTop: 10, fontSize: 11,
        background: copied ? "#dcfce7" : undefined,
        color: copied ? "#16a34a" : undefined,
        transition: "background 0.2s, color 0.2s" }}
    >
      {copied ? "✓ Copied" : "Copy Text"}
    </button>
  );
}

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
          <CopyTextButton text={result.text as string} />
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

// ── Hypothesis Generator ─────────────────────────────────────────────

function HypothesesTool({ studies }: { studies: StudyResponse[] }) {
  const { toast } = useToast();
  const [studyId, setStudyId] = useState("");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const run = async () => {
    setLoading(true); setResult(null);
    try {
      const r = await aiGenerateHypotheses({
        study_id: studyId || undefined,
        context: context || undefined,
      });
      setResult(r as Record<string, unknown>);
    } catch (e) {
      toast(e instanceof Error ? e.message : "AI error", "error");
    } finally { setLoading(false); }
  };

  return (
    <div>
      <h3 style={{ margin: "0 0 10px", fontSize: 14, color: "#374151" }}>💡 Hypothesis Generator</h3>
      <p style={{ margin: "0 0 12px", fontSize: 13, color: "#6b7280", lineHeight: 1.5 }}>
        Ask the AI for testable, falsifiable hypotheses, optionally seeded by a
        specific study or freeform context (e.g. “what would distinguish
        Dravidian vs Indo-Aryan if M-410 contains a verb final?”).
      </p>
      <div style={{ display: "grid", gap: 8, marginBottom: 10 }}>
        <select value={studyId} onChange={(e) => setStudyId(e.target.value)} style={inputStyle}>
          <option value="">— no study (freeform) —</option>
          {studies.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
        <textarea value={context} onChange={(e) => setContext(e.target.value)}
          placeholder="Optional context (research question, partial findings, constraints…)"
          rows={3} style={{ ...inputStyle, resize: "vertical" }} />
        <div>
          <button onClick={run} disabled={loading} style={btnPurple}>
            {loading ? "✨ Thinking…" : "✨ Generate hypotheses"}
          </button>
        </div>
      </div>
      {result && <ResultPanel result={result} onClose={() => setResult(null)} />}
    </div>
  );
}

// ── Experiment Chain Planner ────────────────────────────────────────

function ExperimentChainTool({ experiments }: { experiments: ExperimentMeta[] }) {
  const { toast } = useToast();
  const [hypothesis, setHypothesis] = useState("");
  const [picked, setPicked] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const togglePick = (id: string) =>
    setPicked((p) => (p.includes(id) ? p.filter((x) => x !== id) : [...p, id]));

  const run = async () => {
    if (!hypothesis.trim()) { toast("Enter a hypothesis", "warning"); return; }
    setLoading(true); setResult(null);
    try {
      const r = await aiExperimentChain({
        hypothesis: hypothesis.trim(),
        available_experiment_ids: picked.length ? picked : undefined,
      });
      setResult(r as Record<string, unknown>);
    } catch (e) {
      toast(e instanceof Error ? e.message : "AI error", "error");
    } finally { setLoading(false); }
  };

  return (
    <div>
      <h3 style={{ margin: "0 0 10px", fontSize: 14, color: "#374151" }}>🔗 Experiment Chain Planner</h3>
      <p style={{ margin: "0 0 12px", fontSize: 13, color: "#6b7280", lineHeight: 1.5 }}>
        Given a hypothesis and (optionally) a set of available experiments, the
        AI proposes an ordered chain of experiments that would confirm,
        constrain, or falsify it.
      </p>
      <textarea value={hypothesis} onChange={(e) => setHypothesis(e.target.value)}
        placeholder="Hypothesis to test (e.g. ‘M77 long inscriptions are linguistic; short ones are administrative tags.’)"
        rows={3} style={{ ...inputStyle, marginBottom: 8, resize: "vertical" }} />
      <div style={{ marginBottom: 8 }}>
        <div style={{ fontSize: 11, fontWeight: 700, color: "#6b7280", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 }}>
          Constrain to specific experiments (optional)
        </div>
        <div style={{ display: "flex", gap: 4, flexWrap: "wrap", maxHeight: 120, overflowY: "auto" }}>
          {experiments.map((e) => (
            <button key={e.id} onClick={() => togglePick(e.id)}
              style={{ padding: "3px 9px", borderRadius: 5, border: "1px solid",
                cursor: "pointer", fontSize: 10,
                background: picked.includes(e.id) ? "#7c3aed" : "#fff",
                borderColor: picked.includes(e.id) ? "#7c3aed" : "#d1d5db",
                color: picked.includes(e.id) ? "#fff" : "#374151" }}>
              {e.id}
            </button>
          ))}
        </div>
      </div>
      <button onClick={run} disabled={loading} style={btnPurple}>
        {loading ? "✨ Planning…" : "✨ Plan chain"}
      </button>
      {result && <ResultPanel result={result} onClose={() => setResult(null)} />}
    </div>
  );
}

// ── Multi-Report Synthesis ──────────────────────────────────────────

function ReportSynthTool() {
  const { toast } = useToast();
  const [files, setFiles] = useState<Array<{ name: string; filename: string; data: unknown }>>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [out, setOut] = useState<{ title: string; markdown: string; n_reports: number } | null>(null);

  const onPick = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const fl = Array.from(e.target.files ?? []);
    const next: typeof files = [];
    for (const f of fl) {
      try {
        const text = await f.text();
        const data = JSON.parse(text);
        next.push({ name: f.name.replace(/\.json$/i, ""), filename: f.name, data });
      } catch (err) {
        toast(`${f.name}: ${err instanceof Error ? err.message : "not valid JSON"}`, "warning");
      }
    }
    setFiles((prev) => [...prev, ...next]);
  };

  const run = async () => {
    if (files.length === 0) { toast("Pick at least one report JSON", "warning"); return; }
    setLoading(true); setOut(null);
    try {
      const r = await aiReportSynthesis({
        report_contents: files,
        title: title.trim() || undefined,
      });
      setOut(r);
    } catch (e) {
      toast(e instanceof Error ? e.message : "AI error", "error");
    } finally { setLoading(false); }
  };

  return (
    <div>
      <h3 style={{ margin: "0 0 10px", fontSize: 14, color: "#374151" }}>📚 Multi-Report Synthesis</h3>
      <p style={{ margin: "0 0 12px", fontSize: 13, color: "#6b7280", lineHeight: 1.5 }}>
        Drop multiple report JSONs (e.g. from <code>reports/</code>) and the AI
        produces a unified, citation-aware synthesis. Useful for end-of-phase
        write-ups across many experiments.
      </p>
      <input value={title} onChange={(e) => setTitle(e.target.value)}
        placeholder="Optional title (e.g. ‘Phase-19 results: spectral entropy analysis’)"
        style={{ ...inputStyle, marginBottom: 8 }} />
      <input type="file" multiple accept="application/json,.json" onChange={onPick}
        style={{ marginBottom: 8 }} />
      {files.length > 0 && (
        <div style={{ fontSize: 11, color: "#374151", marginBottom: 8 }}>
          <strong>Reports loaded:</strong> {files.map((f) => f.name).join(", ")}
          <button onClick={() => setFiles([])} style={{ marginLeft: 8, fontSize: 10,
            border: "1px solid #d1d5db", borderRadius: 4, background: "#fff",
            cursor: "pointer", padding: "1px 7px" }}>Clear</button>
        </div>
      )}
      <button onClick={run} disabled={loading || files.length === 0} style={btnPurple}>
        {loading ? "✨ Synthesising…" : "✨ Synthesise reports"}
      </button>
      {out && (
        <div style={{ marginTop: 12, padding: "14px 16px", background: "#f8f9fa",
          border: "1px solid #e5e7eb", borderRadius: 8 }}>
          <div style={sl}>{out.title} — {out.n_reports} report(s)</div>
          <pre style={{ margin: "8px 0 0", fontSize: 12, color: "#111827",
            whiteSpace: "pre-wrap", lineHeight: 1.6 }}>{out.markdown}</pre>
          <CopyTextButton text={out.markdown} />
        </div>
      )}
    </div>
  );
}

// ── Research Context Inspector ────────────────────────────────────
function ContextTool() {
  const { toast } = useToast();
  const [data, setData] = useState<ResearchContextResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const refresh = async () => {
    setLoading(true);
    try { setData(await getResearchContext()); }
    catch (e) { toast(e instanceof Error ? e.message : "Could not load context", "error"); }
    finally { setLoading(false); }
  };
  useEffect(() => { void refresh(); }, []);

  return (
    <div>
      <h3 style={{ margin: "0 0 10px", fontSize: 14, color: "#374151" }}>🧠 Research Context</h3>
      <p style={{ margin: "0 0 12px", fontSize: 13, color: "#6b7280", lineHeight: 1.5 }}>
        This is the live research context Glossa AI sees on every call — sign
        catalogue, benchmark scores, M77 profiles, ledger summaries, etc. Use
        it to verify the AI is grounded in real data.
      </p>
      <button onClick={refresh} disabled={loading} style={btnPurple}>
        {loading ? "Loading…" : "↻ Refresh context"}
      </button>
      {data && (
        <div style={{ marginTop: 12 }}>
          <div style={{ display: "flex", gap: 12, fontSize: 11, color: "#6b7280", marginBottom: 8 }}>
            <span><strong>{data.summary.n_assigned_signs}</strong> assigned signs</span>
            <span>·</span>
            <span><strong>{data.summary.token_coverage_pct.toFixed(1)}%</strong> token coverage</span>
            <span>·</span>
            <span><strong>{data.summary.context_chars.toLocaleString()}</strong> chars in context</span>
          </div>
          <pre style={{ background: "#1e293b", color: "#e2e8f0",
            padding: "12px 14px", borderRadius: 6, fontSize: 11,
            fontFamily: "monospace", margin: 0, overflowX: "auto",
            maxHeight: 420 }}>
            {data.context}
          </pre>
        </div>
      )}
    </div>
  );
}

// ── Main view ───────────────────────────────────────────────────────

export function AIToolsView() {
  const [activeTool, setActiveTool] = useState<Tool>("decipher");
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [studies, setStudies] = useState<StudyResponse[]>([]);

  useEffect(() => {
    listExperiments().then(setExperiments).catch(() => {});
    listStudies().then(setStudies).catch(() => {});
  }, []);

  return (
    <div>
      <h2 style={{ margin: "0 0 0.4rem" }}>✨ AI Hub</h2>
      <p style={{ margin: "0 0 1.25rem", fontSize: 13, color: "#6b7280" }}>
        Every AI capability available to Glossa Lab in one place. Pick a tool below,
        or open the freeform Glossa AI chat for conversational research — it has
        access to live research context, can run experiments via actions, and
        respects your AI Profiles.
      </p>

      {/* Hub overview — capability cards grouped by category */}
      <div style={{ display: "grid", gap: 16, marginBottom: 20 }}>
        {GROUPS.map((g) => (
          <div key={g}>
            <div style={{ fontSize: 11, fontWeight: 700, color: "#7c3aed",
              textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>{g}</div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 8 }}>
              {TOOLS.filter((t) => t.group === g).map((t) => (
                <button key={t.id} onClick={() => setActiveTool(t.id)}
                  style={{ padding: "10px 12px", border: "1px solid",
                    borderColor: activeTool === t.id ? "#7c3aed" : "#e5e7eb",
                    borderRadius: 8, background: activeTool === t.id ? "#f5f3ff" : "#fff",
                    cursor: "pointer", textAlign: "left" }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#111827",
                    display: "flex", alignItems: "center", gap: 6 }}>
                    <span style={{ fontSize: 16 }}>{t.icon}</span>{t.label}
                  </div>
                  <div style={{ fontSize: 11, color: "#6b7280", marginTop: 4 }}>{t.blurb}</div>
                </button>
              ))}
              {g === "Agent Console" && (
                <button
                  onClick={() => {
                    // Ask AppContent to open the left-docked AISidePanel.
                    // openChat() from useAIChat would only flip the floating
                    // AIChatWindow on, not the docked panel the user expects.
                    window.dispatchEvent(new CustomEvent("glossa:open-ai-panel"));
                  }}
                  style={{ padding: "10px 12px", border: "1px solid #c7d2fe",
                    borderRadius: 8, background: "#eef2ff", cursor: "pointer", textAlign: "left" }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#3730a3",
                    display: "flex", alignItems: "center", gap: 6 }}>
                    <span style={{ fontSize: 16 }}>💬</span>Glossa AI chat
                  </div>
                  <div style={{ fontSize: 11, color: "#4338ca", marginTop: 4 }}>
                    Open the docked Glossa AI panel (left side, full context + actions)
                  </div>
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Active tool body */}
      <div style={{ padding: "14px 16px", border: "1px solid #e5e7eb", borderRadius: 8 }}>
        {activeTool === "decipher"     && <DecipherTool />}
        {activeTool === "sign-reading" && <SignReadingTool />}
        {activeTool === "hypotheses"   && <HypothesesTool studies={studies} />}
        {activeTool === "chain"        && <ExperimentChainTool experiments={experiments} />}
        {activeTool === "draft"        && <DraftTool experiments={experiments} />}
        {activeTool === "synthesis"    && <SynthesisTool studies={studies} />}
        {activeTool === "report-synth" && <ReportSynthTool />}
        {activeTool === "context"      && <ContextTool />}
      </div>
    </div>
  );
}

const sl: React.CSSProperties = { fontSize: 10, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 };
const inputStyle: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box", display: "block" };
const btnPurple: React.CSSProperties = { background: "#7c3aed", color: "#fff", border: "none", borderRadius: 4, padding: "7px 16px", fontSize: 12, cursor: "pointer", fontWeight: 600, whiteSpace: "nowrap" };
const btnSecondary: React.CSSProperties = { background: "#fff", color: "#374151", border: "1px solid #d1d5db", borderRadius: 4, padding: "5px 12px", fontSize: 12, cursor: "pointer" };
