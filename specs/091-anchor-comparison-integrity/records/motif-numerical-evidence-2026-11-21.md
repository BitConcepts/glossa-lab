# Q5 item 5 — Motif and numerical evidence tables, replicated (2026-11-21)

**Workstream:** Round 2 of the weekend iteration executing the Co-scientist
audit adjudication, Q5 item 5: replicated, value-relevant motif and
numerical evidence with full contingency tables for the Indus strict-core
readings. **Venue:** tower-compute, fresh clone `~/glossa-work/r2-motif-a333`.
**Machine-readable companion:** `motif-numerical-evidence-2026-11-21.json`
(same directory). **Scripts:** `r2-motif-path-a-phase100.py` and
`r2-motif-path-b-phase114-mayig.py` (same directory).
**Effect:** evidence only. This record changes no standing, no ledger
entry, and no register value. Motif association strength is not a phonetic
identification, and nothing in this record claims any reading is
established. The Indus script remains undeciphered.

## 1. Headline outcome

- **Animal-motif claims (13 of 13): NOT REPRODUCIBLE FROM THE RECORDS.**
  The full 2x2 contingency tables (sign present/absent x motif
  present/absent) cannot be built from anything tracked in this
  repository, because no tracked file joins per-seal sign sequences to
  per-seal motif/iconography labels over the seal population. What is
  missing is named in section 2. The sign-side marginal of every table
  (how many seals bear the sign at all) WAS computed and replicated
  exactly (section 3); the motif-side cells do not exist in the record.
- **Numerical claims (3 of 3): WEAKENED.** The distributions are fully
  computable and replicated exactly (section 5), and they do not show a
  numerical pattern: counted/stroke-series contexts are not identifiable
  in the records, the corpus NUMERAL_FORMULA tag covers 1 to 2 of each
  sign's seals, and no sign is enriched in short inscriptions. A
  numerical ROLE is therefore not established by this evidence; the
  phonetic readings are a separate question this record does not touch.

## 2. What the corpus records actually contain (the missing join)

Every historical motif script in this repo (for example
`backend/scripts/phase261_coverage_recalc.py`,
`backend/scripts/phase54_falsification.py`) reads the motif from one
file: `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`
(the Holdat corpus, with an `iconography` column). That path is
gitignored (`corpora/` in `.gitignore`) and **absent from the
repository**; it was absent from this fresh clone. The tracked files
that do carry the 1,670-seal population carry no motif field:

| Tracked source | Seals | Signs | Site | Motif label | Object type / period |
|---|---|---|---|---|---|
| `outputs/phase100_full_corpus.json` | 1,670 | yes (M-numbers) | yes | **no** | object_type is the literal `?`; no period |
| `outputs/phase114_full_seal_translations.json` | 1,670 | yes (M-numbers) | yes | **no** | no |
| `data/corpus_layers/mayig_cisi_layer_v1.json` | 179 | yes (P-numbers) | no | description is unicorn-only (179 of 179 unicorn I to V) | no |
| `glossa-corpus/indus/exports/indus_open.jsonl` | 5,087 rows | partial (27 distinct canonical grapheme ids populated) | null | **no** | no |
| Phase-134 / Phase-135 pilot datasets (`data/evidence_integration/`) | 100 + 100 objects | **no sign sequences** | yes | adjudicated motif codes, yes | object_type yes |

The pilot datasets are the only tracked per-object motif coding, and
they cannot be joined to signs: they record CISI ids and motif codes
only. They are also, on the program's own record, a closed measurement
basis: Spec 024 Stage 1 ran twice (exact agreement 0.84, kappa 0.7885;
then 0.78, kappa 0.7129), the frozen proceed gate was not met either
time, and the motif arm was closed as run on 2026-10-09
(`specs/024-evidence-integration/motif-arm-closure.md`). Their
adjudicated compositions are recorded here descriptively only:
Phase-134 (100 objects): SCRIPT_ONLY 34, ILLEGIBLE 26, UNICORN 26,
GEOMETRIC 6, COMPOSITE 2, GOAT_ANTELOPE 2, ELEPHANT 1, TIGER 1,
BUFFALO 1, RHINOCEROS 1, ZEBU 0. Phase-135 (100 fresh objects):
SCRIPT_ONLY 38, UNICORN 30, ILLEGIBLE 10, GEOMETRIC 8, ELEPHANT 4,
GOAT_ANTELOPE 2, RHINOCEROS 2, TIGER 2, BUFFALO 2, HUMAN_CULT 2.
Gharial appears in neither pilot sample at all. A proportional sample
of this size cannot carry the rare-motif cells in any case.

