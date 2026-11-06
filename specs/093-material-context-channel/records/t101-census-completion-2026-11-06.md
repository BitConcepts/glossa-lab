# Spec 093 Stage 1 — T101 census completion (2026-11-06)

This record completes the census the grounding inventory
(`records/grounding-data-inventory-2026-11-05.md`) started,
under claim C093-2 (the inventory is complete against its
named sources, by its amendment path) and C093-3 (the
snapshot's joint coverage as counted). Every count below was
computed from the pinned files by
`tools/spec093/stage1_census.py` on 2026-11-06; the script is
committed with this record and every count is recomputable
from the pins. Presence counting only: no statistic relating
a culture-side value to a sequence property is computed
anywhere in this census (hard constraint H1).

**Uniform EMPTY convention.** A value is EMPTY iff it is
None, an empty list/dict, or a string whose stripped form is
one of `''`, `'None'`, `'-'`, `'--'`. Presence counts use
this convention throughout; where a source's own missing
marker makes the raw and convention counts differ materially,
both are stated.

**Run identity.** These counts sit on no Spec 089 registered
surface (run-defs v2 §1's list is closed: settling /
experiment / study / suite), and registering one is out of
Stage 1's scope (C089-19). Like the grounding inventory
itself, this census is a counting pass identified by its
input pins and its committed script, not by a run id.

## 1. The pinned snapshot

`glossa-corpus/indus/exports/indus_research.jsonl`, SHA-256
`08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e`
(= the Spec 090 G1 pin): **15,508 records**.

| source_system | records |
|---|---|
| PennMuseum | 7,515 |
| MetOpenAccess | 4,904 |
| indusscript-m77 | 2,906 |
| mayig-cisi | 179 |
| ClevelandArtOpenAccess | 4 |

**Record shape.** Every record carries exactly 16 keys
(key-count census: `{16: 15508}`), and the key union over all
records is exactly those 16 — no record carries a field
outside the censused set. **Amendment A5** (see §8): the
grounding inventory's prose said "17 keys"; its own table
lists 16, and 16 is the count (amendments are collected in §8).

**Field presence** (of 15,508): `glossa_id`, `source_system`,
`rights_status`, `artifact_type`, `sign_instance_count`,
`crosswalk_coverage`, `_citation` — 15,508 each;
`current_holding` 12,423; `image_master_uri` 12,423;
`material` 11,839; `accession_number` 7,519 (PennMuseum
7,515 + ClevelandArtOpenAccess 4; 7,492 distinct values);
`site_name` 1,865; `text_code_diplomatic`,
`text_code_diplomatic_normalized`, `sign_id_scheme`,
`canonical_grapheme_ids` — 3,085 each (the text-bearing
population).

**Joint coverage (C093-3, re-counted).** The two populations
are disjoint on every culture-side field:

| co-presence | records |
|---|---|
| sequence ∧ site | 966 |
| sequence ∧ material | 0 |
| sequence ∧ holding | 0 |
| sequence ∧ accession | 0 |
| sequence ∧ image | 0 |
| material ∧ holding | 11,839 |
| material ∧ accession | 6,938 |
| material ∧ image | 11,839 |
| site ∧ accession | 899 |
| site ∧ holding | 899 |
| site ∧ material | 893 |
| holding ∧ image | 12,423 |
| holding ∧ accession | 7,519 |

**Sites.** `site_name` takes 6 distinct values overall:
Mohenjo-daro 887, Harappa 726, Sutkagen-Dor 184,
Chanhu-Daro 48, Lothal 19, Kalibangan 1. In the
sequence-bearing population (966 records, all
indusscript-m77): Mohenjo-daro 839, Harappa 110,
Chanhu-Daro 7, Sutkagen-Dor 6, Lothal 3, Kalibangan 1. The
remaining site-named records are PennMuseum objects (899):
Harappa 616, Sutkagen-Dor 178, Mohenjo-daro 48,
Chanhu-Daro 41, Lothal 16. **Holdings** take 3 distinct
values: the Penn Museum (Philadelphia), the Metropolitan
Museum of Art (New York), the Cleveland Museum of Art.

**Artifact type is degenerate in the snapshot**
(`seal` 10,072 / `unknown` 5,436; by source — seal: Penn
3,565, Met 3,419, m77 2,906, cisi 179, Cleveland 3; unknown:
Penn 3,950, Met 1,485, Cleveland 1). **Confirmed gap**
(Stage 1 plan): the snapshot carries no usable per-record
artifact typology, and no period field at all; §5's CSV is
the only in-repo per-object typology/period source. These
absences are register-bound gaps (Stage 6), not patched here.

**Rights by source:** Penn CC BY 4.0; Met and Cleveland CC0;
indusscript-m77 `rmrl-research`; mayig-cisi MIT.
**Sign-id schemes:** Mahadevan1977 2,906; Parpola1982 179.
**Crosswalk coverage** equals 1.0 on 2,907 records
(m77 2,905, cisi 2).

**Sequence bookkeeping (counting facts about the record
system).** 635 of the 3,085 sequence records carry the
eroded token `000` in their diplomatic code, and exactly
those 635 are the records whose `sign_instance_count`
differs from both their grapheme-list length and their
code-token count: the count field deterministically counts
tokens EXCLUDING `000`. Exactly one sequence record has
count 0: `GLI-IND-M77-03080`.

## 2. The canonical store — a source the inventory missed

`glossa-corpus/indus/canonical/objects.jsonl`, SHA-256
`e24f42a95ee4cc1fdb16c789c3edfb937993ed7c82223d6daa96d66895174ae5`:
**19,925 records, 22 fields**. The snapshot's ids are a
strict subset. The 4,417 canonical ids NOT in the snapshot
are **all MuseumsOfIndia** — an entire sixth source
population the research export excluded
(`exports/export_report.json`: canonical 19,925 → research
export 15,508 with 4,417 rejected; open export 5,087 with
14,838 rejected). **Amendment A1** (§8).

Fields the export dropped, censused here from the canonical
store: `dimensions_mm` (free-text dimension strings despite
the name; present Met 4,253, Penn 1,605) and
`source_object_id` (present on all 19,925; the key field
T103's join design turns on — its per-source namespaces are
censused in the join record) reach the census only here, as
does `_source_extra` (present on all rows), the per-source
raw subfields:

- **PennMuseum** {title, culture, provenience}:
  provenience present 7,515, non-empty 7,421, 672 distinct;
  the most common are NOT Indus sites ('Iraq,Ur' 706, 'Iraq'
  445, 'Iraq,Nippur' 425, 'Iraq,Tepe Gawra' 406, 'Near East'
  344, 'Egypt' 312); the 899 records that also carry
  `site_name` are the Indus-site subset. Culture non-empty
  2,164.
- **MetOpenAccess** {title, culture, department,
  is_public}: culture values are mostly non-Indus
  ('Sasanian' 478, empty 2,583, 'BMAC' 156, 'Gandhara' 149,
  'Babylonian' 115, 'Minoan' 110).
- **ClevelandArtOpenAccess** {title, culture,
  share_license}; **MuseumsOfIndia** {title, description
  (4,382 non-empty), search_terms}; **indusscript-m77**
  {textnum, doc_count, fs80, level} (`fs80` is an unexplained
  integer field, not an object key); **mayig-cisi**
  {source_file, raw_signs}.

`pipeline_stage` is 'normalized' and `review_state`
'unreviewed' on all 19,925 rows; `quarantine_reason` is
present on 0. **The museum-side populations are general
collection slices** taken by the acquisition passes, not
Indus-only sets — provenience and culture censuses above,
and the export's own rejection counts, establish this; it is
why a museum accession was never an Indus-site fact in this
census and why T103's K1 family fails the way it does.

## 3. The other exports

**Open export** (`exports/indus_open.jsonl`): 5,087 records,
12 fields, ids a subset of the snapshot's; `site_name`
presence 0 (redacted out); sequences retained only for the
179 mayig-cisi records.

**ICIT-format export** (`exports/indus_icit_format.json`): a
dict whose `sequences` list holds 3,085 entries with keys
{artifact_type, glossa_id, icit_text, rights_status,
sign_count, sign_id_scheme, site_name, source_system}.

**Flat files.** M77 `reports/mahadevan_corpus_flat.txt`,
SHA-256 `878fd223…` (the standing pin): 1,669 lines, 5,361
tokens, 64 distinct codes, maximum code 920. ICIT
`reports/icit_corpus_flat.txt`, SHA-256 `c8839fd3…`: 4,410
lines, 14,213 tokens, 713 distinct codes, maximum code 958.
Both are bare sign-code lines with NO per-line object
identity — positional only; neither can carry culture-side
fields.

## 4. The CISI backend corpus and findspots

`backend/glossa_lab/data/indus_cisi_corpus.json`, SHA-256
`f9633c70…`: 179 inscriptions; per-inscription fields {id,
site, description, signs, n_signs} present on all 179;
`site` is the constant 'M'. The header carries 1,003 sign
tokens, 182 distinct signs, Parpola allograph numbering.
**Amendment A4:** `description` is a motif/type note per
inscription (e.g. 'unicorn I seal') — an iconography-adjacent
field the snapshot dropped; it is censused here as a field,
and no Stage 1 act consumes its content.

`backend/glossa_lab/data/cisi_findspots.json`, SHA-256
`42fc4c41…`: a CISI site-prefix → findspot map sourced from
CISI Vol 3 Part 3 (Desset ed. 2022) — 24 Vol-3.3 prefixes
(entry fields site/country/region/is_contact_zone/
n_seals_in_volume), 7 core Indus prefixes, and 4
Mesopotamia/Dilmun external prefixes. **Amendment A3** (the
inventory did not name this file). CISI discipline: this
census reports the file's structure and counts only;
nothing from CISI scans is reproduced anywhere in Stage 1.

## 5. The CISI data-list compilation — the big missed source

`backend/glossa_lab/data/yajnadevam_inscriptions.csv`,
SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`:
**5,679 rows × 38 fields**, a third-party compilation of
the CISI data lists. It is the ONLY in-repo source carrying
material + site + period + typology per text-bearing object,
and the grounding inventory missed it entirely.
**Amendment A2.**

Field presence (uniform EMPTY convention; the file's own
missing marker is `'-'` — e.g. `material` is non-blank on
5,679 rows raw and 4,706 after the convention removes 973
`'-'` values): id 5,679; cisi 5,018 (4,074 distinct; 1,871
rows M-prefixed; 661 rows carry no catalogue number);
region 5,679; site 5,679 (77 distinct — Harappa 2,717,
Mohenjo-daro 1,923, Dholavira 238, Kalibangan 212, Lothal
208, Chanhu-daro 74, Nausharo 38, Unknown 28, and a 69-site
tail); area-section 4,260; block-house 1,513; room-grid
2,191; excavation-idno 5,147; time 3,067; period 2,318 (a
mixed vocabulary: 'Late' 329, 'Intermediate' 425, 'Early'
49, and numeric codes '3' 1,027, '2' 190, '4' 41, '5' 44,
'6' 37); phase 2,652; depth 5,679; boss 1,512; material
4,706 (23 distinct values: Steatite 2,633, Clay 960,
Faience 619, Copper 264, Terracotta 78 and 'terracotta' 14,
Stoneware 40, Ivory 37, Ceramic 22, Stone 10, and a tail);
color 2,008; shape 4,376; cross-section 2,113; preservation
5,670; symbol 2,512; cult 1,457; type 5,679 (a real artifact
typology: SEAL:S 1,777, TAB:B 1,108, TAB:I 952, POT:T:g 538,
SEAL:R 388, TAB:C 230, TAG 172, SEAL 82, and a tail); sides
5,679; condition 5,666; complete 5,679; dir. 4,903; class
5,679; text length 5,679; signs 5,679; dimensions h 2,592 /
v 2,499 / th 1,049 as text and horizontal(mm) /
vertical(mm) / thickness(mm) 5,679 each as numbers; text
5,679; notes 47.

**Named and never consumed:** the columns `sanskrit` (3,823
present) and `translation` (1,761 present) are the compiling
third party's claimed-readings layer — contested content,
named here because the census is complete against its
sources, and used by NO Stage 1 act (the join consumes
data-list fields only; hard constraint H1 and the freeze's
§7 bound). Provenance/restriction: the metadata columns
trace to the CISI data lists; under the standing CISI
restriction their statistics are publishable and no scan is
involved.

## 6. Contact zone and comparanda seed sources

`glossa-corpus/indus/sources/contact-zone-rebuilt-2026-10-25/`:
**seals_at_mesopotamia.json** — 14 rows × 13 fields
(`indus_signs` present on 11; the `catalogue_ids` are
holding-collection ids such as AO_22310, BM_122187_UR_seal_1
— no overlap with CISI M- ids, censused as a fact for the
join design); **meluhha_tablets.json** — 1,462 hits × 10
fields (collection 1,367, designation 1,460,
primary_publication 1,460, the rest full);
**laursen_2010_table1.json** — 121 rows × 12 fields
(gulf_type, provenance, reference, seal_no, site on all 121;
dia 117, th 93, grooves 85, boss_dia 82, dh 74,
al_sindi_1999_no 46, bbm_no 25; aggregate
n_inscribed_with_indus_text 28; NO sequence field per row).

**Corpus catalogue** (`backend/glossa_lab/corpus_catalogue_seeder.py`,
CATALOGUE parsed, not executed): 39 entries × 12 fields
(id, name, language, language_family, script_type, period,
tokens_approx, source_url, license, description,
is_undeciphered on all 39; **local_module on 12 —
Amendment A6**: the inventory's field list did not name it).

## 7. Acquisition batches

`glossa-corpus/indus/sources/batch_*.json` (8 files) plus
`master_acquisition_2026-05-14.json` are acquisition
MANIFESTS — wrapper {batch_id, source, timestamp, results}
where `results` is a summary dict, not records
(**Amendment A7**: they are dispositioned as manifests, not
censused as populations). Salient summary facts: penn —
total_rows 474,538, indus_rows 19,711, checksum `814a45ed…`;
met — csv_indus_rows 8,250, api_supplement 45, total_objects
8,295, checksum `af25989d…`; cleveland — objects_fetched
10, checksum `51e5fa70…`; mayig — json_files_found 582,
inscription_candidates 0, success true; indian-culture —
pdfs 0 of 0; internet-archive — page_images_fetched 0;
rmrl — bulletins/portal pages only. **Provenance anomaly,
one line:** the museums-of-india batch reports all four
searches 'FAIL', yet the MuseumsOfIndia population exists
in the canonical store (§2) — how it arrived is not
recorded in the batch. The raw per-object captures live
OUTSIDE the repo (the manifests' local_path values point at
the owner's desktop); their culture-side content reaches
this census only through the canonical store's
`_source_extra`, censused in §2. Also dispositioned by
inspection, not census: `iconographic_anchors.json` (a
Parpola-2010 anchor dossier — sequence-side interpretive
material, not an object-metadata source); the
Mahadevan↔Parpola crosswalk files (SIGN crosswalks, not
object concordances); `mesopotamian_contact.py` (a loader
over §6's files — same data, no new population).

## 8. Amendments to the grounding inventory (C093-2)

- **A1** — The canonical store is a source population in
  its own right (19,925 records incl. the whole
  MuseumsOfIndia population and the fields the export
  dropped: dimensions_mm, source_object_id, _source_extra).
- **A2** — The CISI data-list compilation (5,679 × 38) was
  missed entirely; it is the only in-repo per-object
  material/site/period/typology source for text-bearing
  objects.
- **A3** — The CISI findspots map was not named.
- **A4** — The CISI loader corpus carries per-inscription
  `description` (motif notes) and `site` fields the
  snapshot dropped.
- **A5** — The snapshot's record key count is 16, not 17.
- **A6** — The corpus catalogue carries a 12th field
  (`local_module`, 12 present).
- **A7** — The acquisition batches are manifests (summary
  dicts), not record populations.

*This does not establish:* that the census's sources are
all the culture-side data in the world — only completeness
against the named sources. (T101's line, carried verbatim.)
