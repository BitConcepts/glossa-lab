# Stage T701 record — closeout (Spec 087)

**Stage:** closeout (task T701, plus the T304/T305
dispositions). **Branch:** `feat/087-t701-closeout`, built on
main `4cffe3b2` (PR #502 merge). **Date:** 2026-11-03.
**Seat:** build worker; the parent gates and merges.

Every number in this record was read by this worker from a
tool result, a file, or a process log it inspected itself on
this branch. Commits are per item, in item order:
`78c5dc3` (item 1), `d4fb20c` (item 2), `503d663` (item 3),
`327d892` (item 4), `caffc50` (item 5), then this record.

## 1. Item 1 — shadow-trio description fidelity

The S1 record (T103) kept the live `experiment_graph_phase_misc_gaps.py`
definitions of `IndusPhase254SemanticConstraint`,
`IndusPhase255CommodityPhonemes`, and `IndusPhase256LEExtension`
byte-unchanged and deleted the dead `phase248_253` definitions,
recording that the dead definitions' names/descriptions were
the faithful ones. This item discharges that finding:
**descriptions only** — ports, params, and compute functions
are byte-unchanged (the diff is the three description strings).

The replacement text is the dead definitions' text (recovered
from the pre-S1 tree at `8445da1f`), verified against the
scripts before adoption:

- **254** — the script's upgrade gate is domain-matched motif
  enrichments at chi2 > 6.64 and lift > 2.0
  (`phase254_semantic_constraint.py`, "For upgrade: require
  chi2 > 6.64 (p < 0.01) AND lift > 2.0" and the candidate
  loop over `domain_matched`); motifs unicorn/zebu/elephant/
  rhino/tiger per its docstring and MOTIF_DOMAINS.
- **255** — AST count of the script's `COMMODITY_MAP` is
  exactly **16** entries (carnelian … stone standard);
  cross-reference is over zebu/bull seals with a MEDIUM→HIGH
  upgrade, per its docstring and map.
- **256** — the script's upgrade path is recorded in its own
  upgrade log as `"LE+DEDR+McAlpin"` with the basis text
  "Linear Elamite (E41) + DEDR … + McAlpin Elamo-Dravidian
  bridge"; the extended-LE phoneme mapping survives as
  analysis output (`le_matches`).

Pins checked before editing: no test or fixture pins
description text for these ids — the registry-integrity and
palette-curation tests pin ids, counts, categories, and
compute-function provenance only. The generated manual
surfaces were regenerated with the S4 generator after the
edit: **byte-identical output** (no diff in
`docs/user-manual.md`, `docs/USER_GUIDE.md`, or
`nodeReference.generated.ts`). The reason is mechanical and
is recorded against the closeout brief's expectation: the
trio are legacy-flagged census wrappers, and the generated
node reference covers the palette set only, so their
descriptions never entered the generated surfaces. Generator
`--check` OK; manual conformance 7 passed.

## 2. Item 2 — PR-B record wording correction

Appended to PR-B's section of
`records/stage-s3-conversions.md`, immediately after the
paragraph it corrects, as an explicit dated note
(2026-11-03, parent ruling): the "was copied into the pre
worktree" sentence is wrong in the same way PR-C's section
was corrected for — the copy failed (a fresh worktree has no
`backend/data/`), the pre side read ABSENT CGSA tables, the
post side read the clone DB's EMPTY tables, and absent-vs-
empty is the same exercised state, so the equivalence
conclusion stands. The section's original text is
unrewritten; the note is the correction of record.

## 3. Item 3 — fallback-retirement reconciliation

PR #493 (merge `16f61755`), "Spec 087 S3: retire the silent
Holdat fallback (owner-approved)", was S3 work that sat
outside the conversions narrative. A reconciliation entry is
appended to `records/stage-s3-conversions.md` naming it as
S3 family work with its PR and record pointers
(`records/stage-s3-m77-fallback-retirement.md`), and
tasks.md T303 carries the pointer annotation. It was a
behaviour change to a PR-A-converted node's engine (the
JsonCorpusLoader first-existing-source loop), executed under
the owner's 2026-11-03 approval, answering the Step 0
record's fallback question; it moves no S3 count and T303's
completion arithmetic is unchanged.

## 4. Item 4 — PR-A fitz fix (route: reasoned exception)

