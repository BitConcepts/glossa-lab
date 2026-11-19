# Spec 093 Stage 2 — T201 channel definition (2026-11-19)

The material-context projection, defined against G1
§2.1's state, under Stage 1's vocabularies, over named
populations, with the bookkeeping feature set the
prediction test may use — each stated so a second worker
can implement from this definition alone. Every count
below is recomputed from the pinned files by
`tools/spec093/stage2_counts.py`; the machine output is
`records/t201-counts-2026-11-19.json`. Presence counting
only: nothing in this record relates a culture-side
value to a sequence property.

## 1. The definition against G1 §2.1

G1 §2.1 (Spec 090's G1 document,
`specs/090-projected-constraints-generalization-study/records/g1-document.md`)
defines a candidate state as a four-tuple
s = (Σ, γ, ρ, λ), and §2.2 defines the projection
π(s) = T(s): the sequence table assigning to each object
o in the object set O the sequence γ(o) that the state's
glyph classification produces for o's glyph stream.
Every further record the state determines on the text
side — token counts, sign frequencies, positional
statistics — is a function of T(s), not an addition to
the projection.

**The material-context channel is the second map the
same state determines:** for each object o, the tuple

    μ(o) = (site, material class, artifact type,
            holding/provenance, find context)

of the object's recorded culture-side values, under the
vocabularies §2 registers. The historical state that
fixed o's text also fixed where o was deposited, what o
is made of, what kind of object o is, where o is held,
and where o was found; the record system holds those
values through different hands and different derivations
(museum cataloguing, excavation records, published data
lists) than the coded corpora that carry π. C093-1
asserts that μ is not a function of the pair
(T(s), bookkeeping): no rule statable in advance of
Stage 2's freeze computes μ(o) from o's sequence table
entry together with the record system's bookkeeping
about o. T202's freeze administers exactly that
assertion, per field (D-093-3).

The operative object set is the pinned corpus
snapshot's record set (§3). An object the snapshot does
not carry stands outside this stage's μ as it stands
outside its π (G1 §2.2's operative reading).

## 2. The five fields, as recorded

The empty convention is the Stage 1 census's: a value
is empty iff it is null, an empty list or dict, or a
string whose stripped form is one of '', 'None', '-',
'--'. A record carries a sequence iff its
`canonical_grapheme_ids` list is non-empty (3,085
records; the census's text-code definition counts the
same 3,085).

1. **Site** — the snapshot's `site_name`, as recorded.
   On the sequence-bearing population it is present on
   966 records, all of source system indusscript-m77,
   with six recorded values: Mohenjo-daro 839, Harappa
   110, Chanhu-Daro 7, Sutkagen-Dor 6, Lothal 3,
   Kalibangan 1.
2. **Material class** — recorded in two forms. The
   snapshot's `material` (museum side; the T102 register
   normalizes its 1,122 distinct values) is present on
   **0** sequence-bearing records (C093-3). The form
   that co-occurs with a sequence is the CISI data
   list's material value, carried on the Stage 1 join
   output as `material_raw`. On the joined population
   (§3) it is present on 178 of 179 pairs: Steatite 176,
   Clay 1, Faience 1. **Bound, stated on the face:** the
   T102 register is bound to the snapshot's values and
   does not cover the data list's (T103 audit record
   §5); this stage takes the field as recorded in the
   data list. Normalizing the joined values is a
   successor-register act that belongs to Stage 4, not a
   definition this stage may improvise.
3. **Artifact type** — the snapshot's `artifact_type`,
   as recorded. It is present on all 3,085
   sequence-bearing records and takes exactly one value
   there: 'seal' (3,085 of 3,085). On the joined
   population the data list's `type` concurs in family
   on all 179 pairs ('SEAL:S'; T103 audit §3's type
   consistency check).
4. **Holding/provenance** — the snapshot's
   `current_holding`, as recorded. It is present on
   **0** sequence-bearing records; the joined pairs
   carry no holding on either side (snapshot side
   present 0 of 179). The field is defined over the
   snapshot's museum populations, which carry no
   sequences.
5. **Find context** — the CISI data list's
   `area_section`, carried on the join output: the
   excavation area within Mohenjo-daro under which the
   data list files the object. Present on 175 of 179
   pairs, 17 recorded values (largest: DKG. (S) 68,
   DKG. (N) 17, DK- 16, HRB 13, VSA 11). The finer
   recorded value `excavation_idno` is named here and
   excluded from the field's vocabulary: it takes 178
   distinct values over the 179 pairs — an identifier
   for the object, not a context class a channel could
   carry.

## 3. The named populations

- **P-seq** — the snapshot's sequence-bearing records:
  3,085 (indusscript-m77 2,906; mayig-cisi 179).
  Snapshot: `glossa-corpus/indus/exports/indus_research.jsonl`,
  SHA-256 `08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`
  (the pin Spec 090's G3 freeze also carries).
- **P-site** — P-seq records carrying a site: 966, as
  §2.1 counts. Site is administered over this
  population.
- **P-join** — the Stage 1 join's output:
  `records/t103-join-pairs-v1.jsonl`, 179 pairs,
  SHA-256 `7107f738832a4e3b04cff91d81073212bc0f3a77afed6f0ccc3cee4fce621703`,
  each pair joining a mayig-cisi text record (by
  `text_id` = the snapshot record's `glossa_id`; all 179
  found, all 179 sequence-bearing) to its data-list
  fields under key family K2, accepted at precision
  1.000 against the freeze's 0.90 floor (T103).
  Material class, artifact type, and find context are
  administered over this population, as §2 defines them.

No other population carries a sequence and a
culture-side field jointly; the copresence counts are in
the counts file (sequence ∧ site 966; sequence ∧
material 0; sequence ∧ holding 0; sequence ∧
accession 0).

## 4. Bookkeeping — the feature set's boundary

The prediction test may use, beside the sequence table
itself, only bookkeeping: facts about the record's
derivation inside the record system. The bookkeeping
feature set is exactly these four recorded fields:

- `source_system` — the corpus the record derives from;
- `sign_id_scheme` — the numbering the record's codes
  are stated in;
- `rights_status` — the record's stated rights class;
- `crosswalk_coverage` — the record's stated crosswalk
  coverage, as recorded.

Everything computed from `canonical_grapheme_ids` —
length, sign inventory, sign counts, positional facts —
is table-side: a function of π, part of what the test
predicts *from*, never bookkeeping and never channel
data. A culture-side field is never a feature for any
field's test, including its own. On P-site all four
bookkeeping fields are constant (indusscript-m77 /
Mahadevan1977 / rmrl-research / 1.0, on all 966) — the
site test is therefore a test of the table alone, which
the freeze states. On P-join the first three are
constant (mayig-cisi / Parpola1982 / MIT) and
`crosswalk_coverage` varies.

## 5. What this definition makes askable

Per field, the Stage 2 question is now statable: over
the field's named population, can the field's recorded
value be recovered from the object's table entry plus
the §4 bookkeeping, by a predictor frozen before its
administration, at or above a frozen bar, on held-out
objects, against permutation controls? Which fields can
be administered at all — and which cannot, at what
forcing counts — is T202's freeze to state under its
frozen floors, from §2's and §3's counts.

*This does not establish:* that the channel is
independent — that is T202's question, and this task
only makes it askable. (T201's line, carried verbatim.)
