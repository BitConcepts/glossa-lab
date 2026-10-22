# PRED-2026-011 — OSF Registration Payload

> ## FILED — 2026-10-20 — REGISTRATION `t6whq`
>
> Draft prepared 2026-10-20 and filed the same day
> under Tristen Pierson's registration order. The
> text below is the payload as filed from the
> Predictions & Registrations node `nrb9u`. The
> registration is approved and public:
> https://osf.io/t6whq/, DOI 10.17605/OSF.IO/T6WHQ.

## Filing metadata

- **Title (as filed):** PRED-2026-011 — Cross-Site Class
  Preservation (Clean Withholding, Disclosed
  Mappability Screen): Successor Registration to
  PRED-2026-010
- **Filing node:** Predictions & Registrations,
  https://osf.io/nrb9u/ (id `nrb9u`)
- **Schema:** OSF Preregistration
  (`697b72f611a8e98484c6139b`)
- **Subjects:** Computational Linguistics; Social and
  Behavioral Sciences; Anthropology; Linguistics;
  Archaeological Anthropology
- **Registration status of this payload:** FILED
  2026-10-20 (registration `t6whq`, approved and
  public; DOI 10.17605/OSF.IO/T6WHQ)

## Study description

This study tests a narrow positional prediction about
the Indus script. A recorded classification method is
applied only to CISI Mohenjo-daro inscriptions. Signs
that the method classifies as INITIAL are then
screened, before registration, to ensure that each
one has a best-match counterpart in a frozen public
crosswalk to the Yajnadevam sign inventory. The study
asks whether both screened INITIAL signs also tend to
stand at the start of Harappa inscription sequences
in the pinned Yajnadevam dataset.

The design succeeds PRED-2026-010. That predecessor
used the same clean training pool and produced three
INITIAL signs, but one of them, P000, has no
best-match counterpart in the crosswalk. Its absence
would make 33% of the predecessor's trained set
unmappable, above its registered 20% cap. This
successor discloses the mappability screen in
advance and uses the resulting two-sign set:
**P217 and P324**.

This is a deliberately weak, small test. With two
signs, the success bar can pass only if both signs
pass. A positive result would be limited to those
two signs and this dataset. It would not validate
the INITIAL class in general.

## Hypotheses

### Primary hypothesis

At least 70% of the trained INITIAL signs — P217 and
P324 — will have a Harappa start rate of at least
0.40 in the pinned Yajnadevam data.

Because there are only two trained signs, the
possible shares are 0%, 50%, and 100%. The hypothesis
is therefore supported under the registered
criterion only at **2 of 2**.

### Outcome language

- **CONFIRMED:** both P217 and P324 have Harappa
  start rates at or above 0.40.
- **NOT CONFIRMED:** one or both signs have Harappa
  start rates below 0.40, including a mappable sign
  with zero Harappa occurrences.
- **CANNOT BE RUN AS WRITTEN:** a pre-scoring check
  fails because an input hash differs, the training
  derivation or mappability screen does not
  reproduce, or a trained sign is unmappable under
  the pinned crosswalk. This is a closure, not a
  verdict.

## Design plan

### Study type

Observational analysis of existing inscription
datasets. There is no intervention, treatment,
experimental manipulation, or new data collection.

### Blinding

There is no analyst blinding, and none is claimed.
The relevant protection is verified training-pool
exclusion: the classification is derived from CISI
Mohenjo-daro rows only, and the derivation is
recomputed and checked against fixed hashes before
scoring.

The Yajnadevam Harappa pool was previously inspected
in aggregate during the closure audit for
PRED-2026-006 / Spec 032. Those aggregate counts are
published in that record. No Harappa start rate has
been computed for P217 or P324.

### Design

The design has four fixed stages:

1. Recompute the classification from the CISI
   Mohenjo-daro pool only.
2. Confirm that the unscreened INITIAL set is P000,
   P217, and P324.
3. Apply the disclosed crosswalk screen: retain an
   INITIAL sign only if a frozen crosswalk row names
   it as `best_parpola_match`.
4. If the prediction is later taken to scoring under
   a separate order, compute start rates only for
   the retained signs, P217 and P324, in Harappa
   rows of the pinned Yajnadevam file.

No pool widening, sign substitution, crosswalk
substitution, or threshold change is permitted.

## Sampling plan

### Existing data

All data already exist. This registration is made
before any scoring of PRED-2026-011 and before any
Harappa start rate is computed for its trained signs.

The design-stage mappability screen used only the
public crosswalk. It did not use Harappa inscription
rows, sequences, occurrence counts, or start rates.

### Training data

- File: `data/normalized/corpus_master.csv`
- SHA-256:
  `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`
- Filter: `source_name` equals "Corpus of Indus
  Seals and Inscriptions (mayig digitization)"
- Filtered pool: 179 inscriptions, all
  Mohenjo-daro, zero Yajnadevam rows
- Filtered-pool manifest SHA-256:
  `ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a`
- Classifiable signs: 28
- Class counts: INITIAL 3, MEDIAL 19, MIXED 3,
  TERMINAL 3

### Crosswalk

- File:
  `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`
