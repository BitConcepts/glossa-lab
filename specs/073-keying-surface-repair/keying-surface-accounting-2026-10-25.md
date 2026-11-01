# Keying-Surface Accounting — 2026-10-25 (programme red team, Cell C)

Appended to the Spec 073 record so the keying surface's shape is
stated in one place, in the form Spec 073 used for token 999.
Findings C-2, C-3, C-4, C-9 and C-7 of the 2026-10-25 programme
red team. All counts re-derived from the committed files
(Registry v2 SHA 42ab09fb…, Asset A v2 SHA 681e017d…, and
`reports/phase441_results.json` SHA f55ae911…).

## The three key spaces do not compare directly

- **Population signs** (Spec 075): 557 Wells numeric codes.
- **Asset A v2 rows**: 552 = 341 P-keys + 210 W-keys + 1 M-key
  (M059).
- **Registry v2 rows**: 1,013 = 396 parpola_1982 + 407
  yajnadevam_glyphid + 210 icit_wells.

"557 signs, 552 rows, five missing" is a category error. Exactly
**one** population sign has no Asset A row: **token 999** (2
primary rows, 2 occurrences), already named in
`registry-v2/no-published-identity.json`.

## What the keying actually did (Spec 075)

- 556 keyed signs → **424 distinct Asset A rows** (423 leg-1 signs
  → 291 rows; 133 leg-2 signs → 133 rows).
- **67 Asset A rows serve more than one population sign**,
  covering 199 signs and 3,399 of 11,322 identified-kind
  occurrences (30.0%). Exposure by kind (occurrences on
  multi-sign rows ÷ kind total): human 451/978 = 46.1%; other
  2,591/7,006 = 37.0%; animal 298/1,179 = 25.3%; object_goods
  59/2,159 = 2.7%. Largest groups: P205 ← 13 signs; P086 ← 418
  occurrences; P306 ← 8 signs; P186 ← 8 signs.
- **Distinct-row census** (member signs → distinct Asset A rows
  represented): other 307 → 204; human 53 → 39; animal 39 → 29;
  object_goods 24 → 19; unidentified 133 → 133.
- All 133 leg-2 signs are keyed to W-key rows with empty
  `depicted_label_verbatim` and empty `governing_source` — keyed
  for joining, honestly unclassified (as Spec 073's outcome
  states). 23.9% of the keyed population was never classifiable
  by this surface.

## The inverse gaps (previously unnamed)

- **128 of 552 Asset A rows are keyed by no population sign**
  (77 W rows, 50 P rows, M059).
- **55 of Registry v2's 396 parpola_1982 rows have no Asset A
  v2 row at all** (including P101, P119). No current population
  sign keys to them; any future population that does will be
  unkeyable for a reason no record previously named. They are
  named here as a class; an exclusion schedule in 073's form is
  future registry work.

## Registry content classes (the "1,013 rows" headline)

Only the 396 parpola_1982 rows carry descriptions and crosswalk
data. The 407 yajnadevam_glyphid rows carry corpus frequencies
and positional rates but no identity fields; the 210 icit_wells
rows carry only sign_id / wells_ids. 65 Parpola rows have empty
`wells_ids`. Headline counts of registry rows should not be read
as counts of identified signs.

## Mahadevan-column collisions (C-2, C-3)

- 29 of 396 parpola_1982 rows carry more than one Mahadevan id;
  in 22 of the 67 multi-sign keying groups, the Mahadevan column
  splits the Parpola lump (extreme: P086 carries
  M161|M162|M167|M168|M169).
- **13 Mahadevan ids are claimed by two registry rows each:**
  M002→{P015,P016}; M050→{P043,P044}; M064→{P054,P055};
  M076→{P066,P071}; M161→{P085,P086}; M167→{P086,P101};
  M168→{P086,P100}; M099→{P119,P122}; M103→{P123,P139};
  M216→{P230,P234}; M264→{P260,P359}; M199→{P292,P293};
  M409→{P346,P348}. Kind consequence: M199 sits under
  P292 = object_goods and P293 = other — the same Mahadevan
  sign under two depicted kinds. M167 and M099 each also point
  at one row with no Asset A row (P101, P119).
- Any future spec keying through `mahadevan_ids` must resolve
  these 13 first, on the record. Adjudicating them (genuine
  many-to-one in Mahadevan's own list vs transcription error)
  is future registry work, not settled here.

## Canonical pin for the M77 raw text (C-7)

Three copies of `mahadevan_m77_raw.txt` exist on main. The two
distinct files differ by exactly one trailing empty line at EOF;
no freeze, spec pin, or committed result cites either hash.
**Canonical: `data/mahadevan_m77_raw.txt`, SHA-256 11441e38…,
673,943 B.** The other copies are duplicates of record, not
divergent data.

*What this accounting establishes: the keying surface's shape,
counts, and named gaps, from the committed files. What it does
not establish: that any grouping is wrong — Parpola's lumping
may be right; it establishes that the lumping is inherited,
unadjudicated per group, and was invisible to Spec 075's frozen
sensitivities.*
