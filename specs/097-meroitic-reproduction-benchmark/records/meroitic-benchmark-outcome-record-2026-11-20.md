# Meroitic Benchmark — Outcome Record (Spec 097, Stage 2–3)

**Date: 2026-11-20. Program: Spec 097, Meroitic Reproduction
Benchmark Program. Target: Otten & Anastasopoulos, "Towards
Ancient Meroitic Decipherment: A Computational Approach",
ALP@NAACL 2025, pp. 208–219 (ACL Anthology 2025.alp-1.11,
DOI 10.18653/v1/2025.alp-1.11). Criteria and falsifier as fixed
in the founding scoping (Spec 095 Stage 5) and the execution
freeze filed at Stage 1; neither was moved after computation.**

## Verdict

**Overall outcome: NOT REPRODUCED**, under the program's fixed
falsifier (C097-5): Leg A fails on a majority of its ten counts
(6 of 10), and the divergences trace to the published corpus
and the paper's stated methods — specifically, to material the
published record does not contain (the processed corpus, the
Ramses scrape, the Nubian scanning output) and to repository
state after publication. Per-leg verdicts, exactly as the
criteria read:

- **Leg A (census): NOT REPRODUCED** — 4 of 10 counts exact;
  6 diverged, each with its cause named below (C097-2's
  reporting requirement is satisfied for every count).
- **Leg B (sign inventory and distribution): NOT REPRODUCED**
  — criteria (i) and (ii) fail on both frozen bases; criterion
  (iii) administered and archived.
- **Leg C (alignment): DIVERGED** — the headline pattern at
  100 dimensions reproduces (training accuracy at or below
  20 percent, numerals best in the primary arm in 2 of 3
  seeds), but the fixed points do not hold cell-for-cell:
  unseen precision@10 is not exactly 0 percent in the seeded
  cells, and the at-most-25 percent training band is exceeded
  in some non-100d cells.

A NOT REPRODUCED outcome under this falsifier is a statement
about the published record's completeness for reproduction,
not a judgment on the paper's scholarship beyond
reproducibility (C097-5, "does not establish").

## Venues

Step 0 and all three legs were computed on the **mini-server**
(worker clone and scratch under `~/glossa-work/`), before the
owner's venue transition of 2026-11-20. After the transition,
the corpus custody and all run state were transferred to
**tower-compute** and verified there (step-0 manifest 30/30
files hash-equal; ledger and run-record hashes equal on both
hosts). The Leg A census scripts were re-run on tower-compute
as a grounding check and reproduced the filed numbers exactly;
the program registration, gates, and verification runs for the
landings ran on tower-compute. No benchmark computation ran
inside the Muse VM at any point; the VM prepared files only.
No Indus claim, anchor, or standing was changed by any part of
this work (C097-6).

## Step 0 (C097-1) — held

Pin `c9158f6865325877112b6b9ceef83b3c80a93c56` of
`Joshua-Otten/Meroitic-Corpus`; license **none** (no LICENSE
file, GitHub API license null). Ruling of record (identity
record, Stage 1): scholarly reproduction only, corpus held in
custody, never committed to this repository or redistributed;
only the program's own code and derived aggregate statistics
are published. The falsifier's step-0 arm (NOT EXECUTABLE AS
SCOPED if the repository is unavailable or unlicensable) is
recorded as **not fired** on that basis; the stricter reading
— that an unlicensed corpus cannot ground a reproduction at
all — is stated openly in the identity record. The processed
corpora and Ramses JSONs the paper's pipeline produced are not
in the repository at any commit, and `Code/vecmap` is a gitlink
with no `.gitmodules`, so the alignment code was necessarily
the program's own implementation (Artetxe et al. 2018 steps,
as frozen). Independence: the authors' code was read for the
mapping scheme only; every reading is logged in the identity
record.

## Leg A — census (C097-2)

Counting bases as frozen; alternatives enumerated in the
freeze were never selected post hoc. Reproduced values are
from the pinned corpus; the tower-compute grounding re-run
reproduced every value below exactly.

