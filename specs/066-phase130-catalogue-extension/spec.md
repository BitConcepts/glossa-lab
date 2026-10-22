# Spec 066 — Phase-130 Catalogue Extension: CISI Vol. 3.1 Portion Objects into the Pinned Catalogue Layer

> ## FROZEN — 2026-10-21
>
> This intake act was approved by the owner on
> 2026-10-21 as Item 7 of the amendment package of
> that date (the intake act itself, including the
> lawful line of §4), and is frozen the same day
> under that approval (`adjudication.md` §§1, 4).
> Execution is **Phase-428**, run under this frozen
> contract in the same run as the freeze, after the
> freeze merges. The authoritative draft is the
> amendment-queue Item 7 draft (research notes,
> 2026-10-21); its §4 (the lawful line) and §5
> (construction, verification ladder, stratum,
> halt rule, pinned artifacts) govern exactly, and
> this spec carries them into frozen form without
> softening any of them. The subject material is
> **restricted** (the Phase-130 gate, §2): at draft
> and freeze, no portion data beyond the byte-level
> pin verifications and the count-level derivations
> recorded in `adjudication.md` §2 was processed —
> no candidate was graded, no layer was built, and
> nothing was joined.

## 1. Purpose — and the fences, stated first

Spec 059 closed at step 0, JOIN GATE NOT MET: the
object-ID join resolved 2,899 of 5,679 lineage
rows (51.05%) against a frozen bar of ≥ 3,465
rows, because 2,119 rows carry identifiers that
resolve to zero objects in the pinned catalogue
layer (CISI vols. 1–2 merged: 7,705 rows, 3,493
distinct objects). The unblocking act named in
Spec 059's frozen outcome wording is "a more
complete published object catalogue entering
through Phase-130 intake." The programme already
holds such a source: the CISI Vol. 3.1 portion
copy intaken on 2026-10-20 under the Phase-130
gate (2,123 extracted records; 2,101 distinct
well-formed catalogue numbers). Item 7's counts,
re-derived first-hand at this draft
(`adjudication.md` §2), show that 1,293 of the
1,595 distinct zero-resolution identifiers are
numbers the portion carries (1,790 of the 2,119
zero-resolution rows), and that a further 48
portion numbers are referenced only by rows that
already joined, while 760 portion numbers are
referenced by no lineage row at all.

This spec is the intake act that turns those
numbers — lawfully, under the gate — into
catalogue objects: grade every portion number
under a fixed verification ladder, build the
merged catalogue layer v2 (vols. 1–2 plus the
verified 3.1 objects) **locally**, and commit
only the derived products the gate permits (§4).
It is a data-intake act under the Spec 021
machinery, **not a study**: it computes no join
against the merged layer, no F1 quantity, and no
verdict of any kind. The fences govern
everything below, and any product of this act
that breaches one defeats the claims register
(§10):

- **Restricted material.** The portion is an
  ILL-supplied copy held for the owner's own
  study (Phase-130 gate: PROVENANCE entry 22,
  recorded before any processing). Local research
  use, extraction, and publishable **derived
  statistics** are permitted; the owner-approved
  §4 line adds one publishable derived fact list
  (the extension index, §4 item 1). Redistribution
  of scans or page images, upload to any service,
  and sharing copies are not permitted. Every
  row-level product of this act beyond the §4
  item-1 fact list lives in the restricted local
  store (§2) and never enters git.
- **A string match is not a catalogue object.**
  A portion number appearing among the lineage
  layer's identifiers is a *candidate*, nothing
  more. The ladder of §5.3 exists because the
  programme does not treat candidates as objects,
  exactly as Spec 037 did not treat string
  matches as joins.
- **A VERIFIED catalogue object is not a
  verified join.** Grading under §5.3 verifies
  that a candidate number may lawfully and
  soundly enter the catalogue as an object. It
  does not join any lineage row to that object,
  and no output of this act may be cited as a
  join result.
- **No F1 quantity exists under this act.**
  `STUDY-SPEC-024/F1` stands exactly as recorded
  (SUPPORTED on its original joined subset),
  regardless of anything this act finds, and Spec
  059's frozen record, outcome, and closure are
  never patched. Any study use of the merged
  layer waits for a successor spec with its own
  freeze and its own OSF registration (§8).

