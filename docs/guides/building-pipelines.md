# Building Pipelines in Glossa Lab

## What is a pipeline?

Pipelines are **long-running async background jobs** that appear in the Jobs panel
and can be submitted via the UI or API. They are distinct from experiments:

| | Experiments | Pipelines |
|---|---|---|
| Run mode | Synchronous (blocks caller) | Async (submitted to engine queue) |
| UI trigger | Experiments → Run | Jobs → Submit new job |
| Code location | `experiments/` | `pipelines/` |
| Base class | `ExperimentBase` | Registered in `catalog.py` |
| Output | Returns dict immediately | Polled via job results |

Pipelines are best for: corpus analysis that takes minutes, multi-corpus batch jobs,
OCR extraction, or anything you want to queue and check later.

---

## Pipeline file structure

```python
# backend/glossa_lab/pipelines/my_pipeline.py
from __future__ import annotations
import logging
from glossa_lab.engine import register_pipeline

_log = logging.getLogger(__name__)


@register_pipeline("my_pipeline")
def run(params: dict, db=None) -> dict:
    """Execute the pipeline. Called by the engine when the job is claimed.

    Args:
        params:  Job params dict from the submitted job (from UI or API).
        db:      Database instance (optional; may be None in CLI mode).

    Returns:
        Result dict saved to job_results table.
    """
    text_id = params.get("text_id", "")
    _log.info("my_pipeline starting | text_id=%s", text_id)

    # --- your analysis here ---
    result = {"processed": True, "text_id": text_id}

    _log.info("my_pipeline done")
    return result
```

## Registering in the catalog

Add an entry to `backend/glossa_lab/catalog.py` so the UI can discover the pipeline
and pre-fill its default parameters:

```python
# In catalog.py, add to the PIPELINE_CATALOG list:
{
    "id":          "my_pipeline",
    "label":       "My Analysis Pipeline",
    "group":       "Analysis",
    "description": "What this pipeline does.",
    "inputs":      "text_id: str",
    "outputs":     "result dict saved to job_results",
    "default_params": {"text_id": ""},
    "needs_lm":    False,
    "registered":  True,
    "module":      "glossa_lab.pipelines.my_pipeline",
},
```

## Submitting a pipeline job

From the UI: **Jobs** → Submit new job → select `my_pipeline` → fill params → Submit

From the API:
```bash
curl -X POST http://localhost:8001/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{"name": "My Analysis", "pipeline": "my_pipeline", "params": {"text_id": "abc123"}}'
```

From Python:
```python
import httpx
httpx.post("http://localhost:8001/api/v1/jobs", json={
    "name": "My Analysis",
    "pipeline": "my_pipeline",
    "params": {"text_id": "abc123"},
})
```

## GPU/parallel execution in pipelines

Follow the same rules as experiments (H10):

```python
from glossa_lab.experiments._parallel import run_seeds_parallel, compute_device_label

@register_pipeline("batch_decipher")
def run(params: dict, db=None) -> dict:
    _log.info("Compute device: %s", compute_device_label())

    # Parallel seeds (GPU via BigramScorer when CuPy installed)
    def _one_seed(seed, flat, lm):
        from glossa_lab.pipelines.decipher import decipher
        return decipher(flat, lm, seed=seed, ocp_weight=0.0).get("proposed_mapping", {})

    mappings = run_seeds_parallel(_one_seed, list(range(10)), flat, lm)
    return {"n_mappings": len(mappings)}
```

## Typed port contracts

Pipeline functions receive a `params` dict. Document expected keys and output keys
in the catalog entry's `inputs` and `outputs` fields. This enables the Study Builder
to show type hints in the Inspector panel.

Supported output value types: `str`, `int`, `float`, `bool`, `list`, `dict`.
Complex Python objects (LanguageModel, numpy arrays) must be serialized before
returning from `run()`.

## Engine lifecycle

1. Job submitted via API → `create_job(status="pending")`
2. Engine loop polls every 2 s → `claim_pending_job()`
3. Engine imports the pipeline module and calls `run(params, db)`
4. Result stored via `store_result(job_id, result)`
5. Job status set to `completed` or `failed`
6. UI Jobs panel shows result; click **Results** to view

## Existing pipelines

See `backend/glossa_lab/pipelines/` for reference implementations:

| Pipeline | Description |
|---|---|
| `block_entropy.py` | Shannon entropy H1–H4 per corpus |
| `positional.py` | Sign positional profile (I/M/T rates) |
| `cooccurrence.py` | Sign co-occurrence matrix |
| `nwsp.py` | NWSP word-structure metric (Fuls 2013) |
| `decipher.py` | SA decipherment engine (also used by experiments) |
| `beam_decipher.py` | Beam-search decipherment |
| `structural_fingerprint.py` | Script typology fingerprint |
