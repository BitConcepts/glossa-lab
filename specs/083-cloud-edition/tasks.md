# Tasks: Glossa Lab Cloud Edition — Accounts, Workspaces, Hosted Tool (Spec 083)

Amendments 1–5 govern where they conflict with the base spec
(workspaces, not programs; no staging, ever; the glassbreak seed
email; Amendment 4's Cloud Run + GCS route **superseded in full by
Amendment 5**: desktop origin via Cloudflare Tunnel + Workers VPC;
no cloud dataset). Every task names its claim(s) or the FR /
decision it discharges.


## Step 0 — spec adoption (PR: `spec/083-cloud-edition`)

- [x] T001 Spec package: spec.md (problem, Stories 1–5, FR-001…017 as amended), plan.md, tasks.md, aee-claims.json (C083-1…19 with evidence + falsifiers, normalized format)
- [x] T002 Companion documents: architecture-route-study.md (route evidence), decisions-for-owner.md (D-0…D-7), carryover-touchpoints.md (deltas for the 17 carried-over screens)
- [x] T003 Amendments: amendment-1-workspaces.md (access model, C083-15…19), amendment-2-no-staging.md (production-only rollout, C083-14 as amended), amendment-3-glassbreak-email.md (seed record, C083-3)
- [x] T004 Wireframes 01–11 + desktop 1440 / mobile 390 renders, approved; README.md for the package
- [x] T005 Claims bundle verified: validates + assesses under the pinned AEE 1.5.3 (`aee validate` + `aee assess --no-ledger`), output recorded in the PR body; LEDGER.md entry (H1)

## Step 1 — cloud foundation (PR: `feat/083-cloud-foundation`)

