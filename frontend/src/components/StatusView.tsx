/**
 * StatusView — the Status screen (Spec 081 step 7, wireframe 14).
 *
 * Identity before metrics, always: the first card names what is
 * actually answering — application, version + build, host, data
 * folder, serving-since — read from the serving backend itself
 * (/status + /health), never inferred (FR-007 / C081-3). Then
 * health, the two foundation sets shown separately and labelled
 * (D2.1), the frontend error-reporting state (GAP-C09F: never fired /
 * last confirmed / last FAILED), the machine metrics (kept from the
 * previous dashboard; streamed by fetch, never EventSource — Spec
 * 082), and finally the session log: this session's lines only,
 * framed as such, with earlier lines behind a labelled history
 * toggle. The bottom panel that used to carry the log is gone (Q8).
 */
import { useCallback, useEffect, useRef, useState, useSyncExternalStore } from "react";
import {
  clearPeaks,
  getCatalog,
  getFoundationStatus,
  getHealth,
  getLog,
  getResearchFoundationCheck,
  getStatus,
  listStudies,
  streamSystemMetrics,
  type CatalogResponse,
  type FoundationStatus,
  type HealthResponse,
  type ResearchFoundationCheck,
  type StatusResponse,
  type SystemMetrics,
} from "../api";
import { getFeReportState, subscribeFeReport } from "../feReport";
import { useToast } from "../hooks/useToast";
import { fmtClock, fmtDayTime, humanizeUptime } from "./ui081";

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

// ── Identity rows ─────────────────────────────────────────────────────────────

function IdRow({ k, children }: { k: string; children: React.ReactNode }) {
  return (
    <div style={{ display: "flex", gap: 12, padding: "5px 0", borderBottom: "1px solid #f3f4f6", fontSize: 13, alignItems: "baseline" }}>
      <span style={{ color: "#9ca3af", width: 130, flexShrink: 0, fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5 }}>{k}</span>
      <span style={{ color: "#111827", minWidth: 0 }}>{children}</span>
    </div>
  );
}

// ── Session log parsing ───────────────────────────────────────────────────────

interface LogLine { raw: string; ts: number | null; level: string; text: string }

