# Spec 012 — Phase-113: Blind Language-Affiliation Study, Adversarial Protocol (pre-registration)

**Status:** FROZEN 2026-10-07 on `phase/113-blind-affiliation-adversarial`
(from main f82c81fa, which contains the completed Phase-111 (spec
009) and Phase-112 (spec 010) pipelines and outcomes). Owner
authorization: Tristen Pierson, 2026-10-07 (roadmap item 4 — the
adversarial successor). The git order — design-stage tooling commits
(110c1fe9, dc57566b), then this spec committed before any Phase-113
panel build, gate evaluation, adversarial round, or Indus statistic
exists — is the pre-registration proof.

**Phase-numbering note:** ledger-sequence **Phase-113**. A legacy
script already carries this number
(`backend/scripts/phase113_medium_to_high_upgrade.py`, from an
earlier era). That file is append-only history and is NOT renamed
or reused. All new artifacts carry distinct names
(`phase113_blind_*`, `phase113_features`, `phase113_custodian`,
`phase113_analyst`, `phase113_run`, `phase113_feature_audit`) and
new graph node IDs, per the spec-009/010 precedent.

**AI disclosure:** this study is designed for execution by an AI
agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI. The blinding protocol (inherited
from spec 009 §6; §5 below) is
written for exactly this situation: the executing agent is also
the analyst, so the freeze, the custodian/analyst code separation,
and the no-re-run rules are the controls that substitute for a
human firewall.

## Context — why this study exists

Phase-111 (spec 009) passed its validation gate perfectly, then
failed control validity: S1 (Indus texts with sign order destroyed)
and S2 (i.i.d. draws from the Indus unigram distribution) classified
as linguistic in 100% of draws — its 28-feature vector's power was
carried by unigram statistics. Phase-112 (spec 010) admitted only
permutation-sensitive (order-carrying) features; its gate passed
perfectly again, the traps that killed Phase-111 (S1, S2) and the
inherited S3/S4 were rejected in every draw — and the run was
invalidated by the one new trap, **S5**: a grammar-free positional
template matching R1's text lengths exactly, its unigram profile
to TV = 0.0419, and its **relative-position bigram statistics by
construction** sat in family space in 100% of draws.

The recorded lesson, twice confirmed: **a fixed trap is beaten by
the next subtler mimic.** Any frozen feature family creates a
mimicry surface of exactly its own shape; a control set designed
by hand enumerates only the mimics the designer imagined.
Phase-113 therefore replaces the fixed-trap design with an
**adversarial protocol**: each round, a budgeted, deterministic,
seeded optimizer searches a parametric generator family for
synthetic corpora that (a) match R1 on **all previous rounds'
feature families** and (b) maximize the frozen round classifier's
family assignment. The classifier is credited only with structure
that survives an adversary that was actively trying to fake it.
Feature escalation is by a ladder frozen in this spec (§4) — one
new feature family per round, no mid-study additions.

**Phase-113 asks:** does Indus sign structure — at ladder steps
extending beyond relative-position bigrams into longer-range
sequential and cross-text composition structure — survive
adversarial mimicry at each step, pass the inherited gate at each
step, and (only if every round holds) support a §10 affiliation
verdict under the inherited rules? And, antecedently (§4.4): do
the longer-range features carry enough signal **at the actual
corpus sizes** (Holdat 7,002 tokens; pooled working layer ~11k)
for the question to be askable at all — if not, the study's
pre-registered outcome is INDETERMINATE AT THIS CORPUS SIZE.

## Scope

**In scope (the verdict path):** the ladder feature sets of §4
(L1/L2/L3) + the frozen LDA classifier, evaluated under the
per-round gate (§8/§9), the adversarial rounds (§7/§8), the
inherited final control validity (§8.4), and the verdict rules
(§10).

**Out of scope for verdicts (registered exclusions):**
- All permutation-invariant statistics: excluded from
  classification, exactly as in spec 010 (they may appear in the
  optimizer's round-1 base constraint and in descriptive reporting
  only — never as classifier features).
- Dictionary reading under blind SA assignment (SA falsified by
  Phase-107); segmented-unit features; any anchor/reading change.
  This phase touches no anchors and makes no decipherment claim.

## 1. Panel (inherited from spec 009 as assembled; spec 010 §1)

Identical panel, identical roles and family classes:
`dravidian`, `indo_aryan`, `semitic`, `indo_european_other`,
`isolate_sumerian`, `turkic`, `austronesian`, plus
`non_linguistic`.

| ID | Corpus | Family/class | Panel role |
|---|---|---|---|
| K1 | Linear B (DAMOS, in-repo) | indo_european_other | known |
| K2 | Vedic Sanskrit (Ṛgveda padapāṭha, in-repo) | indo_aryan | known |
| K3 | Classical Sanskrit (DCS Bhāgavatapurāṇa, first 15 files) | indo_aryan | known |
| K4 | Old Tamil (kee2u morpheme sequences, in-repo) | dravidian | known |
| K5 | Sumerian Ur III (CDLI via MTAAC, local only) | isolate_sumerian | known |
| K7 | Ge'ez Genesis (in-repo) | semitic | known |
| K8 | Turkish (UD_Turkish-IMST, addendum-A substitution) | turkic | known |
| K9 | Indonesian (UD_Indonesian-GSD, addendum-A substitution) | austronesian | known |
| N1 | Khipu cord sequences (Open Khipu Repository 2.1.0) | non_linguistic | known |
| S1–S5 | Synthetic controls (spec 009 §5; spec 010 §5) | — | blind |
| A1–A3 | Adversarial corpora (§6/§7; built during the rounds) | — | blind (round artifacts) |
| R1 | Holdat corpus (1,670 texts / 7,002 tokens / 390 signs) | target | blind |
| R2 | ICIT-extracted corpus (4,410 / 14,213 / 714) | target | blind |
| R3 | Mixed pool R1+R2 (namespaces prefixed) | target | blind |

