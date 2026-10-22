# Spec 025 — Stage 2 Controlled Follow-Up

> ## FROZEN — OWNER-ADJUDICATED 2026-10-10 (see §11)
>
> This spec was drafted as a proposal and adjudicated by the
> owner (Tristen Pierson) on 2026-10-10: all six §11 asks were
> answered **with the recommended answers** of the agent's
> recommendation set of the same date. The adjudication record
> (§11) is the governing text wherever it differs from the
> proposal text. Phase-139 (covariate audit + harmonization,
> margins only) is authorized and executes first; Phase-140 is
> gated on the Phase-139 freeze record (plan.md, Freeze gate);
> Phase-141 proceeds per §5 under the same freeze record. No
> other execution is authorized by this freeze.

**Phases:** 139 (covariate audit + harmonization),
140 (controlled F3 re-test), 141 (F1 leave-one-site-out
sensitivity) · **Parent spec:** 024 (Stage 2, complete 2026-10-10) ·
**Date of proposal:** 2026-10-10 · **Frozen:** 2026-10-10 (§11).

**AI disclosure:** this proposal is produced by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

---

## 1. Why this spec exists

Spec 024 Stage 2 closed with a mixed family (BH q = 0.05, m = 3).
Two results carry named, uncontrolled confounders, and this proposal
addresses exactly those — nothing else:

- **F3 (Phase-137, ICIT-lineage layer): site repertoire
  differentiation SUPPORTED** (Cramér's V 0.2190; 0 of 9,999
  composition-controlled permutations ≥ observed). The freeze
  controlled object-type mix and text-length mix. It stated, and
  every report since has repeated, that **period, preservation,
  and excavation history were NOT controlled** — the layer's raw
  period/phase fields were not usable as cross-site covariates
  (§3 of this proposal verifies why, from the file).
- **F1 (Phase-136, ICIT-lineage joined subset): terminal-class ×
  object type SUPPORTED** (common OR 2.384, 95% CI 1.847–3.077)
  over exactly **three** eligible site strata — Mohenjo-daro
  (n = 1,151), Harappa (n = 860), Kalibangan (n = 51). A
  three-stratum result invites the question a sensitivity analysis
  can answer: does the association survive the removal of any one
  stratum? That question was not pre-specified in Spec 024 and
  must not be answered post hoc without a declaration — hence
  this proposal.

No other Spec 024 result is reopened. F2's null stands. Arm (d)
stays descriptive. The motif arm stays closed on its recorded
terms. No anchor, reading, or PRED-2026 state is touched by
anything proposed here (§8).

## 2. Design overview

Two panels, **one declared family** (§6):

| Panel | Member | Kind | Content |
|---|---|---|---|
| Confirmatory | **G1** | New test | F3 site-repertoire re-test on the ICIT-lineage layer with confounder control added to the Phase-137 composition control (§4) |
| Sensitivity | **L-MD, L-HA, L-KA** | Sensitivity analyses of F1 — **not new tests** | Phase-136 design re-run with one eligible stratum dropped in turn (§5) |

G1 is gated on a **covariate stage (Phase-139)** that runs first
and inspects covariate margins only — no repertoire outcome is
computed in Phase-139. If Phase-139 cannot produce comparable,
adequately covered covariates under the rules pre-declared in the
eventual freeze, G1 is recorded **NOT ESTIMABLE** and does not
execute; the proposal says so now so that outcome is a designed
result, not a failure improvised later (§4.4).

## 3. Covariate evidence — verified from the layer file

All numbers below were computed 2026-10-10 directly from the
ICIT-lineage layer file as acquired
(`data/inscriptions.csv`, horus84 lineage; 5,679 rows × 38 fields;
sha256 `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`,
1,190,884 bytes — the same file hash recorded in the Phase-136
inputs). "Informative" means a recorded value other than the
layer's missing sentinels (`-` for period/phase; `- -` for depth).

### 3.1 Fill rates — full layer and F3 analysis population

The F3 analysis population is the Phase-137 population: the 7
sites passing the frozen inclusion rule (≥ 30 inscriptions,
≥ 100 tokens), 5,410 inscriptions.

