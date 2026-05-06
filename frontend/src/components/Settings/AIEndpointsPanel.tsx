/**
 * AIEndpointsPanel — register custom OpenAI-compatible AI endpoints.
 *
 * Distinct from the cloud API keys (Mistral / OpenAI / Anthropic / Google)
 * and from Ollama. Use this panel to plug in vLLM, LM Studio, OpenRouter,
 * Together, Groq, Fireworks, Azure OpenAI deployments, etc.
 *
 * Each saved endpoint can be referenced by an AI Profile (see AIProfilesPanel)
 * via backend_kind="endpoint" + backend_ref=<endpoint id>.
 */

import { useCallback, useEffect, useMemo, useState } from "react";
// (useCallback + useMemo + useState all in use below)
import {
  createAIEndpoint, deleteAIEndpoint, listAIEndpointPresets, listAIEndpoints,
  updateAIEndpoint, verifyAIEndpoint, verifyAIEndpointConfig,
  type AIEndpoint, type AIEndpointPreset,
} from "../../api";
import { useToast } from "../../hooks/useToast";

interface DraftEndpoint {
  name: string;
  endpoint_kind: string;
  base_url: string;
  api_key: string;
  default_model: string;
  notes: string;
}

const EMPTY: DraftEndpoint = {
  name: "", endpoint_kind: "openai_compatible",
  base_url: "", api_key: "", default_model: "", notes: "",
};