**Staging note (recorded, pre-run):** the Phase-112 worktree that
held the panel staging was removed after Phase-112 closed. The
panel sources were re-obtained from their original openly licensed
origins into `glossa-corpus/indus/sources/phase113/` (gitignored):
Holdat CSV and the restricted-local ICIT file transferred with
SHA-256 equality verified against the Phase-112 record; DCS
re-downloaded (the `Bhāgavatapurāṇa` directory — diacritic name —
first-15-files selection identified by exact reproduction of the
Phase-111 loader statistics); UD treebanks re-cloned; the Open
Khipu Repository 2.1.0 archive re-downloaded from Zenodo (record
18025748, file size 79,808,932 bytes, exact); the MTAAC CDLI Ur III
repository re-cloned from cdli-gh. **Panel equivalence is
verified, not assumed:** every loader-backed corpus's loader
statistics and chunk counts were recomputed from the Phase-113
staging and matched exactly against the committed Phase-111 build
log (`reports/phase111_blind_affiliation_results.json`,
`panel_build_log`) before any Phase-113 run: all eleven loader-backed corpora MATCH (K1, K2, K3, K4, K5,
K7, K8, K9, R1, R2 by direct recomputation; N1 khipu by the
design-stage audit's index-free load, §4.5 note).
The khipu loader equivalence was obtained with the unindexed
upstream DB; the local index `idx_knot_cord_local` was then added
to the extracted staging copy only (loader code untouched) for
build speed, mirroring Phase-112. Full record:
`reports/phase113_acquisition_log.json`.

**Registered gaps (unchanged):** Elamite (no verified openly
licensed machine-readable corpus; the suffixing-isolate confound
is carried by Sumerian alone); K6 Akkadian (ORACC unreachable;
`semitic` carried by Ge'ez alone); N2 proto-cuneiform (no openly
licensed sequence source; attested non-linguistic panel = khipu
alone, with the boundary role additionally carried by the
synthetic and adversarial generators); attested SCA heraldry
(license unverified; S3 substitutes). Recorded caveats stand:
R2's sign order is source-reconstructed, not attested; Holdat
transcriptions carry the CITATIONS A.13 caveat. Power rule: every
assembled corpus supplies ≥ 5,000 clean tokens (as verified in
Phase-111/112; the identical panel is rebuilt here).

## 2. Resampling (inherited from spec 009 §2, unchanged)

Draw size N = 11,000 tokens primary; sensitivity 5,000 / 19,600
(reported, never verdict-bearing). 100 draws per member; draws
0–49 train / 50–99 test for the gates (frozen by index). Target
length distribution = Holdat empirical (lengths 2–8, counts
{2: 269, 3: 330, 4: 415, 5: 330, 6: 164, 7: 116, 8: 46}, mean
4.193). Stream-chunking, draw construction, and the custodian
token remap use the frozen spec-009 code and seed streams, reused
by import (§15.3). Chunking RNG `SeedSequence([20261006,
corpus_index])`; draw RNG `SeedSequence([20261006, corpus_index,
draw_index])`; remap RNG `SeedSequence([20261008, corpus_index])`;
blind-ID assignment RNG `SeedSequence([20261007])` over the
17-member panel list of spec 010 (S5 at corpus_index 35).
Adversarial corpora A_r use corpus_index 40 + r for remapping and
draw construction (§7).

## 3. Unit rules (inherited from spec 009 §3, unchanged)

Token = the sign in source transliteration/numbering (Indus,
Linear B, Sumerian); kee2u morpheme ID (Old Tamil); syllable
(Ge'ez, by character); the frozen Sanskrit IAST syllabifier (spec
009 §3) for K2/K3; the frozen Latin vowel-nucleus syllabifiers
for K8/K9. Representation-level heterogeneity is a recorded
limitation (§12), frozen as in specs 009/010.

## 4. Feature ladder

### 4.1 L1 — family A (frozen, inherited from spec 010 §4.3)

The 16 admitted order-carrying features of spec 010, definitions
and estimators unchanged, in the frozen order:
`term_productivity`, `init_productivity`, `blockH2`, `blockH3`,
`blockH4`, `cond_ent`, `cond_ent_gap`, `cond_ent2`, `ent_incr_43`,
`rep_adj_1`, `rep_adj_3`, `pp_ratio`, `restore_acc`,
`pp_ratio_tri`, `bigram_type_ratio`, `adj_clustering`.

### 4.2 New candidates (design stage; definitions in
`backend/glossa_lab/phase113_features.py`, committed 110c1fe9)