| Field | Full layer (n = 5,679) | F3 population (n = 5,410) |
|---|---|---|
| `period` informative | 2,318 (40.8%); `-` on 3,361 | 2,266 (41.9%) |
| `phase` informative | 2,652 (46.7%); `-` on 3,025, blank on 2 | 2,638 (48.8%) |
| `depth` numeric with unit (ft/m/cm) | 2,732 (48.1%); `- -` on 2,869 (50.5%) | 2,701 (49.9%) |
| `period` AND `phase` both informative | — | 1,788 (33.0%) |
| All three informative | — | **911 (16.8%)** |
| `preservation` informative (context) | 5,670 (99.8%) | 5,404 (99.9%) |

### 3.2 Missingness is structural, not random

Coverage varies by site in blocks — the fields were recorded by
different excavation/reporting traditions:

| Site | period | phase | depth | all three |
|---|---|---|---|---|
| Harappa | 38.0% | 59.1% | 38.8% | **0.6%** |
| Mohenjo-daro | 41.8% | 41.5% | 72.1% | 41.5% |
| Kalibangan | 74.5% | 59.0% | 3.3% | 2.8% |
| Lothal | 46.2% | 50.5% | 48.1% | 42.8% |
| Dholavira | 58.4% | 0.4% | 0.0% | 0.0% |
| Chanhu-daro | 0.0% | 0.0% | 94.6% | 0.0% |
| Nausharo | 100.0% | 7.9% | 0.0% | 0.0% |

At Harappa, period and phase are informative on almost disjoint
row sets (both together: 0.6%). A complete-case analysis on all
three covariates would keep 16.8% of the population, effectively
reduce the test to Mohenjo-daro + Lothal, and confound
"controlled" with "recorded by a particular tradition". **The
draft therefore does not propose a naive complete-case primary
test.** Any freeze that ignored this table would be freezing a
biased design.

### 3.3 The labels are not cross-site comparable as recorded

Even where filled, the vocabularies are site-local:

- `period`: Harappa uses its own numeric scheme (`3` on 989 rows,
  `2`, `2/3`, …); Mohenjo-daro uses `Early / Intermediate / Late`;
  Lothal uses `Layer 2 … Layer 15`; Dholavira uses `1 … 6`. The
  same numeral does not denote the same chronological unit at two
  sites.
- `phase`: Roman-numeral and letter labels (`I–III`, `B/C`,
  `Stratum II–VI`) recur across sites but name **local** strata,
  not a shared chronology.
- `depth`: mixed units (ft, m, cm), mixed sign/reference
  conventions, ranges and surface notations; absolute depths are
  relative to site- and trench-specific datums.
- Excavation-context fields (`area-section`, `block-house`,
  `room-grid`: 75.0% / 26.6% / 38.6% informative, 202 / 441 / 865
  distinct values) are provenience labels within a site. They are
  not covariates that can be crossed between sites at all.

**Consequence, stated plainly:** no mechanical relabeling of the
raw fields yields a defensible cross-site chronological
covariate. One must either (a) build a harmonization from
published site stratigraphies — an external, interpretive coding
step that must carry provenance and be reviewed as such — or
(b) accept designs that control only what the layer supports
(§4.3), or (c) record G1 NOT ESTIMABLE and let the Phase-137
result stand with its caveat. The owner chooses among these in
§11; the draft recommends (a) with (b) as pre-declared fallback.

## 4. Panel 1 — G1: controlled F3 re-test (Phase-140)

### 4.1 Estimand and statistic (unchanged family)

- **Population:** the Phase-137 F3 population and inclusion rule,
  reused verbatim (7 eligible sites, 5,410 inscriptions; native
  Wells/ICIT sign space; placeholders `000`/`999` excluded;
  signs with layer-wide count ≥ 10 retained, rarer pooled to
  `OTHER`).
- **Statistic:** the Phase-137 statistic family, for
  comparability — Pearson chi-square of the site × sign profile
  table as a divergence statistic; Cramér's V and per-site
  total-variation distances as descriptive effect sizes; all
  inference by permutation (B = 9,999; p = (1 + #{χ²_perm ≥
  χ²_obs}) / (1 + B); seed to be named in the freeze).
- **What changes:** only the permutation's exchangeability
  structure — site labels are permuted **within strata** that
  now cross the Phase-137 composition strata (object-type class
  × length class) with the confounder strata of §4.2. Rows in
  strata containing a single site are constant under permutation
  and contribute nothing; the freeze reports the permutable
  (effective) N alongside the nominal N.

