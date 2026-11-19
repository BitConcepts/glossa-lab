# Spec 093 Stage 2 — T202 find-context successor freeze v2 (2026-11-19)

Frozen before any computation under this freeze. This
record is the successor freeze for **one field only —
find context** — under spec.md §5 and C093-8: freeze
v1's find-context administration was invalid as frozen,
because its control battery's 99th-percentile κ was
0.1322, at or above v1 §7's 0.10 validity ceiling (run
`study-20261119T190257Z-cdc1e1`; the Stage 2 record,
`records/stage2-record-2026-11-19.md` §T202, names the
battery's values as the obstruction). The field took
NOT YET — the machinery, not the channel, is what
failed. This freeze states what changes, what does not,
and the rule that maps its outcomes to find context's
standing. Nothing in §§1–9 may move after this record
is committed; a change is a superseding freeze that
voids every run under this one (C093-8).

**Scope.** This freeze supersedes
`records/t202-freeze-v1.md` (SHA-256
`075b5124171db8ab04d657cd5a85842db93e0fef29cc1a7717a61fd4f4b644d2`)
for the find-context field alone. Freeze v1's runs for
find context stand in the record as the obstruction's
evidence and are void for adjudication. Every other
field's v1 outcome stands untouched: site NOT
RECOVERED, material class / artifact type /
holding-provenance NOT ADMINISTERED. C093-1's standing
label from Stage 2 — INDEPENDENT IN PART — is not
reopened by this freeze; §8 restates only find
context's place in its per-field table.

## 1. Inputs and pins

Identical to freeze v1 §1:

- Corpus snapshot:
  `glossa-corpus/indus/exports/indus_research.jsonl`,
  SHA-256
  `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`.
- Join output (Stage 1, T103):
  `specs/093-material-context-channel/records/t103-join-pairs-v1.jsonl`,
  SHA-256
  `7107f738832a4e3b04cff91d81073212bc0f3a77afed6f0ccc3cee4fce621703`.
- Channel definition (T201):
  `specs/093-material-context-channel/records/t201-channel-definition-2026-11-19.md`,
  SHA-256
  `deaa5a71f26ac5eb7e2e089767388458dbaf922fe974f59bfcaa762186bdb641`.
- Grounding counts (T201):
  `specs/093-material-context-channel/records/t201-counts-2026-11-19.json`,
  SHA-256
  `15e2cef667872868a4ba3145677aecc7b818dcbf8cf3ccc13a9d6aff532df3b8`.
- Stage 2 record (the obstruction's record):
  `specs/093-material-context-channel/records/stage2-record-2026-11-19.md`,
  SHA-256
  `4d64bd2bebbb806878131a03f578bdeecc78600208691cffaf9936165bf94a8f`.

The runner verifies the two data pins against constants
it carries and refuses (an absence run record, kind
`refused`) on any mismatch; the definition, counts, and
Stage 2 record hashes are carried into every run
record's pins.

## 2. Population and floors (unchanged from v1 §§2–3)

The field is find context as T201 §2.5 defines it: the
snapshot text record's identity joined to its pair's
`area_section`; the sequence and bookkeeping are the
text record's. The administration population is P-join
restricted to pairs with a non-empty `area_section`:
**175 records**.

The floors are v1's, applied mechanically, unchanged:

- **Class floor 10** — a class is adjudged only if it
  carries at least 10 records.
- **Formation floor** — at least 2 adjudged classes and
  at least 50 adjudged records.

Applied: the field **FORMS**. Adjudged classes:
DKG. (S) 68, DKG. (N) 17, DK- 16, HRB 13, VSA 11 —
**125 adjudged records**. Not adjudged, named: DKC 9,
DKB 7, HR- 7, DKE 6, DKG 6, SD- 5, HRA 5, DKD 1,
DKH 1, L- 1, SDBath Cells 1, VS- 1 (50 records,
excluded from training and adjudication alike).

## 3. Features (unchanged from v1 §4)

Each adjudged record yields events of exactly these
kinds, computed from the record alone:

- one `tok` event per sequence token, valued by the
  token's recorded code string (`canonical_grapheme_ids`,
  as recorded, in order, with multiplicity);
- one `first` event valued by the first token's code;
- one `last` event valued by the last token's code;
- one `len` event valued by the sequence length as a
  decimal string;
- one `distinct` event valued by the count of distinct
  codes as a decimal string;
- one `bk` event per bookkeeping field of T201 §4,
  valued by the field's recorded value as a string
  (`source_system`, `sign_id_scheme`, `rights_status`,
  `crosswalk_coverage`).

No culture-side value enters any feature. The event
vocabulary for a fit is the set of events occurring in
that fit's training records; an event outside it at
prediction time is ignored.

## 4. Predictor (unchanged from v1 §5)

Multinomial Naive Bayes over §3's events. For class c:
prior P(c) = (training records in c) / (training
records). For event e: P(e|c) = (count of e in c's
training records + α) / (total events in c's training
records + α · |V|), with α = 1.0 and V the fit's §3
vocabulary. A record's score for c is log P(c) +
Σ log P(e|c) over its events with multiplicity; the
prediction is the highest score, ties broken by
ascending class label. The predictor is fitted on each
fold's training records only (§5). The majority-class
rule's metrics are computed and reported for scale;
they are not a verdict input.

## 5. Evaluation design (the change): repeated stratified cross-validation

