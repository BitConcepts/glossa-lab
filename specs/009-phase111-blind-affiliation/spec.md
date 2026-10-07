# Spec 009 — Phase-111: Blind Language-Affiliation Study (pre-registration)

**Status:** FROZEN 2026-10-06 on `phase/111-blind-affiliation`
(from main cb2e43da), before any pipeline output exists. Owner-approved
execution ("do all this now", 2026-10-06) of the blind-study design in
`~/workspace/research_notes/indus-blind-language-affiliation-study-d-20261007-0101/report.md`
(deep-research report, 32 sources; cited below as "the design report"
with section numbers). This spec freezes the design into binding
protocol. The git order — this spec committed before any code output,
result, or panel statistic exists — is the pre-registration proof.

**Phase-numbering note:** ledger-sequence **Phase-111**. A legacy
script from an earlier era already carries this number
(`backend/scripts/phase111_allograph_resolution.py`, the allograph
resolution adjudicated in spec 008 / Phase-110). That file is
append-only history and is NOT renamed or reused. All new artifacts
carry distinct names (`phase111_blind_*`) and new graph node IDs, per
the spec-005/006/007/008 precedent.

**AI disclosure:** this study is designed for execution by an AI agent
(Muse Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI. The blinding protocol (§6) is written for exactly
this situation: the executing agent is also the analyst, so the
freeze, the custodian/analyst code separation, and the no-re-run
rules are the controls that substitute for a human firewall.

## Context

- Phase-107 (spec 005) falsified the program's simulated-annealing
  decipherment method under pre-registered held-out validation:
  held-out anchor agreement 0.000 under every lever, and blind controls
  (Sanskrit z = 60.874, scrambled lexicon z = 16.477) also scored zero
  held-out. An independent June-2026 blind re-test of a rival claim
  showed an identical annealing protocol "reading" the corpus at
  ~100% in Sanskrit, Gujarati, Tamil, Telugu AND a scrambled lexicon
  (design report §2, §3.1). Lesson, now doctrine: **an unconstrained
  fit proves nothing; only a blinded pipeline that first proves it can
  classify known corpora at the target's size may say anything about
  the target.**
- Phases 108–110 re-based the anchor set on provenance (strict
  SA-independent core: 94 HIGH+MEDIUM readings, 73.68% Holdat token
  coverage). Those are *reading* claims. This phase asks a different,
  prior question with a different instrument: **does the Indus sign
  system's joint statistical profile classify as linguistic, and —
  only if the instrument validates — does it discriminate among
  language families?**
- The design report's bottom line binds this spec's expectations:
  blind feature classification can credibly test (i) linguistic vs.
  structured non-linguistic and (ii) broad typology; it **cannot by
  itself credibly assign a genetic family**, because every single
  statistic has been reproduced by some non-linguistic system,
  because suffixing/agglutination is typological not genetic
  (Sumerian and Elamite are the key confounds), and because the
  corpus is ~11,000–19,616 tokens of mean length ~4.4–5. The gate
  (§7) exists so the study can discover its own invalidity and stop.

## Scope

**In scope (the verdict path):** the design report's ranked features
1–9 (§(a)) as one joint feature vector + one frozen classifier,
evaluated under the gate (§7), control-validity (§8), and verdict
rules (§9). Feature rank 1 (the joint vector) is the primary
endpoint; ranks 2–9 are its components and are never standalone
claims.

**Out of scope for verdicts (registered exclusions):**
- Feature rank 10 (dictionary-reading under blind SA assignment):
  excluded from Phase-111 verdicts. Rationale, frozen: SA was
  falsified as a validation instrument by Phase-107, and the design
  report (§(a) rank 10) records the test as currently demonstrated
  uninformative (all languages tie). It may be proposed as a later
  phase with its own spec.
- Segmented-unit features: the primary panel uses unsegmented
  features only (design report §5, segmentation failure mode).
- Any anchor/reading change: this phase touches no anchors, makes no
  decipherment claim, and its outputs cannot upgrade or downgrade any
  anchor tier.

## 1. Panel (frozen)

Family classes for the family task: `dravidian`, `indo_aryan`,
`semitic`, `indo_european_other`, `isolate_sumerian`, `turkic`,
`austronesian`, plus class `non_linguistic`. A corpus's class is its
label for every draw.

### 1a. Known linguistic corpora (gate + training)

| ID | Corpus | Family | Source | Unit rule | Text rule |
|---|---|---|---|---|---|
| K1 | Linear B (DAMOS) | indo_european_other | in-repo `backend/glossa_lab/data/phase17_corpora/damos_inscriptions.csv` | token = whitespace-separated sign/syllabogram as transcribed; drop tokens `.`, `vac.`, pure punctuation | stream-chunked (§2) |
| K2 | Vedic Sanskrit (Ṛgveda padapāṭha) | indo_aryan | in-repo `backend/glossa_lab/data/phase18_corpora/rv_padapatha_seqs.csv` | word → syllables (frozen splitter, §3) | stream-chunked |
| K3 | Classical Sanskrit (DCS) | indo_aryan | download, DCS (CC BY 4.0 per design report §4; verify at acquisition) | word form → syllables (same splitter) | stream-chunked |
| K4 | Old Tamil (kee2u morpheme sequences) | dravidian | in-repo `backend/glossa_lab/data/phase16_corpora/kee2u_tamil_morpheme_seqs.csv` | token = morpheme ID as given | stream-chunked |
| K5 | Sumerian, Ur III administrative | isolate_sumerian | download, CDLI (CC BY-NC 4.0; local use only, no redistribution) | token = cuneiform sign in transliteration sequence | stream-chunked |
| K6 | Akkadian (ORACC, admin/letters project) | semitic | download, ORACC (CC BY-SA 3.0 per project; record project at acquisition) | token = sign in transliteration (split on `-` and whitespace) | stream-chunked |
| K7 | Ge'ez (Genesis) | semitic | in-repo `backend/glossa_lab/data/geez/Geez_Genesis_syllabic_nopunctuation.txt` | token = syllable as given | stream-chunked |
| K8 | Turkish (modern, public-domain text) | turkic | download, Project Gutenberg (public domain) | word → syllables (vowel-nucleus splitter, §3) | stream-chunked |
| K9 | Malay/Indonesian (modern, public-domain text) | austronesian | download, Project Gutenberg (public domain) | word → syllables (vowel-nucleus splitter, §3) | stream-chunked |

### 1b. Known non-linguistic / boundary corpora (gate + training)

| ID | Corpus | Class | Source | Unit / text rule |
|---|---|---|---|---|
| N1 | Khipu cord sequences | non_linguistic | download, Open Khipu Repository (Zenodo DOI 10.5281/zenodo.5037551; verify license at acquisition) | token = pendant-cord knot-type token as encoded in the repository; stream-chunked |
| N2 | Proto-cuneiform | non_linguistic | download, CDLI (CC BY-NC 4.0; local use only) | token = sign in transliteration sequence; stream-chunked |

### 1c. Synthetic controls (custodian-generated, §5; anonymized in the panel)

S1 within-text permutation of the Indus R1 source; S2 i.i.d. Zipf
generator matched to R1 unigram distribution; S3 heraldic-style
positional-template generator; S4 administrative-style generator.
Algorithms frozen in §5.

### 1d. Target replicates (anonymized; the only classification targets)

| ID | Replicate | Sign list | Source |
|---|---|---|---|
| R1 | Holdat corpus (1,670 seals / 7,002 tokens / 390 signs; verified 2026-10-06) | Mahadevan M-numbers | in-repo downloads dir `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv` (CITATIONS A.13) |
| R2 | ICIT-extracted corpus (4,410 inscriptions / 14,213 tokens / 714 signs) | Wells numbers | `glossa-corpus/indus/sources/restricted-local/icit_extracted_corpus.json` — LOCAL computation only, never committed or published (PR #65 compliance removal) |
| R3 | Mixed pool: R1 texts + R2 texts pooled (token namespaces kept distinct by prefix before pooling) | both | as above |

Recorded caveats (frozen into the report template): R2's sign order
is probabilistically reconstructed by its source (OCR + initial/
terminal-rate ordering), not attested order; Holdat transcriptions
are not independently verified against CISI plates (CITATIONS A.13).

### 1e. Registered gaps (known at freeze time; not silent drops)

- **Elamite: GAP.** No verified openly-licensed machine-readable
  corpus exists (design report §4, "Could not verify"). Elamite is
  not in the panel. Consequence, frozen: the suffixing-isolate
  confound is carried by Sumerian (K5) alone; §9's confound rule
  references Sumerian accordingly.
- **SCA heraldry (attested): GAP.** Source license unverified
  (design report §4). The heraldic role in the panel is carried by
  the synthetic generator S3. Attested non-linguistic panel members
  are N1 and N2.
- **Sproat anchor set** (kudurru, Pictish, totem poles, barn stars,
  weather icons): not acquired (licenses unverified, design report
  §4); the anchor panel is not part of the verdict path.
- **Classical Sanskrit (K3):** conditional — if the DCS download
  cannot be obtained under its stated license at acquisition time,
  K3 becomes a gap, logged in the acquisition log before any run;
  Indo-Aryan is then carried by K2 alone. Same rule for K5/K6/N2
  downloads: failure to obtain under the stated license = gap,
  logged pre-run, never scraped around.
- **Power rule (design report §(b)):** any primary-panel corpus
  supplying < 5,000 clean tokens after processing moves to anchor
  status (excluded from gate and verdicts), the move logged in the
  acquisition log before unblinding.

## 2. Resampling (frozen)

- **Draw size:** primary N = 11,000 tokens per draw. Sensitivity
  sizes N = 5,000 and N = 19,600 (sensitivity results are reported
  and can never upgrade a verdict).
- **Draws:** 100 per panel member. Draw index split for the gate:
  draws 0–49 = train, draws 50–99 = test (frozen by index).
- **Target length distribution:** the empirical inscription-length
  distribution of the Holdat corpus (lengths 2–8; counts
  {2: 269, 3: 330, 4: 415, 5: 330, 6: 164, 7: 116, 8: 46}; mean
  4.193; verified from the source CSV 2026-10-06). Operationalization
  note: the design report's panel text cites mean ~4.6 from the
  published full-M77 counts (2,906 texts / 13,372 occurrences); the
  frozen target here is the target corpus's own empirical
  distribution as held locally, which is what the design's general
  rule ("resample to the Indus inscription-length distribution")
  requires. The 4.193 figure and this note are part of the freeze.
- **Stream-chunking** (for corpora marked stream-chunked in §1):
  at panel build, once per corpus: concatenate the corpus's token
  stream in source order (documents in file order), then chunk into
  pseudo-texts whose lengths are drawn i.i.d. from the target length
  distribution until the stream is exhausted (final partial chunk
  dropped). Chunking RNG: `SeedSequence([20261006, corpus_index])`.
  The chunked pseudo-texts are the corpus's text list thereafter.
- **Natural-text corpora** (targets R1–R3; synthetics as generated):
  texts as attested/generated.
- **Draw construction:** sample texts with replacement
  (`SeedSequence([20261006, corpus_index, draw_index])`) until
  cumulative tokens ≥ N; trim the final text's tail so the draw
  totals exactly N tokens (if the trim would empty the final text,
  discard it and continue sampling). Every draw therefore has
  exactly N tokens — a unit-tested invariant.
- **Custodian token remap:** before feature extraction, each corpus's
  token vocabulary is replaced by integers via a seeded permutation
  (`SeedSequence([20261008, corpus_index])`), vocabulary order
  shuffled. Features are distributional, so this changes nothing
  numerically; it exists so no artifact downstream of the custodian
  carries source token identities (recorded as a blind-integrity
  measure, design report §3.2).

## 3. Unit rules and the Sanskrit syllable splitter (frozen)

- Indus / Linear B / proto-cuneiform / Sumerian / Akkadian: the sign
  in the source transliteration/numbering is the token.
- Old Tamil: the kee2u morpheme ID is the token.
- Ge'ez: the syllable token as given in the in-repo syllabic file.
- Sanskrit (K2, K3): each word is syllabified by this deterministic
  rule over its IAST string: a syllable is (onset consonant cluster)
  + (one vowel nucleus) + (optional coda: anusvāra `ṃ`, visarga `ḥ`,
  or a single consonant when immediately followed by another
  consonant onset). Vowel set: a ā i ī u ū ṛ ṝ ḷ e ai o au. Any
  character sequence the splitter cannot parse is passed through as
  a single token (logged count in the acquisition log).
- Turkish / Malay-Indonesian: each whitespace-delimited word is
  syllabified by vowel-nucleus splitting over the language's Latin
  orthography (Turkish vowels a e ı i o ö u ü; Indonesian/Malay
  vowels a e i o u; adjacent vowels are separate nuclei unless a
  frozen diphthong list applies — Indonesian: ai au oi; Turkish:
  none). Punctuation is stripped before splitting.
- Representation-level note (design report §1 warning, §5): the
  primary level is "the minimal sequential unit as logged per
  corpus" — sign for logo-syllabic corpora, syllable/morpheme for
  language corpora. This heterogeneity is a recorded limitation
  (§12), not a post-hoc choice: it is frozen here, and the gate is
  the empirical check on whether classification survives it.

## 4. Feature vector (frozen; design report §(a) ranks 2–9)

Computed per draw. Notation: texts T₁…T_m; token counts n_i; total
N; vocabulary size K; unigram probabilities p; all entropies in bits,
plug-in estimator with Miller–Madow correction (frozen estimator;
design report §1.2 requires a frozen estimator and names NSB or
Miller–Madow — Miller–Madow is frozen here for determinism and
implementability in the repo's numpy-only environment). N-grams are
within-text only (never across text boundaries).

**Positional (report rank 2):**
- F01 `init80_frac` = (# distinct signs in the smallest set covering
  ≥ 80% of text-initial tokens) / K
- F02 `term80_frac` = same for text-final tokens, / K
- F03 `term_init_ratio` = (raw count for F02) / (raw count for F01)
- F04 `hend_first` = entropy of the text-initial token distribution / H₁
- F05 `hend_last` = entropy of the text-final token distribution / H₁
- F06 `term_productivity` = for the 10 most frequent text-final
  signs, mean # distinct immediate predecessors, / K
- F07 `init_productivity` = for the 10 most frequent text-initial
  signs, mean # distinct immediate successors, / K

**Entropy curve (report rank 3):**
- F08–F11 `blockH1..blockH4` = joint block entropies H₁, H₂, H₃, H₄
- F12 `cond_ent` = H₂ − H₁
- F13 `cond_ent_gap` = F12 − mean(H₂ − H₁ over 20 seeded within-text
  permutations of the same draw; permutation seed
  `SeedSequence([20261012, draw_index])`, permutations applied per
  text, preserving lengths and unigram counts)

**Local repetition (report rank 4):** for distance d, obs_d = share
of within-text token pairs at distance d that are identical;
exp = Σ pᵢ² ; adj_d = (obs_d − exp)/(1 − exp).
- F14 `rep_adj_1` (d = 1), F15 `rep_adj_2` (d = 2), F16 `rep_adj_3` (d = 3)

**Vocabulary growth (report rank 5):** rarefaction by text
subsampling without replacement at token fractions
{0.125, 0.25, 0.5, 0.75, 1.0} (5 seeded repetitions per fraction,
seed `SeedSequence([20261013, draw_index])`):
- F17 `hapax_prop` = (# signs with draw count 1) / K
- F18 `heaps_beta` = OLS slope of log(types) on log(tokens) over the
  five rarefaction points (repetition means)
- F19 `ttr` = K / N

**Markov predictability (report rank 6):** seeded 80/20 text split
(seed `SeedSequence([20261014, draw_index])`); bigram model with
add-α smoothing, α = 0.1 (frozen), trained on the 80%:
- F20 `pp_ratio` = held-out bigram perplexity / held-out unigram
  perplexity
- F21 `restore_acc` = on held-out texts, mask 10% of token positions
  (seeded), restore each by bigram argmax given the left neighbour
  (unigram argmax for text-initial positions); accuracy

**Zipf–Mandelbrot (report rank 7) and inventory (rank 8):**
- F22 `zipf_slope` = OLS slope of log frequency on log rank, ranks 1..K
- F23 `top10_share` = token share of the 10 most frequent signs
- F24 `cover80_frac` = (# signs covering ≥ 80% of tokens) / K
- F25 `vocab_K` = K (draw vocabulary size)

**Length (report rank 9):**
- F26 `len_mean`, F27 `len_sd`, F28 `singleton_share`
  (= share of texts of length 1)

Total: 28 features. No other features may enter the verdict path.
Features are standardized (z-scores) using TRAIN draws only (gate
model) or all known-corpus draws (final model, §6).

## 5. Synthetic generators (frozen algorithms)

All generators consume the R1 (Holdat) source statistics and the
target length distribution; each produces a text list used exactly
like a natural-text corpus thereafter. Generator RNG:
`SeedSequence([20261009, s])` for S_s.

- **S1 permutation null:** R1 texts with within-text token order
  permuted (one seeded permutation per text).
- **S2 i.i.d. Zipf null:** text lengths drawn from the target
  distribution; tokens i.i.d. from the R1 unigram distribution;
  generate until ≥ 5× the tokens one draw requires (the resampler
  draws from this text list as usual).
- **S3 heraldic generator:** position-class model over R1: three
  token distributions — initial (first tokens), final (last tokens),
  medial (all other tokens). Each generated text: length from the
  target distribution; first token ~ initial dist, last token ~
  final dist, medial tokens i.i.d. ~ medial dist. No sequential
  dependency beyond position class.
- **S4 administrative generator:** inventory = R1's 60 most frequent
  signs. Each text: length from the target distribution; tokens
  i.i.d. from the R1 unigram distribution restricted to the 60-sign
  inventory (renormalized); then, with probability 0.3 (per text,
  seeded), the first token is duplicated at the final position
  (template closure motif).

Control-validity (§8) applies to S1–S4. The linguistic BF verdict
(§9) names S3 and S4 as the synthetic comparators (design report
§(c).4/§(c).6: "both synthetic generators" = the heraldic and
administrative generators; S1/S2 are covered by control-validity).

## 6. Classifier and blinding (frozen)

- **Classifier:** linear discriminant analysis, shared covariance
  with shrinkage λ = 0.1 toward the diagonal (frozen), equal class
  priors, implemented in numpy (deterministic; the repo venv has no
  sklearn/scipy and none will be added). Posteriors from the LDA
  Gaussians. Bayes factor between classes a and b over a replicate =
  median over that replicate's draws of the posterior odds
  P(a)/P(b) (equal priors ⇒ posterior odds = likelihood ratio).
- **Gate model:** trained on known corpora draws 0–49, evaluated on
  draws 50–99.
- **Final model:** if and only if the gate passes, retrained on all
  100 draws of every known corpus (plus S3/S4 generator draws as
  their own classes `gen_heraldic`, `gen_administrative` for the
  §9 BF-vs-generator comparisons) and applied to the anonymized
  targets and synthetic controls.
- **Custodian / analyst separation (code-level, frozen):**
  `phase111_custodian.py` builds the panel, holds the ID → identity
  key, applies token remapping, generates synthetics, and writes
  (i) an anonymized panel file (IDs C01… only, feature matrices +
  draw metadata, no names) and (ii) the key file, which lives only
  in the gitignored runtime state dir during the run.
  `phase111_analyst.py` imports nothing from the custodian, reads
  only the anonymized panel file plus the KNOWN-corpus label map
  (gate training requires known answers — that is inherent to a
  validation gate and is disclosed here, per the design report's
  custodian model in which the custodian, not the analyst, holds
  only the *target* identities), and emits per-ID posteriors.
  The verdict step joins posteriors to the key (unblinding event,
  logged with timestamp and code hash in the results file).
  Synthetic controls and the three Indus replicates are the blinded
  items; the analyst artifacts (panel file, posterior file) contain
  no corpus names or source IDs — a unit-tested invariant.
- **No re-runs:** after unblinding, no parameter, feature, panel, or
  threshold may change for the verdict. Bugs found post-unblinding
  are handled by §11 (deviations), never by silent re-runs.

## 7. Validation gate (frozen stop rule; design report §(c).1)

Evaluated on held-out test draws (50–99) of the known corpora only,
with the gate model:

- **G1 (linguistic):** balanced accuracy of the binary task
  (linguistic = any family class; non_linguistic = class
  `non_linguistic`, corpora N1+N2) ≥ **0.85**, AND the lower bound
  of its 95% bootstrap CI (2,000 seeded resamples over test draws,
  seed `SeedSequence([20261011])`) > **0.70**.
- **G2 (family):** balanced accuracy over the 7 family classes
  (per-class recall on test draws of linguistic corpora, a draw
  counting correct only if its predicted argmax class is its own
  family) ≥ **0.70**, AND permutation p < **0.001** (1,000 seeded
  label permutations of the training labels, seed
  `SeedSequence([20261010])`; p = (1 + #{perm BA ≥ observed BA}) /
  1001), BH-adjusted per §10.

**If either fails: STOP.** The study reports INCONCLUSIVE
("method not validated at Indus size"), no Indus classification is
computed or reported, and the phase closes with the gate report as
its result. Tuning features, panel, or thresholds to pass the gate
is prohibited; §11 is the only remedy path.

## 8. Control validity (frozen; design report §(c).2)

Under the final model, each synthetic control S1–S4 must be
classified non-linguistic (binary collapse: posterior mass on
`non_linguistic` + `gen_heraldic` + `gen_administrative` classes ≥
posterior mass on all family classes) in ≥ **95%** of its draws.
Failure invalidates the run (verdict: INVALID RUN), not the
hypotheses, and is reported as such.

## 9. Indus verdict rules (frozen; design report §(c).3–6)

Applied only if the gate passes and control validity holds.
"Linguistic posterior" of a draw = summed posterior over the 7
family classes.

- **V1 replicate consistency:** R1, R2, R3 must agree on the binary
  verdict (linguistic vs not, by median linguistic posterior ≥ 0.5)
  and, if a family winner is named, on the winner. Any disagreement
  → verdict **UNSTABLE / INCONCLUSIVE**.
- **V2 linguistic verdict:** "linguistic" requires BF ≥ **10** for
  linguistic over EACH of: S3 (gen_heraldic), S4 (gen_administrative),
  and the best-matching attested non-linguistic corpus (the higher
  posterior of N1/N2 classes) — jointly, per the design report's
  Nair criterion (§(c).6), computed per replicate and required in
  all three replicates. If V2 fails in any replicate → the binary
  verdict is **NOT ESTABLISHED** (reported exactly so; this is not
  a finding of non-linguistic status).
- **V3 family support:** a family is SUPPORTED only if ALL hold:
  median posterior of the winning family ≥ **0.90** in each
  replicate; BF ≥ **10** vs the runner-up family; BF ≥ **10** vs
  S3 and vs S4 classes; the winner is the same in R1 and R2 (both
  sign lists); and in each of R1 and R2, ≥ **90%** of draws have
  argmax = the winning family.
- **V4 refutation / no discrimination:** if the top two families
  differ by BF < **3**, OR the bootstrap 95% CI of their median
  posterior difference lies within the equivalence band **±0.05**
  (TOST, α = 0.05), the verdict is **NO FAMILY DISCRIMINATION**
  — a positive equivalence result, reported as such.
- **V5 suffixing-confound rule:** if the winning family is
  `dravidian` but `isolate_sumerian` falls within the V4 equivalence
  band of it (BF < 3 or CI within ±0.05), the verdict is
  **NO FAMILY DISCRIMINATION (suffixing confound not excluded)** —
  a typological resemblance may be reported as exploratory text,
  never as family support. The same applies mutatis mutandis to any
  winner tied by a typologically similar confound class.
- **V6 verdict vocabulary (exhaustive):** the results summary must
  use exactly one of: `SUPPORTED: <family>` (only via V3 with V5
  not triggered), `NO FAMILY DISCRIMINATION`,
  `NO FAMILY DISCRIMINATION (suffixing confound not excluded)`,
  `NOT ESTABLISHED` (binary level), `UNSTABLE / INCONCLUSIVE`,
  `INCONCLUSIVE — GATE FAILED`, `INVALID RUN — CONTROL VALIDITY
  FAILED`. No narrative upgrading of any verdict is permitted in
  any program artifact.

## 10. Multiplicity (frozen; design report §(c).7)

The primary family of p-valued tests is fixed as: (T1) gate
linguistic bootstrap test, (T2) gate family permutation test,
(T3) Indus linguistic margin vs S3 (draw-exceedance p: share of S3
draws whose maximum family posterior ≥ the Indus median winning
posterior, pooled across replicates), (T4) same vs S4, (T5) Indus
family margin vs runner-up (draw-exceedance over runner-up family
draws). Benjamini–Hochberg at q = **0.05** across T1–T5 (tests not
reached because the gate failed are recorded as not-run and
excluded). Effect thresholds (§§7–9) stand as frozen regardless;
BH-adjusted significance is additionally required for any test
whose p-value is cited in support of a verdict. All other
analyses (sensitivities, per-feature contrasts, word-level) are
exploratory and cannot upgrade a verdict.

## 11. Deviations (frozen policy)

Any change to §§1–10 after this freeze — a design bug, a data
defect, a formula correction — requires: (i) a written deviation
note in this spec (dated addendum), (ii) a spec v2 commit BEFORE
any re-run, (iii) disclosure in the results summary and PR body,
(iv) re-running from the panel build (no partial re-use of pre-fix
artifacts). Deviations discovered after unblinding additionally
require the unblinded results to be reported alongside the
corrected ones, labelled superseded, never deleted.

## 12. Limitations (registered at freeze time)

- The study's ceiling is calibrated evidential support/refutation
  of *feature-based* affiliation claims; it can never refute "the
  Indus language was in family X" in full (design report §5
  asymmetry). Sproat's standard (a credible decipherment or
  independent archaeological evidence of literacy) remains the
  standard for proof; the Farmer–Sproat–Witzel falsifiers (a
  several-hundred-sign text; a ≥ 50-sign text with ordinary
  duplication; a ≥ 30-sign bilingual; an independently usable
  decipherment) would supersede this study's verdicts.
- Representation levels are heterogeneous across the panel (§3);
  genre is mismatched (seal inscriptions vs. administrative tablets
  vs. scripture vs. modern prose); chunking makes positional
  features of stream corpora measure stream-local structure rather
  than natural text boundaries (Indus texts are natural; comparators
  are chunked to Indus lengths). The gate is the mitigation, and a
  gate failure is the honest outcome if these confounds dominate.
- Indus draws at N = 11,000 are bootstrap draws from 7,002 (R1) /
  14,213 (R2) native tokens: draws are not independent samples of
  new inscriptions, and draw-to-draw SD understates true sampling
  uncertainty about the underlying population.
- R2's sign order is source-reconstructed, not attested (§1d).
- Elamite's absence (§1e) weakens the suffixing-confound exclusion
  to Sumerian alone.
- Holdat transcriptions carry the CITATIONS A.13 verification
  caveat; the M77 flat file (in-repo concordance extraction) is a
  registered sensitivity corpus, not a replicate.

## 13. Licensing (frozen; owner directive 2026-10-06)

Publish nothing that requires permission we do not hold.
- Downloads only under the licenses recorded in the acquisition log
  (`reports/phase111_acquisition_log.json`, Phase-107 format):
  DCS CC BY 4.0; ORACC CC BY-SA 3.0 (per project); CDLI CC BY-NC
  4.0 (local computation only, attribution, never redistributed);
  Open Khipu Repository (license verified at acquisition);
  Project Gutenberg (public domain).
- Raw downloaded texts live only under
  `glossa-corpus/indus/sources/phase111/` (gitignored). Committed
  artifacts are: code, this spec, the acquisition log, feature
  matrices, posteriors, and results — never source texts.
- NEVER ingest: ETCSL (no CC license), Project Madurai text (no
  redistribution), any Elamite edition (no verified open corpus).
  Restricted-local files (R2) are used locally and never committed.
- Feature vectors and statistics derived from any panel corpus are
  publishable; source texts are not.

## 14. Deliverables (frozen)

1. This spec (own commit, first).
2. `reports/phase111_acquisition_log.json` (Phase-107 format) —
  every panel corpus: source, license, token/text counts, unit and
  text rules as applied, gaps.
3. Pipeline: `backend/glossa_lab/phase111_custodian.py`,
  `backend/glossa_lab/phase111_features.py`,
  `backend/glossa_lab/phase111_analyst.py`,
  `backend/glossa_lab/phase111_run.py` (orchestrator: panel build →
  gate → [stop | classify → verdict]), with H23 graph registration
  (`backend/glossa_lab/experiment_graph_phase111.py`, nodes
  `IndusPhase111BlindGate` / `IndusPhase111BlindClassify`) before
  any run.
4. Unit tests: `backend/tests/test_phase111_blind.py` — feature
  extraction on toy corpora (hand-computed values), blinding
  invariant (analyst artifacts contain no corpus names/IDs),
  resampling exactness (exactly N tokens per draw; chunk-length
  distribution matches target), gate logic on synthetic feature
  matrices (pass and fail branches), generator determinism.
5. Results: `reports/phase111_blind_affiliation_results.json` +
  `reports/phase111_blind_affiliation_summary.md` (design recap,
  gate outcome, panel table as assembled with gaps, verdict in the
  §9 V6 vocabulary verbatim, limitations, licensing log summary,
  unblinding record with code hash).
6. Ledger entries (root `LEDGER.md` + `glossa-indus/LEDGER.md`)
  with AI disclosure; foundation check run; full backend suite
  green; ONE PR (spec + code + reports), NOT merged.

## Addendum A — 2026-10-06 (pre-run, pre-results; spec §11 procedure)

Recorded after the freeze commit and BEFORE the panel build, gate
run, or any result. No threshold, feature, or verdict rule changes.

1. **K8/K9 source substitution.** Project Gutenberg's index
   (Gutendex) returns no Turkish/Malay/Indonesian entries and the
   direct holdings could not be verified at acquisition time. The
   two modern decoy roles are filled instead by Universal
   Dependencies treebanks: UD_Turkish-IMST (CC BY-NC-SA 4.0) and
   UD_Indonesian-GSD (CC BY-SA 4.0), same unit rule (word → Latin
   vowel-nucleus syllables) and same stream-chunking. Local
   computation only; no text redistribution.
2. **Gaps confirmed under the §1e rule** (failure to obtain under a
   stated license = logged gap, never scraped around):
   - **K6 Akkadian — GAP.** ORACC hosts were unreachable from the
     execution network (repeated connection failures on both
     oracc.museum.upenn.edu and the München mirror); the openly
     available CDLI CoNLL dump carries no per-file language
     metadata that would isolate an Akkadian subset reliably; the
     MTAAC "gold" corpus proved to be Sumerian (ETCSRI). The
     `semitic` family is carried by K7 Ge'ez alone.
   - **N2 proto-cuneiform — GAP.** The only openly licensed
     sequence-adjacent source found (SFU pe-pc datasets,
     CC BY-SA 4.0) publishes n-gram count aggregates, not tablet
     sign sequences; CDLI bulk routes did not yield an openly
     licensed sequence file. The attested non-linguistic panel is
     N1 khipu alone; the boundary role is additionally carried by
     the synthetic generators S3/S4.
   - Elamite and attested SCA heraldry gaps stand as frozen in §1e.
3. **Sumerian source.** K5 is the CDLI Ur III corpus as republished
   in the MTAAC cdli_ur3 corpus repository (repository license
   CC0; underlying CDLI data CC BY-NC 4.0 — local computation only,
   attribution in the acquisition log). The catalogue index is
   filtered Language = Sumerian, Period = Ur III (72,877 entries).
   Loader caps, frozen here: files are read in CDLI-number order
   until 30,000 files or 2,000,000 sign tokens, whichever first.
4. **Khipu encoding (N1), operationalized.** Token stream = for each
   khipu (KHIPU_ID order), for each cord (CORD_ID order), the
   cord's knot TYPE_CODEs ordered by (CLUSTER_ORDINAL,
   KNOT_ORDINAL), from the Open Khipu Repository database
   (MIT license; Zenodo DOI 10.5281/zenodo.5037551, record version
   2.1.0). Stream-chunked per §2.
5. **Generator training instances (mechanical route for §6).** The
   final model's `gen_heraldic` / `gen_administrative` classes are
   trained on SEPARATE generator instances produced by the frozen
   §5 algorithms with seed stream [20261009, s, 777] and disclosed
   (non-blind) panel entries. The blind S3/S4 members use the
   frozen §5 seed streams and are the instances control validity
   (§8) is evaluated on. No threshold changes.
6. **BF operationalizations (clarifying §6/§9, no threshold
   change).** "BF for linguistic over comparator class c" = median
   over the replicate's draws of P(linguistic mass)/P(c). Family
   BFs and the TOST posterior-difference are computed on the pooled
   draws of the three replicates. Generator classes in the final
   model come from item 5.
7. **Classical Sanskrit (K3) obtained.** DCS CoNLL-U files
   (Bhāgavatapurāṇa, 15 files, 10,815 word forms); the CC BY 4.0
   license was verified in the official DCS repository's data
   readme at acquisition time.
