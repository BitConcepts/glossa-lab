# Spec 060 — Freeze Record (The Holdat Site Effect: Margin Curve and Shared Population; Design D-23)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner as written on 2026-10-21
> (the campaign's Wave 2 freeze wave;
> `adjudication.md` §§1, 8). The AEE lifecycle
> hooks ran over the register first (register
> recovered to 0.7-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035 ordering).
> The freeze also files this spec's own OSF
> contract registration (DD-060-10;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-422**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> nothing has been computed: no margin-curve
> cell, no shared-population quantity, and not
> even the gate-0.4 census, which is an
> execution act under gate order.

## 1. Basis

The contract implements design D-23 (campaign
member 17): the two residues of
`STUDY-SPEC-024/F2-HOLDAT`, standing SETTLED —
CONTRADICTED at the declared margin 0.10
(Phase-384 v2 governing interval [0.0589,
0.0778], entirely below 0.10; descriptive V
0.1154 on 1,670 Holdat inscriptions), with its
family sibling F3-ICIT standing SUPPORTED at
the same margin (interval [0.1823, 0.2104];
V 0.2190; n = 5,410). Arm 1 publishes the F2
verdict as a function of the margin on the
design's fixed grid — a sensitivity display,
never a verdict. Arm 2 puts both layers on
the population they share (same sites, same
object types) and asks whether their effect
intervals then move toward each other. **No
verdict moves under this design, by its own
terms.**

The freeze decided the open points
(`adjudication.md` §8): **DD-060-10** (OPEN-060-1:
the spec files its own OSF contract registration
at the freeze, under campaign E-1 — the
DD-060-6 proposal adopted), **DD-060-11**
(OPEN-060-4, first part: DD-060-2 **confirmed** —
TOO THIN closes arm 2 only), **DD-060-12**
(OPEN-060-4, second part: DD-060-3 **confirmed** —
the shared type is SEAL: the Holdat layer
carries no object-type field and its type is a
constant, so the Holdat side enters whole and
the ICIT side is restricted to its recorded
SEAL class), **DD-060-13** (OPEN-060-4, third
part: DD-060-4 **confirmed** — period mix is
stated as not described where a layer carries
no period field in the fields its loader uses,
and **no period assignment is imported from
any other source**, including any Spec
041-style assignment), **DD-060-14** (OPEN-060-2:
no fresh synthetic calibration beyond gate
0.3's exact reproduction of both recorded
governing intervals), **DD-060-15** (OPEN-060-3:
the execution venue is the owner's machines at
the Phase-137 loaders' default paths, and both
held copies were verified at the freeze to hash
exactly to the §3 pins), **DD-060-16**
(OPEN-060-6: the execution phase is
**Phase-422**), and **DD-060-17** (the DD-038-10
AEE gate reading adopted). DD-060-1, DD-060-5,
and DD-060-9 are **confirmed** as drafted, and
the D-20 correction (adjudication §2) stands
exactly as drafted: arm 2 is written against
Spec 034's finished composition result
(ATTRIBUTED TO COMPOSITION, Phase-398), and no
wording in this frozen contract resurrects the
pre-034 framing of D-20 as a pending next step.

## 2. Pin verification (two routes, at the freeze)

Every §3 repository pin was re-derived **in the
foreground** by two independent routes — the
contents-API raw route and the git-blob route —
both at the merged record (`main` at
`a3509525fab64e22a4c053d7bbed14c7083a14d3`).
The two routes agree byte-for-byte on every
file, and every recomputed hash equals its pin:

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| `reports/phase137_results.json` | `18f86f45892526b947a4a7447201be9d69584ec96d33a1d18139309b9dc2a7a1` | 62,653 |
| `backend/scripts/phase137_site_repertoire.py` | `e00dacf4df8f52871b482e36ca0a37f66503c5f1b107ee835ac99fa21dfc8c86` | 28,765 |
| `reports/phase384_results.json` | `dda6092d9f4d368869a6e3a590948dfa97d02c5db50bf75868d6e055f0896aad` | 1,659 |
| `backend/scripts/phase384_stage2_margins_v2.py` | `3313394e6a716898cdfd440a46333ebd2b9136b77306413ed1514eab322a72a5` | 8,266 |
| `specs/026-rcph-framework-transfer/reruns/phase384-contract-v2.md` | `f0a67bd766ae28a33edc33553613bf9c50cc933df1bfbe2b5e1192d6571bbc75` | 2,161 |
| `specs/026-rcph-framework-transfer/reruns/phase384-freeze-v2.json` | `5749c6b89ac26be6333e0c20457bc320ca624c15f5ca65e689c107aa12b7b8e9` | 964 |
| `specs/034-matched-object-attribution/outcome.md` | `c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175` | 8,142 |
| `specs/024-evidence-integration/spec.md` | `a817f698fd5f2dd0a2d324d580d25cba41fc989762b20e0b77a4144a02d3ee25` | 38,517 |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |

The estimator pin and the contract pin are
verified a third way: both hashes also match
the Phase-384 freeze-v2 sources record carried
inside the pinned freeze-v2 file itself (its
recorded digest `4e6c78bc917c96a3…`).

The two held layers are not repository files;
their pins are verified two ways. First, the
values the pinned Phase-137 results record for
them: Holdat (`indus_corpus 2.csv`)
`62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`;
ICIT lineage (`inscriptions.csv`)
`c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`.
Second, the held copies themselves at the
Phase-137 loaders' default paths on the freeze
machine (DD-060-15) hash **exactly** to those
values. Gate 0.1 re-asserts the execution
venue's copies at execution time.

The facts the design rests on were re-read from
the pinned bytes in the same pass: the
Phase-137 record's analysis populations
(Holdat 1,670 inscriptions, 9 eligible sites,
table 9 × 98, χ² 745.953, V 0.1154; ICIT 5,410,
7 eligible sites, table 7 × 187, χ² 4966.362,
V 0.2190; eligible-site intersection of six:
Chanhu-daro, Dholavira, Harappa, Kalibangan,
Lothal, Mohenjo-daro); its strata definition
stating verbatim that the Holdat layer "carries
no object-type field and its inscriptions are
seal texts, so the type mix is a constant";
its `fields_used` lists (Holdat `letters,
position, seal_id, site`; ICIT `text, site,
type` — no period field in either) and its
confounder statement recording period as not
available in these layers; the Phase-384 v2
governing intervals (F2 basic [0.058939204306206666,
0.0777941604081594], percentile [0.15300258989494483,
0.17185754599689756], bootstrap median
0.16180470665653984; F3 basic [0.18229651053139323,
0.21036863506165235]; B = 9,999, seed 20261012);
and Spec 034's outcome (169 matched objects,
median distance 0.025694, residual 0.040340,
ATTRIBUTED TO COMPOSITION, the slice all
Mohenjo-daro seals). `backend/tests/test_spec060_freeze.py`
pins all of these facts so later drift fails
loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/060-f2-margin-curve/freeze.md` (this
  document)
- `specs/060-f2-margin-curve/spec.md`
- `specs/060-f2-margin-curve/claims.json`
- `specs/060-f2-margin-curve/adjudication.md`
- `specs/060-f2-margin-curve/aee/freeze-aee-note.md`
- `specs/060-f2-margin-curve/build_freeze.py`
- `backend/tests/test_spec060_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-060-10: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The scope fence** (spec §1 / F060-C01, C06,
  C15): two arms on F2's residue only. No
  verdict moves; nothing states which
  compilation is right, and no outcome
  establishes that there is no site effect in
  the Holdat layer.
