# Spec 095 — commission and grounding (2026-11-15)

## The commission

On 2026-11-15 the owner pasted an external red-team review of the
Glossa-Lab / Indus program into this chat with the order "Make sure
you are working on all this." The review's own section 5 ends in a
Definition of Done and a recommended work order; its five stated
priorities are reproducibility, evidence independence, research
software, scientific direction (identifiability over assignment
coverage), and a second decipherment target.

The commission this spec answers is narrower than the review, on
purpose: reconcile first. The program's standing experience is that
an external review of this program mixes genuine findings with
restatements of work already owned and with factual errors about
the current state. Nothing was to be specced until every row of the
review had been checked against the program's own records and
dispositioned. The owner adopted the result on 2026-11-15 (22:29
ET) as Spec 095, reconciliation first, with the decisions recorded
in `ratification-2026-11-15.md`.

## The review, as received

Preserved verbatim at `hidden_files/red-team-2026-11-15/REVIEW.md`
in the goal workspace (30,751 bytes; SHA-256
`fa72ca0dc8ed541037273c9c5d5d5e8ed4482f217b961b768da3f16add47712e`).
By its own section 1 statement it is a source-level and documentary
review, not a runtime penetration test; its claims about running
systems are bounded accordingly, and the reconciliation treated
them that way (its one runtime-adjacent claim, about the app, proved
to be its own tool limit).

## The reconciliation (Stage 0, executed before adoption)

Four passes, run in parallel on 2026-11-15 and verified by the
parent from the files before the adoption was offered; the Stage 0
record (`stage-0-record-2026-11-15.md`) carries their full hashes
and headline results. In summary:

- Of 43 register rows, 23 are DUPLICATE-OF-RECORD. The review's two
  P0s, all of Spec 092's remainder, Spec 094 entire, the
  validator-repair lineage, the evidence-independence categories,
  and the Indus discriminating-test program were already owned.
- 14 genuinely NEW items were isolated (register section N). They
  are this spec's build substance.
- Exactly one defect was newly proven by the review: RT-03, the
  anchor-model README presenting the v2-era package as current.
- One duplicate-vehicle row is classified a security risk
  requiring verification, not a proven defect: RT-06, cloud
  tenancy, whose vehicle is the outstanding Spec 083 proof set.
- Two of the review's factual claims are wrong against the record
  (RT-42, claim and study counts; RT-43, where the research data
  lives). The record governs both; the review was not edited.

## What was deliberately not specced

- Everything the register mapped to an owning vehicle. Spec 092's
  Stage 2 and 3, Spec 094's build stages, Spec 091, Spec 093's
  remainder, the gap register's open entries, and Spec 083's
  outstanding proofs proceed under their own commissions; this spec
  adds no parallel work item for any of them (C095-1, D-095-1).
- The two confirmed-defect micro-fixes. They are one-banner and
  one-sentence acts, not stage work; D-095-5 records them as
  owner-gated micro-tasks in the Stage 0 record.
- Execution of either second target. The review ranks Eteocypriot
  first and Meroitic second as future decipherment targets; the
  adoption takes scoping only (D-095-4).
- Any change to a frozen record, a live store, or the research
  loop's standing. Spec 053's re-execution, when Stage 1 reaches
  it, runs under a new order with its gates unchanged and files its
  own record.

## The adoption shape

The adoption follows the clean Spec 092 pattern (PR #548): the
claims intake rides inside the adoption PR, so the PR's own CI is
green on its face, and no records-only exception is needed or taken
(D-095-6, tasks.md T004). The Spec 094 adoption's #566 exception is
explicitly not repeated.
