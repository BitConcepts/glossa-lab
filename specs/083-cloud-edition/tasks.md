# Tasks: Glossa Lab Cloud Edition — Accounts, Workspaces, Hosted Tool (Spec 083)

Amendments 1–3 govern where they conflict with the base spec (workspaces,
not programs; no staging, ever; the glassbreak seed email). Every task names
its claim(s) or the FR / decision it discharges.

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
- [x] T009 `cloud/edge/`: edge Worker + Durable Object front — `X-Robots-Tag: noindex, nofollow` on every response, `robots.txt` disallowing all, session termination point, routing to the single container instance (C083-7, C083-4)
- [x] T010 D1 identity schema + migrations: `users` (global type owner/admin/member/guest), `invites` (hash only), `sessions` (hash only), `workspaces`, `workspace_roles`, `audit_log` (append-only), `setup_state` (C083-2, C083-4, C083-12, C083-16, C083-19)
- [x] T011 R2 bundle plumbing: manifest format (bundle id, build time, source commit, per-artifact SHA-256); hydration library verifies the full manifest and swaps atomically — never a mixture (C083-13); job state restored before the engine resumes, sleep suppressed while jobs run (C083-10)
- [x] T012 Wrangler configuration: production only + ephemeral preview deployments for verification; no staging project and no staging hostname created (Amendment 2, C083-14)
- [x] T013 GitHub Actions deploy workflow (image build/push to the Cloudflare container registry, wrangler deploy, D1 migrations) under the repo's existing CI discipline; local production-shaped build (compose file) for later steps' proofs; LEDGER.md entry

## Step 2 — identity implementation (PR: `feat/083-identity`)

