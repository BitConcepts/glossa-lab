# Phase-113 — Blind Language-Affiliation Study, Adversarial Protocol: Summary

Study: Phase-113 (spec 012, frozen 2026-10-07, freeze commit
848a9273). Successor to Phase-111 (spec 009) and Phase-112 (spec
010). Results file:
`reports/phase113_blind_affiliation_results.json`.

## Verdict

> **INVALID RUN — CONTROL VALIDITY FAILED** (fired at round 1,
> adversarial control A1)

This is a verdict about the method's validation at ladder step
L1, not about the Indus script. The frozen protocol (spec 012
§8.2) stops the study the moment an optimized adversarial
generator defeats a frozen round classifier; that happened in
the first round. **No affiliation verdict — for or against any
family, and not even for linguistic status — is produced by
Phase-113, and none may be quoted from it.** Rounds 2 and 3 were
not run, the final control-validity recheck (§8.4) was not
reached, and the blind key was never opened (see "Blinding
record" below).

What the run establishes, exactly: the round-1 classifier C_1 —
which is Phase-112's classifier (same 16 order-carrying
features, same LDA) — passes the inherited validation gate
perfectly on held-out known corpora, and is nevertheless
defeated, in 100% of draws, by a grammar-free generator that the
frozen optimizer found inside the pre-registered family G(θ)
while satisfying the round-1 matching constraint (unigram
TV ≤ 0.05 to R1). Phase-112's S5 was one point of that defeating
region; Phase-113 shows the region is broad (see "The defeating
generator").

## The design in brief

Phase-111 fell to unigram mimicry (S1/S2). Phase-112 admitted
only permutation-sensitive features and fell to S5, a positional
bigram template. Spec 012 replaces fixed traps with an
adversarial protocol: a feature ladder frozen in advance
(L1 = Phase-112's 16 features; L2 = L1 + admitted longer-range
family B; L3 = L2 + admitted cross-text family C), and three
rounds, one per ladder step. In each round the classifier is
frozen first; then a deterministic, seeded optimizer (budget
200 evaluations) searches the generator family G(θ) —
positional/global bigram and trigram mixtures with burst
(repeat-previous) and copy (whole-text duplication) components,
all built from R1's own statistics — for corpora that (a) match
R1 on all previous rounds' feature families (round 1: unigram
profile) and (b) maximize the frozen classifier's family
posterior mass. A round holds only if the frozen classifier
rejects the round's optimized corpus (A_r) in ≥ 95% of 100
fresh draws. Everything else — panel, resampling, LDA,
blinding, gate thresholds, verdict rules, BH q = 0.05 — is
inherited from specs 009/010 unchanged.

## Power analysis (spec §4.4): the question was askable

Design-stage audits on the nine known corpora only (full record:
`reports/phase113_feature_audit.json`):

- Permutation audit (spec-010 rule): family B admitted 8 of 14
  (`blockH5`, `blockH6`, `mi_lag2`, `mi_lag3`, `rep_adj_4`,
  `adj_clustering_lag2`, `restore_acc_tri`,
  `bigram_type_ratio_lag2`); family C admitted 6 of 6. Six
  family-B candidates were dropped on permutation grounds —
  five for inconsistent sign of the permutation response across
  corpora (`ent_incr_54`, `pp_ratio_ord3`, `rep_adj_5`,
  `ctx_pos_gain`, and `rep_adj_6`/`ent_incr_65` also on
  median |d|).
- Power audit at N = 7,002 (Holdat's exact size): all 20
  candidates passed (median pairwise between-class |Cohen's d|
  ≥ 0.5; smallest 0.738); the power criterion excluded nothing.
- Ladder power: family balanced accuracy at N = 7,002 was
  **1.000** at every ladder step (L1, L1+B, full L3).
- **INDETERMINATE AT THIS CORPUS SIZE did not fire** (admitted
  new features 14 ≥ 3; full-ladder family BA 1.000 ≥ 0.70). The
  adversarial rounds therefore proceeded.

## Gate (round 1, L1 features)

| Check | Value | Threshold | Pass |
|---|---|---|---|
| G1 binary BA | 1.000 | ≥ 0.85 | ✓ |
| G1 bootstrap 95% CI lower bound | 1.000 | > 0.70 | ✓ |
| G1 bootstrap p (T1) | 0.00050 | — | ✓ |
| G2 family BA | 1.000 | ≥ 0.70 | ✓ |
| G2 permutation p (T2) | 0.000999 | < 0.001 | ✓ |
| Per-family recall (all 7) | 1.000 each | — | ✓ |

The gate passed perfectly — as it did in Phases 111 and 112.
All three studies agree on the lesson: known-corpus validation
at these effect sizes is not where this method fails; control
validity is.

## Adversarial round 1: the defeat

Search (200 evaluations against the frozen C_1; full trace in
`.glossa-state/phase113/optimizer_trace_round1.jsonl`,
runtime state):

- 183 of 200 candidates satisfied the round-1 constraint
  (unigram TV ≤ 0.05). The objective (mean family posterior
  mass over 16 evaluation draws) is bimodal across the search
  space: median 0.0, but 82 candidates scored ≥ 0.99.
- Candidate 0 — the forced θ_S5 anchor, S5's exact construction
  — scored 0.99999995, feasible (TV 0.0383).

  *Sanity-anchor qualification (2026-10-07):* the spec §6
  anchor's positional-bigram TV < 0.10 is statistic-dependent.
  Under the finest-grained (frequency-weighted per-context)
  reading, the identical-model sampling-noise floor at ~55k
  tokens is 0.246 and G(θ_S5)-vs-S5 measured 0.243 — no
  systematic excess; the committed unit test therefore asserts
  TV < 0.30 and ≤ noise floor + 0.05, plus unigram TV to R1
  < 0.10 (measured 0.038). Under the coarser per-bin-pair
  successor-TV reading the value is 0.064, which meets 0.10.
  The anchor's substance is confirmed (S5's recorded unigram
  TV 0.0419 reproduced exactly; candidate 0 behaved exactly
  as S5 in this run); no outcome depends on the anchor's
  threshold. Full record: spec 012 §12.1 addendum (2026-10-07).