### 4.2 Covariate stage (Phase-139) and the strata the freeze would name

Phase-139 produces, and the freeze then names, the following —
in this order, each step decided on covariate margins only:

1. **Chronology band (`chron_band`).** A harmonization of
   `period`/`phase` into a small number of cross-site bands
   (proposal: three bands — early / middle / late relative to
   each site's published stratigraphic sequence — plus
   `UNRECORDED`), built **only** from published stratigraphic
   sources cited per site, stored as a versioned mapping table
   with per-cell provenance, and graded as constructed context
   (Class C), never as a layer field. If the owner does not
   approve external harmonization (§11 Q2), this step is skipped
   and G1 falls back per §4.3.
2. **Depth band (`depth_band`).** Within each site (and within
   unit/datum group where a site mixes them), parseable depths
   are binned into within-site tertiles (`shallow / mid / deep`)
   + `UNRECORDED`. Within-site relative bands control vertical-
   provenience composition without asserting that an absolute
   depth at one site equals one at another — the draft is
   explicit that this is a relative control, and reports are
   worded accordingly.
3. **Eligibility gate (proposed thresholds, for adjudication):**
   a covariate enters the primary strata only if, on the F3
   population, (i) its harmonized form is recorded (non-
   `UNRECORDED`) for ≥ 70% of inscriptions, (ii) at least 3
   eligible sites retain ≥ 30 inscriptions in the recorded
   subset, and (iii) crossing it with composition leaves
   ≥ 1,000 permutable inscriptions in multi-site strata.
   `UNRECORDED` is retained as its own stratum level so rows are
   not silently dropped; the recorded-coverage share is reported
   with the result, and a result whose control rests on a
   minority recorded share must say so in its headline paragraph.

   **Adjudication amendment (2026-10-10, §11 Q5) — the routing
   rule.** Any approved covariate that *fails* this eligibility
   gate routes automatically to the sensitivity panel (labeled
   EXPLORATORY wherever it appears, reported as bounds, never as
   the controlled verdict). If exactly one covariate passes the
   gate, the primary strata are composition × that covariate.
   If no covariate passes the gate, no primary strata can be
   formed: G1 is recorded NOT ESTIMABLE under §4.3 F-c, with any
   routed sensitivities reported as exploratory bounds only.
   This rule governs the gate-failure case wherever §4.3's
   fallback ladder is silent or in tension with it.

### 4.3 Pre-declared fallbacks (in order)

- **F-a:** chronology harmonized but depth fails the gate →
  primary strata = composition × `chron_band`.
- **F-b:** chronology not approved or not harmonizable → G1 as a
  **confirmatory** test does not run. (Gate failure of an
  approved, harmonized covariate is *not* this case — it is
  governed by the §4.2 routing rule, under which a sole
  gate-passer forms the primary strata and G1 does run.) Two
  sensitivity analyses may run instead, labeled EXPLORATORY
  wherever they appear:
  (i) composition × `depth_band` permutation on the same
  population; (ii) composition × `preservation` permutation
  (`preservation` collapsed to complete / fragment / damaged,
  99.9% filled — the one confounder field the layer records
  near-completely). Neither sensitivity can upgrade, downgrade,
  or replace the Phase-137 verdict; they bound its robustness
  and are reported as bounds.
- **F-c:** no covariate passes and no sensitivity is approved →
  G1 is recorded NOT ESTIMABLE with the §3 tables as its record.

### 4.4 Falsifier

If G1 executes and its BH-adjusted q > 0.05 (§6), the controlled
site-repertoire association is recorded **NOT SUPPORTED under
confounder control on this layer** — reported alongside, never
instead of, the Phase-137 composition-only result, with the
difference between the two designs stated as the finding.

## 5. Panel 2 — F1 leave-one-site-out sensitivity (Phase-141)

- **Design:** the Phase-136 test exactly as frozen (same joined
  subset construction, TERMINAL14 outcome, catalogue object
  type, CMH statistic, within-stratum permutation, B = 9,999),
  run three times with one eligible stratum removed:
  **L-MD** (drop Mohenjo-daro; Harappa + Kalibangan remain),
  **L-HA** (drop Harappa; Mohenjo-daro + Kalibangan remain),
  **L-KA** (drop Kalibangan; Mohenjo-daro + Harappa remain).
