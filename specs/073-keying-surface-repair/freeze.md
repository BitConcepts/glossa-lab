# Spec 073 — Freeze Record (Repairing the Keying Surface: Registry Wells Coverage and a Second Depicted-Kind Classification, from Published Sources Only)

> ## FROZEN — 2026-10-23
>
> This contract was frozen on 2026-10-23 under
> the owner's order of 2026-10-23: freeze Spec
> 073 with the draft's stated defaults and
> execute it. The AEE lifecycle hooks ran over
> the register first (recovered from the draft
> register 0.5-draft to 0.9-draft in four
> recovery rounds finished before the digest;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035
> ordering). The freeze performed the
> freeze-stage exhibits in order — every pin of
> spec §2 re-asserted against the merged
> records (OPEN-073-9; §3 below), and the ruled
> source list exhibited in hand, with two
> sources struck for non-exhibition
> (OPEN-073-1; §4 below). The freeze also files
> this spec's own OSF contract registration
> (OPEN-073-7; `osf-spec-registration.md`,
> completed by append after filing). Execution
> runs as **Phase-436** under this frozen
> contract, under the execution order given in
> the same owner tasking that commissioned
> this freeze. At the freeze itself no registry
> row has been added, no depiction has been
> entered, and no coverage figure beyond the
> merged records' own baselines has been
> computed.

## 1. Basis

Spec 073 is the repair study the merged
outcome records of Spec 070 (Phase 433, closed
POPULATION NOT KEYED at its gate 0.4) and Spec
071 (Phase 434, closed INVALID at its gate
0.3) name as their successor's first task. The
draft was opened as draft PR #352 (branch
`spec-073-keying-surface-repair-draft`, head
`4d1b3c55`, off main `d20bc1bc`; main verified
unchanged at the freeze act) under the
program's standing drafting authorization.
Its adjudication inputs are recorded in
`adjudication.md`: the two outcome records
read in full, Spec 069's executed Asset A
record, Spec 045's frozen §§2–3, and the
pinned registry, crosswalk and intake record,
recomputed first-hand at drafting.

The owner's freeze order of 2026-10-23 rules
every open item per the draft's stated
defaults. §2 records each ruling by number.

## 2. The owner's rulings — OPEN-073-1 … OPEN-073-9, and DD-073-1 … DD-073-7

- **OPEN-073-1 — Governing source list and
  hierarchy: CONFIRMED as drafted.** For new
  material the governing order is: **CISI**
  (the *Corpus of Indus Seals and
  Inscriptions* sign list, Shah & Parpola
  eds.) first; **Fuls 2023, *A Catalog of
  Indus Signs*** second; **Parpola 1994**
  third, as consulted in held form (the CISI
  volumes' own list, and Parpola 2010's
  published identifications in the same
  numbering). **Fuls 2023, *Corpus of Indus
  Inscriptions*** is corroborating.
  **Mahadevan 1977 and Wells 1998 are struck
  from this study's ruled list at this
  freeze**, for non-exhibition (§4): neither
  full text is in hand on the executing
  machine — of Mahadevan 1977 only the
  introduction OCR is held in the program's
  sources, and Wells 1998's text could not be
  exhibited (its publisher record was
  resolved at record level, DOI
  10.11575/PRISM/23641, but the full-text
  fetch was refused). Nothing in this study
  is entered, corroborated, or contested
  from either; their standing in Spec 045's
  hierarchy as a program matter is untouched,
  and no source is substituted for them.
  **Yajnadevam, the Fuls volumes' OCR texts,
  and the ICIT documentation are locators
  only, never evidence** (DD-073-3,
  confirmed).
- **OPEN-073-2 — Registry v2's form:
  CONFIRMED as drafted.** A new versioned
  file, `data/crosswalks/
  canonical_sign_registry_v2.csv`, in v1's
  field order with no new columns. The
  appended numbering value is `icit_wells`;
  an `icit_wells` row's `sign_id` is `W`
  followed by the zero-padded ICIT code
  (W136, W298, W401, W617, W824, …). The
  supplement-file alternative was not taken.
- **OPEN-073-3 — The attested frame:
  CONFIRMED as drafted.** The frame is the
  distinct ICIT codes attested in the Shakti
  corpus's **documented + corroborated**
  rows (P-F1 S4). Uncorroborated rows attest
  nothing and enter no measurement.
