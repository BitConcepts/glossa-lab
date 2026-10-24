# Spec 058 — Freeze Record (What Drove the Spec 023 Transcription Disagreement — Design D-21, Arm A Only)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner as written on 2026-10-21
> (the campaign's Wave 2 freeze wave;
> `adjudication.md` §§1, 7). The AEE lifecycle
> hooks ran over the register first (register
> recovered to 0.8-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035 ordering).
> The freeze also files this spec's own OSF
> contract registration (DD-058-14;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-420**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> no alignment, event, or share has been
> computed, and no localisation quantity exists.

## 1. Basis

The contract implements design D-21, arm A
(campaign member 15): the mechanism re-analysis
of the recorded Phase-132 pilot passes of
Spec 023. The claim under test is residue only —
`STUDY-SPEC-023/PHASE-132+383`, SETTLED —
CONTRADICTED (pilot exact-sequence agreement
0.20 against the frozen 0.80 floor; Phase-383
interval [0.10, 0.32]; every coder an AI agent
of a single model family). This spec tests no
part of that verdict. It tabulates the recorded
passes under rules fixed in advance and records
where the disagreement lives — signs, object
types, or segmentation choices — or records, in
pre-written words, that it does not localise
anywhere. Arm B (the human-coder calibration
arm) is blocked and out of scope (F058-C06);
no AI substitution for human coders is designed
anywhere in this spec.

The freeze decided the open points
(`adjudication.md` §7): **DD-058-14** (the spec
files its own OSF contract registration at the
freeze, under campaign E-1; DD-058-10 resolved
as proposed), **DD-058-15** (DD-058-11 resolved:
the Phase-132 store record set **survives
complete** on the machine holding the program's
main checkout — inventoried read-only at the
freeze at the pilot report's §9 counts, and
proven to be the pilot's record set by exact
reproduction of the committed metrics, the
adjudication taxonomy, and frame identity, all
run read-only with the pinned machinery;
production is **deferred to execution gate
0.2** exactly as drafted, the freeze pins no
store bytes and orders no separate preservation
act first, and the execution venue is the
machine holding that store), **DD-058-16**
(DD-058-12 resolved: gates 0.4–0.6 suffice; no
separate margins/census audit),
**DD-058-17** (Phase-420 allocated),
**DD-058-18** (the DD-038-10 AEE gate reading
adopted), and **DD-058-19** (DD-058-1 to
DD-058-9 and DD-058-13 confirmed as drafted,
including the object-type locus rule DD-058-8,
the segmentation proxy DD-058-3, the
involvement basis DD-058-6, and the MULTIPLE
LOCI combination class DD-058-9).

## 2. Pin verification (two routes, at the freeze)

Every §2.1 pin was re-derived **in the
foreground** by two independent routes — the
contents-API route and the git-blob route —
both at the merged record (`main` at
`770155dea66c5d5dde194728560aacf83c7514d0`,
after Spec 050's freeze merge). The two routes
agree byte-for-byte on every file, and every
recomputed hash equals its pin:

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| `specs/023-keyed-transcription-layer/spec.md` | `c2e5d1668b270266d5a20e30b1ec87cd4c1d5d2ffe786a45331a9a5ade1275d2` | 44,521 |
| `reports/phase132_pilot_metrics.json` | `e864fca57ecd1dc403c8e52ab9df6414372478d5781457f0aaca5e9084914554` | 21,070 |
| `reports/phase132_pilot_report.md` | `e1df32da86f7d3fd276d0ad546b3c351b58fd88b73f4468461f61075f6460e00` | 12,880 |
| `data/keyed_transcription/phase132_pilot_frame.json` | `a967144be0531c9d8396615d1ca07161dca0bc7347ca8c2c0d6a3c21a037a2ea` | 48,339 |
| `data/keyed_transcription/phase132_pilot_dataset_v1.json` | `adb596a1745470835e46c5148c1848d8408c45a030687d96427f00dbb6f74400` | 143,834 |
| `data/keyed_transcription/phase132_pilot_dataset_v1_meta.json` | `b2c607fae5f2602bb7b9634ff103f01df1de3885a1f1bbeeb6da3fc489cdefd4` | 5,815 |
| `reports/phase383_results.json` | `4e52942dc6be25fed4ab2004823a1d9353c9abfe6f5428e1050ee8d0d9a98334` | 2,870 |
| `reports/phase383_report.md` | `9f35f722611f6acd57e1ee05c9de0c8e95267ccf7f93b27eacb31bdff9cd08ca` | 3,400 |
| `backend/scripts/phase132_metrics.py` | `238dfafa3bac17dc0ad610ff4b7e6cf4fa577462d04cd31a3c612537cbe21984` | 24,363 |
| `backend/scripts/phase383_pilot_rescoring.py` | `b64b60de35d59bd99177e8ac3f68a80ffd2b0d31f8c75ea87312f69f927729ec` | 9,384 |
| `data/crosswalks/parpola_mahadevan_crosswalk_v1.json` | `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb` | 257,779 |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |

The facts the design rests on were re-read from
the pinned bytes in the same pass: the committed
metrics record exact-sequence agreement 0.20
(10/50, P and M), per-token agreement 0.4798
(95/198) over all 50 objects and 0.4286 (18/42)
on the gold sample, the gold error estimator
0.05 (2/40), and pass token totals 191 / 190 /
40 / 189; the Phase-383 record carries the
bootstrap interval [0.10, 0.32] (B = 9,999, seed
20261011), the CONTRADICTED verdict, and the
origin-group audit (one model family; effective
independent coder origin groups = 1); the frame
carries 50 objects — Mohenjo-Daro 25, Harappa
15, Lothal 6, Kalibangan 4; recorded types
Seals 34, Tablets 11, unrecorded 5; gold sample
10 (seed 20261009); and the dataset meta carries
content hash `7bdc73f5…` and the crosswalk hash
identical to the pinned crosswalk.
`backend/tests/test_spec058_freeze.py` pins all
of these facts so later drift fails loudly. The
lane-2 drafts file carrying the claim's record
(`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`,
SHA-256 `3f645c9a4…`) is asserted there too.

**The store evidence (DD-058-15).** Read-only
at the freeze, on the main-checkout machine:
the store at
`corpora/downloads/cisi_image_layer/phase132_pilot/`
holds `frame.json`, 50 files under `pass_a/`,
50 under `pass_b/`, 10 under `pass_gold/`, 50
under `adjudication/`, and `effort_log.csv`
with 320 data events — the pilot report's §9
inventory, complete. The pinned metrics module
(the stale checkout's copy hashes to its pin
above, as do its crosswalk, metrics, and frame
files) recomputed the committed metrics file
from that store **exactly** — full-record
equality — and the recomputed taxonomy
(identity 93, legibility 45, count 11, key 10,
orientation 2, order 1; total 162) and frame
identity (the store's frame list equals the
committed frame's list in full) also match
exactly. That is the evidence the freeze's
DD-058-15 ruling stands on; it is not an
execution, and gates 0.2–0.5 still run in order
at execution on the produced set.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/058-transcription-disagreement-mechanism/freeze.md` (this
  document)
- `specs/058-transcription-disagreement-mechanism/spec.md`
- `specs/058-transcription-disagreement-mechanism/claims.json`
- `specs/058-transcription-disagreement-mechanism/adjudication.md`
- `specs/058-transcription-disagreement-mechanism/aee/freeze-aee-note.md`
- `specs/058-transcription-disagreement-mechanism/build_freeze.py`
- `backend/tests/test_spec058_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-058-14: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The scope fence** (spec §1 / F058-C01, C16):
  the mechanism account for the recorded pilot
  passes only. Nothing about human coders, the
  0.80 floor, or any codebook revision.
- **The inputs** (spec §2 / F058-C07): the
  §2.1 committed pins, re-asserted at this
  freeze (§2 above), and the Phase-132 store
  record set produced at execution under gate
  0.2 — no other data, no re-coding, no images.
- **The step-0 gates** (spec §3 / F058-C09):
  0.1 committed-record integrity (INVALID),
  0.2 record-set production with inventory and
  per-file manifest (PILOT-PASS RECORDS NOT
  PRODUCIBLE), 0.3 frame identity (INVALID),
  0.4 exact reproduction of the committed
  metrics (INVALID), 0.5 adjudication-taxonomy
  cross-check (INVALID), 0.6 the mismatched-
  population census (40 objects on the committed
  record) — fail-closed, in order, before any
  event is tabulated. DD-058-16: these gates
  suffice; no separate audit.
- **The machinery** (spec §4.1–4.2 / F058-C08,
  C10): P space primary by the frozen
  derivation, the frozen minimum-edit alignment
  imported unchanged from the pinned metrics
  module, mismatch events typed SUBSTITUTION /
  INDEL, first divergence per mismatched object.
- **The tabulations** (spec §4.3–4.4 / F058-C10,
  C15): T1 by sign (involvement counts, total
  ranking, top-10 share over summed involvement,
  frequency shares over 381 tokens), T2 by
  recorded object type, T3 by divergence type;
  UNK and UNMAPPED counted as recorded in the
  primary, the UNK-excluded secondary descriptive
  only, the mandatory UNK headline sentence, and
  the M-space sensitivity descriptive only.
- **The locus rules** (spec §5.1 / F058-C11,
  C12, C13): SIGNS at top-10 involvement share
  at least 50% (with the design's UNIFORM /
  BETWEEN companion states); OBJECT TYPES at
  at least 50% of events plus a 10-point
  enrichment margin, Unrecorded unable to fire
  (DD-058-8, confirmed); SEGMENTATION at INDEL
  share at least 50% (the registered proxy,
  DD-058-3, confirmed).
- **The headline mapping** (spec §5.2 /
  F058-C14): exactly one of LOCALISED TO SIGNS,
  LOCALISED TO OBJECT TYPES, LOCALISED TO
  SEGMENTATION, LOCALISED TO MULTIPLE LOCI
  (DD-058-9, confirmed), or NOT LOCALISED,
  determined mechanically by the set of loci
  that fire, in the pre-written wordings — with
  PILOT-PASS RECORDS NOT PRODUCIBLE and INVALID
  as the step-0/stop classes.

## 5. What the freeze does not do

- **It does not itself localise anything.** No
  alignment has been run under this spec, no
  event has been tabulated, the event total E
  is unstated, and the 40-object census is gate
  0.6's product at execution, not a freeze
  product. The freeze's store check (§2)
  reproduced the pilot's already-published
  aggregates as adjudication evidence; it
  computed no §4 quantity.
- **It produces and pins no store bytes.**
  Production, inventory, and manifest are
  execution gate 0.2's acts (DD-058-15); the
  freeze-time manifest is inspection evidence,
  recorded in the freeze workpapers, not in
  this record.
- **It changes no verdict.** The pilot still
  failed, and stays failed:
  `STUDY-SPEC-023/PHASE-132+383` remains
  CONTRADICTED exactly as recorded, and Spec
  023's files stand unedited. The anchors file
  is asserted byte-identical before and after
  any execution; this spec moves no anchor.
- **It designs and runs nothing of arm B.** The
  human-coder arm stays blocked on the owner's
  hold; no AI substitution exists in this spec.
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  (Phase-420) awaits the freeze merge, the
  OSF registration's approval act, and a
  separate execution order, in campaign Wave 3
  group 2.

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec058_freeze.py` were
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

Under DD-058-14 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-420, the hypothesis and its
falsifier, the §2.1 pins, the store posture and
the DD-058-15 ruling (store survives complete;
production deferred to gate 0.2, fail-closed,
with the NOT PRODUCIBLE closure and its named
unblocking act), the step-0 gates 0.1–0.6, the
frozen machinery and event definitions, the
T1–T3 tabulations with the UNK handling, the
three locus rules with their draft-fixed
readings confirmed (DD-058-19), the headline
mapping including MULTIPLE LOCI, and the
limits stated as limits on results: nothing
about human coders, the floor, or the codebook,
and the SEGMENTATION headline carrying its
registered proxy meaning. The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is
the parent's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution (Phase-420)
does not begin while the registration stands
pending: it awaits that approval act and a
separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
