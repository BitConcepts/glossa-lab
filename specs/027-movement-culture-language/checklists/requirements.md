# Spec 027 — Requirements Checklist

> DRAFT checklist for owner adjudication. A checked item means
> the draft states or structures the requirement; it does not
> mean a future stage has executed it.

## Specification quality

- [x] CQ-1 The draft is bannered DRAFT — PROPOSAL FOR OWNER
      ADJUDICATION and states that it authorizes nothing.
- [x] CQ-2 Epistemic boundaries are explicit (spec §12, H13),
      including assumptions, adversarial challenges, and the
      secondary status of the movement research report.
- [x] CQ-3 The hard limits in spec §10 are stated as stop
      conditions, including the absolute PRED/decipherment fence.
- [x] CQ-4 No phase number is reserved and no stage is described
      as frozen.

## Claim governance

- [x] CR-1 Every governed claim has a stable `F027-C…` ID in
      `claims.json`.
- [x] CR-2 Every claim carries a layer (`O`, `I`, `M`, or
      `Interp.`), boundary, assumptions, dependencies,
      forbidden assumptions, strongest rival, falsifier,
      evidence origin groups, and verdict rule.
- [x] CR-3 The verdict taxonomy is exactly INVALID /
      INCONCLUSIVE / CONTRADICTED / SUPPORTED, and
      NOT-YET-TESTABLE is defined as a registration status.
- [x] CR-4 Poseidon and AADR are assigned one origin group for
      shared samples; aggregators do not create origin groups.
- [x] CR-5 The claim register passes the Spec 026 integrity
      check (cycles, missing dependencies, forbidden
      inheritance).

## Stage 0

- [x] CR-6 The gazetteer unit is a source assertion, with
      `source_gazetteer`, locator, published period scheme, and
      licence state required on every row.
- [x] CR-7 Coordinate precision/restriction states are defined,
      and restricted coordinates cannot be republished more
      precisely than the source allows.
- [x] CR-8 Sources that are not lawfully reusable are
      catalogued, not copied.
- [x] CR-9 The chronology spine requires dated material,
      context association, calibration/version, and origin
      tracing; aggregate period labels are not timing rows.
- [x] CR-10 Charcoal versus short-lived sample status and
      old-wood risk are explicit audit fields.
- [x] CR-11 Mutin et al. (2025) is carried as CONTESTED, with
      competing chronology assertions preserved.

## Stage 1

- [x] CR-12 Q2 is stated as the gate for all downstream
      repertoire-geography work, with a designed negative
      closure.
- [x] CR-13 The Q2 null is pre-declared: after rarefaction and
      object-type stratification, site explains no more
      variation than permuted site labels under the frozen
      design.
- [x] CR-14 `sign_list_version` is a required field; M77,
      Parpola/CISI, and Wells/ICIT-native numbering are stated
      as not interchangeable.
- [x] CR-15 Corpus rules requiring a freeze are enumerated:
      governing list, crosswalks, object inclusion, damage and
      multi-line handling, duplicates, unmapped signs, minimum
      support, and lineage.
- [x] CR-16 Rarefaction, permutation strata, practical margin,
      interval reporting, and leave-one-site-out jackknife are
      required in the Stage 1 freeze.
- [x] CR-17 Positive and negative discriminating controls are
      required; a non-discriminating control maps to INVALID.

## Stage 2 and blocked questions

- [x] CR-18 Q7 and Q6 are separate conditional designs, each
      requiring its own freeze.
- [x] CR-19 Q7's licensed conclusions are limited to objects,
      materials, and techniques; no people claim is licensed.
- [x] CR-20 Q6 may proceed only if the Stage 0 chronology
      support conditions are evidenced before timing outcomes
      are inspected.
- [x] CR-21 Q1's mobility arm is registered NOT-YET-TESTABLE
      with the ≤3-site coverage blocker and ecological-fallacy
      fence.
- [x] CR-22 Q3 is registered blocked on new paired primary
      isotope/aDNA data that this program cannot generate.
- [x] CR-23 Q4 is registered blocked, with its fallback and
      weaker verdict ceiling stated.
- [x] CR-24 Q5 is registered blocked on primary chronology
      replication; Mutin et al. is not silently adopted.
- [x] CR-25 Q8 is registered blocked on at least two blind
      human etymologists; AI coding is expressly not a
      substitute.
- [x] CR-26 Q9 is registered with the advance possibility that
      it remains not-yet-testable.

## Hard limits and lifecycle

- [x] CR-27 No gene→language identification, backward ethnic
      projection, object→mass-migration inference, later-text
      transcript claim, package deal, teleology join, silent
      model-shopping, or absence upgrade is permitted.
- [x] CR-28 Mobility/context evidence is barred from sign
      readings, anchors, and PRED-2026 scoring.
- [x] CR-29 AEE assess and evaluator-contract outputs are
      saved after specify, plan, and tasks; stricter-than-warn
      outcomes require recorded recovery.
- [x] CR-30 Tool versions and the known AEE version split are
      recorded in `working/tooling.md`.
- [x] CR-31 Future phases are required to follow H15/H23
      graph-first order under their own freezes.
- [x] CR-32 The five owner decision asks are stated verbatim
      in spec §13 and in `tasks.md`.

## Traceability

| Requirement | Checklist items | Task path |
|---|---|---|
| FR-027-1 | CR-1…CR-5 | L2, L9, S0-1, S1-2 |
| FR-027-2 | CR-6…CR-8 | S0-2…S0-4 |
| FR-027-3 | CR-9…CR-11 | S0-5…S0-6 |
| FR-027-4 | CR-6, CR-21…CR-26 | S0-7 |
| FR-027-5 | CR-12…CR-17 | S1-1…S1-5 |
| FR-027-6 | CR-14…CR-15 | S1-1…S1-2 |
| FR-027-7 | CR-17 | S1-2…S1-4, S2A-2, S2B-2 |
| FR-027-8 | CR-18…CR-19 | S2A-1…S2A-3 |
| FR-027-9 | CR-18, CR-20 | S2B-1…S2B-3 |
| FR-027-10 | CR-21…CR-26 | B1…B6 |
| FR-027-11 | CR-4 | S0-1, S0-3, S0-5 |
| FR-027-12 | CR-29…CR-31 | S0-1, S1-2, S2A-2, S2B-2 |
| FR-027-13 | CR-31 | S1-3 and each later stage freeze |
| FR-027-14 | CR-29…CR-30 | L4, L6, L8 |
| FR-027-15 | CR-27…CR-28 | X2 and every stage closeout |
