# WP1 — Baseline and finding-by-finding dispositions

Glossa Lab external-audit repair program, 2026-10-26. Work Packages 1
(baseline + containment) and 10 (public-claim reconciliation, prepared
not published).

**Status of this document:** staged patch content only. Nothing in this
repair package is published, pushed, or applied to any live surface.
The repository at `~/workspace/glossa-lab` was not touched. Historical
verdicts and deposited versions are preserved throughout: a computation
error invalidates its certification; it does not falsify the underlying
linguistic hypothesis, and no invalid-method finding in this document
is labeled a falsified reading.

**Sources used:** the governing brief
(`2026-10-26-repair-brief-from-external-audit.txt`); byte-verified
staged copies of the repository at HEAD in
`~/workspace/glossa-run/repair-2026-10-26/work/`; staged code inspection
copies in `~/workspace/glossa-run/repair-2026-10-26/inspect/`; and the
goal-side post-snapshot records listed in §2. Every defect mechanism
cited below was re-read in the staged code during this task, not taken
from the brief on trust.

---

## 1. Baseline: audited snapshot vs current HEAD

| | |
|---|---|
| Audited snapshot | `cc9ffeb4c8afe9ab4f8a42ccd6467c7bc0c90278` |
| Current HEAD | `d80dcb7c` (branch `main`) |
| Distance | 11 commits ahead of the snapshot |
| Changed files | 50 |
| What the 50 files are | Spec 077 freeze and execution; Spec 078 (M13) freeze and pilot; the M77 Table I record |
| Defect sites touched | **None.** No changed file touches the audited defect sites: the Phase-58 phonological checker, the Phase-69 site-stratification routine, the Phase-96 crosswalk construction, `provenance_audit.py`, or the Phase-48 / Phase-109 machinery |

**Conclusion.** The brief's code findings still apply at HEAD. The
eleven post-snapshot commits advanced other work (two studies were
frozen and run; see §2) but repaired none of the audited defects, so
every code-level disposition in §4 starts from "still applies" unless a
goal-side record corrects the specific point.

Spot checks performed in this task (in addition to the coordinator's
compare):

- SHA-256 hashes were computed over all staged evidence files; they
  are recorded in `dependency-map.json` and reproduced in
  `dependency-map.md`. The staged anchor table hashes to
  `df0cf620…`, matching the pin the post-snapshot M13 pilot record
  verified before its run — the staged data is the data the
  post-snapshot work actually used.
