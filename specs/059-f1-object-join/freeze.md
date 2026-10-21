# Spec 059 — Freeze Record (The Seal/Tablet Difference on a Better Join — Spec 024 F1 Rebuilt Through Object Identifiers; Design D-22)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner as written on 2026-10-21
> (the campaign's Wave 2 freeze wave;
> `adjudication.md` §§1, 8). The AEE lifecycle
> hooks ran over the register first (register
> recovered to 0.8-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035 ordering).
> The freeze also files this spec's own OSF
> contract registration (DD-059-10;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-421**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> no object-ID join has been built, no join
> census exists, and no F1 quantity on any
> enlarged set has been computed.

## 1. Basis

The contract implements design D-22 (campaign
member 16): Spec 024's family member F1 — within
sites, a text's final sign falls in the frozen
TERMINAL14 class at different rates on seals
than on tablets; standing SETTLED — SUPPORTED on
the joined subset of one lineage layer (odds
ratio 2.384, interval [1.847, 3.077], family
q = 0.00015; Phase-141 leave-one-site-out
STABLE) — re-tested on a corpus joined through
object identifiers rather than catalogue
concordance, gated at step 0 on whether the
better join is in fact better. The original
concordance join matched 2,895 of 5,679 lineage
rows (51.0%); the silent 49.0% is the claim's
named open point, and this spec is its
registered answer. If the object-ID join does
not clear the gate, the design closes at step 0,
unscored, with the census published as the
finding — a pre-registered outcome of the
frozen contract, not a failure of it.

The freeze decided the open points
(`adjudication.md` §8): **DD-059-7** (OF-059-1:
the gate bar's reading ADOPTED — the design's
stated 61.0%, ≥ 3,465 of 5,679 joined rows, with
the exact-points and relative readings refused
on the record and the arithmetic shown),
**DD-059-8** (OF-059-2: the single-test
correction family CONFIRMED — DD-059-4 stands;
the closed Spec 024 family's correction is not
re-run), **DD-059-9** (OF-059-3: the
object-identifier sources NAMED AND PINNED —
the lineage layer's `cisi` field carried as
`provenance.object_id` under the pinned
Phase-130 schema, per the pinned Spec 034
route-(b) construction, resolving against the
pinned catalogue layer's distinct objects),
**DD-059-10** (OF-059-4: the spec files its own
OSF contract registration at the freeze, under
campaign E-1), **DD-059-11** (OF-059-5: the gate
census, published either way, suffices as the
join's audit), **DD-059-12** (DD-059-3's verdict
precedence CONFIRMED), **DD-059-13** (the
execution phase is Phase-421), and **DD-059-14**
(the DD-038-10 AEE gate reading adopted).
DD-059-1, DD-059-2, and DD-059-5 are
**confirmed** as drafted, including the census
unit (the layer row) and the append-only
posture toward Spec 024's frozen record.

## 2. Pin verification (two routes, at the freeze)

Every committed §2 pin was re-derived **in the
foreground** by two independent routes — the
contents-API raw route and the git-blob route —
both at the merged record (`main` at
`a3509525fab64e22a4c053d7bbed14c7083a14d3`).
The two routes agree byte-for-byte on every
file, and every recomputed hash equals its pin.
The local-store pins were recomputed by two
further routes (Python `hashlib` and
`sha256sum`), agreeing:

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| `reports/phase136_results.json` | `11a0741317f50d9b8c2791fbfdd42ebec0f2a250d6f76809a2dec29fef857022` | 12,992 |
| `specs/024-evidence-integration/stage2a-freeze.md` | `c65a4b9ba7820f8dcf65fccfe64b8c271e488b036a754c76c45cd19f7cb4b94c` | 13,150 |
| `backend/scripts/phase136_terminal_type.py` | `d5ceec463bd271cd900fd2e5dbe2efb5b9e5f2b36444942b1d6cab12a6ee8871` | 22,853 |
| `reports/phase141_report.md` | `d442f8d2bcd1e7500c6df169f1dda0d8f48117c349e1710b34ff83011c7e4347` | 5,453 |
| `reports/phase136_137_138_stage2_report.md` | `6a4f5d2651ddc8316cf69d65ff6f4d29a7138ddc528c68310e6f07047eaed062` | 13,823 |
| `data/crosswalks/canonical_sign_registry.csv` | `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` | 111,583 |
| `specs/034-matched-object-attribution/outcome.md` | `c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175` | 8,142 |
| `specs/037-cisi31-concordance-spine/outcome.md` | `28e444f20e698b3533559aac3a4bc3efcbc50440e79427ae58f656642886a02a` | 16,077 |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |
| `data/intake/intake_dataset_schema_v1.json` (new pin, DD-059-9) | `b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b` | 6,197 |
| `backend/glossa_lab/phase398_matched_object.py` (new pin, DD-059-9) | `278f16b0ae8b02b77412cc925ac9e767110f5d5461729b73e8c122a9ff7673f0` | 40,104 |
| `backend/glossa_lab/intake.py` (new pin, DD-059-9) | `02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03` | 18,867 |
| ICIT-lineage (horus84) layer (local store, as recorded in the Phase-136 results) | `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef` | 1,190,884 |
| CISI catalogue vol. 1 (local store, as recorded) | `e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e` | 804,665 |
| CISI catalogue vol. 2 (local store, as recorded) | `e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9` | 1,431,631 |
| ICIT converted keyed layer v2 (local store; build record in `reports/phase398_results.json`) | `bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8` | 1,586,137 |

The local-store files are not committed, so the
freeze tests assert their pins as definition
constants here and assert the same values inside
the committed Phase-136 results file, which
records them — the Spec 038 form for held
inputs. Gate 0.1 at execution recomputes them
against these constants.

The facts the design rests on were re-read from
the pinned bytes in the same pass: the Phase-136
flow (5,679 → 2,895 matched / 2 ambiguous /
2,782 unmatched → 2,752 typed → 2,676
seals/tablets → 2,195 mapped → 2,062 in eligible
strata), its parameters (TERMINAL14's 14 signs,
B = 9,999, seed 20261009), the combined report's
family table (F1 raw p 0.0001 → q 0.00015 →
SUPPORTED), Phase-141's LOSO table (F1 STABLE;
all three dropped-site intervals excluding 1),
Spec 034 route (b)'s census (5,018 inscriptions
carrying a CISI reference, validation verdict
pass, joined on `provenance.object_id` only),
Spec 037's census (693 candidates: 269 VERIFIED
/ 341 CONFLICT (49.21%) / 83 UNRESOLVED), and
the catalogue layer's shape re-derived from the
pinned volume files (7,705 rows; 3,493 distinct
objects; vol. 1: 3,320 rows / 1,475 distinct
IDs; vol. 2: 4,385 rows / 2,019 distinct IDs;
one ID, `H-311`, in both volumes).
`backend/tests/test_spec059_freeze.py` pins
these facts so later drift fails loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/059-f1-object-join/freeze.md` (this
  document)
- `specs/059-f1-object-join/spec.md`
- `specs/059-f1-object-join/claims.json`
- `specs/059-f1-object-join/adjudication.md`
- `specs/059-f1-object-join/aee/freeze-aee-note.md`
- `specs/059-f1-object-join/build_freeze.py`
- `backend/tests/test_spec059_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-059-10: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The gate bar** (spec §3.4 / F059-C04):
  joined share ≥ 61.0% (≥ 3,465 of 5,679
  rows), adopted at DD-059-7 with its
  arithmetic shown and the two alternative
  readings refused on the record. Below the
  bar the execution closes at step 0 as
  JOIN GATE NOT MET, in the §3.5 wording,
  with the census as its finding.
