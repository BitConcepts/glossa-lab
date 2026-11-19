# Spec 093 Stage 2 — T202 freeze v1 (2026-11-19)

Frozen before any Stage 2 computation. This record
states the fields, the populations, the features, the
predictor, the split, the controls, the floors, and the
bars of the channel-independence administration, and the
rule that maps its outcomes to C093-1's standing in
spec.md §5's vocabulary. Nothing in §§2–9 may move after
this record is committed; a change is a superseding
freeze that voids every run under this one (C093-8).

## 1. Inputs and pins

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

The runner verifies the two data pins against constants
it carries and refuses (an absence run record, kind
`refused`) on any mismatch; the definition and counts
hashes are carried into every run record's pins.

## 2. Fields and administration populations

Fields are the five of D-093-2, as T201 §2 defines them.
A field's **administration population** is its T201
population restricted to records carrying a non-empty
field value (the census empty convention, T201 §2):

- **Site** — P-site: 966 records (snapshot records with
  a non-empty `canonical_grapheme_ids` and a non-empty
  `site_name`).
- **Material class** — P-join restricted to pairs with a
  non-empty `material_raw`: 178 records.
- **Artifact type** — P-seq (3,085 records, all carrying
  the field) and, concurring, P-join (179).
- **Holding/provenance** — no population: sequence ∧
  holding copresence in the snapshot is 0, and the join
  pairs carry no holding on either side.
- **Find context** — P-join restricted to pairs with a
  non-empty `area_section`: 175 records. The field's
  value is the snapshot text record's identity joined to
  the pair's `area_section`; the sequence and
  bookkeeping are the text record's.

## 3. Floors, and their mechanical application

Two floors, applied mechanically to every field before
any computation:

- **Class floor 10.** A field value (class) is adjudged
  only if it carries at least 10 records in the field's
  administration population — the smallest class that
  places at least 3 records in the held-out set under
  §6's split rule.
- **Formation floor.** A field's administration forms
  only if at least 2 classes are adjudged and the
  adjudged records number at least 50.

Applied to §2's counts, the floors decide, before any
computation:

- **Site: FORMS.** Adjudged classes: Mohenjo-daro 839,
  Harappa 110 — 949 adjudged records. Not adjudged,
  named: Chanhu-Daro 7, Sutkagen-Dor 6, Lothal 3,
  Kalibangan 1 (17 records, excluded from training and
  adjudication alike).
- **Find context: FORMS.** Adjudged classes: DKG. (S)
  68, DKG. (N) 17, DK- 16, HRB 13, VSA 11 — 125 adjudged
  records. Not adjudged, named: DKC 9, DKB 7, HR- 7,
  DKE 6, DKG 6, SD- 5, HRA 5, DKD 1, DKH 1, L- 1,
  SDBath Cells 1, VS- 1 (50 records).
- **Material class: DOES NOT FORM.** Adjudged classes:
  Steatite alone (176); Clay 1 and Faience 1 fall under
  the class floor. One adjudged class fails the
  formation floor. Outcome: NOT ADMINISTERED, forcing
  counts 176 / 1 / 1 (and 1 empty of 179).
- **Artifact type: DOES NOT FORM.** The field takes one
  distinct value ('seal') on all 3,085 sequence-bearing
  records and one concurring value on the join: zero
  variance on every population that carries a sequence.
  One class fails the formation floor, and no per-object
  recovery question exists to administer. Outcome: NOT
  ADMINISTERED, forcing counts 3,085 records / 1
  distinct value.
- **Holding/provenance: DOES NOT FORM.** No
  administration population exists. Outcome: NOT
  ADMINISTERED, forcing count: sequence ∧ holding
  copresence 0.

A NOT ADMINISTERED outcome is a finding about the record
system's present contents (C093-8), recorded with its
forcing counts; it is not repaired by moving a floor.

## 4. Features (frozen construction)

