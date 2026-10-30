# Feature Specification: Glossa Lab Cloud Edition — Accounts, Invites, Admin, Hosted Tool (Spec 083)

**Feature Branch**: `spec/083-cloud-edition` (spec) · implementation branches per the Phase 2 plan
**Created**: 2026-10-30
**Status**: APPROVED 2026-10-30 by the owner, as recommended (route + decisions D-1…D-7), **as amended** by Amendment 1 (workspaces are the tenancy unit), Amendment 2 (no staging — D-7 cancelled), and Amendment 3 (the glassbreak account's email; the setup prompt), all adopted with this spec in the Phase 0 PR. Where an amendment and the original text differ, the amendment governs. Claims frozen before code (spec-kit + AEE flow).
**Input**: Owner orders, 2026-10-30, in sequence: (1) a BitConcepts subdomain for Glossa Lab, hosted there; an admin dashboard for user management; himself added as the **glassbreak** user; invite codes to invite people to the project; (2) **not** hosted from his desktop — "the same approach we've always been using… using GitHub"; (3) **robots kept away** — the site must not show up in searches, at least not yet; (4) scope settled: the **full working tool** for invitees in the cloud (over the coordinator's project-space-first recommendation — the owner's override stands and this spec implements it).
**Predecessors**: Spec 079 (supervised install), Spec 080 (desktop host migration — the desktop remains the owner's local install and the dataset's home side), Spec 081 (the generic-tool UI: programs, scoped surfaces, the 17 screens this edition carries over), Spec 082 (per-install token auth — explicitly *not* the cloud credential; see FR-008).

## Problem statement

Glossa Lab is a single-operator local tool: one install token, no accounts,
no concept of *who* acted. The owner now wants collaborators inside the
tool — real invited users, working in the real surfaces, on infrastructure
that follows his standing hosting pattern (GitHub as source, Cloudflare as
host, staging → production) on `glossa.bitconcepts.tech` — while two
boundaries hold absolutely: the restricted material under the program's
custody (the CISI class) never enters the cloud copy, and the site stays
invisible to search engines until he lifts that himself.

The architecture route is decided by the companion study
(`architecture-route-study.md`): **Cloudflare Containers running the
existing FastAPI application**, fronted by an edge Worker + Durable Object
that own identity and the perimeter, identity data in **D1**, the research
dataset moving as hash-verified **bundles through R2**. It is the only
route under which "the full working tool" is literally true — same code,
same pinned assessor (AEE ≥1.5.0), same verdicts.

## Design summary

- **Topology.** Pages serves the built SPA on `glossa.bitconcepts.tech`
  — the single production deployment (Amendment 2: there is no staging
  deployment or staging hostname; verification runs against local builds
  and ephemeral preview deployments). An edge Worker fronts all dynamic traffic: it
  terminates sessions, enforces the perimeter, sets the noindex header on
  every response, and routes authenticated API traffic through a Durable
  Object to the single named container instance running the unmodified
  application. GitHub remains the source: the repo builds the SPA, the
  edge Worker, and the container image.
- **Accounts.** Username + password; passwords hashed with Argon2id
  (parameters in the Phase 2 plan) and never stored, logged, or transmitted
  in any other form. Registration exists **only** as invite redemption
  (FR-001). Sessions are opaque ≥256-bit tokens, hashed at rest in D1,
  carried in an `HttpOnly; Secure; SameSite=Lax` cookie (FR-004).
- **The glassbreak admin.** The first-run setup (FR-003): the deployment
  pipeline issues a one-time setup code (CSPRNG, single-use, 24-hour
  expiry), printed once to the deploying operator's terminal — never to
  git or email. The owner opens `/setup`, enters the code, the
  username **glassbreak**, and a password he chooses on that screen. The
  moment an admin exists, the setup path closes permanently. The seed
  record carries the account's email, **`tristen.pierson@gmail.com`**,
  as its contact identifier (Amendment 3), and at go-live the owner
  receives the setup code + the production URL as the glassbreak account
  prompt — the password itself is never collected by the agent, in any
  form, anywhere.
- **Invites.** Admin-generated codes (≥128-bit CSPRNG, stored hashed),
  single-use, default 7-day expiry, revocable, optionally bound to an
  email and to one or more programs. The dashboard presents each invite as
  a shareable link (`/invite/<code>`); the admin sends it by whatever
  channel he chooses. (In-app email sending is deliberately not in this
  spec — see Out of scope; the desktop app's SMTP notification subsystem
  is a desktop facility.)
- **Roles — two axes (Amendment 1).** The tenancy unit is the
  **Workspace**; the existing Program entity *is* the workspace (same
  `projects` entity, tenant language), and a primary workspace, **Indus
  Script**, is seeded at deploy with all existing project state.
  Access crosses two axes, on the conventional GitHub/Slack/Notion
  pattern: a **global user type** (Owner — glassbreak, singular /
  Admin / Member / Guest) and a **per-workspace role** (Owner / Admin /
  Member / Viewer / none), held independently per workspace. Global
  Admins hold implicit Workspace Admin everywhere; Guests may hold
  Viewer only. A user with no role in a workspace sees none of it — no
  surface, no name, no count (FR-015…FR-017, Amendment 1 for the full
  matrix). A member with no grants sees the tool home with an honest
  "no program access yet" state (wireframe 07); the workspace switcher
  is the Spec 081 Q1 sidebar card (wireframe 11).
- **Attribution.** The edge passes the authenticated identity into the
  container API on every request; acts are stamped with the acting user
  (FR-011). Lane-2 digestion is by named humans — multi-user makes that
  literally true in the cloud edition.
- **The dataset.** Research state (app SQLite + checkout file state) is
  *not* edited in place in the cloud from some shared drive; it moves as
  a **bundle**: built by the publish pipeline from allowlisted sources,
  scanned, manifested (bundle id, build time, source commit, per-artifact
  SHA-256), stored in R2. The container hydrates atomically from the
  manifest and exports its changed state back on cadence and on orderly
  stop. Importing cloud changes back into the repo/desktop side is a
  reviewed step, never a silent overwrite (FR-013, Out of scope).
- **Data boundary.** The publish builder works from an **allowlist**
  (publishable tables, publishable checkout paths) with **structural
  exclusion** of restricted stores (raw scan directories, page previews,
  restricted folders), then runs a **restricted-marker scan** over every
  artifact. A scan failure fails the publish before anything uploads
  (FR-006, claim C083-6 with a planted-canary falsifier).
- **Noindex.** Three layers (FR-007): `X-Robots-Tag: noindex, nofollow`
  set by the edge on *every* response; a `robots.txt` that disallows
  everything; and the login wall itself. Standing until the owner lifts
  it by name.
- **Credential separation.** Spec 082's install token governs desktop
  installs and first-party automation only; the cloud edge never accepts
  it. The edge↔container hop uses a per-deployment service credential
  held only in platform secret stores (FR-008).

## User Scenarios & Testing

### User Story 1 — The owner becomes glassbreak (Priority: P1)

The deployment exists (the production deployment — Amendment 2: there
is no staging). The operator runs the seed step;
a setup code appears once in the operator's terminal. The owner opens the
setup screen, enters the code, sets his username (**glassbreak**) and his
own password, and lands in the tool as admin.

**Acceptance Scenarios**:

1. **Given** a fresh production deployment with no users, **When** the owner
   completes setup with a valid code, **Then** exactly one admin account
   (`glassbreak`) exists, he is signed in, and the audit log records the
   setup with a timestamp.
2. **Given** setup has completed, **When** anyone requests `/setup` or
   replays the code, **Then** the path answers as closed (404) — forever.
3. **Given** the code was issued over 24 hours ago unused, **When** it is
   presented, **Then** it is refused as expired and no account is created;
   re-issue requires the operator seed step again.

### User Story 2 — The owner invites a collaborator (Priority: P1)

From the admin dashboard's Invites tab the owner creates an invite for
the Indus Script program, copies the link, and sends it. The invitee
opens the link, chooses a username and password, and is inside the
program as a member.

**Acceptance Scenarios**:

1. **Given** a valid unused invite, **When** the invitee completes the
   acceptance screen, **Then** a member account exists with membership in
   exactly the invite's programs, a session is issued, and the invite is
   marked used (by whom, when) in the dashboard and the audit log.
2. **Given** the same link opened again, **When** anyone submits it,
   **Then** redemption is refused — the code is spent.
3. **Given** the owner revokes an unredeemed invite, **When** its link is
   opened, **Then** redemption is refused with a named, honest message.
4. **Given** no invite at all, **When** a stranger finds the login page,
   **Then** there is no registration path offered to them.

### User Story 3 — A member does real work (Priority: P1)

A member signs in and works in their program: registers a claim with its
falsifier, records a digestion act, runs a study, checks a job — the
Spec 081 surfaces, unchanged in shape, with their name on their acts.

**Acceptance Scenarios**:

1. **Given** a member of the Indus Script program, **When** they register
   a claim, **Then** the claim record carries their user id and the
   detail surface shows "registered by <username>".
2. **Given** a member who does not belong to a second program, **When**
   they request that program's surfaces or API, **Then** they receive the
   scoped 404 and none of its data.
3. **Given** a member, **When** they request any admin surface or API,
   **Then** 403, and the attempt is audit-logged.

### User Story 4 — The owner manages people (Priority: P1)

In the admin dashboard the owner sees every user, their role, status,
programs, and last activity; he can grant or remove program membership,
change a role, disable an account (sessions die immediately), issue a
password-reset link, and remove an account (attribution on past work is
preserved; the account can no longer sign in).

**Acceptance Scenarios**:

1. **Given** a signed-in member, **When** the owner disables their
   account, **Then** the member's next request is refused and their
   session rows are gone.
2. **Given** any admin action in this story, **When** the owner opens the
   Audit tab, **Then** the action is there with actor and timestamp.
3. **Given** a removed user's past claims, **When** a member opens one,
   **Then** the attribution still renders (as the removed username,
   marked removed) — history is not rewritten.

### User Story 5 — The dataset moves honestly (Priority: P2)

The owner (or the pipeline on cadence) publishes a new dataset bundle
from the repo/desktop side. The cloud Status surface shows the bundle id
and source commit being served; members see the new state; a bundle that
fails the restricted-marker scan never exists in R2.

**Acceptance Scenarios**:

1. **Given** a publish with a planted restricted marker in a publishable
   source, **When** the pipeline runs, **Then** the publish fails at the
   scan gate and R2 holds no new bundle.
2. **Given** a hydration interrupted mid-transfer, **When** the instance
   next serves, **Then** the dataset is entirely the old manifest or
   entirely the new one — verified by sampled artifact hashes.
3. **Given** a long-running job in flight, **When** the instance sleeps
   and wakes (or is redeployed), **Then** the job reaches a terminal
   state with its outcome or its failure reason recorded.

## Requirements

- **FR-001 Invite-only registration.** Account creation exists only as
  invite redemption (FR-002) and the first-run setup (FR-003). No open
  registration route, form, or API exists.
- **FR-002 Invite lifecycle.** Codes are ≥128-bit CSPRNG values stored
  only as hashes; single-use via atomic check-and-consume; default expiry
  7 days (admin-adjustable at creation); revocable until redeemed;
  optionally bound to an email and to a set of programs, which become the
  new member's initial memberships.
- **FR-003 Glassbreak seeding.** One setup window per deployment,
  gated by a single-use setup code expiring within 24 hours of issue,
  issued by an operator-side seed step that displays it exactly once, in
  the operator's terminal only. The owner sets the password on the setup
  screen. Completion permanently closes the setup path. No password or
  password-equivalent material in chat, code, configuration, logs, or
  pipeline artifacts; the salted Argon2id hash in D1 is the only residue.
- **FR-004 Sessions.** Opaque ≥256-bit session tokens, hashed at rest,
  `HttpOnly; Secure; SameSite=Lax` cookie, server-side expiry, immediate
  revocation on logout, disable, removal, or role change. Unauthenticated
  surface is exactly: login, invite redemption, setup (while open),
  `robots.txt`, and the static shell assets needed to render those.
  **The login wall is the deployment's protection (Amendment 2)**: for
  anonymous requests every other route answers redirect-to-login or 401,
  and no project data — records, names, counts, content-bearing payloads
  — is served anonymously in any form; the shell may load but contains
  no project data, and the dataset hydrates only after authentication.
- **FR-005 Roles and membership.** *Replaced by Amendment 1* — the
  two-axis access model (global user type × per-workspace role) is
  specified as FR-015…FR-017 below and in `amendment-1-workspaces.md`,
  which governs wherever this section's original single-axis wording
  appeared. The terminal remains a global Admin/Owner facility in the
  cloud edition (D-5).
- **FR-006 Publish pipeline and data boundary.** The bundle builder is
  allowlist-based with structural exclusion of restricted stores, and
  every artifact passes the restricted-marker scan before upload; a
  failed scan uploads nothing. The marker list is a maintained file in
  the repo (its *patterns* are publishable; the restricted content is
  not). Direct editing of the cloud dataset outside a publish is not a
  supported path.
- **FR-007 Noindex perimeter.** Edge-set `X-Robots-Tag: noindex, nofollow`
  on every response from both hostnames; `robots.txt` disallowing all;
  the login wall. Removal requires the owner's named lift and a spec
  amendment — it is not a dashboard toggle.
- **FR-008 Credential separation.** The Spec 082 token is never accepted
  by the cloud edge in any position (cookie, header, query). The
  edge↔container service credential is per-deployment, held only in
  platform secret stores, injected by the edge, and never rendered into
  any client-visible artifact.
- **FR-009 Assessor identity.** The container image installs
  `applied-epistemic-engineering` within the repo's existing pin
  (≥1.5.0,<1.6) and runs the repo's `aee_core` adapter unmodified; the
  GAP-ENV regression set (23 claims, incl. the 0.1625 sign_val
  expectations) is part of the deployment acceptance run.
- **FR-010 Job durability.** Job state lives in the dataset (exported to
  R2 on cadence and on orderly stop); the engine's stall semantics carry
  over — a job without heartbeat past the stall window is failed *with
  the reason recorded*; hydration restores job state before the engine
  resumes; the instance's sleep policy is suppressed while jobs run.
- **FR-011 Attribution.** Every mutating act in the cloud edition is
  stamped with the acting user's id and timestamp at the record level;
  surfaces that show an act show its actor (wireframe notes in
  `carryover-touchpoints.md`).
- **FR-012 Audit log.** Append-only (no update/delete path in any API);
  records logins (success/failure), invite events, membership and role
  changes, disable/removal, setup, publishes, and admin API denials;
  viewable and filterable in the admin dashboard.
- **FR-013 Dataset versioning and atomic hydration.** Every bundle has a
  manifest (id, build time, source commit, per-artifact SHA-256);
  hydration verifies the full manifest before swap; the Status surface
  displays the served bundle id + source commit + hydration time.
- **FR-014 Production-only rollout (Amendment 2; D-7 cancelled).** There
  is exactly one deployment, at `glossa.bitconcepts.tech`; no staging
  resources or staging hostname are ever created. Verification runs
  against local production-shaped builds and ephemeral preview
  deployments. The pre-launch proof battery — the claim-test suites, the
  planted-canary and marker-scan gates, a fresh adversarial pass over
  the auth surface, and the noindex header checks — passes against the
  production-shaped build *before* the production deploy, and go-live
  follows the proofs directly, recorded in the rollout record. There
  is no separate staging-proof gate; the login wall (FR-004) is the
  protection this rollout relies on.
- **FR-015 Workspaces and the primary seed (Amendment 1).** The
  workspace is the tenancy unit and is the existing Program/`projects`
  entity. At deploy, a primary workspace (**Indus Script**) is seeded
  and the publish pipeline assigns *all* existing project state to it;
  every project resource carries a workspace scope from the first
  bundle onward — nothing is served unscoped.
- **FR-016 Workspace lifecycle (Amendment 1).** Only global Admin/Owner
  accounts can create or archive workspaces (D-1 applied). An archived
  workspace serves nothing: scoped 404 to all non-admin users, listed
  as archived in the admin surfaces only.
- **FR-017 Two-axis access enforcement (Amendment 1).** Global types:
  Owner (singular, glassbreak), Admin, Member, Guest (Viewer-only
  ceiling). Per-workspace roles: Owner (exactly one per workspace),
  Admin, Member, Viewer, none. Enforcement on every request — at the
  edge for global/admin surfaces, in the container API for workspace
  scope (the API binds queries to the identity's entitled workspace
  ids itself). Workspaces a user has no role in answer scoped 404 in
  every resource class enumerated in Amendment 1 §3, and contribute
  nothing to search results, lists, counts, or badges. Viewer mutation
  attempts answer 403. The admin dashboard shows each user's
  workspace-access matrix exactly as stored, and edits take effect on
  the target's next request.

## Claims

Frozen in `aee-claims.json` (C083-1…C083-19), each with evidence and a
falsifier, in the post-PR-#450 normalized bundle format. Summary:
invite-only registration (1), invite lifecycle (2), glassbreak seeding
(3), the login wall + session perimeter (4, strengthened by Amendment
2's enumerated anonymous-access falsifier), access-model enforcement
(5, revised to the two-axis model by Amendment 1), the data
boundary + marker-scan gate (6), noindex (7), credential separation (8),
assessor identity (9), job durability (10), attribution (11), audit
completeness (12), dataset version honesty + atomic hydration (13),
production-only rollout (14, revised by Amendment 2 — no staging),
primary-workspace seeding fidelity (15), workspace creation gating
(16), per-workspace role enforcement (17), cross-workspace isolation —
scoped 404s and no count/list/search leakage (18), and admin
access-matrix accuracy (19).

## Assumptions — epistemic boundaries (H13)

- **Trust model**: invited collaborators are trusted *as researchers*
  and untrusted *as infrastructure operators*. Members get the full
  working tool inside their programs; shells, user management, and
  publishing are operator facilities. A member is not sandboxed from
  their own programs' data — membership *is* the authorization.
- **Single instance**: one container instance serves the edition
  (matching the tool's single-process design). Concurrent members share
  one engine; long jobs queue exactly as they do on the desktop. If the
  invited team outgrows one instance, that is a new spec, not a setting.
- **Cloud work is a branch, not a fork**: the cloud dataset is a working
  copy of the repo/desktop state with a reviewed import path back.
  Simultaneous editing of the same records on desktop and cloud is a
  merge the owner reviews — the spec does not pretend otherwise.
- **Restricted material**: the boundary claim (C083-6) is mechanical, not
  promissory — allowlist + structural exclusion + scan + canary — because
  the custody rule (statistics publishable, scans never redistributed)
  does not soften for a friendlier audience.
- **Adversarial challenge that would break this design**: compromise of
  the Cloudflare account itself (it holds the secrets, the identity
  store, and the dataset) — mitigated by the owner's existing account
  posture (Microsoft SSO on the BitConcepts account), and stated here
  because no application-layer control answers it; and a restricted
  marker that matches nothing on the maintained list — mitigated by the
  allowlist being the primary control and the scan the second, so a
  list gap alone does not publish restricted material (the source must
  also be allowlisted).
- **Confidence**: the route rests on structural platform facts read from
  Cloudflare's docs on 2026-10-30 (route study §2). Pricing figures are
  estimates from published rates. The Phase 2 plan re-verifies the
  structural facts before the first deploy.

## Out of scope

- **In-app email sending of invites** (the link is the deliverable; the
  admin sends it by his own channel). A transactional-email integration
  is a follow-up spec if the owner wants it.
- **Host-management surfaces whose object is the local machine** —
  excluded from the cloud edition with reasons, present unchanged on the
  desktop: environment setup/rebuild/upgrade (pip mutation of a running
  shared instance contradicts the immutable container image and endangers
  every member's work); the shutdown endpoint (instance lifecycle belongs
  to the platform/Durable Object; a per-user shutdown of a shared
  instance is a denial of service against the other members — an admin
  *restart instance* action through the Durable Object replaces it);
  the tray (no desktop exists in this edition).
- **Bundled local LLM (Ollama)** in the container image: no GPU, model
  weights against a 20 GB disk ceiling; the provider reports offline
  exactly as on a desktop without Ollama, and external providers from the
  existing registry serve the AI surfaces. Not a surface removal.
- **Multi-instance scaling, per-program databases, public registration,
  password self-service by email** (reset is an admin-issued link),
  and any change to the desktop edition's behavior. The desktop remains
  the owner's local install; Spec 083 changes nothing there except adding
  the publish/export tooling on the dataset's home side.
- **Lifting the noindex perimeter** — owner's named act, future amendment.
