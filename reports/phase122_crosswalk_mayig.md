# Phase-122 — Parpola↔Mahadevan Crosswalk v1 + mayig Corpus Integration

Date: 2026-10-08. Branch `phase/122-crosswalk-mayig`. Builder:
`backend/scripts/phase122_build_crosswalk_mayig.py` (deterministic;
re-runs reproduce the data files byte-identically). Statistics:
`reports/phase122_crosswalk_mayig_results.json`.

## 1. Crosswalk v1

Artifacts: `data/crosswalks/parpola_mahadevan_crosswalk_v1.csv` /
`.json`; loader `backend/glossa_lab/data/parpola_mahadevan_crosswalk_v1.py`.

**Canonical basis.** The map of record is
`data/crosswalks/canonical_sign_registry.csv` (sha256
`8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`,
unchanged). Spec 018 (Phase-119) §A2 names this registry the program's
primary cross-system map, and its appendix A.4 explicitly **rejects**
`backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json` as
canonical: at design time it covered only 131 of 284 attested M signs
and inverted several high-frequency assignments relative to the
registry (under v2, P385 — the dominant terminal — receives 0 tokens).
v2 is therefore used in v1 only as a labelled *source*, never as the
map of record. This phase's data confirms A.4 independently (below).

**Sources** (every row carries its source):

