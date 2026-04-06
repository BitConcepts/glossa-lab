/**
 * Experiments View — live CRUD for all discovered experiments.
 *
 * Features:
 *  - Lists experiments auto-discovered from backend/experiments/
 *  - Run an experiment in-place with live result display
 *  - Duplicate, delete experiments
 *  - AI-generate a new experiment from a natural-language prompt
 */

import { useEffect, useRef, useState, useCallback } from "react";
import {
  deleteExperiment,
  duplicateExperiment,
  generateExperiment,
  isLocalKeySet,
  listExperiments,
  reloadExperiments,
  runExperiment,
  type ExperimentMeta,
} from "../api";

const CATEGORY_COLORS: Record<string, string> = {
  "Data Extraction": "#7c3aed",
  Validation: "#16a34a",
  Analysis: "#2563eb",
  Experiments: "#d97706",
  Custom: "#6b7280",
};

function catColor(cat: string) {
  return CATEGORY_COLORS[cat] ?? "#6b7280";
}

// ── Generate dialog ────────────────────────────────────────────────────────────────

interface GenerateDialogProps {
  onClose: () => void;
  onCreated: () => void;
}

function GenerateDialog({ onClose, onCreated }: GenerateDialogProps) {
  const [name, setName] = useState("");
  const [category, setCategory] = useState("Analysis");
  const [prompt, setPrompt] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!name.trim() || !prompt.trim()) {
      setError("Name and description are required.");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await generateExperiment({ name: name.trim(), category, prompt: prompt.trim() });
      await reloadExperiments();
      onCreated();
      onClose();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  const backdropRef = useRef<HTMLDivElement>(null);

  return (
    <div
      ref={backdropRef}
      onClick={(ev) => { if (ev.target === backdropRef.current) onClose(); }}
      style={{
        position: "fixed", inset: 0, background: "rgba(0,0,0,0.45)",
        display: "flex", alignItems: "center", justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <div style={{
        background: "#fff", borderRadius: 12, padding: "1.75rem 2rem",
        width: 540, maxWidth: "95vw", boxShadow: "0 20px 60px rgba(0,0,0,0.2)",
      }}>
        <h3 style={{ margin: "0 0 1.25rem 0", color: "#111827", fontSize: 16 }}>
          ✨ AI-Generate Experiment
        </h3>

        <label style={labelStyle}>Experiment name</label>
        <input
          style={inputStyle}
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g. Markov Chain Analysis"
          autoFocus
        />

        <label style={labelStyle}>Category</label>
        <select
          style={{ ...inputStyle, cursor: "pointer" }}
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          {["Analysis", "Validation", "Data Extraction", "Experiments", "Custom"].map((c) => (
            <option key={c}>{c}</option>
          ))}
        </select>

        <label style={labelStyle}>Describe what the experiment should do</label>
        <textarea
          style={{ ...inputStyle, height: 100, resize: "vertical", fontFamily: "inherit" }}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Analyse bigram frequency distributions in the Fuls catalog and produce a heatmap JSON report…"
        />

        {!isLocalKeySet("openai_api_key") && (
          <div style={{
            background: "#fef3c7", border: "1px solid #fcd34d",
            borderRadius: 6, padding: "8px 12px", marginBottom: 12, fontSize: 12,
          }}>
            Requires <strong>openai_api_key</strong> — set it in the Settings tab first.
          </div>
        )}

        {error && (
          <div style={{
            background: "#fef2f2", border: "1px solid #fca5a5",
            borderRadius: 6, padding: "8px 12px", marginBottom: 12, fontSize: 12, color: "#b91c1c",
          }}>
            {error}
          </div>
        )}

        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 8 }}>
          <button onClick={onClose} style={btnSecondary} disabled={busy}>Cancel</button>
          <button onClick={handleGenerate} style={btnPrimary} disabled={busy}>
            {busy ? "Generating…" : "Generate"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Experiment card ───────────────────────────────────────────────────────────

interface CardProps {
  exp: ExperimentMeta;
  onDeleted: (id: string) => void;
  onDuplicated: () => void;
}

function ExperimentCard({ exp, onDeleted, onDuplicated }: CardProps) {
  const [expanded, setExpanded] = useState(false);
  const [running, setRunning] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [streamLines, setStreamLines] = useState<string[]>([]);
  const esRef = useRef<EventSource | null>(null);
  const [runResult, setRunResult] = useState<unknown | null>(null);
  const [runError, setRunError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [duplicating, setDuplicating] = useState(false);

  const color = catColor(exp.category);
  const needsKey = Boolean(exp.requires_key && !isLocalKeySet(exp.requires_key));

  const handleRun = async () => {
    setRunning(true);
    setRunResult(null);
    setRunError(null);
    if (!expanded) setExpanded(true);
    try {
      const res = await runExperiment(exp.id);
      setRunResult(res);
    } catch (e: unknown) {
      setRunError(e instanceof Error ? e.message : String(e));
    } finally {
      setRunning(false);
    }
  };

  const handleDelete = async () => {
    if (!confirmDelete) { setConfirmDelete(true); return; }
    setDeleting(true);
    try {
      await deleteExperiment(exp.id);
      onDeleted(exp.id);
    } catch (e: unknown) {
      setRunError(e instanceof Error ? e.message : String(e));
      setDeleting(false);
      setConfirmDelete(false);
    }
  };

  const stopStream = useCallback(() => {
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
    }
    setStreaming(false);
    setStreamLines((l) => [...l, "⏹ Stopped"]);
  }, []);

  const handleStream = () => {
    if (streaming) return;
    setStreaming(true);
    setStreamLines(["Starting…"]);
    setRunResult(null);
    setRunError(null);
    if (!expanded) setExpanded(true);
    const url = `/api/v1/experiments/${exp.id}/stream`;
    const es = new EventSource(url);
    esRef.current = es;
    es.addEventListener("started", () => {
      setStreamLines((l) => [...l, "▶ Running…"]);
    });
    es.addEventListener("heartbeat", (ev) => {
      const d = JSON.parse(ev.data) as { elapsed_s: number };
      setStreamLines((l) => [...l, `⏳ Elapsed: ${d.elapsed_s}s`]);
    });
    es.addEventListener("complete", (ev) => {
      const d = JSON.parse(ev.data) as { result: unknown };
      setRunResult(d.result);
      setStreamLines((l) => [...l, "✓ Complete"]);
      setStreaming(false);
      es.close();
      esRef.current = null;
    });
    es.addEventListener("error", (ev) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const data = (ev as any).data as string | undefined;
      const msg = data ? (JSON.parse(data) as { message: string }).message : "Connection error";
      setRunError(msg);
      setStreamLines((l) => [...l, `✗ Error: ${msg}`]);
      setStreaming(false);
      es.close();
      esRef.current = null;
    });
    es.onerror = () => {
      if (esRef.current) {
        setRunError("SSE connection lost");
        setStreaming(false);
        es.close();
        esRef.current = null;
      }
    };
  };

  const handleDuplicate = async () => {
    setDuplicating(true);
    try {
      await duplicateExperiment(exp.id);
      onDuplicated();
    } catch (e: unknown) {
      setRunError(e instanceof Error ? e.message : String(e));
    } finally {
      setDuplicating(false);
    }
  };

  return (
    <div style={{
      border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden",
      boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
    }}>
      {/* Header row */}
      <div style={{
        display: "flex", alignItems: "center", gap: 10, padding: "11px 14px",
        background: "#fafafa",
        borderBottom: expanded ? "1px solid #e5e7eb" : "none",
      }}>
        <span
          style={{ fontSize: 13, flex: 1, fontWeight: 600, cursor: "pointer", userSelect: "none" }}
          onClick={() => setExpanded((x) => !x)}
        >
          {exp.name}
        </span>

        <span style={{
          fontSize: 11, padding: "2px 7px", borderRadius: 10,
          background: color + "20", color, fontWeight: 600, whiteSpace: "nowrap",
        }}>
          {exp.category}
        </span>

        {exp.custom && (
          <span style={{
            fontSize: 10, padding: "1px 6px", borderRadius: 8,
            background: "#f3f4f6", color: "#6b7280", fontWeight: 600,
          }}>custom</span>
        )}

        <span style={{ fontSize: 11, color: "#9ca3af", whiteSpace: "nowrap" }}>
          {exp.estimated_time}
        </span>

        <button
          onClick={handleRun}
          disabled={running || streaming || needsKey}
          title={needsKey ? `Requires ${exp.requires_key}` : "Run (waits for full result)"}
          style={{
            ...btnSmall,
            background: needsKey ? "#f3f4f6" : running ? "#e0e7ff" : "#1e3a5f",
            color: needsKey ? "#9ca3af" : running ? "#4338ca" : "#fff",
            cursor: needsKey ? "not-allowed" : "pointer",
            minWidth: 52,
          }}
        >
          {running ? "Running…" : "▶ Run"}
        </button>
        {streaming ? (
          <button
            onClick={stopStream}
            title="Stop streaming"
            style={{
              ...btnSmall,
              background: "#fef2f2",
              color: "#b91c1c",
              border: "1px solid #fca5a5",
              minWidth: 52,
            }}
          >
            ⏹ Stop
          </button>
        ) : (
          <button
            onClick={handleStream}
            disabled={running || needsKey}
            title={needsKey ? `Requires ${exp.requires_key}` : "Stream — live heartbeat output, use for long runs"}
            style={{
              ...btnSmall,
              background: needsKey ? "#f3f4f6" : "#f3f4f6",
              color: needsKey ? "#9ca3af" : "#374151",
              cursor: needsKey ? "not-allowed" : "pointer",
              minWidth: 52,
            }}
          >
            ↯ Stream
          </button>
        )}

        <button
          onClick={handleDuplicate}
          disabled={duplicating}
          title="Duplicate experiment"
          style={{ ...btnSmall, background: "#f3f4f6", color: "#374151" }}
        >
          {duplicating ? "…" : "⎆"}
        </button>

        <button
          onClick={handleDelete}
          disabled={deleting}
          title={confirmDelete ? "Click again to confirm delete" : exp.custom ? "Delete experiment" : "Delete experiment (built-in — will remove from disk)"}
          style={{
            ...btnSmall,
            background: confirmDelete ? "#fef2f2" : "#f3f4f6",
            color: confirmDelete ? "#b91c1c" : "#6b7280",
            border: confirmDelete ? "1px solid #fca5a5" : "1px solid #e5e7eb",
          }}
        >
          {deleting ? "…" : confirmDelete ? "Confirm?" : "🗑"}
        </button>

        <span
          style={{ fontSize: 14, color: "#9ca3af", cursor: "pointer", userSelect: "none" }}
          onClick={() => setExpanded((x) => !x)}
        >
          {expanded ? "▲" : "▼"}
        </span>
      </div>

      {/* Expanded body */}
      {expanded && (
        <div style={{ padding: "14px 16px" }}>
          <p style={{ margin: "0 0 0.75rem", fontSize: 13, color: "#374151", lineHeight: 1.6 }}>
            {exp.description}
          </p>

          {needsKey && (
            <div style={{
              background: "#fef3c7", border: "1px solid #fcd34d",
              borderRadius: 6, padding: "8px 12px", marginBottom: "0.75rem", fontSize: 12,
            }}>
              Requires API key: <strong>{exp.requires_key}</strong> — set it in the Settings tab.
            </div>
          )}

          {exp.results_file && (
            <div style={{ fontSize: 12, color: "#6b7280", marginBottom: "0.75rem" }}>
              Results file: <code>{exp.results_file}</code>
            </div>
          )}

          {exp.source_file && (
            <div style={{ fontSize: 11, color: "#9ca3af", marginBottom: "0.75rem" }}>
              Source: <code>{exp.source_file}</code>
            </div>
          )}

          {exp.command && (
            <div style={{ marginBottom: "0.75rem" }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 4 }}>
                CLI command (run from repo root):
              </div>
              <pre style={{
                background: "#1e293b", color: "#e2e8f0", padding: "9px 13px",
                borderRadius: 6, fontSize: 12, fontFamily: "monospace",
                margin: 0, overflowX: "auto", lineHeight: 1.7,
              }}>
                {exp.command}
              </pre>
            </div>
          )}

          {streaming && streamLines.length > 0 && (
            <div style={{
              marginTop: "0.75rem",
              border: "1px solid #fcd34d",
              borderRadius: 6, overflow: "hidden",
            }}>
              <div style={{ background: "#fef3c7", padding: "6px 12px", fontSize: 12, fontWeight: 600, color: "#d97706" }}>
                Streaming output
              </div>
              <pre style={{
                background: "#1e293b", color: "#e2e8f0",
                margin: 0, padding: "10px 14px",
                fontSize: 11, fontFamily: "monospace",
                maxHeight: 200, overflowY: "auto", lineHeight: 1.6,
              }}>
                {streamLines.join("\n")}
              </pre>
            </div>
          )}

          {(runResult !== null || runError !== null) && (
            <div style={{
              marginTop: "0.75rem",
              border: `1px solid ${runError ? "#fca5a5" : "#86efac"}`,
              borderRadius: 6, overflow: "hidden",
            }}>
              <div style={{
                background: runError ? "#fef2f2" : "#f0fdf4",
                padding: "6px 12px", fontSize: 12, fontWeight: 600,
                color: runError ? "#b91c1c" : "#15803d",
              }}>
                {runError ? "Run failed" : "Run result"}
              </div>
              {runError ? (
                <div style={{ padding: "8px 12px", fontSize: 12, color: "#b91c1c" }}>{runError}</div>
              ) : (
                <pre style={{
                  background: "#1e293b", color: "#e2e8f0",
                  margin: 0, padding: "10px 14px",
                  fontSize: 11, fontFamily: "monospace",
                  maxHeight: 300, overflowY: "auto", overflowX: "auto",
                  lineHeight: 1.6,
                }}>
                  {JSON.stringify(runResult, null, 2)}
                </pre>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Main view ──────────────────────────────────────────────────────────────────

export function ExperimentsView() {
  const [experiments, setExperiments] = useState<ExperimentMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState("all");
  const [showGenerate, setShowGenerate] = useState(false);
  const [reloading, setReloading] = useState(false);

  const load = async () => {
    setError(null);
    try {
      const exps = await listExperiments();
      setExperiments(exps);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void load(); }, []);

  const handleReload = async () => {
    setReloading(true);
    try {
      await reloadExperiments();
      await load();
    } finally {
      setReloading(false);
    }
  };

  const handleDeleted = (id: string) =>
    setExperiments((prev) => prev.filter((e) => e.id !== id));

  const categories = ["all", ...Array.from(new Set(experiments.map((e) => e.category)))];

  const visible =
    filter === "all" ? experiments : experiments.filter((e) => e.category === filter);

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "0.25rem" }}>
        <h2 style={{ marginTop: 0 }}>Experiments</h2>
        <div style={{ display: "flex", gap: 6 }}>
          <button
            onClick={handleReload}
            disabled={reloading}
            style={{ ...btnSmall, background: "#f3f4f6", color: "#374151", fontSize: 12 }}
            title="Re-scan experiments directory"
          >
            {reloading ? "Scanning…" : "⟳ Reload"}
          </button>
          <button
            onClick={() => setShowGenerate(true)}
            style={{ ...btnSmall, background: "#1e3a5f", color: "#fff", fontSize: 12 }}
          >
            ✨ Generate
          </button>
        </div>
      </div>

      <p style={{ margin: "0 0 1.25rem", fontSize: 13, color: "#6b7280" }}>
        {experiments.length} experiment{experiments.length !== 1 ? "s" : ""} discovered.
        Run any experiment directly from the browser, or copy the CLI command below each card.
        Custom experiments (marked <strong>custom</strong>) can be deleted.
      </p>

      <nav style={{ display: "flex", gap: 6, marginBottom: "1.25rem", flexWrap: "wrap" }}>
        {categories.map((c) => {
          const color = c === "all" ? "#1e3a5f" : (catColor(c) ?? "#1e3a5f");
          const active = filter === c;
          return (
            <button
              key={c}
              onClick={() => setFilter(c)}
              style={{
                padding: "4px 14px", border: "1px solid", borderRadius: 20,
                cursor: "pointer", fontSize: 12, fontWeight: active ? 600 : 400,
                background: active ? color : "#fff",
                borderColor: active ? color : "#d1d5db",
                color: active ? "#fff" : "#374151",
              }}
            >
              {c.charAt(0).toUpperCase() + c.slice(1)}
              {c !== "all" && (
                <span style={{
                  marginLeft: 5, fontSize: 10,
                  background: active ? "rgba(255,255,255,0.3)" : "#f3f4f6",
                  color: active ? "#fff" : "#6b7280",
                  padding: "0 4px", borderRadius: 6, fontWeight: 700,
                }}>
                  {experiments.filter((e) => e.category === c).length}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {loading && (
        <div style={{ color: "#6b7280", fontSize: 13 }}>Loading experiments…</div>
      )}

      {error && (
        <div style={{
          background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 8,
          padding: "12px 16px", fontSize: 13, color: "#b91c1c", marginBottom: "1rem",
        }}>
          Could not load experiments: {error}
        </div>
      )}

      {!loading && !error && visible.length === 0 && (
        <div style={{ color: "#6b7280", fontSize: 13 }}>
          No experiments found. Use <strong>✨ Generate</strong> to create one.
        </div>
      )}

      <div style={{ display: "grid", gap: "0.75rem" }}>
        {visible.map((exp) => (
          <ExperimentCard
            key={exp.id}
            exp={exp}
            onDeleted={handleDeleted}
            onDuplicated={load}
          />
        ))}
      </div>

      {showGenerate && (
        <GenerateDialog
          onClose={() => setShowGenerate(false)}
          onCreated={load}
        />
      )}
    </div>
  );
}

// ── Shared micro-styles ─────────────────────────────────────────────────────────────────

const inputStyle: React.CSSProperties = {
  display: "block", width: "100%", boxSizing: "border-box",
  padding: "7px 10px", border: "1px solid #d1d5db", borderRadius: 6,
  fontSize: 13, marginBottom: 12, outline: "none",
};

const labelStyle: React.CSSProperties = {
  display: "block", fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 4,
};

const btnSmall: React.CSSProperties = {
  padding: "4px 10px", border: "1px solid transparent", borderRadius: 5,
  cursor: "pointer", fontSize: 12, fontWeight: 600,
  background: "#f3f4f6", color: "#374151",
};

const btnPrimary: React.CSSProperties = {
  padding: "7px 18px", border: "none", borderRadius: 6,
  cursor: "pointer", fontSize: 13, fontWeight: 600,
  background: "#1e3a5f", color: "#fff",
};

const btnSecondary: React.CSSProperties = {
  padding: "7px 18px", border: "1px solid #d1d5db", borderRadius: 6,
  cursor: "pointer", fontSize: 13, fontWeight: 400,
  background: "#fff", color: "#374151",
};

