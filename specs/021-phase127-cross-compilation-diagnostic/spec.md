# Spec 021 — Phase-127: Cross-Compilation Disagreement Diagnostic — How Much of Phase-125's Disagreement Is Genuine vs Sampling Noise / Crosswalk Ambiguity / Composition (pre-registration)

**Status:** DESIGN FROZEN 2026-10-08 on
`phase/127-cross-compilation-diagnostic` (from main
`3bae1c2e`). Owner authorization: Tristen Pierson,
2026-10-08 — WORKSTREAM 1 of the owner-ordered
Glossa-Lab program (Phase-127 diagnostic). This spec is
committed before any Phase-127 diagnostic statistic
exists. The only numbers in this spec are (i) the
Phase-125 results of record, quoted verbatim from
`reports/phase125_cross_compilation_results.json`,
(ii) the Phase-122 crosswalk / mayig-layer counts of
record, and (iii) metadata-support facts for §7
(inscription counts per metadata stratum, computed from
metadata columns only — no profile, distance, or
diagnostic statistic is computed at design stage).

**Phase-numbering note:** ledger-sequence **Phase-127**
(Phase-125 spec 019, Phase-126 ledger-sequence Wells-split
precede it). Artifact names carry the phase number
(`phase127_cross_compilation_diagnostic`, graph node
`IndusPhase127CrossCompilationDiagnostic`).

**AI disclosure:** this study is designed and executed
by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.

## Context — why this phase exists, and what it is not

Phase-125 (spec 019) returned a FINAL verdict:
**FAIL — DISAGREEMENT**. On the PRIMARY arm (high-
confidence, unambiguous crosswalk pairs, floor 8):
16 judgeable pairs of 286; median TV **0.636931**;
Spearman ρ initial **−0.424758** / terminal
**0.316034**; pairing-shuffle null (B = 999, seed
125125) **p = 0.824**. Crosswalk v1 (Phase-122): 762
pairs (372 high-confidence); the mayig layer: 179
inscriptions / 1,003 tokens / 182 distinct P signs.

Phase-125's own claim scope (spec 019 §7) states that a
FAIL "does not identify which side (transcription,
segmentation, crosswalk, population) produces the
disagreement; mechanism attribution would require a
successor diagnostic spec in the Phase-116 pattern."
**This spec is that successor diagnostic.** It asks a
strictly decompositional question about the Phase-125
result: how much of the observed disagreement is
consistent with (i) sampling noise at the observed
token counts, (ii) crosswalk ambiguity, and
(iii) population composition — and how much is not
explained by any of those.

**Non-goals, registered in advance and binding on every
artifact of this phase:**

- This phase does **NOT** re-score Phase-125. No
  Phase-125 statistic is recomputed as a verdict input,
  no verdict rule is applied to any Phase-127 number,
  and no PASS / FAIL / NULL pattern is issued here.
- The Phase-125 verdict is **FINAL and unchanged**:
  FAIL — DISAGREEMENT. No finding of this diagnostic
  softens, qualifies, conditions, or re-opens it. The
  Phase-127 report's abstract states the Phase-125
  verdict unchanged in its first lines, and every
  interpretive sentence in Phase-127 artifacts is a
  statement about the *composition of the observed
  distances*, never about the verdict.
- This phase modifies no anchor, issues no PRED
  verdict, changes no status, and touches no Phase-125
  artifact. The anchors file is never opened for
  writing; its sha256 (Appendix A) is asserted
  unchanged at the end of the run.

## Epistemic boundaries

Assumptions, declared:

- **A1 — Fixed judgeable set.** Every diagnostic arm
  operates on exactly the **16 PRIMARY judgeable pairs
  of Phase-125** (spec 019 §4.2 floor 8, PRIMARY arm),
  taken from the Phase-125 results of record. No pair
  is added or removed by any Phase-127 procedure,
  except where a §7 composition control re-applies the
  same frozen floor 8 to restricted-compilation counts
  — and there the restricted judgeable set is reported
  alongside, never substituted for, the fixed set.
