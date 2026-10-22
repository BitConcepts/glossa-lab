# Spec 063 — Freeze Record (Sign 821, Identification Successor to Spec 056)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the owner's approval of the same date
> (amendment package Item 5: take the sign 821
> successor through freeze and OSF filing;
> `adjudication.md` §§1, 7). The preservation
> act named in Spec 056's outcome and in the
> authoritative draft's §9.1 is performed
> inside this freeze: `drawn-form-reference-821.json`
> is committed in this directory with exactly
> the amendment draft §6.1 contents, and its
> SHA-256, computed at commitment, is pinned
> in §2 below and in `freeze.json`. The AEE
> lifecycle hooks ran over the register first
> (register recovered to 0.6-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). The freeze also files this spec's
> own OSF contract registration (DD-063-9;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-425** under this frozen contract,
> and only after the freeze has merged, the
> registration's approval act has completed —
> the parent's approval click on OSF's admin
> notification — and a separate execution
> order is given. At the freeze itself no
> derivation has been performed, no plate has
> been read under this spec, and nothing has
> been identified.

## 1. Basis

The contract is the successor to Spec 056
(campaign member 12, design D-17), which
executed at Phase-418 on 2026-10-21 and
closed **IDENTIFICATION FAILED**: its two
independent extraction passes recovered
candidate K-1 — "sign 821, in the Dholavira
signboard contexts, has a meaning of 'city',
either as a determinative or as a word"
(Wells 2015, printed p. 92) — which passed
the recovery test's argument conditions
R-1, R-2, R-4 and R-5 and failed R-3 only,
because the drawn sign could not be
identified by either route the frozen test
allowed (the registry carries no W821 entry;
Figure 2.6's entry is graphic-only in the
held text). Spec 056's outcome named the
unblocking act: the preservation, as a
committed and hashed record, of an
inspectable drawn-form reference for Wells's
sign 821. The amendment draft (Amendment
Queue Item 5) established the lawful text
form of that reference — for 821, by two
independent routes that agree: the
composition route (the book's own 'Doubled
Signs' formation text plus the registry's
drawn description of the base sign) and the
thesis-plate descriptor route (glyph
inspection of Figure 3.2 in the open-deposit
Wells 2006 PhD thesis) — and drafted the
reference record (§6.1), the identification
protocol (§7), and this successor's charter
(§8). This freeze preserves the reference
inside the spec, freezes the protocol with
the new third route (composition) and its
justification, and fixes the successor's
three outcomes: RECOVERED, IDENTIFICATION
FAILED on the new record, or CLOSED AT
STEP 0. Spec 056's record is cited, never
edited; its IDENTIFICATION FAILED stands
until a successor execution replaces the
outcome with its own.

The freeze decided the draft's open points
(`adjudication.md` §7): **DD-063-9** (the
spec files its own OSF contract registration
at the freeze, under campaign E-1),
**DD-063-10** (OP-063-1: Phase-425 allocated
— verified unallocated in the repo records
at this freeze; Phase-424 was Spec 062's),
**DD-063-11** (OP-063-3: route 3, the
composition route, adopted exactly as
drafted, with the draft §7 justification
carried into spec §5 step M verbatim in
substance), **DD-063-12** (OP-063-4: the
step-0 class names confirmed — INPUT PIN
MISMATCH, THESIS FILE PIN MISMATCH,
REFERENCE NOT PRODUCIBLE), **DD-063-13**
(OP-063-5: the freeze and filing acts taken
under the owner's approval; execution not
authorised), **DD-063-14** (every §2 pin
re-verified two routes before freezing; the
preserved reference's digest pinned as
computed at commitment), and **DD-063-15**
(the DD-038-10 AEE gate reading adopted).
DD-063-1 to DD-063-8 are **confirmed** as
drafted, including the three-word outcome
set (DD-063-3), the preservation act inside
this spec (DD-063-4), and step C passing on
the anchors' agreement for 821 (DD-063-6).

## 2. Pin verification (two routes, before freezing)

Every repository pin below was re-derived
**in the foreground, before freezing** by two
independent routes — the git-blob route and
the contents-API raw route — both at the
merged record (`main` at
`e03f7832f99463d3496241676e21bf85e62fb9cc`),
the routes agreeing byte-for-byte on every
file, and every recomputed hash equalling
its pin. The thesis PDF is a local file, not
a repository file: its digest was asserted
on the local file itself in the same pass.

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| `glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt` | `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` | 268,195 |
| `data/crosswalks/canonical_sign_registry.csv` | `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` | 111,583 |
| `data/crosswalks/wells_segmentation_witness_v1.csv` | `ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da` | 67,692 |
| `specs/056-sign821-recovery/freeze.json` | file `8a7d13904d3e06cca0fcabbc0ab9d25af7c72176c5e1d7f3bdb957fd9075d759`; its digest `64c28ce1aa379d9b47d230544e372b3446906d53422fe16da51fbce3bc94a63e` | 14,137 |
| `specs/056-sign821-recovery/outcome.md` | `ff16184aa265b68358865c51e8f43dc9c9ec40688a53614792640f1d2e2d844e` | 24,515 |
| `specs/056-sign821-recovery/extraction-record.md` | `ad4a3f747d6ae4e0f13ae984c1169bd4a94570625e7dcc199146ff2ef73fb6ab` | 17,773 |
| `glossa-indus/reports/phase104_claims_evaluation.json` | `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` | 17,475 |
| `specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json` | `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` | 127,338 |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |
| Passage slice (held text lines 2783–2871) | `51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604` | 5,354 |
| **Preserved reference** `specs/063-sign821-identification-successor/drawn-form-reference-821.json` | `695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999` | 5,689 |
| Thesis PDF (local file; asserted on the file) | `4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e` | 19,313,853 |

The claim file's freeze-time hash
(`bd0f7abd…`) is carried as a freeze
definition constant in the Spec 038 form: the
extracted-claims store is regenerated by the
backend suite, so the freeze tests assert the
constant plus the fragment's facts on the live
file, never a live-file hash on that store.
The live file's _0001 entry was asserted in
the same pass: present, wording, UNTESTED
status and created stage as the frozen record
states, and carrying the appended
`spec056_closure` entry (Phase-418,
IDENTIFICATION FAILED, the unblocking act
named).

The facts the design rests on were re-read
from the pinned bytes in the same pass: the
registry carries **803 rows**, no W821 value
in any row (sole or inside a multi-value
cell), W820 solely on P378 ("Wheel with 6
spokes with even angles", M391), and the
`Yunmapped_0821` trap row (Yajnadevam glyph
identifier, empty `wells_ids`, frequency 10);
the witness carries **157 rows** with no
grapheme 821 in any `wells_graphemes` field;
the held text carries the list-naming lines
(414, 665), the Figure 2.6 captions (868,
872, 876, 880), the K-1 suggestion (2835–2836,
printed p. 92), the sign 861 passage
(2848–2853), the Figure 6.13 caption (2860;
list of figures 176), and the 'Doubled
Signs' formation passage (3691–3704) with
Table AII.4's caption (3705–3706);
**Phase-425 was verified genuinely free**
(the frozen records allocate Phase-419…
Phase-424 to Specs 057… 062; a repository
code search for "Phase-425" / "phase425"
returns no record; the root LEDGER allocates
none; no phase425 report, script, or graph
module exists). `backend/tests/test_spec063_freeze.py`
pins all of these facts so later drift fails
loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/063-sign821-identification-successor/freeze.md` (this
  document)
- `specs/063-sign821-identification-successor/spec.md`
- `specs/063-sign821-identification-successor/claims.json`
- `specs/063-sign821-identification-successor/adjudication.md`
- `specs/063-sign821-identification-successor/drawn-form-reference-821.json`
- `specs/063-sign821-identification-successor/aee/freeze-aee-note.md`
- `specs/063-sign821-identification-successor/build_freeze.py`
- `backend/tests/test_spec063_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-063-9: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The preservation act** (spec §2 /
  F063-C05): the drawn-form reference for
  Wells's sign 821, committed in this
  directory with exactly the amendment draft
  §6.1 contents (schema
  `glossa.drawn-form-reference/1`), its
  SHA-256 `695dd35d…` computed at
  commitment and pinned in this record and
  in `freeze.json`. Text only; no image is
  committed anywhere in this spec.
- **The candidate and its record** (spec §§1,
  4 / F063-C02, C08): candidate K-1, with
  R-1, R-2, R-4 and R-5 of record from Spec
  056's executed extraction on the pinned
  passage, and R-3 the one open condition,
  run afresh under §5.
- **The step-0 gates** (spec §3 / F063-C06):
  input integrity (INPUT PIN MISMATCH);
  the thesis file asserted to its frozen
  digest on the local file **before any
  plate is read** (THESIS FILE PIN
  MISMATCH); the reference producible at its
  pinned digest with the plate page produced
  from the pinned file (REFERENCE NOT
  PRODUCIBLE). Each closes the run in its
  named class before any derivation exists.
- **The identification protocol** (spec §5 /
  F063-C07, C09): step D — two independent
  descriptor derivations, without sight of
  each other or of the drafted descriptor
  wording, reconciled by recorded features,
  unsettled disagreement resolving against
  identification, and the reconciled
  descriptor required to agree with the
  preserved record's descriptor (a material
  difference closes as IDENTIFICATION FAILED,
  reference not sustained); step C —
  continuity passes on the anchors' agreement
  (the formation passage, the P378 registry
  anchor, the plate agreement), the plate
  number alone anchoring nothing; step M —
  exactly one of three frozen routes: route 1
  (registry, by drawn form, no fallback to
  P378, which is the base sign), route 2 (the
  list's own entry through the preserved
  reference), and **route 3 (composition;
  NEW)** — the formation passage plus the base
  sign's registry drawn description, with the
  plate confirmation as its check, frozen
  with its justification: every step is a
  drawn form (the base sign's registry
  description, the doubling operation from the
  source's own appendix, the plate's drawn
  pair), and the number is used only to
  locate them. Traps asserted in every run
  record: `Yunmapped_0821`, sign 861, P378 as
  the target, and number-only matching in any
  form.
- **The outcomes** (spec §6 / F063-C10):
  exactly one of RECOVERED, IDENTIFICATION
  FAILED (on the new record, naming the
  failed limb — step D, step C, or step M),
  or CLOSED AT STEP 0, under the pre-written
  §6.1 wordings. No retirement word exists
  under this spec (DD-063-3).
- **What the outcomes write** (spec §7 /
  F063-C11, C12, C15): appends only. On
  RECOVERED, the restatement entry on the
  fragment's own record, the claim entering
  at created, untested, with its
  designed-never-run test note (the
  DD-056-6 / DD-056-17 pattern). On
  IDENTIFICATION FAILED, the outcome record,
  the dated closure entry, the LEDGER entry,
  and the graph node. Spec 056's record is
  cited, never edited.

## 5. What the freeze does not do

- **It does not identify sign 821.** The
  protocol is fixed, not run: no derivation
  has been performed, no plate has been read
  under this spec, step C has not been
  stated from a run record, and no route has
  been attempted. **Freezing the reference
  does not establish that sign 821 is
  identified** — identification is the
  execution's step D/C/M work, which has not
  run; Spec 056's IDENTIFICATION FAILED
  stands as the record until a successor
  execution replaces the outcome with its
  own.
- **It does not recover K-1, and it retires
  nothing.** Recovery is an execution
  outcome under Phase-425, not a freeze
  act; no test-design note arises at the
  freeze (that note belongs to a RECOVERED
  outcome, designed at that point).
- **It decides nothing about what sign 821
  means.** Not its reading, meaning,
  classification, or distribution — and
  nothing about sign 861, sign 297, or any
  other sign or claim.
- **It changes no prior record.** Spec 056's
  spec, freeze, extraction record, and
  outcome stand exactly as executed; the
  fragment stands UNTESTED at created with
  its `spec056_closure` append. The anchors
  file is asserted byte-identical before and
  after any execution; this spec moves no
  anchor.
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  (Phase-425) awaits the freeze merge, the
  OSF registration's approval act, and a
  separate execution order (DD-063-13).

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec063_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string, `0.6-draft` →
`0.6-MUTATED`) and the suite was run — the
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

Under DD-063-9 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-425, the falsifier, the
preservation act and the reference's pinned
digest, the step-0 gates in their three named
classes (including the thesis-file assertion
before any plate read), the identification
protocol (step D double derivation, step C
continuity on the anchors' agreement, step M
routes 1–3 with route 3's justification), the
traps, the three-word outcome set with no
retirement word, the recovered claim's
lifecycle position (created, untested,
designed-never-run test note), and the fence
stated as a limit on results: freezing the
reference does not establish that sign 821 is
identified. The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is
the parent's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution (Phase-425)
does not begin while the registration stands
pending: it awaits that approval act and a
separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
