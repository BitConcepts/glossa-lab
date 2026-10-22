# Spec 053 — Freeze Record (Yadav's Zipf Fit with Proper Controls: Design D-07, Arm A Only)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner AS WRITTEN on 2026-10-21
> (the campaign's Wave 2 freeze wave;
> `adjudication.md` §§1, 8). The AEE lifecycle
> hooks ran over the register first (register
> recovered to 0.7-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). The freeze also files this spec's
> own OSF contract registration (DD-053-17;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-413**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed, and a separate execution
> order is given. At the freeze itself no system
> has been fitted, no control count has been
> entered, and no corpus has been exported.

## 1. Basis

The contract implements design D-07, arm A only
(campaign member 6): one identical
Zipf-Mandelbrot fit applied to the Indus strict
corpus, to the named non-linguistic control
systems, and to a linguistic positive control,
with the subsampling and split/merge
sensitivities — producing an honest strength
label for the settled claim
`yadav_2009_arxiv_manual_001` (strongly
supported; recorded exponent about 1.35), not a
new verdict on it. Arm B is not a member of
this spec (campaign E-3; §12 of the spec).

The freeze decided the open points
(`adjudication.md` §8). The central ruling is
**DD-053-11 (option (a))**: the estimator of
spec §4.2 is specified completely at the freeze
— model, normalisation, objective, grid,
refinement, self-test, seeds, and the control
constructions — as a freeze-stage design
decision, and the "identical to Phase-43"
reading is honestly **retired**. The evidence,
re-verified first-hand at this freeze:
`outputs/phase43_all.json` (SHA-256
`78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4`)
carries no Zipf fit — no exponent, no Mandelbrot
parameters, no fitting procedure, not even the
word "Zipf" — and no Phase-43 Zipf estimator is
on `main`; Yadav's recorded ~1.35 rests on the
claim file's evidence string alone. Option (b),
a freeze failure, does not arise, because the
spec's falsifier never depended on a Phase-43
fit: it fires iff a named non-linguistic control
fits as well as or better than the Indus strict
corpus under §4's one estimator — a comparison
internal to this spec. The spec therefore tests
Yadav's recorded 1.35 value under the named
§4.2 estimator, as context; its claims and
falsifier are restated to say exactly that
(claims edited at draft stage, before the
digest; IDs stable).

The remaining rulings: **DD-053-12** (gate 0.3's
identify-export-pin posture and the strict
population confirmed; the full inventory is
sensitivity S3), **DD-053-13** (the named control
systems and bibliographic pins confirmed; gate
0.4 is the fixed pin source for the control
tables, entered as cited data before any fit,
failing closed as CONTROL SET FREEZE FAILED;
no second positive control), **DD-053-14**
(the census floors confirmed: 50 types, 2,000
tokens), **DD-053-15** (the comparison rule
confirmed: ε = 0 in the verdict, the 0.02 band
reporting-only), **DD-053-16** (the Yule–Simon
synthetic process confirmed: ρ = 0.10, seed
20261021, 99 replicates), **DD-053-17** (the
spec files its own OSF contract registration at
the freeze, under campaign E-1), **DD-053-18**
(Phase-413 allocated), and **DD-053-19** (the
DD-038-10 AEE gate reading adopted; the one
negation-conflict challenge, F053-C01/C04,
adjudicated as no contradiction). DD-053-1,
DD-053-2, DD-053-4, DD-053-5, DD-053-6,
DD-053-9, and DD-053-10 stand as drafted.

## 2. Pin verification (two routes, at the freeze)

Every §2 pin was re-derived **in the
foreground** by two independent routes — the
contents-API raw route and the git-blob route —
both at the merged record (`main` at
`3af269f660a9368e898cdece41132200d31b87cc`).
The two routes agree byte-for-byte on every
file, and every recomputed hash equals its pin:

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json` | `904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3` | 13,230 |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |
| `data/crosswalks/sign_crosswalk_master.csv` | `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` | 18,568 |
| `backend/glossa_lab/data/mahadevan_parpola_crosswalk.json` | `9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b` | 6,394 |
| `outputs/phase43_all.json` | `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` | 15,047 |

The claim file's hash is carried as a freeze
definition constant in the Spec 038 form: the
extracted-claims store is regenerated by the
backend suite, so the freeze tests assert the
constant plus the `manual_001` facts on the live
file, never a live-file hash on that store.

The facts the design rests on were re-read from
the pinned bytes in the same pass: the claim
record's `manual_001` entry reads strongly
supported, stage explained, normalised claim
"Indus script sign frequencies follow a
Zipf-Mandelbrot distribution", falsification
condition "If frequency distribution deviates
from Zipf-Mandelbrot law", and evidence string
"Phase-43: V3 Zipf exponent ~1.35
(super-Zipfian)"; the anchors census is 287
anchors of which **94** carry
`strict_sa_independent`; and the Phase-43 file
carries the corpus census and positional/SA
tables with **no Zipf fit** — the ground for
DD-053-11.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`,
computed by `build_freeze.py` in this
directory). Covered sources (nothing else
decides the question):

