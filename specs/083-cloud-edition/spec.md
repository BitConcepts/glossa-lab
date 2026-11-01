# Feature Specification: Glossa Lab Cloud Edition — Accounts, Invites, Admin, Hosted Tool (Spec 083)

**Feature Branch**: `spec/083-cloud-edition` (spec) · implementation branches per the Phase 2 plan
**Created**: 2026-10-30
**Status**: APPROVED 2026-10-30 by the owner, as recommended (route + decisions D-1…D-7), **as amended** by Amendment 1 (workspaces are the tenancy unit), Amendment 2 (no staging — D-7 cancelled), and Amendment 3 (the glassbreak account's email; the setup prompt), all adopted with this spec in the Phase 0 PR. Amendment 4 (Cloud Run compute; GCS bundles) was adopted and then **superseded in full by Amendment 5** (2026-10-30): the origin is the owner's Spec 080 production desktop install on TRISTEN-DESKTOP, reached through a named Cloudflare Tunnel consumed by the edge Worker through a Workers VPC Service binding; no cloud dataset exists. Where an amendment and the original text differ, the amendment governs. Claims frozen before code (spec-kit + AEE flow).

**Input**: Owner orders, 2026-10-30, in sequence: (1) a BitConcepts subdomain for Glossa Lab, hosted there; an admin dashboard for user management; himself added as the **glassbreak** user; invite codes to invite people to the project; (2) **not** hosted from his desktop — "the same approach we've always been using… using GitHub"; (3) **robots kept away** — the site must not show up in searches, at least not yet; (4) scope settled: the **full working tool** for invitees in the cloud (over the coordinator's project-space-first recommendation — the owner's override stands and this spec implements it); (5) **Amendment 5 (later on 2026-10-30, superseding item (2)'s hosting outcome and Amendment 4)**: "host on the desktop (Tristen-desktop) and route to the cloudflare subdomain. but again, only allow members to log in and use." — the hosted edition runs on the owner's desktop and reaches members through Cloudflare; the member login is the gate.
**Predecessors**: Spec 079 (supervised install), Spec 080 (desktop host migration — the desktop remains the owner's local install and the dataset's home side), Spec 081 (the generic-tool UI: programs, scoped surfaces, the 17 screens this edition carries over), Spec 082 (per-install token auth — explicitly *not* the cloud credential; see FR-008).

## Problem statement

Glossa Lab is a single-operator local tool: one install token, no accounts,
no concept of *who* acted. The owner now wants collaborators inside the
tool — real invited users, working in the real surfaces — hosted on the
Spec 080 production install on TRISTEN-DESKTOP and routed through
Cloudflare to `glossa.bitconcepts.tech` (Amendment 5) — while two
boundaries hold absolutely: project data and the restricted material
under the program's custody (the CISI class) are never copied into a
cloud dataset — none exists in this design — and the site stays
invisible to search engines until he lifts that himself.


The architecture route is decided by the companion study
(`architecture-route-study.md`) as amended by Amendment 5's fact-check
(`amendment-5-desktop-tunnel-hosting.md` §2): **the Spec 080 production
desktop install is the application, and its dataset's only home**. An
edge Worker + D1 own identity and the perimeter at
`glossa.bitconcepts.tech`; a Workers VPC Service binding carries
authorized origin traffic through a named Cloudflare Tunnel to the
desktop backend at `127.0.0.1:8001`. "The full working tool" is
literally true — same code, same pinned assessor (AEE ≥1.5.0), same
verdicts — because the hosted route serves the desktop install itself.


## Design summary

- **Topology.** `glossa.bitconcepts.tech` is a **Worker Custom
  Domain**: the edge Worker is the public entry and the origin for
  the hostname (Cloudflare creates the DNS records and certificate;
  there is no staging deployment or staging hostname — Amendment 2).
  The Worker terminates sessions, enforces the perimeter, sets the
  noindex header on every response, and — only after the session and
  route authorization checks pass — calls a **Workers VPC Service
  binding** whose registered target is the named Cloudflare Tunnel
  `glossa-desktop` to the desktop backend at `127.0.0.1:8001`. The
  desktop backend serves the built SPA and the API. The tunnel
  publishes no hostname in this design: there is no
  `glossa` CNAME to `<UUID>.cfargotunnel.com` and no published
  application route for the hostname (Amendment 5 §2.2). GitHub
  remains the source of the code; the running origin is the desktop
  install.

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
  desktop API on every request; acts are stamped with the acting user
  (FR-011). Lane-2 digestion is by named humans — multi-user makes that
  literally true in the cloud edition.
- **The dataset.** Research state (app SQLite + checkout file state)
  is resident in the Spec 080 production desktop install and is
  served in place through the edge/Tunnel route. There is no second
  dataset: no publish, no bundle, no hydration, no import, and no
  sync. The primary workspace's scope assignment is verified in that
  resident dataset before go-live (FR-015, T057).
- **Data boundary.** No cloud dataset exists. The edge stores only
  accounts, invites, sessions, workspace-access records, setup state,
  and audit data (D1). Restricted material remains on the desktop
  under the program's existing custody restrictions; it is never
  copied into D1, Worker storage, a bundle store, or any other cloud
  storage, and it may be returned through the hosted route only
  inside an authenticated, workspace-authorized member session under
  the desktop application's existing restrictions (FR-006, claim
  C083-6 as restated by Amendment 5).

- **Noindex.** Three layers (FR-007): `X-Robots-Tag: noindex, nofollow`
  set by the edge on *every* response; a `robots.txt` that disallows
  everything; and the login wall itself. Standing until the owner lifts
  it by name.
- **Credential separation.** Spec 082's install token governs desktop
  installs and first-party automation only; the cloud edge never accepts
  it. The edge↔desktop-origin hop uses a per-deployment service credential
  held only in the Worker secret store and the desktop install's
  protected credential storage (FR-008).

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

### User Story 5 — Members work on the desktop-resident dataset; offline fails closed (Priority: P2)

A member signs in through the hosted route and works against the
current state of the desktop install — there is no publish step and
no second copy to wait for. When the desktop backend or the tunnel
is down, the subdomain serves the edge's own error and no data.

**Acceptance Scenarios**:

1. **Given** restricted material exists in the desktop install's
   restricted stores, **When** the cloud side (D1, Worker storage and
   configuration) is audited, **Then** no project artifact, restricted
   marker, or scan/preview exists there; and no anonymous or
   workspace-unauthorized request receives restricted or project
   content through the hosted route.
2. **Given** the desktop backend is stopped, or `cloudflared` is
   stopped, **When** a member requests a project surface, **Then**
   the edge returns its own noindex 503 containing no project data
   and no cached dataset; when the host returns, the same resident
   state serves again.
3. **Given** a long-running job in flight, **When** the desktop
   backend restarts, **Then** the job reaches a terminal state with
   its outcome or its failure reason recorded (FR-010).


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
  no project data, and the edge does not call the desktop origin for project data
  before authentication.
- **FR-005 Roles and membership.** *Replaced by Amendment 1* — the
  two-axis access model (global user type × per-workspace role) is
  specified as FR-015…FR-017 below and in `amendment-1-workspaces.md`,
  which governs wherever this section's original single-axis wording
  appeared. The terminal remains a global Admin/Owner facility in the
  cloud edition (D-5).
- **FR-006 Desktop residency and the data boundary (restated by
  Amendment 5).** No cloud dataset exists. Project and research data
  are resident only on TRISTEN-DESKTOP, in the Spec 080 production
  install. The edge stores only accounts, invite and session records,
  workspace-access records, setup state, and audit data. Restricted
  material is never copied into D1, Worker storage, a bundle store,
  or any other cloud storage, and may be returned through the hosted
  route only inside an authenticated, workspace-authorized member
  session under the desktop application's existing restrictions. The
  former publish pipeline — allowlist builder, marker scan, bundle,
  hydration — is retired; no production path creates a dataset copy.

- **FR-007 Noindex perimeter.** Edge-set `X-Robots-Tag: noindex, nofollow`
  on every response from both hostnames; `robots.txt` disallowing all;
  the login wall. Removal requires the owner's named lift and a spec
  amendment — it is not a dashboard toggle.
- **FR-008 Credential separation.** The Spec 082 token is never accepted
  by the cloud edge in any position (cookie, header, query). The
  edge↔desktop-origin service credential is per-deployment, held only
  in the Worker secret store and the desktop install's protected
  credential storage, injected by the edge onto the Workers VPC
  binding request, and never rendered into any client-visible
  artifact. The desktop application accepts edge-injected identity
  only when that credential validates; identity headers without it
  confer nothing.

- **FR-009 Assessor identity.** The hosted route serves the Spec 080
  production desktop install, which installs
  `applied-epistemic-engineering` within the repo's existing pin
  (≥1.5.0,<1.6) and runs the repo's `aee_core` adapter unmodified; the
  GAP-ENV regression set (23 claims, incl. the 0.1625 sign_val
  expectations) is part of the deployment acceptance run against that
  install.

- **FR-010 Job durability (revised by Amendment 5).** Jobs execute in
  the resident engine of the Spec 080 production desktop install, and
  job state lives in the desktop-resident dataset. The engine's stall
  semantics carry over — a job without heartbeat past the stall
  window is failed *with the reason recorded* — across ordinary
  desktop-backend restarts. Amendment 4's machinery is retired: no
  Cloud Run Job executions, no service scale-to-zero, no journal
  export to a bundle store, and no scheduled cloud watchdog.

- **FR-011 Attribution.** Every mutating act in the cloud edition is
  stamped with the acting user's id and timestamp at the record level;
  surfaces that show an act show its actor (wireframe notes in
  `carryover-touchpoints.md`).
- **FR-012 Audit log.** Append-only (no update/delete path in any API);
  records logins (success/failure), invite events, membership and role
  changes, disable/removal, setup, hosted-route configuration
  changes, and admin API denials;
  viewable and filterable in the admin dashboard.
- **FR-013 Dataset versioning and atomic hydration — SUPERSEDED by
  Amendment 5.** No dataset bundle, manifest, bundle store, or
  hydration exists in this design, because no dataset moves. Claim
  C083-13 is superseded with it. The Status surface instead displays
  the desktop install's revision/source commit and the origin's
  health — the honest identity of what is being served.

- **FR-014 Production-only rollout (Amendment 2; D-7 cancelled;
  revised by Amendment 5).** There is exactly one public hosted
  route, at `glossa.bitconcepts.tech`: a Worker Custom Domain whose
  edge reaches the desktop origin only through the named Tunnel's
  Workers VPC Service. No staging resources or staging hostname are
  ever created; no published Tunnel application or
  `cfargotunnel.com` CNAME exists for the hostname; and no second
  public origin or bypass route reaches the desktop backend.
  Verification runs against local production-shaped builds and
  ephemeral preview deployments, and the route-specific proof
  battery (T059) passes on the assembled production route before it
  opens for member use: the claim-test suites as amended, the
  C083-6 cloud-storage audit, a fresh adversarial pass over the auth
  surface, the noindex header checks, and the desktop-offline and
  bypass proofs. Go-live follows the proofs directly, recorded in
  the rollout record, and requires Amendment 5's three gates (§8 of
  the amendment). There is no separate staging-proof gate; the login
  wall (FR-004) is the protection this rollout relies on.

