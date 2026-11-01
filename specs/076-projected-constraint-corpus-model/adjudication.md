# Spec 076 — Adjudication (drafting record and freeze rulings)

This record carries the drafting decisions for Spec
076, the projected-constraint corpus model (method
M12), from its design draft (2026-10-26, programme
goal record, SHA-256 8945399d7621f9db9286ce3773538c0b9821a93f07d400556366fe0a474a4122)
to this freeze, under the owner's order of
2026-10-26 06:51 EDT ("Freeze and run the M12
pilot"). The design is carried as written; the
only additions are the freeze-fixed completions of
§2 below — places the design itself left open for
the freeze to close — each stated in spec §0 and
ruled here. No bar, threshold, frame, null, or
closure word of the design was moved.

## 1. Provenance

- The method is the owner's proposal of 2026-10-26:
  use a projected-constraint model for the language
  to understand what we have and demand what must
  be true of the missing signs. The design draft
  (M12, the next free M-number; M10 is "the
  carver's evidence", M11 is "dated drift") was
  written the same day, design only, with its
  worked example recomputed from the pinned
  records and its pilot designed but not run.
- The freeze order is the owner's, 2026-10-26
  06:51 EDT. The pilot executes under FF-5 after
  this freeze merges.

## 2. Verification at drafting (the freeze worker's own derivation)

The freeze worker re-derived the §7 census from the
pins as fetched from repo main (export SHA-256
08fc96c8…; anchors df0cf620…; Registry v2
42ab09fb… — each recomputed and equal to its pin)
before drafting this spec. Every pre-named figure
of the design reproduced exactly: 2,906 records;
680 placeholder + 452 marked tokens dropped;
11,507 tokens; 5,883 strict tokens; slot totals
2,655 / 2,655 / 225 / 5,972; the finals partition
1,707 / 250 / 520 / 178 summing to 2,655; 122 U2
signs holding 1,825 tokens and 178 finals; 677
(sign, type) exclusions over U2 with the size
distribution 14 / 29 / 23 / 56; the solo-only set
of 13 (031 ×2, 378 ×2, eleven ×1); the rows of
signs 358, 342, 276, 031 and their possibility
sets; the 24 absent signs as listed; 2,558 attested
ordered pairs of 154,449. The C2 record carries
the independent recomputation by a worker who did
not draft the spec.

## 3. Freeze rulings

- **DD-076-1 — Numbering and phase.** This freeze
  consumes **Spec 076** (the next free spec number
  after 075) and **Phase 442** (sequential after
  Spec 075's Phase 441). Directory:
  `specs/076-projected-constraint-corpus-model`.
  Experiment id: `spec076-projected-constraint-corpus-model`.
- **DD-076-2 — The claim set.** The register
  carries ten claims, F076-C01…F076-C10: the
  design's D-M12-C01/C02/C03 as C01/C02/C03; the
  standing assumptions A-FRAME / A-DIR / A-FACE /
  A-KEY as C04…C07 (the design's §3.1 requires each
  assumption filed as a claim with its own
  falsifier); the pilot's positive-control
  calibration as C08; the design's output
  discipline and non-claims as C09/C10. F076-C02
  is pilot-gated: it is filed as a supported claim
  only on a pilot pass.
- **DD-076-3 — Freeze-fixed completions.** FF-1
  (shuffle seed 20261026), FF-2 (step-3 coding
  rules CR-1…CR-7), FF-3 (the resolution-value
  operationalisation), FF-4 (the A-KEY
  clarification), FF-5 (pilot execution order) are
  adopted as spec §0 states them. Each closes a
  place the design expressly left to the freeze
  ("seed fixed in the freeze text"; "coding rules
  fixed in the freeze text"; "computed from the
  coupling edges by the frozen rules"). CR-6 errs
  toward the control being able to fail. CR-7
  exists because 5 of the 94 strict signs are
  frame-absent (039, 044, 046, 362, 374): a frame
  cannot exclude a claimed type for a sign it does
  not contain, and counting those signs either way
  would rig the bar.
- **DD-076-4 — The A-KEY clarification (FF-4).**
  The design's A-KEY text, read flat, would exclude
  the rows of the 13 duplicated Mahadevan ids from
  the deductive layer — but Spec 073's accounting
  locates the duplication on the registry's
  cross-scheme join surface (each id claimed by two
  *Parpola-keyed rows*), and the design's own §7
  derivation — whose numbers the pilot's step 0
  must reproduce — excludes no frame row. The two
  readings cannot both stand. Ruled: the §7
  derivation governs (it is the design's worked,
  reproduced substance); A-KEY's exclusion applies
  to derivations that join through `mahadevan_ids`,
  of which the pilot performs none; attested
  members of the 13 are flagged in the register.
  This is recorded here as a ruling on the design's
  internal tension, not a silent edit: spec §3.2
  carries the design's A-KEY text with the FF-4
  application stated beside it.
- **DD-076-5 — No OSF registration at this
  freeze.** Specs 074/075 filed their own OSF
  registrations at their freezes under their
  designs' provisions. The M12 design's filing
  provisions name no OSF registration (its §11
  claims and §13 dependencies are silent on OSF).
  Per the freeze order's instruction — where the
  draft names an OSF registration, file it; where
  it is silent, the repo freeze record governs —
  no OSF registration is filed for Spec 076, and
  the absence is recorded here and in freeze.md
  rather than improvised around. A later filing
  remains possible as its own act; nothing in the
  pilot depends on it.
- **DD-076-6 — The S5 sentence.** The design's §4
  table gated the depiction source's deductive use
  on "the owed C-1 computation". That computation
  ran on 2026-10-26 (exploratory; goal record
  2026-10-26-c1-settling-sensitivity.md) and found
  Spec 075's human verdict pooling-sensitive. Spec
  §4/§9 carry that updated standing; the pilot does
  not use S5 at all, so the update touches no bar
  and no derivation.
- **DD-076-7 — This freeze is a required-C4
  freeze.** The C4 records check is a required
  branch-protection check (owner act of 2026-10-25,
  after the 075 shadow freeze). The gate records
  under `gate-records/` are filed beside this
  record and must pass the C4 job in CI on the
  freeze PR.

## 4. What was not changed

The bars of §8 (residual below the null's 5th
percentile; solo-only count above its 95th; step-3
exclusions ≤ 5), the null (marginals-preserving
shuffle, B = 999; label permutation named invalid),
the frame and its pins, the closure words, the
three-tier discipline, and the non-claims of §12
stand exactly as the design wrote them. The
pilot's statistics were not recomputed in any
exploratory form at drafting or at this freeze:
the only computations performed are the census
reproductions the design itself prints in §7 and
the gate's C2 recomputation of the same figures.

## 5. Establishes / does not establish (adjudication)

This adjudication establishes that the design was
carried into frozen form without moving any of its
bars, with its open places closed on the record and
its one internal tension (A-KEY) ruled in the open.
It does not establish that the pilot will pass, that
any register entry is true of any frame beyond its
pins, or anything about what any sign means.
