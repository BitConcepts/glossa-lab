# Spec 031 — OSF Registration Record (Phase-395)

Filed 2026-10-13, after the Spec 031 freeze merged and
before any Phase-395 execution, per the frozen
sequencing (adjudication.md, adopted Ask 6A: OSF
registration of the frozen contract is a precondition
of execution, mirroring Spec 027 Stage 1).

## State at filing: PENDING APPROVAL

- **Registration: https://osf.io/jtwvc/** (id `jtwvc`)
- **State (OSF API, at filing):** `reviews_state:
  initial`, `public: false`,
  `pending_registration_approval: true`,
  `date_registered: 2026-10-13T06:42:44Z`. No DOI
  exists yet; a DOI is minted on acceptance.
- **What remains:** the approval click — via the
  tokenised approve link in the admin-notification
  email (below), in the signed-in browser, per the
  standing approvals loop (owner order 2026-10-11:
  registration approvals are the agent's job). The
  API review-action POST was attempted exactly once
  at filing and returned **HTTP 409** ("OSF
  Registries is an unmoderated provider"), as the
  program record predicts for every filing on this
  route. After the click, this record is completed
  by append: API verification (`reviews_state:
  accepted`, `public: true`), the minted DOI, and
  the public page's Date Registered.
- Schema: OSF Preregistration
  (`697b72f611a8e98484c6139b`) — the same schema as
  the Spec 027 registrations https://osf.io/a2xvc/
  (design) and https://osf.io/pnqrx/ (Stage 1
  contract), the Spec 028 registration
  https://osf.io/7m35w/, and the Spec 030
  registration https://osf.io/bge3k/.
- Node: `rfhd4` — "Spec 031 (Phase-395) — Q7
  Provenanced-Material Networks: Frozen Contract
  (Spec 031 freeze, merged 2026-10-13)", a public
  project created for this filing (the precedent
  contract nodes are likewise standalone projects
  carrying no files).
- Draft: `6acdd2c1dee2c4dcf72ef217`; all 29 response
  fields of the frozen contract (spec.md / freeze.md
  / adjudication.md / claims.json — the bounded
  question, the two-tier link construction, the arm
  definitions and support rules, the estimand and
  verdict rules, the controls, the declared
  estimability limits, provenance) filed from the
  frozen record; read-back verified exact, field for
  field, against the filed responses.
- Subjects (mirroring the precedent registrations):
  Computational Linguistics; Social and Behavioral
  Sciences; Anthropology; Linguistics; Archaeological
  Anthropology. One filing irregularity, resolved at
  filing in the Spec 030 pattern: OSF auto-adds
  parent subjects, so the set was applied by
  PATCHing the four leaf subjects in one call, after
  which the draft carried exactly the five. A
  `submit-draft` call against the draft-actions
  endpoint returned HTTP 404 before filing; the
  registration was created through the register
  route (`registration_choice: immediate`), the same
  route the precedent filings used.
- Freeze filed: `freeze.json` digest
  `f63167fc99c8d3c31f885b1014cad69fab3788fcf8e6212d018aa6948a2cdac6`
  (framework026, over the recovered claim register,
  register_version `0.3-draft`, claims F031-C01…C12),
  design merged as PR #191 (`b00b3b1d`), freeze
  merged as PR #192 (`95388bbc`).
- Posture: public, no embargo (takes effect on
  approval).
- **Admin notification:** "Pending Registration -
  Admin Notification" from
  openscienceframework-noreply@osf.io, received
  2026-10-13T06:42:56Z, **Gmail id
  `1a134000191cceec`** — arrived 12 seconds after
  the registration was created. The approve link in
  that email is the approval route; the cancel link
  must not be touched.
- Execution gate: adopted 6A is satisfied once the
  approval verifies. Phase-395 execution follows
  only under a separate owner order; it has not
  been ordered, and nothing has been executed.

## Completion — APPROVED AND PUBLIC (2026-10-13)

- **DOI: https://doi.org/10.17605/OSF.IO/JTWVC**
- Approval route: the API review-action POST
  returned **HTTP 409** at filing (recorded above),
  as the program record predicts; approval was
  effected via the tokenised approve link in the
  "Pending Registration - Admin Notification" email
  (Gmail id `1a134000191cceec`, received
  2026-10-13T06:42:56Z), opened in the signed-in
  browser — the standing approvals loop (owner
  order 2026-10-11: registration approvals are the
  agent's job, never left as an owner action item).
  The cancel link in the same email was not
  touched.
- The registration's public page shows "Public
  registration", Date Registered Oct 13, 2026,
  2:42 AM EDT.
- State verified via the OSF API after approval
  (2026-10-13): `reviews_state: accepted`,
  `public: true`,
  `pending_registration_approval: false`,
  `withdrawn: false`, `embargoed: false`;
  `date_registered: 2026-10-13T06:42:44Z`;
  `registered_from` node `rfhd4`; the identifiers
  record carries DOI `10.17605/OSF.IO/JTWVC`.
- Execution gate: adopted 6A is satisfied by this
  approval and verification. Phase-395 execution
  remains a separate owner act; nothing has been
  executed under this record.