- **The join construction** (spec §3.3 /
  F059-C05, C06): object identifiers only,
  from the sources named and pinned at
  DD-059-9; resolution to exactly one
  distinct catalogue object; the census unit
  is the layer row (DD-059-2); string
  identity is never a join key — the
  original concordance rule is re-run at
  gate 0.2 only to reproduce the recorded
  baseline, and contributes no row.
- **The step-0 gates** (spec §3 /
  F059-C07): input integrity (gate 0.1,
  asserting every §2 and DD-059-9 pin),
  original-join reproduction exactly
  (gate 0.2: 5,679 / 2,895 / 2 / 2,782, or
  INVALID), the object-ID census (gate
  0.3, under Phase-130 validation), and the
  gate comparison (gate 0.4) — in order,
  before any enlarged-set quantity exists.
- **The test machinery** (spec §4 / F059-C10):
  Phase-136's frozen flow unchanged on the
  enlarged set — TERMINAL14, eligibility
  (N ≥ 20, ≥5 Seals, ≥5 Tablets), the
  estimability rule, the CMH statistic, the
  permutation null (B = 9,999, seed
  20261009), and the MH odds ratio with its
  Robins–Breslow–Greenland interval.
  Unchanged means unchanged.
- **The correction** (spec §4.3 / F059-C13):
  the single-test family confirmed at
  DD-059-8; adjusted q = raw p.
