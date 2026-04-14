# Adding Corpora to Glossa Lab

## Two ways to add a corpus

### Option A: Upload via the UI (recommended for most corpora)

**Corpora** tab → **+ Upload / import corpus** → paste or import your text.

This stores the corpus in SQLite and makes it immediately available to all experiments,
pipelines, and the CorpusReader atomic node in the Experiment Builder.

Set:
- **Name**: human-readable label
- **Type**: `ancient`, `linguistic`, `dna`, `code`, `random`, `other`
- **Reading direction**: `LTR`, `RTL`, or **Auto-detect** (uses Ashraf 2018 entropy method)
- **Tokenisation**: space-separated, line-per-token, or character-level

After upload, click **Edit** → **Auto-detect** to automatically infer reading direction.

### Option B: Built-in data module (for reference corpora, always available)

Built-in corpora are Python modules in `backend/glossa_lab/data/`. They load without
a DB upload, work offline, and are auto-seeded into the DB on first startup.

Use this for: linguistic reference corpora, decipherment targets, controlled benchmarks.

---

## Creating a built-in data module

### Step 1: Create the Python module

```python
# backend/glossa_lab/data/my_corpus.py
"""My Corpus — brief description.

Tokens/signs:  ~50,000
Language:      My Language
Script:        My Script
Source:        Publication or collection
Reading dir:   ltr  (or rtl)
"""
from __future__ import annotations
from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).parent / "my_corpus_files"  # optional, if data files needed

# Required metadata dict
METADATA: dict[str, Any] = {
    "name":           "My Corpus (My Language)",
    "language":       "My Language",
    "script":         "My Script",
    "writing_type":   "alphabetic",  # or: abjad, abugida-syllabic, logo-syllabic, etc.
    "reading_direction": "ltr",      # or: rtl, unknown
    "status":         "deciphered",  # or: undeciphered, partially_deciphered
    "period":         "1st century CE",
    "source":         "My Source Publication",
    "geo_centroid":   [35.0, 36.0],  # [lat, lon] for diffusion timeline experiments
    "date_range_bce": [100, -2000],  # [date_BCE_start, date_BCE_end] (negative = CE)
    "language_family": "Semitic",
    "note": "Optional longer description.",
}


def get_corpus_symbols() -> list[str]:
    """Return a flat list of all tokens (symbols/signs) in the corpus.

    Each element is one token: a character, sign ID, or word depending on the script.
    For syllabic/alphabetic scripts, each element is one sign character.
    For logographic scripts, each element is one sign ID string.
    """
    # Option 1: hardcoded list (for small corpora)
    return ["a", "b", "c", "a", "b", "a", ...]

    # Option 2: load from file (for larger corpora)
    text = (_DATA_DIR / "my_corpus.txt").read_text("utf-8")
    return text.split()


def get_corpus_inscriptions() -> list[list[str]]:
    """Return word-level inscriptions (list of word lists).

    Each inner list is one word (sequence of signs).
    Used by: LanguageModel (word bigrams), Ashraf direction detection,
             CorpusSplitter, and the LMBuilder atomic node.
    """
    # Each line/sentence is a "word" (sequence of signs)
    text = (_DATA_DIR / "my_corpus.txt").read_text("utf-8")
    return [line.split() for line in text.splitlines() if line.strip()]


def corpus_statistics() -> dict[str, Any]:
    """Return summary statistics (used by corpus_seeder.py metadata)."""
    syms  = get_corpus_symbols()
    inscs = get_corpus_inscriptions()
    return {
        "n_tokens":   len(syms),
        "n_words":    len(inscs),
        "n_distinct": len(set(syms)),
    }
```

### Step 2: Register in corpus_seeder.py

Add your corpus name to `BUILT_IN_CORPORA` and add a `_load_corpus` handler:

```python
# backend/glossa_lab/corpus_seeder.py

BUILT_IN_CORPORA = [
    "ugaritic",
    "linear_b",
    "hebrew",
    "indus_synthetic",
    "sumerian_ur3",
    "geez",
    "my_corpus",   # ← add here
]

def _corpus_name(corpus_id: str) -> str:
    return {
        ...
        "my_corpus": "My Corpus (My Language)",  # ← add here
    }.get(corpus_id, corpus_id)


def _load_corpus(corpus_id: str) -> dict | None:
    ...
    elif corpus_id == "my_corpus":
        from glossa_lab.data.my_corpus import (
            get_corpus_symbols, get_corpus_inscriptions, corpus_statistics
        )
        flat  = get_corpus_symbols()
        inscs = get_corpus_inscriptions()
        stats = corpus_statistics()
        return {
            "corpus_type":      "ancient",
            "content":          flat,
            "reading_direction": "ltr",  # or rtl / unknown
            "metadata": {
                "source":        "My Source Publication",
                "n_words":       stats["n_words"],
                "n_distinct":    stats["n_distinct"],
                "writing_type":  "alphabetic",
                "language":      "My Language",
                "inscriptions":  inscs,  # enables Ashraf direction auto-detection
            },
        }
```

The corpus is now auto-seeded into the DB on next backend startup and appears in:
- Corpora tab
- CorpusReader node dropdown in the Experiment Builder
- `BuiltinCorpus` atomic node (add `"my_corpus"` to the param description)

### Step 3: (Optional) Add to BuiltinCorpus node

If you want the corpus available via the `BuiltinCorpus` atomic node (no DB corpus ID
required), add a case to `_builtin_corpus()` in `experiment_graph.py`:

```python
elif name == "my_corpus":
    from glossa_lab.data.my_corpus import get_corpus_symbols, get_corpus_inscriptions
    flat = get_corpus_symbols(); seqs = get_corpus_inscriptions()
```

And add `"my_corpus"` to the `BuiltinCorpus` node's params description string.

---

## Reading direction

Set `reading_direction` in the corpus metadata:
- `"ltr"` — left-to-right (default)
- `"rtl"` — right-to-left (sequences will be reversed by the DirectionNormalizer node)
- `"unknown"` — use Auto-detect in the UI or via the detect-direction API

The DirectionNormalizer atomic node and `corpus_utils.normalise_sequences()` function
both respect this field and reverse word sequences when needed.

---

## Corpus data model

When stored in the DB, a corpus has:

| Field | Type | Description |
|---|---|---|
| `id` | str | UUID |
| `name` | str | Human-readable label |
| `corpus_type` | str | `ancient`, `linguistic`, `dna`, `code`, `random`, `other` |
| `content` | list[str] | Flat list of tokens |
| `symbol_set` | list[str] | Sorted unique tokens |
| `alphabet_size` | int | `len(symbol_set)` |
| `reading_direction` | str | `ltr`, `rtl`, or `unknown` |
| `metadata` | dict | Arbitrary key-value metadata |
| `created_at` | str | ISO 8601 timestamp |

The `metadata.inscriptions` key (list of lists) is read by the detect-direction
endpoint to run the Ashraf entropy test.

---

## Verifying your corpus

After adding, restart the backend and check:

```bash
# Check corpus is in the DB:
curl http://localhost:8001/api/v1/texts | python -m json.tool | grep "my_corpus"

# Run direction detection:
CORPUS_ID=<your-id>
curl -X POST http://localhost:8001/api/v1/texts/$CORPUS_ID/detect-direction \
  -H "Content-Type: application/json" \
  -d '{"update_field": true}'
```

Or from the UI: Corpora → find your corpus → Edit tab → Auto-detect.
