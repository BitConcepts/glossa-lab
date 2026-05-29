/**
 * ResearchLoopPanel — dashboard tile for the Integrated Research Loop.
 *
 * Shows last run results + Start/Stop controls. When running, displays
 * real-time cycle-by-cycle progress via SSE from the backend.
 *
 * API:
 *   POST /api/v1/research-loop/start?max_cycles=N  → SSE stream
 *   GET  /api/v1/research-loop/status               → current state
 *   POST /api/v1/research-loop/stop                 → graceful stop
 *   GET  /api/v1/research-loop/results              → full results
 */

import { useCallback, useEffect, useState } from "react";

const BASE = "/api/v1/research-loop";

interface CycleEntry {
  cycle: number;
  gap_targeted: string;
  experiment: string;
  n_papers: number;
  n_insights: number;
  verdict: string;
  is_new_info: boolean;
}

interface LoopStatus {
  running: boolean;
  cycles_completed: number;
  max_cycles: number;
  total_papers: number;
  total_insights: number;
  history: CycleEntry[];
}

export function ResearchLoopPanel() {
  const [status, setStatus] = useState<LoopStatus | null>(null);
  const [running, setRunning] = useState(false);
  const [cycles, setCycles] = useState(15);
  const [log, setLog] = useState<CycleEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/status`);
      if (res.ok) {
        const data = await res.json();
        setStatus(data);
      }
    } catch {
      // Backend may not be running
    }
  }, []);

  useEffect(() => {
    void fetchStatus();
  }, [fetchStatus]);

  const startLoop = async () => {
    setRunning(true);
    setError(null);
    setLog([]);

    try {
      const res = await fetch(`${BASE}/start?max_cycles=${cycles}`, {
        method: "POST",
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

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
            if (line.startsWith("data: ")) {
              try {
                const entry = JSON.parse(line.slice(6)) as CycleEntry & { type?: string };
                if (entry.type === "complete") {
                  // Final event
                  void fetchStatus();
                } else if (entry.cycle) {
                  setLog((prev) => [...prev, entry]);
                }
              } catch {
                // Ignore parse errors
              }
            }
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
    try {
      await fetch(`${BASE}/stop`, { method: "POST" });
    } catch {
      // Ignore
    }
  };

  const totalPapers = log.reduce((s, c) => s + c.n_papers, 0);
  const totalInsights = log.reduce((s, c) => s + c.n_insights, 0);

  return (
    <div style={{
      border: "1px solid #c4b5fd",
      borderRadius: 10,
      padding: 16,
      background: "#faf5ff",
      marginBottom: 16,
    }}>
      {/* Header */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 12,
      }}>
        <div>
          <span style={{ fontSize: 16, fontWeight: 700, color: "#5b21b6" }}>
            🔄 Integrated Research Loop
          </span>
          <span style={{
            marginLeft: 8,
            padding: "2px 8px",
            borderRadius: 4,
            fontSize: 11,
            fontWeight: 600,
            background: running ? "#dcfce7" : "#f3f4f6",
            color: running ? "#15803d" : "#6b7280",
          }}>
            {running ? "⏳ Running…" : "Ready"}
          </span>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <select
            value={cycles}
            onChange={(e) => setCycles(parseInt(e.target.value, 10))}
            disabled={running}
            style={{
              padding: "4px 8px",
              border: "1px solid #d1d5db",
              borderRadius: 5,
              fontSize: 12,
              background: "#fff",
            }}
          >
            {[5, 10, 15, 20, 30].map((n) => (
              <option key={n} value={n}>
                {n} cycles
              </option>
            ))}
          </select>
          {!running ? (
            <button
              onClick={() => void startLoop()}
              style={{
                padding: "6px 14px",
                border: "1px solid #7c3aed",
                borderRadius: 6,
                background: "#7c3aed",
                color: "#fff",
                fontSize: 12,
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              ▶ Start Loop
            </button>
          ) : (
            <button
              onClick={() => void stopLoop()}
              style={{
                padding: "6px 14px",
                border: "1px solid #dc2626",
                borderRadius: 6,
                background: "#dc2626",
                color: "#fff",
                fontSize: 12,
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              ■ Stop
            </button>
          )}
        </div>
      </div>

      {/* Protocol description */}
      <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 10 }}>
        Mine → Analyze → Register → Execute → Analyze · {cycles} cycles ·
        15 gap topics × 15 experiment templates
      </div>

      {/* Metrics row */}
      {(log.length > 0 || status?.cycles_completed) && (
        <div style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr 1fr",
          gap: 8,
          marginBottom: 12,
        }}>
          <MetricTile label="Cycles" value={log.length || status?.cycles_completed || 0} />
          <MetricTile label="Papers" value={totalPapers || status?.total_papers || 0} />
          <MetricTile label="Insights" value={totalInsights || status?.total_insights || 0} />
          <MetricTile
            label="New experiments"
            value={log.filter((c) => c.is_new_info).length}
          />
        </div>
      )}

      {/* Cycle log */}
      {log.length > 0 && (
        <div style={{
          maxHeight: 240,
          overflowY: "auto",
          border: "1px solid #e5e7eb",
          borderRadius: 6,
          background: "#fff",
        }}>
          {log.map((entry) => (
            <div
              key={entry.cycle}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                padding: "6px 10px",
                borderBottom: "1px solid #f3f4f6",
                fontSize: 11,
              }}
            >
              <span style={{
                width: 24,
                fontWeight: 700,
                color: "#7c3aed",
              }}>
                C{entry.cycle}
              </span>
              <span style={{
                width: 140,
                color: "#374151",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}>
                {entry.gap_targeted}
              </span>
              <span style={{ color: "#6b7280" }}>→</span>
              <span style={{
                width: 160,
                color: "#1d4ed8",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}>
                {entry.experiment}
              </span>
              <span style={{
                flex: 1,
                color: "#374151",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}>
                {entry.verdict.slice(0, 60)}
              </span>
              <span style={{
                fontSize: 10,
                padding: "1px 6px",
                borderRadius: 3,
                background: entry.is_new_info ? "#dcfce7" : "#f3f4f6",
                color: entry.is_new_info ? "#15803d" : "#9ca3af",
                fontWeight: 600,
              }}>
                {entry.is_new_info ? "NEW" : "repeat"}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Last run summary (when not actively running) */}
      {!running && !log.length && status && status.cycles_completed > 0 && (
        <div style={{ fontSize: 12, color: "#374151" }}>
          Last run: {status.cycles_completed} cycles,{" "}
          {status.total_papers} papers, {status.total_insights} insights
        </div>
      )}

      {error && (
        <div style={{
          marginTop: 8,
          fontSize: 12,
          color: "#dc2626",
          background: "#fef2f2",
          border: "1px solid #fca5a5",
          borderRadius: 6,
          padding: "6px 10px",
        }}>
          {error}
        </div>
      )}
    </div>
  );
}

function MetricTile({ label, value }: { label: string; value: number }) {
  return (
    <div style={{
      padding: "8px 10px",
      background: "#fff",
      border: "1px solid #e5e7eb",
      borderRadius: 6,
      textAlign: "center",
    }}>
      <div style={{ fontSize: 18, fontWeight: 800, color: "#5b21b6" }}>
        {value.toLocaleString()}
      </div>
      <div style={{ fontSize: 10, color: "#6b7280" }}>{label}</div>
    </div>
  );
}
