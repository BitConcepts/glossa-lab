# Phase-133 — Stage 0 Report (Spec 024, Evidence Integration)

**Spec:** 024 — Evidence Integration: Tying the Inscriptions
to Non-Textual Evidence, **Stage 0 FROZEN 2026-10-09**
(owner: Tristen Pierson — "Execute the plan"). **Freeze +
merge:** PR #105 (merge commit `467adbcf`, freeze commit
`fecba9ec`). **Date of this report:** 2026-10-09.

**AI disclosure:** this Stage 0 build and this report were
executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.

Every quantity in this report is recomputed by
`backend/scripts/phase133_stage0_inventory.py` from the
files as they exist in the local store, and is recorded in
`data/evidence_integration/phase133_stage0_inventory.json`
(meta: `phase133_stage0_inventory_meta.json`, with input
paths and sha256 per input). **Nothing is copied from spec
Appendix A** — Appendix A values are the claims the drift
table in §7 checks the measured values against.

**Scope, stated once and binding (spec §3.1):** Stage 0
computes coverage and joinability only. No associations,
no correlations, no cross-tabulations beyond coverage
counting and the §3.3 key tests were computed. If a number
would be a finding about the inscriptions rather than
about the data, it is out of scope and does not appear
here. No anchor, reading, or PRED-2026 value is an input
or an output of this inventory (boundary 1); anchors
sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed
is asserted unchanged by the Phase-133 tests.

**Filled, defined:** a cell is filled iff its value is
present and, for strings, non-empty after stripping
whitespace; for lists/dicts, non-empty. Placeholder
strings that encode absence (`-`, `--`, `- -`, `None`,
`?`, `??`) are non-empty cells: they are counted as
filled in raw rates, and their count is recorded
separately per field in the inventory JSON wherever they
occur (materially: horus84 fields, §2.4 below).

---

## 1. What context evidence exists — and what does not (plain statement)

**Exists, as counted:**

- A catalogue spine: the Phase-124 CISI Vol. 1–2
  catalogue, 7,705 photo rows over 3,494 distinct
  volume-scoped objects, carrying `site` on 7,187 rows
  (93.3% of photo rows; Vol. 1 94.7%, Vol. 2 92.2%) and
  `object_type` on 7,380 rows (95.8%; Vol. 1 95.1%,
  Vol. 2 96.3%), and the CISI editors' own depiction
  classification `motif_chapter` on 2,005 rows (26.0%).
