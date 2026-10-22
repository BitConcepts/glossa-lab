# Spec 029 — Closeout Record: Tao Claim Lifecycle

> Phase X of `tasks.md` (tasks X1–X2). Base: main
> `db1c3832ae1654d29266851b5e89c69b8a322204` (PR #188
> merged). Branch: `impl/029-phase-x-closeout`.
> Date: 2026-10-13.
>
> This record closes Spec 029. It changes no stage, no
> verdict, no score, and no live record. The freeze is
> not regenerated; the only edit to a frozen file in
> this closeout is the `tasks.md` checkbox tick pass,
> applied once under `freeze.md` §2 and recorded as a
> freeze amendment in §4 below.

## 1. Per-phase completion table

Every implementation phase is merged to main. Gate
results are as recorded in each phase's own record in
this directory (foundation check and full backend
suite; every phase PR's CI was verified from its own
run conclusions — all 7 checks success — before its
owner-gated merge).

| Phase | PR | Merge SHA (main) | Gate results (per its phase record) |
|---|---|---|---|
| Plan + tasks | #165 | `9202fd44` | Plan-freeze head; adjudication OD-1…OD-6 + D-A…D-E addendum in history (#164, #166) |
| L3 recovery | #167 | `e60b8408` | AEE hook pass `pass` at after_specify / after_plan / after_tasks (13 claims, 0 failure modes, 0 below threshold) |
| Freeze (F1/F2) | #168 | `a38cf92e` | `freeze.json` digest `80d589fee7bfc0099f7df496e22d8570014817ee04bca37ca8d408d3841af59d`; freeze tests pin digest + ledger §3 counts |
| A — stage axis + transition core | #169 | `028d416c` | Foundation 40/0/8; suite 2112 passed / 5 skipped (local venv, aee 1.0.4, as recorded); CI 7/7 |
| D — OD-1 re-staging migration | #171 | `712f3b99` | Foundation 40/0/8; suite 1207 passed / 6 skipped; ledger-vs-live reconciliation exact (D3/D5) |
| H — anchor annotation + schema (D-A) | #175 | `f8da5eaf` | Foundation 40/0/8; suite 1227 passed / 6 skipped; strict-set reconciliation exact (94) |
| I — claim-store deduplication (D-B) | #180 | `92e8f392` | Foundation 40/0/8; final gate 1256 passed / 6 skipped under aee 1.4.0 (post-pin integration; see §3) |
| B — bundles, attribution, explanation, digestion | #182 | `411386a6` | Foundation 40/0/8; suite 1316 passed / 6 skipped |
| C — priority register + trails | #183 | `7f773d6b` | Foundation 40/0/8; suite 1352 passed / 6 skipped |
| J — foundation annotations (D-D) | #184 | `7528ddc5` | Foundation 40/0/8; suite 1368 passed / 6 skipped |
| E1 — display withdrawals | #185 | `1533425b` | Foundation 40/0/8; suite 1374 passed / 6 skipped; screenshots desktop + mobile |
| E2 — lane-separated rendering | #186 | `587dec70` | Foundation 40/0/8; suite 1381 passed / 6 skipped; screenshots desktop + mobile |
| G — CI gates + trail completeness | #187 | `3e14dce2` | Foundation 40/0/8; suite 1407 passed / 6 skipped (26 new tests; 1,412 collected) |
| G record correction | #188 | `db1c3832` | Collection count corrected to 1,412 in the record (verified by direct re-run) |
| X — closeout | this PR | — (see PR timeline) | §2 below; foundation 40/0/8 + suite green on the closeout head (§5) |

Dispositions required by task X2: audit §9 items
**D-A, D-B, D-D, D-E are disposed by this spec's
phases** (H, I, J, and D respectively). **D-C was
executed separately**, outside this spec, by PR #166
(the adjudication addendum carrying the README
errata), before implementation began.

## 2. X1 — Final verification on merged main (verbatim results)

All runs were made against the main tree at
`db1c3832` in this phase's worktree, under the
CI-parity venv `~/workspace/venvs/glossa-ci-pin`
(aee 1.4.0), before any closeout edit.

**(a) Canonical anchors integrity — PASS, exact.**
Stripping all Spec 029 additive keys from
`backend/reports/INDUS_FINAL_ANCHORS.json` — the
Phase D stage stamps (`stage`, `stage_source`,
`stage_as_of`, `stage_history`,
`verified_unexplained`) and the Phase H annotation
(`strict_set` on every record, the `validation_status`
values Phase H assigned, and the
`metadata.spec029_phase_h_annotation` block) — and
re-serializing canonically (`json.dumps(indent=2,
ensure_ascii=False)`) gives SHA-256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`,
byte-identical to the pre-Spec-029 canonical file.
Live file at this head: 287 anchors, SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`.
No pre-existing field of any anchor was changed by
the entire spec.

