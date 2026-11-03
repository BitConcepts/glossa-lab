# Stage S2 record — palette curation (Spec 087)

**Stage:** S2 (tasks T201–T206). **Branch:**
`feat/087-s2-palette-curation`, built on main `dea267f8`
(PR #488, Spec 087 S1). **Date:** 2026-11-02. **Seat:** build
worker; the parent gates and merges.

## What was built

### T201 — The `legacy` flag and the migration data

`AtomicNodeDef` gains a `legacy` attribute (constructor
keyword, default `False`), carried in `to_dict()`. The flag
is applied at registry build, not per registration site:
after the last plugin block and before the build closes,
`_apply_legacy_flags()` reads the committed migration data
file `backend/glossa_lab/spec087_s2_legacy_ids.json` and
flags every listed id on its registered definition. A listed
id that is not registered is recorded through the S1 failure
channel (`_record_registration_failure`), so strict contexts
refuse to start over a migration/registry drift and lenient
production names it at ERROR plus the registry-health
report. `ATOMIC_NODES` keeps all 517 entries — the flag is
the only change to the definitions, and resolution and
execution consult the same table as before (decision D1(a)).

The migration data file was generated mechanically from the
classification of record — the system-coupling audit census
(2026-11-02) Appendix A — by extracting every row whose
§4.3 param-carry verdict is WRAPPER: **359 ids**, committed
in census order, reviewable id by id (the full list is
Appendix A of this record). The file is the act's data; any
future change to it is a recorded act (C087-17).

**The one discrepancy, named rather than absorbed.** The
census's runtime counts (§4.3) say 360 registered nodes have
both no input ports and an empty params schema, while its
WRAPPER class holds 359. Recomputed live at this stage, the
shape set is exactly 360, the flagged set is exactly the
census's 359, and the symmetric difference is a single node:
**`ResearchLoopRunner`**. The census classes it GENERIC
(Appendix A row 490; a core node defined in
`experiment_graph.py` itself), and WRAPPER is a verdict over
DOMAIN nodes — census-evidence Table 1 nests it under
DOMAIN ("of which WRAPPER"). So the census's rule is
two-stage — DOMAIN (§4.1) ∧ wrapper shape (§4.3) — and the
flagged set follows the census, not the bare shape. The
agreement test (`test_flagged_set_matches_the_wrapper_rule`)
pins all three facts: every flagged node has the wrapper
shape; every shaped node is flagged except the one named
exception; the exception is unflagged. A future node that
breaks the identity in either direction fails CI by name.
`ResearchLoopRunner` stays in the palette (the frontend e2e
suite asserts its catalog presence, and it passes).

**Two flagged nodes are in the live working set.**
`DravidianSyllableLM` and `KalyanCrossValidation` are used
by live graphs (1 instance each) and are classed WRAPPER by
the census (no inputs, no params — the domain content is the
implementation), so they take the flag like every other
wrapper. This is the census and the approved 359/158 pin
speaking, not an oversight: both stay resolvable, both
graphs' comparison runs are byte-identical after the change
(T204 below), and Stage S3's triage takes the live
domain-flavoured ids first (T301), which is where their
dispositions are decided.

### T202 — Catalog filtering

`GET /experiment-graphs/catalog` gains
`?include_legacy=true`. The default response is the palette
set — exactly the registered nodes not flagged legacy
(**158**); with the opt-in it returns the full registry
(**517**, of which 359 entries carry `legacy: true`). Every
entry carries its `legacy` flag. Verified three ways: the
API-function level, the pytest client, and live HTTP against
a locally started backend (verbatim output under Test
evidence).

**No builder-UI change in this stage.** Plan.md's S2
contents state it directly: "No frontend change beyond the
manual-level copy; if the builder UI gains a legacy
affordance it is out of this stage's scope by design." The
palette simply renders the default (filtered) catalog, as it
already renders whatever the catalog returns; the opt-in is
an API surface for diagnostics. No `frontend/dist` rebuild
was needed (no frontend source changed).

### T203 — Resolution sweep

`test_every_stored_graph_resolves_against_the_full_registry`
loads all 27 stored graph fixtures
(`backend/glossa_lab/experiments/graphs/*.json`; the
`_archive/` folder is out of scope per the spec's non-goals)
and resolves every node's atomicId against `ATOMIC_NODES`:
36 distinct atomicIds, zero dangling. `SubExperiment`
targets resolve to a stored graph id or to the built-in spec
library the seeder materializes into the graph library
(`tier3_sumerian_validation` is the one such reference).
Execution leg: a saved-form graph naming the legacy type
`ICITMetadataLoader` runs through `execute_graph` and returns
the node's own result — the flag removes the palette offer,
never the resolution.

### T204 — Comparison runs over the 27 live graphs

Method: each graph executed with the same dispatch
`execute_graph()` uses (same topo sort, same
`ATOMIC_NODES[id].fn` calls), capturing **every** node's
result dict (not only the merged output), canonicalized as
JSON (sort keys) and hashed per graph. The pre-change pin
was taken at stage start on unmodified main and **re-pinned
by the act of this stage's start** (the audit baseline held
graph definitions, not outputs), then the post-change run
was compared against it.

Control experiment, run before any code change: two
executions of all 27 graphs on unmodified code. 17 graphs
were byte-identical raw; the other 10 differed at exactly
one kind of path — an LM node's `lm` field, whose value is
the `repr()` of a `glossa_lab.pipelines.decipher.LanguageModel`
object, e.g. `<glossa_lab.pipelines.decipher.LanguageModel
object at 0x7755ced82840>` vs `… at 0x7b8cf725c3e0>`. The
only run-to-run variance in the entire working set is a
process memory address — not result content. The comparison
therefore normalizes exactly that pattern
(` object at 0x[0-9a-f]+>` → ` object>`) before hashing;
under it, the two pre-change runs agree on all 27 graphs,
and the post-change run agrees with the pre-change pin on
all 27:

| graph | normalized sha256 (pre == post) |
|---|---|
| fuls_independence_suite | cb52a39e0d2e9e2078044f442ea52b32a84d545f8431f48eaece0f8854859cfb |
| fuls_nw_semitic_benchmark | 6d118312cd03257e622af114fc335a49924aa040ec5e2819ef0d10961e1be479 |
| fuls_validation_suite | 437a2a1c961588de865ffcc6810064971d440286fdd12cbc09150a905df5cc01 |
| generic_sa_multi_comparison | 1e912af2b3b56c7e9d4e40cea79a50d7462127465cf9a2210a27b4e1e3341750 |
| indus_anchor_sweep | bd48265a45cc82deea639f4f6a81c062f24bde57840b7266d807a62c54fc4a49 |
| indus_cgsa_cluster_analysis | 4dec998157aa95f86c4234f83a151a3b18bd7e906f22db176c0da4daa9c0818b |
| indus_cisi_anchored_10 | 6da9fc43759bc55706eba6fed02c7ce32954bd6b3b04b34f4e285d58f85214a6 |
| indus_cisi_dravidian_vs_pali | 2c0eabe7a99f32855a66a7e1d1b7ff26f541e57298f20ef96f1c4a3308341891 |
| indus_cisi_dravidian_vs_sanskrit | 8c547ad0006160185d27c0e9bc43709f4a42dbe4ffa561a969adaa8ca27cdeea |
| indus_cisi_sa_dravidian_vs_nw_semitic | 1ad9de1c0a719ab499767edf4be1c45f870fc8c9aa13d59d0db417fbec675145 |
| indus_cisi_sa_dravidian_vs_sanskrit | ffc95b065afe0e85deb686fb318374f8f9512ed28ef223421981d3ae5ca36346 |
| indus_cisi_structural | a8caf36fa8bde2bfe9934f0c0d3bdcec9bcb4ff76cb759319a66d64cd7029ecd |
| indus_contact_zone_v2 | ed731e064c2d0c6dd830c038baaa3016d2f8ad9faeb1392895713b3003fda2fc |
| indus_dravidian_vs_sanskrit | 17a3cc9fae33b95a57dc066edad54cb59d35f1dc23d855a63cfb502c8403a164 |
| indus_kalyanaraman_crossval | cf2adbc08f1b66fd01f9e7c9adee216dcf1850769bee7694c613a2335ba2c3e5 |
| indus_sa_dravidian | effafae6b3d2e97f27f5ee3882b912bffd44714b04d951fff55de12dc6c06169 |
| indus_sa_dravidian_syllable | 68c6fc770715f8d9a24d136f8e6d5e8c482fff094cda1b9ae6e9345a2bb4ac4e |
| indus_sa_dravidian_vs_nw_semitic | f7639e33f3332dd257de73ef07bc0d053c99f2cd5f5a4072a7ef9824bef2fd3b |
| indus_sa_dravidian_vs_sanskrit | c8401cdda8f996eef02afad648597af87f2fb2398fed9d809379c71bc3855161 |
| indus_sa_sanskrit_falsification | 65d8cede72810c421a40275f079d048f55c82dceb64034d82502c1c18b82aead |
| indus_sign_function_dravidian | 2dcc11669d10d232120bbb82d0556ef0f10b86150a07f3268b9dc942f77e7380 |
| indus_structural_atlas | 77479ecea27e3920cb3bafd3df206f83f6b06e3d58eb721c61bed65de0c6d39f |
| indus_validation_a1_a3_holdout | c6422f898d11459636f116df51ea1a24ec02024d28068d0d7b32942297a8023d |
| indus_validation_neg_controls | 0ab2c5a36544fdda06441c77be849fbce511f123fa417e3924a9c8dfb5f9072d |
| kl_comparison | cf9a8e10b3043bc8942c29483118739688a02439fe20d5237f9d98e1647cca9c |
| ugaritic_sa_decipher | b9f524251337048bc3a1ef5dbd6982f18d644634c0a7b06661c87c617f7f52bc |
| ventris_validation | d51a30ab7b17ae1ee904ea6396cb4e2a5200e259e510bb59f811763b1825f572 |

**Result: 27 of 27 byte-identical, pre vs post** (full
digests, machine-compared over the canonical outputs:
0 differing). The
runs regenerate `reports/*.json` and
`outputs/partial_loop_result.json` in-tree as a side effect
of executing the graphs; those files were restored
(`git checkout --`) and are not in this stage's diff.

### T205 — The three-way re-pin

The census pin fixture
(`backend/tests/fixtures/spec087_registry_census.json`) is
extended in place — the recorded act C087-17 requires — with
`legacy_total` 359, `palette_total` 158, and per-category
splits `by_category_legacy` / `by_category_palette`, counted
from the live flags and cross-checked against the S1
per-category totals (legacy + palette == registered for all
66 categories). Shape of the split: legacy spans 23
categories, the palette 51; the "Indus Decipherment"
category is 319 of 319 legacy. The registry build report and
`registry_self_check()` carry the same three-way split
(`legacy`, `palette`; `legacy_total`, `palette_total`,
`legacy_mismatch`), and the self-check now fails if the
flagged set and the migration data disagree in either
direction.

### Manual (C087-15, S2 leg)

`docs/user-manual.md`, "Using the Builder": a **Legacy
nodes** paragraph after the S1 palette note — what legacy
nodes are (older single-study nodes, nothing to wire or
configure), why they left the Palette (the Palette is the
composable building-block set), that nothing is deleted and
saved experiments using them still open, run, and produce
the same results, and the `?include_legacy=true` API opt-in
for diagnostics. The Node Reference section is untouched
(S4 owns it), as is HelpView.

## Test evidence

New suite `backend/tests/test_spec087_palette_curation.py`
— **10 passed**: migration set == flagged set counted both
ways; the wrapper-rule agreement with the named
`ResearchLoopRunner` exception; the S1 shadow trio flagged
with misc_gaps provenance unchanged; catalog default ==
palette exactly (158, no legacy entry, no missing
non-legacy); `include_legacy` == full registry (517, the 359
flagged entries exactly the flagged set); the three-way pin
(totals + per-category, summed back to the S1 totals);
registry-health split over HTTP; the self-check's legacy
agreement; the 27-graph resolution sweep (36 atomicIds, zero
dangling, SubExperiment targets resolved); the legacy-type
execution proof.

Run together with the S1 suite: **26 passed**. Targeted
backend areas (test_catalog, test_experiment_graph,
test_graph_experiments, test_atomic_nodes,
test_evidence_atomic_nodes): **148 passed, 1 skipped**.

Full backend suite, local, no `-x`: **2246 passed, 84
skipped, 1 failed, 1 deselected** (240.9 s). The 1 failure
is the known phase133 environmental baseline
(`test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`
— missing local download; does not fail CI). The 1
deselected test is
`test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`,
excluded per the standing stage instruction: it stalls for
tens of minutes on this shared VM (verified pre-existing on
pristine main at S1); CI is its authoritative runner. No
tray teardown error appeared in this run.

Frontend: no source change (see T202). Builder-area
Playwright against a locally started backend
(PLAYWRIGHT_USE_BACKEND=1): `experiment-builder.spec.ts` +
`palette-error.spec.ts` — **25 passed, 1 skipped** (the
conditional inspector test, as at S1). The palette tests now
run against the filtered 158-node catalog.

Live HTTP verification against the same local backend:

```text
GET /experiment-graphs/registry-health
{"ok":true,"registered":517,"legacy":359,"palette":158,"failures":[],"duplicates":[],"strict":true}
GET /experiment-graphs/catalog                 -> 158 entries
GET /experiment-graphs/catalog?include_legacy=true
                                               -> 517 entries, 359 legacy-flagged
```

Ruff: `python -m ruff check backend/` — all checks passed.

## Gate-neutral statement

S2 changes no Indus claim content. The PR diff names no
files under `glossa-indus/ledger/`, `glossa-indus/matrix/`,
or `glossa-indus/map/` (verified from the branch diff
against `origin/main` before push). Test and comparison runs
regenerated some `glossa-indus/claims/…` and `reports/…`
files in-tree transiently; they were restored
(`git checkout --`) and are not in the diff.

## Claim assessments (stage scope)

- **C087-4 — SUPPORTED at S2 scope.** The flagged set is
  exactly the census's WRAPPER set (migration data counted
  both ways; the shape rule recomputed live with the one
  named GENERIC exception), and the catalog's default
  response is exactly registry-minus-legacy while
  `?include_legacy=true` returns the whole registry — the
  palette is computed from the registry and the flag, never
  maintained as a list.
