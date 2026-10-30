import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { intakeTokenFromFragment, initAuth } from "./auth";
import { reportFrontend } from "./feReport";

// Spec 082: take the API token in from the launch fragment and strip
// it BEFORE anything else runs — the router's hash sync in App must
// never observe (or preserve) the token-bearing fragment. initAuth
// completes the startup probe (health auth mode) asynchronously.
intakeTokenFromFragment();
void initAuth();

/**
 * Send a frontend log entry to the backend. Delegates to the shared
 * reporter (feReport.ts, GAP-C09F): the outcome of every report is
 * tracked and a failure is console-visible — never fire-and-forget.
 */
function feLog(level: string, message: string, stack?: string): void {
  reportFrontend(level, message, { stack });
}

// ── Global error capture ─────────────────────────────────────────────────────
// Catches errors that escape React (e.g. in event handlers, setTimeout callbacks).
// React render errors are caught by ErrorBoundary.componentDidCatch.

const _origConsoleError = console.error.bind(console);
console.error = (...args: unknown[]) => {
  _origConsoleError(...args);
  // Only forward strings — avoid trying to serialise huge React objects.
  const msg = args
    .filter((a) => typeof a === "string" || a instanceof Error)
    .map((a) => (a instanceof Error ? `${a.name}: ${a.message}` : String(a)))
    .join(" ");
  if (msg) feLog("ERROR", `[console.error] ${msg}`);
};

window.onerror = (event, source, lineno, colno, error) => {
  const msg = error ? `${error.name}: ${error.message}` : String(event);
  feLog("ERROR", `[uncaught] ${msg} (${source ?? "?"}:${lineno ?? 0}:${colno ?? 0})`,
    error?.stack);
  return false; // let default handler run too
};

window.onunhandledrejection = (e) => {
  const reason = e.reason instanceof Error
    ? `${e.reason.name}: ${e.reason.message}`
    : String(e.reason ?? "(unknown)");
  feLog("ERROR", `[unhandledrejection] ${reason}`,
    e.reason instanceof Error ? e.reason.stack : undefined);
};

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
