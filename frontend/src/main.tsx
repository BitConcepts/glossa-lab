import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { ErrorBoundary } from "./components/ErrorBoundary";

const BASE_URL = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8001/api/v1";

/** Send a frontend log entry to the backend (best-effort, never throws). */
function feLog(level: string, message: string, stack?: string): void {
  try {
    fetch(`${BASE_URL}/terminal/log/frontend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        level,
        message: message.slice(0, 800),
        source: "FE",
        module: "frontend",
        stack: stack?.slice(0, 800),
        url: window.location.href,
      }),
    }).catch(() => {});
  } catch { /* noop */ }
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
