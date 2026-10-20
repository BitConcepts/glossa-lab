# Spec 036 — OSF Registration Record (spec-level contract registration)

> ## FILED — PENDING APPROVAL — 2026-10-20
>
> The frozen Spec 036 contract was filed on OSF on
> 2026-10-20 under the OSF Preregistration schema,
> after the freeze merged and before any execution
> (the pnqrx / 7m35w / bge3k / jtwvc / 3htn8 / zd7uq
> / qkj8d filing pattern). Filing this spec-level
> contract registration was decided at the freeze
> (`adjudication.md` §4, DD-036-4: YES — the Spec
> 032–034 pattern), in addition to the prediction's
> own preregistration (t6whq), which remains the
> registered contract this design implements. The
> registration is **pending admin approval**: the
> approval is completed via the token link in OSF's
> admin-notification email (the standing arrangement —
> the OSF API returns HTTP 409 for the unmoderated
> Registries provider, recorded below). On approval
> this record is completed by append with the public
> state and the minted DOI; nothing already written
> here is edited.

## Registration

- **Registration:** https://osf.io/gjen4/ (id `gjen4`)
- **Project node:** https://osf.io/nrb9u/ (id `nrb9u`,
  the programme's Predictions & Registrations node —
  the same node the prediction's preregistration
  (t6whq) was filed from)
- **Title:** "Spec 036 (Phase-400) — PRED-2026-011
  Scoring: Frozen Contract (Spec 036 freeze, merged
  2026-10-20)"
- **Schema:** OSF Preregistration
  (`697b72f611a8e98484c6139b`) — the same schema as
  the Spec 027 Stage 1 (`pnqrx`), Phase-393 (`7m35w`),
  Spec 030 (`bge3k`), Spec 031 (`jtwvc`), Spec 032
  (`3htn8`), Spec 034 (`zd7uq`), and Spec 035
  (`qkj8d`) registrations.
- **Draft registration id:** `6ad7cfe7944151e4130da8c2`
- **Filed:** 2026-10-20 (`date_registered`
  2026-10-20T20:36:16Z).
- **State at filing:** `reviews_state: initial`;
  `public: false`;
  `pending_registration_approval: true`; **no DOI
  yet** (DOIs mint on approval).
- **Subjects:** Computational Linguistics;
  Social and Behavioral Sciences; Anthropology;
  Linguistics; Archaeological Anthropology (the
  programme's standing set; set by leaf subject and
  verified by read-back — the subjects endpoint
  rejects a payload that also lists a listed
  subject's parent, so the two leaf subjects were
  set and OSF attached the parents, reproducing the
  standing five exactly).
- **Content:** all 29 schema fields filed from the
  frozen contract (spec.md as frozen; claims.json at
  register_version 0.9-draft, 15 claims F036-C01…C15)
  and verified by read-back — **exact, no
  differences**. Filed quantities include the
  registered criterion (≥ 70% of trained signs at
  Harappa start rate ≥ 0.40; with 2 signs, only 2 of
  2), the trained set {P217, P324}, the four
  registered input pins, the fail-closed step-0
  order (0.1–0.4), the zero-occurrence rule
  (DD-036-2, registered text), the cleanliness
  disclosure (verified exclusion, not blindness),
  and — in the foreknowledge field, stated plainly —
  that step 0's coverage check (0.4) is designed to
  pass on the disclosed registration screen (P217 →
  Y0520, confidence 1.0, confirmed; P324 → Y0740,
  confidence 0.9867, confirmed, read from the public
  crosswalk at design time) and that the scoring
  outcome is unknown: no Harappa count or start rate
  had been taken for either sign.
- **Frozen contract cited:** freeze.md / freeze.json
  in this directory; **freeze digest
  `bbd5c4fd5abdb69bd79dfc1115a13e7debf56a7ec38d00ab8e2c8ff6132e946`**
  (framework026). Design + freeze: PR #224 (merged
  `3419df56`, 2026-10-20).
- **API approval attempt:** the API review-action
  POST was attempted **exactly once** at filing and
  returned **HTTP 409** — "OSF Registries is an
  unmoderated provider" — the known behaviour for
  this provider; it is recorded here and will not be
  retried. Approval proceeds by the admin token link.
- **Admin notification:** OSF's "Pending
  Registration - Admin Notification" email for this
  registration reached the programme mailbox at
  2026-10-20T20:36:24Z (Gmail id
  `1a15b079160908ce`); its token link is the approval
  route. (The registration's Gmail messages are
  archived only after approval is verified — the
  standing rule.)

## What happens next

Execution (**Phase-400**) runs under the owner's
2026-10-20 do-all order. Step 0's registration
check (spec §3, check 0.1) names the prediction's
preregistration (**t6whq**) — not this filing — so
execution does not wait on this registration's
approval; the two proceed in parallel, as the
freeze recorded. On approval, this record is
completed by append (public state, DOI) and the
registration's Gmail messages are archived.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