**Breakdowns by site, period, and object type** (the audit's question
of whether a text might signify the animal, the owner, an office, a
place, or a commodity): site breakdowns of the sign marginals are
computable and are in the JSON companion for the numerical signs (and
were computed for all 16 signs in both paths). Period and object-type
breakdowns are **not supported by the records**: the population files
carry no period field and no usable object-type field. No control of
that kind is invented here.

## 3. Animal-motif tables: sign marginals (replicated) and verdicts

Population: 1,670 seals (both paths; see section 6). "Sign seals" is
the number of seals bearing the sign (each sign occurs exactly once per
bearing seal in this population, so tokens equal seals). The filed
basis for 12 of the 13 is the anchor file's summary assertion
"Exclusive to <animal> seals (lift > 5.0)"
(`backend/reports/INDUS_FINAL_ANCHORS.json`); no contingency table was
ever filed behind it. Because the motif column is absent, cells a, b,
c, d of each 2x2 table, and therefore lift and odds ratio, **cannot be
computed**; the table for every candidate is recorded as:

| Cell | Count |
|---|---|
| sign present, motif present (a) | NOT IN RECORDS |
| sign present, motif absent (b) | NOT IN RECORDS |
| sign absent, motif present (c) | NOT IN RECORDS |
| sign absent, motif absent (d) | NOT IN RECORDS |
| sign present, total (a+b) | see per-sign row below (replicated) |
| population total | 1,670 (replicated) |

| Sign | Reading | Filed motif | Sign seals (A = B) | Verdict |
|---|---|---|---|---|
| M006 | puli | tiger | 15 | NOT REPRODUCIBLE FROM THE RECORDS |
| M013 | nakaram | gharial | 23 | NOT REPRODUCIBLE FROM THE RECORDS |
| M016 | kaḷiṟu | elephant | 23 | NOT REPRODUCIBLE FROM THE RECORDS |
| M039 | āṉai | elephant | 18 | NOT REPRODUCIBLE FROM THE RECORDS |
| M045 | yānai | elephant | 24 | NOT REPRODUCIBLE FROM THE RECORDS |
| M057 | māṭu | zebu | 18 | NOT REPRODUCIBLE FROM THE RECORDS |
| M060 | kāṇṭāmirukam | rhinoceros | 20 | NOT REPRODUCIBLE FROM THE RECORDS |
| M062 | erutu | zebu | 28 | NOT REPRODUCIBLE FROM THE RECORDS |
| M063 | mutalai | gharial | 18 | NOT REPRODUCIBLE FROM THE RECORDS (see note) |
| M067 | kōṭṭāṉ | rhinoceros | 15 | NOT REPRODUCIBLE FROM THE RECORDS |
| M068 | maṟi | rhinoceros | 13 | NOT REPRODUCIBLE FROM THE RECORDS |
| M073 | kōṉ | zebu | 25 | NOT REPRODUCIBLE FROM THE RECORDS |
| M080 | vēṅkai | tiger | 19 | NOT REPRODUCIBLE FROM THE RECORDS |

**M063 note.** The filed correction (2026-05-11, in the anchor basis)
states M063 appears on 3 of 18 gharial-motif seals, with lift 4.35
against the original claim threshold of 5.0, and also 4 unicorn and
3 zebu-bull seals. This record verifies exactly one part of that
fragment: the total number of seals bearing M063 is 18, replicated by
both paths, which is consistent with the fragment's denominator if
the 18 is the sign total. The 3 / 4 / 3 split across motifs cannot be
checked, because the motif labels are absent. The filed lift of 4.35
is neither confirmed nor contradicted by anything in the repo.

**Competing-word structure.** The tables, had the labels existed,
would test motif association only, not which word is right. The
competing sets stand as filed and are untouched by this record:
tiger M006 vs M080; zebu M057 vs M062 (with M073 also claiming a zebu
association through a bull-to-king metaphor step, so its association,
if any, would not by itself pick the animal word over the office
word); elephant M016 vs M039 vs M045; gharial M013 vs M063;
rhinoceros M060 vs M067 vs M068 (M068's gloss is the generic
"young animal / calf", so a rhinoceros association for it would need
the same owner/office/place/commodity controls the audit asks for).
Multiple signs associating with one motif is compatible with several
structures (synonymy, register, office or commodity marking); an
association table alone does not decide between them.

**What would close this item:** deposit or re-derive, as a tracked
repo record, the per-seal iconography labels for the 1,670-seal
population joined on the same seal ids the sign files use (the Holdat
`iconography` column, or a fresh coding under a measurement basis that
meets its own gates), after which every table in this section is a
mechanical count. Until then the honest verdict stands as above.

## 4. (reserved)

## 5. Numerical tables (full counts, replicated)

