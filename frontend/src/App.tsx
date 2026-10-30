import { useEffect, useRef, useState } from "react";
import { StatusView } from "./components/StatusView";
import { JobsView } from "./components/JobsView";
import { SettingsView } from "./components/SettingsView";
import { ReportsView } from "./components/ReportsView";
import { ProjectsView } from "./components/ProjectsView";
import { ExperimentBuilderView } from "./components/ExperimentBuilderView";
import { AIToolsView } from "./components/AIToolsView";
import { HelpView } from "./components/HelpView";
import { ProgramHome } from "./components/ProgramHome";
import { DigestionBoard, effectiveStage } from "./components/DigestionBoard";
import { ClaimsView } from "./components/ClaimsView";
import { FoundationCheckView } from "./components/FoundationCheckView";
import { DiscoveryView } from "./components/Discovery/DiscoveryView";
import { EvidenceSourcesView } from "./components/EvidenceSourcesView";
import { DataView } from "./components/DataView";
import { AnalysisView } from "./components/AnalysisView";
import { SweepPanel } from "./components/SweepPanel";
import { ApiTokenGate, useAuthState } from "./components/ApiToken";
import { ResearchLoopPanel } from "./components/ResearchLoopPanel";
import { ProgramsView } from "./components/ProgramsView";
import { CommandPalette, type PaletteCommand } from "./components/CommandPalette";
import { AISidePanel } from "./components/AIChatWindow";
import { NotificationCenter } from "./components/NotificationDrawer";
import { ToastProvider } from "./hooks/useToast";
import { AIChatProvider } from "./hooks/useAIChat";
import { ProjectProvider, useProject } from "./hooks/useProject";
import {
  getDiscoveryStats, getStatus, listIndusClaims, listJobs,
  getOllamaContextConfig, setLocalCtxLength,
  type StatusResponse,
} from "./api";
import { fmtClock } from "./components/ui081";

/**
 * Spec 081 shell. The tool's top-level unit is the *program* (the
 * Project entity in UI language). Navigation has two spaces:
 *   program space — Home, Claims, Digestion, Evidence & sources, Data,
 *     Analysis, Experiments, Discovery, Research loop, Reports & ledger
 *     (in loop order, FR-002);
 *   tool space — Jobs, Status, Settings, Help.
 * The shell contains no program's subject matter (FR-001/C081-1).
 * Legacy view ids resolve to the new routes at navigation time.
 */
type Tab =
  | "programs" | "home" | "claims" | "digestion" | "evidence" | "data"
  | "analysis" | "experiments" | "discovery" | "loop" | "reports"
  | "jobs" | "status" | "settings" | "help"
  // Utility routes (not in the nav): the foundation check opens from
  // the program home (FR-006); AI tools is a workbench reached from
  // the palette/settings, not a destination (Q6); builder is the
  // legacy program manager.
  | "foundation-check" | "ai-tools" | "builder"
  // Analysis sub-views, addressed directly; the Analysis wrapper
  // renders them as tabs (step 6).
  | "entropy" | "signs" | "timeline"
  // Legacy ids — resolved at navigation time, never stored.
  | "dashboard" | "corpora" | "pipelines" | "hypotheses" | "notebooks"
  | "citations" | "correspondence" | "exp-builder";

interface NavItem { id: Tab; label: string; icon: string; count?: number; alert?: boolean }

const SIDEBAR_W = 232;
const MOBILE_NAV_H = 56;

/** Resolve any legacy/alias view id to a current route id (Spec 081 step 1). */
function resolveView(view: string, hasProgram: boolean): Tab | null {
  switch (view) {
    case "exp-builder": return "experiments";
    case "studies": return "claims";
    case "indus-data": return hasProgram ? "home" : "programs";
    case "dashboard": return hasProgram ? "home" : "programs";
    case "foundation": return "foundation-check";
    case "ai_tools": return "ai-tools";
    case "hypothesis": case "hypotheses": return "claims";
    case "notebook": case "notebooks": return "evidence";
    case "citations": case "correspondence": return "evidence";
    case "job": return "jobs";
    case "corpora": return "data";
    case "pipelines": return "experiments";
    case "projects": return "programs";
    default: return null;
  }
}

const VALID_TABS: ReadonlySet<string> = new Set([
  "programs", "home", "claims", "digestion", "evidence", "data", "analysis",
  "experiments", "discovery", "loop", "reports", "jobs", "status", "settings",
  "help", "foundation-check", "ai-tools", "builder", "entropy", "signs", "timeline",
]);

const TAB_LABELS: Partial<Record<Tab, string>> = {
  programs: "Programs", home: "Home", claims: "Claims", digestion: "Digestion",
  evidence: "Evidence & sources", data: "Data", analysis: "Analysis",
  experiments: "Experiments", discovery: "Discovery", loop: "Research loop",
  reports: "Reports & ledger", jobs: "Jobs", status: "Status",
  settings: "Settings", help: "Help", "foundation-check": "Foundation Check",
  "ai-tools": "AI Tools", builder: "Manage programs",
  entropy: "Analysis", signs: "Analysis", timeline: "Analysis",
};