- [ ] T014 Invite lifecycle: CSPRNG ≥128-bit, hash-stored only, atomic check-and-consume, default 7-day expiry, revocable, optional email + workspace grants (C083-2, FR-002, D-2)
- [ ] T015 Registration only via invite redemption or setup; no open registration route, form, or API registered (C083-1, FR-001)
- [ ] T016 Login/logout; sessions opaque ≥256-bit, hashed at rest, `HttpOnly; Secure; SameSite=Lax` cookie, 30-day sliding (D-3), instant revocation on logout/disable/removal/role change (C083-4, FR-004)
- [ ] T017 Glassbreak setup: operator seed step prints the one-time setup code in the deploy terminal only (single-use, 24 h); seed record carries username `glassbreak` + email `tristen.pierson@gmail.com` (Amendment 3); owner sets his own password on the setup screen; setup path permanently closes when an admin exists (C083-3, FR-003)
- [ ] T018 Access model: global types (Owner singular / Admin / Member / Guest) × per-workspace roles (Owner / Admin / Member / Viewer); Guest capped at Viewer; global Admin/Owner hold implicit Workspace Admin (C083-5, C083-19; Amendment 1)
- [ ] T019 Scope enforcement: edge for global/admin surfaces, container API for workspace scope; scoped 404s with no data for every resource class — claims, digestion, evidence, anchors/data, studies, experiments, jobs, discovery, research-loop, notebooks, reports (C083-5, C083-17, C083-18)
- [ ] T020 Admin API — users (role/type change, disable with instant session death, removal preserving attribution) and invites (create, list, revoke) (C083-5, C083-4, C083-11)
- [ ] T021 Admin API — workspaces (create/archive, global Admin/Owner only) and the per-user workspace-access matrix (read/write a user's full grant set) (C083-16, C083-19)
- [ ] T022 Audit: append-only writes for every FR-012 event (logins success/failure, invite events, role/type and membership changes, disable/removal, setup, publishes, admin API denials), actor + timestamp on each (C083-12)
- [ ] T023 Attribution: edge injects the authenticated identity on every container request; container stamps mutating records with actor id + timestamp; bundle-imported records labelled "via desktop import" (C083-11, FR-011)
- [ ] T024 Credential separation tests: the Spec 082 install token refused at the edge in every position (cookie, header, query); edge↔container service credential only in platform secret stores, in no client-visible artifact (C083-8, FR-008); terminal admin-only in cloud, member attempts 403 + audit-logged (C083-5, D-5); claim-test matrix from the plan (Step 2) green; LEDGER.md entry

## Step 3 — frontend (PR: `feat/083-frontend`)

- [ ] T025 Wireframes 01–06 in the SPA's existing design system: login, invite acceptance, glassbreak setup, admin users, admin invites, admin audit (C083-1, C083-2, C083-3, C083-12)
- [ ] T026 Wireframes 07–11: shell with membership + workspace switcher, account & security, admin workspaces, admin user-access matrix (C083-5, C083-16, C083-19)
- [ ] T027 Carryover deltas on the 17 carried-over screens per carryover-touchpoints.md: user chip, dataset chip (bundle id · source commit · hydrated at), *Started by* on jobs, actor rendering on claims/digestion/evidence (C083-11, C083-13)
- [ ] T028 Membership filtering applied to lists **and** counts/badges — no count computed over a workspace the user cannot see (C083-18)
- [ ] T029 Verification: Playwright screenshots at desktop 1440 + mobile 390 compared against the approved wireframes screen by screen; any deviation stops the step and is reported, not improvised around; LEDGER.md entry

## Step 4 — the data-boundary publisher (PR: `feat/083-cloud-publish`)

- [ ] T030 `tools/cloud-publish/` builder (home-side): allowlist configuration (publishable tables + checkout paths); restricted stores structurally excluded (C083-6, FR-006)
- [ ] T031 Restricted-marker scan: maintained marker-list file; scan over every artifact before upload; a failed scan uploads nothing (C083-6)
- [ ] T032 Manifest emission (Step 1 format) + R2 upload; publish recorded with its scan-gate result as a first-class report line (C083-6, C083-13, C083-12)
- [ ] T033 Planted-canary test wired into CI: a restricted marker planted in a publishable source must fail the publish (C083-6)
- [ ] T034 Primary-workspace seeding: the bundle assigns all existing project state to the seeded "Indus Script" workspace; per-class counts reconciled against the source in the publish report (C083-15)
- [ ] T035 Export / reviewed-import tooling: cloud-side changes come home as an inspected diff (by table and file), owner-triggered — never an auto-sync (D-4); LEDGER.md entry

## Step 5 — pre-launch proofs + production go-live (Amendment 2 rollout; no staging)

- [ ] T036 Acceptance script (Stories 1–5 as amended by the workspace model) run against the local production-shaped build **and** an ephemeral preview deployment; both runs recorded (C083-1…19)
- [ ] T037 Falsifier suites for C083-1…19 executed as written; results recorded in the rollout record; a falsified claim stops the rollout (C083-1…19)
- [ ] T038 Adversarial pass over the auth surface: invite brute force / code guessing, session fixation, role escalation (member→admin, guest→member-role grant, cross-workspace id probing for every Step 2 resource class) (C083-2, C083-4, C083-5, C083-17, C083-18)
- [ ] T039 Anonymous payload scan: anonymous fetches of the shell and assets contain no project data, names, or counts; every non-public route answers redirect-to-login or 401 (C083-4, C083-18)
- [ ] T040 Noindex checks across response types (pages, API, errors, assets) — `X-Robots-Tag: noindex, nofollow` on each — plus `robots.txt` disallowing all (C083-7, FR-007)
- [ ] T041 External gate + production deploy: BitConcepts Cloudflare account access in hand (DNS record, Pages/Workers/Containers resources, Workers Paid plan), then deploy to `glossa.bitconcepts.tech` — production follows the proofs directly, no staging-proof gate (C083-14; Amendment 2)
- [ ] T042 Glassbreak setup prompt: the one-time setup code + `https://glossa.bitconcepts.tech` delivered to the owner through the coordinator only; owner sets his own password at `/setup` (C083-3)
- [ ] T043 Rollout record (proofs, falsifier results, deployed image/bundle identity, go-live timestamp) + LEDGER.md entry (H1)
