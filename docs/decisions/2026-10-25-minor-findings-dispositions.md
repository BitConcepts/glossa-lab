# Batch record — 2026-10-25: disposition of the red-team minor findings (road-to-decipherment plan, Step 7)

**Scope.** The ten minor findings of the 2026-10-24/25
red-team attack that Step 7 of the road-to-decipherment plan
assigned to this batch: RT-18, RT-19, RT-20, RT-21, RT-22,
RT-23, RT-24, RT-25, RT-31, RT-32. RT-16 is not in this
batch (already dispositioned; not reopened). Nothing in
this batch changes any verdict, status, or frozen text;
every record change is a dated append of 2026-10-25, in
the programme's append-only form. For Spec 072, the Roif
discipline is absolute throughout: this batch writes no
result content and no verdict word for that study anywhere;
its surfaces stand in the gate's permitted form ("executed
— held under the Roif gate") under the owner's 2026-10-25
realignment decision.

**Base.** main at `a462f7b5` (PR #388 merge), fresh clone
for this step. All evidence below was read first-hand in
this act.

## Dispositions

| Finding | Disposition | What landed where | Evidence |
|---|---|---|---|
| RT-18 (072 outcome cites a file that does not exist) | DISPOSITIONED — overtaken by the redaction; no append | Nothing. The wrong-pointer sentence no longer exists on the public record, so there is nothing to correct by append. | Current `specs/072-fish-family-profiles-redesign/outcome.md` on main is the 2026-10-25 redacted record (Roif gate permitted form); a repo-wide grep for `phase431_nonfish_distribution.json` returns no occurrence anywhere. The pointer was removed by the RT-26 redaction, not by this batch. |
| RT-19 (074's S-B sensitivity vacuous) | FIXED (record append + standing rule) | Dated addendum appended to `specs/074-hunt-opening-signs-repaired-surface/outcome.md` (post-freeze note surface — see the relocation note below): records the vacuity (the "unicorn" label of Spec 069's attestation never entered Asset A v2's columns, so S-B could only return not-applicable) and adopts the standing rule — at any future asset rebuild, assert every frozen sensitivity label exists in the new table's vocabulary before freeze, with the result recorded in the build record. | Outcome record's own S-B lines (not applicable; gate 0.5 unicorn naming scan returns no sign); adjudication §6's drafting note (nothing at drafting turned on the label; the not-applicable branch was carried). |
| RT-20 (054's digest-covered §§9.2/9.5 still say Phase-437) | FIXED (pointer append) | Dated pointer addendum (§9.11 in the adjudication's numbering) appended to `specs/054-yadav-opening-closing/outcome.md`, pointing single-section readers of the adjudication to its §9.9 (the Phase-437 → Phase-438 reassignment). The digest-covered text itself is not edited. | §9.9's text (allocation at §§9.2/9.3; reassignment recorded there); the execution in fact ran as Phase-438 (`reports/phase438_results.json`). |
| RT-21 (Yadav + Hunt claims' `not_understood` fields stale) | FIXED (refresh + dated refresh keys; regeneration-safety proven) | `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json`, claim `yadav_2009_arxiv_manual_002`: `not_understood` refreshed (the falsifier was appended at the Spec 054 amended freeze, 2026-10-23; the test froze and closed UNEXECUTED at step 0, STRICT CORPUS NOT PINNABLE, corpus not pinnable — claim untouched, strongly_supported, falsifier carried, execution awaits the corpus layer's recovery) + dated key `spec054_not_understood_refresh_2026_10_25`. `glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json`, claim `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`: `not_understood` refreshed (the animal test ran as Spec 074 / Phase-440 on the repaired surface; the refreshed text carries only what the merged outcome record states, with its containment — internal restatement of the claim, one compilation (Shakti), ICIT numbering) + dated key `spec074_not_understood_refresh_2026_10_25`. No status, stage, or falsification condition changes in either file. | The claims' own dated appends (`spec054_falsifier_append_2026_10_23`, `spec054_outcome_append_2026_10_24`, `spec074_outcome_append_2026_10_24`) and the two outcome records. Regeneration-safety: both refresh keys match the generator's dated-append carry-over pattern (`^spec\d{3}_.+_\d{4}_\d{2}_\d{2}$`, glossa-indus/scripts/indus_claims.py, the widened carry-over of 2026-10-25) and `not_understood` is in the generator's fixed carry-over list; `backend/tests/test_indus_claims_carryover.py` passes against the edited store (2 tests, including the real yadav_2009_arxiv regression case), as do the regeneration-preservation tests in the Spec 052/054/074 execution test files. No regeneration was committed. |
| RT-22 (preprint "independent" in two senses) | DISPOSITIONED — no repo change | The fix is queued verbatim in the v9 journal-readiness checklist (goal record `2026-10-25-v9-journal-readiness.md`, item B7): where v9 calls the linguistic and distributional routes "independent lines of evidence," it adds the clause *independent of each other as methods; both rest on the single-lineage corpus of §6*. | Checklist item B7, state "REQUIREMENT RECORDED," read first-hand in this act. The preprint itself is not edited by this batch. |
| RT-23 (074's verdict travelling without containment) | DISPOSITIONED — verified in substance, one element a gap (see note) | No repo change; the daily article is a dated published record and is not edited by this batch. Verification recorded here; the v9 side was already recorded in the readiness checklist (item B6). | The 2026-10-25 daily article (see the RT-23 note below). |
| RT-24 (orphaned OSF draft 39vkd for Spec 073; missing `osf-spec-registration.md`) | DISPOSITIONED — record file landed; withdrawal flagged as an owner UI act | `specs/073-keying-surface-repair/osf-spec-registration.md` landed as a dated record file naming the approved registration 9kh4a (DOI 10.17605/OSF.IO/9KH4A) and the orphan draft 39vkd with its disposition. 9kh4a was not touched. | API read-back 2026-10-25: 9kh4a `reviews_state: accepted`, public, DOI verified via its identifiers endpoint, freeze digest in its study-design answer. Withdrawal: the OSF connector doc documents no operation for deleting a never-submitted draft registration (its CLI offers create/patch/submit/register for drafts; the only DELETE it records is for files via files.osf.io), so no improvised deletion was attempted; read-back under the programme credential returns 404 for both the draft-registration and registration routes for 39vkd, it appears in neither the account's registrations listing nor node nrb9u's drafts, and the GUID resolves to an unrelated user record. **Withdrawal of 39vkd requires an OSF UI act by the owner** — annotated here and in the record file. |
| RT-25 (declared environment cannot reproduce the statistics) | FIXED (scientific stack pinned) | `backend/requirements.txt` created, pinning the imported scientific stack: `numpy==2.5.3`, `scipy==1.18.1`, `pandas==3.0.6`, with a header recording the provenance of each pin. (The file did not exist on main; the declared environment is `backend/pyproject.toml`, which carried numpy only as a range and scipy/pandas not at all.) | Grep of `backend/`: numpy imported in 72 files, pandas in 26, scipy in 11 (including the statistics-bearing execution/analysis scripts). Environment of record: the programme venv (`~/workspace/venvs/glossa-lab`) carries numpy 2.5.3 and **no scipy and no pandas** — the absence is the gap RT-25 names. The desktop execution environment of record for Spec 062 ran NumPy 2.5.3 / SciPy 1.18.1 (Spec 062 outcome record) — the scipy pin's source. A second environment's versions are on the same record: the drafting machine ran NumPy 1.26.4 / SciPy 1.11.4, expressly not the execution environment of record. Pandas: no glossa execution of record imports it (the Phase-430…440 scripts do not); 3.0.6 is the only pandas version installed in any workspace venv at the pin date, and the header says so. This pinned environment is the outcome-records note for RT-25: future outcome records should name the pinned stack in `backend/requirements.txt` as the declared environment. |
| RT-31 (073 outcome bullets truncate the Parpola placements) | FIXED (dated correction append) | Correction append of 2026-10-25 appended to `specs/073-keying-surface-repair/outcome.md`, giving the five complete placements; the truncated bullets stand unedited above it. | Verified first-hand against `reports/phase436_results.json` (M2_five_named_signs, `catalog_section_2_5_placement`) in this act: 136 → Parpola (1994) sign 6; 298 → 217; 401 → 107; 617 → 272; 824 → 373. |
| RT-32 (052's `total_occurrences` ≠ N, semantics undocumented) | FIXED (field definition added to the results JSON — the unpinned route) | `field_definitions` entry added to the header area of `reports/phase437_results.json` (in the file's own sorted-key form, between `execution` and `gates`), defining the per-sign fields from the execution code — in particular: `total_occurrences` counts the sign's occurrences in **all** sequences of the population, of every length, while `N` counts only occurrences in sequences of length ≥ 2 (NB-1.2/NB-1.3), so `total_occurrences − N` is exactly the sign's occurrences in length-1 sequences, and every rate is count / N. No executed value changed. | Pin check: the results file's SHA-256 is `2cc28aca6b5d7e5a6e10ee31cace1a78b93412bd6993a54e1755241db88f0478`; that hash occurs **nowhere** in `specs/052-*`, in any freeze record, or anywhere else in the tree — the file is not hash-pinned, so the definition went into the JSON rather than into an outcome append. Semantics derived from the code, not paraphrased: `backend/scripts/phase437_farmer_nb1_shakti.py`, `_battery()` — `total_occ = Counter(...)` over the full sequence list; `n_cnt` updated over `seqs_ge2` only. Numeric tie-outs recomputed in this act: the per-sign differences sum to the census length-1 counts in both populations (primary 103; sensitivity 838), I + T + M = N for every sign, and sign 540's recorded instance (total 22, N 13) matches the census_notes remark. |

## RT-23 note — the daily article's containment, verified element by element

Article: `2026-10-25-spec-074-hunt-opening-signs-not-supported.md`
(daily article of 2026-10-25, programme research-notes series),
read in full in this act. The containment RT-23 requires has
three elements:

- **One compilation (Shakti) — carried.** The article states
  the two lists are "both drawn from the same graded
  compilation of inscriptions, called the Shakti corpus in
  the record," and again: "The test was run against one
  compilation's position framework. It does not test the
  claim against the program's earlier position framework."
- **ICIT numbering — carried in lineage form.** The article
  states the compilation "belongs to one published corpus
  tradition, the ICIT lineage: agreement between it and the
  program's earlier layer from the same tradition is
  consistency within one tradition, not independent
  confirmation from separate material," and notes the rows'
  CISI numbering. It does not name ICIT as the numbering
  system of the test's sign list in so many words.
- **Internal restatement — GAP (implicit only).** The
  article frames the tested claim as a published reading,
  cites it by its record id (`…_manual_003`), and qualifies
  its verdict sentences with "in the form the test stated" /
  "in the form this test stated" — but it nowhere states
  that the tested form is the programme's own internal
  restatement of the Hunt claim. A reader quoting the
  article alone would not learn that element of the
  containment from its text.

The article is a dated published record; this batch does
not edit it. Any repair of the internal-restatement element
is a separate owner-visible act, flagged here and in the
Step 7 report. The v9 side of RT-23 is already recorded
(readiness checklist item B6: any Spec 074 mention carries
its containment).

## Relocation note — the RT-19 and RT-20 appends stand in the outcome records, not the adjudications

This batch's dispositions for RT-19 and RT-20 were first
landed as dated appends to the two specs' adjudication
records. That placement cannot stand, on evidence read
first-hand in this act: each adjudication.md is a
digest-covered frozen source — its SHA-256 stands in the
spec's freeze.json, and the freeze-replay tests
(`test_spec054_freeze.py` / `test_spec074_freeze.py`,
`verify_freeze`) fail on any changed byte. Appending there
would change frozen text, which this batch's own rules
forbid, and the batch's first CI run confirmed it (run
40217946870: Backend tests failed; the same two replay
tests fail locally on the appended tree and pass on clean
main). The appends were therefore moved, text preserved,
to the specs' outcome records — the programme's established
surface for post-freeze dated notes (the RT-27 correction
note in Spec 074's outcome record, landed 2026-10-25 in
PR #377, is the nearest precedent) — and the adjudication
files stand byte-identical to their frozen pins
(Spec 054: as frozen; Spec 074: SHA-256
`4e6d6f818e4a515f62631aec296321b0d8c057615e9bfc91e7bc53649db15e05`,
recomputed in this act). The RT-20 addendum keeps its
§9.11 number, recorded in the outcome record as §9.11 in
the adjudication's numbering.

## What this batch does not establish

No verdict, status, stage, or frozen text is changed by
anything in this batch; no execution was run; the OSF
orphan draft still exists (its withdrawal is an owner's UI
act, flagged above, not performed here); and the RT-23
internal-restatement gap in the daily article stands
unrepaired by design, pending a separate owner-visible act.

---

*AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution §VI.*
