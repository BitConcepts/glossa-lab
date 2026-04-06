import { useEffect, useState } from "react";
import { StatusView } from "./components/StatusView";
import { CorporaView } from "./components/CorporaView";
import { JobsView } from "./components/JobsView";
import { StudiesView } from "./components/StudiesView";
import { ExperimentsView } from "./components/ExperimentsView";
import { PipelinesView } from "./components/PipelinesView";
import { SettingsView } from "./components/SettingsView";
import { ReportsView } from "./components/ReportsView";
import { StudyBuilderView } from "./components/StudyBuilderView";
import { EntropyDashboard } from "./components/EntropyDashboard";
import { HypothesisTracker } from "./components/HypothesisTracker";
import { ResearchNotebook } from "./components/ResearchNotebook";
import { AIChatView } from "./components/AIChatView";
import { AIToolsView } from "./components/AIToolsView";
import { SignDictionary } from "./components/SignDictionary";
import { TimelineView } from "./components/TimelineView";
import { CitationManager } from "./components/CitationManager";
import { CommandPalette, type PaletteCommand } from "./components/CommandPalette";
import { ToastProvider } from "./hooks/useToast";
import { getHealth } from "./api";

type Tab =
  | "status" | "studies" | "builder" | "experiments" | "pipelines"
  | "corpora" | "jobs" | "reports" | "settings"
  | "entropy" | "hypotheses" | "notebooks" | "ai-chat" | "ai-tools"
  | "signs" | "timeline" | "citations";

interface TabDef { id: Tab; label: string; icon: string; group: string; }

const TABS: TabDef[] = [
  { id: "status",      label: "Status",       icon: "⚡", group: "core" },
  { id: "studies",     label: "Studies",      icon: "📋", group: "core" },
  { id: "builder",     label: "Builder",      icon: "🔧", group: "core" },
  { id: "experiments", label: "Experiments",  icon: "🧪", group: "core" },
  { id: "corpora",     label: "Corpora",      icon: "📚", group: "core" },
  { id: "reports",     label: "Reports",      icon: "📄", group: "core" },
  { id: "entropy",     label: "Entropy",      icon: "📊", group: "analysis" },
  { id: "signs",       label: "Signs",        icon: "𓀀", group: "analysis" },
  { id: "timeline",    label: "Timeline",     icon: "📅", group: "analysis" },
  { id: "hypotheses",  label: "Hypotheses",   icon: "💡", group: "research" },
  { id: "notebooks",   label: "Notebooks",    icon: "📓", group: "research" },
  { id: "citations",   label: "Citations",    icon: "📖", group: "research" },
  { id: "ai-chat",     label: "AI Chat",      icon: "✨", group: "ai" },
  { id: "ai-tools",    label: "AI Tools",     icon: "🔬", group: "ai" },
  { id: "pipelines",   label: "Pipelines",    icon: "⚙️", group: "infra" },
  { id: "jobs",        label: "Jobs",         icon: "📦", group: "infra" },
  { id: "settings",    label: "Settings",     icon: "⚙️", group: "infra" },
];

const GROUP_ORDER = ["core", "analysis", "research", "ai", "infra"];
const GROUP_LABELS: Record<string, string> = {
  core: "Core", analysis: "Analysis", research: "Research", ai: "AI", infra: "System",
};

function HealthBadge() {
  const [status, setStatus] = useState<"healthy" | "degraded" | "down">("down");
  useEffect(() => {
    const check = () => getHealth().then((h) => setStatus(h.status)).catch(() => setStatus("down"));
    check();
    const t = setInterval(check, 6000);
    return () => clearInterval(t);
  }, []);
  const c = { healthy: "#16a34a", degraded: "#d97706", down: "#dc2626" }[status];
  const label = { healthy: "Healthy", degraded: "Degraded", down: "Offline" }[status];
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 5, padding: "3px 9px", borderRadius: 20, background: c + "18", border: `1px solid ${c}38`, flexShrink: 0 }}>
      <span style={{ width: 7, height: 7, borderRadius: "50%", background: c, display: "inline-block", animation: status === "healthy" ? "healthPulse 2s infinite" : "none" }} />
      <span style={{ fontSize: 11, fontWeight: 600, color: c }}>{label}</span>
    </div>
  );
}

