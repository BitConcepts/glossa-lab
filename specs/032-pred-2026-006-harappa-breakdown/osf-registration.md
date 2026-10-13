# Spec 032 — OSF Registration Record

> ## FILED — PENDING APPROVAL — 2026-10-13
>
> The frozen Spec 032 contract was filed on OSF on
> 2026-10-13 under the OSF Preregistration schema,
> after the freeze merged and before any execution
> (the pnqrx / 7m35w / bge3k / jtwvc filing pattern).
> The registration is **pending admin approval**: the
> approval is completed by the programme owner via
> the token link in OSF's admin-notification email
> (the standing arrangement — the OSF API returns
> HTTP 409 for the unmoderated Registries provider,
> recorded below). On approval this record is
> completed by append with the public state and the
> minted DOI; nothing already written here is edited.

## Registration

- **Registration:** https://osf.io/3htn8/ (id `3htn8`)
- **Project node:** https://osf.io/2zcr5/ (id `2zcr5`,
  public standalone project created for this filing;
  the Spec 027/028/030/031/032 precedent nodes carry
  no files, and neither does this one)
- **Title:** "Spec 032 (Phase-396) — PRED-2026-006
  Harappa Breakdown: Frozen Contract (Spec 032
  freeze, merged 2026-10-13)"
- **Schema:** OSF Preregistration
  (`697b72f611a8e98484c6139b`) — the same schema as
  the Spec 027 Stage 1 (`pnqrx`), Phase-393 (`7m35w`),
  Spec 030 (`bge3k`), and Spec 031 (`jtwvc`)
  registrations.
- **Draft registration id:** `6ace12eb68211cdf47da6aca`
- **Filed:** 2026-10-13 (`date_registered`
  2026-10-13T11:18:19Z).
- **State at filing:** `reviews_state: initial`;
  `public: false`;
  `pending_registration_approval: true`; **no DOI
  yet** (DOIs mint on approval).
- **Subjects:** Computational Linguistics;
  Social and Behavioral Sciences; Anthropology;
  Linguistics; Archaeological Anthropology (the
  programme's standing set; the four leaf subjects
  were set in one call and OSF attached the parent).
- **Content:** all 29 schema fields filed from the
  frozen contract (spec.md as frozen; claims.json at
  register_version 0.4-draft, 12 claims F032-C01…C12)
  and verified by read-back — the only differences
  are OSF's HTML-escaping of `>=` in two fields.
  Filed quantities include the registered criterion
  (≥ 70% of CISI-trained INITIAL signs with Harappa
  start rate ≥ 0.40), the step-0 provenance design
  (fail-closed; CANNOT BE RUN AS WRITTEN), the
  unmappable coverage rule (> 20% stated in the
  verdict's first sentence), the data census
  (5,679 inscriptions, 77 sites, 2,717 Harappa), and
  the within-lineage caution on verdict wording.
  One filing correction is recorded for honesty: the
  first field patch was rejected (HTTP 400) because
  the foreknowledge option text had been paraphrased;
  it was re-filed with the schema's exact option text
  — the situation it describes is this study's.
- **Frozen contract cited:** freeze.md / freeze.json
  in this directory; **freeze digest
  `34cd6230471c746878ab80110c4a07c3f3daeecef6c05bf222521b39054490ab`**
  (framework026). Design: PR #199 (merged `c00b87fa`).
  Freeze: PR #202 (merged `8dd3954c`).
- **API approval attempt:** the API review-action
  POST was attempted **exactly once** at filing and
  returned **HTTP 409** — "OSF Registries is an
  unmoderated provider" — the known behaviour for
  this provider; it is recorded here and will not be
  retried. Approval proceeds by the admin token link.
- **Admin notification:** OSF's "Pending
  Registration - Admin Notification" email for this
  registration arrived 2026-10-13T11:18:40Z
  (**Gmail message `1a134fc6fd2260c7`**; its snippet
  names this registration's exact title).

## What happens next

Execution (**Phase-396**) runs under the owner's
2026-10-13 order once this registration's approval
verifies (public, DOI minted). Until then nothing
executes and no other record changes: the PRED
register's existing text is untouched (the outcome,
when it exists, is appended as a dated entry), and
the Spec 026–032 frozen records stand as frozen.

## Completion — APPROVED AND PUBLIC (2026-10-13)

- **DOI: https://doi.org/10.17605/OSF.IO/3HTN8**
- Approval route: the API review-action POST
  returned **HTTP 409** at filing (recorded above),
  as the program record predicts; approval was
  effected via the tokenised approve link in the
  "Pending Registration - Admin Notification" email
  (Gmail id `1a134fc6fd2260c7`, received
  2026-10-13T11:18:40Z), opened in the signed-in
  browser — the standing approvals loop (owner
  order 2026-10-11: registration approvals are the
  agent's job, never left as an owner action item).
  The cancel link in the same email was not
  touched.
- The registration's public page shows "Public
  registration", Date Registered Oct 13, 2026,
  7:18 AM EDT (browser-verified).
- State verified via the OSF API after approval
  (2026-10-13): `reviews_state: accepted`,
  `public: true`,
  `pending_registration_approval: false`,
  `withdrawn: false`, `embargoed: false`;
  `date_registered: 2026-10-13T11:18:19Z`;
  `registered_from` node `2zcr5`; the identifiers
  record carries DOI `10.17605/OSF.IO/3HTN8`.
- Execution gate: the registration precondition is
  satisfied by this approval and verification.
  Phase-396 execution proceeds under the owner's
  2026-10-13 order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