## 2. The material and the gate

**The portion.** *Corpus of Indus Seals and
Inscriptions*, Vol. 3, Part 1 (Mohenjo-daro and
Harappa), eds. Parpola, Pande & Koskikallio,
Helsinki 2010, ISBN 978-951-41-1040-5 — the
section "Basic data for the objects illustrated",
printed pp. 413–443, delivered 2026-10-14 by
Oakland University ILL, as one PDF: `376929.pdf`,
8,206,446 bytes, SHA-256
`514338b1f6c498bd318b114e39b0e77a79a6685918a0a4c2c5b116dfc2482b6a`
(verified against the delivered bytes at intake,
at Spec 037, and again at this draft by two
routes; `adjudication.md` §2).

**The gate.** Phase-130 intake gate, recorded
2026-10-20 in the restricted store's provenance
record (entry 22) **before any processing**, in
its own words:

> - Classification: restricted research material.
>   ILL-supplied copies are made for the
>   requesting patron's own study; they are not
>   the program's to distribute, deposit, or
>   publish.
> - Permitted: local research use on this machine;
>   OCR and table extraction for analysis;
>   derived statistics, counts, and feature
>   vectors (publishable, as with all restricted
>   sources in this program); citation of facts
>   (page counts, yields, field values) in
>   program reports.
> - Not permitted: redistributing scans or page
>   images; uploading the material to the repo,
>   Zenodo, OSF, or any third-party service;
>   sharing copies with collaborators; bulk
>   reproduction beyond the received portion. Any
>   ambiguous use waits for an owner ruling.
> - The delivery carried no stricter terms, so
>   the plan's terms govern as written.

The in-repo gate pack is
`specs/021-phase130-intake-pack/`; the intake
report (restricted store, research notes) is the
census of record for this design. The owner's
approval of 2026-10-21 (Item 7) confirms the §4
reading of this gate — in particular that the
§4 item-1 fact list is a publishable derived
fact list under it. Any use beyond §4 is outside
the gate as recorded and needs its own owner
ruling; this act requests none and takes none.

**The extracted table (local only).** In the
portion folder of the restricted store
(`downloads/oakland-ill-cisi31-portion/`, beside
the scan): `cisi31-basic-data.csv` — 2,123
records × 26 columns, SHA-256
`7179858d9b2bc18b480ba092a08ea2ee021ce569fcaceb5b992d22c541d333c8`,
parse-validated at intake; 2,029 rows from the
PDF text layer + 94 visually transcribed
(`row_source` separates them); per-cell
confidence and per-row provenance grades
carried. Census, as found at intake and never
adjusted: **2,123 records; 2,101 distinct
well-formed catalogue numbers** (plus 5 garbled
low-confidence tokens that are not catalogue
numbers); Mohenjo-daro 519 records, Harappa old
excavations 510, Harappa HARP 1,094; per-cell
confidence for the catalogue-number field: high
1,933 / medium 183 / low 7 of 2,123 records. The
tables carry **no sign-by-sign transcriptions** —
object-level basic data only. H-1019 appears in
a page header range but is printed nowhere in
the portion — a source discrepancy, recorded as
found; this act fills no gap.

**The merge base (local only).** The pinned
vols. 1–2 catalogue layer, held in the local
store (gitignored) exactly as Spec 059 resolved
against it: vol. 1 CSV, 3,320 rows, 804,665
bytes, SHA-256
`e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e`;
vol. 2 CSV, 4,385 rows, 1,431,631 bytes, SHA-256
`e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9`;
merged 7,705 rows, 3,493 distinct objects, one
ID (`H-311`) in both volumes. The lineage layer
(horus84 `inscriptions.csv`, 1,190,884 bytes,
SHA-256
`c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`)
and the committed Phase-421 census and results
(SHA-256
`952829317a7b8e48e809da4353cdf5f6b6f872180920bc349aaf747595b99bb8`
and
`3948cd01f960842b963061d96ddeabd5ee0b5cdeb572d786976d476d84ff0c7f`)
are the demand side: they define which portion
numbers are referenced, and by rows of which
resolution class (§5.1).

