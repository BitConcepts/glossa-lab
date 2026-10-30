# Spec 083 — Cloud Edition, Phase 1 design package (for approval)

> **ADOPTED 2026-10-30.** The owner approved this package as recommended
> (Containers route + D-1…D-7) and it lands in the repo with three
> amendments adopted the same day: **Amendment 1** (workspaces are the
> tenancy unit — `amendment-1-workspaces.md`; wireframes grow to 01–11
> with the workspace admin screens and the shell switcher), **Amendment
> 2** (no staging; D-7 cancelled — `amendment-2-no-staging.md`), and
> **Amendment 3** (the glassbreak account's email; the setup prompt —
> `amendment-3-glassbreak-email.md`). The claims bundle as adopted
> carries C083-1…19. Below this note, the text is the package as
> presented for approval, kept as the record; where it conflicts with
> an amendment (staging, the single-axis role wording, "Phase 2" for
> what plan.md now lays out as Steps 1–5), the amendment and plan.md
> govern.

**What this is.** The complete approval package for hosting Glossa Lab as
the **full working tool** for invited users at `glossa.bitconcepts.tech`,
on the owner's standing pattern (GitHub as source, Cloudflare as host,
staging → production, **no desktop hosting**), with user accounts, the
**glassbreak** admin, invite codes, an admin dashboard, and a hard
no-indexing perimeter. Phase 1 is design only — no application code has
changed, no Cloudflare resource exists, no DNS record has been touched.
Phase 2 (the build) starts only after this package is approved.

**Owner directives (2026-10-30):** "Make BitConcepts subdomain for
glossa-lab and move it to be hosted there. Create admin dashboard for
user management and add me as glassbreak user and allow invite codes to
be sent to invite folks to the project" — then, correcting the
coordinator's first proposal: not hosted from the desktop; the usual
GitHub/Cloudflare approach — and "keep the robots away… not yet" — and,
on the scope question, the **full working tool** for invitees.

**The package.**

| File | What it decides |
|---|---|
| `architecture-route-study.md` | The route, on evidence: the backend inventoried from the code, Cloudflare's platform facts quoted from the official docs (read 2026-10-30), the four candidate routes scored, one recommendation, the losers' disqualifiers stated plainly. **Recommendation: Cloudflare Containers running the existing app**, edge Worker + D1 for identity, dataset bundles via R2. |
| `spec.md` | The spec-kit specification: design summary, 5 user stories with acceptance scenarios, FR-001…FR-014, epistemic boundaries, and the explicit out-of-scope list with reasons for every exclusion. |
| `aee-claims.json` | C083-1…C083-14 in the normalized bundle format — every claim carries a falsifier, including the mechanical ones: a planted-canary test for the restricted-material boundary (C083-6) and a header-check for the noindex perimeter (C083-7). |
| `carryover-touchpoints.md` | How the 17 Spec 081 screens change under multi-user (attribution, membership, dataset labelling) without changing shape — and which desktop furniture simply does not render in this edition. |
| `decisions-for-owner.md` | The route (D-0) plus the seven questions the study could not settle from evidence (D-1…D-7), each with the coordinator's recommendation. |
| `wireframes/` | 8 HTML wireframes for the new/changed surfaces only + `wireframes.css` + `render-shots.py` + `shots/` (desktop 1440 and mobile 390 renders of every screen, produced and visually verified 2026-10-30). Each screen carries the 081-pattern annotation block (purpose · primary action · what changed and why · claims). |

**The wireframes.**

| # | Screen | One line |
|---|---|---|
| 01 | `01-login.html` | The only door in; no registration offered; one undifferentiated error |
| 02 | `02-invite-accept.html` | Invite link → member account in named programs; spent/expired/revoked specimen |
| 03 | `03-glassbreak-setup.html` | One-time setup: code from the deployment terminal, owner sets his own password, then the door closes forever |
| 04 | `04-admin-users.html` | Users: role, status, programs, activity; Manage actions; last-admin guard |
| 05 | `05-admin-invites.html` | Create (email optional, programs, expiry) → link shown exactly once; full lifecycle list |
| 06 | `06-admin-audit.html` | The append-only event record as a surface — including failed logins and failed publishes |
| 07 | `07-shell-membership.html` | Spec 081's Programs screen in the cloud shell: user chip, dataset chip, membership framing, the no-access member state |
| 08 | `08-account-settings.html` | Profile, password, sessions, and the user's own slice of the audit log |

**Two honest notes.**

1. **Stylesheet damage found and worked around, not hidden.** The Spec
   081 design-system file (`wireframes.css`) is truncated *in the
   committed repo tree* (blob SHA-256 `d5afd16a…`, 8,535 bytes, ending
   mid-rule at `.callout.bad` with a literal tool-truncation marker as
   its last line) and identically in the 081 package copy — everything
   after that rule (`.divider`, `.annotation`, `.mobile-nav`, the
   responsive shell) is missing from both. This package's copy repairs
   the truncation minimally (the damaged rule completed; the missing
   furniture reconstructed in the same visual language, labelled in the
   file) so these wireframes render as designed. **The repo file itself
   is deliberately not fixed here** — Phase 1 is design-only with no
   repo writes; the defect is reported with this package for the main
   flow to repair in the repo and the 081 record.
2. **Mobile renders** are full-page captures; the fixed bottom nav
   appears overlaid at the stitch point of the capture (visible on
   wireframe 07's mobile shot). The layout itself carries the clearance
   padding — this is a capture artifact, not a layout defect.

**What approval starts.** A Phase 2 plan in the program's usual shape
(edge + identity first, container image second, publish pipeline third,
role gates + admin UI fourth, staging acceptance against the five user
stories, production only on the recorded go) — and, before go-live, the
standing red-team pass over the new auth surface, with the terminal's
cloud posture as an explicit item.
