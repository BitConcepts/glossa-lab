# Spec 032 / Phase-396 — Outcome record (2026-10-13)

Execution of the frozen Spec 032 contract under the owner's
authorisation of 2026-10-13 ("Do ALL that remains now", and
the Spec 032 execution order of the same day).
Registration: OSF https://osf.io/3htn8/, DOI
10.17605/OSF.IO/3HTN8, approved and public before execution
(record: `osf-registration.md` in this directory; PR #204,
merge `d08b6e3e`). Infrastructure: PR #210. Frozen text was
not edited by this execution; this record is an append-only
outcome document.

**Result in one paragraph.** PRED-2026-006 — registered on
2026-04-22 — says that signs classed as opening signs
(INITIAL) in the CISI Mohenjo-daro training would also open
texts at Harappa in the held-back Yajnadevam data, with
success fixed in advance at at least 70% of those signs
showing a Harappa start rate of at least 0.40. The frozen
design runs three provenance checks before any counting,
and the second one failed on the program's own record:
the classification that produced the INITIAL signs was
not trained on CISI Mohenjo-daro alone. It was trained on
the combined corpus of 2,722 inscriptions, and 970 of
those inscriptions are Yajnadevam Harappa inscriptions —
the very kind of held-back data the prediction was
supposed to be tested on. Eleven of the twelve trained
signs occur inside those 970 inscriptions (1,013
occurrences in all). The withholding the registration
specified was therefore never real for this test, so
under the frozen rules the study closes as **CANNOT BE
RUN AS WRITTEN**. No start rate was computed, no share
exists, and there is no verdict: the prediction remains
unscored, exactly as the frozen closure rules require a
step-0 closure to be reported — as itself, not dressed
as a result about the prediction.

## 1. What was executed

The frozen execution shape (spec section 10), in order:

