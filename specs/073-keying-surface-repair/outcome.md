# Spec 073 outcome — Phase-436 — Spec 073: keying-surface repair (Registry v2 + Asset A v2)

## Outcome: REPAIRED WITH NAMED SHORTFALL

**Headline.** The repair is built and measured. Registry v2 keeps all
803 v1 rows byte-identical and adds 210 rows for attested signs the
old registry could not name, each stated in the published ICIT sign
list (Fuls 2023, *A Catalog of Indus Signs*, Ch. 2.3). Asset A v2
keeps all 187 v1 rows untouched and adds 365 rows entered blind under
the same discipline as v1. Measured over the recorded populations:
the 31-sign opening-strong set now keys 31 of 31 (baseline
26 by resolution in Spec 070's record) and the 557-sign documented
set now keys 556 of 557 (baseline 285). The one attested
code no published source identifies is named, not dropped: token
999, a corpus placeholder that appears in no published sign list.
The celestial (sky/cycle) class in Asset A v2 is 0 rows —
stated plainly beside Spec 071's frozen TOO THIN floor of 30: a
future re-freeze of the sky-signs question would still meet an empty
celestial class on the published labels, because no ruled source
depicts any of the newly keyed signs as a sky object.

## The five named signs (Spec 070's unkeyable five)

- ICIT 136: resolved + keyed — Registry v2 identity W136, Asset A v2 row present (depicted kind: unidentified); the Catalog's Parpola concordance places it at Parpola.
- ICIT 298: resolved + keyed — Registry v2 identity W298, Asset A v2 row present (depicted kind: unidentified); the Catalog's Parpola concordance places it at Parpola.
- ICIT 401: resolved + keyed — Registry v2 identity W401, Asset A v2 row present (depicted kind: unidentified); the Catalog's Parpola concordance places it at Parpola.
- ICIT 617: resolved + keyed — Registry v2 identity W617, Asset A v2 row present (depicted kind: unidentified); the Catalog's Parpola concordance places it at Parpola.
- ICIT 824: resolved + keyed — Registry v2 identity W824, Asset A v2 row present (depicted kind: unidentified); the Catalog's Parpola concordance places it at Parpola.

Each of the five is *resolved + keyed*: a Registry v2 row now names
it and an Asset A v2 row exists. None of the five carries a verbal
depiction in any ruled published source, so each row's depicted kind
is *unidentified* — keyed for joining, honestly unclassified.

## Coverage (M1–M5)

- M1 (Wells coverage): the parpola_1982 Wells map still carries
  498 distinct ids
  (baseline 498; completions added: 0);
  the new icit_wells rows carry 210
  further ids; Registry v2 names 708 distinct
  Wells/ICIT ids in total.
- M3 remainders: 31-set {}; 557-set {'no registry resolution': 1}.
- M4 (census by kind, new rows): {'human': 18, 'animal': 10, 'other': 119, 'object_goods': 8, 'unidentified': 210};
  carried rows unchanged.
- M5 (frame accounting, §4.3): of 707
  attested frame codes, 496
  were already carried by a v1 identity, 210
  received a new icit_wells identity, 1
  has NO PUBLISHED IDENTITY (['999']), and
  0 is CONTESTED IDENTITY.
  Lineage (P-F1 S3): every identity statement behind Registry v2 and every label behind Asset A v2 sits in the ICIT tradition and its published concordances (the CISI sign list, the Fuls 2023 Catalog) — consistency within one tradition, not independent corroboration.

## Closing checks

Registry v1 re-hashed at the close: 8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420
(pin 8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420) — untouched: True. Asset A v1 re-hashed:
952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b (pin 952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b) — untouched: True.
Step-0 gates 0.1–0.4 all PASS (execution/step0-record.json).

## What this does not establish

- It does not re-run, amend, or supersede Spec 070's POPULATION NOT
  KEYED closure or Spec 071's INVALID closure; both stand exactly as
  recorded, and neither Hunt claim changes state.
- It does not decide whether either Hunt question should be re-frozen
  against the repaired surface; that is a separate owner decision.
- It establishes nothing about what any sign means; the celestial
  count is a property of the published labels, not of the script.
