import { Fragment, useEffect, useState, useCallback, useRef } from "react";
import { fmtTime, fmtDateTimeCompact, fmtElapsed } from "../dateFormat";
import {
  cancelJob, clearJobs, createJob, getJobResults, getPipelineCatalog,
  listJobs, pauseJob, resumeJob, pauseAllJobs, resumeAllJobs,
  CatalogPipeline, JobResponse,
} from "../api";
import { useProject } from "../hooks/useProject";

// Internal runtime-only param keys that should NOT be re-submitted on retry
const RUNTIME_PARAM_KEYS = new Set(["node_count", "nodes_done", "stall_reason"]);

/** Build a clean params object suitable for re-submitting a job. */
function buildRetryParams(params: Record<string, unknown>): Record<string, unknown> {
  return Object.fromEntries(
    Object.entries(params).filter(([k]) => !k.startsWith("_") && !RUNTIME_PARAM_KEYS.has(k))
  );
}

/** Human-readable label for a params key. */
function fmtParamKey(k: string): string {
  return k.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

/** Render a param value as a readable string (not raw JSON). */
function fmtParamValue(v: unknown): string {
  if (v === null || v === undefined) return "—";
  if (typeof v === "boolean") return v ? "Yes" : "No";
  if (typeof v === "object") return JSON.stringify(v); // compact for objects/arrays
  return String(v);
}

// ── Helpers ─────────────────────────────────────────────────────────────────

/** Try to parse a string as JSON; return the object or null. */
function tryParseJson(s: string | undefined | null): Record<string, unknown> | null {
  if (!s) return null;
  try { const v = JSON.parse(s); return typeof v === "object" && v !== null ? v as Record<string, unknown> : null; }
  catch { return null; }
}

/** Render a user-friendly label for an error category. */
function errorCategory(msg: string): { label: string; color: string } {
  const m = msg.toLowerCase();
  if (m.includes("no module") || m.includes("import") || m.includes("attribute"))
    return { label: "Code / Import Error", color: "#7c3aed" };
  if (m.includes("timeout") || m.includes("unreachable") || m.includes("network"))
    return { label: "Network / Timeout", color: "#d97706" };
  if (m.includes("database") || m.includes("sqlite") || m.includes("sql"))
    return { label: "Database Error", color: "#0369a1" };
  if (m.includes("key") || m.includes("auth") || m.includes("permission"))
    return { label: "Auth / Permission", color: "#b45309" };
  if (m.includes("assertion") || m.includes("assert"))
    return { label: "Assertion Failed", color: "#9f1239" };
  return { label: "Experiment Error", color: "#991b1b" };
}

// ── Shared error dialog ─────────────────────────────────────────────────────
interface ErrorModalProps {
  title: string;
  message: string;
  detail?: string | null;
  params?: Record<string, unknown> | null;
  job?: JobResponse | null;        // if supplied, enables Retry button
  onRetry?: (() => void) | null;   // called on Retry — modal auto-closes
  onClose: () => void;
}
export function JobErrorModal({ title, message, detail, params, job, onRetry, onClose }: ErrorModalProps) {
  const text = `${title}\n${message}${detail ? "\n" + detail : ""}`;
  const [copied, setCopied] = useState(false);
  const [showRaw, setShowRaw] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text).then(() => { setCopied(true); setTimeout(() => setCopied(false), 1500); });
  };

  // Try to parse the message itself as JSON (structured error objects)
  const parsedMsg = tryParseJson(message);
  const displayMsg = parsedMsg
    ? (parsedMsg.error as string ?? parsedMsg.message as string ?? JSON.stringify(parsedMsg, null, 2))
    : message;
  const cat = errorCategory(displayMsg || "");

  const cleanDetail = detail ?? null;

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.55)", zIndex: 12000,
      display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}
      onClick={onClose}>
      <div style={{ background: "#fff", borderRadius: 12, maxWidth: 720, width: "100%", maxHeight: "85vh",
        display: "flex", flexDirection: "column", boxShadow: "0 24px 64px rgba(0,0,0,0.4)" }}
        onClick={e => e.stopPropagation()}>

        {/* Header */}
        <div style={{ padding: "16px 20px", borderBottom: "1px solid #fee2e2", background: "#fef2f2",
          borderRadius: "12px 12px 0 0", display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 22 }}>⚠️</span>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: "#991b1b", overflow: "hidden",
              textOverflow: "ellipsis", whiteSpace: "nowrap" }} title={title}>{title}</div>
            <span style={{ fontSize: 11, padding: "1px 7px", borderRadius: 8, background: cat.color + "20",
              color: cat.color, fontWeight: 600 }}>{cat.label}</span>
          </div>
          <button onClick={copy} style={{ padding: "4px 10px", border: "1px solid #fca5a5", borderRadius: 5,
            background: copied ? "#fee2e2" : "#fff", cursor: "pointer", fontSize: 11,
            color: copied ? "#16a34a" : "#dc2626" }}>
            {copied ? "✓ Copied" : "📋 Copy"}
          </button>
          <button onClick={onClose} style={{ border: "none", background: "none",
            cursor: "pointer", fontSize: 22, color: "#9ca3af", lineHeight: 1, padding: "0 4px" }}>×</button>
        </div>

        <div style={{ flex: 1, overflowY: "auto" }}>
          {/* Human-friendly error summary */}
          <div style={{ padding: "14px 20px", borderBottom: "1px solid #f3f4f6" }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 6,
              textTransform: "uppercase", letterSpacing: "0.05em" }}>What went wrong</div>
            <div style={{ fontSize: 13, color: "#111827", lineHeight: 1.7,
              background: "#fef2f2", padding: "10px 14px", borderRadius: 7,
              border: "1px solid #fecaca", whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
              {displayMsg || "No error message available."}
            </div>
          </div>

          {/* Job params — shown as a clean key-value table */}
          {params && Object.keys(params).filter(k => !k.startsWith("_")).length > 0 && (
            <div style={{ padding: "12px 20px", borderBottom: "1px solid #f3f4f6" }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 8,
                textTransform: "uppercase", letterSpacing: "0.05em" }}>Job parameters</div>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                <tbody>
                  {Object.entries(params)
            .filter(([k]) => !k.startsWith("_") && k !== "traceback")
                    .map(([k, v]) => (
                      <tr key={k} style={{ borderBottom: "1px solid #f3f4f6" }}>
                        <td style={{ padding: "4px 10px 4px 0", color: "#6b7280", fontWeight: 500,
                          whiteSpace: "nowrap", verticalAlign: "top", width: "35%" }}>{fmtParamKey(k)}</td>
                        <td style={{ padding: "4px 0", color: "#111827", wordBreak: "break-all",
                          fontFamily: typeof v === "string" ? "inherit" : "monospace" }}>
          {fmtParamValue(v)}
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Traceback / raw detail — collapsible */}
          {cleanDetail && (
            <div style={{ padding: "12px 20px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                <div style={{ fontSize: 12, fontWeight: 600, color: "#374151",
                  textTransform: "uppercase", letterSpacing: "0.05em" }}>Stack trace</div>
                <button onClick={() => setShowRaw(!showRaw)}
                  style={{ fontSize: 11, border: "1px solid #e5e7eb", background: "#f9fafb",
                    borderRadius: 4, cursor: "pointer", padding: "2px 8px", color: "#6b7280" }}>
                  {showRaw ? "Hide" : "Show"}
                </button>
              </div>
              {showRaw && (
                <pre style={{ fontFamily: "monospace", fontSize: 11, color: "#374151",
                  background: "#f8fafc", padding: "10px 14px", borderRadius: 7,
                  border: "1px solid #e5e7eb", lineHeight: 1.6,
                  whiteSpace: "pre-wrap", wordBreak: "break-word", margin: 0, maxHeight: 260, overflowY: "auto" }}>
                  {cleanDetail}
                </pre>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ padding: "12px 20px", borderTop: "1px solid #f3f4f6",
          display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
          {/* Left: job identity */}
          {job && (
            <div style={{ fontSize: 10, color: "#9ca3af", fontFamily: "monospace" }}>
              Job ID: {job.id.slice(0, 12)}… &middot; {job.pipeline}
            </div>
          )}
          {/* Right: action buttons */}
          <div style={{ display: "flex", gap: 8, marginLeft: "auto" }}>
            {onRetry && (
              <button
                onClick={() => { onRetry(); onClose(); }}
                style={{ padding: "6px 16px", border: "none", borderRadius: 6,
                  background: "#2563eb", color: "#fff", cursor: "pointer", fontSize: 13, fontWeight: 600 }}
                title="Re-submit this job with the same parameters">
                ↻ Retry
              </button>
            )}
            <button onClick={onClose} style={{ padding: "6px 18px", border: "1px solid #d1d5db",
              borderRadius: 6, background: "#fff", cursor: "pointer", fontSize: 13 }}>Close</button>
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Job details (Spec 081, FR-009): the completed job's record with the
 * meaning first — the result's own summary fields — and the raw
 * record one click deeper, never the other way round.
 */
function JobDetailsModal({ job, program, onClose }: {
  job: JobResponse;
  program: string;
  onClose: () => void;
}) {
  const [result, setResult] = useState<unknown>(undefined);
  const [showRaw, setShowRaw] = useState(false);
  useEffect(() => {
    let cancelled = false;
    getJobResults(job.id)
      .then((r) => { if (!cancelled) setResult(r); })
      .catch(() => { if (!cancelled) setResult(null); });
    return () => { cancelled = true; };
  }, [job.id]);

  const meaning: [string, string][] = [];
  if (result && typeof result === "object" && !Array.isArray(result)) {
    const r = result as Record<string, unknown>;
    for (const key of ["verdict", "outcome", "status", "summary", "message", "headline", "conclusion"]) {
      const v = r[key];
      if (typeof v === "string" && v.trim()) meaning.push([fmtParamKey(key), v]);
      else if (typeof v === "number" || typeof v === "boolean") meaning.push([fmtParamKey(key), String(v)]);
    }
  }
  const displayParams = Object.entries(job.params ?? {})
    .filter(([k]) => !k.startsWith("_") && k !== "traceback");

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.55)", zIndex: 12000,
      display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}
      onClick={onClose}>
      <div style={{ background: "#fff", borderRadius: 12, maxWidth: 720, width: "100%", maxHeight: "85vh",
        display: "flex", flexDirection: "column", boxShadow: "0 24px 64px rgba(0,0,0,0.4)" }}
        onClick={(e) => e.stopPropagation()}>
        <div style={{ padding: "16px 20px", borderBottom: "1px solid #e5e7eb",
          display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: "#111827", overflow: "hidden",
              textOverflow: "ellipsis", whiteSpace: "nowrap" }} title={job.name}>{job.name}</div>
            <div style={{ fontSize: 11, color: "#6b7280" }}>
              {job.pipeline} · {program} · {job.status}
            </div>
          </div>
          <button onClick={onClose} style={{ border: "none", background: "none",
            cursor: "pointer", fontSize: 22, color: "#9ca3af", lineHeight: 1, padding: "0 4px" }}>×</button>
        </div>
        <div style={{ flex: 1, overflowY: "auto", padding: "14px 20px" }}>
          <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 12 }}>
            Started {fmtDateTimeCompact(job.created_at)}
            {job.updated_at ? <> · Finished {fmtDateTimeCompact(job.updated_at)}</> : ""}
          </div>

          <div style={{ fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 6,
            textTransform: "uppercase", letterSpacing: "0.05em" }}>Result</div>
          {result === undefined && <div style={{ fontSize: 13, color: "#6b7280" }}>Reading the result record…</div>}
          {result === null && (
            <div style={{ fontSize: 13, color: "#6b7280" }}>
              No result record is stored for this job — the run finished
              without leaving one, and this screen will not invent one.
            </div>
          )}
          {result !== undefined && result !== null && meaning.length === 0 && (
            <div style={{ fontSize: 13, color: "#6b7280" }}>
              The result record carries no summary fields — its content is
              the raw record below.
            </div>
          )}
          {meaning.length > 0 && (
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, marginBottom: 12 }}>
              <tbody>
                {meaning.map(([k, v]) => (
                  <tr key={k} style={{ borderBottom: "1px solid #f3f4f6" }}>
                    <td style={{ padding: "4px 10px 4px 0", color: "#6b7280", fontWeight: 500, whiteSpace: "nowrap", verticalAlign: "top", width: "35%" }}>{k}</td>
                    <td style={{ padding: "4px 0", color: "#111827", wordBreak: "break-word" }}>{v}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {displayParams.length > 0 && (
            <>
              <div style={{ fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 6,
                textTransform: "uppercase", letterSpacing: "0.05em" }}>Job parameters</div>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, marginBottom: 12 }}>
                <tbody>
                  {displayParams.map(([k, v]) => (
                    <tr key={k} style={{ borderBottom: "1px solid #f3f4f6" }}>
                      <td style={{ padding: "4px 10px 4px 0", color: "#6b7280", fontWeight: 500, whiteSpace: "nowrap", verticalAlign: "top", width: "35%" }}>{fmtParamKey(k)}</td>
                      <td style={{ padding: "4px 0", color: "#111827", wordBreak: "break-all",
                        fontFamily: typeof v === "string" ? "inherit" : "monospace" }}>{fmtParamValue(v)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}

          {result !== undefined && result !== null && (
            <div>
              <button onClick={() => setShowRaw((v) => !v)}
                style={{ fontSize: 11, border: "1px solid #e5e7eb", background: "#f9fafb",
                  borderRadius: 4, cursor: "pointer", padding: "2px 8px", color: "#6b7280" }}>
                {showRaw ? "Hide the raw record" : "Show the raw record"}
              </button>
              {showRaw && (
                <pre style={{ fontFamily: "monospace", fontSize: 11, color: "#374151",
                  background: "#f8fafc", padding: "10px 14px", borderRadius: 7,
                  border: "1px solid #e5e7eb", lineHeight: 1.6, marginTop: 8,
                  whiteSpace: "pre-wrap", wordBreak: "break-word", maxHeight: 300, overflowY: "auto" }}>
                  {JSON.stringify(result, null, 2)}
                </pre>
              )}
            </div>
          )}
        </div>
        <div style={{ padding: "12px 20px", borderTop: "1px solid #f3f4f6",
          display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
          <div style={{ fontSize: 10, color: "#9ca3af", fontFamily: "monospace" }}>
            Job ID: {job.id.slice(0, 12)}… · {job.pipeline}
          </div>
          <button onClick={onClose} style={{ padding: "6px 18px", border: "1px solid #d1d5db",
            borderRadius: 6, background: "#fff", cursor: "pointer", fontSize: 13 }}>Close</button>
        </div>
      </div>
    </div>
  );
}

export function JobsView() {
  const { projects, activeProject } = useProject();
  const [jobs, setJobs] = useState<JobResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pipelines, setPipelines] = useState<CatalogPipeline[]>([]);
  const [clearing, setClearing] = useState(false);
  const [pausing, setPausing] = useState<Set<string>>(new Set());
  // Track nodes_done per job to detect slow SA nodes (avoid growing ETA)
  const nodesDoneTracker = useRef<Map<string, { done: number; since: number }>>(new Map());

  // Submit form
  const [jobName, setJobName] = useState("");
  const [pipeline, setPipeline] = useState("block_entropy");
  const [paramsText, setParamsText] = useState('{"text_id": ""}');
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  // Error modal
  const [errorModal, setErrorModal] = useState<{
    title: string; message: string; detail?: string;
    params?: Record<string, unknown> | null;
    job?: JobResponse | null;
    onRetry?: (() => void) | null;
  } | null>(null);

  // Details modal (completed jobs: meaning first, raw record deeper)
  const [detailsJob, setDetailsJob] = useState<JobResponse | null>(null);

  // Spec 081 (FR-009): every row names its program. The job record
  // carries no program field of its own; jobs submitted from this
  // screen are stamped with the open program's id in their params
  // (below), and older/unstamped jobs say so honestly.
  const programLabel = useCallback((job: JobResponse): string => {
    const pid = job.params?.project_id;
    if (typeof pid === "string" && pid) {
      return projects.find((p) => p.id === pid)?.label ?? pid;
    }
    return "Not recorded";
  }, [projects]);

  // What-happened lines for failed rows, read once per failed job
  // from its stored result record (never invented, never re-polled).
  const [failureLines, setFailureLines] = useState<Record<string, string>>({});
  useEffect(() => {
    const missing = jobs.filter((j) => j.status === "failed" && !(j.id in failureLines));
    if (missing.length === 0) return;
    let cancelled = false;
    (async () => {
      const updates: Record<string, string> = {};
      for (const j of missing.slice(0, 10)) {
        try {
          const data = (await getJobResults(j.id)) as Record<string, unknown>;
          const msg = (data.error as string) ?? (data.message as string) ?? (data.detail as string) ?? "";
          updates[j.id] = msg
            ? String(msg).slice(0, 240)
            : "The job failed; no error message was stored with it.";
        } catch {
          updates[j.id] = "The job failed; its error record could not be read.";
        }
      }
      if (!cancelled && Object.keys(updates).length > 0) {
        setFailureLines((prev) => ({ ...prev, ...updates }));
      }
    })();
    return () => { cancelled = true; };
  }, [jobs, failureLines]);

  const load = useCallback(async (manual = false) => {
    if (manual) setRefreshing(true);
    try {
      const j = await listJobs();
      setJobs(j.sort((a, b) => b.created_at.localeCompare(a.created_at)));
      setLastUpdated(new Date());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load jobs");
    } finally {
      setLoading(false);
      if (manual) setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    load();
    const id = setInterval(load, 3000);
    getPipelineCatalog().then(setPipelines).catch(() => {});
    return () => clearInterval(id);
  }, [load]);

  const makeRetryHandler = useCallback((job: JobResponse) => async () => {
    try {
      const retryParams = buildRetryParams(job.params ?? {});
      // Keep the job's program stamp; stamp the open program when the
      // original carried none (FR-009).
      if (!retryParams.project_id && activeProject) {
        retryParams.project_id = activeProject.id;
      }
      await createJob({
        name: `${job.name} (retry)`,
        pipeline: job.pipeline,
        params: retryParams,
      });
      await load();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Retry failed");
    }
  }, [load, activeProject]);

  const handleClearJobs = async () => {
    if (!confirm("Delete all jobs and results?")) return;
    setClearing(true);
    try { await clearJobs(); await load(); } finally { setClearing(false); }
  };

  const handleSubmit = async () => {
    if (!jobName.trim()) {
      setSubmitError("Job name is required");
      return;
    }
    let params: Record<string, unknown>;
    try {
      params = JSON.parse(paramsText);
    } catch {
      setSubmitError("Params must be valid JSON");
      return;
    }
    try {
      setSubmitting(true);
      setSubmitError(null);
      // Stamp the open program so the row can name it (FR-009).
      if (activeProject && !params.project_id) {
        params = { ...params, project_id: activeProject.id };
      }
      await createJob({ name: jobName.trim(), pipeline, params });
      setJobName("");
      await load();
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : "Submit failed");
    } finally {
      setSubmitting(false);
    }
  };

  const handleViewResults = async (job: JobResponse) => {
    // Determine the result filename: exp_run uses exp_id.json, pipeline jobs use result_file param
    const expId      = (job.params?.exp_id   as string) ?? "";
    const resultFile = (job.params?.result_file as string) ?? "";
    const filename   = expId ? `${expId}.json` : resultFile;

    if (job.status === "failed") {
      // Extract the job params for display (strip internal keys)
      const displayParams: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(job.params ?? {})) {
        if (!k.startsWith("_") && k !== "traceback") displayParams[k] = v;
      }
      try {
        const data = await getJobResults(job.id);
        const raw  = data as Record<string, unknown>;
        // Try structured error fields, fall back to any string property
        const errMsg =
          (raw.error as string) ??
          (raw.message as string) ??
          (raw.detail as string) ??
          JSON.stringify(raw).slice(0, 300);
        const trace  = (raw.traceback as string) ?? null;
      setErrorModal({
          title: job.name,
          message: errMsg || "Unknown error — see stack trace below.",
          detail: trace ?? undefined,
          params: Object.keys(displayParams).length ? displayParams : null,
          job,
          onRetry: makeRetryHandler(job),
        });
      } catch {
        setErrorModal({
          title: job.name,
          message: "Job failed — no error details stored in the database.",
          detail: undefined,
          params: Object.keys(displayParams).length ? displayParams : null,
          job,
          onRetry: makeRetryHandler(job),
        });
      }
      return;
    }

    // All completed jobs: navigate to Reports → Data tab
    window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "reports" } }));
    if (filename) {
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent("glossa:reports_highlight", {
          detail: { tab: "data", search: filename },
        }));
      }, 120);
    }
  };

  const handleCancel = async (id: string) => {
    try {
      await cancelJob(id);
      await load();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Cancel failed");
    }
  };

  const handlePause = async (id: string) => {
    setPausing(s => new Set([...s, id]));
    try { await pauseJob(id); await load(); }
    catch (e) { alert(e instanceof Error ? e.message : "Pause failed"); }
    finally { setPausing(s => { const n = new Set(s); n.delete(id); return n; }); }
  };

  const handleResume = async (id: string) => {
    setPausing(s => new Set([...s, id]));
    try { await resumeJob(id); await load(); }
    catch (e) { alert(e instanceof Error ? e.message : "Resume failed"); }
    finally { setPausing(s => { const n = new Set(s); n.delete(id); return n; }); }
  };

  const handlePauseAll = async () => {
    try { await pauseAllJobs(); await load(); }
    catch (e) { alert(e instanceof Error ? e.message : "Pause all failed"); }
  };

  const handleResumeAll = async () => {
    try { await resumeAllJobs(); await load(); }
    catch (e) { alert(e instanceof Error ? e.message : "Resume all failed"); }
  };

  const statusColor = (s: string) => {
    if (s === "completed") return "#16a34a";
    if (s === "failed")    return "#dc2626";
    if (s === "running")   return "#2563eb";
    if (s === "pending")   return "#d97706";
    if (s === "paused")    return "#92400e";
    if (s === "cancelled") return "#6b7280";
    return "#6b7280";
  };
  const statusBg = (s: string) => {
    if (s === "completed") return "#dcfce7";
    if (s === "failed")    return "#fee2e2";
    if (s === "running")   return "#dbeafe";
    if (s === "pending")   return "#fef3c7";
    if (s === "paused")    return "#fef3c7";
    if (s === "cancelled") return "#f3f4f6";
    return "#f3f4f6";
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
          <h2 style={{ margin: 0 }}>Jobs</h2>
          {lastUpdated && (
            <span style={{ fontSize: 11, color: "#9ca3af" }}>
              updated {fmtTime(lastUpdated)}
            </span>
          )}
        </div>
        <div style={{ display: "flex", gap: 6 }}>
          <button onClick={() => load(true)} disabled={refreshing}
            style={{ ...btnStyle, background: "#f3f4f6", color: "#374151", fontSize: 12, padding: "4px 12px" }}
            title="Manually refresh the job list">
            {refreshing ? "Refreshing…" : "⟳ Refresh"}
          </button>
          <button
            onClick={handlePauseAll}
            disabled={jobs.filter(j => j.status === "pending" || j.status === "running").length === 0}
            style={{ ...btnStyle, background: "#d97706", fontSize: 12, padding: "4px 12px" }}
            title="Pause all pending and running jobs">
            ⏸ Pause All
          </button>
          <button
            onClick={handleResumeAll}
            disabled={jobs.filter(j => j.status === "paused").length === 0}
            style={{ ...btnStyle, background: "#059669", fontSize: 12, padding: "4px 12px" }}
            title="Resume all paused jobs">
            ▶ Resume All
          </button>
          <button onClick={handleClearJobs} disabled={clearing || jobs.length === 0}
            style={{ ...btnStyle, background: "#6b7280", fontSize: 12, padding: "4px 12px" }}>
            {clearing ? "Clearing…" : "Delete All"}
          </button>
        </div>
      </div>

      {/* Submit panel */}
      <details style={{ marginBottom: "1.5rem" }}>
        <summary style={{ cursor: "pointer", fontWeight: 600 }}>
          + New job
        </summary>
        <div
          style={{
            marginTop: "0.75rem",
            padding: "1rem",
            border: "1px solid #e5e7eb",
            borderRadius: 6,
            maxWidth: 560,
          }}
        >
          <Field label="Job name">
            <input
              value={jobName}
              onChange={(e) => setJobName(e.target.value)}
              placeholder="e.g. Entropy analysis — English"
              style={inputStyle}
            />
          </Field>
          <Field label="Pipeline">
            <select
              value={pipeline}
              onChange={(e) => {
                setPipeline(e.target.value);
                const meta = pipelines.find((p) => p.id === e.target.value);
                setParamsText(meta ? JSON.stringify(meta.default_params, null, 2) : '{"text_id": ""}');
              }}
              style={inputStyle}
            >
              {(pipelines.length > 0 ? pipelines.map((p) => p.id) : [pipeline]).map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </Field>
          <Field label="Parameters (JSON)">
            <textarea
              value={paramsText}
              onChange={(e) => setParamsText(e.target.value)}
              rows={4}
              style={{ ...inputStyle, fontFamily: "monospace", resize: "vertical" }}
            />
          </Field>
          {submitError && (
            <p style={{ color: "#dc2626", margin: "4px 0" }}>{submitError}</p>
          )}
          <button onClick={handleSubmit} disabled={submitting} style={btnStyle}>
            {submitting ? "Submitting…" : "Submit"}
          </button>
        </div>
      </details>

      {/* Job list */}
      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "#dc2626" }}>{error}</p>}
      {!loading && jobs.length === 0 && (
        <div style={{
          padding: "1.25rem 1.5rem", background: "#f8fafc",
          border: "1px solid #e2e8f0", borderRadius: 8, maxWidth: 560,
        }}>
          <p style={{ margin: "0 0 8px", fontWeight: 600, color: "#374151", fontSize: 13 }}>
            No jobs yet
          </p>
          <p style={{ margin: "0 0 6px", fontSize: 12, color: "#6b7280", lineHeight: 1.6 }}>
            Jobs are the tool's background runs — experiments, the research loop,
            discovery fetches and pipeline runs appear here while they work and
            stay here as the record once they finish. Start one with the
            <strong> New job</strong> panel above, or from the surface that owns the work.
          </p>
          <p style={{ margin: 0, fontSize: 12, color: "#6b7280", lineHeight: 1.6 }}>
            A failed job stays visible with what happened and a retry — it is
            never silently cleared.
          </p>
        </div>
      )}
      {jobs.length > 0 && (
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              {["Job", "Program", "State", "Started", "Finished", "Result"].map((h) => (
                <Th key={h}>{h}</Th>
              ))}
            </tr>
          </thead>
          <tbody>
            {jobs.map((j) => {
              const device: string = (j.params?.compute_device as string) ?? "";
              const deviceLabel: string = (j.params?.compute_device_label as string) ?? "";
              const isGpu = device === "gpu";
              const isCli = (j.params?.source as string) === "cli";
              const isAiAction = (j.params?.source as string) === "ai_action";
              const deviceBadge = device
                ? { bg: isGpu ? "#dbeafe" : "#f3f4f6", color: isGpu ? "#1e40af" : "#374151",
                    text: isGpu ? `⚡ ${deviceLabel || "GPU"}` : `⚙️ ${deviceLabel || "CPU"}` }
                : null;
              const nodeCount = (j.params?.node_count as number) ?? 0;
              const nodesDone = (j.params?.nodes_done as number) ?? 0;
              const pct = nodeCount > 0 ? Math.round((nodesDone / nodeCount) * 100) : null;
              const isExpRun = j.pipeline === "exp_run";
              const resourceWait = (j.params?.resource_wait as string) ?? null;
              const elapsedSec = j.status === "running"
                ? Math.round((Date.now() - new Date(j.created_at).getTime()) / 1000)
                : null;
              // Historical average duration for this pipeline (from completed jobs)
              const historicalAvgSec = (() => {
                const done = jobs.filter(
                  d => d.status === "completed" && d.pipeline === j.pipeline
                    && d.id !== j.id && d.updated_at
                );
                if (done.length === 0) return null;
                const durations = done.map(d =>
                  (new Date(d.updated_at!).getTime() - new Date(d.created_at).getTime()) / 1000
                ).filter(x => x > 0);
                return durations.length > 0
                  ? durations.reduce((a, b) => a + b, 0) / durations.length
                  : null;
              })();
              // ETA: use historical avg when < 15% complete; blend to linear extrapolation after
              const etaSec = elapsedSec !== null && pct !== null
                ? (() => {
                    if (pct >= 15) return Math.round((elapsedSec / pct) * (100 - pct));
                    if (historicalAvgSec !== null) return Math.max(0, Math.round(historicalAvgSec - elapsedSec));
                    return null;
                  })()
                : null;
              // Stuck-node detection: update tracker when nodes_done changes
              const nowMs = Date.now();
              const tracker = nodesDoneTracker.current.get(j.id);
              if (!tracker || tracker.done !== nodesDone) {
                nodesDoneTracker.current.set(j.id, { done: nodesDone, since: nowMs });
              }
              const stuckMs = tracker && tracker.done === nodesDone ? nowMs - tracker.since : 0;
              // When a node has been running > 3 min and ETA would be > 2× elapsed: show computing label
              const nodeComputingLabel = isExpRun && j.status === "running" && nodeCount > 0
                && stuckMs > 180_000 && etaSec !== null && elapsedSec !== null && etaSec > elapsedSec * 1.5
                ? `node ${nodesDone + 1}/${nodeCount} computing…`
                : null;
              return (
              <Fragment key={j.id}>
              <tr>
                <Td>
                  <div style={{ fontWeight: 500 }}>{j.name}</div>
                  <div style={{ fontSize: 11, color: "#6b7280", display: "flex", gap: 6, alignItems: "center", flexWrap: "wrap", marginTop: 2 }}>
                    <code style={{ fontFamily: "monospace" }}>{j.pipeline}</code>
                    <span style={{ fontFamily: "monospace" }}>{j.id.slice(0, 8)}…</span>
                    {deviceBadge && (
                      <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 6,
                                     background: deviceBadge.bg, color: deviceBadge.color,
                                     fontWeight: 600, whiteSpace: "nowrap" }}>
                        {deviceBadge.text}
                      </span>
                    )}
                    {isCli && (
                      <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 6,
                                     background: "#f0fdf4", color: "#15803d",
                                     fontWeight: 600, whiteSpace: "nowrap" }}
                            title="Run from CLI (terminal/script)">
                        💻 CLI
                      </span>
                    )}
                    {isAiAction && (
                      <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 6,
                                     background: "#fdf4ff", color: "#7e22ce",
                                     fontWeight: 600, whiteSpace: "nowrap" }}
                            title="Triggered by AI assistant">
                        ✨ AI
                      </span>
                    )}
                  </div>
                  {/* Resource-wait banner — job is pending but blocked on CPU/RAM/VRAM */}
                  {j.status === "pending" && resourceWait && (
                    <div style={{ marginTop: 4, fontSize: 10, color: "#92400e",
                                  background: "#fef3c7", border: "1px solid #fcd34d",
                                  borderRadius: 4, padding: "2px 7px",
                                  display: "flex", alignItems: "center", gap: 4 }}>
                      <span>⏳</span>
                      <span>{resourceWait}</span>
                    </div>
                  )}
                  {/* Progress bar for running exp_run jobs */}
                  {j.status === "running" && isExpRun && nodeCount > 0 && (
                    <div style={{ marginTop: 4, display: "flex", alignItems: "center", gap: 6 }}>
                      <div style={{ flex: 1, height: 4, background: "#e5e7eb", borderRadius: 2, overflow: "hidden" }}>
                        <div style={{ height: "100%", width: `${pct ?? 0}%`, background: "#2563eb", borderRadius: 2, transition: "width 0.5s" }} />
                      </div>
                      <span style={{ fontSize: 10, color: "#6b7280", whiteSpace: "nowrap" }}>
                        {nodesDone}/{nodeCount} nodes{pct !== null ? ` (${pct}%)` : ""}
                        {elapsedSec !== null && ` · ${fmtElapsed(elapsedSec)}`}
                        {nodeComputingLabel
                          ? ` · ${nodeComputingLabel}`
                          : etaSec !== null ? ` · ~${fmtElapsed(etaSec)} left` : ""}
                      </span>
                    </div>
                  )}
                </Td>
                <Td>
                  <span style={{ fontSize: 12, color: programLabel(j) === "Not recorded" ? "#9ca3af" : "#111827" }}>
                    {programLabel(j)}
                  </span>
                </Td>
                <Td>
                  <span style={{ display: "inline-block", padding: "1px 7px", borderRadius: 10,
                    background: statusBg(j.status), color: statusColor(j.status), fontWeight: 700, fontSize: 11 }}>
                    {j.status}
                  </span>
                  {j.status === "running" && elapsedSec !== null && !isExpRun && (
                    <div style={{ fontSize: 10, color: "#9ca3af" }}>{fmtElapsed(elapsedSec ?? 0)} elapsed</div>
                  )}
                </Td>
                <Td>{fmtDateTimeCompact(j.created_at)}</Td>
                <Td>
                  {(j.status === "completed" || j.status === "failed" || j.status === "cancelled") && j.updated_at
                    ? fmtDateTimeCompact(j.updated_at)
                    : <span style={{ color: "#9ca3af" }}>—</span>}
                </Td>
                <Td>
                  <span style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                    {j.status === "completed" && (
                      <>
                        <button
                          style={{ ...btnStyle, padding: "2px 10px", fontSize: 12, background: "#059669" }}
                          onClick={() => handleViewResults(j)}
                          title="Open the result in Reports & ledger"
                        >
                          📂 Results
                        </button>
                        <button
                          style={{ ...btnStyle, padding: "2px 10px", fontSize: 12, background: "#f3f4f6", color: "#374151" }}
                          onClick={() => setDetailsJob(j)}
                          title="The job's record — result summary first, raw record inside"
                        >
                          Details
                        </button>
                      </>
                    )}
                    {j.status === "failed" && (
                      <button
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 12, background: "#dc2626" }}
                        onClick={() => handleViewResults(j)}
                        title="View error details"
                      >
                        ⚠ Error Details
                      </button>
                    )}
                    {j.status === "cancelled" && (
                      <span style={{ fontSize: 11, color: "#6b7280", fontStyle: "italic" }}>cancelled</span>
                    )}
                    {(j.status === "pending" || j.status === "running") && (
                      <>
                        <button
                          style={{ ...btnStyle, padding: "2px 10px", fontSize: 12, background: "#d97706" }}
                          onClick={() => handlePause(j.id)}
                          disabled={pausing.has(j.id)}
                          title="Pause this job">
                          {pausing.has(j.id) ? "…" : "⏸ Pause"}
                        </button>
                        <button
                          style={{ ...btnStyle, padding: "2px 10px", fontSize: 12,
                            background: j.status === "running" ? "#ea580c" : "#6b7280" }}
                          onClick={() => handleCancel(j.id)}
                          title={j.status === "running" ? "Abort this running job" : "Cancel this queued job"}>
                          {j.status === "running" ? "❌ Abort" : "⏸ Cancel"}
                        </button>
                      </>
                    )}
                    {j.status === "paused" && (
                      <button
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 12, background: "#059669" }}
                        onClick={() => handleResume(j.id)}
                        disabled={pausing.has(j.id)}
                        title="Resume this paused job">
                        {pausing.has(j.id) ? "…" : "▶ Resume"}
                      </button>
                    )}
                  </span>
                </Td>
              </tr>
              {j.status === "failed" && (
                <tr>
                  <td colSpan={6} style={{ padding: "8px 12px 10px", background: "#fef2f2", borderBottom: "1px solid #fee2e2" }}>
                    <div style={{ display: "flex", gap: 10, alignItems: "flex-start", flexWrap: "wrap" }}>
                      <div style={{ flex: "1 1 320px", fontSize: 12, color: "#7f1d1d", lineHeight: 1.55 }}>
                        <b>What happened:</b>{" "}
                        {failureLines[j.id] ?? "Reading the error record…"}
                      </div>
                      <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                        <button
                          style={{ ...btnStyle, padding: "3px 12px", fontSize: 12, background: "#2563eb" }}
                          onClick={() => { void makeRetryHandler(j)(); }}
                          title="Re-submit this job with the same parameters">
                          ↻ Retry — re-submits with the same parameters
                        </button>
                        <button
                          style={{ ...btnStyle, padding: "3px 12px", fontSize: 12, background: "#f3f4f6", color: "#374151" }}
                          onClick={() => handleViewResults(j)}>
                          Error details
                        </button>
                      </div>
                    </div>
                  </td>
                </tr>
              )}
              </Fragment>
            );
            })}
          </tbody>
        </table>
      )}

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

      {/* Details modal */}
      {detailsJob && (
        <JobDetailsModal
          job={detailsJob}
          program={programLabel(detailsJob)}
          onClose={() => setDetailsJob(null)}
        />
      )}

    </div>
  );
}

function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div style={{ marginBottom: "0.6rem" }}>
      <label
        style={{ display: "block", fontWeight: 500, marginBottom: 2, fontSize: 13 }}
      >
        {label}
      </label>
      {children}
    </div>
  );
}

function Th({ children }: { children: React.ReactNode }) {
  return (
    <th
      style={{
        textAlign: "left",
        padding: "4px 12px 4px 0",
        borderBottom: "2px solid #e5e7eb",
        fontSize: 13,
        color: "#374151",
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </th>
  );
}

function Td({ children }: { children: React.ReactNode }) {
  return (
    <td
      style={{
        padding: "5px 12px 5px 0",
        borderBottom: "1px solid #f3f4f6",
        fontSize: 13,
        verticalAlign: "top",
      }}
    >
      {children}
    </td>
  );
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "5px 8px",
  border: "1px solid #d1d5db",
  borderRadius: 4,
  fontSize: 13,
  boxSizing: "border-box",
};

const btnStyle: React.CSSProperties = {
  background: "#2563eb",
  color: "#fff",
  border: "none",
  borderRadius: 4,
  padding: "6px 16px",
  fontSize: 13,
  cursor: "pointer",
};
