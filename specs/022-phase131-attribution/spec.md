# Spec 022 — Phase-131: Source-of-Disagreement Attribution for the Phase-125/127 Cross-Compilation Result (pre-registration)

**Status:** DESIGN FROZEN 2026-10-09 on
`phase/131-attribution` (from origin/main
`7c062ddfb15d94e21a4ead850ecaf4e7b5c77740`). Owner
authorization: Tristen Pierson, 2026-10-09 — STEP 1 of
the owner-ordered Glossa-Lab program (spec 022 +
Phase-131). This spec is committed before any
Phase-131 attribution statistic exists. The only
numbers in this spec are (i) Phase-125 / Phase-127
results of record, quoted verbatim from their
committed results JSONs, (ii) Phase-122 crosswalk /
mayig-layer counts of record, and (iii) the
design-stage join-feasibility counts of Appendix A
(join-stage and eligibility counts only — no
alignment classification, no profile, and no distance
is computed at design stage beyond the exact-match
counts Appendix A records as the basis for §3's
matcher tiers, following the spec 019 Appendix A /
spec 015 §1 pre-freeze measurement precedent).

**Phase-numbering note:** ledger-sequence
**Phase-131** (Phase-125 spec 019, Phase-127 spec 021
precede it). Artifact names carry the phase number
(`phase131_attribution`, graph node
`IndusPhase131Attribution`).

**AI disclosure:** this study is designed and executed
by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.

## 0. Context — why this phase exists, and what it is not

Phase-125 (spec 019) returned a FINAL verdict:
**FAIL — DISAGREEMENT** (PRIMARY arm: 16 judgeable
pairs of 286; median TV **0.636931**; Spearman ρ
initial **−0.424758** / terminal **0.316034**;
pairing-shuffle null p = **0.824**). Spec 019 §7
stated that a FAIL "does not identify which side
(transcription, segmentation, crosswalk, population)
produces the disagreement; mechanism attribution
would require a successor diagnostic spec in the
Phase-116 pattern."

Phase-127 (spec 021) was the first such diagnostic:
it decomposed the observed distances into sampling
noise (matched-size expected median TV **0.082613**,
95% interval **0.046665–0.131316**; bootstrap CI for
the median TV 0.548638–0.722042), crosswalk-ambiguity
counterfactuals, and site/iconography composition
controls — and it explicitly left the *mechanism*
attribution of the residual disagreement out of
scope (spec 021 §9: the residual is "not accounted
for" by its arms; which mechanism produces it was not
asked). **This spec is the mechanism-attribution
successor.** It asks, for the same finished result:
how much of the disagreement is supported as
segmentation difference, as substitution, as
insertion/deletion (indel / damage), as reading
direction / order, and as population composition —
and how much remains unexplained after every arm has
measured what it can.

**Non-goals, registered in advance and binding on
every artifact of this phase:**

- This phase is **attribution diagnostics ONLY**. It
  does **NOT** re-score Phase-125, applies no verdict
  rule to any Phase-131 number, and issues no PASS /
  FAIL / NULL pattern of its own about the
  cross-compilation question.
- The Phase-125 verdict is **FINAL and unchanged**:
  FAIL — DISAGREEMENT. Spec 020's adjudication
  outcome (**NO**) likewise stands untouched. No
  finding of this phase softens, qualifies,
  conditions, or re-opens either.
- This phase modifies no anchor, issues no PRED
  verdict, changes no status anywhere, and touches
  no Phase-125 or Phase-127 artifact. The anchors
  file is never opened for writing; its sha256
  (Appendix B) is asserted unchanged at the end of
  the run.
- Arm B (§4) recomputes the Phase-125 primary
  statistic under reversed sequence orientation
  **as an attribution diagnostic only**. It is not a
  re-score of Phase-125: no Phase-125 gate is
  applied to it, and the report states this
  explicitly wherever an Arm B number appears.

## Epistemic boundaries

Assumptions, declared:

- **A1 — Fixed judgeable set.** Arms B and C operate
  on exactly the **16 PRIMARY judgeable pairs of
  Phase-125** (spec 019 §4.2 floor 8, PRIMARY arm),
  taken from the Phase-125 results of record. No pair
  is added or removed, except where §5's within-
  stratum floor re-application is itself the reported
  object — and there the stratum judgeable counts are
  reported alongside, never substituted for, the
  fixed set.
