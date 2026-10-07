# Phase-112 — Blind Language-Affiliation Study, Order-Carrying Features: Results Summary

**Spec:** 010 (`specs/010-phase112-blind-affiliation/spec.md`),
frozen in commit 9410a23d after design-stage tooling commits
73ebbfb1 / f0e5a6c5 and before any Phase-112 pipeline output
existed (git order is the pre-registration proof). Pipeline
commit 7e2626cf. Owner authorization: Tristen Pierson,
2026-10-07. Machine-readable record:
`reports/phase112_blind_affiliation_results.json`.
Acquisition record: `reports/phase112_acquisition_log.json`.

**Verdict (spec §9 V6 vocabulary, verbatim):**
**`INVALID RUN — CONTROL VALIDITY FAILED`**

## Why this study existed

Phase-111 (spec 009) passed its validation gate perfectly, then
failed control validity: S1 (Indus texts with sign order
destroyed) and S2 (i.i.d. draws from the Indus unigram
distribution) classified as linguistic in 100% of draws — its
28-feature vector's power was carried by unigram statistics.
Phase-112 made exactly one design change: **the classification
feature set admits only permutation-sensitive (order-carrying)
features**, and added one harder trap (S5). Everything else —
panel, resampling, classifier, gate, control-validity rule,
verdict rules — was inherited from spec 009 unchanged.

## Feature admission audit (spec §4; known corpora only, pre-freeze)

23 candidates; admission required median |Cohen's d| ≥ 0.8 under
within-text permutation, same sign in ≥ 8/9 corpora,
non-degenerate in ≥ 5/9, after a mechanical toy test (all 23
passed the toy test). **16 admitted; 7 dropped.** Full record:
`reports/phase112_feature_audit.json`.

| Feature | median \|d\| | same sign | admitted |
|---|---:|---:|:--|
| `init80_frac` | 0.291 | 6/9 | no |
| `term80_frac` | 0.339 | 7/9 | no |
| `term_init_ratio` | 0.116 | 6/9 | no |
| `hend_first` | 0.421 | 9/9 | no |
| `hend_last` | 0.695 | 7/9 | no |
| `term_productivity` | 5.578 | 8/9 | **YES** |
| `init_productivity` | 6.257 | 9/9 | **YES** |
| `blockH2` | 34.157 | 8/9 | **YES** |
| `blockH3` | 25.119 | 9/9 | **YES** |
| `blockH4` | 12.387 | 9/9 | **YES** |
| `cond_ent` | 40.242 | 8/9 | **YES** |
| `cond_ent_gap` | 60.007 | 8/9 | **YES** |
| `cond_ent2` | 12.276 | 8/9 | **YES** |
| `ent_incr_43` | 7.780 | 8/9 | **YES** |
| `rep_adj_1` | 4.566 | 9/9 | **YES** |
| `rep_adj_2` | 1.910 | 7/9 | no |
| `rep_adj_3` | 2.348 | 9/9 | **YES** |
| `pp_ratio` | 17.493 | 9/9 | **YES** |
| `restore_acc` | 5.089 | 9/9 | **YES** |
| `pp_ratio_tri` | 7.641 | 8/9 | **YES** |
| `bigram_type_ratio` | 35.415 | 9/9 | **YES** |
| `adj_clustering` | 9.033 | 9/9 | **YES** |
| `fl_mi` | 1.280 | 7/9 | no |

## Panel (inherited as assembled; re-staged and verified)

The Phase-111 downloads were lost with their worktree after
Phase-111 closed. The identical panel was re-obtained from the
same openly licensed origins and **verified loader-equivalent**:
every corpus's loader statistics and chunk counts reproduce the
committed Phase-111 build log exactly (all 12 loadable corpora
MATCH — see the acquisition log). As built here: K1 Linear B
(5,840 docs / 43,646 tok), K2 Vedic (374,893 tok), K3 Classical
Sanskrit DCS first-15 (22,298), K4 Old Tamil (17,414), K5
Sumerian Ur III (30,000 files / 1,920,042), K7 Ge'ez (80,221),
K8 Turkish UD (125,818), K9 Indonesian UD (251,339), N1 khipu
(619 khipu / 110,151, vocab 10); R1 Holdat (1,670 texts / 7,002
tokens / 390 signs), R2 ICIT (4,410 / 14,213 / 713), R3 pooled
(6,080 / 21,215 / 1,103); S1–S4 as spec 009; **S5: 13,057 texts /
55,002 tokens, unigram total-variation distance to R1 = 0.0419**
(the positional-bigram template matches R1's unigram profile
closely by construction, as designed). Registered gaps stand
(Elamite, K6 Akkadian, N2 proto-cuneiform, attested SCA
heraldry).

## Gate (§7): PASSED

| Test | Requirement | Observed |
|---|---|---|
| G1 linguistic balanced accuracy | ≥ 0.85, CI low > 0.70 | **1.000**, CI low **1.000**, bootstrap p = 0.00050 |
| G2 family balanced accuracy | ≥ 0.70, perm p < 0.001 | **1.000**, p = 0.000999 (1,000 perms) |
| Per-family recall (all 7) | — | **1.000** each |

Order-carrying features alone separate the known corpora —
including the khipu-vs-linguistic boundary — perfectly at Indus
size on held-out draws. The frozen stop rule did not fire; the
classification stage ran.

