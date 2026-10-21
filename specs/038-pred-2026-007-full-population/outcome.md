# Spec 038 / Phase-401 — Outcome record (EXECUTED 2026-10-20 — CLOSED AT STEP 0.2)

> ## EXECUTED — CLOSED AT STEP 0 (2026-10-20)
>
> Phase-401 ran under the owner's
> freeze-and-execute order of 2026-10-20. The
> frozen step 0 closed the study at check 0.2:
> **CANNOT BE RUN AS WRITTEN**, unscored,
> reported as a closure and not as a verdict.
> PRED-2026-007 stands **PARTIALLY CONFIRMED**
> as its pre-execution record. The skeleton's
> slots were shapes, not outcomes (DD-038-1):
> the determination below is the execution's
> own.

## 1. What was executed

Executed under the Spec 038 freeze (digest
`b54571d845a2be3429bc532fee4bb58c20723f77e2d40ffcd43b56e0caab6eef`,
merged `c363edef`) on the owner's
freeze-and-execute order of 2026-10-20
("Freeze D-31 for execution"), which froze the
contract and ordered this execution in one
act. Graph-first build (H15/H23): execution
script `backend/scripts/phase401_pred007_step0.py`
committed before the run; experiment-graph
module `backend/glossa_lab/experiment_graph_phase401.py`
(node `IndusPhase401Pred007Census`) registered
in `backend/glossa_lab/experiment_graph.py` in
this same record. The run's machine record is
`reports/phase401_results.json`. Nothing else
was executed under this spec.

## 2. Step 0, check by check

_Pending execution._ One subsection per check,
in the frozen order, each with its evidence:

- **0.1 Sources and provenance — PASS.** The
  PRED register file hashed to the freeze
  record's value (SHA-256
  `4f8aeb54fd5853d73766ed9cf0222ef93cccfa8d9a8c399a4631221fbbb4c1c2`);
  the PRED-2026-007 entry located standing as
  registered (criterion line present,
  registered 2026-04-22, Outcome PARTIALLY
  CONFIRMED unaltered). The primary, the
  cross-check, the recorded clustering, and
  the characterisation were each present,
  readable, and hashed to the freeze record's
  cited values (primary `8c2bd605…`;
  cross-check `8a0b2a82…`; sign_clusters
  `623a787d…`; characterisation `54ebf660…`).
  The coding-source readings stood in the
  cited form: the primary's
  `data.a[].icit_function` field present across
  its 611 per-sign records, the cross-check's
  `icit_function` column present. The
  conflict rule (spec §2) in force.
