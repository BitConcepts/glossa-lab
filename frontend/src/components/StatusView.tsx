/**
 * StatusView — live system status + hardware metrics dashboard.
 *
 * Streams CPU, RAM, GPU, disk and network metrics via SSE at 1-second intervals.
 * Shows animated gauges, sparkline history, peak tracking, and clear-peaks button.
 * Also displays backend health and catalog summary.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  clearPeaks,
  getCatalog,
  getHealth,
  getStatus,
  getSystemMetricsStreamUrl,
  listStudies,
  type CatalogResponse,
  type HealthResponse,
  type StatusResponse,
  type SystemMetrics,
} from "../api";
import { useToast } from "../hooks/useToast";

const HISTORY_LEN = 60; // 60 seconds of sparkline history

// ── Gauge component ───────────────────────────────────────────────────────────

function Gauge({
  value, max = 100, label, sub = "", color = "#2563eb", peak,
}: {
  value: number; max?: number; label: string; sub?: string; color?: string; peak?: number;
}) {
  const pct = Math.min(100, (value / max) * 100);
  const peakPct = peak !== undefined ? Math.min(100, (peak / max) * 100) : undefined;
  const warn = pct > 80;
  const crit = pct > 95;
  const gaugeColor = crit ? "#dc2626" : warn ? "#d97706" : color;

  return (
    <div style={{ padding: "12px 14px", borderRadius: 8, border: "1px solid #e5e7eb", background: "#fafafa", flex: 1, minWidth: 140 }}>
      <div style={{ fontSize: 10, fontWeight: 700, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>{label}</div>
      <div style={{ fontSize: 22, fontWeight: 800, color: gaugeColor, fontFamily: "monospace", marginBottom: 4, lineHeight: 1 }}>
        {value.toFixed(value < 10 ? 1 : 0)}<span style={{ fontSize: 11, fontWeight: 400, color: "#9ca3af", marginLeft: 2 }}>
          {max === 100 ? "%" : ""}
        </span>
      </div>
      {sub && <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 6 }}>{sub}</div>}
      {/* Bar */}
      <div style={{ height: 5, background: "#f3f4f6", borderRadius: 3, overflow: "visible", position: "relative" }}>
        <div style={{
          height: "100%", width: `${pct}%`, background: gaugeColor,
          borderRadius: 3, transition: "width 0.4s ease",
        }} />
        {peakPct !== undefined && (
          <div style={{
            position: "absolute", top: -1, left: `${peakPct}%`,
            width: 2, height: 7, background: "#9ca3af", borderRadius: 1,
            transform: "translateX(-50%)",
          }} title={`Peak: ${peak?.toFixed(1)}`} />
        )}
      </div>
      {peakPct !== undefined && (
        <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 3 }}>Peak {peak?.toFixed(1)}{max === 100 ? "%" : ""}</div>
      )}
    </div>
  );
}

// ── Sparkline history ─────────────────────────────────────────────────────────

function SparklineChart({ values, color = "#2563eb", height = 32 }: {
  values: number[]; color?: string; height?: number;
}) {
  if (values.length < 2) return <div style={{ height }} />;
  const max = Math.max(...values, 1);
  const W = 200; const step = W / (values.length - 1);
  const pts = values.map((v, i) => `${i * step},${height - (v / max) * (height - 2) - 1}`).join(" ");
  return (
    <svg viewBox={`0 0 ${W} ${height}`} style={{ width: "100%", height, display: "block" }}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth={1.5} opacity={0.8} />
      <circle cx={(values.length - 1) * step} cy={height - (values[values.length - 1] / max) * (height - 2) - 1}
        r={2.5} fill={color} />
    </svg>
  );
}

// ── Metric row ────────────────────────────────────────────────────────────────

function MetricRow({ label, current, unit, peak, color = "#6b7280" }: {
  label: string; current: string; unit?: string; peak?: string; color?: string;
}) {
  return (
    <div style={{ display: "flex", gap: 8, padding: "4px 0", borderBottom: "1px solid #f3f4f6", alignItems: "center", fontSize: 12 }}>
      <span style={{ color: "#9ca3af", width: 120, flexShrink: 0 }}>{label}</span>
      <span style={{ fontFamily: "monospace", fontWeight: 600, color }}>{current}<span style={{ color: "#9ca3af", marginLeft: 2, fontSize: 10 }}>{unit}</span></span>
      {peak && <span style={{ marginLeft: "auto", fontSize: 10, color: "#9ca3af" }}>↑ {peak}{unit}</span>}
    </div>
  );
}

// ── Core counts ───────────────────────────────────────────────────────────────