- **A2 — Same machinery.** Profiles, positional
  counts, and TV are computed with the Phase-125 /
  Phase-113 machinery exactly (`phase113_battery`
  positional convention: position 0 of a multi-sign
  inscription INITIAL, last TERMINAL, everything else
  — including a sole token — MEDIAL;
  `phase125_cross_compilation` profile/TV functions
  reused, not reimplemented). Inscriptions are never
  pooled across compilations, in this phase as in
  Phase-125.
- **A3 — Resampling units are stated per arm.** Token-
  level procedures (§§3–4, §8) treat a sign's tokens in
  one compilation as a pool of positional-class labels;
  tokens within one inscription are not independent
  (a token's class depends on its inscription's
  length), so token-level nulls *understate* clustered
  noise — that direction is stated wherever a token-
  level number is reported. The inscription-level
  bootstrap (§5) is the cluster-respecting procedure
  and is feasible for both compilations (both layers
  supply inscription token lists); it is the primary
  uncertainty statement.
- **A4 — Descriptive attribution only.** §6's
  attribution estimator is a pre-registered descriptive
  decomposition, not a causal estimate. It is reported
  with its definition attached wherever its numbers
  appear.
- **A5 — Determinism.** Every stochastic procedure uses
  a fixed seed and a pre-registered replicate count
  (§2). Two runs of the phase script must produce
  identical diagnostic statistics (timestamps aside).
- **A6 — One diagnostic, as found.** No threshold in
  this spec is a verdict gate. Numbers are reported as
  found, including numbers that make the observed
  disagreement look *more* genuine, and numbers that
  attribute *more* of it to noise. Neither direction
  changes any prior verdict (§0 non-goals).

## 1. The question (registered)

> For the 16 Phase-125 PRIMARY judgeable pairs, with
> observed per-pair TVs and median TV 0.636931:
> (a) what TV does pure within-compilation sampling
> produce at full Holdat size (split-half noise floor);
> (b) what TV does pure Holdat-internal sampling
> produce at the mayig token counts actually observed
> (matched-size null); (c) how wide are the bootstrap
> confidence intervals on each pair's TV and on the
> median TV; (d) how much of each pair's TV is
> attributable, under the §6 estimator, to crosswalk
> mappings outside the unambiguous primary pair;
> (e) how much does the disagreement move when
> composition is controlled on the metadata strata
> that exist on both sides; and (f) how many tokens
> per sign would the frozen Phase-125 gates need for
> sampling noise alone to sit below the PASS bound?

## 2. Frozen inputs, seeds, and replicate counts

Inputs are exactly the Phase-125 frozen inputs (spec
019 §2), loaded through the same loaders:

| Input | Path / loader | Frozen fact |
|---|---|---|
| mayig CISI layer v1 | `data/corpus_layers/mayig_cisi_layer_v1.json` via `backend/glossa_lab/data/mayig_layer.py` | 179 inscriptions / 1,003 tokens / 182 P signs; sha256 `6a7664c605079373ca80e70b7e9559c1527613e3f67b579a817ced785e129860` |
| Holdat corpus | gitignored CSV in the main checkout, via `phase113_run.load_holdat_inscriptions` (spec 019 replication) | 1,670 inscriptions / 7,002 tokens / 390 M signs; sha256 `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`; never committed or redistributed |
| Crosswalk v1 | `data/crosswalks/parpola_mahadevan_crosswalk_v1.json` via its Phase-122 loader | 762 pairs; high 372 / medium 0 / low 390; sha256 `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb` |
| Phase-125 results | `reports/phase125_cross_compilation_results.json` | the 16 PRIMARY judgeable pairs, their profiles, counts, TVs; observed median TV 0.636931 |
| Anchors (read-only assertion) | `backend/reports/INDUS_FINAL_ANCHORS.json` | sha256 `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`, asserted unchanged |

Stochastic streams (one `random.Random(seed)` per arm,
consumed replicate-by-replicate in the arm's registered
sign order — sorted by (P, M) as in Phase-125):

| Arm | Seed | Replicates |
|---|---|---|
| §3 split-half (a) | 127001 | B = 999 per sign |
| §4 matched-size (b) | 127002 | B = 999 per sign |
| §5 bootstrap (c) | 127003 | B = 999 |
| §8 power grid (f) | 127004 | B = 499 per grid point per sign |

