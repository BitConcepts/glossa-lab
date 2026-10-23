# Spec 073 — Repairing the Keying Surface: Registry Wells Coverage and a Second Depicted-Kind Classification, from Published Sources Only

> ## FROZEN — 2026-10-23
>
> Frozen at the freeze act of 2026-10-23 under
> the owner's order of 2026-10-23 (freeze with
> the drafted defaults and execute), as the
> successor design both Hunt outcome records
> name. Spec 070's outcome record (Phase 433)
> states: "A successor that wants this
> question answered must first repair the
> keying surface — a registry that carries
> Wells identities for these signs, or a
> different freeze-fixed route." Spec 071's
> outcome record (Phase 434) states the two
> repairs its question needs: "a depicted-kind
> classification whose universe covers the
> signs the corpus actually uses … and — on
> the evidence of the frozen asset — a
> celestial class that exists." This spec is
> that repair study, and nothing else.
> The freeze record is `freeze.md` /
> `freeze.json` in this directory; the
> AEE lifecycle hooks ran at the freeze gate
> and passed over the recovered register
> (0.9-draft; `aee/freeze-aee-note.md`); the
> freeze-stage exhibits (every §2 pin
> re-asserted, OPEN-073-9; the ruled source
> list exhibited with two sources struck for
> non-exhibition, OPEN-073-1) are recorded in
> `freeze.md` §§3–4. Execution runs as
> **Phase-436** under this frozen contract,
> under the execution order given in the same
> owner tasking that commissioned this
> freeze. At the freeze itself no registry
> row has been added, no sign has been
> classified, and no coverage figure beyond
> the merged records' own baselines has been
> produced.
>
> This spec **re-runs nothing**. Spec 070
> stands closed as POPULATION NOT KEYED at
> its gate 0.4; Spec 071 stands closed as
> INVALID at its gate 0.3. Neither closure
> is amended, repealed, re-run, or appealed
> by anything here. This spec also does not
> touch Spec 069's frozen Asset A or Spec
> 045's frozen contract: every extension it
> builds is a **new version with its own
> digest**, consumed by nobody until a
> future freeze says so.
>
> The execution phase number is
> **unassigned** at this draft. It is
> allocated at the freeze act, from the
> merged record as it then stands.

