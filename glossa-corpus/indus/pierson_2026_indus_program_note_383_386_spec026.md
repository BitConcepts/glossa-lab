# Indus Program Note — Spec 026: RCPH Framework Transfer, Impact Audit, and Reruns (Phases 383–386)

**Tristen Kyle Pierson / BitConcepts LLC** · 2026-10-11
**Release:** Glossa-Lab v4.10.0 · **Repository:**
github.com/BitConcepts/glossa-lab · **Anchors:**
`INDUS_FINAL_ANCHORS.json` sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`
(287 anchors; unchanged by this program)

**AI disclosure:** the work recorded here was
executed by AI agents (Muse Spark, via Muse) at
the direction of the author, per the project
constitution §VI. All quantities are computed by
script from the data files and are reproducible
from the repository at the commits named below.

---

## 1. What this note reports

Spec 026 is a methods program, not a results program.
At the owner's direction, the program adopted the
study framework of the RCPH formalization program —
transferred principle by principle, with each
principle's Indus adaptation, the pre-existing Glossa
equivalent, the gap, and the adopted change recorded
in `spec026_transfer_map.md` — and then applied that
framework retroactively to the program's own record:
every prior spec (001–025) and every numbered phase
artifact (Phases 52–141) was classified in a frozen
impact register (116 items); every item the frozen
criteria marked RERUN-REQUIRED was actually rerun
under a pre-declared contract and freeze (Phases
383–386); four REPRODUCE-ONLY items were replayed
deterministically; and a historical assessment was
recorded for all 116 items — 75 of them carrying a
changed evidentiary status. This deposit adds the
Spec 026 record (transfer map, claim register, impact
register, rerun contracts/freezes, rerun reports and
results, historical assessments) to the carried-
forward v4.9.0 file set.

The discipline that governs everything below:
original result files and ledger entries are NEVER
rewritten. A historical assessment supersedes an old
label's *evidentiary reading*; the historical label
stands in its file. No rerun in this program changed
any anchor, minted or moved any PRED verdict, or
advanced any decipherment claim. Phase numbers for
the reruns are 383–386 because the repository's
global phase space already runs to 382 in
`backend/reports` — the collision was caught before
any freeze was written.

## 2. Framework transfer

The transfer map (`spec026_transfer_map.md`) works
through twelve principles. The load-bearing ones for
this program:

- **No target smuggling** (Principle 1): a
  hypothesized reading, an SA output, or a later-
  language outcome may not serve as a premise,
  feature, control, label, or tuning target in a test
  of that same claim; bridge assumptions are named,
  never absorbed.
- **Claim discipline** (Principle 2): stable claim
  IDs, kinds, boundaries, falsifiers, assumptions,
  `depends_on`, and `forbidden_assumptions`, with the
  dependency graph checked for cycles and forbidden-
  assumption inheritance. Spec 026's own register
  (`spec026_claims.json`) carries 16 governed claims.
- **Countermodel symmetry** (Principle 3): a rigorous
  negative closure counts as success exactly as a
  positive one does; a narrow closure never closes a
  broader target.
- **Origin groups** (Principle 4): multiple reports
  from one run or source count once; generated
  assertions are neutral evidence, never independent
  corroboration.
- **Discriminating controls** (Principle 5): a gate
  or procedure that cannot differentially pass and
  fail marks the run **INVALID**, not caveated. This
  rule fired inside this very program (§4, Phase-384
  v1).
- **Verdict taxonomy** (Principle 6): INVALID /
  INCONCLUSIVE / CONTRADICTED / SUPPORTED for bounded
  claims, with an explicit mapping onto the program's
  historical labels; passing a test never
  automatically promotes a claim or closes a broader
  obligation.
- **Freeze and replay integrity** (Principles 7, 12):
  canonical definitions, source hashes, and seeds are
  frozen before confirmation data is touched; a
  changed gate is a new version and a new freeze;
  superseding interpretations live in historical-
  assessment records linked to the untouched
  originals.

The spec ran the full spec-kit lifecycle
(constitution check → specify → clarify → plan →
checklist → tasks → analyze → implement → converge)
with the AEE extension assessed after specify, plan,
tasks, and implement, and gaps assessed after verify
(outputs preserved under the spec's `aee/` directory
in the repository). Two residuals are recorded, not
papered over: the evaluator extension has no
registered evaluators in this repository (a standalone
evaluator run honestly reports none configured), and
the AEE package version differs across the program's
venvs (1.0.4 Glossa / 1.0.2 spec-kit) and is pinned
per run in the artifacts. The AEE implement-stage
outcome was `gather_evidence` (16 claims, 0 below the
0.70 threshold, 5 residual heuristic failure modes);
the recovery is recorded and the gaps register after
verify shows 0 open gaps.

## 3. Impact register

Classification criteria were frozen BEFORE any item
was classified (`spec026_classification_criteria.md`),
keyed to method features — never to the direction of
an item's result. The register (PR #139) covers 116
items: Specs 001–025 and Phases 52–141 (82 phase
numbers with in-scope artifacts).

| Class | Items |
|---|---|
| RERUN-REQUIRED | 8 |
| REPRODUCE-ONLY | 12 |
| REINTERPRET-ONLY | 61 |
| UNAFFECTED | 27 |
| NOT-RERUNNABLE | 8 |
| **Total** | **116** |

Coverage gaps are recorded in the register itself:
Phases 92–95 and 97–100 have artifacts only in
`outputs/`, outside the scoped locations (they are
the NOT-RERUNNABLE cohort, §5); Phase-113 carries two
distinct studies under one number; Phase-114 has no
standalone report. Reclassification of any row
requires a dated amendment to the frozen criteria.

## 4. Reruns (Phases 383–386)

Each rerun ran under its own contract and freeze,
committed and merged BEFORE the rerun script executed
(PRs #140–#145). Verdicts use the framework taxonomy
of §2.

**Phase-383 — C4 rescoring of the coding pilots
(132/134/135).** Rescoring from the complete on-disk
coding records; NO re-coding. Every original headline
value reproduces EXACTLY (132 exact-sequence 0.20,
per-token 0.4798; 134 agreement 0.84, κ 0.7885; 135
agreement 0.78, κ 0.7129). The framework adds the
intervals the originals lacked (bootstrap over
objects, B = 9,999) and an origin-group audit: all
coding roles in all three pilots were executed by AI
agents of ONE model family, so the effective number
of independent coder origin groups is 1 — the
agreement statistics measure intra-origin
consistency, not independent corroboration.

- **Phase-132: CONTRADICTED.** Exact-sequence CI
  [0.10, 0.32] against the frozen 0.80 floor — the
  stop-rule failure is not sampling noise.
- **Phase-134: INCONCLUSIVE.** The agreement CI
  [0.77, 0.91] reaches the 0.85 proceed gate, so the
  original "missed the gate by one object"
  characterization cannot be excluded on sampling
  grounds; the gate is a fixed decision rule on the
  point estimate, so the original middle-band outcome
  stands — and the CI spanning the gate is itself the
  finding: a 100-object pilot cannot resolve a 0.01
  margin.
- **Phase-135: INCONCLUSIVE.** Same structure
  (agreement CI [0.70, 0.86]; κ CI [0.606, 0.819]).

**Phase-384 — C1 margin completion for Phase-137
F2/F3.** Practical margin declared before any run:
Cramér's V = 0.10. χ²/V reproduced exactly from the
recorded tables (F2 χ² 745.953, V 0.1154; F3
χ² 4966.362, V 0.2190).

- The v1 interval procedure (parametric bootstrap over
  table cells) was then subjected to the framework's
  own discriminating-control rule: on an independence
  table with F2's exact margins (true V = 0) it
  returns CI [0.1115, 0.1242] — a procedure that finds
  V ≈ 0.11 under exact independence is
  non-discriminating at these dimensions. **The v1
  interval adjudication is INVALID** — preserved in
  the report, not caveated, not used. The framework
  caught its own rerun's first method.
- v2 (contract and freeze written and merged BEFORE
  execution, PR #142): inscription-level bootstrap
  within site (B = 9,999), BASIC interval governing.
  **F2: basic CI [0.0589, 0.0778] — entirely below the
  declared floor → the bounded claim is CONTRADICTED
  at the declared margin**, converging with the
  original composition-controlled permutation
  verdict (raw p = 0.7354, NOT SUPPORTED). No
  reversal: two routes, one conclusion, now with a
  margin. **F3: basic CI [0.1823, 0.2104] — SUPPORTED
  stands at the declared margin.** Phase-137's
  original confounder confessions stand unchanged
  (preservation was later controlled for this
  population by Phase-140/385, where the effect also
  stands).

**Phase-385 — C1 margin completion for Phase-140 G1.**
Population (5,410 inscriptions, 7 sites) and observed
χ² 4966.362228 verified exactly. v1's percentile-only
interval excluded the point estimate under resampling
bias and was superseded by the pre-frozen v2 with the
BASIC interval governing (B = 4,999): **G1 basic CI
[0.1838, 0.2102] — entirely above the 0.10 floor →
SUPPORTED under control stands at the declared
margin.** Mandatory rider, unchanged: **chronology
is NOT controlled in the primary test** — period/
phase remain uncontrolled confounders.
The exploratory S-chron / S-depth basic intervals
([0.1848, 0.2098] / [0.1841, 0.2096]) sit in the same
range — labeled EXPLORATORY; they are not the
controlled primary. Phase-384's F3 margin completion
on the same marginal table returned a near-identical
basic CI [0.182, 0.210] under a different resampling
scheme — independent resampling schemes agree.

**Phase-386 — deterministic replay audit.** The
original scripts for Phases 116, 125, 127, and 131
were re-executed in a disposable worktree of the
frozen tree; the comparator checked every headline
quantity against the committed results files. **All
four REPRODUCED exactly** (116: median W1 0.4519,
Spearman ρ −0.0826; 125: median TV 0.636931, 16
judgeable signs, null 823/999, p = 0.824; 127: null CI
[0.046665, 0.131316], bootstrap median-TV CI
[0.548638, 0.722042], share of replicates ≥ observed
0.0; 131: credited share 0.061321, residual
unexplained 0.938679). No verdict changes; the
REPRODUCE-ONLY classifications for these items are
discharged. Anchors unchanged in every replay.

## 5. Historical assessments — 75 of 116 changed

The assessments (`spec026_historical_assessments.md`
/ `.json`) record, per register item, the framework
status that supersedes the historical label's
evidentiary reading where they differ — and exactly
what the old run does and does not establish. Beyond
the eight rerun rows (§4), the changed cohorts are:

- **INVALID cohort:** Phases 111–114 (blind
  affiliation) and Spec 017 — the instruments could
  not discriminate (a grammar-free generator won the
  blind test), so the bounded claims were not tested
  by a valid instrument. INVALID, not "rejected."
- **Calibration-rejected → INCONCLUSIVE:** Phases
  115/117/118 — the batteries were rejected at
  calibration; under the taxonomy their bounded claims
  are INCONCLUSIVE, which is the honest ceiling for a
  test whose instrument never validated.
- **Taxonomy mappings:** Phases 116/125/127/131
  (replayed, §4) — bounded claims CONTRADICTED;
  the diagnostic findings stand as recorded.
- **SA-era cohort:** Spec 004 and Phases 52–104 —
  evidentiary status superseded under the standing
  H26 quarantine (the SA method was falsified as
  sufficiency evidence at Phase-107). These items
  establish at most their bounded computational /
  descriptive content; no rerun may rehabilitate them
  as promotion evidence.
- **NOT-RERUNNABLE ceiling:** Phases 92–95, 97–100 —
  artifacts exist only outside the scoped locations;
  their claims carry no claim-level weight until and
  unless artifacts are recovered into scope.

The remaining 41 items are unchanged: their
historical labels and evidentiary readings stand as
they were.

## 6. Verification state at the release source

Spec 026 closed on merged main `bf85ff31` (PRs
#138–#146). On that commit: the full backend suite's
terminal record is **1,152 passed / 12 skipped /
0 failed**; the foundation check is **40 passed /
0 failed**; main's own CI run (38110406069) completed
success; and `INDUS_FINAL_ANCHORS.json` is
byte-identical to every prior release (sha256
`eccea6d5…` above). One correction is recorded
plainly, because this program's records are the
product: an early completion summary of the Spec 026
closeout stated a suite figure of 3,647 passed /
29 skipped. That figure came from a misread mid-run
poll fragment; the executing session's own terminal
output — 1,152 passed / 12 skipped / 0 failed —
governs, and the correction was entered on the
record the same day. Only the corrected figure
appears in this note and in the release validation
record.

## 7. What this release does not do

- No anchor changed; anchors sha256 `eccea6d5…`
  unchanged. PRED-2026-001/002/003 remain PENDING —
  no scoring was performed or permitted.
- The motif arm (Spec 024) remains CLOSED on its
  recorded condition (new owner decision AND human
  expert coders); Spec 026's rescoring does not
  reopen it.
- No previously published deposit is altered. Spec
  025's Zenodo v4.9.0 record stands as published;
  this version adds the Spec 026 record alongside
  the carried-forward set.
- Broader targets remain open exactly where they
  were: no narrow rerun closes any decipherment
  claim, and F3's/G1's period and excavation
  confounders beyond preservation remain named,
  not resolved.
