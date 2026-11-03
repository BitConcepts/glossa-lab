# Stage S3 triage record — the 68 PARTIAL nodes, dispositioned (Spec 087)

**Stage:** S3, triage leg (task T301; the retention-bar
assessments of T302 are discharged inside this record — see
§3). **Branch:** `feat/087-s3-triage`, built on main
`698b5bde` (PR #489, Spec 087 S2). **Date:** 2026-11-02.
**Seat:** analysis worker; the parent re-scores this record
and dispatches conversion PRs from it. **Records only:** this
PR changes no code, no node, no graph; the only files touched
are this record and the T301 tick in tasks.md. No manual edit
(the triage changes no user-visible truth today — the manual
moves with the conversion PRs, per C087-15).

**Governing text.** spec.md S3 + decision D3 (the retention
bar), plan.md Stage S3 (triage-record PR first, conversion
PRs grouped by family, parent gates the record), census
Appendix A as snapshotted in records/census-evidence.md and
held in full in the audit folder (CENSUS.md §4.1 rule, §4.3
param-carry verdicts, Appendix A per-node classes).

## 1. Population and reconciliation

The population is the census's PARTIAL class: DOMAIN (§4.1
rule) nodes with real ports and/or params whose domain choice
is fixed in code (§4.3 verdict) — **68 nodes**. Reconciled
three ways, mechanically, against the current tree
(post-S2 main `698b5bde`):

1. **Census parse.** Appendix A of CENSUS.md parsed by script:
   517 rows; GENERIC 90; DOMAIN/WRAPPER 359; DOMAIN/PARTIAL
   **68**. The partition reproduces the census's published
   counts exactly.
2. **Runtime cross-check.** All 68 ids are present in
   `ATOMIC_NODES` (517 registered); **none** carries the S2
   `legacy` flag; **none** appears in
   `backend/glossa_lab/spec087_s2_legacy_ids.json`; **none**
   has the wrapper shape at runtime (every one has input
   ports and/or a non-empty params schema). Zero problems.
3. **Live-graph intersection.** Scanning the 27 stored live
   graphs: exactly **6** of the 68 are used live (189
   instances census; per-node consumers in §2). The 23
   in-code graph specs of `_build_proper_graph_specs()` use
   **none** of the 68.

Every code fact in §5's entries is from a first-hand read of
the node's registered function source in this tree (extracted
by `inspect.getsource` over the live registry), its
`AtomicNodeDef` ports/params, and the module-level helpers
and constants its function calls (quoted where they carry
domain content). Consumer evidence is a scripted scan for
each id over live graphs, `_archive/` graphs, backend code,
backend tests, frontend, other specs, docs, tools, and
`glossa-indus/` (the node's own defining module excluded;
`experiment_ledger.json` hits are registry metadata, not
consumers, and are not counted; hits in other modules'
comments/docstrings were inspected and are named as comments
where that is all they are).

## 2. Disposition key and stage counts

- **CONVERT** — disposition (a)/(b) of spec.md S3: the node
  becomes a generic primitive whose params/ports carry the
  domain specifics (a), or is re-expressed as a composition
  of existing primitives in its consuming graphs (b). Each
  entry names the target primitive (existing or to-be-created)
  and the fixture output-equivalence test its conversion PR
  must pass: same inputs → byte-identical outputs against the
  original node on pinned fixtures, plus the C087-13
  comparison runs for any node a live graph uses.
- **RETAIN** — disposition (c): passes all three legs of
  decision D3 on filed evidence.
- **RETIRE-CANDIDATE** — nomination only: no live consumer,
  no recorded demand, function subsumed by named existing
  primitives. Retirement is **not** executed in S3; it needs
  a separate parent ruling.
- **PROVISIONAL** — a retention whose D3 evidence is
  incomplete (missing leg named). There are no retentions,
  so there are no provisionals.

**Stage counts: CONVERT 64 · RETAIN 0 · RETIRE-CANDIDATE 4 ·
PROVISIONAL 0.** The 64 conversions group into 14 families
(§4); the 4 retire-candidates are Phase22Verdict,
Phase23Verdict, Phase24Verdict, ShuIlishuCandidateFilter
(entries in §5, families F12/F11).

## 3. The retention bar: no node passes it

D3 requires all three legs, evidenced: (1) demonstrated
non-composability — a recorded composition attempt that fails
output-equivalence for a named structural reason; (2)
parameter reality — the domain specifics *cannot* be carried
as parameters; (3) independent demand — ≥2 distinct consumers
(live graphs, registered experiments, or a registered
claim/study naming the mechanism) for the domain-specific
form.

Applied to the whole population, the bar fails every node on
at least one leg, and the failures are mechanical, not
judgement calls:

- **Leg 3 fails for 67 of 68.** The only registered-experiment
  consumers of PARTIAL nodes anywhere in the tree are the 27
  live graphs (§1.3) and they use 6 ids; of those, five have
  exactly **one** consuming graph each. The remaining 62 have
  no live consumer at all (their recorded use is in
  `_archive/` graphs — out of scope as consumers under the
  spec's non-goals — plus tests and docs, which are not
  demand instances under D3's wording).
- **Leg 2 fails for the one node that passes leg 3.**
  `M77InscriptionLoader` has 3 live consumers, but its domain
  specifics are two file paths and a field mapping — data,
  already half-carried by its existing params
  (`use_raw`, `min_length`, `max_length`, `label`). Nothing
  about it resists parameterization.
- **Leg 1 was executed, not asserted, for the three strongest
  retention candidates** — the nodes a reader would most
  plausibly claim are irreducibly domain machinery. All three
  attempts *succeeded* in reproducing the node, which under
  D3's own rule ("if the composition matches on the fixtures,
  the node takes disposition (a) or (b); the bar is not met")
  settles their dispositions as CONVERT:

  **H1 — StructuralTemplateAnalyzer composes from existing
  generics.** On a synthetic 8-sequence cluster fixture
  (with `-1` unmapped labels), the node's template mining
  (lengths 2–4, `min_count=2`) was reproduced exactly by the
  GENERIC `NgramCounter` run per length over the cleaned
  sequences: identical template multiset, 13 templates,
  identical counts (`(2,3): 11, (1,2): 4, (3,2): 4, …` —
  full output in the harness, §8). The node's four summary
  fields (`dominant_prefix_clusters`,
  `dominant_suffix_clusters`, `slot_occupancy`,
  `h_class_sequence`) have no existing generic emitter in
  that shape — `PositionalProfiler` emits per-symbol rates,
  not slot counts — so the conversion is (a) a generic
  `TemplateMiner` primitive rather than a pure (b) graph
  re-expression; that is an effort gap, not a structural
  non-composability, and D3 names the difference.

  **H2 — IndusAnchorSetSyllable's specifics are data,
  byte-proven.** A parameterized copy of the node — anchors
  path, LM-vocab path, Tamil diacritic table, confidence
  order, and skip-pattern all passed in as arguments with
  the values copied out of the module — reproduces the
  original's `anchor_dict` **byte-identically at all three
  confidence levels** (MEDIUM 171 anchors, HIGH 166, LOW
  174; `n_skipped` 0 in both forms at every level) against
  the repo's real `backend/reports/INDUS_FINAL_ANCHORS.json`
  and `backend/glossa_lab/data/dravidian_syllable_lm.json`.

  **H3 — IndusSignRoleClassifier's entire domain content is
  one parameter's default value.** The node self-describes
  as a "pure primitive"; its only Indus-specific content is
  `_DEFAULT_NUMERAL_SIGNS` (Parpola P121–P125, P144–P150 +
  M77 "100"–"115"), which is already the default of its
  existing `numeral_signs` parameter. Run on a synthetic
  corpus with the default vs `numeral_signs=[]`, the two
  `role_table`s differ **only** in the `numeral` role on the
  two default-set signs (`"105"`, `"P121"`) — every other
  role assignment is identical. The mechanism needs no
  domain content in code at all.

  **H4 — loader runnability probe (fixture note, not a
  leg).** `CanonicalSignLoader` in this environment returns
  its own empty-registry error (`Canonical sign registry is
  empty — run POST /canonical-signs/seed first`): the CGSA
  tables live in the backend DB, so the F3 conversion PR's
  fixtures must run against a seeded DB.
  `ClusterMapper` runs here through its frequency-rank
  fallback (`map_rate 1.0` on a 2-sequence fixture).

**Consequence for T302:** there are no disposition-(c)
nodes, so there are no per-node retention files to file; the
bar's application *is* this section plus the per-node leg
notes in §5. The T302 tick is left to the parent's gate on
this record (complete-by-vacuity if the zero-retention
outcome is accepted; if the parent judges any single node's
legs differently, that node alone re-triages).

## 4. Live domain-flavoured ids first

The census §4.1 union of live domain-flavoured ids (census-
evidence Table 2 note) names nine ids. Six are in the 68 and
get full entries here; three are **not** in the population
and are dispositioned by note after them, so the union is
fully covered without contaminating the count.

### 4.1 `M77InscriptionLoader` — CONVERT (a) · Family F1
- **Module/category:** `experiment_graph_phase20.py` (def
  :909), Phase-20 / Sources. **Ports:** none in. **Out:**
  sequences, inscriptions, n_inscriptions, n_tokens,
  n_distinct_signs, label, source. **Params:** use_raw,
  min_length, max_length, label (default `"indus_m77"`).
- **Fixed in code:** the corpus identity and both source
  paths — primary `reports/mahadevan_texts_decoded.json`
  (via `_resolve_report`), fallback the Holdat CSV at
  `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`
  with its column mapping (`cisi_number`, `position`,
  `letters`, `site`); the record shape (`raw` vs `sequence`
  under `use_raw`). Params already carry the length filters
  and the label.
- **Consumers:** live graphs ×3 (`indus_sa_dravidian_syllable`,
  `indus_sa_sanskrit_falsification`,
  `indus_validation_neg_controls`); archive ×15; the
  D3 leg-3 passer (§3) — and leg 2 still fails, so CONVERT.
- **Conversion:** the F1 `JsonCorpusLoader` with a
  fallback-chain source spec as params (primary report file
  + field names; fallback CSV + column mapping). **Fixture:**
  the repo's decoded-report file (and a pinned Holdat CSV
  extract for the fallback branch): sequences + inscriptions
  byte-identical; then the C087-13 comparison runs over the
  3 consuming graphs.