## 3. The candidate sets (fixed)

The candidate unit is the **distinct well-formed
catalogue number**. The census is all **2,101**
such numbers in the portion, in two sets graded
identically and reported separately throughout:

- **Referenced — 1,341 numbers:** the portion
  numbers that appear as a carried identifier
  (`provenance.object_id`) in the committed
  Phase-421 census. Of these, **1,293** are
  referenced by zero-resolution rows only and
  **48** by joined rows only (the two subsets
  are disjoint; verified first-hand at draft,
  `adjudication.md` §2).
- **Unreferenced — 760 numbers:** the portion
  numbers no census row carries. They would grow
  the catalogue but move no Spec 059-class count;
  they are graded for catalogue completeness,
  under the same ladder, and reported separately
  in every table.

The 5 garbled tokens are not candidates: they
are not catalogue numbers, they enter nothing,
and no garbled token is repaired into a number
this act invents (§5.2).

## 4. The lawful line (Item 7 §4, carried exactly)

**May enter the repo (derived material):**

1. The **extension index**: the distinct
   catalogue-number list of the graded candidates
   — each number with its site section
   (Mohenjo-daro / Harappa old / Harappa HARP),
   its **object-type class as published** (the
   plate-heading determination, reduced under
   the closed class set of §5.3 rung 4, or
   "unfilled"), and its **verification grade
   class** (§5.3). Catalogue numbers are the
   volume's own published identifiers, and a list
   of identifiers with published determinations
   is a derived fact list in the gate's sense.
   No other extracted field rides along. The
   index is a census of graded candidates in
   this form; the catalogue objects that
   **enter** the merged layer are exactly its
   VERIFIED rows (§5.6).
2. All **aggregate statistics**: the censuses,
   scenario and projection tables, field-fill
   rates, conflict/verification counts and
   shares, stratum results — the Spec 037 §4.4
   form.
3. The **pins** of every restricted-local
   artifact the build consumed or produced
   (SHA-256 + byte count), asserted in this
   freeze as definition constants — the
   DD-059-9 form.

**Stays restricted-local, always:**

4. The scan and any page image or render; the
   full 26-column extraction table; the
   colour-photo index rows.
5. Every extracted **source-row field** beyond
   item 1: FC numbers, excavation numbers/data,
   museum/owner and registration numbers, photo
   sources/remarks, printed-page-level row
   linkage, per-cell confidence and per-row
   provenance detail, and any row-level grade
   table, build record, or stratum record the
   execution produces (named in the outcome by
   filename and row count only).
6. The **merged catalogue layer v2 file** in its
   full form (it carries the fields of item 5
   for vols. 1–2 objects as well as 3.1
   objects): held in the local store beside the
   existing catalogue CSVs, pinned by hash,
   never committed — exactly as the vols. 1–2
   layer is held today.

## 5. The intake act

### 5.1 Sources (all held; no acquisition)

- The restricted CISI 3.1 extraction table and
  the portion PDF behind it (pins in §2) —
  consumed locally only, under the entry-22
  gate, which step 0 re-verifies on the record
  before any grading (the Spec 037 step-0.1
  form, quoting the gate's own words).
- The pinned vols. 1–2 catalogue layer (pins in
  §2) as the merge base, and the mayig layer
  (the 179-object CISI digitisation carried in
  `corpus_master`) as a corroboration source
  where it carries values (§5.3 rung 5).
- The committed Phase-421 census (pin in §2) as
  the demand side: it defines the referenced set
  (§3) and supplies each referenced candidate's
  referencing rows and their sites. The census
  is already committed and public; this act adds
  nothing to it.

### 5.2 Construction (fixed rules)

- One catalogue object per distinct well-formed
  CISI number in the portion (2,101), keyed by
  the number; merged with the vols. 1–2 layer on
  the same key. A number already in the merged
  layer (the 48 addenda republications and any
  unreferenced duplicates the build finds) does
  **not** create a second object: the merge
  records the collision in the local build
  record and the existing object stands — no
  silent overwrite, no duplicate.
- Each new object carries, in the local merged
  layer: site (by portion section), object-type
  class from the plate heading under the §5.3
  rung-4 class set (blank/addenda heading →
  unfilled), and the portion's printed keys (FC,
  excavation, museum/registration, page) — all
  of which stay local per §4 item 5. The
  committed extension index (§4 item 1) carries
  number + site section + type class + grade
  class only.
