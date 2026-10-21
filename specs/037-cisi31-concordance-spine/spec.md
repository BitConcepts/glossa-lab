# Spec 037 — CISI 3.1 Concordance Spine and HARP Provenance Annex: Verifying the String Matches Before Anything Is Joined

> ## FROZEN — 2026-10-20
>
> Drafted under the owner's order of 2026-10-20 to
> move the CISI follow-on uses forward, and frozen
> the same day under the owner's standing pipeline
> authorisation (freeze order 038, then 037, then
> 039, then 040), both recorded in `adjudication.md`
> (§§1, 4). Execution is **Phase-402**, run under
> this frozen contract after the freeze merged. The
> draft's provisional phase number was Phase-401;
> the allocation at freeze is Phase-402 — Phase-400
> was Spec 036's execution phase and Phase-401
> Spec 038's (DD-037-8). The study's subject
> material is **restricted** (the Phase-130 gate,
> §2): the drafting read only the intake record and
> the gate record, touched no portion data beyond
> the byte-level verifications recorded in
> `adjudication.md` §2, built no join, and
> extracted nothing.

## 1. Purpose — and the fences, stated first

The CISI Vol. 3.1 "Basic data" portion copy
(printed pp. 413–443) was received by interlibrary
loan and intaken on 2026-10-20 under the Phase-130
license gate. The intake extracted 2,123 records
(2,101 distinct catalogue numbers) and found, among
other things, **693 exact-string matches** between
the portion's catalogue numbers and object ids in
the programme's `corpus_master` — and stated, in
the same breath, that those are string matches
against a mixed-provenance compilation, **not
verified same-object joins**. This spec designs
the study that finds out how many of them are
true joins, builds the verified concordance spine
locally, and describes the Harappa HARP provenance
structure the portion carries. The fences govern
everything below, and any product of this study
that breaches one defeats the claims register
(§10):

- **Restricted material.** The portion is an
  ILL-supplied copy held for the owner's own study
  (Phase-130 gate: PROVENANCE entry 22, recorded
  before any processing). Local research use,
  extraction, and publishable **derived statistics**
  are permitted. Redistribution of scans or row
  data, upload to any service, and sharing copies
  are not. Nothing derived from the portion enters
  git; every row-level product of this study lives
  in the restricted local store (§2) and only
  aggregate statistics leave it, via the outcome
  record.
- **A string match is not a same-object join.**
  Two compilations printing the same catalogue
  number string is a *candidate*, nothing more.
  The pilot test in §4 exists because the
  programme does not treat candidates as joins.
- **The concordance is a finding aid, not
  evidence about readings.** A verified join says
  that two records describe the same object. It
  says nothing about any sign, sequence, or
  reading on that object, and no output of this
  study may be cited as evidence for or against
  any decipherment claim.
- **No prediction can be scored from this
  material.** The Basic data tables carry **no
  sign transcriptions** — zero sign tokens in the
  31 pages. No PRED-2026 entry (001, 002, 003,
  010, 011, or any other) can be scored, advanced,
  or retired from this material, and this study
  computes nothing that feeds a verdict without
  its own frozen study (§6).

## 2. The material and the gate

**The portion.** *Corpus of Indus Seals and
Inscriptions*, Vol. 3, Part 1 (Mohenjo-daro and
Harappa), eds. Parpola, Pande & Koskikallio,
Helsinki 2010, ISBN 978-951-41-1040-5 — the
section "Basic data for the objects illustrated",
printed pp. 413–443, delivered 2026-10-14 by
Oakland University ILL (lender: University of
Missouri–Kansas City), as one PDF:
`376929.pdf`, 8,206,446 bytes, SHA-256
`514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a`
(verified against the delivered bytes at intake
and again at this draft; `adjudication.md` §2).

