# Replication index — what an outsider can re-derive

*Step 1 of the road-to-decipherment plan. Written 2026-10-25.*

## What this is

This index maps every headline verdict of the programme's recent
run of studies (Specs 036–074, the sixteen verdicts listed below)
to the evidence an outsider would need to check it: the outcome
record where the verdict stands, the committed script that
produced it, the input pins recorded at the freeze, and one
honest label saying how far an outsider can actually get.

It exists because a verdict is only as good as its trail. Some of
these studies can be re-run end to end by anyone with this
repository. Some can be checked in part — the arithmetic is all
here, but the run itself used a file the programme holds under
restriction. And some rest on an input that is restricted or
lost, so an outsider has to take the programme's word. This
index says which is which, verdict by verdict, in plain words.

Scripts are run from the repository root, in the programme's
Python environment, and write their machine records to
`reports/`. Where a script needs a file that is not in this
repository, the row says so and names the file and its pin.

## The three labels

- **RECOMPUTABLE** — an outsider can re-run the study end to end
  from public inputs. The row names the script, the inputs, and
  where any input that lives outside this repository can be
  fetched, with the pin to check it against.
- **PARTIAL** — part of the check is public and part is not. The
  arithmetic behind the verdict can be re-done from committed
  results, or a verdict-bearing input can be rebuilt from
  committed results, but the run itself needs a restricted
  input. The row states exactly which part is public and which
  part is not.
- **TRUST-ONLY** — a verdict-bearing input is restricted or
  lost, and the committed record does not carry enough to
  re-derive the verdict. The row names the input and the
  reason: the Shakti corpus and its row-grades (restricted-local,
  never published); CISI material (licence terms — statistics
  are publishable, the scans are never redistributed); the
  indusarrays layer (lost; re-acquisition is Route 2, pending);
  or the ICIT website CSVs (lost).

## Correction note — 2026-10-25 (red-team finding RT-10)

The custody-verification record of 2026-10-25
(`docs/decisions/2026-10-25-custody-verification.md`) states, in
the RT-10 row, that Asset A v2's 552-row table is
environment-local — that "the repo carries its hash and citation
log only" and the file's holding location was not established.
**That statement is wrong.** The full table is published in this
repository at
`specs/073-keying-surface-repair/asset-a-v2/depicted-kind-classification.csv`,
and on 2026-10-25 it recomputes to SHA-256
`681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`
— exactly the value pinned in
`specs/073-keying-surface-repair/asset-a-v2/asset-a-v2-freeze.json`.
Step 1(a) of the road-to-decipherment plan therefore resolves as
**VERIFIED-ALREADY-PUBLISHED**, not as a new publication. The
custody record stands unedited (it is cited by frozen records);
this note is the correction of record.

## The keying tables — publication state, verified 2026-10-25

Three tables carry much of the recent work. Their state,
checked first-hand against current `main`:

- **Asset A v2** (Spec 073) — **published in this repository.**
  `specs/073-keying-surface-repair/asset-a-v2/depicted-kind-classification.csv`,
  SHA-256 `681e017d…` (full value above), 552 data rows. Columns
  include the verbatim depicted label
  (`depicted_label_verbatim`), the governing source
  (`governing_source`), and per-row citations
  (`source_citations`). Its entry log is
  `specs/073-keying-surface-repair/asset-a-v2/entry-decisions.json`.
  Provenance, per the Spec 073 freeze record: the programme's own
  compilation, entered blind from held published sources — the
  CISI sign list as held, Parpola 2010, and the Fuls 2023
  *Catalog* for registry identities.
- **Asset A v1** (Spec 069) — **published in this repository.**
  `specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv`,
  187 data rows, recomputing to SHA-256
  `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b`
  — exactly its freeze pin in
  `specs/069-hunt-asset-a/asset-a/asset-a-freeze.json`.
- **Registry v2** (Spec 073) — **published in this repository.**
  The folder `specs/073-keying-surface-repair/registry-v2/` holds
  only three records (`change-schedule.json`,
  `no-published-identity.json`, `registry-v2-freeze.json`), but
  the table itself stands at the canonical path its freeze
  names: `data/crosswalks/canonical_sign_registry_v2.csv`,
  1,013 data rows, recomputing to SHA-256
  `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`
  — exactly the pin in `registry-v2-freeze.json` (803 rows
  carried from Registry v1, 210 ICIT/Wells rows added).

## Summary

