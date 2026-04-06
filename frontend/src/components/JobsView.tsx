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
import { ResultsView } from "./ResultsView";

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

  // Results drawer
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [viewResult, setViewResult] = useState<{ name: string; data: Record<string, any> } | null>(null);

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
    try {
      const data = await getJobResults(job.id);
      setViewResult({ name: job.name, data });
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed to load results");
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
    if (s === "failed") return "#dc2626";
    if (s === "running") return "#2563eb";
    return "#6b7280";
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
        <p style={{ color: "#6b7280" }}>No jobs yet.</p>
      )}
      {jobs.length > 0 && (
        <table style={{ borderCollapse: "collapse", width: "100%", maxWidth: 900 }}>
          <thead>
            <tr>
              {["Name", "Pipeline", "Status", "Created", "Actions"].map((h) => (
                <Th key={h}>{h}</Th>
              ))}
            </tr>
          </thead>
          <tbody>
            {jobs.map((j) => (
              <tr key={j.id}>
                <Td>
                  <span style={{ fontWeight: 500 }}>{j.name}</span>
                  <br />
                  <span style={{ fontSize: 11, color: "#6b7280", fontFamily: "monospace" }}>
                    {j.id.slice(0, 8)}…
                  </span>
                </Td>
                <Td>
                  <code style={{ fontSize: 12 }}>{j.pipeline}</code>
                </Td>
                <Td>
                  <span style={{ color: statusColor(j.status), fontWeight: 600 }}>
                    {j.status}
                  </span>
                </Td>
                <Td>{fmtDateTimeCompact(j.created_at)}</Td>
                <Td>
                  <span style={{ display: "flex", gap: 6 }}>
                    {j.status === "completed" && (
                      <button
                        style={{ ...btnStyle, padding: "2px 10px", fontSize: 12 }}
                        onClick={() => handleViewResults(j)}
                      >
                        Results
                      </button>
                    )}
                    {(j.status === "pending" || j.status === "running") && (
                      <button
                        style={{
                          ...btnStyle,
                          padding: "2px 10px",
                          fontSize: 12,
                          background: "#6b7280",
                        }}
                        onClick={() => handleCancel(j.id)}
                      >
                        Cancel
                      </button>
                    )}
                  </span>
                </Td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Results drawer */}
      {viewResult && (
        <div
          style={{
            marginTop: "2rem",
            padding: "1.25rem",
            border: "1px solid #e5e7eb",
            borderRadius: 6,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "0.75rem",
            }}
          >
            <strong>Results</strong>
            <button
              style={{ background: "none", border: "none", cursor: "pointer", fontSize: 18 }}
              onClick={() => setViewResult(null)}
            >
              ×
            </button>
          </div>
          <ResultsView result={viewResult.data} jobName={viewResult.name} />
        </div>
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