- **A2 — Same machinery.** Profiles, positional
  counts, and TV are computed with the Phase-125 /
  Phase-113 machinery exactly (`phase113_battery`
  positional convention; `phase125_cross_compilation`
  profile/TV functions and the `phase127_diagnostic`
  helpers reused, not reimplemented). Inscriptions
  are never pooled across compilations.
- **A3 — The object-join discipline (binding).**
  Spec 019 §2.1 and spec 015 §1 established, as facts
  of record, that **Holdat's `cisi_number` is
  Holdat-internal sequential numbering, not a CISI
  object ID**, and that the zero-padded coincidence
  (Holdat `M-0001` vs mayig `M-1`) is **not** an
  identity join and must never be used as one. Arm A
  therefore proceeds in registered join stages (§3.1)
  and establishes object identity, where it can, only
  by inscription **content** in the shared M-sign
  space — the Phase-116 §4 matcher route, adapted in
  §3.2. Identity so established is **textual, not
  artifactual** (Phase-116 §8 language): a matched
  pair establishes that the same sign text, up to the
  registered matcher tolerance, occurs in both
  compilations.
- **A4 — Descriptive attribution only.** Every share
  in §6 is a pre-registered descriptive estimator
  with its definition attached wherever its numbers
  appear. No share is a causal estimate, and no
  mechanism is credited beyond what its own arm
  measured (§6).
- **A5 — Determinism.** This phase has **no
  stochastic procedure**: the matcher, the alignment,
  and every statistic are deterministic functions of
  the frozen inputs. Two runs must produce identical
  statistics (timestamps aside). Where the alignment
  dynamic program has tied optima, the tie-break of
  §3.3 is part of the frozen design.
- **A6 — Small joins are findings.** If a join stage
  or a matched set is small or empty, that is
  reported as found, with counts. No threshold in
  this spec may be loosened after the freeze to
  manufacture a larger matched set (§9).

## 1. The question (registered)

> For the Phase-125 PRIMARY result (16 judgeable
> pairs, observed median TV 0.636931): (a) on objects
> that can be matched between Holdat and the
> mayig/CISI layer, what do the pairwise sequence
> differences look like, class by class, and what is
> the positional-profile TV on matched objects only;
> (b) does reversing either compilation's sequences
> collapse the primary statistic into the Phase-127
> sampling-noise band — i.e. is reading direction a
> supported mechanism; (c) how does the disagreement
> distribute across the metadata strata that exist,
> and how much survives a composition adjustment to a
> common composition; and (d) what share of the
> observed disagreement does each mechanism's arm
> support, and what share remains unexplained?

## 2. Frozen inputs

Inputs are exactly the Phase-125/127 frozen inputs,
loaded through the same loaders:

| Input | Path / loader | Frozen fact |
|---|---|---|
| mayig CISI layer v1 | `data/corpus_layers/mayig_cisi_layer_v1.json` via `backend/glossa_lab/data/mayig_layer.py` | 179 inscriptions / 1,003 tokens / 182 P signs; sha256 `6a7664c605079373ca80e70b7e9559c1527613e3f67b579a817ced785e129860` |
| Holdat corpus | gitignored CSV in the main checkout, via `phase125_run._find_holdat_csv` + `phase113_run.load_holdat_inscriptions`; stratum columns via the `phase127_run.load_holdat_stratified` pattern | 1,670 inscriptions / 7,002 tokens / 390 M signs; sha256 `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`; never committed or redistributed |
| Crosswalk v1 | `data/crosswalks/parpola_mahadevan_crosswalk_v1.json` via its Phase-122 loader | 762 pairs; high 372 / medium 0 / low 390; sha256 `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb` |
| Phase-125 results | `reports/phase125_cross_compilation_results.json` | the 16 PRIMARY judgeable pairs; observed median TV 0.636931; verdict FAIL |
| Phase-127 results | `reports/phase127_cross_compilation_diagnostic_results.json` | matched-size noise band: median **0.082613**, 95% interval **[0.046665, 0.131316]** (arm (b), B = 999, seed 127002) |
| Anchors (read-only assertion) | `backend/reports/INDUS_FINAL_ANCHORS.json` | sha256 `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`, asserted unchanged |