function CoreGrid({ values }: { values: number[] }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 3, marginTop: 8 }}>
      {values.map((v, i) => {
        const c = v > 80 ? "#dc2626" : v > 50 ? "#d97706" : "#16a34a";
        return (
          <div key={i} title={`Core ${i}: ${v}%`} style={{
            width: 20, height: 20, borderRadius: 3, background: c + "20", border: `1px solid ${c}40`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 7, fontWeight: 700, color: c,
          }}>
            {Math.round(v)}
          </div>
        );
      })}
    </div>
  );
}

// ── Main StatusView ───────────────────────────────────────────────────────────

export function StatusView() {
  const { toast } = useToast();
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [appStatus, setAppStatus] = useState<StatusResponse | null>(null);
  const [catalog, setCatalog] = useState<CatalogResponse | null>(null);
  const [studyCount, setStudyCount] = useState<number | null>(null);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [connError, setConnError] = useState<string | null>(null);
  const [clearingPeaks, setClearingPeaks] = useState(false);

  // Sparkline history buffers
  const history = useRef<Record<string, number[]>>({
    cpu: [], ram: [], gpu: [], disk_read: [], disk_write: [], net_send: [], net_recv: [],
  });

  const pushHistory = useCallback((key: string, val: number) => {
    const buf = history.current[key] ?? [];
    buf.push(val);
    if (buf.length > HISTORY_LEN) buf.shift();
    history.current[key] = buf;
  }, []);

  // Backend health poll
  useEffect(() => {
    const poll = async () => {
      try {
        const [h, s] = await Promise.all([getHealth(), getStatus()]);
        setHealth(h); setAppStatus(s); setConnError(null);
        getCatalog().then(setCatalog).catch(() => {});
        listStudies().then((ss) => setStudyCount(ss.length)).catch(() => {});
      } catch (e) {
        setConnError(e instanceof Error ? e.message : "Connection failed");
      }
    };
    poll();
    const id = setInterval(poll, 8000);
    return () => clearInterval(id);
  }, []);

  // SSE metrics stream
  const esRef = useRef<EventSource | null>(null);
  const [streaming, setStreaming] = useState(false);

  const startStream = useCallback(() => {
    if (esRef.current) return;
    const es = new EventSource(getSystemMetricsStreamUrl());
    esRef.current = es;
    setStreaming(true);
    es.onmessage = (ev) => {
      try {
        const m: SystemMetrics = JSON.parse(ev.data);
        setMetrics(m);
        pushHistory("cpu", m.cpu.percent);
        pushHistory("ram", m.ram.percent);
        pushHistory("gpu", m.gpu[0]?.utilization_pct ?? 0);
        pushHistory("disk_read", m.disk.read_mbps);
        pushHistory("disk_write", m.disk.write_mbps);
        pushHistory("net_send", m.network.send_mbps * 1000);
        pushHistory("net_recv", m.network.recv_mbps * 1000);
      } catch { /* ignore */ }
    };
    es.onerror = () => {
      es.close(); esRef.current = null; setStreaming(false);
      setTimeout(startStream, 3000);
    };
  }, [pushHistory]);

  useEffect(() => {
    startStream();
    return () => { esRef.current?.close(); esRef.current = null; };
  }, [startStream]);

  const handleClearPeaks = async () => {
    setClearingPeaks(true);
    try { await clearPeaks(); toast("Peaks cleared", "success"); }
    catch { toast("Failed to clear peaks", "error"); }
    finally { setClearingPeaks(false); }
  };

  const healthy = health?.status === "healthy";
  const m = metrics;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h2 style={{ margin: 0 }}>System Status</h2>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          {streaming && (
            <span style={{ fontSize: 11, color: "#16a34a", display: "flex", alignItems: "center", gap: 4 }}>
              <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#16a34a", display: "inline-block", animation: "healthPulse 1.5s infinite" }} />
              Live
            </span>
          )}
          <button onClick={handleClearPeaks} disabled={clearingPeaks}
            style={{ padding: "4px 12px", border: "1px solid #e5e7eb", borderRadius: 4, background: "#f9fafb", cursor: "pointer", fontSize: 12, color: "#6b7280" }}>
            {clearingPeaks ? "…" : "Clear Peaks"}
          </button>
        </div>
      </div>

      {/* Backend health */}
      <div style={{ padding: "12px 16px", borderRadius: 8, border: `1px solid ${healthy ? "#bbf7d0" : "#fca5a5"}`, background: healthy ? "#f0fdf4" : "#fef2f2", marginBottom: "1.5rem" }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
          <span style={{ fontSize: 10, fontWeight: 700, color: "#9ca3af", textTransform: "uppercase" }}>Backend</span>
          <span style={{ fontWeight: 700, color: healthy ? "#16a34a" : "#dc2626" }}>
            {connError ? `Offline — ${connError}` : health?.status ?? "Loading…"}
          </span>
          {health && (
            <>
              <span style={{ fontSize: 12, color: "#6b7280" }}>v{health.version}</span>
              <span style={{ fontSize: 12, color: "#6b7280" }}>up {Math.round(health.uptime_seconds)}s</span>
            </>
          )}
          {catalog && (
            <>
              {Object.entries(catalog.counts).map(([k, v]) => (
                <span key={k} style={{ fontSize: 11, padding: "1px 7px", borderRadius: 6, background: "#f3f4f6", color: "#374151" }}>{k}: {v}</span>
              ))}
            </>
          )}
          {studyCount !== null && (
            <span style={{ fontSize: 11, padding: "1px 7px", borderRadius: 6, background: "#f3f4f6", color: "#374151" }}>studies: {studyCount}</span>
          )}
        </div>
      </div>

      {!m && (
        <div style={{ textAlign: "center", padding: "3rem", color: "#9ca3af" }}>
          <div style={{ fontSize: 28, marginBottom: 8 }}>⚙️</div>
          <div>Connecting to metrics stream…</div>
        </div>
      )}

      {m && (
        <>
          {/* ── CPU ── */}
          <section style={sectionStyle}>
            <div style={sectionHeader}>
              <span style={sectionTitle}>CPU</span>
              <span style={{ fontSize: 11, color: "#6b7280" }}>
                {m.cpu.count_physical}C / {m.cpu.count_logical}T
                {m.cpu.freq_mhz && ` · ${m.cpu.freq_mhz} MHz`}
                {m.cpu.freq_max_mhz && ` (max ${m.cpu.freq_max_mhz} MHz)`}
              </span>
            </div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
              <Gauge value={m.cpu.percent} label="Utilization" color="#2563eb" peak={m.cpu.peak_pct}
                sub={`${m.cpu.count_logical} logical cores`} />
            </div>
            <div style={{ marginBottom: 8 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 }}>60s History</div>
              <SparklineChart values={history.current.cpu} color="#2563eb" height={36} />
            </div>
            <CoreGrid values={m.cpu.per_core_pct} />
          </section>

          {/* ── RAM ── */}
          <section style={sectionStyle}>
            <div style={sectionHeader}>
              <span style={sectionTitle}>Memory</span>
              <span style={{ fontSize: 11, color: "#6b7280" }}>{m.ram.total_gb} GB total</span>
            </div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
              <Gauge value={m.ram.percent} label="RAM Usage" color="#7c3aed" peak={m.ram.peak_pct}
                sub={`${m.ram.used_gb} / ${m.ram.total_gb} GB used`} />
              {m.ram.swap_total_gb > 0 && (
                <Gauge value={(m.ram.swap_used_gb / m.ram.swap_total_gb) * 100} label="Swap"
                  color="#d97706" sub={`${m.ram.swap_used_gb.toFixed(1)} / ${m.ram.swap_total_gb} GB`} />
              )}
            </div>
            <SparklineChart values={history.current.ram} color="#7c3aed" height={36} />
            <div style={{ marginTop: 6 }}>
              <MetricRow label="Available" current={m.ram.available_gb.toString()} unit=" GB" color="#16a34a" />
              <MetricRow label="Used" current={m.ram.used_gb.toString()} unit=" GB" />
            </div>
          </section>

          {/* ── GPU ── */}
          {m.gpu.length > 0 && (
            <section style={sectionStyle}>
              <div style={sectionHeader}>
                <span style={sectionTitle}>GPU</span>
                <span style={{ fontSize: 11, color: "#6b7280" }}>{m.gpu[0].name}</span>
              </div>
              {m.gpu.map((gpu, i) => (
                <div key={i} style={{ marginBottom: 10 }}>
                  <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
                    <Gauge value={gpu.utilization_pct} label="GPU Util" color="#16a34a" peak={m.gpu_peaks.utilization_pct}
                      sub={`${gpu.temperature_c !== null ? gpu.temperature_c + "°C" : ""}`} />
                    <Gauge value={gpu.memory_utilization_pct} label="VRAM %" color="#d97706" peak={m.gpu_peaks.memory_utilization_pct}
                      sub={`${gpu.memory_used_mb} / ${gpu.memory_total_mb} MB`} />
                    <Gauge value={(gpu.memory_used_mb / gpu.memory_total_mb) * 100} label="VRAM Used"
                      color="#d97706" sub={`${(gpu.memory_used_mb / 1024).toFixed(1)} / ${(gpu.memory_total_mb / 1024).toFixed(1)} GB`} />
                  </div>
                </div>
              ))}
              <SparklineChart values={history.current.gpu} color="#16a34a" height={36} />
            </section>
          )}

          {m.gpu.length === 0 && (
            <section style={{ ...sectionStyle, padding: "12px 16px" }}>
              <div style={{ color: "#9ca3af", fontSize: 13 }}>🎮 No NVIDIA GPU detected — nvidia-smi not available or no GPU present.</div>
            </section>
          )}

          {/* ── Disk ── */}
          <section style={sectionStyle}>
            <div style={sectionHeader}>
              <span style={sectionTitle}>Disk</span>
              <span style={{ fontSize: 11, color: "#6b7280" }}>{m.disk.total_gb} GB total · {m.disk.free_gb} GB free</span>
            </div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
              <Gauge value={m.disk.percent} label="Disk Used" color="#dc2626"
                sub={`${m.disk.used_gb} / ${m.disk.total_gb} GB`} />
            </div>
            <div style={{ display: "flex", gap: 16, marginBottom: 8 }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 10, color: "#9ca3af", marginBottom: 2 }}>Read MB/s</div>
                <SparklineChart values={history.current.disk_read} color="#2563eb" height={28} />
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 10, color: "#9ca3af", marginBottom: 2 }}>Write MB/s</div>
                <SparklineChart values={history.current.disk_write} color="#dc2626" height={28} />
              </div>
            </div>
            <div>
              <MetricRow label="Read" current={m.disk.read_mbps.toFixed(2)} unit=" MB/s" color="#2563eb"
                peak={m.disk.peak_read_mbps.toFixed(2)} />
              <MetricRow label="Write" current={m.disk.write_mbps.toFixed(2)} unit=" MB/s" color="#dc2626"
                peak={m.disk.peak_write_mbps.toFixed(2)} />
            </div>
          </section>

          {/* ── Network ── */}
          <section style={sectionStyle}>
            <div style={sectionHeader}>
              <span style={sectionTitle}>Network</span>
              <span style={{ fontSize: 11, color: "#6b7280" }}>
                ↑ {m.network.total_sent_gb.toFixed(2)} GB sent · ↓ {m.network.total_recv_gb.toFixed(2)} GB recv
              </span>
            </div>
            <div style={{ display: "flex", gap: 16, marginBottom: 8 }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 10, color: "#9ca3af", marginBottom: 2 }}>Upload KB/s</div>
                <SparklineChart values={history.current.net_send} color="#7c3aed" height={28} />
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 10, color: "#9ca3af", marginBottom: 2 }}>Download KB/s</div>
                <SparklineChart values={history.current.net_recv} color="#16a34a" height={28} />
              </div>
            </div>
            <div>
              <MetricRow label="Upload" current={(m.network.send_mbps * 1000).toFixed(1)} unit=" KB/s" color="#7c3aed"
                peak={(m.network.peak_send_mbps * 1000).toFixed(1)} />
              <MetricRow label="Download" current={(m.network.recv_mbps * 1000).toFixed(1)} unit=" KB/s" color="#16a34a"
                peak={(m.network.peak_recv_mbps * 1000).toFixed(1)} />
            </div>
          </section>

          {/* ── Pipelines summary ── */}
          {appStatus?.pipelines && appStatus.pipelines.length > 0 && (
            <section style={sectionStyle}>
              <div style={sectionHeader}><span style={sectionTitle}>Registered Pipelines</span></div>
              <ul style={{ columnCount: 2, paddingLeft: "1.2rem", margin: 0, fontSize: 12 }}>
                {appStatus.pipelines.map((p) => <li key={p} style={{ fontFamily: "monospace", marginBottom: 2 }}>{p}</li>)}
              </ul>
            </section>
          )}
        </>
      )}

      <style>{`@keyframes healthPulse { 0%,100%{opacity:1} 50%{opacity:0.3} }`}</style>
    </div>
  );
}

const sectionStyle: React.CSSProperties = {
  marginBottom: "1rem", padding: "14px 16px", border: "1px solid #e5e7eb", borderRadius: 8,
};

const sectionHeader: React.CSSProperties = {
  display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12,
};

const sectionTitle: React.CSSProperties = {
  fontSize: 12, fontWeight: 700, color: "#374151", textTransform: "uppercase", letterSpacing: 0.5,
};
