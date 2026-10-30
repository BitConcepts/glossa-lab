# Amendment 1 to Spec 083 — Workspaces are the tenancy unit (owner, 2026-10-30)

**Status**: Adopted with the spec (Phase 0). Where this amendment and the
original spec text differ, this amendment governs; the spec's FR-005 is
replaced as noted below and FR-015…FR-017 are added by it.

## 1. The tenancy unit

The cloud edition's tenancy unit is the **Workspace**. The existing
Program concept — the Spec 081 entity, the repo's `projects` table —
*is* the workspace: same entity, same surfaces, tenant language. There
is no second concept layered on top. Every project resource in the cloud
edition carries a workspace scope, and membership in that workspace is
the authorization to see or touch it (the spec's trust model, unchanged:
membership *is* the authorization).

A **primary workspace** is seeded at deploy time, named for the program
it carries — **Indus Script** — and receives **all** existing project
state: every claim, anchor set, study, job record, and file-state
artifact in the published dataset is assigned to it by the publish
pipeline (claim C083-15). Nothing arrives unscoped.

Admins can create additional workspaces (creation is an admin act —
decision D-1, applied to workspaces by this amendment; claim C083-16),
and can archive a workspace. An archived workspace serves nothing: its
surfaces answer scoped 404 to everyone except global admins, who see it
in the admin list, marked archived, for the record.

## 2. Two axes of access — the conventional model

A user's access is the crossing of **two separate axes**, following the
conventional model of comparable multi-workspace products — GitHub
(organization role × team/repository permission), Slack (per-workspace
membership with workspace-level roles), and Notion (workspace role ×
page-level sharing). No exotic scheme is invented here; where this model
differs from one of the references it says so.

**Axis 1 — global user type** (one per account, governs the deployment):

| Type | Powers |
|---|---|
| **Owner** | Everything. Singular: exactly one exists — **glassbreak**, created by the first-run setup (FR-003). No API can create a second Owner, and this spec does not transfer ownership. |
| **Admin** | User and invite management, workspace create/archive, the audit log, publishing, the terminal. Holds implicit Workspace Admin in every workspace. |
| **Member** | A working account. Reaches content only through per-workspace roles (Axis 2). |
| **Guest** | A restricted account for read-only collaborators: may hold **Viewer** per-workspace roles only. The grant API refuses any higher per-workspace role for a Guest (the admin UI disables those options, wireframe 10). |

**Axis 2 — per-workspace role** (one per user per workspace; a user may
hold different roles in different workspaces and none in others):

| Role | View content | Mutate content, run jobs/studies | Manage workspace members | Workspace settings |
|---|---|---|---|---|
| **Workspace Owner** | ✓ | ✓ | ✓ | ✓ |
| **Workspace Admin** | ✓ | ✓ | ✓ | ✓ |
| **Workspace Member** | ✓ | ✓ | — | — |
| **Workspace Viewer** | ✓ | — | — | — |
| *(no role)* | — | — | — | — |

Notes on the matrix, deliberately:

- Exactly one **Workspace Owner** per workspace: its creator, or a
  member the global Owner/Admin designates (transfer is an admin act,
  audit-logged). Workspace Owner and Workspace Admin differ only in
  that the owner is the named accountable holder — their powers are the
  same inside the workspace, as in Slack.
- **Archive/delete of a workspace is a global act** (Admin/Owner axis 1),
  never a per-workspace power — a workspace's own admin cannot make its
  record vanish.
- The **terminal** stays a global Admin/Owner facility (D-5); no
  per-workspace role grants it.
- A **Viewer**'s refusal is honest: mutating controls do not render, and
  a mutation attempted anyway answers 403.
- Global **Member**/**Guest** accounts with no role in a workspace do
  not see that workspace at all — not its name, not its counts (§3).

## 3. Isolation

Every project resource carries a workspace scope. The resource classes
in scope — enumerated because claim C083-18's falsifier runs per class:
workspaces themselves; claims and their records (explanations, contests,
digestion acts and the digestion queue); evidence & sources (texts,
uploads, URL imports, correspondence); anchor sets and the Data
surfaces; studies; experiments and analysis runs; jobs and job results;
discovery items; research-loop sessions and state; notebooks; reports;
foundation status. (Identity data — users, invites, sessions, the audit
log — is deployment-scoped, governed by Axis 1, and is not workspace
data.)

Enforcement, on every query and route:

- A signed-in user without a role in a workspace receives the **scoped
  404** treatment for every resource of that workspace, in every class —
  the Spec 081 pattern, now per workspace.
- **No leakage through aggregates**: search results, lists, sidebar
  counts and badges, and the workspace switcher are all computed inside
  the viewer's memberships. A workspace the user has no role in
  contributes nothing — no row, no title, no count — anywhere. (This
  closes, as a requirement, the badge-scoping gap noted in Spec 081's
  closeout observations.)
- The container API enforces scope itself (it does not trust that the
  edge filtered): every scoped query binds the workspace ids the
  propagated identity is entitled to.

## 4. Admin dashboard additions

- **Workspaces** tab (wireframe 09): list (name, member count, the
  admin's own role, status, created), create (name, description,
  initial members), archive with confirmation. The primary workspace is
  badged Primary.
- **Per-user workspace access** (wireframe 10): from the Users tab, one
  user's access matrix — every workspace × their role in it, editable
  in place; the Guest cap is enforced in the UI and at the API.
- **Shell switcher** (wireframe 11): the Spec 081 Q1 sidebar-card
  switcher becomes the workspace switcher — current workspace with the
  user's role in it, the user's other workspaces with their (possibly
  different) role badges, nothing they have no access to, and the admin
  manage entry.

## 5. What this replaces in the spec

- **FR-005 is replaced** by the two-axis model above (formalized as
  FR-015…FR-017 in the spec). The spec's earlier single-axis wording
  (admin/member over "programs") is superseded wherever it appears,
  including User Stories 2–4, read with "workspace" for "program" and
  the matrix for the role names.
- D-1 is confirmed and applied: workspace (program) creation is an
  admin act.
- Claims: C083-5 is revised to the two-axis model; C083-15…C083-19 are
  added (seeding fidelity, creation gating, per-workspace enforcement,
  cross-workspace isolation, access-matrix accuracy).
