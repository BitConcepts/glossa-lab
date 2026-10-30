import { useEffect, useRef, useState, type ReactNode } from "react";
import {
  clearCache, clearLocalCache,
  getEnvPackages,
  getEnvStatus,
  getFoundationStatus,
  getHealth,
  getLoopSchedulerStatus,
  getSettings,
  runEnvRebuild, runEnvSetup, runEnvUpgrade,
  setLoopSchedulerEnabled,
  updateFoundationConfig,
  type EnvPackage, type EnvStatus, type FoundationStatus, type LoopSchedulerStatus,
} from "../api";
import { useProject } from "../hooks/useProject";
import { useToast } from "../hooks/useToast";
import { ApiTokenField } from "./ApiToken";
import { NotificationsPanel } from "./Notifications/NotificationsPanel";
import { AutoDiscoveryPanel } from "./Settings/AutoDiscoveryPanel";
import { ProvidersPanel } from "./Settings/ProvidersPanel";
import { ModelAssignmentsPanel } from "./Settings/ModelAssignmentsPanel";
import { ModelHubPanel } from "./Settings/ModelHubPanel";
import { fmtDayTime, humanizeUptime } from "./ui081";

// Discovery key labels moved to AutoDiscoveryPanel.

// ── Python Environment Section ─────────────────────────────────────────────

