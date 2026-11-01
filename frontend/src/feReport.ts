/**
 * feReport — the shared frontend error reporter (Spec 081, GAP-C09F
 * frontend half; Leg C finding C-09).
 *
 * Before this module, both reporters (main.tsx's feLog and
 * ErrorBoundary's sendToBackend) were fire-and-forget with
 * `.catch(() => {})`: a failed report was indistinguishable from a
 * successful one, and "zero frontend-error entries in the log" proved
 * nothing. The backend half is fixed (PR #448: the FE-log endpoint
 * returns 500 {"ok":"error"} when the write fails). This module is
 * the frontend half:
 *
 *  - every report's outcome is tracked (attempted / confirmed /
 *    failed, with the time of the last attempt);
 *  - a report counts as CONFIRMED only when the server answers
 *    200 {"ok":"logged"} — anything else is a failure;
 *  - a failed report is CONSOLE-VISIBLE: it is written through the
 *    pristine console.error captured at module load (before main.tsx
 *    installs its forwarding override), so the failure can neither be
 *    swallowed nor recurse into another report;
 *  - the Status screen reads the same state (getFeReportState /
 *    subscribeFeReport) and shows whether reporting has fired, and
 *    whether the server confirmed the last report — "never fired"
 *    is a stated state, not an absence.
 *
 * Spec 082: the report endpoint is token-gated, so the POST carries
 * the stored Bearer token (auth.ts). A 401 therefore counts as a
 * failed report — stated in the console and on the Status screen,
 * never swallowed.
 *
 * Reporting never throws and never blocks the UI.
 */

import { authHeaders } from "./auth";

const BASE_URL = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8001/api/v1";

// Captured at module load — main.tsx imports this module (via App /
// ErrorBoundary) before it replaces console.error with the forwarding
// wrapper, so this reference is the browser's own console.error.
const pristineConsoleError: (...args: unknown[]) => void =
  console.error.bind(console);

export interface FeReportState {
  attempted: number;
  confirmed: number;
  failed: number;
  /** "never" until the first report is attempted. */
  lastStatus: "never" | "confirmed" | "failed";
  /** ISO time of the last attempt, or null when never fired. */
  lastAt: string | null;
  /** Short human detail for the last attempt (e.g. "HTTP 500"). */
  lastDetail: string;
}

const state: FeReportState = {
  attempted: 0,
  confirmed: 0,
  failed: 0,
  lastStatus: "never",
  lastAt: null,
  lastDetail: "",
};

const listeners = new Set<(s: FeReportState) => void>();

// Cached snapshot — useSyncExternalStore (the Status screen) needs a
// stable reference between changes, or React loops (error #185).
let snapshot: FeReportState = { ...state };

function notify(): void {
  snapshot = { ...state };
  listeners.forEach((fn) => {
    try { fn(snapshot); } catch { /* a listener must not break reporting */ }
  });
}

export function getFeReportState(): FeReportState {
  return snapshot;
}

export function subscribeFeReport(fn: (s: FeReportState) => void): () => void {
  listeners.add(fn);
  return () => { listeners.delete(fn); };
}

function markFailed(detail: string, originalMessage: string): void {
  state.failed += 1;
  state.lastStatus = "failed";
  state.lastDetail = detail;
  notify();
  // Console-visible by design (C-09): through the pristine reference,
  // so it is neither swallowed by a catch nor forwarded into another
  // report attempt (no loop).
  pristineConsoleError(
    `[glossa] frontend error report FAILED (${detail}) — the error below ` +
    `did NOT reach the backend log: ${originalMessage}`,
  );
}

/**
 * Send one frontend log entry to the backend and track its outcome.
 * Fire-and-forget for the caller; the outcome lands in the shared
 * state and, on failure, in the console.
 */
export function reportFrontend(
  level: string,
  message: string,
  opts: { stack?: string; module?: string } = {},
): void {
  state.attempted += 1;
  state.lastAt = new Date().toISOString();
  notify();
  try {
    fetch(`${BASE_URL}/terminal/log/frontend`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify({
        level,
        message: message.slice(0, 800),
        source: "FE",
        module: opts.module ?? "frontend",
        stack: opts.stack?.slice(0, 800),
        url: window.location.href,
      }),
    })
      .then(async (res) => {
        let ok = false;
        try {
          const body = (await res.json()) as { ok?: unknown };
          ok = res.ok && body?.ok === "logged";
        } catch { ok = false; }
        if (ok) {
          state.confirmed += 1;
          state.lastStatus = "confirmed";
          state.lastDetail = "server confirmed (ok: logged)";
          notify();
        } else {
          markFailed(`HTTP ${res.status}`, message);
        }
      })
      .catch((err: unknown) => {
        markFailed(err instanceof Error ? err.message : "network error", message);
      });
  } catch (err: unknown) {
    markFailed(err instanceof Error ? err.message : "send error", message);
  }
}
