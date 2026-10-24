# Spec 054 — Amendment draft (2026-10-23): the falsifier act under battery NB-1

> ## AMENDMENT — FOR OWNER MINI-GATE — 2026-10-23
>
> Drafted under Item 3 of the owner-approved
> waiting-decisions package of 2026-10-23, on the
> rulings recorded in `adjudication.md` §8. This
> amendment is a draft: it returns to the owner as a
> mini-gate, and nothing in it freezes, files,
> appends, or executes Spec 054. Where this amendment
> and the unamended draft disagree, the amendment
> governs once the owner approves it; until then the
> draft stands as written, with its freeze failure of
> 2026-10-21 as the operative record.

## 1. What this amendment does

The 2026-10-21 freeze attempt failed (`adjudication.md`
§7): the battery could not be pinned out of the
Phase-43 record (OPEN-054-1); the original opening and
closing sets could not be exhibited (OPEN-054-2 — the
closing set 10 of 20 exhibited, the opening set 0 of
40); and the claim the spec exists to give a falsifier
to — `yadav_2009_arxiv_manual_002`, "there are specific
text-beginning and text-ending signs in the Indus
corpus", strongly supported — carries no
`falsification_condition` on its record, so there was
nothing for a freeze to register as the falsifier's
existence proof, and (§7.3) a direct append to the
claim store would have been silently dropped by the
next regeneration of that store.

The owner's rulings of 2026-10-23 (`adjudication.md`
§8) settle the design. This amendment:

1. Defines the **amended statement** the run evaluates
   (§2) and the new battery, **NB-1**, that evaluates
   it (§3) — the same battery Spec 052's amendment
   defines, stated here in full so this spec freezes
   on its own text.
2. Specifies the falsifier's decision procedure
   completely: the two arms and their data (§4); the
   sets, the reappearance measure, the overlap null,
   the precedence rule, and the denominator discipline
   (§5); the step-0 gates and closures (§6).
3. Records the **generator act** (§7): the claim-store
   fix that gives the appended falsifier a durable
   home — decided by the same ruling, prepared in this
   amendment's PR, and proven both ways before it is
   proposed.
4. Fixes the **exact falsifier text** the amended
   freeze will append (§8), and the **verdict
   wordings** the run will use (§9) — rewritten, with
   no RE-EARNED anywhere.

What it does not do: it does not edit the parent claim
record in any way (the append is the amended freeze's
act); it does not claim the original Phase-43 sets can
be recovered, re-derived, or re-earned — OPEN-054-2's
finding stands, and the amended SUPPORTED wording says
so; it allocates no phase number (Phase-417 was never
allocated; allocation stays a freeze act).

## 2. The amended statement

The amended spec evaluates this statement:

> There are specific text-beginning and text-ending
> signs in the Indus corpus, in the following exact
> sense: under battery NB-1 (§3), the strict corpus
> (arm 1) has both a non-empty **opening-strong set**
> and a non-empty **closing-strong set**; each set
> **reappears** in the Holdat layer (arm 2), through
> the pinned crosswalk, at a rate of one half or more
> (§5); and the **pooled overlap** of positional-strong
> signs across the two compilations exceeds the 95th
> percentile of the 999-shuffle label-permutation null
> (§5).

The statement is deliberately narrower than the claim
as recorded: it names the battery, the arms, and the
thresholds that make "specific" checkable. A verdict on
the amended statement is a verdict on that sentence —
§9's wordings keep the difference visible, and the
parent claim's record (status: strongly supported;
falsification condition: none until the amended freeze
appends §8's text) is not rewritten by any verdict.

## 3. Battery NB-1 — full specification

NB-1 is a new battery, defined here. It is not the
Phase-43 battery, and no element of it is presented as
recovered from the Phase-43 pipeline — that pipeline's
rules were never recorded (`adjudication.md` §7.2), and
the owner's ruling forbids supplying them under its
name. Spec 052's amendment defines the same battery
for its member; the two specifications are identical
in elements NB-1.1–NB-1.5, and each spec freezes on its
own text. Two anchors from the Phase-43 record are
used, both labelled where they are used: the
**partition property** (NB-1.2) the results file
observably has, and the **consistency check** on the
strength band (NB-1.5) against the ten exhibited
TERMINAL_STRONG signs.

### NB-1.1 — Population