- **Estimability:** each subset re-applies the Phase-136 §5 rule
  mechanically (≥ 2 strata; pooled expected counts ≥ 5 in ≥ 80%
  of cells). A subset failing it is reported NOT ESTIMABLE as a
  sensitivity — a designed outcome, especially possible where
  Kalibangan (n = 51) is one of two remaining strata.
- **Robustness criterion (pre-specified here):** F1 is reported
  **stable** iff every estimable subset's Mantel–Haenszel common
  OR remains > 1 with its 95% CI excluding 1. If any estimable
  subset's CI includes 1 or its OR ≤ 1, the report names the
  dropped site as load-bearing and downgrades the F1 summary
  language accordingly ("supported, concentrated in …"). The
  criterion is on effect estimates, deliberately: these are
  sensitivity analyses of an already-decided test, **not new
  tests**, and they mint no verdicts of their own.
- Per-stratum descriptive tables from Phase-136 (already
  published) frame expectations honestly in advance: the three
  stratum ORs were 2.18 (Mohenjo-daro), 2.76 (Harappa), and 1.43
  (Kalibangan, n = 51) — all in the same direction, with
  Kalibangan's precision low by construction.

## 6. Family declaration and correction

- **One family, F25:** { G1, L-MD, L-HA, L-KA }.
- **Correction (as adjudicated, §11 Q4 — option (b)):** G1's
  verdict word (SUPPORTED / NOT SUPPORTED under control) is
  assigned from Benjamini–Hochberg over **G1 alone** at
  q = 0.05 — equivalently, its raw permutation p against 0.05,
  stated as such in every report. The LOSO members mint no
  verdicts and make no discovery claim, so they are **not**
  in the correction denominator: they are reported with raw
  permutation p-values, no q-values are computed for them,
  and the §5 robustness criterion governs their
  interpretation. (The proposal's alternative — BH across all
  executing members — was put to the owner as Q4 and not
  adopted; the choice was made at adjudication, before any
  Phase-139 margins or outcomes were seen.)
- Anything computed outside this declaration is EXPLORATORY,
  labeled as such in every artifact, and excluded from the
  family.

## 7. Provenance and reproducibility requirements

- Graph-first execution per H15/H23 (experiment-graph nodes
  registered and verified before any run); foundation check
  (H21) 0 failures after each phase.
