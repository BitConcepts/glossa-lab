/**
 * FoundationCheckView — Research integrity and citation audit panel.
 *
 * Calls GET /api/v1/research/foundation-check and displays:
 *   ✓ pass   — check passed
 *   ✗ fail   — check failed (red, blocks external communication)
 *   ⚠ warn  — known limitation or caveat
 *
 * Each check with an action_type gets a "Fix" button that dispatches the
 * appropriate action (run_script, run_experiment, open_view, etc.).
 *
 * Pre-communication requirement (AGENTS.md H20):
 *   Run this check before sending anything to Dr. Fuls or any external party.
 */

import { useCallback, useEffect, useState } from "react";
import { useToast } from "../hooks/useToast";

interface Check {
  label:        string;
  status:       "pass" | "fail" | "warn";
  detail:       string;
  action_type:  string;
  action_label: string;
  action_params: Record<string, string>;
  citations:    string[];
}

interface CheckSummary {
  n_pass:          number;
  n_fail:          number;
  n_warn:          number;
  overall_status:  string;
  send_to_fuls_ok: boolean;
  send_to_fuls_msg: string;
}

interface FoundationCheckResult {
  timestamp: string;
  checks:    Check[];
  summary:   CheckSummary;
  citations: string[];
}

const STATUS_COLORS: Record<string, string> = {
  pass: "#16a34a",
  fail: "#dc2626",
  warn: "#d97706",
};
const STATUS_ICONS: Record<string, string> = {
  pass: "✓",
  fail: "✗",
  warn: "⚠",
};
const STATUS_BG: Record<string, string> = {
  pass: "#f0fdf4",
  fail: "#fef2f2",
  warn: "#fffbeb",
};

function navigate(view: string) {
  window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view } }));
}

