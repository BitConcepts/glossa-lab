import { useState } from "react";
import { StatusView } from "./components/StatusView";
import { CorporaView } from "./components/CorporaView";
import { JobsView } from "./components/JobsView";

type Tab = "status" | "corpora" | "jobs";

const TABS: { id: Tab; label: string }[] = [
  { id: "status", label: "Status" },
  { id: "corpora", label: "Corpora" },
  { id: "jobs", label: "Jobs" },
];

export function App() {
  const [tab, setTab] = useState<Tab>("status");

  return (
    <div
      style={{
        fontFamily: "system-ui, sans-serif",
        maxWidth: 960,
        margin: "0 auto",
        padding: "1.5rem 2rem",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          gap: "1.5rem",
          marginBottom: "1.5rem",
          borderBottom: "2px solid #e5e7eb",
          paddingBottom: "0.75rem",
        }}
      >
        <h1 style={{ margin: 0, fontSize: "1.4rem", fontWeight: 700 }}>
          Glossa Lab
        </h1>
        <span style={{ color: "#6b7280", fontSize: 13 }}>
          Ancient &amp; modern language analysis
        </span>
      </div>

      {/* Tab bar */}
      <nav style={{ display: "flex", gap: 4, marginBottom: "1.5rem" }}>
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            style={{
              padding: "6px 16px",
              border: "none",
              borderRadius: 4,
              cursor: "pointer",
              fontSize: 14,
              fontWeight: tab === t.id ? 600 : 400,
              background: tab === t.id ? "#2563eb" : "#f3f4f6",
              color: tab === t.id ? "#fff" : "#374151",
            }}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {/* View */}
      <main>
        {tab === "status" && <StatusView />}
        {tab === "corpora" && <CorporaView />}
        {tab === "jobs" && <JobsView />}
      </main>
    </div>
  );
}
