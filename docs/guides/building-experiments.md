# Building Experiments in Glossa Lab

## Architecture overview

```
Atomic Nodes (palette)             generic computational primitives
       ↓  compose into
Graph Experiments (JSON)           reusable study-specific compositions
       ↓  appear alongside
ExperimentBase subclasses (Python) complex monolithic analyses
       ↓  combined in
Studies (visual graph)             full research workflows
```

**Atomic nodes** are generic — they work on any corpus, language, or data.
**Graph experiments** are specific to a research question but reusable across studies.
**ExperimentBase** subclasses are the Python equivalent: subroutines studies call.

---

## Option A: Graph Experiment (visual, no-code)

Build experiments in **Experiment Builder** using atomic nodes from the palette.
Saved as JSON in `backend/glossa_lab/experiments/graphs/`.
Automatically appears in the Experiments list and any Study.

### Atomic node palette

| Category | Nodes |
|---|---|
| Sources | CorpusReader, BuiltinCorpus, BuiltinLM, StaticValue |
| Transforms | FreqCounter, Filter, Merger, CorpusSplitter, DirectionNormalizer |
| Analysis | PositionalProfiler, EntropyCalc, Clusterer, ZipfFitter, KLDivergence, NgramCounter, AnchorGenerator, Comparator |
| Decipherment | LMBuilder, SADecipher, ConsistencyScorer, BenchmarkScorer |
| Outputs | JSONExport, PassResult |
| Experiments | ExperimentWrapper (run any ExperimentBase) |

### Example: SA decipherment graph

```
[BuiltinCorpus: geez]
        |
[CorpusSplitter: 75/25]
   |train_sequences          |test_sequences
[LMBuilder]             [SADecipher: n_seeds=5, ocp_weight=0]
        |lm ─────────────────|lm
                             |all_mappings
                       [ConsistencyScorer]
                             |consistency_per_sign
                         [JSONExport]
```

SADecipher runs 5 seeds in parallel on the GPU (when CuPy is installed).
`ocp_weight=0.0` enables the BigramScorer GPU fast path.

### Design rule: nodes must be generic

Nodes in the palette must be corpus-agnostic and study-agnostic.
Study-specific choices (which corpus, which language model) live in the
graph JSON, not in the node implementation itself.

---

## Option B: Python ExperimentBase (code)

For complex analyses that cannot yet be expressed as atomic node graphs.

### Minimum viable experiment

```python
# backend/glossa_lab/experiments/my_analysis.py
from __future__ import annotations
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from glossa_lab.experiment_base import ExperimentBase
from glossa_lab.experiments._parallel import compute_device_label, run_seeds_parallel

_log     = logging.getLogger(__name__)
_REPORTS = Path(__file__).resolve().parent.parent.parent.parent / "reports"


class MyAnalysis(ExperimentBase):
    id             = "my_analysis"      # unique snake_case
    name           = "My Analysis"
    category       = "Analysis"
    description    = "What this experiment does."
    estimated_time = "~2 min"
    results_file   = "reports/my_analysis.json"

    # params_schema lets the UI render form controls for parameters
    params_schema = {
        "type": "object",
        "properties": {
            "n_seeds": {
                "type": "integer", "default": 5, "minimum": 1,
                "description": "SA seeds run in parallel",
            },
        },
    }

    def run(self, **kwargs) -> dict:
        n_seeds = int(kwargs.get("n_seeds", 5))
        _log.info("Starting | device=%s | n_seeds=%d",
                  compute_device_label(), n_seeds)

        # --- your analysis here ---
        result = {"n_seeds": n_seeds, "answer": 42}

        ts  = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        out = _REPORTS / f"my_analysis_{ts}.json"
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result


# Terminal entry point: run_cli() registers a Job in the UI (H12.3 mandatory)
if __name__ == "__main__":
    MyAnalysis().run_cli()
```

### H12 rules — mandatory

**H12.1 ExperimentBase required** — every experiment file MUST define at least one
`ExperimentBase` subclass. Standalone scripts that bypass it are forbidden.

**H12.2 params_schema** — define JSON Schema for all configurable parameters so the
UI can render form controls.

