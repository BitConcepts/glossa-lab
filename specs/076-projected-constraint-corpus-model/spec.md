# Spec 076 — The Projected-Constraint Corpus Model: Demanding What Must Be True of the Missing Signs

**Status: FROZEN at the freeze act of 2026-10-26** (see
`freeze.md` in this directory). This spec carries the
M12 design (method M12 of the advance-to-decipherment
plan; design draft of 2026-10-26, SHA-256 8945399d…)
into the programme's frozen-contract form. The design
text is carried as written except where this spec's
§0 records a freeze-fixed completion — a place the
design expressly left open for the freeze to close
(the shuffle seed, the step-3 coding rules, the
resolution-value operationalisation, the A-KEY
clarification). Every such completion is stated in
§0 and ruled in the adjudication; none moves a bar,
a threshold, a frame, or a closure word of the
design.

**Governing rule (advance plan, iteration addendum,
2026-10-25), which this spec obeys:** no method whose
verdict rests on a score may proceed past drafting
until an instrument exists at its claimed scale and
has passed a wrong-decipherment null of its own at
that scale. This method's verdicts rest on
*deduction*, not scores — but §8 builds the null in
anyway, in the form this machinery can actually
fail: a marginals-preserving scramble must not
reproduce the register's structural findings. Where
this spec uses statistics at all, they are labelled
tendencies and carry no verdict.

## 0. Freeze-fixed completions (ruled at adjudication DD-076-3)

- **FF-1 — Shuffle seed.** The §8 step-2 null runs
  with seed **20261026** (B = 999 shuffles), fixed
  here, before any run.
- **FF-2 — Step-3 coding rules.** The 94 strict
  signs' claimed types are coded from the anchors
  file's `reading` + `basis` texts only, by a coder
  blind to every census row, under rules CR-1…CR-7:
  - CR-1: an explicit positional statement in the
    basis ("only at the end", "never initial",
    "always final", and the like) codes the type it
    states (ONLY-INIT / ONLY-FIN / ONLY-MED /
    ONLY-SOLO / NEVER-INIT / NEVER-FIN / NEVER-MED /
    NEVER-SOLO as stated).
  - CR-2: a functional positional term — terminal
    marker, ending sign, suffix in its terminal
    sense, case suffix — codes ONLY-FIN; opening
    sign / prefix in its initial sense codes
    ONLY-INIT; infix codes ONLY-MED; a sign claimed
    as a complete inscription by itself codes
    ONLY-SOLO. (A-FACE is the warrant: a completion
    may not hold a type-claim and disown its
    distributional content.)
  - CR-3: a basis asserting a negated position
    ("not a beginning sign") codes the corresponding
    NEVER-* type.
  - CR-4: a purely semantic identification (a
    depicted object, a word gloss, a numeral value)
    with no positional or functional-positional
    content codes FREE.
  - CR-5: where several codable assertions appear,
    the strongest single type is coded, in the order
    ONLY-* before NEVER-* before FREE, and the
    coding note records every assertion seen.
  - CR-6: where the basis is ambiguous between a
    positional and a non-positional reading, the
    positional reading is coded and the ambiguity
    recorded (the control errs toward being able to
    fail, never toward passing).
  - CR-7: a sign attested nowhere in the pilot
    frame (5 of the 94 strict signs are
    frame-absent) is coded as its basis states and
    counted in a separate frame-absent line; it
    cannot be excluded by a frame it is absent
    from, and it does not enter the ≤5 count's
    denominator or numerator.
- **FF-3 — Resolution-value operationalisation**
  (§6.3). RV(x) = log₂|poss(x)| + Σ over bigram
  neighbours y of (c(x,y)/C(x)) · log₂|poss(y)|,
  where N(x) is the set of signs sharing an attested
  ordered bigram with x in either direction,
  c(x,y) the number of attested bigram tokens
  joining x and y, and C(x) the total bigram tokens
  involving x. For a sign with no bigram tokens
  (solo-only signs), RV(x) = log₂|poss(x)|. This is
  the frozen computation the design's §6.3 calls
  for; it is an ordering device only.
- **FF-4 — A-KEY clarification.** The 13 duplicated
  Mahadevan ids of Spec 073's keying-surface
  accounting (M002, M050, M064, M076, M099, M103,
  M161, M167, M168, M199, M216, M264, M409) are ids
  claimed by two *Parpola-keyed registry rows* each
  — a collision on the cross-scheme join surface.
  The pilot frame performs no join through
  `mahadevan_ids`: its sign identity is the frame's
  own Mahadevan numbering (§4 S6, §5.4). A-KEY
  therefore excludes no pilot-frame row; the
  register flags every entry for an attested member
  of the 13 with a join-ambiguity note, and any
  future cross-frame use of those entries must
  resolve the collision on the record first, per
  Spec 073's accounting.
- **FF-5 — Pilot execution order.** The pilot (§8)
  executes once, after this freeze is merged, as a
  single run of the frozen derivation + null +
  control, recorded in `pilot-record.md` in this
  directory and in the programme goal record. No
  parameter of §8 may be altered after the freeze
  for any reason; a premise failure is a
  halt-and-report, recorded with the design's own
  closure words.

## 1. Purpose

Treat the attested corpus as a **constraint
system**: the surviving inscriptions are the
projection the language casts into durable objects,
and everything that projection preserves — counts,
positions, pairings, repetitions — constrains what
the language can have been. A **decipherment**, or
any single sign assignment, is a **completion** of
that system: a way of filling in values for the
signs that leaves every preserved constraint
standing. Most programme effort asks whether a
proposed completion *scores well*. This method asks
the prior question: **what does the constraint
system itself demand of any completion at all — in
particular, of the parts we do not have?**

For each unknown, the method derives the conditions
every valid completion must satisfy:

- **bounded possibility sets** — the value-types
  still open to a sign after the data has excluded
  the rest;
- **forced exclusions** — value-types no completion
  may assign to that sign, because the attested
  data contradicts them;
- **forced co-variations** — ways the unknowns'
  freedoms are coupled, so their joint possibility
  set is smaller than the product of the individual
  sets.

