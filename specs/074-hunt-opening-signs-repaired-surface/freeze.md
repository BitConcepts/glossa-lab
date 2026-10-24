# Spec 074 — Freeze record

**FROZEN — 2026-10-24.** This directory is the frozen
contract for Spec 074: `spec.md` (the design),
`claims.json` (the claims register, recovered to
0.7-draft, 13 claims F074-C01…F074-C13),
`adjudication.md` (the drafting record, with the
freeze rulings at §8), this record, and the AEE hook
artifacts under `aee/`.

The freeze is executed under the owner's order of
2026-10-24 ("Shouldn't we do all three of these?"),
covering the re-freeze and execution of Spec 070's
question on the surface Spec 073 repaired. The
dependency was satisfied before drafting began: Spec
073 executed and merged (outcome REPAIRED WITH NAMED
SHORTFALL; freeze PR #352, execution PR #354), and
Spec 070's closure stands unamended — this is a
successor, not a reopening. **Phase allocated: Phase
440** (DD-074-12). An OSF registration is filed for
this freeze at the freeze act (DD-074-11); its record
is `osf-spec-registration.md` in this directory.
Execution is a separate act, on the owner's word; it
has not run.

## 1. What was frozen

- **The question** (spec §1.1): whether the
  opening-strong positional class of the Shakti
  corpus, counted under the Phase-43 battery on ICIT
  numbering, consists largely of signs depicting
  animals — Spec 070's question, re-asked unchanged.
- **The battery** (spec §2): the Phase-43 positional
  rules as Spec 070 froze them — sequences of length
  ≥ 2; I/M/T by position; classification floor
  total ≥ 5; the strength cascade TERMINAL_STRONG
  t_rate ≥ 0.60, INITIAL_STRONG i_rate ≥ 0.55,
  MEDIAL_STRONG m_rate ≥ 0.65, TERMINAL_MODERATE
  t_rate ≥ 0.40, INITIAL_MODERATE i_rate ≥ 0.40, else
  MIXED, first match wins; threshold-only, with no
  chance baseline (the G5 attestation) — carried
  verbatim.
- **The populations** (spec §4.1): the primary
  population is the documented-lineage rows of the
  pinned Shakti corpus (grade discipline P-F1 S4);
  the opening-strong set is the population the join
  runs over; the corroborated population enters only
  through the pre-registered sensitivity.
- **The arms** (spec §4.2): R1 and R2 as Spec 070
  froze them, over Asset A v2.
- **The precedence** (spec §4.3): Spec 070's verdict
  precedence, carried verbatim.
- **The sensitivities** (spec §4.4): S-A, S-B, S-C as
  Spec 070 froze them.
- **The step-0 gates** (spec §5, gates 0.1–0.6),
  fail-closed, including gate 0.4's keying gate over
  the two-leg route (DD-074-8) and its
  population-reproduction assertion (DD-074-9).
- **The pre-written verdict wordings** (spec §4.6),
  re-pointed to this spec and Asset A v2, with the
  POPULATION NOT REPRODUCED wording added.
- **The outcome classes** (spec §9): NOT-RUN, ASSET
  NOT FROZEN, ASSET PIN MISMATCH, SHAKTI INTAKE NOT
  REPRODUCED, POPULATION NOT REPRODUCED, POPULATION
  NOT KEYED, INVALID, SUPPORTED, NOT SUPPORTED,
  INCONCLUSIVE.

## 2. The named changes against Spec 070

Spec §1.3 is the complete list; in brief: (1) the
keying surface is re-based on Registry v2 and Asset A
v2, replacing Registry v1 and Asset A v1; (2) the
keying route gains a second leg over Registry v2's
`icit_wells` rows; (3) a population-reproduction
assertion is added at gate 0.4, with the POPULATION
NOT REPRODUCED closure; (4) the asset facts quoted
are Asset A v2's, whose recorded consequence is that
the five formerly unkeyable signs are classified
`unidentified` — they key, and are counted, listed,
and excluded from the primary's numerator and
denominator; keying is not classification; (5) the
§4.6 wordings are re-pointed, one added, none changed
in substance. Anything in Spec 070's design not on
this list is carried verbatim; a further difference
found between the two texts is a drafting defect, to
be recorded as such.

## 3. Freeze rulings

Ruled at adjudication §8 (DD-074-7 to DD-074-13):
the v2 digests are copied from Spec 073's executed
record and re-verified by recomputation (DD-074-7);
the two-leg keying route is ruled in the form carried
in the boundary of F074-C08, with DD-070-10's counting
rule carried as a standing rule (DD-074-8); the
reproduction assertion and the POPULATION NOT
REPRODUCED closure are upheld as drafted —
conservative, flagged (DD-074-9); DD-070-11's
disposition is carried unchanged, so the recorded
headline claim's frozen dispute closes as POPULATION
NOT KEYED — conservative, flagged (DD-074-10); an own
OSF registration is filed at the freeze (DD-074-11);
the phase is Phase 440 (DD-074-12); the AEE gate
reading of DD-038-10 governs (DD-074-13). The draft
readings DD-074-1 to DD-074-6 stand as drafted.

## 4. Pins verified first-hand at this freeze

Every pin below was recomputed or read on the merged
tree at the freeze act; none is trusted from a draft.

- **Asset A v2** —
  `specs/073-keying-surface-repair/asset-a-v2/depicted-kind-classification.csv`,
  SHA-256
  `681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`,
  552 rows (187 carried from v1 untouched, 365 new
  entries); per-kind counts animal 30, sky_cycle 0,
  object_goods 22, human 43, other 246, contested 0,
  unidentified 211.
- **Registry v2** —
  `data/crosswalks/canonical_sign_registry_v2.csv`,
  SHA-256
  `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`,
  1,013 rows (803 carried from v1 byte-identical, 210
  `icit_wells` rows appended, completions applied 0).
  Registry v1 stands untouched at SHA-256
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`.
- **Spec 070's executed record** —
  `reports/phase433_results.json`, SHA-256
  `667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214`;
  its published opening-strong enumeration (31 signs)
  and battery class census (220 signs at the floor:
  TERMINAL_STRONG 42, MEDIAL_STRONG 81,
  TERMINAL_MODERATE 37, INITIAL_MODERATE 6, MIXED 23,
  INITIAL_STRONG 31); Spec 070's freeze digest
  `763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e`.
- **Shakti corpus** (`sanitized_corpus.json`,
  restricted-local, cited through the intake record),
  SHA-256
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`;
  row-grades file SHA-256
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`;
  5,704 rows, 5,536 analyzable; grade counts 3,212
  documented-lineage / 2,087
  undocumented-corroborated / 405
  undocumented-uncorroborated.
- **Sign crosswalk of record**
  (`data/crosswalks/sign_crosswalk_master.csv`),
  SHA-256
  `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf`.
- **Anchors file**
  (`backend/reports/INDUS_FINAL_ANCHORS.json`),
  SHA-256
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`.
  This spec moves no anchor.
- **Keyability spot-fact at the freeze** (recorded at
  drafting, re-verified against the pinned files):
  under the two-leg route, all 31 of Spec 070's
  recorded opening-strong signs resolve to exactly
  one Asset A v2 row each, and the combined Wells map
  carries 708 distinct Wells ids with zero resolving
  to more than one sign. No test quantity was
  computed at drafting or at the freeze: the
  depicted-kind distribution of the opening-strong
  set, and every arm share, remain unmeasured until
  an execution runs the frozen gates.

## 5. AEE gate

The hooks ran before the digest was computed, in the
established order (tasks L4). Two recovery rounds
brought the register from 0.5-draft to **0.7-draft**
(vocabulary restatement for loadability; then
`independent_of` declarations; the draft heads were
already single propositions, so no head restatement
was needed). The final round, over 0.7-draft, at all
three hooks (after_specify, after_plan, after_tasks):
**13 failure modes each, every one an FR-2.3
draft-cap record; zero correctness failure modes;
minimum propagated confidence 0.795**, above the 0.70
threshold. The gate passes on the DD-038-10 reading
(DD-074-13). The full record is `aee/freeze-aee-note.md`;
the round artifacts are under `aee/`.

## 6. Freeze digest

The freeze digest is computed by `build_freeze.py`
(framework026) over seven sources — this record,
`spec.md`, `claims.json`, `adjudication.md`,
`aee/freeze-aee-note.md`, `build_freeze.py`, and
`backend/tests/test_spec074_freeze.py` — and is
recorded in `freeze.json` in this directory and
quoted in the freeze commit and pull request. It was
computed exactly once, after the AEE gate passed,
over the final texts. The freeze tests
(`backend/tests/test_spec074_freeze.py`) replay the
digest, assert the definition's constants, the
register's integrity, the hook artifacts' pass shape,
and the input pins of §4 by recomputation.

## 7. Able-to-fail proof

With the assembled freeze in place, the register's
`register_version` was mutated in exactly one place
(0.7-draft → 0.7-draft-MUTATED) and the freeze tests
were run: they failed (the replay and the register
integrity assertions). The register was then restored
byte-identical — its SHA-256 re-verified against the
frozen value — and the tests passed. The freeze is
therefore falsifiable by its own tests: a silent
change to a frozen source breaks the replay rather
than passing unnoticed.

## 8. What this freeze does not establish

This freeze establishes that Spec 070's question is
now askable on a repaired surface, under a frozen
contract whose population keys 31/31 at the keying
spot-check. It does not establish, and does not
prejudge, any answer: no arm has run, no depicted-kind
share of the opening-strong set has been measured,
and the recorded consequence of Asset A v2 — that
the five signs whose keying Spec 070 lacked are
classified `unidentified`, and so leave the primary's
numerator and denominator — is a fact about the
asset, not a result of this test. Spec 070's closure
(POPULATION NOT KEYED) stands exactly as recorded;
nothing here amends, reopens, or re-scores it. The
test this freeze freezes runs only on a separate
execution order.

---

*AI disclosure: this freeze was executed by an AI
agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