- SHA-256:
  `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`
- Counterpart rule: a Yajnadevam glyph is a
  counterpart for a trained sign only when its
  crosswalk row names that sign as
  `best_parpola_match`.
- P217 counterpart: Y0520 (confidence 1.0,
  confirmed).
- P324 counterpart: Y0740 (confidence 0.9867,
  confirmed).
- P000 has no best-match counterpart and is
  therefore excluded before registration. It appears
  only in `top3_parpola` alternatives, which do not
  establish a counterpart.

### Scoring data

- File:
  `backend/glossa_lab/data/yajnadevam_inscriptions.csv`
- SHA-256:
  `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`
- Scoring subset: all Harappa-site rows in that
  pinned file. The file's recorded census for the
  byte-identical data is 5,679 inscriptions across
  77 sites, including 2,717 Harappa inscriptions.
- The file is byte-hashed for this registration
  design. Its Harappa content is not scored until a
  separate scoring act.

### Sample-size rationale

The sample is fixed by the clean training pool and
the disclosed screen. The pool was not widened to
increase the number of trained signs. Widening the
pool was the defect that invalidated the withholding
behind PRED-2026-006.

The resulting two-sign denominator is a limitation,
not a target. It is accepted because changing the
pool or the mapping after seeing the mappability
problem would create a different, less honest test.

### Stopping rule

A future scoring run uses the complete Harappa
subset of the pinned file. It does not sample, stop
early, add rows, or substitute another dataset. A
failed integrity or mappability check stops the run
as CANNOT BE RUN AS WRITTEN.

## Variables

### Manipulated variables

None.

### Measured variables

For each trained sign:

- total Harappa occurrences, counted through its
  frozen best-match counterpart glyphs;
- Harappa occurrences in initial position, meaning
  the counterpart glyph is the first sign in the
  inscription sequence;
- start rate, defined as initial-position
  occurrences divided by total Harappa occurrences.

### Index

The primary index is the share of trained signs
whose start rate is at least 0.40:

```text
(number of trained signs with start_rate >= 0.40) / 2
```

The possible values are 0, 0.5, and 1.

## Analysis plan

### Computation

For each trained sign, count every occurrence of its
counterpart glyphs in Harappa sequences in the
pinned Yajnadevam file. Count an occurrence as
initial when the glyph is the first token in its
sequence. A one-sign sequence therefore counts its
only sign as initial.

Compute:

```text
start_rate = initial_occurrences / total_occurrences
share_passing = signs_with_start_rate_at_least_0.40 / 2
```

No statistical model, p-value, confidence interval,
or composition adjustment is part of the criterion.

### Inference criteria

- The prediction is CONFIRMED only if the share is
  at least 0.70. With two signs, that means 2 of 2.
- The prediction is NOT CONFIRMED if the share is
  0 or 0.5.
- A descriptive per-sign table will be reported with
  the outcome. It carries no separate criterion.

### Data exclusion and missing-data rules

- A trained sign with no best-match counterpart
  under the pinned crosswalk is unmappable. One
  unmappable sign is 50% of the trained set, above
  the 20% cap, so the run closes as CANNOT BE RUN
  AS WRITTEN.
- A mappable trained sign with zero Harappa
  occurrences has no start rate at or above 0.40. It
  counts as not meeting the bar and remains in the
  denominator.
- No trained sign may be removed after counting
  begins.
- No alternative crosswalk, manual sign match, or
  top-three alternative may be used to rescue an
  unmappable sign.

### Transformations

None.

### Exploratory analyses

No exploratory result may change the criterion or
the verdict. Sequence-length composition and
crosswalk conflict flags may be described beside
the outcome, but they do not adjust the registered
share.

## Other

### Small-set limitation

This registration's central limitation is its size.
Two signs cannot support a broad conclusion about
the INITIAL class or about Indus sign behaviour in
general.

A pass would establish only that P217 and P324 both
met the stated bar in this pinned Harappa dataset.
It would not establish that the signs begin
linguistic words, that they have particular sounds
or meanings, that the script is deciphered, or that
other INITIAL signs would pass.

A failure would establish only that this exact
two-sign criterion was not met. It would not refute
cross-site preservation for the wider INITIAL class
or say anything about P000's positional behaviour.
P000 was excluded because it lacks a best-match
crosswalk counterpart, not because it was observed
to fail at Harappa.

### Lineage limitation

The independence claimed is site withholding:
Harappa rows were excluded from the training pool.
It is not a claim that the datasets are independent
of scholarly lineage. The Yajnadevam compilation's
object base is published-corpus material.

### Scoring gate

This registration text does not itself authorise
scoring. Scoring requires a separate owner order
and a scoring design that first verifies the OSF
registration, all input hashes, the training-pool
exclusion, the reproduced classification, and the
mappability screen.

### Source records

- Proposed register entry:
  `docs/research/pred-2026-011-registration/proposed-prediction-register-entry.md`
- Derivation record:
  `docs/research/pred-2026-011-registration/derivation-record.json`
- Derivation script:
  `backend/scripts/pred011_register_derivation.py`
- Predecessor derivation:
  `reports/pred010_derivation_record.json`

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
