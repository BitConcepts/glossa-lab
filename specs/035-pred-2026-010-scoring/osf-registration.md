# Spec 035 — OSF Registration Verification Record

> ## VERIFIED AT DRAFT — 2026-10-20
>
> The registration this design rests on is the
> prediction's own preregistration, filed
> 2026-10-13 at PRED-2026-010's registration —
> not a filing of this spec. It was verified by
> API read-back at this draft (the step-0 check
> 0.1 discharge for design purposes, spec §3);
> execution re-verifies it before any run,
> because a registration's state can change.

## Registration

- **Registration:** https://osf.io/wjebq/ (id
  `wjebq`)
- **DOI:** 10.17605/OSF.IO/WJEBQ (the identifiers
  read-back carries exactly one identifier, of
  category `doi`, with this value)
- **Filed from:** the Predictions & Registrations
  node https://osf.io/nrb9u/ (id `nrb9u`;
  `registered_from` = `nrb9u`, confirmed in the
  read-back)
- **Title:** "PRED-2026-010 — Cross-Site Class
  Preservation (Clean Withholding): Successor
  Registration to PRED-2026-006 (registered
  2026-10-13)"
- **Schema:** OSF Preregistration
  (`registration_supplement` in the read-back:
  "OSF Preregistration")
- **Filed:** 2026-10-13 (`date_registered`
  2026-10-13T12:45:55Z, per the API read-back)
- **State at this verification (2026-10-20):**
  `reviews_state: accepted`; `public: true`;
  `pending_registration_approval: false`;
  `withdrawn: false`; `embargoed: false`;
  `pending_embargo_approval: false`;
  `pending_withdrawal: false`; an archive copy
  exists (`ia_url`:
  https://archive.org/details/osf-registrations-wjebq-v1).
- **Content check:** the read-back's registered
  fields restate the contract this spec implements
  — the trained set (P000, P217, P324), the bars
  (≥ 70% of trained signs at Harappa start rate
  ≥ 0.40; with 3 signs, only 3 of 3), the
  hash-pinned pool / withheld file / crosswalk,
  and the disclosure (cleanliness = verified
  training-pool exclusion, not analyst blindness;
  no Harappa start rate has been computed).
- **Filing record:** `docs/pred-2026-010-osf-registration.md`
  (filed pending approval 2026-10-13; the
  approval was completed and the record completed
  by append the same day — the values above are
  the API's, which govern).

## How this differs from Specs 032–034

Specs 032–034 each froze a study contract and
then filed that frozen contract as its own OSF
registration before execution. PRED-2026-010
arrived already registered: its preregistration
(wjebq) is the registered contract this spec
implements, filed before any scoring by the
registration act itself. This draft files nothing
new. Whether the frozen Spec 035 also files its
own contract registration is a freeze-time
decision (DD-035-4); either way, execution step 0
re-verifies wjebq (§0.1), and any spec
registration filed at freeze is verified the
same way before any run.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