- **C087-5 — SUPPORTED at S2 scope.** `ATOMIC_NODES` is
  unchanged as the one resolution table (517 entries before
  and after); the sweep resolves all 27 stored graphs'
  references, and a graph naming a legacy type executes it.
- **C087-17 — S2 leg discharged.** The re-pin is this stage's
  recorded act: totals and per-category counts moved only in
  the dimensions S2 names (legacy/palette split added;
  registered and per-category totals unmoved), in this PR,
  with this record.
- **C087-13 — S2 leg SUPPORTED.** All 27 live graphs resolve
  every atomicId after S2, and the pinned comparison runs
  are byte-identical to their pre-stage records under the
  one named normalization (object-address reprs), which the
  pre-vs-pre control on unmodified code proved is the only
  run-to-run variance in the set.

Assessments are recorded here, in the stage record, per
this repo's stage-record convention (Spec 086 stage records;
the Spec 087 adoption record; the S1 record). `claims.md`
is not edited: its claim texts are the bundle the adoption
intake appended to the claims ledger — annotations belong
in records, not in the bundle text.

## Appendix A — The migration id list (T201/T206)

The 359 ids of `backend/glossa_lab/spec087_s2_legacy_ids.json`,
in the census's Appendix A order. The data file is the
operative record; this list is its review copy.

