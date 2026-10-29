# Feature Specification: Per-Install API Token Authentication (Spec 082)

**Feature Branch**: `spec/082-api-token-auth` (spec) · `feat/082-backend-auth` (backend) · `feat/082-consumers` (tray/scripts/proof kit)
**Created**: 2026-10-29
**Status**: DRAFT — claims frozen before code (spec-kit + AEE flow). Implementation lands in the PR sequence in `plan.md`; the desktop cutover is declared final only when the proof kit (`tools/auth-proof/check_auth.py`) passes against the desktop install.
**Input**: Owner decision, 2026-10-29 (standing rule: the coordinator's recommendation is the decision): token authentication lands BEFORE the desktop cutover is declared final. The cutover sequence continues in parallel.
**Predecessor**: Leg C red-team finding **C-01 (Critical)** in `docs/governance/legc-gaps-2026-10-29.md` (GAP-C01) — no authentication anywhere in the backend, confirmed against code and the production OpenAPI schema. Builds on Spec 079 (supervised backend + tray), Spec 080 (desktop host migration — installer, tray, verify discipline), and Leg C C-08 (health carries served identity, not liveness).

## Problem statement

The backend executes studies, exposes a (sandboxed, since PR #445) terminal, accepts evidence uploads and URL imports, and drives the full claim machinery — and every one of those routes answers **any** caller who can reach the port. Today the port is loopback plus Tailscale Serve on the owner's tailnet, so the unauthenticated write surface is exposed to every process on the owner's machines and every device on the tailnet. C-01 rated this Critical; GAP-C01 recorded it as an architecture decision for the program owner. The owner has now decided: **a per-install bearer token**, sized to what this tool is — a single-operator local research tool. No user accounts, no sessions, no OAuth, no per-route scopes: one install, one token, full access for whoever holds it, nothing for whoever does not.

## Design summary

- **Token**: 256 bits from a CSPRNG (`secrets.token_urlsafe(32)`), generated once per install.
- **Storage**: one file, `api_token`, in the install's data directory (`Settings.data_dir` — Windows installed mode: `%LOCALAPPDATA%\GlossaLab\data\`; Linux installed mode: the XDG data dir; dev/supervised layout: `backend/data\` beside the database it protects). POSIX permissions `0600` where the OS supports asserting them. The token is **never** in git (the data dir is runtime state, gitignored), **never** logged, and **never** returned by any API response. Startup logs name the token file's *path* and the auth *mode* only.
- **Enforcement**: one pure-ASGI middleware in `glossa_lab.main:create_app`. Header: `Authorization: Bearer <token>` — the single accepted credential form. Comparison is constant-time (`hmac.compare_digest`). Rejection is `401` with a JSON detail and a `WWW-Authenticate: Bearer` header; the presented value is never reflected.
- **Resolution order** (backend): `GLOSSA_API_TOKEN` env → token file in the data dir → generate-and-persist at startup (so a pre-token install upgrades itself on first start of the new code, and the tray/installer pre-provisioning below is a convenience, not a prerequisite). Rotation is live: the middleware re-reads the file when its mtime changes, so a rotated token takes effect without a backend restart.
- **Kill switch**: `GLOSSA_API_AUTH=off` disables enforcement. It exists for exactly one purpose — CI's frontend-tests job runs a pre-token-handling frontend against a throwaway backend until Spec 081 Phase 2 ships the UI contract — and it is **loud, never silent**: startup logs a warning naming it, and the health payload reports `"auth": "disabled"` (see FR-006). Installers never set it. Its removal is a filed task (T010) owned by the Phase 2 landing.

## Open routes — the complete list, with reasons

| Route | Why it stays open |
|---|---|
| `GET /api/v1/health` | Carries only the C-08 identity stamp — `status`, `version`, `uptime_seconds`, `component`, `build` — plus, from this spec, `auth` (the mode word `token`/`disabled`). No install data, no claim data, no secret. The tray's 3-second poll, the Spec 079 bounded healthcheck, the desktop verify scripts, and Tailscale Serve health all depend on an unauthenticated liveness+identity read; gating it would force the token into every supervisor before it can prove the app is the app. Acceptable on the loopback+tailnet posture precisely because the payload is identity-only. |
| `GET /` and the built frontend bundle (`StaticFiles` at `/`) | The SPA must load before it can present a credential; the bundle is built assets only — no install data, no token (the token reaches the page via the tray's URL-fragment handoff, `ui-contract.md`, never via a served file). |
| `GET /static/signs/...` | Published sign-glyph images from the open corpus. Not install data; the restricted page-preview scans are **not** served by any route (Leg C C-10) and stay that way. |

Everything else requires the token: **all** other `/api/...` routes of every method (data reads, study execution, terminal, uploads/imports, settings, the shutdown route the stop path uses), and the schema surfaces `GET /docs`, `GET /redoc`, `GET /openapi.json` — the OpenAPI schema was C-01's confirmation vector, so it is behind the token too; the supervision healthcheck sends the token for its `/docs` + `/openapi.json` identity legs (FR-005).

## User Scenarios & Testing

### User Story 1 — The operator's own surfaces keep working (Priority: P1)

The operator starts Glossa Lab from the tray as today. The tray polls health (open), opens the UI with access, and can stop the backend (the shutdown route now requires the token the tray reads from the install's token file).

**Acceptance Scenarios**:

1. **Given** an installed host with a token file, **When** the tray polls health, **Then** it reports status exactly as before (the route is open).
2. **Given** the tray, **When** the operator clicks *Open Glossa Lab*, **Then** the browser opens the UI with the token in the URL fragment (`#token=…`) per `ui-contract.md`, and the UI's API calls succeed.
3. **Given** the tray, **When** the operator stops the service, **Then** the shutdown request carries the token and the backend stops gracefully (no fall back to the kill path because of a 401).
4. **Given** the tray, **When** the operator clicks *Copy API Token*, **Then** the install token is on the clipboard and nothing about it appears in any log.

### User Story 2 — A stranger on the tailnet gets nothing (Priority: P1)

Another device on the tailnet (or any local process) calls the API without the token.

**Acceptance Scenarios**:

1. **Given** no `Authorization` header, **When** any protected route is called (read or write), **Then** the response is `401` and no state changes and no data is returned.
2. **Given** a wrong token, **When** any protected route is called, **Then** `401`, identical in shape to the missing-token response.
3. **Given** the install token, **When** the same routes are called, **Then** they behave exactly as they did before this spec.

### User Story 3 — Supervision still verifies identity (Priority: P1)

The bounded healthcheck (Linux unit + desktop start path) and the desktop verify scripts prove the served app's identity against an authed install.

**Acceptance Scenarios**:

1. **Given** an authed backend and the token file present, **When** `services/linux/healthcheck.py` runs, **Then** the identity check passes (health leg open; `/docs` + `/openapi.json` legs carry the token).
2. **Given** an authed backend and **no** resolvable token, **When** the healthcheck runs, **Then** it fails *named* — the result's errors say the token could not be resolved and list the paths tried — never a silent pass and never a bare unexplained 401.

### User Story 4 — Rotation without data loss (Priority: P2)

The operator rotates the token (suspected leak, new device, routine hygiene).

**Acceptance Scenarios**:

1. **Given** a running install, **When** the operator runs `python -m glossa_lab.auth rotate`, **Then** a new token replaces the old one atomically, the old token immediately returns `401`, the new token works with no backend restart and no data change, and the command prints only the token's fingerprint and path — never the value.
2. **Given** a consumer still holding the old token, **When** it calls the API, **Then** it gets `401` (a named, diagnosable failure), and the operator's remedy is the documented procedure in `plan.md` §Rotation.

### User Story 5 — Agent access via MCP (Priority: P2)

The MCP server (in-repo, `backend/glossa_mcp/server.py`) and the skill client call the backend with the token taken from `GLOSSA_API_TOKEN` (or the token file), so agent tooling keeps working against the authed backend — including after the cutover repoints `GLOSSA_BASE_URL` at the desktop install.

## Requirements

- **FR-001 Enforcement.** Every route not listed in the open-routes table rejects a missing or incorrect token with `401` and accepts the install token, for all HTTP methods. Enforcement lives in middleware, not per-route code, so a future route is protected by default.
- **FR-002 Token lifecycle.** Generation uses a CSPRNG (≥ 256 bits). The token lives only in the data-dir token file (`0600` on POSIX) or the `GLOSSA_API_TOKEN` env of a process the operator launched. It is never written to git, never logged (including in error paths), never returned by an API response, and never placed in a URL query string by any first-party consumer (the tray's fragment handoff is the one sanctioned URL carrier; fragments are not sent to servers and the UI contract requires stripping it from the address bar on load).
- **FR-003 Consumers.** The tray (health poll, shutdown, open-UI, copy-token), the supervision healthcheck and desktop verify path, the in-repo MCP server, and the skill client all obtain and present the token as specified in `plan.md`; each one's failure to resolve a token is a *named* failure in its own log/output, never a silent pass.
- **FR-004 Rotation.** A documented, scripted rotation (`python -m glossa_lab.auth rotate`) replaces the token atomically and takes effect without a backend restart or any data migration; consumers re-resolve on their next call (tray/healthcheck read the file per use; MCP reads its env — an env-carried token is rotated by updating the env, which the procedure states).
- **FR-005 Healthcheck identity.** `services/linux/healthcheck.py` keeps its bounded, identity-first contract (H11): health leg unauthenticated; `/docs` and `/openapi.json` legs authenticated with the resolved token; unresolvable token ⇒ failed check with the resolution paths named in the errors.
- **FR-006 No silent open state.** The only non-enforcing configuration is `GLOSSA_API_AUTH=off`; it logs a startup warning and is reported by the health payload as `"auth": "disabled"` (enforcing installs report `"auth": "token"`). No mode flag, dev flag, or file state other than that switch disables enforcement.
- **FR-007 UI contract.** The web UI's token behavior is specified in `ui-contract.md` in this folder and is implemented by the Spec 081 Phase 2 build (frontend/ is that worker's surface). This spec's server side guarantees the contract's assumptions: the header is accepted from any origin the CORS policy already allows, SSE endpoints accept the header on a fetch-based stream (no query-param credential exists or will be added), and a `401` body is JSON with a stable `detail` string the UI can key on.
- **FR-008 Proof kit.** `tools/auth-proof/check_auth.py` (stdlib-only, bounded waits) proves an install end-to-end: health open and reporting `auth: token`; a data route without a token → `401`; with a wrong token → `401`; with the install token → `200`; a state-changing route without a token → `401`. "Cutover declared final" is gated on its pass against the desktop install.

## Claims

Frozen in `aee-claims.json` (C082-1…C082-6), each with evidence and a falsifier, in the post-PR-#450 normalized bundle format; the bundle loads and assesses under the pinned AEE 1.5.3 assessor. Summary:

- **C082-1** Route enforcement matrix (FR-001) — tested per route family.
- **C082-2** Token generation, storage, and non-disclosure (FR-002).
- **C082-3** Named consumers keep working with the token in place (FR-003, FR-005).
- **C082-4** Rotation is atomic, restart-free, and data-preserving (FR-004).
- **C082-5** Health posture: open, identity-only, auth mode visible (FR-006 + open-routes table).
- **C082-6** No silent open state (FR-006).

## Assumptions — epistemic boundaries (H13)

- **Trust model**: single operator; the token is a bearer credential — possession is authorization, with no scoping. This deliberately does not defend against a process already running as the operator's own user (it can read the token file); it defends the port against everything that is *not* the operator's own session: other tailnet devices, other local users, stray processes, and accidental cross-tool calls.
- **Exposure model**: loopback + the owner's tailnet via Tailscale Serve. No TLS is added (the tailnet leg is already encrypted by Tailscale; the loopback leg never leaves the machine). If the backend is ever bound beyond loopback/tailnet, this spec must be revisited first.
- **SSE**: streaming endpoints are header-authenticated like every other route; browser consumers must use fetch-based streaming (an `EventSource` cannot set headers). No query-string token fallback is provided — query strings land in logs, which FR-002 forbids for the token.
- **Adversarial challenge that would break this design**: theft of the token file itself (mitigated only by OS file permissions and the operator's machine hygiene — accepted, stated, and the reason rotation exists); a future first-party consumer that logs request headers (guarded by C082-2's falsifier: a token string found in any log fails the claim).
- **Confidence**: the route inventory is derived from `create_app()` at `bb68bb88`; middleware-level enforcement makes the inventory non-load-bearing (a route added tomorrow is protected by construction), which is why FR-001 is stated at the middleware, not as a route list.

## Out of scope

User accounts, login UI, sessions, OAuth/OIDC, per-route or per-scope permissions, rate limiting, TLS termination, token expiry (rotation is the lifecycle), the frontend implementation of `ui-contract.md` (Spec 081 Phase 2), and any change to the VM's running backend (it stays on its current code — unauthenticated — until the cutover replaces it; this spec's code lands on `main` only).
