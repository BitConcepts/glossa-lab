# Building Experiments and Pipelines in Glossa Lab

## Overview

Glossa Lab has two layers for running computational analyses:

1. **Experiments** — standalone Python classes that run a specific analysis and save results to `reports/`
2. **Study Pipelines** — visual graph-based workflows that chain experiments, corpora, and analyses into a full research study

---

## Experiments

### What is an Experiment?

An experiment is a Python class in `backend/glossa_lab/experiments/` that:

- Implements a `run()` method that returns a `dict`
- Saves its results as a JSON file to `reports/`
- Registers itself in the discovery registry via the `ExperimentBase` class (optional but recommended)

### Anatomy of an Experiment

```python
# backend/glossa_lab/experiments/my_analysis.py

from glossa_lab.experiment_base import ExperimentBase
from pathlib import Path
import json
from datetime import datetime, timezone

REPORTS = Path(__file__).resolve().parent.parent.parent.parent / "reports"

class MyAnalysis(ExperimentBase):
    id             = "my_analysis"          # must be unique, kebab-case
    name           = "My Analysis"
    category       = "Validation"           # shown in the UI palette
    description    = "What this experiment does."
    estimated_time = "~1 min"
    command        = "python -m glossa_lab.experiments.my_analysis"

    def run(self, **kwargs) -> dict:
        # --- your analysis here ---
        result = {"answer": 42}

        # Always save to reports/
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        out = REPORTS / f"my_analysis_{ts}.json"
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")

        return result


# Standalone runner (for CLI invocation)
if __name__ == "__main__":
    from glossa_lab.cli_bridge import run_with_reporting
    run_with_reporting("my_analysis", "My Analysis", MyAnalysis().run, verbose=True)
```

### Running Experiments

**From the UI**: Go to **Experiments** → find your experiment → click **Run**

**From the CLI**:
```bash
python -m glossa_lab.experiments.my_analysis
```

**From Glossa AI**: Ask "Run my_analysis experiment"

**From a Study pipeline**: add an Experiment node and connect it to your corpus

### Accessing Corpus Data

```python
# Load the Indus corpus (primary Glossa Lab corpus)
import json
from pathlib import Path
R = Path(__file__).resolve().parent.parent.parent.parent / "reports"
data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
inscriptions = [i["sequence"] for i in data["inscriptions"] if i.get("sequence")]
# inscriptions = [["066", "069", "090"], ["003", "069"], ...]
```

### Using the Decipherment Engine

```python
from glossa_lab.pipelines.decipher import LanguageModel, decipher
from glossa_lab.data.old_hebrew import _HEBREW_LINES

# Build Hebrew language model
hw = []
for line in _HEBREW_LINES:
    for w in line.split("."):
        w = w.strip()
        if w: hw.append(w.split())
lm = LanguageModel([s for w in hw for s in w], inscriptions=hw)

# Run SA mapping inference
flat_tokens = ["066", "069", "090", "112", ...]  # your cipher tokens
result = decipher(
    flat_tokens, lm,
    seed=42,
    max_iterations=12000,
    restarts=10,
    cipher_inscriptions=[[...]],  # word-split cipher
    surjective=True,              # many cipher signs → fewer target signs
    anchors={"066": "m"},         # verified assignments (optional)
)
mapping = result["proposed_mapping"]  # dict: sign -> consonant
```

### GPU/CPU Policy

Per `AGENTS.md` rule H10:

```python
# Always prefer GPU
try:
    import cupy as xp
    _GPU = xp.cuda.is_available()
except ImportError:
    import numpy as xp
    _GPU = False

if not _GPU:
    import logging
    logging.getLogger(__name__).info("GPU unavailable — using NumPy CPU path")
```

For CPU-bound loops (multiple seeds), use parallel execution:

