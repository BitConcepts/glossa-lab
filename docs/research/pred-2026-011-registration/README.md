# PRED-2026-011 — Registration Record

> ## REGISTERED — 2026-10-20
>
> PRED-2026-011 was registered on 2026-10-20 under
> Tristen Pierson's registration order of the same
> day: the entry is appended to the authoritative
> prediction register (`docs/PREDICTION_REGISTER.md`
> §3, with dated notes in §6), and the OSF
> Preregistration filed from the Predictions &
> Registrations node `nrb9u` is approved and public:
> https://osf.io/t6whq/, DOI **10.17605/OSF.IO/T6WHQ**
> (API-verified 2026-10-20: accepted, public, DOI
> as stated, `registered_from` `nrb9u`). The
> prediction stands PENDING and unscored; scoring
> requires its own future spec and owner order.

## The registration in brief

PRED-2026-011 asks the same question as
PRED-2026-010:

> Will signs classified as INITIAL from CISI
> Mohenjo-daro inscriptions also tend to appear at the
> start of Harappa inscriptions in the Yajnadevam data?

The one design change is disclosed here, before any
registration or scoring: **the trained signs are
screened for mappability before the prediction is
registered**. A sign may enter the trained set only
if the frozen public crosswalk gives it a best-match
counterpart on the Yajnadevam side.

That screen changes the trained set from
PRED-2026-010's three signs to two:

| Underlying INITIAL sign | Best-match counterpart | Eligible for PRED-2026-011? |
|---|---|---:|
| P000 | none | No |
| P217 | Y0520 | Yes |
| P324 | Y0740 | Yes |

**Trained INITIAL set: P217, P324.**

This is a weak test because it has only two signs.
The registered 70% bar can pass only if **both** signs
meet the per-sign bar. A pass would be a narrow result
about P217 and P324 in this dataset. It would not
validate the INITIAL class as a whole.

## Why a successor is needed

PRED-2026-010 derived three INITIAL signs from the
clean CISI Mohenjo-daro pool: P000, P217, and P324.
The frozen crosswalk reading used by the programme
treats a row's `best_parpola_match` as the counterpart
and treats `top3_parpola` entries only as alternatives
or conflict flags.

Under that reading:

- P217 has a best-match counterpart, Y0520
  (confidence 1.0, confirmed).
- P324 has a best-match counterpart, Y0740
  (confidence 0.9867, confirmed).
- P000 has no best-match counterpart. It appears only
  in `top3_parpola` on the rows for Y0527, Y0740,
  Y0820, and Y0892.

PRED-2026-010's own rule says that an unmappable share
above 20% closes its scoring as CANNOT BE RUN AS
WRITTEN. With three signs, P000 alone is 33%. The
successor does not change that rule after the fact.
It creates a new prediction whose eligibility rule is
stated before registration.

This package does not alter PRED-2026-010 or its
register status; its formal closure under Spec 035 /
Phase-399 is recorded in the register's §6 entry of
2026-10-20 and in
`specs/035-pred-2026-010-scoring/outcome.md`.

## Design

### Training pool

The training pool is unchanged from PRED-2026-010:

- Source file: `data/normalized/corpus_master.csv`
- Filter: rows whose `source_name` is "Corpus of
  Indus Seals and Inscriptions (mayig digitization)"
- Pool size: 179 inscriptions
- Sites: Mohenjo-daro only
- Yajnadevam rows in the pool: 0

The recorded `global_class_stability` classification
logic is carried through the PRED-2026-010 derivation
unchanged. Recomputing it for this registration
reproduced the 010 record exactly:

- 28 classifiable signs
- INITIAL 3
- MEDIAL 19
- MIXED 3
- TERMINAL 3
- Unscreened INITIAL set: P000, P217, P324

### Mappability screen

After classification, and before registration, each
INITIAL sign is checked against the frozen crosswalk:

- **Eligible:** at least one crosswalk row names the
  sign as `best_parpola_match`.
- **Not eligible:** no such row exists.
- `top3_parpola` appearances do not establish a
  counterpart.

The screen produced:

- Retained: **P217, P324**
- Excluded: **P000**

The screening input is the public crosswalk file. The
design step read no Harappa inscription rows,
sequences, occurrence counts, or start rates. That is
a statement about this design step; the crosswalk
remains a mapping assumption and is fixed by hash so
it cannot be quietly replaced.

### Withheld scoring data

If PRED-2026-011 is separately taken to scoring
under a future spec and owner order, the scoring
pool remains the Harappa-site rows of the same
withheld file used for PRED-2026-010:

- `backend/glossa_lab/data/yajnadevam_inscriptions.csv`
- SHA-256:
  `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`

No Harappa start rate was computed for this
registration.

## Fixed inputs

| Input | SHA-256 |
|---|---|
| Training corpus file, `data/normalized/corpus_master.csv` | `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e` |
| Filtered CISI Mohenjo-daro pool manifest | `ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a` |
| Frozen crosswalk, `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv` | `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2` |
| Withheld Yajnadevam file | `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` |
| Recorded classification script, `scripts/global_class_stability.py` | `37e7bb533778daf1c4cf1220f71331e38c156b09abce7436bccc53bafb97ad5d` |
| PRED-2026-010 derivation record | `95c197afd414ac0895b2e621932b9f8920aaac7a56d701702975c02951a3e9ef` |
| PRED-2026-010 derivation script | `f7df0b94820a0dce8b1e25bb461b976e7b7fa7537728b777a78a09aaa1bac13c` |

