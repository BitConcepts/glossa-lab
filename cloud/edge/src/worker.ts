// The Glossa Lab cloud edge Worker (Spec 083, Step 1 / T009;
// Step 2 identity routes added on the same seams).
//
// The Worker is the perimeter:
//   1. EVERY response carries `X-Robots-Tag: noindex, nofollow`
//      (FR-007) — pass-through, edge-generated, error, and redirect.
//   2. `GET /robots.txt` is served by the edge itself, disallowing all.
//   3. Sessions terminate here: the session cookie is checked against
//      D1 (via the SessionStore seam) before any traffic is routed.
//      Only the session cookie authenticates — Authorization headers
//      are never consulted, and the Spec 082 install token is not a
//      cloud credential in any position (FR-008, T024).
//   4. The anonymous surface is exactly /login, /setup, /invite/*,
//      /robots.txt, and the SPA shell/assets (FR-004, Amendment 2).
//      Anonymous API requests answer 401; anonymous page requests
//      redirect to /login.
//   5. Identity routes (Step 2) are answered by the edge itself from
//      D1: POST /login, POST /logout, POST /invite/:code/redeem,
//      POST /setup, and the whole /api/admin/* surface. Account
//      creation exists ONLY as invite redemption and the setup —
//      there is no other registration route in this Worker (FR-001).
//      Step 3 adds the read/self-service companions the frontend
//      needs: GET /invite/:code/preview, GET /api/session, the
//      /api/account/* self-service surface, GET /api/admin/audit,
//      and workspace descriptions (migration 0005).
//   6. Everything else that reaches the container goes through the
//      single named Durable Object instance (GlossaFront,
//      "glossa-lab").

import { classifyRoute, normalizePathname } from "./routes";
import {
  D1SessionStore,
  type SessionIdentity,
  type SessionStore,
} from "./session-store";
import { readSessionCookie, sha256Hex } from "./session";
import {
  HEADER_GLOBAL_TYPE,
  HEADER_SERVICE_CREDENTIAL,
  HEADER_USER_ID,
  HEADER_USER_NAME,
  HEADER_WORKSPACE_ROLES,
  withNoindex,
} from "./headers";
import type { Env } from "./types";
import {
  D1IdentityStore,
  type IdentitySessionStore,
} from "./identity-store";
import {
  auditContainerDenial,
  handleAccountApi,
  handleAdminApi,
  handleInvitePreview,
  handleInviteRedeem,
  handleLogin,
  handleLogout,
  handleSessionIdentity,
  handleSetup,
  isSetupOpen,
  jsonError,
  requireAdmin,
  type IdentityDeps,
} from "./identity";
import { defaultHasher, type PasswordHasher } from "./password";

/** The one named GlossaFront instance — there is exactly one. */
export const FRONT_INSTANCE_NAME = "glossa-lab";

/** robots.txt body: disallow everything, on every crawler. */
export const ROBOTS_TXT = "User-agent: *\nDisallow: /\n";

/** Test seam: Phase 1 tests inject a fake SessionStore and clock;
 *  Step 2 tests additionally inject an IdentityStore + hasher. */
export interface EdgeDeps {
  store?: SessionStore;
  identityStore?: IdentitySessionStore;
  hasher?: PasswordHasher;
  now?: () => Date;
}

export async function handleRequest(
  request: Request,
  env: Env,
  ctx: ExecutionContext,
  deps: EdgeDeps = {},
): Promise<Response> {
  try {
    return withNoindex(await route(request, env, ctx, deps));
  } catch (err) {
    console.error("glossa-edge: unhandled error", err);
    return withNoindex(
      jsonError(500, "internal_error", "The edge failed to handle this request."),
    );
  }
}

/**
 * Paths that must never create an account at the edge (FR-001).
 * They are refused outright (404) for write methods, for anonymous
 * and authenticated callers alike — defensive depth behind the fact
 * that no registration handler is registered for them at all.
 */
const REGISTRATION_REFUSAL_PATHS = new Set([
  "/register",
  "/signup",
  "/api/register",
  "/api/signup",
  "/api/auth/register",
  "/api/auth/signup",
  "/api/users",
]);

