/**
 * ResearchLoopPanel — dashboard tile for the Integrated Research Loop.
 *
 * Shows last run results + Start/Stop controls. When running, displays
 * real-time cycle-by-cycle progress via SSE from the backend. After
 * completion (and on initial load) shows a full RunSummary with insight
 * breakdown, foundation check status, and proposals.
 *
 * API:
 *   POST /api/v1/research-loop/start?max_cycles=N  → SSE stream
 *   GET  /api/v1/research-loop/status               → current state
 *   POST /api/v1/research-loop/stop                 → graceful stop
 *   GET  /api/v1/research-loop/last-run             → last synthesis + results
 */

import { useCallback, useEffect, useState } from "react";

const BASE = "/api/v1/research-loop";

// Insight type colour map
const INSIGHT_COLORS: Record<string, { bg: string; text: string }> = {
  reading:   { bg: "#ede9fe", text: "#5b21b6" },
  formula:   { bg: "#dbeafe", text: "#1d4ed8" },
  guild:     { bg: "#dcfce7", text: "#15803d" },
  function:  { bg: "#fef9c3", text: "#854d0e" },
  morphology:{ bg: "#fce7f3", text: "#9d174d" },
  compound:  { bg: "#ffedd5", text: "#9a3412" },
};

interface CycleEntry {
  cycle: number;
  gap_targeted: string;
  experiment: string;
  n_papers: number;
  n_insights: number;
  insight_types: Record<string, number>;
  verdict: string;
  is_new_info: boolean;
  selection_method: string;
}

interface FoundationCheck {
  n_ok: number;
  n_fail: number;
  n_warn: number;
  verdict: string;
  failed: string[];
  skipped?: boolean;
  reason?: string;
}

interface Proposal {
  action: string;
  experiment: string;
  rationale: string;
}

interface Synthesis {
  summary: string;
  insight_type_totals: Record<string, number>;
  unexplored_types: string[];
  proposals: Proposal[];
  foundation_check: FoundationCheck;
}

interface LastRun {
  job_id?: string;
  completed_at?: string;
  total_papers_mined?: number;
  total_insights?: number;
  cycles_run?: number;
  synthesis?: Synthesis;
  no_runs?: boolean;
}

interface LoopStatus {
  running: boolean;
  cycles_completed: number;
  max_cycles: number;
  total_papers: number;
  total_insights: number;
  history: CycleEntry[];
}