### 4.2 `CanonicalSignLoader` — CONVERT (a) · Family F3
- **Module/category:** `experiment_graph.py` (def :1945),
  CGSA / Structural. **Ports:** none in. **Out:** registry,
  n_signs, n_parpola, sign_ids, sign_id_to_uuid. **Params:**
  in_corpus_only (default true), numbering_system.
- **Fixed in code:** the DB table name `canonical_signs`
  (read via `_sync_db_all`), its column names (`sign_id`,
  `internal_id`, `numbering_system`, `in_corpus`), and the
  hardcoded `"parpola_1982"` filter behind the `n_parpola`
  output.
- **Consumers:** live ×1 (`indus_cgsa_cluster_analysis`);
  tests (`test_graph_experiments.py`); no other references.
- **Conversion:** the F3 `RegistryTableLoader` — table name,
  filter spec, and summary-field spec (the parpola count
  becomes a named filter-count in params). **Fixture:** a
  seeded `canonical_signs` table (H4: no seeded DB exists in
  this environment; the conversion PR seeds a fixture table
  and byte-compares registry/n_signs/sign_id_to_uuid), then
  the comparison run over `indus_cgsa_cluster_analysis`.

### 4.3 `ClusterMapper` — CONVERT (a) · Family F3
- **Module/category:** `experiment_graph.py` (def :1960),
  CGSA / Structural. **Ports in:** sequences. **Out:**
  cluster_sequences, n_sequences, map_rate, n_mapped_tokens,
  n_clusters, sign_to_cluster. **Params:** none.
- **Fixed in code:** the map's three sources in fixed
  priority — DB table `sign_cluster_assignments`; fallback
  file `analysis/sign_clusters.json`; fallback
  frequency-rank binning into ~40 clusters — and the `-1`
  unmapped label. The mechanism (apply a sign→label dict) is
  generic; everything CGSA is in the source spec.
- **Consumers:** live ×1 (`indus_cgsa_cluster_analysis`);
  archive ×1; tests (`test_graph_experiments.py`).
- **Conversion:** the F3 `LabelMapApplier` — map-source spec
  (table | file | frequency-fallback with bin count) and
  unmapped label as params, gaining the parameter surface it
  lacks today. **Fixture:** the fallback branches exercised
  in isolation (H4 shows the frequency branch running);
  byte-compare cluster_sequences + sign_to_cluster per
  branch; comparison run over the consuming graph.

### 4.4 `StructuralTemplateAnalyzer` — CONVERT (a) · Family F3
- **Module/category:** `experiment_graph.py` (def :1972),
  CGSA / Structural. **Ports in:** cluster_sequences.
  **Out:** recurrent_templates, n_templates,
  dominant_prefix_clusters, dominant_suffix_clusters,
  slot_occupancy, h_class_sequence,
  n_distinct_class_sequences. **Params:** min_count,
  max_template_length.
- **Fixed in code:** almost nothing domain: it operates on
  integer label sequences; the "domain" content is the
  input's provenance (ClusterMapper's CGSA label space) and
  fixed shape choices (template lengths 2–5, top-50 cut,
  top-10 slot tables). Census DOMAIN via the CGSA framing.
- **Consumers:** live ×1 (`indus_cgsa_cluster_analysis`);
  archive ×1; tests (`test_graph_experiments.py`).
- **Conversion:** the F3 generic `TemplateMiner` (label-
  sequence template mining; length range, cuts as params).
  H1 (§3) proves the core composes from `NgramCounter`
  today; the primitive exists to carry the four summary
  fields in one node. **Fixture:** H1's synthetic fixture
  plus the consuming graph's pinned comparison run, all
  output fields byte-compared.

### 4.5 `IndusAnchorSetSyllable` — CONVERT (a) · Family F8
- **Module/category:** `experiment_graph_phase30.py` (def
  :959), Phase-33 / Decipherment. **Ports:** none in.
  **Out:** anchor_dict, n_anchors, n_skipped, verdict.
  **Params:** min_confidence (default `"MEDIUM"`).
- **Fixed in code:** both file paths
  (`backend/reports/INDUS_FINAL_ANCHORS.json`;
  `backend/glossa_lab/data/dravidian_syllable_lm.json`), the
  Tamil romanization diacritic table (~22 replacements), the
  CV syllable splitter, the confidence order
  `{HIGH:3, MEDIUM:2, LOW:1, UNCERTAIN:0}`, and the
  positional-label skip regex `(term|med|init|ctx|role)[-:]`.
- **Consumers:** live ×1 (`indus_sa_dravidian_syllable`);
  archive ×1. Its output feeds `SADecipher`'s anchors port.
- **Conversion:** the F8 `AnchorSyllabifier` — paths,
  transliteration table, confidence order, skip pattern as
  params/data. H2 (§3) is the conversion's fixture proof
  already executed: byte-identical anchor_dicts at three
  confidence levels. The conversion PR re-pins that fixture
  as a test and adds the consuming graph's comparison run.

### 4.6 `MeluhhaCooccurrenceCheck` — CONVERT (a) · Family F11
- **Module/category:** `experiment_graph_phase30.py` (def
  :920), Phase-30 / Statistical Validation. **Ports in:**
  top_candidates, unique_names. **Out:** n_hits,
  meluhha_hits, verdict. **Params:** none.
- **Fixed in code:** the corpus file path
  (`backend/reports/meluhha_corpus_audit.json` — absent from
  this tree, so the node currently runs with an empty term
  set), the bidirectional substring match rule with the
  `len(term) > 3` guard, the top-20 candidate cap, and the
  FAVORABLE/NEUTRAL verdict labels.
- **Consumers:** live ×1 (`indus_validation_a1_a3_holdout`);
  archive ×1.
- **Conversion:** the F11 `CorpusCooccurrenceCheck` —
  corpus path, match mode, minimum term length, candidate
  cap as params; gains a parameter surface. **Fixture:** a
  pinned synthetic corpus-audit file with known hits/misses
  (the real file is not in the repo; the fixture must be
  created by the conversion PR and the absence behaviour —
  empty term set, all misses — pinned too); comparison run
  over the consuming graph.

### 4.7 Named live ids outside the 68 (no S3 entry, by class)
- **`WritingSystemClassifier`** (3 live graphs) — classed
  **GENERIC** by the census (§4.2 list): corpus metrics
  arrive via ports/params and are compared against a
  reference set of 11 writing systems. Not a PARTIAL node;
  no S3 action. (Its reference set is data inside a generic
  mechanism — the same shape S3 converts *toward*.)
- **`DravidianSyllableLM`** (1 live graph) and
  **`KalyanCrossValidation`** (1 live graph) — classed
  **WRAPPER** (no inputs, no params; verified at runtime
  here) and legacy-flagged at S2. Their disposition belongs
  to the wrapper set, not the 68; the natural path, named
  for the parent's ruling, is composition (b) in their
  consuming graphs (`BuiltinLM`/`LMBuilder` already carry
  the syllable-LM shape for the first; the cross-validation
  family is generic machinery for the second). This record
  takes no position beyond naming the path: converting
  wrappers is outside T301's population.

## 5. Families and the conversion-PR sequence

