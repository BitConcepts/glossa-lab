# Spec 095 — Red-Team Remediation Program

**Status: ADOPTED 2026-11-15** (owner's decision, this chat, 2026-11-15
22:29 ET: "Adopt it as Spec 095, reconciliation first, as recommended").
Stage 0 (reconciliation and register) is COMPLETE at adoption; it was
executed before the adoption, as the condition the adoption was offered
on. No build stage is commissioned by the adoption: the build stages
run in the adopted queue (D-095-2), after Spec 094's build stages.

**Provenance.** An external red-team review of the Glossa-Lab / Indus
program (source-level and documentary by its own section 1 statement;
not a runtime penetration test) was delivered to the owner and pasted
into this chat on 2026-11-15. The owner ordered it worked ("Make sure
you are working on all this"). Stage 0 reconciled the review against
the program's own records before anything was specced: most of the
review restates work the program already owns, exactly one defect was
newly proven by it, and two of its factual claims are disputed by the
record. This spec exists for what the reconciliation isolated as
genuinely new, plus the remediation the reconciliation itself
prescribed for the review's first priority. The review is preserved
verbatim in the goal workspace (`hidden_files/red-team-2026-11-15/
REVIEW.md`, SHA-256
`fa72ca0dc8ed541037273c9c5d5d5e8ed4482f217b961b768da3f16add47712e`;
the Stage 0 record carries the four reconciliation deliverables'
full hashes, recomputed at adoption).

## 1. What this spec is

A remediation program over the program's own evidence machinery:
corpus reproducibility, validator lineage, synthetic-corpus
containment, contamination automation, statistical-reporting and
identifiability standards, the multi-script data model, the platform's
dashboard and audit surfaces, a composed release gate, and two
second-target scopings. Its scope of record is the reconciliation
register (C095-1): what the register dispositioned as already owned
stays with its owning vehicle and is not worked twice.

## 2. The grounding (Stage 0, complete)

Four deliverables, all in the goal workspace
(`hidden_files/red-team-2026-11-15/`), all cited with full SHA-256 in
`records/stage-0-record-2026-11-15.md`:

- **The register** (43 rows, RT-01..RT-43): 23 rows
  DUPLICATE-OF-RECORD, each mapped to the vehicle that already owns it
  (RT-01 to GR-088-29/GR-088-08 and Spec 053; RT-05 is Spec 092's
  T201-T401 verbatim; RT-13's independence categories are Spec 088's
  C088-12; RT-15 is Spec 094; RT-29's discriminating tests are Specs
  033/052/076/090/093; RT-06 among them, classified a security risk
  requiring verification, never a confirmed defect, with the
  outstanding Spec 083 proofs as its vehicle); 18 rows carrying the
  14 NEW items isolated in the register's section N (RT-03 among
  them: the review's one confirmed defect, a NEW micro-task on the
  GR-088-34 stale-bookkeeping family); two FACT-DISPUTED rows
  (RT-42, RT-43) where the record governs.
