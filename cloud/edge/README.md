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
   removed. Step 2 builds issuance, login/logout, and the revocation
   cascades on this same store (see "Step 2 — identity" below): the
   activity stamp is sliding — each authenticated request extends
   `expires_at` to now + 30 days (D-3). No other credential
   position is consulted — the Spec 082 install token is not a cloud
   credential in any position (FR-008), and an `Authorization` header
   is never treated as a session.

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

## Step 2 — identity (T014–T017, T020–T022, T024)

Identity logic lives behind the `IdentityStore` seam
(`src/identity-store.ts`, D1 implementation + the interface the tests
fake), with handlers in `src/identity.ts`. These routes are answered
by the edge itself from D1 — never forwarded to the container:

| Route | Who | Behavior |
|---|---|---|
| `POST /login` `{username, password}` | anyone | 200 + session cookie on success; unknown user, wrong password, disabled, and removed all answer the identical 401, and every attempt (success and failure) is audit-logged. A dummy-hash Argon2 verify runs for unknown users so timing does not separate them. |
| `POST /logout` | session holder | Deletes the session row (instant revocation), clears the cookie, audit-logged. |
| `POST /invite/:code/redeem` `{username, password, email?}` | invite holder | **Registration path 1 of 2.** Creates a `member` user, applies the invite's workspace grants as initial `workspace_roles`, issues a session. |
| `POST /setup` `{code, password}` | setup-code holder | **Registration path 2 of 2.** Creates the `owner` from the seed record (below). Once any admin/owner exists, `/setup` — page and API — answers 404 forever. |
| `/api/admin/*` | global Admin/Owner only | Member/Guest → 403 (audit-logged denial); anonymous → 401 (audit-logged). See the admin table below. |

There is **no other account-creation route** in the Worker; stray
registration paths (`/register`, `/api/users`, …) are refused 404
for write methods as defensive depth (FR-001, C083-1).

**Passwords (Argon2id, T015).** Implementation: **Argon2id via
`hash-wasm`** — its WASM is inlined as base64, so it runs inside the
Workers isolate with no native binding (Node-native Argon2 packages
cannot load in workerd). Parameters are the OWASP Password Storage
Cheat Sheet's first Argon2id recommendation, inside the 128 MB
isolate budget: **memory 19,456 KiB (19 MiB), iterations 2,
parallelism 1, salt 16 bytes, output 32 bytes**. The encoded hash
(`$argon2id$v=19$m=19456,t=2,p=1$…`) is the only password residue in
D1. Usernames are 3–32 chars of `[a-z0-9_.-]`, normalized to
lowercase, unique case-insensitively (functional unique index in
migration 0004).

**Invites (T014).** Codes are 24-byte CSPRNG values (192 bits;
FR-002 floor is 128). Only the SHA-256 hash is stored
(`invites.code_hash`); the plaintext code is returned **exactly
once**, in the creation response, as `code` + `invite_url`
(`/invite/<code>`) — never stored, never logged, never listed.
Default expiry 7 days (admin-adjustable via `expires_in_days` or
`expires_at` at creation); optional email binding (a bound invite
redeems only for that email, checked before consumption, so a
mismatch never spends it); revocable until redeemed. Redemption is
an atomic check-and-consume: a single conditional
`UPDATE invites … WHERE code_hash = ? AND redeemed_at IS NULL AND
revoked_at IS NULL AND expires_at > ?` — a second redemption, an
expired code, and a revoked code always fail.

**Sessions (T016).** Tokens are 32-byte CSPRNG values (256 bits),
SHA-256 hashed at rest (`sessions.token_hash`), carried only in the
`glossa_session` cookie (`HttpOnly; Secure; SameSite=Lax`,
30-day `Max-Age`). Lifetime is 30 days **sliding**: each
authenticated request stamps `last_seen_at` and extends
`expires_at`. Revocation is by row deletion, in the same operation
as its cause: logout, disable, removal, global-type change, and
workspace-matrix change all delete the target's session rows.