function initialTabFromHash(): Tab {
  const m = window.location.hash.match(/^#\/([a-z-]+)/);
  if (m && VALID_TABS.has(m[1])) return m[1] as Tab;
  return "programs";
}

// ── Mobile bottom nav (FR-002: Home / Claims / Digestion / Jobs / More) ──
function MobileNavBar({
  active, onNav, hasProgram,
}: {
  active: Tab;
  onNav: (t: Tab) => void;
  hasProgram: boolean;
}) {
  const items: { id: Tab | "menu"; label: string; icon: string }[] = [
    { id: hasProgram ? "home" : "programs", label: "Home", icon: "⌂" },
    { id: "claims", label: "Claims", icon: "§" },
    { id: "digestion", label: "Digestion", icon: "✓" },
    { id: "jobs", label: "Jobs", icon: "⚙" },
    { id: "menu", label: "More", icon: "☰" },
  ];
  return (
    <div style={{
      position: "fixed", bottom: 0, left: 0, right: 0, zIndex: 250,
      height: MOBILE_NAV_H,
      paddingBottom: "env(safe-area-inset-bottom, 0px)",
      background: "#1e3a5f",
      borderTop: "1px solid rgba(255,255,255,0.10)",
      display: "flex", alignItems: "stretch",
      boxShadow: "0 -2px 12px rgba(0,0,0,0.3)",
    }}>
      {items.map(item => {
        const isMenu = item.id === "menu";
        const isActive = !isMenu && active === item.id;
        return (
          <button
            key={item.label}
            onClick={() => {
              if (isMenu) { window.dispatchEvent(new CustomEvent("glossa:toggle-sidebar")); return; }
              onNav(item.id as Tab);
            }}
            style={{
              flex: 1, border: "none", background: "none",
              display: "flex", flexDirection: "column",
              alignItems: "center", justifyContent: "center",
              gap: 3, cursor: "pointer",
              color: isActive ? "#60a5fa" : "rgba(255,255,255,0.5)",
              fontSize: 10, fontWeight: isActive ? 700 : 400,
              padding: "4px 0 2px",
              borderTop: isActive ? "2px solid #3b82f6" : "2px solid transparent",
              transition: "color 0.15s, border-color 0.15s",
            }}
          >
            <span style={{ fontSize: 17, lineHeight: 1 }}>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        );
      })}
    </div>
  );
}

/**
 * Service chip (FR-007 / C081-3): identity + observation time, never a
 * bare dot — app, version, host, and when this was last checked.
 */
function ServiceChip({ onOpenStatus }: { onOpenStatus: () => void }) {
  const [health, setHealth] = useState<StatusResponse | null>(null);
  const [checkedAt, setCheckedAt] = useState<Date | null>(null);
  useEffect(() => {
    let cancelled = false;
    const check = () =>
      getStatus()
        .then((h) => { if (!cancelled) { setHealth(h); setCheckedAt(new Date()); } })
        .catch(() => { if (!cancelled) { setHealth(null); setCheckedAt(new Date()); } });
    check();
    const t = setInterval(check, 30000);
    return () => { cancelled = true; clearInterval(t); };
  }, []);
  return (
    <button
      onClick={onOpenStatus}
      title="Open Status — service identity and health"
      style={{
        display: "flex", alignItems: "center", gap: 8, padding: "5px 11px",
        border: "1px solid #e5e7eb", borderRadius: 20, fontSize: 11,
        color: "#64748b", background: "none", cursor: "pointer", whiteSpace: "nowrap",
      }}
    >
      <span style={{ width: 8, height: 8, borderRadius: "50%", background: health ? "#16a34a" : "#dc2626", flexShrink: 0 }} />
      <span>
        {health ? (
          <>
            <b style={{ color: "#111827", fontWeight: 600 }}>
              {health.app ?? "Glossa Lab"} v{health.version}
            </b>
            {" · "}{health.host ?? "this machine"}
            {" · checked "}{checkedAt ? fmtClock(checkedAt.toISOString()) : "—"}
          </>
        ) : (
          <>Backend not answering{checkedAt ? ` · checked ${fmtClock(checkedAt.toISOString())}` : ""}</>
        )}
      </span>
    </button>
  );
}

/** Program switcher card (Q1: sidebar card — names the program + its question). */
function ProgramSwitchCard({ onNavigate }: { onNavigate: (t: Tab) => void }) {
  const { activeProject, projects, setActiveProject } = useProject();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const h = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false); };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, [open]);

  const question = (activeProject?.question ?? "").trim() || activeProject?.description || "";

  return (
    <div ref={ref} style={{ position: "relative", padding: "0 12px", flexShrink: 0 }}>
      <button
        onClick={() => setOpen((v) => !v)}
        aria-label="Switch program"
        style={{
          margin: "12px 0 4px", padding: "9px 11px", borderRadius: 8, width: "100%",
          border: activeProject ? "1px solid rgba(96,165,250,.45)" : "1px dashed rgba(255,255,255,.25)",
          background: activeProject ? "rgba(37,99,235,.14)" : "rgba(255,255,255,.04)",
          color: "#dbeafe", display: "block", textAlign: "left", cursor: "pointer",
        }}
      >
        <div style={{ fontSize: 9, letterSpacing: 1, textTransform: "uppercase", color: "#93c5fd", fontWeight: 700 }}>
          Program
        </div>
        <div style={{ fontSize: 13, fontWeight: 700, color: activeProject ? "#fff" : "#a8c2e2", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 6 }}>
          <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {activeProject ? activeProject.label : "None open"}
          </span>
          <span>▾</span>
        </div>
        <div style={{ fontSize: 11, color: "#a8c2e2", marginTop: 2, lineHeight: 1.35 }}>
          {activeProject ? question : "Open a program to work in it, or start a new one."}
        </div>
      </button>

      {open && (
        <div style={{
          position: "absolute", top: "100%", left: 12, right: 12, zIndex: 300,
          background: "#1e293b", border: "1px solid rgba(255,255,255,0.12)",
          borderRadius: 8, boxShadow: "0 8px 24px rgba(0,0,0,0.4)",
          maxHeight: 300, overflowY: "auto", marginTop: 2,
        }}>
          <button
            onClick={() => { onNavigate("programs"); setOpen(false); }}
            style={{
              width: "100%", padding: "8px 12px", border: "none", background: "none",
              color: "rgba(255,255,255,0.75)", cursor: "pointer", textAlign: "left", fontSize: 11,
              borderBottom: "1px solid rgba(255,255,255,0.06)",
            }}
          >
            ▦ All programs (tool home)
          </button>
          {projects.map((proj) => {
            const sel = activeProject?.id === proj.id;
            return (
              <button key={proj.id}
                onClick={() => { void setActiveProject(proj.id); setOpen(false); onNavigate("home"); }}
                style={{
                  width: "100%", padding: "8px 12px", border: "none",
                  background: sel ? "rgba(37,99,235,0.15)" : "none",
                  color: sel ? "#93c5fd" : "rgba(255,255,255,0.6)",
                  cursor: "pointer", textAlign: "left", fontSize: 11,
                  fontWeight: sel ? 700 : 400,
                  borderBottom: "1px solid rgba(255,255,255,0.04)",
                  display: "block",
                }}
              >
                {proj.label}
              </button>
            );
          })}
          <button
            onClick={() => { onNavigate("builder"); setOpen(false); }}
            style={{
              width: "100%", padding: "7px 12px", border: "none",
              borderTop: "1px solid rgba(255,255,255,0.08)",
              background: "none", color: "rgba(255,255,255,0.4)",
              cursor: "pointer", textAlign: "left", fontSize: 10,
            }}
          >
            ⚙ Manage programs…
          </button>
        </div>
      )}
    </div>
  );
}