**Family B — longer-range sequential structure (14 candidates):**
`blockH5`, `blockH6` (block entropies, same estimator);
`ent_incr_54` = H₅ − H₄; `ent_incr_65` = H₆ − H₅;
`pp_ratio_ord3` (held-out order-3 perplexity / held-out order-2
perplexity on the frozen 80/20 split; add-α backoff chain as
implemented in the design-stage extractor, extending the
spec-010 trigram model one level); `mi_lag2`, `mi_lag3` (lag-L mutual
information between tokens L apart, normalized by H₁);
`rep_adj_4`, `rep_adj_5`, `rep_adj_6` (exact-lag repetition at
distances 4–6, spec-009 F14–F16 construction);
`adj_clustering_lag2` (clustering of the distance-2 adjacency
graph); `restore_acc_tri` (masked-token restoration by best
trigram successor, spec-010 masking); `ctx_pos_gain`
(context-conditioned sign-choice entropy: the fractional
reduction in next-sign uncertainty from adding the next token's
relative-position bin — S5's 5-bin scheme — to the previous-sign
context); `bigram_type_ratio_lag2` (distinct lag-2 pairs / lag-2
pair tokens).

**Family C — cross-text repetition / composition structure
(6 candidates):** `dup_text_frac` (fraction of texts whose exact
sequence occurs ≥ 2 times in the draw); `dup_token_coverage`
(token share of duplicated texts); `shared_bigram_type_frac`
(fraction of bigram tokens whose type occurs in ≥ 2 distinct
texts); `cross_bigram_texts_mean` (mean distinct-text count per
bigram type, normalized by # texts); `longest_cross_repeat`
(longest n-gram, 3 ≤ n ≤ 12, attested in ≥ 2 distinct texts,
normalized by mean text length); `pair_bigram_overlap` (mean
bigram-multiset overlap coefficient over 2,000 seeded distinct
text pairs, seed stream [20261025, draw]).

### 4.3 Admission rule for new candidates (frozen before the
audit was run)

A family-B or family-C candidate is admitted only if it passes
BOTH audits, each computed on the nine known panel corpora ONLY
(never Indus, never synthetics):

(a) **Permutation-sensitivity audit** (spec 010 §4.1(b) rule,
    verbatim): 20 draws at N = 11,000 (seed stream [20261020,
    corpus_index, draw]) and their within-text permuted
    counterparts (seed stream [20261021, corpus_index, draw]);
    Cohen's d of (original − permuted) per corpus. Admission
    requires median |d| ≥ **0.8**, the same sign of the mean
    difference in ≥ **8 of 9** corpora, and non-degeneracy (SD of
    original draws > 0 in ≥ 5 corpora). A mechanical toy test
    (spec 010 §4.1(a) pattern: the feature changes by > 0.002
    under a seeded within-text permutation on at least one of
    two structured toy corpora) is a precondition, verified by
    unit test at design stage.
(b) **Power audit** (new in this spec): 20 draws at
    N = **7,002** — Holdat's exact token count — per known corpus
    (seed stream [20261024, corpus_index, draw]). For each
    candidate, Cohen's d between every pair of the 8 known
    classes (corpora pooled within class; 28 pairs). Admission
    requires the median pairwise |d| at N = 7,002 ≥ **0.5**.

A candidate failing either audit is dropped BEFORE this freeze,
and the drop is recorded in §4.5. The audit's full numeric record
is `reports/phase113_feature_audit.json` (committed with this
spec).

### 4.4 Power analysis and the INDETERMINATE outcome (frozen)

From the same power draws (§4.3(b)), LDA classifiers (frozen
implementation, shrinkage λ = 0.1) are trained on draws 0–9 and
evaluated on draws 10–19 at N = 7,002 for three feature sets:
L1 alone; L1 + admitted B; L1 + admitted B + admitted C (the full
ladder L3). Family balanced accuracy is computed over the 7
family classes exactly as in the §9 G2 evaluation (non-linguistic
draws excluded); the binary linguistic balanced accuracy is
recorded for the report only.

**INDETERMINATE AT THIS CORPUS SIZE** is the study's
pre-registered outcome — firing before any round is run — if
either criterion holds, evaluated mechanically from
`reports/phase113_feature_audit.json`:

- **(a)** the total number of admitted new features (family B ∪
  family C) is < **3** — the extension beyond position-bigrams
  is empty in substance; or
- **(b)** the full-ladder (L3) family balanced accuracy at
  N = 7,002 is < **0.70** — the method cannot validate family
  discrimination at the target's true corpus size, so an
  11,000-token verdict would rest on resampling inflation
  (draws at 11,000 from a 7,002-token corpus reuse texts).

If INDETERMINATE fires, the phase closes with the spec, the
audit/power record, and this outcome as its results; no panel
build, gate, round, or Indus statistic is produced. This outcome
is a first-class result of the design, not a failure of it: it
prices the corpus-size constraint exactly.

### 4.5 Audit outcome (recorded at freeze; numbers from
`reports/phase113_feature_audit.json`)

Permutation audit (20 draws at N = 11,000 per known corpus;
median |Cohen's d| of (original − within-text permuted), sign
consistency, non-degenerate corpora; admission ≥ 0.8 / ≥ 8/9 /
≥ 5/9) and power audit (median pairwise between-class |Cohen's
d| over the 28 class pairs at N = 7,002; admission ≥ 0.5):

