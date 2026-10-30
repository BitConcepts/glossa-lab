# glossa-edge — the cloud edition perimeter (Spec 083, Step 1)

A TypeScript Cloudflare Worker + Durable Object front, managed by
wrangler. This is the only public surface of the Glossa Lab cloud
edition: identity terminates here, and the container application
behind it is reachable solely through this edge.

```
browser ──> Worker (src/worker.ts)          perimeter, session check
              │                              via D1 (src/session-store.ts)
              └──> GlossaFront (src/front.ts)  one named Durable Object
                     └──> container          the repo-root Dockerfile image,
                                             single instance, port 8001
```

## What the Worker does (T009)

1. **Noindex perimeter (FR-007, C083-7).** Every response the Worker
   returns — container pass-through, edge-generated error, redirect,
   static asset — carries `X-Robots-Tag: noindex, nofollow`, set by the
   edge last so nothing inside can weaken it. `GET /robots.txt` is
   served by the edge itself:

   ```
   User-agent: *
   Disallow: /
   ```

2. **Session termination (FR-004).** The `glossa_session` cookie is
   the only credential the edge reads. The presented token is SHA-256
   hashed and looked up through the `SessionStore` seam
   (`src/session-store.ts`); `D1SessionStore` resolves it against the
   `sessions`/`users`/`workspace_roles` tables. A session authenticates
   only if it is unrevoked, unexpired, and its user is active and not
   removed. Phase 1 ships this lookup seam plus the sliding-activity
   stamp (`last_seen_at`); issuance, login/logout, and revocation
   cascades are Phase 2 (Step 2) on the same store. No other credential
   position is consulted — the Spec 082 install token is not a cloud
   credential in any position (FR-008).

3. **The login wall (FR-004, Amendment 2).** The anonymous surface is
   exactly:

   | Route | Anonymous behavior |
   |---|---|
   | `/robots.txt` | Served by the edge, disallows all |
   | `/login`, `/setup`, `/invite/*` | Forwarded to the container (public pages) |
   | SPA shell assets (`/assets/*`, and a closed list of static extensions: js/css/svg/fonts/images/`webmanifest`) | Forwarded to the container — the shell carries no project data |
   | `/api/*` | **401** `{ "error": { "code": "authentication_required", … } }` |
   | Any other page (GET/HEAD) | **302** to `/login?next=<original path>` |
   | Any other route (non-GET) | **401** |

   A forged, expired, or revoked session is exactly anonymous. The
   dataset hydrates only after authentication — nothing content-bearing
   is served anonymously in any form.

4. **Single-instance routing.** All container-bound traffic goes
   through the one named `GlossaFront` instance, `glossa-lab`
   (`wrangler.toml` caps the container at `max_instances = 1`). The
   Durable Object is the serialization point in front of the single
   container instance, matching the application's single-instance
   design.

## Edge → container header contract

The container trusts these headers **only** because the edge sets
them: the Worker deletes every client-supplied `X-Glossa-*` header
before forwarding, so a value on a container-bound request is the
edge's own assertion, never the client's.

| Header | Present | Meaning |
|---|---|---|
| `X-Glossa-Service-Credential` | On **every** container-bound request | The per-deployment edge↔container service credential (FR-008). Value comes from the Worker secret `SERVICE_CREDENTIAL` (`wrangler secret put`), never from code or config. The container must refuse requests without it. |
| `X-Glossa-User-Id` | Authenticated requests only | The acting user's D1 `users.id`. The container stamps mutating records with it (FR-011). |
| `X-Glossa-User-Name` | Authenticated requests only | The acting user's username, for attribution rendering (FR-011). |
| `X-Glossa-Global-Type` | Authenticated requests only | One of `owner` / `admin` / `member` / `guest` (Amendment 1). |
| `X-Glossa-Workspace-Roles` | Authenticated requests only | JSON object mapping workspace id → role, e.g. `{"ws_…":"owner","ws_…":"viewer"}`. Global Admin/Owner implicit Workspace Admin is applied by the consumer per Amendment 1, not expanded here. |

Anonymous pass-through (public pages/assets) carries the service
credential and **no** identity headers: absence of `X-Glossa-User-Id`
is how the container knows the request is anonymous and may serve only
the public surface.