- **Arm 1** (spec §5.1 / F060-C07, C08): the
  Phase-384 v2 estimator unchanged (B = 9,999,
  seed 20261012, basic interval governing), the
  margin grid fixed at 0.05 / 0.075 / 0.10 /
  0.125 / 0.15, each cell worded by the frozen
  family rule, the curve labelled sensitivity
  in every output, and gate 0.3 as the
  estimator check with no further synthetic
  calibration admitted as a gate (DD-060-14).
- **Arm 2's construction** (spec §5.2 /
  F060-C09): both layers restricted to the
  sites present in both analysis populations
  and to the shared type SEAL (DD-060-12) —
  Holdat whole, ICIT restricted to its
  recorded SEAL class; signs never pooled,
  mapped, or harmonised (F060-C14).
- **The step-0 gates** (spec §4 / F060-C11):
  input integrity (the venue's held copies
  asserted at the loaders' default paths,
  DD-060-15), exact population reproduction in
  both layers, and the estimator regression,
  each stopping the run as INVALID before any
  arm quantity; gate 0.4's census then governs
  arm 2 alone.
- **Arm 2's outcomes** (spec §§5.2, 6 /
  F060-C03, C04, C10, C12): exactly one of
  COMPOSITION EXPLAINS THE GAP (intervals
  overlap), COMPOSITION DOES NOT (they still
  exclude each other — the falsifier, stated
  in the §6.3 wording alongside Spec 034's
  finished attribution, designing no
  successor), or TOO THIN (fewer than 5 sites
  or fewer than 500 inscriptions in either
  layer; arm 2 only, DD-060-11).
- **Period mix** (spec §§5.2, 7 / F060-C13):
  described per layer only from what the
  layer carries; for both layers the frozen
  stated-unavailability wording stands
  (DD-060-13), and period is never treated as
  controlled.

## 5. What the freeze does not do

- **It computes nothing.** No margin-curve
  cell beyond the recorded 0.10 adjudication,
  no shared-population quantity, and not the
  gate-0.4 census: the ICIT SEAL-only counts
  on the six shared sites appear nowhere in
  the frozen record, by design.
- **It moves no verdict.** F2 stands
  CONTRADICTED at 0.10 and F3 stands SUPPORTED
  at 0.10, exactly as recorded; Spec 024's,
  Phase-137's, and Phase-384's files and
  verdicts are never edited by this spec.
- **It re-runs no part of Spec 034.** D-20 is
  complete; its verdict is a pinned input to
  this contract's reasoning, not a pending
  step, and this freeze designs, registers,
  and implies no successor attribution study.
- **It imports no period assignment.** The
  layers' period mix stands as not described
  on their own fields; no mapping from any
  other spec is admitted (DD-060-13).
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  (Phase-422) awaits the freeze merge, the
  OSF registration's approval act, and a
  separate execution order, in campaign Wave 3
  group 2.

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec060_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string, `0.7-draft` →
`0.7-MUTATED`) and the suite was run — the
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

Under DD-060-10 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-422, the hypothesis and its
falsifier under the corrected D-20 hand-off,
the margin grid and its sensitivity label, the
shared-population construction with the SEAL
reading (DD-060-12), the period
stated-unavailability wording (DD-060-13), the
estimator identity with gate 0.3 as its check
(DD-060-14), the venue and held-copy pins
(DD-060-15), the step-0 gates, the TOO THIN
floors closing arm 2 only (DD-060-11), and the
no-verdict-moves limit stated as a limit on
results. The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is
the parent's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution (Phase-422)
does not begin while the registration stands
pending: it awaits that approval act and a
separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