| Spec | Headline verdict | Label |
|---|---|---|
| 036 | PRED-2026-011 CONFIRMED | RECOMPUTABLE |
| 040 | NOT-YET-TESTABLE | RECOMPUTABLE |
| 041 | Mapping EXECUTED | PARTIAL |
| 052 | INCONSISTENT | PARTIAL |
| 054 | STRICT CORPUS NOT PINNABLE (closure, no counts) | TRUST-ONLY |
| 062 | NO TARGET UNDER EITHER SCENARIO | RECOMPUTABLE |
| 063 | RECOVERED | PARTIAL |
| 064 | IDENTIFICATION FAILED | PARTIAL |
| 065 | Class A complete — both sources resolved | PARTIAL |
| 067 | REPLICATED | PARTIAL |
| 068 | COMPARISON UNINFORMATIVE | PARTIAL |
| 070 | POPULATION NOT KEYED (closure) | PARTIAL |
| 071 | INVALID (closure, stopped at step 0) | PARTIAL |
| 072 | Executed — held under the Roif gate | TRUST-ONLY |
| 073 | REPAIRED WITH NAMED SHORTFALL | PARTIAL |
| 074 | NOT SUPPORTED | PARTIAL |

Counts: 3 recomputable, 11 partial, 2 trust-only.

## Spec 036 — PRED-2026-011 CONFIRMED — RECOMPUTABLE

- **Verdict and scope.** PRED-2026-011 is CONFIRMED on its exact
  registered criterion: the two trained signs (P217, P324) both
  show a Harappa start rate above the 0.40 bar (0.8739 and
  0.6111; share 1.0 against the registered ≥ 70% criterion).
  Two signs only; nothing about P000; nothing about the INITIAL
  class as a whole.
