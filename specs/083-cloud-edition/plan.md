# Plan: Glossa Lab Cloud Edition — Accounts, Workspaces, Hosted Tool (Spec 083)

Claims first (Step 0, this PR), then five build steps, each landing green on
its own under the repo discipline (genuine CI from per-job conclusions, C4
freeze gate included; branches deleted on merge). Nothing here changes the
desktop edition. Production go-live is Step 5 and follows the pre-launch
proofs directly — there is no staging deployment at any point.

**Reading note — amendments govern.** Amendments 1–4 supersede the base
spec and decisions file wherever they conflict: Amendment 1 replaces the
spec's program-membership model with **workspaces** (global user types
crossed with per-workspace roles) and adds claims C083-15…19; Amendment 2
deletes FR-014's staging-first rollout, D-7's staging hostname, and every
"staging" reference in the design summary and claim C083-14 — production
only, verified on a local production-shaped build and ephemeral preview
deployments; Amendment 3 fixes the glassbreak seed record (username
`glassbreak`, email `tristen.pierson@gmail.com`). Where the base text says
"program," read "workspace" in the amended sense.

## Step 0 — spec adoption (PR: `spec/083-cloud-edition`)

`specs/083-cloud-edition/`: spec.md, plan.md (this file), tasks.md,
aee-claims.json (C083-1…19, normalized format), architecture-route-study.md,
decisions-for-owner.md, carryover-touchpoints.md,
amendment-1-workspaces.md, amendment-2-no-staging.md,
amendment-3-glassbreak-email.md, wireframes 01–11 with desktop + mobile
renders, README.md. Plus a LEDGER.md entry (H1).

**Claims gate**: the bundle validates and assesses under the pinned
AEE 1.5.3 (`aee validate` + `aee assess --no-ledger`); the output goes in
the PR body. No build step starts from an unvalidated bundle.

## Step 1 — cloud foundation (PR: `feat/083-cloud-foundation`)