function PythonEnvSection() {
  const { toast } = useToast();
  const [status, setStatus] = useState<EnvStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [output, setOutput] = useState<{ text: string; type: string }[]>([]);
  const [packages, setPackages] = useState<EnvPackage[] | null>(null);
  const [outputOpen, setOutputOpen] = useState(true);
  const [packagesOpen, setPackagesOpen] = useState(true);
  // ref points to the scrollable output container, NOT a sentinel inside it
  const outputContainerRef = useRef<HTMLDivElement>(null);

  const refresh = async () => {
    setLoading(true);
    try { setStatus(await getEnvStatus()); } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  useEffect(() => { refresh(); }, []);
  // Scroll the output container itself — never scroll the page
  useEffect(() => {
    const el = outputContainerRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [output]);

  const runStream = async (fetcher: () => Promise<Response>, label: string) => {
    setRunning(true);
    setOutput([{ text: `Running: ${label}…`, type: "info" }]);
    try {
      const resp = await fetcher();
      if (!resp.body) { setOutput(o => [...o, { text: "No response body", type: "error" }]); return; }
      const reader = resp.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const parts = buf.split("\n\n"); buf = parts.pop() ?? "";
        for (const part of parts) {
          for (const ln of part.split("\n")) {
            if (ln.startsWith("data: ")) {
              try {
                const d = JSON.parse(ln.slice(6)) as { text?: string };
                if (d.text) {
                  const isErr = d.text.toLowerCase().includes("error") || d.text.startsWith("⚠");
                  const isDone = d.text.startsWith("✓");
                  setOutput(o => [...o, { text: d.text!, type: isErr ? "error" : isDone ? "success" : "output" }]);
                }
              } catch { /* ignore */ }
            } else if (ln.startsWith("event: done") || ln.startsWith("event: error")) {
              // handled via data
            }
          }
        }
      }
      await refresh();
      toast(`${label} complete`, "success");
    } catch (e) {
      setOutput(o => [...o, { text: `Failed: ${e instanceof Error ? e.message : String(e)}`, type: "error" }]);
      toast(`${label} failed`, "error");
    } finally {
      setRunning(false);
    }
  };

  // Show-packages is a *toggle*: first click fetches + shows; second click
  // hides the list without re-fetching; a third click re-shows the cached
  // list immediately, with the latest counts updated only on the first click
  // of each session.
  const togglePackages = async () => {
    if (packages !== null) {
      // Already loaded — toggle visibility without re-fetching.
      setPackages(null);
      return;
    }
    const r = await getEnvPackages();
    setPackages(r.packages);
    // Default the inner accordion to "open" when first revealed so the user
    // sees the list immediately rather than just a header.
    setPackagesOpen(true);
  };

  const active = status?.venv_exists;
  const dotColor = loading ? "#9ca3af" : active ? "#16a34a" : "#ef4444";
  const dotLabel = loading ? "checking…" : active ? `Active \u00b7 Python ${status?.python_version ?? "?"}` : "Not found";

  const btnSt = (color: string, disabled: boolean): React.CSSProperties => ({
    padding: "5px 12px", border: "none", borderRadius: 5,
    background: disabled ? "#e5e7eb" : color, color: disabled ? "#9ca3af" : "#fff",
    cursor: disabled ? "not-allowed" : "pointer", fontSize: 12, fontWeight: 600,
  });

  return (
    <section style={ollamaSection}>
      <h3 style={{ margin: "0 0 10px", fontSize: 15, fontWeight: 600, color: "#111827" }}>🐍 Python Environment</h3>

      {/* Status row */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12, padding: "10px 14px",
        background: active ? "#f0fdf4" : "#fef2f2",
        border: `1px solid ${active ? "#86efac" : "#fca5a5"}`, borderRadius: 7 }}>
        <span style={{ width: 9, height: 9, borderRadius: "50%", background: dotColor, flexShrink: 0 }} />
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#111827" }}>{dotLabel}</div>
          {status?.venv_path && <div style={{ fontSize: 10, color: "#6b7280", fontFamily: "monospace", marginTop: 1 }}>{status.venv_path}</div>}
          {active && <div style={{ fontSize: 11, color: "#6b7280", marginTop: 2 }}>{status?.pkg_count ?? 0} packages installed</div>}
        </div>
        <button onClick={refresh} style={{ padding: "3px 8px", border: "1px solid #d1d5db", borderRadius: 4, background: "#fff", cursor: "pointer", fontSize: 11, color: "#6b7280" }}>⟳</button>
      </div>

      {/* Warning if no venv */}
      {!active && !loading && (
        <div style={{ padding: "12px 14px", background: "#fef3c7", border: "1px solid #fcd34d", borderRadius: 6, marginBottom: 12, fontSize: 12, color: "#92400e" }}>
          No virtual environment found. Click <strong>Setup venv</strong> to create one and install all dependencies.
        </div>
      )}

      {/* Action buttons */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
        <button onClick={() => runStream(runEnvSetup, "Setup venv")} disabled={running}
          style={btnSt("#16a34a", running)}>
          ⬇ Setup venv
        </button>
        <button onClick={() => runStream(runEnvRebuild, "Rebuild venv")} disabled={running}
          style={btnSt("#ea580c", running)}>
          ↺ Rebuild venv
        </button>
        <button onClick={() => runStream(runEnvUpgrade, "Upgrade deps")} disabled={running || !active}
          style={btnSt("#2563eb", running || !active)}>
          ↑ Upgrade deps
        </button>
        <button onClick={togglePackages} disabled={!active}
          style={btnSt("#7c3aed", !active)}
          title={packages !== null
            ? "Hide the package list (does not uninstall anything)"
            : "Fetch and show installed packages"}>
          {packages !== null ? "📦 Hide packages" : "📦 Show packages"}
        </button>
      </div>

      {/* Output stream — collapsible */}
      {output.length > 0 && (
        <div style={{ marginBottom: 10 }}>
          <button
            onClick={() => setOutputOpen(o => !o)}
            style={{ display: "flex", alignItems: "center", gap: 5, background: "none",
              border: "none", cursor: "pointer", padding: "2px 0", marginBottom: 4,
              fontSize: 11, fontWeight: 700, color: "#374151", textTransform: "uppercase", letterSpacing: 0.5 }}
          >
            <span style={{ fontSize: 9, transition: "transform .15s", transform: outputOpen ? "rotate(90deg)" : "rotate(0deg)" }}>▶</span>
            Install output
          </button>
          {outputOpen && (
            /* ref is on THIS div so scrollTop affects only this container */
            <div ref={outputContainerRef}
              style={{ background: "#0f172a", borderRadius: 5, padding: "8px 10px",
                maxHeight: 200, overflowY: "auto", fontFamily: "monospace", fontSize: 11 }}>
              {output.map((l, i) => (
                <div key={i} style={{ color: l.type === "error" ? "#f87171" : l.type === "success" ? "#86efac" : "#e2e8f0", lineHeight: 1.6 }}>{l.text}</div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Package list — collapsible */}
      {packages && (
        <div>
          <button
            onClick={() => setPackagesOpen(o => !o)}
            style={{ display: "flex", alignItems: "center", gap: 5, background: "none",
              border: "none", cursor: "pointer", padding: "2px 0", marginBottom: 4,
              fontSize: 11, fontWeight: 700, color: "#374151", textTransform: "uppercase", letterSpacing: 0.5 }}
          >
            <span style={{ fontSize: 9, transition: "transform .15s", transform: packagesOpen ? "rotate(90deg)" : "rotate(0deg)" }}>▶</span>
            Installed packages ({packages.length})
          </button>
          {packagesOpen && (
            <div style={{ display: "flex", flexWrap: "wrap", gap: "2px 8px", maxHeight: 140, overflowY: "auto" }}>
              {packages.map(p => (
                <span key={p.name} style={{ fontSize: 10, fontFamily: "monospace", color: "#374151" }}>
                  {p.name} <span style={{ color: "#9ca3af" }}>{p.version}</span>
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
}

// ── Grouped settings layout (Spec 081 step 7, wireframe 13) ─────────────
//
// Two kinds of settings, never mixed: the TOOL's (this install, this
// machine) and the open PROGRAM's (its question, its sources, its
// loop schedule, its foundation gate). A program setting changed
// here changes it for the program everywhere; a tool setting never
// touches a program's record.

function GroupTitle({ children }: { children: ReactNode }) {
  return (
    <h3 style={{
      margin: "26px 0 4px", fontSize: 12, fontWeight: 700, color: "#2563eb",
      textTransform: "uppercase", letterSpacing: 0.8,
    }}>
      {children}
    </h3>
  );
}

function SettingRow({ name, state, children }: {
  name: string;
  state?: ReactNode;
  children?: ReactNode;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ borderBottom: "1px solid #eef1f5", padding: "10px 0" }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" }}>
        <span style={{ fontSize: 13, fontWeight: 600, color: "#111827", minWidth: 170 }}>{name}</span>
        <span style={{ fontSize: 12, color: "#6b7280", flex: "1 1 260px" }}>{state}</span>
        {children && (
          <button
            onClick={() => setOpen((v) => !v)}
            style={{
              padding: "4px 12px", border: "1px solid #e5e7eb", borderRadius: 6,
              background: "#fff", cursor: "pointer", fontSize: 12, color: "#374151",
            }}
          >
            {open ? "Hide" : "Manage"}
          </button>
        )}
      </div>
      {open && children && <div style={{ marginTop: 12 }}>{children}</div>}
    </div>
  );
}

// ── Main SettingsView ─────────────────────────────────────────────────────

export function SettingsView({ darkMode = true }: { darkMode?: boolean }) {
  const { activeProject } = useProject();
  const [dataDir, setDataDir] = useState("");
  const [backendVersion, setBackendVersion] = useState("");
  const [backendUptime, setBackendUptime] = useState("");
  const [scheduler, setScheduler] = useState<LoopSchedulerStatus | null>(null);
  const [schedulerBusy, setSchedulerBusy] = useState(false);
  const [foundation, setFoundation] = useState<FoundationStatus | null>(null);

  const load = async () => {
    try {
      const [s, h] = await Promise.all([getSettings(), getHealth()]);
      setDataDir(s.data_dir);
      setBackendVersion(h.version ?? "");
      setBackendUptime(humanizeUptime(h.uptime_seconds ?? 0));
    } catch {
      // Backend might not be available; the token field still works.
    }
    getLoopSchedulerStatus().then(setScheduler).catch(() => {});
    getFoundationStatus().then(setFoundation).catch(() => {});
  };

  useEffect(() => { void load(); }, []);

  const toggleScheduler = async () => {
    if (!scheduler) return;
    setSchedulerBusy(true);
    try {
      await setLoopSchedulerEnabled(!scheduler.enabled);
      setScheduler(await getLoopSchedulerStatus());
    } catch { /* state stays as read */ }
    finally { setSchedulerBusy(false); }
  };

  const toggleFoundationAuto = async () => {
    if (!foundation) return;
    try {
      await updateFoundationConfig({ auto_check_enabled: !foundation.auto_check_enabled });
      setFoundation(await getFoundationStatus());
    } catch { /* state stays as read */ }
  };

  const servedPort = window.location.port || (window.location.protocol === "https:" ? "443" : "80");
  const programName = activeProject?.label ?? "No program open";
  const question = (activeProject?.question ?? "").trim();

  return (
    <div style={{ maxWidth: 860 }}>
      <h2 style={{ marginTop: 0, marginBottom: 6 }}>Settings</h2>
      <p style={{ ...hintTextStyle, maxWidth: "68ch", marginBottom: 4 }}>
        Two kinds of settings live here and are never mixed: the tool's — this
        install, on this machine — and the open program's. Changing a program
        setting changes it for the program everywhere it is opened.
      </p>

      {/* ═══ TOOL — SERVICE ═══ */}
      <GroupTitle>Tool — service</GroupTitle>

      <SettingRow name="API token" state="The credential this app sends the backend (Spec 082)">
        <ApiTokenField darkMode={darkMode} />
      </SettingRow>

      <SettingRow
        name="Port"
        state={<>This page was served on port {servedPort}. The tray's Change Port writes the same service setting — two doors, one setting.</>}
      />
      <SettingRow
        name="Data folder"
        state={dataDir
          ? <span style={{ fontFamily: "monospace", fontSize: 12 }}>{dataDir}</span>
          : "Not read — the backend has not answered yet."}
      />
      <SettingRow
        name="Backend"
        state={backendVersion
          ? <>v{backendVersion} · up {backendUptime}</>
          : "Not read — the backend has not answered yet."}
      />
      <SettingRow
        name="Start at sign-in"
        state="On the desktop install the service starts at sign-in (the GlossaLab task owns this). It is stated here, not changed here — the tray is the door for it."
      />

      {/* ═══ TOOL — ENVIRONMENT & AI ═══ */}
      <GroupTitle>Tool — environment &amp; AI</GroupTitle>

      <SettingRow name="AI providers" state="Which providers this install can call, and their keys">
        <ProvidersPanel />
      </SettingRow>
      <SettingRow name="Model assignments" state="Which model does which job in this install">
        <ModelAssignmentsPanel />
      </SettingRow>
      <SettingRow name="Model hub" state="Local models available to this install">
        <ModelHubPanel />
      </SettingRow>
      <SettingRow name="AI behavior" state="How the assistant's action proposals are approved">
        <AutoApproveSetting />
      </SettingRow>
      <SettingRow name="Python environment" state="The backend's virtual environment on this machine">
        <PythonEnvSection />
      </SettingRow>
      <SettingRow name="Notifications" state="What this install sends, and where">
        <NotificationsPanel />
      </SettingRow>
      <SettingRow name="Cache" state="Clearing run state stored by this install">
        <JobCacheSection />
      </SettingRow>

      {/* ═══ PROGRAM ═══ */}
      <GroupTitle>Program — {programName}</GroupTitle>

      {!activeProject && (
        <p style={{ ...hintTextStyle, marginTop: 8 }}>
          No program is open, so there are no program settings to show. Open a
          program and its question, sources, loop schedule and foundation gate
          appear here.
        </p>
      )}

      {activeProject && (
        <>
          <SettingRow
            name="The question"
            state={question || "Not stated yet — the program has no question on its record."}
          >
            <div>
              <p style={hintTextStyle}>
                The question is part of the program's record and is edited
                with the program itself.
              </p>
              <button
                onClick={() => window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "builder" } }))}
                style={{
                  marginTop: 8, padding: "5px 12px", border: "1px solid #e5e7eb", borderRadius: 6,
                  background: "#fff", cursor: "pointer", fontSize: 12, color: "#374151",
                }}
              >
                Edit in Manage programs
              </button>
            </div>
          </SettingRow>

          <SettingRow
            name="Discovery sources"
            state="Where this program's discovery looks for new material"
          >
            <AutoDiscoveryPanel />
          </SettingRow>

          <SettingRow
            name="Research-loop schedule"
            state={scheduler
              ? scheduler.enabled
                ? <>On — runs every {scheduler.interval_hours ?? "—"} h, {scheduler.iterations ?? "—"} iterations a run</>
                : "Off — the loop runs only when started by hand"
              : "Not read — the backend has not answered yet."}
          >
            <div>
              <p style={hintTextStyle}>
                The schedule belongs to the program: when it is on, the loop
                runs on its interval whether or not anyone is watching. The
                loop surface shows the same state and links back here.
              </p>
              <button
                onClick={() => void toggleScheduler()}
                disabled={!scheduler || schedulerBusy}
                style={{
                  marginTop: 8, padding: "5px 12px", border: "1px solid #e5e7eb", borderRadius: 6,
                  background: "#fff", cursor: scheduler ? "pointer" : "default", fontSize: 12, color: "#374151",
                }}
              >
                {schedulerBusy ? "…" : scheduler?.enabled ? "Turn schedule off" : "Turn schedule on"}
              </button>
            </div>
          </SettingRow>

          <SettingRow
            name="Foundation-check gate"
            state={foundation
              ? <>Last verdict: {foundation.verdict ?? "not run yet"} · automatic check {foundation.auto_check_enabled ? "on" : "off"}{foundation.last_checked_at ? ` · checked ${fmtDayTime(foundation.last_checked_at)}` : ""}</>
              : "Not read — the backend has not answered yet."}
          >
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <button
                onClick={() => window.dispatchEvent(new CustomEvent("glossa:navigate", { detail: { view: "foundation-check" } }))}
                style={{
                  padding: "5px 12px", border: "1px solid #e5e7eb", borderRadius: 6,
                  background: "#fff", cursor: "pointer", fontSize: 12, color: "#374151",
                }}
              >
                Open foundation check
              </button>
              <button
                onClick={() => void toggleFoundationAuto()}
                disabled={!foundation}
                style={{
                  padding: "5px 12px", border: "1px solid #e5e7eb", borderRadius: 6,
                  background: "#fff", cursor: foundation ? "pointer" : "default", fontSize: 12, color: "#374151",
                }}
              >
                {foundation?.auto_check_enabled ? "Turn automatic check off" : "Turn automatic check on"}
              </button>
            </div>
          </SettingRow>
        </>
      )}
    </div>
  );
}

// ── Job Cache section ────────────────────────────────────────────────────────────

function JobCacheSection() {
  const { toast } = useToast();
  const [clearing, setClearing] = useState(false);

  const handleClear = async () => {
    setClearing(true);
    try {
      const result = await clearCache();
      clearLocalCache();
      // Tell listeners to re-read the now-empty seq queue from localStorage
      window.dispatchEvent(new CustomEvent("glossa:seq_queue_updated"));
      toast(`${result.cleared_jobs} job(s) cleared — cache reset`, "success");
    } catch (e) {
      toast(e instanceof Error ? e.message : "Clear failed", "error");
    } finally {
      setClearing(false);
    }
  };

  return (
    <section style={sectionStyle}>
      <h3 style={sectionTitleStyle}>🗑 Clear Cache</h3>
      <p style={hintTextStyle}>
        Removes all non-running jobs from the database (completed, failed, paused, queued)
        and clears all run-related browser state:
      </p>
      <ul style={{ ...hintTextStyle, margin: "6px 0 0 16px", padding: 0 }}>
        <li>Experiment run badges (✓/✗) in the Builder</li>
        <li>Sequential run queue</li>
        <li>Dashboard AI insight + applied action state</li>
      </ul>
      <p style={{ ...hintTextStyle, marginTop: 8, color: "#9ca3af" }}>
        <strong>Running jobs are never affected.</strong> Use this before re-running
        experiments to start completely clean.
      </p>
      <button
        onClick={handleClear}
        disabled={clearing}
        style={{
          marginTop: 12, padding: "6px 16px", border: "none", borderRadius: 5,
          background: clearing ? "#e5e7eb" : "#b45309",
          color: clearing ? "#9ca3af" : "#fff",
          cursor: clearing ? "not-allowed" : "pointer",
          fontSize: 13, fontWeight: 600,
        }}>
        {clearing ? "Clearing…" : "🗑 Clear Cache"}
      </button>
    </section>
  );
}

// ── Auto-approve setting ─────────────────────────────────────────────────────────

const AUTO_APPROVE_KEY = "glossa_auto_approve";

function AutoApproveSetting() {
  const { toast } = useToast();
  const [enabled, setEnabled] = useState(() => localStorage.getItem(AUTO_APPROVE_KEY) === "true");

  const toggle = (v: boolean) => {
    setEnabled(v);
    localStorage.setItem(AUTO_APPROVE_KEY, v ? "true" : "false");
    // Notify any open AIChatWindow instances
    window.dispatchEvent(new CustomEvent("glossa:auto_approve_changed"));
    toast(v ? "Auto-approve enabled — Glossa AI will run all actions automatically" : "Auto-approve disabled", v ? "success" : "info");
  };

  return (
    <div style={{ marginTop: 12 }}>
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "12px 14px", borderRadius: 7,
        border: `1px solid ${enabled ? "#fbbf24" : "#e5e7eb"}`,
        background: enabled ? "#fffbeb" : "#fafafa",
      }}>
        <div>
          <div style={{ fontSize: 13, fontWeight: 600, color: enabled ? "#92400e" : "#374151", display: "flex", alignItems: "center", gap: 6 }}>
            <span style={{ fontSize: 15 }}>{enabled ? "⚡" : "✋"}</span>
            Auto Approve All AI Actions
            {enabled && (
              <span style={{ fontSize: 9, padding: "1px 6px", borderRadius: 8, background: "#f59e0b", color: "#78350f", fontWeight: 700 }}>ACTIVE</span>
            )}
          </div>
          <p style={{ ...hintTextStyle, marginTop: 3 }}>
            {enabled
              ? "Glossa AI will execute all proposed actions automatically without asking for approval. Click to disable."
              : "Glossa AI will ask for approval before executing actions. Toggle on to run all actions automatically."}
          </p>
        </div>
        {/* Toggle switch */}
        <div
          onClick={() => toggle(!enabled)}
          title={enabled ? "Click to disable auto-approve" : "Click to enable auto-approve"}
          style={{
            width: 44, height: 24, borderRadius: 12, cursor: "pointer", flexShrink: 0,
            background: enabled ? "#f59e0b" : "#d1d5db",
            position: "relative", transition: "background 0.2s",
          }}
        >
          <div style={{
            position: "absolute", top: 3, left: enabled ? 23 : 3,
            width: 18, height: 18, borderRadius: "50%",
            background: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.25)",
            transition: "left 0.2s",
          }} />
        </div>
      </div>
      <p style={{ ...hintTextStyle, marginTop: 6, color: "#9ca3af" }}>
        You can also toggle auto-approve per-session from the <strong>⚡ AUTO</strong> badge
        in the Glossa AI chat header, or via the <strong>▾</strong> dropdown on any Approve button.
      </p>
    </div>
  );
}

const sectionStyle: React.CSSProperties = {
  marginBottom: "2rem",
  padding: "1.25rem",
  border: "1px solid #e5e7eb",
  borderRadius: 8,
};

const sectionTitleStyle: React.CSSProperties = {
  margin: "0 0 0.75rem 0",
  fontSize: 15,
  fontWeight: 600,
  color: "#111827",
};

const hintTextStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 12,
  color: "#6b7280",
  lineHeight: 1.5,
};


const ollamaSection: React.CSSProperties = {
  marginBottom: "2rem",
  padding: "1.25rem",
  border: "1px solid #d1fae5",
  borderRadius: 8,
  background: "#fafffe",
};

