# Glossa Lab — User Manual

**Version**: 1.0 · BitConcepts LLC Research Platform

---

## What is Glossa Lab?

Glossa Lab is an agentic computational linguistics research platform for the statistical analysis and mapping inference of ancient and unknown writing systems. It combines:

- **Corpus management** — upload, register, inspect, and sanitize sign-sequence corpora
- **Structural analysis** — entropy, Zipf, positional profiles (T/I/M), writing-system classification
- **Mapping inference** — statistical SA-based sign-to-phoneme hypothesis generation
- **Experiment Builder** — composable graph-based experiments using atomic nodes (no coding required)
- **Study Builder** — multi-experiment research workflows composed as graphs
- **Glossa AI** — an embedded research assistant that runs analyses, proposes hypotheses, and navigates the tool
- **Reports & Data** — PDF, Markdown, JSON and CSV export of all experimental results

---

## Quick Start

### 1. Start the Backend

**Windows:** double-click the **Glossa Lab** tray icon, or run:

```
setup-os.cmd start
```

**macOS / Linux:**

```
./setup-os.sh start
```

The backend runs on **port 8001** by default. To change the port, right-click the tray icon and select **Change Port...**.

### 2. Open the UI

Navigate to **`http://localhost:8001`** in your browser.

On Windows, the tray icon provides an **Open UI** shortcut.

### 3. Upload Your First Corpus

1. Click **Corpora** in the left sidebar
2. Expand **+ Upload / import corpus**
3. Paste or load a sign-sequence file (see Corpus File Formats below)
4. Or click **Browse World Language Corpus Catalogue** to import a pre-curated corpus in one click

### 4. Run an Experiment

- Go to **Experiments** → select a graph experiment → click **Run**
- Or open **Glossa AI** and ask: *"Run the NW Semitic analysis"*

### 5. View Results

Results appear in **Reports** (PDF/Markdown) and **Data** (JSON/CSV).

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| **Ctrl+K** | Open command palette |
| **Shift+Enter** | New line in Glossa AI input |
| **Enter** | Send Glossa AI message |

---

## Tray Icon (Windows/macOS)

Right-click the system tray icon for:

- **Open UI** — opens the browser at the current port
- **Port: 8001** — displays the current port (read-only)
- **Change Port...** — opens a dialog to enter a new port. Changes are saved to `~/.glossa-lab/config.json` and the backend restarts automatically.
- **Stop Backend** — terminates the backend process

---

## Interface Overview

### Left Sidebar

The sidebar is program-scoped: open a program (workspace) and
the sidebar lists that program's views.

