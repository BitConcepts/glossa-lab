# Spec 064 — Freeze Record ("Sign 297 Is the Horned Tiger": an Identification Concordance, Successor to Spec 046)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the owner's approval of the same date
> (amendment package Item 5: build Spec 064,
> the successor to Spec 046, through freeze
> and OSF filing; `adjudication.md` §§5, 7).
> The AEE lifecycle hooks ran over the register
> first (register recovered to 0.7-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035 ordering).
> The freeze also files this spec's own OSF
> contract registration (DD-064-16;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-426**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> no list was opened for scoring, no descriptor
> was derived, and step C has not run.

## 1. Basis

The contract is the successor to Spec 046
(design D-18): the four-list concordance for
the fragment
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`
— "Sign value: 297 / the horned tiger, or
perhaps just 'tiger' generically" — with
Wells scored as SOURCE, never toward
CONSENSUS. Spec 046 (Phase-405, executed
2026-10-21; OSF dnts8 APPROVED + PUBLIC)
passed step 0, named the list at step 1.1,
and closed **IDENTIFICATION FAILED (sign
unmatched)** at step 1.2: Figure 2.6's drawn
forms did not survive the held copy's text
extraction (captions only), so no inspectable
drawn-form reference existed in the held
record. This successor performs the
preservation act Spec 046's outcome named —
the §6.2 reference record of the amendment
draft, committed in this directory as
`drawn-form-reference-297.json`, SHA-256
`33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4`
— and re-runs the question with step 1.2
satisfiable through it, under the amendment
draft §7 protocol frozen as spec §3 gate 0.4
and §4 steps D, C, M. Spec 046's frozen
record, outcome, and closure delivery
(SHA-256 `772db4df…`) stand unedited;
nothing in this spec patches them.

The preserved reference's continuity status
is **QUALIFIED** — anchored at family level
only (the P205 cell groups W289–W306 as one
Parpola sign's Wells counterparts; the thesis
plates show the 289–308 run as one bent-ray
family; no record fixes 297 individually from
the 2015 side). The qualification is
load-bearing in this contract: step C is
mandatory, its closure IDENTIFICATION FAILED
(continuity/discrimination not sustained) is
pre-registered, and the QUALIFIED status is
carried into reporting wherever the result
would be stated.

The freeze decided the draft's open points
(`adjudication.md` §7): **DD-064-14** (the
freeze basis — the owner's amendment package
Item 5 approval; DD-064-1…DD-064-13 stand as
drafted), **DD-064-15** (OP-064-1: Phase-426
allocated — verified unallocated in the repo
records at this freeze), **DD-064-16**
(OP-064-2: the spec files its own OSF contract
registration at the freeze, under campaign
E-1), **DD-064-17** (OP-064-3: the freeze and
filing acts are taken; execution is a separate
later act, not authorised by the freeze), and
**DD-064-18** (carried freeze matter: the
lists of record as Spec 046's freeze named
them, the lineage note standing in the
CONSENSUS wording, no separate dry-run sign,
and the DD-038-10 AEE gate reading adopted).

## 2. Pin verification (two routes, at the freeze)

Every §2 repository pin was re-derived **in
the foreground** by two independent routes —
the git-blob route and the contents-API raw
route — both at the merged record (`main` at
`e03f7832f99463d3496241676e21bf85e62fb9cc`),
with the working tree agreeing as a third
read. The routes agree byte-for-byte on every
file, and every recomputed hash equals its pin.

| Input | SHA-256 (both routes) |
|---|---|
| `data/crosswalks/canonical_sign_registry.csv` (803 rows) | `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` |
| `glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt` | `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` |
| `data/crosswalks/wells_segmentation_witness_v1.csv` (157 rows) | `ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da` |
| `specs/046-horned-tiger-concordance/concordance-297.json` | `772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf` |
| `glossa-indus/reports/phase104_claims_evaluation.json` | `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` |
| `specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json` | `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` |

The claim record recomputes to
`997fa33699ccce3feecfe0d09f6e6a1dbd165c05cd9f255939ad96e84bc99031`:
its bytes differ from Spec 046's draft pin
(`bd0f7abd…`) because the record now carries
Spec 046's dated first-check append of
Phase-405 beside the frozen entry (restored
to the record by PR #306); the fragment entry
itself — normalised claim, untested status,
created stage — is unchanged, verified by read
at this freeze. The preserved reference
record's digest was computed at its commitment
in this spec:
`33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4`
(7,168 bytes). The thesis PDF's digest
(`4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e`,
19,313,853 bytes) is the amendment draft's
verified value from the program's local store;
the file is not in the repository, and gate
0.4 asserts it on the local file at execution
before any plate is read.

The facts the design rests on were re-read
from the pinned bytes in the same pass: the
registry carries W297 only inside P205's
17-value cell, P297 is the "Ladder motif"
with `wells_ids` empty, and no registry
description names a tiger (0 of 803); the
witness carries no grapheme 297, and its
M297 row's Wells grapheme is 924; the held
text carries the passage verbatim at lines
2938–2941, the list-naming statements at
lines 414 and 665, and Figure 2.6 as captions
only at lines 868–880; the reference record
carries the bent-ray descriptor, the P205
family anchor as corroboration only, the five
named traps, and continuity_status QUALIFIED.
`backend/tests/test_spec064_freeze.py` pins
all of these facts so later drift fails loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/064-sign297-concordance-successor/freeze.md` (this
  document)
- `specs/064-sign297-concordance-successor/spec.md`
- `specs/064-sign297-concordance-successor/claims.json`
- `specs/064-sign297-concordance-successor/adjudication.md`
- `specs/064-sign297-concordance-successor/aee/freeze-aee-note.md`
- `specs/064-sign297-concordance-successor/build_freeze.py`
- `specs/064-sign297-concordance-successor/drawn-form-reference-297.json`
  (the preservation act is digest-covered: the
  successor cannot silently re-issue its own
  reference)
- `backend/tests/test_spec064_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-064-16: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The claim and its fence** (spec §1 / F064-C01,
  C02, C15): an outcome states only whether the
  published lists concur on the identification of
  the drawn sign as a tiger. Spec 046's records
  stand unedited; its IDENTIFICATION FAILED
  stands until this successor's execution
  produces its own outcome.
- **The preservation act** (spec §2 / F064-C05,
  C06; DD-064-10): the §6.2 reference record is
  committed in this directory at its pinned
  digest — citation-pinned Figure 2.6 reference,
  the thesis-plate descriptor with its recorded
  limitation, the P205 family anchor at its
  frozen status (corroboration only), the named
  traps, QUALIFIED continuity status, provenance
  chain, and license position. No images.
- **The step-0 gates** (spec §3 / F064-C05):
  input integrity (0.1, including the reference
  at its pinned digest), source producible
  (0.2), all four lists producible or citable
  (0.3), and reference producible (0.4 — thesis
  file digest asserted before any plate is read,
  plate page produced from the pinned local
  file; no substitute artefact). Each failure
  closes the run in its named class before any
  identification work.
- **The identification protocol** (spec §4 /
  F064-C06, C07; DD-064-11, DD-064-12): step D
  derives the descriptor twice, independently,
  and checks it against the preserved record
  (a material difference closes IDENTIFICATION
  FAILED (reference not sustained)); step C is
  mandatory — both derivations must affirm the
  descriptor picks out plate 297 and no
  neighbour in the 289–308 run, or the run
  closes IDENTIFICATION FAILED
  (continuity/discrimination not sustained);
  step M admits route 1 (registry, by drawn
  form) and route 2 (the preserved reference as
  the list's own entry) and no other route. The
  traps are asserted in every run record:
  P205's cell as identification, P297 "Ladder
  motif", witness M297 → 924, M180 as W297's
  identity, any number-only match.
- **The scoring and the total outcome set**
  (spec §5 / F064-C08–C10): carried from Spec
  046 — AGREE / DISAGREE / SILENT per list with
  `entry_present` on silence; Wells scored as
  SOURCE and never counted toward CONSENSUS;
  the mapping CONSENSUS / CONTESTED / PARTIAL
  CONCURRENCE / SINGLE-SOURCE total over every
  score pattern; the §5.3 wordings, each
  carrying the qualification sentence.
- **The delivery form** (spec §6 / F064-C11):
  `concordance-297.json` in **this** spec's
  directory, schema `glossa.concordance/1`,
  `producer_spec` `"064"`, produced on every
  terminal outcome — on a closure, an empty
  `signs` array plus a `closure` block; on
  CONTESTED, the feed records the dispute
  instead of picking a side. Asset A consumes
  only this successor's delivery if one is
  produced.
- **The reporting** (spec §8 / F064-C13): the
  carried elements plus the identification
  record — the reference's digest, both step D
  derivation sheets and their reconciliation,
  the step C statement, the route used and the
  traps asserted, and the QUALIFIED status
  stated wherever the result is stated.

## 5. What the freeze does not do

- **It identifies nothing.** No descriptor has
  been derived under this contract, step C has
  not run, no list has been opened for scoring,
  and no concordance row exists. The preserved
  reference is an input to step 1, checked by
  step D — not an identification.
- **It does not remove the qualification.**
  The frozen reference is QUALIFIED — it does
  not establish that 297's identification will
  survive its own step C discrimination check.
  Spec 046's IDENTIFICATION FAILED stands until
  a successor execution produces its own
  outcome.
- **It does not patch Spec 046.** Its frozen
  record, outcome, and closure delivery stand
  exactly as executed, and Asset A does not
  consume that closure delivery under this
  spec.
- **It supplies no run-time discretion.** Every
  value the gates read is in spec §§2–4 and
  this record. Anything missing or failing
  closes the run in its named class — nothing
  is repaired at run time, and no route may be
  constructed at run time.
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  (Phase-426) awaits the freeze merge, the OSF
  registration's approval act, and a separate
  execution order (DD-064-17).

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec064_freeze.py` were
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

Under DD-064-16 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-426, the claim and its
falsifier, the predecessor fence (Spec 046
closed IDENTIFICATION FAILED at step 1.2, its
closure delivery standing unedited), the
preserved drawn-form reference at its pinned
digest with its QUALIFIED continuity status
stated as a limit on the identification, the
identification protocol (step D twice-derived
with the reference checked not inherited,
step C mandatory with the pre-registered
closure IDENTIFICATION FAILED
(continuity/discrimination not sustained),
step M routes 1 and 2 only), the step-0 gates
including gate 0.4 (reference producible), the
four lists of record (Wells as SOURCE, never
toward CONSENSUS), the total outcome mapping
with its identification and step-0 closures,
the `concordance-297.json` delivery in this
spec's directory with its closure form, and
the identification-layer fence. The filing
record is `osf-spec-registration.md`,
completed by append after filing. The
registration stands **pending approval** after
filing; its approval act is the parent's
approval click on OSF's admin-notification
email, and no mail is handled by this freeze.
Execution (Phase-426) does not begin while the
registration stands pending: it awaits that
approval act and a separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