`DravidianSyllableLM`, `ICITMetadataLoader`, `indus_auto_decipher_loop`, 
`indus_integrated_research_loop`, `indus_mining_discovery_loop`, `indus_phase322_mega_mine`, 
`indus_phase323_330_experiments`, `indus_phase331_335_fixed`, `indus_phase336_339_unlock`, 
`indus_phase340_345_validate`, `indus_phase346_348_level3`, `indus_phase352_357_advancement`, 
`indus_phase358_362_consolidate`, `indus_phase363_370_deep`, `indus_phase371_376_exploit`, 
`indus_phase378_381_advances`, `indus_phase382_390_actionable`, `IndusAcademicPackage`, 
`IndusAcadSubmit`, `IndusADNAArchaeogeneticsMine181`, `IndusAdvancementAnalysis`, 
`IndusAdversarialBattery`, `IndusAllograph200`, `IndusAllographs`, `IndusAnchor120`, 
`IndusAnchorGap`, `IndusAnchorInjection206`, `IndusAnchorSprint120`, 
`IndusAnchorUpdateProposal192`, `IndusAnchorUpgrades128`, `IndusArthasastraMine`, 
`IndusArxivDraft`, `IndusBayesianPhylo205`, `IndusBetweennessStratification172_174`, 
`IndusBlockerTargetedSA`, `IndusBulkMine183`, `IndusBulkMine184`, `IndusCisiCrossval`, 
`IndusCisiCrosswalk116`, `IndusClaimsEval`, `IndusCollocateNetwork`, 
`IndusCommoditySemantic188`, `IndusComprehensiveVal132`, `IndusConstrainedSA`, 
`IndusContactDeep`, `IndusContactInvestigate`, `IndusCrosswalkComplete`, 
`IndusCrosswalkTop100`, `IndusDataResolution133`, `IndusDecodeBlockerAudit`, 
`IndusDEDRCatalogue`, `IndusDedrExpansion120`, `IndusDEDRLookup198`, `IndusDedrRebus`, 
`IndusDeepDive144`, `IndusDeepEvidenceMine182`, `IndusElamoAnchorInjection190`, 
`IndusElamoDravidianGap186`, `IndusEnsembleCalibration`, `IndusEnsembleDecipher`, 
`IndusEnsembleFix`, `IndusExpandedSA`, `IndusExtendedBattery`, `IndusF3Redesign146`, 
`IndusFalsificationBattery`, `IndusFalsificationSuite`, `IndusFilteredSA`, `IndusFishPolysemy`, 
`IndusFishSignBattery185`, `IndusFishSitePolysemy`, `IndusFormulaLexicon`, `IndusFormulaPilot`, 
`IndusFormulaPilot59`, `IndusFormulaSemantics`, `IndusFormulaTranslation`, `IndusFullCorpus`, 
`IndusFullEmail`, `IndusFulltextMine`, `IndusGapSprint`, `IndusGrammarExpand`, 
`IndusGrammarInfer`, `IndusGrammarLow`, `IndusGrammarReval195`, `IndusGrammarValidation191`, 
`IndusGrammarVariance170`, `IndusGulfSealFishTest`, `IndusICITCorpusPlan`, 
`IndusIconographicFormula`, `IndusInscriptionReading201`, `IndusIntakeRunner`, 
`IndusLevitReadings`, `IndusLiteratureMine`, `IndusLowToMedium`, `IndusM267Grammar`, 
`IndusM267Validation`, `IndusM293Iconic`, `IndusM293SA`, `IndusMasterScorecard`, 
`IndusMasterSynthesis169`, `IndusMcAlpinCognates204`, `IndusMediumToHigh`, 
`IndusMediumValidator`, `IndusMeluhhanNames`, `IndusMeluhhanNamesExpanded`, 
`IndusMesopotamianMine180`, `IndusMetrological203`, `IndusMine196`, `IndusMine208`, 
`IndusMorphBoundary`, `IndusMSign293`, `IndusMundaSubstrate`, `IndusNameLexicon`, 
`IndusNameSASprint`, `IndusNameSigns`, `IndusNetworkCentrality171`, `IndusNetworkDeep175_178`, 
`IndusNorthDravidianLM189`, `IndusOCR`, `IndusParpola56Expansion`, `IndusParpolaImporter`, 
`IndusParpolaPDF`, `IndusParpolarParser`, `IndusPhase109Rebase`, `IndusPhase109Rereviews`, 
`IndusPhase109SaFlags`, `IndusPhase109StagingReview`, `IndusPhase110M222Apply`, 
`IndusPhase110M222Dossier`, `IndusPhase111BlindClassify`, `IndusPhase111BlindGate`, 
`IndusPhase112BlindClassify`, `IndusPhase112BlindGate`, `IndusPhase113BlindClassify`, 
`IndusPhase113BlindRounds`, `IndusPhase113NonSaValidation`, `IndusPhase115NonSaValidation`, 
`IndusPhase116Harmonization`, `IndusPhase117WithinCompilationValidation`, 
`IndusPhase118WithinCompilationValidation`, `IndusPhase119PredHarness`, 
`IndusPhase120BhaskarTriage`, `IndusPhase125CrossCompilationPositional`, 
`IndusPhase126WellsSplitCandidates`, `IndusPhase127CrossCompilationDiagnostic`, 
`IndusPhase130IntakePack`, `IndusPhase131Attribution`, `IndusPhase132PilotMetrics`, 
`IndusPhase133Stage0Inventory`, `IndusPhase134MotifPilot`, `IndusPhase135MotifRepilot`, 
`IndusPhase136TerminalType`, `IndusPhase137SiteRepertoire`, `IndusPhase138GraffitiDescriptive`, 
`IndusPhase139CovariateAudit`, `IndusPhase140G1Controlled`, `IndusPhase141Loso`, 
`IndusPhase202BulkMine2`, `IndusPhase209AnchorM712M817`, `IndusPhase210BrahuiGenomics`, 
`IndusPhase211ComputationalSurvey`, `IndusPhase212ScaleFreeNetwork`, `IndusPhase213SARerun408`, 
`IndusPhase214FinalInjection`, `IndusPhase215PDFReport`, `IndusPhase216SARecal`, 
`IndusPhase218SiteSemantic`, `IndusPhase219ArxivDraft`, `IndusPhase220PapolaCISI`, 
`IndusPhase221P324P122`, `IndusPhase222CISIInjection`, `IndusPhase224SlotMismatch`, 
`IndusPhase225PDFReport`, `IndusPhase226P122Phonetic`, `IndusPhase227P324Formula`, 
`IndusPhase228CISITripartite`, `IndusPhase229CISIAnchorSA`, `IndusPhase230CrossRefMatrix`, 
`IndusPhase231IndirectBilingualMine`, `IndusPhase232IndirectBilingualScoring`, 
`IndusPhase233CulturalDemographic`, `IndusPhase234P324CISIExpansion`, 
`IndusPhase235ElamiteBridge`, `IndusPhase236SanskritLoanwords`, `IndusPhase237BlockerMine`, 
`IndusPhase238BlockerFollowup`, `IndusPhase239MediumBatchUpgrade`, `IndusPhase240UnlockMine`, 
`IndusPhase241_242Experiments`, `IndusPhase243Synthesis`, `IndusPhase244E41Dedr`, 
`IndusPhase245_246SACrossing`, `IndusPhase248CeilingMine`, `IndusPhase249CeilingExperiments`, 
`IndusPhase250AllographCommodity`, `IndusPhase252AllographUpgrade`, 
`IndusPhase253CISIAllograph`, `IndusPhase254SemanticConstraint`, 
`IndusPhase255CommodityPhonemes`, `IndusPhase256LEExtension`, `IndusPhase257SA137High`, 
`IndusPhase258CandidateResolution`, `IndusPhase259CeilingMine`, `IndusPhase260ArxivUpdate`, 
`IndusPhase261CoverageRecalc`, `IndusPhase262CollocateUpgrade`, `IndusPhase264SAExperiments`, 
`IndusPhase266DEDRUpgrade`, `IndusPhase270MineUpgrade`, `IndusPhase272FinalUpgrades`, 
`IndusPhase275EvidenceSynthesis`, `IndusPhase278CompetitorMine`, `IndusPhase279PaperAnalysis`, 
`IndusPhase280DeepMine`, `IndusPhase281YajnadevamCorpus`, `IndusPhase284FullYajnadevam`, 
`IndusPhase288ExpandDecipherment`, `IndusPhase292CandidateUpgrade`, `IndusPhase294Final12`, 
`IndusPhase295BulkMine`, `IndusPhase296MineCrossref`, `IndusPhase297GapAnalysis`, 
`IndusPhase298DeepMundaArchMine`, `IndusPhase299MundaLM`, `IndusPhase300CompetingSA`, 
`IndusPhase301MundaSubstrate`, `IndusPhase302ArchaeologyScoring`, 
`IndusPhase303AnchoredMundaSA`, `IndusPhase304AllographValidation`, 
`IndusPhase305CrossResearcher`, `IndusPhase306SemanticCoherence`, `IndusPhase307DEDRCoverage`, 
`IndusPhase308ElamiteBaseline`, `IndusPhase383PilotRescoring`, `IndusPhase384Stage2Margins`, 
`IndusPhase385G1Margins`, `IndusPhase386ReplayAudit`, `IndusPhase391Stage0Spine`, 
`IndusPhase392Q2Gate`, `IndusPhase393HarappaRobustness`, `IndusPhase394SpineExtension`, 
`IndusPhase395Q7Execution`, `IndusPhase396Pred006Scoring`, `IndusPhase397LanguageComparison`, 
`IndusPhase398MatchedObjectAttribution`, `IndusPhase399Pred010Scoring`, 
`IndusPhase400Pred011Scoring`, `IndusPhase401Pred007Census`, `IndusPhase402Concordance`, 
`IndusPhase403GazetteerAssignment`, `IndusPhase404FishCoastalStep0`, 
`IndusPhase405HornedTigerConcordance`, `IndusPhase406RoifLedgerStep1`, 
`IndusPhase406RoifLedgerStep2`, `IndusPhase407ArmBObjectTypeSplit`, 
`IndusPhase408FishFamilyStep0`, `IndusPhase409RoifArrowSign`, `IndusPhase410Pred012Step0`, 
`IndusPhase411HuntDepictedStep0`, `IndusPhase413YadavZipfControls`, 
`IndusPhase414Sign900Numeral`, `IndusPhase418Sign821Recovery`, 
`IndusPhase419FiveSourcesHeading`, `IndusPhase420TranscriptionDisagreement`, 
`IndusPhase421F1ObjectJoin`, `IndusPhase422F2MarginCurve`, `IndusPhase423ArmAPrecision`, 
`IndusPhase424ArmAPrecisionRepair`, `IndusPhase425Sign821Identification`, 
`IndusPhase426Sign297ConcordanceSuccessor`, `IndusPhase427S1S5Heading`, 
`IndusPhase428CatalogueExtension`, `IndusPhase429F1EnlargedJoin`, 
`IndusPhase430YadavZipfControls`, `IndusPhase431FishFamilyProfiles`, 
`IndusPhase432AssetABuild`, `IndusPhase433OpeningSigns`, `IndusPhase434SkySigns`, 
`IndusPhase435SitePeriodMapping`, `IndusPhase436KeyingSurfaceRepair`, `IndusPhase437FarmerNB1`, 
`IndusPhase438YadavOpeningClosing`, `IndusPhase439G1ChronologyControlled`, 
`IndusPhase440HuntOpeningSigns`, `IndusPhase441DepictedKindEndingsAtlas`, 
`IndusPhase44Infrastructure`, `IndusPhase45FishCoastal`, `IndusPhase46ContactZone`, 
`IndusPhase47PhonemeAssign`, `IndusPhonExhaust`, `IndusPhonologicalGap`, `IndusPhonologyRecon`, 
`IndusPhonotactic`, `IndusPhonotacticSibilant`, `IndusPlaceFormula`, 
`IndusPolysemyPermutation`, `IndusProvenanceClassify`, `IndusProvenanceExtract`, 
`IndusProvenanceImpact`, `IndusProvenanceRecompute`, `IndusReadingExtraction`, 
`IndusRecentLitMine179`, `IndusReferenceMining`, `IndusRetroPlex`, `IndusRoifMining`, 
`IndusRoifValidation`, `IndusSAConstraintAblation`, `IndusSACorpusLayerBuild`, 
`IndusSACorpusPool`, `IndusSAgreement`, `IndusSAHeldOutValidation`, `IndusSAMetrologyCheck`, 
`IndusSanskritNorm`, `IndusSanskritSA`, `IndusSARecal`, `IndusSARerun193`, `IndusSARerun207`, 
`IndusSAScaledDeltaRun`, `IndusSAStep1SanityAudit`, `IndusScholarlyTranslations`, 
`IndusSealTranslation`, `IndusSealTranslations`, `IndusSemanticCluster`, `IndusShuIlishu152`, 
`IndusSibilantAnchors`, `IndusSibilantDedrValidation`, `IndusSibilantDiscovery`, 
`IndusSignHypothesisBattery187`, `IndusSignifTests`, `IndusSiteKLBootstrap`, 
`IndusSiteSemantic`, `IndusSiteStratification`, `IndusSSRNFetch194`, `IndusSyllabicLMBuilder`, 
`IndusSyllabicSA`, `IndusTargetedSA`, `IndusTBNameCheck`, `IndusTop8Analysis197`, 
`IndusTrigramSA`, `IndusTripleLM199`, `IndusUncertainReduce`, `IndusVowelHarmonyDx`, 
`KalyanCrossValidation`, `LaursenTable1Loader`, `MahadevanCrosswalkLoader`, 
`Phase25CorpusLoader`, `Phase25Verdict`, `Phase26CorpusLoader`, `Phase26Verdict`, 
`Phase27CorpusLoader`, `Phase27Verdict`, `Phase28CorpusLoader`, `Phase28Verdict`, 
`Phase29CorpusLoader`, `Phase29Verdict`, `RefinedSealLoader`, `RefinedSealLoaderV2`, 
`SanskritSyllableLM`, `ShuIlishuAnchorSearch`, `TamilBrahmiCrosscheck`
