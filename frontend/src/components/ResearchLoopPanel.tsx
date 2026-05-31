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

interface AnchorCandidate {
  sign: string;
  proposed_reading: string;
  evidence_type: string;
  evidence_score: number;
  dedr_support?: string;
  source_experiment: string;
  conflict?: string;
  review_status: "staged" | "blocked" | "approved" | "rejected";
  neighbor_reading?: string;
  neighbor_count?: number;
  corpus_freq?: number;
  animal_freq?: number;
  partner_reading?: string;
}

interface Synthesis {
  summary: string;
  needle_moved?: boolean;
  insight_type_totals: Record<string, number>;
  unexplored_types: string[];
  path_signals?: Record<string, number>;
  proposals: Proposal[];
  foundation_check: FoundationCheck;
  anchor_candidates?: AnchorCandidate[];
  candidate_counts?: { total: number; staged: number; blocked: number };
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

interface StagingData {
  candidates: AnchorCandidate[];
  counts: { total: number; staged: number; approved: number; rejected: number };
  error?: string;
}

export function ResearchLoopPanel() {
  const [, setStatus] = useState<LoopStatus | null>(null);
  const [running, setRunning] = useState(false);
  const [cycles, setCycles] = useState(15);
  const [log, setLog] = useState<CycleEntry[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [lastRun, setLastRun] = useState<LastRun | null>(null);
  const [synthesis, setSynthesis] = useState<Synthesis | null>(null);
  const [staging, setStaging] = useState<StagingData | null>(null);
  const [showReview, setShowReview] = useState(false);
  // Track which proposal button was last clicked so it can show Done/Retry
  const [proposalKey, setProposalKey] = useState<string | null>(null);

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

  const fetchStaging = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/staging`);
      if (res.ok) setStaging(await res.json() as StagingData);
    } catch { /* ignore */ }
  }, []);

  useEffect(() => {
    void fetchStatus();
    void fetchLastRun();
    void fetchStaging();
  }, [fetchStatus, fetchLastRun, fetchStaging]);

  const startLoop = async (fromProposal?: string) => {
    if (fromProposal) {
      setProposalKey(fromProposal);
    } else {
      setProposalKey(null); // main button clears proposal tracking
    }
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
                // Notify DashboardView so it can pull the new insight
                window.dispatchEvent(new CustomEvent("glossa:loop-complete"));
                void fetchStatus();
                void fetchLastRun();
                void fetchStaging();
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
          totalInsights={lastRun?.total_insights ?? 0}
          loopRunning={running}
          loopError={error}
          proposalKey={proposalKey}
          onStartLoop={(key) => void startLoop(key)} />
      )}

      {/* ── Staging review queue ── */}
      {(staging?.counts?.staged ?? 0) > 0 && staging?.counts && (
        <div style={{ marginTop: 8 }}>
          <button
            onClick={() => setShowReview((v) => !v)}
            style={{
              width: "100%", padding: "7px 12px",
              border: "1px solid #f59e0b", borderRadius: 6,
              background: showReview ? "#fef3c7" : "#fffbeb",
              color: "#92400e", fontSize: 12, fontWeight: 700,
              cursor: "pointer", textAlign: "left",
              display: "flex", justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span>
              📎 {staging.counts.staged} candidate{staging.counts.staged !== 1 ? "s" : ""} awaiting review
              {staging.counts.approved > 0 && (
                <span style={{ marginLeft: 8, color: "#15803d" }}>
                  ✓ {staging.counts.approved} approved
                </span>
              )}
            </span>
            <span style={{ fontSize: 11, fontWeight: 400 }}>
              {showReview ? "Hide ▲" : "Review ▼"}
            </span>
          </button>
          {showReview && staging && (
            <StagingReview
              staging={staging}
              onAction={async (sign, reading, action, reason) => {
                const res = await fetch(`${BASE}/staging/action`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ sign, proposed_reading: reading, action, reason }),
                });
                if (res.ok) void fetchStaging();
              }}
            />
          )}
        </div>
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
  loopRunning, loopError, proposalKey, onStartLoop,
}: {
  synthesis: Synthesis;
  completedAt?: string;
  totalPapers: number;
  totalInsights: number;
  loopRunning?: boolean;
  loopError?: string | null;
  proposalKey?: string | null;
  onStartLoop?: (key: string) => void;
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
        {synthesis.needle_moved !== undefined && (
          <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 4,
                         fontWeight: 700,
                         background: synthesis.needle_moved ? "#dcfce7" : "#fef9c3",
                         color: synthesis.needle_moved ? "#15803d" : "#854d0e" }}>
            {synthesis.needle_moved ? "⬆ needle moved" : "→ no movement"}
          </span>
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
            {synthesis.proposals.slice(0, 4).map((p, i) => {
              const isFixFoundation = p.action === "fix_foundation";
              const isExpandMining = p.action === "expand_mining";
              const isReviewCandidates = p.action === "review_candidates";
              return (
                <div key={i} style={{ display: "flex", gap: 8, alignItems: "flex-start",
                                      padding: "5px 8px", borderRadius: 5,
                                      background: isFixFoundation ? "#fef2f2" : "#f5f3ff",
                                      border: `1px solid ${
                                        isFixFoundation ? "#fca5a5" : "#e9d5ff"}` }}>
                  <span style={{ fontSize: 13, flexShrink: 0 }}>
                    {isFixFoundation ? "🔴"
                      : p.action === "run_experiment" ? "🔬"
                      : isExpandMining ? "🔁"
                      : isReviewCandidates ? "📎"
                      : "▸"}
                  </span>
                  <div style={{ flex: 1, fontSize: 11, color: "#374151" }}>
                    {p.rationale}
                  </div>
                  {/* Action button for expand_mining — tracks running/done/error */}
                  {isExpandMining && onStartLoop && (() => {
                    const isTracked = proposalKey === "expand_mining";
                    const btnState = isTracked
                      ? (loopRunning ? "running" : loopError ? "error" : "done")
                      : "idle";
                    if (btnState === "done") {
                      return (
                        <span style={{
                          fontSize: 10, padding: "2px 7px", borderRadius: 4,
                          background: "#dcfce7", color: "#15803d",
                          fontWeight: 700, flexShrink: 0,
                        }}>✓ Done</span>
                      );
                    }
                    return (
                      <button
                        disabled={btnState === "running"}
                        onClick={() => onStartLoop("expand_mining")}
                        style={{
                          padding: "2px 8px", fontSize: 10, fontWeight: 700,
                          borderRadius: 4, whiteSpace: "nowrap", flexShrink: 0,
                          cursor: btnState === "running" ? "default" : "pointer",
                          border: btnState === "error" ? "1px solid #dc2626" : "1px solid #7c3aed",
                          background: btnState === "running" ? "#f3f4f6"
                            : btnState === "error" ? "#fef2f2" : "#7c3aed",
                          color: btnState === "running" ? "#9ca3af"
                            : btnState === "error" ? "#dc2626" : "#fff",
                        }}
                      >
                        {btnState === "running" ? "⏳…"
                          : btnState === "error" ? "✕ Retry"
                          : "▶ Start Loop"}
                      </button>
                    );
                  })()}
                  {/* Action button for review_candidates — scroll to review queue */}
                  {isReviewCandidates && (
                    <span style={{
                      fontSize: 10, padding: "2px 6px", borderRadius: 3,
                      background: "#fef3c7", color: "#92400e",
                      fontWeight: 600, flexShrink: 0,
                    }}>
                      ↓ see below
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Anchor candidates table */}
      <CandidatesTable candidates={synthesis.anchor_candidates}
        counts={synthesis.candidate_counts} />

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

// ── Anchor candidates table ───────────────────────────────────────────────────

function CandidatesTable({
  candidates, counts,
}: {
  candidates?: AnchorCandidate[];
  counts?: { total: number; staged: number; blocked: number };
}) {
  const staged = (candidates || []).filter((c) => c.review_status === "staged");
  const blocked = (candidates || []).filter((c) => c.review_status === "blocked");

  return (
    <div style={{ marginTop: 12, marginBottom: 8 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 6,
                    marginBottom: 6 }}>
        <span style={{ fontSize: 11, fontWeight: 600, color: "#374151" }}>
          Anchor candidates
        </span>
        {counts && (
          <span style={{ fontSize: 11, color: "#6b7280" }}>
            {counts.staged} staged · {counts.blocked} blocked
          </span>
        )}
      </div>

      {staged.length === 0 && blocked.length === 0 ? (
        <div style={{ fontSize: 11, color: "#9ca3af",
                      background: "#f9fafb", borderRadius: 5,
                      padding: "6px 10px", border: "1px solid #e5e7eb" }}>
          No candidates staged this run. Loop ran experiments but produced no
          promotable anchor signals. Try running with
          <code style={{ fontSize: 10, background: "#f3f4f6",
                          padding: "0 3px", borderRadius: 2 }}>
            blocker_sign_context
          </code>
          {" "}or increasing cycle count.
        </div>
      ) : (
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 6,
                      overflow: "hidden" }}>
          {/* Staged */}
          {staged.map((c, i) => (
            <div key={i} style={{
              display: "grid",
              gridTemplateColumns: "60px 80px 1fr 80px 60px",
              gap: 6, alignItems: "center",
              padding: "5px 10px",
              borderBottom: "1px solid #f3f4f6",
              background: "#f0fdf4",
              fontSize: 11,
            }}>
              <span style={{ fontWeight: 700, color: "#374151",
                              fontFamily: "monospace" }}>
                {c.sign}
              </span>
              <span style={{ fontWeight: 600, color: "#5b21b6" }}>
                {c.proposed_reading}
              </span>
              <span style={{ color: "#6b7280", overflow: "hidden",
                              textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {c.dedr_support
                  ? `DEDR: ${c.dedr_support.slice(0, 40)}`
                  : c.evidence_type.replace(/_/g, " ")}
              </span>
              <span style={{ fontSize: 10, color: "#6b7280",
                              overflow: "hidden", textOverflow: "ellipsis",
                              whiteSpace: "nowrap" }}>
                {c.evidence_type.replace(/_/g, "\u200b").slice(0, 18)}
              </span>
              <span style={{ fontSize: 10, padding: "1px 5px", borderRadius: 3,
                              background: "#dcfce7", color: "#15803d",
                              fontWeight: 600, textAlign: "center" }}>
                staged
              </span>
            </div>
          ))}
          {/* Blocked (collapsed) */}
          {blocked.length > 0 && (
            <div style={{ padding: "4px 10px", background: "#fafafa",
                          fontSize: 10, color: "#9ca3af" }}>
              +{blocked.length} blocked (conflict with existing HIGH readings)
            </div>
          )}
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

// ── Staging Review Queue ───────────────────────────────────────────────────

function StagingReview({
  staging,
  onAction,
}: {
  staging: StagingData;
  onAction: (sign: string, reading: string,
             action: "approve" | "reject" | "delete",
             reason?: string) => Promise<void>;
}) {
  const [confirming, setConfirming] = useState<{
    sign: string; reading: string; action: "approve" | "reject" | "delete";
  } | null>(null);
  const [rejectReason, setRejectReason] = useState("");
  const [busy, setBusy] = useState(false);

  const stagedCandidates = staging.candidates.filter(
    (c) => c.review_status === "staged");
  const approvedCandidates = staging.candidates.filter(
    (c) => c.review_status === "approved");

  const doAction = async (
    sign: string, reading: string,
    action: "approve" | "reject" | "delete",
    reason?: string,
  ) => {
    setBusy(true);
    try {
      await onAction(sign, reading, action, reason);
    } finally {
      setBusy(false);
      setConfirming(null);
      setRejectReason("");
    }
  };

  return (
    <div style={{ border: "1px solid #fed7aa", borderRadius: 6,
                  background: "#fff", marginTop: 6, overflow: "hidden" }}>

      {/* Column header */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "60px 72px 1fr 100px 90px 100px",
        gap: 6, padding: "5px 10px",
        background: "#fef3c7", fontSize: 10,
        fontWeight: 700, color: "#78350f",
        borderBottom: "1px solid #fed7aa",
      }}>
        <span>Sign</span>
        <span>Reading</span>
        <span>Evidence</span>
        <span>Type</span>
        <span>Score</span>
        <span>Actions</span>
      </div>

      {/* Staged candidates */}
      {stagedCandidates.length === 0 ? (
        <div style={{ padding: "10px", fontSize: 11, color: "#9ca3af",
                      textAlign: "center" }}>
          All candidates have been reviewed.
        </div>
      ) : (
        stagedCandidates.map((c, i) => (
          <div key={i}>
            <div style={{
              display: "grid",
              gridTemplateColumns: "60px 72px 1fr 100px 90px 100px",
              gap: 6, padding: "7px 10px",
              borderBottom: "1px solid #f3f4f6",
              fontSize: 11, alignItems: "center",
              background: confirming?.sign === c.sign &&
                          confirming?.reading === c.proposed_reading
                ? "#fef9c3" : "#fff",
            }}>
              <span style={{ fontWeight: 700, fontFamily: "monospace",
                              color: "#374151" }}>
                {c.sign}
              </span>
              <span style={{ fontWeight: 600, color: "#5b21b6" }}>
                {c.proposed_reading}
              </span>
              <span style={{ color: "#6b7280", overflow: "hidden",
                              textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {c.dedr_support
                  ? <>◆ DEDR: <em>{c.dedr_support.slice(0, 35)}</em></>
                  : c.evidence_type.replace(/_/g, " ")}
              </span>
              <span style={{ fontSize: 10, color: "#6b7280",
                              overflow: "hidden", textOverflow: "ellipsis",
                              whiteSpace: "nowrap" }}>
                {c.evidence_type.replace(/_/g, " ").slice(0, 20)}
              </span>
              <span style={{ fontSize: 11, fontWeight: 600,
                              color: c.evidence_score >= 0.5 ? "#15803d" : "#6b7280" }}>
                {(c.evidence_score * 100).toFixed(0)}%
              </span>
              <div style={{ display: "flex", gap: 4 }}>
                <button
                  disabled={busy}
                  onClick={() => setConfirming(
                    { sign: c.sign, reading: c.proposed_reading, action: "approve" })}
                  style={{
                    padding: "2px 7px", fontSize: 10, fontWeight: 700,
                    border: "1px solid #16a34a", borderRadius: 4,
                    background: "#dcfce7", color: "#15803d",
                    cursor: busy ? "default" : "pointer",
                  }}
                >
                  ✔ Approve
                </button>
                <button
                  disabled={busy}
                  onClick={() => setConfirming(
                    { sign: c.sign, reading: c.proposed_reading, action: "reject" })}
                  style={{
                    padding: "2px 7px", fontSize: 10, fontWeight: 700,
                    border: "1px solid #dc2626", borderRadius: 4,
                    background: "#fef2f2", color: "#dc2626",
                    cursor: busy ? "default" : "pointer",
                  }}
                >
                  ✕ Reject
                </button>
                <button
                  disabled={busy}
                  onClick={() => void doAction(c.sign, c.proposed_reading, "delete")}
                  title="Remove from queue (no audit trail)"
                  style={{
                    padding: "2px 6px", fontSize: 10,
                    border: "1px solid #d1d5db", borderRadius: 4,
                    background: "#f9fafb", color: "#6b7280",
                    cursor: busy ? "default" : "pointer",
                  }}
                >
                  Ὕ1
                </button>
              </div>
            </div>

            {/* Confirmation row */}
            {confirming?.sign === c.sign &&
             confirming?.reading === c.proposed_reading && (
              <div style={{
                padding: "8px 12px", background: "#fef9c3",
                borderBottom: "1px solid #fcd34d",
                display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap",
              }}>
                {confirming.action === "approve" ? (
                  <>
                    <span style={{ fontSize: 11, color: "#78350f", fontWeight: 600 }}>
                      Approve {c.sign} = &ldquo;{c.proposed_reading}&rdquo;?
                      This adds it to the review queue for future anchor promotion.
                    </span>
                    <button
                      disabled={busy}
                      onClick={() => void doAction(c.sign, c.proposed_reading, "approve")}
                      style={{
                        padding: "3px 10px", fontSize: 11, fontWeight: 700,
                        border: "1px solid #16a34a", borderRadius: 4,
                        background: "#16a34a", color: "#fff",
                        cursor: busy ? "default" : "pointer",
                      }}
                    >
                      Confirm approve
                    </button>
                    <button
                      disabled={busy}
                      onClick={() => setConfirming(null)}
                      style={{
                        padding: "3px 8px", fontSize: 11,
                        border: "1px solid #d1d5db", borderRadius: 4,
                        background: "#fff", cursor: "pointer",
                      }}
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <>
                    <span style={{ fontSize: 11, color: "#78350f", fontWeight: 600 }}>
                      Reject reason (optional):
                    </span>
                    <input
                      value={rejectReason}
                      onChange={(e) => setRejectReason(e.target.value)}
                      placeholder="e.g. insufficient DEDR evidence"
                      style={{
                        flex: 1, minWidth: 160, padding: "3px 7px",
                        border: "1px solid #d1d5db", borderRadius: 4,
                        fontSize: 11,
                      }}
                    />
                    <button
                      disabled={busy}
                      onClick={() => void doAction(
                        c.sign, c.proposed_reading, "reject", rejectReason)}
                      style={{
                        padding: "3px 10px", fontSize: 11, fontWeight: 700,
                        border: "1px solid #dc2626", borderRadius: 4,
                        background: "#dc2626", color: "#fff",
                        cursor: busy ? "default" : "pointer",
                      }}
                    >
                      Confirm reject
                    </button>
                    <button
                      disabled={busy}
                      onClick={() => { setConfirming(null); setRejectReason(""); }}
                      style={{
                        padding: "3px 8px", fontSize: 11,
                        border: "1px solid #d1d5db", borderRadius: 4,
                        background: "#fff", cursor: "pointer",
                      }}
                    >
                      Cancel
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        ))
      )}

      {/* Approved log (collapsed summary) */}
      {approvedCandidates.length > 0 && (
        <div style={{
          padding: "6px 10px", background: "#f0fdf4",
          borderTop: stagedCandidates.length > 0 ? "1px solid #bbf7d0" : undefined,
          fontSize: 11, color: "#15803d",
        }}>
          <strong>✔ {approvedCandidates.length} approved:</strong>{" "}
          {approvedCandidates.map((c) =>
            `${c.sign}=${c.proposed_reading}`).join(" · ")}
        </div>
      )}
    </div>
  );
}