- **FR-015 Workspaces and the primary seed (Amendment 1; mechanism
  revised by Amendment 5).** The workspace is the tenancy unit and is
  the existing Program/`projects` entity. A primary workspace
  (**Indus Script**) exists in the desktop-resident dataset and holds
  *all* existing project state, assigned and verified there before
  the hosted route opens (T057); every project resource carries a
  workspace scope from the first hosted request onward — nothing is
  served unscoped.

- **FR-016 Workspace lifecycle (Amendment 1).** Only global Admin/Owner
  accounts can create or archive workspaces (D-1 applied). An archived
  workspace serves nothing: scoped 404 to all non-admin users, listed
  as archived in the admin surfaces only.
- **FR-017 Two-axis access enforcement (Amendment 1).** Global types:
  Owner (singular, glassbreak), Admin, Member, Guest (Viewer-only
  ceiling). Per-workspace roles: Owner (exactly one per workspace),
  Admin, Member, Viewer, none. Enforcement on every request — at the
  edge for global/admin surfaces, in the desktop API for workspace
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
2's enumerated anonymous-access falsifier; wording updated by
Amendment 5 — the desktop origin is not called for project data
before authentication), access-model enforcement (5, revised to the
two-axis model by Amendment 1; the enforcing API is the desktop API
after Amendment 5), the data boundary (6, **restated by Amendment 5**
— desktop residency; no cloud dataset), noindex (7), credential
separation (8, revised by Amendment 5 — edge → desktop origin through
the Workers VPC binding and the named Tunnel), assessor identity (9,
evidence re-anchored by Amendment 5 in the desktop install itself),
job durability (10, revised by Amendment 5 — the resident desktop
engine; Amendment 4's Jobs model retired), attribution (11), audit
completeness (12, event list updated by Amendment 5), dataset
version honesty + atomic hydration (13, **SUPERSEDED by Amendment
5** — no bundle or hydration exists), production-only rollout (14,
revised by Amendment 2 — no staging — and by Amendment 5 — one
hosted route, no published Tunnel application, no bypass),
primary-workspace seeding fidelity (15, mechanism revised by
Amendment 5 — assignment verified in the desktop-resident dataset),
workspace creation gating (16), per-workspace role enforcement (17),
cross-workspace isolation — scoped 404s and no count/list/search
leakage (18), and admin access-matrix accuracy (19).


## Assumptions — epistemic boundaries (H13)

- **Trust model**: invited collaborators are trusted *as researchers*
  and untrusted *as infrastructure operators*. Members get the full
  working tool inside their programs; shells, user management, and
  host management are operator facilities. A member is not sandboxed from
  their own programs' data — membership *is* the authorization.
- **Single instance**: the one Spec 080 production desktop install
  serves the edition — locally and through the hosted route alike
  (matching the tool's single-process design). Concurrent members
  share one engine; long jobs queue exactly as they do on the
  desktop. If the invited team outgrows one desktop install, that is
  a new spec, not a setting.

- **One dataset, on the desktop**: hosted use and local use are two
  doors into the same desktop dataset. There is no branch, fork,
  sync, or import to reconcile; simultaneous editing is concurrency
  inside one install, governed by the application's existing
  single-process design — the spec does not pretend otherwise.

- **Restricted material**: the boundary claim (C083-6) is structural,
  not promissory — desktop residency plus cloud-storage exclusion,
  membership and workspace authorization, and the desktop
  application's existing restrictions — because the custody rule
  (statistics publishable, scans never redistributed) does not soften
  for a friendlier audience.

- **Adversarial surfaces that would break this design**: compromise
  of the Cloudflare account itself (it holds the edge secrets and
  the identity store); compromise of the Tunnel token (anyone
  holding it can run the tunnel — Amendment 5 §2.3) or of the
  edge↔origin service credential; and compromise of the desktop host
  itself, which is now the origin as well as the owner's local
  install. These are stated here because no application-layer
  control answers them; the mitigations are the owner's account
  posture (Microsoft SSO on the BitConcepts account), credential
  custody and rotation, the login wall, and the bypass proofs
  (T059). There is no Google account surface: Amendment 4's is dead.

- **Confidence**: the route rests on structural platform facts read
  from Cloudflare's official documentation on 2026-10-30 (Tunnel,
  Worker Custom Domains, Workers VPC — Amendment 5 §2, with
  citations). Amendment 4's Google Cloud Run facts are historical;
  that route is superseded. The Phase 2 plan re-verifies the
  structural facts before the first deploy.


## Out of scope

- **In-app email sending of invites** (the link is the deliverable; the
  admin sends it by his own channel). A transactional-email integration
  is a follow-up spec if the owner wants it.
- **Host-management surfaces whose object is the local machine** —
  excluded from the *hosted route*, present unchanged for the owner's
  local desktop use: environment setup/rebuild/upgrade (pip mutation
  of the production install endangers every member's work and the
  owner's local tool alike) and the shutdown endpoint (a remote
  per-user shutdown of the shared desktop origin is a denial of
  service against the other members and the owner). Edge-authenticated
  requests cannot invoke either (Amendment 5 §5). The tray is the
  owner's local desktop surface; hosted members have no tray.

- **Bundled local LLM (Ollama).** Spec 083 installs and bundles no
  Ollama. A desktop does exist in this edition — it is the origin —
  so a provider already configured on that desktop is a
  desktop-install fact, not a Spec 083 component; this spec neither
  adds nor promises one. Not a surface removal.

- **Multi-instance scaling, per-program databases, public registration,
  password self-service by email** (reset is an admin-issued link),
  and any change to the desktop edition's behavior beyond the
  edge-identity acceptance and hosted-route restrictions Amendment 5
  requires. The desktop remains the owner's local install — and, by
  Amendment 5, the hosted origin; no publish/export tooling is added
  to it.

- **Lifting the noindex perimeter** — owner's named act, future amendment.
