# Spec 093 Stage 2 — T202 find-context freeze v3 (2026-11-20)

Frozen before any computation under this freeze. This
record is the second successor freeze for **one field
only — find context** — under spec.md §5 and C093-8:
freeze v1's find-context administration was invalid
as frozen, because its control battery's
99th-percentile κ was 0.1322, at or above v1 §7's 0.10
validity ceiling (run `study-20261119T190257Z-cdc1e1`);
freeze v2 repaired the evaluation design (repeated
stratified 5-fold cross-validation, the repeat-mean
statistic) and its control battery's 99th-percentile
κ̄ was 0.1106, still at or above the same ceiling
(runs `study-20261119T202359Z-72b357` and
`study-20261119T202434Z-6d1f2a`; the successor record,
`records/stage2-findcontext-successor-record-2026-11-19.md`,
names the battery's values as the remaining
obstruction and identifies the control construction
as the remaining axis). The field took NOT YET under
both freezes — the machinery, not the channel, is
what failed. This freeze states what changes, what
does not, and the rule that maps its outcomes to find
context's standing. Nothing in §§1–10 may move after
this record is committed; a change is a superseding
freeze that voids every run under this one (C093-8).

**Authority.** This freeze is Item 5 of the
2026-11-20 delegated-decisions package, executed on
the owner's approval of git work in the
tower-compute clones given in the Glossa-Lab chat on
2026-11-20 at 19:51 ET. The package's decision of
record: change the CONTROL CONSTRUCTION, not the
validity rule.

**Scope.** This freeze supersedes
`records/t202-findcontext-freeze-v2.md` (SHA-256
`26444704e0a530ada78e9aebcae25df3dabdd4e0ad202524970ac05dcaac286b`)
for the find-context field alone; freeze v2 in turn
superseded `records/t202-freeze-v1.md` (SHA-256
`075b5124171db8ab04d657cd5a85842db93e0fef29cc1a7717a61fd4f4b644d2`)
for that field. Freeze v1's and v2's runs for find
context stand in the record as the obstruction's
evidence and are void for adjudication. Every other
field's v1 outcome stands untouched: site NOT
RECOVERED, material class / artifact type /
holding-provenance NOT ADMINISTERED. C093-1's standing
label from Stage 2 — INDEPENDENT IN PART — is not
reopened by this freeze; §8 restates only find
context's place in its per-field table.

## 1. Inputs and pins