- The three defect mechanisms were re-read in the staged code:
  - *Phonotactics (Phase-58).* Each reading is reduced with a regular
    expression that keeps only `a–z` and the long-vowel markers
    `ā ī ū ē ō` before testing. The prohibited initial sounds
    (ṭ ḍ ṇ ḷ ṟ ṉ) are not in the kept set, so they are deleted from
    the reading before the test ever sees them — a reading beginning
    with one of them is tested as if it began with the following
    vowel. Input that reduces to nothing returns "valid" ("can't
    check"). Only the first segment before a `/` and only the
    word-initial position are ever tested. `provenance_audit.py`
    reuses this machinery by import, so the defect flows unchanged
    into the Phase-108 and Phase-109 headline quantities.
  - *Site statistics (Phase-69).* The chi-square routine returns
    preset p-values — 0.0 outright when the statistic exceeds twice
    the degrees of freedom, 1.0 outright when it is below 0.5 — and
    returns 0.5 on any exception, instead of computing a p-value.
    Its degrees-of-freedom count is accumulated per cell and then
    overwritten. A numerical failure can therefore become evidence.
  - *Crosswalk (Phase-96).* The construction script loads the
    project's own anchor table and writes each new crosswalk entry's
    `reading` field from the anchor's own reading. The agreement
    routine in `provenance_audit.py` later treats that field as
    Parpola's reading and compares the anchor against it. On those
    entries, agreement is guaranteed by construction.

## 2. What changed after the snapshot (goal-side records)

These records postdate the audited snapshot. They correct specific
brief points; they do not repair the audited code defects.

| Record (goal files, 2026-10-26) | Post-snapshot outcome | Brief point it corrects |
|---|---|---|
| Spec 077 (M7) freeze-and-execution record | Spec 077 executed once as frozen. F077-C01: **NOT SUPPORTED** — signary witnessed 399/557 = 71.63%, with an exact 158-sign gap list | The brief treated M7 as a draft to locate; it is now an executed study with a verdict |
| M13 pilot record (Spec 078) | Pilot closes **CANNOT BE ADMINISTERED**: blind coding yielded checkable claims from 7 of the 86 counted signs, against the frozen administrability floor of 25. OSF registration 49fgu, DOI 10.17605/OSF.IO/49FGU | WP7's M13 items: the design was frozen and run; the route returns to the iteration loop |
| M14 pilot record + M14 iteration-2 pilot record | Both pilots fail at instrument recovery; the M14 line closes **PARKED**. No freeze, no pair verdicts | WP7's M14 items: successor work exists and has closed as parked |
| Step 0-G instrument record (G44) | **FAILED** — leg 1 (planted recovery); leg 3 outstanding; Method M4 remains gated, draft only | WP8-adjacent instrument work, post-snapshot |
| G44-S validation record | **FAILED** — legs 1 and 1B | Same line |
| G44-S2 validation record | **INCOMPLETE** — generation defect; kill criterion K2 triggered (the synthetic family is infeasible as designed); no instrument verdict exists | Same line |
| Atlas Line 1 catalog leg | Catalog leg executed on the completed Laursen Table 1: 121 rows, 28 Gulf INDUS entries. Catalog-level results only; the sequence leg remains blocked | WP9 contact-zone item, descriptive leg |
| v9 deposit record | Preprint **v9 published**: Zenodo record 23668053, version DOI **10.5281/zenodo.23668053**, concept DOI 10.5281/zenodo.20379070 (unchanged); website tracker promoted to v9 | The brief's "no v9 DOI exists" was true only of its snapshot. WP10's version reconciliation now runs v8 → v9 |
| Rerun / invalidation audit | Sixteen map items audited against final data (4 unaffected, 6 superseded-but-harmless, recomputations run or queued, 4 needing a new spec or owner decision) | Context for WP9/WP10; also the source of the progress-percentage wording treated in the overlay |

One internal inconsistency found while building the dependency map,
recorded here so it is not lost: `reports/phase109_rebase.json` heads
its anchor counts as HIGH 166 / MEDIUM 5 / LOW 112 / CANDIDATE 4,
while the canonical anchor table's own counts are HIGH 166 /
MEDIUM 5 / LOW 3 / CANDIDATE 113. The totals (287) and the H+M count
(171) agree; only the LOW/CANDIDATE split differs. No headline claim
in this repair turns on that split, but the rebase header should not
be quoted for it.

## 3. Lifecycle states: what exists, and the narrow additions proposed

The brief asks that existing lifecycle states be reused where
suitable, with narrowly scoped additions only for: invalid method,
requires revalidation, insufficient evidence, and superseded record.

### 3.1 What already exists (from the staged record)

- **Spec 006 provenance categories** (pre-registered in
  `specs/006-anchor-provenance-audit/spec.md`): ICONOGRAPHIC,
  LITERATURE, DEDR, GRAMMAR, FORMULA, CROSSWALK_CORPUS, SA_DERIVED,
  SA_CONFIRMED_ONLY, MIXED, UNTRACEABLE. These classify *where an
  anchor's value came from*. They are provenance categories, not
  claim-health states, and they are reused here unchanged — the
  dependency map's derivation chains are stated in their terms.
- **The anchor flag `pending_non_sa_validation`** (Phase-108/109):
  an anchor-level marker that a reading's chain is not yet validated
  by a non-SA route. This is the existing home of "requires
  revalidation" *for anchors*; the claim-level state proposed below
  points at it rather than replacing it.
- **Record-level words already in use** in the README and rebase
  artifacts: *retired* (the v4 headline basis; the 161-anchor set),
  *superseded* (v4 by v8), *falsified as evidence* (the SA machinery,
  Phase-107 — a verdict about a method's evidential value, carefully
  not a verdict about the readings it produced).
- **Study verdict words** in the post-snapshot records: NOT
  SUPPORTED, CANNOT BE ADMINISTERED, PARKED, FAILED, INCOMPLETE.
  These are verdicts on studies and instruments and are reused
  verbatim for them.

What does **not** exist in the staged record is a claim-level state
set for the health of a *displayed claim* — the thing WP1 item 5 and
WP10 need. (A claim-lifecycle spec, Spec 029, is referenced by the
README's 2026-10-12 errata as the authority for an in-place factual
correction; its full text was not among the staged files, so no state
is attributed to it here beyond that one recorded use.)

### 3.2 The four narrow additions (claim-level states)

Each applies to a claim or a displayed summary, never to a reading's
truth. Definitions are deliberately narrow:

| State | Definition | Use when |
|---|---|---|
| `invalid_method` | The method that produced the claim's number or certification was defective in a way that can manufacture the reported result (a checker that cannot fail, a statistic replaced by a preset value, a comparison against a copy of oneself). | The certification is void. The underlying hypothesis or reading is **not** thereby falsified; it returns to unvalidated. |
| `requires_revalidation` | The claim's own method may be sound, but a load-bearing input or supporting leg has been invalidated or superseded, so the claim cannot rest on that leg until the dependent decision is reassessed individually. | A dependency fails; the claim itself has not been re-examined yet. |
| `insufficient_evidence` | The claim asserts more than its evidence supports — including a characterization of someone else's work that the record does not back, and any single percentage offered as a measured distance to decipherment without a defined population and sampling basis. | The honest statement is weaker than the displayed one, and no corrected evaluation exists yet. |
| `superseded_record` | The claim faithfully reports a record that has since been replaced — an older anchor set, an older deposit, an older version. The number may be accurate *for that record*. | The defect is currency, not computation: move to clearly labeled history; do not present as current. |

Mapping onto what exists: `superseded_record` is the claim-level
form of the record-level *retired / superseded* words already in
use. `requires_revalidation` is the claim-level companion of the
anchor flag `pending_non_sa_validation`. `insufficient_evidence` is
the claim-level companion of Spec 006's UNTRACEABLE (which says, at
anchor level, "the record does not establish this"). Only
`invalid_method` is genuinely new, and it is needed because none of
the existing words say "the certifying computation itself was
broken" without implying the reading is false — the exact confusion
the brief forbids.