- **Outcome record.** `specs/036-pred-2026-011-scoring/outcome.md`
  (freeze digest `bbbd5c4f…` in the spec's `freeze.json`).
- **Script.** `backend/scripts/phase400_pred011_scoring.py`
  (scoring logic carried from the frozen Phase-396 build,
  `backend/scripts/phase396_pred006_step0.py`; derivation in
  `backend/scripts/pred011_register_derivation.py`). Run:
  `python backend/scripts/phase400_pred011_scoring.py`. One
  step-0 check reads the prediction's OSF registration standing
  (t6whq) live, as the contract requires.
- **Input pins (freeze).** Training corpus
  `data/normalized/corpus_master.csv` `b19cfe95…`; withheld
  Harappa file `backend/glossa_lab/data/yajnadevam_inscriptions.csv`
  `c02e3d7b…`; crosswalk
  `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`
  `e44b8b55…`; filtered-pool manifest `ab3b4c8a…`.
- **Why this label.** Every input is committed in this
  repository at its pin, and the outcome record reports an
  independent recount through a separate code path agreeing
  exactly. An outsider can re-run the whole scoring from public
  inputs.

## Spec 040 — NOT-YET-TESTABLE — RECOMPUTABLE

- **Verdict and scope.** The chronology-controlled rerun of the
  G1 site-repertoire test (Phase-439 execution, 2026-10-24)
  closes NOT-YET-TESTABLE at the margins gate: arms 1 and 2
  failed (EARLY keeps 1 distinct site and LATE 2, against 5
  required; unassigned share 73.1% against the 40% arm), arm 3
  passed. No outcome quantity was computed, and G1 stands
  unchanged with its rider — chronology is NOT controlled in
  the primary test. (The outcome record also carries the
  earlier freeze-stage record of 2026-10-20, where the same
  word closed the spec at the dependency gate; the Phase-439
  execution is the executed headline.)
- **Outcome record.**
  `specs/040-d25-g1-chronology-controlled/outcome.md`, with
  `specs/040-d25-g1-chronology-controlled/step0-record.md`
  (freeze digest `16aeeb70…`).
- **Script.** `backend/scripts/phase439_g1_chronology_controlled.py`.
  Run: `python backend/scripts/phase439_g1_chronology_controlled.py`.
- **Input pins (freeze).** The ICIT-lineage layer (horus84
  `inscriptions.csv`) `c368f290…` — not in this repository;
  fetch it from its public source,
  `horus84/Computational_Linguistics` at commit `ac44f08c` (the
  source and commit recorded in the step-0 record), and check
  the hash before use. Spec 041's mapping artifact
  `data/evidence_integration/site_period_mapping.jsonl`
  `1e5b54c9…`; Phase-139 covariates
  `data/evidence_integration/phase139_harmonized_covariates.json`
  `a0f0d05a…`; chronology spine
  `data/movement/chronology_rows_phase394.jsonl` `9dc2fba5…`;
  anchors `df0cf620…` — all committed here.
- **Why this label.** The margins computation is deterministic
  code over those inputs, and every input is either committed
  here or fetchable from the named public source at a pinned
  commit under a hash pin. An outsider can re-run step 0 and
  the margins gate end to end.

## Spec 041 — Mapping EXECUTED — PARTIAL

- **Verdict and scope.** The site × local-label period mapping
  Spec 040 needed was built: of 78 attested label cells on the
  5,410 population inscriptions, 24 are assigned a coarse
  period on a published determination (4 EARLY, 18 MATURE,
  2 LATE) and 54 are unassigned, each with a stated reason;
  none contested. The mapping is not a dating of any
  inscription, and it does not by itself make Spec 040's test
  testable.
- **Outcome record.**
  `specs/041-site-local-label-period-mapping/outcome.md`, with
  `coverage-report.md` and `step0-record.md` in the same
  directory (freeze digest `fe618886…`).
- **Scripts.** `backend/scripts/phase435_site_period_mapping.py`
  (stages `step0`, `build`, `verify`).
- **Input pins (freeze).** ICIT-lineage layer `c368f290…` (as
  in Spec 040: not in this repository; public source
  `horus84/Computational_Linguistics` at `ac44f08c`); Phase-139
  covariates `a0f0d05a…`; anchors `df0cf620…`. Products: the
  artifact `1e5b54c9…`, its meta `bda1017d…`, the step-0 census
  `b57fb6b1…` — all committed.
- **Why this label.** Public: the finished mapping, the full
  determinations record (`determinations.json`), the
  independent verification record (`verification-record.json`),
  the census, and the coverage report are all committed, so
  every one of the 78 cells can be audited against its cited
  published determination, and the mechanical census and build
  can be re-run once the layer is fetched at its pin. Not
  public as a re-run: the determinations themselves are a
  judgement extraction from published sources — recorded in
  full, checkable cell by cell, but not something code
  re-derives.

## Spec 052 — INCONSISTENT — PARTIAL

- **Verdict and scope.** On the Shakti corpus layer, both
  pattern conditions of battery NB-1 hold (7 TERMINAL_STRONG
  signs against a permutation chance level of 0; the opening
  bigram (400, 740) recurring 179 times against a chance level
  of 76), so under the amended contract's re-pointed wording
  the outcome is INCONSISTENT: the Farmer pattern is absent in
  this compilation, and the "artefact of the Soviet dataset"
  caveat widens. It is not a verdict on the
  Farmer–Sproat–Witzel thesis. Read the word with the amendment
  and the freeze, not with `spec.md` §4.1 alone — the
  outcome record's 2026-10-25 correction notes (RT-05, RT-28)
  say why, and give the threshold-robustness of the strong set.
- **Outcome record.** `specs/052-farmer-not-writing-soviet/outcome.md`
  (freeze digest `83658949…`); machine record
  `reports/phase437_results.json`.
- **Script.** `backend/scripts/phase437_farmer_nb1_shakti.py`.
- **Input pins (freeze).** Shakti corpus `345241b1…` and
  row-grades `02394241…` — restricted-local, never published
  (intake record:
  `docs/decisions/2026-10-22-shakti-corpus-intake-record.md`).
  Phase-43 record `outputs/phase43_all.json` `78a6c219…`,
  committed.
- **Why this label.** Public: the machine record carries the
  per-sign initial/medial/terminal counts for every sign in
  both arms (557 primary, 707 sensitivity), and those counts
  sum to the recorded token totals (11,805 primary; 17,216
  sensitivity) — so the strong sets, both conditions, and the
  headline quantities can all be re-checked by arithmetic from
  committed results. Not public: the sequences themselves.
  Re-running the battery, including its permutation null,
  needs the Shakti corpus and row-grades, which are
  restricted-local.


## Spec 054 — STRICT CORPUS NOT PINNABLE (closure, no counts) — TRUST-ONLY

- **Verdict and scope.** A closure, not a measurement: the test
  closed at step 0, gate G2, because the strict corpus the
  Phase-43 battery used — the programme's V3 layer, a
  reconstruction of the indusscript.in database — could not be
  uniquely identified and pinned. No positional quantity was
  computed in either arm, no strong set exists, and the claim
  stands exactly as recorded.
- **Outcome record.** `specs/054-yadav-opening-closing/outcome.md`
  (freeze digest `d85f6ace…`); machine record
  `reports/phase438_results.json`; step-0 record
  `specs/054-yadav-opening-closing/step0-record.md`.
- **Script.** `backend/scripts/phase438_yadav_opening_closing.py`
  (the full frozen instrument; the gates stopped it before any
  count, as designed).
- **Input pins (freeze).** Claim store at its post-append pin
  `938174b0…`; Phase-43 record `78a6c219…`; crosswalk v1
  (CSV `3d0b9ef1…`, JSON `4e7559df…`); anchors `df0cf620…` —
  all committed, and gate G1 re-verified them at the run.
- **Why this label.** The verdict-bearing input is the V3
  layer's data file — the Firestore "indusarrays" dump the
  Phase-43 record names as its corpus's source. It is **lost**:
  absent from this tree, from the programme's database (whose
  only Indus text is the synthetic prototype), and from every
  neighbouring tree scanned. Re-acquisition is Route 2,
  prepared 2026-10-24 and still pending. An outsider can audit
  the recorded identification attempt — the machine record
  carries the reference census (3,916 records / 2,665 dockeys /
  3,137 sequences / 12,494 sign instances) and the censuses of
  the five other layers checked — but the finding itself is a
  statement about the programme's own stores, and it cannot be
  re-derived from public inputs.