Population controls (1,670 seals): inscription lengths 2:269, 3:330,
4:415, 5:330, 6:164, 7:116, 8:46 (no 1-sign seals in this population);
formula tags TITLE_FORMULA_SIMPLE 294, SUFFIX_ONLY 477,
OWNERSHIP_FORMULA 350, PLACE_FORMULA 182, UNCERTAIN 218, TITLE_ONLY
103, TITLE_FORMULA_ANIMAL 32, NUMERAL_FORMULA 14. Per-site population:
Mohenjo-daro 606, Harappa 492, Lothal 124, Kalibangan 110, Dholavira
106, Chanhu-daro 78, Surkotada 61, Banawali 60, Rakhigarhi 33.

| Quantity | M012 oṉṟu / 1 | M059 ēḷ / eḷ, seven | M391 ka / kaṇ |
|---|---|---|---|
| Seals bearing sign | 141 | 210 | 187 |
| Tokens | 143 | 222 | 193 |
| Seals with sign repeated | 2 | 12 | 6 |
| Max repeats in one seal | 2 | 2 | 2 |
| NUMERAL_FORMULA seals | 1 of 141 | 1 of 210 | 2 of 187 |
| Length 2 to 3 share | 43 of 141 (30.5%) | 52 of 210 (24.8%) | 42 of 187 (22.5%) |
| Population length 2 to 3 share | 599 of 1,670 (35.9%) | same | same |
| First-position share of its seals | 20.6% | 20.5% | 11.8% |
| Last-position share of its seals | 43.3% | 35.7% | 32.1% |

Full length distributions, formula distributions, and per-site counts
for all three signs are in the JSON companion. Reading of the tables:

- **M012 (filed: "single stroke = numeral 1").** The program's own
  Phase-54 prediction for a numerical sign was enrichment in short
  (1 to 3 sign) inscriptions. Measured: 30.5% of M012 seals are length
  2 to 3, BELOW the population rate of 35.9%, and there are no 1-sign
  seals in the population at all. Stroke-series behaviour is absent
  (repeats in 2 of 141 seals, never more than twice). The sign leans
  final (43.3% last position). **Verdict: WEAKENED.** The counts
  reproduce; a numerical role does not follow from them.
- **M059 (filed: "Numeral 7"; note the Phase-54 battery instead
  treated M059 as a person/owner marker, an internal inconsistency in
  the filed record).** Broad distribution (210 seals, every major
  site), NUMERAL_FORMULA on 1 seal, no stroke series (max repeat 2).
  **Verdict: WEAKENED** as a numerical claim: the distribution shows
  an ordinary, widely used sign, not a numeral pattern.
- **M391 (filed basis: "Numeral/stroke sign"; the Phase-54 battery
  treated it as a case-marker suffix).** SUFFIX_ONLY formula on 74 of
  187 seals and a final-position lean are the strongest pattern in
  its row, which points to the suffix behaviour, not a numerical one;
  NUMERAL_FORMULA covers 2 seals. **Verdict: WEAKENED** as a
  numerical claim.

For all three: quantity contexts (tallies, counted commodities) are
not labelled anywhere in the tracked records, so the counted-context
versus control comparison the audit frames cannot be run; what can be
run (length, position, repetition, formula, site) is run above. This
evidence bears on a numerical ROLE only; it neither establishes nor
refutes the phonetic readings oṉṟu, ēḷ, or ka/kaṇ.

## 6. Replication outcome

Two independently written paths, both run on tower-compute:

- **Path A** (`r2-motif-path-a-phase100.py`) over
  `outputs/phase100_full_corpus.json` (list of translations with
  formula tags). Payload verdict: exit 0, headline "n_translations
  1670" with per-sign counts as tabled.
- **Path B** (`r2-motif-path-b-phase114-mayig.py`) over the different
  representation `outputs/phase114_full_seal_translations.json`
  (dict keyed by CISI id, no formula field), written separately.
  Payload verdict: exit 0 on the final run. Its first run exited 1 on
  a null `text_code_diplomatic` in the auxiliary mayig-mapping leg
  only; the guard was fixed and the rerun is the run of record. The
  mayig leg itself returned no P-to-M mapping for M012 / M059 / M391
  (only 27 distinct canonical grapheme ids are populated in
  `indus_open.jsonl`), so it is recorded as a failed third leg and was
  not used for any count.

**Outcome: EXACT AGREEMENT on every computable count** — seals and
tokens for all 16 signs, per-site counts, inscription-length
distributions, first/last position shares, and repeat counts; zero
discrepancies (the comparison was computed and printed by the run).
For the motif cells there is nothing to replicate: no path can count
labels that are not in the records, and that absence, not a
disagreement between paths, is the finding of this workstream.

## 7. Discipline notes

Scripts were run on tower-compute only; each script's own exit code
is its payload verdict (wrapper success was not used as a verdict).
This record reports evidence only and moves no standing. No external
sends, no purchases, no paper changes, no contact with Andreas Fuls.
