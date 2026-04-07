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
import { AIToolsView } from "./components/AIToolsView";
import { SignDictionary } from "./components/SignDictionary";
import { TimelineView } from "./components/TimelineView";
import { CitationManager } from "./components/CitationManager";
import { CommandPalette, type PaletteCommand } from "./components/CommandPalette";
import { AIChatBubble, AIChatWindow } from "./components/AIChatWindow";
import { BottomPanel } from "./components/BottomPanel";
import { NotificationBell, NotificationDrawer } from "./components/NotificationDrawer";
import { ToastProvider } from "./hooks/useToast";
import { AIChatProvider, useAIChat } from "./hooks/useAIChat";
import { getHealth } from "./api";

type Tab =
  | "status" | "studies" | "builder" | "experiments" | "pipelines"
  | "corpora" | "jobs" | "reports" | "settings"
  | "entropy" | "hypotheses" | "notebooks" | "ai-tools"
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
  { id: "ai-tools",    label: "AI Tools",     icon: "🔬", group: "ai" },
  { id: "pipelines",   label: "Pipelines",    icon: "⚙️", group: "infra" },
  { id: "jobs",        label: "Jobs",         icon: "📦", group: "infra" },
  { id: "settings",    label: "Settings",     icon: "⚙️", group: "infra" },
];

const GROUP_ORDER = ["core", "analysis", "research", "ai", "infra"];
const GROUP_LABELS: Record<string, string> = {
  core: "Core", analysis: "Analysis", research: "Research", ai: "AI", infra: "System",
};

const DEFAULT_PANEL_HEIGHT = 220;
type PanelTab = "logs" | "jobs" | "terminal" | "chat";

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
  const [notifOpen, setNotifOpen] = useState(false);
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({
    analysis: false, research: false, ai: false, infra: true,
  });

  // Bottom panel state
  const [panelHeight, setPanelHeight] = useState(DEFAULT_PANEL_HEIGHT);
  const [panelMinimized, setPanelMinimized] = useState(false);
  const [panelTab, setPanelTab] = useState<PanelTab>("logs");
  const [panelVisible, setPanelVisible] = useState(true);

  // Open panel to Chat tab whenever AI chat is docked
  const { isDocked } = useAIChat();
  useEffect(() => {
    if (isDocked) { setPanelVisible(true); setPanelMinimized(false); setPanelTab("chat"); }
  }, [isDocked]);

  const effectivePanelH = panelVisible ? (panelMinimized ? 30 : panelHeight) : 0;

  useEffect(() => {
    document.body.style.background = darkMode ? "#0f172a" : "#fff";
    document.body.style.color = darkMode ? "#e2e8f0" : "#111827";
    localStorage.setItem("glossa_dark", darkMode ? "1" : "0");
  }, [darkMode]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") { e.preventDefault(); setPaletteOpen(p => !p); }
      if ((e.metaKey || e.ctrlKey) && e.key === "j") { e.preventDefault(); setPanelVisible(v => !v); }
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
    { id: "panel-toggle", label: "Toggle Bottom Panel", icon: "⊟", description: "Ctrl+J", action: () => setPanelVisible(v => !v) },
    { id: "panel-logs", label: "Open Logs Panel", icon: "📋", action: () => { setPanelVisible(true); setPanelMinimized(false); setPanelTab("logs"); } },
    { id: "panel-terminal", label: "Open Terminal Panel", icon: ">_", action: () => { setPanelVisible(true); setPanelMinimized(false); setPanelTab("terminal"); } },
    { id: "panel-jobs", label: "Open Jobs Panel", icon: "📦", action: () => { setPanelVisible(true); setPanelMinimized(false); setPanelTab("jobs"); } },
  ];

  const bg = darkMode ? "#0f172a" : "#fff";
  const cardBg = darkMode ? "#1e293b" : "#fafafa";
  const border = darkMode ? "#334155" : "#e5e7eb";
  const fg = darkMode ? "#e2e8f0" : "#111827";
  const muted = darkMode ? "#94a3b8" : "#6b7280";

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", maxWidth: 1100, margin: "0 auto", padding: "1.25rem 2rem", background: bg, minHeight: "100vh", color: fg, paddingBottom: effectivePanelH + 32 }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: "1rem", borderBottom: `2px solid ${border}`, paddingBottom: "0.75rem" }}>
        <div style={{ width: 32, height: 32, borderRadius: 8, background: "linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 14, flexShrink: 0 }}>G</div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h1 style={{ margin: 0, fontSize: "1.15rem", fontWeight: 700, color: fg, lineHeight: 1.2 }}>Glossa Lab</h1>
          <span style={{ color: muted, fontSize: 11 }}>Indus Script Analysis — Dr. A. Fuls, TU Berlin</span>
        </div>
        <HealthBadge />
        <NotificationBell onClick={() => setNotifOpen(o => !o)} />
        <button onClick={() => setPaletteOpen(true)} title="Command palette (Cmd+K)"
          style={{ padding: "4px 10px", border: `1px solid ${border}`, borderRadius: 6, background: cardBg, cursor: "pointer", fontSize: 12, color: muted }}>
          ⌘K
        </button>
        <button onClick={() => setPanelVisible(v => !v)} title="Toggle panel (Ctrl+J)"
          style={{ padding: "4px 10px", border: `1px solid ${border}`, borderRadius: 6, background: cardBg, cursor: "pointer", fontSize: 12, color: panelVisible ? "#2563eb" : muted }}>
          ⊟
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
        {tab === "ai-tools"    && <AIToolsView />}
        {tab === "signs"       && <SignDictionary />}
        {tab === "timeline"    && <TimelineView onNavigate={(t) => setTab(t as Tab)} />}
        {tab === "citations"   && <CitationManager />}
      </main>

      {/* Command palette */}
      {paletteOpen && <CommandPalette commands={paletteCommands} onClose={() => setPaletteOpen(false)} />}

      {/* Notification drawer */}
      <NotificationDrawer open={notifOpen} onClose={() => setNotifOpen(false)} />

      {/* Bottom IDE panel */}
      {panelVisible && (
        <BottomPanel
          height={panelHeight}
          onHeightChange={setPanelHeight}
          minimized={panelMinimized}
          onMinimizedChange={setPanelMinimized}
          activeTab={panelTab}
          onTabChange={setPanelTab}
        />
      )}

      {/* Floating AI Chat */}
      <AIChatWindow />
      <AIChatBubble />

      <style>{`
        @keyframes healthPulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
      `}</style>
    </div>
  );
}

export function App() {
  return (
    <ToastProvider>
      <AIChatProvider>
        <AppContent />
      </AIChatProvider>
    </ToastProvider>
  );
}
