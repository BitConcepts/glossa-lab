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

interface NavItem { id: Tab; label: string; icon: string; }
interface NavSection { title: string; items: NavItem[]; }

// Navigation organised as always-visible sections (no collapsing)
const NAV_SECTIONS: NavSection[] = [
  {
    title: "Workspace",
    items: [
      { id: "studies",     label: "Studies",      icon: "📋" },
      { id: "builder",     label: "Study Builder", icon: "🔧" },
      { id: "experiments", label: "Experiments",   icon: "🧪" },
      { id: "corpora",     label: "Corpora",       icon: "📚" },
      { id: "reports",     label: "Reports",       icon: "📄" },
    ],
  },
  {
    title: "Analysis",
    items: [
      { id: "entropy",    label: "Entropy",    icon: "📊" },
      { id: "signs",      label: "Signs",      icon: "𓀀" },
      { id: "timeline",   label: "Timeline",   icon: "📅" },
    ],
  },
  {
    title: "Research",
    items: [
      { id: "hypotheses", label: "Hypotheses", icon: "💡" },
      { id: "notebooks",  label: "Notebooks",  icon: "📓" },
      { id: "citations",  label: "Citations",  icon: "📖" },
    ],
  },
  {
    title: "AI",
    items: [
      { id: "ai-tools",   label: "AI Tools",   icon: "🔬" },
    ],
  },
];

// System items shown at the bottom of the sidebar (separated by a divider)
const SYSTEM_ITEMS: NavItem[] = [
  { id: "status",    label: "Status",    icon: "⚡" },
  { id: "pipelines", label: "Pipelines", icon: "⚙️" },
  { id: "jobs",      label: "Jobs",      icon: "📦" },
  { id: "settings",  label: "Settings",  icon: "🔧" },
];