**The Phase-127 matched-size noise band (registered
for §4's criterion):** the distribution of the median
TV under pure Holdat-internal sampling at mayig token
counts has median 0.082613 and type-7 95% percentile
interval **[0.046665, 0.131316]**. In this spec "the
noise band" means that interval; its **upper bound
0.131316** is the §4 support threshold.

All reported floats are rounded to 6 decimals, as in
Phases 125/127.

## 3. Arm A — Matched-object alignment

### 3.1 Join stages (all counted, all reported)

Starting populations: mayig **179** objects (one
inscription record each); Holdat **1,670**
inscriptions. Stages, in order:

- **S1 — Direct CISI-ID join.** mayig keys are true
  CISI object IDs (`M-1` … `M-184`). Holdat keys are
  internal sequential numbers (A3). Apparent
  zero-padded namesakes (every mayig number has a
  Holdat `M-NNNN` with the same integer) are counted
  as **apparent** and **rejected as non-identity**:
  validated S1 matches = **0 by the A3 discipline**,
  whatever the apparent count. Any implementation
  that joins on S1 is in deviation (§9).
- **S2 — Catalogue cross-reference join.** Any
  committed table mapping Holdat keys (`cisi_number`,
  `seal_id`, `form`) to CISI object IDs. The run
  asserts the search it performs (the crosswalk
  files and corpus-layer metadata of §2); the count
  of usable cross-references found is reported as
  found.
- **S3 — Shared artifact keys.** Keys present on both
  sides with the same meaning (mayig `side_id` /
  `source_file` are mayig-internal; Holdat `seal_id`
  / `form` are Holdat-internal). Count reported as
  found.
- **S4 — Content matcher (§3.2).** The only stage
  that can produce matched pairs under A3.

### 3.2 The content matcher (frozen)

The **primary crosswalk map** is the Phase-125
PRIMARY arm's pair set (286 unambiguous
high-confidence pairs), used as a function P → M.
A mayig inscription is **matcher-eligible** iff
**every** one of its tokens has a primary-map image
(design-stage count: 32 of 179; Appendix A). Its
**mapped sequence** is the token-wise image in
M-space. Eligibility, and its coverage of the 179,
is reported with counts; ineligible inscriptions are
excluded from matching, never partially mapped —
a wildcard/sentinel design was considered and
rejected at design stage because Appendix A's
wildcard-exact probe found no matches either, and
partial sequences would make the §3.3 segmentation
classes uninterpretable.

For an eligible mapped sequence `a` and a Holdat
sequence `b`, **similarity** is
`1 − lev(a, b) / max(|a|, |b|)`, where `lev` is
unit-cost Levenshtein distance. Tiers, assigned in
this order, each pair in at most one tier:

- **Tier EXACT:** `a == b`, and the pairing is
  mutually unique (a matches exactly one Holdat
  inscription; that inscription is matched by exactly
  one eligible mayig inscription).
- **Tier EXACT-REV:** `a == reverse(b)` under the
  same mutual-uniqueness rule, and the pair is not
  Tier EXACT. A pair compatible in both orientations
  is **ambiguous-orientation**: excluded from both
  tiers, counted.
- **Tier NEAR:** not in an exact tier; `a`'s best
  Holdat candidate by similarity has similarity
  **≥ 0.60**, that candidate's best eligible-mayig
  candidate (same similarity) is `a` (mutual best),
  and the pairing is not also mutual-best in reversed
  orientation at ≥ 0.60 (if it is, the pair is
  ambiguous-orientation: excluded, counted).

**MATCHED set** = Tier EXACT ∪ Tier EXACT-REV ∪ Tier
NEAR pairs. Per-tier counts, the eligible count, and
the matched count are all reported. The matched
mayig coverage (matched / 179) and matched Holdat
coverage (matched / 1,670) are reported.

### 3.3 Alignment and difference classification (frozen)

For each matched pair, align the mapped mayig
sequence `a` (M-space) to the Holdat sequence `b`
(for Tier EXACT-REV pairs, align to `reverse(b)` and
record the tier so the reversal is never hidden) by
unit-cost Levenshtein dynamic programming.
**Tie-break (frozen):** when multiple optimal
alignments exist, prefer, at each backtrace step,
**diagonal (match/substitution) over deletion
(a-token unaligned) over insertion (b-token
unaligned)**.

