/**
 * SweepPanel — the literature sweep, mounted under the Research loop
 * (Spec 081 step 6, the step-3 as-built deferral): the sweep is how
 * new candidate sources reach the loop, so its home is the loop
 * surface, fenced as candidate intake — running a sweep changes no
 * claim. Extracted verbatim from the retired IndusEvidenceView
 * three-tab workspace.
 */
import { useEffect, useState } from "react";
import {
  getIndusSweepCandidates,
  getIndusSweepConfig,
  intakeSweepCandidate,
  runIndusSweep,
  saveIndusSweepConfig,
  type SweepCandidate,
  type SweepConfig,
} from "../api";
import { useToast } from "../hooks/useToast";

function fmtDate(s: string): string {
  if (!s) return "–";
  return s.slice(0, 10);
}

export function SweepPanel({ darkMode = true }: { darkMode?: boolean }) {
  const { toast } = useToast();
  const cardBg = darkMode ? "#1e293b" : "#ffffff";
  const border = darkMode ? "#334155" : "#e5e7eb";
  const fg = darkMode ? "#e2e8f0" : "#111827";
  const muted = darkMode ? "#94a3b8" : "#6b7280";
  const inputBg = darkMode ? "#0f172a" : "#ffffff";
  const inputBdr = darkMode ? "#334155" : "#d1d5db";
  return (
    <div style={{ marginTop: 28 }}>
      <div style={{ fontSize: 15, fontWeight: 700, color: fg, marginBottom: 4 }}>Literature sweep</div>
      <div style={{ fontSize: 12, color: muted, marginBottom: 14, maxWidth: "68ch" }}>
        The sweep searches the configured sources for candidate papers. Importing a
        candidate registers it in the library — it stages a source for the loop to
        read, and changes no claim by itself.
      </div>
      <SweepTab darkMode={darkMode} cardBg={cardBg} border={border} fg={fg} muted={muted}
        inputBg={inputBg} inputBdr={inputBdr} toast={toast} />
    </div>
  );
}

// ── Sweep Tab ──────────────────────────────────────────────────────────────