1. **Graph-first build (E1).** Script
   (`backend/scripts/phase396_pred006_step0.py`), graph
   module (`backend/glossa_lab/experiment_graph_phase396.py`,
   node `IndusPhase396Pred006Scoring`), registration in
   the experiment graph, registration verification, then
   the run (PR #210).
2. **Step 0 (E2)** — section 2 below. The step-0 record
   was written and hashed before any counting began;
   check 3.2 failed and the study closed there.
3. **Scoring (E3).** Not run. The registered computation
   exists in the build, gated behind a full step-0 pass,
   and is fenced by unit tests on synthetic fixtures
   (`backend/tests/test_phase396_build.py`), so the
   machinery is verified even though the data never
   lawfully reached it.
4. **Outcome (E4).** This record; the register append
   (section 5); the root LEDGER entry. Nothing was
   written into any frozen record.

## 2. Step 0, check by check

### 3.1 The trained INITIAL set — PASS

The recorded lineage (`scripts/global_class_stability.py`;
output of 2026-04-22T18:16:22Z) was reconstructed from
the record: the classification logic, carried verbatim,
was recomputed over the recorded training corpus
(`data/normalized/corpus_master.csv`; the recorded
script's `data_normalized/` path is the same file at its
present location). The recomputed classifiable map
matches the recorded output
(`outputs/analysis/global_class_stability.json`) exactly
— 105 classifiable signs, no differences. The trained
INITIAL set is therefore frozen, as the design requires,
at the recorded 12 signs:

P000, P001, P004, P013, P051, P098, P217, P238, P265,
P301, P310, P324.

### 3.2 The withholding — FAIL

The frozen fact has two parts: the INITIAL assignments
came from CISI Mohenjo-daro, and the Harappa Yajnadevam
sequences played no part in training them. The program's
own corpus definition (`docs/research/CORPUS_DEFINITION.md`,
v1.0, 2026-04-23) and the training corpus itself answer
both parts, against the fact:

- The training corpus is the **combined** corpus: 179
  CISI inscriptions (Component A — Mohenjo-daro only)
  plus 2,543 Yajnadevam inscriptions (Component B), for
  the recorded total of 2,722. The recorded
  classification pooled all of it; there is no
  Mohenjo-daro-only training anywhere in the recorded
  lineage the freeze anchors to.
- Of the 2,543 Yajnadevam inscriptions inside the
  training corpus, **970 are Harappa inscriptions**.
  The trained signs occur inside them as follows
  (provenance counts from the training corpus itself,
  not from the withheld file):

  | Sign | Occurrences inside the 970 | Sign | Occurrences inside the 970 |
  |---|---|---|---|
  | P000 | 0 | P217 | 91 |
  | P001 | 16 | P238 | 5 |
  | P004 | 64 | P265 | 2 |
  | P013 | 33 | P301 | 16 |
  | P051 | 4 | P310 | 60 |
  | P098 | 254 | P324 | 468 |

  Eleven of the twelve trained signs; 1,013 occurrences
  in total. (P324 alone — the dominant opening sign —
  occurs 468 times in the Harappa inscriptions that sat
  inside the training corpus.) The global positional
  profiles from which the INITIAL classes were assigned
  were computed over those inscriptions, so the Harappa
  Yajnadevam material did play a part in training the
  assignments.

The later exposure the design names (Phases 281–293
loaded the Yajnadevam corpus for unrelated work) is real
but is not the failure: the failure is earlier and
structural — the held-back corpus was a training input
from the day the classes were computed (2026-04-22).
Under spec section 3 and claim F032-C05, a withholding
that cannot be verified closes the study as **CANNOT BE
RUN AS WRITTEN**, with the reason. This is that closure,
with the reason.

### 3.3 Sign identity — not reached

The study closed at 3.2, in the frozen order, so the
crosswalk was never fixed for counting and no
unmappable count exists. The crosswalk files the design
names are present in the record
(`data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`
and its recorded statistics); they were inputs to the
step-0 record's hashes only.

## 3. What this closure is, and what it is not

- It **is** the frozen outcome for this case: the
  registered test cannot be run as written, because the
  set it would test was trained on data that included
  the withheld corpus. Scoring it anyway — or rebuilding
  a Mohenjo-daro-only set now and testing that — would
  score a different prediction, and the register's own
  rules require a new PRED number for it (spec section
  3.1). No such substitution was made.
- It **is not** a verdict on PRED-2026-006. The
  prediction is neither confirmed nor not confirmed;
  it remains unscored. The register's "PARTIALLY
  CONFIRMED" wording — resting on the global 72.7%
  figure, a different quantity measured across all sites
  on this same pooled corpus — stands in the register
  as the pre-execution record; the appended entry
  (section 5) records this closure alongside it.
- It **is not** a finding about opening signs at
  Harappa. Nothing about Harappa start rates was
  measured; the withheld file was not opened for
  scoring at any point in this execution.

## 4. Step-0 record

The step-0 record (checks, the frozen trained set, the
composition evidence, and the SHA-256 hashes of the
training corpus, the recorded stability output, the
crosswalk file, and the withheld file) is committed as
`reports/phase396_results.json`, with a readable summary
at `reports/phase396_step0_report.md`. Step-0 record
sha256:
`26781336c8c34b006e62474448b17be4d895c1d7ea06d5c24418d49a38e7c4e7`.

## 5. Register handling

The outcome is appended to `docs/PREDICTION_REGISTER.md`
as a dated entry under its section 6 (append-only
adjudication notes), in this PR. The register's existing
text is byte-identical; the PRED-2026-006 entry in
section 3 is unchanged, and its recorded state is now
annotated by the appended entry: taken to execution
under Spec 032 / Phase-396 on 2026-10-13; closed at
step 0.2 as CANNOT BE RUN AS WRITTEN; unscored.

## 6. Per-claim determinations (frozen register F032-C01…C12)

The frozen claims register is not edited; determinations
are recorded here, in the Spec 029 machinery's pattern.

| Claim | Determination | Basis |
|---|---|---|
| F032-C01 | No change | No verdict was issued, so the claim's bound on verdict wording was never exercised; the closure wording claims nothing about the prediction. |
| F032-C02 | Checked (execution) | The registered criterion (share ≥ 70%; start-rate bar 0.40) was carried unmodified into the build as pinned constants; the closure is precisely the refusal to substitute any other criterion. |
| F032-C03 | Checked (execution) | The trained INITIAL set was reconstructed from the recorded lineage and frozen before any counting (section 2, check 3.1). |
| F032-C04 | No change | The set was reproduced exactly, so this claim's closure condition did not fire. |
| F032-C05 | Checked (execution) | The withholding check ran as the claim prescribes and the fact failed: 970 Yajnadevam Harappa inscriptions sat inside the training corpus, carrying 1,013 occurrences of 11 of the 12 trained signs. The claim's closure — CANNOT BE RUN AS WRITTEN — is the outcome. |
| F032-C06 | No change | Not reached: the study closed at 3.2, before the crosswalk fixing of 3.3; no counting began. |
| F032-C07 | No change | Not reached: no unmappable count exists and no verdict exists for a coverage statement to lead. |
| F032-C08 | No change | No score was computed; the share the claim defines does not exist. |
| F032-C09 | No change | No per-sign scoring table exists. The per-sign table in section 2 is a provenance table (occurrences inside the training corpus), published as step-0 evidence; it is not the descriptive table this claim pre-registers, and is not presented as it. |
| F032-C10 | No change | No verdict wording was issued. The closure record claims only what section 2 verifies from the record. |
| F032-C11 | Checked (execution) | The outcome is appended to the PRED register as a dated entry in this PR; the register's existing text is byte-identical. |
| F032-C12 | Checked (execution) | The step-0 closure is reported as itself — in this record, in the step-0 report, and in the register entry — and nowhere as a verdict. |

## 7. What remains not understood, and open items

- Whether opening signs are in fact stable at Harappa
  remains exactly as not-understood as the lane-2 record
  left it: the registered test cannot answer it, because
  its trained set was never independent of the Harappa
  data. A future test would need a trained set derived
  without the Yajnadevam corpus in the training pool —
  a new prediction under a new PRED number, registered
  before its withheld data is touched, per the
  register's own rules. Registering one is an owner
  decision; nothing here pre-judges it.
- The global 72.7% INITIAL stability figure keeps its
  own caveat, now sharper: it was computed on the pooled
  corpus, so it measures agreement between a global
  classification and its own parts, not preservation
  into held-out data. The lane-2 explanation record for
  PRED-2026-006 already states the neighbouring-quantity
  gap; this closure adds the reason the registered
  quantity cannot now be produced from that lineage.
- Nothing in this record re-opens PRED-2026-007 or any
  other prediction (spec section 11).

## 8. Products and gates

`reports/phase396_results.json` (the step-0 record, with
input hashes), `reports/phase396_step0_report.md`, this
outcome record, the PRED register append, and the root
LEDGER entry. Build: `backend/scripts/phase396_pred006_step0.py`
via the experiment graph node `IndusPhase396Pred006Scoring`
(H23 steps 1–5; PR #210 + this record's PR). Gates:
foundation check 40 passed / 0 failed / 8 warnings; full
backend suite green in CI on PR #210 and on this PR (see
PR records); branding sweep clean. One test pin advanced
by name in this PR: the Spec 029 Phase D guard
`test_pred_register_document_untouched` pins the PRED
register's whole-document hash to prove that migration
did not alter it; the register append this execution is
frozen to make (spec section 7) changes that hash, so
the pin now names the 2026-10-13 append as the one
authorised drift, with the new hash recorded in the
test. The Spec 029 freeze replay is unaffected (the
test file is not among its frozen sources).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
