# Spec 029 — Phase I Record: Claim-Store Deduplication (D-B)

> Phase I of `tasks.md` (D-B; plan §2.6; after D6). Base:
> main `f8da5eaf` (Phase H merged as PR #175). Branch:
> `impl/029-phase-i-db`. Date: 2026-10-12.
>
> D-B (ratified 2026-10-12, `adjudication.md` addendum):
> deduplicate by proposition — merge, never delete; guard
> the intake. The unit of repair is the 2026-10-09
> extraction batch: 31 records in
> `glossa-indus/claims/extracted_claims/*.json` (10
> documents), Phase-D-stamped. Where `tasks.md` Phase I
> and the phase instructions differed in summarisation,
> `tasks.md` governed.

## Recovery note (2026-10-12, recovery worker)

The original Phase I worker's session died on a runtime
infrastructure fault ("background exec disappeared")
with the implementation complete but uncommitted. This
recovery worker forensically verified the uncommitted
work rather than re-implementing or blindly trusting it:

- The merge tool was re-run live in a scratch tree
  against a pristine checkout of base `f8da5eaf`'s store
  (the pre-run snapshots were also byte-compared against
  `f8da5eaf` — all 10 files match). The scratch merge
  output is byte-identical in substance to the found
  worktree store: the only differences were the volatile
  `extracted_at` / `extraction_date` timestamps refreshed
  by the prior worker's final test run (2026-10-12
  18:24). The store was restored to the exact verified
  merge bytes before committing, and is restored again
  after every test run in this recovery.
- The batch-4 claims report's found diff was only a
  regenerated `batch_id` / `timestamp` pair (test-run
  noise, not merge output) — reverted to base bytes.
- Counts, the five groups, the Zipf pair, stage stamps,
  and score movements were recomputed independently
  (see §I3): 31 store records → 23 canonical claims,
  8 evidence instances; every surviving score
  byte-identical to the Phase A pre-change fixture;
  mean 0.484903 → 0.497641, composition only.
- The substantive findings below are the original
  worker's, verified as above and unchanged.

## I1 — Fingerprint + inventory