**Glassbreak setup (T017).** The operator seed step:

```sh
cd cloud/edge
npm run seed:setup               # local D1 (the persistence wrangler dev uses)
npm run seed:setup -- --remote   # production D1
```

`scripts/seed-setup.mjs` generates a 32-byte CSPRNG code, stores
only its SHA-256 hash + a 24-hour expiry in `setup_state`, together
with the seed record (username `glassbreak` and the contact email
fixed by Amendment 3), and prints the code to the terminal **once**,
with the production URL `https://glossa.bitconcepts.tech/setup`.
It creates **no user**; the guarded `UPDATE … WHERE completed_at IS
NULL` means re-seeding after completion stores nothing and the
script refuses to print a code. `POST /setup` takes the username
and email from the seed record — they are not request input.

**Admin API (T020/T021)** — all under `/api/admin/*`:

| Route | Behavior |
|---|---|
| `GET /users`, `GET /users/:id` | Sanitized user views (never the password hash), with stored `workspace_roles`. |
| `PATCH /users/:id` or `POST /users/:id/type` `{global_type}` | Type change; sessions revoked in the same operation. **Owner is singular**: granting `owner` to another account is refused (409) and granting it is never possible; removing the owner's type is refused (409) — both refusals are audit-recorded. |
| `POST /users/:id/disable` / `POST /users/:id/enable` | Disable kills sessions instantly; a removed account cannot be re-enabled. |
| `POST /users/:id/remove` (or `DELETE /users/:id`) | Sets `removed_at` (row retained for attribution), status disabled, sessions deleted. |
| `POST /invites`, `GET /invites`, `POST /invites/:id/revoke` (or `DELETE /invites/:id`) | T014 lifecycle. |
| `POST /workspaces` `{name}`, `GET /workspaces`, `POST /workspaces/:id/archive` | Create derives the slug from the name (suffixing `-2`, … on collision); archive stamps `archived_at`. Global Admin/Owner only (FR-016). |
| `GET/PUT /users/:id/workspaces` | The per-user workspace-access matrix: GET returns every workspace with the user's stored role (or null) plus `implicit_workspace_admin` for global Admin/Owner — implicit admin is **not** stored as rows. PUT replaces the full stored set. A Guest may hold **Viewer only**: a PUT granting a Guest more is refused 403 and changes nothing. Granting a workspace `owner` role while another user holds it is refused 409 (one workspace owner per workspace). |

Password-reset link issuance is not part of this step (out of the
Step 2 task list) and is not implemented.

**Audit (T022).** Append-only `audit_log` writes (actor id + label +
timestamp on every row) for: `login_success`, `login_failure`,
`logout`, `invite_created`, `invite_redeemed`, `invite_revoked`,
`setup_completed`, `user_type_changed`, `user_type_change_refused`,
`user_disabled`, `user_enabled`, `user_removed`,
`workspace_created`, `workspace_archived`,
`workspace_matrix_changed`, `admin_api_denial` (every 401/403 the
admin gate produces, and Guest-cap refusals), and
`container_scope_denial` — when an authenticated request is proxied
and the container answers 403/404 on a scoped route (`/api/*`,
`/workspaces/*`), the edge logs the denial with actor + route +
status. There is no update or delete path for the audit log in any
API, and the Step 1 triggers make that structural.

**Credential separation (T024).** Tested in
`test/credential-separation.test.ts`: the Spec 082 install token
presented as the session cookie, as another cookie, as an
`Authorization` header, or as a query parameter yields no
authenticated access in any position; a genuine session token moved
out of the cookie into a header or query likewise does not
authenticate.

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
- `0004_setup_seed_and_username_case.sql` (Step 2) — `setup_state`
  gains the seed record columns (`username`, `email`) the seed step
  writes, and a functional unique index on `lower(username)` makes
  username uniqueness case-insensitive structurally.

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