## Spec 062 — NO TARGET UNDER EITHER SCENARIO — RECOMPUTABLE

- **Verdict and scope.** Inside the frozen search frame (grid
  multiples m = 1…25, 199 trials per point), no grid point
  under either stated scenario reaches the 80% resolving share
  Arm A would need at the 0.01 margin — the best point anywhere
  is 0.1759. "No target" is scoped to that frame; it does not
  say no amount of data could resolve Arm A in principle, and
  Spec 028 Arm A stands INCONCLUSIVE exactly as recorded.
- **Outcome record.**
  `specs/062-arm-a-precision-calibration-repair/outcome.md`
  (freeze digest `1800de53…`); machine record
  `reports/phase424_results.json`; the full grid table is in
  the outcome record and the machine record.
- **Script.** `backend/scripts/phase424_arm_a_precision_calibration_repair.py`,
  importing the pinned machinery
  `specs/028-harappa-robustness/pipeline393.py`. Run the gates
  with `--step0-only`; the grid with `--scenario 1` and
  `--scenario 2`; finish with `--assemble`.
- **Input pins (freeze).** Phase-393 results
  `reports/phase393_results.json` `0a1657a8…`; corpus
  `backend/glossa_lab/data/yajnadevam_inscriptions.csv`
  `c02e3d7b…`; pipeline `6c2ff91c…`; margins audit
  `specs/028-harappa-robustness/margins-audit.json`
  `15ae0281…`; Spec 028 freeze record `376cd8e7…`; anchors
  `df0cf620…` — all committed.
- **Why this label.** Every input is committed at its pin, and
  step 0 reproduces the recorded Arm A summary digit-for-digit
  — that reproduction is the cheap first check. The honest
  caveat is cost, not access: the full grid is 9,950 trials
  and ran as a multi-day checkpointed computation on the
  owner's desktop. Recomputable, but not quick.

## Spec 063 — RECOVERED — PARTIAL

- **Verdict and scope.** Candidate K-1 (Wells 2015, printed
  p. 92: sign 821 in the Dholavira signboard contexts has a
  meaning of "city") is recovered as a claim in proper form —
  its subject sign is identified, by route 2, through the
  preserved drawn-form reference. Recovery establishes that
  the passage argues this and that its subject is identified;
  it establishes nothing about whether the argument is right,
  and nothing about what sign 821 means. The claim enters at
  the created stage, untested.
- **Outcome record.**
  `specs/063-sign821-identification-successor/outcome.md`
  (freeze digest `dc24a10e…`); evidence of record
  `specs/063-sign821-identification-successor/identification-record.md`;
  machine record `reports/phase425_results.json`.
- **Script.** `backend/scripts/phase425_sign821_identification.py`.
- **Input pins (freeze).** Held cleaned text of Wells 2015
  `62acf855…`; Registry v1 `8a0b2a82…`; Phase-123 witness
  `ecbc37a4…`; preserved reference
  `specs/063-sign821-identification-successor/drawn-form-reference-821.json`
  `695dd35d…` — all committed. The Wells 2006 thesis PDF
  `4b39330c…` (19,313,853 bytes) is **not** committed: an open
  deposit, held locally, asserted on the local file before
  any plate was read.
- **Why this label.** Public: every repository input, the
  preserved reference, both independent derivation sheets, the
  reconciliation, and the route record are committed, so the
  identification can be audited step by step. Not a re-run:
  the descriptor derivations are readings of a plate in a
  thesis file an outsider must obtain from its open deposit
  and hash-check — a judgement recorded in full, not a
  computation code re-derives.

## Spec 064 — IDENTIFICATION FAILED — PARTIAL