## Registered criterion

The criterion keeps the form used by PRED-2026-006
and PRED-2026-010:

- For each trained sign, compute its Harappa start
  rate: the share of its Harappa occurrences, counted
  through its frozen crosswalk counterpart glyphs, in
  which it is the first sign of an inscription
  sequence.
- A sign meets its bar if its start rate is at least
  **0.40**.
- The prediction passes if at least **70%** of the
  trained signs meet that bar.
- A mappable trained sign with zero Harappa
  occurrences does not meet the bar and stays in the
  denominator.
- The unmappable cap remains **20%**. If a future
  scoring check finds a trained sign unmappable under
  the pinned crosswalk, that is 1 of 2 signs, or 50%,
  so the scoring closes as CANNOT BE RUN AS WRITTEN
  before any share is reported.

### The arithmetic for two signs

The possible shares are only:

- 0 of 2 = 0%
- 1 of 2 = 50%
- 2 of 2 = 100%

Therefore, **only 2 of 2 passes**. There is no partial
pass at 1 of 2.

## What the result would and would not establish

### If both signs pass

A pass would establish only this narrow statement:

> P217 and P324, the two mappable signs classified as
> INITIAL from the clean CISI Mohenjo-daro pool, both
> met the registered 0.40 start-rate bar in the
> Harappa rows of the pinned Yajnadevam file.

It would **not** establish that:

- the INITIAL class is generally preserved across
  sites;
- all or most Mohenjo-daro INITIAL signs behave the
  same way at Harappa;
- P000 would have passed, because P000 is excluded
  for a mapping reason, not scored on its positional
  behaviour;
- the signs begin words in a linguistic sense, as
  opposed to standing first in recorded inscription
  sequences;
- any sign has a sound, meaning, or deciphered
  reading;
- the result is independent of scholarly lineage.
  The independence claimed is Harappa's exclusion
  from training, not independence of the published
  corpus tradition behind the datasets.

### If one or both signs fail

A fail would establish only that the registered
two-sign criterion was not met. Because each sign is
half of the denominator, one sign determines the
difference between pass and fail. A fail would not
refute cross-site preservation for the wider INITIAL
class, and it would say nothing about P000's
positional behaviour.

## Disclosures that must travel with the registration

1. **Mappability was screened before registration.**
   This is the one deliberate design change from
   PRED-2026-010. The screen used the public,
   hash-pinned crosswalk and no Harappa inscription
   data.
2. **Cleanliness is not blindness.** The trained set
   was derived without Yajnadevam rows in the
   training pool. That is verified training-pool
   exclusion. The Yajnadevam Harappa pool had
   previously been inspected in aggregate during
   the Spec 032 closure audit; the aggregate counts
   are in that record. No Harappa start rate has
   been computed for P217 or P324.
3. **The set is very small.** Two signs are enough
   to run the stated arithmetic, but not enough to
   support a broad claim about a sign class. The
   small-set warning belongs in the registration
   itself, not only in later reporting.
4. **The crosswalk is fixed, not chosen at scoring.**
   Best-match rows carry sign identity. Top-three
   alternatives do not create counterparts.
5. **P000 was not removed because of its Harappa
   behaviour.** It was removed because it has no
   best-match counterpart in the frozen crosswalk.
   No Harappa behaviour for P000 was examined.

## Registration record

The registration was completed on 2026-10-20, in
this order:

1. This package was prepared as a draft under the
   owner's order of 2026-10-20 ("go with your
   recommendation") and merged as PR #219.
2. Under the owner's registration order of the same
   day, the entry in
   `proposed-prediction-register-entry.md` was
   appended to `docs/PREDICTION_REGISTER.md` (§3,
   with a dated note in §6), and the Phase D
   register-hash pin was advanced by name for that
   authorised append (PR #220).
3. The OSF Preregistration text in
   `osf-registration-payload.md` was filed from the
   Predictions & Registrations node `nrb9u`
   (draft `6ad7639c62324b723e259c5e`; registration
   `t6whq`, `date_registered` 2026-10-20T12:54:02Z).
4. The registration was approved via the token link
   in OSF's admin-notification email and verified
   approved and public by API on 2026-10-20:
   https://osf.io/t6whq/, DOI
   **10.17605/OSF.IO/T6WHQ** (`reviews_state`
   accepted, public, no approval pending, not
   withdrawn, `registered_from` `nrb9u`). The
   verified URL and DOI are recorded in the
   register's §6 by dated append, and the
   registration's OSF emails were archived after
   verification.
5. Scoring remains for a separate owner order and
   scoring design. Registration alone is not a
   scoring order.

## Package contents and reproduction

- `proposed-prediction-register-entry.md` — the
  register entry text as appended at registration
  (its status lines completed at filing) and its
  dated append note.
- `osf-registration-payload.md` — the OSF
  Preregistration text as filed on 2026-10-20.
- `derivation-record.json` — the machine-readable
  derivation and screening record.
- `backend/scripts/pred011_register_derivation.py`
  — the reproducible derivation and screen.
- `backend/tests/test_pred011_draft_registration.py`
  — checks that the derivation reproduces the
  screened set and that the package records the
  completed registration.

Reproduce the derivation from the repository root:

```bash
python backend/scripts/pred011_register_derivation.py
```

The script fails closed if the recomputed
PRED-2026-010 basis differs from its committed record
or if the crosswalk hash differs from its pin.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
