# Spec 069 — Freeze Record (Hunt Depicted-Kind Classification: The Asset A Build, Contract of Spec 045 §§2–3)

> ## FROZEN — 2026-10-22
>
> This contract was frozen on 2026-10-22 under
> the owner's freeze rulings of 2026-10-22 for
> the Hunt chain (every open item ruled per the
> draft's stated default; a predecessor's
> decided position standing where the draft
> carries one; phase numbers allocated by the
> owner; an OSF registration filed for each
> spec at its freeze). The rulings are recorded
> in `adjudication.md` §8 (DD-069-6 …
> DD-069-12). The AEE lifecycle hooks ran over
> the register first (recovered at the freeze
> from 0.5-draft to 0.9-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). The freeze also files this spec's
> own OSF contract registration (DD-069-10;
> `osf-spec-registration.md`, completed by
> append after filing). Execution runs as
> **Phase 432** under the same owner act's
> chain order — freeze, merge, registration,
> execution — in the commissioned dependency
> order Spec 069 → Spec 070 → Spec 071. At the
> freeze itself nothing has been entered,
> joined, or computed: Asset A does not exist
> yet, and no depicted-kind label for any sign
> has been produced by this freeze.

## 1. Basis

Spec 045 froze a careful contract for building
the depicted-kind classification the Hunt
tests consume — its §§2–3, quoted word-for-word
in Spec 069's spec §2 under Spec 045's freeze
digest
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`
— but Spec 045 closed INVALID at its own step-0
gate 0.2 (positional reproduction) on
2026-10-21, before its step-1 Asset A build was
reached, so the asset was never built and no
Asset A digest exists on any record. The
owner's readiness decisions of 2026-10-22
(decision 3) commissioned this spec to perform
the build alone, under that exact contract,
keyed natively in the pinned crosswalk's sign
space: the build is corpus-independent, takes
its labels only from the held published sources
of the quoted §2.3, is entered blind to any
positional result, and freezes before any join.
Its frozen product — the classification file
and its SHA-256 digest, in this spec's own
directory (DD-069-6) — is the asserted step-0
input of Spec 070 and Spec 071, neither of
which can freeze before this spec has executed.

## 2. Pin verification (at the freeze)

Every spec §4 pin was recomputed at the freeze
against the merged record (`main` at
`bfc811df`, merged into this branch before the
freeze act; Python `hashlib` over the working
tree, cross-checked with `sha256sum`):

| Input | SHA-256 (recomputed = pin) | State |
|---|---|---|
| Contract (Spec 045 §§2–3) | freeze digest `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a` (from `specs/045-hunt-depicted-kinds/freeze.json`) | Quoted in full in spec §2; the quotation's fidelity is asserted by the freeze tests against Spec 045's frozen text on `main`. |
| Sign crosswalk of record (`data/crosswalks/sign_crosswalk_master.csv`) | `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` | 205 rows carrying 187 distinct `registry_sign_id` values — the full sign universe of gate A3, re-counted at this freeze. |
| D-18 concordance output (Spec 046) | `772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf` (`specs/046-horned-tiger-concordance/concordance-297.json`) | Terminal delivery on record: `signs` an empty array, `closure` block of its IDENTIFICATION FAILED outcome — the frozen §2.6 closure form, an empty feed (DD-069-7). |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | This spec moves no anchor; the file is asserted byte-identical before and after any execution. |
| Held published sources for the build | named at gate A1 in the build record | The CISI volumes (Vol. 1 and Vol. 2, held digitally) and Parpola's published sign identifications, per the quoted §2.3; their editions are named in the build record at execution, and no label may cite a source not so named. |

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`,
computed by `build_freeze.py` in this
directory). Covered sources (nothing else
decides the question):