- **Verdict and scope.** The fragment "sign 297 is the horned
  tiger" cannot be carried to a concordance: the descriptor's
  discrimination of 297 from its neighbours in the 289–308 run
  was not sustained by either independent derivation, so the
  run closed at step C, before any list was scored. No
  statement about the sign is made, and nothing is fed to
  Asset A. The preserved reference's continuity status stays
  QUALIFIED — anchored at family level only.
- **Outcome record.**
  `specs/064-sign297-concordance-successor/outcome.md`
  (freeze digest `cfeb7baf…`); delivery (empty feed, the
  stated closure form)
  `specs/064-sign297-concordance-successor/concordance-297.json`
  `9e765576…`; machine record `reports/phase426_results.json`.
- **Script.** `backend/scripts/phase426_concordance.py`.
- **Input pins (freeze).** Claim record `997fa336…`; held
  cleaned text `62acf855…`; Registry v1 `8a0b2a82…`;
  Phase-123 witness `ecbc37a4…`; Spec 046 closure delivery
  `772db4df…`; preserved reference
  `specs/064-sign297-concordance-successor/drawn-form-reference-297.json`
  `33ee22ec…` — all committed. The Wells 2006 thesis PDF
  `4b39330c…` is **not** committed: local research store only,
  an open deposit (named in the freeze by its Internet Archive
  identifier), asserted on the local file before any plate
  was read.
- **Why this label.** Public: every repository input, the
  preserved reference, both derivation sheets with their
  neighbour counts (recorded in full in the outcome record),
  and the closure delivery are committed, so the failure can
  be audited feature by feature. Not a re-run: as in Spec 063,
  the decisive step is a plate reading from a hash-pinned file
  held outside this repository — a recorded judgement, not a
  computation.


## Spec 065 — Class A complete — both sources resolved — PARTIAL

- **Verdict and scope.** Both of Spec 057's unlocated rows are
  resolved on the documents themselves, and the heading record
  stands retired: on each document, the heading "Statistical
  finding: positional analysis" is HEADING ABSENT FROM
  DOCUMENT. The 2026-10-22 run closed in class B (S-5
  resolved, S-1 still blocked); the recovery act appended the
  same day searched S-1 on the document the owner handed over
  and completed the accounting in class A. This act searched
  documents for a heading; it checked nothing either passage
  states.
- **Outcome record.** `specs/065-s1-s5-heading-successor/outcome.md`
  (run record §§1–8.1; recovery act §9) (freeze digest
  `f50a6e9c…`); machine record `reports/phase427_results.json`.
- **Script.** `backend/scripts/phase427_s1_s5_heading.py`.
- **Input pins (freeze and intake).** The S-5 document
  (Hunt preprint, Zenodo DOI 10.5281/zenodo.17066226) at
  SHA-256 `77f10f32…` — public from Zenodo, not committed.
  The S-1 document (Fuls chapter, *Studies on Indus Script*,
  2020) at SHA-256 `51831ac9…` — handed over by the owner, held
  locally, not committed and not redistributed. Held cleaned
  texts `1275b795…` (S-1) and `dd584975…` (S-5), literature
  registry files, and Spec 057's records — committed.
- **Why this label.** Public: the full text layer actually
  searched for each document is committed as an artifact —
  `specs/065-s1-s5-heading-successor/extraction-S5.txt`
  (`74e42f8e…`) and `extraction-S1.txt` (`e5bc973d…`) — so
  every occurrence (one in S-5, two in S-1) and its judgement
  can be re-checked line by line without either document, and
  the S-5 document itself can be fetched from its public DOI
  and hash-checked. Not public: the S-1 document, which rests
  on the owner's hand-over; an outsider re-checks its search
  from the committed extraction, not from the document.

## Spec 067 — REPLICATED — PARTIAL

