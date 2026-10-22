# Spec 072 — Parpola's Fish-Sign Family, Sign by Sign, in ICIT Numbering on the Shakti Corpus (the Spec 048 Question, Re-Designed)

> ## FROZEN — 2026-10-22
>
> Frozen at the freeze act of 2026-10-22 under
> the owner's freeze rulings of 2026-10-22 on
> the freeze-gate package for the Shakti draft
> specs (the draft was commissioned under the
> owner's readiness decisions of 2026-10-22,
> decision 4: the ICIT-native fish-family
> re-design). The freeze record is `freeze.md`
> / `freeze.json` in this directory; the
> AEE lifecycle hooks ran at the freeze gate
> and passed over the recovered register
> (`aee/freeze-aee-note.md`); the freeze-stage
> step-0 acts are recorded in `freeze.md`
> (gates 0.1–0.5, including the concordance
> act and the derived verdict line **L =
> 0.765**, whose reference-distribution record
> is `reference-distribution.json` in this
> directory). The spec's OSF contract
> registration is filed at the freeze under
> campaign decision E-1
> (`osf-spec-registration.md`). **Execution
> is a separate later act**: it runs as
> **Phase-431**, after this freeze has
> merged; the execution order for it was
> given in the same owner tasking that
> commissioned this freeze. At the freeze
> itself no fish member
> has been scored: the freeze-stage acts
> computed the census and the non-member
> reference distribution only, exactly as
> §5.3 prescribes.
>
> This is a **new design answering Spec
> 048's question**. Spec 048 stands closed
> exactly as recorded — executed 2026-10-21,
> closed at its step 0 as **STRICT CORPUS NOT
> PINNABLE** (gate 0.3). Its gate 0.3 is **not
> amended, not repealed, and not re-run** by
> this spec; nothing here reopens, patches,
> or supersedes Spec 048's record. Where
> this design differs from Spec 048 — a
> different corpus, a different numbering,
> reference behaviour measured for the first
> time instead of reproduced, and a verdict
> line derived instead of inherited — it
> differs because it is a new design, and it
> says so wherever the difference matters.
>
> The execution phase number is **Phase-431**,
> allocated at the freeze act (OPEN-072-8).

**Design source:** the readiness assessment
of 2026-10-22 (Workstream F), §1.5 (Spec 048:
"DOES NOT TRANSFER"; the re-design's three
needs stated there), §1.6 (proposal P-F1,
the Shakti intake gates S1–S4), and §3
Family 5 (fish-family profiles in ICIT
numbering), read in full at this draft; with
Spec 048's frozen text (design D-04) as the
statement of the question, and the Phase-43
battery record recovered in Amendment Queue
Item 2 (`research_notes/
amendment-queue-2026-10-21/
item-2-phase43-battery.md`) as the source of
the carried method (§5).

**Claim under test:**
`parpola_2010_dravidian_solution_manual_002`
— "The fish sign (meen in Dravidian) is the
primary rebus sign in the Indus script" —
standing **IN QUESTION, partially supported**:
Mahadevan sign 72 passed its Phase-43 T2.4
positional test; sign 267, the family's most
frequent member, failed it clearly. That
standing is Spec 048's record and this
spec's starting point; this spec does not
re-derive it and does not inherit Spec 048's
calibration (see §5.3).

**AI disclosure:** this draft is produced by
an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per
constitution §VI.

---

## 1. The claim and the record it stands on

The claim says *the fish sign* — a family of
related fish signs — works as the script's
primary sound-sign (the 'meen' reading). The
program's Phase-43 test T2.4 asked whether
the signs that follow a fish sign behave the
way case endings should if the fish sign were
a word being read aloud. The recorded result
is a split family (read first-hand at this
draft from `outputs/phase43_all.json`,
§T2_4_fish_rebus, and from Spec 048's frozen
text):

- **Sign 72** — 181 occurrences, ending-follower
  (terminal) fraction **25.9%**, recorded
  supported.
- **Sign 267** — 356 occurrences, ending-follower
  fraction **3.8%**, recorded not supported;
  the family's most frequent member.