**Mechanism, pinned:** `pymupdf>=1.24,<2` is declared under
`backend/pyproject.toml`'s `ocr` optional extra; CI installs
only `.[dev]`. CI is therefore the fitz-free environment —
the opposite of the PR-A test file's original comment ("the
CI venv installs it from pyproject; the local glossa-ci venv
does not"). PR #499's first CI run disproved that comment for
the PR-F file; the same correction applies here.

**Fix:** the two-page fixture PDF is committed as base64 in
`backend/tests/test_spec087_s3_conversions.py` (1,203 bytes,
SHA-256 `b677341cc62409cdbf83c9de3d60fbbba406cf73f9dff33032803a55a0fb47c3`,
produced with the exact former run-time recipe — `*.pdf` is
gitignored, so the bytes could not be committed as a file),
materialized into tmp_path per case; wherever PyMuPDF is
present the materialized document's real page count is
asserted against the pinned count (2). The false comment is
replaced with the true mechanism.

**Route on the stand-in question — reasoned exception, no
stand-in.** PR-F's repair installs a minimal stand-in `fitz`
where the library is absent, and that is sound there because
the pixmap bytes the stand-in fabricates feed only a data
URI handed to an already-stubbed vision call that ignores
them; every compared output is produced by the node's own
real logic. `PDFTextExtractor` is the opposite shape: its
whole function is fitz (`doc.page_count`,
`doc.load_page(i).get_text("text")`), and the pinned outputs
ARE the extracted texts, down to fitz's trailing newline
("Glossa fixture page one\n"). A stand-in would have to
return those very strings, and the test would compare the
fixture against itself — circular, pinning nothing about
extraction. So: where fitz exists, the pdf cases replay the
committed bytes byte-identically (full mode, unchanged
expectations); where fitz is absent, the node's designed
behaviour — its `{"error": "PyMuPDF not available: …"}` dict
(the node checks file existence before its lazy import, so
the materialized PDF is what carries execution to the
import) — is the pinned expectation, asserted exactly
(result key set and error prefix), not probed loosely.

**Proofs, both environments** (this branch): fitz present —
**42 passed** (the full file, pdf cases in full replay).
Fitz BLOCKED via a sitecustomize setting
`sys.modules["fitz"] = None` (block verified live in that
environment: `import fitz` raises `ModuleNotFoundError:
import of fitz halted; None in sys.modules`) — **42
passed**; the two pdf cases also run named — **2 passed**.

## 5. Item 5 — USER_GUIDE §16 disposition

Every name in §16's "Evidence Graph in the Experiment
Builder" table was checked against the live registry. All
seven display names match the seven registered `Evidence
Graph` nodes exactly:

| Table name | Registered id | Legacy |
|---|---|---|
| Literature Loader | IndusLiteratureLoader | yes (S3 conversion, PR-F) |
| Claims Loader | IndusClaimsLoader | yes (S3 conversion, PR-F) |
| Cross-Hypothesis Matrix | CrossHypothesisMatrix | no |
| Hidden Hypothesis Generator | HiddenHypothesisGen | no |
| Claim Tester | IndusClaimTester | yes (S3 conversion, PR-F) |
| Null Model Test | IndusNullModelTest | yes (S3 conversion, PR-E) |
| Intake Runner | IndusIntakeRunner | yes (S2 census-wrapper flag) |

`BuiltinCorpus` in the section's pipeline line also exists
("Built-in Corpus", palette). **No name in the table is
false; the table stands unedited.** What had gone stale is
the framing sentence — "the palette category … provides 7
atomic nodes" — when only two of the seven are in the
default palette after S3. The minimal edit corrects the
framing and adds a short note recording the true state
(four S3 conversions delegating to palette primitives; the
Intake Runner S2-flagged with its own implementation; all
five still registered and resolvable). Manual conformance
green after the edit (the §16 table is prose outside the
generated blocks). Disposition recorded here per the brief.

## 6. T304 — complete by vacuity, with one named supersession

T304 covers re-expression PRs for disposition (b). No such
PRs exist, because no (b) disposition was ever assigned:

- In the 68, every CONVERT entry in the triage record names
  a target primitive — form (a). The family table (triage
  §5) is 14 families of (a) conversions/relabels, and the
  strongest (b) candidate was weighed expressly: H1
  (triage §3) found StructuralTemplateAnalyzer's conversion
  is "(a) a generic TemplateMiner primitive rather than a
  pure (b) graph re-expression".
