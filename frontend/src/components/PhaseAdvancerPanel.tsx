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
};

export function PhaseAdvancerPanel() {
  const [status, setStatus] = useState<PhaseStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [advancing, setAdvancing] = useState(false);
  const [lastMessage, setLastMessage] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/status`);
      if (res.ok) setStatus(await res.json() as PhaseStatus);
    } catch { /* offline */ }
    finally { setLoading(false); }
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
                const doneCount = status.top_actions.length - status.remaining_actions;
                const isDone = i < doneCount;
                const isNext = i === doneCount;
                return (
                  <div key={i} data-testid={`phase-action-${i}`} style={{
                    padding: "6px 10px", marginBottom: 4, borderRadius: 5,
                    opacity: isDone ? 0.5 : 1,
                    background: isDone ? "#f0fdf4" : isNext ? colors.bg : "#f9fafb",
                    border: `1px solid ${isDone ? "#86efac" : isNext ? colors.border : "#e5e7eb"}`,
                  }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <span style={{
                        fontSize: 11, fontWeight: isNext ? 700 : 500,
                        color: isDone ? "#16a34a" : isNext ? colors.text : "#374151",
                        textDecoration: isDone ? "line-through" : "none",
                      }}>
                        {isDone ? "✓ " : isNext ? "▶ " : ""}{action.label}
                      </span>
                      <span style={{
                        fontSize: 9, fontWeight: 600, borderRadius: 3, padding: "1px 6px",
                        background: isDone ? "#dcfce7" : "#f3f4f6",
                        color: isDone ? "#15803d" : "#6b7280",
                      }}>
                        {isDone ? "done" : action.action_type.replace(/_/g, " ")}
                      </span>
                    </div>
                    {!isDone && <div style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>{action.rationale}</div>}
                  </div>
                );
              })}
            </div>
          )}

          {/* Advance button */}
          <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
            {status.all_done ? (
              <div data-testid="phase-all-done" style={{
                padding: "8px 16px", fontSize: 12, fontWeight: 700, borderRadius: 6,
                background: "#f0fdf4", border: "1px solid #86efac", color: "#15803d",
              }}>
                🏆 Phase {status.current_phase} complete
              </div>
            ) : (
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
                {advancing ? "⏳ Advancing…" : `▶ Advance (${status.remaining_actions} left)`}
              </button>
            )}
            <button
              data-testid="refresh-button"
              onClick={() => void refresh()}
              disabled={loading}
              style={{
                padding: "8px 12px", fontSize: 11, borderRadius: 6,
                border: "1px solid #d1d5db", background: "#fff",
                cursor: loading ? "default" : "pointer", color: "#6b7280",
              }}
            >
              ↻ Refresh
            </button>
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
