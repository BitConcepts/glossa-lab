/**
 * ResearchLoopPanel — Autonomous Study Loop dashboard panel.
 *
 * Shows last session insights, scheduler toggle, iteration presets,
 * live progress, and full run history. SSE events flow from
 * POST /api/v1/study-loop/start?iterations=N.
 *
 * API:
 *   POST /api/v1/study-loop/start?iterations=N    → SSE stream
 *   GET  /api/v1/study-loop/status                → current state
 *   POST /api/v1/study-loop/stop                  → graceful stop
 *   GET  /api/v1/study-loop/last-session          → last session insights
 *   GET  /api/v1/study-loop/history               → past sessions
 *   GET  /api/v1/study-loop/scheduler/status      → scheduler on/off
 *   POST /api/v1/study-loop/scheduler/enable      → enable daily loop
 *   POST /api/v1/study-loop/scheduler/disable     → disable daily loop
 */

import { Fragment, useCallback, useEffect, useState } from "react";

const BASE = "/api/v1/study-loop";

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
  review_status: "staged" | "blocked" | "approved" | "rejected" | "verified" | "expired";
  neighbor_reading?: string;
  neighbor_count?: number;
  corpus_freq?: number;
  animal_freq?: number;
  partner_reading?: string;
  verified_at?: string;
  archived_at?: string;
  archived_reason?: string;
  sa_delta?: number;
  recommended?: boolean;
  statistically_sufficient?: boolean;
}

interface TopFinding {
  experiment: string;
  metric: string;
  value: number | string;
  interpretation: string;
}

interface ProposedNext {
  experiment_id: string;
  display_name: string;
  rationale: string;
  priority: number;
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
  top_findings?: TopFinding[];
  proposed_next?: ProposedNext[];
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
  archive_counts?: { total: number; approved: number; verified: number; promotable: number };
  error?: string;
}

// ── Study-loop–specific types ────────────────────────────────────────────────

interface StudySession {
  session_id?: string;
  completed_at?: string;
  iterations_run?: number;
  coverage_before?: number;
  coverage_after?: number;
  anchor_delta?: number;
  where_we_came_from?: string;
  what_we_learned?: string;
  actions_taken?: string;
  whats_next?: string;
  synthesis?: Synthesis;
  total_papers_mined?: number;
  total_insights?: number;
}

interface SchedulerStatus {
  enabled: boolean;
  next_run?: string;
  last_run?: string;
}

interface HistorySession {
  session_id: string;
  completed_at: string;
  iterations_run: number;
  coverage_before?: number;
  coverage_after?: number;
  coverage_delta?: number;
  what_we_learned?: string;
}

