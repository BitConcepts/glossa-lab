# Meroitic Benchmark — Step-0 Corpus Identity Record (C097-1)

**Date: 2026-11-20. Commission: execution of the Meroitic
reproduction benchmark founded on the scoping under Spec 095
Stage 5 (T502, C095-16) in
`second-targets/meroitic-benchmark-scoping-2026-11-17.md`,
commissioned by the owner in chat on 2026-11-20 ("in parallel
start the other ancient language decoding work"), and placed
the same day under the Meroitic Reproduction Benchmark
Program by the owner's direction that the benchmark stand as
its own program. The program was adopted as Spec 097 after
renumbering (D-097-1: the package was first drafted as Spec
096; the parallel Eteocypriot program landed as Spec 096
first). This record is filed under Spec 097 Stage 1 (T101,
claim C097-1) as step 0 of that scoping (§4.2): pin, license,
identity — filed BEFORE any benchmark computation. It was
first opened the same day as PR #603 under the Spec 095
placement; that PR was closed unmerged on the placement
direction, and the record is re-filed here with its
substance unaltered.** The structural census
in §5 is the identity record's census under its named basis
(line/row/token counts of the pinned files); no benchmark
statistic (no leg verdict, no frequency rank, no alignment
score) is computed in or claimed by this record.**

Execution venue: mini-server, worker clone
`~/glossa-work/meroitic-bench-2026-11-20` at origin/main
`e7e7898f8730f5a41e48c1c11d5a4ecab8f3b4c8`; corpus held in
scratch custody at `~/glossa-work/meroitic-corpus-src`
(never committed to this repository — see the licensing
ruling, §3). Custody note (2026-11-20, owner venue
transition): the corpus custody and all run state were
transferred to tower-compute the same day and verified there
against this record's manifest (30/30 files hash-equal)
before any further computation; Glossa-Lab study execution
sits on tower-compute from that point.

## 1. The target

Otten, Joshua & Anastasopoulos, Antonios (2025). "Towards
Ancient Meroitic Decipherment: A Computational Approach."
*Proceedings of the Second Workshop on Ancient Language
Processing (ALP), associated with NAACL 2025*, pp. 208–219.
ACL Anthology 2025.alp-1.11; DOI 10.18653/v1/2025.alp-1.11.
Read in full at execution from the publisher's PDF
(ACL Anthology, 12 pp., extracted text held in scratch).

## 2. The pin

- Repository: `github.com/Joshua-Otten/Meroitic-Corpus`
  (the repository named in the paper's footnote 1).
- **Pinned commit: `c9158f6865325877112b6b9ceef83b3c80a93c56`**
  (2026-11-10, "add bilingual dictionaries"), tree
  `76138c53118dbc273068f1ad1e5d411b3e3362fd`, default branch
  `main`, HEAD at pinning time (2026-11-20).
- Provenance fact, recorded because it decides what the pin
  means: the paper-era tip is `1a6eb1097d89309944908400e8d8b7905fa2bea1`
  (2024-05-14). A tree diff between `1a6eb109` and the pin
  shows **every `Data/` and `Embeddings/` file byte-identical
  across the two commits**; the pin's single change is the
  addition of `bilingual_dicts/` (the seven evaluation
  dictionaries and the French–English dictionary) — material
  the paper's experiments used but which entered the
  repository only after publication. The pin therefore
  reproduces against paper-era data plus the authors' own
  later deposit of their evaluation dictionaries.
- `Code/vecmap` is a gitlink (commit
  `b82246f6c249633039f67fa6156e51d852bd73a3`) with **no
  `.gitmodules` in the tree**: the alignment code the paper
  used is not retrievable from this repository at the pin.
  The benchmark's VecMap is therefore necessarily the
  program's own implementation of Artetxe et al. (2018),
  which is what the scoping's independence rule requires in
  any case.
- The processed corpora named in the authors' training
  script (`ProcessedData/meroitic_clean2.txt`,
  `ProcessedData/egyptian_clean.txt`) and the scraped
  Ramses JSON files are **not in the repository at any
  commit**. Consequences are carried into the freeze
  (companion record): the Egyptian token count (99,338)
  and the Egyptian embedding training cannot be re-derived
  from the published repository; the published Egyptian
  type count (1,729) is checkable against the published
  embedding files' vocabulary headers.

## 3. Licensing — the step-0 ruling, stated openly

- **No license exists for this repository.** Verified at
  pinning: the GitHub API reports `license: null`; the
  license endpoint returns 404; the tree at the pin contains
  no LICENSE or COPYING file; the README (113 bytes) states
  only that the repository "Provides the first
  machine-readable Meroitic corpus, along with data and
  alignment experiments". Default copyright therefore
  applies to the authors' compilation and code.
- What the authors do state, on the record: the paper
  (fn. 1 and §4) presents the corpus as the data "necessary
  to replicate our experiments" and states the data "will be
  made publicly available on Github" for that purpose.
- **Ruling applied (mirroring this program's CISI
  restricted-custody handling):** the absence of a license
  is recorded as a restriction, not concealed and not
  treated as a permission. The corpus is used for
  **scholarly reproduction only, in held custody**: the
  pinned files live in scratch storage on the execution
  host and are **never committed to this repository, never
  redistributed**; the authors' code is read only as the
  independence rule permits (§4) and is never copied in;
  what this program publishes from the benchmark is its own
  code and **derived aggregate statistics** (counts,
  frequency and positional distributions, alignment
  scores) — the same statistics-only posture the program
  applies to CISI material.
- The falsifier's step-0 arm is therefore recorded as
  **not fired, on a stated basis**: the repository is
  available, and it is usable for scholarly reproduction
  under the custody terms above; it is **not** licensable
  for redistribution, and no redistribution occurs. A
  reviewer who holds that any use without a license is a
  bar has the full evidence for that reading in this
  section; the benchmark's outcome record will restate the
  ruling so the verdict never travels without it.

## 4. Independence-rule readings of the authors' code (complete log)

The scoping permits reading the authors' code for the
mapping scheme only; every reading is recorded here.

1. `Code/getW2V_embeddings.py` (36 lines) — read for the
   training configuration and file mapping: gensim
   `Word2Vec`, whitespace tokenization of a line-separated
   cleaned corpus, `vector_size=100` in the committed
   script (the paper varies 20/50/100/120), `window=5`,
   `min_count=1`, all other parameters at gensim defaults;
   input files `ProcessedData/meroitic_clean2.txt` /
   `egyptian_clean.txt` (absent from the repo, §2).
2. `Code/find_nearest_neighbors.py` (21 lines) and
   `Code/intrinsic_eval.py` (46 lines) — read for the
   evaluation mapping only: cosine nearest neighbours over
   the published embedding files via gensim `KeyedVectors`;
   the intrinsic script's analogy call uses the corpus form
   `qEr`, confirming the `E`-for-/o/ convention inside the
   published vocabulary.
3. `Code/RamsesScraperComplete.py` (294 lines) — read for
   provenance only: the Egyptian texts were scraped from
   `ramses.ulg.ac.be` into per-text JSON files; neither the
   JSONs nor any cleaned Egyptian corpus is in the repo.
4. The per-file transcription headers in `Data/*.txt` —
   read as the mapping scheme of record: dotted letters are
   transcribed with capitals; `X` = 4th h, `x` = 3rd h,
   `S` = š, `N` = ñ, `H` = ḥ-tilde, `E` = ê (the paper's
   /o/), `A` = dotted a, `G` = ġ; Rilly/Millet files
   additionally map dotted consonants to capitals
   (`M B Y Q W I R K T`). Kalabsha_Millet.txt's header notes
   Millet's `E` correlates with `o` in the
   Kharamadoye-narrative transcription, which uses `o`.

No other authors' code was read. The benchmark's
implementation (companion freeze, and the outcome record)
is the program's own, written from the paper's stated
methods and the mapping facts above.

## 5. Identity census of the pinned corpus (named basis)

Basis: UTF-8 text read at the pin; a *data line* is a
non-blank line not starting with `#`; Lobban rows are
tab-separated; *whitespace tokens/types* split on
whitespace runs exactly as deposited; embedding
*vocabulary* is the word2vec text header's first field,
checked against the file's word-line count. Structural
counts only.

| Object | Count under the basis |
|---|---|
| LobbanVocabList.txt | 195 data rows; **193 distinct headword forms**; 175 rows carry a translation, 20 do not |
| MilletExamples.txt | 931 data lines (1,447 total; 260 comment, 256 blank) |
| RillyExamples.txt | 23 data lines (40 total) |
| Kalabsha_Millet.txt | 10 data lines |
| Three royal narratives | 1 data line each (3 files) |
| mero-corpus.txt (as deposited) | 18,090 lines, all non-blank; 756,028 whitespace tokens; **1,868 distinct whitespace types** |
| Egyptian embeddings vocab | dim 100/120: **1,729**; dim 20/50: 1,746 |
| Meroitic embeddings vocab | dim 100/120: **1,868**; dim 20/50: 1,902 |
| Dictionary lines | nouns 26, names 22, numbers 15, verbs 14, titularies 9, adj/adv 6, prepositions 3 (combined nouns+names+nums file: 59 lines) |
| French–English dictionary | 4,904 pairs |

Content hashes (SHA-256) of every pinned file are listed
in the appendix filed alongside this record
(`records/meroitic-benchmark-step0-manifest-2026-11-20.txt`);
the load-bearing ones:
`Data/mero-corpus.txt` `b7f3350c2f2118a8223854462a8e881c424cba6b26c01ebfb676efa92ea253ce`;
`Data/LobbanVocabList.txt` `1275c34d10bf4dc397cc0e457f3a686fdb76f3fbc192b3b42efb6afba753d622`;
`Data/MilletExamples.txt` `9e0dc67ca945fa915479f015cdb6083b5788f86c3cc096f171994b0e4e670e6f`;
`Data/RillyExamples.txt` `beae69e1b417cdd6bcdf88b2d6987af22b6cc99044dbd40d3276b8b13815f1f7`;
`Embeddings/egyptian_dim_100.txt` `20fc91ebd357736a8e96311dd4dc2086e72ebb66255e311cae41679f0f3adfe9`;
`Embeddings/meroitic_dim_100.txt` `9da08536433995ef577d392e17a0440cc0a2e722ca740315e34af8d303e98c94`.

## 6. Normalization and orientation basis (C095-3)

- Normalization of record for all benchmark computation:
  the corpus's own ASCII mapping as deposited; the paper's
  `E`-for-/o/ convention reconciled explicitly in Leg B by
  mapping `E` → `o` for sign-set and frequency purposes
  and reporting both bases where they differ; no other
  normalization is applied silently — every cleaning step
  a leg applies is enumerated in the execution freeze and
  logged per run.
- Orientation basis: Meroitic and Egyptian transcriptions
  are read left-to-right as deposited; word-position
  (Leg B) is position within the whitespace-delimited word
  as deposited. No reading-order transformation is applied.

## 7. What this record does not do

It computes no leg, moves no claim, and touches no Indus
record. The benchmark's criteria and falsifier stand
exactly as fixed in the scoping; the companion freeze
(`meroitic-benchmark-freeze-2026-11-20.md`) fixes the
execution details the scoping left to execution (counting
bases per count, seeds, the Egyptian-data ruling) before
any computation, and the outcome record reports against
both documents.