- `specs/069-hunt-asset-a/freeze.md` (this document)
- `specs/069-hunt-asset-a/spec.md`
- `specs/069-hunt-asset-a/claims.json`
- `specs/069-hunt-asset-a/adjudication.md`
- `specs/069-hunt-asset-a/aee/freeze-aee-note.md`
- `specs/069-hunt-asset-a/build_freeze.py`
- `backend/tests/test_spec069_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-069-10: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The contract** (spec §2 / F069-C02): Spec
  045 §§2–3 verbatim, under Spec 045's freeze
  digest; the quoted text governs over any
  other part of this spec.
- **The asset's form and home** (spec §2.1–2.2
  / F069-C03): exactly the quoted §2.2 fields,
  in one canonical CSV generated by a CSV
  writer and round-trip validated, at
  `specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv`
  with its machine record at
  `specs/069-hunt-asset-a/asset-a/asset-a-freeze.json`
  (DD-069-6). No jurisdiction coding is
  performed at entry (DD-069-8).
- **The sources** (quoted §2.3 / F069-C04): the
  CISI volumes governing, Parpola's published
  identifications governing where CISI is
  silent, a D-18 input never governing on its
  own; program-internal classifications,
  earlier phase outputs, and any worker's own
  visual judgement are not sources.
- **Blind entry and order** (quoted §2.4 /
  F069-C05): entry blind to positional results,
  in the quoted order, attested in the build
  record with the entry log preserved. No
  second-enterer spot check is added
  (DD-069-9, carrying DD-045-16).
- **The dispute rule** (quoted §2.5 /
  F069-C06): disagreeing governing sources
  produce `contested`, both verbatim labels
  recorded, no tie broken; disputes coded
  before the freeze point of the asset and
  before any join.
- **The D-18 disposition** (quoted §2.6 /
  F069-C07): the terminal empty feed on record
  (DD-069-7); the build proceeds without the
  feed, records its absence, and never
  reconstructs it.
- **Coverage** (quoted §2.1 + gate A3 /
  F069-C08): the full pinned-crosswalk sign
  universe — 187 distinct sign keys at this
  freeze's census — each carrying a row: a
  kind, `contested`, or `unidentified` with its
  searched sources recorded.
- **The gates** (spec §3 / F069-C09): A1–A6
  exactly as quoted, in order, before any
  join; ASSET FAILED for A1, A3, A4, A5, A6;
  gate A2 the quoted sequencing stop.
- **The freeze point and the digest** (quoted
  §2.7 / F069-C10): `asset-a-freeze.json`
  records the canonical CSV's SHA-256, the row
  count and per-kind counts, the pins of every
  input, the build-order attestation, and the
  freeze date; Specs 070 and 071 pin that
  digest, not the idea.
- **Corpus independence** (spec §1.2, §4 /
  F069-C11): no corpus of any kind is an input;
  no positional quantity is computed; no
  corpus gate exists in this spec.
- **The limits** (spec §6 / F069-C01, C12): no
  output establishes a gloss or a meaning;
  depiction is the published identification
  layer; Spec 037's 49% caution is restated
  wherever the asset is stated; Spec 045's
  closure stands untouched.

## 5. What the freeze does not do

- **It does not build the asset.** No sign has
  been classified by this freeze, no entry has
  been made, and no Asset A digest exists until
  the Phase 432 execution produces one through
  gates A1–A6.
- **It adjudicates no Hunt claim.** The three
  claims the asset serves stand exactly as
  recorded; this freeze is a build contract,
  not a verdict on any of them.
- **It re-opens nothing.** Spec 045's INVALID
  closure, Spec 046's IDENTIFICATION FAILED
  closure, and their frozen records stand
  exactly as recorded.
- **Execution is the chain act's next steps,**
  not this freeze's own act: the freeze merges,
  the OSF registration is filed under
  DD-069-10, and Phase 432 then runs under the
  same owner act that ordered this chain. The
  registration's approval act remains the
  owner's and is not performed by this freeze.

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec069_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string, `0.9-draft` →
`0.9-MUTATED`) and the suite was run — the
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

Under DD-069-10, this freeze files the spec's
own OSF contract registration carrying the
frozen contract — freeze digest, execution
Phase 432, the falsifier of spec §1.1 (the
build gates A1–A6), the quoted contract and
its source hierarchy, the blind-entry and
dispute rules, the D-18 empty-feed disposition,
the coverage scope of gate A3, the asset's
home in this spec's directory, the
no-jurisdiction-coding ruling, the
spot-check ruling carrying DD-045-16, the
outcome classes of spec §5 with their
pre-written wordings, and the epistemic limits
of spec §6. The filing record is
`osf-spec-registration.md`, completed by
append after filing. The registration stands
**pending approval** after filing; its approval
act is the owner's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution (Phase 432)
proceeds under the chain order of the owner
act that commissioned this chain — freeze,
merge, registration, execution — and its
outcome is recorded in this directory by
append, whatever it is.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
