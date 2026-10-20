# Spec 035 / Phase-399 — Outcome record (2026-10-20)

Execution of the frozen Spec 035 contract under the owner's
freeze-and-execute order of 2026-10-20 ("go with your
recommendation"; freeze record: `freeze.md` in this
directory; freeze digest
`d72a50e1943c1af55846dfb2db93e73b50e08a287c06925a331c0304096128c4`).
The prediction's preregistration: OSF https://osf.io/wjebq/,
DOI 10.17605/OSF.IO/WJEBQ (record: `osf-registration.md`).
The frozen spec's own contract registration: OSF
https://osf.io/qkj8d/, filed 2026-10-20 before execution
(record: `osf-spec-registration.md`; pending admin approval
at execution — not a step-0 condition, since spec §3 check
0.1 names wjebq). Frozen text was not edited by this
execution; this record is an append-only outcome document.

**Result in one paragraph.** PRED-2026-010 — registered on
2026-10-13 — says that the three signs classed as opening
signs (INITIAL) in training on CISI Mohenjo-daro alone —
P000, P217, P324 — would also open texts at Harappa in the
held-back Yajnadevam data, with success fixed in advance at
at least 70% of those signs showing a Harappa start rate of
at least 0.40 (with three signs, only 3 of 3 passes). The
frozen design runs four checks before any counting, and
the fourth one closed the study on the program's own
published mapping: under the frozen reading of the
crosswalk (a sign's identity is carried by the rows where
it is the best match), P217 and P324 have confirmed
counterparts (Y0520 and Y0740), but **P000 has none** — it
appears only as a top-3 alternative on four other glyphs'
rows. One unmappable sign out of three is 33%, above the
20% cap the registration itself fixed, so under the frozen
rules the study closes as **CANNOT BE RUN AS WRITTEN**.
The withheld file was never opened, no start rate was
computed, no share exists, and there is no verdict: the
prediction remains unscored, exactly as the frozen closure
rules require a step-0 closure to be reported — as itself,
not dressed as a result about the prediction. This is the
outcome the draft recorded as expected (spec §0.4, from the
public crosswalk alone); the freeze was taken with open
eyes on the owner's order, and the formal determination is
this step-0 act.

## 1. What was executed

The frozen execution shape (spec §10), in order:

1. **Graph-first build (E1).** Script
   (`backend/scripts/phase399_pred010_step0.py`), graph
   module (`backend/glossa_lab/experiment_graph_phase399.py`,
   node `IndusPhase399Pred010Scoring`), registration in the
   experiment graph, then the run. The build carries step 0
   only: the registered computation is reached only behind
   a full step-0 pass, and step 0 closed the study — no
   scoring code exists in the build, so the closure is
   structural, not a branch taken.
2. **Step 0 (E2)** — §2 below. The step-0 record was
   written and hashed before any scoring could begin;
   check 0.4 failed and the study closed there.
3. **Scoring (E3).** Not run, and not reachable: the
   withheld file's content was never opened.
4. **Outcome (E4).** This record; the register append
   (§5); the root LEDGER entry; the foundation check (H21)
   in this PR's CI. Nothing was written into any frozen
   record.

**Execution environment, stated plainly.** This VM's write
restriction (recorded in the freeze work) blocks local git
object writes, so the run executed against the freeze-merge
tree (`b481a866`) with every input fetched from that tree
and verified at check 0.2 against the registered pins
before any use — the same bytes the in-repo build reads,
and the same bytes that stand on main today (the
PRED-2026-011 registration merged alongside this work
touched none of the inputs).
The committed step-0 record (`reports/phase399_results.json`)
is that run's record. A first run of the same checks
produced the identical outcome with two descriptive fields
of the coverage record (match confidence, review status)
left unpopulated by a column-name fault in the reporting
layer; it was superseded before any record was committed
by the corrected run recorded here. No check, pin, or
outcome differs between the two runs.

## 2. Step 0, check by check

Fixed order, fail-closed (spec §3). Full record:
`reports/phase399_results.json` (step-0 record sha256
`e231baf4cd0c664211089c6758296c10a035062b6566ac5200407872e4aeee1f`).

- **0.1 Registration — PASS.** The prediction's OSF
  preregistration (wjebq) re-verified at execution:
  `reviews_state: accepted`, `public: true`,
  `pending_registration_approval: false`, not withdrawn;
  `date_registered` 2026-10-13T12:45:55Z.
- **0.2 Input integrity — PASS.** All three file pins
  matched the bytes on main exactly (corpus
  `b19cfe95…`, crosswalk `e44b8b55…`, withheld file
  `c02e3d7b…`), and the derivation record's internal pins
  match the registered values, including the
  filtered-pool manifest pin `ab3b4c8a…`. The withheld
  file was byte-hashed only.