| Candidate | Family | Perm. median \|d\| | Signs | Nondeg | Perm. | Power med \|d\| @7,002 | Admitted |
|---|---|---|---|---|---|---|---|
| blockH5 | B | 2.737 | 9/9 | 9/9 | pass | 4.417 | **yes** |
| blockH6 | B | 1.595 | 9/9 | 9/9 | pass | 2.695 | **yes** |
| ent_incr_54 | B | 3.727 | 7/9 | 9/9 | fail (signs) | 3.030 | no |
| ent_incr_65 | B | 0.445 | 7/9 | 9/9 | fail (median, signs) | 0.860 | no |
| pp_ratio_ord3 | B | 4.794 | 6/9 | 9/9 | fail (signs) | 2.234 | no |
| mi_lag2 | B | 6.109 | 9/9 | 9/9 | pass | 18.628 | **yes** |
| mi_lag3 | B | 2.846 | 8/9 | 9/9 | pass | 14.631 | **yes** |
| rep_adj_4 | B | 1.067 | 8/9 | 9/9 | pass | 3.456 | **yes** |
| rep_adj_5 | B | 0.998 | 7/9 | 9/9 | fail (signs) | 2.229 | no |
| rep_adj_6 | B | 0.629 | 6/9 | 9/9 | fail (median, signs) | 2.109 | no |
| adj_clustering_lag2 | B | 2.269 | 9/9 | 9/9 | pass | 6.595 | **yes** |
| restore_acc_tri | B | 6.210 | 9/9 | 9/9 | pass | 2.043 | **yes** |
| ctx_pos_gain | B | 6.155 | 6/9 | 9/9 | fail (signs) | 12.955 | no |
| bigram_type_ratio_lag2 | B | 9.409 | 9/9 | 9/9 | pass | 12.436 | **yes** |
| dup_text_frac | C | 11.996 | 9/9 | 9/9 | pass | 11.957 | **yes** |
| dup_token_coverage | C | 11.473 | 9/9 | 9/9 | pass | 11.418 | **yes** |
| shared_bigram_type_frac | C | 31.164 | 9/9 | 9/9 | pass | 12.310 | **yes** |
| cross_bigram_texts_mean | C | 22.766 | 9/9 | 9/9 | pass | 12.235 | **yes** |
| longest_cross_repeat | C | 8.315 | 8/9 | 9/9 | pass | 0.738 | **yes** |
| pair_bigram_overlap | C | 2.170 | 8/9 | 9/9 | pass | 3.333 | **yes** |

Recorded honestly: the power audit admitted all 20 candidates
(the smallest median pairwise |d| at N = 7,002 is
`longest_cross_repeat` at 0.738); every exclusion was made by
the permutation audit — six family-B candidates whose
permutation response, though large in magnitude for several
(`pp_ratio_ord3`, `ctx_pos_gain`), does not have a consistent
sign across corpora, so they do not certify order-carrying
signal in the frozen sense. Family C admitted 6 of 6.

Ladder power at N = 7,002 (LDA, train draws 0–9 / test 10–19 of
the §4.3(b) power draws): L1 family BA **1.000**, binary BA
1.000; L1 + B family BA **1.000**, binary BA 1.000; full ladder
L3 family BA **1.000**, binary BA 1.000.

**INDETERMINATE evaluation (§4.4), mechanical:** criterion (a)
— admitted new features = 14 ≥ 3 → does not fire. Criterion (b)
— full-ladder family BA at N = 7,002 = 1.000 ≥ 0.70 → does not
fire. **INDETERMINATE AT THIS CORPUS SIZE does not fire; the
adversarial rounds proceed.** (N1's loader statistics were
recorded by this audit's index-free khipu load — documents 619,
cords 54,403, tokens 110,151, vocab 10, texts after chunking
26,289 — completing the §1 equivalence verification.)

**Ladder (frozen):** L1 = family A (16 features, §4.1).
L2 = L1 + admitted family B (`blockH5`, `blockH6`, `mi_lag2`,
`mi_lag3`, `rep_adj_4`, `adj_clustering_lag2`, `restore_acc_tri`,
`bigram_type_ratio_lag2` — 24 features). L3 = L2 + admitted
family C (`dup_text_frac`, `dup_token_coverage`,
`shared_bigram_type_frac`, `cross_bigram_texts_mean`,
`longest_cross_repeat`, `pair_bigram_overlap` — 30 features). If a family admits zero features, its ladder
step runs with the previous step's feature set — the round still
escalates through the §7 matching constraint, which grows every
round regardless (§7).

## 5. Fixed synthetic controls S1–S5 (inherited, unchanged)

S1–S4 are the frozen spec-009 §5 algorithms and S5 is the frozen
spec-010 §5 positional-bigram template generator, all reused by
import, with their frozen seed streams. S3/S4 keep their disclosed
generator-training instances (classes `gen_heraldic` /
`gen_administrative`); S5 has no disclosed instance and no class,
exactly as in spec 010.