Group the alignment columns into maximal **blocks**
separated by match columns. A block with `p` a-side
tokens and `q` b-side tokens is one **difference**,
classified exactly one way:

- `p == q ≥ 1` (all diagonal): **substitution** —
  the block contributes `p` substituted tokens.
- `p == 1, q == 2`: **segmentation split** — one
  mayig-side sign corresponds to two Holdat-side
  signs in the alignment.
- `p == 2, q == 1`: **segmentation merge** — two
  mayig-side signs correspond to one Holdat-side
  sign.
- otherwise (`p == 0` or `q == 0`, or `{p, q}` not in
  {1,2}×{1,2} with `p ≠ q`): **insertion-deletion**
  (indel / damage).

Each matched **pair** receives exactly one pair
class, by this priority: **identical** (no difference
block) > **order-only** (`a` ≠ `b` but the token
multisets of `a` and `b` are equal — checked before
blocks) > the class of the pair's **first** difference
block in alignment order (split / merge /
substitution / insertion-deletion).

Report: per-tier and total pair-class counts;
difference-block counts by class; token counts by
class; and **at least 3 concrete examples per
non-identical pair class (or all pairs of the class
if fewer than 3)** — each example naming the mayig
object ID, the Holdat key, both sequences, and the
alignment blocks. (Holdat keys and sequences are
published only as the matched examples' sign-token
sequences, consistent with the Phases 125/127
statistics-only publication pattern for Holdat
material.)

### 3.4 Matched-object positional TV (frozen)

Restrict each compilation to its matched
inscriptions (mayig: matched eligible records;
Holdat: matched inscriptions). Recompute profiles
for the fixed 16 judgeable pairs (A1) on the
restricted inscriptions only. A pair's matched TV is
**defined** iff both restricted counts are ≥ 1.
The **matched-object median TV** is **estimable**
iff (i) the MATCHED set has ≥ **10** pairs
(`MIN_MATCHED = 10`, frozen) **and** (ii) ≥ 4 of the
16 pairs have defined matched TVs; it is then the
median over the defined pairs, reported with the
defined-pair count. Otherwise the matched-object
median TV is **NOT ESTIMABLE**: the per-pair defined
TVs and counts are still reported, and the reason
(which of (i)/(ii) failed, with counts) is stated.

## 4. Arm B — Reading direction (frozen criterion)

Recompute the Phase-125 primary statistic — median
TV over the fixed 16 judgeable pairs, same profiles,
same TV definition (A1, A2) — under two named arms:

- **B1 — mayig reversed:** every mayig inscription's
  token sequence is reversed before profiling; Holdat
  unchanged.
- **B2 — Holdat reversed:** every Holdat
  inscription's sequence is reversed; mayig unchanged.

Reversal does not change token counts, so the
judgeable set is identical by construction; this is
asserted in code. Per-pair TVs and the median TV are
reported per arm, plus the reduction
`0.636931 − median TV` per arm.

**Support criterion (frozen):** an arm **supports
direction as a mechanism** iff its median TV falls
to or below the Phase-127 matched-size noise band's
upper bound: **median TV ≤ 0.131316** (§2). An arm
whose median TV is above the band does not support
direction as *the* mechanism under this criterion,
whatever its reduction; the reduction is still
reported as found.

**Binding framing:** Arm B is attribution
diagnostics, **not a re-score of Phase-125**. No
Phase-125 gate, bound, or verdict rule is applied to
any Arm B number; Phase-125's FAIL stands untouched
(§0), and the report repeats this in the Arm B
section itself.

## 5. Arm C — Stratification and composition adjustment

### 5.1 Strata (frozen)

