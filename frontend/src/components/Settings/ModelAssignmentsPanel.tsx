import { useEffect, useState } from "react";
import {
  listProviders, listModelAssignments, setModelAssignment, autoConfigureAssignments,
  listModelScores, syncModelIntelligence, testHuggingFace,
  type ProviderEntry, type BucketGroup, type Bucket, type ModelScore,
  type ModelAssignment, type AutoConfigProfile,
} from "../../api";
import { useToast } from "../../hooks/useToast";

const PROVIDER_BADGES: Record<string, { icon: string; label: string; bg: string; color: string }> = {
  ollama:       { icon: "🦙", label: "Ollama",       bg: "#fef3c7", color: "#92400e" },
  cloud:        { icon: "☁️",  label: "Cloud",        bg: "#dbeafe", color: "#1e40af" },
  byoe:         { icon: "⚡",  label: "vLLM/Custom",  bg: "#f3e8ff", color: "#6b21a8" },
  huggingface:  { icon: "🤗", label: "HuggingFace",  bg: "#fce7f3", color: "#9d174d" },
};

/** Detect effective provider type, using URL heuristic to catch Ollama
 *  instances that were registered under the wrong type. */
function effectiveType(providerType: string, baseUrl: string): string {
  if (providerType === "ollama") return "ollama";
  if (providerType === "huggingface") return "huggingface";
  // Heuristic: if the URL looks like a local Ollama instance, use ollama badge
  if (
    baseUrl?.includes(":11434") ||
    baseUrl?.toLowerCase().includes("ollama")
  ) return "ollama";
  if (providerType === "byoe") return "byoe";
  return providerType; // cloud, etc.
}

const BUCKET_META: Record<string, { label: string; icon: string; desc: string }> = {
  reasoning:      { label: "Reasoning",      icon: "🧠", desc: "Decipher, hypotheses, experiment planning, discovery classification" },
  conversational: { label: "Conversational", icon: "💬", desc: "Chat, synthesis, general Q&A" },
  longform:       { label: "Long-form",      icon: "📝", desc: "Paper drafting, report generation" },
  global:         { label: "Global Default",  icon: "🌐", desc: "Used when no bucket-specific assignment exists" },
};

/** Build the canonical saved value string for a ModelAssignment. */
function assignmentToVal(a: ModelAssignment | undefined): string {
  return a ? `${a.provider_registry_id}|${a.model}` : "";
}