- **OPEN-073-4 — The `row_origin` field:
  CONFIRMED as drafted.** Every Asset A v2
  row carries `row_origin`: `carried_v1` for
  the 187 carried rows, `new_entry` for rows
  entered under this spec.
- **OPEN-073-5 — Entry checking: CONFIRMED
  as drafted.** The two-pass rule
  reconciliation as executed for v1: an
  enterer pass coding from the verbatim
  labels under Spec 045's fixed reading
  rules, then an independent deterministic
  rule pass over the entered labels;
  disagreements adjudicated by re-reading the
  verbatim label, on the record. No
  second-enterer spot check is added.
- **OPEN-073-6 — Concordance inputs:
  DIRECT ENTRY ruled.** Identifications enter
  by direct entry from the ruled sources
  under §5.3's hierarchy. No D-18-style
  concordance input is created for this
  study; new Asset A rows record
  `d18_input` = none.
- **OPEN-073-7 — OSF registration: FILED at
  the freeze**, in the program's contract
  form, carrying this freeze's digest (§9).
- **OPEN-073-8 — Execution phase: Phase-436
  allocated.** Phases 430–434 are the merged
  Shakti-chain executions and Phase-435 is
  Spec 041's frozen phase; 436 is the next
  free number in the merged record.
- **OPEN-073-9 — Pins re-asserted: PASS.**
  Every pin of spec §2 was recomputed
  first-hand at the freeze act and each value
  equals its pin (§3). No pin failed; nothing
  was re-based.

**Draft decisions DD-073-1 … DD-073-7 are
confirmed as drafted** (adjudication.md §5):
two products in gated order (DD-073-1); new
files, never edits (DD-073-2); Yajnadevam a
locator, never evidence (DD-073-3); coverage
measured, never targeted (DD-073-4); the
celestial class measured, never filled
(DD-073-5); new rows mirror Spec 045 §§2.2–2.5
plus `row_origin` (DD-073-6); unresolved
attested signs live in the schedule, not the
asset (DD-073-7).

## 3. Step 0 at the freeze — frozen-input integrity and the §2 pins (OPEN-073-9)

Recomputed first-hand at the freeze act, from
the PR #352 branch tree (whose pinned files
are byte-identical to main's at `d20bc1bc`)
and from the held restricted-local files.
Every recomputed value equals its pin:

| Input | Pin (spec §2) | Recomputed at the freeze |
|---|---|---|
| Registry v1, `data/crosswalks/canonical_sign_registry.csv` | `8a0b2a82…` | `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` — 803 rows (396 `parpola_1982`, 407 `yajnadevam_glyphid`); 498 distinct Wells ids in the `parpola_1982` map; W136/W298/W401/W617/W824 in no row |
| Crosswalk, `data/crosswalks/sign_crosswalk_master.csv` | `4ace1a61…` | `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` — 205 rows, 187 distinct sign ids |
| Asset A v1 canonical CSV (Spec 069) | `95231935…` | `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b` — 187 rows; census animal 20, sky_cycle 0, object_goods 14, human 25, other 127, contested 0, unidentified 1 |
| Spec 045 freeze digest | `5d8254dd…` | `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a` |
| Spec 070 freeze digest | `763108f8…` | `763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e` |
| Spec 071 freeze digest | `c06a7a86…` | `c06a7a86804d8da2c9896638446f5712be9eccb8716a7b02303a5944f4bc0478` |
| Shakti corpus (restricted-local) | `345241b1…` | `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68` |
| Shakti row grades (restricted-local) | `02394241…` | `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739` |
| Fuls, *Corpus of Indus Inscriptions* (PROVENANCE entry 27) | PDF `185fd057…`; OCR txt `d8aab176…` | OCR txt recomputed `d8aab17680af50012a8d78487c9e047dfc1f9d93d7cbcd4ed3c5c5a84acb5cc5`; PDF of record stays pinned in place on the owner's desktop |
| Fuls, *A Catalog of Indus Signs* (PROVENANCE entry 27) | PDF `31729a4f…`; OCR txt `3e9c6758…` | OCR txt recomputed `3e9c6758b112364f33c057c7c8464324511fa6008662aaeae26e10f1962df27c`; PDF of record stays pinned in place on the owner's desktop |