**The gate.** Phase-130 intake gate, recorded
2026-10-20 in the restricted store's provenance
record (entry 22) **before any processing**:
classification *restricted research material*;
permitted — local use, OCR/table extraction,
publishable derived statistics, citation of facts;
not permitted — redistribution of scans or page
images, upload to the repo/Zenodo/OSF/any service,
sharing copies, bulk reproduction beyond the
portion; ambiguous uses wait for an owner ruling.
The in-repo gate pack is `specs/021-phase130-intake-pack/`;
the intake report (restricted store, research
notes) is the census of record for this design.

**The extracted table (local only).** In the
portion folder of the restricted store
(`downloads/oakland-ill-cisi31-portion/`, beside
the scan): `cisi31-basic-data.csv` — 2,123 records
× 26 columns, parse-validated at intake; 2,029
rows from the PDF text layer + 94 visually
transcribed (`row_source` separates them);
per-cell confidence and per-row provenance grades
carried. Census, as found at intake and never
adjusted: **2,123 records; 2,101 distinct
catalogue numbers**; Mohenjo-daro 519 records,
Harappa old excavations 510, Harappa HARP 1,094;
plus the colour-photo index (119 entries), which
this study does not use. The printed table
columns are: (1) CISI number, (2) FC number,
(3) excavation number/data, (4) museum/owner +
registration number(s), (5) photo sources/remarks;
object type and motif come from the plate-section
headings interleaved through the tables. HARP rows
carry, by the section's own conventions: dig year
+ accession as the excavation number (e.g.
H98-3503), excavation unit (lot) + object record
number, and a period code (1A = Period 1
sub-period A; 1/2 = mixed Periods 1–2; M =
unspecified mixed context; S = surface; bracketed
codes are typological ascriptions).

**Completeness, as found.** Every number in every
page's stated range is accounted for **except
H-1019**, absent from the portion (a
header/section discrepancy in the source, recorded
at intake). Fourteen numbers carry more than one
record (genuine multiple plate listings); two
pairs (H-2243, H-2245) carry different data under
one number — both records retained, as found.
The portion covers the ranges M-1660–M-2134 and
H-1020–H-2590 plus addenda — a slice of the
volume, not Vol. 3.1.

## 3. The two workstreams

- **Workstream A (§4) — the concordance spine.**
  Verify the 693 string-match candidates as
  same-object joins under a fixed field-agreement
  ladder (the pilot test); build the spine from
  the verified joins as a **local** table in the
  restricted store; report aggregate statistics
  only.
- **Workstream B (§5) — the HARP provenance
  annex.** A descriptive extraction of the HARP
  rows' provenance structure (dig year, lot,
  period codes) from the same local table, with
  its limits stated. Descriptive only; no joins,
  no verdicts.

Both workstreams are execution-gated: the draft
ran neither. Workstream B runs inside Phase-402,
gated on step 0 only (DD-037-6, decided at the
freeze, `adjudication.md` §4).

## 4. Workstream A — the pilot test and the spine

### 4.1 Key inventory

Portion side (per record, from the printed
columns): **CISI number** (the candidate key);
**FC number** (1,028 of 1,029 family-A records at
intake); **excavation number/data** (1,527
records); **museum/owner + registration number**
(1,029 family-A records); section (Mohenjo-daro /
Harappa old / Harappa HARP); plate-section heading
(the object-type source); per-cell confidence and
row provenance grade.

Programme side: `corpus_master`
(`data/normalized/corpus_master.csv` on `main`,
SHA-256
`b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`)
— 2,722 rows from two sources (the mayig CISI
digitisation, 179 rows; the Yajnadevam corpus,
2,543 rows), carrying `source_object_id` (the
string the intake matched), `site`,
`artifact_type`, `source_name`. Corroboration
side: the programme's other in-hand object records
carrying FC, excavation, or museum keys for the
same CISI number (the Vol. 1/2 catalogue
extractions of the Phase-124 work, in the
restricted store). **Holdat `cisi_number` remains
prohibited as a join key** (the standing rule
from the Spec 034 freeze); nothing in this study
uses it.