**H12.3 run_cli() for terminal** — the `if __name__ == "__main__":` block MUST call
`run_cli()`, not `run()`. `run_cli()` registers the job in the Jobs panel.

**H12.4 Parallel seeds** — SA seed loops MUST use `run_seeds_parallel()` from
`glossa_lab.experiments._parallel`. A plain `for seed in range(N):` loop is forbidden.

**H12.5 GPU fast path** — do NOT set `ocp_weight > 0` or `use_word_bigrams=True`
unless scientifically necessary. These bypass the BigramScorer GPU path (50-200x slower).
Document deliberate bypasses with a comment explaining why.

---

### Parallel seed execution (correct pattern)

```python
from glossa_lab.experiments._parallel import run_seeds_parallel, compute_device_label


# Top-level function — must be picklable (no closures over complex objects)
def _one_seed(seed: int, flat: list, lm) -> dict:
    from glossa_lab.pipelines.decipher import decipher
    return decipher(
        flat, lm,
        seed=seed,
        max_iterations=10_000,
        restarts=8,
        ocp_weight=0.0,        # 0 = GPU BigramScorer fast path (H12.5)
        use_word_bigrams=False, # False = GPU fast path (H12.5)
        surjective=True,
    ).get("proposed_mapping", {})


class MyDecipherExperiment(ExperimentBase):
    id = "my_decipher"
    # ...

    def run(self, **kwargs) -> dict:
        n_seeds = int(kwargs.get("n_seeds", 10))
        # GPU is used automatically via BigramScorer when CuPy is installed
        _log.info("Compute device: %s", compute_device_label())

        lm           = ...   # LanguageModel
        cipher_flat  = [...] # flat token list

        # Runs n_seeds in parallel via ThreadPoolExecutor
        # GPU (CuPy BigramScorer) is used automatically if available
        mappings = run_seeds_parallel(
            _one_seed, list(range(n_seeds)),
            cipher_flat, lm
        )
        return {"n_successful_seeds": len(mappings)}
```

### Forbidden patterns

```python
# FORBIDDEN: sequential seed loop (H12.4)
for seed in range(n_seeds):
    m = _run_mapping(corpus, lm, seed)
    results.append(m)

# FORBIDDEN: ocp_weight bypasses GPU (H12.5, unless justified with a comment)
result = decipher(flat, lm, ocp_weight=1.0, ...)

# FORBIDDEN: standalone __main__ without run_cli() (H12.3)
if __name__ == "__main__":
    MyExperiment().run(verbose=True)   # WRONG
```

---

## Accessing corpus data

```python
# User-uploaded corpus (from DB)
from glossa_lab.database import get_db
import asyncio
db   = get_db()
text = asyncio.get_event_loop().run_until_complete(db.get_text(corpus_id))
seqs = text["content"]          # flat list OR list of lists

# Built-in data module (always available)
from glossa_lab.data.geez import get_corpus_symbols, get_corpus_inscriptions
symbols      = get_corpus_symbols()       # flat list of tokens
inscriptions = get_corpus_inscriptions()  # list of words (each word = list)
```

## Using the decipherment engine

```python
from glossa_lab.pipelines.decipher import LanguageModel, decipher
from glossa_lab.data.old_hebrew import get_corpus_symbols, get_corpus_inscriptions

lm = LanguageModel(get_corpus_symbols(), inscriptions=get_corpus_inscriptions())

result = decipher(
    flat_cipher_tokens, lm,
    seed=42,
    max_iterations=10_000, restarts=8,
    cipher_inscriptions=word_split_cipher,
    surjective=True,
    ocp_weight=0.0,         # GPU fast path
    anchors={"066": "m"},   # optional verified assignments
)
mapping = result["proposed_mapping"]  # {cipher_sign: target_consonant}
```

## Running experiments

```bat
# From terminal (job appears in UI Jobs panel):
shell.cmd python -m glossa_lab.experiments.my_analysis

# From UI: Experiments -> My Analysis -> Run

# From Glossa AI: "Run my_analysis"

# From a Study: add Experiment node, select my_analysis
```
