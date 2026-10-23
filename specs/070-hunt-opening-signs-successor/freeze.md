# Spec 070 — Freeze Record

> ## FROZEN — 2026-10-22
>
> Spec 070 is frozen as written in this
> directory: `spec.md` (the contract),
> `claims.json` (the frozen claims register,
> version `0.9-frozen-candidate`, thirteen
> claims F070-C01…F070-C13), `adjudication.md`
> (the draft record, with the freeze rulings at
> its §7), this freeze record, and the AEE gate
> artifacts under `aee/`. The freeze was
> executed under the owner's freeze rulings for
> the Hunt chain (every open item per the
> draft's stated default; a predecessor's
> decided position stands; a genuine unresolved
> choice takes the more conservative option,
> recorded and flagged), after Spec 069's
> executed record was merged to `main`, as the
> spec's own dependency order requires. The
> execution phase allocated at this freeze is
> **Phase 433** (DD-070-13). An OSF registration
> for this spec is filed at this freeze
> (DD-070-12); its record is
> `osf-spec-registration.md` in this directory.

## 1. What was frozen

The re-scoped successor to Spec 049, complete as
drafted: the §2 battery (the recovered Phase-43
rules applied new to the Shakti corpus — position
rule, floor, cascade, threshold-only, G5
attestation mandatory), the §3 primary/sensitivity
design (documented-lineage rows primary; S-A
contested under CISI-governed labels, S-B unicorn
removed, S-C documented + corroborated with classes
re-derived), the §4 test (O the opening-strong set
enumerated in Wells space before any join; U the
≥30-occurrence inventory; R1/R2; Fisher exact on
the disjoint 2×2; the §4.3 precedence carried from
Spec 049's DD-049-3), the §5 step-0 gates
(0.1–0.6, P-F1 S1/S2, the freeze-order proof), and
the §6 deliverables with the pre-written §4.6
outcome wordings. Nothing in the drafted design
was changed by the freeze; the freeze decided the
seven open items (§2), advanced the claims
register through the AEE gate (§4), and computed
the digest (§5) exactly once, after the gate
passed.

## 2. The freeze rulings (adjudication.md §7)

- **DD-070-7 (OPEN-070-1)** — the Shakti intake
  record is landed in final form on `main` (PR
  #339, head `bfc811df`), adopting P-F1; its pins
  re-asserted first-hand at this freeze.
- **DD-070-8 (OPEN-070-2)** — Asset A's digest
  copied character for character from Spec 069's
  executed record and re-verified by recomputation
  on the merged tree (§3).
- **DD-070-9 (OPEN-070-3)** — the keying route is
  fixed: a Shakti sign's ICIT code is its Wells
  number, resolved through the pinned canonical
  sign registry's `parpola_1982` rows' `wells_ids`
  to exactly one Asset A `sign_key`; zero or
  multiple resolutions is unkeyable. At this
  freeze the route's Wells map carries 498 Wells
  ids with no ambiguity (verified).
- **DD-070-10 (OPEN-070-4)** — the counting rule
  is fixed: every occurrence in sequences of
  length ≥ 2, counted once under the battery's
  own counting, on the population in question.
- **DD-070-11 (OPEN-070-5)** — **conservative
  choice, flagged:** an unkeyable sign enumerated
  in the opening-strong set closes the execution
  at gate 0.4 as POPULATION NOT KEYED. The draft
  wrote both branches; the freeze takes closure,
  because a stated continuation would let a
  verdict rest on a population with a hole in it.
- **DD-070-12 (OPEN-070-6)** — this spec files
  its own OSF registration at its freeze, per the
  owner's ruling.
- **DD-070-13 (OPEN-070-7)** — Phase 433.
- **DD-070-14** — the AEE gate reading of
  DD-070-6/DD-038-10 governs (§4).

## 3. Pins verified first-hand at this freeze

- **Asset A** (from Spec 069's executed record,
  `specs/069-hunt-asset-a/asset-a/asset-a-freeze.json`
  as merged by PR #345 at `6a981188`): SHA-256
  `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b`,
  187 rows; per-kind counts animal 20, sky_cycle
  0, object_goods 14, human 25, other 127,
  contested 0, unidentified 1. Re-verified at this
  freeze by recomputing the canonical CSV's
  digest on the merged tree: it recomputes to
  the quoted value. Gate 0.1 asserts this digest;
  the counts are quoted so a reader can see what
  the test's animal class is made of — twenty
  signs, none contested — and what S-A therefore
  is on this asset (equal to the primary, as the
  spec's S-A note anticipates).
- **Shakti corpus pins** (intake record,
  re-verified by direct hash at this freeze):
  corpus SANITIZED SHA-256
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`;
  row-grades CSV SHA-256
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`;
  census 5,704 rows, grades 3,212 documented /
  2,087 corroborated / 405 uncorroborated — the
  grades file's own counts agree.
- **Canonical sign registry** (the keying route's
  pin): `data/crosswalks/canonical_sign_registry.csv`,
  SHA-256
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`,
  803 rows; its `parpola_1982` Wells map verified
  unambiguous at this freeze (498 Wells ids, zero
  resolving to more than one sign).
- **Pinned crosswalk**: `data/crosswalks/sign_crosswalk_master.csv`,
  SHA-256
  `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf`
  (re-hashed at Spec 069's execution).
- **Anchors**: `backend/reports/INDUS_FINAL_ANCHORS.json`,
  SHA-256
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`.

## 4. The AEE freeze gate

The gate of DD-070-6, in the substantive form of
DD-038-10 (DD-070-14): the AEE lifecycle hooks at
after_specify, after_plan and after_tasks, with
zero correctness failure modes and no claim below
0.70 propagated confidence. The draft register
(0.5-draft) did not load in the installed evaluator
(its evidence kinds and one source quality are not
accepted values); it was restated in the
evaluator's vocabulary (0.6) and then recovered
through three documented rounds (0.7, 0.8, 0.9) —
atomic claim heads, drafted substance preserved in
boundaries, the freeze rulings carried into the
boundaries of F070-C05, F070-C08 and F070-C11 — as
recorded in `aee/freeze-aee-note.md`. **Final
result, at the frozen register
(0.9-frozen-candidate): all three hooks pass with
zero failure modes; minimum propagated confidence
0.845** (assessment artifacts
20261022T233858Z / 20261022T233859Z /
20261022T233901Z, copies under `aee/`). The hooks
measure the register's internal discipline; they
do not establish that the re-scoped question is
the right one, that the keying route will resolve
the population the execution enumerates, or that
any outcome will favour the claim — the execution
decides those, under the frozen criteria.

## 5. The freeze digest

Computed exactly once, after the gate passed,
with `build_freeze.py` in this directory over the
seven frozen sources (`freeze.md`, `spec.md`,
`claims.json`, `adjudication.md`,
`aee/freeze-aee-note.md`, `build_freeze.py`,
`backend/tests/test_spec070_freeze.py`): the
machine record is `freeze.json` in this
directory (framework026 build_freeze payload:
definition + source hashes + environment; the
digest is the SHA-256 of its canonical JSON
serialisation). `freeze.md` is itself a
digest-covered source, so the digest value is
carried by `freeze.json` and quoted in the
freeze commit and PR, not in this file.

Freeze digest (SHA-256): see `freeze.json` in
this directory (field `digest`).

`backend/tests/test_spec070_freeze.py` replays
the record over the sources (framework026
verify_freeze) and fails if any frozen source
changes; the freeze PR's CI runs it.

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec070_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string,
`0.9-frozen-candidate` → `0.9-MUTATED`) and the
suite was run — the freeze-replay test and the
register-integrity test went red, as they must,
because a covered source no longer matched its
frozen hash and the register no longer carried
its frozen version. The file was then restored
byte-identically (its SHA-256 re-verified
against the value recorded in `freeze.json`'s
sources) and the full freeze suite was run
again green. The mutation touched no committed
byte; the frozen record replays exactly over
the restored tree.

## 7. What this freeze does not establish

Freezing establishes that the contract is fixed,
that its inputs are the ones its pins name, and
that step 0 can check them. It does not establish
that the opening-strong set will key, that the
animal signs are or are not enriched in it, or
anything about what any sign means. Phase-43's
counts (805/2,267; the 40/61/20 classes) play no
part in this spec, by its honesty fence: the
classes here are a first measurement on Shakti,
checked against nothing.

---

*AI disclosure: frozen by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