- **Verdict and scope.** On the enlarged object-ID-joined set
  (4,676 of 5,679 lineage rows, 82.34%, against the original
  join's 51.0%), the seal/tablet difference in TERMINAL14
  endings replicates within sites: Mantel–Haenszel odds ratio
  2.452, 95% CI [1.965, 3.058], entirely above 1.5, q = 0.0001;
  leave-one-site-out: no site is load-bearing. A statement
  about recorded use in this lineage layer, not about what
  the difference means.
- **Outcome record.** `specs/067-f1-enlarged-join/outcome.md`
  (freeze digest `73463ab9…`); machine record
  `reports/phase429_results.json`.
- **Script.** `backend/scripts/phase429_f1_enlarged_join.py`,
  reusing the pinned Phase-136 statistic functions
  (`backend/scripts/phase136_terminal_type.py`, `d5ceec46…`).
- **Input pins (freeze).** Committed: Phase-136 results
  `11a07413…`; Registry v1 `8a0b2a82…`; CISI 3.1 extension
  index `be20439a…`; Phase-421 census and results. Held in
  the local store, not committed: the ICIT-lineage layer
  `c368f290…`; the CISI vols. 1–2 catalogue layers (`e0d698f9…`,
  `e751244e…`); the converted keyed layer v2 `bbfdbcd5…`; and
  the merged catalogue layer v2 `cd0c2ba8…` (9,741 rows, 5,529
  distinct objects) that the join resolves against.
- **Why this label.** Public: the outcome and machine record
  carry the full per-stratum tables, the pooled table, the
  test quantities, and the leave-one-site-out reruns, so the
  Mantel–Haenszel computation and the verdict mapping can be
  re-done by arithmetic from committed results. Not public:
  the join itself. The per-row join census
  (`phase429_join_census.json`, 5,679 rows) is a
  restricted-local product, and the merged catalogue layer v2
  is built from CISI material held under licence — statistics
  publishable, source rows never redistributed.

## Spec 068 — COMPARISON UNINFORMATIVE — PARTIAL

- **Verdict and scope.** The linguistic positive control,
  Linear B, fitted the Zipf–Mandelbrot curve worst of all
  five systems (fit error 0.9229, against 0.5335, 0.1839, and
  0.2405 for the non-linguistic controls), so under the frozen
  rule the comparison cannot judge the script. The Indus
  quantities on the Shakti corpus (fit error 0.1584, exponent
  2.004) are reported as a new baseline for the record and
  support no separability conclusion either way; the claim
  stands exactly as recorded, with no strength label added.
- **Outcome record.**
  `specs/068-yadav-zipf-controls-successor/outcome.md` (freeze
  digest `ab890859…`); machine record
  `reports/phase430_results.json`.
- **Script.** `backend/scripts/phase430_yadav_zipf_controls.py`,
  with the estimator of record imported from
  `backend/scripts/phase413_yadav_zipf_controls.py`.
- **Input pins (freeze).** Shakti corpus `345241b1…` and
  row-grades `02394241…` — restricted-local, never published.
  The four control systems' tables are committed in
  `specs/068-yadav-zipf-controls-successor/data/` (N1
  `0f938c19…`; N2 charges `0c618df4…`, with its blazon
  transcription and extraction record; P1 `895a1ebf…`; N3 is
  generated under frozen parameters). Crosswalk `4ace1a61…`.
- **Why this label.** Public: the control tables are
  committed, the estimator is committed, and the machine
  record carries every system's fitted quantities, so the
  control fits, the estimator self-test, and the comparison
  arithmetic (the gaps, the positive-control rule, the
  near-miss band) can all be re-run and re-checked. Not
  public: the Indus fits themselves. Their input is the
  Shakti corpus under its row-grades, which are
  restricted-local; the reported Indus fit numbers cannot be
  re-derived from committed results.

## Spec 070 — POPULATION NOT KEYED (closure) — PARTIAL

- **Verdict and scope.** A closure, not a measurement: Shakti's
  opening-strong set was enumerated in full (31 signs), and
  five of them (ICIT 136, 298, 401, 617, 824) could not be
  keyed to exactly one Asset A row in Wells space on the
  pinned Registry v1, so under the disposition the freeze
  fixed in advance the execution closed at step 0, gate 0.4.
  No join was performed and no test quantity was computed;
  the claim stands as recorded.
- **Outcome record.**
  `specs/070-hunt-opening-signs-successor/outcome.md` (freeze
  digest `763108f8…`); machine record
  `reports/phase433_results.json`.
- **Script.** `backend/scripts/phase433_opening_signs.py`.
- **Input pins (freeze).** Asset A v1 `95231935…` (published,
  see the keying-tables section); Registry v1 `8a0b2a82…`;
  crosswalk `4ace1a61…`; anchors `df0cf620…` — committed.
  Shakti corpus `345241b1…` and row-grades `02394241…` —
  restricted-local.
- **Why this label.** Public: the machine record publishes
  the full population enumeration — all 31 opening-strong
  signs with their initial/medial/terminal counts — and names
  the five unkeyable signs with their reasons, so the
  closure's decisive step (the keying check against the
  published Registry v1 and Asset A v1) can be re-done in
  full from committed results. Not public: deriving that
  population from the corpus. The battery ran on the Shakti
  corpus under its row-grades, which are restricted-local.