Identical to freeze v1 §1 and freeze v2 §1:

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
- Stage 2 record (the v1 obstruction's record):
  `specs/093-material-context-channel/records/stage2-record-2026-11-19.md`,
  SHA-256
  `4d64bd2bebbb806878131a03f578bdeecc78600208691cffaf9936165bf94a8f`.

Added for this freeze, in the same pin structure —
the v2 obstruction's record chain:

- Freeze v2:
  `specs/093-material-context-channel/records/t202-findcontext-freeze-v2.md`,
  SHA-256
  `26444704e0a530ada78e9aebcae25df3dabdd4e0ad202524970ac05dcaac286b`.
- Stage 2 find-context successor record (the v2
  obstruction's record):
  `specs/093-material-context-channel/records/stage2-findcontext-successor-record-2026-11-19.md`,
  SHA-256
  `ff7c44ee5b147fdfb4769c458ad96fe42f79e92c8f9697f5a66077184d4fddd8`.
- Freeze v2 adjudication:
  `specs/093-material-context-channel/records/t202-findcontext-adjudication-v2-2026-11-19.json`,
  SHA-256
  `39bdc39549096cdc2b1513375150478dfde584558d915f9616ce9cf6896355e3`.
- Freeze v2 audit:
  `specs/093-material-context-channel/records/t202-findcontext-audit-v2-2026-11-19.json`,
  SHA-256
  `1121757f858ac7b665895bbba608858e669b00e0bc315c009ac115ef6bd18b49`.

The successor-record pin above is the one pin the
preparation draft of this freeze left open; it was
completed before this freeze was committed by
computing the SHA-256 of the successor record as it
stands in the current tree at the origin/main tip
this freeze branches from (merge of PR #621,
`ad4536ae`), and it reproduces from that file
directly. Every other pin above was likewise
recomputed from the current tree before this freeze
was committed and reproduces the value v1/v2 froze;
had any failed to reproduce, no freeze would have
been committed.

The runner verifies the two data pins against constants
it carries and refuses (an absence run record, kind
`refused`) on any mismatch; the definition, counts,
Stage 2 record, freeze v2, successor record, and v2
adjudication and audit hashes are carried into every
run record's pins.

## 2. Population and floors (unchanged from v1 §§2–3, as restated in v2 §2)

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

**Population nuance, stated plainly.** Every one of
the 179 joined pairs carries the pair's `site` value
Mohenjo-daro — the field's values are excavation
areas within that one site — and all 175
administration-population records and all 125 adjudged
records sit at that one site. §6's within-site
stratification therefore realizes a **single stratum**
on this population. This freeze states that rather
than pretending a multi-stratum design exists where
the record carries one site; the construction is
registered in its general form so the rule, not the
realization, is what is frozen, and §6's closing
condition is written knowing the realization.

## 3. Features (unchanged from v1 §4, as restated in v2 §3)

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

## 4. Predictor (unchanged from v1 §5, as restated in v2 §4)

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

## 5. Evaluation design (unchanged from v2 §5)

**Design.** Stratified 5-fold cross-validation,
repeated R = 10 times.

- For repeat r (r = 0, …, 9): one stream
  `random.Random(20261123 + r)` — this freeze's streams,
  replacing v2's `20261121 + r`. For each adjudged
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

## 6. Controls (the change): identical statistic, within-site stratified permutation, 2,000-draw ensemble

### Methodological justification, registered before any computation under this freeze

A permutation null must be generated under the same
statistic and the same exchangeability structure as
the test statistic it calibrates. That is the
standing doctrine of permutation testing from its
foundations (Fisher 1935; Pitman 1937) through its
modern statements (Edgington & Onghena 2007; Phipson
& Smyth 2010; Hemerik & Goeman 2018): the permuted
data sets must be exchangeable with the observed data
under the null, and the quantity whose null
distribution is estimated must be the very quantity
adjudged on the observed data, computed by the very
procedure that computed it — otherwise the battery
calibrates a different instrument than the one under
test, and its tail is evidence about that other
instrument. Freeze v1 breached this in form (a
single-draw held-out κ null against a single-draw
administration happened to match, but at a resolution
its own noise saturated); freeze v2 repaired the
administration's statistic to a repeat-mean and
described its controls as repeat-mean in kind, but
left the registration inexact on two points this
freeze makes exact: the permutation in v2 was drawn
**globally** over the adjudged records, not under the
population's own stratification, and the battery's
ensemble was 200 draws, at which size the
99th-percentile estimate itself carries material
Monte Carlo error (the p99 slot is the 198th of 200
ordered values — a single draw's movement moves the
estimate). On sparse categorical fields with one
dominant class, both defects inflate or destabilize
exactly the tail the validity ceiling reads.

This freeze is therefore an **instrument repair, not
ceiling-shopping**, and states why in its own terms:
the ceiling (0.10), the bar (κ̄ ≥ 0.80, BĀ ≥ 0.85),
every floor, and the population are **unmoved** from
v1/v2 (§§2, 7, 10); nothing this freeze changes makes
the administration's own statistic easier to pass,
because the administration (§5) is v2's, unchanged in
construction. What changes is only that the null is
now generated by the registered procedure the
doctrine requires — the identical statistic, under
the population's exchangeability structure, at an
ensemble size where the tail estimate is stable — so
that if the battery still breaches the unmoved
ceiling, the breach is a property of the population
and the field, recorded as such under §8's closing
condition, and not another artefact of a mismatched
instrument. A freeze that moved the ceiling instead
would be converting a stop into a pass (C093-8); this
one does the opposite: it removes the last registered
reason to distrust the stop.

**Construction.** 2,000 permutations. One stream
`random.Random(20261124)` — this freeze's control
stream, replacing v2's `20261122`. For each
permutation in order:

- Partition the adjudged records by the joined pair's
  `site` value (the stratification). Sites are taken
  in ascending order. On this population the partition
  realizes a single stratum, Mohenjo-daro, holding all
  125 adjudged records (§2's nuance, stated there and
  relied on here — the construction is not described
  as multi-stratum anywhere in this freeze).
- Within each stratum, take the stratum's records'
  labels as a list in record-id-sorted order, shuffle
  the list with the continuing stream, and assign the
  permuted labels to the stratum's records (ids
  ascending). Permutation never crosses a stratum
  boundary, so each stratum's label marginals are
  preserved exactly (matched marginals), as are the
  global marginals.
- Run §5 identically on the relabeled records — fresh
  per-repeat streams `random.Random(20261123 + r)`,
  folds formed by the permuted labels, the §4
  predictor, exact rational metrics — and compute that
  permutation's κ̄ (the mean of its 10 per-repeat κ
  values). No single-draw statistic enters the battery
  anywhere: every control value is a repeat-mean
  computed by the administration's own procedure.

