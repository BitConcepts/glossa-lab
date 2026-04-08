# Glossa Lab — User Guide

> **Version**: current `main` branch  
> **Last updated**: automatically — update this file whenever the UI or workflow changes.

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

- Upload and manage symbol-sequence corpora
- Run statistical analysis **experiments** (positional profiles, entropy, Zipf, NWSP, clustering…)
- Compose experiments into **study graphs** with data-flow edges
- Run complete studies and inspect results per-node
- View, filter, and compose **reports** from experiment output
- Ask **Glossa AI** to interpret results, suggest next steps, or navigate the UI

### Architecture at a glance

```
Corpus (symbol sequences)
    ↓
Experiment (statistical analysis, parametric)
    ↓  ↑ upstream_results propagated through graph edges
Study (DAG of experiments + pipelines, saved to DB)
    ↓
Reports (JSON output files, composable)
    ↓
AI Chat / Hypothesis Tracker (interpretation layer)
```

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

| Section    | Items |
|------------|-------|
| Workspace  | Studies · Study Builder · Experiments · Corpora · Reports |
| Analysis   | Entropy · Signs · Timeline |
| Research   | Hypotheses · Notebooks · Citations |
| AI         | AI Tools |
| System     | Status · Pipelines · Jobs · Settings |

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

**Path**: sidebar → Experiments

Experiments are the analysis units of Glossa Lab. Each experiment is a Python
class in `backend/glossa_lab/experiments/` that inherits from `ExperimentBase`.

### Experiment types

| Category         | Examples |
|-----------------|---------|
| **Analysis**    | Positional Profile Analysis, Symbol Clustering, Indus Structural Atlas |
| **Validation**  | Ventris Validation, Fuls Progression Benchmark, Writing System Progression, Ugaritic Benchmarks |
| **Research**    | Contact Zone Analysis, Luwian KL Scoring |
| **Experiments** | Linear A Circularity Suite, Kandles Bias Comparison |
| **Data Extraction** | OCR — Bigram Tables, OCR — Inscription Sequences (requires Mistral key) |

### Running an experiment

**From the Experiments tab**: click **▶ Run** on any experiment card.
A dialog appears to enter parameters (if any).

**From the Study Builder**: drag an experiment onto the canvas, set its params
in the Inspector panel, then click **▶ Run Study**.

**Via the API**:
```
POST /api/v1/experiments/{id}/run
Content-Type: application/json
{"kwargs": {"corpus_id": "your-corpus-id", "min_count": 5}}
```

**CLI-only experiments**: some experiments (OCR, Kandles Bias, Linear A
Circularity) take too long to run in-process. Their node will show as `skipped`
in the Study Builder. Use the **Terminal** and run the CLI command shown on the
experiment card.

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

**Path**: sidebar → Study Builder

The Study Builder is the central workflow interface. It lets you compose
experiments and pipelines into a **directed acyclic graph (DAG)** where results
flow from upstream nodes to downstream nodes.

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

### Building the graph

1. **Drag** an item from the Palette onto the canvas.
2. **Click** a node to select it — the Inspector panel appears on the right.
3. **Set parameters** in the Inspector. For experiments with configurable params
   (e.g. `corpus_id`, `min_count`), typed form fields appear.
4. **Connect nodes** by dragging from one node's handle to another to create
   a data-flow edge. The upstream node's result is passed to the downstream
   node as `upstream_results`.
5. **Save** (💾 button or Ctrl+S equivalent) to persist the graph to the database.

### Running a study

Click **▶ Run Study**. The backend:
1. Topologically sorts nodes (Kahn's algorithm)
2. Executes each experiment node's `run(**params, upstream_results=...)` in order
3. Passes successful results downstream via edges
4. Pipeline nodes are skipped (they require async job submission)

Results appear inline below the canvas with per-node status:
- ✅ **complete** — ran successfully; JSON result shown
- ⚠ **skipped** — CLI-only experiment or pipeline node
- ❌ **error** — exception raised; error message shown

### Inspector — editing node parameters

Clicking a node opens the Inspector panel (right side). For experiments with
a `params_schema`, you see typed form fields:

- **String fields**: text input (e.g. Corpus ID — paste the UUID from the Corpora tab)
- **Integer/Number fields**: number input with optional min/max
- **Boolean fields**: checkbox toggle

Changes update the node's params immediately. **Save** to persist.

For experiments with no configurable params (most research experiments), the
Inspector shows "No configurable parameters" — they are self-contained.

### Pre-built study seeds

On every server restart, Glossa Lab upserts 8 curated seed studies:

| Study | Purpose |
|-------|---------|
| **Positional Profile Analysis** | Quick-start: single-node, set `corpus_id` in Inspector |
| **Symbol Clustering** | Positional profile → clustering pipeline |
| **Indus Contact Zone & KL Scoring** | Contact zone + KL scoring + structural atlas |
| **Indus Structural Atlas** | Full Indus entropy/Zipf/NWSP analysis |
| **Ugaritic Anti-Circularity Benchmark** | Validates proper train/test split method |
| **Writing System Progression** | 5-tier progression benchmark (Fuls method) |
| **Linear A Anti-Circularity Suite** | 7-experiment circularity analysis (CLI-only) |
| **OCR Pipeline** | OCR extraction nodes (requires Mistral key, CLI-only) |

You can modify these freely — seeds are re-applied on restart but only for
their own stable IDs, never overwriting user-created studies.

### AI features in Study Builder

| Button | Action |
|--------|--------|
| **✨ AI** | AI summarizes the current study: abstract, hypothesis, highlights, next steps |
| **✨ Design** | Opens AI Chat with the study as context; AI suggests experiments and improvements |

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
| **Corpus** | Select a corpus — AI has access to its metadata |
| **Experiment** | Select an experiment — AI can discuss its results |
| **Study** | Select a study — AI can discuss its graph and findings |
| **🔬 Research** | Full Indus research context: sign profiles, formula structure, corpus statistics, next steps |

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
