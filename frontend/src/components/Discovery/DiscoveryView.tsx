/**
 * DiscoveryView — surfaces continuously-fetched + classified items.
 *
 * Layout:
 *   ┌────────────────────────────────────────────────────────────────────────┐
 *   │ Topic chips (all + per topic, with counts)                            │
 *   │ Kind filter · Status filter · 🔍 search · ▶ Run fetch · ✨ Run mine   │
 *   ├────────────────────────────────────────────────────────────────────────┤
 *   │ Items as cards: title, source, kind chip, confidence bar, summary,    │
 *   │ link chips, actions (Save / Dismiss / Reviewed / Open / Send to AI).  │
 *   └────────────────────────────────────────────────────────────────────────┘
 *
 * All API calls go through the typed helpers added to `frontend/src/api.ts`
 * in Phase G part 1 — see `listDiscoveryItems`, `updateDiscoveryStatus`,
 * `startDiscoveryFetch`, `startDiscoveryMine`, etc.
 */

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  getDiscoveryStats,
  listDiscoveryItems,
  listDiscoverySources,
  listDiscoveryTopics,
  startDiscoveryFetch,
  startDiscoveryMine,
  updateDiscoveryStatus,
  type DiscoveryItem,
  type DiscoverySource,
  type DiscoveryTopic,
} from "../../api";
import { useAIChat } from "../../hooks/useAIChat";
import { useToast } from "../../hooks/useToast";

type StatusFilter = "all" | "new" | "reviewed" | "saved" | "dismissed";
type KindFilter = "all" | "hypothesis" | "finding" | "study" | "tablet" | "review" | "tooling" | "other";

const KIND_COLORS: Record<string, { bg: string; fg: string }> = {
  hypothesis: { bg: "#ede9fe", fg: "#6d28d9" },
  finding:    { bg: "#dcfce7", fg: "#15803d" },
  study:      { bg: "#dbeafe", fg: "#1d4ed8" },
  tablet:     { bg: "#fef3c7", fg: "#b45309" },
  review:     { bg: "#fce7f3", fg: "#be185d" },
  tooling:    { bg: "#e0e7ff", fg: "#4338ca" },
  other:      { bg: "#f3f4f6", fg: "#4b5563" },
};

const STATUS_COLORS: Record<string, { bg: string; fg: string }> = {
  new:       { bg: "#eff6ff", fg: "#2563eb" },
  reviewed:  { bg: "#fef3c7", fg: "#b45309" },
  saved:     { bg: "#dcfce7", fg: "#15803d" },
  dismissed: { bg: "#fee2e2", fg: "#b91c1c" },
};

// ── Helpers ────────────────────────────────────────────────────────────────

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

function topicTags(item: DiscoveryItem): string[] {
  return (item.topic || "").split(",").map((s) => s.trim()).filter(Boolean);
}

// ── Item card ──────────────────────────────────────────────────────────────

interface CardProps {
  item: DiscoveryItem;
  onStatus: (id: string, status: string) => Promise<void>;
}

