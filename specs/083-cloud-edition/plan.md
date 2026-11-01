# Plan: Glossa Lab Cloud Edition — Accounts, Workspaces, Hosted Tool (Spec 083)

Claims first (Step 0, this PR), then five build steps, each landing green on
its own under the repo discipline (genuine CI from per-job conclusions, C4
freeze gate included; branches deleted on merge). Nothing here changes the
desktop edition. Production go-live is Step 5 and follows the pre-launch
proofs directly — there is no staging deployment at any point.

**Reading note — amendments govern.** Amendments 1–5 supersede the base
spec and decisions file wherever they conflict: Amendment 1 replaces
the spec's program-membership model with **workspaces** (global user
types crossed with per-workspace roles) and adds claims C083-15…19;
Amendment 2 deletes FR-014's staging-first rollout and D-7's staging
hostname — production only, verified on a local production-shaped
build and ephemeral preview deployments; Amendment 3 fixes the
glassbreak seed record (username `glassbreak`, email
`tristen.pierson@gmail.com`); Amendment 4 (Cloud Run compute + GCS
bundles) is **superseded in full by Amendment 5**: the origin is the
Spec 080 production desktop install, reached through a named
Cloudflare Tunnel consumed through a Workers VPC Service binding, and
Step 4's publisher is retired. Where the base text says "program,"
read "workspace" in the amended sense.


## Step 0 — spec adoption (PR: `spec/083-cloud-edition`)

`specs/083-cloud-edition/`: spec.md, plan.md (this file), tasks.md,
aee-claims.json (C083-1…19, normalized format), architecture-route-study.md,
decisions-for-owner.md, carryover-touchpoints.md,
amendment-1-workspaces.md, amendment-2-no-staging.md,
amendment-3-glassbreak-email.md, amendment-4-cloud-run-compute.md (historical; superseded by Amendment 5), amendment-5-desktop-tunnel-hosting.md, wireframes 01–11 with desktop + mobile
renders, README.md. Plus a LEDGER.md entry (H1).

**Claims gate**: the bundle validates and assesses under the pinned
AEE 1.5.3 (`aee validate` + `aee assess --no-ledger`); the output goes in
the PR body. No build step starts from an unvalidated bundle.

## Step 1 — cloud foundation (PR: `feat/083-cloud-foundation`)

| Work | Notes |
|---|---|
| Container image (Dockerfile) | Built in Phase 1: the existing backend app + the built SPA in one immutable image. **Amendment 5:** not the production origin — the image/compose fixture remains a local verification artifact only; production runs the desktop install (T052–T055). |
| Cloud configuration switch | Env-driven. Under it, the environment setup/rebuild/upgrade endpoints and the shutdown endpoint are **not registered** (absent, not gated — spec Out of scope, with reasons), and Ollama is neither bundled nor probed. **Amendment 5:** the container is gone, but the exclusion survives as a hosted-route rule on the desktop origin (T056): edge-authenticated requests never reach host-management or shutdown endpoints; the owner's local desktop use is unchanged. |
| Image smoke test | The build verifies `applied-epistemic-engineering` resolves inside the pin ≥1.5.0,<1.6 and runs the GAP-ENV 23-claim regression set (incl. the 0.1625 sign_val expectations) against the image (C083-9). An out-of-pin resolution or a divergent score fails the build. |
| `cloud/edge/` — edge Worker + Durable Object | The plan's chosen layout for the edge layer. The Worker is the perimeter and the session termination point: it sets `X-Robots-Tag: noindex, nofollow` on **every** response, serves a `robots.txt` disallowing all, and routes authenticated traffic through the Durable Object to the single named container instance. **Amendment 5:** the production origin transport is retargeted to the Workers VPC Service binding → named Tunnel → desktop backend (T055); GlossaFront's container role is not the production path. |
| D1 identity schema + migrations | `users` (global type: owner / admin / member / guest), `invites` (hash only — no plaintext code column), `sessions` (hash only), `workspaces`, `workspace_roles` (per-user, per-workspace role), `audit_log` (append-only — no update/delete path), `setup_state`. Identity lives at the edge so auth never depends on the container being awake. |
| R2 dataset-bundle plumbing | Built in Phase 1 (manifest format + verify-then-atomic-swap hydration library). **Amendment 5:** retired from the production design — no bundle, bundle store, or hydration exists; the dataset is desktop-resident and served in place (T057/T058). The Phase 1 record stands as built history. |
| Wrangler configuration | **Production only**, plus ephemeral preview deployments used for verification and torn down after. Amendment 2: no staging project, no staging hostname, ever (C083-14). |
| Deploy workflow (GitHub Actions) | Edge legs after Amendment 5: `wrangler deploy` (Worker + Custom Domain + VPC binding) and D1 migrations, under the repo's existing CI discipline. The compute/image deploy legs (Containers; then Amendment 4's Artifact Registry + Cloud Run) are retired; the desktop origin is configured by T052–T054, not by this workflow. |
| Local production-shaped build | A compose fixture reproducing the edge + a local backend on 127.0.0.1:8001 for Steps 3 and 5's local proofs; it is a verification fixture, not a deployment. **Amendment 5:** production itself is the desktop install behind the Tunnel/VPC route, and Step 5's route-specific proofs (T059) run against the assembled production route before go-live. |