**Design source:** the merged execution
records of Spec 070 (Phase 433,
`specs/070-hunt-opening-signs-successor/outcome.md`)
and Spec 071 (Phase 434,
`specs/071-hunt-sky-signs-successor/outcome.md`),
read first-hand at this draft; Spec 069's
executed Asset A record
(`specs/069-hunt-asset-a/asset-a/asset-a-freeze.json`
and its entry log); Spec 045's frozen
§§2–3 (the Asset A contract, freeze digest
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`);
and the Shakti intake record
(`docs/decisions/2026-10-22-shakti-corpus-intake-record.md`,
proposal P-F1 as adopted).

**Claims this repair serves:**
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
(the opening/animal claim — standing
**IN QUESTION** exactly as Spec 070's
closure left it) and
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
(the sky-signs claim — standing
**UNTESTED** exactly as Specs 050 and 071
left it). This spec adjudicates neither
claim and appends nothing to either claim's
record. It repairs a join surface; what the
repaired surface would let a future study
ask is that study's business, under its own
freeze.

**AI disclosure:** this draft is produced
by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per
constitution §VI.

---

## 1. The failure, stated from the records

Both Hunt successors died at step 0, on the
**keying surface** — the chain that turns a
Shakti inscription's ICIT code into a row of
the depicted-kind classification. Neither
reached its question. The chain, as Spec
070's freeze fixed it (DD-070-9, adopted
unchanged by Spec 071 as DD-071-10), is:

> A Shakti sign's ICIT code *n* is its Wells
> number. Among the rows of the pinned
> canonical sign registry
> (`data/crosswalks/canonical_sign_registry.csv`)
> with `numbering_system` = `parpola_1982`
> whose `wells_ids` contains the token `W`
> followed by *n* zero-padded to three
> digits, the sign resolves to the Asset A
> row whose `sign_key` is that registry
> row's `sign_id`. Exactly one distinct
> `sign_id` is a resolution; zero or more
> than one is a resolution failure.

Three distinct breaks in that chain are on
the merged record:

- **Break 1 — Wells identities missing from
  the registry (Spec 070).** Shakti's own
  battery enumerated 31 opening-strong
  signs. Five of them — ICIT codes **136,
  298, 401, 617, 824**, with 6, 7, 5, 56 and
  16 occurrences respectively (617 alone
  carries more occurrences than the other
  four combined) — have no row in the
  pinned registry **in any numbering
  system**: no registry row carries W136,
  W298, W401, W617 or W824. (Verified again
  first-hand at this draft against the
  pinned file: the `parpola_1982` Wells map
  carries 498 Wells ids, and none of the
  five codes appears in any row's
  `wells_ids`.) Under the disposition Spec
  070's freeze fixed in advance (DD-070-11),
  the execution closed at gate 0.4 as
  POPULATION NOT KEYED. No join was
  performed and no test quantity computed.
- **Break 2 — the registry's Wells map
  covers barely half the corpus's signs
  (Spec 071).** Of the **557 distinct signs**
  occurring in the primary (documented-lineage)
  population, only **285** key end-to-end to
  an Asset A row. **134** Wells ids have no
  resolution in the registry's
  `parpola_1982` Wells map at all.
- **Break 3 — the classification's universe
  is smaller than the registry (Spec 071).**
  A further **138** signs resolve in the
  registry but sit outside Asset A's
  187-row universe — Asset A was built, by
  Spec 045's contract, over the pinned
  crosswalk's 187 distinct sign keys, and
  the corpus uses signs the crosswalk never
  carried. Spec 071's gate 0.3 stopped the
  run as INVALID rather than let "no
  classification" silently mean "not
  celestial" in the comparison class.
- **The adjacent fact (Spec 071, recorded
  in its outcome).** Asset A's celestial
  class is **empty**: 0 of its 187 rows
  carry `depicted_kind = sky_cycle`. Even a
  perfect coverage repair would have met,
  at Spec 071's gate 0.4, a celestial census
  of zero against that spec's TOO THIN
  floor of 30 members. Any honest repair
  design starts from this fact, and §8
  states what this spec does and does not
  promise about it.

### 1.1 The question, in plain words

The published sign lists of the field —
taken together, read carefully, and cited
row by row — know more signs than the
program's registry and classification
currently carry. Can a repaired surface,
built **only** from those published lists
under the same blind-entry discipline that
built Asset A, state an identity and a
depiction for the signs the corpus actually
uses — and where the published record
genuinely does not identify a sign, say
exactly that, by name, instead of leaving a
silent hole? And after that repair, how
much of the two Hunt populations would
actually key? That last figure is a
measurement this study reports, not a
result it promises.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** The published lists, taken
together, identify — by ICIT/Wells number,
with a citable depiction — materially more
of the corpus's attested signs than the
pinned registry and Asset A now carry, so
a repaired surface keyed from those lists
raises the keyable share of the Hunt
populations above the recorded baselines
(26 of 31 opening-strong signs keyed; 285
of 557 primary-population signs keyed
end-to-end; a celestial class of 0).

**Falsifier.** The hypothesis fails, in
whole or in part, if the full published-source
pass leaves any of the five named codes
(136, 298, 401, 617, 824) still without a
published identity, or leaves the keyable
share at or below its baseline, or leaves
the celestial class empty. Each failure is
a recorded output of this study, not a
defect to be repaired inside it: the study
succeeds by producing a complete, cited
accounting of what the published record
supports — including, if that is the truth,
the finding that the published record does
not support keying these populations, and
that one or both Hunt questions remain
untestable in this form.

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Canonical sign registry, v1 (`data/crosswalks/canonical_sign_registry.csv`) — the file whose Wells coverage Breaks 1–2 measure | SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` (recomputed first-hand at this draft). 803 rows: 396 `parpola_1982`, 407 `yajnadevam_glyphid` (the latter carry no `wells_ids`). The `parpola_1982` Wells map carries **498 distinct Wells ids** (verified at this draft by tokenising `wells_ids` on `\|`). Consumed by hash only; **never edited by this spec** (§4.1). |
| Sign crosswalk of record (`data/crosswalks/sign_crosswalk_master.csv`) — defines Asset A v1's 187-sign universe | SHA-256 `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` (recomputed at this draft). 205 rows, 187 distinct registry sign ids. Consumed by hash only. |
| Asset A v1 (`specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv`) with its freeze record (`asset-a-freeze.json`, same directory) | Canonical CSV SHA-256 `952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b` (recomputed at this draft); 187 rows; per-kind census animal 20, sky_cycle 0, object_goods 14, human 25, other 127, contested 0, unidentified 1. Built by Spec 069 (Phase 432) under Spec 045's frozen §§2–3 contract. Consumed by digest only; **never edited by this spec** (§5.1). |
| Spec 070 outcome record + machine record (Phase 433) | Outcome: `specs/070-hunt-opening-signs-successor/outcome.md` (merged; closure POPULATION NOT KEYED at gate 0.4, freeze digest `763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e`). Machine record: `reports/phase433_results.json` — the enumerated 31-sign opening-strong set with per-sign counts and the five unkeyable codes with occurrence counts (6, 7, 5, 56, 16). Gate 0.2 reproduces Baseline A from these records and the pinned inputs. |
| Spec 071 outcome record + machine record (Phase 434) | Outcome: `specs/071-hunt-sky-signs-successor/outcome.md` (merged; closure INVALID at gate 0.3, freeze digest `c06a7a86804d8da2c9896638446f5712be9eccb8716a7b02303a5944f4bc0478`). Machine record: `reports/phase434_results.json` — the 557-sign coverage census: 285 keyed, 134 with no registry resolution (each listed with its Wells code and population total), 138 resolving outside Asset A's universe. Gate 0.2 reproduces Baselines B and D from these records and the pinned inputs. |
| The Shakti corpus + row grades, cited only through the intake record (P-F1 S1/S2) | Corpus SHA-256 `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`; row-grades SHA-256 `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`; census 5,704 rows / 5,536 analyzable; grades 3,212 documented / 2,087 corroborated / 405 uncorroborated; **713 distinct signs** corpus-wide; intake record `docs/decisions/2026-10-22-shakti-corpus-intake-record.md`. The corpus is an input to coverage measurement only, and only after both product digests exist (§6, join order). |
| Spec 045's frozen §§2–3 (the Asset A contract) | Freeze digest `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`. The field set (§2.2), source hierarchy (§2.3), blind-entry rule (§2.4) and dispute rule (§2.5) that Asset A v2's new rows follow, as extended only where the freeze rules an extension (OPEN-073-1). |

**Published-source candidates** (the repair's
only permissible evidence; the freeze rules
the governing list and hierarchy —
OPEN-073-1; gate 0.3 asserts each ruled
source in hand and pinned before entry):

| Source | State at this draft, stated plainly |
|---|---|
| CISI volumes 1–2 (Corpus of Indus Seals and Inscriptions) — Asset A's governing sources under Spec 045 §2.3 | Held digitally and complete, per Spec 045 §2.3's record. CISI Vol. 3.1 is held restricted-local under PROVENANCE entry 22 (local use and publishable derived statistics permitted; scans never redistributed). |
| Parpola 1994, *Deciphering the Indus Script* (CUP), published sign list (fig. 5.1, pp. 70–78) | The published list Asset F and the crosswalk already rest on; held in the program's sources. |
| Fuls 2023, *A Catalog of Indus Signs* (Mathematica Epigraphica No. 4; ISBN 979-8-398-42230-6; 571 pp.) — the field's sign-by-sign catalogue **in ICIT numbering**, with a description per sign | Held: the owner's purchased copy, PDF on the owner's desktop (SHA-256 `31729a4f7b33bd1ec08633bb677f963b5de8f50d96afdfc25cff5ddc96f9a32a`, PROVENANCE entry 27), with its April-2026 OCR text in the intake tree as a locator. Entry is from the volume itself; the OCR text never governs a label (§5.3). Bibliographic pin re-verified at the freeze. |
| Fuls 2023, *Corpus of Indus Inscriptions* (Mathematica Epigraphica No. 3; ISBN 978-1-671-80486-9, 2nd ed.; 583 pp. as held) — inscriptions in ICIT numbering | Held likewise (PDF SHA-256 `185fd0575d881568583a7002d705b2ded1313a525fafe093108f72e0fe897727`, PROVENANCE entry 27). Corroborating for attestation and numbering; depictions are governed by the Catalog where it speaks. |
| Mahadevan 1977, *The Indus Script: Texts, Concordance and Tables* — the published sign list and tables | Held as scan + OCR in the program's sources. Under Spec 045 §2.3, Mahadevan's list entered Asset A only through a D-18 concordance row; whether it governs directly for new rows, corroborates, or still enters only via a concordance input is a freeze ruling (OPEN-073-1, OPEN-073-6). |
| Wells 1998, *An Introduction to Indus Writing* (MA thesis, University of Calgary; DOI 10.11575/PRISM/23641) — a published sign list in the numbering that became ICIT's basis | Resolved at record level 2026-10-22; the full text's in-hand state is **not asserted at this draft** — gate 0.3 must exhibit it or the source is struck from the ruled list by the freeze, not substituted at run time. Standing (governing vs corroborating) is OPEN-073-1. |
| ICIT database documentation (held PDF, `fuls_icit_documentation.pdf`) | A documentation artefact for the database, **not a published sign list**: a locator for numbering questions only, never a governing source for an identity or a depiction (DD-073-3's companion rule). |

**Excluded as governing evidence, by name:**
the Yajnadevam glyph list and any product
derived from it. Yajnadevam is an extraction
of ICIT itself (provenance audit of
2026-10-22), and Shakti is an ICIT-lineage
corpus: repairing ICIT identities from an
ICIT extraction would grade the lineage
against its own twin — the same circularity
P-F1 S3 fences off. It may be consulted as a
locator (where to look in a governing
source), and a citation to it may never
appear as a row's evidence (DD-073-3).
Program-internal classifications, earlier
phase outputs, the registry's own derived
columns (`corpus_freq`, `start_rate`,
`end_rate`, `internal_rate` — positional
products of an earlier layer, not identity
evidence), and any enterer's visual
judgement are likewise not sources.

## 3. Step 0 — gates before any row is entered (fail-closed)

Execution runs these gates in order, before
any registry row is added and before any
sign is classified. A failure stops the
execution in the class named; nothing is
repaired at run time, and no product of a
later step exists if an earlier gate fails.

- **0.1 Frozen-input integrity.** Registry
  v1, the crosswalk, and Asset A v1's
  canonical CSV each recompute to the §2
  hashes; the Shakti intake asserts under
  P-F1 S1/S2 against the intake record
  (both corpus pins and the census). Any
  mismatch closes the run as **INPUT PIN
  MISMATCH** (the intake limb closes as
  **SHAKTI INTAKE NOT REPRODUCED**, in
  P-F1's words).
- **0.2 Baseline reproduction.** From the
  pinned inputs and the merged Phase
  433/434 machine records, the run
  reproduces, exactly: **Baseline A** —
  the 31-sign opening-strong set, its
  26/5 keyed/unkeyable split, and the five
  codes with their occurrence counts
  (136: 6, 298: 7, 401: 5, 617: 56,
  824: 16); **Baseline B** — the 557-sign
  primary-population census and its
  285 / 134 / 138 split, sign by sign;
  **Baseline C** — the registry's
  `parpola_1982` Wells map at 498 distinct
  Wells ids; **Baseline D** — Asset A v1's
  census (187 rows; sky_cycle 0). Any
  figure that does not reproduce closes
  the run as **BASELINE NOT REPRODUCED**,
  with the differing figure named. The
  repair starts from the recorded failure
  or it does not start.
- **0.3 Sources in hand.** Every source
  the freeze's ruling (OPEN-073-1) names
  as governing or corroborating is
  exhibited in hand and pinned (file hash
  for held digital copies; full
  bibliographic pin for print), and its
  inspectable text is available to the
  enterer. A named source not in hand
  closes the run as **SOURCE NOT IN
  HAND**, with the source named. No
  source is substituted, added, or
  dropped at run time; a source the
  freeze struck (e.g. a Wells 1998 text
  that cannot be exhibited) is recorded
  as struck in the step-0 record, and the
  build proceeds only if the freeze's
  ruling made it non-governing.
- **0.4 Blind-entry setup.** The entry
  protocol of §5.3 is in place and
  attested before the first row: the
  enterer is given the sign inventory
  (ICIT codes as an unordered list, with
  glyphs as printed in the governing
  sources) and the sources — and is
  **not** given any positional class, any
  population membership (including which
  signs are opening-strong or
  terminal-strong), any occurrence count,
  or any output of Specs 070/071 beyond
  the baselines gate 0.2 published. The
  build order is itself a gate (§5.3): if
  entry is found to have been breached at
  any point, the run closes as **ENTRY
  DISCIPLINE FAILED** and neither product
  is frozen.

## 4. Product R1 — the canonical sign registry, version 2

### 4.1 Form

Registry v2 is a **new file**,
`data/crosswalks/canonical_sign_registry_v2.csv`,
with its own SHA-256 digest computed at the
build's freeze step and recorded in this
spec's directory (`registry-v2/registry-v2-freeze.json`,
with the build record and input pins).
Registry v1's file is not edited, renamed,
or superseded in place; consumers of v1
(Specs 070/071's frozen records among them)
stand on v1's hash forever. A consumer
adopts v2 only by its own freeze naming
v2's digest.

Registry v2 keeps v1's schema and carries
every v1 row **verbatim** (all 803 rows,
byte-identical field values), then appends
the repair's additions. A machine-readable
**change schedule**
(`registry-v2/change-schedule.json`) lists
every difference from v1 — every completed
cell and every appended row — each with its
published source and verbatim citation, so
the whole repair is auditable as a diff
against a pinned file, never as an edited
original.

### 4.2 What may be added, and on what evidence

Exactly two addition forms, both from the
freeze-ruled published sources only:

- **(a) Wells-map completions.** Where a
  ruled published concordance or sign list
  states a Wells identity for a sign a v1
  `parpola_1982` row already carries, the
  v2 copy of that row's `wells_ids` gains
  the stated token(s). The change schedule
  records the source, the page or entry,
  and the source's own wording.
- **(b) Rows for ICIT codes with no v1
  row.** Where a ruled published source
  states a sign under an ICIT/Wells number
  that no v1 row carries in any numbering
  system, v2 appends a row:
  `numbering_system` = `icit_wells` (the
  new value the freeze confirms,
  OPEN-073-2), `sign_id` assigned in the
  stated form `W` + the zero-padded code,
  `wells_ids` carrying that code, and
  `description` carrying the source's
  verbatim description of the sign. All
  other fields are empty — v2 invents no
  derived values, and the positional
  columns of v1's rows are carried, never
  recomputed or extended (they are not
  identity evidence, §2).

Every addition carries its citation in the
change schedule; an addition without a
citable published statement is not made.
Where two ruled sources state different
Wells identities for the same drawn sign,
both are recorded in the change schedule
and the affected code's disposition is
**CONTESTED IDENTITY** (§4.3) until a
future freeze rules a route — v2 does not
silently pick one, and a code with a
contested identity is not a resolution for
any consumer counting distinct `sign_id`s.

### 4.3 The NO PUBLISHED IDENTITY schedule

Every ICIT code attested in the Shakti
corpus (the frame of §5.2) that, after the
full ruled-source pass, still has no
published identity is named in a schedule
published with the build record
(`registry-v2/no-published-identity.json`):
the code, its attestation (which grade
strata it occurs in), and the sources
searched for it. These codes are **named,
never silently dropped**: they are the
study's residual shortfall, stated sign by
sign, and any future consumer sees them
before it sees a coverage percentage.

## 5. Product R2 — Asset A, version 2

### 5.1 Form

Asset A v2 is a **new asset** in this
spec's directory
(`asset-a-v2/depicted-kind-classification.csv`,
with `asset-a-v2/asset-a-v2-freeze.json`
carrying its SHA-256 digest, build record,
and input pins — the form of Spec 045
§2.1, applied to this spec's own
directory). Asset A v1's file, freeze
record, and digest are untouched; gate 0.1
asserts v1's digest before the build and
the closing record re-asserts it after
(§7, FROZEN INPUT MUTATED). Nobody
consumes v2 until a future freeze names
its digest.

### 5.2 The universe

Asset A v2's universe is the union of:

- **(a) the carried rows** — all 187 of
  Asset A v1's sign keys, carried
  **verbatim**: same `sign_key`, same
  depicted kind, same verbatim label, same
  citations. Carried rows are not
  re-entered, re-adjudicated, or improved;
  a defect found in a carried row is
  recorded as a defect against v1 in the
  build record, never corrected inside v2
  (the correction, if any, is a separate
  act against v1's own record); and
- **(b) the new rows** — every sign
  attested in the Shakti corpus's
  documented + corroborated rows (the
  attested frame; uncorroborated rows
  attest nothing, per P-F1 S4) that
  resolves to exactly one registry
  identity in Registry v2 and is not
  already a carried row. The frame is
  enumerated from the pinned corpus at
  the build, after Registry v2's digest
  exists, and published in the build
  record with its count. (The documented
  stratum alone carries 557 distinct
  signs per Baseline B; the corpus-wide
  total is 713.)

Attested signs that do not resolve in
Registry v2 receive **no v2 row** — a row
requires a registry identity to key — and
their disposition is the §4.3 schedule.
That is a stated boundary of the asset's
form, inherited from Spec 045 §2.1 (rows
are keyed by crosswalk/registry identity),
not a quiet omission: the schedule is a
product of this spec, published beside the
asset.

### 5.3 Entry discipline for new rows

New rows follow Spec 045 §§2.2–2.5
field-for-field — `sign_key` (the Registry
v2 `sign_id` of the resolved row),
`cisi_no` / `parpola_no` where the registry
records them, `depicted_kind` (exactly one
of `animal`, `sky_cycle`, `object_goods`,
`human`, `other`, `contested`,
`unidentified`), `depicted_label_verbatim`
(the governing source's own words, copied),
`governing_source`, `source_citations`
(every source consulted, with its verbatim
label where it gives one), `agreement`,
`dispute_status`, `d18_input` (`none`
unless the freeze rules a concordance
input under OPEN-073-6), `entered_blind` —
plus one field v1 did not carry,
**`row_origin`** (`carried_v1` or
`new_entry`), so no reader can mistake a
repaired row for part of the frozen
original (the freeze confirms or drops
this field, OPEN-073-4).

The discipline, carried from Spec 045
§§2.3–2.5 and Spec 069's executed build:

- **Sources only as ruled.** Labels come
  only from the freeze-ruled published
  sources, in the hierarchy the freeze
  fixes (OPEN-073-1). The drafted default
  hierarchy for new rows is: (1) the CISI
  volumes, where the sign is identifiable
  in them; (2) Fuls 2023, *A Catalog of
  Indus Signs* — the ICIT-native published
  catalogue — governing ICIT identities
  and, where CISI is silent, depictions;
  (3) Parpola 1994's published
  identifications; (4) Mahadevan 1977 and
  Wells 1998 as corroborating or
  contesting only, mirroring Spec 045's
  caution about lists that entered v1
  only through a concordance row. The
  freeze may rule otherwise, openly; what
  it may not do is leave the hierarchy
  unstated.
- **Blind entry.** Entry is blind to
  positional results (§3, gate 0.4). The
  build order is: sources consulted →
  Registry v2 built and digested → frame
  enumerated → new rows entered → dispute
  coding completed → Asset A v2 digest
  computed → **only then** any join to
  corpus or positional data (§6). Entry
  from the Fuls volumes is from the
  volumes themselves (page images/print);
  the April-2026 OCR texts are locators
  only and never govern a label — an OCR
  misread entered as a label would be an
  entry defect of exactly the kind the
  verbatim-citation rule exists to catch.
- **Disputes.** Where ruled sources
  disagree on a new row's depicted kind,
  the row is `contested` with both
  verbatim labels and citations recorded;
  no tie is broken by the enterer, by
  frequency, or by which label would suit
  any test (Spec 045 §2.5, carried).
  `borderline` is recorded where the
  published identification is hedged in
  its own source.
- **Unidentified.** A resolved sign no
  ruled source depicts receives
  `depicted_kind = unidentified`, with the
  sources searched recorded in place of a
  citation (Spec 045 §2.2's form).
  `unidentified` is a bookkeeping value:
  it is never pooled into any kind, and no
  consumer of v2 may read it as "not
  animal" or "not celestial" — that
  reading is the exact failure Spec 071's
  gate 0.3 exists to forbid.
- **Pass structure.** As in Spec 069's
  executed build: a first entry pass from
  the verbatim source labels and an
  independent rule pass over the same
  labels, disagreements adjudicated on
  the record by re-reading the verbatim
  label, the log published with the asset
  (`asset-a-v2/entry-decisions.json`).
  Whether a second human-style enterer
  spot check is added is OPEN-073-5.

### 5.4 Build gates (fail-closed, in order)

After entry and dispute coding, and before
any digest is computed:

- **B1 — Universe completeness.** Every
  sign in the §5.2 universe has exactly
  one v2 row. A missing or duplicated row
  closes the build as **ASSET FAILED
  (B1)**.
- **B2 — Citation completeness.** Every
  new row carries at least one citation
  to a ruled published source, or is
  `unidentified` with its sources-searched
  recorded. An uncited row closes the
  build as **ASSET FAILED (B2)**.
- **B3 — Carried-row fidelity.** Every
  carried row is field-identical to its
  v1 row. Any difference closes the build
  as **ASSET FAILED (B3)** — v2 does not
  launder edits to v1.
- **B4 — Blind-entry attestation.** The
  build record attests gate 0.4's protocol
  held for every entry session; a breach
  closes the run as **ENTRY DISCIPLINE
  FAILED** (not repaired inside this
  spec).
- **B5 — Digest.** Both product digests
  recompute from the canonical files as
  written (CSV generated with a CSV writer
  and round-trip validated, per Spec 045
  §2.1 — hand-edited CSV is not an asset).

## 6. Coverage measurement (after both digests exist)

Only after Registry v2 and Asset A v2 are
frozen-in-build (digests computed, gates
B1–B5 passed) does the run join anything.
The join route is DD-070-9's route restated
against the v2 files: a Shakti ICIT code
*n* resolves through Registry v2's
`parpola_1982` rows' `wells_ids` **and**
through v2's appended `icit_wells` rows,
to exactly one `sign_id`, and keys
end-to-end if that `sign_id` carries an
Asset A v2 row. (This route is stated here
so a future freeze can adopt or amend it
in the open; this spec freezes no route
for any consumer.) The measurements,
reported in full whatever their values:

- **M1 — Registry Wells coverage.** The
  count of distinct Wells ids resolvable
  in Registry v2, split by row class
  (carried `parpola_1982` map; completions;
  appended `icit_wells` rows), against
  Baseline C's 498.
- **M2 — The five named codes.** Each of
  136, 298, 401, 617, 824, with its
  disposition: resolved (to which
  `sign_id`, on which source) and keyed
  end-to-end or not; **NO PUBLISHED
  IDENTITY**; or **CONTESTED IDENTITY**.
  The five are reported by name, never
  only as a count.
- **M3 — Keyable share of the recorded
  populations.** End-to-end keyed counts
  for (i) the 31-sign opening-strong set
  (baseline 26) and (ii) the 557-sign
  primary population (baseline 285), each
  as *n* of *N* with the unkeyed remainder
  listed sign by sign with reasons
  (no registry resolution / contested
  identity / resolved but no v2 row).
  These are coverage statements about a
  join surface. They are **not** Spec
  070's or 071's tests re-run: no
  positional quantity is computed, no
  comparison class is formed, and no
  verdict word of either spec is used.
- **M4 — Asset A v2 census.** Rows by
  depicted kind, split by `row_origin`,
  with the **celestial census stated
  plainly**: the number of `sky_cycle`
  rows in v2 (baseline for v1: 0), set
  beside Spec 071's recorded TOO THIN
  floor of 30 members as a bare comparison
  of numbers — not a scoring of Spec 071,
  whose gate never ran on v2 and whose
  re-freeze, if any, is a separate act.
- **M5 — The residual shortfall.** The
  §4.3 schedule's size and contents:
  attested signs still without a published
  identity after the full pass, with their
  attestation strata. M5 is reported in
  the headline block, not an appendix: a
  reader of the headline sees what the
  repair could not do.

## 7. Criteria, outcome set, and pre-written wordings

The execution ends in exactly one of these
classes. The success classes differ only in
what the measurements found; both are
complete executions of the study.

- **KEYING SURFACE REPAIRED** — all gates
  passed, both products frozen with
  digests, and M5 is empty with all five
  named codes resolved and keyed. Wording:
  "Spec 073 repaired the keying surface:
  Registry v2 and Asset A v2 are frozen
  with digests [recorded], built from
  published sources only under blind
  entry. Every sign attested in the graded
  Shakti frame now resolves, and the
  keyable shares are [M3 figures]. This
  establishes nothing about whether
  opening signs are animal signs or sky
  signs gather at text endings; those
  questions stand exactly as Specs 070 and
  071 left them, and any re-asking
  consumes these products under a new
  freeze."
- **REPAIRED WITH NAMED SHORTFALL** — all
  gates passed and both products frozen,
  but M5 is non-empty, or any named code
  is unresolved or contested, or the
  celestial census is zero. Wording: as
  above, with the headline carrying the
  shortfall by name: "…except the
  following, which no ruled published
  source identifies: [codes/signs]. The
  celestial class in Asset A v2 numbers
  [M4 figure]. Where the shortfall leaves
  a Hunt question unkeyable, this record
  says so; it does not soften the count."
- **SOURCE NOT IN HAND** (gate 0.3),
  **BASELINE NOT REPRODUCED** (gate 0.2),
  **INPUT PIN MISMATCH** / **SHAKTI
  INTAKE NOT REPRODUCED** (gate 0.1),
  **ENTRY DISCIPLINE FAILED** (§5.3),
  **ASSET FAILED (gate named)** (§5.4):
  closure classes, each worded in the
  outcome record with the gate, the
  differing figure or missing source
  named, and the statement that neither
  product exists.
- **FROZEN INPUT MUTATED** — the closing
  re-assertion finds registry v1, the
  crosswalk, or Asset A v1 changed in any
  byte. This class voids both products
  regardless of any other result and is
  reported as an integrity finding, not an
  outcome.

No other outcome is available. In
particular there is no outcome in which
this spec reports a positional result, a
verdict on manual_003 or manual_004, or a
recommendation about whether either
question should be re-asked.

## 8. Epistemic limits (binding on all outputs)

- **What a repair establishes.** Facts
  about the join between published lists
  and this corpus: which attested signs
  the published record identifies, on
  which citations, and how much of two
  recorded populations a v2-keyed join
  would cover. Nothing else.
- **The celestial limit, stated in
  advance.** A repaired surface does not
  guarantee the celestial class reaches
  any floor — or reaches one member. If
  the ruled published sources identify no
  celestial depictions among the newly
  covered signs, Asset A v2's `sky_cycle`
  census is what the sources support,
  including zero, and the honest output
  of this study is that Spec 071's
  question remains untestable in this
  form. No row is ever created, split, or
  re-labelled to fill the class: a
  celestial row exists only where a
  published source's own words depict a
  sky or cycle object for that sign.
- **Lineage honesty (P-F1 S3).** Shakti is
  an ICIT-lineage corpus; Registry v2's
  ICIT identities come from the same
  published tradition (Fuls/Wells) that
  numbers the corpus. Agreement between
  the repaired surface and the corpus's
  numbering is therefore consistency
  within one tradition, stated wherever
  the coverage figures are reported, and
  never presented as independent
  corroboration.
- **Carried rows are v1's record.** Asset
  A v2's carried rows inherit v1's
  epistemic standing exactly — including
  its one `unidentified` row and its empty
  celestial class as entered — and the
  carry is visible in every product via
  `row_origin`.
- **No silent absence.** Every attested
  sign has a named disposition in the
  products (§4.3, §5.2, M5). A sign
  missing from every product is a defect
  in the build, and B1 exists to catch
  it.

## 9. Controls and named confounders

- **Circularity via the lineage** —
  controlled by DD-073-3 (Yajnadevam and
  all ICIT-derived products excluded as
  evidence; locators only) and by the
  lineage statement (§8).
- **Positional contamination of entry** —
  the registry's derived rate columns and
  the Phase 433/434 population lists are
  positional products; the enterer works
  from the unordered inventory and the
  sources (gate 0.4), and the coverage
  joins run only after both digests exist
  (§6). The inventory given to the
  enterer carries no occurrence counts:
  a frequent sign (617, 56 occurrences)
  must be exactly as easy to leave
  unidentified as a rare one.
- **OCR error masquerading as a published
  label** — controlled by §5.3's rule
  that entry is from the volumes
  themselves, OCR texts as locators only,
  and verbatim labels quoted so a reader
  can check them against the page.
- **The crosswalk temptation** — extending
  `sign_crosswalk_master.csv` instead
  would edit a file Spec 045's contract
  and two freezes pin; refused (DD-073-2).
  Registry v2 + Asset A v2 carry the
  repair; the crosswalk stands.
- **Frequency-driven adjudication** —
  disputes and identities are settled by
  the sources' words only (§5.3); the
  change schedule makes every settlement
  inspectable.

## 10. Reporting obligations

The execution's record (outcome.md in this
directory, with the machine record) must
carry: the step-0 exhibits (recomputed
hashes, reproduced baselines figure by
figure, the sources-in-hand pins, the
blind-entry attestation); both product
digests with their censuses; the change
schedule's size and its contested-identity
entries; the §4.3 schedule in full;
measurements M1–M5 in the headline block
with the P-F1 S3 lineage statement; the
closing re-assertion of the v1 pins; and
the outcome class in §7's pre-written
wording. The dated record is appended to
the program LEDGER per convention. No
append is made to the records of Specs
045, 069, 070 or 071, and none to either
Hunt claim's record: this study's outcomes
belong to its own record.

## 11. Stop conditions

Execution stops, in the named class, on:
any step-0 gate failure (§3); a blind-entry
breach discovered at any point (ENTRY
DISCIPLINE FAILED); a build-gate failure
(§5.4); discovery that a ruled source's
text in hand is incomplete for the signs
it was ruled to govern (SOURCE NOT IN
HAND, recorded when found — the build does
not quietly narrow a source's role); or
the closing non-mutation check failing
(FROZEN INPUT MUTATED). There is no
stop condition keyed to the measurements:
a disappointing M3 or an empty celestial
census is a result, and the run completes
and reports it.

## 12. Execution shape (gated; NOT run by this draft)

Graph-first per program convention
(H15/H23): step-0 exhibits script →
Registry v2 build (writer-generated CSV,
round-trip validated, change schedule
emitted by diff against pinned v1) →
frame enumeration → blind entry with the
two-pass log → dispute coding → digests →
coverage measurement script (joins only,
no positional quantities) → outcome
record. The labour is entry: the new-row
frame is bounded by the attested frame
(713 corpus-wide signs, less the carried
187 and the unresolvable), read against
the ruled sources sign by sign. Compute is
trivial; the cost is careful reading. No
external cost; the Fuls volumes and CISI
are already held.

## 13. What this spec is not

- Not a re-run, amendment, or appeal of
  Spec 070 or Spec 071; their closures,
  freeze digests, and claim standings are
  untouched, and no quantity in this spec
  is computed under either spec's test.
- Not an amendment of Spec 045's contract
  or Spec 069's Asset A: v1's file, digest,
  and record stand; v2 is a new asset that
  a future freeze may adopt or ignore.
- Not a decipherment claim: an identity in
  Registry v2 says a published list numbers
  a sign so; a depiction in Asset A v2
  says a published source describes the
  sign so. Neither says what any sign
  meant or sounded like.
- Not a promise about the celestial class
  (§8), nor a recommendation that either
  Hunt question be re-frozen. It hands a
  future owner decision a repaired,
  measured surface — and, if the published
  record is thinner than the questions
  need, the named proof of that.

## 14. Open items the freeze must rule

1. **OPEN-073-1 — The governing source
   list and hierarchy** for new material:
   confirm or amend §5.3's drafted default
   (CISI → Fuls 2023 Catalog → Parpola
   1994; Mahadevan 1977 and Wells 1998
   corroborating/contesting only), and
   rule Wells 1998's standing in light of
   what gate 0.3 can exhibit of its text.
2. **OPEN-073-2 — Registry v2's form:**
   the new versioned file and the
   `icit_wells` numbering value as drafted
   (§4.1–4.2), or a supplement-file form
   ruled openly instead.
3. **OPEN-073-3 — Asset A v2's universe
   frame:** the attested frame as drafted
   (documented + corroborated rows;
   §5.2(b)), or the documented stratum
   only, stated openly.
4. **OPEN-073-4 — The `row_origin`
   field:** confirm, or drop it and state
   how carried rows are distinguished.
5. **OPEN-073-5 — Entry checking:** the
   two-pass rule reconciliation as
   executed for v1 (drafted default), or
   an added second-enterer spot check over
   a stated sample of new rows.
6. **OPEN-073-6 — Concordance inputs:**
   whether Mahadevan/Wells identifications
   enter via a D-18-style concordance
   input (Spec 045 §2.6's form) or by
   direct entry from the volumes under
   §5.3's hierarchy.
7. **OPEN-073-7 — OSF registration** at
   the freeze, in the program's contract
   form.
8. **OPEN-073-8 — The execution phase
   number**, allocated from the merged
   record as it then stands.
9. **OPEN-073-9 — Pins re-asserted:** the
   §2 table re-verified against the merged
   records (including the Fuls volumes'
   bibliographic pins and PROVENANCE
   entry 27), and any pin that cannot be
   re-asserted is a freeze failure, not a
   drafting licence.
