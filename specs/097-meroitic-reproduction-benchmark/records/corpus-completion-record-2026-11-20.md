# Meroitic Decipherment Campaign — Corpus Completion Record (Spec 097, Stage 4.1, T402)

**Date: 2026-11-20. Claim C097-7. Executed on tower-compute
under the preregistration in
`records/decipherment-campaign-design-2026-11-20.md` §2.
Account of record: held / acquired / examined / gap-named,
against the REM totals the design registered (some 1,300
published texts, Leclant et al. 2000 with appendices; roughly
900 further known texts unpublished in the REM; more than
2,000 inscriptions known in total — Rilly 2016).**

## 1. Held (from step 0)

The Otten corpus at pin
`c9158f6865325877112b6b9ceef83b3c80a93c56`, license **none**,
held in custody under the step-0 ruling (never committed,
never redistributed): mero-corpus.txt (18,090 lines), the
Millet/Rilly/Lobban/Kalabsha example files, the seven
bilingual dictionaries, the published embeddings.

One property of the held corpus is load-bearing for every
later stage and is recorded here as a completion finding: the
deposited mero-corpus.txt is the paper's **name-augmented
training file**, not a corpus of distinct texts — the
benchmark's Leg A divergence A9 (17,257 phrases published vs
18,090 lines deposited) is explained by it, and an independent
2026 project (see §2) measured the same structure from the
data alone: 662 distinct texts or phrases under name-masking,
each repeated about 27 times on average with personal names
swapped. **Consequence registered for Stages 4.2–4.4:** all
distributional work runs on the de-augmented example material
(the per-scholar files) and the acquired inscription corpus,
never on raw mero-corpus.txt counts; the augmentation pools
(178 private names, 11 royal names in the independent account)
are themselves formula evidence and are registered as such in
the anchor freeze.

## 2. Acquired (openly licensed, pinned)

**MikeKovetsky/meroitic** ("Meroitic with Opus 5.5", 2026),
pinned at commit `145af0836c071e7c9796d37d4b36add00d347c8a`,
held in custody on tower-compute at
`~/glossa-work/meroitic-kovetsky-src`. Licenses: code MIT
(`LICENSE`); data and write-ups CC BY 4.0 (`LICENSE-DATA.md`),
covering transcriptions read from Griffith's public-domain
editions (*Meroitic Inscriptions* I–II, *Meroë*, *Karanòg*,
1911–12). The source's own census: **396 inscriptions
machine-readable under the open license, 327 of them absent
from the public (Otten) corpus**, including the longest text,
the Akinidad stela (REM 1003); measured sign accuracy of its
transcription method 95.6% against the modern edition on
cursive type (99.6% against Griffith's print), 97.7% for the
Karanòg material against Griffith's printed words — accuracy
figures are the source's own measurements and are carried as
such, so every acquired text enters the build with a
transcription-quality caveat, not as a critical edition.
Build-verified structure: a 652-row inscription index keyed
by REM number with site, genre, and source-page provenance
(`data/inscriptions.jsonl`); transcription files under
`data/expansion/` (Griffith MI/Meroë sets, Karanòg, Faras,
JEA sets; 488 data files). Provenance class for the build:
**secondary transcription of public-domain editions, openly
licensed** — usable for distributional and anchor work;
readings that turn on a single sign in a single acquired text
are flagged to the underlying edition before scoring (Stage
4.3 discipline).

## 3. Examined, not acquired (with cause)

- **Zenodo "Meroitic Studies" I–III** (records 1765414,
  2076873, 2332392; CC0): each carries a single article PDF —
  journal literature, not corpus data. Not corpus; available
  to the literature record.
- **notofonts Meroitic fonts** (OFL-1.1): typefaces, not texts.
- **Lackadaisical-Security/Meroitic-Script-Decipherment**:
  license NOASSERTION (no open license granted); not acquired.
  Its "decoded research logs" are claims, not data, and would
  enter, if ever, as claims to test, not as corpus.
- **Trismegistos Meroitic records**: membership-gated;
  examined as a gap (see §4), not acquired.

## 4. Gaps named (not closable lawfully from here)

1. **The REM's own digital edition** — in progress in the
   specialist community; not openly licensed for bulk use.
   The campaign's REM-keyed work therefore keys on the
   acquired index (§2) and the published REM numbering.
2. **The ~900 REM-unpublished texts** (Qasr Ibrim,
   Musawwarat es-Sufra) — unpublished; no lawful route short
   of the edition projects themselves.
3. **Trismegistos full Meroitic data** — membership-gated;
   closing this gap is a purchase/registration decision for
   the owner, recorded, not made.
4. **The 2025 paper's unpublished intermediates** (processed
   corpus, Ramses scrape output, Nubian scanning output) —
   already named in the benchmark's Leg A; unchanged.
5. **Critical-edition readings** — the acquired corpus is a
   measured-accuracy transcription of century-old editions;
   where a future reading turns on a contested sign, the
   modern edition (REM volumes, print) is the settling record
   and is not machine-readable here. Named as a standing
   caveat on Stages 4.3–4.4 scoring.

## 5. The completed corpus, as the campaign will use it

Two components, one build: (i) the de-augmented published
example material from the held pin (871-phrase class material
in its per-scholar files, with translations), and (ii) the
acquired REM-keyed inscription corpus (396 inscriptions,
provenance per text). Together they are the fullest lawfully
obtainable machine-readable Meroitic corpus available to this
program today: on the order of a fifth of the known
inscription count by texts, skewed — as the whole record is
skewed — toward funerary material, with the royal-narrative
class represented by a few dozen texts at most. Every later
stage's record must state which component each observation
came from. The anchor freeze (T403) is taken against this
build.
