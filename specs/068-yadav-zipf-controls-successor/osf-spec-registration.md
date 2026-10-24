# Spec 068 — OSF Contract Registration

> ## FILED — PENDING APPROVAL — 2026-10-22
>
> Filed at the freeze under DD-068-12 (OPEN-068-6),
> following the programme's standing pattern.
> Registration: **https://osf.io/3pbwe/**
> Draft registration id: `6ada9a673106e90669a1179f`
> Filed at: 2026-10-22T23:21:54Z
> Node: nrb9u (Predictions & Registrations)
> Schema: OSF Preregistration
> (697b72f611a8e98484c6139b)
> Subjects: the programme's five standing subjects
> (Computational Linguistics; Social and Behavioral
> Sciences; Anthropology; Linguistics;
> Archaeological Anthropology) — all five set
> cleanly on the draft and read back on the
> registration.
>
> State at filing, verified by API read-back:
> `reviews_state` initial,
> `pending_registration_approval` true, not yet
> public; all 29 schema responses present,
> including the freeze digest in the study-design
> answer (one read-back encoding note: OSF
> returns the `>=` / `<=` of the comparison-rule
> formulas HTML-escaped — the filed content is
> unchanged; a field-by-field diff at filing,
> after unescaping, found no other difference).
> Approval proceeds via the token link in OSF's
> admin-notification email — the owner's approval
> click, which this filing does not perform and
> whose mail it does not archive (the registration
> stands pending). Execution (Phase-430) runs
> under the owner's execution order of 2026-10-22,
> given with the freeze rulings, once this freeze
> had merged and this registration had been filed
> (freeze.md §7); the registration's
> pending-approval state at execution is recorded
> in the outcome record as it stands. This record
> is completed by append once the approval is
> API-verified (accepted + public + DOI).
>
> **Filing route note (recorded openly).** The
> draft was created on node nrb9u under the
> schema, titled, populated with the 29
> responses, and given the five subjects, all
> verified by read-back on the draft (the title
> was set by a PATCH on the draft through the
> CLI's own request machinery). The registration
> was then created from the verified draft
> through the registrations endpoint
> (registration_choice immediate) — the route
> Spec 067's filing record documents after its
> draft-action submit endpoint returned HTTP
> 404 — which returned the registration above in
> the pending-approval state. No content was
> changed between the draft read-back and the
> registration read-back.
>
> The registration carries the frozen contract:
> freeze digest
> `ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d`,
> execution Phase-430, the falsifier (at least
> one named non-linguistic control fitting the
> Zipf–Mandelbrot curve as well as or better
> than the Indus primary fit, ε = 0, the
> synthetic control by its replicate median),
> the population ruling (DD-068-7, LIMB B: the
> strict-sign-set restriction dropped openly;
> the fitted population is the full ICIT sign
> inventory of the restricted corpus; limb A
> considered and not taken), the P-F1 intake
> gates S1–S4 with both SHA-256 pins (corpus
> `345241b1…`, row grades `02394241…`) and the
> intake census, the step-0 gates 0.1–0.7 in
> their order with their named closure classes
> (INVALID / SHAKTI INTAKE NOT REPRODUCED /
> CONTROL SET FREEZE FAILED / TOO THIN), Spec
> 053's frozen estimator carried identically
> (DD-053-11) with the gate 0.2 self-test, the
> four named controls (DD-068-11: Mesopotamian
> numerical signs; heraldic charges; the
> synthetic emblem inventory, Yule–Simon
> ρ = 0.10, seed 20261021, 99 replicates; Linear
> B as the linguistic positive control) with
> gate 0.6 as the fixed pin source for the
> exact tables, the comparison rule with the
> NEAR MISS band (0 < Δ ≤ 0.02, reporting
> only), the positive-control condition, the
> headline mapping (SEPARABLE / NOT SEPARABLE /
> COMPARISON UNINFORMATIVE) on the primary fit
> alone, the grade-sensitivity discipline
> (sensitivity fit in full beside the primary;
> a differing ordering is a grade-sensitivity
> finding and never changes the headline), the
> subsampling tables, the new-baseline fence
> (decision 2c: the result neither confirms
> nor corrects any Phase-43 quantity; the
> Phase-43 exponent is never an input), and
> the append-only posture toward Spec 053's
> frozen record and the claim's recorded
> fields (the outcome appends as a dated
> strength label only, and not on a step-0
> closure).

## Freeze landing (recorded at this filing)

- Freeze PR: **#342** (branch
  `spec-068-yadav-zipf-controls-successor-draft`),
  merged to `main` as merge commit
  **`9bdb21d0e32a096abd87525a2dc159b7685dfd79`**
  at 2026-10-22T23:17:24Z.
- CI: GitHub Actions run **39869769204** on the
  PR head `e149b182` — **7 of 7 jobs success**,
  verified from the settled run's own job
  conclusions (Backend tests (pytest); Frontend
  tests (Playwright); Indus public validation
  checks; Evidence Graph script smoke tests;
  Shell wrappers ubuntu / macos / windows).
- Foundation check (H21) read-back on the
  merged tree, with the two Holdat CSVs copied
  from the existing local downloads (corpus CSV
  SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
  verified first): **40 checks passed, 0
  failed, 8 warnings** — the standing figure.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