function parseLogLine(raw: string): LogLine {
  try {
    const j = JSON.parse(raw) as { timestamp?: string; level?: string; module?: string; message?: string };
    if (j && typeof j === "object" && typeof j.message === "string") {
      let ts: number | null = null;
      if (j.timestamp) {
        const iso = j.timestamp.replace(" ", "T").replace(",", ".");
        const parsed = Date.parse(iso.endsWith("Z") ? iso : `${iso}Z`);
        ts = isNaN(parsed) ? null : parsed;
      }
      return {
        raw, ts,
        level: j.level ?? "",
        text: `${j.timestamp ?? ""} ${j.level ?? ""} ${j.module ?? ""} ${j.message}`.trim(),
      };
    }
  } catch { /* not a JSON line — show it raw */ }
  return { raw, ts: null, level: "", text: raw };
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
  const [checkedAt, setCheckedAt] = useState<Date | null>(null);
  const [foundation, setFoundation] = useState<FoundationStatus | null>(null);
  const [nativeCheck, setNativeCheck] = useState<ResearchFoundationCheck | null>(null);
  const [logLines, setLogLines] = useState<LogLine[] | null>(null);
  const [logExists, setLogExists] = useState(true);
  const [showFullLog, setShowFullLog] = useState(false);
  const fe = useSyncExternalStore(subscribeFeReport, getFeReportState);

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

  // Backend identity + health poll
  useEffect(() => {
    const poll = async () => {
      try {
        const [h, s] = await Promise.all([getHealth(), getStatus()]);
        setHealth(h); setAppStatus(s); setConnError(null); setCheckedAt(new Date());
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

  // Foundation — both sets, kept separate (D2.1)
  useEffect(() => {
    getFoundationStatus().then(setFoundation).catch(() => {});
    getResearchFoundationCheck().then(setNativeCheck).catch(() => {});
  }, []);

  // Session log
  const loadLog = useCallback(() => {
    getLog(500)
      .then((r) => { setLogLines(r.lines.map(parseLogLine)); setLogExists(r.exists); })
      .catch(() => { setLogLines([]); });
  }, []);
  useEffect(() => { loadLog(); }, [loadLog]);

  // Metrics stream — fetch-streaming (Spec 082: EventSource cannot
  // send the Authorization header).
  const [streaming, setStreaming] = useState(false);
  useEffect(() => {
    let cancelled = false;
    const ctrl = new AbortController();
    const run = async () => {
      while (!cancelled) {
        try {
          setStreaming(true);
          for await (const m of streamSystemMetrics(ctrl.signal)) {
            if (cancelled) break;
            setMetrics(m);
            pushHistory("cpu", m.cpu.percent);
            pushHistory("ram", m.ram.percent);
            pushHistory("gpu", m.gpu[0]?.utilization_pct ?? 0);
            pushHistory("disk_read", m.disk.read_mbps);
            pushHistory("disk_write", m.disk.write_mbps);
            pushHistory("net_send", m.network.send_mbps * 1000);
            pushHistory("net_recv", m.network.recv_mbps * 1000);
          }
        } catch { /* stream ended or backend down — retry below */ }
        setStreaming(false);
        if (!cancelled) await new Promise((r) => setTimeout(r, 3000));
      }
    };
    void run();
    return () => { cancelled = true; ctrl.abort(); };
  }, [pushHistory]);

  const handleClearPeaks = async () => {
    setClearingPeaks(true);
    try { await clearPeaks(); toast("Peaks cleared", "success"); }
    catch { toast("Failed to clear peaks", "error"); }
    finally { setClearingPeaks(false); }
  };

  const healthy = health?.status === "healthy";
  const m = metrics;

  // Session framing for the log: lines at/after the backend's own
  // started_at are this session; unparsed lines follow the line above.
  const sessionStartMs = appStatus?.started_at ? Date.parse(appStatus.started_at) : NaN;
  const sessionLines: LogLine[] = [];
  const historyLines: LogLine[] = [];
  if (logLines) {
    let inSession = isNaN(sessionStartMs);
    for (const l of logLines) {
      if (l.ts !== null && !isNaN(sessionStartMs)) inSession = l.ts >= sessionStartMs;
      (inSession ? sessionLines : historyLines).push(l);
    }
  }
  const sessionErrors = sessionLines.filter((l) => l.level === "ERROR" || l.level === "CRITICAL").length;
  const sessionWarnings = sessionLines.filter((l) => l.level === "WARNING").length;
  const visibleLog = showFullLog ? (logLines ?? []) : sessionLines.slice(-50);

  return (
    <div style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1rem", flexWrap: "wrap", gap: 10 }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 22 }}>Status</h2>
          <div style={{ fontSize: 13, color: "#6b7280", marginTop: 4, maxWidth: "68ch" }}>
            What the tool is, whether it is healthy, and what it has been doing this
            session. Machine numbers are secondary; identity comes first.
          </div>
        </div>
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

      {/* ── Identity — what is actually answering ── */}
      <section style={sectionStyle}>
        <div style={sectionHeader}><span style={sectionTitle}>Identity — what is answering</span></div>
        {connError && !appStatus ? (
          <div style={{ fontSize: 13, color: "#b91c1c" }}>
            The backend is not answering — {connError}. Nothing below can be
            trusted until it does; the tray's status line says whether the
            service is running at all.
          </div>
        ) : (
          <>
            <IdRow k="Application">{appStatus?.app ?? "Glossa Lab"}</IdRow>
            <IdRow k="Version">
              {health ? <>v{health.version}{health.build ? <> · build <span style={{ fontFamily: "monospace" }}>{health.build}</span></> : ""}</> : "—"}
            </IdRow>
            <IdRow k="Host">
              {appStatus?.host ?? "—"}
              <span style={{ color: "#6b7280" }}> · served to this browser from {window.location.origin}</span>
            </IdRow>
            <IdRow k="Data folder">
              {appStatus?.data_dir
                ? <><span style={{ fontFamily: "monospace", fontSize: 12 }}>{appStatus.data_dir}</span>
                    <span style={{ color: "#6b7280" }}> · database {appStatus.db_ready ? "verified at startup" : "NOT verified"}</span></>
                : "—"}
            </IdRow>
            <IdRow k="Serving since">
              {appStatus?.started_at
                ? <>{fmtDayTime(appStatus.started_at)} · up {health ? humanizeUptime(health.uptime_seconds) : "—"}</>
                : "—"}
            </IdRow>
            <IdRow k="API token">
              {health?.auth === "token"
                ? "Required — this app sends the token the tray opened it with (Spec 082)"
                : health?.auth === "disabled"
                  ? "Disabled on this backend — no token is required"
                  : "—"}
            </IdRow>
            <div style={{ fontSize: 11, color: "#9ca3af", marginTop: 8 }}>
              Identity read from the serving backend{checkedAt ? ` at ${fmtClock(checkedAt.toISOString())}` : ""} — this
              screen never guesses which service is answering.
            </div>
          </>
        )}
      </section>

      {/* ── Health ── */}
      <div style={{ padding: "12px 16px", borderRadius: 8, border: `1px solid ${healthy ? "#bbf7d0" : "#fca5a5"}`, background: healthy ? "#f0fdf4" : "#fef2f2", marginBottom: "1rem" }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
          <span style={{ fontSize: 10, fontWeight: 700, color: "#9ca3af", textTransform: "uppercase" }}>Backend</span>
          <span style={{ fontWeight: 700, color: healthy ? "#16a34a" : "#dc2626" }}>
            {connError ? `Offline — ${connError}` : health?.status ?? "Loading…"}
          </span>
          {health && (
            <>
              <span style={{ fontSize: 12, color: "#6b7280" }}>v{health.version}</span>
              <span style={{ fontSize: 12, color: "#6b7280" }}>up {humanizeUptime(health.uptime_seconds)}</span>
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

      {/* ── Frontend error reporting (GAP-C09F) ── */}
      <section style={sectionStyle}>
        <div style={sectionHeader}><span style={sectionTitle}>Frontend error reporting</span></div>
        {fe.lastStatus === "never" && (
          <div style={{ fontSize: 13, color: "#374151" }}>
            No frontend error has been reported this session — the reporter has
            not fired yet. That is a stated state, not missing data: when a
            report fires, its outcome lands here.
          </div>
        )}
        {fe.lastStatus === "confirmed" && (
          <div style={{ fontSize: 13, color: "#374151" }}>
            Last report <b style={{ color: "#15803d" }}>confirmed by the server</b>
            {fe.lastAt ? <> at {fmtClock(fe.lastAt)}</> : ""} · {fe.confirmed} confirmed
            of {fe.attempted} sent this session.
          </div>
        )}
        {fe.lastStatus === "failed" && (
          <div style={{ fontSize: 13, color: "#374151" }}>
            Last report <b style={{ color: "#b91c1c" }}>FAILED</b>
            {fe.lastAt ? <> at {fmtClock(fe.lastAt)}</> : ""} ({fe.lastDetail}) — it did
            not reach the backend log; the failure itself is in the browser
            console. {fe.confirmed} of {fe.attempted} reports confirmed this session.
          </div>
        )}
      </section>

      {/* ── Foundation — two sets, labelled separately (D2.1) ── */}
      <section style={sectionStyle}>
        <div style={sectionHeader}><span style={sectionTitle}>Foundation check — two sets, shown separately</span></div>
        <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
          <div style={{ flex: "1 1 300px", border: "1px solid #f3f4f6", borderRadius: 8, padding: "10px 14px" }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: "#374151", marginBottom: 4 }}>The program's canonical record</div>
            {foundation ? (
              <div style={{ fontSize: 12, color: "#6b7280", lineHeight: 1.6 }}>
                Verdict: <b style={{ color: "#111827" }}>{foundation.verdict ?? "not run yet"}</b>
                {" · "}{foundation.n_ok} ok · {foundation.n_fail} failed · {foundation.n_warn} warnings
                {foundation.last_checked_at && <><br />Last checked {fmtDayTime(foundation.last_checked_at)}</>}
                {foundation.running && <><br />A check is running now.</>}
                {foundation.dirty && <><br />Inputs changed since the last check.</>}
              </div>
            ) : (
              <div style={{ fontSize: 12, color: "#9ca3af" }}>Not answering.</div>
            )}
          </div>
          <div style={{ flex: "1 1 300px", border: "1px solid #f3f4f6", borderRadius: 8, padding: "10px 14px" }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: "#374151", marginBottom: 4 }}>This instance's own checks (API-native set)</div>
            {nativeCheck?.summary ? (
              <div style={{ fontSize: 12, color: "#6b7280", lineHeight: 1.6 }}>
                Verdict: <b style={{ color: "#111827" }}>{nativeCheck.summary.overall_status ?? "—"}</b>
                {" · "}{nativeCheck.summary.n_pass ?? 0} passed · {nativeCheck.summary.n_fail ?? 0} failed · {nativeCheck.summary.n_warn ?? 0} warnings
                {nativeCheck.timestamp && <><br />Read {fmtDayTime(nativeCheck.timestamp)}</>}
                <br />A different set from the canonical record — the two are
                never merged into one number.
              </div>
            ) : (
              <div style={{ fontSize: 12, color: "#9ca3af" }}>Not answering.</div>
            )}
          </div>
        </div>
        <button
          onClick={() => window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "foundation-check" } }))}
          style={{ marginTop: 10, padding: "5px 12px", border: "1px solid #e5e7eb", borderRadius: 6, background: "none", cursor: "pointer", fontSize: 12, color: "#374151" }}
        >
          Open foundation check
        </button>
      </section>

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

      {/* ── Session log ── */}
      <section style={sectionStyle}>
        <div style={sectionHeader}>
          <span style={sectionTitle}>
            Session log — showing this session only
            {appStatus?.started_at ? ` (since ${fmtClock(appStatus.started_at)})` : ""}
          </span>
          <button onClick={loadLog}
            style={{ padding: "4px 12px", border: "1px solid #e5e7eb", borderRadius: 4, background: "#f9fafb", cursor: "pointer", fontSize: 12, color: "#6b7280" }}>
            Refresh
          </button>
        </div>
        <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 8 }}>
          {sessionErrors} errors · {sessionWarnings} warnings this session. Warnings and
          errors are counted for this session only — a clean count here never describes
          earlier runs.
        </div>
        {!logExists && (
          <div style={{ fontSize: 12, color: "#9ca3af" }}>No log file yet — the backend has not written one.</div>
        )}
        {logLines === null && logExists && (
          <div style={{ fontSize: 12, color: "#9ca3af" }}>Loading the log…</div>
        )}
        {logLines !== null && logExists && visibleLog.length === 0 && (
          <div style={{ fontSize: 12, color: "#9ca3af" }}>Nothing in the log for this session yet.</div>
        )}
        {visibleLog.length > 0 && (
          <pre style={{
            margin: 0, maxHeight: 340, overflowY: "auto", background: "#0f172a", color: "#cbd5e1",
            borderRadius: 8, padding: "10px 12px", fontSize: 11, lineHeight: 1.55, whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          }}>
            {visibleLog.map((l, i) => (
              <div key={i} style={{
                color: l.level === "ERROR" || l.level === "CRITICAL" ? "#fca5a5"
                  : l.level === "WARNING" ? "#fcd34d" : undefined,
              }}>
                {l.text}
              </div>
            ))}
          </pre>
        )}
        {historyLines.length > 0 && (
          <button
            onClick={() => setShowFullLog((v) => !v)}
            style={{ marginTop: 10, padding: "5px 12px", border: "1px solid #e5e7eb", borderRadius: 6, background: "none", cursor: "pointer", fontSize: 12, color: "#374151" }}
          >
            {showFullLog ? "Hide the full log" : `Full log — includes ${historyLines.length} earlier lines (history)`}
          </button>
        )}
        {showFullLog && (
          <div style={{ fontSize: 11, color: "#b45309", marginTop: 6 }}>
            The full log includes lines from before this session started — history,
            not this session's record.
          </div>
        )}
      </section>

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
