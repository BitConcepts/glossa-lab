# Glossa Lab — User Guide

> **Version**: current `main` branch
> **Last updated**: 2026-04-09

---

## Table of Contents

1. [Overview](#1-overview)
2. [Getting Started](#2-getting-started)
3. [Navigation & Layout](#3-navigation--layout)
4. [Corpora](#4-corpora)
5. [Experiments](#5-experiments)
6. [Pipelines](#6-pipelines)
7. [Study Builder](#7-study-builder) ← _the core workflow_
8. [Reports](#8-reports)
9. [Jobs](#9-jobs)
10. [Analysis Tools](#10-analysis-tools)
11. [Glossa AI Chat](#11-glossa-ai-chat)
12. [Terminal](#12-terminal)
13. [Settings](#13-settings)
14. [Advanced Usage](#14-advanced-usage)
15. [Example Workflows](#15-example-workflows)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Overview

**Glossa Lab** is a computational linguistics research platform designed for
analysing undeciphered scripts and comparing them against known writing systems.
Its primary research focus is the **Indus Script** using the methodology of
Dr. Andreas Fuls (TU Berlin / ICIT), but it is built as a general-purpose tool
for any corpus of symbol sequences.

### Core capabilities

- Upload and manage symbol-sequence **corpora**
- Run statistical analysis **experiments** (positional profiles, entropy, Zipf, NWSP, clustering…)
- Submit long-running **pipelines** as async background Jobs that integrate into study graphs
- Compose any asset into a **study graph** with typed data-flow edges and 8 node types
- **RAG-enhanced AI Chat** that retrieves relevant artifacts before answering
- View, filter, and compose **reports** into unified PDFs
- Track **hypotheses**, write **notebooks**, and cite **references**

### Complete workflow architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                      STUDY GRAPH (DAG)                            │
│                                                                   │
│ [Corpus]──→[Experiment]──→[Pipeline]──→[RAG Query]──→[AI Analysis]│
│  📚 pass     🧪 sync       ⚙️ async+     🔍 search    ✨ interpret │
│ corpus_id    in-process    poll          knowledge    upstream ctx │
│                                                                   │
│ [Note] [Report] [Hypothesis]  ← annotation nodes, no execution    │
└────────────────────────┬──────────────────────────────────────────┘
                         │ results / reports
              ┌──────────┴───────────┐
              │      Reports         │
              │  (JSON in reports/)  │
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
   [AI Chat]      [Hypotheses]    [Notebooks]
   + RAG inject    Tracker         Citations
```

### Execution model: Experiments vs Pipelines

| Node type | Execution | Result available |
|-----------|-----------|------------------|
| **experiment** | Synchronous, in-process | Immediately during Run Study |
| **pipeline** | Async Job submitted + polled | After job completes (120s timeout) |
| **rag_query** | TF-IDF search of the index | Immediately during Run Study |
| **ai_analysis** | Calls Glossa AI with upstream context | Within seconds during Run Study |
| **corpus / note / report / hypothesis** | Annotation only | Instant passthrough |

---

## 2. Getting Started

### Prerequisites

- Python 3.10+ with the project's virtual environment activated
- Node.js 18+ for the frontend (in development)
- Ollama (optional) for local AI models

### Launch

```cmd
setup-os.cmd          # Windows — starts backend + tray + frontend
```

The app runs at **http://localhost:8001** by default.
The tray icon provides Start / Stop / Restart controls.

### First run checklist

1. Open the app in your browser.
2. Check the **Status** badge (top-left ⚡) — should show "Healthy".
3. Go to **Corpora** and verify the built-in Indus corpus is listed.
4. Go to **Study Builder** — you should see 8 pre-built study seeds.
5. Click a study, inspect its nodes, and click **▶ Run Study** to verify the pipeline runs.

---

## 3. Navigation & Layout

### Sidebar sections

| Section | Items |
|---------|-------|
| **Workflow** | Corpora · Experiments · Pipelines · Studies · Reports |
| **Analysis** | Entropy · Signs · Timeline · Indus Data |
| **Research** | Hypotheses · Notebooks · Citations · AI Tools |
| **System** | Status · Jobs · Settings |

**Key name changes (vs older versions)**:
- "Study Builder" → **Studies** (unified workspace: study list + graph editor)
- "Exp. Builder" merged into **Experiments** (unified workspace: experiment list + graph editor)
- "Studies" (Indus statistical data) → **Indus Data** (moved to Analysis)

### Nav indicator dots

Each workspace tab shows a coloured dot reflecting its state:

| Dot | Meaning |
|-----|---------|
| 🟡 Amber | Unsaved graph changes in this workspace |
| 🟢 Pulsing | One or more runs currently in progress |
| 🟢 Solid | Last run completed successfully |
| 🔴 Solid red | Last run failed or was aborted |

### Header toolbar

| Control       | Shortcut   | Purpose |
|---------------|-----------|---------|
| ⌘K             | Ctrl+K    | Command palette — navigate anywhere by name |
| ⊟             | Ctrl+J    | Toggle the bottom panel (Terminal / Logs / Jobs / Chat) |
| 🔔             | —         | Notifications dropdown |
| 🌙/☀️          | —         | Dark / light mode toggle |

### Bottom panel tabs

| Tab      | Purpose |
|----------|---------|
| Logs     | Live backend log stream |
| Jobs     | Running and queued pipeline jobs |
| Terminal | Interactive shell with history, Tab autocomplete, Ask AI button |
| Chat     | Docked AI chat (same as floating bubble) |

### Floating AI Chat

Click the **✨ bubble** (bottom-right) to open the floating AI chat window.
Click **× bubble** (red) or the × header button to close it.

---

## 4. Corpora

**Path**: sidebar → Corpora

A corpus is a collection of symbol sequences. Each sequence represents one
inscription, text, or record. Glossa Lab stores corpora in its SQLite database.

### Uploading a corpus

1. Click **+ New Corpus**.
2. Enter a name and corpus type (e.g. `linguistic`, `genetic`, `cipher`).
3. Paste or upload your data as JSON:
   ```json
   {
     "name": "My Corpus",
     "corpus_type": "linguistic",
     "content": [
       ["A", "B", "C", "A"],
       ["B", "C", "D"],
       ["A", "A", "B"]
     ]
   }
   ```
   Each inner array is one sequence (inscription, sentence, or record).

### Built-in corpora

The Indus synthetic corpus (calibrated to Yadav 2010 / Fuls 2014) is seeded
automatically on first run. It is used by experiments that specify no `corpus_id`.

The **ICIT extracted corpus** (`reports/icit_extracted_corpus.json`) is produced
by the OCR pipeline and used by research-specific experiments like
Contact Zone Analysis and Luwian KL Scoring.

### Corpus ID

Each corpus has a UUID (e.g. `a1b2c3d4e5f6`). Use this as the `corpus_id`
parameter in experiment nodes to target a specific corpus.

---

## 5. Experiments

**Path**: sidebar → Experiments (unified workspace)

The Experiments tab is the **Experiment Builder** — a ComfyUI-style visual
editor where you compose atomic computation nodes into graph experiments.
These graph experiments also appear in the Study Builder palette so you can
use them as nodes in a full research workflow.

### Active graph experiments (Experiment Builder palette)

| Experiment | Description | Corpus |
|------------|-------------|--------|
| Positional Profile Analysis | I/M/T rates per symbol (NWSP) | Any |
| Symbol Clustering | L1 clustering by positional profile | Any |
| Word-Length KL Scoring | KL/JS divergence vs language profiles | Any (or ICIT) |
| Contact Zone Analysis | Site-grouping KL/Jaccard analysis | ICIT only |
| Indus Structural Atlas | Entropy + Zipf + NWSP + clustering | Synthetic Indus |
| Kandles Bias Comparison | Biased vs unbiased Kandles profiles | Synthetic Indus |
| Linear A Anti-Circularity | 7-experiment validation suite | Linear A internal |
| OCR — Tables / Texts | CLI-only Mahadevan extraction | N/A (CLI only) |

Validation experiments (Ugaritic, Ventris, Progression) remain available as
Python classes for study execution but are not in the Experiment Builder palette.

### Running an experiment graph

1. Select a saved experiment from the left panel list, or click **＋ New**
2. Build/edit the node graph on the canvas
3. Click the **▶ Run** floating pill at the **top-centre of the canvas**
4. Each node highlights in blue as it executes (SSE streaming — real-time)
5. Results shown in the banner below the canvas

All runs create a **Job record** visible in the Jobs panel (`pipeline='exp_run'`).

### Multiple concurrent runs

- Click **▶▶** in the experiment list header to run ALL saved experiments in parallel
- Each experiment has its own abort controller — independent runs don't block each other
- **⏹ Stop All** button appears in the toolbar when any runs are active
- Per-experiment `⏹` stop button also appears on the canvas floating pill

### Corpus selection in the Inspector

When you click a node with a `corpus_id` parameter, the Inspector shows a
**corpus dropdown** instead of a plain text field. It lists all uploaded corpora
from the database. Select one or leave blank for the experiment's default.

### Via the API (SSE streaming)

```
POST /api/v1/experiment-graphs/{id}/run
Content-Type: application/json
{"kwargs": {}}
→ returns text/event-stream with events: started | node_start | node_end | run_complete | run_error
```

### Adding a custom experiment

See `backend/glossa_lab/experiments/CONTRIBUTING.md` for the full guide.
Short version:

1. Create a Python file in `backend/glossa_lab/experiments/`.
2. Define a class inheriting from `ExperimentBase` with the required class variables.
3. Add `params_schema` to make params editable in the Study Builder.
4. Click **Reload** in the Experiments tab (or `POST /api/v1/experiments/reload`).

---

## 6. Pipelines

**Path**: sidebar → Pipelines

Pipelines are **statistical analysis functions** that run asynchronously as
background jobs. Unlike experiments, pipelines are invoked by submitting a job
(via the Jobs tab or API) and the result is stored in the job results table.

### Available pipelines (statistical, no language model required)

| Pipeline                | Description |
|------------------------|-------------|
| Block Entropy          | H_n for n=1..N; validates Rao (2009) linguistic claim |
| Character Frequency    | Zipf exponent; validates Yadav (2010) result |
| Positional Analysis    | Initial / medial / terminal rates per sign |
| NWSP — Fuls Method     | Exact Fuls (2013) Normalized Weighted Sign Position |
| Sign Polyvalence       | Bimodal histogram detection (sign 550 analysis) |
| Sign Clustering        | Distributional clustering by co-occurrence |
| Co-occurrence Network  | Louvain community detection on sign pairs |
| Paradigm Detection     | Morphological alternation pattern count |
| Structural Fingerprint | 10-dimensional fingerprint vs known script DB |
| Sign Function Estimator| P(numeral/determinative/logogram/phonetic) per sign |
| Numeral Detection      | Positional numeral candidate identification |
| Word-Structure Typology| KL divergence vs 6 language family profiles |
| Distributional Decipherment | Jensen-Shannon clustering + Ventris grid |
| Logosyllabic Analysis (Ventris) | Full sign classification + proposed CV readings |

### Pipelines requiring a language model

| Pipeline         | Description |
|-----------------|-------------|
| Kandles Fingerprint | Merkur phonological colour fingerprint |
| Decipher (Substitution) | Hill-climbing substitution cipher solver |
| Hypothesis Engine | Iterative hypothesis-test-score loop |

### Running a pipeline

1. Go to **Jobs** → **+ New Job**.
2. Select the pipeline and enter params as JSON.
3. Monitor progress in the Jobs panel.
4. View results in the Reports tab once completed.

---

## 7. Study Builder

**Path**: sidebar → Studies (unified workspace)

The Studies tab is the central workflow interface. Left panel: study list + node palette.
The canvas is a visual DAG editor for composing experiments and pipelines.

### Concepts

| Term         | Meaning |
|-------------|---------|
| **Study**   | A named research workflow saved to the database |
| **Node**    | A single experiment or pipeline in the graph |
| **Edge**    | A data-flow connection from one node's output to another's input |
| **Inspector** | Right panel — shows and edits the selected node's parameters |
| **Palette** | Left panel — lists all available experiments and pipelines |

### Creating a study

1. Type a name in the **New study name** field and click **+**.
2. The study is created with an empty graph.

Or use **✨ AI Design** to describe a research goal and have the AI compose a
study graph automatically.

### Node types in the palette

The palette has four groups:
- **Data & Analysis**: corpus, rag_query, ai_analysis, note, report, hypothesis
- **Experiments**: all ExperimentBase subclasses
- **Pipelines**: all registered pipeline functions

Search by name or filter by group using the pill buttons.

### Building the graph

1. **Drag** an item from the Palette, or **right-click the canvas** to add a node at the cursor.
2. **Click** a node to select it — the Inspector panel appears on the right.
3. **Set parameters** in the Inspector. Typed form fields appear for each configurable param.
4. **Connect nodes** by dragging from the **right-side handle** of one node to the **left-side handle** of another.
5. **Reconnect a connection** by dragging an edge endpoint to a different node handle.
6. **Delete a connection**: right-click the edge → Delete connection, or select + Delete key.
7. **Delete a node**: × button on the node, right-click → Delete node, or select + Delete key.
8. **Save** (💾) to persist the graph. **Run** auto-saves before executing.

### Typical node workflow

```
[Corpus] ──→ [Experiment] ──→ [Pipeline] ──→ [RAG Query] ──→ [AI Analysis]
   Set            Set            Set ref        (auto-builds    (interprets
 corpus_id      exp ref_id    pipeline ref     query from       upstream)
   param          + params       + params       upstream)
```

### Corpus data flow

The recommended pattern for flexible, corpus-agnostic research:

```
[📚 Corpus node]  ← select corpus from dropdown in Inspector
       │  corpus_id flows to all downstream experiments
       ▼
[🧪 Experiment]   ← runs on your corpus (corpus_id injected automatically)
       │  result
       ▼
[🧪 Experiment 2] ← can also use upstream result data
       │  result
       ▼
[📄 Report]       ← saves all upstream results to reports/<name>.json
```

**corpus_id resolution order** (per experiment node, during study run):
1. Explicit `corpus_id` param set on the node in Inspector
2. `corpus_id` from an upstream Corpus (📚) node result
3. Blank → experiment uses its built-in default (usually ICIT corpus)

### Running a study

Click the **▶ Run Study** floating pill at the **top-centre of the canvas**.
The backend streams Server-Sent Events showing each node as it executes:

1. Topologically sorts nodes (sources first)
2. For each node, emits `node_start` → executes → emits `node_end`
3. The **currently executing node** pulses blue on the canvas
4. A Job record (`pipeline='study_run'`) is created and visible in the Jobs panel
5. When complete, emits `run_complete` with all results

Node status colours after run:
- 🔵 **Pulsing blue** — currently executing (real-time, via SSE)
- 🟢 **Green dot** — complete
- 🔴 **Red dot** — error or failed
- 🟡 **Amber dot** — skipped / pending (CLI-only or job timed out)
- ⚫ **Grey dot** — annotation node (corpus/note/hypothesis — not executed)

### Multiple concurrent runs

- Click **▶▶** in the study list header to run **all studies in parallel**
- Each study has its own SSE stream and abort controller
- **⏹ Stop All** appears in the toolbar when any runs are active
- Per-study `⏹` stop button on the canvas; per-study `⏹` in the study list
- Study list shows live status: `⏳ 5s · FreqCounter (2/7)` while running,
  then `✓ 5/7` (success) or `✗ 2/7` (errors) after completion

### Inspector — editing node parameters

Clicking a node opens the Inspector panel (right side). Typed form fields appear
for each configurable parameter:

| Field type | Rendered as |
|------------|-------------|
| `corpus_id` | Dropdown of all uploaded corpora + "Default Indus corpus" option |
| String | Text input |
| Integer / Number | Number input with optional min/max |
| Boolean | Checkbox toggle |

**Corpus selector**: any parameter named `corpus_id` shows a live dropdown
fetched from the Corpora tab. Select a corpus or leave blank for the default.

Changes update the node's params immediately. **💾 Save** to persist.

### Pre-built study seeds

On first startup, Glossa Lab creates 8 curated seed studies:

| Study | Graph structure | Notes |
|-------|-----------------|-------|
| **Positional Profile Analysis** | single node → report | Generic, set corpus_id in Inspector |
| **Symbol Clustering** | positional_profile → symbol_clustering → report | Generic |
| **Indus Contact Zone & KL Scoring** | 3 parallel nodes → report | Requires ICIT corpus |
| **Indus Structural Atlas** | atlas → kandles_bias → report | Synthetic Indus corpus |
| **Ugaritic Anti-Circularity Benchmark** | 2 nodes → report | Validation |
| **Writing System Progression** | 3 nodes → report | Validation |
| **Linear A Anti-Circularity Suite** | linear_a → kandles_bias → report | ~30s (3 MC trials) |
| **OCR Pipeline** | 2 parallel CLI-only nodes | Requires Mistral key + PDFs |

**Graph preservation**: seed study _graphs_ are **never overwritten** after the
first creation. Your modifications survive backend restarts. Only the `name` and
`description` fields update on restart. To reset to the original graph, delete
the study and restart the server.

### AI features in Study Builder

| Button | Action |
|--------|--------|
| **✨ AI** | AI summarizes the current study: abstract, hypothesis, highlights, next steps |
| **✨ Design** | Opens AI Chat with the study as context; AI suggests experiments and improvements |
| **↓ Export** | Download the current study as a `.glossa-study.json` file |
| **↑ Import** (studies panel) | Open a JSON file to import a study into the database |
| **⎘** (studies panel) | Duplicate a study with one click |

### Study management

- **Create**: click **+** in the studies panel header to open the New Study dialog.
- **Import**: click **↑** to open a file picker and import a `.glossa-study.json` file.
- **Export**: click **↓ Export** in the toolbar to download the current study.
- **Duplicate**: click **⎘** next to any study in the list.
- **Delete**: click **×** (confirm with a second click).
- **Dock side**: click **⇄** to move the panel to the other side of the screen.
- **Collapse**: click **◀** to collapse the panel and get more canvas space.

---

## 7b. RAG (Retrieval-Augmented Generation)

Glossa Lab maintains a semantic knowledge base built from your research artifacts.

### What gets indexed

- All JSON files in `reports/`
- Hypothesis statements and evidence
- Notebook content
- Corpus metadata
- Experiment descriptions and param documentation

### How to use RAG

**Automatic**: In AI Chat Research or Study mode, the AI automatically retrieves
relevant chunks before answering. A `=== RETRIEVED RESEARCH ARTIFACTS ===` section
appears in the context (invisible to you but visible to the AI).

**In Study Builder**: Add a **RAG Query** node (🔍). It runs a semantic search
using upstream results as the query and passes retrieved chunks to downstream
**AI Analysis** nodes.

**Rebuild the index**: click the **🔍 RAG** button in the Study Builder toolbar
(it shows 🔍✓ when ready). Or call `POST /api/v1/rag/index`.

**Query directly**: `POST /api/v1/rag/query` with `{"query": "...", "top_k": 5}`.

### When to rebuild

The index is built automatically on startup. Rebuild after:
- Running new experiments (new report files)
- Adding notebooks or hypotheses
- Uploading new corpora

---

## 8. Reports

**Path**: sidebar → Reports

Reports are JSON output files produced when experiments or pipelines run.
They are stored in the `reports/` directory and auto-linked to their producing
experiment.

### Browsing reports

Filter by **type** (json_report, document, table, pdf, artifact), by
**experiment**, or by **study** (filters to experiments in that study's graph).

Sort by name, kind, size, or last-updated timestamp.

Click a row to **view** the file in a popup (if popups are allowed). Use
**Open Folder** to reveal the file in Explorer.

### Compose mode

Click **📊 Compose** to enter compose mode:
1. Check rows you want to include in the composed report.
2. Click **Select all** or **Clear** for bulk selection.
3. Click **📄 Export PDF** to open a print-ready window with all selected reports listed as sections.
4. Use the browser's Print dialog to save as PDF.

This allows you to assemble a multi-experiment research report without manual copying.

---

## 9. Jobs

**Path**: sidebar → Jobs (or bottom panel → Jobs tab)

Jobs are asynchronous pipeline executions. They run in the background via the
pipeline engine and store results when complete.

### Submitting a job

**From the Jobs tab**: click **+ New Job** and fill in the pipeline name and parameters.

**From the Pipelines tab**: expand a pipeline card, then use the "Launch Job" button (if present).

### Job statuses

| Status    | Meaning |
|-----------|---------|
| `pending` | Queued, waiting for the engine to pick it up |
| `running` | Currently executing |
| `completed` | Finished; results stored |
| `failed`  | Error occurred; error stored in results |

### Viewing results

Click a completed job row to expand it and see the result JSON.

---

## 10. Analysis Tools

### Entropy Dashboard

**Path**: sidebar → Entropy

Interactive block entropy analysis for a selected corpus. Shows H_n for n=1..4,
H2/H1 ratio, Zipf table, and linguistic classification.

### Sign Dictionary

**Path**: sidebar → Signs

Browse the Indus sign catalog with positional statistics (I/M/T rates) and
frequency data per sign.

### Timeline

**Path**: sidebar → Timeline

Chronological view of research milestones and experiment runs.

### Hypothesis Tracker

**Path**: sidebar → Hypotheses

Track research hypotheses with evidence links, status (active/confirmed/refuted),
and connections to studies and experiments.

### Research Notebook

**Path**: sidebar → Notebooks

Markdown notebooks for recording observations, attaching to studies, and
tagging for later retrieval.

### Citation Manager

**Path**: sidebar → Citations

Manage academic references with BibTeX import/export. Link citations to
experiments and studies.

---

## 11. Glossa AI Chat

Click the **✨ bubble** (bottom-right corner) to open the floating AI chat.

### Context modes

| Mode | What AI knows |
|------|---------------|
| **Global** | General Glossa Lab knowledge |
| **Corpus** | Corpus metadata + top tokens |
| **Experiment** | Experiment description and params |
| **Study** | Study graph + related RAG artifacts (auto-retrieved) |
| **🔬 Research** | Full Indus decipherment context + sign profiles + LEDGER + RAG-retrieved artifacts |

In Research and Study modes, the AI automatically retrieves semantically relevant
chunks from the RAG knowledge base and prepends them to the context.

### Model picker

Click the **auto ▾** dropdown in the chat header to select:
- **Auto** — uses the backend default (configured in Settings)
- **Ollama local models** — models installed via `ollama pull`; shown bold if installed
- **Cloud providers** — grayed out if no API key is set in Settings

### Slash commands

| Command | Action |
|---------|--------|
| `/compress` | Summarize and compress the chat context |
| `/clear` | Clear all messages |
| `/export md` | Download chat as Markdown |
| `/export pdf` | Open print dialog for PDF export |
| `/help` | Show this command list |

### Context management

The context bar (top of chat window) shows how full the context window is.
At 75% a warning appears; at 90% auto-compression triggers.
Click **⊟** (compress button) or `/compress` to manually summarize.

### AI actions

When the AI suggests an action (run experiment, change setting, open a view,
create a hypothesis), it shows an **action card** with **✓ Approve** / **✗ Cancel**.
Major actions require your approval; minor ones (e.g. opening a view) execute automatically.

---

## 12. Terminal

**Path**: bottom panel → Terminal tab

An interactive shell for running CLI commands, scripts, and experiments.

### Features

- **Tab autocomplete** on commands and file paths
- **Command history** — ↑/↓ arrows
- **Paste** from clipboard
- **Ask AI** button — sends the last command + output to the AI chat for analysis
- **Help** button — inserts the `help` command
- **Clear** button — clears terminal output

### Useful commands

```bash
# Run a CLI-only experiment
python -m glossa_lab.experiments.run_kandles_biased_experiments --trials 30

# Check registered experiments
python -c "from glossa_lab.experiment_base import discover_experiments; print(list(discover_experiments()))"

# Restart the backend without the tray
uvicorn glossa_lab.main:create_app --factory --port 8001 --reload
```

---

## 13. Settings

**Path**: sidebar → Settings (bottom of sidebar)

### API keys

Store API keys for cloud AI providers. Keys are stored locally (encrypted at
rest) and never sent to any third-party service other than the specified provider.

| Key | Provider |
|-----|----------|
| `mistral_api_key` | Mistral AI (required for OCR experiments) |
| `openai_api_key` | OpenAI |
| `anthropic_api_key` | Anthropic Claude |

### Python environment

View the current venv status, installed packages, and actions:
- **Setup** — create or re-create the venv
- **Rebuild** — reinstall all dependencies
- **Upgrade** — upgrade packages to latest compatible versions

### AI backend

Configure the default AI provider and model. If no provider is selected,
Glossa Lab uses Ollama (local) if running, or prompts to configure a provider.

---

## 14. Advanced Usage

### Data flow in study graphs

When nodes are connected by edges, the framework passes each completed node's
output to its downstream neighbors as:

```python
# kwargs received by downstream experiment's run():
kwargs["upstream_results"] = {
    "node_id_of_parent": { ...result dict... }
}
```

Use this to chain analysis steps — e.g. run Positional Profile Analysis on a
corpus, then pass the `profiles` list to Symbol Clustering to compare results
against known archetypes.

### Custom experiments (plugin pattern)

See `backend/glossa_lab/experiments/CONTRIBUTING.md` for the full guide.

Key points:
1. Drop a `.py` file in `backend/glossa_lab/experiments/`
2. Inherit from `ExperimentBase`
3. Define all required class vars including `params_schema`
4. Click **Reload** in the Experiments tab

### Node registry API

Get the params schema for any node type:
```
GET /api/v1/node-registry/experiment/{id}
GET /api/v1/node-registry/pipeline/{id}
```

### Seeding custom studies

Add entries to `_SEEDS` in `backend/glossa_lab/study_seeds.py`. Seeds are
upserted on every restart — user-created studies are never affected.

### Research context in AI chat

The **🔬 Research** context mode injects a comprehensive system prompt with:
- Current sign assignments and confidence levels
- Corpus profile data (T/I/M rates for key signs)
- Formula structure (PREAMBLE → CORE ROOT → CASE MARKER → CATEGORY MARKER → TERMINAL)
- Next research steps

This is the most powerful mode for Indus Script research.

---

## 15. Example Workflows

### Workflow A: Analysing a new corpus

1. **Corpora** → **+ New Corpus** → paste your symbol sequences as a JSON array of arrays.
2. Copy the corpus UUID from the Corpora tab.
3. **Study Builder** → select the **Positional Profile Analysis** seed study.
4. Click the node → **Inspector** → paste your UUID into the **Corpus ID** field.
5. Optionally set `min_count` (default 5) and `top_n` (default 100).
6. **💾 Save** → **▶ Run Study**.
7. View the per-symbol I/M/T rate profiles in the run results panel.
8. Go to **Reports** to open the saved JSON file.

### Workflow B: Running the Indus structural analysis

1. **Study Builder** → select **Indus Structural Atlas**.
2. Click **▶ Run Study** — the two nodes run in order (atlas → kandles_bias).
3. The atlas node completes in ~1 min; kandles_bias shows as `skipped` (CLI-only).
4. To run kandles_bias: open the **Terminal**, paste the CLI command from the experiment card.
5. Open **Reports** to view both output files.
6. Use **📊 Compose** to select both reports and export a combined PDF.

### Workflow C: Validating methodology with Ugaritic

1. **Study Builder** → select **Ugaritic Anti-Circularity Benchmark**.
2. **▶ Run Study** — both nodes run in ~30 seconds each.
3. The result panel shows:
   - `ugaritic_vs_hebrew`: cross-language hill-climbing accuracy
   - `ugaritic_proper_benchmark`: circularity inflation quantification
4. Click **✨ AI** to ask the AI to interpret the findings.
5. Create a **Hypothesis** from the Hypothesis Tracker linking to this study.

### Workflow D: AI-assisted research

1. Open **AI Chat** → select **🔬 Research** context.
2. Ask: _"What should we work on next for Indus decipherment?"_
3. The AI will suggest targeted analyses based on the current research state.
4. If it proposes running an experiment, approve the action card.
5. After it runs, ask the AI to interpret the new results.
6. Use `/compress` periodically to keep the context window manageable.

---

## 16. Troubleshooting

### Backend shows "Offline" in the health badge

- Check the tray icon — click **Start** if it shows as stopped.
- Open the Logs panel to see the error.
- Try: `setup-os.cmd` in a terminal to restart everything.

### Experiments tab is empty

- The backend may not have discovered experiments yet. Click **Reload** in the Experiments tab.
- Check that `backend/glossa_lab/experiments/*.py` files exist and have no syntax errors.

### Study Builder palette is empty

- Verify the backend is running and the Experiments / Pipelines APIs return data.
- Check the browser console for network errors.

### OCR experiments fail

- Ensure `mistral_api_key` is set in Settings → API Keys.
- OCR experiments must be run via the CLI in the Terminal, not from the Study Builder Run button.

### AI chat shows "AI error"

- If using Ollama: verify Ollama is running (`ollama list` in Terminal).
- If using a cloud provider: verify the API key is set in Settings.
- Try switching models via the model picker dropdown in the chat header.

### Context window fills up quickly

- Use `/compress` to summarise the conversation.
- Switch to a model with a larger context window (e.g. `mistral-nemo:latest` via Ollama).
- Start a new chat session for unrelated questions.

### Reports show "Popup blocked"

- Allow popups for `localhost:8001` in your browser settings.
- Or click **Open in new tab instead** to view the report directly.

---

_This guide is a living document. Update it whenever new features are added,
workflows change, or new experiments are registered._
