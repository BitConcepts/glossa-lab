# Spec 054 — Step-0 record (Phase-438 RE-EXECUTION, amended run)

Execution act under the frozen amended contract
(freeze digest
`d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57`;
OSF registration `8spvf`, approved and public).
**Re-execution** of Spec 054 under its existing
freeze, executed 2026-10-25 under the owner's
execution order of 2026-10-25 (15:00 EDT, "Do
your recommended actions" — the recommendation
being this re-execution on the recovered
indusarrays layer). The first execution
(2026-10-24, `step0-record.md` / `outcome.md`)
closed **STRICT CORPUS NOT PINNABLE** at gate
G2 because the layer could not be located;
that verdict stands exactly as executed. This
record is the second execution's own step-0
record; it revises nothing in the first.

**Venue and tree.** TRISTEN-DESKTOP (WSL). The
execution tree is a git worktree of the owner's
desktop clone at the first execution's base,
`9b5ebaf88736c7fa79550e3e4b050824ff791e25`, with
the frozen instrument files
(`backend/scripts/phase438_yadav_opening_closing.py`,
SHA-256
`b5930e27eb44a6b922f3bc30fdf7fc7d89956fa465d1bb5e93d020f186bfb1b6`,
and
`backend/glossa_lab/experiment_graph_phase438.py`)
taken from PR #364's head / current `main` —
byte-identical to the first execution's
instrument, which did not exist at the base
commit (it was authored in the execution PR).
The script's `_MAIN_REPO`
(`~/workspace/glossa-lab`) was satisfied by a
symlink to the desktop clone, in which the V3
loader's data file sits **in place** at its
canonical relative path; the file was read
read-only and was not copied, moved, or
ingested by this run. The frozen script's
embedded `EXECUTION_DATE` string ("2026-10-24")
and its report header's order reference are
the frozen instrument's own text, unmodified;
the actual date and order are as stated above
and in `outcome-run2.md`.

**Verdict: ALL STEP-0 GATES PASSED — the run
proceeded to the battery. Outcome: NOT
SUPPORTED (precedence §5.5(3)); full record in
`outcome-run2.md` and
`reports/phase438_results_run2.json`.**

## Gates (amendment §6, in order)

- **Gate G1 — pin checks (draft 0.1): PASS.**
  Every freeze §2 pin recomputed at execution
  against the tree: the claim store after the
  falsifier append `938174b0…` ✓;
  `outputs/phase43_all.json` `78a6c219…` ✓;
  the positional companion record `0e546962…`
  ✓; crosswalk v1 JSON `4e7559df…` ✓ and CSV
  `3d0b9ef1…` ✓; the anchors file `df0cf620…`
  ✓; the recovered register `ea161e47…` ✓.
  The freeze digest itself re-asserted from
  `freeze.json`: `d85f6ace…` ✓.
- **Gate G2 — strict corpus identification and
  pin (draft 0.3): PASS.** The identification
  is recorded in full below. The layer is the
  corpus the Phase-43 record names, and the
  V3 loader's census of it reproduces the
  reference census exactly.
- **Gate G3 — thinness: PASS.** Arm 1 carries
  2,267 sequences of length ≥ 3 (frozen line
  30) and 103 classifiable signs (frozen line
  10).
- **Gate G4 — second arm runnability: PASS.**
  The Holdat downloads layer was identified at
  the main checkout's path and pinned by
  SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
  — byte-identical to the VM main checkout's
  copy of the same file (hash compared
  cross-venue before the run). Its census
  (1,670 inscriptions / 7,002 tokens / 390
  signs) matches the first execution's C4
  census of this layer exactly. Arm 2 carries
  36 classifiable signs (frozen line 10). The
  crosswalk pins are G1's.
- **Gate G5 — determinism: PASS.** The frozen
  decision computation, run twice over the
  pinned inputs with seed 44054, produced
  identical canonical records (both arms'
  battery records and the decision record).

## The identification (gate G2)

**C3 — the reference census** (read from the
pinned Phase-43 record, `T1_1_corpus_v3`):
source "indusscript.in Firestore 'indusarrays'
(2026-05-14)"; 3,916 total records; 2,665
unique dockeys; 3,137 total sequences; 12,494
total sign instances.

**C1 — the V3 loader's data file.** The loader
(`backend/glossa_lab/data/indus_corpus_v3.py`)
reads exactly one file:
`glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl`.
At this venue the file is **present** — in the
desktop clone, at that canonical relative
path, where it has sat since its acquisition
on 2026-05-14 (intake-pinned in place
2026-10-25, PR #393). The loader's census of
it (the loader module's own reconstruction):
**3,916 records; 2,665 unique dockeys; 3,137
sequences; 12,494 sign instances** — the C3
reference census reproduced exactly. The
identified layer is pinned two ways: the
source file's SHA-256
`073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578`
(equal to the intake pin), and the canonical
export pin
`e90fd7ce41121529…` over the 3,137 exported
sequences.

*Independent corroboration.* The Route 2
census tool (`route2_verify_census.py`, a
rule-for-rule mirror of the loader plus the
Phase-43 positional profiles), run against the
same in-place file before the phase script
ran, judged it against the frozen T1_1 census
as gates V1–V4: **V1 lines 3,916 ✓; V2 census
(2,665 / 3,137 / 12,494) ✓; V3 full top-20
sign frequencies ✓; V4 terminal fractions
(267 → 0.038; 72 → 0.259) ✓ — ALL PASS.**

**C2 — database copies.** No database copy
exists in the execution tree. The desktop
clone's programme database
(`backend/data/glossa.db`) holds 13 texts; its
Indus entries are the Dholavira and Harappan
seal datasets and the synthetic prototype
("Indus Script (synthetic, Yadav 2010 / Fuls
2014)") — not the V3 layer, and never
substitutable for it. Identification rests on
C1, as the frozen gate provides.

**C4 — every other layer held at this venue,
censused.** None is the corpus the Phase-43
record names, and none was substituted: the
site-attributed layer
(`yajnadevam_inscriptions.csv`, 5,679
records); the V1 research export
(`indus_research.jsonl`, 15,508 records); the
mayig CISI layer v1 (179 inscriptions / 1,003
tokens / 182 signs); the Holdat downloads
layer (1,670 inscriptions / 7,002 tokens /
390 signs — arm 2's layer). The Shakti layer
is held on the programme VM, not at this
venue; it is a CISI-lineage compilation in
either case, not arm 1.

## Permission basis (recorded, not resolved)

The layer is the owner's held export of the
indusscript.in Firestore 'indusarrays'
collection, captured 2026-05-14 (the loader's
own citation records "Acquired 2026-05-14 with
user permission via Firebase REST API"). RMRL
did not reply to the programme's enquiries of
2026-10-08 or 2026-10-21. This run records
that basis as it stands; it neither settles
nor enlarges it. The layer's content is not
committed to this repository: the results
record carries counts, sets, and hashes only,
and row-level corpus data appears in no
output — the same discipline as the first
execution.

## Anchors

`backend/reports/INDUS_FINAL_ANCHORS.json`
asserted byte-identical before and after the
run: SHA-256 `df0cf620…` at both readings.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