const SIDEBAR_W = 220;
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

  // Listen for AI-initiated navigation (open_view action)
  useEffect(() => {
    const handler = (e: Event) => {
      const view = (e as CustomEvent<{ view: string }>).detail?.view as Tab | undefined;
      if (view && allItems.some(i => i.id === view)) setTab(view);
    };
    window.addEventListener("glossa:navigate", handler);
    return () => window.removeEventListener("glossa:navigate", handler);
  // allItems is stable (built from constants)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // All nav items flattened — must be declared before paletteCommands
  const allItems: NavItem[] = [
    ...NAV_SECTIONS.flatMap((s) => s.items),
    ...SYSTEM_ITEMS,
  ];

  const paletteCommands: PaletteCommand[] = [
    ...allItems.map((t) => ({
      id: t.id, label: `Go to ${t.label}`, description: `Open the ${t.label} view`, icon: t.icon,
      action: () => setTab(t.id),
    })),
    { id: "dark-mode", label: "Toggle Dark Mode", icon: darkMode ? "☀️" : "🌙", action: () => setDarkMode(d => !d) },
    { id: "panel-toggle", label: "Toggle Bottom Panel", icon: "⊟", description: "Ctrl+J", action: () => setPanelVisible(v => !v) },
    { id: "panel-logs", label: "Open Logs Panel", icon: "📋", action: () => { setPanelVisible(true); setPanelMinimized(false); setPanelTab("logs"); } },
    { id: "panel-terminal", label: "Open Terminal Panel", icon: ">_", action: () => { setPanelVisible(true); setPanelMinimized(false); setPanelTab("terminal"); } },
    { id: "panel-jobs", label: "Open Jobs Panel", icon: "📦", action: () => { setPanelVisible(true); setPanelMinimized(false); setPanelTab("jobs"); } },
  ];

  // ── Derived colours ─────────────────────────────────────────────────────────
  const bg       = darkMode ? "#0f172a" : "#f8fafc";
  const sideBg   = darkMode ? "#0d1526" : "#1e3a5f";
  const sideText = "#c7d8f0";
  const sideHdr  = "#7a9bbf";
  const activeBg = darkMode ? "rgba(37,99,235,0.25)" : "rgba(96,165,250,0.22)";
  const fg       = darkMode ? "#e2e8f0" : "#111827";
  const border   = darkMode ? "#334155" : "#e5e7eb";
  const cardBg   = darkMode ? "#1e293b" : "#fff";
  const muted    = darkMode ? "#94a3b8" : "#6b7280";

  const currentLabel = allItems.find((i) => i.id === tab)?.label ?? tab;

  // ── Sidebar nav item renderer ─────────────────────────────────────────────
  const NavBtn = ({ item }: { item: NavItem }) => {
    const active = tab === item.id;
    return (
      <button
        onClick={() => setTab(item.id)}
        title={item.label}
        style={{
          display: "flex", alignItems: "center", gap: 9,
          width: "100%", padding: "7px 14px",
          border: "none", borderRadius: 0,
          background: active ? activeBg : "none",
          borderLeft: active ? "3px solid #60a5fa" : "3px solid transparent",
          cursor: "pointer",
          color: active ? "#fff" : sideText,
          fontSize: 13,
          fontWeight: active ? 600 : 400,
          textAlign: "left",
          transition: "background 0.12s",
        }}
      >
        <span style={{ fontSize: 14, lineHeight: 1, flexShrink: 0 }}>{item.icon}</span>
        <span>{item.label}</span>
      </button>
    );
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "system-ui, sans-serif", background: bg }}>

      {/* ── Left sidebar ──────────────────────────────────────────────────────── */}
      <aside style={{
        position: "fixed", top: 0, left: 0, bottom: 0,
        width: SIDEBAR_W,
        background: sideBg,
        display: "flex", flexDirection: "column",
        overflow: "hidden",
        zIndex: 200,
        boxShadow: "2px 0 8px rgba(0,0,0,0.15)",
      }}>

        {/* Logo + title */}
        <div style={{ padding: "18px 14px 14px", borderBottom: "1px solid rgba(255,255,255,0.08)", flexShrink: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 9, marginBottom: 8 }}>
            <div style={{ width: 30, height: 30, borderRadius: 7, background: "linear-gradient(135deg,#2563eb,#60a5fa)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 14, flexShrink: 0 }}>G</div>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#fff", lineHeight: 1.2 }}>Glossa Lab</div>
              <div style={{ fontSize: 9, color: sideHdr, lineHeight: 1.4 }}>Indus Script Analysis</div>
            </div>
          </div>
          <HealthBadge />
        </div>

        {/* Scrollable nav */}
        <div style={{ flex: 1, overflowY: "auto", paddingTop: 6, paddingBottom: 6 }}>
          {NAV_SECTIONS.map((section) => (
            <div key={section.title} style={{ marginBottom: 4 }}>
              <div style={{
                padding: "8px 14px 4px",
                fontSize: 10, fontWeight: 700,
                color: sideHdr,
                textTransform: "uppercase",
                letterSpacing: 1,
              }}>
                {section.title}
              </div>
              {section.items.map((item) => <NavBtn key={item.id} item={item} />)}
            </div>
          ))}
        </div>

        {/* System items at bottom — flexShrink:0 ensures they never get hidden */}
        <div style={{ borderTop: "1px solid rgba(255,255,255,0.08)", paddingTop: 4, paddingBottom: 4, flexShrink: 0 }}>
          {SYSTEM_ITEMS.map((item) => <NavBtn key={item.id} item={item} />)}
        </div>
      </aside>

      {/* ── Main content area ─────────────────────────────────────────────────── */}
      <div style={{
        marginLeft: SIDEBAR_W,
        flex: 1, minWidth: 0,
        display: "flex", flexDirection: "column",
        minHeight: "100vh",
      }}>

        {/* Top bar */}
        <div style={{
          display: "flex", alignItems: "center", gap: 8,
          padding: "10px 24px",
          borderBottom: `1px solid ${border}`,
          background: cardBg,
          flexShrink: 0,
          position: "sticky", top: 0, zIndex: 100,
        }}>
          {/* Breadcrumb */}
          <span style={{ fontSize: 13, color: muted }}>Glossa Lab</span>
          <span style={{ color: border, fontSize: 13 }}>/</span>
          <span style={{ fontSize: 13, fontWeight: 600, color: fg }}>{currentLabel}</span>

          <div style={{ flex: 1 }} />

          <NotificationBell onClick={() => setNotifOpen((o) => !o)} />
          <button
            onClick={() => setPaletteOpen(true)}
            title="Command palette (Cmd+K)"
            style={{ padding: "4px 10px", border: `1px solid ${border}`, borderRadius: 6, background: "none", cursor: "pointer", fontSize: 12, color: muted }}
          >
            ⌘K
          </button>
          <button
            onClick={() => setPanelVisible((v) => !v)}
            title="Toggle panel (Ctrl+J)"
            style={{ padding: "4px 10px", border: `1px solid ${border}`, borderRadius: 6, background: "none", cursor: "pointer", fontSize: 12, color: panelVisible ? "#2563eb" : muted }}
          >
            ⊟
          </button>
          <button
            onClick={() => setDarkMode((d) => !d)}
            title="Toggle dark mode"
            style={{ padding: "4px 8px", border: `1px solid ${border}`, borderRadius: 6, background: "none", cursor: "pointer", fontSize: 14 }}
          >
            {darkMode ? "☀️" : "🌙"}
          </button>
        </div>

        {/* Page content */}
        <main style={{
          flex: 1,
          padding: "24px",
          paddingBottom: effectivePanelH + 32,
          color: fg,
          maxWidth: 960,
        }}>
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
      </div>

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
          leftOffset={SIDEBAR_W}
        />
      )}

      {/* Floating AI Chat */}
      <AIChatWindow panelHeight={panelVisible && !panelMinimized ? panelHeight : 0} />
      <AIChatBubble panelHeight={panelVisible && !panelMinimized ? panelHeight : 0} />

      <style>{`
        @keyframes healthPulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        aside::-webkit-scrollbar { width: 4px; }
        aside::-webkit-scrollbar-track { background: transparent; }
        aside::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 2px; }
        aside button:hover { background: rgba(255,255,255,0.08) !important; }
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