- **0.3 Training pool — PASS.** The filter
  (`source_name == "Corpus of Indus Seals and Inscriptions
  (mayig digitization)"`) yields 179 rows, all
  Mohenjo-daro, zero Yajnadevam rows, out of 2,722 corpus
  rows; the filtered-pool manifest hashes to the
  registered `ab3b4c8a…`; the recorded classification
  logic (recorded script hash `37e7bb53…` verified)
  reproduces the derivation record exactly — the full
  28-sign class map is identical (INITIAL 3, MEDIAL 19,
  MIXED 3, TERMINAL 3) and the trained INITIAL set comes
  out exactly {P000, P217, P324}. The cleanliness the
  registration claimed — Harappa excluded from training
  by construction — is verified, not assumed.
- **0.4 Crosswalk coverage — FAIL → closure.** Under the
  frozen best-match reading (DD-035-5): P217 → Y0520
  (match confidence 1.0, review status confirmed;
  conflict flag: no). P324 → Y0740 (0.9867, confirmed;
  conflict flag: yes — P324 also appears as an
  alternative on Y0741's row; recorded, not verdict-
  bearing). **P000 → no best-match row at all**; it
  appears only as a top-3 alternative on the rows of
  Y0527, Y0740, Y0820, and Y0892, which under the frozen
  reading carry no identity. Unmappable share 1/3 =
  0.3333 > the registered cap 0.20. The study therefore
  closes as **CANNOT BE RUN AS WRITTEN**, at the point
  the frozen design specifies: **before the withheld
  file is opened**. It was not opened
  (`withheld_file_content_opened: false`).

## 3. What this closure does and does not establish

It establishes a fact about the registered test's
machinery, verified under a frozen contract: the
registration's own mappability cap is exceeded by the
trained set the clean pool produced, because the frozen
crosswalk gives one of its three signs no counterpart.
Any future test of this hypothesis needs a trained set
whose signs all carry counterparts under a mapping fixed
before counting — a design property to secure at
registration, not a repair available at execution (the
denominator cannot be reduced, the cap cannot be relaxed,
and no sign can be substituted, under the frozen rules).

It does **not** establish anything about the prediction's
truth: no Harappa occurrence was counted, so nothing here
bears on whether these signs open Harappa texts. It is
not a refutation (F035-C15): PRED-2026-010 remains
**unscored**, its §3 Outcome stays **PENDING**, and the
prediction register's §4 (Failed Predictions) gains no
entry. PRED-2026-006's record is untouched and it remains
unscored. No anchor, claim status, or other prediction's
state changes.

## 4. Claim consequences (governed register)

Execution consequences under the frozen register
(F035-C01…C15), recorded here and in the root LEDGER:

| Claim | Consequence |
|---|---|
| F035-C01 | Checked (execution) — the outcome states only the closure, nothing beyond the registered statement. |
| F035-C02 | Checked (execution) — the criterion was carried unmodified; the closure is the refusal to substitute any other test. |
| F035-C03 | Checked (execution) — the trained set reproduced at 0.3 is exactly {P000, P217, P324}. |
| F035-C04 | Checked (execution) — step 0 ran in the frozen order and the record was written and hashed before any scoring; scoring never began. |
| F035-C05 | Checked (execution) — all four registered pins verified at 0.2/0.3. |
| F035-C06 | Checked at the freeze (the registration it names is wjebq); re-verified at execution step 0.1 — PASS. |
| F035-C07 | Checked (execution) — every outcome statement carries the verified-exclusion disclosure, not a blindness claim (this record, §2). |
| F035-C08 | Checked (execution) — identity was carried by the frozen crosswalk under the fixed reading only. |
| F035-C09 | Checked (execution) — fired: P000 unmappable at 0.4; closure before the withheld file opened. |
| F035-C10 | Not reached — no scoring ran; the computation stands as frozen, unexercised. |
| F035-C11 | Not reached — the zero-occurrence rule had no mappable-but-absent sign to apply to. |
| F035-C12 | Not reached — no per-sign scoring table exists; the coverage table at 0.4 is part of the step-0 record instead. |
| F035-C13 | Checked (execution) — outcome wording follows the claim: closure vocabulary only, small-set caveat carried, no verdict words used. |
| F035-C14 | Checked (execution) — register handling per §5 below: §6 dated append; §3 Outcome stays PENDING; §4 gains no entry; 006's entries byte-identical. |
| F035-C15 | Checked (execution) — the closure is reported as itself, not as a verdict and not as a refutation. |

## 5. Records

- Step-0 record: `reports/phase399_results.json`
  (step-0 record sha256
  `e231baf4cd0c664211089c6758296c10a035062b6566ac5200407872e4aeee1f`).
- Prediction register: dated §6 append in
  `docs/PREDICTION_REGISTER.md` (insertions only; the
  Phase D whole-document hash pin in
  `backend/tests/test_spec029_phase_d.py` advanced by
  name for this authorised append, as for the two
  2026-10-13 appends).
- Root LEDGER entry (Phase-399 outcome), this PR.
- tasks.md L6/E1–E4 completed in this PR (E3 marked
  not reached on the closure, as recorded).
- The spec-level OSF registration (qkj8d) completes by
  append in `osf-spec-registration.md` once its approval
  verifies (PR #221); its state does not gate this
  closure.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