function resolveIdentityStore(env: Env, deps: EdgeDeps): IdentitySessionStore | null {
  if (deps.identityStore) return deps.identityStore;
  const db = env.DB as unknown as { prepare?: unknown } | undefined;
  if (db && typeof db.prepare === "function") {
    return new D1IdentityStore(env.DB);
  }
  return null;
}

/** Container routes whose 403/404 answers are workspace-scope denials. */
function isScopedContainerRoute(pathname: string): boolean {
  return pathname.startsWith("/api/") || pathname.startsWith("/workspaces/");
}

async function route(
  request: Request,
  env: Env,
  ctx: ExecutionContext,
  deps: EdgeDeps,
): Promise<Response> {
  const url = new URL(request.url);
  const pathname = normalizePathname(url.pathname);
  const routeClass = classifyRoute(pathname);

  if (routeClass === "robots") {
    return new Response(ROBOTS_TXT, {
      status: 200,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "public, max-age=3600",
      },
    });
  }

  const nowFn = deps.now ?? (() => new Date());
  const now = nowFn();
  const identityStore = resolveIdentityStore(env, deps);
  const store: SessionStore =
    deps.store ?? identityStore ?? new D1SessionStore(env.DB);
  const identityDeps: IdentityDeps | null = identityStore
    ? { store: identityStore, hasher: deps.hasher ?? defaultHasher, now: nowFn }
    : null;

  const token = readSessionCookie(request);
  const tokenHash = token ? await sha256Hex(token) : null;
  const identity = tokenHash
    ? await store.findIdentityByTokenHash(tokenHash, now)
    : null;

  const method = request.method.toUpperCase();

  // ---- Step 2 edge-handled identity routes (never forwarded) ----

  if (pathname === "/login" && method === "POST") {
    if (!identityDeps) return identityUnavailable();
    return handleLogin(request, identityDeps);
  }

  if (pathname === "/logout" && method === "POST") {
    if (!identityDeps) return identityUnavailable();
    return handleLogout(identityDeps, identity, tokenHash);
  }

  const redeemMatch = pathname.match(/^\/invite\/([^/]+)\/redeem$/);
  if (redeemMatch && method === "POST") {
    if (!identityDeps) return identityUnavailable();
    return handleInviteRedeem(
      request,
      identityDeps,
      decodeURIComponent(redeemMatch[1]),
    );
  }

  // ---- Step 3 edge-handled read + self-service routes ----

  const previewMatch = pathname.match(/^\/invite\/([^/]+)\/preview$/);
  if (previewMatch && method === "GET") {
    if (!identityDeps) return identityUnavailable();
    return handleInvitePreview(
      identityDeps,
      decodeURIComponent(previewMatch[1]),
    );
  }

  if (pathname === "/api/session" && method === "GET") {
    if (!identityDeps) return identityUnavailable();
    if (!identity) {
      return jsonError(401, "authentication_required", "Sign in is required for this route.");
    }
    return handleSessionIdentity(identityDeps, identity);
  }

  if (pathname === "/api/account" || pathname.startsWith("/api/account/")) {
    if (!identityDeps) return identityUnavailable();
    if (!identity || !tokenHash) {
      return jsonError(401, "authentication_required", "Sign in is required for this route.");
    }
    const handled = await handleAccountApi(request, identityDeps, identity, tokenHash, pathname);
    return handled ?? jsonError(404, "not_found", "Not found.");
  }

  if (pathname === "/setup") {
    // Once any admin/owner exists (or setup completed), /setup
    // answers 404 forever (T017) — for API-style reads. A browser
    // NAVIGATION (Accept: text/html) falls through to the SPA
    // instead: the setup page probes the status itself with fetch()
    // and renders its own "setup is closed" state, so answering a
    // navigation with raw JSON would strand a human on an error
    // document (Step 3 fix — Playwright verification caught it).
    const isNavigation =
      method === "GET" && (request.headers.get("accept") ?? "").includes("text/html");
    if (identityDeps && !isNavigation && !(await isSetupOpen(identityDeps))) {
      return jsonError(404, "not_found", "Not found.");
    }
    if (method === "POST") {
      if (!identityDeps) return identityUnavailable();
      return handleSetup(request, identityDeps);
    }
    // An open GET /setup falls through to the public-page forward.
  }

  if (REGISTRATION_REFUSAL_PATHS.has(pathname) && method !== "GET" && method !== "HEAD") {
    return jsonError(404, "not_found", "Not found.");
  }

  if (pathname === "/api/admin" || pathname.startsWith("/api/admin/")) {
    if (!identityDeps) {
      if (!identity) {
        return jsonError(401, "authentication_required", "Sign in is required for this route.");
      }
      if (identity.globalType !== "admin" && identity.globalType !== "owner") {
        return jsonError(403, "admin_required", "Admin access is required for this route.");
      }
      return identityUnavailable();
    }
    const gate = await requireAdmin(identityDeps, identity, pathname);
    if (!gate.ok) return gate.response;
    const handled = await handleAdminApi(request, identityDeps, gate.identity, pathname);
    return handled ?? jsonError(404, "not_found", "Not found.");
  }

  // ---- Step 1 perimeter ----

  if (identity && tokenHash) {
    // Sliding activity stamp (FR-004, D-3): last_seen_at is stamped
    // and expires_at extended to now + 30 days (SessionStore.touch).
    // Best-effort: a failed stamp never blocks the request.
    ctx.waitUntil(
      store.touchSession(tokenHash, now).catch(() => undefined),
    );
    const response = await forwardToFront(request, env, identity);
    // T022: log container-scope denials the edge observes on proxied
    // responses (authenticated actor + scoped route + 403/404).
    if (
      identityDeps &&
      (response.status === 403 || response.status === 404) &&
      isScopedContainerRoute(pathname)
    ) {
      ctx.waitUntil(
        auditContainerDenial(identityDeps, identity, method, pathname, response.status)
          .catch(() => undefined),
      );
    }
    return response;
  }

  // Anonymous. A presented-but-invalid session (forged, expired,
  // revoked, disabled/removed user) is exactly anonymous (C083-4).
  switch (routeClass) {
    case "public-page":
    case "public-asset":
      // The shell and its furniture carry no project data; the
      // container serves them and the dataset hydrates only after
      // authentication (Amendment 2's anonymous payload rule).
      return forwardToFront(request, env, null);
    case "api":
      return jsonError(
        401,
        "authentication_required",
        "Sign in is required for this route.",
      );
    case "page":
    default:
      if (request.method === "GET" || request.method === "HEAD") {
        const next = encodeURIComponent(url.pathname + url.search);
        return new Response(null, {
          status: 302,
          headers: { Location: `/login?next=${next}` },
        });
      }
      return jsonError(
        401,
        "authentication_required",
        "Sign in is required for this route.",
      );
  }
}