| source id | document | pairs asserted |
|---|---|---|
| `canonical_registry` | `data/crosswalks/canonical_sign_registry.csv` (`mahadevan_ids` per Parpola row) | 372 |
| `mayig_features` | mayig/indus-valley-script-corpus `features/*.json` `mahadevan_graphemes` (author's cross-match vs Parpola 1982 allographs / Wells 2015; MIT) | 372 |
| `crosswalk_v2` | `mahadevan_parpola_crosswalk_v2.json` (per-entry sources cite e.g. Parpola 1994 App. B) | 171 |
| `candidates_unadmitted` | `mahadevan_parpola_crosswalk_candidates.json` (spec 004 WS2 held candidates — no explicit source; number-identity inference) | 220 (219 new pairs + 1 duplicate of a core pair) |

Published sources checked for additional crosswalk evidence: Wells
1998 MA thesis and Wells 2006 PhD thesis (scanned-image PDFs, no
machine-readable P↔M table extractable in this phase — the Wells
cross-match enters via `mayig_features`, whose README states the
Wells 2015 matching); Bhaskar et al. 2024 (article + ESM — no sign
crosswalk table; ESM13 is an object catalogue, used for §3 overlap);
Parpola 2010 Helsinki lecture (no extractable P↔M table).

**Confidence rubric (frozen for v1).** high = attested by BOTH
`canonical_registry` and `mayig_features` (two independent structured
maps); medium = exactly one of those two, uncontradicted; low =
`crosswalk_v2`-only or candidate-only. Conflicts are flagged
independently of confidence.

**Size and breakdown.**

- 766 rows = **762 mapping pairs + 4 unmapped-P rows**
  (P000 — the damage/lost-material marker — P225, P261, P358: no M
  asserted by any source).
- P signs covered **412**; M signs covered **412**; M signs attested
  in sources but claimed by no P: **0**.
- Relation types (no forced 1:1): **1:1 — 352; one-to-many — 78;
  many-to-one — 66; many-to-many — 266; unmapped — 4.**
- Confidence: **high 372, medium 0, low 390** (171 v2-only + 219
  candidate-only). Medium is empty because the registry and mayig
  pair sets turned out *identical* (372/372) — two independent
  structured maps agree pair-for-pair; every core pair is therefore
  doubly attested.
- **Conflicts: 383 pairs across 209 P signs**, kept on both sides and
  flagged, never silently resolved. Essentially all are the
  documented crosswalk_v2 inversions: v2 is close to a number-identity
  map (M001↔P001, M002↔P002, …) and 168 of its 171 pairs contradict
  the registry+mayig consensus (e.g. P001 = M012 in registry/mayig,
  M001 in v2), and those v2 pairs in turn flag the 215 consensus
  pairs they contradict. The candidates file's 4 pre-recorded
  unresolved conflicts (M045; M006/M039/M062; M087; M047) are carried
  verbatim in the JSON's stats.

**Marshall numbering (note only).** Kondratov's tables (Phase-121)
use MARSHALL numbers — a third numbering. No Marshall↔M/P pairs were
extractable from sources on `main` in this phase; v1 asserts no
Marshall rows. Recording Marshall evidence remains open for a future
phase working from the Kondratov tables directly.

## 2. mayig integration

Artifacts: `data/corpus_layers/mayig_cisi_layer_v1.json` (+
`_meta.json`); loader `backend/glossa_lab/data/mayig_layer.py`;
builder above, following the Phase-115/116 converted-layer pattern
(builder script + build metadata + per-inscription provenance).

- Source: https://github.com/mayig/indus-valley-script-corpus,
  commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb` (2025-04-16),
  per `PROVENANCE.md` entry 1 in the 2026-10-08 deep-sweep downloads.
- **License: MIT** — LICENSE file in the source repo root ("MIT
  License, Copyright (c) 2024 Michael Carlson"), verified from the
  file at acquisition. Because mayig is MIT, the converted layer is
  **committed** as a first-class corpus layer under
  `data/corpus_layers/` — unlike the ICIT converted layers, whose
  source terms keep them in the gitignored `corpora/downloads/` tree
  with statistics only published. (Precedent: the Phase-44
  mayig-derived `indus_cisi_corpus.json` is likewise committed.)
- **Totals: 179 inscriptions (179 CISI objects, all Mohenjo-daro
  M-series), 1,003 sign tokens, 182 distinct P signs.** Every record
  is keyed by **CISI object ID** (e.g. `M-1`) with its side ID
  (e.g. `M-1A`), description, source file, token sequence in source
  order, and per-token mayig feature vectors.
- Lineage: an *independent transcription lineage* vs the held
  Holdat / Mahadevan IC77 / ICIT extractions, over a substantially
  overlapping artefact population — deduplicate by CISI artefact ID
  before any independence claim (carried in the layer metadata).

## 3. Coverage through crosswalk v1

Resolution uses the crosswalk's usable map (high+medium pairs —
registry∪mayig; v2-only and candidate-only pairs excluded). A token
is *clean* if its P sign resolves to exactly one M, *ambiguous* if
it resolves to >1 M (an honest split/merge), *unmapped* if none.

- **Tokens (1,003): clean 768 (76.6%), ambiguous 202 (20.1%),
  unmapped 33 (3.3%).**
- **Inscriptions (179): clean 42, partial 137, none 0** — every
  inscription has at least one resolvable token.
- The registry-only map gives identical figures (its pair set
  equals the mayig pair set).
- Top failure modes: **P122** (76 tokens, ambiguous — the
  stroke-numeral sign maps to several M signs), **P086** (35,
  ambiguous — tree sign), **P000** (19, unmapped — damage marker,
  correctly has no M counterpart), P123 (13, ambiguous), P332 and
  P268 (11 each, ambiguous). Ambiguity is concentrated in
  high-frequency signs whose M-side granularity is finer than
  Parpola's allograph grouping — a property of the two sign lists,
  not a data defect.

## 4. CISI Vols. 1–2 overlap (by CISI object ID)

**What was compared.** mayig's 179 object IDs against the CISI
object identifiers obtainable now, per basis:

| basis | IDs in basis (M-prefixed) | mayig objects found | coverage |
|---|---|---|---|
| CISI Vol. 1 IA scan, djvu OCR regex `M-\d+` | 160 | 12 | 6.7% |
| CISI Vol. 2 IA scan, djvu OCR regex `M-\d+` | 444 | 8 | 4.5% |
| Bhaskar et al. 2024 ESM13 catalogue, CISI ID column | 1,197 (of 2,001 total) | **179** | **100%** |
| Phase-116 keyed ICIT layer, `cisi` field | 1,745 (of 4,070 total) | **179** | **100%** |
| Union of all bases | 1,983 | **179** | **100%** |

**Limits, stated plainly.** The two scan-OCR bases are *not*
catalogues: the CISI plates are images, the djvu OCR only catches
IDs that happen to appear in recognised text, so 12/179 and 8/179
are extraction artefacts, not overlap measurements — they are
reported to show exactly why OCR extraction cannot answer this
question. The meaningful obtainable bases are the two structured
ID lists (Bhaskar ESM13, an updated CISI-derived object catalogue;
and the keyed ICIT layer's `cisi` field, Mahadevan-concordance
lineage): **all 179 mayig objects are present in both** — mayig's
artefact population is entirely contained in the CISI-catalogued
population, as expected for a CISI hand-digitisation. **Phase E
will produce the full structured CISI catalogue table from the
Vol. 1–2 scans; the definitive Vol. 1–2 overlap figure awaits
that table.** This section is provisional and says so.

## 5. Explicit non-claims

- **No positional comparison study was run** in this phase (that is
  a future spec); no positional/profile statistics were computed
  through the crosswalk.
- **No anchor-status implications** follow from any crosswalk row,
  coverage figure, or overlap figure. Anchors and tiers are
  untouched.
- The crosswalk is a **working v1 with stated confidence, not an
  adjudication of sign identity**; conflicted pairs are published
  with both sides and their sources.
- The CISI overlap in §4 is provisional (see its limits); no
  independence claim is made for mayig beyond the transcription-
  lineage note in §2.

## 6. Verification

- New tests: `backend/tests/test_phase122_crosswalk_mayig.py`
  (8 tests: row-field integrity, headline counts, no-forced-1:1,
  both-sides conflicts, honest unmapped, layer totals/keying,
  coverage recomputation, overlap record).
- Full backend suite and foundation check: see the Phase-122
  entries in `LEDGER.md` / `glossa-indus/LEDGER.md` for the recorded
  results of this run.

**AI disclosure:** execution recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per constitution §VI.
