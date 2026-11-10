# Spec 091 — commission and grounding record (2026-11-05)

**Commission.** The owner's tap in the Glossa-Lab chat, 2026-11-05:
"Commission wave 1: GR-01, 02, 03" — the first execution wave from the
Spec 088 gap register v1 (ratified as a block by the owner 2026-11-04;
closeout PR #511, merge `c643500b`). Wave 1 = GR-088-01 + GR-088-02 +
GR-088-03 as one spec with three workstreams. GR-088-03's candidate 2
is gated in part on GR-088-04's linguist leg; the dependency is noted
in this package (spec.md W3, claim C091-11, decision D-091-6) and
GR-088-04 is not absorbed — it remains a separate register entry (the
owner authorized a linguist shortlist, no contact, on 2026-11-05).

**Drafting base.** Package drafted on branch `docs/091-wave1-draft`
off main `858f9a6f` (the tip at drafting; main had advanced past the
Spec 089 closeout `27ce5550` by the two preprint-v10 deposit commits).
The register file is byte-identical at `27ce5550` and `858f9a6f`
(SHA-256 `6afda60c006f98677834624ec80e0d6291c60ae0cbca6fdf56d3bd0cde9a7941`,
verified at both commits), so every register citation below holds at
either base.

**Method.** Every factual input was read first-hand from the repo on
2026-11-05; counts marked ✓ were recomputed mechanically from the
cited file during drafting, not copied from prose.

## Factual inputs, cited

### The register entries (glossa-indus/map/gap-register.md)

- **GR-088-01** (headline rank 1; kind: missing edge; scan source B-01).
  "of 184 Parpola comparisons, zero are eligible as independent
  validation"; "116 entries carry the project's own readings copied
  under a 'Parpola 1994' source label (the Phase-96 mechanism)";
  "per-entry primary-source locators have never been recorded."
  Candidate: entry-level locators for all 184 + independent coding by a
  coder who did not derive the project readings. Falsifier (carried
  verbatim into C091-3): "the locator pass finds every entry's reading
  traceable to the project's own derivation → the eligible count stays
  0 and the gap re-registers as structural … not as an unfinished
  task." Owner gates: "an outside coder is an owner act."
- **GR-088-02** (rank 2; kind: thin evidence; scan source A-05). "for
  46 strict anchors, any support line originating outside the program's
  own derivation lineage" is missing; derivation categories for the 46:
  GRAMMAR 20 / DEDR 17 / ICONOGRAPHIC 4 / MIXED 2 / CROSSWALK_CORPUS 2 /
  LITERATURE 1 (sums to 46 ✓). "The strict core's independently
  supported mass is 6 (M044, M047, M124, M202, M329, M330), not 94."
  Candidate: outside-reproduction pass (independent attestation or
  blind re-derivation). Owner gates: "external readers are an owner act
  (named humans; the program's contact rules apply)."
- **GR-088-03** (rank 3; kind: thin evidence; scan source A-06). 37 =
  28 Phase-48 promotions ("the promoting battery carried four
  pass-by-default paths and promoted 30 of 30 tested") + 5 single-line
  (M042, M046, M108 under R5b; M176, M342 under R5c) + 4 crosswalk /
  literature import (R5d: M087, M165, M264, M311). Three candidates
  with their own falsifiers (carried into C091-9, C091-10, C091-12).
  Candidate 2's owner gate: "gated on GR-088-04's linguist leg for the
  phonotactic arm." Candidate 3's: "external sourcing is an owner act."
- **GR-088-04** (dependency only; scan source B-02). The linguist-
  reviewed rule set was never supplied; the corrected checker
  (`phonotactics_v2`) exists; the "zero violations" quantity "was
  withdrawn, not replaced"; candidate 2 of GR-088-03 stands on this
  leg's phonotactic arm.

### The repair brief record (PR #421, 2026-10-26; docs/repair-2026-10-26/)

- README: WP4 delivered `backend/glossa_lab/crosswalk_provenance.py` +
  `backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_provenance.json`
  — "0 comparisons are eligible as independent validation (116 entries
  carry the project's own readings copied under a 'Parpola 1994' source
  label). The original crosswalk file is unmodified." WP5 delivered
  `backend/scripts/repair_anchor_audit.py` generating
  `anchor-support-audit.json` — "No promotion survives as supported;
  three promotions rest wholly on pass-by-default credits." The brief's
  standing rule: historical records preserved byte-for-byte; corrections
  land as new versioned code, overlays, errata — never edits to history.
- baseline-and-dispositions.md, finding 4.2: "A source-by-source pass
  over the 184 crosswalk entries has not been done; the staged file's
  citations are file-level, not entry-level locators." Finding 4.4:
  partial counts in the staged file "(67 of 184 identity-inference-only;
  113 attested by an independent in-repo source) — but attestation of a
  sign pairing is not an independently sourced *reading*, so 113 must
  not be read as the eligible count."

### WP4 provenance classification (mahadevan_parpola_crosswalk_v2_provenance.json) ✓

`summary`: n_entries 184; by_classification — independently_sourced 0,
used_during_candidate_construction 6, project_derived 116, unverified
7, ineligible 55 (sums to 184 ✓); n_eligible_for_independent_validation
0. Source: crosswalk v2.1 (2026-10-05), `mahadevan_parpola_crosswalk_v2.json`,
SHA-256 `3c54ed09b869a504…`. Entry shape (verified on M001): per-field
`source_as_stated`, `locator_present`, `locator` (null on the reading
fields), `value_origin` (`project_anchor_table_copy` on copied
readings).

### WP5 anchor-support audit (anchor-support-audit.json) ✓

audit_id `repair-2026-10-26-wp5-anchor-support-audit`; 94 records.
`summary_counts.overall`: supported_independent 6,
supported_internal_only 46, requires_revalidation 37,
insufficient_evidence 2, expert_adjudication_pending 3 (sums to 94 ✓).
`phase48_promotion_subset` (n 30): requires_revalidation 28,
insufficient_evidence 2, all other classes 0 ✓ (the 2 are GR-088-27's
pair — outside this spec). `strict_core_not_in_phase48` (n 64):
independent 6, internal-only 46, requires_revalidation 9,
expert-pending 3 (M222, M362, M398 — GR-088-14's, outside this spec) ✓.
Cross-check: the 37 = 28 (Phase-48) + 9 (not-in-Phase-48) = 28 + 5
single-line + 4 R5d ✓, matching the register's routing. The 5's and
4's per-record rules verified in the audit records: M042/M046/M108 =
R5b_restored_reading, M176/M342 = R5c_phase48_cited_as_support,
M087/M165/M264/M311 = R5d_sole_crosswalk_or_literature_import, all at
requires_revalidation.
`phase48_summary`: n_medium_tested 30, n_promoted 30;
pass_credits_by_kind — default_credit_missing_model_character 5,
default_credit_too_short 9, exact_match_lexical_plausibility 15,
genuine_bigram_pass_as_recorded_backend_dependent 20,
genuine_positional_pass_reading_blind 30, prefix_match_weak_lexical_
plausibility 6.
Audit inputs include the anchor register `INDUS_FINAL_ANCHORS.json`,
SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
(287 entries; tier counts per the audit's tier_count_check: HIGH 166 /
MEDIUM 5 / LOW 3 / CANDIDATE 113). Program baseline carried from the
standing record: anchors 287 recorded / 94 strict / 44 pending readings
(GR-088-06's population — outside this spec).

### Machinery already in the tree (build inputs, not new facts)

- `backend/scripts/phase48_medium_validation.py` — the historical
  battery (frozen under D-091-4).
- `backend/glossa_lab/phonotactics_v2.py`, `site_stats_v2.py` — the
  repair brief's corrected checkers, with tests
  `test_repair_phonotactics_v2.py`, `test_repair_site_stats_v2.py`,
  `test_repair_crosswalk_provenance.py`.
- Spec 089's run-defs v1 (`glossa-indus/ledger/RUN-DEFINITIONS.md`) —
  every execution this spec produces is a run under it.

## What the grounding could not support (named, not papered over)

1. **Per-anchor checker-arm assignment for the 5.** The register
   states candidate 2's lineage jointly ("phonotactics_v2 /
   site_stats_v2 lineage") and gates "the phonotactic arm" on
   GR-088-04; the audit records' `evidence_tests` for the 5 name
   "distribution" (all 5) and "functional_role" (the R5c pair) but do
   not name which anchors require the phonotactic checker. The package
   therefore asserts no per-anchor arm split; plan task T105 determines
   it from the R5 rule definitions and the full audit records as a
   Stage 1 deliverable, and C091-10/C091-11 are written over the 5
   collectively so they hold under any split.
2. **The exact pass-by-default path enumeration.** The register
   (A-06) says the battery "carried four pass-by-default paths"; the
   WP5 credit census names six credit kinds, exactly two of them
   default-credit kinds. Four paths cannot be derived from the census
   alone (paths and credit kinds are different units; the
   reconstruction in each audit record is the bridge). C091-8 is
   written over paths as enumerated against the frozen battery code,
   and plan task T104 performs that enumeration and reconciles the
   count before battery v2 is specified; if the enumeration finds the
   register's "four" wrong, the correction lands as a register
   amendment, not as a silent edit to this package's grounding.
3. **How WP4's rules extend to locator + coding inputs.** The frozen
   classifier reads the staged file's provenance fields; the rule by
   which a located, independently coded reading changes an entry's
   class is a design act, not a citable fact. Plan Stage 1 produces it
   as the eligibility-defs document under C091-3's constraint (the
   recomputation must be mechanical over the two records), ruled at
   adoption fidelity review — it is machinery under a ratified claim,
   not a new owner decision, and any extension that would change a WP4
   class definition (rather than apply it) returns to the owner.
4. **The 46's and 37's full membership lists are cited, not
   reproduced.** They exist in full in anchor-support-audit.json's 94
   records and their class counts were recomputed at drafting (✓
   above); the package names only the subsets the register itself
   names (the 6, the 5, the 4). No claim depends on a list this record
   does not point to.

**AI disclosure:** drafted by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution §VI.