### 4.2 Candidate generation (fixed)

The candidate set is the intake's **693
exact-string matches** between the portion's
distinct catalogue numbers and `corpus_master`
`source_object_id` values (M 289 / EH 102 /
HARP 302 by portion section, as counted at
intake). One candidate per (portion record ×
matched corpus row): where a number carries
multiple portion records (14 numbers) or matches
multiple corpus rows, each pairing is its own
candidate row and is graded separately. No
fuzzy matching, no normalisation beyond the
fixed rules of §4.3, no additional candidates:
a number that string-matches nothing is not in
the pilot, and the pilot says nothing about it.

### 4.3 The verification ladder (fixed; the pilot test)

Each candidate is graded by the following ladder,
in this order. The ladder is the test: it is
fixed here so execution has no discretion, and
it is applied to **all 693** candidates (a
census, not a sample — DD-037-2).

1. **Site agreement (mandatory).** Portion section
   maps to site by the fixed mapping
   (Mohenjo-daro → Mohenjo-daro; Harappa old and
   Harappa HARP → Harappa) and must equal the
   corpus row's `site`. Disagreement = CONFLICT
   (reason SITE).
2. **Object-type agreement (mandatory where
   graded).** Both sides are reduced to a class by
   fixed keyword rules over a closed class set
   {seal, seal impression, tablet, graffiti,
   ivory stick, stone object, other}: portion side
   from the plate-section heading (the intake's
   heading classes), corpus side from
   `artifact_type`. **A seal and a seal impression
   are different classes** — an impression is not
   the seal. Where both sides yield a class, they
   must be equal; disagreement = CONFLICT (reason
   TYPE). Where either side yields no class, the
   field is UNGRADED for that candidate — not a
   pass, not a conflict.
3. **Corroborating keys (where available).** For
   each of {FC number, excavation number,
   museum/registration} where **both** the portion
   record and an in-hand corroboration record
   (§4.1) carry a value for the same CISI number,
   compare under a fixed normalisation (case-,
   whitespace-, and punctuation-insensitive token
   equality; no expansion of abbreviations, no
   guessing at garbled tokens — a low-confidence
   portion cell is UNGRADED, never repaired into
   a value). Agreement corroborates; contradiction
   = CONFLICT (reason CORROB-FC / CORROB-EXC /
   CORROB-MUS). Where no corroboration record
   exists, the key is UNGRADED.
4. **Number-level ambiguity.** If the portion
   itself carries two records under one number
   with differing join-relevant data (the H-2243 /
   H-2245 pattern), every candidate for that
   number is barred from VERIFIED: outcome
   CONFLICT (reason NUMBER-AMBIGUOUS). The
   ambiguity is a fact about the printed record
   and is reported, never resolved by picking a
   record.

**Outcome classes (exactly three).** **VERIFIED**
— site agrees, type graded and agrees, no
corroborating contradiction, number not
ambiguous. **CONFLICT** — any ladder conflict,
with its reason code(s). **UNRESOLVED** — site
agrees but the candidate cannot reach VERIFIED
(type ungraded, or grading blocked by
low-confidence cells) and no conflict fired.
UNRESOLVED is its own class in every report; it
is never rounded into VERIFIED, and a spine
built from VERIFIED joins carries unresolved
candidates as flagged rows only if §4.5 says so —
it does not: the spine contains VERIFIED joins
only, and UNRESOLVED candidates are reported in
aggregate and listed in the local build record,
not joined.

### 4.4 Quantities reported (publishable aggregates)

