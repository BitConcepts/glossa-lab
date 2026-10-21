# Spec 043 — PRED-2026-007 at full population, corrected frame: the canonical sign registry as primary source, a documentary provenance gate on the function codes (successor to Spec 038)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-21
>
> This is a **draft** design contract, written
> under the owner's order of 2026-10-21 ("Do the
> successor"), recorded in `adjudication.md`.
> It is the successor to **Spec 038**, whose
> frozen design closed at its step 0.2 on
> 2026-10-20 as **CANNOT BE RUN AS WRITTEN**
> (unscored): the population frame it froze
> named the CGSA analysis file's `icit_function`
> field as the source of the ITM codes, and
> that field carries no coded values (§0.3).
> This draft corrects the frame — the canonical
> sign registry as primary source, its coded
> values verified at draft and its population
> listed in §2 — and adds the gate Spec 038's
> record made unavoidable: a documentary
> **provenance gate** (§4, check 0.3) on what
> the ITM assignments rest on, faced head-on
> in §3. It scores the **same registered
> prediction**, PRED-2026-007, under its frozen
> criterion, with corrected machinery. It does
> not rewrite the prediction, its bar, or its
> population definition.
>
> Number: Spec 041 is the site × local-label
> period-mapping act and Spec 042 is the Arm B
> object-type split, both drafted 2026-10-21,
> so this draft takes **Spec 043** — the next
> free number. The execution phase number is
> allocated at the freeze act (DD-043-13).
>
> Nothing in this draft is frozen and nothing
> is executed. The freeze is a separate owner
> decision — at which the AEE lifecycle hooks
> run as a gate under the programme's current
> aee pin — and execution is a further separate
> owner decision. **What this draft computed,
> stated openly:** a mechanical census of the
> pinned registry's `icit_function` column and
> a re-derivation check of that column against
> the pinned builder rule (§2, `adjudication.md`
> §2). Those are design inputs this frame
> requires — the population is listed in the
> draft, as the corrected design prescribes.
> **No Phase 5 assignment has been looked up
> for any sign the register's own Tested note
> does not already name** (P056, P324, and P310
> were not looked up), and no share has been
> computed.

## 0. Basis

### 0.1 The registered prediction (the contract this design implements)

PRED-2026-007 (H4: ICIT Function Alignment),
registered 2026-04-22 in
`docs/PREDICTION_REGISTER.md` §3, carried
**verbatim**:

- **Prediction**: "Signs with ICIT function
  code ITM will cluster into TERMINAL class in
  CGSA Phase 5 at rate ≥ 70%."
- **Withheld data**: "ICIT function codes (from
  mayig features)"
- **Success criterion**: "≥ 70% of ITM-coded
  signs are TERMINAL or cluster in TERMINAL
  clusters"

The success criterion is the operative scoring
text. Where the Prediction sentence and the
Success criterion differ in wording, the
criterion governs and the difference is
flagged, not harmonised (DD-038-3, carried as
DD-043-7).

### 0.2 The recorded partial test (the pre-execution record)

The register's Tested/Outcome fields, carried
verbatim:

- **Tested**: "PARTIALLY — P385 (ITM) is Cluster
  21 TERMINAL; P378 (ITM) is Cluster 39
  TERMINAL; P098 (LOG) is Cluster 10 INITIAL.
  2/3 ITM in TERMINAL (67%)"
- **Outcome**: "PARTIALLY CONFIRMED (one more
  ITM needed for full pass)"

This is a pre-execution record on a sample of
three named signs, and one feature of it is
stated exactly because the whole successor
turns on it: the note names **two** ITM-coded
signs (P385, P378) and one LOG-coded sign
(P098), yet reports the rate as "2/3" — a
denominator of three checked signs, one of
which is not in the criterion's population.
**The register's 67% figure is a
pre-execution record whose denominator mixed
in a non-ITM sign** (DD-038-1, carried). The
registered criterion ranges over ITM-coded
signs only. This design carries **no
pre-written outcome** for any branch: §7
states the verdict rule mechanically, and
every outcome is whatever that rule yields at
execution over the enumerated population and
the recorded assignments.

### 0.3 What Spec 038 got wrong (its record)

Spec 038 (freeze digest `b54571d8…`, executed
2026-10-20 under the owner's freeze-and-execute
order) closed at its step 0.2. Its record
(`specs/038-pred-2026-007-full-population/outcome.md`;
register §6 entry of 2026-10-20) establishes:

- Check 0.1 passed: every named source was
  present and hashed to its cited value. The
  frame's defect was not missing files.
- Check 0.2 (enumeration) read the primary's
  `icit_function` field mechanically over all
  611 per-sign records of
  `reports/indus_cgsa_cluster_analysis.json`
  and returned **zero ITM-coded signs**: of the
  field's 611 values, **579 are empty and 32
  are free-text decipherment glosses** (for
  example "fish+two -> miiNDu (fish again)");
  no record carries the value ITM, and none
  carries LOG. P385's record carries an empty
  value; P378 has no record in the file at all.
- The study therefore closed as **CANNOT BE
  RUN AS WRITTEN**, unscored. PRED-2026-007
  was neither confirmed nor refuted; its §3
  Outcome stands **PARTIALLY CONFIRMED** as
  the pre-execution record.

The frame's error was a naming error made at
draft: the draft verified the primary source
**by form** (the field exists, with the cited
keys) and deliberately did not inspect its
values, so a field that carries no codes was
frozen as the source of the codes. The codes
were in the other named source all along —
the one Spec 038 had cast as the cross-check.

### 0.4 The corrected frame (this design, in one paragraph)

The primary source is now
`data/crosswalks/canonical_sign_registry.csv`
(SHA-256 `8a0b2a82…`), whose `icit_function`
column this draft **has** read, mechanically
and in full: its values are coded, and §2
lists the entire coded census, the ITM
population included. The CGSA analysis file
is demoted to cross-check, with its known
uncoded state disclosed in advance (§4, check
0.2), so its disagreements are expected,
recorded sign-by-sign, and move nothing. The
registry column must additionally survive a
**re-derivation check**: it is exactly
reproduced by the pinned builder rule that
created it (§4, check 0.2), so the population
rests on a stated rule, not on a file's say-so.
And because Spec 038's provenance record
(DD-038-2) showed the codes descend from
Wells-derived catalog lines — not from
independent function research — this design
adds a **provenance gate** (§4, check 0.3)
that must pass, from documents, before any
Phase 5 assignment is looked up: if the ITM
assignments prove to rest on positional
behaviour in the same catalog lineage the
scored clustering belongs to, the study
closes as **PROVENANCE — CANNOT BE RUN AS
WRITTEN**, unscored. §3 states that threat
precisely.

## 1. Question

