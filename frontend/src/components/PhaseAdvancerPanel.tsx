/**
 * PhaseAdvancerPanel — research phase progress and one-click advancement.
 *
 * Shows: current phase badge, coverage progress bar, top recommended actions,
 * and an "Advance One Step" button that queues the top action as a job.
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
  gap_to_next: number;
  n_staged: number;
  n_rejected: number;
  n_approved: number;
  foundation_ok: boolean;
  anchors_total: number;
  anchors_hm: number;
  top_actions: PhaseAction[];
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
  const [loading, setLoading] = useState(false);
  const [advancing, setAdvancing] = useState(false);
  const [advanceResult, setAdvanceResult] = useState<{
    ok: boolean; message: string; job_id?: string | null;
  } | null>(null);
  const [expanded, setExpanded] = useState(false);

  const fetchStatus = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetch(`${BASE}/status`);
      if (res.ok) setStatus(await res.json() as PhaseStatus);
    } catch { /* backend may not be running */ }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { void fetchStatus(); }, [fetchStatus]);

  const advance = async () => {
    setAdvancing(true);
    setAdvanceResult(null);
    try {
      const res = await fetch(`${BASE}/advance`, { method: "POST",
        headers: { "Content-Type": "application/json" }, body: "{}" });
      if (res.ok) {
        const data = await res.json() as { ok: boolean; message: string; job_id?: string | null };
        setAdvanceResult(data);
        await fetchStatus();
      }
    } catch { /* ignore */ }
    finally { setAdvancing(false); }
  };

  if (!status && !loading) return null;
  if (loading && !status) {
    return <div style={{ padding: 12, fontSize: 12, color: "#9ca3af" }}>Loading phase status…</div>;
  }
  if (!status) return null;

  const colors = PHASE_COLORS[status.current_phase] || PHASE_COLORS[1];
  const pct = Math.round(status.coverage * 100);
  const milestonePct = Math.round(status.next_milestone * 100);
  const barWidth = Math.min(100, Math.round(
    (status.coverage / Math.max(0.01, status.next_milestone)) * 100
  ));

  return (
    <div style={{
      border: `1px solid ${colors.border}`,
      borderRadius: 8,
      background: colors.bg,
      margin: "12px 0",
      overflow: "hidden",
    }}>
      {/* Header */}
      <div
        onClick={() => setExpanded((v) => !v)}
        style={{
          display: "flex", justifyContent: "space-between", alignItems: "center",
          padding: "10px 14px", cursor: "pointer",
        }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{
            background: colors.text, color: "#fff",
            borderRadius: 4, padding: "2px 8px",
            fontSize: 10, fontWeight: 800, letterSpacing: 0.5,
          }}>
            PHASE {status.current_phase}
          </span>
          <span style={{ fontWeight: 700, color: colors.text, fontSize: 13 }}>
            {status.phase_label}
          </span>
          <span style={{ fontSize: 11, color: "#6b7280" }}>
            {pct}% coverage
            {status.current_phase < 5 && ` → ${milestonePct}% target`}
          </span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {!status.foundation_ok && (
            <span style={{ fontSize: 10, color: "#dc2626", fontWeight: 700 }}>⚠ foundation</span>
          )}
          <span style={{ fontSize: 11, color: "#9ca3af" }}>{expanded ? "▲" : "▼"}</span>
        </div>
      </div>

      {/* Progress bar */}
      <div style={{ padding: "0 14px 10px", background: "transparent" }}>
        <div style={{
          height: 6, background: "#e5e7eb", borderRadius: 3, overflow: "hidden",
        }}>
          <div style={{
            height: "100%", width: `${barWidth}%`,
            background: status.current_phase === 5 ? "#16a34a" : colors.text,
            borderRadius: 3, transition: "width 0.4s ease",
          }} />
        </div>
        <div style={{
          display: "flex", justifyContent: "space-between",
          fontSize: 9, color: "#9ca3af", marginTop: 3,
        }}>
          <span>{pct}%</span>
          {status.current_phase < 5 && <span>Next: {milestonePct}%</span>}
          {status.current_phase === 5 && <span style={{ color: "#16a34a", fontWeight: 700 }}>✓ Target reached</span>}
        </div>
      </div>

      {/* Expanded content */}
      {expanded && (
        <div style={{
          borderTop: `1px solid ${colors.border}`,
          padding: "10px 14px",
          background: "#fff",
        }}>
          {/* Phase description */}
          <p style={{ fontSize: 11, color: "#6b7280", margin: "0 0 10px", lineHeight: 1.5 }}>
            {status.phase_description}
          </p>

          {/* Stats row */}
          <div style={{ display: "flex", gap: 16, marginBottom: 10, flexWrap: "wrap" }}>
            {[
              { label: "H+M Anchors", value: status.anchors_hm },
              { label: "Staged", value: status.n_staged },
              { label: "Approved", value: status.n_approved },
              { label: "Rejected", value: status.n_rejected },
            ].map(({ label, value }) => (
              <div key={label} style={{ textAlign: "center" }}>
                <div style={{ fontSize: 16, fontWeight: 800, color: colors.text }}>{value}</div>
                <div style={{ fontSize: 9, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 0.5 }}>{label}</div>
              </div>
            ))}
          </div>

          {/* Top actions */}
          {status.top_actions.length > 0 && (
            <div style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#6b7280",
                             textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>
                Recommended Actions
              </div>
              {status.top_actions.map((action, i) => (
                <div key={i} style={{
                  padding: "6px 10px", marginBottom: 4,
                  background: i === 0 ? `${colors.bg}` : "#f9fafb",
                  border: `1px solid ${i === 0 ? colors.border : "#e5e7eb"}`,
                  borderRadius: 5,
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <span style={{ fontSize: 11, fontWeight: i === 0 ? 700 : 600,
                                    color: i === 0 ? colors.text : "#374151" }}>
                      {i === 0 && "⭐ "}{action.label}
                    </span>
                    <span style={{
                      fontSize: 9, color: "#9ca3af",
                      background: "#f3f4f6", borderRadius: 3, padding: "1px 5px", whiteSpace: "nowrap",
                    }}>
                      {action.action_type.replace(/_/g, " ")}
                    </span>
                  </div>
                  <div style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>
                    {action.rationale}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Advance button */}
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            <button
              disabled={advancing || status.top_actions.length === 0}
              onClick={() => void advance()}
              style={{
                padding: "7px 16px", fontSize: 12, fontWeight: 700,
                border: `1px solid ${colors.text}`,
                borderRadius: 6,
                background: advancing ? "#e5e7eb" : colors.text,
                color: advancing ? "#6b7280" : "#fff",
                cursor: (advancing || status.top_actions.length === 0) ? "default" : "pointer",
                whiteSpace: "nowrap",
              }}>
              {advancing ? "Advancing…" : "▶ Advance One Step"}
            </button>
            <button
              onClick={() => void fetchStatus()}
              disabled={loading}
              style={{
                padding: "7px 12px", fontSize: 11,
                border: "1px solid #d1d5db", borderRadius: 6,
                background: "#fff", cursor: loading ? "default" : "pointer",
                color: "#6b7280",
              }}>
              ↻ Refresh
            </button>
          </div>

          {/* Advance result */}
          {advanceResult && (
            <div style={{
              marginTop: 8, padding: "7px 10px", borderRadius: 5,
              background: advanceResult.ok ? "#f0fdf4" : "#fef2f2",
              border: `1px solid ${advanceResult.ok ? "#bbf7d0" : "#fecaca"}`,
              fontSize: 11,
              color: advanceResult.ok ? "#15803d" : "#dc2626",
            }}>
              {advanceResult.ok ? "✔" : "✕"} {advanceResult.message}
              {advanceResult.job_id && (
                <span style={{ marginLeft: 8, color: "#6b7280", fontFamily: "monospace", fontSize: 10 }}>
                  job: {advanceResult.job_id}
                </span>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