Conversions group by shared primitive shape. Sizes count
CONVERT entries only; retire-candidates ride no family PR
(they await the parent's ruling, then one small removal PR).

| # | Family | n | New/existing generic primitive(s) |
|---|---|---|---|
| F1 | Corpus & dataset loaders | 6 | `JsonCorpusLoader`, `DatasetRecordLoader` (new) |
| F2 | Evidence-graph loaders & claim tester | 3 | `JsonRecordDirLoader`, `PositionalClaimTester` (new) |
| F3 | CGSA / CTT machinery | 6 | `RegistryTableLoader`, `LabelMapApplier`, `TemplateMiner`, `ClusterContingencyProfile`, `SignRoleClassifier`, `ValueRoleMapSource` (new) |
| F4 | Phoneme-map scoring & permutation tests | 5 | `PhonemeMapPermutationTest`, `IconographicAnchorScorer`, `PhonemeMapCoverage` (new) |
| F5 | Name↔seal length matching & readout tests | 8 | `LengthMatchScorer`, `LengthMatchPermutationTest`, `StratifiedPermutationTest` (new) |
| F6 | Persons extraction & aggregation | 4 | `PersonsAggregator` (new) |
| F7 | Janabiyah skeleton search (forward + reverse) | 6 | `SkeletonTabletSearch`, `ReverseSkeletonSearch` (new) |
| F8 | Anchor derivation & syllabification | 3 | `AnchorSyllabifier`, `AssociationAnchorDeriver`, `PMICentralityRanker` (new) |
| F9 | Sequence statistics & signature verdicts | 8 | `InteractionSurplusProfile`, `OrderInformationProfile`, `TokenContextAssociation`, `MetricFieldExtractor`, `PositionalClassClassifier`, `SignatureComparator`, `EvidenceRuleAggregator`, `SignPositionNullTest` (new) |
| F10 | Reporters, auditors & corpus stats | 6 | `RecordGroupSummary`, `CorpusComparisonStats` (new) |
| F11 | Findspot & co-occurrence machinery | 3 | `PrefixFindspotAssigner`, `CorpusCooccurrenceCheck` (new) |
| F12 | Verdict aggregators | 2 | `PredictionVerdictAggregator` (new); 3 further members are retire-candidates |
| F13 | Text & document ingestion | 2 | `VisionOCRNode`, `CatalogTextParser` (new) |
| F14 | Already-generic mechanisms (relabel) | 2 | none — mechanism unchanged |

**Proposed sequence** (family per PR, per plan.md; each PR
carries its fixtures, its output-equivalence proofs, the
completeness re-pin if it registers a new primitive
(C087-17), and the manual update for its nodes (C087-15)):

1. **F14** — zero mechanism change; clears the two
   mislabelled primitives first and proves the family's
   fixture method on the cheapest cases.
2. **F1** — loaders; everything downstream consumes corpora,
   and three live graphs consume F1's M77 member.
3. **F3** — the CGSA live trio (CanonicalSignLoader,
   ClusterMapper, StructuralTemplateAnalyzer) is in one live
   graph; do it while the S2 comparison pins are fresh. Its
   DB-fixture need (H4) is the family's critical path.
4. **F8** — H2 already proves its hardest member.
5. **F4, F5, F7, F6** — the decipherment test machinery, in
   dependency order (map scoring → length matching → the
   Janabiyah searches that reuse both → persons aggregation
   feeding F5/F7 inputs).
6. **F9** — sequence statistics; several members feed F12's
   aggregators and the CTT family (F3) conceptually, no code
   dependency either way.
7. **F2, F10, F11, F13, F12** — evidence loaders, reporters,
   findspot machinery, ingestion, verdict aggregators; no
   interdependencies beyond F5's shared bipartite-test core
   (F12's members consume F5-family outputs as data, not
   code).

Cross-family dependency of note: F5's `LengthMatchPermutationTest`
and F7's searches share the `_length_score` /
`_run_bipartite_test` helper lineage (three separate copies
of `_run_bipartite_test` exist, in phase25/26/27) — F5 lands
first and F7 consumes its primitive. Inside F1, two different
M77 corpus pipelines exist (`data/indus_m77.py` behind
MahadevanInscriptionLoader vs the decoded-report file +
Holdat fallback behind M77InscriptionLoader): the F1 PR must
reconcile them into one source spec or record why both
survive — flagged here, not decided here.

## 6. Per-node entries — the remaining 62, by family

Entry format: ports/params as registered today; the domain
specifics fixed in code (constants quoted); consumers from
the §1 scan (live / archive / tests — archive use is recorded
history, not a D3 consumer); disposition with its conversion
target and fixture. Where a family's fixture method is
shared it is stated once at the family head: **the fixture
is the input set wired in the node's archive graph(s),
pinned into the conversion PR as files, plus synthetic
records for branches the archive inputs don't reach; outputs
byte-compared field by field.**

### F1 — Corpus & dataset loaders (M77InscriptionLoader is §4.1)

Family target: `JsonCorpusLoader` (file-backed corpora with a
source/fallback spec) and `DatasetRecordLoader` (bundled
data-module getters), both new; dataset identity, paths,
getter names, and field mappings become params.

- **ContactCorpusLoader** — CONVERT. `experiment_graph_phase22.py`,
  Phase-22 / Sources. In: none. Out: tablets, n_tablets,
  keyword_counts, period_counts, provenience_counts,
  seals_at_mesopotamia, n_seals_at_mesopotamia, persons,
  n_persons. Params: period_filter, keyword_filter. Fixed:
  the bundled dataset itself — the
  `glossa_lab.data.mesopotamian_contact` getters
  (`get_meluhha_tablets`, `get_indus_seals_at_mesopotamia`,
  `get_meluhhan_persons`, keyword/period/provenience
  counters) are called by name in code. Consumers: archive
  ×4. → `DatasetRecordLoader` (getter set + filters as
  params).
- **EPSD2NamesLoader** — CONVERT. `experiment_graph_phase29.py`,
  Phase-29 / Sources. In: none. Out: names, n_names, n_total,
  metadata, verdict. Param: pos_filter. Fixed: the ePSD2
  dataset identity via `get_epsd2_names` /
  `get_epsd2_metadata` in the same data module. Consumers:
  archive ×1. → `DatasetRecordLoader`.
- **ICITCorpusLoader** — CONVERT. `experiment_graph_phase29.py`,
  Phase-29 / Sources. In: none. Out: available, n_inscriptions,
  n_signs, metadata, verdict. Param: data_path (default
  `corpora/downloads/icit_cache.json`). Fixed: the ICIT
  cache's JSON shape and the no-op-unless-cached behaviour.
  Consumers: archive ×1. → `JsonCorpusLoader` (cache shape as
  a field-map param; the absent-file branch pinned in the
  fixture, since the cache is not in this repo).
- **MahadevanInscriptionLoader** — CONVERT.
  `experiment_graph_phase29.py`, Phase-29 / Sources. In:
  none. Out: inscriptions, n_inscriptions, n_tokens,
  n_distinct_signs, metadata, top_20_signs, verdict. Param:
  min_length. Fixed: the corpus source
  `glossa_lab.data.indus_m77` via
  `mesopotamian_contact.get_mahadevan_inscriptions`
  (1,669 inscriptions / 5,361 tokens per its docstring) — a
  *different* M77 pipeline from §4.1's (see the F1
  reconciliation flag in §5). Consumers: archive ×1. →
  `DatasetRecordLoader`.
- **MathematicaEpigraphicaLoader** — CONVERT.
  `experiment_graph_phase29.py`, Phase-29 / Sources. In:
  none. Out: available, n_inscriptions, inscriptions,
  sites_top, verdict. Param: data_path (default
  `corpora/downloads/fuls_me_vol3_corpus.json`). Fixed: the
  Fuls ME Vol 3 cache shape; same no-op pattern as ICIT.
  Consumers: archive ×1. → `JsonCorpusLoader`.

### F2 — Evidence-graph loaders & claim tester

Family target: `JsonRecordDirLoader` (a directory of JSON
records + field-map/schema defaults as params) and
`PositionalClaimTester`, both new. The evidence base path
`_EVIDENCE_BASE = <repo>/glossa-indus`, with
`literature/documents` and `claims/extracted_claims` beneath
it, is fixed in `experiment_graph_indus_evidence.py` for all
three.

- **IndusLiteratureLoader** — CONVERT. Evidence Graph. In:
  none. Out: papers, total_papers, text. Params: query,
  max_papers. Fixed: the literature documents directory and
  its record shape (the search corpus is the glossa-indus
  literature set; `metadata.json` handling fixed in code).
  Consumers: tests ×2 (`test_evidence_atomic_nodes.py`,
  `test_graph_experiments.py`), docs ×3, glossa-indus
  LEDGER. → `JsonRecordDirLoader` in search mode (directory
  + query fields as params). Fixture: a pinned documents
  directory; the existing tests' fixtures are the starting
  set.
- **IndusClaimsLoader** — CONVERT. Evidence Graph. In:
  papers. Out: claims, total_claims, type_counts,
  status_counts, text. Params: claim_type, claim_status,
  sign_filter, max_claims. Fixed: the extracted-claims
  directory and the claim schema defaults applied in code
  (status default `"needs_extraction"`, confidence default
  `"UNCERTAIN"`). Consumers: tests ×2, docs ×3, glossa-indus
  LEDGER. → `JsonRecordDirLoader` (schema defaults as data
  params).
- **IndusClaimTester** — CONVERT. Evidence Graph. In: claims,
  sequences. Out: test_results, n_tested, support_rate, json,
  text. Params: none. Fixed: the claim-type routing by
  keyword (`"position"` / `"sign_value"` / `"sign_function"`
  in the claim type), the prediction parse out of the
  normalized claim text (initial/terminal over the first 4
  signs), the support rule (observed rate ≥ corpus average
  × 1.2), and the honest untestable verdict for the
  sign-value/sign-function types. Consumers: tests ×2,
  docs ×3, glossa-indus LEDGER. → `PositionalClaimTester`
  (type keywords, prediction fields, lift factor as params).
  Fixture: synthetic claims of each type over sequences with
  known positional rates, incl. the untestable branches.

### F3 — CGSA / CTT machinery (CanonicalSignLoader, ClusterMapper, StructuralTemplateAnalyzer are §4.2–§4.4)

