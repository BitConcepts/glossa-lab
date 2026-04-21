import { useEffect, useState } from "react";
import { StatusView } from "./components/StatusView";
import { CorporaView } from "./components/CorporaView";
import { JobsView } from "./components/JobsView";
import { StudiesView } from "./components/StudiesView";
import { PipelinesView } from "./components/PipelinesView";
import { SettingsView } from "./components/SettingsView";
import { ReportsView } from "./components/ReportsView";
import { StudyBuilderView } from "./components/StudyBuilderView";
import { ExperimentBuilderView } from "./components/ExperimentBuilderView";
import { EntropyDashboard } from "./components/EntropyDashboard";
import { HypothesisTracker } from "./components/HypothesisTracker";
import { ResearchNotebook } from "./components/ResearchNotebook";
import { AIToolsView } from "./components/AIToolsView";
import { HelpView } from "./components/HelpView";
import { SignDictionary } from "./components/SignDictionary";
import { TimelineView } from "./components/TimelineView";
import { CitationManager } from "./components/CitationManager";
import { CommandPalette, type PaletteCommand } from "./components/CommandPalette";
import { AIChatWindow, AISidePanel } from "./components/AIChatWindow";
import { BottomPanel } from "./components/BottomPanel";
import { NotificationCenter } from "./components/NotificationDrawer";
import { ToastProvider } from "./hooks/useToast";
import { AIChatProvider, useAIChat } from "./hooks/useAIChat";
import { getHealth } from "./api";

type Tab =
  | "status" | "indus-data" | "builder" | "experiments" | "pipelines"
  | "corpora" | "jobs" | "reports" | "settings"
  | "entropy" | "hypotheses" | "notebooks" | "ai-tools"
  | "signs" | "timeline" | "citations" | "help"
  | "exp-builder"; // legacy alias — still handled but not in nav

interface NavItem { id: Tab; label: string; icon: string; }
interface NavSection { title: string; items: NavItem[]; }

// Navigation organised as always-visible sections (no collapsing)
// Order reflects the deliberate workflow: Corpus → Experiments → Pipelines → Studies → Reports
// "Experiments" is now the full canvas workspace (Exp Builder + gallery).
// "Studies" is the full canvas workspace (Study Builder + study list).
const NAV_SECTIONS: NavSection[] = [
  {
    title: "Workflow",
    items: [
      { id: "corpora",     label: "Corpora",      icon: "📚" },  // 1. Upload data
      { id: "experiments", label: "Experiments",  icon: "🔀" },  // 2. Build + browse graph experiments
      { id: "pipelines",   label: "Pipelines",    icon: "⚙️" },  // 3. Async jobs
      { id: "builder",     label: "Studies",      icon: "📐" },  // 4. Compose + run studies
      { id: "reports",     label: "Reports",      icon: "📄" },  // 5. View results
    ],
  },
  {
    title: "Analysis",
    items: [
      { id: "entropy",    label: "Entropy",     icon: "📊" },
      { id: "signs",      label: "Signs",       icon: "🔣" },
      { id: "timeline",   label: "Timeline",    icon: "📅" },
      { id: "indus-data", label: "Indus Data",  icon: "📋" },
    ],
  },
  {
    title: "Research",
    items: [
      { id: "hypotheses", label: "Hypotheses", icon: "💡" },
      { id: "notebooks",  label: "Notebooks",  icon: "📓" },
      { id: "citations",  label: "Citations",  icon: "📖" },
      { id: "ai-tools",   label: "AI Tools",   icon: "🔬" },
      { id: "help",       label: "Help",        icon: "📘" },
    ],
  },
];