The restricted-local pins are asserted here as
definition constants, in the Spec 038 form:
those files are never committed, so no
live-file hash is asserted on them in the test
suite; execution gate 0.1 recomputes them.

## 4. Sources in hand at the freeze — the ruled list exhibited (gate 0.3, performed for the ruled list)

Each source the freeze rules as governing or
corroborating was exhibited in hand at the
freeze act, with its pin:

- **CISI, volumes 1–2** (Shah & Parpola
  eds.) — held as the Internet Archive scans:
  Vol. 1, SHA-256
  `8278d815450cb23cf04ffb1ffb43f62a6206bfc75f9a61f505b92eb41c627908`
  (30,027,528 bytes); Vol. 2, SHA-256
  `727132579a485ee626e48a64c663148a85fbc0811fb523818fd615231f8a327d`
  (35,870,617 bytes). The CISI sign list is
  entered through the held mayig digitization
  of the corpus (commit
  `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`),
  whose per-sign feature files carry the
  list's verbatim descriptions and its Wells
  and Mahadevan grapheme statements — the
  entered form Spec 069's build already
  rests on. **CISI 3.1** is held
  restricted-local under PROVENANCE entry 22
  (scan SHA-256
  `772e929782119ff9293088e060562c18f14234e7a24efdf3deb68669fea67afa`);
  derived statistics from it are publishable,
  its scans are never redistributed.
- **Fuls 2023, *A Catalog of Indus Signs***
  (governing, second) — held under PROVENANCE
  entry 27: the owner's print volume, PDF of
  record on TRISTEN-DESKTOP, SHA-256
  `31729a4f7b33bd1ec08633bb677f963b5de8f50d96afdfc25cff5ddc96f9a32a`
  (571 pp.), with the April-2026 OCR text
  held locally as a locator (recomputed
  `3e9c6758…`, §3). Entry is from the volume
  itself; the OCR text locates, it never
  evidences.
- **Parpola 1994** (governing, third) — as
  consulted in held form: the CISI volumes'
  own sign list (above) and Parpola 2010's
  published identifications in the same
  numbering, held as the 2010 Helsinki
  lecture PDF, SHA-256
  `c58137e54cdde3f2acdcfaf05293dfc5f5ba33def3e0b12585c451f76bd4ba84`
  (4,979,212 bytes) — the held form Spec 069's
  record states.
- **Fuls 2023, *Corpus of Indus
  Inscriptions*** (corroborating) — held
  under PROVENANCE entry 27: PDF of record
  SHA-256
  `185fd0575d881568583a7002d705b2ded1313a525fafe093108f72e0fe897727`
  (583 pp.), OCR locator text recomputed
  `d8aab176…` (§3).

**Struck at the freeze (OPEN-073-1):**

- **Wells 1998**, *An Introduction to Indus
  Writing* (MA thesis, University of
  Calgary; DOI 10.11575/PRISM/23641). The
  draft ranked it corroborating-only and
  required gate 0.3 to exhibit its text or
  the freeze to strike it. Its text could
  not be exhibited: no copy is held, and the
  repository fetch of the full text was
  refused (HTTP 403). It is struck from this
  study's ruled list. Wells *identities*
  still enter Registry v2 — through the
  published lists that state them (the CISI
  list's Wells grapheme statements and the
  Catalog), never through the thesis itself.
- **Mahadevan 1977**, *The Indus Script:
  Texts, Concordance and Tables*. The draft's
  §2 row says the work is held as scan + OCR
  in the program's sources; first-hand
  inspection at the freeze finds only the
  introduction's OCR text in the sources
  tree — the sign-list tables are not in
  hand on the executing machine. As a
  corroborating-only source that cannot be
  consulted, it is struck from this study's
  ruled list on the same terms: nothing is
  entered, corroborated, or contested from
  it here. This narrows nothing at run time;
  the narrowing is the freeze's own act,
  recorded here, exactly as spec §5.3's
  no-silent-narrowing rule requires.

Execution gate 0.3 re-asserts this exhibit
against the same pins before any entry; a
source then not in hand closes the run as
SOURCE NOT IN HAND with the source named.

## 5. Machine record