**(b) PRED register untouched — PASS, zero diff.**
Baseline named: main at `9202fd44`, the plan-freeze
head (PR #165), which already contains the
pre-Spec-029 retirement entry. `git diff 9202fd44
db1c3832 -- docs/PREDICTION_REGISTER.md` is empty,
and the file's SHA-256 at both heads is
`3fb5eff1df6c4b8844bbcb8c769a8739b296c962a825557b3b1a6fe0fce75dc1`
(the value the Phase D tests pin). The only
retirement entry in the file — PRED-2026-004/005/
008/009 retired by owner decision — predates
implementation: it is commit `181d655f`, merged by
PR #163 (`5c1f7d5e`), an ancestor of the baseline.
Zero Spec 029 phase changes touched the register.
PRED-2026-001, PRED-2026-002, and PRED-2026-003 still
stand **PENDING** in the register (Tested: PENDING,
Outcome: PENDING), unscored.

**(c) Final ledger-vs-live reconciliation — PASS,
exact on every number.** Recounted from the live
stores with the Phase D migration machinery
(`count_stamped_records` over `collect_live_state`;
match: true, problems: []):

- Per class: anchors 193 created / 94 checked;
  extracted claims 21 created / 10 checked;
  registered predictions 3 created / 2 checked;
  hypothesis models 3 created; study headlines
  10 checked. Grouped/non-record entries: 9.
- **Totals: 220 created / 116 checked / 0 explained /
  0 accepted / 0 digested** — the frozen ledger's §3
  table (`reclassification-ledger.json`, 345 entries)
  reproduced exactly.
- **`verified_unexplained` flags: 105.**
- Anchors `strict_set`: exactly **94** true
  (90 HIGH + 4 MEDIUM), and the strict set is exactly
  the `validation_status == strict_sa_independent`
  set. Phase H vocabulary distribution over the 287
  anchors: `strict_sa_independent` **94**,
  `pending_non_sa_validation` **44**,
  `sa_in_provenance_chain` **33**,
  `premise_superseded` **113**,
  `no_validation_record` **3**.
- Extracted claims after Phase I deduplication: the
  store still holds all **31 records** (merge, never
  delete) resolving to **23 canonical claims** and
  **8 evidence instances** across 5 fingerprint
  groups (31 − 8 merges = 23, per `phase-i-record.md`
  §I1–I2). The Zipf proposition ("Indus script sign
  frequencies follow a Zipf-Mandelbrot distribution")
  is recorded **once** as a canonical claim
  (`yadav_2009_arxiv_manual_001`); the second record
  of it (`yadav_2010_ngrams_manual_001`) stands as
  its evidence instance (`merged_into` the canonical).

Every number above traces to its phase record: stage
totals and flags to `phase-d-record.md` /
`phase-d-run-record.md` and the frozen ledger; the
strict set and vocabulary distribution to
`phase-h-record.md` H1/H2; the dedupe counts and the
Zipf disposition to `phase-i-record.md` §I1–I3. No
mismatch was found; nothing was adjusted.

**(d) Freeze integrity — PASS.** `verify_freeze`
(framework026) over `specs/029-tao-claim-lifecycle`
returns **`[]`**. The freeze digest stands at
`80d589fee7bfc0099f7df496e22d8570014817ee04bca37ca8d408d3841af59d`
over the recovered register. No frozen input file was
touched by any later phase: the register on main
still matches the frozen digest inputs exactly (the
only frozen-file edit in the whole implementation is
this closeout's recorded tick amendment to
`tasks.md`, §4 — applied after this verification,
under the §2 bookkeeping rule, and never by
regenerating the freeze).

**(e) Full suite + foundation on merged main —
PASS.** Foundation check (`backend/scripts/
foundation_check.py`, with the gitignored Holdat
CSVs copied in, never committed): **40 passed /
0 failed / 8 warnings**. Full backend suite
(CI-identical invocation, GPU-only files excluded as
in CI): **1407 passed / 6 skipped / 0 failed**
(483.71s). This reconciles exactly with Phase G's
final run (1407 passed / 6 skipped, its 26 new tests
included): the closeout adds no tests, so the merged
baseline is unchanged.

## 3. External events during implementation

- **The aee-1.5.0 incident and pin PR #181 (external
  event, not part of this spec).** On 2026-10-12 the
  external library `applied-epistemic-engineering`
  released 1.5.0; its FR-8.7 change altered score
  semantics, and this repo's then-unpinned declaration
  (`>=1.0.4,<2`) let CI resolve it, failing one test
  on PR #180's run and leaving main red in waiting.
  The failure was not a Spec 029 defect (full record:
  `phase-i-record.md`, completion addendum; root
  `LEDGER.md`, 2026-10-12 maintenance entry).
  Maintenance PR **#181** (`fix/aee-pin-pre-1-5`,
  merged as `170e6f1f` — acknowledged here as an
  external event that occurred during implementation,
  not a spec phase) pinned the declaration to
  `>=1.0.4,<1.5`, restoring the semantics Specs
  026–029 froze under; CI thereafter resolves
  aee 1.4.0. No Spec 029 file, test, or fixture was
  changed in response to the incident.