TV is recomputed **within matched strata**: for a
stratum, each compilation is restricted to its
inscriptions in that stratum, profiles are recomputed
within the restriction (A2), and the frozen floor 8
is re-applied **within the stratum on both sides**.
A stratum's median TV is **estimable** iff ≥ **4**
pairs are judgeable within the stratum
(`MIN_STRATUM_PAIRS = 4`, frozen); otherwise the
stratum is reported with its inscription counts,
token counts, and judgeable count, and marked
**NOT ESTIMABLE**. (Estimable strata report the
median over their own judgeable pairs, A1's caveat.)

- **Site.** mayig is entirely Mohenjo-daro (M-series,
  179/179). Strata: Mohenjo-daro (both sides) plus
  every Holdat site with ≥ 1 inscription — for which
  the mayig side is empty and the stratum is NOT
  ESTIMABLE by construction; those rows are reported
  as counts, not silently dropped.
- **Object type.** mayig descriptions are unicorn
  seal variants **I / II / III / IV / V**; Holdat's
  `iconography` column's corresponding level is the
  single value `unicorn`. Strata: each variant
  (mayig restricted to the variant; Holdat restricted
  to `iconography == unicorn`), plus every other
  Holdat iconography value as a mayig-empty NOT
  ESTIMABLE row. (Both layers' objects are seals;
  seal-level object type has no variance to stratify.)
- **Text length.** Bins (frozen): **1**, **2–3**,
  **4–5**, **6+** tokens. Both sides restricted to
  inscriptions whose token count falls in the bin.
- **Period.** Neither the mayig layer metadata nor
  the Holdat CSV carries a period / dating field.
  Period stratification is therefore **NOT
  ESTIMABLE** in every cell, stated as a global gap —
  not improvised from site or any proxy.

Stratum-inconsistent Holdat inscriptions (rows of one
inscription disagreeing on site or iconography) are
counted and excluded from the affected stratum,
never silently assigned (Phase-127 pattern).

### 5.2 Composition adjustment (frozen estimator)

The only non-degenerate composition observable on
both sides is **text length** (site and object type
are constant on the mayig side; their "adjustment"
is the corresponding §5.1 stratum, and the report
says so instead of double-counting). The adjusted
comparison reweights Holdat to the mayig length
composition:

- Let `w_bin` = the mayig share of inscriptions in
  each §5.1 length bin (bins with `w_bin = 0` play
  no part).
- For each of the fixed 16 pairs' Holdat sign `M`:
  the **adjusted profile** is
  `Σ_bin ŵ_bin · profile_bin(M)` over bins where
  Holdat attests `M` (≥ 1 token of `M` in that bin),
  with `ŵ` the mayig weights renormalized over those
  bins. **Coverage** per pair = the sum of `w_bin`
  over the bins used, reported per pair.
- The **composition-adjusted median TV** is the
  median, over pairs whose mayig count meets floor 8
  (all 16 by construction — asserted) and whose
  adjusted Holdat profile is defined, of
  TV(mayig full profile, adjusted Holdat profile).
  It is estimable iff ≥ 4 pairs are included
  (`MIN_STRATUM_PAIRS`); otherwise NOT ESTIMABLE with
  counts. The unadjusted comparator is the Phase-125
  observed median TV 0.636931 of record.

## 6. Arm D — Synthesis: the attribution table (frozen estimators)

One row per mechanism. A row's **supported share** is
computed by exactly its registered estimator; a row
whose estimator's inputs are not estimable is marked
**NOT ESTIMABLE** — never filled by another arm's
number.

| Mechanism | Estimator (frozen) | Estimable iff |
|---|---|---|
| Segmentation (split/merge) | (tokens in split blocks + tokens in merge blocks) / (tokens in all difference blocks), over the Arm A MATCHED set; block token count = `p + q` per block | MATCHED ≥ `MIN_MATCHED` (10) and ≥ 1 difference block |
| Substitution | (tokens in substitution blocks) / (tokens in all difference blocks), same basis | same |
| Insertion-deletion / damage | (tokens in indel blocks) / (tokens in all difference blocks), same basis | same |
| Order / direction | `(0.636931 − min(medianTV_B1, medianTV_B2)) / 0.636931`, clipped to [0, 1], credited **only** if the corresponding arm meets §4's support criterion; if neither arm supports, the credited share is **0.000** and the raw reductions of both arms are reported beside it | Arms B1/B2 always computable (deterministic) |
| Composition | `(0.636931 − composition-adjusted median TV) / 0.636931`, clipped to [0, 1] | §5.2 adjusted median estimable |
| Matched-object residual | matched-object median TV (§3.4) / 0.636931 — the share of the observed disagreement that **persists on matched objects**; a persistence measure, not an explained share, and labelled as such | §3.4 estimable |

**Residual unexplained share** = `1 − (sum of the
credited explained shares: segmentation +
substitution + indel + order/direction +
composition)`, floored at 0, reported plainly.
**Overlap caveat (binding on the report's wording):**
the order/direction and composition shares both act
on the median-TV scale and may overlap in what they
account for; the Arm A shares act on matched-pair
token differences, a different denominator. Shares
are therefore **not forced to sum to 100%**, the
table reports each share with its basis named, and
if the credited shares sum to more than 1 the
residual is reported as 0 with the overlap stated —
never resolved by rescaling.

## 7. Claim scope and limitations (registered)

- Every finding is a statement about the frozen
  inputs, the 16 judgeable primary pairs (Arms B/C),
  and the Arm A matched set **as found** — never
  about "the script", any individual pair's crosswalk
  correctness (spec 019 A4), or Holdat vs the ICIT
  lineage (Phase-116 R-NONE stands untouched).
- Arm A identity is textual, not artifactual (A3):
  a matched pair shows the same text occurs in both
  compilations under the primary crosswalk map; it
  does not show the two records describe the same
  physical object, and the primary map's own
  correctness is not validated by matching (matching
  is conditional on the map).
- The matcher-eligible subset (32/179 at design
  stage) is biased toward inscriptions built from
  well-attested, unambiguously mapped signs. Arm A
  findings describe that subset, named as such.
- Arm B's criterion prices direction against the
  Phase-127 noise band, which is a Holdat-internal
  sampling object (Phase-127's registered
  limitation); "supports direction" means exactly
  §4's criterion, nothing more.
- No finding of this phase changes, softens, or
  re-opens the Phase-125 FAIL verdict or spec 020's
  NO (§0). A successor phase that wished to act on
  this attribution would need its own spec and its
  own owner authorization.

## 8. Implementation (this phase)

Following H15/H23 (graph-first, 5-step gate) and the
Phase-127 file pattern:

1. `backend/glossa_lab/phase131_attribution.py` —
   pure machinery: primary-map construction (reusing
   `phase125_cross_compilation.build_arms`), matcher
   tiers (§3.2), Levenshtein alignment + block
   classification (§3.3), matched-object TV (§3.4),
   reversed-context TV (Arm B), stratified TV +
   composition adjustment (Arm C), synthesis shares
   (§6). Pure functions over inscription lists and
   crosswalk rows; reuses `phase113_battery` /
   `phase125_cross_compilation` / `phase127_diagnostic`
   machinery; no hardcoded corpus data (H16).
2. `backend/glossa_lab/phase131_run.py` —
   orchestration: loads the frozen inputs through
   their loaders, asserts corpus totals and the
   anchors hash before and after, computes all arms,
   writes the artifacts. Includes `gpu_device` (H20
   pattern; no SA is run).
3. `backend/scripts/phase131_attribution.py` — the
   phase script (runner for `phase131_run`).
4. `backend/glossa_lab/experiment_graph_phase131_attribution.py`
   — node `IndusPhase131Attribution`, registered in
   `experiment_graph.py` by try/except import and
   asserted present in `ATOMIC_NODES` **before** the
   script is run (H23).
5. `backend/tests/test_phase131_attribution.py` —
   unit tests including: matcher tiers on toy
   sequences (exact / exact-rev / near / ambiguous-
   orientation / mutual-best failure); alignment +
   block classification on hand-computed toy pairs
   (one per class, incl. tie-break determinism);
   pair-class priority (identical, order-only);
   matched-object TV estimability gates; Arm B on toy
   corpora (reversal swaps initial/terminal profiles
   and collapses TV for a direction-only toy
   disagreement); Arm C strata floors / NOT ESTIMABLE
   marking and the §5.2 reweighting estimator on toy
   counts; synthesis shares incl. clipping, the
   NOT ESTIMABLE rows, and the unfloored-sum overlap
   rule; determinism (two runs identical); real-input
   pins: the judgeable set is exactly Phase-125's 16
   PRIMARY pairs, the observed median TV of record is
   0.636931, and the Phase-127 noise band of record
   is [0.046665, 0.131316].
6. Full backend suite + foundation check (H21 — this
   phase adds phase result files under `reports/`);
   ruff clean.
7. Ledger entries in `LEDGER.md` and
   `glossa-indus/LEDGER.md` (H1), with AI disclosure.
8. One PR; merge only when complete and all 7 CI
   checks green, per the owner's standing auto-merge
   rule. If CI is not green, pause and report — do
   not merge on defaults.

## 9. Deviations

Any deviation from this spec discovered during
execution is recorded in the report and the ledger,
not absorbed. The join discipline (A3/§3.1), matcher
tiers and threshold (0.60), `MIN_MATCHED` (10),
alignment tie-break, block classes, Arm B support
threshold (0.131316), strata, bins, `MIN_STRATUM_PAIRS`
(4), and the §6 estimators are not adjustable after
the freeze commit; a substantive design error voids
the design and requires a new spec.

## 10. Deliverables (frozen)

- `specs/022-phase131-attribution/{spec,plan,tasks}.md`
  (spec freeze commit first, before any code)
- `backend/glossa_lab/phase131_attribution.py`,
  `backend/glossa_lab/phase131_run.py`,
  `backend/glossa_lab/experiment_graph_phase131_attribution.py`
  (+ registration in `experiment_graph.py`)
- `backend/scripts/phase131_attribution.py`
- `backend/tests/test_phase131_attribution.py`
- `reports/phase131_attribution_results.json`
  (inputs + hashes, join-stage counts, matcher tiers,
  per-pair alignments + classes + examples, matched
  TVs, Arm B per-pair TVs + medians, Arm C stratum
  table + adjusted comparison, Arm D synthesis table)
- `reports/phase131_attribution.md` (states in its
  first lines that this is attribution diagnostics
  only and that the Phase-125 FAIL and spec 020's NO
  stand untouched)
- Anchors file **unchanged** (sha256 asserted)
- Ledger entries in `LEDGER.md` and
  `glossa-indus/LEDGER.md` (AI disclosure); suite +
  foundation results recorded in the report
- One PR; merged only when complete + green

## Appendix A — Design-stage join feasibility (counts only)

*Computed at freeze time, before any Phase-131
attribution statistic. Boundary: every number below
is a join-stage count, an eligibility count, or an
exact-match count under the frozen definitions of
§3 — no alignment was classified, no profile was
computed on matched objects, and no Arm B/C/D
statistic exists in this appendix.*

| Stage / probe | Count |
|---|---|
| mayig objects / inscriptions | 179 / 179 |
| Holdat inscriptions | 1,670 (606 Mohenjo-daro) |
| S1 apparent zero-padded namesakes (mayig M numbers 1–184, all ≤ 606) | 179 apparent / **0 validated** (A3: Holdat numbering is internal sequential, spec 019 §2.1) |
| S2 catalogue cross-references (Holdat key → CISI ID) in committed crosswalk / layer files | 0 found |
| S3 shared artifact keys (same meaning both sides) | 0 |
| Matcher-eligible mayig inscriptions (all tokens primary-mapped) | 32 / 179 (mean primary-map token coverage over all 179: 0.717) |
| Tier EXACT content matches among the eligible (either orientation) | 0 |
| Wildcard-exact probe (all 179; ≥ 2 mapped positions, UNK wildcards, either orientation) | 0 inscriptions with any match |
| Eligible inscriptions whose best Holdat similarity (§3.2) is ≥ 0.60 | 2 / 32 |

Reading registered at freeze: the content route —
the only legitimate join under A3 — is expected to
yield a matched set at or below `MIN_MATCHED`. That
is a finding the run will report as found (§3, A6),
not a defect to paper over by loosening the matcher.

## Appendix B — Frozen facts of record (no new statistics)

| Fact | Value |
|---|---|
| Phase-125 verdict (FINAL) | FAIL — DISAGREEMENT (spec 019 §6.3) |
| Spec 020 adjudication | NO — stands untouched |
| Phase-125 PRIMARY judgeable / pairs | 16 / 286 |
| Phase-125 observed median TV | 0.636931 |
| Phase-125 Spearman ρ initial / terminal | −0.424758 / 0.316034 |
| Phase-125 shuffle null p (B = 999, seed 125125) | 0.824 |
| Phase-127 matched-size noise band | median 0.082613; 95% interval [0.046665, 0.131316] |
| Phase-127 bootstrap CI for median TV | [0.548638, 0.722042] |
| Crosswalk v1 pairs (high / medium / low) | 762 (372 / 0 / 390) |
| mayig layer | 179 inscriptions / 1,003 tokens / 182 signs |
| Holdat (as loaded by Phase-125) | 1,670 inscriptions / 7,002 tokens / 390 signs |
| Anchors sha256 (asserted unchanged) | `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed` |
