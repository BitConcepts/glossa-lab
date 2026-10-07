# Spec 010 — Phase-112: Blind Language-Affiliation Study, Order-Carrying Features (pre-registration)

**Status:** FROZEN 2026-10-07 on `phase/112-blind-affiliation-ordersensitive`
(from the Phase-111 branch HEAD 6a2384db, which includes the
completed Phase-111 pipeline and outcome; PR #66 merged to main the
same day — this branch is rebased onto main before its PR so the PR
shows only Phase-112 changes). Owner authorization: Tristen Pierson,
2026-10-07 ("yes do the successor now"). The git order — design-stage
tooling commit (73ebbfb1), then this spec committed before any
Phase-112 panel build, gate evaluation, or Indus statistic exists —
is the pre-registration proof.

**Phase-numbering note:** ledger-sequence **Phase-112**. A legacy
script already carries this number
(`backend/scripts/phase112_grammar_slot_inference.py`, from an
earlier era). That file is append-only history and is NOT renamed
or reused. All new artifacts carry distinct names (`phase112_blind_*`,
`phase112_features`, `phase112_custodian`, `phase112_analyst`,
`phase112_run`) and new graph node IDs, per the spec-009 precedent.

**AI disclosure:** this study is designed for execution by an AI
agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI. The blinding protocol (§6) is
written for exactly this situation: the executing agent is also
the analyst, so the freeze, the custodian/analyst code separation,
and the no-re-run rules are the controls that substitute for a
human firewall.

## Context — why this study exists

Phase-111 (spec 009) executed the frozen blind design faithfully.
Its validation gate **passed perfectly** (G1 linguistic balanced
accuracy 1.000, bootstrap p = 0.00050; G2 family balanced accuracy
1.000, permutation p = 0.000999; per-family recall 1.000 for all
seven families on held-out draws of known corpora at Indus size).
The run then failed the frozen control-validity rule (§8 of spec
009) at the classification stage: the synthetic controls **S1**
(real Indus texts with within-text token order permuted — unigram
counts, text lengths, hapax, inventory all preserved; every trace
of sequential and positional structure destroyed) and **S2**
(i.i.d. draws from the Indus unigram distribution) were classified
**linguistic in 100% of draws**. Verdict, verbatim:
`INVALID RUN — CONTROL VALIDITY FAILED`. No admissible evidence
about Indus affiliation was produced in either direction.

The diagnosis is mechanical, not interpretive: the 28-feature
vector's discriminative power was carried by **unigram statistics**
(frequency profile, hapax ratio, inventory, Zipf shape). A bag of
signs with the Indus frequency profile "looks linguistic" to such
a classifier even with all order destroyed — the same trap class
as the June-2026 blind annealing re-test (design report §3.1) and
the reason spec 009's §8 existed. Phase-111's own summary recorded
the successor lesson: the boundary the verdict path needs must be
validated against the nulls that actually threaten it.

**Phase-112 is that successor, with exactly one design change:**
the classification feature set contains **only order-carrying
(permutation-sensitive) features** (§4). Everything else — panel,
resampling, blinding, classifier, gate thresholds, control-validity
rule, verdict rules, multiplicity — is inherited from spec 009
unchanged, plus one additional, harder synthetic trap (S5, §5)
probing subtler order mimicry. Phase-112 asks: **does Indus
sign-order structure alone — with unigram evidence excluded by
construction — classify as linguistic, survive traps built from
Indus's own order-destroyed and order-mimicking statistics, and
(if the frozen bars are met) discriminate among families?**

## Scope

**In scope (the verdict path):** the admitted order-carrying
feature set of §4 as one joint vector + the frozen LDA classifier,
evaluated under the inherited gate (§7), control-validity (§8,
extended to S1–S5), and verdict rules (§9).

**Out of scope for verdicts (registered exclusions):**
- All permutation-invariant statistics (unigram frequency profile,
  Zipf–Mandelbrot parameters, hapax ratio, raw inventory size,
  text-length distribution): **excluded from classification**.
  They may appear in descriptive reporting only and can never
  carry a verdict. This exclusion is the study's raison d'être.
- Feature rank 10 of the design report (dictionary reading under
  blind SA assignment): excluded, as in spec 009 (SA falsified by
  Phase-107; the test as demonstrated is uninformative).