- Anchors asserted byte-identical before and after every run
  (sha256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`).
- The layer file is consumed read-only from its recorded path
  and hash (§3); the Phase-139 harmonization table, if approved,
  is a new versioned artifact with per-cell source citations —
  the layer file itself is never edited.
- Results JSON + report per phase, under the mandatory headline
  label **"ICIT-lineage layer (horus84)"** in every output.

## 8. Epistemic limits (Spec 024 §8-equivalent; binding on all outputs)

1. Every result under this spec describes **the ICIT-lineage
   layer** — a derivative of the ICIT database in open file
   form, not an independent witness — and its joined subsets,
   never "the Indus corpus" in general. The lineage label is
   mandatory in every headline.
2. Associations describe **co-occurrence** in recorded data.
   Repertoire differentiation, controlled or not, is a fact
   about the distribution of sign use as recorded; terminal-
   class association is a fact about use. Neither is evidence
   for regional "dialects" as linguistic entities, for any
   reading of any sign, or for any decipherment claim.
3. **No meaning claims.** Nothing here interprets what a sign,
   a repertoire, or a terminal class means.
4. **No PRED contact.** No output of this spec is an input to
   PRED-2026-001/002/003 scoring, applies a register criterion,
   or runs the PRED dedup protocol. No anchor is minted,
   promoted, demoted, or validated by anything here.
5. Harmonized covariates, if built, are **constructed context
   (Class C)**: their provenance travels with every number that
   uses them, and a result may never be quoted without the
   harmonization's existence and coverage being stated.
6. Compilation-internal explanations remain live alternatives
   for every association: the layer's transcriptions and the
   harmonization's sources sit inside overlapping scholarly
   traditions, and conditioning on recorded covariates cannot
   manufacture independence the data do not have.
7. Negative and NOT ESTIMABLE outcomes are published as found,
   with the same prominence as positive ones.

## 9. Risks and honest weaknesses

- **Harmonization judgment risk:** `chron_band` construction
  involves scholarly judgment about published stratigraphies.
  Mitigation: per-cell citations, a mapping table published with
  the phase report, and the §8.5 labeling rule. If the owner
  judges this risk unacceptable, §4.3 F-b is the designed path.
- **Stratum thinning:** crossing composition × chronology ×
  depth may leave few permutable rows; the §4.2 gate exists to
  detect this on margins before any outcome is computed.
- **Missing-not-at-random:** §3.2 shows covariate missingness is
  structural. `UNRECORDED`-as-stratum preserves rows but cannot
  control what was never recorded; reports must not claim more
  control than the recorded shares support.
- **Kalibangan precision:** L-MD and L-HA both lean partly on a
  51-row stratum; wide intervals there are expected and are
  reported, not smoothed.

## 10. What this spec is not

Not a reopening of Spec 024, not a new study program, not a
data-acquisition spec (no new corpus is sought), not a PRED
evaluation, and not an authorization. If every §11 question were
answered "no", the correct outcome is a one-line record that
Spec 025 was proposed and declined, with F3's caveat standing as
the program's final word on repertoire.

## 11. Adjudication record (owner, 2026-10-10)

Adjudicated by the owner (Tristen Pierson) on 2026-10-10:
**"Adjudicate Spec 025 with the recommended answers and
execute Phase-139."** All six asks are answered with the
recommended answers of the agent's recommendation set of
2026-10-10 (`indus-spec025-recommendations-20261010.md`,
prepared at the owner's request and posted as a comment on
the draft PR). The answers below govern wherever the proposal
text differs.

- **Q1 — Proceed: YES.** Phase-139 (covariate audit +
  harmonization; margins only, no outcome computed) is
  approved and executes first. NOT ESTIMABLE is a designed,
  citable outcome of that phase, not a failure mode.
- **Q2 — Chronology basis: (a)** published-stratigraphy
  harmonization authorized, with the recommendation's three
  conditions: (i) **three bands maximum** (early / middle /
  late relative to each site's published sequence) plus
  `UNRECORDED`; (ii) **per-cell citations or `UNRECORDED`** —
  no cell is forced to chase coverage; (iii) the work is
  scoped to the seven F3 sites' published stratigraphies, a
  mapping table + citations, nothing more (time-boxed at this
  freeze). `chron_band` is constructed context (Class C)
  under §8.5.
- **Q3 — Depth handling: (a)** within-site relative depth
  bands (§4.2 step 2). Option (c), absolute cross-site depth
  harmonization, is **rejected as indefensible** from this
  file (datums are site- and trench-local). Reports repeat
  that the depth control is relative, per §4.2.
- **Q4 — Family accounting: (b)** Benjamini–Hochberg over
  **G1 alone** (§6 as amended). The LOSO members are reported
  with raw permutation p-values, no q-values are computed for
  them, and the §5 robustness criterion governs their
  interpretation. Decided at adjudication, before any
  Phase-139 margins or outcomes were seen; it will not be
  revisited after outcomes are known.
- **Q5 — Estimability thresholds: approved as drafted** —
  ≥ 70% recorded coverage; ≥ 3 eligible sites at ≥ 30
  recorded inscriptions; ≥ 1,000 permutable inscriptions
  (§4.2 step 3). **Plus the pre-declared routing rule** now
  recorded in §4.2: an approved covariate that fails the gate
  routes automatically to the sensitivity panel (EXPLORATORY,
  reported as bounds), and if exactly one covariate passes
  the gate, the primary strata are composition × that
  covariate. The thresholds will not be tuned after
  Phase-139 margins are seen.
- **Q6 — Publication: the standing release path** (repo
  reports + release gate + Zenodo version), as with Spec 024.
  Per the executing instruction for this run, publication
  rides with the Spec 025 outcome record (G1 executed, or the
  NOT ESTIMABLE closeout) — Phase-139 alone does not trigger
  a release. Negative and NOT ESTIMABLE outcomes publish with
  the same prominence as positive ones (§8.7). Repo-local
  only was recommended against and is not adopted.

*Frozen 2026-10-10. Amendments only by a further owner
adjudication, recorded as dated entries in this section.*