The overlay (`claim-status-overlay.json`) uses only these four
states, plus the existing vocabulary where a study verdict is the
right label.

## 4. Finding-by-finding dispositions

Status key: **Still applies** — the finding holds at HEAD and the work
remains to be done (or is gated). **Corrected since snapshot** — a
post-snapshot record (§2) supersedes that specific point.
**Requires further evidence** — the disposition itself cannot be
settled from the staged record; the missing evidence is named.
**Prepared here** — WP1/WP10 work delivered as staged patch content
in this task; live surfaces still carry the old text until the patch
is landed by a separate, authorized act.

### Work package 1 — Baseline and containment

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 1.1 | Record current commit; compare with audited snapshot; triage findings | Prepared here | §1 of this document; the triage is this table |
| 1.2 | Dependency inventory linking claims to evidence records, source passages, artifacts, input hashes, code revisions, run environments, displayed summaries | Prepared here | `dependency-map.md` + `dependency-map.json` (18 records, 17 claims, 50 edges) |
| 1.3a | Trace Phase-48 promotions → Phase-108 provenance → retained tiers → 94 strict subset | Prepared here | Dependency map claims C-PHASE48-PROMOTIONS, C-PROV108-CLASSIFICATION, C-RETAINED-TIERS, C-94SET |
| 1.3b | Trace Phase-58/69 → `provenance_audit.py` → Phase-109 rebase → headline metrics | Prepared here | Dependency map claims C-PHONO-0, C-SITEINV-6565; defect mechanisms re-read in staged code (§1) |
| 1.3c | Trace Phase-96 crosswalk → Parpola agreement → KEEP/RESTORE decisions | Prepared here | Dependency map claims C-PARPOLA-81, C-KEEP-RESTORE-109; copy mechanism re-read in Phase-96 code |
| 1.3d | Trace README/UI metrics → paper source, PDF, version manifest, deposited record | Requires further evidence | README side is mapped (C-RELEASE-CHAIN). Missing: the live UI metric surfaces and the deposited PDF were not among the staged files and no deposit access was exercised in this task; the deposited-PDF-vs-documented-hash comparison is **UNVERIFIED** here |
| 1.4 | Lifecycle states: reuse existing; propose narrow additions only | Prepared here | §3 of this document |
| 1.5 | Contain the four advertisings (zero violations, 65/65 equivalence, independent Parpola validation, combined fish denominator) | Prepared here | `claim-status-overlay.json` (17 entries) + corrected `patch/README.md`. Live surfaces still carry the old text — containment is prepared, not published |
| 1.6 | Preserve unrelated descriptive results; keep assignment coverage distinct from accuracy | Prepared here | Positional-grammar and M267 results untouched; coverage claims carry the distinction in the map, the overlay, and the WP10 report table |
| 1.A | Acceptance: dry-run invalidation reaches all current descendants and public summaries, historical bytes preserved; every affected claim has a disposition and evidence link; no invented replacement | Prepared here — met | `patch/backend/scripts/repair_dry_run_invalidation.py`; output in `outputs/wp1-dry-run.txt`: parent `crosswalk_v2` → 2 descendant claims, 3 displayed summaries; 22 staged historical files hashed before/after, identical; result PASS |

