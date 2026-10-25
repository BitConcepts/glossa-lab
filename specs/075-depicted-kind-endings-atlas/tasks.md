# Spec 075 — Tasks

**Input**: spec.md + claims.json (13 claims,
F075-C01…C13) + adjudication.md of this
directory; the endings-atlas design
(2026-10-25); the freeze-gate build decision
(2026-10-25).

**Standing of this file**: the freeze freezes
the task list with the spec. The Lifecycle
section is the freeze's own work. The
Execution section is gated: it runs under the
owner's order of 2026-10-25 12:03 EDT once the
freeze record is complete (freeze PR merged on
genuine CI including the C4 job, OSF
registration approved and verified), and not
before; the freeze itself executes nothing.

---

## Lifecycle (this freeze)

- [x] T001 Verify the numbering: Spec 075 /
  Phase 441 next free at the freeze base
  (379a9fc3); verify every measured quantity
  the spec pins against main first-hand
  (Asset A v2 census and SHA; Registry v2 /
  v1 / crosswalk / anchors pins; corpus and
  grades pins; the population reproduced
  3,045 / 557 / 550 under §3's construction).
- [x] T002 Draft spec.md per the design's
  R1–R13: claim family F075 its own (not
  Spec 071's, not Hunt's); falsifier first;
  the celestial arm pre-registered EMPTY;
  classes, keying (two-leg route), floors,
  per-kind test and verdict words, the three
  sensitivities, step-0 gates 0.1–0.6 with
  the pre-verification flag, epistemic
  limits, outcome classes.
- [x] T003 Draft claims.json (13 claims) in the
  recovered (0.7) register form;
  `independent_of` on every evidence item;
  structural validation clean (one slip found
  and fixed — adjudication §6).
- [x] T004 Run the AEE hooks
  (after_specify / after_plan / after_tasks)
  with the pinned evaluator in the freeze
  configuration; file the six artifacts and
  the honest note under `aee/` (13 draft caps,
  7 irreducibility + 2 counterexample
  challenges recorded and answered —
  adjudication DD-075-6).
- [x] T005 Adjudication (this freeze's §5
  rulings DD-075-1…7) and this task list.
- [x] T006 Run the shadow gate package: C1
  battery on the pinned evaluator (result
  filed); C2 independent spot-check by a
  worker who did not draft the spec (record
  filed; any unresolved gate-turning mismatch
  blocks the freeze); C3 evidence sample with
  verification on (5 verdict-bearing + the
  scaffold's sample of the rest; record
  filed); C5 statistics regenerated for the
  freeze record.
- [x] T007 Build the freeze record: freeze.md
  (designation, pins, AEE section, gate
  section with the C1 blind spots verbatim and
  the C5 table, digest section, able-to-fail
  section, the closing pair), freeze.json via
  build_freeze.py (framework 0.2.6), and
  backend/tests/test_spec075_freeze.py
  replaying the record in CI (incl. the
  population and keying facts).
- [ ] T008 Commit the owner decision record
  (docs/decisions/2026-10-25-spec-075-freeze-decision.md)
  in the freeze PR; land the freeze PR on
  genuine CI green read from the run's own
  job conclusions, the C4 job passing on the
  complete gate-record set included.
- [ ] T009 File the OSF registration for the
  frozen spec on the merged PR; approve via
  the proven route (ORCID sign-in only; the
  direct token_action URL to the browser);
  verify approved + public via the OSF API;
  archive the registration's Gmail messages
  (mark read + archive, never delete); delete
  the spent approval-link file.

## Execution (gated — the owner's order of 2026-10-25 12:03 EDT, on the completed freeze record)

- [ ] E001 Build the instrument
  (`backend/scripts/phase441_depicted_kind_endings_atlas.py`
  in the Spec 074 pattern) implementing spec
  §6's gates and §5's battery exactly, and
  register its node in the experiment graph
  (`experiment_graph_phase441_*.py`); land on
  genuine CI.
- [ ] E002 Run step 0 (gates 0.1–0.6, in
  order, fail-closed) and publish the census
  (gate 0.5) before any rate exists; a gate
  failure closes the execution in its frozen
  word (§8) and is reported as the result.
- [ ] E003 Past a clean step 0: run the four
  per-kind primaries with their per-sign
  tables, then the sensitivities S1–S3 per
  kind, beside the primaries.
- [ ] E004 Write the outcome record
  (outcome.md in this directory, the celestial
  arm first per §5.5), the phase results and
  report under `reports/`; append to the
  programme ledger and to this spec's claim
  family (appends only — F075-C12); no pooled
  verdict minted (F075-C11).
- [ ] E005 Land the execution PR(s) on genuine
  CI 7/7; read the foundation check as
  measured at the merge and report it as
  measured.
