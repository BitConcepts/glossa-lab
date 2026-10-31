/**
 * Spec 083 (Step 3) — cloud session state + the gate that decides
 * what a visitor sees.
 *
 * Mode detection (one probe, `GET /api/session`):
 *   - 200 with a user        → the cloud edition, signed in;
 *   - 401 authentication_required (the edge's own JSON) → the cloud
 *     edition, anonymous: only the login / setup / invite surfaces
 *     exist (Amendment 2's login wall);
 *   - anything else (404 from the desktop backend, a network
 *     failure, a non-edge deployment) → NOT the cloud edition: the
 *     desktop shell renders exactly as before.
 *
 * The probe result is the only cloud state the shell needs. Sign-in,
 * setup, redemption and sign-out end in full-page navigations (the
 * edge's own flows), so the probe re-runs naturally on each load;
 * it also re-runs on window focus and every minute so an expired or
 * revoked session drops the shell back to the login wall instead of
 * leaving a signed-in-looking UI over a dead session.
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { CloudApiError, getSession, logout } from "./api";
import type { CloudUser, SessionWorkspace } from "./types";
import { InvitePage, LoginPage, SetupPage } from "./pages";
import "./cloud.css";

export type CloudMode = "probing" | "desktop" | "anon" | "user";

export interface CloudSession {
  mode: CloudMode;
  /** True only in the cloud edition with a live session. */
  active: boolean;
  user: CloudUser | null;
  workspaces: SessionWorkspace[];
  implicitAdmin: boolean;
  isAdmin: boolean;
  refresh: () => Promise<void>;
  signOut: () => Promise<void>;
}

const CloudSessionContext = createContext<CloudSession>({
  mode: "probing",
  active: false,
  user: null,
  workspaces: [],
  implicitAdmin: false,
  isAdmin: false,
  refresh: async () => {},
  signOut: async () => {},
});

export const useCloudSession = (): CloudSession => useContext(CloudSessionContext);

interface ProbeState {
  mode: CloudMode;
  user: CloudUser | null;
  workspaces: SessionWorkspace[];
  implicitAdmin: boolean;
}

const DESKTOP: ProbeState = { mode: "desktop", user: null, workspaces: [], implicitAdmin: false };
const ANON: ProbeState = { mode: "anon", user: null, workspaces: [], implicitAdmin: false };

async function probe(): Promise<ProbeState> {
  try {
    const s = await getSession();
    return {
      mode: "user",
      user: s.user,
      workspaces: s.workspaces,
      implicitAdmin: s.implicit_workspace_admin,
    };
  } catch (e) {
    if (e instanceof CloudApiError && e.status === 401 && e.code === "authentication_required") {
      return ANON;
    }
    return DESKTOP;
  }
}

export function CloudSessionProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<ProbeState>({ mode: "probing", user: null, workspaces: [], implicitAdmin: false });
  const stateRef = useRef(state);
  stateRef.current = state;

  const refresh = useCallback(async () => {
    const next = await probe();
    // A desktop verdict from a network hiccup must not tear down a
    // live cloud session view; only cloud↔cloud transitions and the
    // first verdict apply.
    if (next.mode === "desktop" && stateRef.current.mode !== "probing") return;
    setState(next);
  }, []);

  useEffect(() => {
    void refresh();
    const onFocus = () => { void refresh(); };
    window.addEventListener("focus", onFocus);
    const t = window.setInterval(() => { void refresh(); }, 60_000);
    return () => {
      window.removeEventListener("focus", onFocus);
      window.clearInterval(t);
    };
  }, [refresh]);

  const signOut = useCallback(async () => {
    try { await logout(); } catch { /* the cookie may already be gone */ }
    window.location.assign("/login");
  }, []);

  const value: CloudSession = {
    mode: state.mode,
    active: state.mode === "user",
    user: state.user,
    workspaces: state.workspaces,
    implicitAdmin: state.implicitAdmin,
    isAdmin: state.user?.global_type === "admin" || state.user?.global_type === "owner",
    refresh,
    signOut,
  };

  return (
    <CloudSessionContext.Provider value={value}>
      {children}
    </CloudSessionContext.Provider>
  );
}

function inviteCodeFromPath(): string | null {
  const m = window.location.pathname.match(/^\/invite\/([^/]+)\/?$/);
  return m ? decodeURIComponent(m[1]) : null;
}

/**
 * Decides between the desktop shell (children), the cloud auth
 * surfaces, and a neutral loading state — with NO program data in
 * any anonymous render (Amendment 2: the shell an anonymous visitor
 * receives carries no project data; these pages fetch nothing but
 * their own edge reads).
 */
export function CloudGate({ children }: { children: ReactNode }) {
  const cloud = useCloudSession();
  const path = window.location.pathname;
  const inviteCode = inviteCodeFromPath();

  // A signed-in user who lands on /login or /setup belongs in the app.
  useEffect(() => {
    if (cloud.mode === "user" && (path === "/login" || path === "/setup")) {
      window.location.replace("/");
    }
  }, [cloud.mode, path]);

  if (inviteCode !== null && cloud.mode !== "probing") {
    return (
      <div className="cl-root">
        <InvitePage code={inviteCode} />
      </div>
    );
  }

  if (cloud.mode === "probing") {
    return (
      <div className="cl-root">
        <div className="cl-auth-wrap">
          <div style={{ color: "#dbeafe", fontSize: 13 }}>Loading Glossa Lab…</div>
        </div>
      </div>
    );
  }

  if (cloud.mode === "desktop") return <>{children}</>;

  if (cloud.mode === "anon") {
    return (
      <div className="cl-root">
        {path === "/setup" ? <SetupPage /> : <LoginPage />}
      </div>
    );
  }

  // Signed in: /login and /setup redirect above; everything else is
  // the app itself.
  if (path === "/login" || path === "/setup") return null;
  return <>{children}</>;
}
