# Designs 05 — the two registered predictions

PRED-2026-006 and PRED-2026-007 stand in the register as PARTIALLY CONFIRMED.
The Spec 029 audit flagged that wording as acceptance-flavoured, and the
adopted lane-2 texts state the gap plainly: in both cases a neighbouring
quantity was measured instead of the registered test. These two designs do
the simplest thing in this whole packet — they run the registered tests,
exactly as registered, at full scope. Where a design finds the registered
test cannot be run as written, it says so and gives the reason; it does not
substitute a friendlier test.

Scoring either prediction follows the register's own discipline: the
outcome, whatever it is, is appended to the register as a dated entry. The
register's existing text is never edited.

---

## D-30 — PRED-2026-006: the Harappa breakdown, computed exactly as registered

- **Claim:** `PRED-2026-006` (IN QUESTION — registered 2026-04-22; the number
  on record, 72.7% stability for the INITIAL class, is a global figure across
  sites; the register itself says "Harappa-specific breakdown pending").
- **Feasibility:** RUNNABLE-TODAY. The withheld data was verified in hand on
  2026-10-13 (see Data).

**The registered test, quoted in substance.** Prediction: signs assigned to
the INITIAL class in CISI Mohenjo-daro will appear preferentially in initial
position in Harappa-specific Yajnadevam data as well. Withheld data:
Harappa-site Yajnadevam sequences, held separate from the full-corpus
analysis. Success criterion, fixed at registration: **at least 70% of the
CISI-trained INITIAL signs show a start rate of 0.40 or more at Harappa.**

**Step 0 — provenance checks (the design fails closed here).** Three things
are verified from the record before any counting, and each has a stated
failure outcome:

1. **The trained INITIAL set.** The exact set of signs the CISI
   Mohenjo-daro training produced (the lineage of the recorded
   global_class_stability.py check) is reconstructed from the program's
   records and frozen as a list. If the exact trained set cannot be
   reproduced from the record, the design closes as CANNOT BE RUN AS
   WRITTEN — a similar set built fresh would be a different prediction, and
   registering it would require a new PRED number under the register's own
   rules. The design does not improvise one.
2. **The withholding was real for this purpose.** The Yajnadevam corpus has
   been loaded by the program before (Phases 281–293 used it for unrelated
   decipherment work). The design records that exposure openly and verifies
   the narrower fact the registration actually depends on: the INITIAL
   class assignments came from CISI Mohenjo-daro, and the Harappa
   Yajnadevam sequences played no part in training them. If that cannot be
   verified, the closure is again CANNOT BE RUN AS WRITTEN, with the reason.
3. **Sign identity.** Yajnadevam's sign codes are Mahadevan-style codes;
   the trained INITIAL signs are CISI/Mahadevan signs. The mapping between
   them uses the program's existing crosswalks (the Yajnadevam crosswalk
   files under `data/crosswalks/`), fixed before counting. Any trained
   INITIAL sign with no crosswalk counterpart is counted and reported as
   UNMAPPABLE; if unmappable signs exceed 20% of the trained set, the
   verdict is reported with that coverage stated in its first sentence.

**Data.** The withheld set, verified in hand: `backend/glossa_lab/data/
yajnadevam_inscriptions.csv` — 5,679 inscriptions, 77 sites, of which
**2,717 are Harappa** (census counted 2026-10-13 for this design; the
registered computation itself has never been run). Each row carries its
site, sign sequence, and CISI object reference. Rights posture: the file is
Yajnadevam's publicly released lipi dataset, already held and used by the
program; derived statistics are publishable, and the design publishes
statistics, not the dataset.

**Method.** Exactly the registered computation, nothing added: for each
sign in the frozen trained INITIAL set, its start rate at Harappa = the
share of its Harappa occurrences (in the withheld sequences, through the
frozen crosswalk) in which it stands in initial position. Count the signs
with start rate at or above 0.40. Divide by the number of trained INITIAL
signs (with the unmappable handling of step 0.3 stated in the output).
Compare to 70%.

**Criteria.** These are the register's, not this design's: **CONFIRMED** if
the share is at least 70%; **NOT CONFIRMED** if below. There is no
inconclusive band in the registered criterion and this design does not
invent one; the only soft landings are the step-0 closures (CANNOT BE RUN
AS WRITTEN, UNMAPPABLE coverage), each reported as itself, not dressed as a
verdict. One descriptive addition is pre-registered so it cannot be
mistaken for a criterion: the per-sign table (every trained sign, its
Harappa count, its start rate) is published with the outcome, so the
small-denominator risk the claim's not-understood text names — whether the
withheld material is large enough for the rule to be meaningful sign by
sign — is visible to any reader.

**Controls and named confounders.** Within-lineage caution, stated in the
verdict wording: the Yajnadevam compilation's object base is itself
published-corpus material, so the independence this test has is the
*site-withholding* the registration specified — Harappa held out of
training — not independence of scholarly lineage. The design claims the
first and not the second. Crosswalk conflicts: conflict-pair signs are
flagged in the per-sign table. Sequence-length composition at Harappa
differs from Mohenjo-daro's; the registered criterion does not adjust for
it, so neither does the design — the composition is described alongside.

