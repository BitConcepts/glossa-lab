import { useState } from "react";
import { StatusView } from "./components/StatusView";
import { CorporaView } from "./components/CorporaView";
import { JobsView } from "./components/JobsView";
import { StudiesView } from "./components/StudiesView";
import { ExperimentsView } from "./components/ExperimentsView";
import { PipelinesView } from "./components/PipelinesView";
import { SettingsView } from "./components/SettingsView";
import { ReportsView } from "./components/ReportsView";
import { PresetsView } from "./components/PresetsView";
import { StudyBuilderView } from "./components/StudyBuilderView";

type Tab = "status" | "studies" | "builder" | "experiments" | "pipelines" | "corpora" | "jobs" | "reports" | "presets" | "settings";

const TABS: { id: Tab; label: string; badge?: string }[] = [
  { id: "status",      label: "Status" },
  { id: "studies",     label: "Indus Studies",  badge: "NEW" },
  { id: "builder",     label: "Study Builder" },
  { id: "experiments", label: "Experiments" },
  { id: "pipelines",   label: "Pipelines",      badge: "17" },
  { id: "corpora",     label: "Corpora" },
  { id: "jobs",        label: "Jobs" },
  { id: "reports",     label: "Reports" },
  { id: "presets",     label: "Presets" },
  { id: "settings",    label: "Settings" },
];

export function App() {
  const [tab, setTab] = useState<Tab>("studies");

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", maxWidth: 1100, margin: "0 auto", padding: "1.25rem 2rem" }}>
      {/* Header */}
      <div style={{
        display: "flex", alignItems: "center", gap: "1rem",
        marginBottom: "1.25rem", borderBottom: "2px solid #e5e7eb", paddingBottom: "0.75rem",
      }}>
        <div style={{
          width: 32, height: 32, borderRadius: 8,
          background: "linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)",
          display: "flex", alignItems: "center", justifyContent: "center",
          color: "#fff", fontWeight: 800, fontSize: 14, flexShrink: 0,
        }}>G</div>
        <div>
          <h1 style={{ margin: 0, fontSize: "1.25rem", fontWeight: 700, color: "#111827" }}>Glossa Lab</h1>
          <span style={{ color: "#6b7280", fontSize: 12 }}>Indus Script Analysis — Collaboration with Dr. A. Fuls, TU Berlin</span>
        </div>
      </div>

      {/* Tab bar */}
      <nav style={{ display: "flex", gap: 3, marginBottom: "1.5rem", flexWrap: "wrap" }}>
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            style={{
              padding: "6px 14px", border: "none", borderRadius: 4,
              cursor: "pointer", fontSize: 13,
              fontWeight: tab === t.id ? 600 : 400,
              background: tab === t.id ? "#1e3a5f" : "#f3f4f6",
              color: tab === t.id ? "#fff" : "#374151",
              display: "flex", alignItems: "center", gap: 5,
            }}
          >
            {t.label}
            {t.badge && (
              <span style={{
                fontSize: 10, padding: "1px 5px", borderRadius: 8,
                background: tab === t.id ? "rgba(255,255,255,0.25)" : "#e5e7eb",
                color: tab === t.id ? "#fff" : "#6b7280", fontWeight: 700,
              }}>{t.badge}</span>
            )}
          </button>
        ))}
      </nav>

      {/* View */}
      <main>
        {tab === "status"      && <StatusView />}
        {tab === "studies"     && <StudiesView />}
        {tab === "builder"     && <StudyBuilderView />}
        {tab === "experiments" && <ExperimentsView />}
        {tab === "pipelines"   && <PipelinesView />}
        {tab === "corpora"     && <CorporaView />}
        {tab === "jobs"        && <JobsView />}
        {tab === "reports"     && <ReportsView />}
        {tab === "presets"     && <PresetsView />}
        {tab === "settings"    && <SettingsView />}
      </main>
    </div>
  );
}