§§6–7 are deterministic (no RNG). All intervals are
percentile intervals: type-7 (linear interpolation,
the `phase125_cross_compilation.percentile_type7`
convention) 2.5th / 97.5th percentiles of the
replicate distribution, unless a section says
otherwise. All reported floats are rounded to 6
decimals, as in Phase-125.

## 3. Arm (a) — Holdat split-half noise floor

For each of the 16 judgeable pairs, take the M sign's
**Holdat token pool**: the list of positional-class
labels (INITIAL / MEDIAL / TERMINAL, per the frozen
convention) of that sign's Holdat tokens, in
inscription order. In each replicate: shuffle the pool
with the §2 stream, split it into a first half of size
⌊n/2⌋ and a remainder of size ⌈n/2⌉, compute each
half's profile, and record TV(half₁, half₂).

Per sign, report: n, the replicate median TV, and the
95% percentile interval. Across signs, report the
**median of the per-sign median TVs** (the split-half
noise floor) and the distribution of replicate medians
across signs per replicate index is *not* pooled —
split-half replicates are per-sign objects.

**Full-size scaling (registered estimator).** A
split-half TV compares two samples of size ≈ n/2. For
multinomial class counts, the expected TV between two
independent samples of the same underlying profile
scales as 1/√(sample size); the split-half figure
therefore estimates the noise of a comparison at
half size. The **full-size noise-floor estimate** is
registered as split-half median TV / √2, reported
alongside the raw split-half figure wherever either
appears, and labelled an approximation under the
multinomial scaling assumption (A3's clustering
caveat applies to both).

## 4. Arm (b) — Matched-size subsampling null

For each judgeable pair (P, M) with mayig token count
m = n_mayig(P) and Holdat count n = n_holdat(M): in
each replicate, draw m Holdat tokens of M **without
replacement** from M's Holdat class-label pool (the §3
pool, shuffled by the §2 stream; the first m labels
are the subsample, the remaining n − m are the
remainder). Record:

- **Primary:** TV(subsample profile, remainder
  profile) — two disjoint Holdat samples, one at
  exactly the mayig size: the TV pure Holdat-internal
  sampling produces at mayig's size against an
  independent Holdat reference.
- **Secondary (recorded):** TV(subsample profile,
  full-Holdat profile of M).

Per replicate, the **median across the 16 pairs** of
the primary statistic is recorded; the arm reports
that distribution's median (**matched-size expected
median TV**), its 95% percentile interval, and the
share of replicates whose median ≥ the observed
Phase-125 median TV 0.636931. Per-sign medians and
intervals are also reported.

*Registered limitation:* this arm captures Holdat-side
sampling at mayig sizes against a Holdat reference. It
does not include mayig-side sampling noise; §5's
bootstrap (which resamples both compilations) is the
procedure that prices both sides. The two arms are
reported together and never averaged.

## 5. Arm (c) — Inscription-level bootstrap CIs

Both layers support inscription-level resampling (A3):
mayig inscriptions are layer records; Holdat
inscriptions are the loader's grouped token lists. In
each of B = 999 replicates: resample the mayig
inscriptions with replacement (179 drawn), resample
the Holdat inscriptions with replacement (1,670
drawn), independently, from the §2 stream; recompute
each judgeable sign's profile within its resampled
compilation (per-inscription positional counts summed
over the drawn inscriptions — exactly the frozen
convention applied to the resampled multiset);
record each pair's TV.

The judgeable set is **fixed** (A1): it is not
re-floored per replicate. If a sign has 0 tokens in a
replicate (possible only for the smallest mayig
signs), that pair's TV is undefined for that
replicate: it is excluded from that replicate's
median, and the exclusion count per pair is reported.

Report: per-pair TV percentile 95% CI (and the
bootstrap median); the replicate distribution of the
median TV across pairs — its median and 95%
percentile interval is the **CI for the median TV**.

## 6. Arm (d) — Crosswalk arm decomposition

**Registered fact of construction:** the PRIMARY arm
admits only pairs that are unambiguous within the
high-confidence pair set (spec 019 §3). Ambiguous
mappings therefore contribute **exactly zero** to the
Phase-125 PRIMARY TVs by construction — no estimator
is needed for that statement, and no Phase-127 number
may be phrased as though ambiguity leaked into the
primary arm. What this arm quantifies is the
**counterfactual**: what the same signs' TVs look
like when the ambiguous mappings the primary arm
excluded are admitted, and how much of each pair's
observed TV the choice of mapping accounts for under
the estimator below.

