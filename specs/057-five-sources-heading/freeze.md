# Spec 057 — Freeze Record (The Heading Carried by Five Sources: Re-extract the Five Passages; Design D-19)

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
> contract registration (DD-057-13;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-419**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> no passage has been read for content, nothing
> has been recovered, and no source has been
> given an outcome.

## 1. Basis

The contract implements design D-19 (campaign
member 14): the re-extraction act for
`ancient_writing_and_modern_technologies_51831ac9_statisti_0004`
— "Statistical finding: positional analysis" —
an UNTESTED fragment, in full a heading, stopped
at Phase-104 under RULE-NOCOND, carrying no
stated proposition and no falsification
condition. Phase I merged five extractions of
that heading, from five source documents, into
this one record (fingerprint `a4874349…`); the
act goes back to each of the five held sources,
finds the passage under that heading under the
heading-form rule, and accounts for every one
of the five with exactly one pre-registered
outcome — CLAIM RECOVERED, PASSAGE EMPTY, or
SOURCE UNLOCATED — deriving the headline class
and the heading record's disposition
mechanically from the counts.

The freeze decided the open points
(`adjudication.md` §7): **DD-057-10** (OPEN-1:
the HEADING NOT PRESENT sub-state of SOURCE
UNLOCATED confirmed — DD-057-3 stands; the §7
partition stands as drafted), **DD-057-11**
(OPEN-2: the S-3 delimitation of §5.2 confirmed
— the passage is the paper's findings-bearing
body, cited by line range, not reprinted, and
no narrower delimitation is substituted),
**DD-057-12** (OPEN-3: recovered-claim intake
inside the execution confirmed — DD-057-6
stands), **DD-057-13** (OPEN-4: the spec files
its own OSF contract registration at the
freeze, under campaign E-1), **DD-057-14**
(DD-057-5 confirmed: a checkable proposition
without numbers is CLAIM RECOVERED, with
"numbers: none stated" on its record),
**DD-057-15** (DD-057-7 confirmed: retirement
is not available while r = 0 and u ≥ 1),
**DD-057-16** (the execution phase is
Phase-419), and **DD-057-17** (the DD-038-10
AEE gate reading adopted). DD-057-1 to
DD-057-9 are **confirmed** as drafted,
including the two-layer pin (DD-057-2), the
heading-form rule (DD-057-4), and the
accounting-is-success reading (spec §1.2).

## 2. Pin verification (two routes, at the freeze)

Every §2 pin was re-derived **in the
foreground** by two independent routes — the
contents-API raw route and the git-blob route —
both at the merged record (`main` at
`770155dea66c5d5dde194728560aacf83c7514d0`, the
record after Spec 050's freeze merged). The
two routes agree byte-for-byte on every file,
every recomputed hash equals its draft pin, and
a third local route — the checked-out blobs of
a fresh clone at the same main — agrees on
every file:

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| S-1 cleaned text (`ancient_writing_and_modern_technologies_51831ac9.txt`) | `1275b795903260221f5226bada352de27471c010e2ad8ace556c548c20da1fc4` | 48,904 |
| S-1 extracted claims | `e98190894202a2a1c0e314229dcb585c62a0f5c12c059bcabd63b055c42959e8` | 22,894 |
| S-1 literature registry | `92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c` | 1,261 |
| S-2 cleaned text (`fuls2023_catalog_of_indussigns_searchins_1dbdecdb.txt`) | `dae154327592d19366c9feb56362477fa842114cec944416b9b05dc3f0efd4cb` | 48,044 |
| S-2 extracted claims | `857abacac4317fa0f7bdf7d4052661a4109b6f5ee507843b93cac8c5ad46c5a4` | 1,931 |
| S-2 literature registry | `bb23e5e9f90c30ebebb2d45e2967fb668a54432a56692a8772753fd228316f47` | 1,250 |
| S-3 cleaned text (`positional_analysis_of_indus_signs_a2bedc93.txt`) | `9ed24098c006fcde5bb0ca7be6a6fa188011c3bc7bb8db46796abc77961a0708` | 38,641 |
| S-3 extracted claims | `713576363f9678281703866e6b749a9486d754906173bb48b7b44367531dc6f8` | 1,889 |
| S-3 literature registry | `9b95174bad62c9a4879ae3db28a03ee52bc665df4e1d9897e65f84f353baa53c` | 1,210 |
| S-4 cleaned text (`the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`) | `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` | 268,195 |
| S-4 extracted claims | `bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a` | 9,653 |
| S-4 literature registry | `b2638a705549348d2d857989e74f7a8ab09bd4e3ea60d6e3dfab4e49fd9eba68` | 1,259 |
| S-5 cleaned text (`without_kings_or_conquests_the_indus_scr_ce9d98cc.txt`) | `dd58497528db89fe75111d2431b9611aebd4a5a9715a4ecceb012d9d1538029e` | 80,249 |
| S-5 extracted claims | `c1a433d539a0ed899fe7ab11af2be0c608cb85d9f0fc99b2ccfefdb6e866262a` | 32,672 |
| S-5 literature registry | `38122256305b8451e49e4ef4d56df7399363bdc3c57052b10f9165ab593261a7` | 1,313 |
| Phase-104 evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) | `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` | 17,475 |
| Lane-2 adopted drafts (`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`) | `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` | 127,338 |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |

The five extracted-claims files' hashes are
carried as freeze definition constants in the
Spec 038 form: the extracted-claims store is
regenerated by the backend suite, so the freeze
tests assert the constants plus each entry's
facts on the live files, never live-file hashes
on that store. Every other input's hash is
asserted on the live file.

The facts the design rests on were re-read from
the pinned bytes in the same pass: the canonical
record reads in full "Statistical finding:
positional analysis", status *untested*, stage
*created*, quote fragment the lowercase
"positional analysis", fingerprint `a4874349…`,
with exactly the four evidence instances of
§2.1, each carrying the same fingerprint and a
`merged_into` pointer at the canonical record in
its own claims file; the Phase-104 entry reads
*stays_untested* under RULE-NOCOND ("no
falsification condition and no stated
proposition"); the lane-2 entry for the claim
stands at stage *created*, lane-1 status
*untested*, its not-understood text prescribing
exactly this re-extraction; each registry file
carries its source's original filename, size,
and `checksum_sha256` as §2.1 records, with
license_status "unclear" for all five; and the
heading postures stand as the draft recorded
(string occurrences only — no passage was read
for content): S-1 two lines, no heading form;
S-2 three lines, a chapter heading; S-3
eighteen lines, the paper's own title as running
head; S-4 ten lines, an appendix heading at
line 3456; S-5 one line, no heading form.
`backend/tests/test_spec057_freeze.py` pins all
of these facts so later drift fails loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/057-five-sources-heading/freeze.md` (this
  document)
- `specs/057-five-sources-heading/spec.md`
- `specs/057-five-sources-heading/claims.json`
- `specs/057-five-sources-heading/adjudication.md`
- `specs/057-five-sources-heading/aee/freeze-aee-note.md`
- `specs/057-five-sources-heading/build_freeze.py`
- `backend/tests/test_spec057_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-057-13: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The scope fence** (spec §1 / F057-C01, C15):
  the five passages of the five sources, and the
  accounting of them. No outcome establishes any
  positional finding, transfers credit from other
  records, or licenses publication use of the
  verbatim passage texts.
- **The five sources** (spec §2.1 / F057-C03,
  C04): exactly the canonical record plus its
  four evidence instances, each pinned three
  ways (cleaned text, extracted claims, registry
  file, each by SHA-256, plus the source
  document's recorded checksum and size). No
  source may be added, dropped, or substituted.
- **The step-0 gates** (spec §3 / F057-C05):
  input integrity and source-set integrity, in
  order, before any passage is read — each
  closing the run in its named class.
- **The stated search** (spec §4 / F057-C06):
  the four steps a SOURCE UNLOCATED outcome
  must survive, with its sub-states (DOCUMENT
  UNLOCATED; HEADING NOT PRESENT IN HELD TEXT,
  DD-057-10), its full search log, and its named
  unblocking act.
- **Location and extraction** (spec §5 /
  F057-C07, C08): the heading-form rule
  (DD-057-4), the delimitation including the
  S-3 title-as-heading case (DD-057-11), and the
  verbatim passage artifact with its locator
  and SHA-256 on the row.
- **The accounting** (spec §6 / F057-C09, C10):
  exactly one outcome per source over the
  five-row table; CLAIM RECOVERED under the
  checkability standard with "numbers: none
  stated" where none are stated (DD-057-14);
  PASSAGE EMPTY with the passage quoted.
- **Intake** (spec §6 / F057-C11): recovered
  claims enter through the programme's intake
  inside the execution (DD-057-12), at the
  created stage, unchecked; no check is
  designed or run under this spec.
- **The headline and the disposition** (spec §7
  / F057-C12, C13): the six classes over
  (r, e, u), exhaustive over all 21 triples,
  under the pre-written §7.1 wordings; the
  disposition by appended note only —
  superseded, retired, or no disposition while
  a source is unlocated (DD-057-15).
- **The hypothesis** (F057-C14): at least one
  passage states a checkable finding — registered
  so the accounting can defeat it honestly.

## 5. What the freeze does not do

- **It does not itself extract or account for
  anything.** No passage has been located under
  the heading rule, read for content, delimited,
  or extracted; no source carries an outcome;
  no claim has been recovered. Extraction and
  accounting are execution outcomes under
  Phase-419, not freeze acts.
- **It checks nothing recovered.** There is
  nothing recovered to check, and no check for
  a recovered claim is designed or run under
  this spec in any case (F057-C11).
- **It decides nothing about sign positions.**
  Not whether signs occupy preferred positions,
  not what any passage's finding is worth, and
  nothing about any positional result recorded
  elsewhere in the programme.
- **It changes no verdict.** The heading record
  stands UNTESTED on its Phase-104 record, which
  stands unedited, as do the canonical record,
  its evidence instances, and the Phase I merge.
  The anchors file is asserted byte-identical
  before and after any execution; this spec
  moves no anchor.
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  (Phase-419) awaits the freeze merge, the
  OSF registration's approval act, and a
  separate execution order, in campaign Wave 3
  group 2.

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec057_freeze.py` were
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

Under DD-057-13 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-419, the accounting falsifier,
the five sources with their pins and occurrence
postures, the step-0 gates, the stated search
with its sub-states, the heading-form rule and
the S-3 delimitation, the per-source accounting
standards, the mechanical headline partition
and its pre-written wordings, the disposition
rule with the no-retirement-while-unlocated
carve-out, the recovered claims' lifecycle
position (created stage, unchecked, intake
inside the execution), the freeze rulings, and
the limits stated as limits on results:
recovery is not verification, no credit
transfers, and the verbatim passage artifacts
are internal records under license_status
"unclear". The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is
the parent's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution (Phase-419)
does not begin while the registration stands
pending: it awaits that approval act and a
separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