export function ResearchLoopPanel() {
  const [, setStatus] = useState<LoopStatus | null>(null);
  const [running, setRunning] = useState(false);
  const [cycles, setCycles] = useState(15);
  const [log, setLog] = useState<CycleEntry[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [stallReason, setStallReason] = useState<string | null>(null);
  const [failureDetail, setFailureDetail] = useState<{
    reason: string;
    cycles_completed: number;
    last_experiment: string;
    elapsed_seconds: number;
  } | null>(null);
  const [lastRun, setLastRun] = useState<LastRun | null>(null);
  const [synthesis, setSynthesis] = useState<Synthesis | null>(null);
  const [staging, setStaging] = useState<StagingData | null>(null);
  const [showReview, setShowReview] = useState(false);
  const [proposalKey, setProposalKey] = useState<string | null>(null);
  const [currentPhase, setCurrentPhase] = useState<"idle" | "propose" | "build" | "verify" | "analyze">("idle");
  const [currentWork, setCurrentWork] = useState<{ cycle: number; gap: string; experiment: string } | null>(null);
  const [showFullLog, setShowFullLog] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  // Study-loop additions
  const [lastSession, setLastSession] = useState<StudySession | null>(null);
  const [showInsights, setShowInsights] = useState(true);
  const [schedulerStatus, setSchedulerStatus] = useState<SchedulerStatus | null>(null);
  const [schedulerBusy, setSchedulerBusy] = useState(false);
  const [history, setHistory] = useState<HistorySession[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/status`);
      if (res.ok) setStatus(await res.json() as LoopStatus);
    } catch { /* backend may not be running */ }
  }, []);

  const fetchLastSession = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/last-session`);
      if (!res.ok) return;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const raw = await res.json() as Record<string, any>;
      if (raw.no_sessions) return;

      // The API returns a nested structure; flatten it into StudySession.
      //   before.coverage / after.coverage  → coverage_before / coverage_after
      //   narrative.*                        → top-level narrative fields
      //   narrative.actions_taken (array)    → joined string
      //   iterations                         → iterations_run
      //   total_papers                       → total_papers_mined
      const narr = raw.narrative || {};
      const before = raw.before || {};
      const after  = raw.after  || {};
      const anchorDelta = ((after.anchors_hm ?? 0) - (before.anchors_hm ?? 0));

      const flat: StudySession = {
        session_id:      raw.session_id,
        completed_at:    raw.completed_at,
        iterations_run:  raw.iterations ?? raw.iterations_run,
        total_papers_mined: raw.total_papers ?? raw.total_papers_mined,
        total_insights:  raw.total_insights,
        synthesis:       raw.synthesis,
        // Coverage extracted from before/after snapshots
        coverage_before: before.coverage,
        coverage_after:  after.coverage,
        anchor_delta:    anchorDelta || undefined,
        // Narrative fields (nested under "narrative" in the API)
        where_we_came_from: narr.where_we_came_from,
        what_we_learned:    narr.what_we_learned,
        // actions_taken is an array in the API; join for display
        actions_taken: Array.isArray(narr.actions_taken)
          ? narr.actions_taken.join(" · ")
          : narr.actions_taken,
        whats_next: narr.whats_next,
      };

      setLastSession(flat);
      if (flat.synthesis) setSynthesis(flat.synthesis);
      setLastRun({
        completed_at:    flat.completed_at,
        total_papers_mined: flat.total_papers_mined,
        total_insights:  flat.total_insights,
        cycles_run:      flat.iterations_run,
        synthesis:       flat.synthesis,
      });
    } catch { /* ignore */ }
  }, []);

  const fetchStaging = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/staging`);
      if (res.ok) setStaging(await res.json() as StagingData);
    } catch { /* ignore */ }
  }, []);

  const fetchSchedulerStatus = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/scheduler/status`);
      if (res.ok) setSchedulerStatus(await res.json() as SchedulerStatus);
    } catch { /* ignore */ }
  }, []);

  const fetchHistory = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/history`);
      if (!res.ok) return;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const raw = await res.json() as { sessions?: any[] } | any[];
      // API returns {sessions: [...]} not []
      const sessions: any[] = Array.isArray(raw) ? raw : (raw as any).sessions ?? []; // eslint-disable-line @typescript-eslint/no-explicit-any
      setHistory(sessions.map((s: any) => ({ // eslint-disable-line @typescript-eslint/no-explicit-any
        session_id:    s.session_id,
        completed_at:  s.completed_at,
        iterations_run: s.iterations ?? s.iterations_run,
        coverage_before: s.before?.coverage,
        coverage_after:  s.after?.coverage,
        coverage_delta:  s.after && s.before
          ? (s.after.coverage ?? 0) - (s.before.coverage ?? 0)
          : undefined,
        what_we_learned: s.narrative?.what_we_learned,
      })));
    } catch { /* ignore */ }
  }, []);

  useEffect(() => {
    void fetchStatus();
    void fetchLastSession();
    void fetchStaging();
    void fetchSchedulerStatus();
    void fetchHistory();
  }, [fetchStatus, fetchLastSession, fetchStaging, fetchSchedulerStatus, fetchHistory]);

  const toggleScheduler = async () => {
    if (!schedulerStatus) return;
    setSchedulerBusy(true);
    try {
      const action = schedulerStatus.enabled ? "disable" : "enable";
      const res = await fetch(`${BASE}/scheduler/${action}`, { method: "POST" });
      if (res.ok) await fetchSchedulerStatus();
    } catch { /* ignore */ }
    finally { setSchedulerBusy(false); }
  };

  const startLoop = async (fromProposal?: string) => {
    if (fromProposal) {
      setProposalKey(fromProposal);
    } else {
      setProposalKey(null); // main button clears proposal tracking
    }
    setRunning(true);
    setError(null);
    setStallReason(null);
    setFailureDetail(null);
    setLog([]);
    setSynthesis(null);
    setCurrentPhase("idle");
    setCurrentWork(null);
    setShowFullLog(false);

    try {
      const res = await fetch(`${BASE}/start?iterations=${cycles}`, { method: "POST" });
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
                  reason?: string; cycles_completed?: number;
                  last_experiment?: string; elapsed_seconds?: number;
                  experiment?: string; rationale?: string;
                  summary?: string; flags?: string[];
                  ok?: boolean; timeout_seconds?: number; gap_targeted?: string;
                  session?: StudySession;
              };
              if (event.type === "complete") {
                setCurrentPhase("idle");
                setCurrentWork(null);
                if (event.synthesis) setSynthesis(event.synthesis);
                if (event.synthesis?.anchor_candidates && event.synthesis.anchor_candidates.length > 0) {
                  setTimeout(() => setShowReview(true), 400);
                }
                window.dispatchEvent(new CustomEvent("glossa:loop-complete"));
                void fetchStatus();
                void fetchLastSession();
                void fetchStaging();
                void fetchHistory();
              } else if (event.type === "study_loop_complete") {
                if (event.session) {
                  // Same flattening as fetchLastSession — session is nested
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  const s = event.session as any;
                  const narr = s.narrative || {};
                  const before = s.before || {};
                  const after  = s.after  || {};
                  const delta = ((after.anchors_hm ?? 0) - (before.anchors_hm ?? 0));
                  setLastSession({
                    session_id:      s.session_id,
                    completed_at:    s.completed_at,
                    iterations_run:  s.iterations ?? s.iterations_run,
                    total_papers_mined: s.total_papers ?? s.total_papers_mined,
                    total_insights:  s.total_insights,
                    synthesis:       s.synthesis,
                    coverage_before: before.coverage,
                    coverage_after:  after.coverage,
                    anchor_delta:    delta || undefined,
                    where_we_came_from: narr.where_we_came_from,
                    what_we_learned:    narr.what_we_learned,
                    actions_taken: Array.isArray(narr.actions_taken)
                      ? narr.actions_taken.join(" \u00b7 ")
                      : narr.actions_taken,
                    whats_next: narr.whats_next,
                  });
                  setShowInsights(true);
                }
              } else if (event.type === "proposal_selected") {
                setCurrentPhase("propose");
                if (event.cycle) setCurrentWork({ cycle: event.cycle ?? 0, gap: event.gap_targeted ?? "", experiment: event.experiment ?? "" });
                setLog((prev) => [...prev, {
                  cycle: event.cycle ?? 0, gap_targeted: "",
                  experiment: event.experiment ?? "", n_papers: 0, n_insights: 0,
                  insight_types: {}, verdict: `\u{1F4A1} Proposed: ${event.rationale ?? ""}`,
                  is_new_info: false, selection_method: "proposal",
                } as CycleEntry]);
              } else if (event.type === "verify_result") {
                setCurrentPhase("verify");
                setLog((prev) => [...prev, {
                  cycle: event.cycle ?? 0, gap_targeted: "",
                  experiment: event.experiment ?? "", n_papers: 0, n_insights: 0,
                  insight_types: {}, verdict: `\u2713 Verified: ${event.ok ? "pass" : "fail"}`,
                  is_new_info: false, selection_method: "verify",
                } as CycleEntry]);
              } else if (event.type === "analysis_complete") {
                setCurrentPhase("analyze");
                setLog((prev) => [...prev, {
                  cycle: event.cycle ?? 0, gap_targeted: "",
                  experiment: event.experiment ?? "", n_papers: 0, n_insights: 0,
                  insight_types: {}, verdict: `\u{1F4CA} ${(event.summary ?? "").slice(0, 80)}`,
                  is_new_info: false, selection_method: "analysis",
                } as CycleEntry]);
              } else if (event.type === "cycle_timeout") {
                setLog((prev) => [...prev, {
                  cycle: event.cycle ?? 0, gap_targeted: "",
                  experiment: event.experiment ?? "", n_papers: 0, n_insights: 0,
                  insight_types: {}, verdict: `\u23F1 Timeout (${event.timeout_seconds ?? 300}s)`,
                  is_new_info: false, selection_method: "timeout",
                } as CycleEntry]);
              } else if (event.type === "gap_skipped") {
                setLog((prev) => [...prev, {
                  cycle: event.cycle ?? 0, gap_targeted: event.gap_targeted ?? "",
                  experiment: "", n_papers: 0, n_insights: 0,
                  insight_types: {}, verdict: `\u23ED Gap skipped: ${event.reason ?? ""}`,
                  is_new_info: false, selection_method: "skipped",
                } as CycleEntry]);
              } else if (event.type === "error") {
                setError(event.reason || "Loop failed");
                setStallReason(event.reason === "timeout" ? "timeout" : null);
                setFailureDetail({
                  reason: event.reason || "unknown",
                  cycles_completed: event.cycles_completed ?? 0,
                  last_experiment: event.last_experiment ?? "",
                  elapsed_seconds: event.elapsed_seconds ?? 0,
                });
              } else if (event.type === "node_complete" && event.cycle) {
                setCurrentPhase("build");
                setCurrentWork({ cycle: event.cycle, gap: event.gap_targeted ?? "", experiment: event.experiment ?? "" });
                setLog((prev) => {
                  const entry: CycleEntry = {
                    cycle: event.cycle ?? 0,
                    gap_targeted: event.gap_targeted ?? "",
                    experiment: event.experiment ?? "",
                    n_papers: 0, n_insights: 0,
                    insight_types: {},
                    verdict: event.verdict ?? `⚙ ${event.experiment ?? "node"}`,
                    is_new_info: false,
                    selection_method: "node_complete",
                  };
                  const next = [...prev, entry];
                  return next.length > 400 ? next.slice(next.length - 400) : next;
                });
              } else if (event.cycle) {
                setCurrentPhase("build");
                setCurrentWork({ cycle: event.cycle, gap: event.gap_targeted ?? "", experiment: event.experiment ?? "" });
                setLog((prev) => {
                  const entry: CycleEntry = {
                    cycle: event.cycle ?? 0,
                    gap_targeted: event.gap_targeted ?? "",
                    experiment: event.experiment ?? "",
                    n_papers: event.n_papers ?? 0,
                    n_insights: event.n_insights ?? 0,
                    insight_types: (event.insight_types ?? {}) as Record<string, number>,
                    verdict: event.verdict ?? "",
                    is_new_info: event.is_new_info ?? false,
                    selection_method: event.selection_method ?? "cycle",
                  };
                  const next = [...prev, entry];
                  return next.length > 400 ? next.slice(next.length - 400) : next;
                });
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
  const totalPapers = log.reduce((s, c) => s + (c.n_papers ?? 0), 0);
  const totalInsights = log.reduce((s, c) => s + (c.n_insights ?? 0), 0);

  return (
    <div style={{ border: "1px solid #c4b5fd", borderRadius: 10, padding: 16,
                  background: "#faf5ff", marginBottom: 16 }}>

      {/* ── Header ── */}
      <div style={{ display: "flex", justifyContent: "space-between",
                    alignItems: "center", marginBottom: 6 }}>
        <div>
          <span style={{ fontSize: 16, fontWeight: 700, color: "#5b21b6" }}>
            📚 Autonomous Study Loop
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
            <option value={5}>5 — Quick Scan</option>
            <option value={15}>15 — Standard</option>
            <option value={30}>30 — Deep Dive</option>
            <option value={50}>50 — Extensive</option>
          </select>
          {!running && !showConfirm && (
            <button onClick={() => setShowConfirm(true)}
              title="Start the autonomous study loop"
              style={{ padding: "6px 14px", border: "1px solid #7c3aed",
                       borderRadius: 6, background: "#7c3aed", color: "#fff",
                       fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
              ▶ Run Loop
            </button>
          )}
          {running && (
            <button onClick={() => void stopLoop()}
              style={{ padding: "6px 14px", border: "1px solid #dc2626",
                       borderRadius: 6, background: "#dc2626", color: "#fff",
                       fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
              ■ Stop
            </button>
          )}
        </div>
      </div>

      {/* ── Daily scheduler toggle ── */}
      {schedulerStatus && (
        <div style={{
          display: "flex", alignItems: "center", gap: 8,
          fontSize: 11, marginBottom: 10,
          padding: "6px 10px", background: "#f9fafb",
          border: "1px solid #e5e7eb", borderRadius: 5,
        }}>
          <span style={{ color: "#374151" }}>
            Daily loop:{" "}
            <strong style={{ color: schedulerStatus.enabled ? "#15803d" : "#9ca3af" }}>
              {schedulerStatus.enabled ? "Enabled" : "Disabled"}
            </strong>
          </span>
          {schedulerStatus.next_run && schedulerStatus.enabled && (
            <span style={{ color: "#6b7280" }}>
              · next:{" "}
              {new Date(schedulerStatus.next_run).toLocaleString(undefined, {
                month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
              })}
            </span>
          )}
          <button
            disabled={schedulerBusy}
            onClick={() => void toggleScheduler()}
            style={{
              marginLeft: "auto",
              padding: "3px 10px", fontSize: 10, fontWeight: 600,
              border: `1px solid ${schedulerStatus.enabled ? "#dc2626" : "#16a34a"}`,
              borderRadius: 4,
              background: schedulerBusy ? "#f3f4f6" : schedulerStatus.enabled ? "#fef2f2" : "#dcfce7",
              color: schedulerStatus.enabled ? "#dc2626" : "#15803d",
              cursor: schedulerBusy ? "default" : "pointer",
            }}>
            {schedulerBusy ? "…" : schedulerStatus.enabled ? "Disable" : "Enable"}
          </button>
        </div>
      )}

      {/* ── Session Insights card ── */}
      {!running && lastSession && showInsights && lastSession.completed_at && (
        <div style={{
          border: "1px solid #a5b4fc", borderRadius: 8, background: "#eef2ff",
          padding: "12px 16px", marginBottom: 12,
        }}>
          <div style={{ display: "flex", justifyContent: "space-between",
                        alignItems: "center", marginBottom: 10 }}>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#4338ca" }}>
              📊 Session Insights
            </span>
            <button
              onClick={() => setShowInsights(false)}
              style={{
                padding: "3px 10px", fontSize: 10, fontWeight: 600,
                border: "1px solid #c7d2fe", borderRadius: 4,
                background: "#fff", color: "#6366f1", cursor: "pointer",
              }}>
              Dismiss
            </button>
          </div>

          {/* Coverage before/after bar */}
          {lastSession.coverage_before != null && lastSession.coverage_after != null && (
            <div style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 11, fontWeight: 600, color: "#374151",
                            marginBottom: 4 }}>
                Coverage
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 11, color: "#6b7280", width: 50,
                               textAlign: "right" }}>
                  {(lastSession.coverage_before * 100).toFixed(1)}%
                </span>
                <div style={{ flex: 1, height: 10, background: "#e5e7eb",
                              borderRadius: 5, overflow: "hidden", position: "relative" }}>
                  <div style={{
                    position: "absolute", left: 0, top: 0, height: "100%",
                    width: `${lastSession.coverage_after * 100}%`,
                    background: "#6366f1", borderRadius: 5,
                    transition: "width 0.4s",
                  }} />
                  <div style={{
                    position: "absolute", left: 0, top: 0, height: "100%",
                    width: `${lastSession.coverage_before * 100}%`,
                    background: "#a5b4fc", borderRadius: 5,
                  }} />
                </div>
                <span style={{ fontSize: 11, color: "#4338ca", fontWeight: 700,
                               width: 50 }}>
                  {(lastSession.coverage_after * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          )}

          {/* Anchor delta */}
          {lastSession.anchor_delta != null && lastSession.anchor_delta !== 0 && (
            <div style={{
              fontSize: 11, marginBottom: 8, fontWeight: 600,
              color: lastSession.anchor_delta > 0 ? "#15803d" : "#dc2626",
            }}>
              Anchor Δ: {lastSession.anchor_delta > 0 ? "+" : ""}
              {lastSession.anchor_delta}
            </div>
          )}

          {/* Narrative fields */}
          {lastSession.where_we_came_from && (
            <NarrativeField label="Where we came from"
                            text={lastSession.where_we_came_from} />
          )}
          {lastSession.what_we_learned && (
            <NarrativeField label="What we learned"
                            text={lastSession.what_we_learned} />
          )}
          {lastSession.actions_taken && (
            <NarrativeField label="Actions taken"
                            text={lastSession.actions_taken} />
          )}
          {lastSession.whats_next && (
            <NarrativeField label="What's next"
                            text={lastSession.whats_next} />
          )}
        </div>
      )}

      {/* ── Confirmation panel ── */}
      {!running && showConfirm && (
        <div style={{
          border: "1px solid #c4b5fd", borderRadius: 8, padding: "12px 16px",
          background: "#ede9fe", marginBottom: 12,
        }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: "#5b21b6", marginBottom: 8 }}>
            🔄 Study Loop — {cycles} iterations
          </div>
          <div style={{ fontSize: 11, color: "#374151", lineHeight: 1.8 }}>
            <div>📘 <strong>Mine</strong>: Blitz all gap topics for literature evidence</div>
            <div>💡 <strong>Propose</strong>: Select the highest-signal experiment for each gap</div>
            <div>⚙️ <strong>Run &amp; Analyze</strong>: Execute, interpret, stage anchor candidates</div>
            <div>🔄 <strong>Iterate</strong>: Repeat for each of the {cycles} iterations</div>
          </div>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 10 }}>
            <button
              onClick={() => setShowConfirm(false)}
              style={{
                padding: "6px 14px", border: "1px solid #d1d5db",
                borderRadius: 6, background: "#fff", color: "#374151",
                fontSize: 12, fontWeight: 600, cursor: "pointer",
              }}>
              Cancel
            </button>
            <button
              onClick={() => { setShowConfirm(false); void startLoop(); }}
              style={{
                padding: "6px 14px", border: "1px solid #7c3aed",
                borderRadius: 6, background: "#7c3aed", color: "#fff",
                fontSize: 12, fontWeight: 600, cursor: "pointer",
              }}>
              ▶ Start
            </button>
          </div>
        </div>
      )}

      {/* ── Live progress: phase strip + metrics + collapsed log ── */}
      {(running || log.length > 0) && (
        <div style={{ marginBottom: 12 }}>
          {/* Phase progress strip */}
          <div style={{ display: "flex", alignItems: "center", gap: 0, marginBottom: 8 }}>
            {(["propose", "build", "verify", "analyze"] as const).map((phase, i) => {
              const labels: Record<string, string> = {
                propose: "Propose", build: "Build", verify: "Verify", analyze: "Analyze"
              };
              const active = currentPhase === phase;
              const done = running &&
                (["propose", "build", "verify", "analyze"].indexOf(currentPhase) >
                 ["propose", "build", "verify", "analyze"].indexOf(phase));
              return (
                <Fragment key={phase}>
                  {i > 0 && (
                    <div style={{ width: 20, height: 1,
                      background: done || active ? "#7c3aed" : "#d1d5db" }} />
                  )}
                  <div style={{
                    padding: "4px 12px", borderRadius: 14, fontSize: 11, fontWeight: active ? 800 : 600,
                    background: active ? "#7c3aed" : done ? "#ede9fe" : "#f3f4f6",
                    color: active ? "#fff" : done ? "#5b21b6" : "#9ca3af",
                    border: active ? "none" : "1px solid transparent",
                    transition: "all 0.2s",
                  }}>
                    {labels[phase]}
                  </div>
                </Fragment>
              );
            })}
            {running && (
              <div style={{ marginLeft: "auto", fontSize: 11, color: "#6b7280" }}>
                {log.length}/{cycles} cycles
              </div>
            )}
          </div>

          {/* Current work line */}
          {currentWork && (
            <div style={{ fontSize: 11, color: "#374151", padding: "4px 8px",
                          background: "#f9fafb", borderRadius: 5,
                          border: "1px solid #e5e7eb", marginBottom: 6,
                          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              <span style={{ color: "#7c3aed", fontWeight: 700 }}>C{currentWork.cycle}</span>
              {" · "}
              <span style={{ color: "#374151" }}>{currentWork.gap}</span>
              {currentWork.experiment && <>
                {" → "}
                <span style={{ color: "#1d4ed8" }}>{currentWork.experiment.slice(0, 40)}</span>
              </>}
            </div>
          )}

          {/* Metrics row (only after some cycles) */}
          {log.length > 0 && (
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr",
                          gap: 6, marginBottom: 8 }}>
              <MetricTile label="Cycles" value={log.length} />
              <MetricTile label="Papers" value={totalPapers} />
              <MetricTile label="Insights" value={totalInsights} />
              <MetricTile label="New" value={log.filter((c) => c.is_new_info).length} />
            </div>
          )}

          {/* Collapsed full log */}
          {log.length > 0 && (
            <details open={showFullLog} onToggle={(e) => setShowFullLog((e.currentTarget as HTMLDetailsElement).open)}
              style={{ fontSize: 11, border: "1px solid #e5e7eb", borderRadius: 5 }}>
              <summary style={{ padding: "4px 10px", cursor: "pointer",
                                color: "#6b7280", background: "#f9fafb",
                                listStyle: "none", display: "flex",
                                justifyContent: "space-between", alignItems: "center" }}>
                <span>Full log</span>
                <span style={{ fontSize: 10 }}>{log.length} events {showFullLog ? "▲" : "▼"}</span>
              </summary>
              <div style={{ maxHeight: 200, overflowY: "auto", background: "#fff" }}>
                {log.map((entry, idx) => (
                  <div key={`${entry.cycle}-${entry.gap_targeted}-${idx}`}
                    style={{ display: "flex", alignItems: "center", gap: 6,
                             padding: "4px 10px", borderBottom: "1px solid #f3f4f6",
                             fontSize: 10 }}>
                    <span style={{ width: 22, fontWeight: 700, color: "#7c3aed", flexShrink: 0 }}>C{entry.cycle}</span>
                    <span style={{ width: 100, color: "#374151", overflow: "hidden",
                                   textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {entry.gap_targeted}
                    </span>
                    <span style={{ flex: 1, color: "#6b7280", overflow: "hidden",
                                   textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {(entry.verdict ?? "").slice(0, 60)}
                    </span>
                    <InsightTypePills types={entry.insight_types} max={2} />
                    <span style={{ fontSize: 9, padding: "1px 4px", borderRadius: 3,
                                   background: entry.is_new_info ? "#dcfce7" : "#f3f4f6",
                                   color: entry.is_new_info ? "#15803d" : "#9ca3af",
                                   fontWeight: 600, flexShrink: 0 }}>
                      {entry.is_new_info ? "NEW" : "rpt"}
                    </span>
                  </div>
                ))}
              </div>
            </details>
          )}
        </div>
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
      {staging?.counts != null &&
        ((staging.counts.staged ?? 0) > 0 ||
         (staging.counts.approved ?? 0) > 0 ||
         (staging.counts.rejected ?? 0) > 0) && (
        <div style={{ marginTop: 8 }}>
          <button
            onClick={() => setShowReview((v) => !v)}
            style={{
              width: "100%", padding: "8px 14px",
              border: `1px solid ${(staging.counts.staged ?? 0) > 0 ? "#f59e0b" : "#86efac"}`,
              borderRadius: 6,
              background: showReview
                ? ((staging.counts.staged ?? 0) > 0 ? "#fef3c7" : "#f0fdf4")
                : ((staging.counts.staged ?? 0) > 0 ? "#fffbeb" : "#f9fafb"),
              color: (staging.counts.staged ?? 0) > 0 ? "#92400e" : "#15803d",
              fontSize: 12, fontWeight: 700,
              cursor: "pointer", textAlign: "left",
              display: "flex", justifyContent: "space-between", alignItems: "center",
            }}
          >
            <span>
              🔬{" "}
              {(staging.counts.staged ?? 0) > 0
                ? `${staging.counts.staged} anchor candidate${staging.counts.staged !== 1 ? "s" : ""} awaiting review`
                : "Anchor staging"}
              {(staging.counts.approved ?? 0) > 0 && (
                <span style={{ marginLeft: 8, color: "#15803d" }}>
                  · ✓ {staging.counts.approved} approved
                </span>
              )}
              {(staging.counts.rejected ?? 0) > 0 && (
                <span style={{ marginLeft: 6, color: "#9ca3af" }}>
                  · ✕ {staging.counts.rejected} rejected
                </span>
              )}
            </span>
            <span style={{ fontSize: 11, fontWeight: 400 }}>
              {showReview ? "Hide ▲" : ((staging.counts.staged ?? 0) > 0 ? "Review ▼" : "View ▼")}
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
              onArchive={async () => {
                await fetch(`${BASE}/staging/archive`, { method: "POST" });
                void fetchStaging();
              }}
              onDelete={async () => {
                const res = await fetch(`${BASE}/staging/rejected`, { method: "DELETE" });
                if (res.ok) await fetchStaging();
              }}
              onCleanup={async () => {
                const res = await fetch(`${BASE}/staging/cleanup`, { method: "POST" });
                if (res.ok) await fetchStaging();
              }}
            />
          )}
        </div>
      )}

      {/* ── Promote to Anchors ── (always shown when archive has promotable items) */}
      {(staging?.archive_counts?.promotable ?? 0) > 0 && (
        <div style={{ marginTop: 6 }}>
          <PromoteToAnchors
            promotable={staging!.archive_counts!.promotable}
            archiveTotal={staging!.archive_counts!.total}
            onPromoted={() => void fetchStaging()}
          />
        </div>
      )}

      {/* ── Fallback: no run yet ── */}
      {!running && !log.length && !activeSynthesis && lastRun?.no_runs && (
        <div style={{ fontSize: 12, color: "#9ca3af", textAlign: "center",
                      padding: "16px 0" }}>
          No sessions yet. Start the loop to begin mining.
        </div>
      )}

      {error && (
        <div style={{ marginTop: 8, fontSize: 12, color: "#dc2626",
                      background: "#fef2f2", border: "1px solid #fca5a5",
                      borderRadius: 6, padding: "6px 10px" }}>
          {error}
          {failureDetail && (
            <div style={{ marginTop: 6, fontSize: 11, color: "#7f1d1d",
                          borderTop: "1px solid #fca5a5", paddingTop: 6 }}>
              {stallReason === "timeout" && (
                <div style={{ marginBottom: 4, fontWeight: 700 }}>
                  ⏱ Loop timed out after {failureDetail.cycles_completed} cycles.
                  Try fewer cycles or check backend logs.
                </div>
              )}
              <div>Cycles completed: {failureDetail.cycles_completed}</div>
              {failureDetail.last_experiment && (
                <div>Last experiment attempted: <code style={{
                  background: "#fee2e2", padding: "0 4px", borderRadius: 2, fontSize: 10,
                }}>{failureDetail.last_experiment}</code></div>
              )}
              <div>Time elapsed: {failureDetail.elapsed_seconds < 60
                ? `${failureDetail.elapsed_seconds}s`
                : `${Math.floor(failureDetail.elapsed_seconds / 60)}m ${Math.round(failureDetail.elapsed_seconds % 60)}s`
              }</div>
              {stallReason !== "timeout" && failureDetail.reason && (
                <div style={{ marginTop: 4, fontFamily: "monospace", fontSize: 10,
                              color: "#991b1b", wordBreak: "break-all" }}>
                  {failureDetail.reason}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* ── Loop History ── */}
      {history.length > 0 && (
        <details
          open={showHistory}
          onToggle={(e) => setShowHistory((e.currentTarget as HTMLDetailsElement).open)}
          style={{ fontSize: 11, border: "1px solid #e5e7eb", borderRadius: 5, marginTop: 10 }}>
          <summary style={{
            padding: "6px 10px", cursor: "pointer",
            color: "#6b7280", background: "#f9fafb",
            listStyle: "none", display: "flex",
            justifyContent: "space-between", alignItems: "center",
          }}>
            <span>📜 Loop History</span>
            <span style={{ fontSize: 10 }}>
              {history.length} session{history.length !== 1 ? "s" : ""}{" "}
              {showHistory ? "▲" : "▼"}
            </span>
          </summary>
          <div style={{ maxHeight: 200, overflowY: "auto", background: "#fff" }}>
            {history.map((h) => (
              <div key={h.session_id} style={{
                display: "flex", alignItems: "center", gap: 8,
                padding: "5px 10px", borderBottom: "1px solid #f3f4f6",
                fontSize: 10,
              }}>
                <span style={{ width: 80, color: "#6b7280", flexShrink: 0 }}>
                  {new Date(h.completed_at).toLocaleDateString(undefined, {
                    month: "short", day: "numeric",
                  })}
                </span>
                <span style={{ width: 50, color: "#5b21b6", fontWeight: 600, flexShrink: 0 }}>
                  {h.iterations_run} iter
                </span>
                {h.coverage_delta != null && (
                  <span style={{
                    width: 60, fontWeight: 600, flexShrink: 0,
                    color: h.coverage_delta > 0 ? "#15803d" : "#6b7280",
                  }}>
                    {h.coverage_delta > 0 ? "+" : ""}
                    {(h.coverage_delta * 100).toFixed(1)}%
                  </span>
                )}
                <span style={{
                  flex: 1, color: "#374151",
                  overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
                }}>
                  {h.what_we_learned?.slice(0, 80) ?? "—"}
                </span>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}

// ── Narrative field helper ────────────────────────────────────────────────────

function NarrativeField({ label, text }: { label: string; text: string }) {
  return (
    <div style={{ marginBottom: 6 }}>
      <div style={{
        fontSize: 10, fontWeight: 700, color: "#4338ca",
        textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 2,
      }}>
        {label}
      </div>
      <div style={{ fontSize: 11, color: "#374151", lineHeight: 1.5 }}>
        {text}
      </div>
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
  // Fetch live foundation status so it's not stale from last loop run
  const [liveFC, setLiveFC] = useState<FoundationCheck | null>(null);
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("/api/v1/foundation/status");
        if (res.ok) {
          const data = await res.json() as { n_ok?: number; n_fail?: number; n_warn?: number; verdict?: string };
          if (data.verdict != null) {
            setLiveFC({
              n_ok: data.n_ok ?? 0,
              n_fail: data.n_fail ?? 0,
              n_warn: data.n_warn ?? 0,
              verdict: data.verdict ?? "UNKNOWN",
              failed: [],
            });
          }
        }
      } catch { /* use synthesis fallback */ }
    })();
    // Also listen for foundation_complete events to refresh
    const handler = () => {
      fetch("/api/v1/foundation/status")
        .then(r => r.ok ? r.json() : null)
        .then((data: { n_ok?: number; n_fail?: number; n_warn?: number; verdict?: string } | null) => {
          if (data?.verdict != null) {
            setLiveFC({
              n_ok: data.n_ok ?? 0,
              n_fail: data.n_fail ?? 0,
              n_warn: data.n_warn ?? 0,
              verdict: data.verdict ?? "UNKNOWN",
              failed: [],
            });
          }
        })
        .catch(() => {});
    };
    window.addEventListener("glossa:foundation-updated", handler);
    return () => window.removeEventListener("glossa:foundation-updated", handler);
  }, []);

  const fc = liveFC ?? synthesis.foundation_check;
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

      {/* Top Findings (Phase E) */}
      {(synthesis.top_findings?.length ?? 0) > 0 && (
        <div style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: "#374151",
                        marginBottom: 6 }}>Top findings</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            {synthesis.top_findings!.slice(0, 3).map((f, i) => (
              <div key={i} style={{ display: "flex", gap: 8, alignItems: "flex-start",
                                    padding: "5px 8px", borderRadius: 5,
                                    background: "#f0fdf4",
                                    border: "1px solid #bbf7d0" }}>
                <span style={{ fontSize: 13, flexShrink: 0 }}>📈</span>
                <div style={{ flex: 1 }}>
                  <span style={{ fontSize: 11, fontWeight: 600, color: "#15803d" }}>
                    {f.experiment.replace(/_/g, " ")}
                  </span>
                  <span style={{ fontSize: 11, color: "#6b7280", marginLeft: 6 }}>
                    {f.metric}={typeof f.value === "number" ? (f.value as number).toFixed(3) : f.value}
                  </span>
                  <div style={{ fontSize: 10, color: "#374151", marginTop: 2 }}>
                    {f.interpretation}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Proposed Next Experiments (Phase E) */}
      {(synthesis.proposed_next?.length ?? 0) > 0 && (
        <div style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: "#374151",
                        marginBottom: 6 }}>Proposed next experiments</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            {synthesis.proposed_next!.map((p, i) => (
              <div key={i} style={{ display: "flex", gap: 8, alignItems: "center",
                                    padding: "5px 8px", borderRadius: 5,
                                    background: "#ede9fe",
                                    border: "1px solid #c4b5fd" }}>
                <span style={{ fontSize: 13, flexShrink: 0 }}>🔬</span>
                <div style={{ flex: 1, fontSize: 11, color: "#374151" }}>
                  <span style={{ fontWeight: 600, color: "#5b21b6" }}>
                    {p.display_name}
                  </span>
                  <span style={{ marginLeft: 6, color: "#6b7280" }}>
                    — {p.rationale}
                  </span>
                </div>
                {onStartLoop && (
                  <button
                    disabled={loopRunning}
                    onClick={() => onStartLoop(p.experiment_id)}
                    style={{
                      padding: "2px 8px", fontSize: 10, fontWeight: 700,
                      borderRadius: 4, whiteSpace: "nowrap", flexShrink: 0,
                      cursor: loopRunning ? "default" : "pointer",
                      border: "1px solid #7c3aed",
                      background: loopRunning ? "#f3f4f6" : "#7c3aed",
                      color: loopRunning ? "#9ca3af" : "#fff",
                    }}
                  >
                    ▶ Run
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Proposals — filter out stale fix_foundation when live FC passes */}
      {(() => {
        const liveProposals = synthesis.proposals.filter(
          (p) => !(p.action === "fix_foundation" && fc && !fc.skipped && fc.n_fail === 0),
        );
        return liveProposals.length > 0 ? (
        <div>
          <div style={{ fontSize: 11, fontWeight: 600, color: "#374151",
                        marginBottom: 6 }}>Next steps</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            {liveProposals.slice(0, 4).map((p, i) => {
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
      ) : null;
      })()}

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
              <LifecycleBadge status={c.review_status} />
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

/** Lifecycle stage badge for anchor candidates. */
function LifecycleBadge({ status }: { status: string }) {
  const styles: Record<string, { bg: string; fg: string; label: string }> = {
    staged:   { bg: "#dcfce7", fg: "#15803d", label: "staged" },
    approved: { bg: "#dbeafe", fg: "#1d4ed8", label: "approved" },
    rejected: { bg: "#fef2f2", fg: "#991b1b", label: "rejected" },
    verified: { bg: "#ecfdf5", fg: "#065f46", label: "verified" },
    expired:  { bg: "#f3f4f6", fg: "#6b7280", label: "expired" },
    blocked:  { bg: "#fef3c7", fg: "#92400e", label: "blocked" },
  };
  const s = styles[status] ?? styles.staged;
  return (
    <span style={{
      fontSize: 10, padding: "1px 5px", borderRadius: 3,
      background: s.bg, color: s.fg,
      fontWeight: 600, textAlign: "center",
    }}>
      {s.label}
    </span>
  );
}

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
  const entries = Object.entries(types ?? {}).sort(([, a], [, b]) => b - a).slice(0, max);
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

type StagingAction = "approve" | "reject" | "delete" | "staged";

function StagingReview({
  staging,
  onAction,
  onArchive: _onArchive,
  onDelete,
  onCleanup,
}: {
  staging: StagingData;
  onAction: (sign: string, reading: string, action: StagingAction,
             reason?: string) => Promise<void>;
  onArchive: () => Promise<void>;
  onDelete: () => Promise<void>;
  onCleanup: () => Promise<void>;
}) {
  void _onArchive; // retained for caller compatibility; cleanup replaces manual archive
  const [bulkBusy, setBulkBusy] = useState<"approve" | "reject" | "cleanup" | null>(null);
  const [busyKey,  setBusyKey]  = useState<string | null>(null);
  const [deleteConfirm, setdeleteConfirm] = useState(false);
  const [rejectingKey, setRejectingKey] = useState<string | null>(null);
  const [rejectReason, setRejectReason] = useState("");
  const [showApproved, setShowApproved] = useState(true);
  const [showRejected, setShowRejected] = useState(false);

  // ── Optimistic local overrides ────────────────────────────────────────
  const [pendingOverrides, setPendingOverrides] = useState<Record<string, "approved" | "rejected" | null>>({});

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    const serverStatus: Record<string, string> = {};
    for (const c of staging.candidates) {
      serverStatus[`${c.sign}:${c.proposed_reading}`] = c.review_status;
    }
    setPendingOverrides(prev => {
      const next: Record<string, "approved" | "rejected" | null> = {};
      let changed = false;
      for (const [key, override] of Object.entries(prev)) {
        const serverSt = serverStatus[key];
        if (override === null) {
          if (key in serverStatus) { next[key] = null; } else { changed = true; }
        } else if (serverSt && serverSt !== override) {
          next[key] = override;
        } else {
          changed = true;
        }
      }
      return changed || Object.keys(next).length !== Object.keys(prev).length ? next : prev;
    });
  }, [staging]);

  const effectiveCandidates: AnchorCandidate[] = staging.candidates.flatMap((c): AnchorCandidate[] => {
    const key = `${c.sign}:${c.proposed_reading}`;
    if (!(key in pendingOverrides)) return [c];
    const ov = pendingOverrides[key];
    if (ov === null) return [];
    return [{ ...c, review_status: ov }];
  });

  const staged   = effectiveCandidates.filter((c) => c.review_status === "staged");
  const approved = effectiveCandidates.filter((c) => c.review_status === "approved");
  const rejected = effectiveCandidates.filter((c) => c.review_status === "rejected");

  const isBusy = bulkBusy !== null || busyKey !== null;

  const applyOverride = (sign: string, reading: string, action: StagingAction) => {
    const key = `${sign}:${reading}`;
    setPendingOverrides((prev) => {
      const next = { ...prev };
      if (action === "delete") {
        next[key] = null;
      } else if (action === "approve") {
        next[key] = "approved";
      } else if (action === "reject") {
        next[key] = "rejected";
      } else {
        delete next[key];
      }
      return next;
    });
  };

  const doOne = async (sign: string, reading: string, action: StagingAction, reason?: string) => {
    applyOverride(sign, reading, action);
    const key = `${sign}:${reading}`;
    setBusyKey(key);
    try { await onAction(sign, reading, action, reason); }
    finally { setBusyKey(null); setRejectingKey(null); setRejectReason(""); }
  };

  const acceptRecommended = async () => {
    const recs = staged.filter((c) => c.recommended);
    setPendingOverrides((prev) => {
      const next = { ...prev };
      for (const c of recs) next[`${c.sign}:${c.proposed_reading}`] = "approved";
      return next;
    });
    setBulkBusy("approve");
    try {
      for (const c of recs)
        await onAction(c.sign, c.proposed_reading, "approve");
    } finally { setBulkBusy(null); }
  };

  const [verifySABusy, setVerifySABusy] = useState(false);
  const [verifyResult, setVerifyResult] = useState<{
    ok: boolean; message: string; suggested_sa_exp?: string; suggested_sa_name?: string;
  } | null>(null);
  const [saRunBusy, setSaRunBusy] = useState(false);
  const [saRunDone, setSaRunDone] = useState(false);
  const [cleanupBusy, setCleanupBusy] = useState(false);
  const [cleanupResult, setCleanupResult] = useState<{ ok: boolean; message: string } | null>(null);

  const verifyAndArchive = async () => {
    setVerifySABusy(true);
    setVerifyResult(null);
    setSaRunDone(false);
    try {
      const res = await fetch(`${BASE}/staging/verify-sa`, { method: "POST" });
      const data = await res.json() as {
        ok: boolean; message: string; suggested_sa_exp?: string;
        suggested_sa_name?: string; error?: string;
      };
      if (data.ok) {
        setPendingOverrides((prev) => {
          const next = { ...prev };
          for (const c of approved) next[`${c.sign}:${c.proposed_reading}`] = null;
          return next;
        });
      }
      setVerifyResult({
        ok: data.ok,
        message: data.message ?? data.error ?? "Done",
        suggested_sa_exp: data.suggested_sa_exp ?? undefined,
        suggested_sa_name: data.suggested_sa_name ?? undefined,
      });
    } catch (e) {
      setVerifyResult({ ok: false, message: e instanceof Error ? e.message : "Request failed" });
    } finally {
      setVerifySABusy(false);
    }
  };

  const runSaValidation = async (expId: string) => {
    setSaRunBusy(true);
    try {
      const res = await fetch(`/api/v1/experiment-graphs/${encodeURIComponent(expId)}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ kwargs: {}, notify: false }),
      });
      if (res.ok) {
        setSaRunDone(true);
        await onCleanup();
      }
    } catch { /* ignore */ }
    finally { setSaRunBusy(false); }
  };

  const handleCleanup = async () => {
    setPendingOverrides((prev) => {
      const next = { ...prev };
      for (const c of [...approved, ...rejected]) next[`${c.sign}:${c.proposed_reading}`] = null;
      return next;
    });
    setCleanupBusy(true);
    setCleanupResult(null);
    try {
      const res = await fetch(`${BASE}/staging/cleanup`, { method: "POST" });
      const data = await res.json() as { ok: boolean; message: string };
      setCleanupResult(data);
      await onCleanup();
    } catch (e) {
      setCleanupResult({ ok: false, message: e instanceof Error ? e.message : "Request failed" });
    } finally {
      setCleanupBusy(false);
    }
  };

  const approveAll = async () => {
    const snap = [...staged];
    setPendingOverrides((prev) => {
      const next = { ...prev };
      for (const c of snap) next[`${c.sign}:${c.proposed_reading}`] = "approved";
      return next;
    });
    setBulkBusy("approve");
    try { for (const c of snap) await onAction(c.sign, c.proposed_reading, "approve"); }
    finally { setBulkBusy(null); }
  };
  const rejectRemaining = async () => {
    const snap = [...staged];
    setPendingOverrides((prev) => {
      const next = { ...prev };
      for (const c of snap) next[`${c.sign}:${c.proposed_reading}`] = "rejected";
      return next;
    });
    setBulkBusy("reject");
    try { for (const c of snap) await onAction(c.sign, c.proposed_reading, "reject", "batch reject"); }
    finally { setBulkBusy(null); }
  };
  const unstageAll = async () => {
    setBulkBusy("approve");
    const snap = [...approved];
    setPendingOverrides((prev) => {
      const next = { ...prev };
      for (const c of snap) delete next[`${c.sign}:${c.proposed_reading}`];
      return next;
    });
    try { for (const c of snap) await onAction(c.sign, c.proposed_reading, "staged"); }
    finally { setBulkBusy(null); }
  };
  const restageAll = async () => {
    setBulkBusy("reject");
    const snap = [...rejected];
    setPendingOverrides((prev) => {
      const next = { ...prev };
      for (const c of snap) delete next[`${c.sign}:${c.proposed_reading}`];
      return next;
    });
    try { for (const c of snap) await onAction(c.sign, c.proposed_reading, "staged"); }
    finally { setBulkBusy(null); }
  };
  const deleteRejected = async () => {
    setdeleteConfirm(false);
    setPendingOverrides((prev) => {
      const next = { ...prev };
      for (const c of rejected) next[`${c.sign}:${c.proposed_reading}`] = null;
      return next;
    });
    setBulkBusy("reject");
    try { await onDelete(); }
    catch { /* ignore */ }
    finally { setBulkBusy(null); }
  };
  const allReviewed = staged.length === 0 && (approved.length + rejected.length) > 0;

  return (
    <div style={{ border: "1px solid #fed7aa", borderRadius: 8, background: "#fff",
                  marginTop: 6, overflow: "hidden" }}>

      {/* ── Header + bulk actions ── */}
      <div style={{
        padding: "10px 14px", background: "#fffbeb",
        borderBottom: "1px solid #fed7aa",
        display: "flex", justifyContent: "space-between",
        alignItems: "center", flexWrap: "wrap", gap: 8,
      }}>
        <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
          <span style={{ fontSize: 13, fontWeight: 700, color: "#92400e" }}>🔬 Anchor Review Queue</span>
          {staged.length > 0 && (
            <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 10,
              background: "#fef3c7", color: "#92400e", fontWeight: 600 }}>
              {staged.length} pending
            </span>
          )}
          {approved.length > 0 && (
            <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 10,
              background: "#dcfce7", color: "#15803d", fontWeight: 600 }}>
              ✓ {approved.length} approved
            </span>
          )}
          {rejected.length > 0 && (
            <span style={{ fontSize: 11, padding: "2px 8px", borderRadius: 10,
              background: "#fef2f2", color: "#dc2626", fontWeight: 600 }}>
              ✕ {rejected.length} rejected
            </span>
          )}
        </div>
        {approved.length > 0 && (
          <div style={{ display: "flex", flexDirection: "column", gap: 6, width: "100%" }}>
            <button
              disabled={verifySABusy || isBusy}
              onClick={() => void verifyAndArchive()}
              style={{
                padding: "6px 14px", fontSize: 11, fontWeight: 700,
                border: "1px solid #7c3aed", borderRadius: 5,
                background: verifySABusy ? "#ede9fe" : "#7c3aed",
                color: verifySABusy ? "#5b21b6" : "#fff",
                cursor: (verifySABusy || isBusy) ? "default" : "pointer",
                width: "100%",
              }}
              title="Mark approved candidates as verified and archive them">
              {verifySABusy ? "Archiving…" : `✓ Verify & Archive (${approved.length} approved)`}
            </button>
            {verifyResult && (
              <div style={{
                fontSize: 11, padding: "8px 10px", borderRadius: 5,
                background: verifyResult.ok ? "#f0fdf4" : "#fef2f2",
                border: `1px solid ${verifyResult.ok ? "#86efac" : "#fca5a5"}`,
                color: verifyResult.ok ? "#166534" : "#991b1b",
              }}>
                <div>{verifyResult.ok ? "✓" : "✗"} {verifyResult.message}</div>
                {verifyResult.ok && verifyResult.suggested_sa_exp && (
                  <div style={{ marginTop: 6 }}>
                    {saRunDone ? (
                      <span style={{
                        fontSize: 10, padding: "2px 8px", borderRadius: 4,
                        background: "#dcfce7", color: "#15803d", fontWeight: 600,
                      }}>✓ SA queued — check Jobs panel</span>
                    ) : (
                      <button
                        disabled={saRunBusy}
                        onClick={() => void runSaValidation(verifyResult.suggested_sa_exp!)}
                        style={{
                          padding: "3px 10px", fontSize: 10, fontWeight: 700,
                          border: "1px solid #7c3aed", borderRadius: 4,
                          background: saRunBusy ? "#ede9fe" : "#f5f3ff",
                          color: "#5b21b6",
                          cursor: saRunBusy ? "default" : "pointer",
                        }}
                        title={`Run ${verifyResult.suggested_sa_name ?? verifyResult.suggested_sa_exp} to verify SA impact`}>
                        {saRunBusy ? "Starting…" : `▶ Run SA Validation (${verifyResult.suggested_sa_name?.slice(0, 30) ?? verifyResult.suggested_sa_exp})`}
                      </button>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
        {staged.length > 0 && (
          <div style={{ display: "flex", gap: 6 }}>
            {staged.filter(c => c.recommended).length > 0 && (
              <button disabled={isBusy} onClick={() => void acceptRecommended()}
                style={{
                  padding: "4px 12px", fontSize: 11, fontWeight: 700,
                  border: "1px solid #7c3aed", borderRadius: 5,
                  background: bulkBusy === "approve" ? "#ede9fe" : "#7c3aed",
                  color: bulkBusy === "approve" ? "#5b21b6" : "#fff",
                  cursor: isBusy ? "default" : "pointer",
                }}>
                ★ Accept Recommended ({staged.filter(c => c.recommended).length})
              </button>
            )}
            <button disabled={isBusy} onClick={() => void approveAll()}
              style={{
                padding: "4px 12px", fontSize: 11, fontWeight: 700,
                border: "1px solid #16a34a", borderRadius: 5,
                background: bulkBusy === "approve" ? "#dcfce7" : "#16a34a",
                color: bulkBusy === "approve" ? "#15803d" : "#fff",
                cursor: isBusy ? "default" : "pointer",
              }}>
              {bulkBusy === "approve" ? "Approving…" : `✔ Approve All (${staged.length})`}
            </button>
            <button disabled={isBusy} onClick={() => void rejectRemaining()}
              title="Reject all remaining staged items (excludes already-approved)"
              style={{
                padding: "4px 12px", fontSize: 11, fontWeight: 700,
                border: "1px solid #dc2626", borderRadius: 5,
                background: bulkBusy === "reject" ? "#fef2f2" : "#dc2626",
                color: bulkBusy === "reject" ? "#dc2626" : "#fff",
                cursor: isBusy ? "default" : "pointer",
              }}>
              {bulkBusy === "reject" ? "Rejecting…" : `✕ Reject Remaining (${staged.length})`}
            </button>
          </div>
        )}
      </div>

      {/* ── Context banner ── */}
      <div style={{
        padding: "8px 14px", background: "#eff6ff",
        borderBottom: "1px solid #bfdbfe", fontSize: 11, color: "#1d4ed8",
        lineHeight: 1.6,
      }}>
        <strong>Approving</strong> pins a sign reading into the SA anchor table — it directly affects Structural Analysis experiment scores.
        {" "}★ <strong>Recommended</strong> candidates meet the statistical threshold (score ≥ 85% or SA Δ &gt; 5%) and are safe to accept in bulk.
        {" "}Candidates below threshold may still be accepted manually; they just haven&apos;t cleared the confidence bar yet.
      </div>

      {/* ── All-reviewed CTA ── */}
      {allReviewed && (
        <div style={{ margin: 10, padding: "12px 16px",
          background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 8 }}>
          <div style={{ display: "flex", alignItems: "flex-start", gap: 12, marginBottom: 10 }}>
            <span style={{ fontSize: 22 }}>✅</span>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 700, color: "#15803d", fontSize: 13, marginBottom: 2 }}>
                All {approved.length + rejected.length} candidates reviewed!
              </div>
              <div style={{ fontSize: 11, color: "#166534" }}>
                {approved.length > 0 && (
                  <>{approved.length} approved — click below to archive them and clean up the queue.<br /></>
                )}
                {rejected.length > 0 && (
                  <>{rejected.length} rejected will be permanently deleted (not archived).<br /></>
                )}
              </div>
            </div>
          </div>
          <button
            disabled={cleanupBusy || isBusy}
            onClick={() => void handleCleanup()}
            style={{
              width: "100%", padding: "8px 16px", fontSize: 12, fontWeight: 700,
              border: "1px solid #15803d", borderRadius: 6,
              background: cleanupBusy ? "#dcfce7" : "#15803d",
              color: cleanupBusy ? "#15803d" : "#fff",
              cursor: (cleanupBusy || isBusy) ? "default" : "pointer",
            }}>
            {cleanupBusy
              ? "Cleaning up…"
              : `✅ Archive ${approved.length} Approved & Delete ${rejected.length} Rejected`}
          </button>
          {cleanupResult && (
            <div style={{
              marginTop: 8, padding: "6px 10px", borderRadius: 5, fontSize: 11,
              background: cleanupResult.ok ? "#f0fdf4" : "#fef2f2",
              border: `1px solid ${cleanupResult.ok ? "#bbf7d0" : "#fca5a5"}`,
              color: cleanupResult.ok ? "#166534" : "#991b1b",
            }}>
              {cleanupResult.ok ? "✔" : "✕"} {cleanupResult.message}
            </div>
          )}
        </div>
      )}

      {/* ── Staged candidates ── */}
      {staged.length > 0 && staged.map((c) => {
        const key = `${c.sign}:${c.proposed_reading}`;
        const thisRowBusy = busyKey === key || bulkBusy !== null;
        const isRejecting  = rejectingKey === key;
        return (
          <div key={key} style={{
            borderBottom: "1px solid #fef3c7",
            background: isRejecting ? "#fef9c3" : "#fff",
          }}>
            <div style={{
              padding: "10px 14px",
              display: "grid",
              gridTemplateColumns: "58px 72px 1fr 46px 88px 80px",
              gap: 10, alignItems: "start",
            }}>
              <div>
                <div style={{ fontFamily: "monospace", fontWeight: 700, fontSize: 13,
                               color: "#111827" }}>{c.sign}</div>
                {(c.corpus_freq ?? 0) > 0 && (
                  <div style={{ fontSize: 9, color: "#9ca3af", marginTop: 2 }}>
                    freq {c.corpus_freq}
                  </div>
                )}
              </div>
              <div>
                <div style={{ fontWeight: 700, color: "#5b21b6", fontSize: 13 }}>
                  {c.proposed_reading}
                </div>
                {c.neighbor_reading && (
                  <div style={{ fontSize: 9, color: "#6b7280", marginTop: 2 }}>
                    nbr: {c.neighbor_reading}
                    {c.neighbor_count ? ` (×${c.neighbor_count})` : ""}
                  </div>
                )}
              </div>
              <div>
                {c.dedr_support && (
                  <div style={{ fontSize: 11, color: "#374151" }}>
                    ◆ DEDR: <em>{c.dedr_support}</em>
                  </div>
                )}
                <div style={{
                  fontSize: 10, color: "#6b7280", marginTop: 2,
                  display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center",
                }}>
                  <span style={{ padding: "1px 5px", borderRadius: 3,
                                  background: "#f3f4f6", fontWeight: 500 }}>
                    {c.evidence_type.replace(/_/g, " ")}
                  </span>
                  {c.source_experiment && (
                    <span style={{ color: "#9ca3af" }}>
                      via {c.source_experiment.slice(0, 22)}
                    </span>
                  )}
                  {c.recommended && (
                    <span style={{ padding: "1px 5px", borderRadius: 3, fontSize: 9,
                                    background: "#ede9fe", color: "#5b21b6",
                                    fontWeight: 700, letterSpacing: 0.3 }}>
                      ★ REC
                    </span>
                  )}
                </div>
                {c.conflict && (
                  <div style={{ fontSize: 10, color: "#dc2626", marginTop: 3,
                                 fontWeight: 600 }}>
                    ⚠ Conflict: {c.conflict}
                  </div>
                )}
              </div>
              <div style={{ textAlign: "right", paddingTop: 1 }}>
                <span style={{
                  fontSize: 12, fontWeight: 700,
                  color: c.evidence_score >= 0.8 ? "#15803d" :
                         c.evidence_score >= 0.5 ? "#b45309" : "#dc2626",
                }}>
                  {(c.evidence_score * 100).toFixed(0)}%
                </span>
                {c.sa_delta !== undefined && (
                  <div style={{ fontSize: 9, marginTop: 2, fontWeight: 600,
                                color: (c.sa_delta ?? 0) > 0 ? "#15803d" : "#9ca3af" }}>
                    SA Δ {(c.sa_delta ?? 0) > 0 ? "+" : ""}{((c.sa_delta ?? 0) * 100).toFixed(1)}%
                  </div>
                )}
              </div>
              <button
                disabled={thisRowBusy}
                onClick={() => void doOne(c.sign, c.proposed_reading, "approve")}
                title="Approve: add to anchor table"
                style={{
                  padding: "4px 8px", fontSize: 11, fontWeight: 700,
                  border: "1px solid #16a34a", borderRadius: 5,
                  background: "#dcfce7", color: "#15803d",
                  cursor: thisRowBusy ? "default" : "pointer", whiteSpace: "nowrap",
                }}>
                ✔ Approve
              </button>
              <button
                disabled={thisRowBusy}
                onClick={() => { setRejectingKey(key); setRejectReason(""); }}
                style={{
                  padding: "4px 8px", fontSize: 11, fontWeight: 700,
                  border: "1px solid #dc2626", borderRadius: 5,
                  background: isRejecting ? "#dc2626" : "#fef2f2",
                  color: isRejecting ? "#fff" : "#dc2626",
                  cursor: thisRowBusy ? "default" : "pointer",
                }}>
                ✕ Reject
              </button>
            </div>
            {isRejecting && (
              <div style={{
                padding: "8px 14px", background: "#fef9c3",
                borderTop: "1px solid #fcd34d",
                display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap",
              }}>
                <span style={{ fontSize: 11, color: "#78350f", fontWeight: 600, flexShrink: 0 }}>
                  Reject reason (optional):
                </span>
                <input
                  // eslint-disable-next-line jsx-a11y/no-autofocus
                  autoFocus
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter")  void doOne(c.sign, c.proposed_reading, "reject", rejectReason);
                    if (e.key === "Escape") { setRejectingKey(null); setRejectReason(""); }
                  }}
                  placeholder="e.g. conflicts with M42=kal, insufficient DEDR support"
                  style={{
                    flex: 1, minWidth: 180, padding: "4px 8px",
                    border: "1px solid #d1d5db", borderRadius: 4, fontSize: 11,
                  }}
                />
                <button
                  disabled={busyKey === key}
                  onClick={() => void doOne(c.sign, c.proposed_reading, "reject", rejectReason)}
                  style={{
                    padding: "4px 12px", fontSize: 11, fontWeight: 700,
                    border: "1px solid #dc2626", borderRadius: 4,
                    background: "#dc2626", color: "#fff", cursor: "pointer",
                  }}>
                  Confirm reject
                </button>
                <button
                  onClick={() => { setRejectingKey(null); setRejectReason(""); }}
                  style={{
                    padding: "4px 8px", fontSize: 11,
                    border: "1px solid #d1d5db", borderRadius: 4,
                    background: "#fff", cursor: "pointer",
                  }}>
                  Cancel
                </button>
              </div>
            )}
          </div>
        );
      })}

      {/* ── Approved section ── */}
      {approved.length > 0 && (
        <div style={{ borderTop: staged.length > 0 ? "2px solid #86efac" : undefined }}>
          <div style={{
            display: "flex", justifyContent: "space-between", alignItems: "center",
            background: "#f0fdf4", padding: "6px 14px",
          }}>
            <button
              onClick={() => setShowApproved((v) => !v)}
              style={{
                flex: 1, border: "none", background: "none",
                cursor: "pointer", textAlign: "left",
                fontSize: 11, fontWeight: 700, color: "#15803d", padding: 0,
              }}>
              ✔ {approved.length} approved reading{approved.length !== 1 ? "s" : ""}
              <span style={{ fontWeight: 400, marginLeft: 6 }}>{showApproved ? "▲" : "▼"}</span>
            </button>
            <button
              disabled={isBusy || approved.length === 0}
              onClick={() => void unstageAll()}
              title="Move all approved back to staging queue for re-review"
              style={{
                padding: "3px 10px", fontSize: 10, fontWeight: 600,
                border: "1px solid #d1d5db", borderRadius: 4,
                background: "#fff", color: "#6b7280",
                cursor: (isBusy || approved.length === 0) ? "default" : "pointer",
                whiteSpace: "nowrap",
              }}>
              ↩ Unstage All
            </button>
          </div>
          {showApproved && approved.map((c) => (
            <div key={`${c.sign}:${c.proposed_reading}`} style={{
              padding: "8px 14px", borderTop: "1px solid #bbf7d0",
              display: "flex", alignItems: "center", gap: 10, background: "#f0fdf4",
            }}>
              <span style={{ fontFamily: "monospace", fontWeight: 700, fontSize: 12,
                              width: 58, color: "#374151" }}>{c.sign}</span>
              <span style={{ fontWeight: 700, color: "#5b21b6", width: 68, fontSize: 12 }}>
                {c.proposed_reading}
              </span>
              <span style={{ flex: 1, fontSize: 11, color: "#374151" }}>
                {c.dedr_support
                  ? <>◆ DEDR: <em>{c.dedr_support}</em></>
                  : c.evidence_type.replace(/_/g, " ")}
                {c.conflict && (
                  <span style={{ marginLeft: 6, color: "#dc2626", fontWeight: 600 }}>
                    ⚠ {c.conflict}
                  </span>
                )}
              </span>
              <span style={{ fontSize: 11, fontWeight: 700, width: 36,
                              textAlign: "right",
                              color: c.evidence_score >= 0.8 ? "#15803d" : "#b45309" }}>
                {(c.evidence_score * 100).toFixed(0)}%
              </span>
              <button
                disabled={isBusy}
                onClick={() => void doOne(c.sign, c.proposed_reading, "staged")}
                title="Move back to staging queue for re-review"
                style={{
                  padding: "3px 9px", fontSize: 10, fontWeight: 600,
                  border: "1px solid #d1d5db", borderRadius: 4,
                  background: "#fff", color: "#6b7280",
                  cursor: isBusy ? "default" : "pointer",
                }}>
                ↩ Unstage
              </button>
            </div>
          ))}
        </div>
      )}

      {/* ── Rejected section ── */}
      {rejected.length > 0 && (
        <div style={{ borderTop: "1px solid #fecaca" }}>
          <div style={{
            display: "flex", justifyContent: "space-between", alignItems: "center",
            background: "#fff5f5", padding: "5px 14px",
          }}>
            <button
              onClick={() => setShowRejected((v) => !v)}
              style={{
                flex: 1, border: "none", background: "none",
                cursor: "pointer", textAlign: "left",
                fontSize: 11, fontWeight: 700, color: "#dc2626", padding: 0,
              }}>
              ✕ {rejected.length} rejected
              <span style={{ fontWeight: 400, marginLeft: 6 }}>{showRejected ? "▲" : "▼"}</span>
            </button>
            <button
              disabled={isBusy || rejected.length === 0}
              onClick={() => void restageAll()}
              title="Move all rejected back to staging queue"
              style={{
                padding: "3px 10px", fontSize: 10, fontWeight: 600,
                border: "1px solid #d1d5db", borderRadius: 4,
                background: "#fff", color: "#6b7280",
                cursor: (isBusy || rejected.length === 0) ? "default" : "pointer",
                whiteSpace: "nowrap",
              }}>
              ↩ Re-stage All
            </button>
            {!deleteConfirm ? (
              <button
                disabled={isBusy || rejected.length === 0}
                onClick={() => setdeleteConfirm(true)}
                title="Permanently delete all rejected candidates (cannot be undone)"
                style={{
                  padding: "3px 10px", fontSize: 10, fontWeight: 600,
                  border: "1px solid #dc2626", borderRadius: 4,
                  background: "#fef2f2", color: "#dc2626",
                  cursor: (isBusy || rejected.length === 0) ? "default" : "pointer",
                  whiteSpace: "nowrap", marginLeft: 6,
                }}>
                🗑 Delete {rejected.length}
              </button>
            ) : (
              <span style={{ display: "flex", gap: 4, alignItems: "center", marginLeft: 6 }}>
                <span style={{ fontSize: 10, color: "#dc2626", fontWeight: 600 }}>
                  Delete {rejected.length} rejected?
                </span>
                <button
                  onClick={() => void deleteRejected()}
                  style={{
                    padding: "3px 8px", fontSize: 10, fontWeight: 700,
                    border: "1px solid #dc2626", borderRadius: 4,
                    background: "#dc2626", color: "#fff", cursor: "pointer",
                  }}>Yes</button>
                <button
                  onClick={() => setdeleteConfirm(false)}
                  style={{
                    padding: "3px 8px", fontSize: 10,
                    border: "1px solid #d1d5db", borderRadius: 4,
                    background: "#fff", cursor: "pointer",
                  }}>No</button>
              </span>
            )}
          </div>
          {showRejected && rejected.map((c) => (
            <div key={`${c.sign}:${c.proposed_reading}`} style={{
              padding: "7px 14px", borderTop: "1px solid #fecaca",
              display: "flex", alignItems: "center", gap: 10, background: "#fff5f5",
            }}>
              <span style={{ fontFamily: "monospace", fontSize: 11, width: 58,
                              color: "#9ca3af", textDecoration: "line-through" }}>
                {c.sign}
              </span>
              <span style={{ color: "#9ca3af", width: 68, fontSize: 11,
                              textDecoration: "line-through" }}>
                {c.proposed_reading}
              </span>
              <span style={{ flex: 1, fontSize: 10, color: "#9ca3af" }}>
                {c.dedr_support || c.evidence_type.replace(/_/g, " ")}
              </span>
              <button
                disabled={isBusy}
                onClick={() => void doOne(c.sign, c.proposed_reading, "staged")}
                title="Move back to staging queue"
                style={{
                  padding: "2px 8px", fontSize: 10, fontWeight: 600,
                  border: "1px solid #d1d5db", borderRadius: 4,
                  background: "#fff", color: "#6b7280",
                  cursor: isBusy ? "default" : "pointer",
                }}>
                ↩ Re-stage
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Empty state */}
      {staged.length === 0 && approved.length === 0 && rejected.length === 0 && (
        <div style={{ padding: "14px", fontSize: 11, color: "#9ca3af", textAlign: "center" }}>
          No candidates in queue.
        </div>
      )}
    </div>
  );
}

// ── Promote to Anchors ────────────────────────────────────────────────────────

const PROMOTE_RESULT_KEY = "glossa_promote_result";

type PromoteResult = {
  ok: boolean;
  promoted: number;
  skipped: number;
  prev_coverage: number;
  new_coverage: number;
  coverage_delta: number;
  message: string;
  ts?: number;
};

function _loadPromoteResult(): PromoteResult | null {
  try {
    const raw = localStorage.getItem(PROMOTE_RESULT_KEY);
    if (!raw) return null;
    const r = JSON.parse(raw) as PromoteResult;
    // Expire after 2h
    if (r.ts && Date.now() - r.ts > 7_200_000) { localStorage.removeItem(PROMOTE_RESULT_KEY); return null; }
    return r;
  } catch { return null; }
}

function _clearPromoteResult() {
  try { localStorage.removeItem(PROMOTE_RESULT_KEY); } catch { /* ignore */ }
}

function PromoteToAnchors({
  promotable,
  archiveTotal,
  onPromoted,
}: {
  promotable: number;
  archiveTotal: number;
  onPromoted: () => void;
}) {
  const [busy, setBusy] = useState(false);
  const [confirm, setConfirm] = useState(false);
  const [result, setResult] = useState<PromoteResult | null>(() => {
    const stored = _loadPromoteResult();
    if (stored && promotable === 0 && archiveTotal === 0) {
      _clearPromoteResult();
      return null;
    }
    return stored;
  });

  const doPromote = async () => {
    setBusy(true);
    setConfirm(false);
    setResult(null);
    try {
      const res = await fetch(`${BASE}/staging/promote`, { method: "POST" });
      const data = await res.json() as PromoteResult & { ok: boolean; message: string };
      const withTs = { ...data, ts: Date.now() };
      setResult(withTs);
      if (data?.ok) {
        try { localStorage.setItem(PROMOTE_RESULT_KEY, JSON.stringify(withTs)); } catch { /* ignore */ }
        onPromoted();
      }
    } catch (e) {
      setResult({ ok: false, promoted: 0, skipped: 0,
        prev_coverage: 0, new_coverage: 0, coverage_delta: 0,
        message: e instanceof Error ? e.message : "Request failed" });
    } finally {
      setBusy(false);
    }
  };

  const navigate = (view: string) =>
    window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view } }));

  if (result?.ok && result.promoted > 0) {
    return (
      <div style={{
        border: "1px solid #a5f3fc", borderRadius: 8, background: "#ecfeff",
        padding: "12px 16px",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
          <span style={{ fontSize: 18 }}>📋</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 700, color: "#0e7490", fontSize: 13 }}>
              {result.promoted} sign{result.promoted !== 1 ? "s" : ""} promoted to INDUS_FINAL_ANCHORS
            </div>
            <div style={{ fontSize: 11, color: "#164e63", marginTop: 2 }}>
              Coverage: {(result.prev_coverage * 100).toFixed(1)}%
              {" "}<span style={{ color: "#15803d", fontWeight: 600 }}>
                → {(result.new_coverage * 100).toFixed(1)}%
                {result.coverage_delta > 0 &&
                  ` (+${(result.coverage_delta * 100).toFixed(1)}%)`}
              </span>
              {result.skipped > 0 && (
                <span style={{ color: "#6b7280", marginLeft: 8 }}>
                  · {result.skipped} skipped (already HIGH/MEDIUM)
                </span>
              )}
            </div>
            <div style={{ fontSize: 10, color: "#0891b2", marginTop: 3 }}>
              ✓ Signs index refreshed · Insights stale flag set · Foundation check marked dirty
            </div>
          </div>
        </div>
        <div style={{
          background: "#f0f9ff", border: "1px solid #bae6fd",
          borderRadius: 6, padding: "8px 12px", fontSize: 11,
        }}>
          <div style={{ fontWeight: 700, color: "#0369a1", marginBottom: 6 }}>
            🧩 What to do next:
          </div>
          <ol style={{ margin: 0, paddingLeft: 18, color: "#075985", lineHeight: 1.8 }}>
            <li>
              <button
                onClick={() => navigate("foundation-check")}
                style={{ background: "none", border: "none", color: "#0369a1", cursor: "pointer",
                  fontWeight: 600, fontSize: 11, padding: 0, textDecoration: "underline" }}
              >✅ Run Foundation Check
              </button>
              {" "}— verify the new LOW-confidence anchors don't conflict with existing HIGH/MEDIUM ones
            </li>
            <li>
              <button
                onClick={() => navigate("signs")}
                style={{ background: "none", border: "none", color: "#0369a1", cursor: "pointer",
                  fontWeight: 600, fontSize: 11, padding: 0, textDecoration: "underline" }}
              >🔤 Review Signs
              </button>
              {" "}— inspect the newly promoted signs, upgrade confident ones to MEDIUM via SA experiments
            </li>
            <li>
              <button
                onClick={() => {
                  window.dispatchEvent(new Event("glossa:regenerate-insight"));
                  navigate("dashboard");
                }}
                style={{ background: "none", border: "none", color: "#0369a1", cursor: "pointer",
                  fontWeight: 600, fontSize: 11, padding: 0, textDecoration: "underline" }}
              >🔄 Regenerate AI Insights
              </button>
              {" "}— the stale flag is set so new coverage will appear
            </li>
            <li>
              <button
                onClick={() => navigate("experiments")}
                style={{ background: "none", border: "none", color: "#0369a1", cursor: "pointer",
                  fontWeight: 600, fontSize: 11, padding: 0, textDecoration: "underline" }}
              >▶ Run SA Experiments
              </button>
              {" "}— validate promoted readings at the new coverage level
            </li>
          </ol>
        </div>
        <div style={{ marginTop: 10, display: "flex", justifyContent: "flex-end" }}>
          <button
            onClick={() => { _clearPromoteResult(); setResult(null); }}
            style={{
              padding: "4px 12px", fontSize: 10, fontWeight: 600,
              border: "1px solid #a5f3fc", borderRadius: 4,
              background: "#fff", color: "#0e7490", cursor: "pointer",
            }}
            title="Dismiss this notification"
          >
            ✓ Dismiss
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      border: "1px solid #bae6fd", borderRadius: 8, background: "#f0f9ff",
      padding: "10px 14px",
    }}>
      <div style={{ display: "flex", alignItems: "flex-start", gap: 12 }}>
        <span style={{ fontSize: 18 }}>📌</span>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 700, color: "#0369a1", fontSize: 12, marginBottom: 2 }}>
            {promotable} archive sign{promotable !== 1 ? "s" : ""} ready to promote to INDUS_FINAL_ANCHORS
          </div>
          <div style={{ fontSize: 10, color: "#075985", lineHeight: 1.5 }}>
            {archiveTotal} total in archive · {promotable} not yet in anchors file
            (HIGH/MEDIUM existing signs are never overwritten).
            Verified entries become MEDIUM confidence; approved-only become LOW.
            Coverage is recalculated after promotion.
          </div>
          {result && !result.ok && (
            <div style={{
              marginTop: 6, fontSize: 10, color: "#991b1b",
              background: "#fef2f2", border: "1px solid #fca5a5",
              borderRadius: 4, padding: "4px 8px",
            }}>
              ✗ {result.message}
            </div>
          )}
        </div>
        <div style={{ flexShrink: 0 }}>
          {!confirm ? (
            <button
              disabled={busy}
              onClick={() => setConfirm(true)}
              style={{
                padding: "6px 14px", fontSize: 11, fontWeight: 700,
                border: "1px solid #0369a1", borderRadius: 5,
                background: busy ? "#e0f2fe" : "#0369a1",
                color: busy ? "#0c4a6e" : "#fff",
                cursor: busy ? "default" : "pointer",
                whiteSpace: "nowrap",
              }}>
              {busy ? "Promoting…" : `🚀 Promote ${promotable} to Anchors`}
            </button>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 4, alignItems: "flex-end" }}>
              <span style={{ fontSize: 10, color: "#0c4a6e", fontWeight: 600 }}>
                Write {promotable} new anchors?
              </span>
              <div style={{ display: "flex", gap: 4 }}>
                <button
                  onClick={() => void doPromote()}
                  style={{
                    padding: "4px 10px", fontSize: 10, fontWeight: 700,
                    border: "1px solid #0369a1", borderRadius: 4,
                    background: "#0369a1", color: "#fff", cursor: "pointer",
                  }}>Confirm</button>
                <button
                  onClick={() => setConfirm(false)}
                  style={{
                    padding: "4px 10px", fontSize: 10,
                    border: "1px solid #d1d5db", borderRadius: 4,
                    background: "#fff", cursor: "pointer",
                  }}>Cancel</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
