# T103 Execution Order — Spec 053 Step 0 Re-execution (2026-11-16)

**Order.** Under Spec 095 Stage 1, task T103 (the adopted queue of
2026-11-16: Spec 092 Stage 2, Spec 094, then the Spec 095 build
stages), Spec 053's frozen step 0 is re-executed once, in this tree,
under the conditions below. This order was given before the run (it
is the T103 tasking in the Spec 095 Stage 1 commission) and is filed
with the stage's records as T103 requires.

**Instrument.** `backend/scripts/phase413_yadav_zipf_controls.py`,
unmodified at base `966f22ba` (current origin/main, the Spec 094
closeout merge). The instrument executes Spec 053's step 0 gates in
their frozen order and no system fit.

**Gates.** Byte-unchanged from Spec 053's frozen step 0 (freeze
digest `fd2d5cb86b6aed51882a945719bb747ac34f149b08a21e6485b1407c6dc6b309`):
0.1 input integrity, 0.2 estimator self-test, 0.3 strict corpus
identification and pin, 0.4 control set freeze, 0.5 census and
floors. No gate, pin, tolerance, or wording was altered for this
re-execution.

**Precondition.** T102 complete: the strict-corpus artifact
pin-verified against the PR #393 intake pin and placed read-only at
the canonical path in this tree.

**Scope.** Step 0 only. The run's outputs are filed as this stage's
own records (`t103-phase413-results-2026-11-16.json`,
`t103-phase413-step0-report-2026-11-16.md`); the frozen step-0
outputs in `reports/` were restored byte-identical after capture
(SHA-256 `98ccd10a…` and `e0edac40…`, matching their pre-run
values). No frozen text was moved.

**Outcome.** INVALID at gate 0.1 — see the stage record
(`stage-1-record-2026-11-16.md`, §T103) for the pin table and the
finding. Gates 0.2–0.5 were NOT REACHED, in the frozen order.