Computed over the full candidate census, and
reported overall, by portion section
(Mohenjo-daro / Harappa old / Harappa HARP), and
by corpus source (`source_name`): candidate
count; VERIFIED / CONFLICT / UNRESOLVED counts
and shares; conflict breakdown by reason code;
per-field graded bases (how many candidates each
ladder field could grade). Plus the hand-check
stratum result (§4.6) and the spine coverage
(§4.5): verified joins by section; catalogue
numbers of the portion's 2,101 that end with at
least one verified join; field-fill of the spine
(FC / excavation / museum present per join).
These aggregates, and only these, are the
publishable product of Workstream A. The rates
describe **this portion's ranges only** (§2);
they are not rates for Vol. 3.1 as a whole, for
CISI as a whole, or for any other compilation.

### 4.5 The spine (local output)

If the pilot completes and the halt rule (§4.7)
does not fire, execution writes
`cisi31-concordance-spine.csv` **in the portion
folder of the restricted store, beside the
scan** — one row per VERIFIED join, carrying the
portion's keys (CISI, FC, excavation, museum,
registration, printed page, provenance grade) and
the corpus side's identifiers (`source_object_id`,
`source_name`), plus the ladder grades that
verified it. The file is a derived row-level
product of restricted material: it never enters
git, is never uploaded anywhere, and is named in
the outcome record by filename and row count
only — its contents are reported exclusively
through the §4.4 aggregates. Execution step 0
(§7) includes a repo-cleanliness check that no
portion-derived file is present in the
repository tree or index, run before any join
work and again before the outcome record is
committed.

### 4.6 The hand-check stratum (fixed design, size a freeze proposal)

A seeded random sample of graded candidates,
stratified across the three outcome classes, is
hand-checked at execution against the portion's
page renders and the programme records, and each
sampled CONFLICT is classified by cause:
(i) extraction error in the intake table,
(ii) extraction/record error on the programme
side, (iii) genuine compilation divergence (both
sides as printed, disagreeing), (iv) true
non-identity (the string match joins different
objects). The stratum's purpose is to separate
*our* noise from *the record's* disagreement
before anyone reads the conflict rate as a fact
about the compilations; its class-split counts
are reported as aggregates alongside §4.4. The
stratum size and seed handling are fixed at
freeze (DD-037-5; draft proposal: 60 candidates —
30 VERIFIED / 15 CONFLICT / 15 UNRESOLVED, or the
whole class where a class is smaller — seed
recorded in the execution record before sampling).

### 4.7 Failure handling and the halt rule

Conflicts are **recorded, never repaired**:
neither side's data is edited under this study,
no candidate is force-matched, and no ladder step
is re-run under a friendlier reading. If the
CONFLICT share of all 693 candidates exceeds
**20%**, the spine build **halts**: the pilot
still completes and is reported in full, no spine
file is written, and the outcome is recorded as
PILOT COMPLETE — SPINE HALTED, with the conflict
breakdown as the finding (the string-match key is
not trustworthy at scale for these ranges). The
20% value is a draft-fixed reading the freeze
confirms or changes openly (DD-037-4); it is not
chosen at execution, with the rate visible.

## 5. Workstream B — the HARP provenance annex (descriptive)

From the same local table, the HARP section's
1,094 records carry provenance structure at a
scale the programme has not previously held
(the chronology work previously had ~120
other-site determinations plus the Law (2011)
extractions to work with). The annex extracts,
descriptively and in aggregate: the dig-year
distribution (excavation-number years, 1986–2001
at intake; bulk 1990–1999); lot/record-number
structure and fill (754 of 1,094 at intake); the
period-code inventory — every distinct code with
its count, bracketed (typological-ascription)
codes separated from unbracketed, mixed codes
(1/2, M, S) as their own classes — and the
period fill **with its caveat attached wherever
the number appears**: the intake's period fill
(656 of 1,094) is a **floor**, because the scan's
text layer loses split period tokens; execution
recomputes from the pinned local table and
reports the fill as found, floor caveat intact,
and does not silently repair it. Museum/owner
values are reported only as aggregate field-fill
inside §4.4's coverage (they are join keys in
Workstream A); the annex makes no
museum-location claims beyond *as printed in
2010* (F037-C14).

