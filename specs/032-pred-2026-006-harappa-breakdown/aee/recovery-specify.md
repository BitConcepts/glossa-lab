# AEE recovery — Spec 032 register (after_specify)

Register: `specs/032-pred-2026-006-harappa-breakdown/claims.json`
(F032-C01…C12). Recovery follows the Spec 029/030/031
pattern: the register is recovered honestly — atomic
rewrites, enumerations carried into boundaries
verbatim-in-substance, pairwise boundary confirmations
for every flagged pair — and the hook is re-run.
Propositions, falsifiers, and verdict rules are
unchanged throughout; no claim was split, because no
claim carried two propositions that the design states
separately — each flagged text carried one proposition
plus its own elaboration, which moved to the boundary.

## Round 1 — 2026-10-13T10:44:22Z — iterate (17 failure modes)

Artifact: `aee-after_specify-20261013T104422Z.json`
(0 claims below the 0.70 threshold).

- **Irreducibility (9):** C01, C03, C05, C06, C07,
  C08, C09, C11, C12 — texts judged to carry multiple
  independently falsifiable propositions.
- **Negation conflict (8):** C02↔C07; C03↔C04;
  C03↔C05; C03↔C07; C04↔C09; C05↔C08; C06↔C07;
  C07↔C09.

**Recovery (register 0.1-draft → 0.2-draft).** Every
flagged claim text was rewritten as a single atomic
proposition in the Spec 030/031 passing style; the
detail each text shed (the nothing-beyond clause of
C01, the table's columns in C09, the byte-identical
rule in C11, the closure names in C12, the
no-part-in-training clause of C05, the counted-and-
labelled rule in C07, the exclusivity in C08) was
carried into that claim's boundary verbatim-in-
substance. C10 was unflagged and is unchanged. For
each flagged negation pair, both claims'
`boundary_confirmation` fields now state the shared
boundary and why neither negates the other (C02–C07
the bar and its coverage; C03–C04 the requirement and
its closure; C03–C05 set provenance and training
lineage as different facts; C03–C07 the frozen set and
its mapped fraction; C04–C09 the closure and the
descriptive table; C05–C08 training provenance and
scoring data; C06–C07 the fixed instrument and its
residue; C07–C09 the coverage line and the table).

## Round 2 — 2026-10-13T10:45:52Z — iterate (4 failure modes)

Artifact: `aee-after_specify-20261013T104552Z.json`
(0 claims below the 0.70 threshold).

- **Irreducibility (3):** C03 (reconstruction plus
  freezing-before-counting read as two propositions),
  C06 (the mapping instrument plus its fixing time),
  C12 (the reporting rule plus its negation).
- **Negation conflict (1):** C03↔C04 (the set's
  reconstruction against the closure for its failure).

**Recovery (register 0.2-draft → 0.3-draft).** C03 and
C06 were reduced to their single governing
propositions; the freeze-before-counting rule stands
in both boundaries verbatim-in-substance, as it
already did. C04's text was keyed to step 0.1, with
its trigger (the exact trained set not reproducible
from the record) stated in full in its boundary and
verdict rule — the pairing's lexical mirror is gone
and the proposition is unchanged. C12 was reduced to
its single reporting rule; the closure names and the
never-as-verdicts substance stand in its boundary and
verdict rule.

## Round 3 — 2026-10-13T10:46:06Z — iterate (1 failure mode)

Artifact: `aee-after_specify-20261013T104606Z.json`.

- **Irreducibility (1):** C06 (the mapping instrument
  sentence still read as compound).

**Recovery (register 0.3-draft → 0.4-draft).** C06's
text was recast in the Spec 031 C06 sentence shape
("built only from …"). The crosswalk location
(`data/crosswalks`) stands in C06's boundary and in
spec §3.3; the proposition is unchanged.

## Outcome — PASS (register 0.4-draft)

Re-run at after_specify on 2026-10-13T10:46:14Z:
**pass** (12 claims, 0 failure modes, 0 below the
0.70 threshold; artifact
`aee-after_specify-20261013T104614Z.json`). The
after_plan (20261013T104622Z) and after_tasks
(20261013T104624Z) assessments over the same register
also return **pass** with the same summary. The
frozen register is the recovered register
(`0.4-draft`); the pre-recovery drafts were never
frozen.