### Work package 2 — Phonological checking

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 2.1 | Versioned parser preserving linguistically meaningful distinctions; Unicode normalization, schemes, alternatives, annotations, uncertainty specified | Still applies | No corrected parser exists at HEAD; the staged checker is the defective one (§1) |
| 2.2 | Do not equate unknown with permitted; do not collapse contrasts for matching convenience | Still applies | Current code does both: unknown-after-reduction returns "valid", and the reduction deletes contrastive characters |
| 2.3 | Slash alternatives treated as alternatives, each tested | Still applies | Current code tests only the first segment before `/` |
| 2.4 | Linguist must establish which restrictions belong to the proposed historical language vs later Tamil; software may show compliance with declared rules, not historical accuracy | Requires further evidence | Named human dependency (linguist review). Not supplied in the staged record; WP2's certification wording stays gated on it |
| 2.5 | Regression: each of ṭa, ḍa, ṇa, ḷa, ṟa, ṉa triggers the declared prohibited-initial rule | Still applies | By direct code reading, each currently escapes the rule (the initial character is deleted before testing, leaving a vowel-initial string that passes). The regression suite itself belongs to WP2 and was not run here |
| 2.6 | Regression: a permitted example passes only the specified rule | Still applies | WP2 suite not built in this task |
| 2.7 | Regression: empty, malformed, unrecognized, annotation-only input → UNCHECKABLE or explicit error, never PASS | Still applies | Current code returns PASS ("can't check") for input that reduces to nothing — the opposite of the requirement |
| 2.8 | Regression: composed/decomposed Unicode behaves consistently | Still applies | The staged checker performs no Unicode normalization step at all |
| 2.9 | Regression: alternative readings retain distinct outcomes | Still applies | Defeated by the first-segment-only test (2.3) |
| 2.10 | An initials-only test is never reported as a complete phonotactic assessment | Still applies | The README banner presented the initials-only result as "0 Dravidian phonotactic violations" without qualification; contained by the overlay, corrected in the patch README |
| 2.A | Acceptance: controls behave as specified; uncheckable cases stay in the denominator; dependent claims unvalidated until a corrected analysis runs | Still applies | WP2 not executed in this task; the overlay holds the dependent claims at `invalid_method` meanwhile |