- Segmented-unit features; any anchor/reading change. This phase
  touches no anchors and makes no decipherment claim.

## 1. Panel (inherited from spec 009 as assembled)

Identical to spec 009 §1 **as assembled** (i.e., including Addendum
A of spec 009: UD substitutions for K8/K9; gaps K6 Akkadian,
N2 proto-cuneiform, Elamite, attested SCA heraldry). Family classes:
`dravidian`, `indo_aryan`, `semitic`, `indo_european_other`,
`isolate_sumerian`, `turkic`, `austronesian`, plus `non_linguistic`.

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
| S1–S4 | Synthetic controls (§5) | — | blind |
| S5 | Positional-bigram template generator (§5) | — | blind |
| R1 | Holdat corpus (1,670 seals / 7,002 tokens / 390 signs) | target | blind |
| R2 | ICIT-extracted corpus (4,410 / 14,213 / 714) | target | blind |
| R3 | Mixed pool R1+R2 (namespaces prefixed) | target | blind |

**Staging note (recorded, pre-run):** the Phase-111 worktree that
held the original downloads was removed by environment cleanup
after Phase-111 closed, before the staged copies could be fully
transferred. The panel sources were therefore re-obtained from
their original openly-licensed origins into
`glossa-corpus/indus/sources/phase112/` (gitignored): Holdat CSV
and the restricted-local ICIT file transferred with SHA-256
equality verified; DCS re-downloaded (the first-15-files selection
was identified by exact reproduction of the Phase-111 loader
statistics — documents 15, words 8,958, tokens 22,298, vocab
1,696, splitter passthrough 1,162); UD treebanks re-cloned; the
Open Khipu Repository 2.1.0 archive re-downloaded from Zenodo
(record 18025748, concept DOI 10.5281/zenodo.5037551, file size
79,808,932 bytes, exact); the MTAAC CDLI Ur III repository
re-cloned from cdli-gh. **Panel equivalence is verified, not
assumed:** every corpus's loader statistics and chunk counts were
recomputed from the Phase-112 staging and matched exactly against
the committed Phase-111 build log
(`reports/phase111_blind_affiliation_results.json`,
`panel_build_log`) before any Phase-112 run. Full record:
`reports/phase112_acquisition_log.json`.