- **ClusterArchaeology** — CONVERT. `experiment_graph_phase20.py`,
  Phase-20 / Archaeology. In: inscriptions, sign_to_cluster.
  Out: site_table, length_table, chi_squared, dof,
  significant_p05, verdict, target_cluster_signs. Params:
  target_cluster, fixed_members. Fixed: the site strata
  derivation (site key from the inscription record, with the
  2-character prefix grouping and the `"0000"` aggregate),
  and the significance rule `chi2 > 3.84 * dof` in code.
  Consumers: archive ×2 (phase21 mentions are comments).
  → `ClusterContingencyProfile` (strata rule + significance
  rule as params). Fixture: the phase20b archive graph's
  inputs.
- **IndusSignRoleClassifier** — CONVERT. `experiment_graph_ctt.py`,
  CTT / Constraint Topology. In: sequences. Out: role_table,
  n_signs, role_summary, compound_signs, high_pmi_bigrams.
  Params: terminal_threshold, initial_threshold,
  compound_pmi_threshold, min_count, numeral_signs. Fixed:
  exactly one thing — `_DEFAULT_NUMERAL_SIGNS` (Parpola
  P121–P125, P144–P150 + M77 `"100"`–`"115"`) as the
  *default value* of the existing `numeral_signs` param,
  plus the role-rule structure (ROLE_BITS order: suffix,
  determinative, numeral, phonetic, logogram, compound) and
  the relaxed-suffix rule (terminal rate ≥ 0.45 and ≥ 1.5 ×
  initial rate). H3 (§3) proves the default is the whole
  domain content. Consumers: archive ×4, tests ×1. →
  `SignRoleClassifier`: the same mechanism with
  `numeral_signs` defaulting empty; the Indus set moves into
  the consuming graphs' params. Fixture: H3's synthetic
  corpus, run at both the old default and the explicit param
  — outputs identical.
- **DefaultIndusValueRoleMap** — CONVERT. `experiment_graph_ctt.py`,
  CTT / Constraint Topology. In: none. Out: value_role_map,
  n_values, families_applied, family_sizes, unknown_families,
  json. Params: families, include_default, extra. Fixed: the
  entire `DEFAULT_INDUS_VALUE_ROLE_MAP` constant (Tamil case
  suffixes `-um`/`-e`/`-il`/`-ku`/…, CV syllabograms) and
  `_FAMILY_ROLE_MAP_BUILDERS` (old_tamil/dravidian/tamil →
  the Tamil builder; hieroglyphic_luwian/luwian;
  mycenaean_greek/linear_b/greek). Consumers: archive ×4,
  tests ×1. → `ValueRoleMapSource` (base map + family tables
  as data params); the GENERIC sibling
  `LogogramAwareValueRoleMap` already proves the shape.
  Fixture: byte-compare value_role_map per family selection,
  incl. unknown-family handling.

### F4 — Phoneme-map scoring & permutation tests

Family target: `PhonemeMapPermutationTest` (a map-assignment
score with a parameterized shuffle dimension),
`IconographicAnchorScorer` (alias table + weights as data),
`PhonemeMapCoverage`, all new. The family's shared helpers —
`_seal_phoneme_match_score` (phase27 copy), the copy-pasted
`_run_bipartite_test` lineage — are the duplication the
conversion removes.

- **IconographicAnchorScore** — CONVERT.
  `experiment_graph_phase27.py`, Phase-27 / Decipherment. In:
  iconographic_anchors, phoneme_map. Out: n_total_anchors,
  n_matches, total_score, rows, verdict. Params: none.
  Fixed: the `iconic_to_phoneme_alias` table in code (fish →
  `miin`; fig/banyan → `vaTa`; muruku → `muruku`; squirrel →
  `piLLai`; pot → `kuTam`; `veL`; pleiades → `aru-`; ursa
  major → `eZu-`; north star → `vaTa`), the match weights
  (2.0 exact / 1.0 uncertain / 0.5 partial) and the ×1.5
  high-confidence bonus. Consumers: archive ×1 (phase28/29
  mentions are comments). → `IconographicAnchorScorer`
  (alias table + weights + bonus as data params; the node
  gains a parameter surface). Fixture: the phase27c archive
  graph's anchors + map.
- **AllographAwareIconographicScore** — CONVERT.
  `experiment_graph_phase28.py`, Phase-28 / Decipherment. In:
  iconographic_anchors, phoneme_map, allograph_families.
  Out: n_total_anchors, n_matches, n_allograph_extensions,
  extended_sign_ids, total_score, rows, verdict. Params:
  none. Fixed: the same alias table and weights, plus the
  allograph-extension bonus (+0.25 per family member) and
  the fish-family working set its description pins (signs
  47, 48, 50, 52, 60, 145, 147). Consumers: archive ×1. →
  the same `IconographicAnchorScorer`, with the extension
  bonus as a param (0 disables it → the Phase-27 behaviour;
  one primitive replaces both nodes). Fixture: phase28c
  archive inputs, incl. a fish-family anchor.
- **BlindHeldOutTest** — CONVERT. `experiment_graph_phase25.py`,
  Phase-25 / Decipherment. In: inscribed_seals, phoneme_map.
  Out: n_seals, n_readable, n_high_conf, rows, verdict.
  Params: none. Fixed: the readability rule (a seal counts
  readable when its signs resolve to phonemes other than
  `"?"` and free of `"uncertain"`) and a verdict string that
  hardcodes the Janabiyah/CISI study narrative. Consumers:
  archive ×1. → `PhonemeMapCoverage` (readability predicate
  + verdict labels as params). Fixture: phase25 archive
  inputs.
- **BayesianDecoder** — CONVERT. `experiment_graph_phase26.py`,
  Phase-26 / Decipherment. In: inscribed_seals, phoneme_map.
  Out: n_seals, n_phonemes_in_map, observed_total_weight,
  null_mean_weight, p_value, verdict, interpretation.
  Params: n_permutations, seed. Fixed: the permutation
  design (shuffle the map's *confidence labels*) and the
  match statistic's confidence weights (high 1.0 / medium
  0.5 / low 0.2) in `_seal_phoneme_match_score`. Consumers:
  archive ×1. → `PhonemeMapPermutationTest`
  (shuffle_dimension=`confidence`, weight table as data).
  Fixture: phase26 archive inputs at the registered seed —
  permutation outputs are seed-determined, so byte-equality
  is checkable exactly.
- **BayesianDecoderV2** — CONVERT. `experiment_graph_phase27.py`,
  Phase-27 / Decipherment. Ports as V1. Params:
  n_permutations, seed. Fixed: the different permutation
  design (shuffle the phoneme *values*) and the added
  `_compound_plausibility_score` with
  `_DRAVIDIAN_COMPOUND_PATTERNS` — the 8 pairs (aru,miin),
  (eZu,miin), (vaTa,miin), (veL,miin), (muruku,veL),
  (muruku,piLLai), (muruku,miin), (katir,miin) — scored
  +1.0 per adjacent pair, +0.2 per repeat. Consumers:
  archive ×1. → the same `PhonemeMapPermutationTest`
  (shuffle_dimension=`value`, plausibility_patterns as data
  params). Fixture: phase27 archive inputs at seed.

### F5 — Name↔seal length matching & readout tests

Family target: `LengthMatchScorer` (all-pairs or bipartite
assignment), `LengthMatchPermutationTest`,
`StratifiedPermutationTest` (strata rules as ordered
substring→bucket data), all new. Shared fixed machinery
across the family: `_name_n_segments` = hyphen count + 1 and
`_length_score` = 1 − delta/(tolerance+1), 0 beyond
tolerance; `_run_bipartite_test` exists as three separate
copies (phase25, phase26, phase27).

- **BilingualReadoutTest** — CONVERT.
  `experiment_graph_phase25.py`, Phase-23 / Decipherment.
  In: rows_all, inscribed_seals. Out: verdict, p_value,
  observed, null_mean, null_sd, z_score, n_permutations,
  n_candidates, n_seals, interpretation. Params:
  n_permutations, min_name_freq, tolerance, seed. Fixed: the
  best-match statistic choice and the verdict thresholds
  (p < 0.01 / p < 0.05) over the shared length score.
  Consumers: archive ×1. → `LengthMatchPermutationTest`
  (statistic=`best_match`). Fixture: phase23 archive inputs
  at seed.
- **BilingualReadoutTestV2** — CONVERT.
  `experiment_graph_phase24.py`, Phase-24 / Decipherment.
  Ports as V1, plus out observed_assignment. Params as V1.
  Fixed: the greedy bipartite-assignment statistic (the only
  material difference from V1). Consumers: archive ×1. → the
  same primitive (statistic=`bipartite`). Fixture: phase24
  archive inputs at seed.
- **EnhancedNameMatcher** — CONVERT.
  `experiment_graph_phase23.py`, Phase-23 / Decipherment.
  In: rows_all, inscribed_seals. Out: n_candidates, n_seals,
  pairings, pairings_top50, n_pairings, best_per_name,
  verdict. Params: min_name_freq, tolerance. Fixed: the
  all-pairs scoring over the shared segment/length helpers;
  no domain constants beyond the helpers. Consumers:
  archive ×1. → `LengthMatchScorer` (assignment=`all_pairs`).
- **EnhancedNameMatcherV2** — CONVERT.
  `experiment_graph_phase24.py`, Phase-24 / Decipherment.
  Ports as V1. Params: min_name_freq, tolerance. Fixed: the
  bipartite-assignment variant of the same scorer.
  Consumers: archive ×1. → `LengthMatchScorer`
  (assignment=`bipartite`).
