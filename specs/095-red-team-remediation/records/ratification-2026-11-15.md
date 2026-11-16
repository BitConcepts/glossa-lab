# Spec 095 — ratification record (2026-11-15)

## The decision

The owner adopted this package as Spec 095 on 2026-11-15, in this
chat, at 22:29 ET, in these words: "Adopt it as Spec 095,
reconciliation first, as recommended." The recommendation adopted
was the Stage 0 reconciliation's own shape: the register governs
scope, the build stages queue behind Spec 094's, the pinnability
remediation is fail-closed, the second targets are scoping only,
the two micro-fixes stay owner-gated outside the stages, and the
claims intake rides inside the adoption PR.

## The decisions as adopted (D-095-1..6)

- **D-095-1 — the register governs scope.** The reconciliation
  register of 2026-11-15 is the scope of record for the review;
  duplicates stay with their owning vehicles; nothing is worked
  twice (C095-1).
- **D-095-2 — sequencing.** Stage 0 is complete at adoption. Build
  stages run after Spec 094's build stages in the adopted queue:
  Spec 092 Stage 2, then Spec 094 build stages, then Spec 095 build
  stages, then Spec 091 Stage 1. The register's closing line framed
  the queue the NEW items were sequenced against (Spec 092 S2,
  Spec 094 build stages, Spec 091 Stage 1); the adoption inserts
  this spec's build stages between Spec 094's and Spec 091 Stage 1.
- **D-095-3 — pinnability remediation is locate-first and
  fail-closed.** Verification is against the PR #393 intake pin;
  any other digest stops the remediation; no substitute corpus is
  admissible (C095-2).
- **D-095-4 — second targets are scoping only.** Eteocypriot
  enters as proposal and preregistration draft only; Meroitic as a
  scoped reproduction benchmark; execution of either is a separate
  owner decision (C095-15, C095-16).
- **D-095-5 — the micro-fixes are not absorbed.** The RT-03 README
  supersession banner and the tracker stale ledger sentence are
  recorded in the Stage 0 record as owner-gated micro-tasks
  (MT-095-1, MT-095-2), outside this spec's stages.
- **D-095-6 — the intake rides inside the adoption PR.** No frozen
  record is modified by the adoption; C095-1..C095-17 enter the
  claims ledger through the importer in this same PR, on the clean
  Spec 092 pattern (PR #548). The Spec 094 #566 records-only
  exception is explicitly not repeated.

## The AEE assessment of the package

The bundle (`aee-claims.json`, 17 claims, SHA-256
`c0abaca8cba29d8d98ed5a7a6bab7ebf136f78b09c6c57fe31cbf1c49f7e27d0`)
was validated and assessed under the pinned assessor (aee 1.5.3) at
adoption time:

- `aee validate`: **valid — 17 claim(s)**, exit 0.
- `aee assess --no-ledger`: exit 1, outcome **iterate** —
  "Assessed 17 claim(s); found 71 failure mode(s); 17 claim(s)
  below the 0.70 confidence threshold", with the draft cap applied
  (all 17 claims are draft at intake, so the cap is the expected
  posture, the same as at Spec 094's adoption). The full output is
  filed verbatim at `records/adoption-aee-assessment.json` and is
  not edited. The verdict is recorded, not chased: adoption is the
  owner's act, and the claims' discharge is the build stages' work.

## What ratification does not do

It commissions no build stage (D-095-2 queues them; each is
commissioned separately), executes neither second target
(D-095-4), performs neither micro-fix (D-095-5), modifies no frozen
record, and lifts nothing in Spec 094 — the research loop stays off
the live stores until Spec 094's closeout lifts that by name.
