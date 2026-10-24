# Spec 052 — Freeze Record — 2026-10-23

> ## FROZEN — 2026-10-23
>
> Frozen at the freeze act of 2026-10-23 under the
> owner's mini-gate approval of the same day
> (2026-10-23, 22:59 EDT, "Approve both mini-gates
> as specified"; recorded in `adjudication.md`
> §10). The AEE lifecycle hooks ran **first**, at
> the freeze gate (tasks L4, per DD-038-10), over
> the claim register recovered in three rounds at
> the freeze (0.5-draft → 0.8-draft); the freeze
> digest (`freeze.json`) was computed over the
> recovered register and the finalised freeze
> texts **exactly once**. The OSF registration
> for the frozen spec was filed at the freeze
> under campaign decision E-1; it is recorded in
> `osf-spec-registration.md` (completed by append
> after filing). **This freeze executes nothing.**
> Execution (Phase-437) requires a separate owner
> order, and does not begin while the
> registration's approval is pending.

## 1. Basis

Spec 052 is design D-01's arm A as drafted
2026-10-21 (PR #249): a consistency check of
Farmer, Sproat & Witzel's "not writing" thesis on
the Soviet compilation, under the Phase-43
positional battery. Its freeze attempt of
2026-10-21 **failed** at gate 0.5 — BATTERY NOT
PINNABLE: the Phase-43 battery cannot be
reconstructed from the record that survives, and
the Soviet mapping the design required cannot be
built from the records the program holds
(`adjudication.md` §8). The owner's settled
rulings of 2026-10-23 (§9) closed both questions:
no battery element may be invented or borrowed
under the Phase-43 name, and arm A as designed is
closed, its Soviet tables retired from the
member. The amendment (`amendment.md`) is the
route those rulings adopted: a new battery, NB-1,
defined in full; the data re-scoped to the Shakti
corpus layer; amended step-0 gates A–D; and the
§4.1 outcome words re-pointed at the new battery
and population. The owner approved the amendment
as specified at the mini-gate of 2026-10-23
(§10.1). **Where the unamended draft and the
amendment disagree, the amendment and this record
govern**; the draft's text stands unrewritten as
the record of the closed design.

## 2. Owner rulings at the freeze

The mini-gate approval (§10.1) carries the three
decisions of `amendment.md` §7, as there written:

1. **NB-1 as specified** — the battery of
   `amendment.md` §3 is the amended run's battery,
   every constant with its derivation or its
   labelled basis (claim F052-C16).
2. **Shakti re-scope** — the data are the Shakti
   corpus layer as `amendment.md` §4 states it,
   in the layer's own numbering and segmentation,
   in the restricted local venue, with the
   corpus-layer pins taken at freeze (claim
   F052-C17).
3. **Amended gates and outcomes** — step-0 gates
   A–D of `amendment.md` §5 replace the draft's
   Soviet gates and closure classes (claim
   F052-C18), and the outcome semantics of
   `amendment.md` §6 govern the amended run
   (claim F052-C19), the Soviet tables retired
   with them.

The approval is of the freeze path
(`adjudication.md` §9.4). It is not an execution
order.

## 3. Step-0 pins, taken at the freeze

Re-asserted at the freeze against the merged
record as it stands (the draft branch, forked
from main on 2026-10-21 at 83b6a563, was brought
current by merging main at the freeze act, so
these pins speak of the record that includes the
Specs 068–073 freezes and the Spec 041
execution):

| Pin | Value at the freeze |
| --- | --- |
| Shakti corpus layer (`sanitized_corpus.json`, restricted-local, never in git) | SHA-256 `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`; 1,570,041 bytes — recomputed at the freeze; matches the intake record |
| Shakti row grades (`shakti_row_grades_2026-10-22.csv`, restricted-local, never in git) | SHA-256 `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`; 5,704 rows — recomputed at the freeze; matches the intake record |
| Intake census, reproduced from the pinned files at the freeze | 5,704 rows; 5,536 analyzable; grades 3,212 documented-lineage / 2,087 undocumented-corroborated / 405 undocumented-uncorroborated; 18,065 tokens; 713 distinct signs; 4,904 analyzable rows carrying a CISI identifier; 77 sites — exact against the intake record (merged PR #339, `bfc811df`; record file SHA-256 `bd14e2b1f0607366ca1845797bcd17f8b577d23140a2e3111fe0cc2652cf9a9d`) and against Spec 068's executed step-0 census |
| **Primary population** (freeze-recorded counts; gate B's values) | Analyzable documented-lineage rows under Spec 068's step-0 limb: **3,045 rows; 11,805 sign tokens; 557 distinct signs**. Length census of the same extraction: 2,942 sequences of length ≥ 2; 2,068 of length ≥ 3; 103 of length 1; 90 classifiable signs (N(s) ≥ 20) |
| **Sensitivity population** (freeze-recorded counts) | Analyzable documented-lineage + undocumented-corroborated rows, same limb: **5,131 rows; 17,216 sign tokens; 707 distinct signs**; 2,889 sequences of length ≥ 3; 112 classifiable signs |
| Spec 068 record | Freeze digest `ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d` (`specs/068-yadav-zipf-controls-successor/freeze.json`); the populations above are its primary and sensitivity limbs, reproduced at this freeze, not re-derived |
| Phase-43 record (`outputs/phase43_all.json`) | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` — re-asserted. Anchor facts read from it at the freeze: 201 signs profiled on 3,137 sequences; 20 TERMINAL_STRONG and 40 INITIAL_STRONG signs; the ten exhibited TERMINAL_STRONG signs carry rates 0.683–0.892 and a smallest total of 22 (the labelled bases of NB-1.4 and NB-1.5); the (267, 99) opening candidate at bigram count 251 with dominance 0.74 (the record NB-1.6 repairs) |
| Parent claim record (`glossa-indus/claims/extracted_claims/farmer_sproat_witzel_2004.json`) | SHA-256 `41a855c9a79845206d7e63ed6fd835ef60f3611f3e825de5d73615ffba85425e` **at the freeze**. The draft's pin (`c4cf441f…`) predates a dated append to that file: the Spec 025 material audit's framing note of 2026-10-22 (proposal P1, commit `51cf8b3c`). The claim itself is unchanged: `farmer_sproat_witzel_2004_manual_001`, status **contradicted**, stage explained, three contradicting-evidence entries (Rao et al. 2009 entropy; the Phase-43 TERMINAL_STRONG set; the Phase-43 [M77/267][M77/99] formula) |
| The three fragments | `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001` and `…_critique_0002` (in `indus_valley_script_deciphered_from_myth_65ff0a26.json`); `without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001` (in `without_kings_or_conquests_the_indus_scr_ce9d98cc.json`) — each status contradicted, stage checked; restatements of the parent proposition, carrying no separate substance |

The Soviet tables' §2 pins of the draft are **not**
re-asserted as inputs: they stand in `spec.md`
§2 as history, retired from the member by the
§9.2 ruling. The extraction limb named above is
Spec 068's (`backend/scripts/phase430_yadav_zipf_controls.py`,
step 0): a row is analyzable iff at least one of
its symbols is not the layer's `000` placeholder;
tokens are counted excluding `000`; a row's
sequence for NB-1 is its symbols with `000`
removed. Gate B reproduces the primary counts
from the pinned layer under this limb, exactly,
or the run closes INVALID.

## 4. Freeze-stage exhibits

- **AEE lifecycle hooks (tasks L4).** Passed on
  the DD-038-10 reading after three recovery
  rounds (register 0.5-draft → 0.8-draft): at
  after_specify, after_plan and after_tasks, 19
  failure modes, every one an FR-2.3 draft-cap
  record; zero correctness failure modes; minimum
  propagated confidence 0.72 against the 0.70
  threshold. Full record: `aee/freeze-aee-note.md`.
- **Freeze tests.** `backend/tests/test_spec052_freeze.py`
  (see §8 for their able-to-fail proof).
- **House gates.** The freeze PR's CI is reported
  from the merge record, not here; this freeze
  claims nothing about it beyond what the run's
  own job conclusions state.

## 5. Machine record

- Register: `claims.json`, **19 claims**
  (F052-C01…C19), register version **0.8-draft**
  after recovery.
- AEE hooks (aee 1.5.3, lenient load, evidence
  verification off, no ledger): stamps
  20261024T032847Z (after_specify),
  20261024T032850Z (after_plan),
  20261024T032853Z (after_tasks) — UTC stamps of
  the 2026-10-23 owner-local freeze act.
- Freeze digest: `freeze.json` (SHA-256 of the
  canonical payload), covering `freeze.md`,
  `spec.md`, `claims.json`, `adjudication.md`,
  `amendment.md`, `aee/freeze-aee-note.md`,
  `build_freeze.py`, and
  `backend/tests/test_spec052_freeze.py`.
- Environment: Python 3.12.3;
  applied-epistemic-engineering 1.5.3
  (program pin `>=1.5.0,<1.6`); spec-kit
  `specify` 1.0.10.
- Phase allocated at this freeze: **Phase-437**
  (DD-052-6; the highest phase report on main at
  the freeze was Phase-436, Spec 073).

## 6. What the freeze fixes

- **The battery is NB-1** (`amendment.md` §3,
  claim F052-C16): position classes
  initial/terminal/medial over the layer's own
  sequences, length-1 sequences counted and
  reported separately and entering no count
  (partition property: every counted occurrence
  in exactly one class); per-sign counts and
  rates; classifiable iff N(s) ≥ 20; strength
  bands STRONG at a class rate ≥ 2/3, MODERATE at
  ≥ 1/2 and < 2/3, applied symmetrically to all
  three classes; opening bigrams as the first
  two signs of each sequence of length ≥ 2, with
  dominance taken over B, the number of sequences
  of length ≥ 2; the chance baseline a
  within-sequence permutation null (sequence
  length and sign multiset fixed), 999
  permutations, **seed 43052**, chance level the
  nearest-rank 95th percentile (the 950th
  smallest), for two statistics — the
  TERMINAL_STRONG count and the maximum
  opening-bigram dominance; conditions F and O
  as NB-1.8 states them (O carries its stated
  count floor of 10); thinness per NB-1.9. No
  element of NB-1 is the Phase-43 battery's, and
  none is presented under its name.
- **The populations** are §3's: the primary
  (Spec 068's documented-lineage analyzable set)
  and, conditionally, the sensitivity set — run
  and reported with the same prominence only if
  the primary run reaches an outcome word. The
  run's venue is the restricted local store; the
  Shakti source rows never enter git; what
  publishes is the dataset label, the census, the
  per-sign quantities, the strong sets, the null
  percentiles, and the outcome word.
- **The step-0 gates are A–D** (claim
  F052-C18): A corpus pin → INVALID; B population
  reproduction against §3's freeze-recorded
  counts → INVALID; C determinism (the battery
  run twice over the pinned layer with seed
  43052, identical outputs) → INVALID; D
  thinness (NB-1.9) → TOO THIN, with the census
  as its finding. BATTERY NOT PINNABLE cannot
  occur under the amendment; NOT ADJUDICATED is
  retained for a chance baseline that cannot be
  computed as frozen; the draft's Soviet gates
  and mapping-failure closures are retired.
- **The outcome semantics are the amendment's**
  (claim F052-C19): CONSISTENT iff neither
  condition F nor condition O holds on the
  primary population (the Farmer pattern present
  in the CISI-lineage corpus too; the recorded
  caveat narrows); INCONSISTENT iff both hold
  (the caveat widens); PARTIAL (DD-052-3,
  retained) iff exactly one holds, the outcome
  naming which; TOO THIN is gate D's closure.
  The word CONSISTENT is deliberately re-pointed
  from the draft §4.1 mapping, which used it for
  the both-signatures case; the amendment
  governs. Every outcome is appended, in the
  same words, to the parent claim's record and
  to each of the three fragments' records,
  naming the dataset (the Shakti corpus layer,
  CISI-compilation lineage) and the battery
  (NB-1, this amendment as frozen); the census
  and the per-sign quantities publish before the
  outcome word (spec §6 headline rules).
- **Claims served.** The parent claim
  `farmer_sproat_witzel_2004_manual_001` (SETTLED
  — contradicted) and its three restatement
  fragments (SETTLED as restatements). **No
  outcome of the amended run moves the parent
  claim's recorded status** (spec §6, §7 limit
  1), and no outcome is a verdict on the
  Farmer–Sproat–Witzel thesis.

## 7. What the freeze does not do

- It does not execute the study, compute any
  positional quantity, or assign any outcome
  word. The length and classifiability censuses
  of §3 are population facts of the pinned
  extraction (gate D re-derives them at
  execution); they are not results.
- It does not derive, reconstruct, or reproduce
  the Phase-43 battery, and does not map the
  Soviet tables. Both stand closed by the §9
  rulings; the recovery route (the original
  Phase-43 script surfacing) remains open to a
  future act and is not exercised here.
- It does not design or execute arm B, which
  stays trigger-armed and outside this spec
  (claim F052-C06).
- It does not publish, move, or copy any
  restricted corpus row; only the derived
  statistics named in §6 may ever publish, and
  only at execution.
- The lineage limit stands as the amendment
  states it: the Shakti layer is a CISI-tradition
  compilation, a distinct lineage from the Soviet
  compilation and from Holdat/M77, but its
  editions cover substantially the same
  excavated objects — agreement is
  cross-compilation robustness, not independent
  discovery.

## 8. Able-to-fail proof of the freeze tests

With the freeze tests green over the final
texts, exactly one character of
`specs/052-farmer-not-writing-soviet/freeze.md`
(a digest-covered source) was changed; the
freeze tests went red on the replay assertion,
as required. The character was then reverted
byte-identically and the tests returned to
green. The digest in `freeze.json` was computed
once, after the revert, over the final texts.

Correction before merge, 2026-10-23: the freeze
PR's first CI run (run 40059226540) failed on
exactly one assertion — the live-file hash of
the parent claim's record, which hashed
differently inside the full suite than in a
clean checkout (the file is a generated
extraction artifact that the suite's own
Spec 029 tests exercise in-tree). That assertion
was corrected to the record's facts, with the
freeze hash standing as a definition constant,
and the proof above was run over the corrected
texts; the digest in `freeze.json` is computed
over those corrected final texts.

## 9. OSF registration and the execution gate

The OSF registration for this frozen spec was
filed at the freeze under campaign decision E-1,
following the Spec 036–041 pattern; its record
is `osf-spec-registration.md` in this directory.
The registration carries this freeze's digest in
its study-design answer. Its approval is the
owner's act (the email token-link route, OSF
sign-in by ORCID only); execution does not begin
while approval is pending. **Execution
(Phase-437) begins only on a separate owner
order** — after approval, on the frozen
contract, with step 0 re-asserting every §3 pin
before any positional quantity is computed.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