- The one place a (b) path was ever named is triage §4.7,
  for the two live WRAPPERs **outside** the 68
  (DravidianSyllableLM, KalyanCrossValidation): "the natural
  path … is composition (b) in their consuming graphs". That
  path was superseded by the parent's 2026-11-03
  conversion-contract ruling, and both wrappers were
  executed as (a) conversions in PR-F (SyllableLMLoader,
  LexiconCrossValidator; byte-identical fixtures; graphs
  unchanged). Supersession by recorded ruling, not silence.

T304's acceptance mode (test) has no object: there is
nothing to re-prove per PR because there are no (b) PRs.
Ticked complete on this evidence.

## 7. T305 — domain-branch scan executed; comparison leg cited

**Scan (executed at closeout, 2026-11-03, on this branch).**
Population: the CONVERTED_IDS sets pinned by the six batch
test files = 64 registered fns (62 conversions + the 2 F15
wrappers), plus the 2 F14 relabels = **66 fns**, sources read
via `inspect.getsource` on the live registry's defs. Every
conditional line (`if`/`elif`/`while`, ternary) was
extracted: **11 conditional lines in total** across all 66
fns — ICITCorpusLoader and MathematicaEpigraphicaLoader
(`if not p.is_absolute()`), IndusSignRoleClassifier
(`if "numeral_signs" not in merged`), LegacyPhaseScriptRunner
(script_path/output existence and output-type checks),
PDFTextExtractor (file_path presence/existence). Results:
**0** conditional lines name a domain identity (language,
corpus, scholar map, sign system — regex over dravidian,
tamil, sanskrit, ugaritic, elamite, semitic, indus, cisi,
mahadevan, holdat, parpola, fuls, kalyan, meluhha, desset,
mcalpin, dedr, harappan, pali); **0** conditionals compare
against a string literal at all. Every conditional found is
input hygiene (path absoluteness, param presence, file
existence, output type). **Scan clean; no residual.**

**Comparison leg:** the S3 leg of the C087-13 comparison
runs is the per-batch record set — S2's pinned runs plus
PR-A…PR-F, each 27/27 byte-identical under the two named
normalizations (LanguageModel repr addresses; each tree's
own root path), tabled in `records/stage-s3-conversions.md`.
PR-E's within-batch scoping and PR-F's no-cross-batch-
equality statement stand as recorded there.

**68-row disposition table:** the triage record
(`records/stage-s3-triage.md` §5, per-node entries) plus the
per-batch sections of the conversions record are together
the S3 stage record set T305 names; T303's completion note
carries the arithmetic (64 CONVERT discharged, 4
RETIRE-CANDIDATE flagged, 0 RETAIN).

## 8. Final registry census (live, counted on this branch)

Counted from the live registry (never arithmetic):
**556 registered / 425 legacy / 131 palette / 81 core /
65 categories.** (Core, by the program's established
counting: defs whose compute fn lives in
`experiment_graph.py` itself — 42 — plus the generic
machinery modules `generic_loaders.py` /
`generic_primitives.py` — 39.) This closeout moves no count
(descriptions, records, and test-fixture changes only), so
the census pin needs no re-pin; the registry-integrity pin
(556, per-category) passes unchanged in §11's runs.

## 9. Claim assessments — final (all 17)

Stage-record assessments stand as recorded; this section is
the closeout roll-up T701 requires, with pointers.

- **C087-1 — SUPPORTED.** S1: completeness pin over the 144
  loader-derived modules and the by-category census;
  strict fail-fast + registry-health surface
  (`records/stage-s1-record.md`).
- **C087-2 — SUPPORTED.** S1: dead definitions deleted,
  duplicate guard + provenance pins; the description-
  fidelity gap S1 recorded is closed by §1 of this record.
- **C087-3 — SUPPORTED.** S1: palette error state with
  retry, Playwright-proven (`stage-s1-record.md`).
- **C087-4 — SUPPORTED.** S2: palette = registry minus
  legacy, mechanically (`records/stage-s2-record.md`).
- **C087-5 — SUPPORTED.** S2: resolution sweep; nothing
  stored dangles (`stage-s2-record.md`).
- **C087-6 — SUPPORTED.** S3 triage: 68 dispositioned
  exactly once on evidence; zero (c) retentions, so T302
  closed by vacuity at the parent's gate
  (`records/stage-s3-triage.md`).