- `specs/053-yadav-zipf-controls/freeze.md` (this
  document)
- `specs/053-yadav-zipf-controls/spec.md`
- `specs/053-yadav-zipf-controls/claims.json`
- `specs/053-yadav-zipf-controls/adjudication.md`
- `specs/053-yadav-zipf-controls/aee/freeze-aee-note.md`
- `specs/053-yadav-zipf-controls/build_freeze.py`
- `backend/tests/test_spec053_freeze.py`

`plan.md`, `tasks.md`, and `outcome.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds). There is no `plan.md` in this
spec's directory; `tasks.md` carries the
lifecycle.

## 4. What the freeze fixes

- **The estimator** (spec §4.2 / F053-C06,
  C07; DD-053-11): the Zipf-Mandelbrot model
  with C fixed by normalisation, fitted by
  minimising squared log residuals over the
  stated deterministic grid and refinement,
  one implementation for every system; the
  primary quantity NRMSE_log; the verdict rule
  at ε = 0 with the 0.02 NEAR MISS band
  reporting-only (DD-053-15). No Phase-43
  identity is claimed anywhere in the frozen
  contract.
- **The control set** (spec §3 gate 0.4 /
  F053-C08; DD-053-13, DD-053-16): N1
  Mesopotamian numerical signs, N2 heraldic
  charges, N3 the pinned Yule–Simon synthetic
  inventory (ρ = 0.10, seed 20261021, 99
  replicates, size-matched), and P1 Linear B —
  entered whole as cited data and frozen before
  any fit, or the run closes CONTROL SET
  FREEZE FAILED.
- **The population and its gates** (spec §3 /
  F053-C09, C10; DD-053-12, DD-053-14): the
  strict distribution is the primary, pinned at
  gate 0.3; the estimator self-test at gate 0.2
  (planted α = 1.20, q = 2.0, V = 200,
  N = 50,000, seed 20261021; recovery within
  ±0.10 / ±1.0); the census floors at 50 types
  and 2,000 tokens.
- **The outcome set** (spec §§4.4–4.5, 6 /
  F053-C03, C04, C12, C13): SEPARABLE, NOT
  SEPARABLE, or COMPARISON UNINFORMATIVE after
  the gates, with the positive-control validity
  condition checked first; the step-0 closures
  TOO THIN, STRICT CORPUS NOT PINNABLE, CONTROL
  SET FREEZE FAILED, and INVALID — all in §6's
  pre-written wordings.
- **The fences** (spec §7 / F053-C01, C05,
  C15): the outcome is a dated strength label
  appended to the claim's record; no verdict
  changes; no outcome is evidence that the
  script encodes language, or that it does not;
  three named systems are not all non-language;
  the strict fit's exponent is never quoted as
  Yadav's exponent reproduced or contradicted.
- **The sensitivities** (spec §5 / F053-C11):
  S1 inscription-level subsampling, S2 the
  crosswalk's split/merge variants, S3 the
  full-inventory fit reported beside the
  recorded ~1.35 — reported alongside, never
  verdict-changing.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