- A text layer (Holdat) whose own context codings are
  complete at token level — `site` 7,002/7,002 token
  rows over 1,670 inscriptions at 9 sites, and
  `iconography` 7,002/7,002 token rows — but which
  cannot be joined to the catalogue by any audited key
  (§3), and whose iconography is Class C (one
  compilation's depiction coding).
- A small text layer (mayig, 179 inscriptions) that
  joins cleanly to the catalogue (§3), all 179 joined
  objects being Seals at one site (Mohenjo-Daro, via
  the catalogue, for 176 of 179).
- An ICIT-lineage layer (horus84, 5,679 rows) with the
  deepest context schema in hand — region, site,
  area-section, block-house, room-grid, excavation
  ID, time, period, phase, depth, material, shape,
  preservation, object type, dimensions — under its
  standing lineage determination: admissible for
  descriptive and QC purposes, **not** an independent
  witness, and no result computed on it may be
  reported without its lineage label.
- Museum open-data records (Met 28 curated objects;
  Cleveland 10 search records; Penn 2 fetched records)
  carrying the fields CISI does not print — medium /
  material, dimensions, period, culture, accession
  and excavation data — for their own objects under
  their own keys, with **zero** CISI cross-references
  in hand (§3.5), so they join to nothing in the
  catalogue population.

**Does not exist, as counted:**

- Per-object material or dimensions for the CISI
  population. The catalogue `material` and
  `dimensions` fields are filled on **0 of 7,705 rows
  (0%)** — not printed per object in the CISI plates
  (Phase-124 premise correction). They stand empty per
  boundary 3 and were not back-filled from any source.
- Stratigraphic context (area / room / depth) for the
  CISI population. Those fields exist only in the
  ICIT-lineage layer, under its label.
- Any validated join from Holdat to the catalogue.
  `cisi_number` is PROHIBITED (§3.2); `seal_id` is
  intra-Holdat only. The Holdat↔catalogue
  matched-object join remains ~0 under legitimate key
  discipline — the Phase-131 situation, re-measured
  here at the key level, unchanged.
- Any motif coding of the CISI image store. None
  exists; `motif_chapter` (26.0% of rows, 909 of
  3,494 distinct objects) is the only catalogue-level
  depiction field, and it is the CISI editors' chapter
  organisation, with spelling variants and chapter
  headings in the field as printed (§6).
- The Tamil Nadu graffiti corpus. Not in hand
  (0 records); no number in this report assumes it.
- CISI Vols. 3.1 / 3.2 / 3.3 in any form. Stage
  designs use Vols. 1–2 only (spec §2.7).

---

## 2. Coverage summary by layer

The full (layer × field) matrix — 243 rows over 9
machine-readable layers, each with filled count + rate,
distinct-value count, top-5 values with counts, §3.4
grade with reason, and anomaly notes — is the committed
inventory JSON. The layer summary:

| Layer | Unit | Rows | Fields | Headline coverage (as measured) |
|---|---|---:|---:|---|
| CISI catalogue Vol. 1 | photo row | 3,320 | 22 | site 3,144 (94.7%); object_type 3,156 (95.1%); motif_chapter 832 (25.1%); material 0 (0%); dimensions 0 (0%) |
| CISI catalogue Vol. 2 | photo row | 4,385 | 22 | site 4,043 (92.2%); object_type 4,224 (96.3%); motif_chapter 1,173 (26.8%); material 0 (0%); dimensions 0 (0%) |
| Holdat corpus | token row | 7,002 | 19 | site 7,002 (100%); iconography 7,002 (100%); prefix 0 (0%); vowel 0 (0%) |
| Holdat semantic roles | symbol row | 151 | 15 | all 15 fields filled on all rows as acquired |
| mayig CISI layer v1 | inscription | 179 | 7 | all 7 fields filled on all 179 inscriptions |
| mayig source corpus | inscription side | 179 | 3 | 179 sides in 179 per-artefact JSON files; all 3 fields filled |
| horus84 inscriptions | inscription | 5,679 | 38 | site 5,679 (100% raw); material 5,679 raw (973 `-` placeholders); h/v/th dimensions partial (2,592 / 2,499 / 1,049 non-empty) |
| Met open data (curated Indus set) | object | 28 | 57 (union) | medium and dimensions filled on all 28 records |
| Cleveland open data (`indus` search file) | record | 10 | 60 (union) | 3 of 10 records carry type `Seals` |

Notes on the summary:

- **CISI site mass**, as photo rows: Mohenjo-Daro
  1,408 (Vol. 1) + 2,105 (Vol. 2); Harappa 853 +
  1,927; Vol. 1 also carries Lothal 502, Kalibangan
  237, Banawali 65, Jhukar 45, Desalpur 12, Rojdi 8,
  and small counts for Surkotada, Rangpur, Amri, and
  `Addenda` rows in both volumes. Site-name spellings
  differ across layers as printed (`Mohenjo-Daro` in
  the catalogue, `Mohenjo-daro` in Holdat and
  horus84); no normalisation was applied anywhere in
  Stage 0.
- **CISI object types**, as photo rows: Seals 4,778
  (2,055 + 2,723); Tablets 2,180 (977 + 1,203);
  Graffiti 417 (119 + 298); Objects 5 (Vol. 1 only);
  325 rows carry no object_type. As distinct
  volume-scoped objects: Seals 2,016; Tablets 866;
  Graffiti 395; Objects 4; 213 objects carry no type.
- **Holdat iconography** (token counts; Class C):
  unicorn 2,143; zebu bull 1,414; elephant 859;
  rhinoceros 726; script only 572; geometric 397;
  tiger 323; buffalo 292; gharial 276 — 9 distinct
  values over 1,670 inscriptions.
- **horus84 placeholders:** absence is encoded by
  `-`, `--`, `- -`, `None`, `?`, `??` and, in the
  `(mm)` dimension fields, by the value `0`
  (horizontal 1,809 zero rows; vertical 1,680;
  thickness 3,585). Example substantive rates net of
  the recorded placeholder counts: `symbol` carries
  `None`/`-` on 3,167 of 5,679 rows (3,170 rows
  carry a placeholder value in total); `cult` on
  4,222 of 5,679 (3,398 `None` + 824 `-`; 4,237
  placeholder rows in total); `material`
  carries `-` on 973 rows. Per-field placeholder
  counts are in the inventory JSON.
- **horus84 row lengths vary:** rows carry 35–38
  fields (35: 1,837 rows; 36: 1,933; 37: 1,850; 38:
  60); trailing fields omitted on shorter rows are
  treated as unfilled. This is why the trailing
  interpretive fields measure as they do: `sanskrit`
  filled 3,831 rows, `translation` 1,908, `notes`
  57 — as parsed from the file as acquired.

---

## 3. Join-key audit (§3.3) — results as found

Canonical key re-derived: `cisi:v{volume}:{printed_id}`.
Distinct objects: **Vol. 1: 1,475; Vol. 2: 2,019;
3,494 volume-scoped in total.** Exactly one printed ID,
`H-311`, occurs in both volumes, so the unscoped union
is 3,493 and volume-scoping is necessary.

Within-volume duplicates: a printed ID legitimately
carries several photo rows (one per photographed
side/view) — Vol. 1: 1,243 IDs carry more than one
photo row (max 9 rows per ID); Vol. 2: 1,513 (max 8).
That repetition is the catalogue structure, not a
collision. The row-level key anomaly is exact duplicate
`photo_key` values: **Vol. 1: 8** (`H-11 A`, `H-11 a`,
`H-295 B`, `H-332 C`, `H-76 A`, `L-66 c`, `M-489`,
`M-620 A`, each ×2); **Vol. 2: 3** (`M-1083 a`,
`M-1233 a`, `M-1433`, each ×2).

### 3.1 mayig `cisi_object_id` — USABLE for these 179 values

Tested against the volume-scoped catalogue keys:
**matched (exactly one volume): 179 of 179 — all
Vol. 1 only; ambiguous (present in both volumes): 0;
unmatched: 0.** The verdict is empirical for these 179
values; no semantics was assumed from the ID prefixes.

### 3.2 horus84 `cisi` — NOT USABLE as a general join key

Tested the same way, per row (5,679 rows; 4,074
distinct values): **matched (exactly one volume):
2,895 rows (1,365 Vol. 1 only + 1,530 Vol. 2 only);
ambiguous: 2 rows (the single distinct value `H-311`,
present in both volumes); unmatched: 2,782 rows.**
Distinct values: matched 2,476; ambiguous 1 (`H-311`);
unmatched 1,597. The field also carries a `-`
placeholder on 662 rows and non-CISI artefact
numberings (e.g. `Agr-`, `Blk-`, `C-` prefixed
values). A key that fails validation is reported as
**NOT USABLE** with its numbers: no layer-wide join on
this field is validated. Rows whose value matches
exactly one volume are counted above as matched for
that row only (§8 arm (a) uses exactly those rows,
under the ICIT lineage label).

### 3.3 Holdat `cisi_number` — PROHIBITED (documented, never joined on)

- Exact-string coincidence with a printed catalogue
  ID: **0 token rows, 0 distinct values** — the values
  are zero-padded (`H-0001`, `M-0001`) where catalogue
  printed IDs are unpadded (`H-1`, `M-1`).
- Collision behaviour, documented factually: after
  stripping leading zeros only, **1,355 of 1,670
  distinct Holdat values coincide with some printed
  catalogue ID (5,678 of 7,002 token rows)**, and
  **all 179 mayig IDs have a zero-padded namesake in
  Holdat**. That is the Phase-131 fact re-measured:
  179 apparent namesakes, **0 validated** as identity.
  Coincidence under normalisation is not a join, and
  no join on this field was performed.

### 3.4 Holdat `seal_id` — intra-layer only

1,670 distinct `seal_id`s over 7,002 token rows;
rows-per-id distribution: 2 rows ×269 ids, 3 ×330,
4 ×415, 5 ×330, 6 ×164, 7 ×116, 8 ×46 (min 2, max 8).
Cross-layer use requires a validated bridge; none
exists (§3.3).

### 3.5 Museum records — cross-reference census: 0

Rule: a record carries a CISI cross-reference iff any
string value in the acquired record contains `CISI`
or `Corpus of Indus` (no museum schema in hand has a
dedicated CISI cross-reference field). Census:
**Met 0 of 28; Cleveland 0 of 10; Penn 0 of 2;
total 0 of 40 records.** No museum-to-CISI join is
counted or performed. Museum records supply their
own objects' metadata under their own keys only
(boundary 3); the Penn records' other numbers
(Boston MFA number, Field Nos.) are not CISI
cross-references.

---

## 4. Field-provenance grading (§3.4) — the Class I exclusion list

Every field of every machine-readable layer was
graded O / C / I with a one-line reason (all 243
grading records are in the inventory JSON). Totals:
**O: 207 fields; C: 7 fields; I: 29 fields.**

Class C fields (depiction-coded), for the record:
catalogue `motif_chapter` (both volumes); Holdat
`iconography`; mayig layer `description`; mayig
source `description`; horus84 `symbol`; horus84
`cult`.

**Class I fields — excluded from context evidence at
every stage, listed explicitly by layer and name
(29):**

- **Holdat corpus (12):** `letters`,
  `letter_label_encoded`, `FormWithoutLemma`,
  `MorphemeSeparated`, `morpheme boundary`, `noun`,
  `verb`, `prefix`, `prefix_label_encoded`, `vowel`,
  `upos`, `xpos`.
- **Holdat symbol semantic-roles table (9):**
  `symbol`, `num_prefixes`, `num_suffixes`,
  `num_shells`, `shell_density`, `is_starter`,
  `is_ending`, `is_known_role`, `semantic_role`.
- **mayig CISI layer (2):** `tokens`, `features`.
- **mayig source corpus (1):** `graphemes`.
- **horus84 inscriptions (5):** `class`, `text`,
  `sanskrit`, `translation`, `notes`.

Two grading notes, stated plainly: (i) Holdat `upos`
and `xpos` are constant (`SIGN` / `INDUS` on all
7,002 rows) and `prefix`/`vowel` are empty on all
rows — they are graded Class I because they are the
compilation's part-of-speech and morpheme
annotations, regardless of their constant or empty
content as acquired; (ii) the catalogue `material`
and `dimensions` fields are graded Class O — they
would be observational — and stand at **0% filled /
absent as printed**, never back-filled or inferred
(boundary 3).

---

## 5. mayig description parseability (§2.3 / §3)

**Rule, declared before application:** case-insensitive
substring match of the mayig layer's free-text
`description` against a motif-term list (the spec
§4.3 published iconographic categories union the
distinct values of the Holdat `iconography` field as
measured in this run — unicorn, zebu, bull, buffalo,
elephant, rhinoceros, goat, antelope, tiger,
composite, human, cult, narrative, geometric,
script only, no depiction, illegible, gharial) and an
object-type-term list (seal, tablet, object, pottery,
graffiti, plaque, impression). A parse is a string
match under this stated rule only; **a parse is never
reported as ground truth.**

Counts, as measured: descriptions tested: **179**;
containing ≥1 motif term: **179**; containing ≥1
object-type term: **179**; both: **179**; neither:
**0**. Top matched terms: motif — `unicorn` 179 (the
only motif term matched); object type — `seal` 179
(the only object-type term matched). The field
contains only **5 distinct descriptions** in total —
`unicorn I seal` (9), `unicorn II seal` (19),
`unicorn III seal` (45), `unicorn IV seal` (96),
`unicorn V seal` (10) — so the 179/179 parse rate
measures the narrowness of this field's vocabulary
as acquired, not a general property of free-text
descriptions.

---

## 6. Non-machine-readable pass (T4) and anomalies

### 6.1 Kodumanal volume (descriptive only)

152-page scanned excavation-report volume (DLI scan,
local research copy) with an OCR text layer; not a
dataset. The Kodumanal report (printed pp. 1–50 of
the volume, which also contains the Karur and
Poompuhar reports) is organised as: Introduction,
Historical Background, **Trenches**, Cultural Sequence
and Chronology, Pottery, **Graffiti Marks**,
Antiquities, Conclusion. The Trenches section is
organised by trench (15 distinct `KML-n` labels in
the OCR text); each trench entry records
location/orientation, dimensions, depth,
layers/phases, and antiquities recovered, in prose.
Context is habitation trenches plus the megalithic
burial complex; pottery is classified by ware
(Black-and-red, Russet-coated, Red, Black), and the
Graffiti Marks section discusses marks by ware, by
vessel position (shoulder near the rim), and as
pre-firing vs surface marks, then gives a numbered
prose description list of individual marks with
their wares. Its printed tallies are quoted here as
printed prose only, because they are internally
inconsistent: the section states "Out of 175 graffiti
marks 75 in Black and Red ware, 70 Red ware, 70
Russet Coated ware and 10 Black ware were noticed"
— subtotals summing to 225, not 175 — and separately
that "41 Brahmi sherds were observed and 99 Graffiti
marks were collected". **No tally from this volume
is used as a count anywhere in Stage 0.**

### 6.2 Kunal article (descriptive only)

Journal article PDF (J-STAGE, 2012, DOI
10.5356/jorient.55.22), 15 PDF pages, presenting
Early Harappan seals from Kunal within the
excavation's stratigraphic/period framework in prose
and plates (spec §2.6). There is no tabular
per-object record structure a parser could audit.
Measured file property (not a content count): its
embedded text layer contains **0 alphanumeric
characters** (the extracted characters are NUL
glyphs) — the article's text and seal drawings are
page images, which is the mechanical reason no
machine-readable pass is possible on the file as
acquired. No counts are taken from it.

### 6.3 Anomaly: `holdatllc_seal_catalog.csv` — content does not match its name

`data/raw/other_sites/holdatllc_seal_catalog.csv`
(1,031 bytes, 1 line) is **not CSV and contains no
seal catalogue**: it is a single-line JSON document
in the shape of an Ollama `/api/tags` response,
listing three locally installed LLM models
(`qwen2.5-coder:7b-instruct`, `qwen2.5:14b`,
`mistral-nemo:12b`). Zero seal records are
recoverable from it. Recorded as found (spec §3.2 /
task T4); not routed around, and not used as a data
layer anywhere in Stage 0.

### 6.4 Further anomalies recorded

- Catalogue `motif_chapter` values as printed
  include spelling variants of `unicorn` (Vol. 1:
  `unicorm` 33, `unicom` 23, `unicon` 2; Vol. 2:
  `uricorn` 11, `unico` 10, plus `tigerwithzebu` 8)
  and, in Vol. 1, chapter-heading strings in the
  motif field (`SEALS` 8, `SEALSIMPRESSIONS` 10).
  Recorded as found; no cleaning was applied.
- Duplicate catalogue `photo_key` values (§3):
  8 in Vol. 1, 3 in Vol. 2.
- horus84 placeholder conventions and variable row
  lengths (§2). The `(mm)` dimension fields use `0`
  for absence, so their raw filled rate (100%)
  does not mean every object was measured.
- Museum acquisition files vs their summaries: the
  Met objects directory holds 74 fetched files
  (search candidates); the curated Indus layer is
  the 28 listed object IDs. The Cleveland `indus`
  search file holds 10 records, of which 3 are
  seals (§7 drift).

---

## 7. Appendix A drift table (Appendix A claim vs Stage 0 measured)

All Appendix A headline numbers were re-measured
from the files. The full machine-readable table is
in the inventory JSON; it is reproduced here in
full. **Three DRIFT items and one NOT RECOMPUTED
item; everything else MATCHes.**

| Item | Appendix A | Measured | Verdict |
|---|---|---|---|
| CISI catalogue total photo rows | 7705 | 7705 | MATCH |
| CISI Vol. 1 photo rows | 3320 | 3320 | MATCH |
| CISI Vol. 1 distinct printed IDs | 1475 | 1475 | MATCH |
| CISI Vol. 2 photo rows | 4385 | 4385 | MATCH |
| CISI Vol. 2 distinct printed IDs | 2019 | 2019 | MATCH |
| CISI distinct volume-scoped objects | 3494 | 3494 | MATCH (clarification: unscoped union is 3,493 — `H-311` occurs in both volumes) |
| CISI fields per volume | 22 | 22 | MATCH |
| CISI Vol. 1 site fill % | 94.7 | 94.7 | MATCH |
| CISI Vol. 1 object_type fill % | 95.1 | 95.1 | MATCH |
| CISI Vol. 1 motif_chapter fill % | 25.1 | 25.1 | MATCH |
| CISI Vol. 2 site fill % | 92.2 | 92.2 | MATCH |
| CISI Vol. 2 object_type fill % | 96.3 | 96.3 | MATCH |
| CISI Vol. 2 motif_chapter fill % | 26.8 | 26.8 | MATCH |
| CISI motif_chapter filled rows | 2005 | 2005 | MATCH |
| CISI material fill % | 0.0 | 0.0 | MATCH |
| CISI dimensions fill % | 0.0 | 0.0 | MATCH |
| CISI object_type row totals | Seals 4778, Tablets 2180, Graffiti 417, Objects 5 | Seals 4778, Tablets 2180, Graffiti 417, Objects 5 | MATCH |
| Holdat token rows | 7002 | 7002 | MATCH |
| Holdat distinct seal_id | 1670 | 1670 | MATCH |
| Holdat fields | 19 | 19 | MATCH |
| Holdat site fill % (token level) | 100.0 | 100.0 | MATCH |
| Holdat iconography fill % (token level) | 100.0 | 100.0 | MATCH |
| Holdat iconography top values | unicorn 2143, zebu bull 1414, elephant 859, rhinoceros 726, script only 572, geometric 397 | identical | MATCH |
| mayig inscriptions | 179 | 179 | MATCH |
| mayig tokens | 1003 | 1003 | MATCH |
| mayig distinct signs | 182 | 182 | MATCH |
| horus84 rows | 5679 | 5679 | MATCH |
| horus84 fields | 39 | **38** | **DRIFT** — the acquired header contains 38 field names; Appendix A.4's own enumerated list also names 38 (the same 38, in order) while its prose says 39, and §2.4 repeats 39. The "39" is a miscount in the spec text; the field inventory matches the header exactly. |
| Met objects in curated Indus layer | 28 | 28 | MATCH |
| Met "incl. 4 inscribed seals" (A.5) | 4 inscribed seals | 4 seal objects, of which 1 title mentions an inscription | **DRIFT (wording)** — the 4 objects are stamp seals 49.40.1–.4; only 49.40.3 is titled with "inscription". |
| Cleveland "3 seals" (A.5) | 3 | 3 records with type `Seals`, in an acquired search file of 10 records | **DRIFT (presentation)** — A.5 summarises the layer by its seals; the file as acquired is the full `indus` search set (3 seals, 1 jar, 6 other object types). Stage 0 inventories the file as acquired. |
| Penn records | 2 | 2 | MATCH (a third object is noted as seen in a gallery listing but was not fetched and is not counted) |
| Phase-124 sample field accuracy (§2.1) | 98.9% | not recomputed | NOT RECOMPUTED — Stage 0 takes no new hand-verified sample; the Phase-124 figure stands as a fact of record, not a Stage 0 measurement. |

---

## 8. Arm-by-arm feasibility verdicts for the §5 sketches (grounded only in this audit)

These verdicts state which §5 sketches survive
contact with the inventory, on the Stage 0 numbers
only. Each Stage 2 test still requires its own
freeze (§5 / §12); nothing here authorises a test.

### (a) Terminal-class × object-type

> **(a) Terminal-class × object-type — SURVIVES IN
> REDUCED FORM, on the joined subsets only.** An
> audited join from a text layer to catalogue object
> types exists for exactly two layers. mayig: all
> 179 inscriptions join unambiguously to Vol. 1
> catalogue objects (§3.1), 179 of 179 with
> object_type filled — and all 179 joined objects
> are Seals, so the mayig population contains no
> object-type variation and cannot by itself support
> an object-type contingency. horus84 (ICIT-lineage;
> the lineage label is mandatory on any use): 2,895
> of 5,679 rows join unambiguously to a catalogue
> object (§3.2), of which 2,752 rows have a filled
> catalogue object_type (Seals 1,588; Tablets 1,088;
> Graffiti 69; Objects 7; a further 143 joined rows'
> objects carry no type) — object-type variation
> exists on this joined subset only, with 2,784 of
> 5,679 rows (49.0%) unjoinable or ambiguous on the
> audited key. Holdat does not survive for this
> sketch: 0 inscriptions are joinable to catalogue
> object types (`cisi_number` PROHIBITED, `seal_id`
> intra-layer only), and Holdat carries no
> object-type field (its `form` values are
> `seal_NNNN` on all 7,002 token rows). Site, the
> sketch's control variable, is available for the
> joined subsets: mayig via the catalogue for 176 of
> 179 inscriptions (all Mohenjo-Daro; 3 joined
> objects' catalogue rows carry no site), and
> horus84 carries its own `site` field on 5,679 of
> 5,679 rows. A Stage 2 freeze for (a) must restate
> the test on these joined populations, with the
> ICIT lineage label on the horus84 arm; the sketch
> as drafted over "a text layer" generally does not
> survive.

### (b) Motif × sequence

> **(b) Motif × sequence — NO RECOMMENDATION is
> made (per §3.5); the existence question Stage 0
> may answer is answered YES at the proposed
> scale.** Motif-bearing fields exist: the
> catalogue's `motif_chapter` is filled on 2,005 of
> 7,705 photo rows (26.0%), covering 909 of 3,494
> distinct volume-scoped objects; Holdat's
> `iconography` is filled on 7,002 of 7,002 token
> rows over 1,670 inscriptions and is Class C — one
> compilation's depiction coding, with no verifiable
> coding provenance; mayig's `description` parses
> under the stated §5 rule at 179 of 179 with both
> a motif term and an object-type term, but the
> field contains only 5 distinct descriptions, all
> "unicorn {I–V} seal", so that rate measures this
> field's narrow vocabulary, not a general motif
> source; horus84's `symbol` and `cult` fields
> (both Class C, ICIT-lineage) exist, with
> placeholder values on 3,170 and
> 4,237 of 5,679 rows respectively. The image
> population the pilot would draw on exists at the
> proposed ~100-object scale: the catalogue holds
> 7,705 photo rows over 3,494 distinct objects in
> the local image store's catalogue population.
> Stage 1 dependency, stated plainly: test (b) runs
> only if Stage 1 — separately approved in
> principle, still requiring its separate
> post-Stage-0 go — passes its §4.5 proceed gate.
> Stage 0 neither recommends nor forecloses Stage 1
> beyond the existence facts above.

### (c) Site repertoire

> **(c) Site repertoire — SURVIVES as a coverage
> proposition.** Site exists at inscription level in
> two text layers. Holdat: `site` filled on 7,002
> of 7,002 token rows over 1,670 inscriptions at 9
> sites — per-site inscription counts (coverage
> facts): Mohenjo-daro 606, Harappa 492, Lothal 124,
> Kalibangan 110, Dholavira 106, Chanhu-daro 78,
> Surkotada 61, Banawali 60, Rakhigarhi 33.
> horus84 (ICIT-lineage label mandatory): `site`
> filled on 5,679 of 5,679 rows across 77 distinct
> site values — Harappa 2,717, Mohenjo-daro 1,923,
> Dholavira 238, Kalibangan 212, Lothal 208, with
> the remaining 72 values sharing 381 rows
> (including `Unknown`, 28 rows). mayig carries no
> site field of its own; site reaches its
> inscriptions only through the audited catalogue
> join (176 of 179 with a catalogue site, all
> Mohenjo-Daro; 3 with none), so a mayig
> site-repertoire comparison has exactly one site
> represented. The catalogue itself carries `site`
> on 7,187 of 7,705 photo rows (93.3%). Whether the
> per-site populations support any frozen test's
> minimum-cell rule is a Stage 2 freeze question;
> Stage 0 records only that the site fields and the
> per-site populations exist as counted.

### (d) Graffiti comparative

> **(d) Graffiti comparative — SURVIVES ONLY as
> the comparative, descriptive sketch §5.5
> drafted.** In hand: catalogue Graffiti photo
> rows 417 (Vol. 1: 119; Vol. 2: 298) over 395
> distinct volume-scoped objects; the Kodumanal
> volume's prose structure (§6.1 — a
> trench-organised excavation report with a
> dedicated Graffiti Marks section describing
> marks by ware and vessel position, whose printed
> tallies are internally inconsistent and are used
> as no counts); and the horus84 / Holdat type
> fields as the machine-readable graffiti-adjacent
> material. The Tamil Nadu graffiti corpus itself
> is NOT in hand — 0 records (access requested
> 2026-10-08; no reply at spec drafting) — and no
> Stage 0 number assumes it, so a repertoire
> comparison against that corpus cannot be
> computed from material in hand. Boundary 4
> stands: graffiti material is never pooled with
> seal texts in any test under this spec, and the
> §5.5 dating-gap caveat (the Tamil Nadu material
> is separated from the Indus material by ≥1,000
> years on the published rebuttal) attaches to any
> comparative output: a permitted output is
> "resemblance measured"; a prohibited output is
> any continuity, descent, or survival claim.

---

## 9. Deliverables and disposition

- Builder: `backend/scripts/phase133_stage0_inventory.py`
  (deterministic; input paths parameterised; recomputes
  everything from the local-store files).
- Dataset: `data/evidence_integration/phase133_stage0_inventory.json`
  + `phase133_stage0_inventory_meta.json` (provenance,
  license basis per layer, input paths + sha256, spec
  reference; content hash recorded in the meta).
- Experiment graph: node `IndusPhase133Stage0Inventory`
  (additive module
  `backend/glossa_lab/experiment_graph_phase133.py` +
  one registry block, Phase-132 pattern).
- Tests: `backend/tests/test_phase133_stage0_inventory.py`
  — committed-JSON internal consistency (passes where
  the local store does not exist); the recomputation
  test skips cleanly when inputs are absent.
- Tasks T1–T5 of spec 024 are marked done in
  `specs/024-evidence-integration/tasks.md`. **T6 —
  release-gated CC BY 4.0 publication of this
  inventory dataset — is handled separately by the
  coordinator and is not performed by this build.**
  No publication, external send, or outreach of any
  kind was made. No images or restricted source files
  are in this change: text, code, and JSON only.
- No anchor changes: anchors sha256
  eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed
  asserted unchanged in the Phase-133 tests. No PRED
  evaluation was run or implied.
