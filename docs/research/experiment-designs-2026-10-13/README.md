# Experiment designs for the 35 open claims — design packet, 2026-10-13

**Status: DESIGNS ONLY.** Nothing in this packet has been run, frozen, registered, or
approved for execution. Each design is written so it *could* be frozen later under the
program's normal flow (proposal first, then a numbered spec, a claims register, a freeze,
and — where the precedent requires it — a public registration before any run). This
packet is not a numbered spec and carries no verdicts.

**Owner order:** Tristen Pierson, 2026-10-13 — "Design experiments for all of the 35
that remain in question or inconclusive."

## What the 35 are

The 35 are the program's lane-2 claim set: 23 claims extracted from published work,
10 headline claims from the program's own studies, and 2 registered predictions
(PRED-2026-006 and PRED-2026-007). Every one of them now carries a human-adopted
explanation and a "what remains not understood" text (the lane-2 drafts in
`specs/029-tao-claim-lifecycle/lane2-drafts/`, PR #190, adopted by the owner as author
on 2026-10-13). Each design below answers the exact open point its claim's
not-understood text names. No design was invented to dodge a harder one the record
already prescribes.

## How to read a design

Every design states, in this order: the question in plain words; the hypothesis and
what would falsify it, stated **before** any method; the exact data (named, lawful,
with its rights posture); the method in enough detail to freeze; the success,
failure, and inconclusive criteria with their margins, fixed in advance; the controls
and the named confounders the result must beat; what stage or verdict the result could
move; and what the result would **not** establish even if it succeeds.

Feasibility classes:

- **RUNNABLE-TODAY** — the decisive test can run on lawful data already in hand.
  Some runnable designs carry a step-0 feasibility gate (a count that must clear a
  floor fixed in advance); if the gate fails, the design closes honestly at step 0
  and says so. That is a result, not a failure of the design.
- **PARTIAL** — a real arm runs today; the decisive arm is blocked on a named
  precondition.
- **BLOCKED** — the decisive test cannot run today. The blocking precondition and
  the exact act that would unblock it are stated. A blocked design is a complete
  deliverable: it tells the program what to watch for and what to do the day the
  precondition clears.
- **NO EXPERIMENT** — one entry (D-29) where the honest residue is not an
  experiment at all. It is recorded so the claim is not skipped silently.

House discipline these designs are written under: proposals before execution (H2);
every design states its epistemic boundary — what it cannot show (H13); no design
hardcodes an experiment outside the experiment-graph flow at execution time (H15/H23);
all data comes from the database or registered sources, never from values typed into
a script (H16); and no design uses the program's falsified semantic-anchoring (SA)
method as a gate for anything (H26). Where a design replaces an SA-based check, the
replacement is SA-free by construction.

## Classification of all 35

Classes: **SETTLED** (a verdict stands; the design addresses only the open residue
its not-understood text names) · **IN QUESTION** (a verdict or status stands on
evidence that is partial, inherited from the falsified SA machinery, single-lineage,
or missing its falsifier) · **INCONCLUSIVE** (the recorded verdict is literally
inconclusive) · **UNTESTED** (never checked).