- **The pinnability pass** (the review's Priority 0): the missing
  strict corpus and the missing loader are the SAME artifact,
  `firestore_indusarrays_full.jsonl`, the sole data file of the V3
  loader; the file is intake-pinned of record (PR #393, 2026-10-25)
  and Spec 054 recovered the identical file at the identical gate. The
  defect is placement, not existence. The pass prescribes the
  fail-closed remediation C095-2 binds.
- **The public-surfaces pass**: the README defect (RT-03) CONFIRMED
  verbatim; the public tracker matches the record except one stale
  ledger sentence; the review's app claim is the reviewer's tool
  limit, not a defect.
- **The validator census**: every corrected v2 validator module's only
  consumers are its own repair tests; the v1 routines remain
  executable inside the live app as registered Experiment Builder
  nodes with no guard of any kind. No current evidence path computes
  with v1; the exposure is prospective (C095-5).

Two register rows are FACT-DISPUTED and the record governs both:
RT-42 (the review's "912 recorded claims across 91 studies" against
the record's 977 claims across 95 studies at 1,008 ledger lines,
SHA-256 `95d62298e6e4fd059aded79f787ee0c2be06e731bf8e5aaa9ffd2229df31eb1a`
at reconciliation time) and RT-43 (the review's "desktop-resident
research data" against the record: backend and live stores on the
mini-server since the 2026-11-09 re-stand-up; the desktop was
formatted that day).

## 3. The claims and their register basis

Seventeen claims, C095-1..C095-17 (`claims.md`, `aee-claims.json`),
each with a falsifier. The mapping to the register:

| Claim | Register basis |
|---|---|
| C095-1 register as scope of record | the register itself (governance) |
| C095-2 pinnability remediation | the Stage 0 pinnability pass (the reconciliation's P0 deliverable) |
| C095-3 corpus identity standard | RT-08/RT-09, generalized by the pinnability pass's same-layer finding |
| C095-4 twelve-case loader battery | section N item 3 (RT-10) |
| C095-5 validator lineage | section N item 5 (RT-16), census-grounded |
| C095-6 synthetic containment | section N item 2 (RT-04) |
| C095-7 contamination automation | section N item 4 (RT-14) |
| C095-8 equivalence + reporting standards | section N item 6 (RT-17 + RT-32) |
| C095-9 identifiability protocol | section N item 10 (RT-31) |
| C095-10 reading direction as data | section N item 9 (RT-27) |
| C095-11 multi-script abstraction | section N item 8 (RT-24) |
| C095-12 dashboard home + features | section N item 8 (RT-23 + RT-26) |
| C095-13 functional + usability audit | section N item 7 (RT-19 + RT-20) |
| C095-14 composed release gate | section N item 13 (RT-38) |
| C095-15 Eteocypriot scoping only | section N item 11 (RT-34) |
| C095-16 Meroitic benchmark scoping | section N item 12 (RT-35) |
| C095-17 derived documents only | section N item 14 (RT-39) |

Two claims need their standing stated precisely, so the register and
this spec cannot be read as contradicting each other. C095-2 binds
the remediation the reconciliation prescribed, not a re-disposition
of RT-01 or RT-02: Spec 053's record is frozen and cannot commission
its own re-execution, so the new execution order the pass requires
needs an owning spec, and this is it. C095-3 binds the generalization
the pass's same-layer finding points at (identity exists at intake;
it is not carried as a loader-checked standard); the intake work the
register mapped to Specs 053 and 091 stays with them. Register item
N.1 (RT-03, the README supersession banner) is NOT a claim of this
spec: by D-095-5 it and the tracker's stale sentence are owner-gated
micro-tasks, recorded in the Stage 0 record, outside the stages.

## 4. The decisions (D-095-1..6, as adopted)

- **D-095-1 — the register governs scope.** Duplicates stay with
  their owning vehicles; nothing is worked twice.
- **D-095-2 — sequencing.** Stage 0 is complete at adoption. Build
  stages run after Spec 094's build stages in the adopted queue:
  Spec 092 Stage 2, then Spec 094 build stages, then Spec 095 build
  stages, then Spec 091 Stage 1. (The register's closing line framed
  the queue the NEW items were sequenced against — Spec 092 S2, Spec
  094 build stages, Spec 091 Stage 1; the adoption inserts this
  spec's build stages between Spec 094's and Spec 091 Stage 1.)
- **D-095-3 — pinnability remediation is locate-first and
  fail-closed.** Digest mismatch against the PR #393 pin stops the
  remediation; no substitute corpus is admissible (every substitute
  was already rejected on Spec 053's and Spec 054's records).
- **D-095-4 — second targets are scoping only.** Eteocypriot and
  Meroitic enter as proposal and benchmark-scoping only; execution
  is a separate owner decision.
- **D-095-5 — the two confirmed-defect micro-fixes are not absorbed.**
  The RT-03 README supersession banner and the tracker stale ledger
  sentence are recorded in the Stage 0 record as owner-gated
  micro-tasks, not stage work.
- **D-095-6 — no frozen record is modified by the adoption; the
  claims intake rides inside the adoption PR** (the clean Spec 092
  pattern, PR #548 — explicitly not the Spec 094 #566 exception).

## 5. Bars fixed in the claims

- Fail-closed everywhere it is claimed: a digest mismatch stops
  (C095-2), a missing or mismatched corpus identity refuses the load
  (C095-3), the battery's twelve cases refuse or flag (C095-4), a
  planted stale claim blocks its release candidate (C095-14).
- Planted-fixture proofs, not inspections: the legacy-rule plant
  fails (C095-5), the synthetic-as-real plant fails (C095-6), the
  six historical contamination instances are re-detected from their
  records (C095-7).
- No frozen record moves: Spec 053's gates are unchanged in its
  re-execution (C095-2); the Indus record changes no fact, count, or
  standing under the multi-script instantiation (C095-11); earlier
  results keep the rules they were frozen under (C095-8).
- Owner gates stay owner gates: wireframes are approved by name
  before any dashboard build (C095-12); release-gate exceptions
  exist only as recorded owner-approved entries (C095-14); second
  targets execute only on a separate owner decision (C095-15,
  C095-16).
- The research loop stays off the live stores. Nothing in this spec
  lifts Spec 094's C094-13; if a stage ever needs the loop, that is
  Spec 094's closeout decision, not this spec's.

## 6. What adoption does and does not do

Adoption lands this package, enters C095-1..C095-17 into the claims
ledger through the importer inside this same PR (D-095-6), assigns
the spec in the program map, and records Stage 0 as complete with
its four deliverables cited. It commissions no build stage, moves
no claim's status, stage, or score, modifies no frozen record, and
sends nothing anywhere. The build stages run only in the adopted
queue (D-095-2), each on its own commissioning.
