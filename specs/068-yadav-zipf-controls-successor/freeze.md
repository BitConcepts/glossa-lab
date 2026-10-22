# Spec 068 — Freeze Record (Yadav's Zipf Fit: What Is a Curve Fit Worth? — Successor on the Shakti Corpus, Amendment S-053)

> ## FROZEN — 2026-10-22
>
> This contract was frozen on 2026-10-22 under
> the owner's freeze rulings of 2026-10-22
> (DD-068-7 to DD-068-13, `adjudication.md` §7).
> The AEE lifecycle hooks ran over the register
> first (recovered 0.5-draft → 0.8-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). The freeze also files this spec's
> own OSF contract registration (DD-068-12;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-430** under this frozen contract,
> under the owner's execution order of
> 2026-10-22 given with the freeze rulings,
> after the freeze has merged and the
> registration has been filed (§7 states the
> gate exactly). At the freeze itself no census
> has been taken by this spec, no control count
> has been entered, and no fit of any system —
> Indus or control — has been computed; the
> Phase-43 exponent is not an input to anything
> in this freeze.

## 1. Basis

The contract is Spec 053's frozen design
carried onto the Shakti corpus under Amendment
S-053 (spec §2.1): the same question (what a
Zipf–Mandelbrot curve fit is worth), the same
estimator (DD-053-11), the same named controls
(DD-053-13), the same comparison rule
(DD-053-15), and the same floors (DD-053-14),
on the one pinnable Indus distribution the
program now holds — the ShaktiOSindia corpus
as graded in the provenance audit of
2026-10-22, cited only through the P-F1 intake
record (`docs/decisions/2026-10-22-shakti-corpus-intake-record.md`).
Spec 053 itself closed at its step-0 gate 0.3
as STRICT CORPUS NOT PINNABLE, with no fit
computed; its record and closure stand and are
not re-opened. The result of this spec, under
the owner's decision 2c, is a **new baseline**:
it neither confirms nor corrects any Phase-43
quantity, and no Phase-43 quantity is an input
to it.

The freeze decided the open points
(`adjudication.md` §7): **DD-068-7**
(OPEN-068-1: **LIMB B** — the strict-sign-set
restriction is DROPPED, openly; the fitted
population is the full ICIT sign inventory of
the restricted corpus, stated in the freeze
record in spec §2.2's limb-B terms: analyzable
documented-lineage rows counting every token
for the primary fit, analyzable documented +
corroborated rows for the §6.1 sensitivity;
limb A recorded as considered and not taken;
no mapping act is performed and no output may
describe the population as a strict
population), **DD-068-8** (OPEN-068-2: the
intake record asserted standing on the merged
record carrying both pins exactly as spec
§2.1 states them; every other spec §3 pin
re-asserted, with the claim file re-pinned at
its current hash on the open record of §2
below), **DD-068-9** (OPEN-068-3: DD-068-1 to
DD-068-6 confirmed as drafted),
**DD-068-10** (OPEN-068-4: the AEE gate on the
DD-038-10 / DD-053-19 reading; recovery rounds
completed before the digest), **DD-068-11**
(OPEN-068-5: the four control systems stand as
named — Mesopotamian numerical signs, heraldic
charges, the synthetic emblem inventory,
Linear B — no replacement, no second positive
control), **DD-068-12** (OPEN-068-6: a new OSF
contract registration for Spec 068 filed at
the freeze under the program's existing OSF
project), and **DD-068-13** (OPEN-068-7: the
execution phase is Phase-430).

## 2. Pin verification (two routes, at the freeze)

Every committed spec §3 pin was re-derived by
two independent routes — the worktree file and
the git-blob route — both at the freeze tree
(the draft branch with `origin/main` merged
in: `main` at `bfc811df`, the intake record's
merge). The two routes agree byte-for-byte on
every file. The restricted-local pins were
recomputed on the held files by `sha256sum`
at the freeze (step 0 re-asserts them at
execution):

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| Shakti corpus `sanitized_corpus.json` (restricted-local; intake record pin) | `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68` | 1,570,041 |
| Row-grades file `shakti_row_grades_2026-10-22.csv` (restricted-local; intake record pin) | `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739` | — |
| Intake record `docs/decisions/2026-10-22-shakti-corpus-intake-record.md` | `bd14e2b1f0607366ca1845797bcd17f8b577d23140a2e3111fe0cc2652cf9a9d` | — |
| Claim record `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json` (**re-pinned at this freeze**, DD-068-8) | `ec31778a75cbc56f27f385ed7da800edb874a8f600cbe102f46087a8159d6239` | 15,104 |
| Anchors file `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |
| Sign crosswalk `data/crosswalks/sign_crosswalk_master.csv` | `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` | 18,568 |
| Spec 053 frozen spec `specs/053-yadav-zipf-controls/spec.md` | `a41859af4afbddee610afa0c46b94235f61c6079d157b6ca29feba978bb82845` | — |
| Spec 053 adjudication `specs/053-yadav-zipf-controls/adjudication.md` | `cf2965a2c8f899437c8c2b6eb5cf24ef85cd528a53f30e001ebb64d6f7148d28` | — |
| Spec 053 freeze record `specs/053-yadav-zipf-controls/freeze.json` (its digest re-read: `fd2d5cb86b6aed51882a945719bb747ac34f149b08a21e6485b1407c6dc6b309`) | `43ec840123c1d390c87d4cbceff0764bda4b58dcc5cf1cdb179cbb0ffc7cc6b6` | — |

**The one discrepancy, recorded openly
(DD-068-8).** Spec §3 carried the claim record
at Spec 053's freeze pin `90476623…`. That pin
no longer recomputes: the file's bytes changed
after Spec 053's freeze — a re-extraction on
2026-10-21 (timestamps only) and the Spec 025
audit appends of 2026-10-22 (commit
`51cf8b3c`). At the freeze, manual_001's
recorded status (strongly supported), evidence
string ('Phase-43: V3 Zipf exponent ~1.35
(super-Zipfian) [VERIFIED]'), falsifier text,
and stage (explained) were verified
field-by-field **unchanged** against the
pinned version (the file at commit `1ada0a77`,
whose hash is the `90476623…` pin); the only
field-level differences in the whole file are
the two claims' `extracted_at` timestamps and
the top-level `extraction_date`. The freeze
therefore re-pins the claim file at
`ec31778a…` for gate 0.1. `backend/tests/test_spec068_freeze.py`
asserts manual_001's operative fields, so a
later substantive change fails loudly; it
asserts the re-pin as a definition constant,
in the Spec 038 form, because the extracted-
claims store is regenerated by the suite.

The facts the design rests on were re-read
from the pinned bytes in the same pass: the
intake record's census (5,704 rows; 5,536
analyzable; grades 3,212 / 2,087 / 405; 4,904
of 5,536 analyzable rows, 88.6%, carrying a
CISI identifier) and its gates S1–S4; the
anchors census (287 anchors, 94
`strict_sa_independent` — the strict set limb A
would have keyed, recorded here as what limb B
drops); Spec 053's estimator constants,
self-test parameters, comparison rule,
positive-control condition, and floors, as
frozen there.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/068-yadav-zipf-controls-successor/freeze.md` (this
  document)
- `specs/068-yadav-zipf-controls-successor/spec.md`
- `specs/068-yadav-zipf-controls-successor/claims.json`
- `specs/068-yadav-zipf-controls-successor/adjudication.md`
- `specs/068-yadav-zipf-controls-successor/aee/freeze-aee-note.md`
- `specs/068-yadav-zipf-controls-successor/build_freeze.py`
- `backend/tests/test_spec068_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-068-12: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The population** (spec §2.2 / F068-C02):
  limb B as ruled at DD-068-7 — the full ICIT
  sign inventory of the restricted corpus;
  primary on analyzable documented-lineage
  rows, sensitivity on analyzable documented +
  corroborated rows under the same limb; the
  405 undocumented-uncorroborated rows enter
  nothing. Gate 0.5's act is the limb-B
  statement in the step-0 record; STRICT
  MAPPING NOT PINNABLE cannot fire under this
  limb, and no output may call the population
  strict.
- **The intake gates** (spec §4 gates 0.3–0.4
  / F068-C05, C06): S1 (both pins recompute)
  and S2 (the audit census reproduces),
  asserted against the intake record standing
  on the merged record (DD-068-8); failure
  closes as SHAKTI INTAKE NOT REPRODUCED. The
  successor's own restricted census, measured
  at step 0, governs over the draft's derived
  figures.
- **The step-0 gates in order** (spec §4 /
  F068-C09): input integrity against the
  freeze pins of §2 (the claim file at its
  re-pinned hash), the estimator self-test
  (gate 0.2, planted α = 1.20, q = 2.0,
  V = 200, N = 50,000, seed 20261021; failure
  INVALID), S1, S2, the limb-B population act,
  the control set freeze as cited data
  (gate 0.6), and the census floors (gate 0.7:
  ≥ 50 types, ≥ 2,000 tokens on the primary
  fit population; below either, TOO THIN) —
  all before any fit quantity exists.
- **The estimator** (spec §5.2 / F068-C07):
  Spec 053's frozen estimator, identical —
  model C / (r + q)^α with C fixed by
  normalisation; SSE of log residuals; grid
  α 0.00–3.00 step 0.01, q 0.0–20.0 step 0.1,
  one refinement pass at one-tenth steps;
  ranking by count descending, ties by type
  identifier ascending; primary quantity
  NRMSE_log = √(SSE / V).
- **The controls** (spec §4 gate 0.6 /
  F068-C08): exactly the named set of
  DD-068-11, entered whole as cited data and
  frozen before any fit — N1 Mesopotamian
  numerical signs (Nissen, Damerow & Englund,
  *Archaic Bookkeeping* (1993), and the
  published archaic sign counts it reports;
  the exact table and its locator entered at
  gate 0.6, which is the fixed pin source),
  N2 heraldic charges from a published roll of
  arms (roll and edition entered with their
  citation at gate 0.6; unit one charge
  occurrence on one shield), N3 the synthetic
  emblem inventory (Yule–Simon ρ = 0.10, seed
  20261021, 99 replicates, size-matched to the
  Indus primary token total; replicate median),
  P1 Linear B syllabic sign frequencies
  (published corpus counts; exact source
  entered with its citation at gate 0.6). A
  system that cannot be entered whole closes
  the run CONTROL SET FREEZE FAILED; the Indus
  fit is never computed ahead of the controls.
- **The comparison rule and headline**
  (spec §§5.3–5.5 / F068-C10): ε = 0 ("fits as
  well" iff E_control ≤ E_Indus; N3 by its
  replicate median); the falsifier fires iff
  at least one of N1, N2, N3 fits as well; P1
  passes iff E_P1 is strictly below every
  non-linguistic control's error; headline
  SEPARABLE / NOT SEPARABLE / COMPARISON
  UNINFORMATIVE on the primary fit alone; gaps
  reported for every control, 0 < Δ ≤ 0.02
  named NEAR MISS (reporting only).
- **The sensitivities** (spec §6 / F068-C11):
  the grade sensitivity in full beside the
  primary, both orderings exhibited, a
  differing ordering reported as
  grade-sensitivity with the §6.1 sentence in
  the headline block (P-F1 S4); the
  subsampling tables (halves and quarters, 99
  replicates, seed 20261021) for both
  populations; no separate §6.3 fit under
  limb B.
- **The reporting obligations** (spec §10 /
  F068-C12): the P-F1 S3 lineage statement
  verbatim first in every product's headline
  block; the corpus label with both digests
  and the step-0 census; every system's full
  quantities and gaps; the positive-control
  outcome before the headline word; the §7
  pre-written wording for the outcome class;
  the fence sentence.
- **The append-only posture** (spec §8 /
  F068-C03, C14): the outcome appends to
  `yadav_2009_arxiv_manual_001`'s record as a
  dated bounded finding (the strength label);
  the claim's recorded status and exponent,
  Spec 053's record and closure, and the
  Phase-43 files are never edited. The anchors
  file is asserted byte-identical before and
  after any execution; this spec moves no
  anchor.

## 5. What the freeze does not do

- **It does not itself fit anything.** No
  census has been taken by this spec, no
  control count entered, no synthetic
  replicate generated, and no fit quantity
  exists. The derived figures in the draft
  (3,045 / 5,131 analyzable) are expectations
  the step-0 census checks, not measurements.
- **It does not establish anything about the
  old corpus or Phase-43.** The result will
  stand as a new baseline only; the Phase-43
  exponent (~1.35) is named in this freeze only
  inside the fence of §1 and §2, and is an
  input to nothing.
- **It does not choose limb A by the back
  door.** No mapping act, basis source, or
  strict-population reading survives the
  DD-068-7 ruling; a product describing the
  fitted population as strict would be a
  defect of that product.
- **It re-opens nothing.** Spec 053's closure,
  the claim's strongly supported verdict, and
  the intake record's gates stand exactly as
  recorded; this freeze cites them, it does
  not amend them. The claim-file re-pin of
  DD-068-8 changes no claim field: it records
  that the file's bytes moved for reasons
  outside this spec and pins the bytes as they
  stand, with the operative fields verified
  unchanged.
- **Execution is not authorised by the freeze
  alone.** Execution (Phase-430) runs under
  the owner's execution order of 2026-10-22,
  after this freeze has merged and the OSF
  registration has been filed (§7).

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec068_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string, `0.8-draft` →
`0.8-MUTATED`) and the suite was run — the
freeze-replay test and the register-integrity
test went red, as they must, because a covered
source no longer matched its frozen hash and
the register no longer carried its frozen
version. The file was then restored
byte-identically (its SHA-256 re-verified
against the value recorded in `freeze.json`'s
sources) and the full freeze suite was run
again green. The mutation touched no committed
byte; the frozen record replays exactly over
the restored tree.

## 7. OSF registration and the execution gate

Under DD-068-12, this freeze files the spec's
own OSF contract registration — a new
registration for Spec 068 under the program's
existing OSF project (node `nrb9u`, Predictions
& Registrations), not an amendment of Spec
053's — carrying the frozen contract: freeze
digest, execution Phase-430, the falsifier,
the limb-B population as ruled (DD-068-7), the
P-F1 intake gates S1–S4 and both pins, the
step-0 gates in their order with their named
closure classes, the frozen estimator and
comparison rule (ε = 0, NEAR MISS band
reporting-only), the four named controls, the
grade-sensitivity discipline, the new-baseline
fence (decision 2c), and the append-only
posture toward the claim's record and Spec
053's record. The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is
the owner's approval click on OSF's
admin-notification email, and no mail about it
is archived while it stands pending.

Execution gate, as commissioned: execution
(Phase-430) runs under the owner's execution
order of 2026-10-22 — the same owner act that
gave the freeze rulings — once this freeze has
merged and the registration has been filed.
Stated openly, because earlier specs in this
program waited for the registration's approval
act before executing: this commission orders
the freeze, the filing, and the execution as
one end-to-end act, and the registration's
pending-approval state at execution is
recorded in the outcome record as it stands,
not rounded up.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
