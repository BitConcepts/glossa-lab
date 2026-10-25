# Spec 075 — Adjudication at the freeze

**Status:** The record of how the design's
silences were filled by ruling at the drafting
of this spec, and of the verification the draft
was put through before the freeze. It is part
of the frozen record. The governing design is
`2026-10-25-endings-atlas-design.md` (the
depicted-kind endings atlas, Candidate B of the
Spec 071 redesign proposal of 2026-10-24,
designed in full 2026-10-25), read with the
owner's freeze order of 2026-10-25 ("do the
atlas freeze", 11:59 EDT) and the gate build
decision of the same date, which designates
this freeze the C4 shadow freeze.

---

## 1. The adopted basis

1. **The design is carried as written.** Its
   requirements R1–R13 map to the spec without
   remainder: R1 → §3 + gate 0.4; R2 → §1.1;
   R3 → §§1–2, 5; R4 → §4.2 + gate 0.4; R5 →
   §4.5 + gate 0.5; R6 → §§2, 4; R7 → §1.4;
   R8 → §§2.3, 4.4; R9 → §§4.5, 5.2; R10 → §5.1;
   R11 → §5.2; R12 → §§1.2, 5.5; R13 → §5.4.
   The two deviations the design itself states
   (from Spec 071 §4.2's comparison class, R8;
   and the keying-route choice it leaves open,
   its §9) are ruled at DD-075-4 and DD-075-5.
2. **Spec 071's frozen machinery is carried,
   not re-derived** (§§2, 4.5, 5.1, 5.3, 5.4):
   the ending and rate definitions, the
   frequency matching, the two-sided Fisher
   combination, the per-sign reporting, and
   the three sensitivity forms, applied per
   kind. Spec 071's question, claim, and
   governing text are not carried — the
   retirement stands untouched (§1.1, §9.6).
3. **The claim register is drafted directly in
   the recovered (0.7) form** — the round-trip-
   safe form established by Spec 071's §3 and
   used by Specs 073 and 074 — with an
   `independent_of` field on every evidence
   item and the ASM- assumptions defined in the
   register's own note. The AEE artifacts at
   the freeze are filed under `aee/` with the
   honest note Spec 074's freeze established,
   extended by this register's own record
   (DD-075-6).

## 2. Verification record (the drafting worker, first-hand)

Every measured quantity the spec pins was
recomputed by the drafting worker from the
files on main at the freeze base (379a9fc3),
before the spec text was finalized:

| Quantity | Recomputed | Spec pin |
|---|---|---|
| Asset A v2 SHA-256 / rows | 681e017d… / 552 | §3 ✓ |
| Asset A v2 kinds | other 246, unidentified 211, human 43, animal 30, object_goods 22, sky_cycle 0 | §3 ✓ |
| Asset A v2 dispute_status | none 548, borderline 4, contested 0 | §5.4 ✓ |
| Registry v2 SHA-256 / rows | 42ab09fb… / 1,013 | §3 ✓ |
| Registry v1 SHA-256 / rows | 8a0b2a82… / 803 | §3 ✓ |
| Crosswalk SHA-256 / rows | 4ace1a61… / 205 | §3 ✓ |
| Anchors SHA-256 | df0cf620… | §3 ✓ |
| Corpus SHA-256 / rows | 345241b1… / 5,704 | §3 ✓ |
| Grades SHA-256 / counts | 02394241… / 3,212 · 2,087 · 405 | §3 ✓ |
| Primary population | 3,045 rows / 557 signs / 550 in seq ≥ 2 | §3 ✓ |
| Corroborated population | 5,131 analyzable rows | §3 ✓ |
| Token 999 in primary | 2 rows / 2 occurrences | §4.3 ✓ |

The population construction was applied
exactly as §3 states it (grade string
`documented-lineage`; analyzable = symbol list
non-empty and not all-`000`; sequence = list
with `000` dropped) and reproduced the frozen
figures digit-for-digit — the design's
precondition for the study existing at all
(its §2) is met. No class census on the
population and no final-position quantity was
computed at drafting: the §6 pre-verification
flag states exactly this boundary.

## 3. Double derivation (the C2 spot-check)

The freeze's C2 record
(`gate-records/c2-spotcheck.json`) carries an
independent recomputation of every gate-turning
quantity plus the scaffold's sampled rest,
performed by a worker who did not draft this
spec, from the spec text and the pinned inputs
only. Its outcome is recorded in that record
and summarized in the freeze record; §2 above
is the drafting side of the pair. Any
unresolved mismatch on a gate-turning quantity
blocks this freeze under the gate's own rule;
none is resolved silently, here or there.

## 4. What this freeze decides

That the depicted-kind endings question, as
designed, is well-posed against the repaired
surface Spec 073 froze: its population
reproduces, its surface is pinned, its kinds
are the published identifications at measured
sizes, its celestial arm is honestly empty,
its falsifier is stated per kind in advance,
and its verdict words are frozen. The freeze
also files the strengthened gate's first full
run (C1–C3 records under `gate-records/`, C4 in
CI, C5 in the freeze record) as the designated
shadow freeze. The freeze decides nothing
about any kind's ending behaviour: no verdict
exists, and §6's flag states what was and was
not pre-verified.