| View | Description |
|---|---|
| **Home** | The open program's home: its standing position and stage summary |
| **Claims** | The program's claims register |
| **Digestion** | The digestion queue: claims awaiting review |
| **Evidence & sources** | The program's evidence records and sources |
| **Data** | The program's corpora and data artefacts |
| **Analysis** | Analysis surfaces for the program's data |
| **Experiments** | Browse, build, and run graph experiments |
| **System graph** | The program's system graph: claims, evidence, and how they connect |
| **Discovery** | The discovery feed and its triage |
| **Research loop** | The automated research loop's status and controls |
| **Reports & ledger** | Generated reports and the ledger views |
| **Jobs** | Background job queue with result viewer |
| **Logs** | The backend log, live-streamed, and the durable job & phase records read as one log |
| **Status** | CPU, RAM, GPU, DB health, and backend uptime |
| **Settings** | API keys, LLM model selection, environment |
| **Help** | The in-app manual (this document's companion) |

### Logs

The **Logs** view is its own tab in the Tool home group,
between Jobs and Status (restored under Spec 087 Stage S5,
built to the approved wireframes; the pre-redesign bottom
panel was removed in the Spec 081 redesign). It has two tabs:

- **Live stream** — the backend's structured, rotating log
  file (`glossa.log`, 10 MB × 5 backups), served from
  `GET /terminal/log` (first load: the last 200 lines) and
  tailed live over `GET /terminal/log/stream`, with a
  client-side level filter, a pause control, a download of
  the last 200 lines, and a purge control
  (`POST /terminal/log/purge`) behind a confirmation that
  names what purge clears: the current file is truncated and
  its rotated backups are deleted, and it cannot be undone.
- **Job & phase records** — the durable record tables read
  as one log: jobs and their stored results (`jobs` /
  `job_results`), per-phase actions (`phase_actions`), and
  sent notifications (`notification_log`), filterable by
  kind and status, each record expandable to its stored
  detail. Read-only: the **Jobs** view remains the surface
  that acts on records.

What must survive is never only in the log stream: job and
result records are durable tables surfaced in the **Jobs**
view, phase actions and notifications are durable record
tables, and the cloud deployment keeps an append-only audit
log. The in-app events bus is a live-notification channel with
**no delivery guarantee** (the documented-ephemeral
disposition, Spec 087 decision D2): an event emitted with no
live subscriber is lost, and nothing that matters is carried
only by it — the durable surfaces above are the record.

---

## Working with Corpora

### Corpus File Formats

**Text (recommended)** — one word/inscription per line, signs separated by `-`:

```
066-069-090-112
003-069-090-112
066-069-100-073
```

**JSON** — list of inscription objects:

```json
{
  "inscriptions": [
    {"sequence": ["066", "069", "090", "112"]},
    {"sequence": ["003", "069", "090", "112"]}
  ]
}
```

**CSV** — comma-separated, one word per line:

```
066,069,090,112
003,069,090,112
```

### Uploading a Corpus

1. Click **Corpora** → **+ Upload / import corpus**
2. Enter a **Name** and choose a **Type** (linguistic, ancient, dna, code, random, other)
3. Set **Tokenisation**: Space-separated, Line-per-token, or Character-level
4. Set **Reading Direction**: LTR, RTL, or Unknown. Click **Auto-detect** to apply the Ashraf method automatically.
5. Paste content or click **Import File** (.txt / .csv / .json)
6. Click **Upload**

### Importing from the World Language Corpus Catalogue

The catalogue contains approximately 50 pre-curated corpora covering:

- **Ancient scripts**: Sumerian, Akkadian, Ge'ez, Linear B, Old Persian, Sanskrit, Old Chinese
- **Deciphered alphabets**: Greek, Latin, Hebrew, Arabic, Coptic, Syriac
- **Modern typological comparators**: English, Spanish, Hindi, Russian, Japanese, Swahili, Finnish
- **Undeciphered scripts**: Indus Valley, Linear A, Proto-Sinaitic, Meroitic, Rongorongo

To import:

1. Click **Browse World Language Corpus Catalogue**
2. Filter by All / Undeciphered / Deciphered, or search by name
3. Click **Import** on any corpus with a bundled module (loads instantly, no download)
4. Corpora without a module show a **Source** link to their public-domain origin

### Corpus Card Tabs

Click any corpus row to expand it. The tabs inside are:

| Tab | Description |
|---|---|
| **Browse** | Paginated token view. Search box filters results. Right-click to copy. |
| **Edit** | Change name, type, direction, tokenisation, and raw content. |
| **Stats** | H1 entropy, Zipf, TTR, Hapax count, Zipf bar chart, and Unicode token-type breakdown. |
| **N-grams** | Top n-grams by count, with bar chart. Select n = 1, 2, 3, or 4. |
| **Concordance** | KWIC concordance search: find a token and see its left/right context. |
| **AI** | Ask Glossa AI to analyse, detect anomalies, or critique the corpus. |
| **Compare** | Side-by-side entropy metric comparison against any other corpus. |

### Inspecting Corpus Statistics

The **Stats** tab shows:

| Metric | Description |
|---|---|
| **H1 (bits)** | Unigram entropy. Abjad: 4.1–4.7, Syllabary: 4.7–7.5, Logographic: >7.5 |
| **H2/H1 ratio** | Bigram compression vs unigram. <1.0 = strong sequential structure |
| **Conditional H** | Entropy of a sign given the preceding sign |
| **TTR** | Type-Token Ratio — vocabulary richness |
| **Zipf rho** | Pearson correlation of log-rank vs log-freq (Zipf fit quality) |
| **Hapax count** | Number of types appearing exactly once |

The **Token-Type Breakdown** panel classifies all tokens into:

| Category | Description |
|---|---|
| Numeric codes | Tokens like `066` or `066-069` (standard Glossa Lab sign codes) |
| Latin / ASCII | Latin character tokens (annotations, transcriptions) |
| Non-Latin Unicode | Ancient script glyphs (Ge'ez syllabics, Hebrew, Arabic, etc.) |
| Punctuation | Punctuation-only tokens |
| Mixed (noise) | Tokens combining two or more categories — likely corpus noise |

If more than 5% of tokens are Mixed, a warning recommends using a **TokenFilter** node before analysis.

### Detecting Reading Direction (Ashraf 2018 Method)

The Ashraf positional entropy method determines RTL vs LTR empirically from the data:

1. Compute unigram entropy at each word position across all inscriptions
2. **Lower entropy at position 0** (leftmost in file) → position 0 is word-END → **RTL script**
3. **Lower entropy at position -1** (rightmost in file) → position -1 is word-END → **LTR script**

Click **Auto-detect** in the Edit tab, or ask Glossa AI:

> "Apply the Ashraf (2018) handedness method to confirm the reading direction of this corpus."

After RTL is confirmed, all positional analyses (T/I/M profiles, anchor selection) automatically use reversed sequences.

### Sanitizing a Corpus with TokenFilter

Real-world corpora often contain noise: punctuation marks, Latin annotations mixed with ancient glyphs, or rare tokens appearing only once. Use the **TokenFilter** atomic node in your experiment graph to clean the corpus before analysis.

**TokenFilter parameters:**

| Parameter | Description |
|---|---|
| `unicode_ranges` | Keep only tokens whose characters fall within the given ranges, written as range strings (e.g. `['U+1200-U+1360']` keeps Ethiopic/Ge'ez syllabics and removes Ethiopic punctuation). Empty list disables the range filter |
| `blocklist` | List of specific token strings to always remove |
| `min_freq` | Drop token types appearing fewer than N times in the corpus. 0 = disabled |
| `keep_empty_seqs` | If true, retain sequences that become empty after filtering |

**Example — Ge'ez corpus contaminated with punctuation:**

In the Experiment Builder, connect `CorpusReader -> TokenFilter -> SADecipher`. Set `unicode_ranges = ['U+1200-U+137F']` on the TokenFilter node to keep only Ge'ez syllabic characters.

Check the **Stats -> Token-Type Breakdown** before and after filtering to confirm the result.

---

## Anchor Sets

Anchor sets store verified sign-to-phoneme assignments that can be reused across experiments. They replace hardcoded anchor dictionaries.

### Creating an Anchor Set

1. Click **Anchor Sets** in the Corpora panel
2. Click **+ New Set**
3. Enter a **Name** (e.g. "Fuls Ugaritic Anchors") and optional **Language**
4. Paste anchor pairs, one per line:

```
cipher_sign   target   confidence   note
004           T        high         Fuls verified 2024
066           M        high         Word-final mem
208           N        high         Positional I=0.92
128           L        medium       Candidate
080           W        high         Fuls verified
```

5. Click **Create**

Confidence levels: **high** (green), **medium** (yellow), **low** (red).

### Using Anchor Sets in Experiments

Add an **AnchorSetLoader** node to your experiment graph. Set its `anchor_set_id` parameter to the ID of the anchor set you created. Connect its output to the `anchors` input of an **SADecipher** node.

---

## Experiment Builder

### Architecture

All experiments are **graph experiments** — JSON specs describing a directed acyclic graph (DAG) of atomic computation nodes. No Python coding is required.

**Hierarchy:**

- **Study** — a graph of Experiments
- **Experiment** — a graph of atomic Nodes
- **Atomic Node** — a single computation step (implemented internally in Python by the platform)

### Using the Builder

1. Go to **Experiments** in the sidebar
2. Click **+ New Experiment** or open an existing one
3. Drag nodes from the **Palette** (left) onto the **Canvas** (centre)
4. Connect output ports (right side of nodes) to input ports (left side of nodes)
5. Click any node to view and edit its parameters in the **Node Inspector** (right)
6. Click **Run** to execute the graph

The Palette lists the nodes the backend's registry provides. If that list
cannot be loaded (for example, the backend is unreachable), the Palette
shows a "Node palette failed to load" error with a **Retry** button
instead of an empty list — an empty Palette with no error means the list
loaded and the search box is filtering everything out.

**Legacy nodes.** The registry also holds a large set of older
single-study nodes (mostly one per research phase) that each run one
fixed study or read one fixed report, with no inputs to wire and no
parameters to set. These are marked **legacy**: they no longer appear in
the Palette, because the Palette is the set of composable building
blocks, and a node with nothing to connect or configure is not one.
Nothing is deleted — every legacy node stays registered, and any saved
experiment that uses one still opens, runs, and produces the same
results as before. Only the offer to add new instances of them is gone.
(The full registry, legacy nodes included, remains readable through the
API's `?include_legacy=true` catalog option, for diagnostics.)

Two generic loaders, **JsonCorpusLoader** and **DatasetRecordLoader**,
are in the Palette as the composable way to load corpora and bundled
datasets: each takes its source, field mapping, and filters as
parameters. The six older corpus-specific loaders (M77, Mahadevan,
ePSD2, ICIT, Mathematica Epigraphica, and the Contact Corpus loader)
are now legacy — each one is a fixed setting of a generic loader, kept
registered and runnable for saved experiments, but no longer offered
for new ones.

Nine more generic building blocks are in the Palette:
**RegistryTableLoader** (read a registry table, with its filters as
parameters), **LabelMapApplier** (assign labels from a database table,
a JSON file, or a frequency fallback, in that order),
**TemplateMiner** (find repeated sequence templates and their slot
statistics), **ClusterContingencyProfile** (test whether a cluster's
members concentrate in one site or context), **SignRoleClassifier**
(classify signs as suffix, determinative, numeral, phonetic, logogram,
or compound from corpus statistics), **ValueRoleMapSource** (build a
value-to-role map from a base map plus per-language family tables),
**AnchorSyllabifier** (turn anchor readings into syllable tokens),
**AssociationAnchorDeriver** (derive anchors from sign-to-context
associations), and **PMICentralityRanker** (rank signs by how strongly
they associate with their neighbours). The nine older study-specific
nodes they generalise (the CGSA registry loader, cluster mapper, and
template analyser, the cluster archaeology profiler, the CTT sign-role
classifier and value-role-map source, the anchor-set syllabifier, and
the two Phase-14 anchor nodes) are now legacy in the same way: each
one is a fixed setting of a generic block, kept registered and
runnable for saved experiments, but no longer offered for new ones.

Six more generic building blocks are in the Palette:
**IconographicAnchorScorer** (score iconographic anchors against a
phoneme map, with the reading-to-phoneme alias table as a parameter
and an optional allograph-family extension), **PhonemeMapCoverage**
(apply a phoneme map to inscribed seals and report how many can be
read), **PhonemeMapPermutationTest** (test whether a phoneme map's
assignments beat shuffled-map nulls, permuting either the confidence
labels or the phoneme values), **LengthMatchScorer** (pair candidate
names with seals by length compatibility, as all-pairs, one-to-one,
or aggregated pairings), **LengthMatchPermutationTest** (test whether
the observed name-to-seal length matching beats a shuffled null),
and **StratifiedPermutationTest** (run that test separately per
period or provenience stratum, with the stratum rules as parameters).
The thirteen older study-specific nodes they generalise (the two
iconographic anchor scorers, the blind held-out test, the two
Bayesian decoders, the three name matchers, the two bilingual readout
tests, and the three stratified readouts) are now legacy in the same
way: each one is a fixed setting of a generic block, kept registered
and runnable for saved experiments, but no longer offered for new
ones.

Three more generic building blocks are in the Palette:
**SkeletonTabletSearch** (read a phonetic skeleton off a seal
reading and scan tablet lines for a set of its renderings, with the
rendering list, the keyword gate, and the minimum-hit rule as
parameters), **ReverseSkeletonSearch** (score name candidates
against the skeleton in reverse — an extracted-persons list with
substring matching, or the ePSD2 personal-name records with
exact-token matching and optional length-cohort stratification —
with the rendering set and scoring weights as parameters), and
**PersonsAggregator** (aggregate extracted person-name candidates
into frequency rows, with the field mapping, the known-names
source, and segment counting as parameters). The ten older
study-specific nodes they generalise (the two Janabiyah phonetic
readouts, the four reverse Janabiyah searches, and the four
Meluhhan persons extractors) are now legacy in the same way: each
one is a fixed setting of a generic block, kept registered and
runnable for saved experiments, but no longer offered for new
ones.

Eight more generic building blocks are in the Palette:
**InteractionSurplusProfile** (count bigram and trigram
interactions whose surplus over independence clears a threshold in
nats), **OrderInformationProfile** (decompose corpus information
by interaction order and classify the regime by a rule table over
the order fractions), **TokenContextAssociation** (permutation-
tested association between signs and a metadata context field,
with optional length binning), **MetricFieldExtractor** (pull a
flat metric vector out of wired profiler bundles using a field map
given as a parameter), **SignatureComparator** (rank corpora by
distance to a language signature template versus a negative
template), **EvidenceRuleAggregator** (combine diagnostic outputs
into one language verdict by an evidence rule table given as a
parameter), **PositionalClassClassifier** (classify signs into
functional classes by their position profile, with the class
labels and rules as parameters), and **SignPositionNullTest**
(test a sign's positional bias against a shuffle null, with the
significance bands as parameters). The eight older study-specific
nodes they generalise (the two epistatic profilers, the
sign-context association, the degrees-of-freedom extractor, the
language signature comparator, the language detector verdict, the
Fuls positional classifier, and the Indus null model test) are
now legacy in the same way: each one is a fixed setting of a
generic block, kept registered and runnable for saved
experiments, but no longer offered for new ones.

Eleven more generic blocks complete the conversion programme.
**JsonRecordDirLoader** (load JSON records from a directory, in
search or records mode, with the matching and record-shaping
rules as parameters) and **PositionalClaimTester** (test
positional claims about signs against corpus statistics, with
the claim keywords and the support rule as parameters)
generalise the Indus literature and claims loaders and the
claim tester. **RecordGroupSummary** (summarise groups of
records under ordered section specifications) and
**CorpusComparisonStats** (per-corpus sign statistics across
compared corpora) generalise the Mesopotamia seals summary,
the Laursen table auditor, the Meluhha corpus reporter, the
two seal-sign auditors, and the Phase-29 corpus statistics.
**PrefixFindspotAssigner** (assign findspots by catalogue-id
prefix, as a reporter or as a filter) and
**CorpusCooccurrenceCheck** (check whether place-name terms
co-occur across two corpora) generalise the CISI findspot
reporter, the Shu-ilishu contact-zone filter, and the Meluhha
co-occurrence check. **PredictionVerdictAggregator** (assemble
per-prediction verdicts from shaping specifications and
numeric or text rules) generalises the Phase-20 and Phase-21
verdicts. **VisionOCRNode** (run vision OCR over a PDF
catalogue under a line grammar, or reuse a prior results
file) and **CatalogTextParser** (parse inscription records
out of catalogue text) generalise the CISI Volume 3 OCR node
and the CM catalogue parser. **SyllableLMLoader** (load a
syllable-level language model from its JSON form) and
**LexiconCrossValidator** (cross-validate an anchor set
against an external rebus lexicon) generalise the Dravidian
syllable LM loader and the Kalyanaraman cross-validation.
The eighteen older study-specific nodes they generalise are
now legacy in the same way: each one is a fixed setting of a
generic block, kept registered and runnable for saved
experiments, but no longer offered for new ones. Four further
nodes — the Shu-ilishu candidate filter and the Phase-22,
Phase-23 and Phase-24 verdicts — are legacy as retire
candidates, flagged without conversion under the same rule:
kept registered and runnable, no longer offered for new
experiments, and not deleted.

### Node Reference

The reference below is **generated from the live node registry**
by `tools/manual/generate_node_reference.py` (Spec 087 S4): it
lists exactly the palette set — every registered node that is
not legacy — with each node's category, ports, and parameters
as the registry states them. The same generation feeds the
in-app Help view's node reference, so the two cannot drift
apart; a CI conformance test regenerates and diffs, and drift
in either direction fails the build. Do not edit inside the
delimiters — regenerate instead.

<!-- BEGIN GENERATED node-reference -->
Palette: **131 nodes** in 24 categories · registry: 556 registered / 425 legacy (legacy nodes are excluded — they stay resolvable for saved experiments but are not offered in the palette).

#### Analysis

**`CatalogTextParser` — Catalog Text Parser**

Best-effort inscription extraction from catalogue text pages (Spec 087 S3): inscription ids by a spec-built regex (site prefixes + CM pattern + hash pattern), transliteration sign sequences, and glyph runs in a spec Unicode block, with per-page dedupe and threshold verdicts. Prefixes, the block and the thresholds are parameters (parser_spec), not code — CMCatalogParser delegates to this engine.

- Inputs: `pages` (json, required)
- Outputs: `n_pages_processed` (number), `n_inscriptions_recovered` (number), `n_with_sequence` (number), `n_cm_unicode_glyphs` (number), `inscriptions_sample` (json), `verdict` (text)
- Params:
  - `parser_spec` (object) — Site prefixes, patterns, Unicode block, thresholds, verdict texts.

**`ClusterContingencyProfile` — Cluster Contingency Profile**

Per-cluster contingency profile over record strata (Spec 087 S3): site (strata) and length distributions for the inscriptions hosting a target cluster, enrichment rates against the corpus baseline, and a chi-squared test of strata-vs-cluster independence. The strata rule (field + prefix grouping), the significance rule, and the verdict template are parameters. The Phase-20 ClusterArchaeology delegates to this engine.

- Inputs: `inscriptions` (json, required), `sign_to_cluster` (json)
- Outputs: `site_table` (json), `length_table` (json), `chi_squared` (number), `dof` (number), `significant_p05` (any), `verdict` (text), `target_cluster_signs` (json)
- Params:
  - `target_cluster` (integer, default `0`) — Target Cluster
  - `fixed_members` (array, default `[]`) — If provided, override sign_to_cluster and use this list as the target sign set.
  - `strata_field` (string, default `"site_code"`) — Strata Field
  - `prefix_len` (integer, default `2`) — Strata Prefix Length
  - `prefix_suffix` (string, default `"0000"`) — Strata Prefix Suffix
  - `critical_per_dof` (number, default `3.84`) — Chi2 Critical per DoF
  - `site_limit` (integer, default `25`) — Site Table Limit
  - `verdict_template` (string) — Format template with {outcome} {chi2} {dof} {min_rate} {max_rate} {baseline}.

**`Clusterer` — Symbol Clusterer**

Group symbols into positional classes via L1 distance on I/M/T profiles.

- Inputs: `profiles` (profiles, required)
- Outputs: `clusters` (clusters), `n_clusters` (number)
- Params: none

**`Comparator` — AI Comparator**

Use Glossa AI to compare two upstream results and generate structured insights.

- Inputs: `a` (json, required), `b` (json, required)
- Outputs: `comparison` (json)
- Params:
  - `comparison_prompt` (string) — Guide the AI comparison. Leave blank for default.

**`CorpusComparisonStats` — Corpus Comparison Stats**

Per-corpus inscription statistics over a spec list of corpora (Spec 087 S3): input record/sequence corpora, direct loader corpora with spec-carried unavailable rows, and direct-count corpora, closed by a scale-up ratio between two rows and a verdict template. Corpus names, sequence fields and fallback rows are parameters (stats_spec), not code — Phase29CorpusStats delegates to this engine.

- Inputs: `inscribed_seals` (json), `mahadevan_inscriptions` (json)
- Outputs: `rows` (json), `scale_up_factor_cisi_to_m77` (number), `verdict` (text)
- Params:
  - `stats_spec` (object) — Corpus list, scale-up rows, verdict template.

**`CorpusCooccurrenceCheck` — Corpus Co-occurrence Check**

Check candidate names against the term set of a corpus-audit JSON file (Spec 087 S3): a candidate hits when it is a substring of a term or a term is a substring of it, counting only terms longer than a spec guard; an absent corpus file means an empty term set and an absence report. Candidate ports, the corpus path and the verdict texts are parameters (check_spec), not code — MeluhhaCooccurrenceCheck delegates to this engine.

- Inputs: `top_candidates` (json), `unique_names` (json)
- Outputs: `candidates_checked` (number), `meluhha_hits` (json), `meluhha_misses` (json), `n_hits` (number), `meluhha_corpus_available` (any), `verdict` (text)
- Params:
  - `check_spec` (object) — Candidate keys, corpus path, entries key, caps, verdict texts.

**`EntropyCalc` — Entropy Calculator**

Compute Shannon H1 and normalised H1 (Rao 2009 method).

- Inputs: `sequences` (sequences), `freq_map` (freq_map)
- Outputs: `h1` (number), `h1_normalized` (number), `number` (number)
- Params: none

**`EvidenceRuleAggregator` — Evidence Rule Aggregator**

Aggregate independent diagnostic verdicts into one judgement (Spec 087 S3): the evidence rule table (range_pair, field_equals, list_fraction_checks, success_threshold), the language score threshold, the confidence threshold, and the verdict templates are spec data. The Phase-14 LanguageDetectorVerdict delegates to this engine.

- Inputs: `zipf` (json), `conditional_entropy` (json), `mi_decay` (json), `hed` (json), `cas_projection` (json)
- Outputs: `is_language` (json), `confidence` (number), `score` (number), `evidence_for` (json), `evidence_against` (json), `verdict` (text), `json` (json)
- Params:
  - `cas_violation_low` (number, default `0.1`) — CAS Violation Low
  - `cas_violation_high` (number, default `1.0`) — CAS Violation High
  - `aggregator_spec` (object) — Ordered evidence rules, language score threshold, confidence threshold, and the three verdict templates.

**`InteractionSurplusProfile` — Interaction Surplus Profile**

Profile higher-order n-gram interactions beyond independence (Spec 087 S3): bigram PMI and trigram surplus over the pairwise baseline, counted significant at or above a spec-carried cut in nats. The Phase-14 EpistaticInteractionDetector delegates to this engine.

- Inputs: `sequences` (json, required)
- Outputs: `label` (text), `bigrams` (json), `trigrams` (json), `n_significant_bigrams` (number), `n_significant_trigrams` (number), `n_total_bigrams_examined` (number), `n_total_trigrams_examined` (number), `verdict` (text), `json` (json)
- Params:
  - `min_count_2` (integer, default `5`) — Min Bigram Count
  - `min_count_3` (integer, default `3`) — Min Trigram Count
  - `top_k` (integer, default `25`) — Top K
  - `label` (string, default `"unknown"`) — Label
  - `profile_spec` (object) — Significance cut in nats for the bigram/trigram surplus counts.

**`KLDivergence` — KL / JS Divergence**

Compute KL divergence (information gain) and Jensen-Shannon divergence between two frequency distributions. P = primary corpus; Q = reference corpus.

- Inputs: `freq_map` (freq_map, required), `q` (freq_map, required)
- Outputs: `kl_divergence` (number), `js_divergence` (number), `number` (number)
- Params: none

**`LexiconCrossValidator` — Lexicon Cross-Validator**

Cross-validate an anchor set against an external rebus lexicon (Spec 087 S3): readings normalise to root sets, and each lexicon reading is corroborated, conflicting, or a new candidate under spec caps; rebus pairs match through the root index; a grammar/content split and a banded complementarity score close the summary. Paths, markers, caps, bands and frames are parameters (validator_spec), not code — KalyanCrossValidation delegates to this engine.

- Inputs: none
- Outputs: `summary` (json), `corroborated` (json), `conflicting` (json), `new_candidates` (json), `coverage` (json)
- Params:
  - `validator_spec` (object) — Paths, normalisation, grammar markers, caps, bands, templates.

**`NgramCounter` — N-gram Counter**

Count n-gram (bigram, trigram, …) occurrences across sequences. Output freq_map uses space-joined token strings as keys.

- Inputs: `sequences` (sequences, required)
- Outputs: `freq_map` (freq_map), `n_ngrams` (number), `top_10` (json)
- Params:
  - `n` (integer, default `2`) — N
  - `top_n` (integer, default `200`) — Keep Top N

**`OrderInformationProfile` — Order Information Profile**

Decompose corpus information by interaction order (Spec 087 S3): per-symbol block entropies and their successive differences, with the regime classification carried as an ordered rule table over the order-fraction ratios. The Phase-14 EpistaticOrderProfile delegates to this engine.

- Inputs: `sequences` (json, required)
- Outputs: `label` (text), `orders` (json), `per_symbol_entropy` (json), `regime` (text), `f2_over_f1` (number), `f3_over_f2` (number), `verdict` (text), `json` (json)
- Params:
  - `max_order` (integer, default `4`) — Max Order
  - `label` (string, default `"unknown"`) — Label
  - `profile_spec` (object) — Ordered regime rules ([metric, op, threshold] conditions over f2_over_f1 / f3_over_f2) and the fallback regime.

**`PMICentralityRanker` — PMI Centrality Ranker**

Rank candidate anchor signs by PMI centrality (Spec 087 S3): the sum over bigram partners of |PMI| weighted by count — which sign's value, when fixed, most constrains the others. No domain constants. The Phase-14 EpistaticAnchorRanker delegates to this engine.

- Inputs: `sequences` (sequences, required)
- Outputs: `ranking` (json), `n_signs_ranked` (number), `verdict` (text)
- Params:
  - `top_k` (integer, default `10`) — Top K
  - `min_count` (integer, default `5`) — Min Bigram Count

**`PhonemeMapPermutationTest` — Phoneme Map Permutation Test**

Permutation test of a phoneme map's assignment over inscribed seals (Spec 087 S3): the observed confidence-weighted coverage total is compared against null maps that shuffle one dimension of the map — the confidence labels, or the phoneme values with an optional compound-plausibility reweighting whose pattern table and bonuses are data. The Phase-26 BayesianDecoder and the Phase-27 BayesianDecoderV2 delegate to this engine.

- Inputs: `inscribed_seals` (json, required), `phoneme_map` (json, required)
- Outputs: `n_seals` (number), `n_phonemes_in_map` (number), `observed_total_weight` (number), `null_mean_weight` (number), `observed_total_score` (number), `null_mean_score` (number), `p_value` (number), `n_perms` (number), `obs_per_seal_top10` (json), `obs_per_seal` (json), `verdict` (text), `interpretation` (text)
- Params:
  - `n_permutations` (integer, default `1000`) — Permutations
  - `seed` (integer, default `1234`) — Seed
  - `decoder_spec` (object) — Shuffle dimension, confidence weights, plausibility patterns/bonuses, null gloss, output key names, verdict template, interpretation.

**`PositionalClaimTester` — Positional Claim Tester**

Test typed claims against a sequence corpus (Spec 087 S3): a claim is testable when its type contains a spec keyword, it names a sign, and its normalized text names a position; each named sign's observed positional rate is compared with the corpus average over frequent signs, scaled by a spec multiplier. Untestable claims are skipped silently. The Indus-evidence IndusClaimTester delegates to this engine.

- Inputs: `claims` (claims, required), `sequences` (sequences, required)
- Outputs: `test_results` (json), `n_tested` (number), `n_supported` (number), `support_rate` (number), `json` (json), `number` (number), `text` (text)
- Params:
  - `tester_spec` (object) — Type keywords, position needles, support rule, error and verdict texts.

**`PositionalClassClassifier` — Positional Class Classifier**

Classify signs by their within-sequence position profile (Spec 087 S3): the class label set, the ordered dominant-position rules, and the verdict template are spec data; the classification thresholds stay plain params. The Phase-20 FulsPositionalClassifier delegates to this engine.

- Inputs: `sequences` (json, required)
- Outputs: `table` (json), `counts_by_class` (json), `fractions_by_class` (json), `n_signs_classified` (number), `verdict` (text)
- Params:
  - `min_count` (integer, default `5`) — Min Count
  - `dom_threshold` (number, default `0.55`) — Dominance Threshold
  - `secondary_threshold` (number, default `0.3`) — Secondary Threshold
  - `numerical_rr` (number, default `0.2`) — Numerical Repeat Rate
  - `classifier_spec` (object) — Class label set, ordered position-class rules (label key + dominant position), and the verdict template.

**`PositionalProfiler` — Positional Profiler**

Compute I/M/T position rates per symbol (Fuls 2013 NWSP method).

- Inputs: `sequences` (sequences, required)
- Outputs: `profiles` (profiles), `class_summary` (json)
- Params:
  - `min_count` (integer, default `3`) — Min Count

**`PredictionVerdictAggregator` — Prediction Verdict Aggregator**

Aggregate sub-experiment outputs into per-prediction verdicts (Spec 087 S3): spec-carried input shaping (verdict-text and per-bin extraction, shaped and synthesised inputs) and rule kinds — text match, count threshold, gap rise, gap spread, poisson fraction — assembled flat or nested. Rule sets, thresholds, detail texts and summaries are parameters (aggregator_spec), not code — Phase20Verdict and Phase21Verdict delegate to this engine.

- Inputs: `length_strata` (json), `repetition_spectral` (json)
- Outputs: `summary` (text), `predictions` (json), `evidence` (json)
- Params:
  - `aggregator_spec` (object) — Shaping, rules, evidence, assembly, summary template.

**`PrefixFindspotAssigner` — Prefix Findspot Assigner**

Assign records to find-spots by longest-prefix match of their catalogue id against a find-spot map (Spec 087 S3): reporter mode summarises the map and lists assignments (key-presence match); filter mode classifies a spec-named corpus getter's records into contact-zone / core lists (truthy-info match, so empty info entries fall through to shorter prefixes). Prefix lengths, match semantics and texts are parameters (assigner_spec), not code — CISIFindspotReporter and ShuIlishuContactZoneFilter delegate to this engine.

- Inputs: `findspot_map` (json), `inscribed_seals` (json)
- Outputs: `sites_by_country` (json), `sites_distribution` (json), `verdict` (text)
- Params:
  - `assigner_spec` (object) — Mode, prefix lengths, corpus getter (filter mode), verdict templates.

**`RecordGroupSummary` — Record Group Summary**

Grouped summary over a record list (Spec 087 S3): per-record computed fields, then ordered spec blocks — counts, value counters, row projections, derived subsets, sums, match and presence counts, top-N sections over inputs — closed by a verdict template. Field names, defaults, orders, caps and texts are parameters (summary_spec), not code — the phase auditors and reporters delegate to this engine.

- Inputs: `records` (json)
- Outputs: `verdict` (text), `json` (json)
- Params:
  - `summary_spec` (object) — Records key, per-record computed fields, ordered blocks, verdict template.

**`ShuffleControl` — Shuffle Control**

Create a shuffled control corpus for statistical significance testing. Destroys sequential structure while preserving unigram frequencies. Use in parallel with real corpus to test whether sequence order matters.

- Inputs: `sequences` (sequences, required)
- Outputs: `sequences` (sequences), `n_sequences` (number)
- Params:
  - `mode` (string, default `"within_word"`) — within_word: shuffle within each word | global: shuffle all signs
  - `seed` (integer, default `42`) — Random Seed

**`SignPositionNullTest` — Sign Position Null Test**

Test a sign's positional bias against a shuffle null (Spec 087 S3): the observed position-class rate is compared against shuffled re-deals of every sequence, and the z-score maps to a verdict through a spec-carried band table. Sequence-shaped by design — it does not reuse the score-shaped PermutationTest. The Indus-evidence IndusNullModelTest delegates to this engine.

- Inputs: `sequences` (json, required)
- Outputs: `z_score` (number), `p_approx` (number), `verdict` (text), `json` (json), `text` (text)
- Params:
  - `target_sign` (string, default `""`) — Target Sign
  - `test_type` (string, default `"initial"`) — Position Class
  - `n_null_runs` (integer, default `1000`) — Null Runs
  - `random_seed` (integer, default `42`) — Random Seed
  - `null_spec` (object) — Ordered [|z| threshold, verdict] bands and the fallback verdict.

**`SignRoleClassifier` — Sign Role Classifier**

Derive a role mask per sign from corpus statistics (Spec 087 S3): positional rates, strict/relaxed suffix rules, a numeral repetition heuristic, a behaviour-based logogram detector, and bigram-PMI compound detection. Every threshold is a parameter, and the numeral sign set is a parameter that defaults EMPTY — a domain caller's set is data it passes in. The CTT IndusSignRoleClassifier delegates to this engine with its Indus numeral set as the default value.

- Inputs: `sequences` (sequences, required)
- Outputs: `role_table` (json), `n_signs` (number), `role_summary` (json), `compound_signs` (json), `high_pmi_bigrams` (json)
- Params:
  - `terminal_threshold` (number, default `0.85`)
  - `terminal_relaxed` (number, default `0.45`)
  - `initial_threshold` (number, default `0.7`)
  - `compound_pmi_threshold` (number, default `4.0`)
  - `min_count` (integer, default `5`)
  - `numeral_signs` (array, default `[]`) — Signs classed numeral on sight. Empty by design; domain sets are caller data.
  - `numeral_repetition_threshold` (number, default `0.5`)
  - `logogram_min_count` (integer, default `20`)
  - `logogram_position_concentration` (number, default `0.55`)
  - `logogram_solo_rate` (number, default `0.05`)

**`SignatureComparator` — Signature Comparator**

Rank candidate corpora by closeness to language vs negative signature templates (Spec 087 S3): the candidate tag and marker, the negative-tag set, and the verdict margin are spec data. The Phase-14 LanguageSignatureComparator delegates to this engine.

- Inputs: `a` (json), `b` (json), `c` (json), `d` (json), `e` (json), `f` (json)
- Outputs: `ranked` (json), `language_template` (json), `verdict` (text), `json` (json)
- Params:
  - `target_label` (string, default `""`) — Target Label
  - `comparator_spec` (object) — Candidate tag and marker substrings, the negative-tag set, the verdict margin, the feature keys, and the verdict templates.

**`TemplateMiner` — Template Miner**

Find recurrent templates in label sequences (Spec 087 S3): n-gram template mining over a length range with a minimum count, plus the summary fields a plain n-gram composition cannot carry in one node — dominant prefix/suffix labels, per-slot occupancy, and the class-sequence entropy. Length range and cuts are parameters. The CGSA StructuralTemplateAnalyzer delegates to this engine. NO phonetic claims made; outputs are structural class labels.

- Inputs: `cluster_sequences` (json, required)
- Outputs: `recurrent_templates` (json), `n_templates` (number), `dominant_prefix_clusters` (json), `dominant_suffix_clusters` (json), `slot_occupancy` (json), `h_class_sequence` (number), `n_distinct_class_sequences` (number)
- Params:
  - `min_count` (integer, default `3`) — Min Template Count
  - `max_template_length` (integer, default `5`) — Max Template Length
  - `min_template_length` (integer, default `2`) — Min Template Length
  - `top_templates` (integer, default `50`) — Top Templates
  - `top_slots` (integer, default `10`) — Top Slots

**`TokenContextAssociation` — Token-Context Association**

Permutation-tested association between tokens and a metadata context field (Spec 087 S3): the significance cut, the strong-verdict minimum, and the optional length binning are spec data. The Phase-14 SignContextAssociation delegates to this engine.

- Inputs: `sequences` (json, required), `metadata` (json, required)
- Outputs: `associations` (json), `n_significant` (number), `n_total_pairs` (number), `field` (text), `verdict` (text), `json` (json)
- Params:
  - `field` (string, default `"type"`) — Context Field
  - `n_perm` (integer, default `8`) — Permutations
  - `seed` (integer, default `11`) — Seed
  - `min_count` (integer, default `5`) — Min Pair Count
  - `top_k` (integer, default `30`) — Top K
  - `association_spec` (object) — Significance cut, strong-verdict minimum, verdict templates, and the length binning (binned field, source field, [bound, name] bins, default bin).

**`WritingSystemClassifier` — Writing System Classifier**

Classify a corpus typologically by comparing its structural metrics (H1 entropy, sign count, average word length) against 11 known writing systems. Identifies whether the corpus is most similar to an abjad, syllabary, logosyllabic, or logographic system. Connects: EntropyCalc.h1 → h1, FreqCounter.distinct_symbols → n_signs.

- Inputs: `h1` (number, required), `distinct_symbols` (number, required), `avg_word_len` (number)
- Outputs: `tier_classification` (text), `nearest_script` (text), `top3_nearest` (json), `all_ranked` (json), `text` (text)
- Params:
  - `n_signs` (integer, default `0`) — Override if distinct_symbols not connected
  - `avg_word_len` (number, default `0.0`) — Override avg word length

**`ZipfFitter` — Zipf Fitter**

Estimate the Zipf exponent via log-rank regression (Yadav 2010).

- Inputs: `freq_map` (freq_map, required)
- Outputs: `zipf_exponent` (number), `number` (number)
- Params: none

#### CTT / Constraint Topology

**`AnchorAblator` — Anchor Ablator (negative control)**

Drop all iconographic anchors so SA starts from a uniform-random initial mapping. Use to verify anchor priors actually contribute.

- Inputs: `anchors` (json), `family` (text)
- Outputs: `anchors` (json), `n_anchors` (number), `family` (text), `weight` (number)
- Params:
  - `family` (string, default `"unknown"`)

**`AttestedVocabularyLoader` — Attested Vocabulary Loader**

Load an attested-language word list (Old Tamil, Hieroglyphic Luwian, Mycenaean Greek, Vedic Sanskrit, Sumerian) as the gold-standard source for HoldoutWordRecall and CompoundDependencyConstraint.

- Inputs: none
- Outputs: `attested_vocab` (json), `n_words` (number), `family` (text)
- Params:
  - `family` (string, default `"old_tamil"`) — old_tamil | hieroglyphic_luwian | mycenaean_greek | vedic_sanskrit | sumerian
  - `extra_words` (array, default `[]`)
  - `min_len` (integer, default `2`)
  - `max_len` (integer, default `12`)

**`CTTAdmissibilityFilter` — CTT Admissibility Filter**

Per-sign feasibility oracle (Constraint Topology Theory, BitConcepts 2026). Filters a proposed sign-to-value mapping by checking each (sign, value) pair against the sign's admissible roles. O(K) per Theorem 1 of CTT TR. Connects: IndusSignRoleClassifier → role_table; SADecipher → proposed_mapping.

- Inputs: `role_table` (json, required), `proposed_mapping` (json, required), `value_role_map` (json)
- Outputs: `filtered_mapping` (json), `violations` (json), `n_violations` (number), `n_admissible` (number), `admissibility_rate` (number)
- Params:
  - `value_role_map` (object, default `{}`) — Map target-language values to roles. Use DefaultIndusValueRoleMap for the standard set.
  - `strict_mode` (boolean, default `false`) — If True, values not present in value_role_map are treated as having an 'unmapped' role and are filtered as violations (rigorous CTT default). If False, unmapped values fall back to 'phonetic' and pass the filter unless the sign forbids phonetic.

**`CTTAnchoredSADecipher` — CTT-Anchored SA Decipherer**

Simulated annealing decipherment with the CTT admissibility oracle filtering every proposal step. Forbidden (sign, value) pairs are mathematically unselectable per CTT Claim 9. Restarts and seeds controlled like the standard SADecipher. Pure primitive: one engine call with a constraint mask. Use this in place of SADecipher when role_table is available and you want guaranteed-admissible outputs. When `compound_weight` > 0 and high_pmi_bigrams + attested_vocab are wired in, restart selection becomes joint over LM + compound coupling (Cotterell/Eisner 2015 single-pass dual decomposition).

- Inputs: `sequences` (sequences, required), `lm` (any, required), `role_table` (json), `value_role_map` (json), `anchors` (any), `high_pmi_bigrams` (json), `attested_vocab` (json)
- Outputs: `proposed_mapping` (json), `score` (number), `lm_score` (number), `compound_score` (number), `compound_hits` (number), `compound_misses` (number), `n_signs` (number), `n_forbidden_pairs` (number), `n_filtered_proposals` (number), `n_total_proposals` (number), `filter_rate` (number), `anchors_used` (number)
- Params:
  - `seed` (integer, default `1`)
  - `max_iterations` (integer, default `8000`)
  - `restarts` (integer, default `5`)
  - `surjective` (boolean, default `true`)
  - `value_role_map` (object, default `{}`)
  - `strict_mode` (boolean, default `false`) — If True, the final mapping is post-filtered to drop any value missing from value_role_map. Treats unmapped values as having a forbidden role.
  - `compound_weight` (number, default `0.0`) — Weight on the compound-coupling term in the joint score. Set to 1.0 to enable joint LM + compound selection. Requires high_pmi_bigrams + attested_vocab.
  - `compound_separator` (string, default `""`)

**`CompoundDependencyConstraint` — Compound Dependency Constraint**

Score a sign mapping under cross-sign compound coupling (Cotterell/Eisner 2015 dual-decomposition idea). For each high-PMI compound bigram, concatenated decoded value should appear in attested vocabulary. Awards bonus per hit, penalty per miss. This is the dense-dependency layer that pure CTT (independent constraints) cannot capture.

- Inputs: `proposed_mapping` (json, required), `high_pmi_bigrams` (json, required), `attested_vocab` (json)
- Outputs: `compound_score` (number), `n_hits` (number), `n_misses` (number), `hit_rate` (number), `hits` (json), `misses` (json), `number` (number)
- Params:
  - `hit_bonus` (number, default `1.0`)
  - `miss_penalty` (number, default `0.5`)
  - `compound_separator` (string, default `""`)
  - `attested_vocab` (array, default `[]`)

**`CorpusPermuter` — Corpus Permuter (negative control)**

Permute the corpus to produce a negative-control input. Modes: 'relabel' (replace every sign id with a uniform random sign), 'shuffle_within' (shuffle tokens inside each inscription), 'shuffle_global' (flat-shuffle every token across the corpus).

- Inputs: `sequences` (sequences, required)
- Outputs: `sequences` (sequences), `mode` (text), `n` (number), `n_tokens` (number)
- Params:
  - `seed` (integer, default `23`)
  - `mode` (string, default `"relabel"`)

**`CorpusStratifier` — Corpus Stratifier (by inscription length)**

Stratify M77 inscriptions by length into short / medium / long sub-corpora. Inscription length is a proxy for text type (short = seal, long = copper plate / pottery graffiti).

- Inputs: `sequences` (sequences, required)
- Outputs: `short_sequences` (sequences), `medium_sequences` (sequences), `long_sequences` (sequences), `stratum_summary` (json)
- Params:
  - `short_max` (integer, default `2`)
  - `medium_max` (integer, default `5`)

**`DeltaRecall` — Delta Recall (Phase-13)**

Compute the recall delta between a real-corpus run and one or more negative-control runs (permuted corpus, ablated anchors, ablated vocab). Phase-12 showed permuted recall on Tamil > real recall, so this delta is the headline-quality metric: positive delta_permuted means the corpus structure is contributing.

- Inputs: `real_recall` (number), `permuted_recall` (number), `anchor_ablated_recall` (number), `vocab_ablated_recall` (number)
- Outputs: `real_recall` (number), `permuted_recall` (number), `anchor_ablated_recall` (number), `vocab_ablated_recall` (number), `delta_permuted` (number), `delta_anchor` (number), `delta_vocab` (number), `best_delta` (number), `verdict` (text)
- Params:
  - `real_recall` (number)
  - `permuted_recall` (number)
  - `anchor_ablated_recall` (number)
  - `vocab_ablated_recall` (number)

**`GranularityComparison` — Granularity Comparison**

Rank multiple LMGranularityProfiler outputs by vocab + role-map compatibility and emit a textual verdict identifying the best LM for the target language family.

- Inputs: `a` (json), `b` (json), `c` (json), `d` (json), `e` (json), `f` (json)
- Outputs: `ranking` (json), `best` (json), `verdict` (text)
- Params: none

**`HoldoutWordRecall` — Held-out Word Recall**

Decode each held-out inscription with the proposed mapping and count matches against an attested external vocabulary. NON-CIRCULAR test. Connects: CorpusSplitter.test_sequences → sequences, SADecipher → proposed_mapping, AttestedVocabularyLoader → attested_vocab.

- Inputs: `sequences` (sequences, required), `proposed_mapping` (json, required), `attested_vocab` (json)
- Outputs: `recall_score` (number), `n_decoded` (number), `n_attested_hits` (number), `n_unique_hits` (number), `hit_rate` (number), `matched_words` (json), `number` (number)
- Params:
  - `decode_separator` (string, default `""`)
  - `min_word_len` (integer, default `2`)
  - `attested_vocab` (array, default `[]`)

**`IconographicAnchorPin` — Iconographic Anchor Pin**

Emit Mahadevan/Parpola-style iconographic anchors as a sign→value mapping. Wire to CTTAnchoredSADecipher.anchors to bias the SA initial mapping toward established iconic readings (fish=min, jar=kutam, U=uravu, ...). Defaults are family + code_system aware: set code_system='m77' when the upstream corpus is Mahadevan 1977 (indus_m77) so anchors fire on M77 numeric sign IDs.

- Inputs: none
- Outputs: `anchors` (json), `n_anchors` (number), `family` (text), `weight` (number), `code_system` (text)
- Params:
  - `family` (string, default `"old_tamil"`)
  - `weight` (number, default `1.0`)
  - `anchors` (object, default `{}`)
  - `code_system` (string, default `"parpola"`) — Sign-ID code system the upstream corpus uses: 'parpola' (P-codes, CISI) or 'm77' (Mahadevan 1977).

**`KFoldAggregator` — K-Fold Aggregator**

Aggregate up to 10 per-fold scalar metrics into mean / std / 95% CI. Wire each fold's metric (e.g. recall) into ports a..j.

- Inputs: `a` (number), `b` (number), `c` (number), `d` (number), `e` (number), `f` (number), `g` (number), `h` (number), `i` (number), `j` (number)
- Outputs: `k` (number), `mean` (number), `std` (number), `ci_low` (number), `ci_high` (number), `values` (json), `verdict` (text)
- Params: none

**`KFoldCorpusSplitter` — K-Fold Corpus Splitter**

Emit k disjoint train/test partitions of the input sequences for k-fold cross-validation. Convenience output (train_sequences / test_sequences) points at the first fold; the full `folds` list can be consumed by graph runners that fan out across folds.

- Inputs: `sequences` (sequences, required)
- Outputs: `folds` (json), `k` (number), `n` (number), `train_sequences` (sequences), `test_sequences` (sequences), `fold_summaries` (json)
- Params:
  - `k` (integer, default `10`)
  - `seed` (integer, default `7`)

**`KFoldRunner` — K-Fold Runner**

True k-fold cross-validation runner. Internally splits the corpus, runs CTTAnchoredSADecipher + HoldoutWordRecall + CompoundDependencyConstraint on each fold, and aggregates per-fold recall and compound score into mean / std / 95% CI. Replaces the Phase-11 single-fold wiring with a real k-fold experiment. Phase-12 (2026-04-28).

- Inputs: `sequences` (sequences, required), `lm` (any, required), `role_table` (json), `value_role_map` (json), `anchors` (json), `attested_vocab` (json), `high_pmi_bigrams` (json)
- Outputs: `k` (number), `per_fold` (json), `recall_values` (json), `compound_values` (json), `recall_mean` (number), `recall_std` (number), `recall_ci_low` (number), `recall_ci_high` (number), `compound_mean` (number), `verdict` (text)
- Params:
  - `k` (integer, default `5`)
  - `seed` (integer, default `7`)
  - `sa_seed_base` (integer, default `11`)
  - `max_iterations` (integer, default `4000`)
  - `restarts` (integer, default `3`)
  - `surjective` (boolean, default `true`)
  - `strict_mode` (boolean, default `true`)
  - `compound_weight` (number, default `1.0`)
  - `compound_separator` (string, default `""`)
  - `decode_separator` (string, default `""`)
  - `min_word_len` (integer, default `2`)
  - `hit_bonus` (number, default `1.0`)
  - `miss_penalty` (number, default `0.5`)

**`LMGranularityProfiler` — LM Granularity Profiler**

Diagnose an LM's symbol granularity (character / syllabic / word / mixed) and report its overlap with the attested vocab and value-role map for a target language. Use BEFORE strict-mode SA to ensure the LM produces symbols at a granularity compatible with the role-map filter.

- Inputs: `lm` (any, required), `attested_vocab` (json), `value_role_map` (json)
- Outputs: `label` (text), `granularity` (text), `mean_symbol_len` (number), `median_symbol_len` (number), `vocab_overlap` (number), `role_map_overlap` (number), `n_symbols` (number), `length_distribution` (json), `top_symbols` (json), `verdict` (text), `json` (json)
- Params:
  - `label` (string, default `"unknown"`)

**`LogogramAwareValueRoleMap` — Logogram-Aware Value-Role Map (Phase-13)**

Take an upstream value_role_map and re-tag a list of words (provided via `logogram_words` input or top-N from attested_vocab) as 'logogram'. Phase-12 detected 23 logograms in M77 but the role map had no logogram-tagged values, making the bit inert. This node closes that gap.

- Inputs: `value_role_map` (json, required), `logogram_words` (json), `attested_vocab` (json)
- Outputs: `value_role_map` (json), `json` (json), `n_values` (number), `n_logograms_promoted` (number), `n_logograms_total` (number), `n_skipped_preserved` (number), `family` (text), `promoted_sample` (json), `skipped_sample` (json)
- Params:
  - `family` (string, default `"old_tamil"`)
  - `top_n` (integer, default `30`)
  - `min_word_len` (integer, default `3`)
  - `preserve_suffixes` (boolean, default `true`)

**`MatchedWordReporter` — Matched Word Reporter**

Aggregate matched_words from up to six HoldoutWordRecall branches into a single sortable table. Param `labels` names the branches in port order (a..f).

- Inputs: `a` (json), `b` (json), `c` (json), `d` (json), `e` (json), `f` (json)
- Outputs: `table` (json), `n_rows` (number), `by_branch` (json), `summary` (json)
- Params:
  - `labels` (array, default `[]`)

**`MultiWordHitRate` — Multi-Word Hit Rate (Phase-13)**

HoldoutWordRecall variant that only counts inscriptions whose decoded length is at least `min_seq_length` tokens. Eliminates the short-CV trivial-match artifact uncovered by Phase-12 stratification (short=0.74 / medium=0.05 / long=0.11).

- Inputs: `sequences` (sequences, required), `proposed_mapping` (json, required), `attested_vocab` (json)
- Outputs: `recall_score` (number), `n_decoded` (number), `n_attested_hits` (number), `n_unique_hits` (number), `hit_rate` (number), `matched_words` (json), `min_seq_length` (number), `n_filtered_short` (number), `verdict` (text)
- Params:
  - `decode_separator` (string, default `""`)
  - `min_seq_length` (integer, default `3`)
  - `min_word_len` (integer, default `2`)
  - `attested_vocab` (array, default `[]`)

**`PMIBigramAligner` — PMI Bigram Aligner (Phase-13, Berg-Kirkpatrick baseline)**

Direct rank-based alignment of Indus high-PMI bigrams to target-language attested compound bigrams. No SA. Berg-Kirkpatrick 2011 / Cotterell-Eisner 2015 baseline against which the CTT-anchored SA can be compared. Greedy alignment in descending count order; supports preset anchors.

- Inputs: `high_pmi_bigrams` (json, required), `attested_vocab` (json, required), `anchors` (json)
- Outputs: `proposed_mapping` (json), `alignment_table` (json), `n_alignments` (number), `n_signs` (number), `n_anchored` (number), `verdict` (text)
- Params:
  - `target_separator` (string, default `""`)
  - `target_token_len` (integer, default `2`)
  - `max_alignments` (integer, default `30`)
  - `anchors` (object, default `{}`)

**`RoleShuffledNullDistribution` — Role-Shuffled Null Distribution (Phase-13)**

Build a null where the LM and corpus are kept fixed but the role_table assignments are shuffled across signs. Real-mode recall inside this null means the role classifier contributes no decipherment signal.

- Inputs: `sequences` (sequences, required), `lm` (any, required), `attested_vocab` (json, required), `observed_recall` (number, required), `role_table` (json, required), `value_role_map` (json), `anchors` (json), `high_pmi_bigrams` (json)
- Outputs: `null_recalls` (json), `null_mean` (number), `null_std` (number), `observed_recall` (number), `z_score` (number), `empirical_p` (number), `n_trials` (number), `verdict` (text)
- Params:
  - `n_trials` (integer, default `6`)
  - `seed` (integer, default `31`)
  - `iterations_per_trial` (integer, default `1500`)
  - `decode_separator` (string, default `""`)
  - `min_word_len` (integer, default `2`)
  - `compound_weight` (number, default `0.0`)
  - `compound_separator` (string, default `""`)
  - `strict_mode` (boolean, default `true`)

**`ShuffledLMNullDistribution` — Shuffled-LM Null Distribution**

Build an empirical null recall distribution by running SA against shuffled-LM-unigram clones of the input LM. Reports z-score and empirical p of the observed recall vs. the shuffled null. Use to convert raw recall into a defensible significance claim.

- Inputs: `sequences` (sequences, required), `lm` (any, required), `attested_vocab` (json, required), `observed_recall` (number, required), `role_table` (json), `value_role_map` (json)
- Outputs: `null_recalls` (json), `null_mean` (number), `null_std` (number), `observed_recall` (number), `z_score` (number), `empirical_p` (number), `n_trials` (number), `verdict` (text)
- Params:
  - `n_trials` (integer, default `50`)
  - `seed` (integer, default `17`)
  - `iterations_per_trial` (integer, default `1500`)
  - `decode_separator` (string, default `""`)

**`SignMappingConsistency` — Sign Mapping Consistency (Phase-13)**

Compute pairwise per-sign agreement across multiple proposed mappings (Tamil / Luwian / Greek / Sanskrit, etc.). High agreement on the same Indus signs indicates a real cross- language signal; low agreement is consistent with each branch finding language-specific noise. Up to six branches via ports a..f.

- Inputs: `a` (json), `b` (json), `c` (json), `d` (json), `e` (json), `f` (json), `freq_map` (json)
- Outputs: `pairwise` (json), `modal_per_sign` (json), `n_full_agreement` (number), `n_signs_compared` (number), `avg_pairwise_value_agreement` (number), `verdict` (text)
- Params:
  - `labels` (array, default `[]`)
  - `top_k` (integer, default `0`)

**`VocabularyAblator` — Vocabulary Ablator (negative control)**

Strip or shuffle the attested vocabulary so HoldoutWordRecall sees no real targets. Recall should collapse to chance.

- Inputs: `attested_vocab` (json)
- Outputs: `attested_vocab` (json), `n_words` (number), `mode` (text)
- Params:
  - `mode` (string, default `"empty"`)
  - `seed` (integer, default `41`)

#### Contact Zone

**`ContactZoneABComparison` — Contact Zone A/B Comparison**

Compare two corpora A and B against Indus to determine which shows stronger contact signal. Returns winner, confidence, and per-corpus divergence.

- Inputs: `sequences_indus` (sequences, required), `sequences_a` (sequences), `sequences_b` (sequences)
- Outputs: `winner` (text), `confidence` (number), `verdict` (text), `result_a` (json), `result_b` (json)
- Params:
  - `label_a` (string, default `"corpus_a"`)
  - `label_b` (string, default `"corpus_b"`)
  - `top_n` (integer, default `15`)

**`ContactZoneKLDivergence` — Contact Zone KL Divergence**

Compute KL and JS divergence between two corpus symbol distributions. Returns divergence score, top-N overlapping symbols, and contact verdict.

- Inputs: `sequences_a` (sequences), `sequences_b` (sequences), `freq_map_a` (freq_map), `freq_map_b` (freq_map)
- Outputs: `kl_divergence` (number), `js_divergence` (number), `top_overlap` (json), `verdict` (text), `number` (number)
- Params:
  - `label_a` (string, default `"corpus_a"`)
  - `label_b` (string, default `"corpus_b"`)
  - `top_n` (integer, default `20`)

**`ContactZoneSynthesis` — Contact Zone Synthesis**

Synthesise multiple KL divergence comparisons into a ranked summary of which language families show highest contact signal with the target corpus.

- Inputs: `comparisons` (json), `a` (any), `b` (any), `c` (any), `d` (any)
- Outputs: `ranked_summary` (json), `strongest_contact` (text), `verdict` (text)
- Params:
  - `top_n` (integer, default `10`)

#### Cross-Language

**`AnchoredSALanguageAB` — Anchored SA Language A/B**

A/B language comparison using anchored SA: loads LMs for two languages, runs SA on the Indus corpus, compares consistency and z-scores. Returns winner, confidence, and per-language evidence.

- Inputs: `sequences` (sequences)
- Outputs: `winner` (text), `confidence` (number), `evidence` (text), `verdict` (text), `lang_a_zscore` (number), `lang_b_zscore` (number)
- Params:
  - `lang_a` (string, default `"dravidian"`) — Language A identifier (e.g. dravidian, sumerian)
  - `lang_b` (string, default `"sanskrit"`) — Language B identifier (e.g. sanskrit, hebrew)
  - `n_seeds` (integer, default `3`)
  - `max_iterations` (integer, default `3000`)

**`CulturalContactMatrix` — Cultural Contact Matrix**

Compute pairwise contact scores between multiple corpora using entropy signature overlap and KL-divergence. Returns a ranked matrix of which cultures show strongest contact signals.

- Inputs: `corpora` (json), `a` (any), `b` (any), `c` (any), `d` (any), `e` (any)
- Outputs: `matrix` (json), `signatures` (json), `verdict` (text)
- Params:
  - `top_n` (integer, default `10`)

**`LMConsistencyMatrix` — LM Consistency Matrix**

Synthesise multiple A/B language pairing results into an overall consistency matrix with Dravidian confidence score.

- Inputs: `pairings` (json), `a` (any), `b` (any), `c` (any)
- Outputs: `matrix` (json), `dravidian_confidence` (number), `verdict` (text)
- Params: none

**`ScriptFamilyClassifier` — Script Family Classifier**

Classify a script into writing system families (syllabary, logographic, abjad, alphabet, undetermined) using bigram entropy, type-token ratio, Zipf alpha, and positional bias features.

- Inputs: `sequences` (sequences, required)
- Outputs: `classification` (text), `confidence` (number), `features` (json), `scores` (json), `verdict` (text)
- Params:
  - `label` (string, default `"unknown"`) — Label for the corpus being classified

#### Decipherment

**`AnchorConvergenceBenchmark` — Anchor Convergence Benchmark**

Sweep anchor counts and measure convergence in a known-cipher self-test (requires CipherConstructor output). For each anchor count runs structured (frequency-ranked) and random anchor sets; reports accuracy, consistency, and distinct-mappings per condition. Answers: do anchors drive convergence? Connects: CipherConstructor → cipher_sequences + true_mapping + sign_inventory; LMBuilder → lm.

- Inputs: `cipher_sequences` (sequences, required), `lm` (any, required), `true_mapping` (json, required), `sign_inventory` (json)
- Outputs: `results_by_anchor_count` (json), `conclusions` (json), `summary_table` (json)
- Params:
  - `anchor_counts` (array, default `[0, 3, 10, 20]`) — List of anchor counts to evaluate
  - `n_structured` (integer, default `3`) — Structured Sets per Count
  - `n_random` (integer, default `5`) — Random Sets per Count
  - `n_seeds_base` (integer, default `5`) — Seeds at 0 Anchors
  - `n_seeds_struct` (integer, default `3`) — Seeds per Structured Run
  - `n_seeds_rand` (integer, default `2`) — Seeds per Random Run
  - `sa_iterations` (integer, default `2000`) — SA Iterations
  - `sa_restarts` (integer, default `1`) — SA Restarts
  - `use_word_final_anchors` (boolean, default `false`) — Rank anchor candidates by word-final T-rate (Dr. Fuls 2026). Word-final signs have lower positional entropy — better anchors.

**`AnchorGenerator` — Anchor Generator**

Select the top-k most frequent signs as anchor candidates for decipherment. Returns the list of sign IDs to anchor; pair with known values in params or via AI.

- Inputs: `freq_map` (freq_map), `lm` (any)
- Outputs: `anchor_signs` (json), `n_anchors` (number)
- Params:
  - `n_anchors` (integer, default `5`) — Number of Anchors
  - `strategy` (string, default `"frequency"`) — frequency: top-N by occurrence count (recommended starting point)

**`AnchorSetLoader` — Anchor Set Loader**

Load a user-defined anchor set from the database (H16). Anchor sets are created in the Anchor Set Editor (Corpora tab). Returns {cipher_sign: target_value} dict compatible with SADecipher and AnchorConvergenceBenchmark.

- Inputs: none
- Outputs: `anchors` (json), `n_anchors` (number), `anchor_set_name` (text), `pairs` (json)
- Params:
  - `anchor_set_id` (string) — ID of an anchor set created in the Anchor Set Editor.

**`AssociationAnchorDeriver` — Association Anchor Deriver**

Derive a sign->value anchor dict from sign-context associations (Spec 087 S3): associations are sorted by descending pmi_z and each sign's first association at or above min_z binds it to anchor_prefix + context, up to max_anchors. The prefix is a parameter — a caller's context-label convention (e.g. 'ctx:') is data, not mechanism. The Phase-14 DerivedAnchorSet delegates to this engine.

- Inputs: `associations` (json, required)
- Outputs: `anchors` (json), `n_anchors` (number), `anchor_table` (json), `verdict` (text)
- Params:
  - `min_z` (number, default `2.0`) — Min Z
  - `max_anchors` (integer, default `25`) — Max Anchors
  - `anchor_prefix` (string, default `""`) — Anchor Prefix

**`BeamDecipher` — Beam Search Decipherment**

Deterministic beam search mapping inference. Faster than SA for small corpora. Systematically explores top beam_width partial mappings at each depth. Connects: CorpusReader → sequences, LMBuilder/BuiltinLM → lm.

- Inputs: `sequences` (sequences, required), `lm` (any, required), `anchors` (any)
- Outputs: `proposed_mapping` (json), `score` (number), `n_signs` (number)
- Params:
  - `beam_width` (integer, default `200`) — Beam Width
  - `surjective` (boolean, default `true`) — Surjective

**`BenchmarkScorer` — Benchmark Scorer**

Score a proposed sign mapping against a known answer key. Reports top-1 accuracy. Connects: SADecipher.proposed_mapping → proposed_mapping. Supply answer_key as a JSON dict param (cipher_sign: target_sign).

- Inputs: `proposed_mapping` (json, required), `answer_key` (json)
- Outputs: `correct` (number), `total` (number), `accuracy` (number)
- Params:
  - `answer_key` (string) — JSON dict mapping cipher sign → correct target sign. Leave blank to connect AnswerKey node.

**`BuiltinLM` — Built-in Reference LM**

Load a pre-built language model for a known language (hebrew, geez, phoenician, sumerian, dravidian, south_dravidian, kannada, telugu, pali, sanskrit, coptic, linear_b, meroitic, proto_sinaitic, nw_semitic). Use as the target LM in SADecipher or BeamDecipher.

- Inputs: none
- Outputs: `lm` (any), `language` (text), `n_signs` (number), `n_tokens` (number)
- Params:
  - `language` (string, default `"hebrew"`) — hebrew | geez | phoenician | sumerian | dravidian | south_dravidian | kannada | telugu | pali | sanskrit | coptic | linear_b | meroitic | proto_sinaitic | nw_semitic

**`CipherConstructor` — Cipher Constructor**

Create a bijective random substitution cipher from the LM sign inventory. Shuffles the sign-to-sign mapping deterministically and applies it to test sequences. Returns cipher_sequences, true_mapping (cipher→original), and sign_inventory. Pair with AnchorConvergenceBenchmark for controlled self-test experiments.

- Inputs: `sequences` (sequences, required), `lm` (any, required)
- Outputs: `cipher_sequences` (sequences), `true_mapping` (json), `perm` (json), `sign_inventory` (json), `inventory_size` (number), `n_cipher_tokens` (number)
- Params:
  - `cipher_seed` (integer, default `42`) — Random seed for the bijective shuffle (42 = default reproducible)
  - `max_tokens` (integer, default `15000`) — Truncate cipher sequences at this token count

**`ConsistencyScorer` — Consistency Scorer**

Aggregate multiple SA seed mappings into per-sign consistency statistics. Connects: SADecipher.all_mappings → all_mappings.

- Inputs: `all_mappings` (any), `proposed_mapping` (json)
- Outputs: `consistency_per_sign` (json), `mean_consistency` (number), `hci_count` (number), `hci_pct` (number)
- Params: none

**`ConstraintSweep` — Constraint Sweep**

Run SA decipherment across multiple anchor counts and return a consistency curve. Shows how solution space narrows as more correct sign values are provided. Connects: CorpusSplitter.test_sequences → sequences, LMBuilder → lm.

- Inputs: `sequences` (sequences, required), `lm` (any, required)
- Outputs: `consistency_curve` (json), `n_curve_points` (number)
- Params:
  - `anchor_counts` (array, default `[0, 1, 3, 5, 10]`) — Anchor Counts
  - `n_seeds` (integer, default `3`) — Seeds per Count
  - `max_iterations` (integer, default `3000`) — Max SA Iterations
  - `restarts` (integer, default `3`) — Restarts

**`CorpusLM` — Corpus Language Model**

Build a language model from any corpus already uploaded to the database (H16). Users add languages via the Corpora tab — no Python data file required. Preferred over BuiltinLM for user-defined and project-specific languages.

- Inputs: none
- Outputs: `lm` (any), `corpus_name` (text), `n_signs` (number), `n_tokens` (number), `h1` (number)
- Params:
  - `corpus_id` (string) — Select from the Corpora tab. Any uploaded corpus works as an LM source.
  - `min_freq` (integer, default `1`) — Drop signs that appear fewer than this many times.

**`IconographicAnchorScorer` — Iconographic Anchor Scorer**

Score iconographic anchors against a sign->phoneme map (Spec 087 S3): each anchor's iconic reading is matched against the map through an ordered reading->alias table carried as data; matches score by anchor-confidence weights with a high-confidence bonus. With an extension bonus set, the allograph mode credits family members carrying the family's phoneme. The Phase-27 IconographicAnchorScore and the Phase-28 AllographAwareIconographicScore delegate to this engine.

- Inputs: `iconographic_anchors` (json, required), `phoneme_map` (json, required), `allograph_families` (json)
- Outputs: `n_total_anchors` (number), `n_matches` (number), `n_allograph_extensions` (number), `extended_sign_ids` (json), `total_score` (number), `rows` (json), `verdict` (text)
- Params:
  - `scorer_spec` (object) — Alias table (ordered [key, [aliases], family] entries), confidence weights, high-confidence bonus, optional allograph extension bonus, empty result, verdict template.

**`LMBuilder` — Language Model Builder**

Build a statistical language model (unigram+bigram+positional) from sequences. Output 'lm' passes to SADecipher or BeamDecipher.

- Inputs: `sequences` (sequences, required)
- Outputs: `lm` (any), `n_signs` (number), `n_tokens` (number), `h1` (number)
- Params: none

**`LengthMatchPermutationTest` — Length Match Permutation Test**

Permutation test of name-length <-> seal-length matching (Spec 087 S3): the statistic is the per-name best length score summed (null: shuffle the seal lengths) or the greedy bipartite assignment sum (null: random one-to-one assignments). Verdict bands, the insufficient-data verdict, the optional observed-assignment output, and the interpretation are spec data. The Phase-23 BilingualReadoutTest and the Phase-24 BilingualReadoutTestV2 delegate to this engine.

- Inputs: `rows_all` (json, required), `inscribed_seals` (json, required)
- Outputs: `verdict` (text), `p_value` (number), `observed` (number), `null_mean` (number), `null_sd` (number), `z_score` (number), `n_permutations` (number), `n_candidates` (number), `n_seals` (number), `observed_assignment` (json), `interpretation` (text)
- Params:
  - `n_permutations` (integer, default `1000`) — Permutations
  - `min_name_freq` (integer, default `2`) — Min Name Frequency
  - `tolerance` (integer, default `2`) — Tolerance
  - `seed` (integer, default `42`) — Seed
  - `test_spec` (object) — Statistic (best_match or bipartite), defaults, insufficient verdict, verdict bands, assignment output flag, interpretation.

**`LengthMatchScorer` — Length Match Scorer**

Score candidate-name <-> seal pairings by length compatibility (Spec 087 S3): hyphen-segment counts against inscription lengths under a named score spec — the family tolerance falloff or a named divergent linear falloff carried as data, never silently re-shaped. Assignment modes: all-pairs with a best pairing per name, greedy one-to-one bipartite, or pairings aggregated from raw person rows against sign-bearing seals. The Phase-23 EnhancedNameMatcher, the Phase-24 EnhancedNameMatcherV2, and the Phase-22 MeluhhaNameMatcher delegate to this engine.

- Inputs: `rows_all` (json, required), `inscribed_seals` (json, required), `persons` (json), `seals_at_mesopotamia` (json)
- Outputs: `n_candidates` (number), `n_seals` (number), `n_seals_with_signs` (number), `n_seals_total` (number), `n_assigned` (number), `n_unassigned` (number), `pairings` (json), `pairings_top50` (json), `n_pairings` (number), `best_per_name` (json), `total_length_score` (number), `verdict` (text)
- Params:
  - `min_name_freq` (integer, default `2`) — Min Name Frequency
  - `tolerance` (integer, default `2`) — Tolerance
  - `matcher_spec` (object) — Assignment mode, score spec (kind tolerance or a named linear falloff), min-frequency default, verdict/insufficient/no-signs templates.

**`PhonemeMapCoverage` — Phoneme Map Coverage**

Apply a phoneme map to inscribed seals and report readability (Spec 087 S3): a seal is readable when at least one real (non-placeholder) sign resolves to a phoneme that is neither the unknown token nor marked uncertain; per-seal skeletons and high-confidence counts are reported. The unknown token, the uncertain marker, and the verdict text are spec data. The Phase-25 BlindHeldOutTest delegates to this engine.

- Inputs: `inscribed_seals` (json, required), `phoneme_map` (json, required)
- Outputs: `n_seals` (number), `n_readable` (number), `n_high_conf` (number), `rows` (json), `verdict` (text)
- Params:
  - `coverage_spec` (object) — Unknown token, uncertain marker, high-confidence label, placeholder skeleton, verdict template.

**`ReverseSkeletonSearch` — Reverse Skeleton Search**

Score candidate names against a predicted phonetic skeleton (Spec 087 S3): one shared scoring core — target segment positions and length, length/position/free weights — carried as spec data, over three candidate modes: aggregated person rows matched by substring against the rendering set (with a suffix-penalty set as data), ePSD2-style name entries scored over their alternate forms by exact rendering-token match, and that mode binned by best-form segment count over a cohort table with a concentration verdict. The rendering set is data, with an optional dynamic expansion from the phoneme map via a named allograph family. The Phase-27 ReverseJanabiyahSearch, the Phase-28 ReverseJanabiyahSearchV2, the Phase-29 M77ReverseJanabiyahSearchV3, and the Phase-30 LengthCohortReverseJanabiyahSearch delegate to this engine.

- Inputs: `persons_v3` (json), `epsd2_personal_names` (json), `janabiyah_reading` (json, required), `phoneme_map` (json), `allograph_families` (json)
- Outputs: `n_candidates` (number), `n_pns_searched` (number), `n_renderings` (number), `n_with_position_match` (number), `n_with_free_miin` (number), `top_matches` (json), `n_cohorts` (number), `n_with_position_match_total` (number), `n_with_free_miin_total` (number), `cohorts` (json), `verdict` (text)
- Params:
  - `top_k` (integer, default `20`) — Top K
  - `min_icount` (integer, default `1`) — Min Instance Count
  - `cohorts` (array, default `[[3, 4], [5, 6], [7, 8], [9, 99]]`) — [lo, hi] segment-count cohort pairs for the pn_cohorts mode.
  - `search_spec` (object) — Candidate mode, scoring core (target positions/length, weights), rendering set + optional expansion, penalty suffixes, cohort default + concentration factor, output plan, empty result, verdict templates.

**`SADecipher` — SA Decipherment**

Simulated Annealing mapping inference. Runs N seeds in parallel via ThreadPoolExecutor. GPU-accelerated when CuPy is installed (ocp_weight=0 enables BigramScorer GPU path). Connects: CorpusReader/CorpusSplitter → sequences, LMBuilder/BuiltinLM → lm.

- Inputs: `sequences` (sequences, required), `lm` (any, required), `anchors` (any)
- Outputs: `proposed_mapping` (json), `all_mappings` (any), `mean_consistency` (number), `hci_count` (number)
- Params:
  - `n_seeds` (integer, default `5`) — Number of Seeds
  - `max_iterations` (integer, default `10000`) — Max Iterations
  - `restarts` (integer, default `8`) — Restarts per Seed
  - `surjective` (boolean, default `true`) — True: many cipher signs → fewer target signs (cross-language). False: bijective.
  - `ocp_weight` (number, default `0.0`) — 0.0 = GPU fast path via BigramScorer (recommended). >0 = enable OCP penalty (slower).

**`SAMultiComparison` — SA Multi-Language Comparison**

Run Simulated Annealing against multiple reference language models and rank by consistency. Specify 2–6 languages in the 'languages' param (comma-separated). Each language runs independently; results are sorted best→worst by mean_consistency. Connects: BuiltinCorpus/CorpusReader → sequences. No external LM port needed.

- Inputs: `sequences` (sequences, required), `anchors` (any)
- Outputs: `comparison_results` (json), `best_language` (text), `best_consistency` (number), `ranking` (json)
- Params:
  - `languages` (string, default `"dravidian,sanskrit"`) — Comma-separated list of languages to compare. Valid: hebrew, geez, phoenician, sumerian, dravidian, south_dravidian, kannada, telugu, pali, sanskrit, coptic, linear_b, meroitic, proto_sinaitic
  - `n_seeds` (integer, default `3`) — Seeds per Language
  - `max_iterations` (integer, default `5000`) — Max Iterations
  - `restarts` (integer, default `5`) — Restarts per Seed

**`SkeletonTabletSearch` — Skeleton Tablet Search**

Predict a seal reading's phonetic skeleton under a sign->phoneme map and scan tablet lines for syllable-rendering matches (Spec 087 S3): each scan in the carried scan list searches the gated tablets' lines for lines hitting at least the minimum number of renderings, where a scan's rendering list is a spec constant or arrives through an input port; the keyword gate, the hit rule, and the verdict text are spec data. The Phase-25 JanabiyahPhoneticReadout and the Phase-26 JanabiyahPhoneticReadoutV2 delegate to this engine.

- Inputs: `janabiyah_reading` (json, required), `phoneme_map` (json, required), `tablets` (json, required), `miin_renderings` (json), `miin_renderings_direct_only` (json)
- Outputs: `skeleton` (text), `predictions` (json), `n_miin` (number), `n_signs` (number), `matches_top20` (json), `n_matches` (number), `matches_direct_top20` (json), `n_matches_direct` (number), `matches_expanded_top20` (json), `n_matches_expanded` (number), `n_new_matches_from_translation` (number), `miin_renderings_searched` (json), `verdict` (text), `interpretation` (text)
- Params:
  - `readout_spec` (object) — Scan list (rendering source per scan: spec constant or input port; hit key and output keys per scan), keyword gate, minimum hits, line limit, optional derived count, echoed renderings, error result, verdict template, optional interpretation.

**`StratifiedPermutationTest` — Stratified Permutation Test**

Run the bipartite length-match readout test per stratum plus a merged overall (Spec 087 S3): persons are aggregated by candidate name within strata assigned by an ordered substring->bucket rule table carried as data (case sensitivity, value stripping, and the empty/fallback buckets included), each stratum's permutation seed is a base plus the bucket name's length, and strata with fewer than two distinct candidates are skipped. The Phase-25 PeriodStratifiedReadout, the Phase-27 PeriodStratifiedReadout6Bucket, and the Phase-26 ProvenienceStratifiedReadout delegate to this engine.

- Inputs: `persons_v3` (json, required), `inscribed_seals` (json, required)
- Outputs: `results` (json), `n_significant_strata` (number), `verdict` (text)
- Params:
  - `n_permutations` (integer, default `1000`) — Permutations
  - `tolerance` (integer, default `2`) — Tolerance
  - `strata_spec` (object) — Stratum field, result axis key, ordered [bucket, [keys]] rules, case sensitivity, strip flag, empty/fallback buckets, seed base, verdict template.

#### Evidence Graph

**`CrossHypothesisMatrix` — Cross-Hypothesis Matrix**

Group claims by sign or type and compute agree/conflict/untested verdicts.

- Inputs: `claims` (claims, required)
- Outputs: `matrix` (json), `n_conflicts` (number), `json` (json), `text` (text)
- Params:
  - `group_by` (string, default `"sign"`) — 'sign' groups by signs_involved; 'claim_type' groups by claim type.

**`HiddenHypothesisGen` — Hidden Hypothesis Generator**

Derive compound testable hypotheses from cross-paper claim intersections.

- Inputs: `claims` (claims, required), `matrix` (json)
- Outputs: `hypotheses` (json), `total_hypotheses` (number), `json` (json), `text` (text)
- Params:
  - `min_sources_per_hypothesis` (integer, default `2`) — Minimum number of distinct papers a hypothesis must draw from.

#### Experiments

**`ExperimentInput` — Experiment Input Port**

Declare a named input port for this experiment graph. When invoked via SubExperiment, the caller injects a value matched by port_name. Use as subroutine parameters.

- Inputs: none
- Outputs: `value` (any), `port_name` (text)
- Params:
  - `port_name` (string, default `"input"`) — Unique name for this input port (matched by the calling SubExperiment node)
  - `default_value` (string, default `""`) — Used when not called as a sub-experiment

**`ExperimentWrapper` — Experiment**

Run any registered ExperimentBase subclass with upstream inputs merged as kwargs.

- Inputs: `upstream` (any)
- Outputs: `result` (json)
- Params:
  - `experiment_id` (string) — ID of the registered experiment to run (e.g. positional_profile_analysis).
  - `corpus_id` (string) — Optional corpus override for experiments that accept corpus_id.

**`LegacyPhaseScriptRunner` — Legacy Phase Script Runner**

Subprocess-run a pre-WARP.md analysis script under `scripts/phase{N}/` and parse its produced JSON output. Used by retroactive Phase-16/17/18/19 graph migrations to make legacy analyses re-runnable + visible in the Jobs panel without rewriting their internals.

- Inputs: none
- Outputs: `script_path` (text), `output_path` (text), `output_size_bytes` (number), `output_present` (any), `exit_code` (number), `stdout_tail` (text), `stderr_tail` (text), `json_snippet` (json), `verdict` (text)
- Params:
  - `script_path` (string, default `""`) — Repo-relative path of the .py script (e.g. scripts/phase19/omnibus.py).
  - `output_path` (string, default `""`) — Repo-relative path of the JSON file the script writes (e.g. reports/phase19_omnibus.json).
  - `timeout_s` (integer, default `1200`) — Subprocess timeout in seconds.

**`SubExperiment` — Sub-Experiment**

Invoke a graph experiment as a reusable subroutine. Injects caller inputs through ExperimentInput nodes (matched by port_name) and exposes ExperimentOutput values as named ports. Implements the Study → Experiment → Atomic Node hierarchy.

- Inputs: `a` (any), `b` (any), `c` (any)
- Outputs: `result` (json), `conclusions` (json)
- Params:
  - `experiment_id` (string) — ID of the graph experiment to invoke as a subroutine

#### Outputs

**`ExperimentOutput` — Experiment Output Port**

Declare a named output port for this experiment graph. Exposes upstream data under port_name so a calling Study or Experiment can wire the result. Multiple ExperimentOutput nodes can coexist in one graph.

- Inputs: `data` (any, required)
- Outputs: `value` (any), `port_name` (text)
- Params:
  - `port_name` (string, default `"output"`) — Unique name for this output port (visible to the calling graph)

**`JSONExport` — JSON Export**

Save result to a JSON file in reports/.

- Inputs: `data` (any, required)
- Outputs: `saved` (any), `path` (text)
- Params:
  - `filename` (string, default `"graph_experiment_output.json"`) — Filename

**`PassResult` — Pass Result**

Return all upstream inputs as the final experiment result (used in Study Builder).

- Inputs: `data` (any, required)
- Outputs: `result` (json)
- Params: none

**`ReportGenerator` — Report Generator**

Generate a structured report from a user-defined template (H16). Templates are created in the Report Template Editor (Reports tab). Connect upstream result nodes to match the template's data_key fields.

- Inputs: `data` (any)
- Outputs: `report` (json), `template_name` (text), `n_sections` (number)
- Params:
  - `template_id` (string) — ID of a template created in the Report Template Editor.

#### Phase-14 / Structural

**`BlockEntropyProfile` — Block Entropy Profile (Phase-14)**

Compute H(n) for n=1..max_n on the input sequences. Plain MLE estimator. Output is the language-vs-non-language fingerprint (Rao 2009).

- Inputs: `sequences` (sequences, required)
- Outputs: `label` (text), `alphabet_size` (number), `n_tokens` (number), `block_entropies` (json), `json` (json)
- Params:
  - `max_n` (integer, default `6`)
  - `label` (string, default `"unknown"`)

**`ConditionalEntropyProfile` — Conditional Entropy Profile (Phase-14)**

h(n) = H(n) - H(n-1). A natural language plateaus at finite n; non-language is flat or rapidly decaying.

- Inputs: `block_entropies` (json, required)
- Outputs: `label` (text), `conditional_entropies` (json), `plateau` (text), `verdict` (text), `json` (json)
- Params: none

**`MutualInformationDecay` — Mutual Information Decay (Phase-14)**

I(X_t; X_{t+k}) for k=1..max_k. Power-law decay = natural language; exponential decay = Markov-1; flat = unigram-random.

- Inputs: `sequences` (sequences, required)
- Outputs: `label` (text), `decay` (json), `regime` (text), `gamma_powerlaw` (number), `lambda_exponential` (number), `r2_powerlaw` (number), `r2_exponential` (number), `h1_nats` (number), `verdict` (text), `json` (json)
- Params:
  - `max_k` (integer, default `8`)
  - `label` (string, default `"unknown"`)

**`ReferenceCorpusLoader` — Reference Corpus Loader (Phase-14)**

Emit raw sequences for any supported reference language. Mirrors BuiltinLM's language list. Used for Path-1 cross-corpus comparison.

- Inputs: none
- Outputs: `sequences` (sequences), `language` (text), `label` (text), `n_sequences` (number), `n_tokens` (number), `distinct_symbols` (number)
- Params:
  - `language` (string, default `"linear_b"`)
  - `label` (string, default `"linear_b"`)

**`ZipfMandelbrotFit` — Zipf-Mandelbrot Fit (Phase-14)**

Fit f(r) = C / (r + beta)^alpha via 2D grid search. Natural language: alpha approx 1, finite beta. Random: alpha approx 0.

- Inputs: `freq_map` (freq_map), `sequences` (sequences)
- Outputs: `label` (text), `alpha` (number), `beta` (number), `r_squared` (number), `verdict` (text), `json` (json)
- Params:
  - `label` (string, default `"unknown"`)

#### Phase-15 / Hypothesis comparison

**`MultiHypothesisRanker` — Multi-Hypothesis Ranker (Phase-15 step 3)**

Take up to 6 hypothesis projection outputs (each a different language hypothesis) and rank by max_violation. Lowest violation wins. Returns winner, runner-up, and confidence text.

- Inputs: `a` (json), `b` (json), `c` (json), `d` (json), `e` (json), `f` (json)
- Outputs: `ranked` (json), `winner` (text), `winner_max_violation` (number), `runner_up` (text), `spread` (number), `confidence_text` (text), `verdict` (text), `json` (json)
- Params:
  - `labels` (array, default `[]`)

#### Phase-15 / Long-tail

**`LongTailFilter` — Long-Tail Filter (Phase-15)**

Filter a corpus to inscriptions of length >= min_length (default 7). Used to isolate the long-tail subset from a corpus dominated by short inscriptions, so MI decay and HED can be re-measured on samples where long-range correlations have room to fit.

- Inputs: `sequences` (sequences, required)
- Outputs: `sequences` (sequences), `label` (text), `n_input` (number), `n_kept` (number), `n_dropped_short` (number), `n_dropped_long` (number), `share_kept` (number), `n_tokens_kept` (number), `distinct_symbols_kept` (number), `verdict` (text), `min_length` (number), `max_length` (number)
- Params:
  - `min_length` (integer, default `7`)
  - `max_length` (integer, default `0`)
  - `label` (string, default `"long_tail"`)

**`LongTailVerdict` — Long-Tail Verdict (Phase-15 step 1)**

Combines full-corpus + long-tail MI decay with long-tail HED into a four-way verdict: TRUNCATION_ARTIFACT_WINS, POWERLAW_BOTH, HERALDIC_WINS, INSUFFICIENT_DATA, AMBIGUOUS. Tells you whether Phase-14's exponential MI-decay finding survives length filtering.

- Inputs: `mi_decay_full` (json, required), `mi_decay_long` (json, required), `hed_long` (json, required), `zipf_long` (json), `conditional_entropy_long` (json), `filter_summary` (json)
- Outputs: `verdict_class` (text), `verdict` (text), `mi_full_regime` (text), `mi_long_regime` (text), `mi_full_gamma` (number), `mi_long_gamma` (number), `mi_full_lambda` (number), `mi_long_lambda` (number), `hed_long_regime` (text), `n_long_tail_inscriptions` (number), `n_long_tail_tokens` (number), `next_step` (text), `json` (json)
- Params: none

#### Phase-15 / Validation

**`CipherSelfTestRunner` — Cipher Self-Test (Phase-15 step 2)**

Build a known random cipher on a reference corpus, run two SA decipherments (frequency anchors vs epistatic anchors), and score top-1 accuracy. Targets >=95 percent with epistatic anchors. Use to validate the framework on a known-decoded script before applying to Indus.

- Inputs: `sequences` (sequences, required)
- Outputs: `label` (text), `n_inv` (number), `n_anchors` (number), `freq_metrics` (json), `epi_metrics` (json), `delta_top1_all` (number), `delta_top1_free` (number), `verdict` (text), `epistatic_anchor_signs` (json), `frequency_anchor_signs` (json), `json` (json)
- Params:
  - `cipher_seed` (integer, default `42`)
  - `n_anchors` (integer, default `10`)
  - `max_iterations` (integer, default `3000`)
  - `restarts` (integer, default `2`)
  - `label` (string, default `"self_test"`)

#### Phase-16 / Decipherment

**`DecipheredMappingExporter` — Deciphered Mapping Exporter (Phase-16)**

Take a proposed_mapping + epistatic_ranking + winning_hypothesis and emit a structured per-sign decipherment table with confidence categories (anchored / high_centrality / medium / low). The headline output of the Phase-16 decipherment attempt.

- Inputs: `proposed_mapping` (json, required), `anchors` (json), `epistatic_ranking` (json), `winning_hypothesis` (text)
- Outputs: `winning_hypothesis` (text), `table` (json), `n_signs_total` (number), `n_anchored` (number), `n_high_centrality` (number), `n_medium_centrality` (number), `verdict` (text), `json` (json)
- Params:
  - `winning_hypothesis` (string, default `"unknown"`)

#### Phase-20 / Sign clustering

**`AllographDetector` — Allograph Detector (Phase-20)**

Daggumati-style distributional clustering of signs by bigram-context cosine + position-distribution L1 distance.

- Inputs: `sequences` (sequences, required)
- Outputs: `clusters` (json), `biggest_cluster` (json), `sign_to_cluster` (json), `n_signs_total` (number), `n_signs_eligible` (number), `n_clusters` (number), `n_signs_in_multi_clusters` (number)
- Params:
  - `min_count` (integer, default `5`)
  - `cos_threshold` (number, default `0.55`)
  - `pos_threshold` (number, default `0.5`)

#### Phase-20 / Spectral

**`BinSpectralFingerprint` — Bin Spectral Fingerprint (Phase-20)**

Compute the bigram-transition spectral gap and top eigenvalues per length-stratification bin. Tests Phase-19 prediction 1 (M77's anomalously small spectral gap is dominated by short inscriptions).

- Inputs: `stratifications` (json, required)
- Outputs: `per_bin` (json), `verdict` (text), `n_bins_with_data` (number)
- Params: none

#### Phase-20 / Transforms

**`LengthStratifier` — Length Stratifier (Phase-20)**

Bin sequences into length-based strata. Output a `stratifications` dict bin_label -> sequences for downstream per-bin analysis.

- Inputs: `sequences` (sequences, required)
- Outputs: `stratifications` (json), `summary` (json), `n_bins` (number), `total_sequences` (number)
- Params:
  - `bins` (array, default `[[1, 2], [3, 4], [5, 6], [7, 9999]]`)

#### Phase-21 / Numerical

**`NumericalWeightAnalyzer` — Numerical Weight Analyzer (Phase-21)**

For NUMERICAL-classed M77 signs, collect repetition-block lengths conditioned on site group and inscription-length bin. Reports mean / std / CV per sign and classifies each sign's block-length distribution as poisson_count, low_variance_doubling, or high_variance_count.

- Inputs: `inscriptions` (json, required), `table` (json)
- Outputs: `n_signs_analysed` (number), `n_poisson_regime` (number), `n_low_variance_doubling` (number), `n_high_variance_count` (number), `rows` (json), `verdict` (text)
- Params:
  - `rep_rate_min` (number, default `0.4`) — Minimum repetition rate for sign inclusion.
  - `min_block_count` (integer, default `5`)
  - `length_bins` (array, default `[[1, 4], [5, 8], [9, 9999]]`)

#### Phase-21 / Reporters

**`PerStratumSummary` — Per-Stratum Summary (Phase-21)**

Compactly summarise a BinSpectralFingerprint output as a list of {stratum, n_seqs, n_tokens, spectral_gap, verdict} rows with a corpus-level verdict on whether strata differ.

- Inputs: `per_bin` (json, required)
- Outputs: `rows` (json), `verdict` (text), `n_strata` (number)
- Params: none

#### Phase-21 / Transforms

**`RepetitionCollapser` — Repetition Collapser (Phase-21)**

Collapse runs of identical consecutive signs into a single occurrence (e.g. 'A B B B C' → 'A B C'). Outputs both the original and collapsed corpus as a stratifications dict that BinSpectralFingerprint can consume directly. Tests Phase-20 finding 4 (de-numerify the corpus and recheck spectral gap).

- Inputs: `sequences` (sequences), `inscriptions` (json)
- Outputs: `stratifications` (json), `collapsed_sequences` (sequences), `collapsed_inscriptions` (json), `n_runs_collapsed` (number), `n_tokens_dropped` (number), `share_kept` (number), `collapse_stats` (json)
- Params:
  - `min_run` (integer, default `2`) — Minimum consecutive same-sign run to collapse.

**`SiteStratifier` — Site Stratifier (Phase-21)**

Group inscriptions by Mahadevan site_code prefix (first two digits, e.g. 100000 = Mohenjo-daro, 200000 = Harappa, 510000 = Banawali/Rakhigarhi). Output stratifications match the LengthStratifier shape so BinSpectralFingerprint and AllographDetector can be composed against site groups.

- Inputs: `inscriptions` (json, required)
- Outputs: `stratifications` (json), `inscription_strata` (json), `summary` (json), `n_groups` (number), `total_sequences` (number)
- Params:
  - `min_inscriptions` (integer, default `30`) — Site groups smaller than this go into the 'Other' bucket.
  - `top_n` (integer, default `0`) — 0 = no limit; if > 0, keep only the N largest site groups.
  - `site_labels` (object, default `{}`) — Optional prefix→human-label map.

#### Phase-30 / Spectral

**`ShufflePermutationNull` — Shuffle Permutation Null Spectral Test (Phase-30c)**

Per-bin permutation null on bigram-transition spectral gaps. For each length bin, resamples the flat token bag into pseudo-sequences matching the original length profile, computes the null spectral gap N times, and reports the one-sided p-value P(null >= observed).

- Inputs: `stratifications` (json, required)
- Outputs: `per_bin` (json), `n_bins` (number), `n_significant` (number), `n_with_data` (number), `verdict` (text)
- Params:
  - `n_permutations` (integer, default `200`)
  - `seed` (integer, default `42`)

#### Phase-30 / Statistical Validation

**`PermutationTest` — Permutation Statistical Test (Phase-30 A1)**

Computes a one-sided permutation p-value for an observed score against a random null distribution. Used for Phase-30 A1 validation of the Enmenanak finding (Phase-29d score=7.0 vs null).

- Inputs: `observed_score` (number), `enmenanak_score` (number), `top_candidates` (json)
- Outputs: `observed_score` (number), `p_value` (number), `percentile_rank` (number), `null_95th` (number), `verdict` (text)
- Params:
  - `n_permutations` (integer, default `1000`)
  - `max_score` (integer, default `10`) — Maximum possible score value
  - `result_file` (string, default `""`) — Path to Phase-29d result JSON (optional)
  - `seed` (integer, default `42`)

#### Research

**`ResearchLoopRunner` — Research Loop Runner**

Run the Mine→Analyze→Register→Execute→Analyze cycle for N iterations.

- Inputs: none
- Outputs: `total_papers` (number), `total_insights` (number), `json` (json), `text` (text)
- Params:
  - `max_cycles` (integer, default `5`) — Number of Mine→Execute cycles to run.

#### Sources

**`AnchorSyllabifier` — Anchor Syllabifier**

Load an anchor file and map each reading to a syllable token (Spec 087 S3): strip the transliteration (diacritic) table, take a direct syllable-vocab hit when one exists, else split into CV chunks and use the first chunk in the vocab, with prefix-length fallbacks. File paths, the confidence order, the diacritic table, and the positional-label skip pattern are parameters/data. The Phase-33 IndusAnchorSetSyllable delegates to this engine.

- Inputs: none
- Outputs: `anchor_dict` (json), `n_anchors` (number), `n_skipped` (number), `verdict` (text)
- Params:
  - `anchors_path` (string) — Anchor JSON file: {anchors: {sign_id: {reading, confidence}}}
  - `vocab_path` (string) — JSON file holding the syllable vocab list.
  - `min_confidence` (string, default `"MEDIUM"`) — Min Confidence
  - `confidence_order` (object) — Confidence label -> rank. Default HIGH 3, MEDIUM 2, LOW 1, UNCERTAIN 0.
  - `diacritic_table` (array, default `[]`) — Ordered [source, replacement] string pairs applied after lowercasing.
  - `skip_pattern` (string) — Regex matched at the start of a lowercased reading; matches are skipped (positional labels).

**`BuiltinCorpus` — Built-in Corpus**

Load a named built-in corpus directly. Does not require a DB corpus ID — always available offline.

- Inputs: none
- Outputs: `sequences` (sequences), `total_tokens` (number), `distinct_symbols` (number)
- Params:
  - `corpus` (string, default `"indus"`) — indus | indus_cisi (CISI real multi-sign) | hebrew | geez | phoenician | nw_semitic (Fuls RTL)

**`CorpusReader` — Corpus Reader**

Load sequences from a corpus (falls back to ICIT Indus corpus if no ID).

- Inputs: none
- Outputs: `sequences` (sequences), `total_sequences` (number), `total_tokens` (number)
- Params:
  - `corpus_id` (string) — UUID from Corpora tab. Leave blank for default ICIT corpus.

**`DatasetRecordLoader` — Dataset Record Loader**

Load records from a bundled data module (glossa_lab.data.*) via a declarative spec (Spec 087 S3): named getters with parameterised kwargs, record filters, and an ordered output assembly (values, counts, top-N counters, verdict templates). Dataset identity, getter names, and verdict text are parameters (dataset_spec), not code — the domain loaders (Mahadevan, ePSD2, Contact Corpus) delegate to this engine.

- Inputs: none
- Outputs: `records` (json), `n_records` (number), `metadata` (json), `verdict` (text)
- Params:
  - `module` (string) — Dotted path of a glossa_lab.data module.
  - `dataset_spec` (object) — Full declarative spec: module, getters, filters, outputs.

**`JsonCorpusLoader` — JSON Corpus Loader**

Load a sign-sequence corpus from a JSON file via a declarative source spec (Spec 087 S3): a fallback chain of file sources (JSON record files, or a grouped-CSV fallback), a field map, and length filters, projected as sequences + per-inscription metadata + counts. Corpus identity, paths, and field names are parameters (corpus_spec), not code — the domain loaders (M77, ICIT, Mathematica Epigraphica) delegate to this engine.

- Inputs: none
- Outputs: `sequences` (sequences), `inscriptions` (json), `n_inscriptions` (number), `n_tokens` (number), `n_distinct_signs` (number), `label` (text), `source` (text), `available` (any), `verdict` (text)
- Params:
  - `data_path` (string) — JSON corpus file (single-source use; see corpus_spec for chains).
  - `records_key` (string, default `"inscriptions"`) — Records Key
  - `projection` (string, default `"sequence_corpus"`) — sequence_corpus | record_list | cache_summary.
  - `use_raw` (boolean, default `false`) — Use Raw
  - `min_length` (integer, default `1`) — Min Length
  - `max_length` (integer, default `0`) — 0 = no upper bound.
  - `label` (string, default `"corpus"`) — Label
  - `corpus_spec` (object) — Full declarative spec: sources, field_map, absent_result, verdict_template.

**`JsonRecordDirLoader` — JSON Record Directory Loader**

Load a directory of one-JSON-record-per-file documents (Spec 087 S3): search mode projects each parseable record through a field map with an optional substring query and a cross-reference count from a sibling directory; records mode flattens the item lists of every parseable file (optionally restricted to files named by an upstream input) under param-driven filters, per-field value counts, and a cap. Paths, field names, filters, and text are parameters (loader_spec), not code — the Indus evidence loaders delegate to this engine.

- Inputs: `papers` (papers)
- Outputs: `papers` (papers), `claims` (claims), `total_papers` (number), `total_claims` (number), `source_docs` (number), `type_counts` (json), `status_counts` (json), `json` (json), `text` (text)
- Params:
  - `query` (string, default `""`) — Search Query
  - `max_papers` (integer, default `200`) — Max Papers
  - `claim_type` (string, default `""`) — Claim Type Filter
  - `claim_status` (string, default `""`) — Claim Status Filter
  - `sign_filter` (string, default `""`) — Sign Filter
  - `max_claims` (integer, default `500`) — Max Claims
  - `loader_spec` (object) — Full declarative spec: mode, directory, projection / filters / counts, text templates.

**`PDFTextExtractor` — PDF Text Extractor (Phase-20)**

Extract text per page from a PDF using PyMuPDF.

- Inputs: `file_path` (any)
- Outputs: `pages` (json), `n_total_pages` (number), `n_pages_extracted` (number), `total_characters` (number), `file_path` (text)
- Params:
  - `file_path` (string, default `""`)
  - `max_pages` (integer, default `100`)
  - `start_page` (integer, default `0`)

**`RegistryTableLoader` — Registry Table Loader**

Load a registry table from the backend database via a declarative spec (Spec 087 S3): table name, parameter-driven filter clauses, id/uuid fields, and named filter-counts are parameters (registry_spec); the projection — records, total, counts, id->uuid map, id list — is the mechanism. Without a spec it uses the canonical-signs shape it was generalised from. The CGSA CanonicalSignLoader delegates to this engine.

- Inputs: none
- Outputs: `registry` (json), `n_signs` (number), `n_parpola` (number), `sign_ids` (json), `sign_id_to_uuid` (json)
- Params:
  - `table` (string) — Database table to load (single-table use; see registry_spec for the full spec).
  - `in_corpus_only` (boolean, default `true`) — In Corpus Only
  - `numbering_system` (string, default `""`) — Numbering System
  - `registry_spec` (object) — Full declarative spec: table, filters, id_field, uuid_field, count_filters, output key names.

**`StaticValue` — Static Value**

Emit a constant string, number, or JSON value as a node output.

- Inputs: none
- Outputs: `value` (any), `text` (text)
- Params:
  - `value` (string) — Value

**`SyllableLMLoader` — Syllable LM Loader**

Load a syllable-level language model from its JSON form (Spec 087 S3): stored bigram log-probs are exponentiated, unigram counts derive from bigram endpoints, and the ranked list orders the vocabulary by those counts, producing the LanguageModel the decipher pipeline consumes. The file path, language label and error text are parameters (lm_spec), not code — DravidianSyllableLM delegates to this engine.

- Inputs: none
- Outputs: `lm` (any), `language` (text), `n_bigrams` (number), `n_syllables` (number), `verdict` (text)
- Params:
  - `lm_path` (string, default `""`) — LM Path
  - `lm_spec` (object) — Base dir, default path, language, error text.

**`ValueRoleMapSource` — Value-Role Map Source**

Emit a value->role lookup table merged from a base map plus selected per-language family tables (Spec 087 S3). The base map and every family table (seed roles, base values, vocabulary sources, classification sets) are data parameters (base_map, family_tables); the merge order — base, families in the order named, then extra overrides — and unknown-family reporting are the mechanism. The CTT DefaultIndusValueRoleMap delegates to this engine with its Indus base map and family tables as data.

- Inputs: none
- Outputs: `value_role_map` (json), `n_values` (number), `families_applied` (json), `family_sizes` (json), `unknown_families` (json), `json` (json)
- Params:
  - `base_map` (object, default `{}`) — Base value->role map, included when include_default is true.
  - `family_tables` (object, default `{}`) — Map of family name -> family spec (seed_roles, base_values, vocab_sources, vocab_mode, determinative_values, numeral_values).
  - `families` (array, default `[]`) — Family names to merge in, in order. Unknown names are reported, not fatal.
  - `include_default` (boolean, default `true`) — Include Base Map
  - `extra` (object, default `{}`) — Extra Overrides

**`VisionOCRNode` — Vision OCR Node**

Vision-LLM OCR over PDF pages with a line-grammar parse (Spec 087 S3): a no-op by default (loads previously saved results and reports type counts); with run_ocr set, renders pages to PNG data URIs, calls the vision provider, parses transcripts against spec grammar rules, and writes results back. Prompt, grammar, paths and texts are parameters (ocr_spec), not code — CISIVol3OCRNode delegates to this engine.

- Inputs: none
- Outputs: `n_records` (number), `n_seal` (number), `n_iconography` (number), `n_sign_ref` (number), `records` (json), `verdict` (text)
- Params:
  - `run_ocr` (boolean, default `false`) — Run OCR
  - `pdf_path` (string, default `""`) — PDF Path
  - `pages` (array) — Pages
  - `prompt` (string, default `""`) — Prompt
  - `output_path` (string, default `""`) — Output Path
  - `ocr_spec` (object) — Base dir, default prompt/paths, grammar, templates.

#### Transforms

**`CorpusSplitter` — Corpus Splitter**

Split sequences into contiguous train and test portions. Use train for LMBuilder, test for SADecipher (no leakage).

- Inputs: `sequences` (sequences, required)
- Outputs: `train_sequences` (sequences), `test_sequences` (sequences), `train_n_tokens` (number), `test_n_tokens` (number)
- Params:
  - `train_ratio` (number, default `0.75`) — Fraction of sequences used for training (0.1–0.95)

**`DirectionNormalizer` — Direction Normalizer**

Detect or force reading direction (LTR/RTL) and reverse sequences accordingly. 'auto' uses the Ashraf & Sinha (2018) entropy method.

- Inputs: `sequences` (sequences, required)
- Outputs: `sequences` (sequences), `applied_direction` (text)
- Params:
  - `direction` (string, default `"auto"`) — auto | ltr | rtl

**`Filter` — Sequence Filter**

Filter sequences by min/max length.

- Inputs: `sequences` (sequences, required)
- Outputs: `sequences` (sequences), `total_sequences` (number)
- Params:
  - `min_length` (integer, default `1`) — Min Length
  - `max_length` (integer, default `50`) — Max Length

**`FreqCounter` — Frequency Counter**

Count symbol occurrences across all sequences.

- Inputs: `sequences` (sequences, required)
- Outputs: `freq_map` (freq_map), `total_tokens` (number), `distinct_symbols` (number), `top_10` (json)
- Params:
  - `min_count` (integer, default `1`) — Min Count
  - `top_n` (integer, default `0`) — Top N (0=all)

**`LabelMapApplier` — Label Map Applier**

Apply a sign->label map to sequences (Spec 087 S3). The map comes from the first source in the spec's fallback chain that yields one: a DB table, a JSON file, or frequency-rank binning of the input corpus itself. Unmapped signs receive the spec's unmapped label. The CGSA ClusterMapper delegates to this engine. NO phonetic mapping performed.

- Inputs: `sequences` (sequences, required)
- Outputs: `cluster_sequences` (json), `n_sequences` (number), `map_rate` (number), `n_mapped_tokens` (number), `n_unmapped_tokens` (number), `n_clusters` (number), `sign_to_cluster` (json)
- Params:
  - `db_table` (string) — Assignments table (flat use; see map_spec for chains).
  - `file_path` (string) — JSON file holding the map (flat use).
  - `bins` (integer, default `40`) — Frequency Bins
  - `unmapped_label` (integer, default `-1`) — Unmapped Label
  - `map_spec` (object) — Full declarative spec: sources chain, unmapped_label, unavailable_error.

**`Merger` — Result Merger**

Merge two or more upstream results into one JSON dict. Inputs grow automatically: wire any output into the last slot and a new empty slot appears. Supports up to 26 inputs (a–z) before switching to a2, b2, … naming.

- Inputs: `a` (any, required), `b` (any), `c` (any), `d` (any), `e` (any)
- Outputs: `json` (json)
- Params: none

**`MetricFieldExtractor` — Metric Field Extractor**

Extract a flat metric vector from wired analysis bundles (Spec 087 S3): the renaming table is a field_map parameter — an ordered list of extraction entries (a field of an input dict, the first row's field of a carried list, the field of the list row whose n equals a carried value, or the field of a list row at an index), each with a default. The Phase-14 DoFExtractor delegates to this engine, gaining its parameter surface from the map.

- Inputs: `block_entropies` (json), `zipf` (json), `mi_decay` (json), `hed` (json)
- Outputs: `dof_values` (json), `n_dofs` (number)
- Params:
  - `field_map` (array, default `[]`) — Ordered extraction entries: {out, kind, input, field/list_key/n/index, default}.

**`PersonsAggregator` — Persons Aggregator**

Aggregate person rows into per-name candidate counts (Spec 087 S3): rows are counted per candidate name with each name's period set and first example line, plus — as spec data dictates — provenience and source-pattern sets, distinct tablet counts, and segment-count enrichment; known-name confirmation is a carried name set, the rows' upstream is_known flag, or none, and the example-line truncation and verdict text are spec data. The Phase-22 MeluhhanPersonsExtractor, the Phase-23 RefinedMeluhhanPersonsExtractor, the Phase-24 RefinedMeluhhanPersonsExtractorV2, and the Phase-25 Persons_v3_Extractor delegate to this engine.

- Inputs: `persons` (json), `strict_persons` (json), `persons_v2` (json), `persons_v3` (json)
- Outputs: `n_unique_candidates` (number), `n_unique` (number), `rows_top50` (json), `rows_all` (json), `all_rows_count` (number), `n_total` (number), `confirmed_hits` (json), `by_pattern` (json), `verdict` (text)
- Params:
  - `min_freq` (integer, default `1`) — Min Frequency
  - `persons_spec` (object) — Input port key, collected field sets, known-name rule (set / upstream flag / none), example-line limit, output plan (count key names, row lists, by-pattern), verdict template.

**`TokenFilter` — Token Filter (Sanitize)**

Remove unwanted tokens from sequences by Unicode range, explicit blocklist, or minimum frequency. Solves the corpus sanitisation problem: strip punctuation, delimiter symbols, or rare noise tokens before building a language model. Example: unicode_ranges=['U+1200-U+1360'] removes Ethiopic punctuation (U+1361-U+1368) while keeping all syllabic signs.

- Inputs: `sequences` (sequences, required)
- Outputs: `sequences` (sequences), `total_tokens` (number), `removed_tokens` (number), `removed_types` (number), `kept_types` (number)
- Params:
  - `unicode_ranges` (array, default `[]`) — e.g. ['U+1200-U+1360'] keeps Ethiopic syllabic, removes punct. Leave empty to skip range filter.
  - `blocklist` (array, default `[]`) — Explicit list of token strings to remove (e.g. ['-', 'SPACE']).
  - `min_freq` (integer, default `0`) — Remove tokens appearing fewer than this many times. 0 = disabled.
  - `keep_empty_seqs` (boolean, default `false`) — If True, retain sequences that become empty after filtering.
<!-- END GENERATED node-reference -->

### Example: NW Semitic Decipherment Pipeline

```
CorpusReader -> TokenFilter -> SADecipher -> ConsistencyScorer -> JSONExport
BuiltinLM -------------------> SADecipher (lm input)
AnchorSetLoader -------------> SADecipher (anchors input, optional)
```

### GPU Acceleration

SADecipher automatically uses the GPU path (CuPy / BigramScorer) when it is available, and falls back to CPU with multi-core parallelism otherwise.

To enable GPU:

```
pip install cupy-cuda12x
```

Verify with `nvidia-smi`. GPU is 3-10x faster than CPU for experiments with more than 20 seeds.

---

## Study Builder

A Study composes multiple Experiments into a pipeline.

1. Open **Studies** in the sidebar
2. Drag experiment nodes from the palette onto the canvas
3. Connect the output of one experiment to the input of the next
4. Independent branches execute in parallel automatically
5. Click **Run Study** to execute

Results from each node appear in their respective Results views.

---

## Reports and Data

The Reports panel has two tabs:

- **Reports** — generated PDF and Markdown reports. Click to preview in-browser, or download.
- **Data** — raw JSON and CSV artefacts. Download or inspect with the inline JSON viewer.

Both tabs sort by date (newest first) and support keyword search.

---

## Glossa AI

### Opening Glossa AI

Click **Glossa AI** in the sidebar. The assistant panel opens on the right.

### Context Modes

| Context | What it loads |
|---|---|
| Global | General linguistics and scripting knowledge only |
| Corpus | The selected corpus content and statistics |
| Experiment | The selected experiment spec and recent results |
| Study | The selected study graph and all connected results |
| Research | Full LEDGER, notebooks, hypotheses, and all corpus summaries |

Use **Research** context for deep integration with your ongoing work.

### Automatic Actions

Glossa AI detects action requests and executes them, then shows a **View [page]** navigation link.

| Action | What it does |
|---|---|
| run_experiment | Runs a graph experiment by name or ID |
| run_pipeline | Queues an async pipeline job |
| create_hypothesis | Saves a hypothesis to the Hypotheses panel |
| create_notebook | Saves a research note to Notebooks |
| open_view | Navigates to any UI panel |
| acquire_corpus | Downloads and registers a corpus |
| execute_script | Runs a Python snippet in the backend |
| query_corpus | Searches for a token pattern in a corpus |
| summarize_session | Saves the conversation as a Notebook entry |

### Effective Prompting

**Be specific about corpus and experiment:**

> "Run the Fuls RTL corrected analysis on the NW Semitic Test1 corpus."

**Provide anchor assignments directly:**

> "Rerun with anchors: 004=T, 066=M, 208=N, 128=L, 080=W."

**Ask for validation:**

> "Is this result significantly above the random baseline? Compare H1 and TTR."

**Request chained workflows:**

> "Upload the Ge'ez corpus, run the anchor convergence benchmark, and generate a PDF report."

### Conversation Continuity

1. At session end: "Summarize this session and save it to notebooks."
2. Next session: switch to **Research** context — LEDGER and notebooks are loaded automatically.

---

## Understanding Results

### Writing System Classification

| Type | H1 range | Alphabet size | Examples |
|---|---|---|---|
| Abjad | 4.1-4.7 bits | 22-30 signs | Hebrew, Ugaritic, Phoenician |
| Syllabary | 4.7-7.5 bits | 40-120 signs | Linear B, Old Persian, Ge'ez |
| Logographic | >7.5 bits | 400+ signs | Sumerian, Chinese, Egyptian |

The classifier uses H1 and alphabet size jointly. A corpus at H1 = 5.6 bits with 78 signs classifies as **SYLLABIC** (nearest comparator: Linear B, Mycenaean Greek).

### Mapping Consistency

**Consistency** (0-100%) is the fraction of independent SA runs agreeing on the same phoneme for a given sign.

| Consistency | Interpretation |
|---|---|
| 80% or above | Strong signal: data reliably constrains this sign |
| 60-80% | Moderate signal: plausible, check against anchors |
| Below 60% | Weak signal: multiple competing solutions; more data needed |

**What it IS:** signal stability.
**What it IS NOT:** accuracy. High consistency at low token density does not mean the assignment is correct.

### Compression Ratio

Before any anchors, the system reduces the search space from the full target alphabet (e.g. 22 consonants) to approximately 2.4 candidates at 80% posterior coverage — a **10x compression ratio** from corpus statistics alone.

### Anchor Amplifier Effect

Adding one verified anchor produces improvement on non-anchored signs approximately **12x the naive combinatorial expectation**. The constraint propagates through the co-occurrence structure of the corpus.

**Empirical benchmark (Ge'ez syllabic corpus, structured anchors):**

| Anchors | Free-sign accuracy |
|---|---|
| 0 | 4.5% (random baseline) |
| 1 | 7.2% (+60% gain) |
| 3 | 12.1% (+170% gain vs baseline) |
| 6 | Cluster collapse observed |

Random anchors (placebo) produce no consistent improvement, confirming the effect is structural.

### Positional Profiles (T/I/M)

The positional profiler classifies each sign as:

- **T** (terminal) — predominantly at word-end. High T = likely grammatical suffixes or determinatives.
- **I** (initial) — predominantly at word-start. High I = likely prefixes or determinatives.
- **M** (medial) — mainly in the middle of words.

High T or I signs are the highest-priority anchor candidates.

### RTL Correction

For right-to-left scripts, all positional analysis must use reversed sequences. After RTL correction, T/I/M labels apply to linguistically correct positions.

**Example:** Sign 066 in NW Semitic has file-position T=0.022 (near word-start in file), but after RTL correction has T=0.967, consistent with the *-m* suffix (mem).

### Known Limitations

1. **Low token density (~4 tok/sign):** consistency does not predict accuracy. The correct assignment is in the top-3 candidates in ~13% of cases, matching random baseline. Add anchors to improve.
2. **Fragmented solutions:** without anchors, 50 seeds may produce 40-50 distinct full solutions. Only consistency aggregation makes results interpretable.
3. **Frequency-dominated signal:** at 4 tok/sign, the dominant signal is unigram frequency, not within-word sequential order. You need 10+ tok/sign for sequential information to emerge.
4. **LM quality:** using a mismatched language model (e.g. a Hebrew LM for a syllabic corpus) reduces accuracy. Use **CorpusLM** with an appropriate reference corpus.

---

## NW Semitic Analysis Walkthrough

This walkthrough replicates the analysis performed for Dr. Andreas Fuls (TU Berlin) using a 101-word NW Semitic syllabic corpus.

### Step 1: Upload the Corpus

Upload a sign-sequence `.txt` file (signs separated by `-`, one word per line). Name it "NW Semitic Test1", type = Ancient. Leave reading direction as Unknown.

### Step 2: Detect Reading Direction

Open the corpus card -> **Edit** tab -> click **Auto-detect**.

Expected result: **RTL** (entropy lower at position 0 than at position -1).

### Step 3: Inspect Structural Fingerprint

Open **Stats** tab. Expected: H1 ~= 5.6 bits, classifying as SYLLABIC.

### Step 4: Positional Profile Analysis

Ask Glossa AI: "Compute the T/I/M positional profiles for all signs, using RTL-corrected sequences."

Key findings:
- Sign 066 (RTL): T=0.967 — word-final sign (mem suffix)
- Sign 073 (RTL): I=1.000 — word-initial sign
- Sign 112 (RTL): I=1.000 — second most frequent word-initial sign

### Step 5: Run Mapping Inference Without Anchors

Run the `fuls_rtl_corrected` experiment. Expected: ~55-60% mean consistency, 10-17 high-confidence signs.

### Step 6: Add Anchors and Rerun

Create an anchor set with: 004=T, 066=M, 208=N, 128=L, 080=W (all high confidence). Run again with AnchorSetLoader.

Expected with 6 anchors: mean consistency ~64%, high-confidence signs approximately double (10 to 23).

### Step 7: Export the Report

Ask Glossa AI: "Generate the PDF report of all experimental results." Or go to **Reports** to download.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Logs show stale entries | Purge the log with `POST /terminal/log/purge`, or read only the newest rotation of `glossa.log` |
| Logs not updating | The live stream is at `GET /terminal/log/stream`; the in-app Logs view returns under Spec 087 S5 |
| Action fails with error | Rephrase your request more specifically: "Run experiment X on corpus Y" |
| Low consistency results | Expected at low token density; add verified anchor assignments |
| Anchor amplifier not working | Use only high-confidence anchors; conflicting anchors reduce the effect |
| GPU not used | Install CuPy: `pip install cupy-cuda12x`. Verify with `nvidia-smi`. |
| Experiments not listed | Click the reload button in the Experiments panel |
| PDF has white squares | Non-Latin-1 characters in report text; use ASCII equivalents |
| Backend not responding | `setup-os.cmd restart` (Windows) or `./setup-os.sh restart` (macOS/Linux) |
| UI shows wrong port | Check tray icon port. Default is 8001. Navigate to `http://localhost:<port>`. |
| Corpus import fails | File must be UTF-8 encoded. One word per line, signs separated by `-`. |
| World catalogue import unavailable | No bundled module; download from Source link and upload manually |
| Anchor set not loading | Verify `anchor_set_id` in AnchorSetLoader matches the ID of your set |
| TokenFilter removes all tokens | Check `unicode_ranges` covers your script's codepoints. Inspect Stats tab before filtering. |
| SubExperiment node fails | The referenced experiment must declare ExperimentInput/ExperimentOutput ports |

### Log Levels

- **INFO** — normal operation: started, ready, job events
- **WARNING** — non-fatal issues: slow performance, minor data problems
- **ERROR** — failures: exceptions, job errors, connection failures
- **DEBUG** — detailed diagnostic messages (only in debug mode)

### Backend Health

Open **Status** in the sidebar for real-time metrics: CPU, RAM, disk, GPU usage, backend uptime, database path, and Ollama model status.

If the backend does not start:
1. Check that port 8001 is not already in use
2. Look at the backend log (`glossa.log`) for startup error messages
3. Change the port via the tray icon **Change Port...** menu

---

## Performance Tips

- Use GPU (CuPy) for experiments with more than 20 seeds — 3-10x faster than CPU
- For small experiments (fewer than 10 seeds), CPU multi-core mode avoids CUDA overhead
- Keep corpus files under 50,000 tokens for interactive Stats tab responsiveness
- Use `min_freq = 2` in TokenFilter to remove hapax tokens when corpus is sparse
- Use **Research** context in Glossa AI for multi-turn analytical workflows

---

*Glossa Lab — BitConcepts LLC Research Programme*
