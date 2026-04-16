# Glossa Lab — User Manual

**Version**: 1.0 · BitConcepts Research Platform

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
| **Ctrl+J** | Toggle bottom panel (Logs/Jobs/Terminal) |
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

| Section | Description |
|---|---|
| **Corpora** | Upload, inspect, sanitize, and manage sign-sequence corpora |
| **Experiments** | Browse, build, and run graph experiments |
| **Pipelines** | Async job management |
| **Studies** | Compose multi-experiment research workflows |
| **Reports** | PDF and Markdown reports from experiments |
| **Data** | JSON and CSV artefacts from experiments |
| **Entropy** | Visualise H1, Zipf distributions, and positional entropy |
| **Signs** | Browse the sign dictionary |
| **Hypotheses** | Create and track research hypotheses |
| **Notebooks** | Research notes and session summaries |
| **Jobs** | Background job queue with result viewer |
| **Status** | CPU, RAM, GPU, DB health, and backend uptime |
| **Settings** | API keys, LLM model selection, environment |

### Bottom Panel (Ctrl+J)

| Tab | Description |
|---|---|
| **Logs** | Live colour-coded backend log stream. Green=INFO, Yellow=WARN, Red=ERROR. Click **Purge** to clear. |
| **Jobs** | Job queue with status, progress, and expandable result JSON. |
| **Terminal** | Command-line access to the backend environment. |

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
| `unicode_range` | Keep only tokens whose characters fall within a Unicode codepoint range (e.g. `[0x1200, 0x137F]` for Ethiopic/Ge'ez) |
| `blocklist` | List of specific token strings to always remove |
| `min_frequency` | Drop tokens appearing fewer than N times in the corpus |
| `invert` | If true, remove tokens matching the range instead of keeping them |

**Example — Ge'ez corpus contaminated with punctuation:**

In the Experiment Builder, connect `CorpusLoader -> TokenFilter -> MappingInference`. Set `unicode_range = [0x1200, 0x137F]` on the TokenFilter node to keep only Ge'ez syllabic characters.

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

Add an **AnchorSetLoader** node to your experiment graph. Set its `anchor_set_id` parameter to the ID of the anchor set you created. Connect its output to the `anchors` input of a **MappingInference** or **AnchorInjector** node.

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

### Node Reference

**Corpus Loaders:**

| Node | Description |
|---|---|
| CorpusLoader | Loads a corpus from the database by corpus ID |
| CorpusLM | Loads a corpus and builds a language model from it (no Python file needed) |
| BuiltinLM | Loads a pre-seeded LM (Old Hebrew, Ge'ez, Phoenician, Meroitic, etc.) |

**Structural Analysis:**

| Node | Description |
|---|---|
| EntropyAnalyzer | Computes H1, H2, conditional entropy, Zipf, TTR |
| WritingSystemClassifier | Classifies as abjad/syllabary/logographic from H1 and alphabet size |
| PositionalProfiler | Computes T/I/M probability per sign |

**Corpus Filters:**

| Node | Description |
|---|---|
| TokenFilter | Removes tokens by Unicode range, blocklist, or minimum frequency |

**Mapping Inference:**

| Node | Description |
|---|---|
| MappingInference | SA-based sign-to-phoneme inference (main decipherment engine) |
| AnchorInjector | Locks specified sign-phoneme assignments before inference |
| AnchorSetLoader | Loads a saved anchor set from the database by ID |
| AnchorConvergenceBenchmark | Sweeps anchor counts and measures free-sign accuracy |

**Evaluation:**

| Node | Description |
|---|---|
| ConsistencyEvaluator | Measures across-seed agreement for each sign |
| AnchorAccuracyEvaluator | Evaluates held-out anchor recovery rate |
| RandomBaselineComparator | Compares results against a shuffled-corpus baseline |

**Reporting:**

| Node | Description |
|---|---|
| JSONReportWriter | Writes results to JSON in the Data panel |
| MarkdownReportWriter | Writes a Markdown summary to the Reports panel |
| PDFReportWriter | Generates a PDF from a report template |
| ReportGenerator | Uses a user-defined report template |

**Sub-Experiments:**

| Node | Description |
|---|---|
| SubExperiment | Embeds another experiment as a reusable subroutine |
| ExperimentInput | Declares a named input port for an experiment |
| ExperimentOutput | Declares a named output port for an experiment |

### Example: NW Semitic Decipherment Pipeline

```
CorpusLoader -> TokenFilter -> AnchorSetLoader -> MappingInference -> ConsistencyEvaluator -> JSONReportWriter
                                |                                                             |
                         AnchorInjector                                             MarkdownReportWriter
```

### GPU Acceleration

MappingInference automatically uses GPU (CuPy) if available, and falls back to CPU (NumPy) with multi-core parallelism otherwise.

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
| Logs show stale entries | Click **Purge** (orange) in Logs panel to clear the file and restart stream |
| Logs not updating | Click Purge to trigger EventSource reconnect |
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
| TokenFilter removes all tokens | Check `unicode_range` covers your script's codepoints. Inspect Stats tab before filtering. |
| SubExperiment node fails | The referenced experiment must declare ExperimentInput/ExperimentOutput ports |

### Log Levels

- **Green** — INFO, started, ready
- **Yellow** — WARNING
- **Red** — ERROR, exception, failed
- **Grey** — DEBUG

### Backend Health

Open **Status** in the sidebar for real-time metrics: CPU, RAM, disk, GPU usage, backend uptime, database path, and Ollama model status.

If the backend does not start:
1. Check that port 8001 is not already in use
2. Look at the Logs panel for startup error messages
3. Change the port via the tray icon **Change Port...** menu

---

## Performance Tips

- Use GPU (CuPy) for experiments with more than 20 seeds — 3-10x faster than CPU
- For small experiments (fewer than 10 seeds), CPU multi-core mode avoids CUDA overhead
- Keep corpus files under 50,000 tokens for interactive Stats tab responsiveness
- Use `min_frequency = 2` in TokenFilter to remove hapax tokens when corpus is sparse
- Use **Research** context in Glossa AI for multi-turn analytical workflows

---

*Glossa Lab — BitConcepts Research Programme*
