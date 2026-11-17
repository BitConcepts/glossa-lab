# Meroitic Reproduction Benchmark — Study Scoping

**Status: SCOPING under Spec 095 Stage 5 (T502), discharging
C095-16. This document scopes the benchmark as a study spec. No
benchmark has been run: no corpus has been downloaded, no
statistic computed, no result produced. The benchmark's
execution is a separately commissioned study, not a stage of
Spec 095 (C095-16); commissioning it is an owner decision.**

**Register basis.** RT-35: the target is DUPLICATE-OF-RECORD
(pre-named in the program's priority map, `docs/
undeciphered_scripts.md`: "Next target" — script readable,
~1,200 inscriptions in REM, an active toy module); the NEW item
is the 2025-corpus reproduction benchmark. RT-35's acceptance
shape governs: *published corpus statistics reproduced within
stated tolerance, or the divergence is the outcome record.*

## 1. The existing fixture (the starting inventory, named exactly)

`backend/glossa_lab/data/meroitic.py` (301 lines, in the tree at
the Stage 5 base `c2be9869`), with its legacy benchmark
`backend/glossa_lab/experiments/_legacy/meroitic_benchmark.py`
and that benchmark's output of record, `outputs/
meroitic_benchmark.json`. Census verified at scoping
(2026-11-17, from the module itself):

- **Sign inventory:** 19 signs, `MEROITIC_SIGNS` — Griffith
  (1911) phonetic values `a n r e t k l s m i b w d y q h o p g`,
  carried under opaque IDs ME01–ME19 whose **order matches
  frequency rank** (the module's stated convention; ME01 `a` is
  the most frequent). `get_full_answer_key()` returns all 19
  ID→value pairs: the script is deciphered, so the answer key
  is ground truth, not a hypothesis.
- **Fixture corpus:** `_MEROITIC_LINES` — 50 lines, **551 sign
  tokens** under `get_corpus_symbols()` (the register's and the
  priority map's figure, re-derived at scoping). Format: sign
  sequences with `.` word dividers.
- **A Sahidic Coptic language-model corpus** in the same
  module, existing for the Tier 1f wrong-hypothesis test.

The fixture's limits, stated so the benchmark cannot overclaim
its substrate: the 551-token corpus is **constructed formulaic
material** — lines "based on common formulaic sequences in
attested Meroitic inscriptions (Griffith 1911; Leclant 1963;
Rilly 2007; Hintze 1959)", per the module's own header — not
transcriptions of identified inscriptions. The legacy
benchmark's recorded output (self-model sign accuracy 16/19;
Coptic target 1/19; degradation ratio 0.062) answers a
different question (does the engine reject a wrong language
hypothesis?) and is **not** a reproduction target of this
benchmark.

Per C095-16, the fixture module is the benchmark's **starting
inventory**: the sign set, the answer key, and the frequency-
rank order the reproduction checks run against. The benchmark's
*data* is the published 2025 corpus (§2), which is roughly
three orders of magnitude larger.

## 2. The 2025 corpus and paper (the reproduction source)

**Otten, Joshua & Anastasopoulos, Antonios (2025). "Towards
Ancient Meroitic Decipherment: A Computational Approach."
*Proceedings of the Second Workshop on Ancient Language
Processing (ALP), associated with NAACL 2025*, pp. 208–219.
ACL Anthology 2025.alp-1.11; DOI 10.18653/v1/2025.alp-1.11.**
Read in full for this scoping (publisher's PDF via the ACL
Anthology). The review's citation of it (a Wiley-hosted link in
the review's source page) is superseded by this identification:
the paper is the ACL workshop paper above — recorded here as a
correction of the citation, not of the review's substance,
which matches (first machine-readable corpus; baseline
alignment work).

What the paper publishes, as the benchmark's targets:

- **The first machine-readable Meroitic corpus**, built by
  manually converting pre-transcribed examples from three
  sources: the vocabulary list of Lobban Jr (2021), example
  phrases from Rilly (2007) and Millet (1968); plus three long
  royal narratives refitted from prior word-frequency work
  (Tañyidamani; the Hamadab Stela of Amanirenas and Akinidad,
  via Hofmann 1998; the Kalabsha Inscription of Kharamadoye,
  via Hägg 2000). Per-scholar files are kept separate, each
  with its mapping scheme; the combined corpus conforms to
  **Millet's paradigm**. Transcription is an ASCII mapping; the
  paper's convention writes /o/ as `E` (from Millet's /ê/
  transcriptions), although `o` is the standard convention —
  a normalization fact any reproduction must carry explicitly.
- **Corpus and code are public** ("The corpus, along with data
  and code necessary to replicate our experiments:
  github.com/Joshua-Otten/Meroitic-Corpus", paper fn. 1).
  **The repository's license and current commit were not
  verified by this scoping** — pinning and license-recording
  are execution step-0 acts (§5).
- **Published statistics (Table 1, data-collection):**
  translated Meroitic words **193**; Meroitic phrases **897**;
  Late-Egyptian complete texts **302**; scanned Nubian pages
  **708**. (Table 1 excludes the royal narratives.)
- **Published corpus counts (§5.3):** the (pre-augmentation)
  Meroitic corpus contains **871 example texts or phrases**;
  the Egyptian corpus **1,729 unique types / 99,338 tokens**;
  after anthroponym-swap augmentation the Meroitic corpus
  contains **1,868 unique word forms from 17,257 sentences or
  phrases: 782,761 words in all**.
- **Published evaluation dictionaries (Table 2):** seven
  dictionaries, over 90 pairs — nouns 26, names 18, numbers 15,
  verbs 14, titularies 9, adj./adv. 6, prepositions 3.
- **Published alignment results (§6, §6.2):** lexicon induction
  (VecMap, precision@10) — **no setting correctly translated
  any term from an unseen dictionary (0%)**; on the training
  dictionary, **at most 20%** accuracy, the best setting being
  **numerals with 100-dimension vectors**; the French–English
  skyline reached **70% on its training dictionary and ~68% on
  test**. Intrinsic cosine-similarity tables (Tables 3–4)
  publish spot values (e.g. Egyptian *nswt*/*jmn* family above
  0.92; Meroitic *qor(e)*–*qr* 0.91).
- **Stated limitation, carried into this scoping:** REM (Le
  Répertoire d'Épigraphie Méroïtique) holds over 1,000
  digitized inscriptions as **image files requiring
  transcription** — the 2025 corpus is a phrase-and-vocabulary
  corpus, not the inscription corpus. The benchmark reproduces
  the 2025 corpus's results, not Meroitic as a whole.

**An interpretation, stated openly.** C095-16 speaks of
reproducing "published sign-frequency and positional results".
The paper publishes no sign-frequency or positional tables:
its published quantitative results are the census counts above
and the embedding/alignment results. This scoping therefore
maps the claim's phrase onto (a) the published census counts
(Leg A), (b) sign-frequency and positional distributions
*computed from the published corpus* and checked against the
fixture inventory's rank order — the program's own
inventory of record (Leg B), and (c) the published alignment
headline results (Leg C). If the owner reads the claim more
narrowly, Legs A and C are the benchmark and Leg B is an
extension; the scoping record flags the choice rather than
hiding it.

## 3. The benchmark as scoped (study spec)

**Question.** Can an independent implementation, starting from
the fixture inventory and the openly published 2025 corpus,
reproduce the paper's published results — and where it cannot,
is the divergence the outcome record?

**Independence rule.** The reproduction implementation is the
program's own, written from the paper's stated methods. The
authors' code may be read for the mapping scheme only; every
such reading is recorded in the execution record. Running the
authors' pipeline and comparing outputs is not reproduction.

### Leg A — census reproduction (deterministic)

From the pinned corpus repository, applying the paper's stated
cleaning (§5.3: translations, metadata, dashes and colons
eliminated as stated; examples separated per line; per-scholar
files combined under Millet's paradigm), reproduce: Table 1's
four counts and §5.3's six counts (871; 1,729; 99,338; 1,868;
17,257; 782,761).

- **Success criterion (fixed):** every count reproduced
  exactly. Any count that cannot be reproduced is named, with
  the cause as far as it can be traced (repository state,
  unstated cleaning step, paper error) — a named divergence is
  a legitimate outcome (RT-35); a silently dropped count is a
  failed leg.

### Leg B — sign-frequency and positional reproduction

From the same pinned corpus under the paper's ASCII mapping,
compute the sign-frequency distribution and the word-position
(initial / medial / final) sign distributions.

- **Success criteria (fixed):** (i) the attested sign set,
  after reconciling the paper's `E`-for-/o/ convention
  explicitly, equals the fixture inventory's 19 signs — any
  extra or missing sign is named; (ii) the computed frequency
  rank order agrees with the fixture's ME01–ME19 rank order at
  **Spearman ρ ≥ 0.90** (threshold fixed here, before any
  computation; the check is real, not tautological — the
  fixture's order derives from the Griffith/Rilly tradition,
  the computation from a different, 2025 sample); (iii) the
  positional distributions are computed deterministically and
  archived as the benchmark's positional record, reported per
  Standards Part II.

### Leg C — alignment headline reproduction (stochastic)

An independent implementation of the paper's §5.3–§6.2
pipeline (Word2Vec embeddings at the paper's dimensions
20/50/100/120; VecMap alignment; the paper's seven evaluation
dictionaries as published), under seeds fixed in the execution
freeze.

- **Success criteria (fixed bands):** unseen-dictionary
  precision@10 reproduces the paper's hard zero (**0%**);
  training-dictionary accuracy falls in the band **≤ 25%**
  (paper: ≤ 20%; the band admits seed variance and no more);
  the numerals dictionary is the best or tied-best setting at
  100 dimensions. A band failure is recorded as a divergence
  with its magnitude — not tuned away: hyperparameters are the
  paper's, and any deviation is a recorded amendment, never a
  silent search (the run index accounts for every attempt,
  Spec 089).

### Falsifier (fixed in this scoping record, per C095-16)

The benchmark's premise — that the 2025 corpus, as openly
published, supports an independent reproduction of the paper's
results — is **falsified** if, at execution, Leg A fails on a
majority of its ten counts *and* the divergences trace to the
published corpus or the paper's stated methods rather than to
the reproduction implementation (traced by re-derivation from
the pinned data), or if the corpus repository proves
unavailable or unlicensable for scholarly reproduction use at
step 0. In either case the benchmark's outcome record is NOT
REPRODUCED / NOT EXECUTABLE AS SCOPED, filed as the result —
which is itself the calibration finding RT-35 exists to be
able to produce.

## 4. What execution requires

1. **A separate owner commission** (C095-16: execution "is a
   separately commissioned study, not a stage of this spec").
2. **Step 0, fail-closed:** pin the corpus repository by
   commit hash; record its license; enter the corpus under an
   identity record per C095-3 (version, hash, source,
   licensing, counts under a named basis, normalization —
   including the `E`/`o` convention — orientation basis) before
   any computation. A licensing bar or a missing repository
   closes the study at step 0.
3. **The independence rule** (§3) and the run discipline of
   record (Spec 089 run index; every attempt accounted).
4. **Reporting** per the Standards of Record, Part II (effect
   sizes and intervals where quantities are stochastic;
   multiplicity family = the three legs' fixed criteria;
   precision basis stated), and Part I for any equivalence
   phrasing.
5. **Adjudication:** the outcome (REPRODUCED / DIVERGED /
   NOT REPRODUCED per leg) is recorded as a study record under
   the program's claim machinery at execution; nothing in the
   outcome moves any Indus record.

## 5. What the benchmark does not establish

C095-16's bound, carried in substance verbatim: the deciphered
Meroitic values validating the fixture's answer key do **not**
validate any Indus method. The benchmark tests pipeline
fidelity on a solved script; transfer to an undeciphered
script is a separate claim requiring its own evidence. A fully
successful reproduction establishes that the program can
reproduce a published computational result from its published
data — a calibration fact about the platform, and nothing
about Meroitic's remaining unknowns (its grammar and most of
its vocabulary stay as undeciphered after the benchmark as
before it).

## 6. Open questions left for the owner

1. **Commissioning and queue position.** Whether and when to
   commission execution, against the adopted queue (D-095-2) —
   the register takes no position.
2. **Leg B's reading.** The interpretation in §2 (the claim's
   "sign-frequency and positional results" mapped onto Legs
   A–C) is the scoping's; a narrower reading drops Leg B to an
   extension. Either reading leaves Legs A and C intact.
3. **REM.** Whether any future study should approach the REM
   inscription images (transcription labour, institutional
   terms) is beyond this benchmark and is not scoped here.

## Sources relied on, with verification state

| Source | What it grounds | State |
|---|---|---|
| Spec 095 claims.md (C095-16), tasks.md (T502), register-draft.md (RT-35) | The commission, the fixture's standing, the acceptance shape | Program record, read in the clone at `c2be9869` |
| `backend/glossa_lab/data/meroitic.py`; `experiments/_legacy/meroitic_benchmark.py`; `outputs/meroitic_benchmark.json`; `docs/undeciphered_scripts.md` | The fixture, its census, its limits, the priority map | Program record; census re-derived at scoping (551 tokens / 50 lines / 19 signs) |
| Otten & Anastasopoulos 2025, ACL Anthology 2025.alp-1.11 (DOI 10.18653/v1/2025.alp-1.11) | The corpus construction, Table 1, §5.3 counts, Table 2, §6/§6.2 results, the REM limitation | Read in full for this scoping (publisher's PDF) |
| The corpus repository (github.com/Joshua-Otten/Meroitic-Corpus) | Existence and public availability, as stated in the paper's fn. 1 | **UNVERIFIED at the repository itself** — not visited by this scoping (no corpus acquisition); license and current commit are execution step-0 acts |
| The review's citation of the 2025 paper via a Wiley-hosted link | Superseded by the ACL identification above | Corrected on this record; the review's substance (2025 computational corpus + baselines) matches the identified paper |