## 5. Readings of the design fixed at drafting (rulings)

- **DD-075-1 — Where the design's silences are
  ruled.** The design (its §9) names the
  adjudication as the place its open points
  are decided at drafting. This document is
  that record; readings not ruled here are not
  readings of the spec.
- **DD-075-2 — Numbering.** Spec **075**,
  Phase **441**, verified next-free against the
  repo record at the freeze base (074 /
  Phase-440 last; no Phase-441 anywhere in the
  repo at the check).
- **DD-075-3 — The claim set.** Thirteen
  claims, F075-C01…C13, mapping the design's
  requirements one-to-one in substance. The
  verdict-bearing claims for the gate's C3 are
  F075-C03 (the headline hypothesis), C06 (the
  population), C07 (census and floors), C08
  (keying), and C11 (the verdict criteria) —
  the claims an outcome's words rest on.
- **DD-075-4 — The comparison class excludes
  the unidentified signs** (design R8, a stated
  deviation from Spec 071 §4.2). Ruled as the
  design states it: the question is kind
  against kind, the comparison is the other
  identified kinds at matched frequency, and
  §2.3 of the spec states the deviation in the
  open so no reader imports 071's rule.
- **DD-075-5 — The keying route is Spec 074's
  two-leg route** (DD-074-8), the one
  mechanical choice the design leaves open
  (its §9). Decided on Spec 074's executed
  record: the route keyed 31 of 31 there, and
  it is the route under which the surface's
  behaviour is measured fact rather than
  conjecture. §4.2 states both legs exactly.
- **DD-075-6 — The AEE record is filed as it
  ran.** This register drew, beyond the 13
  draft caps, 7 irreducibility and 2
  counterexample challenges under the pinned
  evaluator (aee 1.5.3) — a recorded difference
  from Spec 074's register, answered in
  `aee/freeze-aee-note.md` from the spec's own
  gate structure, not by rewording claims to
  silence a heuristic. The freeze proceeds on
  that record: the nine are advisory challenge
  records; no finding of contradiction,
  independence, ambiguity, or
  evidence-resolution kind appears in any hook
  artifact, and no claim scores below the 0.70
  threshold (minimum propagated 0.8695).
- **DD-075-7 — This freeze is the C4 shadow
  freeze** (gate build decision, 2026-10-25):
  the gate runs in full and is reported; the C4
  CI job must run and pass on the freeze PR;
  it is not yet a required branch-protection
  check, and this record does not call it one.

## 6. Defects found in drafting and fixed before the freeze

- **Register independence slip (fixed).** The
  first structural validation of `claims.json`
  caught one `independent_of` field (F075-C13,
  first evidence item) naming a source outside
  its own claim. Fixed to name the claim's
  other source; the register then validated
  clean (13 claims, every independence field
  exactly the claim's other sources).
- **Evaluator challenges (recorded, not
  fixed).** The 9 challenge findings of
  DD-075-6 were considered as drafting defects
  and ruled otherwise: they concern claim
  shape, each challenged claim carries one
  falsification test, and its decomposition
  lives in the spec's gates. They stand in the
  freeze record as the evaluator's findings.
- **Crosswalk filename in the freeze worker's
  own tasking (fixed).** The C2 recomputer was
  tasked with a file named
  `data/crosswalks/final_crosswalk.csv`, which
  does not exist; the spec's §3 names the sign
  crosswalk of record correctly
  (`data/crosswalks/sign_crosswalk_master.csv`),
  the recomputer found and used that file, and
  its digest and row count agree with the pin.
  The wrong name also appeared in this
  freeze's build_freeze.py inputs block and
  freeze test as first written; both were
  corrected to the spec's path before the
  digest was computed. The pinned quantity
  never differed — the defect was a filename
  in the worker's scaffolding, caught by the
  independent recomputation doing exactly its
  job, and recorded in the C2 record's notes.

## 7. What this freeze does not decide

No kind's verdict; whether the census clears
every floor (the floors are applied at an
execution's step 0, to the in-population
census — the asset-level counts of §2 are the
floors' basis, not their application); and
nothing about Spec 071's claim, the anchors,
any PRED-2026 state, or the preprint.

## 8. Freeze rulings

1. The spec, register, and this adjudication
   freeze as written, under the digest in
   `freeze.json`.
2. The gate records under `gate-records/` are
   part of the frozen record; the C5 statistics
   in `freeze.md` count this freeze as
   strengthened freeze #1 (shadow).
3. The OSF registration is filed on the merged
   freeze and approved by the proven route;
   the record keeps the registration id and
   DOI, never the approval-token URL.
4. Execution is a separate act. (Owner's
   order of 2026-10-25 12:03 EDT: execution
   begins when this freeze record is complete
   — freeze PR merged on genuine CI including
   the C4 job, OSF registration approved and
   verified, this record committed — under the
   frozen §6 gates, fail-closed.)

---

*AI disclosure: this adjudication was drafted
by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per
constitution §VI.*