- The 5 garbled tokens are not catalogue
  numbers: they resolve into the set at intake
  census semantics or they do not enter at all.
  No garbled token is repaired into a number the
  build invents.

### 5.3 The verification ladder (fixed; applied to every candidate)

Each candidate is graded by the following
ladder, in this order. The ladder is fixed here
so execution has no discretion, and it is
applied to **all 2,101** candidates (a census,
not a sample — DD-066-2). The first rung that
fires a CONFLICT decides the candidate's reason
code; a candidate on which no conflict fires
and whose confidence gate (§ rung 2) is passed
is VERIFIED; a candidate blocked only by the
confidence gate is UNRESOLVED.

1. **Site agreement (mandatory).** Portion
   section maps to site by the fixed Spec 037
   mapping (Mohenjo-daro → Mohenjo-daro; Harappa
   old and Harappa HARP → Harappa) and must
   agree with the referencing rows' site where
   referencing rows exist (the Phase-421 census
   rows carrying the number). Disagreement =
   CONFLICT (reason SITE). A candidate whose own
   portion records span sections mapping to
   different sites is barred under rung 3 (its
   records differ on join-relevant data), as in
   Spec 037's grading. For unreferenced
   candidates there is no referencing row; the
   rung is graded by section, and the object's
   site is its section's site.
2. **Extraction-confidence gate.** A
   catalogue-number cell graded **low** is
   UNGRADED — never repaired, never entered —
   until hand-verified against the page render:
   at execution, every low-confidence
   well-formed candidate (2 records at the
   intake census; §2) is hand-verified against
   its page render before grading completes;
   confirmed as printed, the gate passes for
   that candidate (the verification is recorded
   in the local build record); not confirmed,
   the candidate is UNRESOLVED and never
   entered. **Medium**-confidence candidates are
   graded by the ladder but their VERIFIED
   outcome is provisional until the §5.4
   stratum hand-check covers their class: the
   stratum's sampled medium-confidence
   candidates are hand-checked against the page
   renders, and if every sampled medium is sound
   as extracted, the medium class is covered and
   its provisional grades stand; if any sampled
   medium is found mis-extracted, **all**
   medium-confidence VERIFIED candidates are
   demoted to UNRESOLVED (the class is not
   covered) and the demotion is reported as an
   aggregate. High-confidence candidates pass
   the gate directly.
3. **Number-level ambiguity bar.** A number
   whose portion records differ on join-relevant
   data — the Spec 037 comparison tuple:
   section, heading type class, FC, excavation,
   museum, registration — is barred from entry
   as a catalogue object: outcome CONFLICT
   (reason NUMBER-AMBIGUOUS), both records
   retained in the local build record, never
   resolved by picking one.
4. **Type carriage (not a gate).** The type
   class is carried as published: the portion
   record's plate-section heading reduced by
   the fixed Spec 037 keyword rules over the
   closed class set {seal, seal impression,
   tablet, graffiti, ivory stick, stone object,
   other}; a blank/addenda heading yields type
   **unfilled**, which is a fact recorded, not
   a conflict and not a pass. Where a number's
   records carry more than one graded class,
   rung 3 has already fired (the class is part
   of the comparison tuple). No comparison
   against any other compilation's type
   vocabulary is a rung of this ladder — that
   comparison was Spec 037's question, against a
   different compilation, and its result stands
   as recorded for that question.
