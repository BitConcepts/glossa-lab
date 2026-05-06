/**
 * CASModelView — Graphical CAS-YAML constraint model editor.
 *
 * Users define constraint models here instead of writing YAML by hand.
 * Models are saved to the DB and used in graph experiments via the
 * CASModelLoader node in the Experiment Builder palette.
 *
 * CPSC integration: models are run by the CASProjector or CASIndusEngine
 * nodes using CPSC's IterativeEngine/CellularEngine under the hood.
 */

import { useEffect, useState, useCallback, useRef } from "react";
import {
  listCASModels,
  createCASModel,
  updateCASModel,
  deleteCASModel,
  validateCASModel,
  type CASModel,
  type CASValidateResult,
} from "../api";

// ── Types ─────────────────────────────────────────────────────────────────────

interface Variable {
  name: string;
  type: string;
  domain_min: number;
  domain_max: number;
  derived: boolean;
  description: string;
}

interface Constraint {
  id: string;
  expression: string;
  description: string;
}

interface ModelForm {
  name: string;
  description: string;
  engine_hint: string;  // auto | iterative | cellular
  variables: Variable[];
  dof_free: string[];  // names of free (DoF) variables
  constraints: Constraint[];
  max_iterations: number;
  convergence_epsilon: number;
  strategy: string;
}

const EMPTY_FORM: ModelForm = {
  name: "",
  description: "",
  engine_hint: "auto",
  variables: [],
  dof_free: [],
  constraints: [],
  max_iterations: 200,
  convergence_epsilon: 0.00001,
  strategy: "auto",
};

const EMPTY_VAR: Variable = {
  name: "", type: "float", domain_min: 0.0, domain_max: 1.0, derived: false, description: "",
};
const EMPTY_CON: Constraint = { id: "", expression: "", description: "" };

// ── Helpers ────────────────────────────────────────────────────────────────

function formToYaml(form: ModelForm): string {
  const freeVars   = form.variables.filter(v => !v.derived && form.dof_free.includes(v.name));
  const derivedVars = form.variables.filter(v => v.derived);
  const allVars    = [...freeVars, ...derivedVars,
                      ...form.variables.filter(v => !v.derived && !form.dof_free.includes(v.name))];

  const varLines = allVars.map(v => [
    `    - name: ${v.name || "unnamed"}`,
    `      type: ${v.type}`,
    `      domain: [${v.domain_min}, ${v.domain_max}]`,
    v.derived ? `      derived: true` : null,
    v.description ? `      description: "${v.description.replace(/"/g, '\\"')}"` : null,
  ].filter(Boolean).join("\n")).join("\n\n");

  const freeLines = form.dof_free.length > 0
    ? form.dof_free.map(n => `    - ${n}`).join("\n")
    : "    - (none — set at least one variable as free/DoF)";

  const conLines = form.constraints.map(c => [
    `  - id: ${c.id || "unnamed"}`,
    `    expression: "${c.expression.replace(/"/g, '\\"')}"`,
    c.description ? `    description: "${c.description.replace(/"/g, '\\"')}"` : null,
  ].filter(Boolean).join("\n")).join("\n\n");

  return [
    `version: "1.0"`,
    `model_id: ${form.name.toLowerCase().replace(/\s+/g, "_") || "my_model"}`,
    form.description ? `description: "${form.description}"` : "",
    ``,
    `state:`,
    `  variables:`,
    varLines || `    (no variables defined)`,
    ``,
    `degrees_of_freedom:`,
    `  free:`,
    freeLines,
    ``,
    `constraints:`,
    conLines || `  (no constraints defined)`,
    ``,
    `projection:`,
    `  method: bounded_relaxation`,
    `  max_iterations: ${form.max_iterations}`,
    `  convergence_epsilon: ${form.convergence_epsilon}`,
    `  strategy: ${form.strategy}`,
    ``,
    `execution:`,
    `  deterministic: true`,
    `  numeric_mode: float64`,
    `  precision_bits: 64`,
  ].filter(l => l !== null).join("\n");
}

