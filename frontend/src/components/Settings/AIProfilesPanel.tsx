/**
 * AIProfilesPanel — reusable AI profiles spanning cloud + Ollama + custom endpoints.
 *
 * A profile bundles a named (backend, model, params) tuple so the user can pick
 * which one to use per task (chat, decipher, draft, etc.). Setting is_default
 * for a role makes that profile the default for that role.
 */

import { useCallback, useEffect, useState } from "react";
import {
  createAIProfile, deleteAIProfile, listAIEndpoints, listAIProfileRoles,
  listAIProfiles, listOllamaInstalled, suggestAIProfiles, updateAIProfile,
  type AIBackendKind, type AIEndpoint, type AIProfile, type AIProfileRole,
  type AIProfileSuggestion, type OllamaInstalledModel,
} from "../../api";
import { useToast } from "../../hooks/useToast";

const CLOUD_PROVIDERS = [
  { id: "mistral", label: "Mistral" },
  { id: "openai", label: "OpenAI" },
  { id: "anthropic", label: "Anthropic" },
  { id: "google", label: "Google" },
];

interface Draft {
  name: string;
  backend_kind: AIBackendKind;
  backend_ref: string;
  model: string;
  role: string;
  is_default: boolean;
  notes: string;
}

const EMPTY: Draft = {
  name: "", backend_kind: "cloud", backend_ref: "openai",
  model: "", role: "", is_default: false, notes: "",
};