### Work package 3 — Site statistics and invariance

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 3.1 | Replace fabricated p-values and numeric fallbacks with a vetted, version-pinned implementation; validate counts/shape; degenerate tables explicit; a numerical failure halts or errors, never p = .5 | Still applies | All three failure modes re-read in the staged Phase-69 code (§1). No corrected implementation at HEAD |
| 3.2 | Log method, statistic, expected counts, degrees of freedom, uncertainty; specify Pearson/Yates and sparse-table procedures | Still applies | Not present in the staged routine |
| 3.3 | Reference checks: [[12,8],[8,12]] → 1.6, p ≈ .2059032107; [[13,7],[7,13]] → 3.6, p ≈ .0577795711 (uncorrected Pearson, df = 1) | Requires further evidence | These verdicts belong to WP3's corrected implementation and were not run in this task. By inspection, the staged routine cannot certify them: for these tables its shortcut branches and approximation replace the stated asymptotic values |
| 3.4 | Further tests: multidimensional tables, zero margins, all-zero inputs, one eligible site, sparse counts, large effects vs an independent reference | Still applies | WP3 suite not built here |
| 3.5 | Separate "no difference detected" from equivalence; equivalence needs a prespecified margin and procedure, clustering and multiplicity handled; power/precision are design properties; no margin chosen after seeing outcomes | Still applies | No equivalence design exists in the staged record; the README's invariance wording is contained by the overlay |
| 3.6 | Establish the historical source revision for old outputs whose p-values the current routine cannot produce | Requires further evidence | The staged files do not identify which code revision produced the historical Phase-69 outputs; git history beyond the coordinator's compare was not in scope here |
| 3.A | Acceptance: agreement with the reference within declared tolerances; exceptions never become evidence; insufficient data stays explicit | Still applies | WP3 not executed in this task. Note the current displays also hide the insufficient-data remainder (29 of 94 strict; 81 of 171 full) outside the tested denominator |

### Work package 4 — Circular comparator evidence

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 4.1 | Separate sign-mapping, depiction, phonetic-reading, semantic-reading provenance, and project-derived values | Still applies | The crosswalk file does not carry this separation in the staged record |
| 4.2 | Every externally attributed reading needs an exact primary-source locator and sign scheme | Requires further evidence | A source-by-source pass over the 184 crosswalk entries has not been done; the staged file's citations are file-level, not entry-level locators |
| 4.3 | Do not label a copied project value as a scholar's independent reading | Still applies — mechanism confirmed | Phase-96 code writes the project's anchor reading into the crosswalk `reading` field later consumed as "Parpola's reading" (§1) |
| 4.4 | Classify each comparison: independently sourced / used in construction / project-derived / unverified / ineligible; only genuinely eligible evidence counts toward independent validation; zero eligible is a reportable answer | Still applies | Partial counts exist in the file's own stats (67 of 184 identity-inference-only; 113 attested by an independent in-repo source) — but attestation of a sign pairing is not an independently sourced *reading*, so 113 must not be read as the eligible count |
| 4.5 | Reassess affected KEEP/RESTORE decisions individually; other surviving evidence stands | Prepared here (flag only) | The one Phase-109 decision kept on crosswalk support is flagged `requires_revalidation` in the overlay (C-KEEP-RESTORE-109). The reassessment itself is WP4 work, not done here |
| 4.A | Acceptance: a copied-comparator cycle cannot earn support; changing a project reading cannot silently alter its comparator; an independently coded value stays fixed with its source revision | Still applies | No guard or test implementing this exists at HEAD |

### Work package 5 — Anchor promotions and the full core

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 5.1 | Priority order: the 30 Phase-48 promotions first, then all 94 strict entries; the 44 pending candidates maintained without new weight | Still applies | The per-anchor audit was not executed in this task (WP1/WP10 scope). The overlay's claim-level containment is not a substitute for it |
| 5.2 | Per-candidate record: identity and corpus frame, proposed value, alternatives, exact source passages, original derivation | Still applies | Not produced in the staged record at this completeness level |
| 5.3 | Distinguish original independent evidence from later repetition on the same observations | Still applies | Phase-108 trails are the starting material; the WP5 judgment pass remains |
| 5.4 | Record which kind of thing each test tests (drawing, distribution, functional role, phonetic value, meaning) | Still applies | Phase-48's own tests show why: its positional test ignores the proposed reading's sound entirely, and its dictionary test checks lexical plausibility, not a sign-to-word mapping |
| 5.5 | State the actual falsifier and the distinguishing observation for each candidate | Still applies | Not in the staged record |
| 5.6 | Retain historical confidence category; give current evidential status separately; no invented calibrated probabilities | Still applies | The overlay follows this pattern at claim level; the per-anchor application is WP5 work |
| 5.7 | Remove automatic positive credit: short strings, missing model characters, absent neighbors, missing expectations | Still applies — mechanisms confirmed | All four pass-by-default paths re-read in the staged Phase-48 code (`too_short_pass`; `char_not_in_lm—pass_by_default`; `no_anchor_neighbours—pass_by_default`; `no_expectation—pass_by_default`). The Phase-48 output shows the result: 30 tested, 30 promoted |
| 5.8 | Optional compute backends implement the same method | Still applies | The Phase-48 bigram test branches on whether torch is present, and its artifact records `gpu_device: cuda` — CPU and accelerated runs are not the same method as written |
| 5.A | Acceptance: no promotion earned by an uncheckable test; backends agree; every core entry has an auditable current disposition; expert adjudication marked pending where required — never forced complete | Still applies | Not met; WP5 remains the largest single block of audit work in the program |