- Winner (eval 53, random block; first feasible candidate at
  exactly 1.0): the θ* below. Best objective was 1.0 in both the
  random and refinement blocks.

**Round artifact A_1** (100 fresh draws at θ*, seed stream never
used in search): 13,202 texts / 55,002 tokens generated;
unigram TV to R1 = 0.0387; **control share under C_1 = 0.00**
(0 of 100 draws classified non-linguistic under the binary
collapse). The ≥ 0.95 requirement failed maximally, the frozen
stop rule (§8.2) fired, and the study ended at round 1.

| Round | Ladder | Gate | Optimized generator | Control share | Outcome |
|---|---|---|---|---|---|
| 1 | L1 (16) | passed (above) | A_1, θ* below | **0.00** | INVALID — stop |
| 2 | L2 (24) | not run | — | — | not run (frozen stop rule) |
| 3 | L3 (30) | not run | — | — | not run (frozen stop rule) |

Final control validity (§8.4, S1–S5 + A1–A3 under C_3): **not
reached** — no C_3 exists. The fixed controls' validity in this
run is therefore not re-adjudicated here; their Phase-112
record stands as the prior measurement (S1–S4 rejected 1.00,
S5 share 0.00 under the same L1 feature family).

Multiplicity: T1 (gate bootstrap p = 0.00050) and T2 (gate
permutation p = 0.000999) ran as the round-1 primary instances;
T3–T5 were not reached and are recorded as not-run. No verdict
in this study rests on any p-value beyond the gate's frozen
thresholds, which were met.

## The defeating generator (spec §8.3 disclosure, in full)

