# Corpus Versioning Policy — Glossa-Lab Indus Evidence Graph

## Principle

The user's curated primary corpus is **V1**. It is tracked by **acquisition date**,
not by version number. Version numbers only increment when the corpus undergoes
a **major structural change** (new sources added, sign normalization rules changed,
etc.) AND only after all initial research phases are complete.

Do NOT rename or bump to V2 during exploratory research phases.

---

## Primary Corpus: V1

```
File:      glossa-corpus/indus/exports/indus_research.jsonl
Loader:    backend/glossa_lab/data/indus_corpus_v2.py
Label:     V1  (the file is named v2.py for historical reasons — semantically it IS V1)
Status:    Active primary corpus
```

### V1 Acquisition History (date-tracked)

| Date | Event | Records | Notes |
|---|---|---|---|
| 2026-05-14 | Initial multi-source build | 15,514 | mayig-CISI (179) + Penn Museum (7,515) + Met Open Access (4,904) + Cleveland (4) + indusscript.in (2,906) |
| future | TBD — only on major addition | — | Bump date only |

### V1 source breakdown

```yaml
sources:
  - id: mayig_cisi
    count: 179
    type: multi-sign inscription sequences (Parpola numbering)
    license: MIT
    acquired: 2026-05-14

  - id: penn_museum
    count: 7515
    type: seal/artifact metadata + accession numbers
    license: CC BY 4.0
    acquired: 2026-05-14
    notes: "No image URLs. Penn Museum IP-blocks all programmatic image access."

  - id: met_open_access
    count: 4904
    type: museum metadata
    license: CC0
    acquired: 2026-05-14

  - id: cleveland_art
    count: 4
    type: museum metadata
    license: CC0
    acquired: 2026-05-14

  - id: indusscript_m77
    count: 2906
    type: Mahadevan M77 sign sequences (indusscript.in Firestore, dockey-keyed)
    license: user permission
    acquired: 2026-05-14
```

---

## Supplementary Corpus: Firestore Direct Reconstruction

```
File:    glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl
Loader:  backend/glossa_lab/data/indus_corpus_firestore.py
Label:   firestore_2026-05-14
Status:  Supplementary external source (NOT the user's primary corpus)
```

This is a direct reconstruction from the indusscript.in Firestore `indusarrays`
collection dump, acquired 2026-05-14 with user permission. It contains 3,137
clean sign sequences from 2,665 Mahadevan concordance entries after filtering
*NNN supplementary signs.

**Why it is NOT V2:**
- It is derived from a third-party database (indusscript.in / RMRL)
- The user's primary corpus (V1) already contains the same data
  (indusscript-m77 source records in indus_research.jsonl)
- V2 would require adding new sites, new sources, or correcting major errors

---

## Version Bump Rules

V2 may only be created when ALL of the following are true:

1. Initial research phases (Phase-41 through Phase-44+) are complete
2. A major structural change is made:
   - New excavation site data added (e.g., CISI Vol.2 Harappa data)
   - Sign normalization scheme changed
   - New catalog crosswalk incorporated
   - Major duplicate resolution performed
3. The user explicitly approves the version bump

### What does NOT trigger a version bump:
- Adding more analysis scripts
- Running new experiments on existing data
- Fixing *NNN filter bugs (these are load-time filters, not corpus changes)
- Downloading new papers into glossa-indus/raw/papers/

---

## Corpus Integrity Checksums (V1, 2026-05-14)

```
indus_research.jsonl: tracked via provenance.yaml in each source directory
primary_record_count: 15,514
sign_instances_with_sequences: ~12,494 (indusscript-m77 source)
```