| # | Published | Reproduced | Reading |
|---|-----------|------------|---------|
| A1 Table 1, translated Meroitic entries | 193 | **193 exact** (distinct headwords, LobbanVocabList.txt; 195 data rows, 175 carrying translations — the count matches on the distinct-headword basis; the paper's "translated" label against that basis is noted) | EXACT |
| A2 Table 1, Meroitic phrases | 897 | no frozen basis reproduces it (envelope: Millet+Rilly distinct fields 878; +Kalabsha 887; expanded forms 907; cleaned variants 861–885; raw M+R+L lines 1,149) | DIVERGED — the counted processed corpus was never published; Table 1's 897 vs §5.2's 871 differ by 26, consistent with pipeline stages whose intermediate is not in the record |
| A3 Table 1, Egyptian texts | 302 | not countable | NAMED DIVERGENCE — the Ramses scrape material is not in the repository in any form (the paper's scraper is deposited; its output is not) |
| A4 Table 1, Nubian pages | 708 | not countable | NAMED DIVERGENCE — scanning-programme material not in the repository |
| A5 §5.3, phrases pre-augmentation | 871 | no frozen basis reproduces it (closest: join-cleaned Millet+Rilly+Kalabsha+Narrative 872, Δ1; basic Millet+Rilly cleaned distinct 874, Δ3; envelope 838–885 across the frozen cleanings) | DIVERGED — same cause as A2 |
| A6 §5.3, Egyptian types | 1,729 | **1,729 exact** (vocabulary headers of the published dim-100/120 Egyptian embeddings; dim 20/50 carry 1,746, a named variant) | EXACT |
| A7 §5.3, Egyptian tokens | 99,338 | not countable | NAMED DIVERGENCE — no Egyptian corpus text is published |
| A8 §5.3, distinct Meroitic forms post-augmentation | 1,868 | **1,868 exact** (distinct whitespace types in mero-corpus.txt; cross-confirmed by the dim-100/120 Meroitic vocabularies; dim 20/50 carry 1,902, a named variant; \w+ types 1,808) | EXACT |
| A9 §5.3, phrases post-augmentation | 17,257 | 18,090 non-blank lines (17,995 distinct), Δ +833 | DIVERGED — the deposited mero-corpus.txt is not the exact augmented file the paper counted |
| A10 §5.3, words post-augmentation | 782,761 | **782,761 exact** (\w+ token count; whitespace basis 756,028; dot-split 782,750, Δ11) | EXACT |

Table 2 dictionary sizes (standalone-file basis): nouns 26 ✓,
numbers 15 ✓, verbs 14 ✓, titularies 9 ✓, adjectives/adverbs
6 ✓, prepositions 3 ✓ — all exact. **Names: 22 reproduced vs
18 published** — traced cause: repository state after
publication. The combined dictionary file's names section
holds exactly 18 pairs; the standalone names file, added at
the pinned (post-publication) commit, differs by +6 pairs and
−2 orthographic variants.

Falsifier application: 6 of 10 counts fail (A2, A3, A4, A5,
A7, A9 — a majority), and each divergence traces to the
published corpus or the paper's stated methods: the counted
intermediates and source materials were never published (A2,
A3, A4, A5, A7), or the deposited file is not the counted file
(A9). The falsifier's condition is met for Leg A.

## Leg B — sign inventory and distribution (C097-3)

Basis: mero-corpus.txt, letters as signs, 5,011,136 sign
tokens; raw alphabet 39 letters. Full distributions are
archived in the companion `leg-b-results.json`.

- Criterion (i), attested set = the fixture's 19 after
  reconciliation. E-for-/o/ basis only: extras = the 20
  capital/dotted variants plus x; missing = none. Full frozen
  fold (dotted/capital variants folded as stated in the
  freeze): attested set 22, extras = **L, P, U**; missing =
  none. **Fails on both bases** — nothing the fixture lists is
  absent from the corpus, but the corpus attests signs outside
  the reconciled 19 under either reading.
- Criterion (ii), frequency ranks vs the fixture's ME rank
  order at Spearman ρ ≥ 0.90. E-only basis: ρ = **0.314**
  (p 0.190); corpus rank order e i t l o m w y r d k q a b s n
  p h g. Full fold: ρ = **0.258** (p 0.286). **Fails** on both
  bases, far below the bar. (For scale: the fixture's own
  551-token constructed corpus also does not follow its stated
  rank order.)
- Criterion (iii), positional (initial/medial/final)
  distributions: computed for every attested sign on the full
  fold and archived in the companion JSON. Administered.

Leg B verdict: **NOT REPRODUCED**. Per C097-3's "does not
establish": this measures the fixture's stated frequency-rank
convention against the 2025 corpus; it is not a finding about
Meroitic sign values, which are not in question.

## Leg C — alignment (C097-4)

The program's own VecMap implementation (Artetxe et al. 2018:
normalize/center/whiten, adversarial initialization for the
unsupervised setting, iterative Procrustes refinement with
CSLS dictionary induction in both directions, stochastic
dropout, symmetrization), CSLS k = 10, precision@10 = gold in
top 10, seeds 42/1337/2025, settings {unsupervised,
numerals-seeded, nouns-seeded} × dims {20, 50, 100, 120}, two
arms (Arm 1 primary: published embeddings both sides; Arm 2
secondary: program-trained Meroitic Word2Vec under the
authors' committed configuration vs published Egyptian).
Attempts accounted: **72 valid runs, 18 superseded, 2 crashed
driver attempts, 1 smoke test** — all in the companion run
indexes. The 18 superseded cells are named for a defect the
program found in its own first driver (dims 100/120 indexed
with the dim-20 word list; those cells evaluated gold pairs at
wrong rows), were marked superseded-invalid, and were re-run
in a repair batch; Arm 2's two crashed attempts (a wrong
corpus path, then the same vocabulary mismatch) are likewise
in the index. The French–English skyline (70% / ~68%) was not
re-run, per the freeze.

Headline reads (percent; full cells in the companion
`leg-c-summary.json`):

- Unseen-dictionary P@10 across all valid runs: **{0.0, 1.19,
  1.45, 1.72, 3.45}** — 0.0 in the unsupervised cells; the
  non-zero values are the seeded cells, at chance level
  (1–3 pairs of 58–84). The paper's fixed point is exactly
  0 percent; the seeded cells do not meet it exactly.
- Training-dictionary accuracy at 100d, Arm 1: numerals
  [13.33, 6.67, 20.0], nouns [11.54, 7.69, 7.69] — inside the
  paper's at-most-20 percent headline, numerals best in 2 of
  3 seeds. Arm 2: numerals [6.67, 6.67, 20.0], nouns [11.54,
  15.38, 11.54].
- The at-most-25 percent training band is exceeded in some
  non-100d cells; the maximum training accuracy anywhere is
  **33.33 percent**.

Leg C verdict: **DIVERGED** — the pattern the paper headlines
at 100d reproduces (low training accuracy, no meaningful
unseen transfer, numerals strongest in the primary arm), but
the fixed points the criteria bind — unseen exactly 0,
training within the band everywhere — do not hold
cell-for-cell, and the record reports them as they stand.

## Claim adjudication

- **C097-1 (step 0 first): held.** Identity record filed
  before computation; the pin resolves to the commit the
  computations used; no corpus file, authors' embedding, or
  authors' code file exists in this repository's tree.
- **C097-2 (Leg A reporting): satisfied.** Every one of the
  ten counts and seven dictionary sizes is either reproduced
  exactly under a frozen basis or reported diverged with its
  traced cause named; no basis appears here that is absent
  from the freeze.
- **C097-3 (Leg B test): administered as specified; criteria
  (i) and (ii) fail, (iii) archived.** The leg's verdict is
  NOT REPRODUCED.
- **C097-4 (Leg C headlines, attempts accounted): the run
  index is complete against the frozen grid** (72 valid + 18
  superseded + 2 crashed, each named); the headlines fall
  outside their fixed points in the particulars named above,
  and the leg is reported DIVERGED rather than in-band.
- **C097-5 (falsifier applied as fixed): applied verbatim.**
  Leg A's majority failure with divergences tracing to the
  published corpus and stated methods gives the overall
  outcome NOT REPRODUCED.
- **C097-6 (no other program record moves): held.** No Indus
  claim, anchor, standing, or fixture was changed by this
  benchmark.

## Companions and remainders

Companions filed with this record: `leg-a-results.json`
(census outputs), `leg-b-results.json` (full sign statistics
including positional distributions), `leg-c-summary.json`
(cell aggregates), `leg-c-runs.jsonl` and
`leg-c-runs-repair.jsonl` (the run indexes, including the
superseded and crashed attempts). Program code (the census
scripts, the sign-statistics script, the VecMap implementation
and drivers) is the program's own and is named in the run
indexes; the corpus, the authors' embeddings, and the
authors' code remain in held custody and are not in this
repository, per the licensing ruling. Remainders: none for
the benchmark itself; the platform's spec-studies register
shows this program's outcome once this record lands and the
serving tree is pulled (the Stage 1 read-back is in the
adoption record's platform evidence).