## Spec 071 — INVALID (closure, stopped at step 0) — PARTIAL

- **Verdict and scope.** A closure, not a measurement: the run
  stopped at step 0, gate 0.3, as INVALID. Of the 557 signs
  occurring in the primary population, 272 carry no Asset A row
  under the frozen keying route (134 with no resolution in the
  pinned registry's Wells map; 138 resolving to registry signs
  outside Asset A's 187-row universe), and an absent row is
  never treated as non-celestial by default — that default
  would silently define the comparison class. No
  final-position quantity was computed, no verdict on the sky
  signs question exists, and the claim stands UNTESTED. The
  record also states the adjacent fact: Asset A's celestial
  class is empty (zero `sky_cycle` rows), below the frozen
  TOO THIN floor of 30.
- **Outcome record.** `specs/071-hunt-sky-signs-successor/outcome.md`
  (freeze digest `c06a7a86…`); machine record
  `reports/phase434_results.json`.
- **Script.** `backend/scripts/phase434_sky_signs.py`.
- **Input pins (freeze).** Asset A v1 `95231935…`; Registry v1
  `8a0b2a82…`; crosswalk `4ace1a61…`; anchors `df0cf620…` —
  committed. Shakti corpus `345241b1…` and row-grades
  `02394241…` — restricted-local.
- **Why this label.** Public: the machine record's coverage
  census lists every one of the 272 uncovered signs with its
  population total and its reason, beside the 285 covered —
  the full sign set the gate counted — so the coverage
  arithmetic and every keying failure can be re-checked
  against the published Asset A v1 and Registry v1. Not
  public: establishing that these 557 signs are exactly the
  primary population's signs. That census came from the
  Shakti corpus under its row-grades, which are
  restricted-local.

## Spec 072 — Executed — held under the Roif gate — TRUST-ONLY

- **Verdict and scope.** Under Spec 072's §7 limit 1 (the Roif
  gate), this study is named in programme reporting only as
  **executed — held under the Roif gate**, without result
  content, until Roif 2025a and 2025b are cited and the owner
  clears the specific publication act. Neither condition is
  met, so this index carries no outcome word for Spec 072 —
  carrying one would repeat the breach the 2026-10-25
  redaction (red-team finding RT-26;
  `docs/decisions/2026-10-25-realignment-decision.md`)
  repaired.
- **Outcome record.** `specs/072-fish-family-profiles-redesign/outcome.md`,
  in the gate's permitted form (freeze digest `3925f365…`);
  machine record `reports/phase431_results.json` and report
  `reports/phase431_report.md`, both held stubs recording the
  redaction.
- **Script.** `backend/scripts/phase431_fish_family_profiles.py`.
- **Input pins (freeze).** Asset F (the fish-family asset,
  `specs/044-fish-sign-coastal-residue/asset-f-fish-family.json`)
  digest `ca5fb1b5…`; Mahadevan–Parpola crosswalk `9ebd7723…`;
  Phase-43 record `78a6c219…` — committed. Shakti corpus
  `345241b1…` and row-grades `02394241…` — restricted-local.
- **Why this label.** An outsider cannot re-derive anything
  about this study's result from the public record: the
  result records were reduced to held stubs on 2026-10-25
  under the gate above, and the run's corpus inputs were the
  restricted-local Shakti files in any case. (Git history
  retains the original records, as the redaction decision
  states plainly; no history purge has been authorised. The
  gate governs what the current public record carries, and
  this index follows the current record.)

## Spec 073 — REPAIRED WITH NAMED SHORTFALL — PARTIAL

- **Verdict and scope.** The keying surface that closed Specs
  070 and 071 is repaired and measured: Registry v2 keeps all
  803 v1 rows byte-identical and adds 210 rows for attested
  signs the old registry could not name; Asset A v2 keeps all
  187 v1 rows and adds 365 rows entered blind under the same
  discipline. The 31-sign opening-strong set now keys 31 of 31
  (baseline 26) and the 557-sign documented set keys 556 of
  557 (baseline 285). The named shortfall: token 999, a corpus
  placeholder, has NO PUBLISHED IDENTITY in any ruled source,
  and the celestial class in Asset A v2 is 0 rows — a future
  re-freeze of the sky-signs question would still meet an
  empty celestial class. Neither Spec 070's closure nor Spec
  071's closure is amended by this repair.
- **Outcome record.** `specs/073-keying-surface-repair/outcome.md`
  (freeze digest `5419c4c4…`); machine record
  `reports/phase436_results.json`; product freezes
  `specs/073-keying-surface-repair/registry-v2/registry-v2-freeze.json`
  and `specs/073-keying-surface-repair/asset-a-v2/asset-a-v2-freeze.json`.