The battery runs on a named population of inscriptions.
Each inscription enters as the corpus layer's own
record of it: the layer's sign numbering, and the
layer's own segmentation of the inscription into a
sequence of signs. No re-segmentation, no renumbering,
and no crosswalk is applied inside a run of the
battery. (The crosswalk enters this spec only in §5,
between the arms — never inside either arm's counts.)

### NB-1.2 — Position classes

In a sequence of length n ≥ 2: the first sign is an
**initial** occurrence, the last sign is a **terminal**
occurrence, and every sign between them is a **medial**
occurrence. A sequence of length 2 contributes one
initial and one terminal occurrence and no medial
occurrence. Sequences of length 1 are counted and
reported separately (their number is part of the run
record) and enter no count below. Every counted
occurrence of a sign therefore belongs to exactly one
of the three classes — the partition property the
Phase-43 results file observably has (its three
tables' counts sum exactly to each sign's total).

### NB-1.3 — Counts and rates

For each sign s: N(s) = its total occurrences in
sequences of length ≥ 2; I(s), T(s), M(s) = its
occurrences in the initial, terminal, and medial
classes. By NB-1.2, I(s) + T(s) + M(s) = N(s) exactly.
The class rates are i(s) = I(s)/N(s), t(s) = T(s)/N(s),
m(s) = M(s)/N(s).

### NB-1.4 — Count floor

A sign is **classifiable** in a population iff
N(s) ≥ 20. Signs below the floor are reported with
their counts and marked TOO THIN for that population;
they are members of no strong set, and they are never
silently dropped from the report.

*Basis.* In the Phase-43 results file, the smallest
total count among the ten exhibited TERMINAL_STRONG
signs is 22 occurrences. A floor of 20 therefore
excludes none of the signs the recorded class actually
contains, while bounding every rate's resolution at
1/20 = 0.05. The floor is a stated design constant
checked against the record in this one respect; it is
not a recovered Phase-43 value (the record states no
floor).

### NB-1.5 — Strength bands

For a classifiable sign:

- **TERMINAL_STRONG** iff t(s) ≥ 2/3;
  **TERMINAL_MODERATE** iff 1/2 ≤ t(s) < 2/3.
- **INITIAL_STRONG** iff i(s) ≥ 2/3;
  **INITIAL_MODERATE** iff 1/2 ≤ i(s) < 2/3.
- **MEDIAL_STRONG** iff m(s) ≥ 2/3;
  **MEDIAL_MODERATE** iff 1/2 ≤ m(s) < 2/3.

A sign's **opening-strong** membership in a population
is INITIAL_STRONG; its **closing-strong** membership
is TERMINAL_STRONG.

*Basis.* The ten exhibited Phase-43 TERMINAL_STRONG
signs have terminal rates from 0.683 to 0.892. The
STRONG edge 2/3 ≈ 0.667 lies just below the lowest
rate in that recorded class, so every exhibited member
of the class is TERMINAL_STRONG under NB-1 — a
consistency property this battery was checked against
before being proposed, **not** a derivation of 2/3 and
not a claim about the Phase-43 threshold (never
recorded). The MODERATE edge 1/2 is the plain reading
"in this position more often than not", a design
choice. No exhibited rates exist for the initial
class, so the initial and medial bands carry no
recorded anchor: the same bands apply there by
symmetry of definition, labelled a design choice.

## 4. The two arms and their data

**Arm 1 — the strict corpus.** The corpus layer of
the Mahadevan lineage as the program holds it in its
database (the V3 corpus layer, `adjudication.md`
§7.4). Step 0 identifies the layer, counts it, and
pins it by hash before any quantity is computed; the
draft's fail-closed gate survives in the amendment's
§6 as the STRICT CORPUS NOT PINNABLE closure. Arm 1 is
read under its own compilation's published segmentation
conventions, identified and recorded at step 0 from the
layer's documentation.

**Arm 2 — the Holdat layer.** The program's held
Holdat sign-sequence layer, in its own numbering,
already the subject of Spec 045's work on this
compilation. The Holdat↔Mahadevan crosswalk v1 is
pinned exactly as the draft's §2 pinned it — JSON
SHA-256 `4e7559df…`, CSV SHA-256 `3d0b9ef1…`, 762
mapped pairs, 383 of them conflict pairs (full hashes
in the draft's §2; the freeze re-asserts them against
the files). Arm 2 is read under the Holdat layer's own
segmentation conventions, identified and recorded at
step 0. Arm 2 enters the decision procedure only
through §5's reappearance and overlap measures; its
own strong sets are computed under NB-1 in its own
numbering.

## 5. The decision procedure

### 5.1 Sets

Each arm produces, under NB-1 in its own numbering:
an **opening-strong set** (INITIAL_STRONG signs) and a
**closing-strong set** (TERMINAL_STRONG signs). All
four sets are exhibited in the run record with their
member signs and counts — the property whose absence
in the Phase-43 record made OPEN-054-2 a finding is a
requirement here.

### 5.2 Reappearance (per class)

For each class (opening, closing), the **reappearance
rate** is the share of arm 1's strong set in that class
whose members are also strong in arm 2 in the same
class, through the pinned crosswalk:

> reappearance(class) = |{ s in arm-1 strong(class) :
> crosswalk(s) is in arm-2 strong(class) }| /
> |arm-1 strong(class)|.

Arm-1 strong signs that are unmapped in the crosswalk,
conflict-paired, or below NB-1.4's floor in arm 2 count
as **not reappeared** in this primary measure
(DD-054-5's denominator discipline, §5.4). The
condition of §7.5(2) is per class, per DD-054-1's
per-set reading: **a class reappears iff its rate is
≥ 1/2**.

### 5.3 Pooled overlap and its null

The **pooled overlap** is the count of signs that are
positional-strong (in either class) in arm 1 and whose
crosswalk image is positional-strong (in either class)
in arm 2. Its null is a **label permutation**: holding
fixed arm 1's sets, the crosswalk table, arm 2's
per-class strong-set sizes, and arm 2's pooled
strong-set size, the labels of arm 2's strong-set
membership are permuted uniformly at random over arm
2's classifiable signs, and the pooled overlap is
recomputed. **999 shuffles; seed 44054**, fixed here;
the chance level is the **nearest-rank 95th percentile**
(the 950th smallest) of the 999 null overlap counts.
The implementation records its generator algorithm and
library in the run record, and §6's determinism gate
requires an identical second run.

*Basis.* This answers OPEN-054-5 (the draft's own
unstated null) by construction: the shuffle holds
everything about the two arms' marginals fixed and
breaks only the label correspondence the crosswalk
asserts, so the percentile measures exactly the
question "would this much overlap arise if strong-set
membership had nothing to do with the crosswalk's
pairings?" 999 shuffles give percentile resolution of
0.001; the 95th percentile is the conventional
one-sided 5% level, labelled a convention.

### 5.4 Denominator discipline (DD-054-5, carried)

The primary denominators are arm 1's full exhibited
strong sets. Every arm-1 strong sign that does not
reappear is named in the run record with its reason —
**TOO THIN** (below NB-1.4's floor in arm 2),
**UNMAPPED** (no crosswalk pair), or **CONFLICT**
(conflict-paired) — and counted as not reappeared in
the primary measure. A sensitivity measure that removes
named signs from the denominator is reported with the
same prominence as the primary; the verdict follows the
primary, always.

### 5.5 Precedence (DD-054-2, carried)

The conditions are applied in this order, and the first
that fires decides:

1. **Either arm-1 strong set is empty → NOT SUPPORTED.**
   Arm 1 has signs clearing the floor but none STRONG
   in a class: the pattern is absent in the lineage
   compilation under NB-1, and no cross-compilation
   question arises. (If **no** arm-1 sign clears
   NB-1.4's floor at all, the run instead closes
   **TOO THIN** at step 0 — absence cannot be
   pronounced on an unclassifiable corpus.)
2. **Both classes reappear (≥ 1/2) → the pooled overlap
   decides:** overlap > the §5.3 chance level →
   **SUPPORTED**; overlap ≤ the chance level →
   **NOT SUPPORTED** (the overlap condition fired on
   its own terms).
3. **At least one class reappears < 1/2 →** if the
   pooled overlap ≤ the chance level, **NOT SUPPORTED**
   (the overlap condition fired on its own terms, and
   the shortfall is recorded beside it); else
   **INCONCLUSIVE**, with the per-class rates and the
   overlap counts stated in the outcome record.

No other combination is reachable under this order; no
repair, re-weighting, or second battery is permitted at
run time.

## 6. Step-0 gates and closures under the amendment

All gates run, in order, before any positional quantity
is computed (the draft's F054-C09 discipline,
unchanged). No failure is repaired at run time.

- **Pin checks.** The crosswalk files hash to §4's
  pins, and each arm's layer pins at identification.
  Any mismatch: **INVALID**.
- **STRICT CORPUS NOT PINNABLE.** Arm 1's layer cannot
  be identified and pinned in the database as the
  Mahadevan-lineage strict corpus. (The draft's gate
  0.3 form, retained.)
- **TOO THIN.** Arm 1 has fewer than 30 sequences of
  length ≥ 3, or fewer than 10 classifiable signs.
  *Basis:* the 30-sequence line is Spec 052's amended
  NB-1.9 line, kept identical across the two members
  because both batteries are NB-1; the 10-classifiable
  line is NB-1.9's second line, for the same reason.
- **SECOND ARM NOT RUNNABLE.** The Holdat layer cannot
  be pinned, or the crosswalk pin fails, or arm 2 has
  fewer than 10 classifiable signs.
- **Determinism.** The frozen implementation, run
  twice over the pinned inputs with seed 44054,
  produces identical sets and identical null
  percentiles. Failure: **INVALID**. (This replaces the
  draft's BATTERY NOT REPRODUCED closure: NB-1 is
  defined by this amendment and has no external
  original to reproduce.)

Retired by this amendment: ORIGINAL SETS NOT
EXHIBITABLE as a closure (the amended run produces its
own sets; the fact remains in `adjudication.md` §7.2
and in §9's SUPPORTED limit); BATTERY NOT PINNABLE
(the battery is this amendment); BATTERY NOT
REPRODUCED (above).

## 7. The generator act — §7.5(3), decided and prepared

**The problem, in the record.** §7.3 established by
direct inspection that the claim store's generator
(`glossa-indus/scripts/indus_claims.py`) re-authors the
Yadav manual claims on every regeneration and carries
prior authored fields forward only for a fixed list of
fields — stage and merge-state fields, the lane-2
authored fields, and the status-correction fields.
`falsification_condition` was not on that list, so a
falsifier appended directly to the extracted store
would survive only until the next regeneration.

**The proof, run 2026-10-23** in a scratch copy of the
generator's tree (the repository copy untouched),
driving the generator's own `process_document` for
`yadav_2009_arxiv` against the claim store as pinned in
§7.1 (SHA-256 `90476623…`):

- *Baseline:* regenerating the untouched store changes
  nothing but timestamps (the file's `extraction_date`
  and the two manual claims' `extracted_at`).
- *Failure mode:* with a marker `falsification_condition`
  appended to `yadav_2009_arxiv_manual_002`'s store
  record, regeneration with the **unmodified** generator
  produces a record in which the marker is **absent** —
  the only condition present is `manual_001`'s
  generator-authored one. §7.3's finding, reproduced.
- *Fixed generator:* with the fix below applied, the
  same append **survives regeneration verbatim**;
  diffed against the original store, the only changes
  are the appended field itself and the baseline
  timestamps. `manual_001`'s authored condition is
  intact.

**The fix** (prepared in this amendment's PR as a
separate commit, touching only
`glossa-indus/scripts/indus_claims.py`): the
regeneration carry-over's preserved-field list gains
`"falsification_condition"`, with a dated comment in
the block's own comment style recording the Spec 054
amendment, the owner ruling, and this proof. The fix
changes no claim's content and appends nothing: it
makes the amended freeze's append durable, whichever
home the freeze uses — the store record (now carried)
or the generator's manual entry (natively re-authored).

## 8. The falsifier text (appended at the amended freeze)

At the amended freeze, and not before, the following
is appended to the record of
`yadav_2009_arxiv_manual_002` as its
`falsification_condition`, verbatim:

> This claim, as evaluated under battery NB-1 (the
> Spec 054 amendment, as frozen), is falsified if any
> of the following holds when the frozen battery is
> run on the frozen arm-1 and arm-2 corpora: (1)
> either arm-1 positional-strong set (opening or
> closing) is empty; (2) for either class, fewer than
> half of arm 1's positional-strong signs are also
> positional-strong in arm 2 in the same class,
> through the pinned crosswalk; or (3) the pooled
> cross-arm overlap of positional-strong signs does
> not exceed the 95th percentile of the 999-shuffle
> label-permutation null — the three conditions
> applied under the precedence rule of the Spec 054
> amendment (§5.5).

The append is accompanied on the claim's record by a
dated note stating that the design's original falsifier
was never appended because the 2026-10-21 freeze failed
before any append (adjudication §7.2), and that this
condition belongs to the amended statement of §2. The
freeze registers the claim-record hash **after** the
append (§7.5(4)'s step, unchanged).

## 9. Verdict wordings (rewritten — no RE-EARNED)

- **SUPPORTED.** "Positional structure of the Yadav
  kind — specific text-beginning and text-ending sign
  sets — is present in the strict corpus under battery
  NB-1 and reproduces across compilations: both
  classes reappear in the Holdat layer at one half or
  more, and the pooled overlap exceeds the
  label-shuffle null's 95th percentile. This verdict
  is about the amended statement under NB-1 as frozen
  in the Spec 054 amendment. It does not establish
  that the script encodes language, that any sign has
  a meaning or a reading, or anything about Yadav et
  al. (2010)'s original Phase-43 statement, whose sets
  no surviving record exhibits; the parent claim's
  record, including its strongly-supported status, is
  untouched by this verdict."
- **NOT SUPPORTED.** The outcome record names the
  condition that fired, under §5.5's precedence:
  "The amended statement is not supported under
  battery NB-1 as frozen: [an arm-1 positional-strong
  set is empty / a positional class reappears at less
  than one half, with the pooled overlap at or below
  the label-shuffle null's 95th percentile / both
  classes reappear, but the pooled overlap does not
  exceed the null's 95th percentile]. This verdict
  falsifies the amended statement only. It does not
  falsify Yadav et al. (2010)'s original statement —
  the original battery's sets cannot be exhibited —
  and it does not move the parent claim's recorded
  status."
- **INCONCLUSIVE.** "One positional class reappears
  across compilations at less than one half, while the
  pooled overlap exceeds the label-shuffle null's 95th
  percentile. The two measures point opposite ways on
  the record as frozen; the run records the per-class
  rates and the overlap counts and closes INCONCLUSIVE.
  No repair, re-weighting, or second battery is
  permitted at run time."

The draft's F054-C14 wording (SUPPORTED (RE-EARNED))
is superseded by this section in full.

## 10. Carried settlements

§7.3's Spec 045 reconciliation carries into the
amendment unchanged: Spec 045's "Holdat final-position
concentration" (joint-sign rate > 0.5 on an
object-frequency basis) and this spec's closing measure
("closing-strong under NB-1", a per-sign terminal-rate
band on an inscription-position basis) are different
quantities; any outcome record of this spec names this
spec's measure by its own name and, if it mentions Spec
045's result at all, by Spec 045's name. DD-054-6's
pooled-overlap headline carries: the pooled overlap is
the headline statistic of §5.3, with the per-class
placements (reappearance rates, named non-reappearing
signs) beside it in the outcome record.

## 11. What the owner is asked to decide (the mini-gate)

1. Approve the amended statement (§2) and battery NB-1
   as specified (§3) — elements and constants (floor
   20; bands 2/3 and 1/2) — or amend any of them by
   name.
2. Approve the decision procedure (§5): per-class
   reappearance at ≥ 1/2 with DD-054-5 denominators;
   the pooled-overlap null as constructed (label
   permutation, 999 shuffles, seed 44054, nearest-rank
   95th percentile); DD-054-2's precedence as ordered
   in §5.5.
3. Approve the verdict wordings (§9) and the falsifier
   text (§8) as the exact words the amended freeze
   will append.
4. Note the generator fix (§7) is prepared in this PR
   as its own commit, on the §7.5(3) act the owner
   decided with the design; approving this amendment
   approves its landing with this PR.

On approval, the path is the draft's own: AEE
lifecycle hooks over the recovered register (tasks
L4), the freeze act (L5 as amended — including the §8
append and the post-append claim-hash registration,
then the OSF filing), and a separate execution order.
On decline, this amendment, §8 of the adjudication, and
the generator fix's proof stand as the record; the
generator commit is withdrawn with the draft, and the
spec stays un-frozen.

## 12. What this amendment does not establish

Approving this amendment establishes a checkable
statement and a durable home for its falsifier —
nothing more. It does not establish that the amended
statement is true (that is the run's question); it
does not establish anything about Yadav et al.
(2010)'s original statement, whose sets remain
unexhibitable; and it does not move, or promise to
move, the parent claim's recorded status — the verdict
words of §9 are written so that no outcome of the
amended run can be read as doing so.

---

*AI disclosure: drafted by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