### Work package 6 — Corpus representation and replay

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 6.1 | Extend existing artifact/sign registries; stable object, face, seal/die/impression, sign-token, catalog, image, and source-lineage identifiers | Still applies | Not built in this task |
| 6.2 | Distinguish repeat impressions, duplicate publication, duplicate transcription, genuinely separate artifacts | Still applies | Not addressed in the staged record |
| 6.3 | Keep uncertain direction, damaged tokens, compounds, allograph proposals, unresolved crosswalk alternatives; a repeated Mahadevan identifier blocks affected joins, not whole-scheme analysis; never silently take the first join result | Still applies | No staged evidence of a change |
| 6.4 | Gap-aware representations alongside the historical compressed frame; leading/trailing/internal gaps, marked signs, singletons-after-filtering tested; "initial" defined (inscription boundary vs first retained legible token) | Still applies | Directly relevant to WP2/WP3 correctness; not built here |
| 6.5 | Verify each legacy loader's artifact key and position ordering against its input schema | Still applies | Not verified in the staged record |
| 6.6 | Safe replay wrapper for Spec 076 (manifest, hash verification before computation, path resolution, refuse on missing/mismatched dependencies, new output directory, census checks as well as hash checks, unknown historical environment fields marked unknown, refuse to overwrite historical results) | Still applies | Not built in this task. Note from the post-snapshot record: the Spec 078 pilot's Step 0 passed exactly and expressly relied on Spec 076's standing — a replay wrapper is the durable form of that check |
| 6.A | Acceptance: clean authorized checkout reproduces the run or reports a precise access blocker; a one-byte count-preserving change fails at the hash gate; a failed replay leaves every archived file unchanged; resolved Mahadevan dagger flags stay resolved | Still applies | None of these were exercised in this task |

### Work package 7 — Structural calibration, prospectively

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 7.1 | Preserve Spec 076's failed bridge verdict and its successful descriptive shuffle endpoints; append a correction to any "failing the bar proves the marginals-only explanation" implication; report endpoints separately | Still applies | Preservation is standing practice and nothing here disturbs it; the appended correction is not in the staged record |
| 7.2 | Locate the actual current M13/M14/M7 drafts before editing; if unavailable, prepare labeled successor proposals without inventing frozen content or identifiers | Corrected since snapshot | The drafts' successors were located, frozen, and run post-snapshot: Spec 077 (M7), Spec 078 (M13), M14 pilot + iteration 2 (§2). Nothing about their frozen content needs to be invented — the records are on file |
| 7.3 | M13: separate distributional, word-boundary, and functional claims with observable evidence for each; keep the 86-sign panel, at-most-three-failures bar, and at-least-25-checkable coverage bar if operative; add reporting by informative denominator and claim type before freezing; never modify a completed study's thresholds | Corrected since snapshot | Spec 078 was frozen with the 86-sign panel and the 25-checkable floor and executed once as frozen; it closed CANNOT BE ADMINISTERED at 7 of 86 checkable, and no threshold was modified after the fact. Any redesign is a successor proposal under the brief's own rule |
| 7.4 | M14 / M7 handling in the same prospective spirit | Corrected since snapshot | M7 executed (Spec 077: NOT SUPPORTED, 399/557 = 71.63% witnessed, 158-sign gap list). M14 ran twice and closed PARKED |
| 7.5 | Independently coded known-answer positive controls and deliberately false checkable controls; FREE or non-discriminating rows cannot demonstrate accuracy; core-derived controls are consistency checks unless external truth is established | Still applies | A standing design requirement for successor drafts; the G44 instrument line (§2) is where its absence bit hardest — see WP8 |
| 7.A | Acceptance: the bridge rejects false checkable claims at its registered rate and passes known controls without post-result weakening; a vocabulary that cannot express testable functional predictions closes as inadequate; no corpus-only compatibility score licenses a semantic promotion | Still applies | Not met as a program outcome: the executed bridge could not be administered at all, which the record reports honestly; successor design work is gated, not complete |

