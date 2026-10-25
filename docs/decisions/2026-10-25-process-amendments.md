# Process amendments — 2026-10-25 (realignment items 3.2 and 3.4)

Adopted 2026-10-25 as part of the owner-approved realignment package
(decision record: `docs/decisions/2026-10-25-realignment-decision.md`).
These amendments respond to red-team findings RT-06, RT-07, RT-09,
RT-12, and RT-14. They are forward-looking: they do not retroactively
change the standing of any past approval, freeze, or verdict, all of
which stand on their own records.

## Item 3.2 — authorization artefacts

1. **Committed decision records.** From this date, every owner approval
   that a freeze, an execution, or a programme act rests on is
   committed to this repo as a decision record at the act, citing the
   approval's date and text and the package or plan it approves. An
   approval that exists only as agent-attested narrative in a worker's
   record is not sufficient basis for a freeze or an execution.
2. **No non-existent precedent.** A worker adjudication may not cite a
   precedent, standing pattern, or prior section as authority for a
   ruling unless the cited text exists in the record and contains the
   rule invoked. A citation to a rule that does not exist is a **halt
   condition**: the act stops and the citation is reported, in the
   manner of an integrity tripwire. Where no precedent exists, the
   true basis is stated (owner instruction quoted verbatim, or the
   draft's own stated default under an owner instruction that says so).
3. **Digest signing — deferred residual.** Freeze digests remain
   unsigned hash lists. Adopting signing (or an equivalent external
   anchor) is explicitly deferred and recorded here as an accepted
   residual, as it was in the 2026-10-20 remediation close-out. The
   mitigation that does stand: each freeze's OSF registration carries
   the digest in a timestamped external record, and the freeze record
   cites that anchor.

## Item 3.4 — freeze-checklist amendments

The freeze checklist gains two standing lines, effective for every
freeze after this date:

4. **No self-citation for gate preconditions.** A gate precondition is
   cited to a record independent of the outcome it supports. An outcome
   record never cites itself as the evidence that its own preconditions
   (registration approval, pin verification, sequencing) were met;
   external evidence (OSF API state, timestamps, merged PR records) is
   cited instead.
5. **Banner claims are checked against the act's own log.** Any banner
   or summary claim about the freeze act itself ("computed exactly
   once", "not pre-verified", and their kin) is verified against the
   act's own log before it is written. A gate that was pre-run or
   pre-verified at drafting is flagged as pre-verified in the freeze
   record, beside the gate. A reproduction gate is named a replay/drift
   gate in headline text.

## Acceptance note

Item 3.2's acceptance test is the next freeze: it must carry its
committed decision record. Item 3.4's acceptance is the same freeze's
checklist. Neither test can be run today; both are recorded here so
the next freeze act is measured against them.