5. **Corroboration where available.** Where an
   in-hand record (vols. 1–2 layer, mayig layer)
   carries FC / excavation / museum values for
   the same number, compare under Spec 037's
   fixed normalisation (case-, whitespace-, and
   punctuation-insensitive token equality; no
   expansion of abbreviations, no guessing at
   garbled tokens); contradiction = CONFLICT
   (reason CORROB-FC / CORROB-EXC / CORROB-MUS),
   absence = UNGRADED for that key, never
   repaired or borrowed. Recorded at draft, so
   execution cannot mistake absence for
   oversight: neither the vols. 1–2 catalogue
   layer nor the mayig layer carries FC,
   excavation, or museum values for any number
   (verified first-hand at draft from the
   layers' own field inventories,
   `adjudication.md` §2), so this rung is
   UNGRADED for every candidate on the held
   records and no CORROB-* conflict can fire —
   stated here, before grading, as a property
   of the held records, not discovered after it.

**Outcome classes (exactly three).**
**VERIFIED** — site agrees, confidence gate
passed, not ambiguous, no corroboration
contradiction: the candidate enters the
catalogue (§5.6). **CONFLICT** — retained with
its reason code in the local build record,
never entered, never repaired. **UNRESOLVED**
— its own class in every report, never rounded
into VERIFIED, never entered.

### 5.4 The hand-check stratum (fixed design)

A seeded random sample of graded candidates,
stratified across the three outcome classes —
**60 candidates: 30 VERIFIED / 15 CONFLICT / 15
UNRESOLVED, or the whole class where a class is
smaller** — hand-checked at execution against
the portion's page renders and the programme
records (renders stay local, §4 item 4). The
seed is fixed at this freeze: **20261021**,
recorded here and in the execution build script
before any sampling (DD-066-5); the draw is
`random.Random(20261021).sample` over each
class's sorted candidate list, the Spec 037
draw form. Additionally, if the VERIFIED draw
contains no medium-confidence candidate, the
first medium-confidence VERIFIED candidate in
seeded-shuffle order is added as a supplementary
hand-check, so the §5.3 rung-2 medium coverage
determination always has at least one sampled
medium to rest on where the class is non-empty;
the supplement is reported as such. Each
sampled CONFLICT is attributed by cause:
(i) extraction error in the intake table,
(ii) programme-side record error, (iii) genuine
compilation divergence, (iv) **true
non-identity**. Sampled VERIFIED and UNRESOLVED
candidates are checked for soundness and their
results reported as aggregates alongside the
census (the Spec 037 §4.6 form).

### 5.5 The halt rule (frozen form)

- If the CONFLICT share of **all graded
  candidates** (the denominator is the full
  census, 2,101; reasons SITE, NUMBER-AMBIGUOUS,
  CORROB-*) exceeds **20%**, the catalogue
  extension **halts**: the census completes and
  is reported in full, **no extension index is
  committed, no merged layer is pinned**, and
  the outcome is recorded as **INTAKE COMPLETE
  — CATALOGUE EXTENSION HALTED**.
- Independent tripwire: if the §5.4 stratum
  attributes **any** sampled candidate to true
  non-identity, the build halts on the same
  terms regardless of the conflict share — a
  string match that joins different objects is
  the one failure this catalogue must never
  absorb silently.
- On either halt, the remedy is a ruling on the
  conflicting class, not a friendlier re-run:
  no ladder step is re-run under a softer
  reading, and no candidate is force-matched.

### 5.6 The pinned artifacts the act produces

- **Committed (on pass only):** the extension
  index (§4 item 1) as a new file under the
  intake data area (`data/intake/`), with its
  SHA-256 and byte count recorded in the
  outcome record; plus the aggregate census
  record (the Spec 037 §4.4 form: outcome
  counts and shares overall and by referenced /
  unreferenced set and by portion section,
  conflict breakdown by reason, per-rung graded
  bases, the stratum result, the halt verdict
  with its arithmetic) as the phase's machine
  record in `reports/`, and the outcome record
  in this spec's `outcome.md` and the root
  LEDGER. Repo-cleanliness check (no
  portion-derived row-level file in tree or
  index, beyond the §4 item-1 index itself)
  runs before any grading and again before the
  outcome commit — the Spec 037 step-0.4 form.
