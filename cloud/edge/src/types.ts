// Shared types for the Glossa Lab cloud edge (Spec 083, Step 1 / T009).
//
// The Worker is the deployment perimeter and the session termination
// point. Identity data lives in D1 (binding `DB`); dataset bundles live
// in R2 (binding `DATASETS`, consumed by the Step 1 bundle plumbing);
// all container-bound traffic funnels through the single Durable Object
// named by `GLOSSA_FRONT` (class `GlossaFront`, see src/front.ts).

/** Global user types (Amendment 1, FR-017). `owner` is singular. */
export type GlobalType = "owner" | "admin" | "member" | "guest";

/** Per-workspace roles (Amendment 1, FR-017). */
export type WorkspaceRole = "owner" | "admin" | "member" | "viewer";

export interface Env {
  /** D1 identity store (database `glossa-identity`). */
  DB: D1Database;
  /** R2 bucket holding dataset bundles (`glossa-datasets`). */
  DATASETS: R2Bucket;
  /** Durable Object namespace for `GlossaFront`. */
  GLOSSA_FRONT: DurableObjectNamespace;
  /**
   * Edge-to-container service credential (FR-008). A Worker secret,
   * set with `wrangler secret put SERVICE_CREDENTIAL`. It is injected
   * into container-bound requests only and is never rendered into any
   * client-visible artifact. Never put a value in code or config.
   */
  SERVICE_CREDENTIAL: string;
}