- **MeluhhaNameMatcher** — CONVERT.
  `experiment_graph_phase22.py`, Phase-22 / Decipherment.
  In: persons, seals_at_mesopotamia. Out: n_candidates,
  n_seals_with_signs, n_seals_total, pairings_top50,
  n_pairings, verdict. Param: min_name_freq. Fixed: a
  *different* length falloff from the rest of the family —
  1 − |Δ|/5.0 with no tolerance param — over the
  Mesopotamia seal set. Consumers: archive ×2. →
  `LengthMatchScorer` with the falloff as a named score-spec
  param (the conversion must not silently change the
  falloff; the fixture pins it). Fixture: phase22 archive
  inputs.
- **PeriodStratifiedReadout** — CONVERT.
  `experiment_graph_phase25.py`, Phase-25 / Decipherment.
  In: persons_v3, inscribed_seals. Out: results,
  n_significant_strata, verdict. Params: n_permutations,
  tolerance. Fixed: the inline period-coarsening map (Ur III
  / Old Babylonian / Neo-Assyrian / Old Akkadian / Ebla /
  Other) and the per-stratum seed rule (42 + len(period)).
  Consumers: archive ×1. → `StratifiedPermutationTest`
  (axis=`period`, strata rules + seed base as data params).
- **PeriodStratifiedReadout6Bucket** — CONVERT.
  `experiment_graph_phase27.py`, Phase-27 / Decipherment.
  Ports/params as above. Fixed: `_PERIOD_BUCKETS_6` (8 named
  buckets) and seed rule 271 + len(period). Consumers:
  archive ×1. → the same primitive with the 6-bucket rule
  set as data. Fixture note: the two period variants differ
  *only* in the bucket table and seed base — the conversion
  PR proves it by running both rule sets through the one
  primitive.
- **ProvenienceStratifiedReadout** — CONVERT.
  `experiment_graph_phase26.py`, Phase-26 / Decipherment.
  Ports/params as above. Fixed: `_PROVENIENCE_BUCKETS`
  (Girsu, Nippur, Ur, Umma, Lagash, Susa, Mari, Nineveh,
  Sippar, …) and seed rule 137 + len(prov). Consumers:
  archive ×1. → the same primitive (axis=`provenience`).

### F6 — Persons extraction & aggregation

Family target: one `PersonsAggregator` (field mapping,
known-names set, segment counting as params/data). All four
members aggregate person rows into per-name counts with a
known-Meluhhan confirmation list; the family's evolution is
copy-driven.

- **MeluhhanPersonsExtractor** — CONVERT.
  `experiment_graph_phase22.py`, Phase-22 / Reporters. In:
  persons. Out: n_unique_candidates, rows_top50,
  all_rows_count, confirmed_hits, verdict. Param: min_freq.
  Fixed: the known-names set in code — {lu-sun-zi-da,
  lu2-sun-zi-da, shu-ilishu, shu-ilisu, su-ilisu}.
  Consumers: archive ×2. → `PersonsAggregator`
  (known_names as data param).
- **RefinedMeluhhanPersonsExtractor** — CONVERT.
  `experiment_graph_phase23.py`, Phase-23 / Reporters. In:
  strict_persons. Out: n_unique, rows_top50, rows_all,
  n_total, confirmed_hits, by_pattern, verdict. Param:
  min_freq. Fixed: the aggregation takes `is_known` from the
  upstream rows (the known set moved upstream); the pattern
  grouping is fixed in code. Consumers: archive ×2. → the
  same aggregator (known source = upstream flag).
- **RefinedMeluhhanPersonsExtractorV2** — CONVERT.
  `experiment_graph_phase24.py`, Phase-24 / Reporters. In:
  persons_v2. Out/params as V1. Fixed: **a near-verbatim
  copy of V1** — the material differences are the input port
  name and an `example_line[:120]` truncation; mechanism,
  outputs, and rules are V1's. Consumers: archive ×2. → the
  same aggregator; the conversion deletes a duplicate
  implementation, and its fixture is V1's fixture (identical
  outputs expected on identical rows).
- **Persons_v3_Extractor** — CONVERT.
  `experiment_graph_phase25.py`, Phase-25 / Reporters. In:
  persons_v3. Out: n_unique, rows_top50, rows_all, verdict.
  Param: min_freq. Fixed: the same aggregation plus
  `_name_n_segments` enrichment. Consumers: archive ×1. →
  the same aggregator (segment-count enrichment toggled by
  param).

### F7 — Janabiyah skeleton search (forward + reverse)

Family target: `SkeletonTabletSearch` (forward: skeleton →
tablet lines) and `ReverseSkeletonSearch` (reverse: name
list → skeleton matches), both new. All six members share
one scoring core, fixed in each copy: target segment
positions {1, 3, 6}, target length 7 segments, weights
(length 3.0 − 0.5·δ; +1.5 position match; +0.5 free
occurrence), and the −1.5 penalty for names ending
`-me-luh-ha` / `-me-luh-ha-ki`.

- **JanabiyahPhoneticReadout** — CONVERT.
  `experiment_graph_phase25.py`, Phase-25 / Decipherment.
  In: janabiyah_reading, phoneme_map, tablets. Out:
  skeleton, predictions, n_miin, matches_top20, n_matches,
  verdict, interpretation. Params: none. Fixed: an 11-item
  miin_renderings list in code, the `"me-luh"` keyword gate,
  and the hits ≥ 2 match rule, over the shared core.
  Consumers: archive ×1. → `SkeletonTabletSearch`
  (renderings as data param).
- **JanabiyahPhoneticReadoutV2** — CONVERT.
  `experiment_graph_phase26.py`, Phase-26 / Decipherment.
  In: janabiyah_reading, phoneme_map, tablets,
  miin_renderings, miin_renderings_direct_only. Out:
  skeleton, predictions, n_miin, matches_direct_top20,
  n_matches_direct, matches_expanded_top20,
  n_matches_expanded, n_new_matches_from_translation,
  verdict. Params: none. Fixed: only the shared core — **the
  renderings already arrive through input ports** (the
  parameterized form of V1 exists in-tree). Consumers:
  archive ×1. → the same `SkeletonTabletSearch`; V1 and V2
  collapse into it (V1 = V2 with the rendering list supplied
  as a constant input).
- **ReverseJanabiyahSearch** — CONVERT.
  `experiment_graph_phase27.py`, Phase-27 / Decipherment.
  In: persons_v3, janabiyah_reading. Out: n_candidates,
  n_with_position_match, n_with_free_miin, top_matches,
  verdict. Param: top_k. Fixed: a static 15-item rendering
  set in code over the shared core. Consumers: archive ×1.
  → `ReverseSkeletonSearch` (renderings as data).
- **ReverseJanabiyahSearchV2** — CONVERT.
  `experiment_graph_phase28.py`, Phase-28 / Decipherment.
  In: persons_v3, janabiyah_reading, phoneme_map,
  allograph_families. Out: n_candidates, n_renderings,
  n_with_position_match, n_with_free_miin, top_matches,
  verdict. Param: top_k. Fixed: 16 base renderings plus the
  dynamic expansion from the phoneme map via the fish
  allograph family. Consumers: archive ×2. → the same
  primitive (expansion toggle + family source as params).
- **M77ReverseJanabiyahSearchV3** — CONVERT.
  `experiment_graph_phase29.py`, Phase-29 / Decipherment.
  In: epsd2_personal_names, janabiyah_reading, phoneme_map,
  allograph_families. Out: n_pns_searched, n_renderings,
  n_with_position_match, n_with_free_miin, top_matches,
  verdict. Params: top_k, min_icount. Fixed: the same core
  run over ePSD2 personal names with the `_epsd_pn_to_segments`
  segmenter. Consumers: archive ×1, docs ×1. → the same
  primitive (name source + segmenter as params).
- **LengthCohortReverseJanabiyahSearch** — CONVERT.
  `experiment_graph_phase30.py`, Phase-30 / Decipherment.
  In/params: as V3 plus cohorts (default
  [[3,4],[5,6],[7,8],[9,99]]). Out adds cohorts,
  n_cohorts, per-cohort totals. Fixed: a re-implementation
  of V3's scoring plus cohort stratification and the 5×
  concentration verdict rule. Consumers: archive ×1,
  docs ×1. → the same primitive (cohort mode + cohort table
  as params — the param already exists; the conversion is
  mostly deleting the fourth copy of the core).

### F8 — Anchor derivation & syllabification (IndusAnchorSetSyllable is §4.5)

- **DerivedAnchorSet** — CONVERT. `experiment_graph_phase14.py`,
  Phase-14 / Grounding. In: associations. Out: anchors,
  n_anchors, anchor_table, verdict. Params: min_z,
  max_anchors. Fixed: very little — the mechanism (top-K
  sign×context associations → `ctx:`-prefixed anchor
  entries) is already generic; the domain content is the
  `ctx:` anchor-id convention and the input's provenance.
  Consumers: archive ×1, docs ×1. →
  `AssociationAnchorDeriver` (anchor-id prefix as param).