function AppContent() {
  const projCtx = useProject();
  const auth = useAuthState();
  const hasProgram = !!projCtx.activeProject;
  // The tool opens on the program list (wireframe 01) unless a deep
  // link (#/status from the tray, etc.) names a route.
  const [tab, _setTab] = useState<Tab>(() => initialTabFromHash());
  const tabRef = useRef<Tab>(tab);
  const initialTabRef = useRef<Tab>(tab);
  // The last hash this app itself wrote via replaceState. A current
  // hash that differs from it AND from the tab's target was set from
  // outside (deep link landing during boot) and is authoritative.
  const lastSyncedHashRef = useRef<string | null>(null);
  const [navHistory, setNavHistory] = useState<Tab[]>([]);
  const [navFuture, setNavFuture] = useState<Tab[]>([]);
  const userNavigatedRef = useRef(false);
  const hadHashAtLoadRef = useRef(window.location.hash.length > 1);

  const setTab = (v: Tab) => { tabRef.current = v; _setTab(v); };

  const goTo = (view: Tab) => {
    userNavigatedRef.current = true;
    // Evidence & sources sub-tab hint: the legacy notebooks /
    // citations / correspondence routes open the matching tab of the
    // consolidated surface (step 6).
    if (view === "notebooks" || view === "citations" || view === "correspondence") {
      try { sessionStorage.setItem("glossa_evidence_tab", view); } catch { /* */ }
    }
    const resolved = (resolveView(view, hasProgram) ?? view) as Tab;
    const cur = tabRef.current;
    if (cur !== resolved) {
      setNavHistory(prev => [...prev, cur].slice(-40));
      setNavFuture([]);
    }
    setTab(resolved);
  };
  const goBack = () => {
    userNavigatedRef.current = true;
    const cur = tabRef.current;
    setNavHistory(prev => {
      if (prev.length === 0) return prev;
      const dest = prev[prev.length - 1];
      setNavFuture(f => [cur, ...f].slice(0, 40));
      setTab(dest);
      return prev.slice(0, -1);
    });
  };
  const goForward = () => {
    userNavigatedRef.current = true;
    const cur = tabRef.current;
    setNavFuture(prev => {
      if (prev.length === 0) return prev;
      const dest = prev[0];
      setNavHistory(h => [...h, cur].slice(-40));
      setTab(dest);
      return prev.slice(1);
    });
  };
  const goHome = () => goTo(hasProgram ? "home" : "programs");

  // Keep the URL hash naming the route (the tray's "View status &
  // session log" opens /#/status — Spec 081 step 8).
  useEffect(() => {
    const target = `#/${tab}`;
    const current = window.location.hash;
    if (current === target) {
      lastSyncedHashRef.current = target;
      return;
    }
    // A hash naming another valid route that this app did not write
    // (a deep link or tray link that landed while the shell was still
    // booting, before the hashchange listener could catch it) wins
    // over the tab state — adopt it instead of clobbering it with the
    // sync write. Hashes the app itself wrote are told apart via
    // lastSyncedHashRef, so in-app navigation is unaffected.
    const m = current.match(/^#\/([a-z-]+)/);
    if (
      lastSyncedHashRef.current !== current &&
      m && VALID_TABS.has(m[1]) && m[1] !== tab
    ) {
      userNavigatedRef.current = true;
      setTab(m[1] as Tab);
      return;
    }
    window.history.replaceState(null, "", target);
    lastSyncedHashRef.current = target;
  }, [tab]);

  // Hash-driven navigation: a same-document hash change (deep link,
  // back/forward, tray link opened in an existing tab) switches the
  // route without a reload. replaceState in the sync effect above
  // does not fire hashchange, so this cannot loop.
  useEffect(() => {
    const onHash = () => {
      const m = window.location.hash.match(/^#\/([a-z-]+)/);
      if (m && VALID_TABS.has(m[1])) {
        userNavigatedRef.current = true;
        setTab(m[1] as Tab);
      }
    };
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  // Launch landing: with a program open and no deep link, land on the
  // program's home — the workbench opens where the work is. The tool
  // home (wireframe 01) stays one click away via Programs/switcher,
  // and is the landing whenever no program is open (wireframe 16).
  const landedRef = useRef(false);
  useEffect(() => {
    if (landedRef.current || userNavigatedRef.current) return;
    // A hash naming a non-default route is a deep link and wins. The
    // default route's own synced hash (#/programs) is NOT a deep
    // link: a reload that happens before the first landing completes
    // (or any return to the tool home's URL) must still land on the
    // open program's home.
    if (hadHashAtLoadRef.current && initialTabRef.current !== "programs") return;
    if (projCtx.loading) return;
    landedRef.current = true;
    if (projCtx.activeProject) setTab("home");
  }, [projCtx.loading, projCtx.activeProject]);

  const [darkMode, setDarkMode] = useState(() => localStorage.getItem("glossa_dark") === "1");
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [aiPanelOpen, setAiPanelOpen] = useState(false);
  const [aiPanelWidth, setAiPanelWidth] = useState(320);
  const [aiPanelSide, setAiPanelSide] = useState<"left" | "right">("left");
  const [isMobile, setIsMobile] = useState(() => window.innerWidth <= 768);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);
  useEffect(() => {
    const h = () => setSidebarOpen(v => !v);
    window.addEventListener("glossa:toggle-sidebar", h);
    return () => window.removeEventListener("glossa:toggle-sidebar", h);
  }, []);

  useEffect(() => {
    getOllamaContextConfig()
      .then(cfg => {
        const current = parseInt(localStorage.getItem("glossa_ollama_ctx") ?? "0", 10) || 0;
        if (cfg.session_ctx_length > current) {
          setLocalCtxLength(cfg.session_ctx_length);
        }
      })
      .catch(() => { /* Ollama not running — keep localStorage default */ });
  }, []);

  const [expDirty, setExpDirty] = useState(false);
  type RunState = { count: number; lastStatus: "none" | "success" | "fail" };
  const [expRunState, setExpRunState] = useState<RunState>({ count: 0, lastStatus: "none" });
  useEffect(() => {
    const hDirty = (e: Event) => {
      const { builder, dirty } = (e as CustomEvent<{ builder: string; dirty: boolean }>).detail;
      if (builder === "exp") setExpDirty(dirty);
    };
    const hRun = (e: Event) => {
      const d = (e as CustomEvent<{ builder: string; running: boolean; status?: string }>).detail;
      if (d.builder !== "exp") return;
      if (d.running) {
        setExpRunState(prev => ({ count: prev.count + 1, lastStatus: prev.lastStatus }));
      } else {
        const newStatus: RunState["lastStatus"] = d.status === "fail" ? "fail" : "success";
        setExpRunState(prev => ({ count: Math.max(0, prev.count - 1), lastStatus: newStatus }));
      }
    };
    window.addEventListener("glossa:dirty", hDirty);
    window.addEventListener("glossa:running", hRun);
    return () => {
      window.removeEventListener("glossa:dirty", hDirty);
      window.removeEventListener("glossa:running", hRun);
    };
  }, []);

  // Nav counts: active jobs (5 s poll, as before) + register counts
  // (60 s poll): claims total, claims waiting on a human (stage
  // checked/explained/accepted — the digestion queue), discovery inbox.
  const [activeJobCount, setActiveJobCount] = useState(0);
  const [claimsCount, setClaimsCount] = useState<number | undefined>(undefined);
  const [digestionCount, setDigestionCount] = useState<number | undefined>(undefined);
  const [discoveryCount, setDiscoveryCount] = useState<number | undefined>(undefined);
  useEffect(() => {
    let cancelled = false;
    const poll = () => {
      listJobs()
        .then((jobs) => {
          if (!cancelled) {
            setActiveJobCount(jobs.filter(
              (j) => j.status === "pending" || j.status === "running",
            ).length);
          }
        })
        .catch(() => { if (!cancelled) setActiveJobCount(0); });
    };
    poll();
    const t = setInterval(poll, 5000);
    return () => { cancelled = true; clearInterval(t); };
  }, []);
  useEffect(() => {
    let cancelled = false;
    const poll = () => {
      listIndusClaims({ limit: 500 })
        .then((r) => {
          if (cancelled) return;
          setClaimsCount(r.total);
          setDigestionCount(
            r.claims.filter((c) => {
              const s = effectiveStage(c);
              return s === "checked" || s === "explained" || s === "accepted";
            }).length,
          );
        })
        .catch(() => { /* counts are furniture; absence is honest */ });
      getDiscoveryStats("status")
        .then((r) => { if (!cancelled) setDiscoveryCount(r.counts["new"] ?? 0); })
        .catch(() => {});
    };
    poll();
    const t = setInterval(poll, 60000);
    return () => { cancelled = true; clearInterval(t); };
  }, []);

  // Spec 081 step 7 (Q8): the bottom panel is removed. Running work
  // lives on the Jobs screen; the session log lives on Status. The
  // AI assistant docks as a side panel only.

  useEffect(() => {
    document.body.style.background = darkMode ? "#0f172a" : "#fff";
    document.body.style.color = darkMode ? "#e2e8f0" : "#111827";
    localStorage.setItem("glossa_dark", darkMode ? "1" : "0");
  }, [darkMode]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") { e.preventDefault(); setPaletteOpen(p => !p); }
      if (e.altKey && e.key === "ArrowLeft") { e.preventDefault(); goBack(); }
      if (e.altKey && e.key === "ArrowRight") { e.preventDefault(); goForward(); }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const open = () => setAiPanelOpen(true);
    const close = () => setAiPanelOpen(false);
    const toggle = () => setAiPanelOpen((v) => !v);
    window.addEventListener("glossa:open-ai-panel", open);
    window.addEventListener("glossa:close-ai-panel", close);
    window.addEventListener("glossa:toggle-ai-panel", toggle);
    return () => {
      window.removeEventListener("glossa:open-ai-panel", open);
      window.removeEventListener("glossa:close-ai-panel", close);
      window.removeEventListener("glossa:toggle-ai-panel", toggle);
    };
  }, []);

  // AI-initiated navigation (open_view action) + in-app navigate events.
  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent<{ view: string; claimId?: string }>).detail;
      const raw = detail?.view;
      if (!raw) return;
      if (raw === "notebooks" || raw === "citations" || raw === "correspondence") {
        try { sessionStorage.setItem("glossa_evidence_tab", raw); } catch { /* */ }
      }
      const resolved = resolveView(raw, !!projCtx.activeProject) ?? (VALID_TABS.has(raw) ? (raw as Tab) : null);
      if (resolved) {
        goTo(resolved);
        if (detail.claimId) {
          window.dispatchEvent(new CustomEvent("glossa:open-claim", { detail: { claimId: detail.claimId } }));
        }
      }
    };
    window.addEventListener("glossa:navigate", handler);
    return () => window.removeEventListener("glossa:navigate", handler);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projCtx.activeProject]);

  const programItems: NavItem[] = [
    { id: "home", label: "Home", icon: "⌂" },
    { id: "claims", label: "Claims", icon: "§", count: claimsCount },
    { id: "digestion", label: "Digestion", icon: "✓", count: digestionCount, alert: !!digestionCount },
    { id: "evidence", label: "Evidence & sources", icon: "▤" },
    { id: "data", label: "Data", icon: "▦" },
    { id: "analysis", label: "Analysis", icon: "◈" },
    { id: "experiments", label: "Experiments", icon: "⬡" },
    { id: "discovery", label: "Discovery", icon: "◎", count: discoveryCount },
    { id: "loop", label: "Research loop", icon: "↻" },
    { id: "reports", label: "Reports & ledger", icon: "▨" },
  ];
  const toolItems: NavItem[] = [
    { id: "jobs", label: "Jobs", icon: "⚙", count: activeJobCount || undefined },
    { id: "status", label: "Status", icon: "♥" },
    { id: "settings", label: "Settings", icon: "⚙" },
    { id: "help", label: "Help", icon: "?" },
  ];
  const toolHomeItems: NavItem[] = [
    { id: "programs", label: "Programs", icon: "▦" },
    ...toolItems,
  ];

  const paletteTargets: NavItem[] = hasProgram
    ? [...programItems, ...toolItems, { id: "foundation-check", label: "Foundation Check", icon: "✅" }, { id: "ai-tools", label: "AI Tools", icon: "🔬" }]
    : [...toolHomeItems, { id: "ai-tools", label: "AI Tools", icon: "🔬" }];
  const paletteCommands: PaletteCommand[] = [
    ...paletteTargets.map((t) => ({
      id: t.id, label: `Go to ${t.label}`, description: `Open ${t.label}`, icon: t.icon,
      action: () => goTo(t.id),
    })),
    { id: "dark-mode", label: "Toggle Dark Mode", icon: darkMode ? "☀️" : "🌙", action: () => setDarkMode(d => !d) },
  ];

  const bg = darkMode ? "#0f172a" : "#f8fafc";
  const sideBg = darkMode ? "#0d1526" : "#1e3a5f";
  const sideText = "#c7d8f0";
  const sideHdr = "#7a9bbf";
  const activeBg = darkMode ? "rgba(37,99,235,0.25)" : "rgba(96,165,250,0.22)";
  const fg = darkMode ? "#e2e8f0" : "#111827";
  const border = darkMode ? "#334155" : "#e5e7eb";
  const cardBg = darkMode ? "#1e293b" : "#fff";
  const muted = darkMode ? "#94a3b8" : "#6b7280";

  const currentLabel = TAB_LABELS[tab] ?? tab;
  const isToolView = (["jobs", "status", "settings", "help", "ai-tools"] as Tab[]).includes(tab);
  const crumbMiddle = tab === "programs" ? null : isToolView ? "Tool" : (projCtx.activeProject?.label ?? "Tool");

  const NavBtn = ({ item }: { item: NavItem }) => {
    const active = tab === item.id
      || (item.id === "analysis" && (tab === "entropy" || tab === "signs" || tab === "timeline"));
    const dirty = item.id === "experiments" && expDirty;
    const running = item.id === "experiments" && expRunState.count > 0;
    return (
      <button
        onClick={() => { goTo(item.id); if (isMobile) setSidebarOpen(false); }}
        title={item.label + (dirty ? " (unsaved changes)" : "")}
        style={{
          display: "flex", alignItems: "center", gap: 9,
          width: "100%", padding: "7px 16px",
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
        <span style={{ fontSize: 14, width: 18, textAlign: "center", lineHeight: 1, flexShrink: 0 }}>{item.icon}</span>
        <span style={{ flex: 1 }}>{item.label}</span>
        {dirty && !running && (
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#f59e0b", flexShrink: 0, boxShadow: "0 0 4px #f59e0b" }} title="Unsaved changes" />
        )}
        {running && (
          <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#22c55e", flexShrink: 0, boxShadow: "0 0 6px #22c55e", animation: "healthPulse 0.7s ease-in-out infinite" }} title="Running" />
        )}
        {item.count !== undefined && item.count > 0 && (
          <span style={{
            fontSize: 10, fontWeight: 700, padding: "1px 6px", borderRadius: 8,
            background: item.alert ? "#b45309" : "rgba(255,255,255,.14)",
            color: item.alert ? "#fff" : "#dbeafe", flexShrink: 0,
          }}>
            {item.count}
          </span>
        )}
      </button>
    );
  };

  const NavSection = ({ title, items }: { title: string; items: NavItem[] }) => (
    <div style={{ marginBottom: 4 }}>
      <div style={{
        padding: "10px 16px 4px", fontSize: 10, fontWeight: 700,
        color: sideHdr, textTransform: "uppercase", letterSpacing: 1,
      }}>
        {title}
      </div>
      {items.map((item) => <NavBtn key={item.id} item={item} />)}
    </div>
  );

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden", fontFamily: "system-ui, sans-serif", background: bg, userSelect: "none" }}>

      {isMobile && sidebarOpen && (
        <div
          onClick={() => setSidebarOpen(false)}
          style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", zIndex: 199 }}
        />
      )}

      <aside style={{
        position: "fixed", top: 0, left: 0, bottom: 0,
        width: SIDEBAR_W,
        background: sideBg,
        display: "flex", flexDirection: "column",
        overflow: "hidden",
        zIndex: 200,
        boxShadow: "2px 0 8px rgba(0,0,0,0.15)",
        transform: isMobile && !sidebarOpen ? `translateX(-${SIDEBAR_W}px)` : "translateX(0)",
        transition: "transform 0.2s ease",
      }}>
        {/* Brand block — the tool's name, no program's subject (C081-1) */}
        <div style={{ padding: "16px 16px 10px", borderBottom: "1px solid rgba(255,255,255,0.08)", flexShrink: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 9 }}>
            <div style={{ width: 30, height: 30, borderRadius: 7, background: "linear-gradient(135deg,#2563eb,#60a5fa)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 14, flexShrink: 0 }}>G</div>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#fff", lineHeight: 1.2 }}>Glossa Lab</div>
              <div style={{ fontSize: 10, color: sideHdr, lineHeight: 1.4 }}>Epistemic research workbench</div>
            </div>
          </div>
        </div>

        <ProgramSwitchCard onNavigate={goTo} />

        <div style={{ flex: 1, overflowY: "auto", paddingTop: 2, paddingBottom: 6 }}>
          {hasProgram ? (
            <>
              <NavSection title="Program" items={programItems} />
              <div style={{ borderTop: "1px solid rgba(255,255,255,0.08)", marginTop: 6, paddingTop: 2 }}>
                <NavSection title="Tool" items={toolItems} />
              </div>
            </>
          ) : (
            <NavSection title="Tool home" items={toolHomeItems} />
          )}
        </div>
      </aside>

      <div style={{
        marginLeft: isMobile ? 0 : SIDEBAR_W + (aiPanelOpen && aiPanelSide === "left" ? aiPanelWidth : 0),
        marginRight: !isMobile && aiPanelOpen && aiPanelSide === "right" ? aiPanelWidth : 0,
        flex: 1, minWidth: 0,
        display: "flex", flexDirection: "column",
        height: "100vh",
        overflow: "hidden",
        transition: "margin 0.15s",
      }}>
        {/* Top bar */}
        <div style={{
          display: "flex", alignItems: "center", gap: 8,
          padding: isMobile ? "8px 12px" : "10px 24px",
          borderBottom: `1px solid ${border}`,
          background: cardBg,
          flexShrink: 0,
          position: "sticky", top: 0, zIndex: 100,
        }}>
          {isMobile && (
            <button
              onClick={() => setSidebarOpen(v => !v)}
              aria-label="Toggle navigation"
              style={{ padding: "4px 6px", border: "none", background: "none",
                cursor: "pointer", fontSize: 20, color: fg, lineHeight: 1, flexShrink: 0 }}
            >
              {sidebarOpen ? "✕" : "☰"}
            </button>
          )}
          {!isMobile && <span style={{ fontSize: 13, color: muted }}>Glossa Lab</span>}
          {!isMobile && crumbMiddle && (
            <>
              <span style={{ color: border, fontSize: 13 }}>/</span>
              <span style={{ fontSize: 13, fontWeight: crumbMiddle !== "Tool" ? 600 : 400, color: crumbMiddle !== "Tool" ? fg : muted }}>
                {crumbMiddle}
              </span>
            </>
          )}
          {!isMobile && <span style={{ color: border, fontSize: 13 }}>/</span>}
          <span style={{ fontSize: isMobile ? 15 : 13, fontWeight: 600, color: fg }}>{currentLabel}</span>

          <div style={{ flex: 1 }} />

          {!isMobile && (
            <div style={{ display: "flex", gap: 2, marginRight: 4 }}>
              <button
                onClick={goBack}
                disabled={navHistory.length === 0}
                title={navHistory.length > 0 ? "Back (Alt+←)" : "No history"}
                style={{
                  padding: "4px 8px", border: `1px solid ${border}`, borderRadius: 6,
                  background: "none", cursor: navHistory.length > 0 ? "pointer" : "default",
                  fontSize: 13, color: navHistory.length > 0 ? fg : (darkMode ? "#475569" : "#d1d5db"),
                  lineHeight: 1,
                }}
              >←</button>
              <button
                onClick={goForward}
                disabled={navFuture.length === 0}
                title={navFuture.length > 0 ? "Forward (Alt+→)" : "No forward history"}
                style={{
                  padding: "4px 8px", border: `1px solid ${border}`, borderRadius: 6,
                  background: "none", cursor: navFuture.length > 0 ? "pointer" : "default",
                  fontSize: 13, color: navFuture.length > 0 ? fg : (darkMode ? "#475569" : "#d1d5db"),
                  lineHeight: 1,
                }}
              >→</button>
              <button
                onClick={goHome}
                title={hasProgram ? "Program home" : "Programs"}
                style={{
                  padding: "4px 8px", border: `1px solid ${border}`, borderRadius: 6,
                  background: (tab === "home" || tab === "programs") ? (darkMode ? "rgba(37,99,235,0.18)" : "#eff6ff") : "none",
                  cursor: "pointer", fontSize: 13,
                  color: (tab === "home" || tab === "programs") ? "#2563eb" : fg,
                  lineHeight: 1,
                }}
              >⌂</button>
            </div>
          )}

          {!isMobile && (
            <button
              onClick={() => setPaletteOpen(true)}
              title="Command palette (Cmd+K)"
              style={{ padding: "4px 10px", border: `1px solid ${border}`, borderRadius: 6, background: "none", cursor: "pointer", fontSize: 12, color: muted }}
            >
              ⌘K&nbsp; Search
            </button>
          )}
          {!isMobile && (
            <button
              onClick={() => setAiPanelOpen(o => !o)}
              title={aiPanelOpen ? "Close AI assistant" : "Open AI assistant"}
              style={{ padding: "4px 10px", border: `1px solid ${aiPanelOpen ? "rgba(124,58,237,0.5)" : border}`, borderRadius: 6, background: "none", cursor: "pointer", fontSize: 12, color: aiPanelOpen ? "#7c3aed" : muted }}
            >
              ✦ AI assistant
            </button>
          )}
          {!isMobile && <ServiceChip onOpenStatus={() => goTo("status")} />}
          <NotificationCenter />
          <button
            onClick={() => setDarkMode((d) => !d)}
            title="Toggle dark mode"
            style={{ padding: "4px 8px", border: `1px solid ${border}`, borderRadius: 6, background: "none", cursor: "pointer", fontSize: 14 }}
          >
            {darkMode ? "☀️" : "🌙"}
          </button>
        </div>

        {(() => {
          const isCanvas = tab === "experiments";
          const mobileBottomPad = isMobile ? MOBILE_NAV_H + 8 : 0;
          return (
            <main style={{
              flex: 1,
              minHeight: 0,
              display: "flex", flexDirection: "column",
              padding: isCanvas ? 0 : (isMobile ? "12px" : "24px"),
              paddingBottom: isCanvas ? mobileBottomPad : (isMobile ? mobileBottomPad + 8 : 32),
              color: fg,
              maxWidth: "none",
              overflow: isCanvas ? "hidden" : "auto",
              userSelect: "text",
            }}>
              {auth.tokenNeeded && tab !== "settings" ? (
                <ApiTokenGate darkMode={darkMode} />
              ) : (
                <>
                  {tab === "programs" && <ProgramsView darkMode={darkMode} onNavigate={(v) => goTo(v as Tab)} />}
                  {tab === "home" && <ProgramHome darkMode={darkMode} onNavigate={(v) => goTo(v as Tab)} />}
                  {tab === "claims" && <ClaimsView darkMode={darkMode} onNavigate={(v) => goTo(v as Tab)} />}
                  {tab === "digestion" && <DigestionBoard darkMode={darkMode} onNavigate={(v) => goTo(v as Tab)} />}
                  {tab === "evidence" && <EvidenceSourcesView darkMode={darkMode} />}
                  {tab === "data" && <DataView darkMode={darkMode} />}
                  {(tab === "analysis" || tab === "entropy" || tab === "signs" || tab === "timeline") && (
                    <AnalysisView
                      key={tab}
                      darkMode={darkMode}
                      initialTab={tab === "signs" ? "signs" : tab === "timeline" ? "timeline" : "entropy"}
                      onNavigate={(v) => goTo(v as Tab)}
                    />
                  )}
                  {tab === "experiments" && <ExperimentBuilderView darkMode={darkMode} />}
                  {tab === "discovery" && <DiscoveryView />}
                  {tab === "loop" && (
                    <div style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
                      <ResearchLoopPanel />
                      <SweepPanel darkMode={darkMode} />
                    </div>
                  )}
                  {tab === "reports" && <ReportsView darkMode={darkMode} />}
                  {tab === "jobs" && <JobsView />}
                  {tab === "status" && <StatusView />}
                  {tab === "settings" && <SettingsView darkMode={darkMode} />}
                  {tab === "help" && <HelpView />}
                  {tab === "foundation-check" && <FoundationCheckView />}
                  {tab === "ai-tools" && <AIToolsView />}
                  {tab === "builder" && <ProjectsView />}
                </>
              )}
            </main>
          );
        })()}
      </div>

      {paletteOpen && <CommandPalette commands={paletteCommands} onClose={() => setPaletteOpen(false)} />}

      {aiPanelOpen && (
        <AISidePanel
          onClose={() => setAiPanelOpen(false)}
          leftOffset={SIDEBAR_W}
          bottomOffset={0}
          initialSide={aiPanelSide}
          initialWidth={aiPanelWidth}
          onWidthChange={setAiPanelWidth}
          onSideChange={setAiPanelSide}
          isMobile={isMobile}
        />
      )}

      {isMobile && (
        <MobileNavBar
          active={tab}
          onNav={goTo}
          hasProgram={hasProgram}
        />
      )}

      <style>{`
        @keyframes healthPulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        aside::-webkit-scrollbar { width: 4px; }
        aside::-webkit-scrollbar-track { background: transparent; }
        aside::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 2px; }
        aside button:hover { background: rgba(255,255,255,0.08) !important; }
        @supports (padding-bottom: env(safe-area-inset-bottom)) {
          .glossa-bottom-panel { padding-bottom: env(safe-area-inset-bottom); }
        }
        button { touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
        @media (max-width: 768px) {
          button { min-height: 44px; }
          input, select, textarea { font-size: 16px !important; }
          .glossa-card { padding: 10px 12px !important; }
          body { font-size: 14px; }
        }
        main { -webkit-overflow-scrolling: touch; }
        .mobile-nav-btn { touch-action: manipulation; }
      `}</style>
    </div>
  );
}

export function App() {
  return (
    <ToastProvider>
      <AIChatProvider>
        <ProjectProvider>
          <AppContent />
        </ProjectProvider>
      </AIChatProvider>
    </ToastProvider>
  );
}