function AppContent() {
  const [tab, setTab] = useState<Tab>("studies");
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem("glossa_dark") === "1");
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({
    analysis: false, research: false, ai: false, infra: true,
  });

  useEffect(() => {
    document.body.style.background = darkMode ? "#0f172a" : "#fff";
    document.body.style.color = darkMode ? "#e2e8f0" : "#111827";
    localStorage.setItem("glossa_dark", darkMode ? "1" : "0");
  }, [darkMode]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") { e.preventDefault(); setPaletteOpen(p => !p); }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const paletteCommands: PaletteCommand[] = [
    ...TABS.map((t) => ({
      id: t.id, label: `Go to ${t.label}`, description: `Open the ${t.label} tab`, icon: t.icon,
      action: () => setTab(t.id),
    })),
    { id: "dark-mode", label: "Toggle Dark Mode", icon: darkMode ? "☀️" : "🌙", action: () => setDarkMode(d => !d) },
  ];

  const bg = darkMode ? "#0f172a" : "#fff";
  const cardBg = darkMode ? "#1e293b" : "#fafafa";
  const border = darkMode ? "#334155" : "#e5e7eb";
  const fg = darkMode ? "#e2e8f0" : "#111827";
  const muted = darkMode ? "#94a3b8" : "#6b7280";

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", maxWidth: 1100, margin: "0 auto", padding: "1.25rem 2rem", background: bg, minHeight: "100vh", color: fg }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: "1rem", borderBottom: `2px solid ${border}`, paddingBottom: "0.75rem" }}>
        <div style={{ width: 32, height: 32, borderRadius: 8, background: "linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 14, flexShrink: 0 }}>G</div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h1 style={{ margin: 0, fontSize: "1.15rem", fontWeight: 700, color: fg, lineHeight: 1.2 }}>Glossa Lab</h1>
          <span style={{ color: muted, fontSize: 11 }}>Indus Script Analysis — Dr. A. Fuls, TU Berlin</span>
        </div>
        <HealthBadge />
        <button onClick={() => setPaletteOpen(true)} title="Command palette (Cmd+K)"
          style={{ padding: "4px 10px", border: `1px solid ${border}`, borderRadius: 6, background: cardBg, cursor: "pointer", fontSize: 12, color: muted }}>
          ⌘K
        </button>
        <button onClick={() => setDarkMode(d => !d)} title="Toggle dark mode"
          style={{ padding: "4px 10px", border: `1px solid ${border}`, borderRadius: 6, background: cardBg, cursor: "pointer", fontSize: 14 }}>
          {darkMode ? "☀️" : "🌙"}
        </button>
      </div>

      {/* Tab nav — grouped */}
      <nav style={{ display: "flex", flexWrap: "wrap", gap: 3, marginBottom: "1.5rem", alignItems: "center" }}>
        {GROUP_ORDER.map((group) => {
          const groupTabs = TABS.filter((t) => t.group === group);
          const isCollapsed = collapsed[group];
          const activeInGroup = groupTabs.some((t) => t.id === tab);
          return (
            <div key={group} style={{ display: "flex", alignItems: "center", gap: 2, marginRight: 4 }}>
              <button
                onClick={() => setCollapsed(prev => ({ ...prev, [group]: !prev[group] }))}
                style={{ padding: "3px 6px", border: "none", background: "none", cursor: "pointer", fontSize: 10, color: muted, display: "flex", alignItems: "center", gap: 2 }}
                title={`${isCollapsed ? "Expand" : "Collapse"} ${GROUP_LABELS[group]}`}
              >
                <span style={{ fontSize: 9 }}>{isCollapsed ? "▶" : "▾"}</span>
                <span style={{ textTransform: "uppercase", letterSpacing: 0.5, fontWeight: 600 }}>{GROUP_LABELS[group]}</span>
              </button>
              {!isCollapsed && groupTabs.map((t) => (
                <button
                  key={t.id}
                  onClick={() => setTab(t.id)}
                  style={{
                    padding: "5px 10px", border: "none", borderRadius: 4, cursor: "pointer",
                    fontSize: 12, fontWeight: tab === t.id ? 600 : 400,
                    background: tab === t.id ? "#1e3a5f" : (darkMode ? "#1e293b" : "#f3f4f6"),
                    color: tab === t.id ? "#fff" : (darkMode ? "#94a3b8" : "#374151"),
                    display: "flex", alignItems: "center", gap: 3,
                  }}
                >
                  <span style={{ fontSize: 11 }}>{t.icon}</span>
                  {t.label}
                </button>
              ))}
              {isCollapsed && activeInGroup && (
                <button
                  onClick={() => setCollapsed(prev => ({ ...prev, [group]: false }))}
                  style={{ padding: "5px 10px", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 12, fontWeight: 600, background: "#1e3a5f", color: "#fff", display: "flex", alignItems: "center", gap: 3 }}
                >
                  <span style={{ fontSize: 11 }}>{groupTabs.find(t => t.id === tab)?.icon}</span>
                  {groupTabs.find(t => t.id === tab)?.label}
                </button>
              )}
            </div>
          );
        })}
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
        {tab === "settings"    && <SettingsView />}
        {tab === "entropy"     && <EntropyDashboard />}
        {tab === "hypotheses"  && <HypothesisTracker />}
        {tab === "notebooks"   && <ResearchNotebook />}
        {tab === "ai-chat"     && <AIChatView />}
        {tab === "ai-tools"    && <AIToolsView />}
        {tab === "signs"       && <SignDictionary />}
        {tab === "timeline"    && <TimelineView onNavigate={(t) => setTab(t as Tab)} />}
        {tab === "citations"   && <CitationManager />}
      </main>

      {paletteOpen && <CommandPalette commands={paletteCommands} onClose={() => setPaletteOpen(false)} />}

      <style>{`
        @keyframes healthPulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
      `}</style>
    </div>
  );
}

export function App() {
  return (
    <ToastProvider>
      <AppContent />
    </ToastProvider>
  );
}
