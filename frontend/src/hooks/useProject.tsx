/**
 * Global project context — provides the currently selected project to all views.
 *
 * Usage:
 *   const { activeProject, setActiveProject, projects } = useProject();
 *
 * When activeProject is null the app is in "global" mode — all items are shown
 * unfiltered. When a project is selected every view scopes its data to that
 * project's topics, experiments, and corpora.
 *
 * The selected project ID is persisted in localStorage so it survives page
 * reloads. A `glossa:project-changed` CustomEvent is dispatched on every
 * change so non-React consumers (bottom panel, AI chat) can react.
 */
import { createContext, useCallback, useContext, useEffect, useState } from "react";
import {
  activateProject as apiActivate,
  getActiveProject,
  listProjects,
  type Project,
} from "../api";

const LS_KEY = "glossa_active_project";

interface ProjectCtx {
  /** The currently selected project, or null for global scope. */
  activeProject: Project | null;
  /** All known projects (active-first). */
  projects: Project[];
  /** Switch to a project by ID, or pass null to go global. Syncs to backend. */
  setActiveProject: (id: string | null) => Promise<void>;
  /** Re-fetch the project list from the backend. */
  refreshProjects: () => Promise<void>;
  /** True during the initial load. */
  loading: boolean;
}

const ProjectContext = createContext<ProjectCtx>({
  activeProject: null,
  projects: [],
  setActiveProject: async () => {},
  refreshProjects: async () => {},
  loading: true,
});

export function ProjectProvider({ children }: { children: React.ReactNode }) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeProject, setActive] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

  // ── Load project list + resolve active project ───────────────────────
  const load = useCallback(async () => {
    try {
      const ps = await listProjects();
      setProjects(ps);

      // Determine which project to activate:
      //   1. localStorage override
      //   2. Backend's is_active project
      //   3. null (global)
      const storedId = localStorage.getItem(LS_KEY);
      let resolved: Project | null = null;

      if (storedId) {
        resolved = ps.find((p) => p.id === storedId) ?? null;
      }
      if (!resolved) {
        try {
          const backendActive = await getActiveProject();
          resolved = ps.find((p) => p.id === backendActive.id) ?? null;
        } catch {
          // No active project on backend — stay global.
        }
      }
      setActive(resolved);
      if (resolved) {
        localStorage.setItem(LS_KEY, resolved.id);
      }
    } catch {
      // Backend offline — leave empty.
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  // Listen for external refresh requests (e.g. after ProjectsView creates a project).
  useEffect(() => {
    const handler = () => { void load(); };
    window.addEventListener("glossa:project-changed", handler);
    return () => window.removeEventListener("glossa:project-changed", handler);
  }, [load]);

  // ── Switch project ───────────────────────────────────────────────────
  const setActiveProject = useCallback(async (id: string | null) => {
    if (id === null) {
      setActive(null);
      localStorage.removeItem(LS_KEY);
    } else {
      // Activate on backend so dashboard/insight/mine pick it up.
      try { await apiActivate(id); } catch { /* best-effort */ }
      const proj = projects.find((p) => p.id === id) ?? null;
      setActive(proj);
      if (proj) localStorage.setItem(LS_KEY, proj.id);
      else localStorage.removeItem(LS_KEY);
    }
    // Notify the rest of the app.
    window.dispatchEvent(new CustomEvent("glossa:project-changed"));
  }, [projects]);

  return (
    <ProjectContext.Provider value={{
      activeProject,
      projects,
      setActiveProject,
      refreshProjects: load,
      loading,
    }}>
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject(): ProjectCtx {
  return useContext(ProjectContext);
}
