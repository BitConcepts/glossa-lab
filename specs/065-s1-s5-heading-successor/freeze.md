# Spec 065 — Freeze Record (The Two Unlocated Rows of Spec 057: Document Text-Layer Search for the Heading; Successor Recovery Act for S-1 and S-5)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the owner's approval of the same date
> (amendment package Item 6: build Spec 065,
> the successor recovery act for Spec 057's
> S-1 and S-5 rows, through freeze and OSF
> filing; `adjudication.md` §§1, 7). The AEE
> lifecycle hooks ran over the register first
> (register recovered to 0.6-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035 ordering).
> The freeze also files this spec's own OSF
> contract registration (DD-065-15;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-427**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> no text layer has been searched, no heading has
> been judged, and neither row carries an outcome.

## 1. Basis

The contract is the successor recovery act
named on two rows of Spec 057's closed outcome
record (Phase-419, executed 2026-10-21; headline
class C — PARTIAL RECOVERY WITH UNLOCATED
SOURCES, *r* = 2, *e* = 1, *u* = 2; freeze digest
`237b923a2c19b216e0476f70d17a956db0ca68d1ba8af6902109099a82c820d9`).
S-1 (Fuls 2020, *Studies on Indus Script*,
pp. 57–90) and S-5 (Hunt 2025, Zenodo preprint,
DOI 10.5281/zenodo.17066226) each closed SOURCE
UNLOCATED, sub-state HEADING NOT PRESENT IN HELD
TEXT, because Spec 057's §4 step 4 — search the
source document's own text layer under §5's
heading rule — could not run: no copy of either
document exists in the repository. Each row names
the same unblocking act: re-acquisition of the
source, specifically a copy of the edition the
original extraction ran on, so the document text
layer can be searched under §5.

The Item 6 provenance work of 2026-10-21
discharged that act asymmetrically, and this
freeze freezes exactly that posture. **S-5 is
acquired and pinned** (657,863 bytes, SHA-256
`77f10f32…`, MD5 `36616e20…` matching the Zenodo
record; licence CC-BY-4.0 as stated on the record
at acquisition, superseding the registry's
"unclear" for this copy; edition relationship
established — the same September 2025 draft the
original extraction ran on, content-equal modulo
export/cleaning). **S-1 is not acquired**: its
only lawful digital route is gated by
Academia.edu's sign-in wall, an owner account
act, recorded in `BLOCKED.md` and the PROVENANCE
blocked section. The successor therefore searches
the acquired S-5 file's text layer under the
carried §5 rule, and holds S-1 under a frozen
two-arm contract (searched if handed over and
intake-pinned before the run; otherwise resolved
STILL UNLOCATED — ACQUISITION BLOCKED). The
heading record retires only when both sources
resolve (Spec 057's rule, carried verbatim);
while S-1 is blocked it stands
superseded-not-retired exactly as 057 left it.
Spec 057's records are never patched.

The freeze decided the draft's open points
(`adjudication.md` §7): **DD-065-10** (the freeze
basis — the owner's amendment package Item 6
approval; DD-065-1…DD-065-9 stand as drafted);
**DD-065-11** (OPEN-1: the S-1 frozen contract
stands as drafted — the `intake-S1.json` form,
the later-intake rule, the no-contact fence);
**DD-065-12** (OPEN-2: the §7 partition is total
and the disposition forms stand; retirement only
when both resolve); **DD-065-13** (OPEN-3:
Phase-427 allocated — verified genuinely free);
**DD-065-14** (the DD-038-10 AEE gate reading
adopted); and **DD-065-15** (OPEN-4: the spec
files its own OSF contract registration at the
freeze, under campaign E-1; the freeze and filing
acts are taken, execution is not authorised).

## 2. Pin verification (two routes, at the freeze)

Every §2 repository pin was re-derived **in the
foreground** by two independent routes — the
contents-API raw route and the git-blob route —
both at the merged record (`main` at
`7e483e74508ab0f6183a58b951e1be13e0625267`), with
the fresh working tree agreeing as a third read.
The routes agree byte-for-byte on every file, and
every recomputed hash equals its pin.

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| S-1 cleaned text (`ancient_writing_and_modern_technologies_51831ac9.txt`) | `1275b795903260221f5226bada352de27471c010e2ad8ace556c548c20da1fc4` | 48,904 |
| S-1 literature registry | `92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c` | 1,261 |
| S-5 cleaned text (`without_kings_or_conquests_the_indus_scr_ce9d98cc.txt`) | `dd58497528db89fe75111d2431b9611aebd4a5a9715a4ecceb012d9d1538029e` | 80,249 |
| S-5 literature registry | `38122256305b8451e49e4ef4d56df7399363bdc3c57052b10f9165ab593261a7` | 1,313 |
| Spec 057 freeze record (`specs/057-five-sources-heading/freeze.json`) | `3cc68c372790d6bd62d9ab1bb43b15ec2f43502dd614150d660d33b4c452d8af` | 23,935 |
| Spec 057 outcome record (`specs/057-five-sources-heading/outcome.md`) | `d3ae1325bdba52295bd44990db024957c1d3aceeb462ddbf60af73b512834a58` | 31,923 |
| Spec 057 spec (`specs/057-five-sources-heading/spec.md`) | `0798d51aac680c981fe38bf45761358231957391b67cd24228b5cba675ec9e8d` | 27,748 |
| Spec 057 adjudication (`specs/057-five-sources-heading/adjudication.md`) | `041880706d9ebae2c1a30a5dae8cd2066d915317fb551d46af469dd2fd4ec017` | 23,603 |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |

The two extracted-claims pins (S-1 `e9819089…`,
S-5 `c1a433d5…`) are carried as freeze definition
constants in the Spec 057 form: the
extracted-claims store is regenerated by the
backend suite and both files now carry Spec 057's
own dated appends, so the freeze tests assert the
constants plus each entry's facts on the live
files, never live-file hashes on that store. The
facts were re-read from the live files in the same
pass: each row's entry stands with the fingerprint
`a4874349e0cc0ba23b711f10c78f60372639c2dc6f352165b48d4a9e44272469`,
status *untested*, and its recorded
`quote_fragment` (S-1 the lowercase "positional
analysis"; S-5 "Positional analysis"); Spec 057's
freeze digest recomputes as recorded,
`237b923a2c19b216e0476f70d17a956db0ca68d1ba8af6902109099a82c820d9`,
and its outcome record reads class C with S-1 at
§4.1 and S-5 at §4.2 in the sub-state this successor
resolves.

The acquired S-5 file — not a repository input —
was re-asserted on the local file in the same pass:
657,863 bytes, SHA-256
`77f10f3279454bede1ba60a04f3c099500667ca62574b07aaabb9fc69bf94665`,
MD5 `36616e20a2c62be106ebf9c3d4093fd6`. Gate 0.2
asserts the same values again at execution, before
any search. `backend/tests/test_spec065_freeze.py`
pins all of these facts so later drift fails loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/065-s1-s5-heading-successor/freeze.md` (this
  document)
- `specs/065-s1-s5-heading-successor/spec.md`
- `specs/065-s1-s5-heading-successor/claims.json`
- `specs/065-s1-s5-heading-successor/adjudication.md`
- `specs/065-s1-s5-heading-successor/aee/freeze-aee-note.md`
- `specs/065-s1-s5-heading-successor/build_freeze.py`
- `backend/tests/test_spec065_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-065-15: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The scope fence** (spec §1 / F065-C01, C15):
  the resolution of Spec 057's two unlocated rows,
  and nothing else. No outcome establishes any
  positional finding, re-accounts a closed row, or
  licenses publication use of a verbatim passage.
- **The two rows** (spec §2.1 / F065-C02, C03):
  exactly S-1 and S-5 as Spec 057 recorded them,
  identified by claim_id and document_id, each
  pinned as §2 states. No source may be added,
  dropped, or substituted.
- **The step-0 gates** (spec §3 / F065-C05): input
  integrity, the acquired-file assertion (gate
  0.2 — the search is never run on substitute
  bytes, and the held cleaned text is never
  substituted for the acquired document), the S-1
  intake determination, and order — each closing
  the run in its named class before any text layer
  is searched.
- **The searches** (spec §4 / F065-C06): for S-5,
  the acquired file's own text layer, every
  occurrence listed and judged; for S-1, the
  frozen two-arm contract (DD-065-11) — searched
  on the search arm exactly as S-5 is, resolved
  STILL UNLOCATED — ACQUISITION BLOCKED on the
  blocked arm, citing the blocker record.
- **The heading rule** (spec §5 / F065-C07, C08):
  Spec 057 §5 carried verbatim in substance —
  heading form, delimitation, and the verbatim
  passage artifact with its locator and SHA-256
  on the row.
- **The accounting** (spec §6 / F065-C09, C10):
  exactly one outcome per source from the frozen
  set — HEADING FOUND (passage recovered or
  recorded empty under 057 §6's standards,
  carried), HEADING ABSENT FROM DOCUMENT
  (document-level finding; converts the sub-state,
  with the searched file's hash as evidence), or
  (S-1 only) STILL UNLOCATED — ACQUISITION BLOCKED.
- **Intake** (spec §6 / F065-C11): a recovered
  claim enters through the program's intake inside
  the execution, at the created stage, unchecked;
  no check is designed or run under this spec.
- **The headline and the disposition** (spec §7 /
  F065-C12, C13): classes A and B over the two
  rows' outcomes, exhaustive over §6's outcome set,
  under the pre-written §7.1 wordings; the
  disposition by appended note only — the heading
  record retires only when both sources resolve
  (DD-065-12); while S-1 is blocked it stands
  superseded-not-retired exactly as 057 left it.
- **The hypothesis** (F065-C14): at least one of
  the two documents carries the heading in heading
  form — registered so the accounting can defeat it
  honestly, and judged only over documents actually
  searched. The Item 6 prior assessments (both
  headings likely absent) carry no standing
  (DD-065-7).

## 5. What the freeze does not do

- **It searches nothing.** No document text layer
  has been extracted or searched as a finding, no
  occurrence has been judged under §5, no passage
  has been read for content, and neither row carries
  an outcome. The searches and the accounting are
  execution outcomes under Phase-427, not freeze
  acts. (The provenance comparison of the Item 6
  work extracted the acquired file's text layer to
  compare content; it ran no §5 judgement and is
  cited as provenance only.)
- **It acquires nothing.** S-5 was acquired under
  the Item 6 package before this spec was drafted;
  S-1's acquisition is the owner's account act, and
  this freeze neither performs it nor sends any
  request toward it.
- **It checks nothing recovered.** There is nothing
  recovered to check, and no check for a recovered
  claim is designed or run under this spec in any
  case (F065-C11).
- **It changes no record of Spec 057's.** Its spec,
  freeze record, outcome record, and the canonical
  heading record with its evidence instances stand
  unedited. The anchors file is asserted
  byte-identical before and after any execution;
  this spec moves no anchor.
- **Execution has not begun and is not authorised
  by the freeze alone.** Execution (Phase-427)
  awaits the freeze merge, the OSF registration's
  approval act, and a separate execution order
  (DD-065-15).

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec065_freeze.py` were proven
able to fail at the freeze act, before the digest
was relied on: with the assembled freeze in place,
the register file in the working tree was mutated
in exactly one place (its `register_version`
string, `0.6-draft` → `0.6-MUTATED`) and the suite
was run — the freeze-replay test and the
register-integrity test went red, as they must,
because a covered source no longer matched its
frozen hash and the register no longer carried its
frozen version. The file was then restored
byte-identically (its SHA-256 re-verified against
the value recorded in `freeze.json`'s sources) and
the full freeze suite was run again green. The
mutation touched no committed byte; the frozen
record replays exactly over the restored tree.

## 7. OSF registration and the execution gate

Under DD-065-15 (campaign E-1), this freeze files
the spec's own OSF contract registration carrying
the frozen contract — freeze digest, execution
Phase-427, the accounting falsifier, the two rows
with their pins and Spec 057 postures, the
predecessor digest (Spec 057's freeze digest, with
its record unpatched), the step-0 gates including
the acquired-file assertion, the S-5 document-layer
search and the frozen S-1 two-arm contract with its
blocker cited, the carried heading rule and
recovered/empty standards, the frozen outcome set
with the document-scoped absence finding, the
mechanical headline partition and its pre-written
wordings, the retirement rule (retires only when
both sources resolve; superseded-not-retired while
S-1 is blocked), the recovered claims' lifecycle
position (created stage, unchecked, intake inside
the execution), the S-5 licence as recorded for the
acquired copy (CC-BY-4.0), the S-1 fence (no
contact, no account, no request), and the limits
stated as limits on results: recovery is not
verification, prior assessments carry no standing,
and acquiring and pinning the S-5 document
establishes nothing about what its text layer holds
under the §5 rule. The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is the
parent's approval click on OSF's admin-notification
email, and no mail is handled by this freeze.
Execution (Phase-427) does not begin while the
registration stands pending: it awaits that approval
act and a separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