export function ResearchLoopPanel() {
  const [, setStatus] = useState<LoopStatus | null>(null);
  const [running, setRunning] = useState(false);
  const [cycles, setCycles] = useState(15);
  const [log, setLog] = useState<CycleEntry[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [lastRun, setLastRun] = useState<LastRun | null>(null);
  const [synthesis, setSynthesis] = useState<Synthesis | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/status`);
      if (res.ok) setStatus(await res.json() as LoopStatus);
    } catch { /* backend may not be running */ }
  }, []);

  const fetchLastRun = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/last-run`);
      if (res.ok) {
        const data = await res.json() as LastRun;
        setLastRun(data);
        if (data.synthesis) setSynthesis(data.synthesis);
      }
    } catch { /* ignore */ }
  }, []);

  useEffect(() => {
    void fetchStatus();
    void fetchLastRun();
  }, [fetchStatus, fetchLastRun]);

  const startLoop = async () => {
    setRunning(true);
    setError(null);
    setLog([]);
    setSynthesis(null);

    try {
      const res = await fetch(`${BASE}/start?max_cycles=${cycles}`, { method: "POST" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        let buffer = "";
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() ?? "";
          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            try {
              const event = JSON.parse(line.slice(6)) as CycleEntry & {
                type?: string; synthesis?: Synthesis;
              };
              if (event.type === "complete") {
                if (event.synthesis) setSynthesis(event.synthesis);
                void fetchStatus();
                void fetchLastRun();
              } else if (event.cycle) {
                setLog((prev) => [...prev, event as CycleEntry]);
              }
            } catch { /* ignore parse errors */ }
          }
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to start loop");
    } finally {
      setRunning(false);
      void fetchStatus();
    }
  };

  const stopLoop = async () => {
    try { await fetch(`${BASE}/stop`, { method: "POST" }); } catch { /* ignore */ }
  };

  const activeSynthesis = synthesis;
  const totalPapers = log.reduce((s, c) => s + c.n_papers, 0);
  const totalInsights = log.reduce((s, c) => s + c.n_insights, 0);

  return (
    <div style={{ border: "1px solid #c4b5fd", borderRadius: 10, padding: 16,
                  background: "#faf5ff", marginBottom: 16 }}>

      {/* ── Header ── */}
      <div style={{ display: "flex", justifyContent: "space-between",
                    alignItems: "center", marginBottom: 12 }}>
        <div>
          <span style={{ fontSize: 16, fontWeight: 700, color: "#5b21b6" }}>
            🔄 Integrated Research Loop
          </span>
          <span style={{ marginLeft: 8, padding: "2px 8px", borderRadius: 4,
                         fontSize: 11, fontWeight: 600,
                         background: running ? "#dcfce7" : "#f3f4f6",
                         color: running ? "#15803d" : "#6b7280" }}>
            {running ? "⏳ Running…" : "Ready"}
          </span>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <select value={cycles}
            onChange={(e) => setCycles(parseInt(e.target.value, 10))}
            disabled={running}
            style={{ padding: "4px 8px", border: "1px solid #d1d5db",
                     borderRadius: 5, fontSize: 12, background: "#fff" }}>
            {[5, 10, 15, 20, 30].map((n) => (
              <option key={n} value={n}>{n} cycles</option>
            ))}
          </select>
          {!running ? (
            <button onClick={() => void startLoop()}
              style={{ padding: "6px 14px", border: "1px solid #7c3aed",
                       borderRadius: 6, background: "#7c3aed", color: "#fff",
                       fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
              ▶ Start Loop
            </button>
          ) : (
            <button onClick={() => void stopLoop()}
              style={{ padding: "6px 14px", border: "1px solid #dc2626",
                       borderRadius: 6, background: "#dc2626", color: "#fff",
                       fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
              ■ Stop
            </button>
          )}
        </div>
      </div>

      {/* ── Protocol description ── */}
      <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 10 }}>
        Mine → Analyze → Register → Execute → Analyze · {cycles} cycles ·
        15 gap topics × 15 experiment templates
      </div>

      {/* ── Live progress: metrics + cycle log (only while/after running) ── */}
      {log.length > 0 && (
        <>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr",
                        gap: 8, marginBottom: 12 }}>
            <MetricTile label="Cycles" value={log.length} />
            <MetricTile label="Papers" value={totalPapers} />
            <MetricTile label="Insights" value={totalInsights} />
            <MetricTile label="New results"
              value={log.filter((c) => c.is_new_info).length} />
          </div>
          <div style={{ maxHeight: 200, overflowY: "auto",
                        border: "1px solid #e5e7eb", borderRadius: 6,
                        background: "#fff", marginBottom: 12 }}>
            {log.map((entry) => (
              <div key={`${entry.cycle}-${entry.gap_targeted}`}
                style={{ display: "flex", alignItems: "center", gap: 8,
                         padding: "5px 10px", borderBottom: "1px solid #f3f4f6",
                         fontSize: 11 }}>
                <span style={{ width: 24, fontWeight: 700, color: "#7c3aed" }}>
                  C{entry.cycle}
                </span>
                <span style={{ width: 130, color: "#374151", overflow: "hidden",
                               textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {entry.gap_targeted}
                </span>
                <span style={{ color: "#6b7280" }}>→</span>
                <span style={{ width: 150, color: "#1d4ed8", overflow: "hidden",
                               textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {entry.experiment}
                </span>
                <span style={{ flex: 1, color: "#374151", overflow: "hidden",
                               textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {entry.verdict.slice(0, 55)}
                </span>
                <InsightTypePills types={entry.insight_types} max={2} />
                <span style={{ fontSize: 10, padding: "1px 5px", borderRadius: 3,
                               background: entry.is_new_info ? "#dcfce7" : "#f3f4f6",
                               color: entry.is_new_info ? "#15803d" : "#9ca3af",
                               fontWeight: 600, flexShrink: 0 }}>
                  {entry.is_new_info ? "NEW" : "rpt"}
                </span>
              </div>
            ))}
          </div>
        </>
      )}

      {/* ── Run Summary Dashboard ── */}
      {!running && activeSynthesis && (
        <RunSummary synthesis={activeSynthesis} completedAt={lastRun?.completed_at}
          totalPapers={lastRun?.total_papers_mined ?? 0}
          totalInsights={lastRun?.total_insights ?? 0} />
      )}

      {/* ── Fallback: no run yet ── */}
      {!running && !log.length && !activeSynthesis && lastRun?.no_runs && (
        <div style={{ fontSize: 12, color: "#9ca3af", textAlign: "center",
                      padding: "16px 0" }}>
          No runs yet. Start the loop to begin mining.
        </div>
      )}

      {error && (
        <div style={{ marginTop: 8, fontSize: 12, color: "#dc2626",
                      background: "#fef2f2", border: "1px solid #fca5a5",
                      borderRadius: 6, padding: "6px 10px" }}>
          {error}
        </div>
      )}
    </div>
  );
}

// ── Run Summary ──────────────────────────────────────────────────────────────

function RunSummary({
  synthesis, completedAt, totalPapers, totalInsights,
}: {
  synthesis: Synthesis;
  completedAt?: string;
  totalPapers: number;
  totalInsights: number;
}) {
  const fc = synthesis.foundation_check;
  const insightTotals = synthesis.insight_type_totals;
  const totalInsightCount = Object.values(insightTotals).reduce((a, b) => a + b, 0);
  const maxInsight = Math.max(...Object.values(insightTotals), 1);

  const timeLabel = completedAt
    ? new Date(completedAt).toLocaleString(undefined,
        { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })
    : null;

  return (
    <div style={{ borderTop: "1px solid #e9d5ff", paddingTop: 12 }}>

      {/* Header row */}
      <div style={{ display: "flex", alignItems: "center", gap: 8,
                    marginBottom: 10 }}>
        <span style={{ fontSize: 13, fontWeight: 700, color: "#5b21b6" }}>
          📊 Last Run Summary
        </span>
        {timeLabel && (
          <span style={{ fontSize: 11, color: "#9ca3af" }}>{timeLabel}</span>
        )}
        <div style={{ marginLeft: "auto" }}>
          <FoundationBadge fc={fc} />
        </div>
      </div>

      {/* Stats row */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr",
                    gap: 8, marginBottom: 12 }}>
        <MetricTile label="Papers mined" value={totalPapers} />
        <MetricTile label="Insights" value={totalInsights} />
        <MetricTile label="Total insights" value={totalInsightCount} />
      </div>

      {/* Insight type breakdown */}
      {Object.keys(insightTotals).length > 0 && (
        <div style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: "#374151",
                        marginBottom: 6 }}>Insight breakdown</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            {Object.entries(insightTotals)
              .sort(([, a], [, b]) => b - a)
              .map(([type, count]) => {
                const colors = INSIGHT_COLORS[type] ?? { bg: "#f3f4f6", text: "#374151" };
                const pct = Math.round((count / maxInsight) * 100);
                return (
                  <div key={type} style={{ display: "flex", alignItems: "center",
                                          gap: 6 }}>
                    <span style={{ width: 72, fontSize: 11, fontWeight: 600,
                                   color: colors.text,
                                   background: colors.bg,
                                   padding: "1px 6px", borderRadius: 3,
                                   textAlign: "right" }}>
                      {type}
                    </span>
                    <div style={{ flex: 1, height: 8, background: "#f3f4f6",
                                  borderRadius: 4, overflow: "hidden" }}>
                      <div style={{ width: `${pct}%`, height: "100%",
                                    background: colors.text,
                                    borderRadius: 4, opacity: 0.7 }} />
                    </div>
                    <span style={{ fontSize: 11, color: "#6b7280",
                                   width: 28, textAlign: "right" }}>
                      {count}
                    </span>
                  </div>
                );
              })}
          </div>
        </div>
      )}

      {/* Foundation check detail (only if failures or warnings) */}
      {!fc.skipped && fc.n_fail > 0 && (
        <div style={{ background: "#fef2f2", border: "1px solid #fca5a5",
                      borderRadius: 6, padding: "8px 10px", marginBottom: 10 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#dc2626",
                        marginBottom: 4 }}>
            ⚠ Foundation check failures ({fc.n_fail})
          </div>
          {fc.failed.slice(0, 5).map((f, i) => (
            <div key={i} style={{ fontSize: 11, color: "#7f1d1d",
                                   fontFamily: "monospace" }}>
              {f.replace("[FAIL] ", "")}
            </div>
          ))}
        </div>
      )}

      {/* Proposals */}
      {synthesis.proposals.length > 0 && (
        <div>
          <div style={{ fontSize: 11, fontWeight: 600, color: "#374151",
                        marginBottom: 6 }}>Next steps</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            {synthesis.proposals.slice(0, 4).map((p, i) => (
              <div key={i} style={{ display: "flex", gap: 8, alignItems: "flex-start",
                                    padding: "5px 8px", borderRadius: 5,
                                    background: p.action === "fix_foundation"
                                      ? "#fef2f2" : "#f5f3ff",
                                    border: `1px solid ${
                                      p.action === "fix_foundation"
                                        ? "#fca5a5" : "#e9d5ff"}` }}>
                <span style={{ fontSize: 13, flexShrink: 0 }}>
                  {p.action === "fix_foundation" ? "🔴"
                    : p.action === "run_experiment" ? "🔬"
                    : p.action === "refresh_insights" ? "✨" : "▸"}
                </span>
                <div style={{ fontSize: 11, color: "#374151" }}>{p.rationale}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Unexplored types */}
      {synthesis.unexplored_types.length > 0 && (
        <div style={{ marginTop: 8, fontSize: 11, color: "#9ca3af" }}>
          Unexplored this run:{" "}
          {synthesis.unexplored_types.map((t) => (
            <span key={t} style={{
              marginRight: 4,
              padding: "1px 5px",
              borderRadius: 3,
              background: "#f3f4f6",
              color: "#6b7280",
            }}>{t}</span>
          ))}
        </div>
      )}
    </div>
  );
}

// ── Sub-components ───────────────────────────────────────────────────────────

function FoundationBadge({ fc }: { fc: FoundationCheck }) {
  if (fc.skipped) {
    return (
      <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 4,
                     background: "#f3f4f6", color: "#6b7280", fontWeight: 600 }}>
        Foundation ―
      </span>
    );
  }
  const ok = fc.n_fail === 0;
  return (
    <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 4, fontWeight: 600,
                   background: ok ? "#dcfce7" : "#fef2f2",
                   color: ok ? "#15803d" : "#dc2626" }}>
      Foundation {ok ? `✓ ${fc.n_ok} ok` : `✗ ${fc.n_fail} fail`}
      {fc.n_warn > 0 && ` · ${fc.n_warn}⚠`}
    </span>
  );
}

function InsightTypePills({
  types, max,
}: { types: Record<string, number>; max: number }) {
  const entries = Object.entries(types).sort(([, a], [, b]) => b - a).slice(0, max);
  return (
    <div style={{ display: "flex", gap: 2, flexShrink: 0 }}>
      {entries.map(([t, c]) => {
        const col = INSIGHT_COLORS[t] ?? { bg: "#f3f4f6", text: "#6b7280" };
        return (
          <span key={t} style={{ fontSize: 9, padding: "1px 4px", borderRadius: 2,
                                  background: col.bg, color: col.text,
                                  fontWeight: 600 }}>
            {t.slice(0, 3)}:{c}
          </span>
        );
      })}
    </div>
  );
}

function MetricTile({ label, value }: { label: string; value: number }) {
  return (
    <div style={{ padding: "8px 10px", background: "#fff",
                  border: "1px solid #e5e7eb", borderRadius: 6,
                  textAlign: "center" }}>
      <div style={{ fontSize: 18, fontWeight: 800, color: "#5b21b6" }}>
        {value.toLocaleString()}
      </div>
      <div style={{ fontSize: 10, color: "#6b7280" }}>{label}</div>
    </div>
  );
}