// System items shown at the bottom of the sidebar (separated by a divider)
const SYSTEM_ITEMS: NavItem[] = [
  { id: "status",    label: "Status",    icon: "⚡" },
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
  const [tab, setTab] = useState<Tab>("builder");
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem("glossa_dark") === "1");
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [aiPanelOpen, setAiPanelOpen] = useState(false);
  const [aiPanelWidth, setAiPanelWidth] = useState(320);
  const [aiPanelSide, setAiPanelSide] = useState<"left" | "right">("left");
  // Dirty badges — shown when builders have unsaved local changes
  // Both start false on page load; the Study Builder dispatches glossa:dirty
  // whenever the graph diverges from its last-saved state.
  const [studyDirty, setStudyDirty] = useState(false);
  const [expDirty, setExpDirty] = useState(false);
  // Run indicators: count active runs + track last result
  type RunState = { count: number; lastStatus: "none" | "success" | "fail" };
  const [studyRunState, setStudyRunState] = useState<RunState>({ count: 0, lastStatus: "none" });
  const [expRunState,   setExpRunState]   = useState<RunState>({ count: 0, lastStatus: "none" });
  useEffect(() => {
    const hDirty = (e: Event) => {
      const { builder, dirty } = (e as CustomEvent<{ builder: string; dirty: boolean }>).detail;
      if (builder === "study") setStudyDirty(dirty);
      if (builder === "exp")   setExpDirty(dirty);
    };
    const hRun = (e: Event) => {
      const d = (e as CustomEvent<{ builder: string; running: boolean; status?: string }>).detail;
      const setState = d.builder === "study" ? setStudyRunState : setExpRunState;
      if (d.running) {
        // Run started — increment count + open Jobs panel automatically
        setState(prev => ({ count: prev.count + 1, lastStatus: prev.lastStatus }));
        setPanelVisible(true);
        setPanelMinimized(false);
        setPanelTab("jobs");
      } else {
        // Run finished — decrement count, record status
        const newStatus: RunState["lastStatus"] = d.status === "fail" ? "fail" : "success";
        setState(prev => ({ count: Math.max(0, prev.count - 1), lastStatus: newStatus }));
      }
    };
    window.addEventListener("glossa:dirty",   hDirty);
    window.addEventListener("glossa:running", hRun);
    return () => {
      window.removeEventListener("glossa:dirty",   hDirty);
      window.removeEventListener("glossa:running", hRun);
    };
  }, []);

  // Redirect legacy exp-builder navigations to experiments
  useEffect(() => {
    if (tab === "exp-builder") setTab("experiments");
  }, [tab]);
  // notifOpen removed — NotificationCenter is now self-contained

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
      let view = (e as CustomEvent<{ view: string }>).detail?.view as Tab | undefined;
      // Redirect legacy exp-builder links to the unified experiments canvas
      if (view === "exp-builder") view = "experiments";
      // Redirect old "studies" (Indus data) to new id
      if ((view as string) === "studies") view = "indus-data";
      if (view && (allItems.some(i => i.id === view) || view === "indus-data" || view === "experiments")) setTab(view);
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
    const dirty    = (item.id === "builder" && studyDirty)  || (item.id === "experiments" && expDirty);
    const runState = item.id === "builder" ? studyRunState : item.id === "experiments" ? expRunState : { count: 0, lastStatus: "none" as const };
    const running  = runState.count > 0;
    const lastSt   = runState.lastStatus;
    return (
      <button
        onClick={() => setTab(item.id)}
        title={item.label + (dirty ? " (unsaved changes)" : "")}
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
        <span style={{ flex: 1 }}>{item.label}</span>
        {/* Unsaved: amber dot (only when idle and no last-run indicator) */}
        {dirty && !running && lastSt === "none" && (
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#f59e0b", flexShrink: 0, boxShadow: "0 0 4px #f59e0b" }} title="Unsaved changes" />
        )}
        {/* Running: pulsing green dot */}
        {running && (
          <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#22c55e", flexShrink: 0, boxShadow: "0 0 6px #22c55e", animation: "healthPulse 0.7s ease-in-out infinite" }} title="Running" />
        )}
        {/* Completed: solid green dot */}
        {!running && lastSt === "success" && (
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#22c55e", flexShrink: 0, boxShadow: "0 0 4px #22c55e" }} title="Last run succeeded" />
        )}
        {/* Failed: solid red dot */}
        {!running && lastSt === "fail" && (
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#ef4444", flexShrink: 0, boxShadow: "0 0 4px #ef4444" }} title="Last run failed" />
        )}
      </button>
    );
  };

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden", fontFamily: "system-ui, sans-serif", background: bg }}>

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

        {/* AI assistant button — sits above system items */}
        <div style={{ padding: "6px 10px 4px", flexShrink: 0 }}>
          <button
            onClick={() => setAiPanelOpen(o => !o)}
            title={aiPanelOpen ? "Close AI assistant" : "Open AI assistant"}
            style={{
              width: "100%",
              padding: "8px 12px",
              borderRadius: 8,
              border: aiPanelOpen
                ? "1px solid rgba(124,58,237,0.6)"
                : "1px solid rgba(255,255,255,0.07)",
              background: aiPanelOpen
                ? "linear-gradient(135deg,rgba(124,58,237,0.35),rgba(30,58,95,0.5))"
                : "rgba(255,255,255,0.04)",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: 9,
              color: aiPanelOpen ? "#c4b5fd" : "rgba(255,255,255,0.6)",
              transition: "all 0.15s",
            }}
          >
            <span style={{ fontSize: 14, lineHeight: 1 }}>&#x2728;</span>
            <span style={{ fontSize: 12, fontWeight: aiPanelOpen ? 700 : 500, letterSpacing: 0.1 }}>Glossa AI</span>
            {aiPanelOpen && <span style={{ marginLeft: "auto", fontSize: 10, opacity: 0.6 }}>&#x00d7;</span>}
          </button>
        </div>

        {/* System items at bottom — flexShrink:0 ensures they never get hidden */}
        <div style={{ borderTop: "1px solid rgba(255,255,255,0.08)", paddingTop: 4, paddingBottom: 4, flexShrink: 0 }}>
          {SYSTEM_ITEMS.map((item) => <NavBtn key={item.id} item={item} />)}
        </div>
      </aside>

      {/* ── Main content area ─────────────────────────────────────────────────── */}
      <div style={{
        marginLeft: SIDEBAR_W + (aiPanelOpen && aiPanelSide === "left" ? aiPanelWidth : 0),
        marginRight: aiPanelOpen && aiPanelSide === "right" ? aiPanelWidth : 0,
        flex: 1, minWidth: 0,
        display: "flex", flexDirection: "column",
        height: "100vh",
        overflow: "hidden",
        transition: "margin 0.15s",
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
          {/* Bell portal-based dropdown — z-9500 escapes sticky header stacking context */}
          <NotificationCenter />
          <button
            onClick={() => setDarkMode((d) => !d)}
            title="Toggle dark mode"
            style={{ padding: "4px 8px", border: `1px solid ${border}`, borderRadius: 6, background: "none", cursor: "pointer", fontSize: 14 }}
          >
            {darkMode ? "☀️" : "🌙"}
          </button>
        </div>

        {/* Page content
             Canvas views (builder, experiments) get the full remaining height,
             zero padding, no maxWidth, and marginBottom to sit above the bottom panel.
             All other views get the standard padded, scrollable layout. */}
        {(() => {
          const isCanvas = tab === "builder" || tab === "experiments" || tab === "exp-builder";
          return (
            <main style={{
              flex: 1,
              minHeight: 0,
              display: "flex", flexDirection: "column",
              padding:      isCanvas ? 0 : "24px",
              paddingBottom: isCanvas ? 0 : 32,
              marginBottom:  effectivePanelH,
              color: fg,
              maxWidth: isCanvas ? "none" : 960,
              overflow: isCanvas ? "hidden" : "auto",
            }}>
              {tab === "status"      && <StatusView />}
              {tab === "indus-data"   && <StudiesView />}
              {tab === "builder"      && <StudyBuilderView darkMode={darkMode} />}
              {(tab === "experiments" || tab === "exp-builder") && <ExperimentBuilderView darkMode={darkMode} />}
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
              {tab === "help"        && <HelpView />}
            </main>
          );
        })()}
      </div>

      {/* Command palette */}
      {paletteOpen && <CommandPalette commands={paletteCommands} onClose={() => setPaletteOpen(false)} />}

      {/* NotificationDrawer removed — NotificationCenter is self-contained */}

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

      {/* AI side panel — dockable left/right, resizable */}
      {aiPanelOpen && (
        <AISidePanel
          onClose={() => setAiPanelOpen(false)}
          leftOffset={SIDEBAR_W}
          bottomOffset={effectivePanelH}
          initialSide={aiPanelSide}
          initialWidth={aiPanelWidth}
          onWidthChange={setAiPanelWidth}
          onSideChange={setAiPanelSide}
        />
      )}

      {/* Full AIChatWindow — only rendered when explicitly opened (e.g. undock from ChatInline) */}
      {!aiPanelOpen && <AIChatWindow />}

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