Two uses follow. First, defence: a proposed reading
that violates a derived necessity is excluded
*deductively* — no scorer, no percentile, no taste.
Second, aim: where resolving one unknown would
collapse the most remaining freedom, that is where
the next unit of programme effort (a witness check,
a prediction, an identification attempt) buys the
most. The method reads nothing. It narrows the
space in which reading is attempted, and it prices
the narrowing.

## 2. The unknowns — six categories, counted from the records

"The missing signs" is not one set. The design
keeps the categories separate, because the
constraint system speaks to each differently.
Counts are from the records named; frame-relative
counts say which frame.

- **U1 — No published identity (Registry v2
  schedule).** Exactly **one** sign: ICIT token
  **999** (`specs/073-keying-surface-repair/registry-v2/no-published-identity.json`
  carries a single entry). In Spec 075's population
  it has 2 rows / 2 occurrences. M7's two-condition
  attack is its named treatment; this method's
  register must reproduce whatever bounds that
  attack assumes, as register entries (§6). Token
  999 does not occur in the pilot frame (its
  numbering is the ICIT/Wells line, not the
  frame's Mahadevan numbering); the pilot register
  records that absence rather than deriving
  anything about it.
- **U2 — No anchor of any kind.** Signs attested in
  a corpus frame with no entry in the anchors file
  (287 entries, of which 94 strict, 44 pending, 149
  in weaker or superseded standing). In the §7
  pilot frame: **122 signs, 1,825 of 11,507
  tokens**. These are the register's main subject:
  attested, distributed, and entirely unread.
- **U3 — The pending readings.** The **44** anchors
  standing `pending_non_sa_validation` (42 attested
  in the §7 frame). They carry claimed values whose
  *types* the register can test deductively —
  without scoring anything, and without touching
  M4's gate (§10).
- **U4 — Rare and hapax signs.** In the §7 frame:
  **108 signs occur exactly once** (42 of them U2),
  155 occur at most twice, 207 at most five times.
  Their rows are thin; the register's discipline
  about thin rows (§3, §7.5) is written for them.
- **U5 — Signs absent from a frame.** Mahadevan's
  list names 417 signs; the §7 frame attests 393.
  The **24 absent** signs (039, 044, 046, 088, 144,
  154, 156, 179, 231, 235, 266, 275, 279, 282, 312,
  315, 324, 346, 362, 363, 374, 383, 405, 408)
  include 5 strict signs (039, 044, 046, 362, 374)
  and 2 pending (235, 383) — absence is
  frame-relative, never a property of the sign. In
  the primary population (Spec 074/075 frame), the
  parallel fact is 557 distinct signs of which 550
  occur in sequences of length ≥ 2 — **7 signs occur
  only as complete one-sign inscriptions**.
- **U6 — Unmapped witness signs.** Wells 1998's 587
  table entries key a numbering that does not join
  Registry v2 (its `wells_ids` key Wells 2015);
  only Figure 3.6's **55 pairings over 17 M77
  targets** cross over. M77's postscript signs
  418/419 sit outside its 417-sign list. §4 states
  what an unmapped witness can and cannot
  constrain: almost everything it knows is about
  itself until a pairing joins it.

## 3. The honesty architecture — what "must" is allowed to mean

The whole design stands or falls here. "Must" is
the easiest word in decipherment to abuse, so the
spec fixes its meaning before deriving anything.

### 3.1 Necessities are conditional, and the conditions are claims

A **necessity** is a statement true in every
completion consistent with (attested data + a
stated assumption set). Every necessity the
register ever files carries four things:

1. **Its assumption set**, by name (§3.2). Each
   assumption is itself filed as a claim in the
   programme's claim machinery, with its own
   falsifier — an assumption is not a footnote, it
   is a commitment that can die.
2. **Its derivation route** — the exact computation,
   over the exact pinned inputs, that produces it.
   A necessity that cannot be re-derived from its
   pins is withdrawn, not defended.
3. **Its falsifier** — the observation that would
   kill it. For census-tier necessities the
   falsifier is concrete: a change in the
   underlying census fact (a re-keying, an admitted
   compilation, a superseded pin) that alters the
   numbers the necessity was derived from. The
   necessity names its frame pin so the falsifier
   can be checked mechanically.
4. **Its tier** (§3.3). Necessities from different
   tiers never mix in one statement.

### 3.2 The standing assumption set

- **A-FRAME.** The pinned frame construction (named
  file, named pin, named record filter and token
  rules) *is* the attested corpus for this register.
  A necessity binds completions *of that frame's
  language-as-attested*; it says nothing about
  inscriptions the frame excludes, and it is
  re-derived, not carried over, when the frame
  changes.
- **A-DIR.** The stored sequence order is the
  reading order for positional labels: initial =
  first stored token, final = last stored token, a
  one-token sequence's token is SOLO. The M1 pilot
  showed direction conventions move
  cross-compilation comparisons by whole signs;
  within one frame the convention is fixed by this
  assumption and every positional statement
  inherits it.
- **A-FACE.** A completion's value-type claims are
  taken at face value. If a reading calls a sign a
  suffix, it claims final-position behaviour for
  that sign; if it calls a sign a prefix, it claims
  initial behaviour. A completion may not hold a
  type-claim and disown its distributional content
  when the census contradicts it.
- **A-KEY.** Registry v2 is the identity relation
  between frames and witnesses. Signs whose registry
  rows collide — the **13 duplicated Mahadevan ids**
  in the Spec 073 keying-surface accounting — are
  **AMBIGUOUS** for derivation purposes: their rows
  are excluded from the deductive layer until the
  collision is resolved on the record. (This borrows
  the trigger census's binding discipline
  deliberately: an ambiguous row is never silently
  scored in the convenient direction.) FF-4 (§0)
  states how this rule applies to the pilot frame:
  the collision lives on the cross-scheme join
  surface, the pilot frame performs no such join,
  and no pilot-frame row is excluded; attested
  members of the 13 carry a join-ambiguity flag in
  the register.

### 3.3 Three tiers, never blended

- **Tier C — census necessities.** Consequences of a
  pinned frame's exact integer accounting plus
  A-FRAME / A-DIR / A-FACE / A-KEY. These are
  deductions: given the assumptions, the conclusion
  cannot fail while the census stands. Most Tier-C
  necessities are *exclusions by exhibition*: a
  completion whose own type-claim for a sign is
  contradicted by that sign's attested occurrences
  is inconsistent with the corpus it claims to
  read — no probability enters.
- **Tier S — structural necessities.** Consequences
  that need an extra assumption beyond §3.2 — each
  such assumption filed as its own claim, with its
  own falsifier, and each Tier-S necessity
  recording which S-claims it depends on, so that
  if an S-claim falls, its dependent necessities
  fall automatically and visibly. Named candidates:
  **S-CLOSED** (the surviving corpus is closed for
  the context a claim needs — no further inscription
  types will appear); **S-REP** (a frame's positional
  behaviour represents the wider corpus's);
  **S-COPY** (duplicate inscriptions are faithful
  copies, so reading-equality binds at the level of
  the text, not just the reading function). Tier S
  is where most interesting necessities will want
  to live, and the tier exists to make them pay for
  their assumptions in public.
- **Tier T — tendencies.** Everything statistical:
  rates, intervals, cross-compilation transfers,
  model fits. Tendencies may be recorded (in a
  separate annex, never in the necessity register),
  may guide effort, and **may never be upgraded to
  necessities at any sample size**. The M1 pilot is
  the standing warning: sign M267's final-position
  rate is 0.147 in Holdat and 0.740 in Yajnadevam —
  a tendency measured honestly in one compilation
  reversed in another. A rate is a property of a
  sample; a necessity is a property of every
  completion. The register's type discipline (§3.4)
  exists to keep the two apart mechanically, not by
  vigilance.

### 3.4 The type vocabulary — how a census row becomes exclusions

Possibility sets are stated over a small, fixed
vocabulary of **positional value-types** — claims a
completion can make about how a sign's value behaves
in texts:

| Type | The claim it makes |
|---|---|
| ONLY-INIT | the sign occurs only in initial position |
| ONLY-FIN | the sign occurs only in final position |
| ONLY-MED | the sign occurs only in medial position |
| ONLY-SOLO | the sign occurs only as a complete one-sign inscription |
| NEVER-INIT / NEVER-FIN / NEVER-MED / NEVER-SOLO | the sign never occurs in that position |
| FREE | the completion makes no positional claim for the sign |

Against a sign's census row (init *i*, medial *m*,
final *f*, solo *s*, total *t = i+m+f+s*),
contradiction is mechanical: ONLY-INIT is
contradicted iff *m+f+s > 0*; ONLY-FIN iff
*i+m+s > 0*; ONLY-MED iff *i+f+s > 0*; ONLY-SOLO iff
*t > s*; NEVER-INIT iff *i > 0*; NEVER-FIN iff
*f > 0*; NEVER-MED iff *m > 0*; NEVER-SOLO iff
*s > 0*; FREE is never contradicted positionally. A
sign's **possibility set** is the set of types *not*
contradicted. Two honesty properties are built in
and stated now, not discovered later:

- **The register never identifies.** It records set
  membership ("ONLY-FIN ∈ poss(x)"), never set
  identity ("x is final-only"). A surviving type is
  a type the data has not excluded; the distance
  between those statements is exactly the distance
  between a tendency and a necessity, and §7.5 works
  the boundary on a real sign.
- **The vocabulary's granularity is coarse, by
  arithmetic.** A sign's possibility-set size is
  determined by how many of its four slot counts are
  zero: 0 zeros → 1 surviving type (FREE alone);
  1 zero → 2; 2 zeros → 3; 3 zeros → 5. Sizes 4 and
  6–8 cannot occur. Finer narrowing than this
  vocabulary allows must come from pair-level
  constraints (§4) or a richer vocabulary — and a
  richer vocabulary is a new assumption, filed as a
  claim, not a silent refinement.

The vocabulary itself is an assumption of the
design (part of A-FACE's machinery): it is filed as
a claim of this spec (F076-C03, §11), and a
completion whose type-claims fall outside the
vocabulary is handled by extending the vocabulary
on the record, never by forcing the claim into the
nearest type.

## 4. Constraint sources — named, audited, and assigned a layer

Each source the register may draw on, with what it
can legitimately constrain, its known defect, and
the layer it enters. A source enters the deductive
layer only for the statements its defect does not
touch.

| # | Source | What it can legitimately constrain | Known defect | Layer |
|---|---|---|---|---|
| S1 | **Positional behaviour** (initial / medial / final / solo counts per sign, per pinned frame) | Type exclusions by exhibition (§3.4); slot-accounting identities and every bound derived from them (§7.3) | Direction-convention dependence (A-DIR); compilations diverge (M1 pilot: 14 of 20 top signs' final rates outside the other compilation's 95% intervals) | **Deductive (Tier C) within one named frame only.** Any cross-frame positional statement is Tier T by construction |
| S2 | **Co-occurrence and exclusion within inscriptions** (ordered bigram census) | Attested-pair facts; pair-level possibility narrowing (a sign's attested successors/predecessors bound the contexts its type must tolerate); locked-pair co-variation where it exists | Sparsity: in the §7 frame, 2,558 distinct ordered pairs are attested of 154,449 possible (1.7%). An *unattested* pair is usually unattested because the corpus is small, not because it is excluded — absence of a pair is a census fact, not an exclusion | Attested pairs: **Tier C**. Pair *exclusions* (this pair cannot occur): **Tier S only**, under S-CLOSED, or Tier T |
| S3 | **Inscription-length structure** (the frame's length profile; solo count) | The accounting identities themselves; the solo-only sign set (signs with no attested neighbour at all — §7.4) | Length is partly an artefact of object type and fragmentation, not only of language | Accounting: **Tier C**. Any linguistic reading of the profile: **Tier T** |
| S4 | **Sequence repetition across inscriptions** (duplicate and near-duplicate texts) | Equality: a completion is a function — the same sign sequence receives the same reading everywhere it occurs; one-substitution neighbours (M6's census) bound how readings may vary across a substitution | Carvers copy with errors; equality binds the completion, not the carvers | Reading-function equality: **Tier C**. Claims about the *texts'* identity: **Tier S** under S-COPY |
| S5 | **Depiction pairings** (Asset A v2; the Spec 075 population and its per-kind results) | In distinct-depiction units, per-depiction positional facts of the same standing as S1 | The red team's C-1/F-11 qualification travels with this source permanently: kinds pool many-to-one through Parpola rows (46.1% of the human kind's occurrences sit on shared depictions), and 075's TOO THIN floor was stated in signs against a depictions quantity (object_goods: 24 signs = 19 distinct depictions) | **Tier C only in distinct-depiction units with the split sensitivity run** (the C-1 computation, executed 2026-10-26, is the gate this source's deductive use had to pass; its result — the human verdict pooling-sensitive — is carried wherever this source is cited); kind-level claims: **Tier T** |
| S6 | **Witness signary structure** (M77 dataset v3: 417 signs, variant-dagger flags, §11.5 classes; Wells 1998 dataset: 587 entries, classes, his printed totals) | Sign *existence* and enumeration (M77 keys the Mahadevan numbering itself, so its list is the frame's own universe, stated as data); variant structure (a daggered sign has graphic variants — a completion that assigns it a type incompatible with allography must say why); the witnesses' internal accounting as bracket checks | M77's classes are *shape* classes — Mahadevan's own text disclaims identifications for them, so class membership is REPORTED structure, never an identification. Wells is **unmapped**: outside Fig. 3.6's 55 pairings, a Wells number constrains no Registry sign, and Wells' printed totals are internally inconsistent (7,121 in prose vs 7,131 by site sums) | M77 enumeration/daggers: **Tier C as census of the witness**. M77/Wells class semantics: **reported, never adopted** (the census instrument's reported-speech rule). Wells positional/frequency structure: constrains **nothing** in the register until a pairing joins it — then only through the pairing |

**What an unmapped witness can and cannot do,
stated once for the whole design:** it can constrain
the *shape of the problem* — how many signs a
complete signary must have room for, which of its
own signs its own totals force to exist — and it can
serve as the target of a join (M7's work). It cannot
exclude a value-type for any programme sign, bound
any programme sign's occurrences, or break a tie in
the register, because every such act needs the
identity relation the witness does not supply. A
design that lets an unmapped witness constrain a
mapped sign has smuggled in a mapping it has not
built.

## 5. Frames and keying — what this method trusts, and why

The M1 pilot's lesson is load-bearing here:
positional behaviour that looks like a law inside
one compilation (M267 final at 0.147) is a different
number in another (0.740), and the divergence
survived the Spec 073 keying repair — the repaired
key was not the whole story. A method whose product
is *necessities* cannot afford frame-blindness, so:

1. **The deductive layer runs within one named,
   pinned frame at a time.** Every register entry
   names its frame. Necessities are never merged,
   averaged, or intersected across frames at Tier C;
   a statement that holds in two frames is two
   register entries, one per frame, each with its
   own falsifier.
2. **The population frame for programme-level
   claims is the Shakti documented-lineage primary
   population** (3,045 inscriptions / 557 signs /
   11,805 tokens; frozen through Specs 074–075;
   deposit-pinned) — because it is the programme's
   frozen primary frame, the one its executed
   verdicts already stand on. The register's
   production run (if a freeze ever commissions one)
   is derived there first.
3. **The pilot frame (§8) is the Spec 033 corpus
   export** (`glossa-corpus/indus/exports/indus_research.jsonl`,
   SHA-256 `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`)
   — because it is committed, hash-pinned, and its
   census has now been reproduced exactly by two
   independent routes (Spec 033's pipeline census and
   the design draft's recomputation, §7.1). A pilot
   about whether derivation is honest belongs on the
   frame whose numbers are already beyond dispute.
4. **Keying is Registry v2 only** (SHA-256
   `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`,
   1,013 rows), with A-KEY's ambiguity rule for its
   13 duplicated Mahadevan ids, as clarified at FF-4.
   Holdat may host its own register (its frame is
   pinned: SHA-256 `62d14d2b…`, 1,670 inscriptions /
   7,002 tokens / 390 signs), whose necessities bind
   Holdat alone. Yajnadevam / Field-Cady are one
   sequence population under two provenances (M1
   pilot §3) and count as one frame wherever they
   appear.

## 6. Outputs — the register, the possibility sets, the ranking

### 6.1 The necessity register

The method's product is a **register**: a list of
entries, each filed through the programme's claim
machinery as a claim in its own right, carrying —

- the **statement** (an exclusion: "type τ ∉
  poss(x)"; a bound: "fin(x) ≤ 178 in frame F"; a
  co-variation: "Σ fin over U2 = 178 in frame F"; a
  set: "poss(x) = {…}");
- **tier** (C, or S with its S-claim dependencies
  named);
- **assumption set** (from §3.2 plus any S-claims,
  each by claim id);
- **derivation route** (the census computation and
  the pins it ran on);
- **falsifier** (the observation that kills the
  entry);
- **frame** (name + pin), and the entry's **status**
  under the programme's lifecycle (created → checked
  → explained → accepted → digested, like every
  other claim).

Tendencies, if recorded at all, live in a separate
annex with their own labels; no annex entry may be
cited as a register entry, and the register's format
makes the confusion mechanically difficult (annex
entries carry no falsifier field, because a tendency
is not falsified — it is superseded).

The pilot register (§8) is filed as
`pilot-register.json` + `pilot-register.md` in this
directory, in exactly this form, for the pilot frame
only.

### 6.2 Possibility sets

Per unknown sign, per frame: the surviving type set
under §3.4, extended at pair level by S2's
attested-pair facts where the freeze's rules allow
(e.g., a sign attested only before one successor
class has its pair-level set recorded as data, not
as a type). The set is printed whole, never
summarised to its "most likely" member — the
register has no most likely member; likelihood is
the annex's language.

### 6.3 The target ranking — where resolution buys the most

For each unknown x, its **resolution value** is
computed by the frozen rule FF-3 (§0) on the
register's coupling graph (nodes: unknown signs;
edges: attested bigram adjacency in the frame,
shared identity constraints such as the §7.3
residual simplex, and shared S-claim dependencies).
The ranking is an *output*, re-derived whenever the
register changes; it asserts where the next unit of
effort buys the most narrowing, and nothing else.
Its feeds are specified in §10: to M4 as *ordering
only* (which pending readings to write predictions
for first, if M4's gate ever lifts — the ranking
does not score, promote, or demote any reading), and
to M7 as *bounds only* (the register's entries for
token 999 are the conditions M7's two-condition
attack must respect; the attack itself remains
M7's).

## 7. Worked miniature example — real counts, recomputed for the design

Every number below was recomputed during drafting
from the pinned files, by the construction stated.
Nothing is quoted from memory; the frame's census is
reproduced against Spec 033's own pipeline census as
a check, and the slot identities are verified two
ways. (At this freeze the drafting worker
re-derived the same census a third time, from the
pins as fetched from main, and every figure below
reproduced exactly; the C2 record carries the
independent recomputation.)

### 7.1 The frame, and its reproduction

Frame = the `indusscript-m77` records of the Spec
033 corpus export (`glossa-corpus/indus/exports/indus_research.jsonl`,
SHA-256 `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`):
**2,906 records**. Token construction: the records'
stored grapheme ids, dropping **680** placeholder
tokens (`000`) and **452** marked tokens
(`*`-prefixed) → **11,507 tokens** — exactly Spec
033's recorded corpus census. Of those, tokens whose
id is one of the 94 strict signs: **5,883** — exactly
its recorded strict-token census. The anchors file
(`backend/reports/INDUS_FINAL_ANCHORS.json`,
SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`,
taken from repo main) reproduces its own headline
counts under the same reading: 287 entries, **94**
`strict_sa_independent`, **44**
`pending_non_sa_validation`. Non-empty sequences
after token-dropping: **2,880** (26 records consist
only of dropped tokens). Length profile: 1×225,
2×531, 3×563, 4×521, 5×444, 6×249, 7×189, 8×82,
9×32, 10×28, 11×11, 12×2, 13×1, 14×2 — which sums to
2,880 sequences and, weighted by length, to 11,507
tokens. Distinct signs attested: **393**, all within
Mahadevan 001–417.

### 7.2 The slot identities (Tier C bookkeeping)

Under the §3.4 convention (first stored token
initial, last final, one-token sequence's token
solo): **Σ init = 2,655; Σ fin = 2,655; Σ solo =
225; Σ med = 5,972** — and 2,655 + 2,655 + 5,972 +
225 = 11,507, while 2,655 = 2,880 − 225 (every
sequence of length ≥ 2 contributes exactly one
initial and one final slot). These identities hold
in *every* completion and *every* scramble of this
frame — they are bookkeeping, not findings, and
§8's null is designed around that fact rather than
pretending otherwise.

### 7.3 Necessity 1 — the finals residual, and the co-variation it forces

Partition the 2,655 final slots by the final token's
standing (anchors file, same pins):

| Standing | Signs attested | Final slots held |
|---|---|---|
| Strict (94) | 89 | 1,707 |
| Pending (44) | 42 | 250 |
| Anchored, other standing | 140 | 520 |
| **No anchor (U2)** | **122** | **178** |
| Total | 393 | **2,655** |

**The necessity:** in this frame, the 122 unread
signs *jointly* hold exactly **178** final slots.
Therefore no completion — and no proposal evaluated
against this frame — may require any U2 sign, or all
of them together, to account for more than 178 final
occurrences. The scale contrast is attested data,
not rhetoric: the strict sign M342 alone holds
**876** finals (row: t 1,274 = init 26 + med 349 +
fin 876 + solo 23). A completion claiming some
unread sign is "the corpus's standard ending sign"
at anything approaching that scale is not
improbable; it is arithmetically excluded, and the
register files the exclusion without a single
statistic. *Assumption set:* A-FRAME + A-DIR +
A-KEY. *Derivation:* the §7.1 census and this
partition. *Falsifier:* a re-derived census from the
named pins in which the partition does not sum to
2,655, or a frame change (new pin) — in which case
the entry is re-derived under the new pin, not
patched.

**The co-variation:** the U2 signs' final counts
form a vector of 122 non-negative integers summing
to exactly 178. Their joint possibility set is
therefore that simplex — strictly smaller than the
product of the individual bounds [0, min(t(x), 178)].
Concretely: were one U2 sign shown (by a new frame
or a join) to hold 100 finals, the other 121 signs'
combined allowance would fall to 78 and *every one
of their individual bounds would tighten*, though
none of their own rows changed. That is what "the
unknowns' freedoms are coupled" means, in
arithmetic. Two census facts sharpen the picture:
the three largest U2 final counts (signs 098: 13,
373: 13, 086: 12) already consume 38 of the 178, and
**70 of the 122** U2 signs hold **0** finals in this
frame.

### 7.4 Necessity 2 — exclusion by exhibition (sign 358), and the solo-only signs

Sign **358** (U2 — no anchor, no reading, no
published identity beyond its list membership) has
row **t = 31: init 0, med 30, fin 1, solo 0**.
Applying §3.4's rules one type at a time: ONLY-INIT
is contradicted (med+fin = 31 > 0); ONLY-FIN
(med = 30 > 0); ONLY-MED (fin = 1 > 0); ONLY-SOLO
(t > solo); NEVER-FIN (fin = 1 > 0); NEVER-MED
(med = 30 > 0). Six of the nine types are excluded
*by attested occurrences*, leaving **poss(358) =
{NEVER-INIT, NEVER-SOLO, FREE}**: whatever 358 is,
in every completion consistent with this frame its
type tolerates medial occurrence (30 attestations)
and final occurrence (1), and claims neither an
initial-only, final-only, medial-only, nor solo-only
nature. That is a demand the constraint system makes
of a sign nobody has ever read — derived, not
scored. *Falsifier:* an admitted frame exhibiting
an initial occurrence of 358 does not break the
filed entry (which names this frame's pin); it
changes what the *next* frame's register derives —
the entry's frame-relativity is its honesty, stated
on its face.

The **solo-only signs** are the same derivation at
its starkest: 13 signs are attested in this frame
*only* as complete one-sign inscriptions (031 twice,
378 twice, and 165, 220, 317, 377, 085, 118, 115,
411, 232, 269, 392 once each). Sign **031** — a
*pending* reading, U3 — has row t = 2, solo = 2, and
poss(031) = {ONLY-SOLO, NEVER-INIT, NEVER-FIN,
NEVER-MED, FREE}: every type that requires a
neighbour is excluded for it in this frame. §10
states what the register does and does not do with
that fact about a pending reading.

### 7.5 The tendency that must NOT be upgraded (sign 276)

Sign **276** (U2) occurs **once** in the frame, in
final position. Its final-position *rate* is
therefore 1/1 = **100%** — and ONLY-FIN duly survives
in its possibility set: poss(276) = {ONLY-FIN,
NEVER-INIT, NEVER-MED, NEVER-SOLO, FREE}, five of
nine types. The register files exactly that set,
plus the census facts (t = 1, fin = 1). It does
**not** file "276 is an ending sign," because that
statement claims the set is a singleton — an
identity — on the evidence of one token. If a future
frame gives 276 a single medial occurrence, ONLY-FIN
leaves its set on re-derivation and *no filed
necessity breaks*: nothing was ever claimed that the
new token contradicts. The asymmetry is the doctrine,
and this pair of signs teaches it in one frame:
**attested occurrences exclude (358's six dead types
rest on 31 tokens); unattested positions merely fail
to exclude (276's surviving ONLY-FIN rests on an
absence, and absence at n = 1 — or, as M267's
cross-compilation reversal warns, at any n — is not
a law).** A register that printed "276: final-only"
would be a tendency wearing a necessity's clothes;
§3.4's set-membership discipline exists so that it
cannot.

### 7.6 The empty set is also a finding

The 24 M77-listed signs absent from this frame (§2,
U5) have no positional row here at all. The register
files **empty constraint sets** for them — the method
stating, in its own format, that within this frame
it is *silent* about them, and that the correct
response to that silence is a witness or another
frame (M7's territory), not more derivation from
data that does not mention them. The same holds for
Wells' unmapped numbers outside Fig. 3.6 (§4, S6):
no pairing, no constraint, no exceptions.

## 8. Pilot design — with the null built in, and the bars stated now

The pilot's question is narrow and prior to any
production register: **is the derivation honest, and
does the frame's constraint structure exceed what
its own marginals would produce by chance?** The M2
pilot is the standing warning in both directions:
its Part 1 could not be run as written (the input
its design assumed did not exist), and its Part 2
machinery, run exactly, did not discriminate (78.33rd
percentile of its own enumeration). This pilot is
built to be able to die at either door.

**Step 0 — reproduction gate.** Re-derive the §7.1
census from the named pins: 2,906 records → 11,507
tokens; 5,883 strict tokens; the §7.2 identities
exact; the §7.3 partition summing to 2,655. Any
mismatch closes the pilot **CANNOT BE RUN AS
WRITTEN** — the M2 closure word, reused deliberately:
a derivation that cannot reproduce its own frame has
no register to test.

**Step 1 — derivation.** Derive the frame's Tier-C
register (possibility sets for all attested signs;
the residual identity; the solo-only set). Pre-named
headline numbers the derivation must reproduce, from
§7: **677** (sign, type) exclusions over the 122 U2
signs (possibility-set size distribution: size 1 →
14 signs, 2 → 29, 3 → 23, 5 → 56 — sizes 4 and 6–8
absent, per §3.4's arithmetic); U2 finals residual
**178**; solo-only set size **13**.

**Step 2 — the wrong-completion control.** First, a
trap stated in advance so it cannot be "discovered"
after the fact: **label permutation is not a valid
null for this machinery.** The accounting identities
are invariant under relabelling — a scrambled corpus
yields the same identities *by construction*, so a
permutation test on them cannot fail and therefore
tests nothing. The valid null operates one level
down: **shuffle the frame's tokens within sequences,
preserving every sign's total token count and the
exact length profile** (hence preserving every slot
total and every Tier-C identity — by construction,
and that is precisely the point: the test family is
what the identities do *not* fix). B = **999**
shuffles; seed **20261026** (FF-1). Per shuffle,
re-derive the two pre-named statistics:

- **(i) the U2 finals residual** — real value **178**.
  The null's expectation sits near the U2 token share
  of the final slots (1,825 / 11,507 × 2,655 ≈ 421):
  the real frame's unread signs are final-poor far
  beyond their token share. **Bar: the real residual
  must fall below the null's 5th percentile.**
- **(ii) the solo-only sign count** — real value
  **13**. Under the shuffle, solo status is an
  accident of the solo slots' share (≈ 225 / 11,507
  ≈ 2% per single-token sign). **Bar: the real count
  must exceed the null's 95th percentile.**

If either statistic falls inside its null range, the
pilot closes: **THE FRAME'S CONSTRAINT STRUCTURE IS
NOT DISTINGUISHABLE FROM A MARGINALS-PRESERVING
SCRAMBLE IN THE TESTED FAMILY** — the register
entries in that family are then machinery artefacts
(they arise from the marginals alone) and may not be
filed as claims. Where a bounded subsystem's
arrangement count (multinomial, preserving the
subsystem's own marginals) is ≤ ~10⁷, the null is
computed by **exact enumeration** instead of
sampling; at frame scale the arrangement count is
astronomically beyond that, so the frame-scale null
is the sampled permutation null under the governing
rule's standing alternative, with the percentile bars
above committed here, before any run.

Implementation note (frozen): "shuffle the frame's
tokens within sequences, preserving every sign's
total token count and the exact length profile" is
implemented as a uniform random redistribution of
the frame's token multiset into the frame's sequence
slots (sequence lengths fixed; each sign's total
count fixed) — the standard marginals-preserving
shuffle of a contingency structure, equivalent to
shuffling the pooled token list and re-dealing it
into sequences of the frozen lengths. Under this
shuffle a one-token sequence's token is a uniform
draw from the multiset without replacement across
slots, so statistic (ii) is non-degenerate. Any
implementation that instead permutes tokens only
within each sequence leaves every sequence's multiset
— and therefore both statistics' inputs at sequence
level — unchanged in composition per sequence and is
NOT this null.

**Step 3 — positive control (calibration against
the knowns).** Code the 94 strict signs' claimed
types from their anchors-file basis texts, under the
coding rules FF-2 (§0), the coder blind to each
sign's census row; run the same derivation against
the strict rows. **Bar, stated now: if the machinery
excludes more than 5 of the 94 claimed types, the
pilot closes ASSUMPTION SET DOES NOT HOLD** — and
the presumption is that the machinery (vocabulary,
coding rules, or A-FACE) is wrong, not that the
strict core is. (FF-2 CR-7 governs the 5 frame-absent
strict signs: coded, reported on their own line, and
outside the ≤5 count.) A result inside the bar is
reported as a count, never rounded to a pass
adjective.

**Verdict bands.** PILOT PASSES (step 0 exact; both
step-2 statistics beyond their bars; step 3 inside
its bar) → licenses drafting a freeze for the
production register on the primary-population frame.
PILOT FAILS → the named closure word, appended to
this spec with the pilot record, exploratory-labelled,
in the advance plan's iteration loop (cap: three
iterations, then the move re-ranks on evidence or
closes PARKED). The pilot files no production claim
either way; F076-C02 (§11) is filed only on a pass.

## 9. Feasibility verdict — what scale of exact work is real, and what is not

**Real:** the entire deductive layer at frame scale.
The census and register derivation is linear in
tokens plus a signs² pair matrix — 11,507 token
visits and 154,449 cells (2,558 attested) on the
pilot frame; the drafting computation ran in
seconds, and Spec 033's pipeline census, reproduced
exactly here by an independent route, is the
standing proof that this scale of exact integer work
is routine in this programme. Exactness is real at
**constraint order ≤ 2 within a pinned frame**
(per-sign rows; ordered pairs), and at any order on
**named bounded subsystems** small enough to
enumerate (≤ ~10⁷ arrangements, the §8 boundary).

**Not real, and never claimed:** enumerating
completions. A binary type choice over the frame's
393 signs already gives 2³⁹³ ≈ 10¹¹⁸ candidates; the
9-type vocabulary over just the 122 U2 signs gives
9¹²² ≈ 10¹¹⁶ possibility-vectors before pair
constraints. Any method that "checks all completions"
is misdescribing itself. This method does not search:
each identity, each census row, and each attested
pair is a constraint checked independently,
possibility sets are the *closure* of those
independent checks, and the residual simplex (§7.3)
is the joint statement those checks jointly force.
Constraint *propagation* is exact and cheap;
completion *search* is neither needed nor possible.

**The boundary, with numbers:** order 3 is where
exactness dies of sparsity, not of compute — 393³ ≈
6.1×10⁷ possible ordered triples against at most
11,507 attested triple tokens, so nearly every
order-3 statement would be a closure assumption
wearing a census's clothes; order-3 work is Tier S
territory, admitted only under a filed S-claim.
**Cross-frame exactness: none** (M1 — compilations
diverge structurally, and the register's
frame-relativity is the designed response, not a
deficiency to be averaged away). **Witness
exactness:** only through built joins (M77 by
number, since it *is* the frame's numbering; Wells
only through Fig. 3.6's 55 pairings).
**Depiction-source deductive use:** gated on the
programme's C-1 split sensitivity (§4, S5) — that
computation has now run (2026-10-26, exploratory)
and found the human kind's verdict pooling-sensitive;
until a freeze rules on its standing, Asset A v2
feeds the tendency annex, not the register.

## 10. Relationship map — what this composes with, and what it must not touch

- **M7 (triangulation / external witnessing).** M7
  asks whether the signary is witnessed from outside
  — existence, by number, under its match rules and
  ancestry discipline. M12 asks what the corpus itself
  forces about the unwitnessed and unread —
  behaviour, by derivation. M12 consumes M7's gap
  list as part of its unknown set, and returns
  register entries for token **999**: the bounds
  (occurrence and positional behaviour, per frame)
  that any proposed identity for 999 must satisfy —
  of which M7's two-condition attack is the
  witness-side form. The pilot frame contains no 999
  (different numbering line, §2 U1), so the pilot
  register records the absence and derives nothing;
  the 999 entries belong to a production register on
  a frame that contains it. Neither recounts the
  other's evidence; M7's rule that witnesses who
  copied each other are one witness has its §5
  analogue (Yajnadevam and Field-Cady are one
  population under two provenances, and count once).
- **M4 (the pending readings).** M4 is gated: it may
  not score until a 44-scale instrument passes its
  own null, and **this method is not a scorer and
  does not lift, loosen, or route around that gate.**
  What M12 lawfully does to M4's cohort: (i) it files
  Tier-C exclusions against a pending reading's
  *type-claims* where those claims contradict the
  sign's row in a named frame — e.g., a reading whose
  claimed value requires neighbour-dependent behaviour
  for sign 031 is excluded *as filed*, because 031 is
  attested only solo in the pilot frame (§7.4). That
  is a deduction about the claim as stated, delivered
  in the fitting frame itself — stronger than a score
  and narrower: it kills the claim as stated, and a
  revised claim is a new claim, not a rescued one.
  (ii) If M4's gate ever lifts, the §6.3 ranking
  supplies *ordering only* — which readings to write
  predictions for first. The ranking never scores,
  promotes, or demotes a reading, and the records must
  never blur a register exclusion with M4's "failed on
  quasi-held-out data": different acts, different
  words.
- **The trigger census.** The census asks an
  existence question about exhibited witness lists
  (does any list identify ≥ 5 celestial signs, each
  occurring in the frozen primary population — the
  per-sign floor as amended by resolutions A1/B1,
  adopted 2026-10-26). M12 neither runs it nor
  pre-judges it, and the census's formal act remains
  the owner's call. The kinship is methodological, and
  one sentence of it is worth writing down: B1's
  per-sign occurrence floor *is* a register-shaped
  condition — the trigger fires only on signs the
  population's own accounting admits as members — and
  if the census ever runs, its worksheet rows are
  register-shaped objects (assumption set, derivation,
  falsifier) whether or not this method is ever frozen.
- **The owner's projected-constraints framework.**
  Stated plainly, and without borrowing authority the
  design has not earned: elsewhere in the owner's
  programmes, a system is understood through the
  constraints its observable projection imposes on
  any completion of it, and the residual — what the
  constraints leave free — is measured rather than
  imagined. This design applies that discipline to a
  corpus. The projection is the surviving
  inscriptions; the constraints are what the
  projection preserves (counts, positions, pairings,
  repetitions); a reading is a completion; the
  residual is the joint possibility set, and §6.3
  prices it. What is borrowed is the *discipline* —
  necessities conditional on stated assumptions,
  exclusions over identifications, the residual made
  explicit — and nothing else: no result from the
  framework's other programmes transfers here as
  evidence, no entry in the register may cite the
  framework as support, and where the framework's
  usage and this spec's definitions differ, §3's
  definitions govern this spec. The method earns its
  standing from this corpus's censuses and from §8's
  null, or not at all.

## 11. Claims of this spec

- **F076-C01 — the derivation is sound and
  reproducible** (design D-M12-C01). The Tier-C
  register derivation, run on a pinned frame under
  the frozen rules, reproduces the frame's accounting
  identities exactly, and its possibility sets are
  functions of the census rows alone. *Falsifier:*
  a recomputation from the pins that violates an
  identity, or two runs of the frozen derivation on
  the same pins producing different registers.
- **F076-C02 — the frame's constraint structure
  exceeds its marginals (pilot-gated)** (design
  D-M12-C02). The pilot frame's constraint structure
  is distinguishable from a marginals-preserving
  scramble in §8's pre-named family, at the
  pre-committed bars. *Falsifier:* either step-2
  statistic inside its null range → the §8 closure
  word. This claim is **filed only if the pilot
  passes**; the pilot record is appended to this
  spec either way.
- **F076-C03 — the vocabulary suffices to state the
  register** (design D-M12-C03). Every Tier-C entry
  the derivation produces is expressible in §3.4's
  vocabulary or §6.1's identity/bound forms.
  *Falsifier:* a derived constraint the vocabulary
  cannot state, produced by the derivation itself —
  whereupon the vocabulary is extended on the record
  as a new claim and prior entries are re-derived,
  never translated by hand.
- **F076-C04…C07 — the assumption claims** A-FRAME,
  A-DIR, A-FACE, A-KEY (§3.2), each with the falsifier
  its §3.2 statement carries.
- **F076-C08 — the positive-control calibration.**
  Coded blind under FF-2, the strict core's claimed
  types are excluded by the machinery at most 5 times
  in 94 (frame-absent strict signs on their own line,
  per CR-7); a higher count closes the pilot
  ASSUMPTION SET DOES NOT HOLD and indicts the
  machinery, the coding rules, or A-FACE before it
  indicts the strict core.
- **F076-C09 — output discipline.** The register
  records set membership, never identity; the ranking
  feeds M4 as ordering only and M7 as bounds only;
  tendencies are annexed, never upgraded.
- **F076-C10 — the non-claims.** This spec claims no
  reading, value, or identification for any sign; not
  that any completion exists; nothing about signs in
  frames not derived; nothing positional about the
  24 frame-absent signs; and not decipherment, in any
  wording: the standing position of the programme —
  **the script is not deciphered** — is unchanged by
  anything in this spec.

## 12. What this spec does not establish

No reading, value, or identification for any sign.
Not that any completion exists — the register narrows
a space it does not prove non-empty (a register whose
exclusions someday covered every type for some sign
would be a finding about the assumption set first and
the corpus second). Nothing about signs in frames not
derived — each frame's register is its own. Nothing
positional about the 24 frame-absent signs — the
register's silence there is filed, not filled.
Nothing about the language behind the script beyond
what the stated assumptions carry. And not
decipherment, in any wording.

## 13. Cost and dependencies

Pilot: days, not weeks — every input is in hand and
pinned (§5, §7); the derivation itself is seconds of
computation, so the real cost is the step-3
basis-coding under its blindness rule and the
record-keeping the gate demands. Production register
on the primary-population frame: gated on the pilot
passing *and* a freeze; its depiction arm (S5) is
additionally gated on the programme's C-1 split
sensitivity standing. Dependencies: the pins cited in
§5/§7; M77 dataset **v3**; the Wells 1998 dataset as
extracted (588 rows, sign 407 carried as explicit NOT
PRINTED). No dependency on ICIT access, on the
Laursen lawful copy, or on any other in-flight
stream — by design: the method was chosen to run on
what the programme already holds.

## 14. The S4 note (scan of 2026-10-26)

The indirect-methods scan adopted S4 as a
governing-rule extension: because a deterministic
generator of seal-like inscriptions for a fictional
non-language passes published statistical language
diagnostics, permutation nulls are necessary but not
sufficient **for score-based methods** — their pilots
must also face a calibrated structured generator
where one exists for their statistic. This pilot is
not a score-based language diagnostic: its two
statistics are census-concentration measures (where
the unread signs' final slots and the solo-only signs
sit, counted exactly) tested against a
marginals-preserving shuffle, and its calibration is
an independent blind positive control over the strict
core, not a comparison against a language-likeness
score. S4 therefore does not add a generator arm to
this pilot; it is recorded here so the boundary is
explicit — if any future use of this register leans
on a statistic of language-likeness, S4 attaches to
that use at that time.