### Work package 8 — Exposure accounting and negative controls

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 8.1 | Record where each artifact, statistic, and interpretation influenced candidate generation, preprocessing, thresholds, or model selection; unknown exposure stays marked unknown; object-family and source-lineage grouping for validation | Still applies | Not systematically recorded in the staged record; the dependency map marks unknowns as unknown where they occur |
| 8.2 | Challenge the complete search procedure: meaning permutations, matched wrong mappings, plausible wrong morphology, comparable homophony/polyphony flexibility, wrong-language candidates, structured non-language corpora; matched tuning budgets; classification, ranking, and calibrated acceptance kept separate | Still applies | Post-snapshot instrument work (G44, G44-S, G44-S2) attacked part of this space for the 44-anchor scorer and failed or proved infeasible (§2); the full-procedure challenge has not been run |
| 8.3 | Interpretation discipline: a structured fake passing a diagnostic defeats the diagnostic, not the language hypothesis; passing a finite suite licenses only the tested scope; observationally equivalent readings are reported as non-identifiable | Still applies | Standing rule for all successor reporting |
| 8.A | Acceptance: any new discrimination/validation claim has prespecified sensitivity, false-acceptance, abstention, and eligibility rules covering the entire selection procedure; descriptive censuses need accurate provenance and uncertainty, not automatic non-language controls | Still applies | Not met; Method M4 remains gated, draft only, per all three instrument records |

### Work package 9 — Bounded external and completeness studies

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 9.1 | Contact-zone catalog: reconcile 121 rows and 28 Gulf INDUS entries without treating all entries as readable texts; retain full reference strings and uncertainty; separate direct Meluhha attestations from broad contact-term hits; establish object identity, dates, pseudo-Indus status, source quality before proposing paired names; catalog readiness ≠ transcription readiness | Corrected since snapshot (descriptive leg) | The Atlas Line 1 catalog leg ran 2026-10-26 on the completed Laursen Table 1 (121 rows; 28 Gulf INDUS) with exactly this discipline — catalog-level results only, expressly not filed as decipherment anchors. The inferential follow-ons (paired names and the like) remain gated |
| 9.2 | Numeral pilot: one stroke family and independent quantitative constraints chosen before fitting; alternative systems and accidental-fit controls specified; quantity, unit, commodity, and pronunciation claims separated; if no independent constraints exist, close the validation pilot as unavailable and keep exploratory proposals separate | Requires further evidence | The staged record does not establish whether independent quantitative constraints exist for any stroke family; until that is shown, the brief's own rule applies — the validation pilot is unavailable and proposals stay exploratory |
| 9.3 | Completeness: catalog digitization coverage, within-stratum sampling coverage, and historical missingness reported separately; object-family resampling; site/period/medium strata; alternate sign inventories; no single global completeness or decipherment percentage without defensible population and sampling assumptions | Still applies | The no-single-percentage rule is enforced for current claims by overlay entry C-PROGRESS-PCT; the completeness study itself has not been run |
| 9.4 | Method sources (Born et al. 2023 and 2022; Dahl 2005; Luo et al. 2021; Dwork et al. 2015; Chao/Jost 2012) used as benchmark/method sources with transfer assumptions documented; they do not reopen closed SA/M1/M2 routes | Still applies | Standing instruction; nothing in this task reopens a closed route |
| 9.A | Acceptance: each inferential proposal carries exact inputs, falsifier, statistical unit, controls, thresholds, power/precision rationale, stop rule, access status, registration plan; descriptive reconciliation instead carries identity, integrity, provenance, and coverage checks | Still applies | Met for the executed catalog leg's descriptive scope; inferential proposals remain drafts until their conditions are met |

