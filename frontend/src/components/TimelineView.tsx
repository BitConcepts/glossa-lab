/**
 * TimelineView — chronological timeline of experiments and studies.
 * Shows items ordered by date with clickable entries.
 */
import { useEffect, useState } from "react";
import { listExperiments, listStudies, type ExperimentMeta, type StudyResponse } from "../api";

type TimelineItem =
  | { kind: "experiment"; date: string; data: ExperimentMeta }
  | { kind: "study"; date: string; data: StudyResponse };

export function TimelineView({ onNavigate }: { onNavigate?: (tab: string) => void }) {
  const [items, setItems] = useState<TimelineItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "experiment" | "study">("all");

  useEffect(() => {
    Promise.all([listExperiments(), listStudies()]).then(([exps, studies]) => {
      const timeline: TimelineItem[] = [
        ...exps.map((e) => ({ kind: "experiment" as const, date: "2026-01-01", data: e })),
        ...studies.map((s) => ({ kind: "study" as const, date: s.created_at.slice(0, 10), data: s })),
      ];
      timeline.sort((a, b) => b.date.localeCompare(a.date));
      setItems(timeline);
    }).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const visible = filter === "all" ? items : items.filter((i) => i.kind === filter);

  // Group by month
  const grouped: Record<string, TimelineItem[]> = {};
  for (const item of visible) {
    const month = item.date.slice(0, 7);
    if (!grouped[month]) grouped[month] = [];
    grouped[month].push(item);
  }

  const months = Object.keys(grouped).sort((a, b) => b.localeCompare(a));

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>Timeline</h2>
        <div style={{ display: "flex", gap: 6 }}>
          {(["all", "experiment", "study"] as const).map((f) => (
            <button key={f} onClick={() => setFilter(f)}
              style={{ padding: "3px 12px", borderRadius: 6, border: "1px solid", cursor: "pointer", fontSize: 12,
                background: filter === f ? "#1e3a5f" : "#fff", borderColor: filter === f ? "#1e3a5f" : "#d1d5db",
                color: filter === f ? "#fff" : "#374151" }}>
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>
      <p style={{ margin: "0 0 1.25rem", fontSize: 13, color: "#6b7280" }}>
        Chronological overview of experiments and studies.
      </p>

      {loading && <p style={{ color: "#6b7280", fontSize: 13 }}>Loading…</p>}

      {months.map((month) => (
        <div key={month} style={{ marginBottom: "1.5rem" }}>
          <div style={{ fontSize: 12, fontWeight: 700, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8, borderBottom: "1px solid #f3f4f6", paddingBottom: 4 }}>
            {month}
          </div>
          <div style={{ position: "relative", paddingLeft: 24 }}>
            {/* Timeline line */}
            <div style={{ position: "absolute", left: 8, top: 0, bottom: 0, width: 2, background: "#e5e7eb" }} />
            {grouped[month].map((item, i) => {
              const isExp = item.kind === "experiment";
              const color = isExp ? "#2563eb" : "#7c3aed";
              const label = isExp ? (item.data as ExperimentMeta).name : (item.data as StudyResponse).name;
              const sub = isExp
                ? `${(item.data as ExperimentMeta).category} · ${(item.data as ExperimentMeta).estimated_time}`
                : `Study · ${(item.data as StudyResponse).graph?.nodes?.length ?? 0} experiments`;
              const target = isExp ? "experiments" : "builder";
              return (
                <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start", marginBottom: 12 }}>
                  {/* Dot */}
                  <div style={{
                    position: "absolute", left: 4, width: 10, height: 10, borderRadius: "50%",
                    background: color, border: "2px solid #fff", boxShadow: `0 0 0 2px ${color}40`,
                    marginTop: 2,
                  }} />
                  <div style={{ flex: 1, cursor: onNavigate ? "pointer" : "default", padding: "8px 12px", borderRadius: 6, border: "1px solid #f3f4f6", background: "#fafafa", transition: "all 0.15s" }}
                    onClick={() => onNavigate?.(target)}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      <span style={{ fontSize: 11, padding: "1px 6px", borderRadius: 6, background: color + "20", color, fontWeight: 700 }}>
                        {isExp ? "experiment" : "study"}
                      </span>
                      <span style={{ fontWeight: 600, fontSize: 13, color: "#111827" }}>{label}</span>
                    </div>
                    <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>{sub}</div>
                    {!isExp && (item.data as StudyResponse).description && (
                      <p style={{ margin: "4px 0 0", fontSize: 12, color: "#9ca3af", lineHeight: 1.4 }}>
                        {((item.data as StudyResponse).description ?? "").slice(0, 80)}…
                      </p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}

      {!loading && items.length === 0 && (
        <div style={{ textAlign: "center", padding: "3rem", color: "#9ca3af" }}>
          <div style={{ fontSize: 32 }}>📅</div>
          <div style={{ marginTop: 8 }}>No items yet. Run experiments or create studies to populate the timeline.</div>
        </div>
      )}
    </div>
  );
}