// ── Component ──────────────────────────────────────────────────────────────────

export function CASModelView() {
  const [models, setModels]       = useState<CASModel[]>([]);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<CASModel | null>(null);
  const [form, setForm]           = useState<ModelForm>(EMPTY_FORM);
  const [tab, setTab]             = useState<"editor" | "yaml">("editor");
  const [saving, setSaving]       = useState(false);
  const [validating, setValidating] = useState(false);
  const [validation, setValidation] = useState<CASValidateResult | null>(null);
  const [error, setError]         = useState<string | null>(null);
  const [yamlPreview, setYamlPreview] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const all = await listCASModels();
      setModels(all);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  // Regenerate YAML preview whenever form changes
  useEffect(() => {
    setYamlPreview(formToYaml(form));
  }, [form]);

  const selectModel = (m: CASModel) => {
    setSelected(m);
    setValidation(null);
    setError(null);
    // Can't reconstruct full form from stored YAML, so show a new empty editor
    // In production, parse the YAML back; for now, load the raw YAML in the YAML tab
    setForm({ ...EMPTY_FORM, name: m.name, description: m.description, engine_hint: m.engine_hint });
    setTab("yaml");
  };

  const newModel = () => {
    setSelected(null);
    setForm({ ...EMPTY_FORM });
    setValidation(null);
    setError(null);
    setTab("editor");
  };

  const save = async () => {
    if (!form.name.trim()) { setError("Name is required"); return; }
    setSaving(true); setError(null);
    try {
      const yaml_text = tab === "yaml" ? yamlPreview : formToYaml(form);
      if (selected && !selected.is_builtin) {
        const updated = await updateCASModel(selected.id, {
          name: form.name, description: form.description,
          yaml_text, engine_hint: form.engine_hint,
        });
        setSelected(updated);
      } else {
        const created = await createCASModel({
          name: form.name, description: form.description,
          yaml_text, engine_hint: form.engine_hint,
        });
        setSelected(created);
      }
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const validate = async () => {
    if (!selected) { setError("Save the model first, then validate"); return; }
    setValidating(true); setValidation(null); setError(null);
    try {
      const r = await validateCASModel(selected.id);
      setValidation(r);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Validation failed");
    } finally {
      setValidating(false);
    }
  };

  const deleteModel = async (m: CASModel) => {
    if (m.is_builtin) { setError("Built-in models cannot be deleted"); return; }
    if (!confirm(`Delete model "${m.name}"?`)) return;
    try {
      await deleteCASModel(m.id);
      if (selected?.id === m.id) { setSelected(null); setForm(EMPTY_FORM); }
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Delete failed");
    }
  };

  // ── Variable helpers ───────────────────────────────────────────────────────
  const addVar = () => setForm(f => ({ ...f, variables: [...f.variables, { ...EMPTY_VAR }] }));
  const updateVar = (idx: number, patch: Partial<Variable>) =>
    setForm(f => {
      const vars = f.variables.map((v, i) => i === idx ? { ...v, ...patch } : v);
      // Sync dof_free: remove if now derived, add if free and not already in list
      const v = vars[idx];
      let free = f.dof_free;
      if (patch.derived !== undefined) {
        if (v.derived) free = free.filter(n => n !== v.name);
        else if (v.name && !free.includes(v.name)) free = [...free, v.name];
      }
      if (patch.name !== undefined && !v.derived) {
        const old = f.variables[idx].name;
        free = free.map(n => n === old ? (patch.name as string) : n);
      }
      return { ...f, variables: vars, dof_free: free };
    });
  const removeVar = (idx: number) =>
    setForm(f => {
      const name = f.variables[idx]?.name;
      return { ...f,
        variables: f.variables.filter((_, i) => i !== idx),
        dof_free: f.dof_free.filter(n => n !== name),
      };
    });
  const toggleFree = (name: string) =>
    setForm(f => ({
      ...f,
      dof_free: f.dof_free.includes(name) ? f.dof_free.filter(n => n !== name) : [...f.dof_free, name],
    }));

  // ── Constraint helpers ─────────────────────────────────────────────────────
  const addCon = () => setForm(f => ({ ...f, constraints: [...f.constraints, { ...EMPTY_CON }] }));
  const updateCon = (idx: number, patch: Partial<Constraint>) =>
    setForm(f => ({ ...f, constraints: f.constraints.map((c, i) => i === idx ? { ...c, ...patch } : c) }));
  const removeCon = (idx: number) =>
    setForm(f => ({ ...f, constraints: f.constraints.filter((_, i) => i !== idx) }));

  // ── Resizable left panel ────────────────────────────────────────────────────
  const [leftW, setLeftW] = useState(260);
  const isDragging = useRef(false);
  const dragStart = useRef(0);
  const dragW0 = useRef(0);
  const onDividerDown = useCallback((e: React.MouseEvent) => {
    isDragging.current = true; dragStart.current = e.clientX; dragW0.current = leftW;
    const onMove = (me: MouseEvent) => { if (!isDragging.current) return; setLeftW(Math.max(180, Math.min(460, dragW0.current + me.clientX - dragStart.current))); };
    const onUp = () => { isDragging.current = false; document.removeEventListener("mousemove", onMove); document.removeEventListener("mouseup", onUp); };
    document.addEventListener("mousemove", onMove); document.addEventListener("mouseup", onUp);
  }, [leftW]);

  // ── Styles ─────────────────────────────────────────────────────────────────
  const bg = "#f8fafc", cardBg = "#fff", border = "#e5e7eb";
  const muted = "#6b7280", blue = "#2563eb", indigo = "#4f46e5";
  const inp: React.CSSProperties = {
    width: "100%", border: `1px solid ${border}`, borderRadius: 4,
    padding: "4px 8px", fontSize: 12, boxSizing: "border-box",
  };
  const btn: React.CSSProperties = {
    border: "none", borderRadius: 5, cursor: "pointer",
    padding: "5px 12px", fontSize: 12, fontWeight: 600,
  };

  return (
    <div style={{ display: "flex", height: "100%", gap: 0, background: bg, overflow: "hidden" }}>

      {/* ── Left panel: model list ──────────────────────────────────── */}
      <div style={{ width: leftW, borderRight: `1px solid ${border}`, display: "flex",
                    flexDirection: "column", overflow: "hidden", flexShrink: 0 }}>
        <div style={{ padding: "12px 14px", borderBottom: `1px solid ${border}`,
                      display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <span style={{ fontWeight: 700, fontSize: 13 }}>CAS Models</span>
          <button onClick={newModel} style={{ ...btn, background: blue, color: "#fff", padding: "3px 10px" }}>
            + New
          </button>
        </div>

        <div style={{ flex: 1, overflowY: "auto", padding: "6px 0" }}>
          {loading && <div style={{ padding: "12px 14px", color: muted, fontSize: 12 }}>Loading…</div>}
          {!loading && models.length === 0 && (
            <div style={{ padding: "12px 14px", color: muted, fontSize: 12, lineHeight: 1.6 }}>
              No models yet. Click <strong>+ New</strong> to create one,<br/>
              or run the backend to load built-in models.
            </div>
          )}
          {models.map(m => (
            <div key={m.id}
              onClick={() => selectModel(m)}
              style={{
                padding: "8px 14px", cursor: "pointer", borderLeft: "3px solid transparent",
                background: selected?.id === m.id ? "#eff6ff" : "none",
                borderLeftColor: selected?.id === m.id ? blue : "transparent",
                display: "flex", alignItems: "center", gap: 6,
              }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 12, fontWeight: 600, whiteSpace: "nowrap",
                              overflow: "hidden", textOverflow: "ellipsis" }}>
                  {m.is_builtin ? "⚙️ " : "📋 "}{m.name}
                </div>
                {m.description && (
                  <div style={{ fontSize: 10, color: muted, whiteSpace: "nowrap",
                                overflow: "hidden", textOverflow: "ellipsis" }}>
                    {m.description.slice(0, 50)}
                  </div>
                )}
              </div>
              {!m.is_builtin && (
                <button onClick={e => { e.stopPropagation(); deleteModel(m); }}
                  style={{ ...btn, background: "none", color: "#9ca3af", padding: "1px 4px", fontSize: 13 }}
                  title="Delete">×</button>
              )}
            </div>
          ))}
        </div>

        {/* Built-in models info */}
        <div style={{ padding: "10px 14px", borderTop: `1px solid ${border}`, background: "#f1f5f9" }}>
          <div style={{ fontSize: 10, color: muted, lineHeight: 1.6 }}>
            <strong>Built-in models</strong> (⚙️) are protected and come from{" "}
            <code>data/cas_models/</code>. They appear in CASModelLoader
            palette node as <code>builtin</code> parameter.
          </div>
        </div>
      </div>

      {/* ── Resize divider ──────────────────────────────────────────── */}
      <div
        onMouseDown={onDividerDown}
        style={{ width: 4, cursor: "col-resize", background: bg, flexShrink: 0,
          borderLeft: `1px solid ${border}`, transition: "border-color 0.1s" }}
        onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderLeftColor = "#94a3b8"; }}
        onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderLeftColor = border; }}
      />

      {/* ── Right panel: editor ─────────────────────────────────────── */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>

        {/* Header */}
        <div style={{ padding: "10px 20px", borderBottom: `1px solid ${border}`,
                      display: "flex", alignItems: "center", gap: 10, background: cardBg, flexShrink: 0 }}>
          <div style={{ flex: 1 }}>
            <input
              value={form.name}
              onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
              placeholder="Model name (e.g. My Dravidian Constraints)"
              style={{ ...inp, fontSize: 14, fontWeight: 600, border: "none",
                       borderBottom: `1px solid ${border}`, borderRadius: 0, padding: "2px 0" }}
              readOnly={!!selected?.is_builtin}
            />
          </div>
          <select value={form.engine_hint}
            onChange={e => setForm(f => ({ ...f, engine_hint: e.target.value }))}
            style={{ ...inp, width: "auto" }} disabled={!!selected?.is_builtin}>
            <option value="auto">Engine: auto</option>
            <option value="iterative">Engine: iterative</option>
            <option value="cellular">Engine: cellular</option>
          </select>
          <button onClick={save} disabled={saving || !!selected?.is_builtin}
            style={{ ...btn, background: blue, color: "#fff" }}>
            {saving ? "Saving…" : (selected ? "Save" : "Create")}
          </button>
          {selected && (
            <button onClick={validate} disabled={validating}
              style={{ ...btn, background: "#10b981", color: "#fff" }}>
              {validating ? "Validating…" : "✓ Validate"}
            </button>
          )}
        </div>

        {/* Validation banner */}
        {validation && (
          <div style={{
            padding: "8px 20px", fontSize: 12,
            background: validation.valid ? "#dcfce7" : "#fee2e2",
            color: validation.valid ? "#15803d" : "#991b1b",
            borderBottom: `1px solid ${validation.valid ? "#86efac" : "#fca5a5"}`,
            flexShrink: 0,
          }}>
            {validation.valid
              ? `✓ Valid — ${validation.n_variables} variables, ${validation.n_constraints} constraints, DoF: [${validation.dof_vars.join(", ")}]. Projection dry-run: ${validation.dry_run_success ? "converged" : "not converged"} (max_violation=${(validation.dry_run_violation ?? 0).toFixed(4)})`
              : `✗ ${validation.error}`}
          </div>
        )}
        {error && (
          <div style={{ padding: "8px 20px", fontSize: 12, background: "#fee2e2",
                        color: "#991b1b", borderBottom: `1px solid #fca5a5`, flexShrink: 0 }}>
            {error}
          </div>
        )}

        {/* Tab bar */}
        <div style={{ display: "flex", borderBottom: `1px solid ${border}`, background: cardBg, flexShrink: 0 }}>
          {(["editor", "yaml"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              style={{ ...btn, borderRadius: 0, background: tab === t ? "#eff6ff" : "none",
                       borderBottom: tab === t ? `2px solid ${blue}` : "2px solid transparent",
                       color: tab === t ? blue : muted, padding: "8px 18px" }}>
              {t === "editor" ? "🖊 Form Editor" : "📄 YAML Preview"}
            </button>
          ))}
          <div style={{ flex: 1, padding: "6px 14px", fontSize: 11, color: muted, alignSelf: "center" }}>
            {selected?.is_builtin && "Built-in model — read only. Fork it with New to modify."}
            {!selected && "New model — fill in the form or paste YAML, then Create."}
          </div>
        </div>

        {/* Content */}
        <div style={{ flex: 1, overflow: "auto", padding: 20 }}>

          {tab === "editor" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>

              {/* Description */}
              <div>
                <label style={{ fontSize: 11, fontWeight: 700, color: muted, display: "block", marginBottom: 4 }}>
                  DESCRIPTION
                </label>
                <textarea
                  value={form.description}
                  onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                  rows={2}
                  placeholder="What does this model compute or constrain?"
                  style={{ ...inp, resize: "vertical" }}
                  readOnly={!!selected?.is_builtin}
                />
              </div>

              {/* Variables */}
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                  <label style={{ fontSize: 11, fontWeight: 700, color: muted }}>VARIABLES</label>
                  {!selected?.is_builtin && (
                    <button onClick={addVar}
                      style={{ ...btn, background: indigo, color: "#fff", padding: "2px 8px", fontSize: 11 }}>
                      + Add Variable
                    </button>
                  )}
                  <span style={{ fontSize: 10, color: muted }}>
                    Free (DoF) = checked checkbox. Derived = computed from constraints.
                  </span>
                </div>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                  <thead>
                    <tr style={{ background: "#f8fafc" }}>
                      {["Free (DoF)", "Name", "Type", "Domain Min", "Domain Max", "Derived", "Description", ""].map(h => (
                        <th key={h} style={{ padding: "5px 8px", textAlign: "left", fontWeight: 600,
                                             borderBottom: `1px solid ${border}`, color: muted, fontSize: 11 }}>
                          {h}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {form.variables.map((v, i) => (
                      <tr key={i} style={{ borderBottom: `1px solid ${border}` }}>
                        <td style={{ padding: "4px 8px" }}>
                          <input type="checkbox"
                            checked={!v.derived && form.dof_free.includes(v.name)}
                            disabled={v.derived || !!selected?.is_builtin}
                            onChange={() => toggleFree(v.name)} />
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          <input value={v.name} onChange={e => updateVar(i, { name: e.target.value })}
                            style={{ ...inp, width: 110 }} readOnly={!!selected?.is_builtin}
                            placeholder="var_name" />
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          <select value={v.type} onChange={e => updateVar(i, { type: e.target.value })}
                            style={{ ...inp, width: 70 }} disabled={!!selected?.is_builtin}>
                            <option>float</option><option>int</option><option>bool</option>
                          </select>
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          <input type="number" value={v.domain_min}
                            onChange={e => updateVar(i, { domain_min: parseFloat(e.target.value) })}
                            style={{ ...inp, width: 70 }} readOnly={!!selected?.is_builtin} />
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          <input type="number" value={v.domain_max}
                            onChange={e => updateVar(i, { domain_max: parseFloat(e.target.value) })}
                            style={{ ...inp, width: 70 }} readOnly={!!selected?.is_builtin} />
                        </td>
                        <td style={{ padding: "4px 8px", textAlign: "center" }}>
                          <input type="checkbox" checked={v.derived}
                            disabled={!!selected?.is_builtin}
                            onChange={e => updateVar(i, { derived: e.target.checked })} />
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          <input value={v.description}
                            onChange={e => updateVar(i, { description: e.target.value })}
                            style={{ ...inp, width: 180 }} readOnly={!!selected?.is_builtin}
                            placeholder="Optional description" />
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          {!selected?.is_builtin && (
                            <button onClick={() => removeVar(i)}
                              style={{ ...btn, background: "none", color: "#9ca3af", padding: "0 4px" }}>×</button>
                          )}
                        </td>
                      </tr>
                    ))}
                    {form.variables.length === 0 && (
                      <tr><td colSpan={8} style={{ padding: "12px 8px", color: muted, fontSize: 12, textAlign: "center" }}>
                        No variables yet. Add variables above.
                      </td></tr>
                    )}
                  </tbody>
                </table>
              </div>

              {/* Constraints */}
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                  <label style={{ fontSize: 11, fontWeight: 700, color: muted }}>CONSTRAINTS</label>
                  {!selected?.is_builtin && (
                    <button onClick={addCon}
                      style={{ ...btn, background: indigo, color: "#fff", padding: "2px 8px", fontSize: 11 }}>
                      + Add Constraint
                    </button>
                  )}
                  <span style={{ fontSize: 10, color: muted }}>
                    Expressions: <code>derived_var = expr</code> or <code>var == target</code> or predicates like <code>x &gt;= 0.5</code>
                  </span>
                </div>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                  <thead>
                    <tr style={{ background: "#f8fafc" }}>
                      {["ID", "Expression", "Description", ""].map(h => (
                        <th key={h} style={{ padding: "5px 8px", textAlign: "left", fontWeight: 600,
                                             borderBottom: `1px solid ${border}`, color: muted, fontSize: 11 }}>
                          {h}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {form.constraints.map((c, i) => (
                      <tr key={i} style={{ borderBottom: `1px solid ${border}` }}>
                        <td style={{ padding: "4px 8px" }}>
                          <input value={c.id} onChange={e => updateCon(i, { id: e.target.value })}
                            style={{ ...inp, width: 130 }} placeholder="c_name"
                            readOnly={!!selected?.is_builtin} />
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          <input value={c.expression} onChange={e => updateCon(i, { expression: e.target.value })}
                            style={{ ...inp, width: 280, fontFamily: "monospace" }}
                            placeholder='e.g. "sum_val = x0 + x1"'
                            readOnly={!!selected?.is_builtin} />
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          <input value={c.description} onChange={e => updateCon(i, { description: e.target.value })}
                            style={{ ...inp, width: 200 }} placeholder="Optional"
                            readOnly={!!selected?.is_builtin} />
                        </td>
                        <td style={{ padding: "4px 8px" }}>
                          {!selected?.is_builtin && (
                            <button onClick={() => removeCon(i)}
                              style={{ ...btn, background: "none", color: "#9ca3af", padding: "0 4px" }}>×</button>
                          )}
                        </td>
                      </tr>
                    ))}
                    {form.constraints.length === 0 && (
                      <tr><td colSpan={4} style={{ padding: "12px 8px", color: muted, fontSize: 12, textAlign: "center" }}>
                        No constraints yet.
                      </td></tr>
                    )}
                  </tbody>
                </table>
              </div>

              {/* Projection config */}
              <div>
                <label style={{ fontSize: 11, fontWeight: 700, color: muted, display: "block", marginBottom: 8 }}>
                  PROJECTION CONFIG (CPSC engine settings)
                </label>
                <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
                  <div>
                    <label style={{ fontSize: 11, color: muted }}>Max Iterations</label>
                    <input type="number" value={form.max_iterations}
                      onChange={e => setForm(f => ({ ...f, max_iterations: parseInt(e.target.value) || 200 }))}
                      style={{ ...inp, width: 100, marginTop: 2 }}
                      readOnly={!!selected?.is_builtin} />
                  </div>
                  <div>
                    <label style={{ fontSize: 11, color: muted }}>Convergence ε</label>
                    <input type="number" step="0.000001" value={form.convergence_epsilon}
                      onChange={e => setForm(f => ({ ...f, convergence_epsilon: parseFloat(e.target.value) || 1e-5 }))}
                      style={{ ...inp, width: 120, marginTop: 2 }}
                      readOnly={!!selected?.is_builtin} />
                  </div>
                  <div>
                    <label style={{ fontSize: 11, color: muted }}>Strategy</label>
                    <select value={form.strategy}
                      onChange={e => setForm(f => ({ ...f, strategy: e.target.value }))}
                      style={{ ...inp, width: 130, marginTop: 2 }}
                      disabled={!!selected?.is_builtin}>
                      <option value="auto">auto (adaptive)</option>
                      <option value="iterative">iterative (gradient)</option>
                      <option value="cellular">cellular (local rules)</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Usage guide */}
              <div style={{ background: "#eff6ff", border: `1px solid #bfdbfe`, borderRadius: 8, padding: 14 }}>
                <div style={{ fontWeight: 700, fontSize: 12, color: "#1e40af", marginBottom: 6 }}>
                  📋 How to use this model in an experiment
                </div>
                <ol style={{ margin: 0, paddingLeft: 18, fontSize: 12, color: "#1e40af", lineHeight: 1.8 }}>
                  <li>Save/create the model here</li>
                  <li>Open the Experiment Builder and drag <strong>CAS Model Loader</strong> from the <strong>CPSC / Constraint Solver</strong> palette category</li>
                  <li>Set the model_id param to this model's ID, or use <strong>builtin</strong> for built-in models</li>
                  <li>Connect <strong>CAS Model Loader → model → CAS Projector</strong> (or CAS Indus Engine)</li>
                  <li>Supply DoF values from upstream nodes or as inline JSON params</li>
                </ol>
              </div>
            </div>
          )}

          {tab === "yaml" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12, height: "100%" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ fontSize: 11, fontWeight: 700, color: muted }}>
                  {selected ? `CAS-YAML for "${selected.name}"` : "Generated CAS-YAML preview"}
                </span>
                {selected?.is_builtin && (
                  <span style={{ fontSize: 10, color: "#d97706", background: "#fef3c7",
                                 padding: "2px 8px", borderRadius: 4 }}>built-in (read-only)</span>
                )}
              </div>
              <textarea
                value={selected ? selected.yaml_text : yamlPreview}
                onChange={e => {
                  if (!selected?.is_builtin) {
                    setYamlPreview(e.target.value);
                    // When user edits the YAML preview, save it as the canonical form
                    if (selected) setSelected(prev => prev ? { ...prev, yaml_text: e.target.value } : null);
                  }
                }}
                readOnly={!!selected?.is_builtin}
                style={{
                  flex: 1, minHeight: 500,
                  fontFamily: "monospace", fontSize: 12, lineHeight: 1.6,
                  border: `1px solid ${border}`, borderRadius: 6, padding: 14,
                  background: selected?.is_builtin ? "#f8fafc" : "#fff",
                  resize: "vertical",
                }}
              />
              {!selected?.is_builtin && (
                <div style={{ fontSize: 11, color: muted }}>
                  Tip: Edit YAML directly then click <strong>Save</strong> — the YAML is stored as-is.
                  Switch to Form Editor to build constraints interactively.
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