```python
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

def run_one_seed(seed):
    return _run_mapping(words, lm, seed)

n_seeds = 20
with ProcessPoolExecutor(max_workers=min(n_seeds, os.cpu_count() or 4)) as ex:
    futures = [ex.submit(run_one_seed, s) for s in range(n_seeds)]
    results = [f.result() for f in futures]
```

---

## Study Pipelines (Visual Graph Editor)

### What is a Study?

A Study is a visual graph of nodes connected by edges, defining a research workflow. Each node can be:

- A **corpus** — the data source
- An **experiment** — a computation step
- A **pipeline** — an async job
- A **result viewer** — inspection of outputs

### Opening the Study Builder

Click **Studies** in the sidebar to open the graph canvas.

### Node Types

| Node | Description |
|---|---|
| **Corpus** | Input data. Select from registered corpora. |
| **Experiment** | Runs a registered experiment. Config: experiment ID, optional params. |
| **Pipeline** | Queues a job (async). |
| **Script** | Runs inline Python code. |
| **Report** | Generates a PDF report. |
| **Note** | Documentation node (no execution). |

### Connecting Nodes

Draw edges from left to right to define data flow:

```
[Corpus] ──> [Structural Analysis] ──> [Mapping Inference] ──> [Report]
```

Independent branches run in parallel (per AGENTS.md H10.3).

### Example: NW Semitic Analysis Pipeline

```
[NW Semitic Test1 Corpus]
         |
         v
[fuls_nw_semitic_benchmark]  ──> [fuls_writing_system_comparison]
         |
         v
[fuls_rtl_corrected]  ──> [fuls_constraint_space]
         |
         v
[fuls_nw_semitic_decipher_run]
         |
         v
[generate_fuls_nw_semitic_report]
```

### Running a Study

1. Build the graph in the canvas
2. Click **Run Study** (play button)
3. The bottom panel auto-opens to the Jobs tab to show progress
4. Click any job to see detailed results

### Saving and Sharing

Studies are saved automatically to the database. To export:
- Click the **Export** button to download a JSON representation
- Share the JSON file; others can import it via **Import Study**

---

## Writing Custom Analysis Scripts

For one-off analyses, use the **Terminal** in the bottom panel or ask Glossa AI to run a script:

```python
# Example: compute entropy of a corpus
import json
import math
from pathlib import Path
from collections import Counter

R = Path("reports")  # relative to repo root when run via Terminal
data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
inscriptions = [i["sequence"] for i in data["inscriptions"] if i.get("sequence")]
tokens = [s for ins in inscriptions for s in ins]
counts = Counter(tokens)
total = sum(counts.values())
H1 = -sum((c/total) * math.log2(c/total) for c in counts.values())
print(f"H1 = {H1:.4f} bits  (N={len(counts)} distinct signs, {total} tokens)")
```

Save results to `reports/` for them to appear in the Reports panel.

---

## Experiment Best Practices

1. **Always save to `reports/`** with a timestamped filename
2. **Log at INFO level** so results appear in the Logs panel
3. **Return a `dict`** from `run()` — this is what the UI displays on job completion
4. **Use `_safe()` for any text going into PDFs** (see `generate_fuls_nw_semitic_report.py`)
5. **Parallelize** seed loops using `ProcessPoolExecutor`
6. **Check for GPU** before all numerical batch operations
7. **Register via `ExperimentBase`** so the experiment appears in the UI palette and Glossa AI can reference it by ID

---

## File and Directory Layout

```
backend/
  glossa_lab/
    experiments/         ← your experiment .py files go here
      fuls_rtl_corrected.py
      fuls_constraint_space.py
      ...
    data/               ← corpus data modules
    pipelines/          ← SA engine, Kandles, etc.
    api/                ← FastAPI endpoints
  generate_fuls_*.py   ← standalone report generators

reports/               ← all experiment JSON outputs (auto-created)

docs/
  user-manual.md        ← this file's companion
  guides/
    building-experiments.md  ← this file
```

---

*Glossa Lab — BitConcepts Research Programme*
