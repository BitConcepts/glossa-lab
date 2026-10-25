# Spec 073 — OSF Contract Registration

> ## Registration 9kh4a — APPROVED AND PUBLIC — record file landed by dated append, 2026-10-25
>
> This file is the record the freeze ordered (freeze.md §9,
> OPEN-073-7: the filing "is recorded in
> `osf-spec-registration.md`, completed by append after
> filing"). It was missing from this directory until this
> act — red-team finding RT-24 (2026-10-24/25). It is
> written on 2026-10-25 from first-hand API read-back
> performed the same day, and it records two registrations,
> not one: the approved registration of this spec's frozen
> contract, and an orphaned duplicate draft that was never
> submitted.

## 1. The approved registration — 9kh4a

- **Registration:** https://osf.io/9kh4a/
- **DOI:** 10.17605/OSF.IO/9KH4A (verified 2026-10-25 via
  the registration's identifiers endpoint: category `doi`,
  value `10.17605/OSF.IO/9KH4A`).
- **Title:** "Spec 073 (Phase-436) — Repairing the Keying
  Surface: Registry Wells Coverage and a Second
  Depicted-Kind Classification, from Published Sources
  Only — Frozen Contract (Spec 073 freeze, 2026-10-23)".
- **State, verified by API read-back on 2026-10-25:**
  `reviews_state: accepted`, `public: true`,
  `pending_registration_approval: false`, `withdrawn:
  false`; `date_registered: 2026-10-23T13:39:16Z`. The
  registration carries the frozen contract: its
  study-design answer names this spec's freeze digest
  `5419c4c413189acdec31c15494daf1be759c10c28f84d594935c9629e761dc98`
  and execution Phase-436, matching `freeze.json` and
  `freeze.md` in this directory.
- **Node / schema:** filed in the programme's OSF project
  series (node `nrb9u`, "Glossa Indus claims —
  preregistrations"), schema OSF Preregistration, in the
  programme's standing contract form, as the earlier spec
  registrations were filed.
- This registration is the registration of record for
  Spec 073. Nothing in this file or in the RT-24
  disposition touches it.

## 2. The orphan draft — 39vkd (red-team finding RT-24)

- **What the red team verified (2026-10-24/25, RT-24):**
  a duplicate OSF registration draft for Spec 073,
  id `39vkd`, created 2026-10-22, never submitted, still
  in "initial" state, unlinked to any node, existing
  beside the approved 9kh4a with no map in the repo
  between the two.
- **Read-back performed for this record (2026-10-25):**
  under the programme's OSF credential, GET
  `/v2/draft_registrations/39vkd/` and
  `/v2/registrations/39vkd/` both return 404; `39vkd`
  does not appear in the account's registrations
  listing (96 registrations) or in node `nrb9u`'s
  draft registrations (2 drafts, both of other specs);
  and the GUID `39vkd` resolves through the API's guid
  endpoint to an unrelated user record. The orphan
  draft is therefore not reachable as a draft
  registration through the connector's documented API
  operations from this account's view.
- **Withdrawal — disposition.** The OSF connector doc
  (`custom.legacy-osf`) documents no operation for
  deleting or withdrawing a never-submitted draft
  registration: its CLI offers create / patch / submit /
  register actions for drafts and an approve action for
  registrations, and the only DELETE the doc records is
  for files through files.osf.io (WaterButler), which is
  a different object. No improvised API deletion was
  attempted. **Disposition: withdrawal of draft `39vkd`
  requires an OSF UI act by the owner.** It is annotated
  here and in the batch record
  (`docs/decisions/2026-10-25-minor-findings-dispositions.md`,
  RT-24) so that an auditor who finds two registrations
  for this contract has the map: 9kh4a is the approved
  registration of record; 39vkd is the orphan, never
  submitted, carrying no approval and no execution gate.

## 3. What this file does not establish

It does not change the freeze, the execution, or any
record of Spec 073; it supplies the missing registration
map the freeze ordered and RT-24 found absent. The
execution (Phase-436) is the execution the approved
registration 9kh4a registers, per the freeze (§9) and
the registration's own study-design answer.

---

*AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution §VI.*
