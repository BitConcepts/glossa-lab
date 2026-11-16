# Spec 095 — plan

Stage 0 is complete at adoption (D-095-2). The build stages run in
the adopted queue: Spec 092 Stage 2 first, then Spec 094's build
stages, then this spec's build stages, then Spec 091 Stage 1. Each
build stage is commissioned separately; nothing in this plan starts
a stage by itself.

## Stage 0 — Reconciliation and register (COMPLETE 2026-11-15)

The review was reconciled against the program's records in four
passes before any spec was drafted: the register (43 rows, every row
dispositioned; 23 duplicates mapped to their owning vehicles; 14 NEW
items isolated), the pinnability pass (Priority 0 settled as a
placement defect with a fail-closed remediation), the public-surfaces
pass (one confirmed defect, one stale tracker sentence, one reviewer
tool limit), and the validator census (v2 modules test-only; four v1
node paths live and unguarded; exposure prospective). The adoption
itself (package, AEE assessment, ratification record, claims intake
inside the adoption PR) closes the stage. The two confirmed-defect
micro-fixes are recorded in the Stage 0 record as owner-gated
micro-tasks (D-095-5), deliberately outside the stages.

Discharge: C095-1 lands with the register's adoption; the stage's
remaining claims are the build stages'.

## Stage 1 — Corpus reproducibility (C095-2, C095-3, C095-4)

Locate `firestore_indusarrays_full.jsonl` (candidate venues are
checked read-only against the pin; the file's last recorded venue
was the desktop clone of 2026-10-25, a machine formatted 2026-11-09,
so custody snapshots and desktop-era archives are in the search set),
verify its digest against the PR #393 pin, place it read-only at the
canonical path, and prove the census and export pin reproduce
through the V3 loader. Then state the corpus identity standard and
make the covered loaders check it, and build the twelve-case
fail-closed battery as a named CI suite. Only after placement and
reproduction: Spec 053's step 0 re-execution under a new execution
order, gates unchanged.

Bars: any digest mismatch stops the stage cold (D-095-3); no
substitute corpus; the placed file is read-only; the battery's cases
refuse or flag as defined, in CI, on every covered-loader change.

## Stage 2 — Validator and synthetic containment (C095-5, C095-6)

Census the five corrected-validator families' consumers (the Stage 0
census covered the three named families at claim level; this stage
completes corpus_frames and replay076 to the same standard), then
migrate, retire, or mechanically guard each of the four live v1 node
paths, with the planted legacy-rule pinning test as the stage's
proof. Census every `indus_public_corpus` consumer, classify each,
machine-check the synthetic labelling, and plant the
synthetic-as-real fixture that must fail.

Bars: no v1 routine executable unguarded in a claim-bearing path at
stage close; both planted fixtures fail; the census names every
consumer found, or the stage does not close.

## Stage 3 — Evidence machinery (C095-7, C095-8, C095-9, C095-10)

Build the ledger-gate contamination class and prove it against the
six historical instances re-detected from their records. State the
equivalence and statistical-reporting standards once, program-wide.
Run the identifiability protocol's first application: rival
constructions against the six independently supported anchors, the
NOT IDENTIFIABLE amendment recorded, the six standings re-stated
under the outcome. Carry reading direction as data through the
claim-bearing corpora and re-issue the positional results the stage
touches with their orientation assumptions and reversed variants.

Bars: the gate class flags at intake, not in retrospect; standards
are stated once and cited, never restated locally; no reading is
scored SUPPORTED in this stage without a rival-construction record.

## Stage 4 — Platform and surfaces (C095-11, C095-12, C095-13, C095-14, C095-17)

Specify the seventeen-entity multi-script model with its own claims
and falsifiers and instantiate the Indus record unchanged. Build the
dashboard home and feature set wireframe-first (owner approves
wireframes by name; Playwright desktop and mobile verification
before any verified claim), each feature naming its refusals. Run
the functional and usability audit package on the Spec 083 vehicle,
scored against pre-fixed thresholds, failures filed with
screenshots, the accessibility pass included. Compose the
thirteen-component release gate and prove it with the planted
RT-03-shape stale claim. Produce the derived red-team document set
under its no-authority rule.

Bars: no feature ships unapproved or unverified; no release-gate
exception exists off the record; no Indus fact changes under the
instantiation; the research loop stays off the live stores
(C094-13 is Spec 094's to lift, not this stage's).

## Stage 5 — Second targets, scoping only (C095-15, C095-16)

Draft the Eteocypriot proposal and preregistration (corpus legal
status, bilingual and sign-list basis, held-out design, adjudication
route) and stop. Scope the Meroitic 2025-corpus reproduction
benchmark as a study spec on the existing fixture, with success
criteria and a falsifier fixed in the scoping record, and stop.
Execution of either is a separate owner decision (D-095-4) and is
not a stage of this spec. The spec's closeout (register re-check
against C095-1, every claim's discharge or named remainder) runs at
this stage's end.

## Cross-stage bars

- Verdicts come from records, never from delivery summaries; every
  stage files its own record in this directory before it is called
  done.
- Census re-pins and gate readings are recomputed from the machinery
  on the final tree of each change, never carried from a prior run.
- Nothing here touches a frozen record, a live store, or another
  spec's vehicle; collisions with an owning vehicle stop the task
  and go back to the register (C095-1).