function identityUnavailable(): Response {
  return jsonError(
    500,
    "identity_unavailable",
    "The identity store is unavailable for this request.",
  );
}

/**
 * Forward a request through the single GlossaFront instance to the
 * container. Client-supplied `X-Glossa-*` headers are deleted first —
 * the container must only ever see the edge's own assertions. The
 * service credential rides on every container-bound request (it proves
 * the hop came through the edge); identity headers are added only for
 * authenticated requests.
 */
function forwardToFront(
  request: Request,
  env: Env,
  identity: SessionIdentity | null,
): Promise<Response> {
  const headers = new Headers(request.headers);
  for (const name of [...headers.keys()]) {
    if (name.toLowerCase().startsWith("x-glossa-")) headers.delete(name);
  }
  headers.set(HEADER_SERVICE_CREDENTIAL, env.SERVICE_CREDENTIAL);
  if (identity) {
    headers.set(HEADER_USER_ID, identity.userId);
    headers.set(HEADER_USER_NAME, identity.username);
    headers.set(HEADER_GLOBAL_TYPE, identity.globalType);
    headers.set(HEADER_WORKSPACE_ROLES, JSON.stringify(identity.workspaceRoles));
  }
  const forwarded = new Request(request, { headers });
  const stub = env.GLOSSA_FRONT.getByName(FRONT_INSTANCE_NAME);
  return stub.fetch(forwarded);
}