**Limits, stated in the annex itself.** The annex
is descriptive: it characterises what the printed
HARP table records, nothing more. It does **not**
change the Spec 031 (Q7) record — that study
closed at its margins step with in-universe link
mass of 2 sites / 1 pair, bead/craft arm
NOT-YET-TESTABLE and ceramic arm NOT ESTIMABLE —
because Harappa-internal provenance structure is
not cross-site link mass, and no quantity in this
annex is a link. It feeds no verdict, no
chronology claim, and no prediction; any study
that would use this structure as evidence needs
its own spec and freeze. Period codes are as
printed in 2010, including the volume's own
typological ascriptions, and are not re-derived
under this study.

## 6. What this study would and would not establish

**Would.** How many of the 693 string matches are
verified same-object joins, under a ladder fixed
before the joins were examined — a number the
programme currently does not have for any CISI
3.1 range; a local concordance spine for the
portion's ranges (M-1660–2134, H-1020–2590, plus
addenda) carrying the FC / excavation / museum
keys the programme has lacked for these objects,
incl. keys for numbers among the 1,394 new to the
programme where they verify; and a descriptive
map of the HARP provenance structure. Either
pilot outcome is a finding: a high verified rate
makes the spine a reliable finding aid; a high
conflict rate is a fact about the compilations'
agreement in these ranges, reported as found.

**Would not.** Anything about signs, sequences,
or readings (the material has none); any PRED
score or readiness change; any statement about
objects outside the portion's ranges; any
correction to either compilation (conflicts are
reported, not resolved); any change to the Q7
record; anything publishable beyond the aggregate
statistics named in §§4.4–5.

## 7. Execution shape (Phase-402)

1. **Graph-first build** (H15/H23): experiment
   script, graph module, registration in the
   experiment graph, then run.
2. **Step 0 — gate and integrity, fail-closed, in
   this order:** (0.1) the Phase-130 gate is on
   record (PROVENANCE entry 22) and names this
   material restricted; (0.2) the portion PDF
   SHA-256 equals `514338b1…` and the local table
   parse-validates at 2,123 records × 26 columns
   with its intake hash recorded; (0.3)
   `corpus_master` on the execution tree hashes
   to `b19cfe95…`; (0.4) repo cleanliness — no
   portion-derived file in the tree or index.
   Any failure stops the execution as itself,
   before any join is computed.
3. **Pilot** (§4): candidate generation, ladder
   grading, hand-check stratum, aggregates.
4. **Spine build** (§4.5) unless the halt rule
   (§4.7) fires; **annex** (§5) per the freeze's
   DD-037-6 decision.
5. **Outcome:** aggregates and the outcome
   classes recorded in this spec's `outcome.md`,
   the root LEDGER, and the local build record
   (restricted store). No PRED-register entry is
   created or changed; no anchor changes; the
   foundation check is not a gate here because no
   claim consequence lands on the anchors or the
   register — stated openly rather than implied.

## 8. What this spec does not do

- It executes nothing and freezes nothing. Both
  are separate owner orders.
- It touches no portion data at draft beyond the
  byte-level verifications in `adjudication.md`
  §2, computes no join, and extracts nothing new.
- It puts nothing derived from the portion into
  git or any public surface — including in this
  draft, which cites only aggregates already in
  the intake record.
- It scores no prediction and reopens no closed
  line: not Q7 (Spec 031), not the
  keyed-transcription line, not any PRED.
- It edits neither compilation's data, resolves
  no conflict, and contacts no library or lender.
- It does not use the colour-photo index, the
  Proto-Indica portion (not arrived; it enters
  under the same gate when it does), or any
  material outside the received portion.

## 9. Governed claims (summary)

The governed register is `claims.json`
(F037-C01…C15):

- **C01** — outcome statements under this spec
  concern only join verification and descriptive
  provenance structure for the portion's ranges.
