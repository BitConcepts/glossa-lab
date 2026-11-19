# DEDR dataset restoration record — 2026-11-19

**Status: dataset restored and verified in a worker clone; acceptance
is a separate recorded act (§6). No study leg was re-run; no recorded
not_run outcome is changed by this record.**

## 1. What was lost

The DEDR dataset the program consumes is the digitised Burrow &
Emeneau, *A Dravidian Etymological Dictionary*, 2nd ed. 1984, in the
form held as a bare gitlink at `reports/jambu-dedr`, pinned to commit
`d5050e5a9671012df416e9c474c75aba41c07f8c`, with no `.gitmodules` in
any history. The recovery hunt of 2026-11-17 established that the
content existed only on a lost working machine and was NOT
RECOVERED; the Spec 091 Stage 3 record (deviation 2) carries the
consequence: battery v2's DEDR leg was `not_run` for all 28 signs of
run `study-20261117T103816Z-a25969`, reason
`dedr_dataset_not_held—not_run`.

The consumed surface, from the consuming code:

- `reports/jambu-dedr/data/dedr/dedr_new.csv` — read by battery v2
  (`backend/scripts/phase48_medium_validation_v2.py`, `load_dedr` /
  `test_dedr_v2`) and by the Phase-50 catalogue. Headerless CSV;
  the battery keeps rows of ≥5 columns with word = column 3 and
  gloss = column 4 (1-based), a word longer than 1 character, and
  tests a reading by exact match, else by the frozen prefix rule.
- `reports/jambu-dedr/cldf/` — read by
  `backend/glossa_lab/data/cldf_loader.py` (configured in
  `backend/glossa_lab/config.py`): `forms.csv`, `languages.csv`,
  `parameters.csv`, with forms keyed by `Parameter_ID` = DEDR entry.

## 2. What "restored" means

The restored dataset is *the same dataset* iff the content at the
consumed paths is byte-identical to the tree of the recorded
gitlink commit. That identity is checkable without trusting any
single source: Software Heritage archived the same revision
(directory `ce6541aa7b96c31d0ea88e4a116e698e5fc187b9`) and records a
git blob SHA-1 for every file in it. Restoration therefore
requires, per placed file: size and git blob SHA-1 equal to the
archived content id. The dataset's entry keys are the printed DEDR
entry numbers (`d` + number in the CSV's second column), a property
of the published dictionary, verified by sampling against the DSAL
online edition (§5).

## 3. How it was restored

The recovery hunt looked for the upstream under the directory's
name (`jambu/dedr`, 404). The upstream is in fact
**`moli-mandala/data`** — "a CLDF database for the Jambu
application, containing historical linguistic data for many
languages of South Asia" (Aryaman Arora) — live on GitHub, and the
pinned commit is fetchable from it. Its README records the
digitisation's own provenance: `parse.py` scrapes the online DEDR
(the DSAL edition) and splits each entry into language spans;
`dedr_new.csv` is its output. An earlier, deprecated conversion
(`dedr.csv`, from an October 2013 SQL scrape of the same online
edition) sits beside it in the same tree.

On the owner's 2026-11-19 order (everything doable today is done;
the re-derivation/restore decision left open by the recovery hunt
is taken), `backend/scripts/restore_jambu_dedr.py` cloned the
upstream, checked out the pinned commit, verified every file
against the pinned hash table, and placed the consumed surface —
all of `data/dedr/` (9 files), all of `cldf/` (5 files), and the
upstream `README.md` — 15 files, ≈47 MB, into `reports/jambu-dedr/`
in the worker clone. The upstream tree's other subtrees (CDIAL,
Munda, other-forms, model code, statistics) are not DEDR dataset
content and were not placed. The dataset bytes are placed, never
committed: the gitlink remains the tree's only entry for
`reports/jambu-dedr`, exactly as the program always held it. The
underlying dictionary is © Clarendon Press and the upstream
carries no licence file; the program's posture
(`research/indus/DATA_LICENSES.md`: DEDR = reference use, entry
numbers cited, no verbatim text in outputs) is unchanged.

## 4. Verification — identity and coverage