### Work package 10 — Public claims and release artifacts

| # | Element | Status | Basis / what remains |
|---|---|---|---|
| 10.1 | Generate current summaries from the authoritative claim system; reconcile README, report indexes, UI metrics, manuscript source, compiled PDF, supplementary tables, version/deposit metadata; preserve deposited versions and historical verdicts | Prepared here (README scope) | The README reconciliation is staged as patch content. Report indexes, UI metrics, manuscript source, PDF, and supplementary tables were not among the staged files — their reconciliation is prepared as notes in the WP1/WP10 report and **requires further evidence** (the artifacts themselves) before any text is finalized |
| 10.2 | Correct: zero phonotactic violations as independent support | Prepared here | Withdrawn in the overlay and the patch README (banner + table); no replacement number |
| 10.3 | Correct: 65/65 invariance as established equivalence | Prepared here | Withdrawn as established invariance in the overlay and the patch README |
| 10.4 | Correct: project-copy agreement as external Parpola validation | Prepared here | Withdrawn as validation in the overlay and the patch README |
| 10.5 | Correct: combined fish-isolation denominators | Prepared here | Banner and table corrected to separate denominators (0/113 corpus; 0/27 Gulf) using the README's own component counts. One further occurrence in the README's Current research status section sits outside this patch's scoped correction areas and is inventoried in the overlay for the same fix at landing time |
| 10.6 | Correct: Nair as a replication of Glossa readings or grammar | Prepared here | Banner and table corrected; the status-section occurrence is inventoried in the overlay on the same terms as 10.5 |
| 10.7 | Correct: v8/94 vs v8-source/161 conflict and stale DOI/version rows | Prepared here | Patch README cites v9 as deposit of record (10.5281/zenodo.23668053) and keeps v8 as superseded history; the metrics-table DOI row (a v4 DOI labeled "citation of record", contradicting the same file's re-base note) is corrected; the layout line's v4 PDF name is corrected to the v9 PDF. The "161" in the cited paper title is the deposited paper's own title text and is preserved as a citation — the conflict is disclosed, not edited away |
| 10.8 | Correct: any percentage presented as measured distance to decipherment | Prepared here | Overlay entry C-PROGRESS-PCT covers the program-record occurrence (the ~36% ladder figure) and bars the form; the staged README carries no such percentage |
| 10.9 | Verify the actual deposited PDF against the documented artifact hash when access is available; until then, say the comparison is unverified | Requires further evidence | **UNVERIFIED in this task.** No deposit access was exercised. The documented hash (from the v9 deposit record: PDF SHA-256 `d3cea9c3…`, for `pierson_2026_indus_decipherment_preprint_v9.pdf`, 206,529 bytes) is recorded in the dependency map as *documented*, not as *verified by this task* |
| 10.10 | A successful document build or internal integrity check is not scientific validation | Prepared here | Stated in the WP1/WP10 report's closing section and applied throughout these dispositions |
| 10.A | Acceptance: every current numerical claim identifies population, denominator, method version, inputs, status, and limits; no unsupported claim regenerated from archived material; no v9 DOI fabricated | Prepared here | The claim-by-claim table is in the WP1/WP10 report. The v9 DOI comes from the goal-side deposit record, not from inference. Scope limit: the table covers the staged README in full and the paper/UI surfaces as prepared notes (see 10.1) |

## 5. What this package does not establish

- Software correctness beyond the specific defects re-read in the
  staged code. No corrected implementation was built or tested here.
- Historical reproducibility. No historical run was re-executed.
- Scientific validity of any reading. Containment withdraws broken
  certifications; it does not grade the readings themselves. The
  per-anchor audit that would do that, within its limits, is WP5 and
  remains open.
- The deposited-PDF comparison (10.9) and the UI/report-index
  reconciliation (10.1) remain open evidence items, named above.
