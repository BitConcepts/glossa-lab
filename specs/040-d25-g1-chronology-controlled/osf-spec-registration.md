# Spec 040 — OSF Registration (Phase-439)

> ## FILED — PENDING APPROVAL — 2026-10-24
>
> Filed under DD-040-9 and the owner's approval
> of the freeze plan as specified (2026-10-24),
> following the Spec 036–041 pattern: the frozen
> contract is registered before execution,
> execution does not begin while approval is
> pending, and the registration's approval is
> the owner's act (the email token-link route;
> OSF sign-in by ORCID only). Execution
> (Phase-439) additionally requires a separate
> owner order. The freeze act is dated
> 2026-10-24 (owner-local); the filing completed
> at the timestamp below, after the freeze PR
> (#366) merged on genuine CI green (7/7, read
> from the run's own job conclusions).

- **Registration:** https://osf.io/2rgtb/
- **Draft registration id:** `6adcce1f3e93cc6ec26e2fd1`
- **Filed at:** 2026-10-24T15:27:20Z (draft created
  2026-10-24T15:26:23Z)
- **Node:** Predictions & Registrations (`nrb9u`)
- **Schema:** OSF Preregistration
  (`697b72f611a8e98484c6139b`)
- **Subjects (the programme's standing five):**
  Computational Linguistics; Social and Behavioral
  Sciences; Anthropology; Linguistics;
  Archaeological Anthropology — all five set on
  the draft and read back on the registration.
- **State at filing (verified by API read-back):**
  `reviews_state` initial,
  `pending_registration_approval` true, not
  public, not withdrawn; all 29 schema responses
  present and matching the filed values (the one
  read-back difference is OSF's own HTML-escaping
  of ">=" in the study-design answer), including
  the freeze digest in the study-design answer.
- **Freeze digest carried in the study-design
  answer:**
  `16aeeb7017f34f079742e56f13bfd88e3955ce75722693eae87fbbbaa9927515`
  (`specs/040-d25-g1-chronology-controlled/freeze.json`).
- **Title:** Spec 040 (Phase-439) — D-25: The G1
  Site Association Under Chronology Control —
  Frozen Contract (Spec 040 freeze, 2026-10-24)
- **What the registration states openly:** §1 is
  settled by the successor-artifact substitution
  (Spec 039's artifact recorded as not satisfying
  §1; Spec 041's artifact accepted and pinned);
  derivation A1 governs; and on the pinned counts
  the §5 margins gate already fails under every
  derivation, so an execution under this contract
  is expected to close NOT-YET-TESTABLE at the
  margins gate.

## Approval route

Approving through the API is not available for
this registration (the provider node is
unmoderated; the API approve action returns
HTTP 409, as on the programme's earlier
registrations). Approval proceeds through the
token link in OSF's "Pending Registration -
Admin Notification" email — the owner's approval
click, which this filing does not perform. The
direct token_action URL resolved from that
email's approve anchor (the anchor after "To
approve this registration:"; the second "Click
here" is the cancel link and was not used) is
stored verbatim with the filing record.
Message ids (Gmail): admin notification
`1a16e86274b947b2`; the draft-created notice
`1a16e8530c1d65bc`. Under the programme's OSF
mail rule, both messages stay in the inbox until
the registration's approval is verified through
the API; they are archived after. This record is
completed by append once approval is API-verified.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