Machine record:
`records/dedr-restore-verification-2026-11-19.json` (the restore
script's `--verify` output, run in the worker clone over the
placed tree).

- **15/15 files placed; every file's size and git blob SHA-1 match
  the pinned table** (which is Software Heritage's recorded
  content id for the same path in the pinned tree). Headline file:
  `dedr_new.csv`, 5,478,240 B, blob SHA-1
  `4f8411f19b9e3c2c0c235a24096d59d4afc558f1`, SHA-256
  `fbcc2b2d47c9be24338d846319de2b2c5a2ad4f45451274e3223bc63bc60cae0`.
- **Coverage:** `dedr_new.csv` holds 85,374 rows, uniformly 9
  columns ([language tag, param id, lemma, gloss, native form,
  phonemic form, notes, references, page]); 5,623 distinct entry
  params; 89 language tags. Largest: Tam 13,644 rows, Kannada
  11,322, Telugu 8,761, Mal 7,930, Tulu 7,135.
- **The program's own consumers execute over the placed tree:**
  battery v2's `load_dedr` returns **85,251 entries** (its ≥5-column,
  word-length filter over the 85,374 rows), and `test_dedr_v2`
  passes probe readings by exact match — kalam ×5, nal ×18,
  kai ×116, tiru ×3, ko ×93, mutalai ×1. The CLDF loader's summary
  over the placed `cldf/` reads 290,071 forms, 615 languages,
  23,131 parameters (the combined Jambu CLDF; the DEDR component
  is the `d`-keyed subset).

## 5. Verification — against the published dictionary

Sampled entries were checked against the DSAL online edition of
Burrow & Emeneau 1984 (dsal.uchicago.edu), entry by entry, on
2026-11-19, against hash-identical bytes:

- **Verbatim agreement (4):** 340 āppu (Tam. āppu "wedge used in
  splitting wood, peg, stake"; Ma. āppu "wedge, plug, what stops a
  crevice", āppam "wad of gum" — the dataset's d340 rows reproduce
  these); 399 āḷ (dataset d399); 1305 kalam (d1305); 4885 mīṉ
  "fish" (d4885).
- **Scripted agreement (8):** d750 ūr, d1500 kāḷuka, d2153 koḷ,
  d3000 takar, d3900 pāṇṭů, d4450 pai, d5200 leŋ, d5503 veḷḷam —
  for each, DSAL's entry carries the same printed number, the same
  headword, and the dataset's gloss.
- **Inconclusive probes (3):** d2200, d4500, d5557 — the entries'
  first-listed forms are Tulu/Konda/Pengo forms, which are not
  DSAL headwords, so the headword search cannot reach them; no
  disagreement was found, and the limitation is the search
  surface, recorded as such.
- **Cross-pipeline containment:** the same tree's deprecated
  `dedr.csv` is an independent pipeline from the same published
  source (the October 2013 scrape). Of its 64,655 (entry,
  language, lemma) triples, 46,410 (71.8%) are contained in
  `dedr_new.csv`; the newer parse carries more rows (85,374 vs
  68,808) and splits entry spans more finely. The differences are
  parser-generation differences between the two digitisations;
  the restored artifact's identity does not rest on this
  comparison — it is pinned by hash (§2).

One incidental finding, flagged and not corrected here: Phase-89's
embedded candidate table cites "DEDR 0340" for the reading āḷ
"person". Against the published numbering, āḷ is entry 399 and
340 is āppu. The citation lives in a historical phase script and
its report; correcting it is a separate act.

## 6. What remains to acceptance

1. **Acceptance act (owner/program decision, not taken here):**
   accept this restored tree as the program's held DEDR dataset.
2. **Placement into the live origin's tree** (`~/glossa-lab` on
   the mini-server) by the same restore script — an ops act after
   acceptance, mirroring the M77 placement pattern.
3. **Any battery re-run** over the T302 population (or any other)
   is a new run under a new commission. T302's recorded outcomes,
   including `dedr = not_run` for all 28, stand exactly as filed.

Standing position unchanged: the Indus script is not deciphered;
a restored dictionary is an input, not a result.
