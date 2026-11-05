// Shared types for the Glossa Lab cloud edge (Spec 083, Step 1 / T009;
// Amendment 5 retarget, T055).
//
// The Worker is the deployment perimeter and the session termination
// point. Identity data lives in D1 (binding `DB`); the application
// itself lives on the owner's desktop (the Spec 080 production
// install) and is reached only through the Workers VPC Service
// binding `GLOSSA_ORIGIN`, whose private transport is the named
// Cloudflare Tunnel `glossa-desktop` (Amendment 5). The tunnel
// publishes no hostname and no application route: this binding is
// the only path from the edge to the application.

/** Global user types (Amendment 1, FR-017). `owner` is singular. */
export type GlobalType = "owner" | "admin" | "member" | "guest";

/** Per-workspace roles (Amendment 1, FR-017). */
export type WorkspaceRole = "owner" | "admin" | "member" | "viewer";

/**
 * A Workers VPC Service binding: the subset of the binding contract
 * the edge uses. `fetch()` routes the request through the VPC
 * Service's tunnel to the registered host (127.0.0.1:8001 on the
 * desktop) and resolves with the origin's response; it rejects when
 * the origin cannot be reached (desktop offline, tunnel down), which
 * the Worker turns into its own noindex 503 (T055).
 */
export interface VpcOriginBinding {
  fetch(request: Request): Promise<Response>;
}

export interface Env {
  /** D1 identity store (database `glossa-identity`). */
  DB: D1Database;
  /**
   * Workers VPC Service binding for `glossa-desktop-origin` — the
   * single origin of the hosted edition (Amendment 5, T055).
   */
  GLOSSA_ORIGIN: VpcOriginBinding;
  /**
   * Edge-to-origin service credential (FR-008). A Worker secret,
   * set with `wrangler secret put SERVICE_CREDENTIAL`. It is injected
   * into origin-bound requests only and is never rendered into any
   * client-visible artifact. Never put a value in code or config.
   */
  SERVICE_CREDENTIAL: string;
}