Freeze v1 §6 adjudged the field on **one** stratified
70/30 split: 35 held-out records. Its control battery
(§6 below, v1 §7's design) returned a null κ
distribution whose spread — max 0.1351, 99th percentile
0.1322, mean −0.0077 over 200 permutations — is wider
than the 0.10 validity ceiling at that held-out size:
at n = 35 with five classes, a handful of chance
agreements moves κ by more than the ceiling allows.
That is a resolution limit of the machinery, named as
the obstruction in the Stage 2 record. This freeze
repairs the resolution, and nothing else: the
statistic adjudged is now computed over the full
adjudged population, repeatedly, instead of over one
35-record draw.

**Design.** Stratified 5-fold cross-validation,
repeated R = 10 times.

- For repeat r (r = 0, …, 9): one stream
  `random.Random(20261121 + r)`. For each adjudged
  class in ascending label order, take its record ids
  sorted ascending, shuffle them with the continuing
  stream, and assign fold f (f = 0, …, 4) the ids at
  positions f, f+5, f+10, … of the shuffled list.
  Every class therefore places ⌈n/5⌉ or ⌊n/5⌋ records
  in each fold; the smallest adjudged class (VSA, 11)
  places at least 2 records in every fold and keeps at
  least 8 in every fold's training set.
- For fold f: the held-out set is the union over
  classes of the fold-f ids; the training set is the
  remaining records. Fit §4 on the training set and
  predict every held-out record. Each adjudged record
  is predicted exactly once per repeat, always by a
  fit that did not train on it.
- Per repeat, pool the five folds' predictions into
  one confusion matrix over all 125 adjudged records
  and compute accuracy, per-class recall, balanced
  accuracy, and Cohen's κ from it, in exact rational
  arithmetic (the v1 tools' repair, carried).
- **The administration statistics** are κ̄, the mean
  of the 10 per-repeat κ values, and BĀ, the mean of
  the 10 per-repeat balanced accuracies — exact
  rational means, emitted as floats. The per-repeat
  values, the pooled confusion matrix (summed over
  repeats), and the majority-class rule's repeat-mean
  metrics are reported alongside, for scale and audit.

**Replication requirement** (spec.md §5): the 10
repeats are this administration's replication — the
same frozen predictor adjudged on 10 independent
stratified partitions of the full population. No
held-out-site arm exists for this field: every
adjudged record is Mohenjo-daro (the field is an
excavation area within that one site), so no external
replication arm can be named, and none is pretended.

## 6. Controls (design unchanged in kind; statistic repaired with §5)

200 permutations. One stream `random.Random(20261122)`;
for each permutation in order, take the adjudged
records' labels as a list in record-id-sorted order,
shuffle the list with the continuing stream, assign
the permuted labels to the records (ids ascending),
then run §5 identically — fresh per-repeat streams
`random.Random(20261121 + r)`, folds formed by the
permuted labels — and compute that permutation's κ̄
(the mean of its 10 per-repeat κ values). The battery
reports the maximum, the mean, and the 99th percentile
(the value at index 197 of the 200 κ̄ values sorted
ascending).

**Control validity:** the administration is valid only
if the battery's 99th-percentile κ̄ < 0.10 — v1 §7's
ceiling, unchanged. If it is not, the field's outcome
under this freeze is NOT YET, with the battery's
values named as the obstruction, and no
re-administration under this freeze repairs it.

The ceiling is deliberately **not** moved. What §5
changes is the statistic the ceiling adjudges: a mean
over 10 full-population adjudications has a null
spread set by n = 125 repeated, not by one n = 35
draw, so the same 0.10 ceiling is now a test the
machinery can meaningfully pass or fail, instead of
one its own noise saturates.

## 7. Metrics and the bar (unchanged from v1 §8)

**Bar.** The field is **RECOVERED** iff κ̄ ≥ 0.80
**and** BĀ ≥ 0.85. Otherwise, given valid controls,
the field is **NOT RECOVERED**. The bar and its ground
are v1 §8's, restated: C093-1's falsifier names a
predictor that *recovers* the field at near-identity
strength; a merely associated field, recovered at κ of
0.2–0.5, does not meet the falsifier, and this freeze
does not let it.

## 8. The standing rule for this field

- **RECOVERED** → find context falls: C093-1 falls for
  this field, and the successor record names it among
  the fallen fields.
- **NOT RECOVERED** (valid controls) → find context
  survives: it joins site in C093-1's surviving set,
  and downstream claims may cite it as channel data at
  exactly that strength.
- **NOT YET** (controls invalid under §6) → v1's
  NOT YET stands for this field; this freeze's runs
  are void for adjudication and the obstruction is
  named in the successor record.

Under every outcome the overall label remains
**INDEPENDENT IN PART** (site survives from v1;
material class, artifact type, and
holding/provenance carry no standing), and the
successor record restates the full per-field table so
no downstream statement need guess which fields carry
standing.

## 9. Run discipline

The administration and the control battery are each a
Spec 089 run on the `study` surface (run-defs v2),
written through the registered library writer into
this spec's records directory. A refusal this freeze
names (a pin mismatch, a frozen count not reproducing)
writes an absence record (kind `refused`) under the
minted id. An independent auditor who did not compute
recomputes both executions from the pinned inputs
under this freeze, in a second implementation sharing
no code with the runner, and compares result blocks;
the checker adjudges the audited outcome against §6's
validity rule, §7's bar, and §8's mapping mechanically,
and refuses to adjudge on an audit verdict other than
AGREE. All verdict-bearing metrics are computed in
exact rational arithmetic and emitted as floats, so
two correct implementations agree bit-for-bit.

## 10. What may not move

The pins (§1), the population and class lists (§2),
the floors (§2), the feature construction (§3), the
predictor and its constants (§4), the evaluation
design, repeat count, and seeds (§5), the control
count, stream, statistic, and validity ceiling (§6),
the bar (§7), and the standing mapping (§8). Any
change is a new freeze, and runs under this one are
void.

*This does not establish:* that the surviving fields
say anything about any reading — independence is about
projections, and §5's vocabulary is the whole of what
this task may conclude. (T202's line, carried
verbatim.)
