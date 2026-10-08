# Spec 019 — Phase-125: Cross-Compilation Positional Comparison — mayig/CISI Layer vs Holdat Compilation, Joined Only Through the Phase-122 Crosswalk (pre-registration)

**Status:** DESIGN FROZEN 2026-10-08 on
`phase/125-cross-compilation-positional` (from main
`d9cbf54c`). Owner authorization: Tristen Pierson,
2026-10-08 — STEP 1 of the owner-ordered Glossa-Lab
program: spec 019 + Phase-125, executed fully in one
authorization (spec → implement → run → PR → merge when
green, under the standing auto-merge rule). This spec is
committed before any Phase-125 comparison statistic
exists: the only numbers computed at design stage are the
instrument-feasibility statistics of Appendix A
(attestation counts, crosswalk pair counts, and
judgeability under the frozen definitions — no sign's
profile is compared to any other sign's profile, no
distance or correlation is computed, and no verdict is
produced), per the program's pre-freeze measurement
precedent (spec 014 §§1–2, spec 016 Appendix A, spec 017
Appendix A, spec 018 Appendix A).

**Phase-numbering note:** ledger-sequence **Phase-125**
(Phase-117 spec 016, Phase-118 spec 017, Phase-119 spec
018 precede it). Artifact names carry the phase number
(`phase125_cross_compilation`, graph node
`IndusPhase125CrossCompilationPositional`). Note: an
unrelated legacy experiment-graph node family named
"Phase-124-125" (fish polysemy / Arthasastra mining)
exists in `experiment_graph_phase124_125.py`; it is not
this phase, is not touched by this phase, and no artifact
of this phase shares a filename with it.

**AI disclosure:** this study is designed and executed
by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.

## Context — why this phase exists

Phase-116 (spec 015) returned **R-NONE** for
cross-corpus positional *validation* between Holdat and
the ICIT lineage: positional profiles in the two
compilations genuinely disagree (Phase-115 v2: 43/94
strict signs FAIL on T1, median TV 0.79), and no
harmonization transformation was justified. That verdict
constrains validation batteries; Phases 117/118 therefore
validated only **within** Holdat.

Phase-122 then added a genuinely new compilation to the
record: the **mayig CISI layer** — a hand digitisation
of the printed CISI volumes (Parpola P-numbering),
integrated as a committed first-class corpus layer
(179 inscriptions / 179 CISI objects / 1,003 tokens /
182 distinct P signs), together with the
**Parpola↔Mahadevan crosswalk v1** (762 pairs + 4
unmapped-P rows; confidence high 372 / medium 0 / low
390; the canonical registry is the map of record, spec
018 §A2). Phase-122 asserted, as an explicit non-claim,
that **"no positional comparison study was run in this
phase."** This phase is that comparison, pre-registered
here before it is run.

The question is deliberately narrow and
compilation-level, not sign-identity-level and not
reading-level: it asks whether two independent modern
compilations of substantially the same artefact
population, transcribed in two different sign
numberings, **tell the same positional story** about
the signs they share — when each compilation's story is
computed strictly inside itself and the two stories are
joined only through the frozen Phase-122 crosswalk.
Phase-116's R-NONE was about Holdat vs the ICIT lineage
(via a Wells-keyed conversion); the mayig layer is a
different lineage (hand digitisation of the printed
CISI volumes, mayig README lineage note in the layer
metadata) and the join here is the crosswalk of record,
not a conversion chain. A PASS here does not overturn
R-NONE (different pair, different join, different
question); a FAIL here does not extend R-NONE to a new
pair by implication — both readings are blocked in §7.

## Epistemic boundaries

Assumptions, declared:

- **A1 — Orientation.** Sign position is the token
  index in the sequence as the source layer emits it;
  no adapter reverses a sequence (the mayig layer's own
  ordering note: tokens in the source's own order; the
  Holdat loader's order: `position` field order within
  each `cisi_number` group). Reading-direction questions
  are inherited from the two sources, not re-decided.
