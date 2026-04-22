import { useEffect, useState, useCallback } from "react";
import { fmtTime, fmtDateTimeCompact } from "../dateFormat";
import {
  cancelJob,
  clearJobs,
  createJob,
  getJobResults,
  getPipelineCatalog,
  listJobs,
  CatalogPipeline,
  JobResponse,
} from "../api";

// ── Shared error dialog ─────────────────────────────────────────────────────
interface ErrorModalProps {
  title: string;
  message: string;
  detail?: string | null;
  onClose: () => void;
}
export function JobErrorModal({ title, message, detail, onClose }: ErrorModalProps) {
  const text = `${title}\n${message}${detail ? "\n" + detail : ""}`;
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text).then(() => { setCopied(true); setTimeout(() => setCopied(false), 1500); });
  };
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.55)", zIndex: 12000,
      display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}
      onClick={onClose}>
      <div style={{ background: "#fff", borderRadius: 10, maxWidth: 700, width: "100%", maxHeight: "80vh",
        display: "flex", flexDirection: "column", boxShadow: "0 20px 60px rgba(0,0,0,0.4)" }}
        onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div style={{ padding: "16px 20px", borderBottom: "1px solid #fee2e2", background: "#fef2f2",
          borderRadius: "10px 10px 0 0", display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 20 }}>⚠️</span>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: "#991b1b", overflow: "hidden",
              textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{title}</div>
            <div style={{ fontSize: 11, color: "#b91c1c", marginTop: 2 }}>Job failed</div>
          </div>
          <button onClick={copy} style={{ padding: "4px 10px", border: "1px solid #fca5a5", borderRadius: 5,
            background: copied ? "#fee2e2" : "#fff", cursor: "pointer", fontSize: 11,
            color: copied ? "#16a34a" : "#dc2626" }}>
            {copied ? "✓ Copied" : "📋 Copy"}
          </button>
          <button onClick={onClose} style={{ border: "none", background: "none",
            cursor: "pointer", fontSize: 20, color: "#9ca3af", padding: "0 4px" }}>×</button>
        </div>
        {/* Error message */}
        <div style={{ padding: "14px 20px", borderBottom: detail ? "1px solid #fee2e2" : "none" }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#374151", marginBottom: 6 }}>Error message</div>
          <div style={{ fontFamily: "monospace", fontSize: 12, color: "#dc2626",
            background: "#fef2f2", padding: "8px 12px", borderRadius: 5, lineHeight: 1.6,
            whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
            {message || "No error message available."}
          </div>
        </div>
        {/* Detail */}
        {detail && (
          <div style={{ flex: 1, overflowY: "auto", padding: "14px 20px" }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: "#374151", marginBottom: 6 }}>Details</div>
            <pre style={{ fontFamily: "monospace", fontSize: 11, color: "#374151",
              background: "#f8fafc", padding: "8px 12px", borderRadius: 5, lineHeight: 1.6,
              whiteSpace: "pre-wrap", wordBreak: "break-word", margin: 0, overflowX: "auto" }}>
              {detail}
            </pre>
          </div>
        )}
        {/* Footer */}
        <div style={{ padding: "12px 20px", borderTop: "1px solid #f3f4f6",
          display: "flex", justifyContent: "flex-end" }}>
          <button onClick={onClose} style={{ padding: "6px 18px", border: "1px solid #d1d5db",
            borderRadius: 5, background: "#fff", cursor: "pointer", fontSize: 13 }}>Close</button>
        </div>
      </div>
    </div>
  );
}