For each judgeable primary pair (P, M), define its
**crosswalk neighbourhood** from crosswalk v1's
all-pairs set (arm B of Phase-125, 762 pairs): all
pair rows (P, M′) with the same P, plus all pair rows
(P′, M) with the same M. Report per pair:

- k_P = number of all-pairs rows for P; k_M = number
  for M; neighbourhood size (union of rows);
- **ambiguity share** = (|neighbourhood| − 1) /
  |neighbourhood| — the share of the pair's mapping
  neighbourhood that is *not* the primary pair (0 iff
  the pair is the sole row for both signs);
- the **neighbourhood judgeable comparisons**: every
  neighbourhood row other than the primary pair whose
  both sides meet the frozen floor 8 in their own
  compilations (the Phase-125 arm-B judgeability
  rule), with its TV computed by the frozen machinery;
- **neighbourhood median TV** = median TV over those
  comparisons (null if none is judgeable);
- **attributable TV (estimator)** = TV_primary(pair) −
  neighbourhood median TV, reported signed, and
  **attributable share** = attributable TV /
  TV_primary(pair) when TV_primary > 0 (null when
  TV_primary = 0 or the neighbourhood median is null).
  Reading, registered: a positive attributable TV
  means the primary (unambiguous, high-confidence)
  mapping disagrees *more* than the ambiguous
  alternatives typically do — i.e. under this
  estimator, ambiguity is not what produces that
  pair's disagreement; a negative value means the
  ambiguous alternatives disagree more than the
  primary pair. This is a descriptive comparison of
  mapping choices (A4), not evidence about which
  mapping is correct (spec 019 A4 applies unchanged).

Arm-level summaries: median ambiguity share across
the 16 pairs; median attributable TV and share across
pairs where defined; the count of pairs with no
judgeable neighbourhood comparison.

## 7. Arm (e) — Composition controls (metadata-bounded)

Composition controls are computed **only** where the
metadata supports the same stratum on both sides.
The support facts, from metadata columns only:

- **Site.** Every mayig inscription is a Mohenjo-daro
  object (CISI ID prefix `M-`, layer metadata: all 179
  objects are M-series). Holdat's CSV carries a `site`
  column per inscription: Mohenjo-daro 606 of 1,670
  inscriptions (the rest: Harappa 492, Lothal 124,
  Kalibangan 110, Dholavira 106, Chanhu-daro 78,
  Surkotada 61, Banawali 60, Rakhigarhi 33). A
  site-matched control **is supported**: restrict
  Holdat to Mohenjo-daro inscriptions.
- **Object type / iconography.** Every mayig
  inscription's `description` is a unicorn seal
  variant ("unicorn I/II/III/IV/V seal"; 179 of 179).
  Holdat's CSV carries an `iconography` column per
  inscription: unicorn 514 of 1,670 (the rest: zebu
  bull 347, elephant 200, rhinoceros 170, script only
  138, geometric 93, tiger 72, buffalo 72, gharial
  64). An iconography-matched control **is
  supported**: restrict Holdat to unicorn-iconography
  inscriptions. (Both layers' objects are seals; the
  mayig description's seal wording and Holdat's seal
  population agree that object type at the seal level
  has no variance to control on the mayig side.)

Controls (each is a Holdat-side restriction only; the
mayig side is already entirely inside every stratum,
so no mayig restriction exists or is needed):

1. **SITE:** Holdat restricted to site = Mohenjo-daro.
2. **ICONOGRAPHY:** Holdat restricted to
   iconography = unicorn.
3. **SITE ∧ ICONOGRAPHY:** both restrictions.

For each control: recompute the Holdat profiles from
the restricted inscription set (within-compilation,
frozen machinery; stratum membership read from the
CSV's `site` / `iconography` columns per inscription,
grouped exactly as the Phase-125 loader groups, with
per-inscription stratum consistency asserted — an
inscription whose rows disagree on a stratum value is
counted and excluded from that control, never
silently assigned). Re-apply the frozen floor 8 to
the restricted Holdat counts (mayig counts unchanged):
report the restricted judgeable count, the per-pair
restricted TVs, and the **median TV over the
restricted judgeable set**, next to the Phase-125
median TV over its judgeable set. Controls issue no
verdict and are compared descriptively only.