| # | Claim | Recorded status | Class | Design |
|---|-------|-----------------|-------|--------|
| 1 | `farmer_sproat_witzel_2004_manual_001` | contradicted | SETTLED | D-01 (residue) |
| 2 | `indus_valley_script_deciphered_from_myth_65ff0a26_manual_002` | partially falsified | SETTLED | D-02 (residue) |
| 3 | `parpola_2010_dravidian_solution_manual_001` | partially supported, on the falsified SA method | IN QUESTION | D-03 |
| 4 | `parpola_2010_dravidian_solution_manual_002` | partially supported; family split (sign 72 passed, sign 267 failed) | IN QUESTION | D-04 |
| 5 | `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001` | partially supported (positions only) | IN QUESTION | D-05 |
| 6 | `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003` | partially supported (positional half only) | IN QUESTION | D-06 |
| 7 | `yadav_2009_arxiv_manual_001` | strongly supported | SETTLED | D-07 (residue) |
| 8 | `yadav_2009_arxiv_manual_002` | strongly supported, but the record carries no falsifier | IN QUESTION | D-08 |
| 9 | `indus_valley_script_deciphered_from_myth_65ff0a26_manual_001` (Roif ledger thesis) | untested | UNTESTED | D-09 |
| 10 | `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003` (arrow sign) | untested | UNTESTED | D-10 |
| 11 | `indus_valley_script_deciphered_from_myth_65ff0a26_manual_004` (horned deity) | untested | UNTESTED | D-11 |
| 12 | `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_002` (Hunt civic system) | untested | UNTESTED | D-12 |
| 13 | `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004` (sky signs) | untested | UNTESTED | D-13 |
| 14 | `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_005` (Translation Atlas) | untested; the atlas is not in the repository | UNTESTED | D-14 |
| 15 | `ancient_writing_and_modern_technologies_51831ac9_sign_val_0001` ("sign 900 = six") | untested fragment; sign list unnamed | UNTESTED | D-15 |
| 16 | `ancient_writing_and_modern_technologies_51831ac9_sign_val_0002` ("sign 700, unit of 40") | untested fragment; conflicts with #17 | UNTESTED | D-16 (shared) |
| 17 | `ancient_writing_and_modern_technologies_51831ac9_sign_val_0003` ("sign 700, unit of 4") | untested fragment; conflicts with #16 | UNTESTED | D-16 (shared) |
| 18 | `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001` ("sign 821, many contexts") | untested fragment; no testable proposition as written | UNTESTED | D-17 |
| 19 | `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002` ("sign 297, horned tiger") | untested fragment; sign list unnamed | UNTESTED | D-18 |
| 20 | `ancient_writing_and_modern_technologies_51831ac9_statisti_0004` (a heading, five sources) | untested fragment; no proposition stated | UNTESTED | D-19 |
| 21 | `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001` | fragment restating claim #1 | SETTLED (as a restatement of #1) | D-01 (residue) |
| 22 | `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002` | fragment restating claim #1 | SETTLED (as a restatement of #1) | D-01 (residue) |
| 23 | `without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001` | label restating claim #1 | SETTLED (as a restatement of #1) | D-01 (residue) |
| 24 | `STUDY-SPEC-019/PHASE-125` | FAIL — DISAGREEMENT; 93.9% of the disagreement unexplained | SETTLED | D-20 (residue) |
| 25 | `STUDY-SPEC-023/PHASE-132+383` | CONTRADICTED | SETTLED | D-21 (residue) |
| 26 | `STUDY-SPEC-024/F1` | SUPPORTED (joined subset of one lineage) | SETTLED | D-22 (residue) |
| 27 | `STUDY-SPEC-024/F2-HOLDAT` | CONTRADICTED at the declared margin | SETTLED | D-23 (residue) |
| 28 | `STUDY-SPEC-024/F3-ICIT` | SUPPORTED, one lineage, named confounders, other layer disagrees | IN QUESTION | D-24 |
| 29 | `STUDY-SPEC-025/G1` | SUPPORTED under control; chronology not controlled (the rider) | SETTLED | D-25 (residue) |
| 30 | `STUDY-SPEC-027/STAGE1-PHASE-392` | INCONCLUSIVE | INCONCLUSIVE | D-26 |
| 31 | `STUDY-SPEC-028/ARM-A` | INCONCLUSIVE | INCONCLUSIVE | D-27 |
| 32 | `STUDY-SPEC-028/ARM-B` | INCONCLUSIVE | INCONCLUSIVE | D-28 |
| 33 | `STUDY-SPECS-001-023+PHASES-TO-141` (audit rollup) | audit complete; 75 of 116 items reclassified | SETTLED | D-29 (no experiment — digestion-gated) |
| 34 | `PRED-2026-006` | "PARTIALLY CONFIRMED" in the register; the registered test itself was never run | IN QUESTION | D-30 |
| 35 | `PRED-2026-007` | "PARTIALLY CONFIRMED"; 2 of 3 on a population never enumerated | IN QUESTION | D-31 |

Counts: SETTLED 12 · IN QUESTION 8 · INCONCLUSIVE 3 · UNTESTED 12. Total 35.
Designs: 31 entries (D-01 to D-31) covering all 35 claims — D-01 carries the residue
for claims 1, 21, 22, 23; D-16 is one design for the rival pair 16 and 17.

Feasibility split: **RUNNABLE-TODAY 21** (D-02, D-03, D-04, D-05, D-06, D-08, D-09,
D-10, D-13, D-15, D-17, D-18, D-19, D-20*, D-22*, D-23, D-25, D-26, D-28, D-30,
D-31 — *carries a step-0 feasibility gate) · **PARTIAL 4** (D-01, D-07, D-21, D-27)
· **BLOCKED 5** (D-11, D-12, D-14, D-16, D-24) · **NO EXPERIMENT 1** (D-29).

