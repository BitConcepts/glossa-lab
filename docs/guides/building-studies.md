# Building Studies in Glossa Lab

## What is a Study?

A Study is a **visual DAG (directed acyclic graph)** that defines a research workflow
by connecting experiments, corpora, and analyses into a sequence.

Studies are for high-level research organization. A study:
- Chains multiple experiments together
- Tracks provenance (which corpora and experiments produced which results)
- Can be saved, cloned, and shared
- Maintains a research narrative via the Collaboration panel

## Opening the Study Builder

**Studies** in the sidebar → open the canvas → drag nodes from the left palette.

## Node types

| Node | What it does | Config |
|---|---|---|
| **Corpus** | Declares a corpus data source | Select corpus ID from Corpora tab |
| **Experiment** | Runs a registered experiment | Select experiment ID + set params |
| **Pipeline** | Queues an async job | Select pipeline ID + params |
| **Graph Experiment** | Runs a visual graph experiment | Select graph experiment ID |
| **AI Analysis** | Sends upstream context to Glossa AI | Custom prompt |
| **RAG Query** | Semantic search over reports/notebooks | Query string, top-K |
| **Note** | Documentation annotation | Free text |
| **Report** | Links to an existing report file | Filename |
| **Hypothesis** | Links to or creates a Hypothesis record | Hypothesis ID or title |

## Building a study step-by-step

### 1. Create a new study

Studies panel → **+ New Study** → enter name and description.

### 2. Add a corpus node

Drag **Corpus** from the palette to the canvas.
In the Inspector (right panel), enter the corpus ID from the Corpora tab.
The corpus node passes its `corpus_id` downstream.

### 3. Add an experiment node

Drag **Experiment** and select the experiment from the dropdown.
Set any parameters in the Inspector.
Draw an edge from the Corpus node to the Experiment node.

### 4. Connect results to further analysis

Draw edges left-to-right. Upstream results flow as kwargs into downstream nodes:
- `corpus_id` from a Corpus node becomes a param in the next Experiment
- Result dicts from experiments merge into the kwargs of downstream nodes

### 5. Run the study

Click **Run Study** in the Study Builder toolbar.
Node execution is streamed: each node lights up as it runs.
Results appear in the Reports tab and Jobs panel.

## Example study: NW Semitic analysis

```
[Corpus: NW Semitic test1]
         |
         v
[Experiment: fuls_writing_system_comparison]
         |
         v
[Experiment: fuls_rtl_decipher]        (graph experiment — 5 seeds, GPU)
         |
         v
[AI Analysis: "Interpret the RTL corrected mapping results"]
         |
         v
[Hypothesis: "NW Semitic test1 is syllabic LTR-corrected"]
```

## Example study: Geez anchor convergence

```
[Corpus: Geez Genesis]
         |
         v
[Graph Experiment: geez_decipher]      (split, LM, SA, consistency)
         |
         v
[AI Analysis: "Was anchor-amplification validated?"]
         |
         v
[Report: geez_anchor_convergence.csv]
```

## Connecting nodes

Click and drag from a node's right handle to another node's left handle.
To delete an edge: right-click the edge → Delete, or select it and press Delete.

**Independent branches run in parallel** (H10.3 — nodes with no data dependency
between them are dispatched simultaneously).

## Study execution order

The Study Builder respects the DAG topology:
1. Source nodes (Corpus, no inputs) run first
2. Nodes whose all upstream dependencies are complete run next
3. Independent nodes at the same level run in parallel
4. Terminal nodes (no outputs) run last

## Saving and cloning studies

**Save**: auto-saved on every edit.
**Clone**: Studies panel → ⋮ → Duplicate.
**Export**: Studies panel → ⋮ → Export → saves as `.glossa-study.json`.
**Import**: Studies panel → Import → opens file picker.

## Collaboration

Click **Messages** in the Study Builder toolbar to open the collaboration panel.
Pin important findings, attach notes to specific results, mention team members.

## Hypotheses

Add a **Hypothesis** node to formally register a testable claim linked to this study.
Hypotheses appear in the Hypotheses panel with status: active / confirmed / refuted.

Set status after experiment results confirm or refute the claim:
```
[Experiment: geez_decipher] → [Hypothesis: anchor-amplification validated?]
```

## Programmatic access

```python
from glossa_lab.api.studies import run_study
import asyncio

# Run a study by ID and get results
result = asyncio.get_event_loop().run_until_complete(
    run_study("your_study_id")
)
print(result["completed"], "nodes completed")
```
