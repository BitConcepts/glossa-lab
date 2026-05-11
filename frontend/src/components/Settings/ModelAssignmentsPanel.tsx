import { useEffect, useState } from "react";
import {
  listProviders, listModelAssignments, setModelAssignment, autoConfigureAssignments,
  listModelScores, syncModelIntelligence, testHuggingFace,
  type ProviderEntry, type BucketGroup, type Bucket, type ModelScore,
  type AutoConfigProfile,
} from "../../api";
import { useToast } from "../../hooks/useToast";

const PROVIDER_BADGES: Record<string, { icon: string; label: string; bg: string; color: string }> = {
  ollama:       { icon: "🦙", label: "Ollama",       bg: "#fef3c7", color: "#92400e" },
  cloud:        { icon: "☁️",  label: "Cloud",        bg: "#dbeafe", color: "#1e40af" },
  byoe:         { icon: "⚡",  label: "vLLM/Custom",  bg: "#f3e8ff", color: "#6b21a8" },
  huggingface:  { icon: "🤗", label: "HuggingFace",  bg: "#fce7f3", color: "#9d174d" },
};

const BUCKET_META: Record<string, { label: string; icon: string; desc: string }> = {
  reasoning:      { label: "Reasoning",      icon: "🧠", desc: "Decipher, hypotheses, experiment planning, discovery classification" },
  conversational: { label: "Conversational", icon: "💬", desc: "Chat, synthesis, general Q&A" },
  longform:       { label: "Long-form",      icon: "📝", desc: "Paper drafting, report generation" },
  global:         { label: "Global Default",  icon: "🌐", desc: "Used when no bucket-specific assignment exists" },
};

export function ModelAssignmentsPanel() {
  const { toast } = useToast();
  const [providers, setProviders] = useState<ProviderEntry[]>([]);
  const [assignments, setAssignments] = useState<BucketGroup[]>([]);
  const [scores, setScores] = useState<ModelScore[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<Record<string, boolean>>({});
  const [syncing, setSyncing] = useState(false);
  const [testingHF, setTestingHF] = useState(false);
  const [configuring, setConfiguring] = useState(false);
  const [scoredOnly, setScoredOnly] = useState(false);
  const [profile, setProfile] = useState<AutoConfigProfile>("mixed");

  const allModels: { providerId: string; providerName: string; model: string; providerType: string }[] = [];
  for (const p of providers) {
    for (const m of (p.available_models || [])) {
      allModels.push({ providerId: p.id, providerName: p.name, model: m, providerType: p.provider_type });
    }
  }

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

  const handleChange = async (bucket: Bucket, rank: "primary" | "fallback", value: string) => {
    setSaving(s => ({ ...s, [`${bucket}_${rank}`]: true }));
    const [providerId, ...modelParts] = value.split("|");
    const model = modelParts.join("|");
    // CRITICAL: include BOTH ranks in the request so the backend doesn't
    // clear the other rank.  Read the current assignment for the OTHER rank
    // and echo it back unchanged.
    const otherRank = rank === "primary" ? "fallback" : "primary";
    const otherCurrent = getAssignment(bucket, otherRank);
    const body: Record<string, string> = {
      [`${rank}_provider_id`]: providerId || "",
      [`${rank}_model`]: model || "",
      [`${otherRank}_provider_id`]: otherCurrent?.provider_registry_id || "",
      [`${otherRank}_model`]: otherCurrent?.model || "",
    };
    try {
      await setModelAssignment(bucket, body as never);
      await refresh();
      toast(`${bucket} ${rank} updated`, "success");
    } catch (e: unknown) {
      toast(e instanceof Error ? e.message : "Save failed", "error");
    }
    setSaving(s => ({ ...s, [`${bucket}_${rank}`]: false }));
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
    const current = getAssignment(bucket, rank);
    const currentVal = current ? `${current.provider_registry_id}|${current.model}` : "";
    const isSaving = saving[`${bucket}_${rank}`];

    return (
      <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
        <span style={{ fontSize: 10, fontWeight: 600, color: rank === "primary" ? "#2563eb" : "#9ca3af", width: 55, flexShrink: 0 }}>
          {rank === "primary" ? "⚡ Primary" : "⚠️ Fallback"}
        </span>
        <select
          value={currentVal}
          onChange={e => handleChange(bucket, rank, e.target.value)}
          disabled={isSaving}
          style={{ flex: 1, minWidth: 0, fontSize: 12, padding: "4px 6px", borderRadius: 4, border: "1px solid #d1d5db", background: isSaving ? "#f3f4f6" : "#fff", textOverflow: "ellipsis" }}
        >
          <option value="">— not set —</option>
          {allModels
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
          <select value={profile} onChange={e => setProfile(e.target.value as AutoConfigProfile)}
            style={{ fontSize: 11, padding: "3px 4px", borderRadius: 4, border: "1px solid #d1d5db", background: "#fff" }}>
            <option value="mixed">🔀 Mixed</option>
            <option value="cloud">☁️ Cloud</option>
            <option value="local">🖥️ Local</option>
          </select>
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
          return (
            <div key={bucket} style={{ border: "1px solid #e5e7eb", borderRadius: 6, padding: 12, background: "#fafafa", minWidth: 0, overflow: "hidden" }}>
              <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 8 }}>
                <span style={{ fontSize: 16 }}>{meta.icon}</span>
                <div>
                  <div style={{ fontWeight: 700, fontSize: 13 }}>{meta.label}</div>
                  <div style={{ fontSize: 10, color: "#6b7280" }}>{meta.desc}</div>
                </div>
              </div>
              {renderSelector(bucket, "primary")}
              {renderSelector(bucket, "fallback")}
            </div>
          );
        })}
      </div>

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