- **Restricted-local, hash-pinned (on pass
  only):** the merged catalogue layer v2 file
  (vols. 1–2 + VERIFIED 3.1 objects), its
  SHA-256 + byte count + row and distinct-object
  counts recorded in the outcome record as
  definition constants (the DD-059-9 form); the
  local grade table and build record, named in
  the outcome by filename and row count only.
- **Validator:** the Phase-130 validator
  (`backend/glossa_lab/intake.py`, pin §7) runs
  over the extension dataset form **locally**
  before pinning. The dataset form carries one
  record per entered (VERIFIED) object with the
  number as `provenance.object_id`, site, type
  class, and empty token lists (the portion
  carries no transcriptions; the validator's
  empty-token warnings are expected and are
  reported as such). Its `license_basis` is the
  entry-22 gate itself, quoted; a dataset with
  no declared lawful basis is a REJECT at the
  license gate, and any REJECT verdict halts
  the pinning on the §5.5 terms (the census
  still reports in full).

### 5.7 The projected join (a projection, labelled)

On pass, the outcome record also reports a
**projection**: the joined-row count a future
join against the pinned merged layer would
reach on the Phase-421 census's own rows —
2,899 already-joined rows plus the census rows
whose carried identifier is a VERIFIED newly
entered object — stated against Spec 059's
frozen bar of 3,465 rows and labelled a
projection in every place it appears. No join
has run; the projection is arithmetic over the
committed census and this act's grades, nothing
more (§9).

## 6. Quantities reported (publishable aggregates)

Computed over the full candidate census and
reported overall, by candidate set (referenced
/ unreferenced), and by portion section
(Mohenjo-daro / Harappa old / Harappa HARP):
candidate count; VERIFIED / CONFLICT /
UNRESOLVED counts and shares; conflict
breakdown by reason code; per-rung graded bases
(how many candidates each ladder rung could
grade); the confidence-gate accounting
(low-confidence hand-verifications and their
results; medium class coverage determination);
type-class fill of the entered objects; the
hand-check stratum result (§5.4) with its cause
attributions; the halt verdict (§5.5) with its
arithmetic; and, on pass, the merged layer's
counts (rows, distinct objects, collisions
recorded) and the §5.7 projection. These
aggregates, and the §4 item-1 index, are the
publishable product of this act. The rates
describe **this portion's ranges only**; they
are not rates for Vol. 3.1 as a whole or for
CISI as a whole.

## 7. Execution shape (Phase-428)

1. **Graph-first build** (H15/H23): experiment
   script, graph module, registration in the
   experiment graph, registration verification,
   then run.
2. **Step 0 — gate and integrity, fail-closed,
   in this order:** (0.1) the Phase-130 gate is
   on record (PROVENANCE entry 22) and names
   this material restricted — re-verified on the
   record and quoted in the outcome; (0.2) every
   pin of §2 and below recomputes to its frozen
   value, by two routes where the artifact is
   committed: portion PDF `514338b1…` (8,206,446
   bytes); extraction table `7179858d…` (2,123
   records × 26 columns, census as intaken);
   vols. 1–2 CSVs `e0d698f9…` / `e751244e…`;
   horus84 layer `c368f290…`; Phase-421 census
   `95282931…` / results `3948cd01…`; Phase-130
   schema `b94d03ad…` (6,197 bytes); validator
   `backend/glossa_lab/intake.py` `02b24e33…`
   (18,867 bytes); (0.3) the candidate sets
   re-derive to the §3 counts (2,101 / 1,341 /
   1,293 / 48 / 760; zero-resolution rows
   1,790); (0.4) repo cleanliness — no
   portion-derived row-level file in the tree or
   index. Any failure stops the execution as
   itself, before any candidate is graded.
3. **Grading** (§5.3): candidate generation,
   ladder grading of the full census,
   low-confidence hand-verification, the
   hand-check stratum and its cause attribution,
   the medium-coverage determination, the
   §6 aggregates.
4. **Halt evaluation** (§5.5), then — on pass
   only — the merged layer build (§5.2), the
   validator run (§5.6), and the pinning.
