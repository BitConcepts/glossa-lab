# Spec 054 — Freeze Record (Yadav Opening/Closing Signs: the Amended Falsifier Act under Battery NB-1)

> ## FROZEN — 2026-10-23
>
> This contract was frozen on 2026-10-23 under
> the owner's mini-gate approval of 2026-10-23
> (22:59 EDT, "Approve both mini-gates as
> specified"), which approved the amendment
> (`amendment.md`) as written — the amended
> statement, battery NB-1, the decision
> procedure, the verdict wordings, and the
> falsifier text — together with the generator
> act. The AEE lifecycle hooks ran over the
> register first (register recovered to
> 0.8-draft; `aee/freeze-aee-note.md`), and the
> digest in `freeze.json` was then computed
> **exactly once** over the recovered register
> and the finalised freeze texts (the Spec 035
> ordering). The freeze performed the falsifier
> append to `yadav_2009_arxiv_manual_002` and
> registered the claim-record hash **after**
> the append (§4). The freeze also files this
> spec's own OSF contract registration
> (`osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase-437** under this frozen contract,
> and only on a separate execution order.
> **Execution has not been ordered and has not
> started.** At the freeze itself no positional
> quantity was computed, no arm was counted,
> and no verdict was reached.

## 1. Basis

The unamended draft's freeze attempt of
2026-10-21 failed (`adjudication.md` §7): the
Phase-43 battery could not be pinned from the
record (OPEN-054-1) and the original opening
and closing sets could not be exhibited
(OPEN-054-2), so no freeze could append the
falsifier the design wrote, and §7.3 showed a
direct append would not have survived
regeneration of the claim store in any case.
The owner's rulings of 2026-10-23
(`adjudication.md` §8) adopted the §7.5(2)
design — an amended statement evaluated under
a new, explicitly defined battery, NB-1, which
produces its own sets in both arms — and
decided the §7.5(3) generator act with it. The
amendment drafted on those rulings is the
contract this freeze freezes; the mini-gate
approval (§9.1) approved it as specified, and
`amendment.md` and `spec.md` stand
byte-untouched by this act.

The freeze decided the open points as amended
(`adjudication.md` §9.2): OPEN-054-1 discharged
by NB-1's definition; OPEN-054-2 discharged as
a gate (the unexhibitability fact retained in
the record and in the SUPPORTED wording's
limits); OPEN-054-3 decided (floor N(s) ≥ 20,
DD-054-5's denominators confirmed as the
primary); OPEN-054-4 confirmed (crosswalk v1
is the crosswalk of record; DD-054-4 stands);
OPEN-054-5 answered by the amendment §5.3 null;
OPEN-054-6 reconciled as recorded (two
distinct measures, distinctly named);
OPEN-054-7 confirmed (DD-054-2's precedence in
the §5.5 form); OPEN-054-8 answered yes (the
OSF filing at this freeze); OPEN-054-9 decided
(**Phase-437**, DD-054-10). **DD-054-9** adopts
the DD-038-10 AEE gate reading for this spec.
DD-054-1, DD-054-2, DD-054-5, and DD-054-6 are
carried as the amendment states them;
DD-054-3 and DD-054-4 are confirmed as amended.

## 2. Pin verification (at the freeze)

Every pin the contract rests on was recomputed
in the foreground at the freeze act, against
the files as committed by this freeze:

| Input | SHA-256 | Bytes |
|---|---|---|
| `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json` — **before the append** (the §7.1 pin) | `904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3` | 13,230 |
| `glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json` — **after the append** (the pin this freeze registers) | `dcbaf64a728bc4ff7a0a1f76f2c867f924734cbe7f9c8cab2554d131b22533d7` | 15,402 |
| `outputs/phase43_all.json` | `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` | 15,047 |
| `glossa-indus/analysis/positional/hunt_tripartite_test.json` | `0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48` | 923 |
| `data/crosswalks/parpola_mahadevan_crosswalk_v1.json` | `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb` | 257,779 |
| `data/crosswalks/parpola_mahadevan_crosswalk_v1.csv` | `3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823` | 93,692 |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |
| `specs/054-yadav-opening-closing/claims.json` (the recovered register, 0.8-draft) | `ea161e47ed355af909af707f84e2ff5f4367b88f8160dd30d6e8938d8c7d24f0` | 64,454 |

The crosswalk files carry 766 rows, of which
762 are mapped pairs (4 unmapped) and 383 are
conflict pairs — the draft's §2 counts,
re-derived from the pinned file at this
freeze. The two arms' corpus layers (the
strict corpus; the Holdat layer) carry no pin
at the freeze by design (DD-054-3): each is
identified, exported, and pinned at step 0 of
the execution, fail-closed (amendment §6).

## 3. Machine record

`freeze.json` in this directory is the
canonical JSON record (framework026
`build_freeze`, computed by `build_freeze.py`
in this directory). Covered sources (nothing
else decides the question):

- `specs/054-yadav-opening-closing/freeze.md`
  (this document)
- `specs/054-yadav-opening-closing/spec.md`
- `specs/054-yadav-opening-closing/amendment.md`
- `specs/054-yadav-opening-closing/claims.json`
- `specs/054-yadav-opening-closing/adjudication.md`
- `specs/054-yadav-opening-closing/aee/freeze-aee-note.md`
- `specs/054-yadav-opening-closing/build_freeze.py`
- `backend/tests/test_spec054_freeze.py`

`tasks.md` and `osf-spec-registration.md` are
lifecycle bookkeeping and are not
digest-covered (the house rule since Spec 026:
plans change as work proceeds). The claim
store is not a covered source; its post-append
hash is registered in §2 and in the freeze
definition, and `test_spec054_freeze.py`
asserts it.

## 4. The falsifier append (the freeze's central act)

At this freeze, and not before, the following
text was appended to the record of
`yadav_2009_arxiv_manual_002` as its
`falsification_condition`, verbatim
(`amendment.md` §8):

> This claim, as evaluated under battery NB-1
> (the Spec 054 amendment, as frozen), is
> falsified if any of the following holds when
> the frozen battery is run on the frozen arm-1
> and arm-2 corpora: (1) either arm-1
> positional-strong set (opening or closing) is
> empty; (2) for either class, fewer than half
> of arm 1's positional-strong signs are also
> positional-strong in arm 2 in the same class,
> through the pinned crosswalk; or (3) the
> pooled cross-arm overlap of positional-strong
> signs does not exceed the 95th percentile of
> the 999-shuffle label-permutation null — the
> three conditions applied under the precedence
> rule of the Spec 054 amendment (§5.5).

The append is accompanied on the claim's
record by the dated note field
`spec054_falsifier_append_2026_10_23`, stating
that the design's original falsifier was never
appended because the 2026-10-21 freeze failed
before any append (`adjudication.md` §7.2),
and that this condition belongs to the amended
statement (amendment §2). The durability proof
(the amendment §7 standard) was run at this
freeze and is recorded at `adjudication.md`
§9.4: regeneration through the fixed generator
preserves the appended condition verbatim;
the final diff against the pre-append store is
exactly the two added fields, timestamps
apart. The note field is not in the
generator's carry-over list — a future
regeneration keeps the condition and drops
the note — stated openly here and in the note
itself; extending the carry-over was not
decided by any ruling and is not done. The
claim's recorded status (`strongly_supported`)
and stage (`explained`) are untouched by the
append, and no verdict of the future run moves
them (amendment §9).

## 5. What the freeze fixes

- **The amended statement** (amendment §2 /
  F054-C16): specific text-beginning and
  text-ending signs, in the exact sense NB-1
  makes checkable — a verdict on the amended
  statement is a verdict on that sentence, not
  on Yadav et al. (2010)'s original Phase-43
  statement.
- **Battery NB-1** (amendment §3): each
  layer's own numbering and segmentation, no
  re-segmentation inside a run; position
  classes initial / terminal / medial for
  sequences of length ≥ 2, length-1 sequences
  counted separately and entering no count;
  I + T + M = N exactly; classifiable iff
  N(s) ≥ 20; bands STRONG ≥ 2/3, MODERATE
  ≥ 1/2; opening-strong = INITIAL_STRONG,
  closing-strong = TERMINAL_STRONG.
- **The arms** (amendment §4): arm 1 the
  strict corpus (the Mahadevan-lineage V3
  layer as held in the database), identified
  and pinned at step 0; arm 2 the Holdat
  layer in its own numbering, through
  crosswalk v1 at the §2 pins.
- **The decision procedure** (amendment §5 /
  F054-C17): all four strong sets exhibited;
  reappearance per class, a class reappearing
  iff its rate is ≥ 1/2; DD-054-5's
  denominator discipline (unmapped /
  conflict-paired / below-floor-in-arm-2 count
  as not reappeared in the primary, each named
  TOO THIN / UNMAPPED / CONFLICT; the
  sensitivity reported with the same
  prominence; the verdict follows the
  primary); the pooled overlap against the
  999-shuffle label-permutation null (seed
  44054; nearest-rank 95th percentile); and
  DD-054-2's precedence in the §5.5 order.
- **The step-0 gates** (amendment §6), in
  order, fail-closed: pin checks (mismatch →
  INVALID); STRICT CORPUS NOT PINNABLE; TOO
  THIN (arm 1 under 30 sequences of length
  ≥ 3, or under 10 classifiable signs); SECOND
  ARM NOT RUNNABLE; determinism (identical
  second run, seed 44054; failure → INVALID).
  Retired closures: ORIGINAL SETS NOT
  EXHIBITABLE (fact retained), BATTERY NOT
  PINNABLE, BATTERY NOT REPRODUCED.
- **The verdict wordings** (amendment §9 /
  F054-C18), verbatim: SUPPORTED carries its
  limits inside the wording; NOT SUPPORTED
  names the condition that fired; INCONCLUSIVE
  is the §5.5 residue with the rates stated.
  The word RE-EARNED appears in no amended
  wording.
- **The Spec 045 fence** (amendment §10):
  Spec 045's "Holdat final-position
  concentration" and this spec's
  "closing-strong under NB-1" are different
  quantities, distinctly named in every
  outcome record.
- **The generator act** (amendment §7 /
  F054-C19): the regeneration carry-over in
  `glossa-indus/scripts/indus_claims.py`
  preserves `falsification_condition` by claim
  identity (landed in this PR as its own
  commit, `c9b2346e`).

## 6. Execution gate

Not satisfied, by design: execution requires
its own owner order after this freeze has
merged and the registration's approval act
has completed. Nothing in this freeze is an
execution order, and no step-0 gate has been
run under it.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