**Gaps, stated instead of improvised (binding):**

- The mayig unicorn **variants** (I–V) have no
  counterpart granularity in Holdat's `iconography`
  column (a single `unicorn` value): variant-level
  composition **cannot** be controlled and is not.
- The mayig layer has **no non-Mohenjo-daro site, no
  non-seal object type, and no non-unicorn
  iconography**: no mayig-side stratum restriction is
  possible, and no stratum beyond site and
  iconography exists on both sides. Provenience
  finer than site, artefact material, and find
  context are absent from the mayig layer metadata
  and **cannot** be controlled.
- Inscription **length** composition is token data,
  not layer metadata; it is outside this arm's
  registered scope and is not controlled here.

## 8. Arm (f) — Power statement

Derived from the sampling machinery of §§3–4, method
registered here: for tokens-per-sign grid
n ∈ {8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256},
for each judgeable M sign, in each of B = 499
replicates draw min(n, n_holdat(M)) tokens without
replacement from M's Holdat class-label pool and
record TV(subsample, remainder) (the §4 primary
statistic — pure sampling noise at size n against a
disjoint Holdat reference). Signs whose Holdat count
≤ n contribute no replicate at that grid point (no
remainder exists) and are counted as excluded there.

The power statement reports, per grid point: the
per-sign noise distribution's 95th percentile pooled
across contributing signs, and the 95th percentile of
the per-replicate median-across-signs. **Tokens-per-
sign required** is the smallest grid n at which the
95th percentile of the per-replicate median TV ≤
0.35 (the frozen Phase-125 PASS bound) — the size at
which a median-TV PASS/FAIL reading stops being
dominated by sampling noise at the observed effect
scale — reported together with the smallest n at
which the pooled per-sign 95th percentile ≤ 0.35
(the stricter, per-sign figure). If no grid point
qualifies, the statement says so and reports the
largest grid point's values instead of extrapolating.
The statement is about the *gates'* informativeness;
it re-opens no gate and re-judges no pair (A1, §0).

## 9. Claim scope and limitations (registered)

- Every finding is a statement about the **16
  judgeable primary pairs** and the frozen Phase-125
  design — never about "the script", the crosswalk's
  correctness for any individual pair (spec 019 A4),
  any below-floor or ambiguous pair's identity, or
  Holdat vs the ICIT lineage (Phase-116 R-NONE stands
  untouched).
- "Genuine" in this phase's vocabulary means exactly:
  *not accounted for by the §§3–5 sampling nulls, the
  §6 mapping-choice estimator, or the §7 controls, at
  the observed sizes*. It is not a claim about which
  side (transcription, segmentation, population
  beyond the controlled strata) produces the residual
  disagreement; that attribution is out of scope.
- Token-level arms (§§3–4, §8) understate clustered
  noise (A3); the inscription bootstrap (§5) is the
  conservative uncertainty statement and governs
  where the two disagree in implication.
- The matched-size null (§4) prices Holdat-side noise
  only; the split-half floor (§3) is a within-Holdat
  object. Neither is a model of mayig-side
  transcription practice.
- No finding of this phase changes, softens, or
  re-opens the Phase-125 FAIL verdict (§0). A
  successor phase that wished to act on this
  diagnostic would need its own spec and its own
  owner authorization.

## 10. Implementation (this phase)

Following H15/H23 (graph-first, 5-step gate) and the
Phase-125 file pattern:

1. `backend/glossa_lab/phase127_diagnostic.py` — pure
   machinery: class-label pools, split-half (§3),
   matched-size subsampling (§4), inscription
   bootstrap (§5), neighbourhood decomposition (§6),
   composition-control evaluation (§7), power grid
   (§8). Pure functions over inscription lists,
   per-inscription count vectors, crosswalk rows, and
   the Phase-125 judgeable records; reuses
   `phase125_cross_compilation` / `phase113_battery`
   machinery; no hardcoded corpus data (H16).
