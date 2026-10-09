# Program note, Spec 024 and Phase-133: the Stage 0 evidence-integration inventory — context fields audited, join keys validated, feasibility stated as found

**Tristen Pierson** (BitConcepts LLC) — ORCID 0009-0003-7269-956X

Program note, 2026-10-09. Prepared as an addendum to the program's
preprint record (Zenodo concept record DOI
10.5281/zenodo.20379070; previous published version v4.5.0, DOI
10.5281/zenodo.23266588, record 23266588). Program provenance
registry: OSF [osf.io/ybd65](https://osf.io/ybd65/). Code, frozen
specs, and machine-readable results: BitConcepts/glossa-lab
(Spec 024; Phase-133; repository main at commit
a289b19b8ae657e092e426aac651bcacb18298f9, merge of PR #106; the
release-source commit for this note is recorded in
`RELEASE_VALIDATION.json`).

This note reports Spec 024 and Phase-133 exactly as they stand in
the merged report (`reports/phase133_stage0_report.md`), negatives
included. Neither the spec nor the phase changed any decipherment
anchor: the anchors file `backend/reports/INDUS_FINAL_ANCHORS.json`
is byte-identical throughout (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed).
The Phase-125 verdict — **FAIL — DISAGREEMENT** — is final and
unchanged; spec 020's adjudication outcome — **NO** — stands
untouched. **PRED-2026-001, PRED-2026-002, and PRED-2026-003
remain PENDING.** Stage 0 computed coverage and joinability only:
no association, correlation, or cross-tabulation beyond coverage
counting was computed, and nothing in this note is evidence that
any particular reading of any Indus sign is right or wrong.

## Abstract

Spec 024 opened the one axis the program had not used: the
non-textual context of the inscriptions — findspot, object type,
depiction, material — evidence recorded by archaeologists without
any theory of what the signs mean. Its Stage 0 is an inventory,
executed as frozen in Phase-133: a field × layer coverage matrix
(243 rows), a join-key audit with empirical collision rates, and
a provenance grading of every inventoried field (observational
207, depiction-coded 7, interpretive 29 — the 29 interpretive
fields are excluded from context evidence by construction). The
audit's central findings: the mayig layer's keys join its 179
inscriptions unambiguously to Vol. 1 catalogue objects; the
ICIT-lineage `cisi` field joins only 2,895 of 5,679 rows and is
**NOT USABLE** as a general join key; the museum open-data records
in hand carry **zero** CISI cross-references, so no museum join
exists; the CISI catalogue's `material` and `dimensions` fields
stand at **0% filled**, as printed, never back-filled; and the
Holdat `iconography` field — the richest motif source in hand —
is one compilation's depiction coding with no verifiable coding
provenance (Class C). Of the four designed association sketches,
one survives only in reduced form, one survives as a coverage
proposition, one survives only as a comparative description, and
one is not Stage 0's to recommend. Per the owner's adjudication,
the Stage 0 inventory dataset is deposited with this release
under **CC BY 4.0** (facts only; no images, ever).

## 1. Spec 024 — frozen with owner adjudication (Stage 0 freeze)

Spec 024 (evidence integration: tying the inscriptions to
non-textual evidence) was drafted as a proposal, then **frozen
for Stage 0 on 2026-10-09 with the owner's adjudication
recorded** (owner: Tristen Pierson — "Execute the plan";
freeze commit fecba9ec; freeze + merge: PR #105, merge commit
467adbcf). The four decision asks were answered: (1) Stage 0 —
**GO** as specified; (2) the motif pilot (Stage 1) is **approved
in principle** with its shape as drafted and still requires its
separate post-Stage-0 go; (3) the Stage 1 coder basis is
**blinded AI double-coding with the Phase-132 disclosure**,
recorded at the freeze so the Stage 1 decision is not blocked on
it later; (4) publication form — the Stage 0 inventory dataset is
**published CC BY 4.0 through the release gate** at Stage 0
completion (facts only, no images, ever). Stages 1 and 2 are not
frozen; each freezes separately. The spec's epistemic boundary
binds every stage: no output can mint, promote, demote, or
validate any sign reading, change any anchor, or touch
PRED-2026 in either direction.

## 2. Stage 0 as executed (Phase-133; PR #106, merge a289b19b)

Every quantity was recomputed from the files by a deterministic
builder (`backend/scripts/phase133_stage0_inventory.py`); nothing
was copied from the spec's drafting-time Appendix A, and the
drift between the two is tabled in the report and in §7 below.

**Layers inventoried (rows / unit):** CISI Vol. 1 catalogue —
3,320 photo rows, 22 fields; CISI Vol. 2 catalogue — 4,385 photo
rows, 22 fields; Holdat corpus — 7,002 token rows, 19 fields;
Holdat semantic-roles table — 151 symbol rows, 15 fields; mayig
layer — 179 inscriptions, 7 fields; mayig source corpus — 179
sides in 179 files, 3 fields; horus84 (ICIT-lineage) — 5,679
inscription rows, **38 fields**; Met curated Indus set — 28
objects; Cleveland search file — 10 records; Penn Museum — 2
records. The coverage matrix has **243 (layer × field) rows**.

**Key coverage, as found:** catalogue `site` filled 3,144
(94.7%) / 4,043 (92.2%) and `object_type` 3,156 (95.1%) / 4,224
(96.3%) (Vol. 1 / Vol. 2); catalogue `motif_chapter` 832 (25.1%)
/ 1,173 (26.8%) — 2,005 photo rows covering 909 of 3,494 distinct
objects; catalogue `material` **0 of 7,705 (0%)** and
`dimensions` **0 of 7,705 (0%)**, as printed, never back-filled.
Holdat `site` and `iconography` are each filled on 7,002 of 7,002
token rows (iconography top values: unicorn 2,143 tokens, zebu
bull 1,414, elephant 859). The horus84 layer's dimension fields
(`h` / `v` / `th`) are filled on 2,592 / 2,499 / 1,049 rows, and
its millimetre fields record absence as `0` (1,809 / 1,680 /
3,585 zero rows) — a placeholder convention, recorded as found.

## 3. Join-key audit — the keys that pass, and the keys that do not

Canonical keys re-derived: **1,475 (Vol. 1) + 2,019 (Vol. 2) =
3,494 volume-scoped objects** under `cisi:v{volume}:{printed_id}`.
Exactly one printed ID occurs in both volumes — **`H-311`** —
so the unscoped union is 3,493; volume scoping is mandatory, as
Spec 023 established. Exact duplicate `photo_key` values within
a volume: 8 in Vol. 1, 3 in Vol. 2 (listed in the inventory).

- **mayig `cisi_object_id` — USABLE for this layer as found:**
  matched **179 of 179**, all to Vol. 1 only; ambiguous **0**;
  unmatched **0**. The verdict is empirical for these 179 values,
  not a semantics assumed from the ID prefixes.
- **horus84 `cisi` — NOT USABLE as a general join key:** of
  5,679 rows, matched to exactly one volume **2,895** (1,365
  Vol. 1 + 1,530 Vol. 2), ambiguous **2** (the value `H-311`),
  unmatched **2,782**; 662 rows carry the `-` placeholder; the
  field's values include non-CISI artefact numberings. Rows that
  match are counted for those rows only; no layer-wide join on
  this field is validated.
- **Holdat `cisi_number` — PROHIBITED, never joined on**
  (Phase-131: internal sequential numbering). Its collision
  behaviour, documented factually: exact string coincidence with
  a printed catalogue ID is **0 rows / 0 distinct values** (the
  values are zero-padded); after zero-stripping only, 1,355 of
  1,670 distinct values coincide with some printed ID — the
  illusion of a key, quantified. Phase-131 stands: 179 apparent
  matches, 0 validated.
- **Holdat `seal_id`** is an intra-layer key only: 1,670 distinct
  values over 7,002 token rows, 2–8 rows per value.
- **Museum accession / object IDs — no join exists in hand:**
  **0 of 40** museum records (Met 0/28, Cleveland 0/10, Penn 0/2)
  carry any CISI cross-reference. Joins are counted only where a
  published cross-reference exists; none was invented.

**Verification note (coordinator, 2026-10-09).** The key audit
matches candidate values by exact string. Three horus84 `cisi`
values carry trailing whitespace (`H-1734\t`, `L-78␣`, `M-929␣`);
the first matches no printed ID under any rule, and the other two
are whitespace variants of valid printed IDs that count as
unmatched under the exact rule. The audit's counts stand as
computed under that stated rule; the discrepancy against a
whitespace-trimming recount is exactly these 2 rows, recorded
here and in the ledger addendum so the record is complete.

## 4. Field-provenance grading — and the Class I exclusion list

Every inventoried field was graded by recorder provenance:
**Class O (observational) 207, Class C (depiction-coded) 7,
Class I (interpretive) 29**, summing to the 243 coverage rows.
Class I fields — a compilation's own linguistic or semantic
theory — are **excluded from context evidence at every stage**,
and are listed here so the exclusion is auditable. Holdat
corpus: `letters`, `letter_label_encoded`, `FormWithoutLemma`,
`MorphemeSeparated`, `morpheme boundary`, `noun`, `verb`,
`prefix`, `prefix_label_encoded`, `vowel`, `upos`, `xpos`.
Holdat semantic-roles table: `symbol`, `num_prefixes`,
`num_suffixes`, `num_shells`, `shell_density`, `is_starter`,
`is_ending`, `is_known_role`, `semantic_role`. mayig layer:
`tokens`, `features`. mayig source corpus: `graphemes`. horus84:
`class`, `text`, `sanskrit`, `translation`, `notes`. The seven
Class C fields (depiction-coded, usable only with their coding
provenance attached) include the catalogue's `motif_chapter`,
Holdat's `iconography`, and horus84's `symbol` and `cult` — the
last two carrying placeholder values on 3,170 and 4,237 of 5,679
rows respectively.

## 5. The mayig description field — a parseability result that measures itself

Under the rule declared before application (case-insensitive
match against a stated motif-term and object-type-term list),
179 of 179 descriptions contain a motif term, 179 of 179 an
object-type term — **and the field contains only 5 distinct
descriptions, all of the form "unicorn {I–V} seal"** (unicorn IV
96, unicorn III 45, unicorn II 19, unicorn V 10, unicorn I 9).
The 179/179 rate measures this field's narrow vocabulary, not a
general motif source, and no parse is treated as ground truth.
The mayig layer is, as found, a unicorn-seal-only population —
a coverage fact with direct consequences for §7(a).

## 6. Anomalies recorded, not routed around

- `data/raw/other_sites/holdatllc_seal_catalog.csv` **is not a
  catalogue and is not CSV**: it is a single-line JSON document
  in the shape of an Ollama `/api/tags` response listing locally
  installed LLM models (1,031 bytes). Zero seal records are
  recoverable from it. Recorded as found; not used as a layer.
- The catalogue's `motif_chapter` values, as printed, include
  spelling variants (`unicorm` 33, `unicom` 23, `uricorn` 11,
  `unico` 10, `unicon` 2, `tigerwithzebu` 8) and Vol. 1 chapter
  headings (`SEALS` 8, `SEALSIMPRESSIONS` 10) sitting in the
  motif field.
- horus84 rows have variable field counts (35 fields: 1,837
  rows; 36: 1,933; 37: 1,850; 38: 60); trailing fields omitted
  on shorter rows are treated as unfilled.
- The Kodumanal volume's printed graffiti tallies are
  internally inconsistent (subtotals 75+70+70+10=225 under a
  stated total of 175, plus a separate "99 Graffiti marks
  collected"); they are quoted as printed prose only and used
  as **no counts**. The Kunal article, as acquired, has an
  embedded text layer containing **zero** alphanumeric
  characters, so no machine-readable pass is possible; no counts
  were taken from it.

## 7. Feasibility of the designed association sketches — as found

**(a) Terminal-sign class × object type — SURVIVES IN REDUCED
FORM, on the joined subsets only.** An audited join from a text
layer to catalogue object types exists for exactly two layers.
mayig: all 179 inscriptions join unambiguously (179 of 179 with
`object_type` filled) — and all 179 joined objects are **Seals**,
so the mayig population contains no object-type variation and
cannot by itself support an object-type contingency. horus84
(ICIT-lineage; the lineage label is mandatory on any use):
2,895 of 5,679 rows join unambiguously, of which 2,752 rows have
a filled catalogue object type (Seals 1,588; Tablets 1,088;
Graffiti 69; Objects 7) — object-type variation exists on this
joined subset only, with 2,784 of 5,679 rows (49.0%) unjoinable
or ambiguous on the audited key. Holdat does **not** survive for
this sketch: 0 inscriptions are joinable to catalogue object
types, and Holdat carries no object-type field. A Stage 2 freeze
for (a) must restate the test on these joined populations; the
sketch as drafted over "a text layer" generally does not
survive.

**(b) Motif class × sign-sequence class — NO RECOMMENDATION is
made (per spec §3.5); the existence question Stage 0 may answer
is answered YES at the proposed scale.** Motif-bearing fields
exist: the catalogue's `motif_chapter` on 2,005 of 7,705 photo
rows (26.0%), covering 909 of 3,494 distinct objects; Holdat's
`iconography` on 7,002 of 7,002 token rows over 1,670
inscriptions, Class C with no verifiable coding provenance;
mayig's `description`, parseable but vocabulary-narrow (§5);
horus84's Class C `symbol` and `cult` fields. The image
population the pilot would draw on exists at the proposed
~100-object scale. Test (b) runs only if Stage 1 — approved in
principle, still requiring its separate post-Stage-0 go — passes
its §4.5 proceed gate. Stage 0 neither recommends nor forecloses
Stage 1 beyond these existence facts.

**(c) Site repertoire differentiation — SURVIVES as a coverage
proposition.** Site exists at inscription level in two text
layers. Holdat: 7,002 of 7,002 token rows over 1,670
inscriptions at 9 sites (per-site inscription counts, coverage
facts: Mohenjo-daro 606, Harappa 492, Lothal 124, Kalibangan
110, Dholavira 106, Chanhu-daro 78, Surkotada 61, Banawali 60,
Rakhigarhi 33). horus84 (lineage label mandatory): 5,679 of
5,679 rows across 77 distinct site values (Harappa 2,717,
Mohenjo-daro 1,923, Dholavira 238, Kalibangan 212, Lothal 208;
the remaining 72 values share 381 rows, including `Unknown`,
28). mayig reaches site only through the catalogue join (176 of
179, all Mohenjo-Daro). Whether the per-site populations support
any frozen test's minimum-cell rule is a Stage 2 freeze
question; Stage 0 records only that the fields and populations
exist as counted.

**(d) Pottery-graffiti repertoire patterning — SURVIVES ONLY as
the comparative, descriptive sketch the spec drafted.** In
hand: catalogue Graffiti photo rows 417 (Vol. 1: 119; Vol. 2:
298) over 395 distinct objects; the Kodumanal volume's prose
structure (§6); and the horus84 / Holdat type fields as the
machine-readable graffiti-adjacent material. **The Tamil Nadu
graffiti corpus itself is NOT in hand — 0 records** (access
requested 2026-10-08; no reply) — so no repertoire comparison
against that corpus can be computed from material in hand.
Boundary 4 stands: graffiti material is never pooled with seal
texts, and the dating-gap caveat (the Tamil Nadu material is
separated from the Indus material by ≥ 1,000 years on the
published rebuttal) attaches to any comparative output: a
permitted output is "resemblance measured"; a prohibited output
is any continuity, descent, or survival claim.

**Drift against the spec's drafting-time Appendix A** — three
items, all wording or arithmetic in the proposal text, none in
the underlying data: (1) horus84 carries **38** fields, not 39 —
Appendix A.4's own enumerated list names the same 38; the "39"
in the spec text is a miscount, corrected here on the record;
(2) the Met set's "4 inscribed seals" is wording — 4 stamp-seal
objects, only one titled with "inscription"; (3) the Cleveland
file is a 10-record search set (3 seals, 1 jar, 6 other types),
inventoried as acquired. One Appendix A figure is **NOT
RECOMPUTED**: Phase-124's 98.9% sample field accuracy (no new
hand sample was taken in Stage 0).

## 8. What this release deposits, and the limits that govern it

Deposited with v4.6.0, under the owner's adjudication (Decision
Ask 4): the Stage 0 inventory dataset
(`phase133_stage0_inventory.json`, with its provenance meta) —
the coverage matrix, join-key audit, and provenance grading as
machine-readable facts — under **CC BY 4.0**, through the
release gate recorded in `RELEASE_VALIDATION.json`. Facts only:
no images, no crops, and no restricted source material are
deposited at any point.

The governing limits, from Spec 024 §8, stand verbatim over
everything in this note and this deposit:

> Associations describe **use, not meaning**. A finding that a
> sign class clusters on tablets, or that a motif travels with
> a sequence class, is a fact about how the writing system was
> deployed — it is not evidence for what any sign sounds like,
> means, or refers to. **No result obtainable under this spec
> can mint, promote, demote, or validate any sign reading,
> change any anchor's status, or move PRED-2026 in either
> direction.**

Stage 0 computed no associations at all. What it established is
tier (i) of the spec's honest tiering — verified statements
about what context data exists and how it joins. Whether the
motif pilot (Stage 1) proceeds is a separate owner decision,
informed by §7(b)'s existence facts and blocked on nothing else:
the coder basis was settled at the freeze.