**Blinding (inherited from spec 009 §6, unchanged).** The
custodian materializes the panel as anonymized feature matrices
(`panel.json`: blind IDs, the ladder feature vectors, per-size
draws) and withholds the identity key until the rounds complete
and the C_3 classification has run; the key then opens exactly
once, on the record (unblinding timestamp + code hash in the
results file). The analyst module imports nothing from the
custodian (unit-tested invariant). The §7 optimizer is
custodian-side and orchestrator-mediated (features and scalars
only), so the adversarial search cannot leak identities into the
analyst path; R1's own statistics are custodian data by design,
exactly as S1–S5 were custodian-built from R1 in specs 009/010.

## 6. Adversarial generator family G(θ) (frozen)

All component statistics are computed from R1's chunked texts by
the custodian. Generated text lengths always follow the frozen
target length distribution (§2); generation continues until
≥ 5 × N_PRIMARY tokens. Corpus-level copy probability and
per-token mode mixture define θ:

θ = (w_P1, w_P2, w_P3, w_G2, w_G3, β_P2, β_P3, β_G2, β_G3,
     p_burst, p_copy)

with (w_P1, …, w_G3) on the 5-simplex, each β ∈ {0.3, 1.0, 3.0},
p_burst ∈ [0, 0.25], p_copy ∈ [0, 0.30].

Components (b(j, L) = ⌊5j/L⌋ is S5's relative-position binning;
U_b = positional unigram distribution of bin b; U = global
unigram distribution of R1):

- **P1** positional unigram: x ~ U_{b(j,L)}.
- **P2** positional bigram: S5's exact transition —
  P(y|x) = (C_{b,b′}(x→y) + β_P2·U_{b′}(y)) / (C_{b,b′}(x→·) +
  β_P2), b = b(j−1, L), b′ = b(j, L).
- **P3** positional trigram: P(z|x, y) = (C_{b,b′,b″}(x,y→z) +
  β_P3·P2_{b′,b″}(z|y)) / (C_{b,b′,b″}(x,y→·) + β_P3), where
  P2_{b′,b″}(·|y) is the P2 successor distribution with β_P2.
- **G2** global bigram: P(y|x) = (C(x→y) + β_G2·U(y)) /
  (C(x→·) + β_G2).
- **G3** global trigram: P(z|x, y) = (C(x,y→z) + β_G3·G2(z|y)) /
  (C(x,y→·) + β_G3).
- **BURST:** independently per token position j ≥ 1, with
  probability p_burst, emit x_{j−1} again (overrides the mode
  draw).
- **COPY (text level):** with probability p_copy, a text is a
  verbatim copy of a uniformly chosen previously generated text
  of the same build (the first text of a build is never a copy).

Token generation for a non-copied text: x₀ ~ U_{b(0,L)}; for
j ≥ 1, draw a mode from w, then sample from that mode's
distribution given the available context; modes needing more
context than the position affords fall back down the chain
(P3→P2→P1, G3→G2→P1, P2/G2 at j = 1 use the single available
predecessor). Sampling is by inverse-CDF over sorted supports
(deterministic given the RNG stream).

**Sanity anchor (unit-tested):** θ_S5 = (w_P2 = 1, β_P2 = 1.0,
p_burst = 0, p_copy = 0, other weights 0) reproduces S5's
construction: its generated corpora must match the frozen S5
generator's on positional-bigram fidelity (total-variation
distance between the two generators' relative-position bigram
distributions < 0.10 on a seeded 20,000-token comparison) and on
unigram TV to R1 (< 0.10).

## 7. Optimizer (frozen)

Per round r ∈ {1, 2, 3}, against the frozen round classifier C_r
(§8):

- **Mediation.** The optimizer runs custodian-side. For each
  candidate θ it generates a corpus (seed stream [20261030, r,
  eval_index]), the custodian remaps it (corpus_index 40 + r) and
  extracts L_r features for 16 draws at N = 11,000 (draw seed
  stream [20261006, 40 + r, draw_index]); the orchestrator passes
  only the feature matrix to the frozen C_r and returns the
  scalar objective and the constraint report. The optimizer never
  sees posteriors per draw, class names, or any corpus identity
  beyond R1 (whose statistics define G by design, as S1–S5 were
  defined from R1 in specs 009/010).
- **Objective.** Mean family posterior mass (summed over the 7
  family classes) of the 16 evaluation draws under C_r — to be
  MAXIMIZED.
- **Constraints (feasibility), checked on the same 16 draws.**
  Round 1 (base family): unigram total-variation distance
  between the candidate corpus and R1 ≤ **0.05** (text lengths
  match the target distribution exactly by construction).
  Round r ≥ 2: for EVERY feature f in L_{r−1} (the previous
  ladder step's full feature set), the candidate's 16-draw
  median of f must lie within R1's [10%, 90%] percentile
  interval over R1's 100 primary panel draws (custodian-computed
  from the panel; R1 feature values are panel data, not new
  Indus statistics — they were computed blind in every prior
  phase before unblinding as well).
  Ranking: feasible candidates outrank infeasible ones; among
  infeasible, fewer violated constraints wins, then higher
  objective; among feasible, higher objective wins. Ties broken
  by lower eval_index.
