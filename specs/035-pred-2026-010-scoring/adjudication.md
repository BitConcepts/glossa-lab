# Spec 035 — Adjudication Record

> ## ADJUDICATED INPUT — 2026-10-20
>
> This spec has one adjudication input, recorded
> here so the draft's basis is inspectable:
>
> 1. **The owner's draft order of 2026-10-20**:
>    "Let's do your recommendation" — adopting the
>    recommendation put to the owner the same day:
>    run the CISI 3.1 intake, and draft the
>    PRED-2026-010 scoring spec alongside it. That
>    order is the adjudicating act for this
>    **draft**. It commissions the design only: the
>    freeze of this contract and any execution are
>    separate owner decisions, not commissioned by
>    it, and this draft performs neither.

## 1. The adopted basis (operative substance)

The registered test, carried into `spec.md`
without deviation:

- **Prediction.** Signs assigned to the INITIAL
  class in training on CISI Mohenjo-daro
  inscriptions ONLY will appear preferentially in
  initial position in Harappa-specific Yajnadevam
  data as well (PRED-2026-010, the clean-withholding
  successor to PRED-2026-006, closed unscored by
  Spec 032 / Phase-396).
- **Trained set.** P000, P217, P324 (3 signs),
  derived at registration from the CISI
  Mohenjo-daro pool only (179 inscriptions, 28
  classifiable signs) by the recorded
  classification logic carried verbatim.
- **Criterion.** At least 70% of the trained signs
  show a Harappa start rate of at least 0.40 —
  with 3 signs, only 3 of 3 passes (the register's
  small-set caveat).
- **Unmappable rule.** Any trained sign with no
  crosswalk counterpart is 33% of the set, above
  the registered 20% cap: the scoring closes as
  CANNOT BE RUN AS WRITTEN before the withheld
  file is opened.
- **Disclosure.** The cleanliness claimed is
  verified training-pool exclusion, not analyst
  blindness; the Harappa pool was inspected in
  aggregate during the Spec 032 closure audit.

## 2. Verification record at draft

Every registered fact this design rests on was
verified first-hand at drafting, 2026-10-20,
against the record on `main` (head `527e776f`,
the Spec 033 outcome merge):

- **Register entry** — read in
  `docs/PREDICTION_REGISTER.md` §3 (the
  PRED-2026-010 entry) and the §6 note of
  2026-10-13: prediction, trained set, pins,
  criterion, unmappable closure, small-set caveat,
  disclosure, OSF pointer. All as designed here.
- **Derivation record** — read in
  `reports/pred010_derivation_record.json`:
  pool 179 rows, all Mohenjo-daro, zero
  Yajnadevam rows; 28 classifiable signs (INITIAL
  3 / MEDIAL 19 / MIXED 3 / TERMINAL 3); trained
  set [P000, P217, P324]; the verbatim-carry
  basis (recorded script SHA-256
  `37e7bb533778daf1c4cf1220f71331e38c156b09abce7436bccc53bafb97ad5d`;
  Phase-396 check 3.1 reproduced the recorded
  classification exactly).
- **File pins** — recomputed by streaming hash
  from the bytes on `main` at this draft, all
  equal to the registered pins:
  `data/normalized/corpus_master.csv`
  `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`;
  `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`
  `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`;
  `backend/glossa_lab/data/yajnadevam_inscriptions.csv`
  `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`.
  The withheld file was hashed, not opened — the
  same byte operation the registration performed.
- **Withheld census** — 5,679 inscriptions, 77
  sites, 2,717 Harappa, as recorded at the Spec
  032 freeze (§4 of its spec) for the
  byte-identical file; the pin above ties that
  census to these bytes.
- **OSF registration** — API-verified at this
  draft: accepted, public, DOI
  10.17605/OSF.IO/WJEBQ (`osf-registration.md`).
- **Crosswalk coverage observation** — recorded
  in full in `spec.md` §0.4: under the frozen
  Phase-396 reading (best-match rows carry
  identity; top-3 alternatives set conflict flags
  only), P217 → glyph Y0520 (confidence 1.0,
  confirmed) and P324 → glyph Y0740 (confidence
  0.9867, confirmed) carry counterparts, and
  **P000 carries none** (top-3 alternative only,
  on the rows for Y0527, Y0740, Y0820, Y0892). On
  that reading, execution closes at step 0.4 as
  CANNOT BE RUN AS WRITTEN, unscored. This
  observation is the single most decision-relevant
  fact in the draft: the freeze decision is a
  decision to buy the formal step-0 record (the
  closure as a finding under a frozen contract),
  or to leave PRED-2026-010 PENDING. The draft
  itself makes no determination.
- **Not verified at draft, by design** — the
  filtered-pool manifest pin (`ab3b4c8a…`) is a
  derived value: it stands in the derivation
  record as read, and its re-derivation is
  step-0 check 0.3 at execution (spec §3). No
  Harappa count, occurrence count, or start rate
  was computed at this draft, and none exists
  anywhere in the record.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), knowing §0.4's
   observation: execution is expected to close at
   step 0.4, unscored — or decline, leaving
   PRED-2026-010 PENDING.
2. DD-035-2's zero-occurrence reading (a mappable
   sign absent at Harappa counts as not meeting
   the bar) — it stands unless the freeze
   overturns it openly; on the §0.4 observation it
   is unlikely ever to be reached.
3. DD-035-4: whether the frozen spec files its
   own OSF contract registration (the Spec
   032–034 pattern) in addition to the
   prediction's preregistration (wjebq).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