The battery reports the maximum, the mean, and the
99th percentile (the value at index 1979 of the 2,000
κ̄ values sorted ascending) of the 2,000 control κ̄
values, and the count of values at or above 0.10.

**Control validity:** the administration is valid only
if the battery's 99th-percentile κ̄ < 0.10 — v1 §7's
ceiling, carried through v2 §6, unchanged. If it is
not, the field's outcome under this freeze is NOT
YET, with the battery's values named as the
obstruction, and no re-administration under this
freeze repairs it.

## 7. Metrics and the bar (unchanged from v1 §8, as restated in v2 §7)

**Bar.** The field is **RECOVERED** iff κ̄ ≥ 0.80
**and** BĀ ≥ 0.85. Otherwise, given valid controls,
the field is **NOT RECOVERED**. The bar and its ground
are v1 §8's, restated: C093-1's falsifier names a
predictor that *recovers* the field at near-identity
strength; a merely associated field, recovered at κ of
0.2–0.5, does not meet the falsifier, and this freeze
does not let it.

## 8. The standing rule for this field, and the closing condition

- **RECOVERED** → find context falls: C093-1 falls for
  this field, and the successor record names it among
  the fallen fields.
- **NOT RECOVERED** (valid controls) → find context
  survives: it joins site in C093-1's surviving set,
  and downstream claims may cite it as channel data at
  exactly that strength.
- **NOT YET** (controls invalid under §6) → v1's and
  v2's NOT YET stands for this field; this freeze's
  runs are void for adjudication and the obstruction
  is named in the successor record.

**Closing condition (registered with this freeze,
before computation).** This is the third and final
freeze of the find-context line. If the v3 battery
still breaches the §6 ceiling, find context stays
**NOT YET** and the line **closes at three freezes
absent new data**: no fourth freeze may be written on
this population and these inputs; the line reopens
only on new data (a materially enlarged or revised
join population), recorded as such when it arrives.
If the v3 administration is valid, its §7 outcome —
RECOVERED or NOT RECOVERED — is the field's standing
and likewise closes the freeze line: no further
freeze re-adjudges this field on these inputs.

Under every outcome the overall label remains
**INDEPENDENT IN PART** (site survives from v1;
material class, artifact type, and
holding/provenance carry no standing), and the
successor record restates the full per-field table so
no downstream statement need guess which fields carry
standing. The one exception the mapping itself
carries: if find context is NOT RECOVERED under valid
controls, it joins the surviving set named in that
table, and the overall label still remains
INDEPENDENT IN PART, because the three
NOT ADMINISTERED fields carry no standing either way.

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
count, stream, statistic, stratification, and validity
ceiling (§6), the bar (§7), and the standing mapping
and closing condition (§8). Any change is a new
freeze — and under §8's closing condition, on these
inputs there is no new freeze — and runs under this
one are void.

## References for §6

- Fisher, R. A. (1935). *The Design of Experiments.*
  Oliver & Boyd.
- Pitman, E. J. G. (1937). Significance tests which
  may be applied to samples from any populations.
  *Supplement to the Journal of the Royal Statistical
  Society*, 4(2), 238–244.
- Edgington, E. S., & Onghena, P. (2007).
  *Randomization Tests* (4th ed.). Chapman & Hall/CRC.
- Phipson, B., & Smyth, G. K. (2010). Permutation
  p-values should never be zero: calculating exact
  p-values when permutations are randomly drawn.
  *Statistical Applications in Genetics and Molecular
  Biology*, 9(1), Article 39.
- Hemerik, J., & Goeman, J. J. (2018). False discovery
  proportion estimation by permutations: confidence
  and significance. *Biometrika*, 105(4), 1003–1012.

*This does not establish:* that the surviving fields
say anything about any reading — independence is about
projections, and §5's vocabulary is the whole of what
this task may conclude. (T202's line, carried
verbatim.)