Does the registered criterion for
PRED-2026-007 hold over the **full enumerated
population** of ITM-coded signs — every such
sign, not the sample the partial test happened
to check — when the population is enumerated
from a source whose coded values are verified,
and when the codes themselves have passed a
documentary check that they are not merely
positional behaviour wearing a function label?
Plainly: the prediction says signs labelled
ITM in the old ICIT coding end up in
text-ending (TERMINAL) clusters at least 70%
of the time. The only check ever run looked at
two ITM signs (and counted a third, non-ITM
sign in its denominator). This study first
fixes how many ITM signs there actually are —
four, §2 — then asks what those four
assignments rest on, then checks every one of
them against the clustering the prediction
named.

## 2. The population frame (fixed here, listed here, re-derived at step 0)

The population is defined exactly, and —
unlike Spec 038, whose population was an
execution-time fact that did not exist until
the run — its membership is **listed in this
draft**, from a mechanical census of the
pinned primary source taken at drafting
(`adjudication.md` §2). Step 0 re-derives it
at the frozen commit and closes the study if
the re-derivation differs (§4, check 0.2).

- **Unit.** A **distinct sign**, identified by
  the `parpola_id` under which the primary
  source records it. The criterion ranges over
  signs, not inscriptions, tokens, or
  occurrences; frequency plays no part in
  membership or in the share. (P324's recorded
  corpus frequency is 1,366 and P056's is 69;
  each counts once.)