- **Phase I worker runtime death + recovery (process
  note).** The original Phase I worker's session died
  on a runtime infrastructure fault ("background exec
  disappeared") with the implementation complete but
  uncommitted. A recovery worker forensically verified
  the uncommitted work against a pristine checkout of
  the base head before committing it — byte-level
  re-run of the merge tool, snapshot comparison, and
  independent recomputation of counts and scores —
  rather than re-implementing or blindly trusting it.
  Full record: `phase-i-record.md`, "Recovery note".

## 4. Freeze amendment — the tasks.md tick pass (task X2)

Under `freeze.md` §2 ("Checkbox ticks for F1/F2 and
phases A–X are applied in a single closeout pass
(task X2), which is recorded as a freeze amendment in
the closeout record; the freeze itself is never
regenerated"), this closeout applies the completion
ticks to `tasks.md` in the same PR as this record:

- **Ticked: 53 checkboxes** — F1, F2, and every task
  of phases A, D, H, I, B, C, J, E1, E2, G, and X
  (A1–A6, D1–D6, H1–H5, I1–I5, B1–B6, C1–C3, J1–J4,
  E1.1–E1.5, E2.1–E2.4, G1–G5, X1, X2). L1, L2, and L3
  were already ticked in the frozen bytes (L3 by its
  recorded recovery) and are untouched.
- **No task text changed.** The `tasks.md` diff was
  verified mechanically: 53 lines changed, and every
  changed line differs from its original only in the
  checkbox state (`- [ ]` → `- [x]`). After the pass
  the file carries 56 ticked boxes and 0 unticked.
- **Incomplete tasks: none.** Every ticked task was
  completed and merged under its phase gate (§1);
  X1 and X2 are completed by this closeout itself.
  No task stays unticked.
- **The amendment's one test consequence, recorded.**
  Unlike Spec 028 (whose freeze sources excluded
  `tasks.md`), this spec's freeze covers `tasks.md`
  — and this test file itself
  (`backend/tests/test_spec029_freeze.py` is also a
  frozen source). The tick pass therefore makes the
  freeze-replay test's original unconditional
  assertion (`verify_freeze == []`) fail by
  construction, naming `tasks.md` alone. The test is
  amended in this same PR to assert the exact
  post-amendment state: `verify_freeze` returns
  precisely the two named amendment drifts —
  `tasks.md` (the ticks) and
  `backend/tests/test_spec029_freeze.py` (this
  acknowledgment) — and nothing else. `freeze.json`
  is untouched and the digest is not recomputed; any
  other changed, missing, or altered frozen source
  still fails the test. X1(d)'s `[]` result (§2)
  stands as the verification on merged main before
  the amendment was applied, exactly as `freeze.md`
  §2 sequences it.

`plan.md` is not edited: §2's bookkeeping rule
records phase completion in phase records and the
program ledgers, and the tick pass it prescribes
names the `tasks.md` checkboxes. No design source
(`spec.md`, `claims.json`, `adjudication.md`,
`assessment.md`, `audit.md`,
`reclassification-ledger.json`) is changed.

## 5. Closeout gate

This PR changes records plus the §4 amendment — this
closeout record, the tick amendment to `tasks.md`,
the freeze-test acknowledgment that is part of that
amendment (§4), and the two ledger entries (root
`LEDGER.md`; short entry in `glossa-indus/LEDGER.md`).
No live code or data file is in its diff. Test-run
side effects (regenerated
timestamps in `glossa-indus/claims/extracted_claims/
*.json`, the batch-4 claims report, runtime outputs,
and the regenerated foundation report) were restored
to their committed bytes before committing.

Gate on the closeout head, CI-parity venv (aee
1.4.0): foundation check **40 passed / 0 failed /
8 warnings**; full backend suite **1407 passed /
6 skipped / 0 failed** — identical totals to the X1
run (this PR adds no tests; the one amended test
asserts the same count of freeze properties). The
PR's CI is verified from its
own check conclusions — all 7 checks success — before
merge, and the new main head is verified via the
GitHub API after merging (stated in the PR timeline;
a merge commit cannot name itself here).

## 6. Honest residuals (carried forward, not closed by this spec)

- **The promotion writer does not stamp Phase H
  fields at write time.** The research-loop promotion
  writer, which appends new anchors, does not yet
  stamp `validation_status` / `strict_set` when it
  writes; the declared schema is the contract it must
  be brought under, and a promotion landing without
  the fields now fails CI rather than drifting
  silently (`phase-h-record.md`).
- **SignsView counts and historical SA-era node
  schemas: inventoried, not changed.** `SignsView`
  still renders a per-sign deciphered/undeciphered
  count line from the signs API's per-sign flags —
  a different construction from the withdrawn
  headline, recorded by Phases E1/E2 and carried by
  Phase G as the standing follow-up, not a G4-named
  guard (`phase-g-record.md`). The historical
  experiment-graph node schemas declaring
  `sa_aggregate` / `n_fully_decoded` outputs
  (`phase-e1-record.md`) likewise stand inventoried
  and unchanged; they are not serving surfaces.
- **aee 1.5.0 adoption is a future decision.** The
  pin (`>=1.0.4,<1.5`, PR #181) holds. Adopting 1.5.0
  requires re-baselined fixtures and a fresh gate;
  its failure census under 1.5.0 stands at **14
  tests: 5 score-semantics failures and 9
  bundle-validation failures**. It is expressly not
  taken here.
- **Trail-builder string-evidence defect (Phase G
  finding 4, not fixed).** The Phase C trail builder
  iterates a string-form `glossa_lab_evidence`
  character by character on 9 live claims, serializing
  whitespace-only pseudo-refs; it is tolerated under a
  named, dated exception covering exactly those
  records, with the follow-up fix recorded in
  `phase-g-record.md`.
- **Recorded trail-completeness baseline (Phase G
  G1).** Pre-gate gaps are carried as an explicit,
  shrinkage-only baseline, named per record and per
  field in the gate and its record: no anchor carries
  a per-anchor falsifier; no extracted claim's
  extraction-era verdict names an actor (17 also lack
  a falsification condition); the document-class and
  hypothesis stamps carry no record-level evidence or
  falsifier. Any new record is held to the full
  standard with no baseline entry.
- **`not_understood` remains unauthored on all live
  claims.** Every verdict display carries the slot;
  all 31 live claims still show the recorded absence.
  Authoring those statements is lane-2 human work in
  the queue Phases E2/G wrote down; no machine text
  was substituted for it.
- **Foundation report staleness observed at X1.**
  The committed `reports/foundation_check_report.json`
  at `db1c3832` carries a `claims_store_sha256`
  (`8eb6d134…`) that no longer matches the live
  extracted-claims store digest recomputed at X1
  (`86315155…`), while its `anchors_file_sha256`
  matches the live anchors file exactly (`df0cf620…`)
  and its check lists stand at 40/0/8. This is the
  staleness Phase J's as-of label exists to flag; the
  report regenerates at the next foundation run. The
  X1 regeneration was restored to committed bytes, per
  this PR's records-only scope.

## 7. Standing statement

No live claim stands above `checked`. The final
reconciliation (§2c) counts 220 created and 116
checked, and **0 explained, 0 accepted, and
0 digested** — not because the machinery failed, but
because those three stages are lane-2 human outcomes:
a named person's explanation, a human acceptance of
it, and independent engagement with the claim by
people outside the program. Spec 029 built and
CI-gated the machinery that requires those outcomes
before any stage above `checked` can be recorded;
it cannot manufacture them, and it did not. The
105 `verified_unexplained` flags mark the claims that
stand checked but unexplained — the program's
standing risk state, now visible on every surface
that shows a stage.

The script is not deciphered. Nothing in this spec
changed any reading, verdict, or score; it changed
how honestly the program states what its records
have and have not established.

## 8. Deviations (this phase)

- **Worktree source.** The briefed `git clone
  --shared` from the Phase G worktree
  (`~/workspace/glossa-wt-029G`) failed at checkout
  (`fatal: unable to read tree 035a0131…` — a missing
  object in its alternates chain). Per the brief's
  fallback, the worktree was cloned `--shared` from
  the healthy Phase I chain
  (`~/workspace/glossa-wt-029I`), its `github` remote
  repointed at the GitHub URL, and the branch cut
  from the fetched `github/main` at the exact brief
  head `db1c3832`. The resulting tree is main at
  `db1c3832`; only the object source differs. (The
  same fallback is recorded by Phase J for its own
  worktree.)
- **Freeze-test acknowledgment (scope note).** The
  amendment-aware update to
  `backend/tests/test_spec029_freeze.py` (§4) is the
  one file in this PR beyond records and the tick
  pass itself. It is part of the recorded freeze
  amendment — without it, the tick pass `freeze.md`
  §2 prescribes and the required green suite cannot
  both hold, because `tasks.md` is a frozen source in
  this spec. It weakens no assertion: the amended
  test names the amendment's two files exactly and
  fails on any other drift.
- No other deviation. No freeze was regenerated, no
  verdict or stage was changed, no data was changed,
  and no mismatch required smoothing: X1 passed on
  every item as specified.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
