# Spec 030 — OSF Registration Record (Phase-394)

Filed 2026-10-12, after the Spec 030 freeze merged and
before any Phase-394 execution, per the frozen
sequencing (adjudication.md, adopted Ask 5: OSF
registration of the frozen contract is a precondition
of execution, mirroring Spec 027 Stage 1).

- **Registration: https://osf.io/bge3k/** (id `bge3k`)
- **DOI: https://doi.org/10.17605/OSF.IO/BGE3K**
- Filed: 2026-10-12T17:57:38Z (OSF timestamp,
  `date_registered`).
- Schema: OSF Preregistration
  (`697b72f611a8e98484c6139b`) — the same schema as the
  Spec 027 registrations https://osf.io/a2xvc/ (design)
  and https://osf.io/pnqrx/ (Stage 1 contract) and the
  Spec 028 registration https://osf.io/7m35w/.
- Node: `4s9u2` — "Spec 030 (Phase-394) — Q6
  Chronology-Spine Extension: Frozen Contract
  (Spec 030 freeze, merged 2026-10-12)", a public
  project created for this filing (the precedent
  contract nodes are likewise standalone projects
  carrying no files).
- Draft: `6acd1eea5631bd813362c681`; all 29 response
  fields of the frozen contract (spec.md / freeze.md /
  adjudication.md / claims.json — the design, the
  frozen criteria and gaps, the routes and stop-point
  order, the integrity rules, the re-test protocol,
  provenance) filed from the frozen record; read-back
  verified exact except OSF's server-side escaping of
  `>` on read, the same note the Spec 028 record
  carries.
- Subjects (mirroring the precedent registrations):
  Computational Linguistics; Social and Behavioral
  Sciences; Anthropology; Linguistics; Archaeological
  Anthropology. One filing irregularity, resolved at
  filing: a batch subjects PATCH failed ("Subject not
  found") because OSF auto-adds parent subjects; the
  set was applied by PATCHing the two leaf subjects in
  one call, after which the draft carried exactly the
  five.
- Freeze filed: `freeze.json` digest
  `3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3db00e9`
  (framework026, over the recovered claim register,
  register_version `0.2-draft`, claims F030-C01…C07),
  merged as PR #172, merge commit
  `51aec850b9d74ea053d3ac03ba161675f8b928dc`.
- Posture: public, no embargo. Approval route: the
  API review-action POST returned **HTTP 409**
  ("OSF Registries is an unmoderated provider"), as
  the program record predicts; approval was effected
  via the tokenised approve link in the "Pending
  Registration - Admin Notification" email (Gmail id
  `1a131437e4b63966`, received 2026-10-12T17:57:48Z),
  opened in the signed-in browser — the standing
  approvals loop (owner order 2026-10-11: registration
  approvals are the agent's job, never left as an
  owner action item). The cancel link in the same
  email was not touched.
- State verified via the OSF API after approval
  (2026-10-12): `reviews_state: accepted`,
  `public: true`, `pending_registration_approval:
  false`, `withdrawn: false`, `embargoed: false`;
  the identifiers record carries DOI
  `10.17605/OSF.IO/BGE3K`. The registration's public
  page shows "Public registration", Date Registered
  Oct 12, 2026, 1:57 PM EDT.
- Execution gate: adopted Ask 5 is satisfied by this
  filing and verification. Phase-394 execution follows
  under the owner's authorisation (2026-10-12:
  "Register Spec 030 on OSF and execute Phase-394");
  the frozen route order, stop rules, and the §6
  re-test protocol govern it, and its outcomes are
  recorded in this directory and the program ledgers
  — the frozen files are not edited.

AI disclosure: filed and recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.