function SweepTab({ cardBg, border, fg, muted, inputBg, inputBdr, toast }: {
  darkMode?: boolean; cardBg: string; border: string; fg: string; muted: string;
  inputBg: string; inputBdr: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toast: (msg: string, kind?: any) => void;
}) {
  const [config, setConfig] = useState<SweepConfig | null>(null);
  const [configLoading, setConfigLoading] = useState(true);
  const [configSaving, setConfigSaving] = useState(false);
  const [sweepRunning, setSweepRunning] = useState(false);
  const [candidates, setCandidates] = useState<SweepCandidate[]>([]);
  const [candLoading, setCandLoading] = useState(false);
  const [sweepDate, setSweepDate] = useState<string | null>(null);
  const [totalNew, setTotalNew] = useState(0);
  const [intakingIds, setIntakingIds] = useState<Set<string>>(new Set());

  // Editable keyword strings (for inline editing)
  const [primaryKw, setPrimaryKw]     = useState("");
  const [secondaryKw, setSecondaryKw] = useState("");
  const [exclusions, setExclusions]   = useState("");
  const [sweepName, setSweepName]     = useState("");

  useEffect(() => {
    setConfigLoading(true);
    getIndusSweepConfig()
      .then(cfg => {
        setConfig(cfg);
        setSweepName(cfg.sweep.name || "");
        setPrimaryKw((cfg.sweep.keywords.primary || []).join(", "));
        setSecondaryKw((cfg.sweep.keywords.secondary || []).join(", "));
        setExclusions((cfg.sweep.exclusions || []).join(", "));
      })
      .catch(() => {})
      .finally(() => setConfigLoading(false));

    loadCandidates();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadCandidates = async () => {
    setCandLoading(true);
    try {
      const r = await getIndusSweepCandidates();
      setCandidates(r.candidates || []);
      setSweepDate(r.sweep_date || null);
      setTotalNew(r.total_new || 0);
    } catch { /* no candidates yet */ }
    finally { setCandLoading(false); }
  };

  const handleSaveConfig = async () => {
    if (!config) return;
    setConfigSaving(true);
    try {
      const updated: SweepConfig = {
        ...config,
        sweep: {
          ...config.sweep,
          name: sweepName,
          keywords: {
            ...config.sweep.keywords,
            primary:   primaryKw.split(",").map(s => s.trim()).filter(Boolean),
            secondary: secondaryKw.split(",").map(s => s.trim()).filter(Boolean),
          },
          exclusions: exclusions.split(",").map(s => s.trim()).filter(Boolean),
        },
      };
      await saveIndusSweepConfig(updated);
      setConfig(updated);
      toast("Sweep config saved", "success");
    } catch (e) { toast(String(e), "error"); }
    finally { setConfigSaving(false); }
  };

  const handleRunSweep = async () => {
    setSweepRunning(true);
    try {
      const r = await runIndusSweep();
      toast(r.message, "info");
      // Poll for candidates after a delay
      setTimeout(() => void loadCandidates(), 8000);
      setTimeout(() => void loadCandidates(), 20000);
    } catch (e) { toast(String(e), "error"); }
    finally { setSweepRunning(false); }
  };

  const handleIntake = async (cand: SweepCandidate) => {
    const key = cand.url || cand.title;
    setIntakingIds(prev => new Set(prev).add(key));
    try {
      const r = await intakeSweepCandidate({
        url: cand.url,
        pdf_url: cand.pdf_url || undefined,
        title: cand.title,
        doi: cand.doi || undefined,
        authors: cand.authors,
        source: cand.source,
      });
      toast(r.message, "success");
    } catch (e) { toast(String(e), "error"); }
    finally { setIntakingIds(prev => { const n = new Set(prev); n.delete(key); return n; }); }
  };

  const inpStyle: React.CSSProperties = {
    padding: "7px 10px", border: `1px solid ${inputBdr}`, borderRadius: 6,
    fontSize: 12, background: inputBg, color: fg, outline: "none",
    width: "100%", boxSizing: "border-box",
  };
  const textareaStyle: React.CSSProperties = {
    ...inpStyle, resize: "vertical" as const, fontFamily: "inherit",
    minHeight: 60, lineHeight: 1.5,
  };

  if (configLoading) return <div style={{ color: muted, fontSize: 12 }}>Loading sweep config…</div>;

  // Source toggles from config
  const sources = config?.sweep.sources ?? {};
  const enabledSources = Object.entries(sources).filter(([, v]) => v?.enabled).map(([k]) => k);
  const disabledSources = Object.entries(sources).filter(([, v]) => !v?.enabled).map(([k]) => k);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      {/* Config editor */}
      <div style={{ background: cardBg, border: `1px solid ${border}`, borderRadius: 10, padding: "16px 20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: fg }}>⚙️ Sweep Configuration</div>
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => void handleSaveConfig()} disabled={configSaving}
              style={{ padding: "6px 14px", border: "none", borderRadius: 6, background: "#7c3aed",
                color: "#fff", cursor: "pointer", fontSize: 12, fontWeight: 600,
                opacity: configSaving ? 0.5 : 1 }}>
              {configSaving ? "Saving…" : "💾 Save Config"}
            </button>
            <button onClick={() => void handleRunSweep()} disabled={sweepRunning}
              style={{ padding: "6px 14px", border: "none", borderRadius: 6, background: "#059669",
                color: "#fff", cursor: "pointer", fontSize: 12, fontWeight: 600,
                opacity: sweepRunning ? 0.5 : 1 }}>
              {sweepRunning ? "⏳ Running…" : "▶ Run Sweep"}
            </button>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          <div>
            <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
              Sweep Name
            </label>
            <input value={sweepName} onChange={e => setSweepName(e.target.value)} style={inpStyle} />
          </div>
          <div>
            <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
              Enabled Sources
            </label>
            <div style={{ fontSize: 11, color: fg, padding: "7px 10px", border: `1px solid ${inputBdr}`,
              borderRadius: 6, background: inputBg, lineHeight: 1.6 }}>
              {enabledSources.join(", ") || "none"}
            </div>
          </div>
        </div>

        <div style={{ marginTop: 14 }}>
          <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
            Primary Keywords <span style={{ fontWeight: 400 }}>(comma-separated)</span>
          </label>
          <textarea value={primaryKw} onChange={e => setPrimaryKw(e.target.value)} style={textareaStyle} />
        </div>

        <div style={{ marginTop: 14 }}>
          <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
            Secondary Keywords <span style={{ fontWeight: 400 }}>(comma-separated)</span>
          </label>
          <textarea value={secondaryKw} onChange={e => setSecondaryKw(e.target.value)} style={textareaStyle} />
        </div>

        <div style={{ marginTop: 14 }}>
          <label style={{ fontSize: 11, fontWeight: 600, color: muted, display: "block", marginBottom: 4 }}>
            Exclusions <span style={{ fontWeight: 400 }}>(comma-separated, exact phrase match)</span>
          </label>
          <input value={exclusions} onChange={e => setExclusions(e.target.value)} style={inpStyle} />
        </div>

        {disabledSources.length > 0 && (
          <div style={{ marginTop: 12, fontSize: 10, color: muted }}>
            Disabled sources (edit sweep.yaml to enable): {disabledSources.join(", ")}
          </div>
        )}
      </div>

      {/* Candidates */}
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: fg }}>
            🔍 Sweep Candidates
            {sweepDate && <span style={{ fontSize: 10, color: muted, marginLeft: 8 }}>Last sweep: {fmtDate(sweepDate)}</span>}
          </div>
          {totalNew > 0 && (
            <span style={{ fontSize: 11, padding: "3px 10px", borderRadius: 8,
              background: "#7c3aed18", color: "#7c3aed", fontWeight: 700 }}>
              {totalNew} new candidates
            </span>
          )}
          <button onClick={() => void loadCandidates()} disabled={candLoading}
            style={{ padding: "5px 12px", border: `1px solid ${border}`, borderRadius: 6,
              background: "none", color: muted, cursor: "pointer", fontSize: 11 }}>
            {candLoading ? "…" : "↻ Refresh"}
          </button>
        </div>

        {candidates.length === 0 && !candLoading && (
          <div style={{ color: muted, fontSize: 12, fontStyle: "italic" }}>
            No candidates yet. Click "Run Sweep" to search for new papers.
          </div>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {candidates.map((cand, i) => {
            const key = cand.url || cand.title || String(i);
            const busy = intakingIds.has(key);
            return (
              <div key={i} style={{ background: cardBg, border: `1px solid ${border}`,
                borderRadius: 8, padding: "10px 14px", display: "flex", gap: 12, alignItems: "flex-start" }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <a href={cand.url} target="_blank" rel="noopener noreferrer"
                    style={{ fontSize: 12, fontWeight: 600, color: "#7c3aed", textDecoration: "none",
                      display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                    {cand.title || "(untitled)"}
                  </a>
                  <div style={{ fontSize: 10, color: muted, marginTop: 3, display: "flex", gap: 8, flexWrap: "wrap" }}>
                    <span>{cand.source}</span>
                    {cand.authors.length > 0 && <span>{cand.authors.slice(0, 2).join(", ")}</span>}
                    {cand.published_at && <span>{cand.published_at.slice(0, 7)}</span>}
                    {cand.open_access && <span style={{ color: "#16a34a" }}>OA PDF</span>}
                  </div>
                  {cand.summary && (
                    <div style={{ fontSize: 10, color: muted, marginTop: 3, lineHeight: 1.4,
                      display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                      {cand.summary}
                    </div>
                  )}
                </div>
                <button onClick={() => void handleIntake(cand)} disabled={busy}
                  title="Import this paper to the evidence library"
                  style={{ padding: "5px 12px", border: "none", borderRadius: 6, background: "#7c3aed",
                    color: "#fff", cursor: "pointer", fontSize: 11, fontWeight: 600,
                    opacity: busy ? 0.5 : 1, flexShrink: 0, whiteSpace: "nowrap" as const }}>
                  {busy ? "…" : "→ Import"}
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
