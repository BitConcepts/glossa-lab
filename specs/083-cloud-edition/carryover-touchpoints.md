# Spec 083 — where multi-user changes touch the 17 carried-over screens

The cloud edition keeps Spec 081's 17 screens in their approved shapes.
Nothing below redraws them; these are the deltas the Phase 2 build applies
when the same screens run multi-user. New surfaces (login, invite, setup,
admin, account) have their own wireframes in `wireframes/`.

## Amendment 1 (2026-10-30) — programs are workspaces

Read every "program" below as **workspace** (the same entity; Amendment
1). The deltas this adds to the carried-over screens:

- **The switcher is the tenancy control.** The Spec 081 Q1 sidebar-card
  switcher switches *workspaces*. It lists only workspaces the user
  holds a role in, each badged with *their* role there (roles differ
  per workspace), and switches the scope of every surface, list, and
  count with it (wireframe 11). A workspace the user has no role in is
  absent — from the switcher, from search, from everywhere.
- **Counts and badges are workspace- and membership-scoped.** Sidebar
  counts, register counts, and digestion badges are computed inside the
  current workspace and the viewer's memberships only — never across
  workspaces (C083-18). This closes, as a requirement, the badge-scope
  gap Spec 081's closeout recorded as an observation.
- **Viewer is a rendering mode, not a error.** In a workspace where the
  user is Viewer, the 17 screens render read-only: mutating controls
  are absent, and the lede names the role ("You're viewing as Viewer")
  exactly as the surfaces name other honest states.
- **Membership wording follows the matrix.** "Members" steps in create
  forms and program-home member lists show per-workspace roles
  (Owner/Admin/Member/Viewer) rather than a flat member flag, and the
  Programs home card shows the viewer's own role on each card.

**Everywhere**

- **Topbar identity.** The service chip gains the signed-in user:
  `Glossa Lab v… · cloud · checked HH:MM` stays, and a user chip
  (`glassbreak · admin` / `<username> · member`) with the account menu
  (Account & security, Sign out) appears at the topbar's right edge
  (wireframe 07). The tray's fragment-token handoff does not exist here;
  sessions replace it (Spec 082's contract continues to govern desktop).
- **Status screen.** The identity block's "host" line reads the cloud
  instance (container id, region) and gains the **dataset line**: bundle
  id · source commit · hydrated at — the C083-13 honesty surface. The
  desktop's data-folder line does not appear in this edition.
- **Jobs screen.** Rows gain a *Started by* column (username). Retry and
  cancel act on any job for admins, and on the member's own jobs for
  members — the engine itself is unchanged.

**Program surfaces**

- **Programs (tool home).** Cards are membership-filtered: a member sees
  only their programs; the empty state for a member with no grants is
  the "no program access yet" card (wireframe 07), not the desktop's
  first-run create card — members cannot create programs; admins can,
  and the create form gains a *members* step (grant existing users).
  Admins additionally see an **Admin** nav group (Users, Invites, Audit).
- **Program home.** The standing position and counts are program data as
  built in Spec 081 Phase 2; unchanged. The foundation card's "checked"
  line now names the dataset bundle it was computed from.
- **Claims register + claim detail.** Every claim shows its actor:
  "registered by <username>" (+ "via desktop import" for records that
  arrived in a bundle without a cloud actor — the honest label for
  pre-cloud and desktop-side work; records are never given a fake cloud
  author). Contested/explanation records carry their author's name.
- **Digestion board.** Cards already name the act owed; in the cloud they
  also name *who* owes it where a stage was assigned, and completing an
  act stamps the acting member (C083-11). The board is shared: every
  member of the program sees the same queue — that is the point of
  inviting people.
- **Evidence & sources.** Uploads and URL imports record the importing
  user; correspondence entries carry their author. The restricted-material
  rule is unchanged and visible: nothing in this surface can reach the
  restricted stores, because they are not in the dataset (C083-6).
- **Data.** Anchor-set edits are attributed; the import action states the
  dataset consequence ("imports land in the working dataset and export
  with the next bundle") so members are never surprised about where
  their work lives.
- **Experiments / Analysis.** Runs record the launching user; results
  attribution follows the job. Canvas and craft unchanged.
- **Discovery.** Fetch actions record who ran them; triage decisions
  (accept/dismiss) are attributed — the inbox fence (inbox ≠ evidence)
  is unchanged.
- **Research loop.** Sessions are per-user: a member's loop session is
  their own; the surface shows whose session is running and its ceiling
  exactly as Spec 081 specified. One engine, queued work — stated in the
  surface lede, not discovered by collision.
- **Reports & ledger.** Generated reports record their generator; the
  ledger itself is unchanged (append-only). The publish action (new
  bundle) appears here for admins, with the scan-gate result shown as a
  first-class report line — a failed scan is a report, not an error toast.
- **Settings.** Tool settings split as Spec 081 built them; account-level
  items move to the new Account & security screen (wireframe 08).
  AI provider keys, where a member views them, render masked as today;
  editing provider configuration is admin-only in this edition (shared
  infrastructure, shared keys).

**Desktop-only furniture that simply does not render in this edition**

Tray surfaces (no tray), the port/lifecycle controls owned by the Spec
080 starter (the platform owns lifecycle; Status shows instance state
instead), and the env/shutdown endpoints excluded in the spec — their
nav entries are absent, not greyed: an absent surface is the honest
rendering of "not part of this edition."
