# Spec 046 — OSF Contract Registration

> ## FILED — PENDING APPROVAL — 2026-10-21
>
> Filed at the freeze under campaign decision
> E-1 (DD-046-18), following the Specs 036–039
> pattern.
> Registration: **https://osf.io/dnts8/**
> Draft registration id: `6ad88d83ff6a3d17ed00b66c`
> Filed at: 2026-10-21T10:02:26Z (draft created
> 2026-10-21T10:01:39Z)
> Node: nrb9u (Predictions & Registrations)
> Schema: OSF Preregistration
> (697b72f611a8e98484c6139b)
> Subjects: the programme's five standing subjects
> (Computational Linguistics; Social and Behavioral
> Sciences; Anthropology; Linguistics;
> Archaeological Anthropology) — verified by
> read-back on the filed registration.
>
> State at filing, verified via the OSF API:
> `reviews_state: initial`, `public: false`,
> `pending_registration_approval: true`, no DOI
> yet (DOIs mint on approval). All 29 schema
> fields were filed from the frozen contract
> and verified by read-back against the filed
> draft — exact, no differences.
>
> Approval proceeds via the token link in OSF's
> admin-notification email. **This freeze act
> does not touch Gmail**: the approval is the
> parent agent's act, and the registration's
> OSF mail stays in the inbox until the
> approval verifies, per the standing OSF mail
> rule. This record is completed by append
> once the approval is API-verified (accepted
> + public + DOI), and the messages are
> archived at that point.
>
> **Execution awaits this approval**
> (DD-046-18): Phase-405 does not run on the
> filing alone, and no list was opened for
> scoring at the freeze.
>
> The registration carries the frozen contract:
> freeze-act digest
> `80c3be31e5af5236f71cb2c1894b2946f9b8ad47b12bdeab9d03cd76468af405`,
> execution Phase-405, the claim
> `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`,
> the four lists of record (Wells as SOURCE;
> CISI, Parpola, Mahadevan as INDEPENDENT),
> the total outcome mapping (CONSENSUS /
> CONTESTED / PARTIAL CONCURRENCE /
> SINGLE-SOURCE) with its step-0 and
> identification closures, the
> `concordance-297.json` delivery and closure
> form, and the Spec 045 cross-check finding
> recorded at DD-046-14 for Spec 045's freeze
> to repair on its side.

---

## Amendment note — 2026-10-21 (pre-merge)

The freeze PR's first CI run (39581775853)
failed one test for a working-tree reason
recorded in `freeze.md` §6: the suite's own
Spec 029 regeneration tests rewrite the
claim-lifecycle records before the freeze
test reads them, so a live byte-hash
assertion over those records cannot stand
in-suite. The freeze test was corrected
(content-level assertions for the cited
records; the §2 pins stand as freeze-time
facts against the definition), and
`freeze.json` was recomputed exactly once
over the amended state. Per the Spec 030
precedent, the freeze-act digest above
stands in this record and in the filed
registration `dnts8`; the **successor
digest** is
`30c3480b29aeb5468615007f14de5500ba6266b9ea452c428e5d2b81d3bf36f1`,
the value in `freeze.json` as merged. No
claim, decision, outcome, or contract
wording changed.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
