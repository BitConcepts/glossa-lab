# Spec 071 — Freeze Record

> ## FROZEN — 2026-10-22
>
> Spec 071 is frozen as written in this
> directory: `spec.md` (the contract),
> `claims.json` (the frozen claims register,
> version `0.9-frozen-candidate`, thirteen
> claims F071-C01…F071-C13), `adjudication.md`
> (the draft record, with the freeze rulings at
> its §8), this freeze record, and the AEE gate
> artifacts under `aee/`. The freeze was
> executed under the owner's freeze rulings for
> the Hunt chain (every open item per the
> draft's stated default; a predecessor's
> decided position stands; a genuine unresolved
> choice takes the more conservative option,
> recorded and flagged), after Spec 070's
> freeze, as the commissioned order requires
> (DD-071-2). The execution phase allocated at
> this freeze is **Phase 434** (DD-071-13). An
> OSF registration for this spec is filed at
> this freeze (DD-071-12); its record is
> `osf-spec-registration.md` in this directory.

## 1. What was frozen

The re-scoped successor to Spec 050, complete as
drafted: the §2 battery (the recovered Phase-43
rules applied new to the Shakti corpus), the
§4.1 celestial class (exactly Asset A's
`sky_cycle` rows; no widening), the §4.2
frequency-matched comparison class and pooled
occurrence rates, Spec 050's criteria carried
unchanged (enrichment ratio ≥ 1.5, two-sided
Fisher exact at 5%, the half-of-occurrences
condition; the TOO THIN floor of 30 total
occurrences for the celestial or the comparison
class at gate 0.4), the §4.4 per-sign table, the
sensitivities (S1 borderline removed, S2
contested under CISI-governed sky labels, S3
corroborated), the §5 step-0 gates (0.1–0.5,
P-F1 S1/S2, the freeze-order proof), and the §7
outcome classes with the pre-written §4.6
wordings. Nothing in the drafted design was
changed by the freeze; the freeze decided the
six open items (§2), advanced the claims
register through the AEE gate (§4), and computed
the digest (§5) exactly once, after the gate
passed.

## 2. The freeze rulings (adjudication.md §8)

- **DD-071-8 (OPEN-071-1)** — the Shakti intake
  record is landed in final form on `main` (PR
  #339, head `bfc811df`), adopting P-F1; its pins
  re-asserted first-hand at this freeze.
- **DD-071-9 (OPEN-071-2)** — Asset A's digest
  copied character for character from Spec 069's
  executed record and re-verified by
  recomputation on the merged tree (§3); and the
  order recorded: this freeze follows Spec 070's
  freeze (PR #340, merged at `1213029d`) in the
  commissioned order. The pin source for gate
  0.1 is fixed as Spec 069's `asset-a-freeze.json`
  in its merged executed record.
- **DD-071-10 (OPEN-071-3)** — the keying route
  is the shared route Spec 070's freeze fixed,
  stated in this spec's own record: ICIT code =
  Wells number, resolved through the pinned
  canonical registry's `parpola_1982` rows'
  `wells_ids` to exactly one Asset A `sign_key`.
- **DD-071-11 (OPEN-071-4)** — **conservative
  choice, flagged:** an unkeyable sign
  enumerated at gate 0.4 closes the execution as
  POPULATION NOT KEYED.
- **DD-071-12 (OPEN-071-5)** — this spec files
  its own OSF registration at its freeze, per
  the owner's ruling.
- **DD-071-13 (OPEN-071-6)** — Phase 434.
- **DD-071-14** — the AEE gate reading of
  DD-071-7/DD-038-10 governs (§4).

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
  the quoted value. **The celestial class on
  this asset is empty — zero `sky_cycle` rows —
  and that fact is part of the frozen record the
  execution meets at gate 0.4, in the design's
  own pre-registered terms (the TOO THIN floor);
  the freeze neither widens the class (the spec
  forbids it) nor treats the zero as a defect of
  the asset: it is what the held published
  identifications record for this sign universe.**
- **Shakti corpus pins** (intake record,
  re-verified by direct hash at this freeze):
  corpus SANITIZED SHA-256
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`;
  row-grades CSV SHA-256
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`;
  census 5,704 rows, grades 3,212 documented /
  2,087 corroborated / 405 uncorroborated.
- **Canonical sign registry** (the keying route's
  pin): SHA-256
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`,
  803 rows; its `parpola_1982` Wells map carries
  498 Wells ids with no ambiguity (verified at
  Spec 070's freeze and re-verified here).
- **Pinned crosswalk**: SHA-256
  `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf`.
- **Anchors**: SHA-256
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`.

## 4. The AEE freeze gate

The gate of DD-071-7, in the substantive form of
DD-038-10 (DD-071-14): the AEE lifecycle hooks at
after_specify, after_plan and after_tasks, with
zero correctness failure modes and no claim below
0.70 propagated confidence. The draft register
(0.5-draft) did not load in the installed evaluator;
it was restated in the evaluator's vocabulary
(0.6) and then recovered through two documented
rounds (0.7, then 0.9) — atomic claim heads,
drafted substance preserved in boundaries, the
freeze rulings carried into the boundaries of
F071-C07 and F071-C08 — as recorded in
`aee/freeze-aee-note.md`. **Final result, at the
frozen register (0.9-frozen-candidate): all
three hooks pass with zero failure modes;
minimum propagated confidence 0.845** (assessment
artifacts 20261023T001133Z / 20261023T001134Z /
20261023T001134Z, copies under `aee/`). The hooks
measure the register's internal discipline; they
do not establish that the celestial class is
populated, that coverage will hold at gate 0.3,
or that any outcome will favour the claim — the
execution decides those, under the frozen
criteria.

## 5. The freeze digest

Computed exactly once, after the gate passed,
with `build_freeze.py` in this directory over the
seven frozen sources (`freeze.md`, `spec.md`,
`claims.json`, `adjudication.md`,
`aee/freeze-aee-note.md`, `build_freeze.py`,
`backend/tests/test_spec071_freeze.py`): the
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

`backend/tests/test_spec071_freeze.py` replays
the record over the sources (framework026
verify_freeze) and fails if any frozen source
changes; the freeze PR's CI runs it.

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec071_freeze.py` were
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
that the sky signs gather at text endings, or
that they do not; and it records, without
flinching, the two facts the execution will
meet first: the celestial class is empty on the
frozen asset, and Asset A's 187-row universe is
far smaller than the set of signs the corpus
uses — both of which the design's gates were
written to face in their named classes rather
than to finesse.

---

*AI disclosure: frozen by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