function ItemCard({ item, onStatus }: CardProps) {
  const { openChat } = useAIChat();
  const [busy, setBusy] = useState<string | null>(null);

  const kc = KIND_COLORS[item.kind] ?? KIND_COLORS.other;
  const sc = STATUS_COLORS[item.status] ?? STATUS_COLORS.new;
  const conf = Math.max(0, Math.min(1, item.confidence));
  const confPct = Math.round(conf * 100);
  const tags = topicTags(item);

  // Filter out the provider meta-link from the visible link chips.
  const displayLinks = (item.links || []).filter((l) => l.kind !== "provider");

  const sendToAI = () => {
    const prompt = [
      `I'm reviewing this discovery item. Help me decide if it's worth following up.`,
      ``,
      `Title: ${item.title}`,
      `Source: ${item.source}`,
      `URL: ${item.url}`,
      `Topic(s): ${item.topic}`,
      item.summary ? `Summary: ${item.summary}` : "",
    ].filter(Boolean).join("\n");
    openChat({ contextType: "", contextId: "", initialPrompt: prompt });
  };

  const setStatus = async (s: string) => {
    setBusy(s);
    try { await onStatus(item.id, s); }
    finally { setBusy(null); }
  };

  return (
    <div style={{
      border: "1px solid #e5e7eb", borderRadius: 9, background: "#fff",
      boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
      overflow: "hidden",
    }}>
      <div style={{ height: 3, background: `linear-gradient(90deg, ${kc.fg}, ${sc.fg})` }} />
      <div style={{ padding: "12px 14px" }}>
        {/* Header row: title + chips */}
        <div style={{ display: "flex", alignItems: "flex-start", gap: 10, marginBottom: 6 }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <a href={item.url} target="_blank" rel="noopener noreferrer"
              style={{
                fontSize: 14, fontWeight: 700, color: "#111827", textDecoration: "none",
                display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical",
                overflow: "hidden",
              }}
              title={item.title}>
              {item.title || "(untitled)"}
            </a>
            <div style={{ fontSize: 11, color: "#6b7280", marginTop: 3, display: "flex", gap: 8, flexWrap: "wrap" }}>
              <span title="Source">📡 {item.source}</span>
              {item.published_at && <span title="Published">📅 {fmtRelative(item.published_at)}</span>}
              {item.fetched_at   && <span title="Fetched">⬇ {fmtRelative(item.fetched_at)}</span>}
              {item.lang && <span title="Language">🗣 {item.lang}</span>}
            </div>
          </div>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 4 }}>
            <span style={{
              fontSize: 10, padding: "2px 7px", borderRadius: 8,
              background: kc.bg, color: kc.fg, fontWeight: 700,
              textTransform: "uppercase", letterSpacing: 0.4,
            }}>
              {item.kind}
            </span>
            <span style={{
              fontSize: 10, padding: "2px 7px", borderRadius: 8,
              background: sc.bg, color: sc.fg, fontWeight: 700,
              textTransform: "uppercase", letterSpacing: 0.4,
            }}>
              {item.status}
            </span>
          </div>
        </div>

        {/* Confidence bar */}
        {item.summary && (
          <div style={{ marginBottom: 6 }}>
            <div style={{
              height: 4, borderRadius: 4, background: "#f1f5f9", overflow: "hidden",
              border: "1px solid #e5e7eb",
            }}>
              <div style={{
                height: "100%", width: `${confPct}%`,
                background: `linear-gradient(90deg, ${kc.fg}, ${kc.fg}cc)`,
              }} />
            </div>
            <div style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>
              confidence: {confPct}%
            </div>
          </div>
        )}

        {/* Summary */}
        {item.summary && (
          <p style={{ margin: "6px 0 8px", fontSize: 12, color: "#374151", lineHeight: 1.5 }}>
            {item.summary}
          </p>
        )}

        {/* Topic tags + linked entities */}
        {(tags.length > 0 || displayLinks.length > 0) && (
          <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginBottom: 8 }}>
            {tags.map((t) => (
              <span key={`topic-${t}`} style={{
                fontSize: 10, padding: "1px 7px", borderRadius: 9,
                background: "#f1f5f9", color: "#475569", border: "1px solid #cbd5e1",
              }}>
                #{t}
              </span>
            ))}
            {displayLinks.slice(0, 8).map((l, i) => (
              <span key={`link-${i}`} style={{
                fontSize: 10, padding: "1px 7px", borderRadius: 9,
                background: "#fef3c7", color: "#92400e", border: "1px solid #fcd34d",
              }} title={l.label || `${l.kind}:${l.target_id}`}>
                {l.kind}:{l.target_id}{l.scheme ? `(${l.scheme})` : ""}
              </span>
            ))}
            {displayLinks.length > 8 && (
              <span style={{ fontSize: 10, color: "#9ca3af" }}>+{displayLinks.length - 8} more</span>
            )}
          </div>
        )}

        {/* Actions */}
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
          <a href={item.url} target="_blank" rel="noopener noreferrer"
             style={{ ...btnSecondary, textDecoration: "none", display: "inline-block" }}>
            🔗 Open
          </a>
          <button onClick={sendToAI} style={btnSecondary} title="Discuss this item with Glossa AI">
            ✨ Send to AI
          </button>
          <span style={{ flex: 1 }} />
          <button onClick={() => void setStatus("saved")} disabled={busy !== null}
            style={{ ...btnSecondary, color: "#15803d", borderColor: "#86efac" }}
            title="Save this item for follow-up">
            {busy === "saved" ? "…" : "★ Save"}
          </button>
          <button onClick={() => void setStatus("reviewed")} disabled={busy !== null}
            style={{ ...btnSecondary, color: "#b45309", borderColor: "#fcd34d" }}
            title="Mark as reviewed (no follow-up)">
            {busy === "reviewed" ? "…" : "✓ Reviewed"}
          </button>
          <button onClick={() => void setStatus("dismissed")} disabled={busy !== null}
            style={{ ...btnSecondary, color: "#b91c1c", borderColor: "#fca5a5" }}
            title="Dismiss as irrelevant">
            {busy === "dismissed" ? "…" : "✗ Dismiss"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Main view ──────────────────────────────────────────────────────────────

export function DiscoveryView() {
  const { toast } = useToast();
  const [items, setItems] = useState<DiscoveryItem[]>([]);
  const [topics, setTopics] = useState<DiscoveryTopic[]>([]);
  const [sources, setSources] = useState<DiscoverySource[]>([]);
  const [topicCounts, setTopicCounts] = useState<Record<string, number>>({});
  const [statusCounts, setStatusCounts] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [topicFilter, setTopicFilter] = useState<string>("all");
  const [kindFilter, setKindFilter] = useState<KindFilter>("all");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("new");
  const [search, setSearch] = useState("");

  const [fetching, setFetching] = useState(false);
  const [mining, setMining] = useState(false);

  // ── Data loading ────────────────────────────────────────────────────────
  const loadMeta = useCallback(async () => {
    try {
      const [tRes, sRes, byTopic, byStatus] = await Promise.all([
        listDiscoveryTopics(),
        listDiscoverySources(),
        getDiscoveryStats("topic"),
        getDiscoveryStats("status"),
      ]);
      setTopics(tRes.topics);
      setSources(sRes.sources);
      setTopicCounts(byTopic.counts || {});
      setStatusCounts(byStatus.counts || {});
    } catch (e) {
      // Non-fatal; the items load below will surface a more useful error.
      console.warn("discovery meta load failed", e);
    }
  }, []);

  const loadItems = useCallback(async () => {
    setError(null); setLoading(true);
    try {
      const params: Record<string, string | number> = { limit: 100 };
      if (topicFilter !== "all")  params.topic = topicFilter;
      if (kindFilter !== "all")   params.kind = kindFilter;
      if (statusFilter !== "all") params.status = statusFilter;
      const res = await listDiscoveryItems(params);
      setItems(res.items);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load discovery items");
    } finally {
      setLoading(false);
    }
  }, [topicFilter, kindFilter, statusFilter]);

  useEffect(() => { void loadMeta(); }, [loadMeta]);
  useEffect(() => { void loadItems(); }, [loadItems]);

  // ── Filtering by free-text search (client-side) ─────────────────────────
  const visible = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return items;
    return items.filter((it) => {
      const hay = [it.title, it.summary, it.source, it.topic, it.url].join(" ").toLowerCase();
      return hay.includes(q);
    });
  }, [items, search]);

  // ── Actions ─────────────────────────────────────────────────────────────
  const onStatus = useCallback(async (id: string, status: string) => {
    try {
      const updated = await updateDiscoveryStatus(id, status);
      setItems((prev) => {
        // If the active filter no longer matches, drop it from the list.
        if (statusFilter !== "all" && updated.status !== statusFilter) {
          return prev.filter((x) => x.id !== id);
        }
        return prev.map((x) => x.id === id ? updated : x);
      });
      // Refresh status counts so the chip badges stay accurate.
      try { setStatusCounts((await getDiscoveryStats("status")).counts || {}); }
      catch { /* ignore */ }
      toast(`Marked ${status}`, "success");
    } catch (e) {
      toast(e instanceof Error ? e.message : "Status update failed", "error");
    }
  }, [statusFilter, toast]);

  const onRunFetch = async () => {
    setFetching(true);
    try {
      const body: { topics?: string[] } = {};
      if (topicFilter !== "all") body.topics = [topicFilter];
      const ack = await startDiscoveryFetch(body);
      toast(`Fetch started · job ${ack.job_id.slice(0, 8)}`, "info");
    } catch (e) {
      toast(e instanceof Error ? e.message : "Fetch failed to start", "error");
    } finally {
      setFetching(false);
    }
  };

  const onRunMine = async () => {
    setMining(true);
    try {
      const body: { topic?: string; limit?: number } = { limit: 25 };
      if (topicFilter !== "all") body.topic = topicFilter;
      const ack = await startDiscoveryMine(body);
      toast(`Mine started · job ${ack.job_id.slice(0, 8)}`, "info");
    } catch (e) {
      toast(e instanceof Error ? e.message : "Mine failed to start (no LLM key?)", "error");
    } finally {
      setMining(false);
    }
  };

  const totalItems = items.length;
  const configuredSources = sources.filter((s) => s.configured).length;

  // ── Render ──────────────────────────────────────────────────────────────
  return (
    <div>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10, flexWrap: "wrap", gap: 8 }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 20, color: "#111827" }}>🔭 Discovery</h2>
          <p style={{ margin: "4px 0 0", fontSize: 12, color: "#6b7280" }}>
            Continuously fetched + classified findings on Indus script, Dravidian linguistics, and IVC archaeology.
            {" "}{configuredSources} of {sources.length} sources configured · keys editable in Settings.
          </p>
        </div>
        <div style={{ display: "flex", gap: 6 }}>
          <button onClick={() => { void loadItems(); void loadMeta(); }} style={btnSecondary} title="Reload">
            ⟳ Reload
          </button>
          <button onClick={() => void onRunFetch()} disabled={fetching}
            style={{ ...btnPrimary, opacity: fetching ? 0.5 : 1, cursor: fetching ? "not-allowed" : "pointer" }}
            title="Fetch new items from configured sources">
            {fetching ? "⏳ Fetching…" : "▶ Run fetch"}
          </button>
          <button onClick={() => void onRunMine()} disabled={mining}
            style={{ ...btnPrimary, background: "#7c3aed",
              opacity: mining ? 0.5 : 1, cursor: mining ? "not-allowed" : "pointer" }}
            title="Classify + link un-mined items via the configured LLM provider">
            {mining ? "⏳ Mining…" : "✨ Run mine"}
          </button>
        </div>
      </div>

      {/* Topic chips */}
      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 10 }}>
        <TopicChip
          id="all" label="All" count={Object.values(topicCounts).reduce((a, b) => a + b, 0)}
          active={topicFilter === "all"} onClick={() => setTopicFilter("all")}
        />
        {topics.map((t) => (
          <TopicChip key={t.id}
            id={t.id} label={t.label} count={topicCounts[t.id] ?? 0}
            active={topicFilter === t.id} onClick={() => setTopicFilter(t.id)}
          />
        ))}
      </div>

      {/* Filters row */}
      <div style={{ display: "flex", gap: 10, marginBottom: 12, flexWrap: "wrap", alignItems: "center" }}>
        <FilterGroup label="Status">
          {(["new", "saved", "reviewed", "dismissed", "all"] as StatusFilter[]).map((s) => (
            <FilterPill key={s} active={statusFilter === s} onClick={() => setStatusFilter(s)}>
              {s === "all" ? "All" : `${s} (${statusCounts[s] ?? 0})`}
            </FilterPill>
          ))}
        </FilterGroup>
        <FilterGroup label="Kind">
          {(["all", "hypothesis", "finding", "study", "tablet", "review", "tooling", "other"] as KindFilter[]).map((k) => (
            <FilterPill key={k} active={kindFilter === k} onClick={() => setKindFilter(k)}>
              {k}
            </FilterPill>
          ))}
        </FilterGroup>
        <input
          value={search} onChange={(e) => setSearch(e.target.value)}
          placeholder="🔍 Search title / summary / source"
          style={{ flex: 1, minWidth: 220, padding: "6px 10px",
            border: "1px solid #d1d5db", borderRadius: 6, fontSize: 12, outline: "none" }}
        />
      </div>

      {/* Errors / state */}
      {error && (
        <div style={{ background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 7,
          padding: "10px 14px", fontSize: 13, color: "#b91c1c", marginBottom: 12 }}>
          {error}
        </div>
      )}

      {loading && <div style={{ color: "#6b7280", fontSize: 13 }}>Loading discovery items…</div>}

      {!loading && !error && totalItems === 0 && (
        <EmptyState
          configuredSources={configuredSources}
          onRunFetch={() => void onRunFetch()}
          fetching={fetching}
        />
      )}

      {!loading && !error && totalItems > 0 && visible.length === 0 && (
        <div style={{ textAlign: "center", padding: "1.5rem", color: "#9ca3af", fontSize: 13 }}>
          No items match the current search. ({totalItems} hidden by search filter.)
        </div>
      )}

      {/* Card list */}
      <div style={{ display: "grid", gap: 10, gridTemplateColumns: "repeat(auto-fill, minmax(380px, 1fr))" }}>
        {visible.map((it) => <ItemCard key={it.id} item={it} onStatus={onStatus} />)}
      </div>
    </div>
  );
}