- **C087-7 — SUPPORTED.** Conversions complete (PR-F
  assessment) and the closeout scan (§7) finds no
  domain-identity branch in any converted source.
- **C087-8 — SUPPORTED AS SPECIFIED.** S4
  (`records/stage-s4-record.md` §5).
- **C087-9 — SUPPORTED AS SPECIFIED.** S4 (phantom census
  0 across surfaces; experiment list generated = 27); §16's
  table additionally verified name-by-name at §5 here.
- **C087-10 — SUPPORTED.** S5: Logs view built to the
  approved wireframes, Playwright comparison with seven
  differences named (`records/stage-s5-record.md`).
- **C087-11 — SUPPORTED.** S5 T503: D2 documented-ephemeral
  statement in module docstring, user-manual, and HelpView,
  pinned by test (`stage-s5-record.md`).
- **C087-12 — SUPPORTED AS SPECIFIED.** S6: 96 exact
  duplicates deleted via the API only, 104 → 8, distinct
  content unchanged, every removed id recorded
  (`records/stage-s6-dedupe-record.md`).
- **C087-13 — SUPPORTED.** S2 + PR-A…PR-F comparison runs,
  27/27 each under the named normalizations (§7).
- **C087-14 — SUPPORTED, scoped as follows.** No Spec 087
  stage altered any Indus claim's status, stage, or score,
  and no freeze record was modified: git history shows the
  only program commit touching
  `glossa-indus/ledger/claims.jsonl` is the adoption intake
  itself (`b8c9ae7`, appending this spec's own 17 claims
  through the sanctioned bundle intake, before any stage
  ran, recorded in `records/adoption-2026-11-02.md`); every
  stage record carries its gate-neutral diff statement.
- **C087-15 — SUPPORTED.** Each stage's manual leg is
  assessed in its stage record (S1 named why the T105
  rename has no manual surface; S2–S6 carried their updates
  in-PR); this closeout's own manual-affecting items (§1
  regeneration, §5 framing fix) land in this same PR.
- **C087-16 — SUPPORTED.** S1 T105 rename, endpoint
  unchanged (`stage-s1-record.md`).
