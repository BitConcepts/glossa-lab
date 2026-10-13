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
* Full backend suite (CI invocation): **1,450 passed / 6 skipped
  / 0 failed**.
* Foundation check: **40 passed / 0 failed / 8 warnings**.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson.