export function FoundationCheckView() {
  const { toast } = useToast();
  const [result, setResult]   = useState<FoundationCheckResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState<Record<string, boolean>>({});

  const runCheck = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/v1/research/foundation-check");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: FoundationCheckResult = await res.json();
      setResult(data);
    } catch (e) {
      toast(e instanceof Error ? e.message : "Foundation check failed", "error");
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => { void runCheck(); }, [runCheck]);

  const handleFix = async (check: Check) => {
    const key = check.label;
    setRunning((r) => ({ ...r, [key]: true }));
    try {
      if (check.action_type === "run_script") {
        const script = check.action_params.script ?? "";
        toast(`Running ${script} …`, "info");
        // POST to terminal execute
        const res = await fetch("/api/v1/terminal/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ command: `shell.cmd python ${script}`, use_venv: true }),
        });
        if (res.ok) {
          toast(`Script started. Re-running check in 5s …`, "success");
          setTimeout(() => void runCheck(), 5000);
        }
      } else if (check.action_type === "run_experiment") {
        const expId = check.action_params.experiment_id ?? "";
        toast(`Launching experiment ${expId} …`, "info");
        const res = await fetch(`/api/v1/experiment-graphs/${expId}/run`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ kwargs: {} }),
        });
        if (res.ok) toast(`Experiment queued`, "success");
      } else if (check.action_type === "open_view") {
        navigate("settings");
      }
    } catch (e) {
      toast(e instanceof Error ? e.message : "Action failed", "error");
    } finally {
      setRunning((r) => ({ ...r, [key]: false }));
    }
  };

  const summary = result?.summary;

  return (
    <div style={{ maxWidth: 1000, margin: "0 auto" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "flex-end", gap: 12, marginBottom: 20 }}>
        <div style={{ flex: 1 }}>
          <h2 style={{ margin: 0, fontSize: 22, color: "#111827" }}>
            🔬 Foundation Check
          </h2>
          <p style={{ margin: "4px 0 0", fontSize: 13, color: "#6b7280" }}>
            Research integrity audit. Run before any external communication (Fuls, Parpola, prize submission).
            Checks corpora, anchors, citations, and all verified results.
          </p>
        </div>
        <button
          onClick={() => void runCheck()}
          disabled={loading}
          style={{
            padding: "8px 18px", border: "1px solid #2563eb", borderRadius: 6,
            background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600,
            cursor: loading ? "wait" : "pointer", opacity: loading ? 0.7 : 1,
          }}
        >
          {loading ? "Running…" : "↻ Re-run"}
        </button>
      </div>

      {/* Summary banner */}
      {summary && (
        <div style={{
          padding: "12px 16px", borderRadius: 8, marginBottom: 20,
          background: summary.overall_status === "PASS" ? "#f0fdf4" : "#fef2f2",
          border: `1px solid ${summary.overall_status === "PASS" ? "#86efac" : "#fca5a5"}`,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{
              fontSize: 20,
              color: summary.overall_status === "PASS" ? "#16a34a" : "#dc2626",
            }}>
              {summary.overall_status === "PASS" ? "✓" : "✗"}
            </span>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 700, fontSize: 14,
                color: summary.overall_status === "PASS" ? "#15803d" : "#b91c1c" }}>
                {summary.overall_status === "PASS"
                  ? `All checks passed (${summary.n_pass} pass, ${summary.n_warn} warn)`
                  : `${summary.n_fail} check(s) failed — resolve before external communication`}
              </div>
              <div style={{ fontSize: 12, color: "#374151", marginTop: 2 }}>
                {summary.send_to_fuls_msg}
              </div>
            </div>
            <div style={{ textAlign: "right", fontSize: 11, color: "#6b7280" }}>
              <div>✓ {summary.n_pass} pass</div>
              <div style={{ color: "#dc2626" }}>✗ {summary.n_fail} fail</div>
              <div style={{ color: "#d97706" }}>⚠ {summary.n_warn} warn</div>
            </div>
          </div>
        </div>
      )}

      {/* Timestamp */}
      {result && (
        <div style={{ fontSize: 11, color: "#9ca3af", marginBottom: 12 }}>
          Last run: {new Date(result.timestamp).toLocaleString()} ·
          Sources: {result.citations.join(", ")}
        </div>
      )}

      {/* Checks list */}
      {result && (
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {result.checks.map((check) => (
            <div
              key={check.label}
              style={{
                padding: "10px 14px",
                borderRadius: 8,
                border: `1px solid ${STATUS_COLORS[check.status]}44`,
                background: STATUS_BG[check.status],
                display: "flex",
                alignItems: "flex-start",
                gap: 10,
              }}
            >
              {/* Status icon */}
              <span style={{
                fontSize: 16, fontWeight: 700,
                color: STATUS_COLORS[check.status],
                minWidth: 20, marginTop: 1,
              }}>
                {STATUS_ICONS[check.status]}
              </span>

              {/* Content */}
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: "#111827" }}>
                  {check.label}
                </div>
                <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2, lineHeight: 1.5 }}>
                  {check.detail}
                </div>
                {check.citations.length > 0 && (
                  <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 3 }}>
                    📚 CITATIONS.md: {check.citations.join(", ")}
                  </div>
                )}
              </div>

              {/* Action button */}
              {check.action_type !== "no_op" && check.action_label && (
                <button
                  onClick={() => void handleFix(check)}
                  disabled={running[check.label]}
                  style={{
                    padding: "4px 12px",
                    border: `1px solid ${STATUS_COLORS[check.status]}`,
                    borderRadius: 5,
                    background: "transparent",
                    color: STATUS_COLORS[check.status],
                    fontSize: 11, fontWeight: 600,
                    cursor: running[check.label] ? "wait" : "pointer",
                    whiteSpace: "nowrap",
                    flexShrink: 0,
                    marginTop: 2,
                  }}
                >
                  {running[check.label] ? "Running…" : `▶ ${check.action_label}`}
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Loading state */}
      {loading && !result && (
        <div style={{
          textAlign: "center", padding: "3rem",
          color: "#6b7280", fontSize: 13,
        }}>
          Running foundation checks…
        </div>
      )}

      {/* Citations footer */}
      <div style={{
        marginTop: 24, padding: "12px 16px",
        borderRadius: 8, background: "#f8fafc",
        border: "1px solid #e5e7eb", fontSize: 11, color: "#6b7280",
      }}>
        <div style={{ fontWeight: 700, marginBottom: 4, color: "#374151" }}>
          📖 Citation Policy (AGENTS.md H19)
        </div>
        Every data file, corpus, and report must have{" "}
        <code style={{ background: "#e5e7eb", padding: "1px 4px", borderRadius: 3 }}>
          _citation
        </code>{" "}
        metadata referencing CITATIONS.md. All authors must be credited.
        See <strong>CITATIONS.md</strong> for the full source registry including:
        Mahadevan (1977, 2003), Parpola (1994, 2010), Fuls &amp; Wells (ICIT),
        Miller / Holdat LLC, Burrow &amp; Emeneau (DEDR), Laursen, Gadd, Kjærum, Al-Sindi.
      </div>
    </div>
  );
}