- Register: `claims.json`, 16 claims
  (F073-C01…C16), recovered 0.5-draft →
  0.9-draft in four rounds (§5 of
  `aee/freeze-aee-note.md` states them in
  full; the register's own note carries the
  record round by round).
- AEE hooks at the freeze: after_specify
  `20261023T131036Z`, after_plan
  `20261023T131041Z`, after_tasks
  `20261023T131046Z` — at every hook exactly
  16 failure modes, all FR-2.3 draft-cap
  records, zero correctness failure modes,
  minimum propagated confidence 0.795 (gate
  pass on the DD-038-10 reading).
- Freeze digest: `freeze.json` in this
  directory, computed exactly once over
  freeze.md, spec.md, claims.json,
  adjudication.md, aee/freeze-aee-note.md,
  build_freeze.py and
  backend/tests/test_spec073_freeze.py.
- Environment: Python 3.12.3; aee 1.5.3
  (adopted environment, pin `>=1.5.0,<1.6`)
  in the `glossa-aee153` venv; spec-kit
  specify 1.0.10.
- Execution phase allocated: **Phase-436**
  (OPEN-073-8).

## 6. What the freeze fixes

The governing source list and hierarchy with
its two strikes (§§2, 4); Registry v2's form
and the `icit_wells` value (§2); the attested
frame (§2); the `row_origin` field (§2);
two-pass entry checking with no added spot
check (§2); direct entry with `d18_input` =
none (§2); the step-0 gates, build gates and
outcome classes of spec §§3, 5.4 and 7 exactly
as drafted; the baselines of spec §3 gate 0.2
(Baseline A: 31 opening-strong signs, 26 keyed
/ 5 unkeyable, counts 136:6, 298:7, 401:5,
617:56, 824:16; Baseline B: 557 signs, 285 /
134 / 138; Baseline C: 498 distinct Wells ids;
Baseline D: Asset A v1 census with sky_cycle
0); the measurements M1–M5 of spec §6, with
M5 in the headline block; and the §10 record
form. The claims served remain
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
(IN QUESTION) and
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
(UNTESTED), untouched.

## 7. What the freeze does not do

The freeze itself adds no registry row,
enters no depiction, and computes no coverage
figure. It does not re-run, amend, or appeal
Spec 070's or Spec 071's closures, and it
changes neither Hunt claim's standing. It
does not amend Spec 045's contract or Spec
069's asset. It does not promise that the
celestial class reaches Spec 071's floor of
30, or one member: if the ruled sources
identify no celestial depictions, the
execution's recorded output is that the class
is empty or thin and the sky-signs question
remains untestable in this form. And it does
not decide whether either Hunt question
should be re-asked: a re-freeze consuming
the v2 products is a separate owner decision.

## 8. Able-to-fail proof (the freeze tests)

`backend/tests/test_spec073_freeze.py` pins
this freeze: the machine record replays
(framework026 `verify_freeze` over every
covered source), the definition carries the
frozen contract exactly (the rulings of §2,
the strikes of §4, Phase-436, the outcome
classes), the governed register is the frozen
register (16 claims, integrity-clean,
recovered at 0.9-draft), the three freeze-hook
artifacts record the pass on the DD-038-10
reading, and the cited records still carry
the facts the design rests on (the §3 pins;
the registry's 498-id map and the five codes'
absence; the Phase 433/434 machine records'
baselines). The tests were proven able to
fail at the freeze act, before the freeze
commit: with the full suite green over the
final texts, the working tree was mutated in
exactly one place (one character of a
digest-covered source), the freeze tests were
run and went red on the replay assertion, the
mutation was reverted byte-identically, and
the tests were run again green. The mutation
touched no committed file's final bytes.

## 9. OSF registration and the execution gate

Under OPEN-073-7 the freeze files this spec's
OSF contract registration in the program's
contract form, carrying this freeze's digest;
the filing is recorded in
`osf-spec-registration.md` (completed by
append after filing). The registration's
approval act is the owner's click and is not
performed by the freeze or the execution; the
registration's mail stays in the inbox while
it is pending, per the standing OSF mail
rule. Execution (Phase-436) runs after this
freeze has merged and the registration is
filed, under the execution order given in
the same owner tasking that commissioned
this freeze.

---

*AI disclosure: executed by an AI agent (Muse,
via Muse) at the direction of Tristen Pierson,
per constitution §VI.*
