# Spec 070 / Phase 433 — Outcome record (EXECUTED 2026-10-22 — POPULATION NOT KEYED)

> ## EXECUTED — 2026-10-22 — CLOSED AT STEP 0 (gate 0.4): POPULATION NOT KEYED
>
> Executed under the frozen Spec 070 contract
> (freeze digest
> `763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e`;
> freeze PR #340 merged at `1213029d`; OSF
> registration nghs5 filed at the freeze,
> pending the owner's approval act at the time
> of the run), as **Phase 433**, in the chain
> order of the owner act that commissioned the
> Hunt chain. The step-0 gates ran in order:
> 0.1 Asset A asserted and PASS; 0.2 the Shakti
> intake reproduced under P-F1 S1/S2 and PASS;
> 0.3 input integrity PASS; **0.4 the population
> was enumerated and published, and five of its
> signs could not be keyed — under the
> disposition the freeze fixed in advance
> (DD-070-11), the execution closes here as
> POPULATION NOT KEYED.** No join was performed
> and no test quantity was computed. The machine
> record is `reports/phase433_results.json`.

## Headline (spec §4.6 POPULATION NOT KEYED wording, filled from the run)

> "Spec 070 closed at step 0: Shakti's
> opening-strong set was enumerated in full (31
> signs, published with this closure), and the
> signs that could not be keyed to exactly one
> Asset A row in Wells space are listed with
> their reasons; under the disposition the
> freeze stated, the execution closes here. No
> join was performed and no test quantity was
> computed. The claim stands as recorded."

Lineage (P-F1 S3), carried in the headline
block as the design requires: the positional
classes were measured on the Shakti corpus
deposit (Zenodo) as graded by the programme's
intake record — documented-lineage rows are
CISI-verifiable; corroborated rows are supported
by an independent sign list; uncorroborated rows
enter no count. The Phase-43 counts (805/2,267;
the 40/61/20 classes) are never a basis for any
quantity here. G5 attestation: the battery
applied is threshold-only, with no
chance-baseline step, and none is claimed.

What this means, in plain words: the question
was not answered, and the record says exactly
why. Shakti's own battery returns 31
opening-strong signs. Five of them — the ICIT
codes 136, 298, 401, 617 and 824 — have no
Wells identity in the pinned canonical sign
registry: no registry row, in any numbering
system, carries those Wells ids, so under the
keying route the freeze fixed there is no Asset
A row they can be keyed to. (The two numberings
are genuinely different lists — the registry's
Parpola 136, for instance, carries Wells ids
W048 and W049 — which is why the keying rule
exists at all.) The freeze had to choose in
advance what an unkeyable sign would do, and it
chose the conservative branch: close, rather
than let a verdict rest on a population with
five holes in it. That choice, made before the
population existed, is what closed this
execution — not a judgement call at run time.

## 1. The gates, as they ran

- **0.1 Asset A — PASS.** Spec 069's record
  shows Asset A frozen (its freeze digest and
  `asset-a-freeze.json` present in the merged
  record); the canonical CSV recomputes to
  `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b`;
  the presented file's per-kind counts match
  the freeze record's (animal 20, sky_cycle 0,
  object_goods 14, human 25, other 127,
  contested 0, unidentified 1).
- **0.2 Shakti intake (P-F1 S1/S2) — PASS.**
  Both restricted-local files hash to their
  pins; the census reproduces from the files
  themselves: 5,704 rows; 5,536 analyzable;
  grades 3,212 documented / 2,087 corroborated /
  405 uncorroborated; 4,904 of 5,536 analyzable
  rows carrying a CISI identifier.
- **0.3 Input integrity — PASS.** The canonical
  registry, the crosswalk and the anchors hash
  to their freeze values.
- **0.4 Population and keying — CLOSES.** The
  battery over the primary population
  (3,212 documented-lineage rows) classifies
  220 signs at the floor: TERMINAL_STRONG 42,
  MEDIAL_STRONG 81, TERMINAL_MODERATE 37,
  INITIAL_MODERATE 6, MIXED 23, and
  **INITIAL_STRONG 31** — Shakti's own
  opening-strong set, enumerated in full in
  Wells space in the machine record (with each
  sign's I/M/T counts) and hashed there before
  any join (gate 0.6's proof: the population
  publication's SHA-256 is recorded in
  `reports/phase433_results.json` ahead of any
  join quantity, and no join quantity exists in
  the record). Keying under DD-070-9 resolves 26
  of the 31; five cannot be keyed, each for the
  same stated reason — no `parpola_1982`
  registry row carries the sign's Wells id:
  **136** (6 occurrences, all initial),
  **298** (7), **401** (5), **617** (56),
  **824** (16). The finding was verified
  independently of the run: no row of the
  registry in any numbering system carries
  W136, W298, W401, W617 or W824. Under
  DD-070-11 the execution closes at this gate.
- **0.5 / 0.6 — not reached**, and no quantity
  that depends on them exists. The comparison
  census, the sensitivities and the test were
  not computed; nothing in this record reports
  a value for R1, R2 or any p.

## 2. Foundation check (H21), as measured

Run on the execution tree after the phase, with
the two Holdat CSVs copied from the existing
local downloads into the worktree's local store:
**40 checks passed, 0 failed, 8 warnings** — the
standing figure. Anchors were asserted
byte-identical before and after the run
(`df0cf620…`). The run is deterministic: a
second execution of the phase script reproduced
`reports/phase433_results.json` byte-identically.

## 3. What the outcome does not establish

This closure establishes nothing about whether
the opening signs are the animal signs — in
either direction. It establishes a fact about
the join between two published artefacts: on
the pinned registry, five signs Shakti's own
battery calls opening-strong have no Wells
identity to key through. The claim
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
stands exactly as recorded (IN QUESTION), and no
dated append is made to its record, because the
§4.6 closure wordings carry the claim forward
unchanged — the appends belong to the verdict
classes, and this execution reached none. A
successor that wants this question answered
must first repair the keying surface — a
registry that carries Wells identities for
these signs, or a different freeze-fixed route
— and that is a new freeze decision, not a
repair this execution was permitted to make at
run time. Spec 071 is unaffected in its design:
its step 0 asserts the same asset and intake,
and its population frame is Spec 070's
question's sibling, not its product — it runs
on its own frozen terms.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