A_r's generator is G(θ*) with the frozen component definitions
of spec 012 §6: per token position, a mode is drawn from the
weight vector w; P1 samples the relative-position-bin unigram
distribution of R1; P2 is S5's relative-position bigram
transition (smoothing β_P2 toward the next bin's unigram); P3
is the relative-position trigram with backoff β_P3 to P2; G2 is
the global bigram (backoff β_G2 to the global unigram); G3 is
the global trigram (backoff β_G3 to G2); BURST repeats the
previous token with probability p_burst; COPY duplicates a
previously generated text verbatim with probability p_copy.
Text lengths follow the frozen Holdat length distribution
exactly; generation ran to ≥ 55,000 tokens; the corpus was
remapped at corpus_index 41 and drawn at N = 11,000 exactly as
the panel members are.

θ* (winner, eval_index 53):

| Coordinate | Value | | Coordinate | Value |
|---|---|---|---|---|
| w_P1 | 0.0106 | | β_P2 | 3.0 |
| w_P2 | 0.0011 | | β_P3 | 0.3 |
| w_P3 | 0.2800 | | β_G2 | 1.0 |
| w_G2 | 0.1741 | | β_G3 | 0.3 |
| w_G3 | 0.5343 | | p_burst | 0.0477 |
|  |  | | p_copy | 0.1894 |

The winner is a **trigram-dominated grammar-free mixture**:
~53% global-trigram steps, ~28% positional-trigram steps, ~17%
global-bigram steps, with ~19% of texts copied verbatim and a
~4.8% repeat-previous rate. Constraint satisfaction (round 1):
unigram TV of the winner's evaluation corpus to R1 = 0.0394
(≤ 0.05 required); A_1's own TV = 0.0387; text lengths exact by
construction. Its 16 evaluation draws received mean family
posterior mass 1.0 under C_1, and all 100 artifact draws
classified into family space.

Reading (interpretation, labelled as such): the L1 feature
family — block entropies to k = 4, conditional entropies,
Markov perplexity ratios, exact-lag repetition at lags 1/3,
bigram type ratio, adjacency clustering — measures structure
that bounded-order Markov/template mixtures reproduce while
matching the unigram profile. Phase-112 showed one such process
(S5) suffices; Phase-113 shows the defeating set is a broad
region of process space, reachable by random search in a few
dozen evaluations, not a finely tuned point. What this run does
**not** measure — because the frozen protocol forbids
proceeding past a failed round — is whether the L2/L3 features
(longer-range dependence; cross-text composition) separate
attested language from this process class. That is a question
for a successor spec (for example, one whose first tested
ladder step is L2 or L3), never for a patch or re-ordering of
this run: §§8/12 of spec 012 forbid re-runs and mid-study
changes, and none were made.

## Panel as built

Identical panel to specs 009/010, re-staged into
`sources/phase113/` after the Phase-112 staging was lost, and
verified loader-equivalent against the committed Phase-111
build log on all eleven loader-backed corpora (all MATCH,
including S5 regenerated with unigram TV 0.0419 to R1,
identical to Phase-112's record). Full acquisition record:
`reports/phase113_acquisition_log.json`.

| ID | Texts | Tokens | Vocab | ID | Texts | Tokens | Vocab |
|---|---|---|---|---|---|---|---|
| K1 Linear B | 5,840 | 43,646 | 8,506 | N1 Khipu | 619 | 110,151 | 10 |
| K2 Vedic | 20,192 | 374,893 | 2,991 | S1 permuted R1 | 1,670 | 7,002 | — |
| K3 Classical | 15 docs | 22,298 | 1,696 | S2 iid Zipf | 13,177 | 55,004 | — |
| K4 Old Tamil | 600 | 17,414 | 1,924 | S3 heraldic gen | 13,094 | 55,003 | — |
| K5 Sumerian Ur III | 30,000 | 1,920,042 | 3,360 | S4 admin gen | 13,072 | 55,005 | — |
| K7 Ge'ez | 1 doc | 80,221 | 209 | S5 positional bigram | 13,057 | 55,002 | — |
| K8 Turkish | 3 docs | 125,818 | 2,314 | R1 Holdat (target) | 1,670 | 7,002 | 390 |
| K9 Indonesian | 3 docs | 251,339 | 4,891 | R2 ICIT (target) | 4,410 | 14,213 | 713 |
|  |  |  |  | R3 mixed (target) | 6,080 | 21,215 | 1,103 |

(K2/K3/K5/K7/K8/K9 "texts" are source documents/words as in the
Phase-111/112 build logs; the panel's chunked text counts are in
the results file's `panel_build_log`.)

## Blinding record

The custodian/analyst separation held throughout: the analyst
module imports nothing from the custodian (unit-tested). The
rounds stage resolved R1's blind ID custodian-side only (the
generator's design input, as S1–S5 were custodian-built in
every phase). **The key was never opened for classification:
`unblinding` in the results file is null**, because the classify
stage never ran — and cannot run: it was invoked once as an
integrity check after the stop and refused with the recorded
error ("classify stage cannot run: the rounds stage stopped
with verdict 'INVALID RUN — CONTROL VALIDITY FAILED'"). Code
HEAD for the run: 24cb33a0 (module digests in the results file).

## Deviations and operational disclosures

- **Deviations from the frozen spec: none.** No threshold,
  feature, panel member, budget, or rule was changed after the
  freeze; no re-run was performed.
- One VM reboot occurred during the design stage (2026-10-07,
  before the freeze's downstream runs): no committed or
  worktree artifact was lost (ephemeral /tmp scratch only); the
  panel build and the rounds ran uninterrupted after it. The
  panel build was checkpointed per member-size throughout, and
  the optimizer checkpointed every evaluation to its trace file.
- A duplicate index-free khipu verification load was stood down
  mid-verification for host contention; panel equivalence for
  N1 rests on the design-stage audit's index-free load, as
  recorded in the acquisition log (the local DB index was added
  only afterwards, mirroring Phase-112).
- Two staging corrections are recorded in the acquisition log
  (DCS directory's diacritic name; Zenodo's versioned archive
  filename). Neither changed any file content: every loader
  statistic reproduced exactly.
- BLAS thread pinning (OMP/OPENBLAS/MKL = 1) was set by the
  entry scripts' environment, as in Phase-112; environment only,
  no statistical content.
- Suite / foundation at close: backend suite **667 passed /
  12 skipped / 0 failed** (baseline 643/11; the 25 Phase-113
  tests all pass; the +1 skip vs baseline is Phase-112's
  state-dependent panel test, whose runtime state does not
  exist in this worktree — the same mechanism Phase-112
  recorded for Phase-111's test); foundation check **40 passed /
  0 failed / 8 warnings**. The foundation check reads the
  untracked `corpora/downloads` store, which a fresh worktree
  lacks; it was run with the main worktree's gitignored
  downloads symlinked in (no tracked file affected).

## Licensing

Unchanged discipline (owner directive 2026-10-06): publish
nothing requiring permission we lack. CDLI/MTAAC (CC BY-NC 4.0
underlying) and UD_Turkish-IMST (CC BY-NC-SA 4.0) are local
computation only; R2 is restricted-local and is never committed
or published; DCS is CC BY 4.0; UD_Indonesian-GSD CC BY-SA 4.0;
Open Khipu Repository MIT; in-repo corpora per their records.
Committed artifacts are code, the spec, logs, this summary, and
results — never source texts.

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution §VI.