- **Primary source.**
  `data/crosswalks/canonical_sign_registry.csv`,
  column `icit_function` — the canonical sign
  registry `docs/research/SIGN_INVENTORY.md`
  §2 describes as the master sign registry
  (803 signs; created 2026-04-22, CGSA Phase 3).
  SHA-256 at draft:
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`.
- **Inclusion.** A sign is in the population
  if and only if the primary source records
  its `icit_function` value as exactly **ITM**.
- **The coded census (draft, mechanical, in
  full).** Of the registry's 803 rows, 791
  carry an empty `icit_function`; exactly 12
  carry a code — SYL 1, ITM 4, NUM 2, TMK 2,
  SHN 1, LOG 2:

  | Sign | Wells ID(s) | Code |
  |---|---|---|
  | P009 | W100 | SYL |
  | P056 | W231 | ITM |
  | P058 | W233 | NUM |
  | P086 | W390\|W392\|W405\|W406\|W407\|W408 | TMK |
  | P122 | W002 | SHN |
  | P217 | W520 | LOG |
  | P310 | W700 | LOG |
  | P316 | W704\|W705\|W706\|W707 | NUM |
  | P324 | W740 | ITM |
  | P332 | W752\|W760 | TMK |
  | P378 | W820 | ITM |
  | P385 | W817\|W861 | ITM |

  Each coded sign has exactly one coded row;
  every coded row carries at least one Wells
  ID. The parser's code vocabulary also
  includes LON; no registry row carries it.
- **The ITM population.** **P056, P324, P378,
  P385 — four signs.** Two of them (P378, P385)
  are the signs the register's partial test
  named; two (P056, P324) have never been
  through any check. The population strictly
  exceeds the tested sample, so Spec 038's
  census branch (closure with the census as
  the finding, because the population turned
  out to be exactly the tested signs) **cannot
  arise under this frame**; §7 records it as
  foreclosed, not as an available ending.
- **The LOG set, enumerated alongside.**
  **P217, P310 — two signs.** The registered
  criterion ranges over ITM only, and no LOG
  share enters the verdict under this draft.
  The LOG set is enumerated here for three
  stated reasons: the register's own Tested
  note built its defective denominator out of
  a LOG-coded sign, so the corrected record
  must show the LOG class's actual contents;
  the exclusion rule (§2, below) is stated
  against the full coded census, not against a
  sample of it; and the freeze decision is
  asked whether LOG is additionally **scored
  as a control class** or remains
  enumerated-only (DD-043-12, OPEN). Under
  either ruling, the LOG census stands in the
  per-sign record.
- **Exclusion.** Every sign whose recorded
  code is anything else — LOG, SYL, TMK, NUM,
  SHN, LON, or no code — is excluded. The
  standing example is **P098**: the register's
  Tested note calls it "(LOG)", but in the
  primary source P098's row (Wells W400|W402)
  carries **no function code at all** — neither
  ITM nor LOG. Its exclusion from the ITM
  population is therefore a plain application
  of the inclusion rule, doubly secured; and
  the register's "(LOG)" parenthetical is a
  pre-execution label this design does not
  rely on, flagged here rather than smoothed
  (DD-043-5). No held coded source records
  P098 as ITM.
- **No other filter.** No frequency threshold,
  no attestation requirement, no restriction to
  any numbering system beyond the sign IDs the
  registry itself records, and no exclusion of
  signs that turn out to lack a Phase 5
  assignment — those signs are handled by the
  coverage rule (§7), never by quietly
  dropping them from the frame.
- **Deduplication.** By `parpola_id`: each
  distinct sign counts once. Verified at
  draft: no sign carries more than one coded
  row.
- **Ambiguity is a closure, not a judgement
  call.** If at the frozen commit the primary
  source records a sign under conflicting
  codes, or records function codes in a
  multi-code or otherwise ambiguous encoding
  that affects membership, the ambiguity is
  written into the step-0 record and the study
  closes as **CANNOT BE RUN AS WRITTEN**
  rather than resolving membership by
  discretion (§4, check 0.2).

## 3. The provenance problem (DD-038-2, faced head-on)

### 3.1 The derivation chain, from the held documents

The registry's `icit_function` column was not
measured from the corpus by the registry's
builder; it was **transcribed from a
classification the builder took on authority**.
The chain, every link a held or published
document:

1. **The builder.** `scripts/cgsa_pipeline.py`
   (SHA-256 `4af822f1…`), whose Phase 3 built
   the canonical registry, populates
   `icit_function` from a hand-written table,
   `_WELLS_FUNCTIONS` — fourteen Wells-ID keys
   mapped to codes — under the comment "Known
   ICIT/Wells sign function assignments (from
   ICIT docs + Fuls 2013)". The assignment rule
   is mechanical: the code of the first table
   key, in table order, found among the sign's
   Wells IDs; no key, no code. The six ITM
   keys are W740, W585, W820, W817, W861, W231;
   W585 matches no registry row. The same
   script cites its taxonomy source in its own
   summary: "Fuls 2013 paper: NWSP method
   reference + sign function taxonomy".
2. **The lineage.** `backend/glossa_lab/data/fuls_parser.py`
   (SHA-256 `9b57f0ec…`) reads the same code
   vocabulary (NUM, LON, SHN, TMK, ITM, LOG,
   SYL) from sign-catalog lines of "A Catalog
   of Indus Signs" (Fuls 2023), under the
   annotation **"Function classification (from
   Wells)"**. This is the lineage DD-038-2
   established and the register's §6 note of
   2026-10-20 recorded: the codes descend from
   Wells-derived catalog lines, transmitted
   through Fuls/ICIT documents — **not** from
   the mayig features the register's §3 line
   names, and not from any function research
   independent of that lineage.
3. **The classification's origin.** Wells'
   published sign list, as transmitted by the
   ICIT documentation and Fuls 2013's taxonomy.
   What that classification **rests on** is the
   question §3.2 poses and the gate (§4, check
   0.3) must answer from the documents
   themselves.

### 3.2 The circularity threat, stated precisely

The scored side of this study is positional
through and through: the CGSA Phase 5 clusters
were built from signs' positional behaviour,
and their recorded classes are INITIAL,
MEDIAL, TERMINAL. The threat is that the
population side is positional too — in which
case the test measures the classification's
agreement with its own construction:

- **The class name is a positional gloss.**
  The builder's own table expands W740's ITM
  as "**Initial Cluster Terminal Marker**" —
  a class defined, on its face, by where its
  signs sit relative to a cluster's end. Its
  sibling glosses point the same way: TMK is
  "Terminal Marker"; W407's TMK is annotated
  "Fish terminal". A gloss is not a derivation
  record — but a class whose transmitted name
  *is* a positional description cannot be
  presumed position-independent.
- **The catalog format juxtaposes function and
  position on one line, and the pipeline's own
  reading of it cannot separate them.** The
  parser's `parse_sign_catalog_entry` extracts
  from a single catalog line a frequency, a
  **positional classification** (it searches
  the line for "initial", "terminal",
  "medial", "post-terminal") and a **function
  classification**. Its own test fixture is
  the line "Sign 342: frequency 580, terminal,
  TMK", from which it reads all three at once.
  A transcription that reads the function
  token and the positional word off the same
  printed line is consistent with two very
  different worlds: one where Wells assigned
  the function on grounds independent of
  position and the catalog merely prints both
  facts together, and one where the function
  *is* the positional observation, renamed.
  The held record does not distinguish these
  worlds. The gate exists to distinguish them.
- **If the second world is the real one, the
  registered criterion is near-tautological.**
  "Signs coded ITM are TERMINAL in a positional
  clustering at ≥70%" would then say: signs
  selected (in the Wells lineage) for closing
  initial clusters / ending texts do in fact
  cluster terminally in this corpus's
  positional clustering. That is a consistency
  property of the classification's
  construction, not evidence that the
  classification captures a function of the
  signs — and a CONFIRMED verdict stated
  without that boundary would claim more than
  the test can carry.

### 3.3 What settles it — and what the gate is not

The gate (§4, check 0.3) settles the question
**from documents, before any scoring**: the
published sources the builder itself cites
must state, with locators, what the ITM class
is defined by and what each ITM assignment
rests on. If those statements ground the
assignments in something other than the signs'
positional distribution, the gate passes and
the verdict that follows is honestly bounded
(§10). If they ground the assignments in
positional behaviour — or state no checkable
basis, or cannot be produced — the study
closes unscored under its own closure name.

The gate is **not** an analyst's plausibility
judgement, and it is not a literature review
whose conclusion a reader must take on trust:
its evidence set, its three limbs, and its
failure outcomes are fixed here in advance;
the execution record quotes the produced
documents' basis statements with locators, so
the gate's determination is itself checkable.
The one element this draft deliberately does
**not** fix is the adjudication standard for
borderline documents — how explicit a stated
basis must be to count as stated — which is
recorded as OPEN for the freeze (DD-043-10),
with the draft's recommendation. Silence in a
produced document is already fixed as failure;
only the borderline standard is open.

## 4. Step 0 — sources, re-derivation, provenance gate, recorded-output verification; fail-closed, in a fixed order

Step 0 runs before any scoring, in this
order. Each check has a stated failure
outcome; no check is waived, sampled, or
repaired by substitution. **No Phase 5
assignment is looked up for any sign — the
sanity anchor included — until check 0.3 has
passed.** The population side may be fixed
before its provenance is judged; nothing
positional may be read against it until the
gate has passed.

### 0.1 Fix the sources and their pins

The sources are named here, before any
enumeration, so the population cannot be
chosen by shopping among tables — the failure
mode Spec 038's DD-038-5 guarded against and
its own frame then fell to from the other
side, by naming an unverified field. Every
pin below was verified first-hand at draft
(`adjudication.md` §2).

| Role | Source | SHA-256 |
|---|---|---|
| Primary (population) | `data/crosswalks/canonical_sign_registry.csv`, column `icit_function` | `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` |
| Cross-check | `reports/indus_cgsa_cluster_analysis.json`, field `data.a[].icit_function` | `8c2bd6059a671068b645204db37e29ff13ca53009117b9447ed6c7bd1ead02b3` |
| Builder (derivation rule) | `scripts/cgsa_pipeline.py` (`_WELLS_FUNCTIONS`, Phase 3 registry builder) | `4af822f1ad5c924defed7852df967f8633899b27a27fdaea84e2cdad8744efb0` |
| Lineage (catalog reading) | `backend/glossa_lab/data/fuls_parser.py` | `9b57f0ecc10905c0746f1e7fb8e0622ac18e3b08e62bb2eb34fbec4bbd8ef615` |
| Scoring (assignment) | `outputs/analysis/sign_clusters.json` | `623a787dd9cc93c4d3d36377890c4753e3427f57cf7ad70adcd6e8256ba1394a` |
| Scoring (cluster classes) | `reports/cluster_characterization.md` | `54ebf660873fd853a64ce91c7e30d8c4cedc5bc3a0a1555db1f6281a52e3c476` |
| The contract | `docs/PREDICTION_REGISTER.md` (§3 entry; §6 discipline) | `f281bd674d7651e9c13351bad7cb321bd55000cd3f087a38276a4451fbbf7ef3` at draft |

Step 0 verifies each source's presence and
records its SHA-256 at the frozen commit. A
missing source, or a hash that differs from
the frozen record's pin, closes the study as
**CANNOT BE RUN AS WRITTEN**: the draft's
census and gate design are statements about
these files, and a different file is a
different study. No pin is refreshed silently
at execution; a changed file is a freeze
amendment's business, not an execution
repair.

**The mayig features are not a source.** The
files under `data/raw/other_sites/mayig_features/`
carry no function codes (Spec 038 §0.3;
DD-038-2); the register's "from mayig
features" line was already reconciled by
append in the register's §6 (2026-10-20).
This design appends no second reconciliation;
it cites the standing one.

### 0.2 Enumerate the population, and re-derive the column that defines it

Two mechanical reads, both over the whole
primary source, fixed in advance:

- **Enumeration.** Read `icit_function` over
  all 803 registry rows; the population is
  every distinct `parpola_id` whose value is
  exactly ITM, and the full coded census (all
  classes) is recorded with it. The count of
  rows read is recorded and reconciled against
  the file's own structure.
- **Re-derivation.** Apply the pinned builder
  rule — `scripts/cgsa_pipeline.py`'s
  `_WELLS_FUNCTIONS` table, first matching key
  in table order over the row's own split
  `wells_ids` — to every row of the pinned
  registry, and require the derived value to
  equal the row's recorded `icit_function`
  for **all 803 rows**. (Verified at draft:
  exact agreement, zero mismatches; the
  table's W585 ITM key matches no row.)
  Re-derivation failure means the file in hand
  is not the file the builder rule produces —
  the population would rest on a column nobody
  can account for — and closes the study as
  **CANNOT BE RUN AS WRITTEN**.

**Reconciliation against the draft census.**
The enumeration must reproduce §2 exactly:
ITM = {P056, P324, P378, P385}, population 4,
and the coded census of 12. Any difference —
a sign gained, lost, or recoded — closes the
study as **CANNOT BE RUN AS WRITTEN**: the
draft's design (its arithmetic, its gate, its
boundaries) is written against the listed
population, and a different population is a
different design. The closure record states
the difference sign-by-sign.

**Held-record verification, read at the same
pass.** The register's Tested note names P385
and P378 as ITM: both must appear in the
enumeration (they do, §2). P098 must not
appear as ITM (it carries no code). A failure
of either is a discrepancy written into the
step-0 record; under the frame it can only
arise through a census difference, and closes
the study with it.

**Cross-check, with its disagreements
expected and recorded.** The cross-check
source (`reports/indus_cgsa_cluster_analysis.json`)
is read over the whole file under the
conflict rule below. Its state is known in
advance from Spec 038's execution record, and
the expectation is stated here so the
execution record is checked against it: its
`icit_function` field is **not coded** (579
empty, 32 free-text glosses, no ITM and no LOG
values anywhere; P385's record empty; P378
and P098 without records). Every disagreement
between the cross-check and the enumeration
is therefore expected to take exactly that
form, and each is written sign-by-sign into
the step-0 record and published with the
outcome, as Spec 038's conflict rule
prescribed. **Conflict rule, fixed in
advance:** the primary governs membership;
cross-check disagreements never add or remove
a member; a disagreement of a *different
kind* than the recorded expectation (for
example, the cross-check coding a sign ITM
that the registry does not, in a coded value)
is written into the record as an unexplained
discrepancy and reported with the outcome —
it does not close the study, because the
cross-check's authority under this frame is
nil and its known state is disclosed; what
closes the study is ambiguity or conflict
**within the primary itself** (§2), a pin
failure (check 0.1), or a re-derivation or
census failure (this check). No union, no
intersection, and no third source is
consulted to break a tie.

### 0.3 The provenance gate

The gate runs after the population is fixed
and before any Phase 5 lookup. Its evidence
set is named here; documents not in the set
cannot be introduced at execution to rescue a
failing gate, and set documents that cannot
be produced fail it.

**Evidence set.**

- **D1 — the pinned builder** (`scripts/cgsa_pipeline.py`,
  check 0.1): establishes the immediate
  derivation and its own stated sources —
  "ICIT docs + Fuls 2013" — and the table's
  glosses, including ITM's expansion "Initial
  Cluster Terminal Marker".
- **D2 — the pinned parser**
  (`backend/glossa_lab/data/fuls_parser.py`)
  with its test: establishes the catalog-line
  format, the "(from Wells)" attribution, and
  the same-line juxtaposition of function and
  positional class.
- **D3 — the cited taxonomy source**: Fuls
  2013, the publication the builder cites for
  the "sign function taxonomy" — produced at
  execution with locators for its statements
  of what the function classes are and on what
  basis signs are assigned to them.
- **D4 — the classification's published
  origin**: Wells' published sign list (the
  source of the "(from Wells)" classification,
  as transmitted by the ICIT documentation the
  builder cites) — produced at execution with
  locators for its definition of the ITM class
  and for the assignments of W231, W740, W820,
  and W817/W861 (the Wells IDs behind P056,
  P324, P378, P385).

**The three limbs.** The gate passes only if
all three hold:

1. **Class-definition limb.** The produced
   documents state what ITM *is*, and the
   stated definition is not a positional one:
   the class is not defined by its signs'
   distribution across inscription positions,
   by cluster-final or text-final behaviour,
   or by any statistic of where its signs
   occur.
2. **Per-sign basis limb.** For **each** of
   the four ITM signs, the produced documents
   state the basis of its assignment, and that
   basis is position-independent — it does not
   rest on the sign's start, internal, or end
   rates, its cluster position, or any other
   positional statistic, whether computed on
   this corpus or on the lineage's own.
3. **Source-agreement limb.** Where the
   produced published documents list per-sign
   function assignments, they agree with the
   builder table for all four ITM signs. A
   published list that assigns any of the four
   a different function — or omits it where
   the table asserts it — means the registry's
   code rests on the builder's hand
   transcription against its own cited source:
   a provenance defect, and a gate failure.

**Failure outcomes — all fail-closed, one
closure.** The study closes as **PROVENANCE —
CANNOT BE RUN AS WRITTEN**, unscored, if: any
limb fails; the documents state a positional
basis for the class or for any single ITM
sign; the documents state no basis that can
be checked for the class or for any single
ITM sign; or D3/D4 cannot be produced. A
single sign's failure closes the whole study:
scoring the remaining signs would silently
change the population the registered
criterion names, and no subset verdict is
available under this design. The closure
record quotes, with locators, the basis
statements the gate rested on — or records
their absence — so the closure is checkable
in its turn. On a provenance closure,
PRED-2026-007 remains unscored and its §3
Outcome stays **PARTIALLY CONFIRMED** as the
pre-execution record (§8).

**Bounded proceed.** If all three limbs hold,
scoring proceeds, and the gate's finding —
the stated bases, with locators — is carried
into the step-0 record and quoted in every
outcome statement (§7, §10). The proceed is
bounded by §10's boundary: the classification
remains a Wells-lineage classification
transmitted through Fuls/ICIT documents and a
hand-written builder table, and the verdict
speaks about that classification, not about
the signs' true functions.

**The LOG trace.** The gate traces the two
LOG assignments (W520 → P217, W700 → P310)
through the same evidence set and records the
finding in the step-0 record, in the same
form. Under this draft the LOG trace does not
gate anything, because no LOG quantity is
scored; if the freeze rules LOG scored as a
control (DD-043-12), the trace's standard for
the control is fixed by that ruling.

### 0.4 Verify the recorded Phase 5 output survives in sign-assignable form

The scoring reads **only** the recorded CGSA
Phase 5 output: the sign → cluster assignment
(`outputs/analysis/sign_clusters.json` —
verified surviving at draft by its pin: best_k
40, `sign_to_cluster` for 160 signs, 40
populated cluster lists; corroborated by
`reports/cgsa_validation_report.md`, dated
2026-04-22, the registration day) and the
recorded per-cluster class characterisation
(`reports/cluster_characterization.md`,
generated 2026-04-22, 40 clusters). If that
output does not survive in a form that assigns
a cluster and a cluster class to a sign, the
study closes as **CANNOT BE RUN AS WRITTEN**,
unscored: a fresh clustering is a new
prediction's business, under a new number.
**No re-clustering is run under this spec,
for any reason.**

**Cluster-class rule (DD-038-9, carried as
DD-043-7).** A cluster's class is the class
recorded for that cluster in
`reports/cluster_characterization.md` — the
Phase 5 characterisation generated the day
the prediction was registered, whose
per-cluster classes are the very ones the
register's Tested note used (Cluster 21
TERMINAL, Cluster 39 TERMINAL, Cluster 10
INITIAL). The rule is a deterministic lookup
in a named, hashed record; it invents no
threshold and derives no class from rates at
execution. If an enumerated sign's cluster has
no class recorded there, that sign counts as
**unassigned** under the coverage rule (§7) —
its class is never inferred.

**Sanity anchor, fixed at draft.** The
recorded output must reproduce the register's
three named assignments — P385 → Cluster 21
(TERMINAL), P378 → Cluster 39 (TERMINAL),
P098 → Cluster 10 (INITIAL). If it does not,
the output in hand is not the output the
registered test named, and the study closes
as CANNOT BE RUN AS WRITTEN. (This check runs
here, after the gate — not before it: the
anchor is a Phase 5 lookup, and no Phase 5
lookup precedes the gate.)

### The step-0 record

The outcome of every check — the sources and
their hashes, the enumeration and the full
coded census, the re-derivation result, the
cross-check disagreements sign-by-sign, the
provenance gate's determination with its
quoted basis statements and locators, the
Phase 5 output verification — is written as a
step-0 record and hashed before any scoring
begins (the house pattern). If a check closes
the study, that record is the outcome,
reported as a closure under its own name,
not a verdict (§7).

## 5. Data

- **Function codes (the population side).**
  The primary source and cross-check named at
  §4 check 0.1
  (`data/crosswalks/canonical_sign_registry.csv`
  `icit_function`; cross-check
  `reports/indus_cgsa_cluster_analysis.json`
  `data.a[].icit_function`). At draft, the
  primary was read in full for its coded
  census (§2) and its column re-derived
  against the pinned builder rule; the
  cross-check's contents are taken from Spec
  038's execution record, not re-read.
- **Derivation and lineage (the provenance
  side).** The pinned builder and parser
  (check 0.1), and at execution the produced
  published documents D3/D4 (§4, check 0.3).
- **Cluster assignments (the scoring side).**
  The recorded CGSA Phase 5 output only:
  `outputs/analysis/sign_clusters.json`
  (assignment) and
  `reports/cluster_characterization.md`
  (cluster classes, per DD-043-7). Nothing is
  re-clustered, re-characterised, or
  re-derived.
- **The register.** `docs/PREDICTION_REGISTER.md`
  §3 (PRED-2026-007 entry) and its §6 append
  discipline (§8 below).

Rights posture: the held sources are the
programme's own record; the published
documents D3/D4 are cited with locators, not
reproduced beyond the basis statements the
gate record must quote. The study publishes
the per-sign table and statistics, as the
design prescribes.

## 6. Method

Exactly the registered computation, nothing
added. For every sign in the enumerated
population (§2, §4 check 0.2), take its
cluster assignment from the recorded Phase 5
output (§4 check 0.4). A sign **counts as
TERMINAL** if and only if its recorded
cluster's class — under the DD-043-7
operationalisation, the class recorded for
that cluster in
`reports/cluster_characterization.md` — is
TERMINAL (DD-043-7: the criterion's "TERMINAL
or cluster in TERMINAL clusters" is carried
verbatim in §0.1; the operative reading —
count TERMINAL-cluster memberships — is Spec
038's, carried, and any held record that
assigns a sign a class differing from its
cluster's recorded class is reported in the
outcome, not resolved by discretion). Count
the TERMINAL signs; divide under the coverage
rule (§7); compare to 70%.

One descriptive addition is pre-registered
here so it cannot be mistaken for a criterion:
the **per-sign table** — every enumerated ITM
sign, its cluster, its cluster's class (or
"no recorded Phase 5 assignment"), and with
it the full coded census of §2 including the
LOG set and P098's exclusion — is published
with the outcome, so no reader has to trust a
bare percentage over a four-sign population.
The table is descriptive only; it carries no
criterion and moves no verdict.

## 7. Criteria and verdict mapping

These are the register's criteria, not this
spec's. **The verdict rule, stated
mechanically:** the share is the number of
enumerated ITM signs that count as TERMINAL
under §6, divided by the denominator the
coverage rule below fixes (the enumerated
population, or the assigned population where
the coverage rule applies), compared against
the 70% bar. Nothing else enters the verdict —
not the register's recorded 67%, not the
sample's history, not the provenance gate's
finding (the gate decides whether scoring may
run at all; it is not evidence in the share),
and not any expectation written anywhere,
including in this draft.

- **CONFIRMED** — the share is at least 70%.
- **NOT CONFIRMED** — the share is below 70%.

There is no inconclusive band in the
registered criterion, and this spec does not
invent one.

**Small-population arithmetic, stated in
advance.** The population is four signs. The
possible full-population shares are 0, 25,
50, 75, and 100 percent; the 70% bar passes
only at 3 or 4 of 4; each sign carries 25
percentage points of the verdict. Every
outcome statement must present the share
together with the population size and the
per-sign results in the same paragraph — a
bare percentage over four signs is a
misstatement of this test's weight, whatever
it says.

**Coverage rule (the design's, carried from
Spec 038's DD-038-4 in substance).** If some
enumerated ITM signs have no recorded Phase 5
assignment, the share is computed on the
**assigned population** and the coverage is
stated in the verdict's first sentence —
*unless* the unassigned signs cannot change
the outcome arithmetically (the bar already
reached even if all unassigned are
non-TERMINAL, or unreachable even if all are
TERMINAL), in which case the verdict is
decisive and coverage is still stated. If
coverage is below 80% and the outcome is not
arithmetically decisive, the appended register
entry records the test as
**run-at-partial-scope** with the numbers, and
the register's PARTIALLY CONFIRMED wording is
replaced by that precise statement — by
append, never by edit (§8). With four signs,
the rule's arithmetic is concrete: one
unassigned sign is 75% coverage, inside the
partial-scope band unless the three assigned
signs already decide the outcome either way.

**Census branch — foreclosed under this
frame.** Spec 038 carried D-31's census
branch (if the enumerated population is
exactly the signs already tested, close with
the census as the finding and score at that
scope). Under this draft's listed population
it cannot arise: the population is four ITM
signs, of which two (P056, P324) have never
been tested. No census completion is
available to this spec, and no outcome may
claim one. (If step 0's re-derivation ever
produced a different population, that is a
census failure and a closure under check 0.2
— not a route into the census branch.)

**Step-0 closures — two kinds, each reported
under its own name.** A closure is reported
as itself, never as a verdict: PRED-2026-007
remains unscored by this execution, and the
register's §4 (Failed Predictions) gains no
entry from a closure.

- **CANNOT BE RUN AS WRITTEN** — a source,
  integrity, or recorded-output failure
  (checks 0.1, 0.2, 0.4): a pin mismatch, a
  re-derivation or census failure, ambiguity
  within the primary, a missing or
  non-assignable Phase 5 output, or a failed
  sanity anchor.
- **PROVENANCE — CANNOT BE RUN AS WRITTEN** —
  the provenance gate's failure (check 0.3):
  the ITM assignments rest on positional
  grounds, or on no checkable stated grounds,
  or the documents that would settle it
  cannot be produced or do not agree with the
  builder table. This closure is a finding
  about the classification's provenance, not
  about the criterion's truth, and it is
  recorded under its distinct name so it can
  never be mistaken for a source defect or
  read as a verdict either way.

**Pre-written verdict wordings.** The
appended register entry and the outcome
record use these forms, with the bracketed
quantities filled from the execution record
and no other wording substituted:

- *CONFIRMED:* "PRED-2026-007 is CONFIRMED at
  full population. Of the [4] ITM-coded signs
  enumerated from the canonical sign registry
  (P056, P324, P378, P385), [n] are TERMINAL
  in the recorded CGSA Phase 5 output, a
  share of [x]% against the registered bar of
  70%. Coverage: [c] of [4] enumerated signs
  carry a recorded Phase 5 assignment. The
  provenance gate (Spec 043, check 0.3)
  passed: the ITM assignments rest on the
  stated position-independent bases recorded
  in the step-0 record. This verdict states
  that the Wells-lineage ITM classification
  aligns with the recorded Phase 5 TERMINAL
  clusters at the registered rate; it does not
  establish what ITM signs mean, that ITM is
  the script's true function class, or that an
  independent classification would agree."
- *NOT CONFIRMED:* the same form, with "is
  NOT CONFIRMED" and the share below the bar;
  the boundary sentences are carried
  unchanged, with "aligns" replaced by "does
  not align at the registered rate" in the
  final sentence's first clause.
- *Run-at-partial-scope:* "PRED-2026-007 was
  run at partial scope. Of the [4] ITM-coded
  signs enumerated from the canonical sign
  registry, [c] carry a recorded Phase 5
  assignment; on the assigned population the
  TERMINAL share is [x]%, which does not
  decide the registered criterion, because the
  unassigned sign(s) could carry the share
  across the 70% bar in either direction. The
  test is recorded as run-at-partial-scope
  with these numbers; no verdict is claimed."
  (Followed by the gate finding and the
  per-sign table, as in every outcome.)
- *Closure (source/integrity):* "PRED-2026-007
  was not scored under Spec 043: CANNOT BE RUN
  AS WRITTEN at step 0, check [0.1/0.2/0.4] —
  [the named failure, stated exactly]. The
  prediction remains unscored; its §3 Outcome
  stands PARTIALLY CONFIRMED as the
  pre-execution record. This closure is not a
  verdict and not a refutation."
- *Closure (provenance):* "PRED-2026-007 was
  not scored under Spec 043: PROVENANCE —
  CANNOT BE RUN AS WRITTEN at step 0, check
  0.3. [The gate's finding, stated exactly:
  the basis the produced documents state for
  the class / for sign P—, with locators — or
  the absence of a checkable stated basis —
  or the documents' non-production.] The ITM
  population was fixed ([4] signs) and no
  Phase 5 assignment was looked up. The
  prediction remains unscored; its §3 Outcome
  stands PARTIALLY CONFIRMED as the
  pre-execution record. This closure records
  what the classification's assignments rest
  on; it is not a verdict on the criterion
  and not a refutation."

## 8. Register handling at execution

The outcome, whatever it is, is appended to
`docs/PREDICTION_REGISTER.md` as a dated entry
under §6 (insertions only), under the owner's
execution order, and the Phase D register-hash
pin is advanced by name for that authorised
change.

- On a **verdict** (CONFIRMED / NOT
  CONFIRMED, including a decisive verdict
  under partial coverage), the appended entry
  records the supersession of the PARTIALLY
  CONFIRMED wording in the §7 wording's terms;
  the §3 text as registered is never edited in
  place, and the PARTIALLY CONFIRMED wording
  stands in the record as the pre-execution
  record it is, superseded by the appended
  entry.
- On a **run-at-partial-scope** record
  (coverage rule, §7), the appended entry
  replaces the PARTIALLY CONFIRMED wording
  with the precise partial-scope statement.
- On a **step-0 closure of either kind**, the
  §3 Outcome stays **PARTIALLY CONFIRMED** as
  the pre-execution record — the Spec 035
  precedent (F035-C15), carried through Spec
  038: a closure is not a verdict, and the
  register does not record it as one. The
  dated entry records the closure under its
  own name (PROVENANCE closures included),
  with the step-0 record cited.
- No new provenance reconciliation is
  appended: DD-038-2's reconciliation stands
  in §6 (2026-10-20). The execution's dated
  entry cites it and adds this frame's
  provenance-gate finding, which is new
  information, not a second reconciliation.

Every other prediction's entry stays
byte-identical. This draft changes no register
text, no other prediction's state, and no Spec
026–042 record.

## 9. Controls and named confounders

- **Clustering stability, answered by
  fidelity, not repair.** Cluster membership
  is asked to carry weight while the
  programme's cross-compilation work shows
  sign treatment is contested. The registered
  test named this clustering, so this
  clustering is what gets scored; the caveat
  rides in the appended entry and in every
  outcome statement. The instability is not
  repaired, averaged over, or re-run away
  (§4, check 0.4).
- **Small-population arithmetic.** The
  population is four signs; each sign is 25
  percentage points. The per-sign table (§6)
  is published so the arithmetic is visible;
  no outcome statement may present the
  percentage without the population size in
  the same paragraph (§7).
- **The provenance tangle is the design's
  centre, not a footnote.** The codes descend
  from a Wells-lineage classification (§3.1),
  the register's original provenance line was
  false to the files (reconciled by append,
  DD-038-2), and the class's own transmitted
  name is positional (§3.2). The provenance
  gate (§4, check 0.3) exists so that no
  outcome statement can present a CONFIRMED
  verdict as independent corroboration of the
  classification unless documents have first
  established that the classification was not
  built from the behaviour the test measures.
- **Table-shopping, answered by verification,
  not by naming alone.** More than one held
  source records function codes. Spec 038
  named its primary and cross-check in advance
  and still froze an uncoded field, because
  naming is not verification. This design
  names the registry primary **because its
  values were read and re-derived at draft**
  (§2, §4 check 0.2), demotes the CGSA file to
  a cross-check whose disagreements are
  expected in kind and published in full, and
  closes the study if the frozen-commit files
  differ from the pinned ones. No later
  preference among tables can move the
  population, because the population is
  already listed.
- **The recorded partial test is not evidence
  about the population.** That the two named
  ITM signs landed TERMINAL says nothing about
  the two never checked; no outcome statement
  may present the sample's 2-of-2 (or the
  register's 2/3) as a prior estimate of the
  full-population share.
- **Frequency is not weight.** P324 is among
  the most frequent signs in the corpus and
  P056 among the rarer coded ones; the
  criterion ranges over signs, and the share
  counts each once (§2, §6). No outcome
  statement may re-weight by frequency in
  either direction.

## 10. What this design would move, and what it would not establish

**What it would move.** PRED-2026-007 from a
partial check on a mis-denominated sample to
one of three honest endings: a scored result
at full enumerated scope over a verified
population whose codes have passed a
documentary provenance gate; a precise
partial-scope record if the recorded Phase 5
output cannot assign the whole population;
or a named closure — source/integrity, or
PROVENANCE — that states exactly why the test
cannot be run as written. Each ending replaces
an acceptance-flavoured label with the record
that actually supports it.

**What it would NOT establish — the lineage
boundary, carried into every outcome
statement.** The ITM classification under
test is a Wells-lineage classification,
transmitted through ICIT documentation and
Fuls 2013's taxonomy, hand-tabulated in the
programme's own builder, and read off a
registry the programme built. A CONFIRMED
verdict under this spec therefore states
exactly this: **the Wells-lineage ITM class,
as enumerated in the pinned registry, aligns
with the recorded CGSA Phase 5 TERMINAL
clusters at or above the registered 70%
rate** — a statement about one
classification's internal consistency with
one recorded clustering of the same corpus
lineage. It does **not** establish that ITM
signs *mean* anything terminal; that ITM is
the script's true function class; that Wells'
classification is correct; that an independent
classification, built without the Wells
lineage, would agree; or that the Phase 5
clustering carves the script at its joints.
Even with the provenance gate passed, the
classification and the clustering are products
of one scholarly lineage's engagement with one
corpus; the gate removes the specific
circularity of §3.2 — assignments derived
from the positional behaviour under test —
and no more than that. A NOT CONFIRMED
verdict is bounded symmetrically: it states
that this classification does not align with
this clustering at the registered rate, and
refutes nothing beyond the registered
criterion as registered.

## 11. Execution shape (phase allocated at freeze — NOT run by this spec)

1. **Graph-first build** (H15/H23): experiment
   script, graph module, registration in the
   experiment graph, then run.
2. **Step 0** (§4): sources and pins;
   enumeration with re-derivation and census
   reconciliation; the provenance gate; Phase
   5 output verification — in that order,
   fail-closed, with the step-0 record written
   and hashed before any scoring. A step-0
   failure closes the study under its own
   name (§7), and the closure is the outcome.
3. **Scoring** (§6): the registered
   computation only; the per-sign table
   produced with it.
4. **Outcome:** the verdict under §7, the
   partial-scope record, or the closure —
   appended to the PRED register as a dated
   entry (§8), recorded in this spec's
   directory and the root LEDGER; the
   foundation check (H21) run after the claim
   consequence lands; nothing written into any
   frozen record.

## 12. What this spec does not do

- It does not execute anything. Execution
  follows the owner's freeze order for this
  contract and a separate execution order.
- It does not re-register, amend, or replace
  PRED-2026-007. The prediction, its success
  criterion, its 70% bar, and its population
  definition (ITM-coded signs) stand exactly
  as registered in April 2026; this spec is
  corrected machinery for scoring it, under
  the owner's successor order (DD-043-6).
- It does not look up any Phase 5 assignment
  beyond the three signs the register itself
  names, compute any share, or pre-write any
  outcome (§0.2). The computations it does
  perform — the registry census and the
  re-derivation check — are population-side
  design inputs, disclosed where they are
  used (§2).
- It does not re-run, re-derive, or substitute
  any clustering (§4, check 0.4), adjust the
  70% bar, add a band, or substitute a
  different test (§§6–7).
- It does not edit the PRED register — every
  outcome record is an execution-time append
  (§8).
- It files no OSF registration at draft.
  PRED-2026-007 predates the programme's OSF
  registration practice and carries no
  preregistration of its own; whether the
  frozen spec files its own OSF contract
  registration (the Spec 032–039 pattern) is a
  freeze-time decision, recorded as DD-043-11.
- It does not silently harmonise the design
  and the register where they disagree: every
  disagreement found is flagged in
  `adjudication.md` as a DD (§14).

## 13. Governed claims (summary)

The governed register is `claims.json`
(F043-C01…C16):

- **C01** — a verdict under this spec states
  whether the registered criterion for
  PRED-2026-007 is met over the
  registry-enumerated ITM population, and
  nothing beyond that statement.
- **C02** — the success criterion is the
  registered one, carried verbatim: at least
  70% of ITM-coded signs are TERMINAL or
  cluster in TERMINAL clusters; CONFIRMED at
  70% or above, NOT CONFIRMED below, no band
  added; the small-population arithmetic is
  stated wherever the share is stated.
- **C03** — the population is every distinct
  sign whose `icit_function` in the pinned
  canonical sign registry is exactly ITM; the
  registry is primary because its coded values
  were verified at draft; the CGSA analysis
  file is cross-check only, its known uncoded
  state disclosed, its disagreements published
  sign-by-sign and never moving membership.
- **C04** — the registry's `icit_function`
  column is exactly re-derivable from the
  pinned builder rule over the registry's own
  Wells IDs, over all 803 rows; re-derivation
  failure closes the study as CANNOT BE RUN
  AS WRITTEN.
- **C05** — the population is listed at draft
  (P056, P324, P378, P385; four signs), and
  step 0's re-enumeration must reproduce the
  draft census exactly or the study closes;
  the census branch cannot arise under this
  frame.
- **C06** — P098 is excluded by rule: it
  carries no ITM code in the primary source
  (no code at all); the register's 67%
  denominator defect is not reproduced, and
  its "(LOG)" parenthetical is not relied on.
- **C07** — the LOG set (P217, P310) is
  enumerated in the census and the per-sign
  record; no LOG share enters the verdict
  under this draft; whether LOG is scored as
  a control is the freeze's decision
  (DD-043-12).
- **C08** — no Phase 5 assignment is looked up
  for any sign before the provenance gate has
  passed; the gate runs at step 0, in the
  fixed order, fail-closed.
- **C09** — the provenance gate is documentary
  and three-limbed (class definition, per-sign
  basis, source agreement); a positional or
  unstated basis for the class or for any one
  ITM sign, non-production of the named
  documents, or a source disagreement closes
  the study as PROVENANCE — CANNOT BE RUN AS
  WRITTEN, unscored; no subset verdict exists.
- **C10** — every outcome statement carries
  the lineage boundary: a verdict is a
  statement about the Wells-lineage ITM
  classification's consistency with the
  recorded Phase 5 clustering — not about the
  signs' true functions or meanings, Wells'
  correctness, or any independent
  classification.
- **C11** — scoring reads the recorded CGSA
  Phase 5 output only; a cluster's class is
  the class recorded for it in the Phase 5
  characterisation (DD-043-7); no
  re-clustering is run, and if the output does
  not survive in sign-assignable form, or the
  sanity anchor fails, the study closes as
  CANNOT BE RUN AS WRITTEN.
- **C12** — the coverage rule is the design's,
  fixed in advance (carried from DD-038-4):
  assigned-population denominator, coverage in
  the verdict's first sentence, the
  arithmetic-decisiveness exception, and the
  partial-scope record below 80% coverage.
- **C13** — the per-sign table is published
  with the outcome as a descriptive record,
  carrying the full coded census with it; it
  carries no criterion.
- **C14** — the outcome is appended to the
  prediction register as a dated entry; the
  registered §3 text is never edited, every
  other entry stays byte-identical, and the
  Phase D pin is advanced by name for the
  authorised append.
- **C15** — step-0 closures are reported as
  themselves, under their own names (source/
  integrity vs PROVENANCE), never as verdicts;
  a closure is not a refutation, and on a
  closure the §3 Outcome stays PARTIALLY
  CONFIRMED.
- **C16** — every outcome statement carries
  the clustering-stability caveat: fidelity
  to the named clustering, not repair of it.

## 14. Design decisions

- **DD-043-1 — DECIDED-BY-DRAFT: the registry
  is primary; the roles of Spec 038's two
  sources are reversed, and the reason is
  verification, not preference.** Spec 038's
  DD-038-5 named the CGSA analysis file
  primary and the registry cross-check, both
  verified by form only; its execution proved
  the primary's field uncoded and the
  cross-check's column coded. This draft names
  the registry primary *because its values
  were read in full at draft* (§2) — the
  verification Spec 038's frame lacked — and
  demotes the CGSA file to a cross-check whose
  disagreements are expected in kind,
  published in full, and move nothing (§4,
  check 0.2). The anti-table-shopping purpose
  of DD-038-5 is preserved and strengthened:
  the sources are still named before
  execution, and the population is now listed
  before execution too.
- **DD-043-2 — DECIDED-BY-DRAFT: the
  re-derivation gate.** A population defined
  by a column must be able to account for the
  column. Step 0 re-derives all 803
  `icit_function` values from the pinned
  builder rule (`_WELLS_FUNCTIONS` over each
  row's own Wells IDs) and closes the study
  on any mismatch (§4, check 0.2). Verified at
  draft: exact agreement.
- **DD-043-3 — DECIDED-BY-DRAFT: the census
  is published at draft, and the census branch
  is foreclosed.** Spec 038 could not list its
  population (its source was unread by
  design); this frame's source is read, so the
  population is listed (§2) and step 0 checks
  the frozen files against the list. With two
  never-tested signs in the population, D-31's
  census branch cannot arise (§7).
- **DD-043-4 — DECIDED-BY-DRAFT: the
  provenance gate, its limbs, and its distinct
  closure name.** §3 states the threat; §4
  check 0.3 fixes the evidence set (D1–D4),
  the three limbs, the fail-closed outcomes,
  and the closure's name — **PROVENANCE —
  CANNOT BE RUN AS WRITTEN** — so a provenance
  failure is never filed as a source defect
  or read as a verdict. The gate binds the
  whole study on any single sign's failure;
  no subset verdict exists.
- **DD-043-5 — FLAGGED, not harmonised:
  P098's code.** The register's Tested note
  calls P098 "(LOG)"; the primary source gives
  P098 no code at all, and the characterisation's
  Cluster 10 line counts one LOG among its
  members P098 and P217 — that LOG is P217
  under the registry. This design relies only
  on what the pinned sources record: P098 is
  not ITM, and is excluded by the inclusion
  rule. The register's parenthetical stands as
  a pre-execution record; no reconciliation is
  appended for it under this spec (DD-038-2's
  note already covers the codes' provenance).
- **DD-043-6 — DECIDED-BY-DRAFT under the
  owner's successor order: this spec scores
  PRED-2026-007 itself; no new PRED number.**
  Spec 038's register entry (2026-10-20) says
  any future test of this hypothesis requires
  "a population frame whose coded values are
  verified in the named primary source itself
  before the design is frozen, registered as a
  new prediction under a new PRED number."
  This draft satisfies the sentence's
  operative requirement by construction — the
  frame's coded values *are* verified in the
  named primary source before any freeze (§2)
  — and, under the owner's direct order of
  2026-10-21 ("Do the successor"), takes the
  new-number clause as addressed to tests that
  would change the prediction: this successor
  changes no word of the prediction, its bar,
  or its population definition; it corrects
  which held file supplies the codes and adds
  the provenance gate. The freeze is asked to
  confirm this reading openly (§5 of
  `adjudication.md`); if it declines, the
  design retires unscored and a successor
  prediction may be registered instead.
- **DD-043-7 — CARRIED from Spec 038:
  DD-038-3 and DD-038-9.** The criterion's
  wording governs over the Prediction
  sentence's (the difference flagged, §0.1),
  with the operative reading that a sign counts
  iff its recorded cluster's recorded class is
  TERMINAL (§6); and the cluster-class rule is
  the recorded characterisation lookup (§4,
  check 0.4) — a disclosed operationalisation,
  deterministic, inventing no threshold.
- **DD-043-8 — CARRIED from Spec 038:
  DD-038-4's coverage rule**, adopted in
  substance (§7) and flagged as the design's,
  not the register's.
- **DD-043-9 — DECIDED-BY-DRAFT: no second
  provenance reconciliation.** DD-038-2's
  appended note stands as the register's
  provenance record; this spec's execution
  appends its outcome entry and gate finding
  only (§8).
- **DD-043-10 — OPEN for the freeze: the
  provenance gate's borderline standard.**
  The gate's mechanics are fixed (DD-043-4);
  what is open is the adjudication standard
  for documents whose basis statements are
  present but ambiguous — how explicit a
  stated basis must be to count as stated,
  and who adjudicates a borderline document.
  Draft recommendation: a basis counts as
  stated only if the produced document states
  it in words, with a locator, for the class
  or the sign; inference from a class's name,
  from glosses in the builder table, or from
  the classification's general reputation does
  not count; borderline calls are recorded in
  the step-0 record with the quoted text, so
  the determination is checkable. Silence is
  already fixed as failure (§3.3).
- **DD-043-11 — OPEN for the freeze: a
  spec-level OSF registration.** Specs 032–039
  each filed their own OSF contract
  registration at freeze; PRED-2026-007 itself
  predates that practice. Proposal to the
  freeze decision: file this frozen spec's own
  OSF contract registration, following the
  house pattern. This draft files nothing.
- **DD-043-12 — OPEN for the freeze: the LOG
  class's role.** Enumerated-only (this
  draft's design: the LOG census and trace
  are recorded; no LOG quantity is scored), or
  scored as a control class alongside the ITM
  verdict (its TERMINAL share computed and
  published as a descriptive contrast, under
  the same recorded-output rule, carrying no
  criterion and moving no verdict — with the
  provenance gate's LOG trace then gating the
  control under DD-043-10's standard). The
  freeze decides; the draft enumerates either
  way.
- **DD-043-13 — OPEN for the freeze: the
  execution phase number**, allocated at the
  freeze act against the phases then reserved
  (Phase-401 was Spec 038's; Specs 041/042
  likewise allocate at their freezes). Nothing
  in the design turns on the number.
- **DD-043-14 — The freeze gate.** This draft
  runs **no** AEE lifecycle hooks; at the
  freeze act the hooks (after_specify /
  after_plan / after_tasks) run as the gate
  under the programme's adopted aee pin
  (1.5.x), the gate reading of DD-038-10
  applying to this draft-stage register, and
  any freeze digest is computed over the
  recovered register exactly once, at freeze.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