| Work | Notes |
|---|---|
| Container image (Dockerfile) | Builds the existing backend app + the built SPA into one immutable image — no mutation of the running instance, ever. |
| Cloud configuration switch | Env-driven. Under it, the environment setup/rebuild/upgrade endpoints and the shutdown endpoint are **not registered** (absent, not gated — spec Out of scope, with reasons), and Ollama is neither bundled nor probed: the provider reports offline exactly as on a desktop without Ollama. |
| Image smoke test | The build verifies `applied-epistemic-engineering` resolves inside the pin ≥1.5.0,<1.6 and runs the GAP-ENV 23-claim regression set (incl. the 0.1625 sign_val expectations) against the image (C083-9). An out-of-pin resolution or a divergent score fails the build. |
| `cloud/edge/` — edge Worker + Durable Object | The plan's chosen layout for the edge layer. The Worker is the perimeter and the session termination point: it sets `X-Robots-Tag: noindex, nofollow` on **every** response, serves a `robots.txt` disallowing all, and routes authenticated traffic through the Durable Object to the single named container instance. |
| D1 identity schema + migrations | `users` (global type: owner / admin / member / guest), `invites` (hash only — no plaintext code column), `sessions` (hash only), `workspaces`, `workspace_roles` (per-user, per-workspace role), `audit_log` (append-only — no update/delete path), `setup_state`. Identity lives at the edge so auth never depends on the container being awake. |
| R2 dataset-bundle plumbing | Manifest format: bundle id, build time, source commit, per-artifact SHA-256. Hydration library: verify the **full** manifest before swap, swap atomically, never serve a mixture of two manifests (C083-13). Hydration restores job state before the engine resumes, and the instance's sleep is suppressed while jobs run (FR-010, C083-10). **Amendment 4**: jobs move to Cloud Run Job executions (T047) — the sleep-suppression mechanism is superseded; the bundle transport gains a GCS adapter (T045) and R2 is never enabled in production. |
| Wrangler configuration | **Production only**, plus ephemeral preview deployments used for verification and torn down after. Amendment 2: no staging project, no staging hostname, ever (C083-14). |
| Deploy workflow (GitHub Actions) | Image build/push to the Cloudflare container registry, `wrangler deploy`, D1 migrations — following the repo's existing CI discipline. **Amendment 4**: the compute leg retargets — Artifact Registry push + Cloud Run deploy (service + Jobs, T049); the wrangler legs are unchanged. |
| Local production-shaped build | A compose file reproducing the production topology (edge, container, D1/R2 stand-ins — Amendment 4: the storage stand-in becomes the GCS adapter's local fake, T045) on one machine. Steps 3 and 5 run their proofs against it; it is a verification fixture, not a deployment. |

## Step 2 — identity implementation (PR: `feat/083-identity`)

Edge owns identity; the container owns workspace scope. Enforcement is
per-request in both places — no surface trusts a client-supplied role,
workspace, or identity value.

| Work | Claims |
|---|---|
| Invite lifecycle: CSPRNG ≥128-bit codes, stored hashed only, atomic check-and-consume on redemption, default 7-day expiry (admin-adjustable at creation), revocable until redeemed, optional email binding (D-2) and optional workspace grants that become the new user's initial `workspace_roles` | C083-2 |
| Registration surface: account creation exists **only** as invite redemption or the FR-003 setup. No open registration route, form, or API is registered | C083-1 |
| Login / logout; sessions opaque ≥256-bit, hashed at rest, `HttpOnly; Secure; SameSite=Lax` cookie, 30-day sliding lifetime (D-3), revoked instantly on logout, disable, removal, or role/type change | C083-4 |
| Glassbreak setup: the operator seed step prints the one-time setup code in the deploy terminal **only** (single-use, 24-hour expiry; never in git, chat, email, or logs). The seed record carries username `glassbreak` + email `tristen.pierson@gmail.com` (Amendment 3); the owner sets his own password on the setup screen (Argon2id hash in D1 is the only residue). The moment an admin exists, the setup path closes permanently | C083-3 |
| Access model (Amendment 1): global types — **Owner** (singular) / **Admin** / **Member** / **Guest** — crossed with per-workspace roles — **Owner / Admin / Member / Viewer**. A Guest is capped at Viewer in any workspace. Global Admin/Owner hold implicit Workspace Admin everywhere. Workspace creation is global Admin/Owner only (Step 2 admin API; D-1's admins-only rule carried into the workspace model) | C083-5, C083-16, C083-19 |
| Scope enforcement: edge enforces global/admin surfaces; the container API enforces workspace scope. A workspace the user does not belong to — and every resource inside it — answers a scoped 404 with no data, enumerated per resource class: claims, digestion, evidence, anchors/data, studies, experiments, jobs, discovery, research-loop, notebooks, reports | C083-5, C083-17, C083-18 |
| Admin API — users: role/type change, disable (the account's sessions die instantly), removal (the account can no longer sign in; attribution on past work is preserved and renders as the removed username, marked removed). Invites: create, list, revoke. Workspaces: create, archive (global Admin/Owner only, C083-16). Per-user workspace-access matrix: read and write a user's full set of workspace grants (C083-19) | C083-5, C083-16, C083-19 |
| Audit: an append-only audit write for **every** FR-012 event — logins (success and failure), invite events, membership/role/type changes, disable/removal, setup, publishes, admin API denials — with actor and timestamp | C083-12 |
| Attribution: the edge injects the authenticated identity into every container request; the container stamps created/modified records with the acting user's id and timestamp. Records arriving via bundle without a cloud actor are labelled "via desktop import," never given a fake author | C083-11 |
| Credential separation: the Spec 082 install token is refused at the edge in every position (cookie, header, query). The edge↔container service credential is per-deployment, held only in platform secret stores, injected by the edge, never rendered into any client-visible artifact | C083-8 |
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
chip with account menu; the dataset chip (bundle id · source commit ·
hydrated at — C083-13's honesty surface); *Started by* on jobs; actor
rendering on claims, digestion, and evidence ("registered by <username>",
"via desktop import" where there is no cloud actor); membership-filtered
lists **and counts/badges** — a count computed over a workspace the user
cannot see is a leak of exactly the kind C083-18 forbids, so counts are
filtered by the same scope as the lists they summarize.

**Verification**: Playwright screenshots at desktop 1440 and mobile 390,
compared against the approved wireframes screen by screen. Any deviation
stops the step and is reported — it is not improvised around, and no
"verified" claim is made from source checks alone.

## Step 4 — the data-boundary publisher (PR: `feat/083-cloud-publish`)

`tools/cloud-publish/` — the plan's chosen layout; the builder works
home-side (repo/desktop), never in the cloud.

| Work | Claims |
|---|---|
| Allowlist configuration: publishable tables + publishable checkout paths. Anything not allowlisted does not ship — the allowlist is the primary control | C083-6 |
| Structural exclusion of the restricted stores (raw scan directories, page previews, restricted folders): they are outside the builder's reach by construction, not filtered after collection | C083-6 |
| Restricted-marker scan: the maintained restricted-marker list file (its patterns are publishable; the restricted content is not) is scanned over **every** artifact before upload. A failed scan uploads nothing | C083-6 |
| Manifest emission + bundle-store upload in the Step 1 bundle format (**Amendment 4**: Google Cloud Storage); the publish is recorded as an auditable event with its scan-gate result as a first-class report line | C083-6, C083-13 |
| Planted-canary test, wired into CI: a restricted marker planted in a publishable source must fail the publish. If the canary ever ships, the boundary claim is falsified and the step is not done | C083-6 |
| Primary-workspace seeding: the bundle assigns **all** existing project state to the seeded "Indus Script" workspace; the publish report reconciles per-class counts (claims, digestion, evidence, anchors/data, studies, experiments, jobs, discovery, research-loop, notebooks, reports) against the source. A count mismatch fails the publish report, loudly | C083-15 |
| Export / reviewed import: tooling to bring cloud-side changes home as an inspected diff (summary by table and file) the owner triggers and reviews — never an auto-sync (D-4) | — (D-4) |

## Step 5 — pre-launch proofs + production go-live (Amendment 2 rollout)

No staging exists, so the proofs run where Amendment 2 puts them: the
local production-shaped build (Step 1) and an ephemeral preview
deployment. Production follows the proofs directly.

| Proof | Claims |
|---|---|
| (a) Full acceptance script — spec User Stories 1–5 **as amended by the workspace model** (setup → invite → member work → admin management → dataset publish/hydration) — run against the local production-shaped build **and** an ephemeral preview deployment; both runs recorded | C083-1…19 (acceptance level) |
| (b) Falsifier suites for C083-1…19 executed as written in `aee-claims.json`; every result recorded in the rollout record — a falsified claim stops the rollout, it is not waived | C083-1…19 |
| (c) Fresh adversarial pass over the auth surface: invite brute force / code guessing; session fixation; role escalation (member→admin, guest→member-role grant, cross-workspace id probing for **every** resource class in Step 2); anonymous payload scan — anonymous fetches of the shell and its assets must contain no project data, names, or counts, and every non-public route answers redirect-to-login or 401 | C083-2, C083-4, C083-5, C083-17, C083-18 |
| (d) Noindex checks across response types — pages, API responses, error responses, static assets — each carrying `X-Robots-Tag: noindex, nofollow`, plus `robots.txt` disallowing all | C083-7 |
| (e) **Production deploy** to `glossa.bitconcepts.tech`. **Restated by Amendment 4 (2026-10-30).** Named external gate: the owner's **Google Cloud account + project with billing enabled** (Free Tier) — an owner act at deploy time that nothing earlier requires — with the deploy's spend-cap budget set, plus BitConcepts Cloudflare write access (the DNS record, Workers/D1 deploys; no paid plan, no R2). The rollout waits at this gate until both are in hand; nothing substitutes for them | C083-14 |
| (f) Glassbreak setup prompt: the one-time setup code and `https://glossa.bitconcepts.tech` are delivered to the owner through the coordinator; the owner sets his own password at `/setup`. The code travels by that channel only — it is not written into the rollout record, git, or email | C083-3 |
| (g) Rollout record (proofs, falsifier results, deployed bundle/image identity, the go-live timestamp) + LEDGER.md entry (H1) | — |

## Risks and guards

| Risk | Guard |
|---|---|
| Base spec text (staging, "programs") read without the amendments | The reading note above; Amendment 2 forbids creating any staging resource, and Step 1's wrangler config carries production + ephemeral previews only (C083-14) |
| A count or badge leaks a workspace a user cannot see | Counts/badges are scope-filtered with the lists they summarize, and the adversarial pass probes for exactly this (C083-18) |
| Restricted material reaches the bundle store through a gap in the marker list (Amendment 4; R2 in the original text) | The list is the second control, not the first: allowlist + structural exclusion stand in front of it, and the planted-canary test runs in CI on every publish-path change (C083-6) |
| Hydration leaves a mixed dataset after an interrupted transfer | Full-manifest verification before an atomic swap; the served dataset is always exactly one manifest (C083-13) |
| A job is silently lost across container sleep/restart | Job state lives in the dataset, hydration restores it before the engine resumes, sleep is suppressed while jobs run, and stall semantics fail the job *with the reason recorded* (C083-10). **Amendment 4**: the mechanism is restated — Job executions + state journal + scheduled stall watchdog; the guarantee is unchanged |
| The 082 desktop token becomes a second cloud credential by accident | Refused at the edge in every position, tested in Step 2 and re-probed in Step 5's adversarial pass (C083-8) |
| Cloud and desktop datasets diverge silently | Cloud work is a branch, not a fork: changes come home only as an owner-reviewed import diff, never an auto-sync (D-4) |
