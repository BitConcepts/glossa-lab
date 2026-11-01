# Amendment 2 to Spec 083 — No staging; production behind the login wall (owner, 2026-10-30)

**Status**: Adopted with the spec (Phase 0). **Decision D-7 is
cancelled** and FR-014 / claim C083-14 are revised as below. Where this
amendment and the original spec text differ, this amendment governs.

## The decision

There is **no staging deployment** for the cloud edition. No staging
Pages/Workers project, no `staging.glossa.bitconcepts.tech`, no staging
D1 or R2 prefix — not now, not as a stepping stone. Decision D-7, which
recommended a full parallel staging deployment, is **superseded by the
owner's instruction of 2026-10-30**, and the record keeps the reason in
his terms: the deployment's protection is **the login wall** — without
an account, nobody sees anything (claim C083-4, strengthened below) —
not the obscurity of a second hostname. A staging copy would double the
hosted dataset's exposure to protect against a risk the wall already
answers.

## The revised rollout

1. **One production deployment** at `glossa.bitconcepts.tech`.
2. **Verification before it exists**: all verification runs against
   local builds (the production-shaped local build of the same image
   and edge code) and, where an edge runtime is needed, **ephemeral
   preview deployments** (platform-generated preview URLs, torn down
   after the run) — never a public staging hostname.
3. **Pre-launch proofs, then go-live directly**: the old Phase 5 becomes
   a proof battery run against the production-shaped build *before* the
   production deploy — the full claim-test suites (C083-1…19), the
   planted-canary publish test and the restricted-marker scan gate
   (C083-6), a fresh adversarial pass over the auth surface (invite
   brute force, session fixation, role escalation, scoped-404 and
   cross-workspace probing), and the noindex header checks (C083-7).
   Production go-live follows those proofs directly. There is **no
   separate staging-proof owner gate**; the proof results are recorded
   in the rollout record like every other gate in this program.
4. **The glassbreak setup happens on the production deployment at
   launch** — the seed step prints the one-time setup code in the
   deploying operator's terminal, and the owner completes setup at the
   production URL (Amendment 3). Until setup completes, the wall's
   anonymous surface is exactly: login, the setup screen (while open),
   invite acceptance, `robots.txt`, and the static shell assets — and
   after setup, the setup screen is gone forever (C083-3).

## The strengthened login-wall claim

C083-4's falsifier is extended with an enumerated anonymous-access test,
because "the login wall is the protection" must be a testable sentence:

- For anonymous requests, **every** route except login, glassbreak
  setup (while open), and invite acceptance returns a redirect-to-login
  or 401 — enumerated across the API route families and the app routes.
- **No project data is served anonymously in any form**: no records, no
  names, no counts, no content-bearing payloads. The SPA shell may load
  (it is the login screen's own furniture), but it must contain **no
  project data** — the dataset hydrates only after authentication.
- The test fetches the shell, its assets, and a route sample
  **anonymously** and scans every payload for dataset content (record
  text, workspace and program names, counts) — any hit falsifies.

## What does not change

- **Noindex stays exactly as specced** (C083-7): the header on every
  response, the disallow-all `robots.txt`, the wall — now on the single
  production hostname. Lifting it remains the owner's named act.
- The container image, edge, D1 identity store, R2 bundle pipeline, and
  every other claim are unaffected. The wrangler configuration carries
  production (plus preview configuration for ephemeral verification
  deployments) and nothing else.
- The desktop edition and the Spec 080 migration are untouched, as
  throughout this spec.