2. `backend/glossa_lab/phase127_run.py` —
   orchestration: loads the frozen inputs through
   their loaders, asserts corpus totals and the
   anchors hash before and after, reads the Phase-125
   judgeable set from the results of record, computes
   all arms, writes the artifacts. Includes
   `gpu_device` (H20 pattern; no SA is run).
3. `backend/scripts/phase127_cross_compilation_diagnostic.py`
   — the phase script (runner for `phase127_run`).
4. `backend/glossa_lab/experiment_graph_phase127.py`
   — node `IndusPhase127CrossCompilationDiagnostic`,
   registered in `experiment_graph.py` by try/except
   import and asserted present in `ATOMIC_NODES`
   **before** the script is run (H23).
5. `backend/tests/test_phase127_diagnostic.py` — unit
   tests including: pool/profile machinery on toy
   corpora with hand-computed values; split-half on a
   single-profile toy pool (TV distribution centred
   near the multinomial expectation, deterministic
   under the frozen seed); matched-size subsampling
   on toy pools; bootstrap CI machinery on toy
   inscriptions; neighbourhood decomposition on
   synthetic crosswalk rows (ambiguity share and
   attributable TV hand-computed); composition-control
   evaluation on toy stratum-tagged inscriptions;
   power-grid machinery on toy pools; determinism
   (same seed → identical output); and real-input
   pins: the judgeable set is exactly Phase-125's 16
   PRIMARY pairs and the observed median TV read from
   the results of record is 0.636931.
6. Full backend suite + foundation check (H21 — this
   phase adds phase result files under `reports/`);
   ruff clean.
7. Ledger entries in `LEDGER.md` and
   `glossa-indus/LEDGER.md` (H1), with AI disclosure.
8. One PR; merge only when complete and all CI green,
   per the owner's standing auto-merge rule. If CI is
   not green, pause and report — do not merge on
   defaults.

## 11. Deviations

Any deviation from this spec discovered during
execution is recorded in the report and the ledger,
not absorbed. The judgeable set, arms, estimators,
seeds, replicate counts, grids, and interval methods
are not adjustable after the freeze commit; a
substantive design error voids the design and
requires a new spec.

## 12. Deliverables (frozen)

- `specs/021-phase127-cross-compilation-diagnostic/{spec,plan,tasks}.md`
  (spec freeze commit first, before any code)
- `backend/glossa_lab/phase127_diagnostic.py`,
  `backend/glossa_lab/phase127_run.py`,
  `backend/glossa_lab/experiment_graph_phase127.py`
  (+ registration in `experiment_graph.py`)
- `backend/scripts/phase127_cross_compilation_diagnostic.py`
- `backend/tests/test_phase127_diagnostic.py`
- `reports/phase127_cross_compilation_diagnostic_results.json`
  (inputs + hashes, per-arm per-pair records, null /
  CI summaries, composition controls, power grid)
- `reports/phase127_cross_compilation_diagnostic.md`
  (abstract states the Phase-125 verdict unchanged in
  its first lines)
- Anchors file **unchanged** (sha256 asserted)
- Ledger entries in `LEDGER.md` and
  `glossa-indus/LEDGER.md` (AI disclosure); suite +
  foundation results recorded in the report
- One PR; merged only when complete + green

## Appendix A — Frozen facts of record (no new statistics)

| Fact | Value |
|---|---|
| Phase-125 verdict (FINAL) | FAIL — DISAGREEMENT (spec 019 §6.3) |
| Phase-125 PRIMARY judgeable / pairs | 16 / 286 |
| Phase-125 observed median TV | 0.636931 |
| Phase-125 Spearman ρ initial / terminal | −0.424758 / 0.316034 |
| Phase-125 shuffle null p (B = 999, seed 125125) | 0.824 |
| Crosswalk v1 pairs (high / medium / low) | 762 (372 / 0 / 390) |
| mayig layer | 179 inscriptions / 1,003 tokens / 182 signs |
| Holdat (as loaded by Phase-125) | 1,670 inscriptions / 7,002 tokens / 390 signs |
| Anchors sha256 (asserted unchanged) | `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed` |
| §7 metadata support | mayig: 179/179 Mohenjo-daro (M-series), 179/179 unicorn-seal descriptions; Holdat: site column (Mohenjo-daro 606/1,670), iconography column (unicorn 514/1,670) |
