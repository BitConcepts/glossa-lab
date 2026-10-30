# Spec 083 Phase 1 — decisions for the owner

One decision is the package itself (approve the route + spec + wireframes,
and Phase 2 plans the build). The route is the headline:

**D-0 · The route: Cloudflare Containers running the existing app.**
Recommended. It is the only route under which "full working tool" is
literally true — the same code and the same pinned assessor — and the only
one whose build effort buys the features ordered instead of re-creating
the tool. The TypeScript route forks the assessor (a version bump already
changed scores once; a language port is worse); the Python Workers route
is disqualified by Cloudflare's own documented limits (no subprocesses,
non-functional threading, in-memory filesystem, 128 MB ceiling) against an
app whose engine runs jobs for hours. Full evidence: `architecture-route-study.md`.
Estimated running cost from published rates: roughly **$35–40/month** with
the instance awake around the clock, less with idle sleep; the account
needs the Workers Paid plan ($5/month minimum, which the container
charges ride on).

> **SUPERSEDED IN PART — Amendment 4 (owner, 2026-10-30).** The route's edge and identity legs stand (Worker + Durable Object front, D1, Pages) — they never needed a paid plan. The compute and bundle legs are superseded: the owner declined the Workers Paid plan, so the app runs as a **Google Cloud Run service + Jobs** and dataset bundles live in **Google Cloud Storage** (same Google account), deployed by GitHub Actions to us-central1, at $0 within the free-tier allotments. The $35–40/month estimate and the Workers Paid passage above are the original record, kept unedited. Full text and the fit-check: `amendment-4-cloud-run-compute.md`.

Open questions the study could not settle from evidence — each with the
coordinator's recommendation, per standing practice:

**D-1 · Who may create programs in the cloud edition?**
Recommendation: **admins only.** Program creation is an act of the
program owner; members join programs by grant. (Desktop unchanged —
there, the operator is the owner by construction.)

**D-2 · Invite binding: email-bound or open link?**
Recommendation: **email optional.** An invite may name an email (shown in
the dashboard as "sent to …", and the acceptance screen pre-fills it) but
redemption is by possession of the link, because the admin sends links
through his own channels and people routinely redeem on a different
address than they were emailed at. Binding hard to an email buys little
and breaks that flow.

**D-3 · Session lifetime.**
Recommendation: **30 days, sliding** (activity extends it), with
immediate revocation on disable/removal/role change. A research tool
people return to daily should not log them out weekly; the revocation
side is where the security actually lives.

**D-4 · Cloud changes flowing back to the desktop/repo dataset.**
Recommendation: **reviewed import, on the owner's act.** The cloud
exports its dataset bundle; bringing cloud-side work home is a deliberate
import the owner triggers and can inspect first (diff summary by table
and file), never an automatic sync. Automatic two-way sync between two
live copies of a research dataset is how records get silently lost;
the spec's claim set covers the cloud side's honesty, and the import
gate is the home side's.

**D-5 · The terminal in the cloud edition.**
Recommendation: **admin-only, kept.** It is the full tool's own operator
facility and the owner's break-glass inside the deployment (its sandbox
root becomes the cloud working tree). Members never see it. The Phase 2
red-team pass (standing practice before any new auth surface goes live)
gets the terminal's cloud posture as an explicit item.

**D-6 · Sending invite emails from inside the app.**
Recommendation: **not in this spec.** The dashboard produces the link;
sending stays in the owner's hands (his channels, his wording). If
in-app sending is wanted later, it is a small follow-up spec (a
transactional email service + templates), and the invite machinery here
already tracks everything it would need.

**D-7 · Staging hostname.**
Recommendation: **`staging.glossa.bitconcepts.tech`**, a full parallel
deployment, noindexed identically. It follows the fleet's staging pattern
and keeps the production hostname untouched until the recorded go.

> **SUPERSEDED — D-7 is CANCELLED by the owner's instruction of
> 2026-10-30 (Amendment 2).** There is no staging deployment for the
> cloud edition: one production deployment at
> `glossa.bitconcepts.tech`, protected by the login wall, with all
> verification run against local builds and ephemeral preview
> deployments and the pre-launch proof battery run before the deploy.
> This text is kept as the record of what was recommended and
> overridden. (D-1 is likewise confirmed and extended by Amendment 1:
> workspace creation is an admin act.)

Nothing else is open. Password hashing (Argon2id), token sizes, cookie
flags, the marker-scan mechanics, and the bundle format are engineering
choices fixed in the spec's requirements, each pinned by a claim with a
falsifier — if any of them looks wrong, say so on the package and it
changes before Phase 2, not during it.