## Identity schema (T010)

`migrations/` — numbered D1 migrations, applied by the deploy workflow
(remote) or `npm run db:migrate:local` (local):

- `0001_identity_core.sql` — `users` (username unique, Argon2id
  `password_hash`, `global_type` owner/admin/member/guest, `status`,
  `removed_at`), `setup_state` (singleton row; setup code hash-only,
  `completed_at` closes setup forever, FR-003).
- `0002_invites_sessions.sql` — `invites` (**`code_hash` only**,
  optional email binding, `workspace_grants` JSON, expiry/revocation/
  redemption fields), `sessions` (**`token_hash` only**, sliding
  lifetime fields, `revoked_at`).
- `0003_workspaces_audit.sql` — `workspaces` (slug unique,
  `archived_at`), `workspace_roles` (PK user+workspace, role
  owner/admin/member/viewer), `audit_log` (**append-only**: no
  UPDATE/DELETE code path exists anywhere, and BEFORE UPDATE/DELETE
  triggers `RAISE(ABORT)` make it structural).

No real D1 database is created by this step — migrations are files
only until the deploy workflow applies them.

## Configuration decisions (T012)

- **Production only.** `wrangler.toml` defines exactly one deployment:
  name `glossa-edge`, custom domain `glossa.bitconcepts.tech`, D1
  binding `DB` → `glossa-identity`, R2 binding `DATASETS` →
  `glossa-datasets`. There are no `[env.*]` sections.
- **Ephemeral previews** are ad-hoc deploys under a throwaway name,
  used for verification and torn down after:

  ```sh
  npx wrangler deploy --name glossa-edge-preview-<suffix>
  npx wrangler delete glossa-edge-preview-<suffix>   # teardown
  ```

  A preview name has no custom domain; it answers on its
  workers.dev URL for the duration of the proof run only.
- **Container definition.** `[[containers]]` points `image` at
  `../../Dockerfile` — wrangler resolves the path relative to
  `wrangler.toml`'s directory (`cloud/edge/`), i.e. the repository-root
  Dockerfile, and builds with that directory as the build context.
  `instance_type = "standard-1"`; `max_instances = 1` (correctness,
  not sizing). `GlossaFront.defaultPort` is **8001**, the backend's
  configured port — the Dockerfile must serve the app there.
- **DO registration** uses the `[exports.GlossaFront]` block
  (SQLite-backed Durable Object storage), the current wrangler
  mechanism; it supersedes the legacy `[[migrations]]` array, which
  cannot be combined with it.
- **Placeholder database_id.** `wrangler.toml` carries the all-zeros
  UUID until the real D1 database exists; the deploy workflow fails
  closed while the placeholder stands (see the checklist below).

## Deploy checklist (once the Cloudflare account gate clears)

```sh
cd cloud/edge
npx wrangler d1 create glossa-identity        # paste the returned id into wrangler.toml
npx wrangler r2 bucket create glossa-datasets
npx wrangler secret put SERVICE_CREDENTIAL    # operator-generated value; never committed
npm run db:migrate:remote                     # or let the workflow do it
# then deploy via .github/workflows/deploy-cloud.yml (workflow_dispatch or a cloud-* tag)
```

## Local development + tests

```sh
npm install
npm test          # vitest: perimeter, gating, header-contract, D1-store, config guards
npm run typecheck
npx wrangler dev  # local edge (needs Docker for the container; D1/R2 are local stand-ins)
npm run db:migrate:local
```

The full local topology (edge + app + stand-ins) is the compose build
in `cloud/docker-compose.yml`; see `cloud/README.md` for how the
Step 3/5 proofs run against it.

**Testing choice.** The unit tests use plain vitest with mocks rather
than `@cloudflare/vitest-pool-workers`: the pool runs the Worker under
workerd, but `GlossaFront` is a container-backed Durable Object whose
lifecycle needs a Docker-backed runtime, so pool tests could not
exercise the real front from this environment either. Phase 1's proofs
therefore target the Worker's logic against its seams (a fake
`SessionStore`, a fake Durable Object stub), and the integrated
edge→container path is proven in Step 5 against the local
production-shaped build and an ephemeral preview deployment.