**Definition (frozen in this phase).** The proposition
fingerprint is the SHA-256 hex digest of the normalised
claim text (the record's `normalized_claim`), computed by
`backend/glossa_lab/proposition_fingerprint.py`
(rules version `spec029-phase-i-v1`):

1. Unicode NFKC normalisation, then case-folding.
2. Every character that is not a Unicode letter or digit
   is replaced by a single space — this subsumes
   whitespace normalisation (spaces, tabs, and the
   newlines extraction snippets carry mid-phrase) and
   punctuation normalisation (`Zipf-Mandelbrot` ≡
   `Zipf Mandelbrot`; `Indus-Script` ≡ `Indus script`).
3. Split on whitespace, re-join with single spaces.

The fingerprint is a function of the proposition text
only — not of source document, status, stage, or
evidence. Every one of the 31 records now carries its
fingerprint in a `proposition_fingerprint` field.

**Inventory result.** 31 records → **23 unique
propositions, 5 duplicate groups (8 surplus records)** —
more than the audit's two known propositions, as
`tasks.md` I1 anticipated ("further collisions are
reported, not silently absorbed"). All 5 groups:

| # | Fingerprint (first 16) | Proposition (normalised) | Canonical (fuller trail; ties → scan order) | Evidence instances |
|---|---|---|---|---|
| 1 | `fdd32acf462bf2d9` | Indus script sign frequencies follow a Zipf-Mandelbrot distribution | `yadav_2009_arxiv_manual_001` | `yadav_2010_ngrams_manual_001` |
| 2 | `c5d0f0575c8378b1` | There are specific text-beginning and text-ending signs in the Indus corpus | `yadav_2009_arxiv_manual_002` | `yadav_2010_ngrams_manual_002` |
| 3 | `a4874349e0cc0ba2` | Statistical finding: Positional Analysis | `ancient_writing_and_modern_technologies_51831ac9_statisti_0004` | `fuls2023_…_statisti_0001`, `positional_analysis_…_statisti_0001`, `the_archaeology_…_statisti_0003`, `without_kings_…_statisti_0002` |
| 4 | `defa7480501b2b45` | Critique: Myth of a Literate Harappan | `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001` | `without_kings_…_critique_0003` |
| 5 | `d7e4efd6b7748029` | Critique: Collapse of the Indus-Script Thesis | `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002` | `without_kings_…_critique_0004` |

Corroboration: the frozen reclassification ledger flags
exactly groups 1–3's instances `duplicate_record` (the
Yadav 2010 pair and the four positional-analysis
surplus records) and never flags a canonical selected
here. Groups 4–5 are fingerprint-identical after the
frozen normalisation (their raw texts differ only in
case, a mid-phrase newline, and a hyphen — extraction
artifacts of the same Farmer et al. phrases) and so are
the same proposition under the phase's definition; the
ledger did not flag them, which is recorded here as the
scan going beyond the audit's minimum, per I1.

**Canonical selection.** "The fuller trail wins"
(tasks I2): trail richness = count of populated fields
among `falsification_condition`, `glossa_lab_evidence`,
`contradicting_evidence`, `quote_fragment`, `author`,
`signs_involved`, `sign_ids`, `proposed_value`,
`proposed_language`, `required_data`. Group 1's
canonical wins outright (2 vs 2 fields — falsifier +
Glossa evidence — tie broken by scan order; the two
records are otherwise identical). All other groups tie
on richness (identical record shapes) and resolve by
store scan order (sorted file name, then position) —
which in every group selects the record the ledger did
*not* flag as the duplicate.

**Pairs reviewed and NOT merged** (fingerprint-distinct;
merging them would need a semantic judgment the frozen
fingerprint does not license):

- `ancient_writing_…_sign_val_0002` ("700 / a volumetric
  system with a unit of 40") vs `…_sign_val_0003`
  ("700 / a unit of 4") — the highest token similarity
  of any non-colliding pair (Jaccard 0.55), and
  materially different propositions (different units).
- `farmer_sproat_witzel_2004_manual_001` (the full
  non-linguistic-symbols claim) vs
  `without_kings_…_language_0001` ("Language hypothesis:
  non-linguistic symbol") — same thesis family, but one
  is a full claim and the other an extraction label
  fragment; different proposition texts.
- `parpola_2010_…_manual_002` (fish sign = primary
  rebus sign) vs `indus_valley_…_manual_002` (fish sign
  = coastal guild controller) — same sign, different
  proposed values; rival propositions, not duplicates.
- `without_kings_…_manual_003` / `…_manual_004` (faunal
  prefixes; celestial suffixes) vs `without_kings_…
  _manual_001` — components of the tripartite-grammar
  claim's falsifier, but distinct propositions in
  their own right.

## I2 — Merge (never delete)

Writer: `specs/029-tao-claim-lifecycle/
merge_phase_i_dedupe.py` (dry-run → live with pre-run
snapshots at `~/workspace/glossa-wt-029I-snapshots/
phase-i-pre-run-2026-10-12/`, outside the repo; the
identical pre-merge bytes are also main `f8da5eaf`'s
state of the store). Mechanics, per record:

- **Nothing is deleted.** All 31 records remain in
  their own document files with every pre-existing
  field byte-preserved (asserted by the tool before
  writing: removing exactly the Phase I keys —
  `proposition_fingerprint`, `merged_into`,
  `evidence_instances` — from the merged data
  reproduces each file's pre-merge canonical bytes).
- Each instance record gains `proposition_fingerprint`
  and `merged_into` → the canonical claim id.
- Each canonical record gains `proposition_fingerprint`
  and `evidence_instances`: one entry per instance with
  its claim id, source document id, source file, and a
  **full copy of the instance record as stamped by this
  merge** — the instance is preserved verbatim on the
  canonical claim and stays resolvable in its own file.
- **Phase D stamps preserved.** No merge key touches
  `stage`, `stage_source`, `stage_as_of`,
  `stage_history`, or `verified_unexplained`, on
  canonicals or on instances (each instance retains its
  own stamped stage and history as part of its
  preserved record, per plan §2.6). Stage outcomes per
  group: groups 1–2 — canonical `checked`, instance
  `checked` (both Yadav records were ledger-staged
  `checked`; the canonical keeps its stage, the
  instance keeps its own; no stage was raised, lowered,
  or transferred); groups 3–5 — canonical `created`,
  instances `created`. Verdicts/statuses untouched
  everywhere.
- **Falsifiers.** Group 1: both records carried the
  identical falsifier ("If frequency distribution
  deviates from Zipf-Mandelbrot law.") — the canonical
  keeps it. Group 2: **neither** record carried a
  falsifier, so the canonical honestly carries none —
  no falsifier was invented (the audit's 17/31
  no-falsifier finding stands as recorded; repairing
  it is not this phase's scope). Groups 3–5: no
  instance or canonical carried one; none invented.
- **Wording.** No claim text was rewritten. Where the
  two records of a proposition worded it differently
  (groups 3–5: case / newline / hyphen variants), the
  canonical keeps its own wording verbatim and the
  instance's wording is preserved verbatim in the
  instance record (in its file and in the canonical's
  embedded copy).
- Idempotency: a second `--live` run reports "store
  already merged per plan; nothing written" (verified);
  `--verify` recomputes fingerprints, pointers, and
  embedded-copy equality from the live store — clean.
  Post-merge SHA-256 per store file is in the run
  output reproduced in the phase PR description's
  record (tool `--report`).

**Post-merge counts.** Store records: **31** (nothing
deleted). Canonical claims: **23**. Evidence instances:
**8**. Document files' `total_claims` fields are
unchanged (they count records per file, and the
records are all still there).

`GET /claims` still lists all 31 store records — the
instances now visibly carry their `merged_into`
pointer; display-phase surfacing of canonical-only
views is Phase E scope, not this phase's. The scored
surfaces (`GET /claims/aee-scores`, `assessment_summary`)
operate on the 23 canonical claims (I3).

## I3 — Origin-group counting + score movement

**Wiring.** `backend/glossa_lab/aee_core.py`:
`claims_from_record` (and therefore
`load_claims_from_dir` / `assessment_summary`) skips a
record carrying `merged_into` — an evidence instance
is not a claim and must not enter the graph. The
canonical record's `evidence_instances` are preserved
records, surfaced in `Claim.metadata` as instance
claim ids, and are **not** converted into AEE
Evidence: converting them would re-create the double
count. Test evidence: the canonical Zipf claim
carries exactly 2 Evidence items (the Yadav 2009
source assertion + Glossa's Phase-43 test); the
identical Phase-43 evidence on the 2010 instance is
counted **once** (pre-merge it was counted on two
records, each scoring 1.0).

**Score movement (I4 of the phase instructions;
in-depth numbers rule).** Recomputed over the
post-merge set with the Phase A fixture
(`spec029_pre_change_aee_scores.json`, preserved
untouched) as baseline:

- **Every surviving claim's score is byte-identical**
  to its pre-change value — all 23 canonical claims,
  verified dict-for-dict (and under canonical JSON
  serialization) against the fixture. No claim was
  re-scored; the merge changes *which records are
  claims*, not any claim's evidence.
- The 8 records that left the scored set, with their
  pre-change scores: Yadav 2010 Zipf **1.0**; Yadav
  2010 text-begin/end **0.85**; the four surplus
  positional-analysis records and the two surplus
  critique records **0.289375** each. Removed score
  sum: 3.58625.
- **Mean `mean_propagated_score`: 0.484903 (31 claims,
  sum 15.031999) → 0.497641 (23 claims, sum
  11.445749).** Cause, stated plainly: pure composition.
  The removed set's own mean was 0.448281 — below the
  overall mean — so removing the double-counted
  records *raises* the program mean even though the
  two highest-scored duplicates (1.0, 0.85) also left.
  The mean is a lane-1 diagnostic over a changed
  population, not a claim that anything got better;
  the per-claim truth is "no score moved".
- Status counts on the scored surface change by the
  same composition: `strongly_supported` 4 → 2 (the
  Yadav 2010 pair), `verified_unexplained` flagged
  claims 9 → 7. The store-side counts are unchanged
  (the instances retain their statuses in the store).
- A successor fixture,
  `backend/tests/fixtures/spec029_post_merge_aee_scores.json`
  (23 claims), is added; the Phase A regression test
  now pins against it, with the supersession cited in
  the test. The pre-change fixture is byte-untouched.

## I4 — Intake gate

`glossa-indus/scripts/indus_claims.py` (the store's
writer): `process_document` now, after the Phase D
stage carry-over (extended in this phase to also
carry `proposition_fingerprint`, `merged_into`, and
`evidence_instances` by claim identity, so a
regeneration cannot un-merge a proposition), runs
`assert_no_duplicate_propositions` over the incoming
claims against the whole existing store **before any
write**:

- Fingerprints are computed from record text (never
  from a stored fingerprint field), grouped with their
  member claim ids and canonical id.
- A claim passes iff its fingerprint is new, or the
  claim is already a recorded member of that
  fingerprint's group (itself the canonical, or a
  merged instance of it) — the wholesale-regeneration
  case, which recreates the same claim ids and must
  not collide with itself.
- Any other collision raises
  `DuplicatePropositionError` naming **both** records
  (incoming claim id, existing canonical claim id, and
  the fingerprint): intake stops, nothing is written
  for that document.

Test evidence (both directions, discriminating):
planted Zipf duplicate with altered casing/punctuation
under a new claim id → refused, error naming both
records, and the document's file is not written
(end-to-end through `process_document`); distinct
proposition → accepted and written; regeneration of a
known group member → accepted; regeneration preserves
merge state by claim identity. The full backend suite
additionally exercised the gate end-to-end in CI
conditions: the intake-pipeline test re-ran extraction
over all registered documents against the merged store
(17 documents, 31 records) with no collision raised and
the merge intact afterwards.

## I5 — Phase gate

Filled at gate time by the recovery worker (2026-10-12;
see the recovery note at the top of this record). The
branch was integrated with current main before the gate:
main had moved to `09589443` (PR #177, Spec 030
Phase-394 infrastructure — disjoint file surface except
a LEDGER.md append, which auto-merged cleanly with both
entries preserved), merged as `e1f5aed3`.

- **Foundation check** (`backend/scripts/
  foundation_check.py`, Holdat CSVs present in the
  worktree as in prior phases, never committed):
  **40 passed / 0 failed / 8 warnings** — identical to
  the pre-Phase-A baseline; no new warnings.
- **Full backend suite** (CI-identical invocation:
  `python -m pytest tests/ --tb=short -q
  --ignore=tests/test_pipelines_gpu.py
  --ignore=tests/test_install_gpu.py` in `backend/`,
  per `.github/workflows/ci.yml`): **1256 passed,
  6 skipped, 0 failed** in 1h25m19s (Phase H's gate:
  1227 passed / 6 skipped; the +29 are this phase's
  18 new tests, the integrated Phase-394 tests, and
  one further integrated test). The run was unusually
  slow because the VM was heavily loaded (load average
  12–17 throughout; single recomputation tests took
  tens of minutes of wall time while steadily
  accumulating CPU) — no test was skipped or altered
  for speed. An orphaned pytest process from the
  original worker's session (started 18:21, stalled in
  the same recomputation region, sharing the test-data
  directory) was found and killed before this gate run
  so the gate ran alone. Targeted run before the gate:
  Phase I + Phase A suites, 49 passed.
- **Store bytes.** After the suite, the extracted-claims
  store was restored to the exact verified merge bytes
  (see the recovery note) and the merge tool's
  `--verify` re-run clean: 31 records, 23 canonical
  claims, 8 evidence instances, 5 groups, no problems.
  The batch-4 report and `outputs/` files touched by
  test-run regeneration were restored to committed
  bytes; `frontend/dist/index.html` (pre-existing CRLF
  phantom) was never staged.
- **Branding / attribution sweep** over authored and
  edited files: no stray branding; the Phase I authored
  files name no external scholar (pre-existing spec
  naming and already-pushed history are untouched, per
  standing record discipline).

## Deviations and honest limitations

- **More merges than the audit's minimum.** The
  audit named two double-recorded propositions; the
  frozen fingerprint finds five groups. Groups 4–5
  (the critique pairs) are the judgment call closest
  to the line: their raw texts differ (case, a
  mid-phrase newline, a hyphen), and every difference
  is inside the normalisation classes the fingerprint
  definition froze *before* the scan (case /
  whitespace / punctuation) — under that definition
  they are textually identical, and leaving them
  unmerged would leave the store violating the
  one-canonical-claim-per-fingerprint invariant the
  intake gate now enforces. Recorded here, not
  silently absorbed (tasks I1).
- **Phase A / Phase D test supersessions.** Two Phase
  A assertions pinned the pre-merge claim set
  (byte-identical regression over 31 claims; the
  scored-surface flag count 9). Both are updated to
  the post-merge set with the supersession cited in
  the test; the pre-change fixture is untouched, and
  this phase's tests assert per-claim score identity
  against it. Phase D's tests required **no** change:
  all 31 records remain in the store with their stamps
  intact, so the ledger-vs-live reconciliation
  (31 extracted claims, 21 created / 10 checked) still
  matches exactly.
- **Test-run side effects (house gotcha).** Backend
  test runs regenerate `extracted_at` timestamps (and
  the batch-4 report) via the intake pipeline. After
  every local test run the store files were restored
  to exactly this merge's committed bytes (verified
  against the merge tool's post-merge SHA-256 set);
  the batch-4 claims report was restored likewise. In
  CI, an in-suite regeneration preserves fingerprints,
  pointers, instances, and stamps via the extended
  carry-over, changing only the pre-existing volatile
  timestamps. One consequence, stated plainly: the
  embedded instance copy on a canonical record is the
  record **as merged**; a later regeneration refreshes
  the live instance's `extracted_at` (the store's one
  volatile field), so the merge tool's `--verify` and
  this phase's verbatim-preservation test compare the
  embedded copy against the live record with exactly
  `extracted_at` excluded — every other field must
  match byte-for-byte.
- **Anchors untouched.** The diff does not touch
  `backend/reports/INDUS_FINAL_ANCHORS.json`, the PRED
  register, or any frozen design source.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
