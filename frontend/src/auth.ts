/**
 * Spec 082 — API token handling for the SPA (ui-contract.md).
 *
 * The token reaches the app in the launch URL fragment
 * (`/#token=<token>`), is read ONCE at startup, stored in
 * sessionStorage under `glossa_api_token`, and the fragment is
 * stripped from the address bar immediately. Every API call sends
 * `Authorization: Bearer <token>`; query-string tokens are refused by
 * design — the backend rejects them and this module never sends one.
 *
 * On a 401 the stored token is cleared and the app enters the named
 * "API token needed" state (see `tokenNeeded`). When the backend's
 * open health endpoint reports `auth: "disabled"`, no token is needed
 * and the gate never appears.
 */

export const TOKEN_STORAGE_KEY = "glossa_api_token";

/** The one open route — safe to call before any token exists. */
const HEALTH_URL = "/api/v1/health";

export interface AuthState {
  /** A token is stored in sessionStorage. */
  hasToken: boolean;
  /** First 8 hex chars of the token's SHA-256 ("" when absent). */
  fingerprint: string;
  /** Backend auth mode from /health: "token" | "disabled" | null (unknown). */
  authMode: "token" | "disabled" | null;
  /** True when the backend requires a token and none works. */
  tokenNeeded: boolean;
}

let _hasToken = false;
let _fingerprint = "";
let _authMode: AuthState["authMode"] = null;
let _tokenNeeded = false;
let _initialized = false;

const _listeners = new Set<() => void>();

function _emit(): void {
  for (const fn of _listeners) {
    try { fn(); } catch { /* a listener must never break auth */ }
  }
}

export function getAuthState(): AuthState {
  return {
    hasToken: _hasToken,
    fingerprint: _fingerprint,
    authMode: _authMode,
    tokenNeeded: _tokenNeeded,
  };
}

export function subscribeAuth(fn: () => void): () => void {
  _listeners.add(fn);
  return () => { _listeners.delete(fn); };
}

export function getApiToken(): string | null {
  try {
    return sessionStorage.getItem(TOKEN_STORAGE_KEY);
  } catch {
    return null;
  }
}

/** Authorization header for fetch calls, or {} when no token is stored. */
export function authHeaders(): Record<string, string> {
  const t = getApiToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

async function _fingerprintOf(token: string): Promise<string> {
  try {
    const digest = await crypto.subtle.digest(
      "SHA-256",
      new TextEncoder().encode(token),
    );
    return Array.from(new Uint8Array(digest))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("")
      .slice(0, 8);
  } catch {
    return "";
  }
}

async function _refreshTokenMeta(): Promise<void> {
  const t = getApiToken();
  _hasToken = !!t;
  _fingerprint = t ? await _fingerprintOf(t) : "";
  if (_authMode === "token") _tokenNeeded = !_hasToken;
  if (_authMode === "disabled") _tokenNeeded = false;
}

/** Store a token (fragment intake or the Settings paste field). */
export async function setApiToken(token: string): Promise<void> {
  const value = token.trim();
  if (!value) return;
  try { sessionStorage.setItem(TOKEN_STORAGE_KEY, value); } catch { /* */ }
  await _refreshTokenMeta();
  _emit();
}

/** Clear the stored token (401 handling, or the Settings remove action). */
export async function clearApiToken(reason: "unauthorized" | "manual"): Promise<void> {
  try { sessionStorage.removeItem(TOKEN_STORAGE_KEY); } catch { /* */ }
  await _refreshTokenMeta();
  if (reason === "unauthorized" && _authMode !== "disabled") {
    _tokenNeeded = true;
  }
  _emit();
}

/**
 * Called by the API layer on any 401: the presented credential (if
 * any) does not work, so it is cleared and the app asks for a token.
 */
export function noteUnauthorized(): void {
  void clearApiToken("unauthorized");
}

/**
 * Read the launch fragment once. Returns true when a token was taken
 * in. Safe to call before React mounts (main.tsx) so the fragment is
 * stripped before the router's hash sync can observe it.
 */
export function intakeTokenFromFragment(): boolean {
  const hash = window.location.hash;
  if (!hash.startsWith("#token=")) return false;
  const token = decodeURIComponent(hash.slice("#token=".length)).trim();
  // Strip the fragment whatever it carried — it must not linger in
  // the address bar, history, or screenshots.
  window.history.replaceState(null, "", window.location.pathname + window.location.search);
  if (!token) return false;
  try { sessionStorage.setItem(TOKEN_STORAGE_KEY, token); } catch { /* */ }
  void _refreshTokenMeta().then(_emit);
  return true;
}

/**
 * Probe the one open route to learn the backend's auth mode. When the
 * backend does not answer at all, the mode stays unknown and no gate
 * is shown (the shell's own connectivity states carry that case).
 */
export async function probeAuthMode(): Promise<void> {
  try {
    const res = await fetch(HEALTH_URL);
    if (!res.ok) return;
    const data = (await res.json()) as { auth?: string };
    if (data.auth === "token" || data.auth === "disabled") {
      _authMode = data.auth;
    }
  } catch { /* backend unreachable — mode unknown */ }
  await _refreshTokenMeta();
  _emit();
}

/**
 * Startup: fragment intake (idempotent), health probe, and a
 * hashchange listener so a tray "Open Glossa Lab" click in an
 * already-open tab still takes the token in.
 */
export async function initAuth(): Promise<void> {
  if (_initialized) return;
  _initialized = true;
  intakeTokenFromFragment();
  window.addEventListener("hashchange", () => { intakeTokenFromFragment(); });
  await _refreshTokenMeta();
  _emit();
  await probeAuthMode();
}