- **EpistaticAnchorRanker** — CONVERT.
  `experiment_graph_phase14.py`, Phase-14 / Epistatic. In:
  sequences. Out: ranking, n_signs_ranked, verdict. Params:
  top_k, min_count. Fixed: no domain constants — PMI-
  centrality ranking over the input sequences; DOMAIN by its
  Phase-14 framing and its role in the anchor pipeline.
  Consumers: no graph consumers recorded (one non-graph code
  mention). → `PMICentralityRanker` (relabel + param
  surface unchanged).

### F9 — Sequence statistics & signature verdicts

Family target: eight small primitives, each the generic
form of one phase-14/20 statistic with its rule tables as
data. Phase-14's members share the CAS (Corpus Analysis
Suite) vocabulary; none of their mechanisms names Indus in
code except where noted.

- **EpistaticInteractionDetector** — CONVERT.
  `experiment_graph_phase14.py`, Phase-14 / Epistatic. In:
  sequences. Out: label, bigrams, trigrams,
  n_significant_bigrams, n_significant_trigrams, verdict,
  json. Params: min_count_2, min_count_3, top_k, label.
  Fixed: the PMI-surplus significance cut (≥ 2.0 nats) in
  code. Consumers: no graph consumers (one non-graph code
  mention). → `InteractionSurplusProfile` (cut as param).
- **EpistaticOrderProfile** — CONVERT.
  `experiment_graph_phase14.py`, Phase-14 / Epistatic. In:
  sequences. Out: label, orders, regime, f2_over_f1,
  f3_over_f2, per_symbol_entropy, verdict, json. Params:
  max_order, label. Fixed: the regime thresholds —
  f2/f1 ≥ 0.10 ∧ f3/f2 ≥ 0.05 → `language_like`;
  f2/f1 < 0.05 → `non_linguistic` — in code. Consumers: no
  references outside its own module at all. →
  `OrderInformationProfile` (regime rule table as data).
- **SignContextAssociation** — CONVERT.
  `experiment_graph_phase14.py`, Phase-14 / Grounding. In:
  sequences, metadata. Out: associations, n_significant,
  n_total_pairs, field, verdict, json. Params: field,
  n_perm, seed, min_count, top_k. Fixed: the `length_bin`
  bucketing (short ≤ 2 / medium ≤ 5 / long) and the z ≥ 2.0
  significance cut. Consumers: no references outside its own
  module at all. → `TokenContextAssociation` (binning spec +
  cut as params).
- **DoFExtractor** — CONVERT. `experiment_graph_phase14.py`,
  Phase-14 / Structural. In: block_entropies, zipf,
  mi_decay, hed. Out: dof_values, n_dofs. Params: none.
  Fixed: the entire field mapping into CAS
  degrees-of-freedom keys (h1_norm, zipf_alpha, mi_gamma,
  epistatic_2nd_norm, …) — a fixed renaming table.
  Consumers: no references outside its own module at all. →
  `MetricFieldExtractor` (field_map as data param; gains a
  parameter surface).
- **LanguageSignatureComparator** — CONVERT.
  `experiment_graph_phase14.py`, Phase-14 / Structural. In:
  a, b, c, d, e, f (six corpus signatures). Out: ranked,
  language_template, verdict, json. Param: target_label.
  Fixed: the candidate-selection rule `"indus" in label` in
  code (the one literal domain string in the family), the
  negative-tag set (permut / shuffle / random / uniform),
  and the ±0.25 verdict margin. Consumers: one non-graph
  code mention. → `SignatureComparator` (candidate tag +
  negative tags + margin as params).
- **LanguageDetectorVerdict** — CONVERT.
  `experiment_graph_phase14.py`, Phase-14 / Integrative. In:
  zipf, conditional_entropy, mi_decay, hed, cas_projection.
  Out: is_language, confidence, score, evidence_for,
  evidence_against, verdict, json. Params:
  cas_violation_low, cas_violation_high. Fixed: the evidence
  rule table — Zipf alpha in 0.85–1.30 ∧ R² ≥ 0.85; HED
  fractions 0.10 / 0.05; `is_language` at score ≥ 2 — in
  code. Consumers: tests ×1
  (`test_spec086_stub_disposition.py`), named in the Spec
  086 stage-4 record. → `EvidenceRuleAggregator` (rule
  table as data params).
- **FulsPositionalClassifier** — CONVERT.
  `experiment_graph_phase20.py`, Phase-20 / Sign function.
  In: sequences. Out: table, counts_by_class,
  fractions_by_class, n_signs_classified, verdict. Params:
  min_count, dom_threshold (0.55), secondary_threshold
  (0.30), numerical_rr (0.20). Fixed: only the 5-class label
  set (NUMERICAL / INITIAL / MEDIAL / TERMINAL / MIXED) and
  the Fuls framing — **every threshold is already a
  parameter**. Consumers: archive ×4. →
  `PositionalClassClassifier` (class labels as data). The
  cheapest conversion in the stage.
- **IndusNullModelTest** — CONVERT.
  `experiment_graph_indus_evidence.py`, Evidence Graph. In:
  sequences. Out: z_score, p_approx, verdict, json, text.
  Params: target_sign, test_type, n_null_runs, random_seed.
  Fixed: the z-verdict thresholds (3 / 2 / 1.5) in code.
  Consumers: tests ×2, docs ×3, glossa-indus LEDGER. →
  `SignPositionNullTest` (thresholds as params). Note for
  the conversion PR: the GENERIC `PermutationTest` exists
  but its ports are score-shaped, not sequence-shaped — the
  conversion either extends it or lands this primitive; it
  must not force-fit the ports.

### F10 — Reporters, auditors & corpus stats

Family target: `RecordGroupSummary` (group-by + distribution
sections specified as params) and `CorpusComparisonStats`,
both new. Every member is a fixed group-by/distribution over
records whose field names are the only domain content.

- **IndusSealsAtMesopotamiaSummary** — CONVERT.
  `experiment_graph_phase22.py`, Phase-22 / Reporters. In:
  seals_at_mesopotamia. Out: n_seals, by_country, by_type,
  by_period, rows, verdict. Params: none. Fixed: the three
  grouping fields (find_country / type / find_period).
  Consumers: archive ×2. → `RecordGroupSummary`.
- **LaursenTable1Auditor** — CONVERT.
  `experiment_graph_phase24.py`, Phase-24 / Reporters. In:
  rows, parpola_readings. Out: n_rows, n_inscribed,
  n_parpola_readings, by_gulf_type, by_site_top10,
  sample_rows, verdict. Params: none. Fixed: the `"INDUS"`
  substring test on `gulf_type` and the 121-row expectation
  carried in the verdict text. Consumers: archive ×1. → the
  same primitive (match rule + expectation as params).
- **MeluhhaCorpusReporter** — CONVERT.
  `experiment_graph_phase22.py`, Phase-22 / Reporters. In:
  tablets, keyword_counts, period_counts, provenience_counts.
  Out: n_tablets, n_keywords, keyword_counts, top_5_periods,
  top_10_provenience, most_mentioned_top10, verdict.
  Params: none. Fixed: the section set and its top-N cuts
  (5 / 10 / 10). Consumers: archive ×2. → the same
  primitive (section specs as params).
- **Phase29CorpusStats** — CONVERT.
  `experiment_graph_phase29.py`, Phase-29 / Decipherment.
  In: inscribed_seals, mahadevan_inscriptions. Out: rows,
  scale_up_factor_cisi_to_m77, verdict. Params: none.
  Fixed: the corpus labels (CISI vs M77), the sequence-field
  names it reads (`"indus_signs"` / `"signs"`), the `"?"`
  placeholder filter, and the direct calls into the F1
  loader functions for the ME/ICIT comparison rows.
  Consumers: archive ×1. → `CorpusComparisonStats` (corpus
  specs as params). Fixture note: pin the loader outputs it
  consumes so the direct-call leg is fixture-visible.
- **SealSignAuditor** — CONVERT. `experiment_graph_phase23.py`,
  Phase-23 / Reporters. In: all_seals, sign_metadata. Out:
  n_seals, n_inscribed, total_indus_signs, by_confidence,
  by_length, rows, inscribed_rows, method, verdict. Params:
  none. Fixed: the audited field names (confidence, sign
  sequence length). Consumers: archive ×1. → the same
  `RecordGroupSummary` family shape (distribution spec as
  params).
- **SealSignUpgradeAuditor** — CONVERT.
  `experiment_graph_phase24.py`, Phase-24 / Reporters. In:
  all_seals, upgrade_metadata. Out: n_seals,
  n_with_laursen_xref, n_high_conf, total_signs,
  by_confidence, upgrade_rows, metadata_summary, verdict.
  Params: none. Fixed: the cross-reference field name
  `laursen_2010_seal_no` and the rationale truncation
  ([:120]). Consumers: archive ×1. → the same primitive
  (xref field as param).

### F11 — Findspot & co-occurrence machinery (MeluhhaCooccurrenceCheck is §4.6)

Family target: `PrefixFindspotAssigner` (longest-prefix
match at lengths (4,3,2,1), mode reporter|filter) and
`CorpusCooccurrenceCheck`, both new.

- **CISIFindspotReporter** — CONVERT.
  `experiment_graph_phase26.py`, Phase-26 / Reporters. In:
  findspot_map, contact_zone_prefixes, inscribed_seals.
  Out: n_prefixes, n_countries, n_seals_in_cisi_vol3,
  sites_by_country, seal_findspot_assignments, verdict.
  Params: none. Fixed: the prefix lengths (4,3,2,1) tried in
  order, and the CISI Vol 3 framing. Consumers: archive ×1.
  → `PrefixFindspotAssigner` (prefix lengths as param,
  reporter mode).
