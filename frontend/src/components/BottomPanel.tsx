/**
 * BottomPanel — VS Code-style IDE panel.
 * Tabs: Logs | Jobs | Terminal
 * - Drag-resizable from top edge
 * - Minimize collapses to tab bar only
 * - Maximize fills ~65% of viewport
 * - AI Chat tab appears when docked
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  cancelJob, clearJobs, createJob, getJobResults, getEnvStatus,
  getLogStreamUrl, listJobs, pauseJob, resumeJob, pauseAllJobs, resumeAllJobs,
  purgeLog, runTerminalCommand, type EnvStatus, type JobResponse,
} from "../api";
import { fmtDateTimeCompact, fmtElapsed } from "../dateFormat";
import { ChatInline } from "./AIChatWindow";
import { JobErrorModal } from "./JobsView";
import { useAIChat } from "../hooks/useAIChat";
import { useToast } from "../hooks/useToast";

type PanelTab = "logs" | "jobs" | "terminal" | "chat";

const MIN_HEIGHT = 100;
const MAX_HEIGHT_RATIO = 0.65;

// ── Log line parsing + formatting ──────────────────────────────────────────────────────────────
function stripAnsi(s: string): string {
  // eslint-disable-next-line no-control-regex
  return s.replace(/\x1b\[[0-9;]*[mGKHF]/g, "");
}

/**
 * Parse a structured JSON log line like:
 *   {"timestamp":"2026-04-08 16:32:21,111","level":"INFO","module":"glossa_lab.database","message":"Database ready","path":"data/glossa.db"}
 * and return a human-readable string like:
 *   16:32:21 INFO  [glossa_lab.database] Database ready  path=data/glossa.db
 */
function parseLogTimestamp(raw: string): string {
  // Input: "2026-04-08 16:32:21,111" (UTC) or similar
  // Output: locale-formatted time, matching the Jobs panel's toLocaleTimeString()
  try {
    const iso = raw.replace(",", ".").replace(" ", "T") + "Z";
    const dt = new Date(iso);
    if (!isNaN(dt.getTime())) {
      // Show date + time together (e.g. "Apr 13, 6:06 AM")
      return dt.toLocaleString(undefined, {
        month: "short", day: "numeric",
        hour: "numeric", minute: "2-digit",
      });
    }
  } catch { /* fall through */ }
  // Fallback: return full datetime prefix as-is
  return raw.length >= 19 ? raw.slice(0, 19) : raw;
}

/**
 * Extract a short, human-readable message from an embedded JSON error body.
 * Handles OpenAI, Anthropic, FastAPI, Pydantic validation, and generic errors.
 */