- **Search (deterministic, budget 200 evaluations per round).**
  Round 1 candidate 0 is θ_S5 (forced, recorded). Remaining
  candidates 1–119 (rounds 2–3: 0–119): w ~ Dirichlet(1,1,1,1,1),
  each β uniform on the grid, p_burst ~ U[0, 0.25], p_copy ~
  U[0, 0.30], all from RNG stream [20261031, r] consumed in
  order. Candidates 120–199: coordinate refinement of the
  incumbent best — slot s perturbs coordinate (s mod 11) of the
  incumbent: a weight coordinate is multiplied by
  exp(N(0, 0.35)) from the same stream and the simplex
  renormalized; a β moves one grid step (direction alternating
  by slot parity, clipped at the grid ends); a probability
  coordinate moves by U[−0.05, +0.05] from the same stream,
  clipped to its range. The incumbent updates only on strict
  improvement of the ranking key.
- **Round artifact A_r.** 100 draws at the selected θ*_r,
  generated with seed [20261030, r, 999] (a stream never used in
  search), remapped at corpus_index 40 + r, features extracted
  for the full ladder L3 (so A_r can be re-checked under C_3 in
  §8.4 from stored matrices). θ*_r, the full construction (§6),
  the search trace summary (best objective by candidate block,
  feasibility of the winner), and the generated corpus statistics
  are recorded in the results file. The defeating-generator
  disclosure rule (§8.3) requires nothing less.

## 8. Rounds protocol, gates, and control validity

### 8.1 Round r (r = 1, 2, 3), in order

(i) **Gate for C_r.** Train the gate instance of the round
    classifier (L_r features, known draws 0–49) and evaluate the
    §9 gate on known draws 50–99. Gate failure → **STOP**:
    verdict `INCONCLUSIVE — GATE FAILED` (the round is recorded;
    no classification of any blind item under C_r or later
    rounds).
(ii) **Freeze C_r.** Train the round's final-model instance
    (L_r features; all 100 draws of every known corpus plus the
    disclosed S3/S4 generator-training instances as classes
    `gen_heraldic` / `gen_administrative` — the spec-009 final
    model construction, restricted to L_r). This instance is
    frozen for the round; the §7 optimizer and the §8.2 check
    use it and no other.
(iii) **Adversarial search.** Run §7 against the frozen C_r.
(iv) **Round control check (§8.2).**

### 8.2 Round control validity

A_r's 100 draws, classified by the frozen C_r, must be classified
non-linguistic (binary collapse: posterior mass on
`non_linguistic` + `gen_heraldic` + `gen_administrative` ≥
posterior mass on all family classes) in ≥ **95%** of draws.
Failure → **STOP**: verdict `INVALID RUN — CONTROL VALIDITY
FAILED`, recorded as fired at round r, with A_r's construction
reported in full (§7). No later round runs; no §10 verdict rule
fires.

### 8.3 Defeating-generator disclosure

If any round's optimized generator defeats its frozen classifier,
the results file and summary report the generator completely:
θ*_r, component definitions (§6), the constraints it satisfied
(with the numeric medians vs R1's intervals), its objective
trajectory summary, and its control share. An invalid run whose
defeating mechanism is not fully reconstructible from the record
is a protocol breach, not a result.

### 8.4 Final control validity (inherited §8 of specs 009/010,
extended)

Only if all three rounds hold: under C_3 (the round-3 frozen
final-model instance), **each** of S1, S2, S3, S4, S5, A_1, A_2,
A_3 must be classified non-linguistic (same collapse) in ≥ 95%
of its 100 draws (A_r re-checked from their stored L3 matrices).
Any failure → verdict `INVALID RUN — CONTROL VALIDITY FAILED`
(the failing control is recorded). This section is conjunctive
with §8.2, exactly as spec 009/010 §8 was conjunctive across its
controls.

## 9. Validation gate (inherited from spec 009 §7, unchanged)

Evaluated per round (§8.1(i)) on held-out test draws (50–99) of
the known corpora with that round's gate instance:

- **G1 (linguistic):** balanced accuracy of the binary task
  (linguistic = any family class; non_linguistic = N1) ≥ **0.85**,
  AND the lower bound of its 95% bootstrap CI (2,000 seeded
  resamples, seed `SeedSequence([20261011])`) > **0.70**.
- **G2 (family):** balanced accuracy over the 7 family classes
  ≥ **0.70**, AND permutation p < **0.001** (1,000 seeded label
  permutations, seed `SeedSequence([20261010])`), BH-adjusted
  per §11.

## 10. Indus verdict rules (inherited from spec 009 §9,
unchanged; applied with C_3)

Applied only if every round's gate passes, every round's control
check holds, and final control validity (§8.4) holds.
"Linguistic posterior" of a draw = summed posterior over the 7
family classes.

- **V1 replicate consistency:** R1, R2, R3 must agree on the
  binary verdict (median linguistic posterior ≥ 0.5) and, if a
  family winner is named, on the winner. Any disagreement →
  **UNSTABLE / INCONCLUSIVE**.
- **V2 linguistic verdict:** "linguistic" requires BF ≥ **10**
  for linguistic over EACH of: S3 (gen_heraldic), S4
  (gen_administrative), and the best-matching attested
  non-linguistic class (N1) — per replicate, in all three
  replicates. Failure in any replicate → **NOT ESTABLISHED**.