- **C087-17 — SUPPORTED.** Every count change in the
  program landed with its re-pin and stage record (the
  census fixture's comment chain S1 → S2 → PR-A…PR-F);
  this closeout moves no count (§8).

## 10. Audit findings F1–F10, re-scored at closeout

Source: the 2026-11-02 coupling audit (`AUDIT.md`, goal
workspace `hidden_files/system-coupling-2026-11-02/`).

- **F1 (registry sprawl, silent shrink) — CLOSED as a
  mechanism.** The count grew 517 → 556, every step a
  recorded re-pin of new generic primitives; the silent-
  shrink mechanism is gone (completeness pin, strict
  fail-fast, registry-health). Registry size post-curation
  is a fact (131 palette), not the defect F1 named.
- **F2 (silent shadowing) — CLOSED.** One definition per
  id, guard-pinned (S1); description fidelity restored (§1).
- **F3 (wrappers are not primitives) — CLOSED for the
  tractable population, residual by design.** 359 wrappers
  legacy-flagged out of the palette (S2); the 68 PARTIAL
  genericized (S3); both live wrappers converted (PR-F).
  The remaining flagged wrappers stay registered and
  resolvable as historical study nodes — decision D1's
  flag-not-delete design, not an open defect.
- **F4 (live working set small, mostly generic) —
  CONFIRMED AND PRESERVED.** 27 graphs, zero dangling refs
  at every stage; byte-identical comparison runs per stage;
  the live domain-flavoured ids were triaged first.
- **F5 (palette = registry; silent-empty defect; naming
  collision) — CLOSED.** Error surface with retry (S1);
  palette mechanical (S2); `study_node_registry.py` rename
  (S1).
- **F6 (Logs surface write-only; events bus in-memory) —
  CLOSED.** Logs view restored per the approved wireframes
  (S5); the events bus carries the D2 documented-ephemeral
  statement in docstring + manuals, pinned by test.
- **F7 (manuals stale) — CLOSED for enumerable content;
  one named residual.** Generated reference + CI conformance
  (S4); phantom names at 0; USER_GUIDE lists the real 27;
  §16 dispositioned (§5). Residual: deeper pre-081
  walkthrough prose was not re-audited line by line (S4
  record §6.1) — carried at §12, owner: a future
  manual-prose audit; not claimed closed here.
- **F8 (manual work intact; anchor sets duplicated) —
  CLOSED on the dedupe leg.** S6: 104 → 8 via the API,
  distinct content unchanged, foundation check re-run PASS.
  The caveat F8 itself carried — the Oct-30 VM snapshot's
  divergent lineage — is a pre-existing owner question the
  audit named and this program never undertook; §12.
- **F9 (no governing spec) — CLOSED.** Spec 087 is the
  governing spec for the node system; this record discharges
  it.
- **F10 (feature inventory; one orphan surface) —
  CLOSED.** The single orphan (the terminal-log viewer) is
  restored (S5); the program added exactly two surfaces,
  both recorded (registry-health endpoint, S1; the Logs
  tab, S5).

## 11. Test evidence (this PR)

All runs on this branch, venv `glossa-ci`, outputs read by
this worker from the process/log output itself:

- Spec 087 targeted set (`-k "spec087 or spec086 or
  terminal"`): **429 passed, 2 skipped, 2185 deselected**
  (249.46s) — the same profile as S5's corrected record.
- Manual conformance + registry integrity + palette
  curation (item 1 gate): **33 passed**; generator `--check`
  OK after regeneration.
- PR-A conversions file, both environments (item 4): **42
  passed** with fitz present; **42 passed** with fitz blocked
  (block verified live); pdf cases named under the block:
  **2 passed**.
- Full backend suite, one run, no `-x`, log read from
  `tmp-suite/t701-fullsuite.log`: **1 failed, 2530 passed,
  84 skipped, 1 deselected, 1 error in 247.39s**. The one
  failure is the named phase133 local-only baseline
  (`test_phase133_stage0_inventory.py::
  test_builder_recomputation_skips_without_inputs` — missing
  local download; green in CI). The one error is the tray
  teardown flake family
  (`test_tray_token_auth.py::
  test_copy_api_token_without_tkinter_is_named`, sqlite
  closed-database at teardown); standalone rerun of that
  file: **14 passed**. The one deselection is the named
  phase392 determinism test
  (`test_phase392_q2_gate.py::
  test_pipeline_deterministic_under_seed`), whose
  authoritative runner is CI.
- Ruff (CI scope, `ruff check backend/`): **all checks
  passed**.
- In-tree regenerations from the suite runs
  (`glossa-indus/claims/extracted_claims/*`,
  `outputs/partial_loop_result.json`) were restored via
  `git checkout` and are not in this PR's diff. The §1
  manual regeneration produced no diff (recorded there).

## 12. Residuals carried out of the program (named, owned)

1. **Pre-081 walkthrough prose** (from F7 / S4 §6.1):
   panel-interior prose in the manuals was not re-audited
   line by line. Owner: a future manual-prose audit. Not a
   Spec 087 task; not claimed closed.
2. **Data-lineage question** (from F8): the Oct-30 VM
   snapshot's thinner dataset vs the live desktop DB remains
   unadjudicated. Owner: the owner (pre-existing open
   question; both datasets preserved). Outside this
   program's scope by the audit's own framing.
3. **Retire-candidates stay flagged, never deleted**
   (Phase22Verdict, Phase23Verdict, Phase24Verdict,
   ShuIlishuCandidateFilter): executed per the owner's
   2026-11-03 ruling (flag, not delete). Any future deletion
   needs its own owner ruling.

## 13. SPEC 087 COMPLETE

Stages S1–S6 and this closeout have discharged every task
in `tasks.md` on the evidence in the stage records: the
registry is pinned and cannot shrink silently (S1); the
palette is the registry minus legacy, mechanically (S2);
every PARTIAL domain node was triaged once and converted,
relabelled, or flagged on byte-identical fixture evidence,
with no domain-identity branch left in a converted source
(S3, §7); the manuals' enumerable content is generated from
the registry and conformance-pinned in CI (S4); the Logs
surface is restored to its approved wireframes with the
events bus's semantics stated and pinned (S5); the live
anchor sets hold only distinct content, deduped through the
API on the record (S6). Claims C087-1…17 are assessed at §9.

Per T701's own bound, this establishes that **this
program's contract is discharged on its evidence** — not
that the system is finished. The residuals at §12 are the
named remainder.