- Six fish candidates were tested in total:
  **267, 72, 65, 59, 60, 70** (the Phase-43
  record's own list, in Mahadevan numbering).

Spec 048 (design D-04) was the sign-by-sign
family test of that split, run against
Asset F — the fish-family list frozen at
Spec 044's step 0 — on the V3 /
Mahadevan-lineage corpus. It closed at its
gate 0.3 because that corpus's data file is
absent and the T2.4 reference points could
not be re-derived from a pinned layer. Its
claim stands exactly as recorded.

This spec asks the same question on a
different, held corpus: the ShaktiOSindia
corpus (below, §2), which is numbered in
**ICIT (Wells/Fuls) codes** and graded row
by row for provenance. On that corpus the
question can be asked natively — the family
identified in Wells/ICIT codes, the
T2.4-analogue measure computed in ICIT
space, reference behaviour measured on this
corpus for the first time. Nothing about
that is a reproduction of Phase-43, and no
output of this spec may call it one.

### 1.1 The question, in plain words

Do the fish-family signs behave, sign by
sign, the way their recorded profiles claim
— what follows a fish sign looking like text
endings at the rate the 'meen' reading
predicts — when the test is run natively in
ICIT/Wells numbering on the graded Shakti
corpus? One member of the family behaved as
predicted on the old corpus and the
commonest member did not. Is the family
uniform, or was the one pass the exception?

### 1.2 The hypothesis and its falsifier

**Hypothesis.** If the fish family carries
one reading, its members should share the
positional behaviour the reading predicts:
members carrying **more than half** of the
family's tested occurrences — a strict
token-weighted majority — pass the member
criterion of §5.3 (an ending-follower
fraction at or above the verdict line fixed
at the freeze under the derivation rule of
§5.3).

**Falsifier.** The hypothesis fails if
members carrying **half or less** of the
family's tested occurrences pass the member
criterion, so most fish-sign occurrences are
*not* followed by text-ending behaviour.
(The borderline case — a passing share of
exactly half — is INCONCLUSIVE under §6,
not a pass for either side.)

The 70% / 30% family lines and the 20%
member bar of Spec 048 are **not** carried
into this design: they were calibrated
between the Phase-43 reference points, and
§5.3 excludes those points as inputs. The
majority line used here is the plain
meaning of "the family's token-weighted
majority" in the falsifier, stated as a
draft-fixed reading (DD-072-2) and put to
the freeze for confirmation (OPEN-072-5).

## 2. Inputs (pinned at this draft where a pin exists; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/parpola_2010_dravidian_solution.json`) | SHA-256 `3202aeca1ddaf7e588ebf19b2eaf8c93d06a34ecebba20d06c1b22810dfb000c` (the pin Spec 048's frozen text carries, read at this draft from that text). Manual_002's standing — IN QUESTION, partially supported, sign 72 passed T2.4, sign 267 failed it — is taken from this record as Spec 048 states it. |
| Phase-43 results (`outputs/phase43_all.json`) — the historical record of the split this question starts from | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` (the pin Specs 044–054 carry). §T2_4_fish_rebus: candidates [267, 72, 65, 59, 60, 70]; sign 72 — 181 occ., terminal_frac 0.259, supported; sign 267 — 356 occ., terminal_frac 0.038, not supported. **These fractions are history, not inputs to any threshold in this spec (§5.3).** |
| Item 2 battery record (`~/workspace/research_notes/amendment-queue-2026-10-21/item-2-phase43-battery.md`) — the recovered Phase-43 battery, stated in code | Producing script `phase43_part2.py`, SHA-256 `6d5a079d47113937afd3340ab4b35781d1b7202644b180ba814d15f03f49699e` (as recorded in Item 2 §1.1). The T2.4 method carried from this record is stated in §5.2 and labelled **carried method** wherever it is used. It is carried as method, never as reproduced reference points: no Phase-43 count or fraction is an input to this spec's verdict. |
| **Asset F** — the fish-family list, built and frozen at Spec 044's step 0 under Spec 044 §4's contract | Canonical file `specs/044-fish-sign-coastal-residue/asset-f-fish-family.json` on `main`; **7 members**; digest (SHA-256 of the canonical bytes with the `digest` field excluded, Spec 044 §4.2's rule) **`ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3`**, `frozen_at` 2026-10-21, as recorded in the canonical file itself and asserted in Spec 044's step-0 outcome record (census there: M047 13, M048 157, M050 17, M052 22, M060 20, M145 3, M147 2 — on Spec 044's pinned layer, stated here as the asset's provenance, not as counts under this spec). The member list is quoted exactly in §4. Gate 0.2 asserts this digest at execution step 0. |
| **The Shakti corpus** — `sanitized_corpus.json`, the ShaktiOSindia deposit, held restricted-local under its GPL-3.0 terms | SHA-256 **`345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`** (the deposit README pin, verified in the provenance audit of 2026-10-22). 5,704 rows; 5,536 analyzable (not entirely illegible); 713 distinct signs; 77 sites; CISI identifiers on 4,904 of 5,536 analyzable rows (88.6%). The corpus file itself is **not** in this repository and is never committed under this spec; it is cited only through the intake record (next row). |
| Row grades — the provenance audit's per-row grades file (`research_notes/shakti-provenance-audit-2026-10-22.md` is the audit of record) | SHA-256 **`02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`** (as recorded for the intake). Grade counts: **documented-lineage 3,212 rows** (3,045 analyzable); **undocumented-corroborated 2,087 rows** (2,086 analyzable — the one all-`000` corroborated row, H-986, is in the 2,087 but not in the analyzable subset and enters no sign analysis regardless); **undocumented-uncorroborated 405 rows**. The label "undocumented" stays on the corroborated stratum in every product (§7, P-F1 S4). |
| Shakti intake record (`docs/decisions/2026-10-22-shakti-corpus-intake-record.md`) — proposal P-F1 (gates S1–S4) as adopted | **State at this draft, stated plainly:** the intake record is in parallel creation and is **not on `main`** at this draft (verified by direct lookup at drafting, 2026-10-22). This draft therefore pins the corpus and the row grades by the SHA-256 values above — taken from the readiness assessment §1.6 / P-F1 text and the provenance audit, both read first-hand — and names the intake record as the pin source of record. The freeze re-asserts every pin in this table against the merged intake record; a disagreement between this draft and that record is a freeze failure, not a drafting licence (OPEN-072-9; adjudication §6, defect 3). |
| Mahadevan–Parpola crosswalk (`backend/glossa_lab/data/mahadevan_parpola_crosswalk.json`) — the locator source joining Asset F members to Parpola's published list | SHA-256 `9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b` (the pin Specs 044 and 048 carry). Asset F's source: Parpola, Asko. 1994. *Deciphering the Indus Script*. Cambridge: CUP — the published sign list (fig. 5.1, pp. 70–78), as cited in this crosswalk. |
| Concordance basis for Wells/ICIT identities — the programme's held crosswalk and registry files | **No single basis file is asserted as governing at this draft, deliberately.** The held candidates, all on `main` and read at this draft, are: `data/crosswalks/canonical_sign_registry.csv` (carries a `wells_ids` column per registry sign); `data/crosswalks/sign_crosswalk_master.csv` (205 rows; registry sign ids across numbering systems); and `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv` (ICIT/Yajnadevam glyph numbers to Parpola matches; 192 data rows — the provenance audit records 184 confirmed glyph mappings of the 592 glyphs in the upstream dump, so this basis is **partial by its own record**). Gate 0.3 performs the concordance on a **stated** basis and pins the basis file(s) by SHA-256 in the step-0 record; the freeze confirms which basis governs (OPEN-072-2). Inventing a complete basis at draft would repeat the crosswalk-gap failure the Spec 049 record documents. |

## 3. Step 0 — gates before any fish sign is counted (fail-closed)

Execution runs these gates in order, before
any member's ending-follower fraction is
computed in either population. A failure
stops the execution in the class named;
nothing is repaired at run time, and no
count produced before a gate failure is
quotable.

- **0.1 Shakti intake assertion (P-F1 S1/S2).**
  The execution recomputes the Shakti corpus
  file's SHA-256 and the row-grades file's
  SHA-256 and asserts both against the
  intake record (§2 pins), and reproduces
  the audit's census from the pinned files:
  5,704 rows; 5,536 analyzable; grade counts
  3,212 documented-lineage / 2,087
  undocumented-corroborated / 405
  undocumented-uncorroborated; 4,904 of 5,536
  analyzable rows (88.6%) carrying a CISI
  identifier. If either hash differs or the
  census does not reproduce, the run closes
  as **SHAKTI INTAKE NOT REPRODUCED** (§6
  wording) and nothing is counted.
- **0.2 Asset F digest assertion.** The
  execution exhibits Asset F's canonical
  file (preserved in Spec 044's directory on
  `main`), recomputes its SHA-256 over the
  canonical bytes **with the `digest` field
  excluded** (Spec 044 §4.2's exclusion
  rule), and compares it to the digest
  recorded in §2 (`ca5fb1b5…`). If the file
  does not exist in the execution tree, the
  run closes as **ASSET F NOT AVAILABLE**;
  if the recomputed digest differs, the run
  closes as **ASSET F DIGEST MISMATCH**
  (§6 wordings). The asset is never rebuilt,
  re-derived, or substituted under this
  spec, in either case.
- **0.3 The concordance act.** For **every**
  Asset F member, the step-0 record states
  the member's Wells/ICIT identity — the
  ICIT sign code as it appears in the Shakti
  corpus file — and pins that statement in
  the record, on the concordance basis the
  freeze confirmed (OPEN-072-2): the basis
  file(s) named, each pinned by SHA-256,
  and for each member the basis entry the
  identity was read from. A member whose
  Wells/ICIT identity **cannot be stated**
  on that basis is named in the step-0
  record as **UNIDENTIFIED IN ICIT**, with
  the basis gap stated. An unidentified
  member is **never silently dropped and
  never substituted** — no other sign is
  counted in its place, and it is not
  counted as TOO THIN. Its disposition is
  the one **ruled at the freeze**
  (OPEN-072-2; the draft's proposed ruling
  is DD-072-5: excluded from both
  populations' weighting, reported in the
  headline block, its occurrence share of
  the identified family stated). If **no**
  member can be identified, the run closes
  as **CONCORDANCE FAILED** (§6 wording).
  The step-0 record also reports the
  cross-check, for the record only: Asset
  F's membership against the claim record's
  named trio (Mahadevan 72, 64, 70) and the
  Phase-43 six candidates (267, 72, 65, 59,
  60, 70), with every divergence named —
  noting plainly that Asset F and those
  lists are different sets (Asset F holds
  none of 267, 72, 65, 59, 64, or 70; of
  the Phase-43 six only 60 appears, as
  M060), and that the cross-check adds and
  removes no member.
- **0.4 Positional classes and census
  (margins only).** On the primary
  population (§5.1), the execution computes
  the positional classes of §5.2 over the
  whole population — occurrence counts and
  position counts only, no follower
  quantity — and the per-member census:
  for each identified member, its total
  occurrence count in each population.
  Members are classified for reporting by
  the carried floors (§5.2): below the scan
  floor, **NOT SCANNED**; at or above the
  scan floor but below the supported floor,
  **SCANNED — BELOW SUPPORTED FLOOR**; at
  or above the supported floor, testable.
  If **no** identified member is testable
  in the primary population, the execution
  closes as **TOO THIN** (§6 wording) with
  the full census as its finding.
- **0.5 Verdict-line assertion.** The step-0
  record exhibits the verdict line **L** as
  fixed in this spec's freeze record under
  the derivation rule of §5.3, together with
  the freeze's reference-distribution record
  it was derived from (its pin and its
  population statement). If no freeze-fixed
  L exists — an execution attempted on this
  draft, or a freeze record that does not
  state one — the run closes as **INVALID**
  (§6 wording): no member is scored against
  a line invented at run time, and no line
  is derived after any member's fraction
  has been seen.

P-F1 **S3** (the lineage statement, §9) and
**S4** (grade discipline, §5.1) are not
step-0 gates; they bind every product and
every count throughout, and a failure of
either is an integrity finding reported as
such, not repaired silently (P-F1's own
terms).

## 4. Asset F — the consumed contract, and the member list exactly as recorded

This spec consumes Asset F exactly as Spec
044 froze it; this section restates the
contract only so the consumer's obligations
are in one place. Spec 044's text governs
in any conflict.

- **Form.** One canonical JSON file,
  `asset-f-fish-family.json` (UTF-8, keys
  sorted, members sorted by `sign_key`),
  built once at Spec 044's step 0 solely
  from Parpola's published list (Parpola
  1994, fig. 5.1, pp. 70–78).
- **Identity.** The SHA-256 of the canonical
  bytes, with the file's `digest` field
  excluded from the hashed bytes:
  `ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3`,
  `member_count` 7, `frozen_at` 2026-10-21.
- **The member list, quoted exactly as
  recorded** in the canonical file (each
  member: `sign_key`, Mahadevan number,
  Parpola number, depiction note, inclusion
  basis; every member `contested: false`):

  | sign_key | Mahadevan | Parpola | Depiction note | Inclusion basis |
  |---|---|---|---|---|
  | M047 | 47 | 47 | fish (plain) | parpola-list-fish |
  | M048 | 48 | 48 | fish-with-roof | parpola-list-fish-variant |
  | M050 | 50 | 50 | fish-with-fins | parpola-list-fish-variant |
  | M052 | 52 | 52 | fish-with-trefoil | parpola-list-fish-variant |
  | M060 | 60 | 60 | fish (variant; 'badly drawn') | parpola-list-fish-variant |
  | M145 | 145 | 145 | fish with two horizontal lines | parpola-list-fish-variant |
  | M147 | 147 | 147 | fish (sign-list variant) | parpola-list-fish-variant |

  Per-sign source locator for every member:
  "Parpola 1994, fig. 5.1 sign list, entry
  [number] (pp. 70–78)", with the member's
  own number. Recorded notes in the file:
  M048, M050, M052, M060, and M147 each carry
  "Allograph of Parpola 47 in the
  programme's Mahadevan–Parpola crosswalk";
  M047 and M145 carry no note.
- **What the asset does not carry.** No
  member carries a Wells/ICIT identity:
  `sign_key` is keyed to Spec 044's pinned
  layer, and the Mahadevan and Parpola
  numbers are locators, never membership
  criteria (Spec 044 §4.2). The Wells/ICIT
  identity of each member is therefore a
  substantive act of this spec — the
  concordance act of gate 0.3 — not a field
  read off the asset.
- **Join rule for this spec.** A member
  enters this spec's counting only through
  its gate-0.3 ICIT identity. The asset
  itself is not edited to make the join
  easier, and no member is added, removed,
  or replaced under this spec in any case.

## 5. The test

### 5.1 Populations (P-F1 S4 grade discipline, applied)

- **Primary population — documented-lineage
  rows only.** 3,212 rows, 3,045 analyzable
  (audit counts; the step-0 census of gate
  0.1 governs over these figures if they
  differ, and any difference closes gate
  0.1). Positional statistics are computed
  on this population, because the
  corroborated stratum is systematically
  different material — 45.1% incomplete
  against 6.7% of documented rows, 45.2%
  carrying a `000` placeholder against
  7.3%, shorter on average (mean 3.13 signs
  against 3.79) — so including it changes
  the population, not just the sample size
  (provenance audit §2; readiness §3
  preamble).
- **Sensitivity population —
  documented-lineage + undocumented-corroborated
  rows.** 5,299 rows, 5,131 analyzable. The
  sensitivity run of §5.4 is **mandatory**,
  not optional: the whole test (classes,
  census, per-member fractions) is computed
  again on this population and reported
  beside the primary with the same
  prominence.
- **Excluded, always.** Rows graded
  undocumented-uncorroborated (405) enter
  no count, statistic, or argument. Rows
  that are entirely `000` (168, of which
  167 are graded documented-lineage) enter
  no sign analysis. The `000` placeholder
  is not a sign: it forms no bigram, holds
  no position class, and is never a
  follower.
- Sequences are counted **as stored** in
  the pinned corpus file, in stored order,
  with no direction normalisation — the
  form in which gate 0.1's census and the
  audit's grade definitions reproduce.
  (The audit's variant table shows what
  normalisation does to the intake
  reproduction; a normalised count would
  be a different measure, and is not run
  under this spec. The freeze confirms
  this reading, OPEN-072-3.)

### 5.2 The measure — the T2.4 analogue, with its carried method labelled

For every identified member, in each
population separately:

**Positional classes (carried method).**
The classes a follower can belong to are
computed on the population in question
under the Phase-43 battery's rules, as
recovered in Item 2 §2 and **carried here
as method, labelled carried**: for each
sequence of length ≥ 2 (true signs; `000`
excluded), each sign occurrence is counted
once — position 0 → initial (I); last
position → terminal (T); any position
between → medial (M); per sign,
`total` = I + M + T and `t_rate`,
`i_rate`, `m_rate` are the shares; a sign
enters classification only if
`total ≥ 5`; classes are assigned by the
cascade, first match wins —
`t_rate ≥ 0.60` TERMINAL_STRONG;
`i_rate ≥ 0.55` INITIAL_STRONG;
`m_rate ≥ 0.65` MEDIAL_STRONG;
`t_rate ≥ 0.40` TERMINAL_MODERATE;
`i_rate ≥ 0.40` INITIAL_MODERATE;
otherwise MIXED. No chance-baseline step
is added: the Phase-43 battery had none
(Item 2 §2), and adding one would be a new
element, not a carried one.

**Ending-follower fraction (the
T2.4-analogue).** Item 2 §2 states the
Phase-43 measure in one sentence:
`terminal_frac` is the share of the sign's
any-position bigrams whose second sign is
TERMINAL_STRONG or TERMINAL_MODERATE.
This design states that sentence
operationally, as its analogue definition:
for a member *s*, take every occurrence of
*s* that is followed by another true sign
in the same inscription (that is, every
bigram, at any position, whose first sign
is *s*); the fraction is the share of
those bigrams whose second sign is
classified TERMINAL_STRONG or
TERMINAL_MODERATE on the same population.
An occurrence in final position forms no
such bigram and enters neither the
numerator nor the denominator; the
member's `total` is its full occurrence
count in the population. (This denominator
reading is the draft's stated reading of
Item 2's sentence — the only reading under
which the share is a property of the sign —
recorded openly in adjudication §6,
defect 1, and put to the freeze for
confirmation, OPEN-072-3.)

**Carried floors (carried method).** From
Item 2 §2's T2.4 floors, carried and
labelled: a member is **scanned** iff its
`total ≥ 10`; the carried descriptive label
**supported** applies iff
`terminal_frac > 0.15` **and**
`total ≥ 20` (the supported floor). The
carried label is reported for every
scanned member in both populations,
exactly as the carried method states it.
It is a descriptive label carried with the
method — **it is not this spec's verdict**:
the member criterion that decides the
family verdict is the freeze-fixed line L
of §5.3, and no output may present the
carried label as a verdict under this spec
(adjudication §6, defect 2, records why
the two are kept separate).

**Reporting per member, per population:**
total occurrences; bigrams counted
(denominator); ending followers counted
(numerator); ending-follower fraction;
the carried scanned / supported labels;
and the §5.3 PASS / does-not-pass word
(primary population only for the verdict;
the sensitivity's pass words are reported
beside it under §5.4).

### 5.3 The verdict line — derived on this record, never inherited

**What is excluded, expressly.** The
Phase-43 reference points (25.9% for sign
72; 3.8% for sign 267) and Spec 048's 20%
member bar are **not inputs** to this
spec's verdict line, in any form: not as
the line, not as anchors the line is
fitted between, not as a check the line
must pass. They belong to a different
corpus in a different numbering, and the
readiness assessment is explicit that a
Shakti line must be derived on the record,
not inherited from them. **This draft
therefore fixes no numeric verdict line.**
A draft that set one would fail its own
fence.

**The reference distribution.** At the
freeze act — before execution, and before
any fish member is scored under this spec
in any population — the freeze produces a
**reference-distribution record**: the
ending-follower fraction (§5.2's
definition) of every **non-fish** sign in
the primary population that clears the
carried supported floor (`total ≥ 20`;
fish signs are the Asset F members as
identified at a freeze-stage concordance
exhibited in that record, on the basis the
freeze confirms). The record states its
population, its sign count, every
sign's fraction, and its own pin. It is a
measurement of how ordinary signs behave
on this corpus — the background the fish
family is judged against — and it is
produced from non-members only, so no
member's behaviour can move the line it
will be judged by.

**The derivation rule (fixed by this
draft; applied by the freeze).** The
verdict line **L** is the **95th
percentile** of the reference distribution,
taken by the nearest-rank method (the
smallest recorded fraction such that at
least 95% of reference signs sit at or
below it), stated in the freeze record to
three decimal places, rounding the
percentile value **up** at the fourth
decimal place so the recorded line is
never below the computed percentile. A
member **PASSES** iff its primary-population
ending-follower fraction is **at or above
L** and it clears the carried supported
floor (`total ≥ 20`).

**Freeze failure, pre-written.** If the
reference population holds fewer than
**30 signs**, or the distribution is
degenerate for this rule (its 95th
percentile is 0 or 1), the freeze does not
happen: the member is reported as a freeze
failure, **VERDICT LINE NOT DERIVABLE**,
and no fallback line — inherited,
borrowed, or rounded from the carried
0.15 label — may be substituted. The
30-sign floor and the degeneracy rule are
this draft's stated conditions on the
rule, put to the freeze with it
(OPEN-072-1).

**What the freeze fixes, then.** The
numeric value of L, the reference record's
pin, and confirmation of this rule (or an
openly stated replacement rule, applied
the same way — from the reference
distribution, before any member is
scored, with its numeric result recorded
in the freeze record). Those are
OPEN-072-1, the first freeze item. An
execution whose freeze record carries no
L closes at gate 0.5 as INVALID.

### 5.4 The sensitivity, and the grade-flip rule

The mandatory sensitivity (§5.1) recomputes
everything on the
documented + corroborated population:
classes, census, per-member fractions,
carried labels, and pass words against the
**same** freeze-fixed L (the line is not
re-derived per population; a second line
would make the two runs two different
tests).

**A grade-flip is a finding, not a
nuisance.** If a member's status changes
between the two populations — its carried
supported / not-supported label flips, or
its PASS / does-not-pass word flips — that
flip is reported as a finding, in the
outcome record's first section and in the
headline block, naming the member, both
populations' fractions and totals, and the
direction of the flip. The family's
short and damaged texts sit
disproportionately in the corroborated
stratum (audit §2), so a flip is
information about the family, not noise
about the grades. If the **family verdict
itself** differs between populations, the
headline outcome is the primary
population's verdict, stated with the
**GRADE-SENSITIVE** flag in §6's wording,
both verdicts reported, neither
suppressed (P-F1 S4's own rule for a
result that changes between the two
populations; the draft's reading of how
it applies to the headline is DD-072-6,
put to the freeze as OPEN-072-6).

## 6. Criteria, outcome set, and pre-written verdict wordings

**Family rule (fixed in advance, subject
to OPEN-072-5's freeze confirmation).**
Over the tested members (identified at
gate 0.3, clearing the carried supported
floor in the primary population), let the
passing members' share **w** be the
token-weighted share of the tested
members' primary-population occurrences
they carry.

- **FAMILY SUPPORTED** — **w > 50%**, and
  the coverage condition below does not
  fire.
- **FAMILY NOT SUPPORTED** — **w < 50%**,
  and the coverage condition below does
  not fire.
- **INCONCLUSIVE** — **w is exactly 50%**,
  **or** the coverage condition fires:
  members that are UNIDENTIFIED IN ICIT,
  NOT SCANNED, or SCANNED — BELOW
  SUPPORTED FLOOR together carry **more**
  of the identified family's total
  primary-population occurrences than the
  tested members do — in plain words, most
  of the family's occurrences were never
  tested, so a majority verdict either way
  would be a verdict about the minority.

The sensitivity population produces its
own w and its own family word under the
same rule and the same L; it flags the
headline GRADE-SENSITIVE as §5.4 states,
and never replaces the primary's word.

The execution ends in exactly one headline
outcome. The outcome record's headline
paragraph uses one of these forms, with
the bracketed quantities filled from the
run, and is preceded in the headline block
by the P-F1 S3 lineage statement (§9).
These wordings are written before any data
is touched; no other headline wording may
be used.

- **FAMILY SUPPORTED:** "Tested sign by
  sign across the fish family fixed in
  advance by Asset F (digest [d]), in ICIT
  numbering on the Shakti corpus
  (documented-lineage rows only), members
  carrying [w]% of the family's tested
  occurrences pass the freeze-fixed
  ending-follower criterion (line L =
  [L], derived at the freeze from the
  reference distribution of [n] non-fish
  signs on this corpus): [per-member
  fractions]. The family behaves, in its
  token-weighted majority, the way the
  'meen' reading predicts. [Grade sentence:
  either 'The documented + corroborated
  sensitivity returns the same family
  verdict' or 'GRADE-SENSITIVE: the
  documented + corroborated sensitivity
  returns [word] — see the grade-flip
  findings in the first section.'] This
  does not establish that any fish sign
  was pronounced 'meen': positional
  behaviour is a necessary shadow of the
  reading, not the reading."
- **FAMILY NOT SUPPORTED:** "Tested sign by
  sign across the fish family fixed in
  advance by Asset F (digest [d]), in ICIT
  numbering on the Shakti corpus
  (documented-lineage rows only), members
  carrying only [w]% of the family's
  tested occurrences pass the freeze-fixed
  ending-follower criterion (line L =
  [L]): [per-member fractions]. The
  family's token-weighted majority is not
  followed by text-ending behaviour at the
  rate the freeze-fixed line requires, and
  the claim
  `parpola_2010_dravidian_solution_manual_002`
  is recorded as not supported as a family
  claim **on this corpus**. [Grade
  sentence, as above.] This does not
  establish what any fish sign meant or
  was pronounced, and it is not a verdict
  on the Phase-43 or Spec 048 records,
  which stand exactly as recorded."
- **INCONCLUSIVE:** "Tested sign by sign
  across the fish family fixed in advance
  by Asset F (digest [d]), in ICIT
  numbering on the Shakti corpus, the
  result is inconclusive: [the passing
  members carry exactly 50% of tested
  occurrences / the coverage condition
  fired — untested members carry [u]% of
  the identified family's occurrences,
  more than the tested members' [t]%].
  [Per-member fractions and dispositions,
  both populations.] The claim stands
  exactly as recorded — partially
  supported, family split unresolved."
- **TOO THIN (step-0 closure, gate 0.4):**
  "Spec 072 closed at step 0, gate 0.4: no
  identified Asset F member clears the
  carried supported floor (total ≥ 20) in
  the primary population ([census]). No
  ending-follower fraction was computed.
  This closure is a statement about
  runnability on this corpus, not about
  the claim; the claim stands exactly as
  recorded."
- **SHAKTI INTAKE NOT REPRODUCED (step-0
  closure, gate 0.1):** "Spec 072 closed
  at step 0, gate 0.1: the Shakti corpus
  as exhibited does not reproduce the
  intake record — [the corpus file's
  SHA-256 recomputes to [observed] against
  the pinned [pinned] / the row-grades
  file's SHA-256 recomputes to [observed]
  against the pinned [pinned] / the census
  does not reproduce: [observed vs
  recorded]]. No count was computed. This
  closure is a statement about the cited
  corpus's identity, not about the claim;
  the claim stands exactly as recorded."
- **ASSET F DIGEST MISMATCH (step-0
  closure, gate 0.2):** "Spec 072 closed at
  step 0, gate 0.2: Asset F as exhibited
  recomputes to digest [observed], which
  differs from the digest recorded in
  Spec 044's step-0 record and in §2 of
  this spec, [pinned]. No count was
  computed, and the asset was not rebuilt
  or substituted under this spec. This
  closure is a statement about the
  consumed asset's identity, not about
  the claim; the claim stands exactly as
  recorded."
- **ASSET F NOT AVAILABLE (step-0
  dependency closure, gate 0.2):** "Spec
  072 closed at step 0, gate 0.2: Asset
  F's canonical file does not exist in
  the execution tree. No count was
  computed. This is a dependency closure,
  not a verdict; the claim stands exactly
  as recorded."
- **CONCORDANCE FAILED (step-0 closure,
  gate 0.3):** "Spec 072 closed at step 0,
  gate 0.3: no Asset F member could be
  identified in Wells/ICIT codes on the
  stated concordance basis ([basis]), so
  there is no family in ICIT numbering to
  test. No count was computed. This
  closure is a statement about the
  concordance, not about the claim; the
  claim stands exactly as recorded."
- **INVALID (integrity closure):** "Spec
  072 closed as INVALID: [a §2 pin
  mismatched outside gates 0.1–0.2 / no
  freeze-fixed verdict line exists /
  the step-0 record does not precede the
  first count / a count was produced on
  an unidentified, unpinned, or
  uncorroborated-excluded basis / a
  product lacks the P-F1 S3 lineage
  statement]. No result is recorded under
  this spec."

## 7. Epistemic limits (binding on all outputs)

1. **The Roif gate (publication
   conditions).** No publication of this
   study's fish-family results **in any
   form** — no summary, article draft,
   status line, paper or website text, or
   public register wording — without
   **both**: (i) citation of Roif 2025a
   (Academia.edu doc 129921039) and Roif
   2025b (Academia.edu doc 143222807), the
   published statements of the fish-sign
   model this study's question stands on;
   and (ii) **the owner's clearance of
   the specific publication act**. Records
   under this spec are internal until both
   conditions are met for the specific
   act. Campaign reporting names this
   member only as "executed — held under
   the Roif gate", without result content.
   The gate binds **regardless of
   outcome** — supported, not supported,
   inconclusive, or closed at step 0 —
   and it is carried here in substance
   from Spec 048's claim F048-C14 hold,
   which the corpus change does not touch
   (readiness §1.5, under Spec 048).
2. **No pronunciation conclusion.** Even a
   FAMILY SUPPORTED outcome does not
   establish that any fish sign was
   pronounced 'meen', the fish/star
   wordplay, or the reading of any
   inscription. Positional behaviour is a
   necessary shadow of the reading, not
   the reading, and every output carries
   that limit.
3. **No mechanism.** A family verdict
   states how the members behave on this
   corpus; it does not by itself explain
   *why* any member behaves differently
   from another, in Mahadevan numbering or
   in ICIT numbering. Any such account is
   a separate, later act, named as such.
4. **One corpus, one tradition.** Every
   result under this spec is a result on
   the Shakti corpus, an ICIT-lineage
   corpus (P-F1 S3, §9). It is not a
   reproduction of, a confirmation of, or
   a correction to any Phase-43, V3-corpus,
   or Spec 048 quantity, and no output
   may describe it as an independent check
   on the program's ICIT-lineage layer —
   agreement within one tradition is
   consistency, not corroboration.
5. **Spec 048 stands.** Nothing under this
   spec edits, reopens, or re-states Spec
   048's frozen contract, its gate 0.3, or
   its closure. A FAMILY SUPPORTED or
   FAMILY NOT SUPPORTED outcome here does
   not change Spec 048's record or the
   claim's standing except through the
   dated append §9 prescribes.
6. Negative, inconclusive, grade-flip,
   thin, and step-0-closure outcomes
   publish (internally, under limit 1)
   with the same prominence as a supported
   finding.

## 8. Controls and named confounders

- **Background behaviour of ordinary
  signs.** The freeze-stage reference
  distribution (§5.3) is the design's
  control: the fish family is judged
  against how non-fish signs on the same
  population actually behave, measured
  before any member is scored — not
  against a borrowed constant. The
  reference record travels with every
  verdict (§9).
- **Grade sensitivity.** The corroborated
  stratum is systematically shorter, more
  damaged, and more placeholder-bearing
  than the documented stratum (audit §2).
  The mandatory sensitivity and the
  grade-flip rule (§5.4) are the design's
  control; the primary population is the
  documented stratum for exactly this
  reason.
- **Family-definition discretion.**
  Removed from this spec entirely:
  membership is Asset F's, frozen by Spec
  044 before any count under this spec
  existed, and consumed by digest. The
  gate-0.3 cross-check against the claim
  record's trio and the Phase-43 six is
  reported, never acted on.
- **Concordance discretion.** The
  concordance basis is stated and pinned
  at gate 0.3, confirmed at the freeze,
  and unidentifiable members are named
  with a freeze-ruled disposition —
  never dropped or substituted. A
  concordance chosen after fractions were
  seen would be a fitted family; the gate
  order exists to refuse that.
- **Frequency.** Carried floors with exact
  counts beside every fraction, and token
  weighting stated wherever a family
  figure is stated — one frequent member
  can neither carry nor sink the family
  silently, because its weight is printed.
- **The `000` placeholder.** Excluded from
  every count (§5.1): a placeholder is
  damage recorded, not a sign observed,
  and placeholder-rich rows are exactly
  where the two populations differ most.

## 9. Reporting obligations

Every product of an execution carries, in
its headline block, in this order:

1. **The P-F1 S3 lineage statement,
   verbatim:** "This corpus is an
   ICIT-lineage corpus. Agreement between
   it and the program's earlier
   ICIT-lineage layer is consistency
   within one tradition, not independent
   corroboration." A product without the
   statement does not cite the corpus.
2. Asset F's digest (§2 pin, as asserted
   at gate 0.2) and member count, and the
   disposition of every member:
   identified (with its ICIT code) /
   UNIDENTIFIED IN ICIT / NOT SCANNED /
   SCANNED — BELOW SUPPORTED FLOOR /
   tested, with the gate-0.3 cross-check
   and its divergences named;
3. the corpus label — the Shakti corpus as
   pinned at gate 0.1, with the intake
   record named — and the population of
   every figure (documented-lineage only,
   or documented + corroborated);
4. the verdict line L, its derivation
   rule, and the reference-distribution
   record's pin and population;
5. per tested member, per population:
   total occurrences, bigrams counted,
   ending followers counted,
   ending-follower fraction, the carried
   scanned / supported labels, and the
   PASS / does-not-pass word; the
   token-weighted family share w and the
   family word per population; every
   grade-flip, as a finding, in the first
   section;
6. the headline outcome word of §6, in
   §6's pre-written wording;
7. the Roif-hold sentence: "This record
   is internal under the Roif gate; it is
   not a publication."

Deliverables at execution: a results JSON
(step-0 record with all pins, the Asset F
digest assertion, the concordance act with
its basis and per-member identities, the
census, the per-member tables for both
populations, the grade-flip findings), a
report under these headline rules, the
experiment-graph node (H15/H23, registered
and verified before the run), the outcome
append in this directory, and the LEDGER
entry (H1). Foundation check (H21) after
the execution phase: 0 failures, or the
outcome record says why not.

## 10. Stop conditions and outcome classes

Execution ends in exactly one of:

- **FAMILY SUPPORTED**, **FAMILY NOT
  SUPPORTED**, or **INCONCLUSIVE** — per
  §6, after all gates pass.
- **TOO THIN** — gate 0.4 (no identified
  member clears the carried supported
  floor in the primary population).
- **SHAKTI INTAKE NOT REPRODUCED** —
  gate 0.1.
- **ASSET F DIGEST MISMATCH** or **ASSET
  F NOT AVAILABLE** — gate 0.2.
- **CONCORDANCE FAILED** — gate 0.3 (no
  member identifiable in ICIT codes).
- **INVALID** — a §2 pin mismatches
  outside gates 0.1–0.2, no freeze-fixed
  verdict line exists, or any count is
  shown to precede its gate or to rest on
  an unidentified, unpinned, or
  excluded-grade basis.

## 11. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) —
   script, graph node, registration,
   verification.
2. **Step 0** (§3) — intake assertion
   (S1/S2); Asset F digest assertion;
   concordance act; positional classes and
   census; verdict-line assertion.
3. **Primary run** (§5) — per-member
   T2.4-analogue fractions on the
   documented-lineage population; family
   share and word under §6.
4. **Sensitivity** (§5.4) — the whole test
   on the documented + corroborated
   population; grade-flips recorded as
   findings.
5. **Outcome** (§9) — appended records
   only; the claim's record gains its
   dated append (family verdict or
   closure) — under the Roif gate, as an
   internal record.

## 12. What this spec is not

Not an amendment, reopening, or re-run of
Spec 048 (its gate 0.3 stands unamended
and its closure stands); not a build or
re-derivation of Asset F (that was Spec
044's step 0, and this spec consumes the
asset by digest only); not a reproduction
of any Phase-43 quantity (the corpus,
numbering, and calibration are all new,
and the reference points are expressly
excluded as inputs); not a test of what
any fish sign meant or was pronounced;
not an independent-corpus check (the
Shakti corpus is ICIT-lineage, §7 limit
4); and not an authorisation to execute,
to register, or to publish anything. It
is the Spec 048 question asked as a new
design on the corpus the program now
holds in ICIT numbering — designed so
that its honest outcomes, including
closing at its own step 0 on the intake,
the asset, or the concordance, are
written down before any sign is counted.

---

*AI disclosure: executed by an AI agent
(Muse, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