- **Scripts.** `backend/scripts/phase436_step0.py`,
  `backend/scripts/phase436_registry_v2.py`,
  `backend/scripts/phase436_asset_a_v2.py`,
  `backend/scripts/phase436_coverage.py`.
- **Input pins (freeze).** Asset A v1 `95231935…`; Registry v1
  `8a0b2a82…`; crosswalk `4ace1a61…` — committed and published.
  The Fuls volumes as held (Catalog PDF `31729a4f…`; Corpus
  PDF `185fd057…`, held on the owner's desktop) and the
  Shakti corpus and row-grades (frame populations, via the
  Spec 070/071 machine records) — not in this repository.
  Products: Registry v2 `42ab09fb…` and Asset A v2
  `681e017d…`, both published (see the keying-tables section).
- **Why this label.** Public: both product tables are
  published in full at their pins, with the entry log
  (`asset-a-v2/entry-decisions.json`), the change schedule,
  and the catalog consult record
  (`specs/073-keying-surface-repair/execution/catalog-consult.json`),
  so every added row can be audited against its stated source,
  and the coverage measures (M1–M5) can be re-done from the
  published tables and the committed Spec 070/071 machine
  records. Not public as a re-run: the entry work itself —
  blind entry from held published sources (the Fuls volumes
  as held; the CISI sign list as held) is a recorded
  judgement process, not a computation, and the held volumes
  are not in this repository.

## Spec 074 — NOT SUPPORTED — PARTIAL

- **Verdict and scope.** NOT SUPPORTED — and the containment
  is part of the verdict: this is a verdict on the
  programme's internal restatement of the Hunt claim, on
  Shakti, in ICIT numbering. The re-scoped question was
  whether Shakti's opening-strong signs are the animal signs.
  Of the 31 opening-strong signs, 2 are animal signs under
  the frozen classification (226 and 241, both fish signs) —
  a share of 0.0769 among the 26 classified members, against
  a base share of 0.0889: enrichment ratio R1 = 0.8654,
  Fisher exact one-sided p = 0.7345. The frozen falsifier
  fires on both grounds (R1 ≤ 1.0; p ≥ 0.05). The outcome
  record's 2026-10-25 correction note (RT-27) prints the
  frozen formula's literal-reading ratio beside the published
  one (R1 = 0.9359 on the inventory's own share, 6 of 73);
  the verdict is the same under every reading. The honesty
  fence stands: this test measures the claim against a
  positional framework measured on the graded ICIT corpus
  (the Shakti corpus), not against the Phase-43 framework.
- **Outcome record.**
  `specs/074-hunt-opening-signs-repaired-surface/outcome.md`
  (freeze digest `5416a0d3…`); machine record
  `reports/phase440_results.json` (`d539519d…`, byte-identical
  across the execution's two runs); report
  `reports/phase440_report.md`.
- **Script.** `backend/scripts/phase440_hunt_opening_signs.py`.
- **Input pins (freeze).** Asset A v2 `681e017d…` and Registry
  v2 `42ab09fb…` — published (see the keying-tables section).
  Spec 070's machine record `reports/phase433_results.json`
  `667560a5…`; Registry v1 `8a0b2a82…`; crosswalk `4ace1a61…`;
  anchors `df0cf620…` — committed. Shakti corpus `345241b1…`
  and row-grades `02394241…` — restricted-local.
- **Why this label.** Public: the decision arithmetic is fully
  auditable from committed results. The machine record
  carries the keyed population, both classification tables
  (the 31 opening-strong signs and the 76-sign comparison
  inventory, sign by sign), both 2×2 tables, and all three
  sensitivity arms — and gate 0.4's reproduction asserted
  that the population enumeration equals Spec 070's recorded
  enumeration exactly (its canonical publication hash is
  identical). An outsider can rebuild the join from the
  published Asset A v2 and Registry v2 and re-run the exact
  test on the committed population. Not public: where the
  population came from. The opening-strong enumeration was
  measured on the Shakti corpus under its row-grades, which
  are restricted-local, so the corpus counts behind the
  population cannot be re-derived — the verdict's arithmetic
  can be checked in full, its corpus basis cannot.

## Closing line

This index establishes only what an outsider can re-derive —
not that any verdict is right.

---

*AI disclosure: written by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution §VI.
Verification of the keying tables was performed first-hand
against `main` at 379a9fc3 on 2026-10-25; every script path
named above was checked against the tree, and every verdict,
pin, and label was taken from the spec's own outcome and
freeze records as cited.*