## Step 2 — identity implementation (PR: `feat/083-identity`)

Edge owns identity; the desktop API owns workspace scope. Enforcement is
per-request in both places — no surface trusts a client-supplied role,
workspace, or identity value.

| Work | Claims |
|---|---|
| Invite lifecycle: CSPRNG ≥128-bit codes, stored hashed only, atomic check-and-consume on redemption, default 7-day expiry (admin-adjustable at creation), revocable until redeemed, optional email binding (D-2) and optional workspace grants that become the new user's initial `workspace_roles` | C083-2 |
| Registration surface: account creation exists **only** as invite redemption or the FR-003 setup. No open registration route, form, or API is registered | C083-1 |
| Login / logout; sessions opaque ≥256-bit, hashed at rest, `HttpOnly; Secure; SameSite=Lax` cookie, 30-day sliding lifetime (D-3), revoked instantly on logout, disable, removal, or role/type change | C083-4 |
| Glassbreak setup: the operator seed step prints the one-time setup code in the deploy terminal **only** (single-use, 24-hour expiry; never in git, chat, email, or logs). The seed record carries username `glassbreak` + email `tristen.pierson@gmail.com` (Amendment 3); the owner sets his own password on the setup screen (Argon2id hash in D1 is the only residue). The moment an admin exists, the setup path closes permanently | C083-3 |
| Access model (Amendment 1): global types — **Owner** (singular) / **Admin** / **Member** / **Guest** — crossed with per-workspace roles — **Owner / Admin / Member / Viewer**. A Guest is capped at Viewer in any workspace. Global Admin/Owner hold implicit Workspace Admin everywhere. Workspace creation is global Admin/Owner only (Step 2 admin API; D-1's admins-only rule carried into the workspace model) | C083-5, C083-16, C083-19 |
| Scope enforcement: edge enforces global/admin surfaces; the desktop API enforces workspace scope. A workspace the user does not belong to — and every resource inside it — answers a scoped 404 with no data, enumerated per resource class: claims, digestion, evidence, anchors/data, studies, experiments, jobs, discovery, research-loop, notebooks, reports | C083-5, C083-17, C083-18 |
| Admin API — users: role/type change, disable (the account's sessions die instantly), removal (the account can no longer sign in; attribution on past work is preserved and renders as the removed username, marked removed). Invites: create, list, revoke. Workspaces: create, archive (global Admin/Owner only, C083-16). Per-user workspace-access matrix: read and write a user's full set of workspace grants (C083-19) | C083-5, C083-16, C083-19 |
| Audit: an append-only audit write for **every** FR-012 event — logins (success and failure), invite events, membership/role/type changes, disable/removal, setup, hosted-route configuration changes, admin API denials — with actor and timestamp | C083-12 |
| Attribution: the edge injects the authenticated identity into every desktop-bound request; the desktop API stamps created/modified records with the acting user's id and timestamp. Records created by the owner's local desktop use carry no cloud actor and are never given a fake one | C083-11 |
| Credential separation: the Spec 082 install token is refused at the edge in every position (cookie, header, query). The edge↔desktop-origin service credential is per-deployment, held only in the Worker secret store and the desktop install's protected credential storage, injected by the edge on the VPC binding request, never rendered into any client-visible artifact | C083-8 |
| Terminal: admin-only in the cloud edition (D-5); a member session invoking it receives 403 and the attempt is audit-logged | C083-5 |

**Claim tests** (each maps to a falsifier): registration attempts without a
valid code (form posts, code-shaped guesses) create no account and no
session; one invite redeemed twice / after expiry / after revocation fails
on the second use in every case, and no plaintext code exists in D1, logs,
or the repo; `/setup` and a replayed setup code answer closed (404) once an
admin exists, and an expired code creates nothing; a forged, expired, or
revoked session value authenticates nowhere, and a disabled user's next
request is refused with their session rows gone; the cross-product matrix
(global type × workspace role × resource class) is exercised for every
resource class above — member → admin surface is 403 and audit-logged,
non-member → workspace resource is scoped 404 with no data in the body,
Guest granted a Member workspace role is refused or capped at Viewer;
the 082 token presented in each position yields no authenticated access;
every mutating act by a test user is found stamped with that user's id.

## Step 3 — frontend (PR: `feat/083-frontend`)

Wireframes 01–11 implemented in the SPA's existing design system — no new
visual language: login, invite acceptance, glassbreak setup, admin users,
admin invites, admin audit, the shell with membership + workspace switcher,
account & security, admin workspaces, and the admin user-access matrix.

Carryover deltas from `carryover-touchpoints.md` applied to the 17
carried-over Spec 081 screens, in their approved shapes: the topbar user
chip with account menu; the install chip (desktop install revision · source commit · origin health — Amendment 5's replacement for the retired bundle surface); *Started by* on jobs; actor
rendering on claims, digestion, and evidence ("registered by <username>",
"via desktop import" where there is no cloud actor); membership-filtered
lists **and counts/badges** — a count computed over a workspace the user
cannot see is a leak of exactly the kind C083-18 forbids, so counts are
filtered by the same scope as the lists they summarize.

**Verification**: Playwright screenshots at desktop 1440 and mobile 390,
compared against the approved wireframes screen by screen. Any deviation
stops the step and is reported — it is not improvised around, and no
"verified" claim is made from source checks alone.

## Step 4 — the data-boundary publisher (RETIRED by Amendment 5)

No publisher is built. Amendment 5 retires the bundle design: project
data is resident on the desktop and served in place, so there is
nothing to allowlist, scan, manifest, upload, or hydrate. The
data boundary is restated as FR-006 / C083-6 (desktop residency +
cloud-storage exclusion + authorized-session-only return). Tasks
T030–T033 and T035 are superseded with no replacement; T034's
substance (primary-workspace assignment) is replaced by T057
(scope verification in the desktop dataset), and the production
retirement of the bundle path is T058.


## Step 5 — pre-launch proofs + production go-live (Amendment 2 rollout)

No staging exists, so the proofs run where Amendment 2 puts them: the
local production-shaped build (Step 1) and an ephemeral preview
deployment. Production follows the proofs directly.

| Proof | Claims |
|---|---|
| (a) Full acceptance script — spec User Stories 1–5 **as amended** (setup → invite → member work → admin management → desktop-resident work + offline behavior, Amendment 5's Story 5) — run against the local production-shaped build **and** an ephemeral preview deployment, with the route-specific proofs (T059) run against the assembled production route before go-live; all runs recorded | C083-1…19 (acceptance level) |
| (b) Falsifier suites for C083-1…19 executed as written in `aee-claims.json` **as amended by Amendment 5** (C083-13 is checked as a retirement audit, not a hydration test); every result recorded in the rollout record — a falsified claim stops the rollout, it is not waived | C083-1…19 |
| (c) Fresh adversarial pass over the auth surface: invite brute force / code guessing; session fixation; role escalation (member→admin, guest→member-role grant, cross-workspace id probing for **every** resource class in Step 2); anonymous payload scan — anonymous fetches of the shell and its assets must contain no project data, names, or counts, and every non-public route answers redirect-to-login or 401; **Amendment 5 adds** direct-origin/bypass probes (no public route reaches the desktop backend except through the edge) and a Tunnel/VPC configuration audit (no published application for the hostname; no `glossa` CNAME to `<UUID>.cfargotunnel.com`) | C083-2, C083-4, C083-5, C083-17, C083-18 |
| (d) Noindex checks across response types — pages, API responses, error responses, static assets — each carrying `X-Robots-Tag: noindex, nofollow`, plus `robots.txt` disallowing all; the edge's desktop-offline 503 is one of the sampled error responses | C083-7 |
| (e) **Production deploy** to `glossa.bitconcepts.tech`. **Restated by Amendment 5 (2026-10-30).** Three named gates, all required: **(a)** Spec 080 cutover-final — the hosted route rides the production desktop install; **(b)** BitConcepts Cloudflare write/configuration scopes (DNS / Worker Custom Domain, Workers + D1 deploys, a Tunnel write scope, and the Workers VPC roles — Connectivity Directory Admin + Bind) through the venue that owns the account; **(c)** the `cloudflared` desktop service installed through Desktop Access's screened service path. The Amendment 4 Google Cloud gate is **dead**. The rollout waits at these gates until all three are in hand; nothing substitutes for them | C083-14 |
| (f) Glassbreak setup prompt: the one-time setup code and `https://glossa.bitconcepts.tech` are delivered to the owner through the coordinator; the owner sets his own password at `/setup`. The code travels by that channel only — it is not written into the rollout record, git, or email | C083-3 |
| (g) Rollout record (proofs, falsifier results, desktop install revision/source commit, Tunnel ID, VPC Service ID, Worker Custom Domain state, the go-live timestamp) + LEDGER.md entry (H1) | — |

## Risks and guards

| Risk | Guard |
|---|---|
| Base spec text (staging, "programs") read without the amendments | The reading note above; Amendment 2 forbids creating any staging resource, and Step 1's wrangler config carries production + ephemeral previews only (C083-14) |
| A count or badge leaks a workspace a user cannot see | Counts/badges are scope-filtered with the lists they summarize, and the adversarial pass probes for exactly this (C083-18) |
| Restricted material is copied into cloud storage, or served outside an authenticated, workspace-authorized session | No copy path exists: the data is desktop-resident, the edge stores identity data only, and Step 5 audits the cloud side (D1, Worker storage/configuration) for project artifacts while probing the route for unauthorized returns (C083-6 as restated) |
| The desktop or tunnel is offline and stale or cached project data keeps serving | The edge caches no project data and there is no cloud dataset to serve: a failed VPC fetch becomes the edge's own noindex 503 with no project content, proven with the backend stopped and with the tunnel stopped (T059) |
| A job is silently lost across a desktop-backend restart | Job state lives in the desktop-resident dataset and the resident engine's stall semantics fail the job *with the reason recorded* (C083-10 as revised by Amendment 5); the restart case is in the acceptance script (Story 5) |
| The 082 desktop token becomes a second cloud credential by accident | Refused at the edge in every position, tested in Step 2 and re-probed in Step 5's adversarial pass (C083-8) |
| A second dataset is created by accident (a bundle, a store, a sync) and diverges from the desktop's | There is one dataset, on the desktop; the production configuration carries no bundle store or publisher (T058), and the C083-6 audit + C083-13 retirement audit check that none appears |
