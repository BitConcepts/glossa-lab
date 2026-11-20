# Meroitic Benchmark — Execution Freeze (2026-11-20)

**Frozen before any benchmark computation, under the
scoping in `second-targets/meroitic-benchmark-scoping-2026-11-17.md`
(§3 criteria and falsifier are NOT restated differently
here; this freeze fixes only the execution details the
scoping left open). Companion: the step-0 identity record
(`records/meroitic-benchmark-step0-identity-record-2026-11-20.md`)
for the pin, license ruling, census basis, and the
independence-rule reading log. Corpus pin:
`c9158f6865325877112b6b9ceef83b3c80a93c56`. Seeds fixed
here: **42, 1337, 2025** (Leg C stochastic runs; every
attempt is indexed in the outcome record per Spec 089 —
no attempt is deleted, renamed, or retried silently).**

## Leg A — counting bases (primary basis fixed per count)

Paper text relied on: §4/Table 1 (data collection,
narratives excluded from Table 1), §5.2 (cleanup:
"eliminating translations, metadata, dashes, colons,
etc."; examples separated per line; the combined Meroitic
corpus of §5.2 contains 871 phrases; Egyptian 1,729 types
/ 99,338 tokens), §5.2 augmentation paragraph (1,868
forms / 17,257 phrases / 782,761 words), Table 2.

- **A1 — 193 translated Meroitic words.** Primary basis:
  distinct headword forms (first tab field, as deposited)
  in `LobbanVocabList.txt`. Reported alongside: rows
  carrying a translation (175) and distinct translated
  headwords (173) — the paper's label and its count are
  reported against all three readings, the primary being
  the one the label's number must meet.