For an administered field, each adjudged record yields
events of exactly these kinds, computed from the record
alone:

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
vocabulary is the set of events occurring in the
training records; an event outside it at prediction time
is ignored (stated here so the rule is the freeze's, not
the implementer's).

## 5. Predictor (frozen)

Multinomial Naive Bayes over §4's events. For class c:
prior P(c) = (training records in c) / (training
records). For event e: P(e|c) = (count of e in c's
training records + α) / (total events in c's training
records + α · |V|), with α = 1.0 and V the §4 vocabulary.
A record's score for c is log P(c) + Σ log P(e|c) over
its events with multiplicity; the prediction is the
highest score, ties broken by ascending class label.
The predictor is fitted on the training records only.
The majority-class rule's held-out metrics are computed
and reported for scale; they are not a verdict input.

## 6. Split (frozen)

Per administered field: for each adjudged class in
ascending label order, take its record ids sorted
ascending, shuffle them with one stream of
`random.Random(20261119)` consumed class by class in
that order, and assign the first max(1, int(0.3 · n))
ids to the held-out set, the rest to training. (Site:
held-out 284 — Mohenjo-daro 251, Harappa 33; find
context: held-out 35 — DKG. (S) 20, DKG. (N) 5, DK- 4,
HRB 3, VSA 3. The
runner states the realized counts in its result block,
and the auditor recomputes them from this rule.)

## 7. Controls (frozen)

Per administered field: 200 permutations. One stream of
`random.Random(20261120)`; for each permutation in
order, take the administration population's labels as a
list in record-id-sorted order, shuffle the list with
the continuing stream, assign the permuted labels to the
records (ids ascending), then run §§4–6 identically
(fresh split stream per §6) and compute held-out Cohen's
κ. The battery reports the maximum, the mean, and the
99th percentile (the value at index 197 of the 200
values sorted ascending).

**Control validity:** the administration is valid only
if the battery's 99th percentile κ < 0.10. If it is
not, the field's outcome is NOT YET — the machinery, not
the channel, is what failed — with the battery's values
named as the obstruction (C093-6's pattern).

## 8. Metrics and the bar (frozen)

On the held-out set, for the real labels: accuracy,
per-class recall, balanced accuracy (the mean of the
per-class recalls over the adjudged classes), and
Cohen's κ, all computed from the held-out confusion
matrix.

**Bar.** A field is **RECOVERED** iff held-out κ ≥ 0.80
**and** held-out balanced accuracy ≥ 0.85. Otherwise,
the field is **NOT RECOVERED**. The bar's ground, stated
as the freeze's own reasoning: C093-1's falsifier names
a predictor that *recovers* the field — the field shown
to be the same information re-expressed — and recovery
at near-identity strength is what κ ≥ 0.80 (agreement
beyond chance at the conventional floor of "almost
perfect") together with balanced accuracy ≥ 0.85
(which a majority-class rule cannot approach: it scores
κ = 0 and balanced accuracy 1/k) states mechanically.
A merely associated field, recovered at κ of 0.2–0.5,
does not meet the falsifier, and this freeze does not
let it. The program's own identity-precision precedent
(T103's 0.90 floor) sits in the same region.

## 9. The standing rule (frozen mapping to spec.md §5)

Per-field outcomes are RECOVERED, NOT RECOVERED, NOT
ADMINISTERED (§3), or NOT YET (§7). Let R be the
recovered fields, S the not-recovered fields, U the not
administered and NOT YET fields, each named. C093-1's
standing is then:

- R empty, U empty → **INDEPENDENT AT FULL STRENGTH**.
- R empty, U non-empty → **INDEPENDENT IN PART**: the
  channel stands independent for the fields in S
  (named); the fields in U carry no standing either way
  and may not be cited downstream as channel data
  (FR-093-04's conservative direction).
- R non-empty, S non-empty → **INDEPENDENT IN PART**:
  the fields in R have fallen (named); the fields in S
  survive.
- R non-empty, S empty, U non-empty → **INDEPENDENT IN
  PART**, with every administered field fallen.
- R non-empty, S empty, U empty → **NOT INDEPENDENT**.

## 10. Run discipline

Each administered field's administration and each
field's control battery is a Spec 089 run on the
`study` surface (run-defs v2), written through the
registered library writer into this spec's records
directory, the administration's store of record. A
refusal the freeze names (a pin mismatch, a frozen count
not reproducing) writes an absence record (kind
`refused`) under the minted id. An independent auditor
who did not compute recomputes each administration from
the pinned inputs under this freeze and compares result
blocks; the checker adjudges the audited outcomes
against §8's bar and §9's rule mechanically.

## 11. What may not move

The pins (§1), the populations and class lists (§§2–3),
the feature construction (§4), the predictor and its
constants (§5), the split and control streams (§§6–7),
the bar (§8), and the standing rule (§9). Any change is
a new freeze, and runs under this one are void.

*This does not establish:* that the surviving fields say
anything about any reading — independence is about
projections, and §5's vocabulary is the whole of what
this task may conclude. (T202's line, carried verbatim.)
