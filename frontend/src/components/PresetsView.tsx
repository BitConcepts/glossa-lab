/**
 * Presets View — manage custom pipeline and experiment presets.
 * Supports add, duplicate, and delete for user-defined presets.
 */

import { useEffect, useState } from "react";
import {
  getCatalog,
  listPipelinePresets,
  createPipelinePreset,
  duplicatePipelinePreset,
  deletePipelinePreset,
  listExperimentPresets,
  createExperimentPreset,
  duplicateExperimentPreset,
  deleteExperimentPreset,
  CatalogPipeline,
} from "../api";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Preset = Record<string, any>;

export function PresetsView() {
  const [pipelinePresets, setPipelinePresets] = useState<Preset[]>([]);
  const [experimentPresets, setExperimentPresets] = useState<Preset[]>([]);
  const [availablePipelines, setAvailablePipelines] = useState<CatalogPipeline[]>([]);
  const [tab, setTab] = useState<"pipelines" | "experiments">("pipelines");

  // New pipeline preset form
  const [newPipeline, setNewPipeline] = useState("");
  const [newPipelineLabel, setNewPipelineLabel] = useState("");
  const [newPipelineParams, setNewPipelineParams] = useState("{}");

  // New experiment preset form
  const [newExpName, setNewExpName] = useState("");
  const [newExpCategory, setNewExpCategory] = useState("Analysis");
  const [newExpCommand, setNewExpCommand] = useState("");
  const [newExpDesc, setNewExpDesc] = useState("");

  const loadAll = async () => {
    const [pp, ep, cat] = await Promise.all([
      listPipelinePresets().catch(() => []),
      listExperimentPresets().catch(() => []),
      getCatalog().catch(() => null),
    ]);
    setPipelinePresets(pp);
    setExperimentPresets(ep);
    if (cat) setAvailablePipelines(cat.pipelines);
  };

  useEffect(() => { loadAll(); }, []);

  const handleAddPipeline = async () => {
    if (!newPipeline) return;
    let params: Record<string, unknown> = {};
    try { params = JSON.parse(newPipelineParams); } catch { alert("Params must be valid JSON"); return; }
    await createPipelinePreset({ pipeline: newPipeline, label: newPipelineLabel || newPipeline, default_params: params, group: "Custom", description: "", inputs: "", outputs: "", needs_lm: false });
    setNewPipeline(""); setNewPipelineLabel(""); setNewPipelineParams("{}");
    await loadAll();
  };

  const handleAddExperiment = async () => {
    if (!newExpName || !newExpCommand) return;
    await createExperimentPreset({ name: newExpName, category: newExpCategory, command: newExpCommand, description: newExpDesc, estimated_time: "varies" });
    setNewExpName(""); setNewExpCommand(""); setNewExpDesc("");
    await loadAll();
  };

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Presets</h2>
      <p style={{ color: "#6b7280", fontSize: 13, marginTop: 0 }}>
        Save custom pipeline and experiment configurations for quick reuse.
      </p>

      <nav style={{ display: "flex", gap: 4, marginBottom: "1.5rem" }}>
        {(["pipelines", "experiments"] as const).map((t) => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: "6px 16px", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 13,
            fontWeight: tab === t ? 600 : 400,
            background: tab === t ? "#1e3a5f" : "#f3f4f6",
            color: tab === t ? "#fff" : "#374151",
          }}>{t.charAt(0).toUpperCase() + t.slice(1)}</button>
        ))}
      </nav>

      {tab === "pipelines" && (
        <div>
          {/* Add form */}
          <details style={{ marginBottom: "1.5rem" }}>
            <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13 }}>+ Add pipeline preset</summary>
            <div style={{ marginTop: "0.75rem", padding: "1rem", border: "1px solid #e5e7eb", borderRadius: 6, maxWidth: 560 }}>
              <div style={{ marginBottom: 8 }}>
                <label style={labelStyle}>Pipeline</label>
                <select value={newPipeline} onChange={(e) => {
                  setNewPipeline(e.target.value);
                  const meta = availablePipelines.find((p) => p.id === e.target.value);
                  if (meta) setNewPipelineParams(JSON.stringify(meta.default_params, null, 2));
                }} style={inputStyle}>
                  <option value="">— select —</option>
                  {availablePipelines.map((p) => <option key={p.id} value={p.id}>{p.label}</option>)}
                </select>
              </div>
              <div style={{ marginBottom: 8 }}>
                <label style={labelStyle}>Label (optional)</label>
                <input value={newPipelineLabel} onChange={(e) => setNewPipelineLabel(e.target.value)} placeholder="My custom run" style={inputStyle} />
              </div>
              <div style={{ marginBottom: 8 }}>
                <label style={labelStyle}>Parameters (JSON)</label>
                <textarea value={newPipelineParams} onChange={(e) => setNewPipelineParams(e.target.value)} rows={4} style={{ ...inputStyle, fontFamily: "monospace", resize: "vertical" }} />
              </div>
              <button onClick={handleAddPipeline} disabled={!newPipeline} style={btnStyle}>Save preset</button>
            </div>
          </details>

          {/* Preset list */}
          {pipelinePresets.length === 0
            ? <p style={{ color: "#6b7280", fontSize: 13 }}>No custom pipeline presets yet.</p>
            : pipelinePresets.map((p) => (
              <div key={p.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 12px", border: "1px solid #e5e7eb", borderRadius: 6, marginBottom: 6 }}>
                <div style={{ flex: 1 }}>
                  <span style={{ fontWeight: 600, fontSize: 13 }}>{p.label || p.pipeline}</span>
                  <code style={{ marginLeft: 8, fontSize: 11, color: "#6b7280" }}>{p.pipeline}</code>
                </div>
                <button onClick={async () => { await duplicatePipelinePreset(p.id); await loadAll(); }} style={smallBtnStyle}>Duplicate</button>
                <button onClick={async () => { if (confirm("Delete?")) { await deletePipelinePreset(p.id); await loadAll(); } }} style={{ ...smallBtnStyle, color: "#dc2626", borderColor: "#fca5a5" }}>Delete</button>
              </div>
            ))
          }
        </div>
      )}

      {tab === "experiments" && (
        <div>
          {/* Add form */}
          <details style={{ marginBottom: "1.5rem" }}>
            <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13 }}>+ Add experiment preset</summary>
            <div style={{ marginTop: "0.75rem", padding: "1rem", border: "1px solid #e5e7eb", borderRadius: 6, maxWidth: 560 }}>
              {[
                { label: "Name", val: newExpName, set: setNewExpName, placeholder: "My experiment" },
                { label: "Command", val: newExpCommand, set: setNewExpCommand, placeholder: "python my_script.py" },
                { label: "Description", val: newExpDesc, set: setNewExpDesc, placeholder: "What this experiment does" },
              ].map(({ label, val, set, placeholder }) => (
                <div key={label} style={{ marginBottom: 8 }}>
                  <label style={labelStyle}>{label}</label>
                  <input value={val} onChange={(e) => set(e.target.value)} placeholder={placeholder} style={inputStyle} />
                </div>
              ))}
              <div style={{ marginBottom: 8 }}>
                <label style={labelStyle}>Category</label>
                <select value={newExpCategory} onChange={(e) => setNewExpCategory(e.target.value)} style={inputStyle}>
                  {["Analysis", "Validation", "Data Extraction", "Experiments"].map((c) => <option key={c}>{c}</option>)}
                </select>
              </div>
              <button onClick={handleAddExperiment} disabled={!newExpName || !newExpCommand} style={btnStyle}>Save preset</button>
            </div>
          </details>

          {experimentPresets.length === 0
            ? <p style={{ color: "#6b7280", fontSize: 13 }}>No custom experiment presets yet.</p>
            : experimentPresets.map((e) => (
              <div key={e.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 12px", border: "1px solid #e5e7eb", borderRadius: 6, marginBottom: 6 }}>
                <div style={{ flex: 1 }}>
                  <span style={{ fontWeight: 600, fontSize: 13 }}>{e.name}</span>
                  <span style={{ marginLeft: 8, fontSize: 11, color: "#6b7280" }}>{e.category}</span>
                </div>
                <button onClick={async () => { await duplicateExperimentPreset(e.id); await loadAll(); }} style={smallBtnStyle}>Duplicate</button>
                <button onClick={async () => { if (confirm("Delete?")) { await deleteExperimentPreset(e.id); await loadAll(); } }} style={{ ...smallBtnStyle, color: "#dc2626", borderColor: "#fca5a5" }}>Delete</button>
              </div>
            ))
          }
        </div>
      )}
    </div>
  );
}

const labelStyle: React.CSSProperties = { display: "block", fontSize: 12, fontWeight: 600, color: "#374151", marginBottom: 3 };
const inputStyle: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box" };
const btnStyle: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "6px 16px", fontSize: 13, cursor: "pointer" };
const smallBtnStyle: React.CSSProperties = { background: "none", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 11, padding: "2px 10px", cursor: "pointer", color: "#374151" };