// ── Sub-components ─────────────────────────────────────────────────────────

function TopicChip({ id, label, count, active, onClick }: {
  id: string; label: string; count: number; active: boolean; onClick: () => void;
}) {
  return (
    <button key={id} onClick={onClick} style={{
      padding: "5px 12px", borderRadius: 16, border: "1px solid",
      background: active ? "#1e3a5f" : "#fff",
      borderColor: active ? "#1e3a5f" : "#d1d5db",
      color: active ? "#fff" : "#374151",
      cursor: "pointer", fontSize: 12, fontWeight: active ? 700 : 500,
      display: "inline-flex", alignItems: "center", gap: 6,
    }}>
      <span>{label}</span>
      <span style={{
        fontSize: 10, padding: "1px 6px", borderRadius: 9,
        background: active ? "rgba(255,255,255,0.2)" : "#f1f5f9",
        color: active ? "#fff" : "#6b7280", fontWeight: 700,
      }}>
        {count}
      </span>
    </button>
  );
}

function FilterGroup({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>
      <span style={{ fontSize: 10, color: "#9ca3af", fontWeight: 700,
        textTransform: "uppercase", letterSpacing: 0.4, marginRight: 4 }}>
        {label}
      </span>
      {children}
    </div>
  );
}

function FilterPill({ active, onClick, children }: {
  active: boolean; onClick: () => void; children: React.ReactNode;
}) {
  return (
    <button onClick={onClick} style={{
      padding: "3px 9px", borderRadius: 5, border: "1px solid",
      background: active ? "#eff6ff" : "#fff",
      borderColor: active ? "#2563eb" : "#e5e7eb",
      color: active ? "#1d4ed8" : "#6b7280",
      cursor: "pointer", fontSize: 11, fontWeight: active ? 700 : 400,
      textTransform: "capitalize",
    }}>
      {children}
    </button>
  );
}