## Shared input assets (built once, used by several designs)

Three designs' worth of work is really one dataset each, shared:

- **The published-identification sign classification** (D-05, D-06, D-13): which
  signs are animals, which are sky signs, which are objects — taken from published
  sign lists (the CISI volumes and Parpola's published identifications) and entered
  as cited data, frozen before any test uses it. Not new coding by this program:
  the identifications are the field's published ones, with the source named per sign.
- **The site-function classification** (D-09, D-10): the major sites classed by
  function (gateway/border, administrative, port, domestic, ritual) from the
  published excavation literature, as cited data with a two-source agreement rule,
  frozen before the tests. The Spec 027 Stage 0 gazetteer (36 source-asserted rows,
  30 site clusters) is the site spine it hangs on.
- **The object bridge** (D-20, and it raises the value of D-22 and D-26): pairs that
  tie the same physical object in the two great compilations, built through the
  Phase-130 intake schema from published concordance data. Phase-131 found zero
  shared object keys between the two digital layers; the bridge is the lawful route
  around that zero.

## Priority ordering — which designs earn their cost first, and why

Ranked by evidence value per unit of new assumption. The first three are the
recommendation; the rest of the order is in the file notes.

1. **D-30 — run PRED-2026-006 exactly as registered.** Near-zero cost and near-zero
   new assumptions: the registered criterion is mechanical (at least 70% of the
   CISI-trained opening signs show a start rate of 0.40 or more at Harappa), and the
   withheld data is verified in hand (the Yajnadevam inscription file in the
   repository: 5,679 inscriptions, 77 sites, 2,717 of them Harappa). A prediction
   registered in April 2026 has sat for six months scored on a neighbouring number
   instead of its own test. Closing that gap is the cheapest honesty the program
   can buy.
2. **D-03 — the SA-free rerun of the Dravidian-versus-rivals comparison.** The
   program's most prominent language claim stands at "partially supported" on
   evidence produced by a method the program itself falsified (held-out score
   0.000, 0 of 115). Every month that status stands unre-earned, the claim borrows
   credibility the program no longer believes in. The rerun needs no new data —
   the strict sign set and the corpora are in hand — and its result moves the claim
   decisively in one direction or the other.
3. **D-20 — the matched-object attribution of the Phase-125 disagreement.** The
   93.9% unexplained disagreement between the two great compilations is the single
   largest open risk in the program: every positional claim (claims 4, 5, 6, 8,
   and indirectly the whole study line) is computed inside one compilation while
   the other compilation disagrees by an amount nobody has explained. The CISI
   catalogue layer, the 44 Phase-128 dossiers, and the Phase-130 intake schema
   are all in hand; the design's step-0 gate states honestly whether the bridge
   they can build is thick enough to judge.

Then, in order: D-31 (finish PRED-2026-007's population — nearly as cheap as D-30),
D-25 (the chronology-controlled site test — the 205-row extended spine built by
Spec 030 is the first asset that makes it possible), D-28 (Arm B split by object
type, as a registered primary test), D-08 (give the falsifier-less positional claim
its falsifier and rerun), D-04, D-05/D-06/D-13 (one shared classification build,
three tests), D-26, D-23, D-22, D-02, D-09/D-10 (one shared classification build),
D-15/D-18/D-19/D-17 (identification and re-extraction desk work), D-07 arm A,
D-27 arm A (the precision target), D-21 arm A (disagreement mechanism on existing
pilot data). The BLOCKED designs (D-11, D-12, D-14, D-16, D-24) and the blocked
arms (D-01, D-07 arm B, D-21 arm B, D-27's decisive rerun) wait on their named
preconditions; D-29 waits on human scholarly engagement, which is not an
experiment and is not this packet's to schedule.

## Files

- `01-language-and-position.md` — D-01, D-03, D-04, D-07, D-08
- `02-roif-and-hunt.md` — D-02, D-05, D-06, D-09, D-10, D-11, D-12, D-13, D-14
- `03-fragments.md` — D-15, D-16, D-17, D-18, D-19
- `04-study-headlines.md` — D-20 to D-29
- `05-predictions.md` — D-30, D-31