- **A2 — Positional convention.** The Phase-69 /
  spec-011 §3 convention, implemented by
  `phase113_battery.positional_counts` and reused
  unchanged: position 0 of a multi-sign inscription is
  INITIAL, the last position is TERMINAL, everything
  else — including a sole token — is MEDIAL. A sign's
  positional profile is its (INITIAL, MEDIAL, TERMINAL)
  share triple.
- **A3 — Within-compilation logic only.** Every
  profile is computed inside one compilation, from that
  compilation's inscriptions alone. Inscriptions are
  **never pooled** across compilations: no combined
  corpus is built, no profile is ever computed over a
  merged token set, and no statistic in §§5–6 takes a
  cross-compilation token as input. The only
  cross-compilation objects in this study are (a) the
  frozen crosswalk pair list (§3) and (b) per-pair
  comparisons of two separately computed profiles (§5).
- **A4 — No identity adjudication.** A crosswalk pair
  (P, M) is a *join key asserted by the crosswalk of
  record at a stated confidence*, not a finding of this
  phase that P and M are "the same sign". This phase
  tests agreement **conditional on the crosswalk**; it
  does not validate the crosswalk, and no result of
  this phase may be cited as validating any individual
  pair (see §7).
- **A5 — No anchor, prediction, or status
  consequences.** This phase modifies no anchor, issues
  no PRED verdict, and changes no status anywhere. The
  anchors file is never opened for writing under this
  spec; its sha256 at freeze (Appendix A) is asserted
  unchanged at the end of the run.
- **A6 — One verdict, as found.** PASS, FAIL, and
  NULL (starved or inconclusive) are all legitimate
  outcomes, registered in advance with exact patterns
  in §6. The verdict is reported as found; thresholds,
  floors, arms, and the null are not adjustable after
  this freeze (§9).

## 1. The question (registered)

> Do per-sign positional profiles (initial / medial /
> terminal rates) computed **within** the mayig/CISI
> compilation agree with the same profiles computed
> **within** the Holdat compilation, for the same signs
> joined via the Phase-122 crosswalk?

"Agree" is not left as a judgement call: §5 defines the
statistics and §6 the exact numeric patterns that count
as PASS (agreement), FAIL (agreement refuted), and
NULL. §6 is the falsifier.

## 2. Data (frozen inputs)

| Input | Path | Role |
|---|---|---|
| mayig CISI layer v1 | `data/corpus_layers/mayig_cisi_layer_v1.json` (sha256 `6a7664c605079373ca80e70b7e9559c1527613e3f67b579a817ced785e129860`) | mayig-side inscriptions, P-space, keyed by CISI object ID; loaded via `backend/glossa_lab/data/mayig_layer.py` (sha256 `5a6429fdc6e81b9a9f5b2557b7b6fb8ffcdf2e1bf0fba81d1f1cedc5ecc7172e`) |
| Crosswalk v1 | `data/crosswalks/parpola_mahadevan_crosswalk_v1.json` (sha256 `4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb`) + `.csv` (sha256 `3d0b9ef12e6ce4eb8426d449656272365ee157b8c326a130d2261f8e39452823`) | the sole join between P-space and M-space; loaded via `backend/glossa_lab/data/parpola_mahadevan_crosswalk_v1.py` (sha256 `b9caff850508a1eab062a92db131fc2e947e6756edfd642f31ff2c4bc40d430c`) |
| Holdat corpus | `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv` (gitignored; located in the main checkout; sha256 `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`) | Holdat-side inscriptions, M-space; loaded with the `load_holdat_corpus` machinery of `glossa_lab/pipelines/sa_validation.py`, replicated with keys retained exactly as in specs 015/017 (`phase113_run.load_holdat_inscriptions` / `phase117_run` pattern; loader only — no SA code is executed) |
| Anchors (read-only assertion target) | `backend/reports/INDUS_FINAL_ANCHORS.json` (sha256 `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`) | never read as a statistic input, never written; hash asserted unchanged after the run |

Corpus totals (asserted at run time, Appendix A):
mayig layer **179 inscriptions / 1,003 tokens / 182
distinct P signs**; Holdat as loaded **1,670
inscriptions / 7,002 tokens / 390 distinct M signs**.

