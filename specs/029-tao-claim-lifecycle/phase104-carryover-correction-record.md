# Spec 029 — Phase-104 Carry-Over Correction Record (2026-10-13)

> A dated, append-only correction to three live extracted-claim
> records, ordered by the owner on 2026-10-13 after the lane-2
> drafting pass (draft PR #190) surfaced the defect. Base:
> main `69f42320`. Tool:
> `specs/029-tao-claim-lifecycle/correct_phase104_carryover.py`
> (dry-run / `--apply` / `--verify`; fail-closed pre-state asserts).
> Tests: `backend/tests/test_spec029_phase104_correction.py`.

## The defect, verified against the primary record

The Phase-104 evaluation of untested extracted claims
(`glossa-indus/reports/phase104_claims_evaluation.json`, "Evaluation
of untested extracted claims"; 21 evaluated, 5 status-changed,
16 stayed untested) defines:

> RULE-DUP: "verdict carried over from an already-adjudicated
> identical proposition"

For each of the three canonical claims below, its entry reads
(verbatim, identical for all three apart from the claim id and the
normalized claim text):

> `"verdict": "status_changed"`, `"new_status": "contradicted"`,
> `"rule": "RULE-DUP"`, `"reason": "Restates the proposition
> already adjudicated as farmer_sproat_witzel_2004_manual_001
> (verdict: contradicted, with cited evidence). Verdict carries
> over."` — with the evidence list: Rao et al. 2009 conditional
> entropy in the linguistic range; Phase-43's 20 TERMINAL_STRONG
> signs; Phase-43's fixed title formula; and the cross-reference
> to the canonical claim.

The carry-over was never written into the live records. All three
still read `claim_status: "untested"` at stage `created` — the
state the Spec 029 retroactive audit then honestly replayed into
the frozen reclassification ledger ("no test outcome recorded").
The ledger is frozen and is **not** touched by this correction;
the correction supersedes its stamp on these three records
through the machinery's own later provenance (below).

## What was written (per claim)

For `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001`,
`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002`,
and `without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001`:

| field | before | after |
|---|---|---|
| `claim_status` | `untested` | `contradicted` |
| `contradicting_evidence` | *(absent)* | Phase-104's evidence list, verbatim (4 items) |
| `status_correction` | *(absent)* | dated note: kind, date 2026-10-13, previous status `untested`, new status, basis ref, rule RULE-DUP, plain-language note |
| `stage` | `created` | `checked` |
| `stage_source` | frozen-ledger stamp | `transition-service:stage_history[1]` |
| `stage_history` | 1 entry (Phase D) | 2 entries — the Phase D entry stands untouched as [0]; the correction appended [1] (`created → checked`, actor `spec029-phase104-carryover-migration`, Phase-104 + canonical evidence refs, plain-language reason) |

The stage move went through the single stage writer
(`glossa_lab.claim_stage.transition_stage`), so the stored stage
recomputes from the record's own history tail under the Phase G
G2 gate. The canonical claim
(`farmer_sproat_witzel_2004_manual_001`) is unchanged. No
falsification condition was added: Phase-104 carried over a
verdict and its evidence, not a falsifier, and this machinery
invents none — the three records' falsifier gap stays visible on
their trails, inside their recorded Phase G baseline.

**The regeneration carry-over (added after the first CI run).**
The extracted-claims store is regenerated wholesale by
`glossa-indus/scripts/indus_claims.py`, and a suite test that
exercises the refresh path does exactly that. The extractor's
carry-over preserved stage fields (Phase D) and merge state
(Phase I) by claim identity, but a claim's status reverted to
the extraction default — which is, in hindsight, how the
Phase-104 outcome was lost in the first place: it was written
to the store, and a later regeneration silently dropped it.
The first CI run of this correction caught the same failure
(the backend job failed on `critique_0002` reading `untested`
after an in-suite regeneration; the local run's warm data
directory had masked it). The correction therefore also extends
the extractor's carry-over: a record carrying a
`status_correction` has its outcome fields (`claim_status`,
`contradicting_evidence`, `status_correction`) carried over by
claim identity — a regeneration must not silently un-correct a
record. The rule is keyed on the correction field, not on any
claim id, and a control test pins that an uncorrected record's
extraction status stands. Verified directly: both documents
were regenerated wholesale against the real store and the
correction tool's `--verify` still passed on all three records.

## Consequences, measured

* **AEE scores.** A score is computed from the record, so writing
  the contradicting evidence moves exactly the three corrected
  claims' scores: band `low → unknown`, propagated score
  `0.289375 → 0.0`, with the engine's "Contradiction penalty
  0.750" note — the same scoring the canonical contradicted
  claim has always carried. The other 20 canonical claims' scores
  are byte-identical. Per the Phase I supersession pattern, the
  Phase A byte-identical pin now targets the successor fixture
  `fixtures/spec029_post_phase104_correction_aee_scores.json`;
  both earlier fixtures are preserved untouched, and the
  correction tests assert the movement set is exactly the three.
* **Stage counts.** Extracted claims: 21 created / 10 checked →
  18 created / 13 checked (live totals across the migrated
  population: 223 created / 121 checked of 344 gated records).
* **Pinned expectations amended, each naming this correction:**
  the Phase D migration pins (the reconciliation now disagrees
  with the frozen Phase D expectations by exactly this movement;
  the migration plan reports exactly the three records as
  "conflict" against the frozen stamp — the tool does not smooth
  the correction over), the Phase I stamp pin (the merge still
  touched no stamp; the correction is a later, separate act),
  and the Phase G provenance expectation (341 ledger replays +
  exactly the three named transition-service tails — the change
  the Phase G record itself anticipated for the first
  transition-service record).

## The named residual (not corrected here)

Phase-104 returned the same RULE-DUP carry-over for
`without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0003`
and `..._critique_0004`. Phase I had already merged those two
records as evidence instances of the first two canonicals above
(identical proposition fingerprints; `merged_into` set). They are
preserved sightings of now-corrected claims, not separate live
claims, and Phase I's invariant — an embedded instance copy
equals its live top-level record — holds only while both copies
stand as preserved. This correction did not rewrite them; their
preserved records still carry the pre-correction stamp, and the
correction tests pin that as a deliberate, visible state. If the
owner wants the instance records annotated as well, that is a
separate, smaller correction of the same kind.

## Epistemic boundaries (H13)

This correction writes a *recorded* evaluation outcome into the
records it belongs to. It is not a new check of the Farmer,
Sproat and Witzel thesis: the underlying checks stand as
Phase-104 cited them (Rao et al. 2009; Phase-43), with the
caution the canonical claim's own record carries — two of the
three contradicting items are the program's own battery on
Mahadevan/ICIT-lineage corpora. Stage `checked` says only that
a lane-1 outcome is recorded; nothing here moves any claim
toward `explained` or above, and `verified_unexplained` stays
`false` on all three (a contradicted status is not in the
supported class). Frozen records (the reclassification ledger,
Specs 027–031 freezes and registers, the PRED register) are
untouched.

## Verification (this branch, before merge)

* Correction tool: pre-state asserts passed; `--apply` wrote the
  two store files; `--verify` passes; re-apply refuses
  (fail-closed, asserted by test).
* Phase G gates over the full live population: G1 completeness
  and G2 recompute pass (the three records audit clean; their
  gap profiles stay within the recorded baseline
  `{actor, falsifier_state}`).
* Full backend suite (CI invocation), locally: **1,450 passed /
  6 skipped / 0 failed** on the corrected tree. The PR's first
  CI run then failed the backend job on the regeneration gap
  described above (a fresh CI data directory regenerates where
  the local warm one did not); the carry-over fix and its two
  tests were verified locally (affected files green; wholesale
  regeneration of both real documents with `--verify` still
  passing), and the PR's CI re-run is the final full-suite
  evidence for the fixed tree.
* Foundation check: **40 passed / 0 failed / 8 warnings**.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson.

## Merge reconciliation with the lane-2 ingestion (appended 2026-10-13)

This correction was written against main `69f42320`. Before it
merged, main advanced through PR #197 (the lane-2 adoption
ingestion), which placed the owner-authored `not_understood` and
`explanation_record` fields on all 35 adopted records — these
three included — and advanced the canonical claim
`farmer_sproat_witzel_2004_manual_001` from `checked` to
`explained`. The correction branch was therefore merged with
current main and reconciled, under three rules: no authored
lane-2 field is dropped; no correction field is dropped; every
pinned expectation that named the pre-ingestion state was
amended to name both acts rather than silently re-based.

The reconciliation, verified field-by-field: on each of the
three records the merged state differs from main's at exactly
the seven correction paths (`claim_status`,
`contradicting_evidence`, `stage`, `stage_as_of`,
`stage_history`, `stage_source`, `status_correction`) and is
identical to main's on the lane-2 fields; every other record in
the two store files is identical to main's, the canonical claim
included. The extractor's regeneration carry-over is the union
of both acts' field sets, so a regeneration now preserves the
correction's outcome fields and the authored lane-2 fields
alike. The pinned expectations were re-derived from the merged
store and measured, not assumed: extracted claims now stand at
18 created / 5 checked / 8 explained (the correction's three on
top of the ingestion's twenty explained); the transition-service
provenance partition is 23 records (20 lane-2 + 3 corrected) of
344; the migration plan reports 310 stamped / 11 conflicts plus
the sidecar difference. Two assertions in this correction's own
test file were amended to the merged state (the corrected
records' exact key set now includes the two lane-2 keys; the
canonical claim's pin now asserts it is untouched *by this
correction* — no `status_correction`, no correction history
entry — its `explained` stage being the ingestion's act), and
one test was added pinning that the correction and the authored
lane-2 fields coexist on all three records.
