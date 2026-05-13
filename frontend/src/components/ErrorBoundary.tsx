/**
 * ErrorBoundary — catches React render errors so the screen never goes white.
 *
 * Wraps the entire App in main.tsx. Any component that throws during render
 * (or getDerivedStateFromError / componentDidUpdate) is caught here and shown
 * as a readable error card instead of a blank page.
 *
 * The error is also forwarded to POST /api/v1/terminal/log/frontend so it
 * appears in the Glossa Lab log panel alongside backend messages, tagged [FE].
 */
import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props { children: ReactNode; }
interface State { hasError: boolean; error: Error | null; info: ErrorInfo | null; }

const BASE_URL = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8001/api/v1";

function sendToBackend(error: Error, info: ErrorInfo | null): void {
  try {
    const message = `${error.name}: ${error.message}`;
    const stack = (error.stack ?? "") + "\n\nComponent Stack:\n" + (info?.componentStack ?? "");
    fetch(`${BASE_URL}/terminal/log/frontend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        level: "ERROR",
        message,
        source: "FE",
        module: "ErrorBoundary",
        stack: stack.slice(0, 1200),
        url: window.location.href,
      }),
    }).catch(() => {});
  } catch { /* never let logging itself crash */ }
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null, info: null };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    this.setState({ info });
    sendToBackend(error, info);
  }

  render() {
    if (!this.state.hasError) return this.props.children;

    const { error, info } = this.state;
    const msg = error?.message ?? "Unknown error";
    const stack = error?.stack ?? "";
    const compStack = info?.componentStack ?? "";

    return (
      <div style={{
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
        height: "100vh", padding: "32px", background: "#0f172a", color: "#e2e8f0",
        fontFamily: "system-ui, sans-serif",
      }}>
        <div style={{
          maxWidth: 780, width: "100%",
          background: "#1e293b", borderRadius: 12,
          border: "1px solid #ef444444", padding: "28px 32px",
          boxShadow: "0 8px 40px rgba(0,0,0,0.5)",
        }}>
          {/* Header */}
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 18 }}>
            <span style={{ fontSize: 28 }}>💥</span>
            <div>
              <div style={{ fontSize: 18, fontWeight: 700, color: "#f87171" }}>
                Glossa Lab crashed
              </div>
              <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 2 }}>
                A React component threw an error. The error has been logged to the backend.
              </div>
            </div>
          </div>

          {/* Error message */}
          <div style={{
            padding: "10px 14px", background: "#0f172a", borderRadius: 6,
            border: "1px solid #ef444430", marginBottom: 16,
            fontFamily: "monospace", fontSize: 13, color: "#fca5a5",
            wordBreak: "break-all",
          }}>
            {msg}
          </div>

          {/* Stack trace */}
          {stack && (
            <details style={{ marginBottom: 16 }}>
              <summary style={{ cursor: "pointer", fontSize: 12, color: "#64748b", userSelect: "none" }}>
                JS stack trace
              </summary>
              <pre style={{
                marginTop: 8, padding: "8px 12px", background: "#0f172a", borderRadius: 6,
                fontSize: 10, color: "#94a3b8", overflowX: "auto", whiteSpace: "pre-wrap",
                wordBreak: "break-all", maxHeight: 200, overflowY: "auto",
              }}>
                {stack}
              </pre>
            </details>
          )}

          {/* Component stack */}
          {compStack && (
            <details style={{ marginBottom: 20 }}>
              <summary style={{ cursor: "pointer", fontSize: 12, color: "#64748b", userSelect: "none" }}>
                Component stack
              </summary>
              <pre style={{
                marginTop: 8, padding: "8px 12px", background: "#0f172a", borderRadius: 6,
                fontSize: 10, color: "#94a3b8", overflowX: "auto", whiteSpace: "pre-wrap",
                wordBreak: "break-all", maxHeight: 200, overflowY: "auto",
              }}>
                {compStack}
              </pre>
            </details>
          )}

          {/* Actions */}
          <div style={{ display: "flex", gap: 10 }}>
            <button
              onClick={() => window.location.reload()}
              style={{
                padding: "8px 20px", borderRadius: 6, border: "none",
                background: "#2563eb", color: "#fff", cursor: "pointer",
                fontSize: 13, fontWeight: 600,
              }}
            >
              🔄 Reload page
            </button>
            <button
              onClick={() => this.setState({ hasError: false, error: null, info: null })}
              style={{
                padding: "8px 20px", borderRadius: 6,
                border: "1px solid #334155",
                background: "none", color: "#94a3b8", cursor: "pointer",
                fontSize: 13,
              }}
            >
              Try to recover
            </button>
            <div style={{ flex: 1 }} />
            <span style={{ fontSize: 11, color: "#475569", alignSelf: "center" }}>
              Check Logs panel for details
            </span>
          </div>
        </div>
      </div>
    );
  }
}