export function JobsView() {
  const [jobs, setJobs] = useState<JobResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pipelines, setPipelines] = useState<CatalogPipeline[]>([]);
  const [clearing, setClearing] = useState(false);

  // Submit form
  const [jobName, setJobName] = useState("");
  const [pipeline, setPipeline] = useState("block_entropy");
  const [paramsText, setParamsText] = useState('{"text_id": ""}');
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  // Error modal
  const [errorModal, setErrorModal] = useState<{ title: string; message: string; detail?: string } | null>(null);

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
      // Load error details and show in modal
      try {
        const data = await getJobResults(job.id);
        const errMsg = (data as Record<string, unknown>).error as string ?? "Unknown error";
        const trace  = (data as Record<string, unknown>).traceback as string ?? null;
        setErrorModal({ title: job.name, message: errMsg, detail: trace ?? undefined });
      } catch {
        setErrorModal({
          title: job.name,
          message: "Job failed — no error details stored.",
          detail: `Job ID: ${job.id}\nPipeline: ${job.pipeline}`,
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

  const statusColor = (s: string) => {
    if (s === "completed") return "#16a34a";
    if (s === "failed")    return "#dc2626";
    if (s === "running")   return "#2563eb";
    if (s === "pending")   return "#d97706";
    if (s === "cancelled") return "#6b7280";
    return "#6b7280";
  };
  const statusBg = (s: string) => {
    if (s === "completed") return "#dcfce7";
    if (s === "failed")    return "#fee2e2";
    if (s === "running")   return "#dbeafe";
    if (s === "pending")   return "#fef3c7";
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
          <button
            onClick={() => load(true)}
            disabled={refreshing}
            style={{ ...btnStyle, background: "#f3f4f6", color: "#374151", fontSize: 12, padding: "4px 12px" }}
            title="Manually refresh the job list"
          >
            {refreshing ? "Refreshing…" : "⟳ Refresh"}
          </button>
          <button
            onClick={handleClearJobs}
            disabled={clearing || jobs.length === 0}
            style={{ ...btnStyle, background: "#6b7280", fontSize: 12, padding: "4px 12px" }}
          >
            {clearing ? "Clearing…" : "Clear all"}
          </button>
        </div>
      </div>

      {/* Submit panel */}
      <details style={{ marginBottom: "1.5rem" }}>
        <summary style={{ cursor: "pointer", fontWeight: 600 }}>
          + Submit new job
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
            No pipeline jobs yet
          </p>
          <p style={{ margin: "0 0 6px", fontSize: 12, color: "#6b7280", lineHeight: 1.6 }}>
            This tab tracks analysis pipelines submitted through the
            <strong> Submit new job</strong> panel above. Pipeline jobs run corpus analysis
            (block entropy, NWSP, hypothesis engine, etc.) on corpora you upload to the Corpora tab.
          </p>
          <p style={{ margin: 0, fontSize: 12, color: "#6b7280", lineHeight: 1.6 }}>
            <strong>Note:</strong> background scripts like OCR run separately and do not appear
            here — check the <strong>Experiments</strong> tab to run or stream those.
          </p>
        </div>
      )}
      {jobs.length > 0 && (
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              {["Name", "Pipeline", "Device", "Status", "Created", "Actions"].map((h) => (
                <Th key={h}>{h}</Th>
              ))}
            </tr>
          </thead>
          <tbody>
            {jobs.map((j) => {
              const device: string = (j.params?.compute_device as string) ?? "";
              const deviceLabel: string = (j.params?.compute_device_label as string) ?? "";
              const isGpu = device === "gpu";
              const deviceBadge = device
                ? { bg: isGpu ? "#dbeafe" : "#f3f4f6", color: isGpu ? "#1e40af" : "#374151",
                    text: isGpu ? `⚡ ${deviceLabel || "GPU"}` : `⚙️ ${deviceLabel || "CPU"}` }
                : null;
              const nodeCount = (j.params?.node_count as number) ?? 0;
              const nodesDone = (j.params?.nodes_done as number) ?? 0;
              const pct = nodeCount > 0 ? Math.round((nodesDone / nodeCount) * 100) : null;
              const isExpRun = j.pipeline === "exp_run";
              const elapsedSec = j.status === "running"
                ? Math.round((Date.now() - new Date(j.created_at).getTime()) / 1000)
                : null;
              const etaSec = (pct !== null && pct > 5 && elapsedSec !== null)
                ? Math.round((elapsedSec / pct) * (100 - pct))
                : null;
              return (
              <tr key={j.id}>
                <Td>
                  <div style={{ fontWeight: 500 }}>{j.name}</div>
                  <div style={{ fontSize: 11, color: "#6b7280", fontFamily: "monospace" }}>
                    {j.id.slice(0, 8)}…
                  </div>
                  {/* Progress bar for running exp_run jobs */}
                  {j.status === "running" && isExpRun && nodeCount > 0 && (
                    <div style={{ marginTop: 4, display: "flex", alignItems: "center", gap: 6 }}>
                      <div style={{ flex: 1, height: 4, background: "#e5e7eb", borderRadius: 2, overflow: "hidden" }}>
                        <div style={{ height: "100%", width: `${pct ?? 0}%`, background: "#2563eb", borderRadius: 2, transition: "width 0.5s" }} />
                      </div>
                      <span style={{ fontSize: 10, color: "#6b7280", whiteSpace: "nowrap" }}>
                        {nodesDone}/{nodeCount} nodes{pct !== null ? ` (${pct}%)` : ""}
                        {elapsedSec !== null && ` · ${elapsedSec}s`}
                        {etaSec !== null && ` · ~${etaSec}s left`}
                      </span>
                    </div>
                  )}
                </Td>
                <Td>
                  <code style={{ fontSize: 12 }}>{j.pipeline}</code>
                </Td>
                <Td>
                  {deviceBadge
                    ? <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 6,
                                     background: deviceBadge.bg, color: deviceBadge.color,
                                     fontWeight: 600, whiteSpace: "nowrap" }}>
                        {deviceBadge.text}
                      </span>
                    : <span style={{ fontSize: 11, color: "#9ca3af" }}>—</span>}
                </Td>
                <Td>
                  <span style={{ display: "inline-block", padding: "1px 7px", borderRadius: 10,
                    background: statusBg(j.status), color: statusColor(j.status), fontWeight: 700, fontSize: 11 }}>
                    {j.status}
                  </span>
                  {j.status === "running" && elapsedSec !== null && !isExpRun && (
                    <div style={{ fontSize: 10, color: "#9ca3af" }}>{elapsedSec}s elapsed</div>
                  )}
                </Td>
                <Td>{fmtDateTimeCompact(j.created_at)}</Td>
                <Td>
                  <span style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                    {j.status === "completed" && (
                      <button
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 12, background: "#059669" }}
                        onClick={() => handleViewResults(j)}
                        title="Open result in Reports → Data tab"
                      >
                        📂 View in Reports
                      </button>
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
                      <button
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 12,
                          background: j.status === "running" ? "#ea580c" : "#d97706" }}
                        onClick={() => handleCancel(j.id)}
                        title={j.status === "running" ? "Abort this running job" : "Cancel this queued job"}
                      >
                        {j.status === "running" ? "❌ Abort" : "⏸ Cancel"}
                      </button>
                    )}
                  </span>
                </Td>
              </tr>
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
          onClose={() => setErrorModal(null)}
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