**What it would move.** The prediction from IN QUESTION to scored — the
first time since April 2026 that its register entry would rest on its own
test. Either outcome is valuable: confirmation retires a six-month caveat;
non-confirmation corrects a "PARTIALLY CONFIRMED" that the evidence never
carried.

**What it would NOT establish.** Anything beyond the registered statement:
that opening signs are stable at Harappa in this dataset. Not why, not what
the signs mean, and not stability at any other site.

---

## D-31 — PRED-2026-007: every ITM sign, not three of them

- **Claim:** `PRED-2026-007` (IN QUESTION — registered 2026-04-22; recorded
  test in full: three ITM-coded signs checked, two in TERMINAL clusters,
  67% against the 70% bar; the register's own note says "one more ITM
  needed for full pass", and the total number of ITM signs has never been
  recorded).
- **Feasibility:** RUNNABLE-TODAY, with a step-0 enumeration that may
  honestly shrink the design (stated below).

**The registered test, quoted in substance.** Prediction: signs with the
ICIT function code ITM will cluster into the TERMINAL class in the CGSA
Phase 5 clustering at a rate of at least 70%. Success criterion: **at
least 70% of ITM-coded signs are TERMINAL or cluster in TERMINAL
clusters.**

**Step 0 — enumerate the population, and fix the code table's provenance.**
The register says the function codes come "from mayig features". Verification
for this design (2026-10-13) found the record fuzzier than that: the 396
mayig feature files under `data/raw/other_sites/mayig_features/` carry
visual features and grapheme lists per sign — they contain no function
codes at all — while the program's parser (`backend/glossa_lab/data/
fuls_parser.py`) reads the function codes (NUM, LON, SHN, TMK, ITM, LOG,
SYL) from a Wells-derived source text. Step 0 therefore: locate the
authoritative function-code table among the program's held sources,
enumerate **every** ITM-coded sign from it, and record the enumeration
with its source — including an appended note reconciling the register's
provenance line with what the files actually contain (the register text
itself is not edited; the reconciliation is a dated addition, per register
discipline). Failure outcome, stated in advance: if the only ITM signs
enumerable from any held source are the three already tested, the design
closes with that census as its finding — the registered test then *has*
been run at full scope, its outcome is 2 of 3, and the register entry is
appended accordingly. That is a completion, not a failure.

**Method (if the population exceeds three).** For every enumerated ITM
sign, take its cluster assignment from the recorded CGSA Phase 5 output —
the same clustering the registered test specifies; no re-clustering, since
re-running the clustering until the memberships please someone would be
exactly the post-hoc freedom registration exists to prevent. (If Phase 5's
recorded output does not survive in a form that assigns clusters to signs,
that fact is reported and the design closes as CANNOT BE RUN AS WRITTEN —
a fresh clustering is a new prediction's business, under a new number.)
Count TERMINAL-cluster memberships; divide by the enumerated population.

**Criteria.** The register's: **CONFIRMED** at 70% or above; **NOT
CONFIRMED** below. Coverage rule, fixed in advance: if some enumerated ITM
signs have no recorded Phase 5 assignment, the share is computed on the
assigned population and the coverage is stated in the verdict's first
sentence — *unless* the unassigned signs cannot change the outcome
arithmetically (the bar already reached even if all unassigned are
non-TERMINAL, or unreachable even if all are TERMINAL), in which case the
verdict is decisive and the coverage is still stated. If coverage is below
80% and the outcome is not arithmetically decisive, the appended entry
records the test as run-at-partial-scope with the numbers — the register's
PARTIALLY CONFIRMED wording is replaced by the precise statement, which is
the point of running it.

**Controls and named confounders.** Clustering stability: the claim's
not-understood text notes cluster membership is being asked to carry
weight while the program's cross-compilation work shows sign treatment is
contested; the design's answer is fidelity, not repair — the registered
test named this clustering, so this clustering is what gets scored, and
the caveat rides in the appended entry. Small-population arithmetic: with
a population in the single digits, each sign is worth double-digit
percentage points; the per-sign table (every ITM sign, its cluster, its
class) is published with the outcome so no reader has to trust a bare
percentage. The LOG-coded P098 that appears in the register's note is not
an ITM sign and is excluded from the count, as it was in the recorded test
— stated here so the exclusion is a rule, not a convenience.

**What it would move.** The prediction from IN QUESTION to scored at full
enumerated scope — or to a precise statement of why its scope cannot be
enlarged, which is the other honest ending.

**What it would NOT establish.** That ITM signs *mean* anything terminal,
or that the Phase 5 clustering carves the script at its joints. It scores
one registered prediction about one coding scheme inside one clustering —
no more, and the appended entry will say no more.
