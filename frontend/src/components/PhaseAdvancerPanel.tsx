/**
 * PhaseAdvancerPanel — research phase progress and one-click advancement.
 *
 * Shows: current phase badge, coverage progress bar, top recommended actions,
 * and an "Advance One Step" button that queues the top action as a job.
 *
 * Action sequencing (all phases):
 *   run_experiment  → tracked via Jobs API polling (auto-advances when job created/done)
 *   regenerate_insights → tracked in completedSteps after user clicks Advance
 *   open_view       → tracked in completedSteps after user clicks Advance
 *   review_candidates / verify_sa → informational, tracked in completedSteps
 *
 * When ALL actions in the phase are done, PhaseHighlightsCard is shown.
 */

import { useCallback, useEffect, useRef, useState } from "react";

const BASE = "/api/v1/phase";
const JOBS_BASE = "/api/v1/jobs";
const DECIPHER_BASE = "/api/v1/dashboard/decipherment";

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
    action_type?: string | null;
  } | null>(null);
  const [expanded, setExpanded] = useState(true);
  // Experiment IDs that have been queued/started/completed — drives button advancement.
  // Populated from the Jobs API on mount and updated live by polling.
  const [queuedExpIds, setQueuedExpIds] = useState<Set<string>>(new Set());
  // Non-experiment steps (regenerate_insights, open_view, etc.) that have been
  // completed in this session — keyed by action label.
  const [completedSteps, setCompletedSteps] = useState<Set<string>>(new Set());
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);
  // Coverage when panel first mounted, for ‘before’ comparison in Phase Highlights.
  const coverageAtMountRef = useRef<number | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetch(`${BASE}/status`);
      if (res.ok) setStatus(await res.json() as PhaseStatus);
    } catch { /* backend may not be running */ }
    finally { setLoading(false); }
  }, []);

  /** Check the Jobs API for any experiment jobs that are already queued/running/done.
   *  Called on mount and every 8 s so the button auto-advances without user action. */
  const syncQueuedFromJobs = useCallback(async (watchExpIds: string[]) => {
    if (watchExpIds.length === 0) return;
    try {
      const res = await fetch(JOBS_BASE);
      if (!res.ok) return;
      const jobs = await res.json() as Array<{ params?: { exp_id?: string }; status?: string }>;
      const found = new Set<string>();
      for (const job of jobs) {
        const expId = job.params?.exp_id ?? "";
        if (watchExpIds.includes(expId) &&
            ["pending", "running", "completed"].includes(job.status ?? "")) {
          found.add(expId);
        }
      }
      if (found.size > 0) {
        setQueuedExpIds(prev => {
          const merged = new Set([...prev, ...found]);
          // Only trigger re-render if something actually changed
          if (merged.size === prev.size) return prev;
          return merged;
        });
      }
    } catch { /* jobs endpoint unavailable — silently skip */ }
  }, []);

  useEffect(() => { void fetchStatus(); }, [fetchStatus]);

  // Capture coverage on first status load
  useEffect(() => {
    if (status && coverageAtMountRef.current === null) {
      coverageAtMountRef.current = status.coverage;
    }
  }, [status]);

  // Once we have the phase status, start polling the Jobs API every 8 s.
  // This makes the button auto-advance as soon as a job is created or completes,
  // with no user interaction needed.
  useEffect(() => {
    if (!status) return;
    const expIds = status.top_actions
      .filter(a => a.action_type === "run_experiment")
      .map(a => a.params.experiment_id as string)
      .filter(Boolean);
    if (expIds.length === 0) return;
    // Sync immediately on mount (restores state after navigation/reload)
    void syncQueuedFromJobs(expIds);
    // Then poll every 8 s
    pollingRef.current = setInterval(() => void syncQueuedFromJobs(expIds), 8_000);
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [status?.top_actions, syncQueuedFromJobs]);

  const advance = async () => {
    setAdvancing(true);
    setAdvanceResult(null);
    try {
      const res = await fetch(`${BASE}/advance`, { method: "POST",
        headers: { "Content-Type": "application/json" }, body: "{}" });
      if (res.ok) {
      const data = await res.json() as {
          ok: boolean; message: string; job_id?: string | null;
          experiment_id?: string | null; action_type?: string | null;
        };
        // For regenerate_insights: navigate to dashboard + fire regeneration event
        if (data.ok && data.action_type === "regenerate_insights") {
          if (nextAction) setCompletedSteps(prev => new Set([...prev, nextAction.label]));
          window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "dashboard" } }));
          // Small delay so the dashboard mounts before the event fires
          setTimeout(() => {
            window.dispatchEvent(new CustomEvent("glossa:regenerate-insight"));
          }, 300);
          await fetchStatus();
        // For open_view / review_candidates / verify_sa: mark done and navigate if applicable
        } else if (data.ok && ["open_view", "review_candidates", "verify_sa"].includes(data.action_type ?? "")) {
          if (nextAction) setCompletedSteps(prev => new Set([...prev, nextAction.label]));
          if (data.action_type === "open_view") {
            const viewParam = (nextAction?.params?.view as string) || "signs";
            window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: viewParam } }));
          }
          await fetchStatus();
        } else {
          setAdvanceResult(data);
          // Mark this experiment as queued so button advances to next action
          if (data.ok && data.experiment_id) {
            setQueuedExpIds(prev => new Set([...prev, data.experiment_id!]));
          }
          await fetchStatus();
        }
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

  // Next action: first action not yet done (experiments not in queuedExpIds, others not in completedSteps)
  const nextAction = status.top_actions.find(a => {
    if (a.action_type === "run_experiment") {
      const expId = a.params.experiment_id as string | undefined;
      return !expId || !queuedExpIds.has(expId); // include if not yet queued
    }
    return !completedSteps.has(a.label); // include non-exp actions if not yet completed
  }) ?? null;

  const allExpQueued = status.top_actions
    .filter(a => a.action_type === "run_experiment")
    .every(a => queuedExpIds.has(a.params.experiment_id as string));

  // All actions in this phase complete (experiments queued + non-exp steps clicked through)
  const allDone = status.top_actions.length > 0 && status.top_actions.every(a => {
    if (a.action_type === "run_experiment") {
      return queuedExpIds.has(a.params.experiment_id as string);
    }
    return completedSteps.has(a.label);
  });

  return (
    <div style={{
      border: `2px solid ${colors.border}`,
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
          <span style={{ fontSize: 10, color: "#9ca3af", marginLeft: 4 }}>
            Guided autopilot
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
          {/* Purpose banner */}
          <div style={{
            padding: "6px 10px", marginBottom: 10,
            background: "#f0f9ff", border: "1px solid #bae6fd",
            borderRadius: 5, fontSize: 10, color: "#0369a1", lineHeight: 1.5,
          }}>
            <strong>🧭 Phase Guide</strong> queues SA &amp; validation <strong>experiments as background jobs</strong>.
            Check the <strong>Jobs panel</strong> to monitor progress.
            For paper mining, use the <strong>Research Loop</strong> below.
          </div>
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
              {status.top_actions.map((action, i) => {
                const isJob = action.action_type === "run_experiment";
                const isInfo = ["review_candidates","verify_sa","open_view"].includes(action.action_type);
                const isRegen = action.action_type === "regenerate_insights";
                const expId = action.params.experiment_id as string | undefined;
                const wasQueued = isJob && expId && queuedExpIds.has(expId);
                const isNext = !wasQueued && action === nextAction;
                const chipLabel = wasQueued ? "✔ queued" : isJob ? "⚙ queues job" : isRegen ? "✨ triggers regen" : isInfo ? "ℹ action needed" : action.action_type.replace(/_/g, " ");
                const chipBg   = wasQueued ? "#f0fdf4" : isJob ? "#dcfce7" : isRegen ? "#ede9fe" : isInfo ? "#fef3c7" : "#f3f4f6";
                const chipFg   = wasQueued ? "#15803d" : isJob ? "#15803d" : isRegen ? "#6d28d9" : isInfo ? "#92400e" : "#6b7280";
                return (
                  <div key={i} style={{
                    padding: "6px 10px", marginBottom: 4,
                    opacity: wasQueued ? 0.55 : 1,
                    background: isNext ? colors.bg : "#f9fafb",
                    border: `1px solid ${isNext ? colors.border : "#e5e7eb"}`,
                    borderRadius: 5,
                  }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                      <span style={{ fontSize: 11, fontWeight: isNext ? 700 : 600,
                                      color: isNext ? colors.text : "#374151",
                                      textDecoration: wasQueued ? "line-through" : "none" }}>
                        {isNext && "⭐ "}{action.label}
                      </span>
                      <span style={{
                        fontSize: 9, fontWeight: 600,
                        background: chipBg, color: chipFg,
                        borderRadius: 3, padding: "1px 6px", whiteSpace: "nowrap", marginLeft: 6,
                      }}>
                        {chipLabel}
                      </span>
                    </div>
                    <div style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>
                      {action.rationale}
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Advance button */}
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            {allDone ? (
              <div style={{
                padding: "7px 14px", fontSize: 12, fontWeight: 700,
                borderRadius: 6, background: "#f0fdf4",
                border: "1px solid #86efac", color: "#15803d",
              }}>
                ✅ All steps complete — see highlights below
              </div>
            ) : allExpQueued && !nextAction ? (
              // Experiments done but nothing else to advance (shouldn’t normally happen)
              <div style={{
                padding: "7px 14px", fontSize: 12, fontWeight: 700,
                borderRadius: 6, background: "#f0fdf4",
                border: "1px solid #86efac", color: "#15803d",
              }}>
                ✅ All experiments queued — check Jobs panel
              </div>
            ) : (
              <button
                disabled={advancing || !nextAction}
                onClick={() => void advance()}
                style={{
                  padding: "7px 16px", fontSize: 12, fontWeight: 700,
                  border: `1px solid ${colors.text}`,
                  borderRadius: 6,
                  background: advancing ? "#e5e7eb" : colors.text,
                  color: advancing ? "#6b7280" : "#fff",
                  cursor: (advancing || !nextAction) ? "default" : "pointer",
                  whiteSpace: "nowrap",
                }}>
                {advancing
                  ? "Advancing…"
                  : nextAction
                    ? `▶ ${nextAction.label.slice(0, 50)}`
                    : "▶ No actions planned"}
              </button>
            )}
            {!allDone && (
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
            )}
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

          {!allDone && (
            <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 8, textAlign: "center" }}>
              Or{" "}
              <span style={{ color: "#6b7280", textDecoration: "underline", cursor: "default" }}>
                use the Research Loop below for manual control
              </span>
            </div>
          )}
        </div>
      )}

      {/* Phase Highlights — shown when all actions in this phase are done */}
      {allDone && expanded && (
        <PhaseHighlightsCard
          phase={status.current_phase}
          phaseLabel={status.phase_label}
          coverage={status.coverage}
          coverageAtStart={coverageAtMountRef.current ?? status.coverage}
          anchorsHm={status.anchors_hm}
          colors={colors}
        />
      )}
    </div>
  );
}

// ── Phase Highlights Card ────────────────────────────────────────────────

interface DeciphermentSummary {
  corpus_token_coverage?: number;
  n_high?: number;
  n_medium?: number;
  n_low?: number;
  total_all?: number;
  sa_aggregate?: number;
}

function PhaseHighlightsCard({
  phase, phaseLabel, coverage, coverageAtStart, anchorsHm, colors,
}: {
  phase: number;
  phaseLabel: string;
  coverage: number;
  coverageAtStart: number;
  anchorsHm: number;
  colors: { bg: string; text: string; border: string };
}) {
  const [decipher, setDecipher] = useState<DeciphermentSummary | null>(null);

  // Load richer decipherment metrics once
  useEffect(() => {
    fetch(DECIPHER_BASE)
      .then(r => r.ok ? r.json() : null)
      .then(d => {
        if (!d) return;
        const a = d.anchors ?? {};
        setDecipher({
          corpus_token_coverage: a.corpus_token_coverage,
          n_high: a.n_high,
          n_medium: a.n_medium,
          n_low: a.n_low,
          total_all: a.total_all,
          sa_aggregate: d.sa_aggregate,
        });
      })
      .catch(() => {});
  }, []);

  const coverageDelta = coverage - coverageAtStart;
  const pct = Math.round(coverage * 100);
  const startPct = Math.round(coverageAtStart * 100);
  const deltaPct = Math.round(Math.abs(coverageDelta) * 100);
  const needleMoved = Math.abs(coverageDelta) >= 0.001;

  // Phase-specific "what remains" text for Indus decipherment project
  const remainsText: Record<number, string[]> = {
    1: [
      "Expand anchor set beyond initial candidates via more SA experiments",
      "Run Paper Mining Loop to find corroborating literature evidence",
      "Review and approve staged candidates",
    ],
    2: [
      "Validate anchor assignments with holdout data and negative controls",
      "Continue SA experiments to push coverage toward 60%",
      "Mine literature for disputed sign readings",
    ],
    3: [
      "Fill remaining coverage gaps using Structural Atlas and CGSA Cluster Analysis",
      "Continue Research Loop to find evidence for hard-to-decode signs",
    ],
    4: [
      "Final validation of all promoted signs via anchored SA experiments",
      "Regenerate AI insights to reflect 95%+ anchor set",
      "Spot-check and publish the decipherment anchor set",
    ],
    5: [
      `Upgrade ${(decipher?.n_low ?? 0)} LOW-confidence signs to MEDIUM via SA validation`,
      "Continue Paper Mining Loop to gather additional literature evidence",
      "Run contact-zone analysis to validate against Gulf site inscriptions",
      "Prepare final decipherment report and anchor set for publication",
    ],
  };
  const remains = remainsText[phase] ?? ["Continue research experiments"];

  // What was accomplished this phase
  const accomplishments: string[] = [];
  if (needleMoved && coverageDelta > 0) {
    accomplishments.push(`Coverage moved ${startPct}% → ${pct}% (+${deltaPct}%)`);
  } else if (pct >= 95) {
    accomplishments.push(`Coverage target reached: ${pct}% corpus token coverage`);
  }
  accomplishments.push(`${anchorsHm} HIGH + MEDIUM confidence anchors validated`);
  if (decipher?.sa_aggregate && decipher.sa_aggregate > 0) {
    accomplishments.push(`SA aggregate confidence: ${Math.round(decipher.sa_aggregate * 100)}%`);
  }
  if (decipher?.n_low && decipher.n_low > 0) {
    accomplishments.push(`${decipher.n_low} LOW-confidence signs staged for future validation`);
  }

  const isLastPhase = phase >= 5;

  return (
    <div style={{
      borderTop: `2px solid ${colors.border}`,
      background: "#fff",
      padding: "14px 16px",
    }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
        <span style={{
          fontSize: 22, lineHeight: 1,
        }}>
          {isLastPhase ? "🏆" : "✅"}
        </span>
        <div>
          <div style={{ fontWeight: 800, fontSize: 14, color: colors.text }}>
            Phase {phase} {phaseLabel} — Complete
          </div>
          <div style={{ fontSize: 11, color: "#6b7280", marginTop: 1 }}>
            {isLastPhase
              ? "Decipherment target reached. All validation steps done."
              : `All Phase ${phase} actions done. Ready to advance.`}
          </div>
        </div>
      </div>

      {/* Coverage progress bar — big visual */}
      <div style={{ marginBottom: 12 }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, color: "#6b7280", marginBottom: 3 }}>
          <span>Corpus token coverage</span>
          <span style={{ fontWeight: 700, color: pct >= 95 ? "#16a34a" : colors.text }}>{pct}%</span>
        </div>
        <div style={{ height: 10, background: "#e5e7eb", borderRadius: 5, overflow: "hidden" }}>
          <div style={{
            height: "100%", width: `${Math.min(100, pct)}%`,
            background: pct >= 95 ? "#16a34a" : colors.text,
            borderRadius: 5, transition: "width 0.5s ease",
          }} />
        </div>
        {needleMoved && (
          <div style={{ fontSize: 10, marginTop: 3, color: coverageDelta > 0 ? "#15803d" : "#dc2626", fontWeight: 600 }}>
            {coverageDelta > 0 ? "⬆" : "⬇"} {coverageDelta > 0 ? "+" : ""}{deltaPct}% this phase
            <span style={{ fontWeight: 400, color: "#9ca3af", marginLeft: 4 }}>(was {startPct}%)</span>
          </div>
        )}
      </div>

      {/* Accomplished */}
      <div style={{ marginBottom: 12 }}>
        <div style={{ fontSize: 10, fontWeight: 700, color: "#374151",
          textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 5 }}>
          ✨ Accomplished this phase
        </div>
        <ul style={{ margin: 0, paddingLeft: 16, display: "flex", flexDirection: "column", gap: 4 }}>
          {accomplishments.map((a, i) => (
            <li key={i} style={{ fontSize: 11, color: "#374151", lineHeight: 1.5 }}>{a}</li>
          ))}
        </ul>
      </div>

      {/* What remains */}
      <div style={{ marginBottom: 12 }}>
        <div style={{ fontSize: 10, fontWeight: 700, color: "#374151",
          textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 5 }}>
          🔭 What remains (Indus decipherment)
        </div>
        <ul style={{ margin: 0, paddingLeft: 16, display: "flex", flexDirection: "column", gap: 4 }}>
          {remains.map((r, i) => (
            <li key={i} style={{ fontSize: 11, color: "#6b7280", lineHeight: 1.5 }}>{r}</li>
          ))}
        </ul>
      </div>

      {/* CTA */}
      {isLastPhase ? (
        <div style={{
          padding: "10px 14px", background: "#f0fdf4", border: "1px solid #86efac",
          borderRadius: 8, fontSize: 11, color: "#166534", lineHeight: 1.6,
        }}>
          <strong>🏁 Decipherment target complete.</strong>{" "}
          The anchor set is validated at {pct}% corpus coverage with {anchorsHm} H+M confidence signs.
          Continue with the Research Loop for literature mining, or export the anchor set for publication.
          The Phase Guide will reactivate if coverage drops below 95% (e.g. after a corpus expansion).
        </div>
      ) : (
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <div style={{
            padding: "7px 14px", fontSize: 11, fontWeight: 600,
            background: colors.bg, border: `1px solid ${colors.border}`,
            color: colors.text, borderRadius: 6,
          }}>
            ▶ Next: Phase {phase + 1} — click Advance above to continue
          </div>
        </div>
      )}
    </div>
  );
}