5. **Outcome:** the aggregates, the halt
   verdict, and the pins recorded in this
   spec's `outcome.md`, the root LEDGER, the
   phase machine record, and the local build
   record (restricted store). Repo cleanliness
   re-checked before the outcome commit. No
   PRED-register entry is created or changed; no
   anchor changes; the foundation check is run
   as a read-back after the outcome lands (it is
   not a gate here, because no claim consequence
   lands on the anchors or the register — stated
   openly rather than implied, the Spec 037
   form).

## 8. What this act does not do

- It runs no join against the merged layer,
  computes no F1 quantity, and changes no
  verdict: `STUDY-SPEC-024/F1` stands as
  recorded, and Spec 059's record stands
  exactly as written. A successor F1 study
  needs its own spec, its own freeze, and its
  own OSF registration.
- **It files no OSF registration of its own**
  (DD-066-8): this is a data-intake act under
  the Spec 021 machinery, not a study; Item 7
  §6 attaches the registration to the successor
  F1 study spec, and the intake itself
  registers nothing.
- It acquires nothing and spends nothing: CISI
  vols. 3.2/3.3 and any other source for the
  remaining other-site zero-resolution rows are
  outside this act entirely.
- It edits neither compilation's data, resolves
  no conflict, repairs no garbled token, and
  contacts no library or lender.
- It puts nothing derived from the portion into
  git or any public surface beyond the §4
  line — including in this freeze, which cites
  only aggregates and pins already on record.

## 9. What this act would and would not establish

**Would.** How many of the portion's 2,101
numbers may lawfully and soundly enter the
programme's catalogue as objects, under a
ladder fixed before any candidate was graded —
and, on pass, one pinned merged catalogue layer
v2 whose VERIFIED 3.1 objects a successor study
could resolve against, plus the labelled
projection of what that layer would do to the
Spec 059 join arithmetic.

**Would not.** That any VERIFIED catalogue
object is a verified join (no join has run);
any F1 quantity or verdict on any set; anything
about signs, sequences, or readings (the
material has none); any statement about objects
outside the portion's ranges; any correction to
either compilation; coverage of CISI Vol. 3.1
as a whole (the portion is printed pp. 413–443,
≈ 6% of the volume, and its rates describe its
ranges only).

## 10. Governed claims (summary)

The governed register is `claims.json`
(F066-C01…C15):

- **C01** — outcome statements under this spec
  concern only the portion's candidate census
  and the catalogue construction.
- **C02** — a string match is a candidate,
  never a catalogue object.
- **C03** — a candidate is VERIFIED only under
  the fixed ladder of §5.3, applied to all
  2,101 candidates.
- **C04** — conflicts are recorded with reason
  codes, never repaired; ambiguous numbers
  cannot enter.
- **C05** — the halt rule: a conflict share
  above 20% of all graded candidates halts the
  extension; no index is committed, no layer
  pinned.
- **C06** — the tripwire: any stratum
  attribution to true non-identity halts the
  extension regardless of the conflict share.
- **C07** — the lawful line: only the §4
  item-1 fact list, aggregates, and pins enter
  the repo; every other row-level product stays
  in the restricted local store.
- **C08** — execution step 0 precedes any
  grading, fail-closed, in the frozen order.
- **C09** — the census grades all 2,101
  candidates; the referenced and unreferenced
  sets are reported separately.
- **C10** — the hand-check stratum is the
  frozen seeded design of §5.4.
- **C11** — the confidence gate: low-confidence
  numbers are ungraded until hand-verified
  against the page render; medium-confidence
  numbers enter only on the stratum's coverage
  of their class.
- **C12** — type is carried as published under
  the closed class set; an unfilled type is a
  recorded fact, not a gate outcome.
- **C13** — the merged layer holds one object
  per distinct number; a collision leaves the
  existing object standing, with no duplicate
  and no silent overwrite.
- **C14** — the extension dataset form is
  validated by the pinned Phase-130 validator
  under the quoted entry-22 license basis
  before pinning.
- **C15** — a VERIFIED catalogue object is not
  a verified join; no F1 quantity exists under
  this act, and the Spec 024 / Spec 059 records
  stand as recorded.

## 11. Design decisions