## Control validity (§8): FAILED at S5

Share of draws classified non-linguistic (collapsed
non_linguistic + gen_heraldic + gen_administrative mass ≥ family
mass); requirement ≥ 0.95 for EACH control:

| Control | Share | Phase-111 share |
|---|---:|---:|
| S1 permutation of R1 | **1.00** ✓ | 0.00 |
| S2 i.i.d. Zipf | **1.00** ✓ | 0.00 |
| S3 heraldic generator | **1.00** ✓ | 1.00 |
| S4 administrative generator | **1.00** ✓ | 1.00 |
| S5 positional-bigram template | **0.00** ✗ | — (new) |

**The one design change did its work against the traps that
killed Phase-111:** with unigram evidence excluded, destroyed-
order nulls (S1) and unigram resamples (S2) are now rejected in
every draw. **The new, harder trap caught what S1/S2 could
not:** S5 — a non-linguistic process with no grammar, matching
R1's text lengths exactly, its unigram profile to TV = 0.042,
and its **relative-position bigram statistics by construction** —
was placed in family space in 100% of draws. The frozen §8 rule
is conjunctive across controls; one failure invalidates the
run. Per §9, no verdict rule fires and no affiliation claim is
admissible in either direction.

Mechanism, stated precisely: the admitted feature family
(block/conditional entropies to order 3, Markov perplexity
ratios to order 2, repetition structure, bigram type ratio,
adjacency clustering, boundary productivity) measures exactly
the statistics S5 reproduces by construction — local sequential
order up to relative-position bigrams. A positional template
process is therefore indistinguishable from genuine linguistic
order for this vector. Phase-111's failure mode was "unigram
statistics masquerade as linguistic evidence"; Phase-112's is
"positional-bigram statistics masquerade as linguistic order."
Both times, the pre-registered control-validity rule caught
the masquerade before any verdict issued — the protocol working
as designed, twice.

## Audit-only values (no verdict weight, §8 failure)

- Exceedance (draw-level, spec §10): T3 vs gen_heraldic
  p = 0.0099, T4 vs gen_administrative p = 0.0099; BH-adjusted
  T1–T4 all significant at q = 0.05. Recorded for the audit
  trail only.
- Sensitivity (descriptive): at N = 5,000 / 19,600 the Indus
  replicates' median linguistic posteriors are ~10⁻⁷ or smaller
  (winner family semitic at negligible mass) — i.e., under this
  model the Indus replicates sit overwhelmingly on the
  non-linguistic side of the boundary that S5 crosses. Because
  the run is invalid, this is **not** evidence about Indus in
  either direction; it is recorded solely as part of the frozen
  pipeline's complete output.

## Run record

- Pipeline executed unmodified from commit 7e2626cf
  (module SHA-256 digests in the results file; `git_head`
  recorded there matches). Unblinding event:
  2026-10-07T16:02:08.334428+00:00.
- Operational disclosure: two panel-build attempts were aborted
  before completion — the first stalled in a multiprocessing
  worker (futex wait) under extreme host contention (load
  average ≈ 10–48 on a 2-core VM) and was killed; the second
  was destroyed by a VM reboot mid-build. No results of any kind
  were produced by either attempt (the panel file is written
  only at build completion; no gate or Indus statistic existed).
  The completed run executed on the rebooted host with BLAS
  thread-count environment variables pinned to 1
  (OMP/OPENBLAS/MKL/NUMEXPR) as a stall mitigation —
  environment only; no code, feature, panel, seed, or threshold
  changed at any point. This mirrors the Phase-111 precedent of
  disclosing run-path events rather than absorbing them.
- H23: graph nodes `IndusPhase112BlindGate` /
  `IndusPhase112BlindClassify` registered and verified in
  `ATOMIC_NODES` before the run.
- Tests: Phase-112 unit tests 18 passed (incl. the panel
  blinding invariant, run post-build). Full-suite and
  foundation-check counts are recorded in the outcome ledger
  entries and the PR body.

## Limitations and the successor lesson

All spec §12 limitations stand (representation heterogeneity,
chunked positional features, khipu-alone attested
non-linguistic class, R2's reconstructed sign order — which
bites harder in an order study —, Elamite's absence). The
recorded lesson for any future spec, by new spec only, never by
patching this run: **discrimination claims for Indus order
structure must be validated against positional-template nulls,
not only against order destruction.** Two natural strengthenings
present themselves for a future design (recorded, not pursued):
an attested non-linguistic panel member harder than khipu, and
features probing structure beyond adjacent relative-position
pairs (longer-range dependencies, hierarchical constituency
proxies) — each of which would need its own pre-registered
audit and its own traps, because any new feature family creates
a new mimicry surface of exactly the kind S5 exposed here.

## Licensing

Panel sources and handling are exactly Phase-111's (spec §13):
DCS CC BY 4.0; CDLI via MTAAC repo CC0 / CDLI data CC BY-NC 4.0
(local only); UD-NC-SA / UD-SA (local only); khipu MIT; R2
restricted-local, local computation only, never committed.
Nothing new was downloaded beyond re-obtaining the identical
files from the same origins. Committed artifacts are code,
specs, logs, feature definitions, and results — never source
texts.

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution §VI.
