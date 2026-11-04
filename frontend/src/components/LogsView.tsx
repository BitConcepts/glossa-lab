/**
 * LogsView — the Logs screen (Spec 087 Stage S5, T502; claims
 * C087-10, C087-11).
 *
 * Restores the log viewer Spec 081 removed, built to the
 * owner-approved wireframes in
 * specs/087-node-system-tightening/records/logs-view-wireframes/
 * (Q1: Logs is its own tab in the Tool home group, between Jobs
 * and Status; Q2: the purge control ships behind its
 * confirmation). No new backend: the stream tab reads the
 * terminal-log endpoints that stayed live (GET /terminal/log,
 * GET /terminal/log/stream, POST /terminal/log/purge), and the
 * records tab reads the durable record tables through the
 * existing API surface (jobs + GET /jobs/{id}/results,
 * GET /phase/actions, GET /notifications/log).
 *
 * Two standing lessons are built in from birth:
 *  - a failed fetch renders a named error state with retry
 *    (Stage S1 / audit F5) — never a silently empty surface;
 *  - the SSE tail is fetch-streamed with the stored token,
 *    never EventSource (Spec 082).
 *
 * The records tab is read-only: Jobs remains the surface that
 * acts on records. The events bus is a live-notification
 * channel with no delivery guarantee (decision D2,
 * documented-ephemeral) — nothing that must survive is carried
 * only by it; the records tab is where durable history lives.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  getJobResults,
  getLog,
  listJobs,
  listNotificationLog,
  listPhaseActions,
  listReports,
  purgeLog,
  streamLogLines,
  type JobResponse,
  type NotificationLogEntry,
  type PhaseAction,
} from "../api";
import { fmtDuration } from "../dateFormat";
import { Card, PageHead, palette, SmallButton, TabsRow, type Palette } from "./ui081";

type LogsTab = "stream" | "records";
const TABS: { id: LogsTab; label: string }[] = [
  { id: "stream", label: "Live stream" },
  { id: "records", label: "Job & phase records" },
];

const MAX_STREAM_LINES = 5000; // viewer bound; the file itself is untouched

// ── Log line parsing ────────────────────────────────────────────────────────

interface ParsedLine {
  raw: string;
  ts: string;
  level: string; // DEBUG | INFO | WARNING | ERROR | CRITICAL | ""
  module: string;
  message: string;
}

function parseLogLine(raw: string): ParsedLine {
  try {
    const obj = JSON.parse(raw) as Record<string, unknown>;
    if (obj && typeof obj === "object" && ("message" in obj || "level" in obj)) {
      // The file carries two level vocabularies: backend lines use
      // WARNING, the frontend error intake writes WARN. One level,
      // rendered and filtered under the wireframe's name.
      const rawLevel = String(obj.level ?? "").toUpperCase();
      return {
        raw,
        ts: String(obj.timestamp ?? ""),
        level: rawLevel === "WARN" ? "WARNING" : rawLevel,
        module: String(obj.module ?? obj.name ?? ""),
        message: String(obj.message ?? ""),
      };
    }
  } catch {
    /* not a JSON line — render raw */
  }
  return { raw, ts: "", level: "", module: "", message: raw };
}

/** Append `incoming` to `existing`, dropping the overlap where the
 *  stream's backfill repeats the tail of the first load. Finds the
 *  largest k with suffix(existing, k) == prefix(incoming, k). */
function mergeLogLines(existing: string[], incoming: string[]): string[] {
  if (incoming.length === 0) return existing;
  if (existing.length === 0) return incoming.slice(-MAX_STREAM_LINES);
  const maxK = Math.min(existing.length, incoming.length);
  let overlap = 0;
  for (let k = maxK; k > 0; k--) {
    let ok = true;
    for (let i = 0; i < k; i++) {
      if (existing[existing.length - k + i] !== incoming[i]) { ok = false; break; }
    }
    if (ok) { overlap = k; break; }
  }
  return [...existing, ...incoming.slice(overlap)].slice(-MAX_STREAM_LINES);
}

const LEVELS = ["ALL", "DEBUG", "INFO", "WARNING", "ERROR"] as const;
type LevelFilter = (typeof LEVELS)[number];