- [x] T006 Container image: Dockerfile builds the existing backend app + built SPA as one immutable image; image identity recorded for the rollout record (C083-9)
- [x] T007 Cloud configuration switch (env-driven): under it the env setup/rebuild/upgrade endpoints and the shutdown endpoint are not registered, and Ollama is not bundled or probed (spec Out of scope; FR-010's instance lifecycle)
- [x] T008 Image smoke test: build verifies `applied-epistemic-engineering` resolves within ≥1.5.0,<1.6 and runs the GAP-ENV 23-claim regression set against the image; out-of-pin or divergent score fails the build (C083-9)
- [x] T009 `cloud/edge/`: edge Worker + Durable Object front — `X-Robots-Tag: noindex, nofollow` on every response, `robots.txt` disallowing all, session termination point, routing to the single container instance (C083-7, C083-4) — **Amendment 5:** the container origin is superseded prospectively; the production origin transport is T055 (Workers VPC binding → named Tunnel → desktop). The Phase 1 build record stands
- [x] T010 D1 identity schema + migrations: `users` (global type owner/admin/member/guest), `invites` (hash only), `sessions` (hash only), `workspaces`, `workspace_roles`, `audit_log` (append-only), `setup_state` (C083-2, C083-4, C083-12, C083-16, C083-19)
- [x] T011 R2 bundle plumbing: manifest format (bundle id, build time, source commit, per-artifact SHA-256); hydration library verifies the full manifest and swaps atomically — never a mixture (C083-13); job state restored before the engine resumes, sleep suppressed while jobs run (C083-10) — **Amendment 4:** GCS adapter/R2-never-enabled notes superseded in turn by **Amendment 5:** the bundle/hydration production path is retired (T058); C083-13 is superseded; the Phase 1 plumbing remains as built history and test material only

- [x] T012 Wrangler configuration: production only + ephemeral preview deployments for verification; no staging project and no staging hostname created (Amendment 2, C083-14)
- [x] T013 GitHub Actions deploy workflow (image build/push to the Cloudflare container registry, wrangler deploy, D1 migrations) under the repo's existing CI discipline; local production-shaped build (compose file) for later steps' proofs; LEDGER.md entry — **Amendment 5:** the compute/image deploy legs are retired prospectively; the surviving legs are the edge deploy (Worker + Custom Domain + VPC binding) and D1 migrations (T053–T055)


## Step 2 — identity implementation (PR: `feat/083-identity`)

- [ ] T014 Invite lifecycle: CSPRNG ≥128-bit, hash-stored only, atomic check-and-consume, default 7-day expiry, revocable, optional email + workspace grants (C083-2, FR-002, D-2)
- [ ] T015 Registration only via invite redemption or setup; no open registration route, form, or API registered (C083-1, FR-001)
- [ ] T016 Login/logout; sessions opaque ≥256-bit, hashed at rest, `HttpOnly; Secure; SameSite=Lax` cookie, 30-day sliding (D-3), instant revocation on logout/disable/removal/role change (C083-4, FR-004)
- [ ] T017 Glassbreak setup: operator seed step prints the one-time setup code in the deploy terminal only (single-use, 24 h); seed record carries username `glassbreak` + email `tristen.pierson@gmail.com` (Amendment 3); owner sets his own password on the setup screen; setup path permanently closes when an admin exists (C083-3, FR-003)
- [ ] T018 Access model: global types (Owner singular / Admin / Member / Guest) × per-workspace roles (Owner / Admin / Member / Viewer); Guest capped at Viewer; global Admin/Owner hold implicit Workspace Admin (C083-5, C083-19; Amendment 1)
- [ ] T019 Scope enforcement: edge for global/admin surfaces, desktop API for workspace scope; scoped 404s with no data for every resource class — claims, digestion, evidence, anchors/data, studies, experiments, jobs, discovery, research-loop, notebooks, reports (C083-5, C083-17, C083-18)
- [ ] T020 Admin API — users (role/type change, disable with instant session death, removal preserving attribution) and invites (create, list, revoke) (C083-5, C083-4, C083-11)
- [ ] T021 Admin API — workspaces (create/archive, global Admin/Owner only) and the per-user workspace-access matrix (read/write a user's full grant set) (C083-16, C083-19)
- [ ] T022 Audit: append-only writes for every FR-012 event (logins success/failure, invite events, role/type and membership changes, disable/removal, setup, hosted-route configuration changes, admin API denials), actor + timestamp on each (C083-12)
- [ ] T023 Attribution: edge injects the authenticated identity on every desktop-bound request; the desktop API stamps mutating records with actor id + timestamp; records created by the owner's local desktop use carry no cloud actor and are never given a fake one (C083-11, FR-011)

- [ ] T024 Credential separation tests: the Spec 082 install token refused at the edge in every position (cookie, header, query); edge↔desktop-origin service credential only in the Worker secret store and the desktop install's protected credential storage, in no client-visible artifact (C083-8, FR-008); terminal admin-only in the hosted edition, member attempts 403 + audit-logged (C083-5, D-5); claim-test matrix from the plan (Step 2) green; LEDGER.md entry


## Step 3 — frontend (PR: `feat/083-frontend`)

- [ ] T025 Wireframes 01–06 in the SPA's existing design system: login, invite acceptance, glassbreak setup, admin users, admin invites, admin audit (C083-1, C083-2, C083-3, C083-12)
- [ ] T026 Wireframes 07–11: shell with membership + workspace switcher, account & security, admin workspaces, admin user-access matrix (C083-5, C083-16, C083-19)
- [ ] T027 Carryover deltas on the 17 carried-over screens per carryover-touchpoints.md: user chip, install chip (desktop install revision · source commit · origin health — Amendment 5's replacement for the retired dataset/bundle chip), *Started by* on jobs, actor rendering on claims/digestion/evidence (C083-11; C083-13 superseded)

- [ ] T028 Membership filtering applied to lists **and** counts/badges — no count computed over a workspace the user cannot see (C083-18)
- [ ] T029 Verification: Playwright screenshots at desktop 1440 + mobile 390 compared against the approved wireframes screen by screen; any deviation stops the step and is reported, not improvised around; LEDGER.md entry

## Step 4 — the data-boundary publisher (RETIRED by Amendment 5)

No publisher is built: the dataset is desktop-resident and served in
place, so there is nothing to allowlist, scan, manifest, upload, or
hydrate. The tasks below are superseded, not open work.

- [ ] T030 **SUPERSEDED by Amendment 5** — the `tools/cloud-publish/` builder is not built; the data boundary is FR-006/C083-6 as restated (desktop residency + cloud-storage exclusion). No replacement
- [ ] T031 **SUPERSEDED by Amendment 5** — the restricted-marker scan over bundle artifacts is retired with the bundle; the boundary is enforced by residency and audited under T059. No replacement
- [ ] T032 **SUPERSEDED by Amendment 5** — no manifest is emitted and no bundle store exists (R2 or GCS). No replacement
- [ ] T033 **SUPERSEDED by Amendment 5** — the planted-canary publish test is retired; its intent (prove the boundary mechanically) is carried by the C083-6 cloud-storage audit and unauthorized-return probes in T059
- [ ] T034 **SUPERSEDED by Amendment 5** — primary-workspace assignment is not a publish step; replaced by T057 (scope verification in the desktop-resident dataset) (C083-15)
- [ ] T035 **SUPERSEDED by Amendment 5** — export/reviewed-import tooling is not built; D-4's two-datasets premise is retired (one desktop dataset). No replacement


## Step 5 — pre-launch proofs + production go-live (Amendment 2 rollout; no staging)

- [ ] T036 Acceptance script (Stories 1–5 as amended, incl. Amendment 5's desktop-resident/offline Story 5) run against the local production-shaped build **and** an ephemeral preview deployment, with the route-specific proofs of T059 run against the assembled production route before go-live; all runs recorded (C083-1…19)

- [ ] T037 Falsifier suites for C083-1…19 executed as written; results recorded in the rollout record; a falsified claim stops the rollout (C083-1…19, as amended by Amendment 5; C083-13 is executed as a retirement audit, not a hydration test)
- [ ] T038 Adversarial pass over the auth surface: invite brute force / code guessing, session fixation, role escalation (member→admin, guest→member-role grant, cross-workspace id probing for every Step 2 resource class) (C083-2, C083-4, C083-5, C083-17, C083-18)
- [ ] T039 Anonymous payload scan: anonymous fetches of the shell and assets contain no project data, names, or counts; every non-public route answers redirect-to-login or 401 — run against the local build and, under T059, against the real Tunnel/VPC route (C083-4, C083-18)

- [ ] T040 Noindex checks across response types (pages, API, errors — including the edge's desktop-offline 503 — assets) — `X-Robots-Tag: noindex, nofollow` on each — plus `robots.txt` disallowing all (C083-7, FR-007)

- [ ] T041 External gates + production deploy: Amendment 5's three gates in hand — (a) Spec 080 cutover-final (the hosted route rides the production desktop install), (b) BitConcepts Cloudflare write/configuration scopes (DNS / Worker Custom Domain, Workers + D1 deploys, a Tunnel write scope, Connectivity Directory Admin + Bind for Workers VPC), (c) the `cloudflared` desktop service installed via Desktop Access's screened service path — then deploy to `glossa.bitconcepts.tech`; production follows the proofs directly, no staging-proof gate. **The Amendment 4 Google Cloud gate is dead** (C083-14; Amendments 2 + 5)

- [ ] T042 Glassbreak setup prompt: the one-time setup code + `https://glossa.bitconcepts.tech` delivered to the owner through the coordinator only; owner sets his own password at `/setup` (C083-3)
- [ ] T043 Rollout record (proofs, falsifier results, desktop install revision/source commit, Tunnel ID, VPC Service ID, Worker Custom Domain state, go-live timestamp) + LEDGER.md entry (H1)


## Amendment 4 — Cloud Run delta (SUPERSEDED in full by Amendment 5, 2026-10-30)

Amendment 4's route is retired: no Cloud Run service or Jobs, no
Artifact Registry deploy, no Google Cloud Storage. The tasks below
are superseded, not open work; their replacements are the Amendment 5
tasks that follow.

- [ ] T044 **SUPERSEDED by Amendment 5** — the Cloud Run image contract / runner entrypoint is not built; the resident desktop application needs neither. No replacement
- [ ] T045 **SUPERSEDED by Amendment 5** — no GCS bundle adapter; the bundle production path is retired by T058
- [ ] T046 **SUPERSEDED by Amendment 5** — no Cloud Run service definition; replaced by T052–T054 (desktop service, Tunnel/VPC configuration, Worker Custom Domain)
- [ ] T047 **SUPERSEDED by Amendment 5** — no Cloud Run Jobs or Scheduler definitions; jobs run in the resident desktop engine (C083-10 as revised). No replacement
- [ ] T048 **SUPERSEDED by Amendment 5** — the edge retarget to a `*.run.app` origin is replaced by T055 (retarget to the Workers VPC Service binding)
- [ ] T049 **SUPERSEDED by Amendment 5** — no Artifact Registry / Workload Identity Federation deploy leg; the surviving workflow legs are the edge deploy and D1 migrations (T053–T055)
- [ ] T050 **SUPERSEDED by Amendment 5** — the Cloud Run proof deltas (cold start, SIGTERM journal flush, Job execution) are replaced by T059 (route, offline, and bypass proofs)
- [ ] T051 **SUPERSEDED by Amendment 5** — Amendment 4's records task is replaced by T060

## Amendment 5 — Desktop origin via Cloudflare Tunnel + Workers VPC (owner decision, 2026-10-30)

The hosted edition's origin is the Spec 080 production desktop
install on TRISTEN-DESKTOP; the edge reaches it through a named
Cloudflare Tunnel consumed through a Workers VPC Service binding
(amendment-5-desktop-tunnel-hosting.md). Suggested vehicle: one
follow-on PR for T053–T056 + T058 (repo-side configuration and code),
with T052 and the Cloudflare-side parts of T053/T054 executed as the
coordination steps they name, T057 in the Step 2/4 line, and
T059–T060 folding into Step 5 and the rollout record.

- [ ] T052 `cloudflared` as a durable desktop service (repo pattern + coordination): extend the repo's setup-os pattern with the cloudflared companion for the named tunnel `glossa-desktop` (install/status/uninstall surface in the same shape as the existing Windows integration; the tunnel token is handled only on the desktop and never appears in the repo, logs, or chat). **Coordination step:** the actual service installation/registration on TRISTEN-DESKTOP is executed only through the Desktop Access venue's screened service path, under the sole-registrar regime for desktop task/service registration — this spec's build does not install it directly. Acceptance: the venue's record shows the service installed and the tunnel connected/healthy after a logon cycle (C083-14)
- [ ] T053 Tunnel + Workers VPC configuration as code/checklist: create the named, remotely managed tunnel `glossa-desktop`; register exactly one HTTP VPC Service `glossa-desktop-origin` (that tunnel's ID; host IPv4 `127.0.0.1`; HTTP port `8001`; no HTTPS port); record the Tunnel ID and VPC Service ID for the rollout record (never the token); the checklist asserts **no published application route and no ingress hostname** exists for `glossa.bitconcepts.tech`, and carries the token-rotation procedure (Amendment 5 §2.3) (C083-8, C083-14)
- [ ] T054 Worker Custom Domain + DNS verification: deploy the edge with `glossa.bitconcepts.tech` as a Worker Custom Domain (the wrangler route already declares `custom_domain = true`); verify the Cloudflare-created DNS records point to the Worker and the certificate is active; verify there is **no `glossa` CNAME to `<UUID>.cfargotunnel.com`** and no published Tunnel application for the hostname. Executed under go-live gate (b) (DNS + Tunnel + VPC scopes) (C083-14)
- [ ] T055 Edge origin retarget (container/run.app → Workers VPC binding): production wrangler configuration carries a `vpc_services` binding `GLOSSA_ORIGIN` for the T053 service and no container or Cloud Run origin; the Worker calls the binding's `fetch()` only after session termination and route authorization (anonymous traffic only for the exact public surface), strips client-supplied `X-Glossa-*` headers, injects the service credential and (for authenticated requests) the identity headers, and preserves method/path/query/body and streaming responses; a failed VPC fetch becomes the edge's own noindex 503 with no project data, and project-data responses are not cached; GlossaFront's container role is retired from the production request path; edge tests gain a fake VPC binding seam mirroring the former front seam (C083-8, C083-4, C083-7)
- [ ] T056 Desktop acceptance of edge-injected identity (the app side of C083-8 in this topology): the desktop backend accepts `X-Glossa-*` identity only on a request carrying the valid per-deployment service credential (the desktop's copy held in protected credential storage, provisioned through the venue coordination of T052; the value never enters the repo, logs, or chat); identity headers without the credential confer nothing, and local use continues under the Spec 082 token, unchanged; edge-authenticated requests cannot reach the shutdown or environment setup/rebuild/upgrade endpoints, whatever the role; the terminal remains global Admin/Owner only; attribution stamping per FR-011 (C083-8, C083-5, C083-11)
- [ ] T057 Desktop-resident primary-workspace scope (replaces T034): in the Spec 080 production dataset, the primary workspace "Indus Script" exists and **all** existing project state carries its scope; a reconciliation report compares per-class counts (claims, digestion, evidence, anchors/data, studies, experiments, jobs, discovery, research-loop, notebooks, reports) against the desktop dataset itself and fails loudly on any unscoped or misassigned resource; no resource is served unscoped through the hosted route (C083-15)
- [ ] T058 Retire the bundle production path (replaces T045 and Step 4): R2/GCS transports, the publisher, and hydration have no production role — production configuration (wrangler bindings, deploy workflow) carries no bundle store, bucket, or publish leg, and a config-guard test asserts it; Phase 1 bundle code may remain for tests/history but must be unreachable from the production configuration; code deletion, if wanted, is a separate later task (C083-6, C083-13 as superseded)
- [ ] T059 Go-live proof deltas on the real route (replaces T050): anonymous-fetch login-wall scan and payload scan against `glossa.bitconcepts.tech` on the assembled route; noindex sweep including the offline 503; an authenticated member happy path Worker → VPC → Tunnel → desktop, including one streaming (SSE) surface and one job carried to a terminal state; workspace-scope probes; **desktop-backend-stopped** and **tunnel-stopped** tests (edge answers its own 503; no project data; no cached dataset); bypass probes (forged `X-Glossa-*` headers direct to the origin path, the Spec 082 token presented at the edge, any alternate public route to the backend); and the C083-6 cloud-storage audit (D1 and Worker storage/configuration hold no project artifacts) (C083-4, C083-6, C083-7, C083-8, C083-10, C083-14, C083-18)
- [ ] T060 Records (replaces T051): the rollout record carries the Tunnel ID, the VPC Service ID, the Worker Custom Domain state, the desktop install revision/source commit, the proof results, and the go-live timestamp; LEDGER.md entry for Amendment 5 and this delta (H1)
