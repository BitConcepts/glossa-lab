# Spec 054 — Step-0 record (Phase-438 execution, amended run)

Execution act under the frozen amended contract
(freeze digest
`d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57`;
OSF registration `8spvf`, approved and public at
this run). Executed 2026-10-24 under the owner's
execution order of 2026-10-24 (08:07 EDT, "Do
phase 438"), at the execution venue (program VM).
Execution base: `9b5ebaf8` (main at the order:
PR #363 merged).

**Verdict: STEP 0 CLOSED — gate G2 (strict
corpus identification and pin) FAILED; the run
closes STRICT CORPUS NOT PINNABLE. No positional
quantity was computed in either arm.**

## Gates (amendment §6, in order)

- **Gate G1 — pin checks (draft 0.1): PASS.**
  Every freeze §2 pin recomputed at execution
  against the tree: the claim store after the
  falsifier append
  `938174b0dee14169a5340c9299c73f4eb5b997377f8198a146ef611e73924050`
  ✓; `outputs/phase43_all.json` `78a6c219…` ✓;
  the positional companion record `0e546962…` ✓;
  crosswalk v1 JSON `4e7559df…` ✓ and CSV
  `3d0b9ef1…` ✓; the anchors file `df0cf620…` ✓;
  the recovered register `ea161e47…` ✓. The
  freeze digest itself re-asserted from
  `freeze.json`: `d85f6ace…` ✓.
- **Gate G2 — strict corpus identification and
  pin (draft 0.3): FAIL.** The mechanical
  identification attempt, recorded in full
  below, found no layer that is the corpus the
  Phase-43 record names. The run closes here;
  gates G3–G5 were NOT REACHED, and no count
  produced toward a verdict exists.
- **Gate G3 — thinness: NOT REACHED.**
- **Gate G4 — second arm runnability: NOT
  REACHED.** (Arm 2's layer was censused only
  as a C4 alternative layer — see below; its
  own gate was not evaluated.)
- **Gate G5 — determinism: NOT REACHED.** (The
  phase script itself was run twice at the
  venue and produced byte-identical records —
  results JSON SHA-256
  `c776b247489562d69d9d95862cf315e723c1dd5aacb8ad4f1ff68e1d02a9acfc`
  on both runs — a property of the record, not
  the frozen gate, which was not reached.)

## The identification attempt (gate G2)

**C3 — the reference census** (read from the
pinned Phase-43 record, `T1_1_corpus_v3`):
source "indusscript.in Firestore 'indusarrays'
(2026-05-14)"; 3,916 total records; 2,665
unique dockeys; 3,137 total sequences; 12,494
total sign instances. A layer counts as
identified only if it is that corpus and the
V3 loader's census of it reproduces these
numbers exactly.

**C1 — the V3 loader's data file.** The loader
(`backend/glossa_lab/data/indus_corpus_v3.py`)
reads exactly one file:
`glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl`.
That path was checked in this execution tree,
in the main checkout, and in every sibling
tree the machine holds (9 candidate paths):
**absent at all of them** (the whole
`glossa-corpus/indus/sources/` area is
gitignored; the main checkout's `rmrl/` folder
holds only provenance files). Run as the
programme runs it, the loader loads **0
records, 0 sequences, 0 dockeys, 0 sign
instances** — the layer cannot be exported or
pinned from it.

**C2 — database copies.** No database copy
exists in the execution tree
(`backend/data/` is gitignored and absent).
The programme database (the main checkout's
`backend/data/glossa.db`) holds 9 texts; the
only Indus entry is the synthetic prototype
("Indus Script (synthetic, Yadav 2010 / Fuls
2014)", 923 inscriptions by its own metadata,
generated from published statistics) — not
the V3 layer, and never substitutable for it.

**C4 — every other layer held, censused.**
None is the corpus the Phase-43 record names,
and none was substituted:

| Layer | Census | Why it is not arm 1 |
|---|---|---|
| `yajnadevam_inscriptions.csv` (the programme's site-attributed layer; Specs 042/045's layer of record) | 5,679 records | A different layer — the Phase-393 / Yajnadevam layer; the draft itself (§2) forbids substituting it for the V3 corpus, and its record count differs from C3's 3,916 |
| `indus_research.jsonl` (the V1 research export) | 15,508 records | A mixed-source-system export, not the Firestore reconstruction |
| mayig CISI layer v1 (`data/corpus_layers/mayig_cisi_layer_v1.json`) | 179 inscriptions / 1,003 tokens / 182 signs | The CISI compilation in Parpola numbering (Spec 019's arm) — a different compilation |
| The Holdat downloads layer (`indus_corpus 2.csv`) | 1,670 inscriptions / 7,002 tokens / 390 signs | Arm 2's layer — the other compilation; the Phase-43 record itself treats it as a different corpus (its §T4_3 cross-validation against V3) |
| The Shakti corpus layer (restricted-local; Specs 068/052's layer) | 5,704 rows (SHA-256 `345241b1…`) | A CISI-lineage compilation — a different lineage from the Mahadevan-lineage Firestore V3 layer |

## Anchors

`backend/reports/INDUS_FINAL_ANCHORS.json`
asserted byte-identical before and after the
run: SHA-256 `df0cf620…` at both readings.

## What this step-0 record is

The identification was attempted mechanically
and is recorded with its observed values, in
the same form as Spec 053's gate 0.3 record
(Phase-413, 2026-10-21), which closed on the
same observed facts for the sibling claim. The
layer's absence is a fact about the held
record, stated here — not a judgement that
the layer cannot exist elsewhere, and not a
statement about the claim, which stands
exactly as recorded with the falsifier the
freeze appended to it.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