- **A2 — 897 Meroitic phrases.** Primary basis: phrase
  lines surviving §5.2 cleaning across the three scholar
  files (`MilletExamples.txt`, `RillyExamples.txt`,
  `LobbanVocabList.txt`): comment/metadata lines removed,
  translation material removed (in Millet/Rilly files,
  the translation is the post-tab field or the following
  gloss line as the file's own structure marks it), each
  surviving example counted once. The cleaning is
  implemented from the files' structures and every rule
  is logged; intermediate counts per file are reported.
- **A3 — 302 Late-Egyptian complete texts.** Not present
  in the repository in any form. Basis: none available.
  Expected outcome: named divergence (cause: source
  material not published in the corpus repository; the
  count describes the authors' Ramses scrape, §5.2).
- **A4 — 708 scanned Nubian pages.** Not present in the
  repository in any form (the Nubian scanning programme
  is described in §4 as in-process). Expected outcome:
  named divergence, same cause class as A3.
- **A5 — 871 pre-augmentation phrases.** Primary basis:
  phrase lines surviving §5.2 cleaning across ALL
  Meroitic source files including the three royal
  narratives and `Kalabsha_Millet.txt` (the §5.2 corpus
  is the combined corpus the embeddings train on).
  Reported alongside: the same count excluding the
  narrative files (Table 1's exclusion), so the two
  readings the paper's text supports are both on record.
- **A6 — 1,729 Egyptian types.** Primary basis: the
  published `egyptian_dim_100.txt` / `dim_120.txt`
  vocabulary size (the paper's §5.3 intrinsic setting is
  dimension 100). Reported alongside: dim 20/50
  vocabulary (1,746) as a named variant.
- **A7 — 99,338 Egyptian tokens.** Not derivable: no
  Egyptian corpus text is published in the repository.
  Expected outcome: named divergence (cause as A3).
- **A8 — 1,868 post-augmentation forms.** Primary basis:
  distinct whitespace types in `Data/mero-corpus.txt`
  as deposited; cross-checked against the published
  `meroitic_dim_100/120.txt` vocabulary size.
- **A9 — 17,257 post-augmentation phrases.** Primary
  basis: non-blank lines of `Data/mero-corpus.txt` as
  deposited (18,090 at census). Reported alongside:
  distinct lines, and lines after §5.2 punctuation
  cleaning — all three readings reported, none selected
  post hoc as "the" basis.
- **A10 — 782,761 post-augmentation words.** Primary
  basis: whitespace tokens of `Data/mero-corpus.txt` as
  deposited (756,028 at census). Reported alongside the
  tokenizations the paper's own cleaning text supports:
  (ii) additionally splitting tokens on `.` (morpheme
  separator the paper says it preserves in places),
  (iii) additionally splitting on `-`. All readings
  reported with their deltas.
- **Table 2 (A11, one count-family).** Primary basis:
  entry lines in each per-category dictionary file at
  the pin (nouns 26, names 22, numbers 15, verbs 14,
  titularies 9, adj/adv 6, prepositions 3 at census).
  Reported alongside: the names count inside the
  combined `nouns+names+nums.txt` file, and distinct
  source-form counts per file — the paper-era/combined
  readings are part of the record, not a rescue.

Leg A succeeds per count on exact equality under the
primary basis; every non-equal count is a named
divergence with its traced cause. The falsifier's Leg A
arm reads on primary bases.

## Leg B — bases

- Corpus: `Data/mero-corpus.txt` as deposited (the only
  complete Meroitic corpus file in the repository).
- Sign extraction: character-level over word tokens;
  characters are the corpus's ASCII letters; the digraph
  question is settled as follows — Meroitic signs in this
  transcription are single letters (the syllabic signs of
  the fixture tradition are written as consonant
  sequences, per the fixture module's own header), so the
  sign alphabet is the set of distinct letters.
- Reconciliation: `E` → `o` (the paper's convention,
  step-0 record §6); the dotted-letter capitals
  (`S N X x H A G` and dotted consonant capitals) are
  reported as their own signs first, then under the
  explicit fold the file headers state (capitals are
  dotted variants of their base letters) — both sign sets
  are reported; the criterion reads on the reconciled
  set as the scoping states ("after reconciling the
  paper's E-for-/o/ convention explicitly"), with the
  dotted-variant fold named as part of that
  reconciliation and its effect shown.
- Frequency ranks: letters ranked by token frequency
  over the corpus; Spearman ρ (scipy) against the
  fixture's ME01–ME19 order over the 19 fixture signs;
  criterion ρ ≥ 0.90 as fixed in the scoping.
- Positional distributions: per sign, counts and shares
  in word-initial / word-medial / word-final position
  (single-letter words count as initial and final,
  stated here so the archive is unambiguous), computed
  deterministically and archived in full in the outcome
  record's JSON companion.

## Leg C — bases and the Egyptian-data ruling

- **Egyptian-data ruling (forced by step 0, recorded
  here before computation):** no Egyptian corpus text
  exists in the published repository, so Egyptian
  embeddings cannot be independently trained from the
  published data. Leg C therefore has two arms:
  - **Arm 1 (primary):** the alignment machinery —
    the program's own VecMap implementation and its own
    precision@10 evaluation — run over the **published
    embedding files** (the authors' `Embeddings/` word2vec
    text files at dims 20/50/100/120). This tests the
    paper's §6/§6.2 headlines on the paper's own published
    embedding layer with independent alignment code.
  - **Arm 2 (secondary, mixed provenance, reported
    separately and never merged into Arm 1's verdict):**
    Meroitic embeddings trained by the program's own
    Word2Vec on `mero-corpus.txt` (gensim; window 5,
    min_count 1, sg=0, epochs 5, negative 5 — the
    authors' committed configuration, step-0 record §4.1;
    dims 20/50/100/120; seeds as frozen) aligned by the
    same program VecMap against the published Egyptian
    embeddings.
- **VecMap implementation (program's own, from Artetxe
  et al. 2018 as the paper cites it):** length
  normalization, mean centering, whitening; supervised
  mode seeded with the training dictionary under test;
  unsupervised mode by adversarial initialization
  followed by iterative Procrustes refinement with
  dictionary induction, stochastic dictionary
  re-weighting, and symmetrization — the published
  algorithm's named steps, implemented in the benchmark
  code and reviewed against the paper's three settings
  (unsupervised; numerals-seeded; nouns-seeded).
  Retrieval for evaluation: CSLS (k=10) as VecMap's
  standard, precision@10 = the gold target inside the
  10 nearest CSLS neighbours of the mapped source word.
- **Evaluation protocol (from the paper §5.3/§6.2):**
  settings = {unsupervised, numerals-seeded,
  nouns-seeded} × dims {20, 50, 100, 120}; each setting
  is evaluated on every dictionary; the dictionary it
  was seeded on is its *training* dictionary, all others
  are *unseen* for that setting. Criteria as fixed in
  the scoping: unseen precision@10 = 0%; training
  accuracy ≤ 25% band; numerals best-or-tied at 100d.
  Dictionary words absent from either published
  vocabulary are excluded pair-wise and counted —
  the exclusion count is part of the result, since the
  paper does not state its own.
- **French–English skyline:** reported as published
  (70% / ~68%) and NOT re-run: it requires
  Wikipedia-trained embeddings the repository does not
  contain (the repo's `fra-eng.0-5000.txt` is a
  dictionary, not embeddings). Named as not administered
  in the outcome record, with that cause.
- Hyperparameters are the paper's; any deviation is a
  recorded amendment to this freeze, never a silent
  search. The run index in the outcome record accounts
  for every attempt, including failures.

## Reporting

Standards Part II: per-leg verdicts exactly as the
scoping's criteria read (REPRODUCED / DIVERGED /
NOT REPRODUCED per leg; the falsifier read on Leg A's
primary bases and on the step-0 record); stochastic
quantities reported per seed with their spread;
multiplicity family = the three legs' fixed criteria.
Nothing in any outcome moves any Indus record.