- **V3 family support:** a family is SUPPORTED only if ALL hold:
  median posterior of the winning family ≥ **0.90** in each
  replicate; BF ≥ **10** vs the runner-up family; BF ≥ **10** vs
  S3 and vs S4 classes; the same winner in R1 and R2 (both sign
  lists); and in each of R1 and R2, ≥ **90%** of draws have
  argmax = the winning family.
- **V4 refutation / no discrimination:** if the top two families
  differ by BF < **3**, OR the bootstrap 95% CI of their median
  posterior difference lies within **±0.05** (TOST, α = 0.05),
  the verdict is **NO FAMILY DISCRIMINATION**.
- **V5 suffixing-confound rule:** if the winner is `dravidian`
  but `isolate_sumerian` falls within the V4 equivalence band of
  it, the verdict is **NO FAMILY DISCRIMINATION (suffixing
  confound not excluded)**. Mutatis mutandis for any winner tied
  by a typologically similar confound class.
- **V6 verdict vocabulary (exhaustive):** exactly one of
  `SUPPORTED: <family>` (only via V3 with V5 not triggered),
  `NO FAMILY DISCRIMINATION`,
  `NO FAMILY DISCRIMINATION (suffixing confound not excluded)`,
  `NOT ESTABLISHED`, `UNSTABLE / INCONCLUSIVE`,
  `INCONCLUSIVE — GATE FAILED`,
  `INVALID RUN — CONTROL VALIDITY FAILED`,
  `INDETERMINATE AT THIS CORPUS SIZE` (§4.4; pre-rounds outcome).
  No narrative upgrading of any verdict is permitted in any
  program artifact.

## 11. Multiplicity (inherited from spec 009 §10, unchanged)

Primary p-valued tests: (T1) gate linguistic bootstrap test,
(T2) gate family permutation test — each evaluated per round,
with the round-1 instances primary and later rounds' recorded as
gate re-checks of the same two hypotheses on nested feature sets;
(T3) Indus linguistic margin vs S3 (draw-exceedance), (T4) same
vs S4, (T5) Indus family margin vs runner-up. Benjamini–Hochberg
at q = **0.05** across T1–T5 (tests not reached are recorded as
not-run and excluded). Effect thresholds (§§8–10) stand as frozen
regardless; BH-adjusted significance is additionally required for
any test whose p-value is cited in support of a verdict. All
other analyses are exploratory and cannot upgrade a verdict.

## 12. Deviations (inherited policy)

Any change to §§1–11 after this freeze requires: (i) a written
deviation note in this spec (dated addendum), (ii) a spec v2
commit BEFORE any re-run, (iii) disclosure in the results summary
and PR body, (iv) re-running from the panel build (no partial
re-use of pre-fix artifacts). Deviations discovered after
unblinding additionally require the unblinded results to be
reported alongside the corrected ones, labelled superseded, never
deleted.

### 12.1 Addendum (2026-10-07) — §6 sanity-anchor qualification

Post-execution records addendum under the §12 policy. No re-run
was performed; no frozen rule, threshold, or outcome is changed
by this note.

The §6 sanity anchor requires positional-bigram TV between
G(θ_S5) and the frozen S5 generator < 0.10. That figure is
statistic-dependent. Under the finest-grained reading of the
statistic — the frequency-weighted per-(b, b′, x)-context TV
implemented as `positional_bigram_tv` — the 0.10 threshold sits
below the sampling-noise floor: two samples drawn from the
IDENTICAL model at ~55k tokens already sit at TV 0.246, and
G(θ_S5)-vs-S5 measured 0.243 — no systematic excess over the
noise floor. The committed unit test
(`backend/tests/test_phase113_blind.py`) therefore asserts the
anchor as: positional-bigram TV < 0.30 AND TV ≤ noise floor +
0.05, plus unigram TV to R1 < 0.10 (measured 0.038). Under the
coarser per-bin-pair successor-TV reading of the same statistic,
the G(θ_S5)-vs-S5 value is 0.064, which does meet the 0.10
figure as written in §6.

The anchor's substance — that θ_S5 reproduces S5's construction
— is confirmed three ways: (i) S5's recorded unigram TV to R1
(0.0419, specs 010/012) is reproduced exactly under the test's
mapping; (ii) no systematic excess over the identical-model
noise floor (0.243 vs 0.246); (iii) in the run itself, candidate
0 — the forced θ_S5 — behaved exactly as S5 did: objective
0.99999995 under C_1, unigram TV 0.0383.

No study outcome depends on the anchor's threshold. The
INVALID-at-round-1 verdict rests solely on the frozen rounds
protocol (§§7–10): the round-1 artifact A_1's control share of
0.00 against the ≥ 0.95 requirement of §8.2. This addendum
qualifies the reading of the §6 anchor; it does not amend §6.

## 13. Limitations (registered at freeze time)

- All spec-009 §12 limitations stand, as carried through spec
  010 §12 (representation-level heterogeneity, genre mismatch,
  chunked positional features, bootstrap-draw dependence, R2's
  reconstructed sign order, Elamite's absence, Holdat's A.13
  caveat; the gate's attested non-linguistic class is khipu
  alone, an inherited weakness the rounds partially mitigate but
  do not remove — the adversarial controls test the family side
  of the boundary, not the attested-non-linguistic side).