function levelMatches(lineLevel: string, filter: LevelFilter): boolean {
  if (filter === "ALL") return true;
  if (filter === "ERROR") return lineLevel === "ERROR" || lineLevel === "CRITICAL";
  return lineLevel === filter;
}

function levelColor(level: string): string {
  switch (level) {
    case "DEBUG": return "#94a3b8";
    case "INFO": return "#7dd3fc";
    case "WARNING": return "#fbbf24";
    case "ERROR":
    case "CRITICAL": return "#f87171";
    default: return "#dbe7f5";
  }
}

// ── Stream tab ──────────────────────────────────────────────────────────────

interface FileState {
  exists: boolean;
  totalLines?: number;
  file?: string;
}

function StreamTab({ p, onOpenStatus }: { p: Palette; onOpenStatus: () => void }) {
  const [rawLines, setRawLines] = useState<string[]>([]);
  const [fileState, setFileState] = useState<FileState | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [live, setLive] = useState(false);
  const [paused, setPaused] = useState(false);
  const [level, setLevel] = useState<LevelFilter>("ALL");
  const [retryNonce, setRetryNonce] = useState(0);
  const [confirmingPurge, setConfirmingPurge] = useState(false);
  const [purgeBusy, setPurgeBusy] = useState(false);
  const [purgeNote, setPurgeNote] = useState<string | null>(null);
  const pausedRef = useRef(false);
  const pendingRef = useRef<string[]>([]);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  const appendLive = useCallback((texts: string[]) => {
    if (texts.length === 0) return;
    if (pausedRef.current) {
      pendingRef.current.push(...texts);
      return;
    }
    setRawLines((prev) => [...prev, ...texts].slice(-MAX_STREAM_LINES));
  }, []);

  useEffect(() => {
    pausedRef.current = paused;
    if (!paused && pendingRef.current.length > 0) {
      const pending = pendingRef.current;
      pendingRef.current = [];
      setRawLines((prev) => [...prev, ...pending].slice(-MAX_STREAM_LINES));
    }
  }, [paused]);

  useEffect(() => {
    const ctl = new AbortController();
    let cancelled = false;
    (async () => {
      let first: Awaited<ReturnType<typeof getLog>>;
      try {
        first = await getLog(200);
      } catch (err) {
        if (!cancelled) {
          setLoadError(err instanceof Error ? err.message : String(err));
        }
        return;
      }
      if (cancelled) return;
      setLoadError(null);
      setRawLines(first.lines);
      setFileState({
        exists: first.exists,
        totalLines: first.total_lines,
        file: (first as { file?: string }).file,
      });
      // SSE tail. The endpoint backfills the last 100 lines first;
      // buffer them and merge once, so the first load is not doubled.
      let backfill: string[] = [];
      let flushed = false;
      const flushBackfill = () => {
        if (flushed) return;
        flushed = true;
        if (backfill.length > 0) {
          const buffered = backfill;
          backfill = [];
          setRawLines((prev) => mergeLogLines(prev, buffered));
        }
      };
      try {
        setLive(true);
        for await (const ev of streamLogLines(ctl.signal)) {
          if (ev.backfill && !flushed) {
            backfill.push(ev.text);
            if (backfill.length >= 100) flushBackfill();
            continue;
          }
          flushBackfill();
          appendLive([ev.text]);
        }
      } catch {
        /* stream ended or was refused — the fetched lines remain */
      }
      if (!cancelled) setLive(false);
    })();
    return () => {
      cancelled = true;
      ctl.abort();
    };
  }, [retryNonce, appendLive]);

  const parsed = useMemo(() => rawLines.map(parseLogLine), [rawLines]);
  const shown = useMemo(
    () => parsed.filter((l) => levelMatches(l.level, level)),
    [parsed, level],
  );

  useEffect(() => {
    const el = scrollRef.current;
    if (el && !paused) el.scrollTop = el.scrollHeight;
  }, [shown, paused]);

  const openPurgeConfirm = async () => {
    setPurgeNote(null);
    setConfirmingPurge(true);
    try {
      const fresh = await getLog(1);
      setFileState({
        exists: fresh.exists,
        totalLines: fresh.total_lines,
        file: (fresh as { file?: string }).file,
      });
    } catch {
      /* keep the last known count; the confirmation names it as such */
    }
  };

  const doPurge = async () => {
    setPurgeBusy(true);
    try {
      const res = await purgeLog();
      setRawLines([]);
      pendingRef.current = [];
      setConfirmingPurge(false);
      setPurgeNote(
        `Log purged: ${res.file.split(/[\\/]/).pop() ?? res.file} truncated ` +
        `(${res.cleared.toLocaleString()} bytes cleared; rotated backups deleted).`,
      );
      const fresh = await getLog(200);
      setRawLines(fresh.lines);
      setFileState({
        exists: fresh.exists,
        totalLines: fresh.total_lines,
        file: (fresh as { file?: string }).file,
      });
    } catch (err) {
      setPurgeNote(`Purge failed: ${err instanceof Error ? err.message : String(err)}`);
      setConfirmingPurge(false);
    } finally {
      setPurgeBusy(false);
    }
  };

  const downloadTail = () => {
    const tail = rawLines.slice(-200).join("\n") + "\n";
    const url = URL.createObjectURL(new Blob([tail], { type: "text/plain" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = "glossa-log-tail.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  const fileName = fileState?.file
    ? fileState.file.split(/[\\/]/).pop()
    : "glossa.log";

  if (loadError) {
    return (
      <Card p={p}>
        <div data-testid="logs-error" role="alert">
          <div style={{ fontWeight: 700, color: p.bad, marginBottom: 6 }}>
            Log failed to load
          </div>
          <div style={{ color: p.muted, fontSize: 13, marginBottom: 12 }}>
            The first load from <code>GET /terminal/log</code> failed: {loadError}.
            The stream was not opened. This is a load failure, not an empty log.
          </div>
          <SmallButton primary onClick={() => setRetryNonce((n) => n + 1)}>
            Retry
          </SmallButton>
        </div>
      </Card>
    );
  }

  return (
    <div>
      <Card p={p} style={{ marginBottom: 14 }}>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
          <span style={{ fontSize: 13 }}>
            <span
              aria-hidden
              style={{
                display: "inline-block", width: 8, height: 8, borderRadius: "50%",
                background: live ? "#22c55e" : "#94a3b8", marginRight: 6, verticalAlign: 1,
              }}
            />
            <b>{live ? "Live" : "Not live"}</b>
            {" · tailing "}
            <code>glossa.log</code>
            {" via "}
            <code>/terminal/log/stream</code> (SSE)
            {paused && " · paused"}
          </span>
          <div style={{ flex: 1 }} />
          <SmallButton onClick={() => setPaused((v) => !v)}>
            {paused ? "Resume" : "Pause"}
          </SmallButton>
          <SmallButton onClick={downloadTail}>Download last 200 lines</SmallButton>
          <button
            onClick={openPurgeConfirm}
            style={{
              display: "inline-flex", alignItems: "center", padding: "5px 10px",
              borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: "pointer",
              border: "1px solid #fca5a5", background: "#fff", color: "#b91c1c", minHeight: 32,
            }}
          >
            Purge log…
          </button>
        </div>
        <div style={{ borderTop: `1px solid ${p.borderSoft}`, margin: "12px 0" }} />
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center" }}>
          <span style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: "0.06em", color: p.muted }}>
            Level
          </span>
          {LEVELS.map((lv) => (
            <button
              key={lv}
              onClick={() => setLevel(lv)}
              aria-pressed={level === lv}
              style={{
                fontSize: 11.5, fontWeight: 600, padding: "2px 10px", borderRadius: 20,
                border: `1px solid ${level === lv ? "#1e3a5f" : p.border}`,
                background: level === lv ? "#1e3a5f" : p.card,
                color: level === lv ? "#fff" : p.fg, cursor: "pointer",
              }}
            >
              {lv === "ALL" ? "All" : lv}
            </button>
          ))}
          <div style={{ flex: 1 }} />
          <span style={{ fontSize: 12.5, color: p.muted }}>
            File: <code>{fileName}</code>
            {fileState
              ? fileState.exists
                ? ` · exists · ${(fileState.totalLines ?? 0).toLocaleString()} lines`
                : " · does not exist yet"
              : ""}
            {" · rotates at 10 MB × 5 backups · first load: last 200 lines ("}
            <code>GET /terminal/log?lines=200</code>)
          </span>
        </div>
      </Card>

      {confirmingPurge && (
        <div
          data-testid="purge-confirm"
          style={{
            border: "1px solid #fca5a5", background: "#fef2f2", borderRadius: 10,
            padding: "14px 16px", marginBottom: 14, fontSize: 13.5, color: "#7f1d1d",
          }}
        >
          <b>Purge confirmation.</b> Purge clears the current log file through{" "}
          <code>POST /terminal/log/purge</code>: <code>{fileName}</code> is truncated
          and its rotated backups (<code>{fileName}.1</code> …) are deleted. This
          cannot be undone.{" "}
          <button
            onClick={doPurge}
            disabled={purgeBusy}
            style={{
              padding: "5px 10px", borderRadius: 8, fontSize: 12, fontWeight: 700,
              border: "1px solid #fca5a5", background: "#fff", color: "#b91c1c",
              cursor: purgeBusy ? "default" : "pointer", opacity: purgeBusy ? 0.55 : 1,
            }}
          >
            Purge {(fileState?.totalLines ?? 0).toLocaleString()} lines
          </button>{" "}
          <SmallButton onClick={() => setConfirmingPurge(false)}>Cancel</SmallButton>
        </div>
      )}
      {purgeNote && (
        <div style={{ fontSize: 13, color: p.muted, marginBottom: 12 }}>{purgeNote}</div>
      )}

      <div
        ref={scrollRef}
        data-testid="log-stream"
        style={{
          background: "#0f172a", color: "#dbe7f5", borderRadius: 10,
          padding: "14px 16px", fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
          fontSize: 12, lineHeight: 1.75, maxHeight: 560, overflowY: "auto",
        }}
      >
        {shown.length === 0 && (
          <div style={{ color: "#7d93b2" }}>
            {rawLines.length === 0
              ? "No log lines yet."
              : "No lines at this level."}
          </div>
        )}
        {shown.map((line, i) => (
          <div key={i} style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
            {line.ts && <span style={{ color: "#7d93b2" }}>{line.ts} </span>}
            {line.level && (
              <span style={{ color: levelColor(line.level), fontWeight: 700 }}>
                {line.level}{" "}
              </span>
            )}
            {line.module && <span style={{ color: "#a5b4fc" }}>{line.module} — </span>}
            <span>{line.message}</span>
          </div>
        ))}
      </div>
      <div style={{ fontSize: 12.5, color: p.muted, marginTop: 10 }}>
        Watching from inside the app: the Status view is the health surface —{" "}
        <button
          onClick={onOpenStatus}
          style={{ background: "none", border: "none", color: p.accent, cursor: "pointer", fontSize: 12.5, padding: 0 }}
        >
          Open Status
        </button>
      </div>
    </div>
  );
}

// ── Records tab ─────────────────────────────────────────────────────────────

type KindId = "graph" | "pipeline" | "study" | "phase" | "notification" | "other";
type StatusFilter = "ANY" | "COMPLETED" | "FAILED" | "RUNNING";

interface LogRecord {
  key: string;
  ts: string;
  title: string;
  sub: string;
  kind: KindId;
  kindLabel: string;
  status: string;
  durationS: number | null;
  summary: string;
  job?: JobResponse;
  action?: PhaseAction;
  notification?: NotificationLogEntry;
}

const KIND_FILTERS: { id: KindId | "ALL"; label: string }[] = [
  { id: "ALL", label: "All records" },
  { id: "graph", label: "Experiment graphs" },
  { id: "pipeline", label: "Pipelines" },
  { id: "study", label: "Studies" },
  { id: "phase", label: "Phase actions" },
  { id: "notification", label: "Notifications" },
];

const STATUS_FILTERS: { id: StatusFilter; label: string }[] = [
  { id: "ANY", label: "Any status" },
  { id: "COMPLETED", label: "Completed" },
  { id: "FAILED", label: "Failed" },
  { id: "RUNNING", label: "Running" },
];

function jobKind(job: JobResponse): { id: KindId; label: string } {
  if (job.id.endsWith("-graph-run")) return { id: "graph", label: "Experiment graph" };
  if (job.id.endsWith("-pipeline-run")) return { id: "pipeline", label: "Pipeline" };
  if (job.id.endsWith("-study-run")) return { id: "study", label: "Study" };
  if (job.pipeline === "exp_run") return { id: "graph", label: "Experiment graph" };
  return { id: "other", label: job.pipeline || "Job" };
}

function statusMatches(status: string, filter: StatusFilter): boolean {
  const s = status.toLowerCase();
  switch (filter) {
    case "ANY": return true;
    case "COMPLETED": return s === "completed" || s === "sent";
    case "FAILED": return s === "failed";
    case "RUNNING": return s === "running" || s === "pending";
  }
}

function durationSeconds(from: string | null, to: string | null): number | null {
  if (!from || !to) return null;
  const a = Date.parse(from);
  const b = Date.parse(to);
  if (Number.isNaN(a) || Number.isNaN(b)) return null;
  return Math.max(0, (b - a) / 1000);
}

function fmtUtc(ts: string): string {
  const d = new Date(ts);
  if (Number.isNaN(d.getTime())) return ts;
  return d.toISOString().slice(0, 19).replace("T", " ");
}

function fmtSecs(s: number | null): string {
  if (s === null) return "—";
  if (s < 60) return `${s.toFixed(1)}s`;
  return fmtDuration(s);
}

function statusColor(status: string): string {
  const s = status.toLowerCase();
  if (s === "completed" || s === "sent") return "#15803d";
  if (s === "failed") return "#b91c1c";
  if (s === "running") return "#1d4ed8";
  return "#64748b";
}

/** Same redaction rule as the backend's mask_email
 *  (glossa_lab.notifications.smtp): first local character +
 *  "***@" + domain. The /notifications/log endpoint returns the
 *  stored address; this view never displays it unmasked. */
function maskEmail(addr: string): string {
  if (!addr) return addr;
  const at = addr.indexOf("@");
  if (at < 0) return addr;
  const local = addr.slice(0, at);
  if (!local) return addr;
  return `${local[0]}***@${addr.slice(at + 1)}`;
}

function excerpt(text: string, max = 1200): string {
  return text.length > max ? `${text.slice(0, max)}\n… (excerpt)` : text;
}

function RecordsTab({ p }: { p: Palette }) {
  const [records, setRecords] = useState<LogRecord[] | null>(null);
  const [jobsTotal, setJobsTotal] = useState(0);
  const [jobsCompleted, setJobsCompleted] = useState(0);
  const [reportsCount, setReportsCount] = useState<number | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [retryNonce, setRetryNonce] = useState(0);
  const [kindFilter, setKindFilter] = useState<KindId | "ALL">("ALL");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("ANY");
  const [expanded, setExpanded] = useState<string | null>(null);
  const [resultsByJob, setResultsByJob] = useState<
    Record<string, { state: "loading" | "ok" | "none" | "error"; text?: string }>
  >({});

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [jobs, phaseRes, notifRes] = await Promise.all([
          listJobs(),
          listPhaseActions(),
          listNotificationLog(100),
        ]);
        if (cancelled) return;
        if (phaseRes.error) throw new Error(phaseRes.error);
        const recs: LogRecord[] = [];
        for (const job of jobs) {
          const kind = jobKind(job);
          recs.push({
            key: `job:${job.id}`,
            ts: job.created_at,
            title: job.name,
            sub: `job ${job.id}`,
            kind: kind.id,
            kindLabel: kind.label,
            status: job.status,
            durationS: durationSeconds(job.created_at, job.updated_at),
            summary:
              job.status === "completed"
                ? `Pipeline ${job.pipeline}; result stored in job_results.`
                : `Pipeline ${job.pipeline}; status ${job.status}.`,
            job,
          });
        }
        for (const action of phaseRes.actions) {
          recs.push({
            key: `phase:${action.id}`,
            ts: action.started_at ?? action.created_at,
            title: `Phase action — ${action.action_label}`,
            sub: `phase_actions · phase ${action.phase}${action.job_id ? ` · job ${action.job_id}` : ""}`,
            kind: "phase",
            kindLabel: "Phase action",
            status: action.status,
            durationS: durationSeconds(action.started_at, action.completed_at),
            summary: action.error_message
              ? `error_message: ${action.error_message}`
              : `${action.action_type || "action"} · phase ${action.phase}`,
            action,
          });
        }
        for (const entry of notifRes.entries) {
          recs.push({
            key: `notif:${entry.id}`,
            ts: entry.sent_at,
            title: `Notification — ${entry.subject || entry.kind || "notification"}`,
            sub: "notification_log",
            kind: "notification",
            kindLabel: "Notification",
            status: entry.status,
            durationS: null,
            summary: entry.error
              ? `error: ${entry.error}`
              : `${entry.item_count} item${entry.item_count === 1 ? "" : "s"} · recipient masked`,
            notification: entry,
          });
        }
        recs.sort((a, b) => (a.ts < b.ts ? 1 : a.ts > b.ts ? -1 : 0));
        setRecords(recs);
        setJobsTotal(jobs.length);
        setJobsCompleted(jobs.filter((j) => j.status === "completed").length);
        setLoadError(null);
      } catch (err) {
        if (!cancelled) {
          setLoadError(err instanceof Error ? err.message : String(err));
        }
      }
      try {
        const reports = await listReports();
        if (!cancelled) setReportsCount(reports.length);
      } catch {
        /* the census clause is omitted when the count cannot be read */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [retryNonce]);

  const toggleExpand = (rec: LogRecord) => {
    const next = expanded === rec.key ? null : rec.key;
    setExpanded(next);
    if (next && rec.job && rec.job.status === "completed" && !resultsByJob[rec.job.id]) {
      const jobId = rec.job.id;
      setResultsByJob((prev) => ({ ...prev, [jobId]: { state: "loading" } }));
      getJobResults(jobId)
        .then((data) => {
          setResultsByJob((prev) => ({
            ...prev,
            [jobId]: { state: "ok", text: excerpt(JSON.stringify(data, null, 2), 2000) },
          }));
        })
        .catch(() => {
          setResultsByJob((prev) => ({ ...prev, [jobId]: { state: "none" } }));
        });
    }
  };

  if (loadError) {
    return (
      <Card p={p}>
        <div data-testid="logs-error" role="alert">
          <div style={{ fontWeight: 700, color: p.bad, marginBottom: 6 }}>
            Records failed to load
          </div>
          <div style={{ color: p.muted, fontSize: 13, marginBottom: 12 }}>
            Reading the record tables failed: {loadError}. This is a load
            failure, not an empty history.
          </div>
          <SmallButton primary onClick={() => setRetryNonce((n) => n + 1)}>
            Retry
          </SmallButton>
        </div>
      </Card>
    );
  }
  if (records === null) {
    return (
      <Card p={p}>
        <div style={{ color: p.muted, fontSize: 13 }}>Loading records…</div>
      </Card>
    );
  }

  const shownRecords = records
    .filter((r) => kindFilter === "ALL" || r.kind === kindFilter)
    .filter((r) => statusMatches(r.status, statusFilter))
    .slice(0, 50);

  const chipStyle = (on: boolean): React.CSSProperties => ({
    fontSize: 11.5, fontWeight: 600, padding: "2px 10px", borderRadius: 20,
    border: `1px solid ${on ? "#1e3a5f" : p.border}`,
    background: on ? "#1e3a5f" : p.card,
    color: on ? "#fff" : p.fg, cursor: "pointer",
  });

  return (
    <div>
      <Card p={p} style={{ marginBottom: 14 }}>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center" }}>
          {KIND_FILTERS.map((f) => (
            <button
              key={f.id}
              onClick={() => setKindFilter(f.id)}
              aria-pressed={kindFilter === f.id}
              style={chipStyle(kindFilter === f.id)}
            >
              {f.label}
            </button>
          ))}
          <div style={{ flex: 1 }} />
          {STATUS_FILTERS.map((f) => (
            <button
              key={f.id}
              onClick={() => setStatusFilter(f.id)}
              aria-pressed={statusFilter === f.id}
              style={chipStyle(statusFilter === f.id)}
            >
              {f.label}
            </button>
          ))}
        </div>
        <div style={{ borderTop: `1px solid ${p.borderSoft}`, margin: "12px 0" }} />
        <div style={{ fontSize: 12.5, color: p.muted }}>
          Showing the most recent {Math.min(50, shownRecords.length)} of{" "}
          {records.length} records · {jobsTotal} jobs recorded, {jobsCompleted} completed
          {reportsCount !== null &&
            `; ${reportsCount.toLocaleString()} reports on file (Reports view)`}
          . Records are read-only here; Jobs remains the surface that acts on them.
        </div>
      </Card>

      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ textAlign: "left", color: p.muted, fontSize: 12 }}>
              <th style={{ padding: "6px 8px", width: "15%" }}>Started (UTC)</th>
              <th style={{ padding: "6px 8px", width: "30%" }}>Record</th>
              <th style={{ padding: "6px 8px", width: "14%" }}>Kind</th>
              <th style={{ padding: "6px 8px", width: "11%" }}>Status</th>
              <th style={{ padding: "6px 8px", width: "10%" }}>Duration</th>
              <th style={{ padding: "6px 8px" }}>Summary</th>
            </tr>
          </thead>
          <tbody>
            {shownRecords.map((rec) => {
              const isOpen = expanded === rec.key;
              return [
                <tr
                  key={rec.key}
                  style={{ borderTop: `1px solid ${p.borderSoft}`, verticalAlign: "top" }}
                >
                  <td style={{ padding: "8px", fontFamily: "ui-monospace, Menlo, Consolas, monospace", fontSize: 12 }}>
                    {fmtUtc(rec.ts)}
                  </td>
                  <td style={{ padding: "8px" }}>
                    <b>{rec.title}</b>
                    <br />
                    <span style={{ fontFamily: "ui-monospace, Menlo, Consolas, monospace", fontSize: 12, color: p.muted }}>
                      {rec.sub}
                    </span>
                  </td>
                  <td style={{ padding: "8px" }}>{rec.kindLabel}</td>
                  <td style={{ padding: "8px", color: statusColor(rec.status), fontWeight: 700 }}>
                    {rec.status}
                  </td>
                  <td style={{ padding: "8px" }}>{fmtSecs(rec.durationS)}</td>
                  <td style={{ padding: "8px" }}>
                    {rec.summary}{" "}
                    <button
                      onClick={() => toggleExpand(rec)}
                      aria-expanded={isOpen}
                      style={{
                        background: "none", border: "none", color: p.accent,
                        cursor: "pointer", fontSize: 13, padding: 0, whiteSpace: "nowrap",
                      }}
                    >
                      {isOpen ? "▾ Detail open" : "▸ Detail"}
                    </button>
                  </td>
                </tr>,
                isOpen ? (
                  <tr key={`${rec.key}:detail`}>
                    <td colSpan={6} style={{ padding: "10px 12px", background: p.accentSoft }}>
                      {rec.job && (
                        <JobDetail job={rec.job} result={resultsByJob[rec.job.id]} />
                      )}
                      {rec.action && <PhaseDetail action={rec.action} />}
                      {rec.notification && <NotificationDetail entry={rec.notification} />}
                    </td>
                  </tr>
                ) : null,
              ];
            })}
            {shownRecords.length === 0 && (
              <tr>
                <td colSpan={6} style={{ padding: "12px 8px", color: p.muted }}>
                  No records match these filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const monoBox: React.CSSProperties = {
  fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
  fontSize: 12, whiteSpace: "pre-wrap", wordBreak: "break-word",
  background: "rgba(15, 23, 42, 0.04)", borderRadius: 6, padding: "8px 10px",
  marginTop: 8,
};

function JobDetail({
  job,
  result,
}: {
  job: JobResponse;
  result?: { state: "loading" | "ok" | "none" | "error"; text?: string };
}) {
  return (
    <div style={{ fontSize: 13 }}>
      <b>Detail — job record</b> · <code>jobs</code> row + <code>job_results</code> payload
      <div style={{ fontFamily: "ui-monospace, Menlo, Consolas, monospace", fontSize: 12, marginTop: 4 }}>
        id {job.id} · pipeline {job.pipeline} · created {fmtUtc(job.created_at)} · updated{" "}
        {fmtUtc(job.updated_at)} · status {job.status}
      </div>
      {Object.keys(job.params ?? {}).length > 0 && (
        <div style={monoBox}>params: {excerpt(JSON.stringify(job.params, null, 2))}</div>
      )}
      {job.status === "completed" && (
        result?.state === "ok" ? (
          <div style={monoBox}>result (excerpt): {result.text}</div>
        ) : result?.state === "loading" ? (
          <div style={{ marginTop: 8, fontSize: 12.5 }}>Loading stored result…</div>
        ) : (
          <div style={{ marginTop: 8, fontSize: 12.5 }}>
            No stored result payload for this job.
          </div>
        )
      )}
    </div>
  );
}

function PhaseDetail({ action }: { action: PhaseAction }) {
  return (
    <div style={{ fontSize: 13 }}>
      <b>Detail — phase action record</b> · <code>phase_actions</code> row
      <div style={{ fontFamily: "ui-monospace, Menlo, Consolas, monospace", fontSize: 12, marginTop: 4 }}>
        id {action.id} · phase {action.phase} · type {action.action_type || "—"} · status{" "}
        {action.status} · job {action.job_id ?? "—"} · started{" "}
        {action.started_at ? fmtUtc(action.started_at) : "—"} · completed{" "}
        {action.completed_at ? fmtUtc(action.completed_at) : "—"}
      </div>
      {action.error_message && (
        <div style={monoBox}>error_message: {action.error_message}</div>
      )}
      {action.params_json && action.params_json !== "{}" && (
        <div style={monoBox}>params: {excerpt(action.params_json)}</div>
      )}
    </div>
  );
}

function NotificationDetail({ entry }: { entry: NotificationLogEntry }) {
  return (
    <div style={{ fontSize: 13 }}>
      <b>Detail — notification record</b> · <code>notification_log</code> row
      <div style={{ fontFamily: "ui-monospace, Menlo, Consolas, monospace", fontSize: 12, marginTop: 4 }}>
        id {entry.id} · kind {entry.kind || "—"} · sent {fmtUtc(entry.sent_at)} · status{" "}
        {entry.status} · items {entry.item_count} · recipient {maskEmail(entry.recipient)}
      </div>
      {entry.subject && <div style={{ marginTop: 6 }}>Subject: {entry.subject}</div>}
      {entry.error && <div style={monoBox}>error: {entry.error}</div>}
    </div>
  );
}

// ── The view ────────────────────────────────────────────────────────────────

export function LogsView({
  darkMode,
  onNavigate,
}: {
  darkMode: boolean;
  onNavigate: (view: string) => void;
}) {
  const p = palette(darkMode);
  const [tab, setTab] = useState<LogsTab>("stream");
  return (
    <div style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
      <PageHead
        p={p}
        title="Logs"
        lede={
          tab === "stream"
            ? "The backend's own log, streamed into the app. The endpoints behind this view (GET /terminal/log, GET /terminal/log/stream) have been live all along; Spec 081 removed the panel that read them. Spec 087 Stage 5 restores the viewer."
            : "The recorded history: every run the system keeps a record of — jobs and their results (jobs / job_results), per-phase actions (phase_actions), and sent notifications (notification_log) — read as one log, with the stored detail one click away. Unlike the live stream, these records persist."
        }
        primary={
          <SmallButton onClick={() => onNavigate(tab === "stream" ? "status" : "jobs")}>
            {tab === "stream" ? "Open Status" : "Open Jobs"}
          </SmallButton>
        }
      />
      <TabsRow p={p} tabs={TABS} active={tab} onSelect={setTab} />
      {tab === "stream" ? (
        <StreamTab p={p} onOpenStatus={() => onNavigate("status")} />
      ) : (
        <RecordsTab p={p} />
      )}
    </div>
  );
}