- **0.2 Enumeration — FAIL; the study closes
  here.** The mechanical read of the primary's
  `icit_function` field over all 611 records
  (record-count reconciliation exact: 611
  read against the stated 611; no internal
  conflicts within the primary) returned an
  enumeration of **zero ITM-coded signs**
  (enumeration SHA-256
  `b849b0d45d37edea7f2c18af7733143b4e631f2e1aad27c6acaf42112a0436c7`).
  The held-record verification, read at the
  same pass, failed: **P385's record carries
  an empty `icit_function` value**, not ITM;
  **P378 has no record in the primary at
  all**; P098 likewise has no record (its
  must-not-read-ITM condition is the only one
  of the three met). The reason, stated
  exactly: in this file the field is not a
  coded field — of its 611 values, **579 are
  empty and 32 are free-text decipherment
  glosses** (for example "fish+two -> miiNDu
  (fish again)"); **no record carries the
  value ITM, and none carries LOG**. The
  frozen population frame (DD-038-5) names
  this field as the source of the ITM codes;
  the codes are not in it. Population size:
  **0** — the enumeration exists, is written
  here and in the step-0 record, and is empty.
- **0.3 Phase 5 output verification — NOT
  RUN.** The frozen order is fail-closed: the
  recorded clustering and characterisation
  were byte-hashed at 0.1 for integrity and
  never read for assignments. The sanity
  anchor was not reproduced because the check
  that reads it was never reached.
- **Step-0 record** — `reports/phase401_results.json`,
  step-0 record SHA-256
  `4c026edc92cdcb0c1ba6821f5ebc8242b498bb9fc4cd158607d9b1ded24a784a`
  (written before any scoring; no scoring
  figure exists).

The study closed at check 0.2, as the note
to this section pre-stated: the closure is the
outcome, sections 3–5 record it as a closure,
and the scoring section records NOT REACHED.
The census branch was not evaluated: the
enumerated population (zero signs) is not the
ITM signs already tested.

## 3. Scoring (reached only if step 0 passes in full)

**NOT REACHED — step 0 closed the study at
check 0.2.** No per-sign table is produced
(it is a scoring artifact, F038-C09); no
coverage, share, or verdict exists. The
mechanical verdict rule (DD-038-1) was never
applied, because there was no assigned
population to apply it to.

## 4. What this outcome does and does not establish

This closure establishes one bounded fact:
the frozen population frame cannot be run as
written, because the source field it names
for the ITM codes carries no coded values in
the pinned primary file. It establishes
nothing about the registered criterion's
truth: no ITM population was scored, so the
70% question stands exactly where the
register's partial record left it. The
clustering-stability caveat (F038-C11) has no
verdict to attach to, and this closure does
not rest on the Phase 5 clustering at all —
the clustering output was never read. Nothing
here states what ITM signs mean, whether the
function coding is semantically valid, or
whether the Phase 5 clustering carves the
script at its joints (F038-C12). The closure
is recorded as itself, never as a verdict,
and is not a refutation of PRED-2026-007.

## 5. Claim consequences (governed register)

- **F038-C01** (criterion unchanged): upheld —
  the registered criterion governed the run
  and was never edited.
- **F038-C02** (criterion is the registered
  one): upheld — it stood as the run's rule;
  never applied to a share, because none
  existed.
- **F038-C03** (population frame): executed as
  stated at check 0.2 — the frame was read
  exactly as the claim defines it, and
  returned the empty enumeration.
- **F038-C04** (step-0 order, fail-closed):
  **fired** — the study closed at check 0.2,
  in the frozen order, before any Phase 5
  lookup.
- **F038-C05** (provenance reconciliation
  appended): **done** — the dated note stands
  in the register's §6 in this same act.
- **F038-C06** (recorded-outputs-only
  scoring): not reached — no scoring ran; its
  prohibition was never engaged.
- **F038-C07** (coverage rule): not reached —
  no share or coverage was formed.
- **F038-C08** (census branch): not reached —
  the enumerated population (zero) is not the
  partial test's ITM signs.
- **F038-C09** (per-sign table descriptive
  only): not produced — it is a scoring
  artifact; the step-0 record carries the
  enumeration and held-record reads instead.
- **F038-C10** (record written; pin advanced
  by name): the record is written as claimed,
  and the Phase D register-hash pin is
  advanced by name for these authorised
  appends, exactly as the claim's boundary
  prescribes; on this closure the §3 Outcome
  stays PARTIALLY CONFIRMED (C14).
- **F038-C11** (clustering-stability caveat):
  carried — no verdict exists for it to
  attach to, and the closure does not rest on
  the clustering.
- **F038-C12** (non-establishment): holds —
  nothing in this record states what ITM
  signs mean or that the clustering carves
  the script at its joints.
- **F038-C13** (population an execution-time
  fact): borne out in the event — the
  membership and size did not exist before
  the run; the run produced them (empty; 0)
  and closed on the frame's integrity check.
- **F038-C14** (closure reported as closure):
  **fired** — this record and the register's
  §6 entry report the closure as itself; §3
  stands PARTIALLY CONFIRMED; §4 gains no
  entry.

## 6. Records

- Step-0 record: `reports/phase401_results.json`
  (step-0 record SHA-256
  `4c026edc92cdcb0c1ba6821f5ebc8242b498bb9fc4cd158607d9b1ded24a784a`;
  enumeration SHA-256
  `b849b0d45d37edea7f2c18af7733143b4e631f2e1aad27c6acaf42112a0436c7`).
- Register appends, in this same act: the
  dated §6 outcome entry (this closure) and
  the provenance reconciliation note
  (DD-038-2). The §3 entry is left standing as
  the pre-execution record, per spec §7's
  closure handling; the Phase D register-hash
  pin is advanced by name for these appends
  (backend/tests/test_spec029_phase_d.py).
- Root LEDGER entry: appended in this same
  act.
- Foundation check (H21) and suite state:
  verified on this record's pull request —
  the CI backend job is the full-suite
  verifier, and the foundation check is
  measured at the merge commit; both are
  reported with the merge, not asserted here.
- Every other prediction's record is not
  touched by this completion.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