- **The adversary is bounded, and the bound is part of the
  claim.** A round holds means: *this* generator family (§6),
  searched by *this* optimizer (§7) at *this* budget (200
  evaluations), did not produce a feasible corpus that the
  frozen C_r assigns to family space in > 5% of draws. It does
  NOT mean no non-linguistic process can mimic the ladder
  features. Stronger future adversaries (richer families, larger
  budgets) remain possible and would be future specs.
- **The generator family is R1-derived by design.** G's
  components are built from R1's own statistics, like S1–S5
  before it: the rounds test whether R1's structure exceeds
  what R1-derived template/Markov processes of bounded order
  (≤ trigram, positional or global) plus copying and bursting
  can reproduce. A process class outside §6 (e.g., hierarchical
  constituency, long-range agreement beyond trigram context) is
  tested only insofar as the ladder features respond to it.
- **Feature ceiling at corpus size.** Texts are short (target
  lengths 2–8); trigram-and-beyond statistics rest on few
  windows, and cross-text features on resampled text pools whose
  duplication profile is partly a resampling artifact (draws
  sample texts with replacement). §4.4 exists because this
  ceiling may bind before the rounds begin; if it does not bind,
  it still attenuates every longer-range effect the rounds can
  detect.
- **Round classifiers are nested, not independent.** L1 ⊂ L2 ⊂
  L3 by construction; the three gates are re-checks on nested
  feature sets, and the rounds' adversaries face monotonically
  stronger matching constraints. The protocol is a single
  escalating test, not three independent studies.
- The study's ceiling is calibrated evidential support or
  refutation of feature-based affiliation claims under an
  explicitly bounded adversary. It can never refute "the Indus
  language was in family X" in full, and it touches no reading,
  anchor, or decipherment claim.

## 14. Licensing (inherited from spec 009 §13; owner directive 2026-10-06)

Publish nothing that requires permission we do not hold. The
panel's sources and licenses are exactly Phase-111/112's (DCS
CC BY 4.0; CDLI via MTAAC repo CC0 / underlying CDLI CC BY-NC
4.0, local computation only; UD_Turkish-IMST CC BY-NC-SA 4.0 and
UD_Indonesian-GSD CC BY-SA 4.0, local only; Open Khipu Repository
MIT; in-repo corpora per their acquisition records; R2
restricted-local, local computation only, never committed).
Phase-113 downloads nothing new: it re-obtained the identical
files from the same origins after the Phase-112 staging was lost
(§1 staging note), recorded in
`reports/phase113_acquisition_log.json`. Raw texts live only in
the gitignored store; committed artifacts are code, this spec,
the audit + acquisition logs, feature definitions, and results —
never source texts. NEVER ingest: ETCSL, Project Madurai, any
Elamite edition.

## 15. Deliverables (frozen)

1. Design-stage tooling commits (110c1fe9, dc57566b):
   `backend/glossa_lab/phase113_features.py` (family B + C
   candidates), `backend/scripts/phase113_feature_audit.py`
   (permutation + power audits), design-stage tests in
   `backend/tests/test_phase113_blind.py`.
2. This spec (own commit), including the §4.5 audit tables;
   `reports/phase113_feature_audit.json`;
   `reports/phase113_acquisition_log.json` (Phase-107 format);
   ledger freeze entries (root `LEDGER.md` +
   `glossa-indus/LEDGER.md`) with AI disclosure.
3. Pipeline: `backend/glossa_lab/phase113_custodian.py` (panel
   build with per-member checkpoints; S1–S5 by import;
   adversarial generator G and the §7 optimizer),
   `backend/glossa_lab/phase113_analyst.py` (ladder-aware gate /
   round models / verdict; reuses the frozen spec-010 LDA and
   verdict primitives by import where identical),
   `backend/glossa_lab/phase113_run.py` (rounds stage +
   classify stage), H23 graph registration
   (`backend/glossa_lab/experiment_graph_phase113.py`, nodes
   `IndusPhase113BlindRounds` / `IndusPhase113BlindClassify`,
   verified in `ATOMIC_NODES`) before any run; entry scripts
   `backend/scripts/phase113_blind_rounds.py` /
   `backend/scripts/phase113_blind_classify.py`.
4. Unit tests (full): `backend/tests/test_phase113_blind.py` —
   toy permutation sensitivity (§4.3(a) precondition),
   hand-computed feature values, S5-reproduction sanity for
   G(θ_S5), generator determinism, optimizer determinism and
   constraint logic on a toy classifier, round/verdict logic
   branches on synthetic posteriors, blinding invariant,
   ladder = audit admitted sets.
5. Results: `reports/phase113_blind_affiliation_results.json` +
   `reports/phase113_blind_affiliation_summary.md` (design
   recap, §4.4 power outcome, per-round gate numbers, per-round
   optimizer trace + control shares, final §8.4 shares, verdict
   in the §10 V6 vocabulary verbatim, defeating generator in
   full if any, panel table as assembled, limitations,
   licensing summary, unblinding record with code hash).
6. Ledger entries (both ledgers) with AI disclosure; foundation
   check run; full backend suite green; ruff check clean on new
   Python; ONE PR (NOT merged).