- **ShuIlishuContactZoneFilter** — CONVERT.
  `experiment_graph_phase27.py`, Phase-27 / Decipherment.
  In: contact_zone_prefixes, findspot_map. Out:
  n_total_candidates, n_contact_zone, n_core_indus,
  sites_distribution, contact_zone_inscriptions_top20,
  verdict. Params: none. Fixed: the data source
  `glossa_lab.data.indus_cisi.get_corpus_inscriptions_with_ids`
  called in code, the length 3–7 filter, and the same
  (4,3,2,1) prefix matching; note the
  `contact_zone_prefixes` input is read and discarded —
  classification is driven by the findspot map's
  `is_contact_zone` flag. Consumers: archive ×1. → the same
  assigner (filter mode; corpus source as param).
- **ShuIlishuCandidateFilter** — **RETIRE-CANDIDATE**.
  `experiment_graph_phase26.py`, Phase-26 / Decipherment.
  In: findspot_map, contact_zone_prefixes. Out:
  n_contact_zone_prefixes, n_seals_total_in_contact_zone,
  n_inscriptions_inspected, verdict. Params: none.
  Evidence: no live consumer (archive ×1 only); and the
  node **cannot perform its named function** — its own
  verdict text records that the `indus_cisi` corpus view
  exposes no catalogue IDs, so it never inspects a single
  inscription (`n_inscriptions_inspected` is structurally
  0); its only real output, a sum of `n_seals_in_volume`
  over contact-zone prefixes, is subsumed by
  `ShuIlishuContactZoneFilter` above and, after F11's
  conversion, by `PrefixFindspotAssigner`. Nomination only.

### F12 — Verdict aggregators

Family target: `PredictionVerdictAggregator` (a list of
prediction specs — input field, rule, labels — as data
params), new. The family's other three members are
retire-candidates: they aggregate nothing but scalars into a
formatted summary plus canned next-phase narrative, a shape
the GENERIC `Comparator` / `PassResult` / `ReportGenerator`
/ `Merger` composition already covers.

- **Phase20Verdict** — CONVERT. `experiment_graph_phase20.py`,
  Phase-20 / Synthesis. In: length_strata,
  cluster_archaeology, ferrara_cm, fuls_positional. Out:
  prediction_1_length_dominates_spectral_gap,
  prediction_2_cluster_archaeology_nonrandom,
  prediction_3_ferrara_cm_extractable,
  prediction_4_numerical_strokes_confirmed, evidence,
  summary. Params: none. Fixed: the 4 named predictions and
  their rules — text matching (`"CONFIRMED"` in the upstream
  verdict text) and the NUMERICAL count > 5 threshold.
  Consumers: archive ×1. → `PredictionVerdictAggregator`
  (the 4 prediction specs as data). Fixture: synthetic
  upstream verdicts exercising each rule both ways.
- **Phase21Verdict** — CONVERT. `experiment_graph_phase21.py`,
  Phase-21 / Reporters. In: repetition_spectral,
  site_spectral, site_summary, numerical_weights, nw_rows,
  nw_n_poisson. Out: summary, predictions. Params: none.
  Fixed: the numeric rule set over spectral gaps (rise ≥
  max(0.10, 5 × original) → CONFIRMED; spread ≥ 0.10 /
  0.02; poisson count ≥ half). Consumers: archive ×1. → the
  same aggregator.
- **Phase22Verdict** — **RETIRE-CANDIDATE**.
  `experiment_graph_phase22.py`, Phase-22 / Reporters. In:
  n_tablets, n_persons, confirmed_hits, n_seals, n_pairings
  (all scalars). Out: summary, the echoed counts,
  next_steps, verdict. Params: none. Evidence: no live
  consumer (archive ×1); no rule beyond a threshold label on
  the counts; the `next_steps` output is canned narrative
  text naming the next phase's plan — content, not
  mechanism; subsumed by the generic composition named at
  the family head. Nomination only.
- **Phase23Verdict** — **RETIRE-CANDIDATE**.
  `experiment_graph_phase23.py`, Phase-23 / Reporters.
  Ports as the pattern above (7 scalar inputs; summary +
  counts + next_steps + verdict out). Params: none.
  Evidence: **no references anywhere outside its own
  module** — no live graph, no archive graph, no test, no
  doc; same scalar-summary shape as Phase22Verdict.
  Nomination only.
- **Phase24Verdict** — **RETIRE-CANDIDATE**.
  `experiment_graph_phase24.py`, Phase-24 / Reporters. Same
  shape (8 scalar inputs). Params: none. Evidence: no
  references anywhere outside its own module; same
  scalar-summary shape. Nomination only.

### F13 — Text & document ingestion

- **CISIVol3OCRNode** — CONVERT. `experiment_graph_phase28.py`,
  Phase-28 / Sources. In: none. Out: n_records, n_seal,
  n_iconography, n_sign_ref, records, verdict. Params:
  run_ocr, pdf_path, pages, prompt, output_path. Fixed: the
  default prompt `_OCR_PROMPT_DEFAULT` (a CISI Vol 3-specific
  extraction prompt), the line grammar it parses
  (`SEAL:` / `ICONOGRAPHY:` / `SIGN_REF:`), and the default
  output path `reports/cisi_vol3_extracted_signs.json`;
  with `run_ocr` false (the default) it is a loader of prior
  results. Consumers: archive ×1. → `VisionOCRNode` (prompt
  + grammar + paths as params — most of the surface already
  exists). Fixture: the no-OCR branch against a pinned prior
  results file; the OCR branch is provider-bound and its
  fixture is the parse of a pinned OCR transcript, not a
  live call.
- **CMCatalogParser** — CONVERT. `experiment_graph_phase20.py`,
  Phase-20 / Sources. In: pages. Out: inscriptions_sample,
  n_inscriptions_recovered, n_with_sequence, top_sign_codes,
  top_cm_unicode, n_cm_unicode_glyphs, n_pages_with_signs,
  verdict. Params: none. Fixed: the Ferrara Cypro-Minoan
  catalogue specifics — the site-prefix regex (RASH | ENKO |
  HAZO | UGAR | MARO | TEKE | MILO | HALA | KALA | KOUR),
  the Unicode block U+12F90–U+12FFF, and the verdict
  thresholds (30 / 100 / 50 / 20). Consumers: archive ×2. →
  `CatalogTextParser` (prefix set + Unicode block +
  thresholds as params; gains a parameter surface).

### F14 — Already-generic mechanisms (relabel only)

Both members carry **zero domain content in code**; they are
DOMAIN solely through their census category framing
("Phase-16-19 / Migration", "Phase-20 / Sources"). Their
conversion is a registry-metadata act (generic category; the
ScriptRunner also takes a generic id) inside the conversion
PR's completeness re-pin — no mechanism change, fixtures are
identity checks.

- **LegacyPhaseScriptRunner** — CONVERT (relabel).
  `experiment_graph_phase_legacy.py`, Phase-16-19 /
  Migration. In: none. Out: script_path, output_path,
  output_size_bytes, output_present, exit_code, stdout_tail,
  stderr_tail, json_snippet, verdict. Params: script_path,
  output_path, timeout_s. Fixed: nothing domain — it runs a
  subprocess script and tails its output; "legacy phase
  scripts" is the caller's choice of `script_path`, not
  code. Consumers: archive ×7 (the heaviest archive use in
  the 68). → generic `ScriptRunner` metadata.
- **PDFTextExtractor** — CONVERT (relabel).
  `experiment_graph_phase20.py`, Phase-20 / Sources. In:
  file_path. Out: pages, n_total_pages, n_pages_extracted,
  total_characters, file_path. Params: file_path, max_pages,
  start_page. Fixed: nothing domain — a PyMuPDF page-text
  extractor. Consumers: archive ×2. → generic category; the
  id is already generic.

## 7. Summary table — all 68

