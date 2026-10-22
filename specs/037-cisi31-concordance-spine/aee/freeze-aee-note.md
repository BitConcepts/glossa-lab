# Spec 037 — AEE note

The AEE lifecycle hooks (after_specify /
after_plan / after_tasks) have **not run** on
this draft's claim register (F037-C01…C15),
deliberately: the hooks are a **freeze gate**,
not a drafting step (tasks L3). Any recovery
round at the freeze act changes claim text, so
the freeze digest is computed over the
recovered register exactly once, at freeze —
the ordering Spec 035 established and Spec 036
carried. At this draft the register carries
only the draft-stage self-checks pinned by
`backend/tests/test_spec037_freeze.py`
(dependency integrity; the definition
constants; the cited-record facts: the
corpus_master pin, the Spec 031 fence figures,
and the design constants in `freeze.json`).

At the freeze act, the hook outputs and any
recovery rounds are recorded in this directory
(`aee/`), and this note is completed by append
with their record.

## Completion — the freeze act, 2026-10-20

**Verdict: the lifecycle hooks PASS at the
freeze** — all three lifecycle hooks
(after_specify, after_plan, after_tasks) ran
over the register under the adopted aee 1.5.0
at the freeze act, and at every hook the
assessment carries **zero correctness failure
modes** (no irreducibility, no negation
conflict, no counterexample or precision
challenge) and **no claim below the 0.70
confidence threshold** (minimum propagated
0.72). The engine's outcome word reads
"iterate" at all three hooks solely because
the register is a draft: each claim carries
one FR-2.3 draft-cap record (15, one per
claim), which caps a draft bundle's outcome
regardless of score and is lifted only by
human ratification (a status change), not by
any recovery available at a freeze. This is
the gate reading Spec 038 recorded as
DD-038-10; it is adopted for this spec as
DD-037-9 (`adjudication.md` §4), so it is
applied here openly rather than discovered
after the fact.

Rounds at after_specify (aee 1.5.0, threshold
0.70):

- **Round 1** over register 0.5-draft (as
  drafted): outcome iterate, 37 failure modes
  — 15 irreducibility challenges (one per
  claim), 5 counterexample challenges
  (absolute language without a bounded domain:
  C02, C05, C10, C11, C14), 2 shared-evidence
  independence records (C01, C08), 15 FR-2.3
  draft-cap records — and 13 of 15 claims
  below the 0.70 threshold (every evidence
  item carried the FR-8.6 freshness penalty:
  no item recorded `observed_at`).
- **Recovery to 0.6-draft:** every claim text
  restated as its single head proposition,
  the carried clauses moved into the claims'
  boundaries verbatim-in-substance; the five
  counterexample-flagged texts domain-bounded
  ("Under Spec 037, ..."); every evidence
  item gained `observed_at` "2026-10-20" (the
  `adjudication.md` §2 verification date;
  refs, kinds, directions, and descriptions
  unchanged); F037-C01's Phase-130 item gained
  the symmetric `independent_of` declaration
  (the C01/C08 shared-corroboration record is
  in the register's own note).
- **Round 2** over 0.6-draft: outcome
  iterate, 27 failure modes — 5
  irreducibility challenges (C02, C04, C07,
  C09, C14), 4 negation conflicts (C02
  against C05, C10, C11, C14), 3
  counterexample challenges (C04 newly
  flagged; C05, C10), 15 draft-cap records —
  and no claim below the 0.70 threshold
  (minimum propagated 0.72).
- **Round 3 recovery (0.7-draft):** the five
  still-compound texts restated to a single
  predicate each (C02 positively — a match
  "is a candidate for a same-object join",
  the not-a-join fence carried in its
  boundary; C07 scored-only, advancement and
  retirement carried in its boundary; C09
  precedes-any-computation, its checks
  carried in its boundary; C14 museum/owner
  as one compound noun phrase), which also
  retired the four negation conflicts, whose
  trigger was the negated second predicate in
  C02's round-2 text; the absolute quantifier
  removed from the C05 and C10 texts ("the
  693 candidates" — the totality is carried
  by the census proposition and the
  boundaries); C04's "never repaired" moved
  into its boundary.
- **Round 3 result** over 0.7-draft: 15
  failure modes, all FR-2.3 draft-cap
  records; zero correctness failure modes;
  minimum propagated 0.72; no claim below
  threshold. after_plan and after_tasks over
  the same register: clean at first pass on
  the same terms (15 draft-cap records each).

Artifacts in this directory:
`aee-after_specify-20261021T004908Z.json` +
`evaluator-aee-after_specify-20261021T004908Z.json`;
`aee-after_plan-20261021T004923Z.json` +
`evaluator-aee-after_plan-20261021T004923Z.json`;
`aee-after_tasks-20261021T004938Z.json` +
`evaluator-aee-after_tasks-20261021T004938Z.json`
(engine timestamps are UTC; the freeze act is
dated 2026-10-20 local). The register's own
note carries the per-round recovery record.
The freeze digest (`freeze.json`) was
computed over the recovered register
(0.7-draft) exactly once.

**Environment:** aee 1.5.0 (adopted
environment, PR #231; pin `>=1.5.0,<1.6`);
spec-kit-evaluator present; Python 3.12;
assessments run in-process through the same
invocation the repo's `run_aee.py` harness
makes (evidence verification off, lenient
load, no ledger).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
