# Spec 052 / Phase-437 — Outcome record (EXECUTED 2026-10-24 — INCONSISTENT)

> ## EXECUTED — 2026-10-24
>
> Executed under the frozen amended Spec 052
> contract (freeze digest
> `83658949f9988990ddf265735f099e96d4c6c59c93eed66d4a648d3e8307c019`),
> as **Phase-437**, under the owner's execution
> order of 2026-10-24, after the freeze merged
> to `main` (PR #249, merge commit `2bff5857`)
> and after OSF registration **7cu23** was
> approved and public. Outcome: **INCONSISTENT**
> — both pattern conditions hold on the primary
> population, so under the amendment's re-pointed
> semantics the Farmer pattern (no dedicated
> final sets, no opening formula) is **absent**
> in the Shakti corpus layer, and the
> "artefact of the Soviet dataset" caveat on the
> parent claim **widens**. The claim
> `farmer_sproat_witzel_2004_manual_001` stands
> **contradicted** exactly as recorded; this
> outcome moves no verdict and is not a verdict
> on the Farmer–Sproat–Witzel thesis.

## Headline

Dataset: **the Shakti corpus layer
(CISI-compilation lineage)** — corpus SHA-256
`345241b1…`, row grades `02394241…`, read from
the restricted local store only. Battery:
**NB-1 (Spec 052 amendment as frozen)**.
Lineage limit: the Shakti layer is a
CISI-tradition compilation, a distinct lineage
from the Soviet compilation and from
Holdat/M77, but its editions cover
substantially the same excavated objects:
agreement is cross-compilation robustness, not
independent discovery.

Step 0 passed all four amended gates, in order,
fail-closed (step0-record.md): the corpus pin
recomputed exactly; the primary population
reproduced the freeze-recorded counts exactly
(**3,045 rows; 11,805 tokens; 557 distinct
signs**); the battery run twice under seed
43052 produced identical outputs; thinness
cleared (2,068 sequences of length ≥ 3; 90
classifiable signs).

## Primary run (NB-1)

Census: 3,045 sequences; 103 of length 1
(counted, entering no count); 2,942 of
length ≥ 2 (B = 2,942); 2,068 of length ≥ 3;
90 classifiable signs (N ≥ 20) of 557.

- **Condition F (dedicated final sets): HOLDS.**
  7 TERMINAL_STRONG signs — **034, 413, 501,
  503, 692, 817, 820** — against a
  permutation-null chance level of **0**: in
  999 within-sequence permutations (seed
  43052), not one produced a single
  TERMINAL_STRONG sign (null min/median/max
  0/0/0). The observed count exceeds the
  chance level, and the set is non-empty.
- **Condition O (opening formula): HOLDS.**
  The most frequent opening bigram is
  **(400, 740)**, recurring **179** times over
  B = 2,942 (dominance 0.0608), against a
  chance level of **76** occurrences (null
  min/median/max 64/68/84; dominance chance
  level 0.0258) and above the frozen count
  floor of 10. 735 distinct opening bigrams.
- Full per-sign quantities (N, I, T, M with
  rates for all 90 classifiable signs; counts
  for every one of the 557 signs, the 467 below
  the floor marked TOO THIN for this
  population) are in
  `reports/phase437_results.json` and
  `reports/phase437_report.md`, published
  before this outcome word per the headline
  rules. Moderate sets: terminal 8, initial 3,
  medial 21. INITIAL_STRONG: 10 signs;
  MEDIAL_STRONG: 38 signs.

**Outcome: INCONSISTENT** (amendment §6: F and
O both hold). Positional structure of the kind
the thesis denies — dedicated final-position
signs and a fixed inscription-opening pair,
each beyond what sign order alone produces
under the frozen null — is present in this
compilation. The asymmetry with the Soviet
outcome becomes the recorded finding.

## Sensitivity run (same prominence)

Sensitivity population: 5,131 rows; 17,216
tokens; 707 distinct signs; 4,293 sequences of
length ≥ 2; 2,889 of length ≥ 3; 111
classifiable signs under NB-1 (see the census
note in step0-record.md: sign 540; the freeze
census's 112 counted total occurrences).

- **F: HOLDS** — 9 TERMINAL_STRONG signs (the
  primary seven plus 091 and 104) against a
  chance level of 0 (null min/median/max
  0/0/1).
- **O: HOLDS** — the same opening bigram
  (400, 740), 235 occurrences over B = 4,293
  (dominance 0.0547), against a chance level
  of 95 (null min/median/max 80/86/107).

**Sensitivity outcome: INCONSISTENT** — the
same word as the primary run; the outcome is
not grade-sensitive.

## Appends (§4.2)

The outcome text of this record was appended,
as a dated entry
(`spec052_outcome_append_2026_10_24`), in the
same words, to the parent claim's record
(`farmer_sproat_witzel_2004_manual_001`) and
to each of the three fragments' records
(`…_critique_0001`, `…_critique_0002`,
`without_kings…_language_0001`). All four
records stand **contradicted** / SETTLED
exactly as before; the appends are purely
additive. Post-append SHA-256 of the parent
record:
`1177182f8e9c2f31e17f16d597d84307829b98918182870a13121891d7555a6b`
(the claim itself unchanged; the file's hash
moves by dated appends, as with the 2026-10-22
audit note).

Durability note: the extracted-claims
generator (`glossa-indus/scripts/indus_claims.py`)
regenerates the store wholesale and, before
this execution, carried over only enumerated
fields — a regeneration would have stripped
these appends (CI on this execution's PR
caught exactly that, in-tree, via the Spec 029
tests). The generator now carries over dated
append keys (a trailing `_YYYY_MM_DD` date) by
claim identity, under the same never-drop
principle as its stage, merge-state, and
status-correction carry-overs; a test in
`backend/tests/test_spec052_execution.py`
proves the preservation and fails without it.

## What this does not establish

- It does not re-open, confirm, or flip the
  parent claim's contradicted verdict, and it
  is not a verdict on the Farmer–Sproat–Witzel
  thesis (§7 limit 1). The recorded caveat
  widens; the verdict's basis in the published
  record is untouched.
- It does not show what language the signs
  encode, any sign's reading, or that every
  part of the sign system is linguistic
  (§7 limit 2). It says nothing about
  conditional entropy (§7 limit 4).
- It does not reproduce or rehabilitate the
  Phase-43 battery: NB-1 is a new battery,
  defined at the amendment, and no Phase-43
  quantity was computed or compared.
- It does not execute or design arm B, which
  stays trigger-armed and outside this spec.
- The strong sets are properties of this
  compilation's numbering and segmentation;
  the lineage limit in the headline governs
  every reading of them.

## Landing record

Appended at merge (append-only): PR number,
merge commit, CI conclusions, and the
foundation check as measured on the merged
tree.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