export function ModelAssignmentsPanel() {
  const { toast } = useToast();
  const [providers, setProviders] = useState<ProviderEntry[]>([]);
  const [assignments, setAssignments] = useState<BucketGroup[]>([]);
  const [scores, setScores] = useState<ModelScore[]>([]);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [testingHF, setTestingHF] = useState(false);
  const [configuring, setConfiguring] = useState(false);
  const [scoredOnly, setScoredOnly] = useState(false);
  const [profile, setProfile] = useState<AutoConfigProfile>(
    () => (localStorage.getItem("glossa_assignment_filter") as AutoConfigProfile) || "mixed"
  );

  const handleProfileChange = (p: AutoConfigProfile) => {
    setProfile(p);
    localStorage.setItem("glossa_assignment_filter", p);
  };

  // Draft state: keyed "bucket_rank" -> "providerId|model"
  // Initialised (and reset) from server assignments on every refresh.
  const [draftVals, setDraftVals] = useState<Record<string, string>>({});

  const allModels: { providerId: string; providerName: string; model: string; providerType: string; baseUrl: string }[] = [];
  for (const p of providers) {
    for (const m of (p.available_models || [])) {
      allModels.push({
        providerId: p.id, providerName: p.name, model: m,
        providerType: effectiveType(p.provider_type, p.base_url),
        baseUrl: p.base_url,
      });
    }
  }

  /** Filter models shown in selectors based on the active profile. */
  const filteredModels = allModels.filter(m => {
    if (profile === "cloud") return m.providerType === "cloud";
    if (profile === "local") return m.providerType === "ollama" || m.providerType === "byoe";
    return true; // mixed: show all
  });

  /** Recompute draft from a fresh assignments list (revert or initial load). */
  const buildDraftFromAssignments = (a: BucketGroup[]) => {
    const d: Record<string, string> = {};
    for (const bg of a) {
      d[`${bg.bucket}_primary`]  = assignmentToVal(bg.primary);
      d[`${bg.bucket}_fallback`] = assignmentToVal(bg.fallback);
    }
    return d;
  };

  const refresh = async () => {
    setLoading(true);
    try {
      const [prov, assign, sc] = await Promise.all([
        listProviders(true),
        listModelAssignments(),
        listModelScores(),
      ]);
      setProviders(prov.providers);
      setAssignments(assign.assignments);
      setScores(sc.scores);
      // Sync draft to latest saved state
      setDraftVals(buildDraftFromAssignments(assign.assignments));
    } catch { /* */ }
    setLoading(false);
  };

  useEffect(() => { refresh(); }, []);

  const getAssignment = (bucket: string, rank: "primary" | "fallback") => {
    const bg = assignments.find(a => a.bucket === bucket);
    return rank === "primary" ? bg?.primary : bg?.fallback;
  };

  const getScoreForModel = (modelName: string): ModelScore | undefined =>
    scores.find(s => s.model_name === modelName || modelName.includes(s.model_name) || s.model_name.includes(modelName));

  /** Check if any draft value differs from the last saved assignment. */
  const isDirty = (() => {
    for (const bg of assignments) {
      const pk = `${bg.bucket}_primary`;
      const fk = `${bg.bucket}_fallback`;
      if (draftVals[pk] !== assignmentToVal(bg.primary)) return true;
      if (draftVals[fk] !== assignmentToVal(bg.fallback)) return true;
    }
    // also check if draftVals has entries for buckets not yet saved
    for (const key of Object.keys(draftVals)) {
      if (draftVals[key]) {
        const [bucket, rank] = key.split("_");
        const bg = assignments.find(a => a.bucket === bucket);
        const saved = rank === "primary" ? assignmentToVal(bg?.primary) : assignmentToVal(bg?.fallback);
        if (draftVals[key] !== saved) return true;
      }
    }
    return false;
  })();

  /** Update draft on select change — NO backend call. */
  const handleChange = (bucket: Bucket, rank: "primary" | "fallback", value: string) => {
    setDraftVals(d => ({ ...d, [`${bucket}_${rank}`]: value }));
  };

  /** Apply all draft changes to the backend. */
  const handleApply = async () => {
    setApplying(true);
    const buckets: Bucket[] = ["reasoning", "conversational", "longform", "global"];
    let anyError = false;
    for (const bucket of buckets) {
      const pVal = draftVals[`${bucket}_primary`] ?? "";
      const fVal = draftVals[`${bucket}_fallback`] ?? "";
      const [pProv, ...pM] = pVal.split("|"); const pMod = pM.join("|");
      const [fProv, ...fM] = fVal.split("|"); const fMod = fM.join("|");
      const bg = assignments.find(a => a.bucket === bucket);
      const savedP = assignmentToVal(bg?.primary);
      const savedF = assignmentToVal(bg?.fallback);
      if (pVal === savedP && fVal === savedF) continue; // no change for this bucket
      try {
        await setModelAssignment(bucket, {
          primary_provider_id: pProv || "",
          primary_model: pMod || "",
          fallback_provider_id: fProv || "",
          fallback_model: fMod || "",
        } as never);
      } catch (e: unknown) {
        toast(`${bucket}: ${e instanceof Error ? e.message : "Save failed"}`, "error");
        anyError = true;
      }
    }
    await refresh(); // refresh syncs draft from server
    if (!anyError) toast("Model assignments saved", "success");
    setApplying(false);
  };

  /** Discard draft changes — reset to last saved state. */
  const handleRevert = () => {
    setDraftVals(buildDraftFromAssignments(assignments));
    toast("Changes reverted", "info");
  };

  const handleAutoConfig = async () => {
    setConfiguring(true);
    try {
      const r = await autoConfigureAssignments(profile);
      if (r.configured) {
        toast(`Auto-configured (${profile}) model assignments`, "success");
        await refresh();
      } else {
        toast(r.message || "No models available", "error");
      }
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Auto-configure failed", "error");
    }
    setConfiguring(false);
  };

  /** Swap primary and fallback in draft (no API call). */
  const handleSwap = (bucket: Bucket) => {
    const pKey = `${bucket}_primary`;
    const fKey = `${bucket}_fallback`;
    const pVal = draftVals[pKey] ?? "";
    const fVal = draftVals[fKey] ?? "";
    if (!pVal && !fVal) return;
    setDraftVals(d => ({ ...d, [pKey]: fVal, [fKey]: pVal }));
    toast(`${bucket} primary ↔ fallback swapped (not saved yet)`, "info");
  };

  const handleSync = async () => {
    setSyncing(true);
    try {
      const r = await syncModelIntelligence();
      toast(r.message, "success");
      await refresh();
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Sync failed", "error");
    }
    setSyncing(false);
  };

  const handleTestHF = async () => {
    setTestingHF(true);
    try {
      const r = await testHuggingFace();
      toast(r.message, r.valid ? "success" : "error");
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "HF test failed", "error");
    }
    setTestingHF(false);
  };

  const s = { section: { border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 16, background: "#fff" } as const };

  const renderSelector = (bucket: Bucket, rank: "primary" | "fallback") => {
    const draftVal = draftVals[`${bucket}_${rank}`] ?? "";
    const savedVal = assignmentToVal(getAssignment(bucket, rank));
    const isChanged = draftVal !== savedVal;
    const isSaving = applying;

    return (
      <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
        <span style={{ fontSize: 10, fontWeight: 600, color: rank === "primary" ? "#2563eb" : "#9ca3af", width: 55, flexShrink: 0 }}>
          {rank === "primary" ? "⚡ Primary" : "⚠️ Fallback"}
          {isChanged && <span style={{ color: "#f59e0b", marginLeft: 2 }}>●</span>}
        </span>
        <select
          value={draftVal}
          onChange={e => handleChange(bucket, rank, e.target.value)}
          disabled={isSaving}
          style={{ flex: 1, minWidth: 0, fontSize: 12, padding: "4px 6px", borderRadius: 4, border: "1px solid #d1d5db", background: isSaving ? "#f3f4f6" : "#fff", textOverflow: "ellipsis" }}
        >
          <option value="">— not set —</option>
          {filteredModels
            .map(m => {
              const sc = getScoreForModel(m.model);
              const scoreKey = bucket === "conversational" ? "conversational_score" : bucket === "longform" ? "longform_score" : "reasoning_score";
              const scoreVal = sc ? (sc as unknown as Record<string, number>)[scoreKey] ?? 0 : 0;
              return { ...m, scoreVal, hasScore: !!sc };
            })
            .filter(m => !scoredOnly || m.hasScore)
            .sort((a, b) => b.scoreVal - a.scoreVal)
            .map(m => (
            <option key={`${m.providerId}|${m.model}`} value={`${m.providerId}|${m.model}`}>
                {PROVIDER_BADGES[m.providerType]?.icon ?? "🔌"} {m.scoreVal > 0 ? `★${m.scoreVal.toFixed(0)} ` : m.hasScore ? "☆0 " : ""}{m.providerName} · {m.model}
              </option>
            ))}
        </select>
      </div>
    );
  };

  return (
    <section style={s.section}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>🎯 Model Assignments</h3>
        <div style={{ display: "flex", gap: 6 }}>
          <button onClick={handleTestHF} disabled={testingHF} style={{ padding: "4px 10px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer", background: "#fff" }}>
            {testingHF ? "Testing..." : "🤗 Test HF"}
          </button>
          <button onClick={handleSync} disabled={syncing} style={{ padding: "4px 10px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer", background: "#fff" }}>
            {syncing ? "Syncing..." : "🔄 Sync Scores"}
          </button>
          <div style={{ display: "flex", alignItems: "center", gap: 2 }}>
            <span style={{ fontSize: 10, color: "#9ca3af", flexShrink: 0 }}>Filter:</span>
            <select value={profile} onChange={e => handleProfileChange(e.target.value as AutoConfigProfile)}
              style={{ fontSize: 11, padding: "3px 4px", borderRadius: 4, border: "1px solid #d1d5db", background: "#fff" }}>
              <option value="mixed">🔀 All</option>
              <option value="cloud">☁️ Cloud only</option>
              <option value="local">🖥️ Local only</option>
            </select>
          </div>
          <button onClick={handleAutoConfig} disabled={configuring} style={{ padding: "4px 10px", fontSize: 11, border: "none", borderRadius: 4, cursor: "pointer", background: "#7c3aed", color: "#fff", fontWeight: 600 }}>
            {configuring ? "Configuring..." : "✨ Auto-Configure"}
          </button>
        </div>
      </div>

      {loading && <div style={{ color: "#9ca3af", fontSize: 12 }}>Loading...</div>}

      {allModels.length === 0 && !loading && (
        <div style={{ textAlign: "center", padding: 16, color: "#9ca3af", fontSize: 12, background: "#f9fafb", borderRadius: 6 }}>
          No models available. Add providers above and click "Test" to fetch model lists.
        </div>
      )}

      <div style={{ display: "grid", gap: 10, gridTemplateColumns: "1fr 1fr", minWidth: 0 }}>
        {(["reasoning", "conversational", "longform", "global"] as Bucket[]).map(bucket => {
          const meta = BUCKET_META[bucket];
          const hasBoth = !!(draftVals[`${bucket}_primary`] || getAssignment(bucket, "primary"))
                       && !!(draftVals[`${bucket}_fallback`] || getAssignment(bucket, "fallback"));
          return (
            <div key={bucket} style={{ border: "1px solid #e5e7eb", borderRadius: 6, padding: 12, background: "#fafafa", minWidth: 0, overflow: "hidden" }}>
              <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 8 }}>
                <span style={{ fontSize: 16 }}>{meta.icon}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: 700, fontSize: 13 }}>{meta.label}</div>
                  <div style={{ fontSize: 10, color: "#6b7280" }}>{meta.desc}</div>
                </div>
                {hasBoth && (
                  <button
                    onClick={() => handleSwap(bucket)}
                    disabled={applying}
                    title="Swap primary ↔ fallback (draft)"
                    style={{ padding: "2px 6px", fontSize: 11, border: "1px solid #d1d5db", borderRadius: 3, cursor: "pointer", background: "#fff", color: "#6b7280", flexShrink: 0 }}>
                    ⇅
                  </button>
                )}
              </div>
              {renderSelector(bucket, "primary")}
              {renderSelector(bucket, "fallback")}
            </div>
          );
        })}
      </div>

      {/* Apply / Revert bar — only shown when there are unsaved changes */}
      {isDirty && (
        <div style={{ marginTop: 10, display: "flex", alignItems: "center", gap: 8, padding: "8px 12px", background: "#fffbeb", border: "1px solid #fcd34d", borderRadius: 6 }}>
          <span style={{ fontSize: 12, color: "#92400e", flex: 1 }}>
            ⚠️ Unsaved changes
          </span>
          <button
            onClick={handleRevert}
            disabled={applying}
            style={{ padding: "4px 12px", fontSize: 12, border: "1px solid #d1d5db", borderRadius: 4, cursor: "pointer", background: "#fff", color: "#374151" }}>
            Revert
          </button>
          <button
            onClick={handleApply}
            disabled={applying}
            style={{ padding: "4px 16px", fontSize: 12, border: "none", borderRadius: 4, cursor: applying ? "wait" : "pointer", background: "#2563eb", color: "#fff", fontWeight: 700 }}>
            {applying ? "Saving…" : "✓ Apply"}
          </button>
        </div>
      )}

      <div style={{ marginTop: 12, display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
        {scores.length > 0 && (
          <span style={{ fontSize: 10, color: "#9ca3af" }}>
            📊 {scores.length} model(s) scored · ★ = bucket fitness score (higher = better)
          </span>
        )}
        <label style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 11, color: "#6b7280", cursor: "pointer" }}>
          <input type="checkbox" checked={scoredOnly} onChange={e => setScoredOnly(e.target.checked)} />
          Scored models only
        </label>
        <div style={{ display: "flex", gap: 4, marginLeft: "auto", flexWrap: "wrap" }}>
          {Object.values(PROVIDER_BADGES).map(b => (
            <span key={b.label} style={{ fontSize: 10, padding: "2px 6px", borderRadius: 3, background: b.bg, color: b.color, fontWeight: 600 }}>
              {b.icon} {b.label}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
