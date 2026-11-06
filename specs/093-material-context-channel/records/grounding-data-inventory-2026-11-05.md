# Grounding — culture-side data inventory (2026-11-05)

**What this record is.** The data inventory this package's
design rests on: for each named in-repo source, which
culture-side fields actually exist, verified by inspection,
with counts where the record supports them. Counted and read
first-hand from the repository on 2026-11-05 (counting pass
over the files named; file identities re-verified against
their pins where pins exist).

**Method, and its limit.** The counts below are counts of
field *presence* and *co-presence* (how many records carry a
non-empty value in a field, and in two named fields at
once). No statistic relating a culture-side *value* to a
sequence *property* was computed for this inventory: no
association, correlation, conditional distribution, or
pattern of any kind. Presence counting is the inventory act
the G1 document itself performed over this snapshot (its
§1.1/§1.5 census lines); pattern computation is the study's
Stage 4, which this draft does not pre-run.

---

## 1. The corpus snapshot — the primary source

`glossa-corpus/indus/exports/indus_research.jsonl`
(canonical SHA-256
08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e;
G1 §1.5's Class V pin): **15,508 object records**. Every
record carries the same 17 keys: `glossa_id`,
`source_system`, `rights_status`, `artifact_type`,
`site_name`, `current_holding`, `material`,
`text_code_diplomatic`, `text_code_diplomatic_normalized`,
`sign_id_scheme`, `canonical_grapheme_ids`,
`sign_instance_count`, `crosswalk_coverage`,
`image_master_uri`, `accession_number`, `_citation`.

Non-empty values, counted 2026-11-05 (of 15,508):

| field | non-empty | note |
|---|---|---|
| `artifact_type` | 15,508 | degenerate: `seal` 10,072, `unknown` 5,436 — no other value exists |
| `material` | 11,839 | free-text museum strings (see §1.2) |
| `current_holding` | 12,423 | exactly the museum-source records |
| `image_master_uri` | 12,423 | the same 12,423 |
| `accession_number` | 7,519 | PennMuseum 7,515 + 4 |
| `site_name` | 1,865 | 12.0% of records |
| `sign_id_scheme` | 3,085 | Mahadevan1977 or Parpola1982 |
| `text_code_diplomatic` | 3,085 | the sequence-bearing records |
| `canonical_grapheme_ids` | 3,085 | the same 3,085 |

Source systems: PennMuseum 7,515; MetOpenAccess 4,904;
indusscript-m77 2,906; mayig-cisi 179;
ClevelandArtOpenAccess 4. `rights_status` values across the
file: CC BY 4.0, CC0, MIT, rmrl-research.

### 1.1 The disjointness — the inventory's central fact

Per source system, which sides of the record each population
carries:

| source | n | sequence | site | material | holding |
|---|---|---|---|---|---|
| indusscript-m77 | 2,906 | 2,906 | 966 | 0 | 0 |
| mayig-cisi | 179 | 179 | 0 | 0 | 0 |
| PennMuseum | 7,515 | 0 | 899 | 6,934 | 7,515 |
| MetOpenAccess | 4,904 | 0 | 0 | 4,901 | 4,904 |
| ClevelandArtOpenAccess | 4 | 0 | 0 | 4 | 4 |

Co-presence over the whole snapshot, counted:

- sequence ∧ site_name: **966 records** (all indusscript-m77)
- sequence ∧ material: **0 records**
- sequence ∧ current_holding: **0 records**

The snapshot's text-bearing population and its
metadata-bearing population are disjoint except for site,
and for site only inside the m77 subset. Any material-side
question over sequences therefore cannot be answered from
the snapshot alone: it needs a join (accession number /
holding / catalogue identity) between the museum records
and a text-bearing source, or it must abstain. This is a
fact about the record system, stated before any design
rests on it; the package's Stage 1 join design and Stage
4's floors exist because of it.

### 1.2 Field-quality findings

- **`material` is not a class field.** Its distinct values
  are raw museum strings (e.g. "Agate, banded gray white",
  composite lists like "Agate,Carnelian,Steatite",
  uncertainty markers "(?)" / "(uncertain)") and include
  values that are not materials at all (date-like strings
  and fragments, e.g. "-2300", "1800 - 1900 CE"). No
  material-side pass may consume this field raw; a
  normalization to a registered material-class vocabulary
  is Stage 1 work, and the normalization rules are part of
  what a pass's freeze must pin.
- **`artifact_type` carries one bit.** seal vs unknown,
  nothing else: no tablet / pottery / copper-plate /
  other-object distinction exists in the snapshot. The
  owner's "what things had what written on them" question
  cannot be asked of this field beyond that one bit; an
  artifact-typology source is a named inventory gap (§5).
- **Site coverage inside the sequence-bearing subset is
  thin and lopsided.** Of the 966 site-named m77 records,
  6 distinct site names occur: Mohenjo-daro 839, Harappa
  110, Chanhu-Daro 7, Sutkagen-Dor 6, Lothal 3, Kalibangan
  1. A held-out-site arm has exactly one viable second
  site (Harappa, n=110); the remaining four cannot carry
  a replication arm at any honest floor.
- **The mayig-cisi subset (179) carries sequences only**
  in the snapshot: no site, material, or holding. Its
  Mohenjo-daro-only provenance is known from its loader
  (G1 §1.2), not from its snapshot rows. CISI discipline
  (§4) governs any use.

## 2. The coded corpora — sequence side only

- **M77 flat file** (`reports/mahadevan_corpus_flat.txt`,
  SHA-256 878fd223…; G1 §1.2): 1,669 inscriptions, 5,361
  tokens, 64 codes. Lines are sequences only — no
  per-inscription site, material, or object field exists
  in the file. Joining M77 lines to snapshot objects is a
  crosswalk question, not a field read.
- **ICIT flat file** (`reports/icit_corpus_flat.txt`,
  SHA-256 c8839fd3…; G1 §1.2): 4,410 inscriptions, same
  shape — sequences only.
- **CISI coded subset** (loader of record
  `backend/glossa_lab/data/indus_cisi.py`; G1 §1.2): 179
  inscription sides, Mohenjo-daro only, Parpola P-codes.
  Derived from restricted material; §4 governs.

## 3. The contact-zone rebuild — the transmission side, in data

`glossa-corpus/indus/sources/contact-zone-rebuilt-2026-10-25/`
(rebuild provenance in the directory's own
`contact_zone_rebuild_provenance.md` / `provenance.yaml`):

- **`seals_at_mesopotamia.json`** — 14 rows. Fields:
  `catalogue_id`, `type`, `find_spot`, `find_country`,
  `find_period`, `field_provenance`,
  `current_collection`, `indus_signs`,
  `inscription_length`, `inscription_reading`,
  `signs_confidence`, `signs_source`, `source`. This is
  the documented-contact channel in data form: Indus
  seals excavated at Mesopotamian sites, with find
  context and the inscription as read by its source.
  n=14 is an evidence class, not a population; no
  statistical pass may rest on it alone.
- **`meluhha_tablets.json`** — 1,462 hit rows over
  Mesopotamian textual sources. Fields: `p_number`,
  `designation`, `collection`, `provenience`, `period`,
  `primary_publication`, `matched_keywords`,
  `atf_excerpt`, `atf_lines_with_match`. The documentary
  record of the Meluhha contact, with period and
  provenience per hit — comparanda-register grounding for
  the Mesopotamian window (Stage 3).
- **`laursen_2010_table1.json`** — 121 rows parsed.
  Fields: `seal_no`, `site`, `provenance`, `gulf_type`,
  `dia`, `th`, `boss_dia`, `grooves`, `reference`,
  `al_sindi_1999_no`, `bbm_no`; top-level aggregates
  `by_gulf_type`, `by_site`, `n_inscribed_with_indus_text`.
  Seal typology and metrology for the Gulf/Dilmun seal
  population — the intermediate form between Indus and
  Mesopotamian sealing practice. **No sequence field
  exists in any row** (verified by key inspection, as the
  G3 draft verified): Laursen enters this spec as a
  culture-side population in its own right and as
  comparanda grounding, never as a sequence source.
  Laursen is a private author copy in the program's
  custody chain (never in git in its original form; the
  rebuilt table is the in-repo artifact) — see §4.

## 4. Restrictions that bind this inventory

- **CISI.** Page scans are restricted material: held only
  on the owner's machines, never redistributed; statistics
  computed from them are publishable (G1 §1.1 custody
  rule). The publisher (Finnish Academy of Science and
  Letters, email to the owner 2026-11-04) confirms: no
  digital edition of CISI exists or is planned; text not
  explicitly marked copyrighted may be used in academic
  contexts with appropriate referencing (the data lists
  included); reproduction of a photograph of an individual
  object requires the owner/museum's and the
  photographer's (or commissioning project's, e.g. CISI
  or HARP) permission. Andreas Fuls is never contacted
  (standing bar, reaffirmed 2026-11-05).
