// The Glossa Lab cloud edge Worker (Spec 083, Step 1 / T009).
//
// The Worker is the perimeter:
//   1. EVERY response carries `X-Robots-Tag: noindex, nofollow`
//      (FR-007) — pass-through, edge-generated, error, and redirect.
//   2. `GET /robots.txt` is served by the edge itself, disallowing all.
//   3. Sessions terminate here: the session cookie is checked against
//      D1 (via the SessionStore seam) before any traffic is routed.
//   4. The anonymous surface is exactly /login, /setup, /invite/*,
//      /robots.txt, and the SPA shell/assets (FR-004, Amendment 2).
//      Anonymous API requests answer 401; anonymous page requests
//      redirect to /login.
//   5. Everything that reaches the container goes through the single
//      named Durable Object instance (GlossaFront, "glossa-lab"),
//      which is the serialization point in front of the single
//      container instance.

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

/** The one named GlossaFront instance — there is exactly one. */
export const FRONT_INSTANCE_NAME = "glossa-lab";

/** robots.txt body: disallow everything, on every crawler. */
export const ROBOTS_TXT = "User-agent: *\nDisallow: /\n";

/** Test seam: Phase 1 tests inject a fake SessionStore and clock. */
export interface EdgeDeps {
  store?: SessionStore;
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

  const store = deps.store ?? new D1SessionStore(env.DB);
  const now = (deps.now ?? (() => new Date()))();
  const token = readSessionCookie(request);
  const tokenHash = token ? await sha256Hex(token) : null;
  const identity = tokenHash
    ? await store.findIdentityByTokenHash(tokenHash, now)
    : null;

  if (identity && tokenHash) {
    // Sliding activity stamp (FR-004's 30-day sliding lifetime is
    // Phase 2; Phase 1 records last_seen_at). Best-effort: a failed
    // stamp never blocks the request.
    ctx.waitUntil(
      store.touchSession(tokenHash, now).catch(() => undefined),
    );
    return forwardToFront(request, env, identity);
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

function jsonError(status: number, code: string, message: string): Response {
  return new Response(JSON.stringify({ error: { code, message } }), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
}