- **DD-066-1 — Step 0 fails closed, in a fixed
  order.** Gate, pins (two routes where
  committed), candidate-set re-derivation, repo
  cleanliness — each with a stated stop (§7).
  The gate check comes first because the
  material's restricted status governs every
  later act, including where outputs may live.
- **DD-066-2 — The grading is a census, not a
  sample.** 2,101 candidates is tractable, and
  the catalogue's coverage — the act's product —
  would be undefined for an unexamined
  remainder. Sampling appears only in the
  hand-check stratum (§5.4), whose object is
  error attribution and confidence coverage,
  not coverage of the catalogue.
- **DD-066-3 — The ladder's order and
  precedence are frozen.** Site, confidence
  gate, ambiguity bar, type carriage,
  corroboration. The first CONFLICT in ladder
  order is the recorded reason; a number whose
  own records span sites is recorded
  NUMBER-AMBIGUOUS (the Spec 037 grading
  precedent), because its records differ on
  join-relevant data. Type is carried, never
  compared: the Spec 037 TYPE-conflict mass was
  a cross-compilation vocabulary divergence,
  measured against a different compilation, and
  copying that rung here would grade a question
  this act does not ask (Item 7 §5.5).
- **DD-066-4 — The halt threshold and its
  denominator are fixed at freeze.** 20%
  (Item 7 §5.5's successor form, confirmed
  here), of **all graded candidates** — the
  full 2,101 census, referenced and
  unreferenced together, because the extension
  being halted is the whole build, and a
  denominator chosen at execution, with the
  rate visible, would not be a rule. The
  true-non-identity tripwire is independent of
  the share (§5.5).
- **DD-066-5 — The stratum design and seed are
  fixed at freeze.** 60 candidates (30 VERIFIED
  / 15 CONFLICT / 15 UNRESOLVED, whole class
  where smaller), seed **20261021** recorded in
  §5.4 and in the build script before sampling;
  the medium-coverage supplement of §5.4 is
  part of the frozen design, so the rung-2
  medium determination never rests on a
  sample that happened to contain no medium.
- **DD-066-6 — The confidence gate is
  operationalised, not left to judgement.**
  Low: every low-confidence well-formed
  candidate is hand-verified against its page
  render before grading completes; unconfirmed
  means UNRESOLVED and never entered. Medium:
  provisional VERIFIED until the stratum covers
  the class; one sampled medium found
  mis-extracted demotes the whole medium class
  (a class-level coverage failure is not
  repaired candidate-by-candidate).
- **DD-066-7 — The corroboration rung's
  UNGRADED base is stated at freeze.** Neither
  in-hand layer carries FC / excavation /
  museum values, so rung 5 grades no candidate
  on the held records. Stating this at freeze
  keeps the rung honest: it fires the day a
  held record carries such values, and its
  silence today is a property of the records,
  not an execution shortcut.
- **DD-066-8 — No OSF registration for the
  intake itself.** This act is a data act under
  the Spec 021 machinery; Item 7 §6 attaches
  the registration to the successor F1 study
  spec, which files its own at its own freeze.
  The reasoning is recorded here and in
  `adjudication.md` §4, openly, rather than the
  absence being left to look like an oversight.
- **DD-066-9 — Phase allocation: Phase-428.**
  Verified at freeze against `main`: Phase-424
  is Spec 062's execution phase, Phase-425 Spec
  063's, Phase-426 Spec 064's; Phase-427 is not
  referenced anywhere on `main` and execution
  of this act is allocated the next clean
  number, Phase-428.
- **DD-066-10 — The freeze gate reading
  (adopting DD-038-10).** The AEE lifecycle gate
  at this freeze is read as Spec 038's freeze
  read it and Specs 037/059/063 carried: the
  substantive pass is zero correctness failure
  modes and no claim below the 0.70 threshold
  at each of after_specify, after_plan,
  after_tasks; the FR-2.3 draft-cap records a
  draft register carries are structural, are
  disclosed in `aee/freeze-aee-note.md`, and are
  not correctness failures — the engine's
  outcome word therefore reads "iterate" while
  the gate passes.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