Holdat is used locally under its recorded terms
(Phase-107 acquisition log); it is never committed or
redistributed. Published artifacts contain only
counts, shares, distances, correlations, and verdicts.
The mayig layer is MIT-licensed (layer metadata) and
committed in-repo.

### 2.1 The object-join discipline — and why no object-matched arm exists (registered at freeze)

The governing discipline, registered here verbatim:
**objects may join only on CISI object ID, and only
where both compilations attest the same object under
that ID.** Under that discipline, this study has **no
object-matched arm**, for a recorded factual reason —
not as a convenience:

- The mayig layer's keys are true CISI object IDs
  (e.g. `M-1`, site prefix + CISI serial).
- Holdat's `cisi_number` is **not** a CISI object ID.
  It is Holdat-internal sequential numbering (spec 015
  §1, established there against the ICIT lineage and
  re-verified at this freeze, counts only): within
  each site prefix the numbers are exactly the
  contiguous range 1..N (M 1..606, H 1..492, L 1..124,
  K 1..110, DK 1..106, C 1..78, SK 1..61, BN 1..60,
  RGR 1..33) — the seal sequence of the compilation
  itself, where N is that site's inscription count in
  Holdat. CISI serials for the same sites run into the
  thousands and are sparse.
- Therefore the zero-padded coincidence (Holdat
  `M-0001` vs mayig `M-1`) is **not** an identity join
  and must never be used as one: normalizing Holdat
  numbers through integer conversion would fabricate
  179/179 "matches" against the mayig object set out
  of pure sequence alignment. Any implementation that
  performs that join is in deviation from this spec
  (§9).

Consequence, registered: the comparison of §5 is a
**sign-level** comparison over each compilation's full
within-compilation inscription set (joined by §3's
crosswalk pairs only). It is not an object-matched /
same-text comparison, and §7's claim scope is written
for exactly that design: compilation-level profile
agreement over substantially overlapping artefact
populations, not agreement on identical texts. (The
same-text question for the Holdat pair was Phase-116's
matcher design; it is not re-run here against mayig,
whose 179-object population the matcher was not frozen
for.)

## 3. Arms — crosswalk confidence gating (frozen)

The comparison unit is a **crosswalk pair** (P, M).
Sign-level comparison uses **only** crosswalk pairs:
a P sign with no pair in an arm contributes nothing to
that arm, and an M sign likewise. Arms differ only in
which pairs they admit; each arm is computed and
reported separately, and **no arm's pairs are ever
silently pooled into another arm's statistics**. Only
the PRIMARY arm carries the §6 verdict.