| Node | Disposition | Family | Legs / notes |
|---|---|---|---|
| M77InscriptionLoader | CONVERT | F1 | live ×3; leg 3 passes, leg 2 fails (§3) |
| ContactCorpusLoader | CONVERT | F1 | — |
| EPSD2NamesLoader | CONVERT | F1 | — |
| ICITCorpusLoader | CONVERT | F1 | — |
| MahadevanInscriptionLoader | CONVERT | F1 | second M77 pipeline (§5 flag) |
| MathematicaEpigraphicaLoader | CONVERT | F1 | — |
| IndusLiteratureLoader | CONVERT | F2 | — |
| IndusClaimsLoader | CONVERT | F2 | — |
| IndusClaimTester | CONVERT | F2 | — |
| CanonicalSignLoader | CONVERT | F3 | live ×1; H4 fixture note |
| ClusterMapper | CONVERT | F3 | live ×1 |
| StructuralTemplateAnalyzer | CONVERT | F3 | live ×1; H1 composition matches |
| ClusterArchaeology | CONVERT | F3 | — |
| IndusSignRoleClassifier | CONVERT | F3 | H3: domain = one param default |
| DefaultIndusValueRoleMap | CONVERT | F3 | — |
| IconographicAnchorScore | CONVERT | F4 | — |
| AllographAwareIconographicScore | CONVERT | F4 | collapses into F4 scorer |
| BlindHeldOutTest | CONVERT | F4 | — |
| BayesianDecoder | CONVERT | F4 | — |
| BayesianDecoderV2 | CONVERT | F4 | same primitive as V1 |
| BilingualReadoutTest | CONVERT | F5 | — |
| BilingualReadoutTestV2 | CONVERT | F5 | same primitive as V1 |
| EnhancedNameMatcher | CONVERT | F5 | — |
| EnhancedNameMatcherV2 | CONVERT | F5 | same scorer as V1 |
| MeluhhaNameMatcher | CONVERT | F5 | distinct falloff pinned |
| PeriodStratifiedReadout | CONVERT | F5 | — |
| PeriodStratifiedReadout6Bucket | CONVERT | F5 | differs from sibling only in data |
| ProvenienceStratifiedReadout | CONVERT | F5 | — |
| MeluhhanPersonsExtractor | CONVERT | F6 | — |
| RefinedMeluhhanPersonsExtractor | CONVERT | F6 | — |
| RefinedMeluhhanPersonsExtractorV2 | CONVERT | F6 | near-verbatim copy of V1 |
| Persons_v3_Extractor | CONVERT | F6 | — |
| JanabiyahPhoneticReadout | CONVERT | F7 | — |
| JanabiyahPhoneticReadoutV2 | CONVERT | F7 | renderings already via ports |
| ReverseJanabiyahSearch | CONVERT | F7 | — |
| ReverseJanabiyahSearchV2 | CONVERT | F7 | — |
| M77ReverseJanabiyahSearchV3 | CONVERT | F7 | — |
| LengthCohortReverseJanabiyahSearch | CONVERT | F7 | cohorts already a param |
| IndusAnchorSetSyllable | CONVERT | F8 | live ×1; H2 byte-identical |
| DerivedAnchorSet | CONVERT | F8 | mechanism already generic |
| EpistaticAnchorRanker | CONVERT | F8 | no domain constants |
| EpistaticInteractionDetector | CONVERT | F9 | — |
| EpistaticOrderProfile | CONVERT | F9 | no external references |
| SignContextAssociation | CONVERT | F9 | no external references |
| DoFExtractor | CONVERT | F9 | no external references |
| LanguageSignatureComparator | CONVERT | F9 | one literal domain string |
| LanguageDetectorVerdict | CONVERT | F9 | rule table as data |
| FulsPositionalClassifier | CONVERT | F9 | all thresholds already params |
| IndusNullModelTest | CONVERT | F9 | — |
| IndusSealsAtMesopotamiaSummary | CONVERT | F10 | — |
| LaursenTable1Auditor | CONVERT | F10 | — |
| MeluhhaCorpusReporter | CONVERT | F10 | — |
| Phase29CorpusStats | CONVERT | F10 | — |
| SealSignAuditor | CONVERT | F10 | — |
| SealSignUpgradeAuditor | CONVERT | F10 | — |
| CISIFindspotReporter | CONVERT | F11 | — |
| ShuIlishuContactZoneFilter | CONVERT | F11 | subsumes the retire-candidate below |
| ShuIlishuCandidateFilter | RETIRE-CANDIDATE | F11 | cannot perform its named function |
| MeluhhaCooccurrenceCheck | CONVERT | F11 | live ×1; corpus file absent from repo |
| Phase20Verdict | CONVERT | F12 | — |
| Phase21Verdict | CONVERT | F12 | — |
| Phase22Verdict | RETIRE-CANDIDATE | F12 | scalar summary + canned narrative |
| Phase23Verdict | RETIRE-CANDIDATE | F12 | no references anywhere |
| Phase24Verdict | RETIRE-CANDIDATE | F12 | no references anywhere |
| CISIVol3OCRNode | CONVERT | F13 | mostly parameterized already |
| CMCatalogParser | CONVERT | F13 | — |
| LegacyPhaseScriptRunner | CONVERT | F14 | relabel only; zero domain content |
| PDFTextExtractor | CONVERT | F14 | relabel only; zero domain content |

Counts check: 68 rows; CONVERT 64; RETIRE-CANDIDATE 4;
RETAIN 0; PROVISIONAL 0. Family sizes (CONVERT only):
F1 6, F2 3, F3 6, F4 5, F5 8, F6 4, F7 6, F8 3, F9 8, F10 6,
F11 3, F12 2, F13 2, F14 2 — sum 64.

## 8. Surprises, stated plainly

1. **Two of the 68 contain no domain content at all.**
   LegacyPhaseScriptRunner and PDFTextExtractor are generic
   mechanisms wearing phase categories (F14). Their census
   DOMAIN class is a category-label artefact.
2. **The strongest "irreducibly Indus" classifier is one
   parameter default deep.** IndusSignRoleClassifier's
   domain content is the default value of `numeral_signs`,
   proven by H3's diff.
3. **FulsPositionalClassifier needs no parameterization
   work** — every threshold is already a param; only its
   class label set is fixed.
4. **RefinedMeluhhanPersonsExtractorV2 is a near-verbatim
   duplicate of V1** (port name + one truncation differ).
   The same copy-pattern produced three copies of
   `_run_bipartite_test` (F5) and four copies of the
   Janabiyah scoring core (F7).
5. **There are two different M77 corpus pipelines** (F1):
   `data/indus_m77.py` behind MahadevanInscriptionLoader,
   and the decoded-report file + Holdat CSV fallback behind
   M77InscriptionLoader. The triage flags it; the F1 PR must
   reconcile or record why both survive.
6. **JanabiyahPhoneticReadoutV2 already receives its
   renderings through input ports** — the parameterized form
   S3 asks for exists in-tree for the family's hardest input.
7. **ShuIlishuCandidateFilter cannot do what its name
   says**, by its own verdict text (no catalogue IDs in the
   corpus view; zero inscriptions inspected, structurally).
8. **Three nodes have no references anywhere outside their
   own module** (EpistaticOrderProfile, SignContextAssociation,
   DoFExtractor) — plus the two F12 retire-candidates
   Phase23Verdict and Phase24Verdict. They convert anyway:
   zero consumers makes conversion cheap, and retirement
   needs the parent's ruling the triage does not presume for
   mechanism-bearing nodes.
9. **WritingSystemClassifier, named in the census's live
   domain-flavoured union, is GENERIC by the census's own
   classification** (§4.7) — the union mixes classes; only 6
   of its 9 ids were ever in this stage's population.
10. **MeluhhaCooccurrenceCheck's corpus file is not in the
    repo** (`backend/reports/meluhha_corpus_audit.json`
    absent): the live node currently runs against an empty
    term set. Its conversion fixture must create the file
    and pin the absence behaviour too.

## 9. Evidence index

- Population reconciliation: scripted parse of CENSUS.md
  Appendix A (517 = 90 + 359 + 68) + runtime registry
  cross-check (68/68 registered, 0 legacy-flagged, 0
  wrapper-shaped) + live-graph scan (27 graphs; 6 ids) +
  `_build_proper_graph_specs()` scan (23 specs; 0 ids).
- Consumer scan: per-id reference search over live graphs,
  `_archive/` graphs, backend code/tests, frontend, other
  specs, docs, tools, `glossa-indus/`; own defining module
  and this spec's folder excluded; comment-only hits
  inspected by hand and named as such.
- Harnesses (scratch, not committed as product code; run
  2026-11-02 against this tree): H1 StructuralTemplateAnalyzer
  vs per-length `NgramCounter` composition — template
  multisets identical (13 templates); H2 parameterized
  IndusAnchorSetSyllable vs original — `anchor_dict`
  byte-identical at MEDIUM (171 anchors), HIGH (166), LOW
  (174); H3 IndusSignRoleClassifier default vs
  `numeral_signs=[]` — sole diff the numeral role on the
  default-set signs; H4 CanonicalSignLoader empty-registry
  behaviour + ClusterMapper frequency-fallback run.
- Code facts: `inspect.getsource` over the live registry for
  all 68 functions, plus the module helpers/constants they
  call, read first-hand.

## 10. What this triage does NOT establish

- **No conversion has happened.** Every node named here
  still exists in its current domain-specific form; no
  graph, registry entry, or output has changed.
- **No future primitive's output equivalence is proven**,
  beyond the three recorded composition/parameterization
  attempts (H1–H3), which cover exactly three nodes and
  exactly the fixtures named. Each conversion PR owes its
  own pinned fixtures and byte-comparisons, and — for the
  six live ids — the C087-13 comparison runs over their
  consuming graphs.
- **No retirement is executed or pre-authorized.** The four
  RETIRE-CANDIDATEs are nominations with evidence; removal
  needs a separate parent ruling, and the S2 resolvability
  stance for archived graphs applies until then.
- **No retention is granted or denied beyond this record's
  reading of D3.** If the parent scores any node's legs
  differently, that node alone re-triages; the other 67
  dispositions are unaffected.
- **Archive-graph consumers were counted as history, not
  demand.** If the parent later rules archive resolvability
  in scope for demand, leg-3 counts change for the archive-
  used nodes — but leg 2 still fails for every one of them
  on the code evidence above, so no disposition in this
  record depends on that ruling.
- **The F1 two-pipeline question is flagged, not decided**;
  likewise the IndusNullModelTest port-shape question in F9.
  Both are conversion-PR decisions for the parent to gate.