function prettifyErrorBody(raw: string): string {
  // If it looks like a Python traceback, return only the last meaningful line
  if (raw.includes("Traceback (most recent call last)") || raw.includes("  File \"")) {
    const lines = raw.split("\n").map(l => l.trim()).filter(Boolean);
    // Find the last line that looks like an actual exception
    for (let i = lines.length - 1; i >= 0; i--) {
      const l = lines[i];
      if (/^[A-Za-z].*Error:|^[A-Za-z].*Exception:|^ValueError:|^KeyError:|^TypeError:/.test(l)) {
        return `\u274c ${l}`;
      }
    }
    // Fall back to last non-empty line
    return `\u274c ${lines[lines.length - 1] ?? raw}`;
  }

  // Try to find embedded JSON in the message (e.g. "LLM API error 429: {...}")
  const jsonMatch = raw.match(/\{[\s\S]*\}/);
  if (!jsonMatch) return raw;
  try {
    const obj = JSON.parse(jsonMatch[0]) as Record<string, unknown>;

    // FastAPI / Pydantic validation: {detail: [{msg, loc}]}
    if (Array.isArray(obj.detail)) {
      const msgs = (obj.detail as Record<string, unknown>[]).map(d => {
        const loc = Array.isArray(d.loc) ? (d.loc as string[]).filter(p => p !== "body").join(".") : "";
        const msg = typeof d.msg === "string" ? d.msg : JSON.stringify(d);
        return loc ? `${loc}: ${msg}` : msg;
      }).filter(Boolean);
      if (msgs.length) {
        const prefix = raw.match(/^(.*?)\{/)?.[1]?.trim();
        return `${prefix ? prefix + " " : ""}${msgs.join("; ")}`;
      }
    }

    // FastAPI single-string detail: {detail: "some message"}
    if (typeof obj.detail === "string") {
      const prefix = raw.match(/^(.*?)\{/)?.[1]?.trim();
      return `${prefix ? prefix + " " : ""}${obj.detail}`;
    }

    // OpenAI / generic: {error: {message, type}} or flat {message, error}
    const inner = (obj.error ?? obj) as Record<string, unknown>;
    const msg = (inner.message ?? inner.detail ?? inner.error) as string | undefined;
    const type = (inner.type ?? inner.code ?? inner.status) as string | undefined;
    if (typeof msg === "string" && msg) {
      const short = msg
        .replace(/\s*For more information.*$/i, "")
        .replace(/\s*Please wait and try again.*$/i, "")
        .replace(/\s*See https?:\/\/.*$/i, "")
        .trim();
      const prefix = raw.match(/^(.*?)\{/)?.[1]?.trim();
      const typeTag = type ? ` [${type}]` : "";
      return `${prefix ? prefix + " " : ""}${short}${typeTag}`;
    }
  } catch { /* not valid JSON, return as-is */ }

  // Truncate very long raw lines
  return raw.length > 300 ? raw.slice(0, 297) + "\u2026" : raw;
}

/** Formatted line with embedded level, source, and text for accurate coloring. */
interface FormattedLine { text: string; level: string; source: string; }

function formatLogLine(raw: string): FormattedLine {
  try {
    const d = JSON.parse(raw) as Record<string, unknown>;
    if (typeof d.message !== "string") return { text: raw, level: "", source: "BE" };
    const ts     = typeof d.timestamp === "string" ? parseLogTimestamp(d.timestamp) : "";
    const lvl    = typeof d.level     === "string" ? d.level : "";
    const source = typeof d.source    === "string" ? d.source : "BE";
    const mod    = typeof d.module    === "string" ? `[${d.module}]` : "";
    // Source prefix: [FE] in amber, [BE] omitted (most lines are backend)
    const srcTag = source === "FE" ? "[FE] " : "";
    let msg: string = d.message;
    if (msg.includes('{"') || msg.includes('{ ')) {
      msg = prettifyErrorBody(msg);
    }
    const extras = Object.entries(d)
      .filter(([k]) => !["timestamp", "level", "module", "message", "source"].includes(k))
      .map(([k, v]) => {
        if (typeof v === "string") return `${k}=${v}`;
        if (typeof v === "number" || typeof v === "boolean") return `${k}=${v}`;
        return `${k}=${JSON.stringify(v)}`;
      })
      .join("  ");
    return {
      text: `${ts} ${lvl.padEnd(5)} ${srcTag}${mod} ${msg}${extras ? "  " + extras : ""}`,
      level: lvl.toUpperCase(),
      source,
    };
  } catch {
    return { text: stripAnsi(raw), level: "", source: "BE" };
  }
}

/** Color by the actual log level first, then fall back to keyword heuristics. */
function logLineColor(line: FormattedLine): string {
  // Use the real log level when available — this prevents "INFO ... failed"
  // from showing red when it's actually a successful info message.
  switch (line.level) {
    case "ERROR":   case "CRITICAL": return "#f87171"; // red
    case "WARNING": return "#fbbf24"; // amber
    case "INFO":    return "#86efac"; // green
    case "DEBUG":   return "#94a3b8"; // gray
  }
  // No level available — keyword heuristic for non-JSON lines
  const l = line.text.toLowerCase();
  if (l.includes("error") || l.includes("exception")) return "#f87171";
  if (l.includes("warn")) return "#fbbf24";
  return "#e2e8f0";
}

// ── Log Panel ─────────────────────────────────────────────────────────────────

function LogPanel() {
  const [lines, setLines] = useState<FormattedLine[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [filter, setFilter] = useState("");
  // streamKey: incrementing this closes the old EventSource and opens a fresh one
  const [streamKey, setStreamKey] = useState(0);
  const bottomRef = useRef<HTMLDivElement>(null);
  const esRef = useRef<EventSource | null>(null);
  const autoScroll = useRef(true);

  useEffect(() => {
    // Close any existing connection before opening new one
    if (esRef.current) { esRef.current.close(); esRef.current = null; }
    const es = new EventSource(getLogStreamUrl());
    esRef.current = es;
    setStreaming(true);
    es.onmessage = (ev) => {
      try {
        const d = JSON.parse(ev.data) as { text: string };
        setLines((prev) => [...prev.slice(-499), formatLogLine(d.text)]);
      } catch { /* ignore */ }
    };
    es.onerror = () => { setStreaming(false); };
    return () => { es.close(); esRef.current = null; };
  // streamKey causes re-run which closes old ES and opens a fresh one
  }, [streamKey]);

  useEffect(() => {
    if (autoScroll.current) bottomRef.current?.scrollIntoView({ behavior: "auto" });
  }, [lines]);

  const visible = filter ? lines.filter((l) => l.text.toLowerCase().includes(filter.toLowerCase())) : lines;

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ display: "flex", gap: 8, padding: "4px 8px", borderBottom: "1px solid #1e293b", alignItems: "center" }}>
        <input
          placeholder="Filter logs…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ flex: 1, padding: "2px 6px", background: "#1e293b", border: "1px solid #334155", borderRadius: 3, fontSize: 11, color: "#e2e8f0", outline: "none" }}
        />
        {streaming && <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#16a34a", animation: "pulse 1.5s infinite", flexShrink: 0 }} />}
        <button
          onClick={async () => {
            // 1. Tell backend to truncate the log file
            await purgeLog().catch(() => {});
            // 2. Clear the display
            setLines([]);
            // 3. Reconnect EventSource — this starts a fresh stream from the
            //    (now-empty) log file, so stale entries never reappear.
            setStreamKey(k => k + 1);
          }}
          title="Purge log file and reset stream (clears file on disk)"
          style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#f97316", cursor: "pointer", fontSize: 10 }}>
          Purge
        </button>
        <button onClick={() => setLines([])} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#94a3b8", cursor: "pointer", fontSize: 10 }}>Clear</button>
        <button
          onClick={() => {
            const text = visible.map(l => l.text).join("\n");
            navigator.clipboard.writeText(text).catch(() => {});
          }}
          title="Copy all visible log lines to clipboard"
          style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#60a5fa", cursor: "pointer", fontSize: 10 }}>
          Copy All
        </button>
      </div>
      <div
        style={{ flex: 1, overflowY: "auto", fontFamily: "monospace", fontSize: 11, padding: "4px 8px", lineHeight: 1.6 }}
        onScroll={(e) => {
          const el = e.currentTarget;
          autoScroll.current = el.scrollTop + el.clientHeight >= el.scrollHeight - 20;
        }}
      >
        {visible.length === 0 && <div style={{ color: "#64748b", fontStyle: "italic" }}>Waiting for log output…</div>}
        {visible.map((line, i) => (
          <div key={i} style={{ color: logLineColor(line), whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{line.text}</div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}

// ── Jobs Panel ────────────────────────────────────────────────────────────────

// ── Sequential Run Queue (fire-and-forget SSE experiment runner) ───────────────
const SEQ_QUEUE_KEY = "glossa_seq_run_queue";
interface SeqQueue { queue: string[]; watchJobId: string | null; }

function loadSeqQueue(): SeqQueue {
  try {
    const raw = JSON.parse(localStorage.getItem(SEQ_QUEUE_KEY) ?? "{}") as Partial<SeqQueue>;
    return { queue: Array.isArray(raw.queue) ? raw.queue : [], watchJobId: raw.watchJobId ?? null };
  }
  catch { return { queue: [], watchJobId: null }; }
}
function saveSeqQueue(q: SeqQueue) { localStorage.setItem(SEQ_QUEUE_KEY, JSON.stringify(q)); }

/** Start an experiment SSE run in the background (fire-and-forget). Returns job tracker. */
function runExpBackground(expId: string) {
  fetch(`/api/v1/experiment-graphs/${expId}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kwargs: {} }),
  }).then(resp => {
    if (!resp.body) return;
    const reader = resp.body.getReader();
    const consume = (): void => { reader.read().then(({ done }) => { if (!done) consume(); }).catch(() => {}); };
    consume();
  }).catch(() => {});
}

function JobsPanel() {
  const { toast } = useToast();
  const [jobs, setJobs] = useState<JobResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState<Set<string>>(new Set());
  const [pausing, setPausing] = useState<Set<string>>(new Set());
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [seqQueue, setSeqQueue] = useState<SeqQueue>(() => loadSeqQueue());
  // Track nodes_done per job to detect slow SA nodes
  const nodesDoneTracker = useRef<Map<string, { done: number; since: number }>>(new Map());

  // Refresh queue state when Experiment Builder (or anything) writes to it
  useEffect(() => {
    const refresh = () => setSeqQueue(loadSeqQueue());
    window.addEventListener("glossa:seq_queue_updated", refresh);
    // Also poll every 3s so the banner appears even if event was missed
    const t = setInterval(refresh, 3000);
    return () => { window.removeEventListener("glossa:seq_queue_updated", refresh); clearInterval(t); };
  }, []);
  const [errorModal, setErrorModal] = useState<{
    title: string; message: string; detail?: string;
    params?: Record<string, unknown> | null;
    job?: JobResponse | null;
    onRetry?: (() => void) | null;
  } | null>(null);

  const handleViewInReports = (expId: string) => {
    const filename = expId ? `${expId}.json` : "";
    window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "reports" } }));
    if (filename) {
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent("glossa:reports_highlight", {
          detail: { tab: "data", search: filename }
        }));
      }, 120);
    }
  };

  // Build a retry handler that re-submits the same job (minus runtime-tracking params)
  const makeRetry = (job: JobResponse) => async () => {
    const SKIP = new Set(["node_count", "nodes_done", "stall_reason"]);
    const clean = Object.fromEntries(
      Object.entries(job.params ?? {}).filter(([k]) => !k.startsWith("_") && !SKIP.has(k))
    );
    try {
      await createJob({ name: `${job.name} (retry)`, pipeline: job.pipeline, params: clean });
      await load();
      toast("Job re-submitted", "info");
    } catch (e) { toast(e instanceof Error ? e.message : "Retry failed", "error"); }
  };

  const handleShowError = async (job: JobResponse) => {
    // Build display params (strip internal keys)
    const displayParams: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(job.params ?? {}))
      if (!k.startsWith("_") && k !== "traceback") displayParams[k] = v;

    try {
      const data = await getJobResults(job.id);
      const raw  = data as Record<string, unknown>;
      const errMsg = (raw.error as string) ?? (raw.message as string) ?? (raw.detail as string) ?? "Unknown error";
      const trace  = (raw.traceback as string) ?? null;
      setErrorModal({
        title: job.name, message: errMsg, detail: trace ?? undefined,
        params: Object.keys(displayParams).length ? displayParams : null,
        job, onRetry: makeRetry(job),
      });
    } catch {
      setErrorModal({
        title: job.name,
        message: "Job failed. No detailed error was stored.",
        params: Object.keys(displayParams).length ? displayParams : null,
        job, onRetry: makeRetry(job),
      });
    }
  };

  const load = useCallback(async () => {
    try {
      const fetched = await listJobs();
      setJobs(fetched);
      setLoading(false);
      // Sequential queue: check if watched job completed and advance queue
      setSeqQueue(prev => {
        if (!prev.watchJobId || (prev.queue?.length ?? 0) === 0) return prev;
        const watched = fetched.find(j => j.id === prev.watchJobId);
        if (!watched) return prev;
        if (watched.status === "completed" || watched.status === "failed" || watched.status === "cancelled") {
          // Advance: run next in queue
          const [next, ...rest] = prev.queue;
          if (next) {
            // small delay to let GPU cool down
            setTimeout(() => runExpBackground(next), 2000);
            // Watch for the new job: find it after a delay
            setTimeout(async () => {
              const fresh = await listJobs();
              const newJob = fresh.find(j =>
                (j.params?.exp_id as string) === next && j.status === "running"
              );
              if (newJob) {
                setSeqQueue(_prev => {
                  const updated = { queue: rest, watchJobId: newJob.id };
                  saveSeqQueue(updated);
                  return updated;
                });
              }
            }, 5000);
          }
          const updated = { queue: rest, watchJobId: null };
          saveSeqQueue(updated);
          return updated;
        }
        return prev;
      });
    } catch { setLoading(false); }
  }, []);

  useEffect(() => {
    load();
    const t = setInterval(load, 3000);
    return () => clearInterval(t);
  }, [load]);

  const handleCancel = async (id: string) => {
    setCancelling((s) => new Set([...s, id]));
    try { await cancelJob(id); await load(); toast("Job aborted", "info"); }
    catch { toast("Cancel failed", "error"); }
    finally { setCancelling((s) => { const n = new Set(s); n.delete(id); return n; }); }
  };

  const handlePause = async (id: string) => {
    setPausing(s => new Set([...s, id]));
    try { await pauseJob(id); await load(); toast("Job paused", "info"); }
    catch { toast("Pause failed", "error"); }
    finally { setPausing(s => { const n = new Set(s); n.delete(id); return n; }); }
  };

  const handleResume = async (id: string) => {
    setPausing(s => new Set([...s, id]));
    try { await resumeJob(id); await load(); toast("Job resumed", "info"); }
    catch { toast("Resume failed", "error"); }
    finally { setPausing(s => { const n = new Set(s); n.delete(id); return n; }); }
  };

  const handlePauseAll = async () => {
    try { await pauseAllJobs(); await load(); toast("All jobs paused", "info"); }
    catch { toast("Pause all failed", "error"); }
  };

  const handleResumeAll = async () => {
    try { await resumeAllJobs(); await load(); toast("All jobs resumed", "info"); }
    catch { toast("Resume all failed", "error"); }
  };

  const clearQueue = () => {
    const empty = { queue: [], watchJobId: null };
    saveSeqQueue(empty);
    setSeqQueue(empty);
  };

  const handleClearAll = async () => {
    try { await clearJobs(); await load(); toast("Jobs cleared", "info"); }
    catch { toast("Clear failed", "error"); }
  };

  const handleClearDone = async () => {
    try { await clearJobs(true); await load(); toast("Finished jobs cleared", "info"); }
    catch { toast("Clear failed", "error"); }
  };

  const finishedCount = jobs.filter((j) => ["completed", "failed", "cancelled"].includes(j.status)).length;
  const activeJobs    = jobs.filter((j) => ["running", "pending"].includes(j.status));

  const handleStopAll = async () => {
    const ids = activeJobs.map(j => j.id);
    if (!ids.length) return;
    setCancelling(new Set(ids));
    try {
      await Promise.all(ids.map(id => cancelJob(id)));
      await load();
      toast(`Stopped ${ids.length} job${ids.length > 1 ? "s" : ""}`, "info");
    } catch { toast("Some cancellations failed", "error"); }
    finally { setCancelling(new Set()); }
  };

  const statusColor: Record<string, string> = {
    pending: "#d97706", running: "#2563eb", completed: "#16a34a",
    failed: "#dc2626", cancelled: "#6b7280", paused: "#92400e",
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", overflowY: "auto" }}>
      <div style={{ padding: "6px 10px", borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 11, color: "#94a3b8" }}>{jobs.length} jobs{activeJobs.length > 0 ? ` (${activeJobs.length} active)` : ""}</span>
        <div style={{ display: "flex", gap: 4 }}>
          <button onClick={load} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#94a3b8", cursor: "pointer", fontSize: 10 }}>⟳</button>
          {activeJobs.length > 0 && (
            <button onClick={handleStopAll} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#f97316", cursor: "pointer", fontSize: 10 }}>Stop All</button>
          )}
          {activeJobs.length > 0 && (
            <button onClick={handlePauseAll} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#d97706", cursor: "pointer", fontSize: 10 }}>⏸ Pause All</button>
          )}
          {jobs.filter(j => j.status === "paused").length > 0 && (
            <button onClick={handleResumeAll} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#22c55e", cursor: "pointer", fontSize: 10 }}>▶ Resume All</button>
          )}
          {finishedCount > 0 && (
            <button onClick={handleClearDone} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#94a3b8", cursor: "pointer", fontSize: 10 }}>Clear Done</button>
          )}
          {jobs.length > 0 && (
            <button onClick={handleClearAll} style={{ padding: "2px 8px", background: "#334155", border: "none", borderRadius: 3, color: "#ef4444", cursor: "pointer", fontSize: 10 }}>Delete All</button>
          )}
        </div>
      </div>
      {/* Sequential run queue banner */}
      {((seqQueue.queue?.length ?? 0) > 0 || seqQueue.watchJobId) && (
        <div style={{ padding: "5px 10px", background: "#0a1525", borderBottom: "1px solid #1e293b",
          display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 9, color: "#60a5fa", fontWeight: 700, flexShrink: 0 }}>⏭ QUEUE</span>
          <span style={{ fontSize: 10, color: "#94a3b8", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {seqQueue.watchJobId
              ? `Watching job ${seqQueue.watchJobId.slice(0, 8)}…`
              : ""}
            {(seqQueue.queue?.length ?? 0) > 0
              ? ` → ${seqQueue.queue.map(e => e.replace("indus_phase", "ph")).join(" → ")}`
              : " (all queued experiments dispatched)"}
          </span>
          <button onClick={clearQueue} style={{ padding: "1px 6px", background: "none", border: "1px solid #334155",
            borderRadius: 3, color: "#64748b", cursor: "pointer", fontSize: 9, flexShrink: 0 }}>clear</button>
        </div>
      )}
      {loading && <div style={{ padding: 10, color: "#64748b", fontSize: 12 }}>Loading…</div>}
      {!loading && jobs.length === 0 && (
        <div style={{ padding: "1rem", textAlign: "center", color: "#64748b", fontSize: 12 }}>
          <div style={{ fontSize: 22, marginBottom: 6 }}>📦</div>
          No jobs in queue. Submit a pipeline job to see it here.
        </div>
      )}
      {jobs.map((job) => {
        const isRunning  = job.status === "running";
        const isExpanded = expandedId === job.id;
        const elapsed = isRunning ? Math.round((Date.now() - new Date(job.created_at).getTime()) / 1000) : null;
        const result = (job as unknown as Record<string, unknown>).result as Record<string, unknown> | string | null | undefined;
        const errMsg = (job as unknown as Record<string, unknown>).error as string | null | undefined;
        // Progress tracking for exp_run jobs
        const nodeCount  = (job.params?.node_count  as number) ?? 0;
        const nodesDone  = (job.params?.nodes_done  as number) ?? 0;
        const pct        = isRunning && nodeCount > 0 ? Math.min(99, Math.round((nodesDone / nodeCount) * 100)) : null;
        // Historical avg for this pipeline (completed jobs)
        const historicalAvgSec = (() => {
          const done = jobs.filter(
            d => d.status === "completed" && d.pipeline === job.pipeline
              && d.id !== job.id && d.updated_at
          );
          if (done.length === 0) return null;
          const durations = done.map(d =>
            (new Date(d.updated_at!).getTime() - new Date(d.created_at).getTime()) / 1000
          ).filter(x => x > 0);
          return durations.length > 0
            ? durations.reduce((a, b) => a + b, 0) / durations.length
            : null;
        })();
        // ETA: historical avg when < 15%, linear extrapolation after (REQ-JOBS-002)
        const etaSec = elapsed !== null && pct !== null
          ? (() => {
              if (pct >= 15) return Math.round((elapsed / pct) * (100 - pct));
              if (historicalAvgSec !== null) return Math.max(0, Math.round(historicalAvgSec - elapsed));
              return null;
            })()
          : null;
        const isExpRun   = job.pipeline === "exp_run";
        const device     = job.params?.compute_device as string | undefined;
        const deviceLabel = job.params?.compute_device_label as string | undefined;
        // Stall: running exp_run > 5min with 0 nodes completed
        const isStalled  = isRunning && isExpRun && elapsed !== null && elapsed > 300
          && nodesDone === 0 && nodeCount > 0;
        // Stuck-node detection
        const nowMs2 = Date.now();
        const tracker2 = nodesDoneTracker.current.get(job.id);
        if (!tracker2 || tracker2.done !== nodesDone) {
          nodesDoneTracker.current.set(job.id, { done: nodesDone, since: nowMs2 });
        }
        const stuckMs2 = tracker2 && tracker2.done === nodesDone ? nowMs2 - tracker2.since : 0;
        const nodeComputingLabel = isExpRun && isRunning && nodeCount > 0
          && stuckMs2 > 180_000 && etaSec !== null && elapsed !== null && etaSec > elapsed * 1.5
          ? `node ${nodesDone + 1}/${nodeCount} computing…`
          : null;
        return (
          <div key={job.id} style={{ borderBottom: "1px solid #1e293b" }}>
            {/* Clickable header row */}
            <div
              onClick={() => setExpandedId(isExpanded ? null : job.id)}
              style={{ padding: "8px 10px", cursor: "pointer", userSelect: "none",
                touchAction: "manipulation", WebkitTapHighlightColor: "transparent" }}
            >
              <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 3 }}>
                <span style={{ fontSize: 9, color: "#64748b", flexShrink: 0 }}>{isExpanded ? "▼" : "►"}</span>
                <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 3,
                  background: isStalled ? "rgba(220,38,38,0.2)" : (statusColor[job.status] ?? "#6b7280") + "25",
                  color: isStalled ? "#fca5a5" : (statusColor[job.status] ?? "#6b7280"),
                  fontWeight: 700 }}>
                  {isStalled ? "⚠ stalled" : job.status}
                </span>
                {device && (
                  <span style={{ fontSize: 9, padding: "1px 5px", borderRadius: 3,
                    background: device === "gpu" ? "#1e3a5f" : "#1e293b",
                    color: device === "gpu" ? "#60a5fa" : "#94a3b8",
                    fontWeight: 600, flexShrink: 0 }}>
                    {device === "gpu" ? `⚡ ${deviceLabel ?? "GPU"}` : `⚙ ${deviceLabel ?? "CPU"}`}
                  </span>
                )}
                <span style={{ flex: 1, fontWeight: 600, fontSize: 12, color: "#e2e8f0", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{job.name}</span>
                {elapsed !== null && (
                  <span style={{ fontSize: 10, color: "#64748b", flexShrink: 0 }}>
                    {fmtElapsed(elapsed)}
                    {nodeComputingLabel
                      ? ` / ${nodeComputingLabel}`
                      : etaSec !== null ? ` / ~${fmtElapsed(etaSec)} left` : ""}
                  </span>
                )}
                {(isRunning || job.status === "pending") && (
                  <>
                    <button
                      onClick={e => { e.stopPropagation(); handlePause(job.id); }}
                      disabled={pausing.has(job.id)}
                      style={{ padding: "2px 6px", border: "1px solid #d97706", borderRadius: 3,
                        background: "none", color: "#d97706", cursor: "pointer", fontSize: 9, flexShrink: 0 }}
                      title="Pause">
                      {pausing.has(job.id) ? "…" : "⏸"}
                    </button>
                    <button
                      onClick={e => { e.stopPropagation(); handleCancel(job.id); }}
                      disabled={cancelling.has(job.id)}
                      style={{ padding: "2px 7px", border: "1px solid #ef4444", borderRadius: 3,
                        background: "none", color: "#ef4444", cursor: "pointer", fontSize: 10, flexShrink: 0 }}
                      title="Abort">
                      {cancelling.has(job.id) ? "…" : "Abort"}
                    </button>
                  </>
                )}
                {job.status === "paused" && (
                  <button
                    onClick={e => { e.stopPropagation(); handleResume(job.id); }}
                    disabled={pausing.has(job.id)}
                    style={{ padding: "2px 6px", border: "1px solid #22c55e", borderRadius: 3,
                      background: "none", color: "#22c55e", cursor: "pointer", fontSize: 9, flexShrink: 0 }}
                    title="Resume">
                    {pausing.has(job.id) ? "…" : "▶"}
                  </button>
                )}
              </div>
              {/* Progress bar */}
              {isRunning && (
                <div style={{ height: 3, background: "#1e293b", borderRadius: 1, overflow: "hidden", marginBottom: 3 }}>
                  {pct !== null
                    ? <div style={{ height: "100%", width: `${pct}%`, background: isStalled ? "#dc2626" : "#2563eb", borderRadius: 1, transition: "width 0.6s ease" }} />
                    : <div style={{ height: "100%", background: isStalled ? "#dc2626" : "#2563eb", borderRadius: 1, animation: "progress 1.5s linear infinite", width: "30%" }} />
                  }
                </div>
              )}
              <div style={{ fontSize: 10, color: "#64748b", display: "flex", alignItems: "center", gap: 6 }}>
                <span>{job.pipeline} · {fmtDateTimeCompact(job.created_at)}</span>
                {isRunning && isExpRun && nodeCount > 0 && (
                  <span style={{ color: "#94a3b8", fontWeight: 600 }}>
                    {nodesDone}/{nodeCount} nodes{pct !== null ? ` (${pct}%)` : ""}
                  </span>
                )}
                {isStalled && (
                  <span style={{ color: "#f87171", fontWeight: 700 }}>
                    ⚠ no progress {Math.floor(elapsed! / 60)}min — consider aborting
                  </span>
                )}
              </div>
            </div>

            {/* Expanded details */}
            {isExpanded && (
              <div style={{ padding: "6px 12px 10px 28px", background: "#0a1020", borderTop: "1px solid #1e293b" }}>
                <div style={{ fontSize: 10, color: "#64748b", marginBottom: 4 }}>
                  <span style={{ color: "#94a3b8", fontWeight: 600 }}>Job ID:</span> {job.id}
                </div>
                <div style={{ fontSize: 10, color: "#64748b", marginBottom: 4 }}>
                  <span style={{ color: "#94a3b8", fontWeight: 600 }}>Pipeline:</span> {job.pipeline}
                </div>
                <div style={{ fontSize: 10, color: "#64748b", marginBottom: 6 }}>
                  <span style={{ color: "#94a3b8", fontWeight: 600 }}>Created:</span> {fmtDateTimeCompact(job.created_at)}
                </div>
                {/* View in Reports button for completed exp_run */}
                {job.status === "completed" && isExpRun && (
                  <button
                    onClick={e => { e.stopPropagation(); handleViewInReports((job.params?.exp_id as string) ?? ""); }}
                    style={{ padding: "3px 10px", marginBottom: 8, border: "none", borderRadius: 4,
                      background: "#059669", color: "#fff", cursor: "pointer", fontSize: 10, fontWeight: 600 }}>
                    📂 View in Reports
                  </button>
                )}
                {/* Error details button for failed jobs */}
                {job.status === "failed" && (
                  <button
                    onClick={e => { e.stopPropagation(); void handleShowError(job); }}
                    style={{ padding: "3px 10px", marginBottom: 8, border: "none", borderRadius: 4,
                      background: "#dc2626", color: "#fff", cursor: "pointer", fontSize: 10, fontWeight: 600 }}>
                    ⚠ View Error
                  </button>
                )}
                {errMsg && (
                  <div style={{ fontSize: 10, color: "#f87171", marginBottom: 6 }}>
                    <span style={{ fontWeight: 600 }}>Error:</span>{" "}
                    <span style={{ whiteSpace: "pre-wrap" }}>{errMsg}</span>
                  </div>
                )}
                {result && (
                  <div style={{ fontSize: 10, color: "#86efac" }}>
                    <div style={{ fontWeight: 600, color: "#94a3b8", marginBottom: 2 }}>Result summary:</div>
                    <pre style={{ background: "#0f172a", color: "#94a3b8", padding: "5px 8px", borderRadius: 4, overflow: "auto", maxHeight: 150, fontSize: 9, lineHeight: 1.5, margin: 0 }}>
                      {typeof result === "string" ? result : JSON.stringify(result, null, 2)}
                    </pre>
                  </div>
                )}
                {!result && !errMsg && (
                  <div style={{ fontSize: 10, color: "#475569", fontStyle: "italic" }}>
                    {job.status === "running" ? "Job is running — check Logs tab for live output." :
                     job.status === "pending"   ? "Job is queued — waiting for runner." :
                     job.status === "completed" ? "Completed — no detailed result stored." :
                     "No additional details available."}
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
      <style>{`@keyframes progress { 0%{transform:translateX(-100%)} 100%{transform:translateX(350%)} }`}</style>
      {/* Error modal */}
      {errorModal && (
        <JobErrorModal
          title={errorModal.title}
          message={errorModal.message}
          detail={errorModal.detail}
          params={errorModal.params}
          job={errorModal.job}
          onRetry={errorModal.onRetry}
          onClose={() => setErrorModal(null)}
        />
      )}
    </div>
  );
}

// ── Terminal Panel ────────────────────────────────────────────────────────────

const BUILTINS = [
  "ls", "ll", "la", "dir", "cat", "type", "head", "tail",
  "pwd", "cd", "echo", "mkdir", "rm", "rmdir", "cp", "mv",
  "find", "grep", "wc", "env", "which", "clear", "help",
  "python", "python3", "pip", "pip3", "setup",
];

function TerminalPanel() {
  const [, setEnvStatus] = useState<EnvStatus | null>(null);
  const [history, setHistory] = useState<{ text: string; type: "input" | "output" | "error" | "info" }[]>([
    { text: "Glossa Lab Terminal — Tab: autocomplete | pip/pip3: venv pip | setup: env status | help", type: "info" },
    { text: "─────────────────────────────────────────────────────────────────────────────", type: "info" },
  ]);

  // Load venv status on mount and add banner line
  useEffect(() => {
    getEnvStatus().then(s => {
      setEnvStatus(s);
      if (s.venv_exists) {
        setHistory(h => [...h, {
          text: `\u25cf venv active  Python ${s.python_version ?? "?"}  \u00b7  ${s.pkg_count} packages`,
          type: "info",
        }]);
      } else {
        setHistory(h => [
          ...h,
          { text: "\u26a0 No virtual environment found.", type: "error" },
          { text: "  Run 'setup' here or go to Settings \u2192 Python Environment.", type: "info" },
        ]);
      }
    }).catch(() => {});
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const [input, setInput] = useState("");
  const [cmdHistory, setCmdHistory] = useState<string[]>([]);
  const [cmdIdx, setCmdIdx] = useState(-1);
  const [running, setRunning] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  // Track last command + output for Ask AI
  const [lastCmd, setLastCmd] = useState("");
  const lastOutputRef = useRef<string[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { openChat } = useAIChat();

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "auto" }); }, [history]);

  const run = useCallback(async () => {
    const cmd = input.trim();
    if (!cmd) return;
    setHistory((h) => [...h, { text: `$ ${cmd}`, type: "input" }]);
    setCmdHistory((h) => [cmd, ...h.slice(0, 49)]);
    setCmdIdx(-1);
    setInput("");
    setSuggestions([]);
    setLastCmd(cmd);
    lastOutputRef.current = [];
    setRunning(true);

    try {
      const resp = await runTerminalCommand(cmd);
      if (!resp.body) { setHistory((h) => [...h, { text: "No response body", type: "error" }]); setRunning(false); return; }
      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const parts = buf.split("\n\n");
        buf = parts.pop() ?? "";
        for (const part of parts) {
          for (const ln of part.split("\n")) {
            if (ln.startsWith("data: ")) {
              try {
                const d = JSON.parse(ln.slice(6)) as { text?: string; return_code?: number; message?: string };
                if (d.text !== undefined) {
                  const line = stripAnsi(d.text!);
                  setHistory((h) => [...h, { text: line, type: "output" }]);
                  lastOutputRef.current = [...lastOutputRef.current.slice(-29), line];
                }
                // Never show exit code — real terminals don't display them.
                // Only surface actual error messages from the shell.
                if (d.message)
                  setHistory((h) => [...h, { text: `Error: ${d.message}`, type: "error" }]);
              } catch { /* ignore */ }
            }
          }
        }
      }
    } catch (e) {
      setHistory((h) => [...h, { text: `Error: ${e instanceof Error ? e.message : String(e)}`, type: "error" }]);
    } finally {
      setRunning(false);
      // setTimeout lets React finish re-rendering (disabled→enabled) before focus
      setTimeout(() => inputRef.current?.focus(), 0);
    }
  }, [input]);

  const handleKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") { run(); return; }
    if (e.key === "Tab") {
      e.preventDefault();
      const prefix = input.trim();
      // Build unique candidate list: builtins + cmd history that start with prefix
      const all = [...BUILTINS, ...cmdHistory].filter(
        (c, i, arr) => c.startsWith(prefix) && arr.indexOf(c) === i
      );
      if (all.length === 0) return;
      if (all.length === 1) { setInput(all[0] + " "); setSuggestions([]); return; }
      setSuggestions(all);
      // Cycle: each Tab press advances through matches
      const cur = suggestions.indexOf(input);
      setInput(all[(cur + 1) % all.length]);
      return;
    }
    // Any other key clears suggestions
    if (e.key !== "ArrowUp" && e.key !== "ArrowDown") setSuggestions([]);
    if (e.key === "ArrowUp") {
      e.preventDefault();
      const idx = Math.min(cmdIdx + 1, cmdHistory.length - 1);
      setCmdIdx(idx);
      if (cmdHistory[idx]) setInput(cmdHistory[idx]);
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      const idx = Math.max(cmdIdx - 1, -1);
      setCmdIdx(idx);
      setInput(idx === -1 ? "" : (cmdHistory[idx] ?? ""));
    }
  };

  const lineColor: Record<string, string> = {
    input: "#86efac", output: "#e2e8f0", error: "#f87171", info: "#94a3b8",
  };

  // ── Right-click context menu ──────────────────────────────────────
  const [ctxMenu, setCtxMenu] = useState<{ x: number; y: number } | null>(null);
  const outputDivRef = useRef<HTMLDivElement>(null);

  const handleContextMenu = (e: React.MouseEvent) => {
    e.preventDefault();
    setCtxMenu({ x: e.clientX, y: e.clientY });
  };

  useEffect(() => {
    const close = () => setCtxMenu(null);
    document.addEventListener("click", close);
    document.addEventListener("keydown", close);
    return () => { document.removeEventListener("click", close); document.removeEventListener("keydown", close); };
  }, []);

  const ctxCopy = () => {
    const sel = window.getSelection()?.toString();
    if (sel) navigator.clipboard.writeText(sel);
    setCtxMenu(null);
  };
  const ctxCopyAll = () => {
    const text = history.map(l => l.text).join("\n");
    navigator.clipboard.writeText(text);
    setCtxMenu(null);
  };
  const ctxPaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setInput(prev => prev + text);
      inputRef.current?.focus();
    } catch { /* clipboard permission denied */ }
    setCtxMenu(null);
  };
  const ctxSelectAll = () => {
    if (outputDivRef.current) {
      const range = document.createRange();
      range.selectNodeContents(outputDivRef.current);
      const sel = window.getSelection();
      sel?.removeAllRanges();
      sel?.addRange(range);
    }
    setCtxMenu(null);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", position: "relative" }}
      onClick={() => {
        // Don't steal focus (and thus clear selection) when the user has text selected
        if (!ctxMenu && !window.getSelection()?.toString()) inputRef.current?.focus();
      }}>
      {/* Toolbar */}
      <div style={{ display: "flex", gap: 4, padding: "2px 8px", borderBottom: "1px solid #0f172a", alignItems: "center", flexShrink: 0 }}>
        <button onClick={() => { setInput("help"); setTimeout(() => run(), 0); }}
          title="Show available commands"
          style={tBtn}>? help</button>
        <button onClick={() => { setHistory([]); setSuggestions([]); }}
          title="Clear terminal"
          style={tBtn}>✕ clear</button>
        {lastCmd && !running && (
          <button
            onClick={() => openChat({ initialPrompt: `I ran this terminal command:\n\`${lastCmd}\`\n\nOutput:\n\`\`\`\n${lastOutputRef.current.slice(0, 25).join("\n")}\n\`\`\`\n\nCan you help me understand or debug this?` })}
            title="Ask Glossa AI about this command and output"
            style={{ ...tBtn, color: "#c4b5fd" }}>✨ Ask AI</button>
        )}
        <div style={{ flex: 1 }} />
        <span style={{ fontSize: 9, color: "#334155" }}>Right-click to copy</span>
      </div>

      {/* Output — userSelect:text so text is selectable */}
      <div
        ref={outputDivRef}
        onContextMenu={handleContextMenu}
        style={{ flex: 1, overflowY: "auto", fontFamily: "monospace", fontSize: 11,
          padding: "4px 8px", lineHeight: 1.6, userSelect: "text", cursor: "text" }}>
        {history.map((item, i) => (
          <div key={i} style={{ color: lineColor[item.type], whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{item.text}</div>
        ))}
        {running && <div style={{ color: "#d97706" }}>▌ running…</div>}
        <div ref={bottomRef} />
      </div>

      {/* Context menu */}
      {ctxMenu && (
        <div
          style={{ position: "fixed", left: ctxMenu.x, top: ctxMenu.y, zIndex: 9999,
            background: "#1e293b", border: "1px solid #334155", borderRadius: 5,
            boxShadow: "0 4px 16px rgba(0,0,0,0.4)", minWidth: 160, overflow: "hidden" }}
          onClick={e => e.stopPropagation()}>
          {([
            { label: "⧸ Copy selection", action: ctxCopy },
            { label: "⧹ Copy all output", action: ctxCopyAll },
            { label: "⋮ Paste into input", action: ctxPaste },
            { label: "Select all output", action: ctxSelectAll },
            null,
            { label: "✕ Clear terminal", action: () => { setHistory([]); setSuggestions([]); setCtxMenu(null); } },
          ] as ({ label: string; action: () => void } | null)[]).map((item, i) =>
            item === null
              ? <div key={i} style={{ height: 1, background: "#334155", margin: "2px 0" }} />
              : <button key={i} onClick={item.action}
                  style={{ display: "block", width: "100%", padding: "6px 12px", border: "none",
                    background: "none", color: "#e2e8f0", cursor: "pointer", fontSize: 11,
                    textAlign: "left" }}
                  onMouseEnter={e => (e.currentTarget.style.background = "rgba(96,165,250,0.15)")}
                  onMouseLeave={e => (e.currentTarget.style.background = "none")}>
                  {item.label}
                </button>
          )}
        </div>
      )}

      {/* Suggestion bar */}
      {suggestions.length > 0 && (
        <div style={{ display: "flex", gap: 4, padding: "2px 8px", flexWrap: "wrap", borderTop: "1px solid #1e293b", background: "#0f172a" }}>
          {suggestions.map(s => (
            <button key={s} onClick={() => { setInput(s + " "); setSuggestions([]); inputRef.current?.focus(); }}
              style={{ padding: "0 5px", background: "#1e293b", border: "none", borderRadius: 3, color: s === input ? "#60a5fa" : "#94a3b8", cursor: "pointer", fontSize: 10, fontFamily: "monospace" }}>
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input row */}
      <div style={{ display: "flex", alignItems: "center", padding: "4px 8px", borderTop: "1px solid #1e293b", gap: 4 }}>
        <span style={{ color: "#86efac", fontSize: 11, fontFamily: "monospace" }}>$</span>
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => { setInput(e.target.value); if (suggestions.length) setSuggestions([]); }}
          onKeyDown={handleKey}
          disabled={running}
          placeholder="Enter command… (Tab: autocomplete)"
          style={{ flex: 1, background: "transparent", border: "none", outline: "none", color: "#e2e8f0", fontSize: 11, fontFamily: "monospace", caretColor: "#86efac" }}
          autoFocus
        />
        {running && <span style={{ color: "#d97706", fontSize: 10 }}>running…</span>}
      </div>
    </div>
  );
}

const tBtn: React.CSSProperties = { padding: "1px 6px", background: "none", border: "1px solid #1e293b", borderRadius: 3, color: "#64748b", cursor: "pointer", fontSize: 10, fontFamily: "monospace" };

// ── Main BottomPanel ──────────────────────────────────────────────────────────

interface BottomPanelProps {
  height: number;
  onHeightChange: (h: number) => void;
  minimized: boolean;
  onMinimizedChange: (v: boolean) => void;
  activeTab: PanelTab;
  onTabChange: (t: PanelTab) => void;
  leftOffset?: number;
  /** Number of active (pending/running) jobs — drives the Jobs tab dot. */
  activeJobCount?: number;
}

export function BottomPanel({ height, onHeightChange, minimized, onMinimizedChange, activeTab, onTabChange, leftOffset = 0, activeJobCount = 0 }: BottomPanelProps) {
  const [maximized, setMaximized] = useState(false);
  const dragging = useRef(false);
  const dragStartY = useRef(0);
  const dragStartH = useRef(0);
  const { isOpen: chatOpen, isDocked } = useAIChat();

  const TABS: Array<{ id: PanelTab; label: string; icon: string }> = [
    { id: "logs", label: "Logs", icon: "📋" },
    { id: "jobs", label: "Jobs", icon: "📦" },
    { id: "terminal", label: "Terminal", icon: ">_" },
    ...(isDocked && chatOpen ? [{ id: "chat" as PanelTab, label: "AI Chat", icon: "✨" }] : []),
  ];

  // Drag-resize
  const onDragStart = useCallback((e: React.MouseEvent) => {
    dragging.current = true;
    dragStartY.current = e.clientY;
    dragStartH.current = height;
    e.preventDefault();
  }, [height]);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!dragging.current) return;
      const delta = dragStartY.current - e.clientY;
      const newH = Math.max(MIN_HEIGHT, Math.min(window.innerHeight * MAX_HEIGHT_RATIO, dragStartH.current + delta));
      onHeightChange(newH);
      if (minimized && delta > 20) onMinimizedChange(false);
    };
    const onUp = () => { dragging.current = false; };
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    return () => { window.removeEventListener("mousemove", onMove); window.removeEventListener("mouseup", onUp); };
  }, [height, minimized, onHeightChange, onMinimizedChange]);

  const isMobilePanel = typeof window !== "undefined" && window.innerWidth <= 768;
  const panelH = maximized
    ? Math.floor(window.innerHeight * MAX_HEIGHT_RATIO)
    : minimized ? 30 : height;
  const TAB_BAR_H = isMobilePanel ? 36 : 30;

  return (
    <div className="glossa-bottom-panel" style={{
      position: "fixed", bottom: 0, left: leftOffset, right: 0,
      height: panelH, background: "#0f172a", borderTop: "1px solid #1e293b",
      display: "flex", flexDirection: "column", zIndex: 5000, userSelect: "none",
    }}>
      {/* Drag handle */}
      {!minimized && !maximized && (
        <div
          onMouseDown={onDragStart}
          style={{ height: 4, cursor: "ns-resize", background: "transparent", flexShrink: 0 }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLDivElement).style.background = "#334155"; }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = "transparent"; }}
        />
      )}

      {/* Tab bar */}
      <div style={{ display: "flex", alignItems: "center", height: TAB_BAR_H, flexShrink: 0, borderBottom: minimized ? "none" : "1px solid #1e293b", paddingLeft: 6 }}>
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => { onTabChange(tab.id); if (minimized) onMinimizedChange(false); }}
            style={{
              padding: "4px 12px", border: "none", borderBottom: activeTab === tab.id && !minimized ? "2px solid #3b82f6" : "2px solid transparent",
              background: "none", cursor: "pointer", fontSize: 11, fontWeight: activeTab === tab.id ? 600 : 400,
              color: activeTab === tab.id ? "#e2e8f0" : "#64748b",
              display: "flex", alignItems: "center", gap: 4, height: "100%",
            }}
          >
            <span style={{ fontSize: 10 }}>{tab.icon}</span>
            {tab.label}
            {/* Activity dot: pulsing blue for active jobs */}
            {tab.id === "jobs" && activeJobCount > 0 && (
              <span
                style={{
                  width: 6, height: 6, borderRadius: "50%",
                  background: "#3b82f6",
                  boxShadow: "0 0 6px #3b82f6",
                  animation: "healthPulse 0.7s ease-in-out infinite",
                  flexShrink: 0, marginLeft: 2,
                }}
                title={`${activeJobCount} active job(s)`}
              />
            )}
          </button>
        ))}
        <div style={{ flex: 1 }} />
        {/* Panel controls */}
        <button onClick={() => { setMaximized(false); onMinimizedChange(!minimized); }}
          title={minimized ? "Restore" : "Minimize"}
          style={{ padding: "5px 18px", border: "none", background: "none", color: "#94a3b8",
            cursor: "pointer", fontSize: 14, height: "100%", display: "flex", alignItems: "center" }}>
          {minimized ? "▲" : "▼"}
        </button>
        <button onClick={() => { setMaximized(!maximized); if (minimized) onMinimizedChange(false); }}
          title={maximized ? "Restore" : "Maximize"}
          style={{ padding: "5px 12px", border: "none", background: "none", color: "#64748b",
            cursor: "pointer", fontSize: 11, height: "100%", display: "flex", alignItems: "center" }}>
          {maximized ? "⊟" : "⊞"}
        </button>
      </div>

      {/* Content — always mount all tabs to preserve state; hide inactive with display:none */}
      {!minimized && (
        <div style={{ flex: 1, overflow: "hidden", position: "relative" }}>
          <div style={{ display: activeTab === "logs"     ? "flex" : "none", flexDirection: "column", height: "100%", userSelect: "text" }}><LogPanel /></div>
          <div style={{ display: activeTab === "jobs"     ? "flex" : "none", flexDirection: "column", height: "100%", userSelect: "text" }}><JobsPanel /></div>
          <div style={{ display: activeTab === "terminal" ? "flex" : "none", flexDirection: "column", height: "100%" }}><TerminalPanel /></div>
          <div style={{ display: activeTab === "chat"     ? "flex" : "none", flexDirection: "column", height: "100%", userSelect: "text" }}><ChatInline /></div>
        </div>
      )}
      <style>{`@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }`}</style>
    </div>
  );
}
