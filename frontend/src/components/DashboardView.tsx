/**
 * DashboardView — main landing page.
 *
 * Layout:
 *   ┌──────────────────────────────────────────────────────────────────┐
 *   │ Header: counts (items, studies, experiments) + ↻ refresh         │
 *   ├──────────────────────────────────────────────────────────────────┤
 *   │ ✨ AI Insight (lazy-loaded)         │ 📡 RSS feed (last 14 d)    │
 *   │  • Highlights with why-it-matters   │  • most-recent first       │
 *   │  • What it means narrative          │  • kind chip + source      │
 *   │  • Per-study impact suggestions     │                            │
 *   │  • Next actions                     │                            │
 *   ├──────────────────────────────────────────────────────────────────┤
 *   │ 🔭 Top kinds  │ 🏷 Top topics  │ 📡 Top sources                  │
 *   └──────────────────────────────────────────────────────────────────┘
 *
 * The dashboard is intentionally read-only: every action button on it
 * either opens another view or POSTs the same endpoints the rest of the
 * app already uses.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  createHypothesis,
  updateHypothesis,
  executeAiAction,
  getDashboardHighlights,
  getHealth,
  listGraphExperiments,
  regenerateDashboardInsight,
  runGraphExperimentStream,
  startDiscoveryFetch,
  startDiscoveryMine,
  type DashboardActionType,
  type DashboardHighlights,
  type DashboardInsight,
  type DashboardNextAction,
  type DiscoveryItem,
  type GraphExperimentMeta,
} from "../api";
import { useAIChat } from "../hooks/useAIChat";
import { useToast } from "../hooks/useToast";

// ── Insight persistence ──────────────────────────────────────────────────
// Insights are expensive to regenerate (LLM call). We cache the last result
// in localStorage along with the timestamp and the backend's boot time so
// we can detect a backend restart without re-asking the LLM every reload.
const INSIGHT_LS_KEY = "glossa_dashboard_insight_v1";
interface PersistedInsight {
  insight: DashboardInsight;
  generated_at: number;       // epoch ms when LLM generated this
  backend_boot_at: number;    // epoch ms (sec-quantised) when backend started
  days: number;               // window the insight was computed against
  /** Per-button completion state keyed by "impact-0", "na-1", etc.
   *  Persisted so completed actions survive page reloads. */
  completed?: Record<string, "success" | "error" | "warn">;
}
function _loadPersistedInsight(): PersistedInsight | null {
  try {
    const raw = localStorage.getItem(INSIGHT_LS_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as PersistedInsight;
  } catch { return null; }
}
function _savePersistedInsight(p: PersistedInsight): void {
  try { localStorage.setItem(INSIGHT_LS_KEY, JSON.stringify(p)); } catch { /* ignore */ }
}

// Mine batch-size preference (how many un-mined items to classify per click).
const MINE_LIMIT_LS_KEY = "glossa_dashboard_mine_limit";
const MINE_LIMIT_OPTIONS = [10, 25, 50, 100, 200, 500];
const MINE_LIMIT_DEFAULT = 50;
function _loadMineLimit(): number {
  const raw = parseInt(localStorage.getItem(MINE_LIMIT_LS_KEY) ?? "", 10);
  return MINE_LIMIT_OPTIONS.includes(raw) ? raw : MINE_LIMIT_DEFAULT;
}

const KIND_COLOURS: Record<string, { bg: string; fg: string }> = {
  hypothesis: { bg: "#ede9fe", fg: "#6d28d9" },
  finding:    { bg: "#dcfce7", fg: "#15803d" },
  study:      { bg: "#dbeafe", fg: "#1d4ed8" },
  tablet:     { bg: "#fef3c7", fg: "#b45309" },
  review:     { bg: "#fce7f3", fg: "#be185d" },
  tooling:    { bg: "#e0e7ff", fg: "#4338ca" },
  other:      { bg: "#f3f4f6", fg: "#4b5563" },
};

/** Strip HTML/XML/MathML tags from text (safety net for Crossref titles). */
function stripTags(s: string): string {
  return s.replace(/<[^>]+>/g, " ").replace(/\s{2,}/g, " ").trim();
}

function fmtRelative(iso: string): string {
  if (!iso) return "";
  const t = Date.parse(iso);
  if (Number.isNaN(t)) return iso;
  const dSec = Math.round((Date.now() - t) / 1000);
  if (dSec < 60) return "just now";
  if (dSec < 3600) return `${Math.round(dSec / 60)}m ago`;
  if (dSec < 86400) return `${Math.round(dSec / 3600)}h ago`;
  if (dSec < 86400 * 14) return `${Math.round(dSec / 86400)}d ago`;
  return new Date(t).toISOString().slice(0, 10);
}

/** Format an epoch-ms as a short human-readable timestamp for the
 *  "last generated" caption next to the Regenerate button. */
function fmtAbsoluteShort(ms: number): string {
  if (!ms) return "";
  const dt = new Date(ms);
  const today = new Date();
  const sameDay = dt.toDateString() === today.toDateString();
  if (sameDay) {
    return dt.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
  }
  return dt.toLocaleString(undefined, {
    month: "short", day: "numeric",
    hour: "numeric", minute: "2-digit",
  });
}

export function DashboardView() {
  const { toast } = useToast();
  const { openChat } = useAIChat();
  const [data, setData] = useState<DashboardHighlights | null>(null);
  const [insight, setInsight] = useState<DashboardInsight | null>(null);
  const [insightGeneratedAt, setInsightGeneratedAt] = useState<number>(0);
  const [insightLoading, setInsightLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [days, setDays] = useState(14);
  const [running, setRunning] = useState<"" | "fetch" | "mine">("");
  const [mineDropOpen, setMineDropOpen] = useState(false);
  // Mine batch size — persisted; controls how many un-mined items the LLM
  // classifies per "✨ Mine N" click. Default 50.
  const [mineLimit, setMineLimitState] = useState<number>(_loadMineLimit);
  const setMineLimit = (n: number) => {
    setMineLimitState(n);
    try { localStorage.setItem(MINE_LIMIT_LS_KEY, String(n)); } catch { /* ignore */ }
  };
  // Per-button completion state for Apply / Run buttons. Persisted in
  // localStorage alongside the insight so completed actions survive reloads.
  type ApplyResult = "success" | "error" | "warn";
  const [applyResult, setApplyResultRaw] = useState<Record<string, ApplyResult>>({});
  // Wrap setter to also persist to localStorage whenever it changes.
  const setApplyResult = useCallback((updater: Record<string, ApplyResult> | ((prev: Record<string, ApplyResult>) => Record<string, ApplyResult>)) => {
    setApplyResultRaw((prev) => {
      const next = typeof updater === "function" ? updater(prev) : updater;
      // Persist alongside the existing insight cache.
      try {
        const raw = localStorage.getItem(INSIGHT_LS_KEY);
        if (raw) {
          const p = JSON.parse(raw) as PersistedInsight;
          p.completed = next;
          localStorage.setItem(INSIGHT_LS_KEY, JSON.stringify(p));
        }
      } catch { /* ignore */ }
      return next;
    });
  }, []);

  const refresh = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const d = await getDashboardHighlights({ days, limit: 30 });
      setData(d);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load dashboard");
    } finally {
      setLoading(false);
    }
  }, [days]);

  const generateInsight = useCallback(async () => {
    setInsightLoading(true);
    try {
      const ins = await regenerateDashboardInsight({ days, limit: 30 });
      const generatedAt = Date.now();
      setInsight(ins);
      setInsightGeneratedAt(generatedAt);
      // Persist along with backend boot time so we can detect restarts on
      // future mounts and skip auto-regen otherwise.
      try {
        const h = await getHealth();
        const bootAt = Math.round((Date.now() - h.uptime_seconds * 1000) / 1000) * 1000;
        _savePersistedInsight({ insight: ins, generated_at: generatedAt, backend_boot_at: bootAt, days });
      } catch {
        _savePersistedInsight({ insight: ins, generated_at: generatedAt, backend_boot_at: 0, days });
      }
      // Clear stale per-button completion marks now that the insight body
      // has changed — the keyed indices may no longer line up.
      setApplyResult({});
    } catch (e) {
      toast(e instanceof Error ? e.message : "Insight failed", "error");
    } finally {
      setInsightLoading(false);
    }
  }, [days, toast, setApplyResult]);

  useEffect(() => { void refresh(); }, [refresh]);

  // Auto-generate insight policy.
  // The AI insight is expensive (LLM call) and the user explicitly does not
  // want it to regenerate just because the page was reloaded, the backend
  // restarted, or the `days` window changed. Regen happens ONLY when:
  //   • there is no persisted insight at all (first ever generation), OR
  //   • the user clicks ↻ Regenerate (handled in generateInsight()), OR
  //   • a Fetch Now run completes (chained inside onRunFetch).
  // On every other mount we just surface the persisted insight and the
  // "Last regenerated" caption tells the user how stale it is.
  const insightBootstrapDone = useRef(false);
  useEffect(() => {
    if (insightBootstrapDone.current) return;
    if (!data) return;  // wait for highlights so we know n_items
    insightBootstrapDone.current = true;
    const persisted = _loadPersistedInsight();
    if (persisted) {
      setInsight(persisted.insight);
      setInsightGeneratedAt(persisted.generated_at);
      // Restore completed-action marks so they survive reloads.
      if (persisted.completed && Object.keys(persisted.completed).length > 0) {
        setApplyResult(persisted.completed);
      }
      return;
    }
    // No cached insight yet — do a one-time generation so the panel isn't
    // empty on first run. After this it stays sticky until the user acts.
    if (data.n_items > 0) {
      void generateInsight();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);

  const onRunFetch = async () => {
    setRunning("fetch");
    try {
      await startDiscoveryFetch({});
      toast(`Fetch started · will regenerate insight when complete`, "info");
    } catch (e) {
      toast(e instanceof Error ? e.message : "Fetch failed", "error");
      setRunning("");
      return;
    }
    // Per the spec: Fetch Now → always followed by an Insight regen so the
    // Dashboard reflects the new items. We give the backend a moment to
    // ingest+mine the items before asking the LLM to summarise.
    setTimeout(() => {
      void refresh();
      void generateInsight();
      setRunning("");
    }, 1500);
  };

  const onRunMine = async () => {
    setRunning("mine");
    try {
      await startDiscoveryMine({ limit: mineLimit });
      toast(
        `Mine started · classifying up to ${mineLimit} items`,
        "info",
      );
    } catch (e) {
      toast(e instanceof Error ? e.message : "Mine failed", "error");
    } finally {
      setRunning("");
      void refresh();
    }
  };

  const askAIAbout = (it: DiscoveryItem) => {
    openChat({
      contextType: "", contextId: "",
      initialPrompt: `Help me decide if this discovery item should change my research plan.\n\n` +
                     `Title: ${it.title}\nSource: ${it.source}\nURL: ${it.url}\nTopic: ${it.topic}\n` +
                     (it.summary ? `Summary: ${it.summary}\n` : "") +
                     `\nGiven my current studies and experiments, what (if anything) should I do?`,
    });
  };

  const navigate = (view: string) =>
    window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view } }));

  // ── Cached experiment registry for pre-validation ────────────────
  // The LLM occasionally hallucinates experiment IDs (e.g.
  // ``indus_contact_zone_k`` instead of a real ``indus_contact_zone_v2``).
  // We list the registry once on mount and re-fetch on demand so the
  // dashboard can reject phantom IDs with a friendly message AND offer the
  // closest real match.
  const expRegistryRef = useRef<GraphExperimentMeta[] | null>(null);
  const ensureExpRegistry = useCallback(async (force = false): Promise<GraphExperimentMeta[]> => {
    if (expRegistryRef.current && !force) return expRegistryRef.current;
    try {
      const list = await listGraphExperiments();
      expRegistryRef.current = list;
      return list;
    } catch {
      return expRegistryRef.current ?? [];
    }
  }, []);
  useEffect(() => { void ensureExpRegistry(); }, [ensureExpRegistry]);

  /** Fuzzy similarity score for experiment ID matching.
   *  Returns 0–1000; higher = better match. Handles:
   *  - Exact match (1000)
   *  - One is a prefix of the other (500+)
   *  - Substring containment (100+)
   *  - Long common prefix relative to string length (percentage-based) */
  const _scoreMatch = (target: string, candidate: string): number => {
    const a = target.toLowerCase();
    const b = candidate.toLowerCase();
    if (a === b) return 1000;
    if (b.startsWith(a) || a.startsWith(b)) return 500 + Math.min(a.length, b.length);
    // Count common prefix characters
    let common = 0;
    const maxLen = Math.min(a.length, b.length);
    while (common < maxLen && a[common] === b[common]) common += 1;
    if (b.includes(a) || a.includes(b)) return 100 + common;
    // Percentage-based score: if 80%+ of the shorter string matches as a
    // prefix, treat it as a strong match. This catches cases like
    // "indus_contact_zone_k" vs "indus_contact_zone_v2" (19/21 = 90%).
    const pct = common / Math.max(a.length, b.length);
    if (pct >= 0.7) return Math.round(200 * pct);  // 70% → 140, 90% → 180
    return common;
  };

  // ── Apply: execute a structured insight action ───────────────────
  const [applying, setApplying] = useState<string>("");
  const applyAction = async (a: DashboardNextAction, key: string) => {
    if (applying) return;
    setApplying(key);
    // Track outcome for the per-button checkmark/error indicator. Initially
    // assume success; downgrade on warning/error inside each branch.
    let outcome: ApplyResult = "success";
    try {
      switch (a.action_type) {
        case "run_experiment": {
          const expId = String(a.params?.experiment_id || "").trim();
          if (!expId) {
            toast("Action missing experiment_id", "warning");
            break;
          }
          // Pre-validate against the registry so a hallucinated id never
          // reaches the backend (and never produces a raw HTTP 404).
          // When the ID is hallucinated but we have a strong match, auto-
          // correct to it instead of just warning — the LLM is usually
          // close (e.g. "indus_contact_zone_k" → "contact_zone").
          const registry = await ensureExpRegistry();
          let resolvedId = expId;
          const known = registry.some((e) => e.id === expId);
          if (!known) {
            const ranked = registry
              .map((e) => ({ id: e.id, score: _scoreMatch(expId, e.id) }))
              .sort((x, y) => y.score - x.score);
            const best = ranked[0];
            if (best && best.score >= 80) {
              // Strong match — auto-correct silently with a brief info toast.
              resolvedId = best.id;
              toast(
                `Auto-corrected '${expId}' → ${resolvedId}`,
                "info",
                3000,
              );
            } else {
              // No confident match — warn and bail.
              const suggestions = ranked
                .slice(0, 3)
                .filter((s) => s.score > 4)
                .map((s) => s.id);
              const tail = suggestions.length
                ? ` Did you mean: ${suggestions.join(", ")}?`
                : "";
              toast(
                `Experiment '${expId}' is not registered.${tail}`,
                "warning",
                6000,
              );
              outcome = "error";
              break;
            }
          }
          // Stream the run so the user sees per-node progress in the toast row
          // instead of just "started". Keep the Apply button in its busy state
          // until run_complete / run_error.
          toast(`Started experiment ${resolvedId}`, "info");
          let total = 0;
          let lastTick = 0;
          let runOk = false;
          let runFailed = false;
          let hadNodeError = false;
          try {
            for await (const ev of runGraphExperimentStream(resolvedId, {})) {
              if (ev.event === "started") {
                total = ev.node_count ?? 0;
              } else if (ev.event === "node_start") {
                const idx = (ev.idx ?? 0) + 1;
                const totalNow = ev.total ?? total ?? 0;
                // Throttle progress toasts to one per ~1.2s so we don't spam
                // the toast stack on fast graphs.
                const now = Date.now();
                if (now - lastTick > 1200) {
                  lastTick = now;
                  toast(
                    `${resolvedId}: ${idx}/${totalNow} ${ev.label ?? ""}`.trim(),
                    "info",
                    1500,
                  );
                }
              } else if (ev.event === "node_end" && ev.status === "error") {
                hadNodeError = true;
              } else if (ev.event === "run_complete") {
                runOk = true;
                toast(
                  hadNodeError
                    ? `Experiment ${resolvedId} completed with errors`
                    : `Experiment ${resolvedId} complete`,
                  hadNodeError ? "warning" : "success",
                );
                if (hadNodeError) outcome = "warn";
              } else if (ev.event === "run_error") {
                runFailed = true;
                toast(
                  `Experiment ${resolvedId} failed: ${ev.message ?? "run failed"}`,
                  "error",
                );
                outcome = "error";
              }
            }
            if (!runOk && !runFailed) {
              // Stream closed without an explicit run_complete — surface that
              // rather than silently flashing the success toast.
              toast(`Experiment ${resolvedId} ended without completion event`, "warning");
              outcome = "warn";
            }
          } catch (err) {
            toast(
              err instanceof Error ? err.message : `Experiment ${resolvedId} failed`,
              "error",
            );
            outcome = "error";
          }
          break;
        }
        case "open_view": {
          const view = String(a.params?.view || "dashboard");
          // External views: open in a new tab instead of internal navigation
          if (view === "wiki" || view === "github_wiki") {
            window.open("https://github.com/layer1labs/glossa-lab/wiki", "_blank");
            toast("Opened wiki in new tab", "info");
          } else if (view.startsWith("http://") || view.startsWith("https://")) {
            window.open(view, "_blank");
            toast("Opened link in new tab", "info");
          } else {
            navigate(view);
            toast(`Opened ${view}`, "info");
          }
          break;
        }
        case "run_fetch": {
          await startDiscoveryFetch({});
      toast("Fetch started", "info");
          break;
        }
        case "run_mine": {
          const limit = Number(a.params?.limit ?? 50);
          await startDiscoveryMine({ limit });
      toast(`Mine started · classifying up to ${limit} items`, "info");
          break;
        }
        case "create_hypothesis": {
          const title = String(a.params?.title || a.label || "").slice(0, 200);
          const statement = String(a.params?.statement || a.rationale || "");
          if (!title) {
            toast("Action missing hypothesis title", "warning");
            break;
          }
          await createHypothesis({ title, statement });
          toast(`Hypothesis created: ${title.slice(0, 60)}`, "success");
          break;
        }
        case "propose_experiment_chain": {
          // Automated chain: create hypothesis → pick relevant experiments → run them.
          const hypothesis = String(a.params?.hypothesis || a.label || a.rationale || "");
          if (!hypothesis) { toast("No hypothesis text for chain", "warning"); break; }

          // Step 1: create the hypothesis so it’s tracked.
          try {
            await createHypothesis({ title: hypothesis.slice(0, 200), statement: hypothesis });
            toast(`Hypothesis created: ${hypothesis.slice(0, 60)}`, "success");
          } catch { /* may already exist — continue */ }

          // Step 2: pick relevant experiments from the registry.
          // Use simple keyword overlap between hypothesis text and experiment
          // names/descriptions to select the top 3 most relevant.
          const chainRegistry = await ensureExpRegistry();
          const hypWords = new Set(
            hypothesis.toLowerCase().replace(/[^a-z0-9 ]/g, " ").split(/\s+/).filter(w => w.length > 3),
          );
          const scored = chainRegistry
            .map((e) => {
              const txt = `${e.id} ${e.name ?? ""} ${e.description ?? ""}`.toLowerCase();
              let hits = 0;
              for (const w of hypWords) { if (txt.includes(w)) hits++; }
              return { id: e.id, hits };
            })
            .filter((s) => s.hits > 0)
            .sort((x, y) => y.hits - x.hits)
            .slice(0, 3);

          if (scored.length === 0) {
            toast("No matching experiments found in registry — open Experiment Builder to create one", "warning");
            outcome = "warn";
            break;
          }

          // Step 2b: save experiment IDs back to the hypothesis.
          // createHypothesis returns the existing hypothesis on title-dedup,
          // so we can use it to get the ID without a separate find call.
          const chainExpIds = scored.map(s => s.id);
          try {
            const hyp = await createHypothesis({ title: hypothesis.slice(0, 200), statement: hypothesis });
            if (hyp?.id) {
              const prevIds: string[] = Array.isArray(hyp.exp_ids) ? hyp.exp_ids : [];
              const merged = [...new Set([...prevIds, ...chainExpIds])];
              await updateHypothesis(hyp.id, { exp_ids: merged });
            }
          } catch { /* non-critical — continue */ }

          // Step 3: run each experiment sequentially.
          toast(`Running ${scored.length} experiment(s): ${scored.map(s => s.id).join(", ")}`, "info");
          let chainOk = true;
          for (const s of scored) {
            try {
              let ok = false;
              for await (const ev of runGraphExperimentStream(s.id, {})) {
                if (ev.event === "run_complete") { ok = true; toast(`${s.id} complete`, "success"); }
                if (ev.event === "run_error")    { chainOk = false; toast(`${s.id} failed`, "error"); }
              }
              if (!ok && chainOk) { toast(`${s.id} ended without completion`, "warning"); chainOk = false; }
            } catch (err) {
              chainOk = false;
              toast(`${s.id}: ${err instanceof Error ? err.message : "failed"}`, "error");
            }
          }
          outcome = chainOk ? "success" : "warn";
          break;
        }
        case "ai_chat": {
          const prompt = String(a.params?.prompt || a.label || a.rationale || "");
          openChat({ contextType: "", contextId: "", initialPrompt: prompt, autoSend: true });
          toast("Sent to Glossa AI", "info");
          break;
        }
        case "no_op":
        default:
          // Best-effort: pass arbitrary action types to backend executor.
          if (a.action_type && a.action_type !== "no_op") {
            await executeAiAction({
              type: a.action_type,
              params: (a.params || {}) as Record<string, unknown>,
            });
            toast(`Executed ${a.action_type}`, "success");
          } else {
            toast("Informational only — nothing to apply", "info");
            outcome = "warn";
          }
      }
    } catch (e) {
      toast(e instanceof Error ? e.message : "Action failed", "error");
      outcome = "error";
    } finally {
      setApplying("");
      setApplyResult((prev) => ({ ...prev, [key]: outcome }));
      void refresh();
    }
  };

  // ── render ───────────────────────────────────────────────────────────
  return (
    <div style={{ maxWidth: 1280, margin: "0 auto" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "flex-end", gap: 12,
        marginBottom: 14, flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 240 }}>
          <h2 style={{ margin: 0, fontSize: 22, color: "#111827" }}>📊 Dashboard</h2>
          <p style={{ margin: "4px 0 0", fontSize: 13, color: "#6b7280" }}>
            What&rsquo;s new, what it means, and what to do about it. Highlights
            are pulled from the last {days} days of your discovery feed; AI
            insight tells you how new findings might shift your studies and
            experiments.
          </p>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <select value={days} onChange={(e) => setDays(parseInt(e.target.value, 10))}
            style={selectStyle}>
            {[7, 14, 30, 60, 90].map((d) => (
              <option key={d} value={d}>last {d} days</option>
            ))}
          </select>
          <button onClick={() => void refresh()} disabled={loading} style={btnGhost}>
            {loading ? "…" : "⟳ Reload"}
          </button>
          <button onClick={() => void onRunFetch()} disabled={!!running} style={btnPrimary}
            title="Pull new items from every configured source for every topic. Insight regenerates automatically when fetch completes.">
            {running === "fetch" ? "⏳ Fetching…" : "▶ Fetch now"}
          </button>
          {/* Split Mine button: main click runs at current limit; ▾ opens
              a dropdown to pick a different limit before running. */}
          <div style={{ position: "relative", display: "inline-flex" }}
            title={
              "Mine = ask the LLM to read the next N un-mined items and assign "
              + "each one a kind (study / hypothesis / finding / tablet / review / "
              + "tooling / other), confidence score, short summary, and any extracted "
              + "entity/provider links."
            }>
            <button onClick={() => void onRunMine()} disabled={!!running} style={{
              ...btnAccent, borderTopRightRadius: 0, borderBottomRightRadius: 0,
              paddingRight: 10,
            }}>
              {running === "mine" ? "⏳ Mining…" : `✨ Mine ${mineLimit}`}
            </button>
            <button
              onClick={() => setMineDropOpen((o) => !o)}
              disabled={!!running}
              style={{
                ...btnAccent,
                borderTopLeftRadius: 0, borderBottomLeftRadius: 0,
                borderLeft: "1px solid rgba(255,255,255,0.25)",
                padding: "6px 7px", fontSize: 9, lineHeight: 1,
              }}>
              ▾
            </button>
            {mineDropOpen && (
              <div style={{
                position: "absolute", top: "calc(100% + 4px)", right: 0,
                background: "#fff", border: "1px solid #d1d5db", borderRadius: 6,
                boxShadow: "0 4px 12px rgba(0,0,0,0.15)", zIndex: 100,
                minWidth: 130, overflow: "hidden",
              }}>
                {MINE_LIMIT_OPTIONS.map((n) => (
                  <button key={n} onClick={() => {
                    setMineLimit(n); setMineDropOpen(false); void onRunMine();
                  }} style={{
                    display: "block", width: "100%", padding: "7px 14px",
                    border: "none", background: n === mineLimit ? "#f5f3ff" : "#fff",
                    color: "#374151", fontSize: 12, textAlign: "left",
                    cursor: "pointer", fontWeight: n === mineLimit ? 700 : 400,
                  }}>
                    ✨ Mine {n}
                    {n === mineLimit && <span style={{ color: "#7c3aed", marginLeft: 6, fontSize: 10 }}>✓</span>}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Counters */}
      {data && (
        <div style={{ display: "grid", gap: 10, marginBottom: 16,
          gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))" }}>
          <CounterTile label="Discovery items"  value={data.n_items}        emoji="🔭"
            sub={`last ${data.since_days}d`} onClick={() => navigate("discovery")} />
          <CounterTile label="Studies"          value={data.n_studies}      emoji="📐"
            sub="open builder" onClick={() => navigate("builder")} />
          <CounterTile label="Experiments"      value={data.n_experiments}  emoji="🔀"
            sub="graph registry" onClick={() => navigate("experiments")} />
          <CounterTile label="Saved findings"   value={data.by_status.saved ?? 0}
            emoji="★" sub="for follow-up" onClick={() => navigate("discovery")} />
          <CounterTile label="Hypotheses"       value={data.by_kind.hypothesis ?? 0}
            emoji="💡" sub="extracted" onClick={() => navigate("hypotheses")} />
        </div>
      )}

      {error && (
        <div style={{ background: "#fef2f2", border: "1px solid #fca5a5",
          borderRadius: 7, padding: "10px 14px", fontSize: 13, color: "#b91c1c",
          marginBottom: 12 }}>{error}</div>
      )}

      {/* Two-column main: AI insight (left) + RSS feed (right) */}
      <div style={{ display: "grid", gap: 14, marginBottom: 16,
        gridTemplateColumns: "minmax(0, 1.3fr) minmax(0, 1fr)" }}>

        {/* ── AI Insight ─────────────────────────────────────────────── */}
        <section style={card}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
            <h3 style={cardTitle}>✨ AI Insight</h3>
            <span style={{ flex: 1 }} />
            {insight?.model && (
              <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 8,
                background: insight.model === "ai" ? "#ede9fe" : "#fef3c7",
                color: insight.model === "ai" ? "#6d28d9" : "#92400e",
                fontWeight: 700 }}>
                {insight.model}
              </span>
            )}
            {insightGeneratedAt > 0 && (
              <span
                title={`Last regenerated ${new Date(insightGeneratedAt).toLocaleString()} · only changes on Fetch Now or Regenerate`}
                style={{
                  fontSize: 10, color: "#6b7280",
                  background: "#f3f4f6", padding: "1px 7px", borderRadius: 8,
                }}>
                🕒 Last regen: {fmtAbsoluteShort(insightGeneratedAt)}
                <span style={{ color: "#9ca3af", marginLeft: 4 }}>({fmtRelative(new Date(insightGeneratedAt).toISOString())})</span>
              </span>
            )}
            <button onClick={() => void generateInsight()} disabled={insightLoading}
              style={btnGhost}
              title="Re-run the AI to summarise the latest items. Auto-runs after Fetch, after a backend restart, or after a hard reload — but NOT on every page refresh.">
              {insightLoading ? "…" : "↻ Regenerate"}
            </button>
          </div>
          {insightLoading && !insight && (
            <div style={{ fontSize: 13, color: "#6b7280" }}>
              Asking the AI to read the latest items and tell you what they mean…
            </div>
          )}
          {!insightLoading && !insight && (
            <button onClick={() => void generateInsight()} style={btnPrimary}>
              Generate insight
            </button>
          )}
          {insight && (
            <>
              <p style={{ fontSize: 13, color: "#374151", lineHeight: 1.55,
                margin: "4px 0 12px" }}>{insight.what_it_means}</p>

              {insight.highlights.length > 0 && (
                <>
                  <div style={subhead}>Highlights</div>
                  <ul style={{ margin: "4px 0 12px", paddingLeft: 18 }}>
                    {insight.highlights.map((h, i) => (
                      <li key={i} style={{ fontSize: 12, color: "#111827", marginBottom: 6,
                        lineHeight: 1.5 }}>
                        <strong>{h.title}</strong>
                        <div style={{ color: "#4b5563", fontSize: 12, marginTop: 2 }}>
                          {h.why_it_matters}
                        </div>
                      </li>
                    ))}
                  </ul>
                </>
              )}

              {insight.impact.length > 0 && (
                <>
                  <div style={subhead}>Impact on your studies / experiments</div>
                  <ul style={{ margin: "4px 0 12px", paddingLeft: 18 }}>
                    {insight.impact.map((im, i) => {
                      const k = `impact-${i}`;
                      // suggested_action may be a clean string action_type OR a
                      // legacy structured object {action_type, params}. Normalise
                      // both to (at: string, sp: params object) so the rest of
                      // this view can stay simple.
                      let at: DashboardActionType = "no_op";
                      let sp: Record<string, unknown> = { experiment_id: im.study_or_experiment_id };
                      const sa = im.suggested_action as unknown;
                      if (typeof sa === "string") {
                        at = (sa || "no_op") as DashboardActionType;
                      } else if (sa && typeof sa === "object") {
                        const obj = sa as { action_type?: string; type?: string; params?: Record<string, unknown> };
                        at = ((obj.action_type || obj.type) || "no_op") as DashboardActionType;
                        if (obj.params && typeof obj.params === "object") {
                          sp = { ...obj.params };
                        }
                      }
                      // Backend may also send a sibling `suggested_params` block.
                      if (im.suggested_params && typeof im.suggested_params === "object") {
                        sp = { ...sp, ...(im.suggested_params as Record<string, unknown>) };
                      }
                      // Hide raw hex hash IDs — only show if it looks like an experiment name
                      const idStr = String(im.study_or_experiment_id || "");
                      const looksLikeHash = /^[0-9a-f]{8,}$/i.test(idStr);
                      return (
                        <li key={i} style={{ fontSize: 12, color: "#111827", marginBottom: 6,
                          lineHeight: 1.5, display: "flex", alignItems: "flex-start", gap: 8 }}>
                          <div style={{ flex: 1 }}>
                            {!looksLikeHash && idStr && (
                              <><code style={{ color: "#7c3aed", background: "#f5f3ff",
                                padding: "1px 6px", borderRadius: 4, fontSize: 11 }}>
                                {idStr}
                              </code>{" — "}</>
                            )}
                            {im.impact}
                          </div>
                          {at !== "no_op" && (
                            <button
                              onClick={() => void applyAction({
                                label: actionLabel(at),
                                action_type: at,
                                params: sp,
                                rationale: im.impact,
                              }, k)}
                              disabled={!!applying || applyResult[k] === "success"}
                              style={applyButtonStyle(applyResult[k])}
                              title={applyResultTitle(applyResult[k], at)}
                            >
                              {renderApplyLabel(applying === k, applyResult[k], actionLabel(at))}
                            </button>
                          )}
                        </li>
                      );
                    })}
                  </ul>
                </>
              )}

              {insight.next_actions.length > 0 && (
                <>
                  <div style={subhead}>Next actions</div>
                  <ul style={{ margin: "4px 0 0", paddingLeft: 18,
                    display: "flex", flexDirection: "column", gap: 6 }}>
                    {insight.next_actions.map((a, i) => {
                      const k = `na-${i}`;
                      const isApplyable = a.action_type && a.action_type !== "no_op";
                      return (
                        <li key={i} style={{ fontSize: 12, color: "#111827",
                          lineHeight: 1.5 }}>
                          <div style={{ display: "flex", alignItems: "flex-start", gap: 8 }}>
                            <div style={{ flex: 1 }}>
                              <strong>{a.label}</strong>
                              {a.rationale && (
                                <div style={{ color: "#6b7280", fontSize: 11, marginTop: 2 }}>
                                  {a.rationale}
                                </div>
                              )}
                            </div>
                            {isApplyable && (
                              <button
                                onClick={() => void applyAction(a, k)}
                                disabled={!!applying || applyResult[k] === "success"}
                                style={applyButtonStyle(applyResult[k])}
                                title={applyResultTitle(applyResult[k], a.action_type)}
                              >
                                {renderApplyLabel(applying === k, applyResult[k], actionLabel(a.action_type))}
                              </button>
                            )}
                          </div>
                        </li>
                      );
                    })}
                  </ul>
                </>
              )}
              {insight.error && (
                <div style={{ marginTop: 8, fontSize: 11, color: "#b91c1c" }}>
                  ⚠ {insight.error}
                </div>
              )}
            </>
          )}
        </section>

        {/* ── RSS-style feed ─────────────────────────────────────────── */}
        <section style={card}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
            <h3 style={cardTitle}>📡 Latest feed</h3>
            <span style={{ flex: 1 }} />
            <button onClick={() => navigate("discovery")} style={btnGhost}>
              Open Discovery →
            </button>
          </div>
          {data && data.items.length === 0 && (
            <div style={{ fontSize: 12, color: "#9ca3af", fontStyle: "italic", padding: 8 }}>
              No items in the last {days} days. Click <strong>▶ Fetch now</strong> above
              to pull from your configured sources.
            </div>
          )}
          <div style={{ maxHeight: 540, overflowY: "auto", display: "flex",
            flexDirection: "column", gap: 6 }}>
            {data?.items.map((it) => {
              const k = KIND_COLOURS[it.kind] ?? KIND_COLOURS.other;
              return (
                <div key={it.id} style={{
                  border: "1px solid #e5e7eb", borderRadius: 7, padding: "8px 10px",
                  display: "flex", alignItems: "flex-start", gap: 8,
                }}>
                  {/* Title left-justified at top; kind badge moved to the meta
                      row beneath so titles don't get pushed away from the
                      left edge. AI "✨" stays on the right. */}
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <a href={it.url} target="_blank" rel="noopener noreferrer"
                      style={{ fontSize: 12, fontWeight: 600, color: "#111827",
                        textDecoration: "none", display: "block", textAlign: "left",
                        overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {stripTags(it.title) || "(untitled)"}
                    </a>
                    <div style={{ fontSize: 10, color: "#6b7280", marginTop: 3,
                      display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" }}>
                      <span style={{
                        fontSize: 9, padding: "1px 5px", borderRadius: 3,
                        background: k.bg, color: k.fg, fontWeight: 700,
                        textTransform: "uppercase", letterSpacing: 0.3,
                      }}>
                        {it.kind}
                      </span>
                      <span>📡 {it.source}</span>
                      <span>⬇ {fmtRelative(it.fetched_at)}</span>
                      {it.topic && <span>#{it.topic}</span>}
                    </div>
                  </div>
                  <button onClick={() => askAIAbout(it)} title="Ask Glossa AI about this item"
                    style={miniBtn}>✨</button>
                </div>
              );
            })}
          </div>
        </section>
      </div>

      {/* Tally row */}
      {data && (
        <div style={{ display: "grid", gap: 12,
          gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))" }}>
          <Tally title="By kind"   counts={data.by_kind} />
          <Tally title="By topic"  counts={data.by_topic} />
          <Tally title="By source" counts={data.by_source} />
          <Tally title="By status" counts={data.by_status} />
        </div>
      )}
    </div>
  );
}

// ── Subcomponents ──────────────────────────────────────────────────────

function CounterTile({ label, value, emoji, sub, onClick }: {
  label: string; value: number; emoji: string; sub: string; onClick?: () => void;
}) {
  return (
    <button onClick={onClick} style={{
      padding: "12px 14px", border: "1px solid #e5e7eb", borderRadius: 8,
      background: "#fff", textAlign: "left", cursor: onClick ? "pointer" : "default",
      display: "flex", flexDirection: "column", gap: 2,
    }}>
      <div style={{ fontSize: 22, lineHeight: 1 }}>{emoji}</div>
      <div style={{ fontSize: 22, fontWeight: 800, color: "#111827", lineHeight: 1.1 }}>
        {value.toLocaleString()}
      </div>
      <div style={{ fontSize: 11, fontWeight: 700, color: "#374151" }}>{label}</div>
      <div style={{ fontSize: 10, color: "#9ca3af" }}>{sub}</div>
    </button>
  );
}

function Tally({ title, counts }: { title: string; counts: Record<string, number> }) {
  const entries = Object.entries(counts);
  const max = Math.max(1, ...entries.map(([, v]) => v));
  return (
    <section style={card}>
      <div style={cardTitle}>{title}</div>
      {entries.length === 0 ? (
        <div style={{ fontSize: 11, color: "#9ca3af" }}>No data</div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 4, marginTop: 6 }}>
          {entries.map(([k, v]) => (
            <div key={k} style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ flex: 1, minWidth: 0,
                fontSize: 11, color: "#374151",
                overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {k}
              </div>
              <div style={{ flex: 2, height: 6, background: "#f1f5f9", borderRadius: 3,
                overflow: "hidden" }}>
                <div style={{ height: "100%",
                  width: `${(v / max) * 100}%`, background: "#7c3aed" }} />
              </div>
              <div style={{ width: 32, fontSize: 11, color: "#111827",
                fontWeight: 700, textAlign: "right" }}>{v}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

// ── Styles ────────────────────────────────────────────────────────────
const card: React.CSSProperties = {
  padding: "14px 16px", border: "1px solid #e5e7eb", borderRadius: 10,
  background: "#fff",
};
const cardTitle: React.CSSProperties = {
  margin: 0, fontSize: 13, fontWeight: 700, color: "#111827",
};
const subhead: React.CSSProperties = {
  fontSize: 10, fontWeight: 700, color: "#7c3aed",
  textTransform: "uppercase", letterSpacing: 0.5, marginTop: 8, marginBottom: 4,
};
const selectStyle: React.CSSProperties = {
  padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 5,
  fontSize: 12, background: "#fff",
};
const btnGhost: React.CSSProperties = {
  padding: "5px 10px", border: "1px solid #d1d5db", borderRadius: 5,
  background: "#fff", cursor: "pointer", fontSize: 12, color: "#374151",
};
const btnPrimary: React.CSSProperties = {
  padding: "6px 12px", border: "1px solid #2563eb", borderRadius: 6,
  background: "#2563eb", color: "#fff", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const btnAccent: React.CSSProperties = {
  padding: "6px 12px", border: "1px solid #7c3aed", borderRadius: 6,
  background: "#7c3aed", color: "#fff", fontSize: 12, fontWeight: 600,
  cursor: "pointer",
};
const miniBtn: React.CSSProperties = {
  padding: "2px 6px", border: "1px solid #e5e7eb", borderRadius: 4,
  background: "#fff", cursor: "pointer", fontSize: 11,
};
const btnApply: React.CSSProperties = {
  padding: "3px 9px", border: "1px solid #c4b5fd", borderRadius: 5,
  background: "#f5f3ff", color: "#5b21b6", fontSize: 11, fontWeight: 700,
  cursor: "pointer", whiteSpace: "nowrap", flexShrink: 0,
};
// Apply-button styling per outcome. After success the button visibly
// disables itself with a green check; warnings stay clickable but tinted
// amber; errors are red and clickable for retry.
const btnApplySuccess: React.CSSProperties = {
  ...btnApply,
  border: "1px solid #86efac", background: "#f0fdf4", color: "#166534",
  cursor: "default",
};
const btnApplyWarn: React.CSSProperties = {
  ...btnApply,
  border: "1px solid #fcd34d", background: "#fffbeb", color: "#92400e",
};
const btnApplyError: React.CSSProperties = {
  ...btnApply,
  border: "1px solid #fca5a5", background: "#fef2f2", color: "#991b1b",
};
function applyButtonStyle(r: "success" | "warn" | "error" | undefined): React.CSSProperties {
  if (r === "success") return btnApplySuccess;
  if (r === "warn")    return btnApplyWarn;
  if (r === "error")   return btnApplyError;
  return btnApply;
}
function applyResultTitle(
  r: "success" | "warn" | "error" | undefined,
  actionType: string,
): string {
  if (r === "success") return `Done · ${actionType} (regenerate insight to clear)`;
  if (r === "warn")    return `Completed with warnings · ${actionType} (click to retry)`;
  if (r === "error")   return `Failed · ${actionType} (click to retry)`;
  return `Apply: ${actionType}`;
}
function renderApplyLabel(
  busy: boolean,
  r: "success" | "warn" | "error" | undefined,
  fallback: string,
): string {
  if (busy) return "…";
  if (r === "success") return `✓ Done`;
  if (r === "warn")    return `⚠ ${fallback}`;
  if (r === "error")   return `✗ Retry ${fallback}`;
  return `▶ ${fallback}`;
}

function actionLabel(t: DashboardActionType): string {
  switch (t) {
    case "run_experiment":           return "Run";
    case "open_view":                return "Open";
    case "run_fetch":                return "Fetch";
    case "run_mine":                 return "Mine";
    case "create_hypothesis":        return "Add hypothesis";
    case "propose_experiment_chain": return "Plan chain";
    case "ai_chat":                  return "Ask AI";
    default:                         return "Apply";
  }
}
