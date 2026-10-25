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
tests). The generator now carries over
spec outcome-append keys
(`specNNN_outcome_append_YYYY_MM_DD`) by claim
identity, under the same never-drop principle
as its stage, merge-state, and
status-correction carry-overs; a test in
`backend/tests/test_spec052_execution.py`
proves the preservation and fails without it.
The carry-over is scoped to outcome-append
keys deliberately: audit notes
(`audit_note_YYYY_MM_DD`) keep their prior
regeneration behaviour, because the Spec 029
Phase I verbatim-instance pin compares a
preserved instance against the live record
and carrying audit notes over regeneration
broke that pin in the same CI run — widening
the carry-over is a separate, separately
pinned change, not this execution's to make.
The one exact-shape pin over the corrected
fragment records (the Phase-104 correction
tests) was amended the same day, in its own
dated amendment note, to admit dated append
keys while still pinning every non-append key
exactly — the same surgical correction the
Spec 052 freeze itself applied to a live-hash
pin (freeze §8).

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

**Landed 2026-10-24.** Execution PR **#361**,
merged as merge commit
`65d0c75e92e691e596a593d0a48b21c2f8fff76a`.
CI on the merged head (`90d3a103`), run
40067100181: **7/7 jobs successful**, read
from the run's own job conclusions — Backend
tests (pytest); Frontend tests (Playwright);
Evidence Graph script smoke tests; Indus
public validation checks; Shell wrappers
(ubuntu-latest, windows-latest, macos-latest).
Three earlier runs of the PR failed, each on
a regeneration interaction the fixes in this
PR resolved (the outcome append stripped
in-tree; the Phase-104 exact-shape pin; the
Phase I verbatim-instance pin via audit-note
carry-over) — the full account is in the
durability note above and the generator's own
comments. Foundation check on the merged
tree (merge commit `65d0c75e`, run
2026-10-24 with the program's local corpora
linked in read-only): **40 checks passed,
0 failed, 8 warnings** — the warnings are the
standing caveats (site coverage, sign-numbering
crosswalks, the superseded TB corpus, the
Phase-32 inconclusive test); none touches
this spec's records. Read back from merged
`main` by API after the merge: this outcome
record, the machine record (outcome
INCONSISTENT, sensitivity INCONSISTENT, gates
PASS ×4), and the §4.2 append on the parent
record (status still contradicted) are all
present as landed.

## Correction and disclosure notes — 2026-10-25 (realignment item 2.3)

**NB-1's band provenance and threshold-robustness (RT-05).** Battery
NB-1's constants were calibrated against the exhibited Phase-43 class,
and this record should have said so at headline strength: the STRONG
band (>= 2/3) sits just below the lowest exhibited Phase-43
TERMINAL_STRONG rate (0.683), and the classifiability floor (N >= 20)
sits just below the smallest total among the exhibited signs (22). The
calibration is a consistency property, not an independent derivation.
What protects the outcome word is measured, and is recorded here from
`reports/phase437_results.json`: the seven primary TERMINAL_STRONG
rates sit at 0.750-0.967, and the next two classifiable signs sit at
0.6216 and 0.6196 — no classifiable sign lies between 0.622 and 0.750,
so the strong set, and with it condition F, is **identical at every
threshold in (0.6196, 0.75]**, including the frozen 2/3 and the
exhibited 0.683. At the Phase-43 cascade's own 0.60 threshold the
primary count would be 9 (sensitivity 11); the permutation null at
the 0.60 statistic was **not** computed in this record, and that is
stated here as an open sensitivity — it is not repaired post hoc, and
no number in this record changes.

**Outcome-word pointer (RT-28).** A reader of `spec.md` §4.1 alone
will read this outcome backwards. §4.1 as originally drafted mapped
CONSISTENT to "F and O both hold" and INCONSISTENT to "neither holds";
the owner-approved amendment (§6) deliberately re-pointed both words
— CONSISTENT = neither holds, INCONSISTENT = F and O both hold — and
`freeze.md` §6 records the re-pointing. The amendment and the freeze
record govern. Never quote §4.1 without them.

These notes are append-only: no verdict, status, or frozen text
changes.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
