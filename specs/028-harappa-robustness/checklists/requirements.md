# Spec 028 — Requirements Checklist

> A checked item means the spec states or structures the
> requirement; it does not mean execution has occurred.

## Specification quality

- [x] CQ-1 The spec is bannered FROZEN UNDER DELEGATED
      ADJUDICATION and the owner's verbatim order is
      recorded in `adjudication.md`.
- [x] CQ-2 Epistemic boundaries are explicit (spec §10,
      H13), including assumptions, adversarial challenges,
      and inherited limitations (period uncontrolled;
      multi-line unrecorded).
- [x] CQ-3 The hard fences are stated as stop conditions:
      no Phase-392 edit, no pooled headline, no Arm C
      verdict, no anchor/PRED contact.
- [x] CQ-4 The phase number (393) is the first free number
      in the repository's registered phase space, verified
      against the tree.

## Claim governance

- [x] CR-1 Every governed claim has a stable `F028-C…` ID
      in `claims.json` (16 claims).
- [x] CR-2 Every claim carries a layer, boundary,
      assumptions, dependencies, forbidden assumptions,
      strongest rival, falsifier, evidence origin groups,
      and verdict rule.
- [x] CR-3 The verdict taxonomy is exactly INVALID /
      INCONCLUSIVE / CONTRADICTED / SUPPORTED, applied per
      arm; NOT-YET-TESTABLE and NOT ESTIMABLE are statuses.
- [x] CR-4 The register passes the Spec 026 integrity check
      (cycles, missing dependencies, forbidden inheritance).
- [x] CR-5 The ICIT-lineage corpus is counted as one origin
      group; Phase-392's record is governance evidence, not
      independent corroboration.

## Freeze inputs

- [x] CF-1 The margins audit reproduces the Phase-392 frozen
      counts exactly and contains no outcome field
      (test-pinned).
- [x] CF-2 Arm A and Arm B estimability is determined on
      margins before the freeze (both ESTIMABLE; support
      numbers in `margins-audit.json`).
- [x] CF-3 Calibration is synthetic-only, runs through the
      pipeline the execution will use, and both arms'
      controls PASS before the freeze merges.
- [x] CF-4 The calibration-forced design refinement
      (permutation strata) is recorded as a numbered freeze
      amendment with its synthetic evidence and diagnostic.

## Design

- [x] CD-1 Arm A's bounded claim, population, draw,
      jackknife, and sensitivity are frozen (spec §5.1).
- [x] CD-2 Arm B's bounded claim, equal-quota construction,
      and allocation rule are frozen exactly (spec §5.2).
- [x] CD-3 Arm C's descriptive outputs are enumerated and
      fenced (no p-values, no margin, no verdict).
- [x] CD-4 Multiplicity is frozen: hierarchical, Arm A
      primary, Arm B secondary, no pooled headline.
- [x] CD-5 Verdict rules are mechanical and per arm
      (spec §5.5), including the named INCONCLUSIVE case.
- [x] CD-6 One fresh seed (20261012) is pre-declared for
      all arms, controls, jackknives, and sensitivities.

## Execution and closeout

- [x] CE-1 The OSF registration of the frozen contract is
      sequenced after the freeze merge and before
      execution (FR-028-5), with the URL recorded.
- [x] CE-2 The H23 order (script → graph module →
      registration → verification → run) is a task gate.
- [x] CE-3 Population reproduction is asserted in the run
      before outcomes; mismatch stops the run as INVALID.
- [x] CE-4 Decisive numbers are recomputed from the
      results JSON before being reported.
- [x] CE-5 Closeout verifies the full suite, the
      foundation check, anchor byte-identity, and zero
      PRED contact on merged main.