export function AIEndpointsPanel() {
  const { toast } = useToast();
  const [presets, setPresets] = useState<AIEndpointPreset[]>([]);
  const [items, setItems] = useState<AIEndpoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [busyDraft, setBusyDraft] = useState(false);
  const [busySaved, setBusySaved] = useState<string | null>(null);
  const [draft, setDraft] = useState<DraftEndpoint>(EMPTY);
  const [presetId, setPresetId] = useState<string>("custom");
  const [verifyState, setVerifyState] = useState<Record<string, { msg: string; ok: boolean; models: string[] } | null>>({});
  // ── Inline edit state ──────────────────────────────────────
  // editingId is the endpoint id currently in edit mode (null = view-only).
  // editDraft mirrors that endpoint's mutable fields. api_key in editDraft
  // is intentionally a *new* value to write — we never receive the stored
  // one from the backend (it's masked), so empty means "keep existing key".
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editDraft, setEditDraft] = useState<DraftEndpoint>(EMPTY);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const [p, e] = await Promise.all([listAIEndpointPresets(), listAIEndpoints()]);
      setPresets(p.presets);
      setItems(e.endpoints);
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to load endpoints", "error");
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => { void refresh(); }, [refresh]);

  const preset = useMemo(
    () => presets.find((p) => p.id === presetId) ?? null,
    [presets, presetId],
  );

  const onPresetChange = (id: string) => {
    setPresetId(id);
    const p = presets.find((x) => x.id === id);
    if (p && p.id !== "custom") {
      setDraft((d) => ({
        ...d,
        name: d.name || p.label,
        endpoint_kind: p.endpoint_kind,
        base_url: p.base_url || d.base_url,
      }));
    }
  };

  const onSave = async () => {
    if (!draft.name.trim() || !draft.base_url.trim()) {
      toast("Name and Base URL are required", "warning");
      return;
    }
    setBusyDraft(true);
    try {
      await createAIEndpoint({
        name: draft.name.trim(),
        endpoint_kind: draft.endpoint_kind,
        base_url: draft.base_url.trim(),
        api_key: draft.api_key,
        default_model: draft.default_model.trim(),
        notes: draft.notes.trim(),
        enabled: true,
      });
      toast("Endpoint saved", "success");
      setDraft(EMPTY);
      setPresetId("custom");
      await refresh();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Save failed", "error");
    } finally { setBusyDraft(false); }
  };

  const onTestDraft = async () => {
    if (!draft.base_url.trim()) {
      toast("Enter a Base URL first", "warning");
      return;
    }
    setBusyDraft(true);
    try {
      const r = await verifyAIEndpointConfig({
        base_url: draft.base_url.trim(),
        api_key: draft.api_key,
        endpoint_kind: draft.endpoint_kind,
      });
      setVerifyState((s) => ({ ...s, "_draft": { msg: r.message, ok: r.valid, models: r.models } }));
    } catch (err) {
      setVerifyState((s) => ({ ...s, "_draft": { msg: err instanceof Error ? err.message : "request failed", ok: false, models: [] } }));
    } finally { setBusyDraft(false); }
  };

  const onTestSaved = async (e: AIEndpoint) => {
    setBusySaved(e.id);
    try {
      const r = await verifyAIEndpoint(e.id);
      setVerifyState((s) => ({ ...s, [e.id]: { msg: r.message, ok: r.valid, models: r.models } }));
    } catch (err) {
      setVerifyState((s) => ({ ...s, [e.id]: { msg: err instanceof Error ? err.message : "request failed", ok: false, models: [] } }));
    } finally { setBusySaved(null); }
  };

  const onToggleEnabled = async (e: AIEndpoint) => {
    try {
      await updateAIEndpoint(e.id, { enabled: !e.enabled });
      await refresh();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Update failed", "error");
    }
  };

  const onDelete = async (e: AIEndpoint) => {
    if (!window.confirm(`Delete endpoint "${e.name}"?`)) return;
    try {
      await deleteAIEndpoint(e.id);
      toast("Endpoint deleted", "info");
      await refresh();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Delete failed", "error");
    }
  };

  // ── Edit mode handlers ──────────────────────────────────────

  const onStartEdit = (e: AIEndpoint) => {
    setEditingId(e.id);
    setEditDraft({
      name: e.name,
      endpoint_kind: e.endpoint_kind,
      base_url: e.base_url,
      api_key: "",                  // blank = keep existing stored key
      default_model: e.default_model,
      notes: e.notes,
    });
  };

  const onCancelEdit = () => {
    setEditingId(null);
    setEditDraft(EMPTY);
  };

  const onSaveEdit = async (id: string) => {
    if (!editDraft.name.trim() || !editDraft.base_url.trim()) {
      toast("Name and Base URL are required", "warning");
      return;
    }
    setBusySaved(id);
    try {
      const body: Record<string, string> = {
        name: editDraft.name.trim(),
        endpoint_kind: editDraft.endpoint_kind,
        base_url: editDraft.base_url.trim(),
        default_model: editDraft.default_model.trim(),
        notes: editDraft.notes.trim(),
      };
      if (editDraft.api_key) body.api_key = editDraft.api_key;
      await updateAIEndpoint(id, body);
      toast("Endpoint updated", "success");
      onCancelEdit();
      await refresh();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Update failed", "error");
    } finally { setBusySaved(null); }
  };

  return (
    <section style={section}>
      <h3 style={titleStyle}>🔌 Custom AI Endpoints</h3>
      <p style={hint}>
        Bring your own OpenAI-compatible model backend — vLLM, LM Studio, llama.cpp,
        OpenRouter, Together, Groq, Fireworks, Azure OpenAI, etc. These are independent
        of the cloud API keys above and the local Ollama install. Saved endpoints can
        be selected as the backend of an AI Profile.
      </p>

      {/* Add new */}
      <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 7,
        border: "1px solid #c7d2fe", background: "#eef2ff" }}>
        <div style={{ ...subhead, color: "#3730a3" }}>Add new endpoint</div>
        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: 8 }}>
            <select value={presetId} onChange={(e) => onPresetChange(e.target.value)}
              style={input}>
              {presets.map((p) => (
                <option key={p.id} value={p.id}>{p.label}</option>
              ))}
            </select>
            <input value={draft.name}
              onChange={(e) => setDraft({ ...draft, name: e.target.value })}
              placeholder="Display name (e.g. 'Local vLLM' or 'OpenRouter — claude-3.5-sonnet')"
              style={input} />
          </div>
          {preset && preset.id !== "custom" && (
            <p style={{ ...hint, fontSize: 11, color: "#4338ca", margin: 0 }}>
              {preset.description}{preset.needs_key ? " · Requires an API key." : " · Local — no API key needed by default."}
            </p>
          )}
          <input value={draft.base_url}
            onChange={(e) => setDraft({ ...draft, base_url: e.target.value })}
            placeholder="Base URL (e.g. http://localhost:8000/v1 or https://openrouter.ai/api/v1)"
            style={input} />
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            <input value={draft.api_key}
              onChange={(e) => setDraft({ ...draft, api_key: e.target.value })}
              placeholder="API key (leave blank for keyless local endpoints)"
              type="password" autoComplete="off" style={input} />
            <input value={draft.default_model}
              onChange={(e) => setDraft({ ...draft, default_model: e.target.value })}
              placeholder="Default model id (optional)"
              style={input} />
          </div>
          <input value={draft.notes}
            onChange={(e) => setDraft({ ...draft, notes: e.target.value })}
            placeholder="Notes (optional)"
            style={input} />
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
            <button onClick={() => void onSave()} disabled={busyDraft} style={btnPrimary}>
              {busyDraft ? "Saving…" : "Save endpoint"}
            </button>
            <button onClick={() => void onTestDraft()} disabled={busyDraft} style={btnGhostStrong}>
              {busyDraft ? "Testing…" : "Test connection"}
            </button>
            {verifyState["_draft"] && (
              <span style={{ ...verdictStyle(verifyState["_draft"].ok), marginLeft: "auto" }}>
                {verifyState["_draft"].ok ? "✓" : "✗"} {verifyState["_draft"].msg}
              </span>
            )}
          </div>
          {verifyState["_draft"]?.models?.length ? (
            <div style={{ fontSize: 11, color: "#374151", marginTop: 4 }}>
              <strong>Models:</strong> {verifyState["_draft"].models.slice(0, 12).join(", ")}
              {verifyState["_draft"].models.length > 12 ? `, … (+${verifyState["_draft"].models.length - 12})` : ""}
            </div>
          ) : null}
        </div>
      </div>

      {/* Existing endpoints */}
      <div style={{ marginTop: 14 }}>
        <div style={subhead}>Saved endpoints ({items.length})</div>
        {loading ? (
          <div style={{ fontSize: 12, color: "#6b7280" }}>Loading…</div>
        ) : items.length === 0 ? (
          <div style={{ fontSize: 12, color: "#9ca3af", fontStyle: "italic" }}>
            No custom endpoints yet.
          </div>
        ) : (
          <div style={{ display: "grid", gap: 6 }}>
            {items.map((e) => {
              const isEditing = editingId === e.id;
              return (
                <div key={e.id} style={{
                  border: `1px solid ${isEditing ? "#a5b4fc" : "#e5e7eb"}`,
                  borderRadius: 6, padding: "10px 12px",
                  background: isEditing ? "#eef2ff" : (e.enabled ? "#fff" : "#fafafa"),
                }}>
                  {/* Header row — same in view + edit modes so the row layout is stable */}
                  <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
                    <span style={{ fontSize: 13, fontWeight: 700, color: "#111827" }}>{e.name}</span>
                    <span style={chip("#6b7280")}>{e.endpoint_kind}</span>
                    {e.api_key_set ? <span style={chip("#0d9488")}>key set</span> : <span style={chip("#9ca3af")}>no key</span>}
                    {e.default_model ? <span style={chip("#7c3aed")}>{e.default_model}</span> : null}
                    {isEditing ? (
                      <div style={{ marginLeft: "auto", display: "flex", gap: 6 }}>
                        <button onClick={() => void onSaveEdit(e.id)} disabled={busySaved === e.id}
                          style={btnPrimary}>
                          {busySaved === e.id ? "Saving…" : "Save"}
                        </button>
                        <button onClick={onCancelEdit} style={btnGhost}>
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <>
                        <label style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 4, fontSize: 11, color: "#6b7280" }}>
                          <input type="checkbox" checked={e.enabled}
                            onChange={() => void onToggleEnabled(e)} />
                          enabled
                        </label>
                        <button onClick={() => void onTestSaved(e)} disabled={busySaved === e.id} style={btnGhost}>
                          {busySaved === e.id ? "Testing…" : "Test"}
                        </button>
                        <button onClick={() => onStartEdit(e)} style={btnGhost}>
                          Edit
                        </button>
                        <button onClick={() => void onDelete(e)} style={{ ...btnGhost, color: "#dc2626", borderColor: "#fca5a5" }}>
                          Delete
                        </button>
                      </>
                    )}
                  </div>

                  {/* View mode — base_url + notes + last verify result */}
                  {!isEditing && (
                    <>
                      <div style={{ fontSize: 11, color: "#6b7280", marginTop: 4, fontFamily: "monospace" }}>
                        {e.base_url}
                      </div>
                      {e.notes && (
                        <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>{e.notes}</div>
                      )}
                      {verifyState[e.id] && (
                        <div style={{ ...verdictStyle(verifyState[e.id]!.ok), marginTop: 6 }}>
                          {verifyState[e.id]!.ok ? "✓" : "✗"} {verifyState[e.id]!.msg}
                          {verifyState[e.id]!.models.length > 0 && (
                            <span style={{ marginLeft: 8, fontSize: 10, color: "#374151" }}>
                              ({verifyState[e.id]!.models.length} models)
                            </span>
                          )}
                        </div>
                      )}
                    </>
                  )}

                  {/* Edit mode — mirrors the "Add new endpoint" form */}
                  {isEditing && (
                    <div style={{ display: "grid", gap: 8, marginTop: 10 }}>
                      <input value={editDraft.name}
                        onChange={(ev) => setEditDraft({ ...editDraft, name: ev.target.value })}
                        placeholder="Display name"
                        style={input} />
                      <input value={editDraft.base_url}
                        onChange={(ev) => setEditDraft({ ...editDraft, base_url: ev.target.value })}
                        placeholder="Base URL"
                        style={input} />
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                        <input value={editDraft.api_key}
                          onChange={(ev) => setEditDraft({ ...editDraft, api_key: ev.target.value })}
                          placeholder={e.api_key_set
                            ? "●●●●●●●●  (paste new key to replace, blank = keep existing)"
                            : "API key (leave blank for keyless local endpoints)"}
                          type="password" autoComplete="off" style={input} />
                        <input value={editDraft.default_model}
                          onChange={(ev) => setEditDraft({ ...editDraft, default_model: ev.target.value })}
                          placeholder="Default model id"
                          style={input} />
                      </div>
                      <input value={editDraft.notes}
                        onChange={(ev) => setEditDraft({ ...editDraft, notes: ev.target.value })}
                        placeholder="Notes"
                        style={input} />
                      {e.api_key_set && (
                        <p style={{ ...hint, fontSize: 11, margin: 0 }}>
                          ⚠️ Leave the API key field blank to keep the currently stored key.
                          Type a new value to replace it.
                        </p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}

function chip(color: string): React.CSSProperties {
  return {
    fontSize: 9, padding: "1px 6px", borderRadius: 8,
    background: color + "20", color, fontWeight: 700,
    textTransform: "uppercase", letterSpacing: 0.4,
  };
}

function verdictStyle(ok: boolean): React.CSSProperties {
  return {
    fontSize: 11, padding: "3px 8px", borderRadius: 5,
    background: ok ? "#f0fdf4" : "#fef2f2",
    border: `1px solid ${ok ? "#86efac" : "#fca5a5"}`,
    color: ok ? "#15803d" : "#b91c1c",
    display: "inline-flex", alignItems: "center", gap: 4,
  };
}

const section: React.CSSProperties = {
  marginBottom: "2rem", padding: "1.25rem",
  border: "1px solid #e5e7eb", borderRadius: 8,
};
const titleStyle: React.CSSProperties = {
  margin: "0 0 0.5rem 0", fontSize: 15, fontWeight: 600, color: "#111827",
};
const hint: React.CSSProperties = {
  margin: 0, fontSize: 12, color: "#6b7280", lineHeight: 1.5,
};
const subhead: React.CSSProperties = {
  fontSize: 11, fontWeight: 700, color: "#7c3aed",
  textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6,
};
const input: React.CSSProperties = {
  padding: "6px 10px", border: "1px solid #d1d5db", borderRadius: 5,
  fontSize: 13, width: "100%", boxSizing: "border-box", outline: "none",
};
const btnPrimary: React.CSSProperties = {
  padding: "6px 14px", border: "none", borderRadius: 5,
  background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const btnGhostStrong: React.CSSProperties = {
  padding: "6px 12px", border: "1px solid #c7d2fe", borderRadius: 5,
  background: "#fff", color: "#4338ca", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const btnGhost: React.CSSProperties = {
  padding: "4px 9px", border: "1px solid #d1d5db", borderRadius: 4,
  background: "#fff", color: "#374151", fontSize: 11, cursor: "pointer",
};
