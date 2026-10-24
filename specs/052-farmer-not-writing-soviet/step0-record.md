# Spec 052 — Step-0 record (Phase-437 execution, amended run)

Execution act under the frozen amended contract
(freeze digest
`83658949f9988990ddf265735f099e96d4c6c59c93eed66d4a648d3e8307c019`;
OSF registration `7cu23`, approved and public at
this run). Executed 2026-10-24 under the owner's
execution order of 2026-10-24 (00:41 EDT), at the
execution venue (program VM, restricted-local data
area). The corpus layer is **the Shakti corpus
layer (CISI-compilation lineage)**; its source
rows were read from the restricted local store
only and appear in no product.

**Verdict: STEP 0 PASSED — all four amended
gates, in order, fail-closed.** The battery ran.

## Gates (amendment §5)

- **Gate A — corpus pin: PASS.** Corpus layer
  `sanitized_corpus.json` SHA-256
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`
  (1,570,041 bytes); row grades
  `shakti_row_grades_2026-10-22.csv` SHA-256
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`
  (5,704 rows) — both recomputed at execution to
  the freeze §3 values. The freeze digest itself
  re-asserted from `freeze.json`:
  `83658949…` ✓.
- **Gate B — population reproduction: PASS.**
  Under Spec 068's step-0 limb (analyzable iff
  some symbol is not `000`; tokens exclude `000`;
  sequence = symbols with `000` removed), the
  primary population (analyzable
  documented-lineage rows) reproduces the
  freeze-recorded counts exactly: **3,045 rows;
  11,805 tokens; 557 distinct signs**. The
  sensitivity population (documented-lineage +
  undocumented-corroborated analyzable rows)
  likewise reproduces its freeze-recorded counts:
  5,131 rows; 17,216 tokens; 707 distinct signs.
- **Gate C — determinism: PASS.** The battery
  implementation, run twice over the pinned
  layer with seed 43052, produced identical
  outputs (canonical-JSON comparison of the full
  battery records, null distributions included).
  A full second execution of the phase script
  after the run reproduced every quantity
  byte-identically.
- **Gate D — thinness (NB-1.9): PASS.** Primary
  population: 2,068 sequences of length ≥ 3
  (gate line 30); 90 classifiable signs
  (gate line 10) — the freeze-recorded length
  census (2,942 of length ≥ 2; 2,068 of
  length ≥ 3; 103 of length 1; 90 classifiable)
  reproduced exactly.

## Census note (recorded openly, no gate turns on it)

The freeze §3 length census records **112**
classifiable signs for the sensitivity
population; NB-1 as frozen counts **111**. The
difference is one sign, **540**: it carries 22
total occurrences but only 13 in sequences of
length ≥ 2 — 9 of its occurrences are as
single-sign inscriptions. Under NB-1.2/NB-1.3,
length-1 sequences enter no count, so
N(540) = 13 < 20 and the sign is not
classifiable; the freeze census figure counted
total occurrences. The primary count (90) is
identical under both readings, and gate D
governs the primary only. The battery as run
follows the frozen NB-1 definitions; the
difference is recorded here and in the machine
record (`census_notes`), not repaired.

## Anchors

`backend/reports/INDUS_FINAL_ANCHORS.json`
asserted at SHA-256 `df0cf620…` before the run
and byte-identical after it. This act moves no
anchor.

## Graph registration

The Phase-437 experiment-graph node
`IndusPhase437FarmerNB1`
(`backend/glossa_lab/experiment_graph_phase437.py`,
registered in `experiment_graph.py`) was
registered and verified present in the node
registry **before** the run, per the spec §6
deliverables (H15/H23).

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
