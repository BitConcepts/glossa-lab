# Spec 029 lane-2 adoption — the record of the act (2026-10-13)

## The owner act

The 35 lane-2 drafts in `lane2-drafts/` (explanations and
`not_understood` texts for every live claim in scope) were drafted
by an AI agent on 2026-10-13, shown to the owner in full (the
readable copy, `lane2-drafts/drafts-review.md`), and adopted by
him as authored by him — verbatim, 2026-10-13 06:12 EDT:

> "Adopt all 35 lane-2 drafts as authored by me."

Under OD-2 an explanation counts only when a named, accountable
human authors it in a durable record; an AI may draft and may
never be the named human. The adoption is that human act. The
drafting AI is not the author of any record below, and every
record says so in its `ai_assistance_disclosure`.

## Step 1 — adoption (PR #190, merged `93f4c9aa`)

The authoring fields were completed on all 35 records in
`lane2-drafts/drafts.json`:

- `author`: **Tristen Pierson**; `author_kind`: `human`;
- `drafter`: unchanged — "AI agent (Muse Spark, via Muse)";
- `artifact_uri`: the adopted record itself,
  `…/lane2-drafts/drafts.json` on `main`, with a per-claim
  fragment;
- `content_hash`: the SHA-256 of the record's explanation text
  (the artifact's content, per claim);
- `challenge_venue`: `https://github.com/BitConcepts/glossa-lab/issues`
  — the repository issue tracker, where challenges to these
  accounts are filed and answered (no precedent existed in the
  record for a live value; the Phase B fixtures use an example
  URL, so the program's real venue was used);
- `ai_assistance_disclosure`: restated to record both the
  AI drafting and the owner's adoption.

All 35 completed records validate under
`glossa_lab.claim_bundle.validate_explanation_record`, and every
`content_hash` re-computes from its text. The drafts directory's
README and readable copy were updated from DRAFT-unauthored to
ADOPTED at the same time.

## Step 2 — ingestion (this act; script `ingest_lane2_adoption.py`)

The script writes the adopted records into the live stores,
fail-closed (it refuses a non-adopted drafts file, an invalid
explanation record, a hash mismatch, or a record already
carrying lane-2 text), and applies every stage change through
the Phase B gate layer — `gated_transition_stage`, delegating to
the Phase A transition service, the single writer of stage
changes. Its `--verify` mode re-asserts the whole ingested state
against the frozen ledger and the adopted record; it reports
**VERIFY OK**.

What was written, per claim:

- `not_understood`: the adopted text, on all **35** records;
- `explanation_record`: the completed record, on all **35**;
- stage `checked` → `explained`: **20** records (below);
- `verified_unexplained` stamp cleared: **9** records — exactly
  those whose flag was set and whose explanation took effect
  (the flag's own computation also stops firing at `explained`;
  the two agree);
- the 15 records at `created` keep their stage: explanation
  cannot precede checking, so their authored records sit as
  **authored-pending** on a `created` claim (12), except the
  three Phase-104 fragment claims (3), whose texts were ingested
  but whose stage and evaluation state this act deliberately did
  not touch at all — that correction is a separate act.

### Advanced to `explained` (20)

Extracted claims (8): `farmer_sproat_witzel_2004_manual_001`,
`indus_valley_script_deciphered_from_myth_65ff0a26_manual_002`,
`parpola_2010_dravidian_solution_manual_001`,
`parpola_2010_dravidian_solution_manual_002`,
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001`,
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`,
`yadav_2009_arxiv_manual_001`, `yadav_2009_arxiv_manual_002`.

Study headline claims (10): `STUDY-SPEC-019/PHASE-125`,
`STUDY-SPEC-023/PHASE-132+383`, `STUDY-SPEC-024/F1`,
`STUDY-SPEC-024/F2-HOLDAT`, `STUDY-SPEC-024/F3-ICIT`,
`STUDY-SPEC-025/G1`, `STUDY-SPEC-027/STAGE1-PHASE-392`,
`STUDY-SPEC-028/ARM-A`, `STUDY-SPEC-028/ARM-B`,
`STUDY-SPECS-001-023+PHASES-TO-141`.

Registered predictions (2): `PRED-2026-006`, `PRED-2026-007`.

Flags cleared (9): the two Parpola claims, the two
`without_kings` claims above, the two Yadav 2009 claims,
`STUDY-SPEC-024/F1`, `STUDY-SPEC-024/F3-ICIT`,
`STUDY-SPEC-025/G1`.

### Authored-pending at `created` (12)

`indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`,
`_manual_003`, `_manual_004`;
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_002`,
`_manual_004`, `_manual_005`;
`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`,
`_0002`, `_0003`, `_statisti_0004`;
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001`,
`_sign_val_0002`.

### Phase-104 hold — texts only (3)

`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001`,
`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002`,
`without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001`.

## The resulting live state

Across the Phase D stamped population (336 records; the frozen
ledger's §3 table was 220 created / 116 checked / 0 / 0 / 0 with
105 flags): **220 created / 96 checked / 20 explained /
0 accepted / 0 digested; 96 stamped `verified_unexplained`
flags.** Across the full gated population (344, which also
counts the 8 preserved evidence instances as records of their
own): 226 / 98 / 20 / 0 / 0. On the extracted-claims surface the
computed flag now fires only on the two preserved Yadav 2010
instances — records that are not claims of their own and were
never advanced; their canonical propositions stand explained.

Nothing reached `accepted` or `digested`: those gates require,
respectively, exactly what was supplied here plus the program's
acceptance process, and independent scholarly engagement (OD-5)
— neither exists yet, and the machinery manufactured neither.

## Gates

- **Phase G validators**: trail completeness (G1) and stage
  recompute (G2) pass over the whole live population; the
  provenance partition is now 324 ledger replays + the named 20
  transition-service tails, asserted exactly in
  `test_spec029_phase_g.py`.
- **Full backend suite**: green (1,435 passed / 6 skipped /
  0 failed in the pre-merge local run over this act's content;
  CI re-runs it on the PR). The A2/AEE per-claim score regression
  is byte-identical — lane-1 did not move.
- **Foundation check**: 40 ok / 0 fail / 8 warn ("READY WITH
  CAVEATS") on the program's foundation surface. This act touches
  none of its inputs (the anchors file and the phase reports are
  byte-untouched), so the standing result carries over by
  construction.
- **Append-only discipline**: every advanced record keeps its
  Phase D migration entry as `stage_history[0]`, byte-identical;
  the adoption appended exactly one entry per record. No frozen
  record was edited: the reclassification ledger, the PRED
  register document, the anchors file, and Specs 027–031 records
  are untouched. PRED-2026-001/002/003 were not touched.

## Recorded-expectation amendments (named, dated)

Five test files carried assertions pinning the pre-adoption live
state; the act amended them, each with a dated comment naming
this act and preserving the superseded expectation in prose —
never silently: `test_spec029_phase_a.py` (flag set on the
canonical surface 7 → 0; endpoint flag filter 8 → the 2 preserved
instances; first-page stage provenance partitioned),
`test_spec029_phase_d.py` (stamp partition; reconciliation
against the recorded state; the migration plan now fails closed
on the advanced population, by design), `test_spec029_phase_e2.py`
(live `not_understood` serialization partitioned: authored on the
23 canonical claims, absence form on the 8 instances),
`test_spec029_phase_g.py` (the provenance-partition expectation),
`test_spec029_phase_i.py` (Phase D stamps partition; the merge
itself remains stamp-untouched).

AI disclosure: this act was executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution sec.VI. The explanation texts it ingested were
AI-drafted and human-adopted as recorded above; the drafting AI
is not the author of any explanation record.

## Addendum (2026-10-13): regeneration carry-over defect, caught by CI

The first CI run on the ingestion PR (#197, run 38384800347)
failed one backend test:
`test_spec029_phase_e2.py::test_live_claims_serialize_not_understood_state_and_no_bundle`
— a canonical claim serialized `not_understood` as `None` against
its adopted text. The other six jobs were green. Diagnosis, from
the failed job's own log and a local reproduction on a clean
checkout: `POST /api/v1/indus-evidence/intake/run` (exercised by
`test_indus_evidence_api.py`) queues a background task that
re-runs `glossa-indus/scripts/indus_claims.py` over every
registered document, regenerating the extracted-claims store in
place. That regeneration carries prior record fields over by
claim identity — but the carry-over list predated this act and
did not include `not_understood` or `explanation_record`. The
stage fields survived (a regenerated Yadav record still read
stage `explained` with its full history) while its explanation
record and not-understood text were stripped — an `explained`
claim with no explanation behind it, the exact incoherence the
lifecycle machinery exists to prevent. The local full-suite run
had passed; why the mechanism did not fire there is not
established, and the CI result is the governing evidence.

Fix, in this same PR: the carry-over list in `indus_claims.py`
now includes `not_understood` and `explanation_record`, under the
same rule as the stage fields — a regeneration must never drop
them. `test_spec029_phase_d.py`'s regeneration test now plants
both fields on the prior record and asserts they survive
verbatim. No live record changed: the ingestion's committed
store was always correct; only a regeneration could have
stripped it.