- **The verdict mapping** (spec §5 /
  F059-C09, C11, C12): REPLICATED /
  WEAKENED / NOT REPLICATED by the fixed
  rules, with DD-059-3's precedence
  confirmed (DD-059-12); NOT ESTIMABLE as
  the frozen class for a gate-passed set
  failing estimability, cell counts shown,
  no p-value.
- **The reporting obligations** (spec
  §§4.4–4.5 / F059-C14): the LOSO rerun
  (descriptive; mints no verdict) and both
  covariate comparisons (joined vs
  unjoined; original joined set vs added
  rows), reported either way.
- **The append-only posture** (spec §7 /
  F059-C15): Spec 024's frozen records and
  SUPPORTED verdict stand unedited; this
  spec's outcome appends as a dated
  replication record beside them. The
  anchors file is asserted byte-identical
  before and after any execution; this
  spec moves no anchor.

## 5. What the freeze does not do

- **It does not itself join anything.** No
  object-ID join has been built, no census
  computed, no joined share exists, and the
  gate has not been decided — in either
  direction — by anything in this freeze.
- **It does not cover the gate by the back
  door.** The freeze names the identifier
  sources; it asserts nothing about their
  coverage of this layer beyond what the
  cited records state. If the census at
  execution falls below 3,465 joined rows,
  the frozen outcome is the §3.5 closure,
  and that closure is a completed result of
  this spec, not a defect in it.
- **It re-opens nothing.** Spec 024 F1's
  verdict, its family correction, and its
  frozen machinery stand exactly as
  recorded; the enlarged-set test is a new
  variant beside them.
- **It establishes nothing about what the
  difference means.** Genre, habit, and
  survival remain live explanations, named
  as such in every outcome wording.
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  (Phase-421) awaits the freeze merge, the
  OSF registration's approval act, and a
  separate execution order, in campaign
  Wave 3 group 2.

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec059_freeze.py` were
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

Under DD-059-10 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-421, the falsifier, the gate
bar as adopted (61.0% / ≥ 3,465 rows, the
refused readings named), the named and pinned
object-identifier sources, the string-identity
boundary, the frozen Phase-136 machinery
(TERMINAL14, CMH, B = 9,999, seed 20261009),
the single-test correction family, the verdict
mapping with its precedence, the step-0 gates
and the pre-written gate closure, the LOSO and
covariate reporting obligations, and the
append-only posture toward Spec 024's frozen
verdict. The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is
the parent's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution (Phase-421)
does not begin while the registration stands
pending: it awaits that approval act and a
separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