- **C02** — a string match is a candidate, never
  a join; the pilot exists to test candidates.
- **C03** — a join is VERIFIED only under the
  fixed ladder of §4.3, applied to all 693
  candidates.
- **C04** — conflicts are recorded with reason
  codes, never repaired; number-level ambiguous
  numbers cannot verify.
- **C05** — the halt rule: a conflict share
  above 20% of all candidates halts the spine
  build; the pilot still reports in full.
- **C06** — the concordance is a finding aid;
  it is not evidence about readings.
- **C07** — no PRED-2026 entry can be scored
  from this material; it carries no sign
  transcriptions.
- **C08** — the license gate governs every
  product: row-level derivatives stay in the
  restricted local store; only aggregate
  statistics are publishable; nothing
  portion-derived enters git.
- **C09** — execution step 0 re-verifies the
  gate, the pinned inputs, and repo cleanliness
  before any join work, fail-closed.
- **C10** — the pilot is a census of all 693
  candidates; the hand-check stratum estimates
  the extraction-error share of conflicts.
- **C11** — the reported quantities are exactly
  the pre-registered aggregates of §4.4, by
  section and by corpus source; UNRESOLVED is
  always its own class.
- **C12** — the HARP annex is descriptive:
  code inventories and distributions as printed,
  with the period-fill floor caveat attached.
- **C13** — the annex does not change the Q7
  link-mass finding and feeds no verdict
  without its own frozen study.
- **C14** — museum/owner data are as printed in
  2010: a dated snapshot, not current locations.
- **C15** — the spine's coverage is the
  portion's ranges only; no whole-volume or
  whole-corpus claim is made.

## 10. Design decisions

- **DD-037-1 — Step 0 fails closed, in a fixed
  order.** Gate, input integrity, repo
  cleanliness — each with a stated stop (§7).
  The gate check comes first because the
  material's restricted status governs every
  later act, including where outputs may live.
- **DD-037-2 — The pilot is a census, not a
  sample.** 693 candidates is tractable, and a
  sample would leave the spine's coverage —
  the study's product — undefined for the
  unexamined remainder. Sampling appears only
  in the hand-check stratum (§4.6), whose
  object is error attribution, not coverage.
- **DD-037-3 — The ladder's mandatory fields are
  site and type; corroboration grades only
  where records exist on both sides.** Site and
  object type are the two fields every candidate
  carries on both sides; FC / excavation /
  museum values are sparser, so their absence
  is UNGRADED rather than a failure — but a
  contradiction in any of them is a conflict,
  because a contradiction is positive evidence
  against identity in a way an absence is not.
- **DD-037-4 — The halt threshold is fixed at
  draft (20% of all candidates), for the freeze
  to confirm or change openly.** A threshold
  chosen at execution, with the conflict rate
  visible, would not be a rule. If the freeze
  changes the value, it changes it before any
  join is computed and the change is recorded
  here.
- **DD-037-5 — the hand-check stratum size.
  DECIDED at the freeze** (`adjudication.md`
  §4): 60 candidates (30 VERIFIED / 15 CONFLICT
  / 15 UNRESOLVED, whole class where smaller),
  seeded, the seed recorded before sampling.
  The stratification across outcome classes is
  fixed by §4.6.
- **DD-037-6 — Workstream B's placement.
  DECIDED at the freeze** (`adjudication.md`
  §4): inside Phase-402, gated on step 0 only —
  B touches no joins, adds no risk to A's
  ladder, and reads the same pinned local
  table; a separate phase would re-run the same
  step 0 for no epistemic gain.
- **DD-037-7 — a spec-level OSF registration.
  DECIDED at the freeze** (`adjudication.md`
  §4): the pattern is followed and the frozen
  spec's own OSF registration is filed at the
  freeze (`osf-spec-registration.md`), so the
  ladder and the halt rule are timestamped
  outside the repo before execution. This study
  registers no prediction and scores none.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