function EmptyState({ configuredSources, onRunFetch, fetching }: {
  configuredSources: number; onRunFetch: () => void; fetching: boolean;
}) {
  return (
    <div style={{ textAlign: "center", padding: "2rem 1rem", color: "#9ca3af",
      border: "1px dashed #cbd5e1", borderRadius: 10, background: "#f8fafc" }}>
      <div style={{ fontSize: 36, marginBottom: 8 }}>🔭</div>
      <div style={{ fontSize: 14, fontWeight: 700, color: "#374151", marginBottom: 6 }}>
        No discovery items yet
      </div>
      <div style={{ fontSize: 12, marginBottom: 16, lineHeight: 1.5 }}>
        {configuredSources === 0 ? (
          <>Add at least one API key in <strong>Settings</strong> (NewsAPI, SerpAPI, or Brave Search), then run a fetch.</>
        ) : (
          <>{configuredSources} source{configuredSources === 1 ? "" : "s"} configured.<br />Run a fetch to pull the latest findings.</>
        )}
      </div>
      <button onClick={onRunFetch} disabled={fetching} style={{
        padding: "8px 20px", border: "none", borderRadius: 7, cursor: fetching ? "not-allowed" : "pointer",
        fontSize: 13, fontWeight: 700, background: "#2563eb", color: "#fff",
        opacity: fetching ? 0.5 : 1,
      }}>
        {fetching ? "⏳ Fetching…" : "▶ Run fetch now"}
      </button>
    </div>
  );
}

// ── Shared styles ──────────────────────────────────────────────────────────

const btnPrimary: React.CSSProperties = {
  padding: "6px 13px", border: "none", borderRadius: 6,
  cursor: "pointer", fontSize: 12, fontWeight: 700,
  background: "#2563eb", color: "#fff",
};

const btnSecondary: React.CSSProperties = {
  padding: "5px 10px", border: "1px solid #e5e7eb", borderRadius: 5,
  cursor: "pointer", fontSize: 11, fontWeight: 500,
  background: "#f9fafb", color: "#374151",
};