**Registered gaps (unchanged):** Elamite (no verified openly
licensed machine-readable corpus; the suffixing-isolate confound
is carried by Sumerian alone); K6 Akkadian (ORACC unreachable in
Phase-111; the openly available MTAAC "gold" corpus proved
Sumerian; `semitic` is carried by Ge'ez alone); N2 proto-cuneiform
(no openly licensed sequence source; attested non-linguistic panel
= khipu alone, with the boundary role additionally carried by the
synthetic generators); attested SCA heraldry (license unverified;
S3 substitutes). Recorded caveats stand: R2's sign order is
source-reconstructed, not attested; Holdat transcriptions carry
the CITATIONS A.13 caveat. Power rule: every assembled corpus
supplies ≥ 5,000 clean tokens (as verified in Phase-111; the
identical panel is rebuilt here).

## 2. Resampling (inherited from spec 009 §2, unchanged)

Draw size N = 11,000 tokens primary; sensitivity 5,000 / 19,600
(reported, never verdict-bearing). 100 draws per member; draws
0–49 train / 50–99 test for the gate (frozen by index). Target
length distribution = Holdat empirical (lengths 2–8, counts
{2: 269, 3: 330, 4: 415, 5: 330, 6: 164, 7: 116, 8: 46}, mean
4.193). Stream-chunking, draw construction (sample texts with
replacement, trim final text's tail to exactly N — a unit-tested
invariant), and the custodian token remap use the frozen spec-009
code and seed streams, reused by import (§14). Chunking RNG
`SeedSequence([20261006, corpus_index])`; draw RNG
`SeedSequence([20261006, corpus_index, draw_index])`; remap RNG
`SeedSequence([20261008, corpus_index])`; blind-ID assignment RNG
`SeedSequence([20261007])` over the 17-member list (§5 adds S5 at
corpus_index 35).

## 3. Unit rules (inherited from spec 009 §3, unchanged)

Token = the sign in source transliteration/numbering (Indus, Linear
B, Sumerian); kee2u morpheme ID (Old Tamil); syllable (Ge'ez, by
character); the frozen Sanskrit IAST syllabifier (spec 009 §3) for
K2/K3; the frozen Latin vowel-nucleus syllabifiers for K8/K9.
Representation-level heterogeneity across the panel is a recorded
limitation (§12), frozen as in spec 009; the gate is the empirical
check on whether classification survives it — now with order-only
features, which makes the check strictly harder (§12).

## 4. Feature set — the one design change

### 4.1 Admission rule (frozen before the audit was run)

A candidate feature is admitted to the classification vector only
if it passes BOTH:

(a) **Mechanical toy test** (unit test, deterministic): on two
    structured toy corpora (a positional/Markov toy and a period-3
    repetition toy), the feature's value changes by > 0.002 under a
    seeded within-text permutation on at least one toy.
(b) **Known-corpus audit** (`backend/scripts/phase112_feature_audit.py`,
    run pre-freeze on the nine known panel corpora ONLY — never
    Indus, never the synthetics): per corpus, 20 draws at
    N = 11,000 (seed stream `[20261020, corpus_index, draw]`) and
    their within-text permuted counterparts (seed stream
    `[20261021, corpus_index, draw]`); Cohen's d of
    (original − permuted) per corpus. Admission requires:
    median |d| across the 9 corpora **≥ 0.8** (a large effect),
    the same sign of the mean difference in **≥ 8 of 9** corpora,
    and non-degeneracy (SD of original draws > 0 in ≥ 5 corpora).

A candidate failing either test is dropped BEFORE this freeze,
and the drop is recorded in §4.3. The audit's full numeric record
is `reports/phase112_feature_audit.json` (committed with this
spec). No feature may be added, removed, or redefined after this
freeze except through §11.

### 4.2 Candidates

Twenty-three candidates: the seventeen permutation-sensitive
definitions of spec 009 §4 recomputed identically (same estimators
— plug-in with Miller–Madow correction — same smoothing α = 0.1,
same internal seed streams [20261012]/[20261014]/[20261015]), plus
six new order-carrying candidates defined here:

- `cond_ent2` = H₃ − H₂ (second-order conditional entropy).
- `ent_incr_43` = H₄ − H₃ (block-entropy increment).
- `pp_ratio_tri` = held-out trigram perplexity / held-out bigram
  perplexity on the frozen 80/20 split; trigram model
  P(w|a,b) = (c(a,b,w) + α·P_bigram(w|b)) / (c(a,b) + α), with
  position 0 scored by the unigram model and position 1 by the
  bigram model, exactly as in spec 009's `pp_ratio` convention.
- `bigram_type_ratio` = (# distinct within-text bigrams) /
  (# bigram tokens).
- `adj_clustering` = mean local clustering coefficient of the
  undirected token-adjacency graph (edge iff a bigram is attested
  in either direction; nodes of degree < 2 excluded; 0 if none).
- `fl_mi` = MI(text-initial token; text-final token) / H₁, all
  entropies Miller–Madow corrected.

Inherited candidates: `init80_frac`, `term80_frac`,
`term_init_ratio`, `hend_first`, `hend_last`, `term_productivity`,
`init_productivity`, `blockH2`, `blockH3`, `blockH4`, `cond_ent`,
`cond_ent_gap`, `rep_adj_1`, `rep_adj_2`, `rep_adj_3`, `pp_ratio`,
`restore_acc` (spec 009 F01–F07, F09–F16, F20, F21 definitions).

Counting implementation note (design stage, recorded): block
entropies are computed with a Counter-based k-gram counter that
emits counts in sorted-key order, where the Phase-111 estimator
counted via sliding-window `np.unique`. The estimators (plug-in +
Miller–Madow) are unchanged; the two counting methods were
verified to agree to within 2×10⁻¹⁵ (machine precision) on a
known-corpus draw for k = 1–4 before this freeze (commit A2).

**Excluded by construction** (not computed for classification;
descriptive reporting only if at all): `blockH1` as a standalone
(it enters only as a component of differences/ratios),
`hapax_prop`, `heaps_beta`, `ttr`, `zipf_slope`, `top10_share`,
`cover80_frac`, `vocab_K`, `len_mean`, `len_sd`,
`singleton_share` — every permutation-invariant statistic of
spec 009 §4.

### 4.3 Audit outcome (recorded at freeze; numbers from
`reports/phase112_feature_audit.json`)

Audit executed pre-freeze (2026-10-07) exactly as §4.1(b)
prescribes; full per-corpus record in
`reports/phase112_feature_audit.json`. All 23 candidates passed
the §4.1(a) mechanical toy test. Known-corpus results (median
|Cohen's d| of original vs within-text permuted draws, 20 draws
per corpus at N = 11,000):

| Feature | median \|d\| | same sign | nondegenerate | admitted |
|---|---:|---:|---:|:--|
| `init80_frac` | 0.291 | 6/9 | 9/9 | no |
| `term80_frac` | 0.339 | 7/9 | 9/9 | no |
| `term_init_ratio` | 0.116 | 6/9 | 8/9 | no |
| `hend_first` | 0.421 | 9/9 | 9/9 | no |
| `hend_last` | 0.695 | 7/9 | 9/9 | no |
| `term_productivity` | 5.578 | 8/9 | 9/9 | **YES** |
| `init_productivity` | 6.257 | 9/9 | 9/9 | **YES** |
| `blockH2` | 34.157 | 8/9 | 9/9 | **YES** |
| `blockH3` | 25.119 | 9/9 | 9/9 | **YES** |
| `blockH4` | 12.387 | 9/9 | 9/9 | **YES** |
| `cond_ent` | 40.242 | 8/9 | 9/9 | **YES** |
| `cond_ent_gap` | 60.007 | 8/9 | 9/9 | **YES** |
| `cond_ent2` | 12.276 | 8/9 | 9/9 | **YES** |
| `ent_incr_43` | 7.780 | 8/9 | 9/9 | **YES** |
| `rep_adj_1` | 4.566 | 9/9 | 9/9 | **YES** |
| `rep_adj_2` | 1.910 | 7/9 | 9/9 | no |
| `rep_adj_3` | 2.348 | 9/9 | 9/9 | **YES** |
| `pp_ratio` | 17.493 | 9/9 | 9/9 | **YES** |
| `restore_acc` | 5.089 | 9/9 | 9/9 | **YES** |
| `pp_ratio_tri` | 7.641 | 8/9 | 9/9 | **YES** |
| `bigram_type_ratio` | 35.415 | 9/9 | 9/9 | **YES** |
| `adj_clustering` | 9.033 | 9/9 | 9/9 | **YES** |
| `fl_mi` | 1.280 | 7/9 | 9/9 | no |

**Dropped (7):** `init80_frac`, `term80_frac`, `term_init_ratio`,
`hend_first`, `hend_last` (positional-concentration family:
median |d| 0.12–0.70, below the 0.8 bar); `rep_adj_2` and `fl_mi`
(effect sizes above the bar — 1.910 and 1.280 — but same-sign in
only 7/9 corpora, failing the consistency clause). Recorded
observation, not a rule change: the positional family is weak
under this audit plausibly because eight of the nine known
corpora enter as chunked streams (§3), whose chunk-initial tokens
are arbitrary stream positions rather than true text onsets, so
permutation has little positional signal to destroy; the frozen
rule was applied as written regardless — redefining features or
thresholds after seeing audit outcomes is exactly what
pre-registration forbids.

**Admitted feature set (frozen, in vector order):**
`term_productivity`, `init_productivity`, `blockH2`, `blockH3`,
`blockH4`, `cond_ent`, `cond_ent_gap`, `cond_ent2`, `ent_incr_43`,
`rep_adj_1`, `rep_adj_3`, `pp_ratio`, `restore_acc`,
`pp_ratio_tri`, `bigram_type_ratio`, `adj_clustering`
(16 features).

Features are standardized (z-scores) using TRAIN draws only (gate
model) or all known-corpus draws (final model, §6), as in spec 009.

## 5. Synthetic generators (S1–S4 inherited; S5 new)

S1–S4 are the frozen spec-009 §5 algorithms, reused by import:
S1 within-text permutation of R1; S2 i.i.d. unigram (Zipf) null;
S3 heraldic position-class generator; S4 administrative
top-60 + template-closure generator. Generator seed streams
`SeedSequence([20261009, s])`; disclosed TRAINING instances for
S3/S4 use seed stream `[20261009, s, 777]` (spec 009 Addendum A
route, inherited).

**S5 — positional-bigram template generator (new, frozen here).**
Relative-position bins b(j, L) = ⌊5j / L⌋ for slot j (0-based) in a
text of length L. From R1: positional unigram counts U_b(x) per
bin, and adjacent-pair counts C_{b,b′}(x→y) per bin pair.
Generation of a text of length L (drawn from the target length
distribution, until ≥ 5 × N_PRIMARY tokens in total):

- x₀ ~ U_{b(0,L)} (empirical distribution);
- for j ≥ 1, with b = b(j−1, L), b′ = b(j, L):
  P(y | x_{j−1}) = ( C_{b,b′}(x_{j−1}→y) + β·U_{b′}(y) ) /
                   ( C_{b,b′}(x_{j−1}→·) + β ),  β = 1.0 frozen.

Seed stream `SeedSequence([20261009, 5])`. S5 thus matches R1's
text lengths exactly, its unigram profile approximately through
the positional marginals (the build log records the total-variation
distance between the S5 and R1 unigram distributions), and its
**relative-position bigram statistics by construction** — while
being, by construction, a non-linguistic positional template
process with no sequential grammar beyond adjacent
relative-position pairs. It is the subtler trap Phase-111 lacked:
S3 carries positional marginals without bigrams; S5 carries
positional bigrams without grammar.

## 6. Classifier and blinding (inherited from spec 009 §6)

LDA, shared covariance with shrinkage λ = 0.1 toward the diagonal,
equal priors, numpy implementation (deterministic); posteriors
from the LDA Gaussians; Bayes factor between classes over a
replicate = median over its draws of the posterior odds. Gate
model trained on known draws 0–49, evaluated on 50–99. Final model
(if and only if the gate passes) retrained on all 100 draws of
every known corpus plus the disclosed S3/S4 generator-training
instances as classes `gen_heraldic` / `gen_administrative`, and
applied to the anonymized targets and synthetic controls.

**S5 has NO disclosed training instance and NO class in the final
model** (frozen). Rationale, recorded: in Phase-111, S3/S4 were
caught partly by their own disclosed generator classes, which the
Phase-111 summary itself flagged as a weakness of the control
design. S5 must be rejected by the boundary the model learns from
attested corpora and the S3/S4 classes alone; giving it a class
would make its §8 test nearly automatic and the probe toothless.

Custodian/analyst separation (code level, frozen):
`phase112_custodian.py` builds the panel (reusing the frozen
spec-009 loaders/chunking/resampling by import from
`phase111_custodian`, with its SOURCES redirected to the Phase-112
staged copies), holds the ID → identity key, applies token
remapping, generates S1–S5, and writes (i) the anonymized panel
file (IDs C01… only, feature matrices + draw metadata, no names)
and (ii) the key file, which lives only in the gitignored runtime
state dir (`.glossa-state/phase112/`) during the run.
`phase112_analyst.py` imports nothing from any custodian, reads
only the anonymized panel file plus the known-corpus label map,
and emits per-ID posteriors. The verdict step joins posteriors to
the key (unblinding event, logged with timestamp and code hash in
the results file). Synthetic controls and the three Indus
replicates are the blinded items; analyst artifacts contain no
corpus names or source IDs — a unit-tested invariant.

**No re-runs:** after unblinding, no parameter, feature, panel,
or threshold may change for the verdict. Bugs found post-unblinding
are handled by §11, never by silent re-runs.

## 7. Validation gate (inherited from spec 009 §7, unchanged)

Evaluated on held-out test draws (50–99) of the known corpora only,
with the gate model:

- **G1 (linguistic):** balanced accuracy of the binary task
  (linguistic = any family class; non_linguistic = N1) ≥ **0.85**,
  AND the lower bound of its 95% bootstrap CI (2,000 seeded
  resamples, seed `SeedSequence([20261011])`) > **0.70**.
- **G2 (family):** balanced accuracy over the 7 family classes
  ≥ **0.70**, AND permutation p < **0.001** (1,000 seeded label
  permutations, seed `SeedSequence([20261010])`; p = (1 +
  #{perm BA ≥ observed BA}) / 1001), BH-adjusted per §10.

**If either fails: STOP.** The study reports INCONCLUSIVE
("method not validated at Indus size"), no Indus classification
is computed or reported, and the phase closes with the gate
report as its result. Tuning features, panel, or thresholds to
pass the gate is prohibited; §11 is the only remedy path.

Recorded expectations (frozen, not tuning licenses): (i) the
gate's attested non-linguistic class rests on khipu alone, an
extreme outlier in Phase-111 (vocabulary 10) — with order-only
features the G1 task is genuinely harder, because khipu's cord
sequences do carry sequential structure; (ii) family
discrimination (G2) from order features alone at N = 11,000 may
well fall below 0.70. A gate failure is therefore a live,
honourable outcome of this design — it is the price of removing
the confounded features, and it is accepted in advance.

## 8. Control validity (inherited from spec 009 §8, extended to S5)

Under the final model, **each synthetic control S1–S5** must be
classified non-linguistic (binary collapse: posterior mass on
`non_linguistic` + `gen_heraldic` + `gen_administrative` classes
≥ posterior mass on all family classes) in ≥ **95%** of its draws.
The collapse set is exactly Phase-111's; S5 receives no class of
its own (§6). Failure invalidates the run (verdict: INVALID RUN),
not the hypotheses, and is reported as such. This section is
where the Phase-112 claim lives or dies: S1 and S2 are the traps
that defeated Phase-111; S5 is the harder order-mimicry trap.

## 9. Indus verdict rules (inherited from spec 009 §9, unchanged)

Applied only if the gate passes and control validity holds.
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
  replicates. (S5 enters the verdict path through §8, as S1/S2
  did in spec 009; the V2 comparators are unchanged.) Failure in
  any replicate → **NOT ESTABLISHED** (not a finding of
  non-linguistic status).
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
  `INVALID RUN — CONTROL VALIDITY FAILED`. No narrative upgrading
  of any verdict is permitted in any program artifact.

## 10. Multiplicity (inherited from spec 009 §10, unchanged)

Primary p-valued tests: (T1) gate linguistic bootstrap test,
(T2) gate family permutation test, (T3) Indus linguistic margin
vs S3 (draw-exceedance), (T4) same vs S4, (T5) Indus family
margin vs runner-up (draw-exceedance over runner-up family
draws). Benjamini–Hochberg at q = **0.05** across T1–T5 (tests
not reached are recorded as not-run and excluded). Effect
thresholds (§§7–9) stand as frozen regardless; BH-adjusted
significance is additionally required for any test whose p-value
is cited in support of a verdict. All other analyses are
exploratory and cannot upgrade a verdict.

## 11. Deviations (inherited policy)

Any change to §§1–10 after this freeze requires: (i) a written
deviation note in this spec (dated addendum), (ii) a spec v2
commit BEFORE any re-run, (iii) disclosure in the results
summary and PR body, (iv) re-running from the panel build (no
partial re-use of pre-fix artifacts). Deviations discovered after
unblinding additionally require the unblinded results to be
reported alongside the corrected ones, labelled superseded, never
deleted. (Phase-111 precedent: its own outcome commit corrected
a mis-reported suite count transparently in the PR body; the
 Phase-112 design-stage correction of the S5 toy-test expectation
 — final-token share 0.64 measured vs 0.8 initially asserted,
 because relative-position bins smear finality across lengths by
 design — occurred BEFORE this freeze, changed no generator and
 no threshold, and is recorded here for completeness.)

## 12. Limitations (registered at freeze time)

- All spec-009 §12 limitations stand (representation-level
  heterogeneity, genre mismatch, chunked positional features,
  bootstrap-draw dependence, R2's reconstructed sign order,
  Elamite's absence, Holdat's A.13 caveat). The study's ceiling
  is calibrated evidential support/refutation of feature-based
  affiliation claims; it can never refute "the Indus language
  was in family X" in full.
- **Order-only by design:** genuine unigram evidence (e.g., the
  sign-inventory size itself) is deliberately discarded. A
  Phase-112 null or gate failure does NOT imply the Phase-111
  feature set was "wrong" — it implies order structure alone
  does not carry the classification, which is a different and
  narrower statement. Conversely, passing §8 with order-only
  features is strictly stronger evidence about *structure* than
  Phase-111 could have produced, because the traps that defeated
  it are order-defined.
- **What passing §8 would and would not mean:** it would mean
  Indus order structure is not reproduced by (i) order
  destruction, (ii) unigram resampling, (iii) positional
  marginals, (iv) administrative templates, or (v) positional
  bigram templates. It would NOT mean no non-linguistic process
  could produce Indus-like order — only that these five frozen
  ones do not.
- **Gate weakness (Phase-111 lesson, inherited knowingly):** the
  attested non-linguistic class is khipu alone. The one-design-
  change mandate freezes the gate as-is; §8 over five controls is
  this study's real adjudicator, and the summary must say so.
- R2's order is source-reconstructed: for an order-feature study
  this caveat bites harder than in Phase-111. V1's
  replicate-consistency rule (R1 attested order vs R2
  reconstructed order must agree) is the mitigation, and any
  R1/R2 disagreement is reported as UNSTABLE, never averaged away.

## 13. Licensing (inherited from spec 009 §13; owner directive 2026-10-06)

Publish nothing that requires permission we do not hold. The
panel's sources and licenses are exactly Phase-111's (DCS CC
BY 4.0; CDLI via MTAAC repo CC0 / underlying CDLI CC BY-NC 4.0,
local computation only; UD_Turkish-IMST CC BY-NC-SA 4.0 and
UD_Indonesian-GSD CC BY-SA 4.0, local only; Open Khipu Repository
MIT; in-repo corpora per their acquisition records; R2
restricted-local, local computation only, never committed).
Phase-112 downloads nothing new: it re-obtained the identical
files from the same origins after the Phase-111 staging was lost
(§1 staging note), and the re-obtention is recorded in
`reports/phase112_acquisition_log.json`. Raw texts live only in
the gitignored store; committed artifacts are code, this spec,
the audit + acquisition logs, feature matrices, posteriors, and
results — never source texts. NEVER ingest: ETCSL, Project
Madurai, any Elamite edition.

## 14. Deliverables (frozen)

1. Design-stage tooling commit (features module with all 23
   candidates, audit script, toy tests) — commit 73ebbfb1.
2. This spec (own commit, with ledger freeze entries), including
   the §4.3 audit table; `reports/phase112_feature_audit.json`.
3. `reports/phase112_acquisition_log.json` (Phase-107 format) —
   panel inheritance, staging/re-obtention record with the
   loader-equivalence verification, gaps.
4. Pipeline: `backend/glossa_lab/phase112_custodian.py`,
   `backend/glossa_lab/phase112_features.py` (restricted to the
   §4.3 admitted set, definitions unchanged),
   `backend/glossa_lab/phase112_analyst.py`,
   `backend/glossa_lab/phase112_run.py`, with H23 graph
   registration (`backend/glossa_lab/experiment_graph_phase112.py`,
   nodes `IndusPhase112BlindGate` / `IndusPhase112BlindClassify`,
   verified in `ATOMIC_NODES`) before any run; entry scripts
   `backend/scripts/phase112_blind_gate.py` /
   `phase112_blind_classify.py`.
5. Unit tests: `backend/tests/test_phase112_blind.py` —
   permutation-sensitivity (toy, §4.1a), hand-computed feature
   values, blinding invariant, FEATURE_NAMES == audit admitted
   set, resampling exactness (via the reused frozen code), gate
   logic (pass/fail branches), S5 determinism/shape/positional
   fidelity.
6. Results: `reports/phase112_blind_affiliation_results.json` +
   `reports/phase112_blind_affiliation_summary.md` (design recap,
   gate outcome, control-validity shares for S1–S5, verdict in
   the §9 V6 vocabulary verbatim, the §4.3 feature audit table,
   panel table as assembled, limitations, licensing summary,
   unblinding record with code hash).
7. Ledger entries (root `LEDGER.md` + `glossa-indus/LEDGER.md`)
   with AI disclosure; foundation check run; full backend suite
   green; ruff check clean on new Python; ONE PR (NOT merged).
