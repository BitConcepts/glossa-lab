/**
 * PhaseAdvancerPanel — simple, backend-driven phase advancement.
 *
 * The backend is the single source of truth:
 *   GET  /phase/status  → current phase, actions, remaining count, all_done flag
 *   POST /phase/advance → execute next uncompleted action, returns result
 *
 * No client-side state tracking. No polling. Just fetch → render → advance → refresh.
 */

import { useCallback, useEffect, useState } from "react";

const BASE = "/api/v1/phase";

interface PhaseAction {
  action_type: string;
  label: string;
  rationale: string;
  params: Record<string, unknown>;
  priority: number;
  db_status: "pending" | "completed" | "failed" | "skipped" | "running";
  job_id?: string | null;
  error_message?: string;
  completed_at?: string | null;
}

interface PhaseStatus {
  current_phase: number;
  phase_label: string;
  phase_description: string;
  coverage: number;
  next_milestone: number;
  anchors_hm: number;
  anchors_total: number;
  foundation_ok: boolean;
  top_actions: PhaseAction[];
  remaining_actions: number;
  all_done: boolean;
}

interface AdvanceResult {
  ok: boolean;
  action_taken: string;
  action_type: string;
  job_id?: string | null;
  experiment_id?: string | null;
  message: string;
}

const PHASE_COLORS: Record<number, { bg: string; text: string; border: string }> = {
  1: { bg: "#f0f9ff", text: "#0369a1", border: "#bae6fd" },
  2: { bg: "#f0fdf4", text: "#15803d", border: "#bbf7d0" },
  3: { bg: "#fefce8", text: "#854d0e", border: "#fde68a" },
  4: { bg: "#fff7ed", text: "#9a3412", border: "#fed7aa" },
  5: { bg: "#f0fdf4", text: "#166534", border: "#86efac" },
  6: { bg: "#ede9fe", text: "#5b21b6", border: "#c4b5fd" },
  7: { bg: "#fef3c7", text: "#92400e", border: "#fcd34d" },
};

const STATUS_BADGE: Record<string, { bg: string; fg: string; label: string }> = {
  pending:   { bg: "#f3f4f6", fg: "#6b7280", label: "pending" },
  completed: { bg: "#dcfce7", fg: "#15803d", label: "done" },
  failed:    { bg: "#fef2f2", fg: "#dc2626", label: "failed" },
  skipped:   { bg: "#fef3c7", fg: "#92400e", label: "skipped" },
  running:   { bg: "#dbeafe", fg: "#1d4ed8", label: "running" },
};

/** Dispatch event to start the Research Loop from any panel. */
function dispatchStartLoop(cycles = 15) {
  window.dispatchEvent(
    new CustomEvent("glossa:start-research-loop", { detail: { cycles } })
  );
}

/** True when the action is a phase-recommended experiment (runs via loop). */
function isLoopAction(action: PhaseAction) {
  return action.action_type === "run_experiment";
}