- **PRIMARY arm.** Pairs with `confidence == "high"`
  (372 pairs, Phase-122) that are additionally
  **unambiguous within the high-confidence pair set**:
  the pair's P sign appears in exactly one
  high-confidence pair and its M sign appears in
  exactly one high-confidence pair. Pairs failing the
  uniqueness rule are **ambiguous** and are excluded
  from the PRIMARY arm (they are handled in arm B);
  P signs with no high-confidence pair — including the
  4 unmapped P signs (`P000`, `P225`, `P261`, `P358`,
  `relation_type == "unmapped"`) — are excluded from
  the PRIMARY arm (handled in arm B where a pair
  exists; unmapped signs have no pair in any arm and
  are counted as non-judgeable in arm B's report).
  Design-stage count (Appendix A): **286 primary
  pairs**.
- **SENSITIVITY arm A (medium-included).** Pairs with
  `confidence` ∈ {high, medium}, with the same
  uniqueness rule applied within that pair set.
  Registered fact (Phase-122 stats, re-verified at
  this freeze): crosswalk v1 contains **zero medium
  pairs** — the canonical-registry and mayig-feature
  pair sets are identical (372/372), so the rubric's
  medium cell is empty. Arm A is therefore expected to
  coincide pair-for-pair with the PRIMARY arm; it is
  run and reported separately anyway, and if it
  coincides, the summary says so explicitly — arm A is
  **not** an independent sensitivity check, and no
  report may present it as one.
- **SENSITIVITY arm B (all-pairs).** **Every** pair
  row in crosswalk v1 (762 pairs: high + medium +
  low), judged **pair-by-pair**: ambiguity is included
  rather than excluded, so a sign appearing in *k*
  pairs contributes *k* pair-comparisons, each
  comparing that sign's within-compilation profile to
  one partner's profile. Counts in arm B are counts of
  **pairs**, never of signs, and arm B's per-pair
  records name both members so the multiplicity is
  auditable. The 4 unmapped P signs are counted in arm
  B's report as non-judgeable (no pair exists).

Conflict flags are **not** an exclusion in any arm:
a pair's `conflict` field records dissent by a
non-canonical source (chiefly crosswalk_v2, rejected
as canonical by spec 018 A.4); the gating variable
frozen here is the v1 `confidence` field plus the
uniqueness rule, exactly as registered above.

## 4. Profiles and attestation floors (frozen)

### 4.1 Profiles

For a sign *s* in a compilation *C*: let
`(nI, nM, nT) = phase113_battery.positional_counts(
inscriptions(C), s)` — counts over *C*'s inscriptions
only (A3). The profile is `(nI, nM, nT) / n(s)` where
`n(s) = nI + nM + nT`. Rates named in §1 are the
profile components: `initial_rate = nI / n(s)`,
`medial_rate = nM / n(s)`, `terminal_rate = nT / n(s)`.

### 4.2 Minimum-attestation floor (frozen)

A pair (P, M) in an arm is **judgeable** in that arm
iff

> `n_mayig(P) ≥ 8` **and** `n_holdat(M) ≥ 8`,

where `n_mayig` / `n_holdat` are the sign's total
token counts **within its own compilation**. Floor
basis: 8 is the program's standing per-compilation
attestation floor for a positional judgment
(spec 011's `T2_MIN_HOLDAT_TOKENS = 8`, carried in
spirit by spec 016/017's per-half floor 4 over two
halves); spec 018's inventory floor (≥ 10) was for a
class-definition inventory over a single large
corpus, and at floor 10 the mayig side — 1,003 tokens
over 182 signs — would leave 12 judgeable primary
pairs, below this spec's own starved bound (§6).
Signs/pairs below the floor are **counted and
excluded, never imputed**: each arm's report records
its pair total, its judgeable count, and its
below-floor count. Design-stage judgeability at
floor 8 (Appendix A): PRIMARY **16** of 286;
arm A **16** of 286 (expected coincidence, §3);
arm B **28** of 762.

## 5. Statistics (frozen)

Computed per arm, over that arm's judgeable pairs
only, in sorted pair order (by P, then M):

- **Per-pair TV distance.** `TV(pair) = ½ Σ |profile
  _mayig(P) − profile_holdat(M)|` over the three
  classes (the `phase113_battery.tv_distance`
  convention). PRIMARY statistic: **median TV** over
  judgeable pairs (type-7 median = the middle value /
  mean of the two middle values — the standard median;
  with an even judgeable count this is the
  linear-interpolation median).
- **Per-pair W1 distance (secondary, recorded, not
  gated).** Ordinal 1-Wasserstein over the ordered
  classes INITIAL < MEDIAL < TERMINAL with unit bin
  spacing: `W1 = |ΔI| + |(pI + pM) − (qI + qM)|`
  (cumulative-share form). Reported as median W1.
- **Spearman rank correlations (gated).** Spearman ρ
  across judgeable pairs between the mayig-side and
  Holdat-side **initial rates**, and separately
  between the two sides' **terminal rates**. Ties are
  handled by average ranks (the standard Spearman
  construction); ρ is the Pearson correlation of the
  rank vectors. If either rank vector is constant (ρ
  undefined), that ρ is recorded as `null` and the
  §6 PASS pattern cannot be met through it (a constant
  rate vector is not agreement evidence). Medial-rate
  ρ is recorded descriptively, not gated (the three
  shares sum to 1, so the medial rate is not an
  independent axis).
- **Modal-class agreement (descriptive, not gated).**
  Share of judgeable pairs whose modal class
  (`phase113_battery.modal_class`, ties INITIAL >
  TERMINAL > MEDIAL) agrees across compilations.
- **Pairing-shuffle permutation null (gated).** The
  blind-affiliation lesson, applied to pairings: an
  agreement claim must beat the agreement obtainable
  from **wrong pairings** of the same profiles. Over
  the arm's judgeable pairs, hold the mayig-side
  profiles fixed in sorted order and permute the
  Holdat-side profiles among the pairs; the replicate
  statistic is the median TV of the permuted pairing.
  **B = 999** replicates, one stream
  `random.Random(125125)` per arm, instantiated fresh
  for each arm in arm order PRIMARY → A → B and
  consumed replicate-by-replicate (each replicate is
  one full shuffle of the Holdat-side profile list).
  `p_null = (1 + #{b : medianTV_b ≤ medianTV_obs}) /
  (1 + B)`. The null distribution's median and 5th
  percentile are recorded alongside `p_null`.

No other statistic is attached to the verdict.
Per-pair records (both profiles, both token counts,
TV, W1) for every arm are published in the results
JSON, judgeable and below-floor alike (below-floor
records carry counts and profiles but no TV/W1 —
a below-floor pair is not scored, per §4.2).

## 6. Verdict rules — the falsifier (frozen)

The verdict is issued **on the PRIMARY arm only**,
mechanically, in this order:

1. **NULL — STARVED** iff the PRIMARY judgeable count
   **< 12**. (Below 12 pairs, a median TV and two
   Spearman coefficients do not support any agreement
   claim either way; a starved test is reported
   starved, not passed and not failed — the
   Phase-118 precedent.) The starved verdict records
   the judgeable count and the floor table; arms A/B
   are still computed and reported descriptively.
2. Otherwise **PASS — agreement** iff **all** of:
   - median TV ≤ **0.35** (the spec-011 T2a positional
     fit bound, carried through specs 016/017
     unretuned — the program's standing "profiles
     fit" number), **and**
   - Spearman ρ(initial rates) ≥ **0.50**, **and**
   - Spearman ρ(terminal rates) ≥ **0.50**, **and**
   - `p_null` ≤ **0.05** (observed agreement beats
     the shuffled-pairing null at the frozen B).
3. Otherwise **FAIL — agreement refuted** iff **both**
   of:
   - median TV ≥ **0.50**, **and**
   - `p_null` > **0.05** (observed pairing no better
     than shuffled pairings).
   
   This is the exact falsifier pattern: the joined
   profiles are far apart in the median (≥ 0.50 is
   far beyond the 0.35 fit bound, in the range the
   Phase-115/116 record associates with genuine
   cross-compilation disagreement) **and** the
   crosswalk pairing itself carries no positional
   information beyond a random re-pairing of the same
   profiles. Either condition alone does not refute:
   large-but-informative distances (median TV ≥ 0.50
   with `p_null` ≤ 0.05) mean the pairing tracks
   real profile structure that is nonetheless not
   agreement — that is INCONCLUSIVE, below, not FAIL.
4. Otherwise **NULL — INCONCLUSIVE**: the registered
   remainder (e.g. median TV in (0.35, 0.50); or a
   PASS leg missed on a correlation while distances
   are small; or the large-but-informative pattern of
   rule 3's note). INCONCLUSIVE is a reported
   outcome, not a failed run.

Sensitivity arms A and B are evaluated against the
same §5 statistics and the same numeric bands
(their PASS/FAIL/NULL pattern is computed by the
same rule, including their own judgeable counts and
their own null streams) and reported in a separate
table. **They do not change the verdict.** If a
sensitivity arm's pattern differs from the PRIMARY
pattern, the summary records the divergence in plain
terms; it does not average, vote, or otherwise
combine arms.

## 7. Claim scope and limitations (registered at freeze)

- A PASS supports exactly this claim: **for the
  judgeable high-confidence unambiguous crosswalk
  pairs, the two compilations' within-compilation
  positional profiles agree at the frozen thresholds,
  beyond shuffled-pairing chance.** It supports no
  claim about any individual sign's identity, reading,
  or crosswalk correctness (A4); no claim about the
  below-floor or ambiguous or low-confidence pairs;
  and no claim about Holdat vs the ICIT lineage
  (Phase-116's R-NONE stands untouched on its own
  pair and its own join).
- A FAIL supports exactly: **crosswalk-joined
  positional agreement between the mayig/CISI layer
  and Holdat is refuted at the frozen thresholds on
  the judgeable primary pairs** — the pairing carries
  no positional agreement beyond shuffled pairings at
  a median distance ≥ 0.50. It does not identify
  which side (transcription, segmentation,
  crosswalk, population) produces the disagreement;
  mechanism attribution would require a successor
  diagnostic spec in the Phase-116 pattern.
- **Population asymmetry (registered):** the mayig
  layer (179 inscriptions) is a small, CISI-volumes
  population; Holdat (1,670 inscriptions) is a larger
  compilation over substantially the same artefact
  population but not the same inscription set (§2.1).
  Profile disagreement can therefore arise from
  population mix as well as from transcription — the
  §6 FAIL pattern's null leg (pairing carries no
  information) is what makes FAIL a statement about
  the *join*, and the summary must carry this
  paragraph's caveat with any FAIL.
- **Power (registered):** at floor 8 the primary arm
  judges 16 pairs (Appendix A). The frozen gates are
  what 16 pairs can bear: a median, two rank
  correlations, and a permutation null. No per-pair
  significance claim is made anywhere in this study.
- **mayig size ceiling:** with 1,003 mayig tokens,
  most attested signs sit below any defensible floor;
  the verdict is a statement about the well-attested
  minority of pairs, counted and named in the
  results — never about "the script" as a whole.

## 8. Implementation (this phase)

Following H15/H23 (graph-first, 5-step gate) and the
Phase-117/118/122 file pattern:

1. `backend/glossa_lab/phase125_cross_compilation.py`
   — pure machinery: arm construction (§3), profiles
   (§4, reusing `phase113_battery` counts/TV/modal
   conventions), Spearman, median TV/W1, the
   pairing-shuffle null (§5), and the §6 verdict
   rule. Pure functions over inscription lists and
   crosswalk rows; no hardcoded corpus data (H16).
2. `backend/glossa_lab/phase125_run.py` —
   orchestration: loads the three frozen inputs
   through their loaders (§2), asserts the corpus
   totals and the anchors hash, computes all arms,
   writes the artifacts. Includes `gpu_device` in its
   report (H20 pattern; no SA is run).
3. `backend/scripts/phase125_cross_compilation.py` —
   the phase script (runner for `phase125_run`).
4. `backend/glossa_lab/experiment_graph_phase125.py`
   — node `IndusPhase125CrossCompilationPositional`,
   registered in `experiment_graph.py` by try/except
   import and asserted present in `ATOMIC_NODES`
   **before** the script is run (H23 steps 2–4
   precede step 5).
5. `backend/tests/test_phase125_cross_compilation.py`
   — unit tests including: arm construction on the
   real crosswalk (372 high / 286 primary / 762
   all-pairs; medium = 0 recorded); judgeability at
   the frozen floor on the real inputs (PRIMARY 16,
   arm B 28); profile/TV/Spearman machinery on toy
   corpora with hand-computed values; the shuffle
   null on a toy pairing where true pairings agree
   (must beat the null) and on a toy pairing where
   they do not; and **toy end-to-end verdict
   controls**: a synthetic agreeing pair-set yields
   PASS, a synthetic disagreeing-and-uninformative
   pair-set yields FAIL, a 5-pair set yields
   NULL-STARVED — all through the real §6 rule.
6. Full backend suite + foundation check (H21 — this
   phase adds phase result files under `reports/`);
   ruff clean.
7. Ledger entries in `LEDGER.md` and
   `glossa-indus/LEDGER.md` (H1), with AI disclosure.
8. One PR; merge only when complete and all CI
   green, per the owner's standing auto-merge rule
   and this phase's authorization. If CI is not
   green, pause and report — do not merge on
   defaults.

## 9. Deviations

Any deviation from this spec discovered during the
execution is recorded in the summary and the ledger,
not absorbed. Thresholds (0.35 / 0.50 / ρ 0.50 /
`p_null` 0.05), the floor (8), the starved bound
(12), the arms, the null (B = 999, seed 125125), and
the verdict rule are not adjustable after the freeze
commit; a substantive design error voids the design
and requires a new spec (Phase-111/112 precedent).

## 10. Deliverables (frozen)

- `specs/019-phase125-cross-compilation-positional/{spec,plan,tasks}.md`
  (spec freeze commit first, before any code)
- `backend/glossa_lab/phase125_cross_compilation.py`,
  `backend/glossa_lab/phase125_run.py`,
  `backend/glossa_lab/experiment_graph_phase125.py`
  (+ registration in `experiment_graph.py`)
- `backend/scripts/phase125_cross_compilation.py`
- `backend/tests/test_phase125_cross_compilation.py`
- `reports/phase125_cross_compilation_results.json`
  (inputs + hashes, arm pair/judgeable/below-floor
  counts, per-pair records, per-arm statistics,
  null summaries, verdict)
- `reports/phase125_cross_compilation_summary.md`
- Anchors file **unchanged** (sha256 asserted)
- Ledger entries in `LEDGER.md` and
  `glossa-indus/LEDGER.md` (AI disclosure); suite +
  foundation results recorded in the summary
- One PR; merged only when complete + green

## Appendix A — Design-stage feasibility (counts only)

*Computed at freeze time, before any comparison
statistic. Boundary: every number below is an
attestation count, a crosswalk pair count, or a
judgeability determination under the frozen
definitions of §§3–4, computed from the three frozen
inputs. No profile was compared to any other profile;
no distance, correlation, or null statistic exists in
this appendix. Per-pair rows are counts, not results.*

### A.1 Inputs

| Input | Count |
|---|---|
| mayig inscriptions / tokens / distinct P signs | 179 / 1,003 / 182 |
| Holdat inscriptions / tokens / distinct M signs | 1,670 / 7,002 / 390 |
| Crosswalk pair rows (+ unmapped-P rows) | 762 (+ 4) |
| Crosswalk confidence: high / medium / low | 372 / **0** / 390 |
| High pairs: distinct P / distinct M | 334 / 359 |

The medium cell is empty because the canonical
registry and mayig-features pair sets are identical
(372/372, Phase-122): the rubric's medium case
(exactly one of the two) never occurs in v1. This is
recorded here so arm A's expected coincidence with
the PRIMARY arm (§3) is a registered design fact,
not a post-hoc discovery.

### A.2 Object-join verification (§2.1 basis)

Holdat `cisi_number` numeric ranges by site prefix
(counts only): M 1..606 contiguous (606 inscriptions),
H 1..492, L 1..124, K 1..110, DK 1..106, C 1..78,
SK 1..61, BN 1..60, RGR 1..33 — each range exactly
1..(that site's Holdat inscription count). Contiguity
is the signature of internal sequential numbering;
CISI serials are sparse and run to > 2,000 for
Mohenjo-daro alone (spec 015 §1: ICIT `cisi` values
`M-1`…`M-2129`). No CISI object-ID join between
Holdat and mayig therefore exists.

### A.3 Judgeability by floor (counts only)

Judgeable pairs (both sides' token counts ≥ floor):

| Floor | PRIMARY (286 pairs) | All high pairs (372) | Arm B — all pairs (762) |
|---|---|---|---|
| ≥ 3 | 43 | 67 | 112 |
| ≥ 5 | 24 | 34 | 48 |
| **≥ 8 (frozen)** | **16** | 21 | **28** |
| ≥ 10 | 12 | 14 | 18 |
| ≥ 15 | 9 | 11 | 14 |
| ≥ 20 | 5 | 7 | 8 |

Floor 8 is frozen (§4.2): it is the standing
per-compilation floor (spec 011), it keeps the
PRIMARY arm above the §6 starved bound (12), and
floor 10 would put the primary arm exactly at that
bound with no margin for a loader discrepancy.
Arm A's judgeable count at floor 8 is 16, over the
same 286 pairs (expected coincidence, §3).