export function AIProfilesPanel() {
  const { toast } = useToast();
  const [profiles, setProfiles] = useState<AIProfile[]>([]);
  const [roles, setRoles] = useState<AIProfileRole[]>([]);
  const [endpoints, setEndpoints] = useState<AIEndpoint[]>([]);
  const [ollama, setOllama] = useState<OllamaInstalledModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [draft, setDraft] = useState<Draft>(EMPTY);
  // ── Suggester state ──────────────────────────────────────────────
  const [suggesting,   setSuggesting]   = useState(false);
  const [creatingIdx,  setCreatingIdx]  = useState<number | null>(null);
  const [bulkCreating, setBulkCreating] = useState(false);
  const [suggestions,  setSuggestions]  = useState<AIProfileSuggestion[]>([]);
  const [suggestMsg,   setSuggestMsg]   = useState<string>("");

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const [p, r, e, o] = await Promise.all([
        listAIProfiles(),
        listAIProfileRoles(),
        listAIEndpoints(true),
        listOllamaInstalled().catch(() => ({ models: [] as OllamaInstalledModel[], running: false })),
      ]);
      setProfiles(p.profiles);
      setRoles(r.roles);
      setEndpoints(e.endpoints);
      setOllama(o.models ?? []);
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed to load profiles", "error");
    } finally { setLoading(false); }
  }, [toast]);

  useEffect(() => { void refresh(); }, [refresh]);

  const onBackendKindChange = (kind: AIBackendKind) => {
    let backend_ref = "";
    if (kind === "cloud") backend_ref = "openai";
    else if (kind === "ollama") backend_ref = ollama[0]?.name ?? "";
    else if (kind === "endpoint") backend_ref = endpoints[0]?.id ?? "";
    setDraft({ ...draft, backend_kind: kind, backend_ref, model: "" });
  };

  const onSave = async () => {
    if (!draft.name.trim()) {
      toast("Profile name is required", "warning");
      return;
    }
    setBusy(true);
    try {
      await createAIProfile({
        name: draft.name.trim(),
        backend_kind: draft.backend_kind,
        backend_ref: draft.backend_ref,
        model: draft.model.trim(),
        role: draft.role,
        is_default: draft.is_default,
        notes: draft.notes.trim(),
      });
      toast("Profile saved", "success");
      setDraft(EMPTY);
      await refresh();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Save failed", "error");
    } finally { setBusy(false); }
  };

  const onMakeDefault = async (p: AIProfile) => {
    try {
      await updateAIProfile(p.id, { is_default: true });
      toast(`Default for ${roleLabel(roles, p.role) || "global"}: ${p.name}`, "success");
      await refresh();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Update failed", "error");
    }
  };

  const onDelete = async (p: AIProfile) => {
    if (!window.confirm(`Delete profile "${p.name}"?`)) return;
    try {
      await deleteAIProfile(p.id);
      toast("Profile deleted", "info");
      await refresh();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Delete failed", "error");
    }
  };

  // ── Suggester ──────────────────────────────────────────────────────
  // Compare keys for dedup. We treat (name, backend_kind, backend_ref, model)
  // as the natural identity so the same provider+model can hold multiple
  // role-specific profiles.
  const _profileKey = (p: { name: string; backend_kind: string; backend_ref: string; model: string }) =>
    [p.name.trim().toLowerCase(),
     (p.backend_kind || "").toLowerCase(),
     (p.backend_ref  || "").toLowerCase(),
     (p.model        || "").toLowerCase()].join("|");

  const onSuggest = async () => {
    setSuggesting(true);
    try {
      const res = await suggestAIProfiles();
      const proposed = res.profiles ?? [];
      // Dedup against existing profiles before showing the user anything.
      const existing = new Set(profiles.map((p) => _profileKey(p)));
      const fresh:    AIProfileSuggestion[] = [];
      const skipped:  AIProfileSuggestion[] = [];
      for (const p of proposed) {
        if (existing.has(_profileKey(p))) skipped.push(p);
        else                              fresh.push(p);
      }
      setSuggestions(fresh);
      const baseMsg = res.message ?? "";
      const dedupMsg = skipped.length
        ? `${skipped.length} duplicate(s) skipped`
        : "";
      setSuggestMsg([baseMsg, dedupMsg].filter(Boolean).join(" · "));
      if (!fresh.length && !skipped.length) {
        toast(baseMsg || "No suggestions yet", "info");
      } else if (!fresh.length) {
        toast(`All ${skipped.length} suggestion(s) already match existing profiles`, "info");
      } else if (skipped.length) {
        toast(`${fresh.length} new · ${skipped.length} duplicate(s) skipped`, "success");
      } else {
        toast(`Got ${fresh.length} suggestion(s)`, "success");
      }
    } catch (err) {
      toast(err instanceof Error ? err.message : "Suggest failed", "error");
    } finally { setSuggesting(false); }
  };

  const onCreateSuggestion = async (s: AIProfileSuggestion, idx: number) => {
    // Refuse to create a duplicate even if the existing list races behind.
    const existing = new Set(profiles.map((p) => _profileKey(p)));
    if (existing.has(_profileKey(s))) {
      toast(`Skipped "${s.name}" — already exists`, "info");
      setSuggestions((prev) => prev.filter((_, i) => i !== idx));
      return;
    }
    setCreatingIdx(idx);
    try {
      await createAIProfile({
        name:         s.name,
        backend_kind: s.backend_kind,
        backend_ref:  s.backend_ref,
        model:        s.model,
        role:         s.role,
        params:       s.params,
        tags:         s.tags,
        notes:        s.notes,
        is_default:   false,
      });
      toast(`Created "${s.name}"`, "success");
      // Drop this suggestion from the preview list so the user sees progress.
      setSuggestions((prev) => prev.filter((_, i) => i !== idx));
      await refresh();
    } catch (err) {
      toast(err instanceof Error ? err.message : "Create failed", "error");
    } finally { setCreatingIdx(null); }
  };

  const onCreateAllSuggestions = async () => {
    if (!suggestions.length) return;
    if (!window.confirm(`Create all ${suggestions.length} suggested profile(s)?`)) return;
    setBulkCreating(true);
    // Snapshot so removals don't shift indices mid-loop.
    const items = [...suggestions];
    // Filter out anything that already matches an existing profile so the
    // bulk run never creates duplicates even if the suggester missed it.
    const existingKeys = new Set(profiles.map((p) => _profileKey(p)));
    const planned: AIProfileSuggestion[] = [];
    let preSkipped = 0;
    for (const s of items) {
      if (existingKeys.has(_profileKey(s))) preSkipped += 1;
      else                                  planned.push(s);
    }
    let ok = 0, fail = 0;
    const failures: string[] = [];
    for (const s of planned) {
      try {
        await createAIProfile({
          name:         s.name,
          backend_kind: s.backend_kind,
          backend_ref:  s.backend_ref,
          model:        s.model,
          role:         s.role,
          params:       s.params,
          tags:         s.tags,
          notes:        s.notes,
          is_default:   false,
        });
        ok += 1;
      } catch (err) {
        fail += 1;
        failures.push(`${s.name}: ${err instanceof Error ? err.message : "unknown"}`);
      }
    }
    setBulkCreating(false);
    setSuggestions([]);
    const summaryParts = [
      `${ok} created`,
      preSkipped ? `${preSkipped} duplicate(s) skipped` : "",
      fail ? `${fail} failed` : "",
    ].filter(Boolean);
    const summary = summaryParts.join(" · ");
    toast(`Bulk create: ${summary}`, fail ? "warning" : "success");
    if (failures.length) {
      // Persist a second toast so the user sees *which* ones failed in the
      // notification history; the bulk row is intentionally short.
      toast(`Failures: ${failures.slice(0, 3).join("; ")}${failures.length > 3 ? "…" : ""}`, "warning", 6000);
    }
    await refresh();
  };

  const renderBackendField = () => {
    if (draft.backend_kind === "cloud") {
      return (
        <select value={draft.backend_ref}
          onChange={(e) => setDraft({ ...draft, backend_ref: e.target.value })}
          style={input}>
          {CLOUD_PROVIDERS.map((p) => (
            <option key={p.id} value={p.id}>{p.label}</option>
          ))}
        </select>
      );
    }
    if (draft.backend_kind === "ollama") {
      return (
        <select value={draft.backend_ref}
          onChange={(e) => setDraft({ ...draft, backend_ref: e.target.value })}
          style={input}>
          <option value="">— pick an installed Ollama model —</option>
          {ollama.map((m) => (
            <option key={m.name} value={m.name}>{m.display || m.name}</option>
          ))}
        </select>
      );
    }
    return (
      <select value={draft.backend_ref}
        onChange={(e) => setDraft({ ...draft, backend_ref: e.target.value })}
        style={input}>
        <option value="">— pick a custom endpoint —</option>
        {endpoints.map((e) => (
          <option key={e.id} value={e.id}>{e.name}</option>
        ))}
      </select>
    );
  };

  return (
    <section style={section}>
      <h3 style={titleStyle}>🎛️ AI Profiles</h3>
      <p style={hint}>
        A profile is a saved (backend + model + role) bundle. Use the AI hub to
        pick a profile per task — or mark a profile as default for a specific
        role (chat, decipherment, drafting, etc.) so Glossa AI picks it
        automatically. You can mix cloud, Ollama, and custom endpoints.
      </p>

      {/* Auto-suggest profiles */}
      <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 7,
        border: "1px solid #c7d2fe", background: "#eef2ff" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <div style={{ ...subhead, color: "#4338ca", margin: 0 }}>✨ Auto-suggest profiles</div>
          <span style={{ flex: 1 }} />
          {suggestions.length > 0 && (
            <button onClick={() => void onCreateAllSuggestions()}
              disabled={bulkCreating}
              style={btnPrimary}>
              {bulkCreating ? "Creating…" : `➕ Create all ${suggestions.length}`}
            </button>
          )}
          <button onClick={() => void onSuggest()} disabled={suggesting}
            style={btnPrimary}>
            {suggesting ? "…" : "Suggest from my setup"}
          </button>
        </div>
        <p style={{ ...hint, marginTop: 6 }}>
          Inspects your configured cloud API keys, installed Ollama models, and
          saved custom endpoints, then proposes role-tuned profiles. Click
          “Create” on the ones you want — nothing is saved until you do.
        </p>
        {suggestMsg && (
          <div style={{ marginTop: 6, fontSize: 11, color: "#4338ca" }}>
            {suggestMsg}
          </div>
        )}
        {suggestions.length > 0 && (
          <div style={{ marginTop: 10, display: "grid", gap: 8 }}>
            {suggestions.map((s, i) => (
              <div key={`${s.backend_kind}-${s.backend_ref}-${s.role}-${i}`} style={{
                border: "1px solid #c7d2fe", borderRadius: 6,
                padding: "10px 12px", background: "#fff",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
                  <span style={{ fontSize: 13, fontWeight: 700, color: "#111827" }}>{s.name}</span>
                  <span style={chip(backendColor(s.backend_kind))}>{s.backend_kind}</span>
                  <span style={{ fontSize: 11, color: "#6b7280", fontFamily: "monospace" }}>
                    {s.backend_ref}{s.model ? ` · ${s.model}` : ""}
                  </span>
                  {s.role && <span style={chip("#6366f1")}>{roleLabel(roles, s.role)}</span>}
                  <div style={{ marginLeft: "auto", display: "flex", gap: 6 }}>
                    <button onClick={() => void onCreateSuggestion(s, i)}
                      disabled={creatingIdx === i || bulkCreating}
                      style={btnPrimary}>
                      {creatingIdx === i ? "Creating…" : "➕ Create"}
                    </button>
                  </div>
                </div>
                {s.rationale && (
                  <div style={{ fontSize: 11, color: "#4b5563", marginTop: 4 }}>
                    {s.rationale}
                  </div>
                )}
                {s.notes && (
                  <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2, fontStyle: "italic" }}>
                    {s.notes}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* New profile */}
      <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 7,
        border: "1px solid #fbcfe8", background: "#fdf2f8" }}>
        <div style={{ ...subhead, color: "#9d174d" }}>Add new profile</div>
        <div style={{ display: "grid", gap: 8 }}>
          <input value={draft.name}
            onChange={(e) => setDraft({ ...draft, name: e.target.value })}
            placeholder="Profile name (e.g. 'Cheap drafts — Mistral medium' or 'Local Llama 3.1 70B')"
            style={input} />
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            <select value={draft.backend_kind}
              onChange={(e) => onBackendKindChange(e.target.value as AIBackendKind)}
              style={input}>
              <option value="cloud">Cloud provider</option>
              <option value="ollama">Ollama (local)</option>
              <option value="endpoint">Custom endpoint</option>
            </select>
            {renderBackendField()}
          </div>
          <input value={draft.model}
            onChange={(e) => setDraft({ ...draft, model: e.target.value })}
            placeholder={draft.backend_kind === "ollama"
              ? "Model id (defaults to backend ref above)"
              : "Model id (e.g. gpt-4o-mini, mistral-medium-latest, llama-3.1-70b-instruct)"}
            style={input} />
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            <select value={draft.role}
              onChange={(e) => setDraft({ ...draft, role: e.target.value })}
              style={input}>
              {roles.map((r) => (
                <option key={r.id} value={r.id}>{r.label}</option>
              ))}
            </select>
            <label style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12, color: "#374151" }}>
              <input type="checkbox" checked={draft.is_default}
                onChange={(e) => setDraft({ ...draft, is_default: e.target.checked })} />
              Make default for this role
            </label>
          </div>
          <input value={draft.notes}
            onChange={(e) => setDraft({ ...draft, notes: e.target.value })}
            placeholder="Notes (optional)"
            style={input} />
          <div>
            <button onClick={() => void onSave()} disabled={busy} style={btnPrimary}>
              {busy ? "Saving…" : "Save profile"}
            </button>
          </div>
        </div>
      </div>

      {/* Existing */}
      <div style={{ marginTop: 14 }}>
        <div style={subhead}>Saved profiles ({profiles.length})</div>
        {loading ? (
          <div style={{ fontSize: 12, color: "#6b7280" }}>Loading…</div>
        ) : profiles.length === 0 ? (
          <div style={{ fontSize: 12, color: "#9ca3af", fontStyle: "italic" }}>
            No profiles yet. Create one above to use it as the default for chat,
            decipherment, drafting, etc.
          </div>
        ) : (
          <div style={{ display: "grid", gap: 6 }}>
            {profiles.map((p) => (
              <div key={p.id} style={{
                border: `1px solid ${p.is_default ? "#86efac" : "#e5e7eb"}`,
                borderRadius: 6, padding: "10px 12px",
                background: p.is_default ? "#f0fdf4" : "#fff",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
                  <span style={{ fontSize: 13, fontWeight: 700, color: "#111827" }}>{p.name}</span>
                  <span style={chip(backendColor(p.backend_kind))}>{p.backend_kind}</span>
                  <span style={{ fontSize: 11, color: "#6b7280", fontFamily: "monospace" }}>
                    {p.backend_ref}{p.model ? ` · ${p.model}` : ""}
                  </span>
                  {p.role && <span style={chip("#6366f1")}>{roleLabel(roles, p.role)}</span>}
                  {p.is_default && <span style={chip("#15803d")}>★ default</span>}
                  <div style={{ marginLeft: "auto", display: "flex", gap: 6 }}>
                    {!p.is_default && (
                      <button onClick={() => void onMakeDefault(p)} style={btnGhost}>
                        Set default
                      </button>
                    )}
                    <button onClick={() => void onDelete(p)}
                      style={{ ...btnGhost, color: "#dc2626", borderColor: "#fca5a5" }}>
                      Delete
                    </button>
                  </div>
                </div>
                {p.notes && (
                  <div style={{ fontSize: 11, color: "#6b7280", marginTop: 4 }}>{p.notes}</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

function backendColor(kind: AIBackendKind): string {
  return kind === "cloud" ? "#2563eb" : kind === "ollama" ? "#16a34a" : "#7c3aed";
}

function roleLabel(roles: AIProfileRole[], id: string): string {
  return roles.find((r) => r.id === id)?.label ?? id;
}

function chip(color: string): React.CSSProperties {
  return {
    fontSize: 9, padding: "1px 6px", borderRadius: 8,
    background: color + "20", color, fontWeight: 700,
    textTransform: "uppercase", letterSpacing: 0.4,
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
  background: "#7c3aed", color: "#fff", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const btnGhost: React.CSSProperties = {
  padding: "4px 9px", border: "1px solid #d1d5db", borderRadius: 4,
  background: "#fff", color: "#374151", fontSize: 11, cursor: "pointer",
};