- **Laursen.** The author copy is private and never enters
  git; the rebuilt Table 1 (§3) is the usable artifact.
- **Snapshot rights.** Per-record `rights_status` travels
  with the record; the rmrl-research population's terms
  govern its own rows.

## 5. What the inventory does not hold (named gaps)

1. **No ductus / writing-style field anywhere.** No
  in-repo source records how a sign was executed (carved,
  incised, molded, brush) per inscription, beyond what
  material + source-system imply. The owner's
  writing-style arm has no data field today; it is a gap
  entry, not a pass.
2. **No iconography field.** The snapshot carries no
  motif/iconography coding for the 10,072 seals (the
  Laursen rows carry typology, not motif). A motif layer
  would be new coding work with its own independence
  problem (the coder must not see the readings), not an
  inventory read.
3. **No artifact typology beyond seal/unknown** (§1.2).
4. **No period/phase field in the snapshot.** Dating
  enters only through source-level knowledge (e.g. find
  periods in `seals_at_mesopotamia.json`) and the
  comparanda register, not through per-record fields.
5. **The corpus catalogue is not object metadata.** The
  backend's `corpus_catalogue` (seeder:
  `backend/glossa_lab/corpus_catalogue_seeder.py`, the
  CATALOGUE list, 39 entries; the lineage census of
  2026-11-05 counted the live table's 39 rows identical
  across both custody snapshots) catalogues *corpora of
  world scripts* — fields: name, language,
  language_family, script_type, period, tokens_approx,
  source_url, license, is_undeciphered. It is not a
  per-object source; its role in this spec is as the
  seed population for the comparanda register (Stage 3):
  39 named script corpora already carrying period and
  script-type fields (e.g. Linear A 1800–1450 BCE,
  Proto-Sinaitic 1900–1500 BCE, Meroitic 300 BCE–400 CE,
  Rongorongo, Zapotec 500 BCE–700 CE).