export function PhaseAdvancerPanel() {
  const [status, setStatus] = useState<PhaseStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [advancing, setAdvancing] = useState(false);
  const [actionBusy, setActionBusy] = useState<string | null>(null);
  const [lastMessage, setLastMessage] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(true);
  const [refreshedAt, setRefreshedAt] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setRefreshedAt(null);
    try {
      const res = await fetch(`${BASE}/status`);
      if (res.ok) {
        setStatus(await res.json() as PhaseStatus);
        setRefreshedAt(new Date().toLocaleTimeString());
      } else {
        setLastMessage(`Refresh failed (${res.status})`);
      }
    } catch {
      setLastMessage("Refresh failed — backend offline?");
    } finally { setLoading(false); }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  const advance = async () => {
    setAdvancing(true);
    setLastMessage(null);
    try {
      const res = await fetch(`${BASE}/advance`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "{}",
      });
      if (res.ok) {
        const data = await res.json() as AdvanceResult;
        setLastMessage(data.message);
      } else {
        setLastMessage("Failed — check server logs.");
      }
    } catch {
      setLastMessage("Network error.");
    } finally {
      setAdvancing(false);
      await refresh();
    }
  };

  if (loading && !status) {
    return <div style={{ padding: 12, fontSize: 12, color: "#9ca3af" }}>Loading phase…</div>;
  }
  if (!status) return null;

  const colors = PHASE_COLORS[status.current_phase] ?? PHASE_COLORS[1];
  const pct = Math.round(status.coverage * 100);

  return (
    <div style={{
      border: `2px solid ${colors.border}`, borderRadius: 8,
      background: colors.bg, margin: "12px 0", overflow: "hidden",
    }}>
      {/* Header */}
      <div
        onClick={() => setExpanded(v => !v)}
        style={{
          display: "flex", justifyContent: "space-between", alignItems: "center",
          padding: "10px 14px", cursor: "pointer",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{
            background: colors.text, color: "#fff", borderRadius: 4,
            padding: "2px 8px", fontSize: 10, fontWeight: 800, letterSpacing: 0.5,
          }}>
            PHASE {status.current_phase}
          </span>
          <span style={{ fontWeight: 700, color: colors.text, fontSize: 13 }}>
            {status.phase_label}
          </span>
          <span style={{ fontSize: 11, color: "#6b7280" }}>
            {pct}% coverage
          </span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {status.all_done && (
            <span data-testid="phase-complete-badge" style={{ fontSize: 11, color: "#16a34a", fontWeight: 700 }}>✅ Complete</span>
          )}
          <span style={{ fontSize: 11, color: "#9ca3af" }}>{expanded ? "▲" : "▼"}</span>
        </div>
      </div>

      {/* Progress bar */}
      <div style={{ padding: "0 14px 10px" }}>
        <div style={{ height: 6, background: "#e5e7eb", borderRadius: 3, overflow: "hidden" }}>
          <div style={{
            height: "100%", width: `${Math.min(100, pct)}%`,
            background: pct >= 95 ? "#16a34a" : colors.text,
            borderRadius: 3, transition: "width 0.4s ease",
          }} />
        </div>
      </div>

      {expanded && (
        <div style={{ borderTop: `1px solid ${colors.border}`, padding: "12px 14px", background: "#fff" }}>
          {/* Action list */}
          {status.top_actions.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#6b7280", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>
                Phase Actions ({status.remaining_actions} remaining)
              </div>
              {status.top_actions.map((action, i) => {
                const st = action.db_status || "pending";
                const badge = STATUS_BADGE[st] || STATUS_BADGE.pending;
                const isDone = st === "completed";
                const isFailed = st === "failed";
                const isSkipped = st === "skipped";
                const isRunning = st === "running";
                const isPending = st === "pending";
                const isActionBusy = actionBusy === action.label;
                const isLoop = isLoopAction(action);

                return (
                  <div key={i} data-testid={`phase-action-${i}`} style={{
                    padding: "6px 10px", marginBottom: 4, borderRadius: 5,
                    opacity: isSkipped ? 0.4 : 1,
                    background: isDone ? "#f0fdf4" : isFailed ? "#fef2f2"
                      : isRunning ? "#eff6ff"
                      : isLoop && isPending ? "#f5f3ff"
                      : isPending ? "#f9fafb" : "#fefce8",
                    border: `1px solid ${isDone ? "#86efac" : isFailed ? "#fca5a5"
                      : isRunning ? "#bfdbfe"
                      : isLoop && isPending ? "#ddd6fe"
                      : isSkipped ? "#fde68a" : "#e5e7eb"}`,
                  }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 6 }}>
                      <span style={{
                        fontSize: 11, fontWeight: isPending ? 600 : 500, flex: 1,
                        color: isDone ? "#16a34a" : isFailed ? "#dc2626"
                          : isRunning ? "#1d4ed8"
                          : isSkipped ? "#92400e"
                          : isLoop && isPending ? "#6d28d9"
                          : "#374151",
                        textDecoration: isSkipped ? "line-through" : "none",
                      }}>
                        {isDone ? "✓ " : isFailed ? "✗ " : isRunning ? "⏳ "
                          : isLoop && isPending ? "🔬 "
                          : isPending ? "▸ " : "⊘ "}
                        {action.label}
                      </span>

                      {/* Loop badge for pending run_experiment actions */}
                      {isLoop && isPending && (
                        <span style={{
                          fontSize: 9, fontWeight: 700, borderRadius: 3, padding: "1px 7px",
                          background: "#ede9fe", color: "#5b21b6", whiteSpace: "nowrap",
                        }}>🔄 in Research Loop</span>
                      )}

                      {/* Status badge for non-loop or non-pending */}
                      {(!isLoop || !isPending) && (
                        <span style={{
                          fontSize: 9, fontWeight: 600, borderRadius: 3, padding: "1px 6px",
                          background: badge.bg, color: badge.fg,
                        }}>
                          {badge.label}
                        </span>
                      )}

                      {/* Skip — not shown for loop experiments (loop handles them) */}
                      {!isLoop && (isPending || isFailed) && (
                        <button
                          disabled={isActionBusy}
                          onClick={async () => {
                            setActionBusy(action.label);
                            try {
                              await fetch(`${BASE}/actions/${encodeURIComponent(action.label)}/skip`, {
                                method: "POST", headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({ phase: status.current_phase }),
                              });
                            } finally { setActionBusy(null); await refresh(); }
                          }}
                          style={{ fontSize: 9, padding: "1px 6px", borderRadius: 3,
                            border: "1px solid #d1d5db", background: "#fff", color: "#6b7280",
                            cursor: "pointer" }}
                          title="Skip this action"
                        >skip</button>
                      )}

                      {/* Skip still available for failed loop experiments */}
                      {isLoop && isFailed && (
                        <button
                          disabled={isActionBusy}
                          onClick={async () => {
                            setActionBusy(action.label);
                            try {
                              await fetch(`${BASE}/actions/${encodeURIComponent(action.label)}/skip`, {
                                method: "POST", headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({ phase: status.current_phase }),
                              });
                            } finally { setActionBusy(null); await refresh(); }
                          }}
                          style={{ fontSize: 9, padding: "1px 6px", borderRadius: 3,
                            border: "1px solid #d1d5db", background: "#fff", color: "#6b7280",
                            cursor: "pointer" }}
                          title="Skip this failed experiment"
                        >skip</button>
                      )}

                      {/* Redo for completed/skipped */}
                      {(isDone || isSkipped) && (
                        <button
                          disabled={isActionBusy}
                          onClick={async () => {
                            setActionBusy(action.label);
                            try {
                              await fetch(`${BASE}/actions/${encodeURIComponent(action.label)}/redo`, {
                                method: "POST", headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({ phase: status.current_phase }),
                              });
                            } finally { setActionBusy(null); await refresh(); }
                          }}
                          style={{ fontSize: 9, padding: "1px 6px", borderRadius: 3,
                            border: "1px solid #c4b5fd", background: "#f5f3ff", color: "#5b21b6",
                            cursor: "pointer" }}
                          title="Redo this action"
                        >redo</button>
                      )}
                    </div>

                    {isFailed && action.error_message && (
                      <div style={{ fontSize: 10, color: "#dc2626", marginTop: 2, fontFamily: "monospace" }}>
                        {action.error_message}
                      </div>
                    )}

                    {/* Rationale — loop experiments show "runs with Research Loop" */}
                    {isPending && isLoop && (
                      <div style={{ fontSize: 10, color: "#6d28d9", marginTop: 2 }}>
                        Queued automatically when you start the Research Loop below.
                      </div>
                    )}
                    {isPending && !isLoop && (
                      <div style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>{action.rationale}</div>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* Advance buttons */}
          {(() => {
            // Determine what kind of remaining actions we have
            const pendingLoopActions = status.top_actions.filter(
              a => isLoopAction(a) && (a.db_status === "pending" || !a.db_status)
            );
            const pendingNonLoopActions = status.top_actions.filter(
              a => !isLoopAction(a) && a.action_type !== "complete_phase"
                && (a.db_status === "pending" || !a.db_status)
            );
            const allRemainingAreLoopActions =
              status.remaining_actions > 0 &&
              pendingLoopActions.length === status.remaining_actions;

            return (
              <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
                {status.all_done ? (
                  <div data-testid="phase-all-done" style={{
                    padding: "8px 16px", fontSize: 12, fontWeight: 700, borderRadius: 6,
                    background: "#f0fdf4", border: "1px solid #86efac", color: "#15803d",
                  }}>
                    🏆 Phase {status.current_phase} complete
                  </div>
                ) : allRemainingAreLoopActions ? (
                  // All remaining actions are loop experiments — show Run Loop CTA
                  <button
                    data-testid="run-loop-button"
                    disabled={advancing}
                    onClick={() => dispatchStartLoop(15)}
                    style={{
                      padding: "8px 18px", fontSize: 12, fontWeight: 700, borderRadius: 6,
                      border: "none", cursor: advancing ? "default" : "pointer",
                      background: "#7c3aed", color: "#fff",
                    }}
                    title="Start the Research Loop — phase experiments queue automatically"
                  >
                    🔄 Run Research Loop
                  </button>
                ) : pendingNonLoopActions.length > 0 ? (<>
                  <button
                    data-testid="advance-button"
                    disabled={advancing}
                    onClick={() => void advance()}
                    style={{
                      padding: "8px 18px", fontSize: 12, fontWeight: 700, borderRadius: 6,
                      border: "none", cursor: advancing ? "default" : "pointer",
                      background: advancing ? "#e5e7eb" : colors.text,
                      color: advancing ? "#6b7280" : "#fff",
                    }}
                  >
                    {advancing ? "⏳ Advancing…" : `▶ Next (${status.remaining_actions} left)`}
                  </button>
                  {pendingLoopActions.length > 0 && (
                    <button
                      data-testid="run-loop-button"
                      onClick={() => dispatchStartLoop(15)}
                      style={{
                        padding: "8px 14px", fontSize: 11, fontWeight: 700, borderRadius: 6,
                        border: "1px solid #7c3aed", cursor: "pointer",
                        background: "#fff", color: "#7c3aed",
                      }}
                      title="Also queue phase experiments via the Research Loop"
                    >
                      🔄 + Run Loop
                    </button>
                  )}
                </>) : (
                  // Only complete_phase remaining (or nothing actionable manually)
                  <button
                    data-testid="advance-button"
                    disabled={advancing}
                    onClick={() => void advance()}
                    style={{
                      padding: "8px 18px", fontSize: 12, fontWeight: 700, borderRadius: 6,
                      border: "none", cursor: advancing ? "default" : "pointer",
                      background: advancing ? "#e5e7eb" : colors.text,
                      color: advancing ? "#6b7280" : "#fff",
                    }}
                  >
                    {advancing ? "⏳ Advancing…" : `▶ Next (${status.remaining_actions} left)`}
                  </button>
                )}
              </div>
            );
          })()}

          {/* Refresh row */}
          <div style={{ display: "flex", gap: 8, alignItems: "center", marginTop: 8 }}>
            <button
              data-testid="refresh-button"
              onClick={() => void refresh()}
              disabled={loading}
              style={{
                padding: "6px 12px", fontSize: 11, borderRadius: 6,
                border: "1px solid #d1d5db", background: loading ? "#f3f4f6" : "#fff",
                cursor: loading ? "default" : "pointer", color: "#6b7280",
              }}
            >
              {loading ? "⏳ Refreshing…" : "↻ Refresh"}
            </button>
            {refreshedAt && !loading && (
              <span style={{ fontSize: 10, color: "#9ca3af" }}>Updated {refreshedAt}</span>
            )}
          </div>

          {lastMessage && (
            <div data-testid="advance-message" style={{
              marginTop: 8, padding: "6px 10px", borderRadius: 5, fontSize: 11,
              background: "#f0f9ff", border: "1px solid #bae6fd", color: "#0369a1",
            }}>
              {lastMessage}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
