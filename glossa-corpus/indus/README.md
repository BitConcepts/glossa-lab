# glossa-corpus/indus — ICIT-Scale Indus Text Corpus Reconstruction

## Purpose
Reconstruct an ICIT-scale Indus inscription corpus from free and purchasable
public sources, without requiring direct ICIT database access.

ICIT target scale: 4,537 inscribed objects · 5,509 texts · 19,616 sign occurrences
Sign list target: Wells 676-sign list (3-digit codes, ICIT diplomatic encoding)

## Branch
`corpus/icit-scale-reconstruction`

## Architecture — Four Layers (never silently collapsed)
1. **Source layer** — raw asset, fetch hash, source URL, rights class, provenance chain
2. **Diplomatic layer** — lossless ICIT-compatible encoded text: `+NNN-NNN-NNN+`, `000`, `++`
3. **Graphemic layer** — canonical sign IDs via M77/Parpola/Wells/Fuls crosswalk; allograph
   relations stored as typed links, never flattened
4. **Interpretive layer** — semantic/administrative hypotheses with attribution and confidence;
   never treated as authoritative translation

Object model:
```
OBJECT → SURFACE → IMAGE_ASSET + TEXT_WITNESS → SIGN_INSTANCE → SIGN_TYPE ↔ SIGN_RELATION
```

## Directory Structure
```
sources/               ← per-source raw download directories
  indian-culture/      ← Indian Culture portal (india-gov-cultural)
  rmrl/                ← Roja Muthiah Research Library / Indus Research Centre
  penn-museum/         ← Penn Museum CC BY 4.0 CSV + images
  met-open-access/     ← The Met Open Access API (CC0)
  cleveland-art/       ← Cleveland Museum of Art Open Access API (CC0)
  museums-of-india/    ← Museums of India repository (discovery only)
  internet-archive/    ← Internet Archive IIIF (derivative, OCR only)
  mayig-cisi/          ← mayig/indus-valley-script-corpus (MIT, GitHub)
  cisi/                ← STUB: CISI vols 1–3.3 (purchasable, €520 bundle)
  wells-books/         ← STUB: Wells Archaeopress + Oxbow (purchasable, ~£60)
  national-museum-nd/  ← STUB: National Museum New Delhi (permissions required)
  asi-archive/         ← STUB: ASI Archive (permissions required)
  british-museum/      ← STUB: British Museum / BM Images (licensed)
staging/               ← objectization working area; quarantine/
canonical/             ← released object records (JSONL + sign graph)
  objects.jsonl
  sign_instances.jsonl
  sign_crosswalk.json
  rights_register.json
exports/               ← final release packages
  indus_open.jsonl          ← rights-cleared CC0/CC-BY (ML/RAG)
  indus_research.jsonl      ← research-use cleared
  indus_icit_format.json    ← ICIT-format diplomatic sequences
```

## Acquisition Scripts
```
backend/scripts/corpus_indus_acquire_free.py   ← all free-source acquisition
backend/scripts/corpus_indus_objectize.py      ← source → object record pipeline
backend/scripts/corpus_indus_normalize.py      ← diplomatic + graphemic normalization
backend/scripts/corpus_indus_export.py         ← release package builder
backend/scripts/corpus_indus_status.py         ← coverage/quality dashboard
backend/scripts/corpus_indus_acquire_cisi.py   ← STUB for CISI volumes
backend/scripts/corpus_indus_acquire_wells.py  ← STUB for Wells books
backend/scripts/corpus_indus_acquire_permissions.py  ← STUB for permissions batch
```

## Data Loader
`backend/glossa_lab/data/indus_corpus_v2.py` — drop-in replacement for the synthetic
prototype, loading from `exports/indus_research.jsonl`.

## Rights Summary
| Source | Rights Class | ML Training | Redistribution |
|---|---|---|---|
| Met Open Access | CC0 | Yes | Yes |
| Cleveland Art | CC0 | Yes | Yes |
| Penn Museum metadata | CC BY 4.0 | Yes | With attribution |
| Penn Museum images | noncommercial-educational | Research only | No |
| mayig-cisi | MIT | Yes | With attribution |
| Indian Culture | india-gov-cultural | Research | Permission required |
| RMRL | rmrl-research | Research | Contact required |
| Museums of India | india-museum-restricted | No | No |
| Internet Archive | internet-archive-derivative | After verification | No |
| CISI (stub) | purchasable-research | Internal only | No |
| National Museum ND | permission-required | TBD | TBD |
| ASI Archive | permission-required | TBD | TBD |
| British Museum | licensed | TBD | TBD |

## Citations
All sources cited in `CITATIONS.md` per H18 (section I.*).