## 6. The existing machinery this spec extends

- **Ledger** (`glossa-indus/ledger/claims.jsonl`): the
  append-only claims ledger, Spec 086's sole entry
  point. At the closeout of Spec 089 it stood at 943
  lines / 912 claims (bundle 889 + extracted 23); the
  exact count at this spec's adoption is re-counted by
  the adoption task, not assumed from this line.
- **Matrix** (`glossa-indus/matrix/matrix.json` +
  `matrix.md`, with `DEFINITIONS.md`): generated from
  the ledger by `tools/ledger/generate_matrix.py`; never
  hand-edited.
- **Program map** (`glossa-indus/map/program-map.json`,
  `program-map-taxonomy.json`, `program-map.html`,
  `PROGRAM-MAP-DEFINITIONS.md`): generated layers citing
  ledger ids; taxonomy carries domains / subdomains /
  studies.
- **Gap register** (`glossa-indus/map/gap-register.md`):
  Spec 088's 37 entries GR-088-01…37, each with falsifier
  and honesty-rule type, completeness mechanically
  checked (51 checks at ratification).
- **Gate** (`backend/glossa_lab/ledger_gate.py`, V1..V11
  at Spec 089 closeout; standing profile full 29 PASS /
  0 FAIL / 1 NOT-RUN, --regen 32 PASS / 0 FAIL / 0
  NOT-RUN): verifies the one-way flow ledger → matrix →
  map on every publication path.
- **Runs** (Spec 089): every computation is a run under
  run-defs v1 (`glossa-indus/ledger/RUN-DEFINITIONS.md`),
  cited by run id; divergences between comparable runs
  junction, never average.

**AI disclosure:** inventory counted and drafted by an AI
agent (Muse, via Muse) at the direction of Tristen
Pierson, per constitution sec. VI. Presence counts only,
per the method line above; no pattern over the corpus was
computed for this record.
